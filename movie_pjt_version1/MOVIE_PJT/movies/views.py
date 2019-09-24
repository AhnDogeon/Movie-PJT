from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from .models import Movie, Score
from .forms import ScoreModelForm
from django.contrib import messages


@require_GET
def movie_list(request):
    allmovies = Movie.objects.all()
    boxoffice = Movie.objects.all()
    boxoffice = list(reversed(sorted(boxoffice, key=lambda boxoffice: int(boxoffice.audience))))
    boxoffice = boxoffice[:10]

    # return JsonResponse({})
    return render(request, 'movies/movie_list.html', {
        'allmovies': allmovies,
        'boxoffice': boxoffice,
    })


@require_GET
def search_movie(request):

    keyword = request.GET.get('q')
    movies = Movie.objects.filter(title_ko__icontains=keyword)

    if keyword == '':
        movies = Movie.objects.all()

    if movies:
        res = serializers.serialize('json', movies)
        return JsonResponse(res, safe=False)
    else:
        movies = Movie.objects.filter(title_en__icontains=keyword)
        if movies:
            res = serializers.serialize('json', movies)
            return JsonResponse(res, safe=False)
        else:
            for i in range(3):
                if i == 0:
                    movies = Movie.objects.filter(actor1=keyword)
                    if movies:
                        res = serializers.serialize('json', movies)
                        return JsonResponse(res, safe=False)
                elif i == 1:
                    movies = Movie.objects.filter(actor2=keyword)
                    if movies:
                        res = serializers.serialize('json', movies)
                        return JsonResponse(res, safe=False)
                elif i == 2:
                    movies = Movie.objects.filter(actor3=keyword)
                    if movies:
                        res = serializers.serialize('json', movies)
                        return JsonResponse(res, safe=False)
            else:
                movies = Movie.objects.filter(genre=keyword)
                if movies:
                    res = serializers.serialize('json', movies)
                    return JsonResponse(res, safe=False)
                else:
                    movies = Movie.objects.filter(nation=keyword)
                    res = serializers.serialize('json', movies)
                    return JsonResponse(res, safe=False)




@require_http_methods(['GET'])
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie.audience = format(int(movie.audience), ',')
    scores = movie.score_set.all()
    return render(request, 'movies/movie_detail.html' ,{
        'movie': movie,
        'movie.audience': movie.audience,
        'scores': scores,
    })

@require_http_methods(['GET', 'POST'])
def movie_update(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        movie.title = request.POST.get('title')
        movie.genre.name = request.POST.get('genre')
        movie.audience = request.POST.get('audience')
        movie.poster_url = request.POST.get('poster_url')
        movie.description = request.POST.get('description')
        movie.save()
        return redirect('movies:movie_detail', movie_id=movie.id)
    else:
        return render(request, 'movies/movie_edit.html', {
            'movie' : movie
        })

@require_http_methods(['POST'])
def movie_delete(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    return redirect('movies:movie_list')

@login_required
@require_POST
def score_create(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    form = ScoreModelForm(request.POST)
    if form.is_valid() == False:
        messages.add_message(request, messages.INFO, '점수와 내용 모두 입력해주세요 😊')
        return redirect('movies:movie_detail', movie.id)
    if form.is_valid():
        score = form.save(commit=False)
        score.movie = movie
        if len(score.content) < 10:
            messages.add_message(request, messages.INFO, '10글자 이상 작성해주세요.😊')
            return redirect('movies:movie_detail', movie.id)
        score.user = request.user
        user_score = Score.objects.all()
        for i in user_score:
            if request.user.id == i.user_id and score.movie.id == i.movie_id:
                messages.add_message(request, messages.INFO, '리뷰가 이미 있습니다.😉')
                # messages.add_message(request, '리뷰가 이미 있습니다.')
                return redirect('movies:movie_detail', movie.id)
        else:
            score.save()
            movie.score_sum += score.value
            movie.average_score = round(movie.score_sum / movie.score_set.count(), 1)
            movie.save()
    return redirect('movies:movie_detail', movie.id)


@require_POST
@login_required
def score_delete(request, movie_id, score_id):
    movie = get_object_or_404(Movie, id=movie_id)
    score = get_object_or_404(Score, id=score_id)
    if request.user == score.user:
        movie.score_sum -= score.value
        score.delete()
        if movie.score_set.all():
            movie.average_score = round(movie.score_sum / movie.score_set.count(), 1)
        else:
            movie.average_score = 0
        movie.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

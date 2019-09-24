from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from .forms import UserCustomAuthenticationForm, UserCustomCreationForm
from .models import User

# Create your views here.
@require_http_methods(["GET", "POST"])
def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:movie_list')
    if request.method == 'POST':
        user_form = UserCustomCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            auth_login(request, user)
            return redirect('movies:movie_list')
    else:
        user_form = UserCustomCreationForm()
    context = {'form': user_form}
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('movies:movie_list')
    if request.method == 'POST':
        login_form = UserCustomAuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            print(request.META.get('HTTP_REFERER'))
            return redirect('movies:movie_list')
    else:
        login_form = UserCustomAuthenticationForm()
    context = {'form': login_form}
    return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('movies:movie_list')


def user_list(request):
    users = User.objects.all()
    return render(request, 'accounts/user_list.html', {
        'users': users
    })

def user_detail(request, username):
   user_info = User.objects.get(username=username)
   return render(request, 'accounts/user_detail.html', {
       'user_info': user_info,
   })

@login_required
@require_POST
def toggle_follow(request, username):
    sender = request.user
    receiver = get_object_or_404(User, username=username)

    if sender != receiver:
        if receiver in sender.followers.all():
            # unfollow
            sender.followers.remove(receiver)
        else:
            # follow
            sender.followers.add(receiver)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/movies/'))

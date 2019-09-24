import requests
import csv

kobis_key = '10438e83037003ef6197b6b8b864d8db'  # key 값 이메일에 있음 붙여넣기
weekly = ['20190512', '20190505', '20190428', '20190421', '20190414', '20190407', '20190331', '20190324', '20190317',
          '20190310', '20190303']


url_list = [f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?key={kobis_key}&targetDt={date}&weekGb=0' for date in weekly]
movie_list = []

moviedb_key = '3211c45ce1cd80c27ffb0a2d34cb4113'

detail_list = []


for x in url_list:
    # 영화진흥위원회에서 boxoffice 정보 받아오기
    data = requests.get(x).json()
    data_info = data['boxOfficeResult']['weeklyBoxOfficeList']

    for i in range(0, 10):
        if data_info[i]['movieCd'] not in movie_list:
            movie_cd = data_info[i]['movieCd']

            # 영화진흥위원회에서 영화코드로 영화 상세정보 받아오기
            xx = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={kobis_key}&movieCd={movie_cd}'
            kobis_detail = requests.get(xx).json()['movieInfoResult']['movieInfo']

            #영화명(영문)
            movie_en = kobis_detail['movieNmEn']
            # 상영시간
            movie_tm = kobis_detail['showTm']
            # 상영국가
            movie_na = kobis_detail['nations'][0]['nationNm']
            # 장르
            movie_ge = kobis_detail['genres'][0]['genreNm']
            # 감독 1명
            movie_di = kobis_detail['directors'][0]['peopleNm']

            # 배우 3명
            if len(kobis_detail['actors']) == 0:
                actor1 = ''
                actor2 = ''
                actor3 = ''
            elif len(kobis_detail['actors']) == 1:
                actor1 = kobis_detail['actors'][0]['peopleNm']
                actor2 = ''
                actor3 = ''
            elif len(kobis_detail['actors']) == 2:
                actor1 = kobis_detail['actors'][0]['peopleNm']
                actor2 = kobis_detail['actors'][1]['peopleNm']
                actor3 = ''
            elif len(kobis_detail['actors']) >= 3:
                actor1 = kobis_detail['actors'][0]['peopleNm']
                actor2 = kobis_detail['actors'][1]['peopleNm']
                actor3 = kobis_detail['actors'][2]['peopleNm']
            # 영화 등급
            movie_au = kobis_detail['audits'][0]['watchGradeNm']

            # 영화 제목에 - 있다면
            movie_name = data_info[i]['movieNm']
            if '-' in movie_name:
                index_num = movie_name.index('-')
                movie_name = movie_name[:index_num]

            # 영화 제목이 그린북이라면
            elif movie_name == '그린 북':
                movie_name = '그린북'

            # 영화 제목이 페이트
            elif '페이트' in movie_name:
                movie_name = '제2장 로스트 버터플라이'

            elif '어스' in movie_name:
                movie_name = movie_en

            # moviedb에서 영화 제목으로 영화 정보 받아오기
            y = f'https://api.themoviedb.org/3/search/movie?api_key={moviedb_key}&query={movie_name}&language=ko-KR'


            # moviedb에 해당 영화가 있다면
            if requests.get(y).json()['results']:
                moviedb_detail = requests.get(y).json()['results'][0]

                moviedb_detail_id = moviedb_detail['id']

                moviedb_image = f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{moviedb_detail['poster_path']}"




            # moviedb에서 영화 예고편 정보 받아오기
            z = f'https://api.themoviedb.org/3/movie/{moviedb_detail_id}/videos?api_key={moviedb_key}&language=ko-KR'
            moviedb_video = requests.get(z).json()['results']

            # moviedb에 예고편이 있다면
            if moviedb_video:
                moviedb_video = moviedb_video[0]
                moviedb_video_url = moviedb_video['key']

            # moviedb에 예고편이 없다면
            else:
                moviedb_video_url = ""

            score_sum = 0
            average_score = 0

            # 영화코드, 영화명(국문), 영화명(영문), 상영시간, 상영국가, 영화장르, 감독1명, 배우3명, 영화상영등급, 누적관객수, 개봉일, 이미지url, 줄거리, 예고편url, 영화 평점, 평균평점
            movie_list += [data_info[i]['movieCd'], data_info[i]['movieNm'], movie_en, movie_tm, movie_na, movie_ge,
                           movie_di, actor1, actor2, actor3, movie_au, format(data_info[i]['audiAcc'],','), data_info[i]['openDt'],
                           moviedb_image, moviedb_detail['overview'], moviedb_video_url, score_sum, average_score]

a = len(movie_list) / 18

for i in range(int(a)):
    b = movie_list[18 * i: 18 * (i + 1)]
    f = open('movie_list.csv', 'a+', encoding='utf-8', newline='')
    writer = csv.writer(f)

    writer.writerow(b)

    f.close()
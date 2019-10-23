- # READ ME  

  ## 1. Project 소개

  ![28조](/assets/28조.gif)

  - 본 프로젝트는 5인 프로젝트로 다양한 기준으로 영화 검색 기능을 구현한 웹 페이지 입니다.
  - 클러스러링 알고리즘(Kmeans, Hierarchical, EM)과 sparse matrix를 사용하여 데이터를 빠르게 전처리 하여 사용자가 편리하게 영화 검색을 할 수 있게 구현했습니다
  - 안도건 : QA, 팀장, 백엔드
  - 곽동령 : 기획, 프론트엔드, 스크럼 마스터 
  - 권성령 : 백엔드
  - 이상택 : 풀스택 
  - 송건호 : 풀 스택 .

  

  ## 2. Project setup

  1. 파이썬 및 pip 설치

     - https://www.python.orf/downlodas 에서 설치
     - 운영 체제에 맞는 최선 버전의 파이썬 설치

  2. Node.js 설치

     - https://nodejs.orf/en/download
     - 운영 체제에 맞는 최선 버전의 Node.js 설치

  3. Backend 설치

     - /backend 디렉토리 진입 후 다음 커멘드 순차적으로 진행

     ```
     pip install -r requirements.txt
     python manage.py makemigrations
     python manage.py migrate
     ```

     - backend 서버 실행

     ```
     python manage.py runserver
     ```

     

  4. Frontend 설치

     - /frontend 디렉토리 진입 후 다음 커멘드 순차적으로 진행

     ```
     npm install
     ```

     - frontend 서버 실행

     ```
     num run serve
     ```

     

  5. Django admin 계정 생성

     - /backend 디렉토리 진입 후

     ```
     python manage.py shell < create_admin.txt
     ```

     

  ## 3. 사용프로그램

  - Pycharm
  - Python
  - Django
  - Node.js
  - vuetity
  - vue + vuex
  - jira
  - git

  

  ## 4. Naming 규칙

  - 본 프로젝트는 아래의 naming 규칙을 따릅니다

  - 모든 글자는 소문자로 작성합니다

  - 카테고리는 (-) 으로 나누고, 띄어쓰기는 (_)를 사용합니다

    

  ### 1) feature naming 규칙

  - 단계-피처명-이름이니셜

    > ex) 00-base_code-dr

  | 단계 |     feature naming      |                         description                          |
  | :--: | :---------------------: | :----------------------------------------------------------: |
  |  00  |        base_code        |                        프로젝트 코드                         |
  |  01  |       age_rating        |              특정 연령대의 유저가 많이 본 영화               |
  |  02  |    occupation_rating    |              특정 직업군의 유저가 많이 본 영화               |
  |  03  |      gender_rating      |               특정 성별의 유저가 많이 본 영화                |
  |  04  |       signup_page       |                  회원가입 화면 및 기능 구현                  |
  |  05  |       login_page        |                   로그인 화면 및 기능 구현                   |
  |  06  |       admin_page        |       관리자로 등록된 사용자만 관리자 화면에 접속 가능       |
  |  07  |     admin_algorithm     | 관리자 화면에서 클러스터링 알고리즘을 선택하고 파라미터를 조절, 실행 가능 |
  |  08  |     admin_data_edit     |   관리자 화면에서 사용자/ 영화를 삭제하고 정보를 수정 가능   |
  |  09  |  clustering_algorithm   |     학습한 알고리즘를 토대로유저와 영화를 클러스터링하기     |
  |  10  | sparse_matrix_algorithm |               sparse_matrix_algorithm 학습하기               |
  |  11  |    kmeans_algorithm     |               kmeans 알고리즘을 직접 구현하기                |
  |  12  |     movie_recommend     | 특정 영화를 선택하면, 클러스터링 알고리즘의 결과를 바탕으로 유사한 영화를 추천 |
  |  13  |     user_recommend      | 특정 유저를 선택하면, 클러스터링 알고리즘의 결과를 바탕으로 유사한 유저들 추천 |

  

  ### 2) commit naming 규칙 

  - 날짜-단계-피처명-설명-이름이니셜

    > ex) 190723-00-base_code-start_project_dr

    

  ## 5. 사이트 화면

  #### 1) homepage('/')

  - 사용자 진화적인 ui를 통해 쉽고 간편하게 영화 검색을 할 수 있게 제작했습니다. 
  - 제목, 장르, 나이, 성별, 직업, 조회순(높은순), 평점순(높은순)으로 검색 가능합니다

  ![홈](/assets/홈.PNG)

  

  #### 2) homepage에서 search 버튼 누르면 기준에 맞는 영화 목록 생성

  - 기준은 제목, 장르, 조회순, 평점순을 제공합니다
  - 카드를 클릭하면 해당 영화의 조회수가 1씩 증가합니다.

  ![22](/assets/22.PNG)

  

  #### 3) homepage에서 오른쪽 하단 유저 아이콘 누르면 userlist 페이지로 이동 ('/user/list/')

  - 해당 페이지는 moviemovie 사이트에 가입된 유저의 전체 리스트를 보여줍니다

  ![33](/assets/33.PNG)

  

  #### 4) userlist 페이지에서 카드 누르면 user 상세 페이지로 이동 ('/user/detail/user_id')

  - 해당 페이지는 유저의 정보와 유저가 평점을 남긴 영화 목록, 유사한 유저 목록을 보여줍니다
  - 영화 제목을 누르면 해당 영화의 상세페이지로 이동합니다

  ![44](/assets/유저.PNG)

  

  #### 5) user 상세 페이지에서 영화 제목을 누르면 해당 영화의 상세 페이지로 이동 ('/movie/detail/movie_id')

  - 해당 페이지는 영화의 제목, 장르, 조회수, 평점, 이 영화에 평점을 남긴 사용자 정보, 유사한 영화 목록을 제공합니다.
  - 사용자 이름을 누르면 해당 사용자의 상세 페이지로 이동합니다.

  ![55](/assets/영화목록.PNG)

  

  ## 6. 프로젝트를 마치며

  - 본 프로젝트를 통해 데이터 파싱과 데이터를 전처리하는 방법을 알게되어서 좋았습니다
  - 데이터를 어떻게 전처리 하냐에 따라 사용자에게 제공할 정보가 달라지기 때문에 먼저 계획을 세우고 코드를 짜는 것이 중요하다는 것을 알게 되었습니다
  - 그렇지 않으면 migrate zero의 늪에 빠지게 된다는 것을 깨달았습니다...
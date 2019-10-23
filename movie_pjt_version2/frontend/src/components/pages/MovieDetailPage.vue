<!-- 영화 상세 페이지 -->
<template>
  <v-container v-if="movieDetail" class="movie-detail">
    <!-- 영화 정보 -->
    <v-layout xs12>
      <p style="font-size: 35px; font-weight: bold; color: whitesmoke; border-bottom: white 1px solid; display: inline; padding-bottom: 10px;">
        {{ movieDetail.title }}
      </p>
    </v-layout>

    <v-layout xs13 class="movie_info" style="width:100%; margin-top: 15px;">

      <div style="display:inline;float:left;width:30%">
        <img :src="movieDetail.poster" alt="포스터" style="width: 90%">
      </div>

      <div class="ml-5 mt-2" style="display:inline;float:left; width:60%">
        <v-rating :value="movieDetail.rating" color="yellow darken-2" background-color="yellow darken-2" large dense half-increments readonly style="display: inline;"/>
        <span style="font-size: 30px; font-weight: 700; margin-left: 10px;">{{ movieDetail.rating }} / 5</span>
        <v-rating v-model="rating" />
        <p class="mt-2" style="font-size: 25px; font-weight: 700;">🍅 Rotten Tomatoes : <a href="https://www.rottentomatoes.com/m/toy_story" target="_blank"><span>{{ movieDetail.ratings['Rotten Tomatoes'] ? movieDetail.ratings['Rotten Tomatoes'] : 'X' }}</span></a></p>
        <p style="font-size: 25px; font-weight: 700;">📣 누적조회수 : {{ movieDetail.viewCnt }} 회</p>
        <p class="movie-info ">✔️ 장르 : <span class="movie-info-text">{{ movieDetail.genres.join(' ') }}</span></p>
        <p class="movie-info">✔️ 제작 국가 : <span class="movie-info-text">{{ movieDetail.country !== "nan" ? movieDetail.country : 'X' }}</span></p>
        <p class="movie-info">✔️ 개봉일 : <span class="movie-info-text">{{ movieDetail.released !== "nan" ? movieDetail.released : 'X' }}</span></p>
        <p class="movie-info">✔️ 상영시간 : <span class="movie-info-text">{{ movieDetail.runtime !== "nan" ? movieDetail.runtime : 'X' }}</span></p>
        <p class="movie-info">✔️ 감독 : <span class="movie-info-text naver_search">{{ movieDetail.director !== "nan" ? movieDetail.director : 'X' }}</span></p>
        <p class="movie-info">✔️ 주연 : <span class="movie-info-text naver_search">{{ movieDetail.actors !== "nan" ? movieDetail.actors : 'X' }}</span></p>
        <span id="test" style="CURSOR: hand; font-weight: 700; margin-bottom: 20%;"
              onclick="if(plain.style.display=='none') {plain.style.display='';test.innerText='✔️  줄거리 접기'} else {plain.style.display='none';test.innerText='✔️  줄거리 보기'}">✔️  줄거리 보기</span>
        <div id="plain" class="mt-2 ml-4" style="display: none">{{ movieDetail.description }}</div>
<!--        <h2 style="color: white; margin-bottom: 10px;">Internet Movie Database : {{ movieDetail.ratings['Internet MovieDatabase'] ? movieDetail.ratings['Internet Movie Database'] : 'X' }}</h2>-->
<!--        <h2 style="color: white; margin-bottom: 10px;">Metacritic : {{ movieDetail.ratings['Metacritic'] ? movieDetail.ratings['Metacritic'] : 'X' }}</h2>-->
      </div>

    </v-layout>


    <!-- 영화 평점 남긴 유저 정보 -->

      <v-layout row xs12 style="margin-top: 15px;">
        <v-flex xs6>
          <h5 style="color: white; font-size: 20px; margin-top: 40px; margin-bottom: 10px;">
            📝 {{ movieDetail.title }} 에 평점을 남긴 사용자입니다
            <hr style="color: white; background-color: white; height: 1px; width: 500px; margin: 10px 0;">
          </h5>

          <div style="height:50vh; overflow:scroll;">
            <router-link v-for="oneDetailUser in movieDetail.seen_users"
                         :to="{name: 'user-detail', params: {user_id: oneDetailUser[1]}}" style="text-decoration: none">
              <p style="color: white; font-size: 18px; font-weight: bold; margin-left: 30px;">- {{ oneDetailUser[0] }}
              </p>
            </router-link>
          </div>
        </v-flex>
        <v-flex xs6>
          <h5 style="color: white; font-size: 20px; margin-top: 40px; margin-bottom: 10px;">🍿 유사한 영화 목록</h5>
          <hr style="color: white; background-color: white; height: 1px; width: 500px; margin: 10px 0;">
          <div v-if="movie_set">
            <router-link v-for="movie in movie_set" :to="{name: 'movie-detail', params: { movie_id: movie.id }}"
                         style="text-decoration: none; color: white; font-size: 20px;"
            >
              <p>{{ movie.title }}</p>
            </router-link>
          </div>
        </v-flex>
      </v-layout>
  </v-container>
</template>
<script>
    import {mapState, mapActions} from "vuex";
    import api from '../../api'

    export default {
        name: "MovieDetailPage",
        component: {},
        props: {
            movie_id: 0
        },
        data() {
            return {
                movie: {},
                movie_set: [],
                params_url: this.$route.params.movie_id,
                rating: 0
            }
        },
        computed: {
            ...mapState({
                oneMovie: state => state.data.oneMovie,
            }),
            movieDetail() {
                return this.$store.state.data.oneMovie[0]
            },
        },
        watch: {
            movie_id: function (res) {
                const params = {
                    "id": res
                };
                this.searchOneMovie(params);
                this.getMovieRecommendation();
            },
            rating: async function () {
                const rating = {
                    "user_id": this.$store.state.data.userInfo.id,
                    "movie_id": Number(this.$route.params.movie_id),
                    "rating_value": this.rating
                };
                const resp = await api.createOrUpdateRating(rating);
                if (resp) {
                    this.searchOneMovie({"id": Number(this.$route.params.movie_id), 'isUpdateRating': true});
                }
            }
        },
        mounted() {
            const params = {
                'id': this.$route.params.movie_id
            };
            this.searchOneMovie(params);
            this.getMovieRecommendation();
            this.getUserRating();
        },
        methods: {
            ...mapActions("data", ["searchOneMovie"]),
            async getMovieRecommendation() {
                const params = {
                    movie_id: this.$route.params.movie_id,
                    fit: 'KMeans_labels'
                };
                const resp = await api.getMovieRecommendation(params);
                const recommendation_set = resp.data.recommendation_set
                this.movie_set = recommendation_set;
            },
            async getUserRating() {
                const rating = {
                    "user_id": this.$store.state.data.userInfo.id,
                    "movie_id": Number(this.$route.params.movie_id)
                };
                const resp = await api.getRating(rating);
                this.rating = resp.data.rating_value ? resp.data.rating_value : 0;
            },
        }

    };
</script>
<style scoped>
  .movie-detail {
    color : white;
  }
  .movie-info {
    font-family: 'Noto Sans';
    font-weight: 700;
  }

  .movie-info-text {
      font-family: 'Noto Sans';
      font-weight: 400;
  }
</style>
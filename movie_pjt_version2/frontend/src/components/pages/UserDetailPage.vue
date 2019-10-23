<!-- 유저 상세 페이지 -->
<template>
  <v-container grid-list-md text-center style="color: white">
    <v-layout justify-center row wrap>

      <!-- 유저 정보 -->
      <v-flex xs12 v-if="oneUser.username!==undefined" style="margin-top: 25px;" class="my-auto">
        <div style="border-radius:5px;  border: white 1px solid; height: 300px; width: 500px; margin: auto; margin-bottom: 50px;">
          <p style="font-size: 50px; margin-top: 20px;">😃</p>
          <p style="font-size: 25px; font-weight: 600;">이름: {{oneUser.username}}</p>
          <p style="font-size: 20px; font-weight: 500;">성별: {{oneUser.gender}}</p>
          <p style="font-size: 20px; font-weight: 500;">나이: {{oneUser.age}}</p>
          <p style="font-size: 20px; font-weight: 500;">직업: {{oneUser.occupation}}</p>
        </div>
      </v-flex>
<!--      영화 추천 기능 knn mf-->
      <v-flex xs6 v-if="oneUser.username!==undefined" style="margin-top: 25px;" class="my-auto">
        <p style="color:white; font-family: 'Anton', sans-serif; font-size: 30px; margin-top: 25px;">🎞️KNN movie Top5</p>
        <hr style="color: white; background-color: white; height: 1px; width: 400px; margin-left: 100px; margin-bottom: 30px;">
        <div style="height: 50vh; overflow: scroll; ">
          <p v-for="oneMovie in oneUser.knn_recommend" >
            <router-link :to="{name: 'movie-detail', params: {movie_id: oneMovie.movieId}}"
                         style="text-decoration: none; color: white; font-size: 25px;">
              {{ oneMovie.title }}
            </router-link>
          </p>
        </div>
      </v-flex>
      <v-flex xs6 v-if="oneUser.username!==undefined" style="margin-top: 25px;" class="my-auto">
        <p style="color:white; font-family: 'Anton', sans-serif; font-size: 30px; margin-top: 25px;">🎞ALS movie Top5</p>
        <hr style="color: white; background-color: white; height: 1px; width: 400px; margin-left: 100px; margin-bottom: 30px;">
        <div style="height: 50vh; overflow: scroll; ">
          <p v-for="oneMovie in oneUser.als_recommend" >
            <router-link :to="{name: 'movie-detail', params: {movie_id: oneMovie.movieId}}"
                         style="text-decoration: none; color: white; font-size: 25px;">
              {{ oneMovie.title }}
            </router-link>
          </p>
        </div>
      </v-flex>

      <!-- 유저가 평점을 남긴 영화 목록 -->
      <v-flex xs6 v-if="oneUser.username!==undefined">
        <p style="color:white; font-family: 'Anton', sans-serif; font-size: 30px; margin-top: 25px;">🎞️ movie list</p>
        <hr style="color: white; background-color: white; height: 1px; width: 400px; margin-left: 100px; margin-bottom: 30px;">
        <div style="height: 50vh; overflow: scroll; ">
          <p v-for="(oneMovie, index) in oneUser.seen_movies" >
            <router-link :to="{name: 'movie-detail', params: {movie_id: oneUser.seen_movies_id[index]}}"
                         style="text-decoration: none; color: white; font-size: 25px;">
              {{ oneMovie }}
            </router-link>
          </p>
        </div>
      </v-flex>

      <v-flex xs6 v-else>
        <h1>잘못된 접근입니다.</h1>
      </v-flex>

      <!-- 해당 유저와 같은 cluster 에 있는 유저 목록 10개 (랜덤) -->
      <v-flex xs6>
        <p style="color:white; font-family: 'Anton', sans-serif; font-size: 30px; margin-top: 25px; font-weight: bold;">📝 유사한 유저 목록</p>
        <hr style="color: white; background-color: white; height: 1px; width: 400px; margin-left: 100px; margin-bottom: 25px;">
        <v-container v-if="user_set">
          <v-layout v-for="user in user_set">
            <router-link :to="{name: 'user-detail', params: { user_id: user.id }}"
                         style="text-decoration: none; color: white; font-size: 25px; margin: auto;">
              {{ user.username }}
            </router-link>
          </v-layout>
        </v-container>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
    import {mapState, mapActions} from "vuex";
    import api from '../../api'

    export default {
        components: {},
        props: {
            user_id: 0
        },
        data: () => ({
            user_set: [],
        }),
        computed: {
            ...mapState({
                oneUser: state => state.data.oneUser[0] === undefined ? {} : state.data.oneUser[0]
            })
        },
        watch: {
          user_id: function(res) {
              const params = {
                  "id": res
              };
              this.getOneUsers(params);
              this.getUserRecommendation();
          }
        },
        mounted() {
            const params = {
                id: this.user_id
            };
            this.getOneUsers(params);
            this.getUserRecommendation();
        },
        methods: {
            ...mapActions("data", ["getOneUsers"]),
            async getUserRecommendation() {
                const params = {
                    user_id: this.user_id,
                    fit: 'KMeans_labels'
                };
                const resp = await api.getUserRecommendation(params);
                const recommendation_set = resp.data.recommendation_set
                this.user_set = recommendation_set;
            },
        }
    };
</script>

<style scoped>
  /*.scroll1::-webkit-scrollbar {*/
  /*  width: 2px;  !* 세로축 스크롤바 길이 *!*/
  /*  color: white;*/
  /*  height: 100%;*/
  /*}*/

</style>
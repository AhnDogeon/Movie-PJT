<!-- 영화 검색 페이지 -->
<template>
  <v-container grid-list-md text-center class="movie-search">
    <v-layout justify-center wrap>
      <!-- 영화 검색 폼 -->
      <v-flex xs6 style="justify-content: center;">
        <router-link :to="{name: 'movie-search'}" style="text-decoration: none;">
        <div class="pa-10" style="color:white; font-family:'lobster', cursive; font-size: 55px;">
        </div>
        </router-link>
        <MovieSearchForm :submit="searchMovies"/>
      </v-flex>

      <!-- 영화 검색 결과 -->
      <v-flex xs7>
        <MovieList :movie-list-cards="movieList"/>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
    import {mapState, mapActions} from "vuex";
    import MovieSearchForm from "../MovieSearchForm";
    import MovieList from "../MovieList";

    export default {
        components: {
            MovieList,
            MovieSearchForm
        },
        data: () => ({}),
        computed: {
            ...mapState({
                movieList: state => state.data.movieSearchList
            })
        },
        mounted() {
            if (this.$store.state.data.title || this.$store.state.data.genres || this.$store.state.data.sortBy || this.$store.state.data.sortingBy) {
                const params = {
                    title: this.$store.state.data.title,
                    genres: this.$store.state.data.genres,
                    sortBy: this.$store.state.data.sortBy,
                    sortingBy: this.$store.state.data.sortingBy,
                };
                this.searchMovies(params);
            }
        },
        methods: {
            ...mapActions("data", ["searchMovies"])
        },
    };
</script>

<style>
  .movie-search {
    background-color: black;
  }
</style>

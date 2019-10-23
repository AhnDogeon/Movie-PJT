<template>
  <v-container class="px-5" fluid grid-list-md>
    <v-layout column>
      <v-flex v-for="(card, index) in movieListCardsSliced" :key="card.id" pa-2>
        <router-link :to="{name: 'movie-detail' , params: {movie_id: card.id, movie_index: index}}" style="text-decoration: none;">
          <MovieListCard
            :id="card.id"
            :img="card.img"
            :title="card.title"
            :genres="card.genres"
            :rating="card.rating"
            :view-cnt="card.viewCnt"
          />
        </router-link>
      </v-flex>
      <v-pagination color="grey darken-5" dark v-if="maxPages > 1" v-model="page" :length="maxPages"
                    style="margin-top: 20px;"/>
    </v-layout>
  </v-container>
</template>

<script>
    import MovieListCard from "./MovieListCard"

    export default {
        components: {
            MovieListCard
        },
        props: {
            movieListCards: {
                type: Array,
                default: () => new Array(),
            },
        },
        data: () => ({
            cardsPerPage: 10,
            page: 1,
        }),
        computed: {
            // pagination related variables
            movieListEmpty: function () {
                return this.movieListCards.length === 0;
            },
            maxPages: function () {
                return Math.floor((this.movieListCards.length + this.cardsPerPage - 1) / this.cardsPerPage)
            },
            movieListCardsSliced: function () {
                return this.movieListCards.slice(this.cardsPerPage * (this.page - 1), this.cardsPerPage * this.page)
            },
        },
    };
</script>

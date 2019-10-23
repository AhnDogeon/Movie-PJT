<template>
  <v-form ref="form" style="width: 60%; margin:auto;">
    <v-text-field dark outlined v-model="title" label="영화 제목" @keyup="onSubmit"/>
    <v-select dark v-model="genres" :items="genresItems" label="장르" item-color="blue-grey lighten-5" outlined
              class=""></v-select>
    <v-layout>
      <v-select dark v-model="sortingBy" :items="agesItems" label="나이" item-color="blue-grey lighten-5" outlined
                ></v-select>
      <v-select dark v-model="sortingBy" :items="genderItems" label="성별" item-color="blue-grey lighten-5" outlined
                class=""></v-select>
      <v-select dark v-model="sortingBy" :items="occupationItems" label="직업" item-color="blue-grey lighten-5"
                outlined
                class=""></v-select>
    </v-layout>


    <v-checkbox dark v-model="sortBy" label="조회순(높은 순)" value="조회순"></v-checkbox>
    <v-checkbox dark v-model="sortBy" label="평점순(높은 순)" value="평점순"></v-checkbox>
    <v-layout justify-center pa-10>
      <v-btn large outlined color="white" @click="onSubmit">Search</v-btn>
    </v-layout>
  </v-form>
</template>

<script>
    export default {
        props: {
            submit: {
                type: Function,
                default: () => {
                }
            }
        },
        data: () => ({
            title: "",
            genres: "All",
            sortBy: "",
            sortingBy: "",
            genresItems: ['All', 'None', 'Animation', "Children's", 'Comedy', 'Adventure', 'Fantasy', 'Romance', 'Drama', 'Action', 'Crime', 'Thriller', 'Horror', 'Sci-Fi', 'Documentary', 'War', 'Musical', 'Mystery', 'Film-Noir', 'Western'],
            sortByItems: ['조회순(높은 순)', '평점순(높은 순)'],
            agesItems: ["-ㅤ", "0~19", "20~29", "30~39", "40~"],
            genderItems: ["-ㅤㅤ", "Male", "Female"],
            occupationItems: ["-ㅤㅤㅤ", 'other', 'academic/educator', 'artist', 'clerical/admin', 'college/grad student', 'customer service', 'doctor/health care', 'executive/managerial', 'farmer', 'homemaker', 'K-12 student', 'lawyer', 'programmer', 'retired', 'sales/marketing', 'scientist', 'self-employed', 'technician/engineer', 'tradesman/craftsman', 'unemployed', 'writer']
        }),
        methods: {
            onSubmit: function () {
                this.$store.state.data.title = this.title;
                this.$store.state.data.genres = this.genres;
                this.$store.state.data.sortBy = this.sortBy;
                this.$store.state.data.sortingBy = this.sortingBy;

                const params = {
                    title: this.$store.state.data.title,
                    genres: this.$store.state.data.genres,
                    sortBy: this.$store.state.data.sortBy,
                    sortingBy: this.$store.state.data.sortingBy,
                };
                this.submit(params);
            },

        }
    };
</script>

<style>
  .v-card {
    width: 90%;
    margin-left: 10px;
    margin-top: 10px;
  }

  .theme--light.v-list {
    background: #000000 !important;
  }

  .v-list-item__content {
    color: white !important;
  }

  .v-select__selections {
    padding: 8px !important;
  }
</style>

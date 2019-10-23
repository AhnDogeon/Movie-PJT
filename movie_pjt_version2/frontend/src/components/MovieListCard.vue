<template>
  <v-hover v-slot:default="{ hover }">
    <v-card :elevation="hover ? 8 : 2" style="width: 80%; margin: auto; background-color: rgb(241,236,236);">
      <v-layout align-center py-4 pl-4>
        <v-flex text-center>
          <v-container grid-list-lg pa-0>
            <v-layout column>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title class="headline" style="color: black;">
                    {{ title }}
                  </v-list-item-title>
                  <v-list-item-subtitle style="color: #263238; margin-top: 10px;">{{ genresStr }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-card-text>
                <v-layout justify-center>
                  <v-rating
                    :value="rating"
                    color="yellow darken-2"
                    background-color="yellow darken-2"
                    half-increments
                    dense
                    readonly
                  />
                  <div style="margin-top: 4px; margin-left: 5px; font-size: 15px; color: #263238;">{{ rating.toFixed(1) }}
                  </div>
                </v-layout>
              </v-card-text>
              <v-card-text>
                <v-layout justify-center>
                  <v-icon color="black">mdi-eye</v-icon>
                  <div style="margin-top: 1px; margin-left: 10px; font-size: 15px; color: #263238;">{{ viewCnt }}</div>
                </v-layout>
              </v-card-text>
            </v-layout>
          </v-container>
        </v-flex>
      </v-layout>
    </v-card>
  </v-hover>
</template>

<script>

    export default {
        props: {
            id: {
                type: Number,
                default: 0
            },
            title: {
                type: String,
                default: ""
            },
            genres: {
                type: Array,
                default: () => new Array()
            },
            img: {
                type: String,
                default: ""
            },
            rating: {
                type: Number,
                default: 0.0
            },
            viewCnt: {
                type: Number,
                default: 0
            }
        },
        computed: {
            genresStr: function () {
                return this.genres.join(" / ");
            },
        }
    };
</script>
<template>
  <v-hover v-slot:default="{ hover }">
    <v-card :elevation="hover ? 8 : 2" style="background-color: rgb(241,236,236);">
      <v-layout align-center py-4>
        <v-flex text-center>
          <v-container grid-list-lg pa-0>
            <v-layout column>
              <v-list-item>
                <v-list-item-content>
                  <p style="font-size: 50px; margin-bottom: 30px; margin-top: 10px;">😃</p>
                  <v-list-item-title class="headline" style="color: black;">
                    {{ username }}
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-card-text>
                <v-layout justify-center column style="font-size: 15px; color: #263238;">
                  <div class="my-1">gender : {{ gender }}</div>
                  <div class="my-1">age : {{ age }}</div>
                  <div class="my-1">occupation : {{ occupation }}</div>
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
            username: {
                type: String,
                default: ""
            },
            is_staff: {
                type: Boolean,
                default: false
            },
            gender: {
                type: String,
                default: ""
            },
            age: {
                type: Number,
                default: 0
            },
            occupation: {
                type: String,
                default: ""
            },
        },
        computed: {}
    };
</script>
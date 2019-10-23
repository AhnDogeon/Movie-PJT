<template>
  <v-app id="app">
    <v-app-bar app clipped-left color="black">
      <img src="../static/netflix.png" @click="goTo('movie-search')" style="width: 230px; margin-top: 70px; margin-left: 640px; ">
      <v-spacer></v-spacer>
      <div v-if="userInfo" style="margin-top: 30px;">
        <span v-if="userInfo.is_staff">
          <v-btn @click="goTo('admin-page')" class="user-button">Admin</v-btn>
        </span>
        <span>
          <v-btn @click="goTo('user-detail')" class="user-button">{{ userInfo.username }}</v-btn>
        </span>
        <v-btn icon @click="goTo('edit-profile')">
          <v-icon style="color: white; font-size: 25px; padding-bottom: 6px;">mdi-clipboard-account</v-icon>
        </v-btn>
        <v-btn icon @click="logout">
          <v-icon style="color: white; font-size: 25px; padding-bottom: 6px;">mdi-power</v-icon>
        </v-btn>
      </div>
      <div v-else>
        <v-spacer></v-spacer>
        <v-dialog v-model="$store.state.authDialog">
          <template v-slot:activator="{ on }">
            <v-btn text style="color:white; background: transparent; font-weight: bolder; font-size: 20px; margin-top: 10px;"
                   v-on="on">
              Login
            </v-btn>
          </template>
          <UserAuth style="width: 60%; margin: auto; height: 500px;"/>
        </v-dialog>
      </div>
    </v-app-bar>

    <v-content>
      <v-container fluid fill-height class="black">
        <v-layout justify-center align-center>
          <!-- each pages will be placed here -->
          <router-view/>
        </v-layout>
      </v-container>
    </v-content>
    <!--   유저 정보     -->
    <v-layout style="position: fixed; z-index: 1000; top: 90%; left: 94%;">
      <v-tooltip top>
        <template v-slot:activator="{ on }" style="margin-top: -10px;">
          <router-link :to="{name: 'user-search'}">
            <v-icon style="color: white; font-size: 40px;" v-on="on">mdi-account-circle</v-icon>
          </router-link>
        </template>

        <span style="top: 100px; left: 90%;">다양한 사용자를 만나보세요</span>
      </v-tooltip>
    </v-layout>
  </v-app>
</template>

<script>
    import router from "./router";
    import UserAuth from "./components/pages/UserAuth"

    export default {
        components: {
            UserAuth
        },
        data: () => ({
            drawer: null,
            choices: [
                {
                    icon: "mdi-movie",
                    text: "영화 검색",
                    path: "movie-search"
                },
                {
                    icon: "mdi-account-circle",
                    text: "유저 정보",
                    path: "user-search"
                },
            ],
        }),
        computed: {
          userInfo() {
              return this.$store.state.data.userInfo
          }
        },
        mounted() {
            const userInfo = localStorage.getItem('userInfo');
            this.$store.commit('data/getUserInfo', JSON.parse(userInfo));
        },
        methods: {
            goTo: function (path) {
                if (path === 'user-detail')
                    router.push({name: path ,params: {"user_id": this.userInfo.id}});
                else
                    router.push({name: path});
            },
            logout() {
                this.$store.commit('data/logout');
            },
        }
    };
</script>

<style>
  #keep .v-navigation-drawer__border {
    display: none;
  }

  .user-button {
    background-color: transparent !important;
    color: white !important;
    font-weight: bolder !important;
    font-size: 20px !important;
  }
</style>

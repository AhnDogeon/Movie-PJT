<!-- 유저 목록 페이지 -->
<template>
  <v-container grid-list-md text-center>
    <v-layout justify-center wrap>
      <!-- 유저 검색 폼 -->
      <v-flex xs6>
        <router-link :to="{name: 'user-search'}" style="text-decoration: none;">
          <div class="pa-10" style="color:white; font-family: 'Anton', sans-serif; font-size: 45px;">user list</div>
        </router-link>
        <UserSearchForm :user-list-cards="userList"/>
      </v-flex>

      <!-- 유저 검색 결과 -->
      <v-flex xs10>
        <UserList :user-list-cards="userList"/>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
    import UserSearchForm from "../UserSearchForm";
    import UserList from "../UserList"

    export default {
        components: {
            UserSearchForm,
            UserList
        },
        data: () => ({}),
        computed: {
            userList() {
                return this.$store.state.data.oneUser.filter(this.callbackSearch)
            }
        },
        mounted() {
            const params = {}
            this.$store.dispatch("data/getOneUsers", params)
        },
        methods: {
            callbackSearch(user) {
                const username = this.$store.state.data.searchTerm;
                return user.username.indexOf(username) !== -1
            },
        },
    };
</script>

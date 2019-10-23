<template>
  <v-container class="pa-2" fluid grid-list-md>
    <v-layout row wrap>
      <v-flex v-for="card in userListCardsSliced" :key="card.id" pa-4 xs3>
        <router-link :to="{name: 'user-detail' , params: {user_id: card.id}}" style="text-decoration: none;">
          <UserListCard style="height: 300px;"
                        :id="card.id"
                        :username="card.username"
                        :is_staff="card.is_staff"
                        :gender="card.gender"
                        :age="card.age"
                        :occupation="card.occupation"
          />
        </router-link>
      </v-flex>
      <v-pagination color="grey darken-5" v-if="maxPages > 1" v-model="page" :length="maxPages"
                    style="margin-top: 20px;"/>
    </v-layout>
  </v-container>
</template>

<script>

    import UserListCard from "./UserListCard";

    export default {
        components: {
            UserListCard
        },
        props: {
            userListCards: {
                type: Array,
                default: () => new Array(),
            },
        },
        data: () => ({
            cardsPerPage: 12,
            page: 1,
        }),
        computed: {
            // pagination related variables
            userListEmpty: function () {
                return this.userListCards.length === 0;
            },
            maxPages: function () {
                return Math.floor((this.userListCards.length + this.cardsPerPage - 1) / this.cardsPerPage)
            },
            userListCardsSliced: function () {
                return this.userListCards.slice(this.cardsPerPage * (this.page - 1), this.cardsPerPage * this.page)
            },
        },
    };
</script>
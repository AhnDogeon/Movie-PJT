<template>
  <v-form ref="form" style="width: 60%; margin:auto;">
    <v-text-field dark outlined v-model="username" @keyup="searchName" label="유저 이름"/>
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
            username: "",
        }),
        methods: {
            searchName() {
                const params = {
                    searchUserName: this.username
                }
                this.$store.commit("data/searchTerm", params)
            },
        },
    }
</script>
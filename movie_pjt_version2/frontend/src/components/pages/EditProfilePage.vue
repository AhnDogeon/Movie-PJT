<template>
  <v-container style="background: white;">
    <v-text-field v-model="userInfo.username" label="이름" readonly/>
    <v-radio-group v-model="userInfo.gender" label="성별" :mandatory="true" row>
      <v-radio label="남자" value="M"/>
      <v-radio label="여자" value="F"/>
    </v-radio-group>
    <v-text-field v-model="userInfo.age" label="나이"/>
    <v-text-field v-model="userInfo.occupation" label="직업"/>

    <p>{{ deadline }}</p>
    <v-radio-group v-model="subscription" label="추가 구독하기" row class="theme--light v-label">
      <v-radio label="일주일 구독" value="7" />
      <v-radio label="한달 구독" value="30" />
      <v-radio label="구독 취소" value="0" />
    </v-radio-group>
    <v-btn color="error" @click="update">수정</v-btn>
  </v-container>
</template>

<script>
    import api from '../../api'

    export default {
        name: "SubscriptionPage",
        data: () => ({
            subscription: -1,
        }),
        computed: {
            userInfo() {
                return this.$store.state.data.userInfo;
            },
            deadline() {
                const date = new Date(Date.now());
                return date > new Date(this.userInfo.subscription) ? "구독이 만료됐습니다." : "구독 만료일 : " + this.userInfo.subscription
            }
        },
        methods: {
            update: async function () {
                const info = {
                    "id": this.userInfo.id,
                    "subscription": Number(this.subscription),
                    "gender": this.userInfo.gender,
                    "age": this.userInfo.age,
                    "occupation": this.userInfo.occupation
                };
                const resp = await api.updateProfile(info);
                const result = resp.data;
                if (result.status) {
                    this.$store.commit('data/login', result.profile);
                    alert('변경이 완료됐습니다.')
                } else {
                    alert('잘못된 접근입니다.')
                }
            }
            ,
        }
    }
</script>

<style scoped>
  .theme--light.v-label {
    color: white;
  }
</style>
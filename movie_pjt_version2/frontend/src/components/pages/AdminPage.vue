<!-- 관리자 상세 페이지 -->
<template>
    <v-container>
        <div v-html="link"/>

        <div row style="background-color:white; ">
            <h1>
                Admin clustering
            </h1>
            <div style="display:flex; justify-content: center">
                <v-select
                        v-model="selectedAlgorithm"
                        style="width:20%; display:inline-block;"
                        :items="algorithmList"
                        label="algorithm"
                />
                <v-text-field v-model="foo" type="number" label="Number"
                              max="10" min="1"
                              style="width:10%; display:inline-block;"
                />
                <v-btn v-if="!axiosState" @click="goSendAlgoRequest()">
                    submit
                </v-btn>
                <v-progress-circular
                        v-else
                        indeterminate
                        color="green"
                />
            </div>

        </div>
        <div row style="background-color:white; ">
            <h1>
                Knn/MatrixFactorization
            </h1>
            <div style="display:flex; justify-content: center">
                <v-select
                        v-model="selectedAlgorithm"
                        style="width:20%; display:inline-block;"
                        :items="algorithmList2"
                        label="algorithm"
                />
                <v-btn v-if="!axiosState" @click="goSendAlgoRequest()">
                    submit
                </v-btn>
                <v-progress-circular
                        v-else
                        indeterminate
                        color="green"
                />
            </div>
        </div>
        <div row style="background-color:white; ">

            <div>
                <h1>결과</h1>
                <p>{{algoResult}}</p>
            </div>
        </div>

        <!-- 영화 정보 -->
    </v-container>
</template>
<script>
    export default {
        name: "AdminPage",
        component: {},
        data() {
            return {
                link: '<a href="http://127.0.0.1:8000/admin/" target=\'_blank\'>to ADMIN</a>',
                selectedAlgorithm: "",
                selectedAlgorithm2: "",
                algorithmList: ["handmade Kmeans clustering", "Kmeans clustering", "Hierarchical clustering", "Gaussian mixture model clustering"],
                algorithmList2: ["KNN", "MatrixFactorization"],
                foo: 1,
                lena: 100,
            }
        },
        computed: {
            axiosState() {
                return this.$store.state.data.axiosState
            },
            algoResult() {
                return this.$store.state.data.algoResult
            },
        },
        watch: {},
        mounted() {
        },
        methods: {
            goSendAlgoRequest() {
                if (this.selectedAlgorithm === "") {
                    alert("알고리즘을 선택해주세요")
                    return
                }
                const params = {
                    selectedAlgorithm: this.selectedAlgorithm,
                    foo: this.foo
                };
                this.$store.dispatch('data/goSendAlgoRequest', params);
            },
        },
    };
</script>

<style>
    a {
        color: whitesmoke !important;
        text-decoration: none;
        font-size: 30px;
        background: transparent;
        font-weight: bold;
        display: inline;
        padding-bottom: 10px;
    }
</style>
// json-server 의 기본 접속 URI 는 아래와 같습니다. 필요에 따라 수정 가능합니다.
const HOST = "http://127.0.0.1:8000";
const app = new Vue({
    el: "#app",
    delimiters: ['${', '}'],
    data: {
        movies: [],
        search: '',
        isDetail: false,
    },
    methods: {
        async searchMovies() {
            const res = await axios.get(`${HOST}/movies/search?q=${this.search}`);

            this.movies = JSON.parse(res.data);
        },

        get_url(id) {
            console.log(id);
            return `http://127.0.0.1:8000/movies/${id}`
        }

    },
    computed: {},

    watch: {
        search: function () {
            this.searchMovies()
        },
        movies () {
            this.isDetail = false;
        },
    },
    async created() {  // Vue 인스턴스가 생성되는 시점에 실행되는 함수입니다. 현재는 Vue 인스턴스가 생성되면, json-server 에서 장르목록만 받아옵니다.
        // const res = await axios.get(`${HOST}/movies/search/`);
        // this.movies = res.data;
        const res = await axios.get(`${HOST}/movies/search?q=`);
        this.movies = JSON.parse(res.data);
    },


});
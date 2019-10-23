import api from '../../api'

// initial state
const state = {
    // shape: [{ id, title, genres, viewCnt, rating }]
    movieSearchList: [],
    oneMovie: [],
    title: '',
    genres: '',
    sortBy: '',
    sortingBy: '',
    oneUser: [],
    searchTerm: "",
    authDialog: false,
    userInfo: JSON.parse(localStorage.getItem('userInfo')),


    //algorithm  result values
    pdfData: "",
    axiosState: false,
    algoResult: [],

    //algorithm result values KNN ALS
    KNNmovies : [],
    ALSmovies : [],
};

// actions
const actions = {
    async getMovieRecommendation({commit}, params) {
        const resp = await api.getMovieRecommendationKNNALS(params);
        const movieRecommend = resp.data;
        commit('setMovieRecommendation', movieRecommend)
    },
    async searchMovies({commit}, params) {
        const resp = await api.searchMovies(params);
        const movies = resp.data.map(d => ({
            id: d.id,
            title: d.title,
            genres: d.genres_array,
            viewCnt: d.views_count,
            rating: d.average_rating,
            seen_users: d.seen_users,
            description: d.description,
            released: d.released,
            runtime: d.runtime,
            director: d.director,
            actors: d.actors,
            country: d.country,
            poster: d.poster,
            ratings: d.ratings_dict
        }));
        commit('setMovieSearchList', movies)
    },
    async searchOneMovie({commit}, params) {
        const resp = await api.searchMovies(params);
        const movies = resp.data.map(d => ({
            id: d.id,
            title: d.title,
            genres: d.genres_array,
            viewCnt: d.views_count,
            rating: d.average_rating,
            seen_users: d.seen_users,
            description: d.description,
            released: d.released,
            runtime: d.runtime,
            director: d.director,
            actors: d.actors,
            country: d.country,
            poster: d.poster,
            ratings: d.ratings_dict
        }));
        commit('setOneMovie', movies)
    },
    async getOneUsers({commit}, params) {
        const resp = await api.getOneUser(params);
        const oneUser = resp.data;
        console.log(oneUser)
        commit('setOneUser', oneUser)
    },
    async login({commit}, params) {
        const resp = await api.login(params);
        const auth = resp.data;
        commit('login', auth)
    },
    goSendAlgoRequest({commit}, params) {
        commit('axiosStateChange', {})
        const gogo = api.goSendAlgo(params)
            .then(resp => commit('goSendAlgoToState', resp.data))
            .catch(err => commit('goSendAlgoToState', "오류가 발생"))
        console.log(gogo)

    }

};

// mutations
const mutations = {
    setMovieRecommendation(state, payload){
        state.KNNmovies = payload["KNN"]
        state.ALSmovies = payload["ALS"]
    },
    axiosStateChange(state, payload) {
        state.axiosState = true
    },
    goSendAlgoToState(state, payload) {
        state.algoResult = payload;
        state.axiosState = false
    },
    setMovieSearchList(state, movies) {
        state.movieSearchList = movies.map(m => m)
    },
    setOneMovie(state, movies) {
        state.oneMovie = movies.map(m => m)
    },
    setOneUser(state, payload) {
        state.oneUser = payload
    },
    searchTerm(state, payload) {
        state.searchTerm = payload.searchUserName
    },
    login(state, payload) {
        localStorage.setItem('userInfo', JSON.stringify(payload));
        state.userInfo = payload;
    },
    logout(state) {
        localStorage.removeItem('userInfo');
        state.userInfo = null
    },
    getUserInfo(state, payload) {
        state.userInfo = payload;
    },
    closeTab(state) {
        state.authDialog = false;
    }
};

export default {
    namespaced: true,
    state,
    actions,
    mutations
}
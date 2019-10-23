import axios from 'axios'

const apiUrl = '/api'

export default {
    getMovieRecommendationKNNALS(params){
        return axios.get(`${apiUrl}/user/`, {
            params,
        })
    },

    goSendAlgo(params){
        return axios.get(`${apiUrl}/cluster/`, {
            params,
        })
    },
    searchMovies(params) {
        return axios.get(`${apiUrl}/movies/`, {
            params,
        })
    },
    getOneUser(params) {
        return axios.get(`${apiUrl}/auth/user/`, {
            params,
        })
    },
    signup(profile) {
        return axios.post(`${apiUrl}/auth/signup/`, {
            profile
        })
    },
    login(profile) {
        return axios.post(`${apiUrl}/auth/login/`, {
            profile
        })
    },
    checkIsDuplicated(params) {
        return axios.get(`${apiUrl}/auth/signup/`, {
            params,
        })
    },
    getUserRecommendation(params) {
        return axios.get(`${apiUrl}/user_recommendation/`, {
            params,
        })
    },
    getMovieRecommendation(params) {
        console.log('########### api index.js 에 들어옴')
        return axios.get(`${apiUrl}/movie_recommendation/`, {
            params,
        })
    },
    updateProfile(profile) {
        return axios.post(`${apiUrl}/auth/update_profile/`, {
            profile
        })
    },
    getRating(params) {
        return axios.get(`${apiUrl}/ratings/`, {
            params
        })
    },
    createOrUpdateRating(rating) {
        return axios.post(`${apiUrl}/create_or_update_rating/`, {
            rating
        })
    }
}
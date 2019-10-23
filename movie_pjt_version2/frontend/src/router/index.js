import Vue from 'vue'
import VueRouter from 'vue-router'
import MovieSearchPage from '../components/pages/MovieSearchPage'
import UserSearchPage from "../components/pages/UserSearchPage"
import MovieDetailPage from '../components/pages/MovieDetailPage'
import UserDetailPage from '../components/pages/UserDetailPage'
import UserSignupPage from "../components/pages/UserSignupPage";
import AdminPage from "../components/pages/AdminPage";
import EditProfilePage from "../components/pages/EditProfilePage";
import store from "../store"

Vue.use(VueRouter)

const router = new VueRouter({
    mode: 'history',
    routes: [
        {path: '/', component: MovieSearchPage, name: 'movie-search'},
        {
            path: '/admin',
            component: AdminPage,
            name: 'admin-page',
            beforeEnter: function(to, from, next) {
                console.log(store.state.data.userInfo)
                if (store.state.data.userInfo && store.state.data.userInfo.is_staff) {
                    next()
                } else {
                    alert('접근 권한이 없습니다.')
                    next(from)
                }
            }
        },
        {path: '/user/list/', component: UserSearchPage, name: 'user-search'},
        {path: '/user/signup/', component: UserSignupPage, name: 'user-signup'},
        {path: '/user/detail/:user_id', component: UserDetailPage, name: 'user-detail', props: true},
        {
            path: '/movies/detail/:movie_id',
            component: MovieDetailPage,
            name: 'movie-detail',
            props: true,
            beforeEnter: function(to, from, next) {
                if (store.state.data.userInfo) {
                    if (new Date(store.state.data.userInfo.subscription) > new Date(Date.now())) {
                        next()
                    } else {
                        alert("개인정보 수정 페이지에서 구독 기간을 연장해주세요!");
                        next(from)
                    }
                } else {
                    alert('로그인해주세요!');
                    next(from)
                }
            }
        },
        {
            path: '/user/edit/',
            component: EditProfilePage,
            name: 'edit-profile',
            beforeEnter: function(to, from, next) {
                if (store.state.data.userInfo) {
                    next()
                } else {
                    alert('로그인해주세요!');
                    next(from)
                }
            }
        },
        {path: ''}
    ],
    scrollBehavior() {
        return {x: 0, y: 0}
    },
});

export default router
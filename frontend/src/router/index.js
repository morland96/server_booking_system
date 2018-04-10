import Vue from 'vue'
import Router from 'vue-router'
import Vuex from 'vuex'
import HelloWorld from '@/components/HelloWorld'
const Home = () => import('@/components/Home')
const About = () => import('@/components/About')
const Book = () => import('@/components/Book')
const Login = () => import('@/components/Login')
const routes = [
  { path: '/', component: Home },
  { path: '/Home', component: Home, meta: { requireAuth: true } },
  { path: '/About', component: About },
  { path: '/HelloWorld', component: HelloWorld },
  { path: '/Book', component: Book, meta: { requireAuth: true } },
  { path: '/Login', component: Login }
]
Vue.config.is_login = false
Vue.use(Router)
Vue.use(Vuex)

const router = new Router({
  routes,
  mode: 'history'
})
router.beforeEach((to, form, next) => {
  if (store.state.token) {
    next()
  } else {
    next({
      path: '/login',
      query: {redirect: to.fullPath}
    })
  }
})
export default router

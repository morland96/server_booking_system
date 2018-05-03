import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import store from '../store'
import axios from '../http'
const Home = () => import('@/components/Home')
const About = () => import('@/components/About')
const Book = () => import('@/components/Book')
const Manage = () => import('@/components/Manage')
const TimeTable = () => import('@/components/TimeTable')
const Login = () => import('@/components/Login')
const routes = [
  { path: '/', component: Home, meta: { requireAuth: true } },
  { path: '/Home', component: Home, meta: { requireAuth: true } },
  { path: '/About', component: About, meta: { requireAuth: true } },
  { path: '/HelloWorld', component: HelloWorld },
  { path: '/Book', component: Book, meta: { requireAuth: true } },
  {
    path: '/Manage',
    component: Manage,
    meta: { requireAuth: true, requireAdmin: true }
  },
  { path: '/TimeTable', component: TimeTable, meta: { requireAuth: true } },
  { path: '/Login', component: Login }
]
Vue.use(Router)

const router = new Router({
  routes,
  mode: 'history'
})
router.beforeEach((to, form, next) => {
  if (to.meta.requireAuth) {
    if (store.getters.token) {
      axios.get('/api/v1.0/user').then(function (response) {
        store.commit('updateInfo', response.data)
        if (to.meta.requireAdmin) {
          if (store.state.UserInfo.user.privilege !== '1') {
            router.push('/')
          }
        }
      })
      next()
    } else {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    }
  } else {
    next()
  }
})
export default router

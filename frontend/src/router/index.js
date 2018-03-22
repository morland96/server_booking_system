import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Home from '@/components/Home'
import About from '@/components/About'
import Book from '@/components/Book'
const routes = [
  { path: '/', component: Home },
  { path: '/Home', component: Home },
  { path: '/About', component: About },
  { path: '/HelloWorld', component: HelloWorld },
  { path: '/Book', component: Book }
]
Vue.use(Router)

export default new Router({
  routes,
  mode: 'history'
})

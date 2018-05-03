// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import store from './store'
import 'element-ui/lib/theme-chalk/index.css'
import axios from './http'
import echarts from 'echarts'

/* eslint-disable no-new */
Vue.config.productionTip = false
Vue.use(ElementUI)
Vue.prototype.axios = axios

new Vue({
  el: '#app',
  router,
  components: { App },
  store,
  echarts,
  template: '<App/>'
})

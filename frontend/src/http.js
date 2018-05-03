import axios from 'axios'
import store from './store/index'
import router from './router'
axios.defaults.timeout = 5000
axios.interceptors.request.use(
  config => {
    if (store.getters.token) {
      config.headers['Authentication-Token'] = store.getters.token
    }
    return config
  },
  err => {
    console.log('error')
    return Promise.reject(err)
  }
)
axios.interceptors.response.use(
  response => {
    return response
  },
  error => {
    if (error.response) {
      switch (error.response.status) {
        case 401:
          store.commit('logout')
          router.replace({
            path: 'login',
            query: { redirect: router.currentRoute.fullPath }
          })
          break
        case 403:
          return Promise.reject(error)
      }
    }
  }
)
export default axios

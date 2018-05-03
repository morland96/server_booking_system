const state = {
  token: null,
  user: {'username': ''}
}
const getters = {
  token (state) {
    if (!state.token) {
      state.token = localStorage.getItem('session')
      console.log(localStorage.getItem('session'))
    }
    return state.token
  }
}
const mutations = {
  login (state, { token, user }) {
    state.token = token
    state.user = user
    localStorage.setItem('session', token)
  },
  updateInfo (state, user) {
    state.user = user
  },
  logout () {
    state.token = null
    state.user = null
    localStorage.removeItem('session')
  }
}
export default {
  state,
  getters,
  mutations
}

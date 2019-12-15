import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import { HTTP } from '../api/common'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    status: '',
    token: localStorage.getItem('token') || '',
    user: {},
    refresh_token: localStorage.getItem('refresh_token') || '',
    token_type: '',
    access_token: localStorage.getItem('access_token') || ''
  },
  mutations: {
    auth_request (state) {
      state.status = 'loading'
    },
    auth_success (state, token, user) {
      state.status = 'success'
      state.token = token
      state.user = user
    },
    auth_error (state) {
      state.status = 'error'
    },
    logout (state) {
      state.status = ''
      state.token = ''
      state.access_token = ''
      state.token_type = ''
      state.refresh_token = ''
    },
    oauth_success (state, payload) {
      state.status = 'success'
      state.access_token = payload.a_token
      state.token_type = payload.type
      state.refresh_token = payload.r_token
    }
  },
  actions: {
    login ({ commit }, user) {
      return new Promise((resolve, reject) => {
        commit('auth_request')
        HTTP.post('/auth/', user)
          .then(resp => {
            const token = resp.data.token
            const user = resp.data.user
            localStorage.setItem('token', token)
            axios.defaults.headers.common['Authorization'] = token
            commit('auth_success', token, user)
            resolve(resp)
            console.log('success')
          })
          .catch(err => {
            commit('auth_error')
            localStorage.removeItem('token')
            reject(err)
          })
      })
    },
    oauth_login ({ commit }, data) {
      const Atoken = data.access_token
      const Ttype = data.token_type
      const Rtoken = data.refresh_token
      const tokens = { 'a_token': Atoken, 't_type': Ttype, 'r_token': Rtoken }
      localStorage.setItem('access_token', Atoken)
      commit('oauth_success', tokens)
      axios.defaults.headers.common['Authorization'] = Ttype + ' ' + Atoken
    },
    logout ({ commit }) {
      return new Promise((resolve, reject) => {
        commit('logout')
        localStorage.removeItem('token')
        localStorage.removeItem('access_token')
        delete axios.defaults.headers.common['Authorization']
        resolve()
      })
    }
  },
  modules: {
  },
  getters: {
    isLoggedIn: state => !!state.token || !!state.access_token,
    authStatus: state => state.status
  }
})

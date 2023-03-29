import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import router from '../router'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user_id: localStorage.getItem('user_id') || null,
    token: localStorage.getItem('token') || null
  },
  getters: {
    USER_ID(state) {
      return state.user_id
    },
    TOKEN(state) {
      return state.token
    },
    IS_AUTHENTICATED(state) {
      return !!state.token
    }
  },
  mutations: {
    SIGNUP_MUTATION(state, payload) {
      state.token = payload.data.token
      state.user_id = payload.user_id
    },
    LOGIN_MUTATION(state, payload) {
      state.token = payload.data.token
      state.user_id = payload.user_id
    },
    LOGOUT_MUTATION(state) {
      state.token = null
      state.user_id = null
    },
  },
  actions: {
    async SIGNUP_ACTION({ commit }, payload) {
      try {
        const { data } = await axios.post('http://localhost:5000/api/v1/signup', payload, {
          headers: {
            'Content-Type': 'multipart/form-data',
          }
        })
        localStorage.setItem('token', data.token)
        const user_id = JSON.parse(atob(data.token.split('.')[1])).u_id
        localStorage.setItem('user_id', user_id)
        router.push('/dashboard')
        commit('SIGNUP_MUTATION', {data, user_id})
      } catch (error) {
        console.log(error)
      }
    },
    async LOGIN_ACTION({ commit }, payload) {
      try {
        const { data } = await axios.post('http://localhost:5000/api/v1/login', payload)
        localStorage.setItem('token', data.token)
        const user_id = JSON.parse(atob(data.token.split('.')[1])).u_id
        localStorage.setItem('user_id', user_id)
        router.push('/dashboard')
        commit('LOGIN_MUTATION', { data, user_id })
      } catch (error) {
        console.log(error)
      }
    },
    LOGOUT_ACTION({ commit }) {
      commit('LOGOUT_MUTATION')
      localStorage.removeItem('token')
      router.push('/')
    },
  },
  modules: {
  }
})

import { login, logout, getInfo } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'
import router, { resetRouter } from '@/router'
import { test } from '@/api/api';
import axios from 'axios'
import Cookies from 'js-cookie'
import md5 from 'js-md5'

const state = {
  token: getToken(),
  name: '',
  avatar: '',
  introduction: '',
  roles: []
}

const mutations = {
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_INTRODUCTION: (state, introduction) => {
    state.introduction = introduction
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_ROLES: (state, roles) => {
    state.roles = roles
  }
}

const actions = {
  // user login
  login({ commit }, userInfo) {
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: md5(password) }).then(res => {
        const { msg, code, data } = res
        if (code === '999999') {
            const token = data.role + '-token'
            sessionStorage.setItem('username', data.username);
            sessionStorage.setItem('token', data.ticket);
            sessionStorage.setItem('name', data.name);
            sessionStorage.setItem('role', data.role);
            var expire = new Date(new Date().getTime() + data.expire * 1000);
            Cookies.set("ticket",data.ticket,{expires: expire});
            Cookies.set("username",data.username,{expires: expire});
            Cookies.set("userid",data.userid,{expires: expire});
            Cookies.set("name",data.name,{expires: expire});
            Cookies.set("role",data.role,{expires: expire});
            commit('SET_TOKEN', token);
            setToken(token);
            resolve();
        }else {
            //reject();
            //this.loading = false;
            //_this.$message.error({
            //    message: msg,
            //    center: true
            //})
        }
      }).catch(error => {
        reject(error)
      })

      //var loginParams = { username: username.trim(), password: md5(password) }
      //axios.post(`${test}/api/user/login`, loginParams).then(res => {
      //    console.log(3);
      //    let { msg, code, data } = res.data;
      //    if (code === '999999') {
      //        sessionStorage.setItem('username', JSON.stringify(data.username));
      //        sessionStorage.setItem('token', JSON.stringify(data.ticket));
      //        sessionStorage.setItem('name', JSON.stringify(data.name));
      //        sessionStorage.setItem('role', JSON.stringify(data.role));
      //        var expire = new Date(new Date().getTime() + data.expire * 1000);
      //        Cookies.set("ticket",data.ticket,{expires: expire});
      //        Cookies.set("username",data.username,{expires: expire});
      //        Cookies.set("userid",data.userid,{expires: expire});
      //        Cookies.set("name",data.name,{expires: expire});
      //        Cookies.set("role",data.role,{expires: expire});
      //        commit('SET_TOKEN', JSON.stringify(data.ticket));
      //        setToken(JSON.stringify(data.ticket));
      //        console.log(4);
      //        //resolve();
      //    }else {
      //        //reject();
      //        //this.loading = false;
      //        //_this.$message.error({
      //        //    message: msg,
      //        //    center: true
      //        //})
      //    }
      //});
    })
  },

  // get user info
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo(state.token).then(response => {
        const { data } = response

        if (!data) {
          reject('Verification failed, please Login again.')
        }

        const { roles, name, avatar, introduction } = data

        // roles must be a non-empty array
        if (!roles || roles.length <= 0) {
          reject('getInfo: roles must be a non-null array!')
        }

        commit('SET_ROLES', roles)
        commit('SET_NAME', name)
        commit('SET_AVATAR', avatar)
        commit('SET_INTRODUCTION', introduction)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // user logout
  logout({ commit, state, dispatch }) {
    return new Promise((resolve, reject) => {
      logout(state.token).then(() => {
        commit('SET_TOKEN', '')
        commit('SET_ROLES', [])
        removeToken()
        resetRouter()

        // reset visited views and cached views
        // to fixed https://github.com/PanJiaChen/vue-element-admin/issues/2485
        dispatch('tagsView/delAllViews', null, { root: true })

        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      commit('SET_TOKEN', '')
      commit('SET_ROLES', [])
      removeToken()
      resolve()
    })
  },

  // dynamically modify permissions
  changeRoles({ commit, dispatch }, role) {
    return new Promise(async resolve => {
      const token = role + '-token'

      commit('SET_TOKEN', token)
      setToken(token)

      const { roles } = await dispatch('getInfo')

      resetRouter()

      // generate accessible routes map based on roles
      const accessRoutes = await dispatch('permission/generateRoutes', roles, { root: true })

      // dynamically add accessible routes
      router.addRoutes(accessRoutes)

      // reset visited views and cached views
      dispatch('tagsView/delAllViews', null, { root: true })

      resolve()
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

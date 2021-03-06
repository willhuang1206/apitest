import Vue from 'vue'
import 'normalize.css/normalize.css' // a modern alternative to CSS resets
import Element from 'element-ui'
import './styles/element-variables.scss'
import '@/styles/index.scss' // global css
import App from './App'
import store from './store'
import router from './router'
import md5 from 'js-md5'
import './icons' // icon
import './permission' // permission control
import './utils/error-log' // error log
import moment from 'moment'
import Cookies from 'js-cookie'
import JsonViewer from 'vue-json-viewer'
import echarts from 'echarts'

import * as filters from './filters' // global filters

/**
 * If you don't want to use mock-server
 * you want to use MockJs for mock api
 * you can execute: mockXHR()
 *
 * Currently MockJs will be used in the production environment,
 * please remove it before going online ! ! !
 */
if (process.env.NODE_ENV === 'production') {
  const { mockXHR } = require('../mock')
  mockXHR()
}

Vue.use(Element, {
  size: Cookies.get('size') || 'medium' // set element-ui default size
})
Vue.use(JsonViewer);

// register global utility filters
Object.keys(filters).forEach(key => {
  Vue.filter(key, filters[key])
})

Vue.config.productionTip = false
Vue.prototype.md5 = md5
Vue.prototype.$moment = moment;
Vue.prototype.$echarts = echarts;

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})

router.beforeEach((to, from, next) => {
  if (to.path === '/login') {
    sessionStorage.removeItem('token')
  }
  const ticket = Cookies.get('ticket')
  //  let token = JSON.parse(sessionStorage.getItem('token'));
  if (!ticket && to.path !== '/login') {
    console.log(to.path)
    next({ path: '/login', query: { url: to.path }})
  } else {
    next()
  }
  if (to.path === '/') {
    next({ path: '/projectList' })
  }
})

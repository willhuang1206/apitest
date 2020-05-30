import axios from 'axios';
import router from 'vue-router'
import Cookies from 'js-cookie'
import {MessageBox} from 'element-ui';
//export const test = 'http://127.0.0.1:8092';
export const test = 'http://106.53.246.180:8092';

export const requestLogout = params => { return axios.get(`${test}/api/user/logout`, params).then(res => res.data); };
// 获取全局配置列表
export const getProjectConfig = (headers, params) => {
    return axios.get(`${test}/api/project/config_list`, { params: params, headers:headers}).then(res => res.data); };
// 获取全局配置列表
export const getGlobalPublish = (headers, params) => {
    return axios.get(`${test}/api/global/publish_list`, { params: params, headers:headers}).then(res => res.data); };
// 获取项目动态
export const getProjectDynamicList = (headers, params) => {
    return axios.get(`${test}/api/dynamic/dynamic`, { params: params, headers:headers}).then(res => res.data); };
// 运行自动化用例
export const runAutomation = (headers,params) => {
    return axios.post(`${test}/api/automation/run`, params, {headers}).then(res => res.data); };

// 默认超时设置
axios.defaults.timeout = 10000;
// 相对路径设置
axios.defaults.baseURL ='';
axios.defaults.crossDomain = true;
axios.defaults.withCredentials  = true;
//http request 拦截器
axios.interceptors.request.use(
  config => {
    // 获取token
    const ticket = Cookies.get('ticket');
    // 添加token到headers
    if(ticket){
      config.headers.Authorization = ticket;
    }
    ////参数处理
    //if(config.method === 'get' && config.url !== '/api/user/login'){
    //  config.params = config.params;
    //}else if(config.url !== '/api/user/login'){
    //  config.data = config.data || {};
    //  config.params = config.params || {'ticket': ticket};
    //}
    return config;
  },
  err => {
    return Promise.reject(err);
  }
);


//http response 拦截器
axios.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    if (error.response) {
        switch (error.response.status) {
            case 403:
                // 返回 401 清除token信息并跳转到登录页面
                sessionStorage.removeItem('token');
                Cookies.remove('ticket');
                //router.replace({
                //    path: 'login',
                //    query: {redirect: router.currentRoute.fullPath}
                //});
                MessageBox.alert("登录信息超时,请重新登录!","登录超时",{
                  confirmButtonText:"跳转登录页面",
                  callback:action => {
                    window.location.href="/";
                  }
                });
            case 406:
                // 返回 401 清除token信息并跳转到登录页面
                //router.replace({
                //    path: 'login',
                //    query: {redirect: router.currentRoute.fullPath}
                //});
                MessageBox.alert("没有权限执行该操作!","没有权限",{
                  confirmButtonText:"关闭",
                  callback:action => {
                    history.go(0);
                  }
                });
        }
    }
    return Promise.reject(error.response.data);   // 返回接口返回的错误信息
  }
);


/**
 * fetch 请求方法
 * @param url
 * @param params
 * @returns {Promise}
 */
export function fetch(url, params = {}) {

    return new Promise((resolve, reject) => {
        axios.get(url, {
            params: params
        })
        .then(response => {
            resolve(response.data);
        })
        .catch(err => {
            reject(err)
        })
    })
}

/**
 * post 请求方法
 * @param url
 * @param data
 * @returns {Promise}
 */
export function post(url, data = {}) {
    return new Promise((resolve, reject) => {
        axios.post(url, data)
            .then(response => {
                resolve(response.data);
            }, err => {
                reject(err);
            })
    })
}

/**
 * patch 方法封装
 * @param url
 * @param data
 * @returns {Promise}
 */
export function patch(url, data = {}) {
    return new Promise((resolve, reject) => {
        axios.patch(url, data)
            .then(response => {
                resolve(response.data);
            }, err => {
                reject(err);
            })
    })
}

/**
 * put 方法封装
 * @param url
 * @param data
 * @returns {Promise}
 */
export function put(url, data = {}) {
    return new Promise((resolve, reject) => {
        axios.put(url, data)
            .then(response => {
                resolve(response.data);
            }, err => {
                reject(err);
            })
    })
}

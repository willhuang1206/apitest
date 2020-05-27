import request from '@/utils/request'
//  import { test } from '@/api/api'

//export function login(data) {
//  return request({
//    url: '/vue-element-admin/user/login',
//    method: 'post',
//    data
//  })
//}

export function login(data) {
  return request({
    url: 'http://localhost:8092/api/user/login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/vue-element-admin/user/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/vue-element-admin/user/logout',
    method: 'post'
  })
}

import request from '@/utils/request'
/* 登陆接口 */
import { post , get} from '@/utils/request'
import qs from 'qs'
// Form Data 格式
let isForm = { 'Content-Type': 'application/x-www-form-urlencoded' }

// 登录
export function loginUrl (params) {
  return post('/api/user/v1.0/login', qs.stringify(params), isForm)
}

// 登录 带锁定的lock
export function loginLockUrl (params) {
  return post('/api/userlock/v1.0/login', qs.stringify(params), isForm)
}

// 验证码
export function codeImage () {
  return get('/api/kaptcha/image', '', isForm)
}

// 登录 需要验证码
export function loginByCodeUrl (params) {
  return post('/api/userlock/v1.0/loginByCode', qs.stringify(params), isForm)
}

// 后端登录调取用户信息
export function loginUserInfo () {
  return get('/api/user/v1.0/userInfo', '', isForm)
}
// 后端退出登录
export function logout () {
  return get('/api/system/v1.0/logout', '', isForm)
}

// 后端登录调取用户信息
export function ssologinUserInfo(token) {
  // return get('/api/pa/ssologin/login' + '?token=' + token)
  return request({
    url: '/api/user/v1.0/loginByTPToken',
    data: token,
    method: 'post',
  })
}

//广发智汇的单点登陆
export function ssologinUserInfoGFWisdom(code) {
  // return get('/api/pa/ssologin/login' + '?token=' + token)
  return request({
    url: '/api/gfwisdom/user/sso/loginByGFWisdomCode?code=' + code,
   // data: {code:code},
    method: 'post',
  })
}
export function ssologinUserInfoGlr(token) {
  // return get('/api/pa/ssologin/login' + '?token=' + token)
  return request({
    url: '/api/user/sso/loginByTPTokenGlr',
    data: token,
    method: 'post',
  })
}


//测试用
export function loginByUsername(username, password) {
  console.log(username, password)
  const data = {
    username,
    password
  }
  return request({
    url: '/login/login',
    method: 'post',
    data
  })
}
// export function logout() {
//   return request({
//     url: '/login/logout',
//     method: 'post'
//   })
// }

export function getUserInfo(token) {
  return request({
    url: '/user/info',
    method: 'get',
    params: { token }
  })
}

// 修改密码
export function editPwd (params) {
   return post('/api/user/editPwd', qs.stringify(params), isForm)
}

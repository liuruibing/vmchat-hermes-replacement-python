import axios from 'axios'
import {Message, MessageBox} from 'element-ui'
import store from '@/store'
import {getToken, setToken} from '@/utils/auth'
import qs from 'qs'

var loginOvertime = 0 // 登录超时时调用接口次数记录 防止弹框弹出多次
// create an axios instance
const service = axios.create({
  baseURL: process.env.BASE_API, // api 的 base_url
  timeout: 600000 // request timeout
})
// 请求默认带  cookie
axios.defaults.withCredentials = true

function getRndInteger(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

export const urlRE = /(https?):\/\/[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]/

function request(options) {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest()
    xhr.timeout = 6000

    let url = getURL(options.url)
    if (options.method === 'GET') {
      url += `${getURLParam(options.data)}`
    }

    xhr.open(options.method, url)

    xhr.ontimeout = reject
    xhr.onerror = reject
    xhr.onload = (e) => {
      resolve(e.target.response)
    }

    xhr.send(JSON.stringify(getURLData(options.data, options.paramType)))
  })
}

function getURLParam(data) {
  let result = ''
  data.forEach(item => {
    if (item[0]) {
      result += `&${item[0]}=${item[1]}`
    }
  })

  return result ? '?' + result : ''
}

function getURLData(data, paramType) {
  if (!data) return ''

  if (paramType === 'array') {
    return data
  }

  const result = {}
  data.forEach(item => {
    if (item[0]) {
      result[item[0]] = item[1]
    }
  })

  return result
}

export function getURL(url) {
  return url.startsWith('http') ? url : 'https://' + url
}

export function getSeq() {
  let count_seq = getRndInteger(0, Number.MAX_SAFE_INTEGER)
  let time = new Date()
  let temp = getToken() + '|||' + time.getTime() + '|||' + count_seq
  temp = Base64.encode(temp)
  temp = Base64.encode(temp)
  temp = Base64.encode(temp)
  return temp
}

// request拦截器
// 在 interceptors 中对header进行处理
service.interceptors.request.use(
  // 请求对象
  config => {
    // console.log('setting')
    // console.log(store.state.setting.baseApi)
    const regArray = [/^http:.*/, /^:.*/, /^\/.*/]
    if (regArray[0].test(process.env.BASE_API)) {
      config.baseURL = process.env.BASE_API
    } else if (regArray[1].test(process.env.BASE_API)) {
      config.baseURL = window.location.protocol + '//' + window.location.hostname + process.env.BASE_API
      store.state.setting.baseApi = config.baseURL
    } else if (regArray[2].test(process.env.BASE_API)) {
      config.baseURL = window.location.protocol + '//' + window.location.host + process.env.BASE_API
      store.state.setting.baseApi = config.baseURL
    }
    if (store.getters.token) {
      // 让每个请求携带token-- ['X-Token']为自定义key 请根据实际情况自行修改   getToken()
      // config.headers['token'] = "vXcx3IBemn2UF5F+KqWjTf7lbqt37IMY";
      config.headers['Authorization'] = getToken()
    }
    return config
  },
  error => {
    // Do something with request error
    console.log(error) // for debug
    // 错误处理
    Promise.reject(error)
  }
)

// response interceptor
// 异常捕获处理
service.interceptors.response.use(
  // response => response,
  /**
   * 下面的注释为通过在response里，自定义code来标示请求状态
   * 当code返回如下情况则说明权限有问题，登出并返回到登录页
   * 如想通过 xmlhttprequest 来状态码标识 逻辑可写在下面error中
   * 以下代码均为样例，请结合自生需求加以修改，若不需要，则可删除
   */
  response => {
    const res = response.data
    // console.log('response',res);
    if (res.status === 401) {
      if (store.state.setting.fromPlatForm) {
        store.dispatch('LogOut').then(() => {
          location.replace(store.state.setting.saveUnifiedLoginURL)
        }).catch(() => {
          location.replace(store.state.setting.saveUnifiedLoginURL)
        })
        return Promise.reject('')
      }
      loginOvertime++
      // 弹框只执行第一次
      if (loginOvertime === 1) {
        MessageBox('登录失效，请重新登录！', '提示', {
          confirmButtonText: '确定',
          type: 'warning'
        }).then(() => {

          // 调用退出登录
          store.dispatch('LogOut').then(() => {
            // 登录超时时调用接口次数 值还原
            loginOvertime = 0
            location.reload()
          }).catch(() => {
            // 登录超时时调用接口次数 值还原
            loginOvertime = 0
            // 即使失败也跳转  Ps: 后台退出登录接口报 401导致要这样写
            location.reload()
          })
          // 不点击确定按钮也退出登录
        }).catch(() => {
          // 调用退出登录
          store.dispatch('LogOut').then(() => {
            // 登录超时时调用接口次数 值还原
            loginOvertime = 0
            // 即使失败也跳转
            location.reload()
          }).catch(() => {
            // 登录超时时调用接口次数 值还原
            loginOvertime = 0
            // 即使失败也跳转
            location.reload()
          })
        })
      }
      return Promise.reject('')
    } else if (res.status === 403) {
      Message.closeAll()
      Message({
        message: '权限不足',
        type: 'error',
        duration: 2 * 1000
      })
      return Promise.reject(error)
    } else if (res.status === 404) {
      Message.closeAll()
      Message({
        message: '资源不存在',
        type: 'error',
        duration: 2 * 1000
      })
      return Promise.reject(error)
    } else if (res.status === 405) {
      Message.closeAll()
      Message({
        message: '请求方式不支持',
        type: 'error',
        duration: 2 * 1000
      })
      return Promise.reject(error)
    } else if (res.status === 406) {
      Message.closeAll()
      Message({
        message: '数据格式错误',
        type: 'error',
        duration: 2 * 1000
      })
      return Promise.reject(error)
    } else {
      // 如果存在token
      const token = response.headers.authorization
      if (token) {
        setToken(token)
      }
      return response
    }
  },
  error => {
    if (store.state.setting.fromPlatForm) {
      store.dispatch('LogOut').then(() => {
        location.replace(store.state.setting.saveUnifiedLoginURL)
      }).catch(() => {
        location.replace(store.state.setting.saveUnifiedLoginURL)
      })
      return Promise.reject(error)
    }

    // console.log('err-message---' + error.message) // for debug
    // console.info(error.response) // for debug
    // error.message
    // 先关闭之前实例
    if (error.message == 'Network Error') {
      Message.closeAll()
      Message({
        message: '服务器连接异常！',
        type: 'error',
        duration: 2 * 1000
      })
    } else {
      Message.closeAll()
      Message({
        message: error.message || '请求异常',
        type: 'error',
        duration: 2 * 1000
      })
    }
    return Promise.reject(error)
  }
)

/* 导出文件上传url */
export const FILE_URL = process.env.BASE_API

/**
 * post方法，对应post请求
 * @param {String} url [请求的url地址]
 * @param {Object} params [请求时携带的参数]
 * @param {Object} header [请求头部]
 * @returns Promise
 */
export function post(url, params = {}, header) {
  return new Promise((resolve, reject) => {
    service({
      url,
      method: 'post',
      data: params,
      headers: header || {
        'Content-Type': 'application/json;charset=UTF-8'
      }
    }).then(response => {
      resolve(response.data)
    }).catch(error => {
      reject(error)
    })
  })
}

/**
 * get方法，对应get请求
 * @param {String} url [请求的url地址]
 * @param {Object} params [请求时携带的参数]
 * @returns Promise
 */
export function get(url, params = {}, header) {
  return new Promise((resolve, reject) => {
    service({
      url,
      method: 'get',
      params: params,
      headers: header || {
        'Content-Type': 'application/json;charset=UTF-8'
      }
    }).then(response => {
      resolve(response.data)
    }).catch(error => {
      reject(error)
    })
  })
}

/**
 * 导出excel post方法，对应post请求
 * @param {String} url [请求的url地址]
 * @param {Object} params [请求时携带的参数]
 * @returns Promise
 */
export function excelPost(url, params = {}, header) {
  return new Promise((resolve, reject) => {
    service({
      url,
      method: 'post',
      data: qs.stringify(params),
      responseType: 'blob',
      headers: header || {
        'Content-Type': 'application/json;charset=UTF-8'
      }
    }).then(response => {
      resolve(response)
    }).catch(error => {
      reject(error)
    })
  })
}

export function excelPostNoQS(url, params = {}, header) {
  return new Promise((resolve, reject) => {
    service({
      url,
      method: 'post',
      data: params,
      responseType: 'blob',
      headers: header || {
        'Content-Type': 'application/json;charset=UTF-8'
      }
    }).then(response => {
      resolve(response)
    }).catch(error => {
      reject(error)
    })
  })
}

/**
 * 导出excel get方法，对应get请求
 * @param {String} url [请求的url地址]
 * @param {Object} params [请求时携带的参数]
 * @returns Promise
 */
export function excelGet(url, params = {}, header) {
  return new Promise((resolve, reject) => {
    service({
      url,
      method: 'get',
      params: params,
      responseType: 'blob',
      headers: header || {
        'Content-Type': 'application/json;charset=UTF-8'
        // 'Content-Type': 'application/octet-stream;'
      }
    }).then(response => {
      resolve(response)
    }).catch(error => {
      reject(error)
    })
  })
}

export default service

// 错误处理
// Message({
//   message: res.message,
//   type: 'error',
//   duration: 5 * 1000
// })
// 50008:非法的token; 50012:其他客户端登录了;  50014:Token 过期了;
// if (res.code === 50008 || res.code === 50012 || res.code === 50014) {
//   // 请自行在引入 MessageBox
//   // import { Message, MessageBox } from 'element-ui'
//   MessageBox.confirm('你已被登出，可以取消继续留在该页面，或者重新登录', '确定登出', {
//     confirmButtonText: '重新登录',
//     cancelButtonText: '取消',
//     type: 'warning'
//   }).then(() => {
//     store.dispatch('FedLogOut').then(() => {
//       location.reload() // 为了重新实例化vue-router对象 避免bug
//     })
//   })
// }
// return Promise.reject('error')

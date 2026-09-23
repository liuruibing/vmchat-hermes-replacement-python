'use strict'
import Vue from 'vue'
import axios from 'axios'
import qs from 'qs'
import api from '@/apiAxios/configApi.js'
import $ from 'jquery'
import 'vue-beauty/package/style/vue-beauty.min.css'//import css
import fun from '@/assets/js/common.js'
import vueBeauty from 'vue-beauty'//import components
Vue.use(vueBeauty)
import {alert} from 'vue-beauty'//OR
Vue.use(alert)





// IE浏览器不支持promise
import 'es6-promise/auto'

var self=this;
axios.interceptors.request.use(config => {
//   if (config.method == 'post') {
//   config.data = true
// }
// config.headers['H-TOKEN'] = '111'
  return config
}, error => {
  return Promise.reject(error)
})

axios.interceptors.response.use(response => {
  return response
}, error => {
  return Promise.resolve(error.response)
})

function checkStatus (response) {
  // loading
  // 如果http状态码正常，则直接返回数据
  if (response && (response.status === 200 || response.status === 304 || response.status === 400|| response.status === 0 )) {

    return response
    // 如果不需要除了data之外的数据，可以直接 return response.data
  }
  // 异常状态下，把错误信息返回去
  return {
    status: -404,
    msg: '网络异常'
  }
}



function checkCode (res,state) {
  // 如果code异常(这里已经包括网络错误，服务器错误，后端抛出的错误)，可以弹出一个错误提示，告诉用户

  if (res.status === -404) {
    if(state) {
      // res.msg
      //调用本页面的提示
      //fun.abnormal('数据错误')
      //调用父级页面的错误提示
      fun.parent_abnormal('数据错误')
      fun.loadingfadeOut()
    }

  }
  if (res.data && (!res.data)) {
    if(state) {

      fun.loadingfadeOut()
    }

  }

    if(state) {
      fun.loadingfadeOut()
      // if (res.data.data.length == 0) {
      //   fun.nodata();
      // }
      // else{
      //
      // }

    }
    return res
}

export default {

  post (url, params,state ) {
    if(state) {
      fun.loadingfadeIn()
    }
    return axios({
      method: 'post',
      baseURL: api.baseURLHeader+'://'+api.baseURLIp+'/'+api.baseURLCommon,
      url,
      data:params,
      timeout: 100000,
      dataType:'json',
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json;charset=UTF-8'
      }
    }).then(
      (response) => {
        return checkStatus(response)
      }
    ).then(
      (res) => {
        return checkCode(res,state )

  }
    )
  },
  get (url, params,state) {
    if(state) {
      fun.loadingfadeIn()
    }
    return axios({
      method: 'get',

      baseURL: api.baseURLHeader+'://'+api.baseURLIp+'/'+api.baseURLCommon,
      url,
      params, // get 请求时带的参数
      timeout: 100000,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'X-Requested-With': 'XMLHttpRequest',
      }
    }).then(
      (response) => {
        return checkStatus(response)
      }
    ).then(
      (res) => {
        return checkCode(res,state)
      }
    )
  }
}






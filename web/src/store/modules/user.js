import {editPwd, getUserInfo, loginLockUrl, loginUserInfo, logout, loginByCodeUrl} from '@/api/login'
import {getToken, removeCookiesData, removeToken, setCookiesData, setToken} from '@/utils/auth'
// import { Message } from 'element-ui'
import {Base64} from 'js-base64'
import cryptoJs from 'crypto-js'

let BAIDUID = JSON.parse(localStorage.getItem('BAIDUID')) || {}
let defaultImgUrl = require("../../assets/img/dashboardimg.png");
const user = {
  state: {
    // 用户信息
    user: BAIDUID || '',
    // 系统菜单颜色
    meauColor: BAIDUID.meauColor || '#3C3857',
    // 系统首页背景颜色
    homeBackgroundColor: BAIDUID.homeBackgroundColor || '',
    // 首页背景图片
    backgroundImageUrl: BAIDUID.backgroundImageUrl || defaultImgUrl,
    status: '',
    code: '',
    // 登陆token
    token: getToken() || '',
    meau: '',
    // 用户名
    name: BAIDUID.userName || '',
    avatar: '',
    introduction: '',
    // 用户角色
    roles: [],
    setting: {
      articlePlatform: []
    },
    // 记录用户点击的根菜单  和子菜单传值用
    meauTop: '',
    fromPageJump: false, // 用来判断是否是从页面跳转过来的
    fromCreateSumuComb: false, // 用来跳转到 创建模拟组合页面
    fromPageJumpSYCP: false, // 用来控制私有产品页面
    dropFlag: false,
  },
  // 改变状态，不允许异步
  mutations: {
    SET_DROPFLAG: (state, status) => {
      state.dropFlag = status
    },
    SET_MEAUCOLOR: (state, meauColor) => {
      state.meauColor = meauColor
    },
    SET_FROMPAGEJUMPSYCP: (state, status) => {
      state.fromPageJumpSYCP = status
    },
    // 修改跳转标志位状态
    SET_FROMPAGEJUMP: (state, status) => {
      state.fromPageJump = status
    },
    SET_FROMCREATESUMUCOMB: (state, status) => {
      state.fromCreateSumuComb = status
    },
    SET_HOMEBACKGROUNDCOLOR: (state, homeBackgroundColor) => {
      state.homeBackgroundColor = homeBackgroundColor
    },
    SET_BACKGROUNDIMAGEURL: (state, backgroundImageUrl) => {
      state.backgroundImageUrl = backgroundImageUrl
    },
    SET_CODE: (state, code) => {
      state.code = code
    },
    SET_TOKEN: (state, token) => {
      state.token = token
    },
    SET_MEAU: (state, meau) => {
      state.meau = meau
    },
    SET_INTRODUCTION: (state, introduction) => {
      state.introduction = introduction
    },
    SET_SETTING: (state, setting) => {
      state.setting = setting
    },
    SET_STATUS: (state, status) => {
      state.status = status
    },
    SET_NAME: (state, name) => {
      state.name = name
    },
    SET_AVATAR: (state, avatar) => {
      state.avatar = avatar
    },
    SET_ROLES: (state, roles) => {
      state.roles = roles
    },
    SET_MEAUTOP: (state, meauTop) => {
      state.meauTop = meauTop
    }
  },
  // 改变状态,允许异步
  actions: {
    // 用户名登录
    LoginByUsername({commit}, userInfo) {
      return new Promise((resolve, reject) => {
        // 账号
        let username = userInfo.username.trim()
        // 密码加密处理
        let password = userInfo.password
        // Base64三重加密传输
        password = Base64.encode(password)
        password = Base64.encode(password)
        password = Base64.encode(password)
        // 密码SHA512加密处理
        password = cryptoJs.SHA512(password).toString()
        let params = {
          // 用户名
          loginAccount: username,
          // 密码
          loginPw: password
        }
        loginLockUrl(params).then(res => {
          let {status, error, data, message} = res
          if (status === 200) {
            if (error) {
              reject(error)
            } else {
              // 设置token
              commit('SET_TOKEN', getToken())
              // 设置用户名
              commit('SET_NAME', data.userName)
              // 存储个人信息
              // localStorage.setItem('BAIDUID', JSON.stringify(data))
              setCookiesData('BAIDUID', JSON.stringify(data))
              resolve()
            }
          } else {
            reject(message || '登录失败')
          }
        }).catch(error => {
          reject(error)
        })
      })
    },
    // 用户名登录
    LoginByUsernameByCode({ commit }, userInfo) {
      return new Promise((resolve, reject) => {
        // 账号
        let username = userInfo.username;
        // 密码加密处理
        let password = userInfo.password;
        // Base64三重加密传输
        password = Base64.encode(password)
        password = Base64.encode(password)
        password = Base64.encode(password)
        // 密码SHA512加密处理
        password = cryptoJs.SHA512(password).toString()
        // 验证码
        let code = userInfo.code;
        // 验证码ID
        let codeId = userInfo.codeId;
        let params = {
          // 用户名
          loginAccount: username,
          // 密码
          loginPw: password,
          // 验证码
          code: code,
          // 验证码 ID
          codeId: codeId
        }
        loginByCodeUrl(params).then(res => {
          let { status, error, data } = res
          if (status === 200) {
            if (error) {
              reject(error)
            } else {
              // 设置token
              commit('SET_TOKEN', getToken())
              // 设置用户名
              commit('SET_NAME', data.userName)
              // 存储个人信息
              // localStorage.setItem('BAIDUIDRISK', JSON.stringify(data))
              setCookiesData('BAIDUID', JSON.stringify(data))
              resolve()
            }
          } else {
            reject(error || '用户名或登录密码不正确！')
            // Message({
            //   message: "请输入正确的用户名和密码",
            //   type: 'error',
            //   duration: 5 * 1000
            // })
          }
        }).catch(error => {
          reject(error)
        })
      })
    },
    // 后端链接登录
    LoginByBackUsername({commit}, token) {
      //设置 浏览器 token
      setToken(token)
      // 设置token
      commit('SET_TOKEN', token)
      return new Promise((resolve, reject) => {
        loginUserInfo().then(res => {
          let {status, error, data} = res
          if (status === 0) {
            if (error) {
              reject(error)
            } else {
              // 设置用户名
              commit('SET_NAME', data.userName)
              // 存储个人信息
              // localStorage.setItem('BAIDUID', JSON.stringify(data))
              setCookiesData('BAIDUID', JSON.stringify(data))
              resolve()
            }
          } else {
            reject(error || '登录失败')
          }
        }).catch(error => {
          reject(error)
        })
      })
    },

    //后端链接登录，跳转目标路径
    LoginByBackUsernameOnly({commit}, token) {

      return new Promise((resolve, reject) => {
        loginUserInfo().then(res => {
          let {status, error, data} = res
          if (status === 0) {
            if (error) {
              reject(error)
            } else {
              // 设置用户名
              commit('SET_NAME', data.userName)
              // 存储个人信息
              // ps: 如果后端在这里返回用户的首页信息，就不用请求下边的接口
              setCookiesData('BAIDUID', JSON.stringify(data))
              commit('SET_USER', data)
              resolve()
            }
          } else {
            reject(error || '登录失败')
          }
        }).catch(error => {
          reject(error)
        })
      })
    },
    // 获取用户信息
    GetUserInfo({commit, state}) {
      return new Promise((resolve, reject) => {
        getUserInfo('admin').then(response => {
          // getUserInfo('state.token').then(response => {
          // getUserInfo(state.token).then(response => {
          console.log(response)
          // 由于mockjs 不支持自定义状态码只能这样hack
          if (!response.data) {
            reject('Verification failed, please login again.')
          }
          const data = response.data

          if (data.roles && data.roles.length > 0) { // 验证返回的roles是否是一个非空数组
            commit('SET_ROLES', data.roles)
          } else {
            reject('getInfo: roles must be a non-null array!')
          }

          commit('SET_NAME', data.name)
          commit('SET_AVATAR', data.avatar)
          commit('SET_INTRODUCTION', data.introduction)
          resolve(response)
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 第三方验证登录
    // LoginByThirdparty({ commit, state }, code) {
    //   return new Promise((resolve, reject) => {
    //     commit('SET_CODE', code)
    //     loginByThirdparty(state.status, state.email, state.code).then(response => {
    //       commit('SET_TOKEN', response.data.token)
    //       setToken(response.data.token)
    //       resolve()
    //     }).catch(error => {
    //       reject(error)
    //     })
    //   })
    // },

    // 登出
    LogOut({commit, state}) {
      return new Promise((resolve, reject) => {
        logout().then(() => {
          //清空 token 和 名字 角色
          commit('SET_TOKEN', '')
          commit('SET_NAME', '')
          commit('SET_ROLES', [])
          //清空浏览器 token
          removeToken()
          // localStorage
          // localStorage.removeItem("BAIDUID");
          removeCookiesData("BAIDUID");
          removeCookiesData("SSOTOKENID");
          resolve()
        }).catch(error => {
          //清空 token 和 名字 角色
          commit('SET_TOKEN', '')
          commit('SET_NAME', '')
          commit('SET_ROLES', [])
          //清空浏览器 token
          removeToken()
          // localStorage
          // localStorage.removeItem("BAIDUID");
          removeCookiesData("BAIDUID");
          removeCookiesData("SSOTOKENID");
          reject(error)
        })
      })
    },

    // 前端 登出
    FedLogOut({commit}) {
      return new Promise(resolve => {
        commit('SET_TOKEN', '')
        removeToken()
        resolve()
      })
    },

    // 动态修改权限
    ChangeRoles({commit, dispatch}, role) {
      return new Promise(resolve => {
        commit('SET_TOKEN', role)
        setToken(role)
        getUserInfo(role).then(response => {
          const data = response.data
          commit('SET_ROLES', data.roles)
          commit('SET_NAME', data.name)
          commit('SET_AVATAR', data.avatar)
          commit('SET_INTRODUCTION', data.introduction)
          dispatch('GenerateRoutes', data) // 动态修改权限后 重绘侧边菜单
          resolve()
        })
      })
    },


    changePwd({commit, state}, params) {
      return new Promise((resolve, reject) => {
        // 原密码和新密码加密处理
        for (let key in params) {
          if (key === "password" || key === "newPassword" || key === 'newPasswordPlain') {
            // Base64三重加密传输
            params[key] = Base64.encode(params[key])
            params[key] = Base64.encode(params[key])
            params[key] = Base64.encode(params[key])

            // 密码SHA512加密处理
            if(key !== 'newPasswordPlain') {
              params[key] = cryptoJs.SHA512(params[key]).toString();
            }
          }
        }
        editPwd(params).then((res) => {
          if (res.error) {
            reject(res.error)
          } else {
            resolve()
          }
        }).catch(error => {
          reject(error)
        })
      })
    },


  }
}

export default user

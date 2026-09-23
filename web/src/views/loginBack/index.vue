<template>
  <div>
  </div>
</template>

<script>
import {ssologinUserInfo,ssologinUserInfoGlr} from '@/api/login'
import {getToken, removeToken, setCookiesData, setToken} from '@/utils/auth'

export default {
  name: 'LoginBack',
  data() {
    return {
      passwordType: 'password',
      loading: false,
      showDialog: false,
      redirect: undefined
    }
  },
  watch: {
    // 深度监听，可监听到对象、数组的变化
    $route: {
      handler(route) {
        this.redirect = route.query && route.query.redirect
        // console.log(this.redirect,route);
      },
      immediate: true
    }
  },
  mounted() {
    var self = this
    self.handleLogin()
  },
  methods: {
    getUrlParam(name) {
      var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)') // 构造一个含有目标参数的正则表达式对象
      var r = window.location.search.substr(1).match(reg) // 匹配目标参数
      if (r != null) {
        return decodeURIComponent(r[2])
      }
      return null // 返回参数值
    },

    // 登陆
    handleLogin() {
      // 判断url
      let jumpQueryByUrl = this.getUrlParam('query')
      const unifiedLogin = this.getUrlParam('unifiedLogin')
      const ssoTokenId = this.getUrlParam('ssoTokenId')
      this.$store.commit('SET_FROMPLATFORM', false)
      const jumpPath = this.$route.query.path
      // 登陆处理  拿到token
      if (this.$route.query.token && unifiedLogin == 'true') {
        const params = {}
        params.token = this.$route.query.token
        setToken(this.$route.query.token)
        ssologinUserInfoGlr(params).then(res => {
          const {status, error, data} = res.data
          if (status != 0) {
            this.$message({
              message: '登录失败！',
              type: 'error'
            })
            removeToken()
          } else {
            // 判断是否有path
            if (jumpPath) {
              setCookiesData("SSOTOKENID", ssoTokenId)
              window.history.replaceState({}, document.title, window.location.origin + window.location.pathname)
              // 设置用户名
              this.$store.commit('SET_NAME', data.userName)
              // 存储个人信息
              // ps: 如果后端在这里返回用户的首页信息，就不用请求下边的接口
              setCookiesData('BAIDUID', JSON.stringify(data))
              this.$store.commit('SET_USER', data)
              this.$store.commit('SET_FROMPLATFORM', true)
              this.$store.commit('SET_TOKEN', getToken())

              if (jumpQueryByUrl) {
                const queryStr = JSON.parse(jumpQueryByUrl)
                // 将标志位全部置 true
                this.$store.commit('SET_FROMPAGEJUMPSYCP', true)
                this.$store.commit('SET_FROMPAGEJUMP', true)
                this.$store.commit('SET_FROMCREATESUMUCOMB', true)
                this.$router.push({path: jumpPath, replace: true, query: queryStr})
              } else {
                this.$router.push({path: jumpPath, replace: true})
              }
            } else {
              setCookiesData("SSOTOKENID", ssoTokenId)
              window.history.replaceState({}, document.title, window.location.origin + window.location.pathname)
              // 设置用户名
              this.$store.commit('SET_NAME', data.userName)
              // 存储个人信息
              // ps: 如果后端在这里返回用户的首页信息，就不用请求下边的接口
              setCookiesData('BAIDUID', JSON.stringify(data))
              this.$store.commit('SET_USER', data)
              this.$store.commit('SET_FROMPLATFORM', true)
              this.$router.push({path: '/dashboard'})
            }
          }
        })
      } else {
        this.$message({
          message: '登录失败！',
          type: 'error'
        })
      }
    }
  }
}
</script>

<style lang="scss" rel="stylesheet/scss">

</style>


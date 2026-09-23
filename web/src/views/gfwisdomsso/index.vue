<template>
  <div></div>
</template>

<script>
import { ssologinUserInfo, ssologinUserInfoGFWisdom } from '@/api/login'
import { getToken, removeToken, setCookiesData, setToken } from '@/utils/auth'

export default {
  name: 'LoginGFWisdomSSO',
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
    self.handleLogin(this.$route.query.code)
  },
  methods: {
    // 登陆
    handleLogin(code) {
      ssologinUserInfoGFWisdom(code)
        .then(async (res) => {
          const { status, error, data } = res.data
          if (status !== 0) {
            this.$message({
              message: error || '登录失败！',
              type: 'error'
            })
            removeToken()
            // 重定向到登录页
            this.$router.push('/login')
            return
          }

          try {
            // 等待并检查 token
            const token = await this.waitForToken()

            // 更新状态
            this.$store.commit('SET_TOKEN', token)

            // 清理 URL 参数
            window.history.replaceState({}, document.title, window.location.origin + window.location.pathname)

            // 设置用户信息
            this.$store.commit('SET_NAME', data.userName)
            setCookiesData('BAIDUID', JSON.stringify(data))
            this.$store.commit('SET_USER', data)

            // 跳转到首页
            this.$router.push({ path: '/dashboard' })
            return
          } catch (error) {
            console.error('登录过程出错:', error)
            this.$message({
              message: '登录过程中发生错误，请重试',
              type: 'error'
            })
            removeToken()
            // 重定向到登录页
            this.$router.push('/login')
            return
          }
        })
        .catch((error) => {
          console.error('登录请求失败:', error)
          this.$message({
            message: '登录请求失败，请重试',
            type: 'error'
          })
          removeToken()
          // 重定向到登录页
          this.$router.push('/login')
          return
        })
    },

    // 等待并检查 token 是否设置成功
    waitForToken(maxAttempts = 20, interval = 100) {
      return new Promise((resolve, reject) => {
        let attempts = 0

        const checkToken = () => {
          const token = getToken()
          if (token) {
            resolve(token)
          } else if (attempts >= maxAttempts) {
            reject(new Error('Token 设置超时'))
          } else {
            attempts++
            setTimeout(checkToken, interval)
          }
        }

        checkToken()
      })
    }
  }
}
</script>

<style lang="scss" rel="stylesheet/scss"></style>

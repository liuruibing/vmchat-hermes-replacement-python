<template>
  <div class="login-container">
    <el-form
      ref="loginForm"
      :model="loginForm"
      :rules="loginRules"
      class="login-form"
      auto-complete="on"
      label-position="left"
    >
      <div class="title-container">
        <h3 class="title">
          <!--{{ $t('login.title') }}-->
          <img src="../../assets/img/systemTestLogo.png" height="44" width="228" />
        </h3>
        <!--语言设置-->
        <!--<lang-select class="set-language" />-->
      </div>

      <el-form-item prop="username">
        <span class="svg-container">
          <svg-icon icon-class="user" />
        </span>
        <el-input
          v-model="loginForm.username"
          placeholder="账号"
          name="username"
          type="text"
          auto-complete="off"
        />
      </el-form-item>

      <el-form-item prop="password" style="margin-top: 25px;">
        <span class="svg-container">
          <svg-icon icon-class="password" />
        </span>
        <el-input
          v-model="loginForm.password"
          :type="passwordType"
          placeholder="密码"
          name="password"
          auto-complete="off"
        />
        <span class="show-pwd" @click="showPwd">
          <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
        </span>
      </el-form-item>

      <el-button :loading="loading" type="primary" class="loginBtn" @click.native.prevent="handleLogin">
        登录
      </el-button>
    </el-form>

    <el-dialog :title="$t('login.thirdparty')" :visible.sync="showDialog">
      {{ $t('login.thirdpartyTips') }}
      <br />
      <br />
      <br />
      <social-sign />
    </el-dialog>
  </div>
</template>

<script>
// 前端演示验证
import { isvalidUsername } from '@/utils/validate'
import { getToken } from '@/utils/auth'
export default {
  name: 'Login',
  data() {
    const validateUsername = (rule, value, callback) => {
      if (!value) {
        callback(new Error('账号不能为空'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (!value) {
        callback(new Error('密码不能为空'))
      } else {
        callback()
      }
    }
    return {
      loginForm: {
        // 账号
        username: '',
        // 密码
        password: ''
      },
      // 验证规则
      loginRules: {
        // 账号
        username: [{ required: true, trigger: 'blur', validator: validateUsername }],
        // 密码
        password: [{ required: true, trigger: 'blur', validator: validatePassword }]
      },
      passwordType: 'password',
      loading: false,
      showDialog: false,
      redirect: undefined
    }
  },
  watch: {
    //深度监听，可监听到对象、数组的变化
    $route: {
      handler(route) {
        this.redirect = route.query && route.query.redirect
        // console.log(this.redirect,route);
      },
      immediate: true
    }
  },
  created() {
    document.onkeydown = ev => {
      let event = ev || event
      if (event.keyCode == 13) {
        if (this.$route.path === '/login') {
          // 去登陆
          this.handleLogin()
        }
      }
    }
  },
  //在离开页面后执行
  destroyed() {},
  methods: {
    // 显示/隐藏密码
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
    },
    // 登录
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          // 登录按钮上边的延迟显示 true
          this.loading = true
          // 登录处理
          this.$store
            .dispatch('LoginByUsernameByCode', this.loginForm)
            .then(() => {
              this.$store
                .dispatch('LoginByBackUsername', getToken())
                .then(() => {
                  // this.$message({
                  //   message: '登录成功！',
                  //   type: 'success',
                  // })
                  this.loading = false
                  // 默认跳转到首页
                  // if (this.redirect == "/") this.redirect = "/dashboard"
                  // 跳转路由
                  // this.$router.push({ path: this.redirect || '/dashboard' })
                  //登录默认跳转首页，不再重定向
                  this.$router.push({ path: '/dashboard' })
                })
                .catch(error => {
                  this.$message.closeAll()
                  // this.$message.error('用户名/密码不正确，登录失败')
                  this.$message.error(error || '登录失败')
                  this.loading = false
                })
            })
            .catch(error => {
              this.$message.closeAll()
              // this.$message.error('用户名/密码不正确，登录失败')
              this.$message.error(error || '登录失败')
              this.loading = false
            })
        }
      })
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg: #2d3a4b;
$light_gray: #eee;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
    &::first-line {
      color: $light_gray;
    }
  }
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;
    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;
      &:-webkit-autofill {
        -webkit-text-fill-color: #fff !important;
        transition: background-color 5000s ease-in-out 0s;
      }
    }
  }
  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style rel="stylesheet/scss" lang="scss" scoped>
$bg: #2d3a4b;
$dark_gray: #889aa4;
$light_gray: #eee;

.login-container {
  min-height: 100%;
  width: 100%;
  // background-color: $bg;
  overflow: hidden;
  background-image: url('../../assets/img/dashboardimg.png');
  // 全覆盖
  background-size: cover;
  // 定位到图片中间
  background-position: 50% 50%;
  .login-form {
    position: relative;
    width: 520px;
    max-width: 100%;
    padding: 160px 35px 0;
    margin: 0 auto;
    overflow: hidden;
  }
  .tips {
    font-size: 14px;
    color: #fff;
    margin-bottom: 10px;
    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }
  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }
  .title-container {
    position: relative;
    .title {
      font-size: 26px;
      color: $light_gray;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
    .set-language {
      color: #fff;
      position: absolute;
      top: 5px;
      right: 0px;
    }
  }
  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }
  .thirdparty-button {
    position: absolute;
    right: 0;
    bottom: 6px;
  }
  .loginBtn {
    width: 100%;
    margin-top: 20px;
    margin-bottom: 30px;
  }
}
</style>

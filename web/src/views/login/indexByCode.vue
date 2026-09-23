<!-- 需要验证码 -->
<template>
  <div id="login-container" class="login-container" v-loading="$store.state.setting.loginPennding">
    <div class="login-center">
      <div style="height: 100%; width: 100%;position: relative">
        <div style="position: absolute;width: 333px;height :507px;right:26px;top:19px;padding: 35px;padding-top: 70px;">
          <el-form
            ref="loginForm"
            :model="loginForm"
            :rules="loginRules"
            class="login-form"
            auto-complete="on"
            label-position="left"
          >
            <div class="title-container">
              <h3 class="title"><span style="display: inline-block;height: 30px;line-height: 18px;border-bottom: 3px solid;">登录</span></h3>
            </div>

            <el-form-item prop="username">
              <span class="svg-container">
                <svg-icon icon-class="user"/>
              </span>
              <el-input
                v-model.trim="loginForm.username"
                placeholder="账号"
                name="username"
                type="text"
                auto-complete="off"
              />
            </el-form-item>

            <el-form-item prop="password" style="margin-top: 25px;">
              <span class="svg-container">
                <svg-icon icon-class="password"/>
              </span>
              <el-input
                v-model.trim="loginForm.password"
                :type="passwordType"
                placeholder="密码"
                name="password"
                auto-complete="off"
              />
              <span class="show-pwd" @click="showPwd">
                <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'"/>
              </span>
            </el-form-item>

            <!-- 登录验证码 -->
            <div style="margin-top: 25px;position: relative" class="code-box">
              <el-form-item prop="code" style="width:180px;">
              <span class="svg-container">
                <i class="el-icon-postcard"></i>
              </span>
                <el-input v-model.trim="loginForm.code" placeholder="验证码" name="code" style="width: 120px;"/>
              </el-form-item>
              <div v-loading="imgSrcLoading" class="code-img" @click="getCodeImg">
                <img :src="imgSrc"/>
              </div>
            </div>
<!--            <div>
              <el-checkbox v-model="checked">
              </el-checkbox>
              <span class="login-normal-fontcolor">我已阅读并同意</span>
              <span class="login-file-fontcolor">平台协议</span>
              <span class="login-normal-fontcolor">和</span>
              <span class="login-file-fontcolor">平台使用文档</span>
            </div>-->
            <el-button
              :loading="loading"
              :disabled="!checked || loading"
              type="loginPrimary"
              class="loginBtn"
              :class="!checked ? 'nocheck-style' : ''"
              @click.native.prevent="handleLogin"
            >登录
            </el-button>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// 前端演示验证
import { getToken } from '@/utils/auth'
import { codeImage } from '@/api/login'
export default {
  name: 'Login',
  components: {},
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
    const valCode = (rule, value, callback) => {
      if (!value) {
        callback(new Error('验证码不能为空'))
      } else {
        callback()
      }
    }
    return {
      loginPennding: true,
      checked: true,
      loginForm: {
        // 账号
        username: '',
        // 密码
        password: '',
        // 验证码
        code: '',
        // 验证码ID
        codeId: ''
      },
      imgSrc: '', // 验证码图片地址
      imgSrcLoading: false, // 验证码图片加载loading
      // 验证规则
      loginRules: {
        // 账号
        username: [
          { required: true, trigger: 'blur', validator: validateUsername }
        ],
        // 密码
        password: [
          { required: true, trigger: 'blur', validator: validatePassword }
        ],
        // 验证码
        code: [{ required: true, trigger: 'blur', validator: valCode }]
      },
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
  created() {
    document.onkeydown = (ev) => {
      const event = ev || event
      if (event.keyCode == 13) {
        if (this.$route.path === '/login') {
          // 去登陆
          this.handleLogin()
        }
      }
    }

    //  默认获取一张验证码图片
    this.getCodeImg()
  },
  // 在离开页面后执行
  destroyed() {
    this.loading = false
  },
  methods: {
    // 显示/隐藏密码
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
    },
    // 获取验证码图片
    getCodeImg() {
      // 验证码loading
      this.imgSrcLoading = true
      codeImage()
        .then((response) => {
          this.imgSrcLoading = false
          const responseData = response.data
          // 验证码地址
          this.imgSrc = 'data:image/png;base64,' + responseData.code
          // 验证码图片ID
          this.loginForm.codeId = responseData.uid
          // 清空验证码历史填写的值
          this.loginForm.code = ''
        })
        .catch(() => {
          this.imgSrcLoading = false
          this.imgSrc = ''
          this.loginForm.codeId = ''
          this.loginForm.code = ''
        })
    },
    // 登录
    handleLogin() {
      if(!this.checked) {
        this.$message.closeAll()
        this.$message.warning('请先阅读并同意平台协议和平台使用文档')
        return
      }
      this.$refs.loginForm.validate((valid) => {
        if (valid) {
          // 登录按钮上边的延迟显示 true
          this.loading = true
          // 登录处理
          this.$store
            .dispatch('LoginByUsernameByCode', this.loginForm)
            .then(() => {
              this.loading = false
              this.$router.push({ path: '/dashboard' })
            })
            .catch((error) => {
              this.$message.closeAll()
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

//$bg: #283443;
$bg: white;
$light_gray: #eee;
$cursor: #000;
@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    //color: $cursor;
    color: black;

    &::first-line {
      color: black;
    }
  }
}

// 验证码样式
.code-box {
  position: relative;

  .code-img {
    width: 80px;
    height: 37px;
    cursor: pointer;
    overflow: hidden;
    position: absolute;
    border-radius: 5px;
    right: 0px;
    top: 0px;

    img {
      width: 100%;
      height: 100%;
    }
  }
}

#login-container {
  .login-normal-fontcolor, .login-file-fontcolor {
    font-size: 12px;
  }
  .login-file-fontcolor {
    color: #a15008;
  }
  .login-normal-fontcolor {
    color: black;
  }
  .el-form-item__content {
    line-height: unset;
  }
  .el-input__inner {
    border: 0px !important;;
    color: #eeeeee !important;
  }
  .el-form-item__error {
    top: 110%;
  }
  .el-input__placeholder {
    color: #d0d6df;
  }
  .el-button.el-button--loginPrimary {
    background-image: linear-gradient(to right, #f5d7bc, #e0b794);
    border: none;
    color:#612d10;
  }
  .el-checkbox__input.is-focus .el-checkbox__inner,.el-checkbox__inner:hover {
    border-color: #e2a971;
  }
  .el-checkbox__input.is-checked .el-checkbox__inner, .el-checkbox__input.is-indeterminate .el-checkbox__inner {
    background-color: #e2a971;
    border-color: #e2a971;
  }


}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 35px;
    width: 85%;

    input {
      background: rgb(255, 255, 255);
      //opacity: 0.3;
      //background: white;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      //padding: 12px 5px 12px 15px;
      color: $light_gray !important;
      //color: black !important;
      height: 35px;
      caret-color: $cursor;

      &:-webkit-autofill {
        -webkit-box-shadow: 0 0 0px 1000px $bg inset !important;
        color: $light_gray !important;
        //color: black !important;
        -webkit-text-fill-color: black !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.3);
    background: rgb(255, 255, 255);
    border-radius: 5px;
    color: #454545;
  }
}
</style>

<style rel="stylesheet/scss" lang="scss" scoped>
//$bg: #2d3a4b;
$bg: white;
$dark_gray: #889aa4;
$light_gray: #eee;
.login-container {
  .el-form-item__content {
    height: 35px;
  }
  .nocheck-style {
    opacity: .4;
  }
  min-height: 100%;
  width: 100%;
  // background-color: $bg;
  overflow: hidden;
  background-image: url('../../assets/img/loginBg.jpg');
  // 全覆盖
  background-size: cover;
  // 定位到图片中间
  background-position: 50% 50%;

  .login-form {
    width: 100%;
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
      font-size: 20px;
      height: 30px;
      color: #a15008;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: normal;
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
    margin-top: 50px;
    margin-bottom: 30px;
  }
}

.login-center {
  width: 380px;
  height: 560px;
  overflow: hidden;
  //background-image: url('../../assets/img/loginBgcenter.png');
  background-color: rgba(255, 255, 255, 0.5);
  background-size: cover; /* 全覆盖背景图片 */
  position: absolute;
  top: 50%;
  left: 70%;
  transform: translate(-50%, -50%);
}
</style>

<template>
  <div class="lockwindowStyle" :style="showOrhidder">
    <div class="lock-bg" :style="{backgroundImage: $store.state.user.backgroundImageUrl ? 'url(' + $store.state.user.backgroundImageUrl + ')' : 'none'}" v-show="dialogVisible"></div>
    <el-dialog title="请输入密码解锁" :visible.sync="dialogVisible" top="25vh" :close-on-click-modal='false' :close-on-press-escape='false' :show-close='false' center @closed='closedDialog'>
      <div class="mainStyle">
        <el-form :model="dataForm" ref="dataForm" @submit.native.prevent :rules="rulesForm" label-position="right" label-width="80px">
          <el-form-item prop="passWord" label="密码">
            <el-input
              maxlength="20"
              v-model="dataForm.passWord"
              placeholder="请输入密码"
              :show-password='true'
              @keydown.enter.native="submit()"
            ></el-input>
          </el-form-item>
        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
        <!-- <el-button type="info" @click="returnLogin" size="small">退出登录</el-button> -->
        <el-button type="primary" @click="submit" size="small" :loading="loading">提 交</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
import storage from '@/utils/storage'
import { loginUrl } from '@/api/login'
import { Base64 } from 'js-base64'
import cryptoJs from 'crypto-js'
export default {
  props: {
    lock: {
      type: Boolean
    }
  },
  computed: {
    rulesForm (){
    return {
      passWord: [
         { required: true, message: "请输入密码", trigger: "change", },
        //  { message: "请输入数字、字母", pattern: /^[a-zA-Za-z0-9]+$/, trigger: "change" }
        ]
     }
    }
  },
  watch: {
    lock (data) {
      this.dialogVisible =  this.lock
    },
  },
  data() {
    return {
      loading: false,
      dialogVisible: false,
      showOrhidder: {},
      dataForm: {
        key: "",
        passWord: "",
      },
    }
  },
  methods: {
    init (data) {
      this.dialogVisible = this.lock || data
    },
    submit () {
      this.$message.closeAll()
      this.loading = true
      this.$refs.dataForm.validate((valid) => {
        if (valid) {
          this.submitApi()
        } else {
          this.loading = false
        }
      })
    },
    submitApi () {
      this.$message.closeAll()
      let key = this.$store.state.user.user.account
        // 密码加密处理
        let password = this.dataForm.passWord
        // Base64三重加密传输
        password = Base64.encode(password)
        password = Base64.encode(password)
        password = Base64.encode(password)
        // 密码SHA512加密处理
        password = cryptoJs.SHA512(password).toString()
        let params = {
          // 用户名
          loginAccount: this.$store.getters.roles[0],
          // 密码
          loginPw: password
        }
        loginUrl(params).then((data) => {
          if (data.status == 0) {
            this.loading = false
            this.$message.success('解锁成功 欢迎使用')
            this.$store.state.lock.isLock.isLock = false
            storage.setItem('isLock', { isLock: false } )
          } else {
            this.loading = false
            this.$message.error('密码不正确，解锁失败 ！')
          }
        }).catch((err) => {
          this.loading = false
          this.$message.error('服务异常 ！')
          console.log('is msg err', err)
        })
    },
    closedDialog () {
      this.dataForm.key = ''
      this.dataForm.passWord = ''
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    returnLogin () {
      this.dialogVisible = false
    }
  }
}
</script>
<style lang='scss'>
.lockwindowStyle {
  .lock-bg {
    position: fixed;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    z-index: 2000;
    min-height: 100%;
    background-image: url('../../assets/img/dashboardimg.png');
    background-size: 100% 100%;
    background-repeat: no-repeat;
  }
  .el-dialog{
   border-radius: 5px;
   width: 20%!important;
  }
}
</style>
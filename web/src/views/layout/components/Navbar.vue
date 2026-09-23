<template>
  <div class="navbar">
    <!-- <img src="./logo.png" style="    width: 206px;margin-top: 24px;" /> -->
    <img
      src="../../../assets/img/systemTestLogo.png"
      style="cursor: pointer; position: absolute; left: 25px; top: 13px; z-index: 1000 !important"
      @click="handleImgClick"
      height="35"
      width="306"
    />

    <!-- 菜单 -->
    <mymenu></mymenu>

    <!-- 个人中心 -->
    <div class="new_right_toolbar">
      <div class="new_right_toolbar_inner">
        <div v-if="showSysMessageBell" class="message-icon-wrapper">
<!--          <menu-search></menu-search>-->
          <el-popover
            ref="messagePopover"
            v-model="messagePopoverShow"
            placement="bottom"
            trigger="hover"
            width="420"
            popper-class="message-popover-container"
            :append-to-body="true"
            @click="messagePopoverShow = !messagePopoverShow"
          >
            <div class="popover-inner-wrapper">
              <div class="popover-header">
                <span class="popover-title2">系统消息</span>
                <span class="badge">{{ dataMessageData.length }}</span>
              </div>
              <div class="popover-scroll-container">
                <div class="list-body" v-if="dataMessageData.length>0">
                  <div
                    class="list-row"
                    v-for="(item, index) in dataMessageData"
                    :key="index"
                  >
                    <div class="message-card">
                      <div class="message-content">
<!--                        <div class="message-text">产品名称：{{ item.YAXISDATA1 | noDataFilter }}</div>-->
                        <div class="message-text">产品代码：{{ item.YAXISDATA5 | noDataFilter }}</div>
                        <div class="message-text">申请权限：{{ item.YAXISDATA2 | noDataFilter}}</div>
                        <div class="message-text" >处理状态：
                         <span style="color: #70ad47" v-if="item.YAXISDATA3 === '处理完成'"> {{ item.YAXISDATA3 | noDataFilter}}</span>
                         <span style="color: red" v-else-if="item.YAXISDATA3 === '待处理'"> {{ item.YAXISDATA3 | noDataFilter}}</span>
                         <span style="color: #409eff" v-else-if="item.YAXISDATA3 === '处理中'"> {{ item.YAXISDATA3 | noDataFilter}}</span>
                         <span v-else> {{ item.YAXISDATA3 | noDataFilter}}</span>
                        </div>
                        <div class="message-text message-text--last">已拥有权限等级：{{ item.YAXISDATA4 | noDataFilter}}</div>
                      </div>
                      <el-button
                        type="text"
                        size="mini"
                        class="message-mark-read-btn"
                        :loading="isSysMessageMarkReadLoading(item)"
                        @click.stop="onMarkSysMessageRead(item)"
                      >
                        标为已读
                      </el-button>
                    </div>
                  </div>
                </div>
                <div class="list-body" v-else>
                <div style="text-align: center;align-items: center;">暂无系统消息</div>
                </div>
              </div>
            </div>
            <i
              slot="reference"
              class="el-icon-message-solid message-icon"
              :class="{ 'has-unread': dataMessageData.length > 0 }"
              :data-count="dataMessageData.length"
            ></i>
          </el-popover>
        </div>

        <!-- 个人中心 -->
        <div class="personal_center">
          <span v-popover:popover style="padding: 5px">
            <!-- <span class="iconfont icon-D-gerenzhongxin"></span> -->
            <span>{{ $store.getters.name }}</span>
            <i class="el-icon-caret-bottom icon-menu"></i>

          </span>
        </div>
        <span class="segmentation">|</span>
        <!-- <el-tooltip :content="$t('navbar.screenfull')"  effect="dark" placement="bottom"> -->
        <screenfull class="screenfull right-menu-item new_screenfull" fill="#fff" style="position: relative; top: 16px;" />
        <!-- </el-tooltip> -->
      </div>
    </div>

    <el-popover ref="popover" popper-class="admin_popper" v-model="user_popover_show" placement="bottom-end"  style="top: 52px !important" trigger="hover" width="120">
      <div class="admin_box">
        <p class="admin_item" @click="handleEditInfo">个人信息</p>
        <p class="admin_item" @click="changePwd">修改密码</p>
        <p class="admin_item" @click="logout">退出登录</p>
      </div>
    </el-popover>

    <!-- <el-popover ref="admin" v-model="admin_show" placement="left" popper-class="admin_popper" trigger="hover" width="100">

    </el-popover> -->
    <!-- --------------- -->

    <!-- 修改密码 -->
    <div>
      <el-dialog v-dialogDrag :append-to-body="true" :close-on-click-modal="false" :visible.sync="countDialog" center class="changePwd-box" title="修改密码">
        <el-container style="height: 200px">
          <el-main>
            <el-form ref="formCount" :model="formCount" class="standard-form" :rules="countRules" label-position="right">
              <el-form-item :label-width="formLabelWidth" label="原始密码" prop="password">
                <el-input v-model.trim="formCount.password" clearable placeholder="请输入原始密码" show-password size="small" type="text"></el-input>
              </el-form-item>
              <el-form-item :label-width="formLabelWidth" label="新密码" prop="newPassword">
                <el-input v-model.trim="formCount.newPassword" clearable placeholder="请输入新密码" show-password size="small" type="text"></el-input>
              </el-form-item>
              <el-form-item :label-width="formLabelWidth" label="确认密码" prop="newPwdAffirm">
                <el-input v-model.trim="formCount.newPwdAffirm" clearable placeholder="请输入确认密码" show-password size="small" type="text"></el-input>
              </el-form-item>
            </el-form>
          </el-main>
        </el-container>
        <div slot="footer" class="dialog-footer standard-form">
          <el-button :loading="countSubmit_btn" size="small" type="primary" @click="countSubmit('formCount')">提 交</el-button>
          <el-button size="small" type="info" plain @click="countDialog = false">取 消</el-button>
        </div>
      </el-dialog>
    </div>
    <el-dialog
      v-dialogDrag
      v-if="settingVisible"
      :append-to-body="true"
      :close-on-click-modal="false"
      :visible.sync="settingVisible"
      center
      custom-class="setting"
      title="个人信息"
      @close="settingVisible = false"
    >
      <setting @close="settingVisible = false"></setting>
    </el-dialog>
  </div>
</template>

<script>
// import Search from '@/components/HeaderSearch'
import storage from '@/utils/storage'
import { mapGetters } from 'vuex'
import Screenfull from '@/components/Screenfull'
import commonApi from '@/api/common'
import { getCookiesData } from '@/utils/auth'
import pageApi from '@/api/checkPassword.js'
import mymenu from './menuDropDown/index-getMenuAll.vue'
import { getPwdStrategy } from './api/index'
import Setting from './setting'
import MenuSearch from './menuDropDown/MenuSearch.vue'
import invitationApplyApi from '@/views/InvitationApply/scripts/api.js'
// import LockWindows from '../../islockWindowsfile/lock-windows.vue';
export default {
  components: {
    Setting,
    Screenfull,
    mymenu,
    MenuSearch
    // Search
    // LockWindows
  },
  data() {
    //      const newPasswordValidate = (rule, value, callback) => {
    //     if(!value){
    //       callback(new Error('请输入新密码'));
    //     }
    //     else if(!(/^[A-Za-z0-9_]{6,18}$/.test(value))){
    //       callback(new Error('密码为长度在6~18之间，只能包含字母、数字和下划线'));
    //     }
    //     else{
    //       callback();
    //     }
    // };

    const newPasswordValidate = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入新密码'))
      } else {
        let params = {
          password: value
        }
        pageApi
          .checkPassword(params)
          .then((response) => {
            if (response.data.status === 200) {
              callback()
            } else {
              callback(this.pwdMessage)
            }
          })
          .catch(() => {
            callback('校验密码失败')
          })
      }
    }
    const newPwdAffirmValidate = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入确认密码'))
      } else if (this.formCount.newPassword && value !== this.formCount.newPassword) {
        callback(new Error('新密码和确认密码不一致'))
      } else {
        callback()
      }
    }
    return {
      dataMessageData: [],
      /** 正在标记已读的消息 fId（字符串，与 YAXISDATA6 对齐） */
      sysMessageMarkReadFId: null,
      messagePopoverShow: false,
      settingVisible: false,
      formPwdStrategy: {
        pwdLength: '', // 密码长度
        pwdComplexity: [], // 密码复杂度
        pwdAutoUnLock: false, // 是否开始自动解锁
        pwdLockEnable: false, // 是否开启登录失败账户锁定
        pwdLockTime: '', // 锁定时间 (分钟)
        pwdErrCount: '', // 密码输入错误的次数
        pwdContinuityTime: '', //登录的连续时间
        pwdExpiredEnable: false, // 是否开启密码过期
        pwdExpiredTime: '', // 密码过期时间

        minPwdLength: '',
        maxPwdLength: ''
      },
      pwdMessage: '',

      connectedState: '-', //与国君业务总线连通状态

      countDialog: false, //密码重置弹框是否显示
      formCount: {
        password: '', //原始密码
        newPassword: '', //新密码
        newPwdAffirm: '' //确认密码
      },
      countRules: {
        // 原始密码
        password: [{ required: true, type: 'string', message: '请输入原始密码', trigger: 'change' }],
        // 新密码
        newPassword: [{ required: true, trigger: 'change', validator: newPasswordValidate }],
        // 确认密码
        newPwdAffirm: [{ required: true, trigger: 'change', validator: newPwdAffirmValidate }]
      },
      formLabelWidth: '120px',
      countSubmit_btn: false,
      user_popover_show: false,
      admin_show: false
    }
  },
  computed: {
    ...mapGetters(['sidebar', 'name', 'avatar', 'device']),
    sidebar() {
      return this.$store.state.app.sidebar
    },
    /** 仅拥有菜单 40701 权限的用户展示系统消息入口 */
    showSysMessageBell() {
      const menus = this.$store.state.meauList || []
      const hit = (list) => {
        if (!list || !list.length) return false
        for (let i = 0; i < list.length; i++) {
          const m = list[i]
          if (String(m.actionid) === '40701') return true
          if (m.children && m.children.length && hit(m.children)) return true
        }
        return false
      }
      return hit(menus)
    }
  },
  watch: {
    showSysMessageBell: {
      immediate: true,
      handler(val) {
        if (val) {
          this.getSysData()
        } else {
          this.dataMessageData = []
        }
      }
    }
  },
  created() {
    // 获取与国君业务总线连通的状态
    // this.getConnectedState();
    // 每30秒获取一次连接状态
    // let timer = setInterval(() => {
    //    this.getConnectedState();
    // },30000)
  },
  mounted() {
    // 获取校验规则
    this.pwdStrategy()
  },
  methods: {
    isSysMessageMarkReadLoading(item) {
      const raw = item && item.YAXISDATA6
      if (raw === undefined || raw === null || String(raw).trim() === '') return false
      return this.sysMessageMarkReadFId === String(raw).trim()
    },
    async onMarkSysMessageRead(item) {
      const fId = item && item.YAXISDATA6
      if (fId === undefined || fId === null || String(fId).trim() === '') {
        this.$message.warning('无法标记：缺少记录标识')
        return
      }
      const fIdStr = String(fId).trim()
      const fIdNum = Number(fIdStr)
      if (Number.isNaN(fIdNum)) {
        this.$message.warning('无法标记：记录标识无效')
        return
      }
      this.sysMessageMarkReadFId = fIdStr
      try {
        const res = await invitationApplyApi.markAuthApplyMessageRead({ fId: fIdNum })
        const body = res && res.data
        const st = body && body.status
        const msg = String((body && body.message) || '').trim()
        const transportOk = st === 200 || st === 0
        if (!body || !transportOk) {
          this.$message.warning(msg || '标记已读失败')
          return
        }
        /** 网关/datadriver 可能对业务失败仍返回 status=0；业务失败请看 message（勿仅用 resultCount，成功响应也可能不带行数） */
        const bizFailed = /未更新任何记录/i.test(msg)
        if (bizFailed) {
          this.$message.warning(msg || '标记已读失败')
          return
        }
        await this.getSysData()
      } catch (e) {
        this.$message.warning('标记已读请求失败')
      } finally {
        this.sysMessageMarkReadFId = null
      }
    },
    getSysData() {
      const params = {
        indexCode: 'ec596f08-ad56-4fef-ab56-b7dea4f4498a'
      }
      return commonApi.getDataBysqlCode(params).then((res) => {
        const {status, data} = res.data
        if (status === 0) {
          this.dataMessageData = data || []
        }
      })
    },
    handleEditInfo() {
      this.settingVisible = true
    },
    // 密码策略设置
    pwdStrategy() {
      this.pwdStrategyLoading = true
      // 密码策略赋值
      getPwdStrategy().then((response) => {
        this.pwdStrategyDialog = true
        // 值清空
        this.$nextTick(() => {
          this.formPwdStrategy.pwdComplexity = []

          if (response.data.status === 0) {
            let res = response.data.data
            // 密码长度
            //  if(res.pwdLength){
            //    this.formPwdStrategy.pwdLength = res.pwdLength;
            //  }

            if (res.pwdLength) {
              let pwdSet = res.pwdLength.split('-')
              this.formPwdStrategy.pwdLength = res.pwdLength
              this.formPwdStrategy.minPwdLength = pwdSet[0]
              this.formPwdStrategy.maxPwdLength = pwdSet[1]
            }
            // 密码复杂度
            if (res.pwdComplexity) {
              this.formPwdStrategy.pwdComplexity = res.pwdComplexity.split(',')
            }
            // 是否开始自动解锁
            if (res.pwdAutoUnLock === true || res.pwdAutoUnLock === false) {
              this.formPwdStrategy.pwdAutoUnLock = res.pwdAutoUnLock
            }
            // 是否开启登录失败账户锁定
            if (res.pwdLockEnable === true || res.pwdLockEnable === false) {
              this.formPwdStrategy.pwdLockEnable = res.pwdLockEnable
            }
            // 锁定时间 (分钟)
            if (res.pwdLockTime) {
              this.formPwdStrategy.pwdLockTime = res.pwdLockTime
            }
            // 密码输入错误的次数
            if (res.pwdErrCount) {
              this.formPwdStrategy.pwdErrCount = res.pwdErrCount
            }
            //登录的连续时间
            if (res.pwdContinuityTime) {
              this.formPwdStrategy.pwdContinuityTime = res.pwdContinuityTime
            }
            // 是否开启密码过期
            if (res.pwdExpiredEnable === true || res.pwdExpiredEnable === false) {
              this.formPwdStrategy.pwdExpiredEnable = res.pwdExpiredEnable
            }
            // 密码过期时间
            if (res.pwdExpiredTime) {
              this.formPwdStrategy.pwdExpiredTime = res.pwdExpiredTime
            }

            // 装填提示信息语句
            this.pwdMessage = `密码长度为${this.formPwdStrategy.pwdLength},包含`
            for (let i = 0; i < this.formPwdStrategy.pwdComplexity.length; i++) {
              let temp = this.formPwdStrategy.pwdComplexity[i]
              if (temp == '1') {
                this.pwdMessage += `数字 `
              } else if (temp == '2') {
                this.pwdMessage += `字母 `
              } else if (temp == '3') {
                this.pwdMessage += `特殊字符 `
              }
              if ((i !== this.formPwdStrategy.pwdComplexity.length - 1 && temp == '1') || temp == '2' || temp == '3') {
                this.pwdMessage += '、'
              }
            }
          }
        })
      })
    },
    // 跳转到首页
    handleImgClick() {
      this.$router.push({ path: '/dashboard' })
    },
    // 锁屏
    handelLock() {
      storage.setItem('isLock', { isLock: true })
      this.$store.state.lock.isLock.isLock = true
      this.user_popover_show = false
    },
    // 获取与国君业务总线连通的状态
    getConnectedState() {
      commonApi.getConStatus().then((res) => {
        if (res.data.status === 200) {
          this.connectedState = '成功'
        } else {
          this.connectedState = '未连接'
        }
      })
    },
    // 跳转首页
    linkDashboardClick() {
      this.$router.push({ path: '/dashboard' })
    },
    logout() {
      this.$store
        .dispatch('LogOut')
        .then(() => {
          location.reload() // In order to re-instantiate the vue-router object to avoid bugs
        })
        .catch(() => {
          //即使失败也跳转
          location.reload()
        })
    },

    // 修改密码
    changePwd() {
      this.countDialog = true
      this.$nextTick(() => {
        this.$refs['formCount'].resetFields()
      })
      this.user_popover_show = false
    },
    countSubmit(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let params = JSON.parse(JSON.stringify(this.formCount))
          // 删除确认密码字段
          delete params.newPwdAffirm
          // 添加userId字段
          let userData = JSON.parse(getCookiesData('BAIDUID') || '{}')
          params.userId = userData.userId
          params.newPasswordPlain = this.formCount.newPassword
          this.countSubmit_btn = true
          this.$store
            .dispatch('changePwd', params)
            .then((res) => {
              this.countSubmit_btn = false
              this.countDialog = false
              this.$message.closeAll()
              this.$message({
                message: '重置密码成功',
                type: 'success'
              })

              // 调用退出登录
              this.$store
                .dispatch('LogOut')
                .then(() => {
                  location.reload()
                })
                .catch(() => {
                  // 即使失败也跳转
                  location.reload()
                })
              // this.$alert('重置密码成功后请重新登录！', '提示', {
              //    confirmButtonText: '确定',
              //    type: 'warning',
              //    showClose:false
              // }).then(() => {
              //     // 调用退出登录
              //     this.$store.dispatch('LogOut').then(() => {
              //     location.reload()
              //     }).catch(() => {
              //       // 即使失败也跳转
              //      location.reload()
              //     })
              // }).catch(() => {});
            })
            .catch((error) => {
              this.countSubmit_btn = false
              this.$message.closeAll()
              this.$message({
                message: error || '重置密码失败',
                type: 'error'
              })
            })
        } else {
          return false
        }
      })
    }
  }
}
</script>

<style lang="scss">
.message-popover-container {
  width: 420px !important;
  height: 400px !important;
  min-height: 400px !important;
  max-height: 400px !important;
  overflow: hidden !important;
  padding: 0 !important;
  box-sizing: border-box !important;
}

.popover-scroll-container::-webkit-scrollbar {
  width: 6px !important;
  display: block !important;
}
.popover-scroll-container::-webkit-scrollbar-track {
  background: #f5f5f5 !important;
  border-radius: 3px !important;
}
.popover-scroll-container::-webkit-scrollbar-thumb {
  background: #dcdfe6 !important;
  border-radius: 3px !important;
}
.popover-scroll-container::-webkit-scrollbar-thumb:hover {
  background: #c0c4cc !important;
}
</style>

<style lang="scss" scoped>
::v-deep .setting.el-dialog { width: 60% !important; }

.message-icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 9999 !important;
  position: relative;

  .message-icon {
    color: #ffffff !important;
    font-size: 18px !important;
    padding: 10px !important;
    position: relative;

    &:hover { color: #e9c39e !important; }
    &.has-unread::after {
      content: attr(data-count);
      position: absolute;
      top: 2px; right: 2px;
      background: #f56c6c; color: white;
      font-size: 10px; border-radius: 50%;
      min-width: 14px; height: 14px; padding: 0 2px;
      display: flex; align-items: center; justify-content: center;
      opacity: 1;
    }
  }
}
.popover-inner-wrapper {
  height: 100% !important;
  display: flex;
  flex-direction: column;
  overflow: hidden !important;
  box-sizing: border-box !important;
}

.popover-header {
  height: 50px !important;
  padding: 0 16px !important;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fafafa;
  border-bottom: 1px solid #f0f0f0;
  flex-shrink: 0 !important;
  box-sizing: border-box !important;

  .popover-title2 {
    font-size: 16px; font-weight: 600;
    color: #303133; margin: 0;
  }
  .badge {
    background: #f56c6c; color: white;
    font-size: 12px; padding: 2px 8px;
    border-radius: 10px;
  }
}

.popover-scroll-container {
  flex: 1 !important;
  height: calc(100% - 90px) !important;
  overflow-x: hidden !important;
  overflow-y: scroll !important;
  padding: 8px 0 !important;
  box-sizing: border-box !important;
}

.list-body {
  padding: 0 16px !important;
  box-sizing: border-box !important;

  .list-row {
    margin-bottom: 8px !important;
    &:last-child { margin-bottom: 0 !important; }

      .message-card {
      position: relative;
      padding: 12px 10px 12px 12px;
      padding-right: 5.75rem;
      background: #fff;
      border-radius: 6px;
      border: 1px solid #f0f0f0;
      transition: all 0.2s;
      box-sizing: border-box !important;

      &:hover {
        border-color: #e4e7ed;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
      }

      .message-mark-read-btn {
        position: absolute;
        right: 8px;
        bottom: 10px;
        padding: 0 !important;
        margin: 0 !important;
        line-height: 1.2;
        height: auto;
        font-size: 12px;
        color: #a15008 !important;
      }

      .message-tag {
        padding: 4px 10px;
        border-radius: 4px;
        font-size: 12px;
        color: white;
        font-weight: 500;
        margin-right: 12px;
        white-space: nowrap;
        flex-shrink: 0;
      }

      .message-content {
        flex: 1; min-width: 0;

        .message-text {
          font-size: 13px; color: #303133;
          line-height: 1.5; margin-bottom: 6px;
          word-break: break-all;

          &.message-text--last { margin-bottom: 0; }
        }
      }
    }
  }
}

.new_right_toolbar {
  position: absolute;
  top: 3px;
  right: 14px;
  height: 100%;
  z-index: 999 !important;

  .new_right_toolbar_inner {
    display: flex;
    align-items: center;
    gap: 12px;
    .personal_center {
      span {
        font-size: 14px;
        //color: black;
        color: #ffffff;
        cursor: pointer;
      }
      &:hover { span, i { color: #e9c39e !important; } }
    }
    .segmentation { margin: 0 16px; color: #fff; }
  }
}

.user_popover .user_box .user_item {
  cursor: pointer; padding: 6px 0; margin: 2px 0;
  &:hover {
    background: #f9f0e6; color: #a15008;
    .color_B4B9C9 { color: #1078b0 !important; }
  }
  .color_B4B9C9 { color: #b4b9c9; }
}

.admin_popper .admin_box .admin_item {
  cursor: pointer; padding: 6px 0; margin: 2px 0;
  text-align: center;
  &:hover {
    background: #f9f0e6; color: #a15008;
  }
}

.handelLock {
  position: fixed;
  top: 10px;
  right: 117px;
  width: 25px;
  height: 25px;
  cursor: pointer;
  // background-image: url('../../../assets/img/lock.png');
  // -moz-background-size:100% 100%; background-size:100% 100%;
  i {
    color: #fff;
    position: absolute;
    top: 1px;
    left: 3px;
    font-size: 22px;
  }
}

.navbar {
  z-index: 1001 !important;
  width: 100%;
  min-width: 1200px;
  height: 60px;
  line-height: 60px;
  border-radius: 0px !important;
  border:0px !important;
  //border-bottom: 2px solid #d8dce5;
  //overflow: hidden;
  position: fixed;
  top: 0px;
  left: 0px;
  //background-color: #242836;
   background-image: url('../../../assets/img/gfdashboardimg1.png');
  background-size: 100% 100%;
  background-repeat: no-repeat;
  //border-bottom: 1px solid #d8dce5;
  //box-shadow: -2px 2px 6px rgba(0, 0, 0, .12);

  .hamburger-container {
    line-height: 48px;
    height: 40px;
    float: left;
    padding: 0 10px;
  }

  .errLog-container {
    display: inline-block;
    vertical-align: top;
  }

  .right-menu {
    position: absolute;
    right: 0px;
    top: 10px;
    height: 100%;

    &:focus {
      outline: none;
    }

    .right-menu-item {
      display: inline-block;
      margin: 0 8px;
    }

    // 连通状态样式
    .connected-state-box {
      height: 25px;
      line-height: 25px;
      font-size: 14px;
      position: absolute;
      top: 0px;
      right: 17px;
      color: #fff;
      z-index: 1;
    }

    .screenfull {
      height: 40px;
      color: #20212b !important;
    }

    .international {
      vertical-align: top;
    }

    .theme-switch {
      vertical-align: 15px;
    }

    .avatar-container {
      height: 70px;
      margin: 0px !important;

      .avatar-wrapper {
        margin-top: 5px;
        position: relative;
        display: inline-block;

        .user-avatar {
          cursor: pointer;
          position: absolute;
          right: -20px;
          top: 4px;
          font-size: 14px;
          padding: 5px !important;
        }
      }
    }

    .environment {
      width: 36px;
      display: inline-block;
      vertical-align: top;
      line-height: 70px;
      text-align: center;
      font-size: 15px;
      color: #fff;
    }
  }
}
</style>

<style lang="scss" rel="stylesheet/scss">
.changePwd-box {
  .el-dialog {
    width: 484px !important;

    .el-form {
      width: 100% !important;
      margin: auto;

      .el-form-item {
        width: 90%;
        margin-right: 0px;
        margin-bottom: 15px !important;

        .el-form-item__content {
          width: calc(100% - 120px);

          .el-input--small {
            width: 100% !important;
          }
        }
      }
    }
  }
}
</style>

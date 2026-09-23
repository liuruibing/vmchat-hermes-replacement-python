<!--
 * @Description: 
 * @Author: 
 * @Date: 2024-06-27 17:46:38
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2024-07-22 11:31:19
-->
<template>
  <div id="rule_email_dialog">
    <el-dialog
      custom-class="warningMonitoring-dialog"
      title="邮箱设置"
      :visible.sync="visible"
      width="580px !important"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      @close="handleClose"
    >
      <el-form :model="formData" :rules="rules" ref="formData" label-width="150px" class="standard-form" style="width: 85% !important">
        <el-form-item label="我的邮箱" prop="myEmail">
          <el-checkbox v-model="formData.smyemail" :true-label="1" false-label="" style="position: absolute; top: 0; left: -94px"></el-checkbox>
          <el-input v-model="formData.myEmail" size="small" disabled style="width: 100% !important"></el-input>
          <!-- <i class="el-icon-circle-plus" style="position: absolute; top: 12px; right: -20px" @click="onAddItem"></i> -->
        </el-form-item>
        <el-form-item
          v-for="(item, index) in formData.emailList"
          :key="index"
          label="追加邮箱"
          :prop="'emailList.' + index + '.value'"
          :rules="[
            { required: false, message: '请填写邮箱', trigger: 'change' },
            { type: 'email', message: '请输入正确的邮箱地址', trigger: 'change' }
          ]"
        >
          <el-input v-model="item.value" size="small" placeholder="请输入" style="width: 100% !important"></el-input>
          <i v-if="index === 0" class="el-icon-circle-plus" style="position: absolute; top: 12px; right: -20px" @click="onAddItem"></i>
          <i v-else class="el-icon-remove" style="position: absolute; top: 12px; right: -20px" @click="onRemoveRow(index)"></i>
        </el-form-item>
      </el-form>
      <div class="standard-form" style="text-align: center; margin-top: 20px">
        <el-button size="small" info plain @click="handleClose()" :disabled="btnDisabled">取 消</el-button>
        <el-button size="small" type="primary" @click="submitForm()" :disabled="btnDisabled">确 认</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import CONSTANTS from '../scripts/constants.js'
import pageApi from '../scripts/api.js'
export default {
  name: '',
  components: {},
  data() {
    return {
      visible: true,
      CONSTANTS,
      modalType: 'add',
      rowData: {},
      formData: {
        myEmail: '',
        smyemail: '',
        emailList: [{ value: '' }]
      },
      rules: {},
      btnDisabled: false
    }
  },
  mounted() {},
  methods: {
    // 回显
    init({ row, data }) {
      this.modalType = 'edit'
      this.rowData = JSON.parse(JSON.stringify(row))
      const myEmailObj = data.find((item) => item.smyemail == 1) || {}
      let BAIDUID = JSON.parse(localStorage.getItem('BAIDUID')) || {}
      this.formData.myEmail = myEmailObj.mailbox || BAIDUID.email || ''
      this.formData.smyemail = myEmailObj.smyemail || ''
      const moreEmailObj = data.find((item) => !item.smyemail && item.mailbox)
      if (moreEmailObj) {
        let emails = moreEmailObj.mailbox.split(';')
        const emailList = emails.map((item) => ({ value: item }))
        this.formData.emailList = emailList
      }
    },
    onAddItem() {
      this.formData.emailList.push({ value: '' })
    },
    onRemoveRow(index) {
      this.formData.emailList.splice(index, 1)
    },
    // 关闭dialog
    handleClose() {
      this.$emit('close')
      this.visible = false
    },
    submitForm() {
      this.$refs['formData'].validate((valid) => {
        if (valid) {
          this.onSubmit()
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    // 新增提交
    onSubmit() {
      this.$message.closeAll()
      const { myEmail, smyemail, emailList } = this.formData
      let list = []
      // 我的邮箱
      if (smyemail == 1) {
        list.push({ mailbox: myEmail || '', smyemail: 1 })
      }
      // 追加邮箱
      let moreEmails = emailList.filter((item) => item.value).map((item) => item.value)
      if (moreEmails.length) {
        list.push({ mailbox: moreEmails.join(';') })
      }
      let params = {
        id: this.rowData.id,
        rkWrulesMailboxModelList: list
      }
      this.btnDisabled = true
      pageApi.emailSettings(params).then((res) => {
        this.btnDisabled = false
        const { status, message } = res.data
        if (status === 200) {
          this.$message.success(message || '操作成功')
          this.handleClose()
        } else {
          this.$message.error(message || '操作成功')
        }
      })
    }
  }
}
</script>
<style lang="scss">
#rule_email_dialog {
  .warningMonitoring-dialog {
    .el-button--primary {
      color: #fff !important;
    }
  }
}
</style>

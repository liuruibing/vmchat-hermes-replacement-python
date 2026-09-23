<!--
 * @Description:
 * @Author:
 * @Date: 2024-06-27 17:46:38
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2024-07-15 11:00:28
-->
<template>
  <div id="jk-detail-dialog">
    <el-dialog title="监控详情" :visible.sync="visible" width="50% !important" :close-on-click-modal="false" :close-on-press-escape="false" @close="handleClose">
      <el-form :model="formData" :rules="rules" ref="formData" label-width="120px" class="demo-ruleForm">
        <el-row>
          <el-col :span="12">
            <el-form-item label="监控对象代码" prop="objcode">
              <el-input v-model="formData.objcode" size="small" disabled style="width: 100% !important"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="监控对象名称" prop="objname">
              <el-input v-model="formData.objname" size="small" disabled style="width: 100% !important"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="管理人名称" prop="mgrname">
              <el-input v-model="formData.mgrname" size="small" disabled style="width: 100% !important"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="预警规则名称" prop="rulesname">
              <el-input v-model="formData.rulesname" size="small" disabled style="width: 100% !important"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="业务日期" prop="fdate">
              <el-input v-model="formData.fdate" size="small" disabled style="width: 100% !important"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="风险等级" prop="warnLevel">
              <el-input v-model="formData.warnLevel" size="small" disabled style="width: 100% !important"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="warnStatus">
              <el-input v-model="formData.warnStatus" size="small" disabled style="width: 100% !important"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="连续预警天数" prop="warnDays">
              <el-input v-model="formData.warnDays" size="small" disabled style="width: 100% !important"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮件提醒" prop="sendemail">
              <el-input v-model="formData.sendemail" size="small" disabled style="width: 100% !important"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="生成时间" prop="createdate">
              <el-input v-model="formData.createdate" size="small" disabled style="width: 100% !important"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="数据详情" prop="resultsJson">
          <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="" v-model="formData.resultsJson" disabled></el-input>
        </el-form-item>
      </el-form>
      <div style="text-align: center; margin-top: 20px" class="standard-form">
        <el-button type="primary" size="small" @click="handleClose()">确认</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: '',
  components: {},
  data() {
    return {
      visible: true,
      formData: {
        objcode: '',
        objname: '',
        mgrname: '',
        rulesname: '',
        fdate: '',
        warnLevel: '',
        warnStatus: '',
        warnDays: '',
        sendemail: '',
        createdate: '',
        resultsJson: ''
      },
      rules: {}
    }
  },
  mounted() {},
  methods: {
    init(data) {
      for (let key in this.formData) {
        this.formData[key] = data[key] || ''
      }
    },
    handleClose() {
      this.$emit('close')
      this.visible = false
    },
    onSubmit() {}
  }
}
</script>
<style lang="scss">
#jk-detail-dialog {
  .el-dialog__wrapper .el-button--medium {
    color: #ffffff !important;
  }
}
</style>

<!--
 * @Description:
 * @Author:
 * @Date: 2024-06-27 17:46:38
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2024-07-15 15:37:42
-->
<template>
  <div id="gz-detail-dialog">
    <el-dialog title="规则详情" :visible.sync="visible" width="30% !important" :close-on-click-modal="false" :close-on-press-escape="false" @close="handleClose">
      <el-form :model="formData" :rules="rules" ref="formData" label-width="120px" class="demo-ruleForm">
        <el-form-item label="预警规则名称" prop="rulesname">
          <el-input v-model="formData.rulesname" size="small" disabled style="width: 100% !important"></el-input>
        </el-form-item>
        <el-form-item label="指标名称" prop="itname">
          <el-input v-model="formData.itname" size="small" disabled style="width: 100% !important"></el-input>
        </el-form-item>
        <el-form-item label="指标适用类型" prop="ittypeStr">
          <el-input v-model="formData.ittypeStr" size="small" disabled style="width: 100% !important"></el-input>
        </el-form-item>
        <el-form-item label="预警规则描述" prop="wrulesDesc">
          <el-input v-model="formData.wrulesDesc" size="small" disabled style="width: 100% !important"></el-input>
        </el-form-item>
        <el-form-item label="风险等级" prop="warnLevel">
          <el-input v-model="formData.warnLevel" size="small" disabled style="width: 100% !important"></el-input>
        </el-form-item>
        <el-form-item label="备注" prop="itremark">
          <el-input type="itremark" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="" v-model="formData.itremark" disabled></el-input>
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
        rulesname: '',
        itname: '',
        ittypeStr: '',
        wrulesDesc: '',
        warnLevel: '',
        itremark: ''
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
#gz-detail-dialog {
  .el-dialog__wrapper .el-button--medium {
    color: #ffffff !important;
  }
}
</style>

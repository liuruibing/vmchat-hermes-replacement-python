<!--
 * @Description: 
 * @Author: 
 * @Date: 2025-11-19 14:43:08
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2025-12-30 15:37:50
-->
<template>
  <div>
    <el-dialog :visible.sync="visible" :title="dialogTitle" width="650px !important" :close-on-click-modal="false"
      :close-on-press-escape="false" @closed="handleClose">
      <el-form :model="formData" :rules="rules" ref="form" label-width="100px">
        <el-form-item label="明细维度" prop="details" v-if="detailOption.length">
          <MySelectMultiple v-model="formData.details" :options="detailOption"
            :optionsProps="{ value: 'vcId', label: 'vcIndexName' }" placeholder="请选择" size="small"></MySelectMultiple>
        </el-form-item>
        <el-form-item label="时间维度" prop="times" v-if="timeOption.length">
          <MySelectMultiple v-model="formData.times" :options="timeOption"
            :optionsProps="{ value: 'vcId', label: 'vcIndexName' }" placeholder="请选择" size="small"></MySelectMultiple>
        </el-form-item>
        <el-form-item label="单位维度" prop="unit" v-if="unitOption.length">
          <el-radio-group v-model="formData.unit">
            <el-radio v-for="item in unitOption" :key="item.vcId" :label="item.vcId">{{ item.vcIndexName }}</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="visible = false">取 消</el-button>
        <el-button type="primary" @click="handleSubmit">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import MySelectMultiple from '../../components/MySelectMultiple.vue'
export default {
  name: 'IndexParamSet',
  components: {
    MySelectMultiple
  },
  data() {
    return {
      visible: false,
      dialogTitle: '',
      indexInfo: {},
      formData: {
        details: [],
        times: [],
        unit: ''
      },
      rules: {
        details: [{ required: true, message: '请选择明细维度', trigger: 'change' }],
        times: [{ required: true, message: '请选择时间维度', trigger: 'change' }],
        unit: [{ required: true, message: '请选择单位维度', trigger: 'change' }]
      },
      detailOption: [],
      timeOption: [],
      unitOption: []
    }
  },
  mounted() {
    this.visible = true
  },
  methods: {
    init(data) {
      this.indexInfo = _.cloneDeep(data)
      this.dialogTitle = this.indexInfo.vcIndexName
      const { params, paramsValue } = this.indexInfo
      const { details, times, units } = params || {}
      this.detailOption = details || [];
      this.timeOption = times || [];
      this.unitOption = units || [];
      const { details: detailsVal = [], times: timesVal = [], unit: unitVal = {} } = paramsValue || {}
      this.formData.details = detailsVal.map(item => item.vcId)
      this.formData.times = timesVal.map(item => item.vcId)
      this.formData.unit = unitVal.vcId || (units && units.length ? units[0].vcId : '')
    },
    handleClose() {
      this.visible = false
      this.$emit('close')
    },
    handleSubmit() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          const detailsVal = this.detailOption.filter(item => this.formData.details.includes(item.vcId))
          const timesVal = this.timeOption.filter(item => this.formData.times.includes(item.vcId))
          const unitVal = this.unitOption.find(item => item.vcId === this.formData.unit) || {}
          const params = {
            ...this.indexInfo,
            paramsValue: {
              details: detailsVal,
              times: timesVal,
              unit: unitVal
            }
          }
          this.$emit('submit', params)
          this.handleClose()
        }
      })
    }
  }
}
</script>

<style></style>
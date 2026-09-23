<template>
  <div id="mnzh-container">
    <el-form :inline="true" :model="formInline" :rules="formRules" ref="formInline" class="demo-form-inline standard-form" label-position="right" label-width="auto">
      <el-row>
        <el-col :span="6">
          <el-form-item label="组合名称" prop="combineName">
            <el-input v-model="formInline.combineName" placeholder="组合名称" size="small"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="组合成立日期" prop="foundDate">
            <el-date-picker
              :picker-options="pickerOptions"
              :disabled="saveEditFundFlag"
              v-model="formInline.foundDate"
              type="date"
              size="small"
              value-format="yyyy-MM-dd"
              placeholder="选择日期"
            ></el-date-picker>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="初始资金(万元)" prop="price">
            <el-input :disabled="saveEditFundFlag" v-model="formInline.price" placeholder="初始资金"  size="small" onkeyup="value=value.replace(/[^0-9.]/g,'')"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="业绩基准" prop="beCode">
            <el-select v-model="formInline.beCode" placeholder="请选择" size="small" clearable>
              <el-option v-for="item in kpiStandardOpts" :key="item.DIM_CDE" :label="item.DIM_NME" :value="item.DIM_CDE"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="6">
          <el-form-item label="份额(万份)">
            <el-input v-model="formInline.amount" placeholder="份额" size="small" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="6">
<!--          <el-form-item label="拟合频率" prop="frequency">
            <el-select v-model="formInline.frequency" placeholder="请选择" size="small" clearable>
              <el-option v-for="item in frequencyOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item>-->
        </el-col>
      </el-row>
    </el-form>
    <div style="text-align: center; padding: 20px 0" class="standard-form">
      <el-button type="primary" size="small" @click="handleSaveComb" :loading="loading">{{ btnTxt }}</el-button>
    </div>
  </div>
</template>

<script>
import { frequencyOptions } from '@/dataDictionary/frequency'
import request from '@/utils/request'
import { saveComb, saveEditComb } from '../scripts/api'
export default {
  name: 'CreateComposition',
  props: {
    selectList: {
      type: Array,
      required: true,
      default: () => {
        return []
      }
    },
    subCombineCode: {
      type: String,
      default: ''
    },
    saveEditFundFlag: {
      type: Boolean,
      required: true,
      deafult: () => {
        return false
      }
    }
  },
  watch: {
    'formInline.price': {
      handler(val) {
        if (val) {
          this.formInline.amount = val
        } else {
          this.formInline.amount = ''
        }
      }
    }
  },
  data() {
    return {
      formInline: {
        frequency: 'D',//默认日频
        combineName: '',
        foundDate: '',
        price: '',
        beCode: '',
        amount: ''
      },
      formRules: {
        frequency: [{ required: true, message: '请选择拟合频率', trigger: 'change' }],
        beCode: [{ required: true, message: '请选择业绩基准', trigger: 'change' }],
        combineName: [{ required: true, message: '请填写组合名称', trigger: 'blur' }],
        price: [{ required: true, message: '请填写初始资金', trigger: 'blur' }],
        foundDate: [{ required: true, message: '请选择成立日期', trigger: 'change' }]
      },
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() > Date.now() // 禁用未来的日期
        }
      },
      btnTxt: '保存并进入权重设置',
      frequencyOptions: frequencyOptions,
      kpiStandardOpts: [],
      loading: false
    }
  },
  mounted() {
    this.getKpiOptions()
  },
  methods: {
    /**
     * @description 获取模拟组合 - 业绩基准下拉
     */
    getKpiOptions() {
      request({
        url: `/api/report/v1.0/data/sql/d62e680a-5ef8-415e-9764-983d50107d2b`,
        method: 'post',
        data: {
          indexCode: 'd62e680a-5ef8-415e-9764-983d50107d2b'
        }
      })
        .then((res) => {
          if (res.data.status === 0) {
            this.kpiStandardOpts = res.data.data || []
          }
        })
        .catch((err) => {})
    },
    /**
     * @description 创建模拟组合保存/编辑
     */
    handleSaveComb() {
      this.$refs.formInline.validate((valid) => {
        if (valid) {
          if (this.btnTxt === '保存修改') {
            const params = Object.assign({}, this.formInline)
            params.price = params.price * 10000
            params.amount = params.amount * 10000
            params.combineCode = this.subCombineCode
            this.loading = true
            saveEditComb(params)
              .then((res) => {
                if (res.data.status === 0) {
                  this.$message.closeAll()
                  this.$message({
                    type: 'success',
                    message: res.data.message || '修改成功',
                    customClass: 'message-success'
                  })
                  this.$emit('savecomb', {
                    ddate: this.formInline.foundDate,
                    price: this.formInline.price,
                    beCodeName: this.beCodeValToName(this.formInline.beCode)
                  })
                  this.loading = false
                } else {
                  this.$message.closeAll()
                  this.$message({
                    type: 'error',
                    message: res.data.message || '修改失败',
                    customClass: 'message-error'
                  })
                  this.loading = false
                }
              })
              .catch((e) => {
                this.loading = false
              })
          } else {
            const subFundList = this.selectList.map((item) => {
              return {
                fundCode: item.VC_FUNDCODE,
                fundName: item.VC_FUNDNAME
              }
            })
            const params = Object.assign({}, this.formInline)
            params.subFundList = subFundList
            params.price = params.price * 10000
            params.amount = params.amount * 10000
            // params.combineCode = this.subCombineCode
            this.loading = true
            saveComb(params)
              // saveEditComb(params)
              .then((res) => {
                if (res.data.status === 0) {
                  this.btnTxt = '保存修改'
                  this.$message.closeAll()
                  this.$message({
                    type: 'success',
                    message: res.data.message || '保存成功',
                    customClass: 'message-success'
                  })
                  this.$emit('savecomb', {
                    combineCode: res.data.data.combineCode,
                    ddate: this.formInline.foundDate,
                    pid: res.data.data.fid,
                    price: this.formInline.price,
                    combineName: this.formInline.combineName,
                    beCodeName: this.beCodeValToName(this.formInline.beCode)
                  })
                  this.loading = false
                } else {
                  this.$message.closeAll()
                  this.$message({
                    type: 'error',
                    message: res.data.message || '保存失败',
                    customClass: 'message-error'
                  })
                  this.loading = false
                }
              })
              .catch((e) => {
                this.loading = false
              })
          }
        } else {
          return false
        }
      })
    },
    beCodeValToName(code) {
      let name = ''
      for (let i = 0; i < this.kpiStandardOpts.length; i++) {
        let temp = this.kpiStandardOpts[i]
        if (code == temp.DIM_CDE) {
          return temp.DIM_NME
        }
      }
      return ''
    }
  }
}
</script>
<style scoped lang="scss">
#mnzh-container {
  ::v-deep .el-input__inner {
    border: 1px solid #cccccc !important;;

  }
}

</style>

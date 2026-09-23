<template>
  <div class="edit-comb">
    <el-form ref="formEdit" :model="formEdit" :rules="formEditRules" inline class="standard-form" label-position="right" label-width="120px">
      <el-form-item label="组合名称" prop="combineName">
        <el-input v-model="formEdit.combineName" size="small"></el-input>
      </el-form-item>
      <el-form-item label="拟合频率" prop="frequency">
        <el-select v-model="formEdit.frequency" size="small" clearable>
          <el-option v-for="item in frequencyOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="成立日期" prop="foundDate">
        <el-date-picker :disabled="true" v-model="formEdit.foundDate" size="small" type="date" value-format="yyyy-MM-dd"></el-date-picker>
      </el-form-item>
      <el-form-item label="初始资金(万元)" prop="price">
        <el-input :disabled="true" v-model="formEdit.price" size="small" onkeyup="value=value.replace(/[^0-9.]/g,'')"></el-input>
      </el-form-item>
      <el-form-item label="业绩基准" prop="beCode">
        <el-select v-model="formEdit.beCode" clearable placeholder="请选择" size="small">
          <el-option v-for="item in kpiStandardOpts" :key="item.DIM_CDE" :label="item.DIM_NME" :value="item.DIM_CDE"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="份额(万份)">
        <el-input v-model="formEdit.amount" size="small" disabled></el-input>
      </el-form-item>
    </el-form>
    <el-row style="text-align: center" class="standard-form">
      <el-button size="small" type="primary" @click="handleSaveComb">提 交</el-button>
    </el-row>
  </div>
</template>

<script>
import { frequencyOptions } from '@/dataDictionary/frequency'
import { saveEditComb } from '../scripts/api'
export default {
  name: 'editComb',
  data() {
    return {
      formEdit: {
        combineName: '',
        frequency: '',
        foundDate: '',
        beCode: '',
        amount: '',
        price: '',
        combineCode: ''
      },
      frequencyOptions,
      formEditRules: {
        combineName: [
          {
            required: true,
            message: '组合名称不能为空',
            trigger: 'blur'
          }
        ],
        frequency: [
          {
            required: true,
            message: '拟合频率不能为空',
            trigger: 'change'
          }
        ],
        beCode: [
          {
            required: true,
            message: '业绩基准不能为空',
            trigger: 'change'
          }
        ],
        foundDate: [
          {
            required: true,
            message: '成立日期不能为空',
            trigger: 'change'
          }
        ],
        price: [
          {
            required: true,
            message: '初始资金不能为空',
            trigger: 'blur'
          }
        ]
      }
    }
  },
  props: {
    currentCombRow: {
      type: Object,
      default: () => {}
    },
    kpiStandardOpts: {
      type: Array,
      default: () => []
    }
  },
  watch: {
    currentCombRow: {
      handler(val) {
        if (Object.keys(val).length > 0) {
          for (const key in this.formEdit) {
            this.formEdit[key] = val[key]
          }
        }
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    /**
     * @description 编辑保存
     */
    handleSaveComb() {
      this.$refs.formEdit.validate((valid) => {
        if (valid) {
          saveEditComb(this.formEdit).then((res) => {
            if (res.data.status === 0) {
              this.$message({
                type: 'success',
                message: res.data.message || '保存成功',
                customClass: 'message-success'
              })
              this.$emit('closeEdit', 'REFESH')
            } else {
              this.$message({
                type: 'error',
                message: res.data.message || '保存失败',
                customClass: 'message-error'
              })
            }
          })
        } else {
          return false
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
::v-deep .el-form {
  width: 100% !important;
}
</style>

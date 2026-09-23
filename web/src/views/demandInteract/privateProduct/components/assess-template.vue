<template>
  <div class="assess-template">
    <el-form ref="formData" :model="formData" :rules="rules" style="margin: 0 auto" label-width="120px">
      <el-form-item label="估值文件模板" prop="templateId">
        <el-select
          class="template"
          v-model="formData.templateId"
          size="small"
          filterable
          placeholder="请选择"
        >
          <el-option
            v-for="item in tempateOptions"
            :key="item.FID"
            :label="item.TEMPLATENAME"
            :value="item.FID"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="匹配规则" prop="matchingRule">
        <el-input v-model="formData.matchingRule" placeholder="请输入" type="textarea"></el-input>
      </el-form-item>
      <div class="match_rule_detail">
        <div class="label">匹配规则说明：</div>
        <div class="value">
          <p>1. 估值表名20171128.xls 匹配规则写法：估值表名(\d{8}).xls</p>
          <p>2. 估值表名_2017-11-28.xls 匹配规则写法：估值表名_(\d{4}-\d{2}-\d{2}).xls</p>
          <p>3. 估值表名_2017年11月28日.xls 匹配规则写法：估值表名_(\d{4}年\d{2}月\d{2}日).xls</p>
          <p>4. 2017-11-28_(123456)估值表名.xls 匹配规则写法：\d{4}-\d{2}-\d{2}_\(\d{6}\)估值表名.xls</p>
        </div>
      </div>
    </el-form>
    <div style="text-align: center" class="dialog-footer standard-form">
      <el-button size="small" type="primary" @click="handleSaveAssess">
        提 交
      </el-button>
      <el-button size="small" type="info" plain @click="cancel">取 消</el-button>
    </div>
  </div>
</template>

<script>
import { saveTemplate } from '../scripts/api'
export default {
  name: 'assessTemplate',
  props: {
    tempateOptions: {
      type: Array,
      default: () => []
    },
    curAssessRow: {
      type: Object,
      default: () => {}
    }
  },
  watch: {
    curAssessRow: {
      handler(val) {
        if (val && val.fundCode) {
          this.formData.templateId = Number(val.templateId) || ''
          this.formData.matchingRule = val.matchingRule || ''
        } else {
          this.$message.error('缺少产品代码参数')
        }
      },
      deep: true,
      immediate: true
    }
  },
  data() {
    return {
      // form表单绑定
      formData: {
        templateId: '',
        matchingRule: ''
      },
      // 校验规则
      rules: {
        templateId: [{ required: true, message: '估值文件模板不能为空', trigger: 'blur' }],
        matchingRule: [{ required: true, message: '匹配规则不能为空', trigger: 'blur' }]
      }
    }
  },
  methods: {
    /**
     * @description 取消按钮关闭弹窗
     */
    cancel() {
      this.$emit('closeDialog', 'NO_REFESH')
    },
    /**
     * @description 保存估值模板配置
     */
    handleSaveAssess() {
      this.$refs['formData'].validate(valid => {
        if (valid) {
          const params = Object.assign({}, this.formData)
          params.fundCode = this.curAssessRow.fundCode
          params.templateId = params.templateId.toString()
          saveTemplate(params).then(res => {
            if (res.data.status === 0) {
              this.$message.success(res.data.message || '保存成功')
              this.$emit('closeDialog', 'REFESH')
            } else {
              this.$message.error(res.data.message || '保存失败')
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
.assess-template {
  .template {
    ::v-deep .el-input {
      width: 250px !important;
    }
  }
  .match_rule_detail {
    display: flex;
    align-items: center;
    .label {
      color: #333;
      font-size: 14px;
    }
    .value {
      font-size: 14px;
    }
  }
}
</style>

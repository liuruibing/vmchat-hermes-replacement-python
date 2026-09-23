<template>
  <div class="edit-gzb-xls-config">
    <el-form  ref="formData" :model="formData" :rules="rules" class="standard-form" label-width="auto">
      <el-row>
        <el-col :span="24">
          <el-form-item label="模板名称" prop="templateName">
            <el-input v-model="formData.templateName" placeholder="请输入模板名称" size="medium" >

            </el-input>
          </el-form-item>
        </el-col>

      </el-row>
      <div style="vertical-align: middle;display: inline-block">
        <div class="color-box"></div>
      </div>
      <span class="title-style">配置列表</span>
      <vxe-table
        ref="refsTable"
        :cell-style="{ height: '50px' }"
        :data="tableData"
        auto-resize
        stripe
        sync-resize
        show-overflow="tooltip"
        :sort-config="{ remote: true }"
        style="width: 100%;"
        height="400"
        resizable
      >
        <vxe-table-column field="a1" title="配置字段"  align="left" >

        </vxe-table-column>
        <vxe-table-column field="a2" title="配置信息"  align="left" >
          <template v-slot="{ row }">
            <div v-if="row.a2 === 'beginLine'">
              <el-form-item  label="" prop="beginLine">
                <el-input  v-model="formData.beginLine" size="small"></el-input>
              </el-form-item>
            </div>
            <div v-else-if="row.a2 === 'fkmbm'">
              <el-form-item  prop="fkmbm">
                <el-select v-model="formData.fkmbm"  placeholder="请选择"  size="small" clearable filterable >
                  <el-option key="" label="" value="" />
                  <el-option v-for="letter in letters" :key="letter" :value="letter"  :label="letter">
                    {{ letter }}
                  </el-option>
                </el-select>
              </el-form-item>
            </div>

            <div v-else-if="row.a2 === 'fkmmc'">
              <el-form-item  prop="fkmmc">
                <el-select v-model="formData.fkmmc"  placeholder="请选择"  size="small" clearable filterable >
                  <el-option key="" label="" value="" />
                  <el-option v-for="letter in letters" :key="letter" :value="letter"  :label="letter">
                    {{ letter }}
                  </el-option>
                </el-select>
              </el-form-item>
            </div>

            <div v-else-if="row.a2 === 'fhqjg'">
              <el-form-item  prop="fhqjg">
                <el-select v-model="formData.fhqjg"  placeholder="请选择"  size="small" clearable filterable >
                  <el-option key="" label="" value="" />
                  <el-option v-for="letter in letters" :key="letter" :value="letter"  :label="letter">
                    {{ letter }}
                  </el-option>
                </el-select>
              </el-form-item>
            </div>

            <div v-else-if="row.a2 === 'fhqbz'">
              <el-form-item  prop="fhqbz">
                <el-select v-model="formData.fhqbz"  placeholder="请选择"  size="small" clearable filterable >
                  <el-option key="" label="" value="" />
                  <el-option v-for="letter in letters" :key="letter" :value="letter"  :label="letter">
                    {{ letter }}
                  </el-option>
                </el-select>
              </el-form-item>
            </div>

            <div v-else-if="row.a2 === 'fzqsl'">
              <el-form-item  prop="fzqsl">
                <el-select v-model="formData.fzqsl"  placeholder="请选择"  size="small" clearable filterable >
                  <el-option key="" label="" value="" />
                  <el-option v-for="letter in letters" :key="letter" :value="letter"  :label="letter">
                    {{ letter }}
                  </el-option>
                </el-select>
              </el-form-item>
            </div>

            <div v-else-if="row.a2 === 'fzqcb'">
              <el-form-item  prop="fzqcb">
                <el-select v-model="formData.fzqcb"  placeholder="请选择"  size="small" clearable filterable >
                  <el-option key="" label="" value="" />
                  <el-option v-for="letter in letters" :key="letter" :value="letter"  :label="letter">
                    {{ letter }}
                  </el-option>
                </el-select>
              </el-form-item>
            </div>

            <div v-else-if="row.a2 === 'fzqsz'">
              <el-form-item  prop="fzqsz">
                <el-select v-model="formData.fzqsz"  placeholder="请选择"  size="small" clearable filterable >
                  <el-option key="" label="" value="" />
                  <el-option v-for="letter in letters" :key="letter" :value="letter"  :label="letter">
                    {{ letter }}
                  </el-option>
                </el-select>
              </el-form-item>
            </div>


            <div v-else-if="row.a2 === 'fgzZz'">
              <el-form-item  prop="fgzZz">
                <el-select v-model="formData.fgzZz"  placeholder="请选择"  size="small" clearable filterable >
                  <el-option key="" label="" value="" />
                  <el-option v-for="letter in letters" :key="letter" :value="letter"  :label="letter">
                    {{ letter }}
                  </el-option>
                </el-select>
              </el-form-item>
            </div>

            <div v-else-if="row.a2 === 'fcbJzBl'">
              <el-form-item  prop="fcbJzBl">
                <el-select v-model="formData.fcbJzBl"  placeholder="请选择"  size="small" clearable filterable >
                  <el-option key="" label="" value="" />
                  <el-option v-for="letter in letters" :key="letter" :value="letter"  :label="letter">
                    {{ letter }}
                  </el-option>
                </el-select>
              </el-form-item>
            </div>

            <div v-else-if="row.a2 === 'fszJzBl'">
              <el-form-item  prop="fszJzBl">
                <el-select v-model="formData.fszJzBl"  placeholder="请选择"  size="small" clearable filterable >
                  <el-option key="" label="" value="" />
                  <el-option v-for="letter in letters" :key="letter" :value="letter"  :label="letter">
                    {{ letter }}
                  </el-option>
                </el-select>
              </el-form-item>
            </div>

            <div v-else-if="row.a2 === 'ftpxx'">
              <el-form-item  prop="ftpxx">
                <el-select v-model="formData.ftpxx"  placeholder="请选择"  size="small" clearable filterable >
                  <el-option key="" label="" value="" />
                  <el-option v-for="letter in letters" :key="letter" :value="letter"  :label="letter">
                    {{ letter }}
                  </el-option>
                </el-select>
              </el-form-item>
            </div>

            <div v-else-if="row.a2 === 'fqyxx'">
              <el-form-item  prop="fqyxx">
                <el-select v-model="formData.fqyxx"  placeholder="请选择"  size="small" clearable filterable >
                  <el-option key="" label="" value="" />
                  <el-option v-for="letter in letters" :key="letter" :value="letter"  :label="letter">
                    {{ letter }}
                  </el-option>
                </el-select>
              </el-form-item>
            </div>

            <div v-else-if="row.a2 === 'fbz'">
              <el-form-item  prop="fbz">
                <el-select v-model="formData.fbz"  placeholder="请选择"  size="small" clearable filterable >
                  <el-option key="" label="" value="" />
                  <el-option v-for="letter in letters" :key="letter" :value="letter"  :label="letter">
                    {{ letter }}
                  </el-option>
                </el-select>
              </el-form-item>
            </div>

            <div v-else-if="row.a2 === 'fhl'">
              <el-form-item  prop="fhl">
                <el-select v-model="formData.fhl"  placeholder="请选择"  size="small" clearable filterable >
                  <el-option key="" label="" value="" />
                  <el-option v-for="letter in letters" :key="letter" :value="letter"  :label="letter">
                    {{ letter }}
                  </el-option>
                </el-select>
              </el-form-item>
            </div>

          </template>
        </vxe-table-column>

      </vxe-table>
    </el-form>
    <div style="text-align: center;padding-top: 20px;padding-bottom: 20px;" class="standard-form">
      <el-button size="small" type="primary" @click="handleSaveGzbXlsConfig">提 交</el-button>
      <el-button size="small" type="info" plain @click="cancel">取 消</el-button>
    </div>

  </div>
</template>

<script>
import {insertGzbXlsConfig,updateGzbXlsConfig } from '../scripts/api'


export default {
  name: 'editGzbXlsConfig',
  props: {
    curGzbXlsConfigRow: {
      type: Object,
      default: () => {}
    },
    isEdit: {
      type: Boolean,
      default: false
    },


  },
  watch: {
    curGzbXlsConfigRow: {
      handler(val) {
        if (val) {
            for (const key in this.formData) {
            this.formData[key] = val[key]
            }

        }
      },
      deep: true,
      immediate: true
    }
  },
  mounted() {
    const config = {
      beginLine: '起始行',
      fkmbm: '科目编码',
      fkmmc: '科目名称',
      fhqjg: '行情价格',
      fhqbz: '行情标志',
      fzqsl: '证券数量',
      fzqcb: '成本(本位币)',
      fzqsz: '市值(本位币)',
      fgzZz: '估值增值(本位币)',
      fcbJzBl: '成本占净值比例',
      fszJzBl: '市值占净值比例',
      ftpxx: '停牌信息',
      fqyxx: '权益信息',
      fbz: '币种',
      fhl: '汇率'
    }
    for (var i in config) {
      this.tableData.push({a1: config[i], a2: i,a3:'formData.'+i});
    }


  },

  data() {
    const validateBeginLine = (rule, value, callback) => {
      const regBeginLine = /[^0-9]/
      if (regBeginLine.test(value)) {
        callback(new Error('规范为数字'))
      } else {
        callback()
      }
    }
    return {
      // form表单绑定
      letters: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'], // 26个字母的数组
      formData: {
        fId:'',
        templateName: '',
        beginLine:'',
        fkmbm: '',
        fkmmc: '',
        fhqjg: '',
        fhqbz: '',
        fzqsl: '',
        fzqcb: '',
        fzqsz: '',
        fgzZz: '',
        fcbJzBl: '',
        fszJzBl: '',
        ftpxx: '',
        fqyxx: '',
        fbz: '',
        fhl: ''


      },
      // 表格数据
      tableData: [
      ],
      // 校验规则
      rules: {
        templateName: [
          { required: true, message: '模板名称不能为空', trigger: 'blur' },
        ],
        beginLine: [
          { required: true, message: '起始行不能为空', trigger: 'blur' },
          { validator: validateBeginLine, trigger: 'change' }
        ],

      },

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
     * @description 保存
     */
    handleSaveGzbXlsConfig() {
      this.$refs['formData'].validate((valid) => {
        if (valid) {
          const params = Object.assign({}, this.formData)
          console.log("formData"+JSON.stringify(this.formData));
          params.operation = this.isEdit ? 'update' : 'insert'
          if (params.operation == 'insert') {
            insertGzbXlsConfig(params).then((res) => {
              const { message } = res.data
              if (res.data.status === 200) {
                this.$message({
                  type: 'success',
                  message: '保存成功',
                  customClass: 'message-success'
                })
                this.$emit('closeDialog', 'REFESH')
              } else {
                this.$message({
                  type: 'error',
                  message: message || '保存失败',
                  customClass: 'message-error'
                })
              }
            })
          } else if (params.operation == 'update') {
            updateGzbXlsConfig(params).then((res) => {
              const { message } = res.data
              if (res.data.status === 200) {
                this.$message({
                  type: 'success',
                  message: '保存成功',
                  customClass: 'message-success'
                })
                this.$emit('closeDialog', 'REFESH')
              } else {
                this.$message({
                  type: 'error',
                  message: message || '保存失败',
                  customClass: 'message-error'
                })
              }
            })
          }
        } else {
          return false
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.formItemClass{
  display: flex;
  align-items: center; /* 垂直居中对齐 */
  justify-content: start;
}

</style>

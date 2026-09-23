<template>
  <div class="edit-private-index">
    <el-form  ref="formData" :model="formData" :rules="rules" class="standard-form" label-width="auto">
      <el-row>
        <div v-if="isEdit">
          <el-col :span="24">
          <el-form-item label="指数代码" prop="indexCode" >
            <el-input v-model="formData.indexCode" placeholder="请输入私募指数代码:格式GFSM0001" size="medium" :readonly="isEdit" >
            </el-input>
          </el-form-item>
          </el-col>
        </div>
        <div v-else>
          <el-col :span="20">
            <el-form-item label="指数代码" prop="indexCode" >
              <el-input v-model="formData.indexCode" placeholder="请输入私募指数代码:格式GFSM0001" size="medium" :readonly="isEdit" >
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="4" class="generateButtonClass">

            <el-button type="primary" size="small" @click="generate()" :disabled="isEdit">生成</el-button>

          </el-col>
        </div>

      </el-row>
        <el-row>
        <el-col :span="24">
          <el-form-item label="指数名称" prop="indexName">
            <el-input v-model="formData.indexName" placeholder="请输入私募指数名称" size="medium" clearable>
            </el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">
          <el-form-item label="指数分类" prop="indexClassify">
            <el-select v-model="formData.indexClassify" size="small" clearable filterable placeholder="请选择指数分类">
              <el-option v-for="item in indexClassifyOptions" :key="item.indexClassify" :label="item.indexClassifyName" :value="item.indexClassify" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">
            <el-form-item label="运算规则" prop="indexOperaRuleCode">
              <el-select v-model="formData.indexOperaRuleCode" size="small" clearable filterable placeholder="请选择运算规则">
                <el-option v-for="item in indexOperaRuleOptions" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde"/>
              </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">
          <el-form-item label="基准日期" prop="indexBaseDate">
            <el-date-picker
              v-model="formData.indexBaseDate"
              type="date"
              size="small"
              value-format="yyyy-MM-dd"
              placeholder="请选择基准日期"
              clearable
            >
            </el-date-picker>
          </el-form-item>
        </el-col>
      </el-row>

    </el-form>
    <div style="text-align: center;padding-top: 20px;padding-bottom: 20px;" class="standard-form">
      <el-button size="small" type="primary" @click="handleSave">提 交</el-button>
      <el-button size="small" type="info" plain @click="cancel">取 消</el-button>
    </div>

  </div>
</template>

<script>

import { selectPrivateIndexClassifyList,insertPrivateIndex,updatePrivateIndex } from '../scripts/api'
import { generatePrivateIndexCode,checkPrivateIndexCode, checkPrivateIndexName} from '../scripts/api'
import commonApi from "@/api/common";



export default {
  name: 'editPrivateIndex',
  props: {
    curRow: {
      type: Object,
      default: () => {}
    },
    isEdit: {
      type: Boolean,
      default: false
    },


  },
  watch: {
    curRow: {
      handler(val) {
        if (val) {
            for (const key in this.formData) {
            this.formData[key] = val[key]
            }

        }
      },
      deep: true,
      immediate: true
    },
    'formData.indexName'(newVal, oldVal) {
      if (newVal !== oldVal) {
        this.indexNameChanged = true; // 当值改变时设置标志位为 true
      } else {
        this.indexNameChanged = false; // 重置标志位
      }
    }
  },

  mounted() {
    // 查询表格
    this.getIndexClassifyOptions();
    this.getIndexOperaRuleOptions();
  },


  data() {

    return {
      // form表单绑定

     formData: {
       indexCode:'',
       indexName: '',
       indexClassify:'',
       indexOperaRuleCode: '',
       indexBaseDate: '',
      },
      indexClassifyOptions:[],
      indexOperaRuleOptions:[],
      indexNameChanged: false,
      // 校验规则
      rules: {
        indexCode: [
          { required: true, message: '指数代码不能为空', trigger: 'blur' },
          { validator:this.validatorIndexCode, trigger: 'blur'},
        ],
        indexName: [
          { required: true, message: '指数名称不能为空', trigger: 'blur' },
          { validator:this.validatorIndexName, trigger: 'blur'},
        ],
        indexClassify: [
          { required: true, message: '分类不能为空', trigger: 'blur' },
        ],
        indexOperaRuleCode: [
          { required: true, message: '运算规则不能为空', trigger: 'blur' },
        ],
        indexBaseDate: [
          { required: true, message: '基准日期不能为空', trigger: 'blur' },
        ],
      },

    }
  },
  methods: {
     validatorIndexCode(rule, value, callback){
        if (!value) {
          callback(new Error("请输入指数代码"))
        }
        if(!this.isEdit) {
          let param = { indexCode: this.formData.indexCode }
          checkPrivateIndexCode(param).then((res) => {
            if (res.data.status === 0) {
              callback(new Error('指数代码已经存在'))
            } else {
              callback()
            }
          })
        }else{
          callback()
        }

    },
    validatorIndexName(rule, value, callback){
      if (!value) {
        callback(new Error("请输入指数名称"))
      }
     if(this.indexNameChanged) {
       let param = { indexName: this.formData.indexName }
       checkPrivateIndexName(param).then((res) => {
         if (res.data.status === 0) {
           callback(new Error('指数名称已经存在'))
         } else {
           callback()
         }
       })
     }else{
       callback()
     }


    },

    getIndexOperaRuleOptions(){
      commonApi.edimsSelectType('INDEXOPERARULE').then(res => {
        const { status, data } = res.data
        if (status === 0) {
          this.indexOperaRuleOptions = data
        } else {
          this.indexOperaRuleOptions = []
        }
      })
    },

    getIndexClassifyOptions(){

      selectPrivateIndexClassifyList({}).then(res => {
        let { status, data } = res.data
        if (status === 200) {
          this.indexClassifyOptions = data
        }
      })
    },

    generate(){
      const data = {}
      generatePrivateIndexCode(data).then((res) => {
        console.log(res.data.data.indexCode)
        if (res.data.status === 200) {
          this.formData.indexCode = res.data.data.indexCode
        }
      })
    },


    /**
     * @description 取消按钮关闭弹窗
     */
    cancel() {
      this.$emit('closeDialog', 'NO_REFESH')
    },


    /**
     * @description 保存
     */
    handleSave() {
      this.$refs['formData'].validate((valid) => {
        if (valid) {
          const params = Object.assign({}, this.formData)
          console.log("formData"+JSON.stringify(this.formData));
          params.operation = this.isEdit ? 'update' : 'insert'
          if (params.operation == 'insert') {
            insertPrivateIndex(params).then((res) => {
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
            updatePrivateIndex(params).then((res) => {
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
.generateButtonClass{
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  height: 100%; /* 根据需要设置高度 */
}

</style>

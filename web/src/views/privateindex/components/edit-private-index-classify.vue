<template>
  <div class="editPrivateIndexClassify">
    <el-form  ref="formData" :model="formData" :rules="rules" class="standard-form" label-width="auto">
      <el-row>
        <div v-if="isEdit">
          <el-col :span="24">
          <el-form-item label="分类代码" prop="indexClassify" >
            <el-input v-model="formData.indexClassify" placeholder="请输入分类代码:格式ZSFL0001" size="medium" :readonly="isEdit" >
            </el-input>
          </el-form-item>
          </el-col>
        </div>
        <div v-else>
          <el-col :span="20">
            <el-form-item label="分类代码" prop="indexClassify" >
              <el-input v-model="formData.indexClassify" placeholder="请输入分类代码:格式ZSFL0001" size="medium" :readonly="isEdit" >
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="4" class="generateButtonClass">
            <el-button type="primary" size="small" @click="generateClassifyCode" :disabled="isEdit">生成</el-button>
          </el-col>
        </div>

      </el-row>
        <el-row>
        <el-col :span="24">
          <el-form-item label="分类名称" prop="indexClassifyName">
            <el-input v-model="formData.indexClassifyName" placeholder="请输入私募指数名称" size="medium"  clearable>
            </el-input>
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

import { insertPrivateIndexClassify,updatePrivateIndexClassify } from '../scripts/api'
import { generatePrivateIndexClassifyCode,checkPrivateIndexClassifyCode, checkPrivateIndexClassifyName} from '../scripts/api'




export default {
  name: 'editPrivateIndexClassify',
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

    'formData.indexClassifyName'(newVal, oldVal) {
      if (newVal !== oldVal) {
        this.indexClassifyNameChanged = true; // 当值改变时设置标志位为 true
      } else {
        this.indexClassifyNameChanged = false; // 重置标志位
      }
    },

  },

  mounted() {

  },


  data() {

    return {
      // form表单绑定

     formData: {

       indexClassify:'',
       indexClassifyName:'',

      },

      indexClassifyNameChanged: false,
      // 校验规则
      rules: {
        indexClassify: [
          { required: true, message: '分类代码不能为空', trigger: 'blur' },
          { validator:this.validatorIndexClassifyCode, trigger: 'blur'},
        ],
        indexClassifyName: [
          { required: true, message: '分类名称不能为空', trigger: 'blur' },
          { validator:this.validatorIndexClassifyName, trigger: 'blur'},
        ],

      },

    }
  },
  methods: {
    validatorIndexClassifyCode(rule, value, callback){
        if (!value) {
          callback(new Error("请输入分类代码"))
        }
        if(!this.isEdit) {
          let param = { indexClassify: this.formData.indexClassify }
          checkPrivateIndexClassifyCode(param).then((res) => {
            if (res.data.status === 0) {
              callback(new Error('分类代码已经存在'))
            } else {
              callback()
            }
          })
        }else{
          callback()
        }

    },
    validatorIndexClassifyName(rule, value, callback){
      if (!value) {
        callback(new Error("请输入分类名称"))
      }
     console.log("indexClassifyNameChanged:"+this.indexClassifyNameChanged)
     if(this.indexClassifyNameChanged) {
       let param = { indexClassifyName: this.formData.indexClassifyName }
       checkPrivateIndexClassifyName(param).then((res) => {
         if (res.data.status === 0) {
           callback(new Error('分类名称已经存在'))
         } else {
           callback()
         }
       })
     }else{
       callback()
     }


    },


    generateClassifyCode(){
      const data = {}
      generatePrivateIndexClassifyCode(data).then((res) => {
        if (res.data.status === 200) {
          this.formData.indexClassify = res.data.data.indexClassify
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
            insertPrivateIndexClassify(params).then((res) => {
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
            updatePrivateIndexClassify(params).then((res) => {
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

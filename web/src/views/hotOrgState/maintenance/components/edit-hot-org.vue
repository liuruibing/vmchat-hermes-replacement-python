<template>
  <div class="editHotOrg">
    <el-form  ref="formData" :model="formData" :rules="rules" class="standard-form" label-width="auto">
      <el-row>
        <div>
          <el-col :span="24">
          <el-form-item label="热点机构" prop="regCode" >
<!--            <el-input v-model="formData.regCode" placeholder="请选择热点机构" size="medium">-->
            <div v-if="!isEdit">
            <org-inst-select  ref="orgInstSelectRef"
                             v-model="formData.regCode"
                             :value="formData.regCode"
                             @select-change="handleOrgInstSelectChange"  placeholder="请选择机构"></org-inst-select>
            </div>
            <div v-else>
              <el-input v-model="formData.glrName" placeholder="请选择热点机构" size="medium" :readonly="isEdit"></el-input>
            </div>



          </el-form-item>
          </el-col>
        </div>

      </el-row>
      <el-row>
          <el-col :span="24" class="pic">
            <el-form-item label="小logo图标" prop="smallLogo" title="上传尺寸建议：长：宽=1:1">
              <el-upload
                :show-file-list="false"
                :http-request="(e)=>{httpRequest(e,1)}"
                @on-remove="handleSmallLogoRemove"
                class="avatar-uploader"
                action="#">
                      <span v-if="smallLogo" class="avatar">
                        <el-image
                          :src="smallLogo"
                          style="width: 100px; height: 100px"
                          fit="cover"></el-image>
                        <i class="el-icon-close icon-img" @click.stop="deleteImg(1)"/>
                      </span>
                <i v-else class="el-icon-plus avatar-uploader-icon"></i>
              </el-upload>

            </el-form-item>



          </el-col>

      </el-row>

      <el-row>
        <el-col :span="24" class="pic">
          <el-form-item label="机构logo图标" prop="regLogo" title="上传尺寸建议：长：宽=2.5:1">
            <el-upload
              :show-file-list="false"
              :http-request="(e)=>{httpRequest(e,2)}"
              @on-remove="handleLogoRemove"
              class="avatar-uploader"
              action="#">
                  <span v-if="regLogo" class="avatar">
                    <el-image
                      :src="regLogo"
                      style="width: 100px; height: 100px"
                      fit="cover"></el-image>
                    <i class="el-icon-close icon-img" @click.stop="deleteImg(2)"/>
                  </span>
              <i v-else class="el-icon-plus avatar-uploader-icon"></i>
            </el-upload>
          </el-form-item>

        </el-col>
      </el-row>
        <el-row>
        <el-col :span="12">
          <el-form-item label="状态" prop="leftStatus">
            <el-select v-model="formData.leftStatus" size="medium" clearable filterable placeholder="请选择左侧状态">
              <el-option v-for="item in statusArr" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde"  />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="排序" prop="leftOrder">
            <el-input-number v-model="formData.leftOrder" size="medium" clearable filterable placeholder="请输入左侧排序"></el-input-number>

          </el-form-item>
        </el-col>
      </el-row>

<!--      <el-row>-->
<!--        <el-col :span="12">-->
<!--          <el-form-item label="右侧状态" prop="rightStatus">-->
<!--            <el-select v-model="formData.rightStatus" size="medium" clearable filterable placeholder="请选择右侧状态">-->
<!--              <el-option v-for="item in statusArr" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde"  />-->
<!--            </el-select>-->
<!--          </el-form-item>-->
<!--        </el-col>-->
<!--        <el-col :span="12">-->
<!--          <el-form-item label="右侧排序" prop="rightOrder">-->
<!--            <el-input-number v-model="formData.rightOrder" size="medium" clearable filterable placeholder="请输入右侧排序"></el-input-number>-->
<!--          </el-form-item>-->
<!--        </el-col>-->
<!--      </el-row>-->
      <el-row>
        <el-col :span="24">
          <el-form-item label="机构简介" prop="description">
            <el-input v-model="formData.description" placeholder="请输入机构简介" size="medium" clearable>
            </el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="24">
          <el-form-item label="备注" prop="remark">
            <el-input v-model="formData.remark" placeholder="请输入备注" size="medium" clearable>
            </el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="24">
          <el-form-item label="推送日期" prop="pushDate">
            <el-date-picker
              v-model="formData.pushDate"
              type="date"
              editable
              size="small"
              value-format="yyyy-MM-dd"
              placeholder="选择日期"
            >
            </el-date-picker>
          </el-form-item>
        </el-col>
      </el-row>

    </el-form>
    <div style="text-align: center;padding-top: 20px;padding-bottom: 20px;" class="standard-form">
      <el-button :loading="saveLoading" size="small" type="primary" @click="handleSave">提 交</el-button>
      <el-button size="small" type="info" plain @click="cancel">取 消</el-button>
    </div>

  </div>
</template>

<script>

import { insertHotReg,updateHotReg } from '../scripts/api'
import { STATUS_LIST } from '../scripts/constants'
import lodash from 'lodash'
import commonApi from '@/api/common'
import  OrgInstSelect  from './OrgInstSelect.vue'


export default {
  name: 'editHotOrg',
  components: {
    OrgInstSelect
  },
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
              if(val[key] && val[key]!== undefined){
                this.formData[key] = val[key]
              }

            }


        }
      },
      deep: true,
      immediate: true
    },
  },

  mounted() {
    if(this.formData.smallLogoFileId){
      commonApi.manageS3SelectFile(this.formData.smallLogoFileId).then(res=>{

        let blob = new Blob ([res.data],{type:'application/octet-stream'})
        this.smallLogo=URL.createObjectURL(blob)
        this.formData.smallLogo=this.smallLogo
      })

    }

    if(this.formData.logoFileId){

      commonApi.manageS3SelectFile(this.formData.logoFileId).then(res => {
        let blob = new Blob ([res.data],{type:'application/octet-stream'})
        this.regLogo=URL.createObjectURL(blob)
        this.formData.regLogo=this.regLogo
      })

    }
  },
  beforeDestroy() {
    if (this.formData.smallLogoFileId) {
      URL.revokeObjectURL(this.smallLogo); // 清理URL对象
    }
    if (this.formData.logoFileId) {
      URL.revokeObjectURL(this.regLogo); // 清理URL对象
    }

  },

  data() {

    return {
      // form表单绑定
      visible:true,
      selectedProduct1:null,
     formData: {

       id:0,
       regCode:'',
       glrName:'',
       leftStatus: '1',
       leftOrder:100,
       rightStatus: '1',
       rightOrder:50,
       pushDate:'',
       description:'',//热点机构简介
       remark:'',//备注
       smallLogo:'',
       regLogo:'',
       fileIds: [], //需要删除的数组对象
       smallLogoFileId:'',
       logoFileId:'',

      },
      smallLogo:'',
      regLogo:'',
      saveLoading: false,
      statusArr:STATUS_LIST,
      // 校验规则
      rules: {
        regCode: [
          { required: true, message: '热点机构不能为空', trigger: 'blur' },
        ],
        smallLogo: [
          { required: true, message: '小logo图标不能为空', trigger: 'change' },
        ],
        regLogo: [
          { required: true, message: '机构logo图标不能为空', trigger: 'change' },
        ],
        leftStatus: [
          { required: true, message: '左侧状态不能为空', trigger: 'blur' },
        ],
        rightStatus: [
          { required: true, message: '右侧状态不能为空', trigger: 'blur' },
        ],

      },

    }
  },
  methods: {
   // 产品选择变更回调
    handleOrgInstSelectChange(row) {
      this.formData.regCode=row.regCode
     // console.log('产品选择变更：', row.regCode)
     // console.log('this.formData.regCode：', this.formData.regCode)
    },


    /**
     * @description 取消按钮关闭弹窗
     */
    cancel() {
      this.$emit('closeDialog', 'NO_REFESH')
    },


    /**
     * @Description: 小logo图标的remove事件
     * @author Liu Rui Bing
     * @date 2024/7/11
     */
    handleSmallLogoRemove(val) {
      // 如果是编辑模式的情况下触发了remove事件
      if (this.dialogStatus === 'EDIT') {
        this.formData.smallLogo = ''
        let findObj = this.formData.fileIds.find(item => item === this.formData.smallLogoFileId)
        if (!findObj) {
          this.formData.fileIds.push(this.formData.smallLogoFileId) // 摘要图片 存在 删除的逻辑，需要把fid放到数组里面去
        }
      }
    },



    /**
     * @Description: 机构logo图标的remove事件
     * @author Liu Rui Bing
     * @date 2024/7/11
     */
    handleLogoRemove(val) {
      // 如果是编辑模式的情况下触发了remove事件
      if (this.dialogStatus === 'EDIT') {
        this.formData.regLogo = ''
        let findObj = this.formData.fileIds.find(item => item === this.formData.logoFileId)
        if (!findObj) {
          this.formData.fileIds.push(this.formData.logoFileId) // 摘要图片 存在 删除的逻辑，需要把fid放到数组里面去
        }
      }
    },

    beforeAvatarUpload(file, num) {
      const isJpeg = file.type === 'image/jpeg' || file.type === 'image/png' || file.type === 'image/jpg'
      const isLt50M = file.size / 1024 / 1024 < 50
      if (!isJpeg) {
        this.$message.error('上传图片只能是 JPG、PNG、JPEG 格式!')
        return false
      }
      if (!isLt50M) {
        this.$message.error('上传图片大小不能超过 50MB!')
        return false
      }
      if (num === 1 || num === 2) {
        return isJpeg && isLt50M
      }

      return isJpeg && isLt50M
    },
    httpRequest(param, num){
      if (!this.beforeAvatarUpload(param.file, num)) {
        return
      }
      if (num === 1) {
        this.formData.smallLogo = param.file
        //console.log(this.formEditQuery.pic2, 'file')

        const reader = new FileReader()
        let fileResult = ''
        reader.readAsDataURL(param.file)
        // 开始转
        reader.onload = () => {
          fileResult = reader.result
          this.smallLogo = fileResult
        }
        if (this.dialogStatus === 'EDIT') {
          const index = this.formData.fileIds.indexOf(this.formData.smallLogoFileId);
          if (index > -1) {
            this.formData.fileIds.splice(index, 1);
          }

        }
      }
      if (num === 2) {
        this.formData.regLogo = param.file
        //console.log(this.formEditQuery.pic2, 'file')
        const reader = new FileReader()
        let fileResult = ''
        reader.readAsDataURL(param.file)
        // 开始转
        reader.onload = () => {
          fileResult = reader.result
          this.regLogo = fileResult
        }
        if (this.dialogStatus === 'EDIT') {
          const index = this.formData.fileIds.indexOf(this.formData.logoFileId);
          if (index > -1) {
            this.formData.fileIds.splice(index, 1);
          }

        }
      }
    },

    deleteImg(num) {
      // 小logo图片 处理方法
      if (num === 1) {
        this.smallLogo = ''
        if (this.dialogStatus === 'EDIT') {
          let findObj = this.formData.fileIds.find(item => item === this.formData.smallLogoFileId)
          if (!findObj) {
            this.formData.fileIds.push(this.formData.smallLogoFileId) // 摘要图片 存在 删除的逻辑，需要把fid放到数组里面去
          }
        }
        this.formData.smallLogo = ''
      }
      if (num === 2) {
        this.regLogo = ''
        if (this.dialogStatus === 'EDIT') {
          let findObj = this.formData.fileIds.find(item => item === this.formData.logoFileId)
          if (!findObj) {
            this.formData.fileIds.push(this.formData.logoFileId) // 摘要图片 存在 删除的逻辑，需要把fid放到数组里面去
          }
        }
        this.formData.regLogo = ''
      }
    },

    /**
     * @description 保存
     */
    handleSave() {
      this.$refs['formData'].validate((valid) => {
        if (valid) {
          this.saveLoading = true
          const params = lodash.cloneDeep(this.formData)
         // params.fileIds = params.fileIds.toString()
          console.log("formData"+JSON.stringify(this.formData));
          params.operation = this.isEdit ? 'update' : 'insert'
          const id=this.formData.id==='undefined'?0:this.formData.id
          params.id=id

          const formData = new FormData()
          for (const i in params) {
            formData.append(i, params[i])
          }
          if (params.operation == 'insert') {
            insertHotReg(formData).then((res) => {
              const { message } = res.data
              if (res.data.status === 200) {
                this.$message({
                  type: 'success',
                  message: '保存成功',
                  customClass: 'message-success'
                })
                this.saveLoading = false
                this.$emit('closeDialog', 'REFESH')
              } else {
                this.saveLoading = false
                this.$message({
                  type: 'error',
                  message: message || '保存失败',
                  customClass: 'message-error'
                })
              }
            })
          } else if (params.operation == 'update') {
            updateHotReg(formData).then((res) => {
              const { message } = res.data
              if (res.data.status === 200) {
                this.$message({
                  type: 'success',
                  message: '保存成功',
                  customClass: 'message-success'
                })
                this.saveLoading = false
                this.$emit('closeDialog', 'REFESH')
              } else {
                this.saveLoading = false
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
.pic {
  position: relative;

  .notes {
    position: absolute;
    bottom: 30px;
    font-weight: 500;
    color: #F56C6C;
    font-size: 14px;
    line-height: 18px;
    padding-top: 4px;

    div {
      width: 37px;
      display: inline-block;
    }
  }
}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  line-height: 100px;
  text-align: center;
}

.avatar {
  width: 100px;
  height: 100px;
  display: block;
  position: relative;

  .icon-img {
    display: none;
    position: absolute;
    top: 0px;
    right: 0;
    font-size: 20px;
    margin-bottom: 15px;
    color: #e03d3e;
    -webkit-transition: color .15s linear;
    transition: color .15s linear;
    z-index: 100;
  }

  &:hover {
    img {
      opacity: 0.5;
    }

    .icon-img {
      display: block;
    }
  }

}

</style>

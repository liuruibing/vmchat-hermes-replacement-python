<template>
  <div class="importPrivateIndexComponent">
    <div>
      <div class="page-model-title">
        <div class="title-icon">
          <div class="color-box"></div>
        </div>
        <div class="title-txt">
          上传私募指数成分文件
        </div>
      </div>
      <div class="standard-form-margin">
        <div class="inner-margin">
          <el-form ref="formInline" class="standard-form" :inline="true" >
            <el-row>
              <el-col :span="12">
                <el-form-item label="Excel文件" >
                  <el-upload
                    ref="uploadImportPrivateIndexComponent"
                    accept=".xls,.xlsx"
                    :before-upload="beforeUpload"
                    :on-change="handleFileChange"
                    :auto-upload="false"
                    action="#"
                    :multiple="false"
                    :file-list="privateComponentFileList"
                    class="net-upload">
                          <span class="standard-form">
                            <el-button slot="trigger" plain type="primary" size="small" title="请上传文件Excel文件">选取文件</el-button>

                          </span>
                  </el-upload>
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item>
                  <el-button  :loading="uploadLoading"  :disabled="uploadLoading" plain class="view" style="margin-left: 10px" size="small" type="primary" @click.prevent="handleClick($event)"  @click="submitUpload">
                    {{ uploadLoading ? '上传中...' : '提交' }}
                  </el-button>
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item>
                  <el-button   plain class="view" style="margin-left: 10px" size="small" type="primary"   @click="downLoadTemplate()">
                    导入模板下载
                  </el-button>
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import { uploadPrivateIndexComponentFile } from '../scripts/api'
import { downLoadFileByUrl } from '@/utils'




export default {
  name: 'importPrivateIndexComponent',
  data() {

    return {
      // form表单绑定
      privateComponentFileList:[],
      uploadLoading:false,

    }
  },
  methods: {


    beforeUpload(file) {
      const isExcel = file.type === 'xlsx' || file.type === 'xls';
      if (!isExcel) {
        this.$message.error('只能上传Excel文件!');
        return false;
      }
      return true;
    },


    handleFileChange(file, fileList) {

      if (fileList.length > 0) {
        this.privateComponentFileList = [fileList[fileList.length - 1]]
      }else{
        this.privateComponentFileList = fileList[0]
      }

    },

    handleClick(event) {
      event.target.blur()
      if (event.target.nodeName === 'SPAN') {
        event.target.parentNode.blur()
      }
    },

    downLoadTemplate(){

      const fileName = '私募指数成分导入模板.xlsx'
      const url = 'api/gfprivateindexcomponent/downLoadImportExample'
      const params = {  }
      downLoadFileByUrl(url, params, fileName, this)



    },

    async submitUpload(){
      this.uploadLoading = true
      // let isCloseDialog = 0
      const formData = new FormData()
      this.privateComponentFileList.forEach(file => {
        formData.append('uploadFile', file.raw); //
      });

      await this.uploadPromise(formData)
      this.uploadLoading = false
      //this.handleSearchTable()
      this.$refs.uploadImportPrivateIndexComponent.clearFiles(); // 清除文件列表

    },

    uploadPromise(params) {
      return new Promise((resolve, reject) => {
        uploadPrivateIndexComponentFile(params).then((res) => {
          if (res.data.status === 200) {
            this.$message({
              type: 'success',
              message: '上传成功',
              customClass: 'message-success'
            })
            resolve('success')
          } else {
            this.$message({
              type: 'error',
              message:"上传异常！请联系管理人员!"+ res.data.message,
              customClass: 'message-error'
            })
            resolve('error')
          }
        })
      })
    },
    /**
     * @description 取消按钮关闭弹窗
     */
    cancel() {
      this.$emit('closeDialog', 'NO_REFESH')
    }



  }
}
</script>

<style lang="scss" scoped>
::v-deep  .upload-content{
  border-color: #e19c5d;
}
::v-deep  .page-model-title {
  height: 52px;
  padding: 15px 0px 15px 10px;
}

</style>

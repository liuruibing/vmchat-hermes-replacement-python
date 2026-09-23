<!--
 * @Description: 
 * @Author: 
 * @Date: 2023-02-06 10:15:13
 * @LastEditors: zhaojirui zhaojirui@datadriver.com.cn
 * @LastEditTime: 2023-03-10 14:59:24
-->
<template>
  <div class="detail-form">
    <el-form ref="elForm" :model="formData" label-width="auto" class="standard-form" style="margin: 0 auto" disabled>
      <el-form-item :label="fundLabel" prop="">
        <el-input v-model="formData.fundName" size="small"></el-input>
      </el-form-item>
      <el-form-item label="需求类型" prop="">
        <el-select v-model="formData.dataType" placeholder="请选择" size="small">
          <el-option v-for="item in dataTypeOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="说明" prop="">
        <el-input type="textarea" v-model="formData.remark" placeholder=""></el-input>
      </el-form-item>
      <el-form-item label="需求附件" prop="">
        <el-upload class="upload-custom" action="" multiple disabled :file-list="fileList1">
          <div slot="file" slot-scope="{ file }" class="download-acitve" @click="needManageDownloadUrl(file)">
            <span>{{ file.name }}</span>
            <i class="el-icon-download" />
          </div>
        </el-upload>
      </el-form-item>
      <el-form-item label="申请日期" prop="">
        <el-input v-model="formData.date" size="small"></el-input>
      </el-form-item>
      <el-form-item label="申请人" prop="">
        <el-input v-model="formData.sqr" size="small"></el-input>
      </el-form-item>
      <el-form-item label="处理状态" prop="">
        <el-input v-model="formData.status" size="small"></el-input>
      </el-form-item>
      <el-form-item label="处理结果" prop="">
        <el-input type="textarea" v-model="formData.cljg" placeholder=""></el-input>
      </el-form-item>
      <el-form-item label="结果附件" prop="">
        <el-upload class="upload-custom" action="" multiple disabled :file-list="fileList2">
          <div slot="file" slot-scope="{ file }" class="download-acitve" @click="needManageDownloadUrl(file)">
            <span>{{ file.name }}</span>
            <i class="el-icon-download" />
          </div>
        </el-upload>
      </el-form-item>
    </el-form>
    <!-- <div style="text-align: center">
      <el-button size="small" type="">取 消</el-button>
      <el-button size="small" type="primary">提 交</el-button>
    </div> -->
  </div>
</template>

<script>
import accessPoolApi from '@/api/AccessPoolProcess/accessPool'
// import {downLoadFileByUrl} from '@/api/common'
import commonFun from '@/filters/common'
export default {
  name: '',
  components: {},
  data() {
    return {
      fundLabel: '机构/产品名称',
      formData: {
        fundName: '',
        dataType: '',
        remark: '',
        date: '',
        sqr: '',
        status: '',
        cljg: ''
      },
      dataTypeOptions: [
        { label: '产品信息验证', value: '1' },
        { label: '产品数据质检', value: '2' },
        { label: '机构尽调', value: '3' }
      ],
      fileList1: [],
      fileList2: []
    }
  },
  mounted() {},
  methods: {
    init(params) {
      const data = JSON.parse(JSON.stringify(params))
      if (data.type === '1' || data.type === '2') {
        this.fundLabel = '产品名称'
      } else if (data.type === '3') {
        this.fundLabel = '机构名称'
      }
      this.formData.fundName = data.fundName
      this.formData.dataType = data.type
      this.formData.remark = data.state
      this.formData.date = data.applyDate
      this.formData.sqr = data.userName
      if (data.status == '1') {
        data.status = '待提交'
      } else if (data.status == '2') {
        data.status = '处理中'
      } else if (data.status == '3') {
        data.status = '处理完毕'
      }
      this.formData.status = data.status
      this.formData.cljg = data.result
      this.getFileList(data.id, 1)
      this.getFileList(data.id, 2)
    },
    //获取文件列表（1申请文件、2反馈文件）
    getFileList(id, type) {
      accessPoolApi
        .needManageSelectEdit({
          fileType: type,
          id: id
        })
        .then((res) => {
          let { status, data, statusText } = res
          if (status === 200) {
            data.data.forEach((element) => {
              element.name = element.fileName
            })
            if (type == 1) {
              this.fileList1 = data.data
            } else if (type == 2) {
              this.fileList2 = data.data
            }
          }
        })
        .catch(() => {})
    },
    needManageDownloadUrl(file) {
      const params = {
        id: file.id || '',
        token: this.$store.getters.token
      }
      const action = this.$store.state.setting.baseApi + '/api/standArd/needManage/download'
      commonFun.formDownloadFile(params, action, 'post')
    }
  }
}
</script>
<style lang="scss">
.detail-form {
  .upload-custom {
    .el-upload--text {
      display: none;
    }
    .download-acitve {
      cursor: pointer;
      padding-left: 10px;
    }
    .download-acitve:hover {
      color: #319ef1;
    }
  }
}
</style>

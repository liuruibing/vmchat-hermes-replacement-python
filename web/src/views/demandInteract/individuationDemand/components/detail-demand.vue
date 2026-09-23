<template>
  <div class="detail-form">
    <el-form ref="elForm" :model="formData" label-width="100px" class="standard-form" style="margin: 0 auto" disabled>
      <el-form-item label="产品代码">
        <el-input v-model="formData.fcode" size="small"></el-input>
      </el-form-item>
      <el-form-item label="产品名称">
        <el-input v-model="formData.fname" size="small"></el-input>
      </el-form-item>
      <el-form-item label="需求标题">
        <el-input v-model="formData.fundName" size="small"></el-input>
      </el-form-item>
      <el-form-item label="需求内容">
        <el-input v-model="formData.state" type="textarea"></el-input>
      </el-form-item>
      <el-form-item label="申请日期">
        <el-input v-model="formData.applyDate" size="small"></el-input>
      </el-form-item>
      <el-form-item label="申请人">
        <el-input v-model="formData.userName" size="small"></el-input>
      </el-form-item>
      <el-form-item label="处理状态">
        <el-input v-model="formData.status" size="small"></el-input>
      </el-form-item>
      <el-form-item label="需求附件">
        <el-upload class="upload-custom" action="" multiple disabled :file-list="fileList">
          <div slot="file" slot-scope="{ file }" class="download-acitve" @click="handleDownload(file)">
            <span>{{ file.fileName }}</span>
            <i class="el-icon-download" />
          </div>
        </el-upload>
      </el-form-item>
      <el-form-item label="处理结果">
        <el-input type="textarea" v-model="formData.result" placeholder=""></el-input>
      </el-form-item>
      <el-form-item label="结果附件">
        <el-upload class="upload-custom" action="" multiple disabled :file-list="fileListResult">
          <div slot="file" slot-scope="{ file }" class="download-acitve" @click="handleDownload(file)">
            <span>{{ file.fileName }}</span>
            <i class="el-icon-download" />
          </div>
        </el-upload>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { getUplodFile } from '../scripts/api'
import commonFun from '@/filters/common'
export default {
  name: 'detailDemand',
  data() {
    return {
      formData: {
        fcode: '',
        fname: '',
        fundName: '',
        state: '',
        applyDate: '',
        userName: '',
        status: '',
        result: ''
      },
      fileList: [],
      fileListResult: []
    }
  },
  props: {
    curDemandRow: {
      type: Object,
      default: () => {}
    }
  },
  watch: {
    curDemandRow: {
      handler(val) {
        if (Object.keys(val).length > 0) {
          for (const key in this.formData) {
            this.formData[key] = val[key] || ''
          }
          this.getApplyFile(val)
          this.getResultFile(val)
        } else {
          for (const key in this.formData) {
            this.formData[key] = ''
          }
          this.fileList = []
          this.fileListResult = []
        }
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    /**
     * @description 需求文件列表获取
     */
    getApplyFile(val) {
      const params = {}
      params.id = val.id
      params.fileType = 1
      getUplodFile(params).then((res) => {
        if (res.data.status === 0) {
          this.fileList = res.data.data || []
        } else {
          this.$message.error(res.data.message || '需求附件获取失败')
        }
      })
    },
    /**
     * @description 结果文件列表获取
     */
    getResultFile(val) {
      const params = {}
      params.id = val.id
      params.fileType = 2
      getUplodFile(params).then((res) => {
        if (res.data.status === 0) {
          this.fileListResult = res.data.data || []
        } else {
          this.$message.error(res.data.message || '结果附件获取失败')
        }
      })
    },
    /**
     * @description 下载文件
     */
    handleDownload(file) {
      const params = {
        id: file.id || '',
        token: this.$store.getters.token
      }
      console.log(params)
      const action = this.$store.state.setting.baseApi + '/api/standArd/indivduation/download'
      commonFun.formDownloadFile(params, action, 'post')
    }
  }
}
</script>
<style lang="scss" scoped>
.detail-form {
  ::v-deep .upload-custom {
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

<template>
  <div class="examine-dialog">
    <el-row class="search-content mb10">
      <el-form ref="formExamineQuery" class="standard-form" :inline="true" :model="formExamineQuery" :rules="rules" label-width="auto">
        <el-row>
          <el-form-item label="" prop="status">
            <el-select v-model="formExamineQuery.status" placeholder="审批结果" size="small" clearable>
              <el-option v-for="item in statusOptions" :key="item.DIM_CDE" :label="item.DIM_NME" :value="item.DIM_CDE" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <div class="btn-style">
              <el-upload
                ref="upload"
                :on-change="handleChange"
                :file-list="fileList"
                :show-file-list="false"
                :auto-upload="false"
                action="#"
                multiple
                accept=".txt, .doc, .docx, .xls, .pptx"
                class="upload-demo"
              >
                <el-button slot="trigger" type="primary" size="small">选取文件</el-button>
                <el-button class="view" style="margin-left: 10px" size="small" type="primary" @click.prevent="handleClick($event)" @click="submitUpload">上传</el-button>
              </el-upload>
            </div>
          </el-form-item>
        </el-row>
      </el-form>
    </el-row>
    <div id="standard-table">
      <vxe-table ref="multipleTable" :data="tableData" auto-resize stripe="" show-overflow="tooltip" style="width: 100%">
        <vxe-table-column label="文件名称" show-overflow-tooltip field="name" header-align="center" align="center"></vxe-table-column>
        <vxe-table-column label="大小" field="size" header-align="center" align="center"></vxe-table-column>
        <vxe-table-column field="status" label="状态" header-align="center" align="center">
          <template slot-scope="scope">
            <span v-if="scope.row.status == 'ready'">等待上传</span>
            <span v-else-if="scope.row.status == 'success'" style="color: green">上传成功</span>
            <span v-else style="color: red">上传失败</span>
          </template>
        </vxe-table-column>
        <vxe-table-column label="操作" align="center" header-align="center">
          <template slot-scope="scope">
            <span class="table-operation">
              <el-button v-if="scope.row.status == 'ready'" plain size="small" type="info" @click="handleDelete(scope.row)">删除</el-button>
            </span>
          </template>
        </vxe-table-column>
      </vxe-table>
    </div>

    <span slot="footer">
      <el-row :gutter="20" style="margin-top: 10px">
        <el-col :span="20" :offset="11">
          <span class="standard-form">
            <el-button type="primary" size="small" @click="saveExamine('formExamineQuery')">保 存</el-button>
          </span>
        </el-col>
      </el-row>
    </span>
  </div>
</template>
<script>
import { EXAMINE_RESULT_OPTIONS } from '../scripts/constant'
import { uploadFile, saveExamine } from '../scripts/api'
export default {
  name: 'ExamineDialog',
  props: {
    currentFund: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      formExamineQuery: {
        status: ''
      },
      statusOptions: EXAMINE_RESULT_OPTIONS,
      fileList: [],
      tableData: [],
      rules: {
        status: [{ required: true, message: '请选择审核结果', trigger: 'blur' }]
      }
    }
  },
  methods: {
    handleChange(file, fileList) {
      // 限制文件上传后缀
      const fileExtList = ['doc', 'docx', 'xls', 'xlsx', 'pdf', 'ppt', 'pptx', 'txt', 'jpeg', 'png', 'JPEG', 'PNG']
      const fileExtName = file.name.substring(file.name.lastIndexOf('.') + 1)
      if (!fileExtList.includes(fileExtName)) {
        this.$message({
          type: 'warning',
          message: '上传文件类型为：doc、docx、xls、xlsx、pdf、ppt、 pptx、 jpeg、png',
          customClass: 'message-warning'
        })
        return
      }
      // 限制文件上传大小
      const fileSize = Number(file.size / 1024 / 1024)
      if (fileSize > 50) {
        this.$message({
          type: 'warning',
          message: '单个文件大小不超过50M',
          customClass: 'message-warning'
        })
        return
      }
      if (file.status === 'ready') {
        const obj = {
          name: file.name,
          size: (file.size / 1024).toFixed(2) + 'KB',
          status: file.status,
          uid: file.uid,
          raw: file.raw
        }
        this.tableData.push(obj)
      }
      this.fileList = fileList
    },
    handleClick(event) {
      event.target.blur()
      if (event.target.nodeName === 'SPAN') {
        event.target.parentNode.blur()
      }
    },
    handleDelete(row) {
      for (let i = 0; i < this.fileList.length; i++) {
        if (this.fileList[i].uid === row.uid) {
          this.fileList.splice(i, 1)
          break
        }
      }
      for (let i = 0; i < this.tableData.length; i++) {
        if (this.tableData[i].uid === row.uid) {
          this.tableData.splice(i, 1)
          break
        }
      }
    },
    async submitUpload() {
      for (let i = 0; i < this.tableData.length; i++) {
        if (this.tableData[i].status !== 'ready') {
          continue
        }
        const formData = new FormData()
        formData.append('fundCode', this.currentFund.fundCode)
        formData.append('type', '2')
        formData.append('fid', this.currentFund.fid)
        formData.append('file', this.tableData[i].raw)
        const result = await this.uploadPromise(formData)
        this.tableData[i].status = result
        if (result === 'error') return
      }
    },
    uploadPromise(params) {
      return new Promise((resolve, reject) => {
        uploadFile(params).then((res) => {
          if (res.data.status === 0) {
            this.$message({
              type: 'success',
              message: '上传成功',
              customClass: 'message-success'
            })
            resolve('success')
          } else {
            this.$message({
              type: 'error',
              message: '上传失败',
              customClass: 'message-error'
            })
            resolve('error')
          }
        })
      })
    },
    async saveExamine(formName) {
      this.$refs[formName].validate(async (valid) => {
        try {
          if (valid) {
            const data = {
              fid: this.currentFund.fid || '',
              status: this.formExamineQuery.status || ''
            }
            const res = await saveExamine(data)
            if (res.data.status === 0) {
              this.$message({
                type: 'success',
                message: '审批成功',
                customClass: 'message-success'
              })
              this.$emit('closeExamine', 'refesh')
            }
          } else {
            return false
          }
        } catch (e) {
          this.$message({
            type: 'error',
            message: '审批失败',
            customClass: 'message-error'
          })
        }
      })
    }
  }
}
</script>
<style lang="scss" scoped>
.btn-style {
  text-align: right;
  margin-bottom: 5px;
}
::v-deep .vxe-body--row.row--stripe {
  background-color: #f9fafe !important;
}
</style>

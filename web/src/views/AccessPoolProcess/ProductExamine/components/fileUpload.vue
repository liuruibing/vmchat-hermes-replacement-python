<template>
  <div class="file-upload">
    <el-row class="search-content" type="flex" justify="start" style="width: 100%; margin: 5px 0; border-bottom: 1px solid #f2f3f5">
      <el-upload ref="upload" :on-change="handleChange" :file-list="fileList" :show-file-list="false" :auto-upload="false" action="#" multiple class="upload-demo">
        <span class="standard-form">
          <el-button slot="trigger" plain type="primary" size="small">选取文件</el-button>
          <el-button :loading="uploadLoading" plain class="view" style="margin-left: 10px" size="small" type="primary" @click.prevent="handleClick($event)" @click="submitUpload">
            上传
          </el-button>
        </span>
      </el-upload>
    </el-row>
    <div id="standard-table">
      <vxe-table ref="multipleTable" auto-resize stripe="" show-overflow="tooltip" style="width: 100%" :data="tableData">
        <vxe-table-column field="name" label="文件名" show-overflow-tooltip header-align="center" min-width="180" align="center" />
        <vxe-table-column field="size" label="大小" header-align="center" min-width="180" align="center" />
        <vxe-table-column field="status" label="状态" header-align="center" min-width="180" align="center">
          <template slot-scope="scope">
            <span v-if="scope.row.status == 'ready'">等待上传</span>
            <span v-else-if="scope.row.status == 'success'" style="color: green">上传成功</span>
            <span v-else style="color: red">上传失败</span>
          </template>
        </vxe-table-column>
        <vxe-table-column label="操作" align="center" header-align="center" min-width="180">
          <template slot-scope="scope">
            <span class="table-operation">
              <el-button v-if="scope.row.status == 'ready'" plain size="small" type="info" @click="handleDelete(scope.row)">删除</el-button>
            </span>
          </template>
        </vxe-table-column>
      </vxe-table>
    </div>
  </div>
</template>
<script>
import { uploadFile } from '../scripts/api'
export default {
  name: 'FileUpolad',
  props: {
    currentFund: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      uploadLoading: false,
      fileList: [],
      tableData: []
    }
  },
  methods: {
    async submitUpload() {
      this.uploadLoading = true
      let isCloseDialog = 0
      for (let i = 0; i < this.tableData.length; i++) {
        if (this.tableData[i].status !== 'ready') {
          continue
        }
        const formData = new FormData()
        formData.append('fundCode', this.currentFund.fundCode)
        formData.append('type', '1')
        formData.append('fid', this.currentFund.fid)
        formData.append('file', this.tableData[i].raw)
        const result = await this.uploadPromise(formData)
        this.tableData[i].status = result
        if (result === 'error') {
          isCloseDialog += 1
        }
      }
      this.uploadLoading = false
      this.$emit('closeUpload', 'refesh')
    },
    handleClick(event) {
      event.target.blur()
      if (event.target.nodeName === 'SPAN') {
        event.target.parentNode.blur()
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

    handleChange(file, fileList) {
      // 限制文件上传后缀
      const fileExtList = ['doc', 'docx', 'xls', 'xlsx', 'pdf', 'ppt', 'pptx', 'txt', 'jpeg', 'png', 'JPEG', 'PNG', 'rtf']
      const fileExtName = file.name.substring(file.name.lastIndexOf('.') + 1)
      if (!fileExtList.includes(fileExtName)) {
        this.$message({
          type: 'warning',
          message: '上传文件类型为：doc、docx、xls、xlsx、pdf、ppt、 pptx、 jpeg、png、rtf',
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
    }
  }
}
</script>
<style lang="scss" scoped>
@import '../styles/index';
::v-deep .vxe-body--row.row--stripe {
  background-color: #f9fafe !important;
}
</style>

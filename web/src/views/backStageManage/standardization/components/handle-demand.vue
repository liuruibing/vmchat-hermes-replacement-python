<template>
  <div class="detail-form">
    <el-form ref="formData" :model="formData" :rules="rules" label-width="100px" style="margin: 0 auto">
      <el-form-item label="结果附件">
        <el-upload
          ref="upload"
          :auto-upload="false"
          :file-list="fileList"
          :headers="{}"
          :on-change="handleChange"
          :on-remove="handleRemove"
          action=""
          class="upload-demo"
          multiple
          name="file"
        >
          <el-button size="small" type="primary">选择文件</el-button>
        </el-upload>
      </el-form-item>
      <el-form-item label="处理结果" prop="result">
        <el-input type="textarea" v-model="formData.result" placeholder=""></el-input>
      </el-form-item>
    </el-form>
    <div style="text-align: center">
      <el-button size="small" type="" @click="cancel">取 消</el-button>
      <el-button size="small" type="primary" @click="handleSave">
        保 存
      </el-button>
    </div>
  </div>
</template>

<script>
import { handleDispose, getUplodFile } from '../scripts/api'
export default {
  name: 'handleDemandStand',
  props: {
    curHandleRow: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      formData: {
        result: ''
      },
      fileList: [],
      // 校验规则
      rules: {
        result: [{ type: 'string', required: true, message: '处理结果不能为空', trigger: 'blur' }]
      },
      deleteFileId: []
    }
  },
  watch: {
    curHandleRow: {
      handler(val) {
        if (val) {
          this.formData.result = val.result || ''
          this.getResultFile(val)
        }
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    /**
     * @description 结果文件列表获取
     */
    getResultFile(val) {
      const params = {}
      params.id = val.id
      params.fileType = 2
      getUplodFile(params).then(res => {
        if (res.data.status === 0) {
          this.fileList = res.data.data || []
          if (this.fileList && this.fileList.length) {
            this.fileList = this.fileList.map(item => {
              return {
                ...item,
                name: item.fileName
              }
            })
          }
        } else {
          this.$message.error(res.data.message || '结果附件获取失败')
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
     * @description 保存新增需求
     */
    handleSave() {
      this.$refs['formData'].validate(valid => {
        if (valid) {
          const formData = new FormData()
          for (const key in this.formData) {
            formData.append(key, this.formData[key])
          }
          this.fileList.forEach(item => {
            if (item.raw) {
              formData.append('file', item.raw)
            }
          })
          formData.append('deleteFileId', this.deleteFileId)
          formData.append('id', this.curHandleRow.id)
          handleDispose(formData).then(res => {
            if (res.data.status === 0) {
              this.$message.success(res.data.message || '处理成功')
              this.$emit('closeDialog', 'REFESH')
            } else {
              this.$message.error(res.data.message || '处理失败')
            }
          })
        } else {
          return false
        }
      })
    },
    /**
     * @description 监听文件变化
     */
    handleChange(file, fileList) {
      this.fileList = []
      const testmsg = file.name.substring(file.name.lastIndexOf('.') + 1)
      const testmsgArr = ['doc', 'docx', 'xls', 'xlsx', 'pdf', 'ppt', 'pptx', 'txt', 'jpg', 'png']
      const extension = testmsgArr.includes(testmsg)
      // if (!extension && !extension2) {
      if (!extension) {
        this.$message({
          // message: "上传文件类型不正确,只允许上传excel文件!",
          message: '只能上传doc/docx/xls/xlsx/pdf/ppt/txt/jpg/png文件!',
          // duration: 2000,
          type: 'error'
        })
        return false
      }
      if (file.size > 50 * 1024 * 1024) {
        this.$message({
          message: '请上传小于50M的文件',
          type: 'error'
        })
        return false
      }
      this.fileList = fileList
    },
    /**
     * @description 监听文件删除
     */
    handleRemove(file, fileList) {
      if (file.id) {
        this.deleteFileId.push(file.id)
      }
      this.fileList = fileList
    }
  }
}
</script>
<style lang="scss"></style>

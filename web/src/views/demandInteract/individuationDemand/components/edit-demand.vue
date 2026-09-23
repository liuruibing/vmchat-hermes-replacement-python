<template>
  <div class="edit-demand">
    <el-form ref="formData" :model="formData" :rules="rules" class="standard-form" style="margin: 0 auto" label-width="100px">
      <el-form-item label="产品代码" prop="fcode">
        <el-input
          v-model="formData.fcode"
          placeholder="产品代码"
          size="small"
          @click.native="productSelectorVisible = true"
        ></el-input>
      </el-form-item>
      <el-form-item label="需求标题" prop="fundName">
        <el-input v-model="formData.fundName" size="small" placeholder="请输入需求标题"></el-input>
      </el-form-item>
      <el-form-item label="需求内容" prop="state">
        <el-input v-model="formData.state" placeholder="请输入需求内容" type="textarea"></el-input>
      </el-form-item>
      <el-form-item label="需求附件">
        <div style="display: flex">
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
        </div>
      </el-form-item>
    </el-form>
    <div style="text-align: center" class="standard-form">
      <el-button size="small" type="info" plain @click="cancel">取 消</el-button>
      <el-button size="small" type="primary" @click="handleSaveDemand" :loading="saveBtnLoading">保 存</el-button>
    </div>
<!--    <el-dialog :modal="false" :visible.sync="productSelectorVisible" :close-on-click-modal="true" title="产品信息" center custom-class="customWidth">
      <el-container class="hg100">
        <el-main class="mainBox">
          <productSelect
            :dialog-visible="productSelectorVisible"
            :select-list="selectList"
            @closedialog="
              () => {
                productSelectorVisible = false
              }
            "
            @submitdialog="handleSubmitClick"
          />
        </el-main>
      </el-container>
    </el-dialog>-->
    <product-selector
      :dialog-visible="productSelectorVisible"
      :tree-data="treeData"
      :show-tree-key-array="showTreeKeyArray"
      :select-list="selectList"
      default-checked-keys="wdgz"
      @closedialog="handleDialogClosed"
      @submitdialog="handleSubmitClick"
    ></product-selector>
  </div>
</template>

<script>
import { insertDemand, getUplodFile, uploadDemand } from '../scripts/api'
import productSelector from '@/components/productSelector'
//import productSelecto from './productSelector'
export default {
  name: 'editDemand',
  components: { productSelector },
  props: {
    curDemandRow: {
      type: Object,
      default: () => {}
    },
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  watch: {
    curDemandRow: {
      handler(val) {
        if (Object.keys(val).length > 0) {
          for (const key in this.formData) {
            this.formData[key] = val[key] || ''
            if (this.formData.fcode) {
              this.selectList = [this.formData.fcode]
            }
          }
          if (this.formData.id == '' || this.formData.id == undefined || this.formData.id == null) {
            return
          } else {
            this.getApplyFile(val)
          }
        } else {
          for (const key in this.formData) {
            this.formData[key] = ''
          }
          this.fileList = []
        }
      },
      deep: true,
      immediate: true
    }
  },
  data() {
    return {
      saveBtnLoading: false,
      productSelectorVisible: false,
      selectList: [],
      treeData: [
        {
          label: '产品列表',
          id: 'zstgwb'
        },
        {
          label: '我的关注',
          id: 'wdgz',
          children: [
            {
              label: '默认分组',
              id: 'mrfz'
            },
            {
              label: '权益组',
              id: 'qyz'
            }
          ]
        }
      ],
      showTreeKeyArray: ['产品列表','我的关注'],
      // form表单绑定
      formData: {
        id: '',
        fundName: '',
        fcode: '',
        fname: '',
        state: ''
      },
      // 文件列表
      fileList: [],
      // 删除文件id
      deleteFileId: [],
      // 校验规则
      rules: {
        fundName: [{ type: 'string', required: true, message: '需求标题不能为空', trigger: 'blur' }],
        state: [{ type: 'string', required: true, message: '需求内容不能为空', trigger: 'blur' }]
      }
    }
  },
  methods: {
    handleSubmitClick(arr) {
      this.productSelectorVisible = false
      this.formData.fcode = arr[0].VC_FUNDCODE || ''
      this.formData.fname = arr[0].VC_FUNDNAME || ''
      this.selectList = arr
    },
    handleDialogClosed() {
      this.productSelectorVisible = false
    },

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
          if (this.fileList && this.fileList.length) {
            this.fileList = this.fileList.map((item) => {
              return {
                ...item,
                name: item.fileName
              }
            })
          }
        } else {
          this.$message.error(res.data.message || '需求附件获取失败')
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
    },
    /**
     * @description 取消按钮关闭弹窗
     */
    cancel() {
      this.$emit('closeEdit', 'NO_REFESH')
    },
    /**
     * @description 新增需求
     */
    handleSaveDemand() {
      this.$refs['formData'].validate((valid) => {
        if (valid) {
          const formData = new FormData()
          for (const key in this.formData) {
            formData.append(key, this.formData[key])
          }
          this.fileList.forEach((item) => {
            if (item.raw) {
              formData.append('file', item.raw)
            }
          })
          if (this.isEdit) {
            formData.append('deleteFileId', this.deleteFileId)
            formData.append('id', this.curDemandRow.id)
            this.saveBtnLoading = true
            uploadDemand(formData)
              .then((res) => {
                this.saveBtnLoading = false
                if (res.data.status === 0) {
                  this.$message.success(res.data.message || '编辑成功')
                  this.$emit('closeEdit', 'REFESH')
                } else {
                  this.$message.error(res.data.message || '编辑失败')
                }
              })
              .catch((err) => {
                this.saveBtnLoading = false
              })
          } else {
            this.saveBtnLoading = true
            insertDemand(formData)
              .then((res) => {
                this.saveBtnLoading = false
                if (res.data.status === 0) {
                  this.$message.success(res.data.message || '新增成功')
                  this.$emit('closeEdit', 'REFESH')
                } else {
                  this.$message.error(res.data.message || '新增失败')
                }
              })
              .catch((err) => {
                this.saveBtnLoading = false
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

<style></style>

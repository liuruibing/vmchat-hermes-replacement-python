<template>
  <div>
    <el-form ref="formData" :model="formData" class="standard-form" :rules="rules" label-width="auto" style="margin: 0 auto">
      <el-form-item :label="fundLabel" prop="fundName">
        <!-- v-if="fundLabel === '产品名称'" -->
        <el-input v-model="formData.fundName" readonly size="small"></el-input>
        <el-button v-if="fundLabel === '产品名称'" type="info" size="small" plain @click="productSelectorVisible = true">选择产品</el-button>
        <el-button v-if="fundLabel === '机构名称'" type="info" size="small" plain @click="departmentVisible = true">选择机构</el-button>
      </el-form-item>
      <!-- <el-form-item label="机构名称" prop="fundName" v-if="fundLabel === '机构名称'">
        <el-select v-model="formData.fundName" placeholder="请选择" size="small">
          <el-option v-for="item in []" :key="item.value" :label="item.label" :value="item.value">
          </el-option>
        </el-select>s
      </el-form-item> -->
      <el-form-item label="需求类型" prop="type">
        <el-select v-model="formData.type" disabled placeholder="请选择" size="small">
          <el-option v-for="item in dataTypeOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="说明" prop="state">
        <el-input v-model="formData.state" placeholder="请录入信息验证的描述" type="textarea"></el-input>
      </el-form-item>
      <el-form-item label="需求附件" prop="fileList">
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
            <el-button size="small" type="info" plain>选择文件</el-button>
            <!-- <div slot="tip" class="el-upload__tip">，。</div> -->
          </el-upload>
        </div>
      </el-form-item>
    </el-form>
    <div style="text-align: center" class="standard-form">
      <el-button size="small" type="info" plain @click="cancel()">取 消</el-button>
      <el-button :disabled="saveDisabled" :icon="saveIcon" size="small" type="primary" @click="formValidate">保 存</el-button>
    </div>
    <product-selector
      :default-checked-keys="defaultCheckedKeys"
      :dialog-visible="productSelectorVisible"
      :select-list="selectList"
      :show-tree-key-array="showTreeKeyArray"
      :tree-data="treeData"
      @closedialog="handleDialogClosed"
      @submitdialog="handleSubmitClick"
    ></product-selector>
    <department-component :department-visible="departmentVisible" :company-list="companyList" @dialogclose="handleCloseDialog" @submit="handleSubmit"></department-component>
  </div>
</template>

<script>
import productSelector from '@/components/productSelector'
import accessPoolApi from '@/api/AccessPoolProcess/accessPool'
import departmentComponent from '@/components/departmentComponent'

export default {
  name: '',
  components: {
    productSelector,
    departmentComponent
  },
  data() {
    const validateFileList = (rule, value, callback) => {
      if (this.fileList.length) {
        callback(new Error('请选择文件'))
      } else {
        callback()
      }
    }
    return {
      type: '', // 新增/编辑
      rowData: {},
      fundLabel: '机构/产品名称',
      saveIcon: '',
      saveDisabled: false,
      formData: {
        fundName: '',
        fundCode: '',
        type: '3',
        state: ''
      },
      rules: {
        fundName: [{ type: 'string', required: true, message: '请选择产品/机构', trigger: 'change' }],
        type: [{ type: 'string', required: true, message: '请选择需求类型', trigger: 'change' }],
        state: [{ type: 'string', required: true, message: '说明不能为空', trigger: 'change' }]
        // fileList: [{ required: true, trigger: 'change', validator: validateFileList }]
      },
      fundList: [],
      dataTypeOptions: [{ label: '产品信息验证', value: '1' }, { label: '产品数据质检', value: '2' }, { label: '机构尽调', value: '3' }],
      fileList: [],
      deleteFileId: [],
      departmentVisible: false,
      productSelectorVisible: false,
      treeData: [
        {
          label: '市场私募',
          id: 'scsm'
        },
        {
          label: '广发托管/外包',
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
        },
        {
          label: '私有产品',
          code: 'sycp'
        }
      ],
      showTreeKeyArray: [],
      selectList: [],
      companyList: [],
      defaultCheckedKeys: 'scsm'
    }
  },
  mounted() {},
  methods: {
    handleCloseDialog() {
      this.departmentVisible = false
    },
    handleSubmit(arr) {
      this.companyList = arr
      this.formData.fundName = this.companyList.map(item => item.COMPANY_SHORT_NAME).toString()
      this.formData.fundCode = this.companyList.map(item => item.COMPANY_ID).toString()
    },
    handleRemove(file, fileList) {
      if (file.id) {
        this.deleteFileId.push(file.id)
      }
      this.fileList = fileList
    },
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
    // 取消
    cancel(refresh) {
      this.$emit('close', refresh)
    },
    setDefaultType(type) {
      this.formData.type = type
      if (type === '1') {
        this.fundLabel = '产品名称'
        this.defaultCheckedKeys = 'scsm'
        this.showTreeKeyArray = ['市场私募']
      } else if (type === '2') {
        this.fundLabel = '产品名称'
        this.defaultCheckedKeys = 'zstgwb'
        this.showTreeKeyArray = ['广发托管/外包']
      } else if (type === '3') {
        this.fundLabel = '机构名称'
        this.defaultCheckedKeys = 'scsm'
        this.showTreeKeyArray = ['市场私募', '我的关注']
      }
    },
    addInit(data) {
      this.formData.fundName = data.fundName || ''
      this.formData.fundCode = data.fundCode || ''
      this.selectList = [
        {
          VC_FUNDCODE: data.fundCode,
          VC_FUNDNAME: data.fundName
        }
      ]
    },
    addInitManager(data) {
      this.formData.fundName = data.companyName || ''
      this.formData.fundCode = data.companyId || ''
      this.companyList = [
        {
          COMPANY_ID: data.companyId,
          COMPANY_SHORT_NAME: data.companyName
        }
      ]
    },
    editInit(params) {
      this.type = 'edit'
      this.fileList = []
      this.deleteFileId = []
      this.rowData = JSON.parse(JSON.stringify(params))
      const data = JSON.parse(JSON.stringify(params))
      this.$nextTick(() => {
        this.formData.fundName = data.fundName
        this.formData.fundCode = data.fundCode
        this.formData.type = data.type
        this.formData.state = data.state
      })
      if (data.type === '1' || data.type === '2') {
        this.selectList = [
          {
            VC_FUNDCODE: data.fundCode,
            VC_FUNDNAME: data.fundName
          }
        ]
        this.fundLabel = '产品名称'
      } else if (data.type === '3') {
        this.companyList = [
          {
            COMPANY_ID: data.fundCode,
            COMPANY_SHORT_NAME: data.fundName
          }
        ]
        this.fundLabel = '机构名称'
      }
      this.getFileList(data.id)
    },

    // 保存
    formValidate() {
      this.$refs['formData'].validate(valid => {
        if (valid) {
          this.saveData()
          // if (this.fileList.length) {
          //   this.saveData()
          // } else {
          //   this.$message.closeAll()
          //   this.$message({
          //     type: 'warning',
          //     message: '请先选择文件！！'
          //   })
          // }
        } else {
          return false
        }
      })
    },
    saveData() {
      const form = JSON.parse(JSON.stringify(this.formData))
      const formData = new FormData()
      for (const key in form) {
        formData.append(key, form[key])
      }
      if (this.type === 'edit') {
        formData.append('id', this.rowData.id)
      }
      this.fileList.forEach(item => {
        if (item.raw) {
          formData.append('file', item.raw)
        }
      })
      if (this.type === 'edit' && this.deleteFileId.length) {
        formData.append('deleteFileId', this.deleteFileId)
      }
      if (this.type === 'edit') {
        this.needManageUpdateUploadUrl(formData)
      } else {
        this.needManageInsertUploadUrl(formData)
      }
    },
    handleDialogClosed() {
      this.productSelectorVisible = false
    },
    handleSubmitClick(arr) {
      this.productSelectorVisible = false
      const fundCodeArr = []
      const fundNameArr = []
      arr.forEach(element => {
        fundCodeArr.push(element.VC_FUNDCODE)
        fundNameArr.push(element.VC_FUNDNAME)
      })
      this.formData.fundCode = fundCodeArr.join(',')
      this.formData.fundName = fundNameArr.join(',')
    },
    // 获取文件列表（申请文件、反馈文件）
    getFileList(id) {
      accessPoolApi
        .needManageSelectEdit({
          fileType: '1',
          id: id
        })
        .then(res => {
          const { status, data, statusText } = res
          if (status === 200) {
            data.data.forEach(element => {
              element.name = element.fileName
            })
            this.fileList = data.data
          }
        })
        .catch(() => {})
    },
    // 新增申请
    needManageInsertUploadUrl(formData) {
      this.saveIcon = 'el-icon-loading'
      this.saveDisabled = true
      accessPoolApi
        .needManageInsertUpload(formData)
        .then(res => {
          this.saveIcon = ''
          this.saveDisabled = false
          const { status, data, message } = res.data
          if (status === 0) {
            this.cancel(true)
            this.$message.closeAll()
            this.$message({
              type: 'success',
              message: '保存成功！！'
            })
          } else {
            this.$message.closeAll()
            this.$message({
              type: 'warning',
              message: message || '保存失败！！'
            })
          }
        })
        .catch(() => {
          this.saveIcon = ''
          this.saveDisabled = false
          this.$message.closeAll()
          this.$message({
            type: 'error',
            message: '保存失败！！'
          })
        })
    },
    // 编辑申请
    needManageUpdateUploadUrl(formData) {
      this.saveIcon = 'el-icon-loading'
      this.saveDisabled = true
      accessPoolApi
        .needManageUpdateUpload(formData)
        .then(res => {
          this.saveIcon = ''
          this.saveDisabled = false
          const { status, data, message } = res.data
          if (status === 0) {
            this.cancel(true)
            this.$message.closeAll()
            this.$message({
              type: 'success',
              message: '保存成功！！'
            })
          } else {
            this.$message.closeAll()
            this.$message({
              type: 'warning',
              message: message || '保存失败！！'
            })
          }
        })
        .catch(() => {
          this.saveIcon = ''
          this.saveDisabled = false
          this.$message.closeAll()
          this.$message({
            type: 'error',
            message: '保存失败！！'
          })
        })
    }
  }
}
</script>
<style lang="scss" scoped></style>

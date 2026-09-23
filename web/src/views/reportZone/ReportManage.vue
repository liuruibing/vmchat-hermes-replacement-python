<template>
  <div class="research-report report-manage-page" v-auto-enter>
    <!-- 查询条件区域 -->
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form :inline="true" :model="queryForm" class="standard-form">
          <el-form-item label="报告名称">
            <el-input
              v-model="queryForm.vcReportName"
              placeholder="请输入报告名称"
              clearable
              size="small"
            ></el-input>
          </el-form-item>
          <el-form-item label="上传者姓名">
            <el-input
              v-model="queryForm.vcUploaderName"
              placeholder="请输入姓名"
              clearable
              size="small"
            ></el-input>
          </el-form-item>
          <el-form-item label="发布日期">
            <el-date-picker
              v-model="queryForm.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              value-format="yyyy-MM-dd"
              size="small"
            ></el-date-picker>
          </el-form-item>
          <el-form-item label="报告类型">
            <el-select
              v-model="queryForm.vcReportType"
              placeholder="请选择"
              clearable
              size="small"
            >
              <el-option label="私募跟踪报告" value="1"></el-option>
              <el-option label="市场策略月报" value="2"></el-option>
              <el-option label="产品研究报告" value="3"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="状态">
            <el-select
              v-model="queryForm.vcResultEnd"
              placeholder="请选择"
              clearable
              size="small"
            >
              <el-option label="启用" value="1"></el-option>
              <el-option label="禁用" value="0"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="small" icon="el-icon-search" @click="handleQuery">查询</el-button>
            <el-button type="primary" size="small" icon="el-icon-plus" @click="handleAdd">新增</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>

    <div id="standard-table" class="table-content">
      <div id="standard-table-margin">
        <vxe-table
          ref="refsTable"
          :data="tableData"
          :loading="tableLoading"
          :cell-style="{ height: '50px' }"
          :height="tableHeight"
          auto-resize
          stripe
          show-overflow="tooltip"
          style="width: 100%"
          sync-resize
        >
          <vxe-table-column align="center" fixed="left" title="序号" type="seq" width="50"></vxe-table-column>
          <vxe-table-column field="vcReportName" label="报告名称" min-width="100" align="center" header-align="center"></vxe-table-column>
          <vxe-table-column field="vcReportType" label="报告类型" width="120" align="center" header-align="center">
            <template slot-scope="scope">
              {{ scope.row.vcReportType === '1' ? '私募跟踪报告' : (scope.row.vcReportType === '2' ? '市场策略月报' : '产品研究报告') }}
            </template>
          </vxe-table-column>
          <vxe-table-column field="vcResultEnd" label="状态" width="80" align="center" header-align="center">
            <template slot-scope="scope">
              {{ scope.row.vcResultEnd === '1' ? '启用' : '禁用' }}
            </template>
          </vxe-table-column>
          <vxe-table-column field="dUpdateTime" label="更新时间" width="180" align="center" header-align="center">
          </vxe-table-column>
          <vxe-table-column field="dReleaseTime" label="发布日期" width="180" align="center" header-align="center"></vxe-table-column>
          <vxe-table-column field="vcUploaderName" label="上传者" width="100" align="center" header-align="center"></vxe-table-column>
          <vxe-table-column field="vcAttachmentName" label="附件" min-width="150" align="center" header-align="center">
            <template slot-scope="scope">
              {{ scope.row.vcAttachmentName || '无' }}
            </template>
          </vxe-table-column>
          <vxe-table-column label="操作" width="300" align="center" header-align="center">
            <template slot-scope="scope">
              <span class="operate-btn table-operation">
                <el-button size="small" type="info" plain @click="handleEdit(scope.row)">编辑</el-button>
                <el-button size="small" type="info" plain @click="handleDelete(scope.row)">删除</el-button>
                <el-button size="small" type="info" plain @click="handleDownload(scope.row)">下载</el-button>
              </span>
            </template>
          </vxe-table-column>
        </vxe-table>

        <vxe-pager
          :current-page="queryForm.pageNum"
          :page-size="queryForm.pageSize"
          :total="total"
          :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
          border
          size="medium"
          class="standard-vxe-pager"
          @page-change="handlePageChange"
        />
      </div>
    </div>

    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :destroy-on-close="true"
      custom-class="saveAsDialog"
      width="600px"
      append-to-body
    >
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="报告名称" prop="vcReportName">
          <el-input v-model="formData.vcReportName" placeholder="请输入报告名称" style="width: 300px !important;"></el-input>
        </el-form-item>
        <el-form-item label="报告类型" prop="vcReportType">
          <el-select v-model="formData.vcReportType" placeholder="请选择报告类型">
            <el-option label="私募跟踪报告" value="1"></el-option>
            <el-option label="市场策略月报" value="2"></el-option>
            <el-option label="产品研究报告" value="3"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="上传附件" prop="attachedFile">
          <el-upload
            ref="upload"
            :auto-upload="false"
            :file-list="fileList"
            :on-change="handleChange"
            :on-remove="handleRemove"
            action=""
            class="upload-demo"
            name="attachedFile"
          >
            <el-button size="small" type="primary">选择文件</el-button>
            <div slot="tip" class="el-upload__tip">只能上传pdf/word/ppt文件，大小不超过50MB，且仅支持上传1个文件</div>
          </el-upload>
        </el-form-item>

        <el-form-item label="是否启用">
          <el-switch
            v-model="formData.vcResultEnd"
            active-value="1"
            inactive-value="0"
            active-text="启用"
            inactive-text="禁用"
          ></el-switch>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false" size="small" type="info" plain>取消</el-button>
        <el-button type="primary" size="small" @click="handleSave">保存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import reportZoneApi from '@/api/reportZone/index'
import commonApi from '@/api/common'
import moment from 'moment'
import lodash from 'lodash'
export default {
  components: {},
  data() {
    return {
      moment,
      queryForm: {
        vcReportName: '',
        vcUploaderName: '',
        dateRange: [],
        vcReportType: '',
        vcResultEnd: '',
        dReleaseTimeBegin: '',
        dReleaseTimeEnd: '',
        pageNum: 1,
        pageSize: 20,
        offset: 0,
        limit: 20
      },
      tableData: [],
      total: 0,
      tableLoading: false,
      tableHeight: 0,
      dialogVisible: false,
      dialogType: 'add',
      dialogTitle: '新增报告',
      formData: {
        fid: '',
        vcReportName: '',
        vcReportType: '',
        vcResultEnd: '1',
        dReleaseTime: ''
      },
      formRules: {
        vcReportName: [{ required: true, message: '请输入报告名称', trigger: 'blur' }],
        vcReportType: [{ required: true, message: '请选择报告类型', trigger: 'change' }],
        attachedFile: [
          {
            required: true,
            validator: function(rule, value, callback) {
              if (this.fileList.length === 0) {
                callback(new Error('请上传报告附件'))
              } else {
                callback()
              }
            }.bind(this),
            trigger: ['change', 'blur']
          }
        ]
      },
      fileList: [],
      deleteFileId: [],
      oldFileId: ''
    }
  },
  mounted() {
    this.handleTableHeight()
    this.handleQuery()
  },
  methods: {
    handleTableHeight() {
      this.$nextTick(function() {
        if (this.$refs.refsTable) {
          this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 180
          window.onresize = function() {
            this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 180
          }.bind(this)
        }
      }.bind(this))
    },
    formatDateRange() {
      if (this.queryForm.dateRange && this.queryForm.dateRange.length === 2) {
        this.queryForm.dReleaseTimeBegin = this.queryForm.dateRange[0]
        this.queryForm.dReleaseTimeEnd = this.queryForm.dateRange[1]
      } else {
        this.queryForm.dReleaseTimeBegin = ''
        this.queryForm.dReleaseTimeEnd = ''
      }
    },
    async handleQuery() {
      this.formatDateRange()
      this.tableLoading = true
      try {
        const dto = {
          vcReportName: this.queryForm.vcReportName,
          vcUploaderName: this.queryForm.vcUploaderName,
          dReleaseTimeBegin: this.queryForm.dReleaseTimeBegin,
          dReleaseTimeEnd: this.queryForm.dReleaseTimeEnd,
          vcReportType: this.queryForm.vcReportType,
          vcResultEnd: this.queryForm.vcResultEnd,
          offset: (this.queryForm.pageNum - 1) * this.queryForm.pageSize,
          limit: this.queryForm.pageSize
        }
        const res = await reportZoneApi.selectManageReportList(dto)
        if (res && res.data) {
          if (res.data.status === 0) {
            this.tableData = res.data.data.rows || []
            this.total = res.data.data.total || 0
          } else if (res.status === 200) {
            this.tableData = res.data.data.rows || []
            this.total = res.data.data.total || 0
          } else {
            this.$message.error('查询失败：' + (res.data.message || '接口返回异常'))
          }
        }
      } catch (e) {
        this.$message.error('查询失败：' + (e.message || '系统异常'))
      } finally {
        this.tableLoading = false
      }
    },
    handlePageChange({ currentPage, pageSize }) {
      this.queryForm.pageNum = currentPage
      this.queryForm.pageSize = pageSize
      this.queryForm.offset = (currentPage - 1) * pageSize
      this.queryForm.limit = pageSize
      this.handleQuery()
    },
    handleAdd() {
      this.dialogType = 'add'
      this.dialogTitle = '新增报告'
      this.formData = {
        fid: '',
        vcReportName: '',
        vcReportType: '',
        vcResultEnd: '1',
        dReleaseTime: moment().format('YYYY-MM-DD') // 确保日期字段有值
      }
      this.fileList = []
      this.deleteFileId = []
      this.oldFileId = '' // 重置旧文件ID
      this.dialogVisible = true
      this.$nextTick(function() {
        if (this.$refs.formRef) {
          this.$refs.formRef.clearValidate()
        }
        if (this.$refs.upload) {
          this.$refs.upload.clearFiles()
        }
      }.bind(this))
    },
    handleEdit(row) {
      this.dialogType = 'edit'
      this.dialogTitle = '编辑报告'
      this.formData = {
        fid: row.fid,
        vcReportName: row.vcReportName,
        vcReportType: row.vcReportType,
        vcResultEnd: row.vcResultEnd,
        dReleaseTime: row.dReleaseTime || moment().format('YYYY-MM-DD')
      }
      this.fileList = []
      this.deleteFileId = []
      this.oldFileId = row.fid
      if (row.vcAttachmentName) {
        this.fileList = [{
          name: row.vcAttachmentName,
          id: row.fid, // 旧附件ID
          url: row.vcAttachmentUrl || '',
          isOldFile: true // 标记为旧文件
        }]
      }
      this.dialogVisible = true
      this.$nextTick(function() {
        if (this.$refs.formRef) {
          this.$refs.formRef.clearValidate()
        }
      }.bind(this))
    },
    async handleDelete(row) {
      try {
        await this.$confirm('确定删除该报告吗？删除后不可恢复！', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        const res = await reportZoneApi.deleteReport(row.fid)
        if (res.status === 200) {
          this.$message.success('删除成功')
          this.handleQuery()
        } else {
          this.$message.error('删除失败：' + res.data.message)
        }
      } catch (e) {
        if (e !== 'cancel') {
          this.$message.error('删除失败：' + (e.message || '系统异常'))
        }
      }
    },
    async handleDownload(row) {
      try {
        if (!row.vcAttachmentName) {
          this.$message.warning('该报告无附件可下载')
          return
        }
        try {
            const res = await reportZoneApi.downloadReport(row.fid)
            const blob = new Blob([res.data], { type: 'application/octet-stream' })
            const href = URL.createObjectURL(blob)
            this.downloadFile(href, row.vcAttachmentName, row.vcAttachmentExt)
          this.$message.success('下载成功')
        } catch (e) {
          this.$message.error('下载失败：' + e.message)
        }
        /* const res = await reportZoneApi.downloadReport(row.fid)
        if (res.data instanceof Blob) {
          const blob = new Blob([res.data], {
            type: this.getFileMimeType(row.vcAttachmentExt || row.vcAttachmentName.split('.').pop())
          })
          const href = URL.createObjectURL(blob)
          const a = document.createElement('a')
          a.href = href
          a.download = row.vcAttachmentName || '报告文件'
          document.body.appendChild(a)
          a.click()
          document.body.removeChild(a)
          URL.revokeObjectURL(href)
          this.$message.success('下载成功')
        } else {
          const errorText = await res.data.text()
          const errorObj = JSON.parse(errorText)
          this.$message.error('下载失败：' + (errorObj.message || '文件不存在'))
        } */
      } catch (e) {
        this.$message.error('下载失败：' + (e.message || '文件不存在或已被删除'))
      }
    },
    downloadFile(href, name, ext) {
      const a = document.createElement('a')
      a.href = href
      a.download = name ? name : `报告.${ext || ''}`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      if (href.startsWith('blob:')) {
        setTimeout(() => URL.revokeObjectURL(href), 5000)
      }
    },

    handleChange(file, fileList) {
      // 验证文件后缀
      const lastDotIndex = file.name.lastIndexOf('.')
      const fileSuffix = lastDotIndex > -1 ? file.name.substring(lastDotIndex + 1) : ''
      const whiteList = ['pdf', 'doc', 'docx', 'ppt', 'pptx']
      const isSuffixValid = whiteList.indexOf(fileSuffix.toLowerCase()) > -1

      if (!isSuffixValid) {
        this.$message.error('只能上传pdf/word/ppt文件!')
        this.fileList = []
        return false
      }

      if (file.size > 50 * 1024 * 1024) {
        this.$message.error('请上传小于50M的文件!')
        this.fileList = []
        return false
      }

      this.fileList = [fileList[fileList.length - 1]]
      if (this.dialogType === 'edit' && this.oldFileId) {
        this.deleteFileId = [this.oldFileId]
      }

      if (this.$refs.formRef) {
        this.$refs.formRef.validateField('attachedFile')
      }
    },
    handleRemove(file, fileList) {
      // 只有旧文件才加入删除列表
      if (file.isOldFile || file.id) {
        this.deleteFileId.push(file.id || this.oldFileId)
      }
      this.fileList = fileList
      if (this.$refs.formRef) {
        this.$refs.formRef.validateField('attachedFile')
      }
    },
    async handleSave() {
      try {
        if (this.fileList.length === 0) {
          this.$message.error('请上传报告附件！')
          return
        }
        const valid = await new Promise(function(resolve) {
          if (this.$refs.formRef) {
            this.$refs.formRef.validate(function(valid) {
              resolve(valid)
            })
          } else {
            resolve(false)
          }
        }.bind(this))
        if (!valid) return


        const formData = new FormData()
        const formKeys = Object.keys(this.formData)
        for (let i = 0; i < formKeys.length; i++) {
          const key = formKeys[i]
          formData.append(key, this.formData[key] || '')
        }
        if (this.deleteFileId.length > 0) {
          formData.append('deleteFileId', this.deleteFileId.join(','))
        }

        const hasNewFile = this.fileList.some(item => item.raw)
        if (hasNewFile) {
          formData.append('file', this.fileList[0].raw)
        }

        const res = this.dialogType === 'add'
          ? await reportZoneApi.insertReport(formData)
          : await reportZoneApi.updateReport(formData)

        // 处理响应
        if (res && res.data && res.status === 200) {
          this.$message.success(this.dialogType === 'add' ? '新增成功' : '编辑成功')
          this.dialogVisible = false
          this.handleQuery()
        } else {
          this.$message.error((this.dialogType === 'add' ? '新增' : '编辑') + '失败：' + (res && res.data && res.data.message ? res.data.message : '接口返回异常'))
        }
      } catch (e) {
        console.error('保存失败详情：', e)
        this.$message.error('保存失败：' + (e.message || '系统异常，请检查接口或参数'))
      }
    }
  }
}
</script>

<style lang="scss" scoped>
::v-deep .dialog-footer {
  text-align: center !important;  // 按钮居中
}
.report-manage-page {
  background: #fff;

  ::v-deep .saveAsDialog {
    width: 780px !important;
  }

  ::v-deep .el-dialog__wrapper .el-dialog__header span {
    color: #333 !important;
  }

  ::v-deep .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }

  ::v-deep .standard-vxe-pager {
    margin-top: 20px;
    text-align: right;
  }

  .table-operation {
    display: flex;
    justify-content: center;
    gap: 8px;
  }

  ::v-deep .upload-demo {
    margin-top: 5px;
  }
}
</style>

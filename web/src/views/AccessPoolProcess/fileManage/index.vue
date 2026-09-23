<template>
  <div class="file-manage" v-auto-enter>
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formQuery" :inline="true" :model="formQuery" class="standard-form" label-width="auto">
          <el-form-item label="">
            <el-input v-model="formQuery.fundCode" placeholder="请输入产品代码" size="small" />
          </el-form-item>
          <el-form-item label="">
            <el-input v-model="formQuery.fundName" placeholder="请输入产品名称" size="small" />
          </el-form-item>
          <el-form-item label="">
            <el-input v-model="formQuery.fileName" placeholder="请输入文件名称/拼音首字母" style="width: 210px !important;" size="small" />
          </el-form-item>
          <el-form-item label="">
            <el-select v-model="formQuery.fileType" placeholder="请选择文件类型" size="small" clearable>
              <el-option v-for="item in statusOptions" :key="item.DIM_CDE" :label="item.DIM_NME" :value="item.DIM_CDE" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="small" @click="queryUploadFileList" icon="el-icon-search">查询</el-button>
            <el-button type="info" plain size="small" @click="reset" icon="el-icon-refresh-left">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <div id="standard-table" class="table-content">
      <div id="standard-table-margin">
        <vxe-table
          ref="refsTable"
          v-loading="tableLoading"
          :cell-style="{ height: '50px' }"
          :data="tableData"
          :height="tableHeight"
          auto-resize
          stripe=""
          show-overflow="tooltip"
          style="width: 100%"
          sync-resize
          resizable
          @sort-change="handleSortChange"
        >
          <vxe-table-column type="seq" width="50" align="center" header-align="center" title="序号" />
          <vxe-table-column
            v-for="(col, i) in tableColumns"
            :key="i"
            :field="col.prop"
            :label="col.label"
            :min-width="col.minWidth"
            :align="col.align"
            :sortable="col.sortable"
            show-overflow-tooltip
            header-align="center"
            stripe
          >
            <template slot-scope="scope">
              <span v-if="col.prop === 'fileType'">
                <span>
                  {{ scope.row[col.prop] | fileTypeFilter(that) }}
                </span>
              </span>
              <span v-else>{{ scope.row[col.prop] | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column label="操作" width="140" align="center" header-align="center">
            <template slot-scope="scope">
              <span class="operate-btn table-operation">
                <el-button type="info" plain size="small" @click="handleDownload(scope.row)">下载</el-button>
              </span>
            </template>
          </vxe-table-column>
        </vxe-table>
        <vxe-pager
          :current-page="formQuery.pageNum"
          :page-size="formQuery.pageSize"
          :total="total"
          :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
          border
          size="medium"
          class="standard-vxe-pager"
          @page-change="pagination"
        />
      </div>
    </div>
<!--    <Pagination :total="total" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination" />-->
  </div>
</template>

<script>
import { TABLE_COLUMNS } from './scripts/constant'
import Pagination from '@/components/Pagination'
import { getUploadFileAll } from './scripts/api'
import commonFun from '@/filters/new_common'
import commonFunOld from '@/filters/common'
import commonAPI from '@/api/common.js'
export default {
  name: 'FileManage',
  components: { Pagination },
  filters: {
    fileTypeFilter(value, that) {
      const obj = that.statusOptions.find((item) => item.DIM_CDE === value)
      return (obj && obj.DIM_NME) || '-'
    }
  },
  data() {
    return {
      that: this,
      formQuery: {
        fundCode: '',
        fundName: '',
        fileName: '',
        fileType: '',
        pageSize: 20,
        pageNum: 1
      },
      total: 0,
      tableColumns: TABLE_COLUMNS,
      tableData: [],
      statusOptions: [],
      tableLoading: false,
      tableHeight: 0
    }
  },
  mounted() {
    this.initData()
    this.formQuery.fundCode = this.$route.query.fundCode || ''
    this.formQuery.fundName = this.$route.query.fundName || ''
    this.handleTableHeight()
  },
  methods: {
    handleSortChange(val) {
      this.formQuery.orderString = commonFunOld.queryOrderBy_vxe_template(val)
      // 查询
      this.queryUploadFileList()
    },
    /**
     * @description 动态设置表格高度
     */
    handleTableHeight() {
      this.$nextTick(() => {
        // 根据浏览器高度设置初始高度
        this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 165
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 165
        }
      })
    },
    async initData() {
      await this.getFileTypeOptions()
      await this.queryUploadFileList()
    },
    async getFileTypeOptions() {
      const data = {
        indexCode: '1af946e1-025e-4959-84a6-52c28960b80d'
      }
      try {
        const res = await commonAPI.getDataBysqlCode(data)
        if (res.data.status === 0) {
          this.statusOptions = res.data.data || []
        }
      } catch (e) {
        this.statusOptions = []
      }
    },
    async queryUploadFileList() {
      const params = {
        limit: this.formQuery.pageSize,
        offset: (this.formQuery.pageNum - 1) * this.formQuery.pageSize,
        ...this.formQuery
      }
      delete params.pageNum
      delete params.pageSize
      this.tableLoading = true
      try {
        const res = await getUploadFileAll(params)
        if (res.data.status === 0) {
          this.tableData = res.data.data.rows || []
          this.total = res.data.data.total
          this.tableLoading = false
        } else {
          this.tableData = []
          this.total = 0
          this.tableLoading = false
          this.$message({
            type: 'error',
            message: res.data.message || '查询失败',
            customClass: 'message-error'
          })
        }
      } catch (e) {
        this.tableData = []
        this.total = 0
        this.tableLoading = false
      }
    },
    reset() {
      for (const key in this.formQuery) {
        this.formQuery[key] = ''
      }
      this.formQuery.pageSize = 20
      this.formQuery.pageNum = 1
      this.queryUploadFileList()
    },
    handleDownload(row) {
      const data = {
        id: row.id || '',
        token: this.$store.getters.token
      }
      const action = this.$store.state.setting.baseApi + `/api/fundAccess/approve/download`
      commonFun.formDownloadFile(data, action, 'POST')
    },
    pagination(val) {
     /*  const { page, limit } = val
      this.formQuery.pageNum = page
      this.formQuery.pageSize = limit */
      const { currentPage, pageSize } = val;
      // 起始页
      this.formQuery.pageNum  = currentPage;
      // 每页数量
      this.formQuery.pageSize = pageSize;
      this.queryUploadFileList()
    }
  },
  beforeDestroy() {
    // 组件销毁移除监听事件
    window.onresize = null
  }
}
</script>

<style lang="scss" scoped>
.file-manage {
  // padding: 10px;
}
.title-style {
  color: #0f65dd;
  vertical-align: middle;
  height: 35px;
  line-height: 35px;
  font-size: 16px;
  margin-left: 5px;
}
.color-box {
  display: inline-block;
  height: 30px;
  width: 2px;
  background-color: #0f65dd;
}
::v-deep .vxe-table .vxe-body--row.row--stripe {
  background-color: #f9fafe !important;
}
</style>

<template>
  <div class="research-report analyse-page" v-auto-enter>
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formQuery" :inline="true" :model="formQuery" class="standard-form">
          <el-form-item label="">
            <el-input v-model="formQuery.title" placeholder="请输入标题" size="small" clearable />
          </el-form-item>
          <el-form-item label="">
            <el-input v-model="formQuery.summary" placeholder="请输入摘要" size="small" clearable />
          </el-form-item>
          <el-form-item label="">
            <el-input v-model="formQuery.author" placeholder="请输入作者姓名" size="small" clearable />
          </el-form-item>
<!--          <el-form-item label="">
            <el-select v-model="formQuery.type" placeholder="请选择资讯类型" size="small" clearable>
              <el-option v-for="item in zxTypeArr" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
            </el-select>
          </el-form-item>-->
          <el-form-item label="">
            <el-select v-model="formQuery.norgan" placeholder="请选择所属机构" size="small" clearable>
              <el-option v-for="item in norganList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
            </el-select>
          </el-form-item>
          <el-form-item label="">
            <el-select v-model="formQuery.arearType" placeholder="请选择文章展示区域" size="small" clearable @change="changeArear">
              <el-option v-for="item in arearOptions" :key="item.DIM_CDE" :label="item.DIM_NME" :value="item.DIM_CDE" />
            </el-select>
          </el-form-item>

          <el-form-item label="" prop="ndate">
            <el-date-picker
              v-model="formQuery.ndate"
              @change="changeDatePicker"
              type="daterange"
              value-format="yyyy-MM-dd"
              range-separator="至"
              start-placeholder="发布开始日期"
              size="small"
              end-placeholder="发布结束日期"
            ></el-date-picker>
          </el-form-item>
          <el-form-item label="">
            <el-select v-model="formQuery.flag" placeholder="请选择文章类型" size="small" clearable>
              <el-option v-for="item in flagOptions" :key="item.DIM_CDE" :label="item.DIM_NME" :value="item.DIM_CDE" />
            </el-select>
          </el-form-item>
          <el-form-item label="">
            <el-select v-model="formQuery.status" placeholder="请选择状态" size="small" clearable>
              <el-option v-for="item in statusOptions" :key="item.DIM_CDE" :label="item.DIM_NME" :value="item.DIM_CDE" />
            </el-select>
          </el-form-item>
          <el-form-item class="">
            <el-button type="primary" size="small" icon="el-icon-search" @click="queryExamineList">查询</el-button>
            <el-button type="primary" size="small" icon="el-icon-plus" @click="addReport('ADD')">新增</el-button>
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
          :sort-config="{ trigger: 'cell', defaultSort: { field: 'updateTime', order: 'desc' }, orders: ['desc', 'asc', null] }"
          show-overflow="tooltip"
          style="width: 100%"
          sync-resize
          @sort-change="handleSortTable"
        >
          <vxe-table-column align="center" fixed="left" title="序号" type="seq" width="50"></vxe-table-column>
          <vxe-table-column field="editLoading" title="editLoading" :visible=false  ></vxe-table-column>
          <vxe-table-column
            v-for="(col, i) in tableColumns"
            :key="i"
            :field="col.prop"
            :label="col.label"
            :sortable="col.sortable"
            :width="col.width"
            :align="col.align"
            show-overflow-tooltip
            header-align="center"
          >
            <template slot-scope="scope">
              <span v-if="col.prop === 'status'">
                <span
                  :style="{
                    color: setStatusColor(scope.row[col.prop])
                  }"
                >
                  {{ scope.row[col.prop] | statusFilter(that) }}
                </span>
              </span>
              <span v-else-if="col.prop === 'norgan'">{{ scope.row[col.prop] | norganFilter(that) }}</span>
              <span v-else-if="col.prop === 'type'">{{ scope.row[col.prop] | gfTypeFilter(that) }}</span>
              <span v-else-if="col.prop === 'flag'">{{ scope.row[col.prop] | flagFilter(that) }}</span>
              <span v-else-if="col.prop === 'isHdleft'">{{ scope.row[col.prop] | isHdleftFilter(that) }}</span>
              <span v-else-if="col.prop === 'arearType'">{{ scope.row[col.prop] | arearFilter(that, scope.row) }}</span>
              <span v-else>{{ scope.row[col.prop] }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column label="操作" width="200" align="center" header-align="center">
            <template slot-scope="scope">
              <span class="operate-btn table-operation">
                <el-button :loading="scope.row.editLoading" type="info" size="small" plain @click="editReport(scope.row, 'EDIT')">编辑</el-button>
                <el-button type="info" size="small" plain @click="deleteReport(scope.row)">删除</el-button>
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
    </div><!--
    <Pagination :total="total" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination" />-->
    <el-dialog
      :title="editTitle"
      :visible.sync="editDialog"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :destroy-on-close="true"
      custom-class="saveAsDialog"
      @close="closeEdit"
    >
      <report-edit v-if="editDialog" :current-row="currentRow" :typeList="typeOptions" :norganList="norganList" :dialog-status="dialogStatus" @closeEdit="closeEdit"></report-edit>
    </el-dialog>
  </div>
</template>

<script>
import { deleteReport, editArticle, reportList } from './script/api'
import { AREAR_TYPE, FLAG_TYPE, STATUS_COLOR_MAP, STATUS_TYPE, TABLE_COLUMNS } from './script/constant'
import Pagination from '@/components/Pagination'
import reportEdit from './components/reportEdit'
import commonApi from '@/api/common'
import lodash from 'lodash'

export default {
  components: {
    Pagination,
    reportEdit
  },
  data() {
    return {
      editLoading: false,
      that: this,
      formQuery: {
        ndate: [],
        ndateBegin: '',
        ndateEnd: '',
        flag: '',
        arearType: '',
        orderString: 'updateTime desc',
        pageSize: 20,
        pageNum: 1,
        type: '2'
      },
      total: 0,
      tableColumns: TABLE_COLUMNS,
      statusColor: STATUS_COLOR_MAP,
      statusOptions: STATUS_TYPE,
      flagOptions: FLAG_TYPE,
      arearOptions: AREAR_TYPE,
      arearOptionsForm: [],
      typeOptions: [],
      zxTypeArr: [

        { dimCde: '2', dimNme: '广发资讯' },

      ],
      //{ dimCde: '3', dimNme: '私募观点' }，备份
      // { dimCde: '1', dimNme: '监管动态' },备份
      norganList: [],
      tableData: [],
      editDialog: false,
      editTitle: '',
      currentRow: null,
      dialogStatus: 'ADD',
      tableLoading: false,
      tableHeight: 0
    }
  },
  filters: {
    statusFilter(value, that) {
      const obj = that.statusOptions.find((item) => item.DIM_CDE === value)
      return (obj && obj.DIM_NME) || '-'
    },
    typeFilter(value, that) {
      const obj = that.typeOptions.find((item) => item.DIM_CDE === value)
      return (obj && obj.DIM_NME) || '-'
    },
    gfTypeFilter(value, that) {
      const obj = that.zxTypeArr.find((item) => item.dimCde === value)
      return (obj && obj.dimNme) || '-'
    },
    flagFilter(value, that) {
      const obj = that.flagOptions.find((item) => item.DIM_CDE === value)
      return (obj && obj.DIM_NME) || '-'
    },
    isHdleftFilter(value, that) {
      return value === '0' ? '否' : '是'
    },
    arearFilter(value, that, row) {
      // if (value === '1' && row.type === '1') {
      //   return '行业动态上'
      // }
      const obj = that.arearOptions.find((item) => item.DIM_CDE === value)
      return (obj && obj.DIM_NME) || '-'
    },
    norganFilter(value, that, row) {
      const obj = that.norganList.find((item) => item.dimCde === value)
      return (obj && obj.dimNme) || '-'
    }
  },
  watch: {
    'formQuery.type'(val) {
      if (val === '1') {
        this.formQuery.flag = '1'
        if (this.formQuery.arearType !== '0') {
          this.formQuery.arearType = ''
        }
        this.arearOptionsForm = AREAR_TYPE.slice(0, 1)
      }
      if (val === '2') {
        if (this.formQuery.arearType === '0') {
          this.formQuery.arearType = ''
        }
        this.arearOptionsForm = AREAR_TYPE.slice(1)
      }
      if (!val) {
        this.arearOptionsForm = []
      }
    }
  },
  mounted() {
    this.getReportListOptions('0')
    this.getReportListOptions('1')
    this.initData()
  },
  methods: {
    getReportListOptions(type) {
      let params = type === '0' ? 'NEWTYPEDETAIL' : 'NEWORGAN'
      commonApi.edimsDdiaCommon(params).then((res) => {
        if (res.data.status === 0) {
          if (type === '0') {
            this.typeOptions = res.data.data
          } else {
            this.norganList = res.data.data
          }
        }
      })
    },
    changeDatePicker(val) {
      if (val) {
        this.formQuery.ndateBegin = val[0]
        this.formQuery.ndateEnd = val[1]
      } else {
        this.formQuery.ndateBegin = ''
        this.formQuery.ndateEnd = ''
      }
     // console.log(val, 'va')
    },
    changeArear(val) {
      this.formQuery.arearType = val
    },
    /**
     * @description 动态设置表格高度
     */
    handleTableHeight() {
      this.$nextTick(() => {
        // 根据浏览器高度设置初始高度
        this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 180
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 180
        }
      })
    },
    async initData() {
      this.handleTableHeight()
      await this.queryExamineList()
    },
    // 页面排序
    handleSortTable(val) {
      this.formQuery.orderString = this.$fun.queryOrderBy_vxe_template(val)
      this.queryExamineList()
    },
    async queryExamineList() {
      let param = lodash.cloneDeep(this.formQuery)
      const params = {
        limit: param.pageSize,
        offset: (param.pageNum - 1) * param.pageSize,
        ...param
      }
      if (param.arearType === '0') {
        params.type = '1'
        params.arearType = '1'
      }
      if (param.arearType === '1') {
        params.type = '2'
        params.arearType = '1'
      }
      // let arearCopy = lodash.cloneDeep(this.formQuery).arearType
      // params.arearType = arearCopy === '0' ? '1' : arearCopy
      delete params.pageNum
      delete params.pageSize
      delete params.ndate
      this.tableLoading = true
      try {
        const res = await reportList(params)
       // console.log(res, 'res')
        if (res.data.data.rows && res.data.data.rows.length > 0) {
          const resultData = res.data.data.rows || []
          resultData.forEach((item) => {
            if (item.type == '1') {
              item.typeStr = '监管动态'
            } else if (item.type == '2') {
              item.typeStr = '广发资讯'
            } else {
              item.typeStr = '私募观点'
            }
          })
          // resultData.forEach(element => {
          // element.ntypeDetail = getValueForArrayByKey(this.typeOptions, element.ntypeDetail, 'dimCde', 'dimNme')
          // element.norgan = getValueForArrayByKey(this.norganList, element.norgan, 'dimCde', 'dimNme')
          // })
          this.tableData = resultData
          this.total = res.data.data.total
          this.tableLoading = false
        } else {
          this.tableData = []
          this.total = 0
          this.tableLoading = false
        }
      } catch (e) {
        this.tableData = []
        this.total = 0
        this.tableLoading = false
      }
    },
    setStatusColor(val) {
      const colorObj = this.statusColor.find((item) => item.value === val)
      return colorObj && colorObj.color
    },
    pagination(val) {
      /* const { page, limit } = val
      this.formQuery.pageNum = page
      this.formQuery.pageSize = limit */
      const { currentPage, pageSize } = val;
      // 起始页
      this.formQuery.pageNum = currentPage;
      // 每页数量
      this.formQuery.pageSize = pageSize;
      this.queryExamineList()
    },
    addReport(status) {
      this.editDialog = true
      this.editTitle = '新增'
      this.dialogStatus = status
    },
    editReport(row, statusValue) {
      let params = {}
      params.fid = row.fid
      this.$set(row, 'editLoading', true);
      editArticle(params).then((res) => {
        this.$set(row, 'editLoading', false);
        let { status, data, message } = res.data
        if (status === 200) {
          const deepRow = _.cloneDeep(row)
          this.currentRow = { ...deepRow, fileList: data || [] }
          this.dialogStatus = statusValue
          setTimeout(() => {
            this.editDialog = true
          }, 300)
          this.editTitle = '编辑'
        } else {
          this.$message.closeAll()
          this.$message.warning(message || '获取信息失败，无法编辑')
        }
      })

    },
    closeEdit(status) {
      this.editDialog = false
      if (status === 'refesh') {
        this.queryExamineList()
      }
      for (const key in this.currentRow) {
        this.currentRow[key] = ''
      }
    },
    async deleteReport(row) {
      const data = {
        fid: row.fid || ''
      }
      this.$confirm('是否删除该条准入记录？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          deleteReport(data)
            .then((res) => {
              if (res.data.status === 0) {
                this.$message({
                  type: 'success',
                  message: res.data.message || '删除成功'
                })
                this.queryExamineList()
              } else {
                this.$message({
                  type: 'success',
                  message: '删除失败'
                })
              }
            })
            .catch((e) => {
              this.$message({
                type: 'success',
                message: '删除失败'
              })
            })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消操作'
          })
        })
    }
  }
}
</script>

<style lang="scss" scoped>
.research-report {
  ::v-deep .saveAsDialog {
    width: 780px !important;
  }

  .color-box {
    display: inline-block;
    height: 30px;
    width: 2px;
    background-color: #0f65dd;
  }

  .title-style {
    color: #0f65dd;
    vertical-align: middle;
    height: 35px;
    line-height: 35px;
    font-size: 16px;
    margin-left: 5px;
  }

  ::v-deep .el-dialog__wrapper .el-dialog__header span {
    color: #333 !important;
  }

  ::v-deep .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
}
</style>

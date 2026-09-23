<template>
  <div class="private-product">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formInline" class="standard-form" :inline="true" :model="formInline">
          <el-row>
            <el-col :span="24">
              <el-form-item label="产品代码">
                <el-input v-model="formInline.fundCode" size="small" placeholder="请输入产品代码"></el-input>
              </el-form-item>
              <el-form-item label="产品名称">
                <el-input v-model="formInline.fundName" size="small" placeholder="请输入产品名称"></el-input>
              </el-form-item>
              <el-form-item label="策略类型">
                <el-select v-model="formInline.strategyList" size="small" clearable filterable placeholder="请选择策略类型" @change="handleChange">
                  <el-option v-for="item in investOptions" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </el-select>
              </el-form-item>
              <el-form-item label="子策略类型">
                <el-select v-model="formInline.subStrategyList" size="small" clearable filterable placeholder="请选择子策略类型">
                  <el-option v-for="item in investDetailOptions" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </el-select>
              </el-form-item>
              <el-form-item label="产品明细类型">
                <el-select v-model="formInline.typeDetailList" size="small" clearable filterable placeholder="请选择产品明细类型">
                  <el-option v-for="item in typeDetailOptions" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </el-select>
              </el-form-item>

              <el-form-item label="产品属性">
                <el-select v-model="formInline.starWishFlag" size="small" clearable filterable placeholder="请选择产品属性">
                  <el-option v-for="item in starWishOptions" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </el-select>
              </el-form-item>
              <el-form-item label="成立日期">
                <el-date-picker
                  v-model="formInline.date"
                  end-placeholder="结束日期"
                  range-separator="至"
                  size="small"
                  start-placeholder="开始日期"
                  type="daterange"
                  value-format="yyyy-MM-dd"
                ></el-date-picker>
              </el-form-item>
              <el-form-item label="管理人">
                <el-input v-model="formInline.nameGlr" size="small" placeholder="请输入管理人"></el-input>
              </el-form-item>
              <el-form-item label="投资经理">
                <el-input v-model="formInline.fundManage" size="small" placeholder="请输入投资经理"></el-input>
              </el-form-item>
              <el-form-item label="数据来源">
                <el-select v-model="formInline.source" size="small" clearable placeholder="请选择数据来源">
                  <el-option v-for="item in sourceTypeOptions" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </el-select>
              </el-form-item>
              <el-form-item style="">
                <el-button type="primary" size="small" icon="el-icon-search" @click="handleSearchTable">查询</el-button>
                <el-button v-btn="'examineadd'" type="primary" size="small" icon="el-icon-plus" @click="handleAddFund">新增</el-button>
                <el-button :icon="exportIcon2" :disabled="exportButton2" size="small" plain type="info" @click="exportData">
                  {{ exportText2 }}
                </el-button>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>
    </div>
    <div class="table-content" id="standard-table">
      <div id="standard-table-margin">
        <vxe-table
          v-loading="tableLoading"
          ref="refsTable"
          :cell-style="{ height: '50px' }"
          :data="tableData"
          :height="tableHeight"
          auto-resize
          stripe
          sync-resize
          show-overflow="tooltip"
          :sort-config="{ remote: true }"
          style="width: 100%"
          @sort-change="customSortMethod"
          resizable
        >
          <vxe-table-column
            v-for="(item, index) in column"
            :key="item.prop + index"
            :align="item.align"
            :field="item.prop"
            :show-overflow-tooltip="item.showtooltip"
            :title="item.label"
            :min-width="item.width"
            header-align="center"
          >
            <template slot-scope="scope">
                <span v-if="item.prop === 'beCode'">
                <span>{{ scope.row[item.prop] | frequencyFilter(that) }}</span>
               </span>
              <div v-else-if="item.prop === 'fundName'">
                <span style="color: red;font-weight: 800;" v-if="scope.row['starWishFlagCode'] == '1'">*</span>
                <span>{{ scope.row[item.prop] | noDataFilter }}</span>
              </div>
              <span v-else>{{ scope.row[item.prop] | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column label="操作" align="center" width="300px" fixed="right">
            <template slot-scope="scope">
              <span class="table-operation">
                <el-button v-if="scope.row.source == '私有'" type="info" plain size="small" @click="handleEditFund(scope.row)">编辑</el-button>
                <el-button v-btn="'examineupdate'" v-else type="info" plain size="small" @click="handleEditFund(scope.row)">编辑</el-button>
                <el-button v-if="scope.row.source == '私有'" type="info" plain size="small" @click="handleAssess(scope.row)">估值模板配置</el-button>
                <el-button v-btn="'examineconfigure'" v-else type="info" plain size="small" @click="handleAssess(scope.row)">估值模板配置</el-button>
                <el-button v-if="scope.row.source == '私有'" type="info" plain size="small" @click="handleDeleteFund(scope.row)">删除</el-button>
                <el-button v-btn="'examinedelete'" v-else type="info" plain size="small" @click="handleDeleteFund(scope.row)">删除</el-button>
                <!--            <el-button type="primary" size="small" @click="jumpToSYCPBG(scope.row)">查看报告</el-button>-->
              </span>
            </template>
          </vxe-table-column>
        </vxe-table>
        <div id="private-product-pg" class="table-footer">
          <Pagination :total="total" :limit="pageList._pageSize" :page="pageList._pageNum" @pagination="pagination" />
        </div>
      </div>
    </div>
    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :destroy-on-close="true"
      width="55%"
      custom-class="customClass"
      @close="closeDialog"
    >
      <assess-template :cur-assess-row="curAssessRow" :tempate-options="tempateOptions" @closeDialog="closeDialog"></assess-template>
    </el-dialog>
    <el-dialog
      v-if="dialogVisibleEdit"
      :title="dialogTitleEdit"
      :visible.sync="dialogVisibleEdit"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      custom-class="customClass"
      @close="closeDialog"
    >
      <edit-product
        v-if="dialogVisibleEdit"
        :is-manager="isManager"
        :cur-fund-row="curFundRow"
        :type-detail-options="typeDetailOptions"
        :fty-pein-options="ftyPeinOptions"
        :invest-options="investOptions"
        :invest-detail-options="investDetailOption"
        :is-tier-options="isTierOptions"
        :yx-status-options="yxStatusOptions"
        :gz-frequency-options="gzFrequencyOptions"
        :source-type-options="sourceTypeOptions"
        :star-wish-options="starWishOptions"
        :companies-options="companiesOptions"
        :fund-typein-options="fundTypeinOptions"
        :fund-base="fundBase"
        :is-edit="isEdit"
        @closeDialog="closeDialog"
      ></edit-product>
    </el-dialog>
  </div>
</template>

<script>
import { TABLE_COLUMNS } from './scripts/constants'
import Pagination from '@/components/Pagination'
import AssessTemplate from './components/assess-template'
import editProduct from './components/edit-product'
import { allOptionsList, deleteTableList, queryTableList } from './scripts/api'
import { downLoadFileByUrl } from '@/utils'
import commonFun from '@/filters/common.js' // global js
export default {
  name: 'PrivateProduct',
  components: {
    Pagination,
    AssessTemplate,
    editProduct
  },
  filters: {
    frequencyFilter(val, that) {
      const obj = that.fundBase.find((item) => item.beCode === val)
      return obj && obj.beName
    }
  },
  data() {
    return {
      that: this,
      // form表单绑定
      formInline: {
        fundCode: '',
        fundName: '',
        strategyList: '',
        subStrategyList: '',
        typeDetailList: '',
        nameGlr: '',
        fundManage: '',
        source: '',
        starWishFlag:'',
        date: [],
        orderString: ''
      },
      // 表格高度
      tableHeight: 0,
      // 表格loading
      tableLoading: false,
      // 表格数据
      tableData: [],
      // 表格列
      column: TABLE_COLUMNS,
      // 策略类型下拉
      investOptions: [],
      // 是否分级下拉
      isTierOptions: [
        {
          dimCde: 0,
          dimNme: '否'
        },
        {
          dimCde: 1,
          dimNme: '是'
        }
      ],
      // 子策略类型下拉所有数据
      investDetailOption: [],
      // 子策略类型下拉
      investDetailOptions: [],
      // 产品类型明细下拉
      typeDetailOptions: [],
      // 产品类型下拉
      ftyPeinOptions: [],
      // 数据来源下拉
      sourceTypeOptions: [],

      //产品属性下拉
      starWishOptions:[],
      // 净值披露频率下拉
      gzFrequencyOptions: [],
      // 产品募集方式下拉
      fundTypeinOptions: [],
      // 模板配置下拉
      tempateOptions: [],
      // 运行状态下拉
      yxStatusOptions: [],
      // 所属机构下拉
      companiesOptions: [],
      // 基准编码
      fundBase: [],
      // 分页信息
      pageList: {
        _pageSize: 20,
        _pageNum: 1,
        _pageFlag: true
      },
      // 总条数
      total: 0,
      // 模板配置弹窗标题
      dialogTitle: '',
      // 模板配置弹窗状态
      dialogVisible: false,
      // 编辑弹窗标题
      dialogTitleEdit: '',
      // 编辑弹窗状态
      dialogVisibleEdit: false,
      // 当前估值模板配置行数据
      curAssessRow: {},
      // 当前产品编辑行数据
      curFundRow: {},
      isManager: false,
      // 新增 | 编辑状态
      isEdit: false,
      exportButton2: false, // 导出
      exportIcon2: 'el-icon-download',
      exportText2: '导出'
    }
  },
  mounted() {
    this.initData()
  },
  beforeDestroy() {
    // 组件销毁移除监听事件
    window.onresize = null
  },
  methods: {
    // 排序的公共方法
    customSortMethod(val) {
      this.formInline.orderString = commonFun.queryOrderBy_vxe_template(val)
      this.handleSearchTable(false)
    },
    jumpToSYCPBG(row) {
      this.$router.push({
        path: '/thgl/jxbg/sycpbg'
      })
      this.$bus.$emit('fromPageJumpSYCP', row)
      this.$store.commit('SET_FROMPAGEJUMPSYCP', true)
    },
    /**
     * @description 初始化数据
     */
    initData() {
      // 动态设置表格高度
      this.handleTableHeight()
      // 查询表格
      this.handleSearchTable()
      // 初始化下拉查询
      this.getDimOptions()
    },
    /**
     * @description 获取所有下拉信息
     */
    getDimOptions() {
      const data = {}
      allOptionsList(data).then((res) => {
        if (res.data.status === 0) {
          const resutData = res.data.data.edims || []
          this.companiesOptions = res.data.data.companies
          this.tempateOptions = res.data.data.templates
          this.fundBase = res.data.data.jzbm
          this.isManager = res.data.data.isManager
          //console.log(resutData)
          if (resutData && resutData.length) {
            this.investOptions = resutData.filter((item) => item.dimType === 'strategy_type')
            this.investDetailOption = resutData.filter((item) => item.dimType === 'fundinvesttype')
            this.typeDetailOptions = resutData.filter((item) => item.dimType === 'VCTYPEDETAIL')
            this.yxStatusOptions = resutData.filter((item) => item.dimType === 'RUNNINGSTATE')
            this.ftyPeinOptions = resutData.filter((item) => item.dimType === 'ftypein')
            this.sourceTypeOptions = resutData.filter((item) => item.dimType === 'SOURCETYPE')
            this.gzFrequencyOptions = resutData.filter((item) => item.dimType === 'gzFrequency')
            this.fundTypeinOptions = resutData.filter((item) => item.dimType === 'fund_type_in')
            this.starWishOptions = resutData.filter((item) => item.dimType === 'FOFSTARWISH_GF')
          }
        }
      })
    },
    // 监听策略类型
    handleChange(value) {
      this.formInline.subStrategyList = ''
      this.investDetailOptions = this.investDetailOption.filter((item) => item.dimEdit === value)
    },

    /**
     * @description 去除无值字段，包含数组
     */
    parameterSrc(data) {
      const newData = {}
      for (const key in data) {
        if (data[key] === '' || data[key] === undefined || data[key] === null || JSON.stringify(data[key]) === '[]') {
        } else {
          newData[key] = data[key]
        }
      }
      return newData
    },
    /**
     * @description 动态设置表格高度
     */
    handleTableHeight() {
      this.$nextTick(() => {
        // 根据浏览器高度设置初始高度
        this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 185
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 185
        }
      })
    },
    /**
     * @description 表格查询
     */
    handleSearchTable() {
      const params = Object.assign({}, this.formInline)
      if (this.formInline.date && this.formInline.date.length) {
        params.createDateBegin = this.formInline.date[0]
        params.createDateEnd = this.formInline.date[1]
      } else {
        params.createDateBegin = ''
        params.createDateEnd = ''
      }
      params.limit = this.pageList._pageSize
      params.offset = (this.pageList._pageNum - 1) * this.pageList._pageSize
      delete params.date
      const data = this.parameterSrc(params)
      this.tableLoading = true
      this.tableData = []
      queryTableList(data)
        .then((res) => {
          if (res.data.status === 0) {
            this.tableData = res.data.data.rows || []
            console.log('tableData', this.tableData)
            this.total = res.data.data.total || 0
            this.tableLoading = false
          } else {
            this.tableLoading = false
            this.$message({
              type: 'error',
              message: res.data.message || '查询失败',
              customClass: 'message-error'
            })
          }
        })
        .catch((e) => {
          this.tableLoading = false
        })
    },
    // 导出数据
    exportData() {
      this.exportButton2 = true
      this.exportIcon2 = 'el-icon-loading'
      this.exportText2 = '导出数据中...'
      const params = Object.assign({}, this.formInline)
      if (this.formInline.date && this.formInline.date.length) {
        params.createDateBegin = this.formInline.date[0]
        params.createDateEnd = this.formInline.date[1]
      } else {
        params.createDateBegin = ''
        params.createDateEnd = ''
      }
      params.limit = this.pageList._pageSize
      params.offset = (this.pageList._pageNum - 1) * this.pageList._pageSize
      delete params.date
      const fileName = '产品信息列表-导出.xls'
      const url = 'api/fundinfo/export'
      downLoadFileByUrl(url, params, fileName, this)
      setTimeout(() => {
        this.exportButton2 = false
        this.exportIcon2 = 'el-icon-download'
        this.exportText2 = '导出'
      }, 10000)
    },
    /**
     * @description 监听分页
     */
    pagination(val) {
      const { page, limit } = val
      this.pageList._pageNum = page
      this.pageList._pageSize = limit
      this.handleSearchTable()
    },
    /**
     * @description 关闭弹窗
     */
    closeDialog(status) {
      this.dialogTitle = ''
      this.dialogVisible = false
      this.dialogTitleEdit = ''
      this.dialogVisibleEdit = false
      if (status === 'REFESH') this.handleSearchTable()
    },
    /**
     * @description 删除产品
     */
    handleDeleteFund(row) {
      this.$confirm('是否确定删除当前产品?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          const params = {
            fundCode: row.fundCode
          }
          deleteTableList(params).then((res) => {
            if (res.data.status === 0) {
              this.$message({
                type: 'success',
                message: '删除成功',
                customClass: 'message-success'
              })
              this.handleSearchTable()
            } else {
              this.$message({
                type: 'error',
                message: '删除失败',
                customClass: 'message-error'
              })
            }
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          })
        })
    },
    /**
     * @description 估值模板配置
     */
    handleAssess(row) {
      this.dialogTitle = '估值模板配置'
      this.dialogVisible = true
      this.curAssessRow = JSON.parse(JSON.stringify(row))
      console.log(this.curAssessRow)
    },
    /**
     * @description 新增私有产品
     */
    handleAddFund() {
      this.dialogTitleEdit = '新增'
      this.dialogVisibleEdit = true
      this.isEdit = false
      this.curFundRow = {
        source: '私有'
      }
    },
    /**
     * @description 编辑私有产品
     */
    handleEditFund(row) {
      this.dialogTitleEdit = '编辑'
      this.dialogVisibleEdit = true
      this.curFundRow = JSON.parse(JSON.stringify(row))
      this.isEdit = true
    }
  }
}
</script>
<style lang="scss">
#private-product-pg .pagination-container {
  .el-input {
    width: 100px !important;
  }
}
</style>

<style lang="scss" scoped>
.private-product {
  .search-bar {
    // border-bottom: 1px solid #e1e0e0;
  }

  ::v-deep .el-form-item {
    margin-bottom: 0;
  }

  .color-box {
    display: inline-block;
    height: 30px;
    width: 2px;
    background-color: #e03d3e;
  }

  .title-style {
    color: #e03d3e;
    vertical-align: middle;
    height: 35px;
    line-height: 35px;
    font-size: 16px;
    margin-left: 5px;
    display: inline-block;
  }

  ::v-deep .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }

  ::v-deep .el-button.el-button--mini {
    padding: 7px !important;
  }
}

::v-deep .el-dialog.customClass {
  width: 55% !important;
}
</style>
<style>
.customClass .el-dialog__body .edit-product .el-form {
  width: 100% !important;
}
</style>

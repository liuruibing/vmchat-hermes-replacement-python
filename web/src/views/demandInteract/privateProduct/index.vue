<template>
  <div class="private-product " v-auto-enter>
    <div class="search-bar">
      <el-form :inline="true" ref="formInline" :model="formInline" class="standard-form analyse-page">
        <el-row>
          <el-col :span="24">
            <el-form-item label="">
              <el-input v-model="formInline.fundCode" size="small" placeholder="请输入产品代码"></el-input>
            </el-form-item>
            <el-form-item label="">
              <el-input v-model="formInline.fundName" size="small" placeholder="请输入产品名称"></el-input>
            </el-form-item>
            <el-form-item label="">
              <el-select v-model="formInline.investStrategy" size="small" clearable filterable placeholder="请选择策略类型">
                <el-option v-for="item in investOptions" :key="item.DIMCDE" :label="item.DIMNME" :value="item.DIMCDE" />
              </el-select>
            </el-form-item>
            <el-form-item label="">
              <el-select v-model="formInline.typeDetail2" size="small" clearable filterable placeholder="请选择子策略类型">
                <el-option v-for="item in investDetailOptions" :key="item.DIMCDE" :label="item.DIMNME" :value="item.DIMCDE" />
              </el-select>
            </el-form-item>
            <el-form-item label="">
              <el-select v-model="formInline.typeIn" size="small" clearable filterable placeholder="请选择产品类型">
                <el-option v-for="item in typeInOptions" :key="item.DIMCDE" :label="item.DIMNME" :value="item.DIMCDE" />
              </el-select>
            </el-form-item>
            <el-form-item label="">
              <el-select v-model="formInline.typeDetail" size="small" clearable filterable placeholder="请选择产品明细类型">
                <el-option v-for="item in typeDetailOptions" :key="item.DIMCDE" :label="item.DIMNME" :value="item.DIMCDE" />
              </el-select>
            </el-form-item>
            <el-form-item label="">
              <el-date-picker
                v-model="formInline.date"
                end-placeholder="成立结束日期"
                range-separator="至"
                size="small"
                start-placeholder="成立开始日期"
                type="daterange"
                value-format="yyyy-MM-dd"
              ></el-date-picker>
            </el-form-item>
            <el-form-item label="">
              <el-input v-model="formInline.nameGlr" size="small" placeholder="请输入管理人"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" size="small" icon="el-icon-search" @click="handleSearchTable">查询</el-button>
              <el-button type="primary" size="small" icon="el-icon-plus" @click="handleAddFund">新增</el-button>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </div>
    <!--    <el-row justify="space-around" type="flex">
      <el-col :span="24">
        <div class="page-model-title">
          <div class="title-icon">
            <div class="color-box"></div>
          </div>
          <span class="title-txt">产品列表</span>
        </div>
      </el-col>
    </el-row>-->
    <el-row id="standard-table">
      <div id="standard-table-margin">
        <vxe-table
          ref="refsTable"
          v-loading="tableLoading"
          :cell-style="{ height: '40px' }"
          :height="tableHeight"
          resizable
          :data="tableData"
          auto-resize
          stripe
          sync-resize
          show-overflow="tooltip"
          style="width: 100%"
        >
          <vxe-table-column
            v-for="item in column"
            :key="item.prop"
            :align="item.align"
            :field="item.prop"
            :show-overflow-tooltip="item.showtooltip"
            :title="item.label"
            :min-width="item.width"
            header-align="center"
          >
            <template slot-scope="scope">
              <span v-if="item.prop === 'gzFrequency'">
                <span>{{ scope.row[item.prop] | frequencyFilter(that) }}</span>
              </span>
              <span v-else>{{ scope.row[item.prop] | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column label="操作" align="center" width="440px">
            <template slot-scope="scope">
              <div style="text-align: left;" class="table-operation">
                <el-button v-if="scope.row.isqx == '1'" size="small" type="info" plain @click="handleEditFund(scope.row)">编辑</el-button>
                <el-button v-if="scope.row.isqx == '1'" size="small" type="info" plain @click="handleDeleteFund(scope.row)">删除</el-button>
<!--                <el-button type="info" size="small" plain @click="handleAssess(scope.row)">估值模板配置</el-button>-->
                <el-button type="info" size="small" plain @click="jumpToSYCPBG(scope.row)">查看报告</el-button>
                <el-button v-if="scope.row.isqx == '1'" type="info" plain size="small" @click="handleZtrees(scope.row)">授权</el-button>
              </div>
            </template>
          </vxe-table-column>
        </vxe-table>
        <vxe-pager
          :current-page="pageList._pageNum"
          :page-size="pageList._pageSize"
          :total="total"
          :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
          border
          size="medium"
          class="standard-vxe-pager"
          @page-change="pagination"
        />
        <!--        <Pagination :total="total" :limit="pageList._pageSize" :page="pageList._pageNum" @pagination="pagination" />-->
      </div>
    </el-row>

    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" :close-on-click-modal="false" :close-on-press-escape="false" :destroy-on-close="true" @close="closeDialog">
      <assess-template :curAssessRow="curAssessRow" @closeDialog="closeDialog" :tempateOptions="tempateOptions"></assess-template>
    </el-dialog>
    <el-dialog :title="dialogTitle2" :visible.sync="dialogVisible2" :close-on-click-modal="false" :close-on-press-escape="false" :destroy-on-close="true" @close="closeDialog">
      <userZtrees :curZtreesRow="curZtreesRow" @closeDialog="closeDialog"></userZtrees>
    </el-dialog>
    <el-dialog
      v-if="dialogVisibleEdit"
      :title="dialogTitleEdit"
      :visible.sync="dialogVisibleEdit"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      @close="closeDialog"
      custom-class="customClass"
    >
      <edit-product
        @closeDialog="closeDialog"
        :curFundRow="curFundRow"
        :typeDetailOptions="typeDetailOptions"
        :typeInOptions="typeInOptions"
        :investOptions="investOptions"
        :investDetailOptions="investDetailOptions"
        :beCodeOptions="beCodeOptions"
        :yxStatusOptions="yxStatusOptions"
        :isEdit="isEdit"
      ></edit-product>
    </el-dialog>
  </div>
</template>

<script>
import { TABLE_COLUMNS } from './scripts/constants'
import Pagination from '@/components/Pagination'
import AssessTemplate from './components/assess-template'
import userZtrees from './components/userZtrees'
import editProduct from './components/edit-product'
import commonApi from '@/api/common'
import { queryTableList, deleteTableList } from './scripts/api'
import { gzFrequencyOptions } from '@/dataDictionary/frequency'
export default {
  name: 'privateProduct',
  components: {
    Pagination,
    AssessTemplate,
    editProduct,
    userZtrees
  },
  data() {
    return {
      that: this,
      // form表单绑定
      formInline: {
        fundCode: '',
        fundName: '',
        investStrategy: '',
        typeDetail2: '',
        typeIn: '',
        typeDetail: '',
        nameGlr: '',
        date: [],
        orderString: 'createTime desc'
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
      // 子策略类型下拉
      investDetailOptions: [],
      // 产品类型下拉
      typeInOptions: [],
      // 产品类型明细下拉
      typeDetailOptions: [],
      // 基准编码下拉
      beCodeOptions: [],
      // 模板配置下拉
      tempateOptions: [],
      // 运行状态下拉
      yxStatusOptions: [],
      // 分页信息
      pageList: {
        _pageSize: 10,
        _pageNum: 1,
        _pageFlag: true
      },
      // 总条数
      total: 0,
      // 模板配置弹窗标题
      dialogTitle: '',
      // 授权弹窗标题
      dialogTitle2: '',
      // 模板配置弹窗状态
      dialogVisible: false,
      // 授权弹窗状态
      dialogVisible2: false,
      // 编辑弹窗标题
      dialogTitleEdit: '',
      // 编辑弹窗状态
      dialogVisibleEdit: false,
      // 当前估值模板配置行数据
      curAssessRow: {},
      //当前产品数据
      curZtreesRow: {},
      // 当前产品编辑行数据
      curFundRow: {},
      // 新增 | 编辑状态
      isEdit: false,
      // 净值披露频率字典
      gzFrequencyOptions
    }
  },
  mounted() {
    this.initData()
  },
  filters: {
    frequencyFilter(val, that) {
      const obj = that.gzFrequencyOptions.find(item => item.value === val)
      return obj && obj.label
    }
  },
  methods: {
    jumpToSYCPBG(row) {
      this.$router.push({
        path: '/tzgl/sycpbg'
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
      this.getBeCodeOptions()
      this.getTemplateOptions()
    },
    /**
     * @description 获取模板配置下拉
     */
    getTemplateOptions() {
      const params = {
        indexCode: 'd264a514-e09a-49cd-a54d-8fbad116b758'
      }
      commonApi.getDataBysqlCode(params).then(res => {
        if (res.data.status === 0) {
          this.tempateOptions = res.data.data || []
        }
      })
    },
    /**
     * @description 查询基准编码下拉
     */
    getBeCodeOptions() {
      const params = {
        indexCode: '849a9e9d-b7ca-4c20-9143-81875733a546'
      }
      commonApi.getDataBysqlCode(params).then(res => {
        if (res.data.status === 0) {
          this.beCodeOptions = res.data.data || []
        }
      })
    },
    /**
     * @description 查询字典下拉
     */
    getDimOptions() {
      const params = {
        indexCode: 'a9d3e3c3-b5be-414a-90d9-312b5fc1948d'
      }
      commonApi.getDataBysqlCode(params).then(res => {
        if (res.data.status === 0) {
          const resutData = res.data.data || []
          if (resutData && resutData.length) {
            this.investOptions = resutData.filter(item => item.DIMTYPE === 'strategy_type')
            this.investDetailOptions = resutData.filter(item => item.DIMTYPE === 'fundinvesttype')
            this.typeInOptions = resutData.filter(item => item.DIMTYPE === 'ftypein')
            this.typeDetailOptions = resutData.filter(item => item.DIMTYPE === 'VCTYPEDETAIL')
            this.yxStatusOptions = resutData.filter(item => item.DIMTYPE === 'RUNNINGSTATE')
          }
        }
      })
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
        this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 270
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 270
        }
      })
    },
    /**
     * @description 表格查询
     */
    handleSearchTable() {
      const params = Object.assign({}, this.formInline)
      if (this.formInline.date && this.formInline.date.length) {
        params.createDate = this.formInline.date[0]
        params.createDate2 = this.formInline.date[1]
      } else {
        params.createDate = ''
        params.createDate2 = ''
      }
      params.flag = 'A' // 私有产品页面固定用A
      params.limit = this.pageList._pageSize
      params.offset = (this.pageList._pageNum - 1) * this.pageList._pageSize
      delete params.date
      const data = this.parameterSrc(params)
      this.tableLoading = true
      queryTableList(data)
        .then(res => {
          if (res.data.status === 0) {
            this.tableData = res.data.data.rows || []
            this.total = res.data.data.total || 0
            this.tableLoading = false
          } else {
            this.tableLoading = false
            this.$message.error(res.data.message || '查询失败')
          }
        })
        .catch(e => {
          this.tableLoading = false
        })
    },
    /**
     * @description 监听分页
     */
    pagination(val) {
      /* let { page, limit } = val
      this.pageList._pageNum = page
      this.pageList._pageSize = limit */
      const { currentPage, pageSize } = val
      // 起始页
      this.pageList._pageNum = currentPage
      // 每页数量
      this.pageList._pageSize = pageSize
      this.handleSearchTable()
    },
    /**
     * @description 关闭弹窗
     */
    closeDialog(status) {
      this.dialogTitle = ''
      this.dialogVisible = false
      this.dialogTitle2 = ''
      this.dialogVisible2 = false
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
          deleteTableList(params).then(res => {
            if (res.data.status === 0) {
              this.$message.success(res.data.message || '删除成功')
              this.handleSearchTable()
            } else {
              this.$message.error(res.data.message || '删除失败')
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
    },
    /**
     * @description 授权
     */
    handleZtrees(row) {
      this.dialogTitle2 = '授权'
      this.dialogVisible2 = true
      this.curZtreesRow = JSON.parse(JSON.stringify(row))
    },
    /**
     * @description 新增私有产品
     */
    handleAddFund() {
      this.dialogTitleEdit = '新增'
      this.dialogVisibleEdit = true
      this.isEdit = false
      this.curFundRow = {}
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
  },
  beforeDestroy() {
    // 组件销毁移除监听事件
    window.onresize = null
  }
}
</script>

<style lang="scss" scoped>
.private-product {
  //padding-left: 10px;
  .search-bar {
    margin-top: 12px;
    // border-bottom: 1px solid #e1e0e0;
    margin-left: 10px;
    margin-bottom: 8px;
  }
  ::v-deep .el-form-item {
    margin-bottom: 0;
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
    display: inline-block;
  }
  ::v-deep .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
  ::v-deep .el-button.el-button--mini {
    padding: 7px !important;
  }
}
::v-deep .el-button--danger {
  color: #f56c6c;
  background-color: #fff;
  border-color: #f56c6c;
}
</style>
<style>
div .customClass {
  width: 45% !important;
}
.customClass .el-dialog__body .edit-product .el-form {
  width: 100% !important;
}
</style>

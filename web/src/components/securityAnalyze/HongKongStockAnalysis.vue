<template>
  <div class="HongKongStockAnalysis">
    <el-row :gutter="20">
      <el-col :span="24">
        <div class="forms_table_title" ><i class="el-icon-s-data"></i>港股持仓列表
          <hint  hintName = "" dimCode = "GP_GGLB" dimType = "indexHelp"></hint></div>
        <el-form :inline="true" ref="formQuery" :model="formQuery" :rules="rules" class="mb10">
          <el-row>
            <el-col :span="18">
              <el-form-item label="日期" prop="dDate" class="mb20">
                <el-date-picker
                  size="small"
                  v-model="formQuery.dDate"
                  type="date"
                  value-format="yyyy-MM-dd"
                  :picker-options="this.$fun.dateShortDot()"
                  placeholder="选择日期">
                </el-date-picker>
                <span class="dateHint_text">{{$store.state.setting.dateHint}}</span>
              </el-form-item>
              <el-form-item label="投资经理" prop="account" v-if="isAccount">
                <el-select size="small" v-model="formQuery.account" filterable clearable placeholder="请选择">
                  <el-option
                    v-for="(item, index) in manageArr"
                    :key="index"
                    :label="item.userName"
                    :value="item.account">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="组合类型" prop="fundTypes" v-if="isFundType">
                <el-select size="small" v-model="formQuery.fundTypes" multiple placeholder="请选择" >
                  <el-option
                    v-for="(group, index) in groupTypeArr"
                    :value="group.dimCde"
                    :key="index"
                    :label="group.dimNme">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="区间" prop="range">
                <el-select v-model="formQuery.range" clearable placeholder="请选择"  size="small">
                  <template v-for="(item, index) in regionArrs">
                    <el-option :label="item.dimNme" :value="item.dimCde" :key="item.dimCde"></el-option>
                  </template>
                </el-select>
              </el-form-item>
              <el-form-item label="股票代码/股票名称" prop="searchParam">
                <el-input v-model="formQuery.searchParam" placeholder="请输入" size="small"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item class="search_button_com">
                <el-button type="primary" size="small" :disabled="btnDisabled" @click="onQuery(1)">查询</el-button>
                <el-button plain size="small" @click="resetForm('formQuery')">重置</el-button>
                <el-button @click="downloadTableExcel" type="primary" plain :icon="downLoadIcon" :disabled="isDisabled" size="small">{{downLoadText}}</el-button>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>

        <div class="bond_title_box">
          <div class="bond_inline">
            港股资产规模 : <span>{{HongKongSummary.sumPrice | moneyMillion}}万元</span>
          </div>
          <div class="bond_inline">
            占资产净值比 : <span>{{HongKongSummary.netValueRatio | ratioThousand}}%</span>
          </div>
          <div class="bond_inline">
            数据日期 : <span>{{HongKongSummary.dateTime || '--'}}</span>
          </div>
        </div>
        <!--列表-->
        <el-table
          :data="tableData"
          :default-sort="{prop: 'amount', order: 'descending'}"
          stripe
          border
          @row-click="rowClick"
          @sort-change="handleSortChange"
          v-loading="tableLoading"
          style="width: 100%">
          <el-table-column
            type="index"
            label="序号"
            width="60"
            header-align="center">
          </el-table-column>
          <el-table-column
            prop="symbol"
            show-overflow-tooltip
            sortable
				    :sort-orders="['ascending', 'descending']"
            label="股票代码"
            min-width="120"
            header-align="center">
            <template slot-scope="scope">
              <span class="blue">{{scope.row.symbol}}</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="symbolName"
            sortable
				    :sort-orders="['ascending', 'descending']"
            show-overflow-tooltip
            label="股票名称"
            min-width="120"
            header-align="center">
            <template slot-scope="scope">
              <span class="blue">{{scope.row.symbolName}}</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="amount"
            show-overflow-tooltip
            sortable
				    :sort-orders="['ascending', 'descending']"
            label="持仓量(股)"
            min-width="140"
            header-align="center"
            align="right">
            <template slot-scope="scope">
              {{scope.row.amount | moneyYuan}}
            </template>
          </el-table-column>
          <el-table-column
            prop="price"
            show-overflow-tooltip
            sortable
				    :sort-orders="['ascending', 'descending']"
            label="持仓市值(万元)"
            min-width="170"
            header-align="center"
            align="right">
            <template slot-scope="scope">
              {{scope.row.price | moneyMillion}}
            </template>
          </el-table-column>
          <el-table-column
            prop="ratio"
            show-overflow-tooltip
            sortable
				    :sort-orders="['ascending', 'descending']"
            label="占股票资产比例(%)"
            min-width="160"
            header-align="center"
            align="right">
            <template slot-scope="scope">
              {{scope.row.ratio | ratioThousand}}
            </template>
          </el-table-column>
          <el-table-column
            prop="count"
            show-overflow-tooltip
            sortable
				    :sort-orders="['ascending', 'descending']"
            label="持股组合数量"
            min-width="120"
            header-align="center"
            align="right">
            <!-- <template slot-scope="scope">
              {{scope.row.count | moneyYuan}}
            </template> -->
          </el-table-column>
        </el-table>

        <Pagination :total="total" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination"></Pagination>
      </el-col>
    </el-row>

    <el-dialog
      v-el-drag-dialog
      :title="dialogTitle"
      :visible.sync="dialogMask"
      :close-on-click-modal="false">
      <el-table
        :data="dialogTableData"
        :default-sort="{prop: 'price', order: 'descending'}"
        border
        stripe
        @sort-change="handleSortChange2"
        max-height="300"
        style="width: 100%">
        <el-table-column
          prop="symbol"
          show-overflow-tooltip
          sortable
          :sort-orders="['ascending', 'descending']"
          label="股票代码"
          min-width="80"
          header-align="center"
        />
        <el-table-column
          prop="symbolName"
          show-overflow-tooltip
          sortable
          :sort-orders="['ascending', 'descending']"
          label="股票名称"
          min-width="120"
          header-align="center"
        />
        <el-table-column
          prop="fundCode"
          show-overflow-tooltip
          sortable
          :sort-orders="['ascending', 'descending']"
          label="组合代码"
          min-width="80"
          header-align="center"
        />
        <el-table-column
          prop="fundName"
          show-overflow-tooltip
          sortable
          :sort-orders="['ascending', 'descending']"
          label="组合名称"
          min-width="80"
          header-align="center"
        />
        <el-table-column
          prop="amount"
          show-overflow-tooltip
          sortable
          :sort-orders="['ascending', 'descending']"
          label="持仓量"
          min-width="80"
          header-align="center"
          align="right"
        >
          <template slot-scope="scope">
            {{scope.row.amount | moneyYuan}}
          </template>
        </el-table-column>
        <el-table-column
          prop="price"
          show-overflow-tooltip
          sortable
          :sort-orders="['ascending', 'descending']"
          label="持仓市值(万元)"
          min-width="90"
          header-align="center"
          align="right"
        >
          <template slot-scope="scope">
            {{scope.row.price | moneyMillion}}
          </template>
        </el-table-column>
        <el-table-column
          prop="investManager"
          show-overflow-tooltip
          sortable
          :sort-orders="['ascending', 'descending']"
          label="投资经理"
          min-width="80"
          header-align="center"
        />
      </el-table>
    </el-dialog>

  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import commonApi from '@/api/common'
import investmentManagerApi from '@/api/managementView/investmentManager'
import { selectHkAnalysisUrl, hkAnalysisDetailsUrl } from '@/api/securitiesAnalysis'
import hint from '@/components/hint'
export default {
  name: "hong-kong-stock-analysis",
  components: {
    Pagination,hint
  },
  props: {
    // 是否显示投资经理下拉
    isAccount: {
      type: Boolean,
      default: true
    },
    // 组合代码
    fundCode: {
      default: ''
    },
    // 日期
    date: {
      default: ''
    },
    // 是否显示组合类型
    isFundType: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      // 查询参数
      formQuery:{
        // 日期
        dDate:'',
        // 组合类型
        fundTypes: [],
        // 投资经理
        account: '',
        // 区间
        range:'',
        // 股票代码/股票名称
        searchParam: '',
        // 组合代码
        fundCode: '',
        // 排序字段
        orderBy: '"amount" desc nulls last',
        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10
      },
      // 组合类型数组
      groupTypeArr: [],
      // 投资经理数组
      manageArr: [],
      // 区间数组
      regionArrs: [],
      // 验证规则
      rules: {
        // 日期
        dDate: [
          { type: 'string', required: true, message: '请选择日期', trigger: 'change' }
        ],
        // 投资经理
        account: [
          { type: 'string', required: true, message: '请选择投资经理', trigger: 'change' }
        ]
        // 组合类型
        // fundTypes: [
        //   { type: 'array', required: true, message: '请选择组合类型', trigger: 'change' }
        // ],
        // 区间
        // range: [
        //   { type: 'string', required: true, message: '请选择区间', trigger: 'change' }
        // ],
      },
      // 证券分析-汇总
      HongKongSummary: {
        // 港股资产规模
        sumPrice: 0,
        // 数据日期
        dateTime: '--',
        // 占资产净值比
        netValueRatio: 0
      },
      // 列表数据
      tableData: [],
      // 总条数
      total: 0,
      // 表格loading
      tableLoading: false,
      /* 按钮禁止与否 */
      isDisabled: false,
      // 导出图标
      downLoadIcon: 'el-icon-download',
      // 导出提示文字
      downLoadText: '导出数据',
      // 弹窗
      dialogMask: false,
      // 标题
      dialogTitle: '',
      // 列表数据
      dialogTableData: [],
      // 查询按钮禁用
      btnDisabled: false,
      // 保存表格传递值
      saveStr: '',
      // 排序字段
      orderStr: `"price" desc nulls last`
    }
  },
  mounted(){
    this.formQuery.fundCode = this.fundCode
    // 今天
    // let today = this.$moment().subtract(1,'days').format('YYYY-MM-DD')
    if (this.date) {
      // 日期
      this.formQuery.dDate = this.date
    } else {
      // 默认时间
      // this.formQuery.dDate = today
      // 接口返回T-1日
      this.formQuery.dDate = this.$store.state.setting.endDate
    }
    // 组合类型
    this.formQuery.fundTypes = ['*']
    // 组合类型查询
    this.getListEdims('fund_type')
    // 港股分析区间查询
    this.getListEdims('range_type')
    if (!this.isAccount) {
      this.formQuery.account = -1
    } else {
      // 投资经理列表查询
      this.getManagerList()
    }
    // 是否默认查询
    if (this.$store.state.setting.isOnQuery) {
      this.$nextTick(() => {
        let timer = setTimeout(() => {
          // 查询
          this.onQuery()
          clearTimeout(timer)
        }, 1000)
      })
    }
  },
  methods: {
    // 查询
    onQuery(page){
      this.$refs['formQuery'].validate((valid) => {
        if (valid) {
          // 禁用搜索按钮
          this.$fun.searchButtonDisabled("btnDisabled", this)
          // 重置起始页
          if (page) this.formQuery.pageNum = 1
          // 证券分析-港股分析
          this.getSelectHkAnalysis()
        }
      })
    },
    // 清除
    resetForm (formName) {
      this.$refs[formName].resetFields()
    },
    // 下拉列表查询
    getListEdims (type) {
      // 字典类型
      let params = type
      commonApi.edimsCommon(params).then(res => {
        let { status, data } = res.data
        if (status === 0) {
          // 组合类型查询
          if (type === 'fund_type') this.groupTypeArr = data
          // 港股分析区间查询
          if (type === 'range_type') {
            this.regionArrs = data
            if (this.regionArrs.length) this.formQuery.range = this.regionArrs[0].dimCde
          }
        }
      })
    },
    // 投资经理列表查询
    getManagerList () {
      // 权益（1）/固收（2）/混合（0）
      // 港股分析只可以选权益经理
      let params = 1
      investmentManagerApi.managerList(params).then(res => {
        let { status, data } = res.data
        if (status === 0) {
          this.manageArr = data
          if (this.manageArr.length) this.formQuery.account = this.manageArr[0].account
        }
      })
    },
    // 页面点击事件
    pagination (val) {
      let { page, limit } = val
      // 起始页
      this.formQuery.pageNum = page
      // 每页数量
      this.formQuery.pageSize = limit
      // 查询
      this.$refs['formQuery'].validate((valid) => {
        if (valid) {
					// 证券分析-港股分析
          this.getSelectHkAnalysis()
        }
      })
    },
    // 证券分析-港股分析
    getSelectHkAnalysis (flag) {
      if (!flag) {
        this.tableLoading = true
      } else {
        if (this.isDisabled) return
        this.isDisabled = true
        this.downLoadIcon = 'el-icon-loading'
        this.downLoadText = '导出数据中...'
      }
      let params = Object.assign({}, this.formQuery, {
        fundTypes: this.formQuery.fundTypes.join(',')
      })
      if (flag) {
        params.pageNum = 1
        params.pageSize = 5000
        params.ex_tmp_name = '港股分析.xls'
      }
      // 清除空字段
			for (let k in params) {
				if (!params[k] && String(params[k]) !== '0') {
					delete params[k]
				}
			}
      selectHkAnalysisUrl(params).then(res => {
        this.tableLoading = false
        this.isDisabled = false
        this.downLoadIcon = 'el-icon-download'
        this.downLoadText = '导出数据'
        let { status, data } = res
        if (status === 0) {
          if (flag) { // 下载excel
            if (!data) return
					  this.$fun.commonDownloadUrl(data)
          } else {
            let { list,  total } = data
            this.tableData = list
            this.total = total
            if (list.length) {
              this.HongKongSummary.sumPrice = list[0].sumPrice || 0
              this.HongKongSummary.netValueRatio = list[0].netValueRatio || 0
              this.HongKongSummary.dateTime = this.formQuery.dDate
            } else {
              this.HongKongSummary.sumPrice = 0
              this.HongKongSummary.netValueRatio = 0
              this.HongKongSummary.dateTime = '--'
            }
          }
        }
      }).catch(() => {
        this.tableLoading = false
        this.isDisabled = false
        this.downLoadIcon = 'el-icon-download'
        this.downLoadText = '导出数据'
      })
    },
    // 证券分析-港股分析详情
    getHkAnalysisDetails (symbolCodeName) {
      let params = {
        // 开始时间
        beginDate: this.formQuery.dDate,
        // 组合名称/代码
        symbolCodeName: symbolCodeName,
        // 投资经理账户
        account: this.formQuery.account,
        // 组合代码
        fundCode: this.formQuery.fundCode,
        // 排序字段
        orderStr: this.orderStr
      }
      // 清除空字段
			for (let k in params) {
				if (!params[k] && String(params[k]) !== '0') {
					delete params[k]
				}
			}
      hkAnalysisDetailsUrl(params).then(res => {
        let { status, data } = res
        if (status === 0) {
          this.dialogTableData = data
        }
      })
    },
    // 当某一行被点击时会触发该事件
    rowClick (row, column, event) {
      // 当点击的是股票代码/股票名称显示弹窗
      if (column.property === 'symbol'
            || column.property === 'symbolName'
      ) {
        if (!event.target.textContent) return
        // 显示弹窗
        this.dialogMask = true
        // 标题
        this.dialogTitle = `${row.symbol || '未知代码'}-${row.symbolName || '未知名称'}`
        // 保存表格传递值
        this.saveStr = row.symbol
        // 证券分析-港股分析详情
        this.getHkAnalysisDetails(row.symbol)
      }
    },
    // 当表格的排序条件发生变化的时候会触发该事件
    handleSortChange (val) {
      if (val.order === 'ascending') {
        this.formQuery.orderBy = `"${val.prop}" nulls last` // 升序
      } else {
        this.formQuery.orderBy = `"${val.prop}" desc nulls last` // 降序
      }
      // 查询
      this.onQuery()
    },
    // 当表格的排序条件发生变化的时候会触发该事件
    handleSortChange2 (val) {
      if (val.order === 'ascending') {
        this.orderStr = `"${val.prop}" nulls last` // 升序
      } else {
        this.orderStr = `"${val.prop}" desc nulls last` // 降序
      }
      // 证券分析-港股分析详情
      this.getHkAnalysisDetails(this.saveStr)
    },
    // 表格导出excel
    downloadTableExcel () {
      this.$refs['formQuery'].validate((valid) => {
        if (valid) {
          // 证券分析-港股分析（导出excel）
          this.getSelectHkAnalysis(true)
        }
      })
    }
  },
  watch: {
    // 监听组合类型变化
    'formQuery.fundTypes' (val, oldval) {
      if (val.indexOf('*') != -1 && oldval.indexOf('*') == -1 && val.length > 1) {
        this.formQuery.fundTypes = ['*']
      } else if (val.indexOf('*') != -1 && oldval.indexOf('*') != -1 && val.length > 1){
        this.formQuery.fundTypes.splice(val.indexOf('*'), 1)
      }
    },
    // 监听组合代码变化
    fundCode () {
      this.formQuery.fundCode = this.fundCode
      // 查询
      this.onQuery()
    }
  }
}
</script>

<style lang="scss">
.HongKongStockAnalysis{
  .blue{
    color: #409EFF;
    cursor: pointer;
  }
  .el-dialog{
		width: 70%!important;
	}
}
</style>

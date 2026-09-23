<template>
  <div class="depositAnalysis">
    <div class="forms_table_title"><i class="el-icon-s-data"></i>存款分析
      <hint  hintName = "" dimCode = "CK_CKLB" dimType = "indexHelp"></hint></div>
    <!-- 搜索 -->
    <el-form :inline="true" ref="formQuery" :model="formQuery" :rules="rules" style="margin-bottom: 10px">
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
                v-for="item in manageArr"
                :key="item.account"
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
          <el-form-item label="类型" prop="depositTypes">
            <el-select v-model="formQuery.depositTypes" multiple placeholder="请选择"  size="small">
              <template v-for="(item, index) in typeArr">
                <el-option :label="item.dimNme" :value="item.dimCde" :key="index"></el-option>
              </template>
            </el-select>
          </el-form-item>
          <el-form-item label="存款银行" prop="bankName">
            <el-input v-model="formQuery.bankName" placeholder="请输入" size="small"></el-input>
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

    <!-- <div class="fundList_total_box">
      <div class="money">汇总金额：<span>{{totalMoney}}万元</span></div>
    </div> -->
    <div class="bond_title_box">
      <div class="bond_inline">
        存款资产规模 : <span>{{depositSummary.sumPrice | moneyMillion}}万元</span>
      </div>
      <div class="bond_inline">
        占资产净值比 : <span>{{depositSummary.netValueRatio | ratioThousand}}%</span>
      </div>
      <div class="bond_inline">
        数据日期 : <span>{{depositSummary.dateTime || '--'}}</span>
      </div>
    </div>
    <!--列表-->
    <el-table
      :data="tableData"
      :default-sort="{prop: 'startDate', order: 'descending'}"
      :span-method="arraySpanMethod"
      stripe
      border
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
        prop="fundType"
        sortable
				:sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="组合类型"
        min-width="90"
        header-align="center">
      </el-table-column>
      <el-table-column
        prop="fundCode"
        sortable
				:sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="组合代码"
        min-width="80"
        header-align="center">
      </el-table-column>
      <el-table-column
        prop="fundName"
        sortable
				:sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="组合名称"
        min-width="120"
        header-align="center">
      </el-table-column>
      <el-table-column
        prop="qyManage"
        show-overflow-tooltip
        label="权益投资经理"
        min-width="100"
        header-align="center">
      </el-table-column>
      <el-table-column
        prop="gsManage"
        show-overflow-tooltip
        label="固收投资经理"
        min-width="100"
        header-align="center">
      </el-table-column>
      <el-table-column
        prop="receiptNo"
        show-overflow-tooltip
        label="存款号"
        min-width="100"
        header-align="center">
      </el-table-column>
      <el-table-column
        prop="depositType"
        show-overflow-tooltip
        label="存款类型"
        min-width="100"
        header-align="center">
      </el-table-column>
      <el-table-column
        prop="price"
        sortable
				:sort-orders="['ascending', 'descending']"
        label="金额(万元)"
        min-width="90"
        header-align="center"
        align="right">
        <template slot-scope="scope">
          {{scope.row.price | moneyMillion}}
        </template>
      </el-table-column>
      <el-table-column
        prop="rate"
        sortable
				:sort-orders="['ascending', 'descending']"
        label="利率(%)"
        min-width="80"
        header-align="center"
        align="right">
        <template slot-scope="scope">
          {{scope.row.rate | ratioThousand}}
        </template>
      </el-table-column>
      <el-table-column
        prop="bank"
        sortable
				:sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="存款银行"
        min-width="140"
        header-align="center">
      </el-table-column>
      <el-table-column
        prop="startDate"
        sortable
				:sort-orders="['ascending', 'descending']"
        label="存款日"
        min-width="90"
        header-align="center">
      </el-table-column>
      <el-table-column
        prop="endDate"
        sortable
				:sort-orders="['ascending', 'descending']"
        label="到期日"
        min-width="90"
        header-align="center">
      </el-table-column>
    </el-table>

    <Pagination :total="total" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination"></Pagination>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import commonApi from '@/api/common'
import investmentManagerApi from '@/api/managementView/investmentManager'
import {
  selectCoincidenceAnalysisUrl
} from '@/api/securitiesAnalysis'
import { moneyMillion } from '@/filters'
import hint from '@/components/hint'
export default {
  name: "deposit-analysis",
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
      // 查询条件
      formQuery: {
        // 日期
        dDate:'',
        // 组合类型
        fundTypes: [],
        // 投资经理
        account: '',
        // 存款类型
        depositTypes: [],
        // 组合代码
        fundCode: '',
        // 存款银行
        bankName: '',
        // 排序字段
        orderBy: '"startDate" desc nulls last',
        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10
      },
      // 组合类型数组
      groupTypeArr: [],
      // 投资经理数组
      manageArr: [],
      // 验证规则
      rules:{
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
        // 存款类型
        // depositTypes: [
        //   { type: 'array', required: true, message: '请选择存款类型', trigger: 'change' }
        // ],
      },
      // 类型数组
      typeArr: [],
      // 证券分析-汇总
      depositSummary: {
        // 存款资产规模
        sumPrice: 0,
        // 数据日期
        dateTime: '--',
        // 占资产净值比
        netValueRatio: 0
      },
      // 数据列表
      tableData: [],
      // 总条数
      total: 0,
      // 合计
      totalMoney: 0,
      // 表格loading
      tableLoading: false,
      /* 按钮禁止与否 */
      isDisabled: false,
      // 导出图标
      downLoadIcon: 'el-icon-download',
      // 导出提示文字
      downLoadText: '导出数据',
      // 排序字段 降序
      order: 'descending',
      // 查询按钮禁用
      btnDisabled: false
    }
  },
  mounted () {
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
    // 存款类型
    this.formQuery.depositTypes = ['*']
    // 组合类型列表查询
    this.getListEdims('fund_type')
    // 存款类型列表查询
    this.getListEdims('deposit_type')
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
          // 证券分析-存款分析
          this.selectCoincidenceAnalysis()
        }
      })
    },
    // 清除
    resetForm (formName) {
      this.$refs[formName].resetFields()
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
					// 证券分析-存款分析
          this.selectCoincidenceAnalysis()
        }
      })
    },
    // 组合类型列表查询
    getListEdims (type) {
      // 字典类型
      let params = type
      commonApi.edimsCommon(params).then(res => {
        let { status, data } = res.data
        if (status === 0) {
          // 组合类型
          if (type === 'fund_type') this.groupTypeArr = data
          // 存款类型
          if (type === 'deposit_type') this.typeArr = data
        }
      })
    },
    // 投资经理列表查询
    getManagerList () {
      // 权益（1）/固收（2）/混合（0）
      // 存款分析只可以选固收经理
      let params = 2
      investmentManagerApi.managerList(params).then(res => {
        let { status, data } = res.data
        if (status === 0) {
          this.manageArr = data
          if (this.manageArr.length) this.formQuery.account = this.manageArr[0].account
        }
      })
    },
    // 证券分析-存款分析
    selectCoincidenceAnalysis (flag) {
      if (!flag) {
        this.tableLoading = true
      } else {
        if (this.isDisabled) return
        this.isDisabled = true
        this.downLoadIcon = 'el-icon-loading'
        this.downLoadText = '导出数据中...'
      }
      let params = Object.assign({}, this.formQuery, {
        fundTypes: this.formQuery.fundTypes.join(','),
        depositTypes: this.formQuery.depositTypes.join(',')
      })
      if (flag) {
        params.pageNum = 1
        params.pageSize = 5000
        params.ex_tmp_name = '存款分析.xls'
      }
      // 清除空字段
			for (let k in params) {
				if (!params[k] && String(params[k]) !== '0') {
					delete params[k]
				}
			}
      selectCoincidenceAnalysisUrl(params).then(res => {
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
            // 增加合计行
            // let money = 0
            // if (list.length) {
            //   money = list[0].sum || 0
            //   money = moneyMillion(money)
            // }
            // this.totalMoney = money
            if (list.length) {
              this.depositSummary.sumPrice = list[0].sumPrice || 0
              this.depositSummary.netValueRatio = list[0].netValueRatio || 0
              this.depositSummary.dateTime = this.formQuery.dDate
            } else {
              this.depositSummary.sumPrice = 0
              this.depositSummary.netValueRatio = 0
              this.depositSummary.dateTime = '--'
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
    /**
     * 表格合并
     * @param {*} param0
     * row 表格每一行的数据
     * column 表格每一列的数据
     * rowIndex 表格的行索引,不包括表头,从0开始
     * columnIndex 表格的列索引,从0开始
     */
    arraySpanMethod({ row, column, rowIndex, columnIndex }) {
      // if (rowIndex === 0) { // 合并第1行
      if (row.dataOrder === 1) { // 如果有自定义字段
        if (columnIndex === 0) { // 从第1列开始
          return [1, 2]
        } else if (columnIndex === 1) {
          return [0, 0]
        } else if (columnIndex === 2) {
          return [1, 7]
        } else {
          return [0, 0]
        }
      }
    },
    // 当表格的排序条件发生变化的时候会触发该事件
    handleSortChange (val) {
      this.order = val.order
      if (val.order === 'ascending') {
        this.formQuery.orderBy = `"${val.prop}" nulls last` // 升序
      } else {
        this.formQuery.orderBy = `"${val.prop}" desc nulls last` // 降序
      }
      // 查询
      this.onQuery()
    },
    // 表格导出excel
    downloadTableExcel () {
      this.$refs['formQuery'].validate((valid) => {
        if (valid) {
          // 证券分析-存款分析（导出excel）
          this.selectCoincidenceAnalysis(true)
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
    },
    // 监听存款类型变化
    'formQuery.depositTypes' (val, oldval) {
      if (val.indexOf('*') != -1 && oldval.indexOf('*') == -1 && val.length > 1) {
        this.formQuery.depositTypes = ['*']
      } else if (val.indexOf('*') != -1 && oldval.indexOf('*') != -1 && val.length > 1){
        this.formQuery.depositTypes.splice(val.indexOf('*'), 1)
      }
    }
  }
}
</script>

<style lang="scss" scoped>
// .depositAnalysis{}
</style>

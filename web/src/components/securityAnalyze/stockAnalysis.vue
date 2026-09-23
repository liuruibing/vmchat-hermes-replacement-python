<template>
  <div class="stockAnalysis">
    <el-form :inline="true" ref="formQuery" :model="formQuery" :rules="rules" class="mb10">
      <el-row>
        <el-col :span="19">
          <el-form-item label="日期" prop="beginDate">
            <el-date-picker
              size="small"
              v-model="formQuery.beginDate"
              type="date"
              value-format="yyyy-MM-dd"
              :picker-options="this.$fun.dateShortDot()"
              @change="handleChangeDate"
              placeholder="选择日期">
            </el-date-picker>
            <span class="dateHint_text">{{$store.state.setting.dateHint}}</span>
          </el-form-item>
          <!-- <el-form-item label="组合类型" prop="fundType">
            <el-select size="small" v-model="formQuery.fundType" multiple placeholder="请选择" >
              <el-option
                v-for="(group, index) in groupTypeArr"
                :value="group.dimCde"
                :key="index"
                :label="group.dimNme">
              </el-option>
            </el-select>
          </el-form-item> -->
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
          <el-form-item label="指数" prop="targetList">
            <el-select v-model="formQuery.targetList" multiple placeholder="请选择"  size="small">
              <template v-for="(item, index) in targetTypes">
                <el-option :label="item.dimNme" :value="item.dimCde" :key="item.dimCde"></el-option>
              </template>
            </el-select>
          </el-form-item>
          <el-form-item label="组合类型" prop="fundType" v-if="isFundType">
            <el-select size="small" v-model="formQuery.fundType" multiple placeholder="请选择" >
              <el-option
                v-for="(group, index) in groupTypeArr"
                :value="group.dimCde"
                :key="index"
                :label="group.dimNme">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="是否包含“不统计权益”组合" prop="isEquity">
            <el-radio v-model="formQuery.isEquity" :label="1" size="small">是</el-radio>
            <el-radio v-model="formQuery.isEquity" :label="0" size="small">否</el-radio>
          </el-form-item>
        </el-col>
        <el-col :span="5">
          <el-form-item class="search_button_com">
            <el-button type="primary" size="small" :disabled="btnDisabled" @click="onQuery()">查询</el-button>
            <el-button plain size="small" @click="resetForm('formQuery')">重置</el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <div class="bond_title_box">
      <div class="bond_inline">
        股票资产规模 : <span>{{stockPriceData.price | moneyMillion}}万元</span>
      </div>
      <div class="bond_inline">
        占资产净值比 : <span>{{stockPriceData.priceRatio | ratioThousand}}%</span>
      </div>
      <div class="bond_inline">
        数据日期 : <span>{{stockPriceData.dateString || '--'}}</span>
      </div>
    </div>

    <!-- 查询 -->
    <el-form :inline="true" ref="formQuery2" :model="formQuery2" :rules="rules2" class="mt10">
      <el-row>
        <el-col :span="19">
          <el-form-item label="区间" prop="rowNumber">
            <el-select v-model="formQuery2.rowNumber" placeholder="请选择"  size="small">
              <template v-for="(item, index) in regionArrs">
                <el-option :label="item.dimNme" :value="item.dimCde" :key="item.dimCde"></el-option>
              </template>
            </el-select>
          </el-form-item>
          <el-form-item label="股票代码或股票名称" prop="searchName">
            <el-input v-model="formQuery2.searchName" placeholder="请输入内容" size="small"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="5">
          <el-form-item class="search_button_com">
            <el-button type="primary" size="small" :disabled="btnDisabled2" @click="onQuery2(1)">查询</el-button>
            <el-button plain size="small" @click="resetForm('formQuery2')">重置</el-button>
            <el-button @click="downloadTableExcel2" type="primary" plain :icon="downLoadIcon2" :disabled="isDisabled2" size="small">{{downLoadText2}}</el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <el-row :gutter="20" class="mr20">
      <!-- <el-col :span="12">
        <div class="border_box">
          <div class="forms_table_title" style="padding-left: 10px;">
            <i class="el-icon-s-marketing"></i>个股占股票资产比例<hint  hintName = "" dimCode = "GP_GPZB" dimType = "indexHelp"></hint>
            <li @click="exportExcelFile3"><el-tooltip content="下载图表数据" placement="top"><i class="el-icon-s-order"></i></el-tooltip></li>
          </div>
          <div id="myEcharts3" class="echarts_box" style="height:321px;" v-loading="myEcharts3Loading && $store.state.setting.loadingShow"></div>
        </div>
      </el-col> -->
      <el-col :span="24">
        <!--列表-->
        <el-table
          :data="tableData2"
          :default-sort="{prop: 'price', order: 'descending'}"
          stripe
          border
          @row-click="rowClick"
          @sort-change="handleSortChange2"
          v-loading="tableLoading2"
          style="width: 100%">
          <el-table-column
            type="index"
            label="序号"
            width="60"
            header-align="center">
          </el-table-column>
          <el-table-column
            prop="symbolCode"
            show-overflow-tooltip
            sortable
				    :sort-orders="['ascending', 'descending']"
            label="代码"
            min-width="120"
            align="center">
            <template slot-scope="scope">
              <span class="blue">{{scope.row.symbolCode}}</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="symbolName"
            sortable
				    :sort-orders="['ascending', 'descending']"
            label="简称"
            min-width="120"
            align="center">
            <template slot-scope="scope">
              <span class="blue">{{scope.row.symbolName}}</span>
            </template>
          </el-table-column>
          <el-table-column
            prop="price"
            sortable
				    :sort-orders="['ascending', 'descending']"
            label="持仓市值(万元)"
            min-width="120"
            align="center">
            <template slot-scope="scope">
              {{scope.row.price | moneyMillion}}
            </template>
          </el-table-column>
          <el-table-column
            prop="priceRatio"
            sortable
				    :sort-orders="['ascending', 'descending']"
            label="占股票资产比例(%)"
            min-width="150"
            align="center">
            <template slot-scope="scope">
              {{scope.row.priceRatio | ratioThousand}}
            </template>
          </el-table-column>
          <el-table-column
            prop="industryName"
            sortable
				    :sort-orders="['ascending', 'descending']"
            label="所属行业"
            min-width="120"
            align="center">
          </el-table-column>
        </el-table>

        <Pagination :total="total2" :limit="formQuery2.pageSize" :page="formQuery2.pageNum" @pagination="pagination"></Pagination>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt30 mr20">
      <el-col :span="12">
        <div class="border_box">
          <div class="forms_table_title pdl10">
            <i class="el-icon-s-marketing"></i>近一年股票仓位<hint  hintName = "" dimCode = "GP_GPCW" dimType = "indexHelp"></hint>
            <li @click="exportExcelFile2"><el-tooltip content="下载图表数据" placement="top"><i class="el-icon-s-order"></i></el-tooltip></li>
          </div>
          <div id="myEcharts2" class="echarts_box" v-loading="myEcharts2Loading && $store.state.setting.loadingShow"></div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="border_box">
          <div class="forms_table_title pdl10">
            <i class="el-icon-s-marketing"></i>近一年股票流入流出<hint  hintName = "" dimCode = "GP_GPLRLC" dimType = "indexHelp"></hint>
            <li @click="exportExcelFile6"><el-tooltip content="下载图表数据" placement="top"><i class="el-icon-s-order"></i></el-tooltip></li>
          </div>
          <div id="myEcharts6" class="echarts_box" v-loading="myEcharts6Loading && $store.state.setting.loadingShow"></div>
        </div>
         <!-- <el-row style="margin-top: 40px;" >
            <el-col :span="2">
              <div class="termAverageone_box">
                <li><span style="background: #8EB4E3;"></span></li>
                <li><span style="background: #CCC1DA;"></span></li>
                <li><span style="background: #FAC090;"></span></li>
                <li><span style="background: #E6B9B8;"></span></li>
              </div>
            </el-col>
            <el-col :span="11">
              <div class="termAveragetwo_box">
              <li>期间最大仓位</li>
              <li>期间平均仓位</li>
              <li>期间最小仓位</li>
              <li>中证800期间涨跌幅</li>
              </div>
            </el-col>
            <el-col :span="11">
              <div class="termAveragetwo_box">
                <li>66.48%</li>
                <li>19.44%</li>
                <li>16.11%</li>
                <li>6.87%</li>
              </div>
            </el-col>
          </el-row> -->
      </el-col>
    </el-row>

    <div class="forms_table_title">
      <i class="el-icon-tickets"></i>股票行业分布
      <hint  hintName = "" dimCode = "GP_HYFB" dimType = "indexHelp"></hint>
      <li>
        <el-button @click="downloadTableExcel" type="primary" plain :icon="downLoadIcon" :disabled="isDisabled" size="small">{{downLoadText}}</el-button>
      </li>
    </div>

    <el-row :gutter="20">
      <!-- <el-col :span="12">
        <div class="border_box">
          <div class="forms_table_title pdl10">
            <i class="el-icon-s-marketing"></i>股票（总资产）-行业分布
            <li><el-tooltip content="下载图表数据" placement="top"><i class="el-icon-s-order"></i></el-tooltip></li>
          </div>
          <div id="myEcharts" class="echarts_box"></div>
        </div>
      </el-col> -->
      <el-col :span="24">
        <!--列表-->
        <el-table
          :data="tableData"
          :default-sort="{prop: 'priceRatio', order: 'descending'}"
          stripe
          border
          max-height="290"
          @sort-change="handleSortChange"
          v-loading="stockTableLoading"
          style="width: 100%">
          <el-table-column
            type="index"
            label="序号"
            width="60"
            header-align="center">
          </el-table-column>
          <el-table-column
            prop="industryName"
            show-overflow-tooltip
            sortable
            :sort-orders="['ascending', 'descending']"
            label="行业"
            min-width="120"
            header-align="center">
          </el-table-column>
          <el-table-column
            prop="price"
            sortable
            :sort-orders="['ascending', 'descending']"
            label="市值(万元)"
            min-width="120"
            header-align="center"
            align="right">
            <template slot-scope="scope">
              {{scope.row.price | moneyMillion}}
            </template>
          </el-table-column>
          <el-table-column
            prop="priceRatio"
            sortable
            :sort-orders="['ascending', 'descending']"
            label="占股票资产比例(%)"
            min-width="110"
            header-align="center"
            align="right">
            <template slot-scope="scope">
              {{scope.row.priceRatio | ratioThousand}}
            </template>
          </el-table-column>
          <el-table-column
            prop="valueRatio"
            sortable
            :sort-orders="['ascending', 'descending']"
            label="占净值比(%)"
            min-width="80"
            header-align="center"
            align="right">
            <template slot-scope="scope">
              {{scope.row.valueRatio | ratioThousand}}
            </template>
          </el-table-column>
          <el-table-column
            prop="netInflowPrice"
            sortable
            :sort-orders="['ascending', 'descending']"
            label="本周以来净流入(万元)"
            min-width="120"
            header-align="center"
            align="right">
            <template slot-scope="scope">
              {{scope.row.netInflowPrice | moneyMillion}}
            </template>
          </el-table-column>
          <el-table-column
            prop="buy"
            sortable
            :sort-orders="['ascending', 'descending']"
            label="本周以来流入(万元)"
            min-width="120"
            header-align="center"
            align="right">
            <template slot-scope="scope">
              {{scope.row.buy | moneyMillion}}
            </template>
          </el-table-column>
          <el-table-column
            prop="sell"
            sortable
            :sort-orders="['ascending', 'descending']"
            label="本周以来流出(万元)"
            min-width="120"
            header-align="center"
            align="right">
            <template slot-scope="scope">
              {{scope.row.sell | moneyMillion}}
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt10 mr20">
      <el-col :span="12">
        <div class="border_box">
          <div class="forms_table_title" style="padding-left: 10px">
            <i class="el-icon-s-marketing"></i>近一年股票资产PE<hint  hintName = "" dimCode = "GP_GPPE" dimType = "indexHelp"></hint>
            <li @click="exportExcelFile4"><el-tooltip content="下载图表数据" placement="top"><i class="el-icon-s-order"></i></el-tooltip></li>
          </div>
          <div id="myEcharts4" class="echarts_box" v-loading="myEcharts4Loading && $store.state.setting.loadingShow"></div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="border_box">
          <div class="forms_table_title" style="padding-left: 10px">
            <i class="el-icon-s-marketing"></i>近一年股票资产PB<hint  hintName = "" dimCode = "GP_GPPB" dimType = "indexHelp"></hint>
            <li @click="exportExcelFile5"><el-tooltip content="下载图表数据" placement="top"><i class="el-icon-s-order"></i></el-tooltip></li>
          </div>
          <div id="myEcharts5" class="echarts_box" v-loading="myEcharts5Loading && $store.state.setting.loadingShow"></div>
        </div>
      </el-col>
    </el-row>

    <el-dialog
      v-el-drag-dialog
      :title="dialogTitle"
      :visible.sync="dialogMask"
      :close-on-click-modal="false"
      @sort-change="handleSortChange3">
      <el-table
        :data="dialogTableData"
        :default-sort="{prop: 'symbolPrice', order: 'descending'}"
        border
        stripe
        max-height="300"
        style="width: 100%">
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
          prop="investManager"
          show-overflow-tooltip
          sortable
          :sort-orders="['ascending', 'descending']"
          label="投资经理"
          min-width="80"
          header-align="center"
        />
        <el-table-column
          prop="symbolCode"
          show-overflow-tooltip
          sortable
          :sort-orders="['ascending', 'descending']"
          label="个券代码"
          min-width="80"
          header-align="center"
        />
        <el-table-column
          prop="symbolName"
          show-overflow-tooltip
          sortable
          :sort-orders="['ascending', 'descending']"
          label="个券名称"
          min-width="80"
          header-align="center"
        />
        <el-table-column
          prop="symbolType"
          show-overflow-tooltip
          sortable
          :sort-orders="['ascending', 'descending']"
          label="个券类型"
          min-width="70"
          header-align="center"
        />
        <el-table-column
          prop="symbolAcount"
          show-overflow-tooltip
          sortable
          :sort-orders="['ascending', 'descending']"
          label="个券数量"
          min-width="80"
          header-align="center"
          align="right"
        >
          <template slot-scope="scope">
            {{scope.row.symbolAcount | moneyThousand}}
          </template>
        </el-table-column>
        <el-table-column
          prop="symbolPrice"
          show-overflow-tooltip
          sortable
          :sort-orders="['ascending', 'descending']"
          label="个券市值(万元)"
          min-width="90"
          header-align="center"
          align="right"
        >
          <template slot-scope="scope">
            {{scope.row.symbolPrice | moneyMillion}}
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script type="text/ecmascript-6">
import Pagination from '@/components/Pagination'
import * as echarts from 'echarts'
import { exportExcel, forEachSeries} from '@/utils/exportExcel'
import commonApi from '@/api/common'
import investmentManagerApi from '@/api/managementView/investmentManager'
import {
  stockPriceDateUrl,
  stockIndustryDistributionUrl,
  findStockPositionUrl,
  findInflowAndOutflowUrl,
  frontShareOfStockUrl,
  stockAnalysisInvestBondAnalysisDetailsUrl,
  stockPbDistributionUrl,
  stockPeDistributionUrl
} from '@/api/securitiesAnalysis'
import fun from '@/filters/common'
import hint from '@/components/hint'
export default {
  name: "stock-analysis",
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
    },
    // 图表打开关闭
    echartsOpenChild: {
      type: Boolean
    }
  },
  data() {
    return {
      // 查询条件
      formQuery: {
        // 日期
        beginDate:'',
        // 组合类型
        fundType: [],
        // 投资经理
        account: '',
        // 组合代码集合
        fundList: [],
        // 指数
        targetList: [],
        // 是否统计权益
        isEquity: 1,
      },
      // 查询条件2
      formQuery2: {
        // 区间
        rowNumber: '',
        // 股票代码或者股票名称
        searchName: '',
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
        beginDate: [
          { type: 'string', required: true, message: '请选择日期', trigger: 'change' }
        ],
        // 指数
        targetList: [
          { type: 'array', required: true, message: '请选择指数', trigger: 'change' }
        ],
        // 组合类型
        fundType: [
          { type: 'array', required: true, message: '请选择组合类型', trigger: 'change' }
        ],
        // 投资经理
        account: [
          { type: 'string', required: true, message: '请选择投资经理', trigger: 'change' }
        ]
      },
      // 指数类型
      targetTypes: [],
      // 区间数组
      regionArrs: [],
      // 验证规则2
      rules2: {
        // 区间
        rowNumber: [
          { type: 'string', required: true, message: '请选择区间', trigger: 'change' }
        ]
      },
      // 证券分析-股票分析（汇总）
      stockPriceData: {
        // 股票资产规模
        price: 0,
        // 数据日期
        dateString: '--',
        // 占资产净值比
        priceRatio: 0
      },
      // 股票（总资产）-行业分布图
      myEcharts: null,
      // 股票（总资产）-行业分布图数据
      stockIndustryDistributionData: [],
      // 列表数据
      tableData: [],
      // 表格loading
      stockTableLoading: false,
      /* 按钮禁止与否 */
      isDisabled: false,
      // 导出图标
      downLoadIcon: 'el-icon-download',
      // 导出提示文字
      downLoadText: '导出数据',
      // 股票仓位图
      myEcharts2: null,
      // excel表头
			excelHeader2: [],
			// excel数据
			excelData2: [],
      // 股票仓位图loading
      myEcharts2Loading: false,
      // 股票仓位图数据
      findStockPositionData: {},
      // 前十大个股占股票资产比例图
      myEcharts3: null,
      // excel表头3
			excelHeader3: [],
			// excel数据3
			excelData3: [],
      // 前十大个股占股票资产比例图loading
      myEcharts3Loading: false,
      // 前十大个股占股票资产比例图数据
      frontShareOfStockData: [],
      // 列表数据2
      tableData2: [],
      // 表格loading
      tableLoading2: false,
      /* 按钮禁止与否 */
      isDisabled2: false,
      // 导出图标
      downLoadIcon2: 'el-icon-download',
      // 导出提示文字
      downLoadText2: '导出数据',
      // 总条数
      total2: 0,
      // 股票资产PE
      myEcharts4: null,
      // excel表头
			excelHeader4: [],
			// excel数据
			excelData4: [],
      // 股票资产PEloading
      myEcharts4Loading: false,
      // 股票资产PE数据
      stockPeDistributionData: {},
      // 股票资产PB
      myEcharts5: null,
      // excel表头
			excelHeader5: [],
			// excel数据
			excelData5: [],
      // 股票资产PBloading
      myEcharts5Loading: false,
      // 股票资产PB数据
      stockPbDistributionData: {},
      // 流入流出
      myEcharts6: null,
      // excel表头
			excelHeader6: [],
			// excel数据
			excelData6: [],
      // 流入流出PBloading
      myEcharts6Loading: false,
      // 股票分析（流入流出）数据
      findInflowAndOutflowData: [],
      // 弹窗
      dialogMask: false,
      // 标题
      dialogTitle: '',
      // 列表数据
      dialogTableData: [],
      // 股票行业分布排序字段
      orderStr: '"priceRatio" desc nulls last',
      // 个股占股票资产比例排序字段
      orderBy: '"price" desc nulls last',
      // 查询按钮禁用
      btnDisabled: false,
      // 查询按钮禁用2
      btnDisabled2: false,
      // 保存表格传递值
      saveStr: '',
      // 债券/发行人排序字段
      orderStr2: `"symbolPrice" desc nulls last`
    }
  },
  mounted () {
    if (this.fundCode) this.formQuery.fundList = [this.fundCode]
    // 今天
    // let today = this.$moment().subtract(1,'days').format('YYYY-MM-DD')
    if (this.date) {
      // 日期
      this.formQuery.beginDate = this.date
    } else {
      // 日期
      // this.formQuery.beginDate = today
      // 接口返回T-1日
      this.formQuery.beginDate = this.$store.state.setting.endDate
    }
    // 投资经理账户
    // this.formQuery.account = '511'
    // 指数类型
    this.formQuery.targetList = ['*']
    // 组合类型
    this.formQuery.fundType = ['*']
    // 指数类型列表查询
    this.getListEdims('target_type')
    // 区间查询
    this.getListEdims('range_type')
    // 投资经理
    if (!this.isAccount) {
      this.formQuery.account = -1
    } else {
      // 投资经理列表查询
      this.getManagerList()
    }
    // 组合类型
    if (!this.isFundType) {
      this.formQuery.fundType = ['*']
    } else {
      // 组合类型列表查询
      this.getListEdims('fund_type')
    }
    this.$nextTick(() => {
      // 股票（总资产）-行业分布图表初始化
      // this.initEcharts()
      // 股票仓位图表初始化
      this.initEcharts2()
      // 前十大个股占股票资产比例图表初始化
      // this.initEcharts3()
      // 股票资产PE
      this.initEcharts4()
      // 股票资产PB
      this.initEcharts5()
      // 流入流出图表初始化
      this.initEcharts6()
      // 是否默认查询
      if (this.$store.state.setting.isOnQuery) {
        // 延迟2s请求
        let timer = setTimeout(() => {
          // 查询
          this.onQuery()
          clearTimeout(timer)
        }, 2000)
      }
    })
    let _this = this
    // 宽度变化重新渲染图表
    window.addEventListener('resize', () => {
      let timer = setTimeout(() => {
				// 宽度变化重新渲染图表
				_this.echartsResize()
				clearTimeout(timer)
			},500)
    })
  },
  methods: {
    // 查询
    onQuery () {
      this.$refs['formQuery'].validate((valid) => {
        if (valid) {
          // 禁用搜索按钮
          this.$fun.searchButtonDisabled("btnDisabled", this)
          // 股票分析（汇总）
          this.stockPriceDate ()
          // 股票分析（股票行业分布）
          this.stockIndustryDistribution()
          // 股票分析（股票仓位）
          this.findStockPosition()
          // 股票分析（流入流出）
          this.findInflowAndOutflow()
          // 股票分析（个股占股票资产比例）
          // this.frontShareOfStock()
          this.onQuery2(1)
          // 证券分析-股票分析（PB）
          this.stockPbDistribution()
          // 证券分析-股票分析（PE）
          this.stockPeDistribution()
        }
      })
    },
    // 查询2
    onQuery2 (page) {
      this.$refs['formQuery2'].validate((valid) => {
        if (valid) {
          // 禁用搜索按钮
          this.$fun.searchButtonDisabled("btnDisabled2", this)
          // 重置起始页
          if (page) this.formQuery2.pageNum = 1
          // 股票分析（个股占股票资产比例）
          this.frontShareOfStock()
        }
      })
    },
    // 清除
    resetForm (formName) {
      this.$refs[formName].resetFields()
    },
    // 日期变化
    handleChangeDate (date) {
      // if (!date) return
      // this.$bus.$emit('securityAnalyzeDate', date)
    },
    // 页面点击事件
    pagination (val) {
      let { page, limit } = val
      // 起始页
      this.formQuery2.pageNum = page
      // 每页数量
      this.formQuery2.pageSize = limit
      // 查询
      this.$refs['formQuery2'].validate((valid) => {
        if (valid) {
					// 股票分析（个股占股票资产比例）
          this.frontShareOfStock()
        }
      })
    },
    // 类型列表查询
    getListEdims (type) {
      // 字典类型
      let params = type
      commonApi.edimsCommon(params).then(res => {
        let { status, data } = res.data
        if (status === 0) {
          if (type === 'target_type') {
            this.targetTypes = data
          }
          // 组合类型查询
          if (type === 'fund_type') this.groupTypeArr = data
          // 区间查询
          if (type === 'range_type') {
            this.regionArrs = data
            // 区间默认值
            if (data.length) {
              this.formQuery2.rowNumber = data[0].dimCde
            }
          }
        }
      })
    },
    // 投资经理列表查询
    getManagerList () {
      // 权益（1）/固收（2）/混合（0）
      // 股票分析只可以选权益经理
      let params = 1
      investmentManagerApi.managerList(params).then(res => {
        let { status, data } = res.data
        if (status === 0) {
          this.manageArr = data
          if (this.manageArr.length) this.formQuery.account = this.manageArr[0].account
        }
      })
    },
    // 股票分析（汇总）
    stockPriceDate () {
      let payload = {
        // 组合类型
        fundType: this.formQuery.fundType,
        // 组合代码
        fundList: this.formQuery.fundList
      }
      let params = {
        // 开始时间
        beginDate: this.formQuery.beginDate,
        // 是否统计权益
        isEquity: this.formQuery.isEquity,
        // 投资经理账户
        account: this.formQuery.account
      }
      stockPriceDateUrl(params, payload).then(res => {
        let { status, data } = res
        if (status === 0) {
          let { dateString, priceRatio, price } = data || {}
          // 数据日期
          this.stockPriceData.dateString = dateString
          // 占资产净值比
          this.stockPriceData.priceRatio = priceRatio || 0
          // 股票资产规模
          this.stockPriceData.price = price || 0
        }
      })
    },
    // 股票分析（股票行业分布）
    stockIndustryDistribution (flag) {
      if (!flag) {
        this.stockTableLoading = true
      } else {
        if (this.isDisabled) return
        this.isDisabled = true
        this.downLoadIcon = 'el-icon-loading'
        this.downLoadText = '导出数据中...'
      }
      let payload = {
        // 组合类型
        fundType: this.formQuery.fundType,
        // 组合代码
        fundList: this.formQuery.fundList
      }
      let params = {
        // 开始时间
        beginDate: this.formQuery.beginDate,
        // 是否统计权益
        isEquity: this.formQuery.isEquity,
        // 投资经理账户
        account: this.formQuery.account,
        // 排序字段
        orderStr: this.orderStr
      }
      if (flag) {
        params.ex_tmp_name = '股票行业分布.xls'
      }
      stockIndustryDistributionUrl(params, payload).then(res => {
        this.stockTableLoading = false
        this.isDisabled = false
        this.downLoadIcon = 'el-icon-download'
        this.downLoadText = '导出数据'
        let { status, data } = res
        if (status === 0) {
          if (flag) { // 下载excel
            if (!data) return
					  this.$fun.commonDownloadUrl(data)
          } else {
            this.tableData = data
          }
        }
      }).catch(() => {
        this.stockTableLoading = false
        this.isDisabled = false
        this.downLoadIcon = 'el-icon-download'
        this.downLoadText = '导出数据'
      })
    },
    // 股票分析（股票仓位）
    findStockPosition () {
      // 图表遮盖层显示
      this.myEcharts2Loading = true
      let payload = {
        // 组合类型
        fundType: this.formQuery.fundType,
        // 组合代码
        fundList: this.formQuery.fundList,
        // 指数
        targetList: this.formQuery.targetList
      }
      let params = {
        // 开始时间
        beginDate: this.formQuery.beginDate,
        // 是否统计权益
        isEquity: this.formQuery.isEquity,
        // 投资经理账户
        account: this.formQuery.account
      }
      findStockPositionUrl(params, payload).then(res => {
        // 图表遮盖层隐藏
        this.myEcharts2Loading = false
        let { status, data } = res
        if (status === 0) {
          this.findStockPositionData = data
          // 股票（总资产）-行业分布图表初始化
          this.initEcharts2();
        }
      }).catch(() => {
        // 图表遮盖层隐藏
        this.myEcharts2Loading = false
      })
    },
    // 股票分析（流入流出）
    findInflowAndOutflow () {
      // 图表遮盖层显示
      this.myEcharts6Loading = true
      let payload = {
        // 组合类型
        fundType: this.formQuery.fundType,
        // 组合代码
        fundList: this.formQuery.fundList
      }
      let params = {
        // 开始时间
        beginDate: this.formQuery.beginDate,
        // 是否统计权益
        isEquity: this.formQuery.isEquity,
        // 投资经理账户
        account: this.formQuery.account
      }
      findInflowAndOutflowUrl(params, payload).then(res => {
        // 图表遮盖层隐藏
        this.myEcharts6Loading = false
        let { status, data } = res
        if (status === 0) {
          this.findInflowAndOutflowData = data
          // 股票（总资产）-行业分布图表初始化
          this.initEcharts6();
        }
      }).catch(() => {
        // 图表遮盖层隐藏
        this.myEcharts6Loading = false
      })
    },
    // 股票分析（个股占股票资产比例）
    frontShareOfStock (flag) {
      if (!flag) {
        this.tableLoading2 = true
      } else {
        if (this.isDisabled2) return
        this.isDisabled2 = true
        this.downLoadIcon2 = 'el-icon-loading'
        this.downLoadText2 = '导出数据中...'
      }
      // 图表遮盖层显示
      this.myEcharts3Loading = true
      let payload = {
        // 组合类型
        fundType: this.formQuery.fundType,
        // 组合代码
        fundList: this.formQuery.fundList
      }
      let params = {
        // 日期
        beginDate: this.formQuery.beginDate,
        // 是否统计权益
        isEquity: this.formQuery.isEquity,
        // 投资经理
        account: this.formQuery.account,
        // 排序字段
        orderBy: this.orderBy,
        // 起始页
        pageNum: this.formQuery2.pageNum,
        // 每页数量
        pageSize: this.formQuery2.pageSize,
        // 前十
        rowNumber: this.formQuery2.rowNumber,
        // 股票代码或者股票名称
        searchName: this.formQuery2.searchName
      }
      if (flag) {
        params.pageNum = 1
        params.pageSize = 5000
        params.ex_tmp_name = '股票占股票资产比例.xls'
      }
      frontShareOfStockUrl(params, payload).then(res =>{
        this.tableLoading2 = false
        this.isDisabled2 = false
        this.downLoadIcon2 = 'el-icon-download'
        this.downLoadText2 = '导出数据'
        // 图表遮盖层隐藏
        this.myEcharts3Loading = false
        let { status, data } = res
        if (status === 0) {
          if (flag) { // 下载excel
            if (!data) return
					  this.$fun.commonDownloadUrl(data)
          } else {
            let { left, right } = data
            // this.frontShareOfStockData = left
            let { total, list } = right
            // // 列表数据
            this.tableData2 = list
            this.total2 = total
            // 前十大个股占股票资产比例图
            // this.initEcharts3()
          }
        }
      }).catch(() => {
        this.tableLoading2 = false
        this.isDisabled2 = false
        this.downLoadIcon2 = 'el-icon-download'
        this.downLoadText2 = '导出数据'
        // 图表遮盖层隐藏
        this.myEcharts3Loading = false
      })
    },
    // 股票分析（个股占股票资产比例详情）
    stockAnalysisInvestBondAnalysisDetails (symbolCodeName) {
      // 组合代码
      let payload = this.formQuery.fundList
      let params = {
        // 开始时间
        beginDate: this.formQuery.beginDate,
        // 是否统计权益
        isEquity: this.formQuery.isEquity,
        // 组合名称/代码
        symbolCodeName: symbolCodeName,
        // 投资经理
        account: this.formQuery.account,
        // 排序字段
        orderStr: this.orderStr2
      }
      stockAnalysisInvestBondAnalysisDetailsUrl(params, payload).then(res => {
        let { status, data } = res
        if (status === 0) {
          this.dialogTableData = data
        }
      })
    },
    // 证券分析-股票分析（PE）
    stockPeDistribution () {
      // 图表遮盖层显示
      this.myEcharts4Loading = true
      let payload = {
        // 组合类型
        fundType: this.formQuery.fundType,
        // 组合代码
        fundList: this.formQuery.fundList,
        // 指数
        targetList: this.formQuery.targetList
      }
      let params = {
        // 开始时间
        beginDate: this.formQuery.beginDate,
        // 是否统计权益
        isEquity: this.formQuery.isEquity,
        // 投资经理账户
        account: this.formQuery.account
      }
      stockPeDistributionUrl(params, payload).then(res =>{
        // 图表遮盖层隐藏
        this.myEcharts4Loading = false
        let { status, data } = res
        if (status === 0) {
          this.stockPeDistributionData = data
          // 股票资产PE图表初始化
          this.initEcharts4();
        }
      }).catch(() => {
        // 图表遮盖层隐藏
        this.myEcharts4Loading = false
      })
    },
    // 证券分析-股票分析（PB）
    stockPbDistribution () {
      // 图表遮盖层显示
      this.myEcharts5Loading = true
      let payload = {
        // 组合类型
        fundType: this.formQuery.fundType,
        // 组合代码
        fundList: this.formQuery.fundList,
        // 指数
        targetList: this.formQuery.targetList
      }
      let params = {
        // 开始时间
        beginDate: this.formQuery.beginDate,
        // 是否统计权益
        isEquity: this.formQuery.isEquity,
        // 投资经理账户
        account: this.formQuery.account
      }
      stockPbDistributionUrl(params, payload).then(res =>{
        // 图表遮盖层隐藏
        this.myEcharts5Loading = false
        let { status, data } = res
        if (status === 0) {
          this.stockPbDistributionData = data
          // 股票资产PB图表初始化
          this.initEcharts5();
        }
      }).catch(() => {
        // 图表遮盖层隐藏
        this.myEcharts5Loading = false
      })
    },
    // 股票（总资产）-行业分布图表初始化
    initEcharts () {
      let echartsData = this.stockIndustryDistributionData
      // 股票行业占比
      let priceRatioArrs = []
      // 指数行业占比
      let weightArrs = []
      // 纵坐标
      let yData = []
      // 最大值
			let dataMax = 0
      echartsData.forEach(item => {
        yData.push(item.industryName)
        priceRatioArrs.push(item.priceRatio)
        weightArrs.push(item.weight)
      })
      dataMax = Math.max(...priceRatioArrs, ...weightArrs, dataMax)
      // 数据为空清空echarts
      if (this.myEcharts) this.myEcharts.clear()
      this.myEcharts = echarts.init(document.getElementById('myEcharts'))
      this.myEcharts.setOption({
        title: {
          text: ''
        },
        tooltip : {
          trigger: 'axis',
          axisPointer : {            // 坐标轴指示器，坐标轴触发有效
            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
          }
        },
        legend: {
          data: ['股票（总资产）行业占比', '指数行业占比']
        },
        grid: {
          left: '4%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          feature: {
						dataView: {
              optionToContent: this.$fun.optionToContent
            },
            saveAsImage: {}
          }
        },
        color: this.$colorArrs,
        xAxis : [
          {
            type: 'value',
            axisLabel: {
              show: true,
              formatter:'{value}%'
            },
            // max: dataMax,
            // min: 0
          }
        ],
        yAxis : [
          {
            type: 'category',
            axisTick : {
              show: false
            },
            data : yData
          }
        ],
        series : [
          {
            name:'股票（总资产）行业占比',
            type:'bar',
            barWidth : 10,
            label: {
              normal: {
                show: true,
                position: 'inside'
              }
            },
            data: priceRatioArrs
          },
          {
            name:'指数行业占比',
            type:'bar',
            barWidth : 10,
            label: {
              normal: {
                show: true
              }
            },
            data: weightArrs
          }
        ]
      })
    },
    // 股票仓位图表初始化初始化
    initEcharts2 () {
      let echartsData = this.findStockPositionData
      // 横坐标
      let xData = []
      // 头部显示
      let legendData = []
      // 最大值（左）
      let dataMaxl = 0
      // 最小值（左）
			let dataMinl = 0
      // 最大值（右）
      let dataMaxr = 0
      // 最小值（右）
      let dataMinr = 0
      // 数据数组
			let seriesArrs = []
      for (let key in echartsData) {
        if (!xData.length) {
          echartsData[key].forEach(item => {
            xData.push(item.dateTime)
          })
        }
        legendData.push(key)
        let seriesObj = {
          name: key,
          type: 'line',
          barWidth : 10,
          data: []
        }
        echartsData[key].forEach(item => {
          if (key === '股票仓位') {
            // 百分比处理
            if (item.price) {
              item.price = fun.accMul(Number(item.price), 100).toFixed(2)
            } else {
              item.price = 0
            }
          } else {
            item.price = Number(item.price).toFixed(2)
          }
          seriesObj.data.push(item.price)
        })
        if (key !== '股票仓位') {
          seriesObj.yAxisIndex = 1
          // 最大值（右）
          dataMaxr = Math.max(...seriesObj.data, dataMaxr)
          // 最小值（右）
          dataMinr = Math.min(...seriesObj.data, dataMinr)
        } else {
          // 最大值（左）
          dataMaxl = Math.max(...seriesObj.data, dataMaxl)
          // 最小值（左）
          dataMinl = Math.min(...seriesObj.data, dataMinl)
        }
        seriesArrs.push(seriesObj)
      }
      // 数据为空清空echarts
      if (this.myEcharts2) this.myEcharts2.clear()
      this.myEcharts2 = echarts.init(document.getElementById('myEcharts2'))
      this.myEcharts2.setOption({
        title: {
          text: ''
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: legendData,
          x: 'center'
        },
        grid: {
          left: '5.5%',
          right: '6%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          feature: {
            dataView: {
              optionToContent: this.$fun.optionToContent
            },
            saveAsImage: {}
          }
        },
        color: this.$colorArrs,
        xAxis: {
          type: 'category',
          boundaryGap: true,
          data: xData
        },
        yAxis: [
          {
            name: '仓位(%)',
            type: 'value',
            // max: dataMaxl,
            // min: dataMinl
          },
          {
            name: '指数行情(点)',
            type: 'value',
            // max: dataMaxr,
            // min: dataMinr
          }
        ],
        // x轴拖动
        dataZoom: [
          {
            show: true,
            realtime: true,
            start: 0,
            end: 100 ,// 结束位置（共100等份）
            bottom: '3%',
          },
          {
            type: 'inside',
            realtime: true,
            height: 25, //滚动条高度
            start: 0,
            end: 85
          }
        ],
        series: seriesArrs
      })
      // 获取配置信息
      let echartsOption = this.myEcharts2.getOption()
			if (echartsOption.series && echartsOption.series.length) {
				// 遍历组装数据
				let { excelHeader, excelData } = forEachSeries(echartsOption)
				// excel表头
				this.excelHeader2 = excelHeader
				// excel数据
				this.excelData2 = excelData
			}
    },
    // 前十大个股占股票资产比例图
    initEcharts3 () {
      let echartsData = this.frontShareOfStockData
      // 饼状图数据
      let seriesArrs = []
      // 头部显示
      let legendData = []
      echartsData.forEach(item => {
        let obj = {
          value: item.price,
          name: item.symbolName
        }
        legendData.push(item.symbolName)
        seriesArrs.push(obj)
      })
      // 饼状图数据
      // let data = [
      //   {value:33, name:'18银川通联MTN003'},
      //   {value:31, name:'19赣州发展MTN001'},
      //   {value:23, name:'19国联MTN001'},
      //   {value:13, name:'19渝保税MTN006'},
      //   {value:15, name:'19孝感城投MTN001'},
      //   {value:25, name:'19晋江城投MTN009'},
      //   {value:23, name:'19中广核001'},
      //   {value:32, name:'19中山城投MT001'},
      //   {value:19, name:'17陕西水务MT003'},
      //   {value:25, name:'17南京城投MT003'},
      // ]
      this.myEcharts3 = echarts.init(document.getElementById('myEcharts3'))
      this.myEcharts3.setOption({
        tooltip: {
          trigger: 'item',
          formatter: "{a} <br/>{b}: {c} ({d}%)"
        },
        legend: {
          type: 'scroll',
          orient: 'vertical',
          icon:"circle",
          right: 80,
          top: 38,
          bottom: 20,
          itemWidth: 6,// 标志图形的长度
          itemHeight: 6,// 标志图形的宽度
          itemGap: 7 ,// 设置间距
          data: legendData,
          formatter: function(name) {
            var total = 0;
            var tarValue;
            let data = seriesArrs
            for (var i = 0, l = data.length; i < l; i++) {
              total += Number(data[i].value)
              if (data[i].name == name) {
                tarValue = Number(data[i].value)
              }
            }
            var p = (tarValue / total * 100).toFixed(2);
            return name + ' ' + ' '  + p + '%';
          },

        },
        toolbox: {
          feature: {
            dataView: {
              optionToContent: this.$fun.optionToContent
            },
            saveAsImage: {}
          }
        },
        color: this.$colorArrs,
        series: [
          {
            name:'持仓市值',
            type:'pie',
            radius: ['50%', '70%'],
            center: ['30%', '50%'],
            avoidLabelOverlap: false,
            label: {
              normal: {
                show: false,
                position: 'center',
              },
              emphasis: {
                show: true,
                textStyle: {
                  fontSize: '14',
                  fontWeight: 'bold'
                }
              }
            },
            labelLine: {
              normal: {
                show: false
              }
            },
            data: seriesArrs
          }
        ]
      })
      // 获取配置信息
      let echartsOption = this.myEcharts3.getOption()
			if (echartsOption.series && echartsOption.series.length) {
				// 遍历组装数据
				let { excelHeader, excelData } = forEachSeries(echartsOption, 2)
				// excel表头3
				this.excelHeader3 = excelHeader
				// excel数据3
				this.excelData3 = excelData
			}
    },
    // 股票资产PE
    initEcharts4 () {
      let echartsData = this.stockPeDistributionData
      // 横坐标
      let xData = []
      // 头部显示
      let legendData = []
      // 最大值（左）
      let dataMaxl = 0
      // 最小值（左）
			let dataMinl = 0
      // 最大值（右）
      let dataMaxr = 0
      // 最小值（右）
      let dataMinr = 0
      // 数据数组
			let seriesArrs = []
      for (let key in echartsData) {
        if (!xData.length) {
          echartsData[key].forEach(item => {
            xData.push(item.dateTime)
          })
        }
        legendData.push(key)
        let seriesObj = {
          name: key,
          type: 'line',
          barWidth : 10,
          data: []
        }
        echartsData[key].forEach(item => {
          // if (key === 'PE') {
          //   // 百分比处理
          //   if (item.price) {
          //     // item.price = fun.accMul(Number(item.price), 100).toFixed(2)
          //     item.price = Number(item.price).toFixed(2)
          //   } else {
          //     item.price = 0
          //   }
          // } else {
          //   item.price = Number(item.price).toFixed(2)
          // }
          item.price = Number(item.price).toFixed(2)
          seriesObj.data.push(item.price || 0)
        })
        if (key !== 'PE') {
          seriesObj.yAxisIndex = 1
          // 最大值（右）
          dataMaxr = Math.max(...seriesObj.data, dataMaxr)
          // 最小值（右）
          dataMinr = Math.min(...seriesObj.data, dataMinr)
        } else {
          // 最大值（左）
          dataMaxl = Math.max(...seriesObj.data, dataMaxl)
          // 最小值（左）
          dataMinl = Math.min(...seriesObj.data, dataMinl)
        }
        seriesArrs.push(seriesObj)
      }
      // 数据为空清空echarts
      if (this.myEcharts4) this.myEcharts4.clear()
      this.myEcharts4 = echarts.init(document.getElementById('myEcharts4'))
      this.myEcharts4.setOption({
        color: this.$colorArrs,
        title: {
          text: ''
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: legendData
        },
        grid: {
          left: '5%',
          right: '6%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          feature: {
            dataView: {
              optionToContent: this.$fun.optionToContent
            },
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: xData
        },
        yAxis: [
          {
            name: 'PE',
            type: 'value',
            // max: dataMaxl,
            // min: dataMinl
          },
          {
            name: '指数行情(点)',
            type: 'value',
            // max: dataMaxr,
            // min: dataMinr
          }
        ],
        // x轴拖动
        dataZoom: [
          {
            show: true,
            realtime: true,
            start: 0,
            end: 100 ,// 结束位置（共100等份）
            bottom: '3%',
          },
          {
            type: 'inside',
            realtime: true,
            height: 25, //滚动条高度
            start: 0,
            end: 85
          }
        ],
        series: seriesArrs
      })
      // 获取配置信息
      let echartsOption = this.myEcharts4.getOption()
			if (echartsOption.series && echartsOption.series.length) {
				// 遍历组装数据
				let { excelHeader, excelData } = forEachSeries(echartsOption)
				// excel表头
				this.excelHeader4 = excelHeader
				// excel数据
				this.excelData4 = excelData
			}
    },
    // 股票资产PB
    initEcharts5 () {
      let echartsData = this.stockPbDistributionData
      // 横坐标
      let xData = []
      // 头部显示
      let legendData = []
      // 最大值（左）
      let dataMaxl = 0
      // 最小值（左）
			let dataMinl = 0
      // 最大值（右）
      let dataMaxr = 0
      // 最小值（右）
      let dataMinr = 0
      // 数据数组
			let seriesArrs = []
      for (let key in echartsData) {
        if (!xData.length) {
          echartsData[key].forEach(item => {
            xData.push(item.dateTime)
          })
        }
        legendData.push(key)
        let seriesObj = {
          name: key,
          type: 'line',
          barWidth : 10,
          data: []
        }
        echartsData[key].forEach(item => {
          // if (key === 'PB') {
          //   // 百分比处理
          //   if (item.price) {
          //     // item.price = fun.accMul(Number(item.price), 100).toFixed(2)
          //     item.price = Number(item.price).toFixed(2)
          //   } else {
          //     item.price = 0
          //   }
          // } else {
          //   item.price = Number(item.price).toFixed(2)
          // }
          item.price = Number(item.price).toFixed(2)
          seriesObj.data.push(item.price || 0)
        })
        if (key !== 'PB') {
          seriesObj.yAxisIndex = 1
          // 最大值（右）
          dataMaxr = Math.max(...seriesObj.data, dataMaxr)
          // 最小值（右）
          dataMinr = Math.min(...seriesObj.data, dataMinr)
        } else {
          // 最大值（左）
          dataMaxl = Math.max(...seriesObj.data, dataMaxl)
          // 最小值（左）
          dataMinl = Math.min(...seriesObj.data, dataMinl)
        }
        seriesArrs.push(seriesObj)
      }
      // 数据为空清空echarts
      if (this.myEcharts5) this.myEcharts5.clear()
      this.myEcharts5 = echarts.init(document.getElementById('myEcharts5'))
      this.myEcharts5.setOption({
        color: this.$colorArrs,
        title: {
          text: ''
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: legendData
        },
        grid: {
          left: '5%',
          right: '6%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          feature: {
            dataView: {
              optionToContent: this.$fun.optionToContent
            },
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: xData
        },
        yAxis: [
          {
            name: 'PB',
            type: 'value',
            // max: dataMaxl,
            // min: dataMinl
          },
          {
            name: '指数行情(点)',
            type: 'value',
            // max: dataMaxr,
            // min: dataMinr
          }
        ],
        // x轴拖动
        dataZoom: [
          {
            show: true,
            realtime: true,
            start: 0,
            end: 100 ,// 结束位置（共100等份）
            bottom: '3%',
          },
          {
            type: 'inside',
            realtime: true,
            height: 25, //滚动条高度
            start: 0,
            end: 85
          }
        ],
        series: seriesArrs
      })
      // 获取配置信息
      let echartsOption = this.myEcharts5.getOption()
			if (echartsOption.series && echartsOption.series.length) {
				// 遍历组装数据
				let { excelHeader, excelData } = forEachSeries(echartsOption)
				// excel表头
				this.excelHeader5 = excelHeader
				// excel数据
				this.excelData5 = excelData
			}
    },
    // 流入流出图表初始化初始化
    initEcharts6 () {
      let echartsData = this.findInflowAndOutflowData
      // 横坐标
      let xData = []
      // 头部显示
      let legendData = []
      // 最大值
      let dataMax = 0
      // 最小值
			let dataMin = 0
      // 数据数组
			let seriesArrs = []
      let seriesObj = {
        name: '净流入',
        type: 'line',
        barWidth : 10,
        data: []
      }
      echartsData.forEach(item => {
        xData.push(item.dateTime)
        // 万元处理
        if (item.price) {
          item.price = fun.accDiv(Number(item.price), 10000).toFixed(2)
        } else {
          item.price = 0
        }
        seriesObj.data.push(item.price || 0)
      })
      // 最大值
      dataMax = Math.max(...seriesObj.data, dataMax)
      // 最小值
      dataMin = Math.min(...seriesObj.data, dataMin)
      seriesArrs.push(seriesObj)
      // 数据为空清空echarts
      if (this.myEcharts6) this.myEcharts6.clear()
      this.myEcharts6 = echarts.init(document.getElementById('myEcharts6'))
      this.myEcharts6.setOption({
        title: {
          text: ''
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: legendData,
          x: 'center'
        },
        grid: {
          left: '6%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          feature: {
            dataView: {
              optionToContent: this.$fun.optionToContent
            },
            saveAsImage: {}
          }
        },
        color: this.$colorArrs,
        xAxis: {
          type: 'category',
          boundaryGap: true,
          data: xData
        },
        yAxis: [
          {
            name: '净流入(万元)',
            type: 'value',
            // max: dataMax,
            // min: dataMin
          }
        ],
        // x轴拖动
        dataZoom: [
          {
            show: true,
            realtime: true,
            start: 0,
            end: 100 ,// 结束位置（共100等份）
            bottom: '3%',
          },
          {
            type: 'inside',
            realtime: true,
            height: 25, //滚动条高度
            start: 0,
            end: 85
          }
        ],
        series: seriesArrs
      })
      // 获取配置信息
      let echartsOption = this.myEcharts6.getOption()
			if (echartsOption.series && echartsOption.series.length) {
				// 遍历组装数据
				let { excelHeader, excelData } = forEachSeries(echartsOption)
				// excel表头
				this.excelHeader6 = excelHeader
				// excel数据
				this.excelData6 = excelData
			}
    },
    // 当某一行被点击时会触发该事件
    rowClick (row, column, event) {
      // 当点击的是债券名称/债券代码显示弹窗
      if (column.property === 'symbolName'
            || column.property === 'symbolCode'
      ) {
        // 显示弹窗
        this.dialogMask = true
        // 标题
        this.dialogTitle = `${row.industryName || '未知行业'}-${row.symbolCode || ''}-${row.symbolName || ''}`
        // 保存表格传递值
        this.saveStr = event.target.textContent
        // 股票分析（个股占股票资产比例详情）
        this.stockAnalysisInvestBondAnalysisDetails(event.target.textContent)
      }
    },
    // 当表格的排序条件发生变化的时候会触发该事件
    handleSortChange (val) {
      if (val.order === 'ascending') {
        this.orderStr = `"${val.prop}" nulls last` // 升序
      } else {
        this.orderStr = `"${val.prop}" desc nulls last` // 降序
      }
      // 股票分析（股票行业分布）
      this.stockIndustryDistribution()
    },
    // 当表格的排序条件发生变化的时候会触发该事件
    handleSortChange2 (val) {
      if (val.order === 'ascending') {
        this.orderBy = `"${val.prop}" nulls last` // 升序
      } else {
        this.orderBy = `"${val.prop}" desc nulls last` // 降序
      }
      // 股票分析（个股占股票资产比例）
      this.frontShareOfStock()
    },
    // 当表格的排序条件发生变化的时候会触发该事件
    handleSortChange3 (val) {
      if (val.order === 'ascending') {
        this.orderStr2 = `"${val.prop}" nulls last` // 升序
      } else {
        this.orderStr2 = `"${val.prop}" desc nulls last` // 降序
      }
      // 股票分析（个股占股票资产比例详情）
        this.stockAnalysisInvestBondAnalysisDetails(this.saveStr)
    },
    // 图表变化
    echartsResize () {
      if (this.myEcharts) this.myEcharts.resize()
      if (this.myEcharts2) this.myEcharts2.resize()
      if (this.myEcharts3) this.myEcharts3.resize()
      if (this.myEcharts4) this.myEcharts4.resize()
      if (this.myEcharts5) this.myEcharts5.resize()
      if (this.myEcharts6) this.myEcharts6.resize()
    },
    // 导出excel2
		exportExcelFile2 () {
			const excelHeader = this.excelHeader2
			const excelData = this.excelData2
			const filename = '近一年股票仓位'
			exportExcel(excelHeader, excelData, filename)
    },
    // 导出excel3
		exportExcelFile3 () {
			const excelHeader = this.excelHeader3
			const excelData = this.excelData3
			const filename = '个股占股票资产比例'
			exportExcel(excelHeader, excelData, filename)
    },
    // 导出excel4
		exportExcelFile4 () {
			const excelHeader = this.excelHeader4
			const excelData = this.excelData4
			const filename = '近一年股票资产PE'
			exportExcel(excelHeader, excelData, filename)
    },
    // 导出excel5
		exportExcelFile5 () {
			const excelHeader = this.excelHeader5
			const excelData = this.excelData5
			const filename = '近一年股票资产PB'
			exportExcel(excelHeader, excelData, filename)
    },
    // 导出excel6
		exportExcelFile6 () {
			const excelHeader = this.excelHeader6
			const excelData = this.excelData6
			const filename = '近一年股票流入流出'
			exportExcel(excelHeader, excelData, filename)
    },
    // 表格导出excel
    downloadTableExcel () {
      this.$refs['formQuery'].validate((valid) => {
        if (valid) {
          // 股票分析（股票行业分布）（导出excel）
          this.stockIndustryDistribution(true)
        }
      })
    },
    // 表格导出excel2
    downloadTableExcel2 () {
      this.$refs['formQuery2'].validate((valid) => {
        if (valid) {
					// 股票分析（个股占股票资产比例）（导出excel）
          this.frontShareOfStock(true)
        }
      })
    }
  },
  watch: {
    // 监听组合类型变化
    'formQuery.fundType' (val, oldval) {
      if (val.indexOf('*') != -1 && oldval.indexOf('*') == -1 && val.length > 1) {
        this.formQuery.fundType = ['*']
      } else if (val.indexOf('*') != -1 && oldval.indexOf('*') != -1 && val.length > 1){
        this.formQuery.fundType.splice(val.indexOf('*'), 1)
      }
    },
    // 监听指数类型变化
    'formQuery.targetList' (val, oldval) {
      if (val.indexOf('*') != -1 && oldval.indexOf('*') == -1 && val.length > 1) {
        this.formQuery.targetList = ['*']
      } else if (val.indexOf('*') != -1 && oldval.indexOf('*') != -1 && val.length > 1){
        this.formQuery.targetList.splice(val.indexOf('*'), 1)
      }
    },
    // 监听组合代码变化
    fundCode () {
      this.formQuery.fundList = [this.fundCode]
      // 查询
      this.onQuery()
    },
    // 监听左侧栏
    echartsOpenChild () {
      let timer = setTimeout(() => {
				// 宽度变化重新渲染图表
				this.echartsResize()
				clearTimeout(timer)
			}, 500)
    }
  }
}
</script>

<style lang="scss">
.stockAnalysis{
  .el-dialog{
		width: 70%!important;
	}
  .blue{
    color: #409EFF;
    cursor: pointer;
  }
  .termAverageone_box{
    li{
      height: 25px;
      width: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
      span{
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: #3f3f3f;
      }
    }
  }
  .termAveragetwo_box{
    width: 100%;
    li{
      display: block;
      height: 25px;
      line-height: 25px;
      font-size: 14px;
      color: #3f3f3f;
      // &:nth-child(1){
      //   font-weight: 600;
      //   font-size: 14px;
      // }
    }
  }
}
</style>

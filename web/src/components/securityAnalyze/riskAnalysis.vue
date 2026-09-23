<template>
  <div class="riskAnalysis">
    <div class="forms_table_title"><i class="el-icon-s-data"></i>风险分析</div>
    <!-- 搜索 -->
    <el-form :inline="true" ref="formQuery" :model="formQuery" :rules="rules">
      <el-row>
        <el-col :span="16">
          <el-form-item label="日期" prop="dDate" class="mb20">
            <el-date-picker
              v-model="formQuery.dDate"
              type="date"
              size="small"
              value-format="yyyy-MM-dd"
              @change="handleDateChange"
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
        </el-col>
        <el-col :span="8">
          <el-form-item class="search_button_com">
            <el-button type="primary" size="small" :disabled="btnDisabled" @click="onQuery(1)">查询</el-button>
              <el-button type='primary' plain  @click="resetForm('formQuery')" style='margin-bottom: 5px; ' size='small'><i class='el-icon-delete'></i>重置</el-button>
            <!-- <el-button type="primary" plain icon="el-icon-download"  size="small">导出数据</el-button> -->
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <!--标签卡显示-->
    <el-tag
      :key="tag.id"
      v-for="tag in tags"
      closable
      :disable-transitions="false"
      @close="handleClose(tag)">
      {{tag.label}}
    </el-tag>

    <slot name="tag"></slot>

    <el-row class="mt20">
      <el-col :span="12">
        <div class="text-left">数据日期：<span>{{formQuery.dDate}}</span></div>
      </el-col>
      <el-col :span="12">
        <!-- <div class="text-right">数据断点</div> -->
      </el-col>
    </el-row>
    <div class="border_box mt20 pd10">
      <el-row>
        <el-col :span="12">
          <div class="text-left riskAnalysis_title">最近7天变现比例
            <hint  hintName = "" dimCode = "FX_BX" dimType = "indexHelp"></hint></div>
        </el-col>
        <el-col :span="12">
          <div class="text-right">7天累计变现比例：{{cashInSenvenDayRate | ratioFour}}%
            <span class="upload-wrap" @click="exportExcelFile"><el-tooltip content="下载图表数据" placement="top"><i class="el-icon-s-order"></i></el-tooltip></span>
          </div>
        </el-col>
      </el-row>
      <el-row :gutter="20" class="mt20">
        <el-col :span="12">
          <div id="myEchartsRisk" class="echarts_box"></div>
        </el-col>
        <el-col :span="12">
          <!--列表-->
          <el-table
            :data="tableData"
            :default-sort="{prop: 'fPrice', order: 'descending'}"
            stripe
            border
            max-height="300"
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
              prop="vcSymbol"
              sortable
				      :sort-orders="['ascending', 'descending']"
              label="代码"
              min-width="100"
              header-align="center">
            </el-table-column>
            <el-table-column
              prop="vcName"
              show-overflow-tooltip
              label="简称"
              min-width="120"
              header-align="center">
            </el-table-column>
            <el-table-column
              prop="fPrice"
              sortable
				      :sort-orders="['ascending', 'descending']"
              label="持仓市值(万元)"
              min-width="120"
              header-align="center"
              align="right">
              <template slot-scope="scope">
                {{scope.row.fPrice | moneyMillion}}
              </template>
            </el-table-column>
            <el-table-column
              prop="cashChange"
              sortable
				      :sort-orders="['ascending', 'descending']"
              label="日无冲击变现额(万元)"
              min-width="150"
              header-align="center"
              align="right">
              <template slot-scope="scope">
                {{scope.row.cashChange | moneyMillion}}
              </template>
            </el-table-column>
            <el-table-column
              prop="days"
              sortable
				      :sort-orders="['ascending', 'descending']"
              label="无冲击变现天数"
              min-width="150"
              header-align="center"
              align="right">
            </el-table-column>
          </el-table>

          <Pagination :total="total" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination"></Pagination>
        </el-col>
      </el-row>
    </div>

    <!-- 搜索 -->
    <!-- <el-form :inline="true" ref="formQuery2" :model="formQuery2" :rules="rules2" class="formQuery mt10">
      <el-row>
        <el-col :span="19">
          <el-form-item label="日期" prop="date" class="mb20">
            <el-date-picker
                v-model="formQuery2.date"
                type="daterange"
                unlink-panels
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                value-format="yyyy-MM-dd"
                @change="formDateChange"
                size="small"
                >
              </el-date-picker>
          </el-form-item>
        </el-col>
        <el-col :span="5">
          <el-form-item class="search_button_com">
            <el-button type="primary" size="small" @click="onQuery2">查询</el-button>
            <el-button plain size="small" @click="resetForm('formQuery2')">重置</el-button>
            <el-button type="primary" plain icon="el-icon-download"  size="small">导出数据</el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form> -->

    <el-row :gutter="20">
      <el-col :span="12">
        <div class="border_box mt20 pd10">
          <el-row>
            <el-col :span="12">
              <div class="text-left riskAnalysis_title">利率弹性
                <hint  hintName = "" dimCode = "FX_ZHJQ" dimType = "indexHelp"></hint></div>
            </el-col>
            <el-col :span="12">
              <div class="text-right">期末：{{rateElasticityFinal}}
                <span class="upload-wrap" @click="exportExcelFile2"><el-tooltip content="下载图表数据" placement="top"><i class="el-icon-s-order"></i></el-tooltip></span>
              </div>
            </el-col>
          </el-row>
          <div id="myEchartsRisk2" class="echarts_box"></div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="border_box mt20 pd10">
          <el-row>
            <el-col :span="12">
              <div class="text-left riskAnalysis_title">杠杆比例
                <hint  hintName = "" dimCode = "FX_ZHGG" dimType = "indexHelp"></hint></div>
            </el-col>
            <el-col :span="12">
              <div class="text-right">期末：{{leverageRatiosFinal | ratioFour}}%
                <span class="upload-wrap" @click="exportExcelFile3"><el-tooltip content="下载图表数据" placement="top"><i class="el-icon-s-order"></i></el-tooltip></span>
              </div>
            </el-col>
          </el-row>
          <div id="myEchartsRisk3" class="echarts_box"></div>
        </div>
      </el-col>
    </el-row>

    <!-- <el-row :gutter="20" class="mt20" v-if="isRisk">
      <el-col :span="12">
        <div class="border_box mt20 pd10">
          <el-row>
            <el-col :span="4">
              <div class="text-left riskAnalysis_title">VAR</div>
            </el-col>
            <el-col :span="20">
              <div class="text-right">持有期：
                <el-input v-model="week" type="number" min="1" size="mini" placeholder="" class="week"></el-input>周
                <el-button type="primary" size="mini">设置</el-button>
              </div>
            </el-col>
          </el-row>
          <div id="myEchartsRisk4" class="echarts_box"></div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="border_box mt20 pd10">
          <el-row>
            <el-col :span="12">
              <div class="text-left riskAnalysis_title">贝塔系数</div>
            </el-col>
            <el-col :span="12">
              <div class="text-right">期末：0.1</div>
            </el-col>
          </el-row>
          <div id="myEchartsRisk5" class="echarts_box"></div>
        </div>
      </el-col>
    </el-row> -->
  </div>
</template>

<script>
import * as echarts from 'echarts'
import Pagination from '@/components/Pagination'
import { exportExcel, forEachSeries} from '@/utils/exportExcel'
import commonApi from '@/api/common'
import investmentManagerApi from '@/api/managementView/investmentManager'
import {
  cashInSenvenDayChartsUrl,
  cashInSenvenDayTableUrl,
  rateElasticityUrl,
  leverageRatiosUrl,
  selectEndDateUrl
} from '@/api/riskManage'
import hint from '@/components/hint'
export default {
  name: "risk-analysis",
  components: {
		Pagination,hint
  },
  props: {
    // 是否显示投资经理下拉
    isAccount: {
      type: Boolean,
      default: true
    },
    // 是否显示最后两个图表
    isRisk: {
      type: Boolean,
      default: true
    },
    // 组合代码
    fundCode: {
      type: String,
      default: ''
    },
    // 是否显示组合类型
    isFundType: {
      type: Boolean,
      default: true
    },
    // 标签
    tags: {
      type: Array,
      default: () => {
        return []
      }
    },
    // 是否是流动性风险分析
    isRisk: {
      type: Boolean,
      default: false
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
        dDate: '',
        // 组合类型
        fundTypes: [],
        // 投资经理
        account: '',
        // 排序字段
        orderBy: '"fPrice" desc nulls last',
        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 20
      },
      	// 查询条件2
			formQuery2: {
				// 日期
        date: []
      },
      // 开始日期
      startDate: '',
      // 结束日期
			endDate: '',
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
      },
      // 验证规则2
      rules2:{
        date: [
          { type: 'array', required: true, message: '请选择日期', trigger: 'change' }
        ]
      },
      // 最近7天变现比例图
      myEchartsRisk: null,
      // excel表头
			excelHeader: [],
			// excel数据
			excelData: [],
      // 最近7天变现比例图数据
      echartsData: {},
      // 最近7天变现表
      tableData: [],
      // 总条数
      total: 0,
      // 表格loading
      tableLoading: false,
      /* 按钮禁止与否 */
      isDisabled: false,
      // 7天累计变现比例
      cashInSenvenDayRate: 0,
      // 利率弹性图
      myEchartsRisk2: null,
      // excel表头
			excelHeader2: [],
			// excel数据
			excelData2: [],
      // 利率弹性图数据
      echartsData2: [],
      // 利率弹性期末
      rateElasticityFinal: 0,
      // 杠杆比例图
      myEchartsRisk3: null,
      // excel表头
			excelHeader3: [],
			// excel数据
			excelData3: [],
      // 杠杆比例图数据
      echartsData3: [],
      // 杠杆比例期末
      leverageRatiosFinal: 0,
      // VAR图
      myEchartsRisk4: null,
      // VAR图数据
      echartsData4: {},
      // 贝塔系数图
      myEchartsRisk5: null,
      // 贝塔系数图数据
      echartsData5: {},
      // 周数
      week: '',
      // 查询按钮禁用
      btnDisabled: false
    }
  },
  mounted () {
    // 今天
    // let today = this.$moment().subtract(1,'days').format('YYYY-MM-DD')
    // 日期
    // this.formQuery.dDate = today
    // 接口返回T-1日
    this.formQuery.dDate = this.$store.state.setting.endDate
    // 开始日期
    this.endDate = this.formQuery.dDate
    // 组合类型
    this.formQuery.fundTypes = ['*']
    // 组合类型列表查询
    this.getListEdims()
    if (!this.isAccount) {
      this.formQuery.account = -1
    } else {
      // 投资经理列表查询
      this.getManagerList()
    }
    // 如果选择了日期
    if (this.formQuery.dDate) {
      // 证券分析-返回开始日期
      this.selectEndDate()
    }
    this.$nextTick(() => {
      // 最近7天变现比例图表初始化
      this.initEcharts()
      // 利率弹性图表初始化
      this.initEcharts2()
      // 杠杆比例图表初始化
      this.initEcharts3()
      // 管理视图不需要显示
      if (this.isRisk) {
        // // VAR图表初始化
        // this.initEcharts4()
        // // 贝塔系数图表初始化
        // this.initEcharts5()
      }
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
    // 日期变化
    handleDateChange () {
      // 结束日期
      this.endDate = this.formQuery.dDate
      // 如果选择了日期
      if (this.formQuery.dDate) {
        // 证券分析-返回开始日期
        this.selectEndDate()
      }
    },
    // 查询
    onQuery (page) {
      this.$refs['formQuery'].validate((valid) => {
        if (valid) {
          // 流动性风险分析必须选组合代码
          if (this.isRisk && !this.fundCode) {
            // 先关闭之前实例
			      this.$message.closeAll()
            this.$message({
              message: '请选择组合代码',
              type: 'warning'
            })
            return
          }
          // 禁用搜索按钮
          this.$fun.searchButtonDisabled("btnDisabled", this)
          if (page) this.formQuery.pageNum = 1
          // 最近7天变现图
          this.cashInSenvenDayCharts()
          // 最近7天变现比例表格
          this.cashInSenvenDayTable()
          // 查询2
          // this.onQuery2()
          if (this.endDate) {
            // 流动性风险分析-利率弹性
            this.rateElasticity()
            // 流动性风险分析-杠杆比例
            this.leverageRatios()
          } else {
            // 如果选择了日期
            if (this.formQuery.dDate) {
              // 证券分析-返回开始日期
              this.selectEndDate()
            }
          }
        }
      })
    },
    // 查询2
    onQuery2 () {
      this.$refs['formQuery2'].validate((valid) => {
        if (valid) {
          // 流动性风险分析必须选组合代码
          if (this.isRisk && !this.fundCode) {
            // 先关闭之前实例
			      this.$message.closeAll()
            this.$message({
              message: '请选择组合代码',
              type: 'warning'
            })
            return
          }
          // 流动性风险分析-利率弹性
          this.rateElasticity()
          // 流动性风险分析-杠杆比例
          this.leverageRatios()
        }
      })
    },
    // 日期选择
    formDateChange () {
      if (this.formQuery2.date && this.formQuery2.date.length) {
				// 开始日期
        this.startDate = this.formQuery2.date[0]
        // 结束日期
        this.endDate = this.formQuery2.date[1]
      }
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
          // 流动性风险分析必须选组合代码
          if (this.isRisk && !this.fundCode) {
            // 先关闭之前实例
			      this.$message.closeAll()
            this.$message({
              message: '请选择组合代码',
              type: 'warning'
            })
            return
          }
					// 最近7天变现比例表格
          this.cashInSenvenDayTable()
        }
      })
    },
    // 组合类型列表查询
    getListEdims () {
      // 字典类型
      let params = 'fund_type'
      commonApi.edimsCommon(params).then(res => {
        let { status, data } = res.data
        if (status === 0) {
          this.groupTypeArr = data
        }
      })
    },
    // 投资经理列表查询
    getManagerList () {
      // 权益（1）/固收（2）/混合（0）
      // 风险分析为全部的投资经理
      let params = 0
      investmentManagerApi.managerList(params).then(res => {
        let { status, data } = res.data
        if (status === 0) {
          this.manageArr = data
          if (this.manageArr.length) this.formQuery.account = this.manageArr[0].account
        }
      })
    },
    // 证券分析-返回开始日期
    selectEndDate () {
      let params = {
        // 结束日期
        endDate: this.formQuery.dDate,
        // 标志（1为正推，-1为倒推）
        flag: -1,
        // 所查的时间区间（几天，几周，几月，几年）
        section: 1,
        // 时间类型（0为天，1为周 2为月 3为年）
        type: 3
      }
      selectEndDateUrl(params).then(res => {
        let { status, data } = res
        if (status === 0) {
          // 开始日期
          this.startDate = data
        }
      })
    },
    // 最近7天变现图
    cashInSenvenDayCharts () {
      let params = {
        // 日期
        dDate: this.formQuery.dDate,
        // 组合类型
        fundTypes: this.formQuery.fundTypes.join(','),
        // 组合代码
        fundCodes: this.fundCode,
        // 投资经理
        account: this.formQuery.account
      }
      // 清除空字段
			for (let k in params) {
				if (!params[k] && String(params[k]) !== '0') {
					delete params[k]
				}
			}
      cashInSenvenDayChartsUrl(params).then(res => {
        let { status, data } = res
        if (status === 0) {
          this.echartsData = data
          // 最近7天变现比例图表初始化
          this.initEcharts()
        }
      })
    },
    // 最近7天变现比例表格
    cashInSenvenDayTable (flag) {
      if (!flag) {
        this.tableLoading = true
      } else {
        if (this.isDisabled) return
        this.isDisabled = true
      }
      let params = {
        // 日期
        dDate: this.formQuery.dDate,
        // 组合类型
        fundTypes: this.formQuery.fundTypes.join(','),
        // 组合代码
        fundCodes: this.fundCode,
        // 投资经理
        account: this.formQuery.account,
        // 排序字段
        orderBy: this.formQuery.orderBy,
        // 起始页
        pageNum: this.formQuery.pageNum,
        // 每页数量
        pageSize: this.formQuery.pageSize
      }
      if (flag) {
        params.pageNum = 1
        params.pageSize = 5000
        params.ex_tmp_name = '七天变现列表.xls'
      }
      // 清除空字段
			for (let k in params) {
				if (!params[k] && String(params[k]) !== '0') {
					delete params[k]
				}
			}
      cashInSenvenDayTableUrl(params).then(res => {
        this.tableLoading = false
        this.isDisabled = false
        let { status, data } = res
        if (status === 0) {
          if (flag) { // 下载excel
            if (!data) return
					  this.$fun.commonDownloadUrl(data)
          } else {
            let { list, total } = data
            this.tableData = list
            this.total = total
          }
        }
      }).catch(() => {
        this.tableLoading = false
        this.isDisabled = false
      })
    },
    // 流动性风险分析-利率弹性
    rateElasticity () {
      let params = {
        // 开始时间
        startDate: this.startDate,
        // 结束时间
        endDate: this.endDate,
        // 组合类型
        fundTypes: this.formQuery.fundTypes.join(','),
        // 组合代码
        fundCodes: this.fundCode,
        // 投资经理
        account: this.formQuery.account
      }
      // 清除空字段
			for (let k in params) {
				if (!params[k] && String(params[k]) !== '0') {
					delete params[k]
				}
			}
      rateElasticityUrl(params).then(res => {
        let { status, data } = res
        if (status === 0) {
          this.echartsData2 = data
          if (data.length) this.rateElasticityFinal = data[data.length - 1].duration
          // 利率弹性图表初始化
          this.initEcharts2()
        }
      })
    },
    // 流动性风险分析-杠杆比例
    leverageRatios () {
      let params = {
        // 开始时间
        startDate: this.startDate,
        // 结束时间
        endDate: this.endDate,
        // 组合类型
        fundTypes: this.formQuery.fundTypes.join(','),
        // 组合代码
        fundCodes: this.fundCode,
        // 投资经理
        account: this.formQuery.account
      }
      // 清除空字段
			for (let k in params) {
				if (!params[k] && String(params[k]) !== '0') {
					delete params[k]
				}
			}
      leverageRatiosUrl(params).then(res => {
        let { status, data } = res
        if (status === 0) {
          this.echartsData3 = data
          if (data.length) this.leverageRatiosFinal = data[data.length - 1].leverRatio
          // 杠杆比例图表初始化
          this.initEcharts3()
        }
      })
    },
    // 最近7天变现比例图表初始化
    initEcharts () {
      let echartsData = this.echartsData
      // 横坐标
      let xData = []
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
        // 图表类型
        let type = ''
        // 图表名字
        let name = ''
        if (key === 'rateList') {
          if (echartsData[key].length) {
            this.cashInSenvenDayRate = echartsData[key][0]['totalT']
            delete echartsData[key][0]['totalT']
          }
          type = 'bar'
          name = '变现比例'
        } else {
          type = 'line'
          name = '变现额'
        }
        if (!xData.length) {
          if (echartsData[key].length) {
            xData = Object.keys(echartsData[key][0])
          }
        }
        let seriesObj = {
          name,
          type,
          data: []
        }
        if (type === 'bar') seriesObj.barMaxWidth = 10
        if (echartsData[key].length) {
          seriesObj.data = Object.values(echartsData[key][0])
          seriesObj.data = seriesObj.data.map(item => item.toFixed(2))
        }
        if (key === 'rateList') {
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
      if (this.myEchartsRisk) this.myEchartsRisk.clear()
      this.myEchartsRisk = echarts.init(document.getElementById('myEchartsRisk'))
      this.myEchartsRisk.setOption({
        title: {
          text: ''
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data:['变现额','变现比例'],
          x: 'center'
        },
        grid: {
          left: '6%',
          right: '4.5%',
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
            name: '变现额(万元)',
            type: 'value',
            // max: dataMaxl,
            // min: dataMinl
          },
          {
            name: '变现比例',
            type: 'value',
            axisLabel: {
              formatter: '{value}%'
            },
            // max: dataMaxr,
            // min: dataMinr
          }
        ],
        series: seriesArrs
      })
      // 获取配置信息
      let echartsOption = this.myEchartsRisk.getOption()
			if (echartsOption.series && echartsOption.series.length) {
				// 遍历组装数据
				let { excelHeader, excelData } = forEachSeries(echartsOption)
				// excel表头
				this.excelHeader = excelHeader
				// excel数据
				this.excelData = excelData
			}
    },
    // 利率弹性图表初始化
    initEcharts2 () {
      let echartsData = this.echartsData2
      // 横坐标
      let xData = []
      // 最大值
      // let dataMax = 0
      // 最小值
      // let dataMin = 0
      // 数据数组
      let seriesArrs = []
      echartsData.forEach(item => {
        xData.push(item.dDate)
        seriesArrs.push(item.duration)
      })
      // dataMax = Math.max(...seriesArrs)
      // dataMin = Math.min(...seriesArrs)
      // 数据为空清空echarts
      if (this.myEchartsRisk2) this.myEchartsRisk2.clear()
      this.myEchartsRisk2 = echarts.init(document.getElementById('myEchartsRisk2'))
      this.myEchartsRisk2.setOption({
        title: {
          text: ''
        },
        tooltip: {
          trigger: 'axis'
        },
        // legend: {
        //   data:['总资产久期'],
        //   x: 'center'
        // },
        grid: {
          left: '5.5%',
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
        yAxis: {
          name: '总资产久期',
          type: 'value',
          // max: dataMax,
          // min: dataMin
        },
        // x轴拖动
        dataZoom: [
          {
            show: true,
            realtime: true,
            start: 0,
            end: 100 ,// 结束位置（共100等份）
            bottom: '3%',
          }
        ],
        series: [
          {
            name: '总资产久期',
            type:'line',
            data: seriesArrs
          }
        ]
      })
      // 获取配置信息
      let echartsOption = this.myEchartsRisk2.getOption()
			if (echartsOption.series && echartsOption.series.length) {
				// 遍历组装数据
				let { excelHeader, excelData } = forEachSeries(echartsOption)
				// excel表头
				this.excelHeader2 = excelHeader
				// excel数据
				this.excelData2 = excelData
			}
    },
    // 杠杆比例图表初始化
    initEcharts3 () {
      let echartsData = this.echartsData3
      // 横坐标
      let xData = []
      // 最大值
      // let dataMax = 0
      // 最小值
      let dataMin = 100
      // 数据数组
      let seriesArrs = []
      echartsData.forEach(item => {
        xData.push(item.dDate)
        seriesArrs.push(item.leverRatio)
      })
      // dataMax = Math.max(...seriesArrs)
      // dataMin = Math.min(...seriesArrs)
      // 数据为空清空echarts
      if (this.myEchartsRisk3) this.myEchartsRisk3.clear()
      this.myEchartsRisk3 = echarts.init(document.getElementById('myEchartsRisk3'))
      this.myEchartsRisk3.setOption({
        title: {
          text: ''
        },
        tooltip: {
          trigger: 'axis'
        },
        // legend: {
        //   data:['杠杆比例'],
        //   x: 'center'
        // },
        grid: {
          left: '4.5%',
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
        yAxis: {
          name: '杠杆比例',
          type: 'value',
          // max: dataMax,
          min: dataMin,
          axisLabel: {
            formatter: '{value}%'
          }
        },
        // x轴拖动
        dataZoom: [
          {
            show: true,
            realtime: true,
            start: 0,
            end: 100 ,// 结束位置（共100等份）
            bottom: '3%',
          }
        ],
        series: [
          {
            name: '杠杆比例',
            type:'line',
            data: seriesArrs
          }
        ]
      })
      // 获取配置信息
      let echartsOption = this.myEchartsRisk3.getOption()
			if (echartsOption.series && echartsOption.series.length) {
				// 遍历组装数据
				let { excelHeader, excelData } = forEachSeries(echartsOption)
				// excel表头
				this.excelHeader3 = excelHeader
				// excel数据
				this.excelData3 = excelData
			}
    },
    // VAR图表初始化
    initEcharts4 () {
			// 	// 数据为空清空echarts
			// 	if (this.myEchartsRisk4) this.myEchartsRisk4.clear()
      this.myEchartsRisk4 = echarts.init(document.getElementById('myEchartsRisk4'))
      this.myEchartsRisk4.setOption({
        title: {
          text: ''
        },
        tooltip: {
          trigger: 'axis'
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
        xAxis: {
          type: 'category',
          boundaryGap: true,
          data: ['90%','95%','98%','99%']
        },
        yAxis: {
          // name: '杠杆比例',
          type: 'value',
          axisLabel: {
            formatter: '{value}%'
          }
        },
        series: [
          {
            type:'bar',
            data:[2.32, 2.75, 3.27, 3.62]
          }
        ]
      })
    },
    // 贝塔系数图表初始化
    initEcharts5 () {
			// 	// 数据为空清空echarts
			// 	if (this.myEchartsRisk5) this.myEchartsRisk5.clear()
      this.myEchartsRisk5 = echarts.init(document.getElementById('myEchartsRisk5'))
      this.myEchartsRisk5.setOption({
        title: {
          text: ''
        },
        tooltip: {
          trigger: 'axis'
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
        xAxis: {
          type: 'category',
          boundaryGap: true,
          data: ['2019-03-21','2019-05-20','2019-06-30','2019-07-31']
        },
        yAxis: {
          name: '总资产贝塔系数',
          type: 'value'
        },
        series: [
          {
            type:'line',
            data:[0.02, 0.04, 0.08, 0.1]
          }
        ]
      })
    },
    // 图表变化
    echartsResize () {
      if (this.myEchartsRisk) this.myEchartsRisk.resize()
      if (this.myEchartsRisk2) this.myEchartsRisk2.resize()
      if (this.myEchartsRisk3) this.myEchartsRisk3.resize()
      // 管理视图不需要显示
      if (this.isRisk) {
        // if (this.myEchartsRisk4) this.myEchartsRisk4.resize()
        // if (this.myEchartsRisk5) this.myEchartsRisk5.resize()
      }
    },
    // 关闭标签
    handleClose (index) {
      this.tags.splice(this.tags.indexOf(index), 1)
      // 关闭标签事件
      this.$emit('clearFundCode', '')
    },
    // 当表格的排序条件发生变化的时候会触发该事件
    handleSortChange (val) {
      if (val.order === 'ascending') {
        this.formQuery.orderBy = `"${val.prop}" nulls last` // 升序
      } else {
        this.formQuery.orderBy = `"${val.prop}" desc nulls last` // 降序
      }
      // 最近7天变现比例表格
      this.cashInSenvenDayTable()
    },
    // 导出excel
		exportExcelFile () {
			const excelHeader = this.excelHeader
			const excelData = this.excelData
			const filename = '最近7天变现比例'
      exportExcel(excelHeader, excelData, filename)
      // table导出
      this.$refs['formQuery'].validate((valid) => {
        if (valid) {
          // 流动性风险分析必须选组合代码
          if (this.isRisk && !this.fundCode) {
            // 先关闭之前实例
			      this.$message.closeAll()
            this.$message({
              message: '请选择组合代码',
              type: 'warning'
            })
            return
          }
          // 最近7天变现比例表格（导出excel）
          this.cashInSenvenDayTable(true)
        }
      })
    },
    // 导出excel2
		exportExcelFile2 () {
			const excelHeader = this.excelHeader2
			const excelData = this.excelData2
			const filename = '利率弹性'
			exportExcel(excelHeader, excelData, filename)
    },
    // 导出excel3
		exportExcelFile3 () {
			const excelHeader = this.excelHeader3
			const excelData = this.excelData3
			const filename = '杠杆比例'
			exportExcel(excelHeader, excelData, filename)
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
    // 监听左侧栏
    echartsOpenChild () {
      let timer = setTimeout(() => {
				// 宽度变化重新渲染图表
				this.echartsResize()
				clearTimeout(timer)
			},500)
    }
  }
}
</script>

<style lang="scss" scoped>
.riskAnalysis{
  .text-left{
    text-align: left;
    font-size: 14px;
    span{
      font-weight: bold;
      color: #319ef1;
    }
  }
  .text-right{
    text-align: right;
    font-size: 14px;
    color: #333;
    .week{
      width: 100px!important;
    }
  }
  .upload-wrap{
    margin-left: 5px;
    // line-height: 40px;
    font-size: 13px;
    font-weight: 600;
    color: #319ef1;
    cursor: pointer;
  }
}
  .riskAnalysis_title{
    font-size: 13px;
    font-weight: 600;
    color: #319ef1;
  }
</style>

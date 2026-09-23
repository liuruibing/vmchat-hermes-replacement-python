<template>
  <div class="back-test-analyse">
    <div class="search-content">
      <el-form ref="formQuery" class="standard-form" :inline="true" :model="formInline" :rules="searchRules">
        <el-form-item label="开始日期" prop="beginDate">
          <el-date-picker v-model="formInline.beginDate" placeholder="选择开始日期" size="small" type="date" value-format="yyyy-MM-dd" />
        </el-form-item>
        <el-form-item label="结束日期" prop="endDate">
          <el-date-picker v-model="formInline.endDate" placeholder="选择结束日期" size="small" type="date" value-format="yyyy-MM-dd" />
        </el-form-item>
        <el-form-item>
          <el-button size="small" type="primary" @click="getBackTestData">查询</el-button>
        </el-form-item>
      </el-form>
    </div>
    <el-tabs v-model="activeName" type="border-card">
      <el-tab-pane label="净值走势" name="jzzs">
        <net-value-trend :loading="loading" :net-value-chart-data="netValueChartData" :net-value-table-data="netValueTableData"></net-value-trend>
      </el-tab-pane>
      <el-tab-pane label="持仓时序" name="ccsx">
        <time-series :loading="loading" :time-series-chart-data="timeSeriesChartData" :time-series-table-data="timeSeriesTableData"></time-series>
      </el-tab-pane>
      <el-tab-pane label="动态回撤" name="dthc">
        <dynamic :combine-name="combineName" :be-code-name="beCodeName" :dynamic-chart-data="dynamicChartData" :dynamic-table-data="dynamicTableData" :loading="loading"></dynamic>
      </el-tab-pane>
      <el-tab-pane label="波动率" name="bdl">
        <volatility :loading="loading" :volatility-chart-data="volatilityChartData"></volatility>
      </el-tab-pane>
      <div v-if="$route.path === '/tqgl/cjmnzh'" class="standard-form" style="text-align: center; margin: 5px 0">
        <el-button type="primary" size="small" @click="jumpToList">返回模拟组合列表</el-button>
      </div>
    </el-tabs>
  </div>
</template>

<script>
import netValueTrend from './components/netValueTrend.vue'
import volatility from './components/volatility.vue'
import dynamic from './components/dynamic.vue'
import TimeSeries from './components/timeSeries.vue'
import { queryBackTestData } from './scripts/api'
import moment from 'moment'

export default {
  name: 'BackTestAnalyse',
  components: {
    netValueTrend,
    volatility,
    dynamic,
    TimeSeries
  },
  props: {
    combineCodeValue: {
      required: false,
      default: ''
    }
  },
  data() {
    /** 开始日期校验 */
    const validateStartDate = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请选择开始日期'))
      } else {
        if (this.formInline.endDate !== null || this.formInline.endDate !== undefined || this.formInline.endDate !== '') {
          const startTime = new Date(value)
          const endTime = new Date(this.formInline.endDate)
          if (startTime > endTime) {
            callback(new Error('开始日期不能大于结束日期'))
          } else {
            callback()
          }
        } else {
          callback()
        }
      }
    }
    /** 结束日期校验 */
    const validateEndDate = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请选择结束日期'))
      } else {
        if (this.formInline.beginDate !== null || this.formInline.beginDate !== undefined || this.formInline.beginDate !== '') {
          const startTime = new Date(this.formInline.beginDate)
          const endTime = new Date(value)
          if (startTime > endTime) {
            callback(new Error('结束日期不能小于开始日期'))
          } else {
            callback()
          }
        } else {
          callback()
        }
      }
    }
    return {
      // form表单绑定
      formInline: {
        beginDate: '',
        endDate: '',
        combineCode: ''
      },
      // form校验规则
      searchRules: {
        beginDate: [
          { required: true, message: '请选择开始日期', trigger: 'blur' },
          { validator: validateStartDate, trigger: 'blur' }
        ],
        combineCode: [{ required: true, message: '请输入代码', trigger: 'blur' }],
        endDate: [
          { required: true, message: '请选择结束日期', trigger: 'blur' },
          { validator: validateEndDate, trigger: 'blur' }
        ]
      },
      // 当前激活tab
      activeName: 'jzzs',
      // 净值走势echarts数据
      netValueChartData: [],
      // 净值走势表格数据
      netValueTableData: [],
      // 动态回撤echarts数据
      dynamicChartData: [],
      // 动态回撤表格数据
      dynamicTableData: [],
      // 持仓时序echarts数据
      timeSeriesChartData: [],
      // 持仓时序表格数据
      timeSeriesTableData: [],
      // 波动率数据
      volatilityChartData: [],
      // tab加载状态
      loading: false,
      // 模拟组合名称
      combineName: '',
      beCodeName: ''
    }
  },
  watch: {
    combineCodeValue: {
      handler(val) {
        if (val != '') {
          this.formInline.combineCode = val
        }
      },
      deep: true,
      immediate: true
    }
  },
  activated() {
    if (this.$store.getters.fromPageJump && this.$route.path === '/tqgl/hcfx') {
      this.$store.commit('SET_FROMPAGEJUMP', false)
      const newVal = this.$route.query.groupList
      if (newVal.combineCode) {
        this.beCodeName = this.$route.query.beCodeName
        // 动态修改tag-views dom标签
        document.querySelector('.tags-view-item.active .tag-title') &&
          (document.querySelector('.tags-view-item.active .tag-title').innerText = newVal.combineName + ' 回测分析' || '回测分析')
        // 模拟组合代码
        this.formInline.combineCode = newVal.combineCode
        // 模拟组合名称
        this.combineName = newVal.combineName
        // 默认查询近一年
        this.formInline.endDate = moment().format('YYYY-MM-DD')
        this.formInline.beginDate = newVal.foundDate
        // 获取回测分析数据
        this.$nextTick(() => {
          this.getBackTestData()
        })
      } else {
        this.formInline.combineCode = ''
        this.beCodeName = ''
      }
    }
  },
  methods: {
    jumpToList() {
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/tqgl/mnzh/mnzh',
        query: {
          list: {
            FUNDNAME: undefined
          }
        }
      })
    },
    /**
     * @description 获取回测分析tab数据
     */
    getBackTestData() {
      const data = {
        ...this.formInline
      }
      this.loading = true
      this.$refs.formQuery.validate(async (valid) => {
        if (valid) {
          try {
            const res = await queryBackTestData(data)
            if (res.data.status === 0) {
              // 净值走势
              this.netValueChartData = res.data.data['JZZS_ECHARTS'] || []
              this.netValueTableData = res.data.data['JZZS_TABLE'] || []
              // 动态回撤
              this.dynamicChartData = res.data.data['DTHC_ECHARTS'] || []
              this.dynamicTableData = res.data.data['DTHC_TABLE'] || []
              // 持仓时序
              this.timeSeriesChartData = res.data.data['CCSX_ECHARTS'] || []
              this.timeSeriesTableData = res.data.data['CCSX_TABLE'] || []
              // 波动率
              this.volatilityChartData = res.data.data['BDL_ECHARTS'] || []
              this.loading = false
            } else {
              this.$message({
                type: 'error',
                customClass: 'message-error',
                message: res.message || '获取数据失败'
              })
              this.loading = false
            }
          } catch (e) {
            this.loading = false
          }
        } else {
          return false
        }
      })
    },
    // 设置开始时间结束时间
    dateInit(beginDate) {
      if (beginDate == this.getBeforeDate(0)) {
        this.formInline.beginDate = beginDate
        this.formInline.endDate = beginDate
      } else {
        this.formInline.beginDate = beginDate
        this.formInline.endDate = this.getBeforeDate(1)
      }
    },
    getBeforeDate(val) {
      // 获取当前日期
      const today = new Date()

      // 将当前日期减去一天
      const yesterday = new Date(today.getTime() - val * 24 * 60 * 60 * 1000)

      // 获取年、月、日
      const year = yesterday.getFullYear()
      const month = String(yesterday.getMonth() + 1).padStart(2, '0')
      const day = String(yesterday.getDate()).padStart(2, '0')

      // 格式化为 YYYY-MM-DD 形式
      return `${year}-${month}-${day}`
    }
  }
}
</script>

<style lang="scss" scoped>

.back-test-analyse {
   padding: 5px;
  .search-content {
    //background-color: #f7f7f7;
    ::v-deep .el-input.el-input--small .el-input__inner {
      background-color: #f7f7f7;
    }
    ::v-deep .el-form--inline .el-form-item {
      margin-bottom: 0px !important;
    }
  }

  ::v-deep .el-tabs__item {
    height: 40px !important;
    line-height: 40px !important;
  }

  ::v-deep .el-tabs__content {
    padding: 0;
  }

  // 修改tab切换样式
  ::v-deep .el-tabs__item {
    border-left: 1px solid #E4E7ED;
    border-right: 1px solid #E4E7ED;
    border-top: 2px solid transparent;
    color: #612d10;
    background-color: #fcf8f4 !important;;
  }

  .el-tabs__item:first-child {
    border-left: none;
  }

  ::v-deep .el-tabs__item:hover {
    //color: #0F65DD;
  }

  ::v-deep .el-tabs__item.is-active {
    //border-top: 2px solid #612d10;
    color: #612d10;
    background-image: linear-gradient(to right, #f5d7bc, #e0b794) !important;
    //font-weight: bold;
  }
  ::v-deep .el-tabs--border-card > .el-tabs__header{
    color: #612d10;
  }

}
</style>

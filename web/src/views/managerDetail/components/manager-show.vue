<template>
  <div class="manager-show">
    <div class="search-content">
      <el-row>
        <el-form ref="searchForm" :inline="true" :model="simpleSearch" :rules="rules">
          <el-row justify="start" type="flex">
            <el-form-item label="" prop="endDate">
              <el-date-picker v-model="simpleSearch.endDate" :clearable="false" placeholder="选择日期" size="small" type="date" value-format="yyyy-MM-dd" />
            </el-form-item>
            <el-form-item class="dbjz" label="">
              <el-select v-model="simpleSearch.baseCode" clearable collapse-tags multiple placeholder="对比指数" size="small" @change="changeContrasCode">
                <el-option v-for="item in contrasStandardOpts" :key="item.id + 'contras'" :label="item.label + '(' + item.id + ')'" :value="item.id"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="">
              <el-select class="dimensionality" v-model="simpleSearch.dimensionality" clearable placeholder="计算维度" size="small">
                <el-option v-for="item in calculateOps" :key="item.DIM_CDE + 'calculate'" :label="item.DIM_NME" :value="item.DIM_CDE"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button size="small" type="primary" @click="handleQueryChart">查询</el-button>
              <el-button size="small" type="info" plain @click="reset" icon="el-icon-refresh">重置</el-button>
            </el-form-item>
          </el-row>
        </el-form>
      </el-row>
    </div>
    <div class="history-earn">
      <div class="title">
        <div class="title-icon">
          <div class="color-box"></div>
        </div>
        <div class="title-txt">
          <span>历史走势收益图</span>
          <el-tooltip effect="dark" content="管理人净值取自私募排排" placement="top">
            <svg-icon class="tip" icon-class="wenhao"></svg-icon>
          </el-tooltip>
        </div>
        <div class="title-select">
          <el-select style="width: 120px !important; float: right" v-model="frequencyCode" placeholder="请选择" size="mini" clearable @change="handleFrequencyChange">
            <el-option v-for="item in frequencyOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </div>
        <div class="title-radio">
          <el-radio v-for="item in radioGroup" :key="item.value" v-model="sectionRadio" :label="item.value" @input="handleDateChange">
            {{ item.label }}
          </el-radio>
        </div>
      </div>
      <div v-loading="historyLoading" class="content">
        <div class="content-left">
          <myChart id="lssyzst" ref="lssyzst" :options="historyOptions" class="echarts_box" resize-dom="cmbfof" />
        </div>
        <div class="content-right">
          <div class="table-date mb10">日期：{{ historyDate }}</div>
          <el-table :data="historyTableData" :header-cell-style="{ color: '#333', height: '60px', background: '#fff!important' }" stripe style="width: 100%">
            <el-table-column
              v-for="(col, i) in historyTableColumns"
              :key="i"
              :align="col.align"
              :header-align="col.headerAlign"
              :label="col.label"
              :prop="col.prop"
              show-overflow-tooltip
            >
              <template slot-scope="scope">
                <span v-if="['YIELD', 'NHJZ', 'T_POINT'].includes(col.prop)">
                  <span v-if="scope.row[col.prop]">
                    <span v-if="scope.row[col.prop] == '-'">
                      {{ scope.row[col.prop] | noDataFilter }}
                    </span>
                    <span v-else>
                      <span v-if="scope.row[col.prop] > 0" style="color: #d32f2f">
                        <span v-if="col.prop == 'YIELD'">
                          {{ scope.row[col.prop] | numberToFixedStr(4, 100, '%') }}
                        </span>
                        <span v-else>
                          {{ scope.row[col.prop] | noDataFilter }}
                        </span>
                      </span>
                      <span v-else-if="scope.row[col.prop] < 0" style="color: #098c09">
                        <span v-if="col.prop == 'YIELD'">
                          {{ scope.row[col.prop] | numberToFixedStr(4, 100, '%') }}
                        </span>
                        <span v-else>
                          {{ scope.row[col.prop] | noDataFilter }}
                        </span>
                      </span>
                      <span v-else>{{ scope.row[col.prop] | noDataFilter }}%</span>
                    </span>
                  </span>
                  <span v-else>{{ scope.row[col.prop] | noDataFilter }}</span>
                </span>
                <span v-else>{{ scope.row[col.prop] | noDataFilter }}</span>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </div>
    <div class="kpi-analyse">
      <div class="title">
        <div class="title-icon">
          <div class="color-box"></div>
        </div>
        <div class="title-txt">
          <span>业绩分析</span>
          <el-tooltip effect="dark" content="管理人数据取自私募排排" placement="top">
            <svg-icon class="tip" icon-class="wenhao"></svg-icon>
          </el-tooltip>
        </div>
      </div>
      <div v-loading="kpiLoading" class="content">
        <div class="content-middle">
          <div class="content-middle-left">
            <myChart id="yjfx" ref="yjfx" :options="kpiAnalyseOptions" class="echarts_box" resize-dom="cmbfof" />
          </div>
          <div class="content-middle-right">
            <el-table :data="kpiAnalyseMiddleTableData" :header-cell-style="{ color: '#333', height: '60px', background: '#fff!important' }" stripe style="width: 100%">
              <el-table-column
                v-for="(col, i) in kpiAnalyseMiddleTableColumns"
                :key="i"
                :align="col.align"
                :header-align="col.headerAlign"
                :label="col.label"
                :prop="col.prop"
                show-overflow-tooltip
              >
                <template slot-scope="scope">
                  <span
                    v-if="scope.row[col.prop] && col.prop !== 'c0'"
                    :style="{
                      color: Number(scope.row[col.prop]) < 0 ? '#098c09' : '#d32f2f'
                    }"
                  >
                    {{ scope.row[col.prop] | numberToFixedStr(2, 100, '%') }}
                  </span>
                  <span v-else>{{ scope.row[col.prop] | noDataFilter }}</span>
                </template>
              </el-table-column>
            </el-table>
            <div class="table-date mt10">计算日期： {{ kpiCalculateDate }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import request from '@/utils/request'
import myChart from '@/components/Echarts'
import { dateShortcutMap, HISTORY_TABLE_COLUMNS, STATIST_PERIOD_OPTIONS } from './manager-show-core/historyConstants'
import { merger } from '@/utils'
import { frequencyOptions } from '@/dataDictionary/frequency'

export default {
  components: {
    myChart
  },
  props: {
    currentList: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      simpleSearch: {
        endDate: '',
        baseCode: [],
        dimensionality: ''
      },
      contrasStandardOpts: [],
      calculateOps: [],

      historyOptions: {},
      historyTableColumns: HISTORY_TABLE_COLUMNS,
      historyTableData: [],
      historyLoading: false,

      kpiAnalyseOptions: {},
      kpiAnalyseMiddleTableColumns: [],
      kpiAnalyseMiddleTableData: [],
      kpiXdata: [],
      kpiLoading: false,

      radioGroup: STATIST_PERIOD_OPTIONS,
      sectionRadio: '4',
      managerCode: '',
      startDate: '',
      foundDate: '',
      kpiCalculateDate: '',
      historyDate: '',

      rules: {
        endDate: [{ type: 'string', required: true, message: '请选择截止日期', trigger: 'change' }]
      },
      frequencyOptions: frequencyOptions,
      frequencyCode: 'W'
    }
  },
  watch: {
    managerCode: {
      async handler(val) {
        if (val) {
          await this.getEndDate()
          await this.getContrasOptions()
          await this.getCalculateOptions()
          this.handleDateChange('4')
          this.handleQuerykpiAnalyse()
          this.handleQueryHistory('W')
        }
      }
    },
    currentList: {
      handler(val) {
        if (val) {
          this.foundDate = val.ESTABLISH_DATE || ''
        }
      },
      deep: true
    }
  },
  methods: {
    /**
     * @description 监听历史收益走势图频率下拉
     */
    handleFrequencyChange(val) {
      this.handleQueryHistory(val)
    },
    /**
     * @description 统计周期区间映射
     */
    handleDateChange(val) {
      if (val === '6') {
        this.startDate = this.foundDate || ''
      } else {
        this.startDate = dateShortcutMap[val].onClick()[0] || ''
      }
      this.handleQueryHistory(this.frequencyCode)
    },
    /**
     * @description 获取管理人表现 - 历史收益走势图数据
     */
    handleQueryHistory(val) {
      if (this.simpleSearch.baseCode && this.simpleSearch.baseCode.length <= 0) {
        this.$message.closeAll()
        this.$message.warning('对比指数不能为空')
        return
      }
      const params = {
        ...this.simpleSearch,
        baseCode: this.simpleSearch.baseCode.join(','),
        managerCode: this.managerCode,
        startDate: this.startDate,
        rate: val ? val : ''
      }
      this.historyLoading = true
      request({
        url: `/api/report/v1.0/data/sql/d26ca81d-1ab2-41c4-a93f-ac6a983ad066`,
        method: 'post',
        data: {
          indexCode: 'd26ca81d-1ab2-41c4-a93f-ac6a983ad066',
          ...params
        }
      })
        .then((res) => {
          if (res.data.status === 0) {
            this.historyLoading = false
            const resultData = res.data.data || []
            this.historyChart(resultData)
          } else {
            this.historyLoading = false
          }
        })
        .catch((err) => {
          this.historyLoading = false
        })
    },
    /**
     * @description 组装echarts - options
     */
    historyChart(data) {
      const xData = [...new Set(data.map((item) => item.D_DATE))]
      const legendData = []
      const seriesData = []
      const mergeData = merger(data, 'COMPANY_SHORT_NAME')
      mergeData.forEach((item) => {
        const tempOrigin = []
        const seriesObj = {
          name: item.COMPANY_SHORT_NAME,
          type: 'line',
          symbol: 'none',
          smooth: true,
          lineStyle: {
            normal: {
              width: 0.5
            }
          },
          data: []
        }
        legendData.push({ name: item.COMPANY_SHORT_NAME, icon: 'roundRect' })
        for (let i = 0; i < xData.length; i++) {
          const temp = xData[i]
          const objExample = {}
          objExample.D_DATE = temp
          objExample.COMPANY_SHORT_NAME = item.COMPANY_SHORT_NAME
          const obj = item.origin.find((sitem) => sitem.D_DATE == temp) || objExample
          tempOrigin.push(obj)
        }
        item.origin = tempOrigin
        seriesObj.data = item.origin.map((item) => item.T_POINT)
        seriesData.push(seriesObj)
      })
      let dataAll = []
      seriesData.forEach((item) => {
        dataAll.push(...item.data)
      })
      dataAll = dataAll.filter((item) => item !== undefined)
      const y0Max = Math.max(...dataAll)
      const y0Min = Math.min(...dataAll)
      this.historyOptions = {
        tooltip: {
          trigger: 'axis',
          formatter: (params) => {
            this.handleHistoryTableData(mergeData, params)
            var relVal = params[0].name
            for (var i = 0, l = params.length; i < l; i++) {
              relVal += '<br/>' + params[i].marker + params[i].seriesName + '：' + (params[i].value ? params[i].value : '-')
            }
            return relVal
          }
        },
        color: ['#5196dd', '#e16757', '#faa000', '#97E675', '#B354AE'],
        legend: {
          y: '4%',
          data: legendData
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '15%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          axisTick: {
            show: false
          },
          data: xData
        },
        yAxis: [
          {
            type: 'value',
            max: y0Max,
            min: y0Min,
            axisLabel: {
              formatter: '{value} '
            },
            splitLine: {
              show: true,
              lineStyle: {
                type: 'solid',
                color: '#ececec'
              }
            },
            name: '净值'
          }
        ],
        dataZoom: {
          // type: 'slider',
          show: true,
          // start: 0,
          // end: 50,
          textStyle: {
            fontSize: 12,
            color: 'transparent'
          }
        },
        series: seriesData
      }
      this.handleHistoryTableDataByEndValue(mergeData)
      // this.handleHistoryTableData(mergeData, [{ axisValue: xData[xData.length -1] }])
    },

    handleHistoryTableDataByEndValue(mergeData) {
      // 从最后开始往前找

      for (let i = mergeData.length - 1; i >= 0; i--) {
        let temp = mergeData[i]
        if (temp.origin) {
          for (let j = temp.origin.length - 1; j >= 0; j--) {
            let stemp = temp.origin[j]
            if (stemp.NHJZ || stemp.T_POINT || stemp.YIELD) {
              this.historyDate = stemp.D_DATE
              this.handleHistoryTableData(mergeData, [{ axisValue: stemp.D_DATE }])
              return
            }
          }
        }
      }
    },

    /**
     * @description 历史走势收益图 - 表格
     */
    handleHistoryTableData(data, line) {
      const curTime = line[0].axisValue
      this.historyDate = curTime
      const tableData = []
      for (const item of data) {
        const obj = item.origin.find((child) => child.D_DATE === curTime)
        obj && tableData.push(obj)
      }
      this.historyTableData = tableData
    },
    /**
     * @description 查询
     */
    handleQueryChart() {
      this.handleQueryHistory(this.frequencyCode)
      this.handleQuerykpiAnalyse()
    },
    /**
     * @description 获取管理人表现 - 业绩分析数据
     */
    handleQuerykpiAnalyse() {
      if (this.simpleSearch.baseCode && this.simpleSearch.baseCode.length <= 0) {
        this.$message.closeAll()
        this.$message.warning('对比指数不能为空')
        return
      }
      const params = {
        ...this.simpleSearch,
        baseCode: this.simpleSearch.baseCode.join(','),
        managerCode: this.managerCode
      }
      this.kpiLoading = true
      request({
        url: `/api/report/v1.0/data/sql/c99aa840-5138-4aa3-8cc5-dd92b40683bf`,
        method: 'post',
        data: {
          indexCode: 'c99aa840-5138-4aa3-8cc5-dd92b40683bf',
          ...params
        }
      })
        .then((res) => {
          if (res.data.status === 0) {
            const resultData = res.data.data || []
            this.kpiLoading = false
            this.kpiAnalyseChart(resultData)
            this.kpiAnalyseTableColumns(resultData)
            this.kpiAnalyseTableData(resultData)
          } else {
            this.kpiLoading = false
          }
        })
        .catch((err) => {
          this.kpiLoading = false
        })
    },
    /**
     * @description 组装echarts - options
     */
    kpiAnalyseChart(data) {
      if (data && data.length) {
        const color = ['#5196dd', '#e16757', '#faa000', '#97E675', '#B354AE']
        const legendData = data.map((item) => item.COMPANY_SHORT_NAME)
        this.kpiXdata = ['近一月', '近三月', '近六月', '近一年', '近三年', '今年以来', '成立以来']
        const seriesData = []
        data.forEach((item, index) => {
          if (item.RN === 'GLR') this.kpiCalculateDate = item.D_END_DATE || '-'
          const seriesObj = {
            name: item.COMPANY_SHORT_NAME,
            type: 'bar',
            barWidth: '20px',
            color: color[index],
            data: [
              item.YIELD_1M ? (item.YIELD_1M * 100).toFixed(2) : '-',
              item.YIELD_3M ? (item.YIELD_3M * 100).toFixed(2) : '-',
              item.YIELD_6M ? (item.YIELD_6M * 100).toFixed(2) : '-',
              item.YIELD_1Y ? (item.YIELD_1Y * 100).toFixed(2) : '-',
              item.YIELD_3Y ? (item.YIELD_3Y * 100).toFixed(2) : '-',
              item.YIELD_YTD ? (item.YIELD_YTD * 100).toFixed(2) : '-',
              item.YIELD_INCEP ? (item.YIELD_INCEP * 100).toFixed(2) : '-'
            ]
          }
          seriesData[index] = seriesObj
        })
        this.kpiAnalyseOptions = {
          tooltip: {
            trigger: 'axis',
            formatter: function (params) {
              var relVal = params[0].name
              for (var i = 0, l = params.length; i < l; i++) {
                relVal += '<br/>' + params[i].marker + params[i].seriesName + '：' + params[i].value + '%'
              }
              return relVal
            }
          },
          legend: {
            top: '5%',
            data: legendData
          },
          grid: {
            top: '20%',
            left: '3%',
            right: '4%',
            bottom: '5%',
            containLabel: true
          },
          yAxis: [
            {
              type: 'value',
              name: '收益率（%）',
              axisLabel: {
                show: true,
                interval: 'auto',
                formatter: '{value} %'
              },
              splitLine: {
                show: true,
                lineStyle: {
                  type: 'solid',
                  color: '#ececec'
                }
              },
              show: true
            }
          ],
          xAxis: [
            {
              type: 'category',
              axisLabel: {
                interval: 0,
                show: true,
                splitNumber: 15,
                textStyle: {
                  fontSize: 10,
                  color: '#000'
                }
              },
              axisTick: {
                show: false
              },
              data: this.kpiXdata
            }
          ],
          series: seriesData
        }
      }
    },
    /**
     * @description 业绩分析数据 - 动态列
     */
    kpiAnalyseTableColumns(data) {
      const kpiTableColumn = [
        {
          prop: 'c0',
          label: '管理人/对比指标',
          align: 'center',
          headerAlign: 'center'
        }
      ]
      data.forEach((item, index) => {
        const columnObj = {
          prop: 'c' + (index + 1),
          label: item.COMPANY_SHORT_NAME,
          align: 'center',
          headerAlign: 'center'
        }
        kpiTableColumn.push(columnObj)
      })
      this.kpiAnalyseMiddleTableColumns = kpiTableColumn
    },
    /**
     * @description 业绩分析数据 - 列转行
     */
    kpiAnalyseTableData(data) {
      let kpiTableData = []
      this.kpiXdata.forEach((item) => {
        const kpiTableRow = {
          c0: item
        }
        kpiTableData.push(kpiTableRow)
      })
      let YIELD_1M = {},
        YIELD_3M = {},
        YIELD_6M = {},
        YIELD_1Y = {},
        YIELD_3Y = {},
        YIELD_YTD = {},
        YIELD_INCEP = {}
      let index = 0
      data.forEach((item) => {
        YIELD_1M['c' + (index + 1)] = item.YIELD_1M || ''
        YIELD_3M['c' + (index + 1)] = item.YIELD_3M || ''
        YIELD_6M['c' + (index + 1)] = item.YIELD_6M || ''
        YIELD_1Y['c' + (index + 1)] = item.YIELD_1Y || ''
        YIELD_3Y['c' + (index + 1)] = item.YIELD_3Y || ''
        YIELD_YTD['c' + (index + 1)] = item.YIELD_YTD || ''
        YIELD_INCEP['c' + (index + 1)] = item.YIELD_INCEP || ''
        index++
      })
      const rowData = [YIELD_1M, YIELD_3M, YIELD_6M, YIELD_1Y, YIELD_3Y, YIELD_YTD, YIELD_INCEP]
      kpiTableData = kpiTableData.map((item, i) => {
        return {
          ...item,
          ...rowData[i]
        }
      })
      this.kpiAnalyseMiddleTableData = kpiTableData
    },
    /**
     * @description 监听对比基准下拉
     */
    changeContrasCode(val) {
      if (val.length > 4) {
        this.$message({
          type: 'warning',
          message: '对比指数最多只能选四个'
        })
        this.simpleSearch.baseCode.splice(-1)
      }
    },
    /**
     * @description 获取对比基准下拉
     */
    getContrasOptions() {
      return new Promise((resolve, reject) => {
        request({
          url: `/api/report/v1.0/data/sql/ecd8867c-64cc-4ebc-9070-04524b04b72c`,
          method: 'post',
          data: {
            indexCode: 'ecd8867c-64cc-4ebc-9070-04524b04b72c'
          }
        })
          .then((res) => {
            if (res.data.status === 0) {
              const resultDim = res.data.data || []
              this.contrasStandardOpts = resultDim.map((item) => {
                return {
                  label: item.DIM_NME,
                  id: item.DIM_CDE
                }
              })
              this.simpleSearch.baseCode = ['000300', '000905']
              resolve()
            }
          })
          .catch((err) => {
            reject(err)
          })
      })
    },
    /**
     * @description 获取计算维度下拉
     */
    getCalculateOptions() {
      return new Promise((resolve, reject) => {
        request({
          url: `/api/report/v1.0/data/sql/1c5c7b0a-3023-4f89-a040-511d640bdbde`,
          method: 'post',
          data: {
            indexCode: '1c5c7b0a-3023-4f89-a040-511d640bdbde'
          }
        })
          .then((res) => {
            if (res.data.status === 0) {
              this.calculateOps = res.data.data || []
              if (this.calculateOps.length > 0) {
                this.simpleSearch.dimensionality = this.calculateOps[0].DIM_CDE
              }
              resolve()
            }
          })
          .catch((err) => {
            reject(err)
          })
      })
    },
    /**
     * @description 获取截止日期
     */
    getEndDate() {
      return new Promise((resolve, reject) => {
        const params = {
          indexCode: 'bc4ab85f-fb95-449a-948e-a3bb49227850'
        }
        request({
          url: `/api/report/v1.0/data/sql/bc4ab85f-fb95-449a-948e-a3bb49227850`,
          method: 'post',
          data: params
        })
          .then((res) => {
            if (res.data.status === 0) {
              this.simpleSearch.endDate = res.data.data[0].D_DATE
              resolve()
            }
          })
          .catch((err) => {
            reject(err)
          })
      })
    },
    reset() {
      this.simpleSearch.endDate = ''
      this.simpleSearch.baseCode = []
      this.simpleSearch.dimensionality = ''
    }
  }
}
</script>
<style lang="scss" scoped>
.manager-show {
  min-height: 900px;
  overflow: auto;
  margin-bottom: 20px;
  padding: 15px;

  .search-content {
    width: 100%;

    .dbjz {
      ::v-deep .el-select .el-input--small {
        width: 260px !important;
      }

      ::v-deep .el-select .el-select__tags {
        max-width: 234px !important;
      }
    }
  }

  .history-earn {
    .content {
      display: flex;
      align-items: center;

      .content-left {
        flex: 5;
        margin: 0 40px 0 20px;
      }

      .content-right {
        flex: 3;
        margin-right: 20px;
        .table-date {
          color: #0F65DD;
        }
      }
    }
  }

  .kpi-analyse {
    margin-top: 20px;

    .content-middle {
      margin: 10px 0;
      display: flex;
      align-items: center;

      .content-middle-left {
        flex: 5;
        margin: 0 40px 0 20px;
      }

      .content-middle-right {
        flex: 3;
        margin-right: 20px;
        .table-date {
          color: #0F65DD;
        }
      }
    }
  }

  .title {
    padding: 10px 0;
    border-bottom: 1px solid #0F65DD;

    .title-icon {
      vertical-align: middle;
      display: inline-block;
    }

    .color-box {
      display: inline-block;
      height: 27px;
      width: 3px;
      background-color: #0F65DD;
    }

    .title-txt {
      color: #0F65DD;
      vertical-align: middle;
      height: 35px;
      line-height: 35px;
      font-size: 16px;
      margin-left: 5px;
      display: inline-block;
    }

    .tip:hover {
      cursor: pointer;
    }

    .title-radio {
      float: right;
      height: 35px;
      line-height: 35px;
    }
    .title-select {
      float: right;
      height: 35px;
      line-height: 35px;
      margin-left: 20px;
    }

    .echarts_box {
      height: 380px;
      width: 100%;
    }
  }

  ::v-deep .el-radio__input.is-checked .el-radio__inner {
    border-color: #0F65DD;
    background: #0F65DD;
  }

  ::v-deep .el-radio__inner:hover {
    border-color: #0F65DD;
  }

  ::v-deep .el-radio__input.is-checked + .el-radio__label {
    color: #0F65DD;
  }
}
</style>

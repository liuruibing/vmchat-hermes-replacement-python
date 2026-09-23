<template>
  <div class="emotional-index">
    <div class="funds-filter search-content">
      <el-form :inline="true" :model="formQuery">
        <el-row>
          <el-form-item label="">
            <el-select v-model="formQuery.statistPeriod" placeholder="统计周期" size="small" @change="handleDateChange">
              <el-option v-for="item in statistPeriodOpts" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
            <el-date-picker v-model="formQuery.startDate" :disabled="disabledDate" placeholder="开始日期" size="small" type="date" value-format="yyyy-MM-dd"></el-date-picker>
            <el-date-picker v-model="formQuery.endDate" :disabled="disabledDate" placeholder="结束日期" size="small" type="date" value-format="yyyy-MM-dd"></el-date-picker>
          </el-form-item>
          <el-form-item class="dbjz" label="">
            <el-select v-model="formQuery.contrasCode" clearable collapse-tags multiple placeholder="对比指数" size="small" @change="changeContrasCode">
              <el-option v-for="item in contrasStandardOpts" :key="item.id" :label="item.label + '(' + item.id + ')'" :value="item.id"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button size="small" type="primary" @click="handleQueryChartData" icon="el-icon-search">
              查询
            </el-button>
            <el-button size="small" plain type="info" @click="reset" icon="el-icon-refresh-left">重置</el-button>
          </el-form-item>
        </el-row>
      </el-form>
    </div>
    <div class="chart-main">
      <div class="target-trend" style="margin-bottom: 30px">
        <div class="chart-title">
          <div class="title-icon">
            <div class="color-box"></div>
          </div>
          <div class="title-txt">
            指标走势
            <el-tooltip class="table_header_icon" effect="dark" placement="top">
              <span slot="content">
                广发情绪指数:分市场情绪指数与投资者情绪指数，市场情绪指数基于股票策略股票仓位编制，反应基金经理对于股票市场的投资热度；投资者情绪指数基于私募净申购数据编制，反应私募市场投资者投资私募基金的热度
              </span>
              <i class="el-icon-question" style="cursor: pointer;"></i>
            </el-tooltip>
          </div>
        </div>
        <div class="chart-content">
          <myChart id="zbzs" ref="zbzs" :options="targetTrendOptions" class="echarts_box" resize-dom="cmbfof" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { dateShortcutMap, STATIST_PERIOD_OPTIONS } from './scripts/constants'
import request from '@/utils/request'
import myChart from '@/components/Echarts'
import { merger } from '@/utils'
import commonAPI from '@/api/common.js'

export default {
  name: 'EmotionalIndex',
  components: {
    myChart
  },
  data() {
    return {
      formQuery: {
        statistPeriod: '4',
        startDate: '',
        endDate: '',
        contrasCode: []
      },
      estabStartDate: '', // 成立以来开始时间
      disabledDate: true,
      dateShortcutMap,
      statistPeriodOpts: STATIST_PERIOD_OPTIONS,
      contrasStandardOpts: [],
      targetTrendOptions: {}
    }
  },
  async mounted() {
    this.handleDateChange('4')
    await this.getContrasOptions()
    await this.getStartDateFromEstab()
    this.handleQueryChartData()
  },

  methods: {
    /**
     * @description 查询成立以来开始日期
     */
    getStartDateFromEstab() {
      return new Promise((resolve, reject) => {
        const params = {}
        params.indexCode = '741cb4cc-7893-43f5-bb7e-317efe0d7583'
        commonAPI
          .getDataBysqlCode(params)
          .then(res => {
            const { status, data } = res.data
            if (status === 0) {
              if (data && data instanceof Array && data.length > 0) {
                this.estabStartDate = data[0].STARTDATE
              } else {
                this.estabStartDate = new Date().getFullYear() + '-' + (new Date().getMonth() + 1) + '-' + new Date().getDate()
              }
            } else {
              this.estabStartDate = new Date().getFullYear() + '-' + (new Date().getMonth() + 1) + '-' + new Date().getDate()
            }
            resolve()
          })
          .catch(() => {
            resolve()
          })
      })
    },

    getCurrentOrPreviousDay(date) {
      const currentDate = new Date()
      const inputDate = new Date(date)

      // 获取当前年月日
      const currentYear = currentDate.getFullYear()
      const currentMonth = currentDate.getMonth() + 1 // 月份从 0 开始，所以需要加 1
      const currentDay = currentDate.getDate()

      // 获取传入日期的年月日
      const inputYear = inputDate.getFullYear()
      const inputMonth = inputDate.getMonth() + 1 // 月份从 0 开始，所以需要加 1
      const inputDay = inputDate.getDate()

      // 如果传入日期大于当前日期，返回传入日期
      if (
        inputYear > currentYear ||
        (inputYear === currentYear && inputMonth > currentMonth) ||
        (inputYear === currentYear && inputMonth === currentMonth && inputDay > currentDay)
      ) {
        return this.formatDate(inputDate)
      }

      // 如果传入日期等于当前日期，返回当前日期
      if (inputYear === currentYear && inputMonth === currentMonth && inputDay === currentDay) {
        return this.formatDate(currentDate)
      }

      // 否则返回当前日期的前一天
      const previousDay = new Date(currentYear, currentMonth - 1, currentDay - 1)
      return this.formatDate(previousDay)
    },

    // 格式化日期为"YYYY-MM-DD"格式
    formatDate(date) {
      const year = date.getFullYear()
      const month = this.padZero(date.getMonth() + 1)
      const day = this.padZero(date.getDate())
      return `${year}-${month}-${day}`
    },

    // 补零函数
    padZero(num) {
      return String(num).padStart(2, '0')
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
          .then(res => {
            if (res.data.status === 0) {
              const resultDim = res.data.data || []
              this.contrasStandardOpts = resultDim.map(item => {
                return {
                  label: item.DIM_NME,
                  id: item.DIM_CDE
                }
              })
              this.contrasStandardOpts.forEach(item => {
                if (item.id === '000300' || item.id === 'H11001') {
                  this.formQuery.contrasCode.push(item.id)
                }
              })
            }
            resolve()
          })
          .catch(err => {
            resolve()
          })
      })
    },
    /**
     * @description 统计周期区间映射
     */
    handleDateChange(val) {
      if (!val) {
        this.disabledDate = true
        this.formQuery.startDate = ''
        this.formQuery.endDate = ''
        return
      }
      if (val === '7') {
        this.disabledDate = false
      } else if (val === '6') {
        this.disabledDate = true
        this.formQuery.startDate = this.estabStartDate
        this.formQuery.endDate = this.getCurrentOrPreviousDay(this.estabStartDate)
      } else {
        this.disabledDate = true
        this.formQuery.startDate = dateShortcutMap[val].onClick()[0] || ''
        this.formQuery.endDate = dateShortcutMap[val].onClick()[1] || ''
      }
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
        this.formQuery.contrasCode.splice(-1)
      }
    },
    /**
     * @description 查询
     */
    handleQueryChartData() {
      // 判断条件是否有空值
      if (this.formQuery.contrasCode && this.formQuery.contrasCode.length <= 0) {
        this.$message.closeAll()
        this.$message.warning('对比指数不能为空')
        return
      }
      const params = {
        indexCode: 'b14be8e9-e93a-4f7f-849d-2816b75f26f4',
        beginDate: this.formQuery.startDate || '',
        endDate: this.formQuery.endDate || '',
        contrasCode: this.formQuery.contrasCode.join(',')
      }
      request({
        url: `/api/report/v1.0/data/sql/b14be8e9-e93a-4f7f-849d-2816b75f26f4`,
        method: 'post',
        data: params
      }).then(res => {
        if (res.data.status === 0) {
          const resultData = res.data.data || []
          this.handleChartOptions(resultData)
        }
      })
    },
    /**
     * @description 组装指标走势options
     */
    handleChartOptions(data) {
      const xData = [...new Set(data.map(item => item.D_DATE))]
      const legendData = []
      const seriesData = []
      let colors = ['#fc6769', '#d2a25a', '#789d51', '#6c50f3', '#396f92']
      let minArrIndex0 = []
      let minArrIndex1 = []
      let maxArrIndex0 = []
      let maxArrIndex1 = []

      let mergeData = merger(data, 'VC_NAME')
      mergeData.forEach((item, index) => {
        let i = 0
        legendData.push(item.VC_NAME)
        const _name = item.VC_NAME
        const tempOrigin = []
        for (let i = 0; i < xData.length; i++) {
          const temp = xData[i]
          const objExample = Object.assign({}, item.origin[0])
          objExample.D_DATE = temp
          objExample.F_PRICE = ''
          const obj = item.origin.find(sitem => sitem.D_DATE == temp) || objExample
          tempOrigin.push(obj)
        }
        item.origin = tempOrigin
        let _yData = []
        _yData = item.origin.map(ele => {
          return ele.F_PRICE ? Number(ele.F_PRICE).toFixed(4) : ''
        })
        if (_name == '投资者情绪指数') {
          i = 1
          minArrIndex1.push(..._yData)
          maxArrIndex1.push(..._yData)
        } else {
          i = 0
          minArrIndex0.push(..._yData)
          maxArrIndex0.push(..._yData)
        }
        const seriesObj = {
          name: _name,
          type: 'line',
          yAxisIndex: i,
          symbol: 'none',
          lineStyle: {
            normal: {
              width: 0.5
            }
          },
          data: []
        }
        seriesObj.data = _yData
        seriesData.push(seriesObj)
      })
      minArrIndex0 = Math.min(...minArrIndex0) || 0
      minArrIndex1 = Math.min(...minArrIndex1) || 0
      maxArrIndex0 = Math.max(...maxArrIndex0) || 0
      maxArrIndex1 = Math.max(...maxArrIndex1) || 0
      this.targetTrendOptions = {
        legend: {
          top: '3%',
          data: legendData,
          itemWidth: 18,
          itemHeight: 12,
          textStyle: { color: '#000', fontSize: 12 }
        },
        color: colors,
        grid: {
          left: '2%',
          right: '3%',
          bottom: '10%',
          top: '12%',
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          formatter: params => {
            let tip = params[0].name + '<br>'
            for (let i = 0; i < params.length; i++) {
              let value = ''
              if (params[i].value === '') {
                value = '-'
              } else {
                value = Number(params[i].value).toFixed(4)
              }
              tip += params[i].marker + params[i].seriesName + ': ' + value + '<br>'
            }
            return tip
          }
        },
        xAxis: [
          {
            type: 'category',
            axisLine: {
              show: false
            },
            axisTick: {
              show: false
            },
            splitArea: {
              show: true,
              areaStyle: {
                color: ['rgba(250,250,250,0.3)', 'rgba(255,255,255,0.3)']
              }
            },
            splitLine: {
              show: true,
              lineStyle: {
                color: '#e5e5e5',
                type: 'dashed'
              }
            },
            data: xData
          }
        ],
        yAxis: [
          {
            min: value => {
              return value.min
            },
            max: value => {
              return value.max
            },
            axisLine: {
              show: false
            },
            axisLabel: {
              formatter: function(params) {
                return params.toFixed(2)
              }
            },
            axisTick: {
              show: false
            },
            splitArea: {
              show: false
            },
            splitLine: {
              show: true,
              lineStyle: {
                color: '#e5e5e5',
                type: 'dashed'
              }
            }
          },
          {
            min: value => {
              return value.min
            },
            max: value => {
              return value.max
            },
            axisLine: {
              show: false
            },
            axisLabel: {
              formatter: function(params) {
                return params.toFixed(2)
              }
            },
            axisTick: {
              show: false
            },
            splitArea: {
              show: false
            },
            splitLine: {
              show: true,
              lineStyle: {
                color: '#e5e5e5',
                type: 'dashed'
              }
            }
          }
        ],
        dataZoom: {
          show: true,
          textStyle: {
            fontSize: 12,
            color: 'transparent'
          }
          // start: 0,
          // end: 20,
          // maxSpan: 80
        },
        series: seriesData
      }
    },
    reset() {
      this.formQuery.statistPeriod = '4'
      this.formQuery.startDate = ''
      this.formQuery.endDate = ''
      this.formQuery.contrasCode = []
    }
  }
}
</script>

<style lang="scss" scoped>
.emotional-index {
  padding-left: 16px;
  padding-right: 20px;
  .funds-filter {
    width: 100%;
    border-bottom: 1px solid #e1e0e0;

    .dbjz {
      ::v-deep .el-select .el-input--small {
        width: 260px !important;
      }

      ::v-deep .el-select .el-select__tags {
        max-width: 234px !important;
      }
    }
  }

  .chart-main {
    margin-top: 3px;
    width: 100%;

    .chart-title {
      padding: 10px 0;
      margin-bottom: 12px;
      border-bottom: 1px solid #0F65DD;

      .title-icon {
        vertical-align: middle;
        display: inline-block;

        .color-box {
          display: inline-block;
          height: 30px;
          width: 2px;
          background-color: #0F65DD;
        }
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
    }

    .chart-content {
      height: 450px;
      margin-top: 5px;

      .echarts_box {
        height: 100%;
        width: 100%;
      }
    }
  }
}
</style>

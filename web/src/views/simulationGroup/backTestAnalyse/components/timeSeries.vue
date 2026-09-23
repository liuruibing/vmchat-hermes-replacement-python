<template>
  <div class="time-series">
    <div class="chart-content" v-loading="loading">
      <el-empty description="暂无数据" v-if="isEmpty"></el-empty>
      <myChart v-else id="backTestTimeSeries" ref="backTestTimeSeries" :options="timeSeriesChartOptions" resize-dom="cmbfof" class="echart-box" />
    </div>
    <div class="table-content" v-loading="loading" id="standard-table">
      <vxe-table ref="refsTable" :cell-style="{ height: '50px' }" :data="tableData" auto-resize stripe="" show-overflow="tooltip" style="width: 100%" sync-resize>
        <vxe-table-column
          v-for="(col, i) in timeSeriesTableColumns"
          :key="i"
          :label="col.label"
          :field="col.prop"
          :align="col.align"
          :header-align="col.headerAlign"
          show-overflow-tooltip
        >
          <template slot-scope="scope">
            <span v-if="['costRate', 'periodVariation'].includes(col.prop)">
              <span>{{ scope.row[col.prop] | numberToFixedStr(2, 100, '%') }}</span>
            </span>
            <span v-else>{{ scope.row[col.prop] | noDataFilter }}</span>
          </template>
        </vxe-table-column>
      </vxe-table>
    </div>
  </div>
</template>
<script>
import myChart from '@/components/Echarts'
import { TIME_SERIES_CHART_OPTIONS, TIME_SERIES_TABLE_COLUMNS } from '../scripts/timeSeries'
import { merger } from '@/utils'
export default {
  name: 'TimeSeriesComp',
  components: {
    myChart
  },
  props: {
    timeSeriesChartData: {
      type: Array,
      default: () => []
    },
    timeSeriesTableData: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  watch: {
    timeSeriesTableData: {
      handler(newVal) {
        if (newVal && newVal.length) {
          this.tableData = newVal.map((item) => {
            return {
              ...item,
              price: Number(item.price).toFixed(2)
            }
          })
        } else {
          this.tableData = []
        }
      },
      deep: true,
      immediate: true
    },
    timeSeriesChartData: {
      handler(newVal) {
        if (newVal && newVal.length) {
          this.isEmpty = false
          this.setChartOptions(JSON.parse(JSON.stringify(newVal)))
        } else {
          this.isEmpty = true
        }
      },
      deep: true,
      immediate: true
    }
  },
  data() {
    return {
      timeSeriesChartOptions: TIME_SERIES_CHART_OPTIONS,
      timeSeriesTableColumns: TIME_SERIES_TABLE_COLUMNS,
      tableData: [],
      isEmpty: false
    }
  },
  methods: {
    setChartOptions(data) {
      data.forEach((item) => {
        if (item.costRate) {
          item.costRate = item.costRate * 100
        }
      })
      const xData = [...new Set(data.map((item) => item.ddate))]
      const legend = []
      const seriesData = []
      const mergeData = merger(data, 'subFundCode')
      mergeData.forEach((item) => {
        legend.push({ name: item.subFundCode, icon: 'roundRect' })
        const tempOrigin = []
        const seriesObj = {
          name: item.subFundCode,
          type: 'bar',
          stack: '总量',
          barWidth: '45%',
          label: {
            show: false,
            position: 'insideRight'
          },
          data: []
        }
        for (let i = 0; i < xData.length; i++) {
          const temp = xData[i]
          const objExample = Object.assign({}, item.origin[0])
          objExample.ddate = temp
          objExample.costRate = ''
          const obj = item.origin.find((sitem) => sitem.ddate == temp) || objExample
          tempOrigin.push(obj)
        }
        item.origin = tempOrigin
        // seriesObj.data = item.origin.map(item => Number(item.costRate).toFixed(2))
        let tempArray = []
        item.origin.forEach((item) => {
          if (item.costRate == '' || item.costRate == undefined || item.costRate == null || item.costRate == '-') {
            tempArray.push('-')
          } else {
            tempArray.push(Number(item.costRate).toFixed(2))
          }
        })
        seriesObj.data = tempArray
        seriesData.push(seriesObj)
      })
      this.timeSeriesChartOptions.legend.data = legend
      this.timeSeriesChartOptions.xAxis.data = xData
      this.timeSeriesChartOptions.series = seriesData
    }
  }
}
</script>
<style lang="scss" scoped>
.time-series {
  min-height: 670px;
  .title-style {
    color: #0F65DD;
    vertical-align: middle;
    height: 35px;
    line-height: 35px;
    font-size: 16px;
    margin-left: 5px;
  }
  .color-box {
    display: inline-block;
    height: 30px;
    width: 2px;
    background-color: #0F65DD;
  }
  .echart-box {
    height: 400px;
  }
  .table-content {
    margin: 10px 0px;
  }
  ::v-deep .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
}
</style>

<template>
  <div class="net-value-trend">
    <div class="chart-content" v-loading="loading">
      <el-empty description="暂无数据" v-if="isEmpty"></el-empty>
      <myChart v-else id="backTestNetVal" ref="backTestNetVal" :options="netValueChartOptions" resize-dom="cmbfof" class="echart-box" />
    </div>
    <div class="table-content" v-loading="loading" id="standard-table">
      <vxe-table ref="refsTable" :cell-style="{ height: '50px' }" :data="tableData" auto-resize stripe="" show-overflow="tooltip" style="width: 100%" sync-resize>
        <vxe-table-column
          v-for="(col, i) in netValueTableColumns"
          :key="i"
          :label="col.label"
          :field="col.prop"
          :align="col.align"
          :header-align="col.headerAlign"
          show-overflow-tooltip
        >
          <template slot-scope="scope">


              <div v-if ="col.prop !== 'typeName'">
                 <div v-if ="scope.row['typeName']!== '夏普比率(年化)'">
                 <span>{{ scope.row[col.prop] | numberToFixedStr(2, 100, '%') }}</span>
                 </div>
                <div v-else>
                  <span>{{ scope.row[col.prop] | numberToFixedStr(2, 1, '') }}</span>
                </div>
              </div>
              <div v-else>
                <span>{{ scope.row[col.prop] | noDataFilter }}</span>
              </div>


          </template>
        </vxe-table-column>
      </vxe-table>
    </div>
  </div>
</template>
<script>
import myChart from '@/components/Echarts'
import { NET_VALUE_CHART_OPTIONS, NET_VALUE_TABLE_COLUMNS } from '../scripts/netValConstants'
export default {
  name: 'NetValueTrendComp',
  components: {
    myChart
  },
  props: {
    netValueTableData: {
      type: Array,
      default: () => []
    },
    netValueChartData: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  watch: {
    netValueTableData: {
      handler(newVal) {
        if (newVal && newVal.length) {
          this.tableData = newVal
        } else {
          this.tableData = []
        }
      },
      deep: true,
      immediate: true
    },
    netValueChartData: {
      handler(newVal) {
        if (newVal && newVal.length) {
          this.isEmpty = false
          this.setChartOptions(newVal)
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
      netValueChartOptions: NET_VALUE_CHART_OPTIONS,
      netValueTableColumns: NET_VALUE_TABLE_COLUMNS,
      tableData: [],
      isEmpty: false
    }
  },
  methods: {
    setChartOptions(data) {
      // map组装数据
      const xData = data.map((item) => item.ddate || '')
      const convertUnitData = data.map((item) => item.virtualPrice || '')
      const unitPriceData = data.map((item) => item.unitPrice || '')
      const priceData = data.map((item) => (item.price ? Number(item.price).toFixed(2) : ''))
      const amountData = data.map((item) => (item.amount ? Number(item.amount / 10000).toFixed(2) : ''))
      // 取该y轴最大最小值为刻度
      const y0Max = Math.max(...[...unitPriceData, ...convertUnitData])
      const y0Min = Math.min(...[...unitPriceData, ...convertUnitData])
      const y1Max = Math.max(...[...priceData, ...amountData])
      const y1Min = Math.min(...[...priceData, ...amountData])
      // options赋值
      this.netValueChartOptions.yAxis[0].max = y0Max
      this.netValueChartOptions.yAxis[0].min = y0Min
      this.netValueChartOptions.yAxis[1].max = y1Max
      this.netValueChartOptions.yAxis[1].min = y1Min
      this.netValueChartOptions.xAxis.data = xData
      this.netValueChartOptions.series[0].data = convertUnitData
      this.netValueChartOptions.series[1].data = unitPriceData
      this.netValueChartOptions.series[2].data = priceData
      this.netValueChartOptions.series[3].data = amountData
    }
  }
}
</script>
<style lang="scss" scoped>
.net-value-trend {
  min-height: 670px;
  .echart-box {
    height: 400px;
  }
  .table-content {
    margin: 30px 0px;
  }
  ::v-deep .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
}
</style>

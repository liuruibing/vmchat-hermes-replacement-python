<template>
  <div class="dynamic">
    <div class="chart-content" v-loading="loading">
      <el-empty description="暂无数据" v-if="isEmpty"></el-empty>
      <myChart v-else id="backTestDynamic" ref="backTestDynamic" :options="dynamicChartOptions" resize-dom="cmbfof" class="echart-box" />
      <div v-if="!isEmpty" style="color: #80828a; margin-left: 2%">
        注：T日回撤=（T日累计单位净值-回撤区间最大累计单位净值）/回撤区间最大累计单位净值（回撤区间为查询开始日至T日）
      </div>
    </div>

    <div class="table-content" id="standard-table" v-loading="loading">
      <vxe-table ref="refsTable" :cell-style="{ height: '50px' }" :data="tableData" auto-resize stripe="" show-overflow="tooltip" style="width: 100%" sync-resize>
        <vxe-table-column
          v-for="(col, i) in dynamicTableColumns"
          :key="i"
          :label="col.label"
          :field="col.prop"
          :align="col.align"
          :header-align="col.headerAlign"
          show-overflow-tooltip
        >
          <template slot-scope="scope">
            <span>{{ scope.row[col.prop] | noDataFilter }}</span>
          </template>
        </vxe-table-column>
      </vxe-table>
    </div>
  </div>
</template>
<script>
import myChart from '@/components/Echarts'
import { DYNAMIC_CHART_OPTIONS, DYNAMIC_TABLE_COLUMNS } from '../scripts/dynamicConstants'
export default {
  name: 'DynamicComp',
  components: {
    myChart
  },
  props: {
    dynamicTableData: {
      type: Array,
      default: () => []
    },
    dynamicChartData: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    },
    combineName: {
      type: String,
      default: ''
    },
    beCodeName: {
      type: String,
      default: ''
    }
  },
  watch: {
    dynamicTableData: {
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
    dynamicChartData: {
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
      dynamicChartOptions: DYNAMIC_CHART_OPTIONS,
      dynamicTableColumns: DYNAMIC_TABLE_COLUMNS,
      tableData: [],
      isEmpty: false
    }
  },
  methods: {
    setChartOptions(data) {
      // map组装数据
      const xData = data.map((item) => item.ddate || '')
      const drawdownData = data.map((item) => (item.drawdown ? Number(item.drawdown * 100).toFixed(2) : ''))
      const drawdownjzData = data.map((item) => (item.drawdownjz ? Number(item.drawdownjz * 100).toFixed(2) : ''))
      // options赋值
      this.dynamicChartOptions.xAxis.data = xData
      this.dynamicChartOptions.legend.data[0] = this.combineName
      this.dynamicChartOptions.legend.data[1] = this.beCodeName
      this.dynamicChartOptions.series[0].name = this.combineName
      this.dynamicChartOptions.series[1].name = this.beCodeName
      this.dynamicChartOptions.series[0].data = drawdownData
      this.dynamicChartOptions.series[1].data = drawdownjzData
    }
  }
}
</script>
<style lang="scss" scoped>
.dynamic {
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

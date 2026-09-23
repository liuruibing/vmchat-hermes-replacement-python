<template>
  <div class="volatility">
    <div class="chart-content" v-loading="loading">
      <el-empty description="暂无数据" v-if="isEmpty"></el-empty>
      <myChart
        v-else
        id="backTestVolatility"
        ref="backTestVolatility"
        :options="volatilityChartOptions"
        resize-dom="cmbfof"
        class="echart-box"
      />
    </div>
  </div>
</template>
<script>
import myChart from '@/components/Echarts'
import { VOLATILITY_CHART_OPTIONS } from '../scripts/volatilityConstants'
export default {
  name: 'VolatilityComp',
  components: {
    myChart
  },
  props: {
    volatilityChartData: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  watch: {
    volatilityChartData: {
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
      volatilityChartOptions: VOLATILITY_CHART_OPTIONS,
      isEmpty: false
    }
  },
  methods: {
    setChartOptions(data) {
      const xData = data.map(item => item.ddate || '')
      const volatilityData = data.map(item =>
        item.volatility ? Number(item.volatility * 100).toFixed(2) : ''
      )
      const volatilityJzData = data.map(item =>
        item.volatilityjz ? Number(item.volatilityjz * 100).toFixed(2) : ''
      )
      this.volatilityChartOptions.xAxis.data = xData
      this.volatilityChartOptions.series[0].data = volatilityData
      this.volatilityChartOptions.series[1].data = volatilityJzData
    }
  }
}
</script>
<style lang="scss" scoped>
.volatility {
  min-height: 670px;
  .echart-box {
    height: 400px;
  }
}
</style>

<template>
  <div v-if="visible" class="trade-cycle-charts">
    <h3 class="section-title">{{ title }}</h3>
    <div class="half-charts">
      <myChart v-if="leftOption" :id="leftId" :options="leftOption" class="echarts_box half-chart" resize-dom="cmbfof" />
      <myChart v-if="rightOption" :id="rightId" :options="rightOption" class="echarts_box half-chart" resize-dom="cmbfof" />
    </div>
  </div>
</template>

<script>
import myChart from '@/components/Echarts'

export default {
  name: 'TradeCycleCharts',
  components: { myChart },
  props: {
    visible: { type: Boolean, default: false },
    title: { type: String, default: '交易周期分析' },
    leftId: { type: String, required: true },
    rightId: { type: String, required: true },
    leftOption: { type: Object, default: null },
    rightOption: { type: Object, default: null }
  }
}
</script>

<style lang="scss" scoped>
.trade-cycle-charts {
  margin-top: 16px;
  .section-title {
    text-align: center;
    font-size: 16px;
    margin: 8px 0 12px;
  }
  .half-charts {
    display: flex;
    gap: 8px;
    .half-chart {
      flex: 1;
      min-height: 350px;
    }
  }
}
</style>

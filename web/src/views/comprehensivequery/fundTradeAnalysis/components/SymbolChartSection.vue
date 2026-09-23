<template>
  <div v-if="visible" class="symbol-chart-section">
    <myChart v-if="priceOption" id="symbolChartPrice" :options="priceOption" class="echarts_box chart-block" resize-dom="cmbfof" />
    <myChart v-if="yieldOption" id="symbolChartYield" :options="yieldOption" class="echarts_box chart-block" resize-dom="cmbfof" />
    <myChart v-if="incomeOption" id="symbolChartIncome" :options="incomeOption" class="echarts_box chart-block" resize-dom="cmbfof" />
    <div v-if="showTradeMoneyTime" class="trade-money-time">
      <h3 class="section-title">交易周期分析</h3>
      <div class="half-charts">
        <myChart v-if="tradeLeftOption" id="symbolChartTradeLeft" :options="tradeLeftOption" class="echarts_box half-chart" resize-dom="cmbfof" />
        <myChart v-if="tradeRightOption" id="symbolChartTradeRight" :options="tradeRightOption" class="echarts_box half-chart" resize-dom="cmbfof" />
      </div>
    </div>
  </div>
</template>

<script>
import myChart from '@/components/Echarts'

export default {
  name: 'SymbolChartSection',
  components: { myChart },
  props: {
    visible: { type: Boolean, default: false },
    priceOption: { type: Object, default: null },
    yieldOption: { type: Object, default: null },
    incomeOption: { type: Object, default: null },
    tradeLeftOption: { type: Object, default: null },
    tradeRightOption: { type: Object, default: null },
    showTradeMoneyTime: { type: Boolean, default: false }
  }
}
</script>

<style lang="scss" scoped>
.symbol-chart-section {
  margin-top: 16px;
  .chart-block {
    min-height: 350px;
    margin-bottom: 16px;
  }
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

<template>
  <div class="summary-tables">
    <!-- 期货品种汇总 -->
    <div v-if="showQhCategory" class="summary-block">
      <el-row>
        <el-col :span="16">
          <div class="page-model-title">
            <div class="title-icon"><div class="color-box"></div></div>
            <span class="title-txt">期货品种汇总</span>
          </div>
        </el-col>
        <el-col :span="8">
          <div style="float: right">
            <el-button type="info" size="small" plain icon="el-icon-download" @click="$emit('export-qh-category')">导出</el-button>
          </div>
        </el-col>
      </el-row>
      <table ref="qhCategoryTable" class="summary-table native-table">
        <thead>
          <tr>
            <th>行业分类</th><th>品种名称</th>
            <th>期末标的<br>数量(多头)</th><th>期末市值<br>(多头)(元)</th>
            <th>期末标的<br>数量(空头)</th><th>期末市值<br>(空头)(元)</th>
            <th>买入标的<br>数量(多头)</th><th>买入金额<br>(多头)(元)</th>
            <th>卖出标的<br>数量(多头)</th><th>卖出金额<br>(多头)(元)</th>
            <th>买入标的<br>数量(空头)</th><th>买入金额<br>(空头)(元)</th>
            <th>卖出标的<br>数量(空头)</th><th>卖出金额<br>(空头)(元)</th>
            <th>持仓周期</th><th>交易性收益<br>(元)</th><th>持有性收益<br>(元)</th>
            <th>总收益<br>(未扣费)<br>(元)</th><th>交易费用<br>(元)</th><th>总收益<br>(费后)<br>(元)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!qhCategoryRows.length"><td colspan="20" class="center">暂无数据</td></tr>
          <template v-for="(group, gi) in qhCategoryGroups">
            <tr v-for="(row, ri) in group.rows" :key="'qh-' + gi + '-' + ri">
              <td v-if="ri === 0" :rowspan="group.rows.length" class="center group-cell">{{ group.label }}</td>
              <td class="left">
                <a href="javascript:;" class="link-cell" @click="$emit('qh-category-click', row)">{{ fmt(row.futDetailName) }}</a>
              </td>
              <td v-for="field in qhDataFields" :key="field" class="center">{{ fmt(row[field]) }}</td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>

    <!-- 分类汇总 -->
    <div class="summary-block">
      <el-row>
        <el-col :span="16">
          <div class="page-model-title">
            <div class="title-icon"><div class="color-box"></div></div>
            <span class="title-txt">分类汇总</span>
          </div>
        </el-col>
        <el-col :span="8">
          <div style="float: right">
            <el-button type="info" size="small" plain icon="el-icon-download" @click="$emit('export-detail')">导出</el-button>
          </div>
        </el-col>
      </el-row>
      <table ref="detailTable" class="summary-table native-table">
        <thead>
          <tr>
            <th>资产类别</th><th>行业分类</th>
            <th>产品<br>收益率(%)</th><th>基准<br>收益率(%)</th>
            <th>期末标的<br>数量(多头)</th><th>期末市值<br>(多头)(元)</th>
            <th>期末标的<br>数量(空头)</th><th>期末市值<br>(空头)(元)</th>
            <th>买入标的<br>数量(多头)</th><th>买入金额<br>(多头)(元)</th>
            <th>卖出标的<br>数量(多头)</th><th>卖出金额<br>(多头)(元)</th>
            <th>买入标的<br>数量(空头)</th><th>买入金额<br>(空头)(元)</th>
            <th>卖出标的<br>数量(空头)</th><th>卖出金额<br>(空头)(元)</th>
            <th>持仓周期</th><th>交易性收益<br>(元)</th><th>持有性收益<br>(元)</th>
            <th>总收益<br>(未扣费)<br>(元)</th><th>交易费用<br>(元)</th><th>总收益<br>(费后)<br>(元)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!detailGroups.length"><td colspan="22" class="center">暂无数据</td></tr>
          <template v-for="(group, gi) in detailGroups">
            <tr v-for="(row, ri) in group.rows" :key="'detail-' + gi + '-' + ri">
              <td v-if="ri === 0" :rowspan="group.rows.length" class="center group-cell">{{ group.label }}</td>
              <td class="left">
                <a href="javascript:;" class="link-cell" @click="$emit('industry-click', row)">{{ fmt(row.assetTypeDetailName) }}</a>
              </td>
              <td v-for="field in detailDataFields" :key="field" class="center">{{ fmt(row[field]) }}</td>
            </tr>
          </template>
        </tbody>
      </table>
      <p v-if="industryDescription" class="description">{{ industryDescription }}</p>
    </div>

    <!-- 资产汇总 -->
    <div class="summary-block">
      <el-row>
        <el-col :span="16">
          <div class="page-model-title">
            <div class="title-icon"><div class="color-box"></div></div>
            <span class="title-txt">资产汇总</span>
          </div>
        </el-col>
        <el-col :span="8">
          <div style="float: right">
            <el-button type="info" size="small" plain icon="el-icon-download" @click="$emit('export-asset')">导出</el-button>
          </div>
        </el-col>
      </el-row>
      <table ref="assetTable" class="summary-table native-table">
        <thead>
          <tr>
            <th>资产类别</th>
            <th>产品<br>收益率(%)</th><th>基准<br>收益率(%)</th>
            <th>期末标的<br>数量(多头)</th><th>期末市值<br>(多头)(元)</th>
            <th>期末标的<br>数量(空头)</th><th>期末市值<br>(空头)(元)</th>
            <th>买入标的<br>数量(多头)</th><th>买入金额<br>(多头)(元)</th>
            <th>卖出标的<br>数量(多头)</th><th>卖出金额<br>(多头)(元)</th>
            <th>买入标的<br>数量(空头)</th><th>买入金额<br>(空头)(元)</th>
            <th>卖出标的<br>数量(空头)</th><th>卖出金额<br>(空头)(元)</th>
            <th>持仓周期</th><th>交易性收益<br>(元)</th><th>持有性收益<br>(元)</th>
            <th>总收益<br>(未扣费)<br>(元)</th><th>交易费用<br>(元)</th><th>总收益<br>(费后)<br>(元)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="!assetGroups.length"><td colspan="21" class="center">暂无数据</td></tr>
          <template v-for="(group, gi) in assetGroups">
            <tr v-for="(row, ri) in group.rows" :key="'asset-' + gi + '-' + ri">
              <td v-if="ri === 0" :rowspan="group.rows.length" class="center group-cell">
                <a href="javascript:;" class="link-cell" @click="$emit('asset-click', group)">{{ group.label }}</a>
              </td>
              <td v-for="field in assetDataFields" :key="field" class="center">{{ fmt(row[field]) }}</td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { dataHandle } from '../scripts/dataHandle'

export default {
  name: 'SummaryTables',
  props: {
    showQhCategory: { type: Boolean, default: false },
    qhCategoryData: { type: Object, default: () => ({}) },
    detailData: { type: Object, default: () => ({}) },
    assetData: { type: Object, default: () => ({}) },
    industryDescription: { type: String, default: '' }
  },
  data() {
    return {
      qhDataFields: ['dtEndHldAmount', 'dtEndHldPrice', 'ktEndHldAmount', 'ktEndHldPrice', 'dtBuyAmount', 'dtBuyMoney', 'dtSellAmount', 'dtSellMoney', 'ktBuyAmount', 'ktBuyMoney', 'ktSellAmount', 'ktSellMoney', 'hldTime', 'tradeIncome', 'hldIncome', 'totalMoney', 'fee', 'totalMoneyAfterFee'],
      detailDataFields: ['fundYield', 'benchYield', 'dtEndHldAmount', 'dtEndHldPrice', 'ktEndHldAmount', 'ktEndHldPrice', 'dtBuyAmount', 'dtBuyMoney', 'dtSellAmount', 'dtSellMoney', 'ktBuyAmount', 'ktBuyMoney', 'ktSellAmount', 'ktSellMoney', 'hldTime', 'tradeIncome', 'hldIncome', 'totalMoney', 'fee', 'totalMoneyAfterFee'],
      assetDataFields: ['fundYield', 'benchYield', 'dtEndHldAmount', 'dtEndHldPrice', 'ktEndHldAmount', 'ktEndHldPrice', 'dtBuyAmount', 'dtBuyMoney', 'dtSellAmount', 'dtSellMoney', 'ktBuyAmount', 'ktBuyMoney', 'ktSellAmount', 'ktSellMoney', 'hldTime', 'tradeIncome', 'hldIncome', 'totalMoney', 'fee', 'totalMoneyAfterFee']
    }
  },
  computed: {
    qhCategoryGroups() {
      const d = this.qhCategoryData || {}
      return [
        { label: '股指期货', rows: d.gzQHList || [] },
        { label: '国债期货', rows: d.btQHList || [] },
        { label: '商品期货', rows: d.spQHList || [] },
        { label: '指数期货', rows: d.zsQHList || [] }
      ].filter(g => g.rows && g.rows.length)
    },
    qhCategoryRows() {
      return this.qhCategoryGroups.flatMap(g => g.rows)
    },
    detailGroups() {
      const d = this.detailData || {}
      return [
        { label: '股票-A股', rows: d.stockAList || [] },
        { label: '股票-港股', rows: d.stockHKList || [] },
        { label: '可转债', rows: d.bondKzzList || [] },
        { label: '期货', rows: d.qhList || [] }
      ].filter(g => g.rows && g.rows.length)
    },
    assetGroups() {
      const d = this.assetData || {}
      return [
        { label: '股票-A股', assetType: 'GP_A', assetTypeName: '股票-A股', rows: d.stockAList || [] },
        { label: '股票-港股', assetType: 'GP_H', assetTypeName: '股票-港股', rows: d.stockHKList || [] },
        { label: '可转债', assetType: 'ZQ_KZZ', assetTypeName: '可转债', rows: d.bondKzzList || [] },
        { label: 'ETF基金', assetType: 'JJ_ETF', assetTypeName: 'ETF基金', rows: d.fundETFList || [] },
        { label: '期货', assetType: 'QH', assetTypeName: '期货', rows: d.qhList || [] }
      ].filter(g => g.rows && g.rows.length)
    }
  },
  methods: {
    fmt(val) {
      return dataHandle(val)
    },
    getTableRef(name) {
      return this.$refs[name]
    }
  }
}
</script>

<style lang="scss" scoped>
.summary-tables {
  margin-top: 16px;
  .summary-block {
    margin-bottom: 24px;
  }
  .native-table {
    width: 100%;
    border-collapse: collapse;
    table-layout: fixed;
    th, td {
      border: 1px solid #ebeef5;
      padding: 6px 4px;
      font-size: 12px;
      word-break: break-all;
    }
    th {
      text-align: center;
      vertical-align: middle;
      background: #f5f7fa;
    }
    .center { text-align: center; vertical-align: middle; }
    .left { text-align: left; vertical-align: middle; }
    .group-cell { border-right: 1px solid #ddd; }
    .link-cell { color: #409eff; cursor: pointer; }
  }
  .description {
    margin-top: 8px;
    color: #666;
    font-size: 12px;
    line-height: 1.6;
  }
  .color-box {
    display: inline-block;
    height: 30px;
    width: 2px;
    background-color: #e03d3e;
  }
}
</style>

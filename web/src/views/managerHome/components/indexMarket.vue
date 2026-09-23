<template>
  <el-card shadow="never" class="mt20">
    <template #header>
      <div style="display: flex; justify-content: space-between;">
        <div style="display: flex;align-items: center;gap: 10px;">
          <div style="display: flex;align-items: center;">
            <img src="../img/index.svg" alt="" style="width: 40px; height: 40px">
            <span style="font-weight: bold;">指数行情总览</span>
          </div>
          <span>日期：</span>
          <el-date-picker v-model="ddate_" type="daterange" :clearable="false" value-format="yyyy-MM-dd" align="left"
            size="small" unlink-panels range-separator="至" start-placeholder="请选择开始日期" end-placeholder="请选择结束日期"
            popper-class="popperDateShortTP" :picker-options="queryParams.datePickerOptions"></el-date-picker>
          <span>产品：</span>
          <el-select v-model="fundCodeArray" filterable multiple collapse-tags>
            <el-option v-for="item in queryParams.fundList" :key="item.fundCode" :label="item.fundName" :value="item.fundCode"></el-option>
          </el-select>
          <span>私募指数：</span>
          <el-select v-model="privateIndexCodeArray" filterable multiple collapse-tags>
            <el-option v-for="item in privateIndexOptions" :key="item.indexCode" :label="item.indexName" :value="item.indexCode"></el-option>
          </el-select>
          <span>市场指数：</span>
          <el-select v-model="compareIndexCodeArray" filterable multiple collapse-tags>
            <el-option v-for="item in compareIndexOptions" :key="item.dimCde" :label="item.dimNme"
              :value="item.dimCde"></el-option>
          </el-select>
          <span style="color:red">注：数据更新到T-3日</span>
        </div>
        <img src="../img/search.svg" @click="loadData" style="width: 40px; height: 40px;">
      </div>
    </template>
    <el-row>
      <el-col :span="24" v-loading="loading">
        <myChart id="zshqzl" ref="zshqzl" :options="chartOptions" class="echarts_box" style="height: 350px;" resize-dom="cmbfof" />
      </el-col>
    </el-row>
  </el-card>
</template>

<script>
import myChart from '@/components/Echarts'
import api from '../api/indexMarket'
export default {
  name: 'indexMarket',
  components: { myChart },
  props: {
    queryParams: {
      type: Object,
      required: true
    },
    updateFlag: {
      type: Number,
      required: true
    }
  },
  watch: {
    queryParams: {
      immediate: false,
      handler(newVal) {
        this.fundCodeArray = [this.queryParams.fundList[0].fundCode]
        this.ddate_ = [this.queryParams.initBeginDate, this.queryParams.initEndDate];
      }
    },
    updateFlag: {
      immediate: false,
      async handler(newVal) {
        if (!this.isReady) {
          const { data } = await api.selectIndexList();
          this.privateIndexOptions = data.data.privateIndexList
          this.compareIndexOptions = data.data.compareIndexList
          if(!data.data.privateIndexList && data.data.privateIndexList.length >=1){
            this.privateIndexCodeArray = data.data.initCheckedPrivateIndexCodes.split(',')
          }

          this.compareIndexCodeArray = data.data.initCheckedCompareIndexCodes.split(',')
          this.isReady = true;
        }
        await this.loadData()
      }
    },
  },
  data() {
    return {
      ddate_: [],
      chartOptions: {},
      loading: false,
      fundCodeArray: [],
      privateIndexCodeArray: [],
      compareIndexCodeArray: [],
      privateIndexOptions: [],
      compareIndexOptions: [],
      isReady: false,
      completedCount: 0,
      companyFundIndexChartData:[],

      colors: ['#0083C9', '#FF0033', '#FAC958', '#FB8652', '#73C0DF', '#bbbaff', '#f49494', '#e5cf0d', '#d2f5a6','#76f2f2','#c05050','#9a7fd1']

    }
  },
  mounted() {

  },
  methods: {
    initChart() {
      this.completedCount++;
      if (this.completedCount === 1) {

        let xData = [];
        let seriesMap = [];
        let seriesArray = []
        let data=this.companyFundIndexChartData
        for (let i = 0; i < data.length; i++) {

          seriesMap.push( {"name": data[i].indexName,"textStyle": {"fontSize": 14} })
          let oneSeries = []
          let oneIndexData = data[i].data
          for (let j = 0; j < oneIndexData.length; j++) {
            oneSeries.push(oneIndexData[j].F_INDEX_PRICE_GYH)
            if (i === 0) {
              xData.push(oneIndexData[j].TDATE)
            }
          }

          let series = {
            name: data[i].indexName,
            type: 'line',
            data: oneSeries,
            smooth: true,
            symbol: 'none',
            areaStyle: { color: this.colors[i], opacity: 0.3 }
          }

          seriesArray.push(series)

        }

        let interval = 0;
        if (xData.length > 31) {
          interval = Math.floor(xData.length / 30)
        }
        this.chartOptions = {
          color: this.colors,
          "animation": false,
          "tooltip": { "trigger": "axis" },
          toolbox: {
            feature: {
              dataView: {
                optionToContent: this.$fun.optionToContent
              },
              saveAsImage: {
                name: '指数行情总览',
              }
            }
          },
          grid: { left: "80", right: "80", top: "40", bottom: "40", containLabel: true },
          "legend": {
            "borderColor": "#FFF", "top": "5px",
            "data": seriesMap, "itemWidth": 15, "textStyle": { "color": "#000", "fontSize": 14 }
          },
          "xAxis": [{
            "axisLabel": { "color": "#000", "fontSize": 14, "interval": interval, "rotate": -90 },
            "axisLine": { "lineStyle": { "color": "#8d8d8d" } },
            "axisTick": { "alignWithLabel": false, "show": false },
            "boundaryGap": false,
            "data": xData,
            "splitLine": { "lineStyle": { "type": "dotted" }, "show": true },
            "type": "category"
          }],
          "yAxis": [{
            "axisLabel": { "color": "#000", "fontSize": 14, "formatter": function (value, index) { return value.toFixed(2); } },
            "axisLine": { "lineStyle": { "color": "#8d8d8d" } },
            "axisTick": { "alignWithLabel": false, "show": false },
            "min": function (value) {
              return (value.min - 0.05).toFixed(2)
            },
            "splitLine": { "lineStyle": { "type": "dotted" }, "show": true }, "type": "value"
          }],
          "series": seriesArray
        }
        this.loading = false;
      }
    },
    async loadData() {
      this.completedCount = 0;
      this.loading = true
      await this.loadCompanyFundAndIndexChartData()

    },
    async loadCompanyFundAndIndexChartData() {
      this.companyFundIndexChartData = []
      try {
        const params = {}
        params.beginDate = this.ddate_[0];
        params.endDate = this.ddate_[1];
        params.companyId = this.queryParams.companyId;
        let fundCodeArray = this.fundCodeArray;
        let fundCodes = fundCodeArray.join(',');
        params.fundCodes = fundCodes;
        let indexCodeArray = this.privateIndexCodeArray;
        let indexCodes = indexCodeArray.join(',');
        params.indexCodes = indexCodes;

        let compareIndexCodeArray = this.compareIndexCodeArray;
        let baseCodes = compareIndexCodeArray.join(',');
        params.baseCodes = baseCodes;

        params.sqlCode = '7db73307-f551-46f7-a8d5-d9582cdff872';

        const { data } = await api.doCompanyFundAndIndexChart(params)
        if (data.data.length > 0) {
          this.companyFundIndexChartData = data.data
        }
      } catch (error) {
        console.log(error)
      } finally {
        this.initChart()
      }
    },

  }
}

</script>
<style lang="scss" scoped>
::v-deep .el-card__body {
  padding: 0;
}
::v-deep .el-select .el-select__tags > span > .el-tag:first-child {
  width: 50%;
}
</style>

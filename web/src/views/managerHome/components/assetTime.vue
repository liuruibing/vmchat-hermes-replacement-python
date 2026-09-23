<template>
  <el-card shadow="never" class="mt20">
    <template #header>
      <div style="display: flex; justify-content: space-between;">
        <div style="display: flex;align-items: center;gap: 10px;">
          <img src="../img/bar.svg" alt="" style="width: 40px; height: 40px">
          <span>日期：</span>
          <el-date-picker v-model="ddate_" type="daterange" :clearable="false" value-format="yyyy-MM-dd" align="left"
              size="small" unlink-panels range-separator="至" start-placeholder="请选择开始日期" end-placeholder="请选择结束日期"
              popper-class="popperDateShortTP" :picker-options="queryParams.datePickerOptions"></el-date-picker>
          <el-radio-group v-model="companyOrFundType" @change="radioChange">
            <el-radio label="company" size="large">全部</el-radio>
            <el-radio label="fund" size="large">单产品</el-radio>
          </el-radio-group>
          <el-select v-model="fundCode" v-if="companyOrFundType === 'fund'" filterable>
            <el-option v-for="item in queryParams.fundList" :key="item.fundCode" :label="item.fundName"
              :value="item.fundCode"></el-option>
          </el-select>
          <span style="color:red">注：数据更新到T-3日</span>
        </div>
        <img src="../img/search.svg" @click="loadData" style="width: 40px; height: 40px;">
      </div>
    </template>
    <el-row>
      <el-col :span="24" v-loading="loading1">
        <myChart id="dlzczb" ref="dlzczb" :options="chartOptions1" class="echarts_box" resize-dom="cmbfof" />
      </el-col>
      <el-col :span="24" v-loading="loading2" style="margin-top: 10px;">
        <myChart id="dlzcgm" ref="dlzcgm" :options="chartOptions2" class="echarts_box" resize-dom="cmbfof" />
      </el-col>
    </el-row>
  </el-card>
</template>

<script>
import myChart from '@/components/Echarts'
import api from '../api/assetTime'
import moment from 'moment'
export default {
  name: 'assetTime',
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
        this.ddate_ = [this.queryParams.initBeginDate,this.queryParams.initEndDate];
        const list = this.queryParams.fundList
        if (list && list.length > 0) {
          this.fundCode = list[0].fundCode
        } else {
          this.fundCode = ''
        }
      }
    },
    updateFlag: {
      immediate: false,
      handler(newVal) {
        this.loadData()
      }
    },
  },
  data() {
    return {
      ddate_: [],
      chartOptions1: {},
      chartOptions2: {},
      fundCode: '',
      title: "",
      tableData:[],
      loading1: false,
      loading2: false,
      companyOrFundType: 'company'
    }
  },
  mounted() {

  },
  methods: {

    radioChange(val) {
      if (this.fundCode === '') {
        this.fundCode = this.queryParams.fundList[0].fundCode
      }
    },
    loadData() {
      const params = {}
      params.companyId = this.queryParams.companyId;
      params.assetCompanyOrFundType = this.companyOrFundType;
      params.fundCode = this.fundCode;
      params.beginDate = this.ddate_[0];
      params.endDate = this.ddate_[1];
      this.loadChartData1(params)
      this.loadChartData2(params)
    },
    async loadChartData1(params) {
      this.loading1 = true
      try {
        const { data } = await api.assetTimeEchartRatioData(params)
        let title = this.queryParams.companyName;

        if (this.companyOrFundType !== 'company') {
          title = this.queryParams.fundList.filter((item) => item.fundCode === this.fundCode)[0].fundName
        }
        let xData = []
        let seriesMap = new Map();
        let seriesArray = []
        let interval = 0;
        let y2 = 110;
        if (data.data.length > 0) {
          data.data.forEach(item => {
            if (!xData.includes(item.xaxisData)) {
              xData.push(item.xaxisData)
            }
            if (!seriesMap.has(item.yaxisData1)) {
              seriesMap.set(item.yaxisData1, [])
            }
            seriesMap.get(item.yaxisData1).push(item.yaxisData2)
          });
          for (const [key, value] of seriesMap) {
            seriesArray.push({
              name: key,
              type: 'bar',
              barMaxWidth: 40,
              smooth: true,
              symbol: 'none',
              stack: "holdSeq",
              yAxisIndex: 0,
              data: value
            })
          }
          if (seriesArray.length > 6) {
            y2 = 140
          }
          if (xData.length > 31) {
            interval = Math.floor(xData.length / 30);
          }
          this.chartOptions1 = {
            "animation": false,
            "tooltip": { "trigger": "axis" },
            toolbox: {
              feature: {
                dataView: {
                  optionToContent: this.$fun.optionToContent
                },
                saveAsImage: {
                  name: '大类资产占比',
                }
              }
            },
            "title": { "text": title, "textStyle": { "fontSize": 14 }, "borderColor": "#FFF", "left": "center" },
            "grid": { "x": "80px", "y": "30px", "x2": "35px", "y2": y2 + "px" },
            "legend": {
              "data": [...seriesMap.keys()], "bottom": "-5px", "itemWidth": 15, "borderColor": "#FFF", textStyle: { fontSize: 14 }
            },
            "xAxis": [{
              "axisLabel": { "color": "#000", "fontSize": 14, "interval": interval, "rotate": -90 },
              "axisLine": { "lineStyle": { "color": "#8d8d8d" } },
              "axisTick": { "alignWithLabel": false, "show": false },
              "data": xData,
              "splitLine": { "lineStyle": { "type": "dotted" }, "show": true },
              "type": "category"
            }],
            "yAxis": [{
              "type": "value",
              "splitLine": { "show": true, "lineStyle": { "type": "dotted" } },
              "axisTick": { "alignWithLabel": false, "show": false },
              "axisLine": { "lineStyle": { "color": "#8d8d8d" } },
              "axisLabel": { "formatter": "{value}%", "color": "#000", "fontSize": 14 },
              "max": 100,
              "min": 0,
              "name": "占比",
              "nameTextStyle": { // 设置名称的样式
                "fontSize": 14 // 设置字体大小
              }
            }],
            "series": seriesArray
          }
        } else {
          this.chartOptions1 = {}
        }
        this.loading1 = false
      } catch (error) {
        console.log(error)
        this.loading1 = false
        this.chartOptions1 = {}
      }
    },
    async loadChartData2(params) {
      this.loading2 = true
      try {
        const { data } = await api.assetTimeEchartHldData(params)
        let title = this.queryParams.companyName;

        if (this.companyOrFundType !== 'company') {
          title = this.queryParams.fundList.filter((item) => item.fundCode === this.pieFundCode)[0].fundName
        }
        let xData = []
        let seriesMap = new Map();
        let seriesArray = []
        let interval = 0;
        let y2 = 110;
        if (data.data.length > 0) {
          data.data.forEach(item => {
            if (!xData.includes(item.xaxisData)) {
              xData.push(item.xaxisData)
            }
            if (!seriesMap.has(item.yaxisData1)) {
              seriesMap.set(item.yaxisData1, [])
            }
            seriesMap.get(item.yaxisData1).push(item.yaxisData2)
          });
          for (const [key, value] of seriesMap) {
            seriesArray.push({
              name: key,
              type: 'bar',
              barMaxWidth: 40,
              smooth: true,
              symbol: 'none',
              stack: "holdSeq",
              yAxisIndex: 0,
              data: value
            })
          }
          if (seriesArray.length > 6) {
            y2 = 140
          }
          if (xData.length > 31) {
            interval = Math.floor(xData.length / 30);
          }
          this.chartOptions2 = {
            "animation": false,
            "tooltip": { "trigger": "axis" },
            toolbox: {
              feature: {
                dataView: {
                  optionToContent: this.$fun.optionToContent
                },
                saveAsImage: {
                  name: '大类资产规模',
                }
              }
            },
            "title": { "text": title, "textStyle": { "fontSize": 14 }, "borderColor": "#FFF", "left": "center" },
            "grid": { "x": "80px", "y": "30px", "x2": "35px", "y2": y2 + "px" },
            "legend": {
              "data": [...seriesMap.keys()], "bottom": "-5px", "itemWidth": 15, "borderColor": "#FFF",textStyle: { fontSize: 14 }
            },
            "xAxis": [{
              "axisLabel": { "color": "#000", "fontSize": 14, "interval": interval, "rotate": -90 },
              "axisLine": { "lineStyle": { "color": "#8d8d8d" } },
              "axisTick": { "alignWithLabel": false, "show": false },
              "data": xData,
              "splitLine": { "lineStyle": { "type": "dotted" }, "show": true },
              "type": "category"
            }],
            "yAxis": [{
                "type": "value",
                "splitLine": {"show": true, "lineStyle": {"type": "dotted"}},
                "axisTick": {"alignWithLabel": false, "show": false},
                "axisLine": {"lineStyle": {"color": "#8d8d8d"}},
                "axisLabel": {"formatter": "{value}", "color": "#000","fontSize": 14},
                "name": "亿元",
                "nameTextStyle": { // 设置名称的样式
                    "fontSize": 14 // 设置字体大小
                },
            }],
            "series": seriesArray
          }
        } else {
          this.chartOptions2 = {}
        }
        this.loading2 = false

      } catch (error) {
        console.log(error)
        this.loading2 = false
        this.chartOptions2 = {}
      }
    },
  }
}

</script>
<style lang="scss" scoped>

</style>
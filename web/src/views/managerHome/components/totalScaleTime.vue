<template>
  <el-card shadow="never" class="mt20">
    <template #header>
      <div style="display: flex; justify-content: space-between;">
        <div style="display: flex;align-items: center;gap: 10px;">
          <div style="display: flex;align-items: center;">
            <img src="../img/scale.svg" alt="" style="width: 40px; height: 40px">
            <span style="font-weight: bold;">大类资产配置</span>
          </div>
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
      <el-col :span="24" v-loading="loading">
        <myChart id="zgmsx" ref="zgmsx" :options="chartOptions" class="echarts_box" resize-dom="cmbfof" />
      </el-col>
    </el-row>
  </el-card>
</template>

<script>
import myChart from '@/components/Echarts'
import api from '../api/totalScaleTime'
import moment from 'moment'
export default {
  name: 'totalScaleTime',
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
        this.ddate_ = [this.queryParams.initBeginDate, this.queryParams.initEndDate];
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
      chartOptions: {},
      fundCode: '',
      title: "",
      tableData: [],
      loading: false,
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
    async loadData() {
      const params = {}
      params.companyId = this.queryParams.companyId;
      params.netPriceCompanyOrFundType = this.companyOrFundType;
      params.netPriceFundCode = this.fundCode;
      params.netPriceBeginDate = this.ddate_[0];
      params.netPriceEndDate = this.ddate_[1];
      this.loading = true
      try {
        const { data } = await api.netPriceTimeData(params)
        let title = this.queryParams.companyName;
        if (this.companyOrFundType !== 'company') {
          title = this.queryParams.fundList.filter((item) => item.fundCode === this.fundCode)[0].fundName
        }
        if (data.data.length > 0) {

          let xData = []
          let yData = []
          let interval = 0;
          let min = Number(data.data[0].yaxisData1);
          let max = Number(data.data[0].yaxisData1);
          let temp;
          data.data.forEach(item => {
            if (!xData.includes(item.xaxisData)) {
              xData.push(item.xaxisData)
            }
            temp = Number(item.yaxisData1)
            yData.push(temp)
            max = temp > max ? temp : max;
            min = temp < min ? temp : min;
          });
          if (xData.length > 31) {
            interval = Math.floor(xData.length / 30);

          }

          this.chartOptions = {
            "animation": false,
            "tooltip": { "trigger": "axis" },
            toolbox: {
              feature: {
                dataView: {
                  optionToContent: this.$fun.optionToContent
                },
                saveAsImage: {
                  name: '总规模时序',
                }
              }
            },
            grid: { left: "80", right: "80", top: "40", bottom: "40", containLabel: true },
            "legend": {
              "data": [{ "name": title, "icon": "circle", "textStyle": { "fontSize": 14 } }],
              "bottom": "10px",
              "itemWidth": 15,
              "itemGap": 20,
              "borderColor": "#FFF",
              textStyle: { fontSize: 14 }
            },
            "xAxis": {
              "type": "category",
              "data": xData,
              "axisLabel": { "fontSize": 14, "show": true, "interval": interval, "rotate": -90, "color": "#000" },
              "axisLine": { "lineStyle": { "color": "#8d8d8d" } },
              "boundaryGap": false,
              "splitLine": { "show": true, "lineStyle": { "type": "dotted" } },
              "axisTick": { "show": false }
            },
            "yAxis": [{
              "name": "(总规模)亿元",
              "nameTextStyle": { // 设置名称的样式
                "fontSize": 14 // 设置字体大小
              },
              "type": "value",
              "splitLine": { "show": true, "lineStyle": { "type": "dotted" } },
              "axisTick": { "show": false },
              "axisLine": { "lineStyle": { "color": "#8d8d8d" } },
              "max": max.toFixed(2),
              "min": min.toFixed(2),
              "axisLabel": { "color": "#000", "fontSize": 14 }
            }],
            "series": [{
              "name": title,
              "type": "line",
              "smooth": true,
              "symbol": "none",
              "yAxisIndex": 0,
              "data": yData
            }]
          }
        } else {
          this.chartOptions = {}
        }
        this.loading = false
      } catch (error) {
        console.log(error)
        this.loading = false
        this.chartOptions = {}
      }
    },
  }
}

</script>
<style lang="scss" scoped>
::v-deep .el-card__body {
  padding: 0;
}
</style>
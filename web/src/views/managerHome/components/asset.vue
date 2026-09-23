<template>
  <el-card shadow="never" class="mt20">
    <template #header>
      <div style="display: flex; justify-content: space-between;">
        <div style="display: flex;align-items: center;gap: 10px;">
          <div style="display: flex;align-items: center;">
            <img src="../img/pie.svg" alt="" style="width: 40px; height: 40px">
            <span style="font-weight: bold;">大类资产配置</span>
          </div>
          <span> {{ queryParams.initEndDate }}</span>
          <el-radio-group v-model="assetPieCompanyOrFundType" @change="radioChange">
            <el-radio label="company" size="large">全部</el-radio>
            <el-radio label="fund" size="large">单产品</el-radio>
          </el-radio-group>
          <el-select v-model="fundCode" v-if="assetPieCompanyOrFundType === 'fund'" filterable style="width: 150px">
            <el-option v-for="item in queryParams.fundList" :key="item.fundCode" :label="item.fundName"
              :value="item.fundCode"></el-option>
          </el-select>
        </div>
        <img src="../img/search.svg" @click="loadData" style="width: 40px; height: 40px;">
      </div>
    </template>
    <el-row v-loading="loading">
      <el-col :span="24">
        <myChart id="dlzcpz" ref="dlzcpz" :options="chartOptions" class="echarts_box" resize-dom="cmbfof" />
      </el-col>
      <el-col :span="24" style="height: 300px;margin-top: 10px;">
        <el-table :data="tableData" border style="width: 100%;margin-top: 40px;" >
          <el-table-column prop="xaxisData" align="center" label="大类资产" />
          <el-table-column prop="yaxisData1" align="center" label="期末投资市值(万元)" />
          <el-table-column prop="yaxisData2" align="center" label="期末占比(%)" />
          <el-table-column prop="yaxisData3" align="center" label="较上月末(%)">
            <template #default="scope">
              <span :style="{
                color: Number(scope.row.yaxisData3) > 0 ? 'red' : (Number(scope.row.yaxisData3) < 0 ? 'green' : '')
              }">
                {{ scope.row.yaxisData3 }}
              </span>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>
  </el-card>
</template>

<script>
import myChart from '@/components/Echarts'
import api from '../api/asset'
export default {
  name: 'asset',
  components:{ myChart },
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
      handler(newVal){
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
  data(){
    return {
      fundCode: '',
      title: "",
      tableData:[],
      chartOptions: {},
      loading: false,
      assetPieCompanyOrFundType: 'company'
    }
  },
  mounted() {},
  methods: {
    radioChange(val){
      if(this.fundCode === ''){
        this.fundCode = this.queryParams.fundList[0].fundCode
      }
    },
    async loadData() {

      try {
        this.loading = true
        const params = {}
        params.companyId = this.queryParams.companyId;
        params.assetPieCompanyOrFundType = this.assetPieCompanyOrFundType;
        params.pieFundCode = this.fundCode;
        params.dDate = this.queryParams.initEndDate;
        const { data } = await api.assetEndTablePie(params)

        if (data.data.length > 0) {
          const totalObj = {
            xaxisData: "合计",
            yaxisData1: 0,
            yaxisData2: 100.00,
            yaxisData3: "-"
          }
          data.data.forEach(element => {
            totalObj.yaxisData1 += Number(element.yaxisData1)
          });
          totalObj.yaxisData1=processing_Decimal(totalObj.yaxisData1,2)
          this.tableData = [...data.data, totalObj];
          this.initChart(data.data);
        } else {
          this.tableData = []
          this.chartOptions = {}
        }
        this.loading = false
      } catch (error) {
        console.log(error)
        this.loading = false
        this.tableData = []
        this.chartOptions = {}
      }
    },
    initChart(data){

      let title = this.queryParams.companyName;

      if(this.assetPieCompanyOrFundType !== 'company'){
        title = this.queryParams.fundList.filter((item) => item.fundCode === this.fundCode)[0].fundName
      }

      let legendData = []
      let seriesData = []
      data.forEach(element => {
        legendData.push(element.xaxisData)
        seriesData.push({ name: element.xaxisData, value: element.yaxisData2 })
        });
        this.chartOptions  = {
            animation: false,
            tooltip: {"trigger": "item", "formatter": "{b} : {c}"},
            toolbox: {
                  feature: {
                    dataView: { optionToContent: this.optionToContent },
                    saveAsImage: { name: '大类资产配置', }
                  }
                },
            title: {"text": title, "textStyle":{ "fontSize":14},"borderColor":"#FFF",  "left": "center"},
            legend: {
                "orient": "horizontal",
                "bottom": "10px",
                "itemWidth": 15,
                "itemGap": 20,
                "borderColor": "#FFF",
                "data": legendData
            },
            grid: {"x": "50px", "y": "50px", "x2": "30px", "y2": "120px"},
            series: [
                {
                    "name": "期末持仓",
                    "type": "pie",
                    "radius": "70px",
                    // "center": ["50%", center_right+"px"],
                    "label": {"normal": {"show": true, "formatter": "{d}%","fontSize": 14}},
                    "itemStyle": {
                        "emphasis": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": "rgba(0, 0, 0, 0.5)"
                        }
                    },
                    "data": seriesData
                }]
        }
    },
    optionToContent(opt, name) {
      let seriesData = opt.series[0].data || []
      let tdHeads = `<td style="padding: 0 10px;min-width: 100px;text-align:center;">大类资产</td><td style="padding: 0 10px;min-width: 120px;text-align:center;">期末占比</td>`
      let table = `<table border="1" style="margin-left:20px;border-collapse:collapse;font-size:14px;text-align:center"><tbody><tr>${tdHeads}</tr>`
      seriesData.forEach(item => {
        table += `<tr><td style="padding: 0 10px;text-align:center;">${item.name}</td><td style="padding: 0 10px;text-align:center;">${item.value}</td></tr>`
      })
      table += '</tbody></table>'
      return table
    },
  }
}

</script>
<style lang="scss" scoped>

</style>

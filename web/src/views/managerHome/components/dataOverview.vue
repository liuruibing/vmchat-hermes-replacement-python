<template>
  <el-row :gutter="20" class="mt20">
    <el-col :span="8">
      <el-card shadow="never">
        <template #header>
          <div class="vertical-center">
            <img src="../img/year.svg" alt="" style="width: 40px; height: 40px"><span style="font-weight: bold;">本年数据总览</span>
          </div>
        </template>
        <el-row>
          <el-col :span="12">
            新增产品：{{ this.yearData.xzAmount }} 只
          </el-col>
          <el-col :span="12">
            规模增长：{{ this.yearData.netPriceChange }} 亿
          </el-col>
        </el-row>
        <el-row class="mt20">
          <el-col :span="12">
            规模增长率：{{ this.yearData.netPriceRatio }} %
          </el-col>
          <el-col :span="12">
            投资收益：{{ this.yearData.income }} 亿
          </el-col>
        </el-row>
      </el-card>
    </el-col>
    <el-col :span="8">
      <el-card shadow="never">
        <template #header>
          <div class="vertical-center">
            <img src="../img/season.svg" alt="" style="width: 40px; height: 40px"><span style="font-weight: bold;">本季数据总览</span>
          </div>
        </template>
        <el-row>
          <el-col :span="12">
            新增产品：{{ this.seasonData.xzAmount }} 只
          </el-col>
          <el-col :span="12">
            规模增长：{{ this.seasonData.netPriceChange }} 亿
          </el-col>
        </el-row>
        <el-row class="mt20">
          <el-col :span="12">
            规模增长率：{{ this.seasonData.netPriceRatio }} %
          </el-col>
          <el-col :span="12">
            投资收益：{{ this.seasonData.income }} 亿
          </el-col>
        </el-row>
      </el-card>
    </el-col>
    <el-col :span="8">
      <el-card shadow="never">
        <template #header>
          <div class="vertical-center">
            <img src="../img/month.svg" alt="" style="width: 40px; height: 40px"><span style="font-weight: bold;">本月数据总览</span>
          </div>
        </template>
        <el-row>
          <el-col :span="12">
            新增产品：{{ this.monthData.xzAmount }} 只
          </el-col>
          <el-col :span="12">
            规模增长：{{ this.monthData.netPriceChange }} 亿
          </el-col>
        </el-row>
        <el-row class="mt20">
          <el-col :span="12">
            规模增长率：{{ this.monthData.netPriceRatio }} %
          </el-col>
          <el-col :span="12">
            投资收益：{{ this.monthData.income }} 亿
          </el-col>
        </el-row>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
import api from '../api/dataOverview'
export default {
  name: 'dataOverview',
  components:{},
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
      yearData: {},
      seasonData: {},
      monthData: {},
    }
  },
  mounted() {

  },
  methods:{
    loadData(){
      this.getYearData()
      this.getSeasonData()
      this.getMonthData()
    },
    async getYearData() {
      try {
        let param = { companyId: this.queryParams.companyId, dDate: this.queryParams.initEndDate };
        const { data } = await api.thisYearCard(param);
        this.yearData = data.data
      } catch (error) {
        console.log(error)
        this.yearData = {}
      }
    },
    async getSeasonData() {
      try {
        let param = { companyId: this.queryParams.companyId, dDate: this.queryParams.initEndDate };
        const { data } = await api.thisSeasonCard(param);
        this.seasonData = data.data
      } catch (error) {
        console.log(error)
        this.seasonData = {}
      }

    },
    async getMonthData() {
      try {
        let param = { companyId: this.queryParams.companyId, dDate: this.queryParams.initEndDate };
        const { data } = await api.thisMonthCard(param);
        this.monthData = data.data
      } catch (error) {
        console.log(error)
        this.monthData = {}
      }
    },
  }
}

</script>
<style lang="scss" scoped>


.vertical-center{
  display: flex; 
  align-items: center; 
  gap: 8px;
}

</style>
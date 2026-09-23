<template>
  <div class="data-overview">

    <span>总资产净值</span>
    <span class="font-red-color">{{ this.data.totalNetPrice }}</span>
    <span>亿元</span>

    <span>今年净资产涨跌幅</span>
    <span :class="this.data.ratioFlag !== '-1' ? 'font-red-color' : 'font-green-color'">
      {{ this.data.thisYearNetPriceRatio }}
      <i class="fa fa-long-arrow-up" v-if="this.data.ratioFlag === '1'"></i>
      <i class="fa fa-long-arrow-down" v-if="this.data.ratioFlag === '-1'"></i>
    </span>

    <span>公司存续产品数量</span>
    <span class="font-red-color">{{ this.data.cxAmount }} </span>
    <span>只</span>

    <span>公司总产品数量</span>
    <span class="font-red-color">{{ this.data.totalAmount }} </span>
    <span>只</span>
  </div>
</template>

<script>
import API from '../api/totalDescription.js'
export default {
  name: 'totalDescription',
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
      data: {
        totalNetPrice: '-',
        thisYearNetPriceRatio: '-',
        cxAmount: '-',
        totalAmount: '-',
        ratioFlag: ''
      }
    }
  },
  mounted() {

  },
  methods:{
    async loadData(){
      try {
        let param = { companyId: this.queryParams.companyId, dDate: this.queryParams.initEndDate };
        const { data } = await API.totalDescription(param)
        this.data = data.data;
        this.data.thisYearNetPriceRatio = this.data.thisYearNetPriceRatio + '%'
      } catch (error) {
        console.log(error)
        this.data = {}
      }
    }
  }
}

</script>
<style lang="scss" scoped>
.data-overview {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.font-red-color {
  color: red;
  font-size: 22px;
}

.font-green-color {
  color: green;
  font-size: 22px;
}
</style>
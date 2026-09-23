<template>
  <el-card shadow="never" class="mt20">
    <template #header>
      <div style="display: flex; justify-content: space-between;">
        <div style="display: flex;align-items: center;gap: 10px;">
          <div style="display: flex;align-items: center;">
            <img src="../img/number.svg" alt="" style="width: 40px; height: 40px">
            <span style="font-weight: bold;">产品业绩总览</span>
          </div>
          <span>日期：</span>
          <el-date-picker v-model="ddate_" type="daterange" :clearable="false" value-format="yyyy-MM-dd" align="left"
            size="small" unlink-panels range-separator="至" start-placeholder="请选择开始日期" end-placeholder="请选择结束日期"
            popper-class="popperDateShortTP" :picker-options="queryParams.datePickerOptions"></el-date-picker>

          <span>基准类型：</span>

                <el-select v-model="ZB_INDEXTYPE" placeholder="请选择" size="small">
                  <el-option v-for="item in ZB_INDEXTYPEOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
                </el-select>


            <div v-show="ZB_INDEXTYPE == '1'" >
              <span>选择基准：</span>

                <el-select v-model="ZB_INDEXCODEA" placeholder="请选择" size="small">
                  <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
                </el-select>

            </div>
            <div v-show="ZB_INDEXTYPE == '2'" style="display: inline-block">
              <span>基准 A</span>

                <el-select v-model="ZB_INDEXCODEA" placeholder="请选择" size="small">
                  <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
                </el-select>
              <span>比例</span>

                <el-input v-model="ZB_INDEXWEIGHTA" size="small" style="width: 85px !important" @blur="handleInputWeight('A')"></el-input>
                %

            </div>
            <div v-show="ZB_INDEXTYPE == '2'" style="display: inline-block">
              <span>基准 B</span>

                <el-select v-model="ZB_INDEXCODEB" placeholder="请选择" size="small">
                  <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
                </el-select>
              <span>比例</span>

                <el-input v-model="ZB_INDEXWEIGHTB" size="small" style="width: 85px !important" @blur="handleInputWeight('B')"></el-input>
                %

            </div>
          <span style="color:red">注：数据更新到T-3日</span>
        </div>
        <img src="../img/search.svg" @click="loadData" style="width: 40px; height: 40px;">
      </div>
    </template>
    <el-tabs v-model="activeTabName" @tab-click="handleTabClick">
      <el-tab-pane v-for="item in tabList" :key="item.name" :label="item.label" :name="item.name"></el-tab-pane>
    </el-tabs>
    <el-table :data="tableData" :default-sort="{ prop: 'betweenValue', order: 'descending' }" stripe border
      @sort-change="handleSortChange" v-loading="loading" :cell-style="{ height: '40px', fontSize: '14px' }"
      :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }" style="width: 100%">
      <el-table-column v-for="col in columns" :key="col.prop" :prop="col.prop" :label="col.label"
        :align="col.align || 'center'" :sortable="col.sortable || false" :min-width="col.width" show-overflow-tooltip>
        <template #header>
          <span style="display: inline-block; text-align: center;">
            {{ col.label }}
            <span v-if="col.break"><br/> {{ activeTabLabel }}</span>
          </span>
        </template>
      </el-table-column>
    </el-table>
    <Pagination :total="total" :limit="page.pageSize" :page="page.pageNum" @pagination="pagination">
    </Pagination>
  </el-card>
</template>

<script>
import Pagination from '@/components/Pagination'
import api from '../api/productPerformance'
import moment from 'moment'
import fun from '@/filters/common'
export default {
  name: 'productPerformance',
  components: { Pagination },
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
      total: 0,
      page: {
        pageNum: 1,
        pageSize: 10,
        orderString: "betweenValue desc",
      },
      ZB_INDEXTYPEOption: [

        {
          id: '1',
          label: '单基准'
        },
        {
          id: '2',
          label: '复合基准'
        }
      ],

        ZB_INDEXCODE: '', // 基准编码
        ZB_INDEXTYPE: '1', // 基准类型
        ZB_INDEXCODEA: '000300', // 基准A
        ZB_INDEXWEIGHTA: '0.0000', // 基准A权重
        ZB_INDEXCODEB: '000300', // 基准B
        ZB_INDEXWEIGHTB: '0.0000', // 基准B权重



      ddate_: [],
      fundCode: '',
      tableData: [],
      loading: false,
      activeTabName: "yield",
      activeTabLabel: "收益率%",
      tabList: [
        { label: '收益率', name: 'yield', unit: "%", func: api.doPerformanceFundYieldList },
        { label: '年化波动率', name: 'volatility', unit: "%" , func: api.doPerformanceYearVolatilityList },
        { label: 'α系数', name: 'alpha', func: api.doPerformanceAlphaList },
        { label: 'β系数', name: 'beta', func: api.doPerformanceBetaList },
        { label: 'Sharpe指数', name: 'sharpe', func: api.doPerformanceSharpeList },
        { label: '特雷诺比率', name: 'treynor', func: api.doPerformanceTreynorList },
        { label: '信息比率', name: 'info', func: api.doPerformanceInfoRateList },
        { label: '跟踪误差', name: 'trackError', func: api.doPerformanceTeList },
        { label: '索提诺比率', name: 'sortino', func: api.doPerformanceSortinoList },
        { label: '卡玛比率', name: 'calmar', func: api.doPerformanceCalmarList },
        { label: '欧米茄比率', name: 'omega', func: api.doPerformanceOmegaList },
        { label: '卡帕比率', name: 'kappa', func: api.doPerformanceKappaList },
        { label: '上行捕获率', name: 'upCapture', func: api.doPerformanceUcrList },
        { label: '下行捕获率', name: 'downCapture', func: api.doPerformanceDcrList },
        { label: '下行标准差', name: 'downStd', unit: "%", func: api.doPerformanceDescVolatilityList },
      ],
      columns: [
        { prop: 'fundCode', label: '产品代码', width: 120, sortable: true, break:false },
        { prop: 'fundName', label: '产品名称', width: 240, sortable: true, break:false },
        { prop: 'fundCreateDate', label: '产品成立日', width: 120, sortable: true, break:false},
        { prop: 'fundEndDate', label: '产品到期日', width: 120, sortable: true , break:false},
        { prop: 'betweenValue', label: '报告区间', width: 120, sortable: true, break:true },
        { prop: 'oneMonthValue', label: '近1月', width: 120, sortable: true, break:true },
        { prop: 'threeMonthValue', label: '近3月', width: 120, sortable: true, break:true },
        { prop: 'sixMonthValue', label: '近6月', width: 120, sortable: true, break:true },
        { prop: 'thisYearValue', label: '今年以来', width: 120, sortable: true, break:true },
        { prop: 'oneYearValue', label: '近1年', width: 120, sortable: true, break:true },
        { prop: 'twoYearValue', label: '近2年', width: 120, sortable: true, break:true },
        { prop: 'threeYearValue', label: '近3年', width: 120, sortable: true, break:true },
        { prop: 'createValue', label: '成立以来', width: 120, sortable: true, break:true },
      ],
    }
  },
  mounted() {
  },
  methods: {

// 权重校验
handleInputWeight(type) {
  const regex = /^(0(\.\d+)?|[1-9]\d*(\.\d+)?)$/
  if (type == 'A') {
    if (!regex.test(this.ZB_INDEXWEIGHTA)) {
      this.$message.closeAll()
      this.$message({
        type: 'warning',
        message: '只能输入大于等于0的数',
        customClass: 'message-warning'
      })
      this.ZB_INDEXWEIGHTA = '0.0000'
      return
    }
    if (this.ZB_INDEXWEIGHTB != '') {
      if (Number(this.ZB_INDEXWEIGHTA) + Number(this.ZB_INDEXWEIGHTB) > 100) {
        this.$message.closeAll()
        this.$message({
          type: 'warning',
          message: '基金A、B权重不能超过100%',
          customClass: 'message-warning'
        })
        this.ZB_INDEXWEIGHTA = '0'
      } else {
        this.ZB_INDEXWEIGHTA = '' + Number(this.ZB_INDEXWEIGHTA).toFixed(4)
      }
    }
  } else {
    if (!regex.test(this.ZB_INDEXWEIGHTB)) {
      this.$message.closeAll()
      this.$message({
        type: 'warning',
        message: '只能输入大于等于0的数',
        customClass: 'message-warning'
      })
      this.ZB_INDEXWEIGHTB = '0.0000'
      return
    }
    if (this.ZB_INDEXWEIGHTA != '') {
      if (Number(this.ZB_INDEXWEIGHTA) + Number(this.ZB_INDEXWEIGHTB) > 100) {
        this.$message.closeAll()
        this.$message({
          type: 'warning',
          message: '基金A、B权重不能超过100%',
          customClass: 'message-warning'
        })
        this.ZB_INDEXWEIGHTB = '0'
      } else {
        this.ZB_INDEXWEIGHTB = '' + Number(this.ZB_INDEXWEIGHTB).toFixed(4)
      }
    }
  }
},
    handleTabClick(tab,event){
      let arr = this.tabList.filter(item => item.name === this.activeTabName);
      this.activeTabLabel = arr[0].label  + (arr[0].unit?arr[0].unit:'')
      this.loadData();
    },
    async loadData() {
      let arr = this.tabList.filter(item => item.name === this.activeTabName);
      //单基准
      if (this.ZB_INDEXTYPE == '1') {
        this.ZB_INDEXCODEB = ''
        this.ZB_INDEXWEIGHTA = ''
        this.ZB_INDEXWEIGHTB = ''
      }
      const params = {}
      params.companyId = this.queryParams.companyId;
      params.performanceBeginDate = this.ddate_[0];
      params.performanceEndDate = this.ddate_[1];
      params.performanceBeginDate = this.ddate_[0];
      params.performanceEndDate = this.ddate_[1];
      params.benchmarks = this.ZB_INDEXTYPE;
      params.benchmarkA = this.ZB_INDEXCODEA;
      params.benchmarkAValue = this.ZB_INDEXWEIGHTA;
      params.benchmarkB = this.ZB_INDEXCODEB;
      params.benchmarkBValue = this.ZB_INDEXWEIGHTB;
      params.limit = this.page.pageSize
      params.offset = (this.page.pageNum -1) * this.page.pageSize
      params.orderString = this.page.orderString
      this.loading = true
      try {
        const { data } = await arr[0].func(params)
        this.tableData = data.data.rows
        this.total = data.data.total
        this.loading = false
      } catch (error) {
        console.log(error)
        this.loading = false
        this.tableData = []
      }
    },
    handleSortChange(val) {
      this.page.orderString = val.prop + " " + (val.order === 'ascending' ? 'asc' : (val.order === 'descending' ? 'desc' : ''));
      this.loadData();
    },
    pagination(val) {
      let { page, limit } = val
      this.page.pageNum = page
      this.page.pageSize = limit
      this.loadData();
    }
  }
}

</script>
<style lang="scss" scoped>
::v-deep .el-table th.el-table__cell>.cell{
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>

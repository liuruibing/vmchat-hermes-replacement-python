<template>
  <div class="emotional-index analyse-page">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formQuery" :inline="true" class="standard-form" :model="formQuery" :rules="searchRules">
          <el-row>
            <el-col :span="24">
<!--              <el-form-item label="" prop="fundCode">
                <el-input v-model="formQuery.fundCode" placeholder="请选择产品代码" size="small" v-on:click.native="openPositionDialog"></el-input>
              </el-form-item>-->
              <el-form-item label="" prop="fundCode">
                <ProductSelectInput
                  v-model="formQuery.product"
                  placeholder="请选择产品"
                  :input-width="'260px'"
                  @select="handleProductSelect"
                  @clear="handleProductClear"
                />
              </el-form-item>
              <el-form-item label="" prop="startDate">
                <el-date-picker
                  v-model="formQuery.startDate"
                  type="date"
                  :picker-options="pickerOptions"
                  size="small"
                  value-format="yyyy-MM-dd"
                  placeholder="请选择开始日期"
                ></el-date-picker>
              </el-form-item>
              <el-form-item label="" prop="endDate">
                <el-date-picker
                  v-model="formQuery.endDate"
                  type="date"
                  size="small"
                  :picker-options="pickerOptions"
                  value-format="yyyy-MM-dd"
                  placeholder="请选择结束日期"
                ></el-date-picker>
              </el-form-item>
              <el-form-item label="" prop="type">
                <el-select v-model="formQuery.calculateType" placeholder="请选择计算方式" size="small">
                  <el-option v-for="item in typeOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item class="">
                <el-button icon="el-icon-search" type="primary" size="small" @click="onSubmit('formQuery')">查询</el-button>
                <el-button icon="el-icon-refresh" type="info" plain size="small" @click="reset">重置</el-button>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>
    </div>
    <div class="chart-main">
      <div class="target-trend">
        <div class="page-model-title">
          <div class="title-icon">
            <div class="color-box"></div>
          </div>
          <span class="title-txt">穿透对比-资产配置比例走势</span>
        </div>
        <div id="standard-table">
          <div id="standard-table-margin">
            <vxe-table
              ref="table1"
              v-loading="tableLoading"
              show-overflow
              :data="tableData"
              :height="tableHeight"
              auto-resize
              sync-resize
              stripe
              :cell-style="{ height: '50px' }"
              style="width: 100%"
              resizable
            >
              <vxe-table-column
                v-for="(col, i) in tableColumns"
                :key="i"
                :prop="col.prop"
                :label="col.label"
                :width="col.width"
                :align="col.align"
                show-overflow-tooltip
                header-align="center"
                stripe
              >
                <template slot-scope="scope">
                  <span>{{ scope.row[col.prop] | noDataFilter }}</span>
                </template>
              </vxe-table-column>
            </vxe-table>
            <vxe-pager
              :current-page="formQuery.pageNum"
              :page-size="formQuery.pageSize"
              :total="total"
              :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
              border
              class="standard-vxe-pager"
              size="medium"
              @page-change="pagination"
            /><!--
            <Pagination :total="total" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination" />-->
          </div>
        </div>
      </div>
    </div>
    <div style="">
      <div class="chart-content" style="background-color: #fff;margin: 0px 10px 10px 10px;">
        <myChart id="jzzs" ref="jzzs" :options="targetTrendOptions" class="echarts_box" resize-dom="cmbfof" />
      </div>
    </div>
    <product-selector
      :isShowButtonAndTag="false"
      :dialog-visible="productSelectorVisible"
      :tree-data="treeData"
      :show-tree-key-array="showTreeKeyArray"
      :select-list="selectList"
      :default-checked-keys="defaultCheckedKeys"
      @closedialog="handleDialogClosed"
      @submitdialog="handleSubmitClick"
    ></product-selector>
  </div>
</template>

<script>
import { TABLE_COLUMNS } from './scripts/tables'
import request from '@/utils/request'
import myChart from '@/components/Echarts'
import productSelector from '@/components/productSelector'
import Pagination from '@/components/Pagination'
import { CHART_COLOR_ARR } from "@/metaData/enum.js"
import store from '../../../store'
import ProductSelectInput from '@/components/productSelector/ProductSelectInput'

export default {
  name: 'TrendNetIndex',
  components: {
    myChart,
    productSelector,
    Pagination,
    ProductSelectInput
  },
  data() {
    const validatebeginDate = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请选择开始日期'))
      } else {
        if (this.formQuery.endDate !== null || this.formQuery.endDate !== undefined || this.formQuery.endDate !== '') {
          const startTime = new Date(value)
          const endTime = new Date(this.formQuery.endDate)
          if (startTime > endTime) {
            callback(new Error('开始日期不能大于结束日期'))
          } else {
            callback()
          }
        } else {
          callback()
        }
      }
    }
    const validateEndDate = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请选择结束日期'))
      } else {
        if (this.formQuery.startDate !== null || this.formQuery.startDate !== undefined || this.formQuery.startDate !== '') {
          const startTime = new Date(this.formQuery.startDate)
          const endTime = new Date(value)
          if (startTime > endTime) {
            callback(new Error('结束日期不能小于开始日期'))
          } else {
            callback()
          }
        } else {
          callback()
        }
      }
    }
    return {
      formQuery: {
        product: null,
        calculateType: 'cb',
        fundCode: '',
        startDate: '',
        endDate: '',
        pageSize: 10,
        pageNum: 1
      },
      // 表格高度
      tableHeight: 0,
      typeOptions: [
        { label: '按成本', value: 'cb' },
        { label: '按市值', value: 'sz' }
      ],
      treeData: [
        {
          label: '产品列表',
          id: 'zstgwb'
        },
        {
          label: '私有产品',
          code: 'sycp'
        }
      ],
      showTreeKeyArray: ['产品列表', '私有产品'],
      selectList: [],
      pickerOptions: {},
      defaultCheckedKeys: 'zstgwb',
      // 选择产品弹窗
      productSelectorVisible: false,
      disabledDate: true,
      targetTrendOptions: {},
      searchRules: {
        startDate: [
          { required: true, message: '请选择开始日期', trigger: 'blur' },
          { validator: validatebeginDate, trigger: 'blur' }
        ],
        endDate: [
          { required: true, message: '请选择结束日期', trigger: 'blur' },
          { validator: validateEndDate, trigger: 'blur' }
        ],
        fundCode: [{ required: true, message: '请选择产品', trigger: 'change' }],
        product: [
          { required: true, message: '请选择产品', trigger: 'change' },
          { validator: validateFund, trigger: 'blur' }
        ]
      },
      //表格
      tableLoading: false,
      tableData: [],
      tableColumns: TABLE_COLUMNS,
      total: 0
    }
  },
  async mounted() {
    var self = this
    var baseTime = store.state.edims.baseTime
    if(baseTime){
      self.formQuery.startDate = baseTime.beginDate
      self.formQuery.endDate = baseTime.endDate
    }
    this.handleTableHeight();
    // this.handleQueryChartData()
  },
  methods: {
    /**
     * @description 动态设置表格高度
     */
    handleTableHeight() {
      this.$nextTick(() => {
        // 根据浏览器高度设置初始高度
        this.tableHeight = window.innerHeight - this.$refs.table1.$el.offsetTop - 150
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.table1.$el.offsetTop - 150
        }
      })
    },
    //点击弹窗
    openPositionDialog() {
      this.productSelectorVisible = true
    },
    //关闭弹窗
    handleDialogClosed() {
      this.productSelectorVisible = false
    },
    handleSubmitClick(arr) {
      this.productSelectorVisible = false
      this.formQuery.fundCode = arr[0].VC_FUNDCODE || ''
      this.selectList = arr
    },
    handleProductSelect: function(product) {
      this.formQuery.fundCode = product.VC_FUNDCODE || ''
    },
    handleProductClear: function() {
      this.formQuery.fundCode = ''
    },
    onSubmit(formName) {
      var self = this
      self.$refs[formName].validate((valid) => {
        if (valid) {
          try {
            self.handleQueryChartData()
            self.queryExamineList()
          } catch (e) {}
        } else {
          return false
        }
      })
    },
    /**
     * 表格
     * */
    queryExamineList() {
      this.tableLoading = true
      try {
        const params = {
          indexCode: '2d2534c3-275a-48cc-8e8d-3b19a759f422',
          fundCode: this.formQuery.fundCode || '',
          calculateType: this.formQuery.calculateType || '',
          startDate: this.formQuery.startDate || '',
          endDate: this.formQuery.endDate || '',
          _pageNum: this.formQuery.pageNum || '',
          _pageSize: this.formQuery.pageSize || '',
          _pageFlag: true
        }
        request({
          url: `/api/report/v1.0/data/sql/2d2534c3-275a-48cc-8e8d-3b19a759f422`,
          method: 'post',
          data: params
        }).then((res) => {
          if (res.data.status === 0) {
            this.tableData = res.data.data.rows || []
            this.total = res.data.data.total
            this.tableLoading = false
          } else {
            this.tableData = []
            this.total = 0
            this.tableLoading = false
          }
        })
      } catch (e) {
        this.tableData = []
        this.total = 0
        this.tableLoading = false
      }
    },

    /**
     * @description 查询
     */

    handleQueryChartData() {
      // 判断条件是否有空值
      if (this.formQuery.fundCode && this.formQuery.fundCode == '') {
        this.$message.closeAll()
        this.$message({
          message: '产品代码不可为空',
          type: 'warning',
          customClass: 'message-warning'
        })
        return
      }

      const params = {
        indexCode: '4dff7cf4-14ee-4c29-b1e0-4ccf5f5fd304',
        fundCode: this.formQuery.fundCode || '',
        calculateType: this.formQuery.calculateType || '',
        startDate: this.formQuery.startDate || '',
        endDate: this.formQuery.endDate || ''
      }
      request({
        url: `/api/report/v1.0/data/sql/4dff7cf4-14ee-4c29-b1e0-4ccf5f5fd304`,
        method: 'post',
        data: params
      }).then((res) => {
        if (res.data.status === 0) {
          const resultData = res.data.data || []
          this.handleChartOptions(resultData)
        }
      })
    },

    /**
     * @description 组装持仓走势数据options
     */
    handleChartOptions(data) {
      const xData = [...new Set(data.map((item) => item.DATESTR))]
      const legendData = [...new Set(data.map((item) => item.VCFUNDCODE))]
      const seriesData = []
      let colors = CHART_COLOR_ARR
      // let colors = ['#fc6769', '#d2a25a', '#789d51', '#6c50f3', '#396f92', '#64AAEF']
      for (var i = 0; i < legendData.length; i++) {
        var ser = {}
        ser.name = legendData[i]
        ser.type = 'bar' //基准线line
        ser.barMaxWidth = 40
        ser.stack = 'one'
        ser.yAxisIndex = 0
        seriesData.push(ser)
      }
      for (var x = 0; x < seriesData.length; x++) {
        var datay = []

        for (var j = 0; j < xData.length; j++) {
          var state = false

          for (var i = 0; i < data.length; i++) {
            if (data[i].DATESTR == xData[j]) {
              if (data[i].VCFUNDCODE == seriesData[x].name) {
                datay.push(data[i].DATAVAL)
                state = true
                //return false;
              }
            }
          }
          if (!state) {
            datay.push(0)
          }
        }
        seriesData[x].data = datay
      }
      this.targetTrendOptions = {
        legend: {
          top: '3%',
          data: legendData,
          itemWidth: 18,
          itemHeight: 12,
          textStyle: { color: '#000', fontSize: 12 }
        },
        color: colors,
        grid: {
          left: '2%',
          right: '3%',
          bottom: '15%',
          top: '12%',
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          formatter: (params) => {
            let tip = params[0].name + '<br>'
            for (let i = 0; i < params.length; i++) {
              tip += params[i].marker + params[i].seriesName + ': ' + Number(params[i].value).toFixed(2) + '<br>'
            }
            return tip
          }
        },
        xAxis: [
          {
            type: 'category',
            axisLine: {
              show: false
            },
            axisTick: {
              show: false
            },
            splitArea: {
              show: true,
              areaStyle: {
                color: ['rgba(250,250,250,0.3)', 'rgba(255,255,255,0.3)']
              }
            },
            splitLine: {
              show: true,
              lineStyle: {
                color: '#e5e5e5',
                type: 'dashed'
              }
            },
            data: xData
          }
        ],
        yAxis: [
          {
            name: '净值占比',
            axisLabel: {
              formatter: '{value}%'
            },
            axisLine: {
              show: false
            },
            axisTick: {
              show: false
            },
            splitArea: {
              show: false
            },
            splitLine: {
              show: true,
              lineStyle: {
                color: '#e5e5e5',
                type: 'dashed'
              }
            }
          },
          {
            axisLine: {
              show: false
            },
            axisTick: {
              show: false
            },
            splitArea: {
              show: false
            },
            splitLine: {
              show: true,
              lineStyle: {
                color: '#e5e5e5',
                type: 'dashed'
              }
            }
          }
        ],
        dataZoom: {
          show: true,
          textStyle: {
            fontSize: 12,
            color: 'transparent'
          }
          // start: 0,
          // end: 20,
          // maxSpan: 80
        },
        series: seriesData
      }
    },
    //重置清空操作
    reset() {
      this.formQuery.startDate = ''
      this.formQuery.fundCode = ''
      this.formQuery.endDate = ''
      this.formQuery.calculateType = 'cb'
    },
    pagination(val) {
      /* const { page, limit } = val
      this.formQuery.pageNum = page
      this.formQuery.pageSize = limit */
      const { currentPage, pageSize } = val;
      // 起始页
      this.formQuery.pageNum = currentPage;
      // 每页数量
      this.formQuery.pageSize = pageSize;
      this.queryExamineList()
    }
  }
}
</script>

<style lang="scss" scoped>
.emotional-index {
  .funds-filter {
    width: 100%;
    // border-bottom: 1px solid #e1e0e0;

    .dbjz {
      ::v-deep .el-select .el-input--small {
        width: 260px !important;
      }

      ::v-deep .el-select .el-select__tags {
        max-width: 234px !important;
      }
    }
  }
  .chart-main {
    margin-top: 3px;
    width: 100%;
    .chart-title {
      padding: 10px 0;
      // border-bottom: 1px solid #0F65DD;

      .title-icon {
        vertical-align: middle;
        display: inline-block;

        .color-box {
          display: inline-block;
          height: 30px;
          width: 2px;
          background-color: #0f65dd;
        }
      }

      .title-txt {
        color: #0f65dd;
        vertical-align: middle;
        height: 35px;
        line-height: 35px;
        font-size: 16px;
        margin-left: 5px;
        display: inline-block;
      }
    }
    .chart-content {
      height: 500px;
      margin: 10px;
      background-color: #fff;
      .echarts_box {
        height: 100%;
        width: 100%;
      }
    }
  }
}

::v-deep .vxe-table .vxe-body--row.row--stripe {
  background-color: #fafafa !important;
}
</style>

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
                  placeholder="开始日期"
                ></el-date-picker>
              </el-form-item>
              <el-form-item label="" prop="endDate">
                <el-date-picker
                  v-model="formQuery.endDate"
                  type="date"
                  size="small"
                  :picker-options="pickerOptions"
                  value-format="yyyy-MM-dd"
                  placeholder="结束日期"
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
          <span class="title-txt">穿透对比-持仓走势</span>
        </div>
        <div class="chart-content" v-loading="searchLoading">
          <myChart id="cczs" ref="cczs" :options="targetTrendOptions" class="echarts_box" resize-dom="cmbfof" />
        </div>
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
import request from '@/utils/request'
import myChart from '@/components/Echarts'
import productSelector from '@/components/productSelector'
import { CHART_COLOR_ARR } from "@/metaData/enum.js"
import store from '../../../store'
import ProductSelectInput from '@/components/productSelector/ProductSelectInput'

export default {
  name: 'PositionIndex',
  components: {
    myChart,
    productSelector,
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
        endDate: ''
      },
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
      searchLoading:false,
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
      }
    }
  },
  async mounted() {
    var self = this
    var baseTime = store.state.edims.baseTime
    if(baseTime){
      self.formQuery.startDate = baseTime.beginDate
      self.formQuery.endDate = baseTime.endDate
    }
    // this.handleQueryChartData()
  },
  methods: {
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
          } catch (e) {}
        } else {
          return false
        }
      })


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
      this.searchLoading=true
      try {
      const params = {
        indexCode: 'a1d80b40-f9ba-46e0-97c1-ce52e924118a',
        fundCode: this.formQuery.fundCode || '',
        calculateType: this.formQuery.calculateType || '',
        startDate: this.formQuery.startDate || '',
        endDate: this.formQuery.endDate || ''
      }
      request({
        url: `/api/report/v1.0/data/sql/a1d80b40-f9ba-46e0-97c1-ce52e924118a`,
        method: 'post',
        data: params
      }).then((res) => {
        if (res.data.status === 0) {
          const resultData = res.data.data || []
          this.handleChartOptions(resultData)
        }
        this.searchLoading=false
      })
      } catch (e) {
      this.searchLoading = false
     }
    },
    /**
     * @description 组装持仓走势数据options
     */
    handleChartOptions(data) {
      const xData = [...new Set(data.map((item) => item.DATESTR))]
      const legendData = [...new Set(data.map((item) => item.FUNDCODE))]
      const seriesData = []
      // let colors = [
      //   '#fc6769',
      //   '#d2a25a',
      //   '#789d51',
      //   '#6c50f3',
      //   '#396f92',
      //   '#f44336',
      //   '#2196F3',
      //   '#FF9800',
      //   '#FFEB3B',
      //   '#FF5722',
      //   '#E91E63',
      //   '#ef9a9a',
      //   '#00BCD4',
      //   '#9FA8DA',
      //   '#E6EE9C',
      //   '#FF5722',
      //   '#795548',
      //   '#9E9E9E',
      //   '#607D8B',
      //   '#ef9a9a',
      //   '#ff5252',
      //   '#7C4DFF',
      //   '#FF6E40',
      //   '#FFC400',
      //   '#448AFF',
      //   '#FFE082',
      //   '#FFCC80',
      //   '#FFAB91',
      //   '#BCAAA4',
      //   '#EEEEEE',
      //   '#f1c40f',
      //   '#e74c3c',
      //   '#2980b9',
      //   '#e67e22',
      //   '#1abc9c'
      // ]
      let colors = CHART_COLOR_ARR
      for (var i = 0; i < legendData.length; i++) {
        var ser = {}
        ser.name = legendData[i]
        ;(ser.type = 'line'), (ser.smooth = true), (ser.symbol = 'none'), (ser.areaStyle = {}), (ser.yAxisIndex = 0)
        seriesData.push(ser)
      }
      for (var x = 0; x < seriesData.length; x++) {
        var datay = []

        for (var j = 0; j < xData.length; j++) {
          var state = false

          for (var i = 0; i < data.length; i++) {
            if (data[i].DATESTR == xData[j]) {
              if (data[i].FUNDCODE == seriesData[x].name) {
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
          type: 'scroll',
          data: legendData,
          itemWidth: 18,
          itemHeight: 12,
          textStyle: { color: '#000', fontSize: 12 }
        },
        color: colors,
        grid: {
          left: '2%',
          right: '3%',
          bottom: '12%',
          top: '22%',
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          formatter: (params) => {
            let tip = params[0].name + '<br>'
            for (let i = 0; i < params.length; i++) {
              if ((i + 1) % 5 == 0) {
                tip += params[i].marker + params[i].seriesName + ': ' + Number(params[i].value).toFixed(2) + '<br>'
              } else {
                tip += params[i].marker + params[i].seriesName + ': ' + Number(params[i].value).toFixed(2) + '&nbsp&nbsp&nbsp&nbsp'
              }
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
            min: 'dataMin',
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
      border-bottom: 1px solid #0f65dd;

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
</style>

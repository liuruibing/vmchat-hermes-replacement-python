<template>
  <div class="emotional-index">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formQuery" :inline="true" class="standard-form" :model="formQuery" :rules="searchRules">
          <el-row>
            <el-col :span="24">
              <el-form-item label="产品代码" prop="fundCode">
                <el-input v-model="formQuery.fundCode" placeholder="产品代码" size="small" v-on:click.native="openPositionDialog"></el-input>
              </el-form-item>
              <el-form-item label="开始时间" prop="startDate">
                <el-date-picker
                  v-model="formQuery.startDate"
                  type="date"
                  :picker-options="pickerOptions"
                  size="small"
                  value-format="yyyy-MM-dd"
                  placeholder="开始日期"
                ></el-date-picker>
              </el-form-item>
              <el-form-item label="结束时间" prop="endDate">
                <el-date-picker
                  v-model="formQuery.endDate"
                  type="date"
                  size="small"
                  :picker-options="pickerOptions"
                  value-format="yyyy-MM-dd"
                  placeholder="结束日期"
                ></el-date-picker>
              </el-form-item>
              <el-form-item class="">
                <el-button icon="el-icon-search" type="primary" size="small" @click="onSubmit('formQuery')">查询</el-button>
                <el-button icon="el-icon-refresh" type="info" plain size="small" @click="reset">重置</el-button>
              </el-form-item>
              <!--<el-form-item label="计算方式" prop="type">
              <el-select v-model="formQuery.calculateType" placeholder="请选择" size="small" >
                <el-option
                  v-for="item in typeOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                ></el-option>
              </el-select>
            </el-form-item>-->
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
          <span class="title-txt">
            穿透对比-业绩归因
            <el-tooltip class="table_header_icon" effect="dark" placement="top">
              <span slot="content">
                1、收益率=组合期间收益率
                <br />
                2、Sharpe=(组合收益率–无风险收益率)/波动率
                <br />
                3、波动率=组合日收益率的标准差*sqrt交易日天数
                <br />
                4、Alpha=组合收益率–(无风险收益率＋β*(基准收益率–无风险收益率))
                <br />
                5、Calmar=组合收益率 / abs（计算区间内最大回撤）
                <br />
                注：取子基金估值中净值数据计算
              </span>
              <i class="el-icon-question" style="cursor: pointer"></i>
            </el-tooltip>
          </span>
        </div>
        <div id="standard-table">
          <div id="standard-table-margin">
            <vxe-table
              v-loading="tableLoading"
              show-overflow
              :data="tableData"
              auto-resize
              sync-resize
              :cell-style="{ height: '50px' }"
              stripe
              style="width: 100%"
              max-height="500"
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
            <Pagination :total="total" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination" />
          </div>
        </div>
      </div>
    </div>
    <!--<div style="margin-top: 60px">
    <div class="chart-content">
      <myChart
        id="zbzs"
        ref="zbzs"
        :options="targetTrendOptions"
        class="echarts_box"
        resize-dom="cmbfof"
      />
    </div>
    </div>-->
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

export default {
  name: 'PerformanceIndex',
  components: {
    myChart,
    productSelector,
    Pagination
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
        calculateType: 'cb',
        fundCode: '',
        startDate: '',
        endDate: '',
        pageSize: 10,
        pageNum: 1
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
      // 选择产品弹窗
      productSelectorVisible: false,
      disabledDate: true,
      targetTrendOptions: {},
      searchRules: {
        startDate: [
          { required: true, message: '请选择开始日期', trigger: 'blur' },
          {
            validator: validatebeginDate,
            trigger: 'blur'
          }
        ],
        endDate: [
          { required: true, message: '请选择结束日期', trigger: 'blur' },
          {
            validator: validateEndDate,
            trigger: 'blur'
          }
        ],
        fundCode: [{ required: true, message: '请选择产品', trigger: 'change' }]
      },
      //表格
      tableLoading: false,
      tableData: [],
      tableColumns: TABLE_COLUMNS,
      total: 0
    }
  },
  async mounted() {
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
    onSubmit(formName) {
      var self = this
      self.$refs[formName].validate((valid) => {
        if (valid) {
          try {
            /* self.handleQueryChartData()*/
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
          indexCode: '073e4d6e-72c5-4440-839c-58ee8c8b9c16',
          fundCode: this.formQuery.fundCode || '',
          calculateType: this.formQuery.calculateType || '',
          startDate: this.formQuery.startDate || '',
          endDate: this.formQuery.endDate || '',
          _pageNum: this.formQuery.pageNum || '',
          _pageSize: this.formQuery.pageSize || '',
          _pageFlag: true
        }
        request({
          url: `/api/report/v1.0/data/sql/073e4d6e-72c5-4440-839c-58ee8c8b9c16`,
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

    /*  handleQueryChartData() {
      // 判断条件是否有空值
      if (this.formQuery.fundCode && this.formQuery.fundCode == '') {
        this.$message.closeAll()
        this.$message.warning('产品代码不可为空')
        return
      }

      const params = {
        indexCode: '4dff7cf4-14ee-4c29-b1e0-4ccf5f5fd304',
        fundCode: this.formQuery.fundCode || '',
        calculateType: this.formQuery.calculateType || '',
        startDate: this.formQuery.startDate || '',
        endDate: this.formQuery.endDate || '',
      }
      request({
        url: `/api/report/v1.0/data/sql/4dff7cf4-14ee-4c29-b1e0-4ccf5f5fd304`,
        method: 'post',
        data: params
      }).then(res => {
        if (res.data.status === 0) {
          const resultData = res.data.data || []
          this.handleChartOptions(resultData)
        }
      })
    },*/

    /* /!**
     * @description 组装持仓走势数据options
     *!/
    handleChartOptions(data) {
      const xData = [...new Set(data.map(item => item.DATESTR))]
      const legendData = [...new Set(data.map(item => item.VCFUNDCODE))]
      const seriesData = []
      let colors = ['#fc6769', '#d2a25a', '#789d51', '#6c50f3', '#396f92']
      for (var i = 0; i < legendData.length; i++) {
        var ser = {};
        ser.name = legendData[i];
        ser.type= 'line',
          ser.smooth= true,
          ser.symbol= 'none',
          ser.areaStyle={},
          ser.yAxisIndex = 0;
        seriesData.push(ser)
      }
      for (var x = 0; x < seriesData.length; x++) {
        var datay = [];

        for (var j = 0; j < xData.length; j++) {
          var state = false;

            for(var i = 0;i < data.length;i++){
            if (data[i].DATESTR == xData[j]) {
              if (data[i].VCFUNDCODE == seriesData[x].name) {
                datay.push(data[i].DATA)
                state = true;
                //return false;
              }
            }
          }
          if (!state) {
            datay.push(0)
          }
        }
        seriesData[x].data = datay;
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
          formatter: params => {
            let tip = params[0].name + '<br>'
            for (let i = 0; i < params.length; i++) {
              tip +=
                params[i].marker + params[i].seriesName + ': ' + Number(params[i].value).toFixed(2) + '<br>'
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
            name:'净值占比',
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
    },*/
    //重置清空操作
    reset() {
      this.formQuery.startDate = ''
      this.formQuery.fundCode = ''
      this.formQuery.endDate = ''
      this.formQuery.calculateType = 'cb'
    },
    pagination(val) {
      const { page, limit } = val
      this.formQuery.pageNum = page
      this.formQuery.pageSize = limit
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
      margin-top: 15px;

      .echarts_box {
        height: 100%;
        width: 100%;
      }
    }
  }
}

::v-deep .el-button.el-button--info {
  color: #333;
  background-color: #dddddd;
  border-color: #dddddd;
}

::v-deep .vxe-table .vxe-body--row.row--stripe {
  background-color: #f9fafe !important;
}
</style>

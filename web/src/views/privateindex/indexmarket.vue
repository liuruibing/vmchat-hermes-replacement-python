<template>
  <div class="privateIndexMarket">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formInline" class="standard-form" :inline="true" :rules="rules" :model="formInline">
          <el-form-item prop="ddate_" label="日期">
            <el-date-picker v-model="formInline.ddate_" type="daterange" value-format="yyyy-MM-dd" align="left"
              size="small" unlink-panels range-separator="至" start-placeholder="请选择开始日期" end-placeholder="请选择结束日期"
              popper-class="popperDateShortTP" :picker-options="dateShortcut()"></el-date-picker>
          </el-form-item>

          <el-form-item label="私募指数" prop="indexCodeArray" class="index">
            <el-select ref="indexCodeRef" @change="handleIndexCodeChange" v-model="formInline.indexCodeArray" size="small" multiple clearable filterable collapse-tags placeholder="请选择私募指数">
              <el-option v-for="item in indexListOptions" :key="item.indexCode" :label="item.indexName" :value="item.indexCode" />
            </el-select>
          </el-form-item>
          <el-form-item label="对比指数" prop="compareIndexCodeArray" class="index">
            <el-select ref="compareIndexCodeRef" @change="handleCompareIndexCodeChange" v-model="formInline.compareIndexCodeArray" size="small" multiple clearable filterable collapse-tags placeholder="请选择对比指数">
              <el-option v-for="item in compareIndexListOptions" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
            </el-select>
          </el-form-item>
          <el-form-item label="频率" prop="frequency" class="frequency">
            <el-select v-model="formInline.frequency" size="small" filterable placeholder="请选择频率">
              <el-option label="日频" value="DAY" />
              <el-option label="周频" value="WEEK" />
            </el-select>
          </el-form-item>

          <el-form-item style="">
            <el-button type="primary" size="small" icon="el-icon-search" @click="handleSearch">查询</el-button>
            <el-button type="info" icon="el-icon-refresh" size="small" plain @click="handleResetForm">重置</el-button>
            <el-button type="info" size="small" icon="el-icon-refresh" @click="handleRecalculate">重新计算</el-button>
            <el-button type="info" size="small" :icon="exportLoading ? 'el-icon-loading' : 'el-icon-download'":disabled="isDisabled" @click="exportData">{{ downLoadText }}</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <div class="table-content" id="standard-table">
      <div id="standard-table-margin">
        <vxe-table v-loading="tableLoading" ref="refsTable" :cell-style="{ height: '50px' }" :data="tableData"
          :height="tableHeight" :seq-config="{ seqMethod }" auto-resize stripe sync-resize show-overflow="tooltip"
          :sort-config="{ remote: true }" style="width: 100%" @sort-change="customSortMethod" resizable>
          <vxe-table-column v-for="(item, index) in column" :key="item.prop + index" :align="item.align"
            :field="item.prop" :show-overflow-tooltip="item.showtooltip" :title="item.title" :min-width="item.width"
            header-align="center" :sortable="item.sortable">
            <template slot-scope="{ row }">
              <div v-if="item.prop === 'symbolType'">
                <span v-if="row[item.prop] == 'PRODUCT'">产品类型</span>
                <span v-else>指数类型</span>
              </div>
              <div v-else>
                <span>{{ row[item.prop] | noDataFilter }}</span>
              </div>
            </template>
          </vxe-table-column>
        </vxe-table>
        <div class="table-footer">
          <Pagination :total="total" :limit="pageList._pageSize" :page="pageList._pageNum" @pagination="pagination" />
        </div>
      </div>
    </div>
    <div class="chart-content" v-loading="chartLoading">
      <myChart id="smzshq" ref="smzshq" :options="chartOptions" class="echarts_box" resize-dom="cmbfof" />
    </div>
  </div>
</template>

<script>
import myChart from '@/components/Echarts'
import { CHART_COLOR_ARR } from "@/metaData/enum.js"
import { TABLE_INDEXMARKET_COLUMNS } from './scripts/constants'
import Pagination from '@/components/Pagination'
import request from '@/utils/request'
import {
  selectPrivateIndexList,
  selectPrivateIndexMarketByPage,
  recalculatePrivateIndexMarket,
  selectDate
} from './scripts/api'

import commonFun from '@/filters/common.js'
import { downLoadFileByUrl } from '@/utils'
import commonAPI from '@/api/common.js'


export default {
  name: 'privateIndexMarket',
  components: {
    Pagination,
    myChart
  },
  data() {
    return {
      formInline: {
        ddate_: [],
        indexCodeArray: [],
        compareIndexCodeArray: [],
        frequency: 'DAY',
        orderString: ''
      },
      rules:{
        ddate_: [
          { type: 'array', required: true, message: '请选择日期', trigger: 'change' }
        ],
        indexCodeArray: [
          { type: 'array', required: true, message: '请选择私募指数', trigger: 'change' }
        ],
        compareIndexCodeArray: [
          { type: 'array', required: true, message: '请选择对比指数', trigger: 'change' }
        ],
        frequency: [
          { type: 'string', required: true, message: '请选择频率', trigger: 'change' }
        ]
      },
      indexListOptions: [],
      compareIndexListOptions: [],
      // 表格高度
      tableHeight: 0,
      // 表格loading
      tableLoading: false,
      // 表格数据
      tableData: [],
      // 表格列
      column: TABLE_INDEXMARKET_COLUMNS,

      // 分页信息
      pageList: {
        _pageSize: 10,
        _pageNum: 1,
        _pageFlag: true
      },
      // 总条数
      total: 0,

      /* 按钮禁止与否 */
      isDisabled: false,
      // 导出图标
      downLoadIcon: "el-icon-download",
      // 导出提示文字
      downLoadText: "导出",
      exportLoading: false,
      //分类
      chartOptions: {},
      chartLoading: false
    }
  },
  async mounted() {
    await Promise.all([
      this.getBeginEndDate(),
      this.getIndexListOptions(),
      this.getCompareIndexListOptions()]);
    this.handleSearch()
  },
  beforeDestroy() {
    // 组件销毁移除监听事件
    window.onresize = null;
  },
  methods: {

    handleIndexCodeChange(val){

      if(val.length > 5){
        this.formInline.indexCodeArray = val.slice(0,5);
        setTimeout(() => {
          this.$refs.indexCodeRef.blur()
        }, 50)
        this.$message({
          type: 'error',
          message: "最多选择5个私募指数",
          customClass: 'message-error'
        })
      }
    },
    handleCompareIndexCodeChange(val){
      if(val.length > 2){
        this.formInline.compareIndexCodeArray = val.slice(0,2);
        setTimeout(() => {
          this.$refs.compareIndexCodeRef.blur()
        }, 50)
        this.$message({
          type: 'error',
          message: "最多选择2个对比指数",
          customClass: 'message-error'
        })
      }
    },
    getBeginEndDate(){
      return new Promise((resolve, reject) => {
        selectDate()
          .then(res => {
            let { status, data } = res.data
            if (status === 200) {
              this.formInline.ddate_ = [data.beginDate,data.endDate]
              resolve()
            } else {
              reject()
            }
          })
          .catch(err =>{
            reject()
          })
      })
    },
    getIndexListOptions() {
      return new Promise((resolve, reject) => {
        selectPrivateIndexList({}).then(res => {
          let { status, data } = res.data
          if (status === 200) {
            this.indexListOptions = data
            this.formInline.indexCodeArray = this.indexListOptions.slice(0, 3).map(item => item.indexCode);
            resolve()
          }else{
            reject()
          }
        })
        .catch(err =>{
          reject()
        })
      })
    },
    getCompareIndexListOptions() {

      return new Promise((resolve, reject) => {
        commonAPI.edimsSelectType("APPLYINDEXENUM")
          .then(res => {
            let { status, data } = res.data
            if (status === 0) {
              this.compareIndexListOptions = data
              this.formInline.compareIndexCodeArray = this.compareIndexListOptions.slice(0, 1).map(item => item.dimCde);
              resolve()
            } else {
              reject()
            }
          })
          .catch(err => {
            resolve()
          })
      })
    },
    // 日期快捷选项
    dateShortcut() {
      return commonFun.dateShortcut()
    },
    // 排序的公共方法
    customSortMethod(val) {
      this.formInline.orderString = commonFun.queryOrderBy_vxe_template(val)
      this.handleSearchTable()
    },


    /* 自定义序号显示 */
    seqMethod({ rowIndex }) {
      return (
        (this.pageList._pageNum - 1) * this.pageList._pageSize + rowIndex + 1
      );
    },

    /**
     * @description 表单重置
     */
    handleResetForm() {
      this.$refs['formInline'].resetFields()
    },
    /**
     * @description 监听分页
     */
    pagination(val) {
      const { page, limit } = val
      this.pageList._pageNum = page
      this.pageList._pageSize = limit
      this.handleSearchTable()
    },
    /**
     * @description 去除无值字段，包含数组
     */
    parameterSrc(data) {
      const newData = {}
      for (const key in data) {
        if (data[key] === '' || data[key] === undefined || data[key] === null || JSON.stringify(data[key]) === '[]') {
        } else {
          newData[key] = data[key]
        }
      }
      return newData
    },

    handleSearch(){
      this.handleSearchTable()
      this.initChart()
    },
    /**
     * @description 表格查询
     */
    handleSearchTable() {
      this.$refs['formInline'].validate((valid) => {
        if(valid){
          const params = {}
          params.beginDate = this.formInline.ddate_[0]
          params.endDate = this.formInline.ddate_[1]
          params.indexCodeArray = this.formInline.indexCodeArray;
          params.frequency = this.formInline.frequency;
          params.limit = this.pageList._pageSize
          params.offset = (this.pageList._pageNum - 1) * this.pageList._pageSize
          params.orderString = this.formInline.orderString
          const data = this.parameterSrc(params)
          this.tableLoading = true
          this.tableData = []
          selectPrivateIndexMarketByPage(data)
          .then((res) => {
            if (res.data.status === 200) {
              this.tableData = res.data.data.rows || []
              this.total = res.data.data.total || 0
              this.tableLoading = false
            } else {
              this.tableLoading = false
              this.$message({
                type: 'error',
                message: res.data.message || '查询失败',
                customClass: 'message-error'
              })
            }
          })
          .catch((e) => {
            this.tableLoading = false
          })
        }
      })
    },

    /**
     *@description echarts
     */
    initChart() {

      this.$refs['formInline'].validate((valid) => {
        if (valid) {
          this.chartLoading = true
          const params = {}
          params.beginDate = this.formInline.ddate_[0]
          params.endDate = this.formInline.ddate_[1]
          let indexCodeArray = this.formInline.indexCodeArray;
          let indexCodes = indexCodeArray.join(',');
          params.indexCodes = indexCodes;
          params.frequency = this.formInline.frequency;
          let compareIndexCodeArray = this.formInline.compareIndexCodeArray;
          let baseCodes = compareIndexCodeArray.join(',');
          params.baseCodes = baseCodes;
          params.indexCode='58b67612-e042-46a9-bb6e-22f7b4f72a44';

          request({
            url: `/api/report/v1.0/data/sql/${params.indexCode}`,
            method: 'post',
            data: params
          }).then(res => {
            this.chartLoading = false
            let { status, data } = res.data
            if (status === 0) {
              let xData = [];
              let seriesMap = []
              let seriesArray = []

              for (let i = 0; i < data.length; i++) {
                   seriesMap.push(data[i].indexName)
                   let oneSeries= []
                   let oneIndexData=data[i].data
                   for(let j=0;j<oneIndexData.length;j++){
                    oneSeries.push(oneIndexData[j].F_INDEX_PRICE_GYH)
                     if(i===0){
                       xData.push(oneIndexData[j].TDATE)
                     }
                   }

                  let series = {
                    name: data[i].indexName,
                    type: 'line',
                    data: oneSeries,
                    smooth: true,
                    symbol: 'none',
                    areaStyle: { color: CHART_COLOR_ARR[i], opacity: 0.3 }
                  }

                seriesArray.push(series)

              }

              let interval = 0;
              if(xData.length > 31){
                interval = Math.floor(xData.length / 30)
              }
              this.chartOptions = {
                color: CHART_COLOR_ARR,
                // 图例
                legend: {
                  data: seriesMap
                },
                xAxis: {
                  type: 'category',
                  data: xData,
                  boundaryGap: false,
                  axisLabel: {
                    interval: interval,
                    rotate: -90
                  }
                },
                yAxis: {
                  type: 'value'
                },
                tooltip: {
                  trigger: 'axis'
                },
                toolbox: {
                  feature: {
                    dataView: {
                      optionToContent: this.$fun.optionToContent
                    },
                    saveAsImage: {
                      name: '私募指数行情',
                    }
                  }
                },
                grid: {
                  left: '2%',
                  right: '3%',
                  bottom: '15%',
                  top: '10%',
                  containLabel: true
                },
                series: seriesArray
              };
            } else {
              this.chartLoading = false
              this.$message({
                type: 'error',
                message: res.data.message || '查询失败',
                customClass: 'message-error'
              })
            }
          })
            .catch(err => {
              this.chartLoading = false
            })
        }
      })
    },
    /**
     * @description 重新计算
     */
    handleRecalculate() {
      this.$refs['formInline'].validate((valid) => {
        if (valid) {

          this.$confirm("确认是否要重新计算?", "提示", {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "warning"
          }).then(() => {
            const params = {}
            params.beginDate = this.formInline.ddate_[0]
            params.endDate = this.formInline.ddate_[1]
            params.indexCodeArray = this.formInline.indexCodeArray;
            params.frequency = this.formInline.frequency;
            params.limit = this.pageList._pageSize
            params.offset = (this.pageList._pageNum - 1) * this.pageList._pageSize
            params.orderString = this.formInline.orderString
            const data = this.parameterSrc(params)
            this.tableLoading = true
            this.tableData = []
            recalculatePrivateIndexMarket(data)
              .then((res) => {
                if (res.data.status === 200) {
                  this.$message.success("执行成功");
                  this.handleSearch()
                } else {
                  this.tableLoading = false
                  this.$message({
                    type: 'error',
                    message: res.data.message || '重新计算失败',
                    customClass: 'message-error'
                  })
                }
              })
              .catch((e) => {
                this.tableLoading = false
              })
          })
        }
      })
    },
    //导出数据
    exportData() {

      this.$refs['formInline'].validate((valid) => {
        if (valid) {
          this.downLoadText = "导出中...";
          this.exportLoading = true;
          this.isDisabled = true;

          let params = {}
          params.beginDate = this.formInline.ddate_[0]
          params.endDate = this.formInline.ddate_[1]
          params.indexCodeArray = this.formInline.indexCodeArray;
          params.frequency = this.formInline.frequency;
          params.orderString = this.formInline.orderString

          const fileName = '私募指数行情列表.xls'
          const url = '/api/gfprivateindexmarket/downPrivateIndexMarket'
          downLoadFileByUrl(url, params, fileName, this)
          setTimeout(() => {
            this.tableLoading = false;
            this.exportLoading = false;
            this.isDisabled = false;
            this.downLoadText = "导出";
          }, 5000)
        }
      })
    },
  },
}
</script>
<style lang="scss" scoped>
.pagination-container {
  .el-input {
    width: 100px !important;
  }
}
::v-deep .el-dialog.customClass {
  width: 45% !important;
}
.customClass .el-dialog__body .privateIndexMarket .el-form {
  width: 100% !important;
}
::v-deep .vxe-table--render-default .vxe-cell--checkbox:not(.is--disabled):hover .vxe-checkbox--icon:before {
  border-color: #e9c5a5 !important;
}
.privateIndexMarket {
  .index {
    ::v-deep .el-select .el-input--small {
      width: 200px !important;
    }

    ::v-deep .el-select .el-select__tags {
      max-width: 200px !important;
    }
  }

  .chart-content {
    height: 450px;
    margin-top: 50px;

    .echarts_box {
      height: 100%;
      width: 100%;
    }
  }
}

</style>

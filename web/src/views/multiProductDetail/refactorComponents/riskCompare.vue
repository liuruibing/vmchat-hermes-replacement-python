<template>
  <div class="riskCompare">
    <div v-if="showRetracement" class="retracement">
      <div class="title">
        <div class="title-icon">
          <div class="color-box"></div>
        </div>
        <div class="title-txt">
          <span>动态回撤对比
            <el-tooltip class="item table_header_icon" effect="dark" placement="top" content="T日回撤=（T日累计单位净值-回撤区间最大累计单位净值）/回撤区间最大累计单位净值（回撤区间为查询开始日至T日）">
              <i class="el-icon-question" style="cursor: pointer;"></i>
            </el-tooltip>
          </span>
        </div>
        <el-button
          :disabled="exportDisabled"
          size="small"
          style="float: right"
          type="info"
          plain
          @click="tableToExcel"
        >
          导出excel
        </el-button>
      </div>
      <div v-loading="retracementLoading" class="risk-compare-content chart-content">
        <myChart id="dthcdb" ref="dthcdb" :options="chartOptions" class="echarts_box" resize-dom="cmbfof"/>
      </div>
    </div>
    <div v-if="showEarnRisk" class="earn-risk">
      <div class="title">
        <div class="title-icon">
          <div class="color-box"></div>
        </div>
        <div class="title-txt">
          <span>收益与风险指标对比</span>
        </div>
      </div>
      <div style="margin-top: 20px;">
        <span style="color:#ff0000;padding-left: 30px;">数据截止：{{IndustryDataUpDate}}</span>
      </div>
      <div v-loading="earnRiskLoading" class="risk-compare-content" id="standard-table">
        <vxe-table
          :cell-style="setCellStyle"
          :data="tableData"
          auto-resize
          border
          show-header-overflow
          show-overflow
          :sort-config="{ remote: true, defaultSort: { field: 'YDATE1', order: 'desc' } }"
          @sort-change="customSortMethod"
        >
          <vxe-column
            v-for="col in riskTableColumns"
            :key="col.prop"
            :field="col.prop"
            :title="col.label"
            :sortable="col.sortable"
            align="center"
            header-align="center"
          >
            <template slot-scope="scope">
              <span v-if="convertNum.includes(col.prop)">
                {{ scope.row[col.prop] | numberToFixedStr(2, 100, '%') }}
              </span>
              <span v-else-if="col.prop === 'YDATE'">
                {{ scope.row[col.prop] | noDataFilter }}
              </span>
              <span v-else>{{ scope.row[col.prop] | numberToFixedStr(2, 1) }}</span>
            </template>
          </vxe-column>
        </vxe-table>
        <div class="tips">备注：红色代表当前列中该指标值最优的产品，绿色代表当前列中该指标值最差的产品</div>
      </div>
    </div>
  </div>
</template>

<script>
import commonAPI from '@/api/common.js'
import myChart from '@/components/Echarts'
import { chartOptions, riskTableColumns } from '../script/common'
import { merger } from '@/utils'
import XLSX from 'xlsx'
import { saveAs } from 'file-saver'
import commonFun from '@/filters/common'

export default {
  name: 'RiskCompare',
  components: {
    myChart
  },
  props: {
    formQuery: {
      type: Object,
      default: () => {
      }
    }
  },
  data() {
    return {
      IndustryDataUpDate:'',
      // 根据权限控制是否展示模块
      showRetracement: false,
      showEarnRisk: false,
      // 收益与风险指标对比列loading
      earnRiskLoading: false,
      orderString:'YDATE1 desc',
      // 收益与风险指标对比数据
      tableData: [],
      // 收益与风险指标对比列
      riskTableColumns: riskTableColumns,
      // 收益与风险指标对比计算字段
      convertNum: ['YDATE1', 'YDATE2', 'YDATE3', 'YDATE7'],
      // 收益与风险指标对比列字段
      constartIndexArr: ['YDATE1', 'YDATE2', 'YDATE3', 'YDATE4', 'YDATE5', 'YDATE6', 'YDATE7', 'YDATE8'],
      // 动态回撤对比options
      chartOptions: {},
      // 动态回撤对比导出
      chartData: [],
      // 表头
      legend: [],
      xData: [],
      exportDisabled: false,
      // 动态回撤对比loading
      retracementLoading: false
    }
  },
  methods: {

    //业绩对比排序
    customSortMethod(val) {
      this.orderString = commonFun.queryOrderBy_vxe_template(val)
      this.getEarnRiskData('cdb65d50-2f78-40bc-9263-fc0e16dda849');
    },
    /**
     * @desc 初始化数据
     */
    initData() {
      this.fun_iframeSrc()
    },
    /**
     * @description 调用查询权限
     */
    fun_iframeSrc() {
      this.queryAuthIndex()
    },
    /**
     * @description 获取权限指标
     */
    queryAuthIndex() {
      const params = {}
      params.templateCode = 'f059736f-e776-4da6-bde5-4de3d0230f15'
      params.fundCode = this.formQuery.productCodes
      commonAPI.selectIndexInfos(params).then(res => {
        if (res.data.status === 0) {
          const result = res.data.data || []
          const authArr = result.map(item => item.vcCode)
          if (authArr.includes('181c6c26-8b10-421f-804c-dd80527c75f2')) {
            this.getRetracementData('36d4f767-d2ad-41d2-9168-7eec4564d3cb')
            this.showRetracement = true
          } else {
            this.showRetracement = false
          }
          if (authArr.includes('6bbc0080-1b58-476f-b477-c89be8a8023b')) {
            this.getEarnRiskData('cdb65d50-2f78-40bc-9263-fc0e16dda849')
            this.IndustryDataUpDate = ''
            this.getEarnRiskDataDate()
            this.showEarnRisk = true
          } else {
            this.showEarnRisk = false
          }
        } else {
          this.$message.error(res.data.message || '权限获取失败')
        }
      })
    },
    /**
     * @description 根据权限查询动态回撤对比
     */
    getRetracementData(indexCode) {
      const params = {
        indexCode
      }
      params.startDate = this.formQuery.startDate || ''
      params.endDate = this.formQuery.endDate || ''
      params.productCodes = this.formQuery.productCodes || ''
      params.kpiCode = this.formQuery.kpiCode || ''
      params.baseCode = this.formQuery.dbjz.length ? this.formQuery.dbjz.join(',') : ''
      this.retracementLoading = true
      this.exportDisabled = true
      commonAPI.getDataBysqlCode(params).then(res => {
        if (res.data.status === 0) {
          const result = res.data.data || []
          if (result && result.length) {
            this.setChartOptions(result)
            this.chartData = result
            this.retracementLoading = false
            this.exportDisabled = false
          }
        } else {
          this.retracementLoading = false
          this.exportDisabled = false
          this.$message.error(res.data.message || '查询动态回撤对比失败')
        }
      })
    },
    /**
     * @description 组装echarts options
     */
    setChartOptions(data) {
      data.forEach(item => {
        if (item.YDATE1) {
          item.YDATE1 = item.YDATE1 * 100
        }
      })
      const xData = [...new Set(data.map(item => item.XDATE))]
      const legend = []
      const seriesData = []
      const mergeData = merger(data, 'YDATE')
      let color = [
        '#ec9598',
        '#eac083',
        '#bce295',
        '#a194e0',
        '#85b9db',
        '#8EB4E3',
        '#c8aee9',
        '#FAC090',
        '#f3d3d3',
        '#efd8e5',
        '#e0bfa4'
      ]
      mergeData.forEach(item => {
        const tempOrigin = []
        const seriesObj = {
          name: item.YDATE,
          type: 'line',
          symbol: 'none',
          lineStyle: {
            normal: {
              width: 0.5
            }
          },
          areaStyle: {},
          data: []
        }
        legend.push({ name: item.YDATE, icon: 'roundRect' })
        for (let i = 0; i < xData.length; i++) {
          const temp = xData[i]
          const objExample = Object.assign({}, item.origin[0])
          objExample.XDATE = temp
          objExample.YDATE1 = ''
          const obj = item.origin.find(sitem => sitem.XDATE == temp) || objExample
          tempOrigin.push(obj)
        }
        item.origin = tempOrigin
        seriesObj.data = item.origin.map(item => item.YDATE1)
        seriesData.push(seriesObj)
      })
      this.chartOptions = chartOptions
      this.chartOptions.legend.data = legend
      this.chartOptions.xAxis.data = xData
      this.chartOptions.series = seriesData
      this.chartOptions.color = color

      this.legend = legend
      this.xData = xData
    },
    /**
     * @description echarts导出表格
     */
    tableToExcel() {
      const data = []
      let obj = {}

      const mergeData = merger(this.chartData, 'YDATE')
      mergeData.forEach((items, indexs) => {
        for (let i = 0; i < this.xData.length; i++) {
          const item = this.xData[i]
          obj = {}
          obj['日期'] = item
          const tempObj = items['origin'].find(e => e.XDATE === item)
          obj[items['YDATE']] = tempObj.YDATE1.toFixed(2) + '%'
          const index = data.findIndex(k => k['日期'] === item)
          if (indexs < 1) {
            data.push(obj)
          }
          if (index !== -1) {
            data[index][items['YDATE']] = tempObj.YDATE1.toFixed(2) + '%'
          } else {
            // obj[items['YDATE']] = tempObj.YDATE1
          }
        }
      })

      // 创建一个工作簿对象
      const workbook = XLSX.utils.book_new()

      // // 创建一个工作表对象
      const worksheet = XLSX.utils.json_to_sheet(data)

      // // 将工作表对象添加到工作簿中
      XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1')

      // // 将工作簿转换为Excel文件的二进制数据
      const excelData = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' })

      // // 创建一个Blob对象
      const blob = new Blob([excelData], {
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      })

      // // 使用FileSaver保存文件
      saveAs(blob, '动态回撤对比.xlsx')
    },
    /**
     * @description 根据权限查询收益与风险指标对比
     */
    getEarnRiskData(indexCode) {
      const params = {
        indexCode
      }
      params.startDate = this.formQuery.startDate || ''
      params.endDate = this.formQuery.endDate || ''
      params.productCodes = this.formQuery.productCodes || ''
      params.kpiCode = this.formQuery.kpiCode || ''
      params.baseCode = this.formQuery.dbjz.length ? this.formQuery.dbjz.join(',') : ''
      params.orderString=this.orderString
      this.earnRiskLoading = true
      commonAPI.getDataBysqlCode(params).then(res => {
        if (res.data.status === 0) {
          const result = res.data.data || []
          if (result && result.length) {
            this.tableData = result
            const filterTable = this.tableData.filter(item => !item.RN)
            this.constartIndexArr.forEach(item => {
              this.handleConstartIndex(filterTable, item)
            })
            this.earnRiskLoading = false
          }
        } else {
          this.earnRiskLoading = false
          this.$message.error(res.data.message || '查询收益与风险指标对比失败')
        }
      })
    },
    //收益与风险指标对比 截止时间查询
    getEarnRiskDataDate() {
      console.log('进来了')
      return new Promise((resolve, reject) => {
        const params = {}
        params.indexCode = '3ddea7fa-fcc6-4808-b7af-c2278c1776d7'
        params.endDate = this.formQuery.endDate || ''
        params.productCodes = this.formQuery.productCodes || ''
        params.baseCode = this.formQuery.dbjz.length ? this.formQuery.dbjz.join(',') : ''
        commonAPI
          .getDataBysqlCode(params)
          .then((res) => {
            let { status, data } = res.data
            if (status == 0) {
              this.IndustryDataUpDate = data[0].d_maxdate
            } else {
              this.IndustryDataUpDate = ''
            }
          })
          .catch((err) => {})
      })
    },
    /**
     * @description 根据列最大最小值展示颜色
     */
    handleConstartIndex(filterTable, index) {

      const arr = filterTable.map(item => item[index]).filter((s) => {return s})
      let max = Math.max(...arr)
      let min = Math.min(...arr)
      if (max === min) {
        return
      }
      const indexList = ['YDATE2', 'YDATE3', 'YDATE7']
      for (let i in filterTable) {
        if (max === filterTable[i][index]) {
          this.tableData[i][`color${index}`] = indexList.indexOf(index) !== -1 ? 'min' : 'max'
        }
        if (min === filterTable[i][index]) {
          this.tableData[i][`color${index}`] = indexList.indexOf(index) !== -1 ? 'max' : 'min'
        }
      }
    },
    /**
     * @description 表格列对比
     */
    setCellStyle({ row, rowIndex, $rowIndex, column, columnIndex, $columnIndex }) {
      for (let i = 0; i < this.constartIndexArr.length; i++) {
        const item = this.constartIndexArr[i]
        if (column.property === item) {
          if (row[`color${item}`] === 'max') {
            return {
              background: '#cc6666',
              color: '#fff'
            }
          } else if (row[`color${item}`] === 'min') {
            return {
              background: '#8db97b',
              color: '#fff'
            }
          }
        }
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.riskCompare {
  padding: 0 30px;

  .title {
    padding: 10px 0;
    border-bottom: 1px solid #A15008;

    .title-icon {
      vertical-align: middle;
      display: inline-block;
    }

    .color-box {
      display: inline-block;
      height: 12px;
      width: 4px;
      background-image: linear-gradient(-45deg,#e19c5d,#f4cea9);
      position: relative;
      top: 2px;
      margin-left: 5px;
    }

    .title-txt {
      color: #333333;
      vertical-align: middle;
      height: 35px;
      line-height: 35px;
      font-size: 16px;
      margin-left: 5px;
      display: inline-block;
    }

    .tip:hover {
      cursor: pointer;
    }
  }

  .risk-compare-content {
    padding: 20px;

    .tips {
      margin: 5px 0;
      font-size: 14px;
    }
  }

  .chart-content {
    height: 450px;
    margin-top: 5px;

    .echarts_box {
      height: 100%;
      width: 100%;
    }
  }
}
</style>

<template>
  <div class="markowiz-model">
    <el-row>
      <el-col :span="12">
        <div style="margin-top: 10px; margin-left: 10px">
          <!--          <el-form :inline="true" :model="formInline">-->
          <!--            <el-button-->
          <!--              type="primary"-->
          <!--              style="margin-right: 10px"-->
          <!--              @click="downloadTemplate"-->
          <!--            >下载模版-->
          <!--            </el-button-->
          <!--            >-->
          <!--            <el-form-item label="导入文件">-->
          <!--              <el-input-->
          <!--                v-model="formInline.fileName"-->
          <!--                placeholder="请导入文件"-->
          <!--              />-->
          <!--            </el-form-item>-->
          <!--            <el-form-item>-->
          <!--              <el-upload-->
          <!--                :action="fileUrl"-->
          <!--                ref="upload"-->
          <!--                :headers="headersParams"-->
          <!--                :before-upload="beforeUpload"-->
          <!--                :data="dataParams"-->
          <!--                :on-success="handleSuccess"-->
          <!--                :on-error="handleError"-->
          <!--                :on-change="onChange"-->
          <!--                :on-exceed="onExcedd"-->
          <!--                :on-remove="onRemove"-->
          <!--                :auto-upload="true"-->
          <!--                :limit="1"-->
          <!--                :show-file-list="false"-->
          <!--                :file-list="fileList"-->
          <!--                class="upload-demo"-->
          <!--                name="multipartfile"-->
          <!--                multiple-->
          <!--              >-->
          <!--                <el-button-->
          <!--                  size="small"-->
          <!--                  type="primary"-->
          <!--                  icon="el-icon-folder-opened"-->
          <!--                >选择文件-->
          <!--                </el-button>-->
          <!--              </el-upload>-->
          <!--            </el-form-item>-->
          <!--            <el-form-item label="">-->
          <!--              <el-select v-model="formInline.frequent" placeholder="请选择">-->
          <!--                <el-option-->
          <!--                  v-for="item in frequentOption"-->
          <!--                  :key="item.value"-->
          <!--                  :label="item.label"-->
          <!--                  :value="item.value"-->
          <!--                />-->
          <!--              </el-select>-->
          <!--            </el-form-item>-->
          <!--          </el-form>-->
          <div class="titleFontStyle" id="standard-table">
            <span class="blueLine">|</span>
            <span>无风险收益率</span>
            <vxe-table
              :data="riskRateTableData"
              :edit-config="{ trigger: 'click', mode: 'cell' }"
              :cell-style="riskRateStyle"
              style="margin-top: 10px"
              border
              resizable
              show-overflow
            >
              <vxe-column field="name" title="名称" align="center" header-align="center">
                <template slot-scope="scope">
                  <span>{{ scope.row.name | noDataFilter }}</span>
                </template>
              </vxe-column>
              <vxe-table-column :edit-render="{ name: 'input', attrs: { type: 'Number' } }" field="riskFree" title="值(%)" header-align="center" align="right" />
            </vxe-table>
          </div>
          <div class="titleFontStyle" id="standard-table">
            <span class="blueLine">|</span>
            <span>配置比例</span>
            <vxe-table
              :data="allRatioTableData"
              :edit-config="{ trigger: 'click', mode: 'cell' }"
              :cell-style="allRatioStyle"
              style="margin-top: 10px"
              border
              resizable
              show-overflow
            >
              <vxe-column field="typeName" title="产品名称" align="center" header-align="center">
                <template slot-scope="scope">
                  <span>{{ scope.row.typeName | noDataFilter }}</span>
                </template>
              </vxe-column>
              <vxe-table-column :edit-render="{ name: 'input', attrs: { type: 'Number' } }" field="lowerRate" title="配置下限(%)" header-align="center" align="right" />
              <vxe-table-column :edit-render="{ name: 'input', attrs: { type: 'Number' } }" field="upperRate" title="配置上限(%)" header-align="center" align="right" />
            </vxe-table>
          </div>
          <!-- 参数部分 -->
          <div class="divArea">
            <div class="lineArea" />
            <a rel="mean_params" class="showArea">
              <i v-if="isShowIcon" class="el-icon-arrow-up" @click="isShowIcon = !isShowIcon" />
              <i v-if="!isShowIcon" class="el-icon-arrow-down" @click="isShowIcon = !isShowIcon" />
            </a>
          </div>
          <div v-show="isShowIcon">
            <div class="titleFontStyle" id="standard-table">
              <span class="blueLine">|</span>
              <span>预期目标</span>
              <vxe-table
                :data="expectTableData"
                :edit-config="{ trigger: 'click', mode: 'cell' }"
                :cell-style="expectStyle"
                style="margin-top: 10px"
                border
                resizable
                show-overflow
              >
                <vxe-table-column
                  :edit-render="{ name: 'input', attrs: { type: 'Number' } }"
                  field="combinedExpectedReturnLow"
                  title="期望收益下限(%)"
                  header-align="center"
                  align="right"
                />
                <vxe-table-column
                  :edit-render="{ name: 'input', attrs: { type: 'Number' } }"
                  field="combinedExpectedReturnUpper"
                  title="期望收益上限(%)"
                  header-align="center"
                  align="right"
                />
                <vxe-table-column :edit-render="{ name: 'input', attrs: { type: 'Number' } }" field="outCount" title="期望输出组数" header-align="center" align="right" />
              </vxe-table>
            </div>
            <div class="titleFontStyle" id="standard-table">
              <span class="blueLine">|</span>
              <span>收益及风险列表</span>
              <vxe-grid
                :data="benefitsRiskTableData"
                :edit-config="{ trigger: 'click', mode: 'cell' }"
                :columns="benefitsRiskColumn"
                :cell-style="benefitsRiskStyle"
                style="margin-top: 10px"
                border
                resizable
                show-header-overflow
                show-overflow
              />
            </div>
            <div class="titleFontStyle" id="standard-table">
              <span class="blueLine">|</span>
              <span>相关系数</span>
              <vxe-grid
                :data="coefficientTable"
                :edit-config="{ trigger: 'click', mode: 'cell' }"
                :columns="coefficientColumn"
                style="margin-top: 10px"
                border
                resizable
                show-header-overflow
                show-overflow
              />
            </div>
            <el-row type="flex" justify="center" class="mt10 standard-form">
              <el-button type="primary" size="small" @click="runMarkwitz" :disabled="buttonStatus">运行</el-button>
            </el-row>
          </div>
        </div>
      </el-col>
      <el-col :span="12" id="markowiz-right">
        <el-row>
          <el-col :offset="22" :span="2">
            <div style="font-size: 20px">
              <i :class="{ 'table-activate': tableActivate }" class="el-icon-s-grid" @click="tableActivate = !tableActivate" />
              <i :class="{ 'chart-activate': !tableActivate }" class="el-icon-pie-chart" @click="tableActivate = !tableActivate" />
            </div>
          </el-col>
          <el-col style="padding: 10px">
            <div v-show="tableActivate">
              <div style="position: relative; height: 25px" class="standard-form">
                <div style="position: absolute; top: 5px; z-index: 1">
                  <span class="dd-table-title">均值方差模型</span>
                </div>
                <el-button type="primary" size="small" style="position: absolute; top: 5px; right: 40px" @click="handleExport">导出</el-button>
              </div>
              <div id="standard-table">
                <vxe-grid
                  style="margin-top: 15px"
                  ref="xGrid"
                  key="table"
                  highlight-current-row
                  @radio-change="handleCurrentChange"
                  :custom-config="tableCustom"
                  :data="tableData"
                  :columns="tableColumn"
                  border
                  resizable
                  keep-source
                  :max-height="tableHeight"
                  show-overflow
                  show-header-overflow
                >
                  <vxe-column type="radio" width="50"></vxe-column>
                  <vxe-column v-for="(item, index) in tableColumn" :key="index" :field="item.field" align="center" :formatter="item.formatter" :label="item.title"></vxe-column>
                </vxe-grid>
              </div>
            </div>
            <div v-show="!tableActivate">
              <!--              <div id="lineChart" style="width: 100%;height: 250px"></div>-->
              <echarts v-show="calResult" id="lineChart" style="width: 100%; height: 250px" :options="lineChartOption" ref="lineChart" resize-dom="choose"></echarts>
              <echarts v-show="calResult" id="pieChart" style="width: 100%; height: 150px" :options="pieChartOption" ref="pieChart" resize-dom="choose"></echarts>
              <div>
                <span class="dd-table-title">优化比例</span>
              </div>
              <div id="standard-table">
                <vxe-grid ref="xGrid2" :data="tableData2" :columns="tableColumn2" border resizable min-height="500" show-overflow show-header-overflow></vxe-grid>
              </div>
              <div>
                <span class="dd-table-title">组合情况</span>
              </div>
              <div id="standard-table">
                <vxe-grid ref="xGrid3" :data="tableData3" :columns="tableColumn3" border resizable min-height="500" show-overflow show-header-overflow />
              </div>
              <el-row type="flex" justify="center" class="standard-form">
                <el-button type="primary" size="small" @click="handleSubmitClick" style="margin-top: 10px">应 用</el-button>
              </el-row>
            </div>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
    <el-dialog title="基金优化当前可选日期列表" :visible.sync="dialogTableVisible">
      <div id="standard-table">
        <el-table :data="gridData" max-height="500px">
          <el-table-column type="index" width="50"></el-table-column>
          <el-table-column property="vcFundcode" label="产品代码"></el-table-column>
          <el-table-column property="vcFundname" label="产品名称"></el-table-column>
          <el-table-column property="beginDate" label="开始时间"></el-table-column>
          <el-table-column property="endDate" label="结束时间"></el-table-column>
        </el-table>
        <span style="color: red">注:开始与结束时间输入范围，应取当前可选日期列表交集</span>
        <span style="color: red">如发现产品日期净值缺失，请及时与运维人员联系！</span>
      </div>
    </el-dialog>

    <vue-element-loading :active="vueLoading" :text="vueLoadingText" spinner="spinner" color="#FF6700" />
  </div>
</template>
<script>
import { getToken } from '@/utils/auth'
import { FILE_URL, getSeq } from '@/utils/request'
import pageApi from '@/api/setting/markowitzModel'
import Echarts from '@/components/Echarts'
import _ from 'lodash'
import VueElementLoading from 'vue-element-loading'
import FileSaver from 'file-saver'
import XLSX from 'xlsx'

export default {
  components: {
    Echarts,
    VueElementLoading
  },
  data() {
    return {
      tableHeight: 0,
      createSimuCombParams: null,
      buttonStatus: true,
      dialogTableVisible: false,
      gridData: [],
      vueLoadingText: '',
      vueLoading: false,
      tableActivate: true,
      isShowIcon: true,
      file: {},
      fileList: [],
      formFiles: [],
      fileUrl: '',
      // 上传头部
      headersParams: {
        Authorization: getToken(),
        Seq: getSeq()
      },
      dataParams: {
        fileName: 'template.xlsx',
        frequent: 'day',
        version: '1.3'
      },
      formInline: {
        fileName: '',
        frequent: 'day',
        version: '1.3.0'
      },
      frequentOption: [
        {
          value: 'day',
          label: '日频'
        },
        {
          value: 'month',
          label: '月频'
        },
        {
          value: 'quarter',
          label: '季频'
        },
        {
          value: 'year',
          label: '年频'
        }
      ],
      riskRateTableData: [
        {
          name: '无风险收益率(%)',
          riskFree: 1.2
        }
      ], // 无风险收益率表格
      allRatioTableData: [], // 配置比例表格
      expectTableData: [], // 预期目标
      benefitsRiskTableData: [], // 收益及风险列表 表格数据
      benefitsRiskColumn: [],
      coefficientColumn: [], // 相关系数的表头
      fundReslut: [], //
      expectedRevenueT: [], // 期望收益数组
      coefficientTable: [], // 相关系数
      lowRatio: 0,
      highRatio: 0,
      fundCodes: [],
      tableColumn: [
        {
          type: 'radio',
          width: '50px',
          align: 'center'
        },
        {
          field: 'portReturn',
          title: '回报率',
          minWidth: '80px',
          sortable: false,
          align: 'center',
          formatter: function ({ row, column, cellValue, index }) {
            if (!cellValue) return '0%'
            cellValue = parseFloat(cellValue * 100).toFixed(2) + '%'
            return cellValue
          }
        },
        {
          field: 'portRisk',
          title: '波动率',
          minWidth: '60px',
          sortable: false,
          align: 'center',
          formatter: function ({ row, column, cellValue, index }) {
            if (!cellValue) return '0%'
            cellValue = parseFloat(cellValue * 100).toFixed(2) + '%'
            return cellValue
          }
        },
        {
          field: 'markPoint',
          title: 'sharpe',
          minWidth: '60px',
          sortable: false,
          align: 'center',
          formatter: function ({ row, column, cellValue, index }) {
            if (!cellValue) return '0'
            cellValue = parseFloat(cellValue).toFixed(4) + ''
            return cellValue
          }
        },
        {
          field: 'calmar',
          title: 'calmar',
          minWidth: '60px',
          sortable: false,
          align: 'center',
          formatter: function ({ row, column, cellValue, index }) {
            if (!cellValue) return '0'
            cellValue = parseFloat(cellValue).toFixed(4) + ''
            return cellValue
          }
        },
        {
          field: 'maxdrown',
          title: '最大回撤',
          minWidth: '60px',
          sortable: false,
          align: 'center',
          formatter: function ({ row, column, cellValue, index }) {
            if (!cellValue) return '0'
            cellValue = parseFloat(cellValue).toFixed(2) + '%'
            return cellValue
          }
        }
      ],
      saveTableColumn: [
        {
          type: 'radio',
          width: '50px',
          align: 'center'
        },
        {
          field: 'portReturn',
          title: '回报率',
          minWidth: '80px',
          sortable: false,
          align: 'center',
          formatter: function ({ row, column, cellValue, index }) {
            if (!cellValue) return '0%'
            cellValue = parseFloat(cellValue * 100).toFixed(2) + '%'
            return cellValue
          }
        },
        {
          field: 'portRisk',
          title: '波动率',
          minWidth: '60px',
          sortable: false,
          align: 'center',
          formatter: function ({ row, column, cellValue, index }) {
            if (!cellValue) return '0%'
            cellValue = parseFloat(cellValue * 100).toFixed(2) + '%'
            return cellValue
          }
        },
        {
          field: 'markPoint',
          title: 'sharpe',
          minWidth: '60px',
          sortable: false,
          align: 'center',
          formatter: function ({ row, column, cellValue, index }) {
            if (!cellValue) return '0'
            cellValue = parseFloat(cellValue).toFixed(4) + ''
            return cellValue
          }
        },
        {
          field: 'calmar',
          title: 'calmar',
          minWidth: '60px',
          sortable: false,
          align: 'center',
          formatter: function ({ row, column, cellValue, index }) {
            if (!cellValue) return '0'
            cellValue = parseFloat(cellValue).toFixed(4) + ''
            return cellValue
          }
        },
        {
          field: 'maxdrown',
          title: '最大回撤',
          minWidth: '60px',
          sortable: false,
          align: 'center',
          formatter: function ({ row, column, cellValue, index }) {
            if (!cellValue) return '0'
            cellValue = parseFloat(cellValue).toFixed(2) + '%'
            return cellValue
          }
        }
      ],
      tableColumn2: [],
      tableColumn3: [
        {
          field: 'portReturn',
          // title: '计划预期收益(%)',
          title: '预期收益(%)',
          minWidth: '60px',
          sortable: false,
          align: 'center',
          formatter: function ({ cellValue }) {
            if (!cellValue) return '0%'
            cellValue = parseFloat(cellValue).toFixed(2) + '%'
            return cellValue
          }
        },
        {
          field: 'portRisk',
          // title: '计划预期风险(%)',
          title: '预期风险(%)',
          minWidth: '60px',
          sortable: false,
          align: 'center',
          formatter: function ({ cellValue }) {
            if (!cellValue) return '0%'
            cellValue = parseFloat(cellValue).toFixed(2) + '%'
            return cellValue
          }
        },
        {
          field: 'markPoint',
          title: 'sharpe',
          minWidth: '60px',
          sortable: false,
          align: 'center',
          formatter: function ({ cellValue }) {
            if (!cellValue) return '0'
            cellValue = parseFloat(cellValue).toFixed(4) + ''
            return cellValue
          }
        },
        {
          field: 'calmar',
          title: 'calmar',
          minWidth: '60px',
          sortable: false,
          align: 'center',
          formatter: function ({ cellValue }) {
            if (!cellValue) return '0'
            cellValue = parseFloat(cellValue).toFixed(4) + ''
            return cellValue
          }
        },
        {
          field: 'maxdrown',
          title: '最大回撤(%)',
          minWidth: '60px',
          sortable: false,
          align: 'center',
          formatter: function ({ cellValue }) {
            if (!cellValue) return '0'
            cellValue = parseFloat(cellValue).toFixed(2) + '%'
            return cellValue
          }
        }
      ],
      tableData: [],
      tableData2: [],
      tableData3: [],
      calResult: null,
      lineChart: '',
      tableToolbar: {
        custom: true,
        slots: {
          buttons: 'toolbar_buttons',
          tools: 'toolbar_tools'
        }
      },
      tableCustom: {
        storage: false
      },
      handleFresh: null,
      lineChartOption: {},
      pieChartOption: {},
      currentIndex: 0
    }
  },
  watch: {
    tableActivate: {
      handler() {
        if (this.tableActivate == false) {
          this.$nextTick(() => {
            if (this.calResult == null) {
              this.$refs.xGrid2.recalculate(true)
              this.$refs.xGrid3.recalculate(true)
              this.$refs.xGrid.doLayout()
              return
            }
            this.drawLine(this.calResult)
            this.drawPie(this.calResult)
            this.handleTablaData(this.calResult)
            this.$refs.xGrid2.recalculate(true)
            this.$refs.xGrid3.recalculate(true)
            this.$refs.xGrid.doLayout()
          })
        } else {
          // this.$refs.xGrid.recalculate(true)
          this.$refs.xGrid2.recalculate(true)
          this.$refs.xGrid3.recalculate(true)
          this.$refs.xGrid.doLayout()
        }
      }
    }
  },
  created() {},
  mounted() {
    this.$nextTick(() => {
      // this.$refs.xGrid.connect(this.$refs.xToolbar)
    })
    this.handleFresh = _.debounce(() => {
      this.drawPie(this.calResult)
      this.handleTablaData(this.calResult)
    }, 150)
    // 文件上传地址
    this.fileUrl = FILE_URL + '/api/assetAllocation/parseExcel.do'
  },
  methods: {
    // circle 点击应用
    handleSubmitClick() {
      if (this.tableData2.length > 0) {
        this.$emit('weightarray', this.tableData2)
      }
    },
    handleCurrentChange({ row }) {
      console.log(row)
      this.$emit('selectrow', row)
    },
    getRndInteger(min, max) {
      return Math.floor(Math.random() * (max - min + 1)) + min
    },
    exportExcel() {
      /* generate workbook object from table */
      let wb = XLSX.utils.table_to_book(document.getElementById('toolbar_demo_2'))
      /* get binary string as output */
      let wbout = XLSX.write(wb, { bookType: 'xlsx', bookSST: true, type: 'array' })
      try {
        FileSaver.saveAs(new Blob([wbout], { type: 'application/octet-stream' }), '马克维茨模型.xlsx')
      } catch (e) {
        if (typeof console !== 'undefined') {
          console.log(e, wbout)
        }
      }
      return wbout
    },
    handleExport() {
      if (this.tableData.length <= 0) {
        this.$message.closeAll()
        this.$message.warning('表格为空导出失败')
        return
      }
      const $grid = this.$refs.xGrid

      // $grid.exportData({
      //   filename: '马克维茨模型',
      //   type:'xlsx',
      //   useStyle:true, //是否导出样式
      //   data:$grid.data
      // })
      // this.exportExcel()
      this.$refs.xGrid.exportData()
    },

    // 绘制折线图
    drawLine(data) {
      if (!data || !data.calmar || data.calmar.length == 0) {
        return
      }
      let myoption = {}
      var sdata = []
      // x轴对象
      var xdata = []
      const xdataMax = (this.ratioManager(data.portRisk[data.portRisk.length - 1], '+') * 100).toFixed(2)
      const ydataMax = (this.ratioManager(data.portReturn[data.portReturn.length - 1], '+') * 100).toFixed(2)
      let sharpMaxIndex = 0
      let tempIndex = data.markPoint[0]
      for (let i = 0; i < data.markPoint.length; i++) {
        if (tempIndex < data.markPoint[i]) {
          tempIndex = data.markPoint[i]
          sharpMaxIndex = i
        }
      }
      let sharp = (data.portReturn[sharpMaxIndex] * 100).toFixed(2)
      myoption = {
        // 坐标轴显示
        tooltip: {
          // trigger : 'item',
          trigger: 'axis',
          formatter: (params, ticket, callback) => {
            var dataIndex = params[0].dataIndex
            this.currentIndex = dataIndex
            this.handleFresh()
            var html =
              '回报率：' +
              ((this.calResult.portReturn[dataIndex] * 100).toFixed(2) || '') +
              '%<br/>' +
              '波动率：' +
              ((this.calResult.portRisk[dataIndex] * 100).toFixed(2) || '') +
              '%'
            // 处理其他表格的逻辑

            return html
          }
        },
        xAxis: [
          {
            name: '波动率%',
            type: 'value',
            min: 0,
            max: xdataMax,
            data: data.portRisk,
            axisLabel: {
              formatter: function (value, row, index) {
                if (!value) {
                  return '0%'
                }
                value = parseFloat(value).toFixed(2)
                return value
              }
            }
          }
        ],
        yAxis: {
          name: '回报率%',
          type: 'value',
          min: 0,
          max: ydataMax,
          axisLabel: {
            formatter: function (value, row, index) {
              if (!value) {
                return '0%'
              }
              value = parseFloat(value).toFixed(2)
              return value
            }
          }
        },
        series: [
          {
            smooth: true, // 光滑曲线
            symbolSize: 1,
            name: '回报率/波动率',
            type: 'line',
            showSymbol: false,
            data: data.portReturn,
            markPoint: {
              // 显示为圆点
              symbol: 'circle',
              itemStyle: {
                normal: {
                  color: 'red'
                }
              },
              data: [
                {
                  name: 'sharp',
                  label: {
                    normal: {
                      show: false
                    }
                  },
                  symbolSize: 10,
                  xAxis: 0,
                  yAxis: 0
                }
              ]
            }
          }
        ]
      }
      for (let i = 0; i < data.portRisk.length; ++i) {
        xdata.push(parseFloat((data.portRisk[i] * 100).toFixed(4)))
        sdata.push([parseFloat((data.portRisk[i] * 100).toFixed(2)), parseFloat((data.portReturn[i] * 100).toFixed(2))])
        // sdata.push(allData[i]["portReturn"].toFixed(2));
      }
      myoption.xAxis[0].data = xdata
      myoption.series[0].data = sdata
      myoption.series[0].markPoint.data[0].xAxis = (data.portRisk[sharpMaxIndex] * 100).toFixed(2)
      myoption.series[0].markPoint.data[0].yAxis = sharp

      this.lineChartOption = myoption
      // if (this.lineChart) {//   this.lineChart.dispose()
      // }
      // this.lineChart = echarts.init(document.getElementById('lineChart'))
      // this.lineChart.setOption(option, true)
    },
    drawPie(data) {
      this.pieChartOption = {
        tooltip: {
          trigger: 'item',
          formatter: '{b} ({d}%)',
          axisPointer: {
            type: 'none',
            lineStyle: {
              width: 0
            }
          }
        },
        toolbox: {
          show: false
        },
        calculable: false,
        legend: {
          type: 'scroll',
          show: true,
          x: 'center',
          y: 'bottom',
          data: null
        },
        series: [
          {
            name: '占比',
            type: 'pie',
            radius: '55%',
            itemStyle: {
              normal: {
                label: {
                  show: false
                  // 不显示饼图上的名称
                },
                labelLine: {
                  show: false
                  // 不显示饼图的连接线
                }
              }
            },
            data: null
          }
        ]
      }
      let seriesData = []
      let legendData = []
      this.fundCodes.forEach((item) => {
        let obj = {
          name: item,
          value: this.tableData[this.currentIndex][item]
        }
        seriesData.push(obj)
        legendData.push(item)
      })
      this.pieChartOption.series[0].data = seriesData
      this.pieChartOption.legend.data = legendData
    },
    handleTablaData(data) {
      this.tableColumn2 = [
        {
          field: 'typeNum',
          title: '产品名称',
          minWidth: '60px',
          sortable: false,
          align: 'center'
        }
      ]
      this.tableData2 = []
      this.tableData3 = []
      this.fundCodes.forEach((item) => {
        this.tableColumn2.push({
          field: item,
          title: item,
          minWidth: '60px',
          sortable: false,
          align: 'center',
          formatter: function ({ cellValue }) {
            if (!cellValue) return '0%'
            cellValue = parseFloat(cellValue * 100).toFixed(2)
            return cellValue
          }
        })
      })
      let obj = { typeNum: '优化比例(%)' }
      this.fundCodes.forEach((item) => {
        obj[item] = this.tableData[this.currentIndex][item]
      })
      this.tableData2.push(obj)
      this.tableData3.push({
        portReturn: parseFloat(this.tableData[this.currentIndex].portReturn * 100).toFixed(2),
        portRisk: parseFloat(this.tableData[this.currentIndex].portRisk * 100).toFixed(2),
        markPoint: this.tableData[this.currentIndex].markPoint,
        calmar: this.tableData[this.currentIndex].calmar,
        maxdrown: this.tableData[this.currentIndex].maxdrown
      })
    },
    runMarkwitz() {
      let flag = true
      const numberValidation = '^100$|^(\\d|[1-9]\\d)(\\.\\d{1,2})*$'
      // const integerValidation = '^(?:\\d{1,3}|1000)$'
      const integerValidation = '^(?:[2-9]|[1-9]\\d|1\\d{2}|200)$'
      let result = true
      let riskFree = '' // 无风险收益
      const risks = [] // 风险
      const expectedRevenues = [] // 收益
      let fundCodes = [] // 基金数组
      const correlationCoefficient = [] // 相关系数
      let outCount = 0 // 输出组数
      const ratioConfigrution = [] // 配置比例
      const combinedExpectedReturn = [] // 组合预期收益
      const subcode = '702A' // 科目编码
      const fileName = this.formInline.fileName // 文件名
      const version = this.formInline.version // 版本好
      const frequent = this.formInline.frequent // 频率
      riskFree = this.riskRateTableData[0].riskFree

      // 验证无风险收益
      result = this.numberValidations(riskFree, numberValidation)
      if (result === false) {
        flag = false
        this.$message.closeAll()
        this.$message.error('请检查无风险收益的数字格式,必须是0-100之间的数')
        return
      } else {
        riskFree = riskFree / 100
      }

      // 验证配置比例
      this.allRatioTableData.forEach((item) => {
        const tempArray = []
        result = this.numberValidations(item.lowerRate, numberValidation)
        if (result === false) {
          flag = false
          this.$message.closeAll()
          this.$message.error('请检查配置比例的数字格式,必须是0-100之间的数')
          return
        } else {
          tempArray[0] = parseFloat(item.lowerRate) / 100
        }
        result = this.numberValidations(item.upperRate, numberValidation)
        if (result === false) {
          flag = false
          this.$message.closeAll()
          this.$message.error('请检查配置比例的数字格式,必须是0-100之间的数')
          return
        } else {
          tempArray[1] = parseFloat(item.upperRate) / 100
        }
        ratioConfigrution.push(tempArray)
      })

      // 验证预期目标
      this.expectTableData.forEach((item) => {
        result = this.numberValidations(item.combinedExpectedReturnLow, numberValidation)
        if (result === false) {
          flag = false
          this.$message.closeAll()
          this.$message.error('请检查预期目标的数字格式,必须是0-100之间的数')
          return
        } else {
          combinedExpectedReturn[0] = item.combinedExpectedReturnLow / 100
        }
        result = this.numberValidations(item.combinedExpectedReturnUpper, numberValidation)
        if (result === false) {
          flag = false
          this.$message.closeAll()
          this.$message.error('请检查预期目标的数字格式,必须是0-100之间的数')
          return
        } else {
          combinedExpectedReturn[1] = item.combinedExpectedReturnUpper / 100
        }
        result = this.numberValidations(item.outCount, integerValidation)
        if (result === false) {
          flag = false
          this.$message.closeAll()
          this.$message.error('期望输出组数必须在2~200之间')
          return
        } else {
          outCount = item.outCount
        }
      })
      // 判断预期目标是否符合要求
      if (Number(combinedExpectedReturn[0]) > Number(combinedExpectedReturn[1])) {
        flag = false
        this.$message.closeAll()
        this.$message.error('期望计划收益下限不能高于期望组合收益上限')
        return
      }
      if (Number(combinedExpectedReturn[0]) + 0.005 > Number(combinedExpectedReturn[1])) {
        flag = false
        this.$message.closeAll()
        this.$message.error('期望计划收益下限与期望组合收益上限差值必须大于0.5%!')
        return
      }

      this.expectedRevenueT = []
      if (this.benefitsRiskTableData.length > 0) {
        for (let key in this.benefitsRiskTableData[0]) {
          if (key !== '_XID' && key !== 'typeName') {
            this.expectedRevenueT.push(Number(this.benefitsRiskTableData[0][key]))
          }
        }
      }
      this.lowRatio = _.min(this.expectedRevenueT)
      this.highRatio = _.max(this.expectedRevenueT)
      if (Number(combinedExpectedReturn[0]) * 100 < this.lowRatio) {
        flag = false
        this.$message.closeAll()
        this.$message.error('期望计划收益下限不能低于预期收益的最小值')
        return
      }

      if (Number(combinedExpectedReturn[1]) * 100 > this.highRatio) {
        flag = false
        this.$message.closeAll()
        this.$message.error('期望计划收益上限不能高于预期收益的最大值')
        return
      }

      this.benefitsRiskTableData.forEach((item) => {
        // console.log(item)
        if (item.typeName == '预期收益') {
          for (const key in item) {
            if (key != 'typeName' && key != '_XID') {
              if (item[key] < 0) {
                flag = false
                this.$message.closeAll()
                this.$message.error('收益及风险列表数值比例不能小于0')
                return
              } else {
                expectedRevenues.push(parseFloat(item[key]) / 100)
              }
            }
          }
        } else {
          for (const key in item) {
            // console.log(key)
            if (key != 'typeName' && key != '_XID') {
              if (item[key] < 0) {
                flag = false
                this.$message.closeAll()
                this.$message.error('收益及风险列表数值比例不能小于0')
                return
              } else {
                risks.push(parseFloat(item[key]) / 100)
              }
            }
          }
        }
      })
      this.coefficientTable.forEach((item) => {
        const tempArr = []
        for (const key in item) {
          if (key != 'typeName' && key != '_XID') {
            tempArr.push(item[key])
          }
        }
        correlationCoefficient.push(tempArr)
      })
      for (let i = 0; i < correlationCoefficient.length; i++) {
        correlationCoefficient[i] = correlationCoefficient[i].toString()
      }
      for (let i = 0; i < ratioConfigrution.length; i++) {
        ratioConfigrution[i] = ratioConfigrution[i].toString()
      }
      fundCodes = this.fundCodes

      if (flag === false) return
      // 发送请求
      const params = {}
      params.riskFree = riskFree
      params.risks = risks
      params.expectedRevenues = expectedRevenues
      // params.fundCodes = fundCodes
      params.fundCodes = this.createSimuCombParams.fundCodes.split(',')
      params.correlationCoefficient = correlationCoefficient
      params.outCount = outCount
      params.ratioConfigrution = ratioConfigrution
      params.combinedExpectedReturn = combinedExpectedReturn
      params.fileName = fileName
      params.frequent = this.createSimuCombParams.frequent
      params.beginDate = this.createSimuCombParams.beginDate
      params.endDate = this.createSimuCombParams.endDate
      params.vcParentCode = this.createSimuCombParams.vcParentCode
      params.riskFree = riskFree
      params.vcPin = 1
      params.version = '1.3.0'
      params.subcode = '702A'
      params.fundNames = ''
      params.peopleSet = ''
      this.vueLoadingText = '模型计算中'
      this.vueLoading = true
      pageApi
        .runMean(params)
        .then((res) => {
          if (res.data.result.resultCode == 1) {
            let dom = document.getElementsByClassName('markowiz-model')
            if (dom && dom[0]) {
              if (dom[0].clientHeight < 120) {
                this.tableHeight = 10
              } else {
                this.tableHeight = dom[0].clientHeight - 120
              }
            }
            this.calResult = res.data.markwitzResult
            this.handleRunMeanResult(res.data.markwitzResult)
            this.drawLine(this.calResult)
            this.drawPie(this.calResult)
          } else {
            this.$message.closeAll()
            this.$message.error(res.data.result.message)
          }
          this.vueLoading = false
        })
        .catch(() => {
          this.vueLoading = false
        })
    },

    handleRunMeanResult(data) {
      this.tableData = []
      const tempColumns = _.cloneDeep(this.saveTableColumn)
      this.fundCodes.forEach((item) => {
        tempColumns.push({
          field: item,
          title: item,
          minWidth: '60px',
          sortable: false,
          align: 'center',
          formatter: function ({ row, column, cellValue, index }) {
            if (!cellValue) return '0%'
            cellValue = parseFloat(cellValue * 100).toFixed(2) + '%'
            return cellValue
          }
        })
      })
      this.tableColumn = tempColumns
      for (let i = 0; i < data.calmar.length; i++) {
        this.tableData.push({
          portReturn: data.portReturn[i],
          portRisk: data.portRisk[i],
          markPoint: data.markPoint[i],
          calmar: data.calmar[i],
          maxdrown: data.maxdrown[i]
        })
      }
      for (let i = 0; i < data.calmar.length; i++) {
        for (let j = 0; j < this.fundCodes.length; j++) {
          this.tableData[i][this.fundCodes[j]] = data.portWts[i][j]
        }
      }
    },
    // 判断数字格式是否合法
    numberValidations(value, numTest) {
      if (isNaN(value)) {
        return false
      }
      value = parseFloat(value)
      numTest = new RegExp(numTest)
      if (!numTest.test(value)) {
        return false
      }
      return true
    },
    riskRateStyle({ row, column, rowIndex, columnIndex }) {
      if (columnIndex >= 1) {
        if (row.riskFree === null || row.riskFree === undefined || row.riskFree === '') {
          return {
            backgroundColor: 'rgb(255, 117, 117)'
          }
        }
        if (row.riskFree < 0 || row.riskFree > 100) {
          return {
            backgroundColor: 'rgb(255, 117, 117)'
          }
        }
      }
    },
    benefitsRiskStyle({ row, column, rowIndex, columnIndex }) {
      if (columnIndex >= 1) {
        if (row[column.property] == null || row[column.property] == undefined || row[column.property] < 0) {
          return {
            backgroundColor: 'rgb(255, 117, 117)'
          }
        }
      }
    },
    allRatioStyle({ row, column, rowIndex, columnIndex }) {
      var numberValidation = '^100$|^(\\d|[1-9]\\d)(\\.\\d{1,2})*$'
      if (columnIndex >= 1) {
        if (columnIndex >= 1) {
          const res = this.numberValidations(row[column.property], numberValidation)
          if (res === false) {
            return {
              backgroundColor: 'rgb(255, 117, 117)'
            }
          }
        }
      }
    },
    expectStyle({ row, column, rowIndex, columnIndex }) {
      if (columnIndex === 2) {
        // var integerValidation = '^(?:\\d{1,3}|1000)$'
        var integerValidation = '^(?:[2-9]|[1-9]\\d|1\\d{2}|200)$'
        const res = this.numberValidations(row[column.property], integerValidation)
        if (res === false) {
          return {
            backgroundColor: 'rgb(255, 117, 117)'
          }
        }
      } else {
        let tempArray = []
        if (this.benefitsRiskTableData.length > 0) {
          for (let key in this.benefitsRiskTableData[0]) {
            if (key !== '_XID' && key !== 'typeName') {
              tempArray.push(Number(this.benefitsRiskTableData[0][key]))
            }
          }
        }
        this.lowRatio = _.min(tempArray)
        this.highRatio = _.max(tempArray)
        if (columnIndex === 0) {
          if (parseFloat(row[column.property]) > parseFloat(this.highRatio)) {
            return {
              backgroundColor: 'rgb(255, 117, 117)'
            }
          } else if (parseFloat(row.combinedExpectedReturnLow) > parseFloat(row.combinedExpectedReturnUpper)) {
            return {
              backgroundColor: 'rgb(255, 117, 117)'
            }
          } else if (row.combinedExpectedReturnLow < this.lowRatio) {
            return {
              backgroundColor: 'rgb(255, 117, 117)'
            }
          }
        } else {
          if (parseFloat(row[column.property]) < parseFloat(this.lowRatio)) {
            return {
              backgroundColor: 'rgb(255, 117, 117)'
            }
          } else if (parseFloat(row.combinedExpectedReturnUpper) < parseFloat(row.combinedExpectedReturnLow)) {
            return {
              backgroundColor: 'rgb(255, 117, 117)'
            }
          } else if (row.combinedExpectedReturnUpper > this.highRatio) {
            return {
              backgroundColor: 'rgb(255, 117, 117)'
            }
          }
        }
      }
    },
    beforeUpload(file) {
      this.headersParams.Seq = getSeq()
      this.dataParams.fileName = file.name
      this.dataParams.frequent = this.formInline.frequent
      this.dataParams.version = this.formInline.version
      this.vueLoadingText = '上传文件中'
      this.vueLoading = true
    },
    getFile(item) {
      //  this.formFiles.append(item.file)
    },
    changeResult(data) {
      let params = { assetModelDto: [] }
      for (let i = 0; i < data.fundCodes.length; i++) {
        let obj = {
          assetRiskT: data.risks[i],
          correlationCoefficents: data.correlationCoefficient[i],
          expectedRevenueT: data.expectedRevenues[i],
          typeName: data.fundNames[i]
        }
        params.assetModelDto.push(obj)
      }
      return params
    },
    handleResult(data) {
      this.fundReslut = data

      // 补充上限，下限的值
      this.fundReslut.assetModelDto.forEach((item) => {
        if (item.lowerRate == null || item.lowerRate == undefined) {
          item.lowerRate = 0
        }
        if (item.upperRate == null || item.upperRate == undefined) {
          item.upperRate = 100
        }
      })
      this.handleAlloRatioData()
      this.handleBenifitsRiskData()
    },
    // 处理配置比例表格数据
    handleAlloRatioData() {
      this.allRatioTableData = []
      this.fundReslut.assetModelDto.forEach((item) => {
        this.allRatioTableData.push({
          typeName: item.typeName,
          lowerRate: item.lowerRate,
          upperRate: item.upperRate
        })
      })
    },
    // 处理收益及风险列表数据
    handleBenifitsRiskData() {
      this.benefitsRiskTableData = [{ typeName: '预期收益' }, { typeName: '预期风险' }]
      this.benefitsRiskColumn = [{ field: 'typeName', title: '', minWidth: '100px' }]
      this.coefficientColumn = [{ field: 'typeName', title: '相关系数', minWidth: '100px' }]
      this.expectedRevenueT = []
      this.coefficientTable = []
      this.expectTableData = []
      this.fundCodes = []
      this.fundReslut.assetModelDto.forEach((item) => {
        this.fundCodes.push(item.typeName)
        this.coefficientTable.push({ typeName: item.typeName })
        this.coefficientColumn.push({
          minWidth: '100px',
          field: item.typeName,
          title: item.typeName,
          editRender: { name: 'input', attrs: { type: 'Number' } }
        })
        this.benefitsRiskColumn.push({
          minWidth: '100px',
          field: item.typeName,
          title: item.typeName,
          editRender: { name: 'input', attrs: { type: 'Number' } }
        })
        this.benefitsRiskTableData[0][item.typeName] = Number(Number(item.expectedRevenueT * 100).toFixed(2))
        this.benefitsRiskTableData[1][item.typeName] = Number(Number(item.assetRiskT * 100).toFixed(2))
        this.expectedRevenueT.push(Number(Number(item.expectedRevenueT * 100).toFixed(2)))
      })
      this.coefficientTable.forEach((item) => {
        this.fundReslut.assetModelDto.forEach((litem) => {
          item[litem.typeName] = ''
        })
      })

      let i = 0
      this.fundReslut.assetModelDto.forEach((item) => {
        for (let j = 0; j < item.correlationCoefficents.length; j++) {
          this.coefficientTable[i][this.fundCodes[j]] = Number(Number(item.correlationCoefficents[j]).toFixed(4))
        }
        i++
      })
      this.lowRatio = _.min(this.expectedRevenueT)
      this.highRatio = _.max(this.expectedRevenueT)
      this.expectTableData.push({
        combinedExpectedReturnLow: this.lowRatio,
        combinedExpectedReturnUpper: this.highRatio,
        outCount: 50
      })
    },
    // 提交
    handleSuccess({ res, params }, file, fileList) {
      this.createSimuCombParams = params
      if (res.data.judgmentRepetition) {
        this.formInline.fileName = res.data.fileName
        this.$message.closeAll()
        this.$message.error(res.data.judgmentRepetition)
        this.vueLoading = false
        this.$refs.upload.clearFiles()
        this.fileList = []
        this.buttonStatus = true
        return
      }
      if (res.status == 200) {
        // this.$message.closeAll()
        // this.$message.success('上传文件成功')
        this.formInline.fileName = res.data.fileName
        if (res.data.fundAssetList !== undefined) {
          this.gridData = res.data.fundAssetList
          this.dialogTableVisible = true
          this.buttonStatus = true
        } else {
          this.buttonStatus = false
          this.handleResult(res.data.fundReslut)
        }
      } else {
        this.$message.closeAll()
        this.$message.error(res.data.result.message)
      }
      this.$refs.upload.clearFiles()
      this.fileList = []
      this.vueLoading = false
    },

    handleMarkowitzmodelSelect({ res, params }) {
      this.createSimuCombParams = params
      if (res && res.result && res.result.resultCode == '1') {
        this.$message.closeAll()
        this.$message.success(res.result.message || '成功')
        if (res.masterFundList) {
          this.gridData = res.masterFundList
          this.dialogTableVisible = true
          this.buttonStatus = true
        } else {
          this.buttonStatus = false
          this.handleResult(this.changeResult(res.fundAssetDetailDto))
        }
      } else {
        this.$message.closeAll()
        this.$message.warning(res.result.message)
      }
    },
    // 文件上传失败时的钩子
    handleError() {
      this.vueLoading = false
      this.$refs.upload.clearFiles()
      this.$message.error('文件上传失败')
    },
    // 文件改变
    onChange(file, fileList) {
      const existFile = fileList.slice(0, fileList.length - 1).find((f) => f.name === file.name)
      if (existFile) {
        this.$message.error('当前文件已经存在!')
        fileList.pop()
      }
    },
    // 文件个数超过
    onExcedd(files, fileList) {
      if (files) {
        this.$message.closeAll()
        this.$message.error('只能上传一个文件 ！')
        this.$refs.upload.clearFiles()
      }
    },
    // 移出文件
    onRemove(file, fileList) {
      this.fileList = []
      this.$refs.upload.clearFiles()
    },
    // 模板文件下载
    downloadTemplate() {
      // console.log(getToken())
      const params = {
        fileName: 'FundTempelete.xls',
        Authorization: getToken(),
        token: getToken()
      }
      // 参数、地址
      this.$fun.formDownloadFileMethod(params, pageApi.downloadTemplateUrl(), 'POST')
    },

    // 比例数据处理， num 要处理的数据 type 加或减
    ratioManager(num, type) {
      if (!type) {
        return
      }
      if (type == '+') {
        return num + num / 20
      } else {
        return num - num / 6
      }
    },
    // 判断当前值是否在当前数组中
    mContains(data) {
      var tempArr = ['portRisk', 'portReturn', 'markPoint', '0', 'calmar', 'maxdrown']
      for (var i = 0; i < tempArr.length; i++) {
        if (data == tempArr[i]) {
          return true
        }
      }
      return false
    }
  }
}
</script>
<style lang="scss">
.markowiz-model {
  .divArea {
    position: relative;
    margin: 14px 0;
  }
  .showArea {
    cursor: pointer;
    padding: 0 3px;
    border: 1px solid #eeeeee;
    position: absolute;
    top: -10px;
    left: 0px;
  }
  .lineArea {
    border-bottom: 1px green solid;
    margin: 3px 0px 3px 28px;
  }
  .table-activate {
    color: #13ce66;
  }
  .chart-activate {
    color: #13ce66;
  }
}
</style>

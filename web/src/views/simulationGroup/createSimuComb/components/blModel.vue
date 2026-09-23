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
          <div class="titleFontStyle">
            <span class="blueLine">|</span>
            <span>无风险收益率</span>
            <div id="standard-table">
              <vxe-table :data="riskRateTableData" :edit-config="{ trigger: 'click', mode: 'cell' }" border resizable show-overflow style="margin-top: 10px">
                <vxe-column align="center" field="name" header-align="center" title="名称">
                  <template slot-scope="scope">
                    <span>{{ scope.row.name | noDataFilter }}</span>
                  </template>
                </vxe-column>
                <vxe-table-column :edit-render="{ name: 'input', attrs: { type: 'Number' } }" align="right" field="riskFree" header-align="center" title="值(%)" />
              </vxe-table>
            </div>
          </div>
          <div class="titleFontStyle">
            <span class="blueLine">|</span>
            <span>预期目标</span>
            <div id="standard-table">
              <vxe-table :data="expectTableData" :edit-config="{ trigger: 'click', mode: 'cell' }" border resizable show-overflow style="margin-top: 10px">
                <vxe-table-column :edit-render="{ name: 'input', attrs: { type: 'Number' } }" align="right" field="expectedRevenue" header-align="center" title="期望收益(%)" />
                <vxe-table-column :edit-render="{ name: 'input', attrs: { type: 'Number' } }" align="right" field="risk" header-align="center" title="期望风险(%)" />
              </vxe-table>
            </div>
          </div>
          <!-- 参数部分 -->
          <div class="divArea">
            <div class="lineArea" />
            <a class="showArea" rel="mean_params">
              <i v-if="isShowIcon" class="el-icon-arrow-up" @click="isShowIcon = !isShowIcon" />
              <i v-if="!isShowIcon" class="el-icon-arrow-down" @click="isShowIcon = !isShowIcon" />
            </a>
          </div>
          <div v-show="isShowIcon">
            <div class="titleFontStyle" style="position: relative">
              <span class="blueLine">|</span>
              <span>市场均衡配比</span>
              <span class="standard-form">
                <el-button size="small" style="position: absolute; right: 10px" type="primary" @click="handleAddOpinion">新增观点</el-button>
              </span>

              <div id="standard-table">
                <vxe-grid
                  :columns="allRatioColumn"
                  :data="allRatioTableData"
                  :edit-config="{ trigger: 'click', mode: 'cell' }"
                  :span-method="arraySpanMethod"
                  border
                  resizable
                  show-overflow
                  style="margin-top: 10px"
                ></vxe-grid>
              </div>
            </div>
            <div class="titleFontStyle">
              <span class="blueLine">|</span>
              <span>收益及风险列表</span>
              <div id="standard-table">
                <vxe-grid
                  :cell-style="benefitsRiskStyle"
                  :columns="benefitsRiskColumn"
                  :data="benefitsRiskTableData"
                  :edit-config="{ trigger: 'click', mode: 'cell' }"
                  border
                  resizable
                  show-header-overflow
                  show-overflow
                  style="margin-top: 10px"
                />
              </div>
            </div>
            <div class="titleFontStyle">
              <span class="blueLine">|</span>
              <span>相关系数</span>

              <div id="standard-table">
                <vxe-grid
                  :columns="coefficientColumn"
                  :data="coefficientTable"
                  :edit-config="{ trigger: 'click', mode: 'cell' }"
                  border
                  resizable
                  show-header-overflow
                  show-overflow
                  style="margin-top: 10px"
                />
              </div>
            </div>
            <el-row justify="center" type="flex" class="mt10 standard-form">
              <el-button :disabled="buttonStatus" size="small" type="primary" @click="runMarkwitz">运行</el-button>
            </el-row>
          </div>
        </div>
      </el-col>
      <el-col id="markowiz-right" :span="12">
        <el-row>
          <el-col style="padding: 10px">
            <div>
              <echarts v-show="calResult" id="pieChart" ref="pieChart" :options="pieChartOption" resize-dom="choose" style="width: 100%; height: 350px"></echarts>
              <div>
                <span class="dd-table-title">优化比例</span>
              </div>
              <div id="standard-table">
                <vxe-grid ref="xGrid2" :columns="tableColumn2" :data="tableData2" border min-height="500" resizable show-header-overflow show-overflow></vxe-grid>
              </div>
              <div>
                <span class="dd-table-title">组合情况</span>
              </div>
              <div id="standard-table">
                <vxe-grid ref="xGrid3" :columns="tableColumn3" :data="tableData3" border min-height="500" resizable show-header-overflow show-overflow />
              </div>
            </div>
          </el-col>
        </el-row>
      </el-col>
    </el-row>
    <el-dialog :visible.sync="dialogTableVisible" title="基金优化当前可选日期列表">
      <div id="standard-table">
        <el-table :data="gridData">
          <el-table-column type="index" width="50"></el-table-column>
          <el-table-column label="产品代码" property="vcFundcode"></el-table-column>
          <el-table-column label="产品名称" property="vcFundname"></el-table-column>
          <el-table-column label="开始时间" property="beginDate"></el-table-column>
          <el-table-column label="结束时间" property="endDate"></el-table-column>
        </el-table>
        <span style="color: red">注:开始与结束时间输入范围，应取当前可选日期列表交集</span>
        <span style="color: red">如发现产品日期净值缺失，请及时与运维人员联系！</span>
      </div>
    </el-dialog>
    <vue-element-loading :active="vueLoading" :text="vueLoadingText" color="#FF6700" spinner="spinner" />
  </div>
</template>
<script>
import { getToken } from '@/utils/auth'
import { FILE_URL, getSeq } from '@/utils/request'
import pageApi from '@/api/setting/blModel'
import Echarts from '@/components/Echarts'
import _ from 'lodash'
import VueElementLoading from 'vue-element-loading'

export default {
  components: {
    Echarts,
    VueElementLoading
  },
  data() {
    return {
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
        version: '1.2'
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
          field: 'typeName',
          title: '产品名称',
          align: 'center',
          headerAlign: 'center'
        },
        {}
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
      allRatioColumn: [
        {
          field: 'typeName',
          title: '产品名称',
          minWidth: '60px',
          sortable: false,
          align: 'center'
        },
        {
          field: 'equilibriumRatio',
          title: '市场均衡配比(%)',
          minWidth: '60px',
          sortable: false,
          align: 'center',
          editRender: { name: 'input', attrs: { type: 'Number' } }
        },
        {
          field: 'investmentPerspective_1',
          minWidth: '60px',
          sortable: false,
          align: 'center',
          editRender: { name: 'input', attrs: { type: 'Number' } },
          slots: {
            header: ({ row, column, columnIndex }) => {
              let name = '观点' + (columnIndex - 1)
              return [
                <div style="display: inline-block">
                  <span>{name}</span>
                </div>
              ]
            }
          }
        },
        {
          field: 'investmentPerspective_2',
          minWidth: '60px',
          sortable: false,
          align: 'center',
          editRender: { name: 'input', attrs: { type: 'Number' } },
          slots: {
            header: ({ row, column, columnIndex }) => {
              let name = '观点' + (columnIndex - 1)
              return [
                <div style="display: inline-block">
                  <span>{name}</span>
                </div>
              ]
            }
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
  watch: {},
  created() {},
  mounted() {
    this.handleFresh = _.debounce(() => {
      this.drawPie(this.calResult)
      this.handleTablaData(this.calResult)
    }, 150)
    // 文件上传地址
    this.fileUrl = FILE_URL + '/api/assetAllocation/parseExcel.do'
    // let width = document.getElementById('markowiz-right')
    // console.log(width.style)
  },
  methods: {
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
    handleDelOption(index) {
      let fileName = this.allRatioColumn[index].field
      this.allRatioColumn.splice(index, 1)
      this.allRatioTableData.forEach((item) => {
        delete item[fileName]
      })
    },
    handleAddOpinion() {
      if (this.allRatioColumn.length > 11) {
        this.$message.closeAll()
        this.$message.error('观点最多10个')
        return
      }
      let fieldName = 'investmentPerspective' + '_' + (Number(_.last(this.allRatioColumn).field.split('_')[1]) + 1)
      let obj = {
        field: fieldName,
        minWidth: '60px',
        sortable: false,
        align: 'center',
        editRender: { name: 'input', attrs: { type: 'Number' } },
        slots: {
          header: ({ row, column, columnIndex }) => {
            let name = '观点' + (columnIndex - 1)
            return [
              <div style="display: inline-block">
                <span>{name}</span>
                <i class="el-icon-error" style="position: relative;left: 10px;color: red" onClick={() => this.handleDelOption(columnIndex)}></i>
              </div>
            ]
          }
        }
      }
      this.allRatioColumn.push(obj)
      for (let i = 0; i < this.allRatioTableData.length; i++) {
        let temp = this.allRatioTableData[i]
        if (i != this.allRatioTableData.length - 1) {
          temp[fieldName] = 10
        } else {
          temp[fieldName] = 1
        }
      }
    },
    arraySpanMethod({ row, column, rowIndex, columnIndex }) {
      if (this.allRatioTableData.length == 0) {
        return
      }
      let lastIndex = this.allRatioTableData.length - 1
      if (rowIndex === lastIndex) {
        if (columnIndex === 0) {
          return { rowspan: 1, colspan: 2 }
        } else if (columnIndex === 1) {
          return { rowspan: 0, colspan: 0 }
        }
      }
    },
    handleExport() {
      this.$refs.xGrid.exportData()
    },

    // 绘制折线图
    drawLine(data) {
      if (!data || !data.calmar || data.calmar.length == 0) {
        return
      }
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
      this.lineChartOption = {
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
      this.lineChartOption.xAxis[0].data = xdata
      this.lineChartOption.series[0].data = sdata
      this.lineChartOption.series[0].markPoint.data[0].xAxis = (data.portRisk[sharpMaxIndex] * 100).toFixed(2)
      this.lineChartOption.series[0].markPoint.data[0].yAxis = sharp
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
      let i = 0
      // console.log(this.calResult);
      this.fundCodes.forEach((item) => {
        let obj = {
          name: item,
          value: this.calResult.portWts[i]
        }
        i++
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
      let i = 0
      this.fundCodes.forEach((item) => {
        obj[item] = this.calResult.portWts[i]
        i++
      })
      this.tableData2.push(obj)
      if (this.tableData2.length > 0) {
        this.$emit('weightarray', this.tableData2)
      }
      this.tableData3.push({
        portReturn: this.calResult.portReturn * 100,
        portRisk: this.calResult.portRisk * 100,
        markPoint: this.calResult.sharpe,
        calmar: this.calResult.calmar,
        maxdrown: this.calResult.maxdrown
      })
    },
    runMarkwitz() {
      let flag = true
      const numberValidation = '^100$|^(\\d|[1-9]\\d)(\\.\\d{1,2})*$'
      const integerValidation = '^(?:\\d{1,3}|1000)$'
      let result = true
      let riskFree = '' // 无风险收益
      const risks = [] // 风险
      const expectedRevenues = [] // 收益
      let fundCodes = [] // 基金数组
      const correlationCoefficient = [] // 相关系数
      const subcode = '702A' // 科目编码
      const fileName = this.formInline.fileName // 文件名
      const version = this.formInline.version // 版本好
      const frequent = this.formInline.frequent // 频率
      let expectedRevenue = 0
      let risk = 0
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

      // 验证市场均衡配比
      let investmentPerspective = []
      let equilibriumRatio = []
      let confidenceLevels = []
      for (let i = 0; i < this.allRatioColumn.length; i++) {
        let array = []
        if (this.allRatioColumn[i].field != 'typeName' && this.allRatioColumn[i].field != 'equilibriumRatio') {
          for (let j = 0; j < this.allRatioTableData.length - 1; j++) {
            if (this.allRatioTableData[j][this.allRatioColumn[i].field] < 0 || this.allRatioTableData[j][this.allRatioColumn[i].field] > 100) {
              this.$message.closeAll()
              this.$message.error('观点值必须在0～100之间')
              return
            }
            array.push(this.allRatioTableData[j][this.allRatioColumn[i].field] / 100)
          }
          investmentPerspective.push(array)
        }
      }
      for (let i = 0; i < this.allRatioTableData.length - 1; i++) {
        if (this.allRatioTableData[i].equilibriumRatio < 0 || this.allRatioTableData[i].equilibriumRatio > 100) {
          this.$message.closeAll()
          this.$message.error('市场均衡配比必须在0～100之间')
          return
        }
        equilibriumRatio.push(this.allRatioTableData[i].equilibriumRatio)
      }
      for (let i = 0; i < this.allRatioColumn.length; i++) {
        if (this.allRatioColumn[i].field != 'typeName' && this.allRatioColumn[i].field != 'equilibriumRatio') {
          if (
            this.allRatioTableData[this.allRatioTableData.length - 1][this.allRatioColumn[i].field] < 0 ||
            this.allRatioTableData[this.allRatioTableData.length - 1][this.allRatioColumn[i].field] > 1
          ) {
            this.$message.closeAll()
            this.$message.error('观点信心水平必须在0～1之间')
            return
          }
          confidenceLevels.push(this.allRatioTableData[this.allRatioTableData.length - 1][this.allRatioColumn[i].field])
        }
      }

      // 验证预期目标
      this.expectTableData.forEach((item) => {
        result = this.numberValidations(item.expectedRevenue, numberValidation)
        if (result === false) {
          flag = false
          this.$message.closeAll()
          this.$message.error('请检查预期目标的数字格式,必须是0-100之间的数')
          return
        } else {
          expectedRevenue = item.expectedRevenue / 100
        }
        result = this.numberValidations(item.risk, numberValidation)
        if (result === false) {
          flag = false
          this.$message.closeAll()
          this.$message.error('请检查预期目标的数字格式,必须是0-100之间的数')
          return
        } else {
          risk = item.risk / 100
        }
      })

      this.benefitsRiskTableData.forEach((item) => {
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
      for (let i = 0; i < confidenceLevels.length; i++) {
        investmentPerspective[i] = investmentPerspective[i].toString()
      }
      for (let i = 0; i < equilibriumRatio.length; i++) {
        equilibriumRatio[i] = equilibriumRatio[i] / 100
      }
      fundCodes = this.fundCodes

      if (flag === false) return
      // 发送请求
      const params = {}
      let d = new Date()
      params.t = d.getTime()
      params.investmentPerspective = investmentPerspective
      params.equilibriumRatio = equilibriumRatio
      params.confidenceLevels = confidenceLevels
      params.riskFree = riskFree
      params.risks = risks
      params.risk = risk
      params.expectedRevenue = expectedRevenue
      params.expectedRevenues = expectedRevenues
      params.fundCodes = fundCodes
      params.correlationCoefficient = correlationCoefficient
      params.subcode = subcode
      params.fileName = fileName
      params.version = version
      params.frequent = this.createSimuCombParams.frequent
      params.beginDate = this.createSimuCombParams.beginDate
      params.endDate = this.createSimuCombParams.endDate
      params.vcParentCode = this.createSimuCombParams.vcParentCode
      params.riskFree = riskFree
      this.vueLoadingText = '模型计算中'
      this.vueLoading = true
      pageApi
        .runBL(params)
        .then((res) => {
          if (res.data.result.resultCode == 1) {
            this.calResult = res.data.blResult
            this.handleRunMeanResult(res.data.blResult)
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
      this.drawPie(data)
      this.handleTablaData(data)
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
        var integerValidation = '^(?:\\d{1,3}|1000)$'
        const res = this.numberValidations(row[column.property], integerValidation)
        if (res === false) {
          return {
            backgroundColor: 'rgb(255, 117, 117)'
          }
        }
      } else {
        this.lowRatio = _.min(this.expectedRevenueT)
        this.highRatio = _.max(this.expectedRevenueT)
        if (columnIndex === 0) {
          if ((row[column.property], integerValidation > this.highRatio)) {
            return {
              backgroundColor: 'rgb(255, 117, 117)'
            }
          } else if (row.combinedExpectedReturnLow > row.combinedExpectedReturnUpper) {
            return {
              backgroundColor: 'rgb(255, 117, 117)'
            }
          }
        } else {
          if ((row[column.property], integerValidation < this.lowRatio)) {
            return {
              backgroundColor: 'rgb(255, 117, 117)'
            }
          } else if (row.combinedExpectedReturnUpper < row.combinedExpectedReturnLow) {
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
      this.handleBenifitsRiskData()
      this.handleAlloRatioData()
    },
    // 处理配置比例表格数据
    handleAlloRatioData() {
      this.allRatioTableData = []
      this.fundCodes.forEach((item) => {
        let obj = {}
        for (let i = 0; i < this.allRatioColumn.length; i++) {
          if (this.allRatioColumn[i].field == 'typeName') {
            obj.typeName = item
          } else {
            obj[this.allRatioColumn[i].field] = 10
          }
        }
        this.allRatioTableData.push(obj)
      })
      let obj = {
        typeName: '观点信心水平(0,1]',
        lowerRate: '观点信心水平(0,1]'
      }
      for (let i = 0; i < this.allRatioColumn.length; i++) {
        if (this.allRatioColumn[i].field !== 'typeName' && this.allRatioColumn[i].field !== 'equilibriumRatio') {
          obj[this.allRatioColumn[i].field] = 1
        }
      }
      this.allRatioTableData.push(obj)
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
        risk: 12,
        expectedRevenue: 16
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
<style lang="scss" scoped>
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

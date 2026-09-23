<template>
  <div class="factorReturn" >
    <div class="funds-filter search-content">
      <el-form :inline="true" :model="formQuery" class="standard-form" >
        <el-form-item label="">
          <el-select v-model="formQuery.statistPeriod" placeholder="统计周期" size="small" @change="handleDateChange">
            <el-option v-for="item in statistPeriodOpts" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-date-picker v-model="formQuery.startDate" :disabled="disabledDate" placeholder="开始日期" size="small" type="date" value-format="yyyy-MM-dd"></el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-date-picker v-model="formQuery.endDate" :disabled="disabledDate" placeholder="结束日期" size="small" type="date" value-format="yyyy-MM-dd"></el-date-picker>
        </el-form-item>
        <el-form-item class="dbjz">
          <el-select v-model="formQuery.indexType" clearable collapse-tags multiple placeholder="请选择因子类型" size="small">
            <el-option v-for="item in indexOption" :key="item.DIM_CDE" :label="item.DIM_NME + '(' + item.DIM_CDE + ')'" :value="item.DIM_CDE"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item class="dbjz" label="">
          <el-select v-model="formQuery.contrasCode" clearable collapse-tags multiple placeholder="对比指数" size="small" @change="changeContrasCode">
            <el-option v-for="item in contrasStandardOpts" :key="item.id" :label="item.label + '(' + item.id + ')'" :value="item.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button size="small" type="primary" @click="handleSearch" icon="el-icon-search">查询</el-button>
          <el-button size="small" plain type="info" @click="reset" icon="el-icon-refresh-left">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div class="chart-main">

      <div class="kpi-trend" style="margin-bottom: 30px">
        <div class="page-model-title">
          <div class="title-icon">
            <div class="color-box"></div>
          </div>
          <div class="title-txt">
            业绩走势
            <el-tooltip class="table_header_icon" effect="dark" placement="top" v-if="pageType === 'SC'">
              <span slot="content">广发私募市场指数:基于大样本编制的各策略基准指数，季度调仓，季度内用累计增长率加权计算</span>
              <i class="el-icon-question" style="cursor: pointer"></i>
            </el-tooltip>
<!--            <el-button
              size="small"
              type="primary"
              icon="el-icon-download"
              style="margin-left: 15px; padding: 5px 10px;float: right;"
              @click="exportYjzsToExcel"
              :loading="exportLoading"
            >
              导出数据
            </el-button>-->
          </div>
        </div>
        <div class="chart-content" v-loading="searchLoading">
          <myChart id="yjzs" ref="yjzs" :options="kpiOptions" class="echarts_box" resize-dom="cmbfof" />
        </div>
      </div>

      <div class="return">
        <div class="page-model-title">
          <div class="title-icon">
            <div class="color-box"></div>
          </div>
          <div class="title-txt">
            因子收益近期表现
          </div>
        </div>
        <div class="">
          <div>
            <span style="color:#ff0000;padding-left: 30px;">数据截止：{{FactorDataUpDate}}</span>
          </div>
        </div>
        <div class="dataBox" id="standard-table" style="padding:0px 30px 30px;">
          <vxe-table show-header-overflow show-overflow auto-resize :data="tableData" stripe v-loading="searchLoading" >

            <vxe-column field="factorName" title="因子" header-align="center" align="center">
            </vxe-column>
            <vxe-column field="dayYield" title="当日收益" header-align="center" align="right">
              <template slot-scope="scope">
                <span>{{ scope.row.dayYield | numberToFixedStr(2, 100, '%') }}</span>
              </template>
            </vxe-column>
            <vxe-column field="oneMonthYield" title="近一月收益" header-align="center" align="right">
              <template slot-scope="scope">
                <span>{{ scope.row.oneMonthYield | numberToFixedStr(2, 100, '%') }}</span>
              </template>
            </vxe-column>
            <vxe-column field="threeMonthYield" title="近三月收益" header-align="center" align="right">
              <template slot-scope="scope">
                <span>{{ scope.row.threeMonthYield | numberToFixedStr(2, 100, '%') }}</span>
              </template>
            </vxe-column>
            <vxe-column field="sixMonthYield" title="近六月收益" header-align="center" align="right">
              <template slot-scope="scope">
                <span>{{ scope.row.sixMonthYield | numberToFixedStr(2, 100, '%') }}</span>
              </template>
            </vxe-column>
            <vxe-column field="thisYearYield" title="今年以来收益" header-align="center" align="right">
              <template slot-scope="scope">
                <span>{{ scope.row.thisYearYield | numberToFixedStr(2, 100, '%') }}</span>
              </template>
            </vxe-column>
          </vxe-table>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import XLSX from 'xlsx'
import myChart from '@/components/Echarts'
import request from '@/utils/request'
import { dateShortcutMap, STATIST_PERIOD_OPTIONS } from './scripts/constants'
import commonAPI from '@/api/common.js'
import { merger } from '@/utils'
import { CHART_COLOR_ARR } from "@/metaData/enum.js"
import { numberToFixedStr } from '../../../filters'

export default {
  name: 'factorReturn',
  components: {
    myChart
  },
  data() {
    return {
      formQuery: {
        indexType: [],
        statistPeriod: '4',
        startDate: '',
        endDate: '',
        contrasCode: []
      },
      estabStartDate: '', // 成立以来开始时间
      disabledDate: true,
      dateShortcutMap,
      statistPeriodOpts: STATIST_PERIOD_OPTIONS,
      contrasStandardOpts: [],
      zszsOptions: {},
      FactorDataUpDate:'',
      tableData:[],
      searchLoading: false,
      exportLoading: false,

      // 映射查询的编码
      typeToSqlCode: {
        yzsy: {
          title: '因子收益',
          yjzs: '96729115-d7e1-4520-90b1-176123567017',
          dthc: '55f16eb1-37e0-4ce5-af11-bbda6ae45438'
        },
        yhsmzs: {
          title: '广发私募指数',
          yjzs: 'b14be8e9-e93a-4f7f-849d-2816b75f26f4',
          dthc: '517a47cc-d077-438d-8b9c-84882d9ef27d'
        },
        jqbx: {
          jzrq: '25657d95-805c-4b93-a706-0e68c1a381ca',
          table: '5f669efb-5fc7-4c27-974d-057a800ffcfe'
        },
      },
      kpiOptions: {},
      returnOptions: {},
      indexOption: [],
      pageType: 'yzsy'
    }
  },
  async mounted() {
    document.addEventListener('keydown', this.handleGlobalEnter);
    this.formQuery.startDate = dateShortcutMap[this.formQuery.statistPeriod].onClick()[0] || ''
    this.formQuery.endDate = dateShortcutMap[this.formQuery.statistPeriod].onClick()[1] || ''
    await this.getStartDateFromEstab()
    await this.getContrasOptions()
    this.getIndexOptions()
    this.init()
  },
  beforeDestroy() {
    document.removeEventListener('keydown', this.handleGlobalEnter);
  },
  methods: {
    numberToFixedStr,
    handleGlobalEnter(e) {
      if (e.key === 'Enter' && !e.target.classList.contains('el-select__input')) {
        this.handleSearch();
      }
    },
        /**
     * @description 查询指数下拉
     */
     getIndexOptions() {
      return new Promise((resolve, reject) => {
        let params = {
          indexCode: '1db90f0a-e1e4-471f-bcac-f26912ba2e17'
        }
        commonAPI.getDataBysqlCode(params).then(res => {
          const { status, data } = res.data
          if (status === 0) {
            let mergerData = merger(data, 'DIM_TYPE')
            if(this.pageType === 'yzsy') {
              this.indexOption = mergerData.filter(item => item.DIM_TYPE === 'SMPP_INDEXCODE')[0].origin
            } else {
              this.indexOption = mergerData.filter(item => item.DIM_TYPE === 'SM_INDEXCODE')[0].origin
            }
            resolve()
          } else {
            this.indexOption = []
            reject()
          }
        })
      })
    },

    /**
     * @description 查询成立以来开始日期
     */
    getStartDateFromEstab() {
      return new Promise((resolve, reject) => {
        const params = {}
        params.indexCode = '741cb4cc-7893-43f5-bb7e-317efe0d7583'
        commonAPI
          .getDataBysqlCode(params)
          .then((res) => {
            const { status, data } = res.data
            if (status === 0) {
              if (data && data instanceof Array && data.length > 0) {
                this.estabStartDate = data[0].STARTDATE
              } else {
                this.estabStartDate = new Date().getFullYear() + '-' + (new Date().getMonth() + 1) + '-' + new Date().getDate()
              }
            } else {
              this.estabStartDate = new Date().getFullYear() + '-' + (new Date().getMonth() + 1) + '-' + new Date().getDate()
            }
            resolve()
          })
          .catch(() => {
            resolve()
          })
      })
    },
    /**
     * @description 查询所有的echarts指标接口
     */
    getEchartsData(sqlCode) {
      return new Promise((resolve, reject) => {
        // 判断条件是否有空值
        if (this.formQuery.contrasCode && this.formQuery.contrasCode.length <= 0) {
          this.$message.closeAll()
          this.$message({
            type: 'warning',
            customClass: 'message-warning',
            message: '对比指数不能为空'
          })
          reject(new Error('对比指数不能为空'))
          return
        }

        const params = {}
        params.indexCode = sqlCode
        params.startDate = this.formQuery.startDate
        params.endDate = this.formQuery.endDate
        params.baseCode = this.formQuery.contrasCode.toString()
        params.indexType = this.formQuery.indexType.toString()
        commonAPI
          .getDataBysqlCode(params)
          .then((res) => {
            resolve(res)
          })
          .catch((err) => {
            reject(err)
          })
      })
    },

    /**
     * @description 初始化调用
     */
    async init() {
      this.searchLoading = true
      try {
        // 获取业绩走势的echarts数据
        const yjzsReturn = await this.getEchartsData(this.typeToSqlCode.yzsy.yjzs)
        const yjzsData = (yjzsReturn && yjzsReturn.data) || { status: -1, data: [] }
        this.handleYJZSEcharts(yjzsData)

        // 获取因子近期表现数据
        const jqbxJzrqReturn = await this.getEchartsData(this.typeToSqlCode.jqbx.jzrq)
        const jqbxJzrqData = (jqbxJzrqReturn && jqbxJzrqReturn.data) || { status: -1, data: [] }
        await this.handleJQBXjzrq(jqbxJzrqData)
      } catch (error) {
        this.tableData = []
        this.kpiOptions = {}
        this.FactorDataUpDate = ''
        if (error.message !== '对比指数不能为空') {
          this.$message.error('数据查询失败，请重试')
        }
      } finally {
        this.searchLoading = false
      }
    },

    timestampToTime(timestamp) {
      let date = new Date(timestamp)
      let year = date.getFullYear()
      let month = date.getMonth() + 1
      let day = date.getDate()
      return year + '-' + month + '-' + day
    },
    handleJQBXtable(date){
      this.tableData = (date && date.data) || []
    },
    async handleJQBXjzrq(date){
      if (!date || !date.data || date.data.length === 0) {
        this.FactorDataUpDate = ''
        this.tableData = []
        return
      }

      try {
        this.FactorDataUpDate = date.data[0].D_DATE
        const jqbxTableReturn = await this.getTableData(this.typeToSqlCode.jqbx.table, this.FactorDataUpDate)
        const jqbxTableData = (jqbxTableReturn && jqbxTableReturn.data) || { data: [] }
        this.handleJQBXtable(jqbxTableData)
      } catch (error) {
        console.error('获取因子表格数据失败：', error)
        this.tableData = []
        this.FactorDataUpDate = ''
      }
    },
    getTableData(sqlCode,date) {
      return new Promise((resolve, reject) => {
        const params = {}
        params.indexCode = sqlCode
        params.endDate = date
        params.indexType = this.formQuery.indexType.toString()
        commonAPI
          .getDataBysqlCode(params)
          .then((res) => {
            resolve(res)
          })
          .catch((err) => {
            reject(err)
          })
      })
    },

    // 处理业绩走势的echarts数据
    handleYJZSEcharts({ status, data }) {
      if (status === 0) {
        let seriesData = [],
          xData = [],
          legend = []
          let color = CHART_COLOR_ARR
        // let color = ['#f24747', '#5470c6', '#91cc75', '#ee6666',
        //   '#3ba272', '#ff9655', '#f9c956', '#92ce7c',
        //   '#76bedc', '#d87c7c', '#919e8b', '#d7ab82',
        //   '#6e7074', '#61a0a8', '#ec9598', '#eac083', '#bce295',
        //   '#a194e0', '#85b9db', '#7b939b', '#c8aee9',
        //   '#fac090', '#f3d3d3', '#f3bada', '#e0bfa4',
        //   '#bd8f73', '#8fc4d0', '#e9a155', '#8c95c2',
        //   '#f8be55', '#dc8f9c', '#55a296', '#618c86',
        //   '#695630', '#dc3c57', '#afdcd5', '#124d79',
        //   '#836531', '#793742', '#617938', '#4c3860',
        //   '#f8be55', '#257c79', '#657730', '#404867']
        let colorArea = []

        // 分类分离出来广发指数，和对比指数 根据VC_ORDER 来， 1：广发， 2：对比
        let zsArray = [],
          dbArray = []
        data.forEach((item) => {
          item.D_DATE = this.timestampToTime(item.D_DATE)
          if (item.F_YIELD) {
            item.F_YIELD = item.F_YIELD * 100
          }
          // zsArray.push(item)
          if (item.VC_ORDER === '1') {
            zsArray.push(item)
          } else if (item.VC_ORDER === '2') {
            dbArray.push(item)
          }
        })
        // 拿到所有不重复的 日期
        const dateArray = [...new Set(data.map((item) => item.D_DATE))]
        xData = dateArray

        // 分离出来之后，按照不同的DM_NME区分不同的线，ZS 是线，DB是面积图
        // ZSCount
        let ZSCount = 0,
          DBCount = 0
        const mergeDataZS = merger(zsArray, 'DIM_NME')
        mergeDataZS.forEach((item) => {
          const tempOrigin = []
          const seriesObj = {
            name: item.DIM_NME,
            type: 'line',
            symbol: 'none',
            lineStyle: {
              normal: {
                width: 2
              }
            },
            data: []
          }
          legend.push({ name: item.DIM_NME, icon: 'roundRect' })
          for (let i = 0; i < dateArray.length; i++) {
            const temp = dateArray[i]
            const objExample = Object.assign({}, item.origin[0])
            objExample.D_DATE = temp
            objExample.F_YIELD = ''
            const obj = item.origin.find((sitem) => sitem.D_DATE == temp) || objExample
            tempOrigin.push(obj)
          }
          item.origin = tempOrigin
          seriesObj.data = item.origin.map((item) => item.F_YIELD)
          seriesData.push(seriesObj)
          ZSCount = ZSCount + 1
        })
        DBCount = ZSCount
        const mergeDataDB = merger(dbArray, 'DIM_NME')
        mergeDataDB.forEach((item) => {
          let DBColor = color[DBCount % color.length]
          const tempOrigin = []
          const seriesObj = {
            name: item.DIM_NME,
            type: 'line',
            symbol: 'none',
            lineStyle: {
              normal: {
                width: 2
              }
            },
            areaStyle: {
              color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  {
                    offset: 0,
                    color: DBColor // 0% 处的颜色
                  },
                  {
                    offset: 1,
                    color: '#f1f7fd' // 100% 处的颜色
                  }
                ],
                global: false // 缺省为 false
              }
            },
            data: []
          }
          legend.push({ name: item.DIM_NME, icon: 'roundRect' })
          for (let i = 0; i < dateArray.length; i++) {
            const temp = dateArray[i]
            const objExample = Object.assign({}, item.origin[0])
            objExample.D_DATE = temp
            objExample.F_YIELD = ''
            const obj = item.origin.find((sitem) => sitem.D_DATE == temp) || objExample
            tempOrigin.push(obj)
          }
          item.origin = tempOrigin
          seriesObj.data = item.origin.map((item) => item.F_YIELD)
          seriesData.push(seriesObj)
          DBCount = DBCount + 1
        })
        this.kpiOptions = {
          tooltip: {
            trigger: 'axis',
            formatter: (params) => {
              let tip = `<div class="custom-tooltip">`
              tip += params[0].name + '<br>'

              // Display four items per line
              for (let i = 0; i < params.length; i += 4) {
                let row = ''

                // Add first item in the row if it exists
                if (i < params.length) {
                  let value1 = params[i].value === undefined ? '--' : Number(params[i].value).toFixed(2)
                  row += `${params[i].marker} ${params[i].seriesName}: ${value1}&nbsp;&nbsp;&nbsp;&nbsp;`
                }

                // Add second item in the row if it exists
                if (i + 1 < params.length) {
                  let value2 = params[i + 1].value === undefined ? '--' : Number(params[i + 1].value).toFixed(2)
                  row += `${params[i + 1].marker} ${params[i + 1].seriesName}: ${value2}&nbsp;&nbsp;&nbsp;&nbsp;`
                }

                // Add third item in the row if it exists
                if (i + 2 < params.length) {
                  let value3 = params[i + 2].value === undefined ? '--' : Number(params[i + 2].value).toFixed(2)
                  row += `${params[i + 2].marker} ${params[i + 2].seriesName}: ${value3}&nbsp;&nbsp;&nbsp;&nbsp;`
                }

                // Add fourth item in the row if it exists
                if (i + 3 < params.length) {
                  let value4 = params[i + 3].value === undefined ? '--' : Number(params[i + 3].value).toFixed(2)
                  row += `${params[i + 3].marker} ${params[i + 3].seriesName}: ${value4}`
                }

                // Append the completed row to the tooltip
                tip += row + '<br>'
              }

              tip += `</div>`
              return tip
            }
          },
          color: color,
          animation: false,
          legend: {
            top: '3%',
            data: legend,
            type: 'scroll',
            orient: 'horizontal', // 设置水平布局
            left: 'center', // 设置水平位置
            width: '60%',
            itemWidth: 18,
            itemHeight: 16,
            textStyle: { color: '#000', fontSize: 12 }
          },
          grid: {
            left: '2%',
            right: '3%',
            bottom: '10%',
            top: '12%',
            containLabel: true
          },
          toolbox:{
            feature:{
              saveAsImage:{
                name: '业绩走势',
              },
              dataView: {
                show: true,
                title: '数据视图',
                buttonColor: '#e9c5a5',
                buttonTextColor: '#612d10',
                lang: ['数据视图：', '关闭', '导出Excel'],
                contentToOption: function(opts) {
                  this.exportYjzsToExcel();
                }.bind(this),
                optionToContent: function(opt) {
                  var xAxis = (opt.xAxis && Array.isArray(opt.xAxis)) ? opt.xAxis[0] : (opt.xAxis || {});
                  var axisData = xAxis.data || [];
                  var series = opt.series || [];

                  if (axisData.length === 0 || series.length === 0) {
                    return '<div style="text-align:center;padding:20px;">暂无数据</div>';
                  }

                  var tdHeads = '<td style="padding: 0 10px">日期</td>';
                  var tdBodys = '';

                  for (var k = 0; k < series.length; k++) {
                    var item = series[k];
                    var seriesName = item.name ? item.name : '未知指数';
                    tdHeads += '<td style="padding: 0 10px">' + seriesName + '</td>';
                  }

                  var table = '<table id="tableExcel_yjzs" class="table-bordered table-striped" style="width:100%;text-align:center;border-style: solid;border-width: 1px;"><tbody><tr>' + tdHeads + '</tr>';
                  for (var i = 0; i < axisData.length; i++) {
                    var date = axisData[i] || '';
                    tdBodys = '';
                    for (var j = 0; j < series.length; j++) {
                      var ser = series[j];
                      var val = (ser.data && ser.data[i] !== undefined) ? ser.data[i] : undefined;
                      var showVal = '--';
                      if (val !== undefined && val !== '' && !isNaN(Number(val))) {
                        showVal = Number(val).toFixed(2) + '%';
                      }
                      tdBodys += '<td>' + showVal + '</td>';
                    }
                    table += '<tr><td style="padding: 0 10px">' + date + '</td>' + tdBodys + '</tr>';
                  }
                  table += '</tbody></table>';
                  return table;
                }
              }
            }
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: xData,
            axisLabel: {
              inside: false,
              textStyle: {
                fontSize: 11
              }
            },
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
            }
          },
          yAxis: {
            name: '收益率（%）',
            type: 'value',
            position: 'left',
            axisLabel: {
              formatter: function (params) {
                return params.toFixed(2)
              }
            },
            min: function (value) {
              if (value.min < 0) {
                return value.min * 1.1
              } else {
                return value.min
              }
            },
            max: function (value) {
              if (value.max > 0) {
                return value.max
              } else {
                return value.max * 0.9
              }
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
          dataZoom: {
            textStyle: {
              color: 'transparent'
            },
            show: true
            // start: 0,
            // end: 20,
            // maxSpan: 80
          },
          series: seriesData
        }
      } else {
        this.kpiOptions = {}
      }
    },

    // 处理动态回撤的echarts数据
    handleDTHCEcharts({ status, data }) {
      if (status === 0) {
        let seriesData = [],
          xData = [],
          legend = []
        // let color = [
        //   '#fc6769',
        //   '#d2a25a',
        //   '#789d51',
        //   '#6c50f3',
        //   '#396f92',
        //   '#8EB4E3',
        //   '#CCC1DA',
        //   '#FAC090',
        //   '#E6B9B8',
        //   '#E0B1CB',
        //   '#967D69'
        // ]
        let color = CHART_COLOR_ARR

        // let color = ['#f24747', '#5470c6', '#91cc75', '#ee6666', '#3ba272', '#ff9655', '#f9c956', '#92ce7c', '#76bedc', '#d87c7c', '#919e8b', '#d7ab82', '#6e7074', '#61a0a8', '#ec9598', '#eac083', '#bce295', '#a194e0', '#85b9db', '#7b939b', '#c8aee9', '#fac090', '#f3d3d3', '#f3bada', '#e0bfa4', '#bd8f73', '#8fc4d0', '#e9a155', '#8c95c2', '#f8be55', '#dc8f9c', '#55a296']
        let colorArea = []

        // 分类分离出来广发指数，和对比指数 根据VC_ORDER 来， 1：广发， 2：对比
        let zsArray = [],
          dbArray = []
        data.forEach((item) => {
          item.D_DATE = this.timestampToTime(item.D_DATE)
          if (item.MAX_HC) {
            item.MAX_HC = item.MAX_HC * 100
          }
          if (item.VC_ORDER === '1') {
            zsArray.push(item)
          } else if (item.VC_ORDER === '2') {
            dbArray.push(item)
          }
        })
        // 拿到所有不重复的 日期
        const dateArray = [...new Set(data.map((item) => item.D_DATE))]
        xData = dateArray

        // 分离出来之后，按照不同的DM_NME区分不同的线，ZS 是线，DB是面积图
        let ZSCount = 0,
          DBCount = 0
        const mergeDataZS = merger(zsArray, 'DIM_NME')
        mergeDataZS.forEach((item, index) => {
          const tempOrigin = []
          const seriesObj = {
            name: item.DIM_NME,
            type: 'line',
            symbol: 'none',
            lineStyle: {
              normal: {
                width: 2
              }
            },
            // stack: 'Total',
            areaStyle: {},
            data: []
          }
          legend.push({ name: item.DIM_NME, icon: 'roundRect' })
          for (let i = 0; i < dateArray.length; i++) {
            const temp = dateArray[i]
            const objExample = Object.assign({}, item.origin[0])
            objExample.D_DATE = temp
            objExample.MAX_HC = ''
            const obj = item.origin.find((sitem) => sitem.D_DATE == temp) || objExample
            tempOrigin.push(obj)
          }
          item.origin = tempOrigin
          seriesObj.data = item.origin.map((item) => item.MAX_HC)
          seriesData.push(seriesObj)
          ZSCount = ZSCount + 1
        })
        DBCount = ZSCount
        const mergeDataDB = merger(dbArray, 'DIM_NME')
        mergeDataDB.forEach((item) => {
          let DBColor = color[DBCount % color.length]
          const tempOrigin = []
          const seriesObj = {
            name: item.DIM_NME,
            type: 'line',
            // stack: 'Total',
            symbol: 'none',
            lineStyle: {
              normal: {
                width: 2
              }
            },
            // areaStyle: {
            //   color: {
            //     type: 'linear',
            //     x: 0,
            //     y: 0,
            //     x2: 0,
            //     y2: 1,
            //     colorStops: [
            //       {
            //         offset: 0,
            //         color: DBColor // 0% 处的颜色
            //       },
            //       {
            //         offset: 1,
            //         color: '#f1f7fd' // 100% 处的颜色
            //       }
            //     ],
            //     global: false // 缺省为 false
            //   }
            // },
            data: []
          }
          legend.push({ name: item.DIM_NME, icon: 'roundRect' })
          for (let i = 0; i < dateArray.length; i++) {
            const temp = dateArray[i]
            const objExample = Object.assign({}, item.origin[0])
            objExample.D_DATE = temp
            objExample.MAX_HC = ''
            const obj = item.origin.find((sitem) => sitem.D_DATE == temp) || objExample
            tempOrigin.push(obj)
          }
          item.origin = tempOrigin
          seriesObj.data = item.origin.map((item) => item.MAX_HC)
          seriesData.push(seriesObj)
          DBCount = DBCount + 1
        })
        this.returnOptions = {
          tooltip: {
            trigger: 'axis',
            formatter: (params) => {
              let tip = `<div class="custom-tooltip">`
              tip += params[0].name + '<br>'

              // Display two items per line
              for (let i = 0; i < params.length; i += 2) {
                if (i + 1 < params.length) {
                  let value1 = params[i].value === undefined ? '--' : Number(params[i].value).toFixed(2)
                  let value2 = params[i + 1].value === undefined ? '--' : Number(params[i + 1].value).toFixed(2)

                  tip += `${params[i].marker} ${params[i].seriesName}: ${value1}&nbsp;&nbsp;&nbsp;&nbsp;`
                  tip += `${params[i + 1].marker} ${params[i + 1].seriesName}: ${value2}<br>`
                } else {
                  let value = params[i].value === undefined ? '--' : Number(params[i].value).toFixed(2)
                  tip += `${params[i].marker} ${params[i].seriesName}: ${value}<br>`
                }
              }

              tip += `</div>`
              return tip
            }
          },
          color: color,
          legend: {
            top: '3%',
            data: legend,
            type: 'scroll',
            orient: 'horizontal', // 设置水平布局
            left: 'center', // 设置水平位置
            width: '60%',
            itemWidth: 18,
            itemHeight: 16,
            textStyle: { color: '#000', fontSize: 12 }
          },
          animation: false,
          grid: {
            left: '2%',
            right: '3%',
            bottom: '10%',
            top: '12%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            // xData
            data: xData,
            axisLabel: {
              inside: false,
              textStyle: {
                fontSize: 11
              }
            },
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
            }
          },
          yAxis: {
            name: '动态回撤（%）',
            type: 'value',
            position: 'left',
            axisLabel: {
              formatter: function (params) {
                return params.toFixed(2)
              }
            },
            min: function (value) {
              if (value.min < 0) {
                return value.min * 1.1
              } else {
                return value.min
              }
            },
            max: function (value) {
              if (value.max > 0) {
                return value.max
              } else {
                return value.max * 0.9
              }
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
          dataZoom: {
            textStyle: {
              color: 'transparent'
            },
            show: true
            // start: 0,
            // end: 20,
            // maxSpan: 80
          },
          series: seriesData
        }
      } else {
        this.returnOptions = {}
      }
    },
    /**
     * @description 获取对比基准下拉
     */
    getContrasOptions() {
      return new Promise((resolve, reject) => {
        request({
          url: `/api/report/v1.0/data/sql/ecd8867c-64cc-4ebc-9070-04524b04b72c`,
          method: 'post',
          data: {
            indexCode: 'ecd8867c-64cc-4ebc-9070-04524b04b72c'
          }
        })
          .then((res) => {
            if (res.data.status === 0) {
              const resultDim = res.data.data || []
              this.contrasStandardOpts = resultDim.map((item) => {
                return {
                  label: item.DIM_NME,
                  id: item.DIM_CDE
                }
              })
              this.contrasStandardOpts.forEach((item) => {
                if (item.id === '000300' || item.id === 'H11001') {
                  this.formQuery.contrasCode.push(item.id)
                }
              })
            }
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
    },

    /**
     * @description 统计周期区间映射
     */
    handleDateChange(val) {
      if (!val) {
        this.disabledDate = true
        this.formQuery.startDate = ''
        this.formQuery.endDate = ''
        return
      }
      if (val === '7') {
        this.disabledDate = false
      } else if (val === '6') {
        // this.formQuery.startDate = this.baseInfo.FOUND_DATE || ''
        this.disabledDate = true
        this.formQuery.startDate = this.estabStartDate
        // 判断开始时间是不是 当天日期
        this.formQuery.endDate = this.getCurrentOrPreviousDay(this.estabStartDate)
      } else {
        this.disabledDate = true
        this.formQuery.startDate = dateShortcutMap[val].onClick()[0] || ''
        this.formQuery.endDate = dateShortcutMap[val].onClick()[1] || ''
      }
    },

    getCurrentOrPreviousDay(date) {
      const currentDate = new Date()
      const inputDate = new Date(date)

      // 获取当前年月日
      const currentYear = currentDate.getFullYear()
      const currentMonth = currentDate.getMonth() + 1 // 月份从 0 开始，所以需要加 1
      const currentDay = currentDate.getDate()

      // 获取传入日期的年月日
      const inputYear = inputDate.getFullYear()
      const inputMonth = inputDate.getMonth() + 1 // 月份从 0 开始，所以需要加 1
      const inputDay = inputDate.getDate()

      // 如果传入日期大于当前日期，返回传入日期
      if (
        inputYear > currentYear ||
        (inputYear === currentYear && inputMonth > currentMonth) ||
        (inputYear === currentYear && inputMonth === currentMonth && inputDay > currentDay)
      ) {
        return this.formatDate(inputDate)
      }

      // 如果传入日期等于当前日期，返回当前日期
      if (inputYear === currentYear && inputMonth === currentMonth && inputDay === currentDay) {
        return this.formatDate(currentDate)
      }

      // 否则返回当前日期的前一天
      const previousDay = new Date(currentYear, currentMonth - 1, currentDay - 1)
      return this.formatDate(previousDay)
    },

    // 格式化日期为"YYYY-MM-DD"格式
    formatDate(date) {
      const year = date.getFullYear()
      const month = this.padZero(date.getMonth() + 1)
      const day = this.padZero(date.getDate())
      return `${year}-${month}-${day}`
    },

    // 补零函数
    padZero(num) {
      return String(num).padStart(2, '0')
    },

    /**
     * @description 监听对比基准下拉
     */
    changeContrasCode(val) {
      if (val.length > 4) {
        this.$message({
          type: 'warning',
          customClass: 'message-warning',
          message: '对比指数最多只能选四个'
        })
        this.formQuery.contrasCode.splice(-1)
      }
    },
    handleSearch() {
      this.init()
    },
    reset() {
      this.formQuery.indexType = []
      this.formQuery.statistPeriod = '4'
      this.formQuery.startDate = ''
      this.formQuery.endDate = ''
      this.formQuery.contrasCode = []
    },

    exportToExcel(excelData, sheetName, fileName) {
      if (!excelData || excelData.length <= 1) {
        this.$message.warning('暂无有效数据可导出');
        this.exportLoading = false;
        return;
      }
      // 1. 创建工作簿和工作表
      const workbook = XLSX.utils.book_new();
      const worksheet = XLSX.utils.aoa_to_sheet(excelData); // 数组转工作表

      // 2. 将工作表添加到工作簿
      XLSX.utils.book_append_sheet(workbook, worksheet, sheetName);

      // 3. 导出Excel文件
      XLSX.writeFile(workbook, `${fileName}_${new Date().toLocaleDateString().replace(/\//g, '-')}.xlsx`);

      // 4. 关闭加载状态并给出成功提示
      this.exportLoading = false;
      this.$message.success('Excel文件导出成功');
    },

    /**
     * 导出因子收益业绩走势数据到Excel
     */
    exportYjzsToExcel() {
      this.exportLoading = true;
      try {
        const kpiOptions = this.kpiOptions;
        // 校验数据是否存在
        if (!kpiOptions || !kpiOptions.xAxis || !kpiOptions.series || kpiOptions.series.length === 0) {
          this.$message.warning('业绩走势暂无数据可导出');
          this.exportLoading = false;
          return;
        }

        // 1. 提取表头
        const header = ['日期'].concat(kpiOptions.series.map(item => item.name));

        // 2. 提取x轴日期数据
        const xData = (kpiOptions.xAxis && kpiOptions.xAxis.data) || [];
        if (xData.length === 0) {
          this.$message.warning('业绩走势暂无日期数据可导出');
          this.exportLoading = false;
          return;
        }

        // 3. 构建Excel数据行
        const dataRows = xData.map((date, index) => {
          const row = [date];
          kpiOptions.series.forEach(series => {
            const value = series.data[index];
            let formattedValue = '--';
            if (value !== undefined && value !== '' && !isNaN(Number(value))) {
              formattedValue = `${Number(value).toFixed(2)}%`;
            }
            row.push(formattedValue);
          });
          return row;
        });

        // 4. 合并表头和数据行，调用通用导出方法
        const excelData = [header].concat(dataRows);
        this.exportToExcel(excelData, '因子收益业绩走势', '因子收益_业绩走势数据');
      } catch (error) {
        this.exportLoading = false;
        this.$message.error('业绩走势数据导出失败，请重试');
        console.error('因子收益业绩走势导出报错：', error);
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.factorReturn {
  //height: 100%;
  padding-left: 10px;
  padding-right: 10px;
  margin-bottom: 25px;
  .funds-filter {
    width: 100%;

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
    width: 100%;
    //height: 95%;
    //margin-bottom: 30px;
    background-color: #fff;
    .chart-content {
      height: 450px;
      margin-top: 5px;

      .echarts_box {
        height: 100%;
        width: 100%;
      }
    }
  }
}
</style>

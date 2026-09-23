<template>
  <div class="riskIndex">
    <div v-show="showFXZB">
      <div class="titleBox">
        <div class="title_name">
          <div class="title_name_icon"></div>
          风险指标
        </div>
      </div>
      <div class="dataBox" id="standard-table">
        <vxe-table  show-header-overflow show-overflow auto-resize :data="tableData" stripe>
          <vxe-column field="XDATA" title="" header-align="center" align="center" min-width="130">
            <template slot-scope="scope">
              <span>{{ scope.row.XDATA | noDataFilter }}</span>
            </template>
          </vxe-column>
          <vxe-column field="YDATA1" title="收益率(年化)" header-align="center" align="right">
            <template slot="header" slot-scope="{ column }">
              <div>{{ column.title.slice(0, 3) }}</div>
              <span>{{ column.title.slice(3, column.title.length) }}</span>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.YDATA1 | numberToFixedStr(2, 100, '%') }}</span>
            </template>
          </vxe-column>
          <vxe-column field="YDATA2" title="波动率(年化)" header-align="center" align="right">
            <template slot="header" slot-scope="{ column }">
              <div>{{ column.title.slice(0, 3) }}</div>
              <span>{{ column.title.slice(3, column.title.length) }}</span>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.YDATA2 | numberToFixedStr(2, 100, '%') }}</span>
            </template>
          </vxe-column>
          <vxe-column field="YDATA3" title="下行波动率(年化)" header-align="center" align="right">
            <template slot="header" slot-scope="{ column }">
              <div>{{ column.title.slice(0, 5) }}</div>
              <span>{{ column.title.slice(5, column.title.length) }}</span>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.YDATA3 | numberToFixedStr(2, 100, '%') }}</span>
            </template>
          </vxe-column>
          <vxe-column field="YDATA4" title="Alpha" header-align="center" align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.YDATA4 | numberToFixedStr(2, 100, '%') }}</span>
            </template>
          </vxe-column>
          <vxe-column field="YDATA5" title="Beta" header-align="center" align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.YDATA5 | moneyYuan }}</span>
            </template>
          </vxe-column>
          <vxe-column field="YDATA6" title="夏普比率(年化)" header-align="center" align="right">
            <template slot="header" slot-scope="{ column }">
              <div>{{ column.title.slice(0, 4) }}</div>
              <span>{{ column.title.slice(4, column.title.length) }}</span>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.YDATA6 | moneyYuan }}</span>
            </template>
          </vxe-column>
          <vxe-column field="YDATA7" title="索提诺比率(年化)" header-align="center" align="right">
            <template slot="header" slot-scope="{ column }">
              <div>{{ column.title.slice(0, 5) }}</div>
              <span>{{ column.title.slice(5, column.title.length) }}</span>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.YDATA7 | moneyYuan }}</span>
            </template>
          </vxe-column>
          <vxe-column field="YDATA8" title="信息比率(年化)" header-align="center" align="right">
            <template slot="header" slot-scope="{ column }">
              <div>{{ column.title.slice(0, 4) }}</div>
              <span>{{ column.title.slice(4, column.title.length) }}</span>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.YDATA8 | moneyYuan }}</span>
            </template>
          </vxe-column>
          <vxe-column field="YDATA9" title="最大回撤" header-align="center" align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.YDATA9 | numberToFixedStr(2, 100, '%') }}</span>
            </template>
          </vxe-column>
          <vxe-column field="YDATA10" title="最大回撤期间" header-align="center" align="center" min-width="140">
            <template slot-scope="scope">
              <span>{{ scope.row.YDATA10 | noDataFilter }}</span>
            </template>
          </vxe-column>
          <vxe-column field="YDATA11" title="卡玛比率" header-align="center" align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.YDATA11 | moneyYuan }}</span>
            </template>
          </vxe-column>
        </vxe-table>
      </div>
    </div>
    <div v-show="showDTHC">
      <div class="titleBox">
        <div class="line"></div>
        <div class="title_name">
          <div class="title_name_icon"></div>
          动态回撤
          <el-tooltip class="table_header_icon" effect="dark" placement="top">
            <span slot="content">T日回撤=（T日累计单位净值-回撤区间最大累计单位净值）/回撤区间最大累计单位净值（回撤区间为查询开始日至T日）</span>
            <i class="el-icon-question" style="cursor: pointer"></i>
          </el-tooltip>
        </div>
      </div>
      <div class="dataBox chart-content">
        <myChart id="Dthc" ref="dthc" :options="returnOptions" class="echarts_box" resize-dom="cmbfof" />
      </div>
    </div>
    <div v-show="showPM">
      <div class="titleBox">
        <el-row type="flex" align="middle">
          <el-col :span="4" class="title_name title_name1">
            <div class="title_name_icon" style="margin-right: 10px"></div>
            <span>排名</span>
            <el-tooltip class="table_header_icon" effect="dark" placement="top">
              <span slot="content" ref="contentHint">排名样本范围为广发托管/外包产品</span>
              <i class="el-icon-question" style="cursor: pointer"></i>
            </el-tooltip>
          </el-col>
          <el-col :span="20" style="text-align: right">
            <div class="btnClass" v-for="(item, index) of btnArr" :key="index" @click="toSwitchData(item)" :class="{ btnClassClick: item.type == activeType }">
              {{ item.name }}
            </div>
          </el-col>
        </el-row>
      </div>
      <div class="dataBox">
        <el-row>
          <el-col :span="12">
            <el-row>
              <el-col :span="12">
                <myChart id="pm_tg_one" ref="relaParty" :options="echartsOption1" resize-dom="retrade" style="width: 100%; height: 280px"></myChart>
              </el-col>
              <el-col :span="12">
                <myChart id="pm_tg_two" ref="relaParty" :options="echartsOption2" resize-dom="retrade" style="width: 100%; height: 280px"></myChart>
              </el-col>
            </el-row>
            <div style="text-align: center">
              <el-radio-group v-model="radio" @change="selectRadio">
                <el-radio :label="1">收益率</el-radio>
                <el-radio :label="2">最大回撤</el-radio>
                <el-radio :label="3">夏普</el-radio>
              </el-radio-group>
            </div>
          </el-col>
          <el-col :span="12">
            <div style="color: #333; margin-bottom: 10px">
              <span>排名日期：{{ rankingDate }}</span>
            </div>
            <div id="standard-table">
              <vxe-table
                show-header-overflow
                show-overflow
                auto-resize
                :row-config="{ isHover: true }"
                :data="tableData1"
                stripe
              >
                <vxe-column field="YDATE" title="" header-align="center" align="center">
                  <template slot-scope="scope">
                    <span>{{ scope.row.YDATE | noDataFilter }}</span>
                  </template>
                </vxe-column>
                <vxe-column field="YDATE2" title="收益率" header-align="center" align="right">
                  <template slot-scope="scope">
                    <span>{{ scope.row.YDATE2 | numberToFixedStr(2, 100, '%') }}</span>
                  </template>
                </vxe-column>
                <vxe-column field="YDATE5" title="最大回撤" header-align="center" align="right">
                  <template slot-scope="scope">
                    <span>{{ scope.row.YDATE5 | numberToFixedStr(2, 100, '%') }}</span>
                  </template>
                </vxe-column>
                <vxe-column field="YDATE8" title="Sharpe比率" header-align="center" align="right">
                  <template slot-scope="scope">
                    <span>{{ scope.row.YDATE8 | moneyYuan }}</span>
                  </template>
                </vxe-column>
              </vxe-table>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>
    <!-- <div class="noData" v-else>
      无数据
    </div> -->
  </div>
</template>
<script>
import myChart from '@/components/Echarts'
import commonAPI from '@/api/common.js'
import { merger } from '@/utils'
import { dateShortcutMap, STATIST_PERIOD_OPTIONS } from '../../scripts/baseInfoConstant'
export default {
  name: '',
  components: {
    myChart
  },
  props: {
    coverDiv: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      tableData: [],
      tableData1: [], //排名数据
      returnOptions: {},
      searchQuery: null,
      activeType: '6',
      btnArr: [
        { name: '成立以来', type: '6', flag: 'INCEP' },
        { name: '今年以来', type: '5', flag: 'YTD' },
        { name: '近1月', type: '1', flag: '1M' },
        { name: '近3月', type: '2', flag: '3M' },
        { name: '近6月', type: '3', flag: '6M' },
        { name: '近1年', type: '4', flag: '1Y' }
      ],
      echartsOption1: {
        series: [
          {
            type: 'gauge',
            startAngle: 180,
            endAngle: 0,
            center: ['50%', '65%'],
            radius: '90%',
            axisLine: {
              lineStyle: {
                width: 15,
                color: [[1, '#91e5ff']]
              }
            },
            pointer: {
              itemStyle: {
                color: 'inherit'
              },
              length: '25%',
              width: 3,
              offsetCenter: [0, '-45%']
            },
            axisTick: {
              distance: -15,
              length: 8,
              lineStyle: {
                color: '#fff',
                width: 1
              }
            },
            splitLine: {
              distance: -15,
              length: 15,
              lineStyle: {
                color: '#fff',
                width: 2
              }
            },
            axisLabel: {
              color: 'inherit',
              distance: 23,
              fontSize: 14
            },
            title: {
              offsetCenter: [0, '0%'],
              fontSize: 14,
              color: 'inherit'
            },
            detail: {
              fontSize: 20,
              offsetCenter: [0, '-15%'],
              valueAnimation: true,
              formatter: function (value) {
                return value + ''
              },
              color: 'inherit'
            },
            data: [
              {
                value: 0,
                name: '一级策略排名'
              }
            ]
          }
        ]
      },
      echartsOption2: {
        series: [
          {
            type: 'gauge',
            startAngle: 180,
            endAngle: 0,
            center: ['50%', '65%'],
            radius: '90%',
            axisLine: {
              lineStyle: {
                width: 15,
                color: [[1, '#fd7c53']]
              }
            },
            pointer: {
              itemStyle: {
                color: 'inherit'
              },
              length: '25%',
              width: 3,
              offsetCenter: [0, '-45%']
            },
            axisTick: {
              distance: -15,
              length: 8,
              lineStyle: {
                color: '#fff',
                width: 1
              }
            },
            splitLine: {
              distance: -15,
              length: 15,
              lineStyle: {
                color: '#fff',
                width: 2
              }
            },
            axisLabel: {
              color: 'inherit',
              distance: 23,
              fontSize: 14
            },
            title: {
              offsetCenter: [0, '0%'],
              fontSize: 14,
              color: 'inherit'
            },
            detail: {
              fontSize: 20,
              offsetCenter: [0, '-15%'],
              valueAnimation: true,
              formatter: function (value) {
                return value + ''
              },
              color: 'inherit'
            },
            data: [
              {
                value: 0,
                name: '二级策略排名'
              }
            ]
          }
        ]
      },
      startDate: '',
      endDate: '',
      statistPeriodOpts: STATIST_PERIOD_OPTIONS, //统计周期
      estabStartDate: '', // 成立以来开始时间
      radio: 1,
      canShowIndexArr: [],
      showFXZB: false,
      showPM: false,
      showDTHC: false,
      rankingDate: '',
      flag: ''
    }
  },
  methods: {
    async fun_iframeSrc() {
      this.activeType = this.searchQuery.statistPeriod
      this.startDate = this.searchQuery.startDate
      this.endDate = this.searchQuery.endDate
      this.btnArr.forEach((element) => {
        if (element.type == this.searchQuery.statistPeriod) {
          this.flag = element.flag
        }
      })
      //获取可展示指数
      await this.getCanShowIndex()
      //获取成立以来的开始时间
      await this.getStartDateFromEstab()
      //获取风险指标
      if (this.showFXZB) {
        this.getFxzbData('4f554c42-8ce9-45be-9b91-75beaab100be')
      }
      //获取排名数据
      if (this.showPM) {
        this.getDialData_tg('23c7a742-6f73-4380-89c4-f753501897d2')
      }
      // 获取动态回撤的echarts数据
      if (this.showDTHC) {
        const dthcReturn = await this.getEchartsData('25350ae8-3204-4c38-b680-1d4c473bfd0f')
        if (dthcReturn.data) {
          this.handleDTHCEcharts(dthcReturn.data)
        }
      }
    },
    getEchartsData(sqlCode) {
      return new Promise((resolve, reject) => {
        const params = {}
        params.indexCode = sqlCode
        params.startDate = this.searchQuery.startDate
        params.endDate = this.searchQuery.endDate
        params.fundCode = this.searchQuery.fundCode
        params.kpiCode = this.searchQuery.kpiCode
        ;(params.contrasCode = this.searchQuery.contrasCode ? this.searchQuery.contrasCode.join(',') : ''),
          commonAPI
            .getDataBysqlCode(params)
            .then((res) => {
              resolve(res)
            })
            .catch((err) => {
              resolve(err)
            })
      })
    },
    getFxzbData(sqlCode) {
      return new Promise((resolve, reject) => {
        const params = {}
        params.indexCode = sqlCode
        params.startDate = this.searchQuery.startDate
        params.endDate = this.searchQuery.endDate
        params.fundCode = this.searchQuery.fundCode
        params.kpiCode = this.searchQuery.kpiCode
        ;(params.contrasCode = this.searchQuery.contrasCode ? this.searchQuery.contrasCode.join(',') : ''),
          commonAPI
            .getDataBysqlCode(params)
            .then((res) => {
              let { status, data } = res.data
              if (status == 0) {
                this.tableData = data
              }
            })
            .catch((err) => {})
      })
    },
    // 处理动态回撤的echarts数据
    handleDTHCEcharts({ status, data }) {
      if (status === 0) {
        let seriesData = [],
          xData = [],
          legend = []
        let color = ['#fc6769', '#d2a25a', '#789d51', '#6c50f3', '#396f92', '#8EB4E3', '#CCC1DA', '#FAC090', '#E6B9B8', '#E0B1CB', '#967D69']
        data.forEach((item) => {
          if (item.YDATA2) {
            item.YDATA2 = item.YDATA2 * 100
          }
        })
        // 拿到所有不重复的 日期
        const dateArray = [...new Set(data.map((item) => item.XDATA))]
        xData = dateArray
        // 分离出来之后，按照不同的DM_NME区分不同的线，ZS 是线，DB是面积图
        const mergeData = merger(data, 'YDATA1')
        mergeData.forEach((item) => {
          const tempOrigin = []
          const seriesObj = {
            name: item.YDATA1,
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
          legend.push({ name: item.YDATA1, icon: 'roundRect' })
          for (let i = 0; i < dateArray.length; i++) {
            const temp = dateArray[i]
            const objExample = Object.assign({}, item.origin[0])
            objExample.XDATA = temp
            objExample.YDATA2 = ''
            const obj = item.origin.find((sitem) => sitem.XDATA == temp) || objExample
            tempOrigin.push(obj)
          }
          item.origin = tempOrigin
          seriesObj.data = item.origin.map((item) => item.YDATA2)
          seriesData.push(seriesObj)
        })
        this.returnOptions = {
          tooltip: {
            trigger: 'axis',
            formatter: (params) => {
              let tip = params[0].name + '<br>'
              for (let i = 0; i < params.length; i++) {
                let value = ''
                if (params[i].value == undefined || params[i].value == '') {
                  value = '--'
                } else {
                  value = Number(params[i].value).toFixed(2)
                }
                tip += params[i].marker + params[i].seriesName + ': ' + value + '<br>'
              }
              return tip
            }
          },
          color: color,
          legend: {
            top: '3%',
            data: legend,
            itemWidth: 18,
            itemHeight: 12,
            textStyle: { color: '#000', fontSize: 12 }
          },
          animation: false,
          grid: {
            left: '100',
            right: '100',
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
            name: '回撤（%）',
            type: 'value',
            position: 'left',
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
          dataZoom: {
            show: true
            // start: 0,
            // end: 20,
            // maxSpan: 80
          },
          series: seriesData
        }
      }
    },
    timestampToTime(timestamp) {
      let date = new Date(timestamp)
      let year = date.getFullYear()
      let month = date.getMonth() + 1
      let day = date.getDate()
      return year + '-' + month + '-' + day
    },
    getCanShowIndex() {
      return new Promise((resolve, reject) => {
        const params = {}
        params.templateCode = 'b8b0547d-23d5-4150-8308-68d50eee81a8'
        commonAPI
          .selectIndexInfos(params)
          .then((res) => {
            const { status, data } = res.data
            if (status === 0) {
              data.forEach((element) => {
                this.canShowIndexArr.push(element.vcCode)
              })
              if (this.canShowIndexArr.includes('b61a919e-f4cd-46f6-a129-bf99b59185b2')) {
                this.showPM = true
              } else {
                this.showPM = false
              }
              if (this.canShowIndexArr.includes('318b3447-26ff-4857-81e8-05db94a9d7e8')) {
                this.showDTHC = true
              } else {
                this.showDTHC = false
              }
              if (this.canShowIndexArr.includes('e06157be-42af-4ad8-b53d-0a9eb4183f86')) {
                this.showFXZB = true
              } else {
                this.showFXZB = false
              }
            }
            resolve()
          })
          .catch(() => {
            resolve()
          })
      })
    },
    //查询成立以来开始日期
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
    //统计周期区间映射
    toSwitchData(data) {
      let val = data.type
      this.activeType = val
      this.flag = data.flag
      if (!val) {
        this.startDate = ''
        this.endDate = ''
        return
      }
      if (val === '6') {
        this.startDate = this.estabStartDate
        this.endDate = new Date().getFullYear() + '-' + (new Date().getMonth() + 1) + '-' + new Date().getDate()
      } else {
        this.startDate = dateShortcutMap[val].onClick()[0] || ''
        this.endDate = dateShortcutMap[val].onClick()[1] || ''
      }
      this.getDialData_tg('23c7a742-6f73-4380-89c4-f753501897d2')
    },
    getDialData_tg(sqlCode) {
      return new Promise((resolve, reject) => {
        const params = {}
        params.indexCode = sqlCode
        params.startDate = this.startDate
        params.endDate = this.endDate
        params.fundCode = this.searchQuery.fundCode
        params.val = this.flag
        commonAPI
          .getDataBysqlCode(params)
          .then((res) => {
            let { data, status } = res.data
            if (status == 0) {
              this.tableData1 = data
              this.radio = 1
              if (data.length) {
                this.echartsOption1.series[0].data[0].value = data[0].YDATE3 ? data[0].YDATE3 : 0
                this.echartsOption2.series[0].data[0].value = data[0].YDATE4 ? data[0].YDATE4 : 0
              }
            }
            resolve(res)
          })
          .catch((err) => {
            resolve(err)
          })
      })
    },
    selectRadio(val) {
      if (this.tableData1.length) {
        if (val == 1) {
          this.echartsOption1.series[0].data[0].value = this.tableData1[0].YDATE3 ? this.tableData1[0].YDATE3 : 0
          this.echartsOption2.series[0].data[0].value = this.tableData1[0].YDATE4 ? this.tableData1[0].YDATE4 : 0
        } else if (val == 2) {
          this.echartsOption1.series[0].data[0].value = this.tableData1[0].YDATE6 ? this.tableData1[0].YDATE6 : 0
          this.echartsOption2.series[0].data[0].value = this.tableData1[0].YDATE7 ? this.tableData1[0].YDATE7 : 0
        } else {
          this.echartsOption1.series[0].data[0].value = this.tableData1[0].YDATE9 ? this.tableData1[0].YDATE9 : 0
          this.echartsOption2.series[0].data[0].value = this.tableData1[0].YDATE10 ? this.tableData1[0].YDATE10 : 0
        }
      }
    }
  }
}
</script>
<style lang="scss" scoped>
.riskIndex {
  position: relative;
  // height: 2900px;
  margin: 0 30px;
  .titleBox {
    border-bottom: 1px solid #0f65dd;
    padding: 20px 0 10px;
    font-size: 16px;
    margin-bottom: 20px;
  }
  .title_name {
    height: 16px;
    line-height: 16px;
    color: #0f65dd;
    padding-left: 5px;
  }
  .title_name1 {
    position: relative;
    top: 5px;
  }
  .title_name_icon {
    width: 2px;
    display: inline-block;
    height: 14px;
    line-height: 14px;
    background-color: #0f65dd;
    position: relative;
    top: 1px;
    margin-right: 10px;
  }
  .noData {
    border: 1px solid #d4d4d4;
    height: 40px;
    background-color: #f7f7f7;
    text-align: center;
    line-height: 40px;
    color: #333;
    margin: 40px 30px 20px;
  }
  .dataBox {
    padding: 20px 30px 20px;
  }
  .chart-content {
    height: 450px;
    margin-top: 5px;
    .echarts_box {
      height: 100%;
      width: 100%;
    }
  }
  .btnClass {
    padding: 5px 15px;
    background-color: #ddd;
    color: #333;
    // float: right;
    display: inline-block;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
    position: relative;
    top: -2px;
    margin-left: 5px;
  }
  .btnClassClick {
    color: white;
    background-color: #0f65dd;
  }
  .table_header_icon {
    color: #0f65dd;
    font-size: 16px;
    position: relative;
    top: 1px;
  }
}
::v-deep .vxe-table .vxe-body--row.row--stripe {
  background-color: #f9fafe !important;
}
</style>

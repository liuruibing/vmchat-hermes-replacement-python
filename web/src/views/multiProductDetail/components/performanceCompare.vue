<template>
  <div class="investment-history-tg">
    <div v-if="indexInfoArray.indexOf('e6ec5557-984c-41ce-a032-99d357485098') !== -1">
      <div class="title">
        <div class="title-icon">
          <div class="color-box"></div>
        </div>
        <div class="title-txt">
          <span>历史收益走势图</span>
        </div>
<!--        <el-select
          :ref="'test' + index"
          style="width: 120px !important; float: right"
          v-model="frequencyCode"
          placeholder="请选择"
          size="mini"
          clearable
          @change="handleFrequencyChange"
        >
          <el-option v-for="item in frequencyOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>-->
      </div>
    </div>
    <el-row v-if="indexInfoArray.indexOf('e6ec5557-984c-41ce-a032-99d357485098') !== -1">
      <el-col :span="14">
        <div class="chart-content">
          <myChart id="investmentHistoryTg" ref="investmentHistoryTg" :options="investmentHistoryTgOption" class="echarts_box" resize-dom="cmbfof" />
        </div>
      </el-col>
      <el-col :span="10">
        <div class="chart-content" id="standard-table">
          <div>
            <span>日期:</span>
            {{ activatedData | noDataFilter }}
          </div>
          <vxe-table :data="tableData"
                     :default-sort="{ prop: 'f3', order: 'desc' }"
                     auto-resize border show-header-overflow show-overflow>
            <vxe-table-column  align="left" header-align="center" title="产品/对比指标">
              <template slot-scope="scope">
                {{ scope.row.f1 | noDataFilter }}
              </template>
            </vxe-table-column>
            <vxe-table-column align="right" header-align="center" title="收益率">
              <template slot-scope="scope">
                <span v-if="scope.row.f2 && scope.row.f2 > 0" style="color: red">
                  {{ scope.row.f2 | numberToFixedStr(2, 100, '%') }}
                </span>
                <span v-else-if="scope.row.f2 && scope.row.f2 < 0" style="color: green">
                  {{ scope.row.f2 | numberToFixedStr(2, 100, '%') }}
                </span>
                <span v-else>
                  {{ scope.row.f2 | numberToFixedStr(2, 100, '%') }}
                </span>
              </template>
            </vxe-table-column>
            <vxe-table-column  align="right" header-align="center" title="归一化净值">
              <template slot-scope="scope">
                <span>{{ scope.row.f3 | numberToFixed(4, 1) }}</span>
              </template>
            </vxe-table-column>
          </vxe-table>
        </div>
      </el-col>
    </el-row>
    <div v-if="indexInfoArray.indexOf('a54d32cd-d394-4758-ba41-36e8297a39f9') !== -1">
      <div class="title">
        <div class="title-icon">
          <div class="color-box"></div>
        </div>
        <div class="title-txt">
          <span>业绩对比</span>
        </div>
      </div>
    </div>
    <div id="standard-table">
      <vxe-table
        v-if="indexInfoArray.indexOf('a54d32cd-d394-4758-ba41-36e8297a39f9') !== -1"
        :data="tableData2"
        v-loading="tableLoading2"
        auto-resize
        border
        max-height="500px"
        show-header-overflow
        show-overflow
        style="margin: 20px 30px"
        :sort-config="{ remote: true, defaultSort: { field: 'YDATE8', order: 'desc' } }"
        @sort-change="customSortMethod2"
      >

        <vxe-table-column field="XDATE" sortable align="center" header-align="center" min-width="130px" title="产品代码">
          <template slot-scope="scope">
            <span>{{ scope.row.XDATE | noDataFilter }}</span>
          </template>
        </vxe-table-column>
        <vxe-table-column  field="YDATE"  sortable align="left" header-align="center" min-width="180px" title="产品名称">
          <template slot-scope="scope">
            <span>{{ scope.row.YDATE | noDataFilter }}</span>
          </template>
        </vxe-table-column>
        <vxe-table-column  field="YDATE1"  sortable align="center" header-align="center" min-width="130px" title="投资策略">
          <template slot-scope="scope">
            <span>{{ scope.row.YDATE1 | noDataFilter }}</span>
          </template>
        </vxe-table-column>
        <vxe-table-column   field="YDATE2" sortable align="center" header-align="center" min-width="100px" title="管理人">
          <template slot-scope="scope">
            <span>{{ scope.row.YDATE2 | noDataFilter }}</span>
          </template>
        </vxe-table-column>
        <vxe-table-column  field="YDATE3" sortable align="center" header-align="center" min-width="130px" title="成立日期">
          <template slot-scope="scope">
            <span>{{ scope.row.YDATE3 | noDataFilter }}</span>
          </template>
        </vxe-table-column>

        <vxe-table-column  field="YDATE10" sortable align="center" header-align="center" min-width="130px" title="截止日期">
          <template slot-scope="scope">
            <span>{{ scope.row.YDATE10 | noDataFilter }}</span>
          </template>
        </vxe-table-column>
        <vxe-table-column  field="YDATE4" sortable align="right" header-align="center" min-width="130px" title="近一月收益率">
          <template slot-scope="scope">
            <span v-if="scope.row.YDATE4 && scope.row.YDATE4 > 0" style="color: red">
              {{ scope.row.YDATE4 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else-if="scope.row.YDATE4 && scope.row.YDATE4 < 0" style="color: green">
              {{ scope.row.YDATE4 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else>
              {{ scope.row.YDATE4 | numberToFixedStr(2, 100, '%') }}
            </span>
          </template>
        </vxe-table-column>
        <vxe-table-column field="YDATE5"  sortable align="right" header-align="center" min-width="130px" title="近三月收益率">
          <template slot-scope="scope">
            <span v-if="scope.row.YDATE5 && scope.row.YDATE5 > 0" style="color: red">
              {{ scope.row.YDATE5 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else-if="scope.row.YDATE5 && scope.row.YDATE5 < 0" style="color: green">
              {{ scope.row.YDATE5 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else>
              {{ scope.row.YDATE5 | numberToFixedStr(2, 100, '%') }}
            </span>
          </template>
        </vxe-table-column>
        <vxe-table-column   field="YDATE6"  sortable align="right" header-align="center" min-width="130px" title="近六月收益率">
          <template slot-scope="scope">
            <span v-if="scope.row.YDATE6 && scope.row.YDATE6 > 0" style="color: red">
              {{ scope.row.YDATE6 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else-if="scope.row.YDATE6 && scope.row.YDATE6 < 0" style="color: green">
              {{ scope.row.YDATE6 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else>
              {{ scope.row.YDATE6 | numberToFixedStr(2, 100, '%') }}
            </span>
          </template>
        </vxe-table-column>
        <vxe-table-column  field="YDATE7"  sortable align="right" header-align="center" min-width="130px" title="近一年收益率">
          <template slot-scope="scope">
            <span v-if="scope.row.YDATE7 && scope.row.YDATE7 > 0" style="color: red">
              {{ scope.row.YDATE7 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else-if="scope.row.YDATE7 && scope.row.YDATE7 < 0" style="color: green">
              {{ scope.row.YDATE7 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else>
              {{ scope.row.YDATE7 | numberToFixedStr(2, 100, '%') }}
            </span>
          </template>
        </vxe-table-column>
        <vxe-table-column  field="YDATE8" sortable align="right" header-align="center" min-width="130px" title="今年以来收益率">
          <template slot-scope="scope">
            <span v-if="scope.row.YDATE8 && scope.row.YDATE8 > 0" style="color: red">
              {{ scope.row.YDATE8 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else-if="scope.row.YDATE8 && scope.row.YDATE8 < 0" style="color: green">
              {{ scope.row.YDATE8 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else>
              {{ scope.row.YDATE8 | numberToFixedStr(2, 100, '%') }}
            </span>
          </template>
        </vxe-table-column>
        <vxe-table-column  field="YDATE9"  sortable align="right" header-align="center" min-width="130px" title="成立以来收益率">
          <template slot-scope="scope">
            <span v-if="scope.row.YDATE9 && scope.row.YDATE9 > 0" style="color: red">
              {{ scope.row.YDATE9 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else-if="scope.row.YDATE9 && scope.row.YDATE9 < 0" style="color: green">
              {{ scope.row.YDATE9 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else>
              {{ scope.row.YDATE9 | numberToFixedStr(2, 100, '%') }}
            </span>
          </template>
        </vxe-table-column>
      </vxe-table>
    </div>
  </div>
</template>
<script>
import pageApi from '../api/performanceCompare'
import { merger } from '@/utils'
import myChart from '@/components/Echarts'
import commonFun from '@/filters/common'
import commonApi from '@/api/common'
import Pagination from '@/components/Pagination'
import { frequencyOptions } from '@/dataDictionary/frequency'
import { numberToFixedStr } from '@/filters'

export default {
  components: { myChart, Pagination },
  props: {
    formQuery: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      searchQuery: null,
      indexInfoArray: [],
      investmentHistoryTgOption: {},
      orderString2:'YDATE8 desc',
      investmentHistoryTgOption2: {},
      activatedData: '',
      echartData: '',
      tableData: [], // 业绩分析上表格
      tableData2: [],
      tableData3: [],
      tableData4: [],
      tableLoading1: false,
      tableLoading2: false,
      tableLoading3: false,
      tableLoading4: false,
      activeType: '2',
      pageSize: 10,
      pageNum: 1,
      total: 0,
      pageFlag: true,
      numberToFixedStr: numberToFixedStr,
      btnArr: [
        { name: '近2年', type: '2', flag: '2M' },
        { name: '近5年', type: '5', flag: '5M' }
        // {name: '导出', type: '3', flag: 'export'}
      ],
      //frequencyOptions: frequencyOptions,
      frequencyOptions:[
        {
          label: '日频',
          value: 'D'
        },
        {
          label: '周频',
          value: 'W'
        },
      ],
      frequencyCode: ''
    }
  },
  watch: {
    activatedData: {
      handler(val) {
        // 组装tableData数据
        const tableDataArray = []
        for (let i = 0; i < this.echartData.length; i++) {
          const temp = this.echartData[i]
          if (temp.origin && temp.origin.length && temp.origin.length > 0) {
            for (let j = 0; j < temp.origin.length; j++) {
              const tempJ = temp.origin[j]
              if (tempJ.XDATA == val) {
                tableDataArray.push({
                  f1: tempJ.YDATA || '',
                  f2: tempJ.YDATA2 || '',
                  f3: tempJ.YDATA5 || ''
                })
                break
              }
            }
          }
        }
        this.tableData = [...tableDataArray]
      },
      deep: true
    }
  },
  methods: {

    //业绩对比排序
    customSortMethod2(val) {
      this.orderString2 = commonFun.queryOrderBy_vxe_template(val)
      this.getIndustryDataUp()
    },
    /**
     * @description 监听历史收益走势图频率下拉
     */
    handleFrequencyChange(val) {
      this.queryHistoryEarn(val)
    },
    /**
     * @description 根据频率下拉值查询数据（先调用权限判断）
     */
    async queryHistoryEarn(val) {
      // 首先查询 权限
      await this.getIndexInfo()
      // 如果 历史收益走势图编码存在则查询
      if (this.indexInfoArray.indexOf('e6ec5557-984c-41ce-a032-99d357485098') !== -1) {
        this.getInvestMentHistoryData(val)
      }
    },
    /**
     * @desc 初始化数据
     */
    initData() {
      this.fun_iframeSrc()
    },

    // 页面查询
    async fun_iframeSrc() {
      this.echartData = ''
      this.tableData = []
      this.tableData2 = []
      this.tableData3 = []
      this.tableData4 = []
      this.activatedData = ''
      this.indexInfoArray = []
      this.investmentHistoryTgOption = {}
      this.investmentHistoryTgOption2 = {}
      // 首先查询 权限
      await this.getIndexInfo()

      // 如果 历史收益走势图编码存在则查询
      if (this.indexInfoArray.indexOf('e6ec5557-984c-41ce-a032-99d357485098') !== -1) {
        this.getInvestMentHistoryData(this.frequencyCode)
      }

      // 如果 业绩对比编码存在则查询
      if (this.indexInfoArray.indexOf('a54d32cd-d394-4758-ba41-36e8297a39f9') !== -1) {
        this.getIndustryDataUp()
      }
    },
    // 获取权限指标权限列表
    getIndexInfo() {
      return new Promise((resolve, reject) => {
        const params = {}
        params.templateCode = '8efbc22d-00a0-45b0-96bf-e5b21c046f28'
        params.fundCode = this.formQuery.productCodes
        pageApi
          .selectIndexInfos(params)
          .then((res) => {
            const { status, data } = res.data
            if (status == 0) {
              this.indexInfoArray = data.map((item) => item.vcCode)
            } else {
              this.indexInfoArray = []
            }
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
    },

    // 获取历史收益走势图数据
    getInvestMentHistoryData(val) {
      let params = Object.assign({}, this.formQuery)
      params.baseCode = params.dbjz.toString()
      params.rate = val ? val : ''
      params.indexCode = '5f91fd04-3c21-45d8-a7f0-539c7510ee7f'
      params._pageFlag = false
      commonApi.getDataBysqlCode(params).then((res) => {
        const { status, data } = res.data
        if (status == 0) {
          if (data.length > 0) {
            this.handleEchartsData(data)
          } else {
            this.investmentHistoryTgOption = {}
          }
        }
      })
    },
    handleEchartsData(data) {
      const mergeData = merger(data, 'YDATA')
      this.echartData = mergeData

      let xData = [],
        legend = [],
        seriesData = []
      const color = [
        '#ef4136',
        '#fcaf17',
        '#50b7c1',
        '#ea66a6',
        '#4e72b8',
        '#7d5886',
        '#8f4b4a',
        '#006c54',
        '#cbc547',
        '#fedcbd',
        '#ba8448',
        '#f3715c',
        '#9d9087',
        '#008792',
        '#cde6c7',
        '#f58220',
        '#65c294',
        '#454926',
        '#fcf16e',
        '#ca8687',
        '#afb4db',
        '#f7acbc',
        '#b7ba6b',
        '#d5c59f',
        '#d71345',
        '#90d7ec',
        '#224b8f',
        '#ffce7b',
        '#d3d7d4',
        '#ffd400'
      ]
      // 拿到所有不重复的 日期
      const dateArray = [...new Set(data.map((item) => item.XDATA))]
      xData = dateArray
      mergeData.forEach((item) => {
        const tempOrigin = []
        const seriesObj = {
          name: item.YDATA,
          type: 'line',
          symbol: 'none',
          smooth: true,
          lineStyle: {
            normal: {
              width: 0.5
            }
          },
          data: []
        }
        legend.push({ name: item.YDATA, icon: 'roundRect' })
        for (let i = 0; i < dateArray.length; i++) {
          const temp = dateArray[i]
          const objExample = {}
          objExample.XDATA = temp
          objExample.YDATA = item.YDATA
          const obj = item.origin.find((sitem) => sitem.XDATA == temp) || objExample
          tempOrigin.push(obj)
        }
        item.origin = tempOrigin
        seriesObj.data = item.origin.map((item) => item.YDATA1)
        seriesData.push(seriesObj)
      })
      this.investmentHistoryTgOption = {
        // toolbox: {
        //   show: true,
        //   right: '13px',
        //   top: '20px',
        //   feature: {
        //     dataZoom: {
        //       yAxisIndex: 'none',
        //       show: false
        //     },
        //     saveAsImage: {},
        //     dataView: {
        //       show: true,
        //       title: '表格数据',
        //       lang: ['表格数据：', '关闭', '导出Excel'],    // 按钮
        //       contentToOption: (opts) =>  {
        //         console.log(opt)
        //         this.export2Excel()
        //         table2excel('tableExcel_Day',{
        //           exclude: ".noExl", //过滤位置的 css 类名， 有class = “noExl” 的行不被导出
        //           filename: "历史收益走势对比.xls", // 文件名称
        //           name: "历史收益走势对比.xls",
        //           exclude_img: true,
        //           exclude_links: true,
        //           exclude_inputs: true
        //         })
        //       },
        //       // 数据视图展示为table
        //       optionToContent: function (opt) {
        //         var axisData = opt.xAxis[0].data; // 坐标数据
        //         var series = opt.series; //折线图数据，此处即为数据源，可以打印查看
        //         var tdHeads = '<td  style="padding: 0 10px">日期</td>'; //表头第一列
        //         var tdBodys = ''; //表数据
        //
        //         //组装表头
        //         var nameData = new Array();
        //         for (var k = 0; k < series.length; k++) {
        //           nameData.push(series[k].name)
        //         }
        //         for (var i = 0; i < nameData.length; i++) {
        //           tdHeads += '<td style="padding: 0 10px">' + nameData[i] + '</td>';
        //         }
        //         var table = '<table id="tableExcel_Day" border="1" class="table-bordered table-striped" style="width:100%;text-align:center" ><tbody><tr>' + tdHeads + ' </tr>';
        //         //组装表数据
        //         for (var i = 0; i < axisData.length; i++) {
        //           for (var j = 0; j < series.length; j++) {
        //             var temp = series[j].data[i];
        //             if (temp != null && temp != undefined) {
        //               tdBodys += '<td>' + temp + '</td>';
        //             } else {
        //               tdBodys += '<td></td>';
        //             }
        //           }
        //           table += '<tr><td style="padding: 0 10px">' + axisData[i] + '</td>' + tdBodys + '</tr>';
        //           tdBodys = '';
        //         }
        //         table += '</tbody></table>';
        //         return table;
        //       }
        //     }
        //   },
        // },
        tooltip: {
          trigger: 'axis',
          formatter: (params) => {
            if (params[0] && params[0].axisValueLabel) {
              this.activatedData = params[0].axisValueLabel
            } else {
              this.activatedData = '-'
            }
            let tip = params[0].name + '<br>'
            for (let i = 0; i < params.length; i++) {
              let value = ''
              if (params[i].value == undefined || params[i].value == '' || params[i].value == null || params[i].value == '--') {
                value = '--'
              } else {
                value = Number(params[i].value).toFixed(4)
              }
              tip += params[i].marker + params[i].seriesName + ': ' + value + '<br>'
            }
            return tip
          }
        },
        color: color,
        animation: false,
        legend: {
          top: '3%',
          data: legend,
          show: true,
          borderColor: '#FFF',
          itemGap: 20,
          textAlign: {
            fontsize: 16,
            align: 'center'
          }
        },
        grid: {
          top: '26%',
          bottom: '8%',
          containLabel: true
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
          name: '归一化净值',
          type: 'value',
          position: 'left',
          min: 'dataMin',
          axisLabel: {
            formatter: '{value}'
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
        dataZoom: [
          {
            brushSelect: false,
            bottom: '0',
            show: true
          }
        ],
        series: seriesData
      }
      for (let i = this.echartData.length - 1; i >= 0; i++) {
        let temp = this.echartData[i]
        for (let j = temp.origin.length - 1; j >= 0; j--) {
          let stemp = temp.origin[j]
          if (stemp.YDATA2 || stemp.YDATA5) {
            this.activatedData = stemp.XDATA
            return
          }
        }
      }
    },
    // 获取业绩分析上表格数据
    getIndustryDataUp() {
      let params = Object.assign({}, this.formQuery)
      params.baseCode = params.dbjz.toString()
      params.indexCode = '00f1b126-df77-4ed1-9947-59b0ebebb94a'
      params._pageFlag = false
      params.orderString=this.orderString2
      this.tableLoading2 = true
      commonApi
        .getDataBysqlCode(params)
        .then((res) => {
          const { status, data } = res.data
          if (status == 0) {
            if (data.length > 0) {
              let tempArray = []
              data.forEach((item) => {
                tempArray.push({
                  XDATE: item.XDATE,
                  YDATE: item.YDATE,
                  YDATE1: item.YDATE1,
                  YDATE2: item.YDATE2,
                  YDATE3: item.YDATE3,
                  YDATE4: item.YDATE4,
                  YDATE5: item.YDATE5,
                  YDATE6: item.YDATE6,
                  YDATE7: item.YDATE7,
                  YDATE8: item.YDATE8,
                  YDATE9: item.YDATE9,
                  YDATE10: item.YDATE10
                })
              })
              this.tableData2 = [...tempArray]
            } else {
              this.tableData2 = []
            }
            this.tableLoading2 = false
          } else {
            this.tableData2 = []
            this.tableLoading2 = false
          }
        })
        .catch((err) => {
          this.tableData2 = []
          this.tableLoading2 = false
        })
    }
  }
}
</script>
<style lang="scss" scoped>
.investment-history-tg {
  position: relative;
  margin: 0 30px;
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
  .titleBox {
    border-bottom: 1px solid #e03d3e;
    padding: 20px 0 10px;
    font-size: 16px;
    margin-bottom: 20px;
  }
  .title_name_icon {
    width: 2px;
    display: inline-block;
    height: 14px;
    line-height: 14px;
    background-color: #e03d3e;
    position: relative;
    top: 1px;
    margin-right: 10px;
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
    background-color: #e03d3e;
  }

  .title_name {
    height: 30px;
    line-height: 30px;
    color: #e03d3e;
    padding-left: 5px;
  }

  .chart-content {
    height: 400px;
    margin-top: 5px;

    .echarts_box {
      height: 100%;
      width: 100%;
    }
  }
}
</style>

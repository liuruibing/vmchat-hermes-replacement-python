<template>
  <div class="hotspot-fund">
    <el-card>
      <div slot="header" class="clearfix">
        <div class="card-header">
          <span class="title-name">热点产品</span>
          <span class="link-more" >More ></span>
<!--          临时停用点击事件-->
<!--          <span class="link-more" @click="jumpToPage">More ></span>-->
        </div>
      </div>
      <div class="content">
        <img src="@/assets/img/敬请期待.png" style="width: 100%; height: 100%;">
<!--        下方代码临时停用-->
<!--        <vxe-table :data="tableData" ref="fundTable" border="inner" max-height="288px" resizable auto-resize show-overflow>
          <vxe-table-column field="fundCode" title="产品代码" min-width="100" header-align="center" align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.fundCode | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column align="left" header-align="center" min-width="150" label="产品简称" field="fundName">
            <template slot-scope="scope">
              <span class="color_4f95dd fund_cell" @click="jumpToSingle(scope.row)">
                <span class="fund_name">
                  {{ scope.row.fundName | noDataFilter }}
                </span>
                <span v-if="scope.row.VC_SOURCE === 'IN'" style="margin-bottom: 0 !important">
                  <img :src="require('@/assets/img/CMS1.png')" height="14px" width="20px" />
                </span>
              </span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="createDate" title="近六月走势" min-width="100" header-align="center">
            <template slot-scope="scope">
              <myecharts
                :id="'hostpotFund' + scope.row.fundCode + scope.row.VC_SOURCE"
                :ref="'hostpotFund' + scope.row.fundCode + scope.row.VC_SOURCE"
                :options="scope.row.option"
                resize-dom="cmbfof"
                style="width: 100%; height: 20px"
              ></myecharts>
            </template>
          </vxe-table-column>
          <vxe-table-column field="strategyType" title="策略类型" min-width="100" header-align="center" align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.strategyType | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="yearRateReturn" title="今年收益" min-width="100" header-align="center" align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.yearRateReturn | numberToFixedStr(2, 100, '%') }}</span>
            </template>
          </vxe-table-column>
        </vxe-table>-->
      </div>
    </el-card>
  </div>
</template>

<script>
import commonApi from '@/api/common'
import { merger_back_objs } from '@/utils'
import myecharts from '@/components/Echarts'
export default {
  name: 'HotspotFund',
  components: {myecharts},
  data() {
    return {
      tableData: []
    }
  },
  methods: {
    initData() {
      this.getRecommendProducts()
    },
    /** 获取表格数据 */
    getRecommendProducts() {
      let params = {}
      params.indexCode = '95592cbd-0056-4d8d-9a40-1ee37170d4b2'
      params.rankType = 'XX'
      this.tableLoading = true
      commonApi.getDataBysqlCode(params).then((res) => {
        let { status, data } = res.data
        let tableArray = []
        let fundList = []
        if (status === 0) {
          for (let i = 0; i < data.length; i++) {
            let temp = data[i]
            let tableObj = {
              fundCode: temp.VC_FUNDCODE,
              fundName: temp.VC_FUNDNAME,
              monthRateReturn: temp.F_6M_RETURN || '',
              yearRateReturn: temp.F_YTD_RETURN || '',
              VC_SOURCE: temp.VC_SOURCE,
              strategyType: temp.DIM_NME,
              option: {}
            }
            fundList.push({
              fundCode: temp.VC_FUNDCODE,
              dimNme: temp.DIM_NME
            })
            tableArray.push(tableObj)
          }
          let paramsC = {}
          paramsC.indexCode = '2010917d-0cbe-469d-a7a2-4c984aadfa42'
          paramsC.fundList = fundList
          commonApi.getDataBysqlCode(paramsC).then((resC) => {
            let { status: statusC, data: dataC } = resC.data
            if (statusC === 0) {
              const mergeData = merger_back_objs(dataC, 'VC_FUNDCODE')
              tableArray.forEach((temp) => {
                let findObj = mergeData.find((item) => item.VC_FUNDCODE == temp.fundCode + temp.strategyType)
                if (findObj) {
                  if (temp.monthRateReturn > 0) {
                    this.setTableDataOption(findObj.origin, findObj.VC_FUNDCODE, ['#de777a'])
                  } else if (temp.monthRateReturn < 0) {
                    this.setTableDataOption(findObj.origin, findObj.VC_FUNDCODE, ['#81b59e'])
                  } else {
                    this.setTableDataOption(findObj.origin, findObj.VC_FUNDCODE, ['black'])
                  }
                }
              })
              console.log(tableArray)
              // 组装好之后放到原来的数组里面去
            } else {
            }
          })
          this.tableData = tableArray
        }
      })
    },
    /** 根据fundcode设置对应的option */
    setTableDataOption(data, fundCode, color) {
      const seriesData = data.map((item) => item.F_ADDED_NAV)
      const xData = data.map((item) => item.D_DATE)
      // 开始组装option
      let option = {
        color: color,
        legend: {
          textStyle: {
            fontSize: 12
          }
        },
        grid: {
          top: '2%',
          right: '2%',
          bottom: '4%',
          left: '4%'
        },
        xAxis: {
          show: false,
          type: 'category',
          boundaryGap: false, // 设置x轴两边的留白
          axisTick: {
            // x轴刻度尺
            show: false
          },
          axisLine: {
            // x轴线条颜色
            lineStyle: {
              color: '#999'
            }
          },
          data: xData
        },
        yAxis: {
          show: false,
          type: 'value',
          interval: 1, // 刻度值间隔值
          splitLine: {
            // 网格线
            show: false // 关闭网格线
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
            // y轴线条颜色
            show: true,
            lineStyle: {
              color: '#999'
            }
          }
        },
        series: [
          {
            data: seriesData,
            type: 'line',
            smooth: true, // 面积图改成弧形状
            showSymbol: false // 去除面积图节点圆
          }
        ]
      }

      for (let i = 0; i < this.tableData.length; i++) {
        const temp = this.tableData[i]
        if (temp.fundCode + temp.strategyType === fundCode) {
          temp.option = option
          break
        }
      }
    },
    /** 跳转热点产品 */
    jumpToPage() {
      this.$router.push('/hydt/smrd/cprd/XX')
    },
    /** 跳转单产品页面 */
    jumpToSingle(row) {
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/tqgl/dcpfx',
        query: { list: { fundCode: row.fundCode, source: row.source, fundName: row.fundName } }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
@import url('../../style/index.scss');

.hotspot-fund {
}
</style>

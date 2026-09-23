<template>
  <div class="my-focus">
    <el-card>
      <div slot="header" class="clearfix">
        <el-row class="card-header" type="flex" justify="space-around">
          <el-col :span="4">
            <span class="title-name">
              <span>我的关注</span>
            </span>
          </el-col>
          <el-col :span="20" style="text-align: right">
<!--            <span class="toogle-tab">
              <span
                v-for="tab in activeTabs"
                :key="tab.key"
                :class="tab.key === active ? 'tab-item-active ' : ''"
                class="tab-item"
                @click="toogleActive(tab.key)">
                {{ tab.name }}
              </span>
            </span>-->
            <span class="link-more" @click="jumpToPage">更多 ></span>
          </el-col>
        </el-row>
      </div>
      <div v-if="active !== 'manager'" class="content">
        <vxe-table
          ref="fundTable"
          :data="activeTableMap[active].tableData"
          border="inner"
          max-height="288px"
          resizable
          auto-resize
          show-overflow>
          <vxe-table-column
            v-for="col in activeTableMap[active].columns"
            :key="col.field"
            :field="col.field"
            :title="col.title"
            :min-width="col.minWidth"
            :header-align="col.headerAlign"
            :align="col.align"
          >
            <template slot-scope="scope">
              <span v-if="col.field === 'fundCode'" style="padding-left: 10px">
                {{ scope.row[col.field] | noDataFilter }}
              </span>
              <span v-else-if="active === 'fund' && col.field === 'fundName'" class="color_4f95dd fund_cell">
                <span class="fund_name">
                  <el-tooltip :content="scope.row[col.field] || '-'" effect="dark" placement="top">
                    <span @click="jumpToSingle(scope.row)">{{ scope.row[col.field] | noDataFilter }}</span>
                  </el-tooltip>
                </span>
<!--                <span v-if="scope.row.VC_FLAG == 'IN'" style="margin-bottom: 0 !important">
                  <img :src="require('@/assets/img/CMS1.png')" height="14px" width="20px"/>
                </span>-->
              </span>
              <span v-else-if="active === 'fund' && col.field === 'halfYeear'">
                <myecharts
                  :id="'thirdLine' + scope.row.fundCode + scope.row.VC_FLAG"
                  :ref="'thirdLine' + scope.row.fundCode + scope.row.VC_FLAG"
                  :options="scope.row.option"
                  resize-dom="cmbfof"
                  style="width: 100%; height: 20px"
                ></myecharts>
              </span>
              <span v-else-if="active === 'custodian' && col.field === 'managerShortName'" class="color_4f95dd fund_cell">
                <el-tooltip :content="scope.row[col.field] || '-'" effect="dark" placement="top">
                  <span @click="jumpToManagerWdgx(scope.row)">{{ scope.row[col.field] | noDataFilter }}</span>
                </el-tooltip>
              </span>
              <span v-else-if="active === 'fund' && col.field === 'yearRateReturn'">
                {{ scope.row[col.field] | numberToFixedStr(2, 100, '%') }}
              </span>
              <span v-else-if="active === 'custodian' && col.field === 'sixMonth'">
                <myecharts
                  :id="'thirdLine' + scope.row.fundCode + scope.row.VC_FLAG"
                  :ref="'thirdLine' + scope.row.fundCode + scope.row.VC_FLAG"
                  :options="scope.row.option"
                  resize-dom="cmbfof"
                  style="width: 100%; height: 20px"
                ></myecharts>
              </span>
              <span v-else-if="active === 'custodian' && col.field === 'f_ret_ytd'">
                {{ scope.row[col.field] | numberToFixedStr(2, 100, '%') }}
              </span>
              <span v-else>{{ scope.row[col.field] | noDataFilter }}</span>
            </template>
          </vxe-table-column>
        </vxe-table>
      </div>
      <div v-else class="content">
        <img src="@/assets/img/敬请期待.png" style="width: 100%; height: 100%;">
      </div>
    </el-card>
  </div>
</template>

<script>
import commonApi from '@/api/common'
import { merger_back_objs } from '@/utils'
import myecharts from '@/components/Echarts'

export default {
  name: 'MyFocus',
  components: { myecharts },
  data() {
    return {
      active: 'fund',
      activeTabs: [
        { key: 'fund', name: '产品' },
        { key: 'custodian', name: '管理人' },
        { key: 'manager', name: '经理' }
      ],
      activeTableMap: {
        fund: {
          columns: [
            {
              field: 'fundCode',
              title: '产品代码',
              minWidth: '80',
              headerAlign: 'center',
              align: 'left'
            },
            {
              field: 'fundName',
              title: '产品简称',
              minWidth: '200',
              headerAlign: 'center',
              align: 'left'
            },
            {
              field: 'halfYeear',
              title: '近六月走势',
              minWidth: '100',
              headerAlign: 'center',
              align: 'center'
            },
            {
              field: 'yearRateReturn',
              title: '今年收益',
              minWidth: '70',
              headerAlign: 'center',
              align: 'right'
            }
          ],
          tableData: []
        },
        custodian: {
          columns: [
            {
              field: 'regCode',
              title: '备案编号',
              minWidth: '100',
              headerAlign: 'center',
              align: 'center'
            },
            {
              field: 'managerShortName',
              title: '管理人简称',
              minWidth: '100',
              headerAlign: 'center',
              align: 'center'
            },
            {
              field: 'sixMonth',
              title: '近六月走势',
              minWidth: '100',
              headerAlign: 'center',
              align: 'center'
            },
            {
              field: 'f_ret_ytd',
              title: '今年收益',
              minWidth: '100',
              headerAlign: 'center',
              align: 'center'
            }
          ],
          tableData: []
        },
        manager: {
          columns: [
            {
              field: 'YAXISDATA1',
              title: '经理名称',
              minWidth: '100',
              headerAlign: 'center',
              align: 'center'
            },
            {
              field: 'YAXISDATA2',
              title: '近六月走势',
              minWidth: '100',
              headerAlign: 'center',
              align: 'center'
            },
            {
              field: 'YAXISDATA3',
              title: '策略类型',
              minWidth: '100',
              headerAlign: 'center',
              align: 'center'
            },
            {
              field: 'YAXISDATA4',
              title: '今年收益',
              minWidth: '100',
              headerAlign: 'center',
              align: 'right'
            }
          ],
          tableData: []
        }
      }
    }
  },
  methods: {
    initData() {
      this.getFocusProductData()
      //this.getFocusCustodianData()
      //this.getFocusManagerData()
    },
    toogleActive(val) {
      this.active = val
    },
    // 获取推荐产品的数据
    getFocusProductData() {
      const params = {}
      params.indexCode = 'f64c7969-6778-47c5-8acb-04b360e1bc55'
      commonApi.getDataBysqlCode(params).then((res) => {
        const { status, data } = res.data
        const tableArray = [] // 组装tableData数据
        const fundList = []
        if (status === 0) {
          for (let i = 0; i < data.length; i++) {
            const temp = data[i]
            // 同步获取对应的series Data数据，用于组装
            const tableObj = {
              fundCode: temp.VC_FUNDCODE,
              fundName: temp.VC_FUNDNAME,
              monthRateReturn: temp.F_6M_RETURN || '',
              yearRateReturn: temp.F_YTD_RETURN || '',
              option: {},
              VC_IS_VERIFY: temp.VC_IS_VERIFY,
              VC_FLAG: temp.VC_FLAG
            }
            fundList.push({
              fundCode: temp.VC_FUNDCODE,
              source: temp.VC_FLAG
            })
            tableArray.push(tableObj)
          }
          const paramsC = {}
          paramsC.indexCode = 'ca898302-3999-47fc-9670-5b9929e87b6f'
          paramsC.fundList = fundList
          // paramsC.indexCode = 'a50f06a4-bfa6-4858-9c38-a1d0f57e5a51'
          // paramsC.fundCodes = fundCodes.join(',')
          commonApi.getDataBysqlCode(paramsC).then((resC) => {
            const { status: statusC, data: dataC } = resC.data
            if (statusC === 0) {
              const mergeData = merger_back_objs(dataC, 'VC_FUNDCODE')
              tableArray.forEach((temp) => {
                const findObj = mergeData.find((item) => item.VC_FUNDCODE == temp.fundCode + temp.VC_FLAG)
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
              // 组装好之后放到原来的数组里面去
            } else {
            }
          })
          this.activeTableMap['fund'].tableData = tableArray
        }
      })
    },
    // 根据fundcode设置对应的option
    setTableDataOption(data, fundCode, color) {
      const seriesData = data.map((item) => item.F_ADDED_NAV)
      const xData = data.map((item) => item.D_DATE)
      // 开始组装option
      const option = {
        color: color,
        grid: {
          // 设置图表四周留白间距
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
          min: function(value) {
            if (value.min < 0) {
              return value.min * 1.1
            } else {
              return value.min
            }
          },
          max: function(value) {
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

      for (let i = 0; i < this.activeTableMap['fund'].tableData.length; i++) {
        const temp = this.activeTableMap['fund'].tableData[i]
        if (temp.fundCode + temp.VC_FLAG === fundCode) {
          temp.option = option
          break
        }
      }
    },
    // 获取推荐管理人数据
    getFocusCustodianData() {
      const params = {}
      params.indexCode = '089b3d29-f0f3-4927-9edd-d0fb03c45682'
      commonApi.getDataBysqlCode(params).then((res) => {
        const { status, data } = res.data
        const tableArray = [] // 组装tableData数据
        const mgrcodes = []
        if (status === 0) {
          for (let i = 0; i < data.length; i++) {
            const temp = data[i]
            // 同步获取对应的series Data数据，用于组装
            const tableObj = {
              regCode: temp.REG_CODE,
              companyid: temp.COMPANY_ID,
              managerShortName: temp.COMPANY_SHORT_NAME,
              f_ret_6m: temp.F_RET_6M || '',
              f_ret_ytd: temp.F_RET_YTD || '',
              option: {}
            }
            tableArray.push(tableObj)
            mgrcodes.push(temp.COMPANY_ID)
          }
          const paramsC = {}
          paramsC.indexCode = 'c4441b43-8bed-4a26-9206-c8ecdb5bfa96'
          paramsC.mgrcodes = mgrcodes.join(',')
          commonApi.getDataBysqlCode(paramsC).then((resC) => {
            const { status: statusC, data: dataC } = resC.data
            if (statusC === 0) {
              const mergeData = merger_back_objs(dataC, 'COMPANY_ID')
              tableArray.forEach((temp) => {
                const findObj = mergeData.find((item) => item.COMPANY_ID == temp.companyid)
                if (findObj) {
                  if (temp.f_ret_6m > 0) {
                    this.setManangerTableDataOption(findObj.origin, findObj.COMPANY_ID, ['#de777a'])
                  } else if (temp.f_ret_6m < 0) {
                    this.setManangerTableDataOption(findObj.origin, findObj.COMPANY_ID, ['#81b59e'])
                  } else {
                    this.setManangerTableDataOption(findObj.origin, findObj.COMPANY_ID, ['black'])
                  }
                }
              })
              // 组装好之后放到原来的数组里面去
            } else {
            }
          })
          this.activeTableMap['custodian'].tableData = tableArray
        }
      })
    },
    // 根据companyid设置对应的option
    setManangerTableDataOption(data, companyid, color) {
      const seriesData = data.map((item) => item.F_CURVE_NAV)
      const xData = data.map((item) => item.D_END_DATE)
      // 开始组装option
      const option = {
        color: color,
        grid: {
          // 设置图表四周留白间距
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
          min: function(value) {
            if (value.min < 0) {
              return value.min * 1.1
            } else {
              return value.min
            }
          },
          max: function(value) {
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

      for (let i = 0; i < this.activeTableMap['custodian'].tableData.length; i++) {
        const temp = this.activeTableMap['custodian'].tableData[i]
        if (temp.companyid === companyid) {
          temp.option = option
          break
        }
      }
    },
    getFocusManagerData() {
      const params = {}
      params.indexCode = '25fdc482-d89a-4b71-a8d3-6b847f90f2dd'
      commonApi.getDataBysqlCode(params).then((res) => {
        const { status, data } = res.data
        if (status === 0) {
          this.activeTableMap['manager'].tableData = data
        }
      })
    },
    jumpToSingle(row) {
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/tqgl/dcpfx',
        query: { list: { fundCode: row.fundCode, source: row.source, fundName: row.fundName }}
      })
    },
    jumpToManagerWdgx(row) {
      row.company_id =row.companyid
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/tqgl/glrxq',
        query: { managerList: row }
      })
    },
    jumpToPage() {
      if (this.active === 'fund') {
        this.$store.commit('SET_FROMPAGEJUMP', true)
        this.$router.push({
          path: '/tqgl/wdgz/wdgz',
          query: {
            name: 'smcp'
          }
        })
      } else if (this.active === 'custodian') {
        this.$store.commit('SET_FROMPAGEJUMP', true)
        this.$router.push({
          path: '/tqgl/wdgz/wdgz',
          query: {
            name: 'smglr'
          }
        })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
@import url('../../style/index.scss');

.toogle-tab {
  //margin-left: 130px;
}
</style>

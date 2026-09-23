<template>
  <el-row :gutter="20">
    <el-col :span="8">
      <box-template1>
        <template slot="title">
          <div class="title-content rdcp">
            <div class="title">
              <el-row>
                <el-col :span="22">
                  <span class="titletitle" style="margin-right: 8px">私募热点</span>
                  <span
                    v-for="(item, index) of hotProductArr"
                    :key="index"
                    :class="[
                      index == 0 ? 'title-button-left-rdcp' : '',
                      index == hotProductArr.length - 1 ? 'title-button-right-rdcp' : '',
                      index != 0 && index != hotProductArr.length - 1 ? 'title-button-center-rdcp' : '',
                      'pointer',
                      isActive1 === item.value ? 'button-active' : ''
                    ]"
                    @click="handleButtonClick1(item.value, item)"
                  >
                    {{ item.label }}
                  </span>
                </el-col>
                <el-col :span="2">
                  <div class="search_button_com">
                    <span style="font-size: 14px">
                      <el-link :underline="false" type="primary" @click="handleHotProductMoreClick">
                        <span class="elLink">{{ moreStr }}</span>
                      </el-link>
                    </span>
                  </div>
                </el-col>
              </el-row>
            </div>
          </div>
        </template>
        <template slot="content">
          <div style="height: 340px; overflow: hidden" @mouseenter="showOverFlow1 = true" @mouseleave="showOverFlow1 = false" :class="{ tableOverflow: showOverFlow1 === true }">
            <div style="position: relative; width: 100%">
              <div class="blur" v-show="isActive1 !== 'XX'" style="height: 340px; width: 100%">
                <div class="blur-div" :style="{ backgroundImage: 'url(' + frostedGlassPageBg + ')' }">
                  <el-container>
                    <el-aside width="23px">
                      <img width="23px" :src="require('@/assets/img/frostedGlassLogo.png')" />
                    </el-aside>
                    <el-main style="text-align: left; line-height: 24px; padding-left: 5px !important; font-size: 14px" v-html="frostedStr"></el-main>
                  </el-container>
                </div>
              </div>
              <el-table ref="tableData3" :data="tableData3" align="center" header-row-class-name="" height="340px" @cell-click="jumpToSingle">
                <el-table-column header-align="center" label="产品代码" prop="fundCode" show-overflow-tooltip>
                  <template slot-scope="scope">
                    <span>{{ scope.row.fundCode | noDataFilter }}</span>
                  </template>
                </el-table-column>
                <el-table-column align="left" header-align="center" label="产品简称" prop="fundName" show-overflow-tooltip>
                  <template slot-scope="scope">
                    <span class="color_4f95dd fund_cell">
                      <span class="fund_name">
                        {{ scope.row.fundName | noDataFilter }}
                      </span>
                      <span v-if="scope.row.VC_SOURCE === 'IN'" style="margin-bottom: 0 !important">
                        <img :src="require('@/assets/img/CMS1.png')" height="14px" width="20px" />
                      </span>
                    </span>
                  </template>
                </el-table-column>
                <el-table-column align="center" header-align="center" label="近三月走势" prop="halfYeear">
                  <template slot-scope="scope">
                    <myChart
                      :id="'secondline' + scope.row.fundCode + scope.row.strategyType"
                      :ref="'secondline' + scope.row.fundCode + scope.row.strategyType"
                      :options="scope.row.option"
                      resize-dom="cmbfof"
                      style="width: 100%; height: 19px"
                    ></myChart>
                  </template>
                </el-table-column>
                <el-table-column align="center" header-align="center" label="策略类型" prop="strategyType" show-overflow-tooltip>
                  <template slot-scope="scope">
                    <span>{{ scope.row.strategyType | noDataFilter }}</span>
                  </template>
                </el-table-column>
                <el-table-column align="center" header-align="center" label="今年收益" prop="yearRateReturn" show-overflow-tooltip width="80">
                  <template slot-scope="scope">
                    {{ scope.row.yearRateReturn | numberToFixedStr(2, 100, '%') }}
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </div>
        </template>
      </box-template1>
      <div style="border-bottom: 1px solid #333333"></div>
    </el-col>
    <el-col :span="8" class="wdgz">
      <box-template>
        <template slot="title">
          <div class="title">
            <el-row type="flex">
              <el-col :span="22">
                <span class="titletitle">我的关注</span>
                <span :class="['title-button-left2', 'pointer', isActive2 === '产品' ? 'button-active' : '']" @click="handleButtonClick2('产品')">产 品</span>
                <span :class="['title-button-right2', 'pointer', isActive2 === '管理人' ? 'button-active' : '']" @click="handleButtonClick2('管理人')">管理人</span>
              </el-col>
              <el-col :span="2">
                <div class="search_button_com">
                  <span style="font-size: 14px">
                    <el-link :underline="false" type="primary" @click="handleMyFocus">
                      <span class="elLink">{{ moreStr }}</span>
                    </el-link>
                  </span>
                </div>
              </el-col>
            </el-row>
          </div>
        </template>
        <template slot="content">
          <div :class="{ tableOverflow: showOverFlow === true }" style="height: 340px; overflow: hidden" @mouseenter="showOverFlow = true" @mouseleave="showOverFlow = false">
            <el-table v-if="tabIndex === 1" :data="tableData1" align="center" height="340px" @cell-click="jumpToSingle">
              <el-table-column header-align="center" label="产品代码" prop="fundCode" show-overflow-tooltip>
                <template slot-scope="scope">
                  <span style="font-size: 14px">
                    {{ scope.row.fundCode | noDataFilter }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column align="left" header-align="center" label="产品简称" prop="fundName">
                <template slot-scope="scope">
                  <span class="color_4f95dd fund_cell">
                    <span class="fund_name">
                      <el-tooltip :content="scope.row.fundName || '-'" effect="dark" placement="top">
                        <span>{{ scope.row.fundName | noDataFilter }}</span>
                      </el-tooltip>
                    </span>
                    <span v-if="scope.row.VC_FLAG == 'IN'" style="margin-bottom: 0 !important">
                      <img :src="require('@/assets/img/CMS1.png')" height="14px" width="20px" />
                    </span>
                    <!--                    <img v-if="scope.row.VC_IS_VERIFY == 1" src="@/assets/img/已验证.png" @click="jumpPage2(scope.row)" />-->
                    <!--                    <img v-if="scope.row.VC_IS_VERIFY == 0" src="@/assets/img/验证中.png" @click="jumpPage2(scope.row)" />-->
                  </span>
                </template>
              </el-table-column>
              <el-table-column align="center" header-align="center" label="近三月走势" prop="halfYeear">
                <template slot-scope="scope">
                  <myecharts
                    :id="'thirdLine' + scope.row.fundCode + scope.row.VC_FLAG"
                    :ref="'thirdLine' + scope.row.fundCode + scope.row.VC_FLAG"
                    :options="scope.row.option"
                    resize-dom="cmbfof"
                    style="width: 100%; height: 20px"
                  ></myecharts>
                </template>
              </el-table-column>
              <el-table-column align="right" header-align="center" label="近三月收益率" prop="monthRateReturn" show-overflow-tooltip>
                <template slot-scope="scope">
                  <span v-if="scope.row.monthRateReturn > 0" style="color: #de777a">
                    {{ scope.row.monthRateReturn | numberToFixedStr(2, 100, '%') }}
                    <svg-icon class-name="icon-style-arrow" icon-class="upArrowHead"></svg-icon>
                  </span>
                  <span v-else-if="scope.row.monthRateReturn == 0">
                    {{ scope.row.monthRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                  <span v-else style="color: #81b59e">
                    {{ scope.row.monthRateReturn | numberToFixedStr(2, 100, '%') }}
                    <svg-icon class-name="icon-style-arrow" icon-class="downArrowHead"></svg-icon>
                  </span>
                </template>
              </el-table-column>
              <el-table-column align="center" header-align="center" label="今年收益" prop="yearRateReturn" show-overflow-tooltip width="80">
                <template slot-scope="scope">
                  <span>
                    {{ scope.row.yearRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                </template>
              </el-table-column>
            </el-table>
            <el-table v-if="tabIndex === 2" :data="tableData2" align="center" height="340px" @cell-click="jumpToManagerWdgx">
              <el-table-column header-align="center" label="备案编号" prop="regCode" show-overflow-tooltip>
                <template slot-scope="scope">
                  <span style="font-size: 14px">
                    {{ scope.row.regCode | noDataFilter }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column align="left" header-align="center" label="管理人简称" prop="managerShortName" show-overflow-tooltip>
                <template slot-scope="scope">
                  <el-link :underline="false" style="font-size: 14px" type="primary">
                    <span class="elLink" style="font-size: 14px">
                      <el-tooltip :content="scope.row.managerShortName || '-'" effect="dark" placement="top">
                        <span>{{ scope.row.managerShortName | noDataFilter }}</span>
                      </el-tooltip>
                    </span>
                  </el-link>
                </template>
              </el-table-column>
              <el-table-column align="center" header-align="center" label="近六月走势" prop="">
                <template slot-scope="scope">
                  <myecharts
                    :id="`managerEchart` + scope.row.companyid"
                    :ref="`managerEchart` + scope.row.companyid"
                    :options="scope.row.option"
                    resize-dom="cmbfof"
                    style="width: 100%; height: 20px"
                  ></myecharts>
                </template>
              </el-table-column>
              <el-table-column align="right" header-align="center" label="近六月收益率" prop="f_ret_6m" show-overflow-tooltip>
                <template slot-scope="scope">
                  <span>
                    <span v-if="scope.row.f_ret_6m > 0" style="color: #de777a">
                      {{ scope.row.f_ret_6m | numberToFixedStr(2, 100, '%') }}
                      <svg-icon class-name="icon-style-arrow" icon-class="upArrowHead"></svg-icon>
                    </span>
                    <span v-else-if="scope.row.f_ret_6m == 0">
                      {{ scope.row.f_ret_6m | numberToFixedStr(2, 100, '%') }}
                    </span>
                    <span v-else style="color: #81b59e">
                      {{ scope.row.f_ret_6m | numberToFixedStr(2, 100, '%') }}
                      <svg-icon class-name="icon-style-arrow" icon-class="downArrowHead"></svg-icon>
                    </span>
                  </span>
                </template>
              </el-table-column>
              <el-table-column align="center" header-align="center" label="今年收益" prop="f_ret_ytd" show-overflow-tooltip width="80">
                <template slot-scope="scope">
                  <span>
                    {{ scope.row.f_ret_ytd | numberToFixedStr(2, 100, '%') }}
                  </span>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </template>
      </box-template>
      <div style="border-bottom: 1px solid #333333"></div>
    </el-col>
    <el-col :span="8">
      <bygclsybx />
    </el-col>
  </el-row>
</template>
<script>
import shichangdongtai from './shichangdongtai'
import jnylfcljjjzzs from './jnylfcljjjzzs'
import myecharts from '@/components/Echarts'
import boxTemplate from './boxTemplate'
import bygclsybx from './bygclsybx'
import commonApi from '@/api/common'
import fun from '@/filters/common'
import img from '@/assets/img/nullData.png'
import myChart from '@/components/myEcharts'
import boxTemplate1 from './boxTemplate1'

import { merger_back_objs } from '@/utils'
import frostedGlassPageBg from '@/assets/img/frostedGlassPageBG.png'

export default {
  components: {
    shichangdongtai,
    jnylfcljjjzzs,
    myecharts,
    boxTemplate,
    bygclsybx,
    boxTemplate1,
    myChart
  },
  data() {
    return {
      frostedGlassPageBg: frostedGlassPageBg,
      active1Item: '',
      frostedStr: '',
      isActive1: 'XX',
      hotProductArr: [],
      showOverFlow1: false,
      showOverFlow: false,
      moreStr: 'More>',
      imgUrl: img,
      isActive2: '产品',
      combArrays: [
        // [
        //   {
        //     src: 'second1.png',
        //     id: 1,
        //     title: '银德1期',
        //     profitAndLoss: 355.96,
        //     income: -0.0137,
        //     rateReturn: -0.0228,
        //     maxDraw: 0.0455,
        //     operateDay: 251,
        //     echartsData: [1, 2, 3, 4, 5],
        //     divider: true,
        //     option: {
        //       grid: {
        //         // 设置图表四周留白间距
        //         top: '2%',
        //         right: '2%',
        //         bottom: '4%',
        //         left: '4%'
        //       },
        //       xAxis: {
        //         show: false,
        //         type: 'category',
        //         boundaryGap: false, // 设置x轴两边的留白
        //         axisTick: {
        //           // x轴刻度尺
        //           show: false
        //         },
        //         axisLine: {
        //           // x轴线条颜色
        //           lineStyle: {
        //             color: '#999'
        //           }
        //         },
        //         data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        //       },
        //       yAxis: {
        //         min: function (value) {
        //           if (value.min < 0) {
        //             return value.min * 1.1
        //           } else {
        //             return value.min
        //           }
        //         },
        //         max: function (value) {
        //           if (value.max > 0) {
        //             return value.max
        //           } else {
        //             return value.max * 0.9
        //           }
        //         },
        //         show: false,
        //         type: 'value',
        //         interval: 1, // 刻度值间隔值
        //         splitLine: {
        //           // 网格线
        //           show: false // 关闭网格线
        //         },
        //         axisLine: {
        //           // y轴线条颜色
        //           show: true,
        //           lineStyle: {
        //             color: '#999'
        //           }
        //         }
        //       },
        //       series: [
        //         {
        //           data: [100, 97, 98, 99, 97.63],
        //           type: 'line',
        //           smooth: true, // 面积图改成弧形状
        //           lineStyle: {
        //             width: 1, // 外边线宽度
        //             color: '#42b1ff' // 外边线颜色
        //           },
        //           showSymbol: false, // 去除面积图节点圆
        //           areaStyle: {
        //             // 区域填充渐变颜色
        //             color: {
        //               type: 'linear',
        //               x: 0,
        //               y: 0,
        //               x2: 0,
        //               y2: 1,
        //               colorStops: [
        //                 {
        //                   offset: 0,
        //                   color: '#e8f3fc' // 0% 处的颜色
        //                 },
        //                 {
        //                   offset: 1,
        //                   color: '#f8fbff' // 100% 处的颜色
        //                 }
        //               ],
        //               global: false // 缺省为 false
        //             }
        //           }
        //         }
        //       ]
        //     }
        //   },
        //   {
        //     src: 'second2.png',
        //     id: 2,
        //     title: '申尊价值1号',
        //     profitAndLoss: 745.07,
        //     income: 0.0198,
        //     rateReturn: 0.0432,
        //     maxDraw: 0.0437,
        //     operateDay: 157,
        //     echartsData: [1, 2, 3, 4, 5],
        //     divider: true,
        //     option: {
        //       grid: {
        //         // 设置图表四周留白间距
        //         top: '2%',
        //         right: '2%',
        //         bottom: '4%',
        //         left: '4%'
        //       },
        //       xAxis: {
        //         show: false,
        //         type: 'category',
        //         boundaryGap: false, // 设置x轴两边的留白
        //         axisTick: {
        //           // x轴刻度尺
        //           show: false
        //         },
        //         axisLine: {
        //           // x轴线条颜色
        //           lineStyle: {
        //             color: '#999'
        //           }
        //         },
        //         data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        //       },
        //       yAxis: {
        //         min: function (value) {
        //           if (value.min < 0) {
        //             return value.min * 1.1
        //           } else {
        //             return value.min
        //           }
        //         },
        //         max: function (value) {
        //           if (value.max > 0) {
        //             return value.max
        //           } else {
        //             return value.max * 0.9
        //           }
        //         },
        //         show: false,
        //         type: 'value',
        //         interval: 1, // 刻度值间隔值
        //         splitLine: {
        //           // 网格线
        //           show: false // 关闭网格线
        //         },
        //         axisLine: {
        //           // y轴线条颜色
        //           show: true,
        //           lineStyle: {
        //             color: '#999'
        //           }
        //         }
        //       },
        //       series: [
        //         {
        //           data: [100, 97, 98, 99, 101.6],
        //           type: 'line',
        //           smooth: true, // 面积图改成弧形状
        //           lineStyle: {
        //             width: 1, // 外边线宽度
        //             color: '#42b1ff' // 外边线颜色
        //           },
        //           showSymbol: false, // 去除面积图节点圆
        //           areaStyle: {
        //             // 区域填充渐变颜色
        //             color: {
        //               type: 'linear',
        //               x: 0,
        //               y: 0,
        //               x2: 0,
        //               y2: 1,
        //               colorStops: [
        //                 {
        //                   offset: 0,
        //                   color: '#e8f3fc' // 0% 处的颜色
        //                 },
        //                 {
        //                   offset: 1,
        //                   color: '#f8fbff' // 100% 处的颜色
        //                 }
        //               ],
        //               global: false // 缺省为 false
        //             }
        //           }
        //         }
        //       ]
        //     }
        //   },
        //   {
        //     src: 'second3.png',
        //     id: 3,
        //     title: '赢康丰盈三号',
        //     profitAndLoss: 230.67,
        //     income: 0.0102,
        //     rateReturn: 0.0317,
        //     maxDraw: 0.0167,
        //     operateDay: 422,
        //     echartsData: [1, 2, 3, 4, 5],
        //     divider: false,
        //     option: {
        //       grid: {
        //         // 设置图表四周留白间距
        //         top: '2%',
        //         right: '2%',
        //         bottom: '4%',
        //         left: '4%'
        //       },
        //       xAxis: {
        //         show: false,
        //         type: 'category',
        //         boundaryGap: false, // 设置x轴两边的留白
        //         axisTick: {
        //           // x轴刻度尺
        //           show: false
        //         },
        //         axisLine: {
        //           // x轴线条颜色
        //           lineStyle: {
        //             color: '#999'
        //           }
        //         },
        //         data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        //       },
        //       yAxis: {
        //         show: false,
        //         type: 'value',
        //         interval: 1, // 刻度值间隔值
        //         splitLine: {
        //           // 网格线
        //           show: false // 关闭网格线
        //         },
        //         min: function (value) {
        //           if (value.min < 0) {
        //             return value.min * 1.1
        //           } else {
        //             return value.min
        //           }
        //         },
        //         max: function (value) {
        //           if (value.max > 0) {
        //             return value.max
        //           } else {
        //             return value.max * 0.9
        //           }
        //         },
        //         axisLine: {
        //           // y轴线条颜色
        //           show: true,
        //           lineStyle: {
        //             color: '#999'
        //           }
        //         }
        //       },
        //       series: [
        //         {
        //           data: [100, 95, 93, 98, 101.98],
        //           type: 'line',
        //           smooth: true, // 面积图改成弧形状
        //           lineStyle: {
        //             width: 1, // 外边线宽度
        //             color: '#42b1ff' // 外边线颜色
        //           },
        //           showSymbol: false, // 去除面积图节点圆
        //           areaStyle: {
        //             // 区域填充渐变颜色
        //             color: {
        //               type: 'linear',
        //               x: 0,
        //               y: 0,
        //               x2: 0,
        //               y2: 1,
        //               colorStops: [
        //                 {
        //                   offset: 0,
        //                   color: '#e8f3fc' // 0% 处的颜色
        //                 },
        //                 {
        //                   offset: 1,
        //                   color: '#f8fbff' // 100% 处的颜色
        //                 }
        //               ],
        //               global: false // 缺省为 false
        //             }
        //           }
        //         }
        //       ]
        //     }
        //   }
        // ],
        // [
        //   {
        //     src: 'second1.png',
        //     id: 1,
        //     title: '银德2期',
        //     profitAndLoss: 355.96,
        //     income: -0.0137,
        //     rateReturn: -0.0228,
        //     maxDraw: 0.0455,
        //     operateDay: 251,
        //     echartsData: [1, 2, 3, 4, 5],
        //     divider: true,
        //     option: {
        //       grid: {
        //         // 设置图表四周留白间距
        //         top: '2%',
        //         right: '2%',
        //         bottom: '4%',
        //         left: '4%'
        //       },
        //       xAxis: {
        //         show: false,
        //         type: 'category',
        //         boundaryGap: false, // 设置x轴两边的留白
        //         axisTick: {
        //           // x轴刻度尺
        //           show: false
        //         },
        //         axisLine: {
        //           // x轴线条颜色
        //           lineStyle: {
        //             color: '#999'
        //           }
        //         },
        //         data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        //       },
        //       yAxis: {
        //         min: function (value) {
        //           if (value.min < 0) {
        //             return value.min * 1.1
        //           } else {
        //             return value.min
        //           }
        //         },
        //         max: function (value) {
        //           if (value.max > 0) {
        //             return value.max
        //           } else {
        //             return value.max * 0.9
        //           }
        //         },
        //         show: false,
        //         type: 'value',
        //         interval: 1, // 刻度值间隔值
        //         splitLine: {
        //           // 网格线
        //           show: false // 关闭网格线
        //         },
        //         axisLine: {
        //           // y轴线条颜色
        //           show: true,
        //           lineStyle: {
        //             color: '#999'
        //           }
        //         }
        //       },
        //       series: [
        //         {
        //           data: [100, 97, 98, 99, 97.63],
        //           type: 'line',
        //           smooth: true, // 面积图改成弧形状
        //           lineStyle: {
        //             width: 1, // 外边线宽度
        //             color: '#42b1ff' // 外边线颜色
        //           },
        //           showSymbol: false, // 去除面积图节点圆
        //           areaStyle: {
        //             // 区域填充渐变颜色
        //             color: {
        //               type: 'linear',
        //               x: 0,
        //               y: 0,
        //               x2: 0,
        //               y2: 1,
        //               colorStops: [
        //                 {
        //                   offset: 0,
        //                   color: '#e8f3fc' // 0% 处的颜色
        //                 },
        //                 {
        //                   offset: 1,
        //                   color: '#f8fbff' // 100% 处的颜色
        //                 }
        //               ],
        //               global: false // 缺省为 false
        //             }
        //           }
        //         }
        //       ]
        //     }
        //   },
        //   {
        //     src: 'second2.png',
        //     id: 2,
        //     title: '申尊价值2号',
        //     profitAndLoss: 745.07,
        //     income: 0.0198,
        //     rateReturn: 0.0432,
        //     maxDraw: 0.0437,
        //     operateDay: 157,
        //     echartsData: [1, 2, 3, 4, 5],
        //     divider: true,
        //     option: {
        //       grid: {
        //         // 设置图表四周留白间距
        //         top: '2%',
        //         right: '2%',
        //         bottom: '4%',
        //         left: '4%'
        //       },
        //       xAxis: {
        //         show: false,
        //         type: 'category',
        //         boundaryGap: false, // 设置x轴两边的留白
        //         axisTick: {
        //           // x轴刻度尺
        //           show: false
        //         },
        //         axisLine: {
        //           // x轴线条颜色
        //           lineStyle: {
        //             color: '#999'
        //           }
        //         },
        //         data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        //       },
        //       yAxis: {
        //         min: function (value) {
        //           if (value.min < 0) {
        //             return value.min * 1.1
        //           } else {
        //             return value.min
        //           }
        //         },
        //         max: function (value) {
        //           if (value.max > 0) {
        //             return value.max
        //           } else {
        //             return value.max * 0.9
        //           }
        //         },
        //         show: false,
        //         type: 'value',
        //         interval: 1, // 刻度值间隔值
        //         splitLine: {
        //           // 网格线
        //           show: false // 关闭网格线
        //         },
        //         axisLine: {
        //           // y轴线条颜色
        //           show: true,
        //           lineStyle: {
        //             color: '#999'
        //           }
        //         }
        //       },
        //       series: [
        //         {
        //           data: [100, 97, 98, 99, 101.6],
        //           type: 'line',
        //           smooth: true, // 面积图改成弧形状
        //           lineStyle: {
        //             width: 1, // 外边线宽度
        //             color: '#42b1ff' // 外边线颜色
        //           },
        //           showSymbol: false, // 去除面积图节点圆
        //           areaStyle: {
        //             // 区域填充渐变颜色
        //             color: {
        //               type: 'linear',
        //               x: 0,
        //               y: 0,
        //               x2: 0,
        //               y2: 1,
        //               colorStops: [
        //                 {
        //                   offset: 0,
        //                   color: '#e8f3fc' // 0% 处的颜色
        //                 },
        //                 {
        //                   offset: 1,
        //                   color: '#f8fbff' // 100% 处的颜色
        //                 }
        //               ],
        //               global: false // 缺省为 false
        //             }
        //           }
        //         }
        //       ]
        //     }
        //   },
        //   {
        //     src: 'second3.png',
        //     id: 3,
        //     title: '赢康丰盈二号',
        //     profitAndLoss: 230.67,
        //     income: 0.0102,
        //     rateReturn: 0.0317,
        //     maxDraw: 0.0167,
        //     operateDay: 422,
        //     echartsData: [1, 2, 3, 4, 5],
        //     divider: false,
        //     option: {
        //       grid: {
        //         // 设置图表四周留白间距
        //         top: '2%',
        //         right: '2%',
        //         bottom: '4%',
        //         left: '4%'
        //       },
        //       xAxis: {
        //         show: false,
        //         type: 'category',
        //         boundaryGap: false, // 设置x轴两边的留白
        //         axisTick: {
        //           // x轴刻度尺
        //           show: false
        //         },
        //         axisLine: {
        //           // x轴线条颜色
        //           lineStyle: {
        //             color: '#999'
        //           }
        //         },
        //         data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        //       },
        //       yAxis: {
        //         show: false,
        //         type: 'value',
        //         interval: 1, // 刻度值间隔值
        //         splitLine: {
        //           // 网格线
        //           show: false // 关闭网格线
        //         },
        //         min: function (value) {
        //           if (value.min < 0) {
        //             return value.min * 1.1
        //           } else {
        //             return value.min
        //           }
        //         },
        //         max: function (value) {
        //           if (value.max > 0) {
        //             return value.max
        //           } else {
        //             return value.max * 0.9
        //           }
        //         },
        //         axisLine: {
        //           // y轴线条颜色
        //           show: true,
        //           lineStyle: {
        //             color: '#999'
        //           }
        //         }
        //       },
        //       series: [
        //         {
        //           data: [100, 95, 93, 98, 101.98],
        //           type: 'line',
        //           smooth: true, // 面积图改成弧形状
        //           lineStyle: {
        //             width: 1, // 外边线宽度
        //             color: '#42b1ff' // 外边线颜色
        //           },
        //           showSymbol: false, // 去除面积图节点圆
        //           areaStyle: {
        //             // 区域填充渐变颜色
        //             color: {
        //               type: 'linear',
        //               x: 0,
        //               y: 0,
        //               x2: 0,
        //               y2: 1,
        //               colorStops: [
        //                 {
        //                   offset: 0,
        //                   color: '#e8f3fc' // 0% 处的颜色
        //                 },
        //                 {
        //                   offset: 1,
        //                   color: '#f8fbff' // 100% 处的颜色
        //                 }
        //               ],
        //               global: false // 缺省为 false
        //             }
        //           }
        //         }
        //       ]
        //     }
        //   }
        // ],
        // [
        //   {
        //     src: 'second1.png',
        //     id: 1,
        //     title: '银德3期',
        //     profitAndLoss: 355.96,
        //     income: -0.0137,
        //     rateReturn: -0.0228,
        //     maxDraw: 0.0455,
        //     operateDay: 251,
        //     echartsData: [1, 2, 3, 4, 5],
        //     divider: true,
        //     option: {
        //       grid: {
        //         // 设置图表四周留白间距
        //         top: '2%',
        //         right: '2%',
        //         bottom: '4%',
        //         left: '4%'
        //       },
        //       xAxis: {
        //         show: false,
        //         type: 'category',
        //         boundaryGap: false, // 设置x轴两边的留白
        //         axisTick: {
        //           // x轴刻度尺
        //           show: false
        //         },
        //         axisLine: {
        //           // x轴线条颜色
        //           lineStyle: {
        //             color: '#999'
        //           }
        //         },
        //         data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        //       },
        //       yAxis: {
        //         min: function (value) {
        //           if (value.min < 0) {
        //             return value.min * 1.1
        //           } else {
        //             return value.min
        //           }
        //         },
        //         max: function (value) {
        //           if (value.max > 0) {
        //             return value.max
        //           } else {
        //             return value.max * 0.9
        //           }
        //         },
        //         show: false,
        //         type: 'value',
        //         interval: 1, // 刻度值间隔值
        //         splitLine: {
        //           // 网格线
        //           show: false // 关闭网格线
        //         },
        //         axisLine: {
        //           // y轴线条颜色
        //           show: true,
        //           lineStyle: {
        //             color: '#999'
        //           }
        //         }
        //       },
        //       series: [
        //         {
        //           data: [100, 97, 98, 99, 97.63],
        //           type: 'line',
        //           smooth: true, // 面积图改成弧形状
        //           lineStyle: {
        //             width: 1, // 外边线宽度
        //             color: '#42b1ff' // 外边线颜色
        //           },
        //           showSymbol: false, // 去除面积图节点圆
        //           areaStyle: {
        //             // 区域填充渐变颜色
        //             color: {
        //               type: 'linear',
        //               x: 0,
        //               y: 0,
        //               x2: 0,
        //               y2: 1,
        //               colorStops: [
        //                 {
        //                   offset: 0,
        //                   color: '#e8f3fc' // 0% 处的颜色
        //                 },
        //                 {
        //                   offset: 1,
        //                   color: '#f8fbff' // 100% 处的颜色
        //                 }
        //               ],
        //               global: false // 缺省为 false
        //             }
        //           }
        //         }
        //       ]
        //     }
        //   },
        //   {
        //     src: 'second2.png',
        //     id: 2,
        //     title: '申尊价值3号',
        //     profitAndLoss: 745.07,
        //     income: 0.0198,
        //     rateReturn: 0.0432,
        //     maxDraw: 0.0437,
        //     operateDay: 157,
        //     echartsData: [1, 2, 3, 4, 5],
        //     divider: true,
        //     option: {
        //       grid: {
        //         // 设置图表四周留白间距
        //         top: '2%',
        //         right: '2%',
        //         bottom: '4%',
        //         left: '4%'
        //       },
        //       xAxis: {
        //         show: false,
        //         type: 'category',
        //         boundaryGap: false, // 设置x轴两边的留白
        //         axisTick: {
        //           // x轴刻度尺
        //           show: false
        //         },
        //         axisLine: {
        //           // x轴线条颜色
        //           lineStyle: {
        //             color: '#999'
        //           }
        //         },
        //         data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        //       },
        //       yAxis: {
        //         min: function (value) {
        //           if (value.min < 0) {
        //             return value.min * 1.1
        //           } else {
        //             return value.min
        //           }
        //         },
        //         max: function (value) {
        //           if (value.max > 0) {
        //             return value.max
        //           } else {
        //             return value.max * 0.9
        //           }
        //         },
        //         show: false,
        //         type: 'value',
        //         interval: 1, // 刻度值间隔值
        //         splitLine: {
        //           // 网格线
        //           show: false // 关闭网格线
        //         },
        //         axisLine: {
        //           // y轴线条颜色
        //           show: true,
        //           lineStyle: {
        //             color: '#999'
        //           }
        //         }
        //       },
        //       series: [
        //         {
        //           data: [100, 97, 98, 99, 101.6],
        //           type: 'line',
        //           smooth: true, // 面积图改成弧形状
        //           lineStyle: {
        //             width: 1, // 外边线宽度
        //             color: '#42b1ff' // 外边线颜色
        //           },
        //           showSymbol: false, // 去除面积图节点圆
        //           areaStyle: {
        //             // 区域填充渐变颜色
        //             color: {
        //               type: 'linear',
        //               x: 0,
        //               y: 0,
        //               x2: 0,
        //               y2: 1,
        //               colorStops: [
        //                 {
        //                   offset: 0,
        //                   color: '#e8f3fc' // 0% 处的颜色
        //                 },
        //                 {
        //                   offset: 1,
        //                   color: '#f8fbff' // 100% 处的颜色
        //                 }
        //               ],
        //               global: false // 缺省为 false
        //             }
        //           }
        //         }
        //       ]
        //     }
        //   },
        //   {
        //     src: 'second3.png',
        //     id: 3,
        //     title: '赢康丰盈一号',
        //     profitAndLoss: 230.67,
        //     income: 0.0102,
        //     rateReturn: 0.0317,
        //     maxDraw: 0.0167,
        //     operateDay: 422,
        //     echartsData: [1, 2, 3, 4, 5],
        //     divider: false,
        //     option: {
        //       grid: {
        //         // 设置图表四周留白间距
        //         top: '2%',
        //         right: '2%',
        //         bottom: '4%',
        //         left: '4%'
        //       },
        //       xAxis: {
        //         show: false,
        //         type: 'category',
        //         boundaryGap: false, // 设置x轴两边的留白
        //         axisTick: {
        //           // x轴刻度尺
        //           show: false
        //         },
        //         axisLine: {
        //           // x轴线条颜色
        //           lineStyle: {
        //             color: '#999'
        //           }
        //         },
        //         data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        //       },
        //       yAxis: {
        //         show: false,
        //         type: 'value',
        //         interval: 1, // 刻度值间隔值
        //         splitLine: {
        //           // 网格线
        //           show: false // 关闭网格线
        //         },
        //         min: function (value) {
        //           if (value.min < 0) {
        //             return value.min * 1.1
        //           } else {
        //             return value.min
        //           }
        //         },
        //         max: function (value) {
        //           if (value.max > 0) {
        //             return value.max
        //           } else {
        //             return value.max * 0.9
        //           }
        //         },
        //         axisLine: {
        //           // y轴线条颜色
        //           show: true,
        //           lineStyle: {
        //             color: '#999'
        //           }
        //         }
        //       },
        //       series: [
        //         {
        //           data: [100, 95, 93, 98, 101.98],
        //           type: 'line',
        //           smooth: true, // 面积图改成弧形状
        //           lineStyle: {
        //             width: 1, // 外边线宽度
        //             color: '#42b1ff' // 外边线颜色
        //           },
        //           showSymbol: false, // 去除面积图节点圆
        //           areaStyle: {
        //             // 区域填充渐变颜色
        //             color: {
        //               type: 'linear',
        //               x: 0,
        //               y: 0,
        //               x2: 0,
        //               y2: 1,
        //               colorStops: [
        //                 {
        //                   offset: 0,
        //                   color: '#e8f3fc' // 0% 处的颜色
        //                 },
        //                 {
        //                   offset: 1,
        //                   color: '#f8fbff' // 100% 处的颜色
        //                 }
        //               ],
        //               global: false // 缺省为 false
        //             }
        //           }
        //         }
        //       ]
        //     }
        //   }
        // ],
      ],
      combArraysTrue: [],
      tabIndex1: 1,
      tableData: [
        {
          id: 4,
          fundCode: 'SCJ879',
          fundName: '御风进取一号',
          option: {
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
              data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
            },
            yAxis: {
              show: false,
              type: 'value',
              max: 1400, // 最大刻度值
              interval: 100, // 刻度值间隔值
              splitLine: {
                // 网格线
                show: false // 关闭网格线
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
                data: [820, 932, 901, 1300, 300],
                type: 'line',
                smooth: true, // 面积图改成弧形状
                lineStyle: {
                  width: 1, // 外边线宽度
                  color: '#42b1ff' // 外边线颜色
                },
                showSymbol: false // 去除面积图节点圆
              }
            ]
          },
          src: '2.png',
          yearRateReturn: -0.1477,
          monthRateReturn: -0.0733,
          fundManager: '丰穗投资'
        },
        {
          id: 5,
          fundCode: 'SE2068',
          fundName: '银德1期',
          option: {
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
              data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
            },
            yAxis: {
              show: false,
              type: 'value',
              max: 1400, // 最大刻度值
              interval: 100, // 刻度值间隔值
              splitLine: {
                // 网格线
                show: false // 关闭网格线
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
                data: [820, 932, 901, 1300, 300],
                type: 'line',
                smooth: true, // 面积图改成弧形状
                lineStyle: {
                  width: 1, // 外边线宽度
                  color: '#42b1ff' // 外边线颜色
                },
                showSymbol: false // 去除面积图节点圆
              }
            ]
          },
          src: '1.png',
          yearRateReturn: 0.1627,
          monthRateReturn: -0.0719,
          fundManager: '银德资产'
        },
        {
          id: 6,
          fundCode: 'S81870',
          fundName: '芝麻财富3号',
          option: {
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
              data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
            },
            yAxis: {
              show: false,
              type: 'value',
              max: 1400, // 最大刻度值
              interval: 100, // 刻度值间隔值
              splitLine: {
                // 网格线
                show: false // 关闭网格线
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
                data: [820, 932, 901, 1300, 300],
                type: 'line',
                smooth: true, // 面积图改成弧形状
                lineStyle: {
                  width: 1, // 外边线宽度
                  color: '#42b1ff' // 外边线颜色
                },
                showSymbol: false // 去除面积图节点圆
              }
            ]
          },
          yearRateReturn: 0.2515,
          src: '4.png',
          monthRateReturn: -0.0826,
          fundManager: '苏州芝麻财富'
        },
        {
          id: 7,
          fundCode: 'SNJ780',
          fundName: '汇牛上善若水',
          src: '5.png',
          option: {
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
              data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
            },
            yAxis: {
              show: false,
              type: 'value',
              max: 1400, // 最大刻度值
              interval: 100, // 刻度值间隔值
              splitLine: {
                // 网格线
                show: false // 关闭网格线
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
                data: [820, 932, 901, 1300, 300],
                type: 'line',
                smooth: true, // 面积图改成弧形状
                lineStyle: {
                  width: 1, // 外边线宽度
                  color: '#42b1ff' // 外边线颜色
                },
                showSymbol: false // 去除面积图节点圆
              }
            ]
          },
          yearRateReturn: 0.2515,
          monthRateReturn: -0.0826,
          fundManager: '汇牛资产'
        },
        {
          id: 8,
          fundCode: 'SCZ477',
          fundName: '海象1号',
          option: {
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
              data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
            },
            yAxis: {
              show: false,
              type: 'value',
              max: 1400, // 最大刻度值
              interval: 100, // 刻度值间隔值
              splitLine: {
                // 网格线
                show: false // 关闭网格线
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
                data: [820, 932, 901, 1300, 300],
                type: 'line',
                smooth: true, // 面积图改成弧形状
                lineStyle: {
                  width: 1, // 外边线宽度
                  color: '#42b1ff' // 外边线颜色
                },
                showSymbol: false // 去除面积图节点圆
              }
            ]
          },
          src: '6.png',
          yearRateReturn: 0.2255,
          monthRateReturn: -0.0956,
          fundManager: '广东海象私募基金'
        }
      ],
      tableData1: [],
      tableData2: [],
      tableData3: [],
      formInline: {
        pageNum: 1,
        pageSize: 10
      },
      total: 5,
      tabIndex: 1
    }
  },
  mounted() {
    this.getFocusProductData()
    this.getFocusManagerData()
    this.getAnalogGroup()
    this.getTrueGroup()
    this.getHotProduct()
    this.getRecommendProducts()
  },
  filters: {
    priceFormat(value) {
      if (value != null || value != undefined || value != '') {
        value = parseFloat(value / 10000).toFixed(2)
      }
      return value
    }
  },
  watch: {
    isActive1(val) {
      const frostedGlassMap = {
        JX: `精选指数产品专注各策略中长期业绩的优质中大规模管理人，如需了解具体信息请联系我们!<br/>联系方式：广发证券托管部王经理<br/>电话：0755-82721473<br/>邮箱：wangxuanyun@cmschina.com.cn`,
        CZ: '成长指数产品专注成长期业绩爆发力强的中小规模管理人，如需了解具体信息请联系我们!<br/>联系方式：广发证券托管部王经理<br/>电话：0755-82721473<br/>邮箱：wangxuanyun@cmschina.com.cn',
        XX: ''
      }
      this.frostedStr = frostedGlassMap[val]
    }
  },
  methods: {
    /**
     * @description 跳转单产品页面
     */
    jumpToSingle(row, column) {
      if (column.property === 'fundName') {
        this.$store.commit('SET_FROMPAGEJUMP', true)
        this.$router.push({
          path: '/tqgl/dcpfx',
          query: { list: { fundCode: row.fundCode, source: row.source, fundName: row.fundName } }
        })
      }
    },
    // 获取热点产品数据
    getHotProduct() {
      return new Promise((resolve, reject) => {
        let params = {}
        params.indexCode = '24a00f6b-81ce-46c0-8f12-48c721d9b5ff'
        commonApi
          .getDataBysqlCode(params)
          .then((res) => {
            let { status, data } = res.data
            if (status === 0) {
              if (data && data instanceof Array && data.length > 0) {
                this.hotProductArr = []
                let temp = []
                data.forEach((item) => {
                  let obj = {}
                  obj.label = item.DIM_NME
                  obj.value = item.DIM_CDE
                  temp.push(obj)
                })
                temp.sort((a, b) => (a.label === '雏鹰计划' ? -1 : b.label === '雏鹰计划' ? 1 : 0))
                this.hotProductArr = temp
                this.$nextTick(() => {
                  this.isActive1 = this.hotProductArr[0].value
                  this.active1Item = this.hotProductArr[0]
                })
              }
            }
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
    },
    handleButtonClick2(value) {
      this.isActive2 = value
      if (value === '产品') {
        this.tabIndex = 1
      } else {
        this.tabIndex = 2
      }
    },
    handleButtonClick1(value, item) {
      this.isActive1 = value
      this.active1Item = item
      // 根据 不同的 id 查询不同的内容
      this.getRecommendProducts()
    },
    // 热点产品more点击逻辑
    handleHotProductMoreClick() {
      this.$router.push({
        name: '指数榜单301',
        params: {
          id: this.isActive1,
          title: this.active1Item.label
        }
      })
    },
    //获取推荐产品的数据
    getRecommendProducts() {
      let params = {}
      params.indexCode = '95592cbd-0056-4d8d-9a40-1ee37170d4b2'
      params.rankType = this.isActive1
      if (params.rankType !== 'XX') return
      commonApi.getDataBysqlCode(params).then((res) => {
        let { status, data } = res.data

        let tableArray = [] // 组装tableData数据
        let fundList = []
        if (status === 0) {
          for (let i = 0; i < data.length; i++) {
            let temp = data[i]
            // 同步获取对应的series Data数据，用于组装
            let tableObj = {
              fundCode: temp.VC_FUNDCODE,
              fundName: temp.VC_FUNDNAME,
              monthRateReturn: temp.F_3M_RETURN || '',
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
          // paramsC.indexCode = 'a50f06a4-bfa6-4858-9c38-a1d0f57e5a51'
          paramsC.indexCode = '2010917d-0cbe-469d-a7a2-4c984aadfa42'
          paramsC.fundList = fundList

          commonApi.getDataBysqlCode(paramsC).then((resC) => {
            let { status: statusC, data: dataC } = resC.data
            if (statusC === 0) {
              const mergeData = merger_back_objs(dataC, 'VC_FUNDCODE')
              console.log(tableArray, 'tableArray')
              tableArray.forEach((temp) => {
                let findObj = mergeData.find((item) => item.VC_FUNDCODE == temp.fundCode + temp.strategyType)
                if (findObj) {
                  if (temp.monthRateReturn > 0) {
                    this.setTableDataOption3(findObj.origin, findObj.VC_FUNDCODE, ['#de777a'])
                  } else if (temp.monthRateReturn < 0) {
                    this.setTableDataOption3(findObj.origin, findObj.VC_FUNDCODE, ['#81b59e'])
                  } else {
                    this.setTableDataOption3(findObj.origin, findObj.VC_FUNDCODE, ['black'])
                  }
                }
              })
              // 组装好之后放到原来的数组里面去
            } else {
            }
          })
          this.tableData3 = tableArray
          console.log(this.tableData3, '>>>>>>>>>>>>>>tabledata3')
          this.$refs.tableData3.doLayout()
        }
      })
    },
    // 根据fundcode设置对应的option
    setTableDataOption3(data, fundCode, color) {
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

      for (let i = 0; i < this.tableData3.length; i++) {
        const temp = this.tableData3[i]
        if (temp.fundCode + temp.strategyType === fundCode) {
          temp.option = option
          break
        }
      }
    },
    // 跳转我的关注页面
    handleMyFocus() {
      if (this.isActive2 == '产品') {
        this.$store.commit('SET_FROMPAGEJUMP', true)
        this.$router.push({
          path: '/tqgl/wdgz',
          query: {
            name: 'smcp'
          }
        })
      } else {
        this.$store.commit('SET_FROMPAGEJUMP', true)
        this.$router.push({
          path: '/tqgl/wdgz',
          query: {
            name: 'smglr'
          }
        })
      }
    },
    // 获取推荐产品的数据
    getFocusProductData() {
      const params = {}
      params.indexCode = 'f64c7969-6778-47c5-8acb-04b360e1bc55'
      commonApi.getDataBysqlCode(params).then((res) => {
        const { status, data } = res.data
        const tableArray = [] // 组装tableData数据
        let fundList = []
        if (status === 0) {
          for (let i = 0; i < data.length; i++) {
            const temp = data[i]
            // 同步获取对应的series Data数据，用于组装
            const tableObj = {
              fundCode: temp.VC_FUNDCODE,
              fundName: temp.VC_FUNDNAME,
              monthRateReturn: temp.F_3M_RETURN || '',
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
          this.tableData1 = tableArray
        }
      })
    },
    // 获取推荐管理人数据
    getFocusManagerData() {
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
          this.tableData2 = tableArray
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

      for (let i = 0; i < this.tableData1.length; i++) {
        const temp = this.tableData1[i]
        if (temp.fundCode + temp.VC_FLAG === fundCode) {
          temp.option = option
          break
        }
      }
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

      for (let i = 0; i < this.tableData2.length; i++) {
        const temp = this.tableData2[i]
        if (temp.companyid === companyid) {
          temp.option = option
          break
        }
      }
    },

    // 获取模拟组合数据
    getAnalogGroup() {
      commonApi
        .getDataBysqlCode({
          indexCode: '7cf743ed-a5eb-4db5-bfa3-213db91ae7f6'
        })
        .then((res) => {
          const { status, data } = res.data
          if (status === 0) {
            data.forEach((element) => {
              element.CREATEDATE = fun.yyr_timestampToTime(element.CREATEDATE)
            })
            this.combArrays = []
            for (let i = 0; i < data.length; i += 3) {
              this.combArrays.push(data.slice(i, i + 3))
            }
            console.log('combArrays', this.combArrays)
          }
        })
        .catch(() => {})
    },
    // 获取真实组合数据
    getTrueGroup() {
      commonApi
        .getDataBysqlCode({
          indexCode: '7cfff2b0-be73-478f-9061-27ec46303004'
        })
        .then((res) => {
          const { status, data } = res.data
          if (status === 0) {
            data.forEach((element) => {
              element.ENDDATE = fun.yyr_timestampToTime(element.D_GZ_DATE)
              element.option = {}
              const params = {}
              params.indexCode = 'a50f06a4-bfa6-4858-9c38-a1d0f57e5a51'
              params.fundCode = element.VC_FUNDCODE
              commonApi.getDataBysqlCode(params).then((res) => {
                const { status, data } = res.data
                if (status === 0) {
                  this.setTableDataOption1(data, element.VC_FUNDCODE, ['#79c7ff'])
                  // 组装好之后放到原来的数组里面去
                } else {
                }
              })
            })
            this.combArraysTrue = []
            for (let i = 0; i < data.length; i += 3) {
              this.combArraysTrue.push(data.slice(i, i + 3))
            }
          }
        })
        .catch(() => {})
    },
    // 根据fundcode设置对应的option
    setTableDataOption1(data, fundCode, color) {
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
            showSymbol: false, // 去除面积图节点圆
            areaStyle: {
              // 区域填充渐变颜色
              color: {
                type: 'linear',
                x: 0,
                y: 0,
                x2: 0,
                y2: 1,
                colorStops: [
                  {
                    offset: 0,
                    color: '#a7cef5' // 0% 处的颜色
                  },
                  {
                    offset: 1,
                    color: '#f1f7fd' // 100% 处的颜色
                  }
                ],
                global: false // 缺省为 false
              }
            }
          }
        ]
      }

      for (let i = 0; i < this.combArraysTrue.length; i++) {
        this.combArraysTrue[i].forEach((element) => {
          // const temp = element
          if (element.VC_FUNDCODE === fundCode) {
            element.option = option
          }
        })
      }
      console.log(this.combArraysTrue, '>')
    },
    handleMore() {
      this.$router.push({
        path: '/tqgl/tgwbcpsx',
        query: { from: 'myfocus' }
      })
    },
    jumpPage2(data) {
      this.$router.push({
        path: '/xxyzsq',
        query: {
          fundCode: data.fundCode,
          fundName: data.fundName,
          flag: data.flag === '发起验证'
        }
      })
    },
    tabClick(val) {
      this.tabIndex = val
      if (val == 0) {
        this.total = 5
      } else if (val == 1) {
        this.total = 3
      } else {
        this.total = 2
      }
    },
    /**
     * @description 跳转单产品页面
     */
    jumpToSingle(row, column) {
      if (column.property === 'fundName') {
        this.$store.commit('SET_FROMPAGEJUMP', true)
        this.$router.push({
          path: '/tqgl/dcpfx',
          query: { list: { fundCode: row.fundCode, source: row.source, fundName: row.fundName } }
        })
      }
    },
    jumpToManager(row, column) {
      const newObj = {
        company_id: row.companyid,
        manager_name: row.managerShortName
      }
      if (column.property === 'managerShortName') {
        this.$store.commit('SET_FROMPAGEJUMP', true)
        this.$router.push({
          path: '/tqgl/glrxq',
          query: { managerList: newObj }
        })
      }
    }
  }
}
</script>
<style lang="scss" scoped>
.rdcp {
  .elLink {
    width: 34px;
    font-size: 14px;
    color: #005ba1;
    line-height: 30px;
    // padding: 3px;
  }

  .dashboard-title {
    font-size: 18px;
    // font-weight: 600;
  }

  .title-button-left-rdcp {
    display: inline-block;
    position: absolute;
    top: 5px;
    left: 83px;
    border: 1px solid #356385;
    width: 90px;
    height: 22px;
    line-height: 22px;
    font-size: 14px;
    padding-left: 13px;
    -webkit-border-radius: 40px 0px 0px 40px;
    -moz-border-radius: 40px 0px 0px 40px;
    border-radius: 40px 0px 0px 40px;
  }

  .title-button-center-rdcp {
    display: inline-block;
    position: absolute;
    top: 5px;
    left: 173px;
    height: 22px;
    line-height: 22px;
    border: 1px solid #356385;
    border-left: none;
    width: 90px;
    height: 22px;
    font-size: 14px;
    padding-left: 13px;
  }

  .title-button-right-rdcp {
    display: inline-block;
    border: 1px solid #356385;
    border-left: none;
    position: absolute;
    top: 5px;
    left: 263px;
    line-height: 22px;
    width: 90px;
    height: 22px;
    font-size: 14px;
    padding-left: 10px;
    -webkit-border-radius: 0px 40px 40px 0px;
    -moz-border-radius: 0px 40px 40px 0px;
    border-radius: 0px 40px 40px 0px;
  }
}
::v-deep .el-carousel__indicators--horizontal {
  display: none;
}
::v-deep .el-table__body {
  margin-right: 12px !important;
}

.tableOverflow {
  ::v-deep .el-table--scrollable-y .el-table__body-wrapper {
    overflow-y: auto !important;
  }
}

::v-deep .el-table thead tr th {
  background-color: white !important;
}

::v-deep .el-table--scrollable-y .el-table__body-wrapper {
  overflow-y: hidden;
}

.blur {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  backdrop-filter: blur(10px); /* 调整模糊程度，可以根据需要更改 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.blur-div {
  text-align: center;
  vertical-align: middle;
  width: 492px;
  height: 235px;
  padding: 20px;
  padding-top: 50px;
}

.title {
  height: 30px;

  .titletitle {
    position: relative;
    font-size: 18px;
    margin-right: 12px;
    line-height: 30px;
    color: #333;
    vertical-align: middle;
    text-align: center;
    // font-weight: 600;
  }

  .title-button-left {
    display: inline-block;
    position: absolute;
    top: 5px;
    left: 83px;
    border: 1px solid #356385;
    width: 70px;
    height: 22px;
    line-height: 20px;
    font-size: 14px;
    padding-left: 13px;
    -webkit-border-radius: 40px 0px 0px 40px;
    -moz-border-radius: 40px 0px 0px 40px;
    border-radius: 40px 0px 0px 40px;
  }

  .title-button-left2 {
    display: inline-block;
    position: absolute;
    top: 5px;
    left: 83px;
    border: 1px solid #356385;
    width: 70px;
    height: 22px;
    line-height: 20px;
    font-size: 14px;
    padding-left: 22px;
    -webkit-border-radius: 40px 0px 0px 40px;
    -moz-border-radius: 40px 0px 0px 40px;
    border-radius: 40px 0px 0px 40px;
  }

  .title-button-center {
    display: inline-block;
    border: 1px solid #356385;
    border-left: none;
    width: 70px;
    height: 22px;
    font-size: 14px;
    padding-left: 10px;
  }

  .title-button-right {
    display: inline-block;
    border: 1px solid #356385;
    border-left: none;
    position: absolute;
    top: 5px;
    left: 153px;
    line-height: 20px;
    width: 70px;
    height: 22px;
    font-size: 14px;
    padding-left: 8px;
    -webkit-border-radius: 0px 40px 40px 0px;
    -moz-border-radius: 0px 40px 40px 0px;
    border-radius: 0px 40px 40px 0px;
  }

  .title-button-right2 {
    display: inline-block;
    border: 1px solid #356385;
    border-left: none;
    position: absolute;
    top: 5px;
    left: 153px;
    line-height: 20px;
    width: 70px;
    height: 22px;
    font-size: 14px;
    padding-left: 15px;
    -webkit-border-radius: 0px 40px 40px 0px;
    -moz-border-radius: 0px 40px 40px 0px;
    border-radius: 0px 40px 40px 0px;
  }

  .button-active {
    background-color: #6b8da6;
    color: white;
  }

  .elLink {
    width: 34px;
    font-size: 14px;
    color: #005ba1;
    line-height: 30px;
    // padding: 3px;
  }

  .tab {
    color: #c8993d;
    font-size: 14px;
    cursor: pointer;
  }
}

.comb-title {
  color: #005ba1;
  font-size: 16px;
  cursor: pointer;
}

.comb-income {
  font-weight: bold;
  font-size: 18px;
}

.income-red {
  color: red;
}

.income-green {
  color: green;
}

.rate-return-red {
  color: red;
}

.rate-return-green {
  color: green;
}

.el-divider--vertical {
  top: 48px;
  display: inline-block;
  width: 1px;
  height: 130px;
  margin: 0px 8px;
  vertical-align: middle;
  position: relative;
}

.elLink {
  width: 34px;
  color: #005ba1;
  font-size: 14px;
}

.curLink {
  color: #fff;
  background-color: #c8993d;
  padding: 3px;
}

.fund_cell {
  display: flex;
  align-items: center;
  color: #005ba1;
  cursor: pointer;

  .fund_name {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    margin-right: 5px;
  }
}

.over-flow-nowarp {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  -o-text-overflow: ellipsis;
}

.line {
  height: 1px;
  border-bottom: 1px solid #f2f2f2;
  margin: 10px 0 15px;
}

.mnzhBtn {
  // width: calc(100% - 20px);
  border: 1px solid #ebeef5;
  border-radius: 40px;
  height: 30px;
  line-height: 30px;
  font-size: 14px;
  cursor: pointer;
  color: #005ba1;
  text-align: center;
  margin-top: 15px;
}

.noDataStyle {
  text-align: center;
  height: 300px;
}

.noDataStyle img {
  position: relative;
  top: 45px;
}

.elRowClass {
  //line-height: 21px;
  line-height: 36px;
}
.elRowClassOther {
  line-height: 21px;
}
</style>

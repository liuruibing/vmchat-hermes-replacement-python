<template>
  <el-row :gutter="20">
    <el-col :span="8">
      <box-template>
        <template slot="title">
          <el-row style="margin: 16px 0px;">
            <el-col :span="22">
              <span class="dashboard-title">我的组合</span>
              <!--              <span style="margin-left: 20px;color: #c8993d;font-size: 14px;font-weight: normal">-->
              <!--                <span>我的资产</span>-->
              <!--                <span>|</span>-->
              <!--                <span>我的组合</span>-->
              <!--                <span>|</span>-->
              <!--                <span>资产捏合</span>-->
              <!--              </span>-->
            </el-col>
            <el-col :span="2">
              <div class="search_button_com">
                <span style="font-size: 14px">
                  <el-link :underline="false" type="primary" @click="">
                    <span class="elLink">更多</span>
                  </el-link>
                </span>
              </div>
            </el-col>
          </el-row>
        </template>
        <template slot="content">
          <div style="height: 300px;overflow: hidden">
            <el-row style="padding: 10px 10px;">
              <template v-for="item in combArray">
                <el-col :key="item.id" :span="8">
                  <el-row>
                    <el-col :span="22">
                      <div style="display: inline-block">
                        <div>
                          <span class="comb-title">{{ item.title | noDataFilter }}</span>
                        </div>
                        <div><span>近一周盈亏额（元）</span></div>
                        <div>
                          <span class="comb-income">{{ item.profitAndLoss | moneyYuan }}</span>
                        </div>
                        <div>
                          <span>近一周收益</span>
                          <template v-if="item.income >= 0">
                            <span class="income-red">
                              <i class="el-icon-top" />
                              <span>{{ item.income | numberToFixedStr(2, 100, '%') }}</span>
                            </span>
                          </template>
                          <template v-if="item.income < 0">
                            <span class="income-green">
                              <i class="el-icon-bottom" />
                              <span>{{ (item.income * -1) | numberToFixedStr(2, 100, '%') }}</span>
                            </span>
                          </template>
                        </div>
                      </div>
                      <!--                      <myecharts-->
                      <!--                        :id="`combEchart` + item.id"-->
                      <!--                        :ref="`combEchart` + item.id"-->
                      <!--                        :options="item.option"-->
                      <!--                        resize-dom="cmbfof"-->
                      <!--                        style="width: 100%; height: 100px"-->
                      <!--                      />-->
                      <img :src="require(`./img/${item.src}`)" height="100px" width="100%" />
                    </el-col>
                    <el-col :span="2">
                      <el-divider
                        v-if="item.divider"
                        content-position="center"
                        direction="vertical"
                        height="30px;"
                      />
                    </el-col>
                  </el-row>
                  <el-row style="margin-top:30px;">
                    <el-col :span="12">
                      <span>近一月收益率</span>
                    </el-col>
                    <el-col :span="12">
                      <div class="search_button_com" style="padding-right: 20px;">
                        <span v-if="item.rateReturn > 0" class="rate-return-red">
                          {{ item.rateReturn | numberToFixedStr(2, 100, '%') }}
                        </span>
                        <span v-if="item.rateReturn == 0">
                          {{ item.rateReturn | numberToFixedStr(2, 100, '%') }}
                        </span>
                        <span v-if="item.rateReturn < 0" class="rate-return-green">
                          {{ item.rateReturn | numberToFixedStr(2, 100, '%') }}
                        </span>
                      </div>
                    </el-col>
                  </el-row>
                  <el-row>
                    <el-col :span="12">
                      <span>最大回撤</span>
                    </el-col>
                    <el-col :span="12">
                      <div class="search_button_com" style="padding-right: 20px;">
                        <span style="color: green;">-{{ item.maxDraw | numberToFixedStr(2, 100, '%') }}</span>
                      </div>
                    </el-col>
                  </el-row>
                  <el-row>
                    <el-col :span="12">
                      <span>运行天数</span>
                    </el-col>
                    <el-col :span="12">
                      <div class="search_button_com" style="padding-right: 20px;">
                        <span>{{ item.operateDay | noDataFilter }}</span>
                      </div>
                    </el-col>
                  </el-row>
                </el-col>
              </template>
            </el-row>
          </div>
        </template>
      </box-template>
    </el-col>
    <el-col :span="8">
      <box-template>
        <template slot="title">
          <el-row style="margin: 16px 0px;">
            <el-col :span="22">
              <span class="dashboard-title">我的关注</span>
              <span
                style="margin-left: 20px;color: #c8993d;font-size: 14px;font-weight: normal;cursor: pointer;"
              >
                <span @click="tabClick(0)" :class="tabIndex === 0 ? 'curLink' : ''">全部</span>
                <span>|</span>
                <span @click="tabClick(1)" :class="tabIndex === 1 ? 'curLink' : ''">托管产品</span>
                <span>|</span>
                <span @click="tabClick(2)" :class="tabIndex === 2 ? 'curLink' : ''">市场产品</span>
              </span>
            </el-col>
            <el-col :span="2">
              <div class="search_button_com">
                <span style="font-size: 14px">
                  <el-link :underline="false" type="primary" @click="handleMore">
                    <span class="elLink">更多</span>
                  </el-link>
                </span>
              </div>
            </el-col>
          </el-row>
        </template>
        <template slot="content">
          <div style="height: 300px;overflow: hidden;">
            <el-table v-if="tabIndex === 0" :data="tableData" align="center" border max-height="250px">
              <el-table-column header-align="center" label="产品代码" prop="fundCode" show-overflow-tooltip>
                <template slot-scope="scope">
                  <el-link :underline="false" type="primary" @click="more">
                    <span class="elLink" style="font-size: 14px">
                      {{ scope.row.fundCode | noDataFilter }}
                    </span>
                  </el-link>
                </template>
              </el-table-column>
              <el-table-column
                align="left"
                header-align="center"
                label="产品名称"
                prop="fundName"
                show-overflow-tooltip
              >
                <template slot-scope="scope">
                  <el-link
                    type="primary"
                    :underline="false"
                    style="font-size: 14px"
                    @click="jumpPage(scope.row)"
                  >
                    <span class="elLink" style="font-size: 14px">
                      {{ scope.row.fundName | noDataFilter }}
                    </span>
                  </el-link>
                </template>
              </el-table-column>
              <el-table-column align="center" header-align="center" label="近半年走势图" prop="halfYeear">
                <template slot-scope="scope">
                  <!--                  <myecharts-->
                  <!--                    :id="`combEchart` + scope.row.id"-->
                  <!--                    :ref="`combEchart` + scope.row.id"-->
                  <!--                    :options="scope.row.option"-->
                  <!--                    resize-dom="cmbfof"-->
                  <!--                    style="width: 100%; height: 50px"-->
                  <!--                  ></myecharts>-->
                  <img :src="require(`./img/${scope.row.src}`)" height="100%" width="100%" />
                  <!--                  <img src="@/assets/curv/1.png" height="100%" width="100%"/>-->
                </template>
              </el-table-column>
              <el-table-column
                align="right"
                header-align="center"
                label="今年以来收益率(%)"
                prop="yearRateReturn"
                show-overflow-tooltip
              >
                <template slot-scope="scope">
                  <span v-if="scope.row.yearRateReturn > 0" style="color: red">
                    {{ scope.row.yearRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                  <span v-else-if="scope.row.yearRateReturn == 0">
                    {{ scope.row.yearRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                  <span v-else style="color: green;">
                    {{ scope.row.yearRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column
                align="right"
                header-align="center"
                label="近一月收益率(%)"
                prop="monthRateReturn"
                show-overflow-tooltip
              >
                <template slot-scope="scope">
                  <span v-if="scope.row.monthRateReturn > 0" style="color: red">
                    {{ scope.row.monthRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                  <span v-else-if="scope.row.monthRateReturn == 0">
                    {{ scope.row.monthRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                  <span v-else style="color: green;">
                    {{ scope.row.monthRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column
                align="left"
                header-align="center"
                label="管理人"
                prop="fundManager"
                show-overflow-tooltip
              >
                <template slot-scope="scope">
                  <span>
                    {{ scope.row.fundManager | noDataFilter }}
                  </span>
                </template>
              </el-table-column>
            </el-table>
            <el-table v-if="tabIndex === 1" :data="tableData1" align="center" border max-height="250px">
              <el-table-column header-align="center" label="产品代码" prop="fundCode" show-overflow-tooltip>
                <template slot-scope="scope">
                  <el-link :underline="false" type="primary" @click="more">
                    <span class="elLink" style="font-size: 14px">
                      {{ scope.row.fundCode | noDataFilter }}
                    </span>
                  </el-link>
                </template>
              </el-table-column>
              <el-table-column
                align="left"
                header-align="center"
                label="产品名称"
                prop="fundName"
                width="130"
              >
                <!-- show-overflow-tooltip -->
                <template slot-scope="scope">
                  <!-- <el-link
                    type="primary"
                    :underline="false"
                    style="font-size: 14px"
                    @click="jumpPage(scope.row)"
                  >
                    <span class="elLink" style="font-size: 14px">
                      {{ scope.row.fundName | noDataFilter }}
                    </span>
                  </el-link> -->
                  <span class="color_4f95dd fund_cell">
                    <span class="fund_name" :title="scope.row.fundName" @click="jumpPage(scope.row)">
                      {{ scope.row.fundName | noDataFilter }}
                    </span>
                    <el-tag
                      size="mini"
                      type="warning"
                      style="margin-bottom:0 !important"
                      v-if="scope.row.isFlag"
                      @click="jumpPage2(scope.row)"
                    >
                      {{ scope.row.flag || '' }}
                    </el-tag>
                  </span>
                </template>
              </el-table-column>
              <el-table-column align="center" header-align="center" label="近半年走势图" prop="halfYeear">
                <template slot-scope="scope">
                  <!--                  <myecharts-->
                  <!--                    :id="`combEchart` + scope.row.id"-->
                  <!--                    :ref="`combEchart` + scope.row.id"-->
                  <!--                    :options="scope.row.option"-->
                  <!--                    resize-dom="cmbfof"-->
                  <!--                    style="width: 100%; height: 50px"-->
                  <!--                  ></myecharts>-->
                  <img :src="require(`./img/${scope.row.src}`)" height="100%" width="100%" />
                  <!--                  <img src="@/assets/curv/1.png" height="100%" width="100%"/>-->
                </template>
              </el-table-column>
              <el-table-column
                align="right"
                header-align="center"
                label="今年以来收益率(%)"
                prop="yearRateReturn"
                show-overflow-tooltip
              >
                <template slot-scope="scope">
                  <span v-if="scope.row.yearRateReturn > 0" style="color: red">
                    {{ scope.row.yearRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                  <span v-else-if="scope.row.yearRateReturn == 0">
                    {{ scope.row.yearRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                  <span v-else style="color: green;">
                    {{ scope.row.yearRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column
                align="right"
                header-align="center"
                label="近一月收益率(%)"
                prop="monthRateReturn"
                show-overflow-tooltip
              >
                <template slot-scope="scope">
                  <span v-if="scope.row.monthRateReturn > 0" style="color: red">
                    {{ scope.row.monthRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                  <span v-else-if="scope.row.monthRateReturn == 0">
                    {{ scope.row.monthRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                  <span v-else style="color: green;">
                    {{ scope.row.monthRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column
                align="left"
                header-align="center"
                label="管理人"
                prop="fundManager"
                show-overflow-tooltip
              >
                <template slot-scope="scope">
                  <span>
                    {{ scope.row.fundManager | noDataFilter }}
                  </span>
                </template>
              </el-table-column>
            </el-table>
            <el-table v-if="tabIndex === 2" :data="tableData2" align="center" border max-height="250px">
              <el-table-column header-align="center" label="产品代码" prop="fundCode" show-overflow-tooltip>
                <template slot-scope="scope">
                  <el-link :underline="false" type="primary" @click="more">
                    <span class="elLink" style="font-size: 14px">
                      {{ scope.row.fundCode | noDataFilter }}
                    </span>
                  </el-link>
                </template>
              </el-table-column>
              <el-table-column
                align="left"
                header-align="center"
                label="产品名称"
                prop="fundName"
                show-overflow-tooltip
              >
                <template slot-scope="scope">
                  <el-link
                    type="primary"
                    :underline="false"
                    style="font-size: 14px"
                    @click="jumpPage(scope.row)"
                  >
                    <span class="elLink" style="font-size: 14px">
                      {{ scope.row.fundName | noDataFilter }}
                    </span>
                  </el-link>
                </template>
              </el-table-column>
              <el-table-column align="center" header-align="center" label="近半年走势图" prop="halfYeear">
                <template slot-scope="scope">
                  <!--                  <myecharts-->
                  <!--                    :id="`combEchart` + scope.row.id"-->
                  <!--                    :ref="`combEchart` + scope.row.id"-->
                  <!--                    :options="scope.row.option"-->
                  <!--                    resize-dom="cmbfof"-->
                  <!--                    style="width: 100%; height: 50px"-->
                  <!--                  ></myecharts>-->
                  <img :src="require(`./img/${scope.row.src}`)" height="100%" width="100%" />
                  <!--                  <img src="@/assets/curv/1.png" height="100%" width="100%"/>-->
                </template>
              </el-table-column>
              <el-table-column
                align="right"
                header-align="center"
                label="今年以来收益率(%)"
                prop="yearRateReturn"
                show-overflow-tooltip
              >
                <template slot-scope="scope">
                  <span v-if="scope.row.yearRateReturn > 0" style="color: red">
                    {{ scope.row.yearRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                  <span v-else-if="scope.row.yearRateReturn == 0">
                    {{ scope.row.yearRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                  <span v-else style="color: green;">
                    {{ scope.row.yearRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column
                align="right"
                header-align="center"
                label="近一月收益率(%)"
                prop="monthRateReturn"
                show-overflow-tooltip
              >
                <template slot-scope="scope">
                  <span v-if="scope.row.monthRateReturn > 0" style="color: red">
                    {{ scope.row.monthRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                  <span v-else-if="scope.row.monthRateReturn == 0">
                    {{ scope.row.monthRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                  <span v-else style="color: green;">
                    {{ scope.row.monthRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column
                align="left"
                header-align="center"
                label="管理人"
                prop="fundManager"
                show-overflow-tooltip
              >
                <template slot-scope="scope">
                  <span>
                    {{ scope.row.fundManager | noDataFilter }}
                  </span>
                </template>
              </el-table-column>
            </el-table>
            <Pagination
              :limit="formInline.pageSize"
              :page="formInline.pageNum"
              :total="total"
              @pagination="Pagination"
            />
          </div>
        </template>
      </box-template>
    </el-col>
    <el-col :span="8">
      <box-template>
        <template slot="title">
          <el-row style="margin: 16px 0px;">
            <el-col :span="22">
              <span class="dashboard-title">推荐产品</span>
            </el-col>
            <el-col :span="2">
              <div class="search_button_com">
                <span style="font-size: 14px">
                  <el-link :underline="false" type="primary" @click="">
                    <span class="elLink">更多</span>
                  </el-link>
                </span>
              </div>
            </el-col>
          </el-row>
        </template>
        <template slot="content">
          <div style="height: 300px;overflow: hidden;">
            <el-table :data="tableData3" align="center" border max-height="250px">
              <el-table-column header-align="center" label="产品代码" prop="fundCode" show-overflow-tooltip>
                <template slot-scope="scope">
                  <el-link :underline="false" type="primary" @click="more">
                    <span class="elLink" style="font-size: 14px">
                      {{ scope.row.fundCode | noDataFilter }}
                    </span>
                  </el-link>
                </template>
              </el-table-column>
              <el-table-column
                align="left"
                header-align="center"
                label="产品名称"
                prop="fundName"
                show-overflow-tooltip
              >
                <template slot-scope="scope">
                  <el-link type="primary" :underline="false" @click="more">
                    <span class="elLink" style="font-size: 14px">
                      {{ scope.row.fundName | noDataFilter }}
                    </span>
                  </el-link>
                </template>
              </el-table-column>
              <el-table-column align="center" header-align="center" label="近半年走势图" prop="halfYeear">
                <template slot-scope="scope">
                  <img :src="require(`./img/${scope.row.src}`)" height="100%" width="100%" />
                  <!--                  <myecharts-->
                  <!--                    :id="`combEchart` + scope.row.id"-->
                  <!--                    :ref="`combEchart` + scope.row.id"-->
                  <!--                    :options="scope.row.option"-->
                  <!--                    resize-dom="cmbfof"-->
                  <!--                    style="width: 100%; height: 50px"-->
                  <!--                  ></myecharts>-->
                </template>
              </el-table-column>
              <el-table-column
                align="right"
                header-align="center"
                label="今年以来收益率(%)"
                prop="yearRateReturn"
                show-overflow-tooltip
              >
                <template slot-scope="scope">
                  <span v-if="scope.row.yearRateReturn > 0" style="color: red">
                    {{ scope.row.yearRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                  <span v-else-if="scope.row.yearRateReturn == 0">
                    {{ scope.row.yearRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                  <span v-else style="color: green;">
                    {{ scope.row.yearRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column
                align="right"
                header-align="center"
                label="近一月收益率(%)"
                prop="monthRateReturn"
                show-overflow-tooltip
              >
                <template slot-scope="scope">
                  <span v-if="scope.row.monthRateReturn > 0" style="color: red">
                    {{ scope.row.monthRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                  <span v-else-if="scope.row.monthRateReturn == 0">
                    {{ scope.row.monthRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                  <span v-else style="color: green;">
                    {{ scope.row.monthRateReturn | numberToFixedStr(2, 100, '%') }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column
                align="left"
                header-align="center"
                label="管理人"
                prop="fundManager"
                show-overflow-tooltip
              >
                <template slot-scope="scope">
                  <span>
                    {{ scope.row.fundManager | noDataFilter }}
                  </span>
                </template>
              </el-table-column>
            </el-table>
            <Pagination
              :limit="formInline.pageSize"
              :page="formInline.pageNum"
              :total="total"
              @pagination="Pagination"
            ></Pagination>
          </div>
        </template>
      </box-template>
    </el-col>
    <!--    <el-col :span="8">-->
    <!--      <bygclsybx />-->
    <!--    </el-col>-->
  </el-row>
</template>
<script>
import boxTemplate from './boxTemplate'
import myecharts from '@/components/Echarts'
import Pagination from '@/components/Pagination'
import bygclsybx from './bygclsybx'

export default {
  components: { boxTemplate, myecharts, Pagination, bygclsybx },
  data() {
    return {
      isActive: '真实组合',
      formInline: {
        pageNum: 1,
        pageSize: 10
      },
      total: 5,
      combArray: [
        {
          src: 'second1.png',
          id: 1,
          title: '银德1期',
          profitAndLoss: 127355.96,
          income: -0.0137,
          rateReturn: -0.0228,
          maxDraw: 0.0455,
          operateDay: 251,
          echartsData: [1, 2, 3, 4, 5],
          divider: true,
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
              show: false,
              type: 'value',
              interval: 1, // 刻度值间隔值
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
                data: [100, 97, 98, 99, 97.63],
                type: 'line',
                smooth: true, // 面积图改成弧形状
                lineStyle: {
                  width: 1, // 外边线宽度
                  color: '#42b1ff' // 外边线颜色
                },
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
                        color: '#e8f3fc' // 0% 处的颜色
                      },
                      {
                        offset: 1,
                        color: '#f8fbff' // 100% 处的颜色
                      }
                    ],
                    global: false // 缺省为 false
                  }
                }
              }
            ]
          }
        },
        {
          src: 'second2.png',
          id: 2,
          title: '申尊价值1号',
          profitAndLoss: 157245.07,
          income: 0.0198,
          rateReturn: 0.0432,
          maxDraw: 0.0437,
          operateDay: 157,
          echartsData: [1, 2, 3, 4, 5],
          divider: true,
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
              show: false,
              type: 'value',
              interval: 1, // 刻度值间隔值
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
                data: [100, 97, 98, 99, 101.6],
                type: 'line',
                smooth: true, // 面积图改成弧形状
                lineStyle: {
                  width: 1, // 外边线宽度
                  color: '#42b1ff' // 外边线颜色
                },
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
                        color: '#e8f3fc' // 0% 处的颜色
                      },
                      {
                        offset: 1,
                        color: '#f8fbff' // 100% 处的颜色
                      }
                    ],
                    global: false // 缺省为 false
                  }
                }
              }
            ]
          }
        },
        {
          src: 'second3.png',
          id: 3,
          title: '赢康丰盈三号',
          profitAndLoss: 171230.67,
          income: 0.0102,
          rateReturn: 0.0317,
          maxDraw: 0.0167,
          operateDay: 422,
          echartsData: [1, 2, 3, 4, 5],
          divider: false,
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
                data: [100, 95, 93, 98, 101.98],
                type: 'line',
                smooth: true, // 面积图改成弧形状
                lineStyle: {
                  width: 1, // 外边线宽度
                  color: '#42b1ff' // 外边线颜色
                },
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
                        color: '#e8f3fc' // 0% 处的颜色
                      },
                      {
                        offset: 1,
                        color: '#f8fbff' // 100% 处的颜色
                      }
                    ],
                    global: false // 缺省为 false
                  }
                }
              }
            ]
          }
        }
      ],
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
      tableData1: [
        {
          id: 6,
          fundCode: 'S81870',
          fundName: '芝麻财富3号',
          isFlag: true,
          flag: '发起验证',
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
          isFlag: true,
          flag: '已验证',
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
          isFlag: true,
          flag: '验证中',
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
      tableData2: [
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
        }
      ],
      tableData3: [
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
      tabIndex: 0
    }
  },
  methods: {
    handleButtonClick(value) {
      this.isActive = value
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
    handleMore() {
      this.$router.push({
        path: '/tqgl/tgwbcpsx',
        query: { from: 'myfocus' }
      })
    },
    jumpPage() {
      this.$router.push({
        path: '/cpxq'
      })
    },
    jumpPage2(data) {
      this.$router.push({
        path: '/xxyzsq',
        query: {
          fundCode: data.fundCode,
          fundName: data.fundName,
          flag: data.flag === '发起验证' ? true : false
        }
      })
    },
    more() {
      this.$router.push({
        path: '/cpxq'
      })
    },
    Pagination() {}
  }
}
</script>
<style lang="scss" scoped>
::v-deep .el-table--scrollable-y .el-table__body-wrapper {
  overflow-y: hidden;
}
.title-button-left {
  display: inline-block;
  border: 1px solid #000000;
  width: 70px;
  height: 22px;
  padding-left: 13px;
  -webkit-border-radius: 40px 0px 0px 40px;
  -moz-border-radius: 40px 0px 0px 40px;
  border-radius: 40px 0px 0px 40px;
}

.title-button-center {
  display: inline-block;
  border: 1px solid #000000;
  border-left: none;
  width: 70px;
  height: 22px;
  padding-left: 10px;
}

.title-button-right {
  display: inline-block;
  border: 1px solid #000000;
  border-left: none;
  width: 70px;
  height: 22px;
  padding-left: 8px;
  -webkit-border-radius: 0px 40px 40px 0px;
  -moz-border-radius: 0px 40px 40px 0px;
  border-radius: 0px 40px 40px 0px;
}
.button-active {
  background-color: #6b8da6;
  color: white;
}

.dashboard-title {
  font-size: 18px;
  // font-weight: 600;
  margin-right: 16px;
}

.comb-title {
  color: #2772bd;
  font-size: 16px;
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
  color: #2672bc;
  font-size: 14px;
  padding: 3px;
}
.curLink {
  color: #fff;
  background-color: #c8993d;
  padding: 3px;
}
.fund_cell {
  display: flex;
  align-items: center;
  color: #2672bc;
  cursor: pointer;
  .fund_name {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    margin-right: 5px;
  }
}
</style>

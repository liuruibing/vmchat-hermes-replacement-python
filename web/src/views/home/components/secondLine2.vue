<template>
  <el-row :gutter="20">
    <el-col :span="8">
      <box-template>
        <template slot="title">
          <el-row style="margin: 16px 0px">
            <el-col :span="12">
              <div class="dashboard-title">热点机构</div>
            </el-col>
            <el-col :span="12">
              <div class="search_button_com">
                <span style="font-size: 14px">
                  <el-link :underline="false" type="primary" @click="more">
                    <span class="elLink">{{ moreStr }}</span>
                  </el-link>
                </span>
              </div>
            </el-col>
          </el-row>
        </template>
        <template slot="content">
          <div style="height: 290px; padding: 10px 0px" v-if="setupInfoArrs.length">
            <el-carousel height="100%" style="height: 100%; width: 100%; margin: auto" :autoplay="false" arrow="always">
              <el-carousel-item v-for="(setupInfoArr, index1) in setupInfoArrs" :key="index1">
                <el-row type="flex">
                  <el-col :span="8" v-for="(item, index2) in setupInfoArr" :key="index2">
                    <div style="text-align: center; vertical-align: middle" class="imgBox">
                      <img :src="item.VC_LOGO_URL" style="width: 188px; height: 72px; position: relative; left: -20px" />
                    </div>
                    <div
                      @click="jumpToManager(item)"
                      class="font-special-color over-flow-nowarp pointer"
                      style="height: 60px; font-size: 14px; line-height: 60px; padding-right: 10px"
                    >
                      {{ item.COMPANY_NAME }}
                    </div>
                    <div class="over-flow-nowarp" style="height: 25px; font-size: 14px; line-height: 30px; padding-right: 10px">成立日期&nbsp;:&nbsp;{{ item.FOUNDDATE }}</div>
                    <div class="over-flow-nowarp" style="height: 25px; font-size: 14px; line-height: 30px; padding-right: 10px">注册资本&nbsp;:&nbsp;{{ item.CAPITAL }}万元</div>
                    <div class="over-flow-nowarp" style="height: 25px; font-size: 14px; line-height: 30px; padding-right: 10px">基金数量&nbsp;:&nbsp;{{ item.FUND_NUM }}只</div>
                    <div class="over-flow-nowarp" style="height: 25px; font-size: 14px; line-height: 30px; padding-right: 10px">
                      自主管理规模&nbsp;:&nbsp;{{ item.MANAGE_ASSET }}
                    </div>
                    <div class="over-flow-nowarp" style="height: 25px; font-size: 14px; line-height: 30px; padding-right: 10px">员工人数&nbsp;:&nbsp;{{ item.STAFF_NUM }}人</div>
                  </el-col>
                </el-row>
              </el-carousel-item>
            </el-carousel>
          </div>
          <div class="noDataStyle" v-else>
            <img :src="imgUrl" alt="" />
          </div>
        </template>
      </box-template>
      <div style="border-bottom: 1px solid #333333"></div>
    </el-col>
    <el-col :span="8">
      <box-template>
        <template slot="title">
          <div class="title" style="margin: 16px 0px">
            <el-row type="flex">
              <el-col :span="22">
                <span class="titletitle">我的组合</span>
                <span :class="['title-button-left', 'pointer', isActive === '模拟组合' ? 'button-active' : '']" @click="handleButtonClick('模拟组合')">模拟组合</span>
                <span :class="['title-button-right', 'pointer', isActive === '真实组合' ? 'button-active' : '']" @click="handleButtonClick('真实组合')">真实组合</span>
              </el-col>
              <el-col :span="2">
                <div class="search_button_com">
                  <span style="font-size: 14px">
                    <el-link :underline="false" type="primary" @click="jumpToGroup">
                      <span class="elLink">{{ moreStr }}</span>
                    </el-link>
                  </span>
                </div>
              </el-col>
            </el-row>
          </div>
        </template>
        <template slot="content">
          <div v-if="tabIndex1 === 1" style="height: 290px; overflow: hidden">
            <el-carousel v-if="combArrays.length" :autoplay="false" arrow="always" height="100%" style="height: 100%; width: 100%; margin: auto">
              <el-carousel-item v-for="(combArray, index) of combArrays" :key="index">
                <el-row :gutter="20" style="padding: 20px 0px">
                  <template>
                    <el-col v-for="(item, index) of combArray" :key="index" :span="8">
                      <el-row align="middle">
                        <el-col :span="24">
                          <div>
                            <div class="over-flow-nowarp comb-title" @click="handleMNZH(item)">
                              {{ item.FUNDNAME | noDataFilter }}
                            </div>
                            <el-row align="middle" type="flex">
                              <el-col :span="12"><span>持有子基金数量</span></el-col>
                              <el-col :span="12">
                                <div class="comb-income over-flow-nowarp" style="text-align: right">
                                  {{ item.F_FUNDSNUM | noDataFilter }}
                                </div>
                              </el-col>
                            </el-row>
                          </div>
                          <div class="line"></div>
                        </el-col>
                      </el-row>
                      <el-row class="elRowClass">
                        <el-col :span="12">
                          <span>成立日期</span>
                        </el-col>
                        <el-col :span="12">
                          <div class="over-flow-nowarp" style="text-align: right">
                            {{ item.CREATEDATE | noDataFilter }}
                          </div>
                        </el-col>
                      </el-row>
                      <el-row class="elRowClass" style="padding: 10px 0">
                        <el-col :span="12">
                          <span>业绩基准</span>
                        </el-col>
                        <el-col :span="12">
                          <div class="over-flow-nowarp" style="text-align: right">
                            {{ item.VC_BE_NAME | noDataFilter }}
                          </div>
                        </el-col>
                      </el-row>
                      <el-row class="elRowClass">
                        <el-col :span="14">
                          <span>初始资金(亿)</span>
                        </el-col>
                        <el-col :span="10">
                          <div class="over-flow-nowarp" style="text-align: right">
                            {{ item.PRICE | priceFormat | noDataFilter }}
                          </div>
                        </el-col>
                      </el-row>
                      <div class="mnzhBtn" @click="handleQuickBtn(item)">快速调仓</div>
                      <div class="mnzhBtn" @click="handleHCBtn(item)">回测分析</div>
                    </el-col>
                  </template>
                </el-row>
              </el-carousel-item>
            </el-carousel>
            <div v-else class="noDataStyle">
              <img :src="imgUrl" alt="" />
            </div>
          </div>
          <div v-if="tabIndex1 === 2" style="height: 290px; overflow: hidden">
            <el-carousel v-if="combArraysTrue.length" :autoplay="false" arrow="always" height="100%" style="height: 100%; width: 100%; margin: auto">
              <el-carousel-item v-for="(combArray, index) of combArraysTrue" :key="index">
                <el-row :gutter="20" style="padding: 10px 0px">
                  <template>
                    <el-col v-for="(item, index) of combArray" :key="index" :span="8">
                      <el-row>
                        <el-col :span="24">
                          <div>
                            <!-- <div> -->
                            <div class="over-flow-nowarp comb-title" @click="handleWDZH(item)">
                              {{ item.VC_FUNDNAME | noDataFilter }}
                            </div>
                            <!-- </div> -->
                            <div>
                              <span>{{ item.D_GZ_DATE | noDataFilter }}</span>
                            </div>
                            <div class="over-flow-nowarp">近一周盈亏额（元）</div>
                            <!-- <div> -->
                            <div class="over-flow-nowarp comb-income">{{ item.F_INCOME | moneyYuan }}</div>
                            <!-- </div> -->
                          </div>
                          <myecharts
                            :id="item.VC_FUNDCODE + '_group'"
                            :ref="item.VC_FUNDCODE + '_group'"
                            :options="item.option"
                            resize-dom="cmbfof"
                            style="width: 100%; height: 50px; margin-top: 20px"
                          ></myecharts>
                          <!-- <img :src="require(`./img/second1.png`)" height="100px" width="100%"/> -->
                        </el-col>
                        <!-- <el-col :span="2">
                          <el-divider
                            v-if="item.divider"
                            content-position="center"
                            direction="vertical"
                            height="30px;"
                          />
                        </el-col> -->
                      </el-row>
                      <el-row class="elRowClass" style="margin-top: 20px">
                        <el-col :span="12">
                          <span>收益率</span>
                        </el-col>
                        <el-col :span="12">
                          <div class="search_button_com" style="padding-right: 0px">
                            <span v-if="item.F_YIELD > 0" class="rate-return-red">
                              {{ item.F_YIELD | numberToFixedStr(2, 100, '%') }}
                            </span>
                            <span v-if="item.F_YIELD == 0">
                              {{ item.F_YIELD | numberToFixedStr(2, 100, '%') }}
                            </span>
                            <span v-if="item.F_YIELD < 0" class="rate-return-green">
                              {{ item.F_YIELD | numberToFixedStr(2, 100, '%') }}
                            </span>
                            <span v-if="item.F_YIELD == undefined" class="rate-return-green">
                              {{ item.F_YIELD | noDataFilter }}
                            </span>
                          </div>
                        </el-col>
                      </el-row>
                      <el-row class="elRowClass">
                        <el-col :span="12">
                          <span>最大回撤</span>
                        </el-col>
                        <el-col :span="12">
                          <div class="search_button_com" style="padding-right: 0px">
                            <!-- <span style="color: green;">-{{ item.ZDHC | numberToFixedStr(2, 100, '%') }}</span> -->
                            <span>{{ item.F_MAXHC | numberToFixedStr(2, 100, '%') }}</span>
                          </div>
                        </el-col>
                      </el-row>
                      <el-row class="elRowClass">
                        <el-col :span="12">
                          <span>运行天数</span>
                        </el-col>
                        <el-col :span="12">
                          <div class="search_button_com" style="padding-right: 0px">
                            <span>{{ item.F_DAYS | noDataFilter }}</span>
                          </div>
                        </el-col>
                      </el-row>
                    </el-col>
                  </template>
                </el-row>
              </el-carousel-item>
            </el-carousel>
            <div v-else class="noDataStyle">
              <img :src="imgUrl" alt="" />
            </div>
          </div>
          <div style="border-bottom: 1px solid #333333"></div>
        </template>
      </box-template>
    </el-col>
    <el-col :span="8">
      <jnylfcljjjzzs></jnylfcljjjzzs>
      <div style="border-bottom: 1px solid #333333"></div>
    </el-col>
  </el-row>
</template>
<script>
import jnylfcljjjzzs from './jnylfcljjjzzs'
import boxTemplate from './boxTemplate'
import boxTemplate1 from './boxTemplate1'
import myecharts from '@/components/Echarts'
import Pagination from '@/components/Pagination'
import bygclsybx from './bygclsybx'
import commonApi from '@/api/common'
import { merger_back_objs } from '@/utils'
import img from '@/assets/img/nullData.png'
import fun from '@/filters/common'
import pageApi from '@/api/simulationGroup'

export default {
  components: { boxTemplate, boxTemplate1, myecharts, Pagination, bygclsybx, jnylfcljjjzzs },
  data() {
    return {
      tabIndex1: 1,
      isActive: '模拟组合',
      combArrays: [],
      combArraysTrue: [],
      formInline: {
        pageNum: 1,
        pageSize: 10
      },
      moreStr: 'More>',
      imgUrl: img,
      total: 5,
      tableData3: [],
      setupInfoArrs: [],
      setupInfoArr: [],

      hotProductArr: [],
      listArr: [
        {
          label: '精选榜单1',
          value: 'jxbd1'
        },
        {
          label: '精选榜单2',
          value: 'jxbd2'
        },
        {
          label: '精选榜单3',
          value: 'jxbd3'
        }
      ],
      // isActive:'jxbd',
      isActive1: '',
      active1Item: ''
    }
  },
  async mounted() {
    this.getSetupInfo()

    // 获取热点产品
    await this.getHotProduct()

    this.getAnalogGroup()
    this.getTrueGroup()
  },
  filters: {
    priceFormat(value) {
      if (value != null || value != undefined || value != '') {
        value = parseFloat(value / 10000).toFixed(2)
      }
      return value
    }
  },
  methods: {
    /**
     * @description 我的模组根据标签跳转more页面
     */
    jumpToGroup() {
      this.$store.commit('SET_FROMPAGEJUMP', true)
      if (this.isActive === '模拟组合') {
        this.$router.push({
          path: '/tqgl/mnzh/mnzh',
          query: {
            list: {
              FUNDNAME: undefined
            }
          }
        })
      } else if (this.isActive === '真实组合') {
        this.$router.push({
          path: '/thgl/zhfx/wdzh',
          query: {
            list: {
              VC_FUNDNAME: undefined
            }
          }
        })
      }
    },
    handleButtonClick(value) {
      this.isActive = value
      if (value === '模拟组合') {
        this.tabIndex1 = 1
      } else {
        this.tabIndex1 = 2
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
    handleMNZH(item) {
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/tzgl/mnzh',
        query: {
          list: item
        }
      })
    },
    handleWDZH(item) {
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/thgl/zhfx/wdzh',
        query: {
          list: { VC_FUNDNAME: item.VC_FUNDNAME }
        }
      })
    },
    // 快速调仓按钮
    async handleQuickBtn(item) {
      await this.selectAnalogCombInfoQuick(item.FUNDNAME, item.VC_PA_FUNDCODE)
    },
    // 回测分析按钮
    async handleHCBtn(item) {
      await this.selectAnalogCombInfoHC(item.FUNDNAME, item.VC_PA_FUNDCODE)
    },
    // 快速调仓按钮
    async handleQuickBtn(item) {
      await this.selectAnalogCombInfoQuick(item.FUNDNAME, item.VC_PA_FUNDCODE)
    },
    // 回测分析按钮
    async handleHCBtn(item) {
      await this.selectAnalogCombInfoHC(item.FUNDNAME, item.VC_PA_FUNDCODE)
    },
    // 查询模拟组合的信息
    selectAnalogCombInfoQuick(comebineName, comebineCode) {
      if (comebineName == '') {
        return
      }
      return new Promise((resolve, reject) => {
        const params = {
          combineName: comebineName,
          limit: 10,
          offset: (1 - 1) * 10,
          orderString: 'createTime desc'
        }
        pageApi.combineSelect(params).then((res) => {
          let { data, status, statusText } = res
          if (status == 200) {
            if (data && data.rows && data.rows.length > 0) {
              if (data.rows.length == 1) {
                this.$store.commit('SET_FROMPAGEJUMP', true)
                this.$router.push({
                  path: '/tqgl/tc',
                  query: {
                    combList: data.rows[0]
                  }
                })
              } else {
                let row = null
                for (let i = 0; i < data.rows.length; i++) {
                  let temp = data.rows[i]
                  if (temp.combineCode == comebineCode) {
                    row = temp
                    break
                  }
                }
                if (row) {
                  this.$store.commit('SET_FROMPAGEJUMP', true)
                  this.$router.push({
                    path: '/tqgl/tc',
                    query: {
                      combList: row
                    }
                  })
                } else {
                  this.$message.closeAll()
                  this.$message.warning('跳转调仓失败，没有该模拟组合')
                }
              }
            } else {
              this.$message.closeAll()
              this.$message.warning('跳转调仓失败，没有该模拟组合')
            }
          } else {
            this.$message.closeAll()
            this.$message.warning('跳转调仓失败，没有该模拟组合')
          }
        })
      })
    },
    selectAnalogCombInfoHC(comebineName, comebineCode) {
      if (comebineName == '') {
        return
      }
      return new Promise((resolve, reject) => {
        const params = {
          combineName: comebineName,
          limit: 10,
          offset: (1 - 1) * 10,
          orderString: 'createTime desc'
        }
        pageApi.combineSelect(params).then((res) => {
          let { data, status, statusText } = res
          if (status == 200) {
            if (data && data.rows && data.rows.length > 0) {
              if (data.rows.length == 1) {
                this.$store.commit('SET_FROMPAGEJUMP', true)
                this.$router.push({
                  path: '/tqgl/hcfx',
                  query: {
                    groupList: data.rows[0]
                  }
                })
              } else {
                let row = null
                for (let i = 0; i < data.rows.length; i++) {
                  let temp = data.rows[i]
                  if (temp.combineCode == comebineCode) {
                    row = temp
                    break
                  }
                }
                if (row) {
                  this.$store.commit('SET_FROMPAGEJUMP', true)
                  this.$router.push({
                    path: '/tqgl/hcfx',
                    query: {
                      groupList: row
                    }
                  })
                } else {
                  this.$message.closeAll()
                  this.$message.warning('跳转调仓失败，没有该模拟组合')
                }
              }
            } else {
              this.$message.closeAll()
              this.$message.warning('跳转调仓失败，没有该模拟组合')
            }
          } else {
            this.$message.closeAll()
            this.$message.warning('跳转调仓失败，没有该模拟组合')
          }
        })
      })
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

    more() {
      this.$router.push({
        path: '/hydt/rdjgdt'
      })
    },
    Pagination() {},

    //获取机构信息
    getSetupInfo() {
      commonApi
        .getDataBysqlCode({
          indexCode: 'bc6925b1-1e8c-40ca-9455-aa42e501bef9'
        })
        .then((res) => {
          let { status, data } = res.data
          if (status === 0) {
            this.setupInfoArrs = []
            for (var i = 0; i < data.length; i += 3) {
              this.setupInfoArrs.push(data.slice(i, i + 3))
            }
          }
        })
        .catch(() => {})
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
    /**
     * @description 跳转管理人详情
     */
    jumpToManager(data) {
      let newObj = {
        company_id: data.COMPANY_ID,
        manager_name: data.COMPANY_NAME
      }
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/tqgl/glrxq',
        query: { managerList: newObj }
      })
    }
  }
}
</script>
<style lang="scss" scoped>
.comb-title {
  color: #005ba1;
  font-size: 16px;
  cursor: pointer;
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

.line {
  height: 1px;
  border-bottom: 1px solid #f2f2f2;
  margin: 10px 0 15px;
}

.elRowClass {
  line-height: 21px;
}
.elRowClassOther {
  line-height: 21px;
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
    width: 90px;
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
    width: 90px;
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
    left: 173px;
    line-height: 20px;
    width: 90px;
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
    width: 120px;
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

.el-carousel__item {
  z-index: -1;
}

.el-carousel__item.is-active {
  z-index: 2;
}
::v-deep .el-table__body {
  margin-right: 12px !important;
}
.tableOverflow {
  ::v-deep .el-table--scrollable-y .el-table__body-wrapper {
    overflow-y: auto !important;
  }
}
.font-special-color {
  color: #005ba1;
}

.over-flow-nowarp {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  -o-text-overflow: ellipsis;
}

::v-deep .el-table--scrollable-y .el-table__body-wrapper {
  overflow-y: hidden;
}

::v-deep .el-table thead tr th {
  background-color: white !important;
}

.dashboard-title {
  font-size: 18px;
  // font-weight: 600;
  margin-right: 8px;
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

.icon-style {
  margin-bottom: 0px !important;
  font-size: 14px;
}

.icon-style-arrow {
  margin-bottom: 0px !important;
  font-size: 14px;
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
  font-size: 14px;
  color: #005ba1;
  line-height: 30px;
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
  color: #005ba1;
  cursor: pointer;

  .fund_name {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    margin-right: 5px;
  }
}
.noDataStyle {
  text-align: center;
  height: 290px;
}
.noDataStyle img {
  position: relative;
  top: 45px;
}
.title {
  height: 30px;
}
.title-button {
  display: inline-block;
  border: 1px solid #356385;
  // width: 70px;
  height: 22px;
  line-height: 20px;
  font-size: 14px;
  text-align: center;
  border-right: none;
  padding: 0 15px;
}
.title-button-left {
  -webkit-border-radius: 40px 0px 0px 40px;
  -moz-border-radius: 40px 0px 0px 40px;
  border-radius: 40px 0px 0px 40px;
}
.title-button-right {
  border-right: 1px solid #356385;
  -webkit-border-radius: 0px 40px 40px 0px;
  -moz-border-radius: 0px 40px 40px 0px;
  border-radius: 0px 40px 40px 0px;
}
.button-active {
  background-color: #6b8da6;
  color: white;
}
.item-active {
  color: #005ba1;
}
.noDataStyle {
  text-align: center;
  height: 300px;
}

.noDataStyle img {
  position: relative;
  top: 45px;
}
</style>

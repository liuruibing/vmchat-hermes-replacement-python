<template>
  <div class="simulation-group">
    <el-card>
      <div slot="header" class="clearfix">
        <div class="card-header">
          <span class="title-name">
            <span>模拟组合</span>
          </span>
          <span class="link-more" @click="jumpToGroup">更多 ></span>
        </div>
      </div>
      <div class="content">
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
                          <el-col :span="16"><span>持有子基金数量</span></el-col>
                          <el-col :span="8">
                            <div class="comb-income over-flow-nowarp" style="text-align: left;">
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
                      <div class="over-flow-nowarp" style="text-align: left;">
                        {{ item.CREATEDATE | noDataFilter }}
                      </div>
                    </el-col>
                  </el-row>
                  <el-row class="elRowClass" style="padding: 10px 0">
                    <el-col :span="12">
                      <span>业绩基准</span>
                    </el-col>
                    <el-col :span="12">
                      <div class="over-flow-nowarp" style="text-align: left;">
                        {{ item.VC_BE_NAME | noDataFilter }}
                      </div>
                    </el-col>
                  </el-row>
                  <el-row class="elRowClass">
                    <el-col :span="14">
                      <span>初始资金(亿)</span>
                    </el-col>
                    <el-col :span="10">
                      <div class="over-flow-nowarp" style="text-align: left;">
                        {{ item.PRICE | priceFormat | noDataFilter }}
                      </div>
                    </el-col>
                  </el-row>
                  <div class="mnzhBtn" @click="handleQuickBtn(item)">快速调仓</div>
                  <div class="hcfxBtn" @click="handleHCBtn(item)">回测分析</div>
                </el-col>
              </template>
            </el-row>
          </el-carousel-item>
        </el-carousel>
        <div v-else class="noDataStyle">
          <img :src="imgUrl" alt="" />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import commonApi from '@/api/common'
import fun from '@/filters/common'
import img from '@/assets/img/nullData.png'
import pageApi from '@/api/simulationGroup'

export default {
  name: 'SimulationGroup',
  data() {
    return {
      combArrays: [],
      imgUrl: img
    }
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
    initData() {
      this.getAnalogGroup()
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
          }
        })
        .catch(() => {})
    },
    handleMNZH(item) {
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/tqgl/mnzh/mnzh',
        query: {
          list: item
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
                    combList: data.rows[0],
                    type: 'tc'
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
    jumpToGroup() {
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/tqgl/mnzh/mnzh',
        query: {
          list: {
            FUNDNAME: undefined
          }
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
@import url('../../style/index.scss');
::v-deep .el-carousel__item {
  z-index: -1;
}

::v-deep .el-carousel__item.is-active {
  z-index: 2;
}
::v-deep .el-carousel__indicators.el-carousel__indicators--horizontal {
  display: none;
}
.comb-income {
  font-size: 18px;
}
.comb-title {
  cursor: pointer;
  color: #A15008;
  font-size: 16px;
}
.elRowClass {
  line-height: 21px;
}
.mnzhBtn {
  border: 1px solid #804f2b;
  border-radius: 40px;
  height: 30px;
  line-height: 30px;
  font-size: 14px;
  cursor: pointer;
  color: #612D10;
  font-weight: 500;
  text-align: center;
  margin-top: 15px;
}
.hcfxBtn {
  border: 0px;
  background: linear-gradient(to right, #F5D7BC, #E0B794);
  font-weight: 500;
  color: #612D10;
  border-radius: 40px;
  height: 30px;
  line-height: 30px;
  font-size: 14px;
  cursor: pointer;
  text-align: center;
  margin-top: 15px;
}
.line {
  height: 1px;
  border-bottom: 1px solid #f2f2f2;
  margin: 10px 0 15px;
}
::v-deep .el-carousel__arrow{
  background-color: rgba(31,45,61,0) ;
}
::v-deep .el-carousel__arrow:hover{
  background-color: rgba(31,45,61,.23) ;
}
</style>

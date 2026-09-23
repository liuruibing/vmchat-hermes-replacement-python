<template>
  <div class="shichangdongtai">
    <div class="title">
      <el-row type="">
        <div style="position: relative">
          <el-col :span="22">
            <div style="position: absolute;top: -5px;">
              <span class="titletitle">市场动态</span>
              <span
                :class="['title-button-left', isActive === '融智指数' ? 'button-active' : '']"
                @click="handleButtonClick('融智指数')"
              >
                融智指数
              </span>
              <span
                :class="['title-button-center', isActive === '股票市场' ? 'button-active' : '']"
                @click="handleButtonClick('股票市场')"
              >
                股票市场
              </span>
              <span
                :class="['title-button-right', isActive === '债券市场' ? 'button-active' : '']"
                @click="handleButtonClick('债券市场')"
              >
                债券市场
              </span>
            </div>
          </el-col>
          <el-col :span="2">
            <div style="position: absolute;right: 0px;">
              <span style="font-size: 14px">
                <el-link :underline="false" type="primary" @click="">
                  <span class="elLink">{{ moreStr }}</span>
                </el-link>
              </span>
            </div>
          </el-col>
        </div>
      </el-row>
    </div>
    <div class="content">
      <myChart
        id="shichangdongtaiChart"
        ref="shichangdongtaiChart"
        :options="chartOption"
        class="echarts_box"
        resize-dom="cmbfof"
      />
    </div>
  </div>
</template>

<script>
import testData from './js/shichangdongtai'
import myChart from '@/components/Echarts'

export default {
  name: 'Shichangdongtai',
  components: {
    myChart
  },
  data() {
    return {
      chartOption: {},
      isActive: '融智指数', // 控制菜单展示
      moreStr: 'More>'
    }
  },
  mounted() {
    this.init()
  },
  methods: {
    init() {
      this.chartInit()
    },
    handleButtonClick(value) {
      this.isActive = value
    },
    chartInit() {
      let base = +new Date(2018, 7, 1)
      const oneDay = 24 * 3600 * 1000
      const date = []
      // let data = [Math.random() * 300];
      for (let i = 1; i < 1000; i++) {
        var now = new Date((base += oneDay))
        date.push([now.getFullYear(), now.getMonth() + 1, now.getDate()].join('/'))
        // data.push(Math.round((Math.random() - 0.5) * 20 + data[i - 1]));
      }
      const data = []
      testData.data.forEach(item => {
        data.push((item * 0.1).toFixed(2))
      })
      this.chartOption = {
        tooltip: {
          trigger: 'axis'
          // position: function (pt) {
          //   return [pt[0], "10%"];
          // }
        },
        color: ['#42b1ff'],
        grid: {
          left: '30px',
          right: '4%',
          bottom: '5%',
          top: '5%',
          containLabel: true
        },
        // title: {
        //   left: "center",
        //   text: "Large Ara Chart"
        // },
        // toolbox: {
        //   feature: {
        //     dataZoom: {
        //       yAxisIndex: "none"
        //     },
        //     restore: {},
        //     saveAsImage: {}
        //   }
        // },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          axisLine: {
            show: false
          },
          axisTick: {
            show: false
          },
          data: date,
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
          // data: ["2018.07", "2018.09", "2018.11", "2019.01", "2019.03", "2019.05", "2019.07"]
        },
        yAxis: {
          type: 'value',
          boundaryGap: true,
          name: '收益率(%)',
          nameLocation: 'middle',
          nameGap: 40,
          nameRotate: 90,
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
          },
          axisLabel: {
            formatter: '{value}%'
          }
        },
        series: [
          {
            // data: [15, 23, 20, 26, 13, 14, 26],
            data: data,
            type: 'line',
            symbol: 'none',
            lineStyle: {
              normal: {
                width: 0.5
              }
            },
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
    }
  }
}
</script>

<style lang="scss" scoped>
.shichangdongtai {
  height: 180px;
  .title {
    height: 30px;

    .titletitle {
      font-size: 18px;
      margin-right: 12px;
      //vertical-align: middle;
      color: #333;
      text-align: center;
      // font-weight: 600;
    }

    .title-button-left {
      display: inline-block;
      border: 1px solid #356385;
      width: 70px;
      height: 22px;
      padding-left: 13px;
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
      padding-left: 10px;
    }

    .title-button-right {
      display: inline-block;
      border: 1px solid #356385;
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

    .elLink {
      width: 34px;
      font-size: 14px;
      color: #005ba1;
      line-height: 30px;
      padding: 3px;
    }

    //.tab {
    //  color: #c8993d;
    //  font-size: 14px;
    //  cursor: pointer;
    //}
  }

  .content {
    //border: 1px solid #ccc;
    height: 150px;
    // padding-top: 4px;
    margin-top: 10px;
  }
}

.echarts_box {
  height: 150px;
  width: 100%;
}
</style>

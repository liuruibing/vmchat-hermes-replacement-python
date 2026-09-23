<template>
  <div class="jnylfcljjjzzs">
    <div class="title">
      <el-row type="flex">
        <el-col :span="22">
          <span class="title_left_">
            <span class="titletitle">
              广发私募指数当年走势
              <span>{{ '（' + lastDate + '）' }}</span>
            </span>
          </span>
        </el-col>
        <el-col :span="2">
          <div class="search_button_com">
            <span style="font-size: 14px">
              <el-link :underline="false" type="primary" @click="handleMoreClick">
                <span class="elLink">{{ moreStr }}</span>
              </el-link>
            </span>
          </div>
        </el-col>
      </el-row>
    </div>
    <div class="content">
      <myChart
        id="jnylfcljjjzzsChart"
        ref="jnylfcljjjzzsChart"
        :options="chartOption"
        class="echarts_box"
        resize-dom="cmbfof"
      />
    </div>
  </div>
</template>

<script>
import myChart from '@/components/Echarts'
import request from '@/utils/request'

export default {
  name: 'jnylfcljjjzzs',
  components: {
    myChart
  },
  data() {
    return {
      chartOption: {},
      lastDate: '',
      moreStr: 'More>'
    }
  },
  mounted() {
    this.init()
  },
  methods: {
    handleMoreClick() {
      this.$router.push('/hydt/zssmqxzs:type=SC')
    },
    init() {
      this.getChartsData()
    },
    /**
     * @description 后端接口，目前注释状态，3-31先不上
     */
    getChartsData() {
      const params = {
        indexCode: 'cbe35faa-3565-4267-8fc9-daa8c0048426'
      }
      request({
        url: `/api/report/v1.0/data/sql/cbe35faa-3565-4267-8fc9-daa8c0048426`,
        method: 'post',
        data: params
      }).then(res => {
        if (res.data.status === 0) {
          const resultData = res.data.data || []
          if (resultData && resultData.length) {
            const xData = resultData.map(item => item.D_DATE) || []
            const ALData = resultData.map(item => item.F_AL) || []
            const LNData = resultData.map(item => item.F_LN) || []
            const AFData = resultData.map(item => item.F_AF) || []
            const CTData = resultData.map(item => item.F_CT) || []
            const FFData = resultData.map(item => item.F_FF) || []
            const HSData = resultData.map(item => item.F_HS) || []
            this.lastDate = xData[xData.length - 1]
            const allData = [...ALData, ...LNData, ...AFData, ...CTData, ...FFData, ...HSData]
            let max = Math.max(...allData)
            // max = max + 0.01
            let min = Math.min(...allData)
            // min = min - 0.01
            this.chartInit(xData, ALData, LNData, AFData, CTData, FFData, HSData, max, min)
          }
        }
      })
    },
    chartInit(xData, ALData, LNData, AFData, CTData, FFData, HSData, max, min) {
      this.chartOption = {
        tooltip: {
          trigger: 'axis',
          formatter: params => {
            let tip = params[0].name + '<br>'
            for (let i = 0; i < params.length; i++) {
              tip +=
                params[i].marker + params[i].seriesName + ': ' + Number(params[i].value).toFixed(2) + '<br>'
            }
            return tip
          }
        },
        color: ['#fc6769', '#d2a25a', '#789d51', '#6c50f3', '#396f92', '#64AAEF'],
        legend: {
          top: 5,
          data: [
            { name: '综合' },
            { name: '股票多头' },
            { name: '股票中性' },
            { name: 'CTA' },
            { name: 'FOF' },
            { name: '沪深300', icon: 'roundRect' }
          ],
          itemWidth: 18,
          itemHeight: 12,
          textStyle: { color: '#000', fontSize: 12 }
        },
        grid: {
          left: '30px',
          right: '4%',
          bottom: '8%',
          top: '15%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: xData,
          offset: 12,
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
          // data: ["18.09", "18.11", "19.01", "19.03", "19.05", "19.07", "19.09"]
        },
        yAxis: {
          type: 'value',
          position: 'right',
          axisLabel: {},
          splitNumber: 1,
          min: (min - 0.01).toFixed(2),
          max: (max + 0.01).toFixed(2),
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
        series: [
          {
            name: '股票多头',
            type: 'line',
            symbol: 'none',
            smooth: true,
            lineStyle: {
              normal: {
                width: 0.5
              }
            },
            data: LNData
            // data: ["1.20", 1.32, 1.01, 1.34, 0.9, 2.3, 2.1]
          },
          {
            name: '股票中性',
            type: 'line',
            symbol: 'none',
            smooth: true,
            lineStyle: {
              normal: {
                width: 0.5
              }
            },
            data: AFData
            // data: [2.2, 1.82, 1.91, 2.34, 2.9, 3.3, 3.1]
          },
          {
            name: 'CTA',
            type: 'line',
            symbol: 'none',
            smooth: true,
            lineStyle: {
              normal: {
                width: 0.5
              }
            },
            data: CTData
            // data: [1.5, 2.32, 2.01, 1.54, 1.9, 3.3, 4.1]
          },
          {
            name: 'FOF',
            type: 'line',
            symbol: 'none',
            smooth: true,
            lineStyle: {
              normal: {
                width: 0.5
              }
            },
            data: FFData
            // data: [1.5, 2.32, 2.01, 1.54, 1.9, 3.3, 4.1]
          },
          {
            name: '综合',
            type: 'line',
            symbol: 'none',
            smooth: true,
            lineStyle: {
              normal: {
                width: 0.5
              }
            },
            data: ALData
          },
          {
            name: '沪深300',
            type: 'line',
            symbol: 'none',
            smooth: true,
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
            },
            data: HSData
          }
        ]
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.jnylfcljjjzzs {
  .elLink {
    width: 34px;
    font-size: 14px;
    color: #005ba1;
    line-height: 30px;
    padding: 3px;
  }
  .title {
    margin: 16px 0;

    .title_left_ {
      .titletitle {
        font-size: 18px;
        //  font-weight: 600;
        margin-right: 37px;
      }

      .titletitle span {
        font-size: 14px;
        position: relative;
        top: -2px;
      }

      .tab {
        color: #c8993d;
      }
    }

    .more {
      width: 34px;
      color: #2672bc;
      text-align: right;
    }
  }

  .content {
    //border: 1px solid #ccc;
    height: 284px;
    //padding-top: 10px;
  }
}

.echarts_box {
  height: 284px;
  width: 100%;
}
</style>

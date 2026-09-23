<template>
  <div class="yh-private-index">
    <el-card>
      <div slot="header" class="clearfix">
        <div class="card-header">
          <span class="title-name">
            <span>广发私募指数表现</span>
             <el-tooltip class="table_header_icon" effect="dark" placement="top">
            <span slot="content">广发私募指数由广发证券资产托管部编制，不代表市场整体表现，不对市场未来表现作任何预测和保证</span>
            <i class="el-icon-question" style="cursor: pointer"></i>
          </el-tooltip>
            <span class="title_left_">
              <span class="titletitle">
                <span style="font-weight:normal;">{{ '（数据截止：' + lastDate + '）' }}</span>
              </span>
            </span>
          </span>
          <div class="header-actions">
          <span class="link-download" @click="handleDownload">
          <i class="el-icon-download"></i>
          </span>
            <span class="link-more" @click="handleMoreClick">更多 ></span>
          </div>

        </div>
      </div>
      <div class="content">
        <myChart id="yhPrivateIndex" ref="yhPrivateIndex" :options="chartOption" class="echarts_box" resize-dom="cmbfof" />
      </div>
    </el-card>
  </div>
</template>

<script>
import myChart from '@/components/Echarts'
import request from '@/utils/request'
import { merger } from '@/utils'
import { CHART_OPTIONS_COLOR } from '../scripts/constant'
import XLSX from 'xlsx'
export default {
  name: 'YhPrivateIndex',
  components: { myChart },
  data() {
    return {
      lastDate: '-',
      chartOption: {
        tooltip: {
          appendToBody: true,
          trigger: 'axis',
          formatter: (params) => {
            let tip = params[0].name + '<br>'
            for (let i = 0; i < params.length; i++) {
              tip += params[i].marker + params[i].seriesName + ': ' + Number(params[i].value).toFixed(2) + '<br>'
            }
            return tip
          }
        },
        color: CHART_OPTIONS_COLOR,
        legend: {
          top: 5,
          data: [],
          itemWidth: 18,
          itemHeight: 12,
          type: 'scroll',
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
          data: [],
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
        },
        yAxis: {
          type: 'value',
          position: 'right',
          axisLabel: {
            // 使用 formatter 格式化标签
            formatter: function(value) {
              return value.toFixed(2) + '%'; // 保留两位小数
            }
          },
          splitNumber: 1,
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
            show: false,
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
        series: []
      },
      chartRawData: []
    }
  },
  methods: {
    handleDownload() {
      const dates = this.chartOption.xAxis.data || []; // 图表x轴日期
      const legendData = this.chartOption.legend.data || []; // 图表图例
      const seriesData = this.chartOption.series || []; // 图表数据

      if (!dates.length || !legendData.length || !seriesData.length) {
        this.$message.warning('暂无可下载的图表数据！');
        return;
      }

      // 日期为行，指数名为列，直接取series里的数值
      const excelData = [];
      dates.forEach((date, dateIndex) => {
        const row = { '日期': date };
        // 遍历每个指数，从对应的series.data中取数值
        legendData.forEach((indexName, legendIndex) => {
          const targetSeries = seriesData.find(item => item.name === indexName);
          if (targetSeries && targetSeries.data.length > dateIndex) {
            const value = targetSeries.data[dateIndex];
            row[indexName] = value === '-' ? '-' : Number(value).toFixed(2);
          } else {
            row[indexName] = '-';
          }
        });
        excelData.push(row);
      });

      // 生成Excel并下载
      const worksheet = XLSX.utils.json_to_sheet(excelData)
      const workbook = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(workbook, worksheet, '广发私募指数表现')
      const fileName = `广发私募指数表现_数据截止${this.lastDate || new Date().toISOString().split('T')[0]}.xlsx`
      XLSX.writeFile(workbook, fileName)
      this.$message.success('广发私募指数表现数据下载成功！')
    },
    handleMoreClick() {
      this.$router.push({
        path: '/hydt/scbx/zssmqxzs:type=yhsmzs'
      })
    },
    initData() {
      this.getEndDate()
      this.getChartsData()
    },
    /** 获取echarts数据 */
    getChartsData() {
      const params = {
        indexCode: '30cad0b7-32a8-4152-9699-4bef0444a14a'
      }
      request({
        url: `/api/report/v1.0/data/sql/30cad0b7-32a8-4152-9699-4bef0444a14a`,
        method: 'post',
        data: params
      }).then((res) => {
        if (res.data.status === 0) {
          if (res.data.data && res.data.data.length) {
            this.chartRawData = res.data.data;
            let xData = Array.from(new Set(res.data.data.map((item) => item.D_DATE)))
            let seriesData = []
            let legendData = []
            let mergerData = merger(res.data.data, 'VC_INDEX_NAME')
            for (let i = 0; i < mergerData.length; i++) {
              let temp = mergerData[i]
              legendData.push(temp.VC_INDEX_NAME)
              let seriesObj = {
                name: temp.VC_INDEX_NAME || '-',
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
              if( temp.VC_INDEX_NAME === '沪深300') {
                seriesObj.areaStyle = {
                  opacity: 0.3  // 设置透明度
                }
              }
              if (temp.origin && origin.length > 0) {
                temp.origin.forEach((item) => {
                  seriesObj.data.push(item.F_YIELD * 100 || item.F_YIELD * 100 === 0 ? item.F_YIELD * 100 : '-')
                })
              }
              seriesData.push(seriesObj)
            }
            this.$nextTick(() => {
              this.chartOption.xAxis.data = xData
              this.chartOption.legend.data = legendData
              this.chartOption.series = seriesData
            })
          }
        }
      })
    },
    getEndDate() {
      const params = {
        indexCode: '4473832b-f34a-47b4-a214-b36ff683fd5f'
      }
      request({
        url: `/api/report/v1.0/data/sql/4473832b-f34a-47b4-a214-b36ff683fd5f`,
        method: 'post',
        data: params
      }).then((res) => {
        if (res.data.status === 0) {
          if (res.data.data && res.data.data.length) {
            this.lastDate = res.data.data[0].D_DATE || '-'
          }
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
@import url('../../style/index.scss');
.yh-private-index {
}
</style>

<template>
  <div class="factor-return">
    <el-card>
      <div slot="header" class="clearfix">
        <div class="card-header">
          <span class="title-name">
            <span>因子收益表现</span>
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
        <myChart id="factorReturn" ref="factorReturn" :options="chartOption" class="echarts_box" resize-dom="cmbfof" />
      </div>
    </el-card>
  </div>
</template>

<script>
import myChart from '@/components/Echarts'
import request from '@/utils/request'
import { CHART_OPTIONS_COLOR } from '../scripts/constant'
import { merger } from '@/utils'
import XLSX from 'xlsx'
export default {
  name: 'FactorReturn',
  components: { myChart },
  data() {
    return {
      chartOption: {
        tooltip: {
          appendToBody: true,
          trigger: 'axis',
          formatter: (params) => {
            let tip = `${params[0].name}<br>`;
            const tips = params
              .filter(param => param.value !== '-')
              .map(param => `${param.marker}${param.seriesName}: ${Number(param.value).toFixed(2)}<br>`)
              .join('');
            return tip + tips;
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
        series: []
      },
      lastDate: '-',
      chartRawData: []
    }
  },
  methods: {
    handleDownload() {
      const dates = this.chartOption.xAxis.data || []; // 图表x轴日期
      const factorNames = this.chartOption.legend.data || []; // 图表图例
      const seriesData = this.chartOption.series || []; // 图表数据

      if (!dates.length || !factorNames.length || !seriesData.length) {
        this.$message.warning('暂无可下载的图表数据！');
        return;
      }

      // 日期为行，因子名为列，直接取series里的数值
      const excelData = [];
      dates.forEach((date, dateIndex) => {
        const row = { '日期': date };
        factorNames.forEach((factorName) => {
          const targetSeries = seriesData.find(item => item.name === factorName);
          if (targetSeries && targetSeries.data.length > dateIndex) {
            const value = targetSeries.data[dateIndex];
            row[factorName] = value === '-' ? '-' : Number(value).toFixed(2);
          } else {
            row[factorName] = '-';
          }
        });
        excelData.push(row);
      });

      // 生成Excel并下载
      const worksheet = XLSX.utils.json_to_sheet(excelData)
      const workbook = XLSX.utils.book_new()
      XLSX.utils.book_append_sheet(workbook, worksheet, '因子收益表现')
      const fileName = `因子收益表现_数据截止${this.lastDate || new Date().toISOString().split('T')[0]}.xlsx`
      XLSX.writeFile(workbook, fileName)
      this.$message.success('因子收益表现数据下载成功！')
    },
    handleMoreClick() {
      this.$router.push({
        path: '/hydt/scbx/factorReturn'
      })
    },
    initData() {
      this.getEndDate()
      this.getChartsData()
    },
    /** 获取echarts数据 */
    getChartsData() {
      const params = {
        indexCode: '55f96100-bc5e-479e-806a-70d460c57905'
      }
      request({
        url: `/api/report/v1.0/data/sql/55f96100-bc5e-479e-806a-70d460c57905`,
        method: 'post',
        data: params
      }).then((res) => {
        if (res.data.status === 0) {
          if (res.data.data && res.data.data.length) {
            this.chartRawData = res.data.data;
            let xData = Array.from(new Set(res.data.data.map((item) => item.D_DATE)))
            let seriesData = []
            let legendData = []
            let mergerData = merger(res.data.data, 'VC_INDEX_SHORTNAME')
            for (let i = 0; i < mergerData.length; i++) {
              let temp = mergerData[i]
              legendData.push(temp.VC_INDEX_SHORTNAME)
              let seriesObj = {
                name: temp.VC_INDEX_SHORTNAME || '-',
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
              if( temp.VC_INDEX_SHORTNAME === '沪深300') {
                seriesObj.areaStyle = {
                  opacity: 0.3  // 设置透明度
                }
              }
              /*if (temp.origin && origin.length > 0) {
                temp.origin.forEach((item) => {
                  seriesObj.data.push(item.F_YIELD * 100 || item.F_YIELD * 100 === 0 ? item.F_YIELD * 100 : '-')
                })
              }*/
              seriesData.push(seriesObj)
            }
            for (let x = 0; x < seriesData.length; x++) {
              const datay = [];
              const seriesName = seriesData[x].name;
              for (let j = 0; j < xData.length; j++) {
                const date = xData[j];
                let found = false;
                for (let k = 0; k < res.data.data.length; k++) {
                  const item = res.data.data[k];
                  if (item.D_DATE === date && item.VC_INDEX_SHORTNAME === seriesName) {
                    datay.push(item.F_YIELD * 100);
                    found = true;
                    break;
                  }
                }
                if (!found) {
                  datay.push('-');
                }
              }
              seriesData[x].data = datay;
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
        indexCode: '513d3b33-ac98-48a6-ab22-eb952c428e77'
      }
      request({
        url: `/api/report/v1.0/data/sql/513d3b33-ac98-48a6-ab22-eb952c428e77`,
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
.factor-return {
}
</style>

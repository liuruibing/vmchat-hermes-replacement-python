<template>
  <div class="dataBoard ddportal-ui">
    <div class="funds-filter standard-form">
      <el-form :inline="true" :model="formQuery" ref="formQuery" :rules="searchRules">
        <el-row>
          <el-col :span="16">
            <!-- 查询 -->
            <el-form-item label="开始日期" prop="beginDate">
              <el-date-picker
                v-model="formQuery.beginDate"
                type="date"
                placeholder="选择开始日期"
                value-format="yyyy-MM-dd"
                size="small"
              />
            </el-form-item>
            <el-form-item label="结束日期" prop="endDate">
              <el-date-picker
                v-model="formQuery.endDate"
                type="date"
                placeholder="选择结束日期"
                value-format="yyyy-MM-dd"
                size="small"
              />
            </el-form-item>
            <el-form-item label="统计维度" prop="statistical">
              <el-select v-model="formQuery.statistical" clearable placeholder="请选择" size="small">
                <el-option label="用户" value="1"></el-option>
                <el-option label="机构" value="2"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item class="search_btn search_button_com">
              <el-button icon="el-icon-search" type="primary" size="small" @click="onSubmit('formQuery')">
                查询
              </el-button>
              <!--<el-button type="primary" size="small" icon="el-icon-bottom">-->
              <!--导出-->
              <!--</el-button>-->
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </div>
    <div class="chart-main">
      <div class="target-trend">
        <div class="chart-title">
          <div class="title-icon">
            <div class="color-box"></div>
          </div>
          <div class="title-txt">登录总量统计</div>
        </div>
        <div class="chart-content">
          <div
            id="dlzltj"
            ref="dlzltj"
            class="echarts_box"
            resize-dom="cmbfof"
          />
        </div>
        <div class="chart-title">
          <div class="title-icon">
            <div class="color-box"></div>
          </div>
          <div class="title-txt">系统登录情况排名</div>
          <div style="float: right;">
            <el-button type="primary" size="small" icon="el-icon-bottom" @click="exportData">
              导出
            </el-button>
          </div>
          <div style="clear: both;"></div>
        </div>
        <div class="chart-content">
          <div
            id="xtdlqkpm"
            ref="xtdlqkpm"
            class="echarts_box"
            resize-dom="cmbfof"
            style="float: left;width: 60%;height: 500px;"
          />
          <div style="float: right;width: 39%;height: 500px;">
            <vxe-table border show-header-overflow show-overflow auto-resize :data="tableData" stripe id="standard-table">
              <vxe-column field="YDATA1" title="排名" header-align="center" align="center" min-width="100">
                <template slot-scope="scope">
                  <span>{{ scope.row.YDATA1 | noDataFilter }}</span>
                </template>
              </vxe-column>
              <vxe-column field="YDATA" :title="theadtitle" header-align="center" align="center" min-width="100">
                <template slot-scope="scope">
                  <span>{{ scope.row.YDATA | noDataFilter }}</span>
                </template>
              </vxe-column>
              <vxe-column field="XDATA" title="登录次数" header-align="center" align="center" min-width="100">
                <template slot-scope="scope">
                  <span>{{ scope.row.XDATA | noDataFilter }}</span>
                </template>
              </vxe-column>
            </vxe-table>
          </div>
          <div style="clear: both;"></div>
          <div class="tips">备注：统计查询区间内查登录次数最多的前十大用户/机构</div>
        </div>
        <div class="chart-title" style="margin-top: 30px;">
          <div class="title-icon">
            <div class="color-box"></div>
          </div>
          <div class="title-txt">{{xzyhjgtj}}</div>
        </div>
        <div class="chart-content">
          <div
            id="xzyhjgtj"
            ref="xzyhjgtj"
            class="echarts_box"
            resize-dom="cmbfof"
          />
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { CHART_COLOR_ARR } from "@/metaData/enum.js"

  import commonApi from '@/api/common'
  import { downLoadFileByUrl } from '@/utils'
  import request from '@/utils/request'
  import myChart from '@/components/Echarts'
  import productSelector from '@/components/productSelector'
  import commonFun from '@/filters/new_common'

  export default {
    name: 'dataBoard',
    components: {
      commonApi, myChart, productSelector
    },
    data() {
      return {
        formQuery: {
          // 开始日期
          beginDate: '',
          // 结束日期
          endDate: '',
          // 统计维护
          statistical: '1'
        },
        searchRules: {
          beginDate: [
            { required: true, message: '请选择开始日期', trigger: 'blur' }
          ],
          endDate: [
            { required: true, message: '请选择结束日期', trigger: 'blur' }
          ]
        },
        xzyhjgtj: '',
        theadtitle: '',
        tableData: []
      }
    },
    mounted() {
      this.formQuery.endDate = commonFun.get_newDate()
      this.formQuery.beginDate = commonFun.getPreMonthDay(this.formQuery.endDate, 12)
      this.onSubmit('formQuery')
    },
    methods: {
      onSubmit(formName) {
        var self = this
        self.$refs[formName].validate(valid => {
          if (valid) {
            try {
              self.handledlzltjEchartsData()
              self.handledtableData()
              self.handlextdlqkpmEchartsData()
              self.handlxzyhjgtjEchartsData()
            } catch (e) {
            }
          } else {
            return false
          }
        })
      },
      handledlzltjEchartsData() {
        var indexCode = ''
        if (this.formQuery.statistical == '1') {
          //统计维度-用户
          indexCode = '3fd20731-74c7-4d94-be3a-b5cd56e2bf9c'
        } else {
          //统计维护-机构
          indexCode = '9f29f11f-c706-42e6-85d0-3a0aed29aae8'
        }
        const params = {
          indexCode: indexCode,
          statistical: this.formQuery.statistical || '',
          beginDate: this.formQuery.beginDate || '',
          endDate: this.formQuery.endDate || ''
        }

        request({
          url: `/api/report/v1.0/data/sql/${indexCode}`,
          method: 'post',
          data: params
        }).then(res => {

          if (res.data.status === 0) {
            const resultData = res.data.data || []
            console.log('用户总量统计')
            console.log(resultData)
            this.handledlzltjOptions(resultData)
          }
        })
      },
      handledlzltjOptions(data) {
        const xData = data.map(item => item.XDATA) || []
        console.log(xData)
        const yData1 = data.map(item => item.YDATA1) || []
        console.log(yData1)
        const yData2 = data.map(item => item.YDATA2) || []
        console.log(yData2)
        var myChart = this.$echarts.init(
          document.getElementById('dlzltj')
        )
        var legendData = []
        if (this.formQuery.statistical == '1') {
          legendData = ['登录用户总量', '用户登录总次数']
        } else {
          legendData = ['登录机构总量', '机构内登录总次数']
        }

        let colors = CHART_COLOR_ARR
        this.dlzltjOptions = {
          legend: {
            top: '3%',
            data: legendData,
            textStyle: { color: '#000', fontSize: 12 }
          },
          color: colors,
          grid: {
            left: '2%',
            right: '3%',
            bottom: '2%',
            top: '10%',
            containLabel: true
          },
          tooltip: {
            trigger: 'axis',
            formatter: params => {
              let tip = params[0].name + '<br>'
              for (let i = 0; i < params.length; i++) {
                if ((i + 1) % 5 == 0) {
                  tip += params[i].marker + params[i].seriesName + ': ' + Number(params[i].value).toFixed(0) + '<br>'

                } else {
                  tip += params[i].marker + params[i].seriesName + ': ' + Number(params[i].value).toFixed(0) + '&nbsp&nbsp&nbsp&nbsp'
                }
              }
              return tip
            }
          },
          xAxis: [
            {
              type: 'category',
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
              },
              data: xData
            }
          ],
          yAxis: [
            {
              name: '数量（个/次）',
              axisLine: {
                show: false
              },
              axisTick: {
                show: false
              },
              splitArea: {
                show: false
              },
              min: 'dataMin',
              splitLine: {
                show: true,
                lineStyle: {
                  color: '#e5e5e5',
                  type: 'dashed'
                }
              }
            }
          ],
          series: [{
            name: legendData[0],
            data: yData1,
            type: 'line',
            symbol: 'none'

          }, {
            name: legendData[1],
            data: yData2,
            type: 'line',
            symbol: 'none'

          }
          ]
        }
        myChart.setOption(this.dlzltjOptions)
      },
      handlextdlqkpmEchartsData() {

        var indexCode = ''
        if (this.formQuery.statistical == '1') {
          //统计维度-用户
          indexCode = '5afd8b96-a794-4d71-941b-b160bbdcb63d'
        } else {
          //统计维护-机构
          indexCode = '5bdebd2d-db02-44d0-91bd-c3fd198252e2'
        }
        const params = {
          indexCode: indexCode,
          statistical: this.formQuery.statistical || '',
          beginDate: this.formQuery.beginDate || '',
          endDate: this.formQuery.endDate || ''
        }

        request({
          url: `/api/report/v1.0/data/sql/${indexCode}`,
          method: 'post',
          data: params
        }).then(res => {

          if (res.data.status === 0) {
            const resultData = res.data.data || []
            this.handlextdlqkpmOptions(resultData)
          }
        })
      },
      handlextdlqkpmOptions(data) {

        const xData = data.map(item => item.XDATA) || []
        const yData = data.map(item => item.YDATA) || []
        const yData1 = data.map(item => item.YDATA1) || []

        var myChart = this.$echarts.init(
          document.getElementById('xtdlqkpm')
        )
        var legendData = []
        if (this.formQuery.statistical == '1') {
          legendData = ['用户']
          name = '用户名'
        } else {
          legendData = ['机构']
          name = '机构名'
        }

        let colors = CHART_COLOR_ARR
        this.extdlqkpmOptions = {
          legend: {
            top: '3%',
            data: legendData,
            textStyle: { color: '#000', fontSize: 12 }
          },
          color: colors,
          grid: {
            left: '2%',
            right: '5%',
            bottom: '2%',
            top: '10%',
            containLabel: true
          },
          tooltip: {
            trigger: 'axis',
            formatter: params => {
              let tip = params[0].name + '<br>'
              for (let i = 0; i < params.length; i++) {
                if ((i + 1) % 5 == 0) {
                  tip += params[i].marker + params[i].seriesName + ': ' + Number(params[i].value).toFixed(0) + '<br>'

                } else {
                  tip += params[i].marker + params[i].seriesName + ': ' + Number(params[i].value).toFixed(0) + '&nbsp&nbsp&nbsp&nbsp'
                }
              }
              return tip
            }
          },
          xAxis: [
            {
              name: '数量',
              type: 'value',
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
            }
          ],
          yAxis: [
            {
              name: name,
              type: 'category',
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
              data: yData
            }
          ],
          series: [{
            name: legendData[0],
            data: xData,
            type: 'bar',
            barMaxWidth: 35

          }
          ]
        }
        myChart.setOption(this.extdlqkpmOptions)

      },
      handledtableData() {
        var indexCode = ''
        if (this.formQuery.statistical == '1') {
          //统计维度-用户
          indexCode = '5afd8b96-a794-4d71-941b-b160bbdcb63d'
          this.theadtitle = '用户名'
        } else {
          //统计维护-机构
          indexCode = '5bdebd2d-db02-44d0-91bd-c3fd198252e2'
          this.theadtitle = '机构名'
        }
        const params = {
          indexCode: indexCode,
          statistical: this.formQuery.statistical || '',
          beginDate: this.formQuery.beginDate || '',
          endDate: this.formQuery.endDate || ''
        }

        request({
          url: `/api/report/v1.0/data/sql/${indexCode}`,
          method: 'post',
          data: params
        }).then(res => {

          if (res.data.status === 0) {
            this.tableData = res.data.data || []

          }
        })
      },
      handlxzyhjgtjEchartsData() {
        var indexCode = ''
        if (this.formQuery.statistical == '1') {
          //新增用户统计
          indexCode = '6d345e3d-654b-4ebe-906e-a1866c7e3158'
          this.xzyhjgtj = '新增用户统计'
        } else {
          //新增机构统计
          indexCode = '4e8f9c36-52cf-439e-bd35-187e15c983e9'
          this.xzyhjgtj = '新增机构统计'
        }
        const params = {
          indexCode: indexCode,
          statistical: this.formQuery.statistical || '',
          beginDate: this.formQuery.beginDate || '',
          endDate: this.formQuery.endDate || ''
        }

        request({
          url: `/api/report/v1.0/data/sql/${indexCode}`,
          method: 'post',
          data: params
        }).then(res => {

          if (res.data.status === 0) {
            const resultData = res.data.data || []
            this.handlexzyhjgtjOptions(resultData)
          }
        })
      },
      handlexzyhjgtjOptions(data) {

        const xData = data.map(item => item.XDATA) || []
        const yData = data.map(item => item.YDATA) || []
        var myChart = this.$echarts.init(
          document.getElementById('xzyhjgtj')
        )
        var legendData = []
        if (this.formQuery.statistical == '1') {
          legendData = ['新增用户']
        } else {
          legendData = ['新增机构']
        }

        let colors = CHART_COLOR_ARR
        this.dlzltjOptions = {
          legend: {
            top: '3%',
            data: legendData,
            textStyle: { color: '#000', fontSize: 12 }
          },
          color: colors,
          grid: {
            left: '2%',
            right: '3%',
            bottom: '12%',
            top: '10%',
            containLabel: true
          },
          tooltip: {
            trigger: 'axis',
            formatter: params => {
              let tip = params[0].name + '<br>'
              for (let i = 0; i < params.length; i++) {
                if ((i + 1) % 5 == 0) {
                  tip += params[i].marker + params[i].seriesName + ': ' + Number(params[i].value).toFixed(0) + '<br>'

                } else {
                  tip += params[i].marker + params[i].seriesName + ': ' + Number(params[i].value).toFixed(0) + '&nbsp&nbsp&nbsp&nbsp'
                }
              }
              return tip
            }
          },
          xAxis: [
            {
              type: 'category',
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
              },
              data: xData
            }
          ],
          yAxis: [
            {
              name: '数量（个）',
              axisLine: {
                show: false
              },
              axisTick: {
                show: false
              },
              splitArea: {
                show: false
              },
              min: 'dataMin',
              splitLine: {
                show: true,
                lineStyle: {
                  color: '#e5e5e5',
                  type: 'dashed'
                }
              }
            }
          ],
          series: [{
            name: legendData[0],
            data: yData,
            type: 'bar',
            barMaxWidth: 35

          }
          ]
        }
        myChart.setOption(this.dlzltjOptions)

      },
      //导出数据
      exportData() {

        let params = {
          statistical: this.formQuery.statistical || '',
          beginDate: this.formQuery.beginDate || '',
          endDate: this.formQuery.endDate || ''
        }
        var fileName = ''
        var beginDate = this.formQuery.beginDate
        var endDate = this.formQuery.endDate
        if (this.formQuery.statistical == '1') {
          fileName = '系统登录情况排名(' + beginDate + '至' + endDate + ')-用户-导出.xls'
        } else {
          fileName = '系统登录情况排名(' + beginDate + '至' + endDate + ')-机构-导出.xls'
        }

        const url = 'api/dataBoard/export'
        downLoadFileByUrl(url, params, fileName, this)
      }
    }
  }
</script>

<style lang="scss" scoped>

  .dataBoard {
    padding: 10px;

  .tips {
    font-size: 14px;
  }

  .funds-filter {
    width: 100%;
    border-bottom: 1px solid #e1e0e0;

  .dbjz {

  ::v-deep .el-select .el-input--small {
    width: 260px !important;
  }

  ::v-deep .el-select .el-select__tags {
    max-width: 234px !important;
  }

  }
  }
  .chart-main {
    margin-top: 3px;
    width: 100%;

  .chart-title {
    padding: 10px 0;
    border-bottom: 1px solid #e1b996;

  .title-icon {
    vertical-align: middle;
    display: inline-block;

  .color-box {
    display: inline-block;
    height: 30px;
    width: 2px;
  }

  }

  .title-txt {
    color: #333;
    vertical-align: middle;
    height: 35px;
    line-height: 35px;
    font-size: 16px;
    margin-left: 5px;
    display: inline-block;
  }

  }
  .chart-content {
    height: 500px;
    margin-top: 5px;

  .echarts_box {
    height: 100%;
    width: 100%;
  }

  }
  }
  }
  ::v-deep .el-button.el-button--info {
    color: #333;
    background-color: #dddddd;
    border-color: #dddddd;
  }
</style>
=
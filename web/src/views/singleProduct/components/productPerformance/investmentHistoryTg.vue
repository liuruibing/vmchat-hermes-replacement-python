<template>
  <div class="investment-history-tg standard-form">
    <div v-if="indexInfoArray.indexOf('f6296f47-d2e3-4e10-b354-367223d30d07') !== -1" class="titleBox">
      <div class="title_name">
        <div class="title_name_icon"></div>
        <span>历史收益走势图</span>
        <el-button size="small" style="float: right; margin-left: 15px" type="info" plain @click="exportChartToTable">导出excel</el-button>
<!--        <el-select v-model="frequencyCode" clearable placeholder="请选择" size="mini" style="width: 120px !important; float: right" @change="handleFrequencyChange">
          <el-option v-for="item in frequencyOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>-->
      </div>
    </div>
    <el-row v-if="indexInfoArray.indexOf('f6296f47-d2e3-4e10-b354-367223d30d07') !== -1">
      <el-col :span="12" style="margin: 0px 40px 0px 20px">
        <div class="chart-content">
          <myChart id="investmentHistoryTg" ref="investmentHistoryTg" :options="investmentHistoryTgOption" class="echarts_box" resize-dom="cmbfof" />
        </div>
      </el-col>
      <el-col :span="10">
        <div class="chart-content">
          <div>
            <span>日期:</span>
            {{ activatedData | noDataFilter }}
          </div>
          <vxe-table :data="tableData" :header-cell-style="{ color: '#333', height: '60px', background: '#fff' }" auto-resize border show-header-overflow show-overflow stripe>
            <vxe-table-column align="left" header-align="center" title="产品/对比指标">
              <template slot-scope="scope">
                {{ scope.row.f1 | noDataFilter }}
              </template>
            </vxe-table-column>
            <vxe-table-column align="right" header-align="center" title="收益率">
              <template slot-scope="scope">
                <span v-if="scope.row.f2 && scope.row.f2 > 0" style="color: red">
                  {{ scope.row.f2 | numberToFixedStr(2, 100, '%') }}
                </span>
                <span v-else-if="scope.row.f2 && scope.row.f2 < 0" style="color: green">
                  {{ scope.row.f2 | numberToFixedStr(2, 100, '%') }}
                </span>
                <span v-else>
                  {{ scope.row.f2 | numberToFixedStr(2, 100, '%') }}
                </span>
              </template>
            </vxe-table-column>
            <vxe-table-column align="right" header-align="center" title="归一化净值">
              <template slot-scope="scope">
                <span>{{ scope.row.f3 | numberToFixed(4, 1) }}</span>
              </template>
            </vxe-table-column>
          </vxe-table>
        </div>
      </el-col>
    </el-row>
    <div v-if="indexInfoArray.indexOf('a51fd813-f72d-4a47-b673-c7d93365687f') !== -1" class="titleBox">
      <el-row type="flex">
        <el-col :span="4">
          <span class="title_name">
            <div class="title_name_icon"></div>
            业绩分析
          </span>
        </el-col>
        <el-col :span="20" style="text-align: right">
          <div v-for="(item, index) of btnArr" :key="index" :class="{ btnClassClick: item.type == activeType }" class="btnClass" @click="toSwitchData(item)">
            {{ item.name }}
          </div>
        </el-col>
      </el-row>
    </div>
    <div v-if="indexInfoArray.indexOf('a51fd813-f72d-4a47-b673-c7d93365687f') !== -1">
      <span style="color:#ff0000;padding-left: 30px;">月度收益表数据统计至{{IndustryDataUpDate}}</span>
    </div>
    <div id="standard-table">
      <vxe-table
        v-if="indexInfoArray.indexOf('a51fd813-f72d-4a47-b673-c7d93365687f') !== -1"
        v-loading="tableLoading2"
        :data="tableData2"
        auto-resize
        max-height="500px"
        show-header-overflow
        show-overflow
        stripe
        style="margin: 20px 30px"
      >
        <vxe-table-column align="center" header-align="center" min-width="130px" title="名称">
          <template slot-scope="scope">
            <span>{{ scope.row.f1 | noDataFilter }}</span>
          </template>
        </vxe-table-column>
        <vxe-table-column align="right" header-align="center" min-width="120px" title="1月">
          <template slot-scope="scope">
            <span v-if="scope.row.f2 && scope.row.f2 > 0" style="color: red">
              {{ scope.row.f2 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else-if="scope.row.f2 && scope.row.f2 < 0" style="color: green">
              {{ scope.row.f2 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else>
              {{ scope.row.f2 | numberToFixedStr(2, 100, '%') }}
            </span>
          </template>
        </vxe-table-column>
        <vxe-table-column align="right" header-align="center" min-width="120px" title="2月">
          <template slot-scope="scope">
            <span v-if="scope.row.f3 && scope.row.f3 > 0" style="color: red">
              {{ scope.row.f3 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else-if="scope.row.f3 && scope.row.f3 < 0" style="color: green">
              {{ scope.row.f3 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else>
              {{ scope.row.f3 | numberToFixedStr(2, 100, '%') }}
            </span>
          </template>
        </vxe-table-column>
        <vxe-table-column align="right" header-align="center" min-width="120px" title="3月">
          <template slot-scope="scope">
            <span v-if="scope.row.f4 && scope.row.f4 > 0" style="color: red">
              {{ scope.row.f4 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else-if="scope.row.f4 && scope.row.f4 < 0" style="color: green">
              {{ scope.row.f4 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else>
              {{ scope.row.f4 | numberToFixedStr(2, 100, '%') }}
            </span>
          </template>
        </vxe-table-column>
        <vxe-table-column align="right" header-align="center" min-width="120px" title="4月">
          <template slot-scope="scope">
            <span v-if="scope.row.f5 && scope.row.f5 > 0" style="color: red">
              {{ scope.row.f5 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else-if="scope.row.f5 && scope.row.f5 < 0" style="color: green">
              {{ scope.row.f5 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else>
              {{ scope.row.f5 | numberToFixedStr(2, 100, '%') }}
            </span>
          </template>
        </vxe-table-column>
        <vxe-table-column align="right" header-align="center" min-width="120px" title="5月">
          <template slot-scope="scope">
            <span v-if="scope.row.f6 && scope.row.f6 > 0" style="color: red">
              {{ scope.row.f6 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else-if="scope.row.f6 && scope.row.f6 < 0" style="color: green">
              {{ scope.row.f6 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else>
              {{ scope.row.f6 | numberToFixedStr(2, 100, '%') }}
            </span>
          </template>
        </vxe-table-column>
        <vxe-table-column align="right" header-align="center" min-width="120px" title="6月">
          <template slot-scope="scope">
            <span v-if="scope.row.f7 && scope.row.f7 > 0" style="color: red">
              {{ scope.row.f7 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else-if="scope.row.f7 && scope.row.f7 < 0" style="color: green">
              {{ scope.row.f7 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else>
              {{ scope.row.f7 | numberToFixedStr(2, 100, '%') }}
            </span>
          </template>
        </vxe-table-column>
        <vxe-table-column align="right" header-align="center" min-width="120px" title="7月">
          <template slot-scope="scope">
            <span v-if="scope.row.f8 && scope.row.f8 > 0" style="color: red">
              {{ scope.row.f8 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else-if="scope.row.f8 && scope.row.f8 < 0" style="color: green">
              {{ scope.row.f8 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else>
              {{ scope.row.f8 | numberToFixedStr(2, 100, '%') }}
            </span>
          </template>
        </vxe-table-column>
        <vxe-table-column align="right" header-align="center" min-width="120px" title="8月">
          <template slot-scope="scope">
            <span v-if="scope.row.f9 && scope.row.f9 > 0" style="color: red">
              {{ scope.row.f9 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else-if="scope.row.f9 && scope.row.f9 < 0" style="color: green">
              {{ scope.row.f9 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else>
              {{ scope.row.f9 | numberToFixedStr(2, 100, '%') }}
            </span>
          </template>
        </vxe-table-column>
        <vxe-table-column align="right" header-align="center" min-width="120px" title="9月">
          <template slot-scope="scope">
            <span v-if="scope.row.f10 && scope.row.f10 > 0" style="color: red">
              {{ scope.row.f10 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else-if="scope.row.f10 && scope.row.f10 < 0" style="color: green">
              {{ scope.row.f10 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else>
              {{ scope.row.f10 | numberToFixedStr(2, 100, '%') }}
            </span>
          </template>
        </vxe-table-column>
        <vxe-table-column align="right" header-align="center" min-width="120px" title="10月">
          <template slot-scope="scope">
            <span v-if="scope.row.f11 && scope.row.f11 > 0" style="color: red">
              {{ scope.row.f11 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else-if="scope.row.f11 && scope.row.f11 < 0" style="color: green">
              {{ scope.row.f11 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else>
              {{ scope.row.f11 | numberToFixedStr(2, 100, '%') }}
            </span>
          </template>
        </vxe-table-column>
        <vxe-table-column align="right" header-align="center" min-width="120px" title="11月">
          <template slot-scope="scope">
            <span v-if="scope.row.f12 && scope.row.f12 > 0" style="color: red">
              {{ scope.row.f12 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else-if="scope.row.f12 && scope.row.f12 < 0" style="color: green">
              {{ scope.row.f12 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else>
              {{ scope.row.f12 | numberToFixedStr(2, 100, '%') }}
            </span>
          </template>
        </vxe-table-column>
        <vxe-table-column align="right" header-align="center" min-width="120px" title="12月">
          <template slot-scope="scope">
            <span v-if="scope.row.f13 && scope.row.f13 > 0" style="color: red">
              {{ scope.row.f13 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else-if="scope.row.f13 && scope.row.f13 < 0" style="color: green">
              {{ scope.row.f13 | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else>
              {{ scope.row.f13 | numberToFixedStr(2, 100, '%') }}
            </span>
          </template>
        </vxe-table-column>
      </vxe-table>
    </div>
    <el-row v-if="indexInfoArray.indexOf('a51fd813-f72d-4a47-b673-c7d93365687f') !== -1">
      <el-col :span="14">
        <div class="chart-content">
          <myChart id="investmentHistoryTg2" ref="investmentHistoryTg2" :options="investmentHistoryTgOption2" class="echarts_box" resize-dom="cmbfof" />
        </div>
      </el-col>
      <el-col :span="10" style="padding-right: 30px">
        <div>
          <span style="color:#ff0000;">数据截止：{{IndustryDataUpDate2}}</span>
        </div>
        <div id="standard-table">
          <vxe-table
            v-loading="tableLoading3"
            :data="tableData3"
            auto-resize
            show-header-overflow
            show-overflow
            stripe
          >
            <vxe-table-column align="center" header-align="center" title="产品/对比指标">
              <template slot-scope="scope">
                {{ scope.row.f1 | noDataFilter }}
              </template>
            </vxe-table-column>
            <vxe-table-column align="right" header-align="center" title="产品收益率">
              <template slot-scope="scope">
                <span v-if="scope.row.f2 && scope.row.f2 > 0" style="color: red">
                  {{ scope.row.f2 | numberToFixedStr(2, 100, '%') }}
                </span>
                <span v-else-if="scope.row.f2 && scope.row.f2 < 0" style="color: green">
                  {{ scope.row.f2 | numberToFixedStr(2, 100, '%') }}
                </span>
                <span v-else>
                  {{ scope.row.f2 | numberToFixedStr(2, 100, '%') }}
                </span>
              </template>
            </vxe-table-column>
            <vxe-table-column align="right" header-align="center" title="基准收益率">
              <template slot-scope="scope">
                <span v-if="scope.row.f3 && scope.row.f3 > 0" style="color: red">
                  {{ scope.row.f3 | numberToFixedStr(2, 100, '%') }}
                </span>
                <span v-else-if="scope.row.f3 && scope.row.f3 < 0" style="color: green">
                  {{ scope.row.f3 | numberToFixedStr(2, 100, '%') }}
                </span>
                <span v-else>
                  {{ scope.row.f3 | numberToFixedStr(2, 100, '%') }}
                </span>
              </template>
            </vxe-table-column>
            <vxe-table-column align="right" header-align="center" title="超额收益率">
              <template slot-scope="scope">
                <span v-if="scope.row.f4 && scope.row.f4 > 0" style="color: red">
                  {{ scope.row.f4 | numberToFixedStr(2, 100, '%') }}
                </span>
                <span v-else-if="scope.row.f4 && scope.row.f4 < 0" style="color: green">
                  {{ scope.row.f4 | numberToFixedStr(2, 100, '%') }}
                </span>
                <span v-else>
                  {{ scope.row.f4 | numberToFixedStr(2, 100, '%') }}
                </span>
              </template>
            </vxe-table-column>
          </vxe-table>
        </div>
      </el-col>
    </el-row>

    <div v-if="indexInfoArray.indexOf('a323e7c1-5238-4a75-982c-e42929a13d06') !== -1" class="titleBox">
      <div class="title_name">
        <div class="title_name_icon"></div>
        <span>历史净值</span>
        <el-button size="small" style="float: right" type="info" plain @click="exportToExcel">导出excel</el-button>
      </div>
    </div>
    <div id="standard-table">
      <vxe-table
        v-if="indexInfoArray.indexOf('a323e7c1-5238-4a75-982c-e42929a13d06') !== -1"
        v-loading="tableLoading4"
        :data="tableData4"
        auto-resize
        max-height="550px"
        show-header-overflow
        show-overflow
        stripe
        style="margin: 20px 30px"
      >
        <vxe-table-column align="center" header-align="center" min-width="130px" title="净值日期">
          <template slot-scope="scope">
            <span>{{ scope.row.f1 | noDataFilter }}</span>
          </template>
        </vxe-table-column>
        <vxe-table-column align="center" header-align="center" min-width="130px" title="单位净值">
          <template slot-scope="scope">
            <span>{{ scope.row.f2 | numberToFixed(4, 1) }}</span>
          </template>
        </vxe-table-column>
        <vxe-table-column align="center" header-align="center" min-width="130px" title="累计单位净值">
          <template slot-scope="scope">
            <span>{{ scope.row.f3 | numberToFixed(4, 1) }}</span>
          </template>
        </vxe-table-column>
        <vxe-table-column align="center" header-align="center" min-width="130px" title="分红金额">
          <template slot-scope="scope">
            <span>{{ scope.row.f4 | moneyYuan }}</span>
          </template>
        </vxe-table-column>
      </vxe-table>
    </div>
    <el-row>
      <Pagination
        v-if="indexInfoArray.indexOf('a323e7c1-5238-4a75-982c-e42929a13d06') !== -1"
        :limit="pageSize"
        :page="pageNum"
        :total="total"
        @pagination="pagination"
      ></Pagination>
    </el-row>
  </div>
</template>
<script>
import pageApi from '../../api/investmentHistoryTg'
import { merger } from '@/utils'
import myChart from '@/components/Echarts'
import commonApi from '@/api/common'
import Pagination from '@/components/Pagination'
import { numberToFixedStr } from '@/filters'
import { frequencyOptions } from '@/dataDictionary/frequency'

import XLSX from 'xlsx'
import { saveAs } from 'file-saver'

export default {
  components: { myChart, Pagination },
  data() {
    return {
      searchQuery: null,
      indexInfoArray: [],
      investmentHistoryTgOption: {},
      investmentHistoryTgOption2: {},
      activatedData: '',
      echartData: '',
      tableData: [], // 业绩分析上表格
      tableData2: [],
      tableData3: [],
      tableData4: [],
      tableLoading1: false,
      tableLoading2: false,
      tableLoading3: false,
      tableLoading4: false,
      IndustryDataUpDate:'',
      IndustryDataUpDate2:'',
      activeType: '2',
      pageSize: 10,
      pageNum: 1,
      total: 0,
      pageFlag: true,
      numberToFixedStr: numberToFixedStr,
      btnArr: [
        { name: '近两年', type: '2', flag: '2M' },
        { name: '近五年', type: '5', flag: '5M' }
        // {name: '导出', type: '3', flag: 'export'}
      ],
      //frequencyOptions: frequencyOptions,
      frequencyOptions:[
        {
          label: '日频',
          value: 'D'
        },
        {
          label: '周频',
            value: 'W'
        },
      ],
      frequencyCode: '',
      xData: []
    }
  },
  watch: {
    activatedData: {
      handler(val) {
        // 组装tableData数据
        const tableDataArray = []
        for (let i = 0; i < this.echartData.length; i++) {
          const temp = this.echartData[i]
          if (temp.origin && temp.origin.length && temp.origin.length > 0) {
            for (let j = 0; j < temp.origin.length; j++) {
              const tempJ = temp.origin[j]
              if (tempJ.XDATA == val) {
                tableDataArray.push({
                  f1: tempJ.YDATA || '',
                  f2: tempJ.YDATA2 || '',
                  f3: tempJ.YDATA5 || ''
                })
                break
              }
            }
          }
        }
        this.tableData = [...tableDataArray]
      },
      deep: true
    }
  },
  methods: {
    /**
     * @description 公共导出方法
     */
    commonExport(data, name) {
      // 创建一个工作簿对象
      const workbook = XLSX.utils.book_new()

      // // 创建一个工作表对象
      const worksheet = XLSX.utils.json_to_sheet(data)

      // // 将工作表对象添加到工作簿中
      XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1')

      // // 将工作簿转换为Excel文件的二进制数据
      const excelData = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' })

      // // 创建一个Blob对象
      const blob = new Blob([excelData], {
        type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
      })

      // // 使用FileSaver保存文件
      saveAs(blob, name)
    },
    /**
     * @description 导出历史收益走势图chart
     */
    exportChartToTable() {
      const data = []
      let obj = {}
      const mergeData = this.echartData
      mergeData.forEach((ele, indexs) => {
        for (let i = 0; i < this.xData.length; i++) {
          const item = this.xData[i]
          obj = {}
          obj['日期'] = item
          const tempObj = ele['origin'].find((e) => e.XDATA === item)
          obj[`${ele['YDATA']}`] = tempObj.YDATA1 || ''
          const index = data.findIndex((k) => k['日期'] === item)
          if (indexs < 1) {
            data.push(obj)
          }
          if (index !== -1) {
            data[index][ele['YDATA']] = tempObj.YDATA1 || ''
          } else {
            // obj[items['YDATE']] = tempObj.YDATE1
          }
        }
      })
      this.commonExport(data, '历史收益走势图.xlsx')
    },
    /**
     * @description 导出历史净值table
     */
    exportToExcel() {
      const params = {}
      params.indexCode = 'a8a4bc38-d172-4760-b95b-823b3cdf983a'
      params.startDate = this.searchQuery.startDate
      params.endDate = this.searchQuery.endDate
      params.fundCode = this.searchQuery.fundCode
      params.kpiCode = this.searchQuery.kpiCode
      params.contrasCode = this.searchQuery.contrasCode == '' ? '' : this.searchQuery.contrasCode.join(',')
      commonApi.getDataBysqlCode(params).then((res) => {
        if (res.data.status === 0) {
          let exportTable = res.data.data || []
          exportTable = exportTable.map((item) => {
            return {
              净值日期: item.XDATA || '',
              单位净值: item.YDATA1 || '',
              累计单位净值: item.YDATA2 || '',
              分红金额: item.YDATA4 || ''
            }
          })
          this.commonExport(exportTable, '历史净值.xlsx')
        }
      })
    },
    /**
     * @description 监听历史收益走势图频率下拉
     */
    handleFrequencyChange(val) {
      this.queryHistoryEarn(val)
    },
    /**
     * @description 根据频率下拉值查询数据（先调用权限判断）
     */
    async queryHistoryEarn(val) {
      // 首先查询 权限
      await this.getIndexInfo()
      // 如果 历史收益走势图编码存在则查询
      if (this.indexInfoArray.indexOf('f6296f47-d2e3-4e10-b354-367223d30d07') !== -1) {
        this.getInvestMentHistoryData(val)
      }
    },
    // 页面查询
    async fun_iframeSrc() {
      this.echartData = ''
      this.tableData = []
      this.tableData2 = []
      this.tableData3 = []
      this.tableData4 = []
      this.activatedData = ''
      this.indexInfoArray = []
      this.investmentHistoryTgOption = {}
      this.investmentHistoryTgOption2 = {}
      this.IndustryDataUpDate = ''
      this.IndustryDataUpDate2 = ''
      // 首先查询 权限
      await this.getIndexInfo()

      // 如果 历史收益走势图编码存在则查询
      if (this.indexInfoArray.indexOf('f6296f47-d2e3-4e10-b354-367223d30d07') !== -1) {
        this.getInvestMentHistoryData(this.frequencyCode)
      }

      // 查询 业绩分析 上表格
      if (this.indexInfoArray.indexOf('a51fd813-f72d-4a47-b673-c7d93365687f') !== -1) {
        this.getIndustryDataUp()
        this.getIndustryDataUpDate()
        this.getIndustryDataDown()
        this.getIndustryDataDownDate()
      }

      // 查询历史净值
      if (this.indexInfoArray.indexOf('a323e7c1-5238-4a75-982c-e42929a13d06') !== -1) {
        this.getHistoryUnit()
      }

      //
    },
    // 获取权限指标权限列表
    getIndexInfo() {
      return new Promise((resolve, reject) => {
        const params = {}
        params.templateCode = '83e911f2-86a7-4e6d-b07f-a7666a806d89'
        params.fundCode = this.searchQuery.fundCode
        pageApi
          .selectIndexInfos(params)
          .then((res) => {
            const { status, data } = res.data
            if (status == 0) {
              this.indexInfoArray = data.map((item) => item.vcCode)
            } else {
              this.indexInfoArray = []
            }
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
    },

    // 获取历史收益走势图数据
    getInvestMentHistoryData(val) {
      const params = {}
      params.indexCode = 'ba8c5458-ba67-43b5-97d4-cf89a090e39f'
      params.rate = val ? val : ''
      params.startDate = this.searchQuery.startDate
      params.endDate = this.searchQuery.endDate
      params.fundCode = this.searchQuery.fundCode
      params.kpiCode = this.searchQuery.kpiCode
      params.contrasCode = this.searchQuery.contrasCode == '' ? '' : this.searchQuery.contrasCode.join(',')
      commonApi.getDataBysqlCode(params).then((res) => {
        const { status, data } = res.data
        if (status == 0) {
          if (data.length > 0) {
            this.handleEchartsData(data)
          } else {
            this.investmentHistoryTgOption = {}
          }
        }
      })
    },
    handleEchartsData(data) {
      const mergeData = merger(data, 'YDATA')
      this.echartData = mergeData
      let xData = [],
        legend = [],
        seriesData = []
      const color = [
        '#ef4136',
        '#fcaf17',
        '#50b7c1',
        '#ea66a6',
        '#4e72b8',
        '#7d5886',
        '#8f4b4a',
        '#006c54',
        '#cbc547',
        '#fedcbd',
        '#ba8448',
        '#f3715c',
        '#9d9087',
        '#008792',
        '#cde6c7',
        '#f58220',
        '#65c294',
        '#454926',
        '#fcf16e',
        '#ca8687',
        '#afb4db',
        '#f7acbc',
        '#b7ba6b',
        '#d5c59f',
        '#d71345',
        '#90d7ec',
        '#224b8f',
        '#ffce7b',
        '#d3d7d4',
        '#ffd400'
      ]
      // 拿到所有不重复的 日期
      const dateArray = [...new Set(data.map((item) => item.XDATA))]
      xData = dateArray
      this.xData = xData
      mergeData.forEach((item) => {
        const tempOrigin = []
        const seriesObj = {
          name: item.YDATA,
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
        legend.push({ name: item.YDATA, icon: 'roundRect' })
        for (let i = 0; i < dateArray.length; i++) {
          const temp = dateArray[i]
          const objExample = {}
          objExample.XDATA = temp
          objExample.YDATA = item.YDATA
          const obj = item.origin.find((sitem) => sitem.XDATA == temp) || objExample
          tempOrigin.push(obj)
        }
        item.origin = tempOrigin
        seriesObj.data = item.origin.map((item) => item.YDATA1)
        seriesData.push(seriesObj)
      })
      this.investmentHistoryTgOption = {
        // toolbox: {
        //   show: true,
        //   right: '13px',
        //   top: '20px',
        //   feature: {
        //     dataZoom: {
        //       yAxisIndex: 'none',
        //       show: false
        //     },
        //     saveAsImage: {},
        //     dataView: {
        //       show: true,
        //       title: '表格数据',
        //       lang: ['表格数据：', '关闭', '导出Excel'],    // 按钮
        //       contentToOption: (opts) =>  {
        //         console.log(opt)
        //         this.export2Excel()
        //         table2excel('tableExcel_Day',{
        //           exclude: ".noExl", //过滤位置的 css 类名， 有class = “noExl” 的行不被导出
        //           filename: "历史收益走势对比.xls", // 文件名称
        //           name: "历史收益走势对比.xls",
        //           exclude_img: true,
        //           exclude_links: true,
        //           exclude_inputs: true
        //         })
        //       },
        //       // 数据视图展示为table
        //       optionToContent: function (opt) {
        //         var axisData = opt.xAxis[0].data; // 坐标数据
        //         var series = opt.series; //折线图数据，此处即为数据源，可以打印查看
        //         var tdHeads = '<td  style="padding: 0 10px">日期</td>'; //表头第一列
        //         var tdBodys = ''; //表数据
        //
        //         //组装表头
        //         var nameData = new Array();
        //         for (var k = 0; k < series.length; k++) {
        //           nameData.push(series[k].name)
        //         }
        //         for (var i = 0; i < nameData.length; i++) {
        //           tdHeads += '<td style="padding: 0 10px">' + nameData[i] + '</td>';
        //         }
        //         var table = '<table id="tableExcel_Day" border="1" class="table-bordered table-striped" style="width:100%;text-align:center" ><tbody><tr>' + tdHeads + ' </tr>';
        //         //组装表数据
        //         for (var i = 0; i < axisData.length; i++) {
        //           for (var j = 0; j < series.length; j++) {
        //             var temp = series[j].data[i];
        //             if (temp != null && temp != undefined) {
        //               tdBodys += '<td>' + temp + '</td>';
        //             } else {
        //               tdBodys += '<td></td>';
        //             }
        //           }
        //           table += '<tr><td style="padding: 0 10px">' + axisData[i] + '</td>' + tdBodys + '</tr>';
        //           tdBodys = '';
        //         }
        //         table += '</tbody></table>';
        //         return table;
        //       }
        //     }
        //   },
        // },
        tooltip: {
          trigger: 'axis',
          formatter: (params) => {
            if (params[0] && params[0].axisValueLabel) {
              this.activatedData = params[0].axisValueLabel
            } else {
              this.activatedData = '-'
            }
            let tip = params[0].name + '<br>'
            for (let i = 0; i < params.length; i++) {
              let value = ''
              if (params[i].value == undefined || params[i].value == '' || params[i].value == null) {
                value = '--'
              } else {
                value = Number(params[i].value).toFixed(4)
              }
              tip += params[i].marker + params[i].seriesName + ': ' + value + '<br>'
            }
            return tip
          }
        },
        color: color,
        animation: false,
        legend: {
          top: '3%',
          data: legend,
          show: true,
          borderColor: '#FFF',
          itemGap: 20,
          textAlign: {
            fontsize: 16,
            align: 'center'
          }
        },
        grid: {
          top: '22%',
          bottom: '8%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: xData,
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
          name: '归一化净值',
          type: 'value',
          position: 'left',
          min: 'dataMin',
          axisLabel: {
            formatter: '{value}'
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
        dataZoom: [
          {
            brushSelect: false,
            bottom: '0',
            show: true
          }
        ],
        series: seriesData
      }
      for (let i = this.echartData.length - 1; i >= 0; i++) {
        let temp = this.echartData[i]
        for (let j = temp.origin.length - 1; j >= 0; j--) {
          let stemp = temp.origin[j]
          if (stemp.YDATA2 || stemp.YDATA5) {
            this.activatedData = stemp.XDATA
            return
          }
        }
      }
    },
    numberToFixed() {},
    pagination(val) {
      const { page, limit } = val
      this.pageNum = page
      this.pageSize = limit
      this.getHistoryUnit()
    },
    handleEchartsData2(data) {
      let xData = [],
        legend = [],
        seriesData = []
      legend = [data[0].YDATA, '基准收益率']
      xData = data.map((item) => item.XDATA)
      let seriesObj1 = {
        name: data[0].YDATA,
        type: 'bar',
        maxWidth: '25',
        data: data.map((item) => item.YDATA1)
      }
      let seriesObj2 = {
        name: '基准收益率',
        type: 'bar',
        maxWidth: '25',
        data: data.map((item) => item.YDATA2)
      }
      seriesData = [seriesObj1, seriesObj2]
      this.investmentHistoryTgOption2 = {
        tooltip: {
          trigger: 'axis',
          formatter: (params) => {
            if (params[0] && params[0].axisValueLabel) {
              this.activatedData = params[0].axisValueLabel
            } else {
              this.activatedData = '-'
            }
            let tip = params[0].name + '<br>'
            for (let i = 0; i < params.length; i++) {
              let value = ''
              if (params[i].value == undefined || params[i].value == '' || params[i].value == null) {
                value = '--'
              } else {
                value = params[i].value
              }
              tip += params[i].marker + params[i].seriesName + ': ' + this.numberToFixedStr(value, 2, 100, '%') + '<br>'
            }
            return tip
          }
        },
        color: ['#4f81bd', '#c0504d'],
        animation: false,
        legend: {
          top: '3%',
          data: legend,
          show: true,
          borderColor: '#FFF',
          itemGap: 20,
          textAlign: {
            fontsize: 16,
            align: 'center'
          }
        },
        grid: {
          top: '22%',
          bottom: '8%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: true,
          data: xData,
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
          name: '收益率',
          type: 'value',
          position: 'left',
          min: 'dataMin',
          axisLabel: {
            formatter: (val) => {
              return this.numberToFixedStr(val, 2, 100, '%')
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
        series: seriesData
      }
    },

    // 统计周期区间映射
    toSwitchData(data) {
      this.activeType = data.type
      if (data.type == '2' || data.type == '5') {
        this.getIndustryDataUp()
      } else {
        // 调用导出方法
      }
    },

    // 获取业绩分析上表格数据
    getIndustryDataUp() {
      const params = {}
      params.indexCode = '85b97651-b02e-4fb3-ad17-50b1a51973bc'
      params.startDate = this.searchQuery.startDate
      params.endDate = this.searchQuery.endDate
      params.fundCode = this.searchQuery.fundCode
      params.kpiCode = this.searchQuery.kpiCode
      params.contrasCode = this.searchQuery.contrasCode == '' ? '' : this.searchQuery.contrasCode.join(',')
      params.checkJF = this.activeType
      this.tableLoading2 = true
      commonApi
        .getDataBysqlCode(params)
        .then((res) => {
          const { status, data } = res.data
          if (status == 0) {
            if (data.length > 0) {
              let tempArray = []
              data.forEach((item) => {
                tempArray.push({
                  f1: item.XDATA,
                  f2: item.YDATA1,
                  f3: item.YDATA2,
                  f4: item.YDATA3,
                  f5: item.YDATA4,
                  f6: item.YDATA5,
                  f7: item.YDATA6,
                  f8: item.YDATA7,
                  f9: item.YDATA8,
                  f10: item.YDATA9,
                  f11: item.YDATA10,
                  f12: item.YDATA11,
                  f13: item.YDATA12
                })
              })
              this.tableData2 = [...tempArray]
            } else {
              this.tableData2 = []
            }
            this.tableLoading2 = false
          } else {
            this.tableData2 = []
            this.tableLoading2 = false
          }
        })
        .catch((err) => {
          this.tableData2 = []
          this.tableLoading2 = false
        })
    },
    //获取业绩分析上表格时间
    getIndustryDataUpDate() {
      const params = {}
      params.indexCode = '251cf2df-0c46-4d6a-af0d-1360c67b0613'
      params.endDate = this.searchQuery.endDate
      params.fundCode = this.searchQuery.fundCode
      commonApi
        .getDataBysqlCode(params)
        .then((res) => {
          const { status, data } = res.data
          if (status == 0) {
            this.IndustryDataUpDate = data[0].d_maxdate
          } else {
            this.IndustryDataUpDate = ''
          }
        })
        .catch((err) => {
        })
    },

    // 获取业绩分析下表格数据
    getIndustryDataDown() {
      const params = {}
      params.indexCode = '5580be58-0f94-48fa-b191-957cdc2cd6d2'
      params.startDate = this.searchQuery.startDate
      params.endDate = this.searchQuery.endDate
      params.fundCode = this.searchQuery.fundCode
      params.kpiCode = this.searchQuery.kpiCode
      params.contrasCode = this.searchQuery.contrasCode == '' ? '' : this.searchQuery.contrasCode.join(',')
      this.tableLoading3 = true
      commonApi
        .getDataBysqlCode(params)
        .then((res) => {
          const { status, data } = res.data
          if (status == 0) {
            if (data.length > 0) {
              let tempArray = []
              data.forEach((item) => {
                tempArray.push({
                  f1: item.XDATA,
                  f2: item.YDATA1,
                  f3: item.YDATA2,
                  f4: item.YDATA3
                })
              })
              this.tableData3 = tempArray
              this.handleEchartsData2(data)
            } else {
              this.investmentHistoryTgOption2 = {}
              this.tableData3 = []
            }
            this.tableLoading3 = false
          } else {
            this.investmentHistoryTgOption2 = {}
            this.tableData3 = []
            this.tableLoading3 = false
          }
        })
        .catch((err) => {
          this.investmentHistoryTgOption2 = {}
          this.tableData3 = []
          this.tableLoading3 = false
        })
    },

    // 获取业绩分析下表格日期数据
    getIndustryDataDownDate() {
      const params = {}
      params.indexCode = '958b4bef-5f35-47d7-b837-d9bf2fedf6bc'
      params.endDate = this.searchQuery.endDate
      params.fundCode = this.searchQuery.fundCode
      commonApi
        .getDataBysqlCode(params)
        .then((res) => {
          const { status, data } = res.data
          if (status == 0) {
            this.IndustryDataUpDate2 = data[0].d_maxdate
          } else {
            this.IndustryDataUpDate2 = ''
          }
        })
        .catch((err) => {
        })
    },

    // 获取历史净值
    getHistoryUnit() {
      const params = {}
      params.indexCode = 'a8a4bc38-d172-4760-b95b-823b3cdf983a'
      params.startDate = this.searchQuery.startDate
      params.endDate = this.searchQuery.endDate
      params.fundCode = this.searchQuery.fundCode
      params.kpiCode = this.searchQuery.kpiCode
      params.contrasCode = this.searchQuery.contrasCode == '' ? '' : this.searchQuery.contrasCode.join(',')
      params._pageSize = this.pageSize
      params._pageNum = this.pageNum
      params._pageFlag = this.pageFlag
      this.tableLoading4 = true
      commonApi
        .getDataBysqlCode(params)
        .then((res) => {
          const { status, data } = res.data
          if (status == 0) {
            if (data.rows.length > 0) {
              let tempArray = []
              data.rows.forEach((item) => {
                tempArray.push({
                  f1: item.XDATA,
                  f2: item.YDATA1,
                  f3: item.YDATA2,
                  f4: item.YDATA4
                })
              })
              this.tableData4 = [...tempArray]
              this.total = data.total
            } else {
              this.tableData4 = []
              this.total = 0
            }
            this.tableLoading4 = false
          } else {
            this.tableData4 = []
            this.total = 0
            this.tableLoading4 = false
          }
        })
        .catch((err) => {
          this.tableData4 = []
          this.total = 0
          this.tableLoading4 = false
        })
    }
  }
}
</script>
<style lang="scss" scoped>
.investment-history-tg {
  position: relative;
  margin: 0 30px;

  .titleBox {
    border-bottom: 1px solid #A15008;
    padding: 20px 0 10px;
    font-size: 16px;
    margin-bottom: 34px;
  }

  .btnClass {
    padding: 5px 15px;
    //background-color: #ddd;
    background-color: #fcf8f4 !important;
    color: #333;
    // float: right;
    display: inline-block;
    border-radius: 4px;
    font-size: 14px;
    cursor: pointer;
    position: relative;
    top: -2px;
    margin-left: 5px;
  }

  .btnClassClick {
    color: #612d10;
    /*background-color: #0f65dd;*/
    background-image: linear-gradient(to right, #f5d7bc, #e0b794) !important;
  }

  .title_name {
    height: 30px;
    line-height: 30px;
    color: #333333;
    padding-left: 5px;
  }

  .title_name1 {
    position: relative;
    top: 5px;
  }

  .title_name_icon {
    width: 4px;
    display: inline-block;
    height: 12px;
    line-height: 12px;
    background-image: linear-gradient(-45deg,#e19c5d,#f4cea9);
    position: relative;
    top: 1px;
    margin-right: 10px;

  }

  .chart-content {
    height: 400px;
    margin-top: 5px;

    .echarts_box {
      height: 100%;
      width: 100%;
    }
  }
}
::v-deep .vxe-table .vxe-body--row.row--stripe {
  background-color: #f9fafe !important;
}
</style>

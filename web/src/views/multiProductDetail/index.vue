<template>
  <div class="multiProductDetail">
    <!-- 查询表单 -->
    <el-row>
      <el-col style="width: calc(100% - 250px)">
        <el-form ref="formQuery" :inline="true" :model="formQuery" :rules="searchRules" label-width="140px;">
          <el-form-item label="选择产品" prop="productNames">
            <el-input v-model="formQuery.productNames" class="mr20" placeholder="请输入" readonly size="small" @focus="productSelectorVisible = true"></el-input>
          </el-form-item>
          <el-form-item label="统计周期" prop="cycle">
            <el-select v-model="formQuery.cycle" class="mr5" clearable placeholder="请选择" size="small" @change="handleDateChange" @focus="coverDiv = true">
              <el-option v-for="item in cycleArr" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
            <el-date-picker
              v-model="formQuery.startDate"
              :disabled="formQuery.cycle != 7"
              format="yyyy-MM-dd"
              placeholder="开始日期"
              size="small"
              type="date"
              value-format="yyyy-MM-dd"
            />
            <span>-</span>
            <el-date-picker
              v-model="formQuery.endDate"
              :disabled="formQuery.cycle != 7"
              class="mr20"
              format="yyyy-MM-dd"
              placeholder="结束日期"
              size="small"
              type="date"
              value-format="yyyy-MM-dd"
            />
          </el-form-item>
          <el-form-item class="yjjz" label="业绩基准" prop="kpiCode">
            <el-select v-model="formQuery.kpiCode" clearable placeholder="请选择" size="small" @focus="coverDiv = true">
              <el-option v-for="item in kpiStandardOpts" :key="item.id" :label="item.label" :value="item.id"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item class="dbjz" label="对比基准" prop="dbjz">
            <el-select v-model="formQuery.dbjz" clearable multiple placeholder="请选择" size="small" @change="changeContrasCode" @focus="coverDiv = true" collapse-tags>
              <el-option v-for="item in dbjzArr" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
          <!-- <el-form-item label="对比基准" prop="dbjz">
            <el-select
              v-model="formQuery.dbjz"
              class="mr20"
              clearable
              placeholder="请选择"
              size="small"
              @focus="coverDiv = true"
            >
              <el-option
                v-for="item in dbjzArr"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              ></el-option>
            </el-select>
          </el-form-item> -->
        </el-form>
      </el-col>
      <el-col style="width: 250px">
        <div style="text-align: right">
          <el-button icon="el-icon-search" size="small" type="primary" @click="onQuery()">查询</el-button>
          <el-button type="info" plain size="small" icon="el-icon-refresh-left" @click="resetForm()">重置</el-button>
        </div>
      </el-col>
    </el-row>
    <el-row v-if="this.homeParams.length">
      <el-col :span="24">
        <el-form :inline="true" label-width="120px;">
          <el-form-item label="已选产品">
            <el-tag v-for="(item, index) of homeParams" :key="index" :disable-transitions="false" closable @close="handleClose(index)">
              {{ item.VC_FUNDNAME }}
              <!-- {{ item.VC_FUNDCODE }}&nbsp;&nbsp; -->
            </el-tag>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
    <!-- <el-tabs class="mb20" type="border-card">
      <el-tab-pane class="elTabs" label="基本信息对比">
        <div class="title-style">基本信息</div>
        <div class="line"></div>
        <el-table
          v-loading="tableLoading"
          :data="tableData"
          class="tableStyle"
          max-height="500px"
          stripe
          style="width: 100%"
        >
          <el-table-column
            v-for="item in Columns"
            :key="item.prop"
            :align="item.align"
            :label="item.label"
            :min-width="item.minWidth || '100'"
            :prop="item.prop"
            :sortable="item.sortable"
            :width="item.width"
            header-align="center"
            show-overflow-tooltip
          >
            <template slot-scope="scope">
              <span>{{ scope.row[item.prop] | noDataFilter }}</span>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>

      <el-tab-pane class="elTabs" label="业绩对比">
        <div class="title-style">历史收益走势对比</div>
        <div class="line"></div>
        <el-row :gutter="40">
          <el-col :span="14">
            <div class="echartBox">
              <myChart
                id="lssyzsdb"
                ref="lssyzsdb"
                :options="lssyzsdbOptions"
                class="echarts_box"
                resize-dom="cmbfof"
              />
            </div>
          </el-col>
          <el-col :span="10">
            <el-table :data="tableData1" class="tableStyle" max-height="350px" stripe style="width: 100%">
              <el-table-column align="left" label="" width="20"></el-table-column>
              <el-table-column
                v-for="item in Columns1"
                :key="item.prop"
                :align="item.align"
                :header-align="item.headerAlign"
                :label="item.label"
                :min-width="item.minWidth || '100'"
                :prop="item.prop"
                :sortable="item.sortable"
                :width="item.width"
                show-overflow-tooltip
              >
                <template slot-scope="scope">
                  <span
                    v-if="item.prop == 'f2'"
                    :style="{ color: scope.row[item.prop] < 0 ? '#70AD47' : '#FF0000' }"
                  >
                    {{ (scope.row[item.prop] + '%') | noDataFilter }}
                  </span>
                  <span v-else>{{ scope.row[item.prop] | noDataFilter }}</span>
                </template>
              </el-table-column>
            </el-table>
          </el-col>
        </el-row>
        <div class="title-style mt30">业绩对比</div>
        <div class="line"></div>
        <el-table :data="tableData2" class="tableStyle" stripe style="width: 100%">
          <el-table-column
            v-for="item in Columns2"
            :key="item.prop"
            :align="item.align"
            :label="item.label"
            :min-width="item.minWidth || '100'"
            :prop="item.prop"
            :sortable="item.sortable"
            :width="item.width"
            header-align="center"
            show-overflow-tooltip
          >
            <template slot-scope="scope">
              <span v-if="item.setColor" :style="{ color: scope.row[item.prop] < 0 ? '#70AD47' : '#FF0000' }">
                {{ (scope.row[item.prop] + '%') | noDataFilter }}
              </span>
              <span v-else>{{ scope.row[item.prop] | noDataFilter }}</span>
            </template>
          </el-table-column>
          <el-table-column align="left" label="" width="20"></el-table-column>
        </el-table>
      </el-tab-pane>

      <el-tab-pane class="elTabs" label="风险对比">
        <div class="title-style">动态回撤对比</div>
        <div class="line"></div>
        <el-row>
          <el-col :span="24">
            <div class="echartBox">
              <myChart
                id="dthcdb"
                ref="dthcdb"
                :options="dthcdbOptions"
                class="echarts_box"
                resize-dom="cmbfof"
              />
            </div>
          </el-col>
        </el-row>
        <div class="title-style mt30">收益与风险指标对比</div>
        <div class="line"></div>
        <el-table :cell-class-name="myclass" :data="tableData3" class="tableStyle" style="width: 100%">
          <el-table-column
            v-for="item in Columns3"
            :key="item.prop"
            :align="item.align"
            :label="item.label"
            :min-width="item.minWidth || '100'"
            :prop="item.prop"
            :sortable="item.sortable"
            :width="item.width"
            header-align="center"
            show-overflow-tooltip
          >
            <template slot-scope="scope">
              <span v-if="item.setColor" :style="{ color: scope.row[item.prop] < 0 ? '#70AD47' : '#FF0000' }">
                {{ (scope.row[item.prop] + '%') | noDataFilter }}
              </span>
              <span v-else>{{ scope.row[item.prop] | noDataFilter }}</span>
            </template>
          </el-table-column>
        </el-table>
        <div class="tip">备注：红色代表当前列中该项指标最好的基金，绿色代表当前列中该项指标最差的基金</div>
      </el-tab-pane>
    </el-tabs> -->
    <el-tabs v-model="activeName" class="mb20" type="border-card" @tab-click="handleTabClick">
      <el-tab-pane v-for="tab in tabArr" :key="tab.name" :label="tab.label" :name="tab.name" class="elTabs">
        <component :is="compMapRelation[tab.name]" :ref="tab.name" :cover-div="coverDiv" :form-query="formQuery" @uploadCover="uploadCover"></component>
      </el-tab-pane>
    </el-tabs>
    <product-selector
      :dialog-visible="productSelectorVisible"
      :limit="5"
      :select-list="homeParams"
      :show-tree-key-array="showTreeKeyArray"
      :tree-data="treeData"
      default-checked-keys="zstgwb"
      multiple
      title="选择类型"
      @closedialog="handleDialogClosed"
      @submitdialog="handleSubmitClick"
    ></product-selector>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import myChart from '@/components/Echarts'
import productSelector from '@/components/productSelector'
import { dateShortcutMap } from './script/common'
import baseInfo from './components/baseInfo'
import performanceCompare from './components/performanceCompare'
import riskCompare from './refactorComponents/riskCompare'
// import riskCompare from './components/riskCompare'
import request from '@/utils/request'

export default {
  components: {
    Pagination,
    myChart,
    productSelector,
    baseInfo,
    performanceCompare,
    riskCompare
  },
  data() {
    /** 开始日期校验 */
    const validateStartDate = (rule, value, callback) => {
      if (this.formQuery.endDate !== null || this.formQuery.endDate !== undefined || this.formQuery.endDate !== '') {
        const startTime = new Date(value)
        const endTime = new Date(this.formQuery.endDate)
        if (startTime > endTime) {
          callback(new Error('开始日期不能大于结束日期'))
        } else {
          callback()
        }
      } else {
        callback()
      }
    }
    /** 结束日期校验 */
    const validateEndDate = (rule, value, callback) => {
      if (this.formQuery.startDate !== null || this.formQuery.startDate !== undefined || this.formQuery.startDate !== '') {
        const startTime = new Date(this.formQuery.startDate)
        const endTime = new Date(value)
        if (startTime > endTime) {
          callback(new Error('结束日期不能小于开始日期'))
        } else {
          callback()
        }
      } else {
        callback()
      }
    }
    return {
      coverDiv: false,
      tabLeftSelect: false,
      tabCenterSelect: false,
      tabRightSelect: false,
      formQuery: {
        productCodes: '',
        productNames: '',
        cycle: '4',
        startDate: dateShortcutMap['4'].onClick()[0],
        endDate: dateShortcutMap['4'].onClick()[1],
        jzlx: 1,
        dbjz: [],
        kpiCode: '',
        _pageSize: 20,
        _pageNum: 1,
        _pageFlag: true
      },
      kpiStandardOpts: [],
      statusOptions: [
        { label: '已提交', value: '1' },
        { label: '处理中', value: '2' },
        { label: '处理完毕', value: '3' }
      ],
      searchRules: {
        startDate: [{ validator: validateStartDate, trigger: 'blur' }],
        endDate: [{ validator: validateEndDate, trigger: 'blur' }]
      },
      cycleArr: [
        { label: '近一月', value: '1' },
        { label: '近三月', value: '2' },
        { label: '近六月', value: '3' },
        { label: '近一年', value: '4' },
        { label: '今年以来', value: '5' },
        // {label: '成立以来', value: "6"},
        { label: '自定义', value: '7' }
      ],
      jzlxArr: [
        { label: '累计净值', value: 1 },
        { label: '复权累计净值', value: 2 }
      ],
      dbjzArr: [],
      tableData: [
        {
          f1: 'SJC179',
          f2: '弗居绝对收益配置1号',
          f3: '股票市场中性',
          f4: '--',
          f5: '--',
          f6: '--',
          f7: '--',
          f8: '--',
          f9: '--',
          f10: '10.4107',
          f11: '10.4107',
          f12: '10.4107'
        },
        {
          f1: 'SVV251',
          f2: '粤资价值成长9号',
          f3: '房地产',
          f4: '--',
          f5: '--',
          f6: '--',
          f7: '--',
          f8: '--',
          f9: '--',
          f10: '13.1535',
          f11: '14.0598',
          f12: '25.0745'
        }
      ],
      tableData1: [
        {
          f1: '弗居绝对收益配置1号',
          f2: 94.17,
          f3: 10.4457,
          f4: 10.4177
        },
        {
          f1: '粤资价值成长9号',
          f2: -21.33,
          f3: 4.1657,
          f4: 0.7854
        },
        {
          f1: '沪深300',
          f2: -20.29,
          f3: 2.6875,
          f4: 0.9835
        }
      ],
      tableData2: [
        {
          f1: 'SJC179',
          f2: '弗居绝对收益配置1号',
          f3: '股票市场中性',
          f4: '--',
          f5: '--',
          f6: 15.26,
          f7: 23.15,
          f8: -21.05,
          f9: -33.47,
          f10: -6.78,
          f11: 64.15
        },
        {
          f1: 'SVV251',
          f2: '粤资价值成长9号',
          f3: '房地产',
          f4: '--',
          f5: '--',
          f6: 10.24,
          f7: 15.24,
          f8: 18.3,
          f9: -26.78,
          f10: -6.24,
          f11: -23.54
        }
      ],
      tableData3: [
        {
          f1: '弗居绝对收益配置1号',
          f2: 15.26,
          f2_color: 'color: green',
          f3: 23.15,
          f4: -21.05,
          f5: 2.97,
          f6: 12.61,
          f7: 8.97,
          f8: -6.78,
          f9: 3.57
        },
        {
          f1: '粤资价值成长9号',
          f2: 10.24,
          f3: 15.24,
          f4: 18.3,
          f5: 1.64,
          f6: 15.3,
          f7: 7.69,
          f8: -26.24,
          f9: 2.16
        },
        {
          f1: '沪深300',
          f2: 10.37,
          f3: 9.87,
          f4: 19.34,
          f5: 2.66,
          f6: 12.11,
          f7: 8.62,
          f8: -24.87,
          f9: 3.66
        }
      ],
      Columns: [
        { prop: 'f1', label: '产品代码', align: 'center' },
        { prop: 'f2', label: '产品名称', align: 'center' },
        { prop: 'f3', label: '投资策略', align: 'center' },
        { prop: 'f4', label: '管理人', align: 'center' },
        { prop: 'f5', label: '基金经理', align: 'center' },
        { prop: 'f6', label: '存续状态', align: 'center' },
        { prop: 'f7', label: '成立日期', align: 'center' },
        { prop: 'f8', label: '净值日期', align: 'center' },
        { prop: 'f9', label: '资产净值(万元)', align: 'center' },
        { prop: 'f10', label: '单位净值', align: 'center' },
        { prop: 'f11', label: '累计单位净值', align: 'center' },
        { prop: 'f12', label: '复权净值', align: 'center' }
      ],
      Columns1: [
        { prop: 'f1', label: '产品/对比指标', align: 'left', headerAlign: 'left', minWidth: '200' },
        { prop: 'f2', label: '收益率', align: 'center', headerAlign: 'center' },
        { prop: 'f3', label: '复权累计净值', align: 'center', headerAlign: 'center' },
        { prop: 'f4', label: '调整后点位', align: 'center', headerAlign: 'center' }
      ],
      Columns2: [
        { prop: 'f1', label: '产品代码', align: 'center' },
        { prop: 'f2', label: '产品名称', align: 'left' },
        { prop: 'f3', label: '投资策略', align: 'center' },
        { prop: 'f4', label: '管理人', align: 'center' },
        { prop: 'f5', label: '成立日期', align: 'center' },
        { prop: 'f6', label: '近一月收益率', align: 'right', setColor: true },
        { prop: 'f7', label: '近三月收益率', align: 'right', setColor: true },
        { prop: 'f8', label: '近六月收益率', align: 'right', setColor: true },
        { prop: 'f9', label: '近一年收益率', align: 'right', setColor: true },
        { prop: 'f10', label: '今年以来收益率', align: 'right', setColor: true },
        { prop: 'f11', label: '成立以来收益率', align: 'right', setColor: true }
      ],
      Columns3: [
        { prop: 'f1', label: '指标', align: 'center' },
        { prop: 'f2', label: '收益率(年化)', align: 'center', setColor: true },
        { prop: 'f3', label: '波动率(年化)', align: 'center', setColor: true },
        { prop: 'f4', label: '下行波动率(年化)', align: 'center', setColor: true },
        { prop: 'f5', label: '夏普比率(年化)', align: 'center' },
        { prop: 'f6', label: '索提诺比率(年化)', align: 'center' },
        { prop: 'f7', label: '信息(年化)', align: 'center' },
        { prop: 'f8', label: '最大回撤', align: 'center', setColor: true },
        { prop: 'f9', label: '卡玛比率', align: 'center' }
      ],
      total: 0,
      tableLoading: false,
      homeParams: [],

      productSelectorVisible: false,
      treeData: [
        {
          label: '产品列表',
          id: 'zstgwb'
        },
        {
          label: '我的关注',
          id: 'wdgz',
          children: [
            {
              label: '默认分组',
              id: 'mrfz'
            },
            {
              label: '权益组',
              id: 'qyz'
            }
          ]
        },
        {
          label: '私有产品',
          code: 'sycp'
        }
      ],
      showTreeKeyArray: ['产品列表', '我的关注'],
      selectList: [],

      lssyzsdbOptions: {
        tooltip: {
          trigger: 'axis',
          formatter: function (params) {
            var relVal = params[0].name
            for (var i = 0, l = params.length; i < l; i++) {
              relVal += '<br/>' + params[i].marker + params[i].seriesName + ':' + params[i].value.toFixed(2)
            }
            return relVal
          }
        },
        color: ['#faa000', '#458bf0', '#e93f30'],
        legend: {
          y: '4%',
          data: ['弗居绝对收益配置1号', '粤资价值成长9号', '沪深300']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '13%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          axisTick: {
            show: false
          },
          data: [
            '2023/1/24',
            '2023/1/25',
            '2023/1/26',
            '2023/2/3',
            '2023/2/6',
            '2023/2/7',
            '2023/2/8',
            '2023/2/9',
            '2023/2/10',
            '2023/2/13',
            '2023/2/14',
            '2023/2/15',
            '2023/2/16',
            '2023/2/17',
            '2023/2/20',
            '2023/2/21',
            '2023/2/22',
            '2023/2/23',
            '2023/2/24',
            '2023/2/27',
            '2023/2/28',
            '2023/3/1',
            '2023/3/2',
            '2023/3/3',
            '2023/3/6',
            '2023/3/7',
            '2023/3/8',
            '2017/3/9'
          ]
        },
        yAxis: [
          {
            type: 'value',
            axisLabel: {
              formatter: '{value} '
            },
            splitLine: {
              show: true,
              lineStyle: {
                type: 'solid',
                color: '#ececec'
              }
            },
            name: '净值',
            min: 0.98,
            max: 1.1
          }
        ],
        dataZoom: {
          show: true,
          start: 0,
          end: 50,
          maxSpan: 80
        },
        series: [
          {
            name: '弗居绝对收益配置1号',
            type: 'line',
            lineStyle: {
              normal: {
                width: 2
              }
            },
            data: [
              1, 1.02, 1.006987, 1.000011, 1.002603, 1.000365, 1.005599, 1.009463, 1.014575, 1.021349, 1.021207, 1.017019, 1.022731, 1.016938, 1.031785, 1.035182, 1.037245,
              1.032358, 1.032516, 1.024304, 1.026262, 1.027936, 1.020998, 1.018847, 1.02438, 1.026604, 1.02505, 1.018573, 1.018855, 1.027835, 1.027416, 1.029481, 1.034793,
              1.024182, 1.025311, 1.030287, 1.025442, 1.028988, 1.037197, 1.033761, 1.031315, 1.029942, 1.021492
            ]
          },
          {
            name: '粤资价值成长9号',
            type: 'line',
            lineStyle: {
              normal: {
                width: 2
              }
            },
            data: [
              1, 1.005093433, 1.013437423, 1.008349362, 1.021077573, 1.014995541, 1.02278613, 1.028400726, 1.023350276, 1.028185814, 1.025886247, 1.016730961, 1.019562438,
              1.011632155, 1.018127895, 1.0321617, 1.031565317, 1.034778264, 1.041488916, 1.035218835, 1.035428375, 1.038012701, 1.031796349, 1.036035504, 1.054560987, 1.062663199,
              1.055560331, 1.049816787, 1.047705269, 1.058918344, 1.052008897, 1.051901441, 1.056688624, 1.04751722, 1.049752313, 1.053642235, 1.046936955, 1.046824126,
              1.055834345, 1.046372809, 1.044669625, 1.03652443, 1.017450919
            ]
          },
          {
            name: '沪深300',
            type: 'line',
            lineStyle: {
              normal: {
                width: 2
              }
            },
            data: [
              1, 1.004020666, 1.010565602, 1.009638124, 1.016976676, 1.013885082, 1.022257884, 1.027115192, 1.026645079, 1.035793966, 1.036638577, 1.027723949, 1.035691975,
              1.030337462, 1.043213792, 1.051263091, 1.056388126, 1.056220797, 1.057400065, 1.051804917, 1.055859049, 1.058246269, 1.055573793, 1.064413521, 1.076067556,
              1.07753686, 1.070961645, 1.063933846, 1.07060149, 1.084953499, 1.08232405, 1.081551152, 1.090016382, 1.07724523, 1.077606979, 1.083783792, 1.081433225, 1.085240348,
              1.093407574, 1.088373375, 1.08544911, 1.08265552, 1.064013527
            ]
          }
        ]
      },
      dthcdbOptions: {
        tooltip: {
          trigger: 'axis',
          formatter: function (params) {
            var relVal = params[0].name
            for (var i = 0, l = params.length; i < l; i++) {
              relVal += '<br/>' + params[i].marker + params[i].seriesName + ':' + params[i].value.toFixed(2) + '%'
            }
            return relVal
          }
        },
        color: ['#6ba6e1', '#ef8080', '#ffc58c'],
        legend: {
          y: '4%',
          data: ['弗居绝对收益配置1号', '粤资价值成长9号', '沪深300']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '13%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          axisTick: {
            show: false
          },
          data: [
            '2023/1/24',
            '2023/1/25',
            '2023/1/26',
            '2023/2/3',
            '2023/2/6',
            '2023/2/7',
            '2023/2/8',
            '2023/2/9',
            '2023/2/10',
            '2023/2/13',
            '2023/2/14',
            '2023/2/15',
            '2023/2/16',
            '2023/2/17',
            '2023/2/20',
            '2023/2/21',
            '2023/2/22',
            '2023/2/23',
            '2023/2/24',
            '2023/2/27',
            '2023/2/28'
          ]
        },
        yAxis: {
          type: 'value',
          name: '回撤（%）',
          // axisLabel: {
          //   formatter: function (value) {
          //     return Math.abs(value)
          //   }
          // },
          axisLine: {
            show: false
          },
          axisTick: {
            show: false
          }
        },
        dataZoom: {
          show: true,
          start: 0,
          end: 50,
          maxSpan: 80
        },
        series: [
          {
            name: '弗居绝对收益配置1号',
            type: 'line',
            areaStyle: {
              normal: {
                color: '#6ba6e1'
              }
            },
            data: [-20, -32, -10, -34, -70, -30, -10, -20, -32, -10, -34, -70, -30, -10, -20, -32, -10, -34, -70, -30, -10]
          },
          {
            name: '粤资价值成长9号',
            type: 'line',
            areaStyle: {
              normal: {
                color: '#ef8080'
              }
            },
            data: [-20, -82, -91, -34, -20, -30, -50, -20, -82, -91, -34, -30, -30, -50, -30, -52, -91, -34, -20, -30, -50]
          },
          {
            name: '沪深300',
            type: 'line',
            areaStyle: {
              normal: {
                color: '#ffc58c'
              }
            },
            data: [-15, -23, -21, -54, -60, -50, -41, -85, -93, -81, -34, -40, -50, -41, -15, -23, -21, -54, -60, -50, -41]
          }
        ]
      },

      // tabs数据源
      tabArr: [
        // {
        //   label: '产品表现',
        //   name: 'jbxxdb'
        // },
        // {
        //   label: '产品信息',
        //   name: 'yjdb'
        // },
        // {
        //   label: '深度分析',
        //   name: 'fxdb'
        // }
        {
          label: '基本信息对比',
          name: 'jbxxdb'
        },
        {
          label: '业绩对比',
          name: 'yjdb'
        },

        {
          label: '风险对比',
          name: 'fxdb'
        }
      ],
      // 当前激活tabs
      activeName: 'jbxxdb',
      // 动态组件映射关系
      compMapRelation: {
        jbxxdb: 'baseInfo',
        yjdb: 'performanceCompare',
        fxdb: 'riskCompare'
      },

      // 当前选中的node节点
      currentNodeKey: ''
    }
  },
  activated() {},
  mounted() {
    this.getKpiOptions()
    this.getContrasOptions()
  },
  watch: {
    homeParams(val, oldval) {
      let productCodesArr = []
      let productNamesArr = []
      this.homeParams.forEach((element) => {
        productCodesArr.push(element.VC_FUNDCODE)
        productNamesArr.push(element.VC_FUNDNAME)
      })
      this.formQuery.productCodes = productCodesArr.join(',')
      this.formQuery.productNames = productNamesArr.join(',')
    },
    '$route.query.list': {
      handler(newVal) {
        if (newVal) {
          const query = this.$route.query
          if (this.$store.getters.fromPageJump) {
            if (query.list && query.list instanceof Array) {
              this.homeParams = []
              query.list.forEach((element) => {
                let newObj = {}
                newObj.VC_FUNDCODE = element.fundCode
                newObj.VC_FUNDNAME = element.fundName
                this.homeParams.push(newObj)
              })
              let productCodesArr = []
              let productNamesArr = []
              this.homeParams.forEach((element) => {
                productCodesArr.push(element.VC_FUNDCODE)
                productNamesArr.push(element.VC_FUNDNAME)
              })
              this.formQuery.productCodes = productCodesArr.join(',')
              this.formQuery.productNames = productNamesArr.join(',')
              this.$nextTick(() => {
                this.onQuery()
              })
              this.$store.commit('SET_FROMPAGEJUMP', false)
            }
          }
        }
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    /**
     * @description 获取业绩基准下拉
     */
    getKpiOptions() {
      return new Promise((resolve, reject) => {
        request({
          url: `/api/report/v1.0/data/sql/9d40fd1a-b804-4cfb-926f-c7f4174269c2`,
          method: 'post',
          data: {
            indexCode: '9d40fd1a-b804-4cfb-926f-c7f4174269c2'
          }
        })
          .then((res) => {
            if (res.data.status === 0) {
              const resultDim = res.data.data || []
              this.kpiStandardOpts = resultDim.map((item) => {
                return {
                  label: item.DIM_NME,
                  id: item.DIM_CDE,
                  checked: false
                }
              })
              this.formQuery.kpiCode = '000300'
              resolve()
            }
          })
          .catch((err) => {
            reject(err)
          })
      })
    },
    /**
     * @description 获取对比基准下拉
     */
    getContrasOptions() {
      request({
        url: `/api/report/v1.0/data/sql/ecd8867c-64cc-4ebc-9070-04524b04b72c`,
        method: 'post',
        data: {
          indexCode: 'ecd8867c-64cc-4ebc-9070-04524b04b72c'
        }
      }).then((res) => {
        if (res.data.status === 0) {
          const resultDim = res.data.data || []
          this.dbjzArr = resultDim.map((item) => {
            return {
              label: item.DIM_NME,
              value: item.DIM_CDE
            }
          })
          if (this.dbjzArr.length > 0) {
            this.formQuery.dbjz =["000300"] /* 改为默认沪深300[this.dbjzArr[0].value] */
          }
        }
      })
    },
    /**
     * @description 监听对比基准下拉
     */
    changeContrasCode(val) {
      if (val.length > 4) {
        this.$message({
          type: 'warning',
          message: '对比基准最多只能选四个'
        })
        this.formQuery.dbjz.splice(-1)
      }
    },
    /**
     * @desc 解决点击iframe无法收起下拉框
     * @param { Boolean } val 遮罩状态
     */
    uploadCover(val) {
      this.coverDiv = val
    },
    // 重置
    resetForm() {
      this.$refs['formQuery'].resetFields()
    },
    // 查询
    onQuery(flag) {
      this.tabLeftSelect = true
      this.tabCenterSelect = true
      this.tabRightSelect = true

      // 重置 标签页查询
      // this.$refs[this.compMapRelation[this.activeName]].initData()
      if (this.activeName == 'jbxxdb') {
        this.tabLeftSelect = false
        this.$refs['jbxxdb'][0].initData()
        // this.$refs['yjdb'][0].initData()
      } else if (this.activeName == 'yjdb') {
        this.tabCenterSelect = false
        this.$refs['yjdb'][0].initData()
      } else {
        this.tabRightSelect = false
        this.$refs['fxdb'][0].initData()
      }
      // 只查询当前 激活页面的initData方法
      // for (let key in this.compMapRelation) {
      //   debugger
      //   this.$refs[key][0].initData()
      // }
    },
    // 分页
    pagination() {},
    //关闭已选产品
    handleClose(index) {
      this.homeParams.splice(index, 1)
    },
    //风险对比设置单元格背景颜色
    myclass({ row, column, rowIndex, columnIndex }) {
      if (rowIndex == 0) {
        if (columnIndex != 0) {
          if (columnIndex == 7) {
            return 'setclass1'
          } else {
            return 'setclass'
          }
        }
      } else if (rowIndex == 1) {
        if (columnIndex != 0) {
          if (columnIndex == 7) {
            return 'setclass'
          } else {
            return 'setclass1'
          }
        }
      }
      // if(columnIndex == 1 && rowIndex == 0){
      //   return 'setclass';
      // }
    },

    handleDialogClosed() {
      this.productSelectorVisible = false
    },
    handleSubmitClick(arr) {
      this.productSelectorVisible = false
      this.homeParams = arr
    },
    handleDateChange(val) {
      if (!val) {
        this.formQuery.startDate = ''
        this.formQuery.endDate = ''
        return
      }
      if (val === '7') {
      } else {
        this.formQuery.startDate = dateShortcutMap[val].onClick()[0]
        this.formQuery.endDate = dateShortcutMap[val].onClick()[1]
      }
    },

    /**
     * @desc tabs被点击时的回调，点击时初始化查询子页面
     */
    handleTabClick(tab) {
      this.activeName = tab.name
      if (this.activeName == 'jbxxdb' && this.tabLeftSelect) {
        this.tabLeftSelect = false
        this.$refs['jbxxdb'][0].initData()
        // this.$refs['yjdb'][0].initData()
      } else if (this.activeName == 'yjdb' && this.tabCenterSelect) {
        this.tabCenterSelect = false
        this.$refs['yjdb'][0].initData()
      } else if (this.activeName == 'fxdb' && this.tabRightSelect) {
        this.tabRightSelect = false
        this.$refs['fxdb'][0].initData()
      }
    }
    /**
     * @desc 解决点击iframe无法收起下拉框
     * @param { Boolean } val 遮罩状态
     */
  }
}
</script>

<style lang="scss">
// @import './styles/index';
.multiProductDetail {
  padding: 0.5%;

  .title-style {
    color: #0F65DD;
    height: 16px;
    line-height: 16px;
    padding-left: 8px;
    font-size: 14px;
    border-left: 2px solid #0F65DD;
    margin-bottom: 5px;
  }

  .yjjz {
    .el-select .el-input--small {
      width: 180px !important;
    }
  }

  .dbjz {
    .el-select .el-input--small {
      width: 220px !important;
    }

    .el-select .el-select__tags {
      max-width: 200px !important;
    }
  }

  .line {
    height: 10px;
    border-bottom: 1px solid #409eff;
    margin-bottom: 25px;
  }

  .tip {
    margin-top: 5px;
    line-height: 30px;
    font-size: 14px;
    color: #333;
  }

  .tableStyle {
    border: 1px solid #dcdfe6;
    border-bottom: none;
    margin-top: 20px;
  }

  .el-table thead {
    height: 40px !important;
  }

  .el-tabs__item {
    height: 40px !important;
    line-height: 35px !important;
  }

  .elTabs {
    margin-bottom: 50px;
    min-height: 500px;
  }

  .echartBox {
    width: 100%;
    height: 350px;
  }

  .mr5 {
    margin-right: 5px;
  }

  .mr20 {
    margin-right: 20px;
  }

  .setclass {
    background-color: #79cc79;
  }

  .setclass1 {
    background-color: #ffc7c7;
  }

  .el-button.el-button--info {
    background-color: #f4f4f5;
    color: #612d10;
  }

  .el-tabs--border-card>.el-tabs__header .el-tabs__nav {
    border: 1px solid #E4E7ED;
    border-bottom: none;
    border-radius: 4px 4px 0 0;
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
  }

  .el-tabs--border-card > .el-tabs__header .el-tabs__item:first-child {
    border-left: none;
  }

  .el-tabs--border-card > .el-tabs__header .el-tabs__item {
    border-top: 2px solid transparent;
    color: #612d10;
    background-color: #fcf8f4 !important;
    border-bottom: 1px solid transparent;
    border-left: 1px solid #E4E7ED;
  }

  .el-tabs--border-card > .el-tabs__header .el-tabs__item:hover {
    //color: #0F65DD;
  }

  .el-tabs--border-card > .el-tabs__header .el-tabs__item.is-active {
    color: #612d10;
    background-image: linear-gradient(to right, #f5d7bc, #e0b794) !important;
    //font-weight: bold;
  }

  .el-tag {
    border: none;
    color: #612d10 !important;
    background-image: linear-gradient(to right, #f5d7bc, #e0b794) !important;
  }

  .el-tag >.el-tag__close{
    color: #612d10 !important;
  }
  .el-tag>.el-tag__close:hover {
    background-color: transparent;
  }
  .el-select .el-tag__close.el-icon-close{
    background-color:transparent;
  }
  .el-form-item__label {
    color: #333333 !important;
  }
}

</style>

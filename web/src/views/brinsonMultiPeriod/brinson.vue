<template>
  <!--brinson-zhangzhiyong-@Author: zhangzhiyong @Date: 2023/12/29 14:22 -->
  <div class="brinson">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formQuery" :inline="true" :rules="searchRules" :model="formQuery" class="standard-form">
          <el-row>
            <el-col :span="24">
              <el-form-item prop="fundNames">
                <span slot="label" class="item-label">产品</span>
                <el-tooltip class="item" effect="dark" :content="formQuery.fundNames" placement="top-start" :disabled="!formQuery.fundNames">
                  <el-input v-model.trim="formQuery.fundNames" clearable placeholder="请输入" size="small" @click.native="openFundListDialog" @change="handleFundNamesChange" />
                </el-tooltip>
              </el-form-item>
              <el-form-item prop="ddate_" label="日期" class="mb20">
                <el-date-picker
                  v-model="formQuery.ddate_"
                  type="daterange"
                  value-format="yyyy-MM-dd"
                  align="left"
                  size="small"
                  unlink-panels
                  range-separator="至"
                  start-placeholder="开始日期"
                  end-placeholder="结束日期"
                  popper-class="popperDateShortTP"
                  :picker-options="dateShortTPCTA()"
                ></el-date-picker>
              </el-form-item>
              <el-form-item class="">
                <el-button type="primary" size="small" icon="el-icon-search" @click="onSubmit('formQuery')">查询</el-button>
                <el-button type="info" @click="resetForm('formQuery')" icon="el-icon-refresh" size="small" plain>重置</el-button>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>
    </div>

    <el-row>
      <div class="page-model-title">
        <div class="title-icon">
          <div class="color-box"></div>
        </div>
        <span class="title-txt">Brinson模型分析</span>
      </div>
      <!-- <el-col :span="8">
        <div style="float: right">
          <vxe-toolbar
            ref="tableToolbar"
            :custom="{ immediate: true }"
            custom
          />
        </div>
      </el-col>-->
    </el-row>

    <el-row id="standard-table">
      <div id="standard-table-margin">
        <vxe-table
          v-loading="tableLoading"
          :data="tableData"
          :cell-style="{ height: '50px' }"
          auto-resize
          sync-resize
          style="width: 100%"
          max-height="500"
          show-overflow
          :tree-config="{ children: 'children', transform: true, rowField: 'id', parentField: 'parentId' }"
          resizable
        >
          <vxe-table-column field="fundCode" label="产品代码" align="center" show-overflow-tooltip header-align="center" min-width="200" tree-node></vxe-table-column>
          <vxe-table-column
            v-loading="tableLoading"
            v-for="(col, i) in tableColumns"
            :key="i"
            :field="col.prop"
            :label="col.label"
            min-width="200"
            :align="col.align"
            show-overflow-tooltip
            header-align="center"
          >
            <template slot-scope="scope">
              <span
                v-if="
                  col.prop == 'initialWeight' ||
                  col.prop == 'benchWeight' ||
                  col.prop == 'fundYield' ||
                  col.prop == 'benchYield' ||
                  col.prop == 'excessAlloc' ||
                  col.prop == 'excessYield' ||
                  col.prop == 'assetAllocYield' ||
                  col.prop == 'choiceYield' ||
                  col.prop == 'interactYiled'
                "
              >
                {{ scope.row[col.prop] | baifenlv2 }}
              </span>
              <span v-else>{{ scope.row[col.prop] | noDataFilter }}</span>
            </template>
          </vxe-table-column>
        </vxe-table>
      </div>
    </el-row>

    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formQueryB" :inline="true" :model="below" class="standard-form">
          <el-form-item label="产品代码" prop="fundCode">
            <el-select v-model="below.fundCode" placeholder="请选择" size="small">
              <el-option v-for="item in optionsFund" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="small" icon="el-icon-search" @click="onConfirm()">确定</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>

    <el-row>
      <el-col>
        <div class="chart-content">
          <myChart v-loading="charLoading" id="gzzbzs" ref="gzzbzs" :options="targetTrendOptions" class="echarts_box" resize-dom="cmbfof" />
        </div>
      </el-col>
    </el-row>
    <!--    <el-dialog
      v-if="dialogMask"
      :visible.sync="dialogMask"
      :close-on-click-modal="false"
      title="产品信息"
      center
      custom-class="customWidth"
    >
      <el-container class="hg100">
        <el-main class="mainBox">
          <FundListDialogMultiphase
            @getTemplateRow="getTemplateRow"
            :tagsinfo="tags"
          />
        </el-main>
      </el-container>
    </el-dialog>-->
    <product-selector
      :multiple="true"
      :leftList="false"
      :dialog-visible="dialogMask"
      :tree-data="treeData"
      :show-tree-key-array="showTreeKeyArray"
      :select-list="selectList"
      default-checked-keys="wdgz"
      @closedialog="handleDialogClosed"
      @submitdialog="handleSubmitClick"
    ></product-selector>
  </div>
</template>
<script type="text/ecmascript-6">
  import { downLoadFileByUrl } from '@/utils'
import Pagination from "@/components/Pagination";
  import myChart from '@/components/Echarts'
import fun from "@/filters/common";
import commonApi from "@/api/common";
import brinsonApi from "@/api/brinsonMultiPeriod/brinson";
import FundListDialogMultiphase from '@/components/FundListDialogMultiphase';
import moment from 'moment'
import { BRINSON_TABLE } from './scripts/policy'
import productSelector from '@/components/productSelector'

export default {
  name: "brinson",
  components: {
    myChart,
    Pagination,
    FundListDialogMultiphase,
    productSelector
  },
  data() {

    return {
      // 搜索
      formQuery: {
        ddate_: [],
        beginDate: "",
        endDate: "",
        fundCodes: [],
        fundNames: "",
      },
      below:{
        beginDate: "",
        endDate: "",
        fundCode:"",
        fundCodes:[],
        fundNames:[]
      },
      optionsFund:[],
      //echarts
      targetTrendOptions: {},
      // 所有数据
      Datas: [],
      echartsData: [],
      // 表格数据
      tableData: [],
      tableColumns: BRINSON_TABLE,
      issearchButton: false,
      tableLoading: false,
      charLoading:false,
      total: 0,
      dialogMask: false,
      searchRules: {
        ddate_: [{ required: true, message: "请选择日期", trigger: "change" }],
        fundNames: [{ required: true, message: "请选择产品", trigger: "change" }]
      },
      selectList: [],
      treeData: [
        {
          label: '产品列表',
          id: 'zstgwb'
        },{
          label: '私有产品',
          id: 'sycp'
        },{
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
        }
      ],
      showTreeKeyArray: ['产品列表','私有产品','我的关注'],
      //成立日
      timDate:"",
      /* 按钮禁止与否 */
      isDisabled: false,
      // 导出图标
      downLoadIcon: "el-icon-download",
      // 导出提示文字
      downLoadText: "导出",
      exportLoading: false,

      baseApi: "", // 页面根地址
      exportButton: false,
      exportText: "导出",
      exportIcon: "el-icon-download",
      tags: []
    };
  },
  watch: {
    'formQuery.beginDate'() {
      this.below.beginDate = this.formQuery.beginDate
    },
    'formQuery.endDate'() {
      this.below.endDate = this.formQuery.endDate
    }
  },
  mounted() {},

  methods: {
    //清空input
    handleFundNamesChange(val) {
      if (!val) {
        this.tags = [];
        this.formQuery.fundCodes = [];
        this.formQuery.fundNames = "";
      }
    },
    // 获取选中数据
    getTemplateRow(val) {
      this.tags = val.data;
      const self = this;
      const arr = val.data;
      if (arr) {
        self.formQuery.fundCodes = [];
        self.formQuery.fundNames = "";
        self.below.fundCodes = [];
        self.below.fundNames = [];
        arr.forEach(function (item, index) {
          index++;
          if (index < arr.length) {
            self.formQuery.fundNames = self.formQuery.fundNames + item.fundName + ",";
          } else {
            self.formQuery.fundNames = self.formQuery.fundNames + item.fundName;
          }
          self.timDate = item.createDate;
          self.formQuery.fundCodes.push(item.fundCode);
          self.below.fundCodes.push(item.fundCode);
          self.below.fundNames.push(item.fundName);

        });
      }
      this.dialogMask = false;
    },
    handleDialogClosed() {
      this.dialogMask = false
    },
    handleSubmitClick(arr) {
      const self = this;
      this.dialogMask = false
      if (arr) {
        self.formQuery.fundCodes = [];
        self.formQuery.fundNames = "";
        self.below.fundCodes = [];
        self.below.fundNames = [];
        arr.forEach(function (item, index) {
          index++;
          if (index < arr.length) {
            self.formQuery.fundNames = self.formQuery.fundNames + item.VC_FUNDNAME + ",";
          } else {
            self.formQuery.fundNames = self.formQuery.fundNames + item.VC_FUNDNAME;
          }
          self.timDate = item.D_CREATE_DATE;
          self.formQuery.fundCodes.push(item.VC_FUNDCODE);
          self.below.fundCodes.push(item.VC_FUNDCODE);
          self.below.fundNames.push(item.VC_FUNDNAME);

        });
      }
      this.selectList = arr
    },
    // 点击弹窗
    openFundListDialog() {
      this.dialogMask = true;
    },

    onSubmit(formName) {
      var self = this;
      self.optionsFund = [];
      if(self.below.fundCodes.length > 0){
        self.below.fundCode = self.below.fundCodes[0]
        for(var i=0;i<self.below.fundCodes.length;i++){
          self.optionsFund.push({value:self.below.fundCodes[i],label:self.below.fundNames[i]})
        }
      }
      self.$refs[formName].validate((valid) => {
        if (valid) {
          self.onQuery();
          // 禁用搜索按钮
          self.$fun.searchButtonDisabled("issearchButton", self);
        } else {
          return false;
        }
      });
    },
    //确定
    onConfirm() {
      var self = this
      const params = Object.assign({}, this.below, {});
      this.charLoading = true
      new Promise((resolve, reject) => {
        brinsonApi.fun_selectbrinsonChar(params).then((res) => {
          self.handleChartOptions(res)
          this.charLoading = false
        })
          .catch((error) => {
            this.charLoading = false
            reject(error);
          });
      });


    },
    handleChartOptions(data) {
      var excludeField = ['industryName', 'fundCode', 'fundName', 'industryCode', 'excessAlloc'
        ,'benchWeight','benchYield','fundYield','initialWeight'];
      var includeFiled={
         //'industryName':'行业名称',
         //'industryCode':'行业代码',
        //'excessAlloc':'超额配置',
        'excessYield':'超额收益',
        'assetAllocYield':'资产配置收益率',
        'choiceYield':'选择收益'
        ,'interactYiled':'交互收益'
      };
      var xAxisData = [];
      var itemStyle = {
        normal: {
        },
        emphasis: {

        }
      };

      var preSeries = [];

      for(var i in data){
        for(var j in data[i]){
          if(excludeField.indexOf(j) !== -1){
            continue;
          }
          var type = 'bar';
          var stack = 'one';

          var obj = {};
          if(j === 'excessYield'){
            obj = {name : includeFiled[j], type:'line', stack:'two', itemStyle: itemStyle, data:[]};
          }else{
            obj = {name : includeFiled[j], type:type, barMaxWidth:'120px',stack:'one',itemStyle: itemStyle, data:[]};
          }
          preSeries[j] = obj;
        }

      }

      var rows = data;

      for(var i  = 0; i < rows.length; ++i){
        for(var j in rows[i]){

          if(excludeField.indexOf(j) !== -1){
            if(j === 'industryName'){
              xAxisData.push(rows[i][j]);
            }
            continue;
          }
          //排除不需要显示的图例数据
          if(excludeField.indexOf(j) != -1){
            continue;
          }
          preSeries[j]['data'].push(Number(rows[i][j] * 100).toFixed(2));
        }
      }
      var legendData = [];
      var serise = [];
      for(var i in preSeries){
        serise.push(preSeries[i]);
        legendData.push(preSeries[i].name);
      }
      this.targetTrendOptions = {
        // backgroundColor: '#eee',
        legend: {
          data: legendData,
          // align: 'left',
          // left: 10
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross',
            crossStyle: {
              color: '#999'
            }
          }
        },
        toolbox: {

        },
        xAxis: {
          data: xAxisData,
          name: '',
          silent: false,
          axisLine: {onZero: true},
          splitLine: {show: false},
          splitArea: {show: false},
          type:'category',
          //axisTick:{interval:0}
          axisLabel: {
            interval:0,
            rotate:40
          }
        },
        yAxis: {
          type:'value',
          axisLabel: {
            formatter: '{value}%'
          }
        },

        series: serise

      };
    },

    onQuery(flag) {
      var self = this;
      const params = Object.assign({}, this.formQuery, {});
      if (params.ddate_ && params.ddate_.length) {
        params.beginDate = params.ddate_[0];
        params.endDate = params.ddate_[1];
        self.formQuery.beginDate = params.ddate_[0];
        self.formQuery.endDate = params.ddate_[1];
      }
      if (!flag) {
        this.tableLoading = true;
      }
      new Promise((resolve, reject) => {
        brinsonApi.fun_selectbrinson(params).then((res) => {
          const data = res
            if (data != null) {
              if (data != null && data != undefined) {
                self.Datas = data;
                const map = {}
                const val = []
                for (var i = 0; i < data.length; i++) {
                  map[data[i].id] = data[i]
                }
                for (var i = 0; i < data.length; i++) {
                  const parent = map[data[i].parentId]
                  if (parent) {
                    ;(parent.children || (parent.children = [])).push(data[i])
                  } else {
                    val.push(data[i])
                  }
                }
                this.tableData = val
                self.onConfirm();
              }
            } else {
              self.$message({
                message: "系统异常",
                type: "warning"
              });
            }
            this.tableLoading = false;
            self.exportLoading = false;
            self.downLoadText = "导出";
          })
          .catch((error) => {
            this.tableLoading = false;
            self.exportLoading = false;
            self.downLoadText = "导出";
            reject(error);
          });
      });
    },

    //导出数据
    exportData() {
      if(this.formQuery.ddate_.length == 0 || this.formQuery.fundCodes.length ==0){
        this.$message({
          message: "请输入查询条件！",
          type: "warning"
        });
      }else{
      this.downLoadText = "导出中...";
      this.exportLoading = true;
      this.isDisabled = true;
      const params = Object.assign({}, this.formQuery, {});
      if (params.ddate_ && params.ddate_.length) {
        params.beginDate = params.ddate_[0];
        params.endDate = params.ddate_[1];
      }
      const fileName = '估值指标走势.xls'
      const url = 'api/combinedQuery/fundQuery/export'
      downLoadFileByUrl(url, params, fileName, this)
      setTimeout(() => {
        this.tableLoading = false;
        this.exportLoading = false;
        this.downLoadText = "导出";
      }, 5000)
      }

    },

    //日期时间段快捷选项
    dateShortTPCTA() {
      var self = this
      const pickerOptions = {
        shortcuts: [{
          text: '本周',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
            const start = moment(end).isoWeekday(1).format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '本月',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
            const start = moment([moment(end).year(), 0, 1]).month(moment(end).month()).format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '本季度',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
            const start = moment(moment(end).year() + '-01-01').quarter(moment(end).quarter()).format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '今年以来',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
            const start = moment(end).year() + '-01-01'
            picker.$emit('pick', [start, end])
          }
        },
          {
            text: '成立以来',
            onClick(picker) {
              self.getStandard();
                const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
                const start = self.timDate
                picker.$emit('pick', [start, end])
            }
          },
          {
            text: '近一个月',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(1, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          }, {
            text: '近三个月',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(3, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          }, {
            text: '近半年',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(6, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          }, {
            text: '近一年',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(1, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          }, {
            text: '近三年',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(3, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          },]
      }
      return pickerOptions
    },
    //成立日选择校验
    async getStandard() {
      if(this.formQuery.fundCodes.length == 0 || this.formQuery.fundNames ==""){
        this.timDate =""
        this.$message({
          message: '请先选择产品！',
          type: 'warning'
        });
        return
      }
      if(this.formQuery.fundCodes.length > 1){
        this.timDate =""
        this.$message({
          message: '请选择单个产品！',
          type: 'warning'
        });
        return
      }
     if(this.timDate == "" || this.timDate == undefined || this.timDate == null){
       this.$message({
         message: '未获取到成立日！',
         type: 'warning'
       });
       return
     }

    },
    // 清除
    resetForm(formName) {
      this.$refs[formName].resetFields();
      this.tags = [];
      this.formQuery.fundCodes = [];
      this.formQuery.fundNames = "";
    },

  }
};
</script>

<style lang="scss">
.brinson {
  .funds-filter {
    width: 100%;
    // border-bottom: 1px solid #e1e0e0;
  }

  .p1 {
    font-family: FZLanTingHei;
    font-weight: 500;
    font-size: 14px;
    color: rgb(16, 16, 16);
    font-style: normal;
    letter-spacing: 0px;
    line-height: 20px;
    text-decoration: none;
    text-align: left;
  }

  input::-webkit-input-placeholder {
    color: #999 !important;
  }

  .customWidth {
    width: 70% !important;
  }

  .el-tabs__item {
    line-height: 50px !important;
    height: 50px !important;
  }

  .el-checkbox-button__inner {
    border: 0px solid !important;
    border-radius: 0px !important;
  }

  .el-checkbox-button--medium {
    margin-right: 10px;
  }

  .el-checkbox-group {
    float: left;
  }

  .item-label {
    font-size: 14px;
  }
  .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
  .title-style {
    color: #e03d3e;
    vertical-align: middle;
    height: 35px;
    line-height: 35px;
    font-size: 16px;
    margin-left: 5px;
  }
  .color-box {
    display: inline-block;
    height: 30px;
    width: 2px;
    background-color: #e03d3e;
  }
  .vxe-pager.size--medium {
    font-size: 14px;
  }

  .el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell {
    background: #f8f8f8;
  }

  .el-checkbox-button--medium .el-checkbox-button__inner {
    font-size: 16px;
  }

  .customWidth {
    width: 70% !important;
  }

  .el-tabs__item {
    line-height: 50px !important;
    height: 50px !important;
  }
  .chart-content {
    height: 500px;
    margin-top: 5px;

    .echarts_box {
      height: 100%;
      width: 100%;
    }
  }
  .el-dialog {
    width: 54% !important;

    .el-form {
      width: 100% !important;
      font-size: 0;
    }

    .el-form-item {
      min-width: 50%;
      margin-right: 0;
    }
    ::v-deep .vxe-table .vxe-body--row.row--stripe {
      background-color: #f9fafe !important;
    }
    .mr5 {
      margin-right: 5px;
    }
  }
}
</style>

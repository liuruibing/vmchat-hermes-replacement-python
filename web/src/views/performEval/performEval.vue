<template>
  <!--收益分析-zhangzhiyong-@Author: zhangzhiyong @Date: 2023/10/9 14:22 -->
  <div class="performEval">
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
              <el-form-item label="基准类型">
                <el-select v-model="formQuery.ZB_INDEXTYPE" placeholder="请选择" size="small">
                  <el-option v-for="item in ZB_INDEXTYPEOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="选择基准" v-show="formQuery.ZB_INDEXTYPE == 'djz'">
                <el-select v-model="formQuery.ZB_INDEXCODEA" placeholder="请选择" size="small">
                  <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="基准 A" v-show="formQuery.ZB_INDEXTYPE == 'fhjz'">
                <el-select v-model="formQuery.ZB_INDEXCODEA" placeholder="请选择" size="small">
                  <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="比例" v-show="formQuery.ZB_INDEXTYPE == 'fhjz'">
                <el-input v-model="formQuery.ZB_INDEXWEIGHTA" size="small" style="width: 85px !important" @blur="handleInputWeight('A')"></el-input>
                %
              </el-form-item>
              <el-form-item label="基准 B" v-show="formQuery.ZB_INDEXTYPE == 'fhjz'">
                <el-select v-model="formQuery.ZB_INDEXCODEB" placeholder="请选择" size="small">
                  <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="比例" v-show="formQuery.ZB_INDEXTYPE == 'fhjz'">
                <el-input v-model="formQuery.ZB_INDEXWEIGHTB" size="small" style="width: 85px !important" @blur="handleInputWeight('B')"></el-input>
                %
              </el-form-item>
              <el-form-item>
                <el-button type="primary" size="small" icon="el-icon-search" @click="onSubmit('formQuery')">查询</el-button>
                <el-button type="info" size="small" plain icon="el-icon-refresh" @click="resetForm('formQuery')">重置</el-button>
                <el-dropdown v-model="visible">
                  <el-button
                    type="info"
                    plain
                    @click="handleClick"
                    size="small"
                    class="el-dropdown-link"
                    :icon="exportLoading2 ? 'el-icon-loading' : 'el-icon-download'"
                    :disabled="isDisabled2"
                  >
                    导出
                  </el-button>
                  <el-dropdown-menu slot="dropdown">
                    <el-menu
                      v-for="(item, index) in menuItems"
                      :key="index"
                      :index="item.index"
                      :default-active="item.index"
                      class="el-menu-vertical-demo standard-dropdown"
                      mode="vertical"
                      @select="handleSelect"
                    >
                      <el-menu-item :index="item.index">{{ item.name }}</el-menu-item>
                    </el-menu>
                  </el-dropdown-menu>
                </el-dropdown>
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
        <span class="title-txt">组合收益率分析</span>
      </div>
      <!-- <el-col :span="8">
         <div style="float: right">
         <el-button
           type="info"
           :icon="exportLoading ? 'el-icon-loading' : 'el-icon-download'"
           :disabled="isDisabled"
           @click="downloadTableExcel"
         >{{ downLoadText }}
         </el-button>
         </div>
       </el-col>-->
    </el-row>

    <el-row id="standard-table">
      <el-col>
        <div id="standard-table-margin">
          <vxe-table v-loading="tableLoading" show-overflow :data="tableData" :cell-style="{ height: '50px' }" auto-resize sync-resize style="width: 100%" max-height="500" resizable>
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
                    col.prop == 'yield' ||
                    col.prop == 'benchyield' ||
                    col.prop == 'excessyield' ||
                    col.prop == 'standarddeviation' ||
                    col.prop == 'benchstandarddeviation' ||
                    col.prop == 'last1monthyield' ||
                    col.prop == 'last3monthyield' ||
                    col.prop == 'last1yearyield' ||
                    col.prop == 'sincebornyield'
                  "
                >
                  {{ scope.row[col.prop] | baifenlv2 }}
                </span>
                <span v-else>{{ scope.row[col.prop] | noDataFilter }}</span>
              </template>
            </vxe-table-column>
          </vxe-table>
        </div>
      </el-col>
    </el-row>
    <el-row>
      <div class="page-model-title">
        <div class="title-icon">
          <div class="color-box"></div>
        </div>
        <span class="title-txt">组合业绩分析</span>
      </div>

      <!--  <el-col :span="8">
          <div style="float: right">
            <el-button
              type="info"
              :icon="exportLoading2 ? 'el-icon-loading' : 'el-icon-download'"
              :disabled="isDisabled2"
              @click="downloadTableExcel2"
            >{{ downLoadText2 }}
            </el-button>
          </div>
        </el-col>-->
    </el-row>

    <el-row id="standard-table">
      <div id="standard-table-margin">
        <vxe-table v-loading="tableLoading2" show-overflow :data="tableData2" :cell-style="{ height: '50px' }" auto-resize sync-resize style="width: 100%" max-height="500" resizable>
          <vxe-table-column
            v-loading="tableLoading2"
            v-for="(col, i) in tableColumns2"
            :key="i"
            :field="col.prop"
            :label="col.label"
            min-width="200"
            :align="col.align"
            show-overflow-tooltip
            header-align="center"
          >
            <template slot-scope="scope">
              <span v-if="col.prop == 'beta' || col.prop == 'sharp' || col.prop == 'sortino' || col.prop == 'inforatio'">{{ scope.row[col.prop] | moneyYuan }}</span>
              <span
                v-else-if="
                  col.prop == 'alpha' ||
                  col.prop == 'daywin' ||
                  col.prop == 'yearvar' ||
                  col.prop == 'since3monthmaxdraw' ||
                  col.prop == 'sinceyearbeginmaxdraw' ||
                  col.prop == 'sincebornmaxdraw'
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
        <el-form :inline="true" :model="below" class="standard-form">
          <el-form-item prop="fundCode" label="产品代码">
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
          <myChart v-loading="chartLoading2" id="zhsylfx" ref="zhsylfx" :options="targetTrendOptions" class="echarts_box" resize-dom="cmbfof" />
        </div>
      </el-col>
    </el-row>
    <el-row>
      <el-col>
        <div class="chart-content">
          <myChart v-loading="chartLoading" id="zhyjfx" ref="zhyjfx" :options="targetTrendOptions2" class="echarts_box" resize-dom="cmbfof" />
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
import {downLoadFileByUrl} from '@/utils'
import Pagination from "@/components/Pagination";
import myChart from '@/components/Echarts'
import performEvalApi from "@/api/performEval/performEval";
import FundListDialogMultiphase from '@/components/FundListDialogMultiphase';
import request from '@/utils/request'
import moment from 'moment'
import {ASSET_TABLE, ASSET2_TABLE} from './scripts/policy'
import productSelector from '@/components/productSelector'

export default {
  name: "performEval",
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
        ZB_INDEXCODE: '', // 基准编码
        ZB_INDEXTYPE: 'djz', // 基准类型
        ZB_INDEXCODEA: '000300', // 基准A
        ZB_INDEXWEIGHTA: '0.0000', // 基准A权重
        ZB_INDEXCODEB: '000300', // 基准B
        ZB_INDEXWEIGHTB: '0.0000', // 基准B权重
        offset: 0,
        limit: 99999
      },
      visible: false,
      menuItems: [
        {index: '1', name: '组合收益率分析'},
        {index: '2', name: '组合业绩分析'},
      ],
      ZB_INDEXTYPEOption: [
        {
          id: 'djz',
          label: '单基准'
        },
        {
          id: 'fhjz',
          label: '复合基准'
        }
      ],
      datumOption: [],
      below: {
        fundCode: '',
        fundCodes: [],
        fundNames: [],
        beginDate: "",
        endDate: "",
        benchmarkA: '',
        benchmarkB: '',
        benchmarkAValue: '',
        benchmarkBValue: '',
      },
      isVisible: true,
      optionsFund: [],
      //echarts
      targetTrendOptions: {},
      targetTrendOptions2: {},
      // 所有数据
      Datas: [],
      echartsData: [],
      // 表格数据
      tableData: [],
      tableData2: [],
      tableColumns: ASSET_TABLE,
      tableColumns2: ASSET2_TABLE,
      issearchButton: false,
      tableLoading: false,
      tableLoading2: false,
      chartLoading: false,
      chartLoading2: false,
      total: 0,
      dialogMask: false,
      searchRules: {
        ddate_: [{required: true, message: "请选择日期", trigger: "change"}],
        fundNames: [{required: true, message: "请选择产品", trigger: "change"}]
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
      timDate: "",
      /* 按钮禁止与否 */
      isDisabled: false,
      isDisabled2: false,
      // 导出图标
      downLoadIcon: "el-icon-download",
      // 导出提示文字
      downLoadText: "导出",
      downLoadText2: "导出",
      exportLoading: false,
      exportLoading2: false,

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
    },
    'formQuery.ZB_INDEXCODEA'() {
      this.below.benchmarkA = this.formQuery.ZB_INDEXCODEA
    },
    'formQuery.ZB_INDEXWEIGHTA'() {
      this.below.benchmarkAValue = this.formQuery.ZB_INDEXWEIGHTA
    },
    'formQuery.ZB_INDEXCODEB'() {
      this.below.benchmarkB = this.formQuery.ZB_INDEXCODEB
    },
    'formQuery.ZB_INDEXWEIGHTB'() {
      this.below.benchmarkBValue = this.formQuery.ZB_INDEXWEIGHTB
    },
  },
  mounted() {
    var self = this
    // self.getContrasOptions()
  },

  methods: {
    handleClick() {
      this.visible = !this.visible; // 切换下拉菜单的可见性
    },
    handleSelect(key, index) {
      if (key == 1) {
        this.downloadTableExcel()
      } else if (key == 2) {
        this.downloadTableExcel2()
      }
    },
    /**
     * @description 获取基准下拉
     */
    getContrasOptions() {
      return new Promise((resolve, reject) => {
        request({
          url: `/api/report/v1.0/data/sql/d43c924b-eebd-4d8f-97e5-ed46b609456d`,
          method: 'post',
          data: {
            indexCode: 'd43c924b-eebd-4d8f-97e5-ed46b609456d'
          }
        })
          .then(res => {
            if (res.data.status === 0) {
              const resultDim = res.data.data || []
              this.datumOption = resultDim.map(item => {
                return {
                  label: item.DIM_NME,
                  id: item.DIM_CDE
                }
              })
            }
            resolve()
          })
          .catch(err => {
            resolve()
          })
      })
    },
    // 权重校验
    handleInputWeight(type) {
      const regex = /^(0(\.\d+)?|[1-9]\d*(\.\d+)?)$/
      if (type == 'A') {
        if (!regex.test(this.formQuery.ZB_INDEXWEIGHTA)) {
          this.$message.closeAll()
          this.$message.warning('只能输入大于等于0的数')
          this.formInline.ZB_INDEXWEIGHTA = '0.0000'
          return
        }
        if (this.formQuery.ZB_INDEXWEIGHTB != '') {
          if (
            Number(this.formQuery.ZB_INDEXWEIGHTA) +
            Number(this.formQuery.ZB_INDEXWEIGHTB) >
            100
          ) {
            this.$message.closeAll()
            this.$message.warning('基金A、B权重不能超过100%')
            this.formQuery.ZB_INDEXWEIGHTA = '0'

          } else {
            this.formQuery.ZB_INDEXWEIGHTA = '' + Number(this.formQuery.ZB_INDEXWEIGHTA).toFixed(4)
          }
        }
      } else {
        if (!regex.test(this.formQuery.ZB_INDEXWEIGHTB)) {
          this.$message.closeAll()
          this.$message.warning('只能输入大于等于0的数')
          this.formQuery.ZB_INDEXWEIGHTB = '0.0000'
          return
        }
        if (this.formQuery.ZB_INDEXWEIGHTA != '') {
          if (
            Number(this.formQuery.ZB_INDEXWEIGHTA) +
            Number(this.formQuery.ZB_INDEXWEIGHTB) >
            100
          ) {
            this.$message.closeAll()
            this.$message.warning('基金A、B权重不能超过100')
            this.formQuery.ZB_INDEXWEIGHTB = '0'

          } else {
            this.formQuery.ZB_INDEXWEIGHTB = '' + Number(this.formQuery.ZB_INDEXWEIGHTB).toFixed(4)
          }
        }
      }
    }
    ,
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
      if (self.below.fundCodes.length > 0) {
        self.below.fundCode = self.below.fundCodes[0]
        for (var i = 0; i < self.below.fundCodes.length; i++) {
          self.optionsFund.push({value: self.below.fundCodes[i], label: self.below.fundNames[i]})
        }
      }
      if (self.formQuery.ZB_INDEXTYPE == 'djz') {
        self.formQuery.ZB_INDEXCODEB = ''
        self.formQuery.ZB_INDEXWEIGHTA = ''
        self.formQuery.ZB_INDEXWEIGHTB = ''
      }
      self.$refs[formName].validate((valid) => {
        if (valid) {
          self.onQuery();
          self.onQuery2();
          // 禁用搜索按钮
          self.$fun.searchButtonDisabled("issearchButton", self);
        } else {
          return false;
        }
      });
    },
    // 导出
    downloadTableExcel() {
      this.onQuery(true);
    },
    // 导出
    downloadTableExcel2() {
      this.onQuery2(true);
    },
    //确定
    onConfirm() {
      if (this.below.fundCode == "") {
        this.$message({
          message: '请先查询列表！',
          type: 'warning'
        });
        return
      }
      const params = Object.assign({}, this.below, {});
      params.beginDate = this.formQuery.ddate_[0];
      params.endDate = this.formQuery.ddate_[1];
      params.benchmarkA = this.formQuery.ZB_INDEXCODEA
      params.benchmarkB = this.formQuery.ZB_INDEXCODEB
      params.benchmarkAValue = this.formQuery.ZB_INDEXWEIGHTA
      params.benchmarkBValue = this.formQuery.ZB_INDEXWEIGHTB
      delete params.fundNames
      delete params.fundCodes
      this.chartLoading2 = true
      new Promise((resolve, reject) => {
        performEvalApi.fun_selectdoYieldAnalysisGraphChart(params).then((res) => {
          var configs = [{
            field: 'dayyield',
            name: '日收益率',
            type: 'bar'
          }, {
            field: 'accumulativeyield',
            name: '收益率'
          }, {
            field: 'accumulativebenchyield',
            name: '基准收益率'
          }];
          this.targetTrendOptions = this.lineTimeSeries(res.data, configs, '组合收益率分析', 'doYieldAnalysisGraph');
          this.chartLoading2 = false
        })
          .catch((error) => {
            this.chartLoading2 = false
            reject(error);
          });
      });
      this.chartLoading = true
      new Promise((resolve, reject) => {
        performEvalApi.fun_selectdoPerformAnalysis(params).then((res) => {
          var configs = [{
            field: 'alpha',
            name: 'Alpha'
          }, {
            field: 'beta',
            name: 'Beta'
          }];
          this.targetTrendOptions2 = this.lineTimeSeries(res.data, configs, '组合业绩分析', 'doPerformAnalysisGraph');
          this.chartLoading = false
        })
          .catch((error) => {
            this.chartLoading = false
            reject(error);
          });
      });
    },


    onQuery(flag) {
      var self = this;
      const params = Object.assign({}, this.formQuery, {});
      if (params.ddate_ && params.ddate_.length) {
        params.beginDate = params.ddate_[0];
        params.endDate = params.ddate_[1];
      }
      params.benchmarkA = this.formQuery.ZB_INDEXCODEA
      params.benchmarkB = this.formQuery.ZB_INDEXCODEB
      params.benchmarkAValue = this.formQuery.ZB_INDEXWEIGHTA
      params.benchmarkBValue = this.formQuery.ZB_INDEXWEIGHTB
      delete params.ddate_
      delete params.ZB_INDEXCODEA
      delete params.ZB_INDEXCODEB
      delete params.ZB_INDEXWEIGHTA
      delete params.ZB_INDEXWEIGHTB
      delete params.ZB_INDEXCODE
      delete params.ZB_INDEXTYPE
      if (flag) {
        self.downLoadText2 = "导出中...";
        self.exportLoading2 = true;
        self.isDisabled2 = true;
        params.ex_tmp_name = "组合收益率分析-导出.xlsx";
      }
      if (!flag) {
        this.tableLoading = true;
      }
      new Promise((resolve, reject) => {
        performEvalApi.fun_selectperformEval(params).then((res) => {
          const {status, data} = res;
          if (status === 0) {
            if (data != null && data != undefined) {
              if (!flag) {
                this.tableData = data.list
                self.onConfirm();
              }
              if (flag) {
                if (!data) return;
                this.$fun.commonDownloadUrl(data);
              }
            }
          } else {
            self.$message({
              message: "系统异常",
              type: "warning"
            });
          }
          this.tableLoading = false;
          self.exportLoading2 = false;
          self.downLoadText2 = "导出";
          self.isDisabled2 = false;
        })
          .catch((error) => {
            this.tableLoading = false;
            self.exportLoading2 = false;
            self.downLoadText2 = "导出";
            self.isDisabled2 = false;
            reject(error);
          });
      });
    },
    onQuery2(flag) {
      var self = this;
      const params = Object.assign({}, this.formQuery, {});
      if (params.ddate_ && params.ddate_.length) {
        params.beginDate = params.ddate_[0];
        params.endDate = params.ddate_[1];
      }
      params.benchmarkA = this.formQuery.ZB_INDEXCODEA
      params.benchmarkB = this.formQuery.ZB_INDEXCODEB
      params.benchmarkAValue = this.formQuery.ZB_INDEXWEIGHTA
      params.benchmarkBValue = this.formQuery.ZB_INDEXWEIGHTB
      delete params.ddate_
      delete params.ZB_INDEXCODEA
      delete params.ZB_INDEXCODEB
      delete params.ZB_INDEXWEIGHTA
      delete params.ZB_INDEXWEIGHTB
      delete params.ZB_INDEXCODE
      delete params.ZB_INDEXTYPE
      if (flag) {
        self.downLoadText2 = "导出中...";
        self.exportLoading2 = true;
        self.isDisabled2 = true;
        params.ex_tmp_name = "组合业绩分析-导出.xlsx";
      }
      if (!flag) {
        this.tableLoading2 = true;
      }
      new Promise((resolve, reject) => {
        performEvalApi.fun_selectperformEval2(params).then((res) => {
          const {status, data} = res;
          if (status === 0) {
            if (data != null && data != undefined) {
              if (!flag) {
                this.tableData2 = data.list
              }
              if (flag) {
                if (!data) return;
                this.$fun.commonDownloadUrl(data);
              }
            }
          } else {
            self.$message({
              message: "系统异常",
              type: "warning"
            });
          }
          this.tableLoading2 = false;
          self.exportLoading2 = false;
          self.downLoadText2 = "导出";
          self.isDisabled2 = false;
        })
          .catch((error) => {
            this.tableLoading2 = false;
            self.exportLoading2 = false;
            self.downLoadText2 = "导出";
            self.isDisabled2 = false;
            reject(error);
          });
      });
    },
    lineTimeSeries(data, configs, title, type) {
      var xAix = [];
      var preData;

      //console.log(data);

      preData = {};

      for (var i in configs) {
        preData[configs[i].field] = {
          name: configs[i].name,
          type: configs[i].type ? configs[i].type : 'line',
          barMaxWidth: '120px',
          dateData: {},
          data: []
        };
      }
      for (var i in data) {
        for (var j in preData) {
          preData[j].dateData[data[i].ddate] = Number(data[i][j]).toFixed(2);
        }

        if (xAix.indexOf(data[i].ddate) === -1) {
          xAix.push(data[i].ddate);
        }

      }

      xAix.sort();

      for (var i in xAix) {
        for (var j in preData) {
          if (preData[j].dateData[xAix[i]]) {
            preData[j].data.push(preData[j].dateData[xAix[i]]);
          } else {
            preData[j].data.push(0);
          }
        }
      }

      var series = [];
      var legend = [];
      for (var i in preData) {
        series.push(preData[i]);
        legend.push(preData[i].name);
      }

      var yAxisLabelFmt = '{value}%';
      if (type == 'doPerformAnalysisGraph') {
        yAxisLabelFmt = '{value}';
      }

      var option = {
        title: {
          text: title
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: legend
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          },
          right: 30
        },
        xAxis: {
          type: 'category',
          boundaryGap: true,
          data: xAix
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: yAxisLabelFmt
          }
        },
        series: series
      };

      return option;
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
      if (this.formQuery.fundCodes.length == 0 || this.formQuery.fundNames == "") {
        this.timDate = ""
        this.$message({
          message: '请先选择产品！',
          type: 'warning'
        });
        return
      }
      if (this.formQuery.fundCodes.length > 1) {
        this.timDate = ""
        this.$message({
          message: '请选择单个产品！',
          type: 'warning'
        });
        return
      }
      if (this.timDate == "" || this.timDate == undefined || this.timDate == null) {
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
.performEval {
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

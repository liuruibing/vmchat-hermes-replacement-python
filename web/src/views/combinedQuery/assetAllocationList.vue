<template>
  <!--资产配置-zhangzhiyong-@Author: zhangzhiyong @Date: 2023/10/9 14:22 -->
  <div class="assetAllocationList">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formQuery" :inline="true" :rules="searchRules" :model="formQuery" class="standard-form">
          <el-row>
            <el-form-item prop="fundNames">
              <span slot="label" class="item-label">产品</span>
              <el-tooltip class="item" effect="dark" :content="formQuery.fundNames" placement="top-start" :disabled="!formQuery.fundNames">
                <el-input v-model.trim="formQuery.fundNames" clearable placeholder="请输入" size="small" @click.native="openFundListDialog" @change="handleFundNamesChange" />
              </el-tooltip>
            </el-form-item>
            <el-form-item label="日期" prop="endDate">
              <el-date-picker v-model="formQuery.endDate" placeholder="选择日期" type="date" size="small" value-format="yyyy-MM-dd" />
            </el-form-item>
            <el-form-item class="">
              <el-button type="primary" size="small" icon="el-icon-search" @click="onSubmit('formQuery')">查询</el-button>
              <el-button type="info" size="small" icon="el-icon-refresh" plain @click="resetForm('formQuery')">重置</el-button>
              <el-button type="info" size="small" plain :icon="exportLoading ? 'el-icon-loading' : 'el-icon-download'" :disabled="isDisabled" @click="downloadTableExcel">
                {{ downLoadText }}
              </el-button>
            </el-form-item>
          </el-row>
        </el-form>
      </div>
    </div>
    <el-row>
      <el-col :span="16">
        <div class="page-model-title">
          <div class="title-icon">
            <div class="color-box"></div>
          </div>
          <span class="title-txt">资产配置</span>
        </div>
      </el-col>
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
        <vxe-table v-loading="tableLoading" :data="tableData" :cell-style="{ height: '50px' }" auto-resize sync-resize style="width: 100%" max-height="500" resizable>
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
                  col.prop == 'XIANJIN' ||
                  col.prop == 'STOCKVAL' ||
                  col.prop == 'BONDVAL' ||
                  col.prop == 'FUNDPRICE' ||
                  col.prop == 'LCPRICE' ||
                  col.prop == 'HGPRICE' ||
                  col.prop == 'QHPRICE'
                "
              >
                {{ scope.row[col.prop] | moneyYuan }}
              </span>
              <span
                v-else-if="
                  col.prop == 'XIANJINZB' ||
                  col.prop == 'STOCKRATIO' ||
                  col.prop == 'BONDRATIO' ||
                  col.prop == 'FUNDRATIO' ||
                  col.prop == 'LCRATIO' ||
                  col.prop == 'HGRATIO' ||
                  col.prop == 'QHRATIO'
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
            <el-select v-model="below.fundCode" size="small" placeholder="请选择">
              <el-option v-for="item in optionsFund" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item prop="assetsType" label="资产类型">
            <el-select v-model="below.assetsType" size="small" placeholder="请选择">
              <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item prop="typeDetail" label="行业分类">
            <el-select v-model="below.typeDetail" size="small" v-show="isVisible" placeholder="请选择">
              <el-option v-for="item in optionsType" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="small" icon="el-icon-search" @click="onConfirm()">确定</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <el-row v-if="type1">
      <el-col :span="12">
        <div class="chart-content">
          <myChart v-loading="charLoading" id="zcpzzzt" ref="zcpzzzt" :options="targetTrendOptions" class="echarts_box" resize-dom="cmbfof" />
        </div>
      </el-col>
      <el-col :span="12">
        <div class="chart-content">
          <myChart v-loading="charLoading" id="zcpzbzt" ref="zcpzbzt" :options="targetTrendOptionspie" class="echarts_box" resize-dom="cmbfof" />
        </div>
      </el-col>
    </el-row>
    <el-row v-if="type2">
      <el-col :span="24">
        <div class="chart-content">
          <myChart v-loading="charLoading" id="zzfb" ref="zzfb" :options="targetTrendOptions" class="echarts_box" resize-dom="cmbfof" />
        </div>
      </el-col>
    </el-row>
    <el-row v-if="type3">
      <el-col :span="24">
        <div class="chart-content">
          <myChart v-loading="charLoading" id="yspfb" ref="yspfb" :options="targetTrendOptions" class="echarts_box" resize-dom="cmbfof" />
        </div>
      </el-col>
    </el-row>
    <el-row v-if="type4">
      <el-col :span="24">
        <div class="chart-content">
          <myChart v-loading="charLoading" id="lczb" ref="lczb" :options="targetTrendOptions" class="echarts_box" resize-dom="cmbfof" />
        </div>
      </el-col>
    </el-row>
    <el-row v-if="type5">
      <el-col :span="12">
        <div class="chart-content">
          <myChart v-loading="charLoading" id="zcpz" ref="zcpz" :options="targetTrendOptions" class="echarts_box" resize-dom="cmbfof" />
        </div>
      </el-col>
      <el-col :span="12">
        <div class="chart-content">
          <myChart v-loading="charLoading" id="zcpzpie" ref="zcpzpie" :options="targetTrendOptionspie" class="echarts_box" resize-dom="cmbfof" />
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
import assetAllocationListApi from "@/api/combinedQuery/assetAllocationList";
import FundListDialogMultiphase from '@/components/FundListDialogMultiphase';
import moment from 'moment'
import { ASSET_TABLE } from './scripts/policy'
  import productSelector from '@/components/productSelector'

export default {
  name: "assetAllocationList",
  components: {
    myChart,
    Pagination,
    FundListDialogMultiphase,
    productSelector
  },
  data() {

    return {
      type1:false,
      type2:false,
      type3:false,
      type4:false,
      type5:false,
      // 搜索
      formQuery: {
        endDate: "",
        fundCodes: [],
        fundNames: "",
        offset: 0,
        limit: 99999
      },
      below:{
        assetsType:"GP",
        typeDetail:"SWSR",
        fundCode:'',
        time:'',
        fundCodes:[],
        fundNames:[]
      },
      isVisible:true,
      optionsFund:[],
      options: [{
        value: 'GP',
        label: '股票'
      }, {
        value: 'JJ',
        label: '基金'
      }, {
        value: 'ZQ',
        label: '债券'
      }, {
        value: 'YSP',
        label: '衍生品'
      }, {
        value: 'LC',
        label: '理财'
      }],
      optionsType: [{
        value: 'CSRC',
        label: '证监会行业分类'
      }, {
        value: 'ZXSR',
        label: '中信行业分类'
      }, {
        value: 'SWSR',
        label: '申万行业分类'
      }],
      //echarts
      targetTrendOptions: {},
      targetTrendOptionspie: {},
      // 所有数据
      Datas: [],
      echartsData: [],
      // 表格数据
      tableData: [],
      tableColumns: ASSET_TABLE,
      issearchButton: false,
      tableLoading: false,
      charLoading:false,
      total: 0,
      dialogMask: false,
      searchRules: {
        endDate: [{ required: true, message: "请选择日期", trigger: "change" }],
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
    'below.assetsType'(newValue) {
    if(newValue == 'GP'){
      this.isVisible = true
    }else {
      this.isVisible = false
    }

    },
    'formQuery.endDate'() {
     this.below.time = this.formQuery.endDate
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
    // 导出
    downloadTableExcel() {
      this.onQuery(true);
    },
    //确定
    onConfirm() {
      var self = this;
      const params = Object.assign({}, this.below, {});
      delete params.fundNames
      delete params.fundCodes
      this.charLoading = true
      new Promise((resolve, reject) => {
        assetAllocationListApi.fun_selectassetAllocationChart(params).then((res) => {
          if(res.type == '1'){
            this.type1 = true;
            this.type2 = false;
            this.type3 = false;
            this.type4 = false;
            this.type5 = false;
          this.targetTrendOptions = {
            title: {
              text: '资产配置柱状图',
              //subtext: '虚构数据',
              left: 'center'
            },
            color: ['#3398DB'],
            tooltip: {
              trigger: 'axis',
              axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
              }
            },
            grid: {
              // left: '3%',
              // right: '4%',
              bottom: '10%',
              containLabel: true
            },
            xAxis: [
              {
                type: 'category',
                data: res.groupName,
                axisTick: {
                  alignWithLabel: true
                },
                axisLabel: {     //加上这个强制显示
                  interval: 0,
                  rotate: -90
                }
              }
            ],
            yAxis: [
              {
                type: 'value',
                axisLabel: {
                  formatter: '{value}%'
                }
              }
            ],
            series: [
              {
                //name:'直接访问',
                type: 'bar',
                // barWidth: '60%',
                barMaxWidth: '120px',
                //data:[10, 52, 200, 334, 390, 330, 220]
                data: res.rate
              }
            ]
          }
          this.targetTrendOptionspie = {
            title: {
              text: '资产配置饼状图',
              //subtext: '虚构数据',
              left: 'center'
            },
            tooltip: {
              trigger: 'item',
              formatter: "{b} : {c} ({d}%)"
            },
            // legend: {
            //     // orient: 'vertical',
            //     // top: 'middle',
            //     // bottom: 50,
            //     bottom: 0,
            //     left: 'center',
            //     data: data.groupName
            // },
            animation: false,
            series: [
              {
                type: 'pie',
                label: {
                  formatter: "{b} : {c}%"
                },
                radius: '50%',
                center: ['50%', '50%'],
                selectedMode: 'single',
                data: res.pie,
                itemStyle: {
                  emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                  }
                }
              }
            ]
          }
          }
          if(res.type == '2') {
            this.type1 = false;
            this.type2 = true;
            this.type3 = false;
            this.type4 = false;
            this.type5 = false;
            this.targetTrendOptions = {
              title: {
                text: '债种分布',
                //subtext: '虚构数据',
                left: 'center'
              },
              tooltip: {
                trigger: 'item',
                formatter: "{b} : {c} ({d}%)"
              },
              legend: {
                // orient: 'vertical',
                // top: 'middle',
                bottom: 10,
                left: 'center',
                data: res.kindName
              },
              series: [
                {
                  type: 'pie',
                  label: {
                    formatter: "{b} : {c}%"
                  },
                  radius: '65%',
                  center: ['50%', '50%'],
                  selectedMode: 'single',
                  data: res.pv,
                  itemStyle: {
                    emphasis: {
                      shadowBlur: 10,
                      shadowOffsetX: 0,
                      shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                  }
                }
              ]
            }
          }
          if(res.type == '3') {
            this.type1 = false;
            this.type2 = false;
            this.type3 = true;
            this.type4 = false;
            this.type5 = false;
            this.targetTrendOptions = {
              title: {
                text: '衍生品分布',
                //subtext: '虚构数据',
                left: 'center'
              },
              legend: {
                data: ['金额'],
                top: '10%',

              },
              tooltip: {
                trigger: 'axis',
                axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                  type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                }
              },
              grid: {
                top: '20%',
                left: '3%',
                right: '4%',
                bottom: '0',
                containLabel: true
              },
              xAxis: [
                {
                  type: 'category',
                  data: res.qhRatio,
                }
              ],
              yAxis: [
                {
                  type: 'value',
                  name: '市值(元)',
                  nameLocation: 'middle',
                  nameGap: '80'
                }
              ],
              series: [
                {
                  //name:'直接访问',
                  type: 'bar',
                  barMaxWidth: '40',
                  //data:[10, 52, 200, 334, 390, 330, 220]
                  data: res.netValue
                }
              ]
            }
          }
          if(res.type == '4') {
            this.type1 = false;
            this.type2 = false;
            this.type3 = false;
            this.type4 = true;
            this.type5 = false;
            this.targetTrendOptions = {
              title: {
                text: '理财占比',
                //subtext: '虚构数据',
                left: 'center'
              },
              tooltip: {
                trigger: 'item',
                formatter: "{b} : {c} ({d}%)"
              },
              legend: {
                // orient: 'vertical',
                // top: 'middle',
                bottom: 10,
                left: 'center',
                data: res.kindName
              },
              series: [
                {
                  type: 'pie',
                  label: {
                    formatter: "{b} : {c}%"
                  },
                  radius: '65%',
                  center: ['50%', '50%'],
                  selectedMode: 'single',
                  data: res.pv,
                  itemStyle: {
                    emphasis: {
                      shadowBlur: 10,
                      shadowOffsetX: 0,
                      shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                  }
                }
              ]
            }
          }
          if(res.type == '5'){
            this.type1 = false;
            this.type2 = false;
            this.type3 = false;
            this.type4 = false;
            this.type5 = true;
            this.targetTrendOptions = {
              title: {
                text: '资产配置柱状图',
                //subtext: '虚构数据',
                left: 'center'
              },
              color: ['#3398DB'],
              tooltip: {
                trigger: 'axis',
                axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                  type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                }
              },
              grid: {
                // left: '3%',
                // right: '4%',
                bottom: '10%',
                containLabel: true
              },
              xAxis: [
                {
                  type: 'category',
                  data: res.groupName,
                  axisTick: {
                    alignWithLabel: true
                  },
                  axisLabel: {     //加上这个强制显示
                    interval: 0,
                    rotate: -90
                  }
                }
              ],
              yAxis: [
                {
                  type: 'value',
                  axisLabel: {
                    formatter: '{value}%'
                  }
                }
              ],
              series: [
                {
                  //name:'直接访问',
                  type: 'bar',
                  // barWidth: '60%',
                  barMaxWidth: '120px',
                  //data:[10, 52, 200, 334, 390, 330, 220]
                  data: res.rate
                }
              ]
            }
            this.targetTrendOptionspie = {
              title: {
                text: '资产配置饼状图',
                //subtext: '虚构数据',
                left: 'center'
              },
              tooltip: {
                trigger: 'item',
                formatter: "{b} : {c} ({d}%)"
              },
              // legend: {
              //     // orient: 'vertical',
              //     // top: 'middle',
              //     // bottom: 50,
              //     bottom: 0,
              //     left: 'center',
              //     data: data.groupName
              // },
              animation: false,
              series: [
                {
                  type: 'pie',
                  label: {
                    formatter: "{b} : {c}%"
                  },
                  radius: '50%',
                  center: ['50%', '50%'],
                  selectedMode: 'single',
                  data: res.pie,
                  itemStyle: {
                    emphasis: {
                      shadowBlur: 10,
                      shadowOffsetX: 0,
                      shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                  }
                }
              ]
            }
          }
          this.charLoading = false
        })
          .catch((error) => {
            this.charLoading = false
            reject(error);
          });
      });

    },


    onQuery(flag) {
      var self = this;
      const params = Object.assign({}, this.formQuery, {});
      if (flag) {
        self.downLoadText = "导出中...";
        self.exportLoading = true;
        self.isDisabled = true;
        params.ex_tmp_name = "资产配置-导出.xlsx";
      }
      if (!flag) {
        this.tableLoading = true;
      }
      new Promise((resolve, reject) => {
        assetAllocationListApi.fun_selectassetAllocationList(params).then((res) => {
            const { status, data } = res;
            if (status === 0) {
              if (data != null && data != undefined) {
                if(!flag){
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
            self.exportLoading = false;
            self.isDisabled = false;
            self.downLoadText = "导出";
          })
          .catch((error) => {
            this.tableLoading = false;
            self.exportLoading = false;
            self.isDisabled = false;
            self.downLoadText = "导出";
            reject(error);
          });
      });
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
.assetAllocationList {
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

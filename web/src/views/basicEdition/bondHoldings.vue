<template>
  <!-- 持仓查询 -->
  <div class="bondHoldings">
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
              <el-form-item prop="fundType">
                <span slot="label" class="item-label">债券类型</span>
                <el-select v-model="formQuery.fundType" clearable placeholder="请选择" size="small">
                  <template v-for="(item, index) in fundTypeList">
                    <el-option :key="item.dimcde" :label="item.dimnme" :value="item.dimcde" />
                  </template>
                </el-select>
              </el-form-item>
              <el-form-item prop="bondCrdit">
                <span slot="label" class="item-label">债券信用级别</span>
                <el-select v-model="formQuery.bondCrdit" clearable placeholder="请选择" size="small">
                  <template v-for="(item, index) in bondCrditList">
                    <el-option :key="item.dimcde" :label="item.dimnme" :value="item.dimcde" />
                  </template>
                </el-select>
              </el-form-item>
              <el-form-item prop="levelIssuer">
                <span slot="label" class="item-label">发债主体信用级别</span>
                <el-select v-model="formQuery.levelIssuer" clearable size="small" placeholder="请选择">
                  <template v-for="(item, index) in levelIssuerList">
                    <el-option :key="item.dimcde" :label="item.dimnme" :value="item.dimcde" />
                  </template>
                </el-select>
              </el-form-item>
              <el-form-item prop="industryName">
                <span slot="label" class="item-label">行业</span>
                <el-select v-model="formQuery.industryName" clearable size="small" placeholder="请选择">
                  <template v-for="(item, index) in industryNameList">
                    <el-option :key="item.dimcde" :label="item.dimnme" :value="item.dimcde" />
                  </template>
                </el-select>
              </el-form-item>
              <el-form-item prop="issuerName">
                <span slot="label" class="item-label">发行人名称</span>
                <el-input class="fxrmc" v-model.trim="formQuery.issuerName" clearable placeholder="请输入" size="small" />
              </el-form-item>
              <el-form-item prop="bondsymBol">
                <span slot="label" class="item-label">债券代码</span>
                <el-input v-model.trim="formQuery.bondsymBol" clearable placeholder="请输入" size="small" />
              </el-form-item>
              <el-form-item prop="bondName">
                <span slot="label" class="item-label">债券名称</span>
                <el-input v-model.trim="formQuery.bondName" clearable placeholder="请输入" size="small" />
              </el-form-item>
              <el-form-item class="">
                <el-button type="primary" size="small" icon="el-icon-search" @click="onSubmit('formQuery')">查询</el-button>
                <el-button type="info" icon="el-icon-refresh" size="small" plain @click="resetForm('formQuery')">重置</el-button>
                <el-button type="info" size="small" plain :icon="exportLoading ? 'el-icon-loading' : 'el-icon-download'" :disabled="isDisabled" @click="downloadTableExcel">
                  {{ downLoadText }}
                </el-button>
              </el-form-item>
            </el-col>
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
          <span class="title-txt">债券持仓查询</span>
        </div>
      </el-col>
      <el-col :span="8">
        <div style="float: right">
          <vxe-toolbar ref="tableToolbar" class="standard-vxe-toolbar" :custom="{ immediate: true }" custom />
        </div>
      </el-col>
    </el-row>

    <el-row>
      <el-col>
        <!--<vxe-table
          border
          highlight-hover-row
          resizable
          show-overflow
          auto-resize
          id="toolbar_table1"
          ref="table1"
          :loading="tableLoading"
          :data="tableData"
          row-id="id"
          :header-cell-style="this.$fun.headerRowStyle"
          :cell-style="this.$fun.cellStyle"
          :tree-config="{children: 'children', trigger: 'row',expandAll: true}"
        >-->
        <div id="standard-table">
          <div id="standard-table-margin">
            <vxe-table
              ref="table1"
              :sort-config="{ remote: true }"
              :loading="tableLoading"
              :custom-config="{ storage: true }"
              :data="tableData"
              :cell-style="{ height: '50px' }"
              show-header-overflow
              auto-resize
              show-overflow
              stripe
              @sort-change="handleSortChange"
              resizable
            >
              <vxe-table-column field="fundCode" title="产品代码" min-width="150" header-align="center" align="left" />
              <vxe-table-column field="fundName" title="产品名称" min-width="250" header-align="center" align="center" />
              <vxe-table-column field="newDate" title="日期" min-width="100" header-align="center" align="center" sortable />
              <vxe-table-column field="fundType" title="债券类型" min-width="120" header-align="center" align="center" />
              <!--          <vxe-table-column field="interestRate" title="资产类型" min-width="120" header-align="center" align="center"/>-->
              <vxe-table-column field="market" title="交易市场" min-width="120" header-align="center" align="center" />
              <vxe-table-column field="bondsymBol" title="债券代码" min-width="250" header-align="center" align="center" />
              <vxe-table-column field="bondName" title="债券名称" min-width="250" header-align="center" align="center" />
              <vxe-table-column field="bondCrdit" title="债券信用级别" min-width="120" header-align="center" align="center" />
              <vxe-table-column field="issuerName" title="发行人名称" min-width="120" header-align="center" align="center" />
              <vxe-table-column field="levelIssuer" title="发债主体信用级别" min-width="120" header-align="center" align="center" />
              <vxe-table-column field="industryName" title="行业" min-width="120" header-align="center" align="center" />
              <vxe-table-column field="amount" title="数量" min-width="120" header-align="center" sortable align="right">
                <template slot-scope="scope">
                  <span>{{ scope.row.amount | moneyYuan }}</span>
                </template>
              </vxe-table-column>
              <vxe-table-column field="unitCost" title="单位成本(元)" min-width="150" header-align="center" sortable align="right">
                <template slot-scope="scope">
                  <span>{{ scope.row.unitCost | moneyYuan }}</span>
                </template>
              </vxe-table-column>
              <vxe-table-column field="fCost" title="成本(元)" min-width="120" header-align="center" align="right">
                <template slot-scope="scope">
                  <span>{{ scope.row.fCost | moneyYuan }}</span>
                </template>
              </vxe-table-column>
              <vxe-table-column field="costRatio" title="成本占净值比%" min-width="120" header-align="center" align="right">
                <template slot-scope="scope">
                  <span>{{ scope.row.costRatio | baifenlvS }}</span>
                </template>
              </vxe-table-column>
              <vxe-table-column field="balance" title="余额(元)" min-width="200" header-align="center" sortable align="right">
                <template slot-scope="scope">
                  <span>{{ scope.row.balance | moneyYuan }}</span>
                </template>
              </vxe-table-column>
              <vxe-table-column field="price" title="市价(元)" min-width="120" header-align="center" sortable align="right">
                <template slot-scope="scope">
                  <span>{{ scope.row.price | moneyYuan }}</span>
                </template>
              </vxe-table-column>
              <vxe-table-column field="priceValue" title="市值(元)" min-width="120" header-align="center" sortable align="right">
                <template slot-scope="scope">
                  <span>{{ scope.row.priceValue | moneyYuan }}</span>
                </template>
              </vxe-table-column>
              <vxe-table-column field="priceRatio" title="市值占净值比%" min-width="120" header-align="center" align="right">
                <template slot-scope="scope">
                  <span>{{ scope.row.priceRatio | baifenlvS }}</span>
                </template>
              </vxe-table-column>
              <vxe-table-column field="residual" title="剩余期限(年)" min-width="150" header-align="center" align="right">
                <template slot-scope="scope">
                  <span>{{ scope.row.residual | numberTwoPoint }}</span>
                </template>
              </vxe-table-column>
              <vxe-table-column field="fixedDuration" title="修正久期(年)" min-width="150" header-align="center" align="right">
                <template slot-scope="scope">
                  <span>{{ scope.row.fixedDuration | numberTwoPoint }}</span>
                </template>
              </vxe-table-column>
              <vxe-table-column field="areas" title="主体地区" min-width="150" header-align="center" align="right">
                <!--<template slot-scope="scope">
              <span>{{scope.row.duration | numberTwoPoint}}</span>
            </template>-->
              </vxe-table-column>
              <vxe-table-column field="debtVal" title="中债估值(全价)" min-width="150" header-align="center" align="right">
                <!--  <template slot-scope="scope">
              <span>{{scope.row.duration2 | numberTwoPoint}}</span>
            </template>-->
              </vxe-table-column>
            </vxe-table>
            <Pagination :total="total" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination" />
          </div>
        </div>

        <!-- <vxe-pager
        border
        size="medium"
        :current-page="formQuery.pageNum"
        :page-size="formQuery.pageSize"
        :total="total"
        :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
        @page-change="pagination">
        </vxe-pager>-->
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
            :tagsinfo="tags"
            @getTemplateRow="getTemplateRow"
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
import $ from "jquery";
import { FILE_URL } from "@/utils/request";
import { getToken } from "@/utils/auth";
import Pagination from "@/components/Pagination";
import fun from "@/filters/common";
import commonApi from "@/api/common";
import bondHoldingsApi from "@/api/basicEdition/bondHoldings";
import FundListDialogMultiphase from '@/components/FundListDialogMultiphase';
import { downLoadFileByUrl } from "@/utils";
import moment from 'moment'
import productSelector from '@/components/productSelector'
export default {
  name: "BondHoldings",
  components: {
    Pagination,
    FundListDialogMultiphase,
    productSelector
  },
  data() {
    return {
      // 搜索
      formQuery: {
        date: [],
        ddate_: [],
        // 持仓日期
        thisDate: "",
        beginDate: "",
        endDate: "",
        // 产品代码
        fundCodes: [],
        fundNames: "",
        // 债券类型
        fundType: "",
        // 资产大类
        // policyType: [],
        // 债券信用级别
        bondCrdit: "",
        subPolicyType: "",
        // 发行主体信用级别
        levelIssuer: "",
        // 行业
        industryName: "",
        // 发行人名称
        issuerName: "",
        // 债券代码
        bondsymBol: "",
        // 债券名称
        bondName: "",

        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10,
        orderString: ""
        // 排序方式
        /*  orderBy: '"price" desc ',*/
      },
      // 债券类型下拉框
      fundTypeList: [],
      // 资产大类下拉框
      // propertyTypeList: [],
      // 债券信用级别下拉框
      bondCrditList: [],
      // 发行主体信用级别下拉框
      levelIssuerList: [],
      // 行业下拉框
      industryNameList: [],
      // 表格数据
      tableData: [],
      issearchButton: false,
      tableLoading: false,
      total: 0,
      columnWidth: "120",
      dialogMask: false,

      searchRules: {
        // endDate: [{ required: true,message: "请输入指标统计日期", trigger: "change" }],
        // thisDate: [{ required: true, message: '请输入持仓日期', trigger: 'change' }],
        fundNames: [{ required: true, message: "请选择产品", trigger: "change" }],
        ddate_: [{ required: true, message: "请选择日期", trigger: "change" }]
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
  watch: {},
  mounted() {
    const self = this;
    if (self.$route.query.endDate) {
      self.formQuery.endDate = self.$route.query.endDate;
    } else {
      this.formQuery.endDate = this.$store.state.setting.bussinessTwoEndDate;
    }
    if (self.$route.query.symBolCode) {
      self.formQuery.symBol = self.$route.query.symBolCode;
    }
    if (self.$route.query.fundType) {
      self.formQuery.fundType.push(self.$route.query.fundType);
    }

    // 默认查询
    this.$nextTick(() => {
      this.$refs.table1.connect(this.$refs.tableToolbar);
      // 债券类型
      this.getTypeListEdims("BONDINNERTYPE");
      // 债券信用级别
      this.getBondCrditListEdims("gradelevel");
      // 发债主体信用级别
      this.getLevelIssuerListEdims("gradelevel");
      // 行业
      this.getIndustryNameListEdims("ZXSR");

      // this.getManagerList();
    });
  },
  // activated() {
  //   if(this.$store.getters.formQueryFundNames !== '') {
  //     this.formQuery.fundNames = this.$store.getters.formQueryFundNames
  //   }
  //   // if(this.$store.getters.formQueryBeginDate !== '') {
  //   //   this.formQuery.beginDate = this.$store.getters.formQueryBeginDate
  //   // }
  //   if(this.$store.getters.formQueryEndDate !== '') {
  //     this.formQuery.thisDate = this.$store.getters.formQueryEndDate
  //   }
  // },
  methods: {
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
        arr.forEach(function (item, index) {
          index++;
          if (index < arr.length) {
            self.formQuery.fundNames = self.formQuery.fundNames + item.fundName + ",";
          } else {
            self.formQuery.fundNames = self.formQuery.fundNames + item.fundName;
          }
          self.timDate = item.createDate;
          self.formQuery.fundCodes.push(item.fundCode);
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
        arr.forEach(function (item, index) {
          index++;
          if (index < arr.length) {
            self.formQuery.fundNames = self.formQuery.fundNames + item.VC_FUNDNAME + ",";
          } else {
            self.formQuery.fundNames = self.formQuery.fundNames + item.VC_FUNDNAME;
          }
          self.timDate = item.D_CREATE_DATE;
          self.formQuery.fundCodes.push(item.VC_FUNDCODE);

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
      self.formQuery.pageNum = 1;
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
    onQuery(flag) {
      var self = this;
      const params = Object.assign({}, this.formQuery, {});
      if (params.ddate_ && params.ddate_.length) {
        params.beginDate = params.ddate_[0];
        params.endDate = params.ddate_[1];
      }
      let fileName="";
       if(params.fundCodes.length==1) {
        fileName=params.fundCodes[0]+"_"+params.fundNames+"_" +
         params.beginDate.replace(/\-/g,"")+"-"+
         params.endDate.replace(/\-/g,"")+"_债券持仓查询.xlsx";
       }else{
         fileName= params.beginDate.replace(/\-/g,"")+"-"+
                   params.endDate.replace(/\-/g,"")+"_债券持仓查询.xlsx";
       }

      delete params.ddate_;
      if (flag) {
        self.downLoadText = "导出中...";
        self.exportLoading = true;
        self.isDisabled = true;
        params.pageNum = 1;
        params.pageSize = 999999;
        params.ex_tmp_name = "债券持仓查询-导出.xlsx";
      }

      if (!flag) {
        this.tableLoading = true;
      }
      new Promise((resolve, reject) => {
        bondHoldingsApi
          .fun_selectBondHoldings(params)
          .then((res) => {
            const { status, data } = res;
            if (status === 0) {
              if (data != null && data != undefined) {
                if (!flag) {
                  const { list, total } = data;

                  this.tableData = list;
                  // 不分页
                  // this.tableData = data;
                  this.total = total;
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
    // 债券类型
    getTypeListEdims(type) {
      // 字典类型
      const params = type;
      bondHoldingsApi.fun_selectByfundTypeEdims(params).then((res) => {
        const { status, data } = res.data;
        if (status === 0) {
          // 产品类型
          if (type === "BONDINNERTYPE") {
            this.fundTypeList = data;
          }
        }
      });
    },
    // 债券信用级别
    getBondCrditListEdims(type) {
      // 字典类型
      const params = type;
      bondHoldingsApi.fun_selectBybondCrditEdims(params).then((res) => {
        const { status, data } = res.data;
        if (status === 0) {
          // 产品类型
          if (type === "gradelevel") {
            this.bondCrditList = data;
          }
        }
      });
    },
    // 发债主体信用级别
    getLevelIssuerListEdims(type) {
      // 字典类型
      const params = type;
      bondHoldingsApi.fun_selectBylevelIssuerEdims(params).then((res) => {
        const { status, data } = res.data;
        if (status === 0) {
          // 产品类型
          if (type === "gradelevel") {
            this.levelIssuerList = data;
          }
        }
      });
    },
    // 行业
    getIndustryNameListEdims(type) {
      // 字典类型
      const params = type;
      bondHoldingsApi.fun_selectByindustryNameEdims(params).then((res) => {
        const { status, data } = res.data;
        if (status === 0) {
          // 产品类型
          if (type === "ZXSR") {
            this.industryNameList = data;
          }
        }
      });
    },
    // 资产大类
    /* getBondHoldingsEdims() {
       // 字典类型
       //let params = type;
       bondHoldingsApi.fun_selectBondHoldingsEdims().then(res => {
         let {status, data} = res.data;
         this.propertyTypeList = data[0];
         if (status === 0) {
           // 产品类型
         /!*  if (type === "VC_BONDTYPE2") {
             this.propertyTypeList = data;
           }*!/
         }
       });
     },*/
    // 导出
    downloadTableExcel() {
      this.onQuery(true);
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
    async getStandard() {
      if(this.formQuery.fundCodes.length == 0 || this.formQuery.fundNames ==""){
        this.timDate =""
        this.$message({
          message: '请先选择产品！',
          type: 'warning',
          customClass: "message-warning"
        });
        return
      }
      if(this.formQuery.fundCodes.length > 1){
        this.timDate =""
        this.$message({
          message: '请选择单个产品！',
          type: 'warning',
          customClass: "message-warning"
        });
        return
      }
      if(this.timDate == "" || this.timDate == undefined || this.timDate == null){
        this.$message({
          message: '未获取到成立日！',
          type: 'warning',
          customClass: "message-warning"
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
    // 分页点击事件
    pagination(val) {
      const { page, limit } = val;
      // 起始页
      this.formQuery.pageNum = page;
      // 每页数量
      this.formQuery.pageSize = limit;
      // 查询
      this.onQuery();
    },
    // 当表格的排序条件发生变化的时候会触发该事件
    handleSortChange(val) {
      if (val.property == "amount") {
        val.property = "k.f_amount";
      } else if (val.property == "priceValue") {
        val.property = "k.f_price";
      } else if (val.property == "price") {
        val.property = "k.f_szprice";
      } else if (val.property == "unitCost") {
        val.property = "k.f_unitprice";
      } else if (val.property == "marketVal") {
        val.property = "k.f_price";
      }
      this.formQuery.orderString = this.$fun.queryOrderBy_vxe(val);
      // 查询
      this.onQuery();
    }
  }
};
</script>

<style lang="scss">
.bondHoldings {
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
  .color-box {
    display: inline-block;
    height: 30px;
    width: 2px;
    background-color: #e03d3e;
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

    .mr5 {
      margin-right: 5px;
    }
  }
}
</style>

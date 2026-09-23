<template>
  <!-- 个股持仓查询 -->
  <div class="stockPosition">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formQuery" :inline="true" :rules="searchRules" class="standard-form" :model="formQuery">
          <el-row>
            <el-col :span="24">
              <el-form-item prop="fundNames">
                <span slot="label" class="item-label">产品</span>
                <el-tooltip class="item" effect="dark" :content="formQuery.fundNames" placement="top-start" :disabled="!formQuery.fundNames">
                  <el-input v-model.trim="formQuery.fundNames" clearable placeholder="请输入" size="small" @click.native="openFundListDialog" @change="handleFundNamesChange" />
                </el-tooltip>
              </el-form-item>
              <el-form-item prop="ddate_" label="日期">
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
              <el-form-item label="" prop="industry">
                <span slot="label" class="item-label">行业</span>
                <el-select class="hy" v-model="formQuery.industry" clearable size="small" placeholder="请选择">
                  <template v-for="(item, index) in industryList">
                    <el-option :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                  </template>
                </el-select>
              </el-form-item>
              <el-form-item label="" prop="growth">
                <span slot="label" class="item-label">成长属性</span>
                <el-select v-model="formQuery.growth" clearable size="small" placeholder="请选择">
                  <template v-for="(item, index) in growthList">
                    <el-option :key="item.dimCde" :label="item.dimNme" :value="item.dimNme" />
                  </template>
                </el-select>
              </el-form-item>
              <el-form-item label="" prop="suspension">
                <span slot="label" class="item-label">停牌信息</span>
                <el-select v-model="formQuery.suspension" clearable size="small" placeholder="请选择">
                  <template v-for="(item, index) in suspensionList">
                    <el-option :key="item.dimCde" :label="item.dimNme" :value="item.dimNme" />
                  </template>
                </el-select>
              </el-form-item>
              <el-form-item label="" prop="plate">
                <span slot="label" class="item-label">板块</span>
                <el-select v-model="formQuery.plate" clearable size="small" placeholder="请选择">
                  <template v-for="(item, index) in plateList">
                    <el-option :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                  </template>
                </el-select>
              </el-form-item>
              <el-form-item label="" prop="scale">
                <span slot="label" class="item-label">规模</span>
                <el-select v-model="formQuery.scale" clearable size="small" placeholder="请选择">
                  <template v-for="(item, index) in scaleList">
                    <el-option :key="item.dimCde" :label="item.dimNme" :value="item.dimNme" />
                  </template>
                </el-select>
              </el-form-item>
              <el-form-item prop="stockCode">
                <span slot="label" class="item-label">股票代码</span>
                <el-input v-model.trim="formQuery.stockCode" clearable placeholder="请输入" size="small" />
              </el-form-item>
              <el-form-item prop="stockName">
                <span slot="label" class="item-label">股票名称</span>
                <el-input v-model.trim="formQuery.stockName" clearable placeholder="请输入" size="small" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" size="small" icon="el-icon-search" @click="onSubmit('formQuery')">查询</el-button>
                <el-button type="info" size="small" plain icon="el-icon-refresh" @click="resetForm('formQuery')">重置</el-button>
                <el-button
                  type="info"
                  size="small"
                  plain
                  :icon="exportLoading ? 'el-icon-loading' : 'el-icon-download'"
                  :disabled="isDisabled"
                  @click="downloadTableExcel('formQuery')"
                >
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
          <span class="title-txt">个股持仓查询</span>
        </div>
      </el-col>
      <el-col :span="8">
        <div style="float: right">
          <vxe-toolbar ref="tableToolbar" class="standard-vxe-toolbar" :custom="{ immediate: true }" custom />
        </div>
      </el-col>
    </el-row>
    <el-row id="standard-table">
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
          <vxe-table-column type="seq" title="序号" width="60" header-align="center" />
          <vxe-table-column field="fundcode" title="产品代码" min-width="120" header-align="center" align="center" />
          <vxe-table-column field="fundname" title="产品名称" min-width="250" header-align="center" align="center" />
          <vxe-table-column field="thisdate" title="日期" min-width="100" header-align="center" align="center" sortable />
          <vxe-table-column field="industry" title="行业" min-width="100" header-align="center" align="center" />
          <vxe-table-column field="stockcode" title="股票代码" min-width="100" header-align="center" align="center" />
          <vxe-table-column field="stockname" title="股票名称" min-width="120" sortable header-align="center" align="center" />
          <vxe-table-column field="plate" title="板块" min-width="120" sortable header-align="center" align="center" />
          <vxe-table-column field="scale" title="规模" min-width="120" sortable header-align="center" align="center" />
          <vxe-table-column field="growth" title="成长属性" min-width="120" sortable header-align="center" align="center" />
          <vxe-table-column field="suspension" title="停牌信息" min-width="120" sortable header-align="center" align="center" />
          <vxe-table-column field="amount" title="数量" min-width="120" header-align="center" sortable align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.amount | moneyYuan }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="unitcost" title="单位成本(元)" min-width="150" header-align="center" sortable align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.unitcost | moneyYuan }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="f_cost" title="成本(元)" min-width="120" header-align="center" sortable align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.f_cost | moneyYuan }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="costratio" title="成本占净值比" min-width="150" header-align="center" sortable align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.costratio | baifenlv2 }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="price" title="市价(元)" min-width="120" sortable header-align="center" align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.price | moneyYuan }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="pricevalue" title="市值(元)" min-width="120" sortable header-align="center" align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.pricevalue | moneyYuan }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="priceratio" title="市值占净值比" min-width="150" header-align="center" sortable align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.priceratio | baifenlv2 }}</span>
            </template>
          </vxe-table-column>
        </vxe-table>
        <vxe-pager
          :current-page="formQuery.pageNum"
          :page-size="formQuery.pageSize"
          :total="total"
          class="standard-vxe-pager"
          :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
          border
          size="medium"
          @page-change="pagination"
        />
      </div>
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
import stockPositionApi from "@/api/basicEdition/stockPosition";
import FundListDialogMultiphase from '@/components/FundListDialogMultiphase';
import moment from 'moment'
import productSelector from '@/components/productSelector'
export default {
  name: "StockPosition",
  components: {
    Pagination,
    FundListDialogMultiphase,
    productSelector
  },
  data() {
    const validatebeginDate = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请选择开始日期"));
      } else {
        if (this.formQuery.endDate !== null || this.formQuery.endDate !== undefined || this.formQuery.endDate !== "") {
          const startTime = new Date(value);
          const endTime = new Date(this.formQuery.endDate);
          if (startTime > endTime) {
            callback(new Error("开始日期不能大于结束日期"));
          } else {
            callback();
          }
        } else {
          callback();
        }
      }
    };
    const validateEndDate = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请选择结束日期"));
      } else {
        if (
          this.formQuery.beginDate !== null ||
          this.formQuery.beginDate !== undefined ||
          this.formQuery.beginDate !== ""
        ) {
          const startTime = new Date(this.formQuery.beginDate);
          const endTime = new Date(value);
          if (startTime > endTime) {
            callback(new Error("结束日期不能小于开始日期"));
          } else {
            callback();
          }
        } else {
          callback();
        }
      }
    };
    return {
      // 搜索
      formQuery: {
        ddate_: [],
        beginDate: "",
        endDate: "",
        fundCodes: [],
        fundNames: "",
        // 行业
        industry: "",
        // 板块
        plate: "",
        // 规模
        scale: "",
        // 成长属性
        growth: "",
        // 停牌信息
        suspension: "",
        // 个券代码
        stockCode: "",
        // 个券名称
        stockName: "",
        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10,
        // 排序方式
        orderString: ""
      },
      tags: [],
      // 表格数据
      tableData: [],
      formLabelWidth: "120px",
      // 行业
      industryList: [],
      // 板块
      plateList: [],
      // 规模
      scaleList: [],
      // 成长属性
      growthList: [],
      // 停牌信息
      suspensionList: [],
      issearchButton: false,

      tableLoading: false,
      total: 0,

      dialogMask: false,

      searchRules: {
        ddate_: [{ required: true, message: "请选择日期", trigger: "change" }],
        // beginDate: [
        //   { required: true, message: '请选择开始日期', trigger: 'change' },
        //   { validator: validatebeginDate, trigger: 'change' }
        // ],
        // endDate: [
        //   { required: true, message: '请选择结束日期', trigger: 'change' },
        //   { validator: validateEndDate, trigger: 'change' }
        // ],
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
      exportIcon: "el-icon-download"
    };
  },
  watch: {},
  mounted() {
    this.$refs.table1.connect(this.$refs.tableToolbar);
    // 获取行业
    this.getListEdimss("ZXSR");
    // 获取板块
    this.getListEdims("STOCKINNERTYPE");
    // 获取规模
    this.getListEdims("MAX_PRICE");
    // 成长属性
    this.getListEdims("fund_size");
    // 停牌信息
    this.getListEdims("stop_status");
    // 默认显示个框架
    // self.onSubmit("formQuery");
  },
  // activated() {
  //   if(this.$store.getters.formQueryFundNames !== '') {
  //     this.formQuery.fundNames = this.$store.getters.formQueryFundNames
  //   }
  //   if(this.$store.getters.formQueryBeginDate !== '') {
  //     this.formQuery.beginDate = this.$store.getters.formQueryBeginDate
  //   }
  //   if(this.$store.getters.formQueryEndDate !== '') {
  //     this.formQuery.endDate = this.$store.getters.formQueryEndDate
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
          // this.$store.commit('SET_FUNDNAMES',this.formQuery.fundNames)
          // this.$store.commit('SET_BEGINDATE',this.formQuery.beginDate)
          // this.$store.commit('SET_ENDDATE',this.formQuery.endDate)
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
         params.endDate.replace(/\-/g,"")+"_个股持仓查询.xlsx";
       }else{
         fileName= params.beginDate.replace(/\-/g,"")+"-"+
                   params.endDate.replace(/\-/g,"")+"_个股持仓查询.xlsx";
       }
      delete params.ddate_;
      if (flag) {
        self.downLoadText = "导出中...";
        self.exportLoading = true;
        self.isDisabled = true;
        params.pageNum = 1;
        params.pageSize = 999999;
        params.ex_tmp_name = "个股持仓查询-导出.xlsx";

      }

      if (!flag) {
        this.tableLoading = true;
      }
      new Promise((resolve, reject) => {
        stockPositionApi
          .fun_selectStockPosition(params)
          .then((res) => {
            const { status, data } = res;
            if (status === 0) {
              if (data != null && data != undefined) {
                if (!flag) {
                  const { list, total } = data;
                  this.tableData = list;
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

    getListEdimss(type) {
      // 字典类型
      const params = type;
      stockPositionApi.edimsCommon(params).then((res) => {
        const { status, data } = res.data;

        if (status === 0) {
          // 行业
          if (type === "ZXSR") {
            this.industryList = data;
          }
        }
      });
    },
    getListEdims(type) {
      // 字典类型
      const params = type;
      commonApi.edimsDdiaCommon(params).then((res) => {
        const { status, data } = res.data;
        if (status === 0) {
          // 板块
          if (type === "STOCKINNERTYPE") {
            this.plateList = data;
          } else if (type === "MAX_PRICE") {
            this.scaleList = data;
          } else if (type === "fund_size") {
            this.growthList = data;
          } else if (type === "stop_status") {
            this.suspensionList = data;
          }
        }
      });
    },
    // 导出
    downloadTableExcel(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.onQuery(true);
        } else {
        }
      });
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
      // let { page, limit } = val;
      const { currentPage, pageSize } = val;
      // 起始页
      this.formQuery.pageNum = currentPage;
      // 每页数量
      this.formQuery.pageSize = pageSize;
      // 查询
      this.onQuery();
    },
    // 当表格的排序条件发生变化的时候会触发该事件
    handleSortChange(val) {
      if (val.property == "stockName") {
        val.property = "k.VC_NAME";
      } else if (val.property == "plate") {
        val.property = "e.dim_nme";
      } else if (val.property == "scale") {
        val.property = "k.scaletype";
      } else if (val.property == "growth") {
        val.property = "k.cztype";
      } else if (val.property == "suspension") {
        val.property = "k.status";
      } else if (val.property == "amount") {
        val.property = "k.F_AMOUNT";
      }
      this.formQuery.orderString = this.$fun.queryOrderBy_vxe(val);
      // 查询
      this.onQuery();
    }
  }
};
</script>

<style lang="scss">
.stockPosition {
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
  .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
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
  .el-checkbox-button--medium .el-checkbox-button__inner {
    font-size: 16px;
  }
  ::v-deep .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
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

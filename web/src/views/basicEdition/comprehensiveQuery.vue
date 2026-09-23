<template>
  <!--
  综合查询 -->
  <div class="comprehensiveQuery analyse-page">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formQuery" :inline="true" :rules="searchRules" :model="formQuery" class="standard-form">
          <el-row>
            <el-form-item prop="fundNames">
              <el-tooltip effect="dark" :content="formQuery.fundNames" placement="top-start" :disabled="!formQuery.fundNames">
                <el-input v-model.trim="formQuery.fundNames" clearable placeholder="请选择产品" size="small" @click.native="openFundListDialog" @change="handleFundNamesChange" />
              </el-tooltip>
            </el-form-item>

            <el-form-item label="" prop="fundType">
              <el-select v-model="formQuery.fundType" clearable size="small" placeholder="请选择资产大类">
                <template v-for="(item, index) in fundTypeList">
                  <el-option :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </template>
              </el-select>
            </el-form-item>
            <el-form-item prop="symBolCode">
              <el-input v-model.trim="formQuery.symBolCode" clearable placeholder="请输入个券代码" size="small" />
            </el-form-item>
            <el-form-item prop="symBolName">
              <el-input v-model.trim="formQuery.symBolName" clearable placeholder="请输入个券名称" size="small" />
            </el-form-item>
            <el-form-item prop="ddate_" label="" class="mb20">
              <el-date-picker
                v-model="formQuery.ddate_"
                type="daterange"
                value-format="yyyy-MM-dd"
                align="left"
                size="small"
                unlink-panels
                range-separator="至"
                start-placeholder="请选择开始日期"
                end-placeholder="请选择结束日期"
                popper-class="popperDateShortTP"
                :picker-options="dateShortTPCTA()"
              ></el-date-picker>
            </el-form-item>
            <el-form-item>
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
          <span class="title-txt">综合持仓查询</span>
        </div>
      </el-col>
      <el-col :span="8">
<!--        <div style="float: right">
          <vxe-toolbar class="standard-vxe-toolbar" ref="tableToolbar" :custom="{ immediate: true }" custom />
        </div>-->
      </el-col>
    </el-row>
    <el-row id="standard-table">
      <div id="standard-table-margin">
        <vxe-table
          ref="table1"
          :sort-config="{ remote: true }"
          :loading="tableLoading"
          :custom-config="{ storage: true }"
          :height="tableHeight"
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
          <vxe-table-column field="FUNDCODE" title="产品代码" min-width="120" header-align="center" align="center" />
          <vxe-table-column field="FUNDNAME" title="产品名称" min-width="250" header-align="center" align="center" />
          <vxe-table-column field="THISDATE" title="日期" sortable min-width="100" header-align="center" align="center" />
          <vxe-table-column field="ASSET" title="资产大类" min-width="100" header-align="center" align="center" />
          <vxe-table-column field="SYMBOLCODE" title="个券代码" min-width="100" header-align="center" align="center" />
          <vxe-table-column field="SYMBOLNAME" title="个券名称" min-width="120" sortable header-align="center" align="center" />
          <vxe-table-column field="AMOUNT" title="数量" min-width="120" header-align="center" sortable align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.AMOUNT | moneyYuan }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="UNITCOST" title="单位成本(元)" min-width="150" header-align="center" sortable align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.UNITCOST | moneyYuan }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="F_COST" title="成本(元)" min-width="120" header-align="center" sortable align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.F_COST | moneyYuan }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="COSTRATIO" title="成本占净值比" min-width="150" header-align="center" align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.COSTRATIO | baifenlv2 }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="MARKETPRICE" title="市价(元)" min-width="120" header-align="center" align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.MARKETPRICE | moneyYuan }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="MARKETVAL" title="市值(元)" min-width="120" sortable header-align="center" align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.MARKETVAL | moneyYuan }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="MARKETRATIO" title="市值占净值比" min-width="120" header-align="center" align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.MARKETRATIO | baifenlv2 }}</span>
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
import $ from "jquery";
import { FILE_URL } from "@/utils/request";
import { getToken } from "@/utils/auth";
import Pagination from "@/components/Pagination";
import fun from "@/filters/common";
import commonApi from "@/api/common";
import comprehensiveQueryApi from "@/api/basicEdition/comprehensiveQuery";
import FundListDialogMultiphase from '@/components/FundListDialogMultiphase'
import moment from 'moment'
import productSelector from '@/components/productSelector'
import store from '../../store'
export default {
  name: "ComprehensiveQuery",
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
        // 产品类型
        fundType: [],
        // 个券代码
        symBolCode: "",
        // 个券名称
        symbolName: "",
        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10,
        // 排序方式
        orderString: ""
      },
      // 表格高度
      tableHeight: 0,
      // 表格数据
      tableData: [],
      formLabelWidth: "120px",
      // 资产大类
      fundTypeList: [],
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
      showTreeKeyArray: ['产品列表','我的关注'],
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
    var self = this
    var baseTime = store.state.edims.baseTime
    if(baseTime){
      self.formQuery.ddate_ = [baseTime.beginDate, baseTime.endDate]
      self.formQuery.beginDate = baseTime.beginDate
      self.formQuery.endDate = baseTime.endDate
    }
    this.handleTableHeight();
    if (self.$route.query.endDate) {
      self.formQuery.endDate = self.$route.query.endDate;
    } else if (this.$store.state.setting.bussinessTwoEndDate) {
      this.formQuery.endDate = this.$store.state.setting.bussinessTwoEndDate;
    }
    if (self.$route.query.symBolCode) {
      self.formQuery.symBol = self.$route.query.symBolCode;
    }
    if (self.$route.query.fundType) {
      self.formQuery.fundType.push(self.$route.query.fundType);
    }
    this.$refs.table1.connect(this.$refs.tableToolbar);
    // 获取资产大类
    this.getListEdims("SECTYPE");
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
    inputMouserIn(){

    },
    /**
     * @description 动态设置表格高度
     */
    handleTableHeight() {
      this.$nextTick(() => {
        // 根据浏览器高度设置初始高度
        this.tableHeight = window.innerHeight - this.$refs.table1.$el.offsetTop - 325
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.table1.$el.offsetTop - 325
        }
      })
    },
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
         params.endDate.replace(/\-/g,"")+"_综合持仓查询.xlsx";
       }else{
         fileName= params.beginDate.replace(/\-/g,"")+"-"+
                   params.endDate.replace(/\-/g,"")+"_综合持仓查询.xlsx";
       }
      delete params.ddate_;
      if (flag) {
        self.downLoadText = "导出中...";
        self.exportLoading = true;
        self.isDisabled = true;
        params.pageNum = 1;
        params.pageSize = 999999;
        params.ex_tmp_name = "综合持仓查询-导出.xlsx";
      }

      if (!flag) {
        this.tableLoading = true;
      }
      new Promise((resolve, reject) => {
        comprehensiveQueryApi
          .fun_selectComprehensivePosition(params)
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

    getListEdims(type) {
      // 字典类型
      const params = type;
      commonApi.edimsDdiaCommon(params).then((res) => {
        const { status, data } = res.data;

        if (status === 0) {
          // 产品类型
          if (type === "SECTYPE") {
            this.fundTypeList = data;
          }
        }
      });
    },
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
      if (val.property == "SYMBOLNAME") {
        val.property = "k.vc_name";
      } else if (val.property == "AMOUNT") {
        val.property = "k.f_amount";
      } else if (val.property == "F_COST") {
        val.property = "k.f_cost";
      } else if (val.property == "UNITCOST") {
        val.property = "k.F_DWCB";
      } else if (val.property == "MARKETVAL") {
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
.comprehensiveQuery {
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

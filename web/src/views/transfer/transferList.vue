<template>
  <div>
    <el-tabs @tab-click="handleClick">
      <el-tab-pane label="待办"> </el-tab-pane>
      <el-tab-pane label="已办"> </el-tab-pane>
    </el-tabs>
    <!-- el-form -->
    <div class="toolbar">
      <el-form
        :inline="true"
        ref="formInline"
        :model="formInline"
        class="demo-form-inline form_inline_search"
        @submit.native.prevent
      >
        <el-row>
          <el-col :span="20">
            <div class="grid-content bg-purple">
              <el-form-item label="产品" prop="productInfo">
                <select-table v-model="formInline.productInfo" @enter='onSubmit()'></select-table>
              </el-form-item>
              <el-form-item label="指令编号" prop="pfomBizNum">
                <el-input v-model="formInline.pfomBizNum" maxlength="30" clearable @keydown.enter.native="onSubmit()"></el-input>
              </el-form-item>

              <el-form-item label="发起时间" prop="beginDate">
                <el-date-picker
                  v-model="formInline.beginDate"
                  type="date"
                  value-format="yyyy-MM-dd"
                  size="small"
                  placeholder="选择日期"
                >
                </el-date-picker>
              </el-form-item>

              <el-form-item label="要求划款日期" prop="date">
                <el-date-picker
                  v-model="formInline.date"
                  type="date"
                  value-format="yyyy-MM-dd"
                  size="small"
                  placeholder="选择日期"
                >
                </el-date-picker>
              </el-form-item>

              <el-form-item label="划款状态" prop="transferStatus">
                <el-select
                  :disabled="transferStatus_able"
                  clearable
                  v-model="formInline.transferStatus"
                  placeholder="划款状态"
                  size="small"
                >
                  <el-option
                    v-for="item in transferStatuses"
                    :key="item.code"
                    :label="item.name"
                    :value="item.code"
                  >
                  </el-option>
                </el-select>
              </el-form-item>
            </div>
          </el-col>
          <el-col :span="4">
            <div class="grid-content bg-purple-light">
              <el-form-item class="search_button_com">
                <el-button
                  type="primary"
                  @click="onSubmit()"
                  style="margin-bottom: 5px"
                  :disabled="investmentSearch1"
                  size="small"
                  ><i class="el-icon-search"></i>查询</el-button
                >
                <el-button
                  type="primary"
                  plain
                  @click="resetForm('formInline')"
                  style="margin-bottom: 5px"
                  size="small"
                  ><i class="el-icon-delete"></i>重置</el-button
                >
                <el-button
                  v-btn="'transfer.bizBegin.info'"
                  type="primary"
                  v-if="tabLabel === '待办'"
                  plain
                  @click="send()"
                  style="margin-bottom: 5px"
                  size="small"
                  ><i class="el-icon-plus"></i>流程发起</el-button
                >
              </el-form-item>
            </div>
          </el-col>
        </el-row>
      </el-form>
    </div>
    <!-- el-table -->
    <el-table
      :data="myData.datas"
      ref="table"
      stripe
      border
      style="width: 100%"
      id="transferTable"
      :height="tableHeight"
      v-loading="investLoading"
      @sort-change="trackingAgentComDataChangeSort"
      :default-sort="{ prop: 'dMettingdate', order: 'descending' }"
    >
      <el-table-column
        prop="fundCode"
        label="产品代码"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        min-width="150"
        header-align="left"
        align="left"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fundCode | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fundName"
        label="产品名称"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        min-width="150"
        header-align="left"
        align="left"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fundName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="cmdCode"
        label="划款类型"
        min-width="120"
        sortable="custom"
        :show-overflow-tooltip="true"
        :sort-orders="['ascending', 'descending']"
        header-align="left"
      >
        <template slot-scope="scope">
          <span>{{ dataStatus(scope.row.cmdCode, "2") | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="transferAmount"
        label="划款金额（元）"
        min-width="130"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        :show-overflow-tooltip="true"
        header-align="left"
        align="left"
      >
        <template slot-scope="scope">
          <span>{{
            amountFilter(scope.row.transferAmount) | noDataFilter | moneyYuan
          }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="transferReqdate"
        label="要求划款日期"
        min-width="130"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        :show-overflow-tooltip="true"
        header-align="left"
        align="left"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.transferReqdate | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="cmdStatus"
        label="指令状态"
        min-width="150"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        :show-overflow-tooltip="true"
        header-align="left"
        align="left"
      >
        <template slot-scope="scope">
          <span>{{ dataStatus(scope.row.cmdStatus, "0") | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="procStatus"
        label="划款状态"
        min-width="150"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        :show-overflow-tooltip="true"
        header-align="left"
        align="left"
      >
        <template slot-scope="scope">
          <span>{{
            dataStatus(scope.row.procStatus, "1") | noDataFilter
          }}</span>
        </template>
      </el-table-column>

      <el-table-column
        v-if="tabLabel === '待办'"
        prop="creatorName"
        label="发起人"
        min-width="150"
        :show-overflow-tooltip="true"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        header-align="left"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.creatorName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="beginTime"
        label="发起时间"
        min-width="150"
        :show-overflow-tooltip="true"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        header-align="left"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.beginTime | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="pfomBizNum"
        label="指令编号"
        min-width="130"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        header-align="left"
        :show-overflow-tooltip="true"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.pfomBizNum | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="payerAccount"
        label="付款账号"
        min-width="110"
        :show-overflow-tooltip="true"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        header-align="left"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.payerAccount | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="payeeAccount"
        label="收款账号"
        min-width="110"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        header-align="left"
        :show-overflow-tooltip="true"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.payeeAccount | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column label="操作" min-width="150" fixed="right" align="center">
        <template slot-scope="scope">
          <el-button
            type="primary"
            size="small"
            @click="serachDetail(scope.row, false)"
            >查看详情</el-button
          >
          <!-- v-btn="'transfer.update.info'" -->
          <el-button
            plain
            v-if="tabLabel === '待办'"
            type="danger"
            size="small"
            @click="serachDetail(scope.row, true)"
            >处理</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <div style="width: 100%; height: 20px">
      <Pagination
        :total="total"
        :page="pageNumber"
        :limit="pageSize"
        @pagination="Pagination"
      ></Pagination>
    </div>
    <!-- el-drawer -->
    <el-drawer
      :visible.sync="dialogVisible"
      :size="dialogSize"
      :title="dialogTitle"
      :direction="direction"
      :before-close="handleClose"
    >
      <el-row style="width: 100%">
        <el-col
          v-if="isShowYd"
          :span="10"
          style="border-right: 1px dashed #409eff; height: 700px"
        >
          <div class="forms_table_title">
            <i class="el-icon-s-data" />交互指引
          </div>

          <div id="handle_div" v-show="!isHaveData"></div>
          <div v-show="isHaveData">暂无数据</div>
        </el-col>
        <el-col :span="isShowYd ? 14 : 24">
          <!-- 指令经办 span class="el-drawer_myspan" >{{dialogTitle}}</span> -->
          <div lazy v-show="cmdOptPage_show" id="cmdOptPage_div" width="100%">
            <cmdOptPage
              :pageData="pageData"
              v-if="cmdOptPage_show"
              @drawerClick="drawerClick"
            >
            </cmdOptPage>
          </div>

          <!-- 指令复核 -->
          <div
            lazy
            v-show="cmdCheckPage_show"
            id="cmdCheckPage_div"
            width="100%"
          >
            <cmdCheckPage
              :pageData="pageData"
              v-if="cmdCheckPage_show"
              @drawerClick="drawerClick"
            >
            </cmdCheckPage>
          </div>

          <!-- 管理人复核 -->
          <div
            lazy
            v-show="managerCheckPage_show"
            id="managerCheckPage_div"
            width="100%"
          >
            <managerCheckPage
              :pageData="pageData"
              v-if="managerCheckPage_show"
              @drawerClick="drawerClick"
            >
            </managerCheckPage>
          </div>

          <!-- 管理人审批 -->
          <div
            lazy
            v-show="managerApprovePage_show"
            id="managerApprovePage"
            width="100%"
          >
            <managerApprovePage
              :pageData="pageData"
              v-if="managerApprovePage_show"
              @drawerClick="drawerClick"
            >
            </managerApprovePage>
          </div>

          <!-- 划款结果确认-->
          <div lazy v-show="bizEndPage_show" id="bizEndPage" width="100%">
            <bizEndPage
              :pageData="pageData"
              v-if="bizEndPage_show"
              @drawerClick="drawerClick"
            >
            </bizEndPage>
          </div>
        </el-col>
      </el-row>

      <span slot="footer" class="dialog-footer">
        <el-button plain size="small" @click="closeDialog()">取消</el-button>
      </span>

      <el-drawer
        title="流程图"
        :append-to-body="true"
        direction="ltr"
        size="65%"
        style="overflow-x: auto"
        :visible.sync="leftDrawer"
      >
        <bpmPage v-if="bpmPage_show" :id="definedId"></bpmPage>
      </el-drawer>
    </el-drawer>
    <el-dialog
      title="流程发起"
      customClass="transferListWidth"
      :before-close="dialogClose"
      center
      :visible.sync="countDialog"
      :close-on-click-modal="false"
      :modal-append-to-body="false"
    >
      <bizBeginPage
        v-if="bizBeginPage_show"
        @transferCheckClick="transferCheckClick"
      >
      </bizBeginPage>
    </el-dialog>
    <!-- drawer组件 -->
    <open-drawer
      v-if="openDrawerShow"
      ref="openDrawerRelation"
      @rightDrawer="onSubmit()"
      :cmdStatus='cmdStatus_'
      @closedD="openDrawerShow=false"
    ></open-drawer>
  </div>
</template>

<script>
import selectTable from '@/views/commonComponents/selectTable.vue';
import Pagination from "@/components/Pagination";
import commonApi from "@/api/common";
import commonFun from "@/filters/new_common";
import fun from "@/filters/common";
import hint from "@/components/hint";
import $ from "jquery";
import trackingAgentApi from "@/api/transfer/trackingAgentList";
import cmdCheckPage from "./cmdCheck.vue";
import cmdOptPage from "./cmdOpt.vue";
import managerCheckPage from "./managerCheck.vue";
import managerApprovePage from "./managerApprove.vue";
import bizEndPage from "./bizEnd.vue";
import bizBeginPage from "./bizBegin.vue";
import bpmPage from "./bpm/testBpm.vue";
import tableMethod from '@/utils/tableHeight'
// 引进drawer组件
import OpenDrawer from "./elDrawer/rightDrawer";

export default {
  name: "trackingAgentBase",
  inject: ["reload"],
  components: {
    Pagination,
    hint,
    cmdCheckPage,
    cmdOptPage,
    managerCheckPage,
    managerApprovePage,
    bizEndPage,
    bizBeginPage,
    bpmPage,
    OpenDrawer,
    selectTable
  },
  data(data) {
    return {
      tableHeight:0,
      cmdStatus_:'',
      openDrawerShow: false,
      formInline: {
        pfomBizNum: '', //指令编号
        productInfo: "", //产品信息
        date: "", //要求划款日期
        transferStatus: "", //划款状态
        accountType: "", //付款方账户类型
        procStatusArr: [],
        beginDate:'', //发起时间
      },
      productInfos: [], //产品下拉框
      transferStatuses: [], //划款状态数组
      myData: { datas: [] }, //列表数据
      orderByString: "", //排序字段
      total: 0, //总条数
      pageSize: 50, //条数
      pageNumber: 1, //页码
      offset: 0,
      investmentSearch1: false, //查询按钮禁用
      dialogVisible: false, //抽屉控制
      direction: "rtl", //抽屉展开方向
      cmdOptPage_show: false, //指令经办页面是否展示
      cmdCheckPage_show: false, //指令复核页面是否展示
      managerCheckPage_show: false, //管理人审批页面是否展示
      managerApprovePage_show: false, //管理人复核页面是否展示
      bizEndPage_show: false, //划款确认页面是否展示
      transferStatus_able: false, //划款状态下拉是否禁用
      cx_btn: true, //按钮禁用
      investLoading: false, //列表加载
      fileList: [], //附件列表
      resultData: [], //获取的数据
      resultPath: "", //跳转页面
      dialogTitle: "流程详情", //dialog标题
      cmdStatusArr: {}, //划款流程
      procStatusArr: {}, //划款状态
      cmdCodeArr: {}, //划款类型
      isSubmit: false, //是否点击查询
      submitData: {}, //查询搜索数据
      tabLabel: "待办",
      bizBeginPage_show: false,
      countDialog: false,
      leftDrawer: false,
      definedId: "",
      bpmPage_show: false,
      dialogSize: "50%",
      isShowYd: false,
      handleHtmlParams: {
        processKey: "",
        taskKey: "",
      },
      isHaveData: true,
      pageData: {
        pauseCode: "transfer.update.Pause",
        unPauseCode: "transfer.update.UnPause",
        abandonCode: "transfer.update.Abandon",
        cancleCode: "transfer.update.Cancle",
        normalCode: "transfer.update.Normal",
        retireCode: "transfer.update.Retire",
      },
    };
  },
  created(){
    tableMethod.fetTableHeight(this,'transferTable');
  },
  activated(){
    let self = this;
    this.fetTableHeight();
    window.addEventListener("resize",self.fetTableHeight,false);
  },
  deactivated(){
    let self = this;
    window.removeEventListener("resize",self.fetTableHeight,false);
  },
  beforeDestroy(){
    let self = this;
    window.removeEventListener("resize",self.fetTableHeight,false);
  },
  mounted() {
    //初始化数据字典
    this.initHandle();

    //查询产品信息
    // this.getProductInfo();

    //查询所有信息
    this.selectAll("");
    // let that = this;
    // window.addEventListener("popstate", function(e) {
    //   console.log('popstate-浏览器回退');
    //     that.countDialog = false;

    // }, false);
  },
  methods: {
    // 列表自适应高度
    fetTableHeight(){
      tableMethod.fetTableHeight(this,'transferTable');
    },
    //判断当前是何种流程
    isInvest(taskxmlId) {
      return taskxmlId.indexOf("Invest") > -1;
    },
    //查询
    onSubmit() {
      this.investLoading = true;
      this.isSubmit = true;
      this.pageNumber = 1;
      this.offset = (this.pageNumber - 1) * this.pageSize;
      let data = this.formInline;
      this.submitData.productInfo = data.productInfo;
      this.submitData.date = data.date;
      this.submitData.transferStatus = data.transferStatus;
      this.submitData.procStatusArr = data.procStatusArr;
      this.submitData.pfomBizNum = data.pfomBizNum;
      this.submitData.beginDate = data.beginDate;
      let label = this.tabLabel;
      if (label === "待办") {
        this.selectAll("");
      } else {
        this.getTrasnferDealtList("");
      }
    },
    // 清除
    resetForm(formName) {
      var self = this;
      self.$refs[formName].resetFields();
    },
    //列表排序
    trackingAgentComDataChangeSort(val) {
      var self = this;
      self.orderByString = self.$fun.orderByString(val);
      let label = this.tabLabel;
      if (label === "待办") {
        this.selectAll("");
      } else {
        this.getTrasnferDealtList("");
      }
    },
    //分页
    Pagination(val) {
      let self = this;
      self.pageSize = val.limit;
      self.pageNumber = val.page;
      self.offset = (self.pageNumber - 1) * self.pageSize;

      let label = this.tabLabel;
      if (label === "待办") {
        self.selectAll("2");
      } else {
        this.getTrasnferDealtList("2");
      }
    },
    //查询所有信息
    selectAll(flag) {
      let data = this.formInline;
      let data2 = this.submitData;
      let isSubmit = this.isSubmit;
      if (isSubmit) {
        data = data2;
      }
      let fundCode = data.productInfo;
      if (fundCode) {
        fundCode = fundCode.split("_")[0];
      }

      let transferReqdate = data.date;

      let procStatus = data.transferStatus;
      let procStatusArr = data.procStatusArr;
      let orderByString = this.orderByString;

      if (!fundCode) {
        fundCode = "";
      }
      if (!transferReqdate) {
        transferReqdate = "";
      }
      if (!procStatus) {
        procStatus = "";
      }

      if (this.tabLabel === "待办") {
        if (procStatus === "0") {
          procStatusArr = ["transApproving", "transOperating", "cmdSuspend"];
        } else {
          procStatusArr = [];
        }
      } else if (this.tabLabel === "已办") {
        if (procStatus === "0") {
          procStatusArr = ["transSuccess", "cmdCancel", "cmdInvalid"];
        } else {
          procStatusArr = [];
        }
      }
      let self = this;
      self.investLoading = true;
      // let pfomBizNum = this.formInline.pfomBizNum || ''
      let obj = {
         fundCode: fundCode,
         transferReqdate: transferReqdate,
         procStatus: procStatus,
         orderString: orderByString,
         limit: this.pageSize,
         offset: this.offset,
         procStatusArr: procStatusArr,
         procStatus: this.formInline.transferStatus || '',
         pfomBizNum: this.formInline.pfomBizNum || '',
         beginDate: this.formInline.beginDate || '',
      }
      trackingAgentApi
        .getTransferList( obj )
        .then((res) => {
          if (res.data.status === 200) {
            this.myData.datas = res.data.data.rows;
            let len = res.data.data.rows.length;
            //初始化date
            for (let i = 0; i < len; i++) {
              if (this.myData.datas[i].transferReqdate) {
                this.myData.datas[i].transferReqdate = fun.yyr_timestampToTime(
                  this.myData.datas[i].transferReqdate
                );
              }
            }
            this.pageSize = res.data.data.limit;
            self.total = res.data.data.total;
          } else {
            self.pageSize = 50;
            self.pageNumber = 1;
            self.total = 0;
            self.myData.datas = null;
            this.resetForm("formInline");
            this.$message.closeAll();
            this.$message.error("查询列表信息失败");
          }
          self.investLoading = false;
        })
        .catch(() => {
          this.$message.closeAll();
          this.$message.error("查询列表信息失败");
          self.investLoading = false;
        });
    },
    //查询所有信息
    getTrasnferDealtList(flag) {
      let data = this.formInline;
      let data2 = this.submitData;
      let isSubmit = this.isSubmit;
      if (isSubmit) {
        data = data2;
      }
      let fundCode = data.productInfo;
      if (fundCode) {
        fundCode = fundCode.split("_")[0];
      }

      let transferReqdate = data.date;

      let procStatus = data.transferStatus;
      let procStatusArr = data.procStatusArr;
      let orderByString = this.orderByString;

      if (!fundCode) {
        fundCode = "";
      }
      if (!transferReqdate) {
        transferReqdate = "";
      }
      if (!procStatus) {
        procStatus = "";
      }

      if (this.tabLabel === "待办") {
        if (procStatus === "0") {
          procStatusArr = ["transApproving", "transOperating", "cmdSuspend"];
        } else {
          procStatusArr = [];
        }
      } else if (this.tabLabel === "已办") {
        if (procStatus === "0") {
          procStatusArr = ["transSuccess", "cmdCancel", "cmdInvalid"];
        } else {
          procStatusArr = [];
        }
      }
      let self = this;
      self.investLoading = true;
      let obj = {
        fundCode: fundCode,
        transferReqdate: transferReqdate,
        orderString: orderByString,
        limit: this.pageSize,
        offset: this.offset,
        procStatusArr: procStatusArr,
        procStatus: this.formInline.transferStatus || '',
        pfomBizNum: this.formInline.pfomBizNum || '',
        beginDate: this.formInline.beginDate || '',
      }
      trackingAgentApi
        .getTrasnferDealtList( obj )
        .then((res) => {
          if (res.data.status === 200) {
            this.myData.datas = res.data.data.rows;
            let len = res.data.data.rows.length;
            //初始化date
            for (let i = 0; i < len; i++) {
              if (this.myData.datas[i].transferReqdate) {
                this.myData.datas[i].transferReqdate = fun.yyr_timestampToTime(
                  this.myData.datas[i].transferReqdate
                );
              }
            }
            this.pageSize = res.data.data.limit;
            self.total = res.data.data.total;
          } else {
            self.pageSize = 50;
            self.pageNumber = 1;
            self.total = 0;
            self.myData.datas = null;
            this.resetForm("formInline");
            this.$message.closeAll();
            this.$message.error("查询列表信息失败");
          }
          self.investLoading = false;
        })
        .catch(() => {
          this.$message.closeAll();
          this.$message.error("查询列表信息失败");
          self.investLoading = false;
        });
    },
    //查询产品信息
    getProductInfo() {
      trackingAgentApi
        .getProductInfo()
        .then((res) => {
          if (res.data.message === "success") {
            let arr = res.data.data;
            this.productInfos = [];
            for (let i = 0; i < arr.length; i++) {
              let obj = {};
              obj.value = arr[i].fundCode + "_" + arr[i].fundName;
              obj.name = arr[i].fundName + " (" + arr[i].fundCode + ")";
              this.productInfos.push(obj);
            }
          } else {
            this.productInfos = [];
            this.$message.closeAll();
            this.$message.error("查询产品信息失败");
          }
        })
        .catch(() => {
          this.$message.closeAll();
          this.$message.error("查询产品信息失败");
        });
    },
    //查看详情
    serachDetail(val, show_flag) {
      this.cmdStatus_=val.cmdStatus;
      // console.log(val.cmdStatus,'cmdstatus');
      localStorage.setItem("resultData", "");
      localStorage.setItem("trackingAgent_taskId", "");
      localStorage.setItem("show_flag", show_flag);
      // this.getResultData(val);  //老写法
      this.openDrawer(val, show_flag);
    },
    openDrawer(data, flag) {
      let rowInfo = { ...data, isCheck: flag };
      this.openDrawerShow = true;
      this.$nextTick(() => {
        this.$refs.openDrawerRelation.init(rowInfo);
      });
    },
    //关闭dialog
    handleClose(done) {
      done();
      // this.reload();
      this.cmdOptPage_show = false;
      this.cmdCheckPage_show = false;
      this.managerCheckPage_show = false;
      this.managerApprovePage_show = false;
      this.bizEndPage_show = false;
    },
    leftClose() {
      done();
      this.bpmPage_show = false;
    },
    dialogClose(done) {
      done();
      // this.reload();

      this.bizBeginPage_show = false;
    },
    send() {
      this.countDialog = true;
      this.bizBeginPage_show = true;
    },
    //tab切换
    handleClick(tab, event) {
      this.$nextTick(()=>{
        this.$refs.table.doLayout();
      })
      let tabs = tab;
      this.resetForm("formInline");
      this.isSubmit = false;
      this.pageNumber = 1;
      this.tabLabel = tab.label;

      if (tab.label === "待办") {
        //this.transferStatus_able = false;
        let arr2 = [
          { name: "划款审批中", code: "transApproving" },
          { name: "托管划款中", code: "transOperating" },
          { name: "指令暂缓", code: "cmdSuspend" },
        ];
        this.transferStatuses = arr2;
        this.formInline.transferStatus = "";
        this.formInline.procStatusArr = [
          "transApproving",
          "transOperating",
          "cmdSuspend",
        ];
        this.selectAll("0");
      } else {
        //初始化划款状态
        let arr2 = [
          { name: "划款审批中", code: "transApproving" },
          { name: "托管划款中", code: "transOperating" },
          { name: "划款成功", code: "transSuccess" },
          { name: "划款失败", code: "transFailed" },
          { name: "指令暂缓", code: "cmdSuspend" },
          { name: "指令撤销", code: "cmdCancel" },
          { name: "指令作废", code: "cmdInvalid" },
        ];
        //初始化划款状态
        this.transferStatuses = arr2;
        //this.transferStatus_able = true;
        this.formInline.transferStatus = "";
        this.formInline.procStatusArr = [
          "transSuccess",
          "cmdCancel",
          "cmdInvalid",
        ];
        this.getTrasnferDealtList("1");
      }
    },
    //获取dialog数据
    getResultData(vals) {
      let taskId = vals.pfomTaskid;
      let taskXmlId = vals.pfomTaskXmlid;
      this.handleHtmlParams.taskKey = vals.pfomTaskXmlid;
      this.handleHtmlParams.processKey = vals.cmdType;
      this.isShowYd = false;
      this.dialogSize = "50%";
      let drawerSpan = $("#el-drawer__title span");
      drawerSpan.html("");
      drawerSpan[0].setAttribute(
        "title",
        "" + vals.fundName + "-" + this.dataStatus(vals.procStatus, "1")
      );
      drawerSpan.append("<span>流程详情 (" + vals.fundName + "-</span>");
      drawerSpan.append(
        "<span style='color:red'>" +
          this.dataStatus(vals.procStatus, "1") +
          "</span>"
      );
      drawerSpan.append("<span>)</span>");

      trackingAgentApi
        .getResultDatas(taskId)
        .then((res) => {
          let datas = res.data.data;
          if (datas) {
            let resultDatas = res.data;
            this.resultPath = resultDatas.data.formPath;
            this.resultData = resultDatas;
            this.resultData.procStatus = vals.procStatus;
            this.resultData.cmdStatus = vals.cmdStatus;
            this.resultData.definedId = vals.procDefineid;
            localStorage.setItem("trackingAgent_taskId", taskId);

            let relaId = vals.id;
            let relaType = "transfer_file";
            //debugger;
            if (this.isInvest(taskXmlId)) {
              relaType = "invest_file";
            }
            let fileId = datas.formData.fileId;
            if (fileId && fileId !== "" && fileId !== null) {
              relaType = "invest_file";
            }
            this.getFileList(relaId, relaType);
          } else {
            this.$message.closeAll();
            this.$message.error("查询详情信息失败");
          }
        })
        .catch(() => {
          this.$message.closeAll();
          this.$message.error("查询详情信息失败");
        });
    },
    //获取FileList并打开dialog
    getFileList(relaId, relaType) {
      trackingAgentApi
        .getFileList(relaId)
        .then((res) => {
          if (res.data.message === "success") {
            let arr = res.data.data;
            this.fileList = [];
            for (let i = 0; i < arr.length; i++) {
              let obj = {};
              obj.id = arr[i].id;
              obj.url = arr[i].fileUri;
              obj.name = arr[i].fileName;
              obj.size = arr[i].fileSize;
              this.fileList.push(obj);
            }
            this.resultData.data.fileList = this.fileList;
            localStorage.setItem("resultData", JSON.stringify(this.resultData));
            this.showPage();
            this.dialogVisible = true;
          } else {
            this.fileList = [];
            this.$message.closeAll();
            this.$message.error("查询详情附件信息失败");
          }
        })
        .catch(() => {
          this.$message.closeAll();
          this.$message.error("查询详情附件信息失败");
        });
    },
    //加载所需页面
    showPage() {
      let formPath = this.resultPath;
      if (!formPath || formPath === "") {
        return;
      }
      if (formPath.indexOf("cmdOpt") > -1) {
        this.cmdOptPage_show = true;
        this.cmdCheckPage_show = false;
        this.managerCheckPage_show = false;
        this.managerApprovePage_show = false;
        this.bizEndPage_show = false;
      } else if (formPath.indexOf("cmdCheck") > -1) {
        this.cmdOptPage_show = false;
        this.cmdCheckPage_show = true;
        this.managerCheckPage_show = false;
        this.managerApprovePage_show = false;
        this.bizEndPage_show = false;
      } else if (formPath.indexOf("managerCheck") > -1) {
        this.cmdOptPage_show = false;
        this.cmdCheckPage_show = false;
        this.managerCheckPage_show = true;
        this.managerApprovePage_show = false;
        this.bizEndPage_show = false;
      } else if (formPath.indexOf("managerApprove") > -1) {
        this.cmdOptPage_show = false;
        this.cmdCheckPage_show = false;
        this.managerCheckPage_show = false;
        this.managerApprovePage_show = true;
        this.bizEndPage_show = false;
      } else if (formPath.indexOf("bizEnd") > -1) {
        this.cmdOptPage_show = false;
        this.cmdCheckPage_show = false;
        this.managerCheckPage_show = false;
        this.managerApprovePage_show = false;
        this.bizEndPage_show = true;
      }
    },
    //关闭dialog
    closeDialog() {
      this.dialogVisible = false;
      this.cmdOptPage_show = false;
      this.cmdCheckPage_show = false;
      this.managerCheckPage_show = false;
      this.managerApprovePage_show = false;
      this.bizEndPage_show = false;
    },
    //数据字典转换
    dataStatus(statusCode, flag) {
      if (flag === "0") {
        return this.cmdStatusArr[statusCode];
      } else if (flag === "1") {
        return this.procStatusArr[statusCode];
      } else if (flag === "2") {
        return this.cmdCodeArr[statusCode];
      }
    },
    //金额千分位
    amountFilter(num) {
      return fun.formatNumber(num);
    },
    //初始化数据字典
    initHandle() {
      let arr = [
        { name: "指令经办(国泰君安)", code: "cmdOpt" },
        { name: "指令复核(国泰君安)", code: "cmdCheck" },
        { name: "管理人经办", code: "transfer_glrjb" },
        { name: "管理人复核", code: "managerCheck" },
        { name: "管理人审批", code: "managerApprove" },
        { name: "托管划款中", code: "transOperating" },
        { name: "划款成功", code: "transSuccess" },
        { name: "划款失败", code: "transFailed" },
        { name: "指令撤销", code: "cmdCancel" },
        { name: "指令作废", code: "cmdInvalid" },
        { name: "指令暂缓", code: "cmdSuspend" },
      ];
      //初始化划款状态
      let arr2 = [
        { name: "划款审批中", code: "transApproving" },
        { name: "托管划款中", code: "transOperating" },
        { name: "指令暂缓", code: "cmdSuspend" },
      ];
      let arr4 = [
        { name: "划款审批中", code: "transApproving" },
        { name: "托管划款中", code: "transOperating" },
        { name: "划款失败", code: "transFailed" },
        { name: "划款成功", code: "transSuccess" },
        { name: "指令撤销", code: "cmdCancel" },
        { name: "指令作废", code: "cmdInvalid" },
        { name: "指令暂缓", code: "cmdSuspend" },
      ];
      //初始化划款类型
      let arr3 = [
        { name: "银转证", code: "gm040101" },
        { name: "证转银", code: "gm040102" },
        { name: "银转期", code: "gm040201" },
        { name: "期转银", code: "gm040202" },
        { name: "银转期(手工入金)", code: "gm040203" },
        { name: "银转信", code: "gm040301" },
        { name: "信转银", code: "gm040302" },
        { name: "银转衍", code: "gm040401" },
        { name: "衍转银", code: "gm040402" },
        { name: "银转衍(手工入金)", code: "gm040403" },
        { name: "银转贵", code: "gm040501" },
        { name: "贵转银", code: "gm040502" },
        { name: "银转贵(手工入金)", code: "gm040503" },
        { name: "基金认申购", code: "gm050101" },
        { name: "存款投资", code: "gm050102" },
        { name: "网下新股申购(上海)", code: "gm050103" },
        { name: "网下新股申购(深圳)", code: "gm050104" },
        { name: "网下新债申购", code: "gm050105" },
        { name: "银行间债券交易", code: "gm050106" },
        { name: "交易所交易（付款）", code: "gm040601" },
        { name: "交易所交易（收款）", code: "gm040602" },
        { name: "备付金代付", code: "gm040603" },
        { name: "托管转中债", code: "gm040701" },
        { name: "中债转托管", code: "gm040702" },
        { name: "托管转上清", code: "gm040703" },
        { name: "上清转托管", code: "gm040704" },
        { name: "中债转上清", code: "gm040705" },
        { name: "上清转中债", code: "gm040706" },
      ];

      //初始化划款状态
      this.transferStatuses = arr2;
      //绑定数据字典
      for (let i = 0; i < arr.length; i++) {
        this.cmdStatusArr[arr[i].code] = arr[i].name;
      }
      for (let i = 0; i < arr4.length; i++) {
        this.procStatusArr[arr4[i].code] = arr4[i].name;
      }

      for (let i = 0; i < arr3.length; i++) {
        this.cmdCodeArr[arr3[i].code] = arr3[i].name;
      }
    },
    isShowCl(val) {
      let procStatus = val.procStatus;
      if (
        procStatus === "transApproving" ||
        procStatus === "transOperating" ||
        procStatus === "cmdSuspend"
      ) {
        return true;
      }
      return false;
    },
    transferCheckClick(data) {
      if (data.flag) {
        this.countDialog = false;
        this.bizBeginPage_show = false;
        this.selectAll("");
      }
    },
    getBpm(bpmnId) {
      var bpmnxml = "";
      commonApi
        .get_processdefine_xml(bpmnId)
        .then((res) => {
          // debugger;
          if (res.data.status === 0) {
            bpmnxml = res.data.data;
            $("#diagram").html("");
            $("#diagram").fadeIn(100);
            //$(".bpmn_delete_img").fadeIn(100);
            commonFun.bpmnModule(bpmnxml, [], "", "");
            this.leftDrawer = true;
          } else {
            this.$message.closeAll();
            this.$message.error("查询失败");
          }
        })
        .catch(() => {
          this.$message.closeAll();
          this.$message.error("查询失败");
        });
    },
    getHandleHtml() {
      commonApi
        .getHandleHtml(this.handleHtmlParams)
        .then((res) => {
          if (res.data.status === 200) {
            if (res.data.data) {
              let html = res.data.data.html;
              $("#handle_div").html(html);
              this.isHaveData = false;
            } else {
              this.isHaveData = true;
            }
          } else {
            this.$message.closeAll();
            this.$message.error("查询失败");
          }
        })
        .catch(() => {
          this.$message.closeAll();
          this.$message.error("查询失败");
        });
    },
    drawerClick(data) {
      if (data.flag) {
        console.log(data.definedId);
        this.definedId = data.definedId;
        //this.getBpm(data.definedId);
        this.bpmPage_show = true;
        this.leftDrawer = true;
      } else {
        if (data.isOpen) {
          this.dialogSize = "80%";
          this.isShowYd = true;
          this.getHandleHtml();
        } else {
          this.dialogSize = "50%";
          this.isShowYd = false;
        }
      }
    },
  },
};
</script>

<style>
.transferListWidth {
  width: 60% !important;
}
</style>
<style rel="stylesheet/scss" lang="scss" scoped>
.el-dialog__wrapper .el-dialog__header {
  padding: 10px !important;
  width: 690px;
  background-color: white;
}
.el-dialog__wrapper .el-dialog__headerbtn {
  top: 10px !important;
  right: 10px !important;
  left: 660px !important;
}
.el-dialog__wrapper .el-dialog__body {
  padding: 10px !important;
  width: 690px;
  background-color: white;
}
.el-dialog .el-dialog__footer {
  padding: 10px !important;
  width: 690px;
  background-color: white;
}
.el-drawer_myspan {
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
  color: #72767b;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  margin-bottom: 32px;
  padding: 20px 20px 0;
  margin-top: -75px;
}
</style>

<style rel="stylesheet/scss" lang="scss" >
//  .el-drawer.rtl {
//        overflow: scroll;
//   }

:focus {
  outline: 0;
}

.el-drawer__header > :first-child {
  color: #409eff;
}
</style>





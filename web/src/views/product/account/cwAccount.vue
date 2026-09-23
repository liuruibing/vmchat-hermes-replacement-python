<template>
  <div>
    <el-form
      :inline="true"
      :rules="rulesCw"
      ref="formInline"
      :model="formInline"
      style="margin-bottom: 8px"
      class="demo-form-inline form_inline_search"
      @submit.native.prevent
    >
      <el-row>
        <el-col :span="16">
          <div style="width: 100%; height: 50px">
            <el-form-item label="产品" prop="fundCode">
              <select-table
                v-model="formInline.fundCode"
                @enter="onSubmit()"
              ></select-table>
            </el-form-item>
            <el-form-item label="开户机构" prop="openStruc">
              <el-input
                @keydown.enter.native="onSubmit()"
                maxlength="100"
                v-model.trim="formInline.openStruc"
                clearable
                placeholder="请填写开户机构"
                size="small"
              ></el-input>
            </el-form-item>
            <el-form-item label="场外衍生品类型" prop="otcdTypeDim">
              <el-select
                style="width: 100%"
                v-model="formInline.otcdTypeDim"
                clearable
                filterable
                placeholder="请选择"
              >
                <el-option
                  v-for="item in otcdTypeDimHiddenArr"
                  :key="item.value"
                  :label="item.name"
                  :value="item.value"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="8">
          <el-form-item class="search_button_com">
            <el-button
              type="primary"
              @click="onSubmit(true)"
              style="margin-bottom: 5px"
              size="small"
              ><i class="el-icon-search"></i>查询</el-button
            >
            <el-button
              type="primary"
              plain
              size="small"
              style="margin-bottom: 5px"
              @click="restForm('formInline')"
              ><i class="el-icon-delete"></i>重置</el-button
            >
            <el-button
              v-btn="'cwAccount.insert.info'"
              type="primary"
              plain
              @click="addData()"
              style="margin-bottom: 5px"
              size="small"
              ><i class="el-icon-circle-plus-outline"></i>新增</el-button
            >
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <div class="forms_table_title">
      <i class="el-icon-s-data"></i>场外期权账户列表
    </div>
    <el-table
      ref="multipleTable"
      @selection-change="handleSelectionChange"
      :data="tableData"
      border
      stripe
      @sort-change="handleSortChange"
      v-loading="tableLoading"
      style="width: 100%"
    >
      <!-- <el-table-column fixed type='selection' width='35'></el-table-column> -->
      <el-table-column
        prop="productCode"
        sortable="custom"
        show-overflow-tooltip
        label="产品代码"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.productCode | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="productName"
        sortable="custom"
        show-overflow-tooltip
        label="产品名称"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.productName | noDataFilter }}</span>
        </template>
      </el-table-column>
      
      <el-table-column
        prop="otcdTypeName"
        sortable="custom"
        show-overflow-tooltip
        label="场外衍生品类型"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.otcdTypeName | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="openStruc"
        sortable="custom"
        show-overflow-tooltip
        label="开户机构"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.openStruc | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="isHold"
        sortable="custom"
        show-overflow-tooltip
        label="是否持仓"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">
            <span v-if="scope.row.isHold === 0">否</span>
            <span v-else-if="scope.row.isHold === 1">是</span>
            <span v-else>{{ scope.row.isHold | noDataFilter }}</span>
          </span>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        fixed="right"
        width="280"
        align="center"
      >
        <template slot-scope="scope">
          <el-button style="width:52px;" 
            type="primary" 
            size="small" 
            v-if="scope.row.approvalStatus=='0'" 
            v-btn="'audit'"
            :loading="pass_loading"
            @click="check(scope.row)"
            >审 核</el-button
          >
          <el-button 
            type="primary" 
            size="small" 
            v-if="scope.row.approvalStatus=='1'"
            v-btn="'Anti-audit'" 
            :loading="pass_loading"
            @click="check_back(scope.row)"
            >反审核</el-button
          >
          <el-button type="primary" size="small" @click="searchData(scope.row)"
            >查看详情</el-button
          >
          <el-button
            v-btn="'cwAccount.update.info'"
            v-if="scope.row.approvalStatus=='1'?false:true"
            type="primary"
            size="small"
            @click="editData(scope.row)"
            >编辑</el-button
          >
          <el-button
            v-btn="'cwAccount.delete.info'"
            v-if="scope.row.approvalStatus=='1'?false:true"
            type="danger"
            plain
            size="small"
            @click="delData(scope.row)"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <Pagination
      :total="total"
      :page="formInline.pageNum"
      :limit="formInline.pageSize"
      @pagination="Pagination"
    ></Pagination>
    <!-- 新增、编辑 -->
    <el-dialog
      :title="countTitle"
      customClass="MyWidth"
      center
      @closed="closedDialog"
      @open="opendDialog"
      :visible.sync="countDialog"
      :close-on-click-modal="false"
    >
      <el-container style="height: 400px" v-if="isContainerRush">
        <el-main class="mainBox">
          <el-form
            ref="formCount"
            :model="formCount"
            :rules="countRules"
            label-position="right"
          >
            <div class="forms_table_title">
              <i class="el-icon-s-data"></i>账户基本信息
            </div>
            <el-row>
              <el-col :span="12">
                <el-form-item
                  label=" 产品"
                  prop="productId"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <select-table v-model="formCount.productId" @sendDataObj='dataObj' v-if="!isSearchData" ref="relation"></select-table>
                  <el-input v-model="formCount.productId" disabled v-else></el-input>
                </el-form-item>
                <el-form-item
                  label="场外衍生品类型"
                  prop="otcdTypeDim"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-select
                    style="width:100%"
                    :disabled="isSearchData"
                    v-model="formCount.otcdTypeDim"
                    clearable
                    filterable
                    placeholder="请选择"
                    ref="otcdTypeDim"
                  >
                    <el-option
                      v-for="item in otcdTypeDimHiddenArr"
                      :key="item.value"
                      :label="item.name"
                      :value="item.value"
                    >
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item
                  label="是否持仓"
                  prop="isHold"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-radio
                    :disabled="isSearchData"
                    v-model="formCount.isHold"
                    :label="0"
                    >否</el-radio
                  >
                  <el-radio
                    :disabled="isSearchData"
                    v-model="formCount.isHold"
                    :label="1"
                    >是</el-radio
                  >
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item
                  style="visibility:hidden;"
                  label="产品代码"
                  prop="productCode"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    disabled
                    v-model.trim="formCount.productCode"
                    clearable
                    ref="productCode"
                  ></el-input>
                </el-form-item>

                <el-form-item
                  label="开户机构"
                  prop="openStruc"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    v-model.trim="formCount.openStruc"
                    clearable
                    ref="openStruc"
                  ></el-input>
                </el-form-item>
              </el-col>
            </el-row>

            <el-form-item
              label="备注"
              prop="remark"
              class="mb20"
              :label-width="formLabelWidth"
            >
              <el-input
                :disabled="isSearchData"
                type="textarea"
                :autosize="{minRows: 3}"
                maxlength="166"
                show-word-limit
                placeholder="请输入备注"
                v-model="formCount.remark"
                ref="remark"
              >
              </el-input>
            </el-form-item>
            <br />
            <el-form-item
              label="账户资料上传"
              prop="file"
              class="mb20"
              :label-width="formLabelWidth"
            >
              <el-upload
                class="upload-demo"
                ref="upload"
                :disabled="isSearchData"
                :headers="hearders"
                :on-preview="downFile"
                :action="fileUploadUrl"
                :on-error="handleError"
                :on-remove="handleRemove"
                :on-success="handleSuccess"
                :on-change="handleChange"
                :file-list="fileList"
                :auto-upload="false"
              >
                <el-button
                  slot="trigger"
                  size="small"
                  type="primary"
                  v-show="!isSearchData"
                  >浏览</el-button
                >
              </el-upload>
            </el-form-item>
          </el-form>
          <div class="forms_table_title">
            <i class="el-icon-s-data"></i>投资工具
          </div>
          <el-button
            type="primary"
            :disabled="isSearchData"
            plain
            @click="insertEvent"
            style="margin-bottom: 5px"
            size="small"
          >
            <i class="el-icon-circle-plus-outline"></i>新增
          </el-button>
          <el-button
            type="danger"
            :disabled="isSearchData"
            plain
            @click="removeEvent"
            style="margin-bottom: 5px"
            size="small"
          >
            <i class="el-icon-delete"></i>移除
          </el-button>
          <vxe-table
            border
            keep-source
            show-overflow
            ref="xTable"
            class="my_table_insert"
            height="200"
            :cell-class-name="cellClassName"
            :header-cell-class-name="headerCellClassName"
            :edit-rules="validRules"
            :data="tableDataEdit"
            :edit-config="{
              trigger: 'click',
              mode: 'row',
              icon: 'fa fa-pencil',
              showStatus: true,
            }"
          >
            <vxe-table-column type="checkbox" width="60"></vxe-table-column>
            <vxe-table-column
              type="seq"
              title="序号"
              width="60"
            ></vxe-table-column>
            <vxe-table-column
              field="investToolDims"
              title="投资工具"
              :edit-render="{
                name: '$select',
                props: { disabled: isSearchData },
                options: investToolDimsArr,
                optionProps: { value: 'dimCde', label: 'dimNme' },
              }"
            ></vxe-table-column>
            <vxe-table-column
              field="counterpartyName"
              title="对手方账户名称"
              :edit-render="{
                name: 'input',
                attrs: { type: 'text', disabled: isSearchData, maxlength: 66 },
              }"
            ></vxe-table-column>
            <vxe-table-column
              field="counterpartyAccount"
              title="对手方账号"
              :edit-render="{
                name: 'input',
                attrs: { type: 'text', disabled: isSearchData, maxlength: 66 },
              }"
            ></vxe-table-column>

            <vxe-table-column
              field="isHold"
              title="是否持仓"
              :edit-render="{
                name: '$select',
                props: { disabled: isSearchData },
                options: isHoldArr,
                optionProps: { value: 'dimCde', label: 'dimNme' },
              }"
            ></vxe-table-column>
            <vxe-table-column
              field="emailKey"
              title="交互邮箱关键字"
              :edit-render="{
                name: 'input',
                attrs: { type: 'text', disabled: isSearchData, maxlength: 66 },
              }"
            ></vxe-table-column>
            <vxe-table-column
              field="email"
              title="交互邮箱"
              :edit-render="{
                name: 'input',
                attrs: { type: 'text', disabled: isSearchData, maxlength: 66 },
              }"
            ></vxe-table-column>
            <vxe-table-column
              field="gzbSubject"
              title="估值表科目"
              :edit-render="{
                name: 'input',
                attrs: { type: 'text', disabled: isSearchData, maxlength: 66 },
              }"
            ></vxe-table-column>
          </vxe-table>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="countDialog = false">取 消</el-button>
        <el-button
          v-btn="saveCode"
          v-if="!isSearchData"
          type="primary"
          size="small"
          :loading="countSubmit_btn"
          @click="countSubmit()"
          >确 定</el-button
        >
      </div>
    </el-dialog>
  </div>
</template>

<script>
import selectTable from "@/views/commonComponents/selectTable.vue";
import Pagination from "@/components/Pagination";
import commonFun from "@/filters/new_common";
import commonApi from "@/api/common";
import { FILE_URL } from "@/utils/request";
import { getToken } from "@/utils/auth";
import pageApi from "@/api/product/cwAccount";
import modelFileValidate from '@/mixinsModel/file-validate'
export default {
  name: "cwAccount",
  mixins: [modelFileValidate],
  components: { Pagination, selectTable },
  data() {
    const emailValid = ({ cellValue }) => {
      let reg = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      // new Error("请输入邮箱");
      if (cellValue == "") return 
      else if (cellValue) {
        if (!reg.test(cellValue)) {
          return new Error("请输入正确的邮箱格式");
        }
      } else {
      }
    };
    return {
      isContainerRush: true,
      formInline: {
        fundCode: "",
        openStruc: "",
        otcdTypeDim: "",
        orderString: "",
        pageSize: 50,
        pageNum: 1,
      },
      //  查询校验
      rulesCw: {
        openStruc: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message: this.$regularValidator.empty().msg,
          },
        ],
      },
      validRules: {
        counterpartyName: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message: this.$regularValidator.empty().msg,
          },
        ],
        counterpartyAccount: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: /^[a-zA-Z0-9]*$/,
            message: "请输入字母或者数字",
          },
        ],
        emailKey: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message: this.$regularValidator.empty().msg,
          },
        ],
        email: [
          // {required: false, type: 'string', pattern: /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/, trigger: 'change', message: '请输入正确的邮箱格式' },
          { required: false, validator: emailValid, trigger: "change" },
        ],
        gzbSubject: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message: this.$regularValidator.empty().msg,
          },
        ],
      },
      tableData: [], //表格数据
      tableLoading: false, //表格加载
      pass_loading:false,
      tableMultipleSelection: [], //表格选择数据集合
      total: 0, //总条数
      countDialog: false, // 弹窗
      countTitle: "", //标题
      countFormList: "", //是新增还是编辑
      // 新增 编辑
      formCount: {
        productId: "", //产品名称
        productCode: "", //产品代码
        productName: "",
        otcdTypeDim: "", //场外衍生品类型
        openStruc: "", //开户机构
        isHold: "", //是否持仓
        remark: "",
      },
      // 操作类型 1、添加 2、编辑
      operationType: 1,
      // 弹窗验证规则
      countRules: {
        productId: [
          {
            required: true,
            type: "string",
            message: "请选择产品",
            trigger: "change",
          },
        ],
        openStruc: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message: this.$regularValidator.empty().msg,
          },
        ],
        remark: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message: this.$regularValidator.empty().msg,
          },
        ],
      },
      formLabelWidth: "170px",
      countSubmit_btn: false,
      accountCodes: [], //产品数组
      investTypeSearchArr: [],
      tableDataEdit: [],
      otcdTypeDimHiddenArr: [
        { name: "场外期权", value: "otcdType_cwqq" },
        { name: "收益互换", value: "otcdType_syhh" },
        { name: "跨境收益互换", value: "otcdType_kjsyhh" },
        { name: "利率互换", value: "otcdType_llhh" },
      ],
      investToolDimsArr: [],
      isHoldArr: [
        { dimCde: 0, dimNme: "否" },
        { dimCde: 1, dimNme: "是" },
      ],
      fileUploadUrl: "", //上传文件url
      hearders: {
        Authorization: "vXcx3IBemn1kShhobK2DfpY3kFqiBaSb",
        "Access-Control-Allow-Origin": "*",
      }, //上传头
      fileList: [], //文件列表
      isChangeFile: false,
      bigSize: true,
      nowSize: 0,
      isSearchData: false,
      rmoveFileId: [],
      saveCode: "",
    };
  },

  mounted() {
    this.getProductsAll();
    this.getEdims();
    this.onSubmit(true);
  },

  methods: {
    cellClassName ({ row, rowIndex, column, columnIndex }) {
      return 'vxe-cell-class-name'
    },
    headerCellClassName ({ column, columnIndex }) {
      return 'vxe-header-cell-class-name'
    },
    dataObj (data) {
      if(data){
        this.formCount.productCode = data.fundCode
        this.formCount.productName = data.fundName
      }else{
        this.formCount.productCode = ''
        this.formCount.productName = ''
      }
    },
    // dialog关闭初始化
    closedDialog() {
      this.fileList = [];
      this.$refs["formCount"].resetFields();
      this.isContainerRush = false;
    },
    opendDialog() {
      this.isContainerRush = true;
    },
    // 查询
    onSubmit(flag) {
      // 接口请求前的查询输入框校验
      this.$refs["formInline"].validate((valid) => {
        // if (!valid) return this.$message.warning("请输入正确的查询条件 !");
        this.tableLoading = true;
        // 消除没有值的参数
        if (flag) {
          this.formInline.pageNum = 1;
        }
        let data = { ...this.formInline };
        if (data.fundCode) data["fundCode"] = data.fundCode.split("_")[0];
        let params = commonFun.parameterSrc(data);
        pageApi
          .getDataSourceList(params)
          .then((response) => {
            if (response.data.status === 200) {
              this.tableData = response.data.data.list;
              // 页面总条数
              this.total = response.data.data.total;
            } else {
              this.tableData = [];
              this.total = 0;
              this.formInline.pageSize = 50;
              this.formInline.pageNum = 1;
            }
            this.tableLoading = false;
          })
          .catch(() => {
            this.tableData = [];
            this.total = 0;
            this.formInline.pageSize = 50;
            this.formInline.pageNum = 1;
            this.tableLoading = false;
          });
      });
    },
    //分页
    Pagination(val) {
      this.formInline.pageSize = val.limit; //页面条数
      this.formInline.pageNum = val.page; //页面
      this.onSubmit(false);
    },
    // table批量选择结果
    handleSelectionChange(val) {
      this.tableMultipleSelection = val;
    },

    //排序
    handleSortChange(val) {
      this.formInline.orderString = commonFun.orderByString(val);
      this.onSubmit(false);
    },
    //新增数据
    addData() {
      this.countTitle = "新增";
      this.countFormList = "add";
      this.countDialog = true;
      this.operationType = 1;

      this.bigSize = true;
      this.fileList = [];
      this.isSearchData = false;
      this.isChangeFile = false;
      this.tableDataEdit = [];
      this.saveCode = "cwAccount.insert.save";

      // 清除
      this.$nextTick(() => {
        this.$refs["formCount"].resetFields();
        this.formCount.productId = "";
        this.formCount.productCode = "";
        this.formCount.productName = "";
        this.formCount.otcdTypeDim = "";
        this.formCount.openStruc = "";
        this.formCount.isHold = "";
        this.formCount.remark = "";
        this.formCount.id = "";
      });
    },
    // 行编辑数据
    editData(row) {
      console.log("修改", row);
      this.countTitle = "编辑";
      this.countFormList = "edit";
      this.countDialog = true;
      this.operationType = 2;

      this.bigSize = true;
      this.fileList = [];
      this.isSearchData = false;
      this.isChangeFile = false;
      this.tableDataEdit = [];
      this.rmoveFileId = [];
      this.saveCode = "cwAccount.update.save";

      this.getFileList(row.id, "cwh_file");
      this.$nextTick(() => {
        this.$refs["formCount"].resetFields();
        this.formCount.productId = row.productCode+'_'+row.productName;
        this.formCount.productCode = row.productCode;
        this.formCount.productName = row.productName || '';
        this.formCount.otcdTypeDim = row.otcdTypeDim;
        this.formCount.openStruc = row.openStruc;
        if (row.isHold != undefined) {
          this.formCount.isHold = +row.isHold;
        } else {
          this.formCount.isHold = "";
        }
        this.formCount.remark = row.remark;
        this.formCount.id = row.id;
        this.tableDataEdit = row.otcdTools;
        console.log("修改this.formCount", this.formCount);
      });
    },
    searchData(row) {
      this.bigSize = true;
      this.countTitle = "查看详情";
      this.countFormList = "edit";
      this.countDialog = true;
      this.operationType = 2;

      this.isSearchData = true;
      this.bigSize = true;
      this.fileList = [];
      this.isChangeFile = false;
      this.tableDataEdit = [];
      this.getFileList(row.id, "cwh_file");
      this.$nextTick(() => {
        this.$refs["formCount"].resetFields();
        this.formCount.productId = row.productCode+'_'+row.productName;
        this.formCount.productCode = row.productCode;
        this.formCount.productName = row.productName || '';
        this.formCount.otcdTypeDim = row.otcdTypeDim;
        this.formCount.openStruc = row.openStruc;
        this.formCount.isHold = row.isHold;
        this.formCount.remark = row.remark;
        this.formCount.id = row.id;
        this.tableDataEdit = row.otcdTools;
      });
    },
    //新增计算任务确认
    countSubmit() {
      var self = this;
      if (!this.bigSize) {
        this.$message.error("上传文件大小不能超过 50MB!");
        return;
      }
      this.$refs["formCount"].validate((valid, object) => {
        if (valid) {
          //     this.$message.closeAll()
          //     if (this.operationType === 1) {
          //          // 添加
          //          this.saveData();
          //     } else {
          //          // 修改
          //          this.updateParamSet();
          //  }
          this.$refs["xTable"].validate((vxeValid) => {
            if (!vxeValid) {
              this.$message.closeAll();
              if (this.operationType === 1) {
                // 添加
                this.saveData();
              } else {
                // 修改
                this.updateParamSet();
              }
            } else {
              return false;
            }
          });
        } else {
          let temp = []
          for (let i in object) {
            temp.push(i)
          }
          if (temp.length){
            if (temp[0] == 'productId') {
              this.$nextTick(() => {
                this.$refs.relation.relation()
              })
            } else {
              this.$nextTick(() => {
               this.$refs[temp[0]].focus()}
             )}
           }
        }
      });
    },
    saveData() {
      this.$confirm("确定新增?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          let params = {};
          params = commonFun.parameterSrc(this.formCount);
          this.countSubmit_btn = true;
          if (this.$refs.xTable) {
            params.otcdTools = this.$refs.xTable.getTableData().tableData;
          } else {
            params.otcdTools = [];
          }
          let formData = this.initFormData(params);
          pageApi
            .addDataSource(formData)
            .then((response) => {
              if (response.data.status === 200) {
                this.countDialog = false;
                this.$message.closeAll();
                this.$message({
                  message: "新增成功",
                  type: "success",
                });
                // 刷新列表
                this.onSubmit(true);
              } else {
                // 关闭移动指标弹框
                this.countDialog = false;
                this.$message.closeAll();
                this.$message({
                  message: response.data.message || "新增失败",
                  type: "warning",
                });
              }
              this.countSubmit_btn = false;
            })
            .catch(() => {
              // 关闭移动指标弹框
              this.countDialog = false;
              this.countSubmit_btn = false;
              this.$message.closeAll();
              this.$message({
                message: "新增失败",
                type: "warning",
              });
            });
        })
        .catch(() => {
          // 关闭移动指标弹框
          this.$message.info('已取消')
          this.countDialog = true;
          this.countSubmit_btn = false;
        });
    },
    updateParamSet() {
      this.$confirm("确定修改?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          let params = {};
          params = commonFun.parameterSrc(this.formCount);
          this.countSubmit_btn = true;
          if (this.$refs.xTable) {
            params.otcdTools = this.$refs.xTable.getTableData().tableData;
          } else {
            params.otcdTools = [];
          }
          let formData = this.initFormData(params);
          pageApi
            .updateDataSource(formData)
            .then((response) => {
              if (response.data.status === 200) {
                this.countDialog = false;
                this.$message.closeAll();
                this.$message({
                  message: "修改成功",
                  type: "success",
                });
                this.removeFiles();
                this.onSubmit(false);
              } else {
                // 关闭移动指标弹框
                this.countDialog = false;
                this.$message.closeAll();
                this.$message({
                  message: response.data.message || "修改失败",
                  type: "warning",
                });
              }
              this.countSubmit_btn = false;
            })
            .catch(() => {
              // 关闭移动指标弹框
              this.countDialog = false;
              this.countSubmit_btn = false;
              this.$message.closeAll();
              this.$message({
                message: "修改失败",
                type: "warning",
              });
            });
        })
        .catch(() => {
          // 关闭移动指标弹框
          this.$message.info('已取消')
          this.countDialog = true;
          this.countSubmit_btn = false;
        });
    },
    // 按钮批量删除
    deleteData() {
      if (this.tableMultipleSelection.length === 0) {
        this.$message.closeAll();
        this.$message({
          message: "请选择要删除的数据",
          type: "warning",
        });
      } else {
        this.delData(this.tableMultipleSelection);
      }
    },
    // 行删除数据
    delData(row) {
      this.$confirm("确定删除?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          let params = {};
          params["id"] = row.id;
          pageApi
            .deleteDataSource(params)
            .then((response) => {
              if (response.data.status === 200) {
                this.$message.closeAll();
                this.$message({
                  message: "删除成功",
                  type: "success",
                });
                // 刷新树列表
                this.onSubmit(false);
              } else {
                this.$message.closeAll();
                this.$message({
                  message: response.data.message || "删除失败",
                  type: "warning",
                });
              }
            })
            .catch(() => {
              // 关闭移动指标弹框
              this.$message.closeAll();
              this.$message({
                message: "删除失败",
                type: "warning",
              });
            });
        })
        .catch(() => {});
    },
    restForm(formName) {
      var self = this;
      self.$refs[formName].resetFields();
    },
    getProductsAll() {
      commonApi
        .getProductsAll()
        .then((res) => {
          let self = this;
          if (res.data.message === "success") {
            let arr = res.data.data;
            this.accountCodes = [];
            for (let i = 0; i < arr.length; i++) {
              let obj = {};
              obj.value = arr[i].fundCode;
              obj.name = arr[i].fundName + " (" + arr[i].fundCode + ")";
              this.accountCodes.push(obj);
            }
          } else {
            this.accountCodes = [];
            this.$message.error("初始化数据失败");
          }
        })
        .catch(() => {
          this.accountCodes = [];
          this.$message.error("初始化数据失败");
        });
    },
    insertEvent() {
      const record = {};
      this.$refs.xTable.insert(record).then(({ row }) => {
        this.$refs.xTable.setActiveCell(-1, "sex");
        this.$refs.xTable.setActiveRow(row);
      });
    },

    removeEvent() {
      const selectRecords = this.$refs.xTable.getCheckboxRecords();
      if (selectRecords.length) {
        this.$confirm("您确定要删除选中的数据吗?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        })
          .then(() => {
            this.$refs.xTable.removeCheckboxRow();
          })
          .catch(() => {
            this.$message({
              type: "info",
              message: "已取消",
            });
          });
      } else {
        this.$message({ type: "error", message: "请至少选择一条数据" });
      }
    },
    removeFiles() {
      let temp = []
      for (let i of this.fileList) {
        if (i.id) temp.push(i)
      }
      this.rmoveFileId.forEach(item => {
        let flag = false
        temp.forEach(item2 => {
          if (item.id == item2.id) flag = true
        })
        if (!flag) this.removeFile(item.id)
      })
    },
    removeFile(id) {
      commonApi
        .delFileList(id)
        .then((res) => {
          if (res.data.message === "success") {
          } else {
            this.$message.closeAll();
            this.$message.error("删除失败");
          }
        })
        .catch(() => {
          this.$message.closeAll();
          this.$message.error("删除失败");
        });
    },
    //移除文件事件
    handleRemove(file, fileList) {
      this.fileList = fileList
      this.isChangeFile = true;
      // if (file.id) {
      //   this.rmoveFileId.push(file.id);
      // }

      this.nowSize = this.nowSize - file.size;
      this.bigSize = this.nowSize / 1024 / 1024 < 50;
    },
    //上传文件异常事件
    handleError() {
      this.$message.error("文件上传失败");
      this.submit_btn = false; //按钮启用
    },
    //上传文件成功事件
    handleSuccess(res, file, fileList) {
      if (res.message === "success") {
        this.countDialog = false;
        this.$message.closeAll();
        this.$message({
          message: "操作成功",
          type: "success",
        });
        // 刷新列表
        this.onSubmit(true);
      } else {
        this.$message.error("文件上传失败");
        this.fileList = [];
      }
      this.submit_btn = false; //按钮启用
    },
    downFile(file) {
      if (file.id) {
        let params = {};
        params.id = file.id;
        params = commonFun.parameterSrc(params);

        // token信息
        if (this.$store.getters.token) {
          params["token"] = this.$store.getters.token;
        }
        //    // 表头名
        // params["exportAliasName"] = '年份,组合代码,报告类型,父标签名称,标签名称,标签值,导入时间';
        // // 导出文件名
        // params["exportFileName"] = 'XBRL.xls';
        // // 数据格式化
        // params["exportFormat"] = 'string,string,string,string,string,string,string';
        // // 表头属性名
        // params["exportPoName"] = 'rptYear,combinedId,rptType,parentElementName,elementName,elementValue,importDate';
        // // 表标题
        // params["exportTitle"] = 'XBRL导出数据';
        // 请求地址
        let action =
          this.$store.state.setting.baseApi + "api/file/v1.0/downloadFile";

        commonFun.formDownloadFile(params, action, "GET");
      }
    },
    //文件修改事件
    handleChange(file, filelist) {
      this.fileValidate(file, filelist)
      // if (filelist.length === 0) return;
      // this.fileList = [];
      // // 多个文件的累加超过50m时
      // let totalSize = 0; //文件大小的累加
      // let totalFlag = 0;
      // let totalFilel = [];
      // if (!file.size) {
      //   for (let item of filelist) {
      //     if (item.size) totalFilel.push(item);
      //   }
      //   this.fileList = totalFilel;
      //   return this.$message.error("上传的文件不能为空文件");
      // }
      // for (let item of filelist) {
      //   totalSize = item.size + totalSize;
      // }
      // totalFlag = 0 < totalSize / 1024 / 1024 && totalSize / 1024 / 1024 < 50;
      // if (!totalFlag) {
      //   this.$message.error("上传的文件不能超过 50M !");
      //   for (let item of filelist) {
      //     if (file.uid !== item.uid) {
      //       totalFilel.push(item);
      //     }
      //   }
      // } else {
      //   for (let item of filelist) {
      //     totalFilel.push(item);
      //   }
      // }
      // this.fileList = totalFilel;
      this.isChangeFile = true;
    },
    //获取FileList并打开dialog
    getFileList(relaId, relaType) {
      commonApi
        .getFileList(relaId, relaType)
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
            this.rmoveFileId = [ ...this.fileList ]
          } else {
            this.fileList = [];
            this.rmoveFileId = []
            this.$message.error("查询详情附件信息失败");
          }
        })
        .catch(() => {
          this.$message.error("查询详情附件信息失败");
        });
    },
    initFormData(params) {
      let formData = new FormData(); //  用FormData存放上传文件
      if (this.fileList.length > 0) {
        let fileIds = []
        for(let i=0;i< this.fileList.length;i++){
          if(this.fileList[i].raw){
            let aa = this.fileList[i].raw;
            formData.append('files', aa);
          }
          if(this.fileList[i].id){
            let bb = this.fileList[i].id;
            fileIds.push(bb);
          }
        }
        formData.append("fileIds", fileIds);
        formData.append("relaType", "cwh_file");
      }

      if (params.id) {
        formData.append("id", params.id);
      }
      if (params.otcdTools.length > 0) {
        let arr = params.otcdTools;
        for (let i = 0; i < arr.length; i++) {
          for (let key in arr[i]) {
            //假设这个数组对应的字段为box
            if (
              key === "investToolDims" ||
              key === "counterpartyName" ||
              key === "counterpartyAccount" ||
              key === "isHold" ||
              key === "emailKey" ||
              key === "email" ||
              key === "gzbSubject"
            ) {
              if (arr[i][key]) {
                formData.append(`otcdTools[${i}].${key}`, arr[i][key]);
              }
            }
          }
          //formData.append('stockSyss['+i+']',  arr[i]);
        }
      }

      if (params.productId) {
        formData.append("productId", params.productCode);
      }
      if (params.productCode) {
        formData.append("productCode", params.productCode);
      }
      if (params.productName) {
        formData.append("productName", params.productName);
      }
      if (params.otcdTypeDim) {
        formData.append("otcdTypeDim", params.otcdTypeDim);
      }
      if (params.openStruc) {
        formData.append("openStruc", params.openStruc);
      }
      if (params.isHold == "0" || params.isHold == "1") {
        formData.append("isHold", params.isHold);
      }
      if (params.remark) {
        formData.append("remark", params.remark);
      }
      return formData;
    },
    getEdims() {
      commonApi
        .getTransferType(280)
        .then((res) => {
          if (res.data) {
            this.investToolDimsArr = res.data;
          } else {
            this.investToolDimsArr = [];
            this.$message.error("查询投资工具失败");
          }
        })
        .catch(() => {
          this.$message.error("查询投资工具失败");
        });
    },
    // 审核
    check(row){
      let params = {
        id:row.id
      }
      this.pass_loading = true;
      pageApi.pass(params).then(res=>{
        this.pass_loading = false;
        if(res.data.status===200){
          this.$message({
            type:"success",
            message:"审核成功"
          })
          this.onSubmit(false);
        }else{
          this.$message({
            type:"error",
            message: res.data.message || "审核失败"
          })
        }
      }).catch(()=>{
        this.pass_loading = false;
      })
    },
    // 反审核
    check_back(row){
      let params = {
        id:row.id
      }
      this.pass_loading = true;
      pageApi.unpass(params).then(res=>{
        this.pass_loading = false;
        if(res.data.status===200){
          this.$message({
            type:"success",
            message:"反审核成功"
          })
          this.onSubmit(false);
        }else{
          this.$message({
            type:"error",
            message: res.data.message || "反审核失败"
          })
        }
      }).catch(()=>{
        this.pass_loading = false;
      })
    },
  },
};
</script>
<style lang='css' scoped>
</style>
 <style>
.MyWidth {
  width: 60% !important;
}
</style>

<style rel="stylesheet/scss" lang="scss" >
.vxe-select--panel {
  z-index: 9999 !important;
}
</style>
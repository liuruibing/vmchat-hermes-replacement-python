<template>
  <div>
    <el-form
      :inline="true"
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
              v-btn="'qhOpenAccount.insert.info'"
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
      <i class="el-icon-s-data"></i>期货开户统一编码列表
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
        min-width="120"
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
        min-width="120"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.productName | noDataFilter }}</span>
        </template>
      </el-table-column>
      
      <el-table-column
        prop="futureCode"
        sortable="custom"
        show-overflow-tooltip
        label="统一开户编码"
        min-width="130"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.futureCode | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="speculateCode"
        sortable="custom"
        show-overflow-tooltip
        label="中金所投机交易编码"
        min-width="170"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.speculateCode | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="hedgingCode"
        sortable="custom"
        show-overflow-tooltip
        label="中金所套保交易编码"
        min-width="170"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.hedgingCode | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="arbitrageCode"
        sortable="custom"
        show-overflow-tooltip
        label="中金所套利交易编码"
        min-width="170"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.arbitrageCode | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="shanghaiNo"
        sortable="custom"
        show-overflow-tooltip
        label="上期所交易编码"
        min-width="150"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.shanghaiNo | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="zhengzhouNo"
        sortable="custom"
        show-overflow-tooltip
        label="郑商所交易编码"
        min-width="150"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.zhengzhouNo | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="dalianNo"
        sortable="custom"
        show-overflow-tooltip
        label="大商所交易编码"
        min-width="150"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.dalianNo | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="energyNo"
        sortable="custom"
        show-overflow-tooltip
        label="能源中心交易编码"
        min-width="170"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.energyNo | noDataFilter }}</span>
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
            v-btn="'qhOpenAccount.update.info'"
            v-if="scope.row.approvalStatus=='1'?false:true"
            type="primary"
            size="small"
            @click="editData(scope.row)"
            >编辑</el-button
          >
          <el-button
            v-btn="'qhOpenAccount.delete.info'"
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
      <!-- style="height: 241px"  -->
      <el-container v-if="isContainerRush">
        <el-main class="mainBox">
          <el-form
            ref="formCount"
            :model="formCount"
            :rules="countRules"
            label-position="right"
          >
            <el-row>
              <el-col :span="12">
                <el-form-item
                  label=" 产品"
                  prop="productId"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <!-- <el-select
                    :disabled="isSearchData"
                    v-model="formCount.productId"
                    clearable
                    filterable
                    placeholder="请选择"
                  >
                    <el-option
                      v-for="item in accountCodes"
                      :key="item.value"
                      :label="item.name"
                      :value="item.value"
                    >
                    </el-option>
                  </el-select> -->
                  <select-table v-model="formCount.productId" @sendDataObj='dataObj' v-if="!isSearchData"></select-table>
                  <el-input v-model="formCount.productId" disabled v-else></el-input>
                </el-form-item>
                <el-form-item
                  label="统一开户编码"
                  prop="futureCode"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    v-model.trim="formCount.futureCode"
                    clearable
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="中金所套保交易编码"
                  prop="hedgingCode"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    v-model.trim="formCount.hedgingCode"
                    clearable
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="上期所交易编码"
                  prop="shanghaiNo"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    v-model.trim="formCount.shanghaiNo"
                    clearable
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="郑商所交易编码"
                  prop="zhengzhouNo"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    v-model.trim="formCount.zhengzhouNo"
                    clearable
                  ></el-input>
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
                    maxlength="100"
                    disabled
                    v-model.trim="formCount.productCode"
                    clearable
                  ></el-input>
                </el-form-item>

                <el-form-item
                  label="中金所投机交易编码"
                  prop="speculateCode"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    v-model.trim="formCount.speculateCode"
                    clearable
                  ></el-input>
                </el-form-item>

                <el-form-item
                  label="中金所套利交易编码"
                  prop="arbitrageCode"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    v-model.trim="formCount.arbitrageCode"
                    clearable
                  ></el-input>
                </el-form-item>

                <el-form-item
                  label="大商所交易编码"
                  prop="dalianNo"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    v-model.trim="formCount.dalianNo"
                    clearable
                  ></el-input>
                </el-form-item>

                <el-form-item
                  label="能源中心交易编码"
                  prop="energyNo"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    v-model.trim="formCount.energyNo"
                    clearable
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
                :autosize="{ minRows: 3 }"
                maxlength="166"
                show-word-limit
                placeholder="请输入备注"
                v-model="formCount.remark"
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
                :on-preview="downFile"
                :headers="hearders"
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
import pageApi from "@/api/product/qhOpenAccount";
import modelFileValidate from '@/mixinsModel/file-validate'
export default {
  name: "qhOpenAccount",
  mixins: [modelFileValidate],
  components: { Pagination, selectTable },
  data() {
    return {
      isContainerRush: true,
      formInline: {
        fundCode: "",
        orderString: "",
        pageSize: 50,
        pageNum: 1,
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
        productName: "", //产品名称
        futureCode: "", //统一开户编码
        speculateCode: "", //中金所投机交易编码
        hedgingCode: "", //中金所套保交易编码
        arbitrageCode: "", //中金所套利交易编码
        shanghaiNo: "", //上期所交易编码
        dalianNo: "", //大商所交易编码
        zhengzhouNo: "", //郑商所交易编码
        remark: "",
        energyNo: "", //能源中心交易编码
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
        futureCode: [
          {
            type: "string",
            trigger: "change",
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母或者数字",
          },
          { required: false, trigger: "blur", message: "请填写统一开户编码"}
        ],
        dalianNo: [
          {
            type: "string",
            trigger: "change",
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母或者数字",
          },
          { required: false, trigger: "blur", message: "请填写大商所交易编码"}
        ],
        speculateCode: [
          {
            type: "string",
            trigger: "change",
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母或者数字",
          },
          { required: false, trigger: "blur", message: "请填写中金所投机交易编码"}
        ],
        hedgingCode: [
          {
            type: "string",
            trigger: "change",
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母或者数字",
          },
          { required: false, trigger: "blur", message: "请填写中金所套保交易编码"}
        ],
        arbitrageCode: [
          {
            type: "string",
            trigger: "change",
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母或者数字",
          },
          { required: false, trigger: "blur", message: "请填写中金所套利交易编码"}
        ],
        shanghaiNo: [
          {
            type: "string",
            trigger: "change",
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母或者数字",
          },
          { required: false, trigger: "blur", message: "请填写上期所交易编码"}
        ],
        zhengzhouNo: [
          {
            type: "string",
            trigger: "change",
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母或者数字",
          },
          { required: false, trigger: "blur", message: "请填写郑商所交易编码"}
        ],
        energyNo: [
          {
            type: "string",
            trigger: "change",
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母或者数字",
          },
          { required: false, trigger: "blur", message: "请填写能源中心交易编码"}
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
    this.onSubmit(true);
  },

  methods: {
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
      this.$refs.formCount.clearValidate();
      this.$refs["formCount"].resetFields();
      // this.isContainerRush = false;
      // this.$nextTick(() => {
      //   this.isContainerRush = true;
      // });
    },
    opendDialog() {
      this.isContainerRush = true;
    },
    // 查询
    onSubmit(flag) {
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
      this.saveCode = "qhOpenAccount.insert.save";

      // 清除
      this.$nextTick(() => {
        this.$refs["formCount"].resetFields();
        this.formCount.productId = "";
        this.formCount.productCode = "";
        this.formCount.productName = "";
        this.formCount.futureCode = "";
        this.formCount.speculateCode = "";
        this.formCount.hedgingCode = "";
        this.formCount.arbitrageCode = "";
        this.formCount.shanghaiNo = "";
        this.formCount.dalianNo = "";
        this.formCount.zhengzhouNo = "";
        this.formCount.energyNo = "";
        this.formCount.remark = "";
        this.formCount.id = "";
      });
    },
    // 行编辑数据
    editData(row) {
      this.countTitle = "编辑";
      this.countFormList = "edit";
      this.countDialog = true;
      this.operationType = 2;

      this.bigSize = true;
      this.fileList = [];
      this.isSearchData = false;
      this.isChangeFile = false;
      this.rmoveFileId = [];
      this.saveCode = "qhOpenAccount.update.save";

      this.getFileList(row.id, "qhOpen_file");
      this.$nextTick(() => {
        this.$refs["formCount"].resetFields();
        this.formCount.productId = row.productCode+'_'+row.productName;
        this.formCount.productCode = row.productCode;
        this.formCount.productName = row.productName || '';
        this.formCount.futureCode = row.futureCode;
        this.formCount.speculateCode = row.speculateCode;
        this.formCount.hedgingCode = row.hedgingCode;
        this.formCount.arbitrageCode = row.arbitrageCode;

        this.formCount.shanghaiNo = row.shanghaiNo;
        this.formCount.dalianNo = row.dalianNo;
        this.formCount.zhengzhouNo = row.zhengzhouNo;
        this.formCount.energyNo = row.energyNo;

        this.formCount.remark = row.remark;
        this.formCount.id = row.id;
      });
    },
    searchData(row) {
      this.bigSize = true;
      this.countTitle = "查看详情";
      this.countFormList = "edit";
      this.countDialog = true;
      this.operationType = 2;
      this.bigSize = true;
      this.fileList = [];
      this.isSearchData = true;
      this.isChangeFile = false;
      this.getFileList(row.id, "qhOpen_file");
      this.$nextTick(() => {
        this.$refs["formCount"].resetFields();
        this.formCount.productId = row.productCode+'_'+row.productName;
        this.formCount.productCode = row.productCode;
        this.formCount.productName = row.productName || '';
        this.formCount.futureCode = row.futureCode;
        this.formCount.speculateCode = row.speculateCode;
        this.formCount.hedgingCode = row.hedgingCode;
        this.formCount.arbitrageCode = row.arbitrageCode;

        this.formCount.shanghaiNo = row.shanghaiNo;
        this.formCount.dalianNo = row.dalianNo;
        this.formCount.zhengzhouNo = row.zhengzhouNo;
        this.formCount.energyNo = row.energyNo;

        this.formCount.remark = row.remark;
        this.formCount.id = row.id;
      });
    },
    //新增计算任务确认
    countSubmit() {
      var self = this;
      if (!this.bigSize) {
        this.$message.error("上传文件大小不能超过 50MB!");
        return;
      }
      this.$refs["formCount"].validate((valid) => {
        if (valid) {
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
    },
    saveData() {
      this.$confirm("确定新增?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          let params = {}
          let data = { ...this.formCount }
          data['productId'] = data.productCode
          params = commonFun.parameterSrc(data)
          this.countSubmit_btn = true;
          let formData = this.initFormData(params);
          pageApi
            .addDataSource(formData)
            .then((response) => {
              if (response.data.status === 200) {
                // 关闭移动指标弹框
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
          let data = { ...this.formCount }
          data['productId'] = data.productCode
          params = commonFun.parameterSrc(data);
          this.countSubmit_btn = true;
          let formData = this.initFormData(params);
          pageApi
            .updateDataSource(formData)
            .then((response) => {
              if (response.data.status === 200) {
                // 关闭移动指标弹框
                this.countDialog = false;
                this.$message.closeAll();
                this.$message({
                  message: "修改成功",
                  type: "success",
                });
                this.removeFiles();
                this.onSubmit(false);
                // 刷新树列表
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
        formData.append("relaType", "qhOpen_file");
      }

      if (params.id) {
        formData.append("id", params.id);
      }

      if (params.productId) {
        formData.append("productId", params.productId);
      }
      if (params.productCode) {
        formData.append("productCode", params.productCode);
      }
      if (params.futureCode) {
        formData.append("futureCode", params.futureCode);
      }
      if (params.speculateCode) {
        formData.append("speculateCode", params.speculateCode);
      }
      if (params.hedgingCode) {
        formData.append("hedgingCode", params.hedgingCode);
      }
      if (params.arbitrageCode) {
        formData.append("arbitrageCode", params.arbitrageCode);
      }
      if (params.shanghaiNo) {
        formData.append("shanghaiNo", params.shanghaiNo);
      }
      if (params.dalianNo) {
        formData.append("dalianNo", params.dalianNo);
      }
      if (params.zhengzhouNo) {
        formData.append("zhengzhouNo", params.zhengzhouNo);
      }
      if (params.energyNo) {
        formData.append("energyNo", params.energyNo);
      }

      if (params.remark) {
        formData.append("remark", params.remark);
      }

      return formData;
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
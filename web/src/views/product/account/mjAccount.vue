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
              <select-table v-model="formInline.fundCode" @enter='onSubmit()'></select-table>
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
              v-btn="'mjAccount.insert.info'"
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
      <i class="el-icon-s-data"></i>募集户账户列表
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
        prop="mjType"
        sortable="custom"
        show-overflow-tooltip
        label="募集户类型"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">
            <span v-if="scope.row.mjType === '0'">公司账户</span>
            <span v-else-if="scope.row.mjType === '1'">产品账户</span>
            <span v-else>{{ scope.row.mjType | noDataFilter }}</span>
          </span>
        </template>
      </el-table-column>
      <el-table-column
        prop="companyName"
        sortable="custom"
        show-overflow-tooltip
        label="公司名称"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.companyName | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="accoName"
        sortable="custom"
        show-overflow-tooltip
        label="账户名称"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.accoName | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="accoNo"
        sortable="custom"
        show-overflow-tooltip
        label="账户账号"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.accoNo | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="accoBank"
        sortable="custom"
        show-overflow-tooltip
        label="开户行"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.accoBank | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="hvpsNo"
        sortable="custom"
        show-overflow-tooltip
        label="大额支付系统号"
        min-width="130"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.hvpsNo | noDataFilter }}</span>
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
            v-btn="'mjAccount.update.info'"
            v-if="scope.row.approvalStatus=='1'?false:true"
            type="primary"
            size="small"
            @click="editData(scope.row)"
            >编辑</el-button
          >
          <el-button
            v-btn="'mjAccount.delete.info'"
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
      customClass="mjAccountWidth"
      center
      :visible.sync="countDialog"
      :close-on-click-modal="false"
      @closed="closeDialog"
    >
     <!-- style="height: 300px" -->
      <el-container>
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
                  label="募集户类型"
                  prop="type"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-select
                    :disabled="isSearchData"
                    style="width: 100%"
                    v-model="formCount.mjType"
                    placeholder="请选择"
                    @change="selectChangemj"
                  >
                    <el-option
                      v-for="item in typeArr"
                      :key="item.value"
                      :label="item.name"
                      :value="item.value"
                    >
                    </el-option>
                  </el-select>
                </el-form-item>
                <!-- <el-form-item
                  v-show="formCount.mjType === '1'"
                  label="产品"
                  prop="productId"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <select-table v-model="formCount.productId" @sendDataObj='dataObj' v-if="!isSearchData" ref="relation"></select-table>
                  <el-input v-model="formCount.productId" disabled v-else></el-input>
                </el-form-item> -->
                <el-form-item 
                  label="产品" 
                  prop="fundCodes"
                  :label-width="formLabelWidth" 
                  v-if="formCount.mjType === '1'">
                  <multipleSelectTable
                    v-show="!isSearchData"
                    v-model="formCount.fundCodes"
                    :data="fundList"
                    :Columns="Columns"
                    idField="codeName"
                    nameField="codeName"
                    placeholder="请选择"
                  ></multipleSelectTable>
                  <el-input v-model="formCount.productId" disabled v-show="isSearchData"></el-input>
                </el-form-item>
                <el-form-item
                  label="账户名称"
                  prop="accoName"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    type="text"
                    v-model.trim="formCount.accoName"
                    clearable
                    ref="accoName"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="大额支付系统号"
                  prop="hvpsNo"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    type="text"
                    v-model.trim="formCount.hvpsNo"
                    clearable
                    ref="hvpsNo"
                  ></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item
                  label="开户行"
                  prop="accoBank"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    type="text"
                    v-model.trim="formCount.accoBank"
                    clearable
                    ref="accoBank"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  style="visibility:hidden;"
                  v-show="formCount.mjType === '1'"
                  label="产品代码"
                  prop="productCode"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="100"
                    disabled
                    v-model.trim="formCount.productCode"
                    ref="productCode"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="账户账号"
                  prop="accoNo"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    type="text"
                    v-model.trim="formCount.accoNo"
                    clearable
                    ref="accoNo"
                  ></el-input>
                </el-form-item>

                <el-form-item
                  v-if="formCount.mjType === '0'"
                  label="公司名称"
                  prop="companyName"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    type="text"
                    v-model.trim="formCount.companyName"
                    clearable
                    ref="companyName"
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
                maxlength="1000"
                show-word-limit
                style="width: 100%"
                placeholder="请输入备注"
                v-model="formCount.remark"
                ref="remark"
              >
              </el-input>
            </el-form-item>
            <el-form-item
              label="账户资料上传"
              prop="file"
              class="mb20"
              :label-width="formLabelWidth"
            >
              <el-upload
                style="width: 480px"
                class="upload-demo"
                ref="upload"
                :disabled="isSearchData"
                :headers="hearders"
                :action="fileUploadUrl"
                :on-preview="downFile"
                :on-error="handleError"
                :on-remove="handleRemove"
                :on-success="handleSuccess"
                :on-change="handleChange"
                :file-list="fileList"
                :auto-upload="false"
              >
                <el-button slot="trigger" type="primary" v-show="isUpload"
                  >浏览</el-button
                >
              </el-upload>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="cancel">取 消</el-button>
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
import bizBeginApi from '@/api/transfer/bizBegin'
import multipleSelectTable from "@/views/commonComponents/multiple-select-table2";
import selectTable from "@/views/commonComponents/selectTable.vue";
import Pagination from "@/components/Pagination";
import commonFun from "@/filters/new_common";
import commonApi from "@/api/common";
import { FILE_URL } from "@/utils/request";
import { getToken } from "@/utils/auth";
import pageApi from "@/api/product/mjAccount";
import { ecmRules } from "@/api/product/cemJudge";
import modelFileValidate from '@/mixinsModel/file-validate'
export default {
  name: "mjAccount",
  mixins: [modelFileValidate],
  components: { Pagination, selectTable, multipleSelectTable },
  data() {
    return {
      isUpload: true,
      fundList:[],
      Columns: [
        { label: "产品", prop: "codeName" },
        { label: "托管机构", prop: "trustorName" },
        { label: "基金服务机构", prop: "operatorName" },
      ],
      formInline: {
        fundCode: "",
        accoType: "raise",
        orderString: "",
        pageSize: 50,
        pageNum: 1,
      },
      tableData: [], //表格数据
      tableLoading: false, //表格加载
      tableMultipleSelection: [], //表格选择数据集合
      total: 0, //总条数
      countDialog: false, // 弹窗
      countTitle: "", //标题
      countFormList: "", //是新增还是编辑
      // 新增 编辑
      formCount: {
        mjType: "1",
        companyName: "", //公司名称
        productId: "", //产品名称
        productCode: "", //产品代码
        productName:"", //产品名称
        accoName: "", //账户名称
        accoNo: "", //账户号码
        accoBank: "", //开户行
        remark: "",
        accoType: "raise",
        hvpsNo: "", //大额支付系统号
        fundCodes:[]
      },
      // 操作类型 1、添加 2、编辑
      operationType: 1,
      // 弹窗验证规则
      countRules: {
        // productId: [
        //   {
        //     required: true,
        //     type: "string",
        //     message: "请选择产品",
        //     trigger: "change",
        //   },
        // ],
        fundCodes:[
          { required: true, message: "请选择产品", trigger: "change",}
        ],
        companyName: [
          {
            required: true,
            type: "string",
            message: "请填写公司名称",
            trigger: "blur",
          },
        ],
        accoName: [
          {
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message: this.$regularValidator.empty().msg,
          },
          {required: true,trigger: "blur",message:'请填写账户名称'}
        ],
        accoNo: [
          // {required: false, type: 'string',  trigger: 'change',  pattern: /^[\u4e00-\u9fa5a-zA-Z0-9]+$/, message: '请输入中文，字母或者数字' }
          {
            type: "string",
            trigger: "change",
            // pattern: /^[a-zA-Z0-9]+$/,
            pattern: this.$regularValidator.en_num().reg,
            message: this.$regularValidator.en_num().msg,
          },
          {required: true,trigger: "blur",message:'请填写账户账号'}
        ],
        accoBank: [
          {
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message: this.$regularValidator.empty().msg,
          },
          {required: true,trigger: "blur",message:'请填写开户行'}
        ],
        hvpsNo: [
          {
            type: "string",
            trigger: "change",
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母或者数字",
          },
          {required: true,trigger: "blur",message:'请填写大额支付系统号'}
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
      formLabelWidth: "150px",
      countSubmit_btn: false,
      accountCodes: [], //产品数组
      typeArr: [
        { name: "公司账户", value: "0" },
        { name: "产品账户", value: "1" },
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
      pass_loading:false,
    };
  },

  mounted() {
    this.getFundList(); //获取产品信息
    // this.getProductsAll();
    this.onSubmit(true);
  },

  methods: {
    // 获取产品信息
    getFundList(){
      bizBeginApi.getProductFund().then(({ data: res }) =>{
        if(res.status === 200){
          let temp = [...res.data]
          for (let i of temp) { i['codeName'] = i.fundCode + "_"+ i.fundName }
          this.fundList = temp
        } else this.$message.error('查询产品信息失败');
      }).catch((err) => { this.$message.error('查询产品信息失败') })
    },
    dataObj (data) {
      // console.log(data)
      if(data){
        this.formCount.productCode = data.fundCode;
        this.formCount.productName = data.fundName;
      }else{
        this.formCount.productCode = '';
        this.formCount.productName = '';
      }
    },
    closeDialog() {
      this.fileList = [];
      this.$refs.formCount.clearValidate();
      this.$refs.formCount.resetFields();
    },
    //  募集选择
    selectChangemj(data) {
      console.log(data);
      this.$nextTick(()=>{
        if(data==0){
          this.countRules.companyName=[{required: true, type: "string", message: "请填写公司名称", trigger: "blur", }]
          this.countRules.productId={}
        }
        if(data==1){
          this.countRules.productId=[{required: true, type: "string", message: "请选择产品", trigger: "change", }]
          this.countRules.companyName={}
        }
      })
      this.formCount.companyName='';
      this.$set(this.formCount,'fundCodes',[])
      this.$nextTick(()=>{
        this.$refs.formCount.resetFields();
      })
    },
    // 查询
    onSubmit(flag) {
      this.tableLoading = true;
      // 消除没有值的参数
      if (flag) {
        this.formInline.pageNum = 1;
      }
      let data = { ...this.formInline };
      if (data.fundCode){
        // console.log('产品代码',data.fundCode);
        data["fundCode"] = data.fundCode.split("_")[0];
      } 

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
    // 关闭formCount
    cancel() {
      this.countDialog = false;
      this.fileList = [];
    },
    //新增数据
    addData() {
      this.bigSize = true;
      this.isUpload = true;
      this.fileList = [];
      this.isSearchData = false;
      this.countTitle = "新增";
      this.countFormList = "add";
      this.countDialog = true;
      this.operationType = 1;
      this.isChangeFile = false;
      this.saveCode = "mjAccount.insert.save";
      // 清除
      this.$nextTick(() => {
        this.$refs["formCount"].resetFields();
        this.formCount.productId = "";
        this.formCount.mjType = "1";
        this.formCount.companyName = "";
        this.formCount.productCode = "";
        this.formCount.productName = "";
        this.formCount.accoName = "";
        this.formCount.accoNo = "";
        this.formCount.accoBank = "";
        this.formCount.hvpsNo = "";
        this.formCount.remark = "";
        this.formCount.id = "";
        this.formCount.fundCodes = [];
      });
    },
    // 行编辑数据
    editData(row) {
      // console.log(row);
      this.bigSize = true;
      this.isUpload = true;
      this.fileList = [];
      this.isSearchData = false;
      this.countTitle = "编辑";
      this.countFormList = "edit";
      this.countDialog = true;
      this.operationType = 2;
      this.isChangeFile = false;
      this.rmoveFileId = [];
      this.saveCode = "mjAccount.update.save";
      this.getFileList(row.id, "mjh_file");
      this.$nextTick(() => {
        this.$refs["formCount"].resetFields();
        this.formCount.productCode = row.productId || '';
        this.formCount.productName = row.productName || '';
        this.formCount.productId = row.productCode+'_'+row.productName;
        if(row.productCode){
          this.formCount.fundCodes = [row.productCode+'_'+row.productName];
        }else{
          this.formCount.fundCodes = [];
        }
        if(row.productId=='undefined') {this.formCount.productCode=''}
        this.formCount.accoName = row.accoName || ''
        this.formCount.accoNo = row.accoNo || ''
        this.formCount.accoBank = row.accoBank || ''
        this.formCount.hvpsNo = row.hvpsNo || ''
        this.formCount.mjType = row.mjType || ''
        this.formCount.companyName = row.companyName || ''
        this.formCount.remark = row.remark || ''
        this.formCount.id = row.id;
        // console.log(this.formCount);
      });
    },
    searchData(row) {
      this.bigSize = true;
      this.isUpload = false;
      this.countTitle = "查看详情";
      this.countFormList = "edit";
      this.countDialog = true;
      this.operationType = 2;
      this.bigSize = true;
      this.fileList = [];
      this.isChangeFile = false;
      this.isSearchData = true;
      this.getFileList(row.id, "mjh_file");
      this.$nextTick(() => {
        this.$refs["formCount"].resetFields();
        this.formCount.productCode = row.productId;
        this.formCount.productName = row.productName || '';
        this.formCount.productId = row.productCode+'_'+row.productName;
        this.formCount.fundCodes = [row.productCode+'_'+row.productName];
        if(row.productId=='undefined') {this.formCount.productCode=''}
        this.formCount.accoName = row.accoName;
        this.formCount.accoNo = row.accoNo;
        this.formCount.accoBank = row.accoBank;
        this.formCount.hvpsNo = row.hvpsNo;
        this.formCount.mjType = row.mjType;
        this.formCount.companyName = row.companyName;
        this.formCount.remark = row.remark;
        this.formCount.id = row.id;
      });
    },
    //新增计算任务确认
    countSubmit() {
      if (!this.bigSize) {
        this.$message.error("上传文件大小不能超过 50MB!");
        return;
      }
      var self = this;
      this.$refs["formCount"].validate((valid, object) => {
        if (valid) {
          this.$message.closeAll();
          if (this.operationType === 1) {
            // 添加
            this.saveData();
          } else {
            // 修改
            this.updateParamSet();
            // this.upDateConfirm();
          }
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
          let data = { ...this.formCount }
          params = this.$fun.parameterStringSrc(data);
          let formData = new FormData(); // 用FormData存放上传文件
          this.countSubmit_btn = true;
          
          if(params.id){
            formData.append("id", params.id);
          }
          // if(params.productCode){
          //   formData.append("productId", params.productCode);
          // }
          // if(params.productCode){
          //   formData.append("productCode", params.productCode);
          // }
          // if(params.productName){
          //   formData.append("productName", params.productName);
          // }
          if(params.accoName){
            formData.append("accoName", params.accoName);
          }
          if(params.accoNo){
            formData.append("accoNo", params.accoNo);
          }
          if(params.accoBank){
            formData.append("accoBank", params.accoBank);
          }
          if(params.hvpsNo){
            formData.append("hvpsNo", params.hvpsNo);
          }
          if(params.mjType){
            formData.append("mjType", params.mjType);
          }
          if(params.companyName){
            formData.append("companyName", params.companyName);
          }
          if(params.remark){
            formData.append("remark", params.remark);
          }
          if(params.fundCodes){
            formData.append("fundCodes", params.fundCodes);
          }
          
          formData.append("accoType", "raise");

          if (this.fileList.length > 0) {
            for (let i = 0; i < this.fileList.length; i++) {
              let aa = this.fileList[i].raw;
              if (aa) {
                formData.append("files", aa);
              }
            }
            formData.append("relaType", "mjh_file");
          }
          pageApi
            .addDataSource(formData)
            .then((response) => {
              if (response.data.status === 200) {
                // 关闭移动指标弹框
                this.$message({
                  message: "新增成功",
                  type: "success",
                });
                this.countDialog = false;
                // 刷新列表
                this.onSubmit(true);
              } else {
                // 关闭移动指标弹框
                this.$message({
                  message: response.data.message || "新增失败",
                  type: "warning",
                });
              }
              this.countSubmit_btn = false;
            })
            .catch(() => {
              // 关闭移动指标弹框
              // this.countDialog = false;
              // console.log('aaa');
              this.cancel();
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
          // console.log('aaa');
          this.$message.info('已取消')
          // this.countDialog = true;
          this.countSubmit_btn = false;
        });
    },
    upDateConfirm(){
      this.$confirm("确定修改?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          this.removeFiles();
        })
        .catch(()=>{
          this.$message.info('已取消')
          this.countSubmit_btn = false;
        })
    },
    updateParamSet() {
      this.$confirm("确定修改?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          let params = {};
          params = this.$fun.parameterStringSrc(this.formCount);
          this.countSubmit_btn = true;
          let formData = new FormData(); //  用FormData存放上传文件

          formData.append("id", params.id);
          // formData.append("productId", params.productCode || '');
          // formData.append("productCode", params.productCode || '');
          // formData.append("productName", params.productName || '');
          formData.append("fundCodes", params.fundCodes || []);
          formData.append("accoName", params.accoName);
          formData.append("accoNo", params.accoNo);
          formData.append("accoBank", params.accoBank);
          formData.append("hvpsNo", params.hvpsNo);
          formData.append("mjType", params.mjType);
          formData.append("companyName", params.companyName);
          formData.append("remark", params.remark);
          formData.append("accoType", "raise");

          if (this.fileList.length > 0) {
            // for (let i = 0; i < this.fileList.length; i++) {
            //   let aa = this.fileList[i].raw;
            //   if (aa) {
            //     formData.append("files", aa);
            //   }
            // }
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
            formData.append("relaType", "mjh_file");
          }
          pageApi
            .updateDataSource(formData)
            .then((response) => {
              if (response.data.status === 200) {
                // 关闭移动指标弹框
                //  this.countDialog = false;
                this.$message.closeAll();
                this.$message({
                  message: "修改成功",
                  type: "success",
                });
                this.removeFiles();
                this.onSubmit(false);
                this.cancel();
              } else {
                // 关闭移动指标弹框
                // this.countDialog = false;
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
              // this.countDialog = false;
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
          // this.countDialog = true;
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
        // this.$message.closeAll();
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
      // // this.fileList = [];
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
<style lang='scss'>
.mjAccountWidth {
  width: 55% !important;
  // .el-form-item__content {
  //   width: 480px;
  // }
}
</style>
 <style>
.mjAccountWidth {
  width: 55% !important;
}
</style>
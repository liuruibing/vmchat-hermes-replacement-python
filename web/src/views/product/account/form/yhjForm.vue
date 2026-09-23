<template>
  <div class="yhj_form" v-loading='yhj_form_loading'>
    <div v-if="none_show"><span>未找到当前产品的账户信息。</span></div>
    <div class="forms_table_title" v-if="table_show">
      <i class="el-icon-s-data"></i>银行间债券账户列表
    </div>
    <el-table
      v-if="table_show"
      ref="multipleTable"
      :data="tableData"
      border
      stripe
      v-loading="tableLoading"
      style="width: 100%"
    >
      <!-- <el-table-column fixed type='selection' width='35'></el-table-column> -->
      <el-table-column
        prop="productCode"
        sortable="custom"
        show-overflow-tooltip
        label="产品代码"
        min-width="110"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.productCode | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="productName"
        sortable="custom"
        show-overflow-tooltip
        label="产品名称"
        min-width="110"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.productName | noDataFilter }}</span>
        </template>
      </el-table-column>
      
      <el-table-column
        prop="admittanceNo"
        sortable="custom"
        show-overflow-tooltip
        label="全国银行间债券市场准入备案通知书编号"
        min-width="270"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.admittanceNo | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="shchName"
        sortable="custom"
        show-overflow-tooltip
        label="上清所持有人账户名称"
        min-width="190"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.shchName | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="shchAccount"
        sortable="custom"
        show-overflow-tooltip
        label="上清所持有人账户账号"
        min-width="190"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.shchAccount | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="shchCapitalName"
        sortable="custom"
        show-overflow-tooltip
        label="上清所资金账户名称"
        min-width="180"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.shchCapitalName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="shchCapitalAccount"
        sortable="custom"
        show-overflow-tooltip
        label="上清所资金账户账号"
        min-width="180"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.shchCapitalAccount | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="shchCapitalBank"
        sortable="custom"
        show-overflow-tooltip
        label="上清所资金账户开户行"
        min-width="190"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.shchCapitalBank | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="shchCapitalCode"
        sortable="custom"
        show-overflow-tooltip
        label="上清所资金账户开户行行号"
        min-width="200"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.shchCapitalCode | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="shchInstName"
        sortable="custom"
        show-overflow-tooltip
        label="上清所托管机构名称"
        min-width="190"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.shchInstName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="shchInstAccount"
        sortable="custom"
        show-overflow-tooltip
        label="上清所托管账号"
        min-width="180"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.shchInstAccount | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="ccdcName"
        sortable="custom"
        show-overflow-tooltip
        label="中债登债券账户名称"
        min-width="180"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.ccdcName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="ccdcAccount"
        sortable="custom"
        show-overflow-tooltip
        label="中债登债券账户账号"
        min-width="180"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.ccdcAccount | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="ccdcCapitalName"
        sortable="custom"
        show-overflow-tooltip
        label="中债登资金账户名称"
        min-width="190"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.ccdcCapitalName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="ccdcCapitalAccount"
        sortable="custom"
        show-overflow-tooltip
        label="中债登资金账户账号"
        min-width="190"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.ccdcCapitalAccount | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="ccdcCapitalBank"
        sortable="custom"
        show-overflow-tooltip
        label="中债登资金账户开户行"
        min-width="190"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.ccdcCapitalBank | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="ccdcCapitalCode"
        sortable="custom"
        show-overflow-tooltip
        label="中债登资金账户开户行行号"
        min-width="200"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.ccdcCapitalCode | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="ccdchInstName"
        sortable="custom"
        show-overflow-tooltip
        label="中债登托管机构名称"
        min-width="180"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.ccdchInstName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="ccdcInstAccount"
        sortable="custom"
        show-overflow-tooltip
        label="中债登托管账号"
        min-width="170"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.ccdcInstAccount | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="investTypeNames"
        sortable="custom"
        show-overflow-tooltip
        label="投资类型"
        min-width="110"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.investTypeNames | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        fixed="right"
        min-width="100"
        align="center"
      >
        <template slot-scope="scope">
          <el-button type="primary" size="small" @click="searchData(scope.row)">查看详情</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-container v-if="form_show && !preview_show">
        <el-main class="mainBox">
          <div style="overflow: hidden;padding: 15px;">
            <span @click="close_form" style="font-size: 20px;float: right;cursor: pointer;"><i class="el-icon-close"></i></span>
          </div>
          <el-form
            ref="formCount"
            :model="formCount"
            label-position="right"
          >
            <el-row>
              <el-col :span="12">
                <el-form-item
                  label=" 产品名称"
                  prop="productId"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <!-- <select-table v-model="formCount.productId" @sendDataObj='dataObj' v-if="!isSearchData" ref="relation"></select-table> -->
                  <el-input v-model="formCount.productId" disabled ></el-input>
                </el-form-item>
                <el-form-item
                  label="上清所持有人账户名称"
                  prop="shchName"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    type="text"
                    v-model.trim="formCount.shchName"
                    clearable
                    ref="shchName"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="上清所持有人账户账号"
                  prop="shchAccount"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    type="text"
                    v-model.trim="formCount.shchAccount"
                    clearable
                    ref="shchAccount"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="上清所资金账户名称"
                  prop="shchCapitalName"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    type="text"
                    v-model.trim="formCount.shchCapitalName"
                    clearable
                    ref="shchCapitalName"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="上清所资金账户账号"
                  prop="shchCapitalAccount"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    type="text"
                    v-model.trim="formCount.shchCapitalAccount"
                    clearable
                    ref="shchCapitalAccount"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="上清所资金账户开户行"
                  prop="shchCapitalBank"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    type="text"
                    v-model.trim="formCount.shchCapitalBank"
                    clearable
                    ref="shchCapitalBank"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="上清所资金账户开户行号"
                  prop="shchCapitalCode"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    type="text"
                    v-model.trim="formCount.shchCapitalCode"
                    clearable
                    ref="shchCapitalCode"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="上清所托管机构名称"
                  prop="shchInstName"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    type="text"
                    v-model.trim="formCount.shchInstName"
                    clearable
                    ref="shchInstName"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="上清所托管账号"
                  prop="shchInstAccount"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    type="text"
                    v-model.trim="formCount.shchInstAccount"
                    clearable
                    ref="shchInstAccount"
                  ></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item
                  label="产品代码"
                  prop="productCode"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="100"
                    type="text"
                    disabled
                    v-model.trim="formCount.productCode"
                    clearable
                    ref="productCode"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="中债登债券账户名称"
                  prop="ccdcName"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    type="text"
                    v-model.trim="formCount.ccdcName"
                    clearable
                    ref="ccdcName"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="中债登债券账户账号"
                  prop="ccdcAccount"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    type="text"
                    v-model.trim="formCount.ccdcAccount"
                    clearable
                    ref="ccdcAccount"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="中债登资金账户名称"
                  prop="ccdcCapitalName"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    type="text"
                    v-model.trim="formCount.ccdcCapitalName"
                    clearable
                    ref="ccdcCapitalName"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="中债登资金账户账号"
                  prop="ccdcCapitalAccount"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    type="text"
                    v-model.trim="formCount.ccdcCapitalAccount"
                    clearable
                    ref="ccdcCapitalAccount"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="中债登资金账户开户行"
                  prop="ccdcCapitalBank"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    type="text"
                    v-model.trim="formCount.ccdcCapitalBank"
                    clearable
                    ref="ccdcCapitalBank"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="中债登资金账户开户行号"
                  prop="ccdcCapitalCode"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    type="text"
                    v-model.trim="formCount.ccdcCapitalCode"
                    clearable
                    ref="ccdcCapitalCode"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="中债登托管机构名称"
                  prop="ccdchInstName"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    type="text"
                    v-model.trim="formCount.ccdchInstName"
                    clearable
                    ref="ccdchInstName"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="中债登托管账号"
                  prop="ccdcInstAccount"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    type="text"
                    v-model.trim="formCount.ccdcInstAccount"
                    clearable
                    ref="ccdcInstAccount"
                  ></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="24">
                <el-form-item
                  label="全国银行间债券市场准入备案通知书编号"
                  prop="admittanceNo"
                  class="mb20"
                  label-width="280px"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    type="text"
                    v-model.trim="formCount.admittanceNo"
                    clearable
                    ref="admittanceNo"
                  ></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="24">
                <el-form-item
                  label="备注"
                  prop="remark"
                  class="mb20"
                  label-width="100px"
                >
                  <el-input
                    :disabled="isSearchData"
                    type="textarea"
                    :autosize='{ minRows: 4}'
                    maxlength="166"
                    placeholder="请输入备注"
                    v-model="formCount.remark"
                    ref="remark"
                  >
                  </el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="24">
                <el-form-item
                  label="投资工具"
                  prop="investTypeDimsTr"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <!-- <el-checkbox
                    v-model="checkAll"
                    disabled
                    >全选</el-checkbox
                  > -->
                  <div style="margin: 15px 0"></div>
                  <el-checkbox-group
                    v-model="checkfundInvestArea"
                  >
                    <el-checkbox
                      disabled
                      v-for="(group, index) in fundInvestArea"
                      :key="index"
                      :label="group.dimCde"
                      >{{ group.dimNme }}</el-checkbox
                    >
                  </el-checkbox-group>
                </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col>
                <el-form-item
                  label="账户资料上传"
                  prop="file"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-upload
                    class="upload-demo"
                    ref="upload"
                    :disabled='isSearchData'
                    :headers="hearders"
                    :action="fileUploadUrl"
                    :on-preview="downFile"
                    :file-list="fileList"
                    :auto-upload="false"
                  >
                    <el-button
                      slot="trigger"
                      
                      type="primary"
                      v-show="!isSearchData"
                      >浏览</el-button
                    >
                  </el-upload>
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
        </el-main>
      </el-container>
      <div v-if="preview_show" style="height:100%;padding: 0 20px">
      <p class="yulan_title"> <span class="yulan_title_name">附件预览</span><span style="font-size:20px;color:#000;cursor: pointer;"><i @click="closePreview" class="el-icon-close"></i></span> </p>
      <PdfPreview :urlArr='fileList' :PreviewFileId="PreviewFileId" style="width:100%;height:100%" ref="PdfPreview"></PdfPreview>
    </div>
  </div>
</template>

<script>
import PdfPreview from '@/components/PdfPreview'
import pageApi from "@/api/product/yhAccount";
import commonApi from "@/api/common";
export default {
  components:{PdfPreview},
  data(){
    return{
      tableData:[],
      tableLoading:false,
      isSearchData:true,
      table_show:false,
      form_show:false,
      none_show:false,
      formLabelWidth:'200px',
      formCount: {
        productId: "", //产品名称
        productCode: "", //产品代码
        admittanceNo: "", //全国银行间债券市场准入备案通知书编号
        investTypeDimsTr: "", //投资工具
        shchName: "", //上清所持有人账户名称
        ccdcName: "", //中债登债券账户名称
        shchAccount: "", //上清所持有人账户账号
        ccdcAccount: "", //中债登债券账户账号
        shchCapitalName: "", //上清所资金账户名称
        ccdcCapitalName: "", //中债登资金账户名称

        ccdcCapitalCode: "",
        shchCapitalAccount: "", //上清所资金账户账号
        ccdcCapitalAccount: "", //中债登资金账户账号
        shchCapitalBank: "", //上清所资金账户开户行
        ccdcCapitalBank: "", //中债登资金账户开户行
        shchCapitalCode: "", //上清所资金账户开户行号
        shchInstName: "", //上清所托管机构名称
        ccdchInstName: "", //中债登托管机构名称
        shchInstAccount: "", //上清所托管账号
        ccdcInstAccount: "", //中债登托管账号
        remark: "", //备注
      },
      fundInvestArea:[],
      checkfundInvestArea:[],
      hearders:{},
      fileUploadUrl:"",
      fileList:[],
      yhj_form_loading:false,
      preview_show:false,
      PreviewFileId:''
    }
  },
  mounted(){
    this.getEdims();
  },
  methods:{
    init(val){
      this.preview_show = false;
      this.form_show = false;
      this.yhj_form_loading = true;
      this.getTableList(val)
    },
    getTableList(data){
      this.tableData = [];
      this.tableLoading = true;
      let fundCode = data;
      let params = {
        fundCode:fundCode,
        pageSize: 500,
        pageNum: 1
      }
      pageApi
          .getDataSourceList(params)
          .then((response) => {
            this.yhj_form_loading = false;
            if (response.data.status === 200) {
              this.tableData = response.data.data.list;
              if(this.tableData.length){
                this.table_show = true;
                this.none_show = false;
              }else{
                this.table_show = false;
                this.none_show = true;
              }
            } else {
              this.tableData = [];
              this.table_show = false;
            }
            this.tableLoading = false;
          })
          .catch(() => {
            this.tableData = [];
            this.tableLoading = false;
            this.table_show = false;
            this.yhj_form_loading = false;
          });
    },
    searchData(row){
      this.table_show = false;
      this.form_show = true;
      this.getFileList(row.id,"yh_file");
      this.$nextTick(() => {
        this.$refs["formCount"].resetFields();
        this.formCount.productId = row.productName;
        this.formCount.productCode = row.productCode;
        this.formCount.admittanceNo = row.admittanceNo;
        this.formCount.investTypeDimsTr = row.investTypeDimsTr;
        this.formCount.shchName = row.shchName;
        this.formCount.ccdcName = row.ccdcName;
        this.formCount.shchAccount = row.shchAccount;
        this.formCount.ccdcAccount = row.ccdcAccount;
        this.formCount.shchCapitalName = row.shchCapitalName;
        this.formCount.ccdcCapitalName = row.ccdcCapitalName;

        this.formCount.shchCapitalAccount = row.shchCapitalAccount;
        this.formCount.ccdcCapitalAccount = row.ccdcCapitalAccount;
        this.formCount.shchCapitalBank = row.shchCapitalBank;
        this.formCount.ccdcCapitalBank = row.ccdcCapitalBank;
        this.formCount.shchCapitalCode = row.shchCapitalCode;
        this.formCount.shchInstName = row.shchInstName;
        this.formCount.ccdchInstName = row.ccdchInstName;
        this.formCount.shchInstAccount = row.shchInstAccount;
        this.formCount.ccdcCapitalCode = row.ccdcCapitalCode;
        this.formCount.ccdcInstAccount = row.ccdcInstAccount;
        this.formCount.remark = row.remark;
        this.formCount.id = row.id;
        this.checkAll = false;
        this.checkfundInvestArea = [];
        if (row.investTypeDims) {
          let arr = row.investTypeDims.split(",");
          if (arr.length === this.fundInvestArea.length) {
            this.checkAll = true;
          }

          this.checkfundInvestArea = arr;
        }
      });
      
    },
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
            // this.rmoveFileId = [ ...this.fileList ]
          } else {
            this.fileList = [];
            // this.rmoveFileId = []
            this.$message.error("查询详情附件信息失败");
          }
        })
        .catch(() => {
          this.$message.error("查询详情附件信息失败");
        });
    },
    getEdims() {
      commonApi
        .getTransferType(280)
        .then((res) => {
          if (res.data) {
            this.fundInvestArea = res.data;
          } else {
            this.fundInvestArea = [];
            this.$message.error("查询投资工具失败");
          }
        })
        .catch(() => {
          this.$message.error("查询投资工具失败");
        });
    },
    close_form(){
      this.table_show = true;
      this.form_show = false;
    },
    downFile(file) {
      if(file.id){
        this.PreviewFileId = file.id;
        this.preview_show=true;
      }
    },
    closePreview(){
      this.preview_show = false;
      this.$notify.closeAll();
    }
  }
}
</script>

<style lang="scss">
  .yhj_form{
    // min-height: 50px;
    height: 100%;
    .el-form-item__content{
      min-width: 0 !important;
    }
  }
</style>
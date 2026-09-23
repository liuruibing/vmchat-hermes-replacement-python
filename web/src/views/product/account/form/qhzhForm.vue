<template>
  <div class="qhzh_form" v-loading="qhzh_form_loading">
    <div v-if="none_show"><span>未找到当前产品的账户信息。</span></div>
    <div class="forms_table_title" v-if="table_show">
      <i class="el-icon-s-data"></i>期货账户列表
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
        min-width="120"
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
        min-width="120"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.productName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="futureCode"
        sortable="custom"
        show-overflow-tooltip
        label="统一开户编码"
        min-width="160"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.futureCode | noDataFilter }}</span>
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
          <span>{{ scope.row.openStruc | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="openExchange"
        sortable="custom"
        show-overflow-tooltip
        label="开户营业部"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.openExchange | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="statusName"
        sortable="custom"
        show-overflow-tooltip
        label="账户状态"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.statusName == 'opening'">正在开户</span>
          <span v-else-if="scope.row.statusName == 'trading'">正常交易</span>
          <span v-else-if="scope.row.statusName == 'closing'">正在销户</span>
          <span v-else-if="scope.row.statusName == 'closed'">已销户</span>
          <span v-else>{{ scope.row.statusName | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="capitalAccount"
        sortable="custom"
        show-overflow-tooltip
        label="资金账户"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.capitalAccount | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="tradeFee"
        sortable="custom"
        show-overflow-tooltip
        label="交易费用"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.tradeFee | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="tradeAuth"
        sortable="custom"
        show-overflow-tooltip
        label="已开通交易权限"
        min-width="150"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.tradeAuth | noDataFilter }}</span>
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
            :rules="countRules"
            label-position="right"
          >
            <div class="forms_table_title">
              <i class="el-icon-s-data"></i>账户基本信息
            </div>
            <el-row>
              <el-col :span="12">
                <el-form-item
                  label="产品名称"
                  prop="productId"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <select-table v-model="formCount.productId" @sendDataObj='dataObj' v-if="!isSearchData" ref="relation"></select-table>
                  <el-input v-model="formCount.productId" disabled v-else></el-input>
                </el-form-item>
                <el-form-item
                  label="账户状态"
                  prop="status"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-select
                    style="width: 100%"
                    :disabled="isSearchData"
                    v-model="formCount.status"
                    clearable
                    filterable
                    placeholder="请选择"
                    ref="status"
                  >
                    <el-option
                      v-for="item in statusArr"
                      :key="item.value"
                      :label="item.name"
                      :value="item.value"
                    >
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item
                  label="资金账户"
                  prop="capitalAccount"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    v-model.trim="formCount.capitalAccount"
                    clearable
                    ref="capitalAccount"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="已开通交易权限"
                  prop="tradeAuth"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="333"
                    :disabled="isSearchData"
                    v-model.trim="formCount.tradeAuth"
                    clearable
                    ref="tradeAuth"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="保密协议签署状态"
                  prop="ndaSigned"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-radio
                    :disabled="isSearchData"
                    v-model="formCount.ndaSigned"
                    label="0"
                    >未签署</el-radio
                  >
                  <el-radio
                    :disabled="isSearchData"
                    v-model="formCount.ndaSigned"
                    label="1"
                    >已签署</el-radio
                  >
                </el-form-item>
                <el-form-item
                  label="开户日期"
                  prop="openDate"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-date-picker
                    style="width: 100%"
                    :disabled="isSearchData"
                    v-model="formCount.openDate"
                    type="date"
                    @change="isSelect"
                    value-format="yyyy-MM-dd"
                    placeholder="选择日期"
                    ref="openDate"
                  >
                  </el-date-picker>
                </el-form-item>
                <el-form-item
                  label="销户日期"
                  prop="closeDate"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-date-picker
                    style="width: 100%"
                    @change="isSelect"
                    :disabled="isSearchData"
                    v-model="formCount.closeDate"
                    type="date"
                    value-format="yyyy-MM-dd"
                    placeholder="选择日期"
                    ref="closeDate"
                  >
                  </el-date-picker>
                </el-form-item>
                <el-form-item
                  label="保证金监控中心账号"
                  prop="srfsAccount"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    v-model.trim="formCount.srfsAccount"
                    clearable
                    ref="srfsAccount"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="资金调拨人"
                  prop="transfer"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    v-model.trim="formCount.transfer"
                    clearable
                    ref="transfer"
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
                    maxlength="30"
                    disabled
                    v-model.trim="formCount.productCode"
                    clearable
                    ref="productCode"
                  ></el-input>
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
                    ref="futureCode"
                  ></el-input>
                </el-form-item>

                <el-form-item
                  label="交易费用"
                  prop="tradeFee"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    :disabled="isSearchData"
                    v-model.trim="formCount.tradeFee"
                    clearable
                    maxlength="132"
                    ref="tradeFee"
                  ></el-input>
                </el-form-item>

                <el-form-item
                  label="银期关联情况"
                  prop="bfRelated"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-radio
                    :disabled="isSearchData"
                    v-model="formCount.bfRelated"
                    label="0"
                    >未关联</el-radio
                  >
                  <el-radio
                    :disabled="isSearchData"
                    v-model="formCount.bfRelated"
                    label="1"
                    >已关联</el-radio
                  >
                </el-form-item>

                <el-form-item
                  label="经纪服务协议签署状态"
                  prop="bsaSigned"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-radio
                    :disabled="isSearchData"
                    v-model="formCount.bsaSigned"
                    label="0"
                    >未签署</el-radio
                  >
                  <el-radio
                    :disabled="isSearchData"
                    v-model="formCount.bsaSigned"
                    label="1"
                    >已签署</el-radio
                  >
                </el-form-item>

                <el-form-item
                  label="开户原因"
                  prop="openReason"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="333"
                    :disabled="isSearchData"
                    v-model.trim="formCount.openReason"
                    clearable
                    ref="openReason"
                  ></el-input>
                </el-form-item>

                <el-form-item
                  label="销户原因"
                  prop="closeReason"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="333"
                    :disabled="isSearchData"
                    v-model.trim="formCount.closeReason"
                    clearable
                    ref="closeReason"
                  ></el-input>
                </el-form-item>

                <el-form-item
                  label="指定下单人"
                  prop="single"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    v-model.trim="formCount.single"
                    clearable
                    ref="single"
                  ></el-input>
                </el-form-item>

                <el-form-item
                  label="结算确认人"
                  prop="confirmer"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    v-model.trim="formCount.confirmer"
                    clearable
                    ref="confirmer"
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
            <div class="forms_table_title">
              <i class="el-icon-s-data"></i>联系人信息
            </div>
            <el-row>
              <el-col :span="12">
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
                <el-form-item
                  label="营业部地址"
                  prop="exchangeAddress"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="333"
                    :disabled="isSearchData"
                    v-model.trim="formCount.exchangeAddress"
                    clearable
                    ref="exchangeAddress"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="对接人联系电话"
                  prop="brokerPhone"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    v-model.trim="formCount.brokerPhone"
                    clearable
                    ref="brokerPhone"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="出入金联系电话"
                  prop="cashPhone"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    v-model.trim="formCount.cashPhone"
                    clearable
                    ref="cashPhone"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="账户维护经办人"
                  prop="accountOperator"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    v-model.trim="formCount.accountOperator"
                    clearable
                    ref="accountOperator"
                  ></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item
                  label="开户营业部"
                  prop="openExchange"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    v-model.trim="formCount.openExchange"
                    clearable
                    ref="openExchange"
                  ></el-input>
                </el-form-item>

                <el-form-item
                  label="营业部对接人"
                  prop="exchangeBroker"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    v-model.trim="formCount.exchangeBroker"
                    clearable
                    ref="exchangeBroker"
                  ></el-input>
                </el-form-item>

                <el-form-item
                  label="出入金联系人"
                  prop="cashContact"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    v-model.trim="formCount.cashContact"
                    clearable
                    ref="cashContact"
                  ></el-input>
                </el-form-item>

                <el-form-item
                  label="开户经办人"
                  prop="openOperator"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    v-model.trim="formCount.openOperator"
                    clearable
                    ref="openOperator"
                  ></el-input>
                </el-form-item>

                <el-form-item
                  label="销户经办人"
                  prop="closeOperator"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    v-model.trim="formCount.closeOperator"
                    clearable
                    ref="closeOperator"
                  ></el-input>
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
import pageApi from "@/api/product/qhAccount";
import commonApi from "@/api/common";
export default {
  components:{PdfPreview},
  data(){
    return{
      tableData:[],
      tableLoading:false,
      table_show:false,
      form_show:false,
      none_show:false,
      formCount: {
        productId: "", //产品名称
        productCode: "", //产品代码
        status: "", //账户状态
        futureCode: "", //统一开户编码
        capitalAccount: "", //资金账户
        tradeFee: "", //A股交易费率
        szaAccount: "", //深市A股账号
        shaAccount: "", //沪市A股账号
        tradeAuth: "", //已开通交易权限
        bfRelated: "", //银证关联情况
        ndaSigned: "", //保密协议签署状态
        bsaSigned: "", //经纪服务协议签署状态
        openDate: "", //开户日期
        openReason: "", //开户原因
        closeDate: "", //销户日期
        closeReason: "", //销户原因
        openStruc: "", //开户机构
        openExchange: "", //开户营业部
        exchangeAddress: "", //营业部地址
        exchangeBroker: "", //营业部对接人
        brokerPhone: "", //对接人联系电话
        cashContact: "", //出入金联系人
        cashPhone: "", //出入金联系电话
        openOperator: "", //开户经办人
        accountOperator: "", //账户维护经办人
        closeOperator: "", //销户经办人
        srfsAccount: "", //保证金监控中心账号
        single: "", //指定下单人
        transfer: "", //资金调拨人
        confirmer: "", //结算确认人
        remark: "",
      },
      formLabelWidth: "150px",
      countRules:{},
      isSearchData:true,
      hearders:{},
      fileUploadUrl:'',
      fileList:[],
      typeArr:[],
      isUpload:false,
      validRules:{},
      tableDataEdit:[],
      statusArr:[],
      qhzh_form_loading:false,
      preview_show:false,
      PreviewFileId:''
    }
  },
  methods:{
    init(val){
      // console.log(val);
      this.preview_show = false;
      this.form_show = false;
      this.qhzh_form_loading = true;
      this.getTableList(val);
    },
    selectChangemj(){},
    downFile(file) {
      if(file.id){
        this.PreviewFileId = file.id;
        this.preview_show=true;
      }
    },
    handleError(){},
    handleRemove(){},
    handleSuccess(){},
    handleChange(){},
    isSelect(){},
    close_form(){
      this.table_show = true;
      this.form_show = false;
    },
    closePreview(){
      this.preview_show = false;
      this.$notify.closeAll();
    },
    searchData(row){
      this.table_show = false;
      this.form_show = true;
      // console.log(row);
      this.getFileList(row.id, "qh_file");
      this.$nextTick(() => {
        this.$refs["formCount"].resetFields();
        this.formCount.productId = row.productName || '';
        this.formCount.productCode = row.productCode || '';
        this.formCount.status = row.status || '';
        this.formCount.futureCode = row.futureCode || '';
        this.formCount.capitalAccount = row.capitalAccount || '';
        this.formCount.tradeFee = row.tradeFee || '';
        this.formCount.szaAccount = row.szaAccount || '';
        this.formCount.shaAccount = row.shaAccount || '';
        this.formCount.tradeAuth = row.tradeAuth || '';
        this.formCount.bfRelated = row.bfRelated || '';
        this.formCount.ndaSigned = row.ndaSigned || '';
        this.formCount.bsaSigned = row.bsaSigned || '';
        this.formCount.openDate = row.openDateStr || '';
        this.formCount.openReason = row.openReason || '';
        this.formCount.closeDate = row.closeDateStr || '';
        this.formCount.closeReason = row.closeReason || '';
        this.formCount.openStruc = row.openStruc || '';
        this.formCount.openExchange = row.openExchange || '';
        this.formCount.exchangeAddress = row.exchangeAddress || '';
        this.formCount.exchangeBroker = row.exchangeBroker || '';
        this.formCount.brokerPhone = row.brokerPhone || '';
        this.formCount.cashContact = row.cashContact || '';
        this.formCount.cashPhone = row.cashPhone || '';
        this.formCount.openOperator = row.openOperator || '';
        this.formCount.accountOperator = row.accountOperator || '';
        this.formCount.closeOperator = row.closeOperator || '';
        this.formCount.srfsAccount = row.srfsAccount || '';
        this.formCount.single = row.single || '';
        this.formCount.transfer = row.transfer || '';
        this.formCount.confirmer = row.confirmer || '';
        this.formCount.id = row.id || '';
        this.formCount.remark = row.remark || '';
      });
    },
    getFileList(relaId, relaType){
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
            this.qhzh_form_loading = false;
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
            this.qhzh_form_loading = false;
          });
    },
  }
}
</script>

<style lang="scss">
  .qhzh_form{
    // min-height: 50px;
    height: 100%;
    .el-form-item__content{
      min-width: 0 !important;
    }
  }
</style>
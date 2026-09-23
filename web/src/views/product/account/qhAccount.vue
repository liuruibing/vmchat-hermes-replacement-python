<template>
  <div>
    <el-form
      :inline="true"
      :rules="rulesQh"
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
            <el-form-item label="资金账户" prop="capitalAccount">
              <el-input
                maxlength="100"
                @keydown.enter.native="onSubmit()"
                v-model.trim="formInline.capitalAccount"
                clearable
                placeholder="请填写资金账户"
                size="small"
              ></el-input>
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
              v-btn="'qhAccount.insert.info'"
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
      <i class="el-icon-s-data"></i>期货账户列表
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
        min-width="160"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.futureCode | noDataFilter }}</span>
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
        prop="openExchange"
        sortable="custom"
        show-overflow-tooltip
        label="开户营业部"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.openExchange | noDataFilter }}</span>
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
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">
            <span v-if="scope.row.statusName == 'opening'">正在开户</span>
            <span v-else-if="scope.row.statusName == 'trading'">正常交易</span>
            <span v-else-if="scope.row.statusName == 'closing'">正在销户</span>
            <span v-else-if="scope.row.statusName == 'closed'">已销户</span>
            <span v-else>{{ scope.row.statusName | noDataFilter }}</span>
          </span>
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
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.capitalAccount | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="tradeFee"
        sortable="custom"
        show-overflow-tooltip
        label="交易费用说明"
        min-width="130"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.tradeFee | noDataFilter }}</span>
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
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.tradeAuth | noDataFilter }}</span>
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
            v-btn="'qhAccount.update.save'"
            v-if="scope.row.approvalStatus=='1'?false:true"
            type="primary"
            size="small"
            @click="editData(scope.row)"
            >编辑</el-button
          >
          <el-button
            v-btn="'qhAccount.delete.info'"
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
      customClass="qhAccountWidth"
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
                  label="产品"
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
                  label="资金账户名称"
                  prop="accoName"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    v-model.trim="formCount.accoName"
                    clearable
                    ref="accoName"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="资金账户账号"
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
                  style="visibility:hidden;"
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
                  label="交易费用说明"
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
                  label="支付系统号"
                  prop="hvpsNo"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    :disabled="isSearchData"
                    v-model.trim="formCount.hvpsNo"
                    clearable
                    maxlength="66"
                    ref="hvpsNo"
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
import pageApi from "@/api/product/qhAccount";
import { ecmRules } from "@/api/product/cemJudge";
import modelFileValidate from '@/mixinsModel/file-validate'
export default {
  name: "tgAccount",
  mixins: [modelFileValidate],
  components: { Pagination, selectTable },
  data() {
    const openDateValid = (rule, value, callback) => {
      let openDate = this.formCount.openDate;
      let closeDate = this.formCount.closeDate;
      if (openDate && closeDate) {
        if (openDate >= closeDate) {
          callback(new Error("日期选择错误"));
        } else callback();
      } else callback();
    };
    return {
      isContainerRush: true,
      formInline: {
        fundCode: "",
        openStruc: "",
        capitalAccount: "",
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
        productName:"", 
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
        accoName: "", //资金账户名称
        hvpsNo: "", //支付系统号
      },
      // 操作类型 1、添加 2、编辑
      operationType: 1,
      //  查询校验
      rulesQh: {
        openStruc: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message:this.$regularValidator.empty().msg,
          },
        ],
        capitalAccount: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母或者数字",
          },
        ],
      },
      // 弹窗验证规则
      countRules: {
        closeDate: {
          required: false,
          message: "",
          validator: openDateValid,
          trigger: "change",
        },
        openDate: {
          required: false,
          message: "",
          validator: openDateValid,
          trigger: "change",
        },
        productId: [
          {
            required: true,
            type: "string",
            message: "请选择产品",
            trigger: "change",
          },
        ],
        brokerPhone: [
          {
            required: false,
            trigger: "change",
            pattern: /^((\d{3,4}-\d{7,8})|(1[3456789]\d{9}))$/,
            message: "输入电话格式不正确",
          },
        ],
        cashPhone: [
          {
            required: false,
            trigger: "change",
            pattern: /^((\d{3,4}-\d{7,8})|(1[3456789]\d{9}))$/,
            message: "输入电话格式不正确",
          },
        ],
        //  /^((0){1}(\.\d{0,2})?|1)$/      /^[0-9]+(.[0-9]{1,5})?$/
        tradeFee: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: '',
            message: "",
          },
        ],
        futureCode: [
          { required: true, type: "string", message: "请输入统一开户编码" },
          {
            trigger: "change",
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母或者数字",
          },
        ],
        capitalAccount: [
          { required: true, type: "string", message: "请输入资金账户" },
          {
            trigger: "change",
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母或者数字",
          },
        ],
        tradeAuth: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message:this.$regularValidator.empty().msg,
          },
        ],
        ndaSigned: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message:this.$regularValidator.empty().msg,
          },
        ],
        openReason: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message:this.$regularValidator.empty().msg,
          },
        ],
        closeReason: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message:this.$regularValidator.empty().msg,
          },
        ],
        srfsAccount: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母或者数字",
          },
        ],
        single: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message:this.$regularValidator.empty().msg,
          },
        ],
        transfer: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message:this.$regularValidator.empty().msg,
          },
        ],
        confirmer: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message:this.$regularValidator.empty().msg,
          },
        ],
        remark: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message:this.$regularValidator.empty().msg,
          },
        ],
        openStruc: [
          { required: true, type: "string", message: "请输入开户机构" },
          {
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message:this.$regularValidator.empty().msg,
          },
        ],
        openExchange: [
          { required: true, type: "string", message: "请输入开户营业部" },
          {
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message:this.$regularValidator.empty().msg,
          },
        ],
        exchangeAddress: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message:this.$regularValidator.empty().msg,
          },
        ],
        exchangeBroker: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message:this.$regularValidator.empty().msg,
          },
        ],
        cashContact: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message:this.$regularValidator.empty().msg,
          },
        ],
        openOperator: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message:this.$regularValidator.empty().msg,
          },
        ],
        accountOperator: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message:this.$regularValidator.empty().msg,
          },
        ],
        closeOperator: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message:this.$regularValidator.empty().msg,
          },
        ],
        hvpsNo: [
          {required: false,trigger:"change",pattern: /^[a-zA-Z0-9]+$/,message:"请输入字母或者数字"}
        ],
        accoName: [
          {required: true,trigger:"change",message:"请输入资金账户名称"}
        ]
      },
      formLabelWidth: "170px",
      countSubmit_btn: false,
      accountCodes: [], //产品数组
      tableDataEdit: [],
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
      statusArr: [
        { name: "正在开户", value: "opening" },
        { name: "正常交易", value: "trading" },
        { name: "正在销户", value: "closing" },
        { name: "已销户", value: "closed" },
      ],
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
    isSelect() {
      this.$refs.formCount.clearValidate();
    },
    //  dialog关闭初始化
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
        // this.$message.closeAll();
        if (!valid) return this.$message.warning("请输入正确的查询条件 !");
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

      this.saveCode = "qhAccount.insert.save";
      // 清除
      this.$nextTick(() => {
        this.$refs["formCount"].resetFields();
        this.formCount.productId = "";
        this.formCount.productCode = "";
        this.formCount.productName = "";
        this.formCount.status = "";
        this.formCount.futureCode = "";
        this.formCount.capitalAccount = "";
        this.formCount.tradeFee = "";
        this.formCount.szaAccount = "";
        this.formCount.shaAccount = "";
        this.formCount.tradeAuth = "";
        this.formCount.bfRelated = "";
        this.formCount.ndaSigned = "";
        this.formCount.bsaSigned = "";
        this.formCount.openDate = "";
        this.formCount.openReason = "";
        this.formCount.closeDate = "";
        this.formCount.closeReason = "";
        this.formCount.openStruc = "";
        this.formCount.openExchange = "";
        this.formCount.exchangeAddress = "";
        this.formCount.exchangeBroker = "";
        this.formCount.brokerPhone = "";
        this.formCount.cashContact = "";
        this.formCount.cashPhone = "";
        this.formCount.openOperator = "";
        this.formCount.accountOperator = "";
        this.formCount.closeOperator = "";

        this.formCount.srfsAccount = "";
        this.formCount.single = "";
        this.formCount.transfer = "";
        this.formCount.confirmer = "";
        this.formCount.id = "";
        this.formCount.remark = "";
        this.formCount.accoName = "";
        this.formCount.hvpsNo = "";
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
      this.saveCode = "qhAccount.update.save";

      this.getFileList(row.id, "qh_file");

      this.$nextTick(() => {
        this.$refs["formCount"].resetFields();
        this.formCount.productId = row.productCode+'_'+row.productName;
        this.formCount.productCode = row.productCode;
        this.formCount.productName = row.productName || '';
        this.formCount.status = row.status;
        this.formCount.futureCode = row.futureCode;
        this.formCount.capitalAccount = row.capitalAccount;
        this.formCount.tradeFee = row.tradeFee;
        this.formCount.szaAccount = row.szaAccount;
        this.formCount.shaAccount = row.shaAccount;
        this.formCount.tradeAuth = row.tradeAuth;
        this.formCount.bfRelated = row.bfRelated;
        this.formCount.ndaSigned = row.ndaSigned;
        this.formCount.bsaSigned = row.bsaSigned;
        this.formCount.openDate = row.openDateStr;
        this.formCount.openReason = row.openReason;
        this.formCount.closeDate = row.closeDateStr;
        this.formCount.closeReason = row.closeReason;
        this.formCount.openStruc = row.openStruc;
        this.formCount.openExchange = row.openExchange;
        this.formCount.exchangeAddress = row.exchangeAddress;
        this.formCount.exchangeBroker = row.exchangeBroker;
        this.formCount.brokerPhone = row.brokerPhone;
        this.formCount.cashContact = row.cashContact;
        this.formCount.cashPhone = row.cashPhone;
        this.formCount.openOperator = row.openOperator;
        this.formCount.accountOperator = row.accountOperator;
        this.formCount.closeOperator = row.closeOperator;
        this.formCount.srfsAccount = row.srfsAccount;
        this.formCount.single = row.single;
        this.formCount.transfer = row.transfer;
        this.formCount.confirmer = row.confirmer;
        this.formCount.id = row.id;
        this.formCount.remark = row.remark;
        this.formCount.accoName = row.accoName || '';
        this.formCount.hvpsNo = row.hvpsNo || '';
      });
    },
    searchData(row) {
      this.bigSize = true;
      this.countTitle = "查看详情";
      this.countFormList = "edit";
      this.countDialog = true;
      this.operationType = 2;
      this.isChangeFile = false;
      this.isSearchData = true;
      this.getFileList(row.id, "qh_file");
      this.$nextTick(() => {
        this.$refs["formCount"].resetFields();
        this.formCount.productId = row.productCode+'_'+row.productName;
        this.formCount.productCode = row.productCode || '';
        this.formCount.productName = row.productName || '';
        this.formCount.status = row.status;
        this.formCount.futureCode = row.futureCode;
        this.formCount.capitalAccount = row.capitalAccount;
        this.formCount.tradeFee = row.tradeFee;
        this.formCount.szaAccount = row.szaAccount;
        this.formCount.shaAccount = row.shaAccount;
        this.formCount.tradeAuth = row.tradeAuth;
        this.formCount.bfRelated = row.bfRelated;
        this.formCount.ndaSigned = row.ndaSigned;
        this.formCount.bsaSigned = row.bsaSigned;
        this.formCount.openDate = row.openDateStr;
        this.formCount.openReason = row.openReason;
        this.formCount.closeDate = row.closeDateStr;
        this.formCount.closeReason = row.closeReason;
        this.formCount.openStruc = row.openStruc;
        this.formCount.openExchange = row.openExchange;
        this.formCount.exchangeAddress = row.exchangeAddress;
        this.formCount.exchangeBroker = row.exchangeBroker;
        this.formCount.brokerPhone = row.brokerPhone;
        this.formCount.cashContact = row.cashContact;
        this.formCount.cashPhone = row.cashPhone;
        this.formCount.openOperator = row.openOperator;
        this.formCount.accountOperator = row.accountOperator;
        this.formCount.closeOperator = row.closeOperator;
        this.formCount.srfsAccount = row.srfsAccount;
        this.formCount.single = row.single;
        this.formCount.transfer = row.transfer;
        this.formCount.confirmer = row.confirmer;
        this.formCount.id = row.id;
        this.formCount.remark = row.remark;
        this.formCount.accoName = row.accoName || '';
        this.formCount.hvpsNo = row.hvpsNo || '';
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
          if (this.formCount.openDate && this.formCount.closeDate) {
            if (this.formCount.openDate >= this.formCount.closeDate) {
              this.$message.closeAll();
              this.$message({
                message: "销户日期选择错误",
                type: "warning",
              });
              return;
            }
          }
          if (this.operationType === 1) {
            // 添加
            this.saveData();
          } else {
            // 修改
            this.updateParamSet();
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
          params = commonFun.parameterSrc(this.formCount);
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
                // this.countDialog = false;
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
              // this.countDialog = false;
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
          let formData = this.initFormData(params);
          pageApi
            .updateDataSource(formData)
            .then((response) => {
              if (response.data.status === 200) {
                // 关闭移动指标弹框
                // 关闭移动指标弹框
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
        formData.append("relaType", "qh_file");
      }

      if (params.id) {
        formData.append("id", params.id);
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
      if (params.status) {
        formData.append("status", params.status);
      }
      if (params.futureCode) {
        formData.append("futureCode", params.futureCode);
      }
      if (params.capitalAccount) {
        formData.append("capitalAccount", params.capitalAccount);
      }
      if (params.tradeFee) {
        formData.append("tradeFee", params.tradeFee);
      }
      if (params.szaAccount) {
        formData.append("szaAccount", params.szaAccount);
      }
      if (params.shaAccount) {
        formData.append("shaAccount", params.shaAccount);
      }
      if (params.tradeAuth) {
        formData.append("tradeAuth", params.tradeAuth);
      }
      if (params.bfRelated) {
        formData.append("bfRelated", params.bfRelated);
      }

      if (params.ndaSigned) {
        formData.append("ndaSigned", params.ndaSigned);
      }
      if (params.bsaSigned) {
        formData.append("bsaSigned", params.bsaSigned);
      }
      if (params.openDate) {
        formData.append("openDate", params.openDate);
      }
      if (params.openReason) {
        formData.append("openReason", params.openReason);
      }
      if (params.closeDate) {
        formData.append("closeDate", params.closeDate);
      }
      if (params.closeReason) {
        formData.append("closeReason", params.closeReason);
      }
      if (params.openStruc) {
        formData.append("openStruc", params.openStruc);
      }
      if (params.openExchange) {
        formData.append("openExchange", params.openExchange);
      }
      if (params.exchangeAddress) {
        formData.append("exchangeAddress", params.exchangeAddress);
      }
      if (params.exchangeBroker) {
        formData.append("exchangeBroker", params.exchangeBroker);
      }
      if (params.cashContact) {
        formData.append("cashContact", params.cashContact);
      }
      if (params.brokerPhone) {
        formData.append("brokerPhone", params.brokerPhone);
      }
      if (params.cashPhone) {
        formData.append("cashPhone", params.cashPhone);
      }
      if (params.openOperator) {
        formData.append("openOperator", params.openOperator);
      }
      if (params.accountOperator) {
        formData.append("accountOperator", params.accountOperator);
      }
      if (params.closeOperator) {
        formData.append("closeOperator", params.closeOperator);
      }

      if (params.srfsAccount) {
        formData.append("srfsAccount", params.srfsAccount);
      }
      if (params.single) {
        formData.append("single", params.single);
      }
      if (params.transfer) {
        formData.append("transfer", params.transfer);
      }
      if (params.confirmer) {
        formData.append("confirmer", params.confirmer);
      }
      if (params.remark) {
        formData.append("remark", params.remark);
      }
      formData.append("accoName", params.accoName || '');
      formData.append("hvpsNo", params.hvpsNo || '');
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
.qhAccountWidth {
  width: 60% !important;
}
</style>
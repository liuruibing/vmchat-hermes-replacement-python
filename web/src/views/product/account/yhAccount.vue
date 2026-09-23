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
            <el-form-item label="投资品种" prop="investTypeSearch">
              <el-select
                v-model="formInline.investTypeSearch"
                clearable
                filterable
                placeholder="请选择"
              >
                <el-option
                  v-for="item in investTypeSearchArr"
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
              v-btn="'yhAccount.insert.info'"
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
      <i class="el-icon-s-data"></i>银行间债券账户列表
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
        min-width="110"
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
        min-width="110"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.productName | noDataFilter }}</span>
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
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.admittanceNo | noDataFilter }}</span>
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
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.shchName | noDataFilter }}</span>
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
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.shchAccount | noDataFilter }}</span>
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
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.shchCapitalName | noDataFilter }}</span>
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
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.shchCapitalAccount | noDataFilter }}</span>
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
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.shchCapitalBank | noDataFilter }}</span>
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
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.shchCapitalCode | noDataFilter }}</span>
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
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.shchInstName | noDataFilter }}</span>
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
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.shchInstAccount | noDataFilter }}</span>
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
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.ccdcName | noDataFilter }}</span>
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
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.ccdcAccount | noDataFilter }}</span>
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
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.ccdcCapitalName | noDataFilter }}</span>
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
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.ccdcCapitalAccount | noDataFilter }}</span>
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
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.ccdcCapitalBank | noDataFilter }}</span>
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
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.ccdcCapitalCode | noDataFilter }}</span>
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
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.ccdchInstName | noDataFilter }}</span>
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
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.ccdcInstAccount | noDataFilter }}</span>
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
          <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.investTypeNames | noDataFilter }}</span>
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
            v-btn="'yhAccount.update.info'"
            v-if="scope.row.approvalStatus=='1'?false:true"
            type="primary"
            size="small"
            @click="editData(scope.row)"
            >编辑</el-button
          >
          <el-button
            v-btn="'yhAccount.delete.info'"
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
      <el-container style="height: 400px" v-if="containerRush">
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
                  <select-table v-model="formCount.productId" @sendDataObj='dataObj' v-if="!isSearchData" ref="relation"></select-table>
                  <el-input v-model="formCount.productId" disabled v-else></el-input>
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
                  style="visibility:hidden;"
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
                    show-word-limit
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
                  <el-checkbox
                    :indeterminate="isIndeterminate"
                    v-model="checkAll"
                    @change="handleCheckAllChange"
                    :disabled="isDisable"
                    >全选</el-checkbox
                  >
                  <div style="margin: 15px 0"></div>
                  <el-checkbox-group
                    v-model="checkfundInvestArea"
                    @change="handleCheckedInvestAreaChange"
                  >
                    <el-checkbox
                      :disabled="isDisable"
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
import selectTable from '@/views/commonComponents/selectTable.vue';
import Pagination from "@/components/Pagination";
import commonFun from "@/filters/new_common";
import commonApi from "@/api/common";
import { FILE_URL } from "@/utils/request";
import { getToken } from "@/utils/auth";
import pageApi from "@/api/product/yhAccount";
import modelFileValidate from '@/mixinsModel/file-validate'
export default {
  name: "yhAccount",
  mixins: [modelFileValidate],
  components: { Pagination, selectTable },
  data() {
    return {
      isDisable: false,
      containerRush: true,
      formInline: {
        productCode: "",
        investTypeSearch: "",
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
        productName: "", //产品代码
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
        admittanceNo: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母或者数字",
          },
        ],
        shchName: [
          {
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message: this.$regularValidator.empty().msg,
          },
          { required: false, trigger: "blur", message: "请填写上清所持有人账户名称"}
        ],
        ccdcName: [
          {
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message: this.$regularValidator.empty().msg,
          },
          { required: false, trigger: "blur", message: "请填写中债登债券账户名称"}
        ],
        shchAccount: [
          {
            type: "string",
            trigger: "change",
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母或者数字",
          },
          { required: false, trigger: "blur", message: "请填写上清所持有人账户账号"}
        ],
        ccdcAccount: [
          {
            type: "string",
            trigger: "change",
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母或者数字",
          },
          { required: false, trigger: "blur", message: "请填写中债登债券账户账号"}
        ],
        shchCapitalName: [
          {
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message: this.$regularValidator.empty().msg,
          },
          { required: false, trigger: "blur", message: "请填写上清所资金账户名称"}
        ],
        ccdcCapitalName: [
          {
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message: this.$regularValidator.empty().msg,
          },
          { required: false, trigger: "blur", message: "请填写中债登资金账户名称"}
        ],
        shchCapitalAccount: [
          {
            type: "string",
            trigger: "change",
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母或者数字",
          },
          { required: false, trigger: "blur", message: "请填写上清所资金账户账号"}
        ],
        ccdcCapitalAccount: [
          {
            type: "string",
            trigger: "change",
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母或者数字",
          },
          { required: false, trigger: "blur", message: "请填写中债登资金账户账号"}
        ],
        shchCapitalBank: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message: this.$regularValidator.empty().msg,
          },
        ],
        ccdcCapitalBank: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message: this.$regularValidator.empty().msg,
          },
        ],
        shchCapitalCode: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母或者数字",
          },
        ],
        ccdcCapitalCode: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母或者数字",
          },
        ],
        shchInstName: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message: this.$regularValidator.empty().msg,
          },
        ],
        ccdchInstName: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message: this.$regularValidator.empty().msg,
          },
        ],
        shchInstAccount: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母或者数字",
          },
        ],
        ccdcInstAccount: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母或者数字",
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
      investTypeSearchArr: [
        { name: "上清", value: "bondInvestTypes_shch" },
        { name: "中债", value: "bondInvestTypes_ccdc" },
        { name: "质押式回购", value: "bondInvestTypes_zyshg" },
        { name: "现券买卖", value: "bondInvestTypes_xqmm" },
        { name: "利率互换", value: "bondInvestTypes_llhh" },
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
      fundInvestArea: [],
      checkAll: false,
      isIndeterminate: true,
      checkfundInvestArea: [], //投资工具选择
      saveCode: "",
    };
  },

  mounted() {
    this.getProductsAll();
    this.getEdims();
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
    closedDialog() {
      this.$refs["formCount"].resetFields();
      this.fileList = [];
      this.checkfundInvestArea = [];
      this.containerRush = false;
    },
    opendDialog() {
      this.containerRush = true;
    },
    // 查询
    onSubmit(flag) {
      this.tableLoading = true;
      // 消除没有值的参数
      if (flag) {
        this.formInline.pageNum = 1;
      }
      let data = { ...this.formInline }
      if (data.fundCode) data['fundCode'] = data.fundCode.split('_')[0]
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
      this.isDisable = false;
      this.countDialog = true;
      this.operationType = 1;

      this.bigSize = true;
      this.fileList = [];
      this.isSearchData = false;
      this.isChangeFile = false;
      this.saveCode = "yhAccount.insert.save";

      // 清除
      this.$nextTick(() => {
        this.$refs["formCount"].resetFields();
        this.formCount.productId = "";
        this.formCount.productCode = "";
        this.formCount.productName = "";
        this.formCount.admittanceNo = "";
        this.formCount.investTypeDimsTr = "";
        this.formCount.shchName = "";
        this.formCount.ccdcName = "";
        this.formCount.shchAccount = "";
        this.formCount.ccdcAccount = "";
        this.formCount.shchCapitalName = "";
        this.formCount.ccdcCapitalName = "";

        this.formCount.shchCapitalAccount = "";
        this.formCount.ccdcCapitalAccount = "";
        this.formCount.shchCapitalBank = "";
        this.formCount.ccdcCapitalBank = "";
        this.formCount.shchCapitalCode = "";
        this.formCount.shchInstName = "";
        this.formCount.ccdchInstName = "";
        this.formCount.shchInstAccount = "";
        this.formCount.ccdcCapitalCode = "";
        this.formCount.ccdcInstAccount = "";
        this.formCount.remark = "";
        this.formCount.id = "";
        this.checkAll = false;
        this.checkfundInvestArea = [];
      });
    },
    // 行编辑数据
    editData(row) {
      this.countTitle = "编辑";
      this.countFormList = "edit";
      this.isDisable = false;
      this.countDialog = true;
      this.operationType = 2;
      this.bigSize = true;
      this.fileList = [];
      this.isSearchData = false;
      this.isChangeFile = false;
      this.rmoveFileId = [];
      this.saveCode = "yhAccount.update.save";
      this.getFileList(row.id, "yh_file");
      this.$nextTick(() => {
        this.$refs["formCount"].resetFields();
        this.formCount.productId = row.productCode+'_'+row.productName;
        this.formCount.productCode = row.productCode;
        this.formCount.productName = row.productName || '';
        this.formCount.admittanceNo = row.admittanceNo;

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
    searchData(row) {
      this.bigSize = true;
      this.isDisable = true;
      this.countTitle = "查看详情";
      this.countFormList = "edit";
      this.countDialog = true;
      this.operationType = 2;

      this.isSearchData = true;
      this.bigSize = true;
      this.fileList = [];
      this.isChangeFile = false;
      this.tableDataEdit = [];
      this.getFileList(row.id, "yh_file");
      this.$nextTick(() => {
        this.$refs["formCount"].resetFields();
        this.formCount.productId = row.productCode+'_'+row.productName;
        this.formCount.productCode = row.productCode;
        this.formCount.productName = row.productName || '';
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
    handleRemove(file, filelist) {
      this.fileList = filelist
      if (filelist.length === 0) return;
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
      //     if (item.size) totalFilel.push(item)
      //   }
      //   this.fileList = totalFilel
      //   return this.$message.error("上传的文件不能为空文件")
      // }
      // for (let item of filelist) {
      //   totalSize = item.size + totalSize;
      // }
      // totalFlag = totalSize / 1024 / 1024 < 50;
      // if (!totalFlag) {
      //   this.$message.warning("上传的文件不能大于50M !");
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
        formData.append("relaType", "yh_file");
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
      if (params.admittanceNo) {
        formData.append("admittanceNo", params.admittanceNo);
      }

      if (params.shchName) {
        formData.append("shchName", params.shchName);
      }
      if (params.ccdcName) {
        formData.append("ccdcName", params.ccdcName);
      }
      if (params.shchAccount) {
        formData.append("shchAccount", params.shchAccount);
      }
      if (params.ccdcAccount) {
        formData.append("ccdcAccount", params.ccdcAccount);
      }
      if (params.shchCapitalName) {
        formData.append("shchCapitalName", params.shchCapitalName);
      }
      if (params.ccdcCapitalName) {
        formData.append("ccdcCapitalName", params.ccdcCapitalName);
      }

      if (params.shchCapitalAccount) {
        formData.append("shchCapitalAccount", params.shchCapitalAccount);
      }
      if (params.ccdcCapitalAccount) {
        formData.append("ccdcCapitalAccount", params.ccdcCapitalAccount);
      }
      if (params.shchCapitalBank) {
        formData.append("shchCapitalBank", params.shchCapitalBank);
      }
      if (params.ccdcCapitalBank) {
        formData.append("ccdcCapitalBank", params.ccdcCapitalBank);
      }
      if (params.shchCapitalCode) {
        formData.append("shchCapitalCode", params.shchCapitalCode);
      }
      if (params.shchInstName) {
        formData.append("shchInstName", params.shchInstName);
      }
      if (params.ccdchInstName) {
        formData.append("ccdchInstName", params.ccdchInstName);
      }
      if (params.shchInstAccount) {
        formData.append("shchInstAccount", params.shchInstAccount);
      }
      if (params.ccdcCapitalCode) {
        formData.append("ccdcCapitalCode", params.ccdcCapitalCode);
      }
      if (params.ccdcInstAccount) {
        formData.append("ccdcInstAccount", params.ccdcInstAccount);
      }

      if (params.remark) {
        formData.append("remark", params.remark);
      }

      if (this.checkfundInvestArea.length > 0) {
        let str = this.checkfundInvestArea.join(",");
        formData.append("investTypeDims", str);
      }

      return formData;
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
    handleCheckAllChange(val) {
      let arr = this.fundInvestArea;
      let chekAllArr = [];
      if (arr) {
        for (let i = 0; i < arr.length; i++) {
          chekAllArr.push(arr[i].dimCde);
        }
      }
      this.checkfundInvestArea = val ? chekAllArr : [];
      this.isIndeterminate = false;
    },
    handleCheckedInvestAreaChange(value) {
      let checkedCount = value.length;
      this.checkAll = checkedCount === this.fundInvestArea.length;
      this.isIndeterminate =
        checkedCount > 0 && checkedCount < this.fundInvestArea.length;
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
  width: 50% !important;
}
</style>
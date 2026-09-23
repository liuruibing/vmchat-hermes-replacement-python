<template>
  <div class="zq_form" v-loading="zq_form_loading">
    <div v-if="none_show"><span>未找到当前产品的账户信息。</span></div>
    <div class="forms_table_title" v-if="table_show">
      <i class="el-icon-s-data"></i>证券账户列表
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
        min-width="100"
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
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.productName | noDataFilter }}</span>
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
        prop="optionCapitalAcco"
        sortable="custom"
        show-overflow-tooltip
        label="期权资金账户"
        min-width="120"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.optionCapitalAcco | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="smtCapitalAcco"
        sortable="custom"
        show-overflow-tooltip
        label="两融资金账户"
        min-width="120"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.smtCapitalAcco | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="tradeFee"
        sortable="custom"
        show-overflow-tooltip
        label="A股交易费率"
        min-width="120"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.tradeFee | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="optionTradeFee"
        sortable="custom"
        show-overflow-tooltip
        label="期权交易费率"
        min-width="120"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.optionTradeFee | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="smtTradeFee"
        sortable="custom"
        show-overflow-tooltip
        label="两融交易费率"
        min-width="120"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.smtTradeFee | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="tradeAuth"
        sortable="custom"
        show-overflow-tooltip
        label="已开通交易权限"
        min-width="140"
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
    <div class="mainBox" v-if="form_show && !preview_show">
      <div style="overflow: hidden;padding: 15px;">
        <span @click="close_form" style="font-size: 20px;float: right;cursor: pointer;"><i class="el-icon-close"></i></span>
      </div>
        <el-form
          ref="formCount"
          :model="formCount"
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
                <!-- <select-table v-model="formCount.productId" @sendDataObj='dataObj' v-if="!isSearchData" ref="relation"></select-table> -->
                <el-input v-model="formCount.productId" disabled></el-input>
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
                label="深市A股账号"
                prop="szaAccount"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <el-input
                ref="szaAccount"
                  maxlength="66"
                  :disabled="isSearchData"
                  v-model.trim="formCount.szaAccount"
                  clearable
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
                label="一码通"
                prop="yard"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <el-input
                  maxlength="66"
                  :disabled="isSearchData"
                  v-model.trim="formCount.yard"
                  clearable
                  ref="yard"
                ></el-input>
              </el-form-item>

              <el-form-item
                label="A股交易费率(%)"
                prop="tradeFee"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <el-input
                  maxlength="16"
                  :disabled="isSearchData"
                  v-model.trim="formCount.tradeFee"
                  clearable
                  ref="tradeFee"
                ></el-input>
              </el-form-item>

              <el-form-item
                label="沪市A股账号"
                prop="shaAccount"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <el-input
                  maxlength="66"
                  :disabled="isSearchData"
                  v-model.trim="formCount.shaAccount"
                  clearable
                  ref="shaAccount"
                ></el-input>
              </el-form-item>
              <el-form-item
                label="银证关联情况"
                prop="bsRelated"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <el-radio
                  :disabled="isSearchData"
                  v-model="formCount.bsRelated"
                  label="0"
                  >未关联</el-radio
                >
                <el-radio
                  :disabled="isSearchData"
                  v-model="formCount.bsRelated"
                  label="1"
                  >已关联</el-radio
                >
              </el-form-item>
            </el-col>
          </el-row>

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
          <el-row>
            <el-col :span="12">
              <el-form-item
                label="开户日期"
                prop="openDate"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <el-date-picker
                  ref="openDate"
                  style="width: 100%"
                  @change="isSelect()"
                  :disabled="isSearchData"
                  v-model="formCount.openDate"
                  type="date"
                  value-format="yyyy-MM-dd"
                  placeholder="选择日期"
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
                 ref="closeDate"
                 style="width: 100%"
                  @change="isSelect()"
                  v-model="formCount.closeDate"
                  type="date"
                  :disabled="isSearchData"
                  value-format="yyyy-MM-dd"
                  placeholder="选择日期"
                >
                </el-date-picker>
              </el-form-item>
            </el-col>
            <el-col :span="12">
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
              :on-preview="downFile"
              :headers="hearders"
              :action="fileUploadUrl"
              :file-list="fileList"
              :disabled="isSearchData"
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

          <div class="forms_table_title">
            <i class="el-icon-s-data"></i>期权账户信息
          </div>
          <el-row>
            <el-col :span="12">
              <el-form-item
                label="期权资金账户"
                prop="optionCapitalAcco"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <el-input
                  maxlength="66"
                  :disabled="isSearchData"
                  v-model.trim="formCount.optionCapitalAcco"
                  clearable
                  ref="optionCapitalAcco"
                ></el-input>
              </el-form-item>
              <el-form-item
                label="银衍关联情况"
                prop="bdRelated"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <el-radio
                  :disabled="isSearchData"
                  v-model="formCount.bdRelated"
                  label="0"
                  >未关联</el-radio
                >
                <el-radio
                  :disabled="isSearchData"
                  v-model="formCount.bdRelated"
                  label="1"
                  >已关联</el-radio
                >
              </el-form-item>
              <el-form-item
                label="期权销户日期"
                prop="optionCloseDate"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <el-date-picker
                  ref="optionCloseDate"
                  style="width: 100%"
                  :disabled="isSearchData"
                  v-model="formCount.optionCloseDate"
                  type="date"
                  @change="isSelect()"
                  value-format="yyyy-MM-dd"
                  placeholder="选择日期"
                >
                </el-date-picker>
              </el-form-item>
              <el-form-item
                label="开通情况"
                prop="optionOpenType"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <el-checkbox-group
                  :disabled="isSearchData"
                  v-model="formCount.optionOpenType"
                >
                  <el-checkbox label="szOption">深市期权</el-checkbox>
                  <el-checkbox label="shOption">沪市期权</el-checkbox>
                </el-checkbox-group>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item
                label="期权开户日期"
                prop="optionOpenDate"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <el-date-picker
                  style="width: 100%"
                  ref="optionOpenDate"
                  @change="isSelect()"
                  v-model="formCount.optionOpenDate"
                  type="date"
                  :disabled="isSearchData"
                  value-format="yyyy-MM-dd"
                  placeholder="选择日期"
                >
                </el-date-picker>
              </el-form-item>

              <el-form-item
                label="期权交易费率(%)"
                prop="optionTradeFee"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <el-input
                  maxlength="16"
                  :disabled="isSearchData"
                  v-model.trim="formCount.optionTradeFee"
                  clearable
                  ref="optionTradeFee"
                ></el-input>
              </el-form-item>

              <el-form-item
                label="销户原因"
                prop="optionCloseReason"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <el-input
                  maxlength="333"
                  :disabled="isSearchData"
                  v-model.trim="formCount.optionCloseReason"
                  clearable
                  ref="optionCloseReason"
                ></el-input>
              </el-form-item>
            </el-col>
          </el-row>

          <div class="forms_table_title">
            <i class="el-icon-s-data"></i>两融账户信息
          </div>
          <el-row>
            <el-col :span="12">
              <el-form-item
                label="两融资金账户"
                prop="smtCapitalAcco"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <el-input
                  maxlength="66"
                  :disabled="isSearchData"
                  v-model.trim="formCount.smtCapitalAcco"
                  clearable
                  ref="smtCapitalAcco"
                ></el-input>
              </el-form-item>
              <el-form-item
                label="银信关联情况"
                prop="bcRelated"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <el-radio
                  :disabled="isSearchData"
                  v-model="formCount.bcRelated"
                  label="0"
                  >未关联</el-radio
                >
                <el-radio
                  :disabled="isSearchData"
                  v-model="formCount.bcRelated"
                  label="1"
                  >已关联</el-radio
                >
              </el-form-item>
              <el-form-item
                label="两融销户日期"
                prop="smtCloseDate"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <el-date-picker
                  ref="smtCloseDate"
                  style="width: 100%"
                  :disabled="isSearchData"
                  v-model="formCount.smtCloseDate"
                  type="date"
                  @change="isSelect()"
                  value-format="yyyy-MM-dd"
                  placeholder="选择日期"
                >
                </el-date-picker>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item
                label="两融开户日期"
                prop="smtOpenDate"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <el-date-picker
                  ref="smtOpenDate"
                  style="width: 100%"
                  v-model="formCount.smtOpenDate"
                  type="date"
                  @change="isSelect()"
                  :disabled="isSearchData"
                  value-format="yyyy-MM-dd"
                  placeholder="选择日期"
                >
                </el-date-picker>
              </el-form-item>

              <el-form-item
                label="两融交易费率(%)"
                prop="smtTradeFee"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <el-input
                  maxlength="16"
                  :disabled="isSearchData"
                  v-model.trim="formCount.smtTradeFee"
                  clearable
                  ref="smtTradeFee"
                ></el-input>
              </el-form-item>

              <el-form-item
                label="销户原因"
                prop="smtCloseReason"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <el-input
                  maxlength="333"
                  :disabled="isSearchData"
                  v-model.trim="formCount.smtCloseReason"
                  clearable
                  ref="smtCloseReason"
                ></el-input>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
        <div class="forms_table_title">
          <i class="el-icon-s-data"></i>交易系统信息
        </div>
        <!-- <el-button
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
        </el-button> -->
        <div class="vxeMixHeight">
          <vxe-table
            border
            keep-source
            show-overflow
            ref="xTable"
            height="600"
            class="my_table_insert"
            :cell-class-name="cellClassName"
            :header-cell-class-name="headerCellClassName"
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
              field="tradeSys"
              title="交易系统"
              :edit-render="{
                name: 'input',
                attrs: {
                  type: 'text',
                  disabled: isSearchData,
                  maxlength: '66',
                },
              }"
            ></vxe-table-column>
            <vxe-table-column
              field="reportName"
              title="报备人员"
              :edit-render="{
                name: 'input',
                attrs: {
                  type: 'text',
                  disabled: isSearchData,
                  maxlength: '66',
                },
              }"
            ></vxe-table-column>
            <vxe-table-column
              field="reportRole"
              title="报备角色"
              :edit-render="{
                name: 'input',
                attrs: {
                  type: 'text',
                  disabled: isSearchData,
                  maxlength: '66',
                },
              }"
            ></vxe-table-column>
            <vxe-table-column
              field="macAddress"
              title="MAC地址"
              :edit-render="{
                name: 'input',
                attrs: {
                  type: 'text',
                  disabled: isSearchData,
                  maxlength: '1000',
                },
              }"
            ></vxe-table-column>
            <vxe-table-column
              field="ipAddress"
              title="IP地址"
              :edit-render="{
                name: 'input',
                attrs: {
                  type: 'text',
                  disabled: isSearchData,
                  maxlength: '1000',
                },
              }"
            ></vxe-table-column>
            <vxe-table-column
              field="harddiskNo"
              title="硬盘序列号"
              :edit-render="{
                name: 'input',
                attrs: {
                  type: 'text',
                  disabled: isSearchData,
                  maxlength: '1000',
                },
              }"
            ></vxe-table-column>
          </vxe-table>
        </div>
      </div>
      <div v-if="preview_show" style="height:100%;padding: 0 20px">
      <p class="yulan_title"> <span class="yulan_title_name">附件预览</span><span style="font-size:20px;color:#000;cursor: pointer;"><i @click="closePreview" class="el-icon-close"></i></span> </p>
      <PdfPreview :urlArr='fileList' :PreviewFileId="PreviewFileId" style="width:100%;height:100%" ref="PdfPreview"></PdfPreview>
    </div>
  </div>
</template>

<script>
import PdfPreview from '@/components/PdfPreview'
import pageApi from "@/api/product/zqAccount";
import commonApi from "@/api/common";
export default {
  components:{PdfPreview},
  data(){
    return{
      formLabelWidth:'150px',
      isSearchData:true,
      tableData:[],
      tableLoading:false,
      table_show:false,
      form_show:false,
      none_show:false,
      formCount: {
        productId: "", //产品名称
        productCode: "", //产品代码
        status: "", //账户状态
        yard: "", //一码通
        capitalAccount: "", //资金账户
        tradeFee: "", //A股交易费率
        szaAccount: "", //深市A股账号
        shaAccount: "", //沪市A股账号
        tradeAuth: "", //已开通交易权限
        bsRelated: "", //银证关联情况
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
        optionCapitalAcco: "", //期权资金账户
        optionOpenDate: "", //期权开户日期
        bdRelated: "", //银衍关联情况
        optionTradeFee: "", //期权交易费率
        optionCloseDate: "", //销户原因
        optionCloseReason: "",
        optionOpenType: [], //开通情况
        smtCapitalAcco: "", //两融资金账户
        smtOpenDate: "", //两融开户日期
        bcRelated: "", //银信关联情况
        smtTradeFee: "", //两融交易费率
        smtCloseDate: "", //销户日期
        smtCloseReason: "", //销户原因
        remark: "",
      },
      tableDataEdit:[],
      hearders:{},
      fileUploadUrl:'',
      fileList:[],
      statusArr:[
        { name: "正在开户", value: "opening" },
        { name: "正常交易", value: "trading" },
        { name: "正在销户", value: "closing" },
        { name: "已销户", value: "closed" },
      ],
      zq_form_loading:false,
      preview_show:false,
      PreviewFileId:''
    }
  },
  methods:{
    cellClassName ({ row, rowIndex, column, columnIndex }) {
      return 'vxe-cell-class-name'
    },
    headerCellClassName ({ column, columnIndex }) {
      return 'vxe-header-cell-class-name'
    },
    init(val){
      this.preview_show = false;
      this.form_show = false;
      this.zq_form_loading = true;
      this.getTableList(val)
    },
    downFile(file) {
      if(file.id){
        this.PreviewFileId = file.id;
        this.preview_show=true;
      }
    },
    searchData(row){
      this.table_show = false;
      this.form_show = true;
      this.getFileList(row.id, "zqh_file");
      this.$nextTick(() => {
        this.$refs["formCount"].resetFields();
        this.formCount.productId = row.productName;
        this.formCount.productCode = row.productCode;
        this.formCount.status = row.status;
        this.formCount.yard = row.yard;
        this.formCount.capitalAccount = row.capitalAccount;
        this.formCount.tradeFee = row.tradeFee;
        this.formCount.szaAccount = row.szaAccount;
        this.formCount.shaAccount = row.shaAccount;
        this.formCount.tradeAuth = row.tradeAuth;
        this.formCount.bsRelated = row.bsRelated;
        this.formCount.ndaSigned = row.ndaSigned;
        this.formCount.bsaSigned = row.bsaSigned;
        if (row.openDateStr) {
          this.formCount.openDate = row.openDateStr;
        }

        this.formCount.openReason = row.openReason;
        if (row.closeDateStr) {
          this.formCount.closeDate = row.closeDateStr;
        }

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
        this.formCount.optionCloseReason = row.optionCloseReason;
        this.formCount.optionCapitalAcco = row.optionCapitalAcco;
        if (row.optionOpenDateStr) {
          this.formCount.optionOpenDate = row.optionOpenDateStr;
        }

        this.formCount.bdRelated = row.bdRelated;
        this.formCount.optionTradeFee = row.optionTradeFee;

        if (row.optionCloseDateStr) {
          this.formCount.optionCloseDate = row.optionCloseDateStr;
        }
        if (row.optionOpenType) {
          let optionOpenType = row.optionOpenType;
          let arr = optionOpenType.split(",");
          this.formCount.optionOpenType = arr;
        } else {
          this.formCount.optionOpenType = [];
        }

        this.formCount.smtCapitalAcco = row.smtCapitalAcco;

        if (row.smtOpenDateStr) {
          this.formCount.smtOpenDate = row.smtOpenDateStr;
        }
        this.formCount.bcRelated = row.bcRelated;
        this.formCount.smtTradeFee = row.smtTradeFee;

        if (row.smtCloseDateStr) {
          this.formCount.smtCloseDate = row.smtCloseDateStr;
        }
        this.formCount.smtCloseReason = row.smtCloseReason;
        this.formCount.id = row.id;
        this.formCount.remark = row.remark;

        this.tableDataEdit = row.stockSyss;
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
            this.zq_form_loading = false;
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
            this.zq_form_loading = false;
          });
    },
    close_form(){
      this.table_show = true;
      this.form_show = false;
    },
    closePreview(){
      this.preview_show = false;
      this.$notify.closeAll();
    },

  }
}
</script>

<style lang="scss">
  .zq_form{
    // min-height: 50px;
    height: 100%;
    .el-form-item__content{
      min-width: 0 !important;
    }
    .vxe-table--body-wrapper{
      height: 100% !important;
      max-height: 550px !important;
      min-height: 50px !important;
    }
  }
</style>
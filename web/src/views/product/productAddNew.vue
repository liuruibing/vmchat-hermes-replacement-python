<template>
  <div>
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="基础信息" name="first">
        <div class="product_detail">
          <el-row>
            <el-col :span="23" :offset="1">
              <el-row>
                <el-form
                  :inline="true"
                  :rules="commonRules"
                  label-width="150px"
                  label-position="right"
                  ref="formInline"
                  :model="formInline"
                  class="demo-form-inline form_inline_search"
                  style="
                    margin-top: 8px;
                    margin-bottom: 10px;
                    margin-left: 80px;
                  "
                >
                  <el-col :span="11">
                    <el-form-item label="产品名称" prop="fundName">
                      <el-input
                        v-model="formInline.fundName"
                        placeholder="产品名称"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />
                    <el-form-item label="英文名称" prop="fundNameEn">
                      <el-input
                        v-model="formInline.fundNameEn"
                        placeholder="英文名称"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />
                    <el-form-item label="托管人名称" prop="trustorCode">
                      <el-select
                        clearable
                        class="el_form_item"
                        v-model="formInline.trustorCode"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in trustorCodeArr"
                          :value="group.id"
                          :key="index"
                          :label="group.instName"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <br />
                    <el-form-item label="基金类型" prop="fundType">
                      <el-select
                        clearable
                        class="el_form_item"
                        v-model="formInline.fundType"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in fundTypeArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <br />
                    <el-form-item label="证券营业部" prop="operateDept">
                      <el-input
                        v-model="formInline.operateDept"
                        placeholder="证券营业部"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />
                    <el-form-item label="产品存续期限(年)" prop="holdYear">
                      <el-input
                        v-model="formInline.holdYear"
                        placeholder="产品存续期限"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />
                    <el-form-item label="风险等级" prop="riskLevel">
                      <el-select
                        clearable
                        class="el_form_item"
                        v-model="formInline.riskLevel"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in riskLevelArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <br />
                    <el-form-item label="产品备案代码" prop="recordCode">
                      <el-input
                        v-model="formInline.recordCode"
                        placeholder="产品备案代码"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />
                    <el-form-item label="是否分级" prop="isGrade">
                      <el-select
                        clearable
                        class="el_form_item"
                        @change="isGradeChange"
                        v-model="formInline.isGrade"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in isGradeArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                  </el-col>

                  <el-col :span="11" :offset="1">
                    <el-form-item label="产品代码" prop="fundCode">
                      <el-input
                        v-model="formInline.fundCode"
                        placeholder="产品代码"
                        type="text"
                        :disabled="PageDataAdd.addType == 0"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />
                    <el-form-item label="管理人名称" prop="managerCode">
                      <el-select
                        clearable
                        class="el_form_item"
                        v-model="formInline.managerCode"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in managerCodeArr"
                          :value="group.id"
                          :key="index"
                          :label="group.instName"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <br />

                    <el-form-item label="基金服务机构" prop="operatorCode">
                      <el-select
                        clearable
                        class="el_form_item"
                        v-model="formInline.operatorCode"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in operatorCodeArr"
                          :value="group.id"
                          :key="index"
                          :label="group.instName"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <br />
                    <el-form-item label="投资方向" prop="investDirect">
                      <el-select
                        clearable
                        class="el_form_item"
                        v-model="formInline.investDirect"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in investDirectArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <br />
                    <el-form-item label="基金成立日期" prop="setupDate">
                      <el-date-picker
                        v-model="formInline.setupDate"
                        type="date"
                        style="width: 188px !important"
                        value-format="yyyy-MM-dd"
                        placeholder="选择日期"
                      >
                      </el-date-picker>
                    </el-form-item>
                    <br />

                    <el-form-item label="基金备案日期" prop="recordDate">
                      <el-date-picker
                        v-model="formInline.recordDate"
                        type="date"
                        style="width: 188px !important"
                        value-format="yyyy-MM-dd"
                        placeholder="选择日期"
                      >
                      </el-date-picker>
                    </el-form-item>
                    <br />

                    <el-form-item label="运作方式" prop="operateType">
                      <el-select
                        clearable
                        class="el_form_item"
                        v-model="formInline.operateType"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in operateTypeArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <br />
                    <el-form-item label="产品状态" prop="fundState">
                      <el-select
                        clearable
                        class="el_form_item"
                        v-model="formInline.fundState"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in fundStateArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                  </el-col>
                </el-form>
              </el-row>

              <el-row>
                <el-col :span="6" :offset="10">
                  <el-button
                    type="primary"
                    plain
                    @click="myTabNext('1')"
                    style="margin-bottom: 5px"
                    size="small"
                  >
                    下一步
                  </el-button>
                  <el-button
                    type="primary"
                    @click="save('formInline')"
                    style="margin-bottom: 5px"
                    >保存</el-button
                  >
                </el-col>
              </el-row>
            </el-col>
          </el-row>
        </div>
      </el-tab-pane>
      <el-tab-pane label="交易信息" name="second">
        <div class="product_detail">
          <el-row>
            <el-col :span="23" :offset="1">
              <el-row>
                <el-form
                  :inline="true"
                  :rules="commonRules"
                  label-width="170px"
                  label-position="right"
                  ref="formInline"
                  :model="formInline"
                  class="demo-form-inline form_inline_search"
                  style="
                    margin-top: 8px;
                    margin-bottom: 10px;
                    margin-left: 80px;
                  "
                >
                  <!-- <el-form-item label="销售方式" prop="saleType">
                    <el-select clearable  v-model="formInline.saleType"   class="el_form_item"  placeholder="请选择"  >
                            <el-option
                              v-for="(group, index) in saleTypeArr"
                               :value="group.dimCde"
                              :key="index"
                              :label="group.dimNme">
                            </el-option>
                        </el-select>
                 </el-form-item> -->
                  <el-col :span="11">
                    <el-form-item
                      label="认申购起点（不含费）元"
                      prop="purchasePoint"
                    >
                      <el-input-number
                        class="el_form_item"
                        v-model="formInline.purchasePoint"
                        controls-position="right"
                        @change="handleChange"
                        :min="-999"
                        :max="100"
                      ></el-input-number>
                    </el-form-item>
                    <br />
                    <el-form-item
                      label="认购交易确认天数"
                      prop="subscribeConfirmDay"
                    >
                      <el-select
                        clearable
                        v-model="formInline.subscribeConfirmDay"
                        class="el_form_item"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in subscribeConfirmDayArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <br />
                    <el-form-item
                      label="认购费率(1%填0.01)"
                      prop="subscribeRate"
                    >
                      <el-input-number
                        class="el_form_item"
                        v-model="formInline.subscribeRate"
                        controls-position="right"
                        @change="handleChange"
                        :min="-999"
                        :max="100"
                      ></el-input-number>
                    </el-form-item>
                    <br />
                    <el-form-item
                      label="申购资金交收天数"
                      prop="applyDeliverDay"
                    >
                      <el-select
                        clearable
                        v-model="formInline.applyDeliverDay"
                        class="el_form_item"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in applyDeliverDayArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <br />
                    <el-form-item label="销售服务费计提" prop="saleFeePrepare">
                      <el-select
                        clearable
                        v-model="formInline.saleFeePrepare"
                        class="el_form_item"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in saleFeePrepareArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <br />
                    <el-form-item
                      label="赎回交易确认天数"
                      prop="callConfirmDay"
                    >
                      <el-select
                        clearable
                        v-model="formInline.callConfirmDay"
                        class="el_form_item"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in callConfirmDayArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <br />
                    <el-form-item label="赎回费率浮动类型" prop="callFloatType">
                      <el-select
                        clearable
                        v-model="formInline.callFloatType"
                        @change="callFloatTypeChange"
                        class="el_form_item"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in callFloatTypeArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <br />
                    <el-form-item
                      label="赎回费率类型"
                      prop="callRateType"
                      v-if="callFloat_select_show"
                      :rules="callRateTypeRul"
                    >
                      <el-select
                        clearable
                        v-model="formInline.callRateType"
                        class="el_form_item"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in callRateTypeArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <br />
                    <el-form-item
                      label="赎回费率(1%填0.01)"
                      prop="callRate"
                      v-if="callFloat_input_show"
                      :rules="callRateRul"
                    >
                      <el-input-number
                        class="el_form_item"
                        v-model="formInline.callRate"
                        controls-position="right"
                        @change="handleChange"
                        :min="-999"
                        :max="100"
                      ></el-input-number>
                    </el-form-item>
                  </el-col>

                  <el-col :span="11" :offset="1">
                    <el-form-item label="封闭期" prop="blockDate">
                      <el-date-picker
                        v-model="formInline.blockDate"
                        type="date"
                        style="width: 188px !important"
                        value-format="yyyy-MM-dd"
                        placeholder="选择日期"
                      >
                      </el-date-picker>
                    </el-form-item>
                    <br />
                    <el-form-item
                      label="追加认申购级差"
                      prop="purchaseDiffAppend"
                    >
                      <el-input-number
                        class="el_form_item"
                        v-model="formInline.purchaseDiffAppend"
                        controls-position="right"
                        @change="handleChange"
                        :min="-999"
                        :max="100"
                      ></el-input-number>
                    </el-form-item>
                    <br />
                    <el-form-item
                      label="认购资金交收天数"
                      prop="subscribeDeliverDay"
                    >
                      <el-select
                        clearable
                        v-model="formInline.subscribeDeliverDay"
                        class="el_form_item"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in subscribeDeliverDayArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <br />
                    <el-form-item
                      label="申购交易确认天数"
                      prop="applyConfirmDay"
                    >
                      <el-select
                        clearable
                        v-model="formInline.applyConfirmDay"
                        class="el_form_item"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in applyConfirmDayArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <br />
                    <el-form-item label="申购费率(1%填0.01)" prop="applyRate">
                      <el-input-number
                        class="el_form_item"
                        v-model="formInline.applyRate"
                        controls-position="right"
                        @change="handleChange"
                        :min="-999"
                        :max="100"
                      ></el-input-number>
                    </el-form-item>
                    <br />
                    <el-form-item label="销售服务费支付" prop="saleFeePay">
                      <el-select
                        clearable
                        v-model="formInline.saleFeePay"
                        class="el_form_item"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in saleFeePayArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <br />
                    <el-form-item
                      label="赎回资金交收天数"
                      prop="callDeliverDay"
                    >
                      <el-select
                        clearable
                        v-model="formInline.callDeliverDay"
                        class="el_form_item"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in callDeliverDayArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                  </el-col>
                </el-form>
              </el-row>
              <el-row v-if="callFloat_select_show">
                <el-col :span="18" :offset="4">
                  <div style="height: 10px">
                    <el-button
                      type="primary"
                      plain
                      @click="insertEvent('redeem')"
                      style="margin-bottom: 5px"
                      size="small"
                    >
                      <i class="el-icon-circle-plus-outline"></i>新增
                    </el-button>
                    <el-button
                      type="danger"
                      plain
                      @click="removeEvent('redeem')"
                      style="margin-bottom: 5px"
                      size="small"
                    >
                      <i class="el-icon-delete"></i>移除
                    </el-button>
                  </div>
                  <!-- <el-button type="error"  plain  @click="revertEvent" style="margin-bottom: 5px; " size="small">
                          <i class="el-icon-back"></i>还原
                  </el-button> -->
                  <div style="margin-top: 30px">
                    <vxe-table
                      border
                      show-overflow
                      ref="xTableRedeem"
                      width="auto"
                      max-height="400"
                      :data="tableDataRedeem"
                      :edit-config="{
                        trigger: 'click',
                        mode: 'cell',
                        icon: 'fa fa-pencil',
                      }"
                    >
                      <vxe-table-column
                        type="checkbox"
                        width="60"
                      ></vxe-table-column>
                      <vxe-table-column
                        type="seq"
                        title="序号"
                        width="60"
                      ></vxe-table-column>
                      <vxe-table-column
                        field="redeemFrom"
                        title="From"
                        :edit-render="{ name: 'input' }"
                      ></vxe-table-column>
                      <vxe-table-column
                        field="redeemTo"
                        title="To"
                        :edit-render="{ name: 'input' }"
                      ></vxe-table-column>
                      <vxe-table-column
                        field="redeemRate"
                        title="费率"
                        :edit-render="{ name: 'input' }"
                      ></vxe-table-column>
                    </vxe-table>
                  </div>
                </el-col>
              </el-row>

              <el-row style="margin-top: 10px">
                <el-col :span="6" :offset="10">
                  <el-button
                    type="primary"
                    plain
                    @click="myTabNext('2')"
                    style="margin-bottom: 5px"
                    size="small"
                  >
                    下一步
                  </el-button>
                  <el-button
                    type="primary"
                    @click="save('formInline')"
                    style="margin-bottom: 5px"
                    >保存</el-button
                  >
                </el-col>
              </el-row>
            </el-col>
          </el-row>
        </div>
      </el-tab-pane>
      <el-tab-pane label="费用信息" name="third">
        <div class="product_detail">
          <el-row>
            <el-col :span="23" :offset="1">
              <el-row>
                <el-form
                  :inline="true"
                  :rules="commonRules"
                  label-width="170px"
                  label-position="right"
                  ref="formInline"
                  :model="formInline"
                  class="demo-form-inline form_inline_search"
                  style="
                    margin-top: 8px;
                    margin-bottom: 10px;
                    margin-left: 80px;
                  "
                >
                  <el-form-item label="管理费" prop="manageFeePrepare">
                    <el-select
                      clearable
                      v-model="formInline.manageFeePrepare"
                      class="el_form_item"
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="(group, index) in manageFeePrepareArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme"
                      >
                      </el-option>
                    </el-select>

                    <el-select
                      clearable
                      v-model="formInline.manageFeeAsset"
                      class="el_form_item"
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="(group, index) in manageFeeAssetArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme"
                      >
                      </el-option>
                    </el-select>

                    <el-select
                      clearable
                      v-model="formInline.manageFeePay"
                      class="el_form_item"
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="(group, index) in manageFeePayArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme"
                      >
                      </el-option>
                    </el-select>
                  </el-form-item>

                  <el-form-item label="托管费" prop="trustFeePrepare">
                    <el-select
                      clearable
                      v-model="formInline.trustFeePrepare"
                      class="el_form_item"
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="(group, index) in manageFeePrepareArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme"
                      >
                      </el-option>
                    </el-select>

                    <el-select
                      clearable
                      v-model="formInline.trustFeeAsset"
                      class="el_form_item"
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="(group, index) in manageFeeAssetArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme"
                      >
                      </el-option>
                    </el-select>

                    <el-select
                      clearable
                      v-model="formInline.trustFeePay"
                      class="el_form_item"
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="(group, index) in manageFeePayArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme"
                      >
                      </el-option>
                    </el-select>
                  </el-form-item>

                  <el-form-item label="运营服务费" prop="operateFeePrepare">
                    <el-select
                      clearable
                      v-model="formInline.operateFeePrepare"
                      class="el_form_item"
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="(group, index) in manageFeePrepareArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme"
                      >
                      </el-option>
                    </el-select>

                    <el-select
                      clearable
                      v-model="formInline.operateFeeAsset"
                      class="el_form_item"
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="(group, index) in manageFeeAssetArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme"
                      >
                      </el-option>
                    </el-select>

                    <el-select
                      clearable
                      v-model="formInline.operateFeePay"
                      class="el_form_item"
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="(group, index) in manageFeePayArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme"
                      >
                      </el-option>
                    </el-select>
                  </el-form-item>

                  <el-col :span="11">
                    <el-form-item label="管理费率(1%填0.01)" prop="manageRate">
                      <el-input-number
                        class="el_form_item"
                        v-model="formInline.manageRate"
                        controls-position="right"
                        @change="handleChange"
                        :min="-999"
                        :max="100"
                      ></el-input-number>
                    </el-form-item>
                    <br />
                    <el-form-item
                      label="运营服务费(1%填0.01)"
                      prop="operateRate"
                    >
                      <el-input-number
                        class="el_form_item"
                        v-model="formInline.operateRate"
                        controls-position="right"
                        @change="handleChange"
                        :min="-999"
                        :max="100"
                      ></el-input-number>
                    </el-form-item>
                    <br />
                    <el-form-item label="管理人账号" prop="manageAccount">
                      <el-input
                        v-model="formInline.manageAccount"
                        placeholder="管理人账号"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />
                    <el-form-item label="业绩报酬" prop="rewardType">
                      <el-select
                        clearable
                        v-model="formInline.rewardType"
                        @change="rewardTypeChange"
                        class="el_form_item"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in rewardTypeArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <br />
                  </el-col>

                  <el-col :span="11" :offset="1">
                    <el-form-item label="托管费率(1%填0.01)" prop="trustRate">
                      <el-input-number
                        class="el_form_item"
                        v-model="formInline.trustRate"
                        controls-position="right"
                        @change="handleChange"
                        :min="-999"
                        :max="100"
                      ></el-input-number>
                    </el-form-item>
                    <br />
                    <el-form-item
                      label="管理人收费账户名称"
                      prop="manageAccountName"
                    >
                      <el-input
                        v-model="formInline.manageAccountName"
                        placeholder="管理人收费账户名称"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />
                    <el-form-item
                      label="管理人开户银行名称"
                      prop="manageBankName"
                    >
                      <el-input
                        v-model="formInline.manageBankName"
                        placeholder="管理人开户银行名称"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />
                  </el-col>
                  <el-form-item
                    v-show="rewardType_show"
                    label="计提方式"
                    prop="rewardPrepareType"
                  >
                    <el-select
                      v-model="formInline.rewardPrepareType"
                      class="el_form_item"
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="(group, index) in rewardPrepareTypeArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme"
                      >
                      </el-option>
                    </el-select>

                    <el-select
                      clearable
                      @change="isFixedPrepareChange"
                      v-model="formInline.isFixedPrepare"
                      class="el_form_item"
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="(group, index) in isFixedPrepareArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme"
                      >
                      </el-option>
                    </el-select>

                    <el-select
                      clearable
                      v-show="rewardPrepareDate_show"
                      v-model="formInline.rewardPrepareDate"
                      class="el_form_item"
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="(group, index) in rewardPrepareDateArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme"
                      >
                      </el-option>
                    </el-select>
                  </el-form-item>
                </el-form>
              </el-row>
              <!--  -->
              <el-row v-if="rewardType_show">
                <el-col :span="18" :offset="4">
                  <el-button
                    type="primary"
                    plain
                    @click="insertEvent('reward')"
                    style="margin-bottom: 5px"
                    size="small"
                  >
                    <i class="el-icon-circle-plus-outline"></i>新增
                  </el-button>
                  <el-button
                    type="danger"
                    plain
                    @click="removeEvent('reward')"
                    style="margin-bottom: 5px"
                    size="small"
                  >
                    <i class="el-icon-delete"></i>移除
                  </el-button>

                  <!-- <el-button type="error"  plain  @click="revertEvent" style="margin-bottom: 5px; " size="small">
                            <i class="el-icon-back"></i>还原
                    </el-button> -->
                  <vxe-table
                    border
                    show-overflow
                    ref="xTableReward"
                    class="my_table_insert"
                    max-height="400"
                    :data="tableDataReward"
                    :edit-config="{
                      trigger: 'click',
                      mode: 'cell',
                      icon: 'fa fa-pencil',
                    }"
                  >
                    <vxe-table-column
                      type="checkbox"
                      width="60"
                    ></vxe-table-column>
                    <vxe-table-column
                      type="seq"
                      title="序号"
                      width="60"
                    ></vxe-table-column>
                    <vxe-table-column
                      field="rewardFrom"
                      title="From"
                      :edit-render="{ name: 'input' }"
                    ></vxe-table-column>
                    <vxe-table-column
                      field="rewardTo"
                      title="To"
                      :edit-render="{ name: 'input' }"
                    ></vxe-table-column>
                    <vxe-table-column
                      field="rewardRate"
                      title="计提比例"
                      :edit-render="{ name: 'input' }"
                    ></vxe-table-column>
                  </vxe-table>
                </el-col>
              </el-row>

              <el-row style="margin-top: 10px">
                <el-col :span="6" :offset="10">
                  <el-button
                    type="primary"
                    plain
                    @click="myTabNext('3')"
                    style="margin-bottom: 5px"
                    size="small"
                  >
                    下一步
                  </el-button>
                  <el-button
                    type="primary"
                    @click="save('formInline')"
                    style="margin-bottom: 5px"
                    >保存</el-button
                  >
                </el-col>
              </el-row>
            </el-col>
          </el-row>
        </div>
      </el-tab-pane>
      <el-tab-pane label="收益分配" name="fourth">
        <div class="product_detail">
          <el-row>
            <el-col :span="23" :offset="1">
              <el-row>
                <el-form
                  :inline="true"
                  :rules="commonRules"
                  label-width="160px"
                  label-position="right"
                  ref="formInline"
                  :model="formInline"
                  class="demo-form-inline form_inline_search"
                  style="
                    margin-top: 8px;
                    margin-bottom: 10px;
                    margin-left: 80px;
                  "
                >
                  <el-form-item label="收益分配说明" prop="incomePortionDesc">
                    <el-input
                      type="textarea"
                      :rows="2"
                      style="width: 590px"
                      placeholder="请输入内容"
                      v-model="formInline.incomePortionDesc"
                    >
                    </el-input>
                  </el-form-item>
                  <br />
                  <el-col :span="11">
                    <el-form-item label="分配次数" prop="portionNumber">
                      <el-select
                        clearable
                        v-model="formInline.portionNumber"
                        class="el_form_item"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in portionNumberArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <br />
                    <el-form-item
                      label="预估数据以及计算报表"
                      prop="dataExpect"
                    >
                      <el-select
                        clearable
                        v-model="formInline.dataExpect"
                        class="el_form_item"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in dataExpectArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <br />
                    <el-form-item label="分红资金交收" prop="bonusDeliver">
                      <el-select
                        clearable
                        v-model="formInline.bonusDeliver"
                        class="el_form_item"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in bonusDeliverArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                  </el-col>

                  <el-col :span="11" :offset="1">
                    <el-form-item label="提交分红流程" prop="bonusProcess">
                      <el-select
                        clearable
                        v-model="formInline.bonusProcess"
                        class="el_form_item"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in bonusProcessArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                    <br />
                    <el-form-item label="分红数据确认" prop="bonusConfim">
                      <el-select
                        clearable
                        v-model="formInline.bonusConfim"
                        class="el_form_item"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in bonusConfimArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        >
                        </el-option>
                      </el-select>
                    </el-form-item>
                  </el-col>
                </el-form>
              </el-row>

              <el-row>
                <el-col :span="6" :offset="10">
                  <el-button
                    type="primary"
                    plain
                    @click="myTabNext('4')"
                    style="margin-bottom: 5px"
                    size="small"
                  >
                    下一步
                  </el-button>
                  <el-button
                    type="primary"
                    @click="save('formInline')"
                    style="margin-bottom: 5px"
                    >保存</el-button
                  >
                </el-col>
              </el-row>
            </el-col>
          </el-row>
        </div>
      </el-tab-pane>
      <el-tab-pane label="账户信息" name="five">
        <div class="product_detail">
          <el-row>
            <el-col :span="23" :offset="1">
              <el-row>
                <el-form
                  :inline="true"
                  :rules="commonRules"
                  label-width="160px"
                  label-position="right"
                  ref="formInline"
                  :model="formInline"
                  class="demo-form-inline form_inline_search"
                  style="
                    margin-top: 8px;
                    margin-bottom: 10px;
                    margin-left: 80px;
                  "
                >
                  <el-col :span="11">
                    <el-form-item label="托管户名称" prop="fiduciaryName">
                      <el-input
                        v-model="formInline.fiduciaryName"
                        placeholder="托管户名称"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />
                    <el-form-item label="托管户开户银行" prop="fiduciaryBank">
                      <el-input
                        v-model="formInline.fiduciaryBank"
                        placeholder="托管户开户银行"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />
                    <el-form-item label="募集户名称" prop="raiseName">
                      <el-input
                        v-model="formInline.raiseName"
                        placeholder="募集户名称"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />
                    <el-form-item label="募集账户开户银行" prop="raiseBank">
                      <el-input
                        v-model="formInline.raiseBank"
                        placeholder="募集账户开户银行"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />
                    <el-form-item label="证券账户名称" prop="securityName">
                      <el-input
                        v-model="formInline.securityName"
                        placeholder="证券账户名称"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />
                    <el-form-item
                      label="上海证券账户-股票交易"
                      prop="stockAccountSh"
                    >
                      <el-input
                        v-model="formInline.stockAccountSh"
                        placeholder="上海证券账户-股票交易"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />
                    <el-form-item
                      label="深圳证券账户-股票交易"
                      prop="stockAccountSz"
                    >
                      <el-input
                        v-model="formInline.stockAccountSz"
                        placeholder="深圳证券账户-股票交易"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />
                    <el-form-item
                      label="证券资金账户"
                      prop="securityCapitalAccount"
                    >
                      <el-input
                        v-model="formInline.securityCapitalAccount"
                        placeholder="证券资金账户"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />

                    <el-form-item label="期权账号" prop="optionAccount">
                      <el-input
                        v-model="formInline.optionAccount"
                        placeholder="管理人账号"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                  </el-col>

                  <el-col :span="11" :offset="1">
                    <el-form-item label="托管户账号" prop="fiduciaryAccount">
                      <el-input
                        v-model="formInline.fiduciaryAccount"
                        placeholder="托管户账号"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />
                    <el-form-item label="托管户年利率" prop="fiduciaryYield">
                      <el-input
                        v-model="formInline.fiduciaryYield"
                        placeholder="托管户年利率"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />
                    <el-form-item label="募集户账号" prop="raiseAccount">
                      <el-input
                        v-model="formInline.raiseAccount"
                        placeholder="募集户账号"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />
                    <el-form-item
                      label="募集账户大额支付号"
                      prop="raiseAccountBig"
                    >
                      <el-input
                        v-model="formInline.raiseAccountBig"
                        placeholder="募集账户大额支付号"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />
                    <el-form-item
                      label="一码通证券账户号码"
                      prop="securityAccount"
                    >
                      <el-input
                        v-model="formInline.securityAccount"
                        placeholder="一码通证券账户号码"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />
                    <el-form-item
                      label="上海证券账户-期权交易"
                      prop="optionAccountSh"
                    >
                      <el-input
                        v-model="formInline.optionAccountSh"
                        placeholder="上海证券账户-期权交易"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />
                    <el-form-item
                      label="深圳证券账户-期权交易"
                      prop="optionAccountSz"
                    >
                      <el-input
                        v-model="formInline.optionAccountSz"
                        placeholder="深圳证券账户-期权交易"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />

                    <el-form-item label="期货账号" prop="futuresAccount">
                      <el-input
                        v-model="formInline.futuresAccount"
                        placeholder="期货账号"
                        type="text"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                  </el-col>
                </el-form>
              </el-row>
              <el-row>
                <el-col :span="6" :offset="10">
                  <el-button
                    type="primary"
                    plain
                    @click="myTabNext('5')"
                    style="margin-bottom: 5px"
                    size="small"
                  >
                    下一步
                  </el-button>
                  <el-button
                    type="primary"
                    @click="save('formInline')"
                    style="margin-bottom: 5px"
                    >保存</el-button
                  >
                </el-col>
              </el-row>
            </el-col>
          </el-row>
        </div>
      </el-tab-pane>
      <el-tab-pane label="投资风控" name="six">
        <div class="product_detail">
          <el-row>
            <el-col :span="23" :offset="1">
              <!-- <el-row>
                  <el-col :span="1"><span style="font-weight: bold">投资范围:</span></el-col>
                  <el-col :span="22">
                       <div class="product_detail">
                      <el-row>
                         <el-checkbox-group v-model="checkfundInvestArea">
                        <el-col :span="12">
                            <div v-for="(group, index) in fundInvestArea"  :key="index" >
                                   <el-checkbox v-if="index%2 ==0" :label="group.dimNme"></el-checkbox>
                            </div>
                        </el-col>
                        <el-col :span="11" :offset="1">
                            <div v-for="(group, index) in fundInvestArea"  :key="index">
                                   <el-checkbox v-if="index%2 !=0" :label="group.dimNme"></el-checkbox>
                            </div>
                        </el-col>
                         </el-checkbox-group>
                      </el-row>
                   </div>
                  </el-col>
                </el-row> -->

              <el-form
                :inline="true"
                :rules="commonRules"
                label-width="150px"
                label-position="right"
                ref="formInline"
                :model="formInline"
                class="demo-form-inline form_inline_search"
                style="margin-top: 8px; margin-bottom: 10px; margin-left: 80px"
              >
                <el-form-item label="投资范围">
                  <div class="product_detail">
                    <el-checkbox
                      :indeterminate="isIndeterminate"
                      v-model="checkAll"
                      @change="handleCheckAllChange"
                      >全选</el-checkbox
                    >
                    <div style="margin: 15px 0"></div>
                    <el-checkbox-group
                      v-model="checkfundInvestArea"
                      @change="handleCheckedInvestAreaChange"
                    >
                      <div
                        v-for="(group, index) in fundInvestArea"
                        :key="index"
                      >
                        <el-checkbox :label="group.dimCde">{{
                          group.dimNme
                        }}</el-checkbox>
                      </div>
                    </el-checkbox-group>
                  </div>
                </el-form-item>
                <br />

                <el-form-item label="投资限制" prop="investLimit">
                  <el-input
                    type="textarea"
                    :rows="4"
                    style="width: 605px"
                    placeholder="请输入内容"
                    v-model="formInline.investLimit"
                  >
                  </el-input>
                </el-form-item>
                <br />
                <el-form-item label="预警线" prop="warnPoint">
                  <el-input
                    class="el_form_item"
                    v-model="formInline.warnPoint"
                    placeholder="预警线"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  label="止损线"
                  prop="lossPoint"
                  label-width="215px"
                >
                  <el-input
                    class="el_form_item"
                    v-model="formInline.lossPoint"
                    placeholder="止损线"
                  ></el-input>
                </el-form-item>
              </el-form>

              <el-row>
                <el-col :span="6" :offset="10">
                  <el-button
                    type="primary"
                    plain
                    @click="myTabNext('6')"
                    style="margin-bottom: 5px"
                    size="small"
                  >
                    下一步
                  </el-button>
                  <el-button
                    type="primary"
                    @click="save('formInline')"
                    style="margin-bottom: 5px"
                    >保存</el-button
                  >
                </el-col>
              </el-row>
            </el-col>
          </el-row>
        </div>
      </el-tab-pane>
      <el-tab-pane label="分级关系" v-if="isFj_show" name="eight">
        <div
          class="product_detail"
          v-if="
            PageDataAdd.fjgx_show || PageDataAdd.formData.fundGrades.length > 0
          "
        >
          <el-row>
            <el-col :span="23" :offset="1">
              <div style="height: 10px">
                <el-button
                  type="primary"
                  plain
                  @click="insertEvent('grade', -1)"
                  style="margin-bottom: 5px"
                  size="small"
                >
                  <i class="el-icon-circle-plus-outline"></i>新增
                </el-button>
                <el-button
                  type="danger"
                  plain
                  @click="removeEvent('grade')"
                  style="margin-bottom: 5px"
                  size="small"
                >
                  <i class="el-icon-delete"></i>移除
                </el-button>
              </div>
              <!-- <el-button type="error"  plain  @click="revertEvent" style="margin-bottom: 5px; " size="small">
                    <i class="el-icon-back"></i>还原
            </el-button> 
            :edit-rules="validRulesGrade"
            -->

              <div style="margin-top: 30px">
                <vxe-table
                  border
                  show-overflow
                  keep-source
                  ref="xTableGrade"
                  width="auto"
                  max-height="400"
                  :data="tableDataGrade"
                  :edit-config="{
                    trigger: 'click',
                    mode: 'cell',
                    showStatus: true,
                    activeMethod: activeCellMethodGrade,
                  }"
                >
                  <vxe-table-column
                    type="checkbox"
                    width="10%"
                  ></vxe-table-column>
                  <vxe-table-column
                    type="seq"
                    title="序号"
                    width="10%"
                  ></vxe-table-column>
                  <vxe-table-column
                    width="15%"
                    field="fundNameGrade"
                    title="分级名称"
                    :edit-render="{
                      name: '$select',
                      placement: 'bottom',
                      options: fundNameGradeArr,
                      optionProps: { value: 'fundName', label: 'fundName' },
                      events: { change: fundNameGradeChangeEvent },
                    }"
                  ></vxe-table-column>
                  <vxe-table-column
                    width="20%"
                    field="fundCodeGrade"
                    title="分级代码"
                    :edit-render="{ name: 'input' }"
                  ></vxe-table-column>
                  <!-- <vxe-table-column width="15%" field="fundNameGrade" title="分级名称" :edit-render="{name: 'input'}"></vxe-table-column> -->
                  <vxe-table-column
                    width="20%"
                    field="shareType"
                    title="份额类型"
                    :edit-render="{
                      name: 'select',
                      placement: 'bottom',
                      options: shareTypeArr,
                      optionProps: { value: 'dimCde', label: 'dimNme' },
                    }"
                  ></vxe-table-column>
                  <vxe-table-column
                    width="20%"
                    field="leverageRatio"
                    title="杠杆比例"
                    :edit-render="{ name: 'input' }"
                  ></vxe-table-column>
                </vxe-table>
              </div>
            </el-col>
          </el-row>

          <el-row style="margin-top: 10px">
            <el-col :span="6" :offset="10">
              <el-button
                type="primary"
                plain
                @click="myTabNext('7')"
                style="margin-bottom: 5px"
                size="small"
              >
                下一步
              </el-button>
              <el-button
                type="primary"
                @click="save('formInline')"
                style="margin-bottom: 5px"
                >保存</el-button
              >
            </el-col>
          </el-row>
        </div>
      </el-tab-pane>
      <el-tab-pane label="销售方式" name="nine">
        <div
          v-if="
            PageDataAdd.xsfs_show || PageDataAdd.formData.fundSallers.length > 0
          "
          class="product_detail"
        >
          <el-row>
            <el-col :span="23" :offset="1">
              <div style="height: 10px">
                <span>销售方式:</span>
                <el-select
                  clearable
                  v-model="formInline.saleType"
                  @change="saleTypeChange"
                  class="el_form_item"
                  placeholder="请选择"
                >
                  <el-option
                    v-for="(group, index) in saleTypeArr"
                    :value="group.dimCde"
                    :key="index"
                    :label="group.dimNme"
                  >
                  </el-option>
                </el-select>

                <el-button
                  type="primary"
                  plain
                  @click="insertEvent('saller', -1)"
                  style="margin-bottom: 5px"
                  size="small"
                >
                  <i class="el-icon-circle-plus-outline"></i>新增
                </el-button>
                <el-button
                  type="danger"
                  plain
                  @click="removeEvent('saller')"
                  style="margin-bottom: 5px"
                  size="small"
                >
                  <i class="el-icon-delete"></i>移除
                </el-button>
              </div>
              <!-- <el-button type="error"  plain  @click="revertEvent" style="margin-bottom: 5px; " size="small">
                    <i class="el-icon-back"></i>还原
            </el-button> -->

              <div style="margin-top: 30px">
                <vxe-table
                  border
                  show-overflow
                  keep-source
                  ref="xTableMySaller"
                  width="auto"
                  max-height="400"
                  :data="tableDataSaller"
                  :edit-config="{
                    trigger: 'click',
                    mode: 'cell',
                    showStatus: true,
                    activeMethod: activeCellMethod,
                  }"
                >
                  <vxe-table-column
                    type="checkbox"
                    width="5%"
                  ></vxe-table-column>
                  <vxe-table-column
                    type="seq"
                    title="序号"
                    width="10%"
                  ></vxe-table-column>
                  <vxe-table-column
                    width="10%"
                    field="sallerName"
                    title="渠道名称"
                    :edit-render="{
                      name: '$select',
                      placement: 'bottom',
                      options: sallerNameArr,
                      optionProps: { value: 'sallerName', label: 'sallerName' },
                      events: { change: sallerNameChangeEvent },
                    }"
                  ></vxe-table-column>
                  <vxe-table-column
                    width="15%"
                    field="sallerCode"
                    title="渠道编码"
                    :edit-render="{ name: 'input' }"
                  ></vxe-table-column>
                  <vxe-table-column
                    width="15%"
                    field="sallerType"
                    title="销售方式"
                    :edit-render="{
                      name: 'select',
                      placement: 'bottom',
                      options: saleTypeArr,
                      optionProps: { value: 'dimCde', label: 'dimNme' },
                    }"
                  ></vxe-table-column>
                  <vxe-table-column
                    width="15%"
                    field="feeRate"
                    title="管理费分成比例"
                    :edit-render="{ name: 'input', attrs: { type: 'text' } }"
                  ></vxe-table-column>
                  <vxe-table-column
                    width="15%"
                    field="beginDate"
                    title="开始日期"
                    :edit-render="{ name: '$input', props: { type: 'date' } }"
                  ></vxe-table-column>
                  <vxe-table-column
                    width="15%"
                    field="endDate"
                    title="结束日期"
                    :edit-render="{ name: '$input', props: { type: 'date' } }"
                  ></vxe-table-column>
                </vxe-table>
              </div>
            </el-col>
          </el-row>
          <el-row style="margin-top: 10px">
            <el-col :span="6" :offset="10">
              <el-button
                type="primary"
                plain
                @click="myTabNext('8')"
                style="margin-bottom: 5px"
                size="small"
              >
                下一步
              </el-button>
              <el-button
                type="primary"
                @click="save('formInline')"
                style="margin-bottom: 5px"
                >保存</el-button
              >
            </el-col>
          </el-row>
        </div>
      </el-tab-pane>
      <el-tab-pane label="开放日" name="ten">
        <div
          v-if="
            PageDataAdd.kfr_show || PageDataAdd.formData.fundOpens.length > 0
          "
          class="product_detail"
        >
          <el-row>
            <el-col :span="23" :offset="1">
              <div style="height: 10px">
                <span>是否可以设置临开:</span>
                <el-select
                  clearable
                  v-model="formInline.isOpenShort"
                  class="el_form_item"
                  placeholder="请选择"
                >
                  <el-option
                    v-for="(group, index) in isOpenShortArr"
                    :value="group.dimCde"
                    :key="index"
                    :label="group.dimNme"
                  >
                  </el-option>
                </el-select>

                <el-button
                  type="primary"
                  plain
                  @click="insertEvent('open', -1)"
                  style="margin-bottom: 5px"
                  size="small"
                >
                  <i class="el-icon-circle-plus-outline"></i>新增
                </el-button>
                <el-button
                  type="danger"
                  plain
                  @click="removeEvent('open')"
                  style="margin-bottom: 5px"
                  size="small"
                >
                  <i class="el-icon-delete"></i>移除
                </el-button>
              </div>
              <!-- <el-button type="error"  plain  @click="revertEvent" style="margin-bottom: 5px; " size="small">
                    <i class="el-icon-back"></i>还原
            </el-button> -->

              <div style="margin-top: 30px">
                <vxe-table
                  border
                  show-overflow
                  keep-source
                  ref="xTableMyOpen"
                  width="auto"
                  max-height="400"
                  :data="tableDataOpen"
                  :edit-config="{
                    trigger: 'click',
                    mode: 'cell',
                    showStatus: true,
                  }"
                >
                  <vxe-table-column
                    type="checkbox"
                    width="10%"
                  ></vxe-table-column>
                  <vxe-table-column
                    type="seq"
                    title="序号"
                    width="10%"
                  ></vxe-table-column>
                  <vxe-table-column
                    width="15%"
                    field="openFrequence"
                    title="开放频率"
                    :edit-render="{
                      name: 'select',
                      placement: 'bottom',
                      options: openFrequenceArr,
                      optionProps: { value: 'dimCde', label: 'dimNme' },
                    }"
                  ></vxe-table-column>
                  <vxe-table-column
                    width="20%"
                    field="openRule"
                    title="开放规则"
                    :edit-render="{
                      name: 'select',
                      placement: 'bottom',
                      options: openRuleArr,
                      optionProps: { value: 'dimCde', label: 'dimNme' },
                    }"
                  ></vxe-table-column>
                  <vxe-table-column
                    width="20%"
                    field="beginDate"
                    title="规则生效日期"
                    :edit-render="{ name: '$input', props: { type: 'date' } }"
                  ></vxe-table-column>
                  <vxe-table-column
                    width="20%"
                    field="endDate"
                    title="规则失效日期"
                    :edit-render="{ name: '$input', props: { type: 'date' } }"
                  ></vxe-table-column>
                </vxe-table>
              </div>
            </el-col>
          </el-row>
          <el-row style="margin-top: 10px">
            <el-col :span="6" :offset="10">
              <el-button
                type="primary"
                plain
                @click="myTabNext('9')"
                style="margin-bottom: 5px"
                size="small"
              >
                下一步
              </el-button>
              <el-button
                type="primary"
                @click="save('formInline')"
                style="margin-bottom: 5px"
                >保存</el-button
              >
            </el-col>
          </el-row>
        </div>
      </el-tab-pane>
      <el-tab-pane label="基金经理" name="eleven">
        <div
          v-if="
            PageDataAdd.fundManager_show ||
            PageDataAdd.formData.fundManagers.length > 0
          "
          class="product_detail"
        >
          <el-row>
            <el-col :span="23" :offset="1">
              <el-button
                type="primary"
                plain
                @click="insertEvent('fundManager', -1)"
                style="margin-bottom: 5px"
                size="small"
              >
                <i class="el-icon-circle-plus-outline"></i>新增
              </el-button>
              <el-button
                type="danger"
                plain
                @click="removeEvent('fundManager')"
                style="margin-bottom: 5px"
                size="small"
              >
                <i class="el-icon-delete"></i>移除
              </el-button>

              <!-- <el-button type="error"  plain  @click="revertEvent" style="margin-bottom: 5px; " size="small">
                    <i class="el-icon-back"></i>还原
            </el-button> -->
              <div style="margin-top: 0px">
                <vxe-table
                  border
                  show-overflow
                  keep-source
                  ref="xTableFundManager"
                  width="auto"
                  max-height="400"
                  :edit-rules="validRulesFundManager"
                  :data="tableDataFundManager"
                  :edit-config="{
                    trigger: 'click',
                    mode: 'cell',
                    showStatus: true,
                  }"
                >
                  <vxe-table-column
                    type="checkbox"
                    width="10%"
                  ></vxe-table-column>
                  <vxe-table-column
                    type="seq"
                    title="序号"
                    width="10%"
                  ></vxe-table-column>
                  <vxe-table-column
                    width="15%"
                    field="managerName"
                    title="基金经理"
                    :edit-render="{
                      name: '$select',
                      placement: 'bottom',
                      options: managerNameArr,
                      optionProps: { value: 'name', label: 'name' },
                      events: { change: managerNameChangeEvent },
                    }"
                  ></vxe-table-column>
                  <vxe-table-column
                    field="investStrategy"
                    title="投资策略"
                  ></vxe-table-column>
                  <vxe-table-column
                    field="phone"
                    title="联系电话"
                  ></vxe-table-column>
                  <vxe-table-column
                    field="email"
                    title="联系邮箱"
                  ></vxe-table-column>
                </vxe-table>
              </div>
            </el-col>
          </el-row>

          <el-row style="margin-top: 10px">
            <el-col :span="6" :offset="10">
              <el-button
                type="primary"
                plain
                @click="myTabNext('10')"
                style="margin-bottom: 5px"
                size="small"
              >
                下一步
              </el-button>
              <el-button
                type="primary"
                @click="save('formInline')"
                style="margin-bottom: 5px"
                >保存</el-button
              >
            </el-col>
          </el-row>
        </div>
      </el-tab-pane>
      <el-tab-pane label="联系人" name="seven">
        <div
          v-if="
            PageDataAdd.lxr_show || PageDataAdd.formData.fundContacts.length > 0
          "
          class="product_detail"
        >
          <el-row>
            <el-col :span="23" :offset="1">
              <el-button
                type="primary"
                plain
                @click="insertEvent('contact', -1)"
                style="margin-bottom: 5px"
                size="small"
              >
                <i class="el-icon-circle-plus-outline"></i>新增
              </el-button>
              <el-button
                type="danger"
                plain
                @click="removeEvent('contact')"
                style="margin-bottom: 5px"
                size="small"
              >
                <i class="el-icon-delete"></i>移除
              </el-button>

              <!-- <el-button type="error"  plain  @click="revertEvent" style="margin-bottom: 5px; " size="small">
                    <i class="el-icon-back"></i>还原
            </el-button> -->

              <vxe-table
                border
                show-overflow
                keep-source
                ref="xTableContact"
                :edit-rules="validRulesContact"
                :data="tableDataContact"
                :edit-config="{
                  trigger: 'click',
                  mode: 'cell',
                  showStatus: true,
                }"
              >
                <vxe-table-column
                  type="checkbox"
                  width="10%"
                ></vxe-table-column>
                <vxe-table-column
                  type="seq"
                  title="序号"
                  width="60"
                ></vxe-table-column>
                <vxe-table-column
                  field="contactType"
                  title="联系人类型"
                  :edit-render="{ name: 'input', attrs: { type: 'text' } }"
                ></vxe-table-column>
                <vxe-table-column
                  field="contactName"
                  title="联系人名称"
                  :edit-render="{ name: 'input', attrs: { type: 'text' } }"
                ></vxe-table-column>
                <vxe-table-column
                  field="contactPhone"
                  title="联系人电话"
                  :edit-render="{ name: 'input', attrs: { type: 'text' } }"
                ></vxe-table-column>
                <vxe-table-column
                  field="contactMail"
                  title="联系人邮箱"
                  :edit-render="{ name: 'input', attrs: { type: 'text' } }"
                ></vxe-table-column>
              </vxe-table>
            </el-col>
          </el-row>
        </div>
      </el-tab-pane>
    </el-tabs>

    <div v-show="bc_show" style="margin-top: 10px">
      <el-row>
        <el-col :span="3" :offset="12">
          <el-button
            type="primary"
            v-show="bc_show"
            @click="save('formInline')"
            style="margin-bottom: 5px"
            >保存</el-button
          >
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import productDictionary from "@/dataDictionary/product";
import commonFun from "@/filters/new_common";
import pageApi from "@/api/product/productSearch";
import Pagination from "@/components/Pagination";
export default {
  name: "productAdd",
  components: {
    Pagination,
  },
  props: {
    PageDataAdd: {
      addType: -1, //-1新增，0修改，1复制新增
      fundCode: "",
      isAdd: false,
      fjgx_show: false,
      fundManager_show: false,
      kfr_show: false,
      xsfs_show: false,
      lxr_show: false,
      formData: {},
    },
  },
  data() {
    const contactNameValid = ({ cellValue }) => {
      return new Promise((resolve, reject) => {
        if (cellValue.length < 3 || cellValue.length > 20) {
          reject(new Error("名称长度在 3 到 20 个字符之间"));
        } else {
          resolve();
        }
      });
    };
    return {
      activeName: "first",
      aa: 9999,
      sexList: [],
      formInline: {
        fundName: "", //产品名称
        fundCode: "", //产品代码
        fundNameEn: "", //英文名称
        managerCode: "", //管理人名称
        trustorCode: "", //托管人名称
        operatorCode: "", //基金服务机构
        fundType: "", //基金类型
        riskLevel: "", //风险等级
        investDirect: "", //投资方向
        operateDept: "", //证券营业部
        setupDate: "", //基金成立日期
        holdYear: "", //产品存续期限
        recordDate: "", //基金备案日期
        operateType: "", //运作方式
        recordCode: "", //产品备案代码
        fundState: "", //产品状态
        isGrade: "", //是否分级
        saleType: "", //销售方式
        isOpenShort: "", //是否可以设置临开
        blockDate: "", //封闭期
        purchasePoint: "", //认申购起点（不含费）
        purchaseDiffAppend: "", //追加认申购级差
        subscribeConfirmDay: "", //认购交易确认天数
        subscribeDeliverDay: "", //认购资金交收天数
        subscribeRate: "", //认购费率
        applyConfirmDay: "", //申购交易确认天数
        applyDeliverDay: "", //申购资金交收天数
        applyRate: "", //申购费率
        saleFeePrepare: "", //销售服务费计提
        saleFeePay: "", //销售服务费支付
        callConfirmDay: "", //赎回交易确认天数
        callFloatType: "", //赎回费率浮动类型
        callRate: "", //赎回费率
        callRateType: "", //赎回费率类型
        callDeliverDay: "", //赎回资金交收天数
        manageFeePrepare: "", //管理费
        manageFeeAsset: "", //管理费
        manageFeePay: "", //管理费
        trustFeePrepare: "", //托管费
        trustFeeAsset: "", //托管费
        trustFeePay: "", //托管费
        operateFeePrepare: "", //运营服务费
        operateFeeAsset: "", //运营服务费
        operateFeePay: "", //运营服务费
        manageRate: "", //管理费率
        trustRate: "", //托管费率
        operateRate: "", //运营服务费
        manageAccountName: "", //管理人收费账户名称
        manageAccount: "", //管理人账号
        manageBankName: "", //管理人开户银行名称
        rewardType: "", //业绩报酬
        rewardPrepareType: "", //计提方式
        isFixedPrepare: "", //计提方式
        rewardPrepareDate: "", //计提方式
        incomePortionDesc: "", //收益分配说明
        portionNumber: "", //分配次数
        bonusProcess: "", //提交分红流程
        dataExpect: "", //预估数据以及计算报表
        bonusConfim: "", //分红数据确认
        bonusDeliver: "", //分红资金交收
        fiduciaryName: "", //托管户名称
        fiduciaryAccount: "", //托管户账号
        fiduciaryBank: "", //托管户开户银行
        fiduciaryYield: "", //托管户年利率
        raiseName: "", //募集户名称
        raiseAccount: "", //募集户账号
        raiseBank: "", //募集账户开户银行
        raiseAccountBig: "", //募集账户大额支付号
        securityName: "", //证券账户名称
        securityAccount: "", //一码通证券账户号码
        stockAccountSh: "", //上海证券账户-股票交易
        optionAccountSh: "", //上海证券账户-期权交易
        stockAccountSz: "", //深圳证券账户-股票交易
        optionAccountSz: "", //深圳证券账户-期权交易
        securityCapitalAccount: "", //证券资金账户
        futuresAccount: "", //期货账号
        optionAccount: "", //期权账号
        investLimit: "", //投资限制
        warnPoint: "", //预警线
        lossPoint: "", //止损线
      },
      formInlineKfr: {}, //开放日
      jcxx_show: true, //基础信息展示
      jyxx_show: false, //交易信息展示
      fyxx_show: false, //费用信息展示
      syfp_show: false, //收益分配展示
      zhxx_show: false, //账户信息展示
      tzfk_show: false, //投资风控展示
      lxr_show: true, //联系人展示
      fjgx_show: true, //分级关系展示
      xsfs_show: true, //销售方式展示
      xsfsIf_show: true,
      kfr_show: true, //开放日展示
      kfrIf_show: false, //开放日展示
      tableData: [], //联系人列表
      bc_show: false,
      nameArr: [],
      managerCodeArr: [], //管理人-数组
      trustorCodeArr: [], //托管人-数组
      operatorCodeArr: [], //基金服务机构-数组
      investDirectArr: [], //投资方向-数组
      riskLevelArr: [], //风险等级-数组
      operateTypeArr: [], //运作方式-数组
      fundStateArr: [], //产品状态-数组
      isGradeArr: [], //是否分级-数组
      fundTypeArr: [], //基金类型-数组
      //交易
      saleTypeArr: [], //销售方式-数组
      isOpenShortArr: [], //是否可以设置临开-数组
      subscribeConfirmDayArr: [], //认购交易确认天数-数组
      subscribeDeliverDayArr: [], //认购资金交收天数-数组
      applyConfirmDayArr: [], //申购交易确认天数-数组
      applyDeliverDayArr: [], //申购资金交收天数-数组
      saleFeePrepareArr: [], //销售服务费计提-数组
      saleFeePayArr: [], //销售服务费支付-数组
      callConfirmDayArr: [], //赎回交易确认天数-数组
      callFloatTypeArr: [], //赎回费率浮动类型-数组
      callRateTypeArr: [], //赎回费率类型-数组
      callDeliverDayArr: [], //赎回资金交收天数-数组
      manageFeePrepareArr: [], //管理费-数组
      manageFeeAssetArr: [], //管理费-数组
      manageFeePayArr: [], //管理费-数组
      trustFeePrepareArr: [], //托管费-数组
      trustFeeAssetArr: [], //托管费-数组
      trustFeePayArr: [], //托管费-数组
      operateFeePrepareArr: [], //运营服务费-数组
      operateFeeAssetArr: [], //运营服务费-数组
      operateFeePayArr: [], //运营服务费-数组
      rewardTypeArr: [], //业绩报酬-数组
      rewardPrepareTypeArr: [], //计提方式-数组
      isFixedPrepareArr: [], //计提方式-数组
      rewardPrepareDateArr: [], //计提方式-数组
      portionNumberArr: [], //分配次数-数组
      bonusProcessArr: [], //提交分红流程-数组
      dataExpectArr: [], //预估数据以及计算报表-数组
      bonusConfimArr: [], //分红数据确认-数组
      bonusDeliverArr: [], //分红资金交收-数组
      shareTypeArr: [], //份额类型-数组
      fundNameGradeArr: [], //分级代码
      isFj_show: false, // 分级tab是否展示
      callFloat_input_show: false, //赎回费率_input是否展示
      callFloat_select_show: false, //赎回费率_select是否展示
      rewardType_show: false, //计提方式 是否展示
      rewardPrepareDate_show: false, //计提方式日期 是否展示

      tableDataRedeem: [], //赎回费率列表数据
      tableDataReward: [], //计提列表数据
      tableDataContact: [], //联系人列表数据
      tableDataGrade: [], //分级列表数据
      tableDataSaller: [], //销售方式列表数据
      tableDataOpen: [], //开放日列表数据

      validContactFlag: true, //校验联系人
      validRewardtFlag: true, //校验计提
      validRedeemFlag: true, //校验赎回费率
      validGradeFlag: true, //校验分级
      validSallerFlag: true, //校验销售方式
      validOpenFlag: true, //校验开放日
      validFundManagerFlag: true, //校验基金经理

      //开放日
      total: 0, //列表条数
      pageNum: 1, //页码
      tableDataKfr: [], //列表数据
      tableLoading: false, //列表加载
      pageSize: 10, //条数
      formLabelWidth: "120",
      insertDayRuleDialog: false,
      forminsertDayRule: {
        name: "",
        name1: "",
        name2: "",
        name3: "",
        name4: "",
        name5: "",
        name6: "",
      },
      fundInvestArea: [], //投资范围
      checkfundInvestArea: [], //投资范围选择
      sallerNameArr: [], //渠道名称数组
      openFrequenceArr: [], //开放频率数组
      openRuleArr: [], //开放规则数组

      // 弹窗验证规则
      commonRules: {
        fundName: [
          { required: true, message: "请输入产品名称", trigger: "blur" },
        ],
        fundCode: [
          { required: true, message: "请输入产品代码", trigger: "blur" },
        ],
        fundType: [
          { required: true, message: "请选择基金类型", trigger: "change" },
        ],
        investDirect: [
          { required: true, message: "请选择投资方向", trigger: "change" },
        ],
        holdYear: [
          { required: true, message: "请输入产品存续期限", trigger: "blur" },
        ],
        riskLevel: [
          { required: true, message: "请选择风险等级", trigger: "change" },
        ],
        fundState: [
          { required: true, message: "请选择产品状态", trigger: "change" },
        ],
        isGrade: [
          { required: true, message: "请选择是否分级", trigger: "change" },
        ],
        purchasePoint: [
          {
            required: true,
            message: "请输入认申购起点（不含费）",
            trigger: "blur",
          },
        ],
        purchaseDiffAppend: [
          { required: true, message: "请输入追加认申购级差", trigger: "blur" },
        ],
        subscribeRate: [
          { required: true, message: "请输入认购费率", trigger: "blur" },
        ],
        subscribeConfirmDay: [
          {
            required: true,
            message: "请选择认购交易确认天数",
            trigger: "change",
          },
        ],
        subscribeDeliverDay: [
          {
            required: true,
            message: "请选择认购资金交收天数",
            trigger: "change",
          },
        ],
        applyConfirmDay: [
          {
            required: true,
            message: "请选择申购交易确认天数",
            trigger: "change",
          },
        ],
        applyDeliverDay: [
          {
            required: true,
            message: "请选择申购资金交收天数",
            trigger: "change",
          },
        ],
        callConfirmDay: [
          {
            required: true,
            message: "请选择赎回交易确认天数",
            trigger: "change",
          },
        ],
        callFloatType: [
          {
            required: true,
            message: "请选择赎回费率浮动类型",
            trigger: "change",
          },
        ],
        callDeliverDay: [
          {
            required: true,
            message: "请选择赎回资金交收天数",
            trigger: "change",
          },
        ],
      },
      callRateTypeRul: {
        required: true,
        message: "请选择赎回费率类型",
        trigger: "change",
      },
      callRateRul: {
        required: true,
        message: "请输入赎回费率",
        trigger: "blur",
      },

      //联系人校验规则
      validRulesContact: {
        contactName: [
          { required: true, message: "请填写联系人名称" },
          // { validator: contactNameValid }
        ],
        contactType: [{ required: true, message: "请填写联系人类型" }],
        contactPhone: [
          { pattern: /^1(3|4|5|6|7|8|9)\d{9}$/, message: "格式不正确" },
        ],
        contactMail: [
          { pattern: /^\w+@[a-z0-9]+\.[a-z]{2,4}$/, message: "格式不正确" },
        ],
      },
      //分级校验规则
      validRulesGrade: {
        fundCodeGrade: [{ required: true, message: "请填写分级名称" }],
        fundNameGrade: [{ required: true, message: "请选择分级代码" }],
        shareType: [{ required: true, message: "请填写份额类型" }],
        leverageRatio: [{ required: true, message: "请填写杠杆比例" }],
      },
      checkAll: false,
      isIndeterminate: true,
      fundManager_show: true,
      fundManagerIf_show: false,
      tableDataFundManager: [],
      validRulesFundManager: {
        managerName: [{ required: true, message: "请填写基金经理" }],
        phone: [{ pattern: /^1(3|4|5|6|7|8|9)\d{9}$/, message: "格式不正确" }],
        email: [
          { pattern: /^\w+@[a-z0-9]+\.[a-z]{2,4}$/, message: "格式不正确" },
        ],
      },
      managerNameArr: [], //基金经理数据
      isSave: false, //判断是否点击保存
    };
  },
  //页面加载后触发
  mounted() {
    //初始化数据
    this.initData();
    this.getEdims(); //获取数据字典
    let type = this.PageDataAdd.addType;

    if (type != -1) {
      this.getDetail();
    }
  },
  methods: {
    //列表选择
    handleSelectionChange(val) {
      this.tableMultipleSelection = val;
    },
    //排序
    handleSortChange(val) {
      this.formInline.orderStr = commonFun.orderByString(val);
      //this.selectAll(false);
    },
    //分页
    Pagination(val) {
      this.formInline.pageSize = val.limit; //页面条数
      this.pageNum = val.page; //页码
      this.formInline.offset = (val.page - 1) * val.limit;
      //this.selectAll( false);
    },
    myTabNext(val) {
      let params = {};
      if (val === "1") {
        params.label = "交易信息";
        this.activeName = "second";
        this.handleClick(params, "");
      } else if (val === "2") {
        params.label = "费用信息";
        this.activeName = "third";
        this.handleClick(params, "");
      } else if (val === "3") {
        params.label = "收益分配";
        this.activeName = "fourth";
        this.handleClick(params, "");
      } else if (val === "4") {
        params.label = "账户信息";
        this.activeName = "five";
        this.handleClick(params, "");
      } else if (val === "5") {
        params.label = "投资风控";
        this.activeName = "six";
        this.handleClick(params, "");
      } else if (val === "6") {
        if (this.isFj_show) {
          params.label = "分级关系";
          this.activeName = "eight";
          this.handleClick(params, "");
        } else {
          params.label = "销售方式";
          this.activeName = "nine";
          this.handleClick(params, "");
        }
      } else if (val === "7") {
        params.label = "销售方式";
        this.activeName = "nine";
        this.handleClick(params, "");
      } else if (val === "8") {
        params.label = "开放日";
        this.activeName = "ten";
        this.handleClick(params, "");
      } else if (val === "9") {
        params.label = "基金经理";
        this.activeName = "eleven";
        this.handleClick(params, "");
      } else if (val === "10") {
        params.label = "联系人";
        this.activeName = "seven";
        this.handleClick(params, "");
      }
    },
    handleClick(tab, event) {
      let tabLabel = tab.label;
      //this.fullValidEvent();
      this.initTable();
      // if(!this.PageDataAdd.isAdd){
      //     return;
      // }
      if (tabLabel === "基础信息") {
        this.jcxx_show = true; //基础信息展示
        this.jyxx_show = false; //交易信息展示
        this.fyxx_show = false; //费用信息展示
        this.syfp_show = false; //收益分配展示
        this.zhxx_show = false; //账户信息展示
        this.tzfk_show = false; //投资风控展示
        this.lxr_show = false; //联系人展示
        this.fjgx_show = false; //分级关系展示
        this.bc_show = false; //保存按钮展示
        this.xsfs_show = false; //销售方式
        this.kfr_show = false; //开放日
        this.fundManagerIf_show = false; //基金经理
      } else if (tabLabel === "交易信息") {
        this.jcxx_show = false; //基础信息展示
        this.jyxx_show = true; //交易信息展示
        this.fyxx_show = false; //费用信息展示
        this.syfp_show = false; //收益分配展示
        this.zhxx_show = false; //账户信息展示
        this.tzfk_show = false; //投资风控展示
        this.lxr_show = false; //联系人展示
        this.fjgx_show = false; //分级关系展示
        this.bc_show = false; //保存按钮展示
        this.xsfs_show = false; //销售方式
        this.kfr_show = false; //开放日
        this.fundManagerIf_show = false; //基金经理
      } else if (tabLabel === "费用信息") {
        this.jcxx_show = false; //基础信息展示
        this.jyxx_show = false; //交易信息展示
        this.fyxx_show = true; //费用信息展示
        this.syfp_show = false; //收益分配展示
        this.zhxx_show = false; //账户信息展示
        this.tzfk_show = false; //投资风控展示
        this.lxr_show = false; //联系人展示
        this.fjgx_show = false; //分级关系展示
        this.bc_show = false; //保存按钮展示
        this.xsfs_show = false; //销售方式
        this.kfr_show = false; //开放日
        this.fundManagerIf_show = false; //基金经理
      } else if (tabLabel === "收益分配") {
        this.jcxx_show = false; //基础信息展示
        this.jyxx_show = false; //交易信息展示
        this.fyxx_show = false; //费用信息展示
        this.syfp_show = true; //收益分配展示
        this.zhxx_show = false; //账户信息展示
        this.tzfk_show = false; //投资风控展示
        this.lxr_show = false; //联系人展示
        this.fjgx_show = false; //分级关系展示
        this.bc_show = false; //保存按钮展示
        this.xsfs_show = false; //销售方式
        this.kfr_show = false; //开放日
        this.fundManagerIf_show = false; //基金经理
      } else if (tabLabel === "账户信息") {
        this.jcxx_show = false; //基础信息展示
        this.jyxx_show = false; //交易信息展示
        this.fyxx_show = false; //费用信息展示
        this.syfp_show = false; //收益分配展示
        this.zhxx_show = true; //账户信息展示
        this.tzfk_show = false; //投资风控展示
        this.lxr_show = false; //联系人展示
        this.fjgx_show = false; //分级关系展示
        this.bc_show = false; //保存按钮展示
        this.xsfs_show = false; //销售方式
        this.kfr_show = false; //开放日
        this.fundManagerIf_show = false; //基金经理
      } else if (tabLabel === "投资风控") {
        this.jcxx_show = false; //基础信息展示
        this.jyxx_show = false; //交易信息展示
        this.fyxx_show = false; //费用信息展示
        this.syfp_show = false; //收益分配展示
        this.zhxx_show = false; //账户信息展示
        this.tzfk_show = true; //投资风控展示
        this.lxr_show = false; //联系人展示
        this.fjgx_show = false; //分级关系展示
        this.bc_show = false; //保存按钮展示
        this.xsfs_show = false; //销售方式
        this.kfr_show = false; //开放日
        this.fundManagerIf_show = false; //基金经理
      } else if (tabLabel === "分级关系") {
        this.jcxx_show = false; //基础信息展示
        this.jyxx_show = false; //交易信息展示
        this.fyxx_show = false; //费用信息展示
        this.syfp_show = false; //收益分配展示
        this.zhxx_show = false; //账户信息展示
        this.tzfk_show = false; //投资风控展示
        this.lxr_show = false; //联系人展示
        this.fjgx_show = true; //分级关系展示
        this.bc_show = false; //保存按钮展示
        this.xsfs_show = false; //销售方式
        this.kfr_show = false; //开放日
        this.fundManagerIf_show = false; //基金经理
        this.PageDataAdd.fjgx_show = true;
      } else if (tabLabel === "销售方式") {
        this.jcxx_show = false; //基础信息展示
        this.jyxx_show = false; //交易信息展示
        this.fyxx_show = false; //费用信息展示
        this.syfp_show = false; //收益分配展示
        this.zhxx_show = false; //账户信息展示
        this.tzfk_show = false; //投资风控展示
        this.lxr_show = false; //联系人展示
        this.fjgx_show = false; //分级关系展示
        this.bc_show = false; //保存按钮展示
        this.xsfs_show = true; //销售方式
        this.kfr_show = false; //开放日
        this.xsfsIf_show = true; //销售方式展示
        this.fundManagerIf_show = false; //基金经理
        this.PageDataAdd.xsfs_show = true;
        //this.PageDataAdd.isAdd = false;
      } else if (tabLabel === "开放日") {
        this.jcxx_show = false; //基础信息展示
        this.jyxx_show = false; //交易信息展示
        this.fyxx_show = false; //费用信息展示
        this.syfp_show = false; //收益分配展示
        this.zhxx_show = false; //账户信息展示
        this.tzfk_show = false; //投资风控展示
        this.lxr_show = false; //联系人展示
        this.fjgx_show = false; //分级关系展示
        this.bc_show = false; //保存按钮展示
        this.xsfs_show = false; //销售方式
        this.kfr_show = true; //开放日
        this.kfrIf_show = true; //销售方式展示
        this.fundManagerIf_show = false; //基金经理
        this.PageDataAdd.kfr_show = true;
      } else if (tabLabel === "基金经理") {
        this.jcxx_show = false; //基础信息展示
        this.jyxx_show = false; //交易信息展示
        this.fyxx_show = false; //费用信息展示
        this.syfp_show = false; //收益分配展示
        this.zhxx_show = false; //账户信息展示
        this.tzfk_show = false; //投资风控展示
        this.lxr_show = false; //联系人展示
        this.fjgx_show = false; //分级关系展示
        this.bc_show = false; //保存按钮展示
        this.xsfs_show = false; //销售方式
        this.kfr_show = false; //开放日
        //this.fundManager_show = true;//基金经理
        this.fundManagerIf_show = true; //基金经理
        this.PageDataAdd.fundManager_show = true;
      } else if (tabLabel === "联系人") {
        this.jcxx_show = false; //基础信息展示
        this.jyxx_show = false; //交易信息展示
        this.fyxx_show = false; //费用信息展示
        this.syfp_show = false; //收益分配展示
        this.zhxx_show = false; //账户信息展示
        this.tzfk_show = false; //投资风控展示
        this.lxr_show = true; //联系人展示
        this.fjgx_show = false; //分级关系展示
        this.bc_show = true; //保存按钮展示
        this.xsfs_show = false; //销售方式
        this.kfr_show = false; //开放日
        //this.fundManager_show = true;//基金经理
        this.fundManagerIf_show = false; //基金经理
        this.PageDataAdd.lxr_show = true;
      }
    },
    handleChange(value) {
      //console.log(value);
    },
    activeCellMethod({ column, columnIndex }) {
      if (columnIndex === 4 || columnIndex === 3) {
        return false;
      }
      return true;
    },
    activeCellMethodGrade({ column, columnIndex }) {
      if (columnIndex === 3) {
        return false;
      }
      return true;
    },
    insertEvent(type, row) {
      const record = {};

      if (type === "grade") {
        let { row: newRow } = this.$refs.xTableGrade.insertAt(record, row);
        this.$refs.xTableGrade.setActiveCell(newRow);
        //  this.$refs.xTableGrade.insert().then(({ row }) => {
        //  this.$refs.xTableGrade.setActiveCell(1)
        // })
      } else if (type === "redeem") {
        this.$refs.xTableRedeem.insert().then(({ row }) => {
          this.$refs.xTableRedeem.setActiveCell(1);
        });
      } else if (type === "reward") {
        this.$refs.xTableReward.insert().then(({ row }) => {
          this.$refs.xTableReward.setActiveCell(1);
        });
      } else if (type === "contact") {
        let { row: newRow } = this.$refs.xTableContact.insertAt(record, row);
        this.$refs.xTableContact.setActiveCell(newRow);
      } else if (type === "saller") {
        if (!this.formInline.saleType) {
          this.$message({
            message: "请先选择销售方式",
            type: "erro",
          });
          return;
        }
        if (this.sallerNameArr.length == 0) {
          this.$message({
            message: "该销售方式下没有对应的渠道数据",
            type: "erro",
          });
          return;
        }
        let { row: newRow } = this.$refs.xTableMySaller.insertAt(record, row);
        this.$refs.xTableMySaller.setActiveCell(newRow);
      } else if (type === "open") {
        let { row: newRow } = this.$refs.xTableMyOpen.insertAt(record, row);
        this.$refs.xTableMyOpen.setActiveCell(newRow);
      } else if (type === "fundManager") {
        let { row: newRow } = this.$refs.xTableFundManager.insertAt(
          record,
          row
        );
        this.$refs.xTableFundManager.setActiveCell(newRow);
      }
    },

    removeEvent(type) {
      let selectRecords = "";
      if (type === "grade") {
        selectRecords = this.$refs.xTableGrade.getCheckboxRecords();
      } else if (type === "redeem") {
        selectRecords = this.$refs.xTableRedeem.getCheckboxRecords();
      } else if (type === "reward") {
        selectRecords = this.$refs.xTableReward.getCheckboxRecords();
      } else if (type === "contact") {
        selectRecords = this.$refs.xTableContact.getCheckboxRecords();
      } else if (type === "saller") {
        selectRecords = this.$refs.xTableMySaller.getCheckboxRecords();
      } else if (type === "open") {
        selectRecords = this.$refs.xTableMyOpen.getCheckboxRecords();
      } else if (type === "fundManager") {
        selectRecords = this.$refs.xTableFundManager.getCheckboxRecords();
      }

      if (selectRecords.length) {
        this.$confirm("您确定要删除选中的数据吗?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        })
          .then(() => {
            if (type === "grade") {
              this.$refs.xTableGrade.removeCheckboxRow();
            }
            if (type === "redeem") {
              this.$refs.xTableRedeem.removeCheckboxRow();
            }
            if (type === "reward") {
              this.$refs.xTableReward.removeCheckboxRow();
            }
            if (type === "contact") {
              this.$refs.xTableContact.removeCheckboxRow();
            }
            if (type === "saller") {
              this.$refs.xTableMySaller.removeCheckboxRow();
            }

            if (type === "open") {
              this.$refs.xTableMyOpen.removeCheckboxRow();
            }

            if (type === "fundManager") {
              this.$refs.xTableFundManager.removeCheckboxRow();
            }
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
    initData() {
      this.operateTypeArr = productDictionary.operateType;
      this.isGradeArr = productDictionary.isGrade;
      this.fundStateArr = productDictionary.fundState;
      this.isOpenShortArr = productDictionary.isOpenShort;
      this.saleFeePrepareArr = productDictionary.saleFeePrepare;
      this.saleFeePayArr = productDictionary.saleFeePay;
      this.shareTypeArr = productDictionary.shareType;
      this.callFloatTypeArr = productDictionary.callFloatType;
      this.isFixedPrepareArr = productDictionary.isFixedPrepare;
    },
    //是否分级选择事件
    isGradeChange(value) {
      if (value === 1) {
        this.isFj_show = true;
      } else {
        this.isFj_show = false;
      }
    },
    //浮动-固定选择事件
    callFloatTypeChange(value) {
      if (value === "0") {
        this.callFloat_input_show = true;
        this.callFloat_select_show = false;
        this.formInline.callRateType = "";
      } else {
        this.callFloat_input_show = false;
        this.formInline.callRate = "";
        this.callFloat_select_show = true;
      }
    },
    //业绩报酬选择事件
    rewardTypeChange(value) {
      if (value === "WHOLE" || value === "SINGLE") {
        this.rewardType_show = true;
      } else {
        this.rewardType_show = false;
        this.formInline.rewardPrepareType = "";
        this.formInline.isFixedPrepare = "";
        this.formInline.rewardPrepareDate = "";
      }
    },
    isFixedPrepareChange(value) {
      if (value === "1") {
        this.rewardPrepareDate_show = true;
      } else {
        this.rewardPrepareDate_show = false;
        this.formInline.rewardPrepareDate = "";
      }
    },
    saleTypeChange(value) {
      let params = {};
      params.sallerType = value;
      if (value === "S+A") {
        params.sallerType = "";
      }
      pageApi
        .getSallerData(params)
        .then((response) => {
          if (!response.data.error) {
            let arr = [{ sallerName: "" }];
            let arr1 = response.data.data;
            if (arr1.length > 0) {
              arr = arr.concat(arr1);
              this.sallerNameArr = arr;
            } else {
              this.sallerNameArr = [];
            }
          } else {
            this.$message.closeAll();
            this.$message({
              message: "查询失败",
              type: "error",
            });
            this.sallerNameArr = [];
          }
        })
        .catch(() => {
          this.$message.closeAll();
          this.$message({
            message: "查询失败",
            type: "error",
          });
          this.sallerNameArr = [];
        });
    },
    sallerNameChangeEvent({ row }) {
      let name = row.sallerName || row.managerName;
      if (name) {
        let arr = this.sallerNameArr;
        for (let i = 0; i < arr.length; i++) {
          if (name === arr[i].sallerName) {
            row.sallerCode = arr[i].sallerCode;
            row.sallerType = arr[i].sallerType;
            // let arr1 = this.saleTypeArr;
            //  for(let j=0;j<arr1.length;j++){
            //     if(arr1[j].dimCde === arr[i].sallerType){
            //       return  = arr1[j].dimNme;
            //     }
            //   }
            break;
          }
        }
        this.$refs.xTableMySaller.updateData();
      } else {
        row.sallerCode = null;
        row.sallerType = null;
      }
    },
    fundNameGradeChangeEvent(val) {
      let row = val.row;
      let name = row.fundNameGrade;
      if (name) {
        let arr = this.fundNameGradeArr;
        for (let i = 0; i < arr.length; i++) {
          if (name === arr[i].fundName) {
            row.fundCodeGrade = arr[i].fundCode;
            return;
          }
        }
      } else {
        row.fundCodeGrade = "";
      }
    },
    managerNameChangeEvent({ row }) {
      let name = row.managerName;
      if (name) {
        let arr = this.managerNameArr;
        for (let i = 0; i < arr.length; i++) {
          if (name === arr[i].name) {
            row.managerCode = arr[i].id;
            row.investStrategy = arr[i].investStrategy;
            row.phone = arr[i].phone;
            row.email = arr[i].email;
            break;
          }
        }
        this.$refs.xTableFundManager.updateData();
      } else {
        row.managerCode = null;
        row.investStrategy = null;
        row.phone = null;
        row.email = null;
      }
    },
    save(formName) {
      if (!this.volidFormData()) {
        return;
      }
      this.isSave = true;
      this.fullValidEvent();
    },
    saveBefore() {
      // if(!this.validContactFlag){
      //     this.$message({
      //       message: '请填写正确的联系人信息',
      //       type: 'erro'
      //     });
      //      this.isSave = false;
      //     return;
      // }
      // if(!this.validRewardtFlag){
      //   this.$message({
      //       message: '请填写完整的计提信息',
      //       type: 'erro'
      //     });
      //     this.isSave = false;
      //     return;
      // }
      // if(!this.validRedeemFlag && this.callFloat_select_show){
      //   this.$message({
      //       message: '请填写完整的费率信息',
      //       type: 'erro'
      //     });
      //     this.isSave = false;
      //     return;
      // }
      // if(!this.validGradeFlag || (this.isFj_show && this.tableDataGrade.length===0)){
      //   this.$message({
      //       message: '请填写完整的分级信息',
      //       type: 'erro'
      //     });
      //     this.isSave = false;
      //     return;

      // }

      // if(!this.validSallerFlag || (this.tableDataSaller.length===0)){
      //   this.$message({
      //       message: '请填写完整的销售方式信息',
      //       type: 'erro'
      //     });
      //     this.isSave = false;
      //     return;

      // }

      //   if(!this.validOpenFlag || (this.tableDataOpen.length===0)){
      //   this.$message({
      //       message: '请填写完整的开放日信息',
      //       type: 'erro'
      //     });
      //     this.isSave = false;
      //     return;

      // }

      // if(!this.validFundManagerFlag || (this.tableDataFundManager.length===0)){
      //   this.$message({
      //       message: '请填写完整的基金经理信息',
      //       type: 'erro'
      //     });
      //     this.isSave = false;
      //     return;

      // }

      if (this.tableDataSaller.length > 0) {
        if (this.validTableDate(this.tableDataSaller)) {
          this.$message.closeAll();
          this.$message({
            message: "销售方式列表，开始日期/结束日期填写错误",
            type: "error",
          });
          this.isSave = false;
          return;
        }
      }

      if (this.tableDataOpen.length > 0) {
        if (this.validTableDate(this.tableDataOpen)) {
          this.$message.closeAll();
          this.$message({
            message: "开放日列表，规则生效日期/规则失效日期填写错误",
            type: "error",
          });
          this.isSave = false;
          return;
        }
      }

      let self = this;
      self.$refs["formInline"].validate((valid) => {
        if (valid) {
          let type = this.PageDataAdd.addType;
          if (type == 0) {
            this.updateData();
          } else {
            this.volidFundCode();
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
          let params = {};
          params = commonFun.parameterSrc(this.formInline);

          let insertRecordsContacts = [];
          if (this.$refs.xTableContact) {
            insertRecordsContacts = this.$refs.xTableContact.getTableData()
              .tableData;
          }

          // let  insertRecordsRedeem  = this.$refs.xTableRedeem.getRecordset().insertRecords;
          // //const { insertRecordsGrade } = this.$refs.xTableReward.getRecordset()
          // let insertRecordsContacts  = this.$refs.xTableContact.getRecordset().insertRecords;
          //this.countSubmit_btn = true;
          let params2 = {};
          params2.fundInfo = params;
          if (this.callFloat_select_show) {
            params2.fundRedeems = this.tableDataRedeem;
          } else {
            params2.fundRedeems = [];
          }

          if (this.tableDataGrade.length > 0 && this.formInline.isGrade === 1) {
            params2.fundGrades = this.tableDataGrade;
          }
          if (insertRecordsContacts.length > 0) {
            params2.fundContacts = insertRecordsContacts;
          } else {
            params2.fundContacts = this.tableDataContact;
          }
          if (this.rewardType_show) {
            params2.fundRewards = this.tableDataReward;
          } else {
            params2.fundRewards = [];
          }

          params2.fundSallers = this.tableDataSaller;
          params2.fundOpens = this.tableDataOpen;

          params2.fundManagers = this.tableDataFundManager;

          let arr = this.checkfundInvestArea;
          if (arr.length > 0) {
            let fundInvestsArr = [];
            for (let i = 0; i < arr.length; i++) {
              let investArr = {};
              investArr.investScope = arr[i];
              fundInvestsArr.push(investArr);
            }
            params2.fundInvests = fundInvestsArr;
          }

          pageApi
            .addDataSource(params2)
            .then((response) => {
              if (!response.data.error) {
                // 关闭移动指标弹框

                this.$message.closeAll();
                this.$message({
                  message: "提交审核成功",
                  type: "success",
                });
                // 刷新列表
                // 刷新列表
                this.$emit("pageCheckClick", {
                  data: [],
                  flag: true,
                });
              } else {
                // 关闭移动指标弹框
                // this.countDialog = false;
                this.$message.closeAll();
                this.$message({
                  message: response.data.error || "提交审核失败",
                  type: "error",
                });
                this.isSave = false;
              }
              //this.countSubmit_btn = false;
            })
            .catch(() => {
              // 关闭移动指标弹框

              //this.countSubmit_btn = false;
              this.$message.closeAll();
              this.$message({
                message: "提交审核失败",
                type: "error",
              });
              this.isSave = false;
            });
        })
        .catch(() => {
          // 关闭移动指标弹框

          //this.countSubmit_btn = false;
          this.isSave = false;
        });
    },
    updateData() {
      this.$confirm("确定修改?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          let params = {};
          params = commonFun.parameterSrc(this.formInline);
          //this.countSubmit_btn = true;
          let params2 = {};

          let insertRecordsContacts = [];
          if (this.$refs.xTableContact) {
            insertRecordsContacts = this.$refs.xTableContact.getTableData()
              .tableData;
          }
          params2.fundInfo = params;

          if (insertRecordsContacts.length > 0) {
            params2.fundContacts = insertRecordsContacts;
          } else {
            params2.fundContacts = this.tableDataContact;
          }
          if (this.callFloat_select_show) {
            params2.fundRedeems = this.tableDataRedeem;
          } else {
            params2.fundRedeems = [];
          }
          if (this.rewardType_show) {
            params2.fundRewards = this.tableDataReward;
          } else {
            params2.fundRewards = [];
          }
          if (this.tableDataGrade.length > 0 && this.formInline.isGrade === 1) {
            params2.fundGrades = this.tableDataGrade;
          }
          params2.fundSallers = this.tableDataSaller;
          params2.fundOpens = this.tableDataOpen;
          params2.fundManagers = this.tableDataFundManager;

          let arr = this.checkfundInvestArea;
          if (arr.length > 0) {
            let fundInvestsArr = [];
            for (let i = 0; i < arr.length; i++) {
              let investArr = {};
              investArr.investScope = arr[i];
              fundInvestsArr.push(investArr);
            }
            params2.fundInvests = fundInvestsArr;
          }
          pageApi
            .updateDataSource(params2)
            .then((response) => {
              if (!response.data.error) {
                // 关闭移动指标弹框

                this.$message.closeAll();
                this.$message({
                  message: "提交审核成功",
                  type: "success",
                });
                // 刷新列表
                // 刷新列表
                this.$emit("pageCheckClick", {
                  data: [],
                  flag: true,
                });
              } else {
                // 关闭移动指标弹框
                // this.countDialog = false;
                this.$message.closeAll();
                this.$message({
                  message: response.data.error || "提交审核失败",
                  type: "error",
                });
                this.isSave = false;
              }
              //this.countSubmit_btn = false;
            })
            .catch(() => {
              // 关闭移动指标弹框

              //this.countSubmit_btn = false;
              this.$message.closeAll();
              this.$message({
                message: "提交审核失败",
                type: "error",
              });
              this.isSave = false;
            });
        })
        .catch(() => {
          // 关闭移动指标弹框

          //this.countSubmit_btn = false;
          this.isSave = false;
        });
    },
    initTable() {
      let insertRecordsGrade = [];
      if (this.$refs.xTableGrade) {
        insertRecordsGrade = this.$refs.xTableGrade.getTableData().tableData;
      }
      let insertRecordsRedeem = [];
      if (this.$refs.xTableRedeem) {
        insertRecordsRedeem = this.$refs.xTableRedeem.getTableData().tableData;
      }
      //const { insertRecordsGrade } = this.$refs.xTableReward.getRecordset()
      let insertRecordsContacts = [];
      if (this.$refs.xTableContact) {
        insertRecordsContacts = this.$refs.xTableContact.getTableData()
          .tableData;
      }

      let insertRecordsRewards = [];
      if (this.$refs.xTableReward) {
        insertRecordsRewards = this.$refs.xTableReward.getTableData().tableData;
      }

      let insertRecordsSallers = [];
      if (this.$refs.xTableMySaller) {
        insertRecordsSallers = this.$refs.xTableMySaller.getTableData()
          .tableData;
      }

      let insertRecordsOpen = [];
      if (this.$refs.xTableMyOpen) {
        let data = this.$refs.xTableMyOpen.getTableData();
        insertRecordsOpen = this.$refs.xTableMyOpen.getTableData().tableData;
        //  let self = this;
        //   setTimeout(function(){
        //     insertRecordsOpens  = self.$refs.xTableMyOpen.getTableData().tableData;
        //   },300)
      }

      let insertRecordsFundManager = [];
      if (this.$refs.xTableFundManager) {
        let data = this.$refs.xTableFundManager.getTableData();
        insertRecordsFundManager = this.$refs.xTableFundManager.getTableData()
          .tableData;
      }

      if (insertRecordsContacts.length > 0) {
        this.tableDataContact = insertRecordsContacts; //联系人列表数据
      }
      if (insertRecordsRedeem.length > 0) {
        this.tableDataRedeem = insertRecordsRedeem; //赎回费率列表数据
      }
      if (insertRecordsGrade.length > 0) {
        this.tableDataGrade = insertRecordsGrade; //分级列表数据
      }

      if (insertRecordsRewards.length > 0) {
        this.tableDataReward = insertRecordsRewards; //计提列表数据
      }

      if (insertRecordsSallers.length > 0) {
        this.tableDataSaller = insertRecordsSallers; //计提列表数据
      }

      if (insertRecordsOpen.length > 0) {
        this.tableDataOpen = insertRecordsOpen; //计提列表数据
      }

      if (insertRecordsFundManager.length > 0) {
        this.tableDataFundManager = insertRecordsFundManager; //计提列表数据
      }
    },
    editActivedEvent({ row, column }, event) {
      console.log(`打开 ${column.title} 列编辑`);
    },
    editClosedEvent({ row, column }, event) {
      console.log(`关闭 ${column.title} 列编辑`);
    },
    getDetail() {
      this.initFormData(this.PageDataAdd.formData);
    },
    initFormData(data) {
      if (!data) {
        return;
      }

      if (data.fundRedeems) {
        this.tableDataRedeem = data.fundRedeems; //赎回费率列表数据
      }
      if (data.fundContacts) {
        this.tableDataContact = data.fundContacts; //赎回费率列表数据
      }
      if (data.fundGrades) {
        this.tableDataGrade = data.fundGrades; //赎回费率列表数据
      }

      if (data.fundRewards) {
        this.tableDataReward = data.fundRewards; //计提列表数据
      }

      if (data.fundSallers) {
        this.tableDataSaller = data.fundSallers; //计提列表数据
      }

      if (data.fundManagers) {
        this.tableDataFundManager = data.fundManagers; //计提列表数据
      }

      if (data.fundOpens) {
        let tableDataOpen = [];
        let arr = data.fundOpens; //计提列表数据
        for (let i = 0; i < arr.length; i++) {
          let params = {};
          if (arr[i].openFrequence) {
            params.openFrequence = arr[i].openFrequence;
          }
          if (arr[i].openRule) {
            params.openRule = arr[i].openRule;
          }
          if (arr[i].beginDate) {
            params.beginDate = arr[i].beginDate;
          }
          if (arr[i].endDate) {
            params.endDate = arr[i].endDate;
          }
          tableDataOpen.push(params);
        }
        this.tableDataOpen = tableDataOpen;
      }
      if (data.fundInvests) {
        let arr = [];

        let arrs = data.fundInvests;
        for (let i = 0; i < arrs.length; i++) {
          arr.push(arrs[i].investScope);
        }
        this.checkfundInvestArea = arr;
        if (arr.length === this.fundInvestArea.length) {
          this.checkAll = true;
          this.handleCheckAllChange(true);
        }
      } else {
        this.checkfundInvestArea = [];
      }
      this.initFormInline(data.fundInfo);
    },
    initFormInline(data) {
      let type = this.PageDataAdd.addType;
      if (type == 0) {
        this.formInline.id = "";
      }
      let formData = commonFun.allPrpos(this.formInline, data);

      this.formInline = formData;

      if (type == 1) {
        this.formInline.fundCode = "";
        this.formInline.fundName = "";
        this.formInline.fundNameEn = "";
      }
      if (this.formInline.isGrade && this.formInline.isGrade === 1) {
        this.isFj_show = true;
      }

      if (
        this.formInline.callFloatType &&
        this.formInline.callFloatType === "1"
      ) {
        this.callFloat_select_show = true;
      } else if (
        this.formInline.callFloatType &&
        this.formInline.callFloatType === "0"
      ) {
        this.callFloat_input_show = true;
      }

      if (
        this.formInline.rewardType &&
        (this.formInline.rewardType === "WHOLE" ||
          this.formInline.rewardType === "SINGLE")
      ) {
        this.rewardType_show = true;
      }

      if (
        this.formInline.isFixedPrepare &&
        this.rewardType_show &&
        this.formInline.isFixedPrepare === "1"
      ) {
        this.rewardPrepareDate_show = true;
      }

      if (this.formInline.saleType) {
        this.saleTypeChange(this.formInline.saleType);
      }

      this.formInline.callRateType = formData.callRateType;
      this.formInline.callRate = formData.callRate;
    },
    async fullValidEvent() {
      let errMap = "";

      if (this.$refs.xTableGrade) {
        const errMap2 = await this.$refs.xTableGrade
          .fullValidate()
          .catch((errMap) => errMap);
        errMap = errMap2;
        if (errMap) {
          this.validGradeFlag = false;
        } else {
          this.validGradeFlag = true;
        }
      }

      if (this.$refs.xTableRedeem) {
        const errMap2 = await this.$refs.xTableRedeem
          .fullValidate()
          .catch((errMap) => errMap);
        errMap = errMap2;
        if (errMap) {
          this.validRedeemFlag = false;
        } else {
          this.validRedeemFlag = true;
        }
      }
      //const { insertRecordsGrade } = this.$refs.xTableReward.getRecordset()
      if (this.$refs.xTableContact) {
        const errMap2 = await this.$refs.xTableContact
          .fullValidate()
          .catch((errMap) => errMap);
        errMap = errMap2;
        if (errMap) {
          this.validContactFlag = false;
        } else {
          this.validContactFlag = true;
        }
      }

      if (this.$refs.xTableReward) {
        const errMap2 = await this.$refs.xTableReward
          .fullValidate()
          .catch((errMap) => errMap);
        errMap = errMap2;
        if (errMap) {
          this.validRewardtFlag = false;
        } else {
          this.validRewardtFlag = true;
        }
      }

      if (this.$refs.xTableMySaller) {
        const errMap2 = await this.$refs.xTableMySaller
          .fullValidate()
          .catch((errMap) => errMap);
        errMap = errMap2;
        if (errMap) {
          this.validSallerFlag = false;
        } else {
          this.validSallerFlag = true;
        }
      }

      if (this.$refs.xTableMyOpen) {
        const errMap2 = await this.$refs.xTableMyOpen
          .fullValidate()
          .catch((errMap) => errMap);
        errMap = errMap2;
        if (errMap) {
          this.validOpenFlag = false;
        } else {
          this.validOpenFlag = true;
        }
      }

      if (this.$refs.xTableFundManager) {
        const errMap2 = await this.$refs.xTableFundManager
          .fullValidate()
          .catch((errMap) => errMap);
        errMap = errMap2;
        if (errMap) {
          this.validFundManagerFlag = false;
        } else {
          this.validFundManagerFlag = true;
        }
      }
      if (this.isSave) {
        this.saveBefore();
      }
    },
    getEdimsGet(val) {
      let params = val;
      pageApi.getTransferType(params).then((res) => {
        let self = this;
        if (res.data.message === "success") {
          if (val === "fundTrustorCodeType") {
            this.trustorCodeArr = res.data.data; //托管人名称
          }
          if (val === "fundManagerCodeType") {
            this.managerCodeArr = res.data.data; //管理人名称
          }

          if (val === "fundoperatorCodeType") {
            this.operatorCodeArr = res.data.data; //基金服务机构
          }
          if (val === "fundTypes") {
            this.fundTypeArr = res.data.data; //基金类型
          }
          if (val === "fundInvestDirectType") {
            this.investDirectArr = res.data.data; //投资方向
          }
          if (val === "fundRiskLevelType") {
            this.riskLevelArr = res.data.data; //风险等级
          }
          if (val === "fundSaleType") {
            this.saleTypeArr = res.data.data; //销售方式
          }
          if (val === "fundSubscribeConfirmDayType") {
            this.subscribeConfirmDayArr = res.data.data; //认购交易确认天数
          }
          if (val === "fundSubscribeDeliverDayType") {
            this.subscribeDeliverDayArr = res.data.data; //认购资金交收天数
          }
          if (val === "fundApplyConfirmDayType") {
            this.applyConfirmDayArr = res.data.data; //申购交易确认天数
          }
          if (val === "fundApplyDeliverDayType") {
            this.applyDeliverDayArr = res.data.data; //申购资金交收天数
          }
          if (val === "fundCallConfirmDayType") {
            this.callConfirmDayArr = res.data.data; //赎回交易确认天数
          }
          if (val === "fundCallDeliverDayType") {
            this.callDeliverDayArr = res.data.data; //赎回资金交收天数
          }
          if (val === "fundCallFloatType") {
            this.callRateTypeArr = res.data.data; //赎回费率浮动类型
          }
          if (val === "fundManageFeePrepareType") {
            this.manageFeePrepareArr = res.data.data; //管理费-计提
          }
          if (val === "fundManageFeeStand") {
            this.manageFeeAssetArr = res.data.data; //管理费-计算方式
          }
          if (val === "fundManageFeePayType") {
            this.manageFeePayArr = res.data.data; //管理费-支付方式
          }
          if (val === "fundRewardType") {
            this.rewardTypeArr = res.data.data; //业绩报酬
          }
          if (val === "fundRewardPrepareType") {
            this.rewardPrepareTypeArr = res.data.data; //计提方式
          }
          if (val === "fundPortionNumberType") {
            this.portionNumberArr = res.data.data; //分配次数
          }
          if (val === "fundBonusProcessType") {
            this.bonusProcessArr = res.data.data; //提交分红流程
          }
          if (val === "fundDataExpectType") {
            this.dataExpectArr = res.data.data; //预估数据以及计算报表
          }
          if (val === "fundBonusConfimType") {
            this.bonusConfimArr = res.data.data; //分红数据确认
          }
          if (val === "fundBonusDeliverType") {
            this.bonusDeliverArr = res.data.data; //分红资金交收
          }
          if (val === "fundNameGradeType") {
            this.fundNameGradeArr = res.data.data; //分级代码
          }

          if (val === "fund_investArea") {
            this.fundInvestArea = res.data.data; //投资范围
          }

          if (val === "fundOpenFrequence") {
            let arr = [{ dimCde: "", dimNme: "" }];
            let arr1 = res.data.data;
            if (arr1.length > 0) {
              arr = arr.concat(arr1);
              this.openFrequenceArr = arr;
            } else {
              this.openFrequenceArr = [];
            }
          }

          if (val === "fundOpenRule") {
            let arr = [{ dimCde: "", dimNme: "" }];
            let arr1 = res.data.data;
            if (arr1.length > 0) {
              arr = arr.concat(arr1);
              this.openRuleArr = arr;
            } else {
              this.openRuleArr = [];
            }
          }

          if (val === "fundrewardPrepareDate") {
            this.rewardPrepareDateArr = res.data.data; //投资范围
          }
        } else {
          this.$message.error("初始化数据失败");
        }
      });
    },
    getEdims() {
      //托管人名称
      // this.getEdimsGet('fundTrustorCodeType');

      //管理人名称
      //this.getEdimsGet('fundManagerCodeType');

      //基金服务机构
      // this.getEdimsGet('fundoperatorCodeType');
      //获取托管人，管理人，基金服务机构
      this.getDeptInfoSel();

      //获取基金经理数组
      this.getFundManagerArr();
      //基金类型
      this.getEdimsGet("fundTypes");

      //投资方向
      this.getEdimsGet("fundInvestDirectType");

      //风险等级
      this.getEdimsGet("fundRiskLevelType");

      //销售方式
      this.getEdimsGet("fundSaleType");

      //认购交易确认天数
      this.getEdimsGet("fundSubscribeConfirmDayType");

      //认购资金交收天数
      this.getEdimsGet("fundSubscribeDeliverDayType");

      //申购交易确认天数
      this.getEdimsGet("fundApplyConfirmDayType");

      //申购资金交收天数
      this.getEdimsGet("fundApplyDeliverDayType");

      //赎回交易确认天数
      this.getEdimsGet("fundCallConfirmDayType");

      //赎回资金交收天数
      this.getEdimsGet("fundCallDeliverDayType");

      //赎回费率浮动类型
      this.getEdimsGet("fundCallFloatType");

      //管理费-计提
      this.getEdimsGet("fundManageFeePrepareType");

      //管理费-计算方式
      this.getEdimsGet("fundManageFeeStand");

      //管理费-支付方式
      this.getEdimsGet("fundManageFeePayType");

      //业绩报酬
      this.getEdimsGet("fundRewardType");

      //计提方式
      this.getEdimsGet("fundRewardPrepareType");

      //分配次数
      this.getEdimsGet("fundPortionNumberType");

      //提交分红流程
      this.getEdimsGet("fundBonusProcessType");

      //预估数据以及计算报表
      this.getEdimsGet("fundDataExpectType");

      //分红数据确认
      this.getEdimsGet("fundBonusConfimType");

      //分红资金交收
      this.getEdimsGet("fundBonusDeliverType");

      //分级代码
      this.getEdimsGet("fundNameGradeType");

      //投资范围
      this.getEdimsGet("fund_investArea");

      //开放频率数组
      this.getEdimsGet("fundOpenFrequence");

      //开放规则数组
      this.getEdimsGet("fundOpenRule");

      //计提日期
      this.getEdimsGet("fundrewardPrepareDate");

      //分级代码
      this.getProductInfo();
    },
    //开放日受理规则设置
    insertDayRule() {},
    //回访截止日设置
    returnDate() {},
    //开放期规则设置
    insertOpenRule() {},
    //新增合同开放日
    insertOpenRule() {},
    //新增临时开放日
    insertOpenDay() {},
    //生成开放日
    getOpenDay() {},
    getProductInfo() {
      pageApi
        .getProductInfo()
        .then((res) => {
          if (res.data.message === "success") {
            let arr = [{ fundCode: "", fundName: "" }];
            let arr1 = res.data.data;
            if (arr1.length > 0) {
              arr = arr.concat(arr1);
              this.fundNameGradeArr = arr;
            } else {
              this.fundNameGradeArr = [];
            }
          } else {
            this.fundNameGradeArr = [];
            this.$message.error("查询产品信息失败");
          }
        })
        .catch(() => {
          this.$message.error("查询产品信息失败");
          this.fundNameGradeArr = [];
        });
    },
    validTableDate(arr) {
      for (let i = 0; i < arr.length; i++) {
        if (!arr[i].beginDate) {
          return true;
        } else if (!arr[i].beginDate) {
          return true;
        } else if (arr[i].beginDate > arr[i].endDate) {
          return true;
        }
      }
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
    volidFundCode() {
      let fundCode = this.formInline.fundCode;
      let params = {};

      params.fundCode = fundCode;
      pageApi
        .volidFundCode(params)
        .then((response) => {
          if (response.data.message === "success") {
            this.saveData();
          } else {
            this.$message.closeAll();
            this.$message({
              message: response.data.message || "校验失败",
              type: "error",
            });
            this.isSave = false;
            return true;
          }
        })
        .catch(() => {
          this.$message.closeAll();
          this.$message({
            message: "校验失败",
            type: "error",
          });
          this.isSave = false;
          return true;
        });
    },
    getDeptInfoSel() {
      pageApi
        .getDeptInfoSel()
        .then((response) => {
          if (!response.data.error) {
            let arr = response.data.data;
            // let managerCodeArr = [];
            // let trustorCodeArr = [];
            // let operatorCodeArr = [];

            // for(let i=0;i<arr.length;i++){
            //     if(arr[i].instTypeName === '托管机构'){
            //         operatorCodeArr.push(arr[i])
            //     }
            //     if(arr[i].instTypeName === '管理人'){
            //         managerCodeArr.push(arr[i])
            //     }
            //     if(arr[i].instTypeName === '托管机构'){
            //         operatorCodeArr.push(arr[i])
            //     }
            // }
            this.managerCodeArr = arr; //管理人-数组
            this.trustorCodeArr = arr; //管理人-数组
            this.operatorCodeArr = arr; //管理人-数组
          } else {
            this.managerCodeArr = []; //管理人-数组
            this.trustorCodeArr = []; //托管人-数组
            this.operatorCodeArr = []; //基金服务机构-数组
          }
        })
        .catch(() => {});
    },
    // 获取基金经理数组
    getFundManagerArr() {
      pageApi
        .getFundManagerInfo()
        .then((response) => {
          if (!response.data.error) {
            let arr = [{ name: "" }];
            let arr1 = response.data.data;
            if (arr1.length > 0) {
              arr = arr.concat(arr1);
              this.managerNameArr = arr;
            } else {
              this.managerNameArr = [];
            }
          } else {
            this.managerNameArr = [];
          }
        })
        .catch(() => {});
    },
    volidFormData() {
      this.initTable();
      if (!commonFun.objectIsNotEmpty(this.formInline.fundName)) {
        this.$message({
          message: "请填写基础信息-产品名称",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.fundCode)) {
        this.$message({
          message: "请填写基础信息-产品代码",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.fundType)) {
        this.$message({
          message: "请选择基础信息-基金类型",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.holdYear)) {
        this.$message({
          message: "请填写基础信息-产品存续期限",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.riskLevel)) {
        this.$message({
          message: "请选择基础信息-风险等级",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.isGrade)) {
        this.$message({
          message: "请选择基础信息-是否分级",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.investDirect)) {
        this.$message({
          message: "请选择基础信息-投资方向",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.fundState)) {
        this.$message({
          message: "请选择基础信息-产品状态",
          type: "error",
        });
        return false;
      }

      if (!commonFun.objectIsNotEmpty(this.formInline.purchasePoint)) {
        this.$message({
          message: "请选择交易信息-认申购起点（不含费）",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.subscribeConfirmDay)) {
        this.$message({
          message: "请选择交易信息-认购交易确认天数",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.subscribeRate)) {
        this.$message({
          message: "请选择交易信息-认购费率",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.applyDeliverDay)) {
        this.$message({
          message: "请选择交易信息-申购资金交收天数",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.callConfirmDay)) {
        this.$message({
          message: "请选择交易信息-赎回交易确认天数",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.callFloatType)) {
        this.$message({
          message: "请选择交易信息-赎回费率浮动类型",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.purchaseDiffAppend)) {
        this.$message({
          message: "请选择交易信息-追加认申购级差",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.subscribeDeliverDay)) {
        this.$message({
          message: "请选择交易信息-认购资金交收天数",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.applyConfirmDay)) {
        this.$message({
          message: "请选择交易信息-申购交易确认天数",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.callDeliverDay)) {
        this.$message({
          message: "请选择交易信息-赎回资金交收天数",
          type: "error",
        });
        return false;
      }
      return true;
    },
  },
};
</script>

<style rel="stylesheet/scss" lang="scss" >
.product_detail {
  padding: 10px 15px 15px 15px;
  background: #fff;
  box-shadow: 0 2px 3px rgba(95, 95, 95, 0.1);
  border: 1px solid #e4e4e8;
  border-radius: 5px;
  -moz-border-radius: 5px;
  -webkit-border-radius: 5px;
  margin: auto;
}
.el_form_item {
  width: 188px ;
}
.vxe-dropdown--panel {
  z-index: 9999 !important;
}
.vxe-table--tooltip-wrapper.vxe-table--valid-error {
  display: none;
}
</style>

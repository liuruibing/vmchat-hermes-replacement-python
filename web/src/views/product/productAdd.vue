<template>
  <div class="productNewStyle">
    <el-form
      :inline="true"
      :rules="commonRules"
      label-width="180px"
      label-position="right"
      ref="formInline"
      :model="formInline"
      class="demo-form-inline form_inline_search"
      style="margin-top: 8px;margin-bottom: 10px;"
    >
      <el-tabs v-model="activeName" @tab-click="handleClick">
        <el-tab-pane label="基础信息" name="first">
          <span slot="label" v-if="PageDataAdd.addType==0&&jcxx_i_show&&PageDataAdd.beforeData">基础信息<i style="color: red" class="el-icon-warning"></i></span>
          <div class="product_detail">
            <el-row>
              <el-col :span="23" :offset="1">
                <el-row>
                  <el-col :span="11">
                    <el-form-item label="产品代码" prop="fundCode">
                      <el-input
                        v-model.trim="formInline.fundCode"
                        placeholder="产品代码"
                        type="text"
                        maxlength="8"
                        minlength="6"
                        v-on:input="fundCodeInput"
                        :disabled="PageDataAdd.addType==0"
                        class="el_form_item"
                        auto-complete="off"
                      />
                    </el-form-item>
                    <br />
                    <el-form-item label="英文名称" prop="fundNameEn">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.fundNameEn==PageDataAdd.beforeData.fundInfo.fundNameEn?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.fundNameEn || '-':''}} </div>
                      <el-input
                        v-model="formInline.fundNameEn"
                        placeholder="英文名称"
                        type="text"
                        maxlength="100"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.fundNameEn==PageDataAdd.beforeData.fundInfo.fundNameEn?'':'red':'']"
                        auto-complete="off"
                      />
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="托管人名称" prop="trustorCode">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.trustorCode==PageDataAdd.beforeData.fundInfo.trustorCode?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?trustorCode || '-':''}} </div>
                      <el-select
                        clearable
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.trustorCode==PageDataAdd.beforeData.fundInfo.trustorCode?'':'red':'']"
                        v-model="formInline.trustorCode"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in trustorCodeArr"
                          :value="group.id"
                          :key="index"
                          :label="group.instName"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <!-- 基金类型-旧 -->
                    <!-- <el-form-item label="基金类型" prop="fundType">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.fundType==PageDataAdd.beforeData.fundInfo.fundType?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?fundType || '-':''}} </div>
                      <el-select
                        clearable
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.fundType==PageDataAdd.beforeData.fundInfo.fundType?'':'red':'']"
                        v-model="formInline.fundType"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in fundTypeArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item> -->

                    <!-- 基金类型-分组（新） -->
                    <el-form-item label="基金类型" prop="fundTypeDetails">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.fundTypeDetails==PageDataAdd.beforeData.fundInfo.fundTypeDetails?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?fundTypeDetails || '-':''}} </div>
                      
                      <el-select 
                        clearable
                        v-model="formInline.fundTypeDetails" 
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.fundTypeDetails==PageDataAdd.beforeData.fundInfo.fundTypeDetails?'':'red':'']"
                        placeholder="请选择"
                        @change="fundTypeChange"
                      >
                        <el-option-group
                          v-for="group in options"
                          :key="group.label"
                          :label="group.label">
                          <el-option
                            @click.native="fundTypeClick(item)"
                            v-for="item in group.options"
                            :key="item.dimCde"
                            :label="item.dimNme"
                            :value="item.dimCde">
                          </el-option>
                        </el-option-group>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="证券营业部" prop="operateDept">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0?PageDataAdd.beforeData?formInline.operateDept==PageDataAdd.beforeData.fundInfo.operateDept?true:false:true:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.operateDept || '-':''}} </div>
                      <el-input
                        v-model="formInline.operateDept"
                        placeholder="证券营业部"
                        type="text"
                        maxlength="100"
                        :class="['el_form_item', PageDataAdd.addType==0?PageDataAdd.beforeData?formInline.operateDept==PageDataAdd.beforeData.fundInfo.operateDept?'':'red':'':'']"
                        auto-complete="off"
                      />
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="产品存续期限(年)" prop="holdYear">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.holdYear==PageDataAdd.beforeData.fundInfo.holdYear?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.holdYear || '-':''}} </div>
                      <el-input
                        v-model="formInline.holdYear"
                        placeholder="产品存续期限"
                        type="text"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.holdYear==PageDataAdd.beforeData.fundInfo.holdYear?'':'red':'']"
                        auto-complete="off"
                        maxlength="8"
                        v-on:input="holdYearChange"
                      />
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="风险等级" prop="riskLevel">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.riskLevel==PageDataAdd.beforeData.fundInfo.riskLevel?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?riskLevel || '-':''}} </div>
                      <el-select
                        clearable
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.riskLevel==PageDataAdd.beforeData.fundInfo.riskLevel?'':'red':'']"
                        v-model="formInline.riskLevel"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in riskLevelArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="产品备案代码" prop="recordCode">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.recordCode==PageDataAdd.beforeData.fundInfo.recordCode?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.recordCode || '-':''}} </div>
                      <el-input
                        v-model.trim="formInline.recordCode"
                        placeholder="产品备案代码"
                        type="text"
                        maxlength="50"
                        v-on:input="recordCodeInput"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.recordCode==PageDataAdd.beforeData.fundInfo.recordCode?'':'red':'']"
                        auto-complete="off"
                      />
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="是否分类" prop="isGrade">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.isGrade==PageDataAdd.beforeData.fundInfo.isGrade?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?isGrade || '-':''}} </div>
                      <el-select
                        clearable
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.isGrade==PageDataAdd.beforeData.fundInfo.isGrade?'':'red':'']"
                        @change="isGradeChange"
                        v-model="formInline.isGrade"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in isGradeArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                  </el-col>

                  <el-col :span="11" :offset="1">
                    <el-form-item label="产品名称" prop="fundName">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.fundName==PageDataAdd.beforeData.fundInfo.fundName?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.fundName || '-':''}} </div>
                      <el-input
                        v-model="formInline.fundName"
                        placeholder="产品名称"
                        type="text"
                        maxlength="100"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.fundName==PageDataAdd.beforeData.fundInfo.fundName?'':'red':'']"
                        auto-complete="off"
                      />
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="管理人名称" prop="managerCode">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.managerCode==PageDataAdd.beforeData.fundInfo.managerCode?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?managerCode || '-':''}} </div>
                      <el-select
                        clearable
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.managerCode==PageDataAdd.beforeData.fundInfo.managerCode?'':'red':'']"
                        v-model="formInline.managerCode"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in managerCodeArr"
                          :value="group.id"
                          :key="index"
                          :label="group.instName"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                    <br />

                    <el-form-item label="基金服务机构" prop="operatorCode">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.operatorCode==PageDataAdd.beforeData.fundInfo.operatorCode?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?operatorCode || '-':''}} </div>
                      <el-select
                        clearable
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.operatorCode==PageDataAdd.beforeData.fundInfo.operatorCode?'':'red':'']"
                        v-model="formInline.operatorCode"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in operatorCodeArr"
                          :value="group.id"
                          :key="index"
                          :label="group.instName"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="投资方向" prop="investDirect">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.investDirect==PageDataAdd.beforeData.fundInfo.investDirect?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?investDirect || '-':''}} </div>
                      <el-select
                        clearable
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.investDirect==PageDataAdd.beforeData.fundInfo.investDirect?'':'red':'']"
                        v-model="formInline.investDirect"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in investDirectArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="基金成立日期" prop="setupDate">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.setupDate==PageDataAdd.beforeData.fundInfo.setupDate?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.setupDate || '-':''}} </div>
                      <el-date-picker
                      @change="clearableDate"
                        v-model="formInline.setupDate"
                        type="date"
                        style="width:188px !important"
                        value-format="yyyy-MM-dd"
                        placeholder="选择日期"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.setupDate==PageDataAdd.beforeData.fundInfo.setupDate?'':'red':'']"
                      ></el-date-picker>
                      </el-tooltip>
                    </el-form-item>
                    <br />

                     <!-- 基金日期 -->
                    <el-form-item label="基金到期日期" prop="expireDate">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.expireDate==PageDataAdd.beforeData.fundInfo.expireDate?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.expireDate || '-':''}} </div>
                       <el-date-picker
                        style="width:188px !important"
                        @change="clearableDate"
                        v-model="formInline.expireDate"
                        type="date"
                        format="yyyy-MM-dd"
                        value-format="yyyy-MM-dd"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.expireDate==PageDataAdd.beforeData.fundInfo.expireDate?'':'red':'']"
                        placeholder="选择日期">
                      </el-date-picker>
                      </el-tooltip>
                    </el-form-item>

                    <el-form-item label="基金备案日期" prop="recordDate">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.recordDate==PageDataAdd.beforeData.fundInfo.recordDate?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.recordDate || '-':''}} </div>
                      <el-date-picker
                        v-model="formInline.recordDate"
                        type="date"
                        style="width:188px !important"
                        value-format="yyyy-MM-dd"
                        placeholder="选择日期"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.recordDate==PageDataAdd.beforeData.fundInfo.recordDate?'':'red':'']"
                      ></el-date-picker>
                      </el-tooltip>
                    </el-form-item>
                    <br />

                    <el-form-item label="运作方式" prop="operateType">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.operateType==PageDataAdd.beforeData.fundInfo.operateType?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?operateType || '-':''}} </div>
                      <el-select
                        clearable
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.operateType==PageDataAdd.beforeData.fundInfo.operateType?'':'red':'']"
                        v-model="formInline.operateType"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in operateTypeArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="产品状态" prop="fundState">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.fundState==PageDataAdd.beforeData.fundInfo.fundState?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?fundState || '-':''}} </div>
                      <el-select
                        clearable
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.fundState==PageDataAdd.beforeData.fundInfo.fundState?'':'red':'']"
                        v-model="formInline.fundState"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in fundStateArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-row>
                  <el-col :span="6" :offset="10">
                    <el-button
                      v-btn="saveCode"
                      type="primary"
                      :loading="countSubmit_btn"
                      plain
                      @click="myTabNext('1')"
                      style="margin-bottom: 5px; "
                      size="small"
                    >保存草稿</el-button>
                  </el-col>
                </el-row>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>
        <el-tab-pane label="交易信息" name="second">
          <span slot="label" v-if="PageDataAdd.addType==0&&PageDataAdd.beforeData?jyxx_i_show||jyxx_i_show2?true:false:false">交易信息<i style="color: red" class="el-icon-warning"></i></span>
          <div class="product_detail">
            <el-row>
              <el-col :span="23" :offset="1">
                <el-row>
                  <el-col :span="11">
                    <el-form-item label="认申购起点（不含费）元" prop="purchasePoint">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.purchasePoint==PageDataAdd.beforeData.fundInfo.purchasePoint?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.purchasePoint || '-':''}} </div>
                      <el-input
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.purchasePoint==PageDataAdd.beforeData.fundInfo.purchasePoint?'':'red':'']"
                        v-model="formInline.purchasePoint"
                        @focus="moneyFocus"
                        @blur="moneyBlur"
                        auto-complete="off"
                        show-word-limit
                        placeholder="请输入金额"
                      ></el-input>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="认购交易确认天数" prop="subscribeConfirmDay">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.subscribeConfirmDay==PageDataAdd.beforeData.fundInfo.subscribeConfirmDay?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?subscribeConfirmDay || '-':''}} </div>
                      <el-select
                        clearable
                        v-model="formInline.subscribeConfirmDay"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.subscribeConfirmDay==PageDataAdd.beforeData.fundInfo.subscribeConfirmDay?'':'red':'']"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in subscribeConfirmDayArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="认购费率（%）" prop="subscribeRate">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.subscribeRate==PageDataAdd.beforeData.fundInfo.subscribeRate?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.subscribeRate || '-':''}} </div>
                      <el-input
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.subscribeRate==PageDataAdd.beforeData.fundInfo.subscribeRate?'':'red':'']"
                        v-model="formInline.subscribeRate"
                        :maxlength="16"
                      ></el-input>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="申购资金交收天数" prop="applyDeliverDay">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.applyDeliverDay==PageDataAdd.beforeData.fundInfo.applyDeliverDay?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?applyDeliverDay || '-':''}} </div>
                      <el-select
                        clearable
                        v-model="formInline.applyDeliverDay"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.applyDeliverDay==PageDataAdd.beforeData.fundInfo.applyDeliverDay?'':'red':'']"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in applyDeliverDayArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="销售服务费计提" prop="saleFeePrepare">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.saleFeePrepare==PageDataAdd.beforeData.fundInfo.saleFeePrepare?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?saleFeePrepare || '-':''}} </div>
                      <el-select
                        clearable
                        v-model="formInline.saleFeePrepare"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.saleFeePrepare==PageDataAdd.beforeData.fundInfo.saleFeePrepare?'':'red':'']"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in saleFeePrepareArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="赎回交易确认天数" prop="callConfirmDay">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.callConfirmDay==PageDataAdd.beforeData.fundInfo.callConfirmDay?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?callConfirmDay || '-':''}} </div>
                      <el-select
                        clearable
                        v-model="formInline.callConfirmDay"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.callConfirmDay==PageDataAdd.beforeData.fundInfo.callConfirmDay?'':'red':'']"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in callConfirmDayArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="赎回费率浮动类型" prop="callFloatType">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.callFloatType==PageDataAdd.beforeData.fundInfo.callFloatType?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?callFloatType || '-':''}} </div>
                      <el-select
                        clearable
                        v-model="formInline.callFloatType"
                        @change="callFloatTypeChange"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.callFloatType==PageDataAdd.beforeData.fundInfo.callFloatType?'':'red':'']"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in callFloatTypeArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item
                      label="赎回费率类型"
                      prop="callRateType"
                      v-if="callFloat_select_show"
                      :rules="callRateTypeRul"
                    >
                    <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.callRateType==PageDataAdd.beforeData.fundInfo.callRateType?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?callRateType || '-':''}} </div>
                      <el-select
                        v-model="formInline.callRateType"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.callRateType==PageDataAdd.beforeData.fundInfo.callRateType?'':'red':'']"
                        placeholder="请选择"
                        @change="callDeliverDaySelect"
                        @visible-change='RedeemVisibleChange'
                      >
                        <el-option
                          v-for="(group, index) in callRateTypeArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                    <!-- --- -->
                    <el-form-item
                      label="赎回费率（%）"
                      prop="callRate"
                      v-if="callFloat_input_show"
                      :rules="callRateRul"
                    >
                    <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.callRate==PageDataAdd.beforeData.fundInfo.callRate?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.callRate || '-':''}} </div>
                      <el-input
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.callRate==PageDataAdd.beforeData.fundInfo.callRate?'':'red':'']"
                        v-model="formInline.callRate"
                        :maxlength="16"
                      ></el-input>
                      </el-tooltip>
                    </el-form-item>
                  </el-col>

                  <el-col :span="11" :offset="1">
                    <el-form-item label="封闭期" prop="blockDate">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.blockDate==PageDataAdd.beforeData.fundInfo.blockDate?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.blockDate || '-':''}} </div>
                      <el-date-picker
                        v-model="formInline.blockDate"
                        type="date"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.blockDate==PageDataAdd.beforeData.fundInfo.blockDate?'':'red':'']"
                        style="width:188px !important"
                        value-format="yyyy-MM-dd"
                        placeholder="选择日期"
                      ></el-date-picker>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="追加认申购级差" prop="purchaseDiffAppend">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.purchaseDiffAppend==PageDataAdd.beforeData.fundInfo.purchaseDiffAppend?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.purchaseDiffAppend || '-':''}} </div>
                      <!-- <el-input-number
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.purchaseDiffAppend==PageDataAdd.beforeData.fundInfo.purchaseDiffAppend?'':'red':'']"
                        v-model="formInline.purchaseDiffAppend"
                        controls-position="right"
                        :min="-999"
                        :max="100"
                      ></el-input-number> -->
                      <el-input
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.purchaseDiffAppend==PageDataAdd.beforeData.fundInfo.purchaseDiffAppend?'':'red':'']"
                        v-model="formInline.purchaseDiffAppend"
                      ></el-input>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="认购资金交收天数" prop="subscribeDeliverDay">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.subscribeDeliverDay==PageDataAdd.beforeData.fundInfo.subscribeDeliverDay?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?subscribeDeliverDay || '-':''}} </div>
                      <el-select
                        clearable
                        v-model="formInline.subscribeDeliverDay"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.subscribeDeliverDay==PageDataAdd.beforeData.fundInfo.subscribeDeliverDay?'':'red':'']"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in subscribeDeliverDayArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="申购交易确认天数" prop="applyConfirmDay">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.applyConfirmDay==PageDataAdd.beforeData.fundInfo.applyConfirmDay?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?applyConfirmDay || '-':''}} </div>
                      <el-select
                        clearable
                        v-model="formInline.applyConfirmDay"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.applyConfirmDay==PageDataAdd.beforeData.fundInfo.applyConfirmDay?'':'red':'']"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in applyConfirmDayArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="申购费率（%）" prop="applyRate">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.applyRate==PageDataAdd.beforeData.fundInfo.applyRate?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.applyRate || '-':''}} </div>
                      <el-input
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.applyRate==PageDataAdd.beforeData.fundInfo.applyRate?'':'red':'']"
                        v-model="formInline.applyRate"
                        :maxlength="16"
                      ></el-input>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="销售服务费支付" prop="saleFeePay">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.saleFeePay==PageDataAdd.beforeData.fundInfo.saleFeePay?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?saleFeePay || '-':''}} </div>
                      <el-select
                        clearable
                        v-model="formInline.saleFeePay"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.saleFeePay==PageDataAdd.beforeData.fundInfo.saleFeePay?'':'red':'']"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in saleFeePayArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="赎回资金交收天数" prop="callDeliverDay">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.callDeliverDay==PageDataAdd.beforeData.fundInfo.callDeliverDay?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?callDeliverDay || '-':''}} </div>
                      <el-select
                        clearable
                        v-model="formInline.callDeliverDay"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.callDeliverDay==PageDataAdd.beforeData.fundInfo.callDeliverDay?'':'red':'']"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in callDeliverDayArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                    <!-- 估值频率 -->
                    <el-form-item label="估值频率" prop="assetFrequency">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.assetFrequency==PageDataAdd.beforeData.fundInfo.assetFrequency?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?assetFrequency || '-':''}} </div>
                      <el-select
                        clearable
                        v-model="formInline.assetFrequency"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.assetFrequency==PageDataAdd.beforeData.fundInfo.assetFrequency?'':'red':'']"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in guZhiist"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>

                  </el-col>
                </el-row>
                <el-row v-if="callFloat_select_show">
                  <el-col :span="19" :offset="1" v-if="mdFlagOpen">
                    <div style="height:10px;margin-top:10px">
                      <el-button
                        type="primary"
                        plain
                        @click="insertEventRedReem('redeem',-1)"
                        style="margin-bottom: 5px; "
                        size="small"
                      >
                        <i class="el-icon-circle-plus-outline"></i>新增
                      </el-button>
                      <el-button
                        type="danger"
                        plain
                        @click="removeEvent('redeem')"
                        style="margin-bottom: 5px; "
                        size="small"
                      >
                        <i class="el-icon-delete"></i>移除
                      </el-button>
                    </div>
                    <!-- <el-button type="error"  plain  @click="revertEvent" style="margin-bottom: 5px; " size="small">
                          <i class="el-icon-back"></i>还原
                    </el-button>-->
                    <div style="margin-top:30px; widht: 100%">
                      <vxe-table
                        border
                        resizable
                        show-overflow
                        keep-source
                        sync-resize
                        auto-resize
                        ref="xTableRedeem"
                        height="350"
                        style="width: 100%"
                        :cell-class-name="cellClassName"
                        :header-cell-class-name="headerCellClassName"
                        :edit-rules="rulesRedeem"
                        :data="tableDataRedeem"
                        :edit-config="{trigger: 'click', mode: 'cell', icon: 'fa fa-pencil'}"
                      >
                        <vxe-table-column type="checkbox" width="60"></vxe-table-column>
                        <vxe-table-column type="seq" title="序号" width="60"></vxe-table-column>
                        <vxe-table-column
                          field="redeemFrom"
                          min-width="200"
                          title="区间起点"
                          :edit-render="{name: '$input', props: {type: 'data'}, events: { change: dateChangeFrom}, attrs: {type: 'text',maxlength:'13'}}"
                        >
                        <template slot-scope="scope">
                          <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.redeemFrom!=scope.row.change.redeemFrom?false:true:true:true'>
                            <div slot="content">
                              <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.redeemFrom||'-':'-':'-'}} </span>
                            </div>
                            <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.redeemFrom!=scope.row.change.redeemFrom?'red':'':'':''">
                              {{scope.row.redeemFrom}}
                            </span>
                          </el-tooltip>
                        </template>
                        </vxe-table-column>
                        <vxe-table-column
                          field="redeemTo"
                          min-width="200"
                          title="区间终点"
                          :edit-render="{name: '$input', events: { change: dateChangeTo}, attrs: {type: 'text',maxlength:'13'}}"
                        >
                        <template slot-scope="scope">
                          <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.redeemTo!=scope.row.change.redeemTo?false:true:true:true'>
                            <div slot="content">
                              <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.redeemTo||'-':'-':'-'}} </span>
                            </div>
                            <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.redeemTo!=scope.row.change.redeemTo?'red':'':'':''">
                              {{scope.row.redeemTo}}
                            </span>
                          </el-tooltip>
                        </template>
                        </vxe-table-column>
                        <vxe-table-column
                          field="redeemRate"
                          min-width="200"
                          title="费率（%）"
                          :edit-render="{name: 'input', attrs: {type: 'text',maxlength:'16'}}"
                        >
                        <template slot-scope="scope">
                          <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.redeemRate!=scope.row.change.redeemRate?false:true:true:true'>
                            <div slot="content">
                              <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.redeemRate||'-':'-':'-'}} </span>
                            </div>
                            <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.redeemRate!=scope.row.change.redeemRate?'red':'':'':''">
                              {{scope.row.redeemRate}}
                            </span>
                          </el-tooltip>
                        </template>
                        </vxe-table-column>
                      </vxe-table>
                    </div>
                  </el-col>
                </el-row>

                <el-row style="margin-top:10px">
                  <el-col :span="6" :offset="10">
                    <el-button
                      v-btn="saveCode"
                      type="primary"
                      :loading="countSubmit_btn"
                      plain
                      @click="myTabNext('2')"
                      style="margin-bottom: 5px; "
                      size="small"
                    >保存草稿</el-button>
                  </el-col>
                </el-row>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>
        <el-tab-pane label="费用信息" name="third">
          <span slot="label" v-if="PageDataAdd.addType==0&&PageDataAdd.beforeData?fyxx_i_show||fyxx_i_show2?true:false:false">费用信息<i style="color: red" class="el-icon-warning"></i></span>
          <div class="product_detail">
            <el-row>
              <el-col :span="23" :offset="1">
                <el-row>
                  <el-form-item label="管理费" prop="manageFeePrepare">
                    <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.manageFeePrepare==PageDataAdd.beforeData.fundInfo.manageFeePrepare?true:false:true'>
                      <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?manageFeePrepare || '-':''}} </div>
                    <el-select
                      clearable
                      v-model="formInline.manageFeePrepare"
                      :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.manageFeePrepare==PageDataAdd.beforeData.fundInfo.manageFeePrepare?'':'red':'']"
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="(group, index) in manageFeePrepareArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme"
                      ></el-option>
                    </el-select>
                    </el-tooltip>
                  
                    <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.manageFeeAsset==PageDataAdd.beforeData.fundInfo.manageFeeAsset?true:false:true'>
                      <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?manageFeeAsset || '-':''}} </div>
                    <el-select
                      clearable
                      v-model="formInline.manageFeeAsset"
                      :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.manageFeeAsset==PageDataAdd.beforeData.fundInfo.manageFeeAsset?'':'red':'']"
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="(group, index) in manageFeeAssetArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme"
                      ></el-option>
                    </el-select>
                    </el-tooltip>
                    
                    <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.manageFeePay==PageDataAdd.beforeData.fundInfo.manageFeePay?true:false:true'>
                      <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?manageFeePay || '-':''}} </div>
                    <el-select
                      clearable
                      v-model="formInline.manageFeePay"
                      :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.manageFeePay==PageDataAdd.beforeData.fundInfo.manageFeePay?'':'red':'']"
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="(group, index) in manageFeePayArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme"
                      ></el-option>
                    </el-select>
                    </el-tooltip>
                  </el-form-item>

                  <el-form-item label="托管费" prop="trustFeePrepare">
                    <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.trustFeePrepare==PageDataAdd.beforeData.fundInfo.trustFeePrepare?true:false:true'>
                      <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?trustFeePrepare || '-':''}} </div>
                    <el-select
                      clearable
                      v-model="formInline.trustFeePrepare"
                      :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.trustFeePrepare==PageDataAdd.beforeData.fundInfo.trustFeePrepare?'':'red':'']"
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="(group, index) in manageFeePrepareArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme"
                      ></el-option>
                    </el-select>
                    </el-tooltip>

                    <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.trustFeeAsset==PageDataAdd.beforeData.fundInfo.trustFeeAsset?true:false:true'>
                      <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?trustFeeAsset || '-':''}} </div>
                    <el-select
                      clearable
                      v-model="formInline.trustFeeAsset"
                      :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.trustFeeAsset==PageDataAdd.beforeData.fundInfo.trustFeeAsset?'':'red':'']"
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="(group, index) in manageFeeAssetArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme"
                      ></el-option>
                    </el-select>
                    </el-tooltip>

                    <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.trustFeePay==PageDataAdd.beforeData.fundInfo.trustFeePay?true:false:true'>
                      <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?trustFeePay || '-':''}} </div>
                    <el-select
                      clearable
                      v-model="formInline.trustFeePay"
                      :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.trustFeePay==PageDataAdd.beforeData.fundInfo.trustFeePay?'':'red':'']"
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="(group, index) in manageFeePayArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme"
                      ></el-option>
                    </el-select>
                    </el-tooltip>
                  </el-form-item>

                  <el-form-item label="运营服务费" prop="operateFeePrepare">
                    <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.operateFeePrepare==PageDataAdd.beforeData.fundInfo.operateFeePrepare?true:false:true'>
                      <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?operateFeePrepare || '-':''}} </div>
                    <el-select
                      clearable
                      v-model="formInline.operateFeePrepare"
                      :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.operateFeePrepare==PageDataAdd.beforeData.fundInfo.operateFeePrepare?'':'red':'']"
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="(group, index) in manageFeePrepareArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme"
                      ></el-option>
                    </el-select>
                    </el-tooltip>

                    <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.operateFeeAsset==PageDataAdd.beforeData.fundInfo.operateFeeAsset?true:false:true'>
                      <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?operateFeeAsset || '-':''}} </div>
                    <el-select
                      clearable
                      v-model="formInline.operateFeeAsset"
                      :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.operateFeeAsset==PageDataAdd.beforeData.fundInfo.operateFeeAsset?'':'red':'']"
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="(group, index) in manageFeeAssetArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme"
                      ></el-option>
                    </el-select>
                    </el-tooltip>

                    <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.operateFeePay==PageDataAdd.beforeData.fundInfo.operateFeePay?true:false:true'>
                      <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?operateFeePay || '-':''}} </div>
                    <el-select
                      clearable
                      v-model="formInline.operateFeePay"
                      :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.operateFeePay==PageDataAdd.beforeData.fundInfo.operateFeePay?'':'red':'']"
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="(group, index) in manageFeePayArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme"
                      ></el-option>
                    </el-select>
                    </el-tooltip>
                  </el-form-item>

                  <el-col :span="11">
                    <el-form-item label="管理费率（%）" prop="manageRate">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.manageRate==PageDataAdd.beforeData.fundInfo.manageRate?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.manageRate || '-':''}} </div>
                      <el-input
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.manageRate==PageDataAdd.beforeData.fundInfo.manageRate?'':'red':'']"
                        v-model="formInline.manageRate"
                        :maxlength="16"
                      ></el-input>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="运营服务费（%）" prop="operateRate">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.operateRate==PageDataAdd.beforeData.fundInfo.operateRate?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.operateRate || '-':''}} </div>
                      <el-input
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.operateRate==PageDataAdd.beforeData.fundInfo.operateRate?'':'red':'']"
                        v-model="formInline.operateRate"
                        :maxlength="16"
                      ></el-input>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="管理人账号" prop="manageAccount">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.manageAccount==PageDataAdd.beforeData.fundInfo.manageAccount?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.manageAccount || '-':''}} </div>
                      <el-input
                        v-model="formInline.manageAccount"
                        placeholder="管理人账号"
                        type="text"
                        maxlength="33"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.manageAccount==PageDataAdd.beforeData.fundInfo.manageAccount?'':'red':'']"
                        auto-complete="off"
                      />
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="业绩报酬" prop="rewardType">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.rewardType==PageDataAdd.beforeData.fundInfo.rewardType?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?rewardType || '-':''}} </div>
                      <el-select
                        clearable
                        v-model="formInline.rewardType"
                        @change="rewardTypeChange"
                        @visible-change='visibleChange'
                        @clear='btnClear'
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.rewardType==PageDataAdd.beforeData.fundInfo.rewardType?'':'red':'']"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in rewardTypeArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                  </el-col>

                  <el-col :span="11" :offset="1">
                    <el-form-item label="托管费率（%）" prop="trustRate">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.trustRate==PageDataAdd.beforeData.fundInfo.trustRate?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.trustRate || '-':''}} </div>
                      <el-input
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.trustRate==PageDataAdd.beforeData.fundInfo.trustRate?'':'red':'']"
                        v-model="formInline.trustRate"
                        :maxlength="16"
                      ></el-input>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item style="visibility:hidden">
                      <el-input></el-input>
                    </el-form-item><br />
                    <el-form-item label="管理人收费账户名称" prop="manageAccountName">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.manageAccountName==PageDataAdd.beforeData.fundInfo.manageAccountName?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.manageAccountName || '-':''}} </div>
                      <el-input
                        v-model="formInline.manageAccountName"
                        placeholder="管理人收费账户名称"
                        type="text"
                        maxlength="100"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.manageAccountName==PageDataAdd.beforeData.fundInfo.manageAccountName?'':'red':'']"
                        auto-complete="off"
                      />
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="管理人开户银行名称" prop="manageBankName">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.manageBankName==PageDataAdd.beforeData.fundInfo.manageBankName?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.manageBankName || '-':''}} </div>
                      <el-input
                        v-model="formInline.manageBankName"
                        placeholder="管理人开户银行名称"
                        type="text"
                        maxlength="100"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.manageBankName==PageDataAdd.beforeData.fundInfo.manageBankName?'':'red':'']"
                        auto-complete="off"
                      />
                      </el-tooltip>
                    </el-form-item>
                    <br />
                  </el-col>
                </el-row>
                <el-row>
                  <el-col :span="24">
                      <el-form-item v-show="rewardType_show" label="计提方式" prop="rewardPrepareType">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.rewardPrepareType==PageDataAdd.beforeData.fundInfo.rewardPrepareType?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?rewardPrepareType || '-':''}} </div>
                      <el-select
                        v-model="formInline.rewardPrepareType"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.rewardPrepareType==PageDataAdd.beforeData.fundInfo.rewardPrepareType?'':'red':'']"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in rewardPrepareTypeArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>

                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.isFixedPrepare==PageDataAdd.beforeData.fundInfo.isFixedPrepare?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?isFixedPrepare || '-':''}} </div>
                      <el-select
                          clearable
                          @change="isFixedPrepareChange"
                          v-model="formInline.isFixedPrepare"
                          :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.isFixedPrepare==PageDataAdd.beforeData.fundInfo.isFixedPrepare?'':'red':'']"
                          placeholder="请选择"
                        >
                        <el-option
                          v-for="(group, index) in isFixedPrepareArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>

                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.rewardPrepareDate==PageDataAdd.beforeData.fundInfo.rewardPrepareDate?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?rewardPrepareDate || '-':''}} </div>
                      <el-select
                          clearable
                          v-show="rewardPrepareDate_show"
                          v-model="formInline.rewardPrepareDate"
                          :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.rewardPrepareDate==PageDataAdd.beforeData.fundInfo.rewardPrepareDate?'':'red':'']"
                          placeholder="请选择"
                        >
                        <el-option
                          v-for="(group, index) in rewardPrepareDateArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                      </el-form-item>
                  </el-col>
                </el-row>
                <!--计提方式FROM  to  -->
                <el-row v-if="rewardType_show">
                  <el-col :span="19" :offset="1">
                    <el-button
                      type="primary"
                      plain
                      @click="insertEvent('reward', -1)"
                      style="margin-bottom: 5px; "
                      size="small"
                    >
                      <i class="el-icon-circle-plus-outline"></i>新增
                    </el-button>
                    <el-button
                      type="danger"
                      plain
                      @click="removeEvent('reward')"
                      style="margin-bottom: 5px; "
                      size="small"
                    >
                      <i class="el-icon-delete"></i>移除
                    </el-button>

                    <!-- <el-button type="error"  plain  @click="revertEvent" style="margin-bottom: 5px; " size="small">
                            <i class="el-icon-back"></i>还原
                    </el-button>-->
                    <vxe-table
                      border
                      keep-source
                      show-overflow
                      ref="xTableReward"
                      class="my_table_insert"
                      height="350"
                      :cell-class-name="cellClassName"
                      :header-cell-class-name="headerCellClassName"
                      :edit-rules="validRewardRules"
                      :data="tableDataReward"
                      :edit-config="{trigger: 'click', mode: 'cell', icon: 'fa fa-pencil'}"
                    >
                      <vxe-table-column type="checkbox" width="60"></vxe-table-column>
                      <vxe-table-column type="seq" title="序号" width="60"></vxe-table-column>
                      <vxe-table-column
                        field="rewardFrom"
                        min-width="200"
                        title="区间起点"
                        :edit-render="{name: '$input', props: {type: 'data'}, events: { change: dateChangeFrom}, attrs: {type: 'text',maxlength:'13'}}"
                      >
                      <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.rewardFrom!=scope.row.change.rewardFrom?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.rewardFrom||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.rewardFrom!=scope.row.change.rewardFrom?'red':'':'':''">
                          {{scope.row.rewardFrom}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                      <vxe-table-column
                        field="rewardTo"
                        min-width="200"
                        title="区间终点"
                        :edit-render="{name: '$input', events: { change: dateChangeTo}, attrs: {type: 'text',maxlength:'13'}}"
                      >
                      <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.rewardTo!=scope.row.change.rewardTo?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.rewardTo||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.rewardTo!=scope.row.change.rewardTo?'red':'':'':''">
                          {{scope.row.rewardTo}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                      <vxe-table-column
                        field="rewardRate"
                        min-width="200"
                        title="计提比例（%）"
                        :edit-render="{name: 'input', attrs: {type: 'text',maxlength:'16'}}"
                      >
                      <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.rewardRate!=scope.row.change.rewardRate?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.rewardRate||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.rewardRate!=scope.row.change.rewardRate?'red':'':'':''">
                          {{scope.row.rewardRate}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                    </vxe-table>
                  </el-col>
                </el-row>

                <el-row style="margin-top:10px">
                  <el-col :span="6" :offset="10">
                    <el-button
                      v-btn="saveCode"
                      type="primary"
                      :loading="countSubmit_btn"
                      plain
                      @click="myTabNext('3')"
                      style="margin-bottom: 5px; "
                      size="small"
                    >保存草稿</el-button>
                  </el-col>
                </el-row>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>
        <el-tab-pane label="收益分配" name="fourth">
          <span slot="label" v-if="PageDataAdd.addType==0&&PageDataAdd.beforeData&&syfp_i_show">收益分配<i style="color: red" class="el-icon-warning"></i></span>
          <div class="product_detail">
            <el-row>
              <el-col :span="23" :offset="1">
                <el-row>
                  <el-form-item label="收益分配说明" prop="incomePortionDesc">
                    <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.incomePortionDesc==PageDataAdd.beforeData.fundInfo.incomePortionDesc?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.incomePortionDesc || '-':''}} </div>
                    <el-input
                      type="textarea"
                      :rows="2"
                      maxlength="1000"
                      show-word-limit
                      :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.incomePortionDesc==PageDataAdd.beforeData.fundInfo.incomePortionDesc?'':'red':'']"
                      style="width:590px"
                      placeholder="请输入内容"
                      v-model="formInline.incomePortionDesc"
                    ></el-input>
                    </el-tooltip>
                  </el-form-item>
                  <br />
                  <el-col :span="11">
                    <el-form-item label="分配次数" prop="portionNumber">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.portionNumber==PageDataAdd.beforeData.fundInfo.portionNumber?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?portionNumber || '-':''}} </div>
                      <el-select
                        clearable
                        v-model="formInline.portionNumber"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.portionNumber==PageDataAdd.beforeData.fundInfo.portionNumber?'':'red':'']"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in portionNumberArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="预估数据以及计算报表" prop="dataExpect">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.dataExpect==PageDataAdd.beforeData.fundInfo.dataExpect?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.dataExpect || '-':''}} </div>
                      <el-select
                        clearable
                        v-model="formInline.dataExpect"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.dataExpect==PageDataAdd.beforeData.fundInfo.dataExpect?'':'red':'']"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in dataExpectArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="分红资金交收" prop="bonusDeliver">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.bonusDeliver==PageDataAdd.beforeData.fundInfo.bonusDeliver?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.bonusDeliver || '-':''}} </div>
                      <el-select
                        clearable
                        v-model="formInline.bonusDeliver"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.bonusDeliver==PageDataAdd.beforeData.fundInfo.bonusDeliver?'':'red':'']"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in bonusDeliverArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                  </el-col>

                  <el-col :span="11" :offset="1">
                    <el-form-item label="提交分红流程" prop="bonusProcess">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.bonusProcess==PageDataAdd.beforeData.fundInfo.bonusProcess?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.bonusProcess || '-':''}} </div>
                      <el-select
                        clearable
                        v-model="formInline.bonusProcess"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.bonusProcess==PageDataAdd.beforeData.fundInfo.bonusProcess?'':'red':'']"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in bonusProcessArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                    <br />
                    <el-form-item label="分红数据确认" prop="bonusConfim">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.bonusConfim==PageDataAdd.beforeData.fundInfo.bonusConfim?true:false:true'>
                        <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.bonusConfim || '-':''}} </div>
                      <el-select
                        clearable
                        v-model="formInline.bonusConfim"
                        :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.bonusConfim==PageDataAdd.beforeData.fundInfo.bonusConfim?'':'red':'']"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in bonusConfimArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                      </el-tooltip>
                    </el-form-item>
                  </el-col>
                </el-row>

                <el-row>
                  <el-col :span="6" :offset="10">
                    <el-button
                      v-btn="saveCode"
                      type="primary"
                      :loading="countSubmit_btn"
                      plain
                      @click="myTabNext('4')"
                      style="margin-bottom: 5px; "
                      size="small"
                    >保存草稿</el-button>
                  </el-col>
                </el-row>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>

        <el-tab-pane label="投资风控" name="six">
          <span slot="label" v-if="PageDataAdd.addType==0&&PageDataAdd.beforeData?tzfk_i_show||tzfk_i_show2?true:false:false">投资风控<i style="color: red" class="el-icon-warning"></i></span>
          <div class="product_detail fkheight">
            <el-row>
              <el-col :span="23" :offset="1">
                <el-form-item label="投资范围">
                  <div class="product_detail">
                    <el-checkbox
                      :indeterminate="isIndeterminate"
                      v-model="checkAll"
                      @change="handleCheckAllChange"
                    >全选</el-checkbox>
                    <div style="margin: 15px 0;"></div>
                    <el-checkbox-group
                      v-model="checkfundInvestArea"
                      @change="handleCheckedInvestAreaChange"
                    >
                      <div v-for="(group, index) in fundInvestArea" :key="index">
                          <el-checkbox :label="group.id">
                            <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?!group.change ? 'red' : '':'' ">
                              {{group.dimNme}}
                            </span>
                          </el-checkbox>
                          <!-- <el-checkbox :label="group.id" disabled>
                            <span :class=" !group.change ? 'errInof' : '' "> {{group.dimNme}} </span>
                          </el-checkbox> -->
                      </div>
                    </el-checkbox-group>
                  </div>
                </el-form-item>
                <br />

                <el-form-item label="投资限制" prop="investLimit">
                  <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.investLimit==PageDataAdd.beforeData.fundInfo.investLimit?true:false:true'>
                    <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.investLimit || '-':''}} </div>
                  <el-input
                    type="textarea"
                    :rows="4"
                    style="width:605px"
                    maxlength="1000"
                    show-word-limit
                    placeholder="请输入内容"
                    :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.investLimit==PageDataAdd.beforeData.fundInfo.investLimit?'':'red':'']"
                    v-model="formInline.investLimit"
                    ref="investLimit"
                  ></el-input>
                  </el-tooltip>
                </el-form-item>
                <br />
                <el-form-item label="预警线" prop="warnPoint">
                  <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.warnPoint==PageDataAdd.beforeData.fundInfo.warnPoint?true:false:true'>
                    <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.warnPoint || '-':''}} </div>
                  <el-input
                    v-on:input="warnPointInput"
                    :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.warnPoint==PageDataAdd.beforeData.fundInfo.warnPoint?'':'red':'']"
                    v-model="formInline.warnPoint"
                    placeholder="预警线"
                    maxlength="16"
                    ref="warnPoint"
                  ></el-input>
                  </el-tooltip>
                  <span ref="jump" id="targetbox"></span>
                </el-form-item>
                <el-form-item label="止损线" prop="lossPoint" label-width="215px">
                  <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.lossPoint==PageDataAdd.beforeData.fundInfo.lossPoint?true:false:true'>
                    <div slot="content">修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?PageDataAdd.beforeData.fundInfo.lossPoint || '-':''}} </div>
                  <el-input
                    v-on:input="lossPointInput"
                    :class="['el_form_item', PageDataAdd.addType==0&&PageDataAdd.beforeData?formInline.lossPoint==PageDataAdd.beforeData.fundInfo.lossPoint?'':'red':'']"
                    v-model="formInline.lossPoint"
                    placeholder="止损线"
                    maxlength="16"
                    ref="lossPoint"
                  ></el-input>
                  </el-tooltip>
                </el-form-item>

                <el-row>
                  <el-col :span="6" :offset="10">
                    <el-button
                      v-btn="saveCode"
                      type="primary"
                      :loading="countSubmit_btn"
                      plain
                      @click="myTabNext('6')"
                      style="margin-bottom: 5px; "
                      size="small"
                    >保存草稿</el-button>
                  </el-col>
                </el-row>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>
        <el-tab-pane label="分类关系" v-if="isFj_show" name="eight">
          <!-- v-if="PageDataAdd.fjgx_show || PageDataAdd.formData.fundGrades.length>0" -->  
          <!-- 放在div里面 -->
          <span slot="label" v-if="PageDataAdd.addType==0&&PageDataAdd.beforeData&&fjgx_i_show">分类关系<i style="color: red" class="el-icon-warning"></i></span>
          <div
            class="product_detail"
          >
            <el-row>
              <el-col :span="23" :offset="1">
                <div style="height:10px">
                  <el-button
                    type="primary"
                    plain
                    @click="insertEvent('grade',-1)"
                    style="margin-bottom: 5px; "
                    size="small"
                  >
                    <i class="el-icon-circle-plus-outline"></i>新增
                  </el-button>
                  <el-button
                    type="danger"
                    plain
                    @click="removeEvent('grade')"
                    style="margin-bottom: 5px; "
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

                <div style="margin-top:30px;">
                  <vxe-table
                    border
                    show-overflow
                    keep-source
                    auto-resize
                    ref="xTableGrade"
                    width="auto"
                    height="350"
                    :cell-class-name="cellClassName"
                    :header-cell-class-name="headerCellClassName"
                    :edit-rules="validGradeRules"
                    :data="tableDataGrade"
                    :edit-config="{trigger: 'click', mode: 'cell',showStatus: true,activeMethod: activeCellMethodGrade}"
                  >
                    <vxe-table-column type="checkbox" width="60px"></vxe-table-column>
                    <vxe-table-column type="seq" title="序号" width="60px"></vxe-table-column>
                    <vxe-table-column
                      width="20%"
                      field="fundCodeGrade"
                      title="分类代码"
                      :edit-render="{name: 'input', attrs: {type: 'text',maxlength:'20'}}"
                    >
                    <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.fundCodeGrade!=scope.row.change.fundCodeGrade?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.fundCodeGrade||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.fundCodeGrade!=scope.row.change.fundCodeGrade?'red':'':'':''">
                          {{scope.row.fundCodeGrade}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                    <vxe-table-column
                      width="15%"
                      field="fundNameGrade"
                      title="分类名称"
                      :edit-render="{name: 'input', attrs: {type: 'text',maxlength:'33'}}"
                    >
                    <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.fundNameGrade!=scope.row.change.fundNameGrade?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.fundNameGrade||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.fundNameGrade!=scope.row.change.fundNameGrade?'red':'':'':''">
                          {{scope.row.fundNameGrade}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>

                    <vxe-table-column
                      width="160px"
                      field="assetValue"
                      title="初始单位净值"
                      :edit-render="{name: '$input', attrs: {type: 'text',maxlength:'18'}}"
                    >
                    <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.assetValue!=scope.row.change.assetValue?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.assetValue||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.assetValue!=scope.row.change.assetValue?'red':'':'':''">
                          {{scope.row.assetValue}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>

                    <vxe-table-column
                      width="160px"
                      field="shareType"
                      title="基金分类级别"
                      :edit-render="{name: '$select', placement:'bottom', options: shareTypeArr,optionProps: {value: 'dimCde', label: 'dimNme'}}"
                    >
                    <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.shareType!=scope.row.change.shareType?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.shareType||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.shareType!=scope.row.change.shareType?'red':'':'':''">
                          {{scope.row.shareType}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                    <!-- <vxe-table-column
                      width="20%"
                      field="leverageRatio"
                      title="杠杆比例（%）"
                      :edit-render="{name: 'input', attrs: {type: 'text',maxlength:'6'}}"
                    ></vxe-table-column> -->
                    <vxe-table-column
                      min-width="130px"
                      field="beginDate"
                      title="开始日期"
                      :edit-render="{name: '$input', props: {type: 'date'}}"
                    >
                    <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.beginDate!=scope.row.change.beginDate?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.beginDate||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.beginDate!=scope.row.change.beginDate?'red':'':'':''">
                          {{scope.row.beginDate}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                    <vxe-table-column
                      min-width="130px"
                      field="endDate"
                      title="结束日期"
                      :edit-render="{name: '$input', props: {type: 'date'}}"
                    >
                    <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.endDate!=scope.row.change.endDate?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.endDate||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.endDate!=scope.row.change.endDate?'red':'':'':''">
                          {{scope.row.endDate}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                  </vxe-table>
                </div>
              </el-col>
            </el-row>

            <el-row style="margin-top:10px">
              <el-col :span="6" :offset="10">
                <el-button
                  v-btn="saveCode"
                  type="primary"
                  :loading="countSubmit_btn"
                  plain
                  @click="myTabNext('7')"
                  style="margin-bottom: 5px; "
                  size="small"
                >保存草稿</el-button>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>
        <!-- v-if="PageDataAdd.addType == 0"  -->
         <!-- v-if="PageDataAdd.xsfs_show || PageDataAdd.formData.fundSallers.length>0" -->
        <el-tab-pane label="销售方式" name="nine">
          <span slot="label" v-if="PageDataAdd.addType==0&&PageDataAdd.beforeData&&xsfs_i_show">销售方式<i style="color: red" class="el-icon-warning"></i></span>
          <div
            class="product_detail"
            v-loading='saleTypeDialog'
          >
            <el-row>
              <el-col :span="23" :offset="1">
                <div style="height:10px">
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
                    ></el-option>
                  </el-select>

                  <el-button
                    type="primary"
                    plain
                    @click="insertEvent('saller',-1)"
                    style="margin-bottom: 5px; "
                    size="small"
                  >
                    <i class="el-icon-circle-plus-outline"></i>新增
                  </el-button>
                  <el-button
                    type="danger"
                    plain
                    @click="removeEvent('saller')"
                    style="margin-bottom: 5px; "
                    size="small"
                  >
                    <i class="el-icon-delete"></i>移除
                  </el-button>
                </div>
                <!-- <el-button type="error"  plain  @click="revertEvent" style="margin-bottom: 5px; " size="small">
                    <i class="el-icon-back"></i>还原
                </el-button>-->

                <div style="margin-top:30px;">
                  <vxe-table
                    border
                    show-overflow
                    auto-resize
                    keep-source
                    ref="xTableMySaller"
                    width="auto"
                    height="350"
                    :cell-class-name="cellClassName"
                    :header-cell-class-name="headerCellClassName"
                    :edit-rules="validQd"
                    :data="tableDataSaller"
                    :edit-config="{trigger: 'click', mode: 'cell',showStatus: true,activeMethod: activeCellMethod}"
                  >
                    <vxe-table-column type="checkbox" width="40"></vxe-table-column>
                    <vxe-table-column type="seq" title="序号" width="60"></vxe-table-column>
                    <vxe-table-column
                      min-width="130px"
                      field="sallerName"
                      title="渠道名称"
                      :edit-render="{name: '$select', placement:'bottom', options: sallerNameArr,optionProps: {value: 'sallerName', label: 'sallerName'} ,events: {change: sallerNameChangeEvent}}"
                    >
                    <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.sallerName!=scope.row.change.sallerName?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.sallerName||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.sallerName!=scope.row.change.sallerName?'red':'':'':''">
                          {{scope.row.sallerName}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                    <vxe-table-column
                      min-width="130px"
                      field="sallerCode"
                      title="渠道编码"
                      :edit-render="{name: 'input', attrs: {type: 'text',maxlength:'8'}}"
                    >
                    <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.sallerCode!=scope.row.change.sallerCode?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.sallerCode||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.sallerCode!=scope.row.change.sallerCode?'red':'':'':''">
                          {{scope.row.sallerCode}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                    <vxe-table-column
                      min-width="130px"
                      field="sallerType"
                      title="销售方式"
                      :edit-render="{name: 'select', placement:'bottom', options: saleTypeArr,optionProps: {value: 'dimCde', label: 'dimNme'}}"
                    >
                    <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.sallerType!=scope.row.change.sallerCode?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.sallerType||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.sallerType!=scope.row.change.sallerType?'red':'':'':''">
                          {{scope.row.sallerType}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                    <vxe-table-column
                      min-width="180px"
                      field="feeRate"
                      title="管理费分成比例（%）"
                      :edit-render="{name: 'input', attrs: {type: 'text',maxlength:'16'}}"
                    >
                    <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.feeRate!=scope.row.change.feeRate?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.feeRate||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.feeRate!=scope.row.change.feeRate?'red':'':'':''">
                          {{scope.row.feeRate}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                    <vxe-table-column
                      min-width="130px"
                      field="beginDate"
                      title="开始日期"
                      :edit-render="{name: '$input', props: {type: 'date'}}"
                    >
                    <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.beginDate!=scope.row.change.beginDate?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.beginDate||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.beginDate!=scope.row.change.beginDate?'red':'':'':''">
                          {{scope.row.beginDate}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                    <vxe-table-column
                      min-width="130px"
                      field="endDate"
                      title="结束日期"
                      :edit-render="{name: '$input', props: {type: 'date'}}"
                    >
                    <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.endDate!=scope.row.change.endDate?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.endDate||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.endDate!=scope.row.change.endDate?'red':'':'':''">
                          {{scope.row.endDate}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                  </vxe-table>
                </div>
              </el-col>
            </el-row>
            <el-row style="margin-top:10px">
              <el-col :span="6" :offset="10">
                <el-button
                  v-btn="saveCode"
                  type="primary"
                  :loading="countSubmit_btn"
                  plain
                  @click="myTabNext('8')"
                  style="margin-bottom: 5px; "
                  size="small"
                >保存草稿</el-button>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>
        <!-- v-if="PageDataAdd.kfr_show || PageDataAdd.formData.fundOpens.length>0 " -->
        <el-tab-pane label="开放日" name="ten">
          <span slot="label" v-if="PageDataAdd.addType==0&&PageDataAdd.beforeData&&kfr_i_show">开放日<i style="color: red" class="el-icon-warning"></i></span>
          <div
            class="product_detail"
          >
            <el-row>
              <el-col :span="23" :offset="1">
                <div style="height:10px">
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
                    ></el-option>
                  </el-select>

                  <el-button
                    type="primary"
                    plain
                    @click="insertEvent('open',-1)"
                    style="margin-bottom: 5px; "
                    size="small"
                  >
                    <i class="el-icon-circle-plus-outline"></i>新增
                  </el-button>
                  <el-button
                    type="danger"
                    plain
                    @click="removeEvent('open')"
                    style="margin-bottom: 5px; "
                    size="small"
                  >
                    <i class="el-icon-delete"></i>移除
                  </el-button>
                </div>
                <!-- <el-button type="error"  plain  @click="revertEvent" style="margin-bottom: 5px; " size="small">
                    <i class="el-icon-back"></i>还原
                </el-button>-->
                <div style="margin-top:30px;">
                  <vxe-table
                    border
                    auto-resize
                    show-overflow
                    keep-source
                    ref="xTableMyOpen"
                    width="auto"
                    height="350"
                    :cell-class-name="cellClassName"
                    :header-cell-class-name="headerCellClassName"
                    :edit-rules="validRulesKf"
                    :data="tableDataOpen"
                    :edit-config="{trigger: 'click', mode: 'cell',showStatus: true}"
                  >
                    <vxe-table-column type="checkbox" width="40"></vxe-table-column>
                    <vxe-table-column type="seq" title="序号" width="60"></vxe-table-column>
                    <vxe-table-column
                      min-width="130px"
                      field="openFrequence"
                      title="开放频率"
                      :edit-render="{name: 'select', placement:'bottom', options: openFrequenceArr,optionProps: {value: 'dimCde', label: 'dimNme'}}"
                    >
                    <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.openFrequence!=scope.row.change.openFrequence?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?transition_openFrequence(scope.row.change.openFrequence)||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.openFrequence!=scope.row.change.openFrequence?'red':'':'':''">
                          {{transition_openFrequence(scope.row.openFrequence)}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                    <vxe-table-column
                      min-width="130px"
                      field="openRule"
                      title="开放规则"
                      :edit-render="{name: 'select', placement:'bottom', options: openRuleArr,optionProps: {value: 'dimCde', label: 'dimNme'}}"
                    >
                    <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.openRule!=scope.row.change.openRule?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?transition_openRule(scope.row.change.openRule)||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.openRule!=scope.row.change.openRule?'red':'':'':''">
                          {{transition_openRule(scope.row.openRule)}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                    <vxe-table-column
                      min-width="160px"
                      field="beginDate"
                      title="规则生效日期"
                      :edit-render="{name: '$input', props: {type: 'date'}}"
                    >
                    <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.beginDate!=scope.row.change.beginDate?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.beginDate||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.beginDate!=scope.row.change.beginDate?'red':'':'':''">
                          {{scope.row.beginDate}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                    <vxe-table-column
                      min-width="160px"
                      field="endDate"
                      title="规则失效日期"
                      :edit-render="{name: '$input', props: {type: 'date'}}"
                    >
                    <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.endDate!=scope.row.change.endDate?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.endDate||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.endDate!=scope.row.change.endDate?'red':'':'':''">
                          {{scope.row.endDate}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                  </vxe-table>
                </div>
                
                <!-- <div style="margin-top:30px;">
                  <vxe-table
                    border
                    auto-resize
                    show-overflow
                    keep-source
                    ref="xTableMyOpen"
                    width="auto"
                    height="350"
                    :cell-class-name="cellClassName"
                    :header-cell-class-name="headerCellClassName"
                    :edit-rules="validRulesKf"
                    @edit-actived="editActivedEvent"
                    :data="tableDataOpen"
                    :edit-config="{trigger: 'click', mode: 'cell',showStatus: true}"
                  >
                    <vxe-table-column type="checkbox" width="40"></vxe-table-column>
                    <vxe-table-column type="seq" title="序号" width="60"></vxe-table-column>
                    <vxe-table-column
                      min-width="130px"
                      field="openFrequence"
                      title="开放频率"
                      :edit-render="{}"
                    >
                      
                    <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.openFrequence!=scope.row.change.openFrequence?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?transition_openFrequence(scope.row.change.openFrequence)||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.openFrequence!=scope.row.change.openFrequence?'red':'':'':''">
                          {{transition_openFrequence(scope.row.openFrequence)}} <span v-if="scope.row.openFrequence=='MC'">{{scope.row.customDate}}</span>
                        </span>
                      </el-tooltip>
                    </template>
                    <template slot="edit" slot-scope="{row}">
                      <div class="display_flex" style="display:flex;">
                      <template>
                        <vxe-select 
                          v-model="row.openFrequence" 
                          placeholder="请选择" 
                          transfer 
                          :style="row.openFrequence=='MC'?'width:60%;':''"
                          @change="openFrequenceChange({row})">
                          <vxe-option
                            v-for="item in openFrequenceArr"
                            :key="item.dimCde"
                            :label="item.dimNme"
                            :value="item.dimCde">
                          </vxe-option>
                        </vxe-select>
                      </template>
                      <template v-if="row.openFrequence=='MC'">
                        <el-date-picker
                          v-model="row.customDate"
                          type="month"
                          format="yyyy-MM"
                          value-format="yyyy-MM"
                          placeholder="选择日期"
                          :clearable="false"
                          class="height_34px"
                        >
                        </el-date-picker>
                        
                      </template>
                      </div>
                    </template>
                    </vxe-table-column>
                    <vxe-table-column
                      min-width="130px"
                      field="openRule"
                      title="开放规则"
                      :edit-render="{}"
                    >
                      
                    <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.openRule!=scope.row.change.openRule?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?transition_openRule(scope.row.change.openRule)||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.openRule!=scope.row.change.openRule?'red':'':'':''">
                          {{transition_openRule(scope.row.openRule)}} <span v-if="scope.row.openRule=='DC'">{{scope.row.customDate || scope.row.openDay}}</span>
                        </span>
                      </el-tooltip>
                    </template>
                    <template slot="edit" slot-scope="{row}">
                      <div class="display_flex" style="display:flex;">
                      <template>
                        <vxe-select 
                          v-model="row.openRule" 
                          @change="openRuleChange({row})"
                          placeholder="请选择" 
                          :style="row.openRule=='DC'?'width:80%;':''"
                          transfer>
                          <vxe-option
                            v-for="item in openRuleArr"
                            :key="item.dimCde"
                            :label="item.dimNme"
                            :value="item.dimCde">
                          </vxe-option>
                        </vxe-select>
                      </template>
                      <template v-if="row.openRule=='DC'">
                        <el-date-picker
                          v-if="row.openFrequence=='Y'"
                          v-model="row.customDate"
                          type="date"
                          format="MM-dd"
                          value-format="MM-dd"
                          placeholder="选择日期"
                          :clearable="false"
                          :class="['height_34px',row.customDate?'':'input__inner_red']"
                        >
                        </el-date-picker>
                        <el-date-picker
                          v-if="row.openFrequence=='M'"
                          v-model="row.openDay"
                          type="date"
                          format="dd"
                          value-format="dd"
                          placeholder="选择日期"
                          :clearable="false"
                          :class="['height_34px',row.openDay?'':'input__inner_red']"
                        >
                        </el-date-picker>
                        <el-date-picker
                          v-if="row.openFrequence=='DC'"
                          v-model="row.customDate"
                          type="date"
                          format="yyyy-MM-dd"
                          value-format="yyyy-MM-dd"
                          placeholder="选择日期"
                          :clearable="false"
                          :class="['height_34px',row.customDate?'':'input__inner_red']"
                        >
                        </el-date-picker>
                        
                      </template>
                      </div>
                    </template>
                    </vxe-table-column>
                    <vxe-table-column
                      min-width="160px"
                      field="beginDate"
                      title="规则生效日期"
                      :edit-render="{name: '$input', props: {type: 'date'}}"
                    >
                    <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.beginDate!=scope.row.change.beginDate?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.beginDate||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.beginDate!=scope.row.change.beginDate?'red':'':'':''">
                          {{scope.row.beginDate}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                    <vxe-table-column
                      min-width="160px"
                      field="endDate"
                      title="规则失效日期"
                      :edit-render="{name: '$input', props: {type: 'date'}}"
                    >
                    <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.endDate!=scope.row.change.endDate?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.endDate||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.endDate!=scope.row.change.endDate?'red':'':'':''">
                          {{scope.row.endDate}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                  </vxe-table>
                </div> -->

              </el-col>
            </el-row>
            <el-row style="margin-top:10px">
              <el-col :span="6" :offset="10">
                <el-button
                  v-btn="saveCode"
                  type="primary"
                  :loading="countSubmit_btn"
                  plain
                  @click="myTabNext('9')"
                  style="margin-bottom: 5px; "
                  size="small"
                >保存草稿</el-button>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>
        <el-tab-pane label="基金经理" name="eleven">
          <span slot="label" v-if="PageDataAdd.addType==0&&PageDataAdd.beforeData&&jjjl_i_show">基金经理<i style="color: red" class="el-icon-warning"></i></span>
          <div
            class="product_detail"
          >
            <el-row>
              <el-col :span="23" :offset="1">
                <el-button
                  type="primary"
                  plain
                  @click="insertEvent('fundManager',-1)"
                  style="margin-bottom: 5px; "
                  size="small"
                >
                  <i class="el-icon-circle-plus-outline"></i>新增
                </el-button>
                <el-button
                  type="danger"
                  plain
                  @click="removeEvent('fundManager')"
                  style="margin-bottom: 5px; "
                  size="small"
                >
                  <i class="el-icon-delete"></i>移除
                </el-button>
                <!-- <el-button type="error"  plain  @click="revertEvent" style="margin-bottom: 5px; " size="small">
                    <i class="el-icon-back"></i>还原
                </el-button>-->
                <div style="margin-top:0px;">
                  <vxe-table
                    border
                    show-overflow
                    auto-resize
                    keep-source
                    width="100%"
                    height="350"
                    :cell-class-name="cellClassName"
                    :header-cell-class-name="headerCellClassName"
                    ref="xTableFundManager"
                    :edit-rules="validRulesFundManager"
                    :data="tableDataFundManager"
                    :edit-config="{trigger: 'click', mode: 'cell', showStatus: true}"
                  >
                    <vxe-table-column type="checkbox" width="10%"></vxe-table-column>
                    <vxe-table-column type="seq" title="序号" min-width="10%"></vxe-table-column>
                    <vxe-table-column
                      min-width="20%"
                      field="managerName"
                      title="基金经理"
                      :edit-render="{name: '$select', placement:'bottom', options: managerNameArr,optionProps: {value: 'name', label: 'name'} ,events: {change: managerNameChangeEvent}}"
                    >
                    <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.managerName!=scope.row.change.managerName?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.managerName||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.managerName!=scope.row.change.managerName?'red':'':'':''">
                          {{scope.row.managerName}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                    <vxe-table-column min-width="20%" field="investStrategy" title="投资策略">
                      <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.investStrategy!=scope.row.change.investStrategy?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.investStrategy||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.investStrategy!=scope.row.change.investStrategy?'red':'':'':''">
                          {{scope.row.investStrategy}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                    <vxe-table-column min-width="20%" field="phone" title="联系电话">
                      <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.phone!=scope.row.change.phone?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.phone||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.phone!=scope.row.change.phone?'red':'':'':''">
                          {{scope.row.phone}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                    <vxe-table-column min-width="20%" field="email" title="联系邮箱">
                      <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.email!=scope.row.change.email?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.email||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.email!=scope.row.change.email?'red':'':'':''">
                          {{scope.row.email}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                  </vxe-table>
                </div>
              </el-col>
            </el-row>

            <el-row style="margin-top:10px">
              <el-col :span="6" :offset="10">
                <el-button
                  v-btn="saveCode"
                  type="primary"
                  :loading="countSubmit_btn"
                  plain
                  @click="myTabNext('10')"
                  style="margin-bottom: 5px; "
                  size="small"
                >保存草稿</el-button>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>
        <!-- v-if="PageDataAdd.lxr_show || PageDataAdd.formData.fundContacts.length>0 " -->
        <el-tab-pane label="联系人" name="seven">
          <span slot="label" v-if="PageDataAdd.addType==0&&PageDataAdd.beforeData&&lxr_i_show">联系人<i style="color: red" class="el-icon-warning"></i></span>
          <div
            class="product_detail"
          >
            <el-row>
              <el-col :span="23" :offset="1">
                <el-button
                  type="primary"
                  plain
                  @click="insertEvent('contact',-1)"
                  style="margin-bottom: 5px; "
                  size="small"
                >
                  <i class="el-icon-circle-plus-outline"></i>新增
                </el-button>
                <el-button
                  type="danger"
                  plain
                  @click="removeEvent('contact')"
                  style="margin-bottom: 5px; "
                  size="small"
                >
                  <i class="el-icon-delete"></i>移除
                </el-button>

                <!-- <el-button type="error"  plain  @click="revertEvent" style="margin-bottom: 5px; " size="small">
                    <i class="el-icon-back"></i>还原
                </el-button>-->

                <vxe-table
                  border
                  show-overflow
                  keep-source
                  auto-resize
                  height="350"
                  ref="xTableContact"
                  :cell-class-name="cellClassName"
                  :header-cell-class-name="headerCellClassName"
                  :edit-rules="validRulesContact"
                  :data="tableDataContact"
                  :edit-config="{trigger: 'click', mode: 'cell', showStatus: true}"
                >
                  <vxe-table-column type="checkbox" width="10%"></vxe-table-column>
                  <vxe-table-column type="seq" title="序号" width="60"></vxe-table-column>
                  <vxe-table-column
                    field="contactName"
                    title="联系人名称"
                    :edit-render="{name: 'input', attrs: {type: 'text',maxlength:100}}"
                  >
                    <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.contactName!=scope.row.change.contactName?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.contactName||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.contactName!=scope.row.change.contactName?'red':'':'':''">
                          {{scope.row.contactName}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                  <vxe-table-column
                    field="contactType"
                    title="联系人类型"
                    :edit-render="{name: 'input', attrs: {type: 'text',maxlength:100}}"
                  >
                  <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.contactType!=scope.row.change.contactType?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.contactType||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.contactType!=scope.row.change.contactType?'red':'':'':''">
                          {{scope.row.contactType}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                  <vxe-table-column
                    field="contactPhone"
                    title="联系人电话"
                    :edit-render="{name: 'input', attrs: {type: 'text',maxlength:33}}"
                  >
                  <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.contactPhone!=scope.row.change.contactPhone?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.contactPhone||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.contactPhone!=scope.row.change.contactPhone?'red':'':'':''">
                          {{scope.row.contactPhone}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                  <vxe-table-column
                    field="contactMail"
                    title="联系人邮箱"
                    :edit-render="{name: 'input',  attrs: {type: 'text',maxlength:33}}"
                  >
                  <template slot-scope="scope">
                      <el-tooltip placement="right" :disabled='PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.contactMail!=scope.row.change.contactMail?false:true:true:true'>
                        <div slot="content">
                          <span>修改前:{{PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.change.contactMail||'-':'-':'-'}} </span>
                        </div>
                        <span :class="PageDataAdd.addType==0&&PageDataAdd.beforeData?scope.row.change?scope.row.contactMail!=scope.row.change.contactMail?'red':'':'':''">
                          {{scope.row.contactMail}}
                        </span>
                      </el-tooltip>
                    </template>
                    </vxe-table-column>
                </vxe-table>
              </el-col>
            </el-row>
          </div>
        </el-tab-pane>
      </el-tabs>

      <div v-show="bc_show" style="margin-top:10px">
        <el-row>
          <el-col :span="3" :offset="12">
            <el-button
              v-btn="insertCode"
              type="primary"
              :loading="countSubmit_btn"
              v-show="bc_show"
              @click="save('formInline')"
              style="margin-bottom: 5px;"
            >提交审核</el-button>
          </el-col>
        </el-row>
      </div>
    </el-form>
  </div>
</template>

<script>
import { current } from '@/utils/product-info-db'
import { moneyThousand } from '@/filters/index'
import productDictionary from "@/dataDictionary/product";
import commonFun from "@/filters/new_common";
import commonApi from "@/api/common";
import pageApi from "@/api/product/productSearch";
import Pagination from "@/components/Pagination";
import { judgeData } from "@/utils/product-add-judge";
import { autoScrollTo } from "@/utils/auto-scroll-to";
import $ from "jquery";
import xiugaiData from '@/mixinsModel/xiugaiData'
export default {
  mixins: [xiugaiData],
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
      beforeData:{},
      cacheType:''
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
      })
    }
    const purchasePointValid = (rule, value, callback) => {
      console.log(value)
        let reg = /^[0-9\.]+$/
        if (reg.test(value)) {
          // value = value.toString()
          let temp = value.split('.')
          if (temp.length == 1) {
            if (+temp[0] > 1000000000000000000) callback(new Error('有效值过大'))
            else callback()
          } else if (temp.length == 2)  {
            if (temp[0].length > 15) callback(new Error('有效值过大'))
            if (temp[1].length > 2) callback(new Error('只保留小数后两位'))
            callback()
          } else callback(new Error('输入值无效'))
        } else if (value == '') callback()
        else callback(new Error('请输入有效数字'))
      }
    const assetValueValid = ({ cellValue }) => {
      return new Promise((resolve, reject) => {
        if (cellValue.length  > 18) {
          reject(new Error("数值最大长度为18位"));
        } else {
          resolve();
        }
      })
    }
    const dayRedeemToValidate = ({ cellValue }) => {
      let reg = /^[0-9]+$/
      return new Promise((resolve, reject) => {
        if (reg.test(cellValue)) {
          let number = Number(cellValue)
          if (number > 36500) {
           reject(new Error("输入天数不能大于36500天"));
          } else resolve();
        } else {
          // console.log(cellValue);
          reject(new Error("请输入有效天数"));
        }
      })
    }
    const openDateValid = ((rule, value, callback) => {
       let startDate = this.formInline.setupDate
       let endDate = this.formInline.expireDate
       if (startDate && endDate) {
        if(startDate >= endDate){
          callback(new Error('日期选择错误'))
        } else callback()
       } else callback()
     })
    const managerNameValid = (val)=>{
      // let tableData = this.$refs.xTableFundManager.getTableData().tableData;
      // console.log(tableData);
      // let arr = tableData.map(item=>{
      //   return item.managerCode
      // })
      // let Arr = arr.filter(Boolean)
      // let newArr = Array.from(new Set([...Arr]));
      // console.log('arr',Arr);
      // console.log('newArr',newArr);
      // if(Arr.length!=newArr.length){
      //   return new Error('经理人重复')
      // }
    }
    // 开放频率
    const openFrequenceValid=(value)=>{
      // openRule-规则 openFrequence-频率
      if(value.row.openFrequence){
        if(value.row.openFrequence=='MC'){
          if(value.row.customDate){

          }else{
             return new Error('请选择日期');
          }
        }
      }else{
        return new Error('请选择');
      }
    }
    // 开放规则
    const openRuleValid=(value)=>{
      // openRule-规则 openFrequence-频率
      if(value.row.openRule){
        if(value.row.openRule=='DC' && (value.row.openFrequence=='Y' || value.row.openFrequence=='DC')){
          if(value.row.customDate){

          }else{
             return new Error('请选择日期');
          }
        }
        if(value.row.openRule=='DC' && (value.row.openFrequence=='M')){
          if(value.row.openDay){

          }else{
             return new Error('请选择日期');
          }
        }
      }else{
        return new Error('请选择');
      }
    }
    return {
      fundTypeArr2:[
        { fundType:"GJ", fundTypeDetails:"GJ01", fundTypeName:"公募基金", fundTypeDetailName:"公募基金" },
        { fundType:"ZH", fundTypeDetails:"ZH01", fundTypeName:"资管计划", fundTypeDetailName:"一对一资管计划" },
        { fundType:"ZH", fundTypeDetails:"ZH02", fundTypeName:"资管计划", fundTypeDetailName:"一对多公募基金" },
      ],
      options: [],
      moneyValidateDefalut:/^(0|[1-9]{1}\d{0,15}|[1-9]{1}\d{0,13}\.\d{1}|[1-9]{1}\d{0,12}\.\d{2}|0\.\d{1,2})$/,
		  moneyValidate:/^(0|[1-9]{1}\d{0,15}|[1-9]{1}\d{0,13}\.\d{1}|[1-9]{1}\d{0,12}\.\d{2}|0\.\d{1,2})$/,
      isRewardChange: '',
      isType: '',
      isdraftSaveOrPassSave: false,
      saleTypeDialog: false,
      activeName: "first",
      aa: 9999,
      sexList: [],
      // startDateLimit:{},
      // endDateLimit:{},
      formInline: {
        assetFrequency: '', //估值频率
        expireDate: '', //基金日期
        fundName: "", //产品名称
        fundCode: "", //产品代码
        fundNameEn: "", //英文名称
        managerCode: "", //管理人名称
        trustorCode: "", //托管人名称
        operatorCode: "", //基金服务机构
        fundType: "", //基金类型
        fundTypeDetails:"",
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

      // 修改前下拉框的值
      trustorCode:'',
      fundType:'',
      fundTypeDetails:"", //基金类型-二级
      managerCode:'',
      operatorCode:'',
      investDirect:'',
      riskLevel:'',
      operateType:'',
      isGrade:'',
      fundState:'',
      subscribeConfirmDay:'',
      saleFeePrepare:'',
      callConfirmDay:'',
      applyDeliverDay:'',
      callFloatType:'',
      callRateType:'',
      subscribeDeliverDay:'',
      applyConfirmDay:'',
      saleFeePay:'',
      callDeliverDay:'',
      assetFrequency:'',
      manageFeePrepare:'',
      operateFeePrepare:'',
      trustFeePrepare:'',
      manageFeeAsset:'',
      trustFeeAsset:'',
      operateFeeAsset:'',
      manageFeePay:'',
      trustFeePay:'',
      operateFeePay:'',
      rewardType:'',
      rewardPrepareType:'',
      isFixedPrepare:'',
      rewardPrepareDate:'',
      portionNumber:'',
      // 修改前列表值
      checkfundInvestArea_before:[], //投资风控-投资范围
      tableDataSaller_before:[], //销售方式
      tableDataGrade_before:[], //分级关系
      tableDataOpen_before:[], //开放日
      tableDataFundManager_before:[],  //基金经理
      tableDataRedeem_before:[],
      tableDataReward_before:[],
      


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
	  guZhiist:[],//估值频率
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
      checkfundInvestArea_:[],
      sallerNameArr: [], //渠道名称数组
      openFrequenceArr: [], //开放频率数组
      openRuleArr: [], //开放规则数组
      YopenRuleArr: [], //开放规则数组-每年
      SopenRuleArr: [], //开放规则数组-每半年
      QopenRuleArr: [], //开放规则数组-每季度
      MopenRuleArr: [], //开放规则数组-每月
      MCopenRuleArr: [], //开放规则数组-固定月
      DCopenRuleArr: [
        {dimCde:"DC",dimNme:"固定日"}
      ], //开放规则数组-固定日

      // 渠道名称校验
      validQd: {
        sallerName: [
          { required: true, pattern: "", message: "请选择渠道名称", trigger: "change" },
        ],
        sallerCode: [
          { required: true, pattern: "", message: "", trigger: "change" },
        ],
        sallerType: [
          { required: true, pattern: "", message: "请选择", trigger: "change" },
        ],
        feeRate: [
          { required: true, pattern: "", message: "请输入管理费分成比例", trigger: "change" },
          {
            trigger: "change",
            pattern: /^(\d|[1-9]\d)(\.\d{1,})?$|^(100)+$|^(100)(\.0{1,})$/,
            message: "请输入0-100的数字",
          },
        ],
        beginDate: [
          { required: true, pattern: "", message: "请选择开始日期", trigger: "change" },
        ],
        endDate: [
          { required: true, pattern: "", message: "请选择结束日期", trigger: "change" },
        ],
      },
      // 开放日
      validRulesKf: {
        openFrequence: [
          { required: true, pattern: "", validator: openFrequenceValid, message: "请选择", trigger: "change" },
        ],
        openRule: [
          { required: true, pattern: "", validator: openRuleValid, message: "请选择", trigger: "change" },
        ],
        beginDate: [
          { required: true, pattern: "", message: "请选择", trigger: "change" },
        ],
        endDate: [
          { required: true, pattern: "", message: "请选择", trigger: "change" },
        ],
        // customDate: [
        //   { required: true, pattern: "", message: "请选择", trigger: "change" },
        // ]
      },
      // 表单校验规则
      commonRules: {
        //必填信息校验
        fundName: [
          {
            required: true,
            // pattern: /^[a-zA-Za-z0-9\u4e00-\u9fa5]+$/,
            message: "请输入产品名称",
            trigger: "change",
          },
        ],
        fundCode: [
          {
            required: true,
            trigger: "change",
            pattern: /^[A-Z0-9]+$/,
            message: "请输入大写字母、数字",
          },
        ],
        fundNameEn: [
           {
            required: false,
            pattern: /^[a-zA-Za-z0-9]+$/,
            message: "请输入英文,数字",
            trigger: "change",
          }
        ],
        // fundType: [
        //   { required: true, message: "请选择基金类型", trigger: "change" },
        // ],
        fundTypeDetails: [
          { required: true, message: "请选择基金类型", trigger: "change" },
        ],
        investDirect: [
          { required: true, message: "请选择投资方向", trigger: "change" },
        ],
        holdYear: [
          {
            required: false,
            trigger: "change",
            // pattern: /^([1-9]\d?|100)$/,
            pattern: /^(0|[1-9]{1}\d{0,17}|[1-9]{1}\d{0,15}\.\d{1}|[1-9]{1}\d{0,14}\.\d{2}|0\.\d{1,2})$/,
            message: "请输入数值且最多包含2位小数",
          },
        ],
        riskLevel: [
          { required: true, message: "请选择风险等级", trigger: "change" },
        ],
        fundState: [
          { required: true, message: "请选择产品状态", trigger: "change" },
        ],
        isGrade: [
          { required: true, message: "请选择是否分类", trigger: "change" },
        ],
        purchasePoint: [
          {
            required: true,
            message: "请输入认申购起点（不含费）元",
            trigger: "change",
            type: 'string',
          },
          {
            trigger: "change",
            type: 'string',
            // pattern: /^(0|[1-9]{1}\d{0,17}|[1-9]{1}\d{0,15}\.\d{1}|[1-9]{1}\d{0,14}\.\d{2}|0\.\d{1,2})$/,
            pattern: '',
            message: "请输入数值且最多包含2位小数"
            // validator: purchasePointValid
          },
        ],
        purchaseDiffAppend: [
          {
            required: true,
            message: "请输入追加认申购级差",
            trigger: "change",
          },
          {
            pattern: /^(-|\+)?\d+(\.\d+)?$/,
            message: "请输入数字",
          }
        ],
        subscribeRate: [
          { required: true, message: "请输入0-100的数字", trigger: "change", pattern: /^(\d|[1-9]\d)(\.\d{1,})?$|^(100)+$|^(100)(\.0{1,})$/, },
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

        //选填信息校验
        //基础信息
        operateDept: [
          {
            required: false,
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message: this.$regularValidator.empty().msg,
          },
        ],

        recordCode: [
          {
            required: false,
            trigger: "change",
            pattern: /^[A-Za-z0-9]+$/,
            message: "请输入字母或者数字",
          },
        ],

        //费用信息
        manageAccountName: [
          {
            required: false,
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message: this.$regularValidator.empty().msg,
          },
        ],
        manageAccount: [
          {
            required: false,
            trigger: "change",
            pattern: /^[a-zA-Za-z0-9]+$/,
            message: "请输入字母、数字",
          },
        ],
        manageBankName: [
          {
            required: false,
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message: this.$regularValidator.empty().msg,
          },
        ],

        //成立，到期时间
        setupDate:[{ required: false, message: '', validator: openDateValid, trigger: 'change'}],
        expireDate:[{required: false, message: '', validator: openDateValid, trigger: 'change'}],
        //收益分配
        // incomePortionDesc: [
        //   {
        //     required: false,
        //     trigger: "change",
        //     pattern: /^[a-zA-Za-z0-9\u4e00-\u9fa5]+$/,
        //     message: "请输入中文、字母、数字",
        //   },
        // ],
        //投资风控
        // investLimit: [
        //   {
        //     required: false,
        //     trigger: "change",
        //     pattern: /^[a-zA-Za-z0-9\u4e00-\u9fa5]+$/,
        //     message: "请输入中文、字母、数字",
        //   },
        // ],
        warnPoint: [
          {
            required: false,
            trigger: "change",
            pattern: /^(?:0\.\d+|[01](?:\.0)?)$/,
            message: "请输入0-1的数字",
          },
        ],
        lossPoint: [
          {
            required: false,
            trigger: "change",
            pattern: /^(?:0\.\d+|[01](?:\.0)?)$/,
            message: "请输入0-1的数字",
          },
        ],
        applyRate: [
          {
            required: false,
            trigger: "change",
            pattern: /^(\d|[1-9]\d)(\.\d{1,})?$|^(100)+$|^(100)(\.0{1,})$/,
            message: "请输入0-100的数字",
          },
        ],
        manageRate: [
          {
            required: false,
            trigger: "change",
            pattern: /^(\d|[1-9]\d)(\.\d{1,})?$|^(100)+$|^(100)(\.0{1,})$/,
            message: "请输入0-100的数字",
          },
        ],
        operateRate: [
          {
            required: false,
            trigger: "change",
            pattern: /^(\d|[1-9]\d)(\.\d{1,})?$|^(100)+$|^(100)(\.0{1,})$/,
            message: "请输入0-100的数字",
          },
        ],
        trustRate: [
          {
            required: false,
            trigger: "change",
            pattern: /^(\d|[1-9]\d)(\.\d{1,})?$|^(100)+$|^(100)(\.0{1,})$/,
            message: "请输入0-100的数字",
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
        message: "请输入0-100的数字",
        trigger: "change",
        pattern: /^(\d|[1-9]\d)(\.\d{1,})?$|^(100)+$|^(100)(\.0{1,})$/,
      },

      //联系人校验规则
      validRulesContact: {
        contactName: [
          { required: true, message: "请填写联系人名称" },
          {
            pattern: this.$regularValidator.empty().reg,
            message: this.$regularValidator.empty().msg,
          },
        ],
        contactType: [
          { required: true, message: "请填写联系人类型" },
          {
            pattern: this.$regularValidator.empty().reg,
            message: this.$regularValidator.empty().msg,
          },
        ],
        contactPhone: [
          {required: true, message: "请输入联系人电话" },
          { pattern: /^1(3|4|5|6|7|8|9)\d{9}$|^0\d{2,3}-\d{7,8}$/, message: "格式不正确" }
        ],
        contactMail: [
          {required: true, message: "请输入联系邮箱" },
          {pattern: /^\w+@[a-z0-9]+\.[a-z]{2,4}$/, message: "格式不正确" }
        ],
      },
      checkAll: false,
      isIndeterminate: true,
      fundManager_show: true,
      fundManagerIf_show: false,
      tableDataFundManager: [],
      validRulesFundManager: {
        managerName: [
          // { required: false, message: "" ,validator:managerNameValid ,trigger:'change'},
          { required: true, message: "请选择基金经理" }
          ],
        // phone: [{required: false, pattern: /^1(3|4|5|6|7|8|9)\d{9}$/, message: "格式不正确" }],
        // email: [
        //   {required: false, pattern: /^\w+@[a-z0-9]+\.[a-z]{2,4}$/, message: "格式不正确" },
        // ],
      },
      managerNameArr: [], //基金经理数据
      isSave: false, //判断是否点击保存
      validRewardRules: {
        rewardFrom: [
          { required: true, message: "请填写区间起点" },
          {
            pattern: /^(\d{0,10}|[1-9]\d{0,10})(\.\d{1,2})?$|^(1000000000000)+$|^(1000000000000.0)+$|^(1000000000000.00)+$/,
            message: "请输入小于亿位两位小数",
          },
        ],
        rewardTo: [
          { required: true, message: "请填写区间终点" },
          {
            pattern: /^(\d{0,10}|[1-9]\d{0,10})(\.\d{1,2})?$|^(1000000000000)+$|^(1000000000000.0)+$|^(1000000000000.00)+$/,
            message: "请输入小于亿位两位小数",
          },
        ],
        rewardRate: [
          { required: true, message: "请填写计提比例" },
          { pattern: /^(\d|[1-9]\d)(\.\d{1,})?$|^(100)+$|^(100)(\.0{1,})$/, message: "请输入0-100的数字" },
        ],
      },
      //分级校验规则
      validGradeRules: {
        fundNameGrade: [
          { required: true, message: "请输入分类名称", pattern: "" },
        ],
        // fundCodeGrade: [
        //   { required: true, message: "分级代码" },
        //   { pattern: /^[a-zA-Z0-9]+$/, message: "请输入数子，字母" },
        // ],
        shareType: [{ required: true, message: "请选择基分金类级别", pattern: "" }],
        // leverageRatio: [
        //   { required: true, message: "请填写杠杆比例" },
        //   { pattern: /^(\d|[1-9]\d)(\.\d{1,2})?$|^(100)+$|^(100.0)+$|^(100.00)+$/, message: "请输入0-100两位小数" },
        // ],
        fundCodeGrade: [
          { required: true, message: "请输入分类代码" },
          {
            trigger: 'change',
            pattern:  /^[a-zA-Z0-9]+$/,
            message: "请输入数字，字母"
          }
        ],
        assetValue: [
          {
            required: true,
            message: "请输入初始单位净值"
          },
          {
            // pattern: /^(0|[1-9]{1}\d{0,17}|[1-9]{1}\d{0,15}\.\d{1}|[1-9]{1}\d{0,14}\.\d{2}|0\.\d{1,2})$/,
            // pattern: /^[0-9]+$/,
            validator: assetValueValid
          }
        ]
      },
      mdFlagOpen: false,  //用于强制刷新table
      // 赎回税率的检验
      rulesRedeem: {},
      // 赎回税率的检验---金额
      redeemFrom: {
          redeemFrom: [
          { required: true, message: "请填写区间起点" },
          {
            pattern: /^(\d{0,10}|[1-9]\d{0,10})(\.\d{1,2})?$|^(1000000000000)+$|^(1000000000000.0)+$|^(1000000000000.00)+$/,
            message: "请输入小于亿位两位小数",
          },
         ],
         redeemTo: [
          { required: true, message: "请填写区间终点" },
          {
            pattern: /^(\d{0,10}|[1-9]\d{0,10})(\.\d{1,2})?$|^(1000000000000)+$|^(1000000000000.0)+$|^(1000000000000.00)+$/,
            message: "请输入小于亿位两位小数",
          },
        ],
        redeemRate: [
          { required: true, message: "请填写费率" },
          {
            pattern: /^(\d|[1-9]\d)(\.\d{1,})?$|^(100)+$|^(100)(\.0{1,})$/,
            message: "请输入0-100的数字",
          },
        ]
      },
      // 赎回税率的检验----天数 /^[0-9]$|^[1-9][0-9]$|^[1-3][0-6][0-6]$/
      dayRulesReddm: {
          redeemFrom: [
          { required: true, message: "请填写区间起点" },
          {
            validator: dayRedeemToValidate,
            message: "",
          },
         ],
         redeemTo: [
          { required: true, message: "请填写区间终点" },
          {
            validator: dayRedeemToValidate,
            message: "",
          },
        ],
        redeemRate: [
          { required: true, message: "请填写费率" },
          {
            // pattern: /^((0){1}(\.\d{0,2})?|1|1.0|1.00)$/,
            pattern: /^(\d|[1-9]\d)(\.\d{1,})?$|^(100)+$|^(100)(\.0{1,})$/,
            message: "请输入0-100的数字",
          },
        ]
      },
      countSubmit_btn: false,

      recordCodeVolid: false,
      holdYearVolid: false,
      fundCodeVolid: false,
      warnPointVolid: false,
      lossPointVolid: false,
      saveCode: "",
      insertCode: "",
      defaluteTableDataRedeem: [],
      defaultTableDataReward: []
    };
  },
  //页面加载后触发
  mounted() {
    this.getOptions()
    // console.log('this.PageDataAdd.beforeData',this.PageDataAdd.beforeData,Boolean(this.PageDataAdd.beforeData));
    // console.log(this.jcxx_i_show);

    // console.log('mounted',this.PageDataAdd.beforeData.fundInfo);
    //初始化数据
    this.isType = this.PageDataAdd.addType
    this.initData();
    this.getEdims(); //获取数据字典

    this.isdraftSaveOrPassSave = false
    let type = this.PageDataAdd.addType;
    if (type === -1) {
      this.saveCode = "fund.insert.save";
      this.insertCode = "fund.insert.approve";
    } else if (type === 0) {
      this.saveCode = "fund.update.save";
      this.insertCode = "fund.update.approve";
    } else if (type === 1) {
      this.saveCode = "fund.copy.save";
      this.insertCode = "fund.copy.approve";
    }

    if (type != -1) {
      this.getDetail();
      this.getModificationData(this.PageDataAdd.formData)
    }
  
  },
  methods: {
    cellClassName ({ row, rowIndex, column, columnIndex }) {
      return 'vxe-cell-class-name'
    },
    headerCellClassName ({ column, columnIndex }) {
      return 'vxe-header-cell-class-name'
    },
    clearableDate() {
      // console.log('change');
      this.$refs.formInline.clearValidate('setupDate')
      this.$refs.formInline.clearValidate('expireDate')
     },
    moneyFocus () {
      console.log('focus');
        this.commonRules.purchasePoint[1].pattern = this.moneyValidateDefalut
        if (this.formInline.purchasePoint && this.formInline.purchasePoint.includes(',')) {
          this.formInline.purchasePoint = this.formInline.purchasePoint.toString().replace(/,/gi, '')
        }
      },
      moneyBlur () {
        console.log('blur');
        this.commonRules.purchasePoint[1].pattern = this.moneyValidateDefalut
        let reg = this.moneyValidate.test(this.formInline.purchasePoint)
          this.formInline.purchasePoint = moneyThousand(this.formInline.purchasePoint)
        if (reg && this.formInline.purchasePoint) {  //失去焦点正则为true
          this.commonRules.purchasePoint[1].pattern = ''
          // this.$refs.formInline.validate()
        }
      },
    changeDate () {
      
    },
    getModificationData (data) {
      let dataInfo = data.fundInfo
      Promise.all([this.callFloatTypeChange(dataInfo.callFloatType), this.callDeliverDaySelect(dataInfo.callRateType)]).then(() => {
       if (data.fundRedeems) {
         this.tableDataRedeem = data.fundRedeems; //赎回费率列表数据
        //  this.defaluteTableDataRedeem = data.fundRedeems; //赎回费率列表数据
        if(this.PageDataAdd.beforeData){
          this.tableDataRedeem_before=this.PageDataAdd.beforeData.fundRedeems
          this.tableDataRedeem=current(this.tableDataRedeem,this.tableDataRedeem_before)
          this.jyxx_i_show2=this.judgeChangeJYXX(this.tableDataRedeem);
          console.log(this.jyxx_i_show2,'this.jyxx_i_show2');
        }
        }
      })
    },
    callDeliverDaySelect (data) {
      // console.log('2459',data);
      this.mdFlagOpen = true
      this.rulesRedeem = {}
      if (data == 'M') {
        this.rulesRedeem = this.redeemFrom
      } else if (data == 'D') {
        // console.log('ddd');
        this.rulesRedeem = this.dayRulesReddm
      } else {
        this.mdFlagOpen = false
      }
      this.isClearRedeemForm(data)
    },
    RedeemVisibleChange (data) {
      this.isRewardChange = ''
      if (data) this.isRewardChange = JSON.parse(JSON.stringify(this.formInline.callRateType))
    },
    isClearRedeemForm (data) {
      let lj = this.$refs.xTableRedeem || false
      let tableList = lj ? lj.getTableData().tableData : []
      if (!tableList.length) return
      this.formInline.callRateType = this.isRewardChange
      this.$confirm('此操作会重置数据， 是否继续 ？', "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
          confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
        }).then( ()=> {
          this.formInline.callRateType = data
          this.tableDataRedeem = []
          this.isRewardChange = ''
      }).catch( () => {
        this.$message.info('已取消 ！')
        console.log('取消时',data);
        if (data == 'M') {
          this.rulesRedeem = this.dayRulesReddm
        } else if (data == 'D') {
          this.rulesRedeem = this.redeemFrom
        }
      })
    },
    dateChangeFrom (column, event) {
      // console.log(column)
      this.$message.closeAll()
      let toName = ''
      let fromName = column.column.property  //from的字段
      let mdFlagData = column.visibleData //得到所有table列表
      let row = mdFlagData[column.seq-1]  //得到当前输入的行 redeemTo
      if (fromName == 'rewardFrom') toName = 'rewardTo'
      else toName = 'redeemTo'
      let currentVal = event.value
      if (currentVal == '') return
      if (column.seq === 1) {
        if (row[toName] != null && row[toName] != '') {
          if ((+currentVal) >= (+row[toName])) return this.$message.error('区间起点的值不能大于/等于区间终点值 ！请重新输入')
        }
      }
      if (column.seq > 1) {
        if (mdFlagData[column.seq-2][toName] != null && mdFlagData[column.seq-2][toName] != '') {
          if ((+currentVal) < +(mdFlagData[column.seq-2][toName])) return this.$message.error('区间起点的值不能小于上一行的区间终点值 ！请重新输入')
        }
      }
    },
    dateChangeTo (column, event) {
      this.$message.closeAll()
      let fromName = ''
      let toName = column.column.property  //to的字段
      let mdFlagData = column.visibleData //得到所有table列表
      let row = mdFlagData[column.seq-1]  //得到当前输入的行
      let currentVal = event.value
      if (toName == 'redeemTo') fromName = 'redeemFrom'
      else fromName = 'rewardFrom'
      if (currentVal == '') return
      if (column.seq === 1) {
        if (row[fromName] != null && row[fromName] != '') {
          if ((+currentVal) <= (+row[fromName])) return this.$message.error('区间终点的值不能小于区间起点值 ！请重新输入')
        }
      }
      if (column.seq > 1) {
        if (mdFlagData[column.seq-2][fromName] != null && mdFlagData[column.seq-2][fromName] != '') {
          if ((+currentVal) <= +(mdFlagData[column.seq-1][fromName])) return this.$message.error('区间终点的值不能小于等于区间起点值 ！请重新输入')
        }
      }
    },
    // 获取Selects
    getSelects(val, arr) {
      const params = val;
      pageApi
        .getTransferType(params)
        .then((res) => {
          const self = this;
          if (res.data.message === "success") {
            arr = res.data.data;
          } else {
            this.$message.closeAll();
            this.$message.error("初始化数据失败");
          }
        })
        .catch(() => {
          this.$message.closeAll();
          this.$message.error("初始化数据失败");
        });
    },

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

    nextTab(val) {
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
      if (tabLabel === "基础信息") {
        this.activeName = 'first'
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
        this.activeName = 'second'
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
        if (this.mdFlagOpen) {
          this.$nextTick(() => {
            this.$refs.xTableRedeem.recalculate(true)
          })
        }
      } else if (tabLabel === "费用信息") {
        this.activeName = 'third'
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
        if (this.rewardType_show) {
          this.$nextTick(() => {
            this.$refs.xTableReward.recalculate(true)
          })
        }
      } else if (tabLabel === "收益分配") {
        this.activeName = 'fourth'
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
        // this.activeName = 'fourth'
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
        this.activeName = 'six'
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
        this.getEleHeight()
      } else if (tabLabel === "分级关系") {
        this.activeName = 'eight'
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
      } else if (tabLabel === "销售方式") {
        this.activeName = 'nine'
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
      } else if (tabLabel === "开放日") {
        this.activeName = 'ten'
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
        this.activeName = 'eleven'
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
        this.fundManagerIf_show = true; //基金经理
        this.PageDataAdd.fundManager_show = true;
      } else if (tabLabel === "联系人") {
        this.activeName = 'seven'
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
        this.fundManagerIf_show = false; //基金经理
        this.PageDataAdd.lxr_show = true;
      }
    },
    getEleHeight () {
      // getBoundingClientRect()
       let targetbox= document.getElementById('targetbox');
      this.$nextTick(() => {
        let elHeight = this.$refs['jump'].getBoundingClientRect().top
        let sh = autoScrollTo(elHeight)
        // console.log(sh)
        // this.$refs['jump'].scrollTo(0, sh)
        // document.documentElement.scrollTop = sh
        // console.log(targetbox.scrollHeight)
        // targetbox.scrollTop = sh
        // document.body.parentNode.scrollTop = sh
        // document.body.scrollTop = sh
      })
    },
    activeCellMethod({ column, columnIndex }) {
      if (columnIndex === 4 || columnIndex === 3) {
        return false;
      }
      return true;
    },
    activeCellMethodGrade({ column, columnIndex }) {
      // if (columnIndex === 3) {
      //   return false;
      // }
      return true;
    },
    async insertEventRedReem (type, row) {
      this.$message.closeAll()
        if (this.formInline.callRateType) {
            const errMapRedeem = await this.$refs.xTableRedeem.validate(true).catch(errMap => errMap)
            if (errMapRedeem) {
              this.$message.error("请完善信息再新增 ！")
            } else {
              const record = {}
              let { row: newRow } = this.$refs.xTableRedeem.insertAt(record, row);
              this.$refs.xTableRedeem.setActiveCell(newRow);
            }
        } else this.$message.error("请先选择赎回费率类型 ！")

    },
    async insertEvent(type, row) {
      const record = {};

      if (type === "grade") {
        let { row: newRow } = this.$refs.xTableGrade.insertAt(record, row);
        this.$refs.xTableGrade.setActiveCell(newRow);
      }
      // else if (type === "redeem") {
      //   if (this.formInline.callRateType) {
      //     this.$message.closeAll();
      //       const errMapRedeem = await this.$refs.xTableRedeem.validate(true).catch(errMap => errMap)
      //       if (errMapRedeem) {
      //         this.$message.error("请完善信息再新增 ！");
      //       } else {
      //         let { row: newRow } = this.$refs.xTableRedeem.insertAt(record, row);
      //         this.$refs.xTableRedeem.setActiveCell(newRow);
      //       }
      //   } else {
      //     this.$message.closeAll();
      //     this.$message({
      //       message: "请先选择赎回费率类型",
      //       type: "error",
      //     });
      //     return;
      //   }
      // }
      else if (type === "reward") {
          this.$message.closeAll();
          const errMapReward = await this.$refs.xTableReward.validate(true).catch(errMap => errMap)
          if (errMapReward) {
              this.$message.error("请完善信息再新增 ！");
            } else {
              let { row: newRow } = this.$refs.xTableReward.insertAt(record, row);
              this.$refs.xTableReward.setActiveCell(newRow);
            }
      } else if (type === "contact") {
        let { row: newRow } = this.$refs.xTableContact.insertAt(record, row);
        this.$refs.xTableContact.setActiveCell(newRow);
      } else if (type === "saller") {
        if (!this.formInline.saleType) {
          this.$message.closeAll();
          this.$message({
            message: "请先选择销售方式",
            type: "error",
          });
          return;
        }
        if (this.sallerNameArr.length == 0) {
          this.$message.closeAll();
          this.$message({
            message: "该销售方式下没有对应的渠道数据",
            type: "error",
          });
          return;
        }
        let { row: newRow } = this.$refs.xTableMySaller.insertAt(record, row);
        this.$refs.xTableMySaller.setActiveCell(newRow);
      } else if (type === "open") {
        let aaa= { customDate:"", openDay:"" }
        let { row: newRow } = this.$refs.xTableMyOpen.insertAt(aaa, row);
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
          confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
        })
          .then(() => {
            if (type === "grade") {
              this.$refs.xTableGrade.removeCheckboxRow();
              this.tableDataGrade = this.$refs.xTableGrade.getTableData().tableData;
            }
            if (type === "redeem") {
              this.$refs.xTableRedeem.removeCheckboxRow();
              this.tableDataRedeem = this.$refs.xTableRedeem.getTableData().tableData;
            }
            if (type === "reward") {
              this.$refs.xTableReward.removeCheckboxRow();
              this.tableDataReward = this.$refs.xTableReward.getTableData().tableData;
            }
            if (type === "contact") {
              this.$refs.xTableContact.removeCheckboxRow();
              this.tableDataContact = this.$refs.xTableContact.getTableData().tableData;
            }
            if (type === "saller") {
              this.$refs.xTableMySaller.removeCheckboxRow();
              this.tableDataSaller = this.$refs.xTableMySaller.getTableData().tableData;
            }

            if (type === "open") {
              this.$refs.xTableMyOpen.removeCheckboxRow();
              this.tableDataOpen = this.$refs.xTableMyOpen.getTableData().tableData;
            }

            if (type === "fundManager") {
              this.$refs.xTableFundManager.removeCheckboxRow();
              this.tableDataFundManager = this.$refs.xTableFundManager.getTableData().tableData;
            }
          })
          .catch(() => {
            this.$message.closeAll();
            this.$message({
              type: "info",
              message: "已取消",
            });
          });
      } else {
        this.$message.closeAll();
        this.$message({ type: "error", message: "请至少选择一条数据" });
      }
    },
    initData() {
      this.operateTypeArr = productDictionary.operateType;
      // console.log('operateType',this.PageDataAdd.beforeData.fundInfo);
      if(this.PageDataAdd.beforeData){
        if(this.PageDataAdd.beforeData.fundInfo.operateType){
          let operateTypeobj = this.operateTypeArr.find((item,index,arr)=>{
            return item.dimCde == this.PageDataAdd.beforeData.fundInfo.operateType
          })
          this.operateType=operateTypeobj.dimNme;
        }
      }

      this.isGradeArr = productDictionary.isGrade;
      if(this.PageDataAdd.beforeData){
        if(this.PageDataAdd.beforeData.fundInfo.isGrade){
          let isGradeobj = this.isGradeArr.find((item,index,arr)=>{
            return item.dimCde == this.PageDataAdd.beforeData.fundInfo.isGrade
          })
          this.isGrade=isGradeobj.dimNme;
        }
      }

      //产品状态
      this.getEdimsGet("fundinfo_fundState");
      this.isOpenShortArr = productDictionary.isOpenShort;

      this.saleFeePrepareArr = productDictionary.saleFeePrepare;
      if(this.PageDataAdd.beforeData){
        if(this.PageDataAdd.beforeData.fundInfo.saleFeePrepare){
          let saleFeePrepareobj = this.saleFeePrepareArr.find((item,index,arr)=>{
            return item.dimCde == this.PageDataAdd.beforeData.fundInfo.saleFeePrepare
          })
          this.saleFeePrepare=saleFeePrepareobj.dimNme;
        }
      }

      this.saleFeePayArr = productDictionary.saleFeePay;
      if(this.PageDataAdd.beforeData){
        if(this.PageDataAdd.beforeData.fundInfo.saleFeePay){
          let saleFeePayobj = this.saleFeePayArr.find((item,index,arr)=>{
            return item.dimCde == this.PageDataAdd.beforeData.fundInfo.saleFeePay
          })
          this.saleFeePay=saleFeePayobj.dimNme;
        }
      }

      this.shareTypeArr = productDictionary.shareType;

      this.callFloatTypeArr = productDictionary.callFloatType;
      if(this.PageDataAdd.beforeData){
        if(this.PageDataAdd.beforeData.fundInfo.callFloatType){
          let callFloatTypeobj = this.callFloatTypeArr.find((item,index,arr)=>{
            return item.dimCde == this.PageDataAdd.beforeData.fundInfo.callFloatType
          })
          this.callFloatType=callFloatTypeobj.dimNme;
        }
      }

      this.isFixedPrepareArr = productDictionary.isFixedPrepare;
      if(this.PageDataAdd.beforeData){
        if(this.PageDataAdd.beforeData.fundInfo.isFixedPrepare){
          let isFixedPrepareobj = this.isFixedPrepareArr.find((item,index,arr)=>{
            return item.dimCde == this.PageDataAdd.beforeData.fundInfo.isFixedPrepare
          })
          this.isFixedPrepare=isFixedPrepareobj.dimNme;
        }
      }
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
      this.rulesRedeem = {} //清空from和同的校验功能
      if (value == "0") {
        this.callFloat_input_show = true;
        this.callFloat_select_show = false;
        this.mdFlagOpen = false
        this.formInline.callRateType = "";
        this.tableDataRedeem = []
      } else if (value == "1"){
        this.callFloat_input_show = false;
        this.callFloat_select_show = true;
        this.formInline.callRate = "";
      } else {
        this.callFloat_input_show = false;
        this.callFloat_select_show = false;
        this.mdFlagOpen = false
        this.tableDataRedeem = []
        this.formInline.callRateType = ''
        this.formInline.callRate = "";
      }
      // if (value != '1') this.isClearRedeemForm()
      this.$nextTick(() => {
        this.$refs.formInline.clearValidate()
      })
    },
    //业绩报酬选择事件
    rewardTypeChange(value) {
      this.isClear(value)  //下拉切换是是否清空重置-----
    },
    visibleChange (data) {
      if (data) this.isRewardChange = JSON.parse(JSON.stringify(this.formInline.rewardType))
    },
    isClear (data) {
      let obj = new Object
      let isDelect = false
      obj['rewardPrepareType'] = this.formInline.rewardPrepareType || ''
      obj['isFixedPrepare'] = this.formInline.isFixedPrepare || ''
      obj['rewardPrepareDate'] = this.formInline.rewardPrepareDate || ''
      for (let i in obj) {
        if (obj[i] !== '') {
          isDelect = true
          break
        }
      }
      if (isDelect) {
         this.formInline.rewardType = this.isRewardChange
          this.$confirm('此操作会重置数据， 是否继续 ？', "提示", {
             confirmButtonText: "确定",
             cancelButtonText: "取消",
             type: "warning",
             confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
           }).then( ()=> {
             this.formInline.rewardType = data
             this.rewardTypeClear(data)
          }).catch( () => {
            this.$message.info('已取消 ！')
          })
      } else {
        this.rewardTypeClear(data)
      }
    },
    rewardTypeClear (data) {
        if (data === "WHOLE" || data === "SINGLE") this.rewardType_show = true;
        else this.rewardType_show = false
        this.tableDataReward = []
        this.formInline.rewardPrepareType = "";
        this.formInline.isFixedPrepare = "";
        this.formInline.rewardPrepareDate = "";
    },
    btnClear () {
      this.rewardTypeClear('clearInput')
    },
    isFixedPrepareChange(value) {
      if (value == "1") {
        this.rewardPrepareDate_show = true;
      } else {
        this.rewardPrepareDate_show = false;
        this.formInline.rewardPrepareDate = "";
      }
    },
    saleTypeChange(value) {
      let params = {};
      this.saleTypeDialog = true
      params.sallerType = value;
      if (value === "S+A") {
        params.sallerType = "";
      }
      pageApi
        .getSallerData(params)
        .then((response) => {
          if (response.data.status === 200) {
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
              message: response.data.message || "查询失败",
              type: "error",
            });
            this.sallerNameArr = [];
          }
          this.saleTypeDialog = false
        })
        .catch(() => {
          this.$message.closeAll();
          this.$message({
            message: "查询失败",
            type: "error",
          });
          this.sallerNameArr = [];
          this.this.saleTypeDialog = false
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
      // let row = val.row;
      // let name = row.fundNameGrade;
      // if (name) {
      //   let arr = this.fundNameGradeArr;
      //   for (let i = 0; i < arr.length; i++) {
      //     if (name === arr[i].fundName) {
      //       row.fundCodeGrade = arr[i].fundCode;
      //       return;
      //     }
      //   }
      // } else {
      //   row.fundCodeGrade = "";
      // }
    },
    leverageRatioChangeEvent(val) {
      let row = val.row;
      let name = row.leverageRatio;
      if (name) {
        let reg = new RegExp("/^(1|0(.d{1,2})?)$/");
        if (!reg.test(name)) {
          this.$message.closeAll();
          this.$message({
            message: "请输正确的杠杆比例",
            type: "error",
          });
          row.leverageRatio = "";
        }
      } else {
        row.leverageRatio = "";
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
      // 重复选择校验
      {
        let tableData = this.$refs.xTableFundManager.getTableData().tableData;
        // console.log('tableData',tableData);
        let arr = tableData.map(item=>{
          return item.managerCode
        })
        // console.log('arr',arr);
        let Arr = arr.filter(Boolean)
        let newArr = Array.from(new Set([...Arr]));
        // console.log('Arr',Arr);
        // console.log('newArr',newArr);
        if(Arr.length!=newArr.length){
          row.managerName = null;
          row.managerCode = null;
          row.investStrategy = null;
          row.phone = null;
          row.email = null;
          this.$message({
              message: '已选择此基金经理，不需重复选择！',
              type: "error",
            });
        }
      }
    },
    saveVolidFundCode() {
      let fundCode = this.formInline.fundCode;
      let params = {};

      params.fundCode = fundCode;
      pageApi
        .volidFundCode(params)
        .then((response) => {
          if (response.data.status === 200) {
            this.saveCg();
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
            message: response.data.message || "校验失败",
            type: "error",
          });
          this.isSave = false;
          return true;
        });
    },
    // 重置vxetable的数据
    vxeTableListDataResh () {
      this.$nextTick(() => {
        if (!this.tableDataRedeem.length) {
          this.tableDataRedeem = this.defaluteTableDataRedeem
        } else {}
        if (!this.tableDataReward.length) {
          this.tableDataReward = this.defaultTableDataReward
        } else {}
      })
    },
    myTabNext() {
      this.$message.closeAll()
      this.countSubmit_btn = true;
      this.isdraftSaveOrPassSave = false
      this.$refs["formInline"].validate((valid, obj) => {
        if (valid) {
          this.xTableRedeemJudge()  //分级管理校验
        } else {
          this.assignJudge(obj)
        }
      })
    },
    // 保存草稿提示是否要提交保存
    isPassSave () {
      this.$confirm("保存草稿成功，是否提交审核？", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "success",
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      }).then(() => {
        this.submitSave()
      }).catch(() => {
        // this.$message({
        //   type: "info",
        //   message: "已取消提交审核",
        // })
        this.countSubmit_btn = false
        this.isdraftSaveOrPassSave = false
        this.$emit('close')
      })
    },
    jumpInverList () {},
    assignJudge (obj) {
      let arr =  new Array
      for (let i in obj) {
        arr.push(i)
      }
      // console.log(arr)
      this.countSubmit_btn = false
      if (judgeData(arr).base == 1) this.handleClick({ label: '基础信息' })
      else if (judgeData(arr).base == 2) this.handleClick({ label: '交易信息' })
      else if (judgeData(arr).base == 3) this.handleClick({ label: '费用信息' })
      else if (judgeData(arr).base == 4) this.handleClick({ label: '收益分配' })
      else if (judgeData(arr).base == 5) {
        this.handleClick({ label: '投资风控' })
        this.$nextTick(() => {
           if (judgeData(arr).code) this.$refs[judgeData(arr).code].focus()
         })
      }
      else console.log('未知')
      this.$message({
        message: judgeData(arr).msg,
        type: "error",
      })
    },
    // 交易信息的from和to
   async xTableRedeemJudge() {
      if (this.callFloat_select_show) {
        var redeemData = this.$refs.xTableRedeem.getTableData().tableData
        if (redeemData.length == 0) {
          this.$message.error('交易信息 费率浮动范围不能为空 ！')
          this.countSubmit_btn = false
          this.handleClick({ label: '交易信息' })
          return
        }
      } else return this.xTableRewardJudge()
      if (!this.mdFlagOpen) return this.xTableRewardJudge()
      let errMsg = await this.$refs["xTableRedeem"].validate().catch(errMap => errMap)
      if (errMsg) {
        // console.log(errMsg)
        this.countSubmit_btn = false
        let temp = new Array
        let msg = ''
        for (let i in errMsg) temp.push(i)
        if (temp[0] == 'redeemData') msg = '区间起点的值'
        else if (temp[0] == 'redeemTo') msg = '区间终点的值'
        else if (temp[0] == 'redeemRate') msg = '费率（%）'
        else msg ='未知区间'
        this.$message.error("交易信息--赎回付费-" + '浮动范围' + " 校验不通过！");
        this.handleClick({ label: '交易信息' })
      } else {
        let redeemData = this.$refs.xTableRedeem.getTableData().tableData
        for (let i = 0; i < redeemData.length; i++) {
          if (+(redeemData[i].redeemFrom) >= +(redeemData[i].redeemTo)) {
            this.$refs.xTableRedeem.setActiveCell(redeemData[i], 'redeemFrom')  //当前校验不通过的单元格获取到焦点
            this.countSubmit_btn = false
            this.$message.error("交易信息--区间起点的值不能 大于 / 等于 区间终点的值 ！");
            this.handleClick({ label: '交易信息' })
            return
          }
          if (i > 0) {
            if (+(redeemData[i-1].redeemTo) >  +(redeemData[i].redeemFrom)) {
              this.$refs.xTableRedeem.setActiveCell(redeemData[i-1], 'redeemTo')
              this.countSubmit_btn = false
              this.$message.error("交易信息--上一列区间终点的值不能 大于 下一列区间起点的值 ！");
              this.handleClick({ label: '交易信息' })
              return
            }
          }
        }
        this.xTableRewardJudge()
      }
    },
    // 费用信息的from和to
   async xTableRewardJudge () {
      if (this.rewardType_show) {
          var redeemData = this.$refs.xTableReward.getTableData().tableData
          if (redeemData.length == 0) {
            this.$message.error('费用信息 计提比例浮动范围不能为空 ！')
            this.countSubmit_btn = false
            this.handleClick({ label: '费用信息' })
            return
          }
      } else return this.xTableGradeJudge()
      
      let errMsg = await this.$refs["xTableReward"].validate().catch(errMap => errMap)
      if (errMsg) {
        this.countSubmit_btn = false
        let temp = new Array
        let msg = ''
        for (let i in errMsg) temp.push(i)
        if (temp[0] == 'rewardFrom') msg = '区间起点的值'
        else if (temp[0] == 'rewardTo') msg = '区间终点的值'
        else if (temp[0] == 'rewardRate') msg = '计提比例（%）'
        else msg ='未知区间'
        this.$message.error("费用信息--业绩报酬-" + '浮动范围' + " 校验不通过 ！");
        this.handleClick({ label: '费用信息' })
        return
      } else {
        // let redeemData = this.$refs.xTableReward.getTableData().tableData
        for (let i = 0; i < redeemData.length; i++) {
          if (+(redeemData[i].rewardFrom) >= +(redeemData[i].rewardTo)) {
            this.$refs.xTableReward.setActiveCell(redeemData[i], 'rewardFrom')
            this.countSubmit_btn = false
            this.$message.error("费用信息--区间起点的值不能 大于 / 等于 区间终点的值 ！");
            this.handleClick({ label: '费用信息' })
            return
          }
          if (i > 0) {
            if (+(redeemData[i-1].rewardTo) >  +(redeemData[i].rewardFrom)) {
              this.$refs.xTableReward.setActiveCell(redeemData[i-1], 'rewardTo')
              this.countSubmit_btn = false
              this.$message.error("费用信息--上一列区间终点的值不能 大于 下一列区间起点的值 ！");
              this.handleClick({ label: '费用信息' })
              return
            }
          }
        }
        this.xTableGradeJudge()
      }
    },
    // 分级管理校验
   async xTableGradeJudge() {
     if (!this.isFj_show) return this.xTableMySallerJudge()
     let errMsg = await this.$refs["xTableGrade"].validate().catch(errMap => errMap)
     if (errMsg) {
       this.countSubmit_btn = false
       this.$message.error("分级关系 列表校验不通过 ！");
       this.handleClick({ label: '分级关系' })
     } else {
       this.xTableMySallerJudge();
     }
    },
    // 销售方式1
   async xTableMySallerJudge() {
     let errMsg = await this.$refs["xTableMySaller"].validate().catch(errMap => errMap)
     if (errMsg) {
       this.countSubmit_btn = false
       this.$message.error('销售方式 列表校验不通过 ！')
       this.handleClick({ label: '销售方式' })
     } else {
       this.xTableMyOpenJudge();
     }
    },
    // 开放日2
   async xTableMyOpenJudge() {
     let errMsg = await this.$refs["xTableMyOpen"].validate().catch(errMap => errMap)
     if (errMsg) {
       this.countSubmit_btn = false
       this.$message.error("开放日 列表校验不通过 ！");
       this.handleClick({ label: '开放日' })
     } else {
      //  this.countSubmit_btn = false
      //  console.log('pass');
       this.xTableFundManagerJudge();
     }
    },
    // 基金经理3
   async xTableFundManagerJudge() {
      let errMsg = await this.$refs["xTableFundManager"].validate().catch(errMap => errMap)
      if (errMsg) {
        this.countSubmit_btn = false
        this.$message.error("基金经理 列表校验不通过 ！");
        this.handleClick({ label: '基金经理' })
      } else this.xTableContactJudge();
    },
    // 联系人4
   async xTableContactJudge() {
     let errMsg = await this.$refs["xTableContact"].validate().catch(errMap => errMap)
     if (errMsg) {
       this.countSubmit_btn = false
       this.$message.error("联系人 列表校验不通过 ！");
       this.handleClick({ label: '联系人' })
     } else {
       this.initTable()
      //  if (this.isdraftSaveOrPassSave) {
            this.isSave = true;
            this.fullValidEvent();
      //   } else {
      //     this.countSubmit_btn = false
      //     this.draftSave()
      //   }
     }
    },
    draftSave () {
      if(this.PageDataAdd.addType === 0 ){
            this.saveCg();
          } else {
            this.saveVolidFundCode();
        }
    },
    saveCg() {
      let params = {};
      params = commonFun.parameterSrc(this.formInline);
      this.initTable();
      this.countSubmit_btn = true;
      let insertRecordsContacts = [];
      if (this.$refs.xTableContact) {
        insertRecordsContacts = this.$refs.xTableContact.getTableData()
          .tableData;
      }
      let params2 = {};
	  if(params.purchasePoint){
		 params.purchasePoint=params.purchasePoint.toString().replace(/,/gi, '');
	  }
	  
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
      // console.log(params2); return
      pageApi.saveDataSource(params2).then((response) => {
          if (response.data.status === 200) {
            // 关闭移动指标弹框
            // this.$message.closeAll();
            // this.$message({
            //   message: "保存成功",
            //   type: "success",
            // });
            // 刷新列表
            // this.$emit("pageCheckClick", {
            //   data: [],
            //   flag: true,
            // });
            // 提交保存草稿后 提示是否要提审核
            this.isPassSave()
          } else {
            // 关闭移动指标弹框
            // this.countDialog = false;
            this.$message.closeAll();
            this.$message({
              message: response.data.message || "保存失败",
              type: "error",
            });
            this.isSave = false;
          }
          this.countSubmit_btn = false;
        })
        .catch(() => {
          // 关闭移动指标弹框

          this.countSubmit_btn = false;
          this.$message.closeAll();
          this.$message({
            message: "保存失败",
            type: "error",
          });
          this.isSave = false;
        });
    },
    save(formName) {
       this.$message.closeAll()
      this.countSubmit_btn = true;
      this.isdraftSaveOrPassSave = true  //判断是保存草稿还是提交审核
      this.$refs["formInline"].validate((valid, obj) => {
        if (valid) {
          this.xTableRedeemJudge()  //分级管理校验
        } else {
          this.assignJudge(obj)
        }
      })
    },
    saveBefore() {
      if (!this.validContactFlag) {
        this.$message.closeAll();
        this.$message({
          message: "请填写正确的联系人信息",
          type: "erro",
        });
        this.isSave = false;
        this.countSubmit_btn = false
        this.handleClick({ label: '联系人' })
        return;
      }
      if (!this.validRewardtFlag) {
        this.$message.closeAll();
        this.$message({
          message: "请填写完整的计提信息",
          type: "erro",
        });
        this.isSave = false;
        this.countSubmit_btn = false
        this.handleClick({ label: '费用信息' })
        return;
      }
      if (!this.validRedeemFlag && this.callFloat_select_show) {
        this.$message.closeAll();
        this.$message({
          message: "请填写完整的费率信息",
          type: "erro",
        });
        this.isSave = false;
        this.countSubmit_btn = false
        this.handleClick({ label: '交易信息' })
        return;
      }
      if (!this.validGradeFlag && this.isFj_show) {
        this.$message.closeAll();
        this.$message({
          message: "请填写完整的分级信息",
          type: "erro",
        });
        this.isSave = false;
        this.countSubmit_btn = false
        if (this.isFj_show) this.handleClick({ label: '分级关系' })
        return;
      }
      if (this.tableDataGrade.length > 0 && this.isFj_show) {
        if (this.validTableDate(this.tableDataGrade)) {
          this.$message.closeAll();
          this.$message({
            message: "分级关系列表，开始日期/结束日期填写错误",
            type: "error",
          });
          this.isSave = false;
          this.countSubmit_btn = false
          this.handleClick({ label: '分级关系' })
          return;
        }
      }

      if (!this.validSallerFlag) {
        this.$message.closeAll();
        this.$message({
          message: "请填写完整的销售方式信息",
          type: "erro",
        });
        this.isSave = false;
        this.countSubmit_btn = false
        this.handleClick({ label: '销售方式' })
        return;
      }

      if (!this.validOpenFlag) {
        this.$message.closeAll();
        this.$message({
          message: "请填写完整的开放日信息",
          type: "erro",
        });
        this.isSave = false;
        this.countSubmit_btn = false
        this.handleClick({ label: '开放日' })
        return;
      }

      if (!this.validFundManagerFlag) {
        this.$message.closeAll();
        this.$message({
          message: "请填写完整的基金经理信息",
          type: "erro",
        });
        this.isSave = false;
        this.countSubmit_btn = false
        this.handleClick({ label: '基金经理' })
        return;
      }

      if (this.tableDataSaller.length > 0) {
        if (this.validTableDate(this.tableDataSaller)) {
          this.$message.closeAll();
          this.$message({
            message: "销售方式列表，开始日期/结束日期填写错误",
            type: "error",
          });
          this.isSave = false;
          this.countSubmit_btn = false
          this.handleClick({ label: '销售方式' })
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
          this.countSubmit_btn = false
          this.handleClick({ label: '开放日' })
          return;
        }
      }

        if (this.isdraftSaveOrPassSave) {
            // this.isSave = true;
            // this.fullValidEvent();
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
                this.$message.closeAll();
                this.$message({
                  message: "请完善输入信息",
                  type: "error",
                });

                return false;
              }
            });
        } else {
          this.countSubmit_btn = false
          this.draftSave()
        }


      
    },
    saveData() {
      this.$confirm("确定提交审核?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          let params = {};
          params = commonFun.parameterSrc(this.formInline);

          let insertRecordsContacts = [];
          if (this.$refs.xTableContact) {
            insertRecordsContacts = this.$refs.xTableContact.getTableData()
              .tableData;
          }
          this.countSubmit_btn = true;
          let params2 = {};
		  
		  if(params.purchasePoint){
			 params.purchasePoint=params.purchasePoint.toString().replace(/,/gi, '');
		  }
		  
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
              if (response.data.status === 200) {
                // 关闭移动指标弹框
                this.$message.closeAll();
                this.$message({
                  message: response.data.message || "提交审核成功",
                  type: "success",
                });
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
                  message: response.data.message || "提交审核失败",
                  type: "error",
                });
                this.isSave = false;
              }
              this.countSubmit_btn = false;
            })
            .catch(() => {
              // 关闭移动指标弹框
              this.countSubmit_btn = false;
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
          this.countSubmit_btn = false;
          this.isSave = false;
        });
    },
    updateData() {
      this.$confirm("确定提交审核?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          this.submitSave()
        }).catch(() => {
          // 关闭移动指标弹框
          this.countSubmit_btn = false;
          this.isSave = false;
          this.isdraftSaveOrPassSave = false
        });
    },
    submitSave () {
          let params = {};
          params = commonFun.parameterSrc(this.formInline);
          this.countSubmit_btn = true;
          let params2 = {};
		  
		  if(params.purchasePoint){
			 params.purchasePoint=params.purchasePoint.toString().replace(/,/gi, '');
		  }

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
              if (response.data.status === 200) {
                // 关闭移动指标弹框
                this.$message.closeAll();
                this.$message({
                  message: response.data.message || "提交审核成功",
                  type: "success",
                });
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
                  message: response.data.message || "提交审核失败",
                  type: "error",
                });
                this.isSave = false;
              }
              this.countSubmit_btn = false;
            })
            .catch(() => {
              // 关闭移动指标弹框
              this.countSubmit_btn = false;
              this.$message.closeAll();
              this.$message({
                message: "提交审核失败",
                type: "error",
              });
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
      let insertRecordsContacts = [];
      if (this.$refs.xTableContact) {
        insertRecordsContacts = this.$refs.xTableContact.getTableData().tableData;
      }
      let insertRecordsRewards = [];
      if (this.$refs.xTableReward) {
        insertRecordsRewards = this.$refs.xTableReward.getTableData().tableData;
      }
      let insertRecordsSallers = [];
      if (this.$refs.xTableMySaller) {
        insertRecordsSallers = this.$refs.xTableMySaller.getTableData().tableData;
      }
      let insertRecordsOpen = [];
      if (this.$refs.xTableMyOpen) {
        let data = this.$refs.xTableMyOpen.getTableData();
        insertRecordsOpen = this.$refs.xTableMyOpen.getTableData().tableData;
      }
      let insertRecordsFundManager = [];
      if (this.$refs.xTableFundManager) {
        let data = this.$refs.xTableFundManager.getTableData();
        insertRecordsFundManager = this.$refs.xTableFundManager.getTableData().tableData;
      }
      if (insertRecordsContacts.length > 0) {
        this.tableDataContact = insertRecordsContacts; //联系人列表数据
      }
      if (insertRecordsRedeem.length > 0) {
        this.tableDataRedeem = insertRecordsRedeem; //赎回费率列表数据
      }
      if (insertRecordsGrade.length > 0) {
        this.tableDataGrade = insertRecordsGrade; //分级列表数据
        // console.log('分级关系1',this.tableDataGrade);
      }

      if (insertRecordsRewards.length > 0) {
        this.tableDataReward = insertRecordsRewards; //计提列表数据
        // this.defaultTableDataReward = insertRecordsRewards; //计提列表数据
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
      // if (data.fundRedeems) {
      //   this.tableDataRedeem = data.fundRedeems; //赎回费率列表数据
      // }
      if (data.fundContacts) {
        this.tableDataContact = data.fundContacts; //赎回费率列表数据
        if(this.PageDataAdd.beforeData){
          if(this.PageDataAdd.beforeData.fundContacts){
            this.tableDataContact_before=this.PageDataAdd.beforeData.fundContacts;
            this.tableDataContact=current(this.tableDataContact,this.tableDataContact_before);
            // console.log('联系人列表',this.tableDataContact);
            this.lxr_i_show=this.judgeChangeLXR(this.tableDataContact);
            console.log('this.lxr_i_show',this.lxr_i_show);
          }
        }
      }
      if (data.fundGrades) {
        this.tableDataGrade = data.fundGrades; //赎回费率列表数据
        // console.log('分级关系2',this.tableDataGrade);
        
        if(this.PageDataAdd.beforeData){
          if(this.PageDataAdd.beforeData.fundGrades){
            this.tableDataGrade_before=this.PageDataAdd.beforeData.fundGrades;
            this.tableDataGrade=current(this.tableDataGrade,this.tableDataGrade_before)
            this.fjgx_i_show=this.judgeChangeFJ(this.tableDataGrade)
          }
        }
      }
      if (data.fundRewards) {
        this.tableDataReward = data.fundRewards; //计提列表数据
        // this.defaultTableDataReward = data.fundRewards; //计提列表数据
        if(this.PageDataAdd.beforeData){
          this.tableDataReward_before=this.PageDataAdd.beforeData.fundRewards
          this.tableDataReward=current(this.tableDataReward,this.tableDataReward_before)
          this.fyxx_i_show2=this.judgeChangeFYXX(this.tableDataReward)

          // console.log('new and old',this.tableDataSaller);
        }
      }
      if (data.fundSallers) {
        this.tableDataSaller = data.fundSallers; //计提列表数据
        // console.log('销售方式',this.tableDataSaller);
        if(this.PageDataAdd.beforeData){
          this.tableDataSaller_before=this.PageDataAdd.beforeData.fundSallers
          this.tableDataSaller=current(this.tableDataSaller,this.tableDataSaller_before)
          this.xsfs_i_show=this.judgeChangeXS(this.tableDataSaller);
          console.log(this.xsfs_i_show,'this.xsfs_i_show');
          // console.log('new and old',this.tableDataSaller);

        }
      }
      if (data.fundManagers) {
        this.tableDataFundManager = data.fundManagers; //计提列表数据

        if(this.PageDataAdd.beforeData){
          this.tableDataFundManager_before=this.PageDataAdd.beforeData.fundManagers
          this.tableDataFundManager=current(this.tableDataFundManager,this.tableDataFundManager_before)
          // console.log('new and old',this.tableDataFundManager);
          this.jjjl_i_show=this.judgeChangeJJJL(this.tableDataFundManager)
        }
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
        // console.log('this.tableDataOpen--',this.tableDataOpen);
        if(this.PageDataAdd.beforeData){
          this.tableDataOpen_before=this.PageDataAdd.beforeData.fundOpens
          this.tableDataOpen=current(this.tableDataOpen,this.tableDataOpen_before)
          this.kfr_i_show=this.judgeChangeKFR(this.tableDataOpen);
          // console.log('this.tableDataOpen',this.tableDataOpen);
        }
      }
      if (data.fundInvests) {
        let arr = [];
        let arrs = data.fundInvests;
        this.checkfundInvestArea_=arrs;
        for (let i = 0; i < arrs.length; i++) {
          arr.push(arrs[i].investScope);
        }
        this.checkfundInvestArea = arr;
        if(this.PageDataAdd.beforeData){
          if(this.PageDataAdd.beforeData.fundInvests){
            this.checkfundInvestArea_before=this.PageDataAdd.beforeData.fundInvests
            // console.log('--------');
            // console.log(this.checkfundInvestArea);
            // console.log(this.checkfundInvestArea_before);
            
          }
        }
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
      // console.log(this.formInline);
      // console.log(formData);
      this.formInline = formData;
      // 基础信息
      if(this.PageDataAdd.beforeData){
        let formInlineJCXX_now = commonFun.allPrpos(this.formInlineJCXX, data);
        this.formInlineJCXX_now = formInlineJCXX_now;
        let formInlineJCXX_before = commonFun.allPrpos(this.formInlineJCXX1, this.PageDataAdd.beforeData.fundInfo);
        this.formInlineJCXX_before = formInlineJCXX_before;
        this.jcxx_i_show=this.judgeChange (this.formInlineJCXX_now, this.formInlineJCXX_before);
      }
      // console.log('this.formInlineJCXX_now',this.formInlineJCXX_now);
      // console.log('this.formInlineJCXX_before',this.formInlineJCXX_before);
      // console.log('boo',this.judgeChange (this.formInlineJCXX_now, this.formInlineJCXX_before));
      // 交易信息
      if(this.PageDataAdd.beforeData){
        let formInlineJYXX_now = commonFun.allPrpos(this.formInlineJYXX, data);
        this.formInlineJYXX_now = formInlineJYXX_now;
        let formInlineJYXX_before = commonFun.allPrpos(this.formInlineJYXX1, this.PageDataAdd.beforeData.fundInfo);
        this.formInlineJYXX_before = formInlineJYXX_before;
        this.jyxx_i_show=this.judgeChange (this.formInlineJYXX_now, this.formInlineJYXX_before);
      }
      // console.log('this.formInlineJCXX_now',this.formInlineJYXX_now);
      // console.log('this.formInlineJCXX_before',this.formInlineJYXX_before);
      // console.log('boo',this.judgeChange (this.formInlineJYXX_now, this.formInlineJYXX_before));
      // 费用信息
      if(this.PageDataAdd.beforeData){
        let formInlineFYXX_now = commonFun.allPrpos(this.formInlineFYXX, data);
        this.formInlineFYXX_now = formInlineFYXX_now;
        let formInlineFYXX_before = commonFun.allPrpos(this.formInlineFYXX1, this.PageDataAdd.beforeData.fundInfo);
        this.formInlineFYXX_before = formInlineFYXX_before;
        this.fyxx_i_show=this.judgeChange (this.formInlineFYXX_now, this.formInlineFYXX_before);
      }
      // console.log('this.formInlineJCXX_now',this.formInlineJYXX_now);
      // console.log('this.formInlineJCXX_before',this.formInlineJYXX_before);
      // console.log('boo',this.judgeChange (this.formInlineJYXX_now, this.formInlineJYXX_before));
      // 收益分配
      if(this.PageDataAdd.beforeData){
        let formInlineSYFP_now = commonFun.allPrpos(this.formInlineSYFP, data);
        this.formInlineSYFP_now = formInlineSYFP_now;
        let formInlineSYFP_before = commonFun.allPrpos(this.formInlineSYFP1, this.PageDataAdd.beforeData.fundInfo);
        this.formInlineSYFP_before = formInlineSYFP_before;
        this.syfp_i_show=this.judgeChange (this.formInlineSYFP_now, this.formInlineSYFP_before);
      }
      // 投资风控
      if(this.PageDataAdd.beforeData){
        let formInlineTZFK_now = commonFun.allPrpos(this.formInlineTZFK, data);
        this.formInlineTZFK_now = formInlineTZFK_now;
        let formInlineTZFK_before = commonFun.allPrpos(this.formInlineTZFK1, this.PageDataAdd.beforeData.fundInfo);
        this.formInlineTZFK_before = formInlineTZFK_before;
        // console.log(formInlineTZFK_now,formInlineTZFK_before,'111');
        this.tzfk_i_show=this.judgeChange (this.formInlineTZFK_now, this.formInlineTZFK_before);
        console.log(this.tzfk_i_show,'tzfk_i_show');
      }
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
        // this.callFloat_select_show = true;
        // this.mdFlagOpen = true
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
        this.formInline.isFixedPrepare == "1"
      ) {
        this.rewardPrepareDate_show = true;
      }
      if (this.formInline.saleType) {
        this.saleTypeChange(this.formInline.saleType);
      }
      this.formInline.callRate = formData.callRate;
      // this.callDeliverDaySelect(formData.callRateType)
      this.formInline.callRateType = formData.callRateType;
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
		
		  if (val === "gz_date") {
            this.guZhiist = res.data.data; //估值频率
            if(this.PageDataAdd.beforeData){
              if(this.PageDataAdd.beforeData.fundInfo.assetFrequency){
                let assetFrequencyobj = res.data.data.find((item,index,arr)=>{
                    return item.dimCde == this.PageDataAdd.beforeData.fundInfo.assetFrequency
                  })
                this.assetFrequency=assetFrequencyobj.dimNme;
              }
            }
          }
          if (val === "fundinfo_fundState") {
            this.fundStateArr = res.data.data; //产品状态
            if(this.PageDataAdd.beforeData){
              if(this.PageDataAdd.beforeData.fundInfo.fundState){
                let fundStateobj = res.data.data.find((item,index,arr)=>{
                    return item.dimCde == this.PageDataAdd.beforeData.fundInfo.fundState
                  })
                this.fundState=fundStateobj.dimNme;
              }
            }
          }

          if (val === "fundTrustorCodeType") {
            this.trustorCodeArr = res.data.data; //托管人名称
            // console.log('托管人名称',this.trustorCodeArr);
          }
          if (val === "fundManagerCodeType") {
            this.managerCodeArr = res.data.data; //管理人名称
          }

          if (val === "fundoperatorCodeType") {
            this.operatorCodeArr = res.data.data; //基金服务机构
          }
          if (val === "fundTypes") {
            this.fundTypeArr = res.data.data; //基金类型
            if(this.PageDataAdd.beforeData){
              if(this.PageDataAdd.beforeData.fundInfo.fundType){
                let fundTypeobj = res.data.data.find((item,index,arr)=>{
                    return item.dimCde == this.PageDataAdd.beforeData.fundInfo.fundType
                  })
                // console.log(fundTypeobj.dimNme);
                this.fundType=fundTypeobj.dimNme;
              }
            }
          }
          if (val === "fundInvestDirectType") {
            this.investDirectArr = res.data.data; //投资方向
            if(this.PageDataAdd.beforeData){
              if(this.PageDataAdd.beforeData.fundInfo.investDirect){
                let investDirectobj = res.data.data.find((item,index,arr)=>{
                  return item.dimCde == this.PageDataAdd.beforeData.fundInfo.investDirect
                })
                this.investDirect=investDirectobj.dimNme;
              }
            }
          }
          if (val === "fundRiskLevelType") {
            this.riskLevelArr = res.data.data; //风险等级
            if(this.PageDataAdd.beforeData){
              if(this.PageDataAdd.beforeData.fundInfo.riskLevel){
                let riskLevelobj = res.data.data.find((item,index,arr)=>{
                  return item.dimCde == this.PageDataAdd.beforeData.fundInfo.riskLevel
                })
                this.riskLevel=riskLevelobj.dimNme;
              }
            }
          }
          if (val === "fundSaleType") {
            this.saleTypeArr = res.data.data; //销售方式
          }
          if (val === "fundSubscribeConfirmDayType") {
            this.subscribeConfirmDayArr = res.data.data; //认购交易确认天数
            if(this.PageDataAdd.beforeData){
              if(this.PageDataAdd.beforeData.fundInfo.subscribeConfirmDay){
                let subscribeConfirmDayobj = res.data.data.find((item,index,arr)=>{
                  return item.dimCde == this.PageDataAdd.beforeData.fundInfo.subscribeConfirmDay
                })
                this.subscribeConfirmDay=subscribeConfirmDayobj.dimNme;
              }
            }
          }
          if (val === "fundSubscribeDeliverDayType") {
            this.subscribeDeliverDayArr = res.data.data; //认购资金交收天数
            if(this.PageDataAdd.beforeData){
              if(this.PageDataAdd.beforeData.fundInfo.subscribeDeliverDay){
                let subscribeDeliverDayobj = res.data.data.find((item,index,arr)=>{
                  return item.dimCde == this.PageDataAdd.beforeData.fundInfo.subscribeDeliverDay
                })
                this.subscribeDeliverDay=subscribeDeliverDayobj.dimNme;
              }
            }
          }
          if (val === "fundApplyConfirmDayType") {
            this.applyConfirmDayArr = res.data.data; //申购交易确认天数
            // this.applyConfirmDayArr = res.data.data; //申购资金交收天数
            if(this.PageDataAdd.beforeData){
              if(this.PageDataAdd.beforeData.fundInfo.applyConfirmDay){
                let applyConfirmDayobj = res.data.data.find((item,index,arr)=>{
                  return item.dimCde == this.PageDataAdd.beforeData.fundInfo.applyConfirmDay
                })
                this.applyConfirmDay=applyConfirmDayobj.dimNme;
              }
            }
          }
          if (val === "fundApplyDeliverDayType") {
            this.applyDeliverDayArr = res.data.data; //申购资金交收天数
            if(this.PageDataAdd.beforeData){
              if(this.PageDataAdd.beforeData.fundInfo.applyDeliverDay){
                let applyDeliverDayobj = res.data.data.find((item,index,arr)=>{
                  return item.dimCde == this.PageDataAdd.beforeData.fundInfo.applyDeliverDay
                })
                this.applyDeliverDay=applyDeliverDayobj.dimNme;
              }
            }
          }
          if (val === "fundCallConfirmDayType") {
            this.callConfirmDayArr = res.data.data; //赎回交易确认天数
            if(this.PageDataAdd.beforeData){
              if(this.PageDataAdd.beforeData.fundInfo.callConfirmDay){
                let callConfirmDayobj = res.data.data.find((item,index,arr)=>{
                  return item.dimCde == this.PageDataAdd.beforeData.fundInfo.callConfirmDay
                })
                this.callConfirmDay=callConfirmDayobj.dimNme;
              }
            }
          }
          if (val === "fundCallDeliverDayType") {
            this.callDeliverDayArr = res.data.data; //赎回资金交收天数
            if(this.PageDataAdd.beforeData){
              if(this.PageDataAdd.beforeData.fundInfo.callDeliverDay){
                let callDeliverDayobj = res.data.data.find((item,index,arr)=>{
                  return item.dimCde == this.PageDataAdd.beforeData.fundInfo.callDeliverDay
                })
                this.callDeliverDay=callDeliverDayobj.dimNme;
              }
            }
          }
          if (val === "fundCallFloatType") {
            this.callRateTypeArr = res.data.data; //赎回费率浮动类型
            // console.log('赎回费率浮动类型',res.data.data);
            if(this.PageDataAdd.beforeData){
              if(this.PageDataAdd.beforeData.fundInfo.callRateType){
                let callRateTypeobj = res.data.data.find((item,index,arr)=>{
                  return item.dimCde == this.PageDataAdd.beforeData.fundInfo.callRateType
                })
                // console.log(callRateTypeobj);
                this.callRateType=callRateTypeobj.dimNme;
              }
            }
          }
          if (val === "fundManageFeePrepareType") {
            this.manageFeePrepareArr = res.data.data; //管理费-计提
            if(this.PageDataAdd.beforeData){
              if(this.PageDataAdd.beforeData.fundInfo.manageFeePrepare){
                let manageFeePrepareobj = res.data.data.find((item,index,arr)=>{
                  return item.dimCde == this.PageDataAdd.beforeData.fundInfo.manageFeePrepare
                })
                this.manageFeePrepare=manageFeePrepareobj.dimNme;
              }
            }

            if(this.PageDataAdd.beforeData){
              if(this.PageDataAdd.beforeData.fundInfo.trustFeePrepare){
                let trustFeePrepareobj = res.data.data.find((item,index,arr)=>{
                  return item.dimCde == this.PageDataAdd.beforeData.fundInfo.trustFeePrepare
                })
                this.trustFeePrepare=trustFeePrepareobj.dimNme;
              }
            }

            if(this.PageDataAdd.beforeData){
              if(this.PageDataAdd.beforeData.fundInfo.operateFeePrepare){
                let operateFeePrepareobj = res.data.data.find((item,index,arr)=>{
                  return item.dimCde == this.PageDataAdd.beforeData.fundInfo.operateFeePrepare
                })
                this.operateFeePrepare=operateFeePrepareobj.dimNme;
              }
            }
          }
          if (val === "fundManageFeeStand") {
            this.manageFeeAssetArr = res.data.data; //管理费-计算方式
            if(this.PageDataAdd.beforeData){
              if(this.PageDataAdd.beforeData.fundInfo.manageFeeAsset){
                let manageFeeAssetobj = res.data.data.find((item,index,arr)=>{
                  return item.dimCde == this.PageDataAdd.beforeData.fundInfo.manageFeeAsset
                })
                this.manageFeeAsset=manageFeeAssetobj.dimNme;
              }
            }

            if(this.PageDataAdd.beforeData){
              if(this.PageDataAdd.beforeData.fundInfo.trustFeeAsset){
                let trustFeeAssetobj = res.data.data.find((item,index,arr)=>{
                  return item.dimCde == this.PageDataAdd.beforeData.fundInfo.trustFeeAsset
                })
                this.trustFeeAsset=trustFeeAssetobj.dimNme;
              }
            }

            if(this.PageDataAdd.beforeData){
              if(this.PageDataAdd.beforeData.fundInfo.operateFeeAsset){
                let operateFeeAssetobj = res.data.data.find((item,index,arr)=>{
                  return item.dimCde == this.PageDataAdd.beforeData.fundInfo.operateFeeAsset
                })
                this.operateFeeAsset=operateFeeAssetobj.dimNme;
              }
            }
          }
          if (val === "fundManageFeePayType") {
            this.manageFeePayArr = res.data.data; //管理费-支付方式
            if(this.PageDataAdd.beforeData){
              if(this.PageDataAdd.beforeData.fundInfo.manageFeePay){
                let manageFeePayobj = res.data.data.find((item,index,arr)=>{
                  return item.dimCde == this.PageDataAdd.beforeData.fundInfo.manageFeePay
                })
                this.manageFeePay=manageFeePayobj.dimNme;
              }
  
              if(this.PageDataAdd.beforeData.fundInfo.trustFeePay){
                let trustFeePayobj = res.data.data.find((item,index,arr)=>{
                  return item.dimCde == this.PageDataAdd.beforeData.fundInfo.trustFeePay
                })
                this.trustFeePay=trustFeePayobj.dimNme;
              }
  
              if(this.PageDataAdd.beforeData.fundInfo.operateFeePay){
                let operateFeePayobj = res.data.data.find((item,index,arr)=>{
                  return item.dimCde == this.PageDataAdd.beforeData.fundInfo.operateFeePay
                })
                this.operateFeePay=operateFeePayobj.dimNme;
              }
            }
          }
          if (val === "fundRewardType") {
            this.rewardTypeArr = res.data.data; //业绩报酬
            if(this.PageDataAdd.beforeData){
              if(this.PageDataAdd.beforeData.fundInfo.rewardType){
                let rewardTypeobj = res.data.data.find((item,index,arr)=>{
                  return item.dimCde == this.PageDataAdd.beforeData.fundInfo.rewardType
                })
                this.rewardType=rewardTypeobj.dimNme;
              }
            }
          }
          if (val === "fundRewardPrepareType") {
            this.rewardPrepareTypeArr = res.data.data; //计提方式
            if(this.PageDataAdd.beforeData){
              if(this.PageDataAdd.beforeData.fundInfo.rewardPrepareType){
                let rewardPrepareTypeobj = res.data.data.find((item,index,arr)=>{
                  return item.dimCde == this.PageDataAdd.beforeData.fundInfo.rewardPrepareType
                })
                this.rewardPrepareType=rewardPrepareTypeobj.dimNme;
              }
            }
          }
          if (val === "fundPortionNumberType") {
            this.portionNumberArr = res.data.data; //分配次数
            if(this.PageDataAdd.beforeData){
              if(this.PageDataAdd.beforeData.fundInfo.portionNumber){
                let portionNumberobj = res.data.data.find((item,index,arr)=>{
                  return item.dimCde == this.PageDataAdd.beforeData.fundInfo.portionNumber
                })
                this.portionNumber=portionNumberobj.dimNme;
              }
            }
          }
          if (val === "fundBonusProcessType") {
            this.bonusProcessArr = res.data.data; //提交分红流程
          }
          if (val === "fundDataExpectType") {
            this.dataExpectArr = res.data.data; //预估数据以及计算报表
            // console.log('预估数据以及计算报表',this.dataExpectArr);
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
            // console.log('投资范围',this.fundInvestArea);
            // console.log(this.checkfundInvestArea_,this.checkfundInvestArea_before,'this.fundInvestArea');
            if(this.fundInvestArea[0]){
              this.tzfk_i_show2 = this.isCheackChange(this.checkfundInvestArea_,this.checkfundInvestArea_before,this.fundInvestArea)
              console.log('tzfk_i_show2',this.tzfk_i_show2);
            }
            // this.isCheackChange()
          }

          if (val === "fundOpenFrequence") {
            let arr = [{ dimCde: "", dimNme: "" }];
            let arr1 = res.data.data;
            // arr1.forEach(item=>{
            //   this.getEdims2(item)
            // })
            if (arr1.length > 0) {
              arr = arr.concat(arr1);
              this.openFrequenceArr = arr;
              // console.log('开放频率数组',this.openFrequenceArr);
              
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
            if(this.PageDataAdd.beforeData){
              if(this.PageDataAdd.beforeData.fundInfo.rewardPrepareDate){
                let rewardPrepareDateobj = res.data.data.find((item,index,arr)=>{
                  return item.dimCde == this.PageDataAdd.beforeData.fundInfo.rewardPrepareDate
                })
                this.rewardPrepareDate=rewardPrepareDateobj.dimNme;
              }
            }
          }
        } else {
          this.$message.closeAll();
          this.$message.error("初始化数据失败");
        }
      });
    },
    transition_openFrequence(val){
      if(this.openFrequenceArr[0]){
        if(val){
          let openFrequenceobj = this.openFrequenceArr.find((item,index,arr)=>{
            return item.dimCde == val
          })
          return openFrequenceobj.dimNme;
        }
      }
    },
    transition_openRule(val){
      if(this.openRuleArr[0]){
        if(val){
          let openRuleobj = this.openRuleArr.find((item,index,arr)=>{
            return item.dimCde == val
          })
          return openRuleobj.dimNme;
        }
      }
    },
    // transition_openRule(val){
    //   if(this.YopenRuleArr[0]){
    //     if(val){
    //       let openRuleobj = this.YopenRuleArr.find((item,index,arr)=>{
    //         return item.dimCde == val
    //       })
    //       return openRuleobj.dimNme;
    //     }
    //   }
    // },
    getEdims2(obj){
      let params = {dimTypecode:"fundOpenRule",parentId:obj.id}
      commonApi.getEdims2(params).then(res=>{
        if(obj.dimCde=="Y"){
          //每年
          this.YopenRuleArr = res.data.data;
        }
        if(obj.dimCde=="S"){
          // 每半年
          this.SopenRuleArr = res.data.data;
        }
        if(obj.dimCde=="Q"){
          // 每季度
          this.QopenRuleArr = res.data.data;
        }
        if(obj.dimCde=="M"){
          // 每月
          this.MopenRuleArr = res.data.data;
        }
        if(obj.dimCde=="MC"){
          // 固定月
          this.MCopenRuleArr = res.data.data;
        }
        if(obj.dimCde=="DC"){
          // 固定日
          // this.DCopenRuleArr = res.data.data;
        }
      })
    },
    getEdims() {
	  //估值频率
      this.getEdimsGet('gz_date');
      // 管理人
      this.getDeptInfoSel('institution_manager');
      // 托管人
      this.getDeptInfoSel('institution_trusteeship');
      // 基金服务机构
      this.getDeptInfoSel('institution_operator');

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
      // this.getProductInfo();
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
            this.$message.closeAll();
            this.$message.error("查询产品信息失败");
          }
        })
        .catch(() => {
          this.$message.closeAll();
          this.$message.error("查询产品信息失败");
          this.fundNameGradeArr = [];
        });
    },
    validTableDate(arr) {
      for (let i = 0; i < arr.length; i++) {
        if (arr[i].beginDate && arr[i].endDate) {
          if (arr[i].beginDate > arr[i].endDate) {
            return true;
          }
        }
      }
    },
    handleCheckAllChange(val) {
      let arr = this.fundInvestArea;
      let chekAllArr = [];
      if (arr) {
        for (let i = 0; i < arr.length; i++) {
          chekAllArr.push(arr[i].id);
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
          if (response.data.status === 200) {
            this.saveData();
          } else {
            this.$message.closeAll();
            this.$message({
              message: response.data.message || "校验失败",
              type: "error",
            });
            this.isSave = false;
            this.countSubmit_btn = false;
            return true;
          }
        })
        .catch(() => {
          this.$message.closeAll();
          this.$message({
            message: response.data.message || "校验失败",
            type: "error",
          });
          this.isSave = false;
          return true;
        });
    },
    getDeptInfoSel(val) {
      // pageApi.getDeptInfoSel().then((response) => {
      //     if (response.status === 200) {
      //       let arr = response.data.data;
      //       this.managerCodeArr = arr; //管理人-数组
      //       this.trustorCodeArr = arr; //管理人-数组
      //       this.operatorCodeArr = arr; //管理人-数组
      //     } else {
      //       this.managerCodeArr = []; //管理人-数组
      //       this.trustorCodeArr = []; //托管人-数组
      //       this.operatorCodeArr = []; //基金服务机构-数组
      //     }
      //   })
      //   .catch(() => {});
      // console.log('1111');
      let params ={instTypeDim:val};
      pageApi.getDeptInfoSel(params).then((response) => {
        // console.log(response);
          if (response.data.status === 200){
            if(val==='institution_manager'){
              this.managerCodeArr = response.data.data; //管理人-数组
              if(this.PageDataAdd.beforeData){
                if(this.PageDataAdd.beforeData.fundInfo.managerCode){
                  let managerCodeobj = response.data.data.find((item,index,arr)=>{
                    return item.id == this.PageDataAdd.beforeData.fundInfo.managerCode
                  })
                  this.managerCode=managerCodeobj.instName;
                }
              }
            }
            if(val==='institution_trusteeship'){
              this.trustorCodeArr = response.data.data;  //托管人-数组
              // console.log('托管人-数组',this.trustorCodeArr);
              // console.log('qqq',this.PageDataAdd.beforeData.fundInfo.trustorCode);
              if(this.PageDataAdd.beforeData){
                if(this.PageDataAdd.beforeData.fundInfo.trustorCode){
                  let trustorCodeobj = response.data.data.find((item,index,arr)=>{
                    // console.log('aa',item);
                    return item.id == this.PageDataAdd.beforeData.fundInfo.trustorCode
                  })
                  this.trustorCode=trustorCodeobj.instName;
                }
              }
              // console.log('trustorCodeobj',trustorCodeobj.instName);
            }
            if(val==='institution_operator'){
              this.operatorCodeArr = response.data.data; //基金服务机构-数组
              if(this.PageDataAdd.beforeData){
                if(this.PageDataAdd.beforeData.fundInfo.operatorCode){
                  let operatorCodeobj = response.data.data.find((item,index,arr)=>{
                    return item.id == this.PageDataAdd.beforeData.fundInfo.operatorCode
                  })
                  this.operatorCode=operatorCodeobj.instName;
                }
              }
            }
          }else{
            this.managerCodeArr = []; //管理人-数组
            this.trustorCodeArr = []; //托管人-数组
            this.operatorCodeArr = []; //基金服务机构-数组
          }
      }).catch(()=>{});
    },
    // 获取基金经理数组
    getFundManagerArr() {
      pageApi
        .getFundManagerInfo()
        .then((response) => {
          if (response.data.status === 200) {
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
      if (!commonFun.objectIsNotEmpty(this.formInline.fundName)) {
        this.$message.closeAll();
        this.$message({
          message: "请填写基础信息-产品名称",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.fundCode)) {
        this.$message.closeAll();
        this.$message({
          message: "请填写基础信息-产品代码",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.fundType)) {
        this.$message.closeAll();
        this.$message({
          message: "请选择基础信息-基金类型",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.holdYear)) {
        this.$message.closeAll();
        this.$message({
          message: "请填写基础信息-产品存续期限",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.riskLevel)) {
        this.$message.closeAll();
        this.$message({
          message: "请选择基础信息-风险等级",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.isGrade)) {
        this.$message.closeAll();
        this.$message({
          message: "请选择基础信息-是否分级",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.investDirect)) {
        this.$message.closeAll();
        this.$message({
          message: "请选择基础信息-投资方向",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.fundState)) {
        this.$message.closeAll();
        this.$message({
          message: "请选择基础信息-产品状态",
          type: "error",
        });
        return false;
      }

      if (!commonFun.objectIsNotEmpty(this.formInline.purchasePoint)) {
        this.$message.closeAll();
        this.$message({
          message: "请选择交易信息-认申购起点（不含费）",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.subscribeConfirmDay)) {
        this.$message.closeAll();
        this.$message({
          message: "请选择交易信息-认购交易确认天数",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.subscribeRate)) {
        this.$message.closeAll();
        this.$message({
          message: "请选择交易信息-认购费率",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.applyDeliverDay)) {
        this.$message.closeAll();
        this.$message({
          message: "请选择交易信息-申购资金交收天数",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.callConfirmDay)) {
        this.$message.closeAll();
        this.$message({
          message: "请选择交易信息-赎回交易确认天数",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.callFloatType)) {
        this.$message.closeAll();
        this.$message({
          message: "请选择交易信息-赎回费率浮动类型",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.purchaseDiffAppend)) {
        this.$message.closeAll();
        this.$message({
          message: "请选择交易信息-追加认申购级差",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.subscribeDeliverDay)) {
        this.$message.closeAll();
        this.$message({
          message: "请选择交易信息-认购资金交收天数",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.applyConfirmDay)) {
        this.$message.closeAll();
        this.$message({
          message: "请选择交易信息-申购交易确认天数",
          type: "error",
        });
        return false;
      }
      if (!commonFun.objectIsNotEmpty(this.formInline.callDeliverDay)) {
        this.$message.closeAll();
        this.$message({
          message: "请选择交易信息-赎回资金交收天数",
          type: "error",
        });
        return false;
      }
      return true;
    },
    holdYearChange(value) {
      return true;
      let reg = /^([1-9]\d?|100)$/;
      if (!reg.test(value)) {
        this.holdYearVolid = true;
      } else {
        this.holdYearVolid = false;
      }
    },
    recordCodeInput(value) {
      return true;
      let reg = /^[A-Za-z0-9]+$/;
      if (!reg.test(value)) {
        this.recordCodeVolid = true;
      } else {
        this.recordCodeVolid = false;
      }
    },
    fundCodeInput(value) {
      return true;
      let reg = /^[A-Z0-9]+$/;
      if (!reg.test(value)) {
        this.fundCodeVolid = true;
      } else {
        this.fundCodeVolid = false;
      }
    },
    warnPointInput(value) {
      return true;
      let reg = /^((0){1}(\.\d{0,2})?|1)$/;
      if (!reg.test(value)) {
        this.warnPointVolid = true;
      } else {
        this.warnPointVolid = false;
      }
    },
    lossPointInput(value) {
      return true;

      let reg = /^((0){1}(\.\d{0,2})?|1)$/;
      if (!reg.test(value)) {
        this.lossPointVolid = true;
      } else {
        this.lossPointVolid = false;
      }
    },
    valiadRedeem() {
      let arr = this.tableDataRedeem;
      arr.forEach((element) => {
        if (!element.redeemFrom) {
          this.$message.closeAll();
          this.$message({
            message: "请输入区间起点",
            type: "error",
          });
        }

        if (element.redeemTo) {
          this.$message.closeAll();
          this.$message({
            message: "请输入区间终点",
            type: "error",
          });
        }

        if (element.redeemRate) {
          this.$message.closeAll();
          this.$message({
            message: "请输入费率",
            type: "error",
          });
        }
        if (this.formInline.callRateType === "M") {
          if (element.redeemFrom > element.redeemTo) {
            this.$message.closeAll();
            this.$message({
              message: "区间起点必须小于区间终点",
              type: "error",
            });
          }
        }
      });
    },
    fundTypeChange(data){
      // console.log('fundTypeChange',data);
      if(!data){
        this.formInline.fundType = ''
      }
    },
    fundTypeClick(data){
      // console.log('fundTypeClick',data);
      this.formInline.fundType = data.fundType;
      console.log(this.formInline.fundType);
    },
    getOptions(){
      pageApi.getFundType().then(res=>{
        if(res.data.status === 200){
          // let arr = this.fundTypeArr2;
          let arr = res.data.data;
          let arr1 = [];
          let arr2 = [];
          arr1 = arr.map(item=>{
            return item.fundType
          })
          arr1 = [...new Set(arr1)]
          arr1.forEach(i=>{
            let obj = { label: "", options: [] };
            arr.forEach(j=>{
              if(j.fundType==i){
                obj["label"] = j.fundTypeName;
                obj["options"].push({
                  dimCde: j.fundTypeDetails,
                  dimNme: j.fundTypeDetailName,
                  fundType: j.fundType
                });
              }
            })
            arr2.push(obj)
          })
          this.options = arr2;

          // 获取修改前 fundTypeDetails中文值
          if(this.PageDataAdd.beforeData.fundInfo.fundTypeDetails){
            let fundTypeobj = res.data.data.find((item)=>{
              return item.fundTypeDetails == this.PageDataAdd.beforeData.fundInfo.fundTypeDetails
            })
            this.fundTypeDetails=fundTypeobj.fundTypeDetailName;
          }
        }else{
          this.options = [];
          this.$message({
            type:"error",
            message:"获取基金类型失败"
          })
        }
      }).catch(()=>{

      })
      
    },


    editActivedEvent({ row, column }, event) {
      // row.customDate = ""
      if(row.openFrequence=="Y"){
        // 每年
        this.openRuleArr = this.YopenRuleArr;
      }else if(row.openFrequence=="S"){
        // 每半年
        this.openRuleArr = this.SopenRuleArr;
      }else if(row.openFrequence=="Q"){
        // 每季度
        this.openRuleArr = this.QopenRuleArr;
      }else if(row.openFrequence=="M"){
        // 每月
        this.openRuleArr = this.MopenRuleArr;
      }else if(row.openFrequence=="MC"){
        // 固定月
        this.openRuleArr = this.MCopenRuleArr;
      }else if(row.openFrequence=="DC"){
        // 固定日
        this.openRuleArr = this.DCopenRuleArr;
      }else{
        this.openRuleArr = []
      }
    },
    // 开放频率change
    openFrequenceChange({row}){
      row.openRule = ""
      row.customDate = ""
      if(row.openFrequence=="Y"){
        // 每年
        this.openRuleArr = this.YopenRuleArr;
        console.log(this.openRuleArr);
      }else if(row.openFrequence=="S"){
        // 每半年
        this.openRuleArr = this.SopenRuleArr;
      }else if(row.openFrequence=="Q"){
        // 每季度
        this.openRuleArr = this.QopenRuleArr;
      }else if(row.openFrequence=="M"){
        // 每月
        this.openRuleArr = this.MopenRuleArr;
      }else if(row.openFrequence=="MC"){
        // 固定月
        this.openRuleArr = this.MCopenRuleArr;
      }else if(row.openFrequence=="DC"){
        // 固定日
        this.openRuleArr = this.DCopenRuleArr;
      }
      
    },
    // 开放规则change
    openRuleChange({row}){
      if(row.openRule=="LT"){
        // 最后一个交易日

      }else if(row.openRule=="FT"){
        // 第一个交易日

      }else if(row.openRule=="D"){
        // 每个交易日

      }else if(row.openRule=="DC"){
        // 固定日

      }
    },
    pickerChange(data){
      this.$nextTick(()=>{
        this.$forceUpdate()
      })
      console.log(data,'qqqqq');
    }
  },
};
</script>
<style rel="stylesheet/scss" lang="scss">
.productNewStyle {
  .el_form_item {
    width: 188px;
  }
  .el-tabs__content{
     margin:0 auto;
     width: 100% !important
  }
  .fkheight {
    height: 450px;
    overflow-y: scroll;
  }
  .red{
    color: red !important;
  }
  .red .el-input__inner{
    color: red !important;
  }
  .red .el-textarea__inner {
   color: red !important;
 }
 .height_34px{
   .el-input__inner{
     height: 34px !important;
   }
 }
 .input__inner_red{
   .el-input__inner{
     border-color: red;
   }
 }

}
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
  .vxe-dropdown--panel {
    z-index: 9999 !important;
  }
  .vxe-table--tooltip-wrapper.vxe-table--valid-error {
    display: none;
  }
  //日期框
  .vxe-input--panel.type--date,
  .vxe-input--panel.type--month,
  .vxe-input--panel.type--week,
  .vxe-input--panel.type--year {
    z-index: 9998 !important;
  }
  .vxe-select--panel {
    z-index: 9997 !important;
  }

.el-select-group__wrap{
  .el-select-group__title{
    color: #303133;
  }
  .el-select-group{
    .el-select-dropdown__item{
      padding-left: 36px !important;
    }
  }

}

</style>

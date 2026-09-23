<template>
  <div style="productDetailStyle">
    <el-form
      :rules="commonRules"
      :inline="false"
      label-width="180px"
      label-position="right"
      ref="formInline"
      :model="formInline"
      class="demo-form-inline form_inline_search"
      style="margin-top: 8px; margin-bottom: 10px"
    >
      <el-tabs v-model="activeName" @tab-click="handleClick">
        <el-tab-pane label="基础信息" name="first">
          <span slot="label"
            >基础信息<i
              v-show="jcxxI_show"
              style="color: red"
              class="el-icon-warning"
            ></i
          ></span>
        </el-tab-pane>
        <el-tab-pane label="交易信息" name="second">
          <span slot="label"
            >交易信息<i
              v-show="jyxxI_show"
              style="color: red"
              class="el-icon-warning"
            ></i
          ></span>
        </el-tab-pane>
        <el-tab-pane label="费用信息" name="third">
          <span slot="label"
            >费用信息<i
              v-show="fyxxI_show"
              style="color: red"
              class="el-icon-warning"
            ></i
          ></span>
        </el-tab-pane>
        <el-tab-pane label="收益分配" name="fourth">
          <span slot="label"
            >收益分配<i
              v-show="syxxI_show"
              style="color: red"
              class="el-icon-warning"
            ></i
          ></span>
        </el-tab-pane>
        <el-tab-pane label="投资风控" name="six">
          <span slot="label"
            >投资风控<i
              v-show="tzxxI_show"
              style="color: red"
              class="el-icon-warning"
            ></i
          ></span>
        </el-tab-pane>
        <!-- <el-tab-pane label="分级关系" name="hierarchical_relationship">
            <hierarchicalRelationship ref="relationShip" v-if='relationShow'></hierarchicalRelationship>
          </el-tab-pane> -->
        <el-tab-pane label="销售方式" name="eight"></el-tab-pane>
        <el-tab-pane label="开放日" name="nine"></el-tab-pane>
        <el-tab-pane label="基金经理" name="eleven"></el-tab-pane>
        <el-tab-pane label="联系人" name="seven"></el-tab-pane>
      </el-tabs>
      <div v-show="jcxx_show" id="jcxxDiv" class="product_detail">
        <el-row>
          <el-col :span="12">
            <el-form-item label="产品名称">
              <span>{{ formInline.fundName | noDataFilter }}</span>
              <span
                v-if="
                  tooltipIsDisabled(beforeData.fundName, formInline.fundName)
                "
                style="color: red"
                >{{ tips(beforeData.fundName) | noDataFilter }}</span
              >
            </el-form-item>
            <el-form-item label="英文名称">
              <span>{{ formInline.fundNameEn | noDataFilter }}</span>
              <span
                v-if="
                  tooltipIsDisabled(
                    beforeData.fundNameEn,
                    formInline.fundNameEn
                  )
                "
                style="color: red"
                >{{ tips(beforeData.fundNameEn) | noDataFilter }}</span
              >
            </el-form-item>
            <el-form-item label="托管人名称">
              <span>{{
                getInitName(formInline.trustorCode) | noDataFilter
              }}</span>
              <span
                v-if="
                  tooltipIsDisabled(
                    beforeData.trustorCode,
                    formInline.trustorCode
                  )
                "
                style="color: red"
                >{{
                  tips(getInitName(beforeData.trustorCode)) | noDataFilter
                }}</span
              >
            </el-form-item>
            <el-form-item label="证券营业部">
              <span>{{ formInline.operateDept | noDataFilter }}</span>
              <span
                v-if="
                  tooltipIsDisabled(
                    beforeData.operateDept,
                    formInline.operateDept
                  )
                "
                style="color: red"
                >{{ tips(beforeData.operateDept) | noDataFilter }}</span
              >
            </el-form-item>
            <el-form-item label="产品存续期限">
              <span>{{ formInline.holdYear | noDataFilter }}</span>
              <span
                v-if="
                  tooltipIsDisabled(beforeData.holdYear, formInline.holdYear)
                "
                style="color: red"
                >{{ tips(beforeData.holdYear) | noDataFilter }}</span
              >
            </el-form-item>
            <el-form-item label="风险等级">
              <span>{{
                getDataName("fundRiskLevelType", formInline.riskLevel)
                  | noDataFilter
              }}</span>
              <span
                v-if="
                  tooltipIsDisabled(beforeData.riskLevel, formInline.riskLevel)
                "
                style="color: red"
                >{{
                  tips(getDataName("fundRiskLevelType", beforeData.riskLevel))
                    | noDataFilter
                }}</span
              >
            </el-form-item>
            <el-form-item label="产品备案代码">
              <span>{{ formInline.recordCode | noDataFilter }}</span>
              <span
                v-if="
                  tooltipIsDisabled(
                    beforeData.recordCode,
                    formInline.recordCode
                  )
                "
                style="color: red"
                >{{ tips(beforeData.recordCode) | noDataFilter }}</span
              >
            </el-form-item>
            <el-form-item label="分级产品代码">
              <div class="gradeStyle">
                <span>{{ formInline.isGrade | noDataFilter }}</span>
                <span
                  v-if="
                    tooltipIsDisabled(beforeData.isGrade, formInline.isGrade)
                  "
                  style="color: red"
                  >{{ tips(beforeData.isGrade) | noDataFilter }}</span
                >
              </div>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="产品代码">
              <span>{{ formInline.fundCode | noDataFilter }}</span>
              <span
                v-if="
                  tooltipIsDisabled(beforeData.fundCode, formInline.fundCode)
                "
                style="color: red"
                >{{ tips(beforeData.fundCode) | noDataFilter }}</span
              >
            </el-form-item>
            <el-form-item label="管理人名称">
              <span>{{
                getInitName(formInline.managerCode) | noDataFilter
              }}</span>
              <span
                v-show="
                  tooltipIsDisabled(
                    beforeData.managerCode,
                    formInline.managerCode
                  )
                "
                style="color: red"
                >{{
                  tips(getInitName(beforeData.managerCode)) | noDataFilter
                }}</span
              >
            </el-form-item>
            <el-form-item label="基金服务机构">
              <span>{{
                getInitName(formInline.operatorCode) | noDataFilter
              }}</span>
              <span
                v-show="
                  tooltipIsDisabled(
                    beforeData.operatorCode,
                    formInline.operatorCode
                  )
                "
                style="color: red"
                >{{
                  tips(getInitName(beforeData.operatorCode)) | noDataFilter
                }}</span
              >
            </el-form-item>
            <el-form-item label="基金成立日期">
              <span>{{ formInline.setupDate | noDataFilter }}</span>
              <span
                v-show="
                  tooltipIsDisabled(beforeData.setupDate, formInline.setupDate)
                "
                style="color: red"
                >{{ tips(beforeData.setupDate) | noDataFilter }}</span
              >
            </el-form-item>
            <el-form-item label="基金备案日期">
              <span>{{ formInline.recordDate | noDataFilter }}</span>
              <span
                v-show="
                  tooltipIsDisabled(
                    beforeData.recordDate,
                    formInline.recordDate
                  )
                "
                style="color: red"
                >{{ tips(beforeData.recordDate) | noDataFilter }}</span
              >
            </el-form-item>
            <el-form-item label="运作方式">
              <span>{{
                getDataName("operateType", formInline.operateType)
                  | noDataFilter
              }}</span>
              <span
                v-show="
                  tooltipIsDisabled(
                    beforeData.operateType,
                    formInline.operateType
                  )
                "
                style="color: red"
                >{{
                  tips(getDataName("operateType", beforeData.operateType))
                    | noDataFilter
                }}</span
              >
            </el-form-item>
            <el-form-item label="产品状态">
              <span>{{
                getDataName("fundState", formInline.fundState) | noDataFilter
              }}</span>
              <span
                v-show="
                  tooltipIsDisabled(beforeData.fundState, formInline.fundState)
                "
                style="color: red"
                >{{
                  tips(getDataName("fundState", beforeData.fundState))
                    | noDataFilter
                }}</span
              >
            </el-form-item>
          </el-col>
        </el-row>
      </div>
      <div v-show="jyxx_show" id="jyxxDiv" class="product_detail">
        <el-row>
          <el-col :span="22" :offset="2">
            <el-row>
              <el-col :span="11">
                <el-form-item label="封闭期">
                  <span>{{ formInline.blockDate | noDataFilter }}</span>
                  <span
                    v-show="
                      tooltipIsDisabled(
                        beforeData.blockDate,
                        formInline.blockDate
                      )
                    "
                    style="color: red"
                    >{{ tips(beforeData.blockDate) | noDataFilter }}</span
                  >
                </el-form-item>
                <el-form-item label="追加认申购（不含费）">
                  <span>{{
                    formInline.purchaseDiffAppend | noDataFilter
                  }}</span>
                  <span
                    v-show="
                      tooltipIsDisabled(
                        beforeData.purchaseDiffAppend,
                        formInline.purchaseDiffAppend
                      )
                    "
                    style="color: red"
                    >{{
                      tips(beforeData.purchaseDiffAppend) | noDataFilter
                    }}</span
                  >
                </el-form-item>
                <el-form-item label="认购资金交收天数">
                  <span>{{
                    getDataName(
                      "fundSubscribeDeliverDayType",
                      formInline.subscribeDeliverDay
                    ) | noDataFilter
                  }}</span>
                  <span
                    v-show="
                      tooltipIsDisabled(
                        beforeData.subscribeDeliverDay,
                        formInline.subscribeDeliverDay
                      )
                    "
                    style="color: red"
                    >{{
                      tips(
                        getDataName(
                          "fundSubscribeDeliverDayType",
                          beforeData.subscribeDeliverDay
                        )
                      ) | noDataFilter
                    }}</span
                  >
                </el-form-item>
                <el-form-item label="申购交易确认天数">
                  <span>{{
                    getDataName(
                      "fundApplyConfirmDayType",
                      formInline.applyConfirmDay
                    ) | noDataFilter
                  }}</span>
                  <span
                    v-show="
                      tooltipIsDisabled(
                        beforeData.applyConfirmDay,
                        formInline.applyConfirmDay
                      )
                    "
                    style="color: red"
                    >{{
                      tips(
                        getDataName(
                          "fundApplyConfirmDayType",
                          beforeData.applyConfirmDay
                        )
                      ) | noDataFilter
                    }}</span
                  >
                </el-form-item>
                <el-form-item label="申购费率">
                  <span>{{ formInline.applyRate | noDataFilter }}</span>
                  <span
                    v-show="
                      tooltipIsDisabled(
                        beforeData.applyRate,
                        formInline.applyRate
                      )
                    "
                    style="color: red"
                    >{{ tips(beforeData.applyRate) | noDataFilter }}</span
                  >
                </el-form-item>
                <el-form-item label="销售服务费计提">
                  <span>{{
                    getDataName("saleFeePrepare", formInline.saleFeePrepare)
                      | noDataFilter
                  }}</span>
                  <span
                    v-show="
                      tooltipIsDisabled(
                        beforeData.saleFeePrepare,
                        formInline.saleFeePrepare
                      )
                    "
                    style="color: red"
                    >{{
                      tips(
                        getDataName("saleFeePrepare", beforeData.saleFeePrepare)
                      ) | noDataFilter
                    }}</span
                  >
                </el-form-item>
              </el-col>
              <el-col :span="11" :offset="2">
                <el-form-item label="认申购起点（不含费）元">
                  <span>{{ formInline.purchasePoint | noDataFilter }}</span>
                  <span
                    v-show="
                      tooltipIsDisabled(
                        beforeData.purchasePoint,
                        formInline.purchasePoint
                      )
                    "
                    style="color: red"
                    >{{ tips(beforeData.purchasePoint) | noDataFilter }}</span
                  >
                </el-form-item>
                <el-form-item label="认购交易确认天数">
                  <span>{{
                    getDataName(
                      "fundSubscribeConfirmDayType",
                      formInline.subscribeConfirmDay
                    ) | noDataFilter
                  }}</span>
                  <span
                    v-show="
                      tooltipIsDisabled(
                        beforeData.subscribeConfirmDay,
                        formInline.subscribeConfirmDay
                      )
                    "
                    style="color: red"
                    >{{
                      tips(
                        getDataName(
                          "fundSubscribeConfirmDayType",
                          beforeData.subscribeConfirmDay
                        )
                      ) | noDataFilter
                    }}</span
                  >
                </el-form-item>
                <el-form-item label="认购费率">
                  <span>{{ formInline.subscribeRate | noDataFilter }}</span>
                  <span
                    v-show="
                      tooltipIsDisabled(
                        beforeData.subscribeRate,
                        formInline.subscribeRate
                      )
                    "
                    style="color: red"
                    >{{ tips(beforeData.subscribeRate) | noDataFilter }}</span
                  >
                </el-form-item>
                <el-form-item label="申购资金交收天数">
                  <span>{{
                    getDataName(
                      "fundApplyDeliverDayType",
                      formInline.applyDeliverDay
                    ) | noDataFilter
                  }}</span>
                  <span
                    v-show="
                      tooltipIsDisabled(
                        beforeData.applyDeliverDay,
                        formInline.applyDeliverDay
                      )
                    "
                    style="color: red"
                    >{{
                      tips(
                        getDataName(
                          "fundApplyDeliverDayType",
                          beforeData.applyDeliverDay
                        )
                      ) | noDataFilter
                    }}</span
                  >
                </el-form-item>
                <el-form-item label="销售服务费支付">
                  <span>{{
                    getDataName("saleFeePay", formInline.saleFeePay)
                      | noDataFilter
                  }}</span>
                  <span
                    v-show="
                      tooltipIsDisabled(
                        beforeData.saleFeePay,
                        formInline.saleFeePay
                      )
                    "
                    style="color: red"
                    >{{
                      tips(getDataName("saleFeePay", beforeData.saleFeePay))
                        | noDataFilter
                    }}</span
                  >
                </el-form-item>
                <el-form-item label="赎回费率">
                  <span>{{ formInline.callRate | noDataFilter }}</span>
                  <span
                    v-show="
                      tooltipIsDisabled(
                        beforeData.callRate,
                        formInline.callRate
                      )
                    "
                    style="color: red"
                    >{{ tips(beforeData.callRate) | noDataFilter }}</span
                  >
                </el-form-item>
              </el-col>
            </el-row>
          </el-col>
        </el-row>
      </div>

      <div v-show="fyxx_show" id="fyxxDiv" class="product_detail">
        <el-row>
          <el-col :span="23" :offset="1">
            <el-form-item label="费用说明">
              <span>{{
                (getDataName(
                  "fundManageFeePrepareType",
                  formInline.manageFeePrepare
                ) +
                  "," +
                  getDataName("fundManageFeePayType", formInline.manageFeePay))
                  | noDataFilter
              }}</span>
              <span
                v-show="
                  tooltipIsDisabled(
                    (beforeData.manageFeePrepare || '') +
                      ',' +
                      (beforeData.manageFeePay || ''),
                    (formInline.manageFeePrepare || '') +
                      ',' +
                      (formInline.manageFeePay || '')
                  )
                "
                style="color: red"
                >{{
                  tips(
                    getDataName(
                      "fundManageFeePrepareType",
                      beforeData.manageFeePrepare
                    ) +
                      "," +
                      getDataName(
                        "fundManageFeePayType",
                        beforeData.manageFeePay
                      )
                  ) | noDataFilter
                }}</span
              >
            </el-form-item>
            <el-row>
              <el-col :span="10">
                <el-form-item label="管理费率">
                  <span>{{ formInline.manageRate | noDataFilter }}</span>
                  <span
                    v-show="
                      tooltipIsDisabled(
                        beforeData.manageRate,
                        formInline.manageRate
                      )
                    "
                    style="color: red"
                    >{{ tips(beforeData.manageRate) | noDataFilter }}</span
                  >
                </el-form-item>
                <el-form-item label="运营服务费">
                  <span>{{ formInline.operateRate | noDataFilter }}</span>
                  <span
                    v-show="
                      tooltipIsDisabled(
                        beforeData.operateRate,
                        formInline.operateRate
                      )
                    "
                    style="color: red"
                    >{{ tips(beforeData.operateRate) | noDataFilter }}</span
                  >
                </el-form-item>
                <!-- <el-tooltip :disabled="tooltipIsDisabled(beforeData.rewardPrepareType,formInline.rewardPrepareType)" :content="tips(getDataName('fundRewardPrepareType',beforeData.rewardPrepareType))" placement="bottom" effect="light">
                            <el-form-item label="业绩报酬计提">
                            <span :style="{'color':compareData(beforeData.rewardPrepareType,formInline.rewardPrepareType) ? 'red':''}">{{getDataName('fundRewardPrepareType',formInline.rewardPrepareType) | noDataFilter}}</span>
                          </el-form-item>
                      </el-tooltip> -->
                <el-form-item label="管理人账号">
                  <span>{{ formInline.manageAccount | noDataFilter }}</span>
                  <span
                    v-show="
                      tooltipIsDisabled(
                        beforeData.manageAccount,
                        formInline.manageAccount
                      )
                    "
                    style="color: red"
                    >{{ tips(beforeData.manageAccount) | noDataFilter }}</span
                  >
                </el-form-item>
                <el-form-item label="管理人开户银行名称">
                  <span>{{ formInline.manageBankName | noDataFilter }}</span>
                  <span
                    v-show="
                      tooltipIsDisabled(
                        beforeData.manageBankName,
                        formInline.manageBankName
                      )
                    "
                    style="color: red"
                    >{{ tips(beforeData.manageBankName) | noDataFilter }}</span
                  >
                </el-form-item>
              </el-col>
              <el-col :span="10" :offset="2">
                <el-form-item label="托管费率">
                  <span>{{ formInline.trustRate | noDataFilter }}</span>
                  <span
                    v-show="
                      tooltipIsDisabled(
                        beforeData.trustRate,
                        formInline.trustRate
                      )
                    "
                    style="color: red"
                    >{{ tips(beforeData.trustRate) | noDataFilter }}</span
                  >
                </el-form-item>
                <el-form-item label="业绩报酬计提">
                  <span>{{
                    getDataName("fundRewardType", formInline.rewardType)
                      | noDataFilter
                  }}</span>
                  <span
                    v-show="
                      tooltipIsDisabled(
                        beforeData.rewardType,
                        formInline.rewardType
                      )
                    "
                    style="color: red"
                    >{{
                      tips(getDataName("fundRewardType", beforeData.rewardType))
                        | noDataFilter
                    }}</span
                  >
                </el-form-item>
                <el-form-item label="管理人收费账户名称">
                  <span>{{ formInline.manageAccountName | noDataFilter }}</span>
                  <span
                    v-show="
                      tooltipIsDisabled(
                        beforeData.manageAccountName,
                        formInline.manageAccountName
                      )
                    "
                    style="color: red"
                    >{{
                      tips(beforeData.manageAccountName) | noDataFilter
                    }}</span
                  >
                </el-form-item>
              </el-col>
            </el-row>
          </el-col>
        </el-row>
      </div>

      <div v-show="syfp_show" id="syfpDiv" class="product_detail">
        <el-row>
          <el-col :span="23" :offset="1">
            <el-form-item label="收益分配说明">
              <span>{{ formInline.incomePortionDesc | noDataFilter }}</span>
              <span
                v-show="
                  tooltipIsDisabled(
                    beforeData.incomePortionDesc,
                    formInline.incomePortionDesc
                  )
                "
                style="color: red"
                >{{ tips(beforeData.incomePortionDesc) | noDataFilter }}</span
              >
            </el-form-item>
            <el-row>
              <el-col :span="10">
                <el-form-item label="分配次数">
                  <span>{{
                    getDataName(
                      "fundPortionNumberType",
                      formInline.portionNumber
                    ) | noDataFilter
                  }}</span>
                  <span
                    v-show="
                      tooltipIsDisabled(
                        beforeData.portionNumber,
                        formInline.portionNumber
                      )
                    "
                    style="color: red"
                    >{{
                      tips(
                        getDataName(
                          "fundPortionNumberType",
                          beforeData.portionNumber
                        )
                      ) | noDataFilter
                    }}</span
                  >
                </el-form-item>
                <el-form-item label="预估数据以及计算报表">
                  <span>{{
                    getDataName("fundDataExpectType", formInline.dataExpect)
                      | noDataFilter
                  }}</span>
                  <span
                    v-show="
                      tooltipIsDisabled(
                        beforeData.dataExpect,
                        formInline.dataExpect
                      )
                    "
                    style="color: red"
                    >{{
                      tips(
                        getDataName("fundDataExpectType", beforeData.dataExpect)
                      ) | noDataFilter
                    }}</span
                  >
                </el-form-item>
                <el-form-item label="分红资金交收">
                  <span>{{
                    getDataName("fundBonusDeliverType", formInline.bonusDeliver)
                      | noDataFilter
                  }}</span>
                  <span
                    v-show="
                      tooltipIsDisabled(
                        beforeData.bonusDeliver,
                        formInline.bonusDeliver
                      )
                    "
                    style="color: red"
                    >{{
                      tips(
                        getDataName(
                          "fundBonusDeliverType",
                          beforeData.bonusDeliver
                        )
                      ) | noDataFilter
                    }}</span
                  >
                </el-form-item>
              </el-col>
              <el-col :span="10" :offset="2">
                <el-form-item label="提交分红流程">
                  <span>{{
                    getDataName("fundBonusProcessType", formInline.bonusProcess)
                      | noDataFilter
                  }}</span>
                  <span
                    v-show="
                      tooltipIsDisabled(
                        beforeData.bonusProcess,
                        formInline.bonusProcess
                      )
                    "
                    style="color: red"
                    >{{
                      tips(
                        getDataName(
                          "fundBonusProcessType",
                          beforeData.bonusProcess
                        )
                      ) | noDataFilter
                    }}</span
                  >
                </el-form-item>
                <el-form-item label="分红数据确认">
                  <span>{{
                    getDataName("fundBonusConfimType", formInline.bonusConfim)
                      | noDataFilter
                  }}</span>
                  <span
                    v-show="
                      tooltipIsDisabled(
                        beforeData.bonusConfim,
                        formInline.bonusConfim
                      )
                    "
                    style="color: red"
                    >{{
                      tips(
                        getDataName(
                          "fundBonusConfimType",
                          beforeData.bonusConfim
                        )
                      ) | noDataFilter
                    }}</span
                  >
                </el-form-item>
              </el-col>
            </el-row>
            <!-- <el-form-item label="认购交易确认天数" >
                   <span>{{formInline.name | noDataFilter}}</span>
                 </el-form-item>

                   <el-form-item label="认购资金交收天数">
                   <span>{{formInline.name | noDataFilter}}</span>
                 </el-form-item> -->
          </el-col>
        </el-row>
      </div>

      <div v-if="zhxx_show" class="product_detail">
        <el-row>
          <el-col :span="22" :offset="2">
            <el-row>
              <el-col :span="11">
                <el-tooltip
                  :disabled="
                    tooltipIsDisabled(
                      beforeData.fiduciaryName,
                      formInline.fiduciaryName
                    )
                  "
                  :content="tips(beforeData.fiduciaryName)"
                  placement="bottom"
                  effect="light"
                >
                  <el-form-item label="托管户名称">
                    <span
                      :style="{
                        color: compareData(
                          beforeData.fiduciaryName,
                          formInline.fiduciaryName
                        )
                          ? 'red'
                          : '',
                      }"
                      >{{ formInline.fiduciaryName | noDataFilter }}</span
                    >
                  </el-form-item>
                </el-tooltip>
                <el-tooltip
                  :disabled="
                    tooltipIsDisabled(
                      beforeData.fiduciaryBank,
                      formInline.fiduciaryBank
                    )
                  "
                  :content="tips(beforeData.fiduciaryBank)"
                  placement="bottom"
                  effect="light"
                >
                  <el-form-item label="托管户开户银行">
                    <span
                      :style="{
                        color: compareData(
                          beforeData.fiduciaryBank,
                          formInline.fiduciaryBank
                        )
                          ? 'red'
                          : '',
                      }"
                      >{{ formInline.fiduciaryBank | noDataFilter }}</span
                    >
                  </el-form-item>
                </el-tooltip>
                <el-tooltip
                  :disabled="
                    tooltipIsDisabled(
                      beforeData.raiseName,
                      formInline.raiseName
                    )
                  "
                  :content="tips(beforeData.raiseName)"
                  placement="bottom"
                  effect="light"
                >
                  <el-form-item label="募集户名称">
                    <span
                      :style="{
                        color: compareData(
                          beforeData.raiseName,
                          formInline.raiseName
                        )
                          ? 'red'
                          : '',
                      }"
                      >{{ formInline.raiseName | noDataFilter }}</span
                    >
                  </el-form-item>
                </el-tooltip>
                <el-tooltip
                  :disabled="
                    tooltipIsDisabled(
                      beforeData.raiseBank,
                      formInline.raiseBank
                    )
                  "
                  :content="tips(beforeData.raiseBank)"
                  placement="bottom"
                  effect="light"
                >
                  <el-form-item label="募集账户开户银行">
                    <span
                      :style="{
                        color: compareData(
                          beforeData.raiseBank,
                          formInline.raiseBank
                        )
                          ? 'red'
                          : '',
                      }"
                      >{{ formInline.raiseBank | noDataFilter }}</span
                    >
                  </el-form-item>
                </el-tooltip>
                <el-tooltip
                  :disabled="
                    tooltipIsDisabled(
                      beforeData.securityName,
                      formInline.securityName
                    )
                  "
                  :content="tips(beforeData.securityName)"
                  placement="bottom"
                  effect="light"
                >
                  <el-form-item label="证券账户名称">
                    <span
                      :style="{
                        color: compareData(
                          beforeData.securityName,
                          formInline.securityName
                        )
                          ? 'red'
                          : '',
                      }"
                      >{{ formInline.securityName | noDataFilter }}</span
                    >
                  </el-form-item>
                </el-tooltip>
                <el-tooltip
                  :disabled="
                    tooltipIsDisabled(
                      beforeData.stockAccountSh,
                      formInline.stockAccountSh
                    )
                  "
                  :content="tips(beforeData.stockAccountSh)"
                  placement="bottom"
                  effect="light"
                >
                  <el-form-item label="上海证券账户-股票交易">
                    <span
                      :style="{
                        color: compareData(
                          beforeData.stockAccountSh,
                          formInline.stockAccountSh
                        )
                          ? 'red'
                          : '',
                      }"
                      >{{ formInline.stockAccountSh | noDataFilter }}</span
                    >
                  </el-form-item>
                </el-tooltip>
                <el-tooltip
                  :disabled="
                    tooltipIsDisabled(
                      beforeData.stockAccountSz,
                      formInline.stockAccountSz
                    )
                  "
                  :content="tips(beforeData.stockAccountSz)"
                  placement="bottom"
                  effect="light"
                >
                  <el-form-item label="深圳证券账户-股票交易">
                    <span
                      :style="{
                        color: compareData(
                          beforeData.stockAccountSz,
                          formInline.stockAccountSz
                        )
                          ? 'red'
                          : '',
                      }"
                      >{{ formInline.stockAccountSz | noDataFilter }}</span
                    >
                  </el-form-item>
                </el-tooltip>
                <el-tooltip
                  :disabled="
                    tooltipIsDisabled(
                      beforeData.securityCapitalAccount,
                      formInline.securityCapitalAccount
                    )
                  "
                  :content="tips(beforeData.securityCapitalAccount)"
                  placement="bottom"
                  effect="light"
                >
                  <el-form-item label="证券资金账户">
                    <span
                      :style="{
                        color: compareData(
                          beforeData.securityCapitalAccount,
                          formInline.securityCapitalAccount
                        )
                          ? 'red'
                          : '',
                      }"
                      >{{
                        formInline.securityCapitalAccount | noDataFilter
                      }}</span
                    >
                  </el-form-item>
                </el-tooltip>
                <el-tooltip
                  :disabled="
                    tooltipIsDisabled(
                      beforeData.optionAccount,
                      formInline.optionAccount
                    )
                  "
                  :content="tips(beforeData.optionAccount)"
                  placement="bottom"
                  effect="light"
                >
                  <el-form-item label="期权账号">
                    <span
                      :style="{
                        color: compareData(
                          beforeData.optionAccount,
                          formInline.optionAccount
                        )
                          ? 'red'
                          : '',
                      }"
                      >{{ formInline.optionAccount | noDataFilter }}</span
                    >
                  </el-form-item>
                </el-tooltip>
              </el-col>

              <el-col :span="11" :offset="1">
                <el-tooltip
                  :disabled="
                    tooltipIsDisabled(
                      beforeData.fiduciaryAccount,
                      formInline.fiduciaryAccount
                    )
                  "
                  :content="tips(beforeData.fiduciaryAccount)"
                  placement="bottom"
                  effect="light"
                >
                  <el-form-item label="托管户账号">
                    <span
                      :style="{
                        color: compareData(
                          beforeData.fiduciaryAccount,
                          formInline.fiduciaryAccount
                        )
                          ? 'red'
                          : '',
                      }"
                      >{{ formInline.fiduciaryAccount | noDataFilter }}</span
                    >
                  </el-form-item>
                </el-tooltip>
                <el-tooltip
                  :disabled="
                    tooltipIsDisabled(
                      beforeData.fiduciaryYield,
                      formInline.fiduciaryYield
                    )
                  "
                  :content="tips(beforeData.fiduciaryYield)"
                  placement="bottom"
                  effect="light"
                >
                  <el-form-item label="托管户年利率">
                    <span
                      :style="{
                        color: compareData(
                          beforeData.fiduciaryYield,
                          formInline.fiduciaryYield
                        )
                          ? 'red'
                          : '',
                      }"
                      >{{ formInline.fiduciaryYield | noDataFilter }}</span
                    >
                  </el-form-item>
                </el-tooltip>
                <el-tooltip
                  :disabled="
                    tooltipIsDisabled(
                      beforeData.raiseAccount,
                      formInline.raiseAccount
                    )
                  "
                  :content="tips(beforeData.raiseAccount)"
                  placement="bottom"
                  effect="light"
                >
                  <el-form-item label="募集户账号">
                    <span
                      :style="{
                        color: compareData(
                          beforeData.raiseAccount,
                          formInline.raiseAccount
                        )
                          ? 'red'
                          : '',
                      }"
                      >{{ formInline.raiseAccount | noDataFilter }}</span
                    >
                  </el-form-item>
                </el-tooltip>
                <el-tooltip
                  :disabled="
                    tooltipIsDisabled(
                      beforeData.raiseAccountBig,
                      formInline.raiseAccountBig
                    )
                  "
                  :content="tips(beforeData.raiseAccountBig)"
                  placement="bottom"
                  effect="light"
                >
                  <el-form-item label="募集账户大额支付号">
                    <span
                      :style="{
                        color: compareData(
                          beforeData.raiseAccountBig,
                          formInline.raiseAccountBig
                        )
                          ? 'red'
                          : '',
                      }"
                      >{{ formInline.raiseAccountBig | noDataFilter }}</span
                    >
                  </el-form-item>
                </el-tooltip>
                <el-tooltip
                  :disabled="
                    tooltipIsDisabled(
                      beforeData.securityAccount,
                      formInline.securityAccount
                    )
                  "
                  :content="tips(beforeData.securityAccount)"
                  placement="bottom"
                  effect="light"
                >
                  <el-form-item label="一码通证券账户号码">
                    <span
                      :style="{
                        color: compareData(
                          beforeData.securityAccount,
                          formInline.securityAccount
                        )
                          ? 'red'
                          : '',
                      }"
                      >{{ formInline.securityAccount | noDataFilter }}</span
                    >
                  </el-form-item>
                </el-tooltip>
                <el-tooltip
                  :disabled="
                    tooltipIsDisabled(
                      beforeData.optionAccountSh,
                      formInline.optionAccountSh
                    )
                  "
                  :content="tips(beforeData.optionAccountSh)"
                  placement="bottom"
                  effect="light"
                >
                  <el-form-item label="上海证券账户-期权交易">
                    <span
                      :style="{
                        color: compareData(
                          beforeData.optionAccountSh,
                          formInline.optionAccountSh
                        )
                          ? 'red'
                          : '',
                      }"
                      >{{ formInline.optionAccountSh | noDataFilter }}</span
                    >
                  </el-form-item>
                </el-tooltip>
                <el-tooltip
                  :disabled="
                    tooltipIsDisabled(
                      beforeData.optionAccountSz,
                      formInline.optionAccountSz
                    )
                  "
                  :content="tips(beforeData.optionAccountSz)"
                  placement="bottom"
                  effect="light"
                >
                  <el-form-item label="深圳证券账户-期权交易">
                    <span
                      :style="{
                        color: compareData(
                          beforeData.optionAccountSz,
                          formInline.optionAccountSz
                        )
                          ? 'red'
                          : '',
                      }"
                      >{{ formInline.optionAccountSz | noDataFilter }}</span
                    >
                  </el-form-item>
                </el-tooltip>
                <el-tooltip
                  :disabled="
                    tooltipIsDisabled(
                      beforeData.futuresAccount,
                      formInline.futuresAccount
                    )
                  "
                  :content="tips(beforeData.futuresAccount)"
                  placement="bottom"
                  effect="light"
                >
                  <el-form-item label="期货账号">
                    <span
                      :style="{
                        color: compareData(
                          beforeData.futuresAccount,
                          formInline.futuresAccount
                        )
                          ? 'red'
                          : '',
                      }"
                      >{{ formInline.futuresAccount | noDataFilter }}</span
                    >
                  </el-form-item>
                </el-tooltip>
              </el-col>
            </el-row>
          </el-col>
        </el-row>
      </div>

      <div v-show="tzfk_show" id="tzfkDiv" class="product_detail">
        <el-row>
          <el-col :span="23" :offset="1">
            <el-tooltip
              :disabled="tooltipIsDisabled(beforeFundInvests, fundInvests)"
              :content="tips(beforeFundInvests)"
              placement="bottom"
              effect="light"
            >
              <el-form-item label="投资范围">
                <div v-if="afterfundInvests.length > 0" class="product_detail">
                  <div
                    class="product_news_box"
                    v-for="(item, index) in afterfundInvests"
                    :key="index"
                  >
                    <i class="el-icon-tickets"></i>
                    <span
                      :style="{
                        color: compareData(beforeFundInvests, fundInvests)
                          ? 'red'
                          : '',
                      }"
                      >{{ item | noDataFilter }}</span
                    >
                  </div>
                </div>
                <span v-if="afterfundInvests.length == 0"> 暂无数据 </span>
              </el-form-item>
            </el-tooltip>
            <el-form-item label="投资限制">
              <span>{{ formInline.investLimit | noDataFilter }}</span>
              <span
                v-show="
                  tooltipIsDisabled(
                    beforeData.investLimit,
                    formInline.investLimit
                  )
                "
                style="color: red"
                >{{ tips(beforeData.investLimit) | noDataFilter }}</span
              >
            </el-form-item>
            <el-form-item label="预警线">
              <span>{{ formInline.warnPoint | noDataFilter }}</span>
              <span
                v-show="
                  tooltipIsDisabled(beforeData.warnPoint, formInline.warnPoint)
                "
                style="color: red"
                >{{ tips(beforeData.warnPoint) | noDataFilter }}</span
              >
            </el-form-item>
            <el-form-item label="止损线">
              <span>{{ formInline.lossPoint | noDataFilter }}</span>
              <span
                v-show="
                  tooltipIsDisabled(beforeData.lossPoint, formInline.lossPoint)
                "
                style="color: red"
                >{{ tips(beforeData.lossPoint) | noDataFilter }}</span
              >
            </el-form-item>
          </el-col>
        </el-row>
      </div>
      <div v-show="lxr_show" class="product_detail">
        <el-row>
          <el-col :span="23" :offset="1">
            <el-table :data="tableDataContact" stripe style="width: 100%">
              <!-- :header-cell-style="{background:'#409EFF !important',color:'black'}" -->
              <el-table-column
                prop="contactType"
                label="联系人类型"
                width="180"
              >
              </el-table-column>
              <el-table-column
                prop="contactName"
                label="联系人名称"
                width="180"
              >
              </el-table-column>
              <el-table-column prop="contactPhone" label="联系人电话">
              </el-table-column>
              <el-table-column prop="contactMail" label="联系人邮箱">
              </el-table-column>
            </el-table>
          </el-col>
        </el-row>
      </div>

      <div v-show="xsfs_show" class="product_detail">
        <el-row>
          <el-col :span="23" :offset="1">
            <el-table :data="tableDataSaller" stripe style="width: 100%">
              <!-- :header-cell-style="{background:'#409EFF !important',color:'black'}" -->
              <el-table-column prop="sallerName" label="渠道名称" width="180">
              </el-table-column>
              <el-table-column prop="sallerCode" label="渠道编码" width="180">
              </el-table-column>
              <el-table-column prop="sallerType" label="销售方式">
                <template slot-scope="scope">
                  <span>{{
                    getDataName("fundSaleType", scope.row.sallerType)
                      | noDataFilter
                  }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="beginDate" label="开始日期">
              </el-table-column>
              <el-table-column prop="endDate" label="结束日期">
              </el-table-column>
            </el-table>
          </el-col>
        </el-row>
      </div>

      <div v-show="kfr_show" class="product_detail">
        <el-row>
          <el-col :span="23" :offset="1">
            <el-table :data="tableDataOpen" stripe style="width: 100%">
              <!-- :header-cell-style="{background:'#409EFF !important',color:'black'}" -->
              <el-table-column
                prop="openFrequence"
                label="开放频率"
                width="180"
              >
                <template slot-scope="scope">
                  <span>{{
                    getDataName("fundOpenFrequence", scope.row.openFrequence)
                      | noDataFilter
                  }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="openRule" label="开放规则" width="180">
                <template slot-scope="scope">
                  <span>{{
                    getDataName("fundOpenRule", scope.row.openRule)
                      | noDataFilter
                  }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="beginDate" label="规则生效日期">
              </el-table-column>
              <el-table-column prop="endDate" label="规则失效日期">
              </el-table-column>
            </el-table>
          </el-col>
        </el-row>
      </div>

      <div v-show="fundManager_show" class="product_detail">
        <el-row>
          <el-col :span="23" :offset="1">
            <el-table :data="tableDataFundManager" stripe style="width: 100%">
              <!-- :header-cell-style="{background:'#409EFF !important',color:'black'}" -->
              <el-table-column prop="managerName" label="基金经理" width="180">
                <template slot-scope="scope">
                  <span>{{ scope.row.managerName | noDataFilter }}</span>
                </template>
              </el-table-column>
              <el-table-column
                prop="investStrategy"
                label="投资策略"
                width="180"
              >
                <template slot-scope="scope">
                  <span>{{ scope.row.investStrategy | noDataFilter }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="phone" label="联系电话"> </el-table-column>
              <el-table-column prop="email" label="联系邮箱"> </el-table-column>
            </el-table>
          </el-col>
        </el-row>
      </div>

      <div v-show="sh_show" style="margin-top: 10px">
        <el-row>
          <el-col :span="11" :offset="8">
            <el-form-item label="审核意见" prop="approveOpinion">
              <el-input
                v-model="formHandle.approveOpinion"
                type="textarea"
                :rows="2"
                maxlength="1000"
                show-word-limit
                style="width: 260px"
                placeholder="请输入审核意见"
                auto-complete="off"
              />
            </el-form-item>
            <el-button
              type="primary"
              v-btn="'fund.approve.submit'"
              :loading="countSubmit_btn"
              @click="updateStatus(1, '审核通过')"
              style="margin-bottom: 5px; margin-left: 58px"
              size="small"
              >审核通过</el-button
            >
            <el-button
              type="primary"
              v-btn="'fund.approve.submit'"
              :loading="countSubmit_btn"
              @click="updateStatus(0, '审核不通过')"
              style="margin-bottom: 5px"
              size="small"
              >审核不通过</el-button
            >
          </el-col>
        </el-row>
      </div>

      <div v-show="PageDataDetail.detailType == 2" style="margin-top: 10px">
        <el-row>
          <el-col :span="11" :offset="8">
            <el-form-item label="审核人">
              <span>{{ modifier }}</span>
            </el-form-item>

            <el-form-item label="审核意见">
              <span>{{ approveOpinion }}</span>
            </el-form-item>
          </el-col>
        </el-row>
      </div>
    </el-form>
  </div>
</template>

<script>
import commonFun from "@/filters/new_common";
import pageApi from "@/api/product/productSearch";
import productDictionary from "@/dataDictionary/product";
import pageExamineApi from "@/api/product/productExamine";
import hierarchicalRelationship from "./account/hierarchical-relationship.vue";
import productDetailJs from '@/mixinsModel/productDetail'
import $ from "jquery";
export default {
  name: "productDetail",
  mixins: [productDetailJs],
  components: {
    hierarchicalRelationship,
  },
  props: {
    PageDataDetail: {
      sh_show: false,
      fundCode: "", //查看详情
      id: "", //审核详情
      detailType: 0, //0查看详情，1审核详情
    },
  },
  data () {
    return {}
  },
  //页面加载后触发
  mounted() {
    this.sh_show = this.PageDataDetail.sh_show;
    let detailType = this.PageDataDetail.detailType;
    this.getEdims();
    this.initData();
    if (detailType == 0) {
      this.getSearchDetail();
    } else if (detailType == 1 || detailType == 2) {
      this.getExamineDetail();
    }
  },
  methods: {
    handleClick(tab, event) {
      let tabLabel = tab.label;
      if (tabLabel === "基础信息") {
        this.jcxx_show = true; //基础信息展示
        this.jyxx_show = false; //交易信息展示
        this.fyxx_show = false; //费用信息展示
        this.syfp_show = false; //收益分配展示
        this.zhxx_show = false; //账户信息展示
        this.tzfk_show = false; //投资风控展示
        this.lxr_show = false; //联系人展示
        this.xsfs_show = false; //销售方式展示
        this.kfr_show = false; //开放日展示
        this.fundManager_show = false;
        if (this.sh_show) {
          this.shtg_show = false;
          this.shbtg_show = true;
        }
      } else if (tabLabel === "交易信息") {
        this.jcxx_show = false; //基础信息展示
        this.jyxx_show = true; //交易信息展示
        this.fyxx_show = false; //费用信息展示
        this.syfp_show = false; //收益分配展示
        this.zhxx_show = false; //账户信息展示
        this.tzfk_show = false; //投资风控展示
        this.lxr_show = false; //联系人展示
        this.xsfs_show = false; //销售方式展示
        this.kfr_show = false; //开放日展示
        this.fundManager_show = false;
        if (this.sh_show) {
          this.shtg_show = false;
          this.shbtg_show = true;
        }
      } else if (tabLabel === "费用信息") {
        this.jcxx_show = false; //基础信息展示
        this.jyxx_show = false; //交易信息展示
        this.fyxx_show = true; //费用信息展示
        this.syfp_show = false; //收益分配展示
        this.zhxx_show = false; //账户信息展示
        this.tzfk_show = false; //投资风控展示
        this.lxr_show = false; //联系人展示
        this.xsfs_show = false; //销售方式展示
        this.kfr_show = false; //开放日展示
        this.fundManager_show = false;
        if (this.sh_show) {
          this.shtg_show = false;
          this.shbtg_show = true;
        }
      } else if (tabLabel === "收益分配") {
        this.jcxx_show = false; //基础信息展示
        this.jyxx_show = false; //交易信息展示
        this.fyxx_show = false; //费用信息展示
        this.syfp_show = true; //收益分配展示
        this.zhxx_show = false; //账户信息展示
        this.tzfk_show = false; //投资风控展示
        this.lxr_show = false; //联系人展示
        this.xsfs_show = false; //销售方式展示
        this.kfr_show = false; //开放日展示
        this.fundManager_show = false;
        if (this.sh_show) {
          this.shtg_show = false;
          this.shbtg_show = true;
        }
      } else if (tabLabel === "账户信息") {
        this.jcxx_show = false; //基础信息展示
        this.jyxx_show = false; //交易信息展示
        this.fyxx_show = false; //费用信息展示
        this.syfp_show = false; //收益分配展示
        this.zhxx_show = true; //账户信息展示
        this.tzfk_show = false; //投资风控展示
        this.lxr_show = false; //联系人展示
        this.xsfs_show = false; //销售方式展示
        this.kfr_show = false; //开放日展示
        this.fundManager_show = false;
        if (this.sh_show) {
          this.shtg_show = false;
          this.shbtg_show = true;
        }
      } else if (tabLabel === "投资风控") {
        this.jcxx_show = false; //基础信息展示
        this.jyxx_show = false; //交易信息展示
        this.fyxx_show = false; //费用信息展示
        this.syfp_show = false; //收益分配展示
        this.zhxx_show = false; //账户信息展示
        this.tzfk_show = true; //投资风控展示
        this.lxr_show = false; //联系人展示
        this.xsfs_show = false; //销售方式展示
        this.kfr_show = false; //开放日展示
        this.fundManager_show = false;
        if (this.sh_show) {
          this.shtg_show = false;
          this.shbtg_show = true;
        }
      } else if (tabLabel === "联系人") {
        this.jcxx_show = false; //基础信息展示
        this.jyxx_show = false; //交易信息展示
        this.fyxx_show = false; //费用信息展示
        this.syfp_show = false; //收益分配展示
        this.zhxx_show = false; //账户信息展示
        this.tzfk_show = false; //投资风控展示
        this.lxr_show = true; //联系人展示
        this.xsfs_show = false; //销售方式展示
        this.kfr_show = false; //开放日展示
        this.fundManager_show = false;
        if (this.sh_show) {
          this.shtg_show = true;
          this.shbtg_show = true;
        }
      } else if (tabLabel === "销售方式") {
        this.jcxx_show = false; //基础信息展示
        this.jyxx_show = false; //交易信息展示
        this.fyxx_show = false; //费用信息展示
        this.syfp_show = false; //收益分配展示
        this.zhxx_show = false; //账户信息展示
        this.tzfk_show = false; //投资风控展示
        this.lxr_show = false; //联系人展示
        this.xsfs_show = true; //销售方式展示
        this.kfr_show = false; //开放日展示
        this.fundManager_show = false;
        if (this.sh_show) {
          this.shtg_show = true;
          this.shbtg_show = true;
        }
      } else if (tabLabel === "开放日") {
        this.jcxx_show = false; //基础信息展示
        this.jyxx_show = false; //交易信息展示
        this.fyxx_show = false; //费用信息展示
        this.syfp_show = false; //收益分配展示
        this.zhxx_show = false; //账户信息展示
        this.tzfk_show = false; //投资风控展示
        this.lxr_show = false; //联系人展示
        this.xsfs_show = false; //销售方式展示
        this.kfr_show = true; //开放日展示
        this.fundManager_show = false;
        if (this.sh_show) {
          this.shtg_show = true;
          this.shbtg_show = true;
        }
      } else if (tabLabel === "基金经理") {
        this.jcxx_show = false; //基础信息展示
        this.jyxx_show = false; //交易信息展示
        this.fyxx_show = false; //费用信息展示
        this.syfp_show = false; //收益分配展示
        this.zhxx_show = false; //账户信息展示
        this.tzfk_show = false; //投资风控展示
        this.lxr_show = false; //联系人展示
        this.xsfs_show = false; //销售方式展示
        this.kfr_show = false; //开放日展示
        this.fundManager_show = true;
        if (this.sh_show) {
          this.shtg_show = true;
          this.shbtg_show = true;
        }
      } else if (tabLabel === "分级关系") {
        this.jcxx_show = false; //基础信息展示
        this.jyxx_show = false; //交易信息展示
        this.fyxx_show = false; //费用信息展示
        this.syfp_show = false; //收益分配展示
        this.zhxx_show = false; //账户信息展示
        this.tzfk_show = false; //投资风控展示
        this.lxr_show = false; //联系人展示
        this.xsfs_show = false; //销售方式展示
        this.kfr_show = false; //开放日展示
        this.fundManager_show = false;
        this.relationShow = true;
        this.$nextTick(() => {
          this.$refs.relationShip.init(this.relationShipData);
        });
      }
    },
    getSearchDetail() {
      let fundCode = this.PageDataDetail.fundCode;
      let params = {};
      params["fundCode"] = fundCode;
      pageApi
        .getDataSourceDetail(params)
        .then((response) => {
          if (response.data.status === 200) {
            let responseData = response.data.data;
            this.relationShipData = responseData;
            this.$message.closeAll();
            let data = responseData.fundInfo;
            if (responseData.fundRedeems) {
              this.tableDataRedeem = responseData.fundRedeems || []; //赎回费率列表数据
            }
            if (responseData.fundContacts) {
              this.tableDataContact = responseData.fundContacts || []; //赎回费率列表数据
            }
            if (responseData.fundGrades) {
              this.tableDataGrade = responseData.fundGrades || []; //赎回费率列表数据
            }
            if (responseData.fundRewards) {
              this.tableDataReward = responseData.fundRewards || []; //赎回费率列表数据
            }
            if (responseData.fundSallers) {
              this.tableDataSaller = responseData.fundSallers || []; //销售方式列表数据
            }

            if (responseData.fundOpens) {
              this.tableDataOpen = responseData.fundOpens || []; //开放日列表数据
            }

            if (responseData.fundManagers) {
              this.tableDataFundManager = responseData.fundManagers || []; //基金经理
            }
            if (responseData.fundInvests) {
              let arr = [];
              let fundInvestsArr = responseData.fundInvests || []
              let fundInvestArea = this.fundInvestArea || [];
              for (let i = 0; i < fundInvestsArr.length; i++) {
                for (let j = 0; j < fundInvestArea.length; j++) {
                  if (
                    fundInvestsArr[i].investScope === fundInvestArea[j].dimCde
                  ) {
                    arr.push(fundInvestArea[j].dimNme);
                    break;
                  }
                }
              }
              this.fundInvests = arr.toString();
              this.afterfundInvests = arr;
            }
            let formData = commonFun.allPrpos(this.formInline, data);
            this.formInline = formData;
            this.mergeInfo(responseData); //合并信息
          } else {
            this.$message.closeAll();
            this.$message({
              message: response.data.message || "查询失败",
              type: "warning",
            });
          }
          //this.countSubmit_btn = false;
        })
        .catch((err) => {
          // 关闭移动指标弹框
          //this.countSubmit_btn = false;
          console.log("is throw err", err);
          this.$message.closeAll();
          this.$message({
            message: "查询失败",
            type: "warning",
          });
        });
    },
    // 合并信息
    mergeInfo(value) {
      let data = JSON.parse(JSON.stringify(value));
      // console.log('合并数据data--->', data)
      if (data.fundInfo.isGrade == 1) this.isMergeInfo(data);
      //分级为是的情况下------
      else this.isMergeInfoFalse(data);
    },
    /**
     * 分级为是的情况下------
     * gradeInfo  -----分级显示的变量
     * rewardTypeInfo  ----赎回率的变量
     * sgRate  ---申购费率
     * sgOriginRate  --申购起点
     * rgRage  --认购费率
     * manageRate ----管理费率
     */
    isMergeInfo(data) {
      data.fundInfo.callRateType = data.fundInfo.callRateType || "";
      data.fundGrades = data.fundGrades || [];
      let gradeInfo = "",
        rewardTypeInfo = "",
        sgRate = "",
        sgOriginRate = "",
        rgRage = "";
      let manageRate = "",
        name = "";
      if (data.fundInfo.callRateType == "M") {
        name = "";
      } else if (data.fundInfo.callRateType == "D") {
        name = "天";
      } else name = "-";
      for (let i of data.fundGrades) {
        let str = "";
        gradeInfo += `${i.shareType + "类：" + i.fundCodeGrade + " "}`;
        sgRate += `${i.shareType + "类:" + i.applyRate + "%; "}`;
        sgOriginRate += `${i.shareType + "类:" + i.purchasePoint + "万元; "}`;
        rgRage += `${i.shareType + "类:" + i.subscribeRate + "%; "}`;
        manageRate += `${i.shareType + "类:" + i.manageRate + "%; "}`;
        for (let itme of i.fundRedeems) {
          str += `${
            itme.redeemFrom +
            "-" +
            itme.redeemTo +
            name +
            ":" +
            Number(itme.redeemRate) * 100 +
            "%;"
          }`;
        }
        if (str == "") str = ";";
        rewardTypeInfo += i.shareType + "类:" + str;
      }
      this.formInline.isGrade = gradeInfo;
      this.formInline.applyRate = sgRate;
      this.formInline.purchasePoint = sgOriginRate;
      this.formInline.subscribeRate = rgRage;
      this.formInline.callRate = rewardTypeInfo;
      this.formInline.manageRate = manageRate;
    },
    // 分级情况为否的情况下-----
    isMergeInfoFalse(data) {
      let formInfo = data.fundInfo;
      this.formInline.isGrade = "否";
      this.formInline.purchasePoint = formInfo.purchasePoint
        ? formInfo.purchasePoint + "%"
        : "-";
      this.formInline.subscribeRate = formInfo.subscribeRate
        ? formInfo.subscribeRate + "%"
        : "-";
      this.formInline.applyRate = formInfo.applyRate
        ? formInfo.applyRate + "%"
        : "-";
      if (formInfo.callRate) {
        //赎回费率浮动类型是------固定的费率
        this.formInline.callRate = formInfo.callRate
          ? formInfo.callRate + "%"
          : "-";
      } else {
        data.fundRedeems = data.fundRedeems || [];
        data.fundInfo.callRateType = data.fundInfo.callRateType || "";
        let name = "",
          redeemsInfo = "";
        if (data.fundInfo.callRateType == "M") {
          name = "";
        } else if (data.fundInfo.callRateType == "D") {
          name = "天";
        } else name = "-";
        for (let i of data.fundRedeems) {
          redeemsInfo += `${
            i.redeemFrom + "-" + i.redeemTo + name + ":" + i.redeemRate + "%;"
          }`;
        }
        this.formInline.callRate = redeemsInfo;
      }
    },
    getExamineDetail() {
      let id = this.PageDataDetail.id;
      let params = {};

      params.id = id;
      pageExamineApi
        .getDataSourceDetail(params)
        .then((response) => {
          if (response.data.status === 200) {
            this.$message.closeAll();
            let responseData = response.data.data.dataAfter;

            this.approveOpinion = response.data.data.approveOpinion || "-";
            this.modifier = response.data.data.modifier || "-";
            let data = responseData.fundInfo || {};
            if (responseData.fundRedeems) {
              this.tableDataRedeem = responseData.fundRedeems; //赎回费率列表数据
            }
            if (responseData.fundContacts) {
              this.tableDataContact = responseData.fundContacts; //赎回费率列表数据
            }
            if (responseData.fundGrades) {
              this.tableDataGrade = responseData.fundGrades; //赎回费率列表数据
            }
            if (responseData.fundRewards) {
              this.tableDataReward = responseData.fundRewards; //赎回费率列表数据
            }
            if (responseData.fundSallers) {
              this.tableDataSaller = responseData.fundSallers; //计提列表数据
            }

            if (responseData.fundOpens) {
              this.tableDataOpen = responseData.fundOpens; //计提列表数据
            }

            if (responseData.fundManagers) {
              this.tableDataFundManager = responseData.fundManagers; //开放日列表数据
            }

            if (responseData.fundInvests) {
              let arr = [];
              let fundInvestsArr = responseData.fundInvests;
              let fundInvestArea = this.fundInvestArea;
              for (let i = 0; i < fundInvestsArr.length; i++) {
                for (let j = 0; j < fundInvestArea.length; j++) {
                  if (
                    fundInvestsArr[i].investScope === fundInvestArea[j].dimCde
                  ) {
                    arr.push(fundInvestArea[j].dimNme);
                    break;
                  }
                }
              }
              this.fundInvests = arr.toString();
              this.afterfundInvests = arr;
            }

            let formData = commonFun.allPrpos(this.formInline, data);
            this.formInline = formData;

            if (response.data.data.dataBefore) {
              this.beforeData = response.data.data.dataBefore.fundInfo;
              if (response.data.data.dataBefore.fundInvests) {
                let arr = [];
                let fundInvestsArr = response.data.data.dataBefore.fundInvests;
                let fundInvestArea = this.fundInvestArea;
                for (let i = 0; i < fundInvestsArr.length; i++) {
                  for (let j = 0; j < fundInvestArea.length; j++) {
                    if (
                      fundInvestsArr[i].investScope === fundInvestArea[j].dimCde
                    ) {
                      arr.push(fundInvestArea[j].dimNme);
                      break;
                    }
                  }
                }
                this.beforeFundInvests = arr.toString();
              }
            }
            this.compareFormData();
            // console.log("response", response);
            this.tanslateSh(response.data.data); //要素审核待
          } else {
            this.$message.closeAll();
            this.$message({
              message: response.data.message || "查询失败",
              type: "warning",
            });
          }
          //this.countSubmit_btn = false;
        })
        .catch((err) => {
          // 关闭移动指标弹框

          //this.countSubmit_btn = false;
          console.log('is msg err', err)
          this.$message.closeAll();
          this.$message({
            message: "查询失败",
            type: "warning",
          });
        });
    },
    // 审核详情的翻译----------
    tanslateSh(data) {
      let afterInfo = data.dataAfter;
      let beforInfo = data.dataBefore;
      if (afterInfo) this.infoJudeg(afterInfo, "formInline");
      if (beforInfo) this.infoJudeg(beforInfo, "beforeData");
    },
    infoJudeg(data, abFlag) {
      let name = data.fundInfo.callRateType == "D" ? "天" : "";
      if (data.fundInfo.isGrade == "1") {
        this[abFlag].isGrade = "是";
      } else {
        this[abFlag].isGrade = "否";
      }
      if (data.fundRedeems.length > 0) {
        let str = "";
        for (let itme of data.fundRedeems) {
          str += `${
            itme.redeemFrom +
            "-" +
            itme.redeemTo +
            name +
            ":" +
            Number(itme.redeemRate) * 100 +
            "%;"
          }`;
        }
        this[abFlag].callRate = str;
      }
    },
    compareData(before, after) {
      let type = this.PageDataDetail.detailType;
      if (type === 0 || !this.beforeData) {
        return false;
      }
      if (!before && !after) {
        return false;
      }
      if (before === after) {
        return false;
      }
      return true;
    },
    tips(value) {
      if (value) {
        return "修改前：" + value;
      } else {
        return "修改前：-";
      }
    },
    tooltipIsDisabled(before, after) {
      if (this.PageDataDetail.detailType == 0) {
        return false;
      }
      let flag = this.compareData(before, after);

      return flag;
    },
    updateStatus(status, name) {
      this.$confirm("确定" + name + "?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          let params = {};
          params.approveStatus = status;
          params.approveOpinion = this.formHandle.approveOpinion;
          params.id = this.PageDataDetail.id;
          this.countSubmit_btn = true;
          pageExamineApi
            .updateDataStatus(params)
            .then((response) => {
              if (response.data.status === 200) {
                // 关闭移动指标弹框
                this.$message.closeAll();
                this.$message({
                  message: "提交成功",
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
                  message: response.data.message || "提交失败",
                  type: "warning",
                });
              }
              this.countSubmit_btn = false;
            })
            .catch(() => {
              this.$message.closeAll();
              this.$message({
                message: response.data.message || "提交失败",
                type: "warning",
              });
              this.countSubmit_btn = false;
            });
        })
        .catch(() => {
          this.countSubmit_btn = false;
        });
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
          if (val === "fundManageFeeAssetType") {
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
            this.openFrequenceArr = res.data.data; //投资范围
          }

          if (val === "fundOpenRule") {
            this.openRuleArr = res.data.data; //投资范围
          }
        } else {
          this.$message.closeAll();
          this.$message.error("初始化数据失败");
        }
      });
    },
    getEdims() {
      //托管人名称
      //  this.getEdimsGet('fundTrustorCodeType');

      //管理人名称
      //this.getEdimsGet('fundManagerCodeType');

      //基金服务机构
      // this.getEdimsGet('fundoperatorCodeType');
      this.getDeptInfoSel();

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
      this.getEdimsGet("fundManageFeeAssetType");

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
    },
    getDataName(val, code) {
      if (!code) {
        return "-";
      }
      if (val === "fundTrustorCodeType") {
        //commonFun.dictionaryArrToName();
        //托管人名称
        return commonFun.dictionaryArrToName(this.trustorCodeArr, code);
      }
      if (val === "fundManagerCodeType") {
        //管理人名称
        return commonFun.dictionaryArrToName(this.managerCodeArr, code);
      }

      if (val === "fundoperatorCodeType") {
        //基金服务机构
        return commonFun.dictionaryArrToName(this.operatorCodeArr, code);
      }
      if (val === "fundTypes") {
        //基金类型
        return commonFun.dictionaryArrToName(this.fundTypeArr, code);
      }
      if (val === "fundInvestDirectType") {
        //投资方向
        return commonFun.dictionaryArrToName(this.investDirectArr, code);
      }
      if (val === "fundRiskLevelType") {
        //风险等级
        return commonFun.dictionaryArrToName(this.riskLevelArr, code);
      }
      if (val === "fundSaleType") {
        //销售方式
        return commonFun.dictionaryArrToName(this.saleTypeArr, code);
      }
      if (val === "fundSubscribeConfirmDayType") {
        //认购交易确认天数
        return commonFun.dictionaryArrToName(this.subscribeConfirmDayArr, code);
      }
      if (val === "fundSubscribeDeliverDayType") {
        //认购资金交收天数
        return commonFun.dictionaryArrToName(this.subscribeDeliverDayArr, code);
      }
      if (val === "fundApplyConfirmDayType") {
        //申购交易确认天数
        return commonFun.dictionaryArrToName(this.applyConfirmDayArr, code);
      }
      if (val === "fundApplyDeliverDayType") {
        //申购资金交收天数
        return commonFun.dictionaryArrToName(this.applyDeliverDayArr, code);
      }
      if (val === "fundCallConfirmDayType") {
        //赎回交易确认天数
        return commonFun.dictionaryArrToName(this.callConfirmDayArr, code);
      }
      if (val === "fundCallDeliverDayType") {
        //赎回资金交收天数
        return commonFun.dictionaryArrToName(this.callDeliverDayArr, code);
      }
      if (val === "fundCallFloatType") {
        this.callRateTypeArr = res.data.data; //赎回费率浮动类型
        return commonFun.dictionaryArrToName(this.managerCodeArr, code);
      }
      if (val === "fundManageFeePrepareType") {
        //管理费-计提
        return commonFun.dictionaryArrToName(this.manageFeePrepareArr, code);
      }
      if (val === "fundManageFeeAssetType") {
        //管理费-计算方式
        return commonFun.dictionaryArrToName(this.manageFeeAssetArr, code);
      }
      if (val === "fundManageFeePayType") {
        //管理费-支付方式
        return commonFun.dictionaryArrToName(this.manageFeePayArr, code);
      }
      if (val === "fundRewardType") {
        //业绩报酬
        return commonFun.dictionaryArrToName(this.rewardTypeArr, code);
      }
      if (val === "fundRewardPrepareType") {
        //计提方式
        return commonFun.dictionaryArrToName(this.rewardPrepareTypeArr, code);
      }
      if (val === "fundPortionNumberType") {
        //分配次数
        return commonFun.dictionaryArrToName(this.portionNumberArr, code);
      }
      if (val === "fundBonusProcessType") {
        //提交分红流程
        return commonFun.dictionaryArrToName(this.bonusProcessArr, code);
      }
      if (val === "fundDataExpectType") {
        //预估数据以及计算报表
        return commonFun.dictionaryArrToName(this.dataExpectArr, code);
      }
      if (val === "fundBonusConfimType") {
        //分红数据确认
        return commonFun.dictionaryArrToName(this.bonusConfimArr, code);
      }
      if (val === "fundBonusDeliverType") {
        //分红资金交收
        return commonFun.dictionaryArrToName(this.bonusDeliverArr, code);
      }
      if (val === "fundNameGradeType") {
        //分级代码
        return commonFun.dictionaryArrToName(this.fundNameGradeArr, code);
      }

      if (val === "operateType") {
        //运作方式
        return commonFun.dictionaryArrToName(this.operateTypeArr, code);
      }

      if (val === "fundState") {
        //产品状态
        return commonFun.dictionaryArrToName(this.fundStateArr, code);
      }

      if (val === "isOpenShort") {
        //是否可以设置临开
        return commonFun.dictionaryArrToName(this.isOpenShortArr, code);
      }

      if (val === "saleFeePrepare") {
        //销售服务费计提
        return commonFun.dictionaryArrToName(this.saleFeePrepareArr, code);
      }

      if (val === "saleFeePay") {
        //销售服务费支付
        return commonFun.dictionaryArrToName(this.saleFeePayArr, code);
      }

      if (val === "fundOpenFrequence") {
        //开放频率
        return commonFun.dictionaryArrToName(this.openFrequenceArr, code);
      }

      if (val === "fundOpenRule") {
        //开放规则
        return commonFun.dictionaryArrToName(this.openRuleArr, code);
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
    },
    getDeptInfoSel() {
      pageApi
        .getDeptInfoSel()
        .then((response) => {
          if (response.status === 200) {
            let arr = response.data.data;
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
    getInitName(code) {
      let arr = this.managerCodeArr;
      for (let i = 0; i < arr.length; i++) {
        if (arr[i].id === code) {
          return arr[i].instName;
        }
      }
    },
    compareFormData() {
      let type = this.PageDataDetail.detailType;
      if (type === 0 || !this.beforeData) {
        return false;
      }
      this.jcxxI_show = this.comparejcxxFormData();

      this.jyxxI_show = this.comparejyxxFormData();

      this.fyxxI_show = this.comparefyxxFormData();

      this.syxxI_show = this.comparesyxxFormData();

      this.tzxxI_show = this.comparetzxxFormData();
    },
    comparejcxxFormData() {
      let beforeData = this.beforeData;
      let formData = this.formInline;

      if (
        (beforeData.fundName || formData.fundName) &&
        beforeData.fundName != formData.fundName
      ) {
        return true;
      }

      if (
        (beforeData.fundNameEn || formData.fundNameEn) &&
        beforeData.fundNameEn != formData.fundNameEn
      ) {
        return true;
      }

      if (
        (beforeData.trustorCode || formData.trustorCode) &&
        beforeData.trustorCode != formData.trustorCode
      ) {
        return true;
      }

      if (
        (beforeData.operateDept || formData.operateDept) &&
        beforeData.operateDept != formData.operateDept
      ) {
        return true;
      }

      if (
        (beforeData.holdYear || formData.holdYear) &&
        beforeData.holdYear != formData.holdYear
      ) {
        return true;
      }

      if (
        (beforeData.riskLevel || formData.riskLevel) &&
        beforeData.riskLevel != formData.riskLevel
      ) {
        return true;
      }

      if (
        (beforeData.recordCode || formData.recordCode) &&
        beforeData.recordCode != formData.recordCode
      ) {
        return true;
      }

      if (
        (beforeData.managerCode || formData.managerCode) &&
        beforeData.managerCode != formData.managerCode
      ) {
        return true;
      }

      if (
        (beforeData.operatorCode || formData.operatorCode) &&
        beforeData.operatorCode != formData.operatorCode
      ) {
        return true;
      }

      if (
        (beforeData.setupDate || formData.setupDate) &&
        beforeData.setupDate != formData.setupDate
      ) {
        return true;
      }

      if (
        (beforeData.recordDate || formData.recordDate) &&
        beforeData.recordDate != formData.recordDate
      ) {
        return true;
      }

      if (
        (beforeData.operateType || formData.operateType) &&
        beforeData.operateType != formData.operateType
      ) {
        return true;
      }

      if (
        (beforeData.fundState || formData.fundState) &&
        beforeData.fundState != formData.fundState
      ) {
        return true;
      }

      return false;
    },
    comparejyxxFormData() {
      let beforeData = this.beforeData;
      let formData = this.formInline;

      if (
        (beforeData.blockDate || formData.blockDate) &&
        beforeData.blockDate != formData.blockDate
      ) {
        return true;
      }

      if (
        (beforeData.purchaseDiffAppend || formData.purchaseDiffAppend) &&
        beforeData.purchaseDiffAppend != formData.purchaseDiffAppend
      ) {
        return true;
      }

      if (
        (beforeData.subscribeDeliverDay || formData.subscribeDeliverDay) &&
        beforeData.subscribeDeliverDay != formData.subscribeDeliverDay
      ) {
        return true;
      }

      if (
        (beforeData.applyConfirmDay || formData.applyConfirmDay) &&
        beforeData.applyConfirmDay != formData.applyConfirmDay
      ) {
        return true;
      }

      if (
        (beforeData.saleFeePrepare || formData.saleFeePrepare) &&
        beforeData.saleFeePrepare != formData.saleFeePrepare
      ) {
        return true;
      }

      if (
        (beforeData.purchasePoint || formData.purchasePoint) &&
        beforeData.purchasePoint != formData.purchasePoint
      ) {
        return true;
      }

      if (
        (beforeData.subscribeConfirmDay || formData.subscribeConfirmDay) &&
        beforeData.subscribeConfirmDay != formData.subscribeConfirmDay
      ) {
        return true;
      }

      if (
        (beforeData.subscribeRate || formData.subscribeRate) &&
        beforeData.subscribeRate != formData.subscribeRate
      ) {
        return true;
      }

      if (
        (beforeData.applyDeliverDay || formData.applyDeliverDay) &&
        beforeData.applyDeliverDay != formData.applyDeliverDay
      ) {
        return true;
      }

      if (
        (beforeData.callRate || formData.callRate) &&
        beforeData.callRate != formData.callRate
      ) {
        return true;
      }

      if (
        (beforeData.saleFeePay || formData.saleFeePay) &&
        beforeData.saleFeePay != formData.saleFeePay
      ) {
        return true;
      }

      return false;
    },
    comparefyxxFormData() {
      let beforeData = this.beforeData;
      let formData = this.formInline;

      if (
        (beforeData.manageFeePrepare || formData.manageFeePrepare) &&
        beforeData.manageFeePrepare != formData.manageFeePrepare
      ) {
        return true;
      }

      if (
        (beforeData.manageFeePay || formData.manageFeePay) &&
        beforeData.manageFeePay != formData.manageFeePay
      ) {
        return true;
      }

      if (
        (beforeData.subscribeDeliverDay || formData.subscribeDeliverDay) &&
        beforeData.subscribeDeliverDay != formData.subscribeDeliverDay
      ) {
        return true;
      }

      if (
        (beforeData.manageRate || formData.manageRate) &&
        beforeData.manageRate != formData.manageRate
      ) {
        return true;
      }

      if (
        (beforeData.operateRate || formData.operateRate) &&
        beforeData.operateRate != formData.operateRate
      ) {
        return true;
      }

      if (
        (beforeData.manageAccount || formData.manageAccount) &&
        beforeData.manageAccount != formData.manageAccount
      ) {
        return true;
      }

      if (
        (beforeData.manageBankName || formData.manageBankName) &&
        beforeData.manageBankName != formData.manageBankName
      ) {
        return true;
      }

      if (
        (beforeData.trustRate || formData.trustRate) &&
        beforeData.trustRate != formData.trustRate
      ) {
        return true;
      }

      if (
        (beforeData.rewardType || formData.rewardType) &&
        beforeData.rewardType != formData.rewardType
      ) {
        return true;
      }

      if (
        (beforeData.manageAccountName || formData.manageAccountName) &&
        beforeData.manageAccountName != formData.manageAccountName
      ) {
        return true;
      }

      return false;
    },
    comparesyxxFormData() {
      let beforeData = this.beforeData;
      let formData = this.formInline;

      if (
        (beforeData.incomePortionDesc || formData.incomePortionDesc) &&
        beforeData.incomePortionDesc != formData.incomePortionDesc
      ) {
        return true;
      }

      if (
        (beforeData.portionNumber || formData.portionNumber) &&
        beforeData.portionNumber != formData.portionNumber
      ) {
        return true;
      }

      if (
        (beforeData.dataExpect || formData.dataExpect) &&
        beforeData.dataExpect != formData.dataExpect
      ) {
        return true;
      }

      if (
        (beforeData.bonusDeliver || formData.bonusDeliver) &&
        beforeData.bonusDeliver != formData.bonusDeliver
      ) {
        return true;
      }

      if (
        (beforeData.bonusProcess || formData.bonusProcess) &&
        beforeData.bonusProcess != formData.bonusProcess
      ) {
        return true;
      }

      if (
        (beforeData.bonusConfim || formData.bonusConfim) &&
        beforeData.bonusConfim != formData.bonusConfim
      ) {
        return true;
      }

      return false;
    },
    comparetzxxFormData() {
      let beforeData = this.beforeData;
      let formData = this.formInline;

      if (
        (beforeData.investLimit || formData.investLimit) &&
        beforeData.investLimit != formData.investLimit
      ) {
        return true;
      }

      if (
        (beforeData.warnPoint || formData.warnPoint) &&
        beforeData.warnPoint != formData.warnPoint
      ) {
        return true;
      }

      if (
        (beforeData.lossPoint || formData.lossPoint) &&
        beforeData.lossPoint != formData.lossPoint
      ) {
        return true;
      }
      return false;
    },
  },
};
</script>

<style lang="scss" rel="stylesheet/scss">
.productDetailStyle {
  .el-tabs__content{
     margin:0 auto;
     width: 100% !important
  }
}
.gradeStyle {
  text-overflow: ellipsis;
  // width: 280px;
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
.product_news_box {
  //  padding-right: 15px;

  height: 36px;
  line-height: 36px;
  background: #fff;
  color: #111;
  font-size: 14px;
}
</style>

<template>
  <div>

    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane v-for="item in tranferTypes" :key="item.id" :label="item.dimNme" :name="item.id+'_'+item.dimValue">
      </el-tab-pane>
    </el-tabs>
    <el-collapse v-model="activeNames" @change="handleChange">
      <el-collapse-item name="1">
        <template slot="title" style="color: #409EFF;font-weight: bold">
          <i class="el-icon-reading"></i>操作指南
        </template>
        <div style="margin-left: 50px;" v-show="is_yz_show">
          <el-row>
            <el-col :span="2"><span style="font-weight: bold">业务场景:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">管理人可以在本界面将基金财产在银行托管账户与证券资金账户之间进行调拨。</div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">交互流程:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">
                1.管理人（基金经理、交易员、基金运营部估值核算岗）划款指令经办人员登录运营管理平台：【账户划款】->【转账指令】->【银证转账】，填写划款信息，点击【提交】，之后由国泰君安公募外包服务中心估值核算岗接收指令，并在估值系统中按照指定格式制作完成指令后上传并提交下一节点，由国泰君安公募外包服务中心估值核算岗复核人员复核并提交回管理人基金运营部估值核算岗，之后由管理人基金运营部经办、复核、审批。
              </div>
              <div style="width:80%;margin-left:10px">
                2.管理人划款指令复核人员（基金运营部估值核算岗）登录运营管理平台：【账户划款】->【跟踪待办】，选择经办人员提交的指令，完成复核并点击确认。
              </div>
              <div style="width:80%;margin-left:10px">3.管理人划款指令审核人员（基金运营部总监）操作界面：【账户划款】->【跟踪待办】，选择复核人员复核的指令，完成审核并点击确认。
              </div>
              <div style="width:80%;margin-left:10px">4.管理人（基金运营部估值核算岗）需要将投资交易系统即将转出的现金头寸冻结。</div>
              <div style="width:80%;margin-left:10px">5.管理人审批完后，下载指令并盖章，以托管人约定的方式发送给管理人。</div>
              <div style="width:80%;margin-left:10px">6.管理人划款指令操作人员通过平台【账户划款】->【跟踪待办】，实时查询指令流程进度与执行结果。</div>
              <div style="width:80%;margin-left:10px">7.执行结果为“划款成功”，管理人（基金运营部估值核算岗）需要将投资交易系统资金进行调整，并将原转出现金解冻。</div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">注意事项:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">1.请于当日13：00前向我部提交有效场内转账划款指令。</div>
              <div style="width:80%;margin-left:10px">2.请确保托管账户有足够的头寸。</div>
              <div style="width:80%;margin-left:10px">
                3.由于银证互换时间截止为15:00，与人行大额转账截止时间17:15有时间差，因此请留意下一工作日场外资金交收情况，以提前应对。
              </div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">反馈时效:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">有效指令提交后，一般于2个工作小时内处理完毕，运营管理平台即时反馈办理结果。</div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">交互方式:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">
                各划款业务节点均有具体操作人电话信息。所有指令与管理人交互均以运营管理平台线上流程为准，除特殊情况可能使用邮件、深证通备选传输方式。
              </div>
            </el-col>
          </el-row>
        </div>

        <div style="margin-left: 50px;" v-show="is_yq_show">
          <el-row>
            <el-col :span="2"><span style="font-weight: bold">业务场景:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">管理人可以在本界面将基金财产在银行托管账户与期货资金账户之间进行调拨。</div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">交互流程:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">
                1.管理人划款指令经办人员（基金经理、交易员、基金运营部估值核算岗）登录运营管理平台：【账户划款】->【转账指令】->【银期转账】后，填写划款信息，点击【提交划款】。
              </div>
              <div style="width:80%;margin-left:10px">
                2.管理人划款指令复核人员（基金运营部估值核算岗）登录运营管理平台：【账户划款】->【跟踪待办】，选择经办人员提交的指令，完成复核并点击确认。
              </div>
              <div style="width:80%;margin-left:10px">3.管理人（基金运营部估值核算岗）需要将投资交易系统即将转出的现金头寸冻结。</div>
              <div style="width:80%;margin-left:10px">4.管理人划款指令审核人员（基金运营部总监）操作界面：【账户划款】->【跟踪待办】，选择复核人员复核的指令，完成审核并点击确认。
              </div>
              <div style="width:80%;margin-left:10px">5.管理人划款指令操作人员通过平台【账户划款】->【跟踪待办】，实时查询指令流程进度与执行结果。</div>
              <div style="width:80%;margin-left:10px">6.执行结果为“划款成功”，管理人（基金运营部估值核算岗）需要将投资交易系统资金进行调整，并将原转出现金解冻。</div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">注意事项:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">1.请于当日13：00前向我部提交有效场内转账划款指令。</div>
              <div style="width:80%;margin-left:10px">2.请确保托管账户有足够的头寸。</div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">反馈时效:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">有效指令提交后，一般于2个工作小时内处理完毕，运营管理平台即时反馈办理结果。</div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">交互方式:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">
                各划款业务节点均有具体操作人电话信息。所有指令与管理人交互均以运营管理平台线上流程为准，除特殊情况可能使用邮件、深证通备选传输方式。
              </div>
            </el-col>
          </el-row>
        </div>

        <div style="margin-left: 50px;" v-show="is_yx_show">
          <el-row>
            <el-col :span="2"><span style="font-weight: bold">业务场景:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">管理人可以在本界面将基金财产在银行托管账户与信用资金账户之间进行调拨。</div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">交互流程:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">
                1.管理人划款指令经办人员（基金经理、交易员、基金运营部估值核算岗）登录运营管理平台：【账户划款】->【转账指令】->【银信转账】后，填写划款信息，点击【提交划款】。
              </div>
              <div style="width:80%;margin-left:10px">
                2.管理人划款指令复核人员（基金运营部估值核算岗）登录运营管理平台：【账户划款】->【跟踪待办】，选择经办人员提交的指令，完成复核并点击确认。
              </div>
              <div style="width:80%;margin-left:10px">3.管理人（基金运营部估值核算岗）需要将投资交易系统即将转出的现金头寸冻结。</div>
              <div style="width:80%;margin-left:10px">4.管理人划款指令审核人员（基金运营部总监）操作界面：【账户划款】->【跟踪待办】，选择复核人员复核的指令，完成审核并点击确认。
              </div>
              <div style="width:80%;margin-left:10px">5.管理人划款指令操作人员通过平台【账户划款】->【跟踪待办】，实时查询指令流程进度与执行结果。</div>
              <div style="width:80%;margin-left:10px">6.执行结果为“划款成功”，管理人（基金运营部估值核算岗）需要将投资交易系统资金进行调整，并将原转出现金解冻。</div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">注意事项:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">1.请于当日13：00前向我部提交有效场内转账划款指令。</div>
              <div style="width:80%;margin-left:10px">2.请确保托管账户有足够的头寸。</div>
              <div style="width:80%;margin-left:10px">3.本业务通过我部运营管理平台办理场内转账业务为人工划款模式。</div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">反馈时效:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">有效指令提交后，一般于2个工作小时内处理完毕，运营管理平台即时反馈办理结果。</div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">交互方式:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">
                各划款业务节点均有具体操作人电话信息。所有指令与管理人交互均以运营管理平台线上流程为准，除特殊情况可能使用邮件、深证通备选传输方式。
              </div>
            </el-col>
          </el-row>
        </div>

        <div style="margin-left: 50px;" v-show="is_yy_show">
          <el-row>
            <el-col :span="2"><span style="font-weight: bold">业务场景:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">管理人可以在本界面将基金财产在银行托管账户与信用资金账户之间进行调拨。</div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">交互流程:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">
                1.管理人划款指令经办人员（基金经理、交易员、基金运营部估值核算岗）登录运营管理平台：【账户划款】->【转账指令】->【银衍转账】后，填写划款信息，点击【提交划款】。
              </div>
              <div style="width:80%;margin-left:10px">
                2.管理人划款指令复核人员（基金运营部估值核算岗）登录运营管理平台：【账户划款】->【跟踪待办】，选择经办人员提交的指令，完成复核并点击确认。
              </div>
              <div style="width:80%;margin-left:10px">3.管理人（基金运营部估值核算岗）需要将投资交易系统即将转出的现金头寸冻结。</div>
              <div style="width:80%;margin-left:10px">4.管理人划款指令审核人员（基金运营部总监）操作界面：【账户划款】->【跟踪待办】，选择复核人员复核的指令，完成审核并点击确认。
              </div>
              <div style="width:80%;margin-left:10px">5.管理人划款指令操作人员通过平台【账户划款】->【跟踪待办】，实时查询指令流程进度与执行结果。</div>
              <div style="width:80%;margin-left:10px">6.执行结果为“划款成功”，管理人（基金运营部估值核算岗）需要将投资交易系统资金进行调整，并将原转出现金解冻。</div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">注意事项:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">1.请于当日13：00前向我部提交有效场内转账划款指令。</div>
              <div style="width:80%;margin-left:10px">2.请确保托管账户有足够的头寸。</div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">反馈时效:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">有效指令提交后，一般于2个工作小时内处理完毕，运营管理平台即时反馈办理结果。</div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">交互方式:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">
                各划款业务节点均有具体操作人电话信息。所有指令与管理人交互均以运营管理平台线上流程为准，除特殊情况可能使用邮件、深证通备选传输方式。
              </div>
            </el-col>
          </el-row>
        </div>

        <div style="margin-left: 50px;" v-show="is_yg_show">
          <el-row>
            <el-col :span="2"><span style="font-weight: bold">业务场景:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">管理人可以在本界面将基金财产在银行托管账户与贵金属保证金账户之间进行调拨。</div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">交互流程:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">
                1.管理人划款指令经办人员（基金经理、交易员、基金运营部估值核算岗）登录运营管理平台：【账户划款】->【转账指令】->【银贵转账】后，填写划款信息，点击【提交划款】。
              </div>
              <div style="width:80%;margin-left:10px">
                2.管理人划款指令复核人员（基金运营部估值核算岗）登录运营管理平台：【账户划款】->【跟踪待办】，选择经办人员提交的指令，完成复核并点击确认。
              </div>
              <div style="width:80%;margin-left:10px">3.管理人（基金运营部估值核算岗）需要将投资交易系统即将转出的现金头寸冻结。</div>
              <div style="width:80%;margin-left:10px">4.管理人划款指令审核人员（基金运营部总监）操作界面：【账户划款】->【跟踪待办】，选择复核人员复核的指令，完成审核并点击确认。
              </div>
              <div style="width:80%;margin-left:10px">5.管理人划款指令操作人员通过平台【账户划款】->【跟踪待办】，实时查询指令流程进度与执行结果。</div>
              <div style="width:80%;margin-left:10px">6.执行结果为“划款成功”，管理人（基金运营部估值核算岗）需要将投资交易系统资金进行调整，并将原转出现金解冻。</div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">注意事项:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">1.请于当日13：00前向我部提交有效场内转账划款指令。</div>
              <div style="width:80%;margin-left:10px">2.部分经纪商对于大额出金存在限额管理，为了提高转账效率，请事先与营业部联系提高转账限额。</div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">反馈时效:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">
                各划款业务节点均有具体操作人电话信息。所有指令与管理人交互均以运营管理平台线上流程为准，除特殊情况可能使用邮件、深证通备选传输方式。
              </div>
            </el-col>
          </el-row>
        </div>
      </el-collapse-item>
    </el-collapse>
    <!-- <div style="width:80%;margin: 0 auto;">
      <el-steps  :active="0"   >
        <el-step status="finish" title="流程发起" description="当前处理"></el-step >
        <el-step  title="指令经办" description="待执行">></el-step >
        <el-step title="指令复核" description="待执行"></el-step >
        <el-step title="管理人复核" description="待执行"></el-step >
        <el-step title="管理人审批" description="待执行"></el-step >
        <el-step title="托管划款中" description="待执行"></el-step >
        <el-step title="划款成功" description="待执行"></el-step >
      </el-steps>

    </div> -->
    <div v-show="startTransfer">
      <div v-show="isGtja==1">
        <start-transfer :transferKey="transferKey" :isGtja="1"></start-transfer>
      </div>
      <div v-show="isGtja==0">
        <start-transfer :transferKey="transferKey" :isGtja="0"></start-transfer>
      </div>
    </div>

    <el-form ref="formInline" status-icon label-width="120px" :model="formInline" :rules="commitRules"
             class="commitClass" auto-complete="on" label-position="left">

      <el-form-item v-if="accountTypes2.length" label="指令类型" prop="type">
        <el-radio v-model="formInline.type" v-for="item in accountTypes2" :key="item.dimValue" :label="item.dimValue"
                  @change="cccc">{{ item.dimNme }}
        </el-radio>
      </el-form-item>

      <el-form-item label="产品" prop="accountCode">
        <select-table v-model="formInline.accountCode" :width="'100%'" @sendDataObj="sendDataObj"></select-table>
      </el-form-item>
      <el-form-item label="要求划款日期" prop="date">
        <el-date-picker
          style="width: 100%"
          v-model="formInline.date"
          type="date"
          class="el_form_item"
          format="yyyy-MM-dd"
          value-format="yyyy-MM-dd"
          @change="handleDateChange"
          :picker-options="pickerOptions"
          placeholder="选择日期">
        </el-date-picker>
      </el-form-item>

      <el-form-item :label="jisxz ? '经纪商' : '经纪商'" prop="broker" v-if="jjs_show">
        <el-select v-if="jisxz" style="width: 100%" filterable clearable v-model="formInline.broker" placeholder="请选择"
                   class="el_form_item">
          <el-option
            v-for="(item, index) in borkerInfos"
            @click.native="brokerChange(item)"
            :key="index + 'broker'"
            :label="item.name"
            :value="item.value">
          </el-option>
        </el-select>
        <el-input style="width: 100%" v-else clearable v-model="formInline.broker" maxlength="134" placeholder="请输入"
                  class="el_form_item"></el-input>
      </el-form-item>

      <!-- <el-form-item v-if="is_skfzh_show" label="收款方账户" prop="payeeAccount">
          <el-input style="width: 100%"  clearable v-model="formInline.payeeAccount" maxlength="66"  placeholder="请输入" class="el_form_item"></el-input>
      </el-form-item> -->

      <el-form-item label="转账金额(元)" prop="money">
        <el-input
          v-model.trim="formInline.money"
          style="width: 100%"
          type="text"
          class="el_form_item"
          auto-complete="off"
          @focus="moneyFocus"
          @blur="moneyBlur"
          maxlength="24"
          placeholder="请输入金额"/>
        <!-- show-word-limit maxlength="18" -->
      </el-form-item>

      <!-- 收款4要素 -->
      <el-row v-if="payeeAcc_show">
        <el-col :span="24">
          <el-form-item label="收款人" prop="payeeAcconame">
            <!-- <el-input placeholder="请输入收款人" v-model="formInline.payeeAcconame" maxlength="100"></el-input> -->
            <selectAccount v-model="formInline.payeeAcconame" ref="selectAccount2" @sendDataObj="getAccountInfo2"
                           :filteredValue="filteredValue2"/>
          </el-form-item>
          <el-form-item label="收款账号" prop="payeeAccount">
            <el-input placeholder="请输入收款账号" v-model="formInline.payeeAccount" maxlength="66"
                      :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="收款行" prop="payeeBank">
            <el-input placeholder="请输入收款行" v-model="formInline.payeeBank" maxlength="166" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="支付系统号" prop="paymentSystemNumber">
            <el-input placeholder="请输入支付系统号" v-model="formInline.paymentSystemNumber" maxlength="66"
                      :disabled="true"></el-input>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20" v-if="account_show">
        <el-col :span="12">
          <el-form-item label="付款人" prop="payerAcconame">
            <selectAccount v-model="formInline.payerAcconame" ref="selectAccount1" @sendDataObj="getAccountInfo1"
                           :filteredValue="filteredValue1"/>
          </el-form-item>
          <el-form-item label="付款账号" prop="payerAccount">
            <el-input placeholder="请输入付款账号" v-model="formInline.payerAccount" maxlength="66"
                      :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="付款行" prop="payerBank">
            <el-input placeholder="请输入付款行" v-model="formInline.payerBank" maxlength="166" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="收款人" prop="payeeAcconame">
            <!-- <el-input placeholder="请输入收款人" v-model="formInline.payeeAcconame" maxlength="100"></el-input> -->
            <selectAccount v-model="formInline.payeeAcconame" ref="selectAccount2" @sendDataObj="getAccountInfo2"
                           :filteredValue="filteredValue2"/>
          </el-form-item>
          <el-form-item label="收款账号" prop="payeeAccount">
            <el-input placeholder="请输入收款账号" v-model="formInline.payeeAccount" maxlength="66"
                      :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="收款行" prop="payeeBank">
            <el-input placeholder="请输入收款行" v-model="formInline.payeeBank" maxlength="166" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="支付系统号" prop="paymentSystemNumber">
            <el-input placeholder="请输入支付系统号" v-model="formInline.paymentSystemNumber" maxlength="66"
                      :disabled="true"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <el-form-item label="用途" prop="processUse" v-if="processUse_show">
        <el-input
          type="textarea"
          :autosize="{ minRows: 2, maxRows: 4}"
          maxlength="1000"
          show-word-limit
          placeholder="请输入内容"
          v-model="formInline.processUse">
        </el-input>
      </el-form-item>
      <el-form-item label="备注" prop="remark">
        <el-input
          style="width: 100%"
          v-model="formInline.remark"
          placeholder="请输入备注"
          type="textarea"
          :autosize="{minRows: 3}"
          maxlength="1000"
          show-word-limit
          class="el_form_item"
          auto-complete="off"/>
      </el-form-item>
      <!--      <p style="color:red;" v-if="true">提醒：当前划款流程已晚于托管约定时间，可能会出现资金不能及时到账情形</p>-->
      <el-button v-btn="'transfer.bizBegin.submit'" :disabled="submit_btn" style="margin-top:15px" type="primary"
                 class="loginBtn" @click="onSubmit('formInline')">
        提交
      </el-button>
      <span v-if="warning_show" style="color:red;">当前划款流程已晚于托管约定时间，可能会出现资金不能及时到账情形</span>
    </el-form>

  </div>

</template>

<script>
import accountApi from '@/api/product/accountSearch'
import customApi from '@/api/custom/customList'
import selectAccount from '@/views/commonComponents/selectAccount.vue'
import pageApi from '@/api/home/calendarList'
import bizBeginApi from '@/api/transfer/bizBegin'
import fun from '@/filters/common'
import { moneyThousand } from '@/filters/index'
import { moneyYuan } from '@/filters/index'
import selectTable from '@/views/commonComponents/selectTable.vue'
import StartTransfer from '../startTransfer/start-transfer.vue'
import moment from 'moment'
import { set } from 'xe-utils/methods'

//时间请求接口

export default {
  components: { selectTable, StartTransfer, selectAccount },
  name: 'bizBegin',
  data() {

    //校验产品或基金代码
    const validateAccount = (rule, value, callback) => {
      if (!value) {
        callback(new Error('产品名称不能为空'))
      } else {
        callback()
      }
    }
    //校验日期
    const validateDate = (rule, value, callback) => {
      if (value === null || value.length === 0) {
        callback(new Error('请选择日期'))
      } else {
        callback()
      }
    }

    //转账金额
    const validateMoney = (rule, value, callback) => {
      if (!value) {
        callback(new Error('转账金额'))
      } else if (value.split('.').length > 2) {
        callback(new Error('输入正确金额'))
      } else {
        value = Math.round(value * Math.pow(10, 2)) / Math.pow(10, 2) //四舍五入
        value = Number(value).toFixed(2) //不足补位
        this.formInline.money = value
        callback()
      }
    }
    //校验经纪商
    const validateBroker = (rule, value, callback) => {
      if (!value) {
        callback(new Error('经纪商不能为空'))
      } else {
        callback()
      }
    }
    return {
      isGtja: 1,
      startTransfer: false,
      nowTime: '',  //当前服务器时间
      pickerOptions: {
        // disabledDate(time) {
        //   return time.getTime() < Date.now() - 24 * 60 * 60 * 1000;
        // },
      },
      transferKey: 'Process_transfer',
      jisxz: true,
      api: 'getZqAccountSELECT',
      formInline: {
        payerAcconame: '',  //付款人
        payerAccount: '',  //付款账号
        payerBank: '',  //付款行
        payeeAcconame: '',  //收款人
        payeeAccount: '',  //收款账号
        payeeBank: '',  //收款行
        paymentSystemNumber: '',  //支付系统号
        accountCode: '',//产品&基金代码
        date: '',//要求划款日期
        broker: '',//经纪商选择
        money: '',//转账金额
        instructType: '',//指令类型
        accountType: '银证转账',//转账类型
        type: '',
        processUse: '', //用途
        remark: ''//备注
      },
      submitOrder: new Date().getTime(),
      tranferTypes: [],//tab数组
      accountTypes: [],//指令类型数组
      accountTypes2: [],//指令类型数组
      activeName: '',//默认tab
      activeStr: '',//默认Tab strName
      is_yg_show: false,//银贵展示
      is_yy_show: false,//银衍展示
      is_yx_show: false,//银信展示
      is_yq_show: false,//银期展示
      is_yz_show: true,//银正展示
      is_skfzh_show: true, //收款方账户展示
      account_show: false,
      payeeAcc_show: false,
      jjs_show: true, //经纪商展示
      processUse_show: false, //用途展示
      warning_show: false, //提醒是否展示
      submit_btn: false,//提交
      definedId: '',
      accountCodes: [],//产品数组
      accountCodesTemp: [],//产品数组
      borkerInfos: [],//经纪商数组
      borkerInfos2: [],//经纪商数组
      // 验证规则
      // moneyValidateDefalut:/^(0|[1-9]{1}\d{0,15}|[1-9]{1}\d{0,13}\.\d{1}|[1-9]{1}\d{0,12}\.\d{2}|0\.\d{1,2})$/,
      moneyValidateDefalut: /^(0|[1-9]{1}\d{0,14}|[1-9]{1}\d{0,12}\.\d{1}|[1-9]{1}\d{0,11}\.\d{2}|0\.\d{1,2})$/,
      moneyValidate: /^(0|[1-9]{1}\d{0,14}|[1-9]{1}\d{0,12}\.\d{1}|[1-9]{1}\d{0,11}\.\d{2}|0\.\d{1,2})$/,
      // 验证规则
      commitRules: {
        // 指令类型
        type: [{ required: true, trigger: 'change', message: '请选择指令类型' }],
        // 产品&基金代码
        accountCode: [{ required: true, trigger: 'change', message: '请选择产品' }],
        // 要求划款日期
        date: [{ required: true, trigger: 'change', message: '请选择划款日期' }],
        broker: [{ required: true, trigger: 'change', message: '请选择经纪商' }],

        money: [{ required: true, trigger: 'change', pattern: '', message: '请输入数值且最多包含2位小数' }],
        remark: [{ required: false, trigger: 'change' }],
        payerAcconame: [{ required: true, pattern: '', message: '请输入付款人', trigger: 'change' }],
        payerAccount: [
          { required: true, pattern: '', message: '请输入付款账号', trigger: 'change' },
          { required: false, pattern: /^[a-zA-Z0-9]+$/, message: '请输入字母加数字的组合', trigger: 'change' }
        ],
        payerBank: [{ required: true, pattern: '', message: '请输入付款行', trigger: 'change' }],
        payeeAcconame: [{ required: true, message: '请输入收款人', trigger: 'change' }],
        payeeAccount: [
          { required: true, message: '请输入收款账号', trigger: 'change' },
          { required: false, pattern: /^[a-zA-Z0-9]+$/, message: '请输入字母加数字的组合', trigger: 'change' }
        ],
        payeeBank: [{ required: true, message: '请输入收款行', trigger: 'change' }],
        paymentSystemNumber: [
          // {required:false, message: "请输入支付系统号", trigger: "change"},
          { required: false, pattern: /^[a-zA-Z0-9]+$/, message: '请输入字母加数字的组合', trigger: 'change' }
        ]
      },

      activeNames: [], //默认展示指南
      qhData: [], //期货data
      zqData: [],//证券data
      accArr: [],
      payeeApi: '',//收款人账户来源
      payerApi: '',//付款人账户来源
      filteredValue1: [], //账户筛选-付款人
      filteredValue2: [] //账户筛选-收款人
    }
  },
  //页面加载后触发
  mounted() {

    //获取提交串submitOrder
    this.getSubmitOrder()

    //  获取当前服务器时间
    this.getServerData()
    //查询产品信息

    this.getProductInfo()

    //查询经纪商
    this.getBrokerInfo()

    //获取defineId
    //this.getDefineId();

    //获取tab数组
    this.getTransferType()
    this.handleDateChange()
    // this.getTody()
    this.commitRules.money[0].pattern = this.moneyValidate
  },
  watch: {
    'formInline.type'(data) {
      console.log(data, '--')
      // this.resetForm('formInline');

        if(data=='gm040101'){
          this.formInline.processUse = "银转证"
        }else if(data=='gm040102'){
          this.formInline.processUse = "证转银"
        }else if(data=='gm040201'){
          this.formInline.processUse = "银转期"
        }else if(data=='gm040202'){
          this.formInline.processUse = "期转银"
        }else if(data=='gm040301'){
          this.formInline.processUse = "银转信"
        }else if(data=='gm040302'){
          this.formInline.processUse = "信转银"
        }else if(data=='gm040401'){
          this.formInline.processUse = "银转衍"
        }else if(data=='gm040402'){
          this.formInline.processUse = "衍转银"
        }else if(data=='gm040501'){
          this.formInline.processUse = "银转贵"
        }else if(data=='gm040502'){
          this.formInline.processUse = "贵转银"
        }else{
          this.formInline.processUse = ""
        }

      if (['gm040203', 'gm040403', 'gm040503', 'gm040601', 'gm040602', 'gm040603', 'gm0407', 'gm040701', 'gm040702', 'gm040703', 'gm040704', 'gm040705', 'gm040706'].includes(data)) {
        this.account_show = true
        this.payeeAcc_show = false
      } else {
        this.payeeAcc_show = true
        this.account_show = false
      }

      if (['gm040101'].includes(data)) {
        // 证券账户
        this.payeeApi = 'getZqAccList'
        this.filteredValue2 = ['zq']
      } else if (['gm040102', 'gm040202', 'gm040302', 'gm040402', 'gm040502', 'gm040602', 'gm040702', 'gm040704'].includes(data)) {
        // 托管户
        this.payeeApi = 'getTgAccList'
        this.filteredValue2 = ['fiduciary']
      } else if (['gm040201'].includes(data)) {
        // 期货账户
        this.payeeApi = 'getQhAccList'
        this.filteredValue2 = ['qh']
      } else if (['gm040701', 'gm040703', 'gm040705', 'gm040706'].includes(data)) {
        // 银行间债券账户
        this.payeeApi = 'getYhjAccList'
        this.filteredValue2 = ['yhjzz', 'yhjsq']
      } else if (['gm040203', 'gm040301', 'gm040401', 'gm040403', 'gm040501', 'gm040503', 'gm040601', 'gm040603'].includes(data)) {
        // 其他账户
        this.payeeApi = 'getQtAccList'
        this.filteredValue2 = ['other']
      } else {
        this.payeeApi = 'getQtAccList'
        this.filteredValue2 = []
      }

      if (['gm040102'].includes(data)) {
        // 证券账户
        this.payerApi = 'getZqAccList'
        this.filteredValue1 = ['zq']
      } else if (['gm040101', 'gm040201', 'gm040203', 'gm040301', 'gm040401', 'gm040403', 'gm040501', 'gm040503', 'gm040601', 'gm040603', 'gm040701', 'gm040703'].includes(data)) {
        // 托管账户
        this.payerApi = 'getTgAccList'
        this.filteredValue1 = ['fiduciary']
      } else if (['gm040202'].includes(data)) {
        // 期货账户
        this.payerApi = 'getQhAccList'
        this.filteredValue1 = ['qh']
      } else if (['gm040702', 'gm040704', 'gm040705', 'gm040706'].includes(data)) {
        // 银行间债券账户
        this.payerApi = 'getYhjAccList'
        this.filteredValue1 = ['yhjzz', 'yhjsq']
      } else if (['gm040302', 'gm040402', 'gm040502', 'gm040602'].includes(data)) {
        // 其他账户
        this.payerApi = 'getQtAccList'
        this.filteredValue1 = ['other']
      } else {
        this.payerApi = 'getQtAccList'
        this.filteredValue1 = []
      }
      console.log('收--' + this.payeeApi, '付--' + this.payerApi)
      // 指令类型变化时，若产品选择框有值，则获取对应指令类型的账户信息
      if (this.formInline.accountCode) {
        // setTimeout(() => {
        //   if(this.$refs.selectAccount1){
        //     this.$refs.selectAccount1.init(this.accArr);
        //   }
        //   if(this.$refs.selectAccount2){
        //     this.$refs.selectAccount2.init(this.accArr);
        //   }
        // }, 50);
        let fundCode = this.formInline.accountCode.split('_')[0]
        // 只展示规定账户类型
        // this.getAcc({fundCode})
        // 展示全部账户类型，默认展示规定账户类型
        this.getAccounts({ productCode: fundCode })
      }

      setTimeout(() => {
        this.$nextTick(() => {
          this.$refs['formInline'].clearValidate('payerAcconame')
          this.$refs['formInline'].clearValidate('payerAccount')
          this.$refs['formInline'].clearValidate('payerBank')
          this.$refs['formInline'].clearValidate('payeeAcconame')
          this.$refs['formInline'].clearValidate('payeeAccount')
          this.$refs['formInline'].clearValidate('payeeBank')
        })
        this.formInline.payerAcconame = ''  //付款人
        this.formInline.payerAccount = ''  //付款账号
        this.formInline.payerBank = ''  //付款行
        this.formInline.payeeAcconame = ''  //收款人
        this.formInline.payeeAccount = ''  //收款账号
        this.formInline.payeeBank = ''  //收款行
        this.formInline.paymentSystemNumber = ''  //支付系统号
        this.$nextTick(() => {
          this.$refs['formInline'].clearValidate(['payerAcconame'])
          this.$refs['formInline'].clearValidate(['payerAccount'])
          this.$refs['formInline'].clearValidate(['payerBank'])
          this.$refs['formInline'].clearValidate(['payeeAcconame'])
          this.$refs['formInline'].clearValidate(['payeeAccount'])
          this.$refs['formInline'].clearValidate(['payeeBank'])
        })
      }, 80)
      this.$nextTick(() => {
        if (this.$refs.selectAccount1) {
          this.$refs.selectAccount1.init([])
        }
        if (this.$refs.selectAccount2) {
          this.$refs.selectAccount2.init([])
        }
      })
    },
    'formInline.accountCode'(data) {
      // this.formInline.payerAcconame='';  //付款人
      // this.formInline.payerAccount='';  //付款账号
      // this.formInline.payerBank='';  //付款行
      // this.formInline.payeeAcconame='';  //收款人
      // this.formInline.payeeAccount='';  //收款账号
      // this.formInline.payeeBank='';  //收款行
      // this.formInline.paymentSystemNumber='';  //支付系统号
    }
  },
  methods: {
    /*
       函数作用：处理-要求划款日期 日期选择器的修改事件，实现托管最晚划款时间提醒
       修改人：lrb - 2021-11
     */
    handleDateChange() {
      pageApi.getTime({}).then(res => {
        if (this.getTimeStr(res.data.timestamp).dataStr === this.formInline.date) {
          let cstr = '银证转账、银期转账、银信转账、银衍转账、银贵转账、中登备付金划款、基金认申购、网下新股申购(上海)、网下新股申购(深圳)、网下新债申购'
          let result = false
          if (cstr.indexOf(this.activeStr) !== -1) {
            result = this.timeCompare(res.data.timestamp, '13:30:00')
          } else {
            result = this.timeCompare(res.data.timestamp, '15:00:00')
          }
          if (result) {
            this.warning_show = true
          } else {
            this.warning_show = false
          }
        } else {
          this.warning_show = false
        }
      })
    },

    cccc(val) {
      // console.log(val);
    },
    getSubmitOrder() {
      pageApi.getSubmitOrder({}).then(({ data: res }) => {
        this.submitOrder = res.data || new Date().getTime()
      })
        .catch((err) => console.log('getSubmitOrder err', err))
    },

    // 获取服务器时间
    getServerData() {
      pageApi
        .getTime({})
        .then(({ data: res }) => {
          // console.log(res.timestamp);
          // console.log(Date.now());
          this.nowTime = res.timestamp
          // this.formInline.date = res.timestamp;
          this.getTody(res.timestamp)
          this.pickerOptions = {
            disabledDate(time) {
              return time.getTime() < res.timestamp - 24 * 60 * 60 * 1000
            }
          }
        })
        .catch((err) => console.log('is msg err', err))
    },

    moneyFocus() {
      this.commitRules.money[0].pattern = this.moneyValidateDefalut
      if (this.formInline.money && this.formInline.money.includes(',')) {
        this.formInline.money = this.formInline.money.toString().replace(/,/gi, '') - 0
      }
    },
    moneyBlur() {
      this.commitRules.money[0].pattern = this.moneyValidateDefalut
      let reg = this.moneyValidate.test(this.formInline.money)
      if (reg && this.formInline.money) {  //失去焦点正则为true
        this.commitRules.money[0].pattern = ''
        // this.formInline.money = moneyThousand(this.formInline.money)
        this.formInline.money = moneyYuan(this.formInline.money)
        this.$refs.formInline.validate()
      }
    },
    getTody(val) {
      let tody = new Date(val)
      let y = tody.getFullYear().toString()
      let m = (tody.getMonth() + 1).toString().padStart('2', '0')
      let d = tody.getDate().toString().padStart('2', '0')
      let str = y + '-' + m + '-' + d
      this.formInline.date = str
    },

    getTimeStr(val) {
      let tody = new Date(val)
      let y = tody.getFullYear().toString()
      let m = (tody.getMonth() + 1).toString().padStart('2', '0')
      let d = tody.getDate().toString().padStart('2', '0')
      let str = y + '-' + m + '-' + d
      return {
        dataStr: str,
        timestmp: val
      }
    },
    timeCompare(now, t) {
      console.log('now', now)
      let nowTime = new Date(now)
      let year = nowTime.getFullYear().toString()
      let month = (nowTime.getMonth() + 1).toString().padStart('2', '0')
      let date = nowTime.getDate().toString().padStart('2', '0')
      var ctimestr = year + '/' + month + '/' + date + ' ' + t
      var ctime = Date.parse(ctimestr)
      console.log('ctime',ctime);
      if (nowTime >= ctime) {
        return true
      } else {
        return false
      }
    },
    getAcc(params) {
      this.getpayeeAcc(params)
      this.getpayerAcc(params)
    },
    // 收款账户
    getpayeeAcc(params) {
      console.log('获取收款账户')
      accountApi
        [this.payeeApi](params)
        .then(res => {
          if (res.data.status == 200) {
            // console.log(res.data.data.list);
            let data = res.data.data.list
            // this.accArr = res.data.data.list;
            let data2 = []
            let data3 = []
            if (this.payeeApi == 'getZqAccList' || this.payeeApi == 'getQhAccList') {
              data.forEach(item => {
                let obj = {}
                obj.accoNo = item.capitalAccount || ''
                obj.accoName = item.accoName || ''
                obj.accoBank = item.openExchange || ''
                obj.hvpsNo = item.hvpsNo || ''
                obj.accoType = this.payeeApi || ''
                obj.id = item.id || ''
                data2.push(obj)
              })
            }
            let code = this.formInline.type
            if (this.payeeApi == 'getYhjAccList' && ['gm040701', 'gm040706'].includes(code)) {
              // 银行间账户-中债账户
              data.forEach(item => {
                let obj = {}
                obj.accoNo = item.ccdcCapitalAccount || ''
                obj.accoName = item.ccdcCapitalName || ''
                obj.accoBank = item.ccdcCapitalBank || ''
                obj.hvpsNo = ''
                obj.accoType = this.payeeApi + 'Zz' || ''
                obj.id = item.id || ''
                data3.push(obj)
              })
            }
            if (this.payeeApi == 'getYhjAccList' && ['gm040703', 'gm040705'].includes(code)) {
              // 银行间账户-上清所账户
              data.forEach(item => {
                let obj = {}
                obj.accoNo = item.shchCapitalAccount || ''
                obj.accoName = item.shchCapitalName || ''
                obj.accoBank = item.shchCapitalBank || ''
                obj.hvpsNo = ''
                obj.accoType = this.payeeApi + 'Sq' || ''
                obj.id = item.id || ''
                data3.push(obj)
              })
            }
            // console.log('data',data);
            // console.log('data2',data2);
            if (this.payeeApi == 'getZqAccList' || this.payeeApi == 'getQhAccList') {
              this.$nextTick(() => {
                if (this.$refs.selectAccount2) {
                  this.$refs.selectAccount2.init(data2)
                }
              })
            } else if (this.payeeApi == 'getYhjAccList') {
              this.$nextTick(() => {
                if (this.$refs.selectAccount2) {
                  this.$refs.selectAccount2.init(data3)
                }
              })
            } else {
              this.$nextTick(() => {
                if (this.$refs.selectAccount2) {
                  this.$refs.selectAccount2.init(data)
                }
              })
            }
          }
        })
        .catch(() => {

        })
    },
    // 付款账户
    getpayerAcc(params) {
      console.log('获取付款账户')
      accountApi
        [this.payerApi](params)
        .then(res => {
          if (res.data.status == 200) {
            // console.log(res.data.data.list);
            let data = res.data.data.list
            // this.accArr = res.data.data.list;
            let data2 = []
            let data3 = []
            if (this.payerApi == 'getZqAccList' || this.payerApi == 'getQhAccList') {
              data.forEach(item => {
                let obj = {}
                obj.accoNo = item.capitalAccount || ''
                obj.accoName = item.accoName || ''
                obj.accoBank = item.openExchange || ''
                obj.hvpsNo = item.hvpsNo || ''
                obj.accoType = this.payerApi || ''
                obj.id = item.id || ''
                data2.push(obj)
              })
            }
            let code = this.formInline.type
            if (this.payerApi == 'getYhjAccList' && ['gm040702', 'gm040705'].includes(code)) {
              // 银行间账户-中债账户
              data.forEach(item => {
                let obj = {}
                obj.accoNo = item.ccdcCapitalAccount || ''
                obj.accoName = item.ccdcCapitalName || ''
                obj.accoBank = item.ccdcCapitalBank || ''
                obj.hvpsNo = ''
                obj.accoType = this.payerApi + 'Zz' || ''
                obj.id = item.id || ''
                data3.push(obj)
              })
            }
            if (this.payerApi == 'getYhjAccList' && ['gm040704', 'gm040706'].includes(code)) {
              // 银行间账户-上清所账户
              data.forEach(item => {
                let obj = {}
                obj.accoNo = item.shchCapitalAccount || ''
                obj.accoName = item.shchCapitalName || ''
                obj.accoBank = item.shchCapitalBank || ''
                obj.hvpsNo = ''
                obj.accoType = this.payerApi + 'Sq' || ''
                obj.id = item.id || ''
                data3.push(obj)
              })
            }
            // console.log('data3',data3);
            if (this.payerApi == 'getZqAccList' || this.payerApi == 'getQhAccList') {
              this.$nextTick(() => {
                if (this.$refs.selectAccount1) {
                  this.$refs.selectAccount1.init(data2)
                }
              })
            } else if (this.payerApi == 'getYhjAccList') {
              this.$nextTick(() => {
                if (this.$refs.selectAccount1) {
                  this.$refs.selectAccount1.init(data3)
                }
              })
            } else {
              this.$nextTick(() => {
                if (this.$refs.selectAccount1) {
                  this.$refs.selectAccount1.init(data)
                }
              })
            }
          }
        })
        .catch(() => {

        })
    },
    sendDataObj(data) {
      // console.log(data);
      if (data) {
        this.startTransfer = true
        let val = data.fundCode
        // console.log(this.api)
        if (this.api) this.getZqAccountSELECT(val, this.api)
      } else {
        this.startTransfer = false
        this.processUse_show = false
        this.formInline.processUse = ''
      }
      // if(["040203","040403","040503","040601","040602","040603","0407","040701","040702","040703","040704","040705","040706"].includes(this.formInline.type)){
      if (data) {
        let fundCode = data.fundCode
        // 只展示规定账户类型
        // let params = {fundCode:fundCode};
        // this.getAcc(params);
        // 展示全部账户类型，默认展示规定账户类型
        let params2 = { productCode: fundCode }
        this.getAccounts(params2)
      }
      this.formInline.payerAcconame = ''
      this.formInline.payeeAcconame = ''
      // }
      this.$message.closeAll()
      if (data == '') {
        this.submit_btn = false
        return
      }
      if (!data.operatorName) data.operatorName = ''
      let flag = data.operatorName.includes('国泰君安') || false
      if (!flag) {
        this.isGtja = 0
        this.processUse_show = true;
        if(this.formInline.type=='gm040101'){
          this.formInline.processUse = "银转证"
        }else if(this.formInline.type=='gm040102'){
          this.formInline.processUse = "证转银"
        }else if(this.formInline.type=='gm040201'){
          this.formInline.processUse = "银转期"
        }else if(this.formInline.type=='gm040202'){
          this.formInline.processUse = "期转银"
        }else if(this.formInline.type=='gm040301'){
          this.formInline.processUse = "银转信"
        }else if(this.formInline.type=='gm040302'){
          this.formInline.processUse = "信转银"
        }else if(this.formInline.type=='gm040401'){
          this.formInline.processUse = "银转衍"
        }else if(this.formInline.type=='gm040402'){
          this.formInline.processUse = "衍转银"
        }else if(this.formInline.type=='gm040501'){
          this.formInline.processUse = "银转贵"
        }else if(this.formInline.type=='gm040502'){
          this.formInline.processUse = "贵转银"
        }
        // this.submit_btn = true
        // this.$message.error('非国泰君安外包产品，请发起自定义划款流程！')
      } else {
        this.isGtja = 1
        this.processUse_show = false
        this.formInline.processUse = ''
        // this.submit_btn = false
      }
    },
    getAccounts(params) {
      this.accArr = []
      accountApi
        .getAllAccList(params)
        .then(res => {
          if (res.data.status == 200) {
            // console.log(res.data.data);
            let data = res.data.data
            this.accArr = res.data.data
            this.$nextTick(() => {
              if (this.$refs.selectAccount1) {
                this.$refs.selectAccount1.init(data)
              }
              if (this.$refs.selectAccount2) {
                this.$refs.selectAccount2.init(data)
              }
            })
          }
        })
        .catch(() => {

        })
    },
    getAccountInfo1(val) {
      // console.log(val);
      this.formInline.payerAccount = val.accoNo
      this.formInline.payerBank = val.accoBank
    },
    getAccountInfo2(val) {
      // console.log(val);
      this.formInline.payeeAccount = val.accoNo || ''
      this.formInline.payeeBank = val.accoBank || ''
      this.formInline.paymentSystemNumber = val.hvpsNo || ''
    },
    // 根据产品名称选择经济商
    //查询经纪商
    getZqAccountSELECT(data, api) {
      let params = { fundCode: data }
      bizBeginApi[api](params).then(res => {
        this.borkerInfos = []
        this.formInline.broker = ''
        if (res.data.status === 200) {
          let arr = res.data.data
          for (let i of arr) {
            let obj = {}
            obj.value = (i.openStruc || ' 无 ') + (i.openExchange ? '( ' + i.openExchange + ' )' : '( 无 )')
            obj.name = (i.openStruc || ' 无 ') + (i.openExchange ? '( ' + i.openExchange + ' )' : '( 无 )')
            obj.accoNo = i.capitalAccount || ''
            obj.accoName = i.accoName || ''
            obj.accoBank = i.openExchange || ''
            obj.hvpsNo = i.hvpsNo || ''
            this.borkerInfos.push(obj)
          }
        }
      }).catch(() => {
      })
    },
    brokerChange(data) {
      // 选择经纪商带出账户信息
      // console.log(data);
      if (data && (this.payeeApi == 'getZqAccList' || this.payeeApi == 'getQhAccList')) {
        this.formInline.payeeAcconame = data.accoName || ''
        this.formInline.payeeAccount = data.accoNo || ''
        this.formInline.payeeBank = data.accoBank || ''
        this.formInline.paymentSystemNumber = data.hvpsNo || ''
      }
      // 银证转账-证转银
      if (this.formInline.type == 'gm040102') {
        let arr = this.accArr.filter(item => {
          return item.accoType == 'fiduciary'
        })
        if (arr.length) {
          this.formInline.payeeAcconame = arr[0].accoName || ''
          this.formInline.payeeAccount = arr[0].accoNo || ''
          this.formInline.payeeBank = arr[0].accoBank || ''
          this.formInline.paymentSystemNumber = arr[0].hvpsNo || ''
        }
      }
      // 银期转账-期转银
      if (this.formInline.type == 'gm040202') {
        let arr = this.accArr.filter(item => {
          return item.accoType == 'fiduciary'
        })
        if (arr.length) {
          this.formInline.payeeAcconame = arr[0].accoName || ''
          this.formInline.payeeAccount = arr[0].accoNo || ''
          this.formInline.payeeBank = arr[0].accoBank || ''
          this.formInline.paymentSystemNumber = arr[0].hvpsNo || ''
        }
      }
      // 银期转账-银转期(手工入金)
      if (this.formInline.type == 'gm040203') {
        // 收款
        let payeeArr = this.accArr.filter(item => {
          return item.accoType == 'other'
        })
        if (payeeArr.length) {
          this.formInline.payeeAcconame = payeeArr[0].accoName || ''
          this.formInline.payeeAccount = payeeArr[0].accoNo || ''
          this.formInline.payeeBank = payeeArr[0].accoBank || ''
          this.formInline.paymentSystemNumber = payeeArr[0].hvpsNo || ''
        }
        // 付款
        let payerArr = this.accArr.filter(item => {
          return item.accoType == 'fiduciary'
        })
        if (payerArr.length) {
          this.formInline.payerAcconame = payerArr[0].accoName || ''
          this.formInline.payerAccount = payerArr[0].accoNo || ''
          this.formInline.payerBank = payerArr[0].accoBank || ''
        }
      }
    },
    //提交事件
    onSubmit(data) {
      // console.log(this.formInline.type);
      let self = this
      this.$refs[data].validate((valid) => {
        if (valid) {
          self.submit_btn = true //按钮禁用
          this.submitData()
        } else {
          self.submit_btn = false //按钮启用
          return false
        }
      })
    },
    // 清除
    resetForm(formName) {
      var self = this
      self.$refs[formName].resetFields()

      this.$nextTick(() => {
        this.getTody(this.nowTime)
      })
    },
    //tab切换
    handleClick(tab, event) {
      this.activeStr = tab.label
      let id = tab.name.split('_')[0]
      if (id == '1' || id == '4') {
        this.jisxz = true
      } else {
        this.jisxz = false
      }
      this.accountCodes = this.accountCodesTemp
      this.api = ''
      this.resetForm('formInline')
      this.getAccountTypes(tab.name)
      this.activeNames = []
      let lab = tab.label
      // this.getTody()
      if (lab === '银证转账') {
        this.is_skfzh_show = true
      } else {
        this.is_skfzh_show = false
      }
      if (lab === '银证转账') {
        this.is_yg_show = false
        this.is_yy_show = false
        this.is_yx_show = false
        this.is_yq_show = false
        this.is_yz_show = true
        this.api = 'getZqAccountSELECT'

      } else if (lab === '银期转账') {
        this.is_yg_show = false
        this.is_yy_show = false
        this.is_yx_show = false
        this.is_yq_show = true
        this.is_yz_show = false
        this.api = 'getZqAccountSELECTYH'

      } else if (lab === '银信转账') {
        this.is_yg_show = false
        this.is_yy_show = false
        this.is_yx_show = true
        this.is_yq_show = false
        this.is_yz_show = false
        // this.borkerInfos = this.borkerInfos2;

      } else if (lab === '银衍转账') {
        this.is_yg_show = false
        this.is_yy_show = true
        this.is_yx_show = false
        this.is_yq_show = false
        this.is_yz_show = false
        // this.borkerInfos = this.borkerInfos2;

      } else if (lab === '银贵转账') {
        this.is_yg_show = true
        this.is_yy_show = false
        this.is_yx_show = false
        this.is_yq_show = false
        this.is_yz_show = false
        // this.borkerInfos = this.borkerInfos2;
      }
      if (lab === '中登备付金划款' || lab === '银行间资金转账') {
        this.jjs_show = false
      } else {
        this.jjs_show = true
      }
      this.handleDateChange()
    },
    //查询产品信息
    getProductInfo() {
      bizBeginApi.getProductFund().then(res => {
        // console.log('resdata', res)
        if (res.data.message === 'success') {
          let arr = res.data.data
          this.accountCodes = []
          this.accountCodesTemp = []
          this.accountCodesTemp = arr
          this.accountCodes = arr
        } else {
          this.accountCodes = []
          this.accountCodesTemp = []
          this.$message.closeAll()
          this.$message.error('查询产品信息失败')
        }
      }).catch(() => {
        this.$message.closeAll()
        this.$message.error('查询产品信息失败')
      })
    },
    //查询经纪商
    getBrokerInfo() {
      let params = 'brokerType'
      bizBeginApi.getBrokerInfo(params).then(res => {
        if (res.data.message === 'success') {
          let arr = res.data.data
          this.borkerInfos2 = []
          for (let i = 0; i < arr.length; i++) {
            let obj = {}
            obj.value = arr[i].dimCde + '_' + arr[i].dimNme
            obj.name = arr[i].dimNme
            this.borkerInfos2.push(obj)
          }
          // console.log('arr', arr)
        } else {
          this.borkerInfos2 = []
          this.$message.closeAll()
          this.$message.error('查询经纪商信息失败')
        }
      }).catch(() => {
        this.$message.closeAll()
        this.$message.error('查询经纪商信息失败')
      })
    },
    //查询转账类型
    getTransferType() {
      let params = 'transCmdType'
      this.tranferTypes = []
      this.accountTypes = []
      bizBeginApi.getTransferType(params).then(res => {
        if (res.data.message === 'success') {
          let data = res.data.data
          for (let i = 0; i < data.length; i++) {
            if (data[i].parentId === null || data[i].parentId === undefined) {
              this.tranferTypes.push(data[i])
            } else {
              this.accountTypes.push(data[i])
            }
          }
          let arr = this.accountTypes
          let id = this.tranferTypes[0].id
          this.activeName = this.tranferTypes[0].id + '_' + this.tranferTypes[0].dimValue
          this.activeStr = this.tranferTypes[0].dimNme
          this.accountTypes2 = []
          for (let i = 0; i < arr.length; i++) {
            if (arr[i].parentId === id) {
              this.accountTypes2.push(arr[i])
            }
          }
          //  this.formInline.type = this.accountTypes2[0].dimValue;
          if (this.accountTypes2.length) {
            this.formInline.type = this.accountTypes2[0].dimValue
          } else {
            this.formInline.type = this.tranferTypes[0].dimValue
          }

        } else {
          this.tranferTypes = []
          this.accountTypes = []
          this.$message.closeAll()
          this.$message.error('查询转账指令类型信息失败')
        }
      }).catch(() => {
        this.$message.closeAll()
        this.$message.error('查询转账指令类型信息失败')
      })
    },
    //查询转账类型-二级
    getAccountTypes(accountId) {
      let arr = this.accountTypes
      let id = accountId.split('_')[0]
      let cmdCode = accountId.split('_')[1]
      this.accountTypes2 = []
      for (let i = 0; i < arr.length; i++) {
        if (arr[i].parentId + '' === id) {
          this.accountTypes2.push(arr[i])
        }
      }
      //  console.log(this.accountTypes2);
      // this.formInline.type = this.accountTypes2[0].dimValue;
      if (this.accountTypes2.length) {
        this.formInline.type = this.accountTypes2[0].dimValue
      } else {
        this.formInline.type = cmdCode
      }
    },
    //获取defineId
    getDefineId() {
      bizBeginApi.getDefineId('Process_transfer').then(res => {
        if (res.data.data) {
          let resultData = res.data.data
          let formPath = resultData.formPath
          let id = resultData.porcessDefineModel.id
          this.definedId = id
        } else {
          this.$message.closeAll()
          this.$message.error('初始化信息失败')
        }
      }).catch(() => {
        this.$message.closeAll()
        this.$message.error('初始化信息失败')
      })
    },
    //  resetForm(){
    //     var self = this;
    //     let formName = 'formInline';
    //     self.$refs[formName].resetFields();
    //  },
    getInitTransFlow() {
      bizBeginApi.startTransfer().then(res => {
        if (res.data.message === 'success') {
          let data = res.data.data
          let id = data.id
          let pfomBiznum = data.pfomBiznum
          this.submitData(id, pfomBiznum)
        } else {
          this.borkerInfos = []
          this.$message.closeAll()
          this.$message.error('初始化信息失败')
        }
      }).catch(() => {
        this.$message.closeAll()
        this.$message.error('初始化信息失败')
      })
    },
    //提交列表数据
    submitData() {

      let self = this
      let params = Object.assign({}, self.formInline)
      let paramData = {}
      paramData.cmdCode = params.type
      paramData.fundCode = params.accountCode.split('_')[0]
      paramData.fundName = params.accountCode.split('_')[1]
      // this.is_yz_show || this.is_yq_show
      //  if(!this.jisxz){
      paramData.brokerName = params.broker
      paramData.brokerCode = params.broker
      //  }else{
      //     paramData.brokerName = params.broker.split('_')[2];
      //     paramData.brokerCode = params.broker.split('_')[0]+"_"+params.broker.split('_')[1];
      //  }
      if (this.formInline.money && this.formInline.money.includes(',')) {
        params.money = this.formInline.money.toString().replace(/,/gi, '')
      }
      paramData.transferAmount = params.money || ''
      paramData.transferCur = 'CNY'
      paramData.transferReqdate = params.date
      paramData.remark = params.remark
      paramData.processUse = params.processUse
      paramData.payerAcconame = params.payerAcconame
      paramData.payerAccount = params.payerAccount
      paramData.payerBank = params.payerBank
      paramData.payeeAcconame = params.payeeAcconame
      paramData.payeeAccount = params.payeeAccount
      paramData.payeeBank = params.payeeBank
      paramData.paymentSystemNumber = params.paymentSystemNumber
      // let sendData = {};
      // sendData.formData = paramData;

      // let taskExcuteCmdMode = {taskExcuteCmdType:'Normal'};
      // sendData.taskExcuteCmdMode = taskExcuteCmdMode;

      //清楚空字段
      for (let k in paramData) {
        if (!paramData[k] && String(paramData[k]) !== '0') {
          delete paramData[k]
        }
      }
      self.submit_btn = true //按钮禁用
      let id = this.definedId
      //sendData= JSON.stringify(sendData);

      paramData.submitOrder = this.submitOrder
      bizBeginApi.startTransfer(paramData).then(res => {
        let data = res.data.data
        if (res.data.status === 200) {
          this.$message.closeAll()
          this.$message({
            type: 'success',
            message: '操作成功'
          })
          this.resetForm('formInline')
          //this.formInline.type = this.accountTypes2[0].dimValue;
          this.$emit('transferCheckClick', {
            data: [],
            flag: true
          })
        } else {
          this.$message.closeAll()
          this.$message({
            type: 'error',
            message: res.data.message || '操作失败'
          })

        }
        self.submit_btn = false //按钮启用
      }).catch(() => {
        this.$message.closeAll()
        this.$message.error('操作失败')
        self.submit_btn = false //按钮启用
      })

    },
    handleChange(val) {
      // console.log(val);
    },
    getQhAccount() {
      if (!this.formInline.accountCode) {
        this.$message.closeAll()
        this.$message.error('请先选择产品')
        return
      }
      let params = {}
      this.borkerInfos = []
      params.fundCode = this.formInline.accountCode.split('_')[0]
      bizBeginApi.getQhAccount(params).then(res => {
        //  console.log(res, 'res')
        if (res.data.status === 200) {
          let arr = res.data.data
          for (let i = 0; i < arr.length; i++) {
            let obj = {}
            if (arr[i].openStruc && arr[i].openExchange) {
              obj.value = arr[i].openStruc + '（' + arr[i].openExchange + '）'
              obj.name = arr[i].openStruc + '（' + arr[i].openExchange + '）'
              this.borkerInfos.push(obj)
            }
          }
        } else {
          this.borkerInfos = []
          this.$message.closeAll()
          this.$message.error('初始化经纪商信息失败')
        }
      }).catch(() => {
        this.borkerInfos = []
        this.$message.closeAll()
        this.$message.error('初始化经纪商信息失败')
      })
    },
    getZqAccount() {
      if (!this.formInline.accountCode) {
        this.$message.closeAll()
        this.$message.error('请先选择产品')
        return
      }
      let params = {}
      this.borkerInfos = []
      params.fundCode = this.formInline.accountCode.split('_')[0]
      bizBeginApi.getZqAccount(params).then(res => {
        if (res.data.status === 200) {
          let arr = res.data.data
          for (let i = 0; i < arr.length; i++) {
            let obj = {}
            if (arr[i].openStruc && arr[i].openExchange) {
              obj.value = arr[i].openStruc + '（' + arr[i].openExchange + '）'
              obj.name = arr[i].openStruc + '（' + arr[i].openExchange + '）'
              this.borkerInfos.push(obj)
            }
          }

        } else {
          this.borkerInfos = []
          this.$message.closeAll()
          this.$message.error('初始化经纪商信息失败')
        }
      }).catch(() => {
        this.borkerInfos = []
        this.$message.closeAll()
        this.$message.error('初始化经纪商信息失败')
      })
    },
    fundChange(val) {
      if (this.is_yz_show) {
        this.getZqAccount()

      } else if (this.is_yq_show) {
        this.getQhAccount()
      }

    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">

</style>

<style rel="stylesheet/scss" lang="scss" scoped>

.commitClass {
  position: relative;
  width: 520px;
  max-width: 100%;
  padding: 10px 20px 0;
  margin: 0 auto;
  // overflow: hidden;
  margin-top: 20px;
}

.el_form_item {
  width: 300px;
  margin-top: 10px;
}
</style>

<style rel="stylesheet/scss" lang="scss">
.inputTableStyle {
  position: relative;

  .selectTableStyle {
    position: absolute;
    width: 100%;
    margin-top: 2px;
    z-index: 9999;

    .table {
      border: 1px solid #f1f1f1;
      box-shadow: 0 0 0 1px #f1f1f1;
    }
  }
}

/* 修复input 背景不协调 和光标变色 */
/* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

$bg: #283443;
$light_gray: #eee;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;

    &::first-line {
      color: $light_gray;
    }
  }
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;

    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      color: $light_gray;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }
  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}


input::-webkit-outer-spin-button, input::-webkit-inner-spin-button {
  -webkit-appearance: none;
}

input[type="number"] {
  -moz-appearance: textfield;
}

.el-steps--simple {
  width: 60%;
  height: 25px;
  margin: 0 auto;
  background-color: white;
}

.el-step.is-simple .el-step__title {
  font-size: 14px;
}

.el-step__title {
  font-size: 14px;
}

.el-icon-circle-check:before {
  color: #67C23A;
}

.el-form--label-left .el-form-item__label {
  text-align: left;
}

.el-collapse-item__header {
  color: #409EFF;
}

</style>


<template>
  <div>
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane v-for="item in tranferTypes" :key="item.dimValue" :label="item.dimNme"
                   :name="item.id+'_'+item.dimValue">
      </el-tab-pane>
    </el-tabs>
    <el-collapse v-model="activeNames">
      <el-collapse-item name="1">
        <template slot="title" style="color: #409EFF;font-weight: bold">
          <i class="el-icon-reading"></i>操作指南
        </template>
        <div style="margin-left: 50px;" v-show="is_jjrsg_show">
          <el-row>
            <el-col :span="2"><span style="font-weight: bold">业务场景:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">管理人拟将基金投资于场外开放式基金，如为代销申购、认购基金，第一次投资前建议管理人咨询托管人即将通过哪家代销是否能够进行划款。
              </div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">交互流程:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">
                1.填写划款信息：管理人的划款经办人员（交易员、基金运营部估值核算岗）登录运营管理平台【账户划款】->【投资指令】->【提交投资指令】界面，根据具体投资业务类型，填写划款信息。
              </div>
              <div style="width:80%;margin-left:10px">
                2.上传场外投资所需材料：管理人的划款经办人员在运营管理平台【账户划款】->【投资指令】->【提交投资指令】界面，点击“浏览”，上传场外投资所需材料（一般为开户确认书、认申购交易申请单），并点击“提交划款”。
              </div>
              <div style="width:80%;margin-left:10px">
                3.复核划款指令：管理人划款复核人员（基金运营部估值核算岗）进入【账户划款】->【跟踪待办】，选择该笔投资指令，确认复核界面中的划款指令信息（如点击“复核通过”，指令信息将传递至托管人执行划款操作；如点击“复核不通过”，指令将退回经办人员修改重签或撤销）。我部会对管理人提交的划款指令及相关附件进行审核。
              </div>
              <div style="width:80%;margin-left:10px">
                4.管理人（基金运营部估值核算岗）需要检查投资交易系统即将转出的现金头寸是否冻结，若没有冻结需要提醒管理人（基金经理、交易员）在投资交易系统中下单，有特殊业务系统无法根据成交信息冻结的，需要由管理人（基金运营部估值核算岗）进行手工冻结。
              </div>
              <div style="width:80%;margin-left:10px">
                5.审核划款指令（基金运营部总监）：管理人划款审核人员（如有）进入【账户划款】->【跟踪待办】，选择该笔投资指令，确认审核界面中的划款指令信息（如点击“审核通过”，指令信息将传递至托管人执行划款操作；如点击“审核不通过”，指令将退回经办人员修改重签或撤销）。我部会对管理人提交的划款指令及相关附件进行审核
              </div>
              <div style="width:80%;margin-left:10px">
                6.如不满足划款要求或指令错误：我部会退回该笔投资划款指令至管理人的操作人员处，并在“处理意见”栏注明退回原因。“处理意见”会通过手机短信的形式发送给管理人。
              </div>
              <div style="width:80%;margin-left:10px">
                7.追加补充附件：如场外投资所需材料不完整，我部会联系管理人划款经办人员沟通待补充材料并开放追加，管理人划款经办可通过运营管理平台【账户划款】->【跟踪待办】追加补充附件。
              </div>
              <div style="width:80%;margin-left:10px">
                8.重新提交、复核、审核指令：管理人的划款经办人员更正划款指令信息及相关附件后，在运营管理平台【账户划款】->【投资指令】->【提交投资指令】界面，重新提交划款指令，并由划款复核人员复核、审核人员审核。
              </div>
              <div style="width:80%;margin-left:10px">
                9.管理人划款操作人员（包括划款经办、复核人员及审核人员）可通过运营管理平台【账户划款】->【跟踪待办】，实时查询划款进度。如您发现有相关指令被退回，请及时查询退回原因，如有问题请随时联系我部
              </div>
              <div style="width:80%;margin-left:10px">
                10.管理人（基金运营部估值核算岗）需要检查投资交易系统资金冻结情况，若系统没有自动调整的，需要在日终清算时调整或盘中在管理人（基金经理、交易员）允许的情况下进行调整。
              </div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">注意事项:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">1.请于划款日13：00前向我部提交完整、有效的场外投资划款指令及附件材料。</div>
              <div style="width:80%;margin-left:10px">
                2.建议管理人尽早提交投资指令与相关材料，以便我部尽快审核与处理划款事宜。为保证场外投资划款的时效性，请管理人务必最晚于场外投资划款日的13:00前提交完整、有效的划款指令及附件材料，并确保此时基金的银行托管账户内有足够的资金余额。
              </div>
              <div style="width:80%;margin-left:10px">3.由于每笔场外投资划款有其特殊性，请将上传的材料尤其扫描件必须清晰且不允许涂改。</div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">反馈时效:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">指令及时、材料齐备的情况下，我部于划款日当天完成资金划。</div>
              <div style="width:80%;margin-left:10px">管理人可通过运营管理平台【账户划款】->【跟踪待办】实时查询划款进度。</div>
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

        <div style="margin-left: 50px;" v-show="is_cktz_show">
          <el-row>
            <el-col :span="2"><span style="font-weight: bold">业务场景:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">
                管理人拟将基金投资于场外产品，即通过场外投资方式投资定期存款。定期存款投资前需要管理人先选定定存银行并开户，之后在定存当天与定存银行签署定存协议。
              </div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">交互流程:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">
                1.填写划款信息：管理人的划款经办人员（交易员、基金运营部估值核算岗）登录运营管理平台【账户划款】->【投资指令】->【提交投资指令】界面，根据具体投资业务类型，填写划款信息。
              </div>
              <div style="width:80%;margin-left:10px">
                2.上传场外投资所需材料：管理人的划款经办人员在运营管理平台【账户划款】->【投资指令】->【提交投资指令】界面，点击“浏览”，上传场外投资所需材料（定存协议、定存框架协议（如有）），并点击“提交划款”。
              </div>
              <div style="width:80%;margin-left:10px">
                3.复核划款指令：管理人划款复核人员（基金运营部估值核算岗）进入【账户划款】->【跟踪待办】，选择该笔投资指令，确认复核界面中的划款指令信息（如点击“复核通过”，指令信息将传递至托管人执行划款操作；如点击“复核不通过”，指令将退回经办人员修改重签或撤销）。我部会对管理人提交的划款指令及相关附件进行审核。
              </div>
              <div style="width:80%;margin-left:10px">
                4.管理人（基金运营部估值核算岗）需要检查投资交易系统即将转出的现金头寸是否冻结，若没有冻结需要提醒管理人（基金经理、交易员）在投资交易系统中下单，有特殊业务系统无法根据成交信息冻结的，需要由管理人（基金运营部估值核算岗）进行手工冻结。
              </div>
              <div style="width:80%;margin-left:10px">
                5.审核划款指令（基金运营部总监）：管理人划款审核人员（如有）进入【账户划款】->【跟踪待办】，选择该笔投资指令，确认审核界面中的划款指令信息（如点击“审核通过”，指令信息将传递至托管人执行划款操作；如点击“审核不通过”，指令将退回经办人员修改重签或撤销）。我部会对管理人提交的划款指令及相关附件进行审核。
              </div>
              <div style="width:80%;margin-left:10px">
                6.如不满足划款要求或指令错误：我部会退回该笔投资划款指令至管理人的操作人员处，并在“处理意见”栏注明退回原因。“处理意见”会通过手机短信的形式发送给管理人。
              </div>
              <div style="width:80%;margin-left:10px">
                7.追加补充附件：如场外投资所需材料不完整，我部会联系管理人划款经办人员沟通待补充材料并开放追加，管理人划款经办可通过运营管理平台【账户划款】->【跟踪待办】追加补充附件。
              </div>
              <div style="width:80%;margin-left:10px">
                8.重新提交、复核、审核指令：管理人的划款经办人员更正划款指令信息及相关附件后，在运营管理平台【账户划款】->【投资指令】->【提交投资指令】界面，重新提交划款指令，并由划款复核人员复核、审核人员审核。
              </div>
              <div style="width:80%;margin-left:10px">
                9.管理人划款操作人员（包括划款经办、复核人员及审核人员）可通过运营管理平台【账户划款】->【跟踪待办】，实时查询划款进度。如您发现有相关指令被退回，请及时查询退回原因，如有问题请随时联系我部。
              </div>
              <div style="width:80%;margin-left:10px">
                10.管理人（基金运营部估值核算岗）需要检查投资交易系统资金冻结情况，若系统没有自动调整的，需要在日终清算时调整或盘中在管理人（基金经理、交易员）允许的情况下进行调整。
              </div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">注意事项:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">1.请于划款日13：00前向我部提交完整、有效的场外投资划款指令及附件材料。</div>
              <div style="width:80%;margin-left:10px">
                2.建议管理人尽早提交投资指令与相关材料，以便我部尽快审核与处理划款事宜。为保证场外投资划款的时效性，请管理人务必最晚于场外投资划款日的13:00前提交完整、有效的划款指令及附件材料，并确保此时基金的银行托管账户内有足够的资金余额。
              </div>
              <div style="width:80%;margin-left:10px">3.由于每笔场外投资划款有其特殊性，请将上传的材料尤其扫描件必须清晰且不允许涂改。</div>
              <div style="width:80%;margin-left:10px">4.管理人应留意单一银行定存比例上限。</div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">反馈时效:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">指令及时、材料齐备的情况下，我部于划款日当天完成资金划拨。</div>
              <div style="width:80%;margin-left:10px">管理人可通过运营管理平台【账户划款】->【跟踪待办】实时查询划款进度。</div>
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

        <div style="margin-left: 50px;" v-show="is_wxxgsgSh_show">
          <el-row>
            <el-col :span="2"><span style="font-weight: bold">业务场景:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">管理人拟将基金投资于网下新股业务，由管理人（基金经理、投资研究、交易员）进行网下申报准备。</div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">交互流程:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">
                1.填写划款信息：管理人的划款经办人员（基金经理、投资研究、交易员、基金运营部估值核算岗）登录运营管理平台【账户划款】->【投资指令】->【提交投资指令】界面，根据具体投资业务类型，填写划款信息。
              </div>
              <div style="width:80%;margin-left:10px">
                2.上传场外投资所需材料：管理人的划款经办人员在运营管理平台【账户划款】->【投资指令】->【提交投资指令】界面，点击“浏览”，上传场外投资所需材料（网下新股申购审批单），并点击“提交划款”。
              </div>
              <div style="width:80%;margin-left:10px">
                3.复核划款指令：管理人划款复核人员（基金运营部估值核算岗）进入【账户划款】->【跟踪待办】，选择该笔投资指令，确认复核界面中的划款指令信息（如点击“复核通过”，指令信息将传递至托管人执行划款操作；如点击“复核不通过”，指令将退回经办人员修改重签或撤销）。我部会对管理人提交的划款指令及相关附件进行审核。
              </div>
              <div style="width:80%;margin-left:10px">
                4.管理人（基金运营部估值核算岗）需要检查投资交易系统即将转出的现金头寸是否冻结，若没有冻结需要提醒管理人（基金经理、交易员）在投资交易系统中下单，有特殊业务系统无法根据成交信息冻结的，需要由管理人（基金运营部估值核算岗）进行手工冻结。
              </div>
              <div style="width:80%;margin-left:10px">
                5.审核划款指令（基金运营部总监）：管理人划款审核人员（如有）进入【账户划款】->【跟踪待办】，选择该笔投资指令，确认审核界面中的划款指令信息（如点击“审核通过”，指令信息将传递至托管人执行划款操作；如点击“审核不通过”，指令将退回经办人员修改重签或撤销）。我部会对管理人提交的划款指令及相关附件进行审核。
              </div>
              <div style="width:80%;margin-left:10px">
                6.如不满足划款要求或指令错误：我部会退回该笔投资划款指令至管理人的操作人员处，并在“处理意见”栏注明退回原因。“处理意见”会通过手机短信的形式发送给管理人。
              </div>
              <div style="width:80%;margin-left:10px">
                7.追加补充附件：如场外投资所需材料不完整，我部会联系管理人划款经办人员沟通待补充材料并开放追加，管理人划款经办可通过运营管理平台【账户划款】->【跟踪待办】追加补充附件。
              </div>
              <div style="width:80%;margin-left:10px">
                8.重新提交、复核、审核指令：管理人的划款经办人员更正划款指令信息及相关附件后，在运营管理平台【账户划款】->【投资指令】->【提交投资指令】界面，重新提交划款指令，并由划款复核人员复核、审核人员审核。
              </div>
              <div style="width:80%;margin-left:10px">
                9.管理人划款操作人员（包括划款经办、复核人员及审核人员）可通过运营管理平台【账户划款】->【跟踪待办】，实时查询划款进度。如您发现有相关指令被退回，请及时查询退回原因，如有问题请随时联系我部。
              </div>
              <div style="width:80%;margin-left:10px">
                10.管理人（基金运营部估值核算岗）需要检查投资交易系统资金冻结情况，若系统没有自动调整的，需要在日终清算时调整或盘中在管理人（基金经理、交易员）允许的情况下进行调整。
              </div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">注意事项:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">1.请于划款日11：00前向我部提交完整、有效的场外投资划款指令及附件材料。</div>
              <div style="width:80%;margin-left:10px">
                2.建议管理人尽早提交投资指令与相关材料，以便我部尽快审核与处理划款事宜。为保证场外投资划款的时效性，请管理人务必最晚于场外投资划款日的11:00前提交完整、有效的划款指令及附件材料，并确保此时基金的银行托管账户内有足够的资金余额。
              </div>
              <div style="width:80%;margin-left:10px">3.由于每笔场外投资划款有其特殊性，请将上传的材料尤其扫描件必须清晰且不允许涂改。</div>
            </el-col>
          </el-row>

          <el-row style="margin-top:10px">
            <el-col :span="2"><span style="font-weight: bold">反馈时效:</span></el-col>
            <el-col :span="22">
              <div style="width:80%;margin-left:10px">指令及时、材料齐备的情况下，我部于划款日当天完成资金划拨。</div>
              <div style="width:80%;margin-left:10px">管理人可通过运营管理平台【账户划款】->【跟踪待办】实时查询划款进度。</div>
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
    <!-- <div v-if="startTransfer">
      <start-transfer transferKey='Process_invest' :isGtja="isGtja"></start-transfer>
    </div> -->
    <div v-show="startTransfer">
      <!-- <div v-show="isGtja==1">
        <start-transfer transferKey="Process_invest" isGtja="1"></start-transfer>
      </div>
      <div v-show="isGtja==0">
        <start-transfer transferKey="Process_invest" isGtja="0"></start-transfer>
      </div> -->
      <div v-show="isGtja==1&&formInline.noTransaction=='1'">
        <start-transfer transferKey="Process_invest" isGtja="1" noTransaction="1"></start-transfer>
      </div>
      <div v-show="isGtja==0&&formInline.noTransaction=='1'">
        <start-transfer transferKey="Process_invest" isGtja="0" noTransaction="1"></start-transfer>
      </div>
      <div v-show="isGtja==1&&formInline.noTransaction=='0'">
        <start-transfer transferKey="Process_invest" isGtja="1" noTransaction="0"></start-transfer>
      </div>
      <div v-show="isGtja==0&&formInline.noTransaction=='0'">
        <start-transfer transferKey="Process_invest" isGtja="0" noTransaction="0"></start-transfer>
      </div>
    </div>
    <el-form ref="formInline" status-icon label-width="120px" :model="formInline" :rules="commitRules"
             class="commitClass" auto-complete="on" label-position="left">
      <el-form-item v-if="accountTypes2.length" label="指令类型" prop="type">
        <el-radio v-model="formInline.type" v-for="item in accountTypes2" :key="item.dimValue" :label="item.dimValue">
          {{ item.dimNme }}
        </el-radio>
      </el-form-item>

      <el-form-item label="" prop="noTransaction" v-if="formInline.type=='gm050106'">
        <el-checkbox 
          v-model="formInline.noTransaction"
          true-label="1"
          false-label="0"
          @change="noTransactionChange"
        >无指令成交单</el-checkbox>
        <el-tooltip class="item" effect="light" content="" placement="right">
          <div slot="content">无需向托管传输划款指令，请区分产品分别上传银行间成交单</div>
          <i class="el-icon-warning"></i>
        </el-tooltip>
      </el-form-item>

      <el-form-item label="产品" prop="accountCode">
        <select-table v-model="formInline.accountCode" :width="'100%'" @sendDataObj="sendDataObj"></select-table>
      </el-form-item>

      <el-form-item v-if="is_gpzq_show" label="股票/债券代码" prop="stockCode">
        <el-input style="width: 100%" clearable v-model="formInline.stockCode" maxlength="66" placeholder="请输入"
                  class="el_form_item"></el-input>
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


      <!-- <el-form-item label="销售机构选择" prop="saleMechanism" v-if="saleOrgsnFlag">
          <el-select style="width: 100%" v-show="saleOrgsnFlag" filterable clearable v-model="formInline.saleMechanism" placeholder="请选择" class="el_form_item">
            <el-option
              v-for="item in saleMechanisms"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
      </el-form-item> -->

      <!-- <el-form-item label="定存银行选择" prop="bank" v-if="bankFlag">
        <el-select style="width: 100%" filterable clearable v-model="formInline.bank" placeholder="请选择" class="el_form_item">
          <el-option
            v-for="item in borkerInfos"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
    </el-form-item> -->

      <el-form-item label="转账金额(元)" prop="money">
        <el-input
          style="width: 100%"
          v-model.trim="formInline.money"
          type="text"
          class="el_form_item"
          auto-complete="off"
          maxlength="24"
          @focus="moneyFocus"
          @blur="moneyBlur"
          placeholder="请输入金额"/>
      </el-form-item>
      <!-- 收款4要素 -->
      <!-- <el-row v-if="payeeAcc_show">
        <el-col :span="24">
          <el-form-item label="收款人" prop="payeeAcconame">
            <selectAccount v-model="formInline.payeeAcconame" ref="selectAccount2" @sendDataObj="getAccountInfo2"/>
          </el-form-item>
          <el-form-item label="收款账号" prop="payeeAccount">
            <el-input placeholder="请输入收款账号" v-model="formInline.payeeAccount" maxlength="66" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="收款行" prop="payeeBank">
            <el-input placeholder="请输入收款行" v-model="formInline.payeeBank" maxlength="166" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="支付系统号" prop="paymentSystemNumber">
            <el-input placeholder="请输入支付系统号" v-model="formInline.paymentSystemNumber" maxlength="66" :disabled="true"></el-input>
          </el-form-item>
        </el-col>
      </el-row> -->
      <!-- 收付款7要素 -->
      <el-row :gutter="20" v-if="account_show">
        <el-col :span="12">
          <el-form-item label="付款人" prop="payerAcconame">
            <selectAccount
              v-model="formInline.payerAcconame" 
              ref="selectAccount1" 
              @sendDataObj="getAccountInfo1"
              :filteredValue="payerFilteredValue"
              :disabled="formInline.noTransaction=='1'?true:false"
            />
            <!-- <el-input placeholder="请输入付款人" v-model="formInline.payerAcconame" maxlength="100"></el-input> -->
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
            <selectAccount 
              v-model="formInline.payeeAcconame" 
              ref="selectAccount2" 
              @sendDataObj="getAccountInfo2"
              :filteredValue="filteredValue"
              :disabled="formInline.noTransaction=='1'?true:false"
              />
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
          name="remark"
          type="textarea"
          :autosize="{minRows: 3}"
          maxlength="1000"
          show-word-limit
          class="el_form_item"
          auto-complete="off"/>
      </el-form-item>
      <el-form-item label="附件上传" prop="file" ref="file">
        <el-upload
          class="upload-demo"
          v-model="formInline.file"
          ref="upload"
          name="file"
          :headers="hearders"
          :action="fileUploadUrl"
          :on-error="handleError"
          :on-remove="handleRemove"
          :on-success="handleSuccess"
          :on-change="handleChange"
          :file-list="fileList"
          :auto-upload="false">
          <el-button slot="trigger" size="small" type="primary">浏览</el-button>
        </el-upload>
      </el-form-item>
      <el-button v-btn="'invest.bizBegin.submit'" :disabled="submit_btn" type="primary" class="loginBtn"
                 @click="onSubmit('formInline')">
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
import StartTransfer from '../startTransfer/start-transfer.vue'
import selectTable from '@/views/commonComponents/selectTable.vue'
import bizBeginApi from '@/api/invest/investBizBegin'
import selTableApi from '@/api/transfer/bizBegin'
import { FILE_URL } from '@/utils/request'
import { getToken } from '@/utils/auth'
import { moneyThousand } from '@/filters/index'
import { moneyYuan } from '@/filters/index'
import fun from '@/filters/common'
import modelFileValidate from '@/mixinsModel/file-validate'

export default {
  mixins: [modelFileValidate],
  components: { selectTable, StartTransfer, selectAccount },
  name: 'investment',
  data() {
    //校验产品或基金代码
    const validateAccount = (rule, value, callback) => {
      if (!value) {
        callback(new Error('产品&基金代码不能为空'))
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
        callback()
      }
    }

    //校验销售机构
    const validateSaleMechanism = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请选择选项'))
      } else {
        callback()
      }
    }
    //校验定存银行
    const validateBank = (rule, value, callback) => {
      if (!value) {
        callback(new Error('定存银行不能为空'))
      } else {
        callback()
      }
    }
    //校验文件
    const validateFile = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请选择文件'))
      } else {
        callback()
      }
    }
    return {
      isGtja: 1,
      startTransfer: false,
      nowTime: '',
      // 日期禁选今天以前的
      pickerOptions: {
        // disabledDate(time) {
        //   return time.getTime() < Date.now() - 24 * 60 * 60 * 1000;
        // },
      },
      processUse_show: false,
      account_show: false,
      payeeAcc_show: false,
      formInline: {
        type: '',
        accountCode: '',//产品&基金代码
        date: '',//要求划款日期
        broker: '',//经纪商选择
        money: '',//转账金额
        instructType: '',//指令类型
        accountType: '银证转账',//转账类型
        saleMechanism: '',//销售机构选择
        bank: '',//定存银行选择
        fileList: [],
        processUse: '', //用途
        remark: '',//备注
        file: '',
        payerAcconame: '',  //付款人
        payerAccount: '',  //付款账号
        payerBank: '',  //付款行
        payeeAcconame: '',  //收款人
        payeeAccount: '',  //收款账号
        payeeBank: '',  //收款行
        paymentSystemNumber: '',  //支付系统号
        stockCode: '', //股票/债券代码
        noTransaction:"0", //无指令成交单
      },
      submitOrder: new Date().getTime(),
      activeName: '',//默认展示tab
      activeStr: '',//默认Tab strName
      activeNames: [],//默认展示coll
      saleOrgsnFlag: true,//机构选择展示
      bankFlag: false,//定存银行展示
      submit_btn: false,//提交按钮禁用
      fileList: [],//文件列表
      accountCodes: [],//产品数组
      accountCodesTemp: [],//产品数组
      borkerInfos: [], //银行数组
      saleMechanisms: [],//机构数组
      tranferTypes: [], //tab数组
      accountTypes: [],
      accountTypes2: [],
      definedId: '',
      fileUploadUrl: '', //上传文件url
      hearders: { Authorization: 'vXcx3IBemn1kShhobK2DfpY3kFqiBaSb', 'Access-Control-Allow-Origin': '*' },//上传头
      fileUploadData: { id: '', status: false },
      fileUploadStatus: true,
      // 验证规则
      // moneyValidateDefalut:/^(0|[1-9]{1}\d{0,15}|[1-9]{1}\d{0,13}\.\d{1}|[1-9]{1}\d{0,12}\.\d{2}|0\.\d{1,2})$/,
      moneyValidateDefalut: /^(0|[1-9]{1}\d{0,14}|[1-9]{1}\d{0,12}\.\d{1}|[1-9]{1}\d{0,11}\.\d{2}|0\.\d{1,2})$/,
      moneyValidate: /^(0|[1-9]{1}\d{0,14}|[1-9]{1}\d{0,12}\.\d{1}|[1-9]{1}\d{0,11}\.\d{2}|0\.\d{1,2})$/,
      commitRules: {
        // 产品&基金代码
        accountCode: [{ required: true, trigger: 'change', message: '请选择产品' }],
        // 要求划款日期
        date: [{ required: true, trigger: 'change', message: '请选择划款日期' }],
        saleMechanism: { required: true, trigger: 'change', message: '请选择销售机构' },
        bank: { required: true, trigger: 'change', message: '请选择定存银行' },
        money: [{
          required: true,
          trigger: 'change',
          pattern: /^(0|[1-9]{1}\d{0,17}|[1-9]{1}\d{0,15}\.\d{1}|[1-9]{1}\d{0,14}\.\d{2}|0\.\d{1,2})$/,
          message: '请输入数值且最多包含2位小数'
        }],
        remark: [{ required: false, trigger: 'change' }],
        file: [{ required: false, trigger: 'change', message: '请选择附件' }],
        stockCode: [
          { required: false, trigger: 'change', pattern: /^[a-zA-Z0-9]+$/, message: '请输入字母加数字的组合' },
          { required: true, trigger: 'change', message: '请输入股票/债券代码' }
        ],
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
      //校验机构
      SaleMechanismRul: { required: false, trigger: 'change', validator: validateSaleMechanism },
      //校验银行
      bankRul: { required: false, trigger: 'change', validator: validateBank },
      //校验金额
      moneyRul: { required: false, trigger: 'change' },

      initTransFlowData: {},//初始化数据
      cmdCode: '',
      is_wxxgsgSh_show: false,
      is_cktz_show: false,
      is_jjrsg_show: true,
      is_gpzq_show: false, //股票/债券代码展示
      is_zh_show: false, //划款、付款账户展示
      bigSize: false,
      uploadData: {},
      fileData: '',  // 文件上传数据（多文件合一）
      payeeApi: '',//收款
      payerApi: '',//付款
      filteredValue: [], //默认筛选
      payerFilteredValue: [], //默认筛选-付款账户
      warning_show: false,// 控制提示信息是否展示
    }
  },
  watch: {
    'formInline.type'(data) {
      console.log(data, 'watch')
      if (['gm050101', 'gm050102', 'gm050105', 'gm050106', 'gm050107'].includes(data)) {
        this.account_show = true
      } else {
        this.account_show = false
      }
      if (['gm050101', 'gm050102', 'gm050105', 'gm050107'].includes(data)) {
        // 其他账户
        this.payeeApi = 'getQtAccList'
        this.payerApi = 'getQtAccList'
        this.filteredValue = ['other']
      } else if (['gm050106'].includes(data)) {
        // 银行间债券账户
        this.payeeApi = 'getYhjAccList'
        this.payerApi = 'getYhjAccList'
        this.filteredValue = ['yhjzz', 'yhjsq']
      } else {
        this.payeeApi = ''
        this.payerApi = ''
        this.filteredValue = []
      }
      if (data == 'gm050107') {
        this.payerFilteredValue = ['other']
      } else {
        this.payerFilteredValue = ['fiduciary']
      }
    },
    "formInline.noTransaction"(data){
      if(data=='1'){
        this.formInline.payerAcconame = ''
        this.formInline.payeeAcconame = ''
        this.commitRules.payerAcconame[0].required = false;
        this.commitRules.payerAccount[0].required = false;
        this.commitRules.payerBank[0].required = false;
        this.commitRules.payeeAcconame[0].required = false;
        this.commitRules.payeeAccount[0].required = false;
        this.commitRules.payeeBank[0].required = false;
        this.$refs['formInline'].validate((valid) => {})
      }else{
        this.commitRules.payerAcconame[0].required = true;
        this.commitRules.payerAccount[0].required = true;
        this.commitRules.payerBank[0].required = true;
        this.commitRules.payeeAcconame[0].required = true;
        this.commitRules.payeeAccount[0].required = true;
        this.commitRules.payeeBank[0].required = true;
      }
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
    //获取defineId
    //this.getDefineId();
    //获取tab列表
    this.getTransferType()
    //查询销售机构
    this.getSaleMechanism()
    //查询银行
    this.getBank()
    this.handleDateChange()
    // this.getTody()
    this.commitRules.money[0].pattern = this.moneyValidate
  },
  methods: {
    /*
     函数作用：处理-要求划款日期 日期选择器的修改事件，实现托管最晚划款时间提醒
     修改人：lrb - 2021-11
   */
    handleDateChange() {
      pageApi.getTime({}).then(res => {
        console.log(this.activeStr)
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
      // console.log('now', now)
      let nowTime = new Date(now)
      let year = nowTime.getFullYear().toString()
      let month = (nowTime.getMonth() + 1).toString().padStart('2', '0')
      let date = nowTime.getDate().toString().padStart('2', '0')
      var ctimestr = year + '/' + month + '/' + date + ' ' + t
      var ctime = Date.parse(ctimestr)
      // console.log('ctime',ctime);
      if (nowTime >= ctime) {
        return true
      } else {
        return false
      }
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
    getAcc(params) {
      this.getpayeeAcc(params)
      this.getpayerAcc(params)
    },
    getpayeeAcc(params) {
      if (!this.payeeApi) return
      accountApi
        [this.payeeApi](params)
        .then(res => {
          if (res.data.status == 200) {
            let data = res.data.data.list
            let data2 = []
            if (this.payeeApi == 'getYhjAccList') {
              // 银行间账户-中债账户
              let arr1 = []
              data.forEach(item => {
                let obj = {}
                obj.accoNo = item.ccdcCapitalAccount || ''
                obj.accoName = item.ccdcCapitalName || ''
                obj.accoBank = item.ccdcCapitalBank || ''
                obj.hvpsNo = ''
                obj.accoType = this.payeeApi + 'Zz' || ''
                obj.id = item.id || ''
                arr1.push(obj)
              })
              // 银行间账户-上清所账户
              let arr2 = []
              data.forEach(item => {
                let obj = {}
                obj.accoNo = item.shchCapitalAccount || ''
                obj.accoName = item.shchCapitalName || ''
                obj.accoBank = item.shchCapitalBank || ''
                obj.hvpsNo = ''
                obj.accoType = this.payeeApi + 'Sq' || ''
                obj.id = item.id || ''
                arr1.push(obj)
              })
              data2 = [...arr1, ...arr2]
            }
            if (this.payeeApi == 'getQtAccList') {
              this.$nextTick(() => {
                if (this.$refs.selectAccount2) {
                  this.$refs.selectAccount2.init(data)
                }
              })
            } else if (this.payeeApi == 'getYhjAccList') {
              this.$nextTick(() => {
                if (this.$refs.selectAccount2) {
                  this.$refs.selectAccount2.init(data2)
                }
              })
            }

          }
        })
        .catch(() => {

        })
    },
    getpayerAcc(params) {
      if (!this.payerApi) return
      accountApi
        [this.payerApi](params)
        .then(res => {
          if (res.data.status == 200) {
            let data = res.data.data.list
            let data2 = []
            if (this.payerApi == 'getYhjAccList') {
              // 银行间账户-中债账户
              let arr1 = []
              data.forEach(item => {
                let obj = {}
                obj.accoNo = item.ccdcCapitalAccount || ''
                obj.accoName = item.ccdcCapitalName || ''
                obj.accoBank = item.ccdcCapitalBank || ''
                obj.hvpsNo = ''
                obj.accoType = this.payerApi + 'Zz' || ''
                obj.id = item.id || ''
                arr1.push(obj)
              })
              // 银行间账户-上清所账户
              let arr2 = []
              data.forEach(item => {
                let obj = {}
                obj.accoNo = item.shchCapitalAccount || ''
                obj.accoName = item.shchCapitalName || ''
                obj.accoBank = item.shchCapitalBank || ''
                obj.hvpsNo = ''
                obj.accoType = this.payerApi + 'Sq' || ''
                obj.id = item.id || ''
                arr1.push(obj)
              })
              data2 = [...arr1, ...arr2]
            }
            if (this.payerApi == 'getQtAccList') {
              this.$nextTick(() => {
                if (this.$refs.selectAccount1) {
                  this.$refs.selectAccount1.init(data)
                }
              })
            } else if (this.payerApi == 'getYhjAccList') {
              this.$nextTick(() => {
                if (this.$refs.selectAccount1) {
                  this.$refs.selectAccount1.init(data2)
                }
              })
            }

          }
        })
        .catch(() => {

        })
    },
    sendDataObj(data) {
      // console.log(data,'sendDataObj');
      if (data) {
        this.startTransfer = true
      } else {
        this.startTransfer = false
        this.processUse_show = false
        this.formInline.processUse = ''
      }
      if (data) {
        let fundCode = data.fundCode
        // 只展示规定账户类型
        // let params = {fundCode:fundCode};
        // this.getAcc(params);
        // 展示全部账户类型，默认展示规定账户类型
        let params2 = { productCode: fundCode }
        this.getAccounts(params2)
      } else {
        this.AccountEmpty()
      }
      this.formInline.payerAcconame = ''
      this.formInline.payeeAcconame = ''
      this.$message.closeAll()
      if (data == '') {
        this.submit_btn = false
        return
      }
      if (!data.operatorName) data.operatorName = ''
      let flag = data.operatorName.includes('国泰君安') || false
      if (!flag) {
        this.isGtja = 0
        this.processUse_show = true
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
      // 付款
      this.getpayerAcc2(params)
      // 收款
      this.getpayeeAcc2(params)
    },
    getpayerAcc2(params) {
      accountApi
        .getAllAccList(params)
        .then(res => {
          if (res.data.status == 200) {
            let data = res.data.data
            this.$nextTick(() => {
              this.$refs.selectAccount1.init(data)
            })
          }
        })
    },
    getpayeeAcc2(params) {
      accountApi
        .getAllAccList(params)
        .then(res => {
          if (res.data.status == 200) {
            let data = res.data.data
            this.$nextTick(() => {
              this.$refs.selectAccount2.init(data)
            })
          }
        })
    },
    // 清空账户
    AccountEmpty() {
      this.$nextTick(() => {
        if (this.$refs.selectAccount1) {
          this.$refs.selectAccount1.init([])
        }
        if (this.$refs.selectAccount2) {
          this.$refs.selectAccount2.init([])
        }
      })
    },
    getAccountInfo1(val) {
      // console.log(val);
      this.formInline.payerAccount = val.accoNo || ''
      this.formInline.payerBank = val.accoBank || ''
    },
    getAccountInfo2(val) {
      // console.log(val);
      this.formInline.payeeAccount = val.accoNo || ''
      this.formInline.payeeBank = val.accoBank || ''
      this.formInline.paymentSystemNumber = val.hvpsNo || ''
    },
    getTody(val) {
      let tody = new Date(val)
      let y = tody.getFullYear().toString()
      let m = (tody.getMonth() + 1).toString().padStart('2', '0')
      let d = tody.getDate().toString().padStart('2', '0')
      let str = y + '-' + m + '-' + d
      this.formInline.date = str
    },
    limitNumber(data) {
      if (data.length > 15) {
        this.$message.closeAll()
        this.formInline.money = data.substring(0, 15)
        this.$message.error('只能输入15位数 ！')
      }
    },
    //提交事件
    onSubmit(data) {
      console.log(this.formInline.type)
      let self = this
      /*
              if(self.fileList.length<=0){
                this.$message.closeAll();
                  this.$message.error('请选择文件');
                  return;
              }
          */
      // if(!this.bigSize){
      //   this.$message.closeAll();
      //      this.$message.error('上传文件大小不能超过 50MB!');
      //     return;
      // }
      this.$refs[data].validate((valid) => {
        if (valid) {
          self.submit_btn = true //按钮禁用
          this.submitData()

        } else {
          self.submit_btn = false //按钮启用
          return false
        }
      })
      if (self.fileList.length > 0) {
        this.$refs.file.clearValidate()
      }

    },
    //初始化列表
    getInitTransFlow() {
      bizBeginApi.getInitTransFlow().then(res => {
        if (res.data.message === 'success') {
          let data = res.data.data
          this.initTransFlowData = data
          let id = data.id
          let url = FILE_URL + '/api/file/v1.0/uploadFile?relaType=invest_file&source=GMYYPT&relaId=' + id
          this.fileUploadUrl = url
          this.hearders = { Authorization: this.$store.getters.token, 'Access-Control-Allow-Origin': '*' }
          let self = this
          setTimeout(function() {
            self.$refs.upload.submit()
          }, 300)

        } else {
          this.$message.closeAll()
          this.$message.error('初始化数据失败')
          this.submit_btn = false //按钮启用
        }
      }).catch(() => {
        this.$message.closeAll()
        this.$message.error('初始化数据失败')
        this.submit_btn = false //按钮启用
      })
    },
    submitData() {

      let self = this
      self.submit_btn = true //按钮禁用
      let params = Object.assign({}, self.formInline)
      let paramData = {}
      if (this.formInline.money && this.formInline.money.includes(',')) {
        params.money = this.formInline.money.toString().replace(/,/gi, '')
      }
      let formData = new FormData()  //  用FormData存放上传文件
      for (let i = 0; i < this.fileList.length; i++) {
        let aa = this.fileList[i].raw
        formData.append('file', aa)
      }
      //console.log(formData.get('file'));
      // formData.append('cmdCode',  this.cmdCode);
      formData.append('cmdCode', params.type)
      formData.append('fundCode', params.accountCode.split('_')[0])
      formData.append('fundName', params.accountCode.split('_')[1])
      formData.append('transferReqdate', params.date)

      if (params.saleMechanism) {
        formData.append('fundSaler', params.saleMechanism.split('|')[0])
        formData.append('fundSalerName', params.saleMechanism.split('|')[1])
      }

      if (params.bank) {
        formData.append('depositBank', params.bank.split('|')[0])
        formData.append('depositBankName', params.bank.split('|')[1])
      }

      if (this.formInline.money && this.formInline.money.includes(',')) {
        params.money = this.formInline.money.toString().replace(/,/gi, '')
      }
      formData.append('transferAmount', params.money || '')

      if (params.remark) {
        formData.append('remark', params.remark)
      }
      if (params.processUse) {
        formData.append('remark', params.processUse)
      }
      if (params.stockCode) {
        formData.append('stockCode', params.stockCode)
      }
      if (params.payeeAccount) {
        formData.append('payeeAccount', params.payeeAccount)
      }
      if (params.payerAccount) {
        formData.append('payerAccount', params.payerAccount)
      }
      formData.append('payerAcconame', params.payerAcconame)
      formData.append('payerBank', params.payerBank)
      formData.append('payeeAcconame', params.payeeAcconame)
      formData.append('payeeBank', params.payeeBank)
      formData.append('paymentSystemNumber', params.paymentSystemNumber)

      formData.append('noTransaction', params.noTransaction) //无指令成交单
      // console.log(params);return

      formData.append('submitOrder', this.submitOrder)
      bizBeginApi.startInvest(formData).then(res => {
        if (res.data.status === 200) {
          this.$message.closeAll()
          this.$message({
            type: 'success',
            message: '操作成功'
          })
          this.$emit('investCheckClick', {
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
        this.submit_btn = false //按钮启用
      }).catch(() => {
        this.$message.closeAll()
        this.$message.error('操作失败')
        this.submit_btn = false //按钮启用
      })

      // let url =  FILE_URL + '/api/transfer/v1.0/startInvest';
      // this.fileUploadUrl = url;
      // this.hearders = {Authorization: this.$store.getters.token,'Access-Control-Allow-Origin': '*'};

      // setTimeout(function(){
      //   self.$refs.upload.submit();
      // },300)

    },
    // 清除
    resetForm(formName) {
      var self = this
      self.$refs[formName].resetFields()
      self.$refs.upload.clearFiles()
      this.$nextTick(() => {
        this.getTody(this.nowTime)
      })
    },
    //tab切换
    handleClick(tab, event) {
      this.accountCodes = this.accountCodesTemp
      this.activeStr = tab.label
      this.resetForm('formInline')
      this.getAccountTypes(tab.name)
      this.formInline.accountType = tab.label
      this.activeNames = []
      this.submit_btn = false //按钮启用
      this.fileList = []
      if (tab.label === '网下新股申购(上海)' || tab.label === '网下新股申购(深圳)') {
        this.is_gpzq_show = true
      } else {
        this.is_gpzq_show = false
      }
      if (tab.label === '银行间债券交易' || tab.label === '其他' || tab.label == '银行间资金转账') {
        this.account_show = true
      } else {
        this.account_show = false
      }
      if (tab.label === '基金认申购') {
        this.saleOrgsnFlag = true
        this.bankFlag = false
        this.is_wxxgsgSh_show = false
        this.is_cktz_show = false
        this.is_jjrsg_show = true
      } else if (tab.label === '存款投资') {

        this.saleOrgsnFlag = false
        this.bankFlag = true
        this.is_wxxgsgSh_show = false
        this.is_cktz_show = true
        this.is_jjrsg_show = false
      } else {

        if (tab.label === '网下新股申购(上海)') {
          this.is_wxxgsgSh_show = true
          this.is_cktz_show = false
          this.is_jjrsg_show = false
        } else {
          this.is_wxxgsgSh_show = false
          this.is_cktz_show = false
          this.is_jjrsg_show = false
        }
        this.saleOrgsnFlag = false
        this.bankFlag = false
      }
      // this.cmdCode = tab.name;
      if (tab.label == '存款投资' || tab.label == '网下新债申购') {
        this.payeeAcc_show = true
      } else {
        this.payeeAcc_show = false
      }
      this.handleDateChange();
    },
    getAccountTypes(tabName) {
      let id = tabName.split('_')[0]
      let cmdCode = tabName.split('_')[1]
      let arr = this.accountTypes
      this.accountTypes2 = []
      for (let i = 0; i < arr.length; i++) {
        //  console.log(arr[i].parentId,id);
        if (arr[i].parentId == id) {
          this.accountTypes2.push(arr[i])
        }
      }
      //  console.log(this.accountTypes2);
      if (this.accountTypes2.length) {
        this.formInline.type = this.accountTypes2[0].dimValue
        this.cmdCode = this.accountTypes2[0].dimValue
      } else {
        this.formInline.type = cmdCode
        this.cmdCode = cmdCode
      }
    },
    //查询产品信息
    getProductInfo() {
      selTableApi.getProductFund().then(res => {
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
    //查询销售机构
    getSaleMechanism() {
      let params = 'fundSalerType'
      bizBeginApi.getSaleMechanism(params).then(res => {
        if (res.data.message === 'success') {
          let arr = res.data.data
          this.saleMechanisms = []
          for (let i = 0; i < arr.length; i++) {
            let obj = {}
            obj.value = arr[i].dimCde + '|' + arr[i].dimNme
            obj.label = arr[i].dimNme
            this.saleMechanisms.push(obj)
          }
        } else {
          this.saleMechanisms = []
          this.$message.closeAll()
          this.$message.error('查询销售机构信息失败')
        }
      }).catch(() => {
        this.$message.closeAll()
        this.$message.error('查询销售机构信息失败')
      })
    },
    //查询银行
    getBank() {
      let params = 'bankType'
      bizBeginApi.getBank(params).then(res => {
        if (res.data.message === 'success') {
          let arr = res.data.data
          this.borkerInfos = []
          for (let i = 0; i < arr.length; i++) {
            let obj = {}
            obj.value = arr[i].dimCde + '|' + arr[i].dimNme
            obj.label = arr[i].dimNme
            this.borkerInfos.push(obj)
          }
        } else {
          this.borkerInfos = []
          this.$message.closeAll()
          this.$message.error('查询银行信息失败')
        }
      }).catch(() => {
        this.$message.closeAll()
        this.$message.error('查询银行信息失败')
      })
    },
    //查询投资指令类型
    getTransferType() {
      let params = 'investCmdType'
      this.tranferTypes = []
      bizBeginApi.getTransferType(params).then(res => {
        // console.log(res)
        if (res.data.message === 'success') {
          let data = res.data.data
          //  this.tranferTypes = data;
          //  this.activeName = this.tranferTypes[0].dimValue;
          //  this.cmdCode = this.tranferTypes[0].dimValue;

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
          if (this.accountTypes2.length) {
            this.formInline.type = this.accountTypes2[0].dimValue
            this.cmdCode = this.accountTypes2[0].dimValue
          } else {
            this.formInline.type = this.tranferTypes[0].dimValue
            this.cmdCode = this.tranferTypes[0].dimValue
          }

        } else {
          this.tranferTypes = []
          this.$message.closeAll()
          this.$message.error('查询投资指令类型信息失败')
        }
      }).catch(() => {
        this.$message.closeAll()
        this.$message.error('查询投资指令类型信息失败')
      })
    },
    //获取defineId
    getDefineId() {
      bizBeginApi.getDefineId('Process_invest').then(res => {
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
    //上传文件
    submitUpload() {
      //this.fileUploadUrl =  this.fileUploadUrl + id;
      this.$refs.upload.submit()
    },
    //移除文件事件
    handleRemove(file, fileList) {
      //  this.formInline.file = fileList;
      //  this.fileList = fileList
      this.handleChange(file, fileList)
    },
    //上传文件异常事件
    handleError() {
      this.$message.closeAll()
      this.$message.error('操作失败')
      this.submit_btn = false //按钮启用
    },
    //上传文件成功事件
    handleSuccess(res, file, fileList) {
      if (res.message === 'success') {
        this.$message.closeAll()
        this.$message({
          type: 'success',
          message: '操作成功'
        })
        // this.resetForm('formInline');
        // this.fileList = [];
        this.$emit('investCheckClick', {
          data: [],
          flag: true
        })
      } else {
        this.$message.closeAll()
        this.$message.error('操作失败')
        this.fileList = []
      }
      this.submit_btn = false //按钮启用
    },
    //文件修改事件
    handleChange(file, filelist) {
      this.fileValidate(file, filelist)

      //this.formInline.file=filelist;

      //  if (filelist.length === 0) return
      //   this.fileList = []
      //  // 多个文件的累加超过50m时
      //   let totalSize = 0  //文件大小的累加
      //   let totalFlag = 0
      //   let totalFilel = []
      //   for (let item of filelist) {
      //     totalSize = item.size + totalSize
      //   }
      //   totalFlag = 0 < (totalSize / 1024 / 1024) && (totalSize / 1024 / 1024) < 50
      //   if (!totalFlag) {
      //     this.$message.closeAll()
      //     this.$message.error('总上传的文件不能为空文件不能大于50M !')
      //     for (let item of filelist) {
      //       if (file.uid !== item.uid) {
      //          totalFilel.push(item)
      //       }
      //     }
      //   } else {
      //     for (let item of filelist) {
      //        totalFilel.push(item)
      //     }
      //   }
      //   this.fileList = totalFilel

      // let self = this;
      // self.fileList = [];
      // let size = 0;
      // let arr = filelist;
      // if(filelist.length>0){
      //    for(let i=0;i<filelist.length;i++){
      //      self.fileList.push(arr[i]);
      //      size = arr[i].size + size;
      //    }
      // }
      // this.bigSize = size / 1024 / 1024 < 50

      this.$refs.file.clearValidate()

      this.formInline.file = 'file'

    },
    noTransactionChange(data){
      // if(data == '1'){
      //   this.formInline.payerAcconame = ''
      //   this.formInline.payeeAcconame = ''
      // }
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

.el-icon-circle-check:before {
  color: #67C23A;
}

.el-form--label-left .el-form-item__label {
  text-align: left;
}
</style>


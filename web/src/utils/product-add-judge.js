export function judgeData (data) {
  for (let i of data) {
    if (i == 'fundName') return { base: 1, msg: '请完善信息---产品名称', code: 'fundName' }
    else if (i == 'fundCode') return { base: 1, msg: '请完善信息---产品代码', code: 'fundCode' }
    else if (i == 'fundType') return { base: 1, msg: '请完善信息---基金类型', code: 'fundType' }
    else if (i == 'investDirect') return { base: 1, msg: '请完善信息---投资方向', code: 'investDirect' }
    else if (i == 'holdYear') return { base: 1, msg: '请完善信息---产品存续期限', code: 'holdYear' }
    else if (i == 'riskLevel') return { base: 1, msg: '请完善信息---风险等级', code: 'riskLevel' }
    else if (i == 'fundState') return { base: 1, msg: '请完善信息---产品状态', code: 'fundState' }
    else if (i == 'isGrade') return { base: 1, msg: '请完善信息---是否分级', code: 'isGrade' }
    // 非必填--1
    else if (i == 'fundNameEn') return { base: 1, msg: '请完善信息---英文名称', code: 'fundNameEn' }
    else if (i == 'operateDept') return { base: 1, msg: '请完善信息---证券营业部', code: 'operateDept' }
    else if (i == 'recordCode') return { base: 1, msg: '请完善信息---产品备案代码', code: 'recordCode' }
    else if (i == 'setupDate') return { base: 1, msg: '请完善信息---基金成立/到期日期', code: 'setupDate' }
    else if (i == 'expireDate') return { base: 1, msg: '请完善信息---基金成立/到期日期', code: 'expireDate' }
     // 非必填--3
     else if (i == 'manageAccountName') return { base: 3, msg: '请完善信息---管理人收费账户名称', code: 'manageAccountName' }
     else if (i == 'manageAccount') return { base: 3, msg: '请完善信息---管理人账号', code: 'manageAccount' }
     else if (i == 'manageBankName') return { base: 3, msg: '请完善信息---管理人开户银行名称', code: 'manageBankName' }
     else if (i == 'rewardType') return { base: 3, msg: '请完善信息---业绩报酬', code: 'rewardType' }
     else if (i == 'rewardType') return { base: 3, msg: '请完善信息---管理费率', code: 'rewardType' }
     else if (i == 'trustRate') return { base: 3, msg: '请完善信息---托管费率', code: 'trustRate' }
     else if (i == 'operateRate') return { base: 3, msg: '请完善信息---运营服务费', code: 'operateRate' }
     // 非必填--4
     else if (i == 'incomePortionDesc') return { base: 4, msg: '请完善信息---收益分配说明', code: 'incomePortionDesc' }
     // 非必填--5
     else if (i == 'investLimit') return { base: 5, msg: '请完善信息---投资限制', code: 'investLimit' }
     else if (i == 'warnPoint') return { base: 5, msg: '请完善信息---预警线', code: 'warnPoint' }
     else if (i == 'lossPoint') return { base: 5, msg: '请完善信息---止损线', code: 'lossPoint' }

    else if (i == 'subscribeConfirmDay') return { base: 2, msg: '请完善信息---认购交易确认天数', code: 'subscribeConfirmDay' }
    else if (i == 'subscribeDeliverDay') return { base: 2, msg: '请完善信息---认购资金交收天数', code: 'subscribeDeliverDay' }
    else if (i == 'applyDeliverDay') return { base: 2, msg: '请完善信息---申购资金交收天数', code: 'applyDeliverDay' }
    else if (i == 'applyConfirmDay') return { base: 2, msg: '请完善信息---申购交易确认天数', code: 'applyConfirmDay' }
    else if (i == 'callConfirmDay') return { base: 2, msg: '请完善信息---赎回交易确认天数', code: 'callConfirmDay' }
    else if (i == 'callFloatType') return { base: 2, msg: '请完善信息---赎回费率浮动类型', code: 'callFloatType' }
    else if (i == 'callDeliverDay') return { base: 2, msg: '请完善信息---赎回资金交收天数', code: 'callDeliverDay' }
    else if (i == 'callRateType') return { base: 2, msg: '请完善信息---赎回费率类型', code: 'callRateType' }
    else if (i == 'callRate') return { base: 2, msg: '请完善信息---赎回费率', code: 'callRate' }
    else if (i == 'purchasePoint') return { base: 2, msg: '请完善信息---认申购起点', code: 'purchasePoint' }
    else if (i == 'subscribeRate') return { base: 2, msg: '请完善信息---认购费率', code: 'subscribeRate' }
    else if (i == 'applyRate') return { base: 2, msg: '请完善信息---申购费率', code: 'applyRate' }
    else if (i == 'purchaseDiffAppend') return { base: 2, msg: '请完善信息---追加认申购级差', code: 'purchaseDiffAppend' }
    else return { base: 9, msg: '未知的校验信息 ！', code: '' }
   }
}
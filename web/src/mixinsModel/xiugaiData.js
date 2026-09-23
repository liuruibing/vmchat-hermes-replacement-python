export default {
  data(){
    return{
      formInlineJCXX: {
        expireDate:'',
        fundName: "",
        fundNameEn: '',
        trustorCode: '',
        operateDept: '',
        holdYear: '',
        riskLevel: '',
        recordCode: '',
        isGrade: '',
        fundCode: '',
        managerCode: '',
        operatorCode: '',
        setupDate: '',
        recordDate: '',
        operateType: '',
        fundState: '',
        investDirect: '',
        fundType:'',
        fundTypeDetails:"", //基金类型-二级
      },
      formInlineJCXX1:{
        expireDate:'',
        fundName: "",
        fundNameEn: '',
        trustorCode: '',
        operateDept: '',
        holdYear: '',
        riskLevel: '',
        recordCode: '',
        isGrade: '',
        fundCode: '',
        managerCode: '',
        operatorCode: '',
        setupDate: '',
        recordDate: '',
        operateType: '',
        fundState: '',
        investDirect: '',
        fundType:'',
        fundTypeDetails:"", //基金类型-二级
      },
      formInlineJCXX_before:{},
      formInlineJCXX_now:{},
      jcxx_i_show:false,
      formInlineJYXX: {
        purchasePoint: "",
        subscribeConfirmDay: '',
        subscribeRate: '',
        applyDeliverDay: '',
        saleFeePrepare: '',
        callConfirmDay: '',
        callFloatType: '',
        purchaseDiffAppend: '',
        subscribeDeliverDay: '',
        applyConfirmDay: '',
        applyRate: '',
        saleFeePay: '',
        callDeliverDay: '',
        blockDate: '',
        callRate: '',
        callRateType: '',
        assetFrequency: '',
      },
      formInlineJYXX1: {
        purchasePoint: "",
        subscribeConfirmDay: '',
        subscribeRate: '',
        applyDeliverDay: '',
        saleFeePrepare: '',
        callConfirmDay: '',
        callFloatType: '',
        purchaseDiffAppend: '',
        subscribeDeliverDay: '',
        applyConfirmDay: '',
        applyRate: '',
        saleFeePay: '',
        callDeliverDay: '',
        blockDate: '',
        callRate: '',
        callRateType: '',
        assetFrequency: '',
      },
      formInlineJYXX_before:{},
      formInlineJYXX_now:{},
      jyxx_i_show:false,
      formInlineFYXX: {
        manageFeePrepare: "",
        manageFeeAsset: "",
        manageFeePay: "",
        trustFeePrepare: "",
        trustFeeAsset: "",
        trustFeePay: "",
        operateFeePrepare: "",
        operateFeeAsset: "",
        operateFeePay: "",
        manageRate: '',
        operateRate: '',
        manageAccount: '',
        rewardType: '',
        trustRate: '',
        manageAccountName: '',
        manageBankName: '',
        rewardPrepareType: '',
        isFixedPrepare: '',
        rewardPrepareDate: '',
      },
      formInlineFYXX1: {
        manageFeePrepare: "",
        manageFeeAsset: "",
        manageFeePay: "",
        trustFeePrepare: "",
        trustFeeAsset: "",
        trustFeePay: "",
        operateFeePrepare: "",
        operateFeeAsset: "",
        operateFeePay: "",
        manageRate: '',
        operateRate: '',
        manageAccount: '',
        rewardType: '',
        trustRate: '',
        manageAccountName: '',
        manageBankName: '',
        rewardPrepareType: '',
        isFixedPrepare: '',
        rewardPrepareDate: '',
      },
      formInlineFYXX_before:{},
      formInlineFYXX_now:{},
      fyxx_i_show:false,
      formInlineSYFP: {
        incomePortionDesc: '',
        portionNumber: '',
        bonusProcess: '',
        dataExpect: '',
        bonusConfim: '',
        bonusDeliver: ''
      },
      formInlineSYFP1: {
        incomePortionDesc: '',
        portionNumber: '',
        bonusProcess: '',
        dataExpect: '',
        bonusConfim: '',
        bonusDeliver: ''
      },
      formInlineSYFP_before:{},
      formInlineSYFP_now:{},
      syfp_i_show:false,
      formInlineTZFK: {
        investLimit: '',
        warnPoint: '',
        lossPoint: '',
      },
      formInlineTZFK1: {
        investLimit: '',
        warnPoint: '',
        lossPoint: '',
      },
      formInlineTZFK_before:{},
      formInlineTZFK_now:{},
      tzfk_i_show:false,
      tzfk_i_show2:false,

      xsfs_i_show:false,
      fjgx_i_show:false,
      kfr_i_show:false,
      jjjl_i_show:false,
      lxr_i_show:false,
      jyxx_i_show2:false,
      fyxx_i_show2:false,
    }
  },
  mounted() {
    this.initBeforeData();
    // this.formInlineJCXX1=JSON.parse(JSON.stringify(this.formInlineJCXX))
  },
  filter:{
    
  },
  methods:{
    judgeChange (data, flag) {
      // console.log('bass-info',flag);
      for(let i in data){
        if (data[i] != flag[i]) return true
      }
    },
    judgeChangeXS(newlist){
      if(this.PageDataAdd.beforeData){
        for (let j of newlist) {
          if (j.change) {
            if (j.sallerName != j.change.sallerName) return true
            if (j.sallerCode != j.change.sallerCode) return true
            if (j.sallerType != j.change.sallerType) return true
            if (j.feeRate != j.change.feeRate) return true
            if (j.beginDate != j.change.beginDate) return true
            if (j.endDate != j.change.endDate) return true
          }
        
        }
      }else{
        return false
      }
    },
    judgeChangeFJ(newlist){
      if(this.PageDataAdd.beforeData){
        for (let j of newlist) {
          if (j.change) {
            if (j.fundCodeGrade != j.change.fundCodeGrade) return true
            if (j.fundNameGrade != j.change.fundNameGrade) return true
            if (j.assetValue != j.change.assetValue) return true
            if (j.shareType != j.change.shareType) return true
            if (j.beginDate != j.change.beginDate) return true
            if (j.endDate != j.change.endDate) return true
          }
        }
      }else{
        return false
      }
    },
    judgeChangeKFR(newlist){
      if(this.PageDataAdd.beforeData){
        for (let j of newlist) {
          if (j.change) {
            if (j.openFrequence != j.change.openFrequence) return true
            if (j.openRule != j.change.openRule) return true
            if (j.beginDate != j.change.beginDate) return true
            if (j.endDate != j.change.endDate) return true
          }
        }
      }else{
        return false
      }
    },
    judgeChangeJJJL(newlist){
      if(this.PageDataAdd.beforeData){
        for (let j of newlist) {
          if (j.change) {
            if (j.managerName != j.change.managerName) return true
            if (j.investStrategy != j.change.investStrategy) return true
            if (j.phone != j.change.phone) return true
            if (j.email != j.change.email) return true
          }
        }
      }else{
        return false
      }
    },
    judgeChangeLXR(newlist){
      if(this.PageDataAdd.beforeData){
        for (let j of newlist) {
          if (j.change) {
            if (j.contactName != j.change.contactName) return true
            if (j.contactType != j.change.contactType) return true
            if (j.contactPhone != j.change.contactPhone) return true
            if (j.contactMail != j.change.contactMail) return true
          }
        }
      }else{
        return false
      }
    },
    judgeChangeJYXX(newlist){
      if(this.PageDataAdd.beforeData){
        for (let j of newlist) {
          if (j.change) {
            if (j.redeemFrom != j.change.redeemFrom) return true
            if (j.redeemTo != j.change.redeemTo) return true
            if (j.redeemRate != j.change.redeemRate) return true
          }
        }
      }else{
        return false
      }
    },
    judgeChangeFYXX(newlist){
      if(this.PageDataAdd.beforeData){
        for (let j of newlist) {
          if (j.change) {
            if (j.rewardFrom != j.change.rewardFrom) return true
            if (j.rewardTo != j.change.rewardTo) return true
            if (j.rewardRate != j.change.rewardRate) return true
          }
        }
      }else{
        return false
      }
    },
    isCheackChange (after1, befor1, textareaList) {
      // console.log('textareaList',textareaList)
      let after = after1 || []
      let befor = befor1 || []
      let warning = false
      let temp = new Array
      let temp2 = new Array
      let temp3 = new Array
      let temp4 = new Array
      for (let i of after) {
        for (let j of befor) {
          if (i.investScope == j.investScope) temp.push({ id: i.investScope, change: true})  //得到相同的
        }
      }
      for (let j of after) temp2.push(j.investScope)
      for (let j of befor) temp2.push(j.investScope)
      temp2 = Array.from(new Set(temp2))  //去掉重复的
      for (let i of temp2) {
        this.tg = false
        for (let j of temp) {
          if (j.id == i && j.change) this.tg = true
        }
        if (!this.tg) {
          warning = true
          temp3.push({ id: i, change: true , des: '是'})
        }
        else temp3.push({ id: i, change: false, des: '否'})
      }
      textareaList.forEach( i => {
        let kg = false
        temp3.forEach( j => {
          if (i.dimCde == j.id && j.change) {  kg = true }
        })
        if (!kg) temp4.push({id: i.dimCde, change: true, des: '否', dimNme: i.dimNme})
        else temp4.push({id: i.dimCde, change: false, des: '是', dimNme: i.dimNme})
      });
      // console.log(temp3)
      // console.log(temp3)
      // console.log(temp3)
      this.fundInvestArea = temp4
      // console.log('lllllllllll',this.fundInvestArea);
      return warning
    },
    initBeforeData(){
      // let data=this.PageDataAdd.beforeData;
      if(this.PageDataAdd.beforeData){
        if(!this.PageDataAdd.beforeData.fundInfo.assetFrequency){
          this.PageDataAdd.beforeData.fundInfo.assetFrequency=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.expireDate){
          this.PageDataAdd.beforeData.fundInfo.expireDate=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.fundName){
          this.PageDataAdd.beforeData.fundInfo.fundName=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.fundCode){
          this.PageDataAdd.beforeData.fundInfo.fundCode=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.fundNameEn){
          this.PageDataAdd.beforeData.fundInfo.fundNameEn=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.managerCode){
          this.PageDataAdd.beforeData.fundInfo.managerCode=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.trustorCode){
          this.PageDataAdd.beforeData.fundInfo.trustorCode=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.operatorCode){
          this.PageDataAdd.beforeData.fundInfo.operatorCode=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.fundType){
          this.PageDataAdd.beforeData.fundInfo.fundType=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.riskLevel){
          this.PageDataAdd.beforeData.fundInfo.riskLevel=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.investDirect){
          this.PageDataAdd.beforeData.fundInfo.investDirect=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.operateDept){
          this.PageDataAdd.beforeData.fundInfo.operateDept=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.setupDate){
          this.PageDataAdd.beforeData.fundInfo.setupDate=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.holdYear){
          this.PageDataAdd.beforeData.fundInfo.holdYear=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.recordDate){
          this.PageDataAdd.beforeData.fundInfo.recordDate=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.operateType){
          this.PageDataAdd.beforeData.fundInfo.operateType=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.recordCode){
          this.PageDataAdd.beforeData.fundInfo.recordCode=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.fundState){
          this.PageDataAdd.beforeData.fundInfo.fundState=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.isGrade){
          this.PageDataAdd.beforeData.fundInfo.isGrade=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.saleType){
          this.PageDataAdd.beforeData.fundInfo.saleType=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.isOpenShort){
          this.PageDataAdd.beforeData.fundInfo.isOpenShort=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.blockDate){
          this.PageDataAdd.beforeData.fundInfo.blockDate=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.purchasePoint){
          this.PageDataAdd.beforeData.fundInfo.purchasePoint=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.purchaseDiffAppend){
          this.PageDataAdd.beforeData.fundInfo.purchaseDiffAppend=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.subscribeConfirmDay){
          this.PageDataAdd.beforeData.fundInfo.subscribeConfirmDay=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.subscribeDeliverDay){
          this.PageDataAdd.beforeData.fundInfo.subscribeDeliverDay=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.subscribeRate){
          this.PageDataAdd.beforeData.fundInfo.subscribeRate=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.applyConfirmDay){
          this.PageDataAdd.beforeData.fundInfo.applyConfirmDay=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.applyDeliverDay){
          this.PageDataAdd.beforeData.fundInfo.applyDeliverDay=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.applyRate){
          this.PageDataAdd.beforeData.fundInfo.applyRate=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.saleFeePrepare){
          this.PageDataAdd.beforeData.fundInfo.saleFeePrepare=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.saleFeePay){
          this.PageDataAdd.beforeData.fundInfo.saleFeePay=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.callConfirmDay){
          this.PageDataAdd.beforeData.fundInfo.callConfirmDay=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.callFloatType){
          this.PageDataAdd.beforeData.fundInfo.callFloatType=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.callRate){
          this.PageDataAdd.beforeData.fundInfo.callRate=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.callRateType){
          this.PageDataAdd.beforeData.fundInfo.callRateType=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.callDeliverDay){
          this.PageDataAdd.beforeData.fundInfo.callDeliverDay=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.manageFeePrepare){
          this.PageDataAdd.beforeData.fundInfo.manageFeePrepare=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.manageFeeAsset){
          this.PageDataAdd.beforeData.fundInfo.manageFeeAsset=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.manageFeePay){
          this.PageDataAdd.beforeData.fundInfo.manageFeePay=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.trustFeePrepare){
          this.PageDataAdd.beforeData.fundInfo.trustFeePrepare=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.trustFeeAsset){
          this.PageDataAdd.beforeData.fundInfo.trustFeeAsset=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.trustFeePay){
          this.PageDataAdd.beforeData.fundInfo.trustFeePay=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.operateFeePrepare){
          this.PageDataAdd.beforeData.fundInfo.operateFeePrepare=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.operateFeeAsset){
          this.PageDataAdd.beforeData.fundInfo.operateFeeAsset=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.operateFeePay){
          this.PageDataAdd.beforeData.fundInfo.operateFeePay=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.manageRate){
          this.PageDataAdd.beforeData.fundInfo.manageRate=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.trustRate){
          this.PageDataAdd.beforeData.fundInfo.trustRate=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.operateRate){
          this.PageDataAdd.beforeData.fundInfo.operateRate=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.manageAccountName){
          this.PageDataAdd.beforeData.fundInfo.manageAccountName=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.manageAccount){
          this.PageDataAdd.beforeData.fundInfo.manageAccount=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.manageBankName){
          this.PageDataAdd.beforeData.fundInfo.manageBankName=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.rewardType){
          this.PageDataAdd.beforeData.fundInfo.rewardType=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.rewardPrepareType){
          this.PageDataAdd.beforeData.fundInfo.rewardPrepareType=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.isFixedPrepare){
          this.PageDataAdd.beforeData.fundInfo.isFixedPrepare=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.rewardPrepareDate){
          this.PageDataAdd.beforeData.fundInfo.rewardPrepareDate=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.incomePortionDesc){
          this.PageDataAdd.beforeData.fundInfo.incomePortionDesc=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.portionNumber){
          this.PageDataAdd.beforeData.fundInfo.portionNumber=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.bonusProcess){
          this.PageDataAdd.beforeData.fundInfo.bonusProcess=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.dataExpect){
          this.PageDataAdd.beforeData.fundInfo.dataExpect=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.bonusConfim){
          this.PageDataAdd.beforeData.fundInfo.bonusConfim=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.bonusDeliver){
          this.PageDataAdd.beforeData.fundInfo.bonusDeliver=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.fiduciaryName){
          this.PageDataAdd.beforeData.fundInfo.fiduciaryName=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.fiduciaryAccount){
          this.PageDataAdd.beforeData.fundInfo.fiduciaryAccount=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.fiduciaryBank){
          this.PageDataAdd.beforeData.fundInfo.fiduciaryBank=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.fiduciaryYield){
          this.PageDataAdd.beforeData.fundInfo.fiduciaryYield=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.raiseName){
          this.PageDataAdd.beforeData.fundInfo.raiseName=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.raiseAccount){
          this.PageDataAdd.beforeData.fundInfo.raiseAccount=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.raiseBank){
          this.PageDataAdd.beforeData.fundInfo.raiseBank=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.raiseAccountBig){
          this.PageDataAdd.beforeData.fundInfo.raiseAccountBig=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.securityName){
          this.PageDataAdd.beforeData.fundInfo.securityName=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.securityAccount){
          this.PageDataAdd.beforeData.fundInfo.securityAccount=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.stockAccountSh){
          this.PageDataAdd.beforeData.fundInfo.stockAccountSh=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.optionAccountSh){
          this.PageDataAdd.beforeData.fundInfo.optionAccountSh=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.stockAccountSz){
          this.PageDataAdd.beforeData.fundInfo.stockAccountSz=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.optionAccountSz){
          this.PageDataAdd.beforeData.fundInfo.optionAccountSz=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.securityCapitalAccount){
          this.PageDataAdd.beforeData.fundInfo.securityCapitalAccount=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.futuresAccount){
          this.PageDataAdd.beforeData.fundInfo.futuresAccount=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.optionAccount){
          this.PageDataAdd.beforeData.fundInfo.optionAccount=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.investLimit){
          this.PageDataAdd.beforeData.fundInfo.investLimit=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.warnPoint){
          this.PageDataAdd.beforeData.fundInfo.warnPoint=''
        }
        if(!this.PageDataAdd.beforeData.fundInfo.lossPoint){
          this.PageDataAdd.beforeData.fundInfo.lossPoint=''
        }
      }
    }
  }
}
export default {
  data() {
    return {
      relationShow: false,
      relationShipData: {},
      activeName: "first",
      preName: "修改前：",
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

      jcxx_show: true, //基础信息展示
      jyxx_show: false, //交易信息展示
      fyxx_show: false, //费用信息展示
      syfp_show: false, //收益分配展示
      zhxx_show: false, //账户信息展示
      tzfk_show: false, //投资风控展示
      lxr_show: false, //联系人展示
      xsfs_show: false, //销售方式展示
      kfr_show: false, //开放日展示
      tableData: [], //联系人列表
      shtg_show: false,
      shbtg_show: true,
      sh_show: false,
      tableDataContact: [], //联系人列表
      tableDataRedeem: [],
      tableDataGrade: [], //赎回费率列表数据
      tableDataReward: [], //计提列表数据
      tableDataSaller: [], //销售方式列表数据
      tableDataOpen: [], //开放日列表数据
      beforeData: "", //修改前的数据数组
      fundInvestArea: [], //投资范围
      beforeFundInvests: "", //投资范围修改前
      afterfundInvests: [],
      fundInvests: "", //投资范围
      sallerNameArr: [], //渠道名称数组
      openFrequenceArr: [], //开放频率数组
      openRuleArr: [], //开放规则数组
      fundManager_show: false,
      tableDataFundManager: [],
      jcxxI_show: false,
      jyxxI_show: false,
      fyxxI_show: false,
      syxxI_show: false,
      tzxxI_show: false,
      formHandle: {
        approveOpinion: "", //处理意见
      },
      approveOpinion: "", //审核意见
      modifier: "", //修改人
      countSubmit_btn: false,

      // 表单校验规则
      commonRules: {
        //必填信息校验
        fundName: [
          {
            required: true,
            pattern: /^[a-zA-Za-z0-9\u4e00-\u9fa5]+$/,
            message: "请输入中文、字母、数字",
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

        fundType: [
          { required: true, message: "请选择基金类型", trigger: "change" },
        ],
        investDirect: [
          { required: true, message: "请选择投资方向", trigger: "change" },
        ],
        holdYear: [
          {
            required: true,
            trigger: "change",
            pattern: /^([1-9]\d?|100)$/,
            message: "请输入1-100的整数",
          },
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
            trigger: "change",
          },
        ],
        purchaseDiffAppend: [
          {
            required: true,
            message: "请输入追加认申购级差",
            trigger: "change",
          },
        ],
        subscribeRate: [
          { required: true, message: "请输入认购费率", trigger: "change" },
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
            pattern: /^[a-zA-Za-z0-9\u4e00-\u9fa5]+$/,
            message: "请输入中文、字母、数字",
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
            pattern: /^[a-zA-Za-z0-9\u4e00-\u9fa5]+$/,
            message: "请输入中文、字母、数字",
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
            pattern: /^[a-zA-Za-z0-9\u4e00-\u9fa5]+$/,
            message: "请输入中文、字母、数字",
          },
        ],

        //收益分配
        incomePortionDesc: [
          {
            required: false,
            trigger: "change",
            pattern: /^[a-zA-Za-z0-9\u4e00-\u9fa5]+$/,
            message: "请输入中文、字母、数字",
          },
        ],
        //投资风控
        investLimit: [
          {
            required: false,
            trigger: "change",
            pattern: /^[a-zA-Za-z0-9\u4e00-\u9fa5]+$/,
            message: "请输入中文、字母、数字",
          },
        ],
        warnPoint: [
          {
            required: false,
            trigger: "change",
            pattern: /^((0){1}(\.\d{0,2})?|1)$/,
            message: "请输入0-1两位小数",
          },
        ],
        lossPoint: [
          {
            required: false,
            trigger: "change",
            pattern: /^((0){1}(\.\d{0,2})?|1)$/,
            message: "请输入0-1两位小数",
          },
        ],
      },
    };
  },
  mounted() {},
}
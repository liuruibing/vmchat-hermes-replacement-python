
//产品数据字典
export default {
  //运作方式
  operateType:[
    {dimNme:'封闭式',dimCde:'1'},
    {dimNme:'开放式',dimCde:'2'}
  ],
  //是否分级
  isGrade:[
    {dimNme:'是',dimCde:1},
    {dimNme:'否',dimCde:0}
  ],
  //产品状态
  fundState:[
    {dimNme:'筹备期',dimCde:'0'},
    {dimNme:'募集期',dimCde:'1'},
    {dimNme:'运作期',dimCde:'2'},
    {dimNme:'清盘',dimCde:'3'}
  ],
  //是否可以设置临开
  isOpenShort:[
    {dimNme:'是',dimCde:1},
    {dimNme:'否',dimCde:0}
  ],
  //销售服务费计提
  saleFeePrepare:[
    {dimNme:'按日计提',dimCde:'d'},
    {dimNme:'按月计提',dimCde:'m'}
  ],
  //销售服务费支付
  saleFeePay:[
    {dimNme:'按月支付',dimCde:'m'},
    {dimNme:'按季支付',dimCde:'q'},
    {dimNme:'按年支付',dimCde:'y'}
  ],
  //份额类型
  shareType:[
    {dimNme:'',dimCde:''},
    {dimNme:'A',dimCde:'A'},
    {dimNme:'B',dimCde:'B'},
    {dimNme:'C',dimCde:'C'},
    {dimNme:'H',dimCde:'H'},
    // {dimNme:'E',dimCde:'E'},
    // {dimNme:'F',dimCde:'F'},
    // {dimNme:'G',dimCde:'G'},
    // {dimNme:'H',dimCde:'H'},
    // {dimNme:'I',dimCde:'I'},
    // {dimNme:'J',dimCde:'J'},
    // {dimNme:'K',dimCde:'K'},
    // {dimNme:'L',dimCde:'L'},
    // {dimNme:'M',dimCde:'M'},
    // {dimNme:'N',dimCde:'N'},
    // {dimNme:'O',dimCde:'O'},
    // {dimNme:'P',dimCde:'P'},
    // {dimNme:'Q',dimCde:'Q'},
    // {dimNme:'R',dimCde:'R'},
    // {dimNme:'S',dimCde:'S'},
    // {dimNme:'T',dimCde:'T'},
    // {dimNme:'U',dimCde:'U'},
    // {dimNme:'V',dimCde:'V'},
    // {dimNme:'W',dimCde:'W'},
    // {dimNme:'X',dimCde:'X'},
    // {dimNme:'Y',dimCde:'Y'},
    // {dimNme:'Z',dimCde:'Z'}
   
  ],
  callFloatType:[
    {dimNme:'固定',dimCde:'0'},
    {dimNme:'浮动',dimCde:'1'}
  ], 
  //计提方式是否
  isFixedPrepare:[
    {dimNme:'是',dimCde:1},
    {dimNme:'否',dimCde:0}
  ],
  //提交截止日-次，当
  submitDc:[
    {dimNme:'当',dimCde:'0'},
    {dimNme:'次',dimCde:'v'}
  ],
  //提交截止日-年，月
  submitYm:[
	{dimNme:'日',dimCde:'D'},
	{dimNme:'周',dimCde:'W'},
	{dimNme:'月',dimCde:'M'},
    {dimNme:'年',dimCde:'Y'}
  ],
  //提交截止日-年
  submitMdY:[
    {dimNme:'一月底',dimCde:'1',disable:false},
    {dimNme:'二月底',dimCde:'2',disable:false},
    {dimNme:'三月底',dimCde:'3',disable:false},
    {dimNme:'四月底',dimCde:'4',disable:false},
    {dimNme:'五月底',dimCde:'5',disable:false},
    {dimNme:'六月底',dimCde:'6',disable:false},
    {dimNme:'八月底',dimCde:'8',disable:false},
    // {dimNme:'三个工作日',dimCde:'3d',disable:true},
    // {dimNme:'五个工作日',dimCde:'5d',disable:true},
    // {dimNme:'十个工作日',dimCde:'10d',disable:true},
    // {dimNme:'十五个工作日',dimCde:'15d',disable:true},
    // {dimNme:'月底',dimCde:'99d',disable:true}
  ],
  //提交截止日-月
  submitMdM:[
    {dimNme:'三个工作日',dimCde:'3d',disable:false},
    {dimNme:'五个工作日',dimCde:'5d',disable:false},
    {dimNme:'十个工作日',dimCde:'10d',disable:false},
    {dimNme:'十五个工作日',dimCde:'15d',disable:false},
    {dimNme:'月底',dimCde:'99d',disable:false},
    // {dimNme:'一月底',dimCde:'1',disable:true},
    // {dimNme:'二月底',dimCde:'2',disable:true},
    // {dimNme:'三月底',dimCde:'3',disable:true},
    // {dimNme:'四月底',dimCde:'4',disable:true},
    // {dimNme:'五月底',dimCde:'5',disable:true},
    // {dimNme:'六月底',dimCde:'6',disable:true}
  ],
  //提交截止日-周
  submitMdW:[
    {dimNme:'一个工作日',dimCde:'1d',disable:false},
    {dimNme:'二个工作日',dimCde:'2d',disable:false},
    {dimNme:'三个工作日',dimCde:'3d',disable:false},
  ],
  submitMdMAll:[
    {dimNme:'一月底',dimCde:'1'},
    {dimNme:'二月底',dimCde:'2'},
    {dimNme:'三月底',dimCde:'3'},
    {dimNme:'四月底',dimCde:'4'},
    {dimNme:'五月底',dimCde:'5'},
    {dimNme:'六月底',dimCde:'6'},
    {dimNme:'八月底',dimCde:'8'},
    {dimNme:'一个工作日',dimCde:'1d'},
    {dimNme:'二个工作日',dimCde:'2d'},
    {dimNme:'三个工作日',dimCde:'3d'},
    {dimNme:'五个工作日',dimCde:'5d'},
    {dimNme:'十个工作日',dimCde:'10d'},
    {dimNme:'十五个工作日',dimCde:'15d'},
    {dimNme:'月底',dimCde:'99d'}
  ]


}
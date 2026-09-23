export default {
  //初始化数据字典
  initHandle() {
    let obj = new Object
    let cmdStatusArr = new Object
    let procStatusArr = new Object
    let cmdCodeArr = new Object
    let transferStatuses = new Array
    let arr = [
      { name: '指令经办(国泰君安)', code: 'cmdOpt' },
      { name: '指令复核(国泰君安)', code: 'cmdCheck' },
      { name: '管理人复核', code: 'managerCheck' },
      { name: '管理人审批', code: 'managerApprove' },
      { name: '托管划款中', code: 'transOperating' },
      { name: '划款成功', code: 'transSuccess' },
      { name: '划款失败', code: 'transFailed' },
      { name: '指令撤销', code: 'cmdCancel' },
      { name: '指令作废', code: 'cmdInvalid' },
      { name: '指令暂缓', code: 'cmdSuspend' }
    ];
    //初始化划款状态
    let arr2 = [
      { name: '划款审批中', code: 'transApproving' },
      { name: '托管划款中', code: 'transOperating' },
      { name: '指令暂缓', code: 'cmdSuspend' }
    ];
    let arr4 = [
      { name: '划款审批中', code: 'transApproving' },
      { name: '托管划款中', code: 'transOperating' },
      { name: '划款失败', code: 'transFailed' },
      { name: '划款成功', code: 'transSuccess' },
      { name: '指令撤销', code: 'cmdCancel' },
      { name: '指令作废', code: 'cmdInvalid' },
      { name: '指令暂缓', code: 'cmdSuspend' }
    ];
    //初始化划款类型
    let arr3 = [
      { name: '银转证', code: '040101' },
      { name: '证转银', code: '040102' },
      { name: '银转期', code: '040201' },
      { name: '期转银', code: '040202' },
      { name: '银转期(手工入金)', code: '040203' },
      { name: '银转信', code: '040301' },
      { name: '信转银', code: '040302' },
      { name: '银转衍', code: '040401' },
      { name: '衍转银', code: '040402' },
      { name: '银转衍(手工入金)', code: '040403' },
      { name: '银转贵', code: '040501' },
      { name: '贵转银', code: '040502' },
      { name: '银转贵(手工入金)', code: '040503' },
      { name: '基金认申购', code: '050101' },
      { name: '存款投资', code: '050102' },
      { name: '网下新股申购(上海)', code: '050103' },
      { name: '网下新股申购(深圳)', code: '050104' },
      { name: '网下新债申购', code: '050105' },
      { name: '银行间债券交易', code: '050106' },
      { name: '其他', code: '050107' }
    ];

    //初始化划款状态
    transferStatuses = arr2;
    //绑定数据字典
    for (let i = 0; i < arr.length; i++) {
      cmdStatusArr[arr[i].code] = arr[i].name;
    }
    for (let i = 0; i < arr4.length; i++) {
      procStatusArr[arr4[i].code] = arr4[i].name;
    }

    for (let i = 0; i < arr3.length; i++) {
      cmdCodeArr[arr3[i].code] = arr3[i].name;
    }
    obj = {
      'transferStatuses': transferStatuses,
      'cmdStatusArr': cmdStatusArr,
      'procStatusArr': procStatusArr,
      'cmdCodeArr': cmdCodeArr
    }
    return obj
  },
}
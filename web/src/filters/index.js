import {Message} from 'element-ui'
import Layout from '@/views/layout/Layout'
// set function parseTime,formatTime to filter
export {parseTime, formatTime} from '@/utils'

function pluralize(time, label) {
  if (time === 1) {
    return time + label
  }
  return time + label + 's'
}

// 除法
function accDiv(arg1, arg2) {
  var t1 = 0, t2 = 0, r1, r2;
  try {
    t1 = arg1.toString().split(".")[1].length
  } catch (e) {
  }
  try {
    t2 = arg2.toString().split(".")[1].length
  } catch (e) {
  }
  r1 = Number(arg1.toString().replace(".", ""))
  r2 = Number(arg2.toString().replace(".", ""))
  return (r1 / r2) * Math.pow(10, t2 - t1);
}

// 乘法
function accMul(arg1, arg2) {
  var m = 0, s1 = Number(arg1).toString(), s2 = Number(arg2).toString();
  try {
    m += s1.split(".")[1].length;
  } catch (e) {
  }
  try {
    m += s2.split(".")[1].length;
  } catch (e) {
  }
  return Number(s1.replace(".", "")) * Number(s2.replace(".", "")) / Math.pow(10, m);
}


export function timeAgo(time) {
  const between = Date.now() / 1000 - Number(time)
  if (between < 3600) {
    return pluralize(~~(between / 60), ' minute')
  } else if (between < 86400) {
    return pluralize(~~(between / 3600), ' hour')
  } else {
    return pluralize(~~(between / 86400), ' day')
  }
}

/* 数字 格式化*/
export function numberFormatter(num, digits) {
  const si = [
    {value: 1E18, symbol: 'E'},
    {value: 1E15, symbol: 'P'},
    {value: 1E12, symbol: 'T'},
    {value: 1E9, symbol: 'G'},
    {value: 1E6, symbol: 'M'},
    {value: 1E3, symbol: 'k'}
  ]
  for (let i = 0; i < si.length; i++) {
    if (num >= si[i].value) {
      return (num / si[i].value + 0.1).toFixed(digits).replace(/\.0+$|(\.[0-9]*[1-9])0+$/, '$1') + si[i].symbol
    }
  }
  return num.toString()
}

export function toThousandFilter(num) {
  return (+num || 0).toString().replace(/^-?\d+/g, m => m.replace(/(?=(?!\b)(\d{3})+$)/g, ','))
}

export function createTreeData(nodes, treeRootId) {
  for (let i = 0; i < nodes.length; i++) {
    if (nodes[i].pId == treeRootId) {
      break;
    } else if (i == nodes.length - 1) {
      Message.closeAll()
      Message({
        message: '数据格式错误',
        type: 'error',
        duration: 2 * 1000
      })
    } else {
    }
  }
  // let nodes01 = [
  //    {
  //      "actionid": "1",
  //      "actionpid": "0",
  //      "id": "1",
  //      "name": "管理视图",
  //      "pId": "0",
  //      "vcactioncode": "MENU.PORTAL",
  //      "vcactionname": "管理视图",
  //      "vcactiontype": "PAGE.PERMISSION.TYPE.MU",
  //      "vcgroup": "本系统",
  //      "vcicon": "dashboard",
  //      "vcmodel": "内部链接",
  //      "vcpid": "1",
  //      "vcremark": "views/managementView/management",
  //      "vcstatus": "启用",
  //      "vcteam": "0",
  //      "vcurl": "/managementView"
  //    },
  //    {
  //      "actionid": "101",
  //      "actionpid": "1",
  //      "id": "101",
  //      "name": "管理视图",
  //      "pId": "1",
  //      "vcactioncode": "MENU.PORTAL",
  //      "vcactionname": "管理视图",
  //      "vcactiontype": "PAGE.PERMISSION.TYPE.MU",
  //      "vcgroup": "本系统",
  //      "vcicon": "fa fa-home",
  //      "vcmodel": "内部链接",
  //      "vcpid": "101",
  //      "vcremark": "views/managementView/management",
  //      "vcstatus": "启用",
  //      "vcteam": "0",
  //      "vcurl": "management"
  //    },
  //    {
  //      "actionid": "102",
  //      "actionpid": "1",
  //      "id": "102",
  //      "name": "投资经理视图",
  //      "pId": "1",
  //      "vcactioncode": "MENU.PORTAL",
  //      "vcactionname": "投资经理视图",
  //      "vcactiontype": "PAGE.PERMISSION.TYPE.MU",
  //      "vcgroup": "本系统",
  //      "vcicon": "fa fa-home",
  //      "vcmodel": "内部链接",
  //      "vcpid": "101",
  //      "vcremark": "views/managementView/investmentManager",
  //      "vcstatus": "启用",
  //      "vcteam": "0",
  //      "vcurl": "investmentManager"
  //    },
  //  ]

  let nodesFilters = nodes;

  // 测试单页面
  // nodesFilters.splice(1, 1);
  // nodesFilters[0].vcurl = "/dashboard";
  // nodesFilters[0].vcremark = "views/home/index";
  // nodesFilters.push({
  //   "actionid": "101232",
  //   "actionpid": "0",
  //   "id": "101232",
  //   "name": "投资经理视图",
  //   "pId": "0",
  //   "vcactioncode": "MENU.PORTAL",
  //   "vcactionname": "投资经理视图",
  //   "vcactiontype": "PAGE.PERMISSION.TYPE.MU",
  //   "vcgroup": "本系统",
  //   "vcicon": "dashboard",
  //   "vcmodel": "内部链接",
  //   "vcpid": "101",
  //   "vcremark": "views/home/index",
  //   "vcstatus": "启用",
  //   "vcteam": "0",
  //   "vcurl": "/investmentManager"
  // })
  // console.log(nodesFilters);

  let groups = {};
  // 按父节点将节点分组
  for (let i in nodesFilters) {
    //只遍历是菜单类型的 并且是菜单类型是启用的
    if (nodesFilters[i].vcactiontype == "PAGE.PERMISSION.TYPE.MU" && nodesFilters[i].vcstatus == "启用") {
      if (!groups[nodesFilters[i].pId]) {
        groups[nodesFilters[i].pId] = [];
      }
      groups[nodesFilters[i].pId].push(nodesFilters[i]);
      if (treeRootId && treeRootId === nodesFilters[i].id) { // 发现传入的根节点id作为节点id时，将根节点设置为该节点的父节点
        treeRootId = nodesFilters[i].pId;
      }
    } else {
    }

  }

  let rootNodes = groups[treeRootId];
  groups[treeRootId] = null; // [SAFEGUARD]防止自为父节点或互为父节点（有环图结构）导致的死循环
  function traverseTreeNodeGroup(treeNodeGroup) {
    for (var i in treeNodeGroup) {
      var node = treeNodeGroup[i];
      if (node.vcactionname === undefined) {
        node.vcactionname = ''
      } else {
      }
      if (node.vcurl === undefined) {
        node.vcurl = ''
      } else {
      }
      if (node.vcicon === undefined) {
        node.vcicon = ''
      } else {
      }
      if (node.vcremark === undefined) {
        node.vcremark = ''
      } else {
      }

      // component:resolve=>(require([`@/${formUrl}.vue`],resolve)),

      // 顶部路由 / / 名字
      node.name = node.name + node.id // 防止name相同报错
      // 先判断是内部链接还是外部链接
      if (node.vcmodel === "外部链接") {
        if (node.vcurl) {
          node.path = node.vcurl.split('?')[0];
        }
      }
      // 路由地址  带？的单独处理 嵌套jsp页面
      else if (node.vcurl && node.vcurl.indexOf('?') != -1) {
        node.path = node.vcurl.split('?').join(':');
      } else {
        node.path = node.vcurl;
      }
      // 去除将子路由作为根路由显示在侧边栏
      node.alwaysShow = true;

      // 描述
      node.meta = {title: node.vcactionname, icon: node.vcicon, vcactionstr: node.vcactioncode};
      //表单路径
      let componentPath = node.vcremark;
      // console.log(componentPath);
      node.component = resolve => (require([`@/${componentPath}.vue`], resolve));

      if (groups[node.id]) {
        node.children = groups[node.id];
        groups[node.id] = null; // [SAFEGUARD]防止自为父节点或互为父节点（有环图结构）导致的死循环
        traverseTreeNodeGroup(node.children);
      }
    }
  }

  traverseTreeNodeGroup(rootNodes);
  // 超过8个路由显示更多 超出路由值记录
  let moreMeau = [];
  for (let i in rootNodes) {
    // 如果不存在children属性 则是单个菜单 需要手动构建children
    if (!rootNodes[i].children) {
      //防止对象间赋值互相覆盖
      let obj = JSON.stringify(rootNodes[i]);
      rootNodes[i].children = [];
      rootNodes[i].children.push(JSON.parse(obj));
      rootNodes[i].children[0].path = '';
      rootNodes[i].children[0].component = resolve => (require([`@/${rootNodes[i].children[0].vcremark}.vue`], resolve));
      rootNodes[i].children[0].meta.icon = '';
      rootNodes[i].Nochildren = true;
      // 去除将子路由作为根路由显示在侧边栏
      rootNodes[i].alwaysShow = false;
    }
    //父菜单页面根节点指向 Layout
    rootNodes[i].component = Layout;
    //删除存在子级的父级的name  key值
    if (rootNodes[i].children && rootNodes[i].children.length) delete rootNodes[i].name
    // 记录菜单数量超过8个的路由
    // if(i > 6){
    //   moreMeau.push(rootNodes[i]);
    // }
  }
  // 如果moreMeau 存在值
  // if(moreMeau.length > 0){
  //   // 说明路由数量大于8,则截取8个路由
  //   rootNodes = rootNodes.slice(0,7);
  //   // 添加更多按钮
  //   let moreMeauObj = {
  //      id:"202020",
  //      children:[],
  //      pId: "0",
  //      component:Layout,
  //      meta:{title:"更多",icon:"more"},
  //      path:"/",
  //      Nochildren:false,
  //   }
  //   for(let i = 0; i < moreMeau.length; i++){
  //     // pid置为上边更多的id
  //     moreMeau[i].pId = moreMeauObj.id;
  //     // 删除路径里边的 / ,因为上边更多已经配置过
  //     moreMeau[i].path = moreMeau[i].path.substr(1);
  //     // 本身作为一级菜单，置为二级后要改变页面地址为routerPage;
  //     moreMeau[i].component = resolve => (require([`@/views/routerPage/index.vue`], resolve))
  //     // 删除对应的icon属性
  //     delete moreMeau[i].meta.icon;
  //     // 添加name属性 菜单key 值需要
  //     moreMeau[i].name = moreMeau[i].meta.title +  moreMeau[i].id;
  //   }
  //   moreMeauObj.children = moreMeau;

  //   // 添加到菜单列表中
  //   rootNodes.push(moreMeauObj);
  // }


  return rootNodes;
}

// 数据为空显示 -
export function noDataFilter(n) {
  if (n === undefined || n === '' || n === null) {
    return '-';
  } else {
    return n;
  }
}
/* 比例乘以100，保留2位小数  */
export function baifenlvS (n) {
  if (!n && n !== 0) return '-'
  if (n == 0) return '-'
  // 如果前面有加减符号
  let head = ''
  if (typeof n === 'number') n = String(n)
  head = n.substring(0, 1)
  if (head === '+' || head === '-') {
    n = n.substring(1)
  } else {
    head = ''
  }
  n = n.toString().replace(/,/gi, '')
  n = accMul(Number(n), 100).toFixed(2)
  let re = /\d{1,3}(?=(\d{3})+$)/g
  let backValue = n.replace(/^(\d+)((\.\d*)?)$/, function (s, s1, s2) {
    return s1.replace(re, '$&,') + s2
  })
  // 转换完加上加减号
  if (head) backValue = head + backValue
  return backValue
}

export function numberTwoPoint(val) {
  if (val === undefined || val === '' || val === null) {
    return '-'
  }
  else {
    return Number(val).toFixed(2)
  }
}
/* 金额（元）千分位 */
export function moneyThousand(n) {
  if (!n && n !== 0) return '-'
  if (n === 0) return '0'
  // 如果前面有加减符号
  let head = ''
  if (typeof n === 'number') n = String(n)
  head = n.substring(0, 1)
  if (head === '+' || head === '-') {
    n = n.substring(1)
  } else {
    head = ''
  }
  n = n.toString().replace(/,/gi, '')
  let re = /\d{1,3}(?=(\d{3})+$)/g
  let backValue = n.replace(/^(\d+)((\.\d*)?)$/, function (s, s1, s2) {
    return s1.replace(re, '$&,') + s2
  })
  // 转换完加上加减号
  if (head) backValue = head + backValue
  return backValue
}

/* 金额（元）千分位，保留两位小数 */
export function moneyYuan(n) {
  if (!n && n !== 0) return '-'
  if (n === '--') return '-'
  if (n === 0) return '0.00'
  // 如果前面有加减符号
  let head = ''
  if (typeof n === 'number') n = String(n)
  head = n.substring(0, 1)
  if (head === '+' || head === '-') {
    n = n.substring(1)
  } else {
    head = ''
  }
  n = n.toString().replace(/,/gi, '')
  n = Number(n).toFixed(2)
  let re = /\d{1,3}(?=(\d{3})+$)/g
  let backValue = n.replace(/^(\d+)((\.\d*)?)$/, function (s, s1, s2) {
    return s1.replace(re, '$&,') + s2
  })
  // 转换完加上加减号
  if (head) backValue = head + backValue
  return backValue
}

export function baifenlv2(n) {
  if (!n && n !== 0) return '-'
  if (n === 0) return '0.00'
  // 如果前面有加减符号
  let head = ''
  if (typeof n === 'number') n = String(n)
  head = n.substring(0, 1)
  if (head === '+' || head === '-') {
    n = n.substring(1)
  } else {
    head = ''
  }
  n = n.toString().replace(/,/gi, '')
  n = accMul(Number(n), 100).toFixed(2)
  let re = /\d{1,3}(?=(\d{3})+$)/g
  let backValue = n.replace(/^(\d+)((\.\d*)?)$/, function (s, s1, s2) {
    return s1.replace(re, '$&,') + s2
  })
  // 转换完加上加减号
  if (head) backValue = head + backValue
  return backValue+'%'
}

export function createTreeDataExternLink(nodes, treeRootId, externalPageNest) {
  for (let i = 0; i < nodes.length; i++) {
    if (nodes[i].pId == treeRootId) {
      break;
    } else if (i == nodes.length - 1) {
      Message.closeAll();
      Message({
        message: "数据格式错误",
        type: "error",
        duration: 2 * 1000,
      });
    } else {
    }
  }
  // let nodes01 = [
  //   {
  //     "actionid": "1",
  //     "actionpid": "0",
  //     "id": "1",
  //     "name": "管理视图",
  //     "pId": "0",
  //     "vcactioncode": "MENU.PORTAL",
  //     "vcactionname": "管理视图",
  //     "vcactiontype": "PAGE.PERMISSION.TYPE.MU",
  //     "vcgroup": "本系统",
  //     "vcicon": "dashboard",
  //     "vcmodel": "内部链接",
  //     "vcpid": "1",
  //     "vcremark": "views/managementView/management",
  //     "vcstatus": "启用",
  //     "vcteam": "0",
  //     "vcurl": "/managementView"
  //   },
  //   {
  //     "actionid": "101",
  //     "actionpid": "1",
  //     "id": "101",
  //     "name": "管理视图",
  //     "pId": "1",
  //     "vcactioncode": "MENU.PORTAL",
  //     "vcactionname": "管理视图",
  //     "vcactiontype": "PAGE.PERMISSION.TYPE.MU",
  //     "vcgroup": "本系统",
  //     "vcicon": "fa fa-home",
  //     "vcmodel": "内部链接",
  //     "vcpid": "101",
  //     "vcremark": "views/managementView/management",
  //     "vcstatus": "启用",
  //     "vcteam": "0",
  //     "vcurl": "management"
  //   },
  //   {
  //     "actionid": "102",
  //     "actionpid": "1",
  //     "id": "102",
  //     "name": "投资经理视图",
  //     "pId": "1",
  //     "vcactioncode": "MENU.PORTAL",
  //     "vcactionname": "投资经理视图",
  //     "vcactiontype": "PAGE.PERMISSION.TYPE.MU",
  //     "vcgroup": "本系统",
  //     "vcicon": "fa fa-home",
  //     "vcmodel": "内部链接",
  //     "vcpid": "101",
  //     "vcremark": "views/managementView/investmentManager",
  //     "vcstatus": "启用",
  //     "vcteam": "0",
  //     "vcurl": "investmentManager"
  //   },
  // ]

  let nodesFilters = nodes;

  // 测试单页面
  // nodesFilters.splice(1, 1);
  // nodesFilters[0].vcurl = "/dashboard";
  // nodesFilters[0].vcremark = "views/home/index";
  // nodesFilters.push({
  //   "actionid": "101232",
  //   "actionpid": "0",
  //   "id": "101232",
  //   "name": "投资经理视图",
  //   "pId": "0",
  //   "vcactioncode": "MENU.PORTAL",
  //   "vcactionname": "投资经理视图",
  //   "vcactiontype": "PAGE.PERMISSION.TYPE.MU",
  //   "vcgroup": "本系统",
  //   "vcicon": "dashboard",
  //   "vcmodel": "内部链接",
  //   "vcpid": "101",
  //   "vcremark": "views/home/index",
  //   "vcstatus": "启用",
  //   "vcteam": "0",
  //   "vcurl": "/investmentManager"
  // })
  // console.log(nodesFilters);
  let groups = {};
  // 按父节点将节点分组
  for (let i in nodesFilters) {
    //只遍历是菜单类型的 并且是菜单类型是启用的
    if (
      nodesFilters[i].vcactiontype == "PAGE.PERMISSION.TYPE.MU" &&
      nodesFilters[i].vcstatus == "启用" &&
      nodesFilters[i].vcurl !== undefined
    ) {
      //截取不规范的URL保留前边
      // nodesFilters[i].vcurl = nodesFilters[i].vcurl.split("?")[0];

      if (!groups[nodesFilters[i].pId]) {
        groups[nodesFilters[i].pId] = [];
      }
      groups[nodesFilters[i].pId].push(nodesFilters[i]);
      if (treeRootId && treeRootId === nodesFilters[i].id) {
        // 发现传入的根节点id作为节点id时，将根节点设置为该节点的父节点
        treeRootId = nodesFilters[i].pId;
      }
    } else {
    }
  }

  let rootNodes = groups[treeRootId];
  groups[treeRootId] = null; // [SAFEGUARD]防止自为父节点或互为父节点（有环图结构）导致的死循环
  function traverseTreeNodeGroup(treeNodeGroup) {
    for (var i in treeNodeGroup) {
      var node = treeNodeGroup[i];
      if (node.vcactionname === undefined) {
        node.vcactionname = "";
      } else {
      }
      if (node.vcurl === undefined) {
        node.vcurl = "";
      } else {
      }
      if (node.vcicon === undefined) {
        node.vcicon = "";
      } else {
      }
      if (node.vcremark === undefined) {
        node.vcremark = "";
      } else {
      }

      // component:resolve=>(require([`@/${formUrl}.vue`],resolve)),

      // 顶部路由 / / 名字
      node.name = node.name + node.id; // 防止name相同报错
      // 路由地址  带？的单独处理
      if (node.vcmodel == "外部链接") {
        // 添加
        node.iframeLink = node.vcurl;
        node.path = node.id;
      } else if (node.vcurl.indexOf("?") != -1) {
        if (node.vcurl.startsWith("outer")) {
          // 添加
          node.iframeLink = node.vcurl;
          node.path = node.id;
        } else {
          node.path = node.vcurl.split("?").join(":");
        }
      } else {
        node.path = node.vcurl;
      }
      // 去除将子路由作为根路由显示在侧边栏
      node.alwaysShow = true;
      // 描述
      node.meta = {
        title: node.vcactionname,
        icon: node.vcicon,
        vcactioncode: node.vcactioncode,
        suffix: node.vcurl,
      };
      //表单路径
      let componentPath = node.vcremark;
      // console.log(componentPath);
      node.component = (resolve) =>
        require([`@/${componentPath}.vue`], resolve);

      if (groups[node.id]) {
        node.children = groups[node.id];
        groups[node.id] = null; // [SAFEGUARD]防止自为父节点或互为父节点（有环图结构）导致的死循环
        traverseTreeNodeGroup(node.children);
      }
    }
  }
  traverseTreeNodeGroup(rootNodes);
  for (let i in rootNodes) {
    // 如果不存在children属性 则是单个菜单 需要手动构建children
    if (!rootNodes[i].children) {
      //防止对象间赋值互相覆盖
      let obj = JSON.stringify(rootNodes[i]);
      rootNodes[i].children = [];
      rootNodes[i].children.push(JSON.parse(obj));
      rootNodes[i].children[0].path = "";
      rootNodes[i].children[0].component = (resolve) =>
        require([`@/${rootNodes[i].children[0].vcremark}.vue`], resolve);
      rootNodes[i].children[0].meta.icon = "";
      // 不去除将子路由作为根路由显示在侧边栏
      rootNodes[i].alwaysShow = false;
    }
    // 父菜单页面根节点指向
    // 如果是被外部页面嵌套的 就不需要Layout
    if (externalPageNest === true) {
      rootNodes[i].component = (resolve) =>
        require([`@/views/routerPage/index.vue`], resolve);
    } else {
      rootNodes[i].component = Layout;
    }
    //删除存在子级的父级的name  key值
    if (rootNodes[i].children && rootNodes[i].children.length)
      delete rootNodes[i].name;
  }
  return rootNodes;
}

export function commafy(num) {
  if ((num + "").Trim() == "") {
    return "";
  }
  if (isNaN(num)) {
    return "";
  }
  num = num + "";
  if (/^.*\..*$/.test(num)) {
    varpointIndex = num.lastIndexOf(".");
    varintPart = num.substring(0, pointIndex);
    varpointPart = num.substring(pointIndex + 1, num.length);
    intPart = intPart + "";
    var re = /(-?\d+)(\d{3})/
    while (re.test(intPart)) {
      intPart = intPart.replace(re, "$1,$2")
    }
    num = intPart + "." + pointPart;
  } else {
    num = num + "";
    var re = /(-?\d+)(\d{3})/
    while (re.test(num)) {
      num = num.replace(re, "$1,$2")
    }
  }
  return num;
}

/* 金额（元）千分位，保留4位小数 */
export function moneyYuan4(n) {
  if (!n && n !== 0) return '-'
  if (n === 0) return '0.0000'
  // 如果前面有加减符号
  let head = ''
  if (typeof n === 'number') n = String(n)
  head = n.substring(0, 1)
  if (head === '+' || head === '-') {
    n = n.substring(1)
  } else {
    head = ''
  }
  n = n.toString().replace(/,/gi, '')
  n = Number(n).toFixed(4)
  let re = /\d{1,3}(?=(\d{3})+$)/g
  let backValue = n.replace(/^(\d+)((\.\d*)?)$/, function (s, s1, s2) {
    return s1.replace(re, '$&,') + s2
  })
  // 转换完加上加减号
  if (head) backValue = head + backValue
  return backValue
}

/* 金额（元）千分位，保留4位小数 */
export function moneyYuanFour(n) {
  if (!n && n !== 0) return '-'
  if (n === 0) return '0.0000'
  // 如果前面有加减符号
  let head = ''
  if (typeof n === 'number') n = String(n)
  head = n.substring(0, 1)
  if (head === '+' || head === '-') {
    n = n.substring(1)
  } else {
    head = ''
  }
  n = n.toString().replace(/,/gi, '')
  n = Number(n).toFixed(4)
  let re = /\d{1,3}(?=(\d{3})+$)/g
  let backValue = n.replace(/^(\d+)((\.\d*)?)$/, function (s, s1, s2) {
    return s1.replace(re, '$&,') + s2
  })
  // 转换完加上加减号
  if (head) backValue = head + backValue
  return backValue
}

/* 金额（万元）千分位，保留两位小数 */
export function moneyMillion(n) {
  if (!n && n !== 0) return '-'
  if (n === 0) return '0.00'
  // 如果前面有加减符号
  let head = ''
  if (typeof n === 'number') n = String(n)
  head = n.substring(0, 1)
  if (head === '+' || head === '-') {
    n = n.substring(1)
  } else {
    head = ''
  }
  n = n.toString().replace(/,/gi, '')
  n = accDiv(Number(n), 10000).toFixed(2)
  let re = /\d{1,3}(?=(\d{3})+$)/g
  let backValue = n.replace(/^(\d+)((\.\d*)?)$/, function (s, s1, s2) {
    return s1.replace(re, '$&,') + s2
  })
  // 转换完加上加减号
  if (head) backValue = head + backValue
  return backValue
}

/* 金额（亿元）千分位，保留两位小数 */
export function moneyHundredMillion(n) {
  if (!n && n !== 0) return '-'
  if (n === 0) return '0.00'
  // 如果前面有加减符号
  let head = ''
  if (typeof n === 'number') n = String(n)
  head = n.substring(0, 1)
  if (head === '+' || head === '-') {
    n = n.substring(1)
  } else {
    head = ''
  }
  n = n.toString().replace(/,/gi, '')
  n = accDiv(Number(n), 100000000).toFixed(2)
  let re = /\d{1,3}(?=(\d{3})+$)/g
  let backValue = n.replace(/^(\d+)((\.\d*)?)$/, function (s, s1, s2) {
    return s1.replace(re, '$&,') + s2
  })
  // 转换完加上加减号
  if (head) backValue = head + backValue
  return backValue
}

/* 比例乘以100千分位，保留4位小数 */
export function ratioThousand(n) {
  if (!n && n !== 0) return '-'
  if (n === 0) return '0.0000'
  // 如果前面有加减符号
  let head = ''
  if (typeof n === 'number') n = String(n)
  head = n.substring(0, 1)
  if (head === '+' || head === '-') {
    n = n.substring(1)
  } else {
    head = ''
  }
  n = n.toString().replace(/,/gi, '')
  n = accMul(Number(n), 100).toFixed(4)
  let re = /\d{1,3}(?=(\d{3})+$)/g
  let backValue = n.replace(/^(\d+)((\.\d*)?)$/, function (s, s1, s2) {
    return s1.replace(re, '$&,') + s2
  })
  // 转换完加上加减号
  if (head) backValue = head + backValue
  return backValue
}

/* 比例千分位，保留4位小数 */
export function ratioFour(n) {
  if (!n && n !== 0) return '-'
  if (n === 0) return '0.0000'
  // 如果前面有加减符号
  let head = ''
  if (typeof n === 'number') n = String(n)
  head = n.substring(0, 1)
  if (head === '+' || head === '-') {
    n = n.substring(1)
  } else {
    head = ''
  }
  n = n.toString().replace(/,/gi, '')
  n = Number(n).toFixed(4)
  let re = /\d{1,3}(?=(\d{3})+$)/g
  let backValue = n.replace(/^(\d+)((\.\d*)?)$/, function (s, s1, s2) {
    return s1.replace(re, '$&,') + s2
  })
  // 转换完加上加减号
  if (head) backValue = head + backValue
  return backValue
}

// 时间戳
export function timestampTransform(n) {
  if (n === undefined || n === '' || n === null) {
    return '-'
  } else {
    let now = new Date(n),
      y = now.getFullYear(),
      m = now.getMonth() + 1,
      d = now.getDate();
    return y + "-" + (m < 10 ? "0" + m : m) + "-" + (d < 10 ? "0" + d : d);
  }
}

//保留n位小数 累乘多少
export function numberToFixed(val, n, ride) {
  if (val === undefined || val === '' || val === null || val === '--') {
    return '-'
  } else {
    return accMul(val, ride).toFixed(n)
  }
}

//保留n位小数 累乘多少 添加什么字符串
export function numberToFixedStr(val, n, ride, str) {
  if (val === undefined || val === '' || val === null || val === '--') {
    return '-'
  } else {
    // 计算结果并保留n位小数
    const result = accMul(val, ride).toFixed(n);
    // 千分位格式化
    const formattedResult = formatThousand(result);
    // 拼接后缀字符串
    return str ? formattedResult + str : formattedResult;
  }
}
function formatThousand(numStr) {
  const [intPart, decimalPart] = numStr.split('.');
  // 整数部分添加千分位
  const formattedInt = intPart.replace(/\d{1,3}(?=(\d{3})+$)/g, '$&,');
  // 拼接小数部分
  return decimalPart ? `${formattedInt}.${decimalPart}` : formattedInt;
}

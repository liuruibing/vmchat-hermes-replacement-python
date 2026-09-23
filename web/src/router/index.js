import Vue from 'vue'
import Router from 'vue-router'
/* Layout */
import Layout from '@/views/layout/Layout'

Vue.use(Router)

/**
 //当设置 true 的时候该路由不会再侧边栏出现 如401，login等页面，或者如一些编辑页面/edit/1
 hidden: true // (默认 false)

 //当设置 noredirect 的时候该路由在面包屑导航中不可被点击
 redirect: 'noredirect'

 //当你一个路由下面的 children 声明的路由大于1个时，自动会变成嵌套的模式--如组件页面
 //只有一个时，会将那个子路由当做根路由显示在侧边栏--如引导页面
 //若你想不管路由下面的 children 声明的个数都显示你的根路由
 //你可以设置 alwaysShow: true，这样它就会忽略之前定义的规则，一直显示根路由
 alwaysShow: true

 name: 'router-name' //设定路由的名字，一定要填写不然使用<keep-alive>时会出现各种问题
 meta: {
  roles: ['admin', 'editor'] //设置该路由进入的权限，支持多个权限叠加
  title: 'title' //设置该路由在侧边栏和面包屑中展示的名字
  icon: 'svg-name' //设置该路由的图标
  noCache: true //如果设置为true，则不会被 <keep-alive> 缓存(默认 false)
  breadcrumb: false // 如果设置为false，则不会在breadcrumb面包屑中显示
}
 {
  path: '/permission',
  component: Layout,
  redirect: '/permission/index', //重定向地址，在面包屑中点击会重定向去的地址
  hidden: true, // 不在侧边栏线上
  alwaysShow: true, //一直显示根路由
  meta: { roles: ['admin','editor'] }, //你可以在根路由设置权限，这样它下面所以的子路由都继承了这个权限
  children: [{
    path: 'index',
    component: ()=>import('permission/index'),
    name: 'permission',
    meta: {
      title: 'permission',
      icon: 'lock', //图标
      role: ['admin','editor'], //或者你可以给每一个子路由设置自己的权限
      noCache: true // 不会被 <keep-alive> 缓存
    }
  }]
}
 **/

var routerfixed = [
  // {
  //   path: '/dashboard',
  //   component: () => import('@/views/Home.vue'),
  //   pId: '0',
  //   Nochildren: true,
  // },
  {
    path: '/login',
    component: () => import('@/views/login/indexByCode'),
    hidden: true
  },
  //后端登录跳转页面
  {
    path: '/login/back',
    component: () => import('@/views/loginBack/index'),
    hidden: true
  },
  {
    path: '/login/gfwisdom',
    component: () => import('@/views/gfwisdomsso/index'),
    hidden: true
  },
  {
    path: '/redirect',
    component: Layout,
    hidden: true,
    children: [
      {
        path: '/redirect/:path*',
        component: () => import('@/views/redirect/index')
      }
    ]
  },
  {
    path: '/404',
    component: () => import('@/views/errorPage/404'),
    hidden: true
  },
  {
    path: '/403',
    component: () => import('@/views/errorPage/403'),
    hidden: true
  },
  // 期权策略回测结果页（隐藏路由，仅通过代码跳转）
  {
    path: '/optionbacktraderResult',
    component: () => import('@/views/optionbacktrader/result.vue'),
    hidden: true
  },
  // 产品筛选 Demo（静态直达路由）
  {
    path: '/productor-filter-single-demo',
    component: () => import('@/views/productorFilterSingleDemo/index'),
    name: 'smcpsxDemo',
    hidden: true,
    meta: { title: '产品筛选 Demo', noCache: true }
  },
  {
    path: '/productor-filter-single-demo/report',
    component: () => import('@/views/productorFilterSingleDemo/report/index'),
    name: 'smcpsxDemoReport',
    hidden: true,
    meta: { title: '周频净值报告 Demo', noCache: true }
  },

  // {
  //   path: '/',
  //   component: () => import('@/views/errorPage/401'),
  //   hidden: true
  // },
  // 首页
  // {
  //   path: '',
  //   component: Layout,
  //   children: [
  //     {
  //       path: 'dashboard',
  //       component: () => import('@/views/dashboard/index'),
  //       name: 'Dashboard',
  //       meta: { title: 'dashboard', icon: 'dashboard', noCache: true }
  //     }
  //   ]
  // },
  {
    path: '/vmChat',
    component: Layout,
    redirect: '/vmChat/index',
    pId: '0',
    name: 'vmChat',
    Nochildren: true,
    meta: {
      title: 'vmChat',
      icon: 'process'
    },
    children: [
      {
        path: 'index',
        component: () => import('@/views/vmChat/index'),
        name: 'vmChatIndex',
        meta: { title: 'vmChat', icon: 'process', noCache: true }
      }
    ]
  }
]

var routerBack = [
  // 首页
  // {
  //   path: '/',
  //   component: Layout,
  //   redirect: '/dashboard',
  //   pId: '0',
  //   meta: { title: '首页', icon: 'iconfont icon-D-shouye' }, //原icon：dashboard
  //   Nochildren: true,
  //   children: [
  //     {
  //       path: 'dashboard',
  //       name: 'dashboard',
  //       component: () => import('@/views/home/dashboard'),
  //       meta: { title: '首页' }
  //     }
  //   ]
  // },
  // 行业动态
  // {
  //   path: '/hydt',
  //   component: Layout,
  //   pId: '0',
  //   name: 'hydt',
  //   meta: {
  //     title: '行业动态',
  //     icon: ''
  //   },
  //   children: [
  //     {
  //       path: 'zssmsczs',
  //       component: () => import('@/views/industryDynamics/marketIndex'),
  //       name: 'zssmsczs',
  //       meta: { title: '私募市场指数', icon: '' }
  //     },
  //     {
  //       path: 'zssmqxzs',
  //       component: () => import('@/views/industryDynamics/emotionalIndex'),
  //       name: 'zssmqxzs',
  //       meta: { title: '私募情绪指数', icon: '' }
  //     },
  //     {
  //       path: 'fxpl',
  //       component: () => import('@/views/industryDynamics/analyseDiscuss'),
  //       name: 'fxpl',
  //       meta: { title: '分析评论', icon: '' }
  //     },
  //     {
  //       path: 'rdjgdt',
  //       component: () => import('@/views/industryDynamics/hotOrgState'),
  //       name: 'rdjgdt',
  //       meta: { title: '热点机构动态', icon: '' }
  //     }
  //   ]
  // },
  // 私募推荐
  // {
  //   path: '/smtj',
  //   component: Layout,
  //   pId: '0',
  //   name: 'smtj',
  //   meta: {
  //     title: '私募推荐',
  //     icon: ''
  //   },
  //   children: [
  //     {
  //       path: 'jxzsbd',
  //       component: () => import('@/views/PrivateRecommend/selectedIndexList'),
  //       name: 'jxzsbd',
  //       meta: { title: '精选指数榜单', icon: '' }
  //     },
  //     {
  //       path: 'czzsbd',
  //       component: () => import('@/views/PrivateRecommend/growthIndexList'),
  //       name: 'czzsbd',
  //       meta: { title: '成长指数榜单', icon: '' }
  //     },
  //     {
  //       path: 'smphXxb',
  //       component: () => import('@/views/PrivateRecommend/privateRanking'),
  //       name: 'smphXxb',
  //       meta: { title: '私募排行/新星榜', icon: '' }
  //     }
  //   ]
  // },
  // 投前管理
  // {
  //   path: '/tqgl',
  //   component: Layout,
  //   pId: '0',
  //   name: 'tqgl',
  //   meta: {
  //     title: '投前管理',
  //     icon: ''
  //   },
  //   children: [
  //     {
  //       path: 'tgwbcpsx',
  //       component: () => import('@/views/productorFilterNew/index'),
  //       name: 'tgwbcpsx',
  //       meta: { title: '托管/外包产品筛选', icon: '' }
  //     },
  //     // {
  //     //   path: "qscsmcpsx",
  //     //   component: () => import("@/views/productorFilter/index"),
  //     //   name: "qscsmcpsx",
  //     //   meta: { title: "私募产品筛选", icon: "" }
  //     // },
  //     {
  //       path: 'smcpsx',
  //       component: () => import('@/views/productorFilterSingle/index'),
  //       name: 'smcpsx',
  //       meta: { title: '全市场私募产品筛选', icon: '' }
  //     },
  //     {
  //       path: 'smcpxx',
  //       component: () => import('@/views/multiProductDetail/index'),
  //       name: 'smcpxx',
  //       meta: { title: '市场私募产品详细', icon: '' }
  //     },
  //     {
  //       path: 'qscsmglrsx',
  //       component: () => import('@/views/privateManagerSelection'),
  //       name: 'qscsmglrsx',
  //       meta: { title: '私募管理人筛选', icon: '' }
  //     },
  //     {
  //       path: 'wdgz',
  //       component: () => import('@/views/myFocus/index'),
  //       name: 'wdgz',
  //       meta: { title: '我的关注', icon: '' }
  //     },
  //     {
  //       path: 'tzjlsx',
  //       component: () => import('@/views/managerFilter/index'),
  //       name: 'tzjlsx',
  //       meta: { title: '投资经理筛选', icon: '' }
  //     },
  //     {
  //       path: 'tzjlfx',
  //       component: () => import('@/views/managerFilter/detail'),
  //       name: 'tzjlfx',
  //       hidden: true,
  //       meta: { title: '投资经理分析', icon: '' }
  //     }
  //   ]
  // },
  // 投中管理
  // {
  //   path: '/tzgl',
  //   component: Layout,
  //   pId: '0',
  //   name: 'tzgl',
  //   meta: {
  //     title: '投中管理',
  //     icon: ''
  //   },
  //   children: [
  //     {
  //       path: 'lcgl',
  //       component: () => import('@/views/routerPage/index'),
  //       name: 'lcgl',
  //       meta: { title: '准入池流程管理', icon: '' },
  //       children: [
  //         {
  //           path: 'cplr',
  //           component: () => import('@/views/AccessPoolProcess/ProductEntry'),
  //           name: 'cplr',
  //           meta: { title: '产品录入', icon: '' }
  //         },
  //         {
  //           path: 'zrc',
  //           component: () => import('@/views/AccessPoolProcess/AccessPool'),
  //           name: 'zrc',
  //           meta: { title: '准入池', icon: '' }
  //         },
  //         {
  //           path: 'cpsp',
  //           component: () => import('@/views/AccessPoolProcess/ProductExamine'),
  //           name: 'cpsp',
  //           meta: { title: '准入审批', icon: '' }
  //         },
  //         {
  //           path: 'examine/:id',
  //           component: () => import('@/views/AccessPoolProcess/ProductExamine/examine.vue'),
  //           name: 'examine',
  //           meta: { title: '提交/审批', icon: '' }
  //         },
  //         {
  //           path: 'admitFileUpLoad',
  //           component: () => import('@/views/AccessPoolProcess/ProductExamine/fileUpload.vue'),
  //           name: 'admitFileUpLoad',
  //           meta: { title: '准入材料上传', icon: '' }
  //         },
  //         {
  //           path: 'wjgl',
  //           component: () => import('@/views/AccessPoolProcess/fileManage'),
  //           name: 'wjgl',
  //           meta: { title: '文件管理', icon: '' }
  //         },
  //         {
  //           path: 'cpbmd',
  //           component: () => import('@/views/AccessPoolProcess/ProductWhitelist'),
  //           name: 'cpbmd',
  //           meta: { title: '产品白名单', icon: '' }
  //         }
  //       ]
  //     },
  //     {
  //       path: 'mnzh',
  //       component: () => import('@/views/routerPage/index'),
  //       name: 'mnzh',
  //       meta: { title: '模拟组合', icon: '' },
  //       children: [
  //         {
  //           path: 'wdmnzh',
  //           component: () => import('@/views/simulationGroup/analogComb'),
  //           name: 'wdmnzh',
  //           meta: { title: '模拟组合', icon: '' }
  //         },
  //         {
  //           path: 'tc',
  //           component: () => import('@/views/simulationGroup/tiaoCang'),
  //           name: 'tc',
  //           meta: { title: '调仓', icon: '' }
  //         },
  //         {
  //           path: 'treeView',
  //           component: () => import('@/views/simulationGroup/treeView'),
  //           name: 'treeView',
  //           meta: { title: '树形展示', icon: '' }
  //         },
  //         {
  //           path: 'cjmnzh',
  //           component: () => import('@/views/simulationGroup/createSimuComb'),
  //           name: 'cjmnzh',
  //           meta: { title: '创建模拟组合', icon: '' }
  //         },
  //         {
  //           path: 'mnzhgj',
  //           component: () => import('@/views/simulationGroup/groupBuild'),
  //           name: 'mnzhgj',
  //           meta: { title: '组合构建', icon: '' }
  //         },
  //         {
  //           path: 'zcpzmxyh',
  //           component: () => import('@/views/simulationGroup/AssetOptimize'),
  //           name: 'zcpzmxyh',
  //           meta: { title: '资产配置模型优化', icon: '' }
  //         },
  //         {
  //           path: 'hcfx',
  //           component: () => import('@/views/simulationGroup/backTestAnalyse'),
  //           name: 'zhhc',
  //           meta: { title: '回测分析', icon: '' }
  //         }
  //       ]
  //     }
  //   ]
  // },
  // 投后管理
  // {
  //   path: '/thgl',
  //   name: 'thgl',
  //   component: Layout,
  //   pId: '0',
  //   meta: { title: '投后管理', icon: '' }, //原icon：dashboard
  //   children: [
  //     {
  //       path: 'zhfx',
  //       component: () => import('@/views/routerPage/index'),
  //       name: 'zhfx',
  //       meta: { title: '组合分析', icon: '' },
  //       children: [
  //         {
  //           path: 'wdzh',
  //           name: 'wdzh',
  //           component: () => import('@/views/groupAnalyse/myGroup'),
  //           meta: { title: '我的组合' }
  //         },
  //         {
  //           path: 'jxgy',
  //           name: 'jxgy',
  //           component: () => import('@/views/groupAnalyse/kpiAttribute'),
  //           meta: { title: '绩效归因' }
  //         },
  //         {
  //           path: 'cpjg',
  //           name: 'cpjg',
  //           component: () => import('@/views/groupAnalyse/productMix'),
  //           meta: { title: '产品结构管理' }
  //         },
  //         {
  //           path: 'ctfx',
  //           name: 'ctfx',
  //           component: () => import('@/views/groupAnalyse/penetrateAnalyse'),
  //           meta: { title: '穿透分析' }
  //         }
  //       ]
  //     },
  //     {
  //       path: 'cpglpj',
  //       component: () => import('@/views/routerPage/index'),
  //       name: 'cpglpj',
  //       meta: { title: '产品/管理人评价', icon: '' },
  //       children: [
  //         {
  //           path: 'glrpj',
  //           name: 'glrpj',
  //           component: () => import('@/views/productManagerEvaluate/managerEvaluate'),
  //           meta: { title: '管理人评价' }
  //         },
  //         {
  //           path: 'cppj',
  //           name: 'cppj',
  //           component: () => import('@/views/productManagerEvaluate/productEvaluate'),
  //           meta: { title: '产品评价' }
  //         }
  //       ]
  //     },
  //     {
  //       path: 'zhcx',
  //       component: () => import('@/views/routerPage/index'),
  //       name: 'zhcx',
  //       meta: { title: '综合查询', icon: '' },
  //       children: [
  //         {
  //           path: 'gzzbzs',
  //           name: 'gzzbzs',
  //           component: () => import('@/views/integratedQuery/valuationTrend'),
  //           meta: { title: '估值指标走势' }
  //         },
  //         {
  //           path: 'zhcccx',
  //           name: 'zhcccx',
  //           component: () => import('@/views/integratedQuery/positionInquiry'),
  //           meta: { title: '综合持仓查询' }
  //         },
  //         {
  //           path: 'zjjcccx',
  //           name: 'zjjcccx',
  //           component: () => import('@/views/integratedQuery/subfundPositioninquiry'),
  //           meta: { title: '子基金持仓查询' }
  //         },
  //         {
  //           path: 'cpsscx',
  //           name: 'cpsscx',
  //           component: () => import('@/views/integratedQuery/redemptionInquiry'),
  //           meta: { title: '产品申赎查询' }
  //         },
  //         {
  //           path: 'gzbcx',
  //           name: 'gzbcx',
  //           component: () => import('@/views/integratedQuery/valuationQuery'),
  //           meta: { title: '估值表查询' }
  //         }
  //       ]
  //     }
  //   ]
  // },
  // 需求互动
  // {
  //   path: '/gljsc',
  //   name: 'gljsc',
  //   component: Layout,
  //   pId: '0',
  //   meta: { title: '需求互动', icon: '' }, //原icon：dashboard
  //   children: [
  //     {
  //       path: '/bzhglxq',
  //       name: 'bzhglxq',
  //       component: () => import('@/views/routerPage/index'),
  //       meta: { title: '标准化需求管理' },
  //       children: [
  //         {
  //           path: '/jdsq',
  //           name: 'jdqs',
  //           component: () => import('@/views/demandInteract/publicRequest'),
  //           meta: { title: '尽调申请' }
  //         },
  //         // {
  //         //   path: "/sjsqsq",
  //         //   name: "sjsqsq",
  //         //   component: () => import("@/views/managementCockpit/publicRequest"),
  //         //   meta: { title: "数据授权申请" }
  //         // },
  //         {
  //           path: '/xxyzsq',
  //           name: 'xxyzsq',
  //           component: () => import('@/views/demandInteract/publicRequest'),
  //           meta: { title: '信息验证申请' }
  //         }
  //       ]
  //     },
  //     {
  //       path: '/gxhxqgl',
  //       name: 'gxhxqgl',
  //       component: () => import('@/views/routerPage/index'),
  //       meta: { title: '个性化需求管理' },
  //       children: [
  //         {
  //           path: '/sjzj',
  //           name: 'sjzj',
  //           component: () => import('@/views/demandInteract/publicRequest'),
  //           meta: { title: '数据质检' }
  //         }
  //       ]
  //     },
  //     {
  //       path: '/sycp',
  //       name: 'sycp',
  //       component: () => import('@/views/demandInteract/privateProduct'),
  //       meta: { title: '私有产品' }
  //     },
  //     {
  //       path: '/grzx',
  //       name: 'grzx',
  //       component: () => import('@/views/routerPage/index'),
  //       meta: { title: '个人中心' },
  //       children: [
  //         {
  //           path: '/cqsq',
  //           name: 'cqsq',
  //           component: () => import('@/views/demandInteract/productApply'),
  //           meta: { title: '产品申请' }
  //         },
  //         // {
  //         //   path: "/sjzj",
  //         //   name: "sjzj",
  //         //   component: () => import("@/views/managementCockpit/dataTest"),
  //         //   meta: { title: "数据质检" }
  //         // },
  //         {
  //           path: '/dbsx',
  //           name: 'dbsx',
  //           component: () => import('@/views/demandInteract/toDoList'),
  //           meta: { title: '待办事项' }
  //         }
  //       ]
  //     }
  //   ]
  // },
  // 单产品详情页面
  // {
  //   path: '/cpxq/:id',
  //   name: 'cpxq',
  //   component: Layout,
  //   pId: '0',
  //   Nochildren: true,
  //   meta: { title: '市场私募产品明细', icon: '', visible: 'false' },
  //   children: [
  //     {
  //       path: '',
  //       name: 'cpxq',
  //       component: () => import('@/views/singleProduct/index'),
  //       meta: { title: '市场私募产品明细', visible: 'false' }
  //     }
  //   ]
  // }
  // // 系统管理
  // {
  //   path: '/xtgl',
  //   name: 'xtgl',
  //   component: Layout,
  //   pId: '0',
  //   meta: { title: '系统管理', icon: '' }, //原icon：dashboard
  //   Nochildren: true,
  //   children: [
  //     {
  //       path: 'xtgl',
  //       name: 'xtgl',
  //       component: () => import('@/views/routerPage/index'),
  //       meta: { title: '系统管理' },
  //       children: [
  //         {
  //           path: '/zcgl',
  //           name: 'zcgl',
  //           // component: () => import('@/views/systemManage/registerManange'),
  //           meta: { title: '注册管理' }
  //         },
  //         {
  //           path: '/bmgl',
  //           name: 'bmgl',
  //           // component: () => import('@/views/systemManage/deptManage'),
  //           meta: { title: '部门管理' }
  //         },
  //         {
  //           path: '/yhgl',
  //           name: 'yhgl',
  //           // component: () => import('@/views/systemManage/userManage'),
  //           meta: { title: '用户管理' }
  //         },
  //         {
  //           path: '/jsgl',
  //           name: 'jsgl',
  //           // component: () => import('@/views/systemManage/roleManage'),
  //           meta: { title: '角色管理' }
  //         },
  //         {
  //           path: '/cpsqgl',
  //           name: 'cpsqgl',
  //           // component: () => import('@/views/systemManage/productAuthorizationManage'),
  //           meta: { title: '产品授权管理' }
  //         },
  //         {
  //           path: '/cpsqcx',
  //           name: 'cpsqcx',
  //           // component: () => import('@/views/systemManage/productAuthorizationQuery'),
  //           meta: { title: '产品授权查询' }
  //         },
  //         {
  //           path: '/czrz',
  //           name: 'czrz',
  //           // component: () => import('@/views/systemManage/operationLog'),
  //           meta: { title: '操作日志' }
  //         },
  //         {
  //           path: '/cdgl',
  //           name: 'cdgl',
  //           // component: () => import('@/views/systemManage/meauManage'),
  //           meta: { title: '菜单管理' }
  //         }
  //       ]
  //     },
  //     {
  //       path: '/khxq',
  //       name: 'khxq',
  //       // component: () => import('@/views/customerDemand/index'),
  //       meta: { title: '客户需求' }
  //     },
  //     {
  //       path: '/sjzj',
  //       name: 'sjzj',
  //       // component: () => import('@/views/dataCheck/index'),
  //       meta: { title: '数据质检' }
  //     },
  //     {
  //       path: '/sjkb',
  //       name: 'sjkb',
  //       // component: () => import('@/views/dataBoard/index'),
  //       meta: { title: '数据看板' }
  //     },
  //     {
  //       path: '/etl',
  //       name: 'etl',
  //       component: () => import('@/views/routerPage/index'),
  //       meta: { title: 'etl管理' },
  //       children: [
  //         {
  //           path: '/cssz',
  //           name: 'cssz',
  //           // component: () => import('@/views/etlManage/paramSet'),
  //           meta: { title: '参数设置' }
  //         },
  //         {
  //           path: '/sjysz',
  //           name: 'sjysz',
  //           // component: () => import('@/views/etlManage/dataSourceSet'),
  //           meta: { title: '数据源设置' }
  //         },
  //         {
  //           path: '/rwsz',
  //           name: 'rwsz',
  //           // component: () => import('@/views/etlManage/taskSet'),
  //           meta: { title: '任务设置' }
  //         },
  //         {
  //           path: '/rwz',
  //           name: 'rwz',
  //           // component: () => import('@/views/etlManage/taskGroup'),
  //           meta: { title: '任务组' }
  //         },
  //         {
  //           path: '/rzjs',
  //           name: 'rzjs',
  //           // component: () => import('@/views/etlManage/logCheck'),
  //           meta: { title: '日志检索' }
  //         }
  //       ]
  //     },
  //     {
  //       path: '/etlDispatch',
  //       name: 'etlDispatch',
  //       component: () => import('@/views/routerPage/index'),
  //       meta: { title: 'etl调度控制' },
  //       children: [
  //         {
  //           path: '/ddsz',
  //           name: 'ddsz',
  //           // component: () => import('@/views/etlDispatch/dispatchSet'),
  //           meta: { title: '调度设置' }
  //         },
  //         {
  //           path: '/ddlb',
  //           name: 'ddlb',
  //           // component: () => import('@/views/etlDispatch/dispatchList'),
  //           meta: { title: '调度列表' }
  //         },
  //         {
  //           path: '/ddzxjl',
  //           name: 'ddzxjl',
  //           // component: () => import('@/views/etlDispatch/dispatchRecord'),
  //           meta: { title: '调度执行记录' }
  //         },
  //         {
  //           path: '/sjhd',
  //           name: 'sjhd',
  //           // component: () => import('@/views/etlDispatch/dataCheckLog'),
  //           meta: { title: '数据核对检查日志' }
  //         },
  //         {
  //           path: '/zhs',
  //           name: 'zhs',
  //           // component: () => import('@/views/etlDispatch/groupTreeDispatch'),
  //           meta: { title: '组合树调度监控记录' }
  //         }
  //       ]
  //     },
  //     {
  //       path: '/generalReportManage',
  //       name: 'generalReportManage',
  //       component: () => import('@/views/routerPage/index'),
  //       meta: { title: '通用报告管理' },
  //       children: [
  //         {
  //           path: '/sqlpz',
  //           name: 'sqlpz',
  //           component: () => import('@/views/generalReportManage/sqlConfig'),
  //           meta: { title: 'SQL配置管理' }
  //         },
  //         {
  //           path: '/zbpz',
  //           name: 'zbpz',
  //           component: () => import('@/views/generalReportManage/indexConfig'),
  //           meta: { title: '指标配置管理' }
  //         },
  //         {
  //           path: '/mbpz',
  //           name: 'mbpz',
  //           component: () => import('@/views/generalReportManage/templateConfig'),
  //           meta: { title: '模板配置管理' }
  //         }
  //       ]
  //     },
  //     {
  //       path: '/backStageManage',
  //       name: 'backStageManage',
  //       component: () => import('@/views/routerPage/index'),
  //       meta: { title: '功能管理后台' },
  //       children: [
  //         {
  //           path: '/ybgl',
  //           name: 'ybgl',
  //           component: () => import('@/views/backStageManage/researchReport'),
  //           meta: { title: '研报管理' }
  //         },
  //         {
  //           path: '/cptjgl',
  //           name: 'cptjgl',
  //           component: () => import('@/views/backStageManage/productRecommended'),
  //           meta: { title: '产品推荐管理' }
  //         },
  //         {
  //           path: '/jgtjgl',
  //           name: 'jgtjgl',
  //           component: () => import('@/views/backStageManage/orgRecommended'),
  //           meta: { title: '机构推荐管理' }
  //         }
  //       ]
  //     }
  //   ]
  // }
]

var routerResult = routerfixed.concat(routerBack)

// constantRouterMap： 代表那些不需要动态判断权限的路由，如登录页、404、等通用页面。
export const constantRouterMap = routerResult

export default new Router({
  // mode: 'history', // require service support
  scrollBehavior(to, from, savedPosition) {
    let flag = false
    for (let i = 0; i < window.saveIframeY.length; i++) {
      if (window.saveIframeY[i].path == to.fullPath) {
        flag = true
        setTimeout(() => {
          window.frames[i].scrollTo(0, 0)
          window.frames[i].scrollTo(0, window.saveIframeY[i].yValue)
        }, 0)
      }
    }
    if (!flag) {
      let appEle = document.getElementsByClassName('app-main')[0]
      let fundAnalysisOverviewEle = document.getElementsByClassName('fundAnalysisOverview')[0]
      if (appEle) {
        if (fundAnalysisOverviewEle) {
          appEle.scrollTop = to.meta.scrollY || 0
        } else {
          let iframNum = window.saveIframeY.length
          let mainEleArray = document.getElementsByClassName('el-main')
          if (mainEleArray.length > iframNum) {
            // from.meta.scrollY = mainEleArray[0].scrollTop
            mainEleArray[0].scrollTop = to.meta.scrollY || 0
          } else {
            appEle.scrollTop = to.meta.scrollY || 0
          }
        }
      }
    }
    if (savedPosition) {
      // console.log(savedPosition);
      // return savedPosition
    } else {
      // return { x: 0, y: 0 }
    }
  },
  routes: constantRouterMap
})

// asyncRouterMap： 代表那些需求动态判断权限并通过 addRouters 动态添加的页面。
export const asyncRouterMap = [
  // 权限测试页
  // {
  //   path: '/permission',
  //   component: Layout,
  //   redirect: '/permission/index',
  //   // alwaysShow: true, // will always show the root menu
  //   meta: {
  //     title: 'permission',
  //     icon: 'lock',
  //     roles: ['admin', 'editor'] // you can set roles in root nav
  //   },
  //   children: [
  //     {
  //       path: 'page',
  //       component: () => import('@/views/permission/page'),
  //       name: 'PagePermission',
  //       meta: {
  //         title: 'pagePermission',
  //         roles: ['admin'] // or you can only set roles in sub nav
  //       }
  //     }
  //   ]
  // },
  // {
  //   path: '*',
  //   component: () => import('@/views/errorPage/401'),
  //   hidden: true
  // },
  // { path: '*', redirect: '/404', hidden: true }
]

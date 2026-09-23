import router from './router'
import store from './store'
// import { Message } from 'element-ui'
import NProgress from 'nprogress' // progress bar NProgress.js加载进度插件
import 'nprogress/nprogress.css' // progress bar style
import { getToken, removeCookiesData, removeToken, setCookiesData } from '@/utils/auth' // getToken from cookie
import btnsAuth from '@/utils/btnsAuth'
// 后端路由请求
import { getMenuAll } from '@/api/layOut'
// 遍历后台返回的路由数据
import { createTreeData } from '@/filters/index'
// 引入公共JS方法
import commonFun from '@/filters/common'
import { getCookiesData } from './utils/auth'
import request from '@/utils/request'
import { createSecureWatermark } from '@/utils/watermark';
/* Layout */
// import Layout from '@/views/layout/Layout'
// 测试路由
// import testRoute from './testRoute'
// 设置进度条  样式  加载时间  禁用右侧进度环
NProgress.configure({ easing: 'ease', speed: 500, showSpinner: false }) // NProgress Configuration

// permission judge function
// function hasPermission(roles, permissionRoles) {
//   if (roles.indexOf('admin') >= 0) return true // admin permission passed directly
//   if (!permissionRoles) return true
//   return roles.some(role => permissionRoles.indexOf(role) >= 0)
// }

const whiteList = ['/login', '/loading', '/productor-filter-single-demo', '/productor-filter-single-demo/report'] // no redirect whitelist

let code = null

function getUrlParam(name) {
  var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)') // 构造一个含有目标参数的正则表达式对象
  var r = window.location.search.substr(1).match(reg) // 匹配目标参数
  if (r != null) {
    return decodeURIComponent(r[2])
  }
  return null // 返回参数值
}

// 获取基准下拉数据
function getDatumOption() {
  return new Promise((resolve, reject) => {
    request({
      url: `/api/report/v1.0/data/sql/d43c924b-eebd-4d8f-97e5-ed46b609456d`,
      method: 'post',
      data: {
        indexCode: 'd43c924b-eebd-4d8f-97e5-ed46b609456d'
      }
    })
      .then((res) => {
        if (res.data.status === 0) {
          let resultDim = res.data.data || []
          resultDim = resultDim.map((item) => {
            return {
              label: item.DIM_NME,
              id: item.DIM_CDE
            }
          })
          store.dispatch('addDatumOption', resultDim)
        }
        resolve()
      })
      .catch((err) => {
        resolve()
      })
  })
}

// 默认T-2近一个月的起始时间
function getBaseTime() {
  return new Promise((resolve, reject) => {
    request({
      url: `/api/report/v1.0/data/sql/868b4212-9d41-4ac0-a3db-8896d2913541`,
      method: 'post',
      data: {
        indexCode: '868b4212-9d41-4ac0-a3db-8896d2913541'
      }
    })
      .then((res) => {
        if (res.data.status === 0) {
          var baseTimeData = {};
          if (res.data.data && res.data.data.length > 0) {
            baseTimeData.beginDate = res.data.data[0].beginDate; // 接口返回的默认开始时间
            baseTimeData.endDate = res.data.data[0].endDate; // 接口返回的默认结束时间
          }
          store.dispatch('setBaseTime', baseTimeData)
        }
        resolve()
      })
      .catch((err) => {
        resolve()
      })
  })
}

//获取用户类型
function userType() {
  return new Promise((resolve, reject) => {
    request({
      url: `/api/report/v1.0/data/sql/da489643-1573-4ea0-9003-c2bdbb636e47`,
      method: 'post',
      data: {
        indexCode: 'da489643-1573-4ea0-9003-c2bdbb636e47'
      }
    })
      .then((res) => {
        if (res.data.status === 0) {
          let resultDim = res.data.data
          store.dispatch('adduserType', resultDim[0].usertype)
        }
        resolve()
      })
      .catch((err) => {
        resolve()
      })
  })
}

// 保存iframe页面的滚动条位置
window.saveIframeY = [
  // {
  //   name: 'dcpfx',
  //   path: '/tqgl/dcpfx',
  //   yValue: 0
  // },
  // {
  //   name: 'smcpxx',
  //   path: '/tqgl/smcpxx',
  //   yValue: 0
  // },
  {
    name: 'csbg',
    path: '/thgl/jxbg/csbg',
    yValue: 0
  },
  {
    name: 'qyljxbg',
    path: '/thgl/jxbg/qyljxbg',
    yValue: 0
  },
  {
    name: 'zqljxbg',
    path: '/thgl/jxbg/zqljxbg',
    yValue: 0
  },
  {
    name: 'ctajxbg',
    path: '/thgl/jxbg/ctajxbg',
    yValue: 0
  },
  {
    name: 'jxjb',
    path: '/thgl/jxbg/jxjb',
    yValue: 0
  },
  {
    name: 'fofjxbg',
    path: '/thgl/jxbg/fofjxbg',
    yValue: 0
  },
  {
    name: 'sycpbg',
    path: '/tzgl/sycpbg',
    yValue: 0
  },
  {
    name: 'gmzl',
    path: '/thgl/jxzb/gmzl',
    yValue: 0
  },
  {
    name: 'dwjzbxzl',
    path: '/thgl/jxzb/dwjzbxzl',
    yValue: 0
  },
  {
    name: 'syfx',
    path: '/thgl/jxzb/syfx',
    yValue: 0
  },
  {
    name: 'rsybx',
    path: '/thgl/jxzb/rsybx',
    yValue: 0
  },
  {
    name: 'lhzbfx',
    path: '/thgl/jxzb/lhzbfx',
    yValue: 0
  },
  {
    name: 'dlzcccsx',
    path: '/thgl/jxzb/dlzcccsx',
    yValue: 0
  },
  {
    name: 'qyljckzbsxt',
    path: '/thgl/jxzb/qyljckzbsxt',
    yValue: 0
  },
  {
    name: 'qmccfx',
    path: '/thgl/jxzb/qmccfx',
    yValue: 0
  },
  {
    name: 'cghyfx',
    path: '/thgl/jxzb/cghyfx',
    yValue: 0
  },
  {
    name: 'zqpzpzsx',
    path: '/thgl/jxzb/zqpzpzsx',
    yValue: 0
  },
  {
    name: 'xypjfbsx',
    path: '/thgl/jxzb/xypjfbsx',
    yValue: 0
  },
  {
    name: 'zhjqbdsx',
    path: '/thgl/jxzb/zhjqbdsx',
    yValue: 0
  },
  {
    name: 'syqxpzsx',
    path: '/thgl/jxzb/syqxpzsx',
    yValue: 0
  },
  {
    name: 'spqhdtccqk',
    path: '/thgl/jxzb/spqhdtccqk',
    yValue: 0
  },
  {
    name: 'dlzcjxgy',
    path: '/thgl/jxzb/dlzcjxgy',
    yValue: 0
  },
  {
    name: 'gpflgy',
    path: '/thgl/jxzb/gpflgy',
    yValue: 0
  },
  {
    name: 'zqgyfx',
    path: '/thgl/jxzb/zqgyfx',
    yValue: 0
  },
  {
    name: 'qhqqgyfx',
    path: '/thgl/jxzb/qhqqgyfx',
    yValue: 0
  },
  {
    name: 'jzfxbg',
    path: '/jxbg/dcpbg/jzfxbg',
    yValue: 0
  },
  {
    name: 'zjqyljxbg',
    path: '/jxbg/dcpbg/zjqyljxbg',
    yValue: 0
  },
  {
    name: 'zqjxbg',
    path: '/jxbg/dcpbg/zqjxbg',
    yValue: 0
  },
  {
    name: 'hhclbg',
    path: '/jxbg/dcpbg/hhclbg',
    yValue: 0
  },
  {
    name: 'foffxbg',
    path: '/jxbg/dcpbg/foffxbg',
    yValue: 0
  },
  {
    name: 'ctaljxbg',
    path: '/jxbg/dcpbg/ctaljxbg',
    yValue: 0
  },
  {
    name: 'qqljxbg',
    path: '/jxbg/dcpbg/qqljxbg',
    yValue: 0
  },
  {
    name: 'campisi',
    path: '/zhgl/gymx/campisi',
    yValue: 0
  },
  {
    name: 'ctfxbg',
    path: '/jxbg/dcpbg/ctfxbg',
    yValue: 0
  },
  {
    name: 'tszbbg',
    path: '/jxbg/dcpbg/tszbbg',
    yValue: 0
  },
  {
    name: 'dcpjcbg',
    path: '/jxbg/qtbg/dcpjcbg',
    yValue: 0
  },
  {
    name: 'dcpqybg',
    path: '/jxbg/qtbg/dcpqybg',
    yValue: 0
  },
  {
    name: 'dcpgsbg',
    path: '/jxbg/qtbg/dcpgsbg',
    yValue: 0
  },
  {
    name: 'jbbg',
    path: '/jxbg/dcpbg/jbbg',
    yValue: 0
  },
  {
    name: 'jbbgweek',
    path: '/jxbg/dcpbg/jbbgweek',
    yValue: 0
  },
  {
    name: 'bzbg',
    path: '/jxbg/dcpbg/bzbg',
    yValue: 0
  },
  {
    name: 'gpdt',
    path: '/jxbg/dcpbg/gpdt',
    yValue: 0
  },
  {
    name: 'zqjj',
    path: '/jxbg/dcpbg/zqjj',
    yValue: 0
  },
  {
    name: 'glqh',
    path: '/jxbg/dcpbg/glqh',
    yValue: 0
  },
  {
    name: 'tgmjj',
    path: '/jxbg/dcpbg/tgmjj',
    yValue: 0
  },
  {
    name: 'ccdlbg',
    path: '/jxbg/dcpbg/ccdlbg',
    yValue: 0
  },
  {
    name: 'gqzbbg',
    path: '/jxbg/dcpbg/gqzbbg',
    yValue: 0
  },
  {
    name: 'dyzbg',
    path: '/jxbg/dcpbg/dyzbg',
    yValue: 0
  },
  {
    name: 'cpfgclpyjk',
    path: '/thgl/clpy/cpfgclpyjk',
    yValue: 0
  },
  {
    name: 'zbg',
    path: '/jxbg/dcpbg/zbg',
    yValue: 0
  },
  {
    name: 'jxxczbg',
    path: '/jxbg/dcpbg/jxxczbg',
    yValue: 0
  },

  {
    name: 'zbgxc',
    path: '/jxbg/dcpbg/zbgxc',
    yValue: 0
  },
  {
    name: 'strategyprivate',
    path: '/jxbg/strategybg/strategyprivate',
    yValue: 0
  },
  {
    name: 'factorindex',
    path: '/jxbg/dcpbg/factorindex',
    yValue: 0
  },

  {
    name: 'gyhhfxbg',
    path: '/gyhh/dcpbg/gyhhfxbg',
    yValue: 0
  },

  {
    name: 'zxcedyzbg',
    path: '/jxbg/dcpbg/zxcedyzbg',
    yValue: 0
  },
  {
    name: 'jxbgdcp',
    path: '/jxbg/dcpbg/jxbgdcp',
    yValue: 0
  },
  {
    name: 'customReportView',
    path: '/jxbg/bgzq/customReportView',
    yValue: 0
  },

]

function deepMeauList(array) {
  array.forEach((item) => {
    if (item && item.vcurl) {
      const vcurlLastSegment = item.vcurl.split('/').pop();
      for (let i = 0; i < saveIframeY.length; i++) {
        if (saveIframeY[i].name === vcurlLastSegment) {
          delete item.component;
          break;
        }
      }
    }
    if (item.children && item.children.length > 0) {
      deepMeauList(item.children);
    }
  })
}

// 路由钩子主要是给使用者在路由发生变化时进行一些特殊的处理而定义的函数。
// 在跳转之前执行
// to:router即将进入的路由对象
// from:当前导航即将离开的路由
// next:Function,进行管道中的一个钩子，如果执行完了，则导航的状态就是 confirmed （确认的）；否则为false，终止导航。
router.beforeEach(async (to, from, next) => {
  if (to.name === '指数榜单301') {
    to.meta.title = to.params.title
  }

  const appEle = document.getElementsByClassName('app-main')[0]
  const fundAnalysisOverviewEle = document.getElementsByClassName('fundAnalysisOverview')[0]
  if (appEle) {
    if (fundAnalysisOverviewEle) {
      from.meta.scrollY = appEle.scrollTop
    } else {
      const iframNum = window.saveIframeY.length
      const mainEleArray = document.getElementsByClassName('el-main')
      if (mainEleArray.length > iframNum) {
        from.meta.scrollY = mainEleArray[0].scrollTop
      } else {
        from.meta.scrollY = appEle.scrollTop
      }
    }
  }

  // from.meta.scrollY = mainEle.scrollTop || 0
  for (let i = 0; i < window.saveIframeY.length; i++) {
    if (window.saveIframeY[i].path === from.fullPath) {
      window.saveIframeY[i].yValue = window.frames[i].scrollY
    }
  }

  NProgress.start() // start progress bar
  // 部署验证是否成功 免登录
  if (to.path === '/ping') {
    next()
    NProgress.done() // finish progress bar
  }
  // 显示状态码页面 免登录
  else if (to.path.indexOf('/responseStatus') !== -1) {
    next()
    NProgress.done() // finish progress bar
  }
  // 后端页面登录 不添加token 控制
  else if (to.path.indexOf('/login/back') !== -1) {
    next()
    NProgress.done() // finish progress bar
  } else if (to.path.indexOf('/login/gfwisdom') !== -1) {
    next()
    NProgress.done() // finish progress bar
  } else {
    code = getUrlParam('code')
    if (code) {
      //清空 token 和 名字 角色
      store.commit('SET_TOKEN', '')
      store.commit('SET_NAME', '')
      store.commit('SET_ROLES', [])
      // //清空浏览器 token
      removeToken()
      removeCookiesData('BAIDUID')
      next({ path: '/login/gfwisdom', query: { code } })
      NProgress.done() // finish progress bar
      return
    }

    // 有历史登录记录
    if (getToken()) {
      // 判断是否存在基准下拉的字典，如果不存在则请求，如果存在直接跳过逻辑
      if (store.state.edims.datumOption && store.state.edims.datumOption.length === 0) {
        // 基准下拉的长度为0，走接口请求
        getDatumOption()
      }
      if(!store.state.edims.baseTime){
        getBaseTime()
      }
      // 获取用户类型
      // userType()
      /* has token*/
      if (to.path === '/login') {
        next({ path: '/dashboard', replace: true })
        NProgress.done() // if current page is dashboard will not trigger	afterEach hook, so manually handle it
      } else if (to.path === '/') {
        next({ path: '/dashboard', replace: true })
        NProgress.done()
      } else {
        // 获取当前路由的根路由是什么 选中顶部路由和侧边路由
        const pathSidebar = to.path.split('/')
        store.commit('SET_MEAUTOP', '/' + pathSidebar[1] || '')
        // 如果获取过菜单信息
        if (store.getters.roles.length) {
          // 判断路由是否存在二级 一级路由左侧默认收起来 二级路由默认展开
          const systemRouters = store.state.permission.routers
          const isSingleRoute = commonFun.getTreeOppositeValue(systemRouters, 'path', to.path, 'Nochildren', 'children')
          // 如果Nochildren 等于 true 则为单个菜单
          if (isSingleRoute === true) {
            if (store.getters.sidebar.opened === true) {
              store.dispatch('toggleSideBar')
            } else {
            }
          } else if (store.getters.sidebar.opened === false) {
            store.dispatch('toggleSideBar')
          } else {
          }
          next()
        } else {
          // 获取本地存储用户信息
          const BAIDUID = JSON.parse(localStorage.getItem('BAIDUID')) || {}
          const { account } = BAIDUID
          // 设置角色
          if (account) store.commit('SET_ROLES', [account])
          // 获取T-1时间
          // store.dispatch('selectStartEndDate')
          // 获取后端返回路由

          // 启动pedding
          store.commit('SET_LOGIN_PEDDING', true)
          getMenuAll()
            .then((response) => {
              const meauList = createTreeData(response.data.data, 0)
              deepMeauList(meauList)
              // let meauList = []
              store.state.meauList = meauList

              router.addRoutes(meauList) // 后端动态添加可访问路由表'
              router.addRoutes([{ path: '*', redirect: '/403', hidden: true }]) // 后端动态添加可访问路由表'
              // console.log(router)
              // meauList.pop();
              store.commit('SET_ROUTERS', meauList) // 将路由数据加入到vuex中 渲染左侧列表
              // 判断路由是否存在二级 一级路由左侧默认收起来 二级路由默认展开
              const systemRouters = store.state.permission.routers
              const isSingleRoute = commonFun.getTreeOppositeValue(systemRouters, 'path', to.path, 'Nochildren', 'children')
              // 如果Nochildren 等于 true 则为单个菜单
              if (isSingleRoute === true) {
                if (store.getters.sidebar.opened === true) {
                  store.dispatch('toggleSideBar')
                } else {
                }
              } else if (store.getters.sidebar.opened === false) {
                store.dispatch('toggleSideBar')
              } else {
              }

              next({ ...to, replace: true }) // hack方法 确保addRoutes已完成 ,set the replace: true so the navigation will not leave a history record
              // 按钮权限控制
              btnsAuth(response.data.data)
              const username = store.getters.name;
              createSecureWatermark(username || '未命名用户');
              setTimeout(() => {
                store.dispatch('setLoginPennding', false)
              }, 1000)
              resolve()
            })
            .catch(() => {
              setTimeout(() => {
                store.dispatch('setLoginPennding', false)
              }, 1000)
            })
        }
      }
    } else {
      /* has no token 没有历史登录记录*/
      if (whiteList.indexOf(to.path) !== -1) {
        // 在免登录白名单，直接进入
        // 如果为true 就是后端登录  跳转到
        if (store.state.setting.backendLogin === true) {
          window.location.href = store.state.setting.backendLoginUrl
        } else {
          next()
        }
      }
      // 如果为true 就是后端登录  跳转到
      else if (store.state.setting.backendLogin === true) {
        window.location.href = store.state.setting.backendLoginUrl
      } else {
        next(`/login?redirect=${to.path}`) // 否则全部重定向到登录页
      }
      NProgress.done() // if current page is login will not trigger afterEach hook, so manually handle it
    }
  }
})
// 在跳转之后判断
router.afterEach(() => {
  NProgress.done() // finish progress bar
  // 跳转页面的时候隐藏tooltip防止一直显示
  const list = document.getElementsByClassName('el-tooltip__popper')
  if (list.length > 0) {
    list[list.length - 1].style.display = 'none'
  }
})

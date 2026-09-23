const user = {
  state: {
    loginPennding: false,
    //websocket url地址
    wsurl: 'ws://localhost:3000/',
    //是否显示加载中
    loadingShow: true,
    // 是否是后端登录
    backendLogin: false,
    // 后端登录跳转地址
    backendLoginUrl: 'http://sso-test.hq.cpic.com',
    //后端请求地址
    baseApi: process.env.BASE_API,
    //页面底部说明
    // footerText:'Data Driver @2020',
    footerText: '版权所有@中国广发证券股份有限公司 京公网安备11010202007775号 京ICP备10021160号',
    // 数据时间说明
    dateHint: '注 : 数据更新到T-1日',
    // 是否要默认查询
    isOnQuery: true,
    // 开始时间
    startDate: '',
    // 结束时间
    endDate: '',
    fromPlatForm: false,
    saveUnifiedLoginURL: '',
    theme: 'red', // 默认红色主题色
  },
  // 改变状态，不允许异步
  mutations: {
    SET_LOGIN_PEDDING: (state, status) => {
      state.loginPennding = status
    },
    SET_UNIFIEDLOGIN_URL: (state, status) => {
      state.saveUnifiedLoginURL = status
    },
    SET_THEME: (state, status) => {
      state.theme = status
    },
    SET_FROMPLATFORM: (state, status) => {
      state.fromPlatForm = status
    },
    // 设置开始时间
    SET_START_DATE: (state, startDate) => {
      state.startDate = startDate
    },
    // 设置结束时间
    SET_END_DATE: (state, endDate) => {
      state.endDate = endDate
    }
  },
  // 改变状态,允许异步
  actions: {
    setLoginPennding({commit}, status) {
      commit('SET_LOGIN_PEDDING', status)
    }
  }
}

export default user

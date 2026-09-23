const edims = {
  state: {
    edimsBuffer: {},
    datumOption: [], //基准数据
    // 隐藏数据的菜单页面
    hideDataUrl: [
      '/tqgl/qscsmcpsx/qscsmcpsx', // 私募产品筛选
      '/tqgl/wdgz/wdgz',// 投前-我的关注
      '/tqgl/glrxq',//私募管理人筛选，管理人详情页面
      '/hydt/smrd/cprd/XX',// 特点产品
    ],
    baseTime: null
  },
  mutations: {
    ADD_EDIMS: (state, edimsObject) => {
      for (let obj in edimsObject) {
        state.edimsBuffer[obj] = edimsObject[obj]
      }
    },
    ADD_DATUMOPTION: (state, value) => {
      state.datumOption = value
    },
    ADD_USERTYPE: (state, value) => {
      state.userType = value
    },
    SET_BASE_TIME: function(state, timeData) {
      state.baseTime = timeData
    }
  }
  ,
  actions: {
    addEdims({commit}, {result}) {
      commit('ADD_EDIMS', result)
    },
    addDatumOption({commit}, value) {
      commit('ADD_DATUMOPTION', value)
    },
    adduserType({commit}, value) {
      commit('ADD_USERTYPE', value)
    },
    setBaseTime: function({ commit }, timeData) {
      commit('SET_BASE_TIME', timeData);
    }
  }
}

export default edims

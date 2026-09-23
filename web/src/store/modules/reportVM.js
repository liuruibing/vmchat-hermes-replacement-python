import Vue from 'vue'

const reportVM = {
  state: {
    conditionTreeData: [], // 条件树
    indexTreeData: [], // 指标树
    currentConditionTreeData: [], //main区域展示的条件
    currentConditionTreeNode: null, // main区域当前点击的条件
    currentIndexTreeData: [], // main区域展示的树
    currentIndexTeeNode: null, // 当前点击的树
  },
  mutations: {
    SET_CURRENT_CONDITION_TREE_DATA: (state, val) => {
      state.currentConditionTreeData = val
    },
    SET_CONDITION_TREE_DATA: (state, val) => {
      state.conditionTreeData = val
    },
    SET_INDEX_TREE_DATA: (state, val) => {
      state.indexTreeData = val
    },
    ADD_CURRENT_TREE_DATA: (state, node) => {
      let findIndex = state.currentIndexTreeData.findIndex(item => item.vcCode === node.vcCode)
      if (findIndex === -1) {
        state.currentIndexTreeData.push(node)
      } else {
        Vue.set(state.currentIndexTreeData, findIndex, node) // 更新并触发响应式更新
      }
    },
    DEL_CURRENT_TREE_DATA: (state, delNode) => {
      let findIndex = state.currentIndexTreeData.findIndex(item => item.vcCode === delNode.vcCode)
      if (findIndex !== -1) {
        state.currentIndexTreeData.splice(findIndex, 1)
      }
    },
    SET_CURRENT_TREE_DATA: (state, array) => {
      state.currentIndexTreeData = array
    },
  },
  actions: {
    setCurrentConditionTreeData({commit}, val) {
      commit('SET_CURRENT_CONDITION_TREE_DATA', val)
    },
    setConditionTreeData({commit}, val) {
      commit('SET_CONDITION_TREE_DATA', val)
    },
    setIndexTreeData({commit}, val) {
      commit('SET_INDEX_TREE_DATA', val)
    },
    addCurrentTreeData({commit}, node) {
      commit('ADD_CURRENT_TREE_DATA', node)
    },
    delCurrentTreeData({commit}, index) {
      commit('DEL_CURRENT_TREE_DATA', index)
    },
    setCurrentTreeData({commit}, array) {
      commit('SET_CURRENT_TREE_DATA', array)
    },
  }
}

export default reportVM

import Vue from 'vue'
import Vuex from 'vuex'
import app from './modules/app'
import errorLog from './modules/errorLog'
import permission from './modules/permission'
import tagsView from './modules/tagsView'
import user from './modules/user'
import setting from './modules/setting'
import lock from './modules/loclwindows'
import edims from './modules/edims'
import getters from './getters'
import reportVM from './modules/reportVM'
import animation from './animation'
import compose from './compose'
import contextmenu from './contextmenu'
import copy from './copy'
import event from './event'
import layer from './layer'
import snapshot from './snapshot'
import lockReport from './lock'
import templateManageMent from '../api/templateManageMent'
import {renderScript} from '../utils/reportComponent'
// 注册vuex
Vue.use(Vuex)
// 状态 创建仓库
const store = new Vuex.Store({
  state: {
    ...animation.state,
    ...compose.state,
    ...contextmenu.state,
    ...copy.state,
    ...event.state,
    ...layer.state,
    ...snapshot.state,
    ...lockReport.state,
    ...reportVM.state,

    editMode: 'edit', // 编辑器模式 edit preview
    isEdit: false, // 判断是否是编辑模式
    canvasStyleData: {
      // 页面全局数据
      width: 595 * 2,
      height: 595 * 2 * 1.41,
      scale: 100,
      color: '#000',
      opacity: 1,
      background: '#fff',
      fontSize: 14,
    },
    isInEdiotr: false, // 是否在编辑器中，用于判断复制、粘贴组件时是否生效，如果在编辑器外，则无视这些操作
    componentData: [], // 画布组件数据 --- 当前活跃的
    componentDataArray: [], // 画布组件数据数组 --- 记录所有的页面
    globalImagComponenteArray: [],
    indexArray: [],// 指标数组
    compareIndexArray: [],//对比基准
    componentDataIndex: 0, // 当前活跃的页面
    canvasGlobalConfig: {}, // 画布全局的属性配置信息
    newReportConfig: {},// 新增模板的信息
    isEditor: false, // 是否是编辑模式
    pageMarginsOption: {
      leftMargin: 0,
      rightMargin: 0,
      topMargin: 0,
      bottomMargin: 0
    },// 画布全局的属性页边距
    curComponent: null,
    curComponentIndex: null,
    // 点击画布时是否点中组件，主要用于取消选中组件用。
    // 如果没点中组件，并且在画布空白处弹起鼠标，则取消当前组件的选中状态
    isClickComponent: false,
    templateData: [],
    btnData: [],
    meauList: [],
  },
  // 模块
  modules: {
    app,
    errorLog,
    permission,
    tagsView,
    user,
    setting,
    lock,
    edims,
    reportVM
  },
  mutations: {
    ...animation.mutations,
    ...compose.mutations,
    ...contextmenu.mutations,
    ...copy.mutations,
    ...event.mutations,
    ...layer.mutations,
    ...snapshot.mutations,
    ...lock.mutations,
    ...reportVM.mutations,
    ...edims.mutations,
    SET_GLOBAL_CONFIG(state, value) {
      state.canvasGlobalConfig = {...state.canvasGlobalConfig, ...value}
    },
    SET_INDEX_ARRAY(state, value) {
      state.indexArray = value
    },
    SET_COMPARE_INDEX_ARRAY(state, value) {
      state.compareIndexArray = value
    },
    SET_GLOBAL_IMAG_COMPONENT_ARRAY(state, {action, curComponent}) {
      if (action === 'add') {
        let index = state.globalImagComponenteArray.findIndex(item => item.id == curComponent.id)
        if (index == -1) {
          state.globalImagComponenteArray.push(curComponent)
        }
      } else {
        let index = state.globalImagComponenteArray.findIndex(item => item.id == curComponent.id)
        if (index !== -1) {
          state.globalImagComponenteArray.splice(index, -1)
        }
      }
    },
    SET_IS_EDITOR(state, value) {
      state.isEditor = value
    },
    SET_NEW_TEMPLATE_CONFIG(state, value) {
      state.newReportConfig = value
    },
    SET_PAGE_MARGIN_OPTION(state, value) {
      state.pageMarginsOption = value
    },
    // 新增画布数组
    addComponentDataArray(state) {
      state.componentDataArray.push([])
    },
    // 设置最新活跃页的下标
    setComponentDataIndex(state, value) {
      state.componentDataIndex = value
      state.componentData = []
      // 将当前的componentData设置为当前数组下标，要注意渲染
    },
    // 保存当前的componentData到对应的array位置
    saveComponentDataArrayByIndex(state) {
      state.componentDataArray[state.componentDataIndex] = state.componentData
    },
    deleteComponentDataArrayByIndex(state, index) {
      if (state.componentDataArray[index]) {
        state.componentDataArray.splice(index, 1)
      }
    },
    aceSetCanvasData(state, value) {
      state.canvasStyleData = value
    },
    setTemplateData(state, value) {
      state.templateData = value
    },
    aceSetcurComponent(state, value) {
      for (let i = 0; i < state.componentData.length; i++) {
        if (state.componentData[i].id === value.id) {
          state.componentData.splice(i, 1)
        }
      }
      state.componentData.push(value)
      state.curComponent = value
    },

    setClickComponentStatus(state, status) {
      state.isClickComponent = status
    },

    setEditMode(state, mode) {
      state.editMode = mode
    },

    setInEditorStatus(state, status) {
      state.isInEdiotr = status
    },

    setCanvasStyle(state, style) {
      state.canvasStyleData = style
    },

    setCurComponent(state, {component, index}) {
      state.curComponent = component
      state.curComponentIndex = index
    },

    setShapeStyle({curComponent}, {top, left, width, height, rotate, offsetLeft, offsetTop}) {
      if (top) curComponent.style.top = Math.round(top)
      if (left) curComponent.style.left = Math.round(left)
      if (width) curComponent.style.width = Math.round(width)
      if (height) curComponent.style.height = Math.round(height)
      if (rotate) curComponent.style.rotate = Math.round(rotate)
    },

    setShapeSingleStyle({curComponent}, {key, value}) {
      curComponent.style[key] = value
    },

    setComponentData(state, componentData = []) {
      Vue.set(state, 'componentData', componentData)
    },

    addComponent(state, {component, index}) {
      if (index !== undefined) {
        state.componentData.splice(index, 0, component)
      } else if (component.info.render.script && component.info.render.div) {
        state.componentData.push(component)
      } else {
        component.style.height = component.info.height || component.style.height
        component.style.width = component.info.width || component.style.width
        component.info.render = component.info.render.replaceAll('#uuid#', component.id)
        let script = component.info.render.match(/<script\b[^>]*>([\s\S]*?)<\/script>/gm)[0]
        const div = component.info.render.replace(script, '')
        script = script.replace(/<script\s+type="text\/javascript"\s*>/g, '')
        script = script.replace(/<\/script>/g, '')
        component.info.render = {
          div: div,
          script: script
        }
        state.componentData.push(component)
      }
      renderScript(component)
    },

    deleteComponent(state, index) {
      if (index === undefined) {
        index = state.curComponentIndex
      }

      if (index == state.curComponentIndex) {
        state.curComponentIndex = null
        state.curComponent = null
      }

      if (/\d/.test(index)) {
        state.componentData.splice(index, 1)
      }
    }
  },
  actions: {
    // 设置页边距
    setPageMarginsOptionValue(context, option) {
      context.commit('SET_PAGE_MARGIN_OPTION', option)
    },

    // 设置 指标数组
    setIndexArrayValue(context, array) {
      context.commit('SET_INDEX_ARRAY', array)
    },

    // 设置 对比指标数组
    setCompareIndexArrayValue(context, array) {
      context.commit('SET_COMPARE_INDEX_ARRAY', array)
    },

    // 异步调用渲染的逻辑
    addComponentAsync(context, {component: object}) {
      // 做判断 是否 需要增加 params属性
      // 对options的params里面做排序
      const compare = property => {
        return function (a, b) {
          var value1 = a[property]
          var value2 = b[property]
          return value1 - value2
        }
      }
      object.info.options.sort(compare('order'))
      // debugger
      if (object && object.info && !object.info.params) {
        const params = {}
        object.info.options.forEach(item => {
          item.show = true
          if (item.level == 3) {
            if (item.id == 'ZB_X_INTERVAL') {
              if (item.default == 'auto') {
                item.default = '自适应'
              }
            }
            if (item.id == 'ZB_INDEXWEIGHTA') {
              if (item.default == '') {
                item.default = 0
              }
            }
            if (item.id == 'ZB_INDEXWEIGHTB') {
              if (item.default == '') {
                item.default = 0
              }
            }
            params[item.id] = item.default
          }
          if (item.type == 'TP_IMG') {
            if (item.applayall === undefined) {
              item.applayall = false
            }
          }
        })
        Vue.set(object.info, 'params', params)
      }
      object.info.params = {
        ...object.info.params, ...{
          ZB_BEGINDATE: context.state.canvasGlobalConfig.ZB_BEGINDATE,
          ZB_ENDDATE: context.state.canvasGlobalConfig.ZB_ENDDATE,
          ZB_FUNDCODE: context.state.canvasGlobalConfig.ZB_FUNDCODE,
          ZB_FUNDNAME: context.state.canvasGlobalConfig.ZB_FUNDNAME,
          ZB_INDEXCODE: context.state.canvasGlobalConfig.ZB_INDEXCODE,
          ZB_INDEXTYPE: context.state.canvasGlobalConfig.ZB_INDEXTYPE,
          ZB_INDEXCODEA: context.state.canvasGlobalConfig.ZB_INDEXCODEA,
          ZB_INDEXWEIGHTA: context.state.canvasGlobalConfig.ZB_INDEXWEIGHTA,
          ZB_INDEXCODEB: context.state.canvasGlobalConfig.ZB_INDEXCODEB,
          ZB_INDEXWEIGHTB: context.state.canvasGlobalConfig.ZB_INDEXWEIGHTB,
        }
      }
      console.log(object)
      const params = {...object.info.params, ...context.state.canvasGlobalConfig}
      if (params.ZB_INDEXTYPE != 'zdyjz') {
        params.ZB_INDEXCODEA = params.ZB_INDEXCODE
        params.ZB_INDEXWEIGHTA = 100
        params.ZB_INDEXCODEB = '000300'
        params.ZB_INDEXWEIGHTB = 0
      }

      if (params.ZB_X_INTERVAL && params.ZB_X_INTERVAL == '自适应') {
        params.ZB_X_INTERVAL = 'auto'
      }
      params.moduleId = object.info.id
      // 如果有dropflag为true的话
      if (context.state.user.dropFlag) {
        Vue.prototype.$bus.$emit('homeload', true)
      }
      templateManageMent.render(params).then(res => {
        if (context.state.user.dropFlag) {
          Vue.prototype.$bus.$emit('homeload', false)
          context.commit('SET_DROPFLAG',false)
        }
        const {status, data} = res.data
        if (status === 200) {
          object.info.render = data
          context.commit('addComponent', {component: object})
        }
      }).catch(err => {
        if (context.state.user.dropFlag) {
          Vue.prototype.$bus.$emit('homeload', false)
          context.commit('SET_DROPFLAG',false)
        }
      })
    },

    // 重新渲染当前的活跃页
    refreshMap(context) {
      setTimeout(() => {
        for (let i = 0; i < context.state.componentDataArray[context.state.componentDataIndex].length; i++) {
          // 一个一个通过add方法加上去
          const temp = context.state.componentDataArray[context.state.componentDataIndex][i]
          context.commit('addComponent', {component: temp})
        }
      }, 0)
    },

    // 初始化画布
    initComponent(context, {componentDataArray}) {
      context.state.componentDataArray = componentDataArray || []
      context.state.componentData = []
      context.state.componentDataIndex = 0
    }
  },
  // 计算属性
  getters
})
// 暴露出去
export default store

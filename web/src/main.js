import Vue from 'vue'

import $ from 'jquery'
window.$ = $
import Cookies from 'js-cookie'
import * as myecharts from 'echarts'
import 'normalize.css/normalize.css' // A modern alternative to CSS resets
import Element from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import moment from 'moment'

import '@/styles/table-style.scss' //表格样式
// 字体图标
import './assets/iconfont/iconfont.css'
import '@/custom-component' // 注册自定义组件
// 引入pingfang字体
import './assets/font/font.css'

import App from './App'
import router from './router'
import store from './store' // 引入vuex里边的仓库
import '@/directive'
import colorArrs from '@/utils/colors'
import regularValidator from '@/utils/regular-validator'
import { hasMeauList, hasPermission } from './utils/index'

import i18n from './lang' // Internationalization
import './icons' // icon
import './errorLog' // error log
import './permission' // permission control
// import './mock' // simulation data
// 页面锁屏
import lockwindows from '@/utils/lockwindows'
import * as filters from './filters' // global filters
import commonfun from './filters/common.js' // global js
import validate from './utils/validate.js' // validate js
// ddportal-ui框架
import DdportalUI from '../ddportal-ui.common'
import '../ddportal-ui.css'
import 'xe-utils'
import VXETable from 'vxe-table'
// import VXETablePluginExportXLSX from 'vxe-table-plugin-export-xlsx'
import 'vxe-table/lib/index.css'
import '@/styles/vxetable-style.scss'
import '@/styles/index.scss' // global css

// 引入 font-awesome 字体图标库
import 'font-awesome/css/font-awesome.min.css'
// 引入渲染器筛选
import './components/Render/index'

// 打印插件
// import vuePrint from '@theshy/vue-print'
// Vue.use(vuePrint)
import Print from 'vue-print-nb'
import watermark from '@/directive/watermark'
import './utils/maxWindow'

import VueCompositionAPI from '@vue/composition-api'

Vue.use(VueCompositionAPI)
var echarts = myecharts

Element.Dialog.props.modalAppendToBody.default = false
Element.Drawer.props.modalAppendToBody.default = false

Vue.use(lockwindows)

Vue.prototype.$fun = commonfun

Vue.prototype.$validate = validate

Vue.prototype.$bus = new Vue() //组件间传值  this.$bus.$emit

Vue.prototype.$moment = moment
Vue.prototype.$colorArrs = colorArrs
Vue.prototype.$hasPermission = hasPermission
Vue.prototype.$hasMeauList = hasMeauList
Vue.prototype.$regularValidator = regularValidator
Vue.prototype.$echarts = myecharts

Vue.use(DdportalUI)

// import VXETablePluginElement from 'vxe-table-plugin-element'
// import 'vxe-table-plugin-element/dist/style.css'
// VXETable.use(VXETablePluginElement)
// VXETable.use(VXETablePluginExportXLSX)
Vue.use(VXETable)
VXETable.setup({
  keepSource: true
})

Vue.use(Print)

Vue.use(Element, {
  size: Cookies.get('size') || 'medium', // set element-ui default size
  i18n: (key, value) => i18n.t(key, value)
})

Vue.use(watermark)
var _ = require('lodash')

// register global utility filters.
Object.keys(filters).forEach((key) => {
  Vue.filter(key, filters[key])
})

import AutoEnterSearch from '@/directive/auto-enter-search'
Vue.directive('auto-enter', AutoEnterSearch)

Vue.config.productionTip = false
// 渲染挂载
new Vue({
  el: '#app',
  router,
  store,
  i18n,
  render: (h) => h(App)
})

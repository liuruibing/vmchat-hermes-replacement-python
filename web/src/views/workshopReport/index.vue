<template>
  <div class="home">
    <Toolbar
      :current-template="currentTemplate"
      :globalSettingConfig="globalSettingConfig"
      :global-config="isSingleFlag ? singleGlobalConfig : mutipleGlobalConfig"
      @changeshow="
        () => {
          this.$emit('changeshow')
        }
      "
    />

    <main :class="[$store.state.setting.fromPlatForm ? 'main-nest' : 'main']">
      <!-- 左侧组件列表 -->
      <section :style="{ height: height}" class="left">
        <ComponentList :chart-options="isSingleFlag ? singleChartOptions : mutipleChartOptions"/>
      </section>
      <!-- 中间画布 -->
      <section :style="{ height: centerHeight}" class="center">
        <div
          class="content"
          @dragover="handleDragOver"
          @drop="handleDrop"
          @mousedown="handleMouseDown"
          @mouseup="deselectCurComponent"
        >
            <Editor/>
        </div>
      </section>
      <!-- 右侧属性列表 -->
      <section :style="{ height: height}" class="right">
        <ComponentAttr v-if="curComponent"></ComponentAttr>
        <CanvasAttr v-else></CanvasAttr>
      </section>
    </main>
  </div>
</template>

<script>
import Editor from '@/components/Editor/index'
import ComponentList from '@/components/ComponentList' // 左侧列表组件
import AnimationList from '@/components/AnimationList' // 右侧动画列表
import EventList from '@/components/EventList' // 右侧事件列表
import componentList from '@/custom-component/component-list' // 左侧列表数据
import Toolbar from '@/components/Toolbar'
import {deepCopy} from '@/utils/utils'
import {mapState} from 'vuex'
import generateID from '@/utils/generateID'
import CanvasAttr from '@/components/CanvasAttr'
import {changeComponentSizeWithScale} from '@/utils/changeComponentsSizeWithScale'
import {setDefaultcomponentData} from '@/store/snapshot'
import ComponentAttr from '@/components/ComponentAttr'
import {merger} from '@/utils'

import pageApi from '@/api/templateManageMent/index'
import * as listenGlobalKeyDown from '@/utils/shortcutKey'

export default {
  components: {
    Editor,
    ComponentList,
    AnimationList,
    EventList,
    Toolbar,
    ComponentAttr,
    CanvasAttr
  },
  props: {
    globalSettingConfig: {
      type: Object,
      default: () => {}
    },
    isEdit: {
      type: Boolean,
      required: true,
      default: () => {
        return false
      }
    },
    currentTemplate: {
      type: Object,
      default: () => {
      }
    },
  },
  data() {
    return {
      activeName: 'attr',
      reSelectAnimateIndex: undefined,
      isSingleFlag: true, // true: 单产品，false: 多产品
      singleChartOptions: [],
      mutipleChartOptions: [],
      singleGlobalConfig: [],
      mutipleGlobalConfig: [],
      height: '0px',
      centerHeight: '0px'
    }
  },
  computed: mapState(['componentData', 'curComponent', 'isClickComponent', 'canvasStyleData', 'editor']),
  watch: {
    '$store.state.componentData': {
      handler() {
        // console.log(this.$store.state.componentData)
      },
      deep: true
    },
    isEdit: {
      handler() {
        if (isEdit == true) {
          // 编辑模式进来 需要merger
        } else {
          // 新建模板模式 不需要merger直接渲染
        }
      },
      deep: true
    },
  },
  created() {
    this.restore()
    // 全局监听按键事件
    listenGlobalKeyDown.listenGlobalKeyDown(this)
    this.getLeftCenterRightHeight()
    window.addEventListener('resize', this.getLeftCenterRightHeight);
  },
  mounted() {
    // this.handleSelectSingleComponents()
    // this.handleSelectMutipleComponents()
  },
  methods: {
    getLeftCenterRightHeight() {
      let height = document.getElementById('app').offsetHeight
      this.height = (height - 80 - 100 + (this.$store.state.setting.fromPlatForm ? 110 : 0)) + 'px'
      this.centerHeight = (height - 80 - 34 - 100 + (this.$store.state.setting.fromPlatForm ? 105 : 0)) + 'px'
    },

    // 处理单产品控件逻辑
    handleSelectSingleComponents(fundCode) {
      // 单产品组件
      const params = {}
      params.moduleType = 1
      params.fundCode = fundCode
      pageApi.selectCompotentList(params).then(res => {
        // 分解合并
        // 按照type类型 排序
        const {status, data} = res.data
        if (status === 200) {
          if (this.isEdit === false) {
            // 新增 - 不需要merge就用default默认值
            // console.log(this.globalSettingConfig)
            let tempArray = JSON.parse(data.publicAttr)
            for(let i = 0; i < tempArray.length; i++) {
              if(this.globalSettingConfig[tempArray[i].id]) {
                tempArray[i].default = this.globalSettingConfig[tempArray[i].id]
              }
            }
            this.singleGlobalConfig = tempArray
          } else {
            // 编辑 - merge（params）
          }

          const mergerData = merger(data.moduleInfo, 'moduleGroup')
          if (mergerData && mergerData.length && mergerData.length > 0) {
            const chartOptions = []
            mergerData.forEach(item => {
              const cr_module_info = []
              item.origin.forEach(sitem => {
                const obj = {}
                obj.vc_module_id = sitem.moduleId
                obj.vc_module_name = sitem.moduleName
                obj.vc_module_group = sitem.moduleGroup
                obj.vc_module_desc = sitem.moduleDesc
                obj.vc_element_config = JSON.parse(sitem.commonElementCfg)
                obj.icon = JSON.parse(sitem.elementConfig).icon
                obj.vc_element_config = [
                  ...JSON.parse(sitem.elementConfig).attribute,
                  ...obj.vc_element_config
                ]
                obj.vc_module_render = sitem.moduleRender
                obj.height = JSON.parse(sitem.elementConfig).height || ''
                obj.width = JSON.parse(sitem.elementConfig).width || ''
                cr_module_info.push(obj)
              })
              chartOptions.push({
                name: item.moduleGroup,
                id: item.moduleGroup,
                cr_module_info: cr_module_info
              })
            })
            this.singleChartOptions = chartOptions
            // this.chartOptions = chartOptions
          }
        }
      })
    },

    // 处理多产品控件逻辑
    handleSelectMutipleComponents() {
      const params2 = {}
      params2.moduleType = 2
      pageApi.selectCompotentList(params2).then(res => {
        // 分解合并
        // 按照type类型 排序
        const {status, data} = res.data
        if (status == 200) {
          this.mutipleGlobalConfig = JSON.parse(data.publicAttr)
          const mergerData = merger(data.moduleInfo, 'moduleGroup')
          if (mergerData && mergerData.length && mergerData.length > 0) {
            const chartOptions = []
            mergerData.forEach(item => {
              const cr_module_info = []
              item.origin.forEach(sitem => {
                const obj = {}
                obj.vc_module_id = sitem.moduleId
                obj.vc_module_name = sitem.moduleName
                obj.vc_module_group = sitem.moduleGroup
                obj.vc_module_desc = sitem.moduleDesc
                obj.vc_element_config = JSON.parse(sitem.elementConfig).attribute
                obj.icon = JSON.parse(sitem.elementConfig).icon
                obj.vc_module_render = sitem.moduleRender
                cr_module_info.push(obj)
              })
              chartOptions.push({
                name: item.moduleGroup,
                id: item.moduleGroup,
                cr_module_info: cr_module_info
              })
            })
            this.mutipleChartOptions = chartOptions
          }
        }
      })
    },

    restore() {
      // 用保存的数据恢复画布
      if (localStorage.getItem('canvasData')) {
        setDefaultcomponentData(JSON.parse(localStorage.getItem('canvasData')))
        this.$store.commit('setComponentData', JSON.parse(localStorage.getItem('canvasData')))
      }

      if (localStorage.getItem('canvasStyle')) {
        this.$store.commit('setCanvasStyle', JSON.parse(localStorage.getItem('canvasStyle')))
      }
    },

    handleDrop(e) {
      e.preventDefault()
      e.stopPropagation()
      const info = JSON.parse(e.dataTransfer.getData('info'))
      const rectInfo = this.editor.getBoundingClientRect()
      if (Object.keys(info).length > 0) {
        const component = deepCopy(componentList[0])
        component.style.top = e.clientY - rectInfo.y
        component.style.left = e.clientX - rectInfo.x
        component.id = generateID()
        component.info = info
        // 根据画面比例修改组件样式比例 https://github.com/woai3c/visual-drag-demo/issues/91
        changeComponentSizeWithScale(component)
        this.$store.commit('SET_DROPFLAG',true)
        this.$store.dispatch('addComponentAsync', {component})
        // this.$store.commit("addComponent", { component });
        this.$store.commit('recordSnapshot')

        // 触发选中
        this.$store.commit('setClickComponentStatus', true)
        this.$store.commit('setCurComponent', {component: component})
        // 隐藏右击显示的菜单
        this.$store.commit('hideContextMenu')
      }
    },

    handleDragOver(e) {
      e.preventDefault()
      e.dataTransfer.dropEffect = 'copy'
    },

    handleMouseDown(e) {
      e.stopPropagation()
      this.$store.commit('setClickComponentStatus', false)
      this.$store.commit('setInEditorStatus', true)
    },

    deselectCurComponent(e) {
      const curComponent = this.curComponent
      if (curComponent) {
        const rootDiv = document.querySelector(`#component${curComponent.id}`)
        var deleteJs = document.getElementById(`script_${curComponent.id}`)
        deleteJs && deleteJs.remove()

        const newScript = document.createElement('script')
        newScript.type = 'text/javascript'
        newScript.id = `script_${curComponent.id}`
        newScript.innerHTML = curComponent.info.render.script

        setTimeout(() => {
          rootDiv.appendChild(newScript)
        }, 200)
      }

      if (!this.isClickComponent) {
        this.$store.commit('setCurComponent', {component: null, index: null})
      }
      // 0 左击 1 滚轮 2 右击
      if (e.button != 2) {
        this.$store.commit('hideContextMenu')
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.home {
  background-color: #f3f5fb;

  .main{
    height: calc(100% - 150px);
  }
  .main-nest{
    height: calc(100% - 10px);
  }
  main {
    padding: 2px 10px 10px 10px;
    position: relative;

    .left {
      position: absolute;
      background-color: #ffffff;
      height: 97.8%;
      width: 300px;
      left: 10px;
      top: 10px;
      margin-bottom: 10px;
      //border: 2px solid #5d5d5d;

      & > div {
        overflow: auto;
      }
    }

    .right {
      position: absolute;
      background-color: #ffffff;
      height: 97.8%;
      width: 250px;
      right: 10px;
      top: 10px;

      .el-select {
        width: 100%;
      }
    }

    .center {
      // 310 + 260
      width: calc(100% - 570px);
      margin-top: 46px;
      margin-left: 310px;
      margin-right: 260px;
      background: #ffffff;
      height: 100%;
      overflow: auto;
      padding: 20px;
      padding-top: 0px;
      border: 2px solid #cccccc;

      .content {
        width: 100%;
        height: 100%;
        overflow: auto;
      }
    }
  }

  .placeholder {
    text-align: center;
    color: #333;
  }

  .global-attr {
    padding: 10px;
  }
}
</style>

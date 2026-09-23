<template>
  <div style="position: relative">
    <div
      :style="{
        width: tabWidth
      }"
      :class="[$store.state.setting.fromPlatForm ? 'el-tab-editor-nest' : 'el-tab-editor']"
    >
      <el-tabs class="editor" v-model="editableTabsValue" editable style="display: inline-block" type="card" @edit="handleTabsEdit" @tab-click="handleTabClick">
        <el-tab-pane v-for="(item, index) in editableTabs" :key="item.name" :label="item.title" :name="item.name" />
      </el-tabs>
    </div>
    <div
      id="templateEditor"
      :style="{
        display: 'inline-block',
        background: '#fff',
        marginTop: '-24px',
        borderLeft: `${pageMarginsOption.leftMargin}px solid #ffffff`,
        borderRight: `${pageMarginsOption.rightMargin}px solid #ffffff`,
        borderTop: `${pageMarginsOption.topMargin}px solid #ffffff`,
        borderBottom: `${pageMarginsOption.bottomMargin}px solid #ffffff`
      }"
    >
      <div
        id="editor"
        :class="{ edit: isEdit }"
        :style="{
          ...getCanvasStyle(canvasStyleData),
          width: changeStyleWithScale(canvasStyleData.width) + 'px',
          height: changeStyleWithScale(canvasStyleData.height) + 'px',
          position: 'relative',
          background: '#fff'
        }"
        class="editor"
        @contextmenu="handleContextMenu"
        @mousedown="handleMouseDown"
      >
        <div class="editor-divider">
          <el-divider></el-divider>
        </div>
        <div style="position: absolute;right: 20px;}">{{ pageNum }}</div>
        <!--      <div class="template-header"></div>-->
        <!-- <div class="template-footer"></div> -->
        <!-- 网格线 -->
        <!--    <Grid />-->

        <!--页面组件列表展示-->
        <Shape
          v-for="(item, index) in componentData"
          :key="item.id"
          :active="item.id === (curComponent || {}).id"
          :class="{ lock: item.isLock }"
          :default-style="item.style"
          :element="item"
          :index="index"
          :style="getShapeStyle(item.style)"
          style="box-sizing: content-box"
        >
          <component
            :is="item.component"
            v-if="item.component.startsWith('SVG')"
            :id="'component' + item.id"
            :element="item"
            :prop-value="item.propValue"
            :request="item.request"
            :style="getSVGStyle(item.style)"
            class="component"
          />

          <component
            :is="item.component"
            v-else-if="item.component != 'VText'"
            :id="'component' + item.id"
            :element="item"
            :prop-value="item.propValue"
            :request="item.request"
            :style="getComponentStyle(item.style)"
            class="component"
          />

          <component
            :is="item.component"
            v-else
            :id="'component' + item.id"
            :element="item"
            :prop-value="item.propValue"
            :request="item.request"
            :style="getComponentStyle(item.style)"
            class="component"
            @input="handleInput"
          />
        </Shape>
        <!-- 右击菜单 -->
        <ContextMenu />
        <!-- 标线 -->
        <MarkLine />
        <!-- 选中区域 -->
        <Area v-show="isShowArea" :height="height" :start="start" :width="width" />
      </div>
    </div>
    <!-- <div
      :style="{
        width: changeStyleWithScale(canvasStyleData.width) + 'px',
        height: changeStyleWithScale(canvasStyleData.height) + 'px'
      }"
      style="position: absolute;z-index: 1000 !important;width: 100%;height:100%;background-color: antiquewhite;top: 0px;left: 0px;text-align: center;vertical-align: middle;"
    >
      <span>导出中</span>
    </div> -->
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Shape from './Shape'
import { getCanvasStyle, getComponentRotatedStyle, getShapeStyle, getStyle, getSVGStyle } from '@/utils/style'
import { $, isPreventDrop } from '@/utils/utils'
import ContextMenu from './ContextMenu'
import MarkLine from './MarkLine'
import Area from './Area'
import eventBus from '@/utils/eventBus'
import Grid from './Grid'
import { changeStyleWithScale } from '@/utils/translate'

export default {
  components: { Shape, ContextMenu, MarkLine, Area, Grid },
  props: {
    isEdit: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      editableTabs: [
        {
          name: '1',
          title: '第1页'
        }
      ],
      tabWidth: '0px',
      tabIndex: '1',
      editableTabsValue: '1',
      editorX: 0,
      editorY: 0,
      start: {
        // 选中区域的起点
        x: 0,
        y: 0
      },
      width: 0,
      height: 0,
      isShowArea: false,
      svgFilterAttrs: ['width', 'height', 'top', 'left', 'rotate']
    }
  },
  computed: {
    ...mapState(['componentData', 'curComponent', 'canvasStyleData', 'editor', 'pageMarginsOption']),
    pageNum() {
      let pageStr = `第${Number(this.$store.state.componentDataIndex) + 1}页（共${this.$store.state.componentDataArray.length}页）`
      return pageStr
    }
  },
  created() {
    this.getTabWidth()
    window.addEventListener('resize', this.getTabWidth)
  },
  mounted() {
    console.log('enter............................')
    this.$bus.$on('initpag', this.initPag)
    // 获取编辑器元素
    this.$store.commit('getEditor')

    eventBus.$on('hideArea', () => {
      this.hideArea()
    })
  },
  methods: {
    getShapeStyle,
    getCanvasStyle,
    changeStyleWithScale,

    getTabWidth() {
      let mainWidth = document.getElementById('app').offsetWidth
      this.tabWidth = mainWidth - 540 + (this.$store.state.setting.fromPlatForm ? 36 : 0) + 'px'
    },

    // 初始化画布的分页
    initPag(editableLength) {
      console.log('editableLength', editableLength)
      let temp = []
      for (let i = 0; i < editableLength; i++) {
        let obj = {
          name: '' + (i + 1),
          title: `第${i + 1}页`
        }
        temp.push(obj)
      }
      this.editableTabs = temp
      this.tabIndex = editableLength
      this.editableTabsValue = '1'
    },

    handleTabClick({ index }) {
      // 保存当前页面的所有内容
      this.$store.commit('saveComponentDataArrayByIndex')
      // 设置当前的活跃下标
      this.$store.commit('setComponentDataIndex', index)
      this.$store.dispatch('refreshMap')
    },
    handleTabsEdit(targetName, action) {
      if (action === 'add') {
        const newTabName = ++this.tabIndex + ''
        this.editableTabs.push({
          title: `第${this.tabIndex}页`,
          name: newTabName
        })
        this.editableTabsValue = newTabName
        // 保存当前页面的所有内容
        this.$store.commit('saveComponentDataArrayByIndex')
        // 新增一个画布页
        // 全局的画布数组新增一个空数组
        this.$store.commit('addComponentDataArray')
        // 把当前的活跃的页面的设置为当前活跃数组下标对应值
        this.$store.commit('setComponentDataIndex', this.editableTabs.length - 1)
      }
      if (action === 'remove') {
        if (this.editableTabs.length <= 1) {
          this.$message.closeAll()
          this.$message.warning('删除失败')
          return
        }
        const tabs = this.editableTabs
        let activeName = this.editableTabsValue
        if (activeName === targetName) {
          tabs.forEach((tab, index) => {
            if (tab.name === targetName) {
              const nextTab = tabs[index + 1] || tabs[index - 1]
              if (nextTab) {
                activeName = nextTab.name
              }
            }
          })
        }

        // 找到需要删除的 标签下标
        let activeIndex = this.editableTabs.findIndex((item) => item.name == targetName)
        this.editableTabsValue = activeName
        this.editableTabs = tabs.filter((tab) => tab.name !== targetName)
        for (let i = 0; i < this.editableTabs.length; i++) {
          const temp = this.editableTabs[i]
          temp.name = '' + (i + 1)
          temp.title = `第${i + 1}页`
        }
        this.tabIndex = this.editableTabs.length
        this.editableTabsValue = '1'

        if (activeIndex || activeIndex == 0) {
          // 如果下标存在
          // 保存当前页
          this.$store.commit('saveComponentDataArrayByIndex')

          // 删除当前的下标的 componentDataArray数组
          this.$store.commit('deleteComponentDataArrayByIndex', activeIndex)
          // 切换到第一页
          this.$store.commit('setComponentDataIndex', 0)
          this.$store.dispatch('refreshMap')
        }
      }
    },
    handleMouseDown(e) {
      // 如果没有选中组件 在画布上点击时需要调用 e.preventDefault() 防止触发 drop 事件
      if (!this.curComponent || isPreventDrop(this.curComponent.component)) {
        e.preventDefault()
      }

      this.hideArea()

      // 获取编辑器的位移信息，每次点击时都需要获取一次。主要是为了方便开发时调试用。
      const rectInfo = this.editor.getBoundingClientRect()
      this.editorX = rectInfo.x
      this.editorY = rectInfo.y

      const startX = e.clientX
      const startY = e.clientY
      this.start.x = startX - this.editorX
      this.start.y = startY - this.editorY
      // 展示选中区域
      this.isShowArea = true

      const move = (moveEvent) => {
        this.width = Math.abs(moveEvent.clientX - startX)
        this.height = Math.abs(moveEvent.clientY - startY)
        if (moveEvent.clientX < startX) {
          this.start.x = moveEvent.clientX - this.editorX
        }

        if (moveEvent.clientY < startY) {
          this.start.y = moveEvent.clientY - this.editorY
        }
      }

      const up = (e) => {
        document.removeEventListener('mousemove', move)
        document.removeEventListener('mouseup', up)

        if (e.clientX == startX && e.clientY == startY) {
          this.hideArea()
          return
        }

        this.createGroup()
      }

      document.addEventListener('mousemove', move)
      document.addEventListener('mouseup', up)
    },

    hideArea() {
      this.isShowArea = 0
      this.width = 0
      this.height = 0

      this.$store.commit('setAreaData', {
        style: {
          left: 0,
          top: 0,
          width: 0,
          height: 0
        },
        components: []
      })
    },

    createGroup() {
      // 获取选中区域的组件数据
      const areaData = this.getSelectArea()
      if (areaData.length <= 1) {
        this.hideArea()
        return
      }

      // 根据选中区域和区域中每个组件的位移信息来创建 Group 组件
      // 要遍历选择区域的每个组件，获取它们的 left top right bottom 信息来进行比较
      let top = Infinity,
        left = Infinity
      let right = -Infinity,
        bottom = -Infinity
      areaData.forEach((component) => {
        let style = {}
        if (component.component == 'Group') {
          component.propValue.forEach((item) => {
            const rectInfo = $(`#component${item.id}`).getBoundingClientRect()
            style.left = rectInfo.left - this.editorX
            style.top = rectInfo.top - this.editorY
            style.right = rectInfo.right - this.editorX
            style.bottom = rectInfo.bottom - this.editorY

            if (style.left < left) left = style.left
            if (style.top < top) top = style.top
            if (style.right > right) right = style.right
            if (style.bottom > bottom) bottom = style.bottom
          })
        } else {
          style = getComponentRotatedStyle(component.style)
        }

        if (style.left < left) left = style.left
        if (style.top < top) top = style.top
        if (style.right > right) right = style.right
        if (style.bottom > bottom) bottom = style.bottom
      })

      this.start.x = left
      this.start.y = top
      this.width = right - left
      this.height = bottom - top

      // 设置选中区域位移大小信息和区域内的组件数据
      this.$store.commit('setAreaData', {
        style: {
          left,
          top,
          width: this.width,
          height: this.height
        },
        components: areaData
      })
    },

    getSelectArea() {
      const result = []
      // 区域起点坐标
      const { x, y } = this.start
      // 计算所有的组件数据，判断是否在选中区域内
      this.componentData.forEach((component) => {
        if (component.isLock) return

        const { left, top, width, height } = getComponentRotatedStyle(component.style)
        if (x <= left && y <= top && left + width <= x + this.width && top + height <= y + this.height) {
          result.push(component)
        }
      })

      // 返回在选中区域内的所有组件
      return result
    },

    handleContextMenu(e) {
      e.stopPropagation()
      e.preventDefault()
      // 计算菜单相对于编辑器的位移
      const target = e.target
      const top = e.clientY
      const left = e.clientX
      // while (target instanceof SVGElement) {
      //   target = target.parentNode;
      // }

      // while (!target.className.includes("editor")) {
      //   left += target.offsetLeft;
      //   top += target.offsetTop;
      //   target = target.parentNode;
      // }
      this.$store.commit('showContextMenu', { top, left })
    },

    getComponentStyle(style) {
      return getStyle(style, this.svgFilterAttrs)
    },

    getSVGStyle(style) {
      return getSVGStyle(style, this.svgFilterAttrs)
    },

    handleInput(element, value) {
      // 根据文本组件高度调整 shape 高度
      this.$store.commit('setShapeStyle', {
        height: this.getTextareaHeight(element, value)
      })
    },

    getTextareaHeight(element, text) {
      let { lineHeight, fontSize, height } = element.style
      if (lineHeight === '') {
        lineHeight = 1.5
      }

      const newHeight = (text.split('<br>').length - 1) * lineHeight * (fontSize || this.canvasStyleData.fontSize)
      return height > newHeight ? height : newHeight
    }
  }
}
</script>

<style lang="scss" scoped>
.clearfix {
  clear: both;
}
.el-tab-editor {
  background-color: #e6e8f0;
  position: fixed;
  top: 150px;
  left: 320px;
  height: 40px !important;
  overflow: hidden;
}
.el-tab-editor-nest {
  background-color: #cccccc;
  position: fixed;
  top: 55px;
  left: 271px;
  height: 40px !important;
  overflow: hidden;
}
::v-deep .el-tabs__item {
  //background-color: #4f4f4f;
  background-color: #e6e8f0;
  color: #787879 !important;
  height: 40px !important;
  line-height: 40px !important;
  border: 1px solid #cccccc;
}

::v-deep .el-tabs__new-tab {
  height: 40px;
  width: 40px;
  background-color: #e6e8f0;
  color: #787879 !important;
  border: 1px solid #cccccc;
  margin: 0px;
  padding-top: 10px;;
}

::v-deep .el-tabs__header .el-tabs__nav {
  border: 1px solid #cccccc;
}

::v-deep .el-tabs__header .el-tabs__item {
  border-left: 1px solid #cccccc;
}

::v-deep .el-tabs__item.is-active {
  color: #3b3b3b !important;
  background-color: #f4f5fb;
  border: 1px solid #f4f5fb !important;
}

.editor-page-num {
  position: absolute;
  right: 20px;
}

.editor-divider {
  position: relative;
  top: 60px;
  width: calc(100% - 40px);
  margin-left: 20px;
  margin-right: 20px;
}

.template-header {
  position: absolute;
  background-color: green;
  height: 60px;
  width: 100%;
  top: 0;
}

.template-footer {
  position: absolute;
  background-color: greenyellow;
  height: 50px;
  width: 100%;
  bottom: 0;
}

.editor {
  position: relative;
  // background: #fff;

  .lock {
    opacity: 0.5;

    &:hover {
      cursor: not-allowed;
    }
  }
}

.edit {
  .component {
    //outline: none;
    width: 100%;
    height: 100%;
  }
}
</style>

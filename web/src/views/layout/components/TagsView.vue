<template>
  <div class="tags-view-container">
    <div class="tags-view-content">
      <scroll-pane ref="scrollPane" class="tags-view-wrapper">
        <span
          v-for="(tag, index) in visitedViews"
          ref="tag"
          :class="{
            active: isActive(tag),
            dragging: draggedIndex === index,
            'drag-over': dragOverIndex === index && draggedIndex !== index
          }"
          :key="tag.path"
          class="tags-view-item"
          draggable="true"
          @click="handleTagClick(tag)"
          @click.middle="closeSelectedTag(tag)"
          @contextmenu.prevent="openMenu(tag, $event)"
          @dragstart="onDragStart($event, index)"
          @dragover.prevent="onDragOver($event, index)"
          @dragleave="onDragLeave(index)"
          @dragend="onDragEnd($event)"
          @drop.prevent="onDrop($event, index)"
        >
          {{ generateTitle(tag.title) }}
          <span class="el-icon-close" @click.prevent.stop="closeSelectedTag(tag)" />
        </span>
      </scroll-pane>
      <menu-search class="menu-search-wrapper"></menu-search>
    </div>

    <ul v-show="visible" :style="{ left: left + 'px', top: top + 'px' }" class="contextmenu">
      <!-- <li @click="refreshSelectedTag(selectedTag)">{{ $t('tagsView.refresh') }}</li> -->
      <li @click="closeSelectedTag(selectedTag)">{{ $t('tagsView.close') }}</li>
      <li @click="closeOthersTags">{{ $t('tagsView.closeOthers') }}</li>
      <li @click="closeAllTags">{{ $t('tagsView.closeAll') }}</li>
    </ul>
  </div>
</template>

<script>
import ScrollPane from '@/components/ScrollPane'
import { generateTitle } from '@/utils/i18n'
import { mapGetters } from 'vuex'
import Hamburger from '@/components/Hamburger'
import MenuSearch from './menuDropDown/MenuSearch.vue'

export default {
  components: {
    ScrollPane,
    Hamburger,
    MenuSearch
  },
  data() {
    return {
      visible: false,
      top: 0,
      left: 0,
      selectedTag: {},
      draggedIndex: null,
      dragOverIndex: null
    }
  },
  computed: {
    closedapin() {
      return this.$store.state.app.closedapin
    },
    visitedViews() {
      return this.$store.state.tagsView.visitedViews
    },
    ...mapGetters(['sidebar', 'name', 'avatar', 'device'])
  },
  watch: {
    $route() {
      this.addViewTags()
      this.moveToCurrentTag()
    },
    visible(value) {
      if (value) {
        document.body.addEventListener('click', this.closeMenu)
      } else {
        document.body.removeEventListener('click', this.closeMenu)
      }
    },
    closedapin(value) {
      if (value) {
        this.$store.dispatch('setClosedapin', false)
        let view = this.visitedViews.filter((ele) => {
          if (ele.path === '/yygl/ShowDapin') {
            return ele
          }
          // 关闭大屏时
          if (ele.path === '/yygl/jkpt') {
            return ele
          }
          if (ele.path === '/yygl/yygzt') {
            return ele
          }
        })
        this.closeSelectedTag(view[0])
      }
    }
  },
  mounted() {
    this.addViewTags()
  },
  // sun 2021-07-29
  beforeDestroy() {
    // 清理document.body上的事件监听器
    if (this.visible) {
      document.body.removeEventListener('click', this.closeMenu)
    }
    // 只清理当前组件相关的事件监听器
    this.$bus.$off('removeCache')
  },
  methods: {
    toggleSideBar() {
      this.$store.dispatch('toggleSideBar')
    },
    generateTitle, // generateTitle by vue-i18n
    isActive(route) {
      return route.path === this.$route.path
    },
    addViewTags() {
      const { name } = this.$route
      if (name) {
        this.$store.dispatch('addView', this.$route)
      }
      return false
    },
    moveToCurrentTag() {
      const tags = this.$refs.tag
      if (!tags) {
        return
      }
      this.$nextTick(() => {
        for (let i = 0; i < tags.length; i++) {
          const tag = tags[i]
          const visitedView = this.visitedViews[i]
          if (visitedView && visitedView.path === this.$route.path) {
            this.$refs.scrollPane.moveToTarget(tag)
            // when query is different then update
            if (visitedView.fullPath !== this.$route.fullPath) {
              this.$store.dispatch('updateVisitedView', this.$route)
            }
            break
          }
        }
      })
    },
    refreshSelectedTag(view) {
      this.$store.dispatch('delCachedView', view).then(() => {
        const { fullPath } = view
        this.$nextTick(() => {
          this.$router.replace({
            path: '/redirect' + fullPath
          })
        })
      })
    },
    closeSelectedTag(view) {
      this.$store.dispatch('delView', view).then(({ visitedViews }) => {
        if (this.isActive(view)) {
          const latestView = visitedViews.slice(-1)[0]
          if (latestView) {
            this.$router.push(latestView)
          } else {
            this.$router.push('/dashboard')
          }
        }
        this.$bus.$emit('removeCache', 'closeSelectedTag', view) //sun 2021-07-29
      })
    },
    closeOthersTags() {
      this.$router.push(this.selectedTag)
      this.$bus.$emit('removeCache', 'closeOthersTags', this.selectedTag) //sun 2021-07-29
      this.$store.dispatch('delOthersViews', this.selectedTag).then(() => {
        this.moveToCurrentTag()
      })
    },
    closeAllTags() {
      // sun 2021-07-29
      this.$store.dispatch('delAllViews').then(({ visitedViews }) => {
        // 关闭所有标签后，导航到最后一个可用视图或默认页面
        if (visitedViews && visitedViews.length > 0) {
          const latestView = visitedViews.slice(-1)[0]
          this.$router.push(latestView)
        } else {
          this.$router.push('/dashboard')
        }
        this.$bus.$emit('removeCache', 'closeAllTags')
      }).catch(() => {
        // 如果store action失败，仍然导航到默认页面
        this.$router.push('/dashboard')
      })
    },
    openMenu(tag, e) {
      const menuMinWidth = 105
      const offsetLeft = this.$el.getBoundingClientRect().left // container margin left
      const offsetWidth = this.$el.offsetWidth // container width
      const maxLeft = offsetWidth - menuMinWidth // left boundary
      const left = e.clientX - offsetLeft + 15 // 15: margin right

      if (left > maxLeft) {
        this.left = maxLeft
      } else {
        this.left = left
      }
      this.top = e.clientY - 50

      this.visible = true
      this.selectedTag = tag
    },
    closeMenu() {
      this.visible = false
    },

    // 导航到标签页
    navigateToTag(tag) {
      if (this.$route.path !== tag.path) {
        this.$router.push({ path: tag.path, query: tag.query })
      }
    },

    // 处理标签点击
    handleTagClick(tag) {
      // 如果正在拖拽，不执行导航
      if (this.draggedIndex !== null) {
        return
      }
      this.navigateToTag(tag)
    },

    // 拖拽开始
    onDragStart(event, index) {
      this.draggedIndex = index
      event.dataTransfer.effectAllowed = 'move'
      event.dataTransfer.setData('text/plain', index.toString())
    },

    // 拖拽经过
    onDragOver(event, index) {
      event.preventDefault()
      event.dataTransfer.dropEffect = 'move'

      // 设置拖拽悬停的目标索引
      if (this.draggedIndex !== null && this.draggedIndex !== index) {
        this.dragOverIndex = index
      }
    },

    // 拖拽离开
    onDragLeave(index) {
      // 清除拖拽悬停状态
      if (this.dragOverIndex === index) {
        this.dragOverIndex = null
      }
    },

    // 拖拽放置
    onDrop(event, targetIndex) {
      event.preventDefault()

      if (this.draggedIndex === null || this.draggedIndex === targetIndex) {
        this.draggedIndex = null
        return
      }

      // 获取当前的标签数组
      const visitedViews = [...this.visitedViews]

      // 移动标签
      const draggedItem = visitedViews.splice(this.draggedIndex, 1)[0]
      visitedViews.splice(targetIndex, 0, draggedItem)

      // 更新 store 中的标签顺序
      this.$store.dispatch('reorderVisitedViews', visitedViews)

      // 重置拖拽状态
      this.draggedIndex = null
      this.dragOverIndex = null
    },

    // 拖拽结束
    onDragEnd() {
      // 重置拖拽状态
      this.draggedIndex = null
      this.dragOverIndex = null
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.tags-view-container {
  border-top: 0.5px solid #4678a2;
  height: 34px;
  width: 100%;
  position: fixed;
  z-index: 1000;
  top: 58px;
  left: 0px;
  padding-left: 10px;
  // width: 100%;
  //background: #242836;
  background-image: url('../../../assets/img/gfdashboardimg2.png');
  background-size: 100% 100%;
  background-repeat: no-repeat;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.12), 0 0 3px 0 rgba(0, 0, 0, 0.04);
  .tags-view-content {
    display: flex;
    align-items: center;
    height: 100%;
    width: 100%;
  }

  .tags-view-wrapper {
    flex: 1;
    overflow: hidden;
    padding: 0 30px 0 40px;

    .tags-view-item {
      display: inline-block;
      position: relative;
      cursor: pointer;
      height: 28px;
      line-height: 28px;
      //background: #F9FAFE;
      background-color: rgba(255, 255, 255, 0.7);
      border: 1px solid #000;
      border-radius: 4px;
      color: #000;
      padding: 0 8px;
      font-size: 14px;
      margin-left: 5px;
      margin-top: 4px;
      &:first-of-type {
        margin-left: 20px;
      }
      &:last-of-type {
        margin-right: 20px;
      }
      &.active {
        //background-color: #3598dc;
        background-color: #fff;
        //color: #612d10;
        // background-image: linear-gradient(90deg, #fbe4cf, #eac4a1);
        border-color: #fff;
        //border-color: #3598dc;
        // border-color: #804f2b;
      }
            // 拖拽相关样式
      &[draggable="true"] {
        cursor: move;
        user-select: none;
        transition: all 0.3s ease;

        &:hover {
          opacity: 0.8;
        }
      }

      // 正在被拖拽的标签样式
      &.dragging {
        opacity: 0.5;
        transform: scale(0.95);
        background: linear-gradient(to right, #f5d7bc, #e0b794) !important;
        color: #000;
        box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4);
        border: 2px solid #fff;
        z-index: 1000;
        position: relative;
      }

      // 拖拽目标位置的高亮样式
      &.drag-over {
        background: linear-gradient(to right, #ddb592, #cb9b72) !important;
        color: #000;
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(245, 108, 108, 0.4);
        border: 2px dashed #fff;
        animation: pulse 1s infinite;
      }

      &:active {
        opacity: 0.6;
      }
    }
  }

  .menu-search-wrapper {
    margin-right: 20px;
    margin-top: 2px;
    z-index: 1001;
  }

  @keyframes pulse {
    0% {
      box-shadow: 0 4px 12px rgba(245, 108, 108, 0.4);
    }
    50% {
      box-shadow: 0 6px 20px rgba(245, 108, 108, 0.8);
    }
    100% {
      box-shadow: 0 4px 12px rgba(245, 108, 108, 0.4);
    }
  }

  .contextmenu {
    margin: 0;
    background: #fff;
    z-index: 10000;
    position: absolute;
    list-style-type: none;
    padding: 5px 0;
    border-radius: 4px;
    font-size: 14px;
    font-weight: 400;
    color: #333;
    box-shadow: 2px 2px 3px 0 rgba(0, 0, 0, 0.3);
    li {
      margin: 0;
      padding: 7px 16px;
      cursor: pointer;
      &:hover {
        background: #eee;
      }
    }
  }
}
</style>

<style rel="stylesheet/scss" lang="scss">
#scrollPane .el-button--small,
.el-button--small.is-round {
  padding: 8px !important;
}
//reset element css of el-icon-close
.tags-view-wrapper {
  .tags-view-item {
    .el-icon-close {
      width: 16px;
      height: 16px;
      vertical-align: 2px;
      border-radius: 50%;
      text-align: center;
      transition: all 0.3s cubic-bezier(0.645, 0.045, 0.355, 1);
      transform-origin: 100% 50%;
      &:before {
        transform: scale(0.6);
        display: inline-block;
        vertical-align: -1px;
      }
      &:hover {
        background-color: #b4bccc;
        color: #fff;
      }
    }
  }
}
</style>

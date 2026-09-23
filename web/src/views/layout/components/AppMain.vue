<template>
  <div :class="getClassName(0)">
    <section id="appMain" :class="getClassName(1)">
      <!--其中transition 定义了页面之间切换动画，可以根据自己的需求，自行修改转场动画-->
      <!--<transition name="fade-transform" mode="out-in">-->
      <!--app-main 外部包了一层 keep-alive 主要是为了缓存 <router-view> 的，配合页面的 tabs-view 标签导航使用，如不需要可自行去除-->
      <!--:include="visitedViews " 名字不对应 删除全部缓存-->
      <keep-alive>
        <!--我创建和编辑的页面使用的是同一个 component，默认情况下当这两个页面切换时并不会触发 vue 的 created 或者 mounted 钩子，官方说你可以通过 watch $route 的变化来做处理，来保证路由切换时都会重新渲染触发钩子了-->
        <router-view :key="key" />
      </keep-alive>
      <component v-for="item in componentsArray" :class="$route.path == item.path ? 'show-iframe' : 'unshow-iframe'" :key="item.name" :is="item.name" :ref="item.name"></component>
      <!-- 新增底部文字 -->
      <div class="content-footer">
        <p class="footer-text">{{ $store.state.setting.footerText }}</p>
      </div>
      <!--</transition>-->
    </section>
  </div>
</template>

<script>
import smcpxx from '@/views/multiProductDetail/index'
import dcpfx from '@/views/singleProduct/index'
import csbg from '@/views/performanceReport/csbg/index'
import qyljxbg from '@/views/performanceReport/qyljxbg/index'
import zqljxbg from '@/views/performanceReport/zqljxbg/index'
import ctajxbg from '@/views/performanceReport/ctajxbg/index'
import jxjb from '@/views/performanceReport/jxjb/index'
import fofjxbg from '@/views/performanceReport/fofjxbg/index'
import sycpbg from '@/views/performanceReport/sycpbg/index'

import gmzl from '@/views/performanceReportZJ/gmzl/index'
import dwjzbxzl from '@/views/performanceReportZJ/dwjzbxzl/index'
import syfx from '@/views/performanceReportZJ/syfx/index'
import rsybx from '@/views/performanceReportZJ/rsybx/index'
import lhzbfx from '@/views/performanceReportZJ/lhzbfx/index'
import dlzcccsx from '@/views/performanceReportZJ/dlzcccsx/index'
import qyljckzbsxt from '@/views/performanceReportZJ/qyljckzbsxt/index'
import qmccfx from '@/views/performanceReportZJ/qmccfx/index'
import cghyfx from '@/views/performanceReportZJ/cghyfx/index'
import zqpzpzsx from '@/views/performanceReportZJ/zqpzpzsx/index'
import xypjfbsx from '@/views/performanceReportZJ/xypjfbsx/index'
import zhjqbdsx from '@/views/performanceReportZJ/zhjqbdsx/index'
import syqxpzsx from '@/views/performanceReportZJ/syqxpzsx/index'
import spqhdtccqk from '@/views/performanceReportZJ/spqhdtccqk/index'
import dlzcjxgy from '@/views/performanceReportZJ/dlzcjxgy/index'
import gpflgy from '@/views/performanceReportZJ/gpflgy/index'
import zqgyfx from '@/views/performanceReportZJ/zqgyfx/index'
import qhqqgyfx from '@/views/performanceReportZJ/qhqqgyfx/index'
import jzfxbg from '@/views/performanceReportZJ/jzfxbg/index'
import zjqyljxbg from '@/views/performanceReportZJ/qyljxbg/index'
import zqjxbg from '@/views/performanceReportZJ/zqljxbg/index'
import hhclbg from '@/views/performanceReportZJ/hhclbg/index'
import foffxbg from '@/views/performanceReportZJ/foffxbg/index'
import ctaljxbg from '@/views/performanceReportZJ/ctaljxbg/index'
import qqljxbg from '@/views/performanceReportZJ/qqljxbg/index'
import campisi from '@/views/performanceReportZJ/campisi/index'
import ctfxbg from '@/views/performanceReportZJ/ctfxbg/index'

import tszbbg from '@/views/performanceReportZJ/tszbbg/index'
import dcpjcbg from '@/views/performanceReportZJ/dcpjcbg/index'
import dcpqybg from '@/views/performanceReportZJ/dcpqybg/index'
import dcpgsbg from '@/views/performanceReportZJ/dcpgsbg/index'

import jbbg from '@/views/performanceReportGF/jbbg/index'
import jbbgweek from '@/views/performanceReportGF/jbbgweek/index'
import bzbg from '@/views/performanceReportGF/bzbg/index'
import gpdt from '@/views/performanceReportGF/gpdt/index'
import zqjj from '@/views/performanceReportGF/zqjj/index'
import glqh from '@/views/performanceReportGF/glqh/index'
import tgmjj from '@/views/performanceReportGF/tgmjj/index'
import ccdlbg from '@/views/performanceReportGF/ccdlbg/index'
import gqzbbg from '@/views/performanceReportGF/gqzbbg/index'
import dyzbg from '@/views/performanceReportGF/dyzbg/index'
import factorindex from '@/views/performanceReportGF/factorindex/index'

import strategyprivate from '@/views/performanceReportGF/strategyprivate/index'

import cpfgclpyjk from '@/views/performanceReportZJ/clpy/index'
import zbg from '@/views/performanceReportGF/zbg/index'

import jxbgdcp from '@/views/performanceReportGF/jxbgdcp/index'

import gyhhfxbg from '@/views/performanceReportGF/gyhhfxbg/index'
import zxcedyzbg from '@/views/performanceReportGF/zxcedyzbg/index'

import jxxczbg from '@/views/performanceReportGF/jxxczbg/index'
import zbgxc from '@/views/performanceReportGF/zbgxc/index'

import customReportView from "@/views/customReport/reportViewNew/index"

import plbgdc from "@/views/gfreport/bathExportReport/index"
import fwptbgdy from "@/views/gfreport/bathReportSubscription/index"

export default {
  name: 'AppMain',
  components: {
    smcpxx,
    dcpfx,
    csbg,
    qyljxbg,
    zqljxbg,
    ctajxbg,
    jxjb,
    fofjxbg,
    sycpbg,
    gmzl,
    dwjzbxzl,
    syfx,
    rsybx,
    lhzbfx,
    dlzcccsx,
    qyljckzbsxt,
    qmccfx,
    cghyfx,
    zqpzpzsx,
    xypjfbsx,
    zhjqbdsx,
    syqxpzsx,
    spqhdtccqk,
    dlzcjxgy,
    gpflgy,
    zqgyfx,
    qhqqgyfx,
    jzfxbg,
    zjqyljxbg,
    zqjxbg,
    hhclbg,
    foffxbg,
    ctaljxbg,
    qqljxbg,
    campisi,
    ctfxbg,
    tszbbg,
    dcpjcbg,
    dcpqybg,
    dcpgsbg,
    jbbg,
    jbbgweek,
    bzbg,
    glqh,
    zqjj,
    gpdt,
    tgmjj,
    strategyprivate,
    ccdlbg,
    gqzbbg,
    dyzbg,
    factorindex,
    cpfgclpyjk,
    zbg,
    jxxczbg,
    zbgxc,
    gyhhfxbg,
    zxcedyzbg,
    jxbgdcp,
    customReportView,
    fwptbgdy,
    plbgdc
  },
  // computed用来监控自己定义的变量，该变量不在data里面声明，直接在computed里面定义，然后就可以在页面上进行双向数据绑定展示出结果或者用作其他处理
  computed: {
    // cachedViews() {
    //   return this.$store.state.tagsView.cachedViews
    // },
    // visitedViews () {
    //   return this.$store.state.tagsView.visitedViews
    // },
    key() {
      return this.$route.fullPath
    },
    componentsArray() {
      return window.saveIframeY
      // return []
    }
  },
  //sun 2021-07-29
  mounted() {
    //  $route.path === '' ? 'app-main-no-bg' : 'app-main'
    // 关闭标签触发
    this.$bus.$on('removeCache', (name, view) => {
      this.removeCache(name, view)
    })
  },
  beforeDestroy() {
    this.$bus.$off('removeCache')
  },
  //sun 2021-07-29
  methods: {
    getClassName(type) {
      if (type === 0) {
        if (this.$store.state.setting.fromPlatForm) {
          if (['/tqgl/dcpfx', '/tqgl/glrxq'].includes(this.$route.path)) {
            return 'app-main-outer-nest-bg'
          } else {
            return 'app-main-outer-nest'
          }
        } else {
          if (['/dashboard'].includes(this.$route.path)) {
            return 'app-main-outer'
          } else {
            return 'app-main-outer-nest-bg'
          }
        }
      } else {
        if (this.$store.state.setting.fromPlatForm) {
          if (['/tqgl/dcpfx', '/tqgl/glrxq'].includes(this.$route.path)) {
            return 'app-main-nest-no-bg'
          } else {
            return 'app-main-nest'
          }
        } else {
          if (['/tqgl/dcpfx', '/tqgl/glrxq'].includes(this.$route.path)) {
            return 'app-main-no-bg'
          } else {
            return 'app-main'
          }
        }
      }
    },
    // 获取有keep-alive子节点的Vnode
    getVnode() {
      // 判断子集非空
      if (this.$children.length == 0) return false
      let vnode
      for (let item of this.$children) {
        // 如果data中有key则代表找到了keep-alive下面的子集，这个key就是router-view上的key
        if (item.$vnode.data.key) {
          vnode = item.$vnode
          break
        }
      }
      return vnode ? vnode : false
    },
    // 移除keep-alive缓存
    removeCache(name, view = {}) {
      let vnode = this.getVnode()
      if (!vnode) return false
      let componentInstance = vnode.parent && vnode.parent.componentInstance
      // 这个key是用来获取前缀用来后面正则匹配用的
      let keyStart = vnode.key.split('/')[0]
      let thisKey = `${keyStart}${view.fullPath}`
      let regKey = `${keyStart}${view.path}`

      this[name]({ componentInstance, thisKey, regKey })
    },
    // 移除其他
    closeOthersTags({ componentInstance, thisKey }) {
      if (componentInstance) {
        Object.keys(componentInstance.cache).forEach((key, index) => {
          if (key != thisKey) {
            // 1 销毁实例(这里存在多个key指向一个缓存的情况可能前面一个已经清除掉了所有要加判断)
            if (componentInstance.cache[key]) {
              componentInstance.cache[key].componentInstance.$destroy()
            }
            // 2 删除缓存
            delete componentInstance.cache[key]
            // 3 移除key中对应的key
            componentInstance.keys.splice(index, 1)
          }
        })
      }
    },
    // 移除所有缓存
    closeAllTags({ componentInstance }) {
      if (componentInstance) {
        // 1 销毁实例
        Object.keys(componentInstance.cache).forEach(key => {
          if (componentInstance.cache[key]) {
            componentInstance.cache[key].componentInstance.$destroy()
          }
        })
        // 2 删除缓存
        componentInstance.cache = {}
        // 3 移除key中对应的key
        componentInstance.keys = []
      }
    },
    // 移除单个缓存
    closeSelectedTag({ componentInstance, regKey }) {
      let reg = new RegExp(`^${regKey}`)
      if (componentInstance) {
        Object.keys(componentInstance.cache).forEach((key, i) => {
          if (reg.test(key)) {
            // 1 销毁实例
            if (componentInstance.cache[key]) {
              componentInstance.cache[key].componentInstance.$destroy()
            }
            // 2 删除缓存
            delete componentInstance.cache[key]
            // 3 移除key中对应的key
            componentInstance.keys.splice(i, 1)
          }
        })
      }
    }
  }
}
</script>

<style scoped>
.app-main-outer {
  //padding: 10px 20px 0px 20px !important;
  //background-image: url('../../../assets/img/gfdashboardimg3.png');
  background-color: #243752;
  background-size: 100% 100%;
  background-repeat: no-repeat;
  height: 100%;
  /*background-color: #F3F5FB;
  height: 100%;*/
}
.app-main-outer-nest {
  padding: 0 !important;
  background-image: none;
  height: 100%;
}
.app-main-outer-nest-bg {
  /* background-image: url('../../../assets/img/gfdashboardimg6.png'); */
  background-size: 100% 100%;
  background-repeat: no-repeat;
  height: 100%;
}
.app-main {
  /*84 = navbar + tags-view = 50 +34 */
  height: calc(100vh - 92px);
  margin-top: 92px;
  width: 100%;
  /*padding: 0.5%;*/
  position: relative;
  overflow-y: auto;
  //background: #F3F5FB ;
  overflow-x: hidden;
  /* 新增Flex布局 */
  display: flex;
  flex-direction: column;
}
/* 新增样式 */
.content-footer {
  position: fixed;
  bottom: 0;
  z-index: 10;
  background-color: #181b25;
  padding: 0;
  width: 100%;
}

.footer-text {
  text-align: center;
  color: #fff;
  font-size: 14px;
  margin: 0;
}

/* 适配其他可能的class */
.app-main-no-bg,
.app-main-nest,
.app-main-nest-no-bg {
  display: flex;
  flex-direction: column;
}
.app-main-no-bg {
  height: calc(100vh - 104px);
  margin-top: 90px;
  width: 100%;
  padding: 10px;
  position: relative;
  overflow-y: auto;
  overflow-x: hidden;
  background-color: #f3f5fb;
}
.app-main-nest {
  height: 100vh;
  width: 100%;
  position: relative;
  overflow-y: auto;
  overflow-x: hidden;
}
.app-main-nest-no-bg {
  height: 100vh;
  width: 100%;
  position: relative;
  overflow-y: auto;
  overflow-x: hidden;
  background-color: #f3f5fb;
}
.app-main-nest > div {
  padding: 10px;
}
</style>
<style>
.app-main-nest > div.nest-none-padding {
  padding: 0px;
}

.show-iframe {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  visibility: unset;
  z-index: 0;
}

.unshow-iframe {
  position: absolute;
  visibility: hidden;
  z-index: -99999;
  top: 0;
  left: 0;
}
</style>

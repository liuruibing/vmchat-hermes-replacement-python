<template>
  <div id="app">
    <!-- :style="background" -->
    <!--    websocket组件-->
    <!--    <websocket/>-->
    <router-view v-if="isRouterAlive"/>
  </div>
</template>

<script>
// import websocket from './components/websocket/websocket'
import changeTheme from './utils/theme'

export default {
  name: 'App',
  components: {
    // websocket
  },
  provide() {
    return {
      reload: this.reload
    }
  },
  data() {
    return {
      isRouterAlive: true,
      background: {
        // 背景图片地址
        backgroundImage: 'url(' + require('./assets/img/dashboardimg.png') + ')',
        // 背景图片是否重复
        backgroundRepeat: 'no-repeat',
        // 背景图片大小
        backgroundSize: 'cover',
        // 背景颜色
        backgroundColor: '#000',
        // 背景图片位置
        backgroundPosition: 'center top'
      }
    }
  },
  watch: {
    $route(to, from) {
      this.initTheme()
    }
  },
  mounted() {
    this.initTheme()
  },
  methods: {
    checkRender() {
      const css = require('path').resolve(__dirname, 'style.css')
      // 检查元素是否已经渲染完成
      if (!css.length) {
        // 元素还未渲染完成，继续检查
        this.checkRender()
      } else {
        console.log(css, 'css')
        this.initTheme()
      }
    },
    initTheme() {
      const theme = this.$store.state.setting.theme
      let color = ''
      if (theme === 'gold') {
        color = '#0F65DD'
      }
      if (color) {
        changeTheme(color)
      }
    },
    reload() {
      this.isRouterAlive = false

      this.$nextTick(function () {
        this.isRouterAlive = true
      })
    }
  }
}
</script>
<style>
.theme-picker .el-color-picker__trigger {
  vertical-align: middle;
}

.theme-picker-dropdown .el-color-dropdown__link-btn {
  display: none;
}
</style>

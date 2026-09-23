<template>
  <div :class="classObj" class="app-wrapper">
    <div class="main-container">
      <div
        v-if="device === 'mobile' && sidebar.opened"
        class="drawer-bg"
        @click="handleClickOutside"
      />
      <!--顶部导航-->
      <navbar v-show="!$store.state.setting.fromPlatForm"/>
      <!--标签导航-->
      <tags-view v-show="!$store.state.setting.fromPlatForm"/>
      <!--页面中间内容-->
      <app-main />
    </div>
<!--     <div class="fotter_box" style="color: #333333;font-size: 14px;position: absolute;bottom: 0px;width: 100%;">{{ $store.state.setting.footerText }}</div>-->
<!--    <lock-windows ref="lockRelation" :lock="lock" v-if="!$store.state.setting.fromPlatForm"></lock-windows>-->
  </div>
</template>

<script>
import storage from "@/utils/storage";
import { Navbar, AppMain, TagsView } from "./components";
import ResizeMixin from "./mixin/ResizeHandler";
import $ from "jquery";
import LockWindows from "../islockWindowsfile/lock-windows.vue";
export default {
  name: "Layout",
  components: {
    Navbar,
    AppMain,
    TagsView,
    LockWindows
  },
  watch: {
    $route(to, form) {
      // console.log(form)
      let lock = this.$store.state.lock.isLock.isLock;
      if (lock) {
        if (form.path == "/yygl/ShowDapin") return;
        this.$store
          .dispatch("LogOut")
          .then(() => {
            location.reload();
            storage.setItem("isLock", { isLock: false });
            this.$store.state.lock.isLock.isLock = false;
          })
          .catch(() => {
            //即使失败也跳转
            location.reload();
            storage.setItem("isLock", { isLock: false });
            this.$store.state.lock.isLock.isLock = false;
          });
      }
    }
  },
  mixins: [ResizeMixin],
  computed: {
    sidebar() {
      return this.$store.state.app.sidebar;
    },
    device() {
      return this.$store.state.app.device;
    },
    classObj() {
      return {
        withoutAnimation: this.sidebar.withoutAnimation,
        mobile: this.device === "mobile"
      };
    },
    lock() {
      return this.$store.state.lock.isLock.isLock;
    }
  },
  mounted() {
    // this.$refs.lockRelation.init(this.$store.state.lock.isLock.isLock);
  },
  methods: {
    handleClickOutside() {
      this.$store.dispatch("closeSideBar", { withoutAnimation: false });
    }
  }
};
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
@import "~@/styles/mixin.scss";
.app-wrapper {
  @include clearfix;
  position: relative;
  height: 100%;
  width: 100%;
  min-width: 1366px;
  &.mobile.openSidebar {
    position: fixed;
    top: 0;
  }
}
.drawer-bg {
  background: #000;
  opacity: 0.3;
  width: 100%;
  top: 0;
  height: 100%;
  position: absolute;
  z-index: 999;
}
.main-container {
  overflow: hidden !important;
  // height: calc(100vh - 20px);
  height: 100%;
}
</style>

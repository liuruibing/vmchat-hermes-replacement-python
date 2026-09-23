<template>
  <!---->
  <div
    style="height: 100%; overflow-y: auto; padding-bottom:20px;margin:10px"
    v-loading="loading && $store.state.setting.loadingShow"
  >
    <!--    v-loading="loading && $store.state.setting.loadingShow"-->
    <iframe
      :src="iframeData.src"
      link
      style="display: inline; border: 0px; overflow: hidden; min-height: 98%"
      :name="name"
      :id="id"
      width="100%"
      frameborder="0"
      class="J_iframe"
    >
      <p>您的浏览器不支持 iframe 标签。</p>
    </iframe>
  </div>
</template>

<script>
import $ from "jquery";
export default {
  name: "reportForms",
  props: {
    iframeData: {
      src: "",
    },
    id: {
      type: String,
      default: "J_iframe_id",
    },
    name: {
      type: String,
      default: "iframeVue",
    },
  },
  data() {
    return {
      loading: false, //显示加载中
    };
  },
  watch: {
    //监听到iframe src改变重新变为加载中
    "iframeData.src": function (newVal, oldVal) {
      var self = this;
      self.loading = true;
    },
  },

  mounted() {
    var self = this;

    window.addEventListener('message', this.handleMessage);
    //iframe加载完成后，对其子元素进行操作
    var iframe = document.getElementById(this.id);
    if (iframe.attachEvent) {
      iframe.attachEvent("onload", function () {
        self.loading = false;
      });
    } else {
      iframe.onload = function () {
        self.loading = false;
      };
    }
  },
  beforeDestroy() {
    window.removeEventListener('message', this.handleMessage);
  },
  methods: {
    handleMessage(msg) {
      if (msg && msg.data && msg.data.action === 'INFO_JSP_PY') {
        const payload = msg.data.payload;
        if (payload && payload.type === 'clpy' && payload.msg && payload.msg.path) {
          const path = {
            path: payload.msg.path,
            query: payload.msg.params || {} // 传递接收到的参数
          };
          this.$router.push(path);
        }
      }
    }
  },
};
</script>

<style>
</style>

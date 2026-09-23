<template>
  <!---->
  <div
    style="height: 100%; overflow-y: auto; padding-bottom: 54px"

  >
<!--    v-loading="loading && $store.state.setting.loadingShow"-->
    <iframe
      :src="iframeData.src"
      link
      style="display: inline; border: 0px; overflow: hidden;  height: 2900px"
      name="iframeVue"
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

    // function fun_iframe_height(){
    //   $(".J_iframe").height($(".J_iframe").contents().find("body").height());
    //   console.log($(".J_iframe").contents().find("body").height());
    // }
    // fun_iframe_height();
    // var iframeHeight = setInterval(fun_iframe_height,200);
    // clearInterval(iframeHeight);

    //  等iframe加载完毕
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
  methods: {},
};
</script>

<style>
</style>

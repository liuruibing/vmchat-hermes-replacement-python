<template>
  <div
    style="height: 100%; overflow-y: auto; padding-bottom: 54px"

  >
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
export default {
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

}
</script>
<style lang="scss" scoped>

</style>

<template>
  <div class="quartile_box">
    <li :class="val == '1' ? 'select_quartile_color' : 'select_quartile_color_none'"></li>
    <li :class="val == '2' ? 'select_quartile_color' : 'select_quartile_color_none'"></li>
    <li :class="val == '3' ? 'select_quartile_color' : 'select_quartile_color_none'"></li>
    <li :class="val == '4' ? 'select_quartile_color' : 'select_quartile_color_none'"></li>
  </div>
</template>

<script>
  export default {
    name: "quartile_box",
    props: {
      val:'',//接收的值
    },
    data() {
      return {

      }
    },
    mounted() {
      let self = this;
    },
    //消除多次传输
    methods:{


    }
  }
</script>

<style scoped>

</style>

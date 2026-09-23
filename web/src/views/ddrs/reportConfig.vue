<template>
  <div class="">
    <dd-report-config :baseApi="baseApiData" :token="tokenData"></dd-report-config>
  </div>
</template>

<script>
export default {
  name: "DdRs",
  data() {
    return {
      baseApiData: "",
      tokenData: "",
    };
  },
  mounted() {
    // params , url 合并
    this.baseApiData = this.$store.state.setting.baseApi;
    this.tokenData = this.$store.state.user.token;
  }
};
</script>

<style lang="scss" scoped></style>

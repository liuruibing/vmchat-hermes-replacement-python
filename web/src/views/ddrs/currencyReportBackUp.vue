<template>
  <div class="page-card-common-rs">
    <dd-currency-report :baseApi="baseApiData" :token="tokenData" :formQueryConfig="formQueryConfig"></dd-currency-report>
  </div>
</template>

<script>
export default {
  name: "DdRs",
  data() {
    return {
      baseApiData: "",
      tokenData: "",
      formQueryConfig: {}
    };
  },
  activated() {
    if (this.$store.getters.fromLinkJump) {
      this.$store.commit("SET_FROM_LINK_JUMP", false);
      this.formQueryConfig = this.$store.getters.rsJumpData;
      this.$store.commit("SET_RS_LINK_JUMP_DATA", []);
    }
  },
  mounted() {
    // params , url 合并

    this.baseApiData = this.$store.state.setting.baseApi;
    this.tokenData = this.$store.state.user.token;
  }
};
</script>

<style lang="scss" scoped></style>

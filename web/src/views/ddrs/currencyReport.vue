<template>
  <div>
    <dd-rs :formQueryConfig="formQueryConfig"></dd-rs>
    <!-- <dd-currency-report :baseApi="baseApiData" :token="tokenData" :formQueryConfig="formQueryConfig" className="page-card-common"></dd-currency-report> -->
  </div>
</template>

<script>
import DdRs from "./reportTemplate";

export default {
  name: "currencyReport",
  components: { DdRs },
  data() {
    return {
      formQueryConfig: {},
      baseApiData: '',
      tokenData: ''
    };
  },
  activated() {
    this.baseApiData = this.$store.state.setting.baseApi;
    this.tokenData = this.$store.state.user.token;
    if (this.$store.getters.fromLinkJump) {
      this.$store.commit("SET_FROM_LINK_JUMP", false);
      this.formQueryConfig = this.$store.getters.rsJumpData || {};
      console.log(this.formQueryConfig);
      this.$store.commit("SET_RS_LINK_JUMP_DATA", {});
    }
  }
};
</script>

<style lang="scss" scoped>
.page-card-common {
  min-height: 0px;
  padding: 0px;
}
</style>

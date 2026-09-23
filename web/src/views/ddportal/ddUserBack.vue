<template>
  <div class="ddportal-ui">
    <dd-user-tactics :baseApi="baseApiData" :token="tokenData"></dd-user-tactics>
  </div>
</template>

<script>
export default {
  name: "home",
  data() {
    return {
      baseApiData: "",
      tokenData: ""
    };
  },
  mounted() {
    this.baseApiData = this.$store.state.setting.baseApi;
    this.tokenData = this.$store.state.user.token;
  }
};
</script>

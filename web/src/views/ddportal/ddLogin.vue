<template>
  <div class="ddportal-ui">
    <dd-login :baseApi="baseApiData" :token="tokenData"></dd-login>
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

<template>
  <div class="ddportal-ui">
    <dd-role :baseApi="baseApiData" :token="tokenData" id="ddportal-ui"></dd-role>
  </div>
</template>

<script>
export default {
  name: "home",
  data() {
    return {
      baseApiData: "",
      tokenData: "",
    };
  },
  mounted() {
    this.baseApiData = this.$store.state.setting.baseApi;
    this.tokenData = this.$store.state.user.token;
  }
};
</script>

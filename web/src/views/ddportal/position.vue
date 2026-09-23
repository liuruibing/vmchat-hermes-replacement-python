<template>
  <div class="ddportal-ui">
     <dd-new-position :baseApi="baseApiData" :token="tokenData"></dd-new-position>
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

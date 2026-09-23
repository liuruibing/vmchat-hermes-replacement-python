<template>
  <div class="ddportal-ui">
      <dd-dictionary :baseApi="baseApiData" :token="tokenData"></dd-dictionary>
  </div>
</template>

<script>
export default {
  name: "DdDictionaryView",
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

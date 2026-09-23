<template>
  <div class="ddportal-ui" >
    <dd-menu :baseApi="baseApiData" :token="tokenData" id="dd-menu"></dd-menu>
  </div>
</template>

<script>
export default {
  name: 'home',
  data() {
    return {
      baseApiData: '',
      tokenData: ''
    }
  },
  mounted() {
    this.baseApiData = this.$store.state.setting.baseApi
    this.tokenData = this.$store.state.user.token
  }
}
</script>
<style lang="scss">
#dd-menu {
  .forms_table_title {
    display: inline-block;
    width: 80px !important;
    padding-left: 8px;
    //font-size: 13px !important;
  }
}
</style>
<style lang="scss" scoped>
::v-deep .forms_table_title {
  padding-left: 8px;
}
</style>

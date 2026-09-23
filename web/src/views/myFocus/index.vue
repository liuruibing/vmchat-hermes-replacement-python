<template>
  <div class="hg100 " v-auto-enter>
    <el-tabs v-model="activeName" type="card" class="standard-tab" @tab-click="handleTabClick" style=" margin: 10px 10px 10px 10px;">
      <el-tab-pane label="私募产品" name="smcp">
        <all-market-private ref="allMarket"></all-market-private>
      </el-tab-pane>
<!--      <el-tab-pane label="私募管理人" name="smglr">
        <private-manager ref="privateManager"></private-manager>
      </el-tab-pane>-->
    </el-tabs>
  </div>
</template>
<script>
import allMarketPrivate from './allMarketPrivate'
import privateManager from './privateManager'

export default {
  name: 'MyFocus',
  components: { allMarketPrivate, privateManager },
  data() {
    return {
      activeName: 'smcp'
    }
  },
  activated() {
    if (this.$store.getters.fromPageJump) {
      if (this.$route.query && this.$route.query.name) {
        this.activeName = this.$route.query.name
        this.$store.commit('SET_FROMPAGEJUMP', false)
      }
    }
  },
  methods: {
    handleTabClick(tab) {
      if (tab.name === 'smglr') {
        this.$refs.privateManager.$refs.allTablePrivateManager.$refs.tableBody.handleTableHeightMyFocus()
      } else {
        this.$refs.allMarket.$refs.allTable.$refs.tableBody.handleTableHeightMyFocus()
      }
    }
  }
}
</script>
<style lang="scss" scoped>
.bg {
  background-color: #f4f6fa;
}
</style>

<template>
  <div class="refactor-dashboard" style="padding-top: 10px;background-color: #243752;">
    <el-row>
      <el-col :span="24" class="pd10">
        <quick-nav></quick-nav>
      </el-col>
    </el-row>
    <el-row>
<!--      <el-col :span="16" class="pd10">-->
<!--        <dynamic-condition ref="dynamicCondition"></dynamic-condition>-->
<!--      </el-col>-->
      <el-col :span="24" class="pd10">
        <market-index ref="MarketIndex"></market-index>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="16" class="pd10">
        <y-hprivate-index ref="YHprivateIndex"></y-hprivate-index>
      </el-col>
      <el-col :span="8" class="pd10">
        <factor-return ref="FactorReturn"></factor-return>
      </el-col>
    </el-row>
<!--    <el-row>-->
<!--      <el-col :span="16" class="pd10">-->
<!--        <my-focus ref="myFocus"></my-focus>-->
<!--      </el-col>-->
<!--      <el-col :span="8" class="pd10">-->
<!--        <simulation-group ref="simulationGroup"></simulation-group>-->
<!--      </el-col>-->
<!--    </el-row>-->
    <!--    <el-row v-for="(rowItems, index) in Array.from({ length: Math.ceil(compList.length / 3) }, (v, i) => compList.slice(i * 3, i * 3 + 3))" :key="index">
          <el-col :span="8" class="pd10" v-for="item in rowItems" :key="item.key">
            <component :ref="item.name" :is="item.comp"></component>
          </el-col>
        </el-row>-->
  </div>
</template>

<script>
import QuickNav from './components/quickNav/QuickNav.vue'
export default {
  name: 'RefactorDashboard',
  components: {
    QuickNav,
    //DynamicCondition: () => import('./components/dynamicCondition/index.vue'),
   // SystemMessage: () => import('./components/systemMessage/index.vue'),
    //PublicRequest: () => import('./components/publicRequest/index.vue'),
    //SimulationGroup: () => import('./components/simulationGroup/index.vue'),
    //MyFocus: () => import('./components/myFocus/index.vue'),
    MarketIndex: () => import('./components/marketIndex/index.vue'),
    FactorReturn: () => import('./components/factorReturn/index.vue'),
    YHprivateIndex: () => import('./components/yHprivateIndex/index.vue'),
  },
  data() {
    return {
      compList: [
        { name: 'myFocus', comp: 'MyFocus', key: 6 },
        { name: 'simulationGroup', comp: 'SimulationGroup', key: 7 },
        { name: 'systemMessage', comp: 'SystemMessage', key: 8}
      ]
    }
  },
  mounted() {
    this.initDashboard()
  },
  methods: {
    /** 初始化数据 */
    initDashboard() {
      setTimeout(() => {
        this.$refs.MarketIndex.initData()
        // this.$refs.dynamicCondition.initData()
        this.$refs.YHprivateIndex.initData()
        this.$refs.FactorReturn.initData()
        //this.$refs.myFocus.initData()
        //this.$refs.simulationGroup.initData()
        /* for (let key in this.$refs) {
          if (this.$refs[key] && this.$refs[key].length) {
            this.$refs[key][0].initData()
          }
        } */
      }, 300)
    }
  }
}
</script>

<style></style>

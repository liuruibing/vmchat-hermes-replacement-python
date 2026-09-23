<template>
  <div class="file_collection">
    <transition name="el-zoom-in-center">
      <!-- 图表 -->
      <chartView 
        class="chartView"
        v-show="chartView_show"
        @transition="chartView_show=false"
      ></chartView>
    </transition>
    <transition name="el-zoom-in-center">
      <!-- 列表 -->
      <fileDataView 
        class="fileDataView"
        v-show="!chartView_show"
        @transition="chartView_show=true"
      ></fileDataView>
    </transition>
  </div>
</template>

<script>
import chartView from "./chartView.vue";
import fileDataView from "./fileDataList.vue";
export default {
  components: {
    chartView,
    fileDataView,
  },
  data(){
    return{
      chartView_show:true,
    }
  }
};
</script>

<style lang="scss">
.file_collection{
  position: relative;
  .chartView{
    width: 100%;
    position: absolute;
  }
  .fileDataView{
    width: 100%;
    position: absolute;
  }
}
</style>
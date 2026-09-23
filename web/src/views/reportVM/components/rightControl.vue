<!-- 右侧控制区域 -->
<template>
  <div class="right-control">
    <div style="color: #FFFFFF;font-size:16px;">已选指标（上下拖动排序）</div>
    <draggable
      v-model="$store.state.reportVM.currentIndexTreeData"
      group="people"
      @change="change"
    >
      <div v-for="(item, index) in reportVMCurrentData" :id="item.vcCode" :key="item.vcCode"
           class="mt10 right-item" style="width: 100%;">
        <div :title="item.vcIndexName" style="color: #FFFFFF;white-space: nowrap;overflow: hidden;text-overflow: ellipsis;display: inline-block;width:100%;">{{ item.vcIndexName }}</div>
      </div>
    </draggable>
  </div>
</template>
<script>
import draggable from "vuedraggable"
import {mapGetters} from 'vuex'

export default {
  name: "RightControl",
  components: {draggable},
  props: {
    indexArray: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {}
  },
  computed: {
    ...mapGetters(['reportVMConditionData', 'reportVMIndexData', 'reportVMCurrentData'])
  },
  methods: {
    change() {
      console.log(this.indexArray)
    },
  }
}
</script>
<style scoped lang="scss">
@import '@/styles/variables.scss';

.right-control {
  height: 100%;
  width: 100%;
  padding: 15px;
  //border: 1px solid #ebeef5;
  //box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
  background-color: $reportVM-model-bg;
  border-radius: 15px;
}
.right-item {
  height: 25px;
  line-height: 25px;
  font-size: 14px;
  cursor: grab;
}
.right-item:hover{
  background-color: $reportVM-bg-color;
}
.right-item:active {
  cursor: grabbing;
}

</style>

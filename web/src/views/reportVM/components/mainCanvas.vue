<!-- 画布区域 -->
<template>
  <div id="mainCanvas" class="main-canvas">
    <div style="height: 100%;width: 100%;overflow-y: auto;">
      <!-- 存放条件区域 -->
      <div id="mainCanvasFormQuery">
        <div v-for="(item, index) in reportVMCurrentConditionData" :id="item.vcCode" :key="item.vcCode"
             v-html="item.htmlStr"
             class="mt10">
        </div>
      </div>
      <!-- 存放指标区域 -->
      <div id="mainCanvasSpace">
        <draggable
          v-model="$store.state.reportVM.currentIndexTreeData"
          group="people"
          @change="change"
        >
          <div v-for="(item, index) in reportVMCurrentData" :id="item.vcCode" :key="item.vcCode"
               class="mt10"
               style="position: relative;"
          >
            <!-- 删除图标 -->
            <span class="delete-icon">
              <i class="el-icon-circle-close" @click="deleteItem(item)"></i>
            </span>
            <div v-html="item.htmlStr" :key="item.vcCode"></div>
          </div>
        </draggable>
      </div>
    </div>
  </div>
</template>
<script>
import draggable from "vuedraggable"
import {mapGetters} from 'vuex'

export default {
  name: 'MainCanvas',
  components: {draggable},
  props: {
    indexArray: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      saveIndexArray: [],
      oldIndexArray: [],
    }
  },
  computed: {
    ...mapGetters(['reportVMConditionData', 'reportVMIndexData', 'reportVMCurrentData', 'reportVMCurrentConditionData'])
  },
  watch: {
    'reportVMCurrentData': {
      handler(newVal, oldVal) {
        // 在数组变化时执行新增元素的脚本
        newVal.forEach(item => {
          const isNew = !this.oldIndexArray.some(oldItem => oldItem.vcCode === item.vcCode);
          if (isNew) {
            let timer = null
            timer = setInterval(() => {
              const div = document.getElementById(item.vcCode)
              if (div) {
                const scripts = div.getElementsByTagName('script')
                for (let i = 0; i < scripts.length; i++) {
                  this.executeScript(scripts[i].textContent)
                }
                if(scripts && scripts.length > 0) {
                  clearInterval(timer)
                }
              }
            }, 3000)
          }
        });
        // 更新旧数组
        this.oldIndexArray = newVal.slice();
      },
      deep: true,
    }
  },
  methods: {
    deleteItem(delNode) {
      let findIndex = this.reportVMCurrentData.find(item => item.vcCode === delNode.vcCode)
      if (findIndex !== -1) {
        this.$emit('deleNode', delNode)
      }
    },
    executeScript(scriptContent) {
      const script = document.createElement('script');
      script.textContent = scriptContent;
      document.body.appendChild(script);
    },
    change() {
      console.log(this.indexArray)
    },
  }
}
</script>
<style scoped lang="scss">
@import '@/styles/variables.scss';

.main-canvas {
  padding: 15px;
  height: 100%;
  width: 100%;
  //border: 1px solid #ebeef5;
  //box-shadow: 0 2px 12px 0 rgba(0,0,0,.1);
  border-radius: 15px;
  background-color: #FFFFFF;
}

.delete-icon {
  width: 100%;
  text-align: right;
  color: rgba(243, 148, 9, 0.8);
  font-size: 20px;
  font-weight: 600;
  line-height: 25px;
  position: absolute;
  top: 0;
  right: 15px;
  cursor: grab;
}

.delete-icon:hover {
  background-color: $reportVM-bg-color;
}

.el-icon-circle-close:hover {
  cursor: pointer;
}

.delete-icon:active {
  cursor: grabbing; /* 鼠标按下时样式为grabbing */
}
</style>

<template>
  <div class="tree-view">
    <div class="time-line">
      <time-line :dateList="dateList" @updateDdate="handleChangeDate"></time-line>
    </div>
    <div class="tree-content" @mousedown.stop="move" v-loading="loading">
      <tree-item :tree-data="treeData"></tree-item>
    </div>
  </div>
</template>

<script>
import TreeItem from './components/tree-item'
import TimeLine from './components/time-line'
import { getNodeList, getTreeData } from './scripts/api'
import commonFun from '@/filters/new_common'
export default {
  name: 'treeView',
  components: {
    TreeItem,
    TimeLine
  },
  data() {
    return {
      treeData: [],
      dateList: [],
      curCombCode: '',
      curDateNode: '',
      loading: false
    }
  },
  watch: {
    '$route.query.combList': {
      async handler(newVal) {
        if (this.$store.getters.fromPageJump && this.$route.query.type === 'treeView') {
          if (newVal && newVal.combineCode) {
            // 动态修改tag-views dom标签
            document.querySelector('.tags-view-item.active .tag-title') &&
              (document.querySelector('.tags-view-item.active .tag-title').innerText = newVal.combineName + ' 树形展示' || '树形展示')
            this.curCombCode = newVal.combineCode
            await this.handleFindNode()
            this.getCombTreeData()
          }
        }
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    /**
     * @description 切换时间节点重新查询
     */
    handleChangeDate(date) {
      this.curDateNode = date
      this.getCombTreeData()
    },
    /**
     * @description 查询时间节点
     */
    handleFindNode() {
      return new Promise((resolve, reject) => {
        const params = {
          combineCode: this.curCombCode
        }
        getNodeList(params)
          .then((res) => {
            if (res.data.status === 0) {
              this.dateList = res.data.data.rows || []
              if (this.dateList && this.dateList.length) {
                this.dateList.forEach((item) => {
                  this.$set(item, 'checked', false)
                })
                this.dateList[this.dateList.length - 1].checked = true
                this.curDateNode = this.dateList[this.dateList.length - 1].ddate
                resolve()
              }
            }
          })
          .catch((err) => {
            reject(err)
          })
      })
    },
    /**
     * @description 获取子产品树形数据
     */
    getCombTreeData() {
      const params = {
        combineCode: this.curCombCode,
        ddate: this.curDateNode
      }
      this.loading = true
      getTreeData(params)
        .then((res) => {
          if (res.data.status === 0) {
            const nodeData = res.data.data.rows || []
            this.treeData = commonFun.converTreeData(nodeData, 0, 'pid', 'fId').data
            this.loading = false
          } else {
            this.loading = false
          }
        })
        .catch((e) => {
          this.loading = false
        })
    },
    /**
     * @description 拖拽移动
     */
    move(e) {
      const odiv = e.currentTarget // 获取元素
      // 算出鼠标相对元素的位置
      const disX = e.clientX - odiv.offsetLeft
      const disY = e.clientY - odiv.offsetTop
      document.onmousemove = (e) => {
        // 鼠标按下并移动的事件
        // 用鼠标的位置减去鼠标相对元素的位置，得到元素的位置
        const left = e.clientX - disX
        const top = e.clientY - disY
        // 移动当前元素
        odiv.style.left = left + 'px'
        odiv.style.top = top + 'px'
      }
      document.onmouseup = () => {
        document.onmousemove = null
        document.onmouseup = null
      }
    }
  }
}
</script>
<style scoped lang="scss">
.tree-view {
  background-color: #f4f6fa;
  height:100%;
  position: relative;
  .time-line {
    position: fixed;
    z-index: 999;
    height: 150px;
    width: 800px;
    left: 50%;
    margin-left: -400px;
  }
  .tree-content {
    width: 100%;
    background: #f4f6fa;
    position: absolute;
    top: 150px;
    left: 0;
    cursor: pointer;
  }
}
</style>

<template>
  <el-container class="report">
    <el-aside width="20%" style="padding-right: 10px;">
      <left-tree
        ref="leftTree"
        check-on-click-node
        :newReportConfig="newReportConfig"
        @conditionNodeClick="handleConditionClick"
        @indexNodeClick="handleIndexNodeClick"
        @checkedIndex="handleCheckedIndex"
        @return="() => {$emit('return')}"
      ></left-tree>
    </el-aside>
    <el-container>
      <el-main>
        <main-canvas ref="mainCanvas" @deleNode="handleDelCurrentTreeData"></main-canvas>
      </el-main>
      <!-- 右侧栏 -->
      <el-aside width="20%" style="padding-left: 10px;">
        <right-control></right-control>
      </el-aside>
    </el-container>
  </el-container>
</template>
<script>
import leftTree from './leftTree'
import mainCanvas from './mainCanvas'
import rightControl from './rightControl'
import pageApi from '../api/index'
import {mapGetters} from "vuex";

export default {
  name: 'ReportVM',
  components: {leftTree, mainCanvas, rightControl},
  props: {
    rowInfo: {
      type: Object,
      default: () => {
        return {}
      }
    },
    newReportConfig: {
      type: Object,
      default: () => {
        return {}
      }
    },
  },
  watch: {
    rowInfo: {
      handler(val) {
      },
    },
    newReportConfig: {
      handler(val) {
        // 初始化
        this.debouncedHandler(val)
      },
      immediate: true,
    }
  },
  data() {
    return {
      indexArray: [], // 存储指标数组
      debouncedFun: null,
    }
  },
  computed: {
    ...mapGetters(['reportVMConditionData', 'reportVMIndexData', 'reportVMCurrentData'])
  },
  methods: {
    debouncedHandler: _.debounce(function(val) {
      this.initReport()
      this.$refs.leftTree.getLeftTree(val.vcReportType);
      this.$refs.leftTree.vcReportType = val.vcReportType;
      if (this.rowInfo && this.rowInfo.row) {
        this.$refs.leftTree.setMode(this.rowInfo.row, 'edit');
        this.$nextTick(() => {
          // data 遍历 设置 选中的 tree 节点
          this.$refs.leftTree.setTreeNode(this.rowInfo.data);
        });
      } else {
        this.$refs.leftTree.setMode({
          vcTemplatEname: val.templateName,
          fType: val.fVmType,
          templateId: '',
          vcReportType: val.vcReportType,
        }, 'add');
      }
    }, 300), // 300 毫秒防抖时间

    /**
     * @Description: 新建报告
     * @author Liu Rui Bing
     * @date 2024/4/29
     */
    setNewReport() {
      this.initReport()
      this.$refs.leftTree.setMode({}, 'add')
    },
    /**
     * @Description: 初始化画布区域
     * @author Liu Rui Bing
     * @date 2024/4/29
     */

    initReport() {
      this.$store.commit('SET_CURRENT_CONDITION_TREE_DATA', [])
      this.$store.commit('SET_CONDITION_TREE_DATA', [])
      this.$store.commit('SET_INDEX_TREE_DATA', [])
      this.$store.commit('SET_CURRENT_TREE_DATA', [])
    },

    /**
     * @Description: 设置指标树 和 条件树 选中状态并渲染
     * @author Liu Rui Bing
     * @date 2024/4/29
     */
    setLeftTree(val) {

    },
    /**
     * @Description: 添加 / 删除 指标元素
     * @author Liu Rui Bing
     * @date 2024/4/26
     */
    handleCheckedIndex({data, type}) {
      if (type === 'addIndex') {
        if (data && !data.children) {
          let params = {}
          params.indexCode = data.vcCode
          pageApi.previewIndex(params).then(res => {
            let {status} = res.data
            if (status === 200) {
              let tempObj = {...data}
              tempObj.htmlStr = res.data.data
              this.$store.dispatch('addCurrentTreeData', tempObj)
            }
          })
        }
      } else {
        if (data && !data.children) {
          let findObj = this.reportVMCurrentData.find(item => item.vcCode === data.vcCode)
          if (findObj) {
            this.$store.commit('DEL_CURRENT_TREE_DATA', findObj)
          }
        }
      }
    },
    handleConditionClick({data, type}) {
      if (type === 'delNode') {
        this.$store.dispatch('setCurrentConditionTreeData', [])
      } else {
        if (data && !data.children) {
          let params = {}
          params.indexCode = data.vcCode
          pageApi.previewIndex(params).then(res => {
            let {status} = res.data
            if (status === 200) {
              let tempObj = {...data}
              tempObj.htmlStr = res.data.data
              this.$store.dispatch('setCurrentConditionTreeData', [tempObj])
            }
          })
        }
      }
    },
    handleIndexNodeClick(data) {
      this.indexArray = data
    },
    /**
     * @Description: 取消勾选 删除的指标
     * @author Liu Rui Bing
     * @date 2024/4/28
     */
    handleDelCurrentTreeData(node) {
      this.$refs.leftTree.handleCancelCheckNode(node)
    }
  }
}
</script>
<style scoped>
.report {
  height: 100%;
  width: 100%;
  padding: 10px;
  background-color: #121212;
}
.el-tree {
  color: #FFFFFF !important;
}


</style>

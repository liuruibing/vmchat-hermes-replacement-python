<template>
  <div class="group-list">
    <el-aside :width="boxWidth" class="productAndProperty_virtual">
      <div style="height: 100%">
        <div class="tree-content">
          <el-tree ref="treeRef"  :props="defaultProps" :data="groupData" node-key="pid" @node-click="handleNodeClick">
            <div slot-scope="{ node, data }" class="custom-tree-node standard-form">
              <el-tooltip class="dd-ellipsis" effect="dark" :content="node.label" placement="top-start">
                <span style="font-size: 14px">{{ node.label || '-' }}</span>
              </el-tooltip>
              <div v-if="node.label !== '默认分组'">
                <el-button type="info" size="mini" icon="el-icon-edit" circle @click="editGroup"></el-button>
                <el-button type="danger" size="mini" icon="el-icon-delete" circle @click="deleteGroup(data.pid)"></el-button>
              </div>
              <div v-else>
                <el-button type="info" size="mini" icon="el-icon-plus" class="plus" @click="addGroup">新建</el-button>
              </div>
            </div>
          </el-tree>
        </div>
        <div class="flex_center left_right_button" style="cursor: col-resize">
          <i :class="left_right_button_icon" style="cursor: pointer" @click="ProductAndProperty_left_right"></i>
        </div>
      </div>
    </el-aside>
    <group-edit ref="groupEdit" :title="dialogTitle" :is-show-edit="isShowEdit" :status="dialogStatus" :current-data="currentData" @closeedit="closeEdit"></group-edit>
  </div>
</template>
<script>
import commonAPI from '@/api/common.js'
import { delFundPool } from '../scripts/api'
import groupEdit from './group-edit.vue'
export default {
  components: {
    groupEdit
  },
  data() {
    return {
      boxWidth: '210px',
      defaultProps: {
        children: 'children',
        label: 'label'
      },
      groupData: [],
      left_right_button_icon: 'el-icon-arrow-left',
      dialogTitle: '',
      isShowEdit: false,
      dialogStatus: 'ADD',
      currentData: {},
      screenHeight: document.documentElement.clientHeight
    }
  },
  async mounted() {
    await this.getMyFocusGroup()
    await this.$nextTick(function () {
      this.$refs.treeRef.setCurrentKey(this.groupData[0].pid)
    })
  },
  methods: {
    productMove(e) {
      const self = this
      const odiv = e.target // 获取目标元素

      // 算出鼠标相对元素的位置
      const disX = e.clientX - odiv.offsetLeft
      const disY = e.clientY - odiv.offsetTop
      document.onmousemove = (e) => {
        // 鼠标按下并移动的事件
        // 用鼠标的位置减去鼠标相对元素的位置，得到元素的位置
        const left = e.clientX - disX
        const top = e.clientY - disY
        // 移动当前元素{
        let boxWidth = 0
        if (left < 10 || left == 25) {
          boxWidth = 25
          self.left_right_button_icon = 'el-icon-arrow-right'
          let ele = document.getElementsByClassName('left_right_button')
          ele[0].style.width = '25px'
        } else if (left > 700) {
          boxWidth = 700
          self.left_right_button_icon = 'el-icon-arrow-left'
          let ele = document.getElementsByClassName('left_right_button')
          ele[0].style.width = '10px'
        } else {
          boxWidth = left
          self.left_right_button_icon = 'el-icon-arrow-left'
          let ele = document.getElementsByClassName('left_right_button')
          ele[0].style.width = '10px'
        }

        self.boxWidth = boxWidth + 'px'
        // 隐藏打开事件
        self.$emit('asideOpen', boxWidth)
      }
      document.onmouseup = (e) => {
        document.onmousemove = null
        document.onmouseup = null
      }
    },
    // 点击隐藏
    ProductAndProperty_left_right() {
      // 0 关闭 1 开启
      let switchOpen = 1
      var self = this
      if (self.boxWidth != '10px') {
        switchOpen = 0
        self.boxWidth = '10px'
        let ele = document.getElementsByClassName('left_right_button')
        ele[0].style.width = '10px'

        self.left_right_button_icon = 'el-icon-arrow-right'
      } else {
        switchOpen = 1
        self.boxWidth = '210px'
        self.left_right_button_icon = 'el-icon-arrow-left'
        let ele = document.getElementsByClassName('left_right_button')
        ele[0].style.width = '10px'
      }
      // 隐藏打开事件
      self.$emit('asideOpen', switchOpen)
    },
    /**
     * @description 选择节点回调
     */
    handleNodeClick(data) {
      this.currentData = data
      this.$emit('getpid', data.pid)
    },
    /**
     * @description 获取分组信息
     */
    async getMyFocusGroup() {
      const data = {
        indexCode: 'f98b1f94-97c7-462d-b7b2-1da0cc1d3fb5'
      }
      try {
        const res = await commonAPI.getDataBysqlCode(data)
        if (res.data.status === 0) {
          const groupArr = res.data.data || []
          this.groupData = groupArr.map((item) => {
            return {
              label: item.VC_POOLNAME,
              pid: item.VC_POOLCODE,
              children: []
            }
          })
          this.$nextTick(function () {
            this.$refs.treeRef.setCurrentKey(this.groupData[0].pid)
          })
        }
      } catch (e) {
        this.groupData = []
      }
    },
    /**
     * @description 删除分组
     */
    async deleteGroup(pid) {
      const data = {
        poolCode: pid || ''
      }
      this.$confirm('此操作将删除该分组, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          delFundPool(data).then((res) => {
            if (res.data.status === 0) {
              this.$message({
                type: 'success',
                message: res.data.message || '删除成功',
                customClass: 'message-success'
              })
              this.getMyFocusGroup()
              this.handleNodeClick(this.groupData[0])
            } else {
              this.$message({
                type: 'error',
                message: res.data.message || '删除失败',
                customClass: 'message-error'
              })
            }
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消操作'
          })
        })
    },
    /**
     * @description 新增分组
     */
    addGroup() {
      this.dialogTitle = '新增分组'
      this.isShowEdit = true
      this.dialogStatus = 'ADD'
    },
    /**
     * @description 重命名分组
     */
    editGroup() {
      this.dialogTitle = '重命名'
      this.isShowEdit = true
      this.dialogStatus = 'EDIT'
      setTimeout(() => {
        this.$refs.groupEdit.formQuery.poolName = this.currentData.label
      }, 300)
    },
    /**
     * @description 关闭弹窗
     */
    closeEdit(flag) {
      this.isShowEdit = false
      if (flag === 'refesh') {
        this.getMyFocusGroup()
      }
    }
  }
}
</script>
<style lang="scss" scoped>
.group-list {
  .productAndProperty_virtual {
    height: 100%;
    overflow-y: auto;
    position: relative;
    transition: width 0s !important;
    -moz-transition: width 0s !important; /* Firefox 4 */
    -webkit-transition: width 0s !important; /* Safari and Chrome */
    -o-transition: width 0s !important; /* Opera */
    padding: 5px 0px;
    .tree-content {
      height: 100%;
      margin-right: 8px;
      ::v-deep .el-tree-node__content {
        padding: 20px 0;
        padding-left: 5px !important;
        font-size: 14px;
      }
      .custom-tree-node {
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 14px;
        padding-right: 8px;
        overflow: auto;
        padding-left: 8px;


        ::v-deep .el-button--mini.is-circle {
          padding: 3px;
        }
        ::v-deep .el-button + .el-button {
          margin-left: 7px;
        }
        ::v-deep .el-button.el-button--info {
          background-color: #81a2bb;
        }
      }
    }
    .left_right_button {
      width: 10px;
      background: #f2f2f2;
      height: 100%;
      border-radius: 7.5px;
      position: absolute;
      top: 0px;
      right: 0px;
      z-index: 10;
      cursor: pointer;
    }
  }
  .dd-ellipsis {
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
}
::v-deep .el-tree-node.is-current.is-focusable {
  color: #111 !important;
  font-weight: bold!important;
  background-color: #fcf7f2 !important;
  border-left: 4px solid #e8ad77!important;
}
::v-deep .el-tree-node.is-focusable {
  color: #989898 !important;
  border-left: 4px solid transparent!important;
}
::v-deep .el-tree-node__content:hover {
  background-color: #fcf7f2 !important;
}
.el-button.el-button--info {
  font-size: 14px !important;
  // background-color: #fff !important;
  border: 1px solid #804f2b !important;
  color: #612d10 !important;
  padding: 4px 6px !important;
}
</style>

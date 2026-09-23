<template>
  <el-aside :width="boxWidth" class="productAndProperty_virtual">
    <div class="tradeSeatAdjust" style="height: 100%">
      <div class="product_show_box">
        <el-row type="flex">
          <el-button size="small" type="primary" @click="addGroup">新增分组</el-button>
          <el-button size="small" type="primary" @click="editGroup">重命名</el-button>
        </el-row>
        <el-row>
          <div style="height:100%;margin-top: 10px;">
            <el-tree
              ref="treeRef"
              :props="defaultProps"
              :data="groupData"
              node-key="pid"
              @node-click="handleNodeClick"
            >
              <span slot-scope="{ node, data }" class="custom-tree-node">
                <span>{{ node.label || '' }}</span>
                <span v-if="node.label !== '默认分组'">
                  <el-button type="text" size="mini" @click="deleteGroup(data.pid)">删除</el-button>
                </span>
              </span>
            </el-tree>
          </div>
        </el-row>
      </div>
      <div class="flex_center left_right_button" style="cursor: col-resize" @mousedown="productMove">
        <i :class="left_right_button_icon" style="cursor: pointer" @click="ProductAndProperty_left_right"></i>
      </div>
    </div>
    <group-edit
      ref="groupEdit"
      :title="dialogTitle"
      :is-show-edit="isShowEdit"
      :status="dialogStatus"
      :current-data="currentData"
      @closeedit="closeEdit"
    ></group-edit>
  </el-aside>
</template>
<script>
import commonAPI from '@/api/common.js'
import { delFundPool } from '../scripts/api'
import groupEdit from './group-edit.vue'
export default {
  name: 'ProductList',
  components: {
    groupEdit
  },
  data() {
    return {
      boxWidth: '210px',
      productText: '',
      tableLoading: false,
      tableData: [],
      currentResult: null,
      left_right_button_icon: '',
      tableHeight: 0,
      defaultProps: {
        children: 'children',
        label: 'label'
      },
      groupData: [],
      isShowEdit: false,
      dialogTitle: '',
      dialogStatus: 'ADD',
      currentData: {}
    }
  },
  async mounted() {
    await this.getMyFocusGroup()
    await this.$nextTick(function() {
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
      document.onmousemove = e => {
        // 鼠标按下并移动的事件
        // 用鼠标的位置减去鼠标相对元素的位置，得到元素的位置
        const left = e.clientX - disX
        const top = e.clientY - disY
        // 移动当前元素{
        let boxWidth = 0
        if (left < 25 || left == 25) {
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
      document.onmouseup = e => {
        document.onmousemove = null
        document.onmouseup = null
      }
    },
    // 点击隐藏
    ProductAndProperty_left_right() {
      // 0 关闭 1 开启
      let switchOpen = 1
      var self = this
      if (self.boxWidth != '25px') {
        switchOpen = 0
        self.boxWidth = '25px'
        let ele = document.getElementsByClassName('left_right_button')
        ele[0].style.width = '25px'

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
          this.groupData = groupArr.map(item => {
            return {
              label: item.VC_POOLNAME,
              pid: item.VC_POOLCODE,
              children: []
            }
          })
          this.$nextTick(function() {
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
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          delFundPool(data).then(res => {
            if (res.data.status === 0) {
              this.$message({
                type: 'success',
                message: res.data.message || '删除成功'
              })
              this.getMyFocusGroup()
              this.handleNodeClick(this.groupData[0])
            } else {
              this.$message({
                type: 'error',
                message: res.data.message || '删除失败'
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
      this.$refs.groupEdit.formQuery.poolName = this.currentData.label
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
<style lang="scss">
.productAndProperty_virtual {
  overflow: hidden;
  position: relative;
  transition: width 0s !important;
  -moz-transition: width 0s !important; /* Firefox 4 */
  -webkit-transition: width 0s !important; /* Safari and Chrome */
  -o-transition: width 0s !important; /* Opera */
  padding: 5px 0px;
  // 头部边框
  .vxe-body--column {
    background-size: 0px 100%, 100% 0px !important;
  }

  .keyword-lighten {
    color: #000;
    background-color: #ffff00;
  }

  .tradeSeatAdjust .vxe-table {
    // 禁用头部禁止的标识
    .is--disabled.vxe-cell--checkbox {
      cursor: auto !important;
    }

    .vxe-tree-cell {
      .vxe-cell--checkbox span {
        padding-left: 10px;
      }

      .is--disabled span {
        color: #333 !important;
        padding-left: 0px;
        position: relative;
        left: -15px;
      }

      .is--disabled .vxe-checkbox--icon {
        display: none;
      }
    }

    .vxe-checkbox--checked-icon:after {
      top: 65% !important;
      left: 30% !important;
    }

    .vxe-checkbox--icon:before {
      top: 4px !important;
      left: -4px !important;
    }
  }

  .product_show_box {
    height: 100%;
    //height: calc(100vh - 150px);
  }

  .product_show_box .content_tree {
    height: calc(100vh - 220px);
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

  .product_show_box span {
    padding: 5px;
  }
  .color_c39330 {
    color: #fff;
    background-color: #c39330;
    border-color: #c39330;
  }
  .custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
  }
}
</style>

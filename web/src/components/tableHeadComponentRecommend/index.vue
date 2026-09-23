<template>
  <div>
    <el-dialog :visible.sync="dialogVisible" style="padding: 0px 20px" width="80%" @closed="handleDialogClosed">
      <el-row :gutter="21" justify="center" type="flex" class="standard-form">
        <el-col :span="4" style="border: 1px solid #cccccc; padding: 0px; max-height: 262px; overflow-y: auto">
          <el-tree
            ref="leftTreeData"
            :data="leftTreeData"
            :default-checked-keys="['fundCode']"
            :default-expanded-keys="['jbxx']"
            :render-after-expand="false"
            :filter-node-method="filterNode"
            accordion
            node-key="id"
            show-checkbox
            @node-click="handleNodeClick"
            @check-change="handleLeftTreeNodeClick"
          ></el-tree>
        </el-col>
        <el-col :span="4" style="border: 1px solid #cccccc; padding: 0px; border-left: none; max-height: 262px; overflow-y: auto">
          <el-tree
            ref="centerTreeDataLeft"
            :data="centerTreeDataLeft"
            :default-expanded-keys="['jgxx']"
            :render-after-expand="false"
            accordion
            node-key="id"
            show-checkbox
            @node-click="handleNodeClick"
            @check-change="handleLeftTreeNodeClick"
          ></el-tree>
        </el-col>
        <el-col :span="4" style="border: 1px solid #cccccc; padding: 0px; border-left: none; max-height: 262px; overflow-y: auto">
          <el-tree
            ref="centerTreeDataCenter"
            :data="centerTreeDataCenter"
            :default-expanded-keys="['jzzb']"
            :render-after-expand="false"
            accordion
            node-key="id"
            show-checkbox
            @node-click="handleNodeClick"
            @check-change="handleLeftTreeNodeClick"
          ></el-tree>
        </el-col>
        <el-col :span="4" style="border: 1px solid #cccccc; padding: 0px; border-left: none; max-height: 262px; overflow-y: auto">
          <el-tree
            ref="centerTreeDataRight"
            :data="centerTreeDataRight"
            :default-expanded-keys="['yjzb']"
            :render-after-expand="false"
            accordion
            node-key="id"
            show-checkbox
            @node-click="handleNodeClick"
            @check-change="handleLeftTreeNodeClick"
          ></el-tree>
        </el-col>
        <el-col :span="5" style="border: 1px solid #cccccc; padding: 0px; border-left: none; max-height: 262px; overflow-y: auto">
          <el-tree
            ref="rightTreeData"
            :data="rightTreeData"
            :default-expanded-keys="['qtzb']"
            :render-after-expand="false"
            accordion
            node-key="id"
            show-checkbox
            @node-click="handleNodeClick"
            @check-change="handleLeftTreeNodeClick"
          ></el-tree>
        </el-col>
      </el-row>
      <!--  行列拖拽案例 -->
      <div style="padding-top: 20px" id="standard-table">
        <el-table
          ref="table"
          :cell-style="{ height: '50px', fontSize: '14px' }"
          :header-cell-style="{ color: '#333', height: '54px', background: '#edf3fd!important' }"
          :key="tableKey"
          :data="tableData"
          height="0px;"
          row-key="id"
        >
          <el-table-column v-for="(item, index) in tableHeaerList" :key="item.id" :label="item.label" :prop="item.id" align="center">
            <template slot="header" slot-scope="{ column, $index }">
              <span>{{ column.label }}</span>
              <i v-if="!dontDeleteColumns.includes(item.id)" class="el-icon-close" @click="handleDeleteColumn($index)"></i>
            </template>
          </el-table-column>
        </el-table>
      </div>
      <div style="color: #e98900; margin-top: 10px">*选中指标名称拖动调整顺序</div>
      <div slot="footer" style="text-align: center" class="dialog-footer standard-form">
        <el-button size="small" type="info" plain @click="handleCancel">取 消</el-button>
        <el-button size="small" type="primary" @click="handleSubmit">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import Sortable from 'sortablejs'
import { centerTreeDataCenter, centerTreeDataLeft, centerTreeDataRight, leftTreeData, rightTreeData } from './constant'

export default {
  name: 'Index',
  props: {
    tableColumnSelectorVisible: {
      type: Boolean,
      required: true,
      default: false
    },
    tableColumn: {
      type: Array,
      required: true,
      default: () => {
        return []
      }
    }
  },
  data() {
    return {
      dialogVisible: false,
      leftTreeData: leftTreeData,
      centerTreeDataRight: centerTreeDataRight,
      centerTreeDataLeft: centerTreeDataLeft,
      centerTreeDataCenter: centerTreeDataCenter,
      rightTreeData: rightTreeData,
      tableKey: '', // 拖拽排序后，将mykey赋随机值，使表格重绘（重绘后需重新挂载拖拽监听事件）
      tableData: [],
      tableHeaerList: [],
      dontDeleteColumns: ['fundCode', 'fundFullName', 'companyFullName', 'rankDate', 'options']
      // 动态表头
    }
  },
  computed: {},
  watch: {
    tableColumnSelectorVisible(val) {
      this.dialogVisible = val
      if (this.dialogVisible === true) {
        this.$nextTick(() => {
          this.tableColumn.forEach((item) => {
            this.$refs[item.type].setChecked(item, true)
          })
          this.tableHeaerList = [...this.tableColumn]
          this.columnDrop()
          // this.$refs.leftTreeData.filter('近六月走势')
        })
        this.$forceUpdate()
      }
    }
  },
  beforeUpdate() {
    this.$nextTick(() => {
      // 在数据加载完，重新渲染表格
      this.$refs['table'] ? this.$refs['table'].doLayout() : ''
    })
  },
  mounted() {},
  methods: {
    filterNode(value, data) {
      if (data.label !== value) {
        return true
      } else {
        return false
      }
    },
    handleCancel() {
      this.dialogVisible = false
      this.$emit('dialogclose')
    },
    handleSubmit() {
      this.$emit('submit', this.tableHeaerList)
      this.$emit('dialogclose')
      this.dialogVisible = false
    },
    handleDialogClosed() {
      this.dialogVisible = false
      this.$emit('dialogclose')
    },
    handleLeftTreeNodeClick(node) {
      if (node.label == '基本信息') {
        return
      }
      const selectArr = this.$refs[node.type] ? this.$refs[node.type].getCheckedNodes() : null
      if (selectArr === null) return
      const selectFlag =
        selectArr.length &&
        selectArr.findIndex((item) => {
          return item.id === node.id
        }) !== -1
      if (selectFlag) {
        // 如果 选中了，需要添加到 tableHeadList里面去
        const index = this.tableHeaerList.findIndex((item) => {
          return item.id === node.id
        })
        if (index === -1) {
          this.tableHeaerList.push(node)
        }
      } else {
        // 如果取消勾选了，需要从tableHeadList里面删掉
        const index = this.tableHeaerList.findIndex((item) => {
          return item.id === node.id
        })
        if (index >= 0) {
          this.tableHeaerList.splice(index, 1)
        }
      }
      this.columnDrop()
    },

    /**
     * 行拖拽
     */
    rowDrop() {
      // 要侦听拖拽响应的DOM对象
      const tbody = document.querySelector('.el-table__body-wrapper tbody')
      const _this = this
      Sortable.create(tbody, {
        // 结束拖拽后的回调函数
        onEnd({ newIndex, oldIndex }) {
          console.log('拖动了行，当前序号：' + newIndex)
          const currentRow = _this.tableData.splice(oldIndex, 1)[0]
          _this.tableData.splice(newIndex, 0, currentRow)
          _this.reDrawTable()
        }
      })
    },
    /**
     * 列拖拽
     */
    columnDrop() {
      const _this = this
      const wrapperTr = document.querySelector('.el-table__header-wrapper tr')
      this.sortable = Sortable.create(wrapperTr, {
        animation: 180,
        delay: 0,
        onEnd: (evt) => {
          console.log(evt, 'evt')
          // 跳过显示的列数量，如开头我们用了一个多选框
          const empty = 0
          const oldItem = _this.tableHeaerList[evt.oldIndex - empty]
          this.newCol = evt.newIndex - 1
          if (evt.newIndex <= 4 || evt.oldIndex <= 4) {
            const temp1 = this.tableHeaerList[evt.oldIndex]
            const temp2 = this.tableHeaerList[evt.newIndex]
            this.tableHeaerList[evt.newIndex] = temp2
            this.tableHeaerList[evt.oldIndex] = temp1
            this.$message.closeAll()
            this.$message({
              type: 'warning',
              message: '固定列无法拖动',
              customClass: 'message-warning'
            })
            _this.reDrawTable()
            return
          }
          _this.tableHeaerList.splice(evt.oldIndex - empty, 1)
          _this.tableHeaerList.splice(evt.newIndex - empty, 0, oldItem)
          _this.reDrawTable()
        }
      })
    },
    // 触发表格重绘
    reDrawTable() {
      this.tableKey = Math.random() + new Date()
      this.$nextTick(() => {
        // this.rowDrop()
        this.columnDrop()
        console.log(this.tableHeaerList)
      })
    },

    // 删除列
    handleDeleteColumn(index) {
      const node = this.tableHeaerList[index]
      this.$refs[node.type].setChecked(node, false)
    },
    handleNodeClick() {}
  }
}
</script>
<style lang="scss" scoped>
::v-deep .el-tree-node__expand-icon.is-leaf {
  display: block !important;
}
::v-deep .el-dialog {
  width: 80% !important;
}
</style>

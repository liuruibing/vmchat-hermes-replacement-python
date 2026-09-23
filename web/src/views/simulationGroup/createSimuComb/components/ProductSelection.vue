<template>
  <div>
    <el-row>
      <el-col :span="4">
        <div class="left-dialog">
          <div class="left-title-bg">
            <span>{{ title }}</span>
          </div>
          <el-tree
            ref="tree"
            :data="treeData"
            class="standard-tree"
            :props="defaultProps"
            check-on-click-node
            current-node-key="scsm"
            node-key="id"
            @node-click="handleNodeClick"
          ></el-tree>
        </div>
      </el-col>
      <el-col :span="16" class="center-padding-left">
        <div class="center-dialog">
          <el-form :model="formQuery" class="center-form-bg standard-form">
            <el-input v-model="formQuery.productName" placeholder="基金简称/拼音/备案号" style="width: 180px !important" />
            <el-button :loading="searchLoading" size="small" type="primary" @click="handleSelect">搜索</el-button>
          </el-form>

          <div id="standard-table">
            <el-table
              ref="table"
              :cell-style="{ height: '50px', fontSize: '14px' }"
              :header-cell-style="{ color: '#333', height: '54px', background: '#fafafa!important' }"
              v-loading="searchLoading"
              :data="tableData"
              stripe
              max-height="350px"
              style="width: 100%"
              @select="handleSelectionChange"
            >
              <el-table-column align="center" header-align="center" type="selection" width="55">
                <template slot-scope=""></template>
              </el-table-column>
              <template v-for="item in columns">
                <el-table-column :key="item.key" :align="item.align" :label="item.label" :min-width="item.width" :prop="item.prop" header-align="center" show-overflow-tooltip="">
                  <template slot-scope="scope">
                    <span v-if="item.filter == 'normal'">{{ scope.row[item.prop] | noDataFilter }}</span>
                  </template>
                </el-table-column>
              </template>
            </el-table>
            <Pagination :limit="formQuery.pageSize" :page="formQuery.pageNum" :total="total" @pagination="Pagination"></Pagination>
          </div>
        </div>
      </el-col>
      <el-col :span="4">
        <div class="right-dialog">
          <div class="right-title-bg">
            <span>已选产品</span>
            <span v-if="limit != -1">{{ selectProductStr }}</span>
          </div>
          <draggable v-model="selectListDialog" @end="dragging = false" @start="dragging = true">
            <div v-for="element in selectListDialog" :key="element.id" class="drag-element-style">
              <el-row type="flex" align="middle">
                <el-col :span="20" style="white-space: nowrap; text-overflow: ellipsis; -o-text-overflow: ellipsis; overflow: hidden">
                  {{ element.VC_FUNDNAME }}
                </el-col>
                <el-col :span="4">
                  <i class="el-icon-delete" style="float: right" @click="handleDelete(element)"></i>
                </el-col>
              </el-row>
            </div>
          </draggable>
        </div>
      </el-col>
    </el-row>
    <div style="text-align: center; padding: 20px 0" class="standard-form">
      <el-button size="small" :disabled="active >= 3" :loading="loading" type="primary" @click="handleSubmit">
        {{ btnTxT }}
      </el-button>
    </div>
  </div>
</template>
<script>
import Pagination from '@/components/Pagination'
import draggable from 'vuedraggable'
import commonApi from '@/api/common'
import lodash from 'lodash'

export default {
  components: { Pagination, draggable },
  props: {
    title: {
      type: String,
      required: false,
      default: '产品范围'
    },
    limit: {
      type: Number,
      required: false,
      default: -1
    },
    showTreeKeyArray: {
      type: Array,
      required: true,
      default: () => {
        return []
      }
    },
    selectList: {
      type: Array,
      required: true,
      default: () => {
        return []
      }
    },
    multiple: {
      type: Boolean,
      default: false
    },
    subCombineCode: {
      type: String,
      default: ''
    },
    ddate: {
      type: String,
      default: ''
    },
    pid: {
      type: String,
      default: ''
    },
    active: {
      type: Number,
      default: 0,
      required: true
    }
  },
  data() {
    return {
      btnTxT: '创建模拟组合',
      searchLoading: false,
      formQuery: {
        productName: '',
        pageNum: 1,
        pageSize: 20
      },
      defaultProps: {
        children: 'children',
        label: 'label'
      },
      total: 0,
      selectProductStr: '',
      columns: [
        {
          label: '产品代码',
          prop: 'VC_FUNDCODE',
          align: 'left',
          width: '100px',
          filter: 'normal'
        },
        {
          label: '产品名称',
          prop: 'VC_FUNDNAME',
          align: 'left',
          width: '180px',
          filter: 'normal'
        },
        {
          label: '成立日期',
          prop: 'D_CREATE_DATE',
          align: 'center',
          width: '100px',
          filter: 'normal'
        },
        {
          label: '子策略类型',
          prop: 'VC_STRATEGY',
          align: 'center',
          width: '100px',
          filter: 'normal'
        },
        {
          label: '管理人',
          prop: 'VC_NAME_GLR',
          align: 'left',
          width: '180px',
          filter: 'normal'
        }
      ],
      selectListDialog: [],
      tableData: [],
      treeData: [],
      loading: false
    }
  },
  watch: {
    selectList: {
      handler(val) {
        this.selectListDialog && (this.selectListDialog = [...val]) && (this.selectProductStr = `(${this.selectListDialog.length}/${this.limit})`)
      },
      deep: true,
      immediate: true
    },
    showTreeKeyArray: {
      async handler(val) {
        const treeDataTemp = []
        const sortOrder = ['产品列表', '市场私募', '我的关注', '私有产品']
        const arr = lodash.cloneDeep(val)
        arr.sort((a, b) => sortOrder.indexOf(a) - sortOrder.indexOf(b))
        for (let i = 0; i < arr.length; i++) {
          const item = arr[i]
          if (item == '市场私募') {
            treeDataTemp.push({
              label: '市场私募',
              id: 'scsm',
              templateCode: '328b54c4-1d91-4368-abb8-ced23952ae95'
            })
          } else if (item == '产品列表') {
            treeDataTemp.push({
              label: '产品列表',
              id: 'zstgwb',
              templateCode: '32aad2ac-edf2-4a05-86a2-75b78aa2ba64'
            })
          } else if (item == '私有产品') {
            treeDataTemp.push({
              label: '私有产品',
              id: 'sycp',
              templateCode: 'befbb4e7-c783-4342-b151-b95c4e14f217'
            })
          } else if (item == '我的关注') {
            const params = {}
            params.indexCode = 'f98b1f94-97c7-462d-b7b2-1da0cc1d3fb5'
            const { data } = await commonApi.getDataBysqlCode(params)
            if (data.status === 0) {
              const treeNode = {
                label: '我的关注',
                id: 'wdgz',
                templateCode: '8c7b188e-a185-422e-919c-8f4ad9df4ef1',
                children: []
              }
              if (data.data.length > 0) {
                data.data.forEach((item) => {
                  const temp = {
                    id: item.VC_POOLCODE,
                    label: item.VC_POOLNAME,
                    parentID: 'wdgz',
                    templateCode: '8c7b188e-a185-422e-919c-8f4ad9df4ef1'
                  }
                  treeNode.children.push(temp)
                })
              }
              treeDataTemp.push(treeNode)
            } else {
              this.$message.closeAll()
              this.$message.warning('我的关注，查询失败')
            }
          }
        }
        this.treeData = [...treeDataTemp]
      },
      deep: true,
      immediate: true
    }
  },
  mounted() {
    setTimeout(() => {
      this.handleSelect()
    }, 1500)
  },
  methods: {
    // 处理
    handleNodeClick(node) {
      this.formQuery.pageNum = 1
      this.formQuery.pageSize = 20
      this.handleSelect()
    },
    handleDelete(element) {
      const index = this.selectListDialog.findIndex((item) => item.VC_FUNDCODE === element.VC_FUNDCODE)
      if (index !== -1) {
        this.selectListDialog.splice(index, 1)
      }
      // 删除 表格的数据
      for (let i = 0; i < this.tableData.length; i++) {
        if (element.VC_FUNDCODE === this.tableData[i].VC_FUNDCODE) {
          this.$refs.table.toggleRowSelection(this.tableData[i], false)
          break
        }
      }
      if (this.limit !== -1) {
        this.selectProductStr = `(${this.selectListDialog.length}/${this.limit})`
      }
    },
    // 点击确定按钮
    handleSubmit() {
      if (this.selectListDialog && this.selectListDialog.length) {
        if (this.btnTxT == '保存修改') {
          this.$emit('submitdialog', { data: this.selectListDialog, status: 'update' })
        } else {
          this.btnTxT = '保存修改'
          this.$emit('submitdialog', { data: this.selectListDialog, status: 'add' })
        }
      } else {
        this.$message.warning('请先选择产品')
      }
    },
    // 处理搜索按钮的逻辑
    handleSelect() {
      const nodeClick = this.$refs.tree.getCurrentNode()
      if (!nodeClick) return
      const params = {}
      params.userInput = this.formQuery.productName
      if (nodeClick.id === 'wdgz') {
        const treeNodeArr = this.treeData.find((item) => item.id === nodeClick.id)
        if (treeNodeArr === undefined) {
          params.poolCode = ''
        } else {
          if (treeNodeArr.children && treeNodeArr.children.length > 0) {
            params.poolCode = treeNodeArr.children[0].id
          } else {
            params.poolCode = ''
          }
        }
      } else {
        if (nodeClick.parentID && nodeClick.parentID === 'wdgz') {
          params.poolCode = nodeClick.id
        }
      }
      if (nodeClick.id == 'sycp') {
        params.flag = 'A'
      }
      if (nodeClick.id == 'zstgwb') {
        params.flag = 'B'
      }
      if (nodeClick.id == 'wdgz') {
        params.flag = 'B'
      }
      if (params.poolCode || params.poolCode == 0) {
        params.flag = 'B'
      }
      params.indexCode = nodeClick.templateCode
      params._pageNum = this.formQuery.pageNum
      params._pageSize = this.formQuery.pageSize
      params._pageFlag = true
      this.searchLoading = true
      commonApi
        .getDataBysqlCode(params)
        .then((res) => {
          const { status, data } = res.data
          if (status === 0) {
            this.tableData = data.rows
            this.total = data.total
            if (this.tableData.length > 0) {
              this.handleSameStatus()
            }
          } else {
            this.total = 0
          }
          this.searchLoading = false
        })
        .catch((err) => {
          this.searchLoading = false
          this.total = 0
        })
    },
    // 同步选中状态
    handleSameStatus() {
      if (!this.multiple) {
        if (this.selectListDialog.length > 1) {
          this.selectListDialog = this.selectListDialog.slice(0, 1)
        }
      }
      this.selectListDialog.forEach((item) => {
        const row = this.tableData.find((sitem) => sitem.VC_FUNDCODE === item.VC_FUNDCODE)
        this.$nextTick(() => {
          this.$refs.table && this.$refs.table.toggleRowSelection(row, true)
        })
      })
    },
    Pagination(val) {
      const { page, limit } = val
      this.formQuery.pageNum = page
      this.formQuery.pageSize = limit
      this.handleSelect()
    },
    handleSelectionChange(selection, row) {
      const selected = selection.length && selection.indexOf(row) !== -1
      if (selected) {
        if (!this.multiple) {
          if (this.selectListDialog.length > 0) {
            this.$message.closeAll()
            this.$message.warning('此页面为产品单选')
            // 取消当前勾选
            this.$refs.table.toggleRowSelection(row, false)
            return
          }
        }
        if (this.limit !== -1 && this.selectListDialog.length >= this.limit) {
          this.$message.closeAll()
          this.$message.warning(`产品最多${this.limit}个`)

          // 把tableData里面check状态改为false
          this.$refs.table.toggleRowSelection(row, false)
          return
        }
        this.selectListDialog.push({ ...row })
      } else {
        const index = this.selectListDialog.findIndex((item) => item.VC_FUNDCODE === row.VC_FUNDCODE)
        if (index !== -1) {
          this.selectListDialog.splice(index, 1)
        }
      }

      if (this.limit !== -1) {
        this.selectProductStr = `(${this.selectListDialog.length}/${this.limit})`
      }
    }
  }
}
</script>
<style lang="scss" scoped>
// 隐藏全选框
::v-deep .el-table__header-wrapper .el-checkbox {
  display: none;
}

::v-deep .el-dialog {
  width: 85% !important;
}

::v-deep .el-tree-node__expand-icon.is-leaf {
  display: block !important;
}

::v-deep .el-form {
  width: 100% !important;
}

.left-title-bg {
  line-height: 46px;
  background: #fafafa;

  span {
    margin-left: 5px;
  }
}

.right-title-bg {
  line-height: 46px;
  background: #fafafa;
  padding: 0 10px;
}

.center-form-bg {
  padding: 5px 5px;
  background: #fafafa;
}

.center-padding-left {
  padding-left: 5px;
  padding-right: 5px;
}

.center-dialog::after {
  content: '';
  clear: both;
  display: block;
  height: 0;
  visibility: hidden;
}
.center-dialog,
.right-dialog,
.left-dialog {
  height: 464px;
  overflow: auto;
  border: 1px solid #cccccc;
}
.left-dialog,
.right-dialog {
  background-color: #fff;
}

.dialog-footer-center {
  text-align: center;
}

.drag-element-style {
  padding: 0 10px;
  text-align: left;
  line-height: 30px;
}

.drag-element-style:hover {
  cursor: pointer;
  background: #e6edfc;
  color: #CF7E34;
}

::v-deep .el-button--primary.is-disabled {
  background-color: #ccc;
  border-color: #ccc;
}
::v-deep .el-table--striped .el-table__body tr.el-table__row--striped td {
  background-color: #f9fafe !important;
}

::v-deep .el-table tbody .el-table__row:hover > td {
  background-color: transparent !important;
}

::v-deep .el-table tbody .el-table__row.el-table__row--striped:hover > td {
  background-color: #f9fafe !important;
}
</style>

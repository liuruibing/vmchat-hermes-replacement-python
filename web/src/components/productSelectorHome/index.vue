<template>
  <el-dialog :visible.sync="productSelectDialogVisible" append-to-body width="80%" @close="handleDialogClose">
    <el-row>
      <el-col :span="4">
        <div class="left-dialog">
          <div class="left-title-bg">
            <span>{{ title }}</span>
          </div>
          <el-tree
            ref="tree"
            :current-node-key="defaultCheckedKeys"
            :data="treeData"
            :props="defaultProps"
            check-on-click-node
            node-key="id"
            @node-click="handleNodeClick"
          ></el-tree>
        </div>
      </el-col>
      <el-col :span="16" class="center-padding-left" v-if="multiple">
        <div class="center-dialog">
          <el-form :model="formQuery" class="center-form-bg">
            <el-input v-model="formQuery.productName" placeholder="基金简称/拼音/备案号" style="width: 180px !important" />
            <el-button :loading="searchLoading" size="small" type="primary" @click="handleSelect(true)">搜索</el-button>
          </el-form>
          <el-table ref="table" v-loading="searchLoading" :data="tableData" class="mt10" max-height="350px" style="width: 100%" @select="handleSelectionChange">
            <el-table-column align="center" header-align="center" type="selection" width="55">
              <template slot-scope=""></template>
            </el-table-column>
            <template v-for="item in columns">
              <el-table-column :key="item.key" :align="item.align" :label="item.label" :min-width="item.width" :prop="item.prop" header-align="center">
                <template slot-scope="scope">
                  <span v-if="item.filter == 'normal'">{{ scope.row[item.prop] | noDataFilter }}</span>
                </template>
              </el-table-column>
            </template>
          </el-table>
          <Pagination :limit="formQuery.pageSize" :page="formQuery.pageNum" :total="total" @pagination="Pagination"></Pagination>
        </div>
      </el-col>
      <el-col :span="20" class="center-padding-left" v-else>
        <div class="center-dialog">
          <el-form :model="formQuery" class="center-form-bg standard-form">
            <el-input v-model="formQuery.productName" placeholder="基金简称/拼音/备案号" style="width: 180px !important" />
            <el-button :loading="searchLoading" size="small" type="primary" @click="handleSelect(true)">搜索</el-button>
          </el-form>
          <el-table ref="table" v-loading="searchLoading" :data="tableData" class="mt10" max-height="350px" style="width: 100%" @select="handleSelectionChange">
            <el-table-column align="center" header-align="center" type="selection" width="55">
              <template slot-scope=""></template>
            </el-table-column>
            <template v-for="item in columns">
              <el-table-column :key="item.key" :align="item.align" :label="item.label" :min-width="item.width" :prop="item.prop" header-align="center">
                <template slot-scope="scope">
                  <span v-if="item.filter == 'normal'">{{ scope.row[item.prop] | noDataFilter }}</span>
                </template>
              </el-table-column>
            </template>
          </el-table>
          <Pagination :limit="formQuery.pageSize" :page="formQuery.pageNum" :total="total" @pagination="Pagination"></Pagination>
        </div>
      </el-col>
      <el-col :span="4" v-if="multiple">
        <div class="right-dialog">
          <div class="right-title-bg">
            <span>已选产品</span>
            <span v-if="limit != -1">{{ selectProductStr }}</span>
          </div>
          <draggable v-model="selectListDialog" @end="dragging = false" @start="dragging = true">
            <div v-for="element in selectListDialog" :key="element.id" class="drag-element-style">
              <el-row type="flex" align="middle">
                <el-col :span="20" style="white-space: nowrap; text-overflow: ellipsis; -o-text-overflow: ellipsis; overflow: hidden">
                  {{ element.VC_FUNDNAME || element.VC_FUNDCODE }}
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
    <div slot="footer" class="dialog-footer-center standard-form">
      <el-button size="small" type="info" plain @click="handleDialogClose">取 消</el-button>
      <el-button size="small" type="primary" @click="handleSubmit">确定</el-button>
    </div>
  </el-dialog>
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
    dialogVisible: {
      type: Boolean,
      required: true,
      default: false
    },
    defaultCheckedKeys: {
      type: String,
      required: true,
      default: () => {
        return 'scsm'
      }
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
    }
  },
  data() {
    return {
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
      productSelectDialogVisible: false,
      columns: [
        {
          label: '产品代码',
          prop: 'VC_FUNDCODE',
          align: 'center',
          width: '80px',
          filter: 'normal'
        },
        {
          label: '产品名称',
          prop: 'VC_FUNDNAME',
          align: 'left',
          width: '150px',
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
          width: '120px',
          filter: 'normal'
        }
      ],
      selectListDialog: [],
      tableData: [],
      treeData: []
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
    dialogVisible: {
      handler(val) {
        this.productSelectDialogVisible = val
        if (this.productSelectDialogVisible === true) {
          this.$nextTick(() => {
            this.handleSelect(true)
          })
        }
      },
      deep: true,
      immediate: true
    },
    showTreeKeyArray: {
      async handler(val) {
        const treeDataTemp = []
        const sortOrder = ['单选产品', '产品列表', '管理人旗下产品', '市场私募', '私有产品', '我的关注']
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
          } else if (item == '我的组合') {
            treeDataTemp.push({
              label: '我的组合',
              id: 'wdzh',
              templateCode: '87e2d1c7-c6e4-457f-a664-038457f4e322'
            })
          } else if (item == '私有产品') {
            treeDataTemp.push({
              label: '私有产品',
              id: 'sycp',
              templateCode: 'befbb4e7-c783-4342-b151-b95c4e14f217'
            })
          } else if (item == '单选产品') {
            treeDataTemp.push({
              label: '单选产品',
              id: 'dxcp',
              templateCode: 'b3fe1321-62f8-4d5e-9453-a2fb8c794ffc'
            })
          } else if (item == '管理人旗下产品') {
            treeDataTemp.push({
              label: '管理人旗下产品',
              id: 'glrqxcp',
              templateCode: '4cf7d988-44e0-4a55-a3d7-94e9cc3e496b'
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
              this.$message({
                type: 'warning',
                message: `我的关注，查询失败`,
                customClass: 'message-warning'
              })
            }
          }
        }
        this.treeData = [...treeDataTemp]
      },
      deep: true,
      immediate: true
    },
    defaultCheckedKeys: {
      handler(val) {
        if ((val && val === 'zstgwb') || (val === 'wdgz' && (this.$route.path.includes('/jxbg/dcpbg/') || this.$route.path.includes('/jxbg/reportTemplate/reportTemplate')))) {
          const i = this.columns.findIndex((v) => v.prop === 'D_CREATE_DATE')
          const authObj = {
            label: '权限等级',
            prop: 'VC_FUND_GRANT',
            align: 'center',
            width: '100px',
            filter: 'normal'
          }
          this.columns.splice(Number(i + 1), 0, authObj)
        }
      },
      deep: true,
      immediate: true
    }
  },
  mounted() {
    if (this.limit !== -1) {
      this.selectProductStr = `(${this.selectListDialog.length}/${this.limit})`
    }
  },
  methods: {
    //报告工坊、投后绩效报告： 左侧 产品列表（B）、我的关注（B）
    //穿透页面： 左侧 产品列表（C）、我的关注（C）、私有产品（B）
    judgeFlag(id) {
      // 判断是投后的穿透页面的
      if (this.$route.path.includes('/thgl/zhctfx')) {
        if (id == 'zstgwb') {
          return 'C'
        } else if (id == 'wdgz') {
          return 'C'
        } else if (id == 'sycp') {
          return 'B'
        }
      }
      // 判断是投后的绩效报告的
      else if (this.$route.path.includes('/jxbg')) {
        if (id == 'zstgwb') {
          return 'B'
        } else if (id == 'wdgz') {
          return 'B'
        }else if (id == 'sycp') {
          return 'A'
        }
      }
      // 判断是投后的报告工坊的
      else if (this.$route.path.includes('/jxbg/reportTemplate/reportTemplate')) {
        if (id == 'zstgwb') {
          return 'C'
        } else if (id == 'glrqxcp') {
          return 'A'
        } else if (id == 'sycp') {
          return 'A'
        } else if (id == 'wdgz') {
          return 'B'
        }
      }
      return ''
    },

    // 处理
    handleNodeClick(node) {
      /** 如果是产品列表添加权限等级列 */
      if (
        node.id === 'zstgwb' ||
        ((this.$route.path.includes('/jxbg/dcpbg/') || this.$route.path.includes('/jxbg/reportTemplate/reportTemplate')) && (node.id === 'wdgz' || node.parentID === 'wdgz'))
      ) {
        if (this.columns.findIndex((g) => g.prop === 'VC_FUND_GRANT') < 0) {
          const i = this.columns.findIndex((v) => v.prop === 'D_CREATE_DATE')
          const authObj = {
            label: '权限等级',
            prop: 'VC_FUND_GRANT',
            align: 'center',
            width: '100px',
            filter: 'normal'
          }
          this.columns.splice(Number(i + 1), 0, authObj)
        }
      } else {
        const i = this.columns.findIndex((v) => v.prop === 'VC_FUND_GRANT')
        if (i > 0) {
          this.columns.splice(i, 1)
        }
      }
      this.formQuery.pageNum = 1
      this.formQuery.pageSize = 20
      this.handleSelect(true)
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
      this.$emit('submitdialog', this.selectListDialog)
    },
    // 处理搜索按钮的逻辑
    handleSelect(flag) {
      flag ? (this.formQuery.pageNum = 1) : ''
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
      let judgeReturn = this.judgeFlag(nodeClick.parentID || nodeClick.id)
      if (judgeReturn) {
        params.flag = judgeReturn
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
      this.handleSelect(false)
    },
    handleSelectionChange(selection, row) {
      const selected = selection.length && selection.indexOf(row) !== -1
      if (selected) {
        if (!this.multiple) {
          if (this.selectListDialog.length > 0) {
            this.$refs.table.toggleRowSelection(selection[0], false)
            this.selectListDialog = []
            // this.$message.closeAll()
            // this.$message.warning('此页面为产品单选')
            // // 取消当前勾选
            // this.$refs.table.toggleRowSelection(row, false)
            // return
          }
        }
        if (this.limit !== -1 && this.selectListDialog.length >= this.limit) {
          this.$message.closeAll()
          this.$message({
            type: 'warning',
            message: `产品最多${this.limit}个`,
            customClass: 'message-warning'
          })

          //把tableData里面check状态改为false
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
    },
    handleDialogClose() {
      this.productSelectDialogVisible = false
      this.$emit('closedialog')
    }
  }
}
</script>
<style lang="scss" scoped>
::v-deep .el-button.el-button--primary {
  // background-color: #e03d3e !important;
  color: #fff !important;
  // border-color: transparent !important;
}
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
  height: 500px;
  overflow: auto;
  border: 1px solid #cccccc;
}

.dialog-footer-center {
  text-align: center;
}

.drag-element-style {
  text-align: left;
  line-height: 20px;
}

.drag-element-style:hover {
  cursor: pointer;
  background: #e6edfc;
  color: #CF7E34;
}
</style>

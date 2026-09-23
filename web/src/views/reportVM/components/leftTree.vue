<!-- 条件树，指标数 -->
<template>
  <div class="left-tree" id="reportVMLeftTree">
    <!--          style="height: calc(50% - 15px); overflow-y: auto;margin-top: 10px;" -->
    <el-row class="left-header">
      <span style="margin-left: 10px; color: #e2a971">{{ mode | modeToStr }}</span>
      <div class="search_button_com">
        <el-link type="primary"><span style="color: #e2a971; font-size: 14px; font-weight: 600" @click="handleSaveBtnClick">保存</span></el-link>
        <el-link type="primary">
          <span
            style="font-size: 14px; font-weight: 600; color: #e2a971"
            @click="
              () => {
                $emit('return')
              }
            "
          >
            返回
          </span>
        </el-link>
      </div>
    </el-row>
    <el-input style="width: 100% !important" size="small" v-model="filterText" placeholder="输入关键字进行过滤"></el-input>
    <!--    <el-tree-->
    <!--      ref="conditionTreeRef"-->
    <!--      :data="reportVMConditionData"-->
    <!--      default-expand-all-->
    <!--      node-key="vcCode"-->
    <!--      :highlight-current="true"-->
    <!--      :check-on-click-node="true"-->
    <!--      @node-click="handleConditionClick"-->
    <!--    ></el-tree>-->

    <el-tree
      ref="indexTreeRef"
      :data="reportVMIndexData"
      :default-checked-keys="indexTreeDefaultCheckedArray"
      default-expand-all
      show-checkbox
      check-on-click-node
      class="standard-tree"
      :filter-node-method="filterNode"
      @check-change="handleIndexCheckChange"
      node-key="vcCode"
    ></el-tree>
    <el-dialog
      :title="dialogTitle"
      :visible="dialogVisible"
      width="30% !important"
      center
      @close="
        () => {
          dialogVisible = false
        }
      "
    >
      <el-form ref="dialogFormRef" class="standard-form" :model="dialogForm" :rules="dialogRules" label-width="120px">
        <el-form-item label="报告名称" prop="templateName">
          <el-input v-model="dialogForm.templateName" size="small"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <span class="standard-form">
          <el-button type="primary" size="small" @click="handleSaveSetting">提 交</el-button>
          <el-button
            size="small"
            type="info"
            plain
            @click="
              () => {
                dialogVisible = false
              }
            "
          >
            取 消
          </el-button>
        </span>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import pageApi from '../api/index'
import commonFun from '@/filters/new_common'
import { mapGetters } from 'vuex'

export default {
  name: 'LeftTree',
  filters: {
    modeToStr(val) {
      if (val === 'edit') {
        return '编辑模式'
      } else {
        return '新增模式'
      }
    }
  },
  data() {
    return {
      filterText: '', //过滤文本
      vcReportType: null,
      indexTreeDefaultCheckedArray: [],
      currentConditionNode: null,
      mode: 'add',
      dialogTitle: '新增模式',
      dialogVisible: false,
      dialogForm: {
        templateName: '',
        fVmType: '',
        templateId: ''
      },
      dialogRules: {
        templateName: [{ required: true, message: '请输入报告名称', trigger: 'blur' }],
        fVmType: [{ required: true, message: '请选择VM报告类型', trigger: 'blur' }]
      },
      leftTreeData: []
    }
  },
  computed: {
    ...mapGetters(['reportVMConditionData', 'reportVMIndexData', 'reportVMCurrentData'])
  },
  async mounted() {},
  watch: {
    filterText(val) {
      this.$refs.indexTreeRef.filter(val)
    }
  },
  methods: {
    filterNode(value, data) {
      if (!value) return true
      return data.label.indexOf(value) !== -1
    },
    setReportInfo(info) {
      if (info.templateName) {
        this.dialogForm.templateName = info.templateName
      }
      if (info.vcReportType) {
        this.dialogForm.vcReportType = info.vcReportType
      }
      if (info.fVmType) {
        this.dialogForm.fVmType = info.fVmType
      }
      if (info.templateId) {
        this.dialogForm.templateId = info.templateId
      }
    },
    /**
     * @Description: 初始化模式
     * @author Liu Rui Bing
     * @date 2024/4/29
     */
    setMode(reportInfo, type) {
      if (type === 'add') {
        this.mode = 'add'
        this.dialogForm.templateName = reportInfo.vcTemplatEname
        this.dialogForm.fVmType = reportInfo.fType
        this.dialogForm.templateId = ''
        this.dialogForm.vcReportType = reportInfo.vcReportType
      } else {
        this.mode = 'edit'
        this.dialogForm.templateName = reportInfo.vcTemplatEname
        this.dialogForm.fVmType = reportInfo.fType
        this.dialogForm.templateId = reportInfo.fTemplateID
        this.dialogForm.vcReportType = reportInfo.vcReportType
      }
    },
    async setTreeNode(val) {
      // 判断一下 左侧数据是否已经请求好了
      if (this.reportVMConditionData.length === 0 || this.reportVMIndexData.length === 0) {
        await this.getLeftTree()
      }
      // 处理 所有的 val的 data值
      for (let i = 0; i < val.length; i++) {
        let findObj = this.leftTreeData.find((item) => item.vcCode === val[i].vcCode)
        if (findObj) {
          val[i] = findObj
        }
      }
      setTimeout(() => {
        // this.setConditionTree(val)
        this.setIndexTree(val)
      }, 0)
    },
    /**
     * @Description: 设置条件树
     * @author Liu Rui Bing
     * @date 2024/4/29
     */
    setConditionTree(val) {
      if (this.reportVMConditionData && this.reportVMConditionData[0] && this.reportVMConditionData[0].children) {
        for (let i = 0; i < val.length; i++) {
          let findObj = this.reportVMConditionData[0].children.find((item) => item.vcCode === val[i].vcCode)
          if (findObj) {
            this.$refs.conditionTreeRef.setCurrentKey(findObj.vcCode)
            this.currentConditionNode = findObj
            this.$emit('conditionNodeClick', { data: findObj, type: 'addNode' })
            break
          }
        }
      }
    },

    /**
     * @Description: 设置指标树
     * @author Liu Rui Bing
     * @date 2024/4/29
     */
    setIndexTree(val) {
      let indexCpArray = _.cloneDeep(val)
      if (this.currentConditionNode) {
        let findIndex = indexCpArray.findIndex((item) => item.vcCode === this.currentConditionNode.vcCode)
        if (findIndex !== -1) {
          indexCpArray.splice(findIndex, 1)
        }
      }
      this.$store.commit('SET_CURRENT_TREE_DATA', indexCpArray)

      let defaultCheckedArray = []
      for (let i = 0; i < indexCpArray.length; i++) {
        defaultCheckedArray.push(indexCpArray[i].vcCode)
      }
      this.indexTreeDefaultCheckedArray = defaultCheckedArray
    },

    handleConditionClick(data, node, self) {
      if (this.currentConditionNode && this.currentConditionNode.id === data.id) {
        // 相同节点被点击，取消选择
        this.$refs.conditionTreeRef.setCurrentKey(null)
        this.currentConditionNode = null
        this.$emit('conditionNodeClick', { data, type: 'delNode' })
      } else {
        // 设置当前节点并保存
        this.$refs.conditionTreeRef.setCurrentKey(data.id)
        this.currentConditionNode = data
        this.$emit('conditionNodeClick', { data, type: 'addNode' })
      }
    },
    handleSaveBtnClick() {
      if (this.mode === 'edit') {
        this.dialogVisible = '编辑模式'
        this.dialogTitle = '编辑模式'
      } else {
        this.dialogVisible = '新增模式'
        this.dialogTitle = '新增模式'
      }
      this.dialogVisible = true
    },
    /**
     * @Description: 保存报告
     * @author Liu Rui Bing
     * @date 2024/4/28
     */
    handleSaveSetting() {
      if (this.mode === 'edit') {
        this.$refs.dialogFormRef.validate((valid) => {
          if (valid) {
            let params = Object.assign({}, this.dialogForm)
            params.indexInfo = []
            // 判断是否满足 保存的条件
            if (this.reportVMCurrentData && this.reportVMCurrentData.length > 0) {
              if (this.currentConditionNode) {
                params.indexInfo.push({ indexCode: this.currentConditionNode.vcCode, f_order: 0 })
                for (let i = 0; i < this.reportVMCurrentData.length; i++) {
                  params.indexInfo.push({ indexCode: this.reportVMCurrentData[i].vcCode, f_order: i + 1 })
                }
              } else {
                for (let i = 0; i < this.reportVMCurrentData.length; i++) {
                  params.indexInfo.push({ indexCode: this.reportVMCurrentData[i].vcCode, f_order: i })
                }
              }
              params.type = '1'
              pageApi.editSave(params).then((res) => {
                let { status, message } = res.data
                if (status === 200) {
                  this.$message.closeAll()
                  this.$message({
                    type: 'success',
                    message: message || '编辑成功',
                    customClass: 'message-success'
                  })
                  this.dialogVisible = false
                } else {
                  this.$message.closeAll()
                  this.$message({
                    type: 'warning',
                    message: message || '编辑失败',
                    customClass: 'message-warning'
                  })
                }
              })
            } else {
              this.$message.closeAll()
              this.$message({
                type: 'warning',
                message: '报表指标不能为空',
                customClass: 'message-warning'
              })
              return
            }
          } else {
            this.$message.closeAll()
            this.$message({
              type: 'warning',
              message: '请按照提示修改',
              customClass: 'message-warning'
            })
            return
          }
        })
      } else {
        this.$refs.dialogFormRef.validate((valid) => {
          if (valid) {
            let params = Object.assign({}, this.dialogForm)
            params.indexInfo = []
            // 判断是否满足 保存的条件
            if (this.reportVMCurrentData && this.reportVMCurrentData.length > 0) {
              if (this.currentConditionNode) {
                params.indexInfo.push({ indexCode: this.currentConditionNode.vcCode, f_order: 0 })
                for (let i = 0; i < this.reportVMCurrentData.length; i++) {
                  params.indexInfo.push({ indexCode: this.reportVMCurrentData[i].vcCode, f_order: i + 1 })
                }
              } else {
                for (let i = 0; i < this.reportVMCurrentData.length; i++) {
                  params.indexInfo.push({ indexCode: this.reportVMCurrentData[i].vcCode, f_order: i })
                }
              }
              params.type = '1'
              pageApi.addSave(params).then((res) => {
                let { status, message } = res.data
                if (status === 200) {
                  this.$message.closeAll()
                  this.$message({
                    type: 'success',
                    message: message || '保存成功',
                    customClass: 'message-success'
                  })
                  this.dialogVisible = false
                } else {
                  this.$message.closeAll()
                  this.$message({
                    type: 'warning',
                    message: message || '保存失败',
                    customClass: 'message-warning'
                  })
                }
              })
            } else {
              this.$message.closeAll()
              this.$message({
                type: 'warning',
                message: '报表指标不能为空',
                customClass: 'message-warning'
              })
              return
            }
          } else {
            this.$message.closeAll()
            this.$message({
              type: 'warning',
              message: '请按照提示修改',
              customClass: 'message-warning'
            })
            return
          }
        })
      }
    },
    /**
     * @Description: 点击 指标树的处理函数
     * @author Liu Rui Bing
     * @date 2024/4/26
     */
    handleIndexCheckChange(data, checked, indeterminate) {
      if (data && !data.children) {
        if (checked) {
          this.$emit('checkedIndex', { data: data, type: 'addIndex' })
        } else {
          this.$emit('checkedIndex', { data: data, type: 'delIndex' })
        }
      }
    },
    /**
     * @Description: 获取 左侧 指标树
     * @author Liu Rui Bing
     * @date 2024/4/26
     */
    getLeftTree(vcReportType = null) {
      if (vcReportType !== null) {
        this.vcReportType = vcReportType
      }
      return new Promise((resolve, reject) => {
        const params = {}
        params.vcReportType = this.vcReportType
        if (params.vcReportType == null) {
          return
        }
        pageApi.indexTree(params).then((res) => {
          const { status, data, message } = res.data
          if (status === 200) {
            // 转换成树形结构
            data.forEach((item) => {
              if (item.vcParentCode == '' || item.vcParentCode == null || item.vcParentCode == undefined) {
                item.vcParentCode = '0'
              }
              item.label = item.vcIndexName
              item.value = item.vcCode
              item.id = item.vcCode
            })
            this.leftTreeData = _.cloneDeep(data)
            const treeData = commonFun.converTreeData(data, '0', 'vcParentCode', 'vcCode', 'vcCode')
            if (treeData.data.length > 0) {
              this.$store.dispatch('setConditionTreeData', [treeData.data[0]])
              if (treeData.data.length > 1) {
                treeData.data.shift()
                this.$store.dispatch('setIndexTreeData', [...treeData.data])
              } else {
                this.$store.dispatch('setIndexTreeData', [])
              }
            } else {
              this.$store.dispatch('setConditionTreeData', [])
              this.$store.dispatch('setIndexTreeData', [])
            }
          }
          resolve()
        })
      })
    },
    handleCheckChange(data, checked, indeterminate) {
      const checkedArray = this.$refs.indexTreeRef.getCheckedNodes(true)
      this.$emit('indexNodeClick', checkedArray)
    },

    /**
     * @Description: 取消勾选删除的checkbox
     * @author Liu Rui Bing
     * @date 2024/4/28
     */
    handleCancelCheckNode(node) {
      this.$refs.indexTreeRef.setChecked(node.id, false)
    }
  }
}
</script>
<style lang="scss">
@import '@/styles/variables.scss';

#reportVMLeftTree {
  .el-tree-node .is-current .el-tree-node__content,
  .is-current > .el-tree-node__content {
    background-color: $reportVM-bg-color !important;
    color: #f79a2a;
  }
  .el-tree-node__content:hover {
    background: rgba(0, 0, 0, 0.4) !important;
    opacity: 0.4;
  }

  .el-dialog__header {
    text-align: left !important;
  }

  .el-dialog__title {
    font-size: 16px !important;
    color: #d6572c !important;
    font-weight: 600 !important;
  }
}
</style>
<style scoped lang="scss">
@import '@/styles/variables.scss';
/* 修改 checkbox 勾选后行的字体颜色 */
::v-deep .is-checked {
  color: #e2a971; /* 将红色替换为你想要的颜色 */
}
//::v-deep .el-tree-node__content:hover {
//  background: #000000 !important;
//  opacity: 0.4;
//}
::v-deep .el-tree-node__content > label.el-checkbox {
  margin-top: 4px;
}
.left-tree {
  height: 100%;
  width: 100%;
  overflow-y: auto;
  padding: 15px 5px 15px 5px;
  //border: 1px solid #ebeef5;
  //box-shadow: 0 2px 12px 0 rgba(0, 0, 0, .1);
  border-radius: 15px;
  background-color: $reportVM-model-bg;

  .el-tree {
    background-color: unset;
  }

  .left-header {
    margin-bottom: 15px;
    font-size: 16px;
    color: #0f65dd;
    font-weight: 600;
  }
}
</style>

<template>
  <div class="assess-template">
    <el-input
      v-model="filterText"
      size="small"
      placeholder="输入关键字过滤"
      clearable
      prefix-icon="el-icon-search"
      style="margin-bottom: 15px; width: 300px"
    />
    <div>
      <el-scrollbar class="content_tree">
        <el-tree
          ref="TreeData"
          :data="TreeData"
          :props="defaultProps"
          :show-checkbox="true"
          node-key="id"
          :indent = 30
          v-loading="treeLoading"
          @check="handleCheckChange"
          :default-checked-keys="checkedArr"
          :default-expand-all="true"
          :filter-node-method="filterNode"
        ></el-tree>
      </el-scrollbar>
    </div>
    <div style="text-align: center" class="dialog-footer standard-form">
      <el-button size="small" type="primary" @click="handleSaveZtrees">
        提 交
      </el-button>
      <el-button size="small" type="info" plain @click="cancel">取 消</el-button>
    </div>
  </div>
</template>

<script>
import { authorization, userZtrees } from '../scripts/api'
import fun from "@/filters/common";
export default {
  name: 'userZtrees',
  props: {
    curZtreesRow: {
      type: Object,
      default: () => {}
    }
  },
  watch: {
    filterText(val) {
      this.$refs.TreeData.filter(val) // 触发树节点过滤
    },
    curZtreesRow: {
      handler(val) {
        if (val && val.fundCode) {
          this.formData.fundCode = val.fundCode || ''
          this.handleSearchZtrees()
        } else {
          this.$message.error('缺少产品代码参数')
        }
      },
      deep: true,
      immediate: true
    }
  },

  data() {
    return {
      filterText: '', // 新增搜索关键词绑定
      // form表单绑定
      formData: {
        fundCode: '',
        userIds:[]
      },
      // tree数据渲染字段
      defaultProps: {
        children: "children",
        label: "label"
      },
      TreeData: [],
      treeLoading: false,
      checkedArr: [],


    }
  },

  methods: {

    handleSearchZtrees() {
      const params = Object.assign({}, this.formData)
      this.treeLoading = true
      userZtrees(params)
        .then((res) => {
          if (res.data.data) {
            let {data} = res.data;
            this.TreeData = fun.TreeDataPId(data, 0).data;
            this.checkedArr = []
            data.map(item => {
              if (item.checked == 'true' && !item.children) {
                this.checkedArr.push(item.id)
              }
            })
          }
          this.treeLoading = false

        })
        .catch((e) => {
          this.treeLoading = false
        })
    },
    filterNode(value, data) {
      if (!value) return true;

      // 当前节点匹配
      const nodeMatch = data.label.includes(value);
      // 递归检查子节点
      const childMatch = (data.children || []).some(child => this.filterNode(value, child));

      return nodeMatch || childMatch;
    },
    // 多用户点击事件
    handleCheckChange(data, checked, indeterminate) {
      this.formData.userIds = [];
      checked.checkedNodes.forEach(item => {
        if (!item.children && item.userId) {
          this.formData.userIds.push(item.userId);
        }
      });
      console.log(this.formData)
    },
    /**
     * @description 取消按钮关闭弹窗
     */
    cancel() {
      this.$emit('closeDialog', 'NO_REFESH')
    },

    handleSaveZtrees() {
      const params = Object.assign({}, this.formData)
      authorization(params)
        .then((res) => {
          if (res.data.status === 0) {
            this.$message.success(res.data.message || '保存成功')
            this.$emit('closeDialog', 'REFESH')
          } else {
            this.$message.error(res.data.message || '保存失败')
          }
        })
        .catch((e) => {
        })

    }
  }
}
</script>

<style lang="scss" scoped>
.assess-template {
  .template {
    ::v-deep .el-input {
      width: 250px !important;
    }
  }
  .content_tree {
    height: 500px;
  }
  ::v-deep .el-scrollbar__wrap {
    overflow-y: auto !important; /* 仅垂直方向滚动 */
    overflow-x: hidden !important; /* 隐藏水平滚动条 */
    height: 100%;
  }
}
</style>

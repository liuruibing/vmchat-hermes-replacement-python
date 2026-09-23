<template>
  <el-dialog
    :visible.sync="groupVisible"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    :destroy-on-close="true"
    :title="title"
    custom-class="group-edit-manager"
    width="20%"
    @close="close"
  >
    <span slot="title">
      <span class="title-txt">{{ title }}</span>
    </span>
    <el-row>
      <el-col :span="24">
        <el-form ref="editForm" style="width: 100% !important" :inline="true" :model="formQuery" :rules="rules" class="standard-form" label-width="auto">
          <el-form-item label="分组名称" prop="poolName">
            <el-input v-model="formQuery.poolName" placeholder="请输入" size="small" />
          </el-form-item>
        </el-form>
      </el-col>
      <el-col style="text-align: center" class="standard-form">
        <el-button type="primary" size="small" @click="savePool('editForm')">保 存</el-button>
      </el-col>
    </el-row>
  </el-dialog>
</template>

<script>
import { saveManagerPool, renameManagerPool } from '../scripts/api'
export default {
  name: 'GroupEdit',
  props: {
    currentData: {
      type: Object,
      default: () => {}
    },
    status: {
      type: String,
      default: '',
      required: true
    },
    isShowEdit: {
      type: Boolean,
      default: false,
      required: true
    },
    title: {
      type: String,
      default: '',
      required: true
    }
  },
  data() {
    return {
      groupVisible: false,
      formQuery: {
        poolName: ''
      },
      rules: {
        poolName: [{ required: true, message: '请填写分组名称', trigger: 'blur' }]
      }
    }
  },
  watch: {
    isShowEdit: {
      handler(val) {
        this.groupVisible = val
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    /**
     * @description 新增/边界分组
     */
    savePool(formName) {
      this.$refs[formName].validate(async (valid) => {
        if (valid) {
          if (this.status === 'ADD') {
            try {
              const res = await saveManagerPool(this.formQuery)
              if (res.data.status === 0) {
                this.$message({
                  type: 'success',
                  message: res.data.message || '新增成功',
                  customClass: 'message-success'
                })
                this.resetForm()
                this.$emit('closeedit', 'refesh')
              } else {
                this.$message({
                  type: 'warning',
                  message: res.data.message || '新增失败',
                  customClass: 'message-warning'
                })
              }
            } catch (e) {
              this.$message({
                type: 'error',
                message: '新增失败',
                customClass: 'message-error'
              })
            }
          } else {
            const data = {
              poolCode: this.currentData.pid,
              poolName: this.formQuery.poolName
            }
            try {
              const res = await renameManagerPool(data)
              if (res.data.status === 0) {
                this.$message({
                  type: 'success',
                  message: res.data.message || '修改成功',
                  customClass: 'message-success'
                })
                this.resetForm()
                this.$emit('closeedit', 'refesh')
              }
            } catch (e) {
              this.$message({
                type: 'error',
                message: '修改失败',
                customClass: 'message-error'
              })
            }
          }
        } else {
          return false
        }
      })
    },
    /**
     * @description 关闭弹窗
     */
    close() {
      for (const key in this.formQuery) {
        this.formQuery[key] = ''
      }
      this.$emit('closeedit', 'norefesh')
    },
    /**
     * @description 重置表单
     */
    resetForm() {
      for (const key in this.formQuery) {
        this.formQuery[key] = ''
      }
    }
  }
}
</script>

<style lang="scss" scoped>
::v-deep .el-dialog {
  width: 20% !important;
}
.group-edit-manager {
  .title-txt {
    color: #e03d3e !important;
    padding-left: 10px;
    font-size: 14px;
  }
}
</style>

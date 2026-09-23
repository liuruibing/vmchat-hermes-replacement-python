<template>
  <div class="focus-manager">
    <el-dialog
      :visible.sync="focusVisible"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :destroy-on-close="true"
      :title="title"
      width="40%"
      @close="close"
    >
      <el-row v-if="page === 'MYFOCUS'">
        <el-col :span="24" :offset="1">
          <el-radio-group v-model="currentType">
            <el-radio label="remove">移动至</el-radio>
            <el-radio label="copy">复制至</el-radio>
          </el-radio-group>
        </el-col>
      </el-row>
      <el-row style="margin-top: 20px">
        <el-col :span="24" :offset="1">
          <el-radio-group v-model="currentRadio">
            <el-radio v-for="item in focusOptions" :key="item.VC_POOLCODE" :label="item.VC_POOLCODE">
              {{ item.VC_POOLNAME }}
            </el-radio>
          </el-radio-group>
        </el-col>
      </el-row>
      <el-row style="margin-top: 20px">
        <el-col :span="24" style="text-align: center">
          <el-button type="primary" size="small" @click="submitFocus">确定</el-button>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
import commonAPI from '@/api/common.js'
import { handleFocusGroup, handleBatchFocusGroup, removeMyConcern } from './api'
export default {
  name: 'Foucs',
  props: {
    // 全市场or我的关注
    page: {
      type: String,
      default: '',
      required: true
    },
    // 弹窗标题
    title: {
      type: String,
      default: '',
      required: true
    },
    // 是否展示弹窗
    isShowFocus: {
      type: Boolean,
      default: false,
      required: true
    },
    // 当前管理人数据
    selectRowData: {
      type: Array,
      default: () => [],
      required: true
    },
    currentGroupId: {
      type: String,
      default: '000000'
    }
  },
  data() {
    return {
      focusVisible: false,
      focusOptions: [],
      currentRadio: '000000',
      currentType: 'remove'
    }
  },
  watch: {
    isShowFocus: {
      handler(val) {
        this.focusVisible = val
        if (val) {
          this.getFocusType()
        }
      },
      deep: true,
      immediate: true
    },
    currentGroupId: {
      handler(val) {
        this.currentRadio = val
      },
      immediate: true
    }
  },
  methods: {
    /**
     * @description 我的关注-分组查询-管理人
     */
    async getFocusType() {
      const data = {
        indexCode: '6e1fd4c2-3c95-4d25-8d71-111b32bfa7e7'
      }
      try {
        const res = await commonAPI.getDataBysqlCode(data)
        if (res.data.status === 0) {
          this.focusOptions = res.data.data || []
          if(this.title === '关注') {
            if(this.focusOptions && this.focusOptions.length > 0) {
              this.currentRadio = this.focusOptions[0].VC_POOLCODE
            }
          }
        }
      } catch (e) {
        this.focusOptions = []
      }
    },
    /**
     * @description 保存关注分组-管理人
     */
    async submitFocus() {
      const params = {
        poolCode: this.currentRadio
      }
      if (this.title === '关注') {
        params.mgrCode = this.selectRowData[0].company_id
        try {
          const res = await handleFocusGroup(params)
          if (res.data.status === 0) {
            this.$message({
              type: 'success',
              message: res.data.message || '关注成功'
            })
            this.$emit('updateFocusStatus', 'refesh')
          }
        } catch (e) {
          this.$message({
            type: 'success',
            message: '关注失败'
          })
        }
      } else if (this.title === '移动分组') {
        const params = {
          poolCode: this.currentGroupId,
          newPoolCode: this.currentRadio,
          type: this.currentType
        }
        const fundCodeArr = this.selectRowData.map(item => item.company_id)
        params.mgrCodes = fundCodeArr.join(',')
        try {
          const res = await removeMyConcern(params)
          if (res.data.status === 0) {
            this.$message({
              type: 'success',
              message: res.data.message || '成功'
            })
            this.$emit('updateFocusStatus', 'refesh')
          }
        } catch (e) {
          this.$message({
            type: 'success',
            message: '失败'
          })
        }
      } else {
        const managerCodeArr = this.selectRowData.map(item => item.company_id)
        params.mgrCodes = managerCodeArr.join(',')
        try {
          const res = await handleBatchFocusGroup(params)
          if (res.data.status === 0) {
            this.$message({
              type: 'success',
              message: res.data.message || '关注成功'
            })
            this.$emit('updateFocusStatus', 'refesh')
          } else {
            this.$message({
              type: 'error',
              message: res.data.message || '关注失败'
            })
          }
        } catch (e) {
          this.$message({
            type: 'success',
            message: '关注失败'
          })
        }
      }
    },
    /**
     * @description 关闭弹窗
     */
    close() {
      this.currentRadio = '000000'
      this.currentType = 'remove'
      this.$emit('updateFocusStatus', 'norefesh')
    }
  }
}
</script>

<style lang="scss" scoped>
.focus-manager {
  ::v-deep .el-dialog__title {
    font-weight: normal !important;
    color: #333 !important;
    padding-left: 10px;
  }
  ::v-deep .el-radio__input.is-checked .el-radio__inner {
    border-color: #e03d3e;
    background: #e03d3e;
  }
  ::v-deep .el-radio.is-checked .el-radio__label {
    color: #333 !important;
  }
  ::v-deep .el-radio .el-radio__label {
    color: #333 !important;
    font-size: 14px !important;
  }
  ::v-deep .el-radio__label {
    display: inline-block;
    width: 120px;
    margin-bottom: 15px;
  }
}
</style>

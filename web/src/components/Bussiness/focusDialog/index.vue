<template>
  <div class="focus">
    <el-dialog :close-on-click-modal="false" :close-on-press-escape="false" :destroy-on-close="true" :title="title" :visible.sync="focusVisible" width="40%" @close="close">
      <div class="standard-form">
        <el-row v-if="page === 'MYFOCUS'">
          <el-col :offset="1" :span="24">
            <el-radio-group v-model="currentType">
              <el-radio label="remove">移动至</el-radio>
              <el-radio label="copy">复制至</el-radio>
            </el-radio-group>
          </el-col>
        </el-row>
        <el-row style="margin-top: 20px">
          <el-col :offset="1" :span="24">
            <el-radio-group v-model="currentRadio">
              <el-radio v-for="item in focusOptions" :key="item.VC_POOLCODE" :label="item.VC_POOLCODE">
                {{ item.VC_POOLNAME }}
              </el-radio>
            </el-radio-group>
          </el-col>
        </el-row>
      </div>
      <el-row style="margin-top: 20px" class="dialog-footer standard-form">
        <el-col :span="24" style="text-align: center">
          <el-button size="small" type="primary" @click="submitFocus">提 交</el-button>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
import commonAPI from '@/api/common.js'
import { handleBatchFocusGroup, handleFocusGroup, removeMyConcern } from './api'

export default {
  name: 'Foucs',
  props: {
    // 全市场or我的关注
    page: {
      type: String,
      default: ''
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
    // 私募or外包
    soucre: {
      type: String,
      default: ''
    },
    // 当前产品数据
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
      currentRadio: 0,
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
     * @description 我的关注-分组查询
     */
    async getFocusType() {
      const data = {
        indexCode: 'f98b1f94-97c7-462d-b7b2-1da0cc1d3fb5'
      }
      try {
        const res = await commonAPI.getDataBysqlCode(data)
        if (res.data.status === 0) {
          this.focusOptions = res.data.data || []
          if (this.title === '关注') {
            if (this.focusOptions && this.focusOptions.length > 0) {
              this.currentRadio = this.focusOptions[0].VC_POOLCODE
            }
          }
        }
      } catch (e) {
        this.focusOptions = []
      }
    },
    /**
     * @description 保存关注分组
     */
    async submitFocus() {
      const params = {
        flag: this.soucre,
        poolCode: this.currentRadio
      }
      if (this.title === '关注') {
        params.fundCode = this.selectRowData[0].fundCode
        params.flag = this.selectRowData[0].source
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
        params.myConcernList = this.selectRowData.map(item => {
          return {
            fundCode: item.fundCode,
            flag: item.source
          }
        })
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
        const data = this.selectRowData.map(item => {
          return {
            fundCode: item.fundCode,
            flag: item.source
          }
        })
        delete params.flag
        params.myConcernList = data
        // params.flags = this.selectRowData.map(item => item.source).join(',')
        try {
          const res = await handleBatchFocusGroup(params)
          if (res.data.status === 0) {
            this.$message({
              type: 'success',
              message: res.data.message || '关注成功'
            })
            this.$emit('updateFocusStatus', 'refesh')
          } else if (res.data.status === -1) {
            let fundNameArr = res.data.message.split(':')[1].split(';')
            fundNameArr = fundNameArr.filter(item => item !== 'null' && item !== '')
            if (fundNameArr.length == 0) {
              return
            }
            const newSelectRowData = []
            this.selectRowData.forEach(element => {
              if (!fundNameArr.includes(element.fundName)) {
                newSelectRowData.push(element)
              }
            })
            if (newSelectRowData.length) {
              this.selectRowData = newSelectRowData
              this.submitFocus()
            } else {
              this.$message({
                type: 'warning',
                message: '所选产品全部已被关注'
              })
            }
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
.focus {
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

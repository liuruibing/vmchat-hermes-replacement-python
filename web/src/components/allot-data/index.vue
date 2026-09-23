<template>
  <div class="allot-data">
    <el-form
      ref="allotForm"
      style="margin: 0 auto; "
      :inline="true"
      :model="formQuery"
      :rules="rules"
      label-width="auto"
    >
      <el-row type="flex" justify="center">
        <el-form-item label="需求处理人" prop="poolName">
          <el-select
            v-model="formQuery.poolName"
            size="small"
            clearable
            filterable
            placeholder="请选择"
            @change="changeSelect"
          >
            <el-option
              v-for="item in selectMemberOptions"
              :key="item.value"
              :label="item.assignerName"
              :value="item.assignerId"
            />
          </el-select>
        </el-form-item>
      </el-row>
    </el-form>
    <el-row class="mt10">
      <el-col style="text-align: center" class="standard-form">
        <el-button type="primary" size="small" @click="submit">提 交</el-button>
        <el-button type="info" plain size="small" @click="close">取 消</el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import pageAPI from './scripts/api'
export default {
  name: 'AllotData',
  props: {
    allotData: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      formQuery: {
        poolName: ''
      },
      rules: {
        poolName: [{ required: true, message: '请选择需求处理人', trigger: 'change' }]
      },
      selectMemberOptions: [],
      selectObj: {}
    }
  },
  mounted() {
    this.querySelectMember()
  },
  methods: {
    /**
     * @description 关闭分配窗口
     */
    close(status) {
      this.$emit('closeDialog', status)
    },
    /**
     * @description 监听下拉变化
     */
    changeSelect(val) {
      const obj = this.selectMemberOptions.find(item => item.assignerId === val)
      if (JSON.stringify(obj) !== '{}') {
        this.selectObj = obj
      }
    },
    /**
     * @description 保存分配人员
     */
    submit() {
      this.$refs.allotForm.validate(valid => {
        if (valid) {
          let data = {}
          if (this.allotData.length > 1) {
            // 批量
            data = Object.assign(
              {
                ids: this.allotData.map(item => item.id).join(',')
              },
              this.selectObj
            )
          } else {
            // 单个
            data = Object.assign({ ids: this.allotData[0].id.toString() }, this.selectObj)
          }
          pageAPI.updateAssigner(data).then(res => {
            const { status, message } = res.data
            if (status === 0) {
              this.$message.success('操作成功')
              this.close('REFESH')
            } else {
              this.$message.success(message || '操作失败')
            }
          })
        } else {
          return false
        }
      })
    },
    querySelectMember() {
      pageAPI.selectAssigner().then(res => {
        const { status, data } = res.data
        if (status === 0) {
          this.selectMemberOptions = data || []
        }
      })
    }
  }
}
</script>

<style></style>

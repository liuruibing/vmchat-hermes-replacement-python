<template>
  <div class="select_table">
    <el-select
      ref="select"
      v-model="names"
      :placeholder="placeholder"
      popper-class="select-table-popper"
      :size="size"
      :title="names"
      :clearable="clearable"
      :disabled="disabled"
      @clear="selectClear"
      @focus="$refs.xTable.clearFilter()"
    >
      <el-option style="display: none !important" label="item.label" value="item.value"></el-option>
      <div class="tableDiv" :style="{ width: `${width}` }">
        <vxe-table
          :data="data"
          border
          auto-resize
          size="mini"
          ref="xTable"
          max-height="240"
          :filter-config="{ showIcon: false }"
          highlight-current-row
          @current-change="currentChangeEvent"
        >
          <vxe-table-column
            v-for="(item, index) in Columns"
            :key="index"
            :field="item.prop"
            :title="item.label"
            :width="item.width"
            :filters="[{ data: '' }]"
            :filter-method="customStringFilterMethod"
            show-overflow
          >
            <template slot="header" slot-scope="{ column }">
              <template v-if="item.filter === 'select'">
                <vxe-select v-model="column.filters[0].data" :placeholder="item.label" clearable transfer filterable @change="filterEvent(column.filters[0])">
                  <vxe-option v-for="(i, index) in (item.filterOption || [])" :key="index" :value="i" :label="i"></vxe-option>
                </vxe-select>
              </template>
              <template v-else>
                <vxe-input
                  type="text"
                  v-for="(option, index) in column.filters"
                  :key="index"
                  v-model="option.data"
                  @change="filterEvent(option)"
                  :placeholder="item.label"
                  clearable
                ></vxe-input>
              </template>
            </template>
          </vxe-table-column>
        </vxe-table>
      </div>
    </el-select>
  </div>
</template>

<script>
export default {
  name: 'SelectTable',
  props: {
    // 输入框尺寸
    size: {
      type: String,
      default: ''
    },
    // 是否可清空
    clearable: {
      type: Boolean,
      default: false
    },
    // 是否禁用
    disabled: {
      type: Boolean,
      default: false
    },
    // 列表数据-必填
    data: {
      type: Array,
      default: () => {
        return []
      },
      required: true
    },
    // 列表表头-必填
    Columns: {
      type: Array,
      required: true
    },
    // 决定v-model的值(一般需要必填)
    valueField: {
      type: String,
      default: 'value'
    },
    // 显示在文本框的字段(一般需要必填)
    labelField: {
      type: String,
      default: 'label'
    },
    // 提示语(可不填)
    placeholder: {
      type: String,
      default: ''
    },
    width: {
      type: String,
      default: '650px'
    },
    value: {}
  },
  // v-model
  model: {
    prop: 'value',
    event: 'sendData'
  },
  data() {
    return {
      names: '', //input 值
      values: ''
    }
  },
  watch: {
    value(data) {
      this.values = data
      this.getNames()
    },
    // 列表数据 监听, 获取input框拼接值
    data(data) {
      // 获取names
      this.getNames()
    }
  },
  mounted() {
    this.values = JSON.parse(JSON.stringify(this.value))
    // 获取names
    this.getNames()
  },
  methods: {
    // 行选中
    currentChangeEvent({ row }) {
      this.$emit('sendData', row[this.valueField])
      this.$emit('change', row)
      this.names = row[this.labelField]
      this.$refs.select.blur()
    },
    // 清空
    selectClear() {
      this.$emit('sendData', '')
      this.$emit('change', {})
      this.$emit('clear')
      this.$refs.xTable.clearCurrentRow()
    },
    // names
    getNames() {
      const tableData = this.data
      if (tableData.length) {
        let obj = tableData.find((item) => {
          return item[this.valueField] == this.values
        })
        if (obj) {
          // 默认选中
          this.$refs.xTable.setCurrentRow(obj)
          this.names = obj[this.labelField] || JSON.parse(JSON.stringify(this.values))
        } else {
          this.names = JSON.parse(JSON.stringify(this.values))
        }
      } else {
        // this.names = JSON.parse(JSON.stringify(this.values));
      }
    },
    // 筛选
    customStringFilterMethod({ option, row, column }) {
      if (option.data) {
        return row[column.property] && row[column.property].toLowerCase().indexOf(option.data) > -1
      }
      return true
    },
    // 筛选
    filterEvent(option) {
      // console.log(option)
      const xTable = this.$refs.xTable
      // // 设置为选中状态
      option.checked = true
      // // 修改条件之后，需要手动调用 updateData 处理表格数据
      xTable.updateData()
    }
  }
}
</script>

<style lang="scss">
.select-table-popper {
  .el-select-dropdown__item {
    display: none !important;
  }
  .el-select-dropdown__list {
    padding: 0 !important;
  }
}
// tooltip 层级
.vxe-table--tooltip-wrapper {
  z-index: 9999 !important;
}
/* 确保下拉框的样式中的 z-index 值足够高 */
.vxe-select--panel {
  z-index: 9999 !important; /* 设置一个高的 z-index 值 */
}
</style>

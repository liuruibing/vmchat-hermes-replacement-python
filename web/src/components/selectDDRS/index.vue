<template>
  <div class="select_table">
    <el-select
      ref="select"
      v-model="name"
      :clearable="clearable"
      :disabled="disabled"
      :placeholder="placeholder"
      :size="size"
      :title="name"
      popper-class="select-table-popper"
      @clear="selectClear"
      @visible-change="handleVisibleChange"
      :automatic-dropdown="isFocus"
      @focus="
        () => {
          isFocus = true;
        }
      "
    >
      <el-option
        label="item.label"
        style="display: none !important"
        value="item.value"
      >
      </el-option>
      <div
        :style="{ width: `${width}`, height: '250px;' }"
        class="tableDiv"
        style="position: relative; z-index: 1"
      >
        <i
          class="el-icon-close"
          style="
            position: absolute;
            right: 5px;
            top: 10px;
            font-size: 22px;
            cursor: pointer;
          "
          @click="handleCloseSelect"
        ></i>
        <report-template
          ref="reportTemplateRef"
          :currencyReportPageData="reportConfig"
          :formCountTemplate="formCount"
          @radioChange="handleEmitRadioChange"
          @DIMCDE="handleDIMCDE"
        ></report-template>
      </div>
      <div
        style="
          position: fixed;
          top: 0px;
          left: 0px;
          height: 100%;
          width: 100%;
          z-index: 0;
        "
      ></div>
    </el-select>
  </div>
</template>

<script>
import reportTemplate from "./reportTemplate";

export default {
  name: "SelectDDRS",
  components: { reportTemplate },
  props: {
    formCount: {
      type: Object,
      default: () => {},
    },
    reportConfig: {
      type: Object,
      default: "",
    },
    // 决定v-model的值(一般需要必填)
    valueField: {
      type: String,
      default: "code",
    },
    // 显示在文本框的字段(一般需要必填)
    labelField: {
      type: String,
      default: "name",
    },
    // 输入框尺寸
    size: {
      type: String,
      default: "",
    },
    // 是否可清空
    clearable: {
      type: Boolean,
      default: true,
    },
    // 是否禁用
    disabled: {
      type: Boolean,
      default: false,
    },
    // 提示语(可不填)
    placeholder: {
      type: String,
      default: "",
    },
    width: {
      type: String,
      default: "700px",
    },
    value: {},
  },
  // v-model
  model: {
    prop: "value",
    event: "sendData",
  },
  data() {
    return {
      isFocus: false,
      name: "", //input 值
      code: "",
    };
  },
  watch: {},
  mounted() {
    this.name =
      this.formCount[`${this.valueField}_NAME`] ||
      this.formCount[`${this.valueField}`];
    this.code = this.formCount[`${this.valueField}`];
  },
  methods: {
    handleDIMCDE() {
      this.$message.closeAll();
      this.$message.warning(`字段[${this.placeholder}] 缺少DIMCDE，DIMNME`);
    },
    handleCloseSelect() {
      this.isFocus = false;
      this.$refs.select.blur();
    },
    handleVisibleChange(val) {
      if (val === false && this.isFocus) {
        this.$refs.select.focus();
        this.isFocus = true;
      } else if (val === false) {
        this.isFocus = false;
      }
    },
    handleEmitRadioChange(row) {
      this.$emit(
        "sendData",
        row.DIM_CDE !== undefined ? row.DIM_CDE : row.DIMCDE
      );
      // this.name = row[this.labelField];
      this.name = row.DIM_CDE !== undefined ? row.DIM_CDE : row.DIMCDE;
      this.isFocus = false;
      this.$refs.select.blur();
    },
    // 清空
    selectClear() {
      this.$emit("sendData", "");
      this.$emit("change", {});
      this.$emit("clear");
      // this.$refs.xTable.clearRadioRow();
      this.$refs.reportTemplateRef.clearRadioRow();
    },
    // name
    getNames() {
      const tableData = this.data;
      if (tableData.length) {
        let obj = tableData.find((item) => {
          return item[this.valueField] == this.code;
        });
        if (obj) {
          // 默认选中
          this.$refs.xTable.setCurrentRow(obj);
          this.name =
            obj[this.labelField] || JSON.parse(JSON.stringify(this.code));
        } else {
          this.name = JSON.parse(JSON.stringify(this.code));
        }
      } else {
      }
    },
    // 筛选
    customStringFilterMethod({ option, row, column }) {
      if (option.data) {
        return (
          row[column.property] &&
          row[column.property].toLowerCase().indexOf(option.data) > -1
        );
      }
      return true;
    },
    // 筛选
    filterEvent(option) {
      // console.log(option);
      const xTable = this.$refs.xTable;
      // // 设置为选中状态
      option.checked = true;
      // // 修改条件之后，需要手动调用 updateData 处理表格数据
      xTable.updateData();
    },
  },
};
</script>
<style lang="scss">
.el-select-dropdown__wrap {
  max-height: 500px !important;
}
</style>

<style lang="scss" scoped>
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

// 滚动条样式
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
  background-color: #f5f5f5;
}

::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(153, 151, 151, 0.3);
  border-radius: 10px;
  background-color: #f5f5f5;
}

::-webkit-scrollbar-thumb {
  border-radius: 10px;
  -webkit-box-shadow: inset 0 0 6px rgba(153, 150, 150, 0.3);
  background-color: #ddd;
}
</style>

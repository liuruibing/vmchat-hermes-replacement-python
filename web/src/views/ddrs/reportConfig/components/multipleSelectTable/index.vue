<template>
  <div class="multiple_select_table">
    <!-- style="width: 100%" -->
    <vxe-pulldown ref="xDown3" destroy-on-close :transfer="isTransfer">
      <template slot-scope="props">
        <!-- style="width: 100% !important" -->
        <el-input
          size="small"
          class="cursor_pointer"
          :placeholder="placeholder"
          :disabled="disabled"
          readonly
          v-model="names"
          :title="names"
          :suffix-icon="isShow ? 'el-icon-arrow-up' : 'el-icon-arrow-down'"
          @click.native="deptogglePanel($event)"
        ></el-input>
      </template>
      <template slot="dropdown" slot-scope="props">
        <div ref="tableList">
          <div class="treeDiv" :style="{ width: `${width}` }">
            <vxe-table
              border
              auto-resize
              size="mini"
              ref="xTable"
              max-height="150"
              :filter-config="{ showIcon: false }"
              :data="data"
              @checkbox-all="selectAllEvent"
              @checkbox-change="selectChangeEvent"
              :checkbox-config="{
                checkMethod: checCheckboxkMethod,
                checkStrictly: checkStrictly,
                trigger: 'row',
                highlight: true,
              }"
            >
              <vxe-table-column
                type="checkbox"
                width="40"
                align="center"
              ></vxe-table-column>
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
              </vxe-table-column>
            </vxe-table>
          </div>
        </div>
      </template>
    </vxe-pulldown>
  </div>
</template>

<script>
export default {
  name: "MultipleSelectTable",
  // checkboxAll
  // checkboxChange
  props: {
    isTransfer: {
      type: Boolean,
      default: false,
    },
    // 列表数据-必填
    data: {
      type: Array,
      default: () => {
        return [];
      },
      required: true,
    },
    // 列表表头-必填
    Columns: {
      type: Array,
      required: true,
    },
    // v-model 数组保存的字段(一般需要必填)
    valueField: {
      type: String,
      default: "id",
    },
    // 显示在文本框的字段(一般需要必填)
    labelField: {
      type: String,
      default: "Name",
    },
    // 提示语(可不填)
    placeholder: {
      type: String,
      default: "",
    },
    checkStrictly: {
      type: Boolean,
      default: false,
    },
    // 是否禁用
    disabled: {
      type: Boolean,
      default: false,
    },
    // 禁用选项
    checCheckboxkMethod: {
      type: Function,
      default: ({ row }) => {
        return row;
      },
    },
    /* 使用示例：
    :checCheckboxkMethod="checCheckboxkMethod"
    ...
    methods:{
      ...
      checCheckboxkMethod({row}){
        //只可选择行数据有 email字段 的数据
        return row.email
      }
    }

    */

    width: {
      type: String,
      default: "650px",
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
      names: "", //input 值
      values: [],
      tableRoleMultipleSelection: [], //保存勾选数组
      isShow: false,
    };
  },
  watch: {
    value(data) {
      this.values = data || [];
      this.getNames();
    },
    // 列表数据 监听, 获取input框拼接值
    data(data) {
      this.getNames();
    },
  },
  mounted() {
    try {
      this.values = JSON.parse(JSON.stringify(this.value || []));
      this.getNames();
    } catch (e) {}
  },
  methods: {
    // 点击input 控制table显示隐藏
    deptogglePanel(event) {
      if (this.disabled) return;
      this.$refs.xDown3.togglePanel();
      // 表格数据勾选
      this.$nextTick(() => {
        this.data.forEach((row) => {
          if (this.values.includes(row[this.valueField])) {
            this.$refs.xTable.setCheckboxRow(row, true);
          }
        });
      });
    },
    // 全选事件
    selectAllEvent({ checked, records }) {
      this.$emit("checkboxAll", { checked, records });
      this.tableRoleMultipleSelection = records;
      this.sureRoleData();
    },
    // 勾选事件
    selectChangeEvent({ checked, records }) {
      this.$emit("checkboxChange", { checked, records });
      this.tableRoleMultipleSelection = records;
      this.sureRoleData();
    },
    // 数据处理
    sureRoleData() {
      this.values = [];
      this.names = "";

      if (this.tableRoleMultipleSelection.length == 0) {
        this.$emit("sendData", this.values);
        return;
      }
      let Selects = this.tableRoleMultipleSelection;
      let Name = "";
      for (let i = 0; i < Selects.length; i++) {
        // 获取数组数据 -- 根据 this.valueField 的值来决定
        this.values.push(Selects[i][this.valueField]);
        Name += Selects[i][this.labelField] + ",";
      }
      // input框赋值
      this.names = Name.slice(0, Name.length - 1);
      // 抛出v-model 数组数据
      this.$emit("sendData", this.values);
    },
    getNames() {
      let Selects = [];
      this.values.forEach((item) => {
        this.data.forEach((ite) => {
          if (ite[this.valueField] == item) {
            Selects.push(ite);
          }
        });
      });
      let Name = "";
      for (let i = 0; i < Selects.length; i++) {
        Name += Selects[i][this.labelField] + ",";
      }
      this.names = Name.slice(0, Name.length - 1);
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

<style lang="scss" scoped>
.multiple_select_table {
  ::v-deep .el-input--small .el-input__inner {
    height: 30px !important;
    line-height: 30px !important;
  }
  .cursor_pointer {
    .el-input__inner {
      cursor: pointer;
    }
  }
  .treeDiv {
    border: 1px solid #ccc;
    border-radius: 5px;
    overflow: hidden;
    position: absolute;
    // top:80px;
    left: -1px;
    z-index: 9999 !important;
    width: 650px;
    //  overflow: auto;
    // max-height: 230px;
    .el-table {
      border: 1px solid #ccc;
      border-radius: 6px;
      overflow: auto;
    }
    .el-table td {
      padding: 4px 0;
    }
    background-color: rgb(241, 239, 239);
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
}
</style>

<style lang="scss" scoped>
::v-deep .vxe-table--render-default .vxe-body--row.row--checked,
.vxe-table--render-default .vxe-body--row.row--radio {
  background-color: #ffffff !important;
  color: #409eff !important;
}
</style>

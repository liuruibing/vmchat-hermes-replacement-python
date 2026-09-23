<template>
  <div class="multiple_select_table">
    <vxe-pulldown ref="xDown3" style="width:100%;" destroy-on-close>
      <template slot="default" slot-scope="scope">
        <el-input
          size="small"
          class="cursor_pointer"
          style="width: 100% !important;"
          :placeholder="placeholder"
          readonly
          v-model="names"
          :suffix-icon="showTree ? 'el-icon-arrow-up' : 'el-icon-arrow-down'"
          @click.native="deptogglePanel($event)"
        ></el-input>
    </template>
    <template slot="dropdown" slot-scope="scope">
    <div ref="tableList">
      <div class="treeDiv" :style="{width:`${width}`}">
        <vxe-table
          border
          auto-resize
          size="mini"
          ref="xTable"
          max-height="250"
          :filter-config="{ showIcon: false }"
          :data="data"
          @checkbox-all="selectAllEvent"
          @checkbox-change="selectChangeEvent"
          :checkbox-config="{ checkMethod: checCheckboxkMethod, checkStrictly: checkStrictly }"
          :cell-class-name="cellClassName"
          :header-cell-class-name="headerCellClassName"
        >
          <vxe-table-column type="checkbox" width="40"></vxe-table-column>
          <vxe-table-column
            v-for="(item, index) in Columns"
            :key="index"
            :field="item.prop"
            :title="item.label"
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
  // checkboxAll
  // checkboxChange
  props: {
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
    idField: {
      type: String,
      default: "id",
    },
    // 显示在文本框的字段(一般需要必填)
    nameField: {
      type: String,
      default: "Name",
    },
    // 提示语(可不填)
    placeholder: {
      type: String,
      default: "",
    },
    checkStrictly:{
      type: Boolean,
      default: false,
    },
    // 禁用选项
    checCheckboxkMethod:{
      type:Function,
      default:({row})=>{
        return row
      }
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
    
    width:{
      type: String,
      default: "650px",
    },
    idss: {},
  },
  model: {
    prop: "idss",
    event: "sendData",
  },
  data() {
    return {
      num: 0,
      num2: 0,
      names: "",
      ids: [],
      tableRoleMultipleSelection: [],
      showTree: false,
    };
  },
  watch: {
    idss(data) {
      this.num++;
      if (this.num) {
        this.ids = JSON.parse(JSON.stringify(this.idss || []));
        let Selects = [];
        this.ids.forEach((item) => {
          this.data.forEach((ite) => {
            if (ite[this.idField] == item) {
              Selects.push(ite);
            }
          });
        });
        let Name = "";
        for (let i = 0; i < Selects.length; i++) {
          // this.ids.push(Selects[i][this.idField]);
          Name += Selects[i][this.nameField] + ",";
        }
        this.names = Name.slice(0, Name.length - 1);
      }
    },
    data(data) {
      this.num2++;
      if (this.num2) {
        let Selects = [];
        this.ids.forEach((item) => {
          this.data.forEach((ite) => {
            if (ite[this.idField] == item) {
              Selects.push(ite);
            }
          });
        });
        let Name = "";
        for (let i = 0; i < Selects.length; i++) {
          // this.ids.push(Selects[i][this.idField]);
          Name += Selects[i][this.nameField] + ",";
        }
        this.names = Name.slice(0, Name.length - 1);
      }
    },
    showTree(data){
      // console.log(data);
    }
  },
  mounted() {
    this.ids = JSON.parse(JSON.stringify(this.idss));
    let Selects = [];
    this.ids.forEach((item) => {
      this.data.forEach((ite) => {
        if (ite[this.idField] == item) {
          Selects.push(ite);
        }
      });
    });
    let Name = "";
    for (let i = 0; i < Selects.length; i++) {
      // this.ids.push(Selects[i][this.idField]);
      Name += Selects[i][this.nameField] + ",";
    }
    this.names = Name.slice(0, Name.length - 1);
  },
  methods: {
    cellClassName({ row, rowIndex, column, columnIndex }) {
      return "vxe-cell-class-name";
    },
    headerCellClassName({ column, columnIndex }) {
      return "vxe-header-cell-class-name";
    },
    // 点击input 阻止冒泡 控制table显示隐藏
    deptogglePanel(event) {
      // event || (event = window.event);
      // event.stopPropagation
      //   ? event.stopPropagation()
      //   : (event.cancelBubble = true);
      // this.showTree ? this.tableHide() : this.tableShow();
      // console.log(this.showTree);
      this.$refs.xDown3.togglePanel();
      this.showTree ? this.tableHide() : this.tableShow();
    },
    tableHide() {
      this.showTree = false;
      document.addEventListener("click", this.tableHideList, false);
      this.$nextTick(() => {
        this.data.forEach((row) => {
          if (this.ids.includes(row[this.idField])) {
            this.$refs.xTable.setCheckboxRow(row, true);
          }
        });
      });
    },
    tableHideList(e) {
      if (this.$refs.tableList && !this.$refs.tableList.contains(e.target)) {
        this.tableHide();
      }
    },
    tableShow() {
      this.showTree = true;
      document.addEventListener("click", this.tableHideList, false);

      this.$nextTick(() => {
        this.data.forEach((row) => {
          if (this.ids.includes(row[this.idField])) {
            this.$refs.xTable.setCheckboxRow(row, true);
          }
        });
      });
    },
    selectAllEvent({ checked, records }) {
      this.$emit("checkboxAll", { checked, records });
      this.tableRoleMultipleSelection = records;
      this.sureRoleData();
    },
    selectChangeEvent({ checked, records }) {
      this.$emit("checkboxChange", { checked, records });
      this.tableRoleMultipleSelection = records;
      this.sureRoleData();
    },
    sureRoleData() {
      this.ids = [];
      this.names = "";

      if (this.tableRoleMultipleSelection.length == 0) {
        // this.$message({
        //   message: "请至少选择一条",
        //   type: "warning",
        // });
        this.$emit("sendData", this.ids);
        return;
      }
      let Selects = this.tableRoleMultipleSelection;
      let Name = "";
      for (let i = 0; i < Selects.length; i++) {
        this.ids.push(Selects[i][this.idField]);
        Name += Selects[i][this.nameField] + ",";
      }
      this.names = Name.slice(0, Name.length - 1);
      this.$emit("sendData", this.ids);
      // this.showTree = false
    },
    customStringFilterMethod({ option, row, column }) {
      if (option.data) {
        return (
          // XEUtils.toValueString(row[column.property])
          row[column.property] &&
          row[column.property].toLowerCase().indexOf(option.data) > -1
        );
      }
      return true;
    },
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
.multiple_select_table {
  .cursor_pointer{
    .el-input__inner{
      cursor: pointer;
    }
  }
  .treeDiv {
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
}
</style>
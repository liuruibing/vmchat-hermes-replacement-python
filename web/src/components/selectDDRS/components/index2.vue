<template>
  <div class="select_contacts" @click.stop="">
    <el-select
      ref="inputFocus"
      popper-class="select_xlk"
      class="select_contacts_input"
      style="width: 100%"
      @remove-tag="remove_tag"
      @focus="inputFocus"
      multiple
      v-model="slValue"
    >
      <!-- <el-option style="display: none" label="11" value="value"> </el-option> -->
      <el-option
        style="display: none"
        v-for="item in tableList"
        :key="item.id"
        :label="item.contactName"
        :value="item.id"
      ></el-option>
    </el-select>
    <!-- <el-input ref="inputFocus" @focus='inputFocus' multiple v-model="slValue"  clearable></el-input> -->
    <div v-show="isTableSelect" class="selectTableStyle">
      <vxe-table
        ref="xTable"
        max-height="300"
        size="mini"
        row-id="id"
        border
        auto-resize
        show-overflow="tooltip"
        :tooltip-config="{ showAll: true }"
        :cell-class-name="cellClassName"
        :header-cell-class-name="headerCellClassName"
        :filter-config="{ showIcon: false }"
        :data="tableList"
        :checkbox-config="{ checkMethod: checCheckboxkMethod, checkRowKeys: defaultSelecteRows }"
        @checkbox-all="selectAllEvent"
        @checkbox-change="selectChangeEvent"
      >
        <vxe-table-column type="checkbox" width="40"></vxe-table-column>
        <vxe-table-column
          field="contactName"
          :filters="[{ data: '' }]"
          :filter-method="customStringFilterMethod"
        >
          <template slot="header" slot-scope="{ column }">
            <vxe-input
              type="text"
              v-for="(option, index) in column.filters"
              :key="index"
              v-model="option.data"
              @change="filterEvent(option)"
              placeholder="姓名"
              clearable
            ></vxe-input>
          </template>
        </vxe-table-column>
        <vxe-table-column
          field="organization"
          :filters="[{ data: '' }]"
          :filter-method="customStringFilterMethod"
        >
          <template slot="header" slot-scope="{ column }">
            <vxe-input
              type="text"
              v-for="(option, index) in column.filters"
              :key="index"
              v-model="option.data"
              @change="filterEvent(option)"
              placeholder="机构"
              clearable
            ></vxe-input>
          </template>
        </vxe-table-column>
        <!-- <vxe-table-column
          field="institutionCode"
          :filters="[{ data: '' }]"
          :filter-method="customEqualFilterMethod"
          :formatter="formatter"
        >
          <template slot="header" slot-scope="{ column }">
            <vxe-input
              type="text"
              v-for="(option, index) in column.filters"
              :key="index"
              v-model="option.data"
              @change="filterEvent(option)"
              placeholder="机构"
              clearable
            ></vxe-input>
          </template>
          <template slot="default" slot-scope="{ row }">
            <span>{{getInitName(row.institutionCode, "orgTrustship") | noDataFilter}}</span>
          </template>
        </vxe-table-column> -->
        <vxe-table-column
          field="email"
          :filters="[{ data: '' }]"
          :filter-method="customStringFilterMethod"
        >
          <template slot="header" slot-scope="{ column }">
            <vxe-input
              type="text"
              v-for="(option, index) in column.filters"
              :key="index"
              v-model="option.data"
              @change="filterEvent(option)"
              placeholder="邮箱"
              clearable
            ></vxe-input>
          </template>
        </vxe-table-column>
        <vxe-table-column
          field="phone"
          :filters="[{ data: '' }]"
          :filter-method="customStringFilterMethod"
        >
          <template slot="header" slot-scope="{ column }">
            <vxe-input
              type="text"
              v-for="(option, index) in column.filters"
              :key="index"
              v-model="option.data"
              @change="filterEvent(option)"
              placeholder="手机号码"
              clearable
            ></vxe-input>
          </template>
        </vxe-table-column>
      </vxe-table>
    </div>
  </div>
</template>

<script>
import commonApi from "../api/common";
import $ from "jquery";
import pageApi from "../api/calendarList";
export default {
  props: ["modelValue", "width", "defaultValue"],
  model: {
    prop: "modelValue",
    event: "sendData",
  },
  watch: {
    modelValue(data) {
      if (data.length) {
        // this.checked(data);

        this.slValue = JSON.parse(JSON.stringify(data));
      } else {
        this.slValue = [];
      }
      // console.log('this.slValue',data);
    },
  },
  data() {
    return {
      tableList: [],
      tableListTemp: [],
      slValue: [],
      isTableSelect: false,
      orgTrustshipArr: [],
      institutionCodeList:[],
      defaultSelecteRows:[],
      flag: true,
    };
  },
  mounted() {
    // this.slValue=['aaa','bbb']
    let that = this;
    $("body").on("click", () => {
      this.tableList = this.tableListTemp;
      that.isTableSelect = false;
    });
    this.getContactList();
    this.getDeptInfoSel();
  },
  // activated(){
  //   console.log('aaaaaa');
  // },
  // deactivated(){},
  methods: {
    cellClassName({}) {
      return "vxe-cell-class-name";
    },
    headerCellClassName({}) {
      return "vxe-header-cell-class-name";
    },
    getDeptInfoSel() {
      commonApi
        .getDeptInfoSel()
        .then((response) => {
          if (response.data.status === 0) {
            let arr = response.data.data;
            // console.log(arr);
            this.orgTrustshipArr = response.data.data;
            if(this.tableListTemp.length){
              this.tableListTemp.forEach(item => {
                if(item.institutionCode){
                  let obj = arr.find(ite=>{
                    return ite.id == item.institutionCode;
                  })
                  if(obj){
                    item.organization = obj.instName || ''
                  }
                }
              });
            }
            // let arr1 = [];
            // arr.forEach((item) => {
            //   let obj = {};
            //   obj.label = item.instName;
            //   obj.Value = item.id;
            //   arr1.push(obj);
            // });
            // this.institutionCodeList = arr1;
            // console.log(arr1);
          } else {
            this.orgTrustshipArr = [];
          }
        })
        .catch(() => {});
    },
    getInitName(code, flag) {
      if (flag === "orgTrustship") {
        let arr = this.orgTrustshipArr;
        for (let i = 0; i < arr.length; i++) {
          if (arr[i].id === code) {
            return arr[i].instName;
          }
        }
      }
    },
    inputvalue(val) {
      // console.log(val);
      if (!val) {
        this.tableList = this.tableListTemp;
      }
      if (val) {
        let newData = this.tableList.filter((item) => {
          // console.log(item);
          if (item.id) {
            if (item.id.includes(val)) return item;
          }
        });
        this.tableList = [...newData];
      }
    },
    rowClick(row) {},
    selectAllEvent({ checked, records }) {
      // console.log(checked ? '所有勾选事件' : '所有取消事件', records)
      if (records.length) {
        let slval = records.map((item) => {
          return item.id;
        });
        // console.log(slval);
        this.slValue = slval;
        this.$emit("sendData", slval);
      } else {
        this.slValue = [];
        this.$emit("sendData", []);
      }

      // let slval_id = records.map((item) => {
      //   return item.id;
      // });
      // this.$emit("sendData", slval_id);
    },
    selectChangeEvent({ checked, records }) {
      // console.log(checked ? '勾选事件' : '取消事件', records)
      if (records.length) {
        let slval = records.map((item) => {
          return item.id;
        });
        // console.log(slval);
        this.slValue = slval;
        this.$emit("sendData", slval);
      } else {
        this.slValue = [];
        this.$emit("sendData", []);
      }

      // let slval_id = records.map((item) => {
      //   return item.id;
      // });
      // this.$emit("sendData", slval_id);
    },
    handleSelectionChange(val) {
      // console.log('handleSelectionChange',val);
      if (val.length) {
        let slval = val.map((item) => {
          return item.id;
        });
        // console.log(slval);
        this.slValue = slval;
        this.$emit("sendData", slval);
      } else {
        this.slValue = [];
        this.$emit("sendData", []);
      }

      // let slval_id = val.map((item) => {
      //   return item.id;
      // });
      // this.$emit("sendData", slval_id);
    },
    inputFocus() {
      this.isTableSelect = true;
      this.tableList = this.tableListTemp;
      this.$refs.xTable.clearFilter();
      this.checked(this.slValue)
    },
    inputBlur() {
      this.isTableSelect = false;
    },
    remove_tag(val) {
      // console.log(val);
      let item = this.tableList.filter((item) => {
        return item.id == val;
      });
      // console.log(item);
      this.$refs.xTable.setCheckboxRow(item[0], false);
      let arr = [];
      this.tableList.forEach((item) => {
        this.slValue.forEach((ite)=>{
          if(item.id == ite){
            arr.push(item.id)
          }
        })
      });
      this.$emit("sendData", arr);
    },
    remove_all() {
      this.$refs.xTable.clearCheckboxRow();
    },
    // 默认选中
    checked(data) {
      if (data.length > 0 && this.tableListTemp.length > 0) {
        for (let i = 0; i < data.length; i++) {
          this.tableListTemp.forEach((item) => {
            if (item.id && item.id == data[i]) {
              this.$nextTick(() => {
                this.$refs.xTable.setCheckboxRow(item, true);
              });
            }
          });
        }
      }
      // this.defaultSelecteRows = JSON.parse(JSON.stringify(data));
      // this.slValue = JSON.parse(JSON.stringify(data));
    },
    selected(row, index) {
      if (row.email) return true;
      if (!row.email) return false;
    },
    getContactList() {
      let params = {};
      pageApi
        .getContactList(params)
        .then((response) => {
          if (response.data.status === 200) {
            this.tableList = response.data.data.list;
            this.tableListTemp = response.data.data.list;
            if(this.orgTrustshipArr.length){
              this.tableListTemp.forEach(item => {
                if(item.institutionCode){
                  let obj = this.orgTrustshipArr.find(ite=>{
                    return ite.id == item.institutionCode;
                  })
                  if(obj){
                    item.organization = obj.instName || ''
                  }
                }
              });
            }
            // this.checked(this.slValue)
            // if (list.length === 0) this.$message.error('查询不到当前联系人')
          } else {
            this.tableList = [];
            this.tableListTemp = [];
            this.$message.error(response.data.message || "服务异常");
          }
        })
        .catch((err) => {
          console.log(err);
          this.tableList = [];
          // this.$message.error({
          //   message:err
          // });
        });
    },
    filterEvent(option) {
      // console.log(option);
      const xTable = this.$refs.xTable;
      // // 设置为选中状态
      option.checked = true;
      // // 修改条件之后，需要手动调用 updateData 处理表格数据
      xTable.updateData();
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
    customEqualFilterMethod ({ option, row, column }) {
      if (option.data) {
        return row[column.property] === option.data
      }
      return true
    },
    formatter ({ cellValue }) {
      const item = this.institutionCodeList.find(item => item.value === cellValue)
      return item ? item.label : ''
    },
    checCheckboxkMethod({row}){
      return row.email
    }
  },
};
</script>

<style lang='scss' scoped>
.select_contacts {
  position: relative;
  // width: 348px;
  .selectTableStyle {
    width: 650px;
    position: absolute;
    margin-top: 2px;
    z-index: 20;
    box-sizing: border-box;
    padding: 1px;
    box-shadow: 0, 0, 0, rgb(83, 117, 212);
    border-radius: 5px;
    border: 1px solid #ccc;
    overflow: hidden;
    .table {
      border: 1px solid #f1f1f1;
      box-shadow: 0 0 0 1px #f1f1f1;
    }
  }
}
</style>
<style lang='scss'>
.select_contacts {
  .el-select__tags-text {
    display: inline-block;
    width: 65px;
    overflow: hidden;
    text-overflow: ellipsis;
    // margin-right: -9px;
  }
  // .el-tag__close {
  //   position: relative;
  //   top: -6px !important;
  // }
  .el-select__caret {
    display: none;
  }
}
.select_xlk {
  display: none !important;
  z-index: -1 !important;
}
.vxe-select--panel {
   z-index: 9997 !important
 }
</style>

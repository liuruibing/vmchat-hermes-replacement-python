<template>
  <div class="select_fundCode" @click.stop="">
    <el-select
      ref="inputFocus"
      popper-class="select_xlk"
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
        :key="item.fundCode"
        :label="item.codeName"
        :value="item.fundCode"
      ></el-option>
    </el-select>
    <!-- <el-input ref="inputFocus" @focus='inputFocus' multiple v-model="slValue"  clearable></el-input> -->
    <div v-show="isTableSelect" class="selectTableStyle_vxe">
      <vxe-table
        border
        auto-resize
        show-overflow="tooltip"
        size="mini"
        :tooltip-config="{showAll: true,}"
        :cell-class-name="cellClassName"
        :header-cell-class-name="headerCellClassName"
        ref="xTable"
        height="300"
        :filter-config="{ showIcon: false }"
        :data="tableList"
        @checkbox-all="selectAllEvent"
        @checkbox-change="selectChangeEvent"
      >
        <vxe-table-column type="checkbox" width="40"></vxe-table-column>
        <!-- <vxe-table-colgroup title="文本"> -->
          <vxe-table-column
            field="codeName"
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
                placeholder="产品"
                clearable
              ></vxe-input>
            </template>
          </vxe-table-column>
          <vxe-table-column
            field="trustorName"
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
                placeholder="托管机构名称"
                clearable
              ></vxe-input>
            </template>
          </vxe-table-column>
          <vxe-table-column
            field="operatorName"
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
                placeholder="基金服务机构名称"
                clearable
              ></vxe-input>
            </template>
          </vxe-table-column>
        <!-- </vxe-table-colgroup> -->
      </vxe-table>
      
    </div>
  </div>
</template>

<script>
import XEUtils from "xe-utils";
import $ from "jquery";
import bizBeginApi from "@/api/transfer/bizBegin";
export default {
  props: ["modelValue", "width", "defaultValue"],
  model: {
    prop: "modelValue",
    event: "sendData",
  },
  watch: {
    modelValue(data) {
      // console.log('xxxx',data);
      if (data.length) {
        this.slValue = JSON.parse(JSON.stringify(data));
      } else {
        this.slValue = [];
      }
      // console.log('this.slValue',data);
    },
    // defaultValue(data){
    //   console.log('defaultValue',data);
    //   this.slValue = data;
    // }
  },
  data() {
    return {
      tableList: [],
      tableListTemp: [],
      slValue: [],
      isTableSelect: false,
    };
  },
  mounted() {
    console.log('mounted');
    // this.slValue=['aaa','bbb']
    let that = this;
    $("body").on("click", () => {
      that.isTableSelect = false;
      this.tableList = this.tableListTemp;
    });
    this.getProductInfo();
  },
  // activated(){
  //   console.log('aaaaaa');
  // },
  // deactivated(){},
  methods: {
    cellClassName({}){
      return "vxe-cell-class-name"
    },
    headerCellClassName({}){
      return "vxe-header-cell-class-name"
    },
    rowClick(row) {
      // console.log(row);
    },
    selectAllEvent ({ checked, records }) {
      // console.log(checked ? '所有勾选事件' : '所有取消事件', records)
      if (records.length) {
        let slval = records.map((item) => {
          return item.fundCode;
        });
        // console.log(slval);
        this.slValue = slval;
        this.$emit("sendData", slval);
      } else {
        this.slValue = [];
        this.$emit("sendData", []);
      }
    },
    selectChangeEvent ({ checked, records }) {
      // console.log(checked ? '勾选事件' : '取消事件', records)
      if (records.length) {
        let slval = records.map((item) => {
          return item.fundCode;
        });
        // console.log(slval);
        this.slValue = slval;
        this.$emit("sendData", slval);
      } else {
        this.slValue = [];
        this.$emit("sendData", []);
      }
    },
    inputFocus() {
      this.tableList = this.tableListTemp;
      this.isTableSelect = true;
      this.$refs.xTable.clearFilter();
      this.checked(this.slValue)
    },
    inputBlur() {
      this.isTableSelect = false;
    },
    remove_tag(val) {
      let item = this.tableList.filter((item) => {
        return item.fundCode == val;
      });
      // console.log(item);
      this.$refs.xTable.setCheckboxRow(item[0], false);
      let arr = [];
      this.tableList.forEach((item) => {
        this.slValue.forEach((ite)=>{
          if(item.fundCode == ite){
            arr.push(item.fundCode)
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
      setTimeout(() => {
        if (data.length > 0 && this.tableListTemp.length > 0) {
          for (let i = 0; i < data.length; i++) {
            this.tableListTemp.forEach((item) => {
              if (item.fundCode && item.fundCode == data[i]) {
                // console.log(item,i,this.slValue[i]);
                this.$nextTick(() => {
                  this.$refs.xTable.setCheckboxRow(item, true);
                });
              }
            });
          }
        }
      }, 100);
    },
    getProductInfo() {
      this.$message.closeAll();
      bizBeginApi
        .getProductFund()
        .then(({ data: res }) => {
          if (res.status === 200) {
            let temp = [...res.data];
            for (let i of temp) {
              i["codeName"] = i.fundCode + "_" + i.fundName;
            }
            this.tableListTemp = temp;
            this.tableList = temp;
            // console.log(this.tableList);
          } else this.$message.error("查询产品信息失败");
        })
        .catch((err) => {
          this.$message.error("查询产品信息失败");
        });
    },
    customStringFilterMethod({ option, row, column }) {
      // console.log('option.data',option.data);
      // console.log('row[column.property]',row[column.property]);
      if (option.data) {
        return (
          // XEUtils.toValueString(row[column.property])
            row[column.property] && row[column.property].toLowerCase()
            .indexOf(option.data) > -1
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

<style lang='scss' scoped>
.select_fundCode {
  position: relative;
  // width: 348px;
  .selectTableStyle_vxe {
    width: 600px;
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
.vxe-table--tooltip-wrapper {
  z-index: 10000 !important;
}
.select_fundCode {
  .el-select__tags-text {
    display: inline-block;
    width: 100px;
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
</style>
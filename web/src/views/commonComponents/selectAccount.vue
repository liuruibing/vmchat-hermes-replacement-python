<template>
  <div class="inputTableStyle" @click.stop="" @keyup.enter="selsectTableFirst">
    <el-input
      ref="inputFocus"
      placeholder="请选择"
      readonly
      v-model="slValue"
      @input="searchData"
      @click.native="deptogglePanel($event)"
      clearable
      @clear="clearInput"
      maxlength="66"
      :disabled="disabled"
    ></el-input>
    <transition name="el-zoom-in-top">
      <div v-show="isTableSelect" class="selectTableStyle" :style="tableWidth">
        <!-- <el-input placeholder="请输入"   v-model="searchvalue" @input="searchData"></el-input> -->
        <el-table
          :data="tableList"
          border
          @row-click="rowClick"
          class="table"
          highlight-current-row
          ref="tableSelect"
          max-height="240"
        >
        <!-- <el-table-column
          type="selection"
          width="55">
        </el-table-column> -->
          <el-table-column
            show-overflow-tooltip
            label="账户名称"
            prop="accoName"
            min-width="100"
            header-align="center"
          >
            <template slot="header" slot-scope="scope">
              账户名称
              <el-input
                v-model="search11"
                size="mini"
                style="width: 100% !important"
                @input="accoNameSearch"
                placeholder="输入关键字搜索"
              />
            </template>
          </el-table-column>
          <el-table-column
            show-overflow-tooltip
            label="账户账号"
            prop="accoNo"
            min-width="100"
            header-align="center"
          >
            <template slot="header" slot-scope="scope">
            账户账号
            <el-input
              v-model="search12"
              size="mini"
              style="width:100% !important"
              @input="accoNameSearch"
              placeholder="输入关键字搜索"/>
          </template>
          </el-table-column>
          <el-table-column
            show-overflow-tooltip
            label="开户行"
            prop="accoBank"
            min-width="100"
            header-align="center"
          >
          <template slot="header" slot-scope="scope">
            开户行
            <el-input
              v-model="search13"
              size="mini"
              style="width:100% !important"
              @input="accoNameSearch"
              placeholder="输入关键字搜索"/>
          </template>
          </el-table-column>
          <el-table-column
            show-overflow-tooltip
            label="账户类型"
            prop="accoType"
            min-width="100"
            header-align="center"
            column-key="accoType"
            :filters="filtersArr"
            :filter-method="filterMethod"
            :filtered-value="filteredValue"
          >
            <template slot-scope="{ row }">
              <span v-if="row.accoType == 'raise'">募集户</span>
              <span v-else-if="row.accoType == 'fiduciary'">托管户</span>
              <span v-else-if="row.accoType == 'other'">其他账户</span>
              <span v-else-if="row.accoType == 'getZqAccList'">证券账户</span>
              <span v-else-if="row.accoType == 'getQhAccList'">期货账户</span>
              <span v-else-if="row.accoType == 'getYhjAccListZz'"
                >银行间债券账户-中债</span
              >
              <span v-else-if="row.accoType == 'getYhjAccListSq'"
                >银行间债券账户-上清</span
              >
              <span v-else-if="row.accoType == 'zq'">证券账户</span>
              <span v-else-if="row.accoType == 'qh'">期货账户</span>
              <span v-else-if="row.accoType == 'yhjzz'"
                >银行间债券账户-中债</span
              >
              <span v-else-if="row.accoType == 'yhjsq'"
                >银行间债券账户-上清</span
              >
              <span v-else>{{ row.accoType || "-" }}</span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </transition>
  </div>
</template>
<script>
import bizBeginApi from "@/api/transfer/bizBegin";
import $ from "jquery";
import { set } from 'xe-utils/methods';
export default {
  // props: ['modelValue', 'width'],
  props: {
    modelValue: {},
    with: {},
    disabled: {
      default: false,
    },
    filteredValue:{
      type:Array,
      default:()=>[]
    }
  },
  model: {
    prop: "modelValue",
    event: "sendData",
  },
  watch: {
    modelValue(data) {
      this.slValue = data;
      if (data == "") {
        this.slValue = data;
        this.slRow = {};
        this.$emit("sendDataObj", "");
        // this.tableList = this.tableListTemp
        // this.getProductInfo()
      } else {
        // console.log(data,'data');
        // if(data){
        //   let isAllMatch = data.split('_')
        //   if (isAllMatch.length > 1 && !this.hasSelectRow) this.matchingAll()
        // }
      }
    },
    isTableSelect(data) {
      if (this.hasSelectRow) this.judge();
      else {
      }
      // this.judge()
    },
    filteredValue(data){
      // console.log('filteredValue',data);
      this.$refs.tableSelect.clearFilter();
      this.setDefaultFilter(3,data);
    }
  },
  data() {
    return {
      tableWidth: {
        width: this.width || "600px",
      },
      search11: "",
      search12: "",
      search13: "",
      slValue: "",
      hasSelectRow: false,
      slRow: {},
      isTableSelect: false,
      tableList: [],
      tableListTemp: [],
      tableData:[],
      searchvalue: "",
      filtersArr: [
        // {text:'募集户',value:'raise'},
        // {text:'托管户',value:'fiduciary'},
        // {text:'证券账户',value:'zq'},
        // {text:'期货账户',value:'qh'},
        // {text:'银行间债券账户-中债',value:'yhjzz'},
        // {text:'银行间债券账户-上清',value:'yhjsq'},
        // {text:'其他账户',value:'other'},
      ],
      // filteredValue:['other']
    };
  },
  mounted() {
    let that = this;
    $("body").on("click", function () {
      that.isTableSelect = false;
      that.tableList = that.tableListTemp;
    });
    //  this.getProductInfo()
    this.tableList = [];
    this.tableListTemp = [];
  },
  methods: {
    init(data) {
      this.tableList = data;
      this.tableListTemp = data;
      let arr = [];
      let arr1 = [];
      data.forEach((item) => {
        arr.push(item.accoType);
      });
      arr = Array.from(new Set(arr));
      arr.forEach((item) => {
        let obj = {};
        obj.value = item;
        obj.text = this.status(item);
        arr1.push(obj);
      });
      this.filtersArr = arr1;
    },
    status(val) {
      let data = "";
      if (val == "raise") {
        data = "募集户";
      } else if (val == "fiduciary") {
        data = "托管户";
      } else if (val == "zq") {
        data = "证券账户";
      } else if (val == "qh") {
        data = "期货账户";
      } else if (val == "yhjzz") {
        data = "银行间债券账户-中债";
      } else if (val == "yhjsq") {
        data = "银行间债券账户-上清";
      } else if (val == "other") {
        data = "其他账户";
      } else if (val == "getZqAccList") {
        data = "证券账户";
      } else if (val == "getQhAccList") {
        data = "期货账户";
      } else if (val == "getYhjAccListZz") {
        data = "银行间债券账户-中债";
      } else if (val == "getYhjAccListSq") {
        data = "银行间债券账户-上清";
      }
      return data;
    },
    rowClick(row) {
      this.slValue = JSON.parse(JSON.stringify(row.accoName));
      this.slRow = JSON.parse(JSON.stringify(row));
      this.isTableSelect = false;
      this.hasSelectRow = true;
      this.$emit("sendData", this.slValue);
      this.$emit("sendDataObj", this.slRow);
    },
    // 检验输入框的值是否存在
    judge() {
      let isClear = this.tableList.filter((item) => {
        return item.accoName == this.slValue;
      });
      if (isClear.length == 0) {
        this.slValue = "";
        this.hasSelectRow = false;
        this.$emit("sendData", "");
      }
    },
    clearInput() {
      this.tableList = this.tableListTemp;
      this.$emit("sendData", "");
    },
    //回车选择第一天
    selsectTableFirst() {
      if (this.tableList.length != 0) {
        let row = this.tableList[0];
        this.rowClick(row);
        this.$refs.inputFocus.blur();
        this.$emit("enter");
      }
    },
    // 获取焦点
    inputFocus() {
      this.search11 = "";
      this.search12 = "";
      this.search13 = "";
      this.isTableSelect = true;
      this.tableList = this.tableListTemp;
      if (this.slValue) {
        let code = this.slValue;
        for (let i of this.tableList) {
          if (i.accoName == code) {
            this.$refs.tableSelect.setCurrentRow(i);
            break;
          }
        }
      }
    },
    hide(){
      this.isTableSelect = false;
      this.tableList = this.tableListTemp;
    },
    //input查找
    searchData(data) {
      // console.log(data);
      if (!data) {
        this.$emit("sendData", "");
        return (this.tableList = this.tableListTemp);
      }
      // this.$emit('sendData', data)
      this.tableList = [];
      // let reg = /^[a-zA-Za-z0-9\u4e00-\u9fa5\-\_]+$/
      let newData = this.tableListTemp.filter((itme) => {
        if (itme.accoName.includes(data)) return itme;
      });
      this.tableList = [...newData];
    },
    // 焦点获取
    relation() {
      this.$nextTick(() => {
        this.$refs.inputFocus.focus();
      });
    },
    filterMethod(value, row, column) {
      const property = column["property"];
      return row[property] === value;
    },
    filterChange(data){
      console.log('filterChangefilterChangefilterChange',data);
    },
    accoNameSearch(data) {
      // console.log(data);
      let accoName = this.search11;
      let accoNo = this.search12;
      let accoBank = this.search13;
      let idArr = [];
      let idArr1 = [];
      let idArr2 = [];
      let idArr3 = [];
      let arr1 = [];
      let arr2 = [];
      let arr3 = [];
      if (accoName) {
        // console.log('accoName',accoName);
        arr1 = this.tableListTemp.filter((item) => {
          return item.accoName && item.accoName.includes(accoName);
        });
      } else {
        arr1 = this.tableListTemp;
      }
      if (accoNo) {
        // console.log('accoNo',accoNo);
        arr2 = this.tableListTemp.filter((item) => {
          return item.accoNo && item.accoNo.includes(accoNo);
        });
      } else {
        arr2 = this.tableListTemp;
      }
      if (accoBank) {
        arr3 = this.tableListTemp.filter((item) => {
          return item.accoBank && item.accoBank.includes(accoBank);
        });
      } else {
        arr3 = this.tableListTemp;
      }
      idArr1 = arr1.map(item=>{
        return item.accoNo
      })
      idArr2 = arr2.map(item=>{
        return item.accoNo
      })
      idArr3 = arr3.map(item=>{
        return item.accoNo
      })
      idArr = [...idArr1,...idArr2]
      let tmp = []
      let tmp1 = []
      idArr.sort();
      idArr.sort(function(a,b){
        // console.log(a,b);
        if(a==b && tmp.indexOf(a) === -1) tmp.push(a);
      });
      tmp = [...tmp,...idArr3];
      tmp.sort();
      // console.log(tmp);
      tmp.sort(function(a,b){
        if(a==b && tmp1.indexOf(a) === -1) tmp1.push(a);
      });
      // console.log(tmp1);
      let tableList = []
      this.tableListTemp.forEach((item,index)=>{
        if(tmp1.includes(item.accoNo)) tableList.push(item)
      })
      this.tableList = tableList;
      // console.log(tableList);



    },
    accoNoSearch(data) {
      // if (data) {
      //   this.tableList = this.tableListTemp.filter((item) => {
      //     return item.accoNo && item.accoNo.includes(data);
      //   });
      // } else {
      //   this.tableList = this.tableListTemp;
      // }
      let arr = [];
      if(this.tableData.length){
        arr = this.tableData
      }else{
        arr = this.tableListTemp
      }
      if (data) {
        this.tableList = arr.filter((item) => {
          return item.accoName && item.accoNo.includes(data);
        });
        this.tableData = arr.filter((item) => {
          return item.accoName && item.accoNo.includes(data);
        });
      } else {
        this.tableList = arr;
        this.tableData = [];
      }
    },
    deptogglePanel(event){
      // this.$refs.inputFocus.blur();
      if(this.disabled) return
      event || (event = window.event)
      event.stopPropagation ? event.stopPropagation() : (event.cancelBubble = true)
      this.isTableSelect ? this.hide() : this.inputFocus()
    },
    setDefaultFilter(col, val) {
      const column = this.$refs.tableSelect.columns[col]
      column.filteredValue = val;
      this.$refs.tableSelect.store.commit('filterChange', {
        column,
        values: column.filteredValue,
        silent: true
      })
    }
  },
};
</script>
<style lang='scss' scoped>
.inputTableStyle {
  position: relative;
  .selectTableStyle {
    position: absolute;
    margin-top: 2px;
    z-index: 99999;
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
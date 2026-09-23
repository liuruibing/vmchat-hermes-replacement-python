<template>
  <div class="fundListDialog">
    <!-- 搜索 -->
    <el-form
      :inline="true"
      ref="formQuery"
      :model="formQuery"
      :rules="rules"
      class="formQuery pdt5"
    >
      <el-row>
        <el-col :span="16">
          <div class="grid-content bg-purple">
            <el-form-item  :label-width="formLabelWidth" prop="fundCode">
              <span class="item-label" slot="label">计划/组合代码</span>
              <el-input
                v-model.trim="formQuery.fundCode"
                clearable
                placeholder="请输入计划/组合代码"
                size="small"
              ></el-input>
            </el-form-item>
            <el-form-item label="" :label-width="formLabelWidth" prop="fundName">
              <span class="item-label" slot="label">计划/组合名称</span>
              <el-input
                v-model.trim="formQuery.fundName"
                clearable
                placeholder="请输入计划/组合名称"
                size="small"
              ></el-input>
            </el-form-item>
            <el-form-item prop="showNull">
              <el-checkbox-group v-model="showNull" @change="changeDataType">
                <el-checkbox label="1">只显示计划</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="grid-content bg-purple-light">
            <el-form-item class="search_button_com">
              <el-button
                type="primary"
                :disabled="btnDisabled"
                @click="onQuery(1)"
                class="mb5"
                icon="el-icon-search"
              >查询</el-button>
              <el-button   @click="resetForm('formQuery')">重置</el-button>
              <el-button type="primary" icon="el-icon-plus" class="mb5" @click="checkFund()">确定</el-button>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
    </el-form>
    <div class="picc_forms_table_title">
      <div class="picc_forms_table_title_line"></div>
      <div>产品信息</div>
    </div>
    <el-table
      :data="tableData"
      border
      @sort-change="handleSortChange"
      v-loading="tableLoading"
      :header-row-style="headerRowStyle"
      :cell-style="cellStyle"
      style="width: 100%"
    >
      <el-table-column  width="55" align="center" label="" >
        <template slot-scope="scope">
           <el-radio :label="scope.row.fundCode" v-model="templateRadio" @change.native="getTemplateRow(scope.$index,scope.row)">&nbsp</el-radio>
        </template>     
      </el-table-column>
      <el-table-column
        prop="fundCode"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="计划/组合代码"
        min-width="100"
        header-align="center"
      ></el-table-column>
      <el-table-column
        prop="fundName"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="计划/组合名称"
        min-width="250"
        align="left"
        header-align="center"
      ></el-table-column>
      <el-table-column v-if="false"
        prop="是否是计划"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="fundPlan"
        min-width="100"
        header-align="center"
      ></el-table-column>
    </el-table>
    <Pagination
      :total="total"
      :limit="formQuery.pageSize"
      :page="formQuery.pageNum"
      @pagination="pagination"
    ></Pagination>
  </div>
</template>

<script type="text/ecmascript-6">
import { FILE_URL } from '@/utils/request'
import Pagination from "@/components/NewPagination";
import commonApi from "@/api/common";
import fundInfoApi from "@/api/dataManage/fundInfoApi";
import { getToken } from '@/utils/auth'

export default {
  components: {
    Pagination
  },
  name: "fundListDialog",
  data() {
    return {
      // 查询参数
      formQuery: {
        // 产品代码
        fundCode: "",
        // 产品名称
        fundName: "",
        //是否计划
        fundPlan:"",
        //筛选
        showNull:"",
        // 起始页
        pageNum: 1,
        isPlan:'0',
        // 每页数量
        pageSize: 10,
        //排序方式
        // orderBy: '"fundCode" asc'
      },

      // 验证规则
      rules: {
      },

      showNull:false,
      //产品列表数据
      tableData:[],
      //筛选
      tableData1:[],
      //总条数
      total: 0,
      // 表格loading
      tableLoading: false,
      // 附件表格loading
      tableLoading_doc: false,
      /* 按钮禁止与否 */
      isDisabled: false,
      // 表单宽度
      formLabelWidth: "120px",

      templateRadio:"",
      //选中行数据
      tableRowData:null,

      // 查询按钮禁用
      btnDisabled: false,
      // 查询按钮禁用 附件列表
      btnDisabled_doc: false,
      //默认页签
      activeName:'baseInfo'
    };
  },
  mounted() {

    // 默认查询
    this.$nextTick(() => {
      // 查询
      this.onQuery();
    });
  },
  methods: {
    //筛选
    changeDataType(){
      if(this.showNull==true){
        this.formQuery.isPlan=1
        this.onQuery();
      }else
      {
        this.formQuery.isPlan=0
        this.onQuery();
      }
      // if(this.tableData){
      //   if(this.formQuery.showNull){
      //     let tempTableData = JSON.parse(JSON.stringify(this.tableData));
      //     let tempTableData1 = JSON.parse(JSON.stringify(this.tableData));
      //     tempTableData = tempTableData.filter(function(rowData){
      //
      //       return rowData.fundPlan == "ROOT"
      //     })
      //     this.tableData = tempTableData
      //     this.tableData1 = tempTableData1
      //   }else {
      //     let tempTableData = JSON.parse(JSON.stringify(this.tableData1));
      //     this.tableData = tempTableData
      //   }
      //
      // }
    },
    // 查询
    onQuery(page) {
      this.$refs["formQuery"].validate(valid => {
        if (valid) {
          // 禁用搜索按钮
          this.$fun.searchButtonDisabled("btnDisabled", this);
          // 重置起始页
          if (page) this.formQuery.pageNum = 1;
          // 查询产品信息
          this.selectFundInfoList();
        }
      });
    },
    //获取选中数据
    getTemplateRow(index,row){
      this.tableRowData = row;
    },
    checkFund(){
      if(this.tableRowData==null || this.tableRowData==undefined || this.tableRowData==""){
        this.$message({
          message: "请选择组合",
          type: "waring"
        });
        return
      }else{
        let data = this.tableRowData
        this.$emit("getTemplateRow", { data: data });
        this.dialogMask = false
      }

    },
    // 清除
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    // 页面分页点击事件
    pagination(val) {
      let { page, limit } = val;
      // 起始页
      this.formQuery.pageNum = page;
      // 每页数量
      this.formQuery.pageSize = limit;
      // 查询
      this.onQuery();
    },

    // 查询产品信息
    selectFundInfoList(flag) {
      this.tableLoading = true;
      let params = Object.assign({}, this.formQuery, {

      });
      // 清除空字段
      for (let k in params) {
        if (!params[k] && String(params[k]) !== "0") {
          delete params[k];
        }
      }
      fundInfoApi.fun_selectFundListNotManager(params)
        .then(res => {
          this.tableLoading = false;
          this.isDisabled = false;
          let { status, data } = res;
          if (status === 0) {
              let { list, total } = data;
              this.tableData = list;
              this.total = total;
          }
        })
        .catch(() => {
          this.tableLoading = false;
          this.isDisabled = false;
        });
    },



    // 当表格的排序条件发生变化的时候会触发该事件
    handleSortChange(val) {
      this.formQuery.orderBy = this.$fun.queryOrderBy(val);
      // 查询
      this.onQuery();
    },

    cellStyle({row, column, rowIndex, columnIndex}){
      return "height:40px;font-size:16px;font-weight:500"
    },
    headerRowStyle({row, column, rowIndex, columnIndex}){
      return "height:40px;font-size:16px;font-weight:500;color:#333333"
    },

  },
  watch: {
  }
};
</script>

<style lang="scss" >
.fundListDialog{
  .el-dialog {
    width: 54% !important;
    .el-form {
      width: 100% !important;
      font-size: 0;
    }
    .el-form-item {
      min-width: 50%;
      margin-right: 0;
    }
    .mr5 {
      margin-right: 5px;
    }
  }
  .ProductAndProperty_box {
    height: 300px;
  }
  .vcConfig {
    width: 100%;

    padding: 10px;
    text-align: center;
    color: #007A77;
    font-weight: 600;
  }
  .tableData2Style {
    margin-top: 10px;
  }
  .mb20 {
    margin-bottom: 15px;
  }
  .pointer{
    color: #007A77;
  }
  // 火狐移除
  input[type="number"] {
    -moz-appearance: textfield;
  }

  //谷歌下的移除
  input[type="number"]::-webkit-inner-spin-button,
  input[type="number"]::-webkit-outer-spin-button {
    -webkit-appearance: none;
  }
  .item-label{
    font-size: 16px;
  }
  .el-table--medium{
    border-top: 2px solid #007A77 !important;
  }
  .el-checkbox-button--medium .el-checkbox-button__inner{
    font-size: 16px;
  }


}
</style>

<template>
  <div class="benchmarkIndexList">
    <!-- 搜索 -->
    <el-form :inline="true" ref="formQuery" :model="formQuery" label-width="auto" :rules="rules" class="standard-form">
      <el-row>
        <el-col :span="24">
          <el-form-item prop="indexCode">
            <span class="item-label" slot="label">指数代码</span>
            <el-input v-model.trim="formQuery.indexCode" clearable placeholder="请输入代码" size="small"></el-input>
          </el-form-item>
          <el-form-item label="" prop="indexName">
            <span class="item-label" slot="label">指数名称</span>
            <el-input v-model.trim="formQuery.indexName" clearable placeholder="请输入名称" size="small"></el-input>
          </el-form-item>
          <el-form-item class="">
            <el-button type="primary" size="small" :disabled="btnDisabled" @click="onQuery(1)" class="mb5" icon="el-icon-search">查询</el-button>
            <el-button @click="resetForm('formQuery')" type="info" size="small" plain>重置</el-button>
            <el-button type="primary" size="small" icon="el-icon-plus" @click="checkFund()">选择</el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <div class="page-model-title">
      <div class="title-icon">
        <div class="color-box"></div>
      </div>
      <span class="title-txt">指数信息</span>
    </div>
    <div id="standard-table">
      <el-table
        id="gantaniang"
        :data="tableData"
        @sort-change="handleSortChange"
        v-loading="tableLoading"
        stripe
        :header-cell-style="{ color: '#20212b', height: '54px' }"
        :cell-style="{ height: '50px' }"
        style="width: 100%"
      >
        <el-table-column width="55" align="center" label="">
          <template slot-scope="scope">
            <el-radio :label="scope.row.indexCode" v-model="templateRadio" @change.native="getTemplateRow(scope.$index, scope.row)">&nbsp</el-radio>
          </template>
        </el-table-column>
        <el-table-column
          prop="indexCode"
          sortable="custom"
          :sort-orders="['ascending', 'descending']"
          show-overflow-tooltip
          label="指数代码"
          min-width="100"
          header-align="center"
        ></el-table-column>
        <el-table-column
          prop="indexName"
          sortable="custom"
          :sort-orders="['ascending', 'descending']"
          show-overflow-tooltip
          label="指数名称"
          min-width="100"
          header-align="center"
        ></el-table-column>
        <el-table-column
          prop="indexTypeStr"
          sortable="custom"
          :sort-orders="['ascending', 'descending']"
          show-overflow-tooltip
          label="指数类型"
          min-width="100"
          align="left"
          header-align="center"
        ></el-table-column>
        <el-table-column
          prop="indexExchange"
          sortable="custom"
          :sort-orders="['ascending', 'descending']"
          show-overflow-tooltip
          label="市场代码"
          min-width="100"
          header-align="center"
        ></el-table-column>
      </el-table>
      <Pagination :total="total" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination"></Pagination>
    </div>
  </div>
</template>

<script type="text/ecmascript-6">
import { FILE_URL } from '@/utils/request'
import Pagination from "@/components/NewPagination";
import commonApi from "@/api/common";
import { getToken } from '@/utils/auth'
import fundSpecimenDetailApi from "@/api/dataManage/benchmarkInfo";

export default {
  components: {
    Pagination
  },
  name: "benchmarkIndexList",
  data() {
    return {
      // 查询参数
      formQuery: {
        // 产品代码
        indexCode: "",
        // 产品名称
        indexType: "",

        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10,
        //排序方式
        orderBy: ''
      },
      // 验证规则
      rules: {
      },


      //产品列表数据
      tableData:[],
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
          type: "waring",
          customClass: "message-warning"
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
        isPlan:'0'
      });
      // 清除空字段
      for (let k in params) {
        if (!params[k] && String(params[k]) !== "0") {
          delete params[k];
        }
      }
      fundSpecimenDetailApi.fun_selectIndexList(params)
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
      return ";font-size:16px;font-weight:500"
    },

  },
  watch: {
  }
};
</script>

<style lang="scss" scoped>
.benchmarkIndexList {
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
    color: #319ef1;
    font-weight: 600;
  }
  .tableData2Style {
    margin-top: 10px;
  }
  .mb20 {
    margin-bottom: 15px;
  }
  .pointer {
    color: #409eff;
  }
  // 火狐移除
  input[type='number'] {
    -moz-appearance: textfield;
  }

  //谷歌下的移除
  input[type='number']::-webkit-inner-spin-button,
  input[type='number']::-webkit-outer-spin-button {
    -webkit-appearance: none;
  }
  .item-label {
    font-size: 14px;
  }
}
</style>

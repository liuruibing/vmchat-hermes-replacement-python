<template>
  <div class="fundListDialog">
    <!-- 搜索 -->
    <el-form :inline="true" ref="formQuery" :model="formQuery" :rules="rules" class="formQuery pdt5">
      <el-row>
        <el-col :span="18">
          <div class="grid-content bg-purple">
            <el-form-item :label-width="formLabelWidth" prop="fundCode">
              <span class="item-label" slot="label">产品代码</span>
              <el-input v-model.trim="formQuery.fundCode" clearable placeholder="请输入产品代码" size="small"></el-input>
            </el-form-item>
            <el-form-item label="" :label-width="formLabelWidth" prop="fundName">
              <span class="item-label" slot="label">产品名称</span>
              <el-input v-model.trim="formQuery.fundName" clearable placeholder="请输入产品名称" size="small"></el-input>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="6">
          <!--          :disabled="btnDisabled"-->
          <div class="grid-content bg-purple-light">
            <el-form-item class="search_button_com">
              <el-button type="primary" @click="onQuery(1)" class="mb5" icon="el-icon-search">查询</el-button>
              <!--              <el-button   @click="resetForm('formQuery')">重置</el-button>-->
              <el-button type="primary" icon="el-icon-plus" class="mb5" @click="checkFund()">确定</el-button>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
    </el-form>
    <div class="table-title">
      <div class="picc_forms_table_title_line"></div>
      <div>产品信息</div>
    </div>
    <vxe-table
      :data="tableData"
      stripe
      :cell-style="{ height: '35px' }"
      highlight-hover-row
      show-header-overflow
      max-height="400px"
      resizable
      auto-resize
      show-overflow
      @sort-change="handleSortChange"
      v-loading="tableLoading"
    >
      <vxe-table-column width="55" align="center" label="">
        <template slot-scope="scope">
           
          <vxe-radio :label="scope.row.fundCode" v-model="templateRadio" @change.native="getTemplateRow(scope.$index, scope.row)">&nbsp</vxe-radio>
        </template>
           
      </vxe-table-column>
      <vxe-table-column field="fundCode" title="产品代码" sortable min-width="100" header-align="center"></vxe-table-column>
      <vxe-table-column field="fundName" title="产品名称" sortable min-width="250" align="left" header-align="center"></vxe-table-column>
      <vxe-table-column field="createDate" title="成立日期" sortable min-width="100" header-align="center"></vxe-table-column>
    </vxe-table>
    <Pagination :total="total" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination"></Pagination>
  </div>
</template>

<script type="text/ecmascript-6">
import { FILE_URL } from '@/utils/request'
import Pagination from "@/components/Pagination";
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
        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10,
        //排序方式
        orderBy: "fundCode asc"
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
          message: "请选择产品",
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
      const params = {}
      params.fundCode = this.formQuery.fundCode
      params.fundName = this.formQuery.fundName
      params.pageNum =this.formQuery.pageNum
      params.pageSize = this.formQuery.pageSize
      params.orderString = this.formQuery.orderBy
      fundInfoApi.fun_selectFundListNotManager(params)
        .then(res => {
          const {status, data} = res
          if (status === 0) {
            this.tableLoading = false;
            this.isDisabled = false;
            this.tableData = data.list
            this.total = data.total
          }else {
            this.tableLoading = false;
            this.isDisabled = false;
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

<style lang="scss">
.el-dialog .el-form {
  width: 100% !important;
}
.fundListDialog {
  .table-title {
    font-size: 14px;
    color: rgba(0, 0, 0, 0.85);
    line-height: 20px;
    font-weight: 600;
    padding: 10px 0 10px 2px;
    ::v-deep .ant-btn {
      border-color: #4055ff;
      color: #4055ff;
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

  .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
  input::-webkit-input-placeholder {
    color: #999 !important;
  }
  .item-label {
    font-size: 14px;
  }
  .el-table--medium {
    border-top: 2px solid #e13c3d !important;
  }
  .el-checkbox-button--medium .el-checkbox-button__inner {
    font-size: 16px;
  }
}
</style>

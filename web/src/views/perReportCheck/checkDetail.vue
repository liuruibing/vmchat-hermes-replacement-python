<template>
  <div class="check_detail">
    <el-form
      :inline="true"
      ref="formInline"
      :model="formInline"
      style="margin-bottom: 8px"
      class="demo-form-inline form_inline_search"
    >
      <el-row>
        <el-col :span="16">
          <div style="width: 100%; height: 50px">
            <el-form-item label="校验状态" prop="flag">
              <el-radio
                @change="selectChange"
                v-model="formInline.flag"
                label=""
                >全部</el-radio
              >
              <el-radio
                @change="selectChange"
                v-model="formInline.flag"
                label="0"
                >校验成功</el-radio
              >
              <el-radio
                @change="selectChange"
                v-model="formInline.flag"
                label="-1"
                >校验失败</el-radio
              >
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="8">
          <el-form-item class="search_button_com">
            <!-- <el-button type='primary' @click='onSubmit(true)' style='margin-bottom: 5px;' size='small'><i class='el-icon-search'></i>查询</el-button>
            <el-button type='primary' plain @click='restForm()' style='margin-bottom: 5px; ' size='small'><i class='el-icon-delete'></i>重置</el-button> -->
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <div class="forms_table_title"><i class="el-icon-s-data"></i>列表</div>
    <el-table
      ref="multipleTable"
      @sort-change="handleSortChange"
      :data="tableData"
      border
      stripe
      v-loading="tableLoading"
      style="width: 100%"
    >
      <el-table-column
        type="index"
        label="序号"
        fixed
        align="center"
        width="60"
      >
      </el-table-column>
      <el-table-column
        prop="nameLog"
        sortable="custom"
        show-overflow-tooltip
        label="校验项"
        width="200"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.nameLog | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="flag"
        sortable="custom"
        show-overflow-tooltip
        label="校验状态"
        width="200"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <!-- <span>{{ scope.row.flag | noDataFilter }}</span> -->
          <span v-if="scope.row.flag==0">校验成功</span>
          <span v-if="scope.row.flag==-1" style="color:red;">校验失败</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="errorInfo"
        show-overflow-tooltip
        label="校验备注"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.errorInfo | noDataFilter }}</span>
        </template>
      </el-table-column>
    </el-table>
    <Pagination
      :total="total"
      :page="formInline.pageNum"
      :limit="formInline.pageSize"
      @pagination="Pagination"
    ></Pagination>
  </div>
</template>

<script>
import commonFun from '@/filters/new_common';
import Pagination from "@/components/Pagination";
import pageApi from "@/api/xbrl/xbrl";
export default {
  name: "checkDetail",
  components: { Pagination },
  data() {
    return {
      formInline: {
        recordId: "",
        flag: "",
        orderString: "",
        pageSize: 50,
        pageNum: 1,
      },
      total:0,
      tableLoading: false,
      tableData: [],
    };
  },
  props: {
    PageData: {
      recordId: "",
    },
  },
  mounted() {
    // console.log("mounted");
    this.formInline.recordId = this.PageData.recordId;
    this.onSubmit(true);
  },
  methods: {
    onSubmit(flag) {
      this.tableLoading = true;
      if(flag) this.formInline.pageNum = 1;
      let params = commonFun.parameterSrc(this.formInline);
      // console.log("params",params);
      pageApi.findCheckInfo(params).then(res=>{
        if(res.data.status==0){
          let data = res.data.data;
          this.tableData = data.list;
          this.total = data.total;
        }else{
          this.$message({
            type:"error",
            message:res.data.message || '查询列表失败！'
          })
          this.tableData = [];
          this.total = 0;
        }
        this.tableLoading = false;
      }).catch((err)=>{
        console.log("err",err);
        this.tableLoading = false;
      })
    },
    selectChange() {
      this.onSubmit(true);
    },
    handleSortChange(val) {
      this.formInline.orderString = commonFun.orderByString(val);
      this.onSubmit(false);
    },
    Pagination(val){
      this.formInline.pageSize = val.limit;//页面条数
      this.formInline.pageNum = val.page;//页码
      this.onSubmit(false);
    }
  },
};
</script>

<style>
</style>
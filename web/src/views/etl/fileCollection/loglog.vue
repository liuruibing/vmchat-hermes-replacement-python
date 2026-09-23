<template>
  <div class="log_log">
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
        prop="userName"
        sortable="custom"
        show-overflow-tooltip
        label="操作用户"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.userName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="operationType"
        sortable="custom"
        show-overflow-tooltip
        label="操作类型"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.operationType | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="operationStatus"
        sortable="custom"
        show-overflow-tooltip
        label="操作状态"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.operationStatus === '1'" style="color: #7095d7"
            >操作成功</span
          >
          <span
            v-else-if="scope.row.operationStatus === '2'"
            style="color: #e74d4d"
            >操作失败</span
          >
          <span
            v-else-if="scope.row.operationStatus === '0'"
            style="color: #6fc5dc"
            >正在进行</span
          >

          <span v-else>{{ scope.row.operationStatus | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="beginTime"
        sortable="custom"
        show-overflow-tooltip
        label="操作开始时间"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.beginTime | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="endTime"
        sortable="custom"
        show-overflow-tooltip
        label="操作结束时间"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.endTime | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="remark"
        sortable="custom"
        show-overflow-tooltip
        label="日志信息"
        min-width="140"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.remark | noDataFilter }}</span>
        </template>
      </el-table-column>
    </el-table>
    <div style="height:50px;">
      <Pagination
        :total="total"
        :page="formInline.pageNum"
        :limit="formInline.pageSize"
        @pagination="pagination"
      ></Pagination>
    </div>
  </div>
</template>

<script>
import pageApi from "@/api/fileCollection";
import Pagination from "@/components/Pagination";
export default {
  components:{
    Pagination
  },
  data(){
    return{
      tableData:[],
      formInline:{
        pageNum:1,
        pageSize:50,
        orderString:""
      },
      total:0,
      tableLoading:false,
      recordId:""
    }
  },
  methods:{
    init(data){
      this.recordId = data;
      this.onSubmit();
    },
    onSubmit(){
      let params = this.$fun.parameterSrc(this.formInline);
      params.recordId = this.recordId;

      // 表格加载显示
      this.tableLoading = true;
      pageApi
        .getOperationLog(params)
        .then((res) => {
          if (res.data.status === 0) {
            this.tableData = res.data.data.list;
            // 页面总条数
            this.total = res.data.data.total;
          } else {
            this.tableData = [];
            this.total = 0;
            this.formInline.pageSize = 50;
            this.formInline.pageNum = 1;
          }
          // 表格加载显示
          this.tableLoading = false;
        })
        .catch(() => {
          // 表格加载显示
          this.tableLoading = false;
          this.tableData = [];
          this.total = 0;
          this.formInline.pageSize = 50;
          this.formInline.pageNum = 1;
        });

    },
    // 分页
    pagination(val) {
      let { page, limit } = val;
      this.formInline.pageNum = page;
      this.formInline.pageSize = limit;
      this.onSubmit();
    },
    // 排序
    handleSortChange(val) {
      this.formInline.orderString = this.$fun.orderByString(val);
      this.onSubmit();
    },
  }
};
</script>

<style>
</style>
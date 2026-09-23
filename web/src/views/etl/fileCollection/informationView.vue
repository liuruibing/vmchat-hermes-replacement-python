<template>
  <div class="information_view">
    <el-form
      :inline="true"
      :model="formInline"
      :rules="formInlineRules"
      class="formInline"
      ref="formInline"
    >
      <el-row>
        <el-col :span="16">
          <!-- 查询 -->
          <div class="grid-content bg-purple">
            <el-form-item label="文件日期" prop="fileDate">
              <el-date-picker
                size="small"
                :clearable="false"
                v-model="formInline.fileDate"
                type="date"
                value-format="yyyy-MM-dd"
                placeholder="选择日期"
                @change="fileDateChange"
              >
              </el-date-picker>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="8">
          <el-form-item class="search_button_com">
            <el-button
              type="primary"
              class="mb5"
              size="small"
              @click="onQueryValidate(true)"
              >查询</el-button
            >

            <el-button type="warning" class="mb5" size="small" @click="batchExecutionValidate" :loading="batchExecution_loading"
              >批量执行</el-button
            >
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <el-table
      ref="Table"
      :data="tableData"
      border
      stripe
      @sort-change="handleSortChange"
      @selection-change="handleSelectionChange"
      v-loading="tableLoading"
      style="width: 100%"
    >
      <el-table-column
        type="selection"
        width="35"
        align="center"
      ></el-table-column>

      <el-table-column
        prop="fId"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="序号"
        width="50"
        type="index"
        align="center"
      >
      </el-table-column>

      <el-table-column
        prop="agencyName"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="机构名称"
        min-width="150"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.agencyName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="procName"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="清洗项"
        min-width="150"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.procName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <!-- <el-table-column
        prop="fileName"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="清洗类型"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fileName | noDataFilter }}</span>
        </template>
      </el-table-column> -->

      <el-table-column
        prop="execStatusName"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="清洗状态"
        min-width="150"
        header-align="center"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.execStatusName=='执行成功'" style="color:#67C23A;">{{ scope.row.execStatusName | noDataFilter }}</span>
          <span v-else-if="scope.row.execStatusName=='执行失败'" style="color:red;">{{ scope.row.execStatusName | noDataFilter }}</span>
          <span v-else-if="scope.row.execStatusName=='未执行'" style="color:#909399;">{{ scope.row.execStatusName | noDataFilter }}</span>
          <span v-else>{{ scope.row.execStatusName | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="busiDate"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="文件日期"
        min-width="150"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.busiDate | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="execBeginTime"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="开始时间"
        min-width="150"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.execBeginTime | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="execEndTime"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="结束时间"
        min-width="150"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.execEndTime | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column label="操作" fixed="right" width="200" align="center">
        <template slot-scope="scope">
          <el-button type="primary" size="small" @click="loglog(scope.row)"
            >操作日志</el-button
          >
          <el-button
            type="danger"
            plain
            size="small"
            @click="beginRun(scope.row)"
            :loading="batchExecution_loading"
            >执行</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <Pagination
      :total="total"
      :page="formInline.pageNum"
      :limit="formInline.pageSize"
      @pagination="pagination"
    ></Pagination>

    <!-- 操作日志 -->
    <el-dialog
      title="操作日志"
      :visible.sync="dialogVisible"
      width="70% !important"
      center
      @closed="closed"
    >
      <logLog 
        v-if="logLog_show"
        ref="logLog"
      ></logLog>
    </el-dialog>
  </div>
</template>

<script>
import logLog from "./loglog.vue"
import Pagination from "@/components/Pagination";
import pageApi from "@/api/etl/fileCollection";
export default {
  components: {
    Pagination,
    logLog
  },
  data() {
    return {
      formInline: {
        fileDate: this.getTime(),
        pageNum: 1,
        pageSize: 50,
        orderString: "",
      },
      total: 0,
      agencyCodeArr: [],
      tableData: [
        // {
        //   fileType: "资讯清洗项",
        //   agencyName: "国泰君安",
        //   fileName11: "失败",
        //   aaaa: "2021-11-11 13:23:04",
        //   bbbb: "2021-11-11 13:25:33",
        //   id:"sasasas"
        // },
        // {
        //   fileType: "资讯清洗项",
        //   agencyName: "国泰君安",
        //   fileName11: "失败",
        //   aaaa: "2021-11-11 13:23:04",
        //   bbbb: "2021-11-11 13:25:33",
        //   id:"sasasqqqqqqas"
        // },
      ],
      procIds:[],
      tableLoading: false,
      batchExecution_loading:false,
      formInlineRules: {
        fileDate: {
          required: true,
          message: "请选择文件日期",
          trigger: "change",
        },
      },
      dialogVisible:false,
      logLog_show:false,
    };
  },
  mounted(){
    // this.$bus.$on('transition1',(data)=>{
    //   console.log('咨询',data);
    //   this.formInline.fileDate = data+'' || ''
    //   this.onQueryValidate();
    // })
    // this.onQueryValidate();
  },
  methods: {
    init(data){
      // console.log(data,'init-咨询');
      this.formInline.fileDate = data+'' || ''
      this.onQueryValidate();
    },
    fileDateChange(data){
      if(data){
        this.$emit('fileDateChange',data)
      }
    },
    getTime () {
      var date = new Date()
      var y = date.getFullYear()
      var m = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1)
      var d = (date.getDate() < 10 ? '0' + (date.getDate()) : date.getDate())
      return y + '-' + m + '-' + d
    },
    onQueryValidate(flag) {
      this.$refs["formInline"].validate((valid) => {
        if (valid) {
          this.onQuery(flag);
        } else {
          return false;
        }
      });
    },
    onQuery(flag) {
      if (flag) {
        this.formInline.pageNum = 1;
      }
      this.tableLoading = true;
      let params = JSON.parse(JSON.stringify(this.formInline));
      pageApi
        .procZxList(params)
        .then((res) => {
          this.tableLoading = false;
          if (res.data.status === 200) {
            this.tableData = res.data.data.list;
            this.total = res.data.data.total;
          } else {
            this.tableData = [];
            this.total = 0;
            this.$message.closeAll();
            this.$message({
              type: "error",
              message: res.data.message || "获取列表数据失败！",
            });
          }
        })
        .catch(() => {
          this.tableLoading = false;
        });
    },
    // 排序
    handleSortChange(val) {
      this.formInline.orderString = this.$fun.orderByString(val);
      this.onQueryValidate(false);
    },
    //  分页
    pagination(val) {
      let { page, limit } = val;
      this.formInline.pageNum = page;
      this.formInline.pageSize = limit;
      this.onQueryValidate(false);
    },
    handleSelectionChange(val) {
      let arr = val.map(item=>{
        return item.id
      })
      this.procIds = arr;
    },
    // 批量执行
    batchExecutionValidate(){
      this.$refs["formInline"].validate((valid) => {
        if (valid) {
          this.batchExecution();
        } else {
          return false;
        }
      });
    },
    batchExecution(){
      if(!this.procIds.length){
        this.$message({
          type:"warning",
          message:"请至少选择一条数据！"
        })
        return
      }
      this.batchExecution_loading = true;
      let obj = JSON.parse(JSON.stringify(this.formInline));
      let params = {};
      params.fileDate = obj.fileDate;
      params.procIds = this.procIds;
      pageApi
        .executeProcZx(params)
        .then((res) => {
          this.batchExecution_loading = false;
          if(res.data.status===200){
            this.$message({
              type:"success",
              message:"执行成功！"
            })
            this.$refs.Table.clearSelection();
            this.procIds = [];
          }else{
            this.$message({
              type:"error",
              message:res.data.message || "执行失败！"
            })
          }
        })
        .catch(() => {
          this.batchExecution_loading = false;
        });
    },
    beginRun(row) {
      let arr = [];
      arr.push(row.id);
      this.procIds = arr;
      this.batchExecutionValidate();
    },
    loglog(row){
      this.dialogVisible = true;
      this.logLog_show = true;
      this.$nextTick(()=>{
        this.$refs.logLog.init(row.id);
      });
    },
    closed(){
      this.logLog_show = false;
    }
    
  },
};
</script>

<style>
</style>
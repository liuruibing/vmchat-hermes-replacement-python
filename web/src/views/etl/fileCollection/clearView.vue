<template>
  <div class="dataClearTable">
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

            <el-form-item label="基金服务机构" prop="agencyCode">
              <el-select
                v-model="formInline.agencyCode"
                size="small"
                placeholder="请选择"
              >
                <el-option
                  v-for="(group, index) in agencyCodeArr"
                  :value="group.agencyCode"
                  :key="index"
                  :label="group.agencyName"
                >
                </el-option>
              </el-select>
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

            <el-button type="warning" class="mb5" size="small" @click="againPerformValidate" :loading="againPerform_loading"
              >重新执行</el-button
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
      v-loading="tableLoading"
      style="width: 100%"
    >
      <!-- <el-table-column
        type="selection"
        width="35"
        align="center"
      ></el-table-column> -->

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

      <el-table-column
        prop="procType"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="清洗类型"
        min-width="150"
        header-align="center"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.procType=='1'">其他过程</span>
          <span v-else-if="scope.row.procType=='3'">业务指标校验过程</span>
          <span v-else-if="scope.row.procType=='5'">基础指标校验过程</span>
          <span v-else-if="scope.row.procType=='7'">AODS到SODS</span>
          <span v-else-if="scope.row.procType=='9'">数据合规过程</span>
          <span v-else-if="scope.row.procType=='Z'">资讯过程</span>
          <span v-else>{{ scope.row.procType | noDataFilter }}</span>
          <span></span>
        </template>
      </el-table-column>

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

      <el-table-column label="操作" fixed="right" min-width="160" align="center">
        <template slot-scope="scope">
          <el-button type="primary" size="small" @click="loglog(scope.row)">操作日志</el-button>
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
import Pagination from '@/components/Pagination'
import pageApi from "@/api/etl/fileCollection";
export default {
  components:{
    Pagination,
    logLog
  },
  data(){
    return{
      formInline:{
        pageNum:1,
        pageSize:50,
        orderString:"",
        fileDate:this.getTime(),
        agencyCode:"GTJA"
      },
      total:0,
      agencyCodeArr:[
        {agencyCode:"GTJA",agencyName:"国泰君安"},
        {agencyCode:"ZX",agencyName:"资讯"},
      ],
      tableData:[
        // {fileName121:"估值",fileType:"测试清洗项",agencyName:"国泰君安",fileName11:"已完成",aaaa:"2021-11-11 13:23:04",bbbb:"2021-11-11 13:25:33"}
      ],
      tableLoading:false,
      againPerform_loading:false,
      formInlineRules: {
        fileDate: {
          required: true,
          message: "请选择文件日期",
          trigger: "change",
        },
        agencyCode:{
          required: true,
          message: "请选择基金服务机构",
          trigger: "change",
        }
      },
      dialogVisible:false,
      logLog_show:false,
    }
  },
  mounted(){
    // this.$bus.$on('transition1',(data)=>{
    //   console.log('清洗',data);
    //   this.formInline.fileDate = data+'' || ''
    //   this.onQueryValidate();
    // })
    this.getAgencyList();
  },
  methods:{
    init(data){
      // console.log(data,'init-清洗');
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
    // 获取基金服务机构
    getAgencyList() {
      pageApi
        .getAgencyList()
        .then((res) => {
          this.agencyCodeArr = res.data.data;
        })
        .catch(() => {});
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
        .procList(params)
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
    // 重新执行
    againPerformValidate(){
      this.$refs["formInline"].validate((valid) => {
        if (valid) {
          this.againPerform();
        } else {
          return false;
        }
      });
    },
    againPerform(){
      this.againPerform_loading = true;
      let obj = JSON.parse(JSON.stringify(this.formInline));
      let params = {};
      params.fileDate = obj.fileDate;
      params.agencyCode = obj.agencyCode;
      pageApi
        .executeProc(params)
        .then((res) => {
          this.againPerform_loading = false;
          if(res.data.status===200){
            this.$message({
              type:"success",
              message:"执行成功！"
            })
            this.onQuery(true);
          }else{
            this.$message({
              type:"error",
              message:res.data.message || "执行失败！"
            })
          }
        })
        .catch(() => {
          this.againPerform_loading = false;
        });
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
  }
};
</script>

<style>
</style>
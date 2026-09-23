<template>
  <div class="files_table ddportal-ui">
    <el-table
      ref="multipleTable"
      @selection-change="handleSelectionChange"
      :data="tableData"
      border
      stripe
      @sort-change="handleSortChange"
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
        min-width="70"
        type="index"
        header-align="center"
      >
      </el-table-column>

      <el-table-column
        prop="agencyName"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="基金服务机构"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.agencyName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fileType"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="文件类型"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fileType | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fileName"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="文件名称"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fileName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fileDate"
        show-overflow-tooltip
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        label="文件日期"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fileDate | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fileStatus"
        show-overflow-tooltip
        label="文件状态"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fileStatus | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fileUpdateTime"
        show-overflow-tooltip
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        label="文件更新时间"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fileUpdateTime | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="execStatus"
        show-overflow-tooltip
        label="文件执行状态"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.execStatus == '未执行'" style="color: ">{{
            scope.row.execStatus | noDataFilter
          }}</span>
          <span
            v-if="scope.row.execStatus == '正在执行'"
            style="color: #6fc5dc"
            >{{ scope.row.execStatus | noDataFilter }}</span
          >
          <span
            v-if="scope.row.execStatus == '执行成功'"
            style="color: #7095d7"
            >{{ scope.row.execStatus | noDataFilter }}</span
          >
          <span
            v-if="scope.row.execStatus == '执行失败'"
            style="color: #e74d4d; font-weight: 700"
            >{{ scope.row.execStatus | noDataFilter }}</span
          >
        </template>
      </el-table-column>

      <el-table-column
        prop="extractTime"
        show-overflow-tooltip
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        label="执行时间"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.extractTime | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        label="操作"
        fixed="right"
        min-width="160"
        align="center"
      >
        <template slot-scope="scope">
          <el-button
            type="primary"
            size="small"
            @click="operationLogData(scope.row)"
            >操作日志</el-button
          >
          <el-button
            type="danger"
            plain
            size="small"
            @click="implementData(scope.row)"
            >执行</el-button
          >
          <el-button
            type="danger"
            plain
            size="small"
            @click="lookData(scope.row)"
            >数据查看</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div style="height:55px;">
      <Pagination
        :total="total"
        :limit="formQuery.pageSize"
        :page="formQuery.pageNum"
        @pagination="pagination"
      ></Pagination>
    </div>

    <el-dialog
      width="70% !important"
      :title="operationLogTitle"
      center
      :visible.sync="operationLogDialog"
      :close-on-click-modal="false"
    >
      <el-container>
        <el-main class="mainBox">
          <el-table
            ref="multipleTable1"
            @sort-change="handleSortChange1"
            :data="tableData1"
            border
            stripe
            v-loading="tableLoading1"
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
                <span
                  v-if="scope.row.operationStatus === '1'"
                  style="color: #7095d7"
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

                <span v-else>{{
                  scope.row.operationStatus | noDataFilter
                }}</span>
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
          <Pagination
            :total="total1"
            :page="formInline.pageNum"
            :limit="formInline.pageSize"
            @pagination="pagination1"
          ></Pagination>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="operationLogDialog = false"
          >取 消</el-button
        >
        <!-- <el-button type="primary" :loading="sqlResultDialogLoading" size="small" @click="countCopySubmit('formCopyCount','sure')">确定复制</el-button> -->
      </div>
    </el-dialog>

    <xbrlDialog v-show="true" ref="xbrlInDdui" />
  </div>
</template>

<script>
import Pagination from "@/components/Pagination";
import commonApi from "@/api/fileCollection";
import fun from "@/filters/common";
import store from "@/store";
import xbrlDialog from "@/views/ann/annreportDialog.vue";
export default {
  name: "filesTable",
  components: {
    Pagination,
    xbrlDialog,
  },
  props: {
    baseApi: {
      type: String,
    },
    token: {
      type: String,
    },
    Query:{
      fileDate:"",
      agencyCode:""
    }
  },
  data() {
    return {
      operationLogTitle: "操作日志",
      operationLogDialog: false,

      tableData: [], //表格数据
      tableData1: [],
      tableLoading: false, //表格加载
      tableLoading1: false, //表格加载
      agencyCodeArr: [],
      // //总条数
      total: 0,
      total1: 0,
      // 顶部查询条件
      formQuery: {
        // 机构编码
        agencyCode: "",
        // 机构名称
        agencyName: "",
        // 文件类型
        fileType: "",
        // 文件日期
        fileDate: "",
        // 文件状态
        fileStatus: "",
        //执行状态
        execStatus: "",
        // 排序字段
        orderBy: "",
        // 起始页
        pageNum: 1,
        // 每页大小
        pageSize: 50,
      },

      formInline: {
        // 排序字段
        orderString: "",
        // 起始页
        pageNum: 1,
        // 每页大小
        pageSize: 50,
      },
      // 弹窗查询参数
      formDialog: {},

      // 弹窗验证规则
      dialogRules: {},
      searchRules: {
        //  agencyCode:[
        //    { required: true, type: 'string', message: "请选择基金服务机构编码", trigger: "change" }
        //  ],
        //  fileDate:[
        //    { required: true, type: 'string', message: "请选择日期", trigger: "change" }
        //  ],
        //  fileType:[
        //    { required: true, type: 'string', message: "请选择文件类型", trigger: "change" }
        //  ],
      },

      // 操作类型 1、添加 2、编辑
      operationType: 1,
      formLabelWidth: "100px",
      // 批量执行的数据
      multipleSelection: [],
    };
  },
  watch: {
    // 获取baseApi
    baseApi: function (newData) {
      store.commit("BASE_API", this.baseApi);
    },
    // 获取token
    token: function (newData) {
      store.commit("TOKEN", this.token);
      //获取完token之后再请求列表信息
      // 默认查询
      //    this.getAgencyList();
      //   //  this.getdatatime();
      //  this.onQuery(true);
      //  this.getAgencyList();
      // 获取任务类型集合
      // this.getList();
    },
  },
  mounted() {
    // this.getAgencyList();
    //  this.getdatatime();
    
    this.onQuery(true);
  },
  methods: {
    getTime() {
      var date = new Date();
      var y = date.getFullYear();
      var m =
        date.getMonth() + 1 < 10
          ? "0" + (date.getMonth() + 1)
          : date.getMonth() + 1;
      var d = date.getDate() < 10 ? "0" + date.getDate() : date.getDate();
      return y + "-" + m + "-" + d;
    },
    // 日期快捷选项
    dateShortcut() {
      return fun.dateShortcut();
    },

    //操作日志
    operationLogData(row) {
      this.operationLogDialog = true;

      let params = fun.parameterSrc(this.formInline);
      params.recordId = row.id;

      // 表格加载显示
      this.tableLoading1 = true;
      commonApi
        .getOperationLog(params)
        .then((response) => {
          if (response.data.status === 0) {
            this.tableData1 = response.data.data.list;
            // 页面总条数
            this.total1 = response.data.data.total;
          } else {
            this.tableData1 = [];
            this.total1 = 0;
            this.formInline.pageSize = 50;
            this.formInline.pageNum = 1;
          }
          // 表格加载显示
          this.tableLoading1 = false;
        })
        .catch(() => {
          // 表格加载显示
          this.tableLoading1 = false;
          this.tableData1 = [];
          this.total1 = 0;
          this.formInline.pageSize = 50;
          this.formInline.pageNum = 1;
        });

      //查询
    },
    //执行
    implementData(row) {
      this.$confirm("确认执行吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          let ids = [];
          ids.push(row.id);
          let params = {};
          params.ids = ids;

          commonApi
            .executeFile(params)
            .then((res) => {
              if (res.data.status === 200) {
                this.onQuery(false);
                this.$message.closeAll();

                this.$message({
                  type: "success",
                  message: "执行成功",
                });
              } else {
                this.$message.closeAll();

                this.$message.error(res.data.message);
              }
            })
            .catch(() => {});
        })
        .catch(() => {});
    },
    //数据查看
    lookData(row) {
      let params = {};
      params.reportId = row.reportCode;
      params.agencyCode = row.agencyCode;
      params.fileDate = row.fileDate;
      if (row.reportCode == "") {
        this.$message({
          message: "报告编码为空",
          type: "warning",
        });
        return;
      } else {
        this.$refs.xbrlInDdui.editData(params);
      }
    },

    handleSelectionChange(val) {
      this.multipleSelection = val;
    },
    handleSortChange(val) {
      this.formQuery.orderString = fun.orderByString(val);

      this.onQuery(false);
    },

    handleSortChange1() {},

    //批量执行
    batchImplement() {
      if (this.multipleSelection.length == 0) {
        this.$message({
          message: "请至少选择一条",
          type: "warning",
        });
        return;
      } else {
        this.$confirm("确认执行吗?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
          confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
        })
          .then(() => {
            let ids = [];
            for (let i = 0; i < this.multipleSelection.length; i++) {
              ids.push(this.multipleSelection[i].id);
            }
            let params = {};
            params.ids = ids;

            commonApi
              .executeFile(params)
              .then((res) => {
                if (res.data.status === 200) {
                  this.onQuery(false);
                  this.$message.closeAll();

                  this.$message({
                    type: "success",
                    message: "执行成功",
                  });
                } else {
                  this.$message.closeAll();

                  this.$message.error(res.data.message);
                }
              })
              .catch(() => {});
          })
          .catch(() => {});
      }
    },

    // 获取基金服务机构
    getAgencyList() {
      commonApi
        .getAgencyList()
        .then((res) => {
          this.agencyCodeArr = res.data.data;
        })
        .catch(() => {});
    },
    // 查询

    onQuery(flag) {
      this.tableLoading = true;
      if (flag) {
        this.formQuery.pageNum = 1;
      }
      //  this.getAgencyList();
      //  this.$refs[formName].validate((valid) => {
      //     if (valid) {
      // if(pageNumOne === true){
      //     this.formQuery.pageNum = 1; //重新搜索初始页面为首页
      // }
      // else{}
      // 消除没有值的参数
      this.formQuery.fileDate = this.Query.fileDate || "";
      this.formQuery.agencyCode = this.Query.agencyCode || "";
      let params = fun.parameterSrc(this.formQuery);
      // 表格加载显示
      // this.tableLoading = true;
      commonApi
        .getFileExtract(params)
        .then((response) => {
          if (response.data.status === 0) {
            this.tableData = response.data.data.list;
            // 页面总条数
            this.total = response.data.data.total;
            this.$emit("getFileTable",response.data.data.list)
          } else {
            this.tableData = [];
            this.total = 0;
            this.formQuery.pageSize = 50;
            this.formQuery.pageNum = 1;
          }
          // 表格加载显示
          this.tableLoading = false;
        })
        .catch(() => {
          // 表格加载显示
          this.tableLoading = false;
          this.tableData = [];
          this.total = 0;
          this.formQuery.pageSize = 50;
          this.formQuery.pageNum = 1;
        });

      //   //   } else {
      //   //   return false;
      //   // }
      // })
    },

    //  分页
    pagination(val) {
      let { page, limit } = val;
      // 起始页
      this.formQuery.pageNum = page;
      // 每页数量
      this.formQuery.pageSize = limit;
      // 查询
      this.onQuery(false);
    },

    pagination1(val) {
      let { page, limit } = val;
      // 起始页
      this.formInline.pageNum = page;
      // 每页数量
      this.formInline.pageSize = limit;
      // 查询
      // this.onQuery(false);
    },
  },
};
</script>

<style lang="scss">
// .files_table {
//   .el-dialog {
//     width: 60% !important;
//     .el-form {
//       width: 100% !important;
//       font-size: 0;
//     }
//     .el-input {
//       // width: 120% !important;
//     }
//     .el-form-item {
//       min-width: 50%;
//       margin-right: 0;
//     }
//     .mr5 {
//       margin-right: 5px;
//     }
//   }

//   .mb20 {
//     margin-bottom: 15px !important;
//   }

//   // 火狐移除
//   input[type="number"] {
//     -moz-appearance: textfield;
//   }

//   //谷歌下的移除
//   input[type="number"]::-webkit-inner-spin-button,
//   input[type="number"]::-webkit-outer-spin-button {
//     -webkit-appearance: none;
//   }
// }
</style>
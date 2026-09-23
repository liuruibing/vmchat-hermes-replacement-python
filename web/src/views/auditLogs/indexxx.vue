<template>
  <!-- 漂移 -->
  <div class="auditLogsxx analyse-page" v-auto-enter>
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formQuery" :inline="true" :model="formQuery" class="standard-form">
          <el-row>
            <el-form-item prop="watchUser">
              <el-input v-model.trim="formQuery.watchUser" clearable placeholder="请输入用户" size="small" />
            </el-form-item>
            <el-form-item prop="menuName">
              <el-input v-model.trim="formQuery.menuName" clearable placeholder="请输入功能名称" size="small" />
            </el-form-item>
            <el-form-item prop="reqUrl">
              <el-input v-model.trim="formQuery.reqUrl" clearable placeholder="请输入URL" size="small" />
            </el-form-item>
            <el-form-item label="" prop="beginDate" class="mb20">
              <el-date-picker
                v-model="formQuery.beginDate"
                style="width:174px"
                type="date"
                size="small"
                value-format="yyyy-MM-dd"
                placeholder="选择开始时间"/>
            </el-form-item>
            <el-form-item label="" prop="endDate" class="mb20">
              <el-date-picker
                v-model="formQuery.endDate"
                style="width:174px"
                type="date"
                size="small"
                value-format="yyyy-MM-dd"
                placeholder="选择结束时间"/>
            </el-form-item>
            <el-form-item class="">
              <el-button type="primary" size="small" icon="el-icon-search" @click="onSubmit('formQuery')">查询</el-button>
              <el-button type="info" size="small" icon="el-icon-refresh" plain @click="resetForm('formQuery')">重置</el-button>
              <el-button type="info" size="small" plain :icon="exportLoading ? 'el-icon-loading' : 'el-icon-download'" :disabled="isDisabled" @click="downloadTableExcel">
                {{ downLoadText }}
              </el-button>
            </el-form-item>
          </el-row>
        </el-form>
      </div>
    </div>

    <el-row>
      <el-col :span="16">
        <div class="page-model-title">
          <div class="title-icon">
            <div class="color-box"></div>
          </div>
          <span class="title-txt">操作日志-明细</span>
        </div>
      </el-col>
<!--      <el-col :span="8">
        <div style="float: right">
          <vxe-toolbar ref="tableToolbar" class="standard-vxe-toolbar" :custom="{ immediate: true }" custom />
        </div>
      </el-col>-->
    </el-row>

    <el-row id="standard-table">
      <div id="standard-table-margin">
        <vxe-table
          ref="table1"
          :sort-config="{ remote: true }"
          :loading="tableLoading"
          :custom-config="{ storage: true }"
          :height="tableHeight"
          :data="tableData"
          :cell-style="{ height: '50px' }"
          show-header-overflow
          auto-resize
          show-overflow
          stripe
          @sort-change="handleSortChange"
          resizable
        >
          <vxe-table-column type="seq" title="序号" width="60" header-align="center" />
          <vxe-table-column field="watchUser" title="用户" min-width="150" header-align="center" align="center" />
          <vxe-table-column field="watchTime" title="访问时间" min-width="150" header-align="center" align="center" />
          <vxe-table-column field="menuName" title="功能名称" min-width="150" header-align="center" align="center" />
          <vxe-table-column field="reqIp" title="IP" min-width="150" header-align="center" align="center" />
          <vxe-table-column field="reqUrl" title="URL" min-width="150" header-align="center" align="center" />
          <vxe-table-column field="bodyParam" title="body参数" min-width="250" header-align="center" align="center" />

        </vxe-table>
        <vxe-pager
          :current-page="formQuery.pageNum"
          :page-size="formQuery.pageSize"
          :total="total"
          :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
          border
          size="medium"
          class="standard-vxe-pager"
          @page-change="pagination"
        />
      </div>
    </el-row>
  </div>
</template>
<script type="text/ecmascript-6">
import Pagination from "@/components/Pagination";
import auditLogsApi from "@/api/auditLogs/index";
import { downLoadFileByUrlPost } from '@/utils'
import moment from 'moment'
export default {
  name: "auditLogsxx",
  components: {
    Pagination
  },
  data() {
    return {

      // 搜索
      formQuery: {
        // 起止日期
        beginDate: moment().format("YYYY-MM-DD"),
        endDate: "",
        menuName: "",
        watchUser: "",
        reqUrl: "",
        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10,
        orderString: ""
      },


      // 表格高度
      tableHeight: 0,
      // 表格数据
      tableData: [],
      issearchButton: false,
      tableLoading: false,
      total: 0,

      /* 按钮禁止与否 */
      isDisabled: false,
      // 导出图标
      downLoadIcon: "el-icon-download",
      // 导出提示文字
      downLoadText: "导出",
      exportLoading: false,

      exportButton: false,
      exportText: "导出",
      exportIcon: "el-icon-download"
    };
  },
  created() {
      this.onQuery();
  },
  mounted() {
    // 动态设置表格高度
    this.handleTableHeight()
    // 默认查询
    //this.onQuery()
  },

  methods: {
    /**
     * @description 动态设置表格高度
     */
    handleTableHeight() {
      this.$nextTick(() => {
        // 根据浏览器高度设置初始高度
        this.tableHeight = window.innerHeight - this.$refs.table1.$el.offsetTop - 285
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.table1.$el.offsetTop - 285
        }
      })
    },
    onSubmit(formName) {
      var self = this;
      self.formQuery.pageNum = 1;
      self.$refs[formName].validate((valid) => {
        if (valid) {
          self.onQuery();
          // 禁用搜索按钮
          self.$fun.searchButtonDisabled("issearchButton", self);
        } else {
          return false;
        }
      });
    },

    onQuery(flag) {
      var self = this;
      const params = Object.assign({}, this.formQuery, {});

      if (!flag) {
        this.tableLoading = true;
      }
      new Promise((resolve, reject) => {
        auditLogsApi
          .fun_selectAuditLogsxx(params)
          .then((res) => {
            const { status, data } = res;
            if (status === 0) {
              if (data != null && data != undefined) {
                if (!flag) {
                  const { list, total } = data;
                  this.tableData = list;
                  this.total = total;
                }
              }
            } else {
              self.$message({
                message: "系统异常",
                type: "warning"
              });
            }
            this.tableLoading = false;
            self.exportLoading = false;
            self.isDisabled = false;
            self.downLoadText = "导出";
          })
          .catch((error) => {
            this.tableLoading = false;
            self.exportLoading = false;
            self.isDisabled = false;
            self.downLoadText = "导出";
            reject(error);
          });
      });
    },
    // 导出
    downloadTableExcel() {
      this.downLoadText = "导出中...";
      this.exportLoading = true;
      this.isDisabled = true;
      const params = Object.assign({}, this.formQuery)
      delete params.fundName;
      const fileName = '操作日志-详细.xlsx'
      const url = '/api/AuditLogs/xx/select/export'
      downLoadFileByUrlPost(url, params, fileName, this)
      setTimeout(() => {
        this.exportLoading = false;
        this.isDisabled = false;
        this.downLoadText = "导出";
      }, 10000)
    },


    // 清除
    resetForm(formName) {
      this.$refs[formName].resetFields();
      this.formQuery.watchUser = "";
      this.formQuery.menuName = "";
      this.formQuery.reqUrl = "";
      this.formQuery.beginDate = "";
      this.formQuery.endDate = "";
    },
    // 分页点击事件
    pagination(val) {
      // let { page, limit } = val;
      const { currentPage, pageSize } = val;
      // 起始页
      this.formQuery.pageNum = currentPage;
      // 每页数量
      this.formQuery.pageSize = pageSize;
      // 查询
      this.onQuery();
    },
    // 当表格的排序条件发生变化的时候会触发该事件
    handleSortChange(val) {
      this.formQuery.orderString = this.$fun.queryOrderBy_vxe(val);
      // 查询
      this.onQuery();
    }
  }
};
</script>

<style lang="scss">
.auditLogsxx {
  .funds-filter {
    width: 100%;
    // border-bottom: 1px solid #e1e0e0;
  }
  .p1 {
    font-family: FZLanTingHei;
    font-weight: 500;
    font-size: 14px;
    color: rgb(16, 16, 16);
    font-style: normal;
    letter-spacing: 0px;
    line-height: 20px;
    text-decoration: none;
    text-align: left;
  }
  .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
  .title-style {
    color: #e03d3e;
    vertical-align: middle;
    height: 35px;
    line-height: 35px;
    font-size: 16px;
    margin-left: 5px;
  }
  .color-box {
    display: inline-block;
    height: 30px;
    width: 2px;
    background-color: #e03d3e;
  }
  input::-webkit-input-placeholder {
    color: #999 !important;
  }
  .customWidth {
    width: 70% !important;
  }

  .el-tabs__item {
    line-height: 50px !important;
    height: 50px !important;
  }
  .el-checkbox-button__inner {
    border: 0px solid !important;
    border-radius: 0px !important;
  }
  .el-checkbox-button--medium {
    margin-right: 10px;
  }
  .el-checkbox-group {
    float: left;
  }
  .item-label {
    font-size: 14px;
  }
  .el-checkbox-button--medium .el-checkbox-button__inner {
    font-size: 16px;
  }
  .customWidth {
    width: 70% !important;
  }
  .el-tabs__item {
    line-height: 50px !important;
    height: 50px !important;
  }
  .el-dialog {
    width: 54% !important;
    .el-form {
      width: 100% !important;
      font-size: 0;
    }
    .item-label {
      font-size: 14px;
    }
    .vxe-pager.size--medium {
      font-size: 14px;
    }
    .el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell {
      background: #f8f8f8;
    }

    .el-form-item {
      min-width: 50%;
      margin-right: 0;
    }
    .mr5 {
      margin-right: 5px;
    }
  }
}
</style>

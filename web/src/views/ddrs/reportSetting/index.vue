<template>
  <div class="report-setting page-card-common">
    <div class="page-top-box">
      <div class="search">
        <el-form
          ref="formQueryRef"
          :model="formQuery"
          :rules="rules"
          :inline="true"
          style="margin-bottom: 8px"
          label-width="65px"
        >
          <el-row>
            <el-form-item label="报表编码" prop="reportCode">
              <el-input v-model="formQuery.reportCode" size="small" placeholder="请输入报表编码" />
            </el-form-item>
            <el-form-item label="报表名称" prop="reportName">
              <el-input v-model="formQuery.reportName" size="small" placeholder="请输入报表名称" />
            </el-form-item>
            <!-- <el-form-item label="" prop="reportType">
              <el-select
                v-model="formQuery.reportType"
                clearable
                placeholder="请选择报表类型"
                size="small"
              >
                <el-option
                  v-for="item in reportTypeOptions"
                  :key="item.dimCde"
                  :label="item.dimNme"
                  :value="item.dimCde"
                >
                </el-option>
              </el-select>
            </el-form-item> -->
            <el-form-item label="报表状态" prop="status">
              <el-select
                v-model="formQuery.status"
                clearable
                placeholder="请选择报表状态"
                size="small"
              >
                <el-option
                  v-for="item in statusOptions"
                  :key="item.dimCde"
                  :label="item.dimNme"
                  :value="item.dimCde"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="">
              <btn-array
                :form-btn-array="formBtnArray"
                :show-type="0"
                @clickEvent="formClickHandle"
              />
            </el-form-item>
          </el-row>
        </el-form>
      </div>
      <div class="xToolbar-box-custom">
        <div class="forms_table_title"><i class="el-icon-s-data"></i> 自定义页面</div>
        <div style="display: flex; align-items: center">
          <span style="display: flex">
            <el-button
              size="small"
              type="primary"
              icon="el-icon-download"
              @click="dowmloadConfig"
              :loading="downloadLoading"
              >导出</el-button
            >
            <el-button size="small" type="primary" icon="el-icon-upload2" @click="openImportConfig"
              >导入</el-button
            >
          </span>
          <vxe-toolbar style="position: relative; right: 0px" custom ref="xToolbar"></vxe-toolbar>
        </div>
      </div>
    </div>

    <vxe-table
      ref="xTable"
      class="selfAdaptationTable"
      :data="tableData"
      :loading="tableLoading"
      border
      auto-resize
      size="mini"
      :max-height="selfAdaptationtHeight"
      show-overflow
      stripe
      :checkbox-config="{ checkMethod: ({ row }) => row.reportCode && row.version }"
    >
      <vxe-table-column type="checkbox" width="60" align="center" fixed="left"></vxe-table-column>
      <vxe-table-column
        v-for="(item, index) in columns"
        :key="index"
        :field="item.prop"
        :title="item.label"
        :align="item.align"
        :header-align="item.headerAlign"
        :width="item.width"
        :min-width="item.minWidth"
      >
        <template slot-scope="scope">
          <span v-if="item.prop === 'status'">
            <el-switch v-model="scope.row.statusBoolean" @change="handleSwitch(scope.row)" />
          </span>
          <span v-else>{{ scope.row[item.prop] | noDataFilter }}</span>
        </template>
      </vxe-table-column>
      <vxe-table-column title="操作" align="center" width="150px">
        <template slot-scope="scope">
          <el-link type="primary" icon="el-icon-edit" :underline="false" @click="editRow(scope.row)"
            >编辑</el-link
          >
          <el-link
            type="danger"
            icon="el-icon-delete"
            :underline="false"
            @click="delteRow(scope.row)"
            >删除</el-link
          >
        </template>
      </vxe-table-column>
    </vxe-table>
    <pagination
      :limit="formQuery.limit"
      :page="formQuery.pageNum"
      :total="formQuery.total"
      @pagination="pagination"
    />

    <!-- 导入配置 -->
    <el-upload
      ref="uploadRef"
      style="display: inline-block"
      action=""
      accept=".ser"
      :show-file-list="false"
      :http-request="importData"
    >
      <el-button size="small" type="primary" icon="el-icon-upload2" style="display: none"
        >导入</el-button
      >
    </el-upload>
  </div>
</template>
<script>
import pageConstantObj from "./constant/index";
import pageApi from "./api/api";
import btnArray from "@/components/btnArrayForNewUi";
import pagination from "@/components/Pagination";
import tableHeightMixins from "@/mixinsModel/tableHeight.js";
import commonApi from "@/api/common";

export default {
  name: "ReportSetting",
  mixins: [tableHeightMixins],
  components: { btnArray, pagination },
  data() {
    return {
      formQuery: {
        reportCode: "",
        reportName: "",
        reportType: "",
        status: "",
        limit: 10,
        offset: 0,
        pageNum: 1,
        total: 0
      },
      rules: {},
      reportTypeOptions: [],
      statusOptions: [
        {
          dimNme: "启用",
          dimCde: "1"
        },
        {
          dimNme: "禁用",
          dimCde: "0"
        }
      ],
      formBtnArray: pageConstantObj.formBtnArray,
      columns: pageConstantObj.TABLECOLUMNS,
      tableData: [],
      tableLoading: false,
      downloadLoading: false
    };
  },
  mounted() {},
  activated() {
    this.getTableData(true);
  },
  methods: {
    /**
     * @Description: 修改行数据状态
     * @author Liu Rui Bing
     * @date 2024/5/8
     */
    handleSwitch(row) {
      const status = row.statusBoolean ? "1" : "0";
      const params = {
        reportCode: row.reportCode,
        status: status
      };
      pageApi.updateRow(params).then((res) => {
        this.getTableData(false);
      });
    },
    /**
     * @Description: 编辑行数据
     * @author Liu Rui Bing
     * @date 2024/5/8
     */
    editRow(row) {
      // 获取 当前行对象 数据
      const params = { ...row };
      pageApi.getVersionRow(params).then((res) => {
        const { data } = res.data;
        if (data) {
          this.$router.push({
            path: "/template/reportConfig",
            query: {
              reportConfig: { ...data, ...row }
            }
          });
        } else {
          this.$message.closeAll();
          this.$message.warning("数据不存在,无法进入编辑");
        }
      });
    },

    /**
     * @Description: 删除行数据
     * @author Liu Rui Bing
     * @date 2024/5/8
     */
    delteRow(row) {
      this.$confirm("此操作将永久删除该数据, 是否继续?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          const params = { ...row };
          pageApi.deleteRow(params).then((res) => {
            this.$message({
              type: "success",
              message: "删除成功!"
            });
            this.getTableData(false);
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除"
          });
        });
    },
    pagination(val) {
      this.formQuery.pageNum = val.page;
      this.formQuery.limit = val.limit;
      this.formQuery.offset = (val.page - 1) * val.limit;
      this.getTableData(false);
    },
    formClickHandle(val) {
      if (val === "查询") {
        this.$refs["formQueryRef"].validate((valid) => {
          if (valid) {
            this.getTableData(true);
          } else {
            return false;
          }
        });
      }
      if (val === "新增") {
        this.$router.push({
          path: "/template/reportConfig"
        });
      }
      if (val === "重置") {
        this.formQuery.reportCode = "";
        this.formQuery.reportName = "";
        this.formQuery.reportType = "";
        this.formQuery.status = "";
      }
    },
    getTableData(flag) {
      if (flag) {
        this.formQuery.pageNum = 1;
        this.formQuery.offset = 0;
      }
      const params = Object.assign({}, this.formQuery);
      this.tableLoading = true;
      pageApi.getTableData(params).then((res) => {
        this.tableLoading = false;
        const { data } = res;
        if (data.rows && data.rows.length > 0) {
          data.rows.forEach((item) => {
            item.statusBoolean = item.status === "1";
          });
        }
        this.tableData = data.rows;
        this.formQuery.total = data.total;
      });
    },
    // 导出勾选的配置
    dowmloadConfig() {
      this.$message.closeAll();
      let checkArray = this.$refs.xTable.getCheckboxRecords(true) || [];
      if (!checkArray.length) {
        return this.$message.warning("至少选择一条数据！");
      }
      let configList = checkArray.map((item) => {
        return {
          reportCode: item.reportCode,
          version: item.version
        };
      });
      const url = "/api/reportQuickConfig/v1.0/export";
      this.downloadLoading = true;
      commonApi.downLoadFileByUrlPost(url, configList, "", () => {
        this.downloadLoading = false;
      });
    },
    // 打开导入
    openImportConfig() {
      const uploadInput = this.$refs.uploadRef.$el.querySelector('input[type="file"]');
      if (uploadInput) {
        uploadInput.click(); // 触发input的点击事件
      }
    },
    // 导入数据
    importData({ file }) {
      const fileName = file.name.toLowerCase();
      if (!fileName.endsWith(".ser")) {
        return this.$message.warning("只能导入.ser文件！");
      }
      const formData = new FormData();
      formData.append("file", file);
      pageApi.uploadFile(formData).then((res) => {
        const { status, message } = res.data;
        if (status === 200) {
          this.$message.success(message || "导入成功");
          this.getTableData(true);
        } else {
          this.$message.error(message || "导入失败");
        }
      });
    }
  }
};
</script>
<style lang="scss" scoped>
.report-setting {
}
</style>

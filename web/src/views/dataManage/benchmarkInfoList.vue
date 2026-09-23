<template>
  <!--基准信息表-->
  <div class="benchmarkInfoList" v-auto-enter>
    <!-- 搜索 -->
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form :inline="true" ref="formQuery" :model="formQuery" :rules="rules" label-width="auto" class="standard-form analyse-page">
          <el-row>
            <el-col :span="24">
              <el-form-item label="" prop="beCode">
                <el-input v-model.trim="formQuery.beCode" clearable placeholder="请输入基准编码" size="small"></el-input>
              </el-form-item>
              <el-form-item label="" prop="beName">
                <el-input v-model.trim="formQuery.beName" clearable placeholder="请输入基准名称" size="small"></el-input>
              </el-form-item>
              <el-form-item label="" prop="vcSource">
                <el-select v-model="formQuery.vcSource" filterable clearable placeholder="请选择数据来源" size="small">
                  <el-option v-for="item in vcSourceArrs" :key="item.dimCde" :label="item.dimNme" :disabled="item.dimCde === '*'" :value="item.dimCde"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item class="">
                <el-button type="primary" :disabled="btnDisabled" @click="onQuery(1)" icon="el-icon-search" size="small">查询</el-button>
                <el-button type="primary" size="small" @click="addData()" icon="el-icon-plus">新增</el-button>
                <el-button type="info" plain :icon="downLoadIcon" :disabled="issearchButton" :loading="exportLoading" @click="downloadTableExcel" size="small">
                  {{ downLoadText }}
                </el-button>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>
    </div>

    <el-row id="standard-table">
      <div id="standard-table-margin">
        <el-col>
          <vxe-table
            show-header-overflow
            auto-resize
            show-overflow
            stripe
            ref="table1"
            :height="tableHeight"
            @sort-change="handleSortChange"
            v-loading="tableLoading"
            :data="tableData"
            :cell-style="{ height: '50px' }"
            resizable
          >
            <vxe-table-column field="beCode" title="基准编码" min-width="100" sortable header-align="center" align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.beCode | noDataFilter }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column field="beName" title="基准名称" min-width="250" sortable header-align="center" align="left">
              <template slot-scope="scope">
                <span>{{ scope.row.beName | noDataFilter }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column field="beType" title="基准类型" min-width="100" sortable header-align="center" align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.beType | noDataFilter }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column field="vcTr" title="基准付息方式" min-width="100" sortable header-align="center" align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.vcTr | noDataFilter }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column field="vcFi" title="基准收益率算法" min-width="200" sortable header-align="center" align="left">
              <template slot-scope="scope">
                <span>{{ scope.row.vcFi | noDataFilter }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column field="vcStatus" title="基准状态" min-width="80" sortable header-align="center" align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.vcStatus | noDataFilter }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column field="beDate" title="基准时间" min-width="100" sortable header-align="center" align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.beDate | noDataFilter }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column field="vcSource" title="数据来源" min-width="100" sortable header-align="center" align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.vcSource | noDataFilter }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column field="" title="操作" min-width="200" header-align="center" align="center">
              <template slot-scope="scope">
                <span class="table-operation">
                  <el-button size="small" type="info" plain @click="editData(scope.row)">编辑</el-button>
                  <el-button size="small" type="info" plain @click="deleteData(scope.row)">删除</el-button>
                </span>
              </template>
            </vxe-table-column>
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
<!--          <Pagination :total="total" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination" />-->
        </el-col>
      </div>
    </el-row>

    <el-dialog title="基准信息维护" center customClass="customWidth" :visible.sync="dialogMask" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox">
          <div class="forms_management_box">
            <el-form :inline="true" class="standard-form" style="width: 100% !important" ref="formDialog" label-width="auto" :model="formDialog" :rules="dialogRules">
              <el-form-item label="" prop="beCode" :label-width="formLabelWidth" class="mb20">
                <span class="item-label" slot="label">基准编码</span>
                <el-input v-model.trim="formDialog.beCode" :disabled="operationType == '2'" clearable placeholder="" size="small"></el-input>
              </el-form-item>
              <el-form-item label="" prop="beName" :label-width="formLabelWidth" class="mb20">
                <span class="item-label" slot="label">基准名称</span>
                <el-input v-model.trim="formDialog.beName" clearable placeholder="" size="small"></el-input>
              </el-form-item>
              <el-form-item label="" prop="vcStatus" :label-width="formLabelWidth" class="mb20">
                <span class="item-label" slot="label">基准状态</span>
                <el-select v-model="formDialog.vcStatus" clearable placeholder="请选择" size="small">
                  <el-option label="启用" value="1"></el-option>
                  <el-option label="关闭" value="0"></el-option>
                </el-select>
              </el-form-item>

              <el-form-item label="" :label-width="formLabelWidth" prop="beType">
                <span class="item-label" slot="label">基准类型</span>
                <el-select v-model="formDialog.beType" filterable clearable placeholder="请选择" size="small">
                  <el-option v-for="item in benchmarkTypeArrs" :key="item.dimCde" :label="item.dimNme" :disabled="item.dimCde === '*'" :value="item.dimCde"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="" :label-width="formLabelWidth" prop="vcTr">
                <span class="item-label" slot="label">基准付息方式</span>
                <el-select v-model="formDialog.vcTr" filterable clearable placeholder="请选择" size="small">
                  <el-option v-for="item in benchmarkTrArrs" :key="item.dimCde" :label="item.dimNme" :disabled="item.dimCde === '*'" :value="item.dimCde"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="" :label-width="formLabelWidth" prop="vcFi">
                <span class="item-label" slot="label">收益率算法(计息天数)</span>
                <el-select v-model="formDialog.vcFi" filterable clearable placeholder="请选择" size="small">
                  <el-option v-for="item in benchmarkFiArrs" :key="item.dimCde" :label="item.dimNme" :disabled="item.dimCde === '*'" :value="item.dimCde"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="" :label-width="formLabelWidth" prop="beDate">
                <span class="item-label" slot="label">基准时间</span>
                <el-date-picker v-model="formDialog.beDate" value-format="yyyy-MM-dd" clearable size="small"></el-date-picker>
              </el-form-item>
              <el-form-item label="" prop="vcRemark" :label-width="formLabelWidth" class="mb20">
                <span class="item-label" slot="label">备注</span>
                <el-input v-model.trim="formDialog.vcRemark" clearable placeholder="" size="small"></el-input>
              </el-form-item>
            </el-form>
          </div>
          <el-row>
            <el-col>
              <benchmarkSetList v-if="operationType == '2'" ref="benchmarkSetList" :paramMap="paramMap"></benchmarkSetList>
            </el-col>
          </el-row>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer standard-form">
        <el-button size="small" type="info" plain @click="dialogMask = false">取 消</el-button>
        <el-button type="primary" size="small" :loading="dealLoading" @click="dealData">保 存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script type="text/ecmascript-6">
import { FILE_URL } from '@/utils/request'
import Pagination from "@/components/Pagination";
import commonApi from "@/api/common";
import { getToken } from '@/utils/auth'
import benchmarkInfoApi from "@/api/dataManage/benchmarkInfo";
import benchmarkSetList from "@/views/dataManage/benchmarkSetList";
export default {
  components: {
    Pagination,benchmarkSetList
  },
  name: "benchmarkInfoList",
  data() {
    return {
      // 查询参数
      formQuery: {
        // 基准编码
        beCode:'',
        // 基准名称
        beName:'',
        // 数据来源
        vcSource:'',


        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10,
        //排序方式
        orderBy : ""
      },
      // 验证规则
      rules: {
        // 数据来源
        // vcSource: [
        //   { type: 'array', required: true, message: '请选择数据来源', trigger: 'change' }
        // ]
      },
      // 弹窗验证规则
      dialogRules: {
        // 投资经理Id
        beCode: [
          { required: true, message: '请输入基准编码', trigger: 'change' }
        ],
      },
// 表格动态高度
      tableHeight: 0,
      //数据来源
      vcSourceArrs:[],
      //基准类型
      benchmarkTypeArrs:[],
      //基准付息方式
      benchmarkTrArrs:[],
      //收益率算法列表
      benchmarkFiArrs:[],

      //子组件参数集合
      paramMap:{
        beCode:"",
        beName:""
      },

      //确定按钮
      dealLoading:false,

      //产品列表数据
      tableData:[],
      //总条数
      total: 0,
      // 表格loading
      tableLoading: false,

      // 新增经理弹窗
      dialogMask: false,
      dialogMask2: false,
      // 表单宽度
      formLabelWidth: "200px",
      // 弹窗查询参数
      formDialog: {
        //基准编码
        beCode:"",
        //基准名称
        beName:"",
        //基准时间
        beDate:"",
        //基准类型
        beType:"",
        //基准付息方式
        vcTr:"",
        //收益率算法
        vcFi:"",
        //备注
        vcRemark:"",
        //状态是否有效1 未删除有效；0 已删除无效
        vcStatus:"",
        vcSource:"",
      },
      dialogLoading: false,

      // 操作类型 1、添加 2、编辑
      operationType: 1,

      exportLoading: false,
      // 导出图标
      downLoadIcon: "el-icon-download",
      // 导出提示文字
      downLoadText: "导出",
      // 查询按钮禁用
      btnDisabled: false,
      issearchButton: false,

    };
  },
  mounted() {
    let self = this
    // 默认查询
    this.$nextTick(() => {
      // 动态设置表格高度
      this.handleTableHeight()
      // 基准类型
      this.getListEdims("benchmark_type");
      // 收据来源
      this.getListEdims("SOURCETYPE");
      // 产品类型
      this.getListEdims("benchmark_tr");

      this.selectFiList();
      // 查询
      this.onQuery();
    });
  },
  methods: {
    /**
     * @description 动态设置表格高度
     */
    handleTableHeight() {
      this.$nextTick(() => {
        // 根据浏览器高度设置初始高度
        this.tableHeight = window.innerHeight - this.$refs.table1.$el.offsetTop - 235
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.table1.$el.offsetTop - 235
        }
      })
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
          this.selectManagerList();
        }
      });
    },


    // 清除
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    // 页面点击事件
    pagination(val) {
     /* let { page, limit  } = val;
      // 起始页
      this.formQuery.pageNum = page;
      // 每页数量
      this.formQuery.pageSize = limit; */
      const { currentPage, pageSize } = val;
      // 起始页
      this.formQuery.pageNum = currentPage;
      // 每页数量
      this.formQuery.pageSize = pageSize;
      // 查询
      this.onQuery();
    },
    // 资产接收的值
    productNodeClick(data){
      // 组合代码
      this.formDialog.fundCode = data.data.id
      // 组合名称
      this.formDialog.fundName = data.data.name
    },
// 字典查询
    getListEdims(type) {
      // 字典类型
      let params = type;
      commonApi.edimsDdiaCommon(params).then(res => {
        let { status, data } = res.data;

        if (status === 0) {
          // 产品类型
          if (type === "benchmark_type") {
            this.benchmarkTypeArrs = data;
          }
          if (type === "SOURCETYPE") {
            this.vcSourceArrs = data;
          }
          if (type === "benchmark_tr") {
            this.benchmarkTrArrs = data;
          }

        }
      });
    },

    // 查询信息
    selectManagerList(flag) {
      if (!flag) {
        this.tableLoading = true;
      } else {
        if (this.issearchButton) return;
        this.issearchButton = true;
        this.exportLoading = true;
        this.downLoadText = "导出";
      }
      let params = Object.assign({}, this.formQuery, {
      });
      if (flag) {
        params.pageNum = 1;
        params.pageSize = 99999999;
        params.ex_tmp_name = "基准信息-导出.xls";
      }
      // 清除空字段
      for (let k in params) {
        if (!params[k] && String(params[k]) !== "0") {
          delete params[k];
        }
      }
      benchmarkInfoApi.fun_selectListPage(params)
        .then(res => {
          this.tableLoading = false;
          this.issearchButton = false;
          this.exportLoading = false;
          this.downLoadText = "导出";
          let { status, data } = res;
          if (status === 0) {
            if (flag) {
              // 下载excel
              if (!data) return;
              this.$fun.commonDownloadUrl(data);
            } else {
              let { list, total } = data;
              this.tableData = list;
              this.total = total;
            }
          }
        })
        .catch(() => {
          this.tableLoading = false;
          this.issearchButton = false;
          this.exportLoading = false;
          this.downLoadText = "导出";
        });
    },
    // 新增信息
    insertInfo() {
      this.dealLoading = true
      let params = Object.assign({}, this.formDialog);
      benchmarkInfoApi.fun_insert(params)
        .then(res => {
          this.dialogMask = false;
          let { status,message } = res;
          if (status === 200) {
            this.$message({
              message: "新增成功",
              type: "success",
              customClass: "message-success"
            });
            // 查询
            this.onQuery();
          } else {
            this.$message({
              message: message,
              type: "error",
              customClass: "message-error"
            });
          }
          this.dealLoading = false
        })
        .catch(() => {
          this.$message({
            message: "系统异常",
            type: "error",
            customClass: "message-error"
          });
          this.dealLoading = false
          this.dialogMask = false;
        });
    },
    // 修改信息
    updateInfo() {
      this.dealLoading = true
      let params = Object.assign({}, this.formDialog);
      benchmarkInfoApi.fun_update(params)
        .then(res => {
          this.dialogMask = false;
          let { status,message } = res;
          if (status === 200) {
            this.$message({
              message: "修改成功",
              type: "success",
              customClass: "message-success"
            });
            // 查询
            this.onQuery();
          } else {
            this.$message({
              message: message,
              type: "error",
              customClass: "message-error"
            });
          }
          this.dealLoading = false
        })
        .catch(() => {
          this.$message({
            message: "系统异常",
            type: "error",
            customClass: "message-error"
          });
          this.dealLoading = false
          this.dialogMask = false;
        });
    },
    // 删除信息
    deleteInfo(beCode) {
      let params = Object.assign({}, {});
      params.beCode = beCode
      benchmarkInfoApi.fun_delete(params)
        .then(res => {
          let { status,message } = res;
          if (status === 200) {
            this.$message({
              message: "删除成功",
              type: "success",
              customClass: "message-success"
            });
            // 查询
            this.onQuery();
          } else {
            this.$message({
              message: message,
              type: "error",
              customClass: "message-error"
            });
          }
        })
        .catch(() => {
          this.$message({
              message: '系统异常',
              type: "error",
              customClass: "message-error"
            });
        });
    },
    // 处理数据
    dealData() {
      this.$refs["formDialog"].validate(valid => {
        if (valid) {
          if(this.operationType==1){
            // 新增信息
            this.insertInfo();
          }
          if(this.operationType==2){
            // 修改信息
            this.updateInfo();
          }
        }
      });
    },

    // 编辑数据
    addData() {
      this.operationType = 1;
      this.dialogMask = true;
      this.$nextTick(() => {
        // 清除
        this.resetForm("formDialog");
      })
    },
    // 编辑数据
    editData(row) {
      this.paramMap.beCode = row.beCode
      this.paramMap.beName = row.beName
      this.operationType = 2;
      this.dialogMask = true;
      this.$nextTick(() => {
        // 清除
        this.resetForm("formDialog");
        this.inputFormDialog(row.beCode);
        this.$refs.benchmarkSetList.onQuery()
      })
    },
    // 删除数据
    deleteData(row) {
      this.$confirm("确认删除该条数据?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          if (row.beCode) {
            // 删除经理信息
            this.deleteInfo(row.beCode);
          }
        })
        .catch(() => {});
    },


    inputFormDialog(beCode){
      let params = Object.assign({},{})
      params.beCode = beCode
      this.dialogLoading = true
      new Promise((resolve, reject) => {
        benchmarkInfoApi.fun_selectById(params).then(res => {
            var responseData = res.data;
            if(responseData!=null && responseData!=undefined && responseData!={}){
              this.formDialog.beCode=responseData.beCode
              this.formDialog.beName=responseData.beName
              this.formDialog.beDate=responseData.beDate
              this.formDialog.beType=responseData.beType
              this.formDialog.vcTr=responseData.vcTr
              this.formDialog.vcFi=responseData.vcFi
              this.formDialog.vcRemark=responseData.vcRemark
              this.formDialog.vcStatus=responseData.vcStatus
              this.formDialog.vcSource=responseData.vcSource
            }
          this.dialogLoading = false
        }).catch(error => {
          this.dialogLoading = false
          reject(error)
        })
      })

    },
    selectFiList(){
      let params = Object.assign({},{})
      new Promise((resolve, reject) => {
        benchmarkInfoApi.fun_selectFiList(params).then(res => {
            var responseData = res.data;
            if(responseData!=null && responseData!=undefined && responseData!={}){
              this.benchmarkFiArrs=responseData
            }
        }).catch(error => {
          reject(error)
        })
      })
    },
    // 当表格的排序条件发生变化的时候会触发该事件
    handleSortChange(val) {
      this.formQuery.orderBy = this.$fun.queryOrderBy_vxe(val);
      // 查询
      this.onQuery();
    },
    // 表格导出excel
    downloadTableExcel() {
      this.$refs["formQuery"].validate(valid => {
        if (valid) {
          // 查询基准信息（导出excel）
          this.selectManagerList(true);
        }
      });
    },
  },
  watch: {
  }
};
</script>

<style lang="scss" scoped>
.benchmarkInfoList {
  .funds-filter {
    width: 100%;
    // border-bottom: 1px solid #e1e0e0;
  }
}

.color-box {
  display: inline-block;
  height: 30px;
  width: 2px;
  background-color: #0f65dd;
}
.title-style {
  color: #0f65dd;
  vertical-align: middle;
  height: 35px;
  line-height: 35px;
  font-size: 16px;
  margin-left: 5px;
}
.benchmarkInfoList {
  .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
  .el-dialog {
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
  ::v-deep .el-dialog.customWidth {
    width: 75% !important;
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
::v-deep .vxe-table .vxe-body--row.row--stripe {
  background-color: #f9fafe !important;
}
::v-deep .el-dialog__wrapper .el-dialog__header span {
  color: #333 !important;
}
::v-deep .el-button--danger {
  color: #F56C6C;
  background-color: #fff;
  border-color: #F56C6C;
}
</style>

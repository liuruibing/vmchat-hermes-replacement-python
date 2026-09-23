<template>
  <!--基准成分配置表-->
  <div class="benchmarkSetList">
    <!-- 搜索 -->
    <el-form :inline="true" ref="formQuery" :model="formQuery" :rules="rules" style="width: 100% !important" class="formQuery standard-form">
      <el-row>
        <el-col :span="12">
          <div class="picc_forms_table_title">
            <div class="picc_forms_table_title_line"></div>
            <div class="title-style" style="color: #cf7e34 !important">基准指数配置</div>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="grid-content bg-purple-light" style="float: right">
            <el-form-item class="search_button_com">
              <el-button type="primary" size="small" @click="addData()" class="mb5">新增</el-button>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
    </el-form>

    <el-row id="standard-table">
      <el-col>
        <vxe-table
          show-header-overflow
          resizable
          auto-resize
          show-overflow
          stripe
          ref="table1"
          @sort-change="handleSortChange"
          :loading="tableLoading"
          :data="tableData"
          :cell-style="{ height: '50px' }"
        >
          <vxe-table-column field="indexCode" title="指数编码" min-width="100" sortable header-align="center" align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.indexCode | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="indexName" title="指数名称" min-width="100" sortable header-align="center" align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.indexName | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="exchange" title="市场代码" min-width="100" sortable header-align="center" align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.exchange | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="indexBaserate" title="指数基础比例" min-width="100" sortable header-align="center" align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.indexBaserate | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="indexType" title="指数类型" min-width="100" sortable header-align="center" align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.indexType | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="" title="付息方式" min-width="100" sortable header-align="center" align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.dd | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="" title="操作" width="200" header-align="center" align="center">
            <template slot-scope="scope">
              <span class="table-operation">
                <el-button type="info" plain size="small" @click="editData(scope.row)">编辑</el-button>
                <el-button type="info" plain size="small" @click="deleteData(scope.row)">删除</el-button>
              </span>
            </template>
          </vxe-table-column>
        </vxe-table>
      </el-col>
    </el-row>

    <el-dialog title="新增" center customClass="customWidth" :visible.sync="dialogMask" :modal="false" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox">
          <div class="forms_management_box">
            <el-form :inline="true" ref="formDialog" class="standard-form" :model="formDialog" :rules="dialogRules">
              <el-form-item label="" prop="beCode" :label-width="formLabelWidth" class="mb20">
                <span class="item-label" slot="label">基准编码</span>
                <el-input v-model.trim="formDialog.beCode" disabled placeholder="" size="small"></el-input>
              </el-form-item>
              <el-form-item label="" prop="beName" :label-width="formLabelWidth" class="mb20">
                <span class="item-label" slot="label">基准名称</span>
                <el-input v-model.trim="formDialog.beName" disabled placeholder="" size="small"></el-input>
              </el-form-item>
              <el-form-item label="" prop="indexCode" :label-width="formLabelWidth" class="mb20">
                <span class="item-label" slot="label">指数代码</span>
                <el-input v-model.trim="formDialog.indexCode" readonly v-on:click.native="openFundListDialog" placeholder="" size="small"></el-input>
              </el-form-item>
              <el-form-item label="" prop="indexName" :label-width="formLabelWidth" class="mb20">
                <span class="item-label" slot="label">指数名称</span>
                <el-input v-model.trim="formDialog.indexName" placeholder="" disabled size="small"></el-input>
              </el-form-item>
              <el-form-item label="" prop="exchange" :label-width="formLabelWidth" class="mb20">
                <span class="item-label" slot="label">市场代码</span>
                <el-input v-model.trim="formDialog.exchange" placeholder="" disabled size="small"></el-input>
              </el-form-item>
              <el-form-item label="" prop="indexBaserate" :label-width="formLabelWidth" class="mb20">
                <span class="item-label" slot="label">指数基础比例</span>
                <el-input v-model="formDialog.indexBaserate" type="number" clearable placeholder="" size="small" @blur="handleInputWeight()"></el-input>
                <!--@keyup.native="formDialog.indexBaserate =-->
                <!--formDialog.indexBaserate = formDialog.indexBaserate.replace(/[^\d.]/g,'');-->
                <!--formDialog.indexBaserate = formDialog.indexBaserate.replace(/\.{2,}/g,'.');-->
                <!--formDialog.indexBaserate = formDialog.indexBaserate.replace(/^\./g,'');-->
                <!--formDialog.indexBaserate = formDialog.indexBaserate.replace('.','$#$').replace(/\./g,'').replace('$#$','.');-->
                <!--formDialog.indexBaserate = formDialog.indexBaserate.replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3');"-->

                <!--oninput ="value=value.replace(/[^0-9.]/g,'')"-->
              </el-form-item>
              <el-form-item :label-width="formLabelWidth" prop="vcRemark">
                <span slot="label" class="content-lable-span">备注</span>
                <el-input type="textarea" maxlength="1000" :rows="3" style="width: 600px !important" show-word-limit v-model.trim="formDialog.vcRemark" size="small"></el-input>
              </el-form-item>
            </el-form>
          </div>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer standard-form">
        <el-button size="small" type="info" plain @click="dialogMask = false">取 消</el-button>
        <el-button type="primary" size="small" @click="dealData">保 存</el-button>
      </div>
    </el-dialog>
    <el-dialog title="指数信息" center customClass="customWidth" :modal="false" :visible.sync="dialogMask2" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox">
          <benchmarkIndexList @getTemplateRow="getTemplateRow"></benchmarkIndexList>
        </el-main>
      </el-container>
    </el-dialog>
  </div>
</template>

<script type="text/ecmascript-6">
import { FILE_URL } from '@/utils/request'
import Pagination from "@/components/NewPagination";
import commonApi from "@/api/common";
import { getToken } from '@/utils/auth'
import benchmarkSetApi from "@/api/dataManage/benchmarkSet";
import benchmarkIndexList from "@/views/dataManage/benchmarkIndexList";

export default {
  components: {
    Pagination,benchmarkIndexList
  },
  name: "benchmarkSetList",
  props:{
    paramMap:{
      beCode:"",
      beName:""
    }
  },
  data() {
    return {
      // 查询参数
      formQuery: {
        // 基准编码
        beCode:'',


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
        beName: [
          { required: true, message: '请输入基准名称', trigger: 'change' }
        ],
        indexCode: [
          { required: true, message: '请输入指数代码', trigger: 'change' }
        ],
        indexName: [
          { required: true, message: '请输入指数名称', trigger: 'change' }
        ],
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
      formLabelWidth: "150px",
      // 弹窗查询参数
      formDialog: {
        //基准编码
        beCode:"",
        //基准名称
        beName:"",
        //基准时间
        indexCode:"",
        //基准类型
        indexName:"",
        //基准类型
        indexType:"",
        //市场代码
        exchange:"",
        //收益率算法
        indexBaserate:0,
        //备注
        vcRemark:"",
      },
      editIndexBaserate:0,
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
    self.formQuery.beCode = this.paramMap.beCode
    self.formDialog.beCode = this.paramMap.beCode
    self.formDialog.beName = this.paramMap.beName

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
          this.selectManagerList();
        }
      });
    },
    handleInputWeight() {
     /* if (isNaN(this.formDialog.indexBaserate) || this.formDialog.indexBaserate < 0 || this.formDialog.indexBaserate > 100) {
        this.$message({
          message: '只能输入0到100之间的数字',
          type: 'warning'
        });
        this.formDialog.indexBaserate = 0;
      } else {
      }*/
    },

    //获取选中数据
    getTemplateRow(data){
      this.formDialog.indexCode = data.data.indexCode
      this.formDialog.indexName = data.data.indexName
      this.formDialog.exchange = data.data.indexExchange
      this.formDialog.indexType = data.data.indexType

      this.dialogMask2 = false
    },
    //点击弹窗
    openFundListDialog(){
      this.dialogMask2 = true
    },
    // 清除
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    // 页面点击事件
    pagination(val) {
      let { currentPage, pageSize  } = val;
      // 起始页
      this.formQuery.pageNum = currentPage;
      // 每页数量
      this.formQuery.pageSize = pageSize;
      // 查询
      this.onQuery();
    },

    // 查询信息
    selectManagerList(flag) {
      if (!flag) {
        this.tableLoading = true;
      } else {
        if (this.issearchButton) return;
        this.issearchButton = true;
        this.exportLoading = true;
        this.downLoadText = "导出数据中...";
      }
      let params = Object.assign({}, this.formQuery, {
      });
      if (flag) {
        params.pageNum = 1;
        params.pageSize = 99999999;
        params.ex_tmp_name = "样本信息-导出.xls";
      }
      // 清除空字段
      for (let k in params) {
        if (!params[k] && String(params[k]) !== "0") {
          delete params[k];
        }
      }
      benchmarkSetApi.fun_selectListPage(params)
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
              this.tableData = data;
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
      benchmarkSetApi.fun_insert(params)
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
      benchmarkSetApi.fun_update(params)
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
    deleteInfo(row) {
      let params = Object.assign({}, {});
      params.beCode = row.beCode
      params.indexCode = row.indexCode
      benchmarkSetApi.fun_delete(params)
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
      if (isNaN(this.formDialog.indexBaserate) || this.formDialog.indexBaserate <= 0 || this.formDialog.indexBaserate > 100) {
        this.$message({
          message: '只能输入0到100之间的数字',
          type: 'warning'
        });
        this.formDialog.indexBaserate = 0;
      } else {
        var numCount = 0.000000;
        let params = Object.assign({}, {});
        params.beCode = this.formDialog.beCode;
        benchmarkSetApi.fun_selectListPage(params)
          .then(res => {
            let resultData = res.data || [];
            for (let i = 0; i < resultData.length; i++) {
              console.log(resultData[i].indexBaserate);
              numCount += resultData[i].indexBaserate;
            }
            if (this.operationType == 2) {
              numCount -= Number(this.editIndexBaserate)
            }
            numCount += Number(this.formDialog.indexBaserate)
            if (numCount > 100) {
              this.$message.closeAll()
              this.$message({
                message: '指数基础比例之和不能大于100',
                type: 'warning'
              });
              this.formDialog.indexBaserate = 0
              return false;
            } else {
              this.$refs["formDialog"].validate(valid => {
                if (valid) {
                  this.formatNumber()
                  if (this.operationType == 1) {
                    // 新增信息
                    this.insertInfo();
                  }
                  if (this.operationType == 2) {
                    // 修改信息
                    this.updateInfo();
                  }
                }
              });
            }
          })
        this.dealLoading = false
      }

    },
    formatNumber(){
    },
    // 编辑数据
    addData() {
      this.operationType = 1;
      this.dialogMask = true;
      this.$nextTick(() => {
        // 清除
        this.resetForm("formDialog");
        this.formDialog.beCode = this.paramMap.beCode
        this.formDialog.beName = this.paramMap.beName
      })
    },
    // 编辑数据
    editData(row) {
      this.editIndexBaserate = row.indexBaserate
      this.operationType = 2;
      this.dialogMask = true;
      this.$nextTick(() => {
        // 清除
        this.resetForm("formDialog");
        this.inputFormDialog(row);
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
          if (row) {
            // 删除经理信息
            this.deleteInfo(row);
          }
        })
        .catch(() => {});
    },


    inputFormDialog(row){
      let params = Object.assign({},{})
      params.indexCode = row.indexCode
      params.beCode = row.beCode
      this.dialogLoading = true
      new Promise((resolve, reject) => {
        benchmarkSetApi.fun_selectById(params).then(res => {
            var responseData = res.data;
            if(responseData!=null && responseData!=undefined && responseData!={}){
              this.formDialog.beCode=responseData.beCode
              this.formDialog.beName=responseData.beName
              this.formDialog.indexCode=responseData.indexCode
              this.formDialog.indexName=responseData.indexName
              this.formDialog.exchange=responseData.exchange
              this.formDialog.vcRemark=responseData.vcRemark
              this.formDialog.indexBaserate=responseData.indexBaserate
            }
          this.dialogLoading = false
        }).catch(error => {
          this.dialogLoading = false
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
    'paramMap.beCode':function(newVal,oldVal){
        this.formDialog.beCode = newVal
        this.formQuery.beCode = newVal
    },
    'paramMap.beName':function(newVal,oldVal){
        this.formDialog.beName = newVal
    }
  }
};
</script>

<style lang="scss" scoped>
.title-style {
  color: #0f65dd;
  height: 35px;
  line-height: 35px;
  padding-left: 4px;
  font-size: 16px;
  //border-left: 4px solid #e03d3e;
  margin-bottom: 5px;
}
.benchmarkSetList {
  padding: 10px;
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
  .customWidth {
    width: 55% !important;
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
.vxe-table .vxe-body--row.row--stripe {
  background-color: #f9fafe !important;
}
</style>

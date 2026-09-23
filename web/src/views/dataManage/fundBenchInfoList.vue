<template>
  <!--数据维护-组合基准信息维护-->
  <div class="fundBenchInfoList">
    <!-- 搜索 -->
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form :inline="true" ref="formQuery" :model="formQuery" :rules="rules" class="standard-form">
          <el-row>
            <el-col :span="24">
              <el-form-item prop="startDays">
                <span slot="label" class="item-label">起始日期</span>
                <el-date-picker v-model="formQuery.startDays" value-format="yyyy-MM-dd" size="small"></el-date-picker>
              </el-form-item>
              <el-form-item>
                <span>-</span>
              </el-form-item>
              <el-form-item prop="startDaye">
                <el-date-picker v-model="formQuery.startDaye" value-format="yyyy-MM-dd" size="small"></el-date-picker>
              </el-form-item>
              <el-form-item label="" prop="fundCode">
                <span class="item-label" slot="label">产品代码</span>
                <el-input v-model.trim="formQuery.fundCode" clearable size="small"></el-input>
              </el-form-item>
              <el-form-item label="" prop="fundName">
                <span class="item-label" slot="label">产品名称</span>
                <el-input v-model.trim="formQuery.fundName" clearable size="small"></el-input>
              </el-form-item>
              <el-form-item prop="endDays">
                <span slot="label" class="item-label">结束日期</span>
                <el-date-picker v-model="formQuery.endDays" value-format="yyyy-MM-dd" size="small"></el-date-picker>
              </el-form-item>
              <el-form-item>
                <span>-</span>
              </el-form-item>
              <el-form-item prop="endDaye">
                <el-date-picker v-model="formQuery.endDaye" value-format="yyyy-MM-dd" size="small"></el-date-picker>
              </el-form-item>
              <el-form-item label="" prop="beCode">
                <span class="item-label" slot="label">基准代码</span>
                <el-input v-model.trim="formQuery.beCode" clearable size="small"></el-input>
              </el-form-item>
              <el-form-item label="" prop="beName">
                <span class="item-label" slot="label">基准名称</span>
                <el-input v-model.trim="formQuery.beName" clearable size="small"></el-input>
              </el-form-item>
              <el-form-item label="" prop="mark" class="mb20">
                <span class="item-label" slot="label">基准收益率计算方式</span>
                <el-select v-model="formQuery.mark" clearable size="small" placeholder="请选择">
                  <el-option label="先计算再加权(构成一段时间收益率 相加)" value="1"></el-option>
                  <el-option label="先加权再计算(构成每天收益率 连乘)" value="2"></el-option>
                  <el-option label="先加权再计算(构成每天收益率 累加)" value="3"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="" prop="source">
                <span class="item-label" slot="label">数据来源</span>
                <el-select v-model="formQuery.source" filterable clearable placeholder="请选择" size="small">
                  <el-option v-for="item in vcSourceArrs" :key="item.dimCde" :label="item.dimNme" :disabled="item.dimCde === '*'" :value="item.dimCde"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item class="">
                <el-button type="primary" size="small" :disabled="btnDisabled" @click="onQuery(1)" class="mb5" icon="el-icon-search">查询</el-button>
                <el-button type="primary" @click="addData()" class="mb5" size="small" icon="el-icon-plus">新增</el-button>
                <el-button @click="downloadTableExcel" type="info" plain size="small" :icon="downLoadIcon" :loading="exportLoading" :disabled="isDisabled" class="mb5">
                  {{ downLoadText }}
                </el-button>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>
    </div>

    <el-row>
      <el-col :span="24">
        <div style="float: right">
          <vxe-toolbar class="standard-vxe-toolbar" custom ref="tableToolbar" :custom="{ immediate: true }"></vxe-toolbar>
        </div>
      </el-col>
    </el-row>
    <el-row id="standard-table">
      <div id="standard-table-margin">
        <el-col>
          <vxe-table
            show-header-overflow
            auto-resize
            show-overflow
            stripe
            ref="table1"
            id="toolbar_table1"
            @sort-change="handleSortChange"
            v-loading="tableLoading"
            :data="tableData"
            :cell-style="{ height: '50px' }"
            resizable
          >
            <vxe-table-column field="fundCode" title="产品代码" min-width="100" sortable header-align="center" align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.fundCode | noDataFilter }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column field="fundName" title="产品名称" min-width="300" sortable header-align="center" align="left">
              <template slot-scope="scope">
                <span>{{ scope.row.fundName | noDataFilter }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column field="beCode" title="基准代码" min-width="100" sortable header-align="center" align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.beCode | noDataFilter }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column field="beName" title="基准名称" min-width="150" sortable header-align="center" align="left">
              <template slot-scope="scope">
                <span>{{ scope.row.beName | noDataFilter }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column field="startDay" title="起始日期" min-width="100" sortable header-align="center" align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.startDay | noDataFilter }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column field="endDay" title="结束日期" min-width="100" sortable header-align="center" align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.endDay | noDataFilter }}</span>
              </template>
            </vxe-table-column>

            <vxe-table-column field="markStr" title="基准收益率计算方式" min-width="100" sortable header-align="center" align="left">
              <template slot-scope="scope">
                <span>{{ scope.row.markStr | noDataFilter }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column field="sourceStr" title="数据来源" min-width="100" sortable header-align="center" align="left">
              <template slot-scope="scope">
                <span>{{ scope.row.sourceStr | noDataFilter }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column field="updateTime" title="更改日期" min-width="100" sortable header-align="center" align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.updateTime | noDataFilter }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column field="updateBy" title="更改人" min-width="100" sortable header-align="center" align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.updateBy | noDataFilter }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column field="" title="操作" min-width="250" header-align="center" align="center">
              <template slot-scope="scope">
                <span class="table-operation">
                  <el-button type="info" plain size="small" @click="editData(scope.row)">编辑</el-button>
                  <el-button type="info" plain size="small" @click="deleteData(scope.row)">删除</el-button>
                </span>

                <!--    <a style="color: #007A77" @click="editData(scope.row)">编辑</a>
              <a style="color: #007A77" @click="deleteData(scope.row)">删除</a>-->
              </template>
            </vxe-table-column>
          </vxe-table>
          <Pagination :total="total" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination" />
        </el-col>
      </div>
    </el-row>

    <el-dialog :title="operationName" center customClass="customWidth" :visible.sync="dialogMask" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox">
          <div class="forms_management_box">
            <el-form :inline="true" ref="formDialog" class="standard-form" :model="formDialog" :rules="dialogRules" style="width: 100% !important">
              <el-row>
                <el-form-item label="" prop="fundCode" :label-width="formLabelWidth" class="mb20">
                  <span class="item-label" slot="label">产品代码</span>
                  <el-input v-model.trim="formDialog.fundCode" :disabled="operationType == 2" v-on:click.native="openFundListDialog" placeholder="" size="small"></el-input>
                </el-form-item>
                <el-form-item label="" prop="fundName" :label-width="formLabelWidth" class="mb20">
                  <span class="item-label" slot="label">产品名称</span>
                  <el-input v-model.trim="formDialog.fundName" disabled placeholder="" size="small"></el-input>
                </el-form-item>
                <el-form-item label="" prop="beCode" :label-width="formLabelWidth" class="mb20">
                  <span class="item-label" slot="label">基准代码</span>
                  <el-input v-model.trim="formDialog.beCode" v-on:click.native="openBenchListDialog" placeholder="" size="small"></el-input>
                </el-form-item>
                <el-form-item label="" prop="beName" :label-width="formLabelWidth" class="mb20">
                  <span class="item-label" slot="label">基准名称</span>
                  <el-input v-model.trim="formDialog.beName" disabled placeholder="" size="small"></el-input>
                </el-form-item>
                <el-form-item label="" prop="startDay" :label-width="formLabelWidth" class="mb20">
                  <span class="item-label" slot="label">起始日期</span>
                  <el-date-picker v-model="formDialog.startDay" value-format="yyyy-MM-dd" clearable size="small"></el-date-picker>
                </el-form-item>
                <el-form-item label="" prop="endDay" :label-width="formLabelWidth" class="mb20">
                  <span class="item-label" slot="label">结束日期</span>
                  <el-date-picker v-model="formDialog.endDay" value-format="yyyy-MM-dd" clearable size="small"></el-date-picker>
                </el-form-item>

                <el-form-item label="" prop="mark" :label-width="formLabelWidth" class="mb20">
                  <span class="item-label" slot="label">基准收益率计算方式</span>
                  <el-select v-model="formDialog.mark" clearable size="small" placeholder="请选择">
                    <el-option label="先计算再加权(构成一段时间收益率 相加)" value="1"></el-option>
                    <el-option label="先加权再计算(构成每天收益率 连乘)" value="2"></el-option>
                    <el-option label="先加权再计算(构成每天收益率 累加)" value="3"></el-option>
                  </el-select>
                </el-form-item>

                <el-form-item label="" prop="source" :label-width="formLabelWidth" class="mb20">
                  <span class="item-label" slot="label">数据来源</span>
                  <el-select v-model="formDialog.source" filterable clearable placeholder="请选择" size="small">
                    <el-option v-for="item in vcSourceArrs" :key="item.dimCde" :label="item.dimNme" :disabled="item.dimCde === '*'" :value="item.dimCde"></el-option>
                  </el-select>
                </el-form-item>
              </el-row>
            </el-form>
          </div>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer standard-form">
        <el-button type="primary" size="small" :loading="dealLoading" @click="dealData">提 交</el-button>
        <el-button size="small" type="info" plain @click="dialogMask = false">取 消</el-button>
      </div>
    </el-dialog>
    <product-selector
      :dialog-visible="productSelectorVisible"
      :tree-data="treeData"
      :show-tree-key-array="showTreeKeyArray"
      :select-list="selectList"
      :default-checked-keys="defaultCheckedKeys"
      @closedialog="handleDialogClosed"
      @submitdialog="handleSubmitClick"
    ></product-selector>

    <!-- <el-dialog title="产品信息" center customClass="customWidth" :modal="false" :visible.sync="dialogMask2" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox">
          <FundListDialog  @getTemplateRow="getTemplateRow"></FundListDialog>
        </el-main>
      </el-container>
    </el-dialog>-->
    <el-dialog title="基准信息" center customClass="customWidth" :modal="false" :visible.sync="dialogMask3" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox">
          <BenchInfoListDialog @getTemplateRow="getTemplateRow2"></BenchInfoListDialog>
        </el-main>
      </el-container>
    </el-dialog>
  </div>
</template>

<script type="text/ecmascript-6">
import { FILE_URL } from '@/utils/request'
import Pagination from "@/components/Pagination";
import commonApi from "@/api/common";
import { getToken } from '@/utils/auth'
import fundBenchInfoListApi from "@/api/dataManage/fundBenchInfoList";
import FundListDialog from "@/components/FundListDialog";
import BenchInfoListDialog from "@/components/BenchInfoListDialog";
import productSelector from '@/components/productSelector'

export default {
  components: {
    Pagination,FundListDialog,BenchInfoListDialog,productSelector
  },
  name: "fundBenchInfoList",
  data() {
    return {
      // 查询参数
      formQuery: {
        // 基准代码
        beCode:'',
        // 组合代码
        fundCode:'',
        //
        startDays:'',
        startDaye:'',
        endDays:'',
        endDaye :'',
        source:'',
        mark:'',


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
      treeData: [
        {
          label: '广发托管/外包',
          id: 'zstgwb'
        },
        {
          label: '私有产品',
          code: 'sycp'
        }
      ],
      showTreeKeyArray: ['广发托管/外包', '私有产品'],
      selectList: [],
      defaultCheckedKeys: 'zstgwb',
      // 选择产品弹窗
      productSelectorVisible: false,
      // 指数弹窗验证规则
      dialogRules: {
        fundCode: [
          { required: true,  trigger: "change",message: '请选择产品',  }
        ],
        beCode: [
          { required: true,  trigger: "change",message: '请选择基准',  }
        ],
      },
      //数据来源
      vcSourceArrs:[],
      benchmarkTrArrs:[],
      //确定按钮
      dealLoading:false,

      //组合列表数据
      tableData:[],
      //总条数
      total: 0,
      // 表格loading
      tableLoading: false,
      /* 按钮禁止与否 */
      isDisabled: false,
      // 导出图标
      downLoadIcon: "el-icon-download",
      // 导出提示文字
      downLoadText: "导出",
      // 新增经理弹窗
      dialogMask: false,
     // dialogMask2: false,
      dialogMask3: false,
      // 修改经理弹窗
      dialogMask_doc: false,
      // 表单宽度
      formLabelWidth: "170px",
      // 弹窗
      formDialog: {
        fId:"",
        fundName:"",
        fundCode:"",
        beId:"",
        beCode:"",
        beName:"",
        startDay:"",
        endDay:"2099-12-31",
        mark:"",
        source:"",
      },
      dialogLoading: false,

      fundTypeList:[],

      managerList:[],

      // 操作类型 1、添加 2、编辑
      operationType: 1,
      operationName: "",

      exportLoading: false,

      // 查询按钮禁用
      btnDisabled: false,
    };
  },
  mounted() {
    // 数据来源
    this.getListEdims("SOURCETYPE");
    // 组合类型
    this.getListEdims("benchmark_tr");
    this.$refs.table1.connect(this.$refs.tableToolbar)
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
          // 查询组合信息
          this.selectManagerList();
        }
      });
    },
    handleSubmitClick(arr) {
      this.productSelectorVisible = false
      this.formDialog.fundCode = arr[0].VC_FUNDCODE || ''
      this.formDialog.fundName = arr[0].VC_FUNDNAME || ''
      this.selectList = arr
    },
    // 字典查询
    getListEdims(type) {
      // 字典类型
      let params = type;
      commonApi.edimsDdiaCommon(params).then(res => {
        let { status, data } = res.data;

        if (status === 0) {
          if (type === "SOURCETYPE") {
            this.vcSourceArrs = data;
          }
          if (type === "benchmark_tr") {
            this.benchmarkTrArrs = data;
          }

        }
      });
    },
  /*  //获取选中数据
    getTemplateRow(data){
      this.formDialog.fundCode = data.data.fundCode
      this.formDialog.fundName = data.data.fundName
      this.dialogMask2 = false
    },*/
    getTemplateRow2(data){
      this.formDialog.beCode = data.data.beCode
      this.formDialog.beName = data.data.beName
      this.formDialog.beId = data.data.beId
      this.dialogMask3 = false
    },
    //点击弹窗
    openFundListDialog(){
      if(this.operationType == 1){
        this.productSelectorVisible = true
      }
    },
    handleDialogClosed() {
      this.productSelectorVisible = false
    },
    openBenchListDialog(){
      this.dialogMask3 = true
    },

    // 清除
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    // 页面点击事件
    pagination(val) {
      let { page, limit  } = val;
      // 起始页
      this.formQuery.pageNum = page;
      // 每页数量
      this.formQuery.pageSize = limit;
      // 查询
      this.onQuery();
    },


    // 查询信息
    selectManagerList(flag) {
      if (!flag) {
        this.tableLoading = true;
      } else {
        if (this.isDisabled) return;
        this.isDisabled = true;
        this.exportLoading = true;
        this.downLoadText = "导出";
      }
      let params = Object.assign({}, this.formQuery, {
      });
      if (flag) {
        params.pageNum = 1;
        params.pageSize = 99999999;
        params.ex_tmp_name = "组合基准信息维护-导出.xls";
      }
      // 清除空字段
      for (let k in params) {
        if (!params[k] && String(params[k]) !== "0") {
          delete params[k];
        }
      }
      fundBenchInfoListApi.fun_selectListPage(params)
        .then(res => {
          this.tableLoading = false;
          this.isDisabled = false;
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
          this.isDisabled = false;
          this.exportLoading = false;
          this.downLoadText = "导出";
        });
    },
    // 修改组合基本信息
    updateInfo() {
      this.dealLoading = true
      let params = Object.assign({}, this.formDialog);
      fundBenchInfoListApi.fun_update(params)
        .then(res => {
          this.dialogMask = false;
          let { status } = res;
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
              message: '修改失败',
              type: "error",
              customClass: "message-error"
            });

          }
          this.dealLoading = false
        })
        .catch(() => {
               this.$message({
              message: '系统异常',
              type: "error",
              customClass: "message-error"
            });
          this.dealLoading = false
          this.dialogMask = false;
        });
    },
    // 新增组合基本信息
    addInfo() {
      this.dealLoading = true
      let params = Object.assign({}, this.formDialog);
      fundBenchInfoListApi.fun_insert(params)
        .then(res => {
          this.dialogMask = false;
          let { status } = res;
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
              message: '新增失败',
              type: "error",
              customClass: "message-error"
            });
          }
          this.dealLoading = false
        })
        .catch(() => {
                    this.$message({
              message: '新增异常',
              type: "error",
              customClass: "message-error"
            });
          this.dealLoading = false
          this.dialogMask = false;
        });
    },
    // 处理数据
    dealData() {
      this.$refs["formDialog"].validate(valid => {
        if (valid) {
          if(this.operationType == 1){
            // 修改 信息
            this.addInfo();
          }else if(this.operationType == 2){
            // 修改 信息
            this.updateInfo();
          }else{

          }

        }
      });
    },

    // 编辑数据
    editData(row) {
      this.operationType = 2,
        this.operationName = '编辑'
      this.dialogMask = true;
      this.$nextTick(() => {
        // 清除
        this.resetForm("formDialog");
        this.inputFormDialog(row.fId);
      })
    },

    // 编辑数据
    addData() {
      this.operationType = 1,
        this.operationName = '新增'
      this.dialogMask = true;
      this.$nextTick(() => {
        // 清除
        this.resetForm("formDialog");
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
            if (row.fId) {
              this.deleteInfo(row.fId);
            }
          })
          .catch(() => {});
    },
    // 删除信息
    deleteInfo(fId) {
      let params = Object.assign({}, {});
      params.fId = fId
      fundBenchInfoListApi.fun_delete(params)
        .then(res => {
          let { status,message } = res;
          if (status === 200) {
            this.$message({
              message: "删除成功",
              type: "success",
              customClass: "message-error"
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

    inputFormDialog(fId){
      let params = Object.assign({},{})
      params.fId = fId
      this.dialogLoading = true
      new Promise((resolve, reject) => {
        fundBenchInfoListApi.fun_selectById(params).then(res => {
            var responseData = res.data;
            if(responseData!=null && responseData!=undefined && responseData!={}){
              this.formDialog.fId=responseData.fId
              this.formDialog.fundName=responseData.fundName
              this.formDialog.fundCode=responseData.fundCode
              this.formDialog.beCode=responseData.beCode
              this.formDialog.beName=responseData.beName
              this.formDialog.startDay=responseData.startDay
              this.formDialog.endDay=responseData.endDay
              this.formDialog.mark=responseData.mark
              this.formDialog.source=responseData.source
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
  }
};
</script>

<style lang="scss" scoped>
.fundBenchInfoList {
  .funds-filter {
    width: 100%;
    // border-bottom: 1px solid #e1e0e0;
  }
  .item-label {
    font-size: 14px;
  }
  .el-table--medium {
    border-top: 2px solid #e13c3d !important;
  }
  ::v-deep .customWidth.el-dialog {
    //padding: 10px;
    width: 75% !important;
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
::v-deep .vxe-table .vxe-body--row.row--stripe {
  background-color: #f9fafe !important;
}
::v-deep .el-dialog__wrapper .el-dialog__header span {
  color: #333 !important;
}
</style>

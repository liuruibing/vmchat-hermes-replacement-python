<template>
  <!--
  组合树调度监控记录 -->
  <div class="combTreeRecord">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formQuery" :inline="true" :rules="searchRules" :model="formQuery" class="demo-form-inline form_inline_search" style="margin-top: 10px">
          <el-row>
            <el-col :span="18">
              <div class="grid-content bg-purple">
                <el-form-item label="" prop="vcTableUpdate" class="mb20">
                  <span slot="label" class="item-label">触发表生成日期</span>
                  <el-date-picker v-model="formQuery.vcTableUpdate" style="width: 174px" type="date" size="small" value-format="yyyy-MM-dd" placeholder="选择日期" />
                </el-form-item>
                <el-form-item prop="vcCode">
                  <span slot="label" class="item-label">编码</span>
                  <el-input v-model.trim="formQuery.vcCode" clearable placeholder="请输入" size="small" />
                </el-form-item>
                <el-form-item prop="vcName">
                  <span slot="label" class="item-label">名称</span>
                  <el-input v-model.trim="formQuery.vcName" clearable placeholder="请输入" size="small" />
                </el-form-item>
                <el-form-item label="" prop="vcResult">
                  <span slot="label" class="item-label">执行结果</span>
                  <el-select v-model="formQuery.vcResult" clearable size="small" placeholder="请选择">
                    <template v-for="(item, index) in vcResultList">
                      <el-option :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                    </template>
                  </el-select>
                </el-form-item>
                <el-form-item label="" prop="vcRunStatus">
                  <span slot="label" class="item-label">运行状态</span>
                  <el-select v-model="formQuery.vcRunStatus" clearable size="small" placeholder="请选择">
                    <template v-for="(item, index) in vcRunStatusList">
                      <el-option :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                    </template>
                  </el-select>
                </el-form-item>
                <el-form-item label="" prop="dExecBeginDate" class="mb20">
                  <span slot="label" class="item-label">开始执行时间</span>
                  <el-date-picker v-model="formQuery.dExecBeginDate" style="width: 174px" type="date" size="small" value-format="yyyy-MM-dd" placeholder="选择日期" />
                </el-form-item>
                <el-form-item label="" prop="dExecEndDate" class="mb20">
                  <span slot="label" class="item-label">结束执行时间</span>
                  <el-date-picker v-model="formQuery.dExecEndDate" style="width: 174px" type="date" size="small" value-format="yyyy-MM-dd" placeholder="选择日期" />
                </el-form-item>
                <el-form-item label="" prop="vcSource">
                  <span slot="label" class="item-label">数据来源</span>
                  <el-select v-model="formQuery.vcSource" clearable size="small" placeholder="请选择">
                    <template v-for="(item, index) in fundTypes">
                      <el-option :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                    </template>
                  </el-select>
                </el-form-item>
              </div>
            </el-col>
            <el-col :span="6">
              <!--          :disabled="issearchButton"-->
              <div class="grid-content bg-purple-light">
                <el-form-item class="search_button_com standatd-form">
                  <el-button type="primary" style="margin-bottom: 5px" icon="el-icon-search" @click="onSubmit('formQuery')">查询</el-button>
                  <el-button type="primary" @click="deleteData()">删除</el-button>
                  <el-button type="primary" style="margin-bottom: 5px" icon="el-icon-truck" @click="formReExecuteData()">重跑数据</el-button>
                  <!-- <el-button
                type="info"
                :icon="exportLoading ? 'el-icon-loading' : 'el-icon-download'"
                :disabled="isDisabled"
                @click="downloadTableExcel"
                >{{ downLoadText }}
              </el-button>-->
                </el-form-item>
              </div>
            </el-col>
          </el-row>
        </el-form>
      </div>
    </div>
    <div id="standard-table" class="table-content">
      <div id="standard-table-margin">
        <el-row>
          <el-col>
            <vxe-table
              id="toolbar_table1"
              ref="refsTable"
              :height="tableHeight"
              :sort-config="{ remote: true }"
              :loading="tableLoading"
              :custom-config="{ storage: true }"
              :data="tableData"
              :cell-style="{ height: '50px' }"
              show-header-overflow
              auto-resize
              show-overflow
              stripe
              :tree-config="{ children: 'children', iconOpen: 'fa fa-minus-square-o', iconClose: 'fa fa-plus-square-o' }"
              @sort-change="handleSortChange"
              @checkbox-change="selectChangeEvent"
              :checkbox-config="{ labelField: 'name', checkStrictly: true }"
            >
              <vxe-table-column type="checkbox" width="60"></vxe-table-column>
              <vxe-table-column field="vcCode" title="编码" min-width="120" header-align="center" sortable align="center" tree-node />
              <vxe-table-column field="vcName" title="名称" min-width="250" header-align="center" sortable align="center" />
              <vxe-table-column field="vcCodeTypeName" title="编码类型" sortable min-width="100" header-align="center" sortable align="center" />
              <vxe-table-column field="vcTableDate" title="触发表生成日期" min-width="130" header-align="center" sortable align="center" />
              <vxe-table-column field="dBusiBeginDate" title="业务开始日期" min-width="100" header-align="center" sortable align="center" />
              <vxe-table-column field="dBusiEndDate" title="业务结束日期" min-width="120" sortable header-align="center" align="center" />
              <vxe-table-column field="dExecBeginDate" title="开始执行时间" min-width="150" header-align="center" sortable align="center" />
              <vxe-table-column field="dExecEndDate" title="结束执行时间" min-width="150" header-align="center" sortable align="center" />
              <vxe-table-column field="vcRunStatusName" title="运行状态" min-width="120" header-align="center" sortable align="center" />
              <vxe-table-column field="vcResult" title="结果" min-width="120" header-align="center" sortable align="center" />
              <vxe-table-column label="明细" width="140" align="center" header-align="center">
                <template slot-scope="scope">
                  <div class="dialog-footer standard-form">
                    <el-button v-if="scope.row.vcCodeType == 'PROC'" type="info" plain size="small" @click="etlfundtriggerlog_list_detail(scope.row)">明细</el-button>
                  </div>
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
          </el-col>
        </el-row>
      </div>
    </div>
    <el-dialog v-if="dialogMask" :visible.sync="dialogMask" :close-on-click-modal="false" title="明细日志" custom-class="customWidth">
      <el-container class="hg100">
        <el-main class="mainBox">
          <el-form ref="formQueryTK" :inline="true" :model="formQueryTK" class="demo-form-inline form_inline_search" style="margin-top: 10px">
            <el-row>
              <el-col :span="18">
                <div class="grid-content bg-purple">
                  <el-form-item label="" prop="vcStatus">
                    <span slot="label" class="item-label">执行结果</span>
                    <el-select v-model="formQueryTK.vcStatus" clearable size="small" placeholder="请选择">
                      <template v-for="(item, index) in vcResultListTK">
                        <el-option :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                      </template>
                    </el-select>
                  </el-form-item>
                </div>
              </el-col>
              <el-col :span="6">
                <!--          :disabled="issearchButton"-->
                <div class="grid-content bg-purple-light">
                  <el-form-item class="search_button_com standard-form">
                    <el-button type="primary" style="margin-bottom: 5px" icon="el-icon-search" @click="onSubmitTK('formQueryTK')">查询</el-button>
                  </el-form-item>
                </div>
              </el-col>
            </el-row>
          </el-form>
          <el-row>
            <el-col :span="24" style="padding-top: 10px">
              <div style="vertical-align: middle; display: inline-block">
                <div class="color-box"></div>
              </div>
              <span class="title-style">日志明细列表</span>
            </el-col>
            <!-- <el-col :span="8">
              <div style="float: right">
                <vxe-toolbar
                  ref="tableToolbars"
                  :custom="{ immediate: true }"
                  custom
                />
              </div>
            </el-col>-->
          </el-row>

          <el-row>
            <el-col>
              <vxe-table
                id="toolbar_table2"
                ref="table2"
                :sort-config="{ remote: true }"
                :loading="tableLoadingTK"
                :custom-config="{ storage: true }"
                :data="tableDataTK"
                :header-cell-style="{ color: '#000', height: '60px' }"
                :cell-style="{ height: '40px' }"
                show-header-overflow
                auto-resize
                show-overflow
                stripe
                @sort-change="handleSortChange"
                @checkbox-change="selectChangeEvent"
              >
                <vxe-table-column field="vcCode" title="任务编码" min-width="120" header-align="center" align="center" />
                <vxe-table-column field="vcName" title="任务名称" min-width="200" header-align="center" align="center" />
                <vxe-table-column field="dBusiBeginDate" title="业务开始日期" min-width="130" header-align="center" align="center" />
                <vxe-table-column field="dBusiEndDate" title="业务结束日期" min-width="130" header-align="center" align="center" />
                <vxe-table-column field="dExecBeginDate" title="开始执行时间" min-width="100" header-align="center" align="center" />
                <vxe-table-column field="dExecEndDate" title="结束执行时间" min-width="120" header-align="center" align="center" />
                <vxe-table-column field="vcResult" title="日志详情" min-width="150" header-align="center" align="center" />
              </vxe-table>
              <vxe-pager
                :current-page="formQueryTK.pageNum"
                :page-size="formQueryTK.pageSize"
                :total="totalTK"
                :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
                border
                size="medium"
              class="standard-vxe-pager"
                @page-change="pagination"
              />
            </el-col>
          </el-row>
        </el-main>
      </el-container>
    </el-dialog>
  </div>
</template>
<script type="text/ecmascript-6">

import Pagination from "@/components/Pagination";
import commonApi from "@/api/common";
import commonFun from '@/filters/common.js'
import combTreeRecordApi from "@/api/etl/combTreeRecord";
import moment from 'moment'

export default {
  name: "combTreeRecord",
  components: {
    Pagination,
  },
  data() {

    return {
      tableHeight: 0,
      // 搜索
      formQuery: {
        //触发表生成时间
        vcTableUpdate:"",
        //编码
        vcCode:"",
        //名称
        vcName:"",
        //执行结果
        vcResult:"",
        //运行状态
        vcRunStatus:"",
        //开始执行时间
        dExecBeginDate:"",
        //结束执行时间
        dExecEndDate:"",
        //数据来源
        vcSource:"",



        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10,
        // 排序方式
        sort: "dExecBeginDate",
        order: "desc"
      },
      // 表格数据
      tableData: [],
      formLabelWidth: "120px",
      // 执行结果
      vcResultList: [
        {dimCde:"",dimNme:"全部"},
        {dimCde:"成功",dimNme:"成功"},
        {dimCde:"失败",dimNme:"失败"}
        ],
      // 运行状态
      vcRunStatusList: [
        {dimCde:"",dimNme:"全部"},
        {dimCde:"COMPLETED",dimNme:"已完成"},
        {dimCde:"UNDO",dimNme:"未执行"},
        {dimCde:"DISABLE",dimNme:"取消"},
        {dimCde:"RUNNING",dimNme:"正在运行"}
      ],
      fundTypes:[],
      issearchButton: false,

      tableLoading: false,
      total: 0,

      dialogMask: false,

      searchRules: {
        ddate_: [{ required: true, message: "请选择日期", trigger: "change" }],
        // beginDate: [
        //   { required: true, message: '请选择开始日期', trigger: 'change' },
        //   { validator: validatebeginDate, trigger: 'change' }
        // ],
        // endDate: [
        //   { required: true, message: '请选择结束日期', trigger: 'change' },
        //   { validator: validateEndDate, trigger: 'change' }
        // ],
        fundNames: [{ required: true, message: "请选择产品", trigger: "change" }]
      },
      //成立日
      timDate:"",
      //复选框选中的数据
      selectDataID:[],
      selectDataCode:[],
      /* 按钮禁止与否 */
      isDisabled: false,
      // 导出图标
      downLoadIcon: "el-icon-download",
      // 导出提示文字
      downLoadText: "导出",
      exportLoading: false,

      baseApi: "", // 页面根地址
      exportButton: false,
      exportText: "导出",
      exportIcon: "el-icon-download",
      tags: [],
      //弹框数据
      vcResultListTK: [
        {dimCde:"",dimNme:"全部"},
        {dimCde:"0",dimNme:"成功"},
        {dimCde:"1",dimNme:"失败"}
      ],
      formQueryTK:{
        fId:"",
        vcStatus:"",
        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10,
      },
      tableLoadingTK: false,
      totalTK: 0,
      // 弹框表格数据
      tableDataTK: [],
    };
  },
  watch: {},
  mounted() {
    // this.$refs.table1.connect(this.$refs.tableToolbar);
    this.handleTableHeight()
    this.dDate();
    // 获取数据来源
    this.getListEdims("SOURCETYPE");
    // 默认显示个框架
    this.onSubmit("formQuery");

  },

  methods: {
        /**
     * @description 动态设置表格高度
     */
     handleTableHeight() {
      this.$nextTick(() => {
        // 根据浏览器高度设置初始高度
        this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 320
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 320
        }
      })
    },
    dDate (){
      let today = commonFun.get_newDate();
      this.formQuery.dExecBeginDate = today;

      let today1 = new Date();
      let yesterday1 = new Date(today1.setDate(today1.getDate() - 1));
      let year = yesterday1.getFullYear();
      let month = yesterday1.getMonth() + 1; // getMonth()方法返回的月份是从0开始的，所以需要加1
      let date = yesterday1.getDate();

      let formattedDate = year + '-' + (month < 10 ? '0' + month : month) + '-' + (date < 10 ? '0' + date : date);
      this.formQuery.vcTableUpdate = formattedDate;
    },
    inputMouserIn(){

    },
    handleFundNamesChange(val) {
      if (!val) {
        this.tags = [];
        this.formQuery.fundCodes = [];
        this.formQuery.fundNames = "";
      }
    },
    //删除数据
    deleteData() {
      if(this.selectDataID.length>0){
        this.$confirm('是否删除所选数据, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
        }).then(() => {

          const params = {
            batchIdArr:JSON.stringify(this.selectDataID)
          }
          new Promise((resolve, reject) => {
            combTreeRecordApi
              .fun_deleteEtlFundTriggerLog(params)
              .then((res) => {
                // 查询
                this.onQuery();
                if(res.resultCode == 1){
                  this.$message({
                    type: 'success',
                    message: '删除成功!'
                  });
                }else {
                  this.$message({
                    type: 'info',
                    message: '删除失败'
                  });
                }

              })
              .catch((error) => {
                reject(error);
              });
          });

        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });
        });
      }else {
        this.$alert('请选择需要删除的数据！', '提示', {
          confirmButtonText: '确定',
          callback: action => {
          }
        });
      }

    },
    //重跑数据
    formReExecuteData(){
      if(this.formQuery.vcTableUpdate != '' && this.formQuery.vcTableUpdate != null){
        this.$confirm('确定要重跑数据吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
        }).then(() => {

          const params = {
            fundCodeArr:JSON.stringify(this.selectDataCode),
            vcTableUpdate:JSON.stringify(this.formQuery.vcTableUpdate),
            vcSource:JSON.stringify(this.formQuery.vcSource),
          }
          new Promise((resolve, reject) => {
            combTreeRecordApi
              .fun_dimFundTriggerLogList(params)
              .then((res) => {
                // 查询
                this.onQuery();
                if(res.resultCode == 1){
                  this.$message({
                    type: 'success',
                    message: '执行成功!'
                  });
                }else {
                  this.$message({
                    type: 'info',
                    message: '执行失败'
                  });
                }

              })
              .catch((error) => {
                reject(error);
              });
          });

        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消执行'
          });
        });
      }else {
        this.$alert('触发表生成日期不能为空！', '提示', {
          confirmButtonText: '确定',
          callback: action => {
          }
        });
      }
    },
    etlfundtriggerlog_list_detail(row){
      this.dialogMask = true
      this.formQueryTK.fId = row.fId
      this.onQueryTK()
    },
    onQueryTK() {
      var self = this;
      const params = {
        limit: this.formQueryTK.pageSize,
        offset: (this.formQueryTK.pageNum - 1) * this.formQueryTK.pageSize,
        ...this.formQueryTK
      }
      delete params.pageNum
      delete params.pageSize

      this.tableLoadingTK = true;

      new Promise((resolve, reject) => {
        combTreeRecordApi
          .fun_detailLogList(params)
          .then((res) => {
            const { rows } = res;
            this.tableDataTK = rows
            this.totalTK = res.total
            this.tableLoadingTK = false;
          })
          .catch((error) => {
            this.tableLoadingTK = false;
            reject(error);
          });
      });
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
    onSubmitTK(formName) {
      var self = this;
      self.formQueryTK.pageNum = 1;
      self.$refs[formName].validate((valid) => {
        if (valid) {
          self.onQueryTK();
          // 禁用搜索按钮
          self.$fun.searchButtonDisabled("issearchButton", self);
        } else {
          return false;
        }
      });
    },

    onQuery(flag) {
      var self = this;
      const params = {
        limit: this.formQuery.pageSize,
        offset: (this.formQuery.pageNum - 1) * this.formQuery.pageSize,
        ...this.formQuery
      }
      delete params.pageNum
      delete params.pageSize

      if (!flag) {
        this.tableLoading = true;
      }
      new Promise((resolve, reject) => {
        combTreeRecordApi
          .fun_selectCombTreeRecord(params)
          .then((res) => {
            const { rows } = res;
            const data = rows;
            const map = {}
            const val = []
            for (var i = 0; i < data.length; i++) {
              map[data[i].fId] = data[i]
            }
            for (var i = 0; i < data.length; i++) {
              const parent = map[data[i].fParentId]
              if (parent) {
                ;(parent.children || (parent.children = [])).push(data[i])
              } else {
                val.push(data[i])
              }
            }
            this.tableData = val
            this.total = res.total
            this.tableLoading = false;
            self.exportLoading = false;
            self.downLoadText = "导出";
          })
          .catch((error) => {
            this.tableLoading = false;
            self.exportLoading = false;
            self.downLoadText = "导出";
            reject(error);
          });
      });
    },

    getListEdims(type) {
      // 字典类型
      const params = type;
      commonApi.edimsDdiaCommon(params).then((res) => {
        const { status, data } = res.data;

        if (status === 0) {
          // 产品类型
          if (type === "SOURCETYPE") {
            this.fundTypes = data;
          }
        }
      });
    },
    // 导出
    downloadTableExcel() {
      this.onQuery(true);
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
    //勾选事件
    selectChangeEvent ({ records }) {
      this.selectDataID=[];
      this.selectDataCode=[];
      for (var i = 0; i < records.length; i++) {
        // 检查records[i]是否包含fBatchId和vcFundCode属性
        if ('fBatchId' in records[i] && 'vcFundCode' in records[i]) {
          this.selectDataID[i] = records[i].fBatchId;
          this.selectDataCode[i] = records[i].vcFundCode;
        } else {
          // 处理或报告错误，例如记录到控制台或抛出异常
          console.error('records[i]缺少必要的属性');
        }
      }
      console.log(this.selectDataID)
      console.log(this.selectDataCode)
    },
    // 当表格的排序条件发生变化的时候会触发该事件
    handleSortChange(val) {
      this.formQuery.order = val.order
      this.formQuery.sort = val.property
      // 查询
      this.onQuery();
    }
  }
};
</script>

<style lang="scss">
.combTreeRecord {
  // padding: 10px;

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
  .vxe-table .vxe-body--row.row--stripe {
    background-color: #f2f2f2 !important;
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
  .vxe-pager.size--medium {
    font-size: 12px;
  }

  .el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell {
    background: #f8f8f8;
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

    .el-form-item {
      min-width: 50%;
      margin-right: 0;
    }
    ::v-deep .vxe-table .vxe-body--row.row--stripe {
      background-color: #f7f7f7 !important;
    }
    .mr5 {
      margin-right: 5px;
    }
  }
}
</style>

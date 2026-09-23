<template>
   <div>
   <!--
  <el-form :inline='true'  ref='formInline' :model='formInline' style='margin-bottom: 8px;' class='demo-form-inline form_inline_search' >
    <el-row>
      <el-col :span='16'>
         <div style='width:100%;height:50px;'>
             <el-form-item label='报表名称' prop='reportName'>
                  <el-input type='text' v-model.trim='formInline.reportName' clearable placeholder='请输入名称' size='small'></el-input>
              </el-form-item>
         </div>
      </el-col>
      <el-col :span='8'>
         <el-form-item class='search_button_com'>
            <el-button type='primary' @click='onSubmit(true)' style='margin-bottom: 5px;' size='small'><i class='el-icon-search'></i>查询</el-button>
            <el-button type='primary' plain @click="restForm('formInline')" style='margin-bottom: 5px; ' size='small'><i class='el-icon-delete'></i>重置</el-button>
            <el-button type="primary"  plain  @click="addData()" style="margin-bottom: 5px; " size="small"><i class="el-icon-circle-plus-outline"></i>新增</el-button>
        </el-form-item>
      </el-col>
    </el-row>
  </el-form>
  -->
  
   <div class='forms_table_title'>
       <i class='el-icon-s-data'></i>自定义报表列表
   </div> 
   <el-table
     ref='multipleTable'
     @selection-change='handleSelectionChange'
     :data='tableData'
     border
     stripe
     v-loading='tableLoading'
     style='width: 100%'
    >
     <el-table-column
            type="index"
            label="序号"
            fixed
            align = "center"
            width="60">
      </el-table-column>
     <el-table-column
       prop='reportName'
       show-overflow-tooltip
       label='报表名称'
       min-width='100'
       algin='left'
       header-align='center'
      >
          <template slot-scope='scope'>
             <span >{{ scope.row.reportName | noDataFilter }}</span>
          </template>
      </el-table-column>
      <el-table-column
       prop='remark'
       show-overflow-tooltip
       label='报表说明'
       min-width='100'
       algin='left'
       header-align='center'
      >
          <template slot-scope='scope'>
             <span >{{ scope.row.remark | noDataFilter }}</span>
          </template>
      </el-table-column>
	  
	  <!--
      <el-table-column
       prop='userName'
       show-overflow-tooltip
       label='创建人'
       min-width='100'
       algin='left'
       header-align='center'
      >
          <template slot-scope='scope'>
             <span >{{ scope.row.userName | noDataFilter }}</span>
          </template>
      </el-table-column>
	  -->
	  
       <el-table-column label="操作" fixed="right" min-width="120" align="center">
        <template slot-scope="scope">
          <el-button type="primary" size="small" @click="searchData(scope.row)">访问</el-button>
		  <!--
           <el-button type="primary" size="small" @click="editData(scope.row)">编辑</el-button>
          <el-button type="danger" plain size="small" @click="delData(scope.row)">删除</el-button>
		  -->
        </template>
      </el-table-column>
     </el-table>
     <Pagination :total = 'total' :page = 'formInline.pageNum'   :limit = 'formInline.pageSize'  @pagination='Pagination'></Pagination>

     <!-- 新增代办 -->
    <el-dialog :title="countTitle" customClass="customReportNewListWidth"   center :visible.sync="countDialog" :close-on-click-modal="false">
      <el-container >
        <el-main class="mainBox" v-if="countDialog">
          <el-form
            :inline="true"
            ref="formCount"
            :model="formCount"
            :rules="countRules"
            label-position="right"
          >
            <el-form-item  label="报表名称"  prop="reportName" class="mb20" :label-width="formLabelWidth">
               <el-input
                  v-model="formCount.reportName"
                  type="text"
                  maxlength="80"
                  auto-complete="off"
                  size="small"
                  placeholder="请输入"
                />
            </el-form-item>
             <el-form-item label="是否开放" prop="status" class="mb20" :label-width="formLabelWidth">
                  <el-select v-model="formCount.status"  size="small"  placeholder="请选择"  >
                     <el-option
                      v-for="(group, index) in isOpenArr"
                      :value="group.dimCde"
                      :key="index"
                      :label="group.dimNme">
                    </el-option>
                  </el-select>
             </el-form-item>
             <br>
             <el-form-item  label="展示排序"  prop="orderStr" class="mb20" :label-width="formLabelWidth">
               <el-input
                  v-model="formCount.orderStr"
                  type="text"
                  auto-complete="off"
                  size="small"
                  placeholder="请输入"
                />
            </el-form-item>
            <br>
            <el-form-item  label="报表说明"  prop="remark" class="mb20" :label-width="formLabelWidth">
              <el-input
                type="textarea"
                :rows="3"
                maxlength="80"
                style="width: 510px;"
                placeholder="请输入报表说明"
                v-model="formCount.remark">
              </el-input>
            </el-form-item>
            <br>
            <el-form-item  label="填写SQL"  prop="selectSql" class="mb20" :label-width="formLabelWidth">
              <el-input
                type="textarea"
                :rows="3"
                style="width: 510px;"
                placeholder="请输入sql"
                v-model="formCount.selectSql">
              </el-input>
              

              <el-tooltip placement="top" effect="light">
              <div slot="content">目前sql查询支持MyBatis写法(例如：vc_fundcode = #{fundCode})<br/>查询条件支持：产品代码(fundCode),开始时间(beginDate),结束时间(endDate)</div>
              <i style="color:red" class="el-icon-info"></i>
            </el-tooltip>
            </el-form-item>
           
           
          </el-form>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="countDialog = false">取 消</el-button>
        <el-button type="primary" size="small" :loading="countSubmit_btn" @click="countSubmit('formCount')">确 定</el-button>
      </div>
    </el-dialog>

     <!-- 新增代办 -->
    <el-dialog title="详情" customClass="customReportNewListWidth"   :before-close="handleClose"  center :visible.sync="detailDialog" :close-on-click-modal="false">
      <el-container >
        <el-main class="mainBox">
             <el-form
      :inline="true"
      ref="formInlineDetail"
      :model="formInlineDetail"
      style="margin-bottom: 8px;"
      class="demo-form-inline form_inline_search"
    >
      <el-row>
        <el-col :span="18">
          <div style="width:100%;">
             <el-form-item label="产品代码" prop="fundCode">
                <!-- <el-select clearable filterable  v-model="formInlineDetail.fundCode"  size="small"  placeholder="请选择"  >
                  <el-option
                    v-for="(group, index) in fundCodeArr"
                    :value="group.value"
                    :key="index"
                    :label="group.name">
                  </el-option>
                </el-select> -->
                <el-input
                  v-model="formInlineDetail.fundCode"
                  type="text"
                  auto-complete="off"
                  size="small"
                  placeholder="请输入"
                />
                  </el-form-item>
                  <el-form-item label="开始日期" prop="beginDate">
                      <el-date-picker
                        v-model="formInlineDetail.beginDate"
                        type="date"
                        value-format="yyyy-MM-dd"
                        placeholder="选择日期">
                    </el-date-picker>
                  </el-form-item>
                  <el-form-item label="结束日期" prop="endDate">
                      <el-date-picker
                        v-model="formInlineDetail.endDate"
                        type="date"
                        value-format="yyyy-MM-dd"
                        placeholder="选择日期">
                    </el-date-picker>
                  </el-form-item>
              </div>
            </el-col>
            <el-col :span="6">
              <el-form-item class="search_button_com">
                <el-button type="primary" @click="report(true)"  style="margin-bottom: 5px; " size="small">
                  <i class="el-icon-search"></i>查询
                </el-button>
                <el-button type="primary" plain @click="restFormDetail()"  style="margin-bottom: 5px; " size="small">
                  <i class="el-icon-delete"></i>重置
                </el-button>
                 <el-button type="primary" plain @click="download()"  style="margin-bottom: 5px; " size="small">
                    <i class="el-icon-download"></i>导出
                 </el-button>
                <!-- <el-button type="primary"  plain  @click="addData()" style="margin-bottom: 5px; " size="small"><i class="el-icon-circle-plus-outline"></i>新增</el-button> -->
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>

         <div class="forms_table_title">
            <i class="el-icon-s-data"></i>自定义数据列表
          </div>

          <div>
              <el-table
                ref="multipleTable"
                :data="tableDataDetail"
                border
                stripe
                v-loading="tableLoadingDetail"
                style="width: 100%"
              >

            <el-table-column
              v-for="(group, index) in tableDataDetailArr"
                :key="index"
                :prop="group.code"
                show-overflow-tooltip
                :label="group.name"
                min-width="100"
                algin="left"
                header-align="center"
              >
            </el-table-column>
          </el-table>
          <Pagination :total="totalDetail" :page="formInlineDetail.pageNum" :limit="formInlineDetail.pageSize" @pagination ="PaginationDetail"></Pagination>
          </div>
        </el-main>
      </el-container>
    </el-dialog>

   </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import commonFun from '@/filters/new_common'
import pageApi from "@/api/dataReport/customReportList";
import commonApi from "@/api/common";
import store from "@/store";
 import {FILE_URL} from '@/utils/request'
export default {
   name:'',
   components: {Pagination},
   data () {
      return {
         formInline:{
            reportName:'',
            pageSize: 50,
            pageNum:1
         },
         tableData: [], //表格数据
         tableLoading: false, //表格加载
         tableMultipleSelection: [],//表格选择数据集合
         total:0,//总条数
         countDialog: false, // 弹窗
          countTitle:"",//标题
          countFormList:"",//是新增还是编辑
          // 新增 编辑计算任务
          formCount: {
          reportName:'',//报表名称
          status:'',//是否开放
          orderStr:'',//展示排序
          remark:'', //报表说明
          selectSql:'' //填写SQL
         
          },
          // 操作类型 1、添加 2、编辑
          operationType: 1,
          // 弹窗验证规则
          countRules: {
             reportName: [
                { required: true, type: 'string', message: "请输入报表名称", trigger: "change" },
                 { pattern: /^[\u4e00-\u9fa5a-zA-Z0-9\.\,\-\_\|]+$/, message: '请输入中文,英文或者数字' }
              ],
              selectSql: [
                { required: true, type: 'string', message: "请输入Sql", trigger: "change"}
              ],
              status: [
                { required: true, trigger: "change", message: "请选择是否开放"}
              ]
          },
          formLabelWidth: "120px",
          countSubmit_btn:false, //保存按钮加载
          detailDialog:false,
          formInlineDetail:{
            uuid:'',
            fundCode:'',
            beginDate:'',
            endDate:'',
            pageSize: 50,
            pageNum:1
         },
         tableDataDetail:[],
         tableLoadingDetail:false,
         tableDataDetailArr:[],
         fundCodeArr:[],
         isOpenArr:[
            {dimCde:'1',dimNme:'是'},
            {dimCde:'0',dimNme:'否'}
         ],
         totalDetail:0,
         
      };
   },


   mounted() {
     this.onSubmit();
     this.getProductsAll();
   },

   methods: {
     // 查询 
      onSubmit(flag){
         this.tableLoading = true;
         // 消除没有值的参数
         if(flag){
             this.formInline.pageNum = 1;
         }
         let params = commonFun.parameterSrc(this.formInline);
         pageApi.getDataSourceList(params).then(response => { 
            if(response.data.status === 200){ 
                this.tableData = response.data.data.list; 
                 // 页面总条数 
                this.total = response.data.data.total; 
             } 
             else{ 
                this.tableData = []; 
                this.total = 0; 
                this.formInline.pageSize = 50; 
                this.formInline.pageNum = 1; 
            } 
                this.tableLoading = false; 
            }).catch(() => { 
                this.tableData = []; 
                this.total = 0; 
                this.formInline.pageSize = 50;
                this.formInline.pageNum = 1;
                this.tableLoading = false;
      })
    },
    //分页
    Pagination(val){
       this.formInline.pageSize = val.limit;//页面条数
       this.formInline.pageNum = val.page;//页面
       this.onSubmit(false);
    },
    PaginationDetail(val){
       this.formInlineDetail.pageSize = val.limit;//页面条数
       this.formInlineDetail.pageNum = val.page;//页面
       this.report(false);
    },
     // table批量选择结果
    handleSelectionChange(val) {
       this.tableMultipleSelection = val;
    },
   
     //dialog关闭事件
     handleClose(done) {
         done();
         this.tableDataDetail = [];
         this.tableDataDetailArr = [];
       
      },
     // table批量选择结果
    restForm(formName) {
       var self = this;
       //self.refs[formName].resetFields();
       this.formInline.reportName = '';
    },
     //新增确认
      countSubmit(formName){
        var self = this;
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.$message.closeAll()
            
            if (this.operationType === 1) {
              // 添加
              this.saveData();
            } else {
              // 修改
              this.updateParamSet();
            }
          } else {
            return false;
          }
        })
      },
    //新增数据
      addData(){
        this.countTitle = "新增";
        this.countFormList = "add";
        this.countDialog = true;
        this.operationType =1;
        // 清除
        this.$nextTick(() => {
          this.$refs["formCount"].resetFields();
          this.formCount.reportName = ""; //报表名称
          this.formCount.status = '';//是否开放
          this.formCount.orderStr = '';//展示排序
          this.formCount.remark = '';//报表说明
          this.formCount.selectSql = '';//填写SQL
            this.formCount.id = '';
        });

      },
       //保存
      saveData(){
        this.$confirm("确定新增?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        })
          .then(() => {
            let params = {};
            params = commonFun.parameterSrc(this.formCount);
            this.countSubmit_btn = true;
            pageApi.addDataSource(params).then(response => {
              if(response.data.status === 200){
                // 关闭移动指标弹框
                this.countDialog = false;
                this.$message.closeAll()
                this.$message({
                  message: '新增成功',
                  type: 'success'
                });
                // 刷新列表
                this.onSubmit(true);
              }
              else{
                // 关闭移动指标弹框
               // this.countDialog = false;
                this.$message.closeAll()
                this.$message({
                  message: response.data.message || '新增失败',
                  type: 'warning'
                });
              }
              this.countSubmit_btn = false;
            }).catch(() => {
              // 关闭移动指标弹框
              //this.countDialog = false;
              //this.countSubmit_btn = false;
              this.$message.closeAll()
              this.$message({
                message: '新增失败',
                type: 'warning'
              });

            })

          })
          .catch(() => {
            // 关闭移动指标弹框
            //this.countDialog = false;
            this.countSubmit_btn = false;
          });
      },
      searchData(row){
           this.detailDialog =true;
           this.formInlineDetail.uuid = row.id;
           this.formInlineDetail.fundCode = '';
           this.formInlineDetail.beginDate = '';
           this.formInlineDetail.endDate = '';
           this.formInlineDetail.pageSize = 50;
           this.formInlineDetail.pageNum = 1;

           this.report(true);
            
      },
      report(flag){
         this.tableLoadingDetail = true;
            let params = {};
            if(flag){
              this.formInlineDetail.pageNum = 1;//页码
            }
            params = this.formInlineDetail;
            //  if(params.fundCode){
            //     params.fundCode =  params.fundCode.split('_')[0];
            // }
            pageApi.reportSearchTable(params).then(response => {
            if(response.data.status === 200 && response.data.data){
              let data = response.data.data;
              if(data.list && data.list.length>0){
                  if(data.list[0].header && data.list[0].header.length>0){
                      this.tableDataDetailArr = this.getAllPrpos(data.list[0].header[0]);
                  }
                  this.tableDataDetail = data.list[0].data;
              }
              // 页面总条数
              this.totalDetail = data.total;
            }
            else{
              this.tableDataDetail = [];
              this.totalDetail = 0;
              this.formInlineDetail.pageSize = 50; //页面条数
              this.formInlineDetail.pageNum = 1;//页码
            }
          
            this.tableLoadingDetail = false;
          }).catch(() => {
            this.tableDataDetail = [];
            this.totalDetail = 0;
            this.formInlineDetail.pageSize = 50; //页面条数
            this.formInlineDetail.pageNum = 1;//页码
            this.tableLoadingDetail = false;
            
          })
      },
     getAllPrpos(formData) {
          // 用来保存所有的属性名称和值
          let data = formData;
          let arr =  [];
          
          // 开始遍历
          for(var p in data){
              let params = {};
              // 方法
              // p 为属性名称，obj[p]为对应属性的值
              params.code = ''+p;
              params.name = data[p];
              arr.push(params);
              
          }
          return arr;
          
      },
      download(){
        let params = {};
        params.uuid = this.formInlineDetail.uuid;
        params.fundCode=this.formInlineDetail.fundCode;
        params.beginDate=this.formInlineDetail.beginDate;
        params.endDate=this.formInlineDetail.endDate;

           // token信息
        if(store.state.user.token){ params["token"] = store.state.user.token;}
        let columns =  this.tableDataDetailArr;
        let tableNames = [];
        let exportPoNames = [];
        let exportFormats = [];
        for(let i=0;i<columns.length;i++){
            tableNames.push(columns[i].name);
            exportPoNames.push(columns[i].code);
            let exportFormat = 'string';
            exportFormats.push(exportFormat);
        }

        if(exportPoNames.length<=0){
            this.$message({
              message:  '列表表头为空无法导出',
              type: 'warning'
            });
            return;
        }
           // 表头名
        params["exportAliasName"] = tableNames.toString();
        // 导出文件名
        params["exportFileName"] = '导出数据.xls';
        // 数据格式化
        params["exportFormat"] = exportFormats.toString();
        // 表头属性名
        params["exportPoName"] = exportPoNames.toString();
        // 表标题
        params["exportTitle"] = '导出数据';
        // 请求地址
        let action = store.state.setting.baseApi + 'api/customReport/v1.0/dataDownLoad';

        commonFun.formDownloadFile(params,action,"POST");
         
      },
     getProductsAll() {
        commonApi.getProductsAll().then(res => {
            // eslint-disable-next-line no-unused-vars
            const self = this
            if (res.data.message === 'success') {
              const arr = res.data.data
              this.fundCodeArr = []
              for (let i = 0; i < arr.length; i++) {
                const obj = {}
                obj.value = arr[i].fundCode + '_' + arr[i].fundName
                obj.name = arr[i].fundName + ' (' + arr[i].fundCode + ')'
                this.fundCodeArr.push(obj)
              }
            } else {
              this.fundCodeArr = []
              this.$message.error('初始化数据失败')
            }
          })
          .catch(() => {
            this.fundCodeArr = []
            this.$message.error('初始化数据失败')
          })
      },
      //修改
      updateParamSet(){
        this.$confirm("确定修改?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        })
          .then(() => {
            let params = {};
            params = commonFun.parameterSrc(this.formCount);
            this.countSubmit_btn = true;
            pageApi.updateDataSource(params).then(response => {
              if(response.data.status === 200){
                // 关闭移动指标弹框
                this.countDialog = false;
                this.$message.closeAll()
                this.$message({
                  message: '修改成功',
                  type: 'success'
                });
                 // 刷新列表
                this.onSubmit(false);

              }
              else{
                // 关闭移动指标弹框
                //this.countDialog = false;
                this.$message.closeAll()
                this.$message({
                  message: response.data.message || '修改失败',
                  type: 'warning'
                });
              }
              this.countSubmit_btn = false;
            }).catch(() => {
              // 关闭移动指标弹框
              //this.countDialog = false;
              this.countSubmit_btn = false;
              this.$message.closeAll()
              this.$message({
                message: '修改失败',
                type: 'warning'
              });
            })

          })
          .catch(() => {
            // 关闭移动指标弹框
            //this.countDialog = false;
            this.countSubmit_btn = false;
          });
      },
       // 行编辑数据
      editData(row) {
        this.countTitle = "编辑";
        this.countFormList = "edit";
        this.countDialog = true;
        this.operationType =2;

        this.$nextTick(() => {
          this.$refs["formCount"].resetFields();
          this.formCount.reportName = row.reportName;
          this.formCount.status = row.status;
          this.formCount.orderStr = row.orderStr;
          this.formCount.remark = row.remark;
          this.formCount.selectSql = row.selectSql;
          this.formCount.id = row.id;

        });

      },
      // 行删除数据
    delData(row) {
      this.$confirm("确定删除?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      })
        .then(() => {
          let params = {};
          params.id = row.id;
          pageApi.deleteDataSource(params)
            .then(response => {
              if (response.data.status === 200) {
                this.$message.closeAll();
                this.$message({
                  message: "删除成功",
                  type: "success"
                });
                // 刷新列表
                this.onSubmit(false);
              } else {
                this.$message.closeAll();
                this.$message({
                  message: response.data.message || "删除失败",
                  type: "warning"
                });
              }
            })
            .catch(() => {
              // 关闭移动指标弹框
              this.$message.closeAll();
              this.$message({
                message: "删除失败",
                type: "warning"
              });
            });
        })
        .catch(() => {});
    },
    restFormDetail(){
      this.formInlineDetail.fundCode = '';
      this.formInlineDetail.beginDate = '';
      this.formInlineDetail.endDate = '';
    }

 }
}
</script>
<style lang='css' scoped>

</style>
<style>
.customReportNewListWidth{
  width: 65% !important;
}
.el-dialog .el-form {
     width: 100%!important; 
}
</style>
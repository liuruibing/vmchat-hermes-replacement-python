<template>
  <div>
      <el-form
      :inline="true"
      ref="formInline"
      :model="formInline"
      style="margin-bottom: 8px;"
      class="demo-form-inline form_inline_search"
    >
      <el-row>
        <el-col :span="18">
          <div style="width:100%;">
            <el-form-item label="SQL" prop="querySql">
              <el-input
                  type="textarea"
                  :rows="3"
                  style="width:500px !important"
                 
                  placeholder="请输入内容"
                  v-model="formInline.querySql">
                </el-input>
            </el-form-item>
            
            
          </div>
        </el-col>
        <el-col :span="6">
          <el-form-item class="search_button_com">
            <el-button type="primary" @click="onSubmit(true)"  style="margin-bottom: 5px; " size="small">
              <i class="el-icon-search"></i>查询
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
          @selection-change="handleSelectionChange"
          :data="tableData"
          border
          stripe
          v-loading="tableLoading"
          style="width: 100%"
        >

       <el-table-column
         v-for="(group, index) in tableDataArr"
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
     <Pagination :total="total" :page="formInline.pageNum" :limit="formInline.pageSize" @pagination = "Pagination"></Pagination>
    </div>

  </div>
</template>

<script>
import commonFun from '@/filters/new_common'
import pageApi from "@/api/dataReport/customReportList";
import Pagination from '@/components/Pagination'
import store from "@/store";
 import {FILE_URL} from '@/utils/request'

export default {
    name: 'customReportList',
    components: {
      Pagination
    },
    data() {
      return {
        formInline:{
          querySql:'',
          pageSize: 50,//条数
          pageNum:1
        },
        total: 0, //列表条数
        pageNum:1, //页码
        pageSize: 50,//条数
        tableNameArr:[],
        tableLoading:false,
        tableData:[],
        tableDataArr:[],
        submitData:{
           tableName:'' //表名称
        },
         isSubmit:false,
        submitDataQuery:{}
      }
    },
    //页面加载后触发
   mounted(){
     this.onSubmit(true);
   },
   methods: {
       //列表选择
        handleSelectionChange(val) {
          this.tableMultipleSelection = val;
        },
        //排序
        handleSortChange(val) {
          //this.formInline.orderStr = commonFun.orderByString(val);
          //this.selectAllTable(false);
        },
        //分页
        Pagination(val) {
          this.formInline.pageSize = val.limit; //页面条数
          this.formInline.pageNum = val.page;//页码
          // this.formInline.offset = (val.page -1) * val.limit;
          // this.formInline.limit = val.limit; //页面条数
          this.onSubmit(false);
        },
          //查询
    onSubmit(flag){
        this.isSubmit = true;
        if(flag){
        this.formInline.pageNum = 1;//页码
      }
        this.selectAllTable(true);
    },
     selectAllTable(flag){
      this.tableLoading = true;
      // 消除没有值的参数
      let params = commonFun.parameterSrc(this.formInline);
      pageApi.getDataTableNameList(params).then(response => {
       
        if(response.data.status === 200 && response.data.data){
          let data = response.data.data;
          if(data.list && data.list.length>0){
              if(data.list[0].header && data.list[0].header.length>0){
                   this.tableDataArr = this.getAllPrpos(data.list[0].header[0]);
              }
              this.tableData = data.list[0].data;
          }
          // 页面总条数
          this.total = data.total;
        }
        else{
          this.tableData = [];
          this.total = 0;
          this.formInline.pageSize = 50; //页面条数
          this.formInline.pageNum = 1;//页码
        }
       
        this.tableLoading = false;
      }).catch(() => {
        this.tableData = [];
        this.total = 0;
        this.formInline.pageSize = 50; //页面条数
        this.formInline.pageNum = 1;//页码
        this.tableLoading = false;
        
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
        let params = commonFun.parameterSrc(this.formInline);
        params.pageSize='';
        params.pageNum='';
        params = commonFun.parameterSrc(params);

           // token信息
        if(store.state.user.token){ params["token"] = store.state.user.token;}
        let columns =  this.tableDataArr;
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
        let action = store.state.setting.baseApi + 'api/customReport/v1.0/sqlDataDownLoad';

        commonFun.formDownloadFile(params,action,"POST");
         
      }

   }

}
</script>
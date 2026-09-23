<template>
   <div>
  <!-- <el-form :inline='true'  ref='formInline' :model='formInline' style='margin-bottom: 8px;' class='demo-form-inline form_inline_search' >
    <el-row>
      <el-col :span='16'>
         <div style='width:100%;height:50px;'>
             <el-form-item label='核对状态' prop='name'>
                  <el-input type='text' v-model.trim='formInline.checkStatus' clearable placeholder='请输入名称' size='small'></el-input>
              </el-form-item>

              
         </div>
      </el-col>
      <el-col :span='8'>
         <el-form-item class='search_button_com'>
            <el-button type='primary' @click='onSubmit(true)' style='margin-bottom: 5px;' size='small'><i class='el-icon-search'></i>查询</el-button>
            <el-button type='primary' plain @click='restForm()' style='margin-bottom: 5px; ' size='small'><i class='el-icon-delete'></i>重置</el-button>
        </el-form-item>
      </el-col>
    </el-row>
  </el-form> -->
   <div class='forms_table_title'>
       <i class='el-icon-s-data'></i>操作日志列表
   </div> 
   <el-table
     ref='multipleTable'
     @selection-change='handleSelectionChange'
     @sort-change="handleSortChange"
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
       prop='operationStep'
       sortable='custom'
       show-overflow-tooltip
       label='操作步骤'
       min-width='100'
       algin='left'
       header-align='center'
      >
          <template slot-scope='scope'>
             <span v-if="scope.row.operationStep === '1'">一键生成</span>
             <span v-else-if="scope.row.operationStep === '2'">勾稽校验</span>
              <span v-else-if="scope.row.operationStep === '3'">与外包核对</span>
               <span v-else-if="scope.row.operationStep === '4'">复核确认</span>
                <span v-else-if="scope.row.operationStep === '5'">一键上报</span>
                 <span v-else-if="scope.row.operationStep === '6'">报表下载</span>
				 <span v-else-if="scope.row.operationStep === '7'">取消复核</span>
             <span v-else>{{ scope.row.operationStep | noDataFilter }}</span>
          </template>
      </el-table-column>

      <el-table-column
       prop='operationStatus'
       sortable='custom'
       show-overflow-tooltip
       label='操作状态'
       min-width='100'
       algin='left'
       header-align='center'
      >
          <template slot-scope='scope'>
              <span v-if="scope.row.operationStatus === '1'">操作成功</span>
             <span v-else-if="scope.row.operationStatus === '2'">操作失败</span>
              <span v-else-if="scope.row.operationStatus === '0'">正在进行</span>
              
             <span v-else>{{ scope.row.operationStatus | noDataFilter }}</span>
          </template>
      </el-table-column>

      <el-table-column
       prop='userName'
       sortable='custom'
       show-overflow-tooltip
       label='操作用户'
       min-width='100'
       algin='left'
       header-align='center'
      >
          <template slot-scope='scope'>
             <span >{{ scope.row.userName | noDataFilter }}</span>
          </template>
      </el-table-column>

       <el-table-column
       prop='beginTime'
       sortable='custom'
       show-overflow-tooltip
       label='操作开始时间'
       min-width='100'
       algin='left'
       header-align='center'
      >
          <template slot-scope='scope'>
             <span >{{ scope.row.beginTime | noDataFilter }}</span>
          </template>
      </el-table-column>


      <el-table-column
       prop='endTime'
       sortable='custom'
       show-overflow-tooltip
       label='操作结束时间'
       min-width='100'
       algin='left'
       header-align='center'
      >
          <template slot-scope='scope'>
             <span >{{ scope.row.endTime | noDataFilter }}</span>
          </template>
      </el-table-column>

      <el-table-column
       prop='remark'
       sortable='custom'
       show-overflow-tooltip
       label='日志信息'
       min-width='140'
       algin='left'
       header-align='center'
      >
          <template slot-scope='scope'>
             <span >{{ scope.row.remark | noDataFilter }}</span>
          </template>
      </el-table-column>
      
     </el-table>
     <Pagination :total='total' :page='formInline.pageNum'   :limit='formInline.pageSize'  @pagination='Pagination'></Pagination>
   </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import commonFun from '@/filters/new_common'
import pageApi from '@/api/xbrl/xbrl'
export default {
   name:'annExcel',
   components: {Pagination},
   props: {
      PageData: {
       recordId:''
      },
    },
   data () {
      return {
         formInline:{
            checkStatus:'',
            recordId:'',
            orderString:'',
            pageSize: 50,
            pageNum:1
         },
         tableData: [], //表格数据
         tableLoading: false, //表格加载
         tableMultipleSelection: [],//表格选择数据集合
         total:0,//总条数
      };
   },


   mounted() {
     this.formInline.recordId = this.PageData.recordId;
     this.onSubmit(true);
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
         pageApi.getLogInfo(params).then(response => { 
            if(!response.data.error){ 
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
     // table批量选择结果
    handleSelectionChange(val) {
       this.tableMultipleSelection = val;
    },
    //排序
    handleSortChange(val) {
      this.formInline.orderString = commonFun.orderByString(val);
    
     this.onSubmit(false);
    },
     // table批量选择结果
    restForm() {
       var self = this;
       self.refs['formInline'].resetFields();
    }
 }
}
</script>
<style lang='css' scoped>

</style>
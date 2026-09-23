<template>
   <div>
  <el-form :inline='true'  ref='formInline' :model='formInline' style='margin-bottom: 8px;' class='demo-form-inline form_inline_search' >
    <el-row>
      <el-col :span='16'>
         <div style='width:100%;height:50px;'>
             <el-form-item label='核对状态' prop='verifyStatus'>
                  <!-- <el-select  @change="selectChange"  v-model="formInline.verifyStatus" clearable filterable placeholder="请选择">
                    <el-option
                      v-for="item in checkStatusArr"
                      :key="item.code"
                      :label="item.name"
                      :value="item.code">
                    </el-option>
                </el-select> -->
                <el-radio @change="selectChange" v-model="formInline.verifyStatus" label="-1">全部</el-radio>
                 <el-radio @change="selectChange" v-model="formInline.verifyStatus" label="0">核对不一致</el-radio>
                <el-radio @change="selectChange" v-model="formInline.verifyStatus" label="1">核对一致</el-radio>
              </el-form-item>

              
         </div>
      </el-col>
      <el-col :span='8'>
         <el-form-item class='search_button_com'>
            <!-- <el-button type='primary' @click='onSubmit(true)' style='margin-bottom: 5px;' size='small'><i class='el-icon-search'></i>查询</el-button>
            <el-button type='primary' plain @click='restForm()' style='margin-bottom: 5px; ' size='small'><i class='el-icon-delete'></i>重置</el-button> -->
        </el-form-item>
      </el-col>
    </el-row>
  </el-form>
   <div class='forms_table_title'>
       <i class='el-icon-s-data'></i>列表
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
       prop='elementName'
       sortable='custom'
       show-overflow-tooltip
       label='核对项'
       min-width='100'
       algin='left'
       header-align='center'
      >
          <template slot-scope='scope'>
             <span >{{ scope.row.elementName | noDataFilter }}</span>
          </template>
      </el-table-column>

      <el-table-column
       prop='lineName'
       sortable='custom'
       show-overflow-tooltip
       label='行号'
       min-width='100'
       algin='left'
       header-align='center'
      >
          <template slot-scope='scope'>
             <span >{{ scope.row.lineName | noDataFilter }}</span>
          </template>
      </el-table-column>

      <el-table-column
       prop='columnName'
       sortable='custom'
       show-overflow-tooltip
       label='列号'
       min-width='100'
       algin='left'
       header-align='center'
      >
          <template slot-scope='scope'>
             <span >{{ scope.row.columnName | noDataFilter }}</span>
          </template>
      </el-table-column>

      <el-table-column
       prop='elementValueOwn'
       sortable='custom'
       show-overflow-tooltip
       label='系统值'
       min-width='100'
       algin='left'
       header-align='center'
      >
          <template slot-scope='scope'>
             <span >{{ scope.row.elementValueOwn | noDataFilter }}</span>
          </template>
      </el-table-column>

      <el-table-column
       prop='elementValueImp'
       sortable='custom'
       show-overflow-tooltip
       label='外包值'
       min-width='100'
       algin='left'
       header-align='center'
      >
          <template slot-scope='scope'>
             <span >{{ scope.row.elementValueImp | noDataFilter }}</span>
          </template>
      </el-table-column>

      <el-table-column
       prop='verifyStatus'
       sortable='custom'
       show-overflow-tooltip
       label='核对状态'
       min-width='100'
       algin='left'
       header-align='center'
      >
          <template slot-scope='scope'>
             <span style="color:red" v-if="scope.row.verifyStatus === '0'">核对不一致</span>
             <span  v-else-if="scope.row.verifyStatus === '1'">核对一致</span>
             <span v-else>{{ scope.row.verifyStatus | noDataFilter }}</span>
          </template>
      </el-table-column>

      <el-table-column
       prop='valueDiff'
       sortable='custom'
       show-overflow-tooltip
       label='差值'
       min-width='100'
       algin='left'
       header-align='center'
      >
          <template slot-scope='scope'>
             <span style="color:red" v-if="scope.row.valueDiff && scope.row.valueDiff!='0'">{{ scope.row.valueDiff | noDataFilter }}</span>
             <span v-else>{{ scope.row.valueDiff | noDataFilter }}</span>
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
   name:'annTxt',
   components: {Pagination},
   props: {
      PageData: {
       recordId:''
      },
    },
   data () {
      return {
         formInline:{
            verifyStatus:'-1',
            recordId:'',
            orderString:'',
            pageSize: 20,
            pageNum:1
         },
         tableData: [], //表格数据
         tableLoading: false, //表格加载
         tableMultipleSelection: [],//表格选择数据集合
         total:0,//总条数
         checkStatusArr:[
           {code:'0',name:'核对不一致'},
           {code:'1',name:'核对一致'},
		   {code:'',name:'全部'}
         ]
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
        if(this.formInline.verifyStatus && this.formInline.verifyStatus==='-1'){
           params.verifyStatus = '';
         }
         pageApi.geVerifyDetail(params).then(response => { 
            if(!response.data.error){ 
                this.tableData = response.data.data.list; 
                 // 页面总条数 
                this.total = response.data.data.total; 
             } 
             else{ 
                this.tableData = []; 
                this.total = 0; 
                this.formInline.pageSize = 10; 
                this.formInline.pageNum = 1; 
            } 
                this.tableLoading = false; 
            }).catch(() => { 
                this.tableData = []; 
                this.total = 0; 
                this.formInline.pageSize = 10;
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
    },
    selectChange(val){
         this.onSubmit(false);
    }
 }
}
</script>
<style lang='css' scoped>

</style>
<template>
  <div>
      <div class="toolbar" >
     <el-form :inline="true" ref = "formInline" :model="formInline"  class="demo-form-inline form_inline_search" >
          <el-row>
            <el-col :span="20">
              <div class="grid-content bg-purple">
           
          <el-form-item label="统计日期" >
              <el-date-picker
                              v-model="formInline.beginDate"
                              type="date"
                              size="small"
                              @change="getdateValue"
                              value-format="yyyy-MM-dd">
                            </el-date-picker>
                            <span style="padding: 0 3px;font-size: 14px;color: #171717;">至</span>
                            <el-date-picker
                              v-model="formInline.endDate"
                              type="date"
                              size="small"
                              @change="getdateVal"
                            value-format="yyyy-MM-dd">
                        </el-date-picker>
                        </el-form-item>

             <!-- <el-form-item>
                <el-checkbox >母基金</el-checkbox>
              </el-form-item> -->
              </div>
            </el-col>
            <el-col :span="4">
              <div class="grid-content bg-purple-light">
                <el-form-item  class="search_button_com">
                  <el-button type="primary" @click="onSubmit('formInline')" style="margin-bottom: 5px;" size="small"><i class="el-icon-search"></i>查询</el-button>
                  <el-button type="primary" style="margin-bottom: 5px;" plain size="small" @click="restForm('formInline')"><i class='el-icon-delete'></i>重置</el-button>
                </el-form-item>
              </div>
            </el-col>
          </el-row>
        </el-form>
  </div>
 <div class="forms_table_title">
      <i class="el-icon-s-data"></i>产品申赎明细统计
    </div>
     <!-- sortable='custom' -->
 <el-table
      ref="multipleTable"
      @selection-change="handleSelectionChange"
      @sort-change="handleSortChange"
      :data="tableData"
      :default-sort="{prop: 'FUNDNAME', order: 'descending'}" 
      border
      stripe
      v-loading="tableLoading"
      style="width: 100%"
    >
      <el-table-column
        type="index"
        label="序号"
        fixed
        align = "center"
        width="50">
      </el-table-column>
          <el-table-column
        prop="VC_FUNDCODE"
        label="基金代码"
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.VC_FUNDCODE | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="VC_FUNDNAME"
        label="基金名称"
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.VC_FUNDNAME | noDataFilter}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="VC_MANAGER_NAME"
        label="基金经理"
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.VC_MANAGER_NAME | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="F_SGZJE"
        label="申购总金额(元)"
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_SGZJE | moneyThousand}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="F_ZXSGJE"
        label="直销申购金额(元)"
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_ZXSGJE | moneyThousand}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="F_ZXSGZB"
        label="直销申购占比(%)"
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_ZXSGZB | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="F_DXSGJE"
        label="代销申购金额(元)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_DXSGJE | moneyThousand}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="F_SGKHS"
        label="申购客户数"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_SGKHS | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="F_SGZXKHS"
        label="申购直销客户数"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_SGZXKHS | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="F_SGDXKHS"
        label="申购代销客户数"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_SGDXKHS | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="F_SGZRRKHS"
        label="申购自然人客户数"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_SGZRRKHS | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="F_SGJGCPKHS"
        label="申购机构/产品客户数"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_SGJGCPKHS | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="F_SHZFE"
        label="赎回总份额(元)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_SHZFE | moneyThousand}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="F_SHZJE"
        label="赎回总金额(元)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_SHZJE | moneyThousand}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="F_SHZXJE"
        label="赎回直销金额(元)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_SHZXJE | moneyThousand}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="F_SHZXZB"
        label="赎回直销占比(%)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_SHZXZB | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="F_SHDXJE"
        label="赎回代销金额(元)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_SHDXJE | moneyThousand}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="F_SHKHS"
        label="赎回客户数"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_SHKHS | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="F_SHZXKHS"
        label="赎回直销客户数"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_SHZXKHS | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="F_SHDXKHS"
        label="赎回代销客户数"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_SHDXKHS | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="F_JSHJE"
        label="净申赎金额(元)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_JSHJE | moneyThousand}}</span>
        </template>
      </el-table-column>
    </el-table>
     <Pagination :total="total" :page="pageNum" :limit = "pageSize" @pagination = "Pagination"></Pagination>
  </div>
</template>

<script>
 import Pagination from '@/components/Pagination'
 import commonFun from '@/filters/new_common'
 import pageApi from "@/api/reportCenter/productDetaile";
 import $ from 'jquery'
export default {
    name: 'productDetaile',
    components: {
      Pagination
    },
    data() {
      return {
          formInline:{
             beginDate: '', // 开始日期
             endDate: '',  //结束日期
            //orderString: '', //列表排序
            limit: 50,//条数
            offset:0
          },
          total: 0, //列表条数
          pageNum:1, //页码
          pageSize: 50,//条数
          tableData:[],//列表数据
          tableLoading:false, //列表加载
          tableMultipleSelection:[],
          submitData:{}, //搜索数据
          isSubmit:false, //是否点击搜索
      }
    },
    //页面加载后触发
   mounted(){
  this.getCurrentMonthFirst()
       this.getCurrentDay()
       this.selectAll(true);


   },


   methods: {
      //列表选择
     handleSelectionChange(val) {
      this.tableMultipleSelection = val;
    },
    //排序
    handleSortChange(val) {
      this.formInline.orderString = commonFun.orderByString(val);
      this.selectAll(false);
    },
    //分页
    Pagination(val) {
      this.pageSize = val.limit; //页面条数
      this.pageNum = val.page;//页码
      this.formInline.offset = (val.page -1) * val.limit;
      this.formInline.limit = val.limit; //页面条数
      this.isSubmit = false;
      this.selectAll(false);
    },
     restForm(formName){
        var self = this;
        self.$refs[formName].resetFields();
        this.formInline.beginDate = '';
        this.formInline.endDate = '';

     },

       //查询
    onSubmit(flag){
        this.isSubmit = true;
        if(flag){
        this.pageNum = 1;
        this.formInline.offset = 0;
      }

        let data = this.formInline;
        this.submitData.endDate = data.endDate; // 选择结束日期
        this.submitData.beginDate = data.beginDate; // 选择开始日期
        this.submitData.orderString = data.orderString;//列表排序
        this.submitData.limit = data.limit;//条数
        this.submitData.offset = data.offset;//分页
        this.selectAll(true);
    },
    selectAll(flag){
      this.tableLoading = true;

      let data = this.formInline;
      let data2 = this.submitData;
      let isSubmit = this.isSubmit;
      if(isSubmit){
          data = data2;
      }
      // 消除没有值的参数
      let params = commonFun.parameterSrc(data);
      if(flag){
        this.pageNum = 1;
        this.formInline.offset = 0;
        params.offset = 0;
      }
      pageApi.getDataSourceList(params).then(response => {
        if(!response.data.error){
          this.tableData = response.data.rows;
          // 页面总条数
          this.total = response.data.total;
        }
        else{
          this.tableData = [];
          this.total = 0;
          this.formInline.limit = 50;
           this.pageSize = 50;
          this.pageNum = 1;
          this.formInline.offset = 0;

        }
        this.tableLoading = false;

      }).catch(() => {
        this.tableData = [];
        this.total = 0;
        this.pageSize = 50;
         this.formInline.limit = 50;
        this.pageNum = 1;
        this.formInline.offset = 0;
        this.tableLoading = false;
      })
    },

           getdateValue (val) {
           this.formInline.beginDate = val
          //  this.getbalanceIndexData()
         },
         getdateVal (val) {
           this.formInline.endDate = val
          //  this.getbalanceIndexData()
         },

        getCurrentMonthFirst () {
           var date = new Date()
           date.setDate(1)
           var month = parseInt(date.getMonth() + 1)
           var day = date.getDate()
           if (month < 10)  month = '0' + month
           if (day < 10)  day = '0' + day
           this.formInline.beginDate = date.getFullYear() + '-' + month + '-' + day
         },
        getCurrentDay () {
         var date = new Date();
        var seperator1 = "-";
       var year = date.getFullYear();
       var month = date.getMonth() + 1;
       var strDate = date.getDate();
      if (month >= 1 && month <= 9) {
      month = "0" + month;
         }
          if (strDate >= 0 && strDate <= 9) {
             strDate = "0" + strDate;
        }
    var currentdate = year + seperator1 + month + seperator1 + strDate;
           this.formInline.endDate = currentdate;
         },

   }

}
</script>

<style>
.productSearchWidth{
  width: 70% !important;
}
</style>

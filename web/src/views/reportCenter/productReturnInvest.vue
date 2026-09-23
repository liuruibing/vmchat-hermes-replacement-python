<template>
  <div>
      <div class="toolbar" >
     <el-form :inline="true" ref = "formInline" :model="formInline"  class="demo-form-inline form_inline_search" >
          <el-row>
            <el-col :span="20">
              <div class="grid-content bg-purple">
                <el-form-item label="选择月份" prop="tDate">
                   <el-date-picker
                      v-model="formInline.tDate"
                      type="month"
                      placeholder="选择月">
                    </el-date-picker>

                  <!-- <el-date-picker
                    class="pickerStyle"
                    v-model="formInline.tDate"
                    type="month"
                    @change="changeMonth"
                    placeholder="选择月">
                  </el-date-picker> -->

                    <span style="color: red;">&nbsp;&nbsp;注:按照月末展示报表数据</span>
                  </el-form-item>


              </div>
            </el-col>
            <el-col :span="4">
              <div class="grid-content bg-purple-light">
                <el-form-item  class="search_button_com">
                  <el-button type="primary" @click="onSubmit('formInline')" style="margin-bottom: 5px;" size="small"><i class="el-icon-search"></i>查询</el-button>
                  <el-button type="primary" style="margin-bottom: 5px;" plain size="small" @click="restForm('formInline')"><i class='el-icon-delete'></i>重置</el-button>
                  <!-- <el-button type="primary" plain style="margin-bottom: 5px; " size="small"><i class="el-icon-download"></i>导出</el-button> -->
                </el-form-item>
              </div>
            </el-col>
          </el-row>
        </el-form>
  </div>
 <div class="forms_table_title">
      <i class="el-icon-s-data"></i>产品平均投资回报率
    </div>
    <!-- sortable='custom' -->
 <el-table
      ref="multipleTable"
      @selection-change="handleSelectionChange"
      :data="tableData"
      :default-sort="{prop: 'FUNDCODE', order: 'descending'}"
      border
      stripe
      @sort-change="handleSortChange"
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
        prop="FUNDNAME"
        label="基金名称"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.FUNDNAME | noDataFilter}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="FUNDCODE"
        label="基金代码"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.FUNDCODE | noDataFilter}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="YEARYIELD"
        label="产品平均投资回报率(YTD年化收益率)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="200"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.YEARYIELD | noDataFilter}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="SHARPE"
        label="夏普比率"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.SHARPE | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="VOLATILITY"
        label="信息比率"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.VOLATILITY | noDataFilter}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="MAXDRAWDOWN"
        label="历史最大回撤率"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.MAXDRAWDOWN | noDataFilter}}</span>
        </template>
      </el-table-column>
    </el-table>
     <Pagination :total="total" :page="pageNum" :limit = "pageSize" @pagination = "Pagination"></Pagination>
  </div>
</template>

<script>
 import store from "@/store";
 import Pagination from '@/components/Pagination'
 import commonFun from '@/filters/new_common'
 import pageApi from "@/api/reportCenter/productReturnInvest";
 import $ from 'jquery'
export default {
    name: 'productReturnInvest',
    components: {
      Pagination
    },
    data() {
      const validateDate = (rule, value, callback) => {
        if (value == "" || value === null) {
          callback(new Error("请选择日期"));
        } else {
          callback();
        }
      };
      return {
          formInline:{
            tDate: '', // 选择月份
            orderString: '', //列表排序
            limit: 50,//条数
            offset:0
          },
          // searchRules: {
          //    tDate: [{ required: true, trigger: "change", validator: validateDate }],
          // },
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

    watch: {
      // 获取baseApi
    baseApi: function(newData) {
      store.commit("BASE_API", this.baseApi);
    },
    // 获取token
    token: function(newData) {
      store.commit("TOKEN", this.token);
    }
    },
    //页面加载后触发
   mounted(){
     // // 搜索时间默认值是本月
       this.formInline.tDate = commonFun.get_newDate();
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
    Pagination(val){
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
     },

       //查询
 onSubmit(flag){
       this.isSubmit = true;
         if(flag){
         this.pageNum = 1;
         this.formInline.offset = 0;
       }

        let data = this.formInline;
        let lastDate=this.changeMonth(data.tDate);
        this.submitData.tDate =lastDate ; //
        this.submitData.orderString = data.orderString;//列表排序

        this.submitData.limit = data.limit;//条数
        this.submitData.offset = data.offset;//分页
        this.selectAll(true);
    },
   selectAll(flag){
     this.tableLoading = true;

     let data = this.formInline;

     data.tDate=this.changeMonth(data.tDate);
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


changeMonth(value){
     if(!value){
              return "";
          }
     let currMonth=commonFun.yyr_getMonth(value);
     let endTime;
  let date = new Date(value);
  let month = (date.getMonth() + 1).toString().padStart(2,'0');
  let year = date.getFullYear();
  let startTime = year + '' + month + '01';
  let day = new Date(year,month,0);

  endTime = year + '-' + month + '-' + day.getDate();

  return endTime;
},

   }

}
</script>

<style>
.productSearchWidth{
  width: 70% !important;
}
</style>

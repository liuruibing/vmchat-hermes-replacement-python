<template>
  <div>
      <div class="toolbar" >
     <el-form :inline="true" ref = "formInline" :model="formInline"  class="demo-form-inline form_inline_search" >
          <el-row>
            <el-col :span="20">
              <div class="grid-content bg-purple">
 <el-form-item label="选择月份" prop="tDate">
                <el-date-picker v-model="formInline.tDate" type="month" placeholder="选择月">
                </el-date-picker>
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
      <i class="el-icon-s-data"></i>基金基本信息
    </div>
    <!-- sortable='custom' -->
 <el-table
      ref="multipleTable"
      @selection-change="handleSelectionChange"
      :data="tableData"
      :default-sort="{prop: 'FUNDNAME', order: 'descending'}"
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
        prop="FUNDCODE"
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
        prop="CREATEDATE"
        label="成立日期"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.CREATEDATE | noDataFilter}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="STATUS"
        label="基金状态"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.STATUS | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="JJLB"
        label="基金类别"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.JJLB | noDataFilter}}</span>
        </template>
      </el-table-column>

      <!-- <el-table-column
        prop="GLLX"
        label="管理类型"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.GLLX | noDataFilter}}</span>
        </template>
      </el-table-column> -->
      <!-- <el-table-column
        prop="ZZXS"
        label="组织形式"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.ZZXS | noDataFilter}}</span>
        </template>
      </el-table-column> -->
      <el-table-column
        prop="BA"
        label="是否在中基协备案"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.BA | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="BABH"
        label="备案编号"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.BABH | noDataFilter}}</span>
        </template>
      </el-table-column>
      <!-- <el-table-column
        prop="ZC"
        label="是否注册在基金小镇"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.ZC | noDataFilter}}</span>
        </template>
      </el-table-column> -->
      <!-- <el-table-column
        prop="ZFCY"
        label="是否为政府产业基金"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.ZFCY | noDataFilter}}</span>
        </template>
      </el-table-column> -->
      <!-- <el-table-column
        prop="TZBD"
        label="主要投资标的"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.TZBD | noDataFilter}}</span>
        </template>
      </el-table-column> -->
       <el-table-column
        prop="RJGM"
        label="认缴规模(万元)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.RJGM | moneyMillion}}</span>
        </template>
      </el-table-column>
       <el-table-column
        prop="SJGM"
        label="实缴规模(万元)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.SJGM | moneyMillion}}</span>
        </template>
      </el-table-column>
       <el-table-column
        prop="LHJJ"
        label="是否为量化基金"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.LHJJ | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="DCJJ"
        label="是否为对冲基金"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.DCJJ | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="FOF"
        label="是否为FOF基金"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.FOF | noDataFilter}}</span>
        </template>
      </el-table-column>
    </el-table>
     <Pagination :total="total" :page="pageNum" :limit = "pageSize" @pagination = "Pagination"></Pagination>
  </div>
</template>

<script>
 import Pagination from '@/components/Pagination'
 import commonFun from '@/filters/new_common'
 import pageApi from "@/api/reportCenter/fundBasicInfo";
 import $ from 'jquery'
export default {
    name: 'fundBasicInfo',
    components: {
      Pagination
    },
    data() {
      return {
          formInline:{
            tDate: '', // 选择月份
            orderString: '', //列表排序
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
     },

       //查询
    onSubmit(flag){
        this.isSubmit = true;
        if(flag){
        this.pageNum = 1;
        this.formInline.offset = 0;
      }

    //     let data = this.formInline;
    //  let lastDate=this.changeMonth(data.tDate);
    //  this.submitData.tDate =lastDate ; //
    //     this.submitData.orderString = data.orderString;//列表排序
    //     this.submitData.limit = data.limit;//条数
    //     this.submitData.offset = data.offset;//分页
        this.selectAll(flag);
    },
    selectAll(flag){
      this.tableLoading = true;

      let data = this.formInline;
        data.tDate=this.changeMonth(data.tDate);
      // let data2 = this.submitData;
      // let isSubmit = this.isSubmit;
      // if(isSubmit){
      //     data = data2;
      // }
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

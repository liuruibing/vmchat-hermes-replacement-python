<template>
  <div>
      <div class="toolbar" >
     <el-form :inline="true" ref = "formInline" :model="formInline"  class="demo-form-inline form_inline_search" >
          <el-row>
            <el-col :span="20">
              <div class="grid-content bg-purple">
                <el-form-item label="净值日期" prop="tDate">
                    <el-date-picker
                    v-model="formInline.tDate"
                    type="date"
                      format="yyyy-MM-dd"
                      value-format="yyyy-MM-dd"
                    placeholder="选择日期">
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
      <i class="el-icon-s-data"></i>产品管理规模统计
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
        prop="VC_TYPE"
        label="基金类型"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.VC_TYPE | noDataFilter}}</span>
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
        prop="D_ESTABLISH_DATE"
        label="成立日期"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.D_ESTABLISH_DATE | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="D_JZRQ"
        label="净值日期"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.D_JZRQ | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="F_DWJZ"
        label="单位净值(元)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_DWJZ | moneyThousand}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="F_SHARE"
        label="总份额(元)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_SHARE | moneyThousand}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="F_ZCJZ"
        label="产品规模(元)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_ZCJZ | moneyThousand}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="F_TOTAL"
        label="客户数"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_TOTAL | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="F_DIRECT"
        label="直销客户数"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_DIRECT | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="F_AGENCY"
        label="代销客户数"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_AGENCY | noDataFilter}}</span>
        </template>
      </el-table-column>
      <!-- <el-table-column
        prop="VC_FREQUENCY"
        label="开放频率"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.VC_FREQUENCY | noDataFilter}}</span>
        </template>
      </el-table-column> -->
    </el-table>
     <Pagination :total="total" :page="pageNum" :limit = "pageSize" @pagination = "Pagination"></Pagination>
  </div>
</template>

<script>
 import Pagination from '@/components/Pagination'
 import commonFun from '@/filters/new_common'
 import pageApi from "@/api/reportCenter/productScaleStatistics";
 import $ from 'jquery'
export default {
    name: 'productScaleStatistics',
    components: {
      Pagination
    },
    data() {
      return {
          formInline:{
            tDate: '', //
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
     // 搜索时间默认值是今天
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

        let data = this.formInline;
        this.submitData.tDate = data.tDate; //
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
    }

   }

}
</script>

<style>
.productSearchWidth{
  width: 70% !important;
}
</style>

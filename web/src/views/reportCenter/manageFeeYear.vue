<template>
  <div>
    <div class="toolbar" >
       <el-form :inline="true" ref = "formInline" :model="formInline"  class="demo-form-inline form_inline_search" @submit.native.prevent>
          <el-row>
            <el-col :span="20">
              <div class="grid-content bg-purple">
                <el-form-item label="产品" prop="fundCode">
                    <!-- <el-select size="small"  v-model="formInline.fundCode" clearable filterable placeholder="请选择">
                        <el-option
                          v-for="item in accountCodes"
                          :key="item.value"
                          :label="item.name"
                          :value="item.value">
                        </el-option>
                    </el-select> -->
                    <select-table v-model="formInline.fundCode" @enter="onSubmit('formInline', true)"></select-table>
                </el-form-item>
                <el-form-item label="统计年份" prop="censusYear" >
                   <el-date-picker
                      v-model="formInline.censusYear"
                      type="year"
                      size="small"
                      value-format="yyyy">
                    </el-date-picker>
                </el-form-item>
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
    <i class="el-icon-s-data"></i>管理费按年份月度统计
    </div>
    <!-- sortable='custom' -->
 <el-table
      ref="multipleTable"
      @selection-change="handleSelectionChange"
      :data="tableData"
      :default-sort="{prop: 'fundcode', order: 'descending'}"
      border
      stripe
      @sort-change="handleSortChange"
      v-loading="tableLoading"
      style="width: 100%"
    >

      <el-table-column
        prop="VC_FUNDCODE"
        label="基金代码"

        :sort-orders="['ascending', 'descending']"
        min-width="90"
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

      <!-- <el-table-column
        prop="VC_SUBFUNDCODE"
        label="分级代码"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.VC_SUBFUNDCODE | noDataFilter}}</span>
        </template>
      </el-table-column> -->

      <!-- <el-table-column
        prop="VC_SUBFUNDNAME"
        label="分级名称"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.VC_SUBFUNDNAME | noDataFilter}}</span>
        </template>
      </el-table-column> -->

     

      <el-table-column
        prop="F_MFEE1"
        label="1月管理费(元)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_MFEE1 | moneyThousand}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="F_MFEE2"
        label="2月管理费(元)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_MFEE2 | moneyThousand}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="F_MFEE3"
        label="3月管理费(元)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_MFEE3 | moneyThousand}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="F_MFEE4"
        label="4月管理费(元)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_MFEE4 | moneyThousand}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="F_MFEE5"
        label="5月管理费(元)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_MFEE5 | moneyThousand}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="F_MFEE6"
        label="6月管理费(元)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_MFEE6 | moneyThousand}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="F_MFEE7"
        label="7月管理费(元)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_MFEE7 | moneyThousand}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="F_MFEE8"
        label="8月管理费(元)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_MFEE8 | moneyThousand}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="F_MFEE9"
        label="9月管理费(元)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_MFEE9 | moneyThousand}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="F_MFEE10"
        label="10月管理费(元)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_MFEE10 | moneyThousand}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="F_MFEE11"
        label="11月管理费(元)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_MFEE11 | moneyThousand}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="F_MFEE12"
        label="12月管理费(元)"
         
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.F_MFEE12 | moneyThousand}}</span>
        </template>
      </el-table-column>

    </el-table>
     <Pagination :total="total" :page="pageNum" :limit = "pageSize" @pagination = "Pagination"></Pagination>

  </div>
</template>

<script>
import selectTable from '@/views/commonComponents/selectTable.vue';
 import store from "@/store";
 import Pagination from '@/components/Pagination'
 import commonFun from '@/filters/new_common'
 import pageApi from "@/api/reportCenter/manageFeeYear";
 import pageApiFund from '@/api/xbrl/xbrl'
 import $ from 'jquery'
export default {
    name: 'manageFeeYear',
    components: {
      Pagination,
      selectTable
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
            fundCode: '', //
            productStatusDim: '', //
            censusYear: '', //
            orderString: '', //列表排序
            limit: 50,//条数
            offset:0
          },
          // searchRules: {
          //    searchDate: [{ required: true, trigger: "change", validator: validateDate }],
          // },
          total: 0, //列表条数
          pageNum:1, //页码
          pageSize: 50,//条数
accountCodes:[],//产品信息数组
          proStatusArr: [], // 产品状态数组
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

       this.selectAll(true);

this.getProductsAll();

   },
   methods: {

getProductsAll(){
        pageApiFund.getProductsAll().then(res =>{

          let self = this;
          if(res.data.message === "success"){

           let arr = res.data.data;
               this.accountCodes = [];
               for(let i=0;i<arr.length;i++){
                  let obj={};
                  obj.value=arr[i].fundCode;
                  obj.name = arr[i].fundName + ' ('+arr[i].fundCode+')';
                  this.accountCodes.push(obj);
                }
              
          }else{
             this.accountCodes = [];
             this.$message.closeAll();
            this.$message.error('初始化数据失败');
          }

        }).catch(() => {
           this.accountCodes = [];
           this.$message.closeAll();
            this.$message.error('初始化数据失败');
           
      })
    },

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
    onSubmit(formInline,flag){
        this.isSubmit = true;
        if(flag){
        this.pageNum = 1;
        this.formInline.offset = 0;
      }

        let data = this.formInline;
        this.submitData.fundCode = data.fundCode; //
        this.submitData.productStatusDim = data.productStatusDim; //
        this.submitData.censusYear = data.censusYear; //
        this.submitData.orderString = data.orderString;//列表排序
        this.submitData.limit = data.limit;//条数
        this.submitData.offset = data.offset;//分页
        this.selectAll(formInline,true);
    },
    selectAll(formInline,flag){
      this.tableLoading = true;

      let data = this.formInline;
      let data2 = this.submitData;
      let isSubmit = this.isSubmit;
      if(isSubmit){
          data = data2;
      }
      // 消除没有值的参数
       if(data.fundCode) data['fundCode'] = data.fundCode.split('_')[0]
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

   }

}
</script>

<style>
.productSearchWidth{
  width: 70% !important;
}
</style>

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
        <el-col :span="16">
          <div style="width:100%;">

             <el-form-item label="开始日期" prop="beginDate">
                <el-date-picker
                  v-model="formInline.beginDate"
                  type="date"
                  value-format="yyyy-MM-dd"
                  placeholder="选择日期">
              </el-date-picker>
            </el-form-item>

             <el-form-item label="结束日期" prop="endDate">
                <el-date-picker
                  v-model="formInline.endDate"
                  type="date"
                  value-format="yyyy-MM-dd"
                  placeholder="选择日期">
              </el-date-picker>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="8">
          <el-form-item class="search_button_com">
            <el-button type="primary" @click="onSubmit('formInline',true)"  style="margin-bottom: 5px; " size="small">
              <i class="el-icon-search"></i>查询
            </el-button>
             <!-- <el-button type="primary" plain @click="restForm('formInline')"  style="margin-bottom: 5px; " size="small">
              <i class="el-icon-delete"></i>重置
            </el-button> -->
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

   <div class="forms_table_title">
      <i class="el-icon-s-data"></i>净值查询
    </div>

    <el-table
      ref="multipleTable"
      @selection-change="handleSelectionChange"
      :data="tableData"
      :default-sort="{prop: 'PARENTFUNDNAME', order: 'descending'}"
      stripe
      @sort-change="handleSortChange"
      v-loading="tableLoading"
      style="width: 100%"
    >
      <el-table-column fixed type="selection" width="35"></el-table-column>

      <el-table-column
        prop="PARENTFUNDNAME"
        fixed
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="产品名称"
        max-width="80"
        header-align="center"
        align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.PARENTFUNDNAME | noDataFilter }}</span>
        </template>
      </el-table-column>
      
      <el-table-column
        prop="PARENTFUNDCODE"
        sortable="custom"
        show-overflow-tooltip
        :sort-orders="['ascending', 'descending']"
        label="产品代码"
        fixed
        max-width="80"
        header-align="center"
        align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.PARENTFUNDCODE | noDataFilter }}</span>
        </template>
      </el-table-column>

       <el-table-column
        prop="FUNDSTATUS"
        sortable="custom"
        show-overflow-tooltip
        :sort-orders="['ascending', 'descending']"
        label="产品状态"
        max-width="80"
        header-align="center"
        align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.FUNDSTATUS | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="FUNDNAME"
        sortable="custom"
        show-overflow-tooltip
        :sort-orders="['ascending', 'descending']"
        label="分级名称"
        max-width="80"
        header-align="center"
        align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.FUNDNAME | noDataFilter }}</span>
        </template>
       </el-table-column>
        <el-table-column
        prop="FUNDCODE"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="分级代码"
        max-width="80"
        header-align="center"
        align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.FUNDCODE | noDataFilter }}</span>
        </template>
      </el-table-column>

       <el-table-column
        prop="DDATE"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="净值日期"
        max-width="80"
        header-align="center"
        align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.DDATE | noDataFilter }}</span>
        </template>
      </el-table-column>

       <el-table-column
        prop="DWJZ"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="单位净值"
        max-width="80"
        header-align="center"
        align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.DWJZ | noDataFilter }}</span>
        </template>
      </el-table-column>

       <el-table-column
        prop="LJJZ"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="累计净值"
        max-width="80"
        header-align="center"
        align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.LJJZ | noDataFilter }}</span>
        </template>
      </el-table-column>

       <el-table-column
        prop="FQJZ"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="复权净值"
        max-width="80"
        header-align="center"
        align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.FQJZ | noDataFilter }}</span>
        </template>
      </el-table-column>

       <el-table-column
        prop="SUMSHARE"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="总份额"
        max-width="80"
        header-align="center"
        align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.SUMSHARE | noDataFilter }}</span>
        </template>
      </el-table-column>

       <el-table-column
        prop="ZCJZ"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="资产净值"
       max-width="80"
        header-align="center"
        align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.ZCJZ | noDataFilter }}</span>
        </template>
      </el-table-column>

       <el-table-column
        prop="YJBC"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="业绩报酬"
        max-width="80"
        header-align="center"
        align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.YJBC | noDataFilter }}</span>
        </template>
      </el-table-column>

       <el-table-column
        prop="LJJZRZF"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="累计净值日涨幅"
        max-width="130"
         min-width="110"
        header-align="center"
        align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.LJJZRZF | noDataFilter }}</span>
        </template>
      </el-table-column>

       <el-table-column
        prop="NHSY"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="年化收益"
        max-width="80"
        header-align="center"
        align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.NHSY | noDataFilter }}</span>
        </template>
      </el-table-column>
    
    </el-table>
     <Pagination :total="total" :page="pageNum" :limit="pageSize" @pagination="Pagination" ></Pagination>
  </div>
</template>

<script>
 import Pagination from '@/components/Pagination'
 import commonFun from '@/filters/new_common'
 import pageApi from '@/api/dataReport/index'
export default {
    name: 'jzList',
    components: {
      Pagination
    },
    data() {
      return {
           //查询表单
      formInline:{
        fundCode:'', //产品信息
        beginDate:'', //持仓日期
        endDate:'',
        parentFundCode:'',//过滤已清盘
        orderString: '"FUNDNAME" desc nulls last', //列表排序
        limit:50,
        offset:0
      },
       total: 0, //列表条数
        pageNum: 1,//页码
       pageSize: 50,//条数
       tableData:[
         {FUNDNAME:'模拟组合测试',FUNDCODE:'MN00000000254',SYMBOL:'002782',NAME:'可立克',DDATE:'2020-04-07',EXCHANGE:'深交所',TYPE:'股票',TYPELIMIT:'',CURCODE:'RMB',AMOUNT:'3500.00',COST:'1000.00',PRICE:'1200.00',GZ:'1130.00',VALPRICE:'1130.00'}
         ],//列表数据
       tableLoading:false, //列表加载
       tableMultipleSelection:[],
       countDialog: false, // 弹窗
       countTitle:"",//标题
       countFormList:"",//是新增还是编辑
       // 新增 编辑计算任务
      formCount: {
       opponentName:'',//对手方名称
       opponentType:'',//对手方类型
       fund:'',//产品
       tradeMan:'', //交易员
       lianType:'', //联系方式
       mark:'' //备注
      },
      opponentTypeArr:[{code:'001',name:'大型银行'}],//对手方类型数组
      // 操作类型 1、添加 2、编辑
      operationType: 1,
      // 弹窗验证规则
      countRules: {
        opponentName: [
          { required: true,  message: "请输入对手方名称", trigger: "bulr" }
        ],
        opponentType: [
          { required: true,  message: "请选择对手方类型", trigger: "change"}
        ]
        
      },
      formLabelWidth: "120px",
      countSubmit_btn:false //保存按钮加载
      }
    },
    //页面加载后触发
   mounted(){
   
     let query = this.$route.query;
     this.formInline.fundCode = query.fundCode;
     this.formInline.parentFundCode = query.parentFundCode;
     this.onSubmit('formInline',true);
   },
   methods: {
     //列表选择
     handleSelectionChange(val) {
      this.tableMultipleSelection = val;
    },
    //排序
    handleSortChange(val) {
      this.formInline.orderString = commonFun.orderByString(val);
      this.onSubmit("formInline", false);
    },
    //分页
    Pagination(val) {
      this.pageSize = val.limit; //页面条数
      this.pageNum = val.page; //页面
       this.formInline.offset = (val.page -1) * val.limit;
      this.formInline.limit = val.limit; //页面条数
      this.onSubmit("formInline", false);
    },
     onSubmit(formName,flag){
       this.tableLoading = true;
        
        let params = commonFun.parameterSrc(this.formInline);
        if(flag){
          this.pageNum = 1;
          this.formInline.offset = 0;
          params.offset = 0;
        }
        params.pageable = true;
        params.generalName = 'product.queryData.hisValuation';
        pageApi.getDataSourceList(params).then(response => {
        
        if(response.data.status === 200){
          this.tableData = response.data.rows;
          // 页面总条数
          this.total = response.data.total;
        }
        else{
          this.tableData = [];
          this.total = 0;
          this.formInline.pageSize = 50;
          this.pageNum = 1;
          this.formInline.offset = 0;

        }
        this.tableLoading = false;

      }).catch(() => {
        this.tableData = [];
        this.total = 0;
        this.formInline.pageSize = 50;
        this.pageNum = 1;
        this.formInline.offset = 0;
        this.tableLoading = false;
      })
     },
     restForm(formName){
         this.formInline.fundCode = ''; //产品信息
        this.formInline.beginDate = ''; //持仓日期
     },
     addData(){
         this.countTitle = "新增";
        this.countFormList = "add";
        this.countDialog = true;
        this.operationType =1;

        // 清除
        this.$nextTick(() => {
          this.$refs["formCount"].resetFields();
          this.formCount.opponentName = ""; //对手方名称
          this.formCount.opponentType = '';//对手方类型
          this.formCount.fund = "";//产品
          this.formCount.tradeMan = "";//交易员
          this.formCount.lianType = "";//联系方式
          this.formCount.mark = '';//备注
        });
     },
     countSubmit(formName){
        var self = this;
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.$message.closeAll()
             this.$message({
              message: '新增成功',
              type: 'success'
            });
             this.countDialog = false;
            return;
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
     }

   }

}
</script>
<style>
.jydsListWidth{
  width: 55% !important;
}
</style>

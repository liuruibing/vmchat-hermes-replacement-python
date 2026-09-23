<template>
  <div>
      <div class="toolbar" >
     <el-form :inline="true" :rules="commonRules" ref = "formInline" :model="formInline"  class="demo-form-inline form_inline_search" >
          <el-row>
            <el-col :span="16">
              <div class="grid-content bg-purple">
               <el-form-item label="产品代码" prop="fundCode">
                  <el-input
                    v-model="formInline.fundCode"
                    placeholder="产品代码"
                    type="text"
                    maxlength="8"
                    auto-complete="off"
                    @keydown.enter.native="onSubmit('formInline')"
                    clearable
                    size="small"/>
                </el-form-item>

               <el-form-item label="产品名称" prop="fundName">
                  <el-input
                    v-model="formInline.fundName"
                    placeholder="产品名称"
                    type="text"
                    maxlength="20"
                    auto-complete="off"
                    @keydown.enter.native="onSubmit('formInline')"
                    clearable
                    size="small"/>
                    <!-- <select-table v-model="formInline.fundName"></select-table> -->
                </el-form-item>

                 <el-form-item label="审核状态" prop="approveStatus">
                 <el-select clearable  v-model="formInline.approveStatus"  size="small"  placeholder="请选择"  >
                    <el-option
                      v-for="(group, index) in approveStatusArr"
                      :value="group.code"
                      :key="index"
                      :label="group.name">
                    </el-option>
                  </el-select>
                </el-form-item>

              </div>

            </el-col>
            <el-col :span="8">
              <div class="grid-content bg-purple-light">
                <el-form-item  class="search_button_com">
                  <el-button :loading='countSubmit_btn' type="primary" @click="onSubmit('formInline')" style="margin-bottom: 5px;" size="small"><i class="el-icon-search"></i>查询</el-button>
                  <el-button :loading='countSubmit_btn' type="primary" plain size="small" style="margin-bottom: 5px;" @click="restForm('formInline')"><i class='el-icon-delete'></i>重置</el-button>
                </el-form-item>
              </div>
            </el-col>
          </el-row>
        </el-form>
  </div>
 <div class="forms_table_title">
      <i class="el-icon-s-data"></i>产品审核列表
    </div>
 <el-table
      ref="multipleTable"
      @selection-change="handleSelectionChange"
      :data="tableData"
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
        prop="fundCode"
        label="产品代码"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        min-width="90"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.fundCode | noDataFilter}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fundName"
        label="产品名称"
        sortable="custom"
        :show-overflow-tooltip="true"
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.fundName | noDataFilter}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="approveType"
        label="操作类型"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
           <span v-if="scope.row.approveType === '1'">新增</span>
           <span v-else-if="scope.row.approveType === '2'">修改</span>
           <span v-else>{{scope.row.approveType | noDataFilter}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="creator "
        label="经办人"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.creator  | noDataFilter}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="modifier "
        label="审核人"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.modifier  | noDataFilter}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="approveStatus"
        label="审核状态"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
           <span v-if="scope.row.approveStatus === '-1'">待审核</span>
           <span v-else-if="scope.row.approveStatus === '0'">审核不通过</span>
            <span v-else-if="scope.row.approveStatus === '1'">审核通过</span>
           <span v-else>{{scope.row.approveStatus | noDataFilter}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="approveBeginTime "
        label="提交审核时间"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.approveBeginTime  | noDataFilter}}</span>
        </template>
      </el-table-column>

      <el-table-column
          label="操作"
          min-width = "120"
          fixed="right"
          align="center">
          <template slot-scope="scope">
            <el-button :loading='countSubmit_btn' type="primary" size="small" @click="serachDetails(scope.row)">查看详情</el-button>
            <el-button v-btn="'fund.approve.info'" :loading='countSubmit_btn' v-if="scope.row.approveStatus === '-1'" type="primary" size="small" @click="serachDetail(scope.row)">审核</el-button>
          </template>
      </el-table-column>
    </el-table>
     <Pagination :total="total" :page="pageNum" :limit = "pageSize" @pagination = "Pagination"></Pagination>


     <!-- 新增代办 -->
    <el-dialog :title="countTitle" :before-close="handleClose" customClass="productSearchWidth"   center :visible.sync="countDialog" :close-on-click-modal="false">
        <productDetailPage v-if="productDetailPage_show" :PageDataDetail = "PageDataDetail" @pageCheckClick = "pageCheckClick"></productDetailPage>
    </el-dialog>
    <!-- 新的查看详情 -->
    <view-info v-if="bassInfoSHow" ref='bassInofRelation' @closed='bassInfoSHow = false' @rushDataList='selectAll(true)'></view-info>
  </div>
</template>

<script>
import selectTable from '@/views/commonComponents/selectTable.vue';
// bass-info
import ViewInfo from './editAndSearchFile/main-box'
 import Pagination from '@/components/Pagination'
import commonFun from '@/filters/new_common'
import pageApi from "@/api/product/productExamine";
 import productDetailPage from './productDetail.vue'
export default {
    name: 'productSearch',
    inject:['reload'],
    components: {
      Pagination,
      productDetailPage,
      ViewInfo,
      selectTable
    },
    watch: {
      "$route.path"(val, oldVal) {
        // 如果是当前页面路由
        if (val === "/product/approve") {
          // console.log(val);
          this.reload();
        } else {
        }
      },
    },
    data() {
      return {
        bassInfoSHow: false,
          formInline:{
            fundCode:'',//产品代码
            fundName:'',//产品名称
            approveStatus:'-1',
            orderString: '', //列表排序
            limit: 50,//条数
            offset:0
          },
          total: 0, //列表条数
          pageNum:1, //页码
          pageSize: 50,//条数
          tableData:[{fundCode:'001'}],//列表数据
          tableLoading:false, //列表加载
          tableMultipleSelection:[],
          countDialog: false, // 弹窗
          countTitle:"",//标题
          productDetailPage_show:false,
          submitData:{},
          PageDataDetail:{
            sh_show:true,
            fundCode:'', //查看详情
            id:'', //审核详情
            detailType: 1 //0查看详情，1审核详情
          },
          approveStatusArr:[
              {code:'-1',name:'待审核'},
               {code:'0',name:'审核不通过'},
                {code:'1',name:'审核通过'}

          ],
	// 表单校验规则
      commonRules: {
	    //必填信息校验
        fundName: [
          // { required: false,pattern: /^[a-zA-Za-z0-9\u4e00-\u9fa5]+$/,  message: "请输入中文、字母、数字", trigger: "change"}
        ],
        fundCode: [
          // {required: false, pattern: /^[A-Z0-9]+$/, message: '请输入大写字母、数字',trigger: 'change'}
        ],
      },
          countSubmit_btn:false
      }
    },
    //页面加载后触发
   mounted(){
     this.selectAll(true);
   },
   methods: {
      //列表选择
     handleSelectionChange(val) {
      this.tableMultipleSelection = val;
    },
    //排序
    handleSortChange(val) {
      this.isSubmit = false
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
     pageCheckClick(data){
       if(data.flag){
            this.countDialog = false; // 弹窗
            this.productDetailPage_show = false;
            this.PageDataDetail.id = '';
            this.selectAll(true);
       }
     },
       //查看详情
     serachDetails(row){
        // if(row.fundCode){
        //      this.PageDataDetail.id = row.id;
        //     this.countDialog = true; // 弹窗
        //     this.countTitle = '查看详情';//标题
        //     this.PageDataDetail.detailType = 2;
        //     this.PageDataDetail.sh_show = false;
        //     this.productAddPage_show = false;
        //     this.productAddNewPage_show =false;
        //     this.productDetailPage_show = true;
            
        // }else{
        //   this.$message.closeAll();
        //   this.$message({type: 'error',message: '产品代码为空'});
        // }
        // 以上老方法---------------
        this.bassInfoSHow = true
        this.$nextTick(() => {
          this.$refs.bassInofRelation.init(row, false)
        })
     },
     serachDetail(row){
      //  if(row.id){
      //     this.PageDataDetail.id = row.id;
      //      this.PageDataDetail.detailType = 1;
      //      this.PageDataDetail.sh_show = true;
      //     this.countDialog = true; // 弹窗
      //     this.countTitle = '审核';//标题
      //     this.productDetailPage_show = true;
         
      //   }else{
      //     this.$message.closeAll();
      //     this.$message({type: 'error',message: 'id为空'});
      //   }
      this.bassInfoSHow = true
        this.$nextTick(() => {
          this.$refs.bassInofRelation.init(row, false, 'judge')
      })
     },
     handleClose(done) {
          done();
            this.productDetailPage_show = false;
      },
       //查询
    onSubmit(flag){
        this.isSubmit = true;
        if(flag){
        this.pageNum = 1;
        this.formInline.offset = 0;
      }
        let data = this.formInline;
        this.submitData.fundCode = data.fundCode; //产品代码
        this.submitData.fundName = data.fundName; //产品名称
         this.submitData.approveStatus = data.approveStatus; //产品名称
        this.submitData.orderString = data.orderString;//列表排序
        this.submitData.limit = data.limit;//条数
        this.submitData.offset = data.offset;//分页
        this.selectAll(true);
    },
    selectAll(flag){
	
	   var continueFlag=false;
	   this.$refs['formInline'].validate((valid) => {
			 if (valid) {
				continueFlag=true;
				return true;
			 }
		});
		if(!continueFlag){
			this.$message.closeAll();
			this.$message({
				message: '请完善输入信息',
				type: 'error'
			});
          return;
		}
	
	
	
      this.tableLoading = true;
      this.countSubmit_btn = true;
      let data = this.formInline
      let data2 = this.submitData;
      let isSubmit = this.isSubmit;
      if(isSubmit){
          data = data2;
      }
      // 消除没有值的参数
      // console.log('data', data)
      // if (data.fundName) {
      //   data.fundCode = data.fundName.split('_')[0]
      //   data.fundName = ''
      //   // data.fundName = data.fundName.split('_')[1]
      // }
      let params = commonFun.parameterSrc(data);
      if(flag){
        this.pageNum = 1;
        this.formInline.offset = 0;
        params.offset = 0;
      }
      pageApi.getDataSourceList(params).then(response => {
        if(response.data.status === 200){
          this.tableData = response.data.data.rows;
          // 页面总条数
          this.total = response.data.data.total;
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
         this.countSubmit_btn = false;

      }).catch(() => {
        this.tableData = [];
        this.total = 0;
        this.formInline.limit = 50;
        this.pageSize = 50;
        this.pageNum = 1;
        this.formInline.offset = 0;
        this.tableLoading = false;
        this.countSubmit_btn = false;

      })
    }

   }

}
</script>

<style lang='scss'>
.productSearchWidth{
  width: 70% !important;
  .el-form{
     width: 100%!important;
  }
}
</style>
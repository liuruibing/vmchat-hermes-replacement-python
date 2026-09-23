<template>
   <div>
    <el-dialog :title="dialogTitle" :before-close="handleClose" customClass="xbrlCzrzListWidth"   center :visible.sync="czrzDialog" :close-on-click-modal="false">
      <el-container >
        <el-main class="mainBox">
           <annExcelPage v-if="annExcelPage_show" :PageData="PageData"></annExcelPage>
           <annXmlPage v-if="annXmlPage_show" :PageData="PageData"></annXmlPage>
           <annTxtPage v-if="annTxtPage_show" :PageData="PageData"></annTxtPage>
           <annLogPage v-if="annLogPage_show" :PageData="PageData"></annLogPage>

           <currencyReportPage v-if="currencyReportPage_show" :currencyReportPageData="currencyReportPageData"></currencyReportPage>
        </el-main>
      </el-container>
    </el-dialog>

     <!-- 复核确认 -->
    <el-dialog title="复核确认" customClass="qrfuListWidth"   center :visible.sync="countDialog" :close-on-click-modal="false">
      <el-container >
        <el-main class="mainBox">
          <el-form
            :inline="true"
            ref="formCount"
            :model="formCount"
            :rules="countRules"
            label-position="right"
          >
            <el-form-item  label="复核确认意见"  prop="confirmOpinion" >
               <el-input
                  v-model="formCount.confirmOpinion"
                  type="textarea"
                  auto-complete="off"
				  maxlength='1000'
				  show-word-limit
				  :autosize='{minRows: 2}'
                  placeholder="请输入"
                />
            </el-form-item>

          </el-form>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="countDialog = false">取 消</el-button>
        <el-button  type="primary" size="small"  @click="countSubmit('formCount')">确 定</el-button>
      </div>
    </el-dialog>
	
	<!-- 取消复核 -->
    <el-dialog title="复核确认" customClass="qrfuListWidth"   center :visible.sync="reportConfirmCancelDialog" :close-on-click-modal="false">
      <el-container >
        <el-main class="mainBox">
          <el-form
            :inline="true"
            ref="formCount"
            :model="formCount"
            :rules="countRules"
            label-position="right"
          >
            <el-form-item  label="取消复核说明"  prop="confirmCancelOpinion">
               <el-input
                  v-model="formCount.confirmCancelOpinion"
                  type="textarea"
                  auto-complete="off"
				  maxlength='1000'
				  show-word-limit
				  :autosize='{minRows: 2}'
                  placeholder="请输入"
                />
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="reportConfirmCancelDialog = false">取 消</el-button>
        <el-button  type="primary" size="small"  @click="reportConfirmCancelSubmit('formCount')">确 定</el-button>
      </div>
    </el-dialog>
	
	
	
    <!-- 新更改pageView -->
    <currency-report-page-new v-if="currenc_new_show" ref="currenc_new_ref" @currencBtn='currencValue'></currency-report-page-new>
   </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import commonFun from '@/filters/new_common'
import pageApi from '@/api/xbrl/xbrl'
import store from "@/store";
import annExcelPage from './annExcel.vue'
import annXmlPage from './annXml.vue'
import annTxtPage from './annTxt.vue'
import annLogPage from './annLog.vue'
import currencyReportPage from '@/views/dataReport/currencyReport'
// 新更改pageView
import CurrencyReportPageNew from './currencyReport/currencyReoportTree'
export default {
   name:'xbrlDialog',
    components: {
    Pagination,
    annExcelPage,
    annXmlPage,
    annTxtPage,
    annLogPage,
    currencyReportPage,
    CurrencyReportPageNew
  },
   data () {
      return {
        currenc_new_show: false,
          activeName:'All',
          activeName2:'fourth',
          accountCodes:[],//产品信息数组
          proStatusArr:[],//负责经办数组
          name2Arr:[
             { name: '未核对', code: '0' },
              { name: '核对一致', code: '1' },
              { name: '核对不一致', code: '2' }
              
          ],//核对状态
          name3Arr:[
             { name: '未校验', code: '0' },
              { name: '校验成功', code: '1' },
              { name: '校验失败', code: '2' }
          ],//勾稽校验
          name5Arr:[
             { name: 'XBRL', code: 'XBRL' },
              { name: 'CISP', code: 'CISP' },
              { name: '人行', code: 'RH' },
               { name: '中基协', code: 'ZJX' }
          ],//产品状态数组
          name6Arr:[],//信批岗确认数组
          formInline:{
            reportType:'',//报告类型
            fundCode:'',//产品信息
            fundState:'',//产品状态
            statusDataValid:'',//勾稽校验
            statusFileVerify:'',//核对状态
            dateData:'',
            pageSize:10,
            pageNum:1,
            orderString:'',
            reportFrequency:'',
            statusReport:''
          },
         
          total:0,
          tableData:[
           // {fundCode:'LBM001',fundName:'路博迈1号',fundType:'公募',name:'产品基本信息',name1:'已清盘',name2:'',name3:'无异常',name4:'未复核',name5:'',name6:'已上报',name7:'2020-07-02',name8:'2020-07-07'},
           // {fundCode:'LBM002',fundName:'路博迈2号',fundType:'公募',name:'产品基本信息',name1:'运作期',name2:'',name3:'未校验',name4:'未生成',name5:'',name6:'未上报',name7:'2020-07-02',name8:'2020-07-07'},
          ],//列表数据
          tableLoading:false, //列表加载
          tableMultipleSelection:[],
          reportTypeArr:[
              { name: '年报', value: 'Y' },
              { name: '半年报', value: 'S' },
              { name: '季报', value: 'Q' },
              { name: '月报', value: 'M' },
              { name: '月报', value: 'W' },
              { name: '日报', value: 'D' }
          ],//报表类型数组
        quarters: [
        { name: '一季度', value: '1' },
        { name: '二季度', value: '2' },
        { name: '三季度', value: '3' },
        { name: '四季度', value: '4' }
        ],
      months: [
        { name: '一月', value: '1' },
        { name: '二月', value: '2' },
        { name: '三月', value: '3' },
        { name: '四月', value: '4' },
        { name: '五月', value: '5' },
        { name: '六月', value: '6' },
        { name: '七月', value: '7' },
        { name: '八月', value: '8' },
        { name: '九月', value: '9' },
        { name: '十月', value: '10' },
        { name: '十一月', value: '11' },
        { name: '十二月', value: '12' }
      ],
       reportTypeArr2:[],
       reportTypeOther_year:false,
       reportTypeOther_show:false,
       reportTypeOther_day:true,
       reportTypeOther_weak:false,
       yjsc_btn_show:true, //一键生成
       gjjy_btn_show:true, //勾稽校验
       ywbhd_btn_show:true, //与外包核对
       qrfh_btn_show:true, //确认复核
       yjsb_btn_show:true, //一键上报
       czrzDialog:false,
       czrzTableData:[], //操作日志列表
       czrzTableLoading:false,//操作日志列表加载
       czrzTotal:0, //操作日志列表总数
       czrzPageNum:1, //操作日志列表页码
       czrzPageSize:10, //操作日志列表条数
       offsetSpan:16,
       spanSize:8,
       fundStatusArr:{},
       weekDate:[],
       selectDate:'',
       reportYear:'',
       czrzOrderString:'',
       PageData:{
         recordId:''
       },
       currencyReportPageData:{},
       annExcelPage_show:false,
       annXmlPage_show:false,
       annTxtPage_show:false,
       annLogPage_show:false,
       currencyReportPage_show:false,
       dialogTitle:'',
       countDialog:false,
	   reportConfirmCancelDialog:false,
	   reportRecordId:'',
       formCount:{
         confirmOpinion:'',
		 confirmCancelOpinion:''
       },
       countRules: {
        confirmOpinion:  { required: true, type: 'string', message: "请输入复核确认意见", trigger: "blur" },
		confirmCancelOpinion:  { required: true, message: "请输入取消复核说明", trigger: "change" }
      },
      formLabelWidth: "120px",
      fundColumnShowFlag:true


      };
   },


   mounted() {
    //  this.getSelects('fundinfo_fundState');
    //  this.getProductsAll();
    //  this.onSubmit(true);
   },

   methods: {
     changeReportType(){
		var curValue=this.formInline.reportType||'';
	    if( curValue=='' ||curValue=='XBRL'){
		   this.fundColumnShowFlag=true;   
		}else{
		   this.fundColumnShowFlag=false;   
		}
	 },
     
   
     handleClick(tab, event){
         let tabLabel = tab.label;
         this.reportTypeChange(this.activeName);
         this.formInline.dateData = '';
         this.formInline.reportFrequency  = this.activeName
         if(this.activeName ==='All'){
              this.formInline.reportFrequency  = '';
          }
         this.onSubmit(true);
     },
     handleClick2(tab, event){
         let tabLabel = tab.label;
         this.formInline.dateData = '';
         if(tabLabel === '全部'){
             this.yjsc_btn_show  = true; //一键生成
             this.gjjy_btn_show = true; //勾稽校验
             this.ywbhd_btn_show = true; //与外包核对
             this.qrfh_btn_show = true; //确认复核
             this.yjsb_btn_show = true; //一键上报
             this.offsetSpan = 16;
             this.spanSize = 8;
            
         }else if(tabLabel === '待生成'){
             this.yjsc_btn_show  = true; //一键生成
             this.gjjy_btn_show = false; //勾稽校验
             this.ywbhd_btn_show = false; //与外包核对
             this.qrfh_btn_show = false; //确认复核
             this.yjsb_btn_show = false; //一键上报
             this.offsetSpan = 18;
             this.spanSize = 6;
         }else if(tabLabel === '复核'){
             this.yjsc_btn_show  = false; //一键生成
             this.gjjy_btn_show = true; //勾稽校验
             this.ywbhd_btn_show = true; //与外包核对
             this.qrfh_btn_show = true; //确认复核
             this.yjsb_btn_show = false; //一键上报
             this.offsetSpan = 21;
             this.spanSize = 3;

         }else if(tabLabel === '待报送'){
             this.yjsc_btn_show  = false; //一键生成
             this.gjjy_btn_show = false; //勾稽校验
             this.ywbhd_btn_show = false; //与外包核对
             this.qrfh_btn_show = false; //确认复核
             this.yjsb_btn_show = true; //一键上报
             this.offsetSpan = 21;
             this.spanSize = 3;

         }else if(tabLabel === '已完成'){
             this.yjsc_btn_show  = false; //一键生成
             this.gjjy_btn_show = false; //勾稽校验
             this.ywbhd_btn_show = false; //与外包核对
             this.qrfh_btn_show = false; //确认复核
             this.yjsb_btn_show = false; //一键上报
             this.offsetSpan = 22;
             this.spanSize = 2;
         }

        if(tabLabel === '全部'){
           this.formInline.statusReport  = '';
        }else{
            this.formInline.statusReport  = this.activeName2
        }
		
		this.changeReportType();
		
         this.onSubmit(true);
     },
      //列表选择
    handleSelectionChange(val) {
      this.tableMultipleSelection = val;
      
    },
    //排序
    handleSortChange(val) {
      this.formInline.orderString = commonFun.orderByString(val);
    
     this.onSubmit(false);
    },
    czrzSortChange(val) {
      this.czrzOrderString = commonFun.orderByString(val);
    
     this.onSubmitCzrz(false);
    },
    //分页
    Pagination(val) {
      this.formInline.pageSize = val.limit; //页面条数
      this.formInline.pageNum = val.page;//页码
      this.onSubmit(false);
    },
    czrzPagination(val) {
      this.czrzPageSize = val.limit; //页面条数
      this.czrzPageNum = val.page;//页码
      this.onSubmitCzrz(false);
     
    },
    //查询
    onSubmit(flag){
      
       this.tableLoading = true;
         // 消除没有值的参数
         if(flag){
             this.formInline.pageNum = 1;
         }
         if(!this.initDate()){
            this.tableLoading = false;
            return;
         }
         let params = commonFun.parameterSrc(this.formInline);
         pageApi.getAnnDataSourceList(params).then(response => { 
            if(response.data.status === 200){ 
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
    initDate(){
      let flag = this.activeName;
      if(flag === 'W'){
        if(this.formInline.dateData){
              let myDate = new Date(this.formInline.dateData); 
              let weekDay = ["星期天", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"];
              let value = weekDay[myDate.getDay()];
              if(value != '星期五'){
                   this.$message.closeAll()
                    this.$message({
                      message: '请选择星期五的日期',
                      type: 'warning'
                      });
                  return false;
              }
        }

      }else if(flag === 'M'){
          if(this.reportYear && !this.selectDate){
               this.$message.closeAll()
               this.$message({
                message: '请选择对应的月份',
                type: 'warning'
                });
              return false;
          }else if(!this.reportYear && this.selectDate){
               this.$message.closeAll()
               this.$message({
                message: '请选择对应的年份',
                type: 'warning'
                });
              return false;
          }else if(this.reportYear && this.selectDate){
              this.initMonthDate(this.reportYear,this.selectDate);
          }
      }else if(flag === 'Q'){
          if(this.reportYear && !this.selectDate){
              this.$message.closeAll()
               this.$message({
                message: '请选择对应的季度',
                type: 'warning'
                });
              return false;
          }else if(!this.reportYear && this.selectDate){
              this.$message.closeAll()
               this.$message({
                message: '请选择对应的年份',
                type: 'warning'
                });
              return false;
          }else if(this.reportYear && this.selectDate){
              let q = this.selectDate
              let date = this.reportYear;
              if(q === '1'){
                  date = date +'-03-31';
              }else if(q === '2'){
                  date = date +'-06-30';
              }else if(q === '3'){
                  date = date +'-09-30';
              }else if(q === '4'){
                  date = date +'-12-31';
              }
              this.formInline.dateData = date;
          }
      }else if(flag === 'S'){
          if(this.reportYear){
              this.formInline.dateData = this.reportYear +'-06-30';
          }
      }else if(flag === 'Y'){
          if(this.reportYear){
              this.formInline.dateData = this.reportYear +'-12-31';
          }
      }

      return true;
      
    },
    initMonthDate(year,m){
        let date = year;
        if(m === '1'){
            date = data +'-01-31';
        }else if(m === '2'){
            date = date +'-03-01'
            let myDate = new Date(date);
            var time= myDate.getTime()-24*60*60*1000;
            var yesterday = new Date(time);
            var month= yesterday.getMonth();
            var day=yesterday.getDate();
            date = year+'-02-'+day;
           // console.log(day);
        }else if(m === '3'){
            date = date +'-03-31';
        }else if(m === '4'){
            date = date +'-04-30';
        }else if(m === '5'){
            date = date +'-05-31';
        }else if(m === '6'){
            date = date +'-06-30';
        }else if(m === '7'){
            date = date +'-07-31';
        }else if(m === '8'){
            date = date +'-08-31';
        }else if(m === '9'){
            date = date +'-09-30';
        }else if(m === '10'){
            date = date +'-10-31';
        }else if(m === '11'){
            date = date +'-11-30';
        }else if(m === '12'){
            date = date +'-12-31';
        }
        this.formInline.dateData = date;
    },
    //编辑
    editData(row){
      if(row.dateData){
          this.currencyReportPageData.dataDate = row.dateData;
		  this.currencyReportPageData.endDate = row.dateData;
      }
      if(row.reportId){
          this.currencyReportPageData.reportCode = row.reportId;
      }
	   if(row.id){
          this.currencyReportPageData.recordId = row.id;
      }

       if(row.agencyCode){
          this.currencyReportPageData.agencyCode = row.agencyCode;
      }


       if(row.fileDate){
          this.currencyReportPageData.fileDate = row.fileDate;
      }
        this.annExcelPage_show = false;
        this.annXmlPage_show = false;
        this.annTxtPage_show = false;
        this.annLogPage_show = false;
        this.currencyReportPage_show = true;
        this.czrzDialog = true;
        this.dialogTitle = row.reportName;
      //  新更改---
      // this.currenc_new_show = true
      // this.$nextTick(() => {
      //   this.$refs.currenc_new_ref.init(row)
      // })
    },
    // 值返回
    currencValue (data) {
      console.log('返回值', data)
      this.currenc_new_show = false
    },
    //一键生成
    yjsc(){
        if(this.tableMultipleSelection.length === 0){
             this.$message.closeAll()
             this.$message({
                message: '请选择要生成的数据',
                type: 'warning'
             });
             return;
        }

        let arr = this.tableMultipleSelection;
        let formData = new FormData();  //  用FormData存放上传文件
        for(let i=0;i<arr.length;i++){
             formData.append('ids',  arr[i].id);
        }
        

        //params.models = arr;
         pageApi.yjscData(formData).then(response => {
            if(response.data.status === 200){
                this.$message.closeAll()
                this.$message({
                    message: '操作成功',
                    type: 'success'
                 });
                 // 刷新树列表
                 this.onSubmit(false);
            }
           else{
               this.$message.closeAll()
               this.$message({
                  message: response.data.message || '操作失败',
                  type: 'warning'
               });
           }
         }).catch(() => {
         // 关闭移动指标弹框
             this.$message.closeAll()
             this.$message({
                message: '操作失败',
                type: 'warning'
             });
         })
         
    },
    //勾稽校验
    gjjy(){
      if(this.tableMultipleSelection.length === 0){
             this.$message.closeAll()
             this.$message({
                message: '请选择要生成的数据',
                type: 'warning'
             });
             return;
        }

        let arr = this.tableMultipleSelection;
        let formData = new FormData();  //  用FormData存放上传文件
        for(let i=0;i<arr.length;i++){
             formData.append('ids',  arr[i].id);
        }
        
        //params.models = arr;
         pageApi.gjjyData(formData).then(response => {
            if(response.data.status === 200){
                this.$message.closeAll()
                this.$message({
                    message: '操作成功',
                    type: 'success'
                 });
                 // 刷新树列表
                 this.onSubmit(false);
            }
           else{
               this.$message.closeAll()
               this.$message({
                  message: response.data.message || '操作失败',
                  type: 'warning'
               });
           }
         }).catch(() => {
         // 关闭移动指标弹框
             this.$message.closeAll()
             this.$message({
                message: '操作失败',
                type: 'warning'
             });
         })

    },
    //与外包核对
    ywbhd(){

        if(this.tableMultipleSelection.length === 0){
             this.$message.closeAll()
             this.$message({
                message: '请选择要生成的数据',
                type: 'warning'
             });
             return;
        }

        let arr = this.tableMultipleSelection;
        let formData = new FormData();  //  用FormData存放上传文件
        for(let i=0;i<arr.length;i++){
             formData.append('ids',  arr[i].id);
        }
        //params.models = arr;
         pageApi.ywbhdData(formData).then(response => {
            if(response.data.status === 200){
                this.$message.closeAll()
                this.$message({
                    message: '操作成功',
                    type: 'success'
                 });
                 // 刷新树列表
                 this.onSubmit(false);
            }
           else{
               this.$message.closeAll()
               this.$message({
                  message: response.data.message || '操作失败',
                  type: 'warning'
               });
           }
         }).catch(() => {
         // 关闭移动指标弹框
             this.$message.closeAll()
             this.$message({
                message: '操作失败',
                type: 'warning'
             });
         })

    },
    //确认复核
    qrfh(){
      if(this.tableMultipleSelection.length === 0){
             this.$message.closeAll()
             this.$message({
                message: '请选择要复核的数据',
                type: 'warning'
             });
             return;
        }

        this.countDialog = true;
        this.formCount.confirmOpinion = '';
    },
	reportConfirmCancel(row){
		this.reportRecordId=row.id;
        this.reportConfirmCancelDialog = true;
        this.formCount.confirmCancelOpinion = '';
    },
    countSubmit(formName){

      var self = this;
        this.$refs[formName].validate((valid) => {
          if (valid) {
             
          let arr = this.tableMultipleSelection;
          let formData = new FormData();  //  用FormData存放上传文件
          for(let i=0;i<arr.length;i++){
              formData.append('ids',  arr[i].id);
          }
          formData.append('confirmOpinion',  this.formCount.confirmOpinion);
        //params.models = arr;
         pageApi.qrfhData(formData).then(response => {
            if(response.data.status === 200){
                this.$message.closeAll()
                this.$message({
                    message: '操作成功',
                    type: 'success'
                 });
                 this.countDialog = false;
                 // 刷新树列表
                 this.onSubmit(false);
                
            }
           else{
               this.$message.closeAll()
               this.$message({
                  message: response.data.message || '操作失败',
                  type: 'warning'
               });
           }
         }).catch(() => {
         // 关闭移动指标弹框
             this.$message.closeAll()
             this.$message({
                message: '操作失败',
                type: 'warning'
             });
         })
          } else {
            return false;
          }
        }) 
    },
	
	reportConfirmCancelSubmit(formName){

      var self = this;
	  let formData = new FormData();
	  
        this.$refs[formName].validate((valid) => {
          if (valid) {
			  formData.append('ids',  this.reportRecordId);
			  formData.append('confirmOpinion',  this.formCount.confirmCancelOpinion);
			  
			 pageApi.reportConfirmCancelData(formData).then(response => {
			 
				if(response.data.status === 200){
					this.$message.closeAll()
					this.$message({
						message: '操作成功',
						type: 'success'
					 });
					 this.reportConfirmCancelDialog = false;
					 // 刷新树列表
					 this.onSubmit(false);
				}
			   else{
				   this.$message.closeAll()
				   this.$message({
					  message: response.data.message || '操作失败',
					  type: 'warning'
				   });
			   }
         }).catch(() => {
			// 关闭移动指标弹框
			 this.$message.closeAll()
			 this.$message({
				message: '操作失败',
				type: 'warning'
			 });
         })
          } else {
            return false;
          }
        }) 
    },
    //一键上报
    yjsb(){
	
		if(this.tableMultipleSelection.length === 0){
             this.$message.closeAll()
             this.$message({
                message: '请选择要生成的数据',
                type: 'warning'
             });
             return;
        }

        let arr = this.tableMultipleSelection;
        
         let formData = new FormData();  //  用FormData存放上传文件
        for(let i=0;i<arr.length;i++){
             formData.append('ids',  arr[i].id);
        }
        //params.models = arr;
         pageApi.yjsbData(formData).then(response => {
            if(response.data.status === 200){
                this.$message.closeAll()
                this.$message({
                    message: '操作成功',
                    type: 'success'
                 });
                 // 刷新树列表
                 this.onSubmit(false);
            }
           else{
               this.$message.closeAll()
               this.$message({
                  message: response.data.message || '操作失败',
                  type: 'warning'
               });
           }
         }).catch(() => {
         // 关闭移动指标弹框
             this.$message.closeAll()
             this.$message({
                message: '操作失败',
                type: 'warning'
             });
         })

    },
    //下载报表
    downloadReport(){
        let arr = this.tableMultipleSelection;
        
         let params = {ids:[],token:this.$store.getters.token};  //  token
        for(let i=0;i<arr.length;i++){
			 params['ids'].push(arr[i].id);
        }
		
		
        //    // 表头名
        // params["exportAliasName"] = '年份,组合代码,报告类型,父标签名称,标签名称,标签值,导入时间';
        // // 导出文件名
        // params["exportFileName"] = 'XBRL.xls';
        // // 数据格式化
        // params["exportFormat"] = 'string,string,string,string,string,string,string';
        // // 表头属性名
        // params["exportPoName"] = 'rptYear,combinedId,rptType,parentElementName,elementName,elementValue,importDate';
        // // 表标题
        // params["exportTitle"] = 'XBRL导出数据';
        // 请求地址
        let action = store.state.setting.baseApi + 'api/annreport/v1.0/download';

        commonFun.formDownloadFile(params,action,"POST");

    },
    //核对明细
    hdmx(row){
      this.PageData.recordId = row.id;
     
      let reportFileType = row.reportFileType
      if(reportFileType){
        if(reportFileType==='EXCEL'){
              this.annExcelPage_show = true;
              this.annXmlPage_show = false;
              this.annTxtPage_show = false;
              this.annLogPage_show = false;
               this.currencyReportPage_show = false;
              
              this.dialogTitle = 'Excel核对页面'
        }else if(reportFileType==='XML'){
              this.annExcelPage_show = false;
              this.annXmlPage_show = true;
              this.annTxtPage_show = false;
              this.annLogPage_show = false;
              this.currencyReportPage_show = false;
              this.dialogTitle = 'XML核对页面'
        }else if(reportFileType==='TXT'){
              this.annExcelPage_show = false;
              this.annXmlPage_show = false;
              this.annTxtPage_show = true;
              this.annLogPage_show = false;
              this.currencyReportPage_show = false;
              this.dialogTitle = 'TXT核对页面'
        }
         this.czrzDialog = true;
         this.dialogTitle = row.reportName;
      }
     
    },
    //操作日志
    czrz(row){
      this.PageData.recordId = row.id;
      this.czrzDialog = true;
      this.dialogTitle = '操作日志'
      this.annExcelPage_show = false;
      this.annXmlPage_show = false;
      this.annTxtPage_show = false;
      this.annLogPage_show = true;
      this.currencyReportPage_show = false;
        
     
      //this.onSubmitCzrz();
    },
    onSubmitCzrz(flag){
        this.czrzTableLoading = true;
         // 消除没有值的参数
         if(flag){
             this.czrzPageNum = 1;
         }
        
         //let params = commonFun.parameterSrc(this.formInline);
          let params = {};
          params.pageNum = this.czrzPageNum;
          params.pageSize = this.czrzPageSize;
          params.orderString = this.czrzOrderString;
          params = commonFun.parameterSrc(params);
         
         pageApi.getDataLogSourceList(params).then(response => { 
            if(response.data.status === 200){ 
                this.czrzTableData = response.data.data.list; 
                 // 页面总条数 
                this.czrzTotal = response.data.data.total; 
             } 
             else{ 
                this.czrzTableData = []; 
                this.czrzTotal = 0; 
                this.czrzPageSize = 10;
                this.czrzPageNum = 1;
            } 
                this.czrzTableLoading = false; 
            }).catch(() => { 
                this.czrzTableData = []; 
                this.czrzTotal = 0; 
                this.czrzPageSize = 10;
                this.czrzPageNum = 1;
                this.czrzTableLoading = false;
      })
    },
    //报告类型change事件
    reportTypeChange(val) {
       this.reportYear = '';
       this.selectDate = '';
       if (val === 'M') {
        this.reportTypeOther_show = true;
        this.reportTypeOther_year = true;
        this.reportTypeOther_day = false;
        this.reportTypeOther_weak = false;
        
        this.reportTypeArr2 = this.months;

      } else if (val === 'Y' || val === 'S') {
        this.reportTypeOther_show = false;
        this.reportTypeOther_year = true;
        this.reportTypeOther_day = false;
        this.reportTypeOther_weak = false;
        this.reportTypeArr2 = [];
      }else if (val === 'Q') {
        this.reportTypeOther_show = true;
        this.reportTypeOther_year = true;
        this.reportTypeOther_day = false;
        this.reportTypeOther_weak = false;
        this.reportTypeArr2 = this.quarters;
      } else if(val === 'D' || val === 'All'){
        this.reportTypeOther_show = false;
        this.reportTypeOther_year = false;
        this.reportTypeOther_day = true;
        this.reportTypeOther_weak = false;
      }else if(val === 'W'){
        this.reportTypeOther_show = false;
        this.reportTypeOther_year = false;
        this.reportTypeOther_day = true;
        //this.reportTypeOther_day = true;
        
      }
	  
	  if(val === 'All' || val === 'Q'|| val === 'S'||val === 'Y'){
		this.fundColumnShowFlag=true;
	  }else{
		this.fundColumnShowFlag=false;
	  }
	  
	  
	  
    },
      //获取Selects
    getSelects(val){
      let params = val;
      pageApi.getSelects(params).then(res =>{

          let self = this;
          if(res.data.message === "success"){

              if(val === 'fundinfo_fundState'){
                  this.proStatusArr = res.data.data;
                  let arr = res.data.data;
                  for(let i=0;i<arr.length;i++){
                    this.fundStatusArr[arr[i].dimCde] = arr[i].dimNme;
                  }

              }

              
          }else{
            this.$message.closeAll();
            this.$message.error('初始化数据失败');
          }

        }).catch(() => {
          this.$message.closeAll();
            this.$message.error('初始化数据失败');
           
      })

    },
    getProductsAll(){
        pageApi.getProductsAll().then(res =>{

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
    //数据字典转换
    dataStatus(statusCode,flag){
         if(flag === '1'){
            return this.fundStatusArr[statusCode];
        }
    },
       //关闭dialog
     handleClose(done){
          done();
         this.annExcelPage_show = false;
         this.annXmlPage_show = false;
         this.annTxtPage_show = false;
         this.annLogPage_show = false;
         this.currencyReportPage_show = false;
       
    }
   

   }
}
</script>
<style lang='css' scoped>

</style>
<style>
  .xbrlCzrzListWidth{
  width: 75% !important;
  margin-top: 5vh !important;
    }
  .qrfuListWidth{
  width: 45% !important;
    }
    .el-dialog .el-form {
    width: 100%!important;
}
</style>

<style rel="stylesheet/scss" lang="scss" scoped>
  
</style>

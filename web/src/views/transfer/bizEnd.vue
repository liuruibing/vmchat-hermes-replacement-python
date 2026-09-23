<template>
  <div>
      <div :style="{'height':form_show?'450px':'670px','overflow-y':form_show ? 'auto':'auto'}">
    <div style="width:80%;margin: 0 auto;">
          <el-steps  :active="activeStep"   finish-status="success">
            <el-step  title="流程发起" description="已完成"></el-step >
            <el-step  title="指令经办" description="已完成">></el-step >
            <el-step  title="指令复核" description="已完成"></el-step >
            <el-step title="管理人复核" description="已完成"></el-step >
            <el-step title="管理人审批" description="已完成"></el-step >
            <el-step  title="托管划款中" v-if="activeStep === 5" description="当前处理"></el-step >
            <el-step title="划款成功" v-if="activeStep === 5" description="待执行"></el-step >
            <el-step  title="托管划款中" v-if="activeStep === 7" description="已完成"></el-step >
            <el-step :title="cmdStatus==='transFailed'?'划款失败':'划款成功'" v-if="activeStep === 7" description="已完成"></el-step >
          </el-steps>
    </div>
    <el-button type="primary" style="margin-left: 70px; margin-top: 10px;" size="small" @click="serachBpm('1')">查看流程图</el-button>
     <el-button type="primary" size="small" @click="serachBpm('2')">查看交互指引</el-button>
    <el-form label-position="right" label-width="110px" :inline="true" ref = "formInline" :model="formInline"  class="commitRules" style="margin-top: 8px;margin-bottom: 10px;">
            <el-row>
              <el-col :span="24">
                <div style="width:620px; max-width: 100%;
                                            padding: 20px 20px 0;
                                            margin: 0 auto;
                                            overflow: hidden;">

                    <el-form-item  label="要求划款日期" prop="date">
                        <el-date-picker
                            v-model="formInline.date"
                            type="date"
                            size="small"
                            disabled
                            placeholder="选择日期">
                        </el-date-picker>
                    </el-form-item>
                    &nbsp;
                    <el-form-item label="产品名称" prop="accountCode">
                        <el-select disabled v-model="formInline.accountCode" placeholder="请选择" size="small">
                            <el-option
                                v-for="item in accountCodes"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>

                    <el-form-item  label="经纪商选择" prop="agent" v-if="formInline.agent">
                         <el-select v-model="formInline.agent" placeholder="请选择" size="small" disabled>
                             <el-option
                                 v-for="item in selects"
                                 :key="item.value"
                                 :label="item.label"
                                 :value="item.value">
                             </el-option>
                         </el-select>
                  </el-form-item>

                   <el-form-item  label="销售机构选择" prop="fundSalerName" v-if="formInline.fundSalerName">
                          <el-select v-model="formInline.fundSalerName" placeholder="请选择" size="small" disabled>
                              <el-option
                                  v-for="item in selects"
                                  :key="item.value"
                                  :label="item.label"
                                  :value="item.value">
                              </el-option>
                          </el-select>
                   </el-form-item>

                   <el-form-item  label="定存银行选择" prop="depositBankName" v-if="formInline.depositBankName">
                          <el-select v-model="formInline.depositBankName" placeholder="请选择" size="small" disabled>
                              <el-option
                                  v-for="item in selects"
                                  :key="item.value"
                                  :label="item.label"
                                  :value="item.value">
                              </el-option>
                          </el-select>
                    </el-form-item>
                    &nbsp;
                   <el-form-item  label="转账金额" prop="money" >
                          <el-input
                             v-model="formInline.money"
                             type="text"
                             disabled
                             size="small"
                          />
                  </el-form-item>

                  <el-form-item  label="备注" prop="remark">
                       <el-input
                           v-model="formInline.remark"
                           name="remark"
                           type="text"
                           disabled
                           size="small"
                         />
                  </el-form-item>
                <br>
                <el-form-item label="附件" prop="file">
                      <el-upload
                          class="upload-demo"
                          ref="upload"
                          action="https://jsonplaceholder.typicode.com/posts/"
                          :on-preview="handlePreview"
                          :on-remove="handleRemove"
                          :file-list="fileList"
                        
                          :auto-upload="false">
                        </el-upload>
                 </el-form-item>
                  </div>
              </el-col>
            </el-row>
          </el-form>
      <div style="width:620px; max-width: 100%;
                  padding: 10px 20px 0;
                  margin: 0 auto;
                  overflow: hidden;">
          <el-table
              :data="myData.datas"
              border
              stripe
              height="190"
              style="width: 100%"
              v-loading="tableLoading">

          <el-table-column
            type="index"
            label="序号"
            fixed
            align = "center"
            width="60">
          </el-table-column>

          <el-table-column
            prop="account.userName"
            label="处理人"
            min-width="90"
            header-align = "center"
            align = "left"
          >
            <template slot-scope="scope">
              <span>{{scope.row.account.userName | noDataFilter}}</span>
            </template>
          </el-table-column>

          <el-table-column
            prop="dateTime"
            label="处理时间"
            min-width = "110"
            :show-overflow-tooltip="true"
            header-align = "center"
          >
            <template slot-scope="scope">
              <span>{{scope.row.dateTime | noDataFilter}}</span>
            </template>
          </el-table-column>

          <el-table-column
            prop="taskName"
            label="任务节点"
            min-width = "90"
            :show-overflow-tooltip="true"
            header-align = "center"
          >
            <template slot-scope="scope">
              <span>{{scope.row.taskName | noDataFilter}}</span>
            </template>
          </el-table-column>

          <el-table-column
            prop="opinion"
            label="处理意见"
            min-width = "90"
            :show-overflow-tooltip="true"
            header-align = "center"
            align = "left"
          >
            <template slot-scope="scope">
              <span>{{scope.row.opinion | noDataFilter}}</span>
            </template>
          </el-table-column>
        </el-table>

          <div style="width:100%;height:20px;">
          <Pagination :total="total" :page="pageNumber" :limit = "pageSize" :page-sizes="[5,10,15,20]" @pagination = "Pagination"></Pagination>
          </div>

      </div>
       </div>
      <el-form ref="formHandle" :model="formHandle" :rules="commitRules" v-show="form_show"    class="commitClass" auto-complete="on" label-position="left">
            <el-form-item label="处理意见" prop="remark">
                <el-input
                  v-model="formHandle.remark"
                  type="textarea"
                  :rows="2"
                  maxlength="1000"
                  show-word-limit
                  placeholder="请输入处理意见"
                  auto-complete="off"
                    />
            </el-form-item>
            <el-button v-btn="pageData.normalCode" style="margin-top:10px" plain  type="primary" size="medium" @click="updateStatus('formHandle',0,'划款成功')">划款成功</el-button>
            <el-button v-btn="pageData.normalCode"  plain  type="primary" size="medium" @click="updateStatus('formHandle',1,'划款失败')">划款失败</el-button>
             
      </el-form>
  </div>


</template>

<script>
import Pagination from '@/components/Pagination'
import fun from '@/filters/common'
import hint from '@/components/hint'
import $ from 'jquery'
import commonApi from '@/api/common'
import commonFun from '@/filters/new_common'
import managerCheckApi from '@/api/transfer/managerCheck'

  export default {
    inject:['reload'],
    name: 'bizEnd',
    components: {Pagination,hint},
    props: {
     pageData:{
          pauseCode:'',
          unPauseCode:'',
          abandonCode:'',
          cancleCode:'',
          normalCode:'',
          retireCode:'',
        }
    },
    data() {
    //意见
      const validateRemark = (rule, value, callback) => {
          if (!value) {
            callback(new Error('请输入意见'))
          } else {
            callback()
          }
      };
      return {
       fileList: [],
       formInline:{
          accountCode:'选项1',//产品&基金代码
          date:'2019-12-18',//要求划款日期
          agent:'选项1',//经纪商选择
          money:'50,000',//转账金额
          instructType:'',//指令类型
          accountType:"银证转账",//转账类型
          type:"1",
          fundSalerName: '',//机构,
          depositBankName: '',//银行,
          remark:'尽快处理',//备注
          handel:''//处理意见
        },
        accountCodes:[],//产品名称数组
        selects:[],//定存银行数组
        myData: {datas:[]},//意见列表
        total:0,//总条数
        orderByString:'"dMettingdate" desc nulls last',//排序字段
        pageSize:5,//意见页面条数
        pageNumber:1,//意见页码
        formHandle:{
          remark: "" //处理意见
        },
        // 验证规则
        commitRules: {
          remark: [{ required: false }]
        },
        tableLoading:false,//意见列表加载
        myTaskId: '',
        procStatus:'',
        activeStep: 5,//进度条
        form_show: false,//form表单是否显示
         isInvest:false,//判断是否投资数据
       definedId:'',
        isOpen:false,
         cmdStatus:'',
        tableDatas: [] //记录传递的数组，前端自己分页

      }
    },
    //页面加载后触发
    mounted(){
         this.initData();
        let flag = localStorage.getItem('show_flag');
         if(flag === true || flag === 'true'){
             this.form_show = true;
         }
     },
    methods: {
      //文件上传事件
      submitUpload() {
          this.$refs.upload.submit();
      },
      //文件移除事件
      handleRemove(file, fileList) {
           console.log(file, fileList);
      },
      handlePreview(file) {
          if(file.id){
             let params = {};
                params.id = file.id;
                params = commonFun.parameterSrc(params);

                // token信息
              if(this.$store.getters.token){ params["token"] = this.$store.getters.token;}
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
              let action = this.$store.state.setting.baseApi + 'api/file/v1.0/downloadFile';

              commonFun.formDownloadFile(params,action,"GET");
          }
      },
      //意见列表分页
      Pagination(val){
        var self = this;
        self.pageSize = val.limit; //10 一页几条
        self.pageNumber = val.page; //1 //页码
        let number = self.pageNumber -1;
        var i =  self.pageSize * number;
        var maxLength = self.pageSize *  self.pageNumber; //一共需要展示条数
        if(maxLength > self.tableDatas.length){
              maxLength = self.tableDatas.length;
        }
        let arr = [];
        for(i;i<maxLength;i++){
            arr.push(this.tableDatas[i]);
        }
        self.myData.datas = arr;
        //self.searchPage();
      } ,
      //列表排序
      managerCheckComDataChangeSort(val){
         var self = this;
         self.orderByString = self.$fun.orderByString(val);
         //self.searchPage();
       },
       //审核通过，退回，作废，暂缓等操作
       updateStatus(vals,status,confirmStatus){
          this.$confirm('是否'+confirmStatus,'提示',{
              confirmButtonText: '确定',
              cancelButtonText: '取消',
              type: 'warning'
          }).then(() => {

              let params = Object.assign({},this.formHandle);
              let sendData = {};
              let taskExcuteCmdMode = {taskExcuteCmdType:'Normal'};
              let taskOpinionModel = {agree:true};
              taskOpinionModel.opinion = this.formHandle.remark;
              let formData = {};
              if(status === 0){
                  formData.transferResult = true;
              }else{
                formData.transferResult = false;
              }
              formData.remoteOperationFlag = false;
              sendData.formData = formData;
              sendData.taskOpinionModel = taskOpinionModel;
              sendData.taskExcuteCmdMode = taskExcuteCmdMode;
              
              let taskId = this.myTaskId;
              managerCheckApi.updateStatus(taskId,sendData).then(res => {
                  let data= res.data.data;
                  if(res.data.status === 0){
                    this.$message.closeAll();
                      this.$message({
                        type: 'success',
                        message: '操作成功'
                      });
                      this.reload();
                  }else{
                    this.$message.closeAll();
                     this.$message({
                      type: 'error',
                      message: res.data.message ||'操作失败'
                      });
                  }

              }).catch(() => {
                this.$message.closeAll();
                  this.$message({
                    type: 'info',
                    message: '操作失败'
                  });
            })
        }).catch(() => {
          this.$message.closeAll();
            this.$message({
              type: 'info',
              message: '已取消'
             });
        })

      },
      initData(){

          //初始化列表数据
          let resultData =  localStorage.getItem('resultData');
          this.myTaskId = localStorage.getItem('trackingAgent_taskId');
          resultData = JSON.parse(resultData);
          let taskOpinionModels = resultData.data.taskOpinionModels;
          for(let i = 0; i < taskOpinionModels.length; i++){
              if(taskOpinionModels[i].dateTime){
                  taskOpinionModels[i].dateTime = fun.yyr_timestampToTime(taskOpinionModels[i].dateTime);
              }
          }

          if(taskOpinionModels.length > 5){
              let arr = [];
              for(let i=0;i< 5;i++){
                let data = taskOpinionModels[i];
                arr.push(data);
              }
              this.myData.datas = arr;
          }else{
              this.myData.datas = taskOpinionModels;
          }
          this.total = taskOpinionModels.length;
          this.tableDatas = resultData.data.taskOpinionModels;

          //初始化表单数据
          let formData = resultData.data.processInstance.processFormData;
          this.formInline.accountCode = formData.fundName;
          this.formInline.date =  formData.transferReqdate;
          this.formInline.agent = formData.brokerName;
          this.formInline.money = fun.formatNumber(formData.transferAmount);
          this.formInline.remark = formData.remark;
          this.formInline.fundSalerName = formData.fundSalerName;
          this.formInline.depositBankName = formData.depositBankName;
          this.fileList = resultData.data.fileList;
          let procStatus = resultData.procStatus;
          this.procStatus = procStatus;
          this.cmdStatus = resultData.cmdStatus;
          this.definedId = resultData.definedId;
          if( procStatus === 'transSuccess' || procStatus === 'transFailed'){
                this.activeStep = 7;
          }

          if(procStatus === 'transFailed'){
                setTimeout(function(){
                var aa = $('.el-step__title');
                var hh = $('.el-step__description');
                 //debugger;
               
                aa[6].style.color="red";
                 hh[6].style.color="red";
                 
                },300)
          }

          setTimeout(function(){
                 //debugger;
                var hh1 = $('.el-icon-close-tip');
                 if(hh1.length>0){
                                    hh1[0].style.display="none";
                              }
          },300)
        
        
          


      },
       serachBpm(val){
     
          if(val ==='2'){
                this.isOpen = !this.isOpen;
               this.$emit('drawerClick', {
                data: [],
                definedId:'',
                flag:false,
                isOpen:this.isOpen
              })
              return;
          }
          this.$emit('drawerClick', {
          data: [],
          definedId:this.definedId,
          flag:true
        })
        
    }

    }
  }
</script>
<style rel="stylesheet/scss" lang="scss" >

</style>

<style rel="stylesheet/scss" lang="scss" scoped>

.commitClass{
 position: relative;
    width: 620px;
    max-width: 100%;
    padding: 10px 20px 0;
    margin: 0 auto;
    overflow: hidden;

}
.el_form_item{
width:240px !important
}

.upload-demo{
    margin-top: -38px;
}
</style>

<style rel="stylesheet/scss" lang="scss" >
  /* 修复input 背景不协调 和光标变色 */
  /* Detail see https://github.com/PanJiaChen/vue-element-admin/pull/927 */

  $bg:#283443;
  $light_gray:#eee;
  $cursor: #fff;

  @supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
    .login-container .el-input input{
      color: $cursor;
      &::first-line {
        color: $light_gray;
      }
    }
  }

  /* reset element-ui css */
  .login-container {
    .el-input {
      display: inline-block;
      height: 47px;
      width: 85%;
      input {
        background: transparent;
        border: 0px;
        -webkit-appearance: none;
        border-radius: 0px;
        padding: 12px 5px 12px 15px;
        color: $light_gray;
        height: 47px;
        caret-color: $cursor;
        &:-webkit-autofill {
          -webkit-box-shadow: 0 0 0px 1000px $bg inset !important;
          -webkit-text-fill-color: $cursor !important;
        }
      }
    }
    .el-form-item {
      border: 1px solid rgba(255, 255, 255, 0.1);
      background: rgba(0, 0, 0, 0.1);
      border-radius: 5px;
      color: #454545;
    }
  }


  input::-webkit-outer-spin-button,input::-webkit-inner-spin-button{
    -webkit-appearance: none;
  }
  input[type="number"]{
    -moz-appearance: textfield;
  }
 .el-steps--simple{
  width:60%;
  height:25px;
  margin: 0 auto;
  background-color:white;
 }
 .el-step.is-simple .el-step__title{
    font-size:14px;
 }

</style>

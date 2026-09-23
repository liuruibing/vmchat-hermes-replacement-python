<template>
  <div class="dialog_email">
    <el-form ref="formData" status-icon label-width="120px" :model="formData" :rules="formDataRules"  class="commitClass" auto-complete="on" label-position="right">
      <el-form-item  label="收件人" prop="emailTos">
        <selectContacts ref="selectContacts" v-model="formData.emailTos" ></selectContacts>
      </el-form-item>
      <el-form-item  label="抄送" prop="emailCcs">
        <selectContacts ref="selectContacts2" v-model="formData.emailCcs" ></selectContacts>
      </el-form-item>
      <el-form-item  label="密送" prop="emailBccs">
        <selectContacts ref="selectContacts3" v-model="formData.emailBccs" ></selectContacts>
      </el-form-item>
        <el-form-item style="width:100%" label="主题" prop="emailSubject">
          <el-input
            type="textarea"
            maxlength="200"
            show-word-limit
            :autosize="{ minRows: 2,maxRows: 2}"
            placeholder="请输入内容"
            v-model="formData.emailSubject">
          </el-input>
        </el-form-item>
        <el-form-item style="width:100%" label="正文" prop="emailContent">
          <el-input
            type="textarea"
            :autosize="{ minRows: 4,maxRows: 8}"
            placeholder="请输入内容"
            v-model="formData.emailContent">
          </el-input>
        </el-form-item>
        <el-form-item label="附件上传" prop="file">
          <el-upload
            class="upload-demo"
				    v-model="fileList"
            ref="upload"
            name="file"
            :headers="hearders"
            :action="fileUploadUrl"
            :on-error="handleError"
            :on-remove="handleRemove"
            :on-success="handleSuccess"
            :on-change="handleChange"
            :file-list="fileList"
            :auto-upload="false">
            <el-button slot="trigger" size="small" type="primary">浏览</el-button><br>
            <el-checkbox v-if="fileName_show" v-model="checked">{{fileName}}</el-checkbox>
          </el-upload>
        </el-form-item>
        <div style="margin-left:120px">
          <span style="color:red">{{warning}}</span>
        </div>
      <div style="overflow:hidden;">
        <span style="float:right;">
        <el-button type="primary" size="small" icon="el-icon-s-promotion" @click="send" :loading="sendLoading">发送邮件</el-button>
        </span>
      </div>
    </el-form>
  </div>
</template>

<script>
import $ from "jquery"
import trackingAgentApi from '@/api/transfer/trackingAgentList'
import selectContacts from '@/components/selectContacts/index2'
import configurationApi from '@/api/configuration/configuration.js'
import fun from '@/filters/common'
export default {
  components:{
    selectContacts,
  },
  data(){
    return{
      formData:{
        emailTos:[],
        emailCcs:[],
        emailBccs:[],
        emailSubject:'',
        emailContent:''
      },
      fileList:[],
      warning:'',
      fileUploadUrl:"",
      hearders:{},
      checked:true,
      sendLoading:false,
      row:{},
      formDataRules:{
        emailTos:[
          { required: true, message: '请选择收件人', trigger: 'change' },
        ],
      },
      cmdCodeArr:{},
      fileName:'',
      fileName_show:false,
    }
  },
  mounted(){
   this.init() 
  },
  methods:{
    init(){
      let arr3 = [
        // 转账指令
        { name: "银转证", code: "gm040101" },
        { name: "证转银", code: "gm040102" },
        { name: "银转期", code: "gm040201" },
        { name: "期转银", code: "gm040202" },
        { name: "银转期(手工入金)", code: "gm040203" },
        { name: "银转信", code: "gm040301" },
        { name: "信转银", code: "gm040302" },
        { name: "银转衍", code: "gm040401" },
        { name: "衍转银", code: "gm040402" },
        { name: "银转衍(手工入金)", code: "gm040403" },
        { name: "银转贵", code: "gm040501" },
        { name: "贵转银", code: "gm040502" },
        { name: "银转贵(手工入金)", code: "gm040503" },
        { name: "交易所交易（付款）", code: "gm040601" },
        { name: "交易所交易（收款）", code: "gm040602" },
        { name: "备付金代付", code: "gm040603" },
        { name: "托管转中债", code: "gm040701" },
        { name: "中债转托管", code: "gm040702" },
        { name: "托管转上清", code: "gm040703" },
        { name: "上清转托管", code: "gm040704" },
        { name: "中债转上清", code: "gm040705" },
        { name: "上清转中债", code: "gm040706" },
        // 投资指令
        { name: "基金认申购", code: "gm050101" },
        { name: "存款投资", code: "gm050102" },
        { name: "网下新股申购(上海)", code: "gm050103" },
        { name: "网下新股申购(深圳)", code: "gm050104" },
        { name: "网下新债申购", code: "gm050105" },
        { name: "银行间债券交易", code: "gm050106" },
        { name: "其他", code: "gm050107" },
        // TA
        { name: "待办TA赎回划款", code: "gm030101" },
        { name: "待办TA分红划款", code: "gm030102" },
        { name: "主动发起划款", code: "gm030103" },
        { name: "待办TA清算款", code: "gm030104" },
        // 付费
        { name: "手动扣费支付", code: "gm020101" },
        { name: "应付管理人报酬", code: "gm020102" },
        { name: "应付管理人风险准备金(含损益平准金)", code: "gm020103" },
        { name: "应付托管费", code: "gm020104" },
        { name: "应付销售服务费", code: "gm020105" },
        { name: "应付佣金", code: "gm020106" },
        { name: "其他费用(含损益平准金)", code: "gm020107" },
        { name: "应付托管人风险准备金", code: "gm020108" },
        { name: "应付银行间交易费", code: "gm020109" },
        { name: "应付投资顾问费", code: "gm020110" },
        { name: "ETF代收代付", code: "gm020111" },
        { name: "付增值税", code: "gm020112" },
        { name: "应付业绩报酬", code: "gm020113" },
        { name: "应付业绩报酬风险金", code: "gm020114" },
      ];
      for (let i = 0; i < arr3.length; i++) {
        this.cmdCodeArr[arr3[i].code] = arr3[i].name;
      }
    },
    //数据字典转换
    dataStatus(statusCode) {
      if(!statusCode){
        return ''
      }else{
        return this.cmdCodeArr[statusCode];
      }
    },
    handleRemove(file, fileList){
      this.fileList = fileList;
    },
    handleSuccess(){},
    handleError(){},
    handleChange(file, fileList){
      console.log(file, fileList);
      this.fileList = fileList;
      // console.log('this.fileList',this.fileList);
    },
    getEmailInfo(row){
      // console.log('email',row);
      this.fileName = row.fundName+'划款指令'+row.pfomBizNum+'.pdf';
      this.row = row;
      this.getTemp(row)
      this.getFileList(row.id);
      this.getFormData(row);
    },
    getTemp(row){
      console.log(row.fundCode);
      let params = {fundCode:row.fundCode}
      configurationApi
        .getTemplate(params)
        .then(res=>{
          // console.log(res);
          if(res.data.status==200){
            this.fileName_show = true;
            this.checked = true;
            setTimeout(() => {
              $('.el-checkbox__label').attr("title",this.fileName)
            }, 500);
          }else{
            this.fileName_show = false;
            this.checked = false;
          }
        })
    },
    getFormData(row){
      let params = {id:row.id}
      trackingAgentApi.getEmailInfo(params).then(res=>{
        if(res.data.data){
          let data = res.data.data;
          this.formData.emailTos = data.emailTos;
          this.formData.emailCcs = data.emailCcs;
          this.formData.emailBccs = data.emailBccs;
          let emailSubject = data.emailSubject;
          let emailContent = data.emailContent;
          this.warning = data.warning;
          // brokerName,cmdCode,depositBankName,fundName,fundSalerName,payeeAcconame,payeeAccount,payeeBank,payerAcconame,payerAccount,payerBank,paymentSystemNum,processUse,remark,stockCode,transferAmount,transferReqDate
          let arr1 = ['brokerName','depositBankName','fundName','fundSalerName','payeeAcconame','payeeAccount','payeeBank','payerAcconame','payerAccount','payerBank','paymentSystemNum','processUse','remark','stockCode','transferReqDate']
          let arr2 = ['brokerName','depositBankName','fundName','fundSalerName','payeeAcconame','payeeAccount','payeeBank','payerAcconame','payerAccount','payerBank','paymentSystemNumber','processUse','remark','stockCode','transferReqdate']

          for(let i = 0; i < arr1.length; i++){
            let reg = new RegExp(`\\$${arr1[i]}\\$`, "g");
            // console.log(reg);
            // emailSubject = emailSubject.replace(`$${arr1[i]}$`, row[arr2[i]] || '');
            // emailContent = emailContent.replace(`$${arr1[i]}$`, row[arr2[i]] || '');
            emailSubject = emailSubject.replace(reg, row[arr2[i]] || '');
            emailContent = emailContent.replace(reg, row[arr2[i]] || '');
          }
          console.log(this.dataStatus(row.cmdCode));
          emailSubject = emailSubject.replace(/\$cmdCode\$/g, this.dataStatus(row.cmdCode) || '');
          emailContent = emailContent.replace(/\$cmdCode\$/g, this.dataStatus(row.cmdCode) || '');
          if(row.transferAmount){
            emailSubject = emailSubject.replace(/\$transferAmount\$/g, fun.moneyYuan(row.transferAmount) || '');
            emailContent = emailContent.replace(/\$transferAmount\$/g, fun.moneyYuan(row.transferAmount) || '');
          }
          if(emailSubject.length>200){
            emailSubject = emailSubject.substr(0,200)
          }
          this.formData.emailSubject = emailSubject;
          this.formData.emailContent = emailContent;
        }
      })
    },
    // 获取文件列表信息
    getFileList(id){
      trackingAgentApi.getFileList(id).then(res =>{
        if(res.data.message === "success"){
          let arr = res.data.data;
          this.fileList = [];
          for(let i=0; i<arr.length; i++){
            let obj={};
            obj.id = arr[i].id;
            obj.url = arr[i].fileUri;
            obj.name = arr[i].fileName;
            obj.size = arr[i].fileSize;
            this.fileList.push(obj);
          }
        }
      }).catch(() => {})
    },
    send(){
      // console.log(this.formData);
      // console.log(this.$parent);
      
      // this.$parent.closeEmail()
      this.$refs['formData'].validate((valid) => {
        if (valid) {
          this.sendTrue();
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    sendTrue(){
      this.sendLoading = true;
      let formData = new FormData();
      formData.append("id",this.row.id);
      formData.append("emailTos",this.formData.emailTos);
      formData.append("emailCcs",this.formData.emailCcs);
      formData.append("emailBccs",this.formData.emailBccs);
      formData.append("emailSubject",this.formData.emailSubject);
      formData.append("emailContent",this.formData.emailContent);
      if(this.checked){
        formData.append("isPdf",1);
      }else{
        formData.append("isPdf",0);
      }
      let oldfileArr = [];
      for(let i=0;i< this.fileList.length;i++){
        if(this.fileList[i].raw){
          let aa = this.fileList[i].raw;
          formData.append('files', aa);
        }
        if(!this.fileList[i].raw){
          let bb = this.fileList[i].id;
          oldfileArr.push(bb);
        }
      }
      formData.append('fileIds', oldfileArr);
      trackingAgentApi.sendMessage(formData).then(res=>{
        if(res.data.status==200){
          // this.$parent.closeEmail();
          this.sendLoading = false;
          this.$emit('close',false)
          this.$message({
            message: res.data.message || '发送成功',
            type: 'success'
          });
          this.$nextTick(()=>{
            this.$parent.$parent.refashBtn()
          })
        }else{
          this.sendLoading = false;
          this.$message({
            message: res.data.message || '发送失败',
            type: 'error'
          });
        }
      }).catch(()=>{
        this.sendLoading = false;
        this.$message({
          message: '发送失败',
          type: 'error'
        });
      })
    },
  },
}
</script>

<style lang="scss">
.dialog_email {
  .el-form-item__content{
    min-width: 0 !important;
  }
  .upload-demo{
    .el-checkbox{
      width: 100%;
      .el-checkbox__label{
        width: 100%;
        white-space: nowrap;
        overflow: hidden;	      
        display: inline-block;
        text-overflow: ellipsis;
        position: absolute;
        top: 8px;
      }
    }
  }
}
</style>
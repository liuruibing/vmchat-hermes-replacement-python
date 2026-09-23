<template>
  <div class="glrgb_edit_form">
    <div class="warning_">
      <p class="warning_message" v-for="item in warningArr" :key="item.id">{{item.messageContent}}</p>
    </div>
    <el-form
      label-position="right"
      label-width="110px"
      :rules="formDataRules"
      :model="formData"
      ref="formData"
      v-loading="form_loading"
    >
      <el-form-item prop="fundCode" label="产品">
        <selectTable
          :disabled="true"
          v-model="formData.fundCode"
          @sendDataObj="fundCodeChange"
        ></selectTable>
      </el-form-item>
      <el-form-item prop="transferReqdate" label="要求划款日期">
        <el-date-picker
          style="width: 100%"
          v-model="formData.transferReqdate"
          type="date"
          :picker-options="pickerOptions"
          value-format="yyyy-MM-dd"
          placeholder="选择日期"
        >
        </el-date-picker>
      </el-form-item>
      <el-form-item
        label="科目数截止日期"
        v-if="cmdType == 'pay'"
        prop="subjectDeadlineAt"
      >
        <el-date-picker
          style="width: 100%"
          v-model="formData.subjectDeadlineAt"
          type="date"
          :picker-options="pickerOptions"
          value-format="yyyy-MM-dd"
          placeholder="选择日期"
        >
        </el-date-picker>
      </el-form-item>
      
      <el-form-item prop="transferAmount" label="转账金额(元)">
        <el-input
          v-model="formData.transferAmount"
          @focus="moneyFocus"
          @blur="moneyBlur"
          type="text"
        >
        </el-input>
      </el-form-item>
      <el-form-item
        prop="brokerCode"
        label="经纪商"
        v-if="cmdType == 'transfer' && !['gm040601','gm040602','gm040603','gm040701','gm040702','gm040703','gm040704','gm040705','gm040706'].includes(cmdCode)"
      >
        <el-select
          style="width: 100%"
          v-if="
            ['040101', '040102', '040201', '040202', '040203'].includes(cmdCode)
          "
          filterable
          clearable
          v-model="formData.brokerCode"
          placeholder="请选择"
          class="el_form_item"
        >
          <el-option
            v-for="(item, index) in borkerInfos"
            :key="index + 'broker'"
            :label="item.name"
            :value="item.value"
          >
          </el-option>
        </el-select>
        <el-input
          v-else
          v-model="formData.brokerCode"
          maxlength="134"
        ></el-input>
      </el-form-item>
      <!-- <el-form-item
        prop="fundSalerName"
        label="销售机构"
        v-if="cmdType == 'invest' && cmdCode == '050101'"
      >
        <el-select
          style="width: 100%"
          v-model="formData.fundSalerName"
          placeholder="请选择"
        >
          <el-option
            v-for="item in saleMechanisms"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
      </el-form-item> -->
      <!-- <el-form-item
        prop="depositBankName"
        label="定存银行"
        v-if="cmdType == 'invest' && cmdCode == '050102'"
      >
        <el-select
          style="width: 100%"
          v-model="formData.depositBankName"
          placeholder="请选择"
        >
          <el-option
            v-for="item in bankArr"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
      </el-form-item> -->
      <el-form-item
        prop="stockCode"
        label="股票/债券代码"
        v-if="
          cmdType == 'invest' && (cmdCode == '050103' || cmdCode == '050104')
        "
      >
        <el-input v-model="formData.stockCode"></el-input>
      </el-form-item>
      <div class="payerAcconame_">
      <el-form-item prop="payerAcconame" label="付款人">
        <selectAccount
          v-model="formData.payerAcconame"
          @sendDataObj="getAccountInfo1"
          :disabled="formData.noTransaction=='1'?true:false"
          ref="selectAccount1"
        ></selectAccount>
      </el-form-item>
      <el-form-item prop="payerAccount" label="付款账号">
        <el-input v-model="formData.payerAccount" maxlength="66" disabled></el-input>
      </el-form-item>
      <el-form-item prop="payerBank" label="付款行">
        <el-input v-model="formData.payerBank" maxlength="66" disabled></el-input>
      </el-form-item>

      </div>
      <el-form-item label="收款人" prop="payeeAcconame">
        <selectAccount
          v-model="formData.payeeAcconame"
          @sendDataObj="getAccountInfo2"
          :disabled="formData.noTransaction=='1'?true:false"
          ref="selectAccount2"
        ></selectAccount>
      </el-form-item>
      <el-form-item prop="payeeAccount" label="收款账号">
        <el-input v-model="formData.payeeAccount" maxlength="66" disabled></el-input>
      </el-form-item>
      <el-form-item prop="payeeBank" label="收款行">
        <el-input v-model="formData.payeeBank" maxlength="66" disabled></el-input>
      </el-form-item>
      <el-form-item prop="paymentSystemNumber" label="支付系统号">
        <el-input
          v-model="formData.paymentSystemNumber"
          maxlength="66"
          disabled
        ></el-input>
      </el-form-item>
      <el-form-item prop="remark" label="用途">
        <el-input
          v-model="formData.processUse"
          name="processUse"
          type="textarea"
          maxlength="1000"
          show-word-limit
          :autosize="{ minRows: 2 }"
        >
        </el-input>
      </el-form-item>
      <el-form-item prop="remark" label="备注">
        <el-input
          v-model="formData.remark"
          name="remark"
          type="textarea"
          maxlength="1000"
          show-word-limit
          :autosize="{ minRows: 2 }"
        >
        </el-input>
      </el-form-item>
      <el-form-item label="附件" prop="file">
        <el-upload
          class="upload-demo"
          ref="upload"
          action="https://jsonplaceholder.typicode.com/posts/"
          :on-preview="handlePreview"
          :on-change="handleChange"
          :on-remove="handleRemove"
          :file-list="fileList"
          :auto-upload="false"
        >
          <el-button slot="trigger" size="small" type="primary"
            >选取文件</el-button
          >
        </el-upload>
      </el-form-item>
      <div style="text-align: right">
        <el-button plain type="primary" @click="save" :loading="btn_loading"
          >保存</el-button
        >
      </div>
    </el-form>
  </div>
</template>

<script>
import fun from "@/filters/common";
import commonFun from "@/filters/new_common";
import customApi from "@/api/custom/customList";
import selectTable from "@/views/commonComponents/selectTable.vue";
import selectAccount from "@/views/commonComponents/selectAccount.vue";
import modelFileValidate from "@/mixinsModel/file-validate";
import investBizBeginApi from "@/api/invest/investBizBegin";
import transferBizBeginApi from "@/api/transfer/bizBegin";
import trackingAgentApi from "@/api/transfer/trackingAgentList";
import accountApi from "@/api/product/accountSearch";
export default {
  mixins: [modelFileValidate],
  components: { selectTable, selectAccount },
  props: {},
  data() {
    return {
      fileList: [],
      formData: {
        // pfomBizNum: "", //业务流水号
        // beginTime: "", //发起时间
        subjectDeadlineAt: "", //科目取数截止日期
        fundCode: "", //产品&基金代码
        transferReqdate: "", //要求划款日期
        brokerCode: "", //经纪商选择
        transferAmount: "", //转账金额
        instructType: "", //指令类型
        accountType: "", //转账类型
        type: "",
        fundSalerName: "", //机构,
        depositBankName: "", //银行,
        remark: "", //备注
        handel: "", //处理意见
        payerAcconame: "", //付款人
        payerAccount: "", //付款账号
        payerBank: "", //付款行
        payeeAcconame: "", //收款人
        payeeAccount: "", //收款账号
        payeeBank: "", //收款行
        paymentSystemNumber: "", //支付系统号
        processUse: "", //用途
        stockCode: "", // 股票债券代码
        noTransaction: "",
      },
      saleMechanisms: [],
      bankArr: [],
      moneyValidateDefalut:
        /^(0|[1-9]{1}\d{0,14}|[1-9]{1}\d{0,12}\.\d{1}|[1-9]{1}\d{0,11}\.\d{2}|0\.\d{1,2})$/,
      moneyValidate:
        /^(0|[1-9]{1}\d{0,14}|[1-9]{1}\d{0,12}\.\d{1}|[1-9]{1}\d{0,11}\.\d{2}|0\.\d{1,2})$/,
      formDataRules: {
        fundCode: [
          {
            required: true,
            pattern: "",
            message: "请选择产品",
            trigger: "change",
          },
        ],
        transferAmount: [
          {
            required: true,
            trigger: "change",
            pattern: "",
            message: "请输入数值且最多包含2位小数",
          },
        ],
        payerAcconame: [
          {
            required: true,
            pattern: "",
            message: "请输入付款人",
            trigger: "change",
          },
        ],
        payerAccount: [
          {
            required: true,
            pattern: "",
            message: "请输入付款账号",
            trigger: "change",
          },
          {
            required: false,
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母加数字的组合",
            trigger: "change",
          },
        ],
        payerBank: [
          {
            required: true,
            pattern: "",
            message: "请输入付款行",
            trigger: "change",
          },
        ],
        payeeAcconame: [
          { required: true, message: "请输入收款人", trigger: "change" },
        ],
        payeeAccount: [
          { required: true, message: "请输入收款账号", trigger: "change" },
          {
            required: false,
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母加数字的组合",
            trigger: "change",
          },
        ],
        payeeBank: [
          { required: true, message: "请输入收款行", trigger: "change" },
        ],
        paymentSystemNumber: [
          // {required:true, message: "请输入支付系统号", trigger: "change"},
          {
            required: false,
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母加数字的组合",
            trigger: "change",
          },
        ],
        // dBeginTime:[{required:true, message: "请选择指令日期", trigger: "change"}],
        transferReqdate: [
          { required: true, message: "请选择到账日期", trigger: "change" },
        ],
        brokerCode: [
          { required: true, message: "请输入经纪商", trigger: "change" },
        ], //经纪商
        subjectDeadlineAt: [
          {
            required: false,
            message: "请选择科目数截止日期",
            trigger: "change",
          },
        ], //科目取数截止日期
        fundSalerName: [
          {
            required: true,
            message: "请选择销售机构",
            trigger: "change",
          },
        ],
        depositBankName: [
          {
            required: true,
            message: "请选择定存银行",
            trigger: "change",
          },
        ],
      },
      pickerOptions: {},
      fundCodeChangeNum: 0,
      cmdType: "",
      cmdCode: "",
      id: "",
      taskId:"",
      btn_loading: false,
      api: "",
      payeeApi:"",
      payerApi:"",
      borkerInfos: [],
      form_loading:false,
      warningArr:[],
    };
  },
  watch:{
    // cmdCode(data){
    //   console.log("watch指令编辑--"+data);
    // }
    "formData.noTransaction"(data){
      if(data=='1'){
        this.formData.payerAcconame = ''
        this.formData.payeeAcconame = ''
        this.formDataRules.payerAcconame[0].required = false;
        this.formDataRules.payerAccount[0].required = false;
        this.formDataRules.payerBank[0].required = false;
        this.formDataRules.payeeAcconame[0].required = false;
        this.formDataRules.payeeAccount[0].required = false;
        this.formDataRules.payeeBank[0].required = false;
        this.$refs['formData'].validate((valid) => {})
      }else{
        this.formDataRules.payerAcconame[0].required = true;
        this.formDataRules.payerAccount[0].required = true;
        this.formDataRules.payerBank[0].required = true;
        this.formDataRules.payeeAcconame[0].required = true;
        this.formDataRules.payeeAccount[0].required = true;
        this.formDataRules.payeeBank[0].required = true;
      }
    },
  },
  mounted() {
    this.$nextTick(() => {});
    this.getSaleMechanism();
    this.getBank();
    this.pickerOptions = {
      disabledDate(time) {
        return time.getTime() < new Date() - 24 * 60 * 60 * 1000;
      },
    };
  },
  methods: {
    handlePreview() {},
    // 文件状态改变时的钩子
    handleChange(file, fileList) {
      this.fileValidate(file, fileList);
    },
    // 移出
    handleRemove(file, fileList) {
      this.handleChange(file, fileList);
    },
    getFormData(id) {
      console.log("getFormData");
      this.form_loading = true;
      let params = {id}
      trackingAgentApi.getFormData(params).then(res=>{
        if(res.data.status==0 && res.data.message == 'success'){
          this.form_loading = false;
          let data = res.data.data;
          this.formData.beginTime = data.beginTime || ''
          this.formData.subjectDeadlineAt = data.subjectDeadlineAt || ''
          if(data.pfomBizNum){
            this.formData.pfomBizNum = data.pfomBizNum
          }else{
            this.formData.pfomBizNum = this.pfomBizNum
          }
          this.formData.transferReqdate = data.transferReqdate || ''
          this.formData.fundCode = data.fundCode+"_"+data.fundName;
          if(data.fundCode){this.fundCode=data.fundCode}
          if(data.id){this.id=data.id}
          // this.formData.money = fun.formatNumber(data.transferAmount) | moneyYuan
          this.formData.transferAmount = fun.moneyYuan(data.transferAmount)
          if(data.fundSaler && data.fundSalerName){
            this.formData.fundSalerName = data.fundSaler +"|"+ data.fundSalerName || ''
          }else{
            this.formData.fundSalerName = ''
          }
          if(data.depositBank && data.depositBankName){
            this.formData.depositBankName =data.depositBank +'|'+ data.depositBankName || ''
          }else{
            this.formData.depositBankName = ''
          }
          this.formData.remark = data.remark || ''
          this.formData.brokerCode = data.brokerCode || ''
          this.formData.payerAcconame = data.payerAcconame || ''
          this.formData.payerAccount = data.payerAccount || ''
          this.formData.payerBank = data.payerBank || ''
          this.formData.payeeAcconame = data.payeeAcconame || ''
          this.formData.payeeAccount = data.payeeAccount || ''
          this.formData.payeeBank = data.payeeBank || ''
          this.formData.paymentSystemNumber = data.paymentSystemNumber || ''; //支付系统号
          this.formData.processUse = data.processUse || ''; //用途
          this.formData.stockCode = data.stockCode || ''; //股票债券代码
          this.formData.noTransaction = data.noTransaction || '';

          this.$bus.$emit('editFormData',JSON.parse(JSON.stringify(this.formData)));
        }else{
          this.$message({type:"error",message:"获取表单数据失败！"})
          this.form_loading = true;
        }
      })
    },
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
    // 查询销售机构
    getSaleMechanism() {
      let params = "fundSalerType";
      investBizBeginApi
        .getSaleMechanism(params)
        .then((res) => {
          if (res.data.message === "success") {
            let arr = res.data.data;
            this.saleMechanisms = [];
            for (let i = 0; i < arr.length; i++) {
              let obj = {};
              obj.value = arr[i].dimCde + "|" + arr[i].dimNme;
              obj.label = arr[i].dimNme;
              this.saleMechanisms.push(obj);
            }
            // console.log('this.saleMechanisms',this.saleMechanisms);
          } else {
            this.saleMechanisms = [];
            this.$message.closeAll();
            this.$message.error("查询销售机构信息失败");
          }
        })
        .catch(() => {
          this.$message.closeAll();
          this.$message.error("查询销售机构信息失败");
        });
    },
    getBank() {
      let params = "bankType";
      investBizBeginApi
        .getBank(params)
        .then((res) => {
          if (res.data.message === "success") {
            let arr = res.data.data;
            this.bankArr = [];
            for (let i = 0; i < arr.length; i++) {
              let obj = {};
              obj.value = arr[i].dimCde + "|" + arr[i].dimNme;
              obj.label = arr[i].dimNme;
              this.bankArr.push(obj);
            }
            // console.log('this.bankArr',this.bankArr);
          } else {
            this.bankArr = [];
            this.$message.closeAll();
            this.$message.error("查询银行信息失败");
          }
        })
        .catch(() => {
          this.$message.closeAll();
          this.$message.error("查询银行信息失败");
        });
    },
    init(cmdType, cmdCode, id , taskId) {
      // console.log(cmdType, cmdCode, id);
      this.cmdType = cmdType;
      this.cmdCode = cmdCode;
      this.id = id;
      this.taskId = taskId;
      // 账户来源
      this.getAccOrigin(cmdType,cmdCode);
      this.getFormData(id);
      this.getFileList(id);
      this.getpmList(taskId);
      // this.formData = JSON.parse(JSON.stringify(data));
      // this.fileList = JSON.parse(JSON.stringify(fileList));
      if (this.cmdType == "transfer") {
        if (["gm040101", "gm040102"].includes(this.cmdCode)) {
          this.api = "getZqAccountSELECT";
        } else if (["gm040201", "gm040202", "gm040203"].includes(this.cmdCode)) {
          this.api = "getZqAccountSELECTYH";
        } else {
          this.api = "";
        }
      } else {
        this.api = "";
      }
      
    },
    getAccOrigin(cmdType,cmdCode){
      if(cmdType=="transfer"){
        if(["gm040101"].includes(cmdCode)){
            // 证券账户
            this.payeeApi = 'getZqAccList2'
          }else if(["gm040102","gm040202","gm040302","gm040402","gm040502","gm040602","gm040702","gm040704"].includes(cmdCode)){
            // 托管户
            this.payeeApi = 'getTgAccList2'
          }else if(["gm040201"].includes(cmdCode)){
            // 期货账户
            this.payeeApi = 'getQhAccList2'
          }else if(["gm040701","gm040706"].includes(cmdCode)){
            // 银行间债券账户-中债
            this.payeeApi = 'getYhjZzAccList2'
          }else if(["gm040703","gm040705"]){
            // 银行间债券账户-上清
            this.payeeApi = 'getYhjSqAccList2'
          }else if(["gm040203","gm040301","gm040401","gm040403","gm040501","gm040503","gm040601","gm040603"].includes(cmdCode)){
            // 其他账户
            this.payeeApi = 'getQtAccList2'
          }else{
            this.payeeApi = 'getQtAccList2'
          }

          if(["gm040102"].includes(cmdCode)){
            // 证券账户
            this.payerApi = 'getZqAccList2'
          }else if(["gm040101","gm040201","gm040203","gm040301","gm040401","gm040403","gm040501","gm040503","gm040601","gm040603","gm040701","gm040703"].includes(cmdCode)){
            // 托管账户
            this.payerApi = 'getTgAccList2'
          }else if(["gm040202"].includes(cmdCode)){
            // 期货账户
            this.payerApi = 'getQhAccList2'
          }else if(["gm040702","gm040705"].includes(cmdCode)){
            // 银行间债券账户-中债
            this.payerApi = 'getYhjZzAccList2'
          }else if(["gm040704","gm040706"]){
            // 银行间债券账户-上清
            this.payerApi = 'getYhjSqAccList2'
          }else if(["gm040302","gm040402","gm040502","gm040602"].includes(cmdCode)){
            // 其他账户
            this.payerApi = 'getQtAccList2'
          }else{
            this.payerApi = 'getQtAccList2'
          }
      }
      if(cmdType=="invest"){
        if(["gm050101","gm050102","gm050105","gm050107"].includes(cmdCode)){
          // 其他账户
          this.payeeApi = "getQtAccList2";
          this.payerApi = "getQtAccList2";
        }else if(["gm050106"].includes(cmdCode)){
          // 银行间债券账户
          this.payeeApi = "getYhjAccList2";
          this.payerApi = "getYhjAccList2";
        }else{
          this.payeeApi = "getQtAccList2";
          this.payerApi = "getQtAccList2";
        }
      }
      if(cmdType=="ta"){
        this.payeeApi = "getAllAccList";
        this.payerApi = "getAllAccList";
      }
      if(cmdType=="pay"){
        this.payeeApi = "getAllAccList";
        this.payerApi = "getAllAccList";
      }
      if(cmdType=="custom_demo"){
        this.payeeApi = "getAllAccList";
        this.payerApi = "getAllAccList";
      }
    },
    fundCodeChange(data) {
      this.fundCodeChangeNum++;
      console.log(data.fundCode);
      let fundCode = data.fundCode;
      if (fundCode) {
        let params = { fundCode: fundCode };
        let params1 = { productCode: fundCode };
        // this.getAccounts(params);
        // this.getAcc(params1);
        this.getAllAcc(params1);
      }
      if (this.fundCodeChangeNum > 1) {
        this.formData.payerAcconame = "";
        this.formData.payeeAcconame = "";
        if (
          ["gm040101", "gm040102", "gm040201", "gm040202", "gm040203"].includes(
            this.cmdCode
          )
        ) {
          this.formData.brokerCode = "";
        }
      }
      if (this.api && data) {
        this.getBrokers(fundCode, this.api);
      }
    },
    getAcc(params){
      this.getpayeeAcc(params);
      this.getpayerAcc(params);
    },
    getpayeeAcc(params){
      accountApi
        [this.payeeApi](params)
        .then(res=>{
          if(res.data.status==200){
            let data = res.data.data;
            this.$nextTick(()=>{
              this.$refs.selectAccount2.init(data);
            })
          }
        })
        .catch(()=>{

        })
    },
    getpayerAcc(params){
      accountApi
        [this.payerApi](params)
        .then(res=>{
          if(res.data.status==200){
            let data = res.data.data;
            this.$nextTick(()=>{
              this.$refs.selectAccount1.init(data);
            })
          }
        })
        .catch(()=>{

        })
    },
    getAllAcc(params){
      accountApi
        ["getAllAccList"](params)
        .then(res=>{
          if(res.data.status==200){
            let data = res.data.data;
            this.$nextTick(()=>{
              this.$refs.selectAccount1.init(data);
              this.$refs.selectAccount2.init(data);
            })
          }else{
            this.$nextTick(()=>{
              this.$refs.selectAccount1.init([]);
              this.$refs.selectAccount2.init([]);
            })
          }
        })
        .catch(()=>{

        })
    },
    getAccounts(params) {
      customApi
        .getAccounts(params)
        .then((res) => {
          if (res.data.status == 200) {
            // console.log(res.data.data.list);
            let data = res.data.data.list;
            this.$nextTick(() => {
              this.$refs.selectAccount1.init(data);
              this.$refs.selectAccount2.init(data);
            });
          }
        })
        .catch(() => {});
    },
    getBrokers(fundCode, api) {
      this.borkerInfos = [];
      let params = { fundCode };
      transferBizBeginApi[api](params).then((res) => {
        if (res.data.status == 200) {
          // console.log('borkerInfos',res);
          let arr = res.data.data;
          for (let i of arr) {
            let obj = {};
            obj.value =
              (i.openStruc || " 无 ") +
              (i.openExchange ? "( " + i.openExchange + " )" : "( 无 )");
            obj.name =
              (i.openStruc || " 无 ") +
              (i.openExchange ? "( " + i.openExchange + " )" : "( 无 )");
            this.borkerInfos.push(obj);
          }
        } else {
        }
      });
    },
    getAccountInfo1(val) {
      // console.log(val);
      this.formData.payerAccount = val.accoNo || "";
      this.formData.payerBank = val.accoBank || "";
    },
    getAccountInfo2(val) {
      // console.log(val);
      this.formData.payeeAccount = val.accoNo || "";
      this.formData.payeeBank = val.accoBank || "";
      this.formData.paymentSystemNumber = val.hvpsNo || "";
    },
    AccountInit() {
      this.$nextTick(() => {
        // this.$refs.selectAccount1.init([]);
        this.$refs.selectAccount2.init([]);
      });
    },
    save() {
      this.$refs["formData"].validate((valid) => {
        if (valid) {
          this.submitForm();
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    submitForm() {
      this.btn_loading = true;
      let params = {};
      params = commonFun.parameterSrc(this.formData);
      if (this.formData.fundCode) {
        params.fundCode = this.formData.fundCode.split("_")[0];
        params.fundName = this.formData.fundCode.split("_")[1];
      }
      if (
        this.formData.transferAmount &&
        this.formData.transferAmount.includes(",")
      ) {
        params.transferAmount = this.formData.transferAmount
          .toString()
          .replace(/,/gi, "");
      }
      if (this.formData.fundSalerName) {
        params.fundSalerName = this.formData.fundSalerName.split("|")[1];
        params.fundSaler = this.formData.fundSalerName.split("|")[0];
      }
      if (this.formData.depositBankName) {
        params.depositBankName = this.formData.depositBankName.split("|")[1];
        params.depositBank = this.formData.depositBankName.split("|")[0];
      }
      params.brokerName = this.formData.brokerCode || "";
      params = commonFun.parameterSrc(params);
      params.paymentSystemNumber = this.formData.paymentSystemNumber || "";
      params.processUse = this.formData.processUse || "";
      params.remark = this.formData.remark || "";

      // console.log(params);return
      let formData = new FormData();
      formData.append("id", this.id);
      for (let key in params) {
        formData.append(key, params[key]);
      }
      let oldfileArr = [];
      for (let i = 0; i < this.fileList.length; i++) {
        if (this.fileList[i].raw) {
          let aa = this.fileList[i].raw;
          formData.append("file", aa);
        }
        if (!this.fileList[i].raw) {
          let bb = this.fileList[i].id;
          oldfileArr.push(bb);
        }
      }
      formData.append("oldfile", oldfileArr);

      // console.log(this.$parent.$parent.$parent);
      // console.log(this.$parent.$parent.$parent.$parent);
      // return
      trackingAgentApi
        .saveFormData(formData)
        .then((res) => {
          if (res.data.status == 0 && res.data.message == "success") {
            this.$message({ type: "success", message: "保存成功！" });
            this.$bus.$emit('editFormData',JSON.parse(JSON.stringify(this.formData)));
            this.btn_loading = false;
            this.getpmList(this.taskId)
            this.$nextTick(() => {
              this.$parent.$parent.$parent.$parent.updateForm(this.id,true);
            });
          } else {
            this.$message({
              type: "error",
              message: res.data.message || "保存失败！",
            });
            this.btn_loading = false;
          }
        })
        .catch(() => {
          this.btn_loading = false;
        });
      // console.log(params);
      // console.log(this.fileList);
    },
    submitForm2(vals,status,confirmStatus) {
      this.btn_loading = true;
      let params = {};
      params = commonFun.parameterSrc(this.formData);
      if (this.formData.fundCode) {
        params.fundCode = this.formData.fundCode.split("_")[0];
        params.fundName = this.formData.fundCode.split("_")[1];
      }
      if (
        this.formData.transferAmount &&
        this.formData.transferAmount.includes(",")
      ) {
        params.transferAmount = this.formData.transferAmount
          .toString()
          .replace(/,/gi, "");
      }
      if (this.formData.fundSalerName) {
        params.fundSalerName = this.formData.fundSalerName.split("|")[1];
        params.fundSaler = this.formData.fundSalerName.split("|")[0];
      }
      if (this.formData.depositBankName) {
        params.depositBankName = this.formData.depositBankName.split("|")[1];
        params.depositBank = this.formData.depositBankName.split("|")[0];
      }
      params.brokerName = this.formData.brokerCode || "";
      params = commonFun.parameterSrc(params);
      params.paymentSystemNumber = this.formData.paymentSystemNumber || "";
      params.processUse = this.formData.processUse || "";
      params.remark = this.formData.remark || "";
      let formData = new FormData();
      formData.append("id", this.id);
      for (let key in params) {
        formData.append(key, params[key]);
      }
      let oldfileArr = [];
      for (let i = 0; i < this.fileList.length; i++) {
        if (this.fileList[i].raw) {
          let aa = this.fileList[i].raw;
          formData.append("file", aa);
        }
        if (!this.fileList[i].raw) {
          let bb = this.fileList[i].id;
          oldfileArr.push(bb);
        }
      }
      formData.append("oldfile", oldfileArr);

      // console.log(this.$parent.$parent.$parent);
      // console.log(this.$parent.$parent.$parent.$parent);
      // return
      trackingAgentApi
        .saveFormData(formData)
        .then((res) => {
          if (res.data.status == 0 && res.data.message == "success") {
            this.$message({ type: "success", message: "保存成功！" });
            this.$bus.$emit('editFormData',JSON.parse(JSON.stringify(this.formData)));
            this.btn_loading = false;
            this.getpmList(this.taskId)
            this.$nextTick(() => {
              this.$parent.$parent.$parent.$parent.updateForm(this.id,true);
            });
            this.$bus.$emit("tongyi",{vals,status,confirmStatus});
          } else {
            this.$message({
              type: "error",
              message: res.data.message || "保存失败！",
            });
            this.btn_loading = false;
          }
        })
        .catch(() => {
          this.btn_loading = false;
        });
      // console.log(params);
      // console.log(this.fileList);
    },
    // 账户校验
    getpmList(taskId){
      let params = {taskId}
      transferBizBeginApi.getpmList(params).then(res=>{
        if(res.data.status==200){
          if(res.data.data.rows.length){
            let arr = res.data.data.rows;
            this.warningArr = arr;
            arr.forEach(item=>{
              if(item.messageContent){
                this.$message({
                  type:"warning",
                  message:item.messageContent
                })
              }
            })
          }else{
            this.warningArr = []
          }
        }else{
          this.warningArr = []
        }
      }).catch(()=>{
        this.warningArr = []
      })
    },
    // 金额转换
    moneyFocus() {
      this.formDataRules.transferAmount[0].pattern = this.moneyValidateDefalut;
      if (
        this.formData.transferAmount &&
        this.formData.transferAmount.includes(",")
      ) {
        this.formData.transferAmount =
          this.formData.transferAmount.toString().replace(/,/gi, "") - 0;
      }
    },
    moneyBlur() {
      this.formDataRules.transferAmount[0].pattern = this.moneyValidateDefalut;
      let reg = this.moneyValidate.test(this.formData.transferAmount);
      if (reg && this.formData.transferAmount) {
        //失去焦点正则为true
        this.formDataRules.transferAmount[0].pattern = "";
        // this.dialogDataForm.money = moneyThousand(this.dialogDataForm.money)
        this.formData.transferAmount = fun.moneyYuan(
          this.formData.transferAmount
        );
        // this.$refs.dialogDataForm.validate()
      }
    },
    getNewData(){
      this.$bus.$emit("NewData",this.formData);
    },
  },
};
</script>

<style lang="scss">
.glrgb_edit_form {
  .el-form-item__content {
    min-width: 0 !important;
  }
  .warning_{
    color: red;
    .warning_message{
      text-align: center;
      margin: 8px;
    }
  }
  // .payerAcconame_{
  //   border: 1px solid red;
  // }
}
</style>
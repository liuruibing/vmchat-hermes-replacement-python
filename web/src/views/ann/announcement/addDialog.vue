<template>
  <div class="announcement_add">
    <el-form
      :model="formData"
      style="margin: 0 auto; width: 85% !important"
      ref="formData"
      :rules="formDataRules"
      label-width="100px"
      label-position="left"
      class="bitianxing"
    >
      <!-- <el-form-item label="产品" prop="fundCode">
        <multipleSelectTable
          class="multipleSelectTable"
          v-model="formData.fundCode"
          :data="fundList"
          :Columns="Columns"
          idField="fundCode"
          nameField="codeName"
          placeholder="请选择"
        ></multipleSelectTable>
      </el-form-item> -->
      <!-- <el-form-item label="报告类型" prop="reportType">
        <el-select v-model="formData.reportType" clearable placeholder="请选择" size="small" style="width:100%;" class="reportType_select">
          <el-option
            v-for="item in reportTypeArr"
            :key="item.dimCde"
            :label="item.dimNme"
            :value="item.dimCde"
          >
          </el-option>
        </el-select>
      </el-form-item> -->
      <el-form-item label="产品" prop="fundCode">
        <select-table
          v-model="formData.fundCode"
          :width="'100%'"
          @sendDataObj="sendDataObj"
        ></select-table>
      </el-form-item>
      <el-form-item label="报告类型" prop="checkedVals">
        <el-radio-group
          v-model="formData.checkedVals"
          class="margin_radio_label"
        >
          <el-radio
            v-for="item in reportTypeArr"
            :key="item.dimCde"
            :label="item.dimCde"
            >{{ item.dimNme }}</el-radio
          >
        </el-radio-group>
      </el-form-item>
      <el-form-item label="报告上报日期" prop="remark">
        <el-date-picker
          v-model="formData.remark"
          type="date"
          editable
          size="small"
          value-format="yyyy-MM-dd"
          placeholder="选择日期"
        >
        </el-date-picker>
      </el-form-item>
      <el-form-item
        label="备注"
        prop="cmdRemark"
        style="margin-top: 10px"
      >
        <!-- :autosize='{minRows: 2, maxRows: 10}' -->
        <el-input
          type="textarea"
          maxlength="1000"
          show-word-limit
          :autosize="{ minRows: 2 }"
          placeholder="请输入内容"
          v-model="formData.cmdRemark"
        >
        </el-input>
      </el-form-item>
      <el-form-item label="添加附件" prop="file">
        <el-upload
          class="upload-demo"
          v-model="fileList"
          ref="upload"
          name="file"
          :headers="hearders"
          :action="fileUploadUrl"
          :on-remove="onRemove"
          :on-change="onChange"
          :file-list="fileList"
          :auto-upload="false"
        >
          <el-button slot="trigger" size="small" type="primary">浏览</el-button>
        </el-upload>
      </el-form-item>
    </el-form>
    <div class="caozuoanniu">
      <el-button size="small" :loading="btn_loading" @click="closeDialog">取 消</el-button>
      <el-button
        type="primary"
        @click="submitFormV"
        size="small"
        :loading="btn_loading"
        >确 定</el-button
      >
    </div>
  </div>
</template>

<script>
import selectTable from "@/views/commonComponents/selectTable.vue";
import multipleSelectTable from "@/views/commonComponents/multiple-select-table2";
import bizBeginApi from "@/api/transfer/bizBegin";
import pageApi from "@/api/home/calendarList";
import synHandleApi from "@/api/conduct/newConduct.js"
import commonFun from "@/filters/new_common";
import commonApi from "@/api/common";
import modelFileValidate from "@/mixinsModel/file-validate";
import testVue from '../../reportCenter/test.vue';
export default {
  mixins: [modelFileValidate],
  components: {
    // multipleSelectTable,
    selectTable
  },
  data() {
    const validatorFile = (rule, value, callback) => {
      if (this.fileList.length > 0) {
        callback();
      } else {
        return callback(new Error("请选择附件"));
      }
    };
    return {
      Columns: [
        { label: "产品", prop: "codeName" },
        { label: "托管机构", prop: "trustorName" },
        { label: "基金服务机构", prop: "operatorName" },
      ],
      fundList: [],
      reportTypeArr:[
        {dimCde:"FA050010",dimNme:"公募基金合同生效公告"},
        {dimCde:"FC100050",dimNme:"公募基金经理变更公告"},
        {dimCde:"FC130050",dimNme:"公募非货币市场基金分红公告"},
        {dimCde:"FC190090",dimNme:"公募基金开放日常申购赎回转换定期定额投资业务公告"},
        {dimCde:"FC190100",dimNme:"公募基金暂停申购公告"},
        {dimCde:"FC190110",dimNme:"公募基金恢复申购公告"},
        {dimCde:"FC070030",dimNme:"公募基金管理人法定名称住所变更公告"},
        {dimCde:"FC100110",dimNme:"公募基金行业高级管理人员变更公告"},
        {dimCde:"FC110010",dimNme:"公募涉及基金管理人诉讼的公告"},
        {dimCde:"FC110040",dimNme:"公募涉及基金财产诉讼的公告"},
        {dimCde:"FC130060",dimNme:"公募货币市场基金收益支付公告"},
        {dimCde:"FC150010",dimNme:"公募基金份额净值计价错误公告"},
        {dimCde:"FC150030",dimNme:"公募货币市场基金偏离度公告"},
        {dimCde:"FC170010",dimNme:"基金改聘会计师事务所公告"},
        {dimCde:"FA010070",dimNme:"基金产品资料概要"},
        {dimCde:"FA010080",dimNme:"基金产品资料概要更新"},
      ],
      submitOrder:new Date().getTime(),
      formData: {
        fundCode:'',
        checkedVals:'',
        remark:'',
        cmdRemark:'',
      },
      hearders: { "Access-Control-Allow-Origin": "*" }, //上传头
      fileUploadUrl: "", //上传文件url
      fileList:[],
      formDataRules: {
        fundCode:{required:true,message:"请选择产品",trigger:"change"},
        checkedVals:{required:true,message:"请选择报告类型",trigger:"change"},
        remark:{required:true,message:"请选择报告上报日期",trigger:"change"},
        file: { validator: validatorFile, trigger: "change" },
      },
      btn_loading: false,
    };
  },
  mounted() {
    // this.getFundList(); // 产品多选数据
    this.getEdims('tempReport'); //报告类型
    //获取提交串submitOrder
    this.getSubmitOrder();
  },
  methods: {
    // 列表自适应高度
    fetTableHeight(){
      tableMethod.fetTableHeight(this,'transferTable');
    },
    getSubmitOrder() {
      pageApi
        .getSubmitOrder({})
        .then(({ data: res }) => {
          this.submitOrder = res.data || new Date().getTime();
        })
        .catch((err) => console.log("getSubmitOrder err", err));
    },
    // 字典值获取
    getEdims(val){
      commonApi.getEdims(val).then(res=>{
        if(res.data.status === 0 && res.data.message==="success"){
          if(val==='tempReport'){
            this.reportTypeArr = res.data.data;
          }
        }
      })
    },
    // 产品选择
    sendDataObj(data){
      if(data){

      }
    },
    // 产品多选数据
    getFundList() {
      bizBeginApi
        .getProductFund()
        .then(({ data: res }) => {
          if (res.status === 200) {
            let temp = [...res.data];
            for (let i of temp) {
              i["codeName"] = i.fundCode + "_" + i.fundName;
            }
            this.fundList = temp;
          } else this.$message.error("查询产品信息失败");
        })
        .catch((err) => {
          this.$message.error("查询产品信息失败");
        });
    },
    // 文件修改事件
    onChange(file, fileList) {
      this.fileValidate(file, fileList);
      this.$refs["formData"].validate((valid) => {});
    },
    // 文件移除事件
    onRemove(file, fileList) {
      this.onChange(file, fileList);
    },
    // 提交前表单校验
    submitFormV() {
      this.$refs["formData"].validate((valid) => {
        if (valid) {
          this.submitForm();
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    // 提交
    submitForm() {
      let params = JSON.parse(JSON.stringify(this.formData));
      if(params.fundCode){
        let arr = params.fundCode.split('_');
        params.fundCode = arr[0];
        params.fundName = arr[1];
      }
      if(params.checkedVals){
        params.checkedVals = [ params.checkedVals ];
      }
      params.wanderLocalStations = [];
      params.wanderRemoteStations = ["GTJA_R_00001"];
      params.cmdCode = "080111";
      let formData = new FormData();
      for (let i = 0; i < this.fileList.length; i++) {
        if (this.fileList[i].raw) {
          let raw = this.fileList[i].raw;
          formData.append("file", raw);
        }
      }
      let sendData = {};
      sendData.formData = params;
      let taskExcuteCmdMode = { taskExcuteCmdType: "Normal" };
      sendData.taskExcuteCmdMode = taskExcuteCmdMode;
      formData.append("datastr", JSON.stringify(sendData));
      formData.append("submitOrder", this.submitOrder);
      this.btn_loading = true;
      synHandleApi.addNewList(formData).then(res=>{
        this.btn_loading = false;
        if(res.data.status === 200){
          this.$message({
            type:"success",
            message:"提交成功"
          })
          this.$emit('close');
          this.$emit('refresh');
        }else{
          this.$message({
            type:"error",
            message:res.data.message || "提交失败"
          })
        }
      }).catch((err)=>{
        this.btn_loading = false;
      })
    },
    closeDialog(){
      this.$emit('close')
    }
  },
};
</script>

<style lang="scss" scoped>
.caozuoanniu {
  text-align: center;
}
</style>

<style lang="scss">
.announcement_add{
  .reportType_select{
    .el-input{
      width: 100% !important;
    }
  }
  .margin_radio_label{
    .el-radio{
      margin-top: 10px;
      margin-bottom: 10px;
      .el-radio__label{
        font-size: 14px !important;
      }
    }
  }
  // 表单 label文本左对齐（不包含*）
  .bitianxing{
    .el-form-item{position: relative;}
    .el-form-item.is-required:not(.is-no-asterisk) .el-form-item__label-wrap>.el-form-item__label:before, .el-form-item.is-required:not(.is-no-asterisk)>.el-form-item__label:before{
      position: absolute;
      left: -10px;
    }
  }
}
</style>
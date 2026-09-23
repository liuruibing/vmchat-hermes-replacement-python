<template>
  <div class="otherAccoutStyle">
    <div class="searchStyle">
      <el-row>
        <!-- formserch -->
        <el-col :span="16">
          <el-form :model="formInline" :inline="true" ref="formInline" label-position="right" size="small" @submit.native.prevent>
            <el-form-item label="产品" prop="fundCode">
              <select-table v-model="formInline.fundCode" @enter='onSubmit()'></select-table>
            </el-form-item>
          </el-form>
        </el-col>
        <el-col :span="8">
          <div style="text-align: right">
             <el-button
                  type="primary"
                  @click="onSubmit()"
                  size="small"><i class="el-icon-search"></i>查询
              </el-button>
              <el-button
                  type="primary"
                  plain
                  size="small"
                  @click="restForm()"><i class="el-icon-delete"></i>重置
              </el-button>
              <el-button
                  v-btn="'mjAccount.insert.info'"
                  type="primary"
                  plain
                  @click="addData()"
                  size="small"><i class="el-icon-circle-plus-outline"></i>新增
            </el-button>
          </div>
        </el-col>
      </el-row>
    </div>
    <!-- title -->
    <div class="forms_table_title">
      <i class="el-icon-s-data"></i>其他账户列表
    </div>
    <!-- teble -->
    <div>
      <el-table :data="tableData" border v-loading='tableLoading' stripe>
         <el-table-column prop="productCode" label="产品代码" align="left" header-align="center" show-overflow-tooltip min-width="100">
          <template slot-scope="scope">
            <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.productCode | noDataFilter }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="productName" label="产品名称" align="left" header-align="center" show-overflow-tooltip min-width="100">
          <template slot-scope="scope">
           <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.productName | noDataFilter }}</span>
          </template>
        </el-table-column>
       
        <el-table-column prop="companyName" label="公司名称" align="left" header-align="center" show-overflow-tooltip min-width="100">
          <template slot-scope="scope">
            <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.companyName | noDataFilter }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="accoName" label="账户名称" align="left" header-align="center" show-overflow-tooltip min-width="100">
          <template slot-scope="scope">
            <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.accoName | noDataFilter }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="accoNo" label="账户账号" align="left" header-align="center" show-overflow-tooltip min-width="100">
          <template slot-scope="scope">
            <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.accoNo | noDataFilter }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="accoBank" label="开户行" align="left" header-align="center" show-overflow-tooltip min-width="100">
          <template slot-scope="scope">
            <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.accoBank | noDataFilter }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="hvpsNo" label="大额支付系统号" align="left" header-align="center" show-overflow-tooltip min-width="100">
          <template slot-scope="scope">
            <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.hvpsNo | noDataFilter }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="mjType" label="其他账户" align="left" header-align="center" show-overflow-tooltip min-width="100">
          <template slot-scope="scope">
           <span :style="{'color':scope.row.approvalStatus=='0'?'red':''}">{{ scope.row.mjType | noDataFilter }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="操作"
          fixed="right"
          width="280"
          align="center">
          <template slot-scope="scope">
            <el-button style="width:52px;" 
              type="primary" 
              size="small" 
              v-if="scope.row.approvalStatus=='0'" 
              v-btn="'audit'"
              :loading="pass_loading"
              @click="check(scope.row)"
              >审 核</el-button
            >
            <el-button 
              type="primary" 
              size="small" 
              v-if="scope.row.approvalStatus=='1'" 
              v-btn="'audit'"
              :loading="pass_loading"
              @click="check_back(scope.row)"
              >反审核</el-button
            >
            <el-button type="primary" size="small" @click="searchData(scope.row)">查看详情</el-button>
            <el-button 
              v-if="scope.row.approvalStatus=='1'?false:true"
              type="primary" 
              size="small" 
              @click="editData(scope.row)">编辑</el-button>
            <el-button 
              v-if="scope.row.approvalStatus=='1'?false:true" 
              type="danger" 
              plain 
              size="small"
              @click="delData(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <Pagination
      :total="total"
      :page="formInline.pageNum"
      :limit="formInline.pageSize"
      @pagination="Pagination"
    ></Pagination>
    </div>
    <!-- dialog  -->
    <!-- v-if="refashDialog" -->
    <div class="otherDialog">
      <el-dialog
        :title="titleName"
        :visible.sync="dialogVisible"
        center
        @closed='closedDialog'
        custom-class="customClass"
        :close-on-click-modal='false'>
        <el-form :model="dialogForm" ref="dialogForm" :rules="dialogRules" label-position="right" label-width="150px">
          <el-row :gutter="2">
            <el-col :span='12'>
              <el-form-item label="其他账户" prop="mjType">
                <el-input v-model.trim="dialogForm.mjType" placeholder="其他账户" maxlength="30" :disabled='isViewInfo'></el-input>
              </el-form-item>
              <!-- <el-form-item label="产品" prop="productId" v-if="titleName=='编辑'">
                 <select-table v-model="dialogForm.productId" @sendDataObj='dataObj' v-show="!isViewInfo"></select-table>
                 <el-input v-model="dialogForm.productId" disabled v-show="isViewInfo"></el-input>
              </el-form-item> -->
              <el-form-item label="产品" prop="fundCodes">
                <multipleSelectTable
                  v-show="!isViewInfo"
                  v-model="dialogForm.fundCodes"
                  :data="fundList"
                  :Columns="Columns"
                  idField="codeName"
                  nameField="codeName"
                  placeholder="请选择"
                ></multipleSelectTable>
                <el-input v-model="dialogForm.productId" disabled v-show="isViewInfo"></el-input>
              </el-form-item>
              <el-form-item label="账户名称" prop="accoName">
                <el-input v-model.trim="dialogForm.accoName" maxlength="66" :disabled='isViewInfo'></el-input>
              </el-form-item>
              <el-form-item label="大额支付系统号" prop="hvpsNo">
                <el-input v-model.trim="dialogForm.hvpsNo" maxlength="66" :disabled='isViewInfo'></el-input>
              </el-form-item>
            </el-col>
            <el-col :span='12'>
              <el-form-item label="开户行" prop="accoBank">
                <el-input v-model.trim="dialogForm.accoBank" maxlength="66" :disabled='isViewInfo'></el-input>
              </el-form-item>
              <el-form-item style="visibility:hidden;" label="产品代码" prop="productCode">
                <el-input v-model.trim="dialogForm.productCode" maxlength="100" disabled></el-input>
              </el-form-item>
              <el-form-item label="账户账号" prop="accoNo">
                <el-input v-model.trim="dialogForm.accoNo" maxlength="66" :disabled='isViewInfo'></el-input>
              </el-form-item>
              <el-form-item label="公司名称" prop="companyName">
                <el-input v-model.trim="dialogForm.companyName" maxlength="66" :disabled='isViewInfo'></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-form-item label="备注" prop="remark">
            <el-input
              :disabled='isViewInfo'
              type="textarea"
              maxlength="1000"
              show-word-limit
              v-model="dialogForm.remark"
              :autosize="{minRows: 3}">
           </el-input>
          </el-form-item>
          <el-form-item label="账户资料上传" prop="file">
              <el-upload
                :disabled='isViewInfo'
                style="width: 480px"
                class="upload-demo"
                ref="upload"
                :headers="hearders"
                :action="fileUploadUrl"
                :on-preview="downFile"
                :on-success="handleSuccess"
                :on-change="handleChange"
                :on-remove="onRemove"
                :file-list="fileList"
                :auto-upload="false">
               <el-button slot="trigger" type="primary" v-show="!isViewInfo">浏览</el-button>
              </el-upload>
            </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false" size="small" :disabled='submitLoading'>取 消</el-button>
          <el-button type="primary" @click="submitFormData" :loading="submitLoading" size="small" v-if="!isViewInfo">提 交</el-button>
        </span>
      </el-dialog>
    </div>
  </div>
</template>
<script>
import bizBeginApi from '@/api/transfer/bizBegin'
import multipleSelectTable from "@/views/commonComponents/multiple-select-table2";
import selectTable from '@/views/commonComponents/selectTable.vue';
import Pagination from "@/components/Pagination";
import commonFun from "@/filters/new_common";
import commonApi from "@/api/common";
import { FILE_URL } from "@/utils/request";
import { getToken } from "@/utils/auth";
import pageApi from "@/api/product/mjAccount";
import { ecmRules } from "@/api/product/cemJudge";
import modelFileValidate from '@/mixinsModel/file-validate'
export default {
  mixins: [modelFileValidate],
  components: { Pagination, selectTable, multipleSelectTable },
  computed: {
    dialogRules () {
      return {
        mjType: [
          {
            required: false,
            type: "string",
            trigger: "change",
            // pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入其他账户",
          }
        ],
        productId: [
          { required: true, message: "请选择产品", trigger: "change",}
        ],
        accoName: [
          {
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message: this.$regularValidator.empty().msg,
          },
          { required: true, trigger: "blur", message: "请填写账户名称"}
        ],
        accoNo: [
          {
            type: "string",
            trigger: "change",
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母或者数字",
          },
          { required: true, trigger: "blur", message: "请填写账户账号"}
        ],
        accoBank: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: this.$regularValidator.empty().reg,
            message: this.$regularValidator.empty().msg,
          }
        ],
        hvpsNo: [
          {
            required: false,
            type: "string",
            trigger: "change",
            pattern: /^[a-zA-Z0-9]+$/,
            message: "请输入字母或者数字",
          }
        ],
        fundCodes:[
          { required: true, message: "请选择产品", trigger: "change",}
        ]
      }
    }
  },
  mounted () {
    this.getFundList();
   this.onSubmit()
  },
  data () {
    return {
      hearders: {
        Authorization: "vXcx3IBemn1kShhobK2DfpY3kFqiBaSb",
        "Access-Control-Allow-Origin": "*",
      }, //上传头
      fileList: [], //文件列表
      fileUploadUrl: "", //上传文件url
      // --------------------
      dialogVisible: false,
      total: 0,
      isViewInfo: false,
      submitLoading: false,
      tableLoading: false,
      removeFile: false,
      refashDialog: false,
      rmoveFileId: [],
      titleName: '新增',
      formInline: {
        accoType: 'other',
        fundCode: '',
        pageSize: 50,
        pageNum: 1
      },
      fundList:[],
      Columns: [
        { label: "产品", prop: "codeName" },
        { label: "托管机构", prop: "trustorName" },
        { label: "基金服务机构", prop: "operatorName" },
      ],
      tableData: [],
      pass_loading:false,
      accountCodes: [],
      dialogForm: {
        fundCodes: [],
        id: '',
        productName: '',
        accoType: 'other',
        mjType: '',
        accoBank: '',
        productId: '',
        accoName: '',
        productCode: '',
        accoNo: '',
        companyName: '',
        remark:'',
        hvpsNo:''
      }
    }
  },
  methods: {
    getFundList(){
      bizBeginApi.getProductFund().then(({ data: res }) =>{
        if(res.status === 200){
          let temp = [...res.data]
          for (let i of temp) { i['codeName'] = i.fundCode + "_"+ i.fundName }
          this.fundList = temp
        } else this.$message.error('查询产品信息失败');
      }).catch((err) => { this.$message.error('查询产品信息失败') })
    },
    dataObj (data) {
      if(data){
        this.dialogForm.productCode = data.fundCode
        this.dialogForm.productName = data.fundName
      }else{
        this.dialogForm.productCode = ''
        this.dialogForm.productName = ''
      }
    },
    onSubmit () {
      this.tableLoading = true
      this.dialogVisible = false
      let data = { ...this.formInline }
      if (this.formInline.fundCode) data.fundCode = this.formInline.fundCode.split('_')[0]
      let params = commonFun.parameterSrc(data);
      pageApi.getDataSourceList(params).then((response) => {
          if (response.data.status === 200) {
            this.tableData = response.data.data.list;
            // 页面总条数
            this.total = response.data.data.total;
          } else {
            this.tableData = [];
            this.total = 0;
            this.formInline.pageSize = 50;
            this.formInline.pageNum = 1;
          }
          this.tableLoading = false;
        }).catch(() => {
          this.tableData = [];
          this.total = 0;
          this.formInline.pageSize = 50;
          this.formInline.pageNum = 1;
          this.tableLoading = false;
        })
    },
    restForm() {
      this.$nextTick(() => {
        this.$refs.formInline.resetFields()
      })
    },
    addData () {
      this.dialogVisible = true
      this.titleName = '新增'
      this.refashDialog = true
      this.$nextTick(() => {
        for(let i in this.dialogForm){
          if(i!='fundCodes'){
            this.dialogForm[i] = ''
          }
        }
        this.$set(this.dialogForm,'fundCodes',[])
        this.dialogForm.accoType = 'other'
        this.$refs.dialogForm.clearValidate()
        this.getProductsAll()
      })
    },
    getProductsAll () {
      commonApi.getProductsAll().then((res) => {
          if (res.data.message === "success") {
            let arr = res.data.data;
            this.accountCodes = [];
            for (let i = 0; i < arr.length; i++) {
              let obj = {}
              obj.value = arr[i].fundCode
              obj.name = arr[i].fundName + " (" + arr[i].fundCode + ")"
              this.accountCodes.push(obj)
            }
          }
        }).catch(() => {});
    },
    changeValue (val) {
      this.dialogForm.productCode = val
    },
    closedDialog () {
      this.isViewInfo = false
      this.fileList = []
      for(let i in this.dialogForm) this.dialogForm[i] = ''
      this.dialogForm.fundCodes = []
      this.dialogForm.accoType = 'other'
      this.refashDialog = false
      this.$refs.dialogForm.clearValidate()
    },
    searchData (row) {
      this.titleName = '详情'
      this.isViewInfo = true
      this.dialogVisible = true
      this.refashDialog = true
      this.$nextTick(() => {
        for (let i in this.dialogForm) {
          if (row[i]) this.dialogForm[i] = row[i]
          else this.dialogForm[i] = ''
        }
        this.dialogForm['productId'] = row.productCode+'_'+row.productName
        this.dialogForm.fundCodes = [row.productCode+'_'+row.productName]
        this.getFileList(row.id, "qtzh_file");
      })
    },
    editData (row) {
      this.dialogVisible = true
      this.isViewInfo = false
      this.titleName = '编辑'
      this.refashDialog = true
      this.$nextTick(() => {
        for (let i in this.dialogForm) {
          if (row[i]) this.dialogForm[i] = row[i]
          else this.dialogForm[i] = ''
        }
        this.dialogForm.fundCodes = [row.productCode+'_'+row.productName]
        this.dialogForm['productId'] = row.productCode+'_'+row.productName
        this.getFileList(row.id, "qtzh_file");
      })
    },
    //分页
    Pagination(val) {
      this.formInline.pageSize = val.limit; //页面条数
      this.formInline.pageNum = val.page; //页面
      this.onSubmit();
    },
    submitFormData () {
      this.$message.closeAll();
      this.$refs["dialogForm"].validate((valid) => {
        if (valid) {
          if (!this.dialogForm.id) {
            // 添加
            this.saveData();
          } else {
            // 修改
            this.updateParamSet();
          }
        }
      });
    },
    saveData() {
      this.$confirm("确定新增?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).then(() => {
          let formData = new FormData(); //  用FormData存放上传文件
          this.submitLoading = true;
          let data = { ...this.dialogForm }
          data['productId'] = data.productCode
          delete data.productId
          delete data.productCode
          delete data.productName
          // console.log(data);
          // this.submitLoading = false;
          // return
          for (let i in data) {
            if (data[i]) {
              formData.append( i, data[i]);
            }
          }
          if (this.fileList.length > 0) {
            for (let i = 0; i < this.fileList.length; i++) {
              let fileCur = this.fileList[i].raw;
              if (fileCur) {
                formData.append("files", fileCur);
              }
            }
            formData.append("relaType", "qtzh_file");
          }
          pageApi.addDataSource(formData).then((response) => {
              if (response.data.status === 200) {
                // 关闭移动指标弹框
                this.$message({
                  message: "新增成功",
                  type: "success",
                });
                // 刷新列表
                this.onSubmit();
              } else {
                this.$message({
                  message: response.data.message || "新增失败",
                  type: "warning",
                })
              }
              this.submitLoading = false;
            }).catch(() => {})
        }).catch(() => {
          this.$message.info('已取消')
          this.submitLoading = false;
        });
    },
    updateParamSet() {
      this.$confirm("确定修改?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).then(() => {
          this.submitLoading = true;
          let formData = new FormData(); //  用FormData存放上传文件
          let data = { ...this.dialogForm }
          data['productId'] = data.productCode
          delete data.productId
          delete data.productCode
          delete data.productName
          for (let i in data) {
            if (data[i]) {
              formData.append( i, data[i]);
            }
          }
          if (this.fileList.length > 0) {
            let fileIds = []
            for(let i=0;i< this.fileList.length;i++){
              if(this.fileList[i].raw){
                let aa = this.fileList[i].raw;
                formData.append('files', aa);
              }
              if(this.fileList[i].id){
                let bb = this.fileList[i].id;
                fileIds.push(bb);
              }
            }
            formData.append("fileIds", fileIds);
            formData.append("relaType", "qtzh_file");
          }
          pageApi.updateDataSource(formData).then((response) => {
              if (response.data.status === 200) {
                // 关闭移动指标弹框
                this.$message({
                  message: "修改成功",
                  type: "success",
                });
                this.onSubmit();
                this.removeFiles()
              } else {
                // 关闭移动指标弹框
                this.$message({
                  message: response.data.message || "修改失败",
                  type: "warning",
                })
              }
              this.submitLoading = false;
            })
            .catch(() => {
              this.submitLoading = false;
              this.$message({
                message: "修改失败",
                type: "warning",
              });
            });
        }).catch(() => {
           this.$message.info('已取消')
           this.submitLoading = false;
        })
    },
   removeFiles() {
      let temp = []
      for (let i of this.fileList) {
        if (i.id) temp.push(i)
      }
      this.rmoveFileId.forEach(item => {
        let flag = false
        temp.forEach(item2 => {
          if (item.id == item2.id) flag = true
        })
        if (!flag) this.removeFileIDS(item.id)
      })
    },
    removeFileIDS(id) {
      commonApi
        .delFileList(id)
        .then((res) => {
          if (res.data.message === "success") {
          } else {
            this.$message.closeAll();
            this.$message.error("删除失败");
          }
        })
        .catch(() => {
          this.$message.closeAll();
          this.$message.error("删除失败");
        });
    },
    // 行删除数据
    delData(row) {
      this.$message.closeAll();
      this.$confirm("确定删除?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).then(() => {
          let params = {};
          params["id"] = row.id;
          pageApi.deleteDataSource(params).then((response) => {
              if (response.data.status === 200) {
                this.$message({
                  message: "删除成功",
                  type: "success",
                });
                // 刷新树列表
                this.onSubmit();
              } else {
                this.$message({
                  message: response.data.message || "删除失败",
                  type: "warning",
                });
              }
            }).catch(() => {});
        }).catch(() => {})
    },
    // ---------
    downFile(file) {
      if (file.id) {
        let params = {};
        params.id = file.id;
        params = commonFun.parameterSrc(params);
        if (this.$store.getters.token) {
          params["token"] = this.$store.getters.token;
        }
        let action = this.$store.state.setting.baseApi + "api/file/v1.0/downloadFile";
        commonFun.formDownloadFile(params, action, "GET");
      }
    },
    //上传文件成功事件
    handleSuccess(res, file, fileList) {
      this.$message.closeAll()
      if (res.message === "success") {
        this.countDialog = false;
        this.$message({
          message: "操作成功",
          type: "success",
        });
        // 刷新列表
        this.onSubmit();
      } else {
        this.$message.error("文件上传失败");
        this.fileList = [];
      }
      // this.submit_btn = false; //按钮启用
    },
    onRemove (file, filelist) {
      this.removeFile = true
      this.handleChange(file, filelist)
    },
    //文件修改事件
    handleChange(file, filelist) {
      this.fileValidate(file, filelist)
      this.removeFile = false
    },
    //获取FileList并打开dialog
    getFileList(relaId, relaType) {
      commonApi.getFileList(relaId, relaType).then((res) => {
          if (res.data.message === "success") {
            let arr = res.data.data;
            this.fileList = [];
            for (let i = 0; i < arr.length; i++) {
              let obj = {};
              obj.id = arr[i].id;
              obj.url = arr[i].fileUri;
              obj.name = arr[i].fileName;
              obj.size = arr[i].fileSize;
              this.fileList.push(obj);
            }
            this.rmoveFileId = [ ...this.fileList ]
          } else {
            this.fileList = []
            this.rmoveFileId = []
            this.$message.error("查询详情附件信息失败");
          }
        }).catch(() => {})
    },
    // 审核
    check(row){
      let params = {
        id:row.id
      }
      this.pass_loading = true;
      pageApi.pass(params).then(res=>{
        this.pass_loading = false;
        if(res.data.status===200){
          this.$message({
            type:"success",
            message:"审核成功"
          })
          this.onSubmit(false);
        }else{
          this.$message({
            type:"error",
            message: res.data.message || "审核失败"
          })
        }
      }).catch(()=>{
        this.pass_loading = false;
      })
    },
    // 反审核
    check_back(row){
      let params = {
        id:row.id
      }
      this.pass_loading = true;
      pageApi.unpass(params).then(res=>{
        this.pass_loading = false;
        if(res.data.status===200){
          this.$message({
            type:"success",
            message:"反审核成功"
          })
          this.onSubmit(false);
        }else{
          this.$message({
            type:"error",
            message: res.data.message || "反审核失败"
          })
        }
      }).catch(()=>{
        this.pass_loading = false;
      })
    },
  }
}
</script>
<style lang='scss'>
.otherAccoutStyle {
  .customClass {
    width: 60% !important;
  }
}
</style>
<template>
  <div class="qt_form" v-loading='qt_form_loading'>
    <div v-if="none_show"><span>未找到当前产品的账户信息。</span></div>
    <div class="forms_table_title" v-if="table_show">
      <i class="el-icon-s-data"></i>其他账户列表
    </div>
     <el-table :data="tableData" border v-loading='tableLoading' v-if="table_show" stripe>
         <el-table-column prop="productCode" label="产品代码" align="left" header-align="center" show-overflow-tooltip min-width="100">
          <template slot-scope="scope">
            <span>{{ scope.row.productCode | noDataFilter }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="productName" label="产品名称" align="left" header-align="center" show-overflow-tooltip min-width="100">
          <template slot-scope="scope">
           <span>{{ scope.row.productName | noDataFilter }}</span>
          </template>
        </el-table-column>
       
        <el-table-column prop="companyName" label="公司名称" align="left" header-align="center" show-overflow-tooltip min-width="100">
          <template slot-scope="scope">
            <span>{{ scope.row.companyName | noDataFilter }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="accoName" label="账户名称" align="left" header-align="center" show-overflow-tooltip min-width="100">
          <template slot-scope="scope">
            <span>{{ scope.row.accoName | noDataFilter }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="accoNo" label="账户账号" align="left" header-align="center" show-overflow-tooltip min-width="100">
          <template slot-scope="scope">
            <span>{{ scope.row.accoNo | noDataFilter }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="accoBank" label="开户行" align="left" header-align="center" show-overflow-tooltip min-width="100">
          <template slot-scope="scope">
            <span>{{ scope.row.accoBank | noDataFilter }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="hvpsNo" label="大额支付系统号" align="left" header-align="center" show-overflow-tooltip min-width="100">
          <template slot-scope="scope">
            <span>{{ scope.row.hvpsNo | noDataFilter }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="mjType" label="其他账户" align="left" header-align="center" show-overflow-tooltip min-width="100">
          <template slot-scope="scope">
           <span>{{ scope.row.mjType | noDataFilter }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="操作"
          fixed="right"
          min-width="100"
          align="center">
          <template slot-scope="scope">
            <el-button type="primary" size="small" @click="searchData(scope.row)">查看详情</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div v-if="form_show && !preview_show">
        <div style="overflow: hidden;padding: 15px;">
          <span @click="close_form" style="font-size: 20px;float: right;cursor: pointer;"><i class="el-icon-close"></i></span>
        </div>
        <el-form :model="dialogForm" ref="dialogForm" label-position="right" label-width="150px">
          <el-row :gutter="2">
            <el-col :span='12'>
              <el-form-item label="其他账户" prop="mjType">
                <el-input v-model="dialogForm.mjType" placeholder="其他账户" maxlength="30" :disabled='isViewInfo'></el-input>
              </el-form-item>
              <el-form-item label="产品名称" prop="productId">
                 <!-- <select-table v-model="dialogForm.productId" @sendDataObj='dataObj' v-show="!isViewInfo"></select-table> -->
                 <el-input v-model="dialogForm.productId" disabled v-show="isViewInfo"></el-input>
              </el-form-item>
              <el-form-item label="账户名称" prop="accoName">
                <el-input v-model="dialogForm.accoName" maxlength="66" :disabled='isViewInfo'></el-input>
              </el-form-item>
              <el-form-item label="大额支付系统号" prop="hvpsNo">
                <el-input v-model="dialogForm.hvpsNo" maxlength="66" :disabled='isViewInfo'></el-input>
              </el-form-item>
            </el-col>
            <el-col :span='12'>
              <el-form-item label="开户行" prop="accoBank">
                <el-input v-model="dialogForm.accoBank" maxlength="30" :disabled='isViewInfo'></el-input>
              </el-form-item>
              <el-form-item label="产品代码" prop="productCode">
                <el-input v-model="dialogForm.productCode" maxlength="100" disabled></el-input>
              </el-form-item>
              <el-form-item label="账户账号" prop="accoNo">
                <el-input v-model="dialogForm.accoNo" maxlength="66" :disabled='isViewInfo'></el-input>
              </el-form-item>
              <el-form-item label="公司名称" prop="companyName">
                <el-input v-model="dialogForm.companyName" maxlength="66" :disabled='isViewInfo'></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-form-item label="备注" prop="remark">
            <el-input
              :disabled='isViewInfo'
              type="textarea"
              maxlength="1000"
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
                :file-list="fileList"
                :auto-upload="false">
               <el-button slot="trigger" type="primary" v-show="!isViewInfo">浏览</el-button>
              </el-upload>
            </el-form-item>
        </el-form>
      </div>
      <div v-if="preview_show" style="height:100%;padding: 0 20px">
      <p class="yulan_title"> <span class="yulan_title_name">附件预览</span><span style="font-size:20px;color:#000;cursor: pointer;"><i @click="closePreview" class="el-icon-close"></i></span> </p>
      <PdfPreview :urlArr='fileList' :PreviewFileId="PreviewFileId" style="width:100%;height:100%" ref="PdfPreview"></PdfPreview>
    </div>
  </div>
</template>

<script>
import PdfPreview from '@/components/PdfPreview'
import pageApi from "@/api/product/mjAccount";
import commonApi from "@/api/common";
export default {
  components:{PdfPreview},
  data(){
    return{
      isViewInfo:true,
      tableLoading:false,
      table_show:false,
      form_show:false,
      none_show:false,
      tableData:[],
      dialogForm: {
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
      },
      hearders:{},
      fileUploadUrl:"",
      fileList:[],
      qt_form_loading:false,
      preview_show:false,
      PreviewFileId:''
    }
  },
  methods:{
    init(val){
      this.preview_show = false;
      this.form_show = false;
      this.qt_form_loading = true;
      this.getTableList(val);
    },
    getTableList(data){
      this.tableData = [];
      this.tableLoading = true;
      let fundCode = data;
      let params = {
        accoType:'other',
        fundCode:fundCode,
        pageSize: 500,
        pageNum: 1,
      }
      pageApi
          .getDataSourceList(params)
          .then((response) => {
            this.qt_form_loading = false;
            if (response.data.status === 200) {
              this.tableData = response.data.data.list;
              if(this.tableData.length){
                this.table_show = true;
                this.none_show = false;
              }else{
                this.table_show = false;
                this.none_show = true;
              }
            } else {
              this.tableData = [];
              this.table_show = false;
            }
            this.tableLoading = false;
          })
          .catch(() => {
            this.tableData = [];
            this.tableLoading = false;
            this.table_show = false;
            this.qt_form_loading = false;
          });
    },
    searchData(row){
      this.table_show = false;
      this.form_show = true;
      this.getFileList(row.id, "qtzh_file");
      for (let i in this.dialogForm) {
          if (row[i]) this.dialogForm[i] = row[i]
          else this.dialogForm[i] = ''
        }
      this.dialogForm['productId'] = row['productName']
    },
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
            // this.rmoveFileId = [ ...this.fileList ]
          } else {
            this.fileList = []
            // this.rmoveFileId = []
            this.$message.error("查询详情附件信息失败");
          }
        }).catch(() => {})
    },
    close_form(){
      this.table_show = true;
      this.form_show = false;
    },
    closePreview(){
      this.preview_show = false;
      this.$notify.closeAll();
    },
    downFile(file) {
      if(file.id){
        this.PreviewFileId = file.id;
        this.preview_show=true;
      }
    },
  }
}
</script>

<style lang="scss">
  .qt_form{
    // min-height: 50px;
    height: 100%;
    .el-form-item__content{
      min-width: 0 !important;
    }
  }
</style>
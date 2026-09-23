<template>
  <div class="fundFilePage">
    <!-- 搜索 -->
    <el-form
      :inline="true"
      ref="formQuery"
      :model="formQuery"
      :rules="rules"
      class="formQuery pdt5"
    >
      <el-row>
        <el-col :span="16">
          <div class="grid-content bg-purple">
            <el-form-item prop="beginDate">
              <span slot="label" class="el-date-picker-title" >日期</span>
              <el-date-picker
                v-model="formQuery.beginDate"
                value-format="yyyy-MM-dd"
                size="small"
              ></el-date-picker>
            </el-form-item>
            <el-form-item>
              <span>-</span>
            </el-form-item>
            <el-form-item prop="endDate">
              <el-date-picker
                v-model="formQuery.endDate"
                value-format="yyyy-MM-dd"
                size="small"
              ></el-date-picker>
            </el-form-item>
            <el-form-item label="" prop="vcType" class="mb20">
              <span class="item-label" slot="label">附件类型</span>
              <el-select  v-model="formQuery.vcType" multiple placeholder="请选择" >
                <template v-for="(item, index) in fileTypeList">
                  <el-option :key="index" :label="item.dimNme" :value="item.dimCde"></el-option>
                </template>
              </el-select>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="grid-content bg-purple-light">
            <el-form-item class="search_button_com">
              <el-button type="primary" icon="el-icon-plus" :disabled="fundData.isView" class="mb5" @click="insertDialog()">新增</el-button>
              <el-button
                type="primary"
                :disabled="btnDisabled"
                @click="onQuery(1)"
                class="mb5"
                icon="el-icon-search"
              >查询</el-button>
              <el-button type="primary" class="mb5"  @click="logDialog()">日志</el-button>
              <el-button class="mb5" plain  @click="resetForm('formQuery')">重置</el-button>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
    </el-form>
    <el-row>
      <el-col :span="10">
        <div class="picc_forms_table_title">
          <div class="picc_forms_table_title_line"></div>
          <div>附件列表</div>
        </div>
      </el-col>
    </el-row>
    <el-row>
      <el-col>
        <el-table
          :data="tableData"
          border
          @sort-change="handleSortChange"
          v-loading="tableLoading"
          :header-row-style="this.$fun.headerRowStyle"
          :cell-style="this.$fun.cellStyle"
          style="width: 100%"
        >
          <el-table-column
            type="index"
            show-overflow-tooltip
            label="序号"
            min-width="100"
            header-align="center"
          ></el-table-column>
          <el-table-column
            prop="fileName"
            sortable="custom"
            :sort-orders="['ascending', 'descending']"
            show-overflow-tooltip
            label="文件名称"
            min-width="120"
            header-align="center"
          ></el-table-column>
          <el-table-column
            prop="typeName"
            sortable="custom"
            :sort-orders="['ascending', 'descending']"
            show-overflow-tooltip
            label="附件类型"
            min-width="80"
            header-align="center"
          ></el-table-column>
          <el-table-column
            prop="creatorName"
            sortable="custom"
            :sort-orders="['ascending', 'descending']"
            show-overflow-tooltip
            label="上传人"
            min-width="100"
            header-align="center"
          ></el-table-column>
          <el-table-column
            prop="createTime"
            sortable="custom"
            :sort-orders="['ascending', 'descending']"
            show-overflow-tooltip
            label="上传时间"
            min-width="100"
            header-align="center"
          ></el-table-column>
          <el-table-column label="操作"  min-width="140" align="center">
            <template slot-scope="scope">
              <el-button type="primary" size="small" :disabled="fundData.isView" @click="updateDialog(scope.row)">编辑</el-button>
              <el-button type="primary" size="small" :disabled="fundData.isView" @click="deleteFile(scope.row)">删除</el-button>
              <el-button type="primary" size="small" :disabled="fundData.isView" @click="downloadFile(scope.row)">下载</el-button>
            </template>
          </el-table-column>
        </el-table>
        <Pagination
          :total="total"
          :limit="formQuery.pageSize"
          :page="formQuery.pageNum"
          @pagination="pagination"
        ></Pagination>
      </el-col>
    </el-row>

    <el-dialog title="附件信息" center :visible.sync="dialogMask" :append-to-body="appendToBody" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox">
          <div class="forms_management_box">
            <el-form :inline="true" ref="formDialog" :model="formDialog" >
              <el-form-item label="" prop="fileName" class="mb20">
                <span class="item-label" slot="label">附件名称</span>
                <el-input
                  v-model.trim="formDialog.fileName"
                  clearable
                  placeholder="请输入"
                  size="small"
                ></el-input>
              </el-form-item>
              <el-form-item label="" prop="vcType" class="mb20">
                <span class="item-label" slot="label">附件类型</span>
                <el-select  v-model="formDialog.vcType"  placeholder="请选择" size="small">
                  <template v-for="(item, index) in fileTypeList">
                    <el-option :key="index" :label="item.dimNme" :value="item.dimCde"></el-option>
                  </template>
                </el-select>
              </el-form-item>
            </el-form>
          </div>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-upload
          :file-list="formFile.fileList"
          class="upload-demo"
          :action="fileUrl"
          :headers="headersParams"
          accept=".xls,.xlsx,.pdf,.doc,.docx"
          :before-upload="beforeUpload"
          :on-success="handleSuccess"
          :on-error="handleError"
          :auto-upload="false"
          ref="upload"
        >
          <el-button v-if="uploadFlag" slot="trigger" size="small" type="primary">选取文件</el-button>
          <el-button v-if="uploadFlag" style="margin-left: 10px;" size="small" :loading="uploading" type="success" @click="submitUpload">上传到服务器</el-button>
        </el-upload>
        <el-button v-if="updateFlag" type="primary" size="small" :loading="uploading2" @click="dealData()">保存</el-button>
      </div>
    </el-dialog>
    <el-dialog title="日志列表" center :visible.sync="logDialogMask" :append-to-body="appendToBody" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox">
          <div class="forms_management_box">
            <el-timeline  :reverse="reverse">
              <el-timeline-item
                v-for="(activity, index) in logList"
                :key="index"
                :timestamp="activity.createTime">
                {{activity.logMsg}}
              </el-timeline-item>
            </el-timeline>
          </div>
        </el-main>
      </el-container>
    </el-dialog>
  </div>

</template>

<script type="text/ecmascript-6">
import { FILE_URL } from '@/utils/request'
import Pagination from "@/components/NewPagination";
import commonApi from "@/api/common";
import fundFileApi from "@/api/dataManage/fundFile";
import { getToken } from '@/utils/auth'

export default {
  components: {
    Pagination
  },
  name: "fundFilePage",
  props:{
    fundData:{
      fundCode:'',
      isView:false,
    }
  },
  data() {
    return {
      // 查询参数
      formQuery: {
        beginDate:"",
        endDate:"",
        //附件类型
        vcType:[],
        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10,
        //排序方式
        orderBy : ""
      },
      formDialog:{
        fId:"",
        //文件名称
        fileName:"",
        //文件类型
        vcType:""
      },
      //文件类型下拉
      fileTypeList:[],
      // 验证规则
      rules: {
      },
      formFile:{
        //文件
        fileList:[]
      },
      // 上传地址
      fileUrl : '',
      uploading : false,
      uploading2 : false,

      uploadFlag:false,
      updateFlag:false,

      //日志数据
      logList:[],
      reverse:true,

      // 上传头部
      headersParams: {},
      appendToBody:true,

      //附件串口开关
      dialogMask:false,

      //日志窗口开关
      logDialogMask:false,

      modifyType:"",

      //列表数据
      tableData:[],
      //总条数
      total: 0,
      // 表格loading
      tableLoading: false,
      // 附件表格loading
      tableLoading_doc: false,
      /* 按钮禁止与否 */
      isDisabled: false,
      // 表单宽度

      // 查询按钮禁用
      btnDisabled: false,
      // 查询按钮禁用 附件列表
      btnDisabled_doc: false,
    };
  },
  mounted() {
    // 上传地址
    this.fileUrl = FILE_URL + `/api/dataManage/fundFile/uploadFile?fundCode=${this.fundData.fundCode}&vcType=${this.formDialog.vcType}`
    this.headersParams = {
      Authorization: this.$store.getters.token
    }
    this.getListEdims('FUND_FILE_TYPE');
    // 默认查询
    this.$nextTick(() => {
      // 查询
      this.onQuery();
    });
  },
  methods: {
    // 查询
    onQuery(page) {
      this.$refs["formQuery"].validate(valid => {
        if (valid) {
          // 禁用搜索按钮
          this.$fun.searchButtonDisabled("btnDisabled", this);
          // 重置起始页
          if (page) this.formQuery.pageNum = 1;
          // 查询信息
          this.selectFileList();
        }
      });
    },
    // 字典查询
    getListEdims(type) {
      // 字典类型
      let params = type;
      commonApi.edimsDdiaCommon(params).then(res => {
        let { status, data } = res.data;
        if (status === 0) {
          // 附件类型
          if (type === "FUND_FILE_TYPE") {
            this.fileTypeList = data;
          }
        }
      });
    },
    //日志列表
    logDialog(){
      let params = Object.assign({}, {}, {
        fundCode:this.fundData.fundCode,
      });
      this.logDialogMask = true
      new Promise((resolve , reject) => {
        fundFileApi.fun_selectLogListPage(params).then(res=>{
          if(res.status==0){
            if(res.data!=null && res.data!=undefined){
              this.logList = res.data
            }
          }
        }).catch(error=>{
          reject(error)
        })
      })
    },
    // 清除
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    // 页面分页点击事件
    pagination(val) {
      let { page, limit } = val;
      // 起始页
      this.formQuery.pageNum = page;
      // 每页数量
      this.formQuery.pageSize = limit;
      // 查询
      this.onQuery();
    },

    // 查询列表信息
    selectFileList(flag) {
      this.tableLoading = true;
      let params = Object.assign({}, this.formQuery, {
        fundCode:this.fundData.fundCode,
      });
      // 清除空字段
      for (let k in params) {
        if (!params[k] && String(params[k]) !== "0") {
          delete params[k];
        }
      }
      new Promise((resolve, reject) => {
        fundFileApi.fun_selectListPage(params)
          .then(res => {
            this.tableLoading = false;
            this.isDisabled = false;
            let { status, data } = res;
            if (status === 0) {
              let { list, total } = data;
              this.tableData = list;
              this.total = total;
            }
          })
          .catch(error => {
            reject(error)
            this.tableLoading = false;
            this.isDisabled = false;
          });
      })

    },
    insertDialog(){
      this.dialogMask = true
      this.uploadFlag = true
      this.updateFlag = false

      this.modifyType = "1"
      this.$nextTick(() => {
        // 清除
        this.resetForm("formDialog");
        this.formFile.fileList=[]

      })

    },
    updateDialog(row){
      this.dialogMask = true
      this.uploadFlag = false
      this.updateFlag = true
      this.modifyType = "2"
      this.$nextTick(() => {
        // 清除
        this.resetForm("formDialog");
        this.formFile.fileList=[]
        this.selectById(row.fId)
      })
    },
    deleteFile(row){
      this.$confirm("确认删除?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          if (row.fId) {
            // 删除附件
            this.deleteFileAction(row.fId);
          }
        })
        .catch(() => {});
    },
    deleteFileAction(fId){
      new Promise((resolve, reject) => {
        fundFileApi.fun_delete(fId).then(res=>{
          if(res.status==200){
            this.$message({
              message: res.message,
              type: 'success'
            })
          }else{
            this.$message({
              message: res.message,
              type: 'warning'
            })
          }
          this.onQuery()
        }).catch(error=>{
          reject(error)
        })
      })
    },
    //渲染窗口数据
    selectById(fId){
      new Promise((resolve, reject) => {
        fundFileApi.fun_selectById(fId).then(res=>{
          if(res.data!=null && res.data!=undefined){
            let reponseData = res.data
            this.formDialog.fId = reponseData.fId
            this.formDialog.fileName = reponseData.fileName
            this.formDialog.vcType = reponseData.vcType
          }
        }).catch(error=>{
          reject(error)
        })
      })
    },
    //编辑保存
    dealData(){
      this.uploading2 = true
      let params = Object.assign({}, this.formDialog, {});
      new Promise((resolve, reject) => {
        fundFileApi.fun_update(params).then(res=>{
          if(res.status==200){
            this.$message({
              message: res.message,
              type: 'success'
            })
          }else{
            this.$message({
              message: res.message,
              type: 'warning'
            })
          }
          this.onQuery()
          this.dialogMask = false
          this.uploading2 = false
        }).catch(error=>{
          this.uploading2 = false
          reject(error)
        })
      })
    },
    //上传按钮
    submitUpload(){
      if(!this.fundData.fundCode){
        this.$message.closeAll()
        this.$message({
          message: '上传失败，组合代码为空！',
          type: 'warning'
        });
        return
      }
      this.uploading = true
      this.$refs.upload.submit()
    },
    // 文件上传前的动作
    beforeUpload(file){
      var testmsg=file.name.substring(file.name.lastIndexOf('.')+1)
      const extension = testmsg === 'xls'
      const extension2 = testmsg === 'xlsx'
      const extension3 = testmsg === 'doc'
      const extension4 = testmsg === 'docx'
      const extension5 = testmsg === 'pdf'
      const extension6 = testmsg === 'txt'
      const extension7 = testmsg === 'mdb'
      if(!extension && !extension2 && !extension3 && !extension4 && !extension5 && !extension6 && !extension7 ) {
        this.$message({
          message: '上传文件只能是 xls,xlsx,pdf,doc,docx,mdb,txt 格式!',
          type: 'warning'
        });
      }
      return extension || extension2 || extension3 || extension4 || extension5
    },
    // 文件上传成功后
    handleSuccess (res, file, fileList) {
      this.uploading = false
      this.dialogMask = false
      let { status, message } = res
      if (status === 200) {
        this.$message.closeAll()
        this.$message({
          message: '文件上传成功',
          type: 'success'
        })
        this.onQuery();
        // setTimeout(()=>{
        // 	this.$refs.upload.clearFiles()
        // },3000)
      }else{
        this.$message.closeAll()
        this.$message({
          message: message,
          type: 'warning'
        })
      }
    },
    // 文件上传失败时的钩子
    handleError () {
      this.uploading = false
      this.$message.error('文件上传失败')
    },
    //下载
    downloadFile(row){
      let params = {
        fId: row.fId,
        token: getToken()
      }
      if (!params.fId || !params.token) return
      // 参数、地址
      let a = fundFileApi.downloadFileUrl();
      a.then((val)=>{
        this.$fun.formDownloadFile(params, val,"GET");
      })
    },

    // 当表格的排序条件发生变化的时候会触发该事件
    handleSortChange(val) {
      this.formQuery.orderBy = this.$fun.queryOrderBy(val);
      // 查询
      this.onQuery();
    },


  },
  watch: {
    'formDialog.vcType':function(newVal,oldVal){
      this.fileUrl = FILE_URL + `/api/dataManage/fundFile/uploadFile?fundCode=${this.fundData.fundCode}&vcType=${this.formDialog.vcType}&fileName=${this.formDialog.fileName}`
    },
    'fundData.fundCode':function(newVal,oldVal){
      this.onQuery()
      this.fileUrl = FILE_URL + `/api/dataManage/fundFile/uploadFile?fundCode=${this.fundData.fundCode}&vcType=${this.formDialog.vcType}&fileName=${this.formDialog.fileName}`
    }

  }
};
</script>

<style lang="scss" >
.fundFilePage{
    padding: 10px;
  .el-dialog {
    width: 75% !important;
  }
  .el-dialog .el-form {
    width: 90% !important;
  }
  .el-dialog .el-form-item {
    min-width: 0% ;
    margin-right: 10px ;
  }
  .ProductAndProperty_box {
    height: 300px;
  }

  .item-label{
    font-size: 16px;
  }
  .el-checkbox-button--medium .el-checkbox-button__inner{
    font-size: 16px;
  }


}
</style>

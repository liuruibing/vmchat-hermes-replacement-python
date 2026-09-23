<template>
  <div class="report_A1005">
    <div style="text-align: right;margin-bottom:10px;">
      <el-button size="small" icon="el-icon-plus" @click="add()">新增</el-button>
    </div>
    <el-table
      :data="tableData"
      border
      style="width: 100%"
      v-loading="tableLoading"
      @sort-change="handleSortChange"
    >
      <el-table-column prop="agencyCode" label="机构编号" min-width="180" sortable='custom' show-overflow-tooltip>
      </el-table-column>
      <el-table-column prop="yearReport" label="报告年度" min-width="180" sortable='custom' show-overflow-tooltip>
      </el-table-column>
      <el-table-column prop="reportingPeriod" label="报告期间" min-width="180" sortable='custom' show-overflow-tooltip>
        <template slot-scope="scope">
          {{transform('2',scope.row.reportingPeriod) || scope.row.reportingPeriod}}
        </template>
      </el-table-column>
      <el-table-column prop="startDate" label="期初日期" min-width="180" sortable='custom' show-overflow-tooltip>
      </el-table-column>
      <el-table-column prop="endDate" label="期末日期" min-width="180" sortable='custom' show-overflow-tooltip>
      </el-table-column>
      <el-table-column prop="productCode" label="产品代码" min-width="180" sortable='custom' show-overflow-tooltip>
      </el-table-column>
      <el-table-column prop="fileType" label="文件类型" min-width="180" sortable='custom' show-overflow-tooltip>
        <template slot-scope="scope">
          {{transform('1',scope.row.fileType) || scope.row.fileType}}
        </template>
      </el-table-column>
      <el-table-column prop="fileName" label="文件名称" min-width="180" sortable='custom' show-overflow-tooltip>
      </el-table-column>
      <el-table-column prop="effectiveDate" label="生效日期" min-width="180" sortable='custom' show-overflow-tooltip>
      </el-table-column>
      <el-table-column prop="remark" label="备注" min-width="180" sortable='custom' show-overflow-tooltip>
      </el-table-column>
      <el-table-column
        label="操作"
        fixed="right"
        min-width="180"
        align="center"
        show-overflow-tooltip
      >
        <template slot-scope="scope">
          <el-button size="small" @click="edit(scope.row)" :loading="delete_loading">编辑</el-button>
          <el-button size="small" @click="delete_(scope.row)" style="color:#F56C6C;" :loading="delete_loading">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <Pagination
      :total="total"
      :page="formInline.pageNum"
      :limit="formInline.pageSize"
      @pagination="Pagination"
    >
    </Pagination>

    <el-dialog
      :title="dialogTitle"
      v-dialogDragWidth
      :before-close="handleClose"
      width="50% !important"
      center
      append-to-body
      :visible.sync="visible"
      :close-on-click-modal="false"
    >
      <el-container>
        <el-main>
          <el-form
            label-position="right"
            label-width="100px"
            :model="formData"
            ref="formData"
            class="report_A1005_mainBox_formData"
            :rules="formRules"
          >
            <el-form-item label="机构编号" prop="agencyCode">
              <el-input v-model="formData.agencyCode"></el-input>
            </el-form-item>
            <el-form-item label="产品代码" prop="productCode">
              <el-input v-model="formData.productCode"></el-input>
            </el-form-item>
            <el-form-item label="报告年度" prop="yearReport">
              <el-date-picker
                v-model="formData.yearReport"
                value-format="yyyy"
                type="year"
                placeholder="选择年"
              >
              </el-date-picker>
            </el-form-item>
            <el-form-item label="报告期间" prop="reportingPeriod">
              <el-select
                v-model="formData.reportingPeriod"
                placeholder="请选择"
              >
                <el-option
                  v-for="item in reportingPeriodArr"
                  :key="item.dimCde"
                  :label="item.dimNme"
                  :value="item.dimCde"
                >
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="期初日期" prop="startDate">
              <el-date-picker
                v-model="formData.startDate"
                type="date"
                editable
                size=""
                value-format="yyyy-MM-dd"
                placeholder="选择日期"
                :disabled="dialogTitle=='编辑'?true:false"
              >
              </el-date-picker>
            </el-form-item>
            <el-form-item label="期末日期" prop="endDate">
              <el-date-picker
                v-model="formData.endDate"
                type="date"
                editable
                size=""
                value-format="yyyy-MM-dd"
                placeholder="选择日期"
                disabled
              >
              </el-date-picker>
            </el-form-item>

            <el-form-item label="生效日期" prop="effectiveDate">
              <el-date-picker
                v-model="formData.effectiveDate"
                type="date"
                editable
                size=""
                value-format="yyyy-MM-dd"
                placeholder="选择日期"
              >
              </el-date-picker>
            </el-form-item>
            <el-form-item label="文件类型" prop="fileType">
              <el-select v-model="formData.fileType" placeholder="请选择">
                <el-option
                  v-for="item in fileTypeArr"
                  :key="item.dimCde"
                  :label="item.dimNme"
                  :value="item.dimCde"
                >
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="备注" prop="remark">
              <el-input
                type="textarea"
                maxlength="70"
                show-word-limit
                v-model="formData.remark"
              ></el-input>
            </el-form-item>
            <el-form-item label="附件上传" prop="file">
              <el-upload
                class="upload-demo"
                v-model="fileList"
                ref="upload"
                name="file"
                :headers="hearders"
                :action="fileUploadUrl"
                :on-remove="handleRemove"
                :on-change="handleChange"
                :file-list="fileList"
                :auto-upload="false"
                :limit="1"
              >
                <el-button slot="trigger" size="small" type="primary"
                  >浏览</el-button
                >
              </el-upload>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="visible = false" :loading="save_loading">取 消</el-button>
        <el-button type="primary" size="small" :loading="save_loading" @click="submit()">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import commonFun from '@/filters/new_common';
import xbrlpageApi from "@/api/xbrl/xbrl";
import trackingAgentApi from "@/api/transfer/trackingAgentList";
import Pagination from "@/components/Pagination";
import pageApi from "@/api/xbrl/reportA1005.js";
import modelFileValidate from "@/mixinsModel/file-validate";
export default {
  mixins: [modelFileValidate],
  components: { Pagination },
  props: {
    currencyReportPageData: {},
  },
  data() {
    return {
      tableData: [],
      tableLoading: false,
      dialogTitle: "",
      visible: false,
      formInline: {
        pageNum: 1,
        pageSize: 20,
        orderString:""
      },
      total: 0,
      // 表单数据
      rowObj:{},
      fileTypeArr: [], //文件类型
      reportingPeriodArr: [], //报告期间
      formData: {
        agencyCode: "",
        yearReport: "",
        reportingPeriod: "",
        startDate: "",
        endDate: this.currencyReportPageData.dataDate || '',
        productCode: "",
        effectiveDate: "",
        remark: "",
        fileType:""
      },
      fileList: [],
      hearders: {},
      fileUploadUrl: "",
      save_loading:false,
      delete_loading:false,
      formRules: {
        agencyCode: [
          { required: true, message: "请填写机构编号", trigger: "change" },
        ],
        yearReport: [
          { required: true, message: "请选择报告年度", trigger: "change" },
        ],
        reportingPeriod: [{required: true, message: '请选择报告期间', trigger: 'change'}],
        startDate: [
          { required: true, message: "请选择期初日期", trigger: "change" },
        ],
        endDate: [
          { required: true, message: "请选择期末日期", trigger: "change" },
        ],
        productCode: [
          { required: true, message: "请选择产品代码", trigger: "change" },
        ],
        effectiveDate: [
          { required: true, message: "请选择生效日期", trigger: "change" },
        ],
        fileType: [
          { required: true, message: "请选择文件类型", trigger: "change" },
        ],
      },
    };
  },
  mounted() {
    this.getSelects('fileTypeA1005'); //获取文件类型下拉值
    this.getSelects('reportPeriod'); //报告期间下拉值
    this.getTableData(true);
  },
  methods: {
    transform(type,val){
      // console.log(type,val);
      if(type=="1"){
        if(this.fileTypeArr.length){
          let arr = this.fileTypeArr;
          let ii = arr.find(item=>{
            return item.dimCde == val
          })
          return ii.dimNme || ''
        }
      }
      if(type=="2"){
        if(this.reportingPeriodArr.length){
          let arr = this.reportingPeriodArr;
          let ii = arr.find(item=>{
            return item.dimCde == val
          })
          return ii.dimNme || ''
        }
      }
    },
    // 下拉框值
    getSelects(val) {
      let params = val;
      xbrlpageApi
        .getSelects(params)
        .then((res) => {
          let self = this;
          if (res.data.message === "success") {
            if (val === "fileTypeA1005") {
              this.fileTypeArr = res.data.data;
              let arr = res.data.data;
              // for (let i = 0; i < arr.length; i++) {
              //   this.fileTypeArr[arr[i].dimCde] = arr[i].dimNme;
              // }
            }
            if (val === "reportPeriod") {
              this.reportingPeriodArr = res.data.data;
              let arr = res.data.data;
              // for (let i = 0; i < arr.length; i++) {
              //   this.reportingPeriodArr[arr[i].dimCde] = arr[i].dimNme;
              // }
            }
            
          } else {
            this.$message.closeAll();
            this.$message.error("初始化数据失败");
          }
        })
        .catch(() => {
          this.$message.closeAll();
          this.$message.error("初始化数据失败");
        });
    },
    // 获取列表数据
    getTableData(flag) {
      if(flag){
        this.formInline.pageNum = 1;
      }
      let params = {
        reportDate: this.currencyReportPageData.dataDate || "",
        pageNum:this.formInline.pageNum,
        pageSize:this.formInline.pageSize,
        orderString:this.formInline.orderString
      };
      this.tableLoading = true;
      pageApi
        .findProductFile(params)
        .then((res) => {
          if (res.data.status == 0) {
            this.tableData = res.data.data.list;
            this.total = res.data.data.total;
          } else {
            this.$message({
              type: "error",
              message: res.data.message || "获取数据失败！",
            });
            this.tableData = [];
            this.total = 0;
          }
          this.tableLoading = false;
        })
        .catch((err) => {
          this.tableLoading = false;
          this.tableData = [];
          this.total = 0;
        });
    },
    Pagination(val) {
      this.formInline.pageSize = val.limit; //页面条数
      this.formInline.pageNum = val.page;//页码
      this.getTableData(false)
    },
    handleSortChange(val){
      this.formInline.orderString = commonFun.orderByString(val);
      this.getTableData(false);
      // console.log(commonFun.orderByString(val));

    },
    // 新增
    add() {
      this.dialogTitle = "新增";
      this.visible = true;
      this.resetForm();
      this.fileList = [];
    },
    // 编辑
    edit(row) {
      this.rowObj = row;
      this.getFileList(row.fileId);
      this.dialogTitle = "编辑";
      this.visible = true;
      this.$nextTick(() => {
        this.formData.agencyCode = row.agencyCode || "";
        this.formData.yearReport = row.yearReport || "";
        this.formData.reportingPeriod = row.reportingPeriod || "";
        this.formData.startDate = row.startDate || "";
        this.formData.endDate = row.endDate || "";
        this.formData.productCode = row.productCode || "";
        this.formData.effectiveDate = row.effectiveDate || "";
        this.formData.remark = row.remark || "";
        this.formData.fileType = row.fileType || "";
      });
    },
    // 删除
    delete_(row){
      let params = {
        id:row.id,
        fileId:row.fileId
      }
      this.$confirm('是否删除该文件?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
        }).then(() => {
          this.delete_loading = true;
          pageApi.delProductFile(params).then(res=>{
            if(res.data.status == 0){
              this.$message({
                type:"success",
                message:"删除成功！"
              })
              this.getTableData(true);
            }else{
              this.$message({
                type:"error",
                message:"删除失败！"
              })
            }
            this.delete_loading = false;
          }).catch(()=>{
            this.delete_loading = false;
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });          
        });
      
    },
    // 获取文件
    getFileList(id) {
      trackingAgentApi
        .getFileList(id)
        .then((res) => {
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
          }
        })
        .catch(() => {});
    },
    // 提交表单
    submit() {
      this.$refs["formData"].validate((valid) => {
        if (valid) {
          if (this.fileList.length) {
            this.onSubmit(this.dialogTitle);
          } else {
            this.$message({
              type: "warning",
              message: "请上传附件！",
            });
            return false;
          }
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    onSubmit(type) {
      let params = JSON.parse(JSON.stringify(this.formData));
      // console.log(params);
      let formdata = new FormData();
      formdata.append("agencyCode", params.agencyCode || "");
      formdata.append("yearReport", params.yearReport || "");
      formdata.append("reportingPeriod", params.reportingPeriod || "");
      formdata.append("startDate", params.startDate || "");
      formdata.append("endDate", params.endDate || "");
      formdata.append("productCode", params.productCode || "");
      formdata.append("effectiveDate", params.effectiveDate || "");
      formdata.append("fileType", params.fileType || "");
      formdata.append("remark", params.remark || "");
      formdata.append("reportDate", this.currencyReportPageData.dataDate || "");

      if (this.fileList[0].raw) {
        let aa = this.fileList[0].raw;
        formdata.append("file", aa);
      }
      if (!this.fileList[0].raw) {
        let bb = this.fileList[0].id;
        formdata.append("oldFile", bb);
      }
      if(type=="新增"){
        this.addSubmit(formdata);
      }else if(type=="编辑"){
        this.editSubmit(formdata)
      }
    },
    // 新增保存
    addSubmit(formdata){
      this.save_loading = true;
      pageApi.addProductFile(formdata).then(res=>{
        if(res.data.status == 0){
          this.$message({
            type:"success",
            message:"新增成功！"
          })
          this.visible = false;
          this.getTableData(true);
        }else{
          this.$message({
            type:"error",
            message:"新增失败！"
          })
        }
        this.save_loading = false;
      }).catch(()=>{
        this.save_loading = false;
      })
    },
    // 编辑保存
    editSubmit(formdata){
      let row = this.rowObj;
      formdata.append('id',row.id || '');
      formdata.append('fileId',row.fileId || '');
      this.save_loading = true;
      pageApi.updateProductFile(formdata).then(res=>{
        if(res.data.status == 0){
          this.$message({
            type:"success",
            message:"编辑成功！"
          })
          this.visible = false;
          this.fileList = [];
          this.getTableData(true);
        }else{
          this.$message({
            type:"error",
            message: res.data.message || "编辑失败！"
          })
        }
        this.save_loading = false;
      }).catch(()=>{
        this.save_loading = false;
      })
    },
    // 关闭弹框
    handleClose(done) {
      this.resetForm();
      this.fileList = [];
      done();
    },
    handleChange(file, fileList) {
      this.fileValidate(file, fileList);
    },
    handleRemove(file, fileList) {
      this.handleChange(file, fileList);
    },
    resetForm() {
      this.$nextTick(() => {
        this.$refs["formData"].resetFields();
      });
    },
  },
};
</script>

<style lang="scss">
.report_A1005_mainBox_formData {
  padding: 0 30px !important;
  .el-date-editor.el-input,
  .el-date-editor.el-input__inner {
    width: 100% !important;
  }
  .el-select--medium {
    width: 100%;
  }
}
</style>
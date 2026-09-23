<template>
  <div class="tg_form" v-loading="tg_form_loading">
    <div v-if="none_show"><span>未找到当前产品的账户信息。</span></div>
    <div class="forms_table_title" v-if="table_show">
      <i class="el-icon-s-data"></i>托管户账户列表
    </div>
    <el-table
      v-if="table_show"
      ref="multipleTable"
      :data="tableData"
      border
      stripe
      v-loading="tableLoading"
      style="width: 100%"
    >
      <!-- <el-table-column fixed type='selection' width='35'></el-table-column> -->
      <el-table-column
        prop="productCode"
        sortable="custom"
        show-overflow-tooltip
        label="产品代码"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.productCode | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="productName"
        sortable="custom"
        show-overflow-tooltip
        label="产品名称"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.productName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="accoName"
        sortable="custom"
        show-overflow-tooltip
        label="账户名称"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.accoName | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="accoNo"
        sortable="custom"
        show-overflow-tooltip
        label="账户账号"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.accoNo | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="accoBank"
        sortable="custom"
        show-overflow-tooltip
        label="开户行"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.accoBank | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="hvpsNo"
        sortable="custom"
        show-overflow-tooltip
        label="大额支付系统号"
        min-width="100"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.hvpsNo | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        label="操作"
        fixed="right"
        min-width="100"
        align="center"
      >
        <template slot-scope="scope">
          <el-button type="primary" size="small" @click="searchData(scope.row)">
            查看详情
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-container v-if="form_show && !preview_show">
      <el-main class="mainBox">
        <div style="overflow: hidden; padding: 15px">
          <span
            @click="close_form"
            style="font-size: 20px; float: right; cursor: pointer"
            ><i class="el-icon-close"></i
          ></span>
        </div>
        <el-form
          ref="formCount"
          :model="formCount"
          :rules="countRules"
          label-position="right"
        >
          <el-row>
            <el-col :span="12">
              <el-form-item
                label=" 产品名称"
                prop="productId"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <select-table
                  v-model="formCount.productId"
                  :width="'600px'"
                  @sendDataObj="dataObj"
                  v-if="!isSearchData"
                ></select-table>
                <el-input
                  v-model="formCount.productId"
                  disabled
                  v-else
                ></el-input>
              </el-form-item>
              <el-form-item
                label="账户名称"
                prop="accoName"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <el-input
                  maxlength="66"
                  :disabled="isSearchData"
                  type="text"
                  v-model.trim="formCount.accoName"
                  clearable
                ></el-input>
              </el-form-item>
              <el-form-item
                label="开户行"
                prop="accoBank"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <el-input
                  maxlength="166"
                  :disabled="isSearchData"
                  type="text"
                  v-model.trim="formCount.accoBank"
                  clearable
                ></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item
                label="产品代码"
                prop="productCode"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <el-input
                  type="text"
                  disabled
                  v-model.trim="formCount.productCode"
                  clearable
                ></el-input>
              </el-form-item>

              <el-form-item
                label="账户账号"
                prop="accoNo"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <el-input
                  maxlength="66"
                  :disabled="isSearchData"
                  type="text"
                  v-model.trim="formCount.accoNo"
                  clearable
                ></el-input>
              </el-form-item>

              <el-form-item
                label="大额支付系统号"
                prop="hvpsNo"
                class="mb20"
                :label-width="formLabelWidth"
              >
                <el-input
                  maxlength="66"
                  :disabled="isSearchData"
                  type="text"
                  v-model.trim="formCount.hvpsNo"
                  clearable
                ></el-input>
              </el-form-item>
            </el-col>
          </el-row>

          <el-form-item
            label="备注"
            prop="remark"
            class="mb20"
            :label-width="formLabelWidth"
          >
            <el-input
              :disabled="isSearchData"
              type="textarea"
              :autosize="{ minRows: 3 }"
              maxlength="1000"
              placeholder="请输入备注"
              v-model="formCount.remark"
            >
            </el-input>
          </el-form-item>
          <br />
          <el-form-item
            label="账户资料上传"
            prop="file"
            class="mb20"
            :label-width="formLabelWidth"
          >
            <el-upload
              class="upload-demo"
              ref="upload"
              :disabled="isSearchData"
              :on-preview="downFile"
              :headers="hearders"
              :action="fileUploadUrl"
              :on-error="handleError"
              :on-remove="handleRemove"
              :on-success="handleSuccess"
              :on-change="handleChange"
              :file-list="fileList"
              :auto-upload="false"
            >
              <el-button
                slot="trigger"
                size="small"
                type="primary"
                v-show="isUpload"
                >浏览</el-button
              >
            </el-upload>
          </el-form-item>
        </el-form>
      </el-main>
    </el-container>
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
  data() {
    return {
      formCount: {
        mjType: "1",
        companyName: "", //公司名称
        productId: "", //产品名称
        productCode: "", //产品代码
        accoName: "", //账户名称
        accoNo: "", //账户号码
        accoBank: "", //开户行
        remark: "",
        accoType: "fiduciary",
        hvpsNo: "", //大额支付系统号
      },
      formLabelWidth: "150px",
      countRules: {},
      isSearchData: true,
      hearders: {},
      fileUploadUrl: "",
      fileList: [],
      isUpload: false,
      tg_form_loading: false,
      none_show: false,
      table_show: false,
      form_show: false,
      preview_show:false,
      PreviewFileId:''
    };
  },
  methods: {
    init(val) {
      this.preview_show = false;
      this.form_show = false;
      this.tg_form_loading = true;
      this.getTableList(val);
    },
    getTableList(data) {
      this.tableData = [];
      this.tableLoading = true;
      let fundCode = data;
      let params = {
        accoType: "fiduciary",
        fundCode: fundCode,
        pageSize: 500,
        pageNum: 1,
      };
      pageApi
        .getDataSourceList(params)
        .then((response) => {
          this.tg_form_loading = false;
          if (response.data.status === 200) {
            this.tableData = response.data.data.list;
            if (this.tableData.length) {
              this.table_show = true;
              this.none_show = false;
            } else {
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
          this.tg_form_loading = false;
        });
    },
    searchData(row) {
      this.table_show = false;
      this.form_show = true;
      this.getFileList(row.id, "tgh_file");
      for (let i in this.formCount) {
        if (row[i]) this.formCount[i] = row[i];
        else this.formCount[i] = "";
      }
      this.formCount["productId"] = row["productName"];
    },
    getFileList(relaId, relaType) {
      commonApi
        .getFileList(relaId, relaType)
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
            // this.rmoveFileId = [ ...this.fileList ]
          } else {
            this.fileList = [];
            // this.rmoveFileId = []
            this.$message.error("查询详情附件信息失败");
          }
        })
        .catch(() => {});
    },
    close_form(){
      this.table_show = true;
      this.form_show = false;
    },
    closePreview(){
      this.preview_show = false;
      this.$notify.closeAll();
    },
    selectChangemj() {},
    downFile(file) {
      if(file.id){
        this.PreviewFileId = file.id;
        this.preview_show=true;
      }
      // console.log(this.fileList);
    },
    handleError() {},
    handleRemove() {},
    handleSuccess() {},
    handleChange() {},
  },
};
</script>

<style lang="scss">
.tg_form{
  // min-height: 50px;
  height: 100%;
  .el-form-item__content{
    min-width: 0 !important;
  }
}
</style>
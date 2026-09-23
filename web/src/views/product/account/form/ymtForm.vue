<template>
  <div class="ymt_form">
    <el-container>
        <el-main class="mainBox">
          <el-form
            ref="formCount"
            :model="formCount"
            :rules="countRules"
            label-position="right"
          >
            <div class="forms_table_title">
              <i class="el-icon-s-data"></i>一码通信息
            </div>
            <el-row>
              <el-col :span="12">
                <el-form-item
                  label=" 产品名称"
                  prop="productId"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                 <select-table v-model="formCount.productId" :width="'600px'" @sendDataObj='dataObj' v-if="!isSearchData" ref="relation"></select-table>
                  <el-input v-model="formCount.productId" disabled v-else></el-input>
                </el-form-item>
                <el-form-item
                  label="一码通"
                  prop="yard"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="66"
                    :disabled="isSearchData"
                    v-model.trim="formCount.yard"
                    clearable
                    ref="yard"
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
                    maxlength="100"
                    disabled
                    v-model.trim="formCount.productCode"
                    clearable
                    ref="productCode"
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
                :autosize="{minRows: 3}"
                maxlength="166"
                placeholder="请输入备注"
                v-model="formCount.remark"
                ref="remark"
              >
              </el-input>
            </el-form-item>
            <el-form-item
              label="账户资料上传"
              prop="file"
              class="mb20"
              :label-width="formLabelWidth"
            >
              <el-upload
                class="upload-demo"
                ref="upload"
                :on-preview="downFile"
                :headers="hearders"
                :action="fileUploadUrl"
                :on-error="handleError"
                :on-remove="handleRemove"
                :on-success="handleSuccess"
                :on-change="handleChange"
                :file-list="fileList"
                :disabled="isSearchData"
                :auto-upload="false"
              >
                <el-button
                  slot="trigger"
                  size="small"
                  type="primary"
                  v-show="!isSearchData"
                  >浏览</el-button
                >
              </el-upload>
            </el-form-item>
          </el-form>

          <div class="forms_table_title">
            <i class="el-icon-s-data"></i>股卡信息
          </div>
          <!-- <el-button
            :disabled="isSearchData"
            type="primary"
            plain
            @click="insertEvent"
            style="margin-bottom: 5px"
            size="small"
          >
            <i class="el-icon-circle-plus-outline"></i>新增
          </el-button>
          <el-button
            :disabled="isSearchData"
            type="danger"
            plain
            @click="removeEvent"
            style="margin-bottom: 5px"
            size="small"
          >
            <i class="el-icon-delete"></i>移除
          </el-button> -->
          <div class="vxeTableTitle">
            <vxe-table
              border
              show-overflow="title"
              keep-source
              ref="xTable"
              class="my_table_insert"
              height="600"
              :edit-rules="validRules"
              :data="tableDataEdit"
              :edit-config="{
                trigger: 'click',
                mode: 'row',
                icon: 'fa fa-pencil',
                showStatus: true,
              }"
            >
              <vxe-table-column type="checkbox" width="60"></vxe-table-column>
              <vxe-table-column
                type="seq"
                title="序号"
                width="60"
              ></vxe-table-column>
              <vxe-table-column
                :disabled="isSearchData"
                field="szaAccount"
                title="深市A股账号"
                :edit-render="{
                  name: 'input',
                  attrs: {
                    type: 'text',
                    disabled: isSearchData,
                    maxlength: 60,
                  },
                }"
              ></vxe-table-column>
              <vxe-table-column
                :disabled="isSearchData"
                field="shaAccount"
                title="沪市A股账号"
                :edit-render="{
                  name: 'input',
                  attrs: {
                    type: 'text',
                    disabled: isSearchData,
                    maxlength: 60,
                  },
                }"
              ></vxe-table-column>
              <vxe-table-column
                :disabled="isSearchData"
                field="openStruc"
                title="	开户机构"
                :edit-render="{
                  name: 'input',
                  attrs: {
                    type: 'text',
                    disabled: isSearchData,
                    maxlength: 60,
                  },
                }"
              ></vxe-table-column>
            </vxe-table>
          </div>
        </el-main>
      </el-container>
  </div>
</template>

<script>
export default {
  data(){
    return{
      formCount:{},
      formLabelWidth: "150px",
      countRules:{},
      isSearchData:true,
      hearders:{},
      fileUploadUrl:'',
      fileList:[],
      typeArr:[],
      isUpload:false,
      validRules:{},
      tableDataEdit:[]
    }
  },
  methods:{
    selectChangemj(){},
    downFile(){},
    handleError(){},
    handleRemove(){},
    handleSuccess(){},
    handleChange(){}
  }
}
</script>

<style>

</style>
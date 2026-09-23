<template>
  <div class="mj_form">
    <el-container>
        <el-main class="mainBox">
          <el-form
            ref="formCount"
            :model="formCount"
            :rules="countRules"
            label-position="right"
          >
            <el-row>
              <el-col :span="12">
                <el-form-item
                  label="募集户类型"
                  prop="type"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-select
                    :disabled="isSearchData"
                    style="width: 100%"
                    v-model="formCount.mjType"
                    placeholder="请选择"
                    @change="selectChangemj"
                  >
                    <el-option
                      v-for="item in typeArr"
                      :key="item.value"
                      :label="item.name"
                      :value="item.value"
                    >
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item
                  v-show="formCount.mjType === '1'"
                  label="产品名称"
                  prop="productId"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <select-table v-model="formCount.productId" @sendDataObj='dataObj' v-if="!isSearchData" ref="relation"></select-table>
                  <el-input v-model="formCount.productId" disabled v-else></el-input>
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
                    ref="accoName"
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
                    ref="hvpsNo"
                  ></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="12">
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
                    ref="accoBank"
                  ></el-input>
                </el-form-item>
                <el-form-item
                  v-show="formCount.mjType === '1'"
                  label="产品代码"
                  prop="productCode"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="100"
                    disabled
                    v-model.trim="formCount.productCode"
                    ref="productCode"
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
                    ref="accoNo"
                  ></el-input>
                </el-form-item>

                <el-form-item
                  v-if="formCount.mjType === '0'"
                  label="公司名称"
                  prop="companyName"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <el-input
                    maxlength="166"
                    :disabled="isSearchData"
                    type="text"
                    v-model.trim="formCount.companyName"
                    clearable
                    ref="companyName"
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
                maxlength="1000"
                style="width: 100%"
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
                style="width: 480px"
                class="upload-demo"
                ref="upload"
                :disabled="isSearchData"
                :headers="hearders"
                :action="fileUploadUrl"
                :on-preview="downFile"
                :on-error="handleError"
                :on-remove="handleRemove"
                :on-success="handleSuccess"
                :on-change="handleChange"
                :file-list="fileList"
                :auto-upload="false"
              >
                <el-button slot="trigger" type="primary" v-show="isUpload"
                  >浏览</el-button
                >
              </el-upload>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
  </div>
</template>

<script>
export default {
  props:{

  },
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
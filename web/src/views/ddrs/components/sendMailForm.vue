<template>
  <div class="send_mail_form">
    <div style="width: 90%; margin: 0 auto" v-if="formArr && formArr.length">
      <p style="padding: 2px">报表数据筛选：</p>
      <el-form
        :inline="true"
        :model="formInline"
        :rules="formInlineRules"
        label-position="right"
        label-width="144px"
        class="form_inline_search currency_report_old_form"
        style="width: 100% !important"
      >
        <el-form-item v-for="(item, index) in formArr" :key="index" :label="item.fieldCn" :prop="item.fieldEn" :label-width="index > 0 ? '144px' : '144px'">
          <el-input
            v-model.trim="formInline[item.fieldEn]"
            type="text"
            v-if="item.fieldType != 'D' && !item.dicSql"
            auto-complete="off"
            size="small"
            clearable
            placeholder="请输入"
          />
          <!-- 产品单选组件 -->
          <select-table v-model="formInline[item.fieldEn]" v-if="item.inputType == 'select_fund'" @sendDataObj="sendDataObj($event, item.fieldEn)"></select-table>
          <!-- 产品多选组件 -->
          <multipleSelectTable
            v-if="item.inputType == 'select_multiple_fund'"
            v-model="formInline[item.fieldEn]"
            :data="fundList"
            :Columns="Columns"
            idField="fundCode"
            nameField="codeName"
            placeholder="请选择"
            @checkboxChange="checkboxChange($event, item.fieldEn)"
            @checkboxAll="checkboxAll($event, item.fieldEn)"
          ></multipleSelectTable>

          <!-- 父 -->
          <el-select
            v-if="item.dicSql && item.inputType == 'select'"
            clearable
            filterable
            v-model="formInline[item.fieldEn]"
            placeholder="请选择"
            @change="item.sonEn ? getSunchange($event, item.fieldEn, item.sonEn) : selectChange($event, item.fieldEn)"
          >
            <el-option
              v-for="(group, index) in formSelectArr[item.fieldEn]"
              :value="group.DIM_CDE"
              :key="index"
              :label="group.DIM_NME"
              @click.native="item.sonEn ? getSun(group.DIM_CDE, group.DIM_NME, group.ID, item.fieldEn, item.sonEn) : getSunClick(group.DIM_CDE, group.DIM_NME, item.fieldEn)"
            >
            </el-option>
          </el-select>

          <el-select
            class="select_multiple"
            popper-class="select_multiple_popper"
            v-if="item.dicSql && item.inputType == 'select_multiple'"
            filterable
            multiple
            collapse-tags
            v-model="formInline[item.fieldEn]"
            placeholder="请选择"
            @change="select_multipleChange($event, item.fieldEn)"
          >
            <el-option v-for="(group, index) in formSelectArr[item.fieldEn]" :value="group.DIM_CDE" :key="index" :label="group.DIM_NME"> </el-option>
          </el-select>

          <el-date-picker
            v-model="formInline[item.fieldEn]"
            type="date"
            size="small"
            v-if="item.fieldType === 'D' && !item.formatValue"
            value-format="yyyy-MM-dd"
            placeholder="选择日期"
          >
          </el-date-picker>
          <el-date-picker
            v-model="formInline[item.fieldEn]"
            type="year"
            size="small"
            v-if="item.fieldType === 'D' && item.formatValue == 'yyyy'"
            value-format="yyyy"
            placeholder="选择年"
          >
          </el-date-picker>
          <el-date-picker
            v-model="formInline[item.fieldEn]"
            type="month"
            size="small"
            v-if="item.fieldType === 'D' && item.formatValue == 'yyyy-mm'"
            value-format="yyyy-MM"
            placeholder="选择月"
          >
          </el-date-picker>
        </el-form-item>
      </el-form>
    </div>
    <div style="width: 90%; margin: 0 auto">
      <p style="padding: 2px">邮件配置：</p>
      <el-form ref="formData" :model="formData" :rules="formDataRules" label-position="right" label-width="144px" style="width: 100% !important">
        <el-form-item label="报表格式" prop="fileType">
          <el-select v-model="formData.fileType" clearable placeholder="请选择" style="width: 100%">
            <el-option key="1" label="EXCEL" value="excel"></el-option>
            <el-option key="2" label="TXT" value="txt"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="收件人" prop="emailTos">
          <selectContacts ref="selectContacts" v-model="formData.emailTos"></selectContacts>
        </el-form-item>
        <el-form-item label="抄送" prop="emailCcs">
          <selectContacts ref="selectContacts2" v-model="formData.emailCcs"></selectContacts>
        </el-form-item>
        <el-form-item label="密送" prop="emailBccs">
          <selectContacts ref="selectContacts3" v-model="formData.emailBccs"></selectContacts>
        </el-form-item>
        <div class="hebing">
          <el-form-item style="width: 100%" label="主题" prop="emailSubject">
            <el-input type="textarea" :autosize="{ minRows: 2 }" maxlength="200" show-word-limit placeholder="请输入内容" v-model="formData.emailSubject"> </el-input>
          </el-form-item>
        </div>
        <div class="hebing">
          <el-form-item style="width: 100%" label="正文" prop="emailContent">
            <el-input type="textarea" :autosize="{ minRows: 2 }" placeholder="请输入内容" v-model="formData.emailContent"> </el-input>
          </el-form-item>
        </div>
      </el-form>
    </div>
    <div style="text-align: center">
      <el-button @click="closeForm" :loading="send_loading">取消</el-button>
      <el-button type="primary" @click="submitFormValid" :loading="send_loading">发送</el-button>
    </div>
  </div>
</template>

<script>
import bizBeginApi from "../api/bizBegin";
import selectTable from "./selectTable.vue";
import multipleSelectTable from "./multiple-select-table2";
import commonFun from "@/filters/new_common";
import reportToolApi from "../api/reportTool";
import selectContacts from "./index2";
export default {
  components: { selectContacts, selectTable, multipleSelectTable },
  props: {
    formArr: {
      type: Array,
      required: true
    },
    formSelectArr: {},
    tableCode: {},
    reportCode: {},
    reportName: {},
    headerArr: {}
  },
  data() {
    return {
      fundList: [],
      Columns: [{ label: "产品", prop: "codeName" }, { label: "托管机构", prop: "trustorName" }, { label: "基金服务机构", prop: "operatorName" }],
      tableData: [
        {
          contactName: "孙文博",
          contactType: "1",
          email: "1349961353@qq.com",
          id: "140e60246d7f4ad7b73e51c2d377c5b0",
          institutionCode: "8db9c1be99534669a34585d603cd1c75",
          isDel: "0"
        },
        {
          contactName: "Vikun",
          contactType: "1",
          email: "huang1997530@163.com",
          id: "27e3c952326449459db133e909dda6c9",
          institutionCode: "8db9c1be99534669a34585d603cd1c75",
          isDel: "0",
          phone: "17621157530"
        },
        {
          contactLabel: "没有标签",
          contactName: "sun",
          contactType: "1",
          deptPost: "前端",
          email: "syl_weiyi@163.com",
          id: "caa8eb4e79214176a1feee11b6f5af6b",
          institutionCode: "8db9c1be99534669a34585d603cd1c75",
          isDel: "0",
          phone: "13788888888"
        }
      ],
      Columns2: [{ prop: "contactName", label: "姓名" }, { prop: "email", label: "邮箱" }, { prop: "phone", label: "手机" }],
      formInline: {},
      // formSelectArr:{},
      formInlineRules: {},
      formData: {
        fileType: "excel",
        emailTos: [],
        emailCcs: [],
        emailBccs: [],
        emailSubject: "",
        emailContent: ""
      },
      formDataRules: {
        fileType: {
          required: true,
          message: "请选择文件格式",
          trigger: "change"
        },
        emailTos: {
          required: true,
          message: "请选择收件人",
          trigger: "change"
        },
        emailSubject: {
          required: true,
          message: "请输入邮件主题",
          trigger: "change"
        }, //邮件主题
        emailContent: {
          required: true,
          message: "请输入邮件正文",
          trigger: "change"
        } //邮件正文
      },
      send_loading: false
    };
  },
  mounted() {
    this.getFundList();
    // setTimeout(() => {
    // this.formData.emailTos=["140e60246d7f4ad7b73e51c2d377c5b0","caa8eb4e79214176a1feee11b6f5af6b",]
    // }, 1000);
  },
  methods: {
    init(data) {
      let obj = JSON.parse(JSON.stringify(data));
      obj.pageSize = null;
      obj.pageNum = null;
      this.formInline = obj;
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
    sendDataObj(data, fieldEn) {
      // console.log(data,aaa);
      if (data) {
        this.formInline[fieldEn + "_fundCode"] = data.fundCode;
        this.formInline[fieldEn + "_TEXT"] = data.fundCode + "-&-" + data.fundName;
      } else {
        this.formInline[fieldEn + "_fundCode"] = "";
        this.formInline[fieldEn + "_TEXT"] = "";
      }
    },
    checkboxChange(data, fieldEn) {
      console.log(data);
      if (data.records.length == 1) {
        let obj = data.records[0];
        this.formInline[fieldEn + "_TEXT"] = obj.fundCode + "-&-" + obj.fundName;
      } else {
        this.formInline[fieldEn + "_TEXT"] = "";
      }
    },
    checkboxAll(data, fieldEn) {
      console.log(data);
      if (data.records.length == 1) {
        let obj = data.records[0];
        this.formInline[fieldEn + "_TEXT"] = obj.fundCode + "-&-" + obj.fundName;
      } else {
        this.formInline[fieldEn + "_TEXT"] = "";
      }
    },
    getSun(val, DIM_NME, pId, p_field, c_field) {
      // console.log('父级下拉框-click',c_field,DIM_NME);
      if (DIM_NME) {
        this.formInline[p_field + "_TEXT"] = DIM_NME;
      }
      if (this.formInline[c_field]) {
        this.formInline[c_field] = "";
        this.formInline[p_field + "_TEXT"] = "";
      }
      if (this.formSelectArr2[c_field]) {
        let arr = this.formSelectArr2[c_field].filter((item) => {
          return item.DIM_PARENT_ID == pId;
        });
        this.$set(this.formSelectArr, c_field, arr);
      }
    },
    getSunClick(DIM_CDE, DIM_NME, fieldEn) {
      // console.log('普通下拉框-click');
      if (DIM_NME) {
        this.formInline[fieldEn + "_TEXT"] = DIM_NME;
      }
    },
    getSunchange(val, fieldEn, c_field) {
      // console.log('父级下拉框-change',val,fieldEn,c_field);
      if (!val) {
        this.$set(this.formSelectArr, c_field, this.formSelectArr2[c_field]);
        this.formInline[fieldEn + "_TEXT"] = "";
      }
    },
    selectChange(val, field) {
      // console.log('普通下拉框-Change',val,field);
      if (!val) {
        this.formInline[field + "_TEXT"] = "";
      }
    },
    select_multipleChange(data, field) {
      if (data.length == 0 || data.length > 1) {
        this.formInline[field + "_TEXT"] = null;
      }
    },
    submitFormValid() {
      this.$refs["formData"].validate((valid) => {
        if (valid) {
          this.submitForm();
        } else {
          return false;
        }
      });
    },
    submitForm() {
      let params = JSON.parse(JSON.stringify(this.formData));
      let params1 = commonFun.parameterSrc(this.formInline);
      for (let key in params1) {
        if (params1[key].constructor == Array) {
          if (params1[key].length == 1) {
            this.formSelectArr[key].forEach((item) => {
              if (item.DIM_CDE == params1[key][0]) {
                params1[key + "_TEXT"] = item.DIM_NME;
              }
            });
          }
        }
        if (key.indexOf("_fundCode") != -1) {
          params1[key.split("_fundCode")[0]] = params1[key];
        }
      }
      let param = {
        [this.reportCode]: params1
      };
      params.param = JSON.stringify(param);
      let filedParam = {
        [this.reportCode]: this.headerArr
      };
      params.filedParam = JSON.stringify(filedParam);
      params.ids = [this.reportCode];
      params.reportNames = this.reportName;
      params.tableCode = this.tableCode;
      this.send_loading = true;
      reportToolApi.sendMail(params).then((res) => {
        this.send_loading = false;
        if (res.data.status === 200) {
          this.$message({
            type: "success",
            message: "发送成功！"
          });
          this.$emit("close");
        } else {
          this.$message({
            type: "error",
            message: res.data.message || "发送失败！"
          });
        }
      });
    },
    closeForm() {
      this.$emit("close");
    }
  }
};
</script>

<style lang="scss" scoped>
.send_mail_form {
  .box {
    border: 1px solid #ccc;
    border-radius: 6px;
  }
}
</style>
<style lang="scss">
.send_mail_form {
  .currency_report_old_form {
    .el-form-item {
      margin-bottom: 10px !important;
      .el-form-item__content {
        .el-input {
          width: 160px !important;
        }
        .el-date-editor {
          width: 160px !important;
        }
        .el-select {
          width: 160px !important;
        }
      }
    }
    // 多选框处理
    .select_multiple {
      .el-tag {
        box-sizing: border-box;
        border-color: transparent;
        margin: 2px 0 2px 6px;
        background-color: #f0f2f5;
        display: flex;
        max-width: 59%;
        align-items: center;
        .el-select__tags-text {
          overflow: hidden;
          text-overflow: ellipsis;
        }
      }
      .el-select__input {
        display: none;
      }
    }
  }
}
</style>

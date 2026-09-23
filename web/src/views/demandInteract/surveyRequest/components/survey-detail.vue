<template>
  <div class="edit">
    <div class="editForm">
      <el-row :gutter="20">
        <el-col :span="16" :offset="6">
          <el-form
            ref="formCount"
            :model="formCount"
            label-position="right"
            label-width="auto"
          >
            <el-form-item label="机构名称">
              <el-input
                v-model.trim="formCount.orgName"
                clearable
                size="small"
                :disabled="true"
              ></el-input>
            </el-form-item>
            <el-form-item label="说明">
              <el-input
                type="textarea"
                :rows="2"
                v-model.trim="formCount.explain"
                clearable
                :disabled="true"
                placeholder="请录入尽调要求的描述"
              ></el-input>
            </el-form-item>
            <el-form-item label="文件附件">
              <el-upload
                class="upload-demo"
                action=""
                :file-list="fileAccessoryList"
                disabled
              >
                <div slot="file" slot-scope="{ file }" class="download-acitve">
                  <span>{{ file.name }}</span>
                  <i class="el-icon-download" />
                </div>
              </el-upload>
            </el-form-item>
            <el-form-item label="申请日期">
              <el-input
                v-model.trim="formCount.applyDate"
                clearable
                size="small"
                :disabled="true"
              ></el-input>
            </el-form-item>
            <el-form-item label="申请人">
              <el-input
                v-model.trim="formCount.applyPeople"
                clearable
                size="small"
                :disabled="true"
              ></el-input>
            </el-form-item>
            <el-form-item label="处理状态">
              <el-select
                v-model="formCount.status"
                class="header-search-select"
                :disabled="true"
                size="small"
              >
                <el-option
                  v-for="item in statusOptions"
                  :key="item.value"
                  :value="item.value"
                  :label="item.label"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="处理结果">
              <el-input
                v-model.trim="formCount.result"
                clearable
                size="small"
                :disabled="true"
              ></el-input>
            </el-form-item>
            <el-form-item label="尽调文件">
              <el-upload
                class="upload-demo"
                action=""
                :file-list="fileSurveyist"
                disabled
              >
                <div slot="file" slot-scope="{ file }" class="download-acitve">
                  <span>{{ file.name }}</span>
                  <i class="el-icon-download" @click="handleDownload(file)" />
                </div>
              </el-upload>
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>
    </div>
    <div slot="footer" class="dialog-footer">
      <el-row :gutter="20">
        <el-col :span="16" :offset="10">
          <el-button size="small" @click="close">取 消</el-button>
          <el-button type="primary" size="small" @click="submit"
            >确 定</el-button
          >
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import constant from "../scripts/constant.js";
export default {
  name: "EditDialog",
  props: {
    detailObj: {
      type: Object,
      default: () => {}
    },
    isDetailReset: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      formCount: {
        orgName: "",
        explain: "",
        applyDate: "",
        applyPeople: "",
        status: "",
        result: ""
      },
      fileAccessoryList: [],
      fileSurveyist: [],
      statusOptions: constant.statusOptions
    };
  },
  methods: {
    submit() {},
    close() {
      this.reset();
      this.$emit("close");
    },
    reset() {
      for (let key in this.formCount) {
        this.formCount[key] = "";
      }
      this.fileAccessoryList = [];
      this.fileSurveyist = [];
    },
    handleDownload(file) {
      console.log(file);
    }
  },
  watch: {
    detailObj: {
      handler: function(newVal) {
        if (Object.keys(newVal).length > 0) {
          this.formCount.orgName = newVal.c2 || "";
          this.formCount.explain = newVal.c3 || "";
          this.formCount.applyDate = newVal.c5 || "";
          this.formCount.applyPeople = newVal.c6 || "";
          this.formCount.status = newVal.c7 || "";
          this.formCount.result = newVal.c8 || "";
          this.formCount.result = newVal.c8 || "";

          this.fileAccessoryList = [{ name: newVal.c4 || "" }];
          this.fileSurveyist = [{ name: newVal.c9 || "" }];
        }
      },
      deep: true,
      immediate: true
    },
    isDetailReset(val) {
      if (val) {
        this.reset();
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.upload-demo {
  ::v-deep .el-upload--text {
    display: none;
  }
  ::v-deep .el-upload-list {
    margin-top: -4px;
  }
  .download-acitve {
    cursor: pointer;
  }
}
</style>

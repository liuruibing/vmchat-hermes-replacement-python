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
              ></el-input>
            </el-form-item>
            <el-form-item label="说明">
              <el-input
                type="textarea"
                :rows="2"
                v-model.trim="formCount.explain"
                clearable
                placeholder="请录入尽调要求的描述"
              ></el-input>
            </el-form-item>
            <el-form-item label="文件附件">
              <el-upload
                class="upload-demo"
                ref="upload"
                action=""
                multiple
                :file-list="fileList"
                :auto-upload="false"
              >
                <el-button slot="trigger" size="small" type="primary"
                  >选取文件</el-button
                >
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
export default {
  name: "EditDialog",
  props: {
    editObj: {
      type: Object,
      default: () => {}
    },
    isEditReset: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      formCount: {
        orgName: "",
        explain: ""
      },
      fileList: []
    };
  },
  methods: {
    submit() {},
    close() {
      this.reset();
      this.$emit("close");
    },
    reset() {
      this.formCount.orgName = "";
      this.formCount.explain = "";
      this.fileList = [];
    }
  },
  watch: {
    editObj: {
      handler: function(newVal) {
        if (Object.keys(newVal).length > 0) {
          this.formCount.orgName = newVal.c2 || "";
          this.formCount.explain = newVal.c3 || "";
          this.fileList = [{ name: newVal.c4 }];
        }
      },
      deep: true,
      immediate: true
    },
    isEditReset(val) {
      if (val) {
        this.reset();
      }
    }
  }
};
</script>

<style></style>

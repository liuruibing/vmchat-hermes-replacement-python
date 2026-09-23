<template>
  <div>
    <el-form ref="elForm" :model="formData" label-width="100px" style="margin: 0 auto">
      <el-form-item label="机构/产品名称" prop="">
        <el-input v-model="formData.fundName" size="small"></el-input>
      </el-form-item>
      <el-form-item label="申请数据类型" prop="">
        <el-select v-model="formData.dataType" placeholder="请选择" size="small">
          <el-option
            v-for="item in dataTypeOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="说明" prop="">
        <el-input
          type="textarea"
          v-model="formData.remark"
          placeholder="请录入信息验证的描述"
        ></el-input>
      </el-form-item>
      <el-form-item label="文件附件" prop="">
        <el-upload
          class="upload-demo"
				    v-model="fileList"
            ref="upload"
            name="file"
            :headers="{}"
            action=""
            :on-remove="handleRemove"
            :on-change="handleChange"
            :file-list="fileList"
            :auto-upload="false">
          <el-button size="small" type="primary">选择文件</el-button>
          <!-- <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div> -->
        </el-upload>
      </el-form-item>
    </el-form>
    <div style="text-align: center">
      <el-button size="small" type="" @click="cancel">取 消</el-button>
      <el-button size="small" type="primary">提 交</el-button>
    </div>
  </div>
</template>

<script>
export default {
  name: "",
  components: {},
  data() {
    return {
      formData: {
        fundName: "",
        dataType: "",
        remark: "",
      },
      dataTypeOptions: [
        { label: "机构信息", value: "1" },
        { label: "产品信息", value: "2" },
        { label: "产品数据", value: "3" },
      ],
      fileList: []
    };
  },
  mounted() {},
  methods: {
    handleRemove(){},
    handleChange(){},
    // 取消
    cancel() {
      this.$emit("close")
    },
    addInit(data){
      this.formData.fundName = data.fundName || ""
    },
    editInit() {
      this.$nextTick(() => {
        this.formData.fundName = "测试机构"
        this.formData.dataType = "1"
        this.formData.remark = "说明说明说明说明"
      })
    }
  }
};
</script>
<style scoped lang='scss'>
</style>
<!--
 * @Description: 
 * @Author: 
 * @Date: 2023-02-06 10:15:13
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2023-02-06 14:25:08
-->
<template>
  <div class="detail-form">
    <el-form ref="elForm" :model="formData" label-width="100px" style="margin: 0 auto" disabled>
      <el-form-item label="机构/产品名称" prop="">
        <el-input v-model="formData.fundName" size="small"></el-input>
      </el-form-item>
      <el-form-item label="信息验证类型" prop="">
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
          placeholder=""
        ></el-input>
      </el-form-item>
      <el-form-item label="文件附件" prop="">
        <el-upload
          class="upload-custom"
          action="https://jsonplaceholder.typicode.com/posts/"
          multiple
          disabled
          :file-list="fileList1">
          <div slot="file" slot-scope="{ file }" class="download-acitve">
            <span>{{ file.name }}</span>
            <i class="el-icon-download" />
          </div>
        </el-upload>
      </el-form-item>
      <el-form-item label="申请日期" prop="">
        <el-input v-model="formData.date" size="small"></el-input>
      </el-form-item>
      <el-form-item label="申请人" prop="">
        <el-input v-model="formData.sqr" size="small"></el-input>
      </el-form-item>
      <el-form-item label="处理状态" prop="">
        <el-input v-model="formData.status" size="small"></el-input>
      </el-form-item>
      <el-form-item label="处理结果" prop="">
        <el-input
          type="textarea"
          v-model="formData.cljg"
          placeholder=""
        ></el-input>
      </el-form-item>
      <el-form-item label="回馈文件" prop="">
        <el-upload
          class="upload-custom"
          action="https://jsonplaceholder.typicode.com/posts/"
          multiple
          disabled
          :file-list="fileList2">
          <div slot="file" slot-scope="{ file }" class="download-acitve">
            <span>{{ file.name }}</span>
            <i class="el-icon-download" />
          </div>
        </el-upload>
      </el-form-item>
    </el-form>
    <!-- <div style="text-align: center">
      <el-button size="small" type="">取 消</el-button>
      <el-button size="small" type="primary">提 交</el-button>
    </div> -->
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
        date: "",
        sqr: "",
        status: "",
        cljg: "",
      },
      dataTypeOptions: [],
      fileList1: [
        { name: "附件一.doc" },
        { name: "附件二.xls" },
      ],
      fileList2: [
        { name: "文件一.doc" },
        { name: "文件二.xls" },
      ]
    };
  },
  mounted() {
    this.init()
  },
  methods: {
    init(){
      this.formData.fundName = "测试机构"
      this.formData.dataType = "机构信息"
      this.formData.remark = "说明说明说明说明"
      this.formData.date = "2023-01-01"
      this.formData.sqr = "申请人"
      this.formData.status = "已提交"
      this.formData.cljg = "处理结果处理结果处理结果处理结果"
    }
  }
};
</script>
<style lang='scss'>
.detail-form{
  .upload-custom{
    .el-upload--text{
      display: none;
    }
  }
}
</style>
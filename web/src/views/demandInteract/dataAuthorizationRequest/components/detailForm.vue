<!--
 * @Description:
 * @Author:
 * @Date: 2023-02-06 10:15:13
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2023-02-06 14:39:08
-->
<template>
  <div class="detail-form">
    <el-form ref="elForm" :model="formData" label-width="100px" style="margin: 0 auto">
      <el-form-item label="产品名称" prop="fundName">
        <el-row>
          <el-col :span="11"><el-input v-model="formData.fundName" size="small" :disabled="true"></el-input></el-col>
          <el-col :span="13"><el-button type="primary" size="mini" :disabled="false">选择产品</el-button></el-col>
        </el-row>
      </el-form-item>
      <el-form-item label="产品代码" prop="fundCode">
        <el-input v-model="formData.fundCode" size="small" :disabled="true"></el-input>
      </el-form-item>
      <el-form-item label="申请数据类型" prop="dataType">
        <el-select v-model="formData.dataType" placeholder="请选择" size="small" :disabled="true">
          <el-option
            v-for="item in dataTypeOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="说明" prop="remark">
        <el-input
          type="textarea"
          v-model="formData.remark"
          placeholder=""
          :disabled="true"
        ></el-input>
      </el-form-item>
      <el-form-item label="申请日期" prop="date">
        <el-input v-model="formData.date" size="small" :disabled="true"></el-input>
      </el-form-item>
      <el-form-item label="申请人" prop="sqr">
        <el-input v-model="formData.sqr" size="small" :disabled="true"></el-input>
      </el-form-item>
      <el-form-item label="处理状态" prop="status">
        <el-input v-model="formData.status" size="small" :disabled="true"></el-input>
      </el-form-item>
      <el-form-item label="处理结果" prop="cljg">
        <el-input
          type="textarea"
          v-model="formData.cljg"
          placeholder=""
          :disabled="true"
        ></el-input>
      </el-form-item>
      <el-form-item label="回馈文件" prop="">
        <el-upload
          class="upload-custom"
          action="https://jsonplaceholder.typicode.com/posts/"
          multiple
          disabled
          :file-list="fileList">
          <div slot="file" slot-scope="{ file }" class="download-acitve">
            <span>{{ file.name }}</span>
            <i class="el-icon-download" />
          </div>
          <!-- <el-button size="small" type="primary">点击上传</el-button> -->
          <!-- <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div> -->
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
        fundCode: "",
        dataType: "",
        remark: "",
        date: "",
        sqr: "",
        status: "",
        cljg: ""
      },
      dataTypeOptions: [],
      fileList: [
        {
          name: '文件一.doc',
          url: 'https://fuss10.'
        }, {
          name: '文件二.xls',
          url: 'https://fuss10.'
        }
      ]
    };
  },
  mounted() {
    this.init()
  },
  methods: {
    init() {
      this.formData.fundName = "测试产品一号"
      this.formData.fundCode = "ZS001"
      this.formData.dataType = "净值"
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

<!--
 * @Description:
 * @Author:
 * @Date: 2023-02-06 10:14:47
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2023-02-06 15:56:17
-->
<template>
  <div>
    <el-form ref="elForm" :model="formData" label-width="100px" style="margin: 0 auto">
<!--      <el-form-item label="产品名称" prop="fundName">-->
<!--        <el-select v-model="formData.fundName" placeholder="请选择" size="small" clearable @change="fundChange">-->
<!--          <el-option-->
<!--            v-for="item in fundList"-->
<!--            :key="item.value"-->
<!--            :label="item.label"-->
<!--            :value="item.value"-->
<!--          >-->
<!--          </el-option>-->
<!--        </el-select>-->
<!--      </el-form-item>-->
      <el-form-item label="产品名称" prop="fundName">
        <el-row>
          <el-col :span="11"><el-input v-model="formData.fundName" size="small" :disabled="true"></el-input></el-col>
          <el-col :span="13"><el-button type="primary" size="mini" :disabled="false">选择产品</el-button></el-col>
        </el-row>
      </el-form-item>
      <el-form-item label="产品代码" prop="fundCode">
        <el-input v-model="formData.fundCode" size="small" disabled></el-input>
      </el-form-item>
      <el-form-item label="申请数据类型" prop="dataType">
        <el-select v-model="formData.dataType" placeholder="请选择" size="small" clearable>
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
          placeholder="请录入数据申请的描述"
        ></el-input>
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
        fundCode: "",
        dataType: "",
        remark: ""
      },
      fundList: [
        { label: "测试产品一号", value: "ZS001" },
        { label: "测试产品二号", value: "ZS002" },
        { label: "测试产品三号", value: "ZS003" },
        { label: "测试产品四号", value: "ZS004" },
      ],
      dataTypeOptions: [
        { label: "净值", value: "1" },
        { label: "持仓", value: "2" },
        { label: "风格", value: "3" },
      ]
    };
  },
  mounted() {},
  methods: {
    // 取消
    cancel() {
      this.$emit("close")
    },
    editInit() {
      this.$nextTick(() => {
        this.formData.fundName = "测试产品一号"
        this.formData.fundCode = "ZS001"
        this.formData.dataType = "1"
        this.formData.remark = "说明说明说明说明"
      })
    },
    fundChange(val) {
      this.formData.fundCode = val || ""
    }
  }
};
</script>
<style scoped lang='scss'>
</style>

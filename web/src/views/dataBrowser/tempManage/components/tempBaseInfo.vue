<!--
 * @Description: 
 * @Author: 
 * @Date: 2025-11-03 14:52:08
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2025-12-31 14:27:52
-->
<template>
  <div>
    <el-dialog :visible.sync="visible" :title="dialogTitle" width="650px !important" :close-on-click-modal="false"
      :close-on-press-escape="false" @closed="handleClose">
      <el-form :model="formData" :rules="rules" ref="form" label-width="120px">
        <el-form-item label="模板名称" prop="vcTemplateName">
          <el-input v-model.trim="formData.vcTemplateName" placeholder="请输入模板名称"></el-input>
        </el-form-item>
        <el-form-item label="模板类型" prop="vcTemplateType">
          <el-select v-model="formData.vcTemplateType" placeholder="请选择模板类型" :disabled="dialogType === 'edit'">
            <el-option v-for="item in templateTypeOptions" :key="item.dimCde" :label="item.dimNme"
              :value="item.dimCde"></el-option>
          </el-select>
        </el-form-item>
        <!-- <el-form-item label="日期类型" prop="vcDateType">
          <el-select v-model="formData.vcDateType" placeholder="请选择日期类型">
            <el-option v-for="item in dateTypeOptions" :key="item.dimCde" :label="item.dimNme"
              :value="item.dimCde"></el-option>
          </el-select>
        </el-form-item> -->
        <!-- 行业类型 -->
        <el-form-item label="行业类型" prop="industryType" v-if="['A', 'C'].includes(formData.vcTemplateType)">
          <el-select v-model="formData.industryType" placeholder="请选择行业类型" :disabled="dialogType === 'edit'">
            <el-option v-for="item in industryTypeOptions" :key="item.dimCde" :label="item.dimNme"
              :value="item.dimCde"></el-option>
          </el-select>
        </el-form-item>
        <!-- 因子类型 -->
        <el-form-item label="因子类型" prop="factorType" v-if="['A', 'C'].includes(formData.vcTemplateType)">
          <template slot="label">因子类型
            <el-tooltip content="只作用于多因子报告类型" placement="top" effect="light">
              <i class="el-icon-info"></i>
            </el-tooltip>
          </template>
          <el-select v-model="formData.factorType" placeholder="请选择因子类型" :disabled="dialogType === 'edit'">
            <el-option v-for="item in factorTypeOptionList" :key="item.dimCde" :label="item.dimNme"
              :value="item.dimCde" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="vcRemark">
          <el-input v-model.trim="formData.vcRemark" type="textarea" :rows="2" placeholder="请输入"></el-input>
        </el-form-item>
        <!-- <el-divider content-position="left">预设查询参数</el-divider>
        <el-form-item label="产品" prop="fundNames">
          <el-tooltip :content="formData.fundNames" :disabled="!formData.fundNames" placement="top-start"
            effect="light">
            <el-input v-model="formData.fundNames" placeholder="请选择产品" readonly
              @click.native="openFundListDialog"></el-input>
          </el-tooltip>
        </el-form-item>
        <el-form-item label="基准" prop="vcBenchMark">
          <el-select v-model="formData.vcBenchMark" placeholder="请选择基准" clearable>
            <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label"
              :value="item.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="数据频率" prop="vcTimeRate">
          <el-select v-model="formData.vcTimeRate" placeholder="请选择数据频率" clearable>
            <el-option v-for="item in dataFrequencyOptions" :key="item.dimCde" :label="item.dimNme"
              :value="item.dimCde"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="时间区间" prop="timeRange">
          <el-date-picker v-model="formData.timeRange" type="daterange" range-separator="至" start-placeholder="开始日期"
            end-placeholder="结束日期" value-format="yyyy-MM-dd"></el-date-picker>
        </el-form-item> -->
      </el-form>
      <div slot="footer">
        <el-button type="primary" :loading="btnLoading" @click="submitForm('form')">确定</el-button>
        <el-button @click="handleClose">取消</el-button>
      </div>
    </el-dialog>
    <!-- 产品列表弹窗 -->
    <product-selector v-if="fundListDialogVisible" :multiple="true" :leftList="false"
      :dialog-visible="fundListDialogVisible" :tree-data="treeData" :show-tree-key-array="showTreeKeyArray"
      :select-list="selectList" default-checked-keys="wdgz" @closedialog="fundListDialogVisible = false"
      @submitdialog="handleFundListSubmit"></product-selector>
  </div>
</template>

<script>
import CONSTANTS from '../../constants.js'
import productSelector from '@/components/productSelector'
import pageApi from "../api.js"
export default {
  components: {
    productSelector
  },
  data() {
    return {
      visible: false,
      dialogTitle: '新增模板',
      btnLoading: false,
      formData: {
        vcTemplateName: '',
        vcTemplateType: '',
        vcDateType: 'workDate',
        industryType: 'SWSR',
        factorType: 'CNE5',
        vcRemark: '',
        vcTimeRate: '',
        timeRange: [],
        vcBenchMark: '',
        fundNames: ''
      },
      rules: {
        vcTemplateName: [{ required: true, message: '请输入模板名称', trigger: 'change' }],
        vcTemplateType: [{ required: true, message: '请选择模板类型', trigger: 'change' }],
        vcDateType: [{ required: true, message: '请选择日期类型', trigger: 'change' }],
        industryType: [{ required: true, message: '请选择行业类型', trigger: 'change' }],
        factorType: [{ required: true, message: '请选择因子类型', trigger: 'change' }]
      },
      templateTypeOptions: CONSTANTS.TEMPTYPE,
      dateTypeOptions: CONSTANTS.DATETYPE,
      dataFrequencyOptions: CONSTANTS.DATAFREQUENCY,
      benchMarkOptions: [
        { dimCde: "000300", dimNme: "沪深300" }
      ],
      tempConfigShow: false,
      fundListDialogVisible: false,
      treeData: [
        {
          label: '产品列表',
          id: 'zstgwb'
        },
        {
          label: '我的关注',
          id: 'wdgz',
          children: [
            {
              label: '默认分组',
              id: 'mrfz'
            },
            {
              label: '权益组',
              id: 'qyz'
            }
          ]
        }
      ],
      showTreeKeyArray: ['产品列表', '我的关注'],
      selectList: [],
      industryTypeOptions: [
        { dimCde: 'SWSR', dimNme: '申万行业' },
        { dimCde: 'ZXSR', dimNme: '中信行业' }
      ],
      factorTypeOptionList: [
        { dimCde: "CNE5", dimNme: "CNE5" },
        { dimCde: "CNE6", dimNme: "CNE6" }
      ],
    }
  },
  props: {
    dialogType: {
      type: String,
      default: 'add'
    }
  },
  mounted() {
    this.visible = true
  },
  methods: {
    // 编辑回显
    init(row) {
      this.dialogTitle = '编辑模板'
      row = _.cloneDeep(row)
      this.formData.vcTemplateName = row.vcTemplateName || ""
      this.formData.vcTemplateType = row.vcTemplateType || ""
      this.formData.vcDateType = row.vcDateType || ""
      if (row.vcBenchMark) {
        try {
          const benchmarkObj = JSON.parse(row.vcBenchMark)
          this.formData.industryType = benchmarkObj.industryType || ""
          this.formData.factorType = benchmarkObj.factorType || ""
        } catch (e) {
          this.formData.industryType = "SWSR"
          this.formData.factorType = "CNE5"
        }
      } else {
        this.formData.industryType = "SWSR"
        this.formData.factorType = "CNE5"
      }
      this.formData.vcRemark = row.vcRemark || ""
      this.formData.vcTemplateId = row.vcTemplateId || ""
      // this.formData.vcTimeRate = row.vcTimeRate || ""
      // this.formData.vcBenchMark = row.vcBenchMark || ""
      if (row.dStartTime && row.dEndTime) {
        this.formData.timeRange = [row.dStartTime, row.dEndTime]
      }
      if (row.templateByFundDtos) {
        this.selectList = row.templateByFundDtos.map(item => {
          return {
            VC_FUNDCODE: item.fundCode,
            VC_FUNDNAME: item.fundName
          }
        })
        this.formData.fundNames = this.selectList.map(item => item.VC_FUNDNAME).join(',');
      }
    },
    // 关闭弹窗
    handleClose() {
      this.visible = false
      this.$emit('close')
    },
    // 提交表单
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let fundInfos = this.selectList.map((item, index) => {
            return {
              isPack: '0',
              key: item.VC_FUNDCODE,
              fundCode: item.VC_FUNDCODE,
              fundName: item.VC_FUNDNAME,
              source: '',
              weight: '',
              more: "{}",
              fOrder: index
            }
          })
          const benchmarkObj = {
            industryType: this.formData.industryType,
            factorType: this.formData.factorType
          }
          const params = {
            vcTemplateName: this.formData.vcTemplateName,
            vcTemplateType: this.formData.vcTemplateType,
            vcDateType: this.formData.vcDateType,
            vcRemark: this.formData.vcRemark || '',
            dStartTime: this.formData.timeRange[0] || '',
            dEndTime: this.formData.timeRange[1] || '',
            vcTimeRate: this.formData.vcTimeRate || '',
            vcBenchMark: JSON.stringify(benchmarkObj),
            vcFundInfos: fundInfos
          }
          console.log(params);
          if (this.dialogType === 'add') {
            this.$emit('addTempConfig', params)
            this.$emit('close')
          } else {
            this.editSave(params)
          }
        }
      })
    },
    // 打开模板配置
    openTempConfig() {
      this.tempConfigShow = true
    },
    // 编辑保存
    editSave(params) {
      params = _.cloneDeep(params);
      params.vcTemplateId = this.formData.vcTemplateId
      this.btnLoading = true;
      pageApi.updateTemplateInfo(params).then(res => {
        const { status, message } = res.data;
        if (status === 200) {
          this.$emit('close');
          this.$emit('refresh');
          this.$message.success(message || "操作成功");
        } else {
          this.$message.error(message || "操作失败");
        }
      }).finally(() => {
        this.btnLoading = false;
      })
    },
    // 打开产品列表弹窗
    openFundListDialog() {
      this.fundListDialogVisible = true
    },
    handleFundListSubmit(data) {
      console.log(data)
      this.selectList = data
      this.formData.fundNames = data.map((item) => item.VC_FUNDNAME).join(',')
      this.fundListDialogVisible = false
    }
  }
}
</script>

<style></style>
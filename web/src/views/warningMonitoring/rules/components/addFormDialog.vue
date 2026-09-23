<!--
 * @Description:
 * @Author:
 * @Date: 2024-06-27 17:46:38
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2024-07-29 13:54:41
-->
<template>
  <div id="rule_add_dialog">
    <el-dialog
      custom-class="warningMonitoring-dialog"
      :title="modalType === 'edit' ? '编辑' : '新增'"
      :visible.sync="visible"
      width="800px !important"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      @close="handleClose"
    >
      <el-form :model="formData" :rules="rules" ref="formData" label-width="150px" class="standard-form" style="width: 100% !important">
        <el-row>
          <el-col :span="24">
            <el-form-item label="预警规则名称" prop="rulename">
              <el-input v-model="formData.rulename" size="small" placeholder="请输入" style="width: 520px !important"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="指标名称" prop="itcode">
              <!-- <el-input v-model="formData.codeAndName" size="small" placeholder="请选择"></el-input> -->
              <SelectTable
                ref="SelectTable"
                v-model="formData.itcode"
                :data="indexList"
                :Columns="Columns"
                size="small"
                width="600px"
                value-field="itcode"
                label-field="itname"
                placeholder="请选择"
                @change="indexChange"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="监控对象类型" prop="ittype">
              <el-select v-model="formData.ittype" size="small" placeholder="" disabled>
                <el-option v-for="item in CONSTANTS.ittypeList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <div v-if="l1Itname === '指标预警'">
          <el-row>
            <el-col :span="12">
              <el-form-item label="运算符" prop="warnOp1">
                <el-select v-model="formData.warnOp1" size="small" clearable filterable placeholder="请选择">
                  <el-option v-for="item in CONSTANTS.warnOpList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12" style="position: relative">
              <el-form-item label="预警阀值" prop="warnVal1">
                <el-input v-model="formData.warnVal1" size="small" placeholder="请输入">
                  <template slot="append" v-if="formData.itunit">
                    <span v-if="formData.itunit === '1'">%</span>
                    <span v-else-if="formData.itunit === '2'">元</span>
                    <span v-else></span>
                  </template>
                </el-input>
              </el-form-item>
              <i v-if="!formData.warnOprel" class="el-icon-circle-plus" style="position: absolute; right: 50px; top: 12px" @click="onMoreShow"></i>
            </el-col>
          </el-row>
          <div v-if="formData.warnOprel">
            <el-form-item prop="warnOprel">
              <el-radio-group v-model="formData.warnOprel">
                <el-radio label="1">并且</el-radio>
                <el-radio label="2">或者</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-row>
              <el-col :span="12">
                <el-form-item label="运算符" prop="warnOp2">
                  <el-select v-model="formData.warnOp2" size="small" clearable filterable placeholder="请选择">
                    <el-option v-for="item in CONSTANTS.warnOpList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="预警阀值" prop="warnVal2">
                  <el-input v-model="formData.warnVal2" size="small" placeholder="请输入">
                    <template slot="append" v-if="formData.itunit">
                      <span v-if="formData.itunit === '1'">%</span>
                      <span v-else-if="formData.itunit === '2'">元</span>
                      <span v-else></span>
                    </template>
                  </el-input>
                </el-form-item>
                <i class="el-icon-remove" style="position: absolute; right: 50px; top: 12px" @click="onRemoveMore"></i>
              </el-col>
            </el-row>
          </div>
        </div>
        <el-form-item label="风险等级" prop="warnLevel">
          <el-radio-group v-model="formData.warnLevel">
            <el-radio v-for="(item, index) in CONSTANTS.warnLevelList" :key="index" :label="item.dimCde">{{ item.dimNme }}</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="邮件提醒规则" prop="emailRule">
          <el-radio-group v-model="formData.emailRule">
            <el-radio v-for="(item, index) in CONSTANTS.emailRuleList" :key="index" :label="item.dimCde">{{ item.dimNme }}</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="是否启用" prop="itdisable">
          <el-radio-group v-model="formData.itdisable">
            <el-radio v-for="(item, index) in CONSTANTS.itdisableList" :key="index" :label="item.dimCde">{{ item.dimNme }}</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注" prop="itremark">
          <el-input type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="请输入" v-model="formData.itremark" style="width: 520px !important"></el-input>
        </el-form-item>
        <div style="text-align: center; margin-top: 20px">
          <el-button size="small" plain type="info" @click="handleClose()" :disabled="btnDisabled">取 消</el-button>
          <el-button size="small" type="primary" @click="submitForm()" :disabled="btnDisabled">确 认</el-button>
        </div>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import CONSTANTS from '../scripts/constants.js'
import SelectTable from '@/components/SelectTable'
import pageApi from '../scripts/api.js'
export default {
  name: '',
  components: {
    SelectTable
  },
  props: {
    indexList: {
      type: Array,
      default: () => []
    }
  },
  data() {
    const warnVal1Validator = (rule, value, callback) => {
      if (!value) {
        callback()
      }
      if (this.formData.itunit == '1') {
        const regex = /^-?\d$|^-?\d+\.?\d{1,4}$/
        if (!regex.test(value)) {
          callback(new Error('请输入数字，最多4位小数'))
        }
        if (!isNaN(value)) {
          if (Number(value) > 100 || Number(value) < -100) {
            callback(new Error('请输入-100 ~ 100之间的数字'))
          }
        }
      } else {
        const regex = /^\d$|^\d+\.?\d{1,4}$/
        if (!regex.test(value)) {
          callback(new Error('请输入数字，最多4位小数'))
        }
      }
      callback()
    }
    const warnVal2Validator = (rule, value, callback) => {}
    return {
      visible: true,
      CONSTANTS,
      modalType: 'add',
      rowData: {},
      formData: {
        rulename: '',
        itcode: '',
        codeAndName: '',
        ittype: '',
        warnOp1: '',
        warnVal1: '',
        warnOprel: '',
        warnOp2: '',
        warnVal2: '',
        itunit: '',
        warnLevel: '1',
        emailRule: '1',
        itdisable: 1,
        itremark: ''
      },
      l1Itname: '',
      rules: {
        rulename: [{ required: true, message: '请输入预警规则名称', trigger: 'change' }],
        itcode: [{ required: true, message: '请选择指标', trigger: 'change' }],
        warnOp1: [{ required: true, message: '请选择运算符', trigger: 'change' }],
        warnVal1: [
          { required: true, message: '请输入预警阀值', trigger: 'change' },
          // { pattern: /^\d$|^\d+\.?\d+$/, trigger: 'change', message: '请输入数字' },
          { validator: warnVal1Validator, trigger: 'change' }
        ],
        warnOp2: [{ required: true, message: '请选择运算符', trigger: 'change' }],
        warnVal2: [
          { required: true, message: '请输入预警阀值', trigger: 'change' },
          // { pattern: /^\d$|^\d+\.?\d+$/, trigger: 'change', message: '请输入数字' },
          { validator: warnVal1Validator, trigger: 'change' }
        ],
        warnLevel: [{ required: true, message: '请选择', trigger: 'change' }],
        emailRule: [{ required: true, message: '请选择', trigger: 'change' }],
        itdisable: [{ required: true, message: '请选择', trigger: 'change' }]
      },
      // indexList: [],
      Columns: [
        { label: '一级类型', prop: 'l1Itname', filter: 'select', filterOption: [] },
        { label: '二级类型', prop: 'l2Itname', filter: 'select', parent: 'l1Itname', filterOption: [] },
        { label: '指标编码', prop: 'itcode' },
        { label: '指标名称', prop: 'itname' }
      ],
      moreShow: false,
      btnDisabled: false
    }
  },
  mounted() {
    // this.getIndexList()
    this.setColumns()
  },
  methods: {
    setColumns() {
      let level1List = this.indexList.filter((item) => item.l1Itname).map((item) => item.l1Itname)
      let level2List = this.indexList.filter((item) => item.l2Itname).map((item) => item.l2Itname)
      level1List = Array.from(new Set(level1List))
      level2List = Array.from(new Set(level2List))
      this.Columns[0].filterOption = level1List
      this.Columns[1].filterOption = level2List
    },
    // getIndexList() {
    //   pageApi.itemList({}).then((res) => {
    //     const { data, status } = res.data
    //     if (status === 0) {
    //       this.indexList = data || []
    //       let level1List = this.indexList.filter((item) => item.l1Itname).map((item) => item.l1Itname)
    //       let level2List = this.indexList.filter((item) => item.l2Itname).map((item) => item.l2Itname)
    //       level1List = Array.from(new Set(level1List))
    //       level2List = Array.from(new Set(level2List))
    //       this.Columns[0].filterOption = level1List
    //       this.Columns[1].filterOption = level2List
    //       if (this.modalType === 'edit') {
    //         const currentItObj = this.indexList.find((item) => item.itcode === this.rowData.itcode) || {}
    //         this.l1Itname = currentItObj.l1Itname || ''
    //       }
    //     } else {
    //       this.indexList = []
    //     }
    //   })
    // },
    // 回显
    init(data) {
      this.modalType = 'edit'
      this.rowData = JSON.parse(JSON.stringify(data))
      for (let key in this.formData) {
        this.formData[key] = data[key] || ''
      }
      if (data.itdisable === 0) {
        this.formData.itdisable = 0
      }
      const currentItObj = this.indexList.find((item) => item.itcode === data.itcode) || {}
      this.l1Itname = currentItObj.l1Itname || ''
    },
    indexChange(data) {
      this.formData.ittype = data.ittype || ''
      this.formData.itunit = data.itunit || ''
      this.l1Itname = data.l1Itname || ''
      this.formData.warnOp1 = ''
      this.formData.warnVal1 = ''
      this.formData.warnOprel = ''
      this.formData.warnOp2 = ''
      this.formData.warnVal2 = ''
    },
    // 显示更多
    onMoreShow() {
      this.formData.warnOprel = '1'
    },
    // 关闭更多
    onRemoveMore() {
      this.formData.warnOprel = ''
      this.formData.warnOp2 = ''
      this.formData.warnVal2 = ''
    },
    // 关闭dialog
    handleClose() {
      this.$emit('close')
      this.visible = false
    },
    submitForm() {
      this.$refs['formData'].validate((valid) => {
        if (valid) {
          if (this.modalType === 'add') {
            this.onSubmit()
          }
          if (this.modalType === 'edit') {
            this.editSubmit()
          }
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    // 新增提交
    onSubmit() {
      this.$message.closeAll()
      let params = JSON.parse(JSON.stringify(this.formData))
      if (params.warnVal1) {
        params.warnVal1 = Number(params.warnVal1)
      }
      if (params.warnVal2) {
        params.warnVal2 = Number(params.warnVal2)
      }
      // console.log(params); return
      this.btnDisabled = true
      pageApi.insert(params).then((res) => {
        this.btnDisabled = false
        const { status, message } = res.data
        if (status === 200) {
          this.$message({
            type: 'success',
            message: message || '新增成功',
            customClass: 'message-success'
          })
          this.$emit('refresh')
          this.handleClose()
        } else {
          this.$message({
            customClass: 'message-error',
            type: 'error',
            message: message || '新增失败'
          })
        }
      })
    },
    // 编辑提交
    editSubmit() {
      this.$message.closeAll()
      let params = JSON.parse(JSON.stringify(this.formData))
      if (params.warnVal1) {
        params.warnVal1 = Number(params.warnVal1)
      }
      if (params.warnVal2) {
        params.warnVal2 = Number(params.warnVal2)
      }
      params.id = this.rowData.id || ''
      this.btnDisabled = true
      pageApi.update(params).then((res) => {
        this.btnDisabled = false
        const { status, message } = res.data
        if (status === 200) {
          this.$message({
            type: 'success',
            message: message || '编辑成功',
            customClass: 'message-success'
          })
          this.$emit('refresh')
          this.handleClose()
        } else {
          this.$message({
            customClass: 'message-error',
            type: 'error',
            message: message || '编辑失败'
          })
        }
      })
    }
  }
}
</script>
<style lang="scss"></style>

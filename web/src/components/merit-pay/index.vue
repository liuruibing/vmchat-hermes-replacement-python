<template>
  <div class="merit-pay">
    <div class="fund-name mb20">{{ curFundRow.VC_FUNDNAME || '-' }}</div>
    <div class="standard-form">
      <div class="radio-choose">
        <span>业绩报酬公式：</span>
        <el-radio v-model="curRadio" v-for="item in radioOptions" :key="item.value" :label="item.value">{{ item.label }}</el-radio>
      </div>
      <div v-if="curRadio === 'A'" class="mt20"></div>
      <div v-if="curRadio === 'B'" class="mt20">
        <el-form ref="fixRatioForm" :model="fixRatioForm">
          <el-form-item
            label="计提比例"
            label-width="100px"
            prop="fixRatio"
            :rules="{
              required: true,
              validator: validateRatio
            }"
          >
            <el-input
              size="small"
              type="text"
              v-model="fixRatioForm.fixRatio"
              style="width: 300px !important"
              onkeyup="value=value.replace(/[^0-9.]/g,'').replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3')"
            >
              <span slot="append">%</span>
            </el-input>
          </el-form-item>
        </el-form>
      </div>
      <div v-if="curRadio === 'C'" class="mt20">
        <el-form ref="yearForm" :model="yearForm" style="width: 100% !important">
          <el-row v-for="(item, index) in yearForm.rows" :key="index">
            <el-col :span="4">
              <el-form-item>
                <el-input
                  size="small"
                  type="text"
                  :disabled="true"
                  v-model="yearForm.rows[index].min"
                  style="width: 200px !important"
                  onkeyup="value=value.replace(/[^0-9.]/g,'').replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3')"
                >
                  <span slot="append">%</span>
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="4" style="margin-left: 30px; text-align: center; height: 35px; line-height: 35px; font-size: 14px">
              <template v-if="yearForm.rows && index === yearForm.rows.length - 1">
                <span v-text="txtNoEnd" style=""></span>
              </template>
              <template v-else>
                <span v-text="txt" style=""></span>
              </template>
            </el-col>
            <el-col :span="4">
              <el-form-item
                v-if="yearForm.rows && index !== yearForm.rows.length - 1"
                :prop="'rows.' + index + '.max'"
                :rules="{
                  required: true,
                  validator: validateMax
                }"
              >
                <el-input
                  size="small"
                  type="text"
                  v-model="yearForm.rows[index].max"
                  style="width: 200px !important"
                  onkeyup="value=value.replace(/[^0-9.]/g,'').replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3')"
                  @change="handleYearMaxChange(index)"
                >
                  <span slot="append">%</span>
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="2" style="height: 35px"></el-col>
            <el-col :span="7">
              <el-form-item
                label="计提比例"
                label-width="100px"
                :prop="'rows.' + index + '.ratio'"
                :rules="{
                  required: true,
                  validator: validateRatio
                }"
              >
                <el-input
                  size="small"
                  type="text"
                  v-model="yearForm.rows[index].ratio"
                  style="width: 200px !important"
                  onkeyup="value=value.replace(/[^0-9.]/g,'').replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3')"
                >
                  <span slot="append">%</span>
                </el-input>
              </el-form-item>
            </el-col>
            <span style="position: absolute; top: 5px; right: 25px; cursor: pointer">
              <i class="el-icon-circle-plus" style="padding-right: 10px" @click="addRows('year', item)" v-show="yearForm.rows.length < 5"></i>
              <i class="el-icon-delete" @click="deleteRows('year', index)" v-show="index === yearForm.rows.length - 1 && index !== 0"></i>
            </span>
          </el-row>
        </el-form>
      </div>
      <div v-if="curRadio === 'D'" class="mt20">
        <div class="mb20">
          <span>基准指数：</span>
          <el-select v-model="excessYearForm.contrasCode" filterable placeholder="请选择" size="small">
            <el-option v-for="item in contrasStandardOpts" :key="item.id" :label="item.label" :value="item.id"></el-option>
          </el-select>
        </div>
        <el-form ref="excessYearForm" :model="excessYearForm" style="width: 100% !important">
          <el-row v-for="(item, index) in excessYearForm.rows" :key="index">
            <el-col :span="4">
              <el-form-item>
                <el-input
                  size="small"
                  type="text"
                  v-model="excessYearForm.rows[index].min"
                  style="width: 200px !important"
                  onkeyup="value=value.replace(/[^0-9.]/g,'').replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3')"
                  :disabled="true"
                >
                  <span slot="append">%</span>
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="4" style="margin-left: 30px; text-align: center; height: 35px; line-height: 35px; font-size: 14px">
              <template v-if="excessYearForm.rows && index === excessYearForm.rows.length - 1">
                <span v-text="txtNoEnd" style=""></span>
              </template>
              <template v-else>
                <span v-text="txt" style=""></span>
              </template>
            </el-col>
            <el-col :span="4">
              <el-form-item
                v-if="excessYearForm.rows && index !== excessYearForm.rows.length - 1"
                :prop="'rows.' + index + '.max'"
                :rules="{
                  required: true,
                  validator: validateMaxExcess
                }"
              >
                <el-input
                  size="small"
                  type="text"
                  v-model="excessYearForm.rows[index].max"
                  style="width: 200px !important"
                  onkeyup="value=value.replace(/[^0-9.]/g,'').replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3')"
                  @change="handleExcessYearMaxChange(index)"
                >
                  <span slot="append">%</span>
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="2" style="height: 35px"></el-col>
            <el-col :span="7">
              <el-form-item
                label="计提比例"
                label-width="105px"
                :prop="'rows.' + index + '.ratio'"
                :rules="{
                  required: true,
                  validator: validateRatio
                }"
              >
                <el-input
                  size="small"
                  type="text"
                  v-model="excessYearForm.rows[index].ratio"
                  style="width: 200px !important"
                  onkeyup="value=value.replace(/[^0-9.]/g,'').replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3')"
                >
                  <span slot="append">%</span>
                </el-input>
              </el-form-item>
            </el-col>
            <span style="position: absolute; top: 5px; right: 25px; cursor: pointer">
              <i class="el-icon-circle-plus" style="padding-right: 10px" @click="addRows('excessYear', item)" v-show="excessYearForm.rows.length < 5"></i>
              <i class="el-icon-delete" @click="deleteRows('excessYear', index)" v-show="index === excessYearForm.rows.length - 1 && index !== 0"></i>
            </span>
          </el-row>
        </el-form>
      </div>
    </div>
    <div style="text-align: center" class="standard-form">
      <el-button size="small" type="primary" @click="saveMeritPay">提 交</el-button>
    </div>
  </div>
</template>

<script>
import request from '@/utils/request'
import pageAPI from './scripts/api'
import BoxTemplate from '../../views/home/components/boxTemplate'

export default {
  name: 'MeritPay',
  components: { BoxTemplate },
  props: {
    subCombineCode: {
      type: String,
      default: ''
    },
    curFundRow: {
      type: Object,
      default: () => {}
    }
  },
  watch: {
    curFundRow: {
      handler(val) {
        console.log(val)
        this.queryMeritPayDetail(val)
      },
      deep: true,
      immediate: true
    }
  },
  data() {
    return {
      txt: '<= 年化收益 <',
      txtNoEnd: '<= 年化收益',
      curRadio: 'A',
      radioOptions: [
        {
          label: '无',
          value: 'A'
        },
        {
          label: '按固定比例计提',
          value: 'B'
        },
        {
          label: '按年化收益梯度计提',
          value: 'C'
        },
        {
          label: '按超额年化收益梯度计提',
          value: 'D'
        }
      ],
      fixRatioForm: {
        fixRatio: ''
      },
      yearForm: {
        rows: [
          {
            min: '0',
            max: '',
            ratio: ''
          }
        ]
      },
      excessYearForm: {
        contrasCode: '000905',
        rows: [
          {
            min: '0',
            max: '',
            ratio: ''
          }
        ]
      },
      contrasStandardOpts: []
    }
  },
  mounted() {
    this.getContrasOptions()
  },
  methods: {
    handleYearMaxChange(index) {
      // 如果是最后一个下表直接 退出
      if (this.yearForm.rows.length === index + 1) {
        return
      }
      // 否则 就更新下一个的min值
      this.yearForm.rows[index + 1].min = this.yearForm.rows[index].max
    },

    handleExcessYearMaxChange(index) {
      // 如果是最后一个下表直接 退出
      if (this.excessYearForm.rows.length === index + 1) {
        return
      }
      // 否则 就更新下一个的min值
      this.excessYearForm.rows[index + 1].min = this.excessYearForm.rows[index].max
    },
    /**
     * @description 查询业绩报酬详情
     */
    queryMeritPayDetail(val) {
      const data = {
        combineCode: val.combineCode || this.subCombineCode,
        fundCode: val.fundCode || val.VC_FUNDCODE,
        fundType: val.fundType
      }
      pageAPI.selectPayRate(data).then((res) => {
        const { status, data } = res.data
        if (status === 0 && data.length) {
          this.curRadio = data[0].rateType
          if (this.curRadio === 'B') {
            this.fixRatioForm.fixRatio = data[0].rate
          } else if (this.curRadio === 'C') {
            this.yearForm.rows = data.map((item) => {
              return {
                min: item.yieldMin,
                max: item.yieldMax,
                ratio: item.rate
              }
            })
          } else if (this.curRadio === 'D') {
            this.excessYearForm.contrasCode = data[0].beCode
            this.excessYearForm.rows = data.map((item) => {
              return {
                min: item.yieldMin,
                max: item.yieldMax,
                ratio: item.rate
              }
            })
          }
        }
      })
    },
    /**
     * @description 保存业绩报酬
     */
    saveMeritPay() {
      const paramsMaps = {
        A: [
          {
            combineCode: this.curFundRow.combineCode || this.subCombineCode,
            fundCode: this.curFundRow.fundCode || this.curFundRow.VC_FUNDCODE,
            fundType: this.curFundRow.fundType,
            rateType: this.curRadio,
            beCode: '',
            levelNumber: 0,
            rate: 0,
            yieldMax: 0,
            yieldMin: 0
          }
        ],
        B: [
          {
            combineCode: this.curFundRow.combineCode || this.subCombineCode,
            fundCode: this.curFundRow.fundCode || this.curFundRow.VC_FUNDCODE,
            fundType: this.curFundRow.fundType,
            rateType: this.curRadio,
            beCode: '',
            levelNumber: 1,
            rate: Number(this.fixRatioForm.fixRatio),
            yieldMax: 0,
            yieldMin: 0
          }
        ]
      }
      if (this.curRadio === 'A') {
        this.apiRef(paramsMaps)
      }
      if (this.curRadio === 'B') {
        this.$refs.fixRatioForm.validate((vaild) => {
          if (vaild) {
            this.apiRef(paramsMaps)
          }
        })
      }
      if (this.curRadio === 'C') {
        const data = this.yearForm.rows.map((item, index) => {
          return {
            combineCode: this.curFundRow.combineCode || this.subCombineCode,
            fundCode: this.curFundRow.fundCode || this.curFundRow.VC_FUNDCODE,
            fundType: this.curFundRow.fundType,
            rateType: this.curRadio,
            beCode: '',
            levelNumber: Number(index) + 1,
            rate: Number(item.ratio),
            yieldMax: item.max === '' ? '' : Number(item.max),
            yieldMin: Number(item.min)
          }
        })
        paramsMaps['C'] = data
        this.$refs.yearForm.validate((vaild) => {
          if (vaild) {
            this.apiRef(paramsMaps)
          }
        })
      }
      if (this.curRadio === 'D') {
        const data = this.excessYearForm.rows.map((item, index) => {
          return {
            combineCode: this.curFundRow.combineCode || this.subCombineCode,
            fundCode: this.curFundRow.fundCode || this.curFundRow.VC_FUNDCODE,
            fundType: this.curFundRow.fundType,
            rateType: this.curRadio,
            beCode: this.excessYearForm.contrasCode,
            levelNumber: Number(index) + 1,
            rate: Number(item.ratio),
            yieldMax: item.max === '' ? '' : Number(item.max),
            yieldMin: Number(item.min)
          }
        })
        paramsMaps['D'] = data
        this.$refs.excessYearForm.validate((vaild) => {
          if (vaild) {
            this.apiRef(paramsMaps)
          }
        })
      }
    },
    apiRef(paramsMaps) {
      pageAPI.updatePayRate(paramsMaps[this.curRadio]).then((res) => {
        const { status, message } = res.data
        if (status === 0) {
          this.$message({
            type: 'success',
            message: message || '操作成功',
            customClass: 'message-success'
          })
          this.$emit('closeDialog')
        } else {
          this.$message({
            type: 'error',
            message: message || '操作失败',
            customClass: 'message-error'
          })
        }
      })
    },
    /**
     * @description 年化收益校验
     */
    validateMax(rule, value, callback) {
      if (value === '') {
        callback(new Error('请填写最大区间值'))
      } else if (Number(value) > 999) {
        callback(new Error('年化收益不可超过999'))
      } else {
        const index = rule.field.split('.')[1]
        if (this.yearForm.rows[index].min !== null || this.yearForm.rows[index].min !== undefined || this.yearForm.rows[index].min !== '') {
          const max = Number(value)
          const min = Number(this.yearForm.rows[index].min)
          if (min >= max) {
            callback(new Error('最大区间值不可小于最小区间值'))
          } else {
            callback()
          }
        } else {
          callback()
        }
      }
    },
    /**
     * @description 年化收益校验
     */
    validateMaxExcess(rule, value, callback) {
      if (value === '') {
        callback(new Error('请填写最大区间值'))
      } else if (Number(value) > 999) {
        callback(new Error('年化收益不可超过999'))
      } else {
        const index = rule.field.split('.')[1]
        if (this.excessYearForm.rows[index].min !== null || this.excessYearForm.rows[index].min !== undefined || this.excessYearForm.rows[index].min !== '') {
          const max = Number(value)
          const min = Number(this.excessYearForm.rows[index].min)
          if (min >= max) {
            callback(new Error('最大区间值不可小于最小区间值'))
          } else {
            callback()
          }
        } else {
          callback()
        }
      }
    },
    /**
     * @description 计提比例校验
     */
    validateRatio(rule, value, callback) {
      if (value === '') {
        callback(new Error('请填写计提比例'))
      } else if (Number(value) > 100) {
        callback(new Error('计提比例不可超过100'))
      } else {
        callback()
      }
    },
    /**
     * @description 获取对比基准下拉
     */
    getContrasOptions() {
      request({
        url: `/api/report/v1.0/data/sql/ecd8867c-64cc-4ebc-9070-04524b04b72c`,
        method: 'post',
        data: {
          indexCode: 'ecd8867c-64cc-4ebc-9070-04524b04b72c',
          fundCode: this.fundCode
        }
      })
        .then((res) => {
          if (res.data.status === 0) {
            const resultDim = res.data.data || []
            this.contrasStandardOpts = resultDim.map((item) => {
              return {
                label: item.DIM_NME,
                id: item.DIM_CDE,
                checked: false,
                defaultChecked: item.ISDEFAULT == '1' ? true : false
              }
            })
          }
        })
        .catch((err) => {
          reject(err)
        })
    },
    /**
     * @description 新增行
     */

    addRows(form, rows) {
      if (Number(rows.max) === 999) {
        this.$message.error('年化收益已达上限')
        return
      }
      if (form === 'excessYear') {
        this.$refs.excessYearForm.validate((vaild) => {
          if (vaild) {
            this.excessYearForm.rows.push({
              min: rows.max,
              max: '',
              ratio: ''
            })
          }
        })
      } else {
        this.$refs.yearForm.validate((vaild) => {
          if (vaild) {
            this.yearForm.rows.push({
              min: rows.max,
              max: '',
              ratio: ''
            })
          }
        })
      }
    },
    /**
     * @description 删除行
     */
    deleteRows(form, index) {
      if (form === 'excessYear') {
        this.excessYearForm.rows.splice(index, 1)
      } else {
        this.yearForm.rows.splice(index, 1)
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.merit-pay {
  .fund-name {
    // color: #e03d3e;
    font-size: 16px;
  }
}

::v-deep .el-radio__input.is-checked .el-radio__inner {
  background: #0F65DD;
  border-color: #0F65DD;
}

::v-deep .el-radio__input.is-checked + .el-radio__label {
  color: #0F65DD;
}

::v-deep .el-icon-circle-plus,
::v-deep .el-icon-delete {
  font-size: 16px;
}
</style>

<template>
  <div class="editPrivateIndexComponent">
    <el-form  ref="formData" :model="formData" :rules="rules" class="standard-form" label-width="auto">




      <el-row>
          <el-col :span="24">

          <el-form-item label="私募指数" prop="indexCode" >
            <el-select v-model="formData.indexCode" size="medium" clearable filterable placeholder="请选择私募指数">
              <el-option v-for="item in indexListOptions" :key="item.indexCode" :label="item.indexName" :value="item.indexCode" :disabled="isEdit" />
            </el-select>
          </el-form-item>
          </el-col>
      </el-row>
        <el-row>
        <el-col :span="24">
          <el-form-item label="证券大类" prop="symbolType">
            <el-radio-group v-model="formData.symbolType" class="margin_radio_label">
              <el-radio
                v-for="item in symbolTypeArr"
                :key="item.dimCde"
                :label="item.dimCde"
                :disabled="isEdit"
              >{{ item.dimNme }}</el-radio>
            </el-radio-group>

          </el-form-item>
        </el-col>
      </el-row>
      <div v-if="formData.symbolType==='PRODUCT'">
      <el-row>
        <el-col :span="10">
          <el-form-item label="产品代码" prop="fundNames">
            <el-tooltip :content="formData.fundNames" :disabled="!formData.fundNames" effect="dark" placement="top-start">
              <el-input size="medium" v-model.trim="formData.fundNames"   clearable placeholder="请选择产品"  @click.native="openFundListDialog" @change="handleFundNamesChange" :disabled="isEdit" />
            </el-tooltip>
          </el-form-item>
        </el-col>
      </el-row>
      </div>
      <div v-if="formData.symbolType!=='PRODUCT'">
      <el-row>
        <el-col :span="24">
            <el-form-item label="指数代码" prop="symbolCode">
              <el-select v-model="formData.symbolCode" size="medium" clearable filterable placeholder="请选择指数">
                <el-option v-for="item in applyIndexListOptions" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" :disabled="isEdit"/>
              </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">

          <el-form-item label="权重%" prop="symbolWeight">
            <el-input-number v-model="formData.symbolWeight" size="medium" clearable filterable placeholder="请输入权重"></el-input-number>

          </el-form-item>

        </el-col>
      </el-row>
      </div>

      <el-row>
        <el-col :span="24">
          <el-form-item label="起止日期" prop="ddate_">
            <el-date-picker
              v-model="formData.ddate_"
              type="daterange"
              value-format="yyyy-MM-dd"
              align="left"
              size="small"
              unlink-panels
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              popper-class="popperDateShortTP"
              :picker-options="dateShortTPCTA()"
            ></el-date-picker>

          </el-form-item>
        </el-col>
      </el-row>

    </el-form>
    <div style="text-align: center;padding-top: 20px;padding-bottom: 20px;" class="standard-form">
      <el-button size="small" type="primary" @click="handleSave">提 交</el-button>
      <el-button size="small" type="info" plain @click="cancel">取 消</el-button>
    </div>
    <product-selector
      :multiple="true"
      :leftList="false"
      :dialog-visible="dialogMask"
      :tree-data="treeData"
      :show-tree-key-array="showTreeKeyArray"
      :select-list="selectList"
      default-checked-keys="wdgz"
      @closedialog="handleDialogClosed"
      @submitdialog="handleSubmitClick"
    ></product-selector>
  </div>
</template>

<script>

import {
  insertPrivateIndexComponent,
  updatePrivateIndexComponent,
  selectPrivateIndexList
} from '../scripts/api'
import { generatePrivateIndexCode } from '../scripts/api'
import commonApi from "@/api/common";
import moment from 'moment'
import productSelector from '@/components/productSelector'



export default {
  name: 'editPrivateIndexComponent',
  components: {
    productSelector
  },
  props: {
    curRow: {
      type: Object,
      default: () => {}
    },
    isEdit: {
      type: Boolean,
      default: false
    },


  },
  watch: {
    curRow: {
      handler(val) {
        if (val) {
            for (const key in this.formData) {
              if(val[key] && val[key]!== undefined) {
                this.formData[key] = val[key]
              }
            }
            if(this.formData.beginDate!=='' || this.formData.endDate!==''){
              this.formData.ddate_=[this.formData.beginDate,this.formData.endDate]
            }
            if(this.formData.symbolName!==''){
              this.formData.fundNames=this.formData.symbolName
            }
            if(this.formData.symbolCode!='') {
              this.formData.fundCodes = [this.formData.symbolCode]
            }
        }
      },
      deep: true,
      immediate: true
    },

  },

  mounted() {
    // 查询表格
    this.getPrivateIndexListOptions();
    this.getApplyIndexListOptions();
  },


  data() {

    return {
      // form表单绑定
      below:{
        index:"dwjz",
        fundS:[],
        fundCodes:[],
        fundNames:[]
      },
     formData: {
       ddate_:[],
       beginDate:'',
       endDate:'',
       indexCode:'',
       symbolCode:'',
       symbolName:'',
       symbolWeight:'',
       symbolType:'PRODUCT',
       fundNames:'',
       fundCodes:[],
       id:'',
      },
      indexListOptions:[],
      applyIndexListOptions:[],
      dialogMask: false,
      symbolTypeArr:[{'dimCde':'PRODUCT','dimNme':'产品'},{'dimCde':'INDEX','dimNme':'指数'}],
      // 校验规则
      rules: {
        indexCode: [
          { required: true, message: '指数代码不能为空', trigger: 'blur' },
        ],
        ddate_: [
           { required: true, message: "请选择日期", trigger: "change" } ,
        ],

      },
      treeData: [
        {
          label: '产品列表',
          id: 'zstgwb'
        },{
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
      showTreeKeyArray: ['产品列表','我的关注'],
      selectList: [],
    }
  },
  methods: {
    // 点击弹窗
    openFundListDialog() {
      this.dialogMask = true;
    },
    handleDialogClosed() {
      this.dialogMask = false
    },
    handleFundNamesChange(val) {
      if (!val) {
        this.tags = [];
        this.formData.fundCodes = [];
        this.formData.fundNames = "";
      }
    },
    handleSubmitClick(arr) {
      const self = this;
      this.dialogMask = false
      if (arr) {
        self.formData.fundCodes = [];
        self.formData.fundNames = "";
        self.below.fundCodes = [];
        self.below.fundNames = [];
        arr.forEach(function (item, index) {
          index++;
          if (index < arr.length) {
            self.formData.fundNames = self.formData.fundNames + item.VC_FUNDNAME + ",";
          } else {
            self.formData.fundNames = self.formData.fundNames + item.VC_FUNDNAME;
          }
          self.formData.fundCodes.push(item.VC_FUNDCODE);
          self.below.fundCodes.push(item.VC_FUNDCODE);
          self.below.fundNames.push(item.VC_FUNDNAME);

        });
      }
      this.selectList = arr
    },
    //日期时间段快捷选项
    dateShortTPCTA() {
      var self = this
      const pickerOptions = {
        shortcuts: [{
          text: '本周',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
            const start = moment(end).isoWeekday(1).format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '本月',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
            const start = moment([moment(end).year(), 0, 1]).month(moment(end).month()).format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '本季度',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
            const start = moment(moment(end).year() + '-01-01').quarter(moment(end).quarter()).format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '今年以来',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
            const start = moment(end).year() + '-01-01'
            picker.$emit('pick', [start, end])
          }
        },
          {
            text: '成立以来',
            onClick(picker) {
              self.getStandard();
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = self.timDate
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '近一个月',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(1, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          }, {
            text: '近三个月',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(3, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          }, {
            text: '近半年',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(6, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          }, {
            text: '近一年',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(1, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          }, {
            text: '近三年',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(3, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          },]
      }
      return pickerOptions
    },


    getApplyIndexListOptions(){
      commonApi.edimsSelectType('APPLYINDEXENUM').then(res => {
        const { status, data } = res.data
        if (status === 0) {
          this.applyIndexListOptions = data
        } else {
          this.applyIndexListOptions = []
        }
      })
    },

    getPrivateIndexListOptions(){

      selectPrivateIndexList({}).then(res => {
        let { status, data } = res.data
        if (status === 200) {
          this.indexListOptions = data
        }
      })
    },

    generate(){
      const data = {}
      generatePrivateIndexCode(data).then((res) => {
        console.log(res.data.data.indexCode)
        if (res.data.status === 200) {
          this.formData.indexCode = res.data.data.indexCode
        }
      })
    },


    /**
     * @description 取消按钮关闭弹窗
     */
    cancel() {
      this.$emit('closeDialog', 'NO_REFESH')
    },


    /**
     * @description 保存
     */
    handleSave() {
      this.$refs['formData'].validate((valid) => {
        if (valid) {
          const params = Object.assign({}, this.formData)
          console.log("formData"+JSON.stringify(this.formData));
          params.operation = this.isEdit ? 'update' : 'insert'
          params.beginDate = this.formData.ddate_[0]
          params.endDate=this.formData.ddate_[1]
          params.id=this.formData.id
          if (params.operation == 'insert') {
            insertPrivateIndexComponent(params).then((res) => {
              const { message } = res.data
              if (res.data.status === 200) {
                this.$message({
                  type: 'success',
                  message: '保存成功',
                  customClass: 'message-success'
                })
                this.$emit('closeDialog', 'REFESH')
              } else {
                this.$message({
                  type: 'error',
                  message: message || '保存失败',
                  customClass: 'message-error'
                })
              }
            })
          } else if (params.operation == 'update') {
            updatePrivateIndexComponent(params).then((res) => {
              const { message } = res.data
              if (res.data.status === 200) {
                this.$message({
                  type: 'success',
                  message: '保存成功',
                  customClass: 'message-success'
                })
                this.$emit('closeDialog', 'REFESH')
              } else {
                this.$message({
                  type: 'error',
                  message: message || '保存失败',
                  customClass: 'message-error'
                })
              }
            })
          }
        } else {
          return false
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>


</style>

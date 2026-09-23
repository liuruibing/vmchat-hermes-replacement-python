<template>
  <div style="height: 100%">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formInline" :inline="true" :model="formInline" :rules="searchRules" class="standard-form">
          <el-row>
            <el-form-item label="产品" prop="fundName">
<!--              <el-tooltip :content="formInline.fundName" :disabled="!formInline.fundName" class="item" effect="dark" placement="top-start">
                <el-input v-model="formInline.fundName" clearable placeholder="请输入" size="small" @click.native="openFundListDialog" />
              </el-tooltip>-->
              <ProductSelectInput
                v-model="formInline.product"
                placeholder="请选择产品"
                :input-width="'260px'"
                @select="handleProductSelect"
                @clear="handleProductClear"
              />
            </el-form-item>
            <el-form-item class="mb20" label="日期" prop="ddate_">
              <el-date-picker
                v-model="formInline.ddate_"
                :picker-options="dateShortTPCTA()"
                align="left"
                end-placeholder="结束日期"
                popper-class="popperDateShortTP"
                range-separator="-"
                size="small"
                start-placeholder="开始日期"
                type="daterange"
                unlink-panels
                value-format="yyyy-MM-dd"
              ></el-date-picker>
            </el-form-item>
            <el-form-item prop="desensitizationFlag">
              <el-checkbox-group v-model="formInline.desensitizationFlag" @change="handlecheckeddesensitizationChange">
                <el-checkbox label="脱敏" value="true"></el-checkbox>
              </el-checkbox-group>
            </el-form-item>

            <el-form-item v-show="showDesensitization" prop="desensitizationFun">
              <el-select v-model="formInline.desensitizationFun" size="small">
                <el-option label="不显示名称、代码" value="ALL" ></el-option>
                <el-option label="仅屏蔽部分字符" value="PAR"></el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="数据频率" prop="dataFreq">
              <el-select v-model="formInline.dataFreq" size="small" clearable filterable >
                <el-option v-for="item in dataFreqOptionList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />

              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button :icon="exportIcon" style="margin-bottom: 5px" size="small" :disabled="onButton" type="primary" @click="onSubmit('formInline')">{{onSub}}</el-button>
              <el-button type="info" plain icon="el-icon-refresh-left" size="small" @click="resetForm('formInline')">重置</el-button>
              <el-button type="info" plain :icon="exportIcon2" style="margin-bottom: 5px" :disabled="exportButton2" @click="fun_export_PDF" size="small">
                {{ exportText2 }}
              </el-button>
            </el-form-item>
            <el-form-item>
              <!-- <div style="color: red;">拥有此产品：{{ fundGrant }}权限，报告仅显示有权限模块。</div> -->
            </el-form-item>
          </el-row>
          <el-row>
            <el-col :span="24">
              <div style="display: inline-block">
                <el-form-item label="基准类型">
                  <el-select v-model="formInline.ZB_INDEXTYPE" placeholder="请选择" size="small">
                    <el-option v-for="item in ZB_INDEXTYPEOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
                  </el-select>
                </el-form-item>
              </div>
              <div v-show="formInline.ZB_INDEXTYPE == '1'" style="display: inline-block">
                <el-form-item label="选择基准">
                  <el-select v-model="formInline.ZB_INDEXCODEA" placeholder="请选择" size="small">
                    <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
                  </el-select>
                </el-form-item>
              </div>
              <div v-show="formInline.ZB_INDEXTYPE == '2'" style="display: inline-block">
                <el-form-item label="基准 A">
                  <el-select v-model="formInline.ZB_INDEXCODEA" placeholder="请选择" size="small">
                    <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="比例">
                  <el-input v-model="formInline.ZB_INDEXWEIGHTA" size="small" style="width: 85px !important" @blur="handleInputWeight('A')"></el-input>
                  %
                </el-form-item>
              </div>
              <div v-show="formInline.ZB_INDEXTYPE == '2'" style="display: inline-block">
                <el-form-item label="基准 B">
                  <el-select v-model="formInline.ZB_INDEXCODEB" placeholder="请选择" size="small">
                    <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="比例">
                  <el-input v-model="formInline.ZB_INDEXWEIGHTB" size="small" style="width: 85px !important" @blur="handleInputWeight('B')"></el-input>
                  %
                </el-form-item>
              </div>
              <div style="display: inline-block">
              <el-form-item label="对比基准">

                <el-select v-model="formInline.contrasCode" clearable collapse-tags multiple placeholder="请选择"
                           size="small" @change="changeContrasCode">
                  <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
                </el-select>

              </el-form-item>
             </div>

              <div style="display: inline-block">
                <el-form-item label="行业类型">

                  <el-select v-model="formInline.industryType" clearable collapse-tags  placeholder="请选择"
                             size="small">
                    <el-option v-for="item in industryTypeOptions" :key="item.id" :label="item.label" :value="item.id"></el-option>
                  </el-select>

                </el-form-item>
              </div>

              <div style="display: inline-block">
                <el-form-item label="因子类型">

                  <el-select v-model="formInline.factorType" clearable collapse-tags  placeholder="请选择"
                             size="small">
                    <el-option v-for="item in factorTypeOptions" :key="item.id" :label="item.label" :value="item.id"></el-option>
                  </el-select>

                </el-form-item>
              </div>
            </el-col>
          </el-row>

        </el-form>
      </div>
    </div>

    <product-selector
      v-if="dialogMask"
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
import iframeModule from '@/components/iframe'
import fun from '@/filters/common'
import productSelector from '@/components/productSelector'
import FundListDialog from '@/components/FundListDialog/ZjzqDialog'
import { getToken } from '@/utils/auth'
import request from '@/utils/request'
import moment from 'moment'
import commonApi from '@/api/common.js'
import ProductSelectInput from '@/components/productSelector/ProductSelectInput'
import store from "../../../store";
export default {
  name: '',
  components: {
    FundListDialog,
    iframeModule,
    productSelector,
    ProductSelectInput
  },
  props: {
    templateCode: {
      type: String,
      default: ''
    },
    reportType: {
      type: String,
      default: ''
    },
    templateName: {
      type: String,
      default: ''
    }
  },
  data() {

    const validateRangeDate = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请选择日期范围'))
      } else {
        if (this.formInline.ddate_ !== null || this.formInline.ddate_ !== undefined || this.formInline.ddate_ !== '') {
          const startTime = new Date(this.formInline.ddate_[0])
          const endTime = new Date(this.formInline.ddate_[1])
          const fundCreateTime=new Date(this.timDate)
          const fundEndTime=new Date(this.dateTime)
          if(endTime >fundEndTime){
            callback(new Error('结束日期不能大于产品最新的估值确认日期'))
          }else if(startTime < fundCreateTime) {
            callback(new Error('开始日期不能早于产品的成立日期'))
          }else if (startTime > endTime) {
            callback(new Error('开始日期不能大于结束日期'))
          } else {
            callback()
          }
        } else {
          callback()
        }
      }
    }
    const validateDate = (rule, value, callback) => {
      if (value === null || value.length === 0) {
        callback(new Error('请选择日期'))
      } else if (!this.$validate.validateThreeYears(value)) {
        callback(new Error('选择日期区间大于三年'))
      } else {
        callback()
      }
    }
    const validatebeginDate = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请选择开始日期'))
      } else {
        if (this.formInline.endDate !== null || this.formInline.endDate !== undefined || this.formInline.endDate !== '') {
          const startTime = new Date(value)
          const endTime = new Date(this.formInline.endDate)
          if (startTime > endTime) {
            callback(new Error('开始日期不能大于结束日期'))
          } else {
            callback()
          }
        } else {
          callback()
        }
      }
    }
    const validateEndDate = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请选择结束日期'))
      } else {
        if (this.formInline.beginDate !== null || this.formInline.beginDate !== undefined || this.formInline.beginDate !== '') {
          const startTime = new Date(this.formInline.beginDate)
          const endTime = new Date(value)
          if (startTime > endTime) {
            callback(new Error('结束日期不能小于开始日期'))
          } else {
            callback()
          }
        } else {
          callback()
        }
      }
    }
    return {
      // 选择产品弹窗
      productSelectorVisible: false,

      selectList: [],
      zhezhao: false,
      dialogMask: false,
      pickerOptions: {},
      productCheckArr: [],
      companyCheckArr: [],
      fundArray: [],
      treeData: [
        {
          label: '产品列表',
          id: 'zstgwb'
        },
        {
          label: '管理人旗下产品',
          id: 'glrqxcp'
        },
        {
          label: '私有产品',
          id: 'sycp'
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
      showTreeKeyArray: ['产品列表', '私有产品', '我的关注'],
      // 搜索
      formInline: {
        product: null,
        // date: [],
        ddate_: [],
        beginDate: '',
        endDate: '',
        fundCode: '',
        fundName: '',
        ZB_INDEXCODE: '', // 基准编码
        ZB_INDEXTYPE: '1', // 基准类型
        ZB_INDEXCODEA: '000300', // 基准A
        ZB_INDEXWEIGHTA: '0.0000', // 基准A权重
        ZB_INDEXCODEB: '000300', // 基准B
        ZB_INDEXWEIGHTB: '0.0000', // 基准B权重
        desensitizationFlag:'', //脱敏标志
        desensitizationFun:'ALL',//脱敏方法 ALL 不显示名称和代码  PAR 仅屏蔽部分字符
        dataFreqOpen:'true',//数据频率过滤是否开启
        dataFreq:'1',//数据频率  1 日频 2 周频  3 月频
        contrasCode:[],//对比基准
        contrasCodes:'',//对比基准,逗号分割
        industryType:'SWSR',//默认申万行业
        factorType:'CNE5'//默认因子类型
      },
      dataFreqOptionList: [],
      ZB_INDEXTYPEOption: [
        {
          id: '0',
          label: '无基准'
        },
        {
          id: '1',
          label: '单基准'
        },
        {
          id: '2',
          label: '复合基准'
        }
      ],
      industryTypeOptions:[
      {
        id: 'SWSR',
        label: '申万行业'
      },
      {
        id: 'ZXSR',
        label: '中信行业'
      }],
      factorTypeOptions:[{
        id: 'CNE5',
        label: 'CNE5'
      },
        {
          id: 'CNE6',
          label: 'CNE6'
        }],
      datumOption: [],
      searchRules: {
        fundName: [{ required: true, message: '请选择产品', trigger: 'change' }],
        ddate_: [
          {required: true, message: "请选择日期", trigger: "change"},
          {validator: validateRangeDate, trigger: 'blur' }
        ],
      },
      issearchFxButton: false,
      fundCode: '', // code值
      fundName: '', // name
      noData: '--', // 没有数据
      iframeData: {
        // iframe链接
        src: ''
      },
      //成立日
      timDate: '',
      //开关
      offOn: false,
      name: 'iframeVue_reportZJZJFX',
      id: 'J_iframe_id_reportZJZJFX',
      baseApi: '', // 页面根地址
      exportButton: false,
      exportText: '导出',
      exportButton2: false, // 导出 word
      exportIcon2: 'el-icon-download',
      /*exportText2: '导出Word',*/
      exportText2: '导出',
      benchmarkA: '',
      fundGrant: '--',
      dateTime:'',
      onButton:false,
      onSub:'查询',
      exportIcon:'el-icon-search',
      showDesensitization:false,
    }
  },
  mounted() {
    var self = this
    var baseTime = store.state.edims.baseTime
    if(baseTime){
      self.formInline.ddate_ = [baseTime.beginDate, baseTime.endDate]
      self.formInline.beginDate = baseTime.beginDate
      self.formInline.endDate = baseTime.endDate
    }
    // self.getContrasOptions()
    // self.getDate()
    self.baseApi = process.env.BASE_API
    window.addEventListener('message', (msg) => {
      if (msg.data && msg.data.action == 'INFO_VM') {
        if (msg.data.payload.type == 'stop') {
          self.onButton = false
          self.onSub = '查询'
          self.exportButton2 = false
          self.exportIcon = 'el-icon-search'
        }
      }
    })
    this.getDataFreqOptions("DATAFREQ")
  },
  watch: {
    'formInline.desensitizationFlag'(newVal,oldVal){
      var self = this
      //  console.log(self.formInline);
      self.formInline.desensitizationFlag = newVal;
      // console.log('Checkbox 值改变:', oldVal, '->', newVal);
    }
  },
  methods: {
    getTimeBig(){
      if(this.formInline.fundCode =='' || this.formInline.fundCode == null){
        if(this.formInline.beginDate!=''){
          this.$message({
            message: '请选择产品代码',
            type: 'warning'
          })
        }
        this.formInline.beginDate =''
      }else {
        if (this.formInline.beginDate !='' && this.formInline.beginDate < this.timDate) {
          setTimeout(() => {
            this.formInline.beginDate = this.timDate;
          }, 500);
        }
      }
    },
    getTimeEnd(){
      if(this.formInline.fundCode =='' || this.formInline.fundCode == null){
        if(this.formInline.endDate!=''){
          this.$message({
            message: '请选择产品代码',
            type: 'warning'
          })
        }
        this.formInline.endDate =''
      }else{
        if((this.formInline.endDate != this.dateTime) && (this.formInline.endDate != '' || this.formInline.endDate != null)){
          this.getTimes(this.formInline.fundCode,this.formInline.endDate)
        }
      }
    },
    getTimes(code,end) {
      return new Promise((resolve, reject) => {
        const params = {
          indexCode: 'dacc5f54-8ff8-418b-984a-52a18409d716',
          fundCode:code,
          endDate: end
        }
        request({
          url: `/api/report/v1.0/data/sql/dacc5f54-8ff8-418b-984a-52a18409d716`,
          method: 'post',
          data: params
        })
          .then((res) => {
            if (res.data.status === 0) {
              this.dateTime = res.data.data[0].endTime
              if(this.dateTime != null && this.formInline.endDate > this.dateTime){
                this.formInline.endDate = this.dateTime
              }
            }
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
    },
    /**
     * @description 获取默认时间
     */
    getDate() {
      return new Promise((resolve, reject) => {
        request({
          url: `/api/report/v1.0/data/sql/3ca0695e-a77a-4aeb-b82c-9b40360ba892`,
          method: 'post',
          data: {
            indexCode: '3ca0695e-a77a-4aeb-b82c-9b40360ba892'
          }
        })
          .then((res) => {
            if (res.data.status === 0) {
              let beg = res.data.data[0].NEXTDATE
              let end = res.data.data[0].PREVDATE
              this.formInline.beginDate = beg
              this.formInline.endDate = end
              //this.formInline.ddate_ = [beg,end]
            }
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
    },

    /**
     * @description 监听对比基准下拉
     */
    changeContrasCode(val) {
      if (val.length > 3) {
        this.$message({
          type: 'warning',
          message: '对比基准最多只能选三个'
        })
        this.formInline.contrasCode.splice(-1)

      }
    },
    /**
     * @description 获取基准下拉
     */
    getContrasOptions() {
      return new Promise((resolve, reject) => {
        request({
          url: `/api/report/v1.0/data/sql/d43c924b-eebd-4d8f-97e5-ed46b609456d`,
          method: 'post',
          data: {
            indexCode: 'd43c924b-eebd-4d8f-97e5-ed46b609456d'
          }
        })
          .then((res) => {
            if (res.data.status === 0) {
              const resultDim = res.data.data || []
              this.datumOption = resultDim.map((item) => {
                return {
                  label: item.DIM_NME,
                  id: item.DIM_CDE
                }
              })
            }
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
    },

    //日期时间段快捷选项  从成立日到 估值确认日期
    dateShortTPCTA() {
      var self = this
      if(self.dateTime!==null && self.dateTime!==""
        && self.timDate!==null && self.timDate!==""){
        const pickerOptions = {
          shortcuts: [{
            text: '本周',
            onClick(picker) {
              const end = moment(self.dateTime).format('YYYY-MM-DD')
              const start = moment(end).isoWeekday(1).format('YYYY-MM-DD')
              const create = self.timDate
              const createTime=moment(self.timDate).format('YYYY-MM-DD')
              //判断开始日期是否再成立日期之前
              picker.$emit('pick', [moment(start).isAfter(create)===true?start:createTime, end])
            }
          }, {
            text: '本月',
            onClick(picker) {
              const end = moment(self.dateTime).format('YYYY-MM-DD')
              const start = moment([moment(end).year(), 0, 1]).month(moment(end).month()).format('YYYY-MM-DD')
              const create = self.timDate
              const createTime=moment(self.timDate).format('YYYY-MM-DD')
              //判断开始日期是否再成立日期之前
              picker.$emit('pick', [moment(start).isAfter(create)===true?start:createTime, end])
            }
          }, {
            text: '本季度',
            onClick(picker) {
              const end = moment(self.dateTime).format('YYYY-MM-DD')
              const start = moment(moment(end).year() + '-01-01').quarter(moment(end).quarter()).format('YYYY-MM-DD')
              const create = self.timDate
              const createTime=moment(self.timDate).format('YYYY-MM-DD')
              //判断开始日期是否再成立日期之前
              picker.$emit('pick', [moment(start).isAfter(create)===true?start:createTime, end])
            }
          }, {
            text: '今年以来',
            onClick(picker) {
              const end = moment(self.dateTime).format('YYYY-MM-DD')
              const start = moment(end).year() + '-01-01'
              const create = self.timDate
              const createTime=moment(self.timDate).format('YYYY-MM-DD')
              //判断开始日期是否再成立日期之前
              picker.$emit('pick', [moment(start).isAfter(create)===true?start:createTime, end])
            }
          },
            {
              text: '成立以来',
              onClick(picker) {
                self.getStandard();
                const end = moment(self.dateTime).format('YYYY-MM-DD')
                const start = self.timDate
                picker.$emit('pick', [start, end])

              }
            },
            {
              text: '近一个月',
              onClick(picker) {
                const end = moment(self.dateTime).format('YYYY-MM-DD')
                const start = moment(moment(end).subtract(1, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
                const create = self.timDate
                const createTime=moment(self.timDate).format('YYYY-MM-DD')
                //判断开始日期是否再成立日期之前
                picker.$emit('pick', [moment(start).isAfter(create)===true?start:createTime, end])
              }
            }, {
              text: '近三个月',
              onClick(picker) {
                const end = moment(self.dateTime).format('YYYY-MM-DD')
                const start = moment(moment(end).subtract(3, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
                const create = self.timDate
                const createTime=moment(self.timDate).format('YYYY-MM-DD')
                //判断开始日期是否再成立日期之前
                picker.$emit('pick', [moment(start).isAfter(create)===true?start:createTime, end])
              }
            }, {
              text: '近半年',
              onClick(picker) {
                const end = moment(self.dateTime).format('YYYY-MM-DD')
                const start = moment(moment(end).subtract(6, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
                const create = self.timDate
                const createTime=moment(self.timDate).format('YYYY-MM-DD')
                //判断开始日期是否再成立日期之前
                picker.$emit('pick', [moment(start).isAfter(create)===true?start:createTime, end])
              }
            }, {
              text: '近一年',
              onClick(picker) {
                const end = moment(self.dateTime).format('YYYY-MM-DD')
                const start = moment(moment(end).subtract(1, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
                const create = self.timDate
                const createTime=moment(self.timDate).format('YYYY-MM-DD')
                //判断开始日期是否再成立日期之前
                picker.$emit('pick', [moment(start).isAfter(create)===true?start:createTime, end])
              }
            }, {
              text: '近三年',
              onClick(picker) {
                const end = moment(self.dateTime).format('YYYY-MM-DD')
                const start = moment(moment(end).subtract(3, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
                const create = self.timDate
                const createTime=moment(self.timDate).format('YYYY-MM-DD')
                //判断开始日期是否再成立日期之前
                picker.$emit('pick', [moment(start).isAfter(create)===true?start:createTime, end])
              }
            },],

          disabledDate(time) {
            // 设置产品的日期范围，成立日到最新的估值确认日期
            return time < new Date(self.timDate) || time > new Date(self.dateTime);
          },
        }
        return pickerOptions
      }else {
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
            },],


        }
        return pickerOptions
      }

    },
    async getStandard() {
      if (this.fundCode == '' || this.formInline.fundName == '') {
        this.offOn = false
        this.timDate = ''
        this.$message({
          message: '请先选择产品！',
          type: 'warning',
          customClass: 'message-warning'
        })
        return
      } else if (this.timDate == '' || this.timDate == undefined || this.timDate == null) {
        this.offOn = false
        this.timDate = ''
        this.$message({
          message: '未获取到成立日！',
          type: 'warning',
          customClass: 'message-warning'
        })
        return
      } else {
        this.offOn = true
      }
    },
    // 权重校验
    handleInputWeight(type) {
      const regex = /^(0(\.\d+)?|[1-9]\d*(\.\d+)?)$/
      if (type == 'A') {
        if (!regex.test(this.formInline.ZB_INDEXWEIGHTA)) {
          this.$message.closeAll()
          this.$message({
            type: 'warning',
            message: '只能输入大于等于0的数',
            customClass: 'message-warning'
          })
          this.formInline.ZB_INDEXWEIGHTA = '0.0000'
          return
        }
        if (this.formInline.ZB_INDEXWEIGHTB != '') {
          if (Number(this.formInline.ZB_INDEXWEIGHTA) + Number(this.formInline.ZB_INDEXWEIGHTB) > 100) {
            this.$message.closeAll()
            this.$message({
              type: 'warning',
              message: '基金A、B权重不能超过100%',
              customClass: 'message-warning'
            })
            this.formInline.ZB_INDEXWEIGHTA = '0'
          } else {
            this.formInline.ZB_INDEXWEIGHTA = '' + Number(this.formInline.ZB_INDEXWEIGHTA).toFixed(4)
          }
        }
      } else {
        if (!regex.test(this.formInline.ZB_INDEXWEIGHTB)) {
          this.$message.closeAll()
          this.$message({
            type: 'warning',
            message: '只能输入大于等于0的数',
            customClass: 'message-warning'
          })
          this.formInline.ZB_INDEXWEIGHTB = '0.0000'
          return
        }
        if (this.formInline.ZB_INDEXWEIGHTA != '') {
          if (Number(this.formInline.ZB_INDEXWEIGHTA) + Number(this.formInline.ZB_INDEXWEIGHTB) > 100) {
            this.$message.closeAll()
            this.$message({
              type: 'warning',
              message: '基金A、B权重不能超过100%',
              customClass: 'message-warning'
            })
            this.formInline.ZB_INDEXWEIGHTB = '0'
          } else {
            this.formInline.ZB_INDEXWEIGHTB = '' + Number(this.formInline.ZB_INDEXWEIGHTB).toFixed(4)
          }
        }
      }
    },
    // 获取选中数据
    getTemplateRow(data) {
      this.fundCode = data.data.fundCode
      this.formInline.fundCode = data.data.fundCode
      this.formInline.fundName = data.data.fundName
      this.timDate = data.data.createDate
      this.dialogMask = false
    },

    initTimGzLastDate(fundCode){
      return new Promise((resolve, reject) => {
        const params = {
          indexCode: 'dacc5f54-8ff8-418b-984a-52a18409d716',
          fundCode:fundCode,
        }
        request({
          url: `/api/report/v1.0/data/sql/dacc5f54-8ff8-418b-984a-52a18409d716`,
          method: 'post',
          data: params
        })
          .then((res) => {
            if (res.data.status === 0) {
              this.dateTime = res.data.data[0].endTime
            }
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
    },
    //初始化数据频率的权限
    initDataFreq(fundCode){
      return new Promise((resolve, reject) => {
        const params = {
          fundCode:fundCode,
        }
        request({
          url: `/api/jxbg/getUserReportDataFreqList`,
          method: 'post',
          data: params
        })
          .then((res) => {
            if (res.data.status === 0) {
              if(res.data.data.length===1){
                const tempDataFreq=res.data.data[0].dimCde
                this.formInline.dataFreq = tempDataFreq
                this.dataFreqOptionList=this.dataFreqOptionList.filter(opt => opt.dimCde === tempDataFreq)
              }



            }
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
    },
    openFundListDialog() {
      /*this.productSelectorVisible = true*/
      this.dialogMask = true
    },
    handleDialogClosed() {
      this.dialogMask = false
    },
    getDataFreqOptions(type){
      // 字典类型
      let params = type
      commonApi.edimsSelectType(params).then(res => {
        let { status, data } = res.data
        if (status === 0) {
          this.dataFreqOptionList = data
        }
      })
    },
    handlecheckeddesensitizationChange(value) {
      this.showDesensitization = value
    },

    handleSubmitClick(arr) {
      this.dialogMask = false
      this.fundCode = arr[0].VC_FUNDCODE || ''
      this.formInline.fundCode = arr[0].VC_FUNDCODE || ''
      this.formInline.fundName = arr[0].VC_FUNDNAME || ''
      this.timDate = arr[0].D_CREATE_DATE || ''
      this.selectList = arr
      this.fundGrant = arr[0].VC_FUND_GRANT || '--'
      //估值最新确认日期
      this.initTimGzLastDate(arr[0].VC_FUNDCODE || '')
      //产品的数据频率加载 非管理员只读，管理员可以下拉
      this.initDataFreq(arr[0].VC_FUNDCODE || '')
    },
    handleProductSelect: function(product) {
      this.fundCode = product.VC_FUNDCODE || ''
      this.formInline.fundCode = product.VC_FUNDCODE || ''
      this.formInline.fundName = product.VC_FUNDNAME || ''
      this.timDate = product.D_CREATE_DATE || ''
      this.fundGrant = product.VC_FUND_GRANT || '--'
      //估值最新确认日期
      this.initTimGzLastDate(product.VC_FUNDCODE || '')
      //产品的数据频率加载 非管理员只读，管理员可以下拉
      this.initDataFreq(product.VC_FUNDCODE || '')
    },
    handleProductClear: function() {
      this.fundCode = ''
      this.formInline.fundCode = ''
      this.formInline.fundName =  ''
      this.fundGrant = ''
      this.timDate = ''
    },
    fromLink() {
      var self = this
      if (this.$route.params && this.$route.params.date) {
        this.formInline.date = []
        this.formInline.date.push(this.$route.params.date[0])
        this.formInline.date.push(this.$route.params.date[1])
        this.fundCode = this.$route.params.fundCode
        this.fundName = this.$route.params.fundName

        try {
          // this.ProductAndPropertyData.fundCode =
          //   this.$route.params.fundCode;
          this.ProductAndPropertyData.performanceDefaultFundCode = this.fundCode
          this.$refs.bondAnalysis.myactiavted()
        } catch (e) {}
        // this.onQuery();
        // self.getFundBenchmark(this.fundCode);
        self.fun_iframeSrc()
      }
    },
    file_vmrisk_src_view(templateCode, beginDate, endDate, fundCode,benchmarks,benchmarkA, benchmarkB, benchmarkAValue, benchmarkBValue, kpiCode, contrasCode,industryType,factorType,desensitizationFlag,desensitizationFun,dataFreqOpen,dataFreq) {
      return (
        process.env.BASE_API +
        '/rest/report/interview.do?templateCode=' +
        templateCode +
        '&beginDate=' +
        beginDate +
        '&endDate=' +
        endDate +
        '&fundCode=' +
        fundCode +
        '&benchmarks=' +
        benchmarks +
        '&benchmarkA=' +
        benchmarkA +
        '&benchmarkB=' +
        benchmarkB +
        '&benchmarkAValue=' +
        benchmarkAValue +
        '&benchmarkBValue=' +
        benchmarkBValue +
        '&kpiCode=' +
        kpiCode +
        '&contrasCode=' +
        contrasCode +
        '&industryType=' +
        industryType +
        '&factorType=' +
        factorType +
        '&desensitizationFlag=' +
        desensitizationFlag+
        '&desensitizationFun=' +
        desensitizationFun+
        '&dataFreqOpen=' +
        dataFreqOpen+
        '&dataFreq=' +
        dataFreq+
        '&token=' +
        encodeURIComponent(getToken()) +
        '&autoRun=false&ajaxRun=true&showParam=true&showCondition=false&markFlag=false&srcSuffix=' +
        process.env.BASE_API +
        '&time=' +
        new Date().getTime()
      )
    },

    file_vmrisk_src_preview(templateCode, beginDate, endDate, fundCode, benchmarks,benchmarkA, benchmarkB, benchmarkAValue, benchmarkBValue, kpiCode, contrasCode,industryType,factorType,desensitizationFlag,desensitizationFun,dataFreqOpen,dataFreq) {
      return (
        process.env.BASE_API +
        '/rest/report/preview.do?templateCode=' +
        templateCode +
        '&beginDate=' +
        beginDate +
        '&endDate=' +
        endDate +
        '&fundCode=' +
        fundCode +
        '&benchmarks=' +
        benchmarks +
        '&benchmarkA=' +
        benchmarkA +
        '&benchmarkB=' +
        benchmarkB +
        '&benchmarkAValue=' +
        benchmarkAValue +
        '&benchmarkBValue=' +
        benchmarkBValue +
        '&kpiCode=' +
        kpiCode +
        '&contrasCode=' +
        contrasCode +
        '&industryType=' +
        industryType +
        '&factorType=' +
        factorType +
        '&desensitizationFlag=' +
        desensitizationFlag+
        '&desensitizationFun=' +
        desensitizationFun+
        '&dataFreqOpen=' +
        dataFreqOpen+
        '&dataFreq=' +
        dataFreq+
        '&token=' +
        encodeURIComponent(getToken()) +
        '&autoRun=false&ajaxRun=true&showParam=true&showCondition=false&markFlag=false&srcSuffix=' +
        process.env.BASE_API +
        '&time=' +
        new Date().getTime()
      )
    },

    onSubmit(formName) {
      var self = this
      self.$refs[formName].validate((valid) => {
        if (valid) {
          try {
            self.fun_iframeSrc()
          } catch (e) {}
          // 禁用搜索按钮
          // self.$fun.searchButtonDisabled('issearchFxButton', self)
        } else {
          return false
        }
      })
    },
    // 清除
    resetForm(formName) {
      var self = this
      self.$refs[formName].resetFields()
      this.fundCode = ''
      this.fundName = ''
    },
    // iframe链接地址
    fun_iframeSrc() {
      /*   if (this.formInline.ddate_ && this.formInline.ddate_.length) {
           this.formInline.beginDate = this.formInline.ddate_[0];
           this.formInline.endDate = this.formInline.ddate_[1];
         }*/
      var self = this
      self.onButton = true
      self.onSub = '查询中...'
      self.exportButton2 = true
      self.exportIcon = 'el-icon-loading'
      self.formInline.contrasCodes=self.formInline.contrasCode.join(",")
      //无基准
      if (self.formInline.ZB_INDEXTYPE == '0') {
        self.formInline.ZB_INDEXCODEA=''
        self.formInline.ZB_INDEXCODEB = ''
        self.formInline.ZB_INDEXWEIGHTA = ''
        self.formInline.ZB_INDEXWEIGHTB = ''
      }
      //单基准
      if (self.formInline.ZB_INDEXTYPE == '1') {
        self.formInline.ZB_INDEXCODEB = ''
        self.formInline.ZB_INDEXWEIGHTA = ''
        self.formInline.ZB_INDEXWEIGHTB = ''
      }
      try {
        if (this.reportType == 'preview') {
          self.iframeData.src = this.file_vmrisk_src_preview(
            // "2ae0c3f9-f8ee-4cab-b7c0-65b0f654548e",
            this.templateCode,
            self.formInline.ddate_[0],
            self.formInline.ddate_[1],
            self.formInline.fundCode,
            self.formInline.ZB_INDEXTYPE,
            self.formInline.ZB_INDEXCODEA,
            self.formInline.ZB_INDEXCODEB,
            self.formInline.ZB_INDEXWEIGHTA,
            self.formInline.ZB_INDEXWEIGHTB,
            '',
            self.formInline.contrasCodes,
            self.formInline.industryType,
            self.formInline.factorType,
            '',
            self.formInline.desensitizationFlag,
            self.formInline.desensitizationFun,
            self.formInline.dataFreqOpen,
            self.formInline.dataFreq

          )
        } else {
          // console.log(self.formInline.desensitizationFlag);
          // console.log(self.formInline.desensitizationFun);
          self.iframeData.src = this.file_vmrisk_src_view(
            // "2ae0c3f9-f8ee-4cab-b7c0-65b0f654548e",
            this.templateCode,
            self.formInline.ddate_[0],
            self.formInline.ddate_[1],
            self.formInline.fundCode,
            self.formInline.ZB_INDEXTYPE,
            self.formInline.ZB_INDEXCODEA,
            self.formInline.ZB_INDEXCODEB,
            self.formInline.ZB_INDEXWEIGHTA,
            self.formInline.ZB_INDEXWEIGHTB,
            '',
            self.formInline.contrasCodes,
            self.formInline.industryType,
            self.formInline.factorType,
            self.formInline.desensitizationFlag,
            self.formInline.desensitizationFun,
            self.formInline.dataFreqOpen,
            self.formInline.dataFreq

          )
        }
        this.$emit('iframeSrc', this.iframeData.src)
      } catch (e) {
        console.log(e)
      }
    },
    // 导出
    fun_export_PDF() {
      var self = this
      // 禁用按钮
      self.exportButton2 = true;
      self.exportIcon2 = 'el-icon-loading';
      self.exportText2 = '导出数据中...';

      // 使用该tab上次查询的参数
      //const params = tab.queryParams;
      const pdfName = '报告.pdf'
      //封面-信创
      const covIndexCode = '8cf9997c-e5c4-40e9-8d79-660e61d323ce';
      const pdfOption = { pagedir: 'h' }; // vm导出word说明文档中相反，h为纵向，v为横向，默认为横向
      const const_iframeid="J_iframe_id_"+this.templateCode
      //信创版本导出
      fun.fun_exportPDFOption_GFJX_new(
        pdfName,
        JSON.stringify(pdfOption),
        const_iframeid,
        this.templateCode,
        self.formInline.fundCode,
        self.formInline.fundName,
        self.formInline.ddate_[0],
        self.formInline.ddate_[1],
        self.formInline.desensitizationFlag,
        self.formInline.desensitizationFun,
        self.formInline.dataFreqOpen,
        self.formInline.dataFreq,
        self.formInline.ZB_INDEXTYPE,
        self.formInline.ZB_INDEXCODEA,
        self.formInline.ZB_INDEXCODEB,
        self.formInline.ZB_INDEXWEIGHTA,
        self.formInline.ZB_INDEXWEIGHTB,

        covIndexCode,
        // 成功回调：恢复按钮
        (res) => {
          self.exportButton2 = false;
          self.exportIcon2 = 'el-icon-download';
          self.exportText2 = '导出';
          self.$message.success(res.message);
        },
        // 失败回调：恢复按钮
        (res) => {
          self.exportButton2 = false;
          self.exportIcon2 = 'el-icon-download';
          self.exportText2 = '导出';
          self.$message.error(res.message);
        }
      );
      //this.$emit('export_PDF')
    },
    // 导出vm
    fun_export() {
      var self = this

      if (self.formInline.fundCode == '') {
        self.$message({
          message: '请选择产品代码',
          type: 'warning'
        })
      } else {
        self.exportButton = true
        self.exportIcon = 'el-icon-loading'
        self.exportText = '导出数据中...'

        fun.file_vmrisk_download(
          // 报告模板ID  新建报告VUE界面需要更换相应的模板ID
          '28c29080-fe73-4c60-87b8-2b0564d78d5e',
          self.formInline.beginDate,
          self.formInline.endDate,
          self.formInline.fundCode,
          '',
          '',
          '',
          '',
          'DWJZ',
          '104'
        )

        setTimeout(function () {
          self.exportButton = false
          self.exportIcon = 'el-icon-download'
          self.exportText = '导出'
        }, 5000)
      }
    },

    // 导出word11
    fun_exportword() {
      this.exportButton2 = true
      this.exportIcon2 = 'el-icon-loading'
      this.exportText2 = '导出数据中...'

      const wordName = '报告.docx'
      // fun.fun_exportwordrisk(wordName);
      const wordOption = { pagedir: 'h' } // vm导出word说明文档中相反，h为纵向，v为横向，默认为横向
      fun.fun_exportwordriskOption(wordName, JSON.stringify(wordOption), this.id)
      setTimeout(() => {
        this.exportButton2 = false
        this.exportIcon2 = 'el-icon-download'
        this.exportText2 = '导出Word'
      }, 10000)
    },
    fun_getDate() {
      var date = new Date()
      date.setDate(1)
      var month = parseInt(date.getMonth() + 1)
      var day = date.getDate()
      if (month < 10) {
        month = '0' + month
      }
      if (day < 10) {
        day = '0' + day
      }
      var statrDate = date.getFullYear() + '-' + month + '-' + day
      var date2 = new Date()
      var day2 = date2.getDate()
      if (day2 < 10) {
        day2 = '0' + day2
      }
      var endDate = date.getFullYear() + '-' + month + '-' + day2
      var dates = [statrDate, endDate]
      return dates
    }
  }
}
</script>

<style lang="scss">
.el-dialog {
  width: 60% !important;
}
</style>
<style lang="scss" scoped>
.el-dialog {
  width: 60% !important;
}

.customWidth {
  width: 80% !important;
}

input::-webkit-input-placeholder {
  color: #999 !important;
}
</style>

<style lang="scss" scoped>

.iframeModule_out {
  width: 100%;
  height: 100vh;
  position: relative;

  .zhezhao {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
  }
}

::v-deep .el-button.el-button--info {
  color: #333;
  background-color: #dddddd;
  border-color: #dddddd;
}
</style>

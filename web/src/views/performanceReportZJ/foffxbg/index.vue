<template>
  <div style="height: 100%" class="PerformanceReportStyle">
    <el-container style="height: 100%">
      <!--板块组合分析-->
      <el-main style="height: 100%; overflow-x: hidden; overflow-y: hidden">
        <div class="standard-form-margin analyse-page">
          <div class="inner-margin">
            <el-form ref="formInline" :inline="true" :model="formInline" :rules="searchRules" class="demo-form-inline form_inline_search standard-form" style="margin-top: 10px">
              <el-row>
                <el-col :span="24">
                  <div class="grid-content bg-purple ">
                    <el-form-item label="" prop="fundName">
                      <el-tooltip :content="formInline.fundName" :disabled="!formInline.fundName" effect="dark" placement="top-start">
                        <el-input v-model="formInline.fundName" clearable placeholder="请选择产品" size="small" @click.native="openFundListDialog" />
                      </el-tooltip>
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

                    <el-form-item label="数据频率" prop="dataFreq">
                      <el-select v-model="formInline.dataFreq" size="small" clearable filterable >
                        <el-option v-for="item in userDataFreqOptionList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />

                      </el-select>
                    </el-form-item>

                    <el-form-item class="">
                      <el-button :icon="exportIcon" style="margin-bottom: 5px" size="small" :disabled="onButton" type="primary" @click="onSubmit('formInline')">{{onSub}}</el-button>
                      <el-button type="info" plain icon="el-icon-refresh-left" size="small" @click="resetForm('formInline')">重置</el-button>
                      <el-button type="info" plain :icon="exportIcon2" style="margin-bottom: 5px" :disabled="exportButton2" @click="fun_export_PDF" size="small">
                        {{ exportText2 }}
                      </el-button>
                      <el-button type="primary" size="small" @click="showMoreQuery">
                        <span>{{ isShowMoreQuery ? '收起筛选' : '展开筛选' }}</span>
                        <i :class="isShowMoreQuery ? 'el-icon-caret-top' : 'el-icon-caret-bottom'" />
                      </el-button>
                    </el-form-item>
                  </div>
                </el-col>
              </el-row>
              <el-row v-show="isShowMoreQuery">
                <el-col :span="24">
                  <div style="display: inline-block">
                    <el-form-item label="基准类型">
                      <!--<span style="width: 60px;display: inline-block;">基准类型</span>-->
                      <el-select v-model="formInline.ZB_INDEXTYPE" placeholder="请选择" size="small">
                        <el-option v-for="item in ZB_INDEXTYPEOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
                      </el-select>
                    </el-form-item>
                  </div>
                  <div v-show="formInline.ZB_INDEXTYPE == 'djz'" style="display: inline-block">
                    <!-- <span style="width: 60px;display: inline-block; margin-left: 20px;">选择基准</span>-->
                    <el-form-item label="选择基准">
                      <el-select v-model="formInline.ZB_INDEXCODEA" placeholder="请选择" size="small">
                        <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
                      </el-select>
                    </el-form-item>
                  </div>
                  <div v-show="formInline.ZB_INDEXTYPE == 'fhjz'" style="display: inline-block">
                    <!--<span style="width: 40px;display: inline-block;margin-left: 20px;">基准 A</span>-->
                    <el-form-item label="基准 A">
                      <el-select v-model="formInline.ZB_INDEXCODEA" placeholder="请选择" size="small">
                        <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
                      </el-select>
                    </el-form-item>
                    <!--<span style="width: 40px;display: inline-block;margin-left: 10px;">比例 A</span>-->
                    <el-form-item label="比例">
                      <el-input v-model="formInline.ZB_INDEXWEIGHTA" size="small" style="width: 85px !important" @blur="handleInputWeight('A')"></el-input>
                      %
                    </el-form-item>
                  </div>
                  <div v-show="formInline.ZB_INDEXTYPE == 'fhjz'" style="display: inline-block">
                    <!-- <span style="width: 40px;display: inline-block;margin-left: 20px;">基准 B</span>-->
                    <el-form-item label="基准 B">
                      <el-select v-model="formInline.ZB_INDEXCODEB" placeholder="请选择" size="small">
                        <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
                      </el-select>
                    </el-form-item>
                    <!--<span style="width: 40px;display: inline-block;margin-left: 10px">比例 B</span>-->
                    <el-form-item label="比例">
                      <el-input v-model="formInline.ZB_INDEXWEIGHTB" size="small" style="width: 85px !important" @blur="handleInputWeight('B')"></el-input>
                      %
                    </el-form-item>
                  </div>
                </el-col>
              </el-row>
            </el-form>
          </div>
        </div>
        <div class="iframeModule_out">
          <iframeModule :id="id" :iframe-data="iframeData" :name="name" />
          <div v-if="zhezhao" class="zhezhao" @click="zhezhao = false"></div>
        </div>
      </el-main>
    </el-container>

    <!--    <el-dialog :visible.sync="dialogMask" :close-on-click-modal="false" title="产品信息" center custom-class="customWidth">
      <el-container class="hg100">
        <el-main class="mainBox">
          <FundListDialog @getTemplateRow="getTemplateRow"/>
        </el-main>
      </el-container>
    </el-dialog>-->
    <product-selector
      v-if="dialogMask"
      :leftList="left"
      :dialog-visible="dialogMask"
      :tree-data="treeData"
      :show-tree-key-array="showTreeKeyArray"
      :select-list="selectList"
      default-checked-keys="zstgwb"
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
import store from "../../../store";
export default {
  name: 'ReportZJFOF',
  components: {
    FundListDialog,
    iframeModule,
    productSelector
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
      isShowMoreQuery: false,
      // 选择产品弹窗
      productSelectorVisible: false,
      left:false,
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
      // 搜索
      formInline: {
        // date: [],
        ddate_: [],
        beginDate: '',
        endDate: '',
        fundCode: '',
        fundName: '',
        ZB_INDEXCODE: '', // 基准编码
        ZB_INDEXTYPE: 'djz', // 基准类型
        ZB_INDEXCODEA: '000300', // 基准A
        ZB_INDEXWEIGHTA: '0.0000', // 基准A权重
        ZB_INDEXCODEB: '000300', // 基准B
        ZB_INDEXWEIGHTB: '0.0000', // 基准B权重
        dataFreqOpen:'true',//数据频率过滤是否开启
        dataFreq:'1' //数据频率  1 日频 2 周频  3 月频
      },
      dataFreqOptionList: [],
      userDataFreqOptionList:[],
      ZB_INDEXTYPEOption: [
        {
          id: 'djz',
          label: '单基准'
        },
        {
          id: 'fhjz',
          label: '复合基准'
        }
      ],
      datumOption: [],
      searchRules: {
        // date: [{ required: true, trigger: "change", validator: validateDate }],
        //ddate_: [{required: true, message: "请选择日期", trigger: "change"}],
        fundName: [{ required: true, message: '请选择产品', trigger: 'change' }],
        ddate_: [
          {required: true, message: "请选择日期", trigger: "change"},
          {validator: validateRangeDate, trigger: 'blur' }
        ]
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
      name: 'iframeVue_reportZJFOF',
      id: 'J_iframe_id_reportZJFOF',
      baseApi: '', // 页面根地址
      exportButton: false,
      onButton:false,
      exportText: '导出',
      exportButton2: false, // 导出 word
      exportIcon2: 'el-icon-download',
      /*exportText2: '导出Word',*/
      exportText2: '导出',
      benchmarkA: '',
      dateTime:'',
      onSub:'查询',
      exportIcon:'el-icon-search'
    }
  },
  mounted() {
    var self = this
    // self.getContrasOptions()
    // self.getDate()
    self.baseApi = process.env.BASE_API
    if(store.state.edims.userType == '2' || store.state.edims.userType == 2){
      self.left = true;
      self.showTreeKeyArray = ['产品列表'];
    }
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
    '$route.path'(val) {
      if (val == '/jxbg/foffxbg' && this.$store.getters.isHome === true) {
        this.$store.commit('SET_HOME_STATUS', false)
        var self = this
        let beg;
        let end;
        if (self.$route.query.rows.ddate_ && self.$route.query.rows.ddate_.length) {

          beg = self.$route.query.rows.ddate_[0]
          end = self.$route.query.rows.ddate_[1]
        }
        self.formInline.ddate_ = [beg,end]
        self.formInline.beginDate = beg
        self.formInline.endDate = end
        self.formInline.fundCode = self.$route.query.rows.fundCode
        self.formInline.fundName = self.$route.query.rows.fundName
        self.fundCode = self.$route.query.rows.fundCode
        self.timDate = self.$route.query.rows.createDate
        self.onSubmit('formInline')
      }
    },
  },
  methods: {
    /**
     * @description 是否展示更多查询
     */
    showMoreQuery() {
      this.isShowMoreQuery = !this.isShowMoreQuery
    },
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
      this.onButton = true
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
            this.onButton = false
            resolve()
          })
          .catch((err) => {
            this.onButton = false
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
              this.formInline.ddate_ = [beg,end]
            }
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
    },

    getDataFreqOptions(type){
      // 字典类型
      let params = type
      commonApi.edimsSelectType(params).then(res => {
        let { status, data } = res.data
        if (status === 0) {
          this.dataFreqOptionList = data
          this.userDataFreqOptionList=data
        }
      })
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
          type: 'warning'
        })
        return
      } else if (this.timDate == '' || this.timDate == undefined || this.timDate == null) {
        this.offOn = false
        this.timDate = ''
        this.$message({
          message: '未获取到成立日！',
          type: 'warning'
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
          this.$message.warning('只能输入大于等于0的数')
          this.formInline.ZB_INDEXWEIGHTA = '0.0000'
          return
        }
        if (this.formInline.ZB_INDEXWEIGHTB != '') {
          if (Number(this.formInline.ZB_INDEXWEIGHTA) + Number(this.formInline.ZB_INDEXWEIGHTB) > 100) {
            this.$message.closeAll()
            this.$message.warning('基金A、B权重不能超过100%')
            this.formInline.ZB_INDEXWEIGHTA = '0'
          } else {
            this.formInline.ZB_INDEXWEIGHTA = '' + Number(this.formInline.ZB_INDEXWEIGHTA).toFixed(4)
          }
        }
      } else {
        if (!regex.test(this.formInline.ZB_INDEXWEIGHTB)) {
          this.$message.closeAll()
          this.$message.warning('只能输入大于等于0的数')
          this.formInline.ZB_INDEXWEIGHTB = '0.0000'
          return
        }
        if (this.formInline.ZB_INDEXWEIGHTA != '') {
          if (Number(this.formInline.ZB_INDEXWEIGHTA) + Number(this.formInline.ZB_INDEXWEIGHTB) > 100) {
            this.$message.closeAll()
            this.$message.warning('基金A、B权重不能超过100')
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
                this.userDataFreqOptionList=this.dataFreqOptionList.filter(opt => opt.dimCde >= tempDataFreq)
              }else{
                this.userDataFreqOptionList=this.dataFreqOptionList
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
    handleSubmitClick(arr) {
      this.dialogMask = false
      this.fundCode = arr[0].VC_FUNDCODE || ''
      this.formInline.fundCode = arr[0].VC_FUNDCODE || ''
      this.formInline.fundName = arr[0].VC_FUNDNAME || ''
      this.timDate = arr[0].D_CREATE_DATE || ''
      this.selectList = arr
      //估值最新确认日期
      this.initTimGzLastDate(arr[0].VC_FUNDCODE || '')
      this.initDataFreq(arr[0].VC_FUNDCODE || '')
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
    file_vmrisk_src(templateCode, beginDate, endDate, fundCode, benchmarkA, benchmarkB, benchmarkAValue, benchmarkBValue, kpiCode, contrasCode,dataFreqOpen,dataFreq) {
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
          self.$fun.searchButtonDisabled('issearchFxButton', self)
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
      /* if (this.formInline.ddate_ && this.formInline.ddate_.length) {
          this.formInline.beginDate = this.formInline.ddate_[0];
          this.formInline.endDate = this.formInline.ddate_[1];
        }*/
      var self = this
      self.onButton = true
      self.onSub = '查询中...'
      self.exportButton2 = true
      self.exportIcon = 'el-icon-loading'
      if (self.formInline.ZB_INDEXTYPE == 'djz') {
        self.formInline.ZB_INDEXCODEB = ''
        self.formInline.ZB_INDEXWEIGHTA = ''
        self.formInline.ZB_INDEXWEIGHTB = ''
      }
      try {
        self.iframeData.src = this.file_vmrisk_src(
          // "2ae0c3f9-f8ee-4cab-b7c0-65b0f654548e",
          '82b18752-2367-4083-8fb8-02d3126c023d',
          self.formInline.ddate_[0],
          self.formInline.ddate_[1],
          self.formInline.fundCode,
          self.formInline.ZB_INDEXCODEA,
          self.formInline.ZB_INDEXCODEB,
          self.formInline.ZB_INDEXWEIGHTA,
          self.formInline.ZB_INDEXWEIGHTB,
          '',
          '',
          self.formInline.dataFreqOpen,
          self.formInline.dataFreq,
          'DWJZ',
          '104'
        )
      } catch (e) {
        console.log(e)
      }
    },
    // 导出
    fun_export_PDF() {
      var self = this
      self.exportButton2 = true
      self.exportIcon2 = 'el-icon-loading'
      self.exportText2 = '导出数据中...'
      const templateCode = '82b18752-2367-4083-8fb8-02d3126c023d'
      const wordName = 'FOF类绩效报告.pdf'
      // fun.fun_exportwordrisk(wordName);const fundName = self.formInline.fundName
      const fundName = self.formInline.fundName
      const beginDate = self.formInline.ddate_[0]
      const endDate = self.formInline.ddate_[1]
      const wordOption = { pagedir: 'h' } // vm导出word说明文档中相反，h为纵向，v为横向，默认为横向
      fun.fun_exportPDFOption(wordName, JSON.stringify(wordOption), this.id, templateCode, fundName, beginDate, endDate)
      setTimeout(() => {
        this.exportButton2 = false
        this.exportIcon2 = 'el-icon-download'
        this.exportText2 = '导出'
      }, 10000)
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
        self.exportButton2 = true
        self.exportIcon2 = 'el-icon-loading'
        self.exportText2 = '导出数据中...'
        const templateCode = '82b18752-2367-4083-8fb8-02d3126c023d'
        const wordName = 'FOF类绩效报告.pdf'
        const fundName = self.formInline.fundName
        const beginDate = self.formInline.ddate_[0]
        const endDate = self.formInline.ddate_[1]
        const wordOption = { pagedir: 'h' } // vm导出word说明文档中相反，h为纵向，v为横向，默认为横向
        fun.fun_exportPDFOption(wordName, JSON.stringify(wordOption), this.id, templateCode, fundName, beginDate, endDate)
        setTimeout(() => {
          this.exportButton2 = false
          this.exportIcon2 = 'el-icon-download'
          this.exportText2 = '导出'
        }, 10000)
      }
    },
    // 导出vm
    fun_export() {
      var self = this

      fun.file_vmrisk_download(
        // 报告模板ID  新建报告VUE界面需要更换相应的模板ID
        '82b18752-2367-4083-8fb8-02d3126c023d',
        self.formInline.ddate_[0],
        self.formInline.ddate_[1],
        self.formInline.fundCode,
        self.formInline.ZB_INDEXCODEA,
        self.formInline.ZB_INDEXCODEB,
        self.formInline.ZB_INDEXWEIGHTA,
        self.formInline.ZB_INDEXWEIGHTB,
        'DWJZ',
        '104'
      )

      setTimeout(function () {
        self.exportButton2 = false
        self.exportIcon2 = 'el-icon-download'
        self.exportText2 = '导出'
      }, 20000)
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
  height: 88%;
  position: relative;

  .zhezhao {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
  }
}
::v-deep .standard-form .el-form-item {
  margin-bottom: 5px !important;
}
</style>

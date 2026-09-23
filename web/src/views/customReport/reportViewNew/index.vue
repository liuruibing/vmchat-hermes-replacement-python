<template>
  <div style="height: 100%" class="PerformanceReportStyle">
    <el-container style="height: 100%">
      <el-main style="height: 100%; overflow-x: hidden; overflow-y: hidden; padding: 10px 0;">
        <div class="standard-form-margin">
          <div class="inner-margin">
            <el-form ref="formInline" :inline="true" :model="formInline" :rules="searchRules"
              class="demo-form-inline form_inline_search standard-form" style="margin-top: 10px">
              <el-row>
                <el-col :span="24">
                  <div class="grid-content bg-purple analyse-page">
                    <el-form-item prop="templateCode">
                      <el-select v-model="formInline.templateCode" size="small" filterable clearable placeholder="请选择模板"
                        @change="handleTemplateChange">
                        <el-option v-for="item in templateList" :key="item.templateCode" :label="item.templateName"
                          :value="item.templateCode">
                          <span style="float: left">{{ item.templateName }}</span>
                          <span style="float: right; color: #8492a6; font-size: 12px; padding-left: 10px;">{{
                            getReportTypeName(item.vcTempType) }}</span>
                        </el-option>
                      </el-select>
                    </el-form-item>

                    <el-form-item label="" prop="fundName" class="fund-select-form-item">
                      <el-tooltip :content="formInline.fundName" :disabled="!formInline.fundName" effect="dark"
                        placement="top-start">
                        <el-input v-model="formInline.fundName" clearable @keydown.native.prevent @paste.native.prevent
                          :style="{ cursor: 'pointer' }" @clear="handleClearProduct" placeholder="请选择产品" size="small"
                          @click.native="showFloatSelector" @mouseenter.native="showFloatSelector"
                          @blur.native="handleInputBlur" />
                      </el-tooltip>

                      <ProductFloatSelector ref="productFloatSelector" :visible="floatSelectorVisible"
                        :route-path="$route.path" @select-product="handleSubmitClick" @hide-selector="hideFloatSelector"
                        @mouseenter.native="handleSelectorMouseEnter" @mouseleave.native="handleSelectorMouseLeave" />
                    </el-form-item>

                    <el-form-item class="mb20" label="日期" prop="ddate_">
                      <el-date-picker v-model="formInline.ddate_" :picker-options="dateShortTPCTA()" align="left"
                        end-placeholder="结束日期" popper-class="popperDateShortTP" range-separator="-" size="small"
                        start-placeholder="开始日期" type="daterange" unlink-panels
                        value-format="yyyy-MM-dd"></el-date-picker>
                    </el-form-item>
                    <el-form-item prop="desensitizationFlag">
                      <el-checkbox-group v-model="formInline.desensitizationFlag"
                        @change="handlecheckeddesensitizationChange">
                        <el-checkbox label="脱敏" value="true"></el-checkbox>
                      </el-checkbox-group>
                    </el-form-item>

                    <el-form-item v-show="showDesensitization" prop="desensitizationFun">
                      <el-select v-model="formInline.desensitizationFun" size="small">
                        <el-option label="不显示名称、代码" value="ALL"></el-option>
                        <el-option label="仅屏蔽部分字符" value="PAR"></el-option>
                      </el-select>
                    </el-form-item>
                    <el-form-item label="数据频率" prop="dataFreq">
                      <el-select v-model="formInline.dataFreq" size="small" clearable filterable>
                        <el-option v-for="item in userDataFreqOptionList" :key="item.dimCde" :label="item.dimNme"
                          :value="item.dimCde" />
                      </el-select>
                    </el-form-item>
                    <el-form-item class="">
                      <el-button :icon="exportIcon" style="margin-bottom: 5px" size="small" :disabled="onButton"
                        type="primary" @click="onSubmit('formInline')">{{ onSub }}</el-button>
                      <el-button type="info" plain icon="el-icon-refresh-left" size="small"
                        @click="resetForm('formInline')">重置</el-button>
                      <el-button type="info" plain :icon="exportIcon2" style="margin-bottom: 5px"
                        :disabled="exportButton2 || !hasQueried" @click="fun_export_PDF" size="small">
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
                      <el-select v-model="formInline.ZB_INDEXTYPE" placeholder="请选择" size="small">
                        <el-option v-for="item in ZB_INDEXTYPEOption" :key="item.id" :label="item.label"
                          :value="item.id"></el-option>
                      </el-select>
                    </el-form-item>
                  </div>
                  <div v-show="formInline.ZB_INDEXTYPE == '1'" style="display: inline-block">
                    <el-form-item label="选择基准">
                      <el-select v-model="formInline.ZB_INDEXCODEA" placeholder="请选择" size="small">
                        <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label"
                          :value="item.id"></el-option>
                      </el-select>
                    </el-form-item>
                  </div>
                  <div v-show="formInline.ZB_INDEXTYPE == '2'" style="display: inline-block">
                    <el-form-item label="基准 A">
                      <el-select v-model="formInline.ZB_INDEXCODEA" placeholder="请选择" size="small">
                        <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label"
                          :value="item.id"></el-option>
                      </el-select>
                    </el-form-item>
                    <el-form-item label="比例">
                      <el-input v-model="formInline.ZB_INDEXWEIGHTA" size="small" style="width: 85px !important"
                        @blur="handleInputWeight('A')"></el-input>
                      %
                    </el-form-item>
                  </div>
                  <div v-show="formInline.ZB_INDEXTYPE == '2'" style="display: inline-block">
                    <el-form-item label="基准 B">
                      <el-select v-model="formInline.ZB_INDEXCODEB" placeholder="请选择" size="small">
                        <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label"
                          :value="item.id"></el-option>
                      </el-select>
                    </el-form-item>
                    <el-form-item label="比例">
                      <el-input v-model="formInline.ZB_INDEXWEIGHTB" size="small" style="width: 85px !important"
                        @blur="handleInputWeight('B')"></el-input>
                      %
                    </el-form-item>
                  </div>
                  <div style="display: inline-block">
                    <el-form-item label="对比基准">
                      <el-select v-model="formInline.contrasCode" clearable collapse-tags multiple placeholder="请选择"
                        size="small" @change="changeContrasCode"
                        :class="formInline.contrasCode.length > 1 && 'custom-select-multiple-tags50'">
                        <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label"
                          :value="item.id"></el-option>
                      </el-select>
                    </el-form-item>
                  </div>
                  <div style="display: inline-block">
                    <el-form-item label="行业类型">
                      <el-select v-model="formInline.industryType" clearable collapse-tags placeholder="请选择"
                        size="small">
                        <el-option v-for="item in industryTypeOptions" :key="item.id" :label="item.label"
                          :value="item.id"></el-option>
                      </el-select>
                    </el-form-item>
                  </div>
                  <el-form-item label="因子类型" prop="factorType">
                    <template slot="label">因子类型
                      <el-tooltip content="只作用于多因子报告类型" placement="top" effect="light">
                        <i class="el-icon-info"></i>
                      </el-tooltip>
                    </template>
                    <el-select v-model="formInline.factorType" size="small" clearable filterable>
                      <el-option v-for="item in factorTypeOptionList" :key="item.dimCde" :label="item.dimNme"
                        :value="item.dimCde" />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>
            </el-form>
          </div>
        </div>

        <!-- iframe容器-->
        <div class="iframe-container" :style="{ height: 'calc(100% - 100px)' }">
          <div class="iframe-wrapper" :style="{
            zIndex: 10,
            opacity: 1,
            pointerEvents: 'auto'
          }">
            <iframeModule ref="iframeModule" :id="iframeData.id" :iframe-data="iframeData" :name="iframeData.name"
              @load="handleIframeLoad" />
          </div>
        </div>
      </el-main>
    </el-container>

  </div>
</template>

<script>
import iframeModule from '@/components/iframe'
import fun from '@/filters/common'
import { getToken } from '@/utils/auth'
import request from '@/utils/request'
import moment from 'moment'
import commonApi from '@/api/common.js'
import store from "../../../store";
import ProductFloatSelector from '@/components/productSelector/ProductFloatSelector'
import pageApi from '../tempManage/scripts/api'

export default {
  name: 'ReportViewNew',
  components: {
    iframeModule,
    ProductFloatSelector
  },
  data() {
    const validateRangeDate = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请选择日期范围'))
      } else {
        if (this.formInline.ddate_ !== null || this.formInline.ddate_ !== undefined || this.formInline.ddate_ !== '') {
          const startTime = new Date(this.formInline.ddate_[0])
          const endTime = new Date(this.formInline.ddate_[1])
          const fundCreateTime = new Date(this.timDate)
          const fundEndTime = new Date(this.dateTime)
          if (endTime > fundEndTime) {
            callback(new Error('结束日期不能大于产品最新的估值确认日期'))
          } else if (startTime < fundCreateTime) {
            callback(new Error('开始日期不能早于产品的成立日期'))
          } else if (startTime > endTime) {
            callback(new Error('开始日期不能大于结束日期'))
          } else {
            callback()
          }
        } else {
          callback()
        }
      }
    }

    return {
      templateList: [],
      // 控制悬浮框显示/隐藏
      floatSelectorVisible: false,
      isHoveringSelector: false,
      isShowMoreQuery: false,
      selectList: [],

      pickerOptions: {},
      treeData: [],
      showTreeKeyArray: [],
      // 搜索
      formInline: {
        templateCode: '',
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
        desensitizationFlag: '', //脱敏标志
        desensitizationFun: 'ALL', //脱敏方法 ALL 不显示名称和代码  PAR 仅屏蔽部分字符
        dataFreqOpen: 'true',//数据频率过滤是否开启
        dataFreq: '1',//数据频率  1 日频 2 周频  3 月频
        contrasCode: [],//对比基准
        contrasCodes: '',//对比基准,逗号分割
        industryType: 'SWSR',//默认申万行业
        factorType: ''
      },
      dataFreqOptionList: [],
      userDataFreqOptionList: [],
      ZB_INDEXTYPEOption: [
        { id: '0', label: '无基准' },
        { id: '1', label: '单基准' },
        { id: '2', label: '复合基准' }
      ],
      industryTypeOptions: [
        {
          id: 'SWSR',
          label: '申万行业'
        },
        {
          id: 'ZXSR',
          label: '中信行业'
        }
      ],
      datumOption: [],
      factorTypeOptionList: [
        { dimCde: "CNE5", dimNme: "CNE5" },
        { dimCde: "CNE6", dimNme: "CNE6" }
      ],
      searchRules: {
        templateCode: [{ required: true, message: '请选择模板', trigger: 'change' }],
        fundName: [{ required: true, message: '请选择产品', trigger: 'change' }],
        ddate_: [
          { required: true, message: "请选择日期", trigger: "change" },
          { validator: validateRangeDate, trigger: 'blur' }
        ]
      },
      issearchFxButton: false,
      noData: '--', // 没有数据

      iframeData: {
        id: 'J_iframe_id_report_view',
        name: 'iframeVue_report_view',
        src: ''
      },
      scrollPosition: 0,
      queryParams: null,
      hasQueried: false,

      //成立日
      timDate: '',
      //估值表最新确认日
      dateTime: '',
      //开关
      offOn: false,
      baseApi: '', // 页面根地址
      exportButton: false,
      exportText: '导出',
      exportButton2: false, // 导出 PDF
      onButton: false,
      exportIcon2: 'el-icon-download',
      exportText2: '导出',
      benchmarkA: '',
      onSub: '查询',
      exportIcon: 'el-icon-search',
      showDesensitization: false,
    }
  },
  watch: {
    '$route.query.templateCode': {
      handler(newVal) {
        if (newVal) {
          this.loadTemplateList()
          this.formInline.templateCode = newVal;
          this.handleTemplateChange(); // 如果之前已经查询过，自动清理旧 iframe

          // 清除 URL 中的 templateCode 参数，避免刷新或切换菜单时一直保留
          const query = { ...this.$route.query };
          delete query.templateCode;
          this.$router.replace({ path: this.$route.path, query }).catch(() => { });
        }
      },
      immediate: true
    }
  },
  mounted() {
    var self = this
    var baseTime = store.state.edims.baseTime
    if (baseTime && baseTime.beginDate && baseTime.endDate) {
      self.formInline.ddate_ = [baseTime.beginDate, baseTime.endDate]
      self.formInline.beginDate = baseTime.beginDate
      self.formInline.endDate = baseTime.endDate
    }

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

    this.loadTemplateList()
    this.setupScrollListener()
    this.getDataFreqOptions("DATAFREQ")
    document.addEventListener('click', this.handleGlobalClick, true);
  },
  beforeDestroy() {
    this.removeScrollListener()
    document.removeEventListener('click', this.handleGlobalClick, true);
  },
  methods: {
    getReportTypeName(reportType) {
      if (reportType === '0') return '标准模板'
      if (reportType === '1') return '自定义模板'
    },
    loadTemplateList() {
      const params = {
        pageNum: 1,
        pageSize: 9999,
        templateName: '',
        fType: '1',
        vcTempType: '',
        orderString: ''
      }
      pageApi.getTempList(params).then(res => {
        const { status, data } = res.data;
        if (status === 200 && data) {
          const list = data.list || [];
          this.templateList = list.map(item => ({
            ...item,
            templateCode: item.fTemplateID,
            templateName: item.vcTemplatEname,
            vcTempType: item.vcTempType
          }));
          // 判断当前模板是否存在
          if (this.formInline.templateCode) {
            const findIndex = this.templateList.findIndex(item => {
              return item.templateCode === this.formInline.templateCode
            });
            if (findIndex < 0) {
              this.formInline.templateCode = "";
              this.handleTemplateChange();
            }
          }
        }
      }).catch(err => {
        console.error(err);
      });
    },
    handleTemplateChange() {
      this.iframeData.src = '';
      this.hasQueried = false;
      this.queryParams = null;
    },
    handleClearProduct() {
      this.formInline.fundCode = '';
      this.formInline.fundName = '';
      this.timDate = '';
      this.selectList = []
    },
    // 显示悬浮框
    showFloatSelector() {
      this.floatSelectorVisible = true;
      this.isHoveringSelector = false;
    },
    // 隐藏悬浮框
    hideFloatSelector() {
      this.floatSelectorVisible = false;
      this.isHoveringSelector = false;
    },
    // 鼠标移入悬浮框，标记
    handleSelectorMouseEnter() {
      this.isHoveringSelector = true;
    },
    // 鼠标移出悬浮框，关闭并重置标记
    handleSelectorMouseLeave() {
      const isHoveringDropdown = document.querySelector('.el-select-dropdown:hover');
      const isHoveringTooltip = document.querySelector('.el-tooltip__popper:hover');
      const isHoveringSelector = this.$refs.floatContainer && document.querySelector('.product-float-selector:hover');

      if (isHoveringDropdown || isHoveringTooltip || isHoveringSelector) {
        return;
      }
      this.isHoveringSelector = false;
      this.floatSelectorVisible = false;
    },

    handleInputBlur() {
      setTimeout(() => {
        if (!this.isHoveringSelector) {
          this.floatSelectorVisible = false;
        }
      }, 100);
    },
    handleGlobalClick(e) {
      const isHoveringDropdown = document.querySelector('.el-select-dropdown:hover');
      if (isHoveringDropdown) {
        return;
      }
      // 获取input和悬浮框元素
      const inputEl = this.$el.querySelector('.fund-select-form-item .el-input');
      const selectorEl = this.$refs.productFloatSelector && this.$refs.productFloatSelector.$el;

      // 若点击区域既不是input，也不是悬浮框，关闭悬浮框
      if (inputEl && selectorEl) {
        if (!inputEl.contains(e.target) && !selectorEl.contains(e.target)) {
          this.floatSelectorVisible = false;
          this.isHoveringSelector = false;
        }
      }
    },

    changeContrasCode(val) {
      if (val.length > 3) {
        this.$message({
          type: 'warning',
          message: '对比基准最多只能选三个'
        })
        this.formInline.contrasCode.splice(-1)
      }
    },

    setupScrollListener() {
      const iframe = document.getElementById(this.iframeData.id);
      if (!iframe) return;

      const handleScroll = () => {
        try {
          if (iframe.contentWindow) {
            this.scrollPosition = iframe.contentWindow.scrollY;
          }
        } catch (e) { }
      };

      this.scrollListener = handleScroll;

      iframe.addEventListener('load', () => {
        this.handleIframeLoad();
        if (this.$refs.iframeModule) {
          this.$refs.iframeModule.loading = false;
        }
        try {
          if (iframe.contentWindow) {
            iframe.contentWindow.addEventListener('scroll', handleScroll);
          }
        } catch (e) { }
      });

      try {
        if (iframe.contentWindow) {
          iframe.contentWindow.addEventListener('scroll', handleScroll);
        }
      } catch (e) { }
    },

    removeScrollListener() {
      const iframe = document.getElementById(this.iframeData.id);
      if (iframe && iframe.contentWindow && this.scrollListener) {
        iframe.contentWindow.removeEventListener('scroll', this.scrollListener);
        this.scrollListener = null;
      }
    },

    showMoreQuery() {
      this.isShowMoreQuery = !this.isShowMoreQuery
    },
    getTimeBig() {
      if (this.formInline.fundCode == '' || this.formInline.fundCode == null) {
        if (this.formInline.beginDate != '') {
          this.$message({
            message: '请选择产品代码',
            type: 'warning'
          })
        }
        this.formInline.beginDate = ''
      } else {
        if (this.formInline.beginDate != '' && this.formInline.beginDate < this.timDate) {
          setTimeout(() => {
            this.formInline.beginDate = this.timDate;
          }, 500);
        }
      }
    },
    getTimeEnd() {
      if (this.formInline.fundCode == '' || this.formInline.fundCode == null) {
        if (this.formInline.endDate != '') {
          this.$message({
            message: '请选择产品代码',
            type: 'warning'
          })
        }
        this.formInline.endDate = ''
      } else {
        if ((this.formInline.endDate != this.dateTime) && (this.formInline.endDate != '' || this.formInline.endDate != null)) {
          this.getTimes(this.formInline.fundCode, this.formInline.endDate)
        }
      }
    },
    getTimes(code, end) {
      this.onButton = true
      return new Promise((resolve, reject) => {
        const params = {
          indexCode: 'dacc5f54-8ff8-418b-984a-52a18409d716',
          fundCode: code,
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
              if (this.dateTime != null && this.formInline.endDate > this.dateTime) {
                this.formInline.endDate = this.dateTime
              }
            }
            resolve()
            this.onButton = false
          })
          .catch((err) => {
            this.onButton = false
            resolve()
          })
      })
    },
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
              this.formInline.ddate_ = [beg, end]
            }
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
    },
    getDataFreqOptions(type) {
      let params = type
      commonApi.edimsSelectType(params).then(res => {
        let { status, data } = res.data
        if (status === 0) {
          this.dataFreqOptionList = data
          this.userDataFreqOptionList = data
        }
      })
    },
    handlecheckeddesensitizationChange(value) {
      this.showDesensitization = value;
    },
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
    dateShortTPCTA() {
      var self = this
      if (self.dateTime !== null && self.dateTime !== ""
        && self.timDate !== null && self.timDate !== "") {
        const pickerOptions = {
          shortcuts: [{
            text: '本周',
            onClick(picker) {
              const end = moment(self.dateTime).format('YYYY-MM-DD')
              const start = moment(end).isoWeekday(1).format('YYYY-MM-DD')
              const create = self.timDate
              const createTime = moment(self.timDate).format('YYYY-MM-DD')
              picker.$emit('pick', [moment(start).isAfter(create) === true ? start : createTime, end])
            }
          }, {
            text: '本月',
            onClick(picker) {
              const end = moment(self.dateTime).format('YYYY-MM-DD')
              const start = moment([moment(end).year(), 0, 1]).month(moment(end).month()).format('YYYY-MM-DD')
              const create = self.timDate
              const createTime = moment(self.timDate).format('YYYY-MM-DD')
              picker.$emit('pick', [moment(start).isAfter(create) === true ? start : createTime, end])
            }
          }, {
            text: '本季度',
            onClick(picker) {
              const end = moment(self.dateTime).format('YYYY-MM-DD')
              const start = moment(moment(end).year() + '-01-01').quarter(moment(end).quarter()).format('YYYY-MM-DD')
              const create = self.timDate
              const createTime = moment(self.timDate).format('YYYY-MM-DD')
              picker.$emit('pick', [moment(start).isAfter(create) === true ? start : createTime, end])
            }
          }, {
            text: '今年以来',
            onClick(picker) {
              const end = moment(self.dateTime).format('YYYY-MM-DD')
              const start = moment(end).year() + '-01-01'
              const create = self.timDate
              const createTime = moment(self.timDate).format('YYYY-MM-DD')
              picker.$emit('pick', [moment(start).isAfter(create) === true ? start : createTime, end])
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
              const createTime = moment(self.timDate).format('YYYY-MM-DD')
              picker.$emit('pick', [moment(start).isAfter(create) === true ? start : createTime, end])
            }
          },
          {
            text: '近三个月',
            onClick(picker) {
              const end = moment(self.dateTime).format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(3, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              const create = self.timDate
              const createTime = moment(self.timDate).format('YYYY-MM-DD')
              picker.$emit('pick', [moment(start).isAfter(create) === true ? start : createTime, end])
            }
          },
          {
            text: '近半年',
            onClick(picker) {
              const end = moment(self.dateTime).format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(6, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              const create = self.timDate
              const createTime = moment(self.timDate).format('YYYY-MM-DD')
              picker.$emit('pick', [moment(start).isAfter(create) === true ? start : createTime, end])
            }
          },
          {
            text: '近一年',
            onClick(picker) {
              const end = moment(self.dateTime).format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(1, 'year').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              const create = self.timDate
              const createTime = moment(self.timDate).format('YYYY-MM-DD')
              picker.$emit('pick', [moment(start).isAfter(create) === true ? start : createTime, end])
            }
          },
          {
            text: '近三年',
            onClick(picker) {
              const end = moment(self.dateTime).format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(3, 'year').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              const create = self.timDate
              const createTime = moment(self.timDate).format('YYYY-MM-DD')
              picker.$emit('pick', [moment(start).isAfter(create) === true ? start : createTime, end])
            }
          }]
        }
        return pickerOptions
      }
    },
    handleInputWeight(type) {
      if (type == 'A') {
        const val = this.formInline.ZB_INDEXWEIGHTA
        const isValid = /^\d+(\.\d{1,4})?$/.test(val);
        if (!isValid) {
          this.$message.warning("请输入有效的正数，最多4位小数");
          this.formInline.ZB_INDEXWEIGHTA = '';
        }
      } else {
        const val = this.formInline.ZB_INDEXWEIGHTB
        const isValid = /^\d+(\.\d{1,4})?$/.test(val);
        if (!isValid) {
          this.$message.warning("请输入有效的正数，最多4位小数");
          this.formInline.ZB_INDEXWEIGHTB = '';
        }
      }
    },
    getStandard() {
      request({
        url: `/api/report/v1.0/data/sql/c6e3b2b7-f58c-45a8-b6ff-1834162ce652`,
        method: 'post',
        data: {
          fundCode: this.formInline.fundCode,
          indexCode: 'c6e3b2b7-f58c-45a8-b6ff-1834162ce652'
        }
      }).then((res) => {
        if (res.data.status === 0) {
          if (res.data.data.length > 0) {
            this.formInline.ZB_INDEXTYPE = '1';
            this.formInline.ZB_INDEXCODEA = res.data.data[0].benchmarkA;
            if (this.formInline.ZB_INDEXCODEA == '') {
              this.formInline.ZB_INDEXCODEA = '000300'
            }
          } else {
            this.formInline.ZB_INDEXCODEA = '000300'
          }
        }
      })
    },

    initTimGzLastDate(fundCode) {
      return new Promise((resolve, reject) => {
        const params = {
          indexCode: 'dacc5f54-8ff8-418b-984a-52a18409d716',
          fundCode: fundCode,
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

    initDataFreq(fundCode) {
      return new Promise((resolve, reject) => {
        const params = {
          fundCode: fundCode,
        }
        request({
          url: `/api/jxbg/getUserReportDataFreqList`,
          method: 'post',
          data: params
        })
          .then((res) => {
            if (res.data.status === 0) {
              if (res.data.data.length === 1) {
                const tempDataFreq = res.data.data[0].dimCde
                this.formInline.dataFreq = tempDataFreq
                this.userDataFreqOptionList = this.dataFreqOptionList.filter(opt => opt.dimCde >= tempDataFreq)
              } else {
                this.userDataFreqOptionList = this.dataFreqOptionList
              }
            }
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
    },

    handleSubmitClick(arr) {
      this.formInline.fundCode = arr[0].VC_FUNDCODE || ''
      this.formInline.fundName = arr[0].VC_FUNDNAME || ''
      this.timDate = arr[0].D_CREATE_DATE || ''
      this.selectList = arr
      this.initTimGzLastDate(arr[0].VC_FUNDCODE || '')
      this.initDataFreq(arr[0].VC_FUNDCODE || '')

      this.floatSelectorVisible = false
    },

    onSubmit(formName) {
      var self = this
      self.$refs[formName].validate((valid) => {
        if (valid) {
          try {
            self.updateReportIframe();
          } catch (e) {
          }
          self.$fun.searchButtonDisabled('issearchFxButton', self)
        } else {
          return false
        }
      })
    },

    updateReportIframe() {
      const params = { ...this.formInline };
      if (this.formInline.ZB_INDEXTYPE == '0') {
        params.ZB_INDEXCODEA = '';
        params.ZB_INDEXCODEB = '';
        params.ZB_INDEXWEIGHTA = '';
        params.ZB_INDEXWEIGHTB = '';
      } else if (this.formInline.ZB_INDEXTYPE == '1') {
        params.ZB_INDEXCODEB = '';
        params.ZB_INDEXWEIGHTA = '';
        params.ZB_INDEXWEIGHTB = '';
      }
      this.queryParams = params;
      this.hasQueried = true;
      const iframeParams = {
        templateCode: this.formInline.templateCode,
        beginDate: this.formInline.ddate_[0],
        endDate: this.formInline.ddate_[1],
        fundCode: this.formInline.fundCode,
        benchmarks: this.formInline.ZB_INDEXTYPE,
        benchmarkA: params.ZB_INDEXCODEA,
        benchmarkB: params.ZB_INDEXCODEB,
        benchmarkAValue: params.ZB_INDEXWEIGHTA,
        benchmarkBValue: params.ZB_INDEXWEIGHTB,
        kpiCode: '',
        contrasCode: this.formInline.contrasCode.join(","),
        industryType: this.formInline.industryType,
        factorType: this.formInline.factorType,
        desensitizationFlag: this.formInline.desensitizationFlag,
        desensitizationFun: this.formInline.desensitizationFun,
        dataFreqOpen: this.formInline.dataFreqOpen,
        dataFreq: this.formInline.dataFreq
      }
      this.iframeData.src = this.file_vmrisk_src_view(iframeParams);

      this.onButton = true;
      this.onSub = '查询中...';
      this.exportButton2 = true;
      this.exportIcon = 'el-icon-loading';
    },

    handleIframeLoad() {
      this.onButton = false;
      this.onSub = '查询';
      this.exportButton2 = false;
      this.exportIcon = 'el-icon-search';
    },

    resetForm(formName) {
      var self = this
      self.$refs[formName].resetFields()
      this.floatSelectorVisible = false
      this.formInline.fundCode = ''
      this.formInline.fundName = ''
      this.hasQueried = false
    },

    file_vmrisk_src_view(params) {
      let url = process.env.BASE_API + '/rest/report/interview.do?';
      for (let key in params) {
        if (params[key] !== undefined && params[key] !== null) {
          url += `${key}=${params[key]}&`;
        }
      }
      url += 'token=' + encodeURIComponent(getToken()) +
        '&autoRun=false&ajaxRun=true&showParam=true&showCondition=false&markFlag=false&srcSuffix=' +
        process.env.BASE_API +
        '&time=' + new Date().getTime();
      return url;
    },

    fun_export_PDF() {
      if (!this.hasQueried || !this.queryParams) {
        this.$message.warning('请先查询再进行导出');
        return;
      }

      const self = this;
      self.exportButton2 = true;
      self.exportIcon2 = 'el-icon-loading';
      self.exportText2 = '导出数据中...';

      const params = this.queryParams;

      const templateItem = this.templateList.find(t => t.templateCode === params.templateCode);
      const templateName = templateItem ? templateItem.templateName : '自定义报告';

      const pdfName = `${templateName}.pdf`;
      const covIndexCode = 'dc4d61469e2b4a9b875706e66e59ab25';
      const pdfOption = { pagedir: 'h' };

      fun.fun_exportPDFOption_GFJX_new(
        pdfName,
        JSON.stringify(pdfOption),
        this.iframeData.id,
        params.templateCode,
        params.fundCode,
        params.fundName,
        params.ddate_[0],
        params.ddate_[1],
        params.desensitizationFlag,
        params.desensitizationFun,
        params.dataFreqOpen,
        params.dataFreq,
        params.ZB_INDEXTYPE,
        params.benchmarkA,
        params.benchmarkB,
        params.benchmarkAValue,
        params.benchmarkBValue,
        covIndexCode,
        (res) => {
          self.exportButton2 = false;
          self.exportIcon2 = 'el-icon-download';
          self.exportText2 = '导出';
          self.$message.success(res.message);
        },
        (res) => {
          self.exportButton2 = false;
          self.exportIcon2 = 'el-icon-download';
          self.exportText2 = '导出';
          self.$message.error(res.message);
        }
      );
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

<style lang="scss" scoped>
.fund-select-form-item {
  position: relative;
  display: inline-block;
  min-width: 160px;
}

.el-dialog {
  width: 60% !important;
}

.customWidth {
  width: 80% !important;
}

input::-webkit-input-placeholder {
  color: #999 !important;
}

.iframe-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.iframe-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  transition: z-index 0.3s ease, opacity 0.3s ease;
}

::v-deep .iframeModule {
  width: 100%;
  height: 100%;
  border: none;
}

::v-deep .standard-form .el-form-item {
  margin-bottom: 5px !important;
}

::v-deep .el-select.custom-select-multiple-tags50 {
  .el-tag {
    max-width: 50% !important;
  }
}
</style>

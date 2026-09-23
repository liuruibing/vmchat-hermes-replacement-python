<template>
  <div style="height: 100%" class="PerformanceReportStyle">
    <el-container style="height: 100%">
      <el-main style="height: 100%; overflow-x: hidden; overflow-y: hidden; padding: 10px 0;">
        <div class="standard-form-margin">
          <div class="inner-margin">
            <el-form ref="formInline" :inline="true" :model="formInline" :rules="searchRules" class="demo-form-inline form_inline_search standard-form" style="margin-top: 10px">
              <el-row>
                <el-col :span="24">
                  <div class="grid-content bg-purple analyse-page">
                    <el-form-item label="" prop="fundName" class="fund-select-form-item">
                      <el-tooltip :content="formInline.fundName" :disabled="!formInline.fundName" effect="dark" placement="top-start">
                        <el-input v-model="formInline.fundName" clearable @keydown.native.prevent @paste.native.prevent :style="{cursor: 'pointer'}"
                                  @clear="handleClearProduct" placeholder="请选择产品" size="small" @click.native="showFloatSelector" @mouseenter.native="showFloatSelector" @blur.native="handleInputBlur"  />
                      </el-tooltip>

                      <ProductFloatSelector
                        ref="productFloatSelector"
                        :visible="floatSelectorVisible"
                        :route-path="$route.path"
                        @select-product="handleSubmitClick"
                        @hide-selector="hideFloatSelector"
                        @mouseenter.native="handleSelectorMouseEnter"
                        @mouseleave.native="handleSelectorMouseLeave"
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
                        <el-option label="不显示名称、代码" value="ALL"></el-option>
                        <el-option label="仅屏蔽部分字符" value="PAR"></el-option>
                      </el-select>
                    </el-form-item>
                    <el-form-item label="数据频率" prop="dataFreq">
                      <el-select v-model="formInline.dataFreq" size="small" clearable filterable >
                        <el-option v-for="item in userDataFreqOptionList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />

                      </el-select>
                    </el-form-item>
                    <el-form-item class="">
                      <el-button :icon="exportIcon" style="margin-bottom: 5px" size="small" :disabled="onButton" type="primary" @click="onSubmit('formInline')">{{onSub}}</el-button>
                      <el-button type="info" plain icon="el-icon-refresh-left" size="small" @click="resetForm('formInline')">重置</el-button>
                      <el-button type="info" plain :icon="exportIcon2" style="margin-bottom: 5px" :disabled="exportButton2 || !currentTabHasQuery" @click="fun_export_PDF" size="small">
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

        <!-- 替代tabs -->
        <div class="report-pills" style="padding-left:10px; margin-bottom: 10px; border-radius: 4px; border-bottom: 1px solid #e9c5a2;">
          <div
            v-for="tab in reportTabs"
            :key="tab.id"
            :class="{ 'pill-item': true, 'active': activeTab === tab.id }"
            @click="switchTab(tab.id)"
          >
            {{ tab.name }}
          </div>
        </div>

        <!-- iframe容器-->
        <div class="iframe-container" :style="{height: 'calc(100% - 140px)'}">
          <div
            v-for="tab in reportTabs"
            :key="tab.id"
            class="iframe-wrapper"
            :style="{
              zIndex: activeTab === tab.id ? 10 : 1,
              opacity: activeTab === tab.id ? 1 : 0,
              pointerEvents: activeTab === tab.id ? 'auto' : 'none'
            }"
          >
            <iframeModule
              :id="tab.iframeId"
              :iframe-data="tab.iframeData"
              :name="tab.iframeName"
              @load="handleIframeLoad(tab.id)"
            />
          </div>
        </div>
      </el-main>
    </el-container>

  </div>
</template>

<script>
import iframeModule from '@/components/iframe'
import fun from '@/filters/common'
import FundListDialog from '@/components/FundListDialog/ZjzqDialog'
import { getToken } from '@/utils/auth'
import request from '@/utils/request'
import moment from 'moment'
import commonApi from '@/api/common.js'
import store from "../../../store";
// 引入新悬浮框组件
import ProductFloatSelector from '@/components/productSelector/ProductFloatSelector'

export default {
  name: 'ReportGF_ZBGXC',
  components: {
    FundListDialog,
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
          const fundCreateTime=new Date(this.timDate)
          const fundEndTime=new Date(this.dateTime)
          if(endTime > fundEndTime){
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

    return {
      // 控制悬浮框显示/隐藏
      floatSelectorVisible: false,
      isHoveringSelector: false,
      //========
      isShowMoreQuery: false,
      // 选择产品弹窗
      productSelectorVisible: false,
      left: false,
      selectList: [],
      dialogMask: false,

      pickerOptions :{},
      productCheckArr: [],
      companyCheckArr: [],
      fundArray: [],
      treeData: [
        {
          label: '产品列表',
          id: 'zstgwb'
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
        desensitizationFun:'ALL', //脱敏方法 ALL 不显示名称和代码  PAR 仅屏蔽部分字符
        dataFreqOpen:'true',//数据频率过滤是否开启
        dataFreq:'1',//数据频率  1 日频 2 周频  3 月频
        contrasCode:[],//对比基准
        contrasCodes:'',//对比基准,逗号分割
        industryType:'SWSR',//默认申万行业
        factorType:'CNE5'//默认因子类型
      },
      dataFreqOptionList: [],
      userDataFreqOptionList:[],
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
        ]

      },
      issearchFxButton: false,
      /* fundCode: '', // code值
      fundName: '', // name */
      noData: '--', // 没有数据
      // 报告Tab相关配置，保持重叠显示
      activeTab: 'simple_xc', // 默认选中简版报告
      reportTemplateList:[],
      reportTabs: [],
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
  computed: {

    // 获取当前激活的tab
    currentTab() {
      return this.reportTabs.find(tab => tab.id === this.activeTab);
    },
    // 检查当前tab是否已经查询过
    currentTabHasQuery() {
      const tab = this.currentTab;
      return tab ? tab.hasQueried : false;
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

    // 初始化所有iframe的滚动监听
    this.initReportTemplateList()
    this.initScrollListeners();
    this.getDataFreqOptions("DATAFREQ")


    document.addEventListener('click', this.handleGlobalClick, true);
  },
  beforeDestroy() {
    // 移除所有滚动监听
    this.removeAllScrollListeners();

    document.removeEventListener('click', this.handleGlobalClick, true);
  },
  methods: {

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
    handleClearProduct() {
      this.formInline.fundCode = '';
      this.formInline.fundName = '';
      this.timDate = '';
      this.selectList = []

    },
    // 显示悬浮框
    showFloatSelector() {
      this.floatSelectorVisible = true;
      // 重置悬浮框悬浮标记
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
          //console.log('123')
          this.floatSelectorVisible = false;
          this.isHoveringSelector = false;
        }
      }
    },

    // 初始化所有iframe的滚动监听
    initScrollListeners() {
      this.reportTabs.forEach(tab => {
        this.setupScrollListener(tab);
      });
    },

    // 为单个iframe设置滚动监听
    setupScrollListener(tab) {
      const iframe = document.getElementById(tab.iframeId);
      if (!iframe) return;

      const handleScroll = () => {
        if (iframe.contentWindow) {
          tab.scrollPosition = iframe.contentWindow.scrollY;
        }
      };

      // 保存监听函数以便后续移除
      tab.scrollListener = handleScroll;

      // 监听iframe内容滚动
      if (iframe.contentWindow) {
        iframe.contentWindow.addEventListener('scroll', handleScroll);
      } else {
        // 如果iframe还没加载完成，等加载后再添加监听
        iframe.onload = () => {
          if (iframe.contentWindow) {
            iframe.contentWindow.addEventListener('scroll', handleScroll);
          }
        };
      }
    },

    // 移除单个iframe的滚动监听
    removeScrollListener(tab) {
      const iframe = document.getElementById(tab.iframeId);
      if (iframe && iframe.contentWindow && tab.scrollListener) {
        iframe.contentWindow.removeEventListener('scroll', tab.scrollListener);
        tab.scrollListener = null;
      }
    },

    // 移除所有iframe的滚动监听
    removeAllScrollListeners() {
      this.reportTabs.forEach(tab => {
        this.removeScrollListener(tab);
      });
    },

    // 切换Tab时恢复滚动位置
    restoreScrollPosition(tabId) {
      const tab = this.reportTabs.find(t => t.id === tabId);
      if (!tab) return;

      const iframe = document.getElementById(tab.iframeId);
      if (iframe && iframe.contentWindow && tab.scrollPosition > 0) {
        iframe.contentWindow.scrollTo(0, tab.scrollPosition);
      }
    },

    /**
     * 切换显示的iframe 重叠显示，只修改z-index、透明度和指针事件，主要是为了报告模块echarts能找到宽度，防止缩到一块
     */
    switchTab(tabId) {
      // 保存当前Tab的滚动位置
      const currentTab = this.reportTabs.find(t => t.id === this.activeTab);
      if (currentTab) {
        const iframe = document.getElementById(currentTab.iframeId);
        if (iframe && iframe.contentWindow) {
          currentTab.scrollPosition = iframe.contentWindow.scrollY;
        }
      }

      // 切换到新Tab
      this.activeTab = tabId;

      // 恢复新Tab的滚动位置
      this.$nextTick(() => {
        this.restoreScrollPosition(tabId);
      });
    },

    /**
     * @description 是否展示更多查询
     */
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
              this.formInline.ddate_ = [beg, end]
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
    handlecheckeddesensitizationChange(value) {
      this.showDesensitization = value;
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
              //判断开始日期是否再成立日期之前
              picker.$emit('pick', [moment(start).isAfter(create) === true ? start : createTime, end])
            }
          }, {
            text: '本月',
            onClick(picker) {
              const end = moment(self.dateTime).format('YYYY-MM-DD')
              const start = moment([moment(end).year(), 0, 1]).month(moment(end).month()).format('YYYY-MM-DD')
              const create = self.timDate
              const createTime = moment(self.timDate).format('YYYY-MM-DD')
              //判断开始日期是否再成立日期之前
              picker.$emit('pick', [moment(start).isAfter(create) === true ? start : createTime, end])
            }
          }, {
            text: '本季度',
            onClick(picker) {
              const end = moment(self.dateTime).format('YYYY-MM-DD')
              const start = moment(moment(end).year() + '-01-01').quarter(moment(end).quarter()).format('YYYY-MM-DD')
              const create = self.timDate
              const createTime = moment(self.timDate).format('YYYY-MM-DD')
              //判断开始日期是否再成立日期之前
              picker.$emit('pick', [moment(start).isAfter(create) === true ? start : createTime, end])
            }
          }, {
            text: '今年以来',
            onClick(picker) {
              const end = moment(self.dateTime).format('YYYY-MM-DD')
              const start = moment(end).year() + '-01-01'
              const create = self.timDate
              const createTime = moment(self.timDate).format('YYYY-MM-DD')
              //判断开始日期是否再成立日期之前
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
                //判断开始日期是否再成立日期之前
                picker.$emit('pick', [moment(start).isAfter(create) === true ? start : createTime, end])
              }
            }, {
              text: '近三个月',
              onClick(picker) {
                const end = moment(self.dateTime).format('YYYY-MM-DD')
                const start = moment(moment(end).subtract(3, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
                const create = self.timDate
                const createTime = moment(self.timDate).format('YYYY-MM-DD')
                //判断开始日期是否再成立日期之前
                picker.$emit('pick', [moment(start).isAfter(create) === true ? start : createTime, end])
              }
            }, {
              text: '近半年',
              onClick(picker) {
                const end = moment(self.dateTime).format('YYYY-MM-DD')
                const start = moment(moment(end).subtract(6, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
                const create = self.timDate
                const createTime = moment(self.timDate).format('YYYY-MM-DD')
                //判断开始日期是否再成立日期之前
                picker.$emit('pick', [moment(start).isAfter(create) === true ? start : createTime, end])
              }
            }, {
              text: '近一年',
              onClick(picker) {
                const end = moment(self.dateTime).format('YYYY-MM-DD')
                const start = moment(moment(end).subtract(1, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
                const create = self.timDate
                const createTime = moment(self.timDate).format('YYYY-MM-DD')
                //判断开始日期是否再成立日期之前
                picker.$emit('pick', [moment(start).isAfter(create) === true ? start : createTime, end])
              }
            }, {
              text: '近三年',
              onClick(picker) {
                const end = moment(self.dateTime).format('YYYY-MM-DD')
                const start = moment(moment(end).subtract(3, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
                const create = self.timDate
                const createTime = moment(self.timDate).format('YYYY-MM-DD')
                //判断开始日期是否再成立日期之前
                picker.$emit('pick', [moment(start).isAfter(create) === true ? start : createTime, end])
              }
            },],

          disabledDate(time) {
            // 设置产品的日期范围，成立日到最新的估值确认日期
            return time < new Date(self.timDate) || time > new Date(self.dateTime);
          },
        }
        return pickerOptions
      } else {
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
      if (this.formInline.fundCode == '' || this.formInline.fundName == '') {
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
      //this.timGZLastDate=
    },

    initReportTemplateList() {
      return new Promise((resolve, reject) => {
        const params = {
          indexCode: '69c2e09d-3081-47c2-b2bb-318553d8bcca'
        }
        request({
          url: `/api/report/v1.0/data/sql/69c2e09d-3081-47c2-b2bb-318553d8bcca`,
          method: 'post',
          data: params
        })
          .then((res) => {
            if (res.data.status === 0) {
              this.reportTemplateList = res.data.data
              for(let i=0;i<this.reportTemplateList.length;i++){
                let templateObject=this.reportTemplateList[i];
                let tabObject={
                  id: templateObject["ID"],
                  name: templateObject["NAME"],
                  templateCode: templateObject["TEMPLATECODE"],
                  iframeId: 'J_iframe_id_report_'+templateObject["ID"],
                  iframeName: 'iframeVue_report_'+templateObject["ID"],
                  iframeData: { src: '' },
                  scrollPosition: 0,
                  needsScrollRestore: false,
                  queryParams: null,
                  hasQueried: false
                }

                this.reportTabs.push(tabObject)


              }


            }
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
      //this.timGZLastDate=
    },
    //初始化数据频率的权限
    initDataFreq(fundCode){
      return new Promise((resolve, reject) => {
        const params = {
          fundCode:fundCode,
        }
        request({
          url: `/api/jxbg/getOrgFundDataFreqList`,
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
      //this.fundCode = arr[0].VC_FUNDCODE || ''
      this.formInline.fundCode = arr[0].VC_FUNDCODE || ''
      this.formInline.fundName = arr[0].VC_FUNDNAME || ''
      this.timDate = arr[0].D_CREATE_DATE || ''
      this.selectList = arr
      //估值最新确认日期
      this.initTimGzLastDate(arr[0].VC_FUNDCODE || '')
      this.initDataFreq(arr[0].VC_FUNDCODE || '')

      // 隐藏悬浮框
      this.floatSelectorVisible = false
    },


    onSubmit(formName) {
      var self = this
      self.$refs[formName].validate((valid) => {
        if (valid) {
          try {
            // 只更新当前激活的tab的iframe
            self.updateCurrentReportIframe();
          } catch (e) {
          }
          // 禁用搜索按钮
          self.$fun.searchButtonDisabled('issearchFxButton', self)
        } else {
          return false
        }
      })
    },

    // 更新当前激活的tab的iframe链接
    updateCurrentReportIframe() {
      const tab = this.currentTab;
      if (!tab) return;

      // 保存当前查询参数的副本
      const params = { ...this.formInline };

      //无基准
      if (this.formInline.ZB_INDEXTYPE == '0') {
        params.ZB_INDEXCODEA=''
        params.ZB_INDEXCODEB = ''
        params.ZB_INDEXWEIGHTA = ''
        params.ZB_INDEXWEIGHTB = ''
      }
      // 处理特殊参数
      if (this.formInline.ZB_INDEXTYPE == '1') {
        params.ZB_INDEXCODEB = '';
        params.ZB_INDEXWEIGHTA = '';
        params.ZB_INDEXWEIGHTB = '';
      }
      tab.queryParams = params;
      tab.hasQueried = true;

      // 更新iframe链接
      tab.iframeData.src = this.file_vmrisk_src_view(
        tab.templateCode,
        this.formInline.ddate_[0],
        this.formInline.ddate_[1],
        this.formInline.fundCode,
        this.formInline.ZB_INDEXTYPE,
        this.formInline.ZB_INDEXCODEA,
        this.formInline.ZB_INDEXCODEB,
        this.formInline.ZB_INDEXWEIGHTA,
        this.formInline.ZB_INDEXWEIGHTB,
        '',
        this.formInline.contrasCodes,
        this.formInline.industryType,
        this.formInline.factorType,
        this.formInline.desensitizationFlag,
        this.formInline.desensitizationFun,
        this.formInline.dataFreqOpen,
        this.formInline.dataFreq
      );

      // 更新按钮状态
      this.onButton = true;
      this.onSub = '查询中...';
      this.exportButton2 = true;
      this.exportIcon = 'el-icon-loading';
    },

    // 处理iframe加载完成
    handleIframeLoad(tabId) {
      // 只有当前激活的tab加载完成才更新按钮状态
      if (tabId === this.activeTab) {
        this.onButton = false;
        this.onSub = '查询';
        this.exportButton2 = false;
        this.exportIcon = 'el-icon-search';

      }
    },

    // 清除
    resetForm(formName) {
      var self = this
      self.$refs[formName].resetFields()
      this.floatSelectorVisible = false
      this.formInline.fundCode = ''
      this.formInline.fundName = ''
    },

    file_vmrisk_src_view(templateCode, beginDate, endDate, fundCode, benchmarks,benchmarkA, benchmarkB, benchmarkAValue, benchmarkBValue, kpiCode, contrasCode,industryType,factorType, desensitizationFlag, desensitizationFun,dataFreqOpen,dataFreq) {
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
        desensitizationFlag +
        '&desensitizationFun=' +
        desensitizationFun +
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

    // 导出当前选中Tab的PDF
    fun_export_PDF() {
      const tab = this.currentTab;
      if (!tab) {
        this.$message.warning('未找到当前报告信息');
        return;
      }

      // 检查是否已查询
      if (!tab.hasQueried || !tab.queryParams) {
        this.$message.warning('请先查询再进行导出');
        return;
      }

      const self = this;
      // 禁用按钮
      self.exportButton2 = true;
      self.exportIcon2 = 'el-icon-loading';
      self.exportText2 = '导出数据中...';

      // 使用该tab上次查询的参数
      const params = tab.queryParams;
      const pdfName = `${tab.name}.pdf`;
      const covIndexCode = '8cf9997c-e5c4-40e9-8d79-660e61d323ce';
      const pdfOption = { pagedir: 'h' }; // vm导出word说明文档中相反，h为纵向，v为横向，默认为横向

      fun.fun_exportPDFOption_GFJX_new(
        pdfName,
        JSON.stringify(pdfOption),
        tab.iframeId,
        tab.templateCode,
        params.fundCode,
        params.fundName,
        params.ddate_[0],
        params.ddate_[1],
        params.desensitizationFlag,
        params.desensitizationFun,
        params.dataFreqOpen,
        params.dataFreq,
        "",
        params.benchmarkA,
        params.benchmarkB,
        params.benchmarkAValue,
        params.benchmarkBValue,
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

// iframe容器样式 - 所有iframe都绝对定位重叠在一起
.iframe-container {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

// 单个iframe的包装器 - 保持重叠显示
.iframe-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  transition: z-index 0.3s ease, opacity 0.3s ease;
}

// 确保iframe占满容器
::v-deep .iframeModule {
  width: 100%;
  height: 100%;
  border: none;
}

::v-deep .standard-form .el-form-item {
  margin-bottom: 5px !important;
}

.report-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 0px;
}

.pill-item {
  padding: 6px 26px;
  border-radius: 2px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  background-color: #fcf8f4;
  border: 1px solid #e9c5a2;
  border-bottom: none;
  color: #612d10 !important;

  &.active {
    background-image: linear-gradient(to right, #f5d7bc, #e0b794) !important;
    color: #612d10 !important;
  }
}
</style>

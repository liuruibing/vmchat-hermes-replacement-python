<template>
  <div>
    <div class="toolbar standard-form" id="report-center-toolbar">
      <div class="canvas-area">
        <!-- <div class="canvas-config">
          <span>画布大小</span>
          <input v-model="canvasStyleData.width" />
          <span>*</span>
          <input v-model="canvasStyleData.height" />
        </div>
        <div class="canvas-config">
          <span>画布比例</span>
          <input v-model="scale" @input="handleScaleChange" /> %
        </div> -->
      </div>
      <div class="page-left-button">
        <el-button class="custom-button" size="small" type="primary" @click="handleClickHome">
          <svg-icon icon-class="template_return"></svg-icon>
          返 回
        </el-button>
        <el-button class="custom-button" size="small" type="primary" @click="dialogVisible = true">
          <svg-icon icon-class="template_set"></svg-icon>
          通用设置
        </el-button>
        <el-button class="custom-button" size="small" type="primary" @click="handleSelectFund">
          <svg-icon icon-class="template_product"></svg-icon>
          选择产品
        </el-button>
      </div>
      <div class="btn-area">
        <!-- <el-button icon="el-icon-s-platform" @click="preview(false)"
          >预览</el-button
        > -->
        <el-button class="custom-button" size="small" type="primary" @click="handleSaveTemplate">
          <svg-icon icon-class="template_save"></svg-icon>
          保 存
        </el-button>
        <el-button v-if="$store.state.isEditor == true" :disabled="isDisabledSaveAs" class="custom-button" size="small" type="primary" @click="handleSaveAs">
          <svg-icon icon-class="template_resave"></svg-icon>
          另 存
        </el-button>
        <!--        <el-button icon="el-icon-download" size="small" type="primary">下载WORD</el-button>-->
        <el-button class="custom-button" size="small" type="primary" plain @click="handleClickPDF">
          <svg-icon icon-class="template_download"></svg-icon>
          下载PDF
        </el-button>
        <!--        <el-button icon="el-icon-share" size="small" type="primary">分 享</el-button>-->
      </div>
    </div>
    <!-- 预览 -->
    <Preview v-if="isShowPreview" :is-screenshot="isScreenshot" @close="handlePreviewChange" />
    <!-- 通用设置 -->
    <div class="global">
      <el-dialog :close-on-click-modal="false" :visible.sync="dialogVisible" title="" width="50%" custom-class="dialog-single-product">
        <div slot="title">
          <span style="color: #333333 !important">通用设置</span>
        </div>
        <div style="background-color: #ffffff">
          <div v-for="item in globalConfigSelf" class="global-class">
            <div class="first-title">{{ item.name }}</div>
            <div v-for="sitem in item.children">
              <el-row>
                <el-col :span="2" class="second-title">
                  <span style="width: 50px; display: inline-block; text-align: right">{{ sitem.name }}</span>
                </el-col>
                <el-col :span="22">
                  <el-row>
                    <el-col v-for="(ssitem, index) in sitem.children" :key="index" :span="8" style="margin-bottom: 10px; height: 32px">
                      <span
                        v-if="ssitem.type == 'TP_COLORPICKER'"
                        style="width: 50px; font-size: 14px; text-align: right; display: inline-block; padding-right: 5px; position: relative; top: -8px"
                      >
                        {{ ssitem.name }}
                      </span>
                      <span v-else style="width: 50px; font-size: 14px; text-align: right; display: inline-block; padding-right: 5px">
                        {{ ssitem.name }}
                      </span>
                      <template v-if="ssitem.type == 'TP_SELECT' || ssitem.type == 'TP_SELECTIMPORT'">
                        <el-select v-model="globalConfigFormquery[ssitem.id]" popper-class="global-drop-down-bg" size="small">
                          <el-option v-for="temp in ssitem.data" :key="temp.val" :label="temp.name" :value="temp.val"></el-option>
                        </el-select>
                      </template>
                      <template v-else-if="ssitem.type == 'TP_TEXT'">
                        <el-input v-model="globalConfigFormquery[ssitem.id]" size="small"></el-input>
                      </template>
                      <template v-else-if="ssitem.type == 'TP_DATE'">
                        <el-date-picker
                          v-model="globalConfigFormquery[ssitem.id]"
                          placeholder="选择日期"
                          popper-class="global-drop-down-bg"
                          type="date"
                          value-format="yyyy-MM-dd"
                        ></el-date-picker>
                      </template>
                      <template v-else-if="ssitem.type == 'TP_COLORPICKER'">
                        <el-color-picker v-model="globalConfigFormquery[ssitem.id]" popper-class="global-drop-down-bg" size="small"></el-color-picker>
                      </template>
                      <template v-else-if="ssitem.type == 'TP_INPUTNUMBER'">
                        <el-input v-model.number="globalConfigFormquery[ssitem.id]" size="small"></el-input>
                      </template>
                    </el-col>
                  </el-row>
                </el-col>
              </el-row>
            </div>
          </div>
        </div>
        <template slot="footer">
          <div style="text-align: center" class="standard-form">
            <el-button
              size="small"
              type="primary"
              @click="
                () => {
                  dialogVisible = false
                }
              "
            >
              取 消
            </el-button>
            <el-button size="small" type="primary" @click="handleClickEnter">确 定</el-button>
          </div>
        </template>
      </el-dialog>
    </div>

    <!-- 产品选择 单产品-->
    <div class="select-fund standard-form">
      <!-- 产品选择   -->
      <el-dialog :close-on-click-modal="false" :visible.sync="selectProductDialogVisible" custom-class="dialog-single-product" title="" width="50%">
        <div slot="title">
          <span>选择产品</span>
        </div>
<!--        <div style="padding: 5px 0px 5px 0px" class="dialog-single-product-firstline">
          <span style="width: 60px; display: inline-block;">选择产品</span>
          <ProductSelectSearch
            v-model="singleCode"
            :forceFlag="'B'"
            :size="'small'"
            style="width: 180px; margin-right: 10px;"
            @select-product="handleProductSelect"
          />
        </div>-->
        <div style="padding: 5px 0px 5px 0px" class="dialog-single-product-firstline">
<!--          <span style="width: 60px; display: inline-block; margin-left: 5px">产品代码</span>-->
<!--          <el-input
            v-model="selectProductTableData[0].fundCode"
            clearable
            placeholder="请选择产品"
            size="small"
            @click.native="handleSelectProductTypeClick(selectProductTableData[0])"
          ></el-input>-->
          <span style="width: 60px; display: inline-block">产品名称</span>
          <ProductSelectInput
            v-model="product"
            placeholder="请选择产品"
            :input-width="'260px'"
            @select="handleProductSelect"
            @clear="handleProductClear"
          />
<!--          <el-input v-model="selectProductTableData[0].fundCode" :disabled="true" clearable size="small"></el-input>-->
          <span style="width: 60px; display: inline-block">产品代码</span>
          <el-input v-model="selectProductTableData[0].fundCode" :disabled="true" clearable size="small"></el-input>
          <span style="width: 60px; display: inline-block">产品类型</span>
          <el-select v-model="selectProductTableData[0].source" :disabled="true" clearable size="small" placeholder="">
            <el-option v-for="item in sourctOptions" :key="item.id" :label="item.label" :value="item.id"></el-option>
          </el-select>
        </div>
        <div class="mt10" style="margin-bottom: 10px; padding: 5px">
          <div class="mt10">
            <span style="width: 60px; display: inline-block">基准类型</span>
            <el-select v-model="productForm.ZB_INDEXTYPE" clearable placeholder="请选择" size="small">
              <el-option v-for="item in ZB_INDEXTYPEOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
            </el-select>
          </div>
          <div v-show="productForm.ZB_INDEXTYPE == 'gdjz'" class="mt10">
            <span style="width: 60px; display: inline-block">选择基准</span>
            <el-select v-model="productForm.ZB_INDEXCODE" clearable placeholder="请选择" size="small">
              <el-option v-for="item in $store.state.indexArray" :key="item.id" :label="item.label + '(' + item.id + ')'" :value="item.id"></el-option>
            </el-select>
          </div>
          <div v-show="productForm.ZB_INDEXTYPE == 'zdyjz'" class="mt10">
            <span style="width: 60px; display: inline-block">基准 A</span>
            <el-select v-model="productForm.ZB_INDEXCODEA" clearable placeholder="请选择" size="small">
              <el-option v-for="item in $store.state.compareIndexArray" :key="item.id" :label="item.label + '(' + item.id + ')'" :value="item.id"></el-option>
            </el-select>
            <span style="width: 60px; display: inline-block; margin-left: 10px">权重 A</span>
            <el-input v-model="productForm.ZB_INDEXWEIGHTA" size="small" @blur="handleInputWeight('A')"></el-input>
            %
          </div>
          <div v-show="productForm.ZB_INDEXTYPE == 'zdyjz'" class="mt10">
            <span style="width: 60px; display: inline-block">基准 B</span>
            <el-select v-model="productForm.ZB_INDEXCODEB" clearable placeholder="请选择" size="small">
              <el-option v-for="item in $store.state.compareIndexArray" :key="item.id" :label="item.label + '(' + item.id + ')'" :value="item.id"></el-option>
            </el-select>
            <span style="width: 60px; display: inline-block; margin-left: 10px">权重 B</span>
            <el-input v-model="productForm.ZB_INDEXWEIGHTB" size="small" @blur="handleInputWeight('B')"></el-input>
            %
          </div>
          <div class="mt10">
            选择时间
            <el-date-picker
              unlink-panels
              v-model="productForm.date"
              :disabled="productForm.timeType != 'self'"
              end-placeholder="结束日期"
              popper-class="popperDateShortTP"
              range-separator="至"
              size="small"
              start-placeholder="开始日期"
              type="daterange"
              value-format="yyyy-MM-dd"
              :picker-options="fundRangeDatePickerOptions()"
            ></el-date-picker>
          </div>
          <div style="margin-left: 60px; margin-top: 10px">
            <el-radio-group v-model="productForm.timeType" @input="handleBasicTemplateTimeTypeClick">
              <el-radio label="self">自定义</el-radio>
              <el-radio label="m1">近一月</el-radio>
              <el-radio label="m3">近三月</el-radio>
              <el-radio label="m6">近六月</el-radio>
              <el-radio label="y1">近一年</el-radio>
              <el-radio label="yd">今年以来</el-radio>
              <el-radio v-if="productForm.fundType == '1'" label="cd">成立以来</el-radio>
            </el-radio-group>
          </div>
        </div>
        <template slot="footer">
          <div style="text-align: center" class="standard-form">
            <el-button
              size="small"
              type="primary"
              @click="
                () => {
                  selectProductDialogVisible = false
                }
              "
            >
              取 消
            </el-button>
            <el-button size="small" type="primary" @click="saveNewFundInfo">确 定</el-button>
          </div>
        </template>
      </el-dialog>
    </div>
    <!-- 另存为 -->
    <div class="global save-as">
      <el-dialog :close-on-click-modal="false" :visible.sync="saveAsDialogVisible" title="" width="30% !important" custom-class="dialog-single-product">
        <div slot="title">
          <span style="color: #ffffff !important">模板信息</span>
        </div>
        <el-form ref="saveAsDialogVisible" :model="saveAsDialogFormQuery" :rules="saveAsDialogFormRules" class="basic-template-dialog" label-width="120px">
          <el-form-item label="模板名称" prop="templateName">
            <el-input v-model="saveAsDialogFormQuery.templateName" size="small" style="width: 100% !important"></el-input>
          </el-form-item>
          <el-form-item label="模板描述" prop="describe">
            <el-input v-model="saveAsDialogFormQuery.describe" :rows="4" placeholder="请输入内容" size="small" type="textarea" style="width: 100% !important"></el-input>
          </el-form-item>
        </el-form>
        <template slot="footer">
          <div style="text-align: center">
            <div class="standard-form">
              <el-button
                size="small"
                type="primary"
                @click="
                  () => {
                    saveAsDialogVisible = false
                  }
                "
              >
                取 消
              </el-button>
              <el-button size="small" type="primary" @click="saveAsNewTemplate">确 定</el-button>
            </div>
          </div>
        </template>
      </el-dialog>
    </div>
    <!-- 产品选择弹窗 -->
    <product-selector
      :dialog-visible="productSelectorVisible"
      :select-list="selectList"
      :show-tree-key-array="showTreeKeyArray"
      :tree-data="treeData"
      default-checked-keys="zstgwb"
      @closedialog="handleDialogClosed"
      @submitdialog="handleSubmitClick"
    ></product-selector>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import productSelector from '@/components/productSelectorHome'
import changeComponentsSizeWithScale from '@/utils/changeComponentsSizeWithScale'
import Preview from '@/components/Editor/Preview'
import pageApi from '@/api/templateManageMent'
import commonFun from '@/filters/new_common.js'
import commonOldFun from '@/filters/common.js'
import Vue from 'vue'
import $ from 'jquery'
import { renderScript } from '@/utils/reportComponent.js'
import moment from 'moment/moment'
import request from '@/utils/request'
import ProductSelectSearch from '@/components/productSelector/ProductSelectSearch.vue'
import ProductSelectInput from '@/components/productSelector/ProductSelectInput'
export default {
  components: { Preview, productSelector,ProductSelectSearch,ProductSelectInput },
  filters: {
    reportTypeToStr(value) {
      if (value == '1') {
        return '默认模板'
      } else {
        return '自定义模板'
      }
    },
    sourceToStr(value) {
      if (value == 'IN') {
        return '托管/外包'
      } else if (value == 'OUT') {
        return '私募排排'
      } else {
        return '-'
      }
    }
  },
  props: {
    globalConfig: {
      type: Array,
      required: true,
      default: () => {
        return []
      }
    },
    currentTemplate: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {

      product: null,
      singleCode:'',
      selectProductDialogRowPointer: null, // 选择产品弹窗对应的行对象
      productSelectorVisible: false,
      selectList: [],
      sourctOptions: [
        {
          label: '托管/外包',
          id: 'IN'
        },
        {
          label: '私募排排',
          id: 'OUT'
        }
      ],
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
      saveAsDialogFormQuery: {
        templateName: '',
        describe: ''
      },
      saveAsDialogFormRules: {
        templateName: [
          {
            required: true,
            message: '模板名称不能为空',
            trigger: 'blur'
          }
        ]
      },
      isSaveAs: false,
      isDisabledSaveAs: false,
      selectProductDialogVisible: false,
      saveAsDialogVisible: false, // 另存为模板变量
      dialogVisible: false,
      globalConfigFormquery: {}, // 全局的通用属性配置
      ZB_INDEXTYPEOption: [
        {
          id: 'gdjz',
          label: '固定基准'
        },
        {
          id: 'zdyjz',
          label: '自定义基准'
        }
      ],
      globalConfigSelf: [],
      timer: null,
      scale: 100,
      isShowPreview: false,
      isScreenshot: false,
      productForm: {
        fundName: '',
        fundCode: '',
        date: [],
        fundType: '',
        timeType: 'self',
        reportType: '',
        ZB_INDEXCODE: '', // 基准编码
        ZB_INDEXTYPE: 'gdjz', // 基准类型
        ZB_INDEXCODEA: '', // 基准A
        ZB_INDEXWEIGHTA: '0', // 基准A权重
        ZB_INDEXCODEB: '', // 基准B
        ZB_INDEXWEIGHTB: '0', // 基准B权重
        source: ''
      },
      selectProductTableData: [
        {
          fundCode: '',
          fundName: '',
          source: '',
          gzLastDate:'', //产品最新的估值确认日期
        }
      ],
      //成立日
      timDate: '',
      //最新估值确认日
      dateTime:'',
      datumOption: this.$store.state.indexArray,
      filterRules: {
        type1: /^\d+$/,
        type2: /^[\u4e00-\u9fa5\w\-]+$/,
        type3: /^\d+$/,
        type4: /^[\u4e00-\u9fa5%￥]+$/,
        type5: /^[\u4E00-\u9FA5()%\-\_\/"“”'‘’]+$/u
      },
      filterMessage: {
        type1: '请输入纯数字',
        type2: '请输入汉字,字母，数字，下划线，-',
        type3: '请输入纯数字或者自适应',
        type4: '请输入纯汉字可以包含%、￥',
        type5: '请输入纯汉字，可以包含' + '（' + '）' + '%' + '——' + '_' + '/' + '""' + "''"
      }
    }
  },
  computed: {
    ...mapState(['canvasStyleData'])
  },
  watch: {
    singleCode(newVal) {
      this.selectProductTableData[0].fundCode = newVal;
    },
    'selectProductTableData[0].fundCode'(newVal) {
      this.singleCode = newVal;
    },
    globalConfig: {
      handler() {
        const treeData = commonFun.converTreeData(this.globalConfig, 0, '', '', 'id', 'leftTree')
        this.globalConfigSelf = treeData.data || []

        // 拿到所有的order为 3 的变量组装成一个公共属性params  -- TODO 判断是 编辑模式，还是新增模式
        this.globalConfigFormquery = {}
        this.globalConfig.forEach((item) => {
          if (item.level === 3) {
            this.$set(this.globalConfigFormquery, item.id, item.default)
          }
        })
      },
      deep: true
    },
    globalConfigFormquery: {
      handler(val) {
        this.$store.commit('SET_GLOBAL_CONFIG', val)
      },
      deep: true
    },
    productForm: {
      handler(val) {
        console.log('productForm', val)
        const obj = {
          ZB_BEGINDATE: val.date[0],
          ZB_ENDDATE: val.date[1],
          ZB_FUNDCODE: val.fundCode,
          ZB_FUNDNAME: val.fundName,
          timeType: val.timeType,
          ZB_INDEXCODE: val.ZB_INDEXCODE,
          ZB_INDEXTYPE: val.ZB_INDEXTYPE,
          ZB_INDEXCODEA: val.ZB_INDEXCODEA,
          ZB_INDEXWEIGHTA: val.ZB_INDEXWEIGHTA,
          ZB_INDEXCODEB: val.ZB_INDEXCODEB,
          ZB_INDEXWEIGHTB: val.ZB_INDEXWEIGHTB,
          source: val.source,
          selectProductTableData: val.selectProductTableData
        }
        this.$store.commit('SET_GLOBAL_CONFIG', obj)
      },
      deep: true
    },
    currentTemplate: {
      handler(val) {
        const { ZB_FUNDCODE, ZB_FUNDNAME, ZB_BEGINDATE, ZB_ENDDATE, timeType, ZB_INDEXCODE, source, selectProductTableData, fundType, reportType } = val
        this.productForm.selectProductTableData = selectProductTableData
        this.productForm.fundCode = ZB_FUNDCODE
        this.productForm.fundName = ZB_FUNDNAME
        this.productForm.date = [ZB_BEGINDATE, ZB_ENDDATE]
        this.productForm.timeType = timeType
        this.productForm.ZB_INDEXCODE = ZB_INDEXCODE
        this.productForm.ZB_INDEXTYPE = val.ZB_INDEXTYPE
        this.productForm.ZB_INDEXCODEA = val.ZB_INDEXCODEA
        this.productForm.ZB_INDEXWEIGHTA = val.ZB_INDEXWEIGHTA
        this.productForm.ZB_INDEXCODEB = val.ZB_INDEXCODEB
        this.productForm.ZB_INDEXWEIGHTB = val.ZB_INDEXWEIGHTB
        this.singleCode = val.ZB_FUNDCODE || '';
        this.productForm.source = source
        this.productForm.fundType = fundType || '1'
        this.selectProductTableData = []
        this.productForm.reportType = reportType
        // 直接 那传过来的selectList 赋值
        for (let i = 0; i < selectProductTableData.length; i++) {
          const temp = selectProductTableData[i]
          // 响应式动态绑定变量
          this.$set(this.selectProductTableData, i, temp)
        }
      },
      deep: true
    }
  },
  created() {
    this.scale = this.canvasStyleData.scale
    this.singleCode = this.selectProductTableData[0].fundCode || ''
  },
  mounted() {
    this.timDate=this.selectProductTableData[0].createDate
    this.dateTime=this.selectProductTableData[0].gzLastDate
  },
  methods: {
    handleProductSelect(selectedProduct) {
        this.selectProductTableData[0] = {
          ...this.selectProductTableData[0],
          fundCode: selectedProduct.VC_FUNDCODE,
          fundName: selectedProduct.VC_FUNDNAME,
          source: selectedProduct.VC_FLAG,
          createDate: selectedProduct.D_CREATE_DATE,
          gzLastDate: ''
        };


        this.singleCode = selectedProduct.VC_FUNDCODE;

        this.productForm = {
          ...this.productForm,
          fundCode: selectedProduct.VC_FUNDCODE,
          fundName: selectedProduct.VC_FUNDNAME,
          source: selectedProduct.VC_FLAG,
          fundType: selectedProduct.fundType || '1'
        };


        this.initTimGzLastDate(selectedProduct.VC_FUNDCODE);

    },
    handleProductClear: function() {
      console.log('清除产品选择')
    // 清空选择
    this.selectProductTableData[0] = {
      fundCode: '',
      fundName: '',
      source: '',
      createDate: '',
      gzLastDate: ''
    };
    this.singleCode = '';
    this.productForm.fundCode = '';
    this.productForm.fundName = '';
    this.productForm.source = '';
    },

    getDateRange(date) {
      const currentDate = new Date(date)
      const currentYear = currentDate.getFullYear()
      const currentMonth = currentDate.getMonth() + 1

      // 计算上个月的年份和月份
      const previousMonthYear = currentMonth === 1 ? currentYear - 1 : currentYear
      const previousMonthMonth = currentMonth === 1 ? 12 : currentMonth - 1

      // 判断上个月是否是闰月
      const isLeapMonth = previousMonthMonth === 2 && ((previousMonthYear % 4 === 0 && previousMonthYear % 100 !== 0) || previousMonthYear % 400 === 0)

      // 获取上个月月初的日期
      const firstDayOfPreviousMonth = `${previousMonthYear}-01-01`

      // 获取上个月月末的日期
      let lastDayOfPreviousMonth
      if (isLeapMonth) {
        lastDayOfPreviousMonth = `${previousMonthYear}-02-29`
      } else {
        const monthsWith31Days = [1, 3, 5, 7, 8, 10, 12]
        const monthsWith30Days = [4, 6, 9, 11]

        if (monthsWith31Days.includes(previousMonthMonth)) {
          lastDayOfPreviousMonth = `${previousMonthYear}-${String(previousMonthMonth).padStart(2, '0')}-31`
        } else if (monthsWith30Days.includes(previousMonthMonth)) {
          lastDayOfPreviousMonth = `${previousMonthYear}-${String(previousMonthMonth).padStart(2, '0')}-30`
        } else {
          lastDayOfPreviousMonth = `${previousMonthYear}-${String(previousMonthMonth).padStart(2, '0')}-28`
        }
      }

      return {
        startDate: firstDayOfPreviousMonth,
        endDate: lastDayOfPreviousMonth
      }
    },
    getPreviousNMonthsRange(date, n) {
      const currentDate = new Date(date)
      const currentYear = currentDate.getFullYear()
      const currentMonth = currentDate.getMonth() + 1

      let previousMonthYear = currentYear
      let previousMonthMonth = currentMonth - n

      // 向前计算年份和月份，确保目标月份在 1-12 的范围内
      while (previousMonthMonth <= 0) {
        previousMonthYear--
        previousMonthMonth += 12
      }

      // 获取前 n 个月的月初和月末日期
      const startDate = new Date(previousMonthYear, previousMonthMonth - 1, 1)
      const endDate = new Date(currentYear, currentMonth - 1, 0)

      const startDay = startDate.getDate()
      const endDay = endDate.getDate()

      const startMonth = startDate.getMonth() + 1
      const endMonth = endDate.getMonth() + 1

      const startYear = startDate.getFullYear()
      const endYear = endDate.getFullYear()

      // 考虑闰年和大小月份的情况
      const isStartLeapYear = (startYear % 4 === 0 && startYear % 100 !== 0) || startYear % 400 === 0
      const isEndLeapYear = (endYear % 4 === 0 && endYear % 100 !== 0) || endYear % 400 === 0

      let startDayOfMonth
      let endDayOfMonth

      if (startMonth === 2 && isStartLeapYear) {
        startDayOfMonth = Math.min(startDay, 29)
      } else if (startMonth === 2) {
        startDayOfMonth = Math.min(startDay, 28)
      } else if ([4, 6, 9, 11].includes(startMonth)) {
        startDayOfMonth = Math.min(startDay, 30)
      } else {
        startDayOfMonth = Math.min(startDay, 31)
      }

      if (endMonth === 2 && isEndLeapYear) {
        endDayOfMonth = Math.min(endDay, 29)
      } else if (endMonth === 2) {
        endDayOfMonth = Math.min(endDay, 28)
      } else if ([4, 6, 9, 11].includes(endMonth)) {
        endDayOfMonth = Math.min(endDay, 30)
      } else {
        endDayOfMonth = Math.min(endDay, 31)
      }

      const firstDayOfPreviousMonth = `${startYear}-${startMonth < 10 ? '0' + startMonth : startMonth}-${startDayOfMonth < 10 ? '0' + startDayOfMonth : startDayOfMonth}`
      const lastDayOfPreviousMonth = `${endYear}-${endMonth < 10 ? '0' + endMonth : endMonth}-${endDayOfMonth < 10 ? '0' + endDayOfMonth : endDayOfMonth}`

      return {
        startDate: firstDayOfPreviousMonth,
        endDate: lastDayOfPreviousMonth
      }
    },
    // 权重校验
    handleInputWeight(type) {
      const regex = /^(0(\.\d+)?|[1-9]\d*(\.\d+)?)$/
      if (type == 'A') {
        if (!regex.test(this.productForm.ZB_INDEXWEIGHTA)) {
          this.$message.closeAll()
          this.$message.warning('只能输入大于等于0的数')
          this.productForm.ZB_INDEXWEIGHTA = '0'
          return
        }
        if (this.productForm.ZB_INDEXWEIGHTB != '') {
          if (Number(this.productForm.ZB_INDEXWEIGHTA) + Number(this.productForm.ZB_INDEXWEIGHTB) > 100) {
            this.$message.closeAll()
            this.$message.warning('基金A、B权重不能超过100%')
            this.productForm.ZB_INDEXWEIGHTA = '0'
            return
          } else {
            this.productForm.ZB_INDEXWEIGHTA = '' + Number(this.productForm.ZB_INDEXWEIGHTA).toFixed(4)
          }
        }
      } else {
        if (!regex.test(this.productForm.ZB_INDEXWEIGHTB)) {
          this.$message.closeAll()
          this.$message.warning('只能输入大于等于0的数')
          this.productForm.ZB_INDEXWEIGHTB = '0'
          return
        }
        if (this.productForm.ZB_INDEXWEIGHTA != '') {
          if (Number(this.productForm.ZB_INDEXWEIGHTA) + Number(this.productForm.ZB_INDEXWEIGHTB) > 100) {
            this.$message.closeAll()
            this.$message.warning('基金A、B权重不能超过100')
            this.productForm.ZB_INDEXWEIGHTB = '0'
            return
          } else {
            this.productForm.ZB_INDEXWEIGHTB = '' + Number(this.productForm.ZB_INDEXWEIGHTB).toFixed(4)
          }
        }
      }
    },
    handleDialogClosed() {
      this.productSelectorVisible = false
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
              this.selectProductTableData[0].gzLastDate=res.data.data[0].endTime
              this.dateTime=res.data.data[0].endTime
            }
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
    },
    handleSubmitClick(arr) {
      this.productSelectorVisible = false
      this.selectList = arr
      if (this.selectList.length) {
        const index = this.selectProductTableData.findIndex((item) => item._XID == this.selectProductDialogRowPointer._XID)
        if (index !== -1) {
          this.$set(this.selectProductTableData, index, {
            fundCode: this.selectList[0].VC_FUNDCODE,
            fundName: this.selectList[0].VC_FUNDNAME,
            source: this.selectList[0].VC_FLAG,
            createDate: this.selectList[0].D_CREATE_DATE
          })
          this.timDate=this.selectList[0].D_CREATE_DATE
        }
        //估值最新确认日期
        this.initTimGzLastDate(this.selectList[0].VC_FUNDCODE || '')
      } else {
        const index = this.selectProductTableData.findIndex((item) => item._XID == this.selectProductDialogRowPointer._XID)
        if (index !== -1) {
          this.$set(this.selectProductTableData, index, {
            fundCode: '',
            fundName: '',
            source: '',
            createDate: '',
            gzLastDate:'',
          })
        }
      }
    },
    // 打开产品选择 弹窗
    handleSelectProductTypeClick(row) {
      this.selectProductDialogRowPointer = row
      if (row.fundCode && row.fundName && row.createDate) {
        this.selectList = [
          {
            VC_FUNDCODE: row.fundCode,
            VC_FUNDNAME: row.fundName,
            D_CREATE_DATE: row.createDate
          }
        ]
      } else {
        this.selectList = []
      }
      this.productSelectorVisible = true
    },

    // 另存为新的模板
    saveAsNewTemplate() {
      if (!this.validateAllPage()) {
        this.$message.closeAll()
        this.$message.warning('校验失败')
        return
      }

      this.$refs.saveAsDialogVisible.validate((valid) => {
        if (valid) {
          this.saveAsDialogVisible = false
          // 保存当前模板
          this.$store.commit('saveComponentDataArrayByIndex')
          const componentData = this.$store.state.componentDataArray
          const canvasGlobalConfig = {
            ...this.$store.state.canvasGlobalConfig,
            pageMarginsOption: this.$store.state.pageMarginsOption
          }
          const params = {
            reportName: this.saveAsDialogFormQuery.templateName,
            fundType: this.productForm.fundType || '1',
            reportHtml: commonOldFun.encryptByAESCommon(document.getElementById('templateEditor').outerHTML),
            reportDesc: this.saveAsDialogFormQuery.describe,
            moduleCfg: commonOldFun.encryptByAESCommon(JSON.stringify(componentData)),
            elementCfg: JSON.stringify(canvasGlobalConfig)
          }
          const moduleCfgRel = []
          this.$bus.$emit('homeload', true)
          this.$store.state.componentDataArray.forEach((item) => {
            const obj = item.map((stem) => {
              return {
                moduleId: stem.info.id,
                vueId: stem.id,
                elementCfg: stem.info.params
              }
            })
            moduleCfgRel.push(obj)
          })

          params.moduleCfgRel = JSON.stringify(moduleCfgRel)
          this.isSaveAs = true
          this.isDisabledSaveAs = true
          pageApi.saveAsReport(params).then((res) => {
            if (res.data.status === 200) {
              this.$message.success(res.data.message || '保存成功')
              this.isSaveAs = false
              this.isDisabledSaveAs = false
            } else {
              this.$message.error(res.data.message || '保存失败')
              this.isSaveAs = false
              this.isDisabledSaveAs = false
            }
            this.$bus.$emit('homeload', false)
          })
        } else {
          this.$message.closeAll()
          this.$message.warning('请根据提示修改')
          this.$bus.$emit('homeload', false)
        }
      })
    },
    // 导出PDF文件
    async handleClickPDF() {
      if (!this.validateAllPage()) {
        this.$message.closeAll()
        this.$message.warning('校验失败')
        return
      }

      // 保存当前页面的所有内容
      this.$store.commit('saveComponentDataArrayByIndex')

      // 获取所有的html结构
      const currentIndex = this.$store.state.componentDataIndex
      const html = []
      for (let i = 0; i < this.$store.state.componentDataArray.length; i++) {
        const returnStr = await this.handleGetHtml(i, html)
        console.log(returnStr)
      }
      this.$store.commit('setComponentDataIndex', currentIndex)
      this.$store.dispatch('refreshMap')

      const params = {}
      // params.pagesHtml = html
      params.pagesHtmlJson = commonOldFun.encryptByAESCommon(JSON.stringify(html))
      params.reportName = this.currentTemplate.reportName || '报告模板'
      this.$bus.$emit('homeload', true)
      const fileName = params.reportName + '_' + this.$store.state.canvasGlobalConfig.ZB_FUNDNAME + '.pdf'
      pageApi
        .exportPDF(params)
        .then((res) => {
          if (res.data instanceof Blob) {
            const fileString = res.headers['content-disposition']
            const blob = new Blob([res.data], { type: 'charset=utf-8' })
            const fileUrl = window.URL.createObjectURL(blob)
            const link = document.createElement('a')
            link.href = fileUrl
            link.download = fileName
            document.body.appendChild(link)
            link.click()
            document.body.removeChild(link)
          } else {
          }
          this.$bus.$emit('homeload', false)
        })
        .catch((err) => {
          this.$bus.$emit('homeload', false)
        })
    },
    handleGetHtml(i, html) {
      return new Promise((resolve, reject) => {
        this.$store.commit('setComponentDataIndex', i)
        this.$store.dispatch('refreshMap')
        setTimeout(() => {
          const htmlText = this.exportHtmlStr()
          html.push(htmlText)
          resolve(htmlText)
        }, 300)
      })
    },

    exportHtmlStr() {
      const style = $('<style>').html(`
  *, :after, :before {
    -webkit-box-sizing: inherit !important;
    box-sizing: inherit !important;
  }
  #templateEditor {
    margin-top: 0px !important;
  }
  .el-divider--horizontal {
    display: block;
    height: 1px;
    width: 100%;
    margin: 24px 0;
  }
  .editor-divider {
    position: relative;
    top: 60px;
    width: calc(100% - 40px);
    margin-left: 20px;
    margin-right: 20px;
  }
  .el-divider {
    background-color: #DCDFE6;
    position: relative;
  }
`)
      const htmlSelf = $('<html>')
      const bodySelf = $('<body>')
      const headSelf = $('<head>')
      const headContent = $('head').clone()
      headContent.find('script').remove()
      const bodyContent = $('#templateEditor').clone()
      bodyContent.find('script').remove()

      headSelf.append(headContent)
      headSelf.append(style)
      bodySelf.append(bodyContent)
      htmlSelf.append(headSelf)
      htmlSelf.append(bodySelf)
      return htmlSelf.prop('outerHTML')
    },

    // 新建模板下的保存
    saveAsByEditor() {
      if (!this.validateAllPage()) {
        this.$message.closeAll()
        this.$message.warning('校验失败')
        return
      }

      this.$bus.$emit('homeload', true)
      // 保存当前模板
      this.$store.commit('saveComponentDataArrayByIndex')
      const componentData = this.$store.state.componentDataArray
      const canvasGlobalConfig = {
        ...this.$store.state.canvasGlobalConfig,
        pageMarginsOption: this.$store.state.pageMarginsOption
      }
      const params = {
        reportName: this.currentTemplate.reportName,
        fundType: this.currentTemplate.fundType,
        reportHtml: commonOldFun.encryptByAESCommon(document.getElementById('templateEditor').outerHTML),
        reportDesc: this.currentTemplate.reportDesc,
        moduleCfg: commonOldFun.encryptByAESCommon(JSON.stringify(componentData)),
        elementCfg: JSON.stringify(canvasGlobalConfig)
      }
      const moduleCfgRel = []
      this.$store.state.componentDataArray.forEach((item) => {
        const obj = item.map((stem) => {
          return {
            moduleId: stem.info.id,
            vueId: stem.id,
            elementCfg: stem.info.params
          }
        })
        moduleCfgRel.push(obj)
      })

      params.moduleCfgRel = JSON.stringify(moduleCfgRel)
      this.isSaveAs = true
      this.isDisabledSaveAs = true
      pageApi
        .saveAsReport(params)
        .then((res) => {
          if (res.data.status === 200) {
            this.currentTemplate.reportId = res.data.data
            this.$message.success(res.data.message || '保存成功')
            this.isSaveAs = false
            this.isDisabledSaveAs = false
          } else {
            this.currentTemplate.reportId = ''
            this.$message.error(res.data.message || '保存失败')
            this.isSaveAs = false
            this.isDisabledSaveAs = false
          }
          this.$bus.$emit('homeload', false)
        })
        .catch((err) => {
          this.isSaveAs = false
          this.isDisabledSaveAs = false
          this.currentTemplate.reportId = ''
          this.$bus.$emit('homeload', false)
        })
    },

    /**
     * @description 选择产品弹窗
     */
    handleSelectFund() {
      this.selectProductDialogVisible = true
    },
    /**
     * @description 选择产品弹窗修改确定
     */
    saveNewFundInfo() {
      const templateObj = {
        ZB_FUNDNAME: this.selectProductTableData.map((item) => item.fundName).toString(),
        ZB_FUNDCODE: this.selectProductTableData.map((item) => item.fundCode).toString(),
        timeType: this.productForm.timeType,
        ZB_INDEXCODE: this.productForm.ZB_INDEXCODE,
        ZB_INDEXTYPE: this.productForm.ZB_INDEXTYPE,
        ZB_INDEXCODEA: this.productForm.ZB_INDEXCODEA,
        ZB_INDEXWEIGHTA: this.productForm.ZB_INDEXWEIGHTA,
        ZB_INDEXCODEB: this.productForm.ZB_INDEXCODEB,
        ZB_INDEXWEIGHTB: this.productForm.ZB_INDEXWEIGHTB,
        ZB_BEGINDATE: this.productForm.date[0],
        ZB_ENDDATE: this.productForm.date[1],
        selectList: this.selectList,
        selectProductTableData: this.selectProductTableData
      }

      // 赋值给 全局对象
      this.$store.commit('SET_GLOBAL_CONFIG', templateObj)
      if (!this.validateAllPage()) {
        this.$message.closeAll()
        this.$message.warning('校验失败')
        return
      }
      for (let i = 0; i < this.$store.state.componentDataArray.length; i++) {
        const tempComponentData = this.$store.state.componentDataArray[i]
        for (let j = 0; j < tempComponentData.length; j++) {
          const temp = tempComponentData[j]
          temp.info.params.ZB_BEGINDATE = templateObj.ZB_BEGINDATE
          temp.info.params.ZB_ENDDATE = templateObj.ZB_ENDDATE
          temp.info.params.ZB_FUNDCODE = templateObj.ZB_FUNDCODE
          temp.info.params.ZB_INDEXCODE = templateObj.ZB_INDEXCODE
          temp.info.params.ZB_INDEXTYPE = templateObj.ZB_INDEXTYPE
          temp.info.params.ZB_INDEXCODEA = templateObj.ZB_INDEXCODEA
          temp.info.params.ZB_INDEXWEIGHTA = templateObj.ZB_INDEXWEIGHTA
          temp.info.params.ZB_INDEXCODEB = templateObj.ZB_INDEXCODEB
          temp.info.params.ZB_INDEXWEIGHTB = templateObj.ZB_INDEXWEIGHTB
          const params = { ...temp.info.params, ...templateObj }
          params.moduleId = temp.info.id
          // TODO 渲染不同的页面
          if (i == this.$store.state.componentDataIndex) {
            this.renderDiv(temp, params)
          } else {
            this.renderReplaceScript(temp, params)
          }
        }
      }
      this.selectProductDialogVisible = false
    },
    // 触发时间选择 点击事件
    handleBasicTemplateTimeTypeClick() {
      // 如果选择了成立时间，需要判断用户是否点击了
      if (this.productForm.timeType == 'cd') {
        if (
          this.selectProductTableData.length == 0 ||
          this.selectProductTableData[0].createDate == '' ||
          this.selectProductTableData[0].createDate == undefined ||
          this.selectProductTableData[0].createDate == null
        ) {
          this.$message.closeAll()
          this.$message.warning('产品不能为空')
          this.productForm.timeType = 'self'
          return
        } else {
          let end = moment().subtract(1, 'days').format('YYYY-MM-DD')
          end = this.selectProductTableData[0].gzLastDate!=''?moment(this.selectProductTableData[0].gzLastDate).format('YYYY-MM-DD'):end
          this.productForm.date = [this.selectProductTableData[0].createDate,end]
        }
      } else {
        if (this.productForm.timeType == 'm1') {
          let end = moment().subtract(1, 'days').format('YYYY-MM-DD')
          end = this.selectProductTableData[0].gzLastDate!=''?moment(this.selectProductTableData[0].gzLastDate).format('YYYY-MM-DD'):end
          let start = moment(moment(end).subtract(1, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
          let createTime="";
          if(this.selectProductTableData[0].createDate!="") {
            createTime = moment(this.selectProductTableData[0].createDate).format('YYYY-MM-DD')
            this.productForm.date = [moment(start).isAfter(createTime)===true?start:createTime, end]
          }else{
            this.productForm.date = [start, end]
          }
        } else if (this.productForm.timeType == 'm3') {
          let end = moment().subtract(1, 'days').format('YYYY-MM-DD')
          end = this.selectProductTableData[0].gzLastDate!=''?moment(this.selectProductTableData[0].gzLastDate).format('YYYY-MM-DD'):end
          let start = moment(moment(end).subtract(3, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
          let createTime="";
          if(this.selectProductTableData[0].createDate!="") {
            createTime = moment(this.selectProductTableData[0].createDate).format('YYYY-MM-DD')
            this.productForm.date = [moment(start).isAfter(createTime)===true?start:createTime, end]
          }else{
            this.productForm.date = [start, end]
          }
        } else if (this.productForm.timeType == 'm6') {
          let end = moment().subtract(1, 'days').format('YYYY-MM-DD')
          end = this.selectProductTableData[0].gzLastDate!=''?moment(this.selectProductTableData[0].gzLastDate).format('YYYY-MM-DD'):end
          let start = moment(moment(end).subtract(6, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
          let createTime="";
          if(this.selectProductTableData[0].createDate!="") {
            createTime = moment(this.selectProductTableData[0].createDate).format('YYYY-MM-DD')
            this.productForm.date = [moment(start).isAfter(createTime)===true?start:createTime, end]
          }else{
            this.productForm.date = [start, end]
          }
        } else if (this.productForm.timeType == 'y1') {
          let end = moment().subtract(1, 'days').format('YYYY-MM-DD')
          end = this.selectProductTableData[0].gzLastDate!=''?moment(this.selectProductTableData[0].gzLastDate).format('YYYY-MM-DD'):end
          let start = moment(moment(end).subtract(1, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
          let createTime="";
          if(this.selectProductTableData[0].createDate!="") {
            createTime = moment(this.selectProductTableData[0].createDate).format('YYYY-MM-DD')
            this.productForm.date = [moment(start).isAfter(createTime)===true?start:createTime, end]
          }else{
            this.productForm.date = [start, end]
          }
        } else if (this.productForm.timeType == 'yd') {
          let end = moment().subtract(1, 'days').format('YYYY-MM-DD')
          end = this.selectProductTableData[0].gzLastDate!=''?moment(this.selectProductTableData[0].gzLastDate).format('YYYY-MM-DD'):end
          let start = moment(end).year() + '-01-01'
          let createTime="";
          if(this.selectProductTableData[0].createDate!="") {
            createTime = moment(this.selectProductTableData[0].createDate).format('YYYY-MM-DD')
            this.productForm.date = [moment(start).isAfter(createTime)===true?start:createTime, end]
          }else{
            this.productForm.date = [start, end]
          }
        }
      }
    },

    fundRangeDatePickerOptions() {
      var self = this
      const pickerOptions = {
        disabledDate(time) {
          let createTime = "";
          if (self.timDate != "") {
            createTime = moment(self.timDate).format('YYYY-MM-DD')
            let end = moment().subtract(1, 'days').format('YYYY-MM-DD')
            end = self.dateTime != '' ? moment(self.dateTime).format('YYYY-MM-DD') : end
            // 设置产品的日期范围，成立日到最新的估值确认日期
            return time < new Date(createTime) || time > new Date(end);
          }else{
            return null;
          }
        },
      }
      return pickerOptions

    },
    // 渲染组件
    renderDiv(temp, params) {
      return new Promise((resolve, reject) => {
        if (params.ZB_INDEXTYPE != 'zdyjz') {
          params.ZB_INDEXCODEA = params.ZB_INDEXCODE
          params.ZB_INDEXWEIGHTA = 100
          params.ZB_INDEXCODEB = '000300'
          params.ZB_INDEXWEIGHTB = 0
          // params.ZB_FUNDCODE = [params.ZB_INDEXCODEA, params.ZB_INDEXWEIGHTA, params.ZB_INDEXCODEB, params.ZB_INDEXWEIGHTB].toString()
        }
        if (params.ZB_X_INTERVAL && params.ZB_X_INTERVAL == '自适应') {
          params.ZB_X_INTERVAL = 'auto'
        }
        pageApi
          .render(params)
          .then((res) => {
            let { status, data } = res.data
            if (status == 200) {
              const scriptStr = `;
                var dom = document.getElementById('component${temp.id}')
                if(dom && dom.childNodes.length > 1) {
                  dom.childNodes[0].style.display = 'none'
                  dom.childNodes[1].style.display = 'flex'
                }
              `
              // 重新渲染div
              data = data.replaceAll('#uuid#', temp.id)
              let script = data.match(/<script\b[^>]*>([\s\S]*?)<\/script>/gm)[0]
              const div = data.replace(script, '')
              script = script.replace(/<script\s+type="text\/javascript"\s*>/g, '')
              script = script.replace(/<\/script>/g, '')
              script += scriptStr
              temp.info.render.script = script
              temp.info.render.div = div
              // 循环清空 组件下的其他dom节点信息
              const rootDiv = document.querySelector(`#component${temp.id}`)
              while (rootDiv.firstChild !== rootDiv.lastChild) {
                rootDiv.removeChild(rootDiv.lastChild)
              }

              renderScript(temp)
            } else if (status == 501) {
              const scriptStr = `;
                var dom = document.getElementById('component${temp.id}')
                if(dom && dom.childNodes.length > 1) {
                  dom.childNodes[0].style.display = 'flex'
                  dom.childNodes[1].style.display = 'none'
                }
              `
              temp.info.render.script = scriptStr
              Vue.nextTick(() => {
                setTimeout(() => {
                  const rootDiv = document.querySelector(`#component${temp.id}`)
                  var deleteJs = document.getElementById(`script_${temp.id}`)
                  deleteJs && deleteJs.remove()
                  // 生产srcipt标签并appendChild
                  const newScript = document.createElement('script')
                  newScript.type = 'text/javascript'
                  newScript.id = `script_${temp.id}`
                  const newScriptInnerHTML = temp.info.render.script
                  newScript.innerHTML = newScriptInnerHTML
                  setTimeout(() => {
                    rootDiv.appendChild(newScript)
                  }, 100)
                }, 100)
              })
            }
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
    },

    renderReplaceScript(temp, params) {
      return new Promise((resolve, reject) => {
        if (params.ZB_INDEXTYPE != 'zdyjz') {
          params.ZB_INDEXCODEA = params.ZB_INDEXCODE
          params.ZB_INDEXWEIGHTA = 100
          params.ZB_INDEXCODEB = '000300'
          params.ZB_INDEXWEIGHTB = 0
          // params.ZB_FUNDCODE = [params.ZB_INDEXCODEA, params.ZB_INDEXWEIGHTA, params.ZB_INDEXCODEB, params.ZB_INDEXWEIGHTB].toString()
        }
        if (params.ZB_X_INTERVAL && params.ZB_X_INTERVAL == '自适应') {
          params.ZB_X_INTERVAL = 'auto'
        }
        pageApi
          .render(params)
          .then((res) => {
            let { status, data } = res.data
            if (status == 200) {
              const scriptStr = `;
                var dom = document.getElementById('component${temp.id}')
                if(dom && dom.childNodes.length > 1) {
                  dom.childNodes[0].style.display = 'none'
                  dom.childNodes[1].style.display = 'flex'
                }
              `
              // 重新渲染div
              data = data.replaceAll('#uuid#', temp.id)
              let script = data.match(/<script\b[^>]*>([\s\S]*?)<\/script>/gm)[0]
              const div = data.replace(script, '')
              script = script.replace(/<script\s+type="text\/javascript"\s*>/g, '')
              script = script.replace(/<\/script>/g, '')
              script += scriptStr
              temp.info.render.script = script
            } else if (status == 501) {
              const scriptStr = `;
                var dom = document.getElementById('component${temp.id}')
                if(dom && dom.childNodes.length > 1) {
                  dom.childNodes[0].style.display = 'flex'
                  dom.childNodes[1].style.display = 'none'
                }
              `
              temp.info.render.script = scriptStr
            }
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
    },

    // 通用属性配置应用全局
    async handleClickEnter() {
      if (!this.validateAllPage()) {
        this.$message.closeAll()
        this.$message.warning('校验失败')
        return
      }
      for (let i = 0; i < this.$store.state.componentDataArray.length; i++) {
        const tempComponentData = this.$store.state.componentDataArray[i]

        for (let j = 0; j < tempComponentData.length; j++) {
          const temp = tempComponentData[j]
          // 全局的对象属性合并
          temp.info.options.forEach((item) => {
            if (item.public) {
              temp.info.params[item.id] = this.$store.state.canvasGlobalConfig[item.public]
            }
          })
          const params = { ...this.$store.state.canvasGlobalConfig, ...temp.info.params }
          params.moduleId = temp.info.id
          // TODO 渲染不同的页面
          if (i == this.$store.state.componentDataIndex) {
            this.renderDiv(temp, params)
          } else {
            this.renderReplaceScript(temp, params)
          }
        }
      }
      this.dialogVisible = false
    },
    // 校验 查询逻辑
    checkRender(info, component) {
      // 先循环遍历info下的options 所有用户的配置属性
      for (const key in info.params) {
        const obj = component.info.options.find((item) => item.id == key)
        if (obj && obj.filter) {
          if (obj.type == 'TP_TXTDOUBLE') {
            if (this.validateInputDouble(key, 0, component) == false || this.validateInputDouble(key, 1, component) == false) {
              return false
            }
          } else if (obj.type == 'TP_TXTSINGLE') {
            if (this.validateInputSingle(key, 0, component) == false) {
              return false
            }
          } else {
            if (this.validateInput(key, component) == false) {
              return false
            }
          }
        }
      }
      return true
    },
    validateInput(id, component) {
      const obj = component.info.options.find((item) => item.id == id)
      if (obj && obj.filter) {
        const reg = new RegExp(this.filterRules[`type${obj.filter}`] || '')
        const msg = this.filterMessage[`type${obj.filter}`] || '输入有误'
        if (obj.filter === '3') {
          if (id == 'ZB_X_INTERVAL') {
            if (component.info.params[id] == 'auto') {
              component.info.params[id] = '自适应'
            }
            if (component.info.params[id] == '自适应') {
              return true
            }
          }
        }
        if (obj.filter == '1' || obj.filter == '3') {
          if (component.info.params[id] == '') {
            // component.info.params[id] = ''
            this.$message.closeAll()
            this.$message.warning('不能为空')
            return false
          }
        }
        if (component.info.params[id] != '' && !reg.test(component.info.params[id])) {
          // component.info.params[id] = ''
          this.$message.closeAll()
          this.$message.warning(msg)
          return false
        }
      }
      return true
    },
    validateInputSingle(id, index, component) {
      const obj = component.info.options.find((item) => item.id == id)
      if (obj && obj.filter) {
        const reg = new RegExp(this.filterRules[`type${obj.filter}`] || '')
        const msg = this.filterMessage[`type${obj.filter}`] || '输入有误'
        if (obj.filter === '3') {
          if (component.info.params[id][index].name == 'auto') {
            return true
          }
        }
        if (obj.filter == '1' || obj.filter == '3') {
          if (component.info.params[id][index].name == '') {
            // component.info.params[id][index].name = ''
            this.$message.closeAll()
            this.$message.warning('不能为空')
            return false
          }
        }
        if (component.info.params[id] != '' && !reg.test(component.info.params[id][index].name)) {
          // component.info.params[id][index].name = ''
          this.$message.closeAll()
          this.$message.warning(msg)
          return false
        }
      }
      return true
    },
    validateInputDouble(id, index, component) {
      const obj = component.info.options.find((item) => item.id == id)
      if (obj && obj.filter) {
        const reg = new RegExp(this.filterRules[`type${obj.filter}`] || '')
        const msg = this.filterMessage[`type${obj.filter}`] || '输入有误'
        if (obj.filter === '3') {
          if (component.info.params[id][index].name == 'auto') {
            return true
          }
        }
        if (obj.filter == '1' || obj.filter == '3') {
          if (component.info.params[id][index].name == '') {
            // component.info.params[id][index].name = ''
            this.$message.closeAll()
            this.$message.warning('不能为空')
            return false
          }
        }
        if (component.info.params[id] != '' && !reg.test(component.info.params[id][index].name)) {
          // component.info.params[id][index].name = ''
          this.$message.closeAll()
          this.$message.warning(msg)
          return false
        }
      }
      return true
    },

    // 校验所有的页面的 组件是否符合校验规则
    validateAllPage() {
      // 保存当前模板
      this.$store.commit('saveComponentDataArrayByIndex')
      let flag = true
      for (let i = 0; i < this.$store.state.componentDataArray.length; i++) {
        const tempComponentData = this.$store.state.componentDataArray[i]
        for (let j = 0; j < tempComponentData.length; j++) {
          const temp = tempComponentData[j]
          if (!this.checkRender(temp.info, temp)) {
            const rootDiv = document.querySelector(`#component${temp.id}`)
            if (rootDiv) {
              rootDiv.style.border = '1px solid red'
            }
            flag = false
          } else {
            const rootDiv = document.querySelector(`#component${temp.id}`)
            if (rootDiv) {
              if (rootDiv.style.border == '1px solid red') {
                rootDiv.style.border = '1px solid #cccccc'
              }
            }
          }
        }
      }
      return flag
    },

    // 转换树形结构
    globalConfigToTree(data) {},

    // 模板-保存（报告内部组件编辑）
    handleSaveTemplate() {
      if (!this.validateAllPage()) {
        this.$message.closeAll()
        this.$message.warning('校验失败')
        return
      }

      if (this.productForm.reportType == '1') {
        this.handleSaveAs()
        return
      }

      if (!this.$store.state.isEditor && (this.currentTemplate.reportId == '' || this.currentTemplate.reportId == undefined)) {
        this.saveAsByEditor()
        return
      }

      this.$bus.$emit('homeload', true)
      // 保存当前模板
      this.$store.commit('saveComponentDataArrayByIndex')
      const componentData = this.$store.getters.componentData
      const canvasGlobalConfig = {
        ...this.$store.state.canvasGlobalConfig,
        pageMarginsOption: this.$store.state.pageMarginsOption
      }
      const params = {
        reportId: this.currentTemplate.reportId,
        fundType: this.currentTemplate.fundType,
        reportHtml: commonOldFun.encryptByAESCommon(document.getElementById('templateEditor').outerHTML),
        source: 'OUT',
        moduleCfg: commonOldFun.encryptByAESCommon(JSON.stringify(this.$store.state.componentDataArray)),
        elementCfg: JSON.stringify(canvasGlobalConfig)
      }
      const moduleCfgRel = componentData.map((item) => {
        return {
          moduleId: item.info.id,
          vueId: item.id,
          elementCfg: item.info.params
        }
      })
      params.moduleCfgRel = JSON.stringify(moduleCfgRel)
      pageApi
        .saveReport(params)
        .then((res) => {
          if (res.data.status === 200) {
            this.$message.success(res.data.message || '保存成功')
          } else {
            this.$message.error(res.data.message || '保存失败')
          }
          this.$bus.$emit('homeload', false)
        })
        .catch((err) => {
          this.$bus.$emit('homeload', false)
        })
    },
    /**
     * @description 模板-新增(另存为)
     */
    handleSaveAs() {
      this.saveAsDialogFormQuery.templateName = ''
      this.saveAsDialogFormQuery.describe = ''
      // 初始化 值
      this.saveAsDialogVisible = true
    },
    handleClickHome() {
      this.$emit('changeshow')
    },
    handleScaleChange() {
      clearTimeout(this.timer)
      this.timer = setTimeout(() => {
        // 画布比例设一个最小值，不能为 0
        // eslint-disable-next-line no-bitwise
        this.scale = ~~this.scale || 1
        changeComponentsSizeWithScale(this.scale)
      }, 1000)
    },
    preview(isScreenshot) {
      this.isScreenshot = isScreenshot
      this.isShowPreview = true
      this.$store.commit('setEditMode', 'preview')
    },
    handlePreviewChange() {
      this.isShowPreview = false
      this.$store.commit('setEditMode', 'edit')
    }
  }
}
</script>

<style lang="scss">
.dialog-single-product {
  width: 55% !important;
  .el-dialog__body {
    overflow: visible !important;
  }
  .dialog-single-product-firstline {
    .el-input--small .el-input__icon {
      line-height: 16px;
    }

    .el-select--small {
      .el-input__icon {
        display: none;
      }
    }
  }
}

.global-drop-down-bg {
  .el-picker-panel__icon-btn {
    color: #ffffff !important;
  }

  .el-select-dropdown__item:hover {
    background-color: #cccccc;
  }

  .el-date-table td.in-range div {
  }
}
</style>
<style lang="scss" scoped>
::v-deep .el-dialog__header span {
  color: #ffffff !important;
}

::v-deep .el-button + .el-button,
.el-checkbox.is-bordered + .el-checkbox.is-bordered {
  margin-left: 5px;
}

.custom-button {
  position: relative;
}

.icon-container {
  position: absolute;
  top: 50%;
  left: 10px; /* 调整左侧图标的位置 */
  transform: translateY(-50%);
}

::v-deep .vxe-cell {
  height: 26px !important;
}

.select-product-table-span {
  height: 26px;
  line-height: 26px;
  font-size: 14px !important;
  -webkit-appearance: none;
  background-image: none;
  border-radius: 4px;
  border: 1px solid #e4e7ed;
  box-sizing: border-box;
  display: inline-block;
  outline: 0;
  padding: 0 15px;
  width: 160px;
  background-color: #f5f7fa;
  color: #c0c4cc;
  cursor: not-allowed;
  overflow: hidden;
}

::v-deep .el-icon-arrow-down:before {
  content: none;
}

.global {
  color: #20212b !important;
  .global-class {
    // background-color: #282828;
    // border: 1px solid #545454;
    margin-bottom: 10px;
    padding: 5px;
  }

  ::v-deep .el-input__suffix {
    top: 3px;
    font-size: 14px;
  }

  ::v-deep .el-select .el-input .el-select__caret {
    font-size: 14px;
  }

  ::v-deep .el-dialog__header {
    font-size: 16px !important;
    // padding: 5px !important;
  }

  ::v-deep .el-dialog__footer {
    // padding: 3px !important;
    margin-top: -15px;
    padding-right: 8px !important;
  }

  ::v-deep .el-dialog__body {
    padding: 8px !important;
    padding-top: 0px !important;
  }

  ::v-deep .el-dialog__title {
    color: white !important;
  }

  ::v-deep .el-input--small .el-input__inner {
    height: 26px;
    // background-color: #202020;
    // color: #FFFFFF;
    // padding-left: 5px;
    // border: 0.5px solid #6d6d6d;
  }

  ::v-deep .el-color-picker--small .el-color-picker__trigger {
    height: 26px;
    // border: 0.5px solid #6d6d6d;
    color: #ffffff;
  }

  .first-title {
    font-weight: 600;
    font-size: 14px;
    margin-bottom: 5px;
  }

  .second-title {
    padding-right: 20px;
    font-size: 14px;
    margin-bottom: 5px;
  }

  ::v-deep .el-color-picker--small .el-color-picker__trigger {
    width: 160px;
  }
}

.save-as {
  ::v-deep .el-dialog {
    width: 20% !important;
  }

  ::v-deep .el-textarea__inner {
    // background-color: #202020;
    // color: #FFFFFF;
    // padding-left: 5px;
    // border: 0.5px solid #6d6d6d;
  }
}

.select-fund {
  ::v-deep .el-input--small .el-input__inner {
    height: 26px;
    // background-color: #202020;
    // color: #FFFFFF;
    // padding-left: 5px;
    // border: 0.5px solid #6d6d6d;
  }

  .el-picker-panel__icon-btn {
    // color: #fff !important;
  }

  ::v-deep .el-dialog__header {
    // background-color: #000;
    font-size: 16px !important;
    // padding: 5px !important;
  }

  ::v-deep .el-dialog__footer {
    // padding: 3px !important;
    margin-top: -15px;
    padding-right: 8px !important;
    // background-color: #000;
  }

  ::v-deep .el-dialog__body {
    color: #20212b;
    // background-color: #000;
    padding: 8px !important;
    padding-top: 0px !important;
  }

  ::v-deep .el-dialog__title {
    // color: #fff !important;
  }

  ::v-deep .el-select input {
    height: 26px;
    // background-color: #202020;
    // color: #FFFFFF;
    // border: 0.5px solid #6d6d6d;
  }

  ::v-deep .el-date-editor input,
  .el-range-editor.is-disabled,
  .el-range-editor--small.el-input__inner {
    height: 26px;
    background-color: rgba(255, 255, 255, 0);
    // background-color: #202020;
    // color: #fff !important;
    // border: 0.5px solid #6d6d6d;
  }

  ::v-deep .el-range-editor.el-input__inner {
    padding: 0px 10px;
  }

  ::v-deep .el-date-editor .el-range-separator {
    width: 10%;
  }

  ::v-deep .el-range-editor--small .el-range-separator {
    color: #c0c4cc !important;
  }

  ::v-deep .el-icon-d-arrow-left,
  .el-icon-arrow-left {
    color: #fff !important;
  }

  ::v-deep .el-input__suffix {
    top: 3px;
    font-size: 14px;
  }

  ::v-deep .el-radio__input.is-checked .el-radio__inner {
    border-color: #e9c5a5;
    background: #e9c5a5;
  }

  ::v-deep .el-radio__input.is-checked + .el-radio__label {
    color: #757778;
  }


  ::v-deep .vxe-header--row {
    // background-color: #282828;
    color: #fff;
  }

  ::v-deep .vxe-table--body-wrapper {
    // background-color: #282828;
    color: #fff;
  }
}

.toolbar {
  background-color: #e6e8f0;
  position: relative;
  padding: 10px 10px 5px 10px;
  white-space: nowrap;
  overflow-x: auto;
  //border-bottom: 1px solid #ddd;
  display: flex;
  align-items: center;

  .canvas-area,
  .btn-area {
    flex: 1;
  }

  .canvas-area {
    text-align: left;
  }

  ::v-deep .el-button.el-button--primary {
    height: 32px;
  }

  .page-left-button {
    position: absolute;
    left: 20px;
    font-size: 22px;
    color: black;
  }

  .icon-hover:hover {
    cursor: pointer;
  }

  .page-title {
    position: absolute;
    left: 20px;
    top: 10px;
    font-size: 16px;
  }

  .btn-area {
    text-align: right;
  }

  .canvas-config {
    display: inline-block;
    margin-left: 10px;
    font-size: 14px;
    color: #333;

    input {
      width: 50px;
      margin-left: 4px;
      outline: none;
      padding: 0 5px;
      border: 1px solid #ddd;
      color: #333;
    }

    span {
      margin-left: 10px;
    }
  }
}
</style>

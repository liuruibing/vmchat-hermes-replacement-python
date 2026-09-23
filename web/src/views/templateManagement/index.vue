<template>
  <div class="template-management" id="template-management" v-auto-enter>
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form class="standard-form" :model="formQuery" inline>
          <el-row>
            <el-form-item>
              <el-input v-model="formQuery.reportName" placeholder="请输入模板名称" size="small" style="width: 180px" @input="handleInputChange"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button size="small" type="primary" @click="handleSearch" icon="el-icon-search">查询</el-button>
              <el-button size="small" type="info" plain icon="el-icon-refresh" @click="() => (formQuery.reportName = '')">重置</el-button>
            </el-form-item>
            <el-rorm-item style="float:right">
              <el-button size="small" type="info" plain @click="handleCreateNewTemplate">新建模板</el-button>
            </el-rorm-item>
          </el-row>
        </el-form>
<!--        <ToolBarSlot>
          <template slot="left">
            <el-button size="small" type="info" plain @click="handleCreateNewTemplate">新建模板</el-button>
          </template>
        </ToolBarSlot>-->
      </div>
    </div>
    <div id="standard-table" class="table-content">
      <div id="standard-table-margin">
        <vxe-table ref="refsTable" v-loading="tableLoading" :data="tableData" :height="tableHeight" auto-resize show-overflow="tooltip" stripe="" style="width: 100%" resizable sync-resize>
          <vxe-table-column align="center" label="序号" type="index" width="50"></vxe-table-column>
          <template v-for="item in columns">
            <vxe-table-column :key="item.key" :align="item.align" :field="item.prop" :label="item.label" :min-width="item.width" :sortable="item.sortable" header-align="center">
              <template slot-scope="scope">
                <span v-if="item.filter == 'moneyYuan'">{{ scope.row[item.prop] }}</span>
                <span v-if="item.filter == 'moneyYuanFour'">
                  {{ scope.row[item.prop] }}
                </span>
                <span v-if="item.filter == 'normal'">{{ scope.row[item.prop] }}</span>
                <div v-if="item.filter == 'image'">
                  <el-image :preview-src-list="[require('@/assets/templateReport.png')]" :src="require('@/assets/templateReport.png')" style="width: 50px; height: 50px"></el-image>
                </div>
                <span v-if="item.filter == 'operate'" class="table-operation">
                  <template v-if="scope.row.reportType == 1">
                    <el-button size="small" type="info" plain @click="handleLookTemplate(scope.row)">查看</el-button>
                    <el-button v-btn="'reportTemplateEdit'" plain size="small" type="info" @click="handleEditTemplateDialog(scope.row)">编辑</el-button>
                    <el-button v-btn="'reportTemplateDel'" plain size="small" type="info" @click="deleteTemplate(scope.row)">删除</el-button>
                  </template>
                  <template v-else>
                    <el-button size="small" type="info" plain @click="handleLookTemplate(scope.row)">查看</el-button>
                    <el-button size="small" type="info" plain @click="handleEditTemplateDialog(scope.row)">编辑</el-button>
                    <el-button plain size="small" type="info" @click="deleteTemplate(scope.row)">删除</el-button>
                  </template>
                </span>
                <span v-if="item.filter == 'reportType'">
                  {{ scope.row[item.prop] | reportTypeToStr }}
                </span>
                <span v-if="item.filter == 'fundType'">
                  {{ scope.row[item.prop] | fundTypeToStr }}
                </span>
              </template>
            </vxe-table-column>
          </template>
        </vxe-table>
      </div>
    </div>
    <!-- 新建模板/编辑模板   -->
    <el-dialog :close-on-click-modal="false" :title="basicTemplateTitle" :visible.sync="basicTemplateDialogVisible" width="50% !important">
      <el-form ref="basicTemplateDialog" :model="basicTemplateFormQuery" :rules="basicTemplateRules" class="basic-template-dialog" label-width="82px">
        <el-row>
          <el-col :span="12">
            <el-form-item label="模板名称" prop="templateName">
              <el-input v-model="basicTemplateFormQuery.templateName" size="small"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="报告类型" prop="fundType">
              <el-select v-model="basicTemplateFormQuery.fundType" :disabled="basicTemplateReportTypeStatus" placeholder="请选择" size="small">
                <el-option v-for="item in fundTypeOption" :key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="模板描述" prop="describe">
          <el-input v-model="basicTemplateFormQuery.describe" :rows="4" placeholder="请输入内容" size="small" style="width: 100% !important" type="textarea"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button size="small" type="primary" @click="handleSaveTemplate" :loading="saveLoading">保存模板</el-button>
      </div>
    </el-dialog>
    <!-- 模板预览   -->
    <el-dialog :close-on-click-modal="false" :visible.sync="previewTemplateDialogVisible" custom-class="previewTemplate" title="模板预览" width="50% !important">
      <el-row style="height: 501px; overflow-y: auto; border-top: 1px solid #e9e9e9">
        <el-col :span="5" style="border-right: 2px solid #e9e9e9; height: 500px">
          <div
            v-for="item in previewArray"
            :class="[previewOption.activedPreview.reportName == item.reportName ? 'activated-preview' : '']"
            style="height: 40px; vertical-align: middle; line-height: 40px; text-align: left; padding-left: 5px"
            @click="handlePreviewClick(item)"
          >
            <span>
              <img v-if="item.reportName == '空白模板'" src="~@/assets/img/emptyTemplate.png" />
              <img v-else src="~@/assets/img/systemTemplate.png" />
              <span :class="[previewOption.activedPreview.reportName == item.reportName ? 'activated-preview-fontcolor' : '']" style="margin-left: 5px">
                {{ item.reportName }}
              </span>
            </span>
          </div>
        </el-col>
        <el-col :span="19" style="padding-left: 20px">
          <div style="max-height: 500px; overflow-y: auto">
            <img v-if="previewOption.activedPreview.thumbnail" :src="'data:image/png;base64,' + previewOption.activedPreview.thumbnail" height="100%" width="100%" />
          </div>
        </el-col>
      </el-row>
      <div slot="footer">
        <el-button size="small" type="primary" @click="handlePreviewNextStep">下一步</el-button>
      </div>
    </el-dialog>

    <!-- 产品选择 输入框  -->
    <el-dialog :close-on-click-modal="false" :visible.sync="selectProductDialogVisible" custom-class="dialog-single-product" title="选择产品" width="55%">
      <div>
        <span style="width: 60px; display: inline-block">产品名称</span>
<!--        <el-input
          v-model="selectProductTableData[0].fundCode"
          clearable
          placeholder="请选择产品"
          size="small"
          @click.native="handleSelectProductTypeClick(selectProductTableData[0])"
        ></el-input>-->
<!--        <ProductSelectSearch
          ref="productSelect"
          v-model="singleCode"
          :forceFlag="'B'"
          :size="'small'"
          style="width: 180px; margin-right: 10px;"
          @select-product="handleProductSelect"
        />-->

          <ProductSelectInput
            v-model="product"
            placeholder="请选择产品"
            :input-width="'260px'"
            @select="handleProductSelect"
            @clear="handleProductClear"
          />
        <span style="width: 60px; display: inline-block">产品代码</span>
        <el-input v-model="selectProductTableData[0].fundCode" :disabled="true" clearable size="small"></el-input>
        <span style="width: 60px; display: inline-block">产品类型</span>
        <el-select v-model="selectProductTableData[0].source" :disabled="true" clearable size="small" placeholder="">
          <el-option v-for="item in sourctOptions" :key="item.id" :label="item.label" :value="item.id"></el-option>
        </el-select>
      </div>
      <div class="mt10">
        <span style="width: 60px; display: inline-block">基准类型</span>
        <el-select v-model="basicTemplateFormQuery.ZB_INDEXTYPE" clearable placeholder="请选择" size="small">
          <el-option v-for="item in ZB_INDEXTYPEOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
        </el-select>
      </div>
      <div v-show="basicTemplateFormQuery.ZB_INDEXTYPE == 'gdjz'" class="mt10">
        <span style="width: 60px; display: inline-block">选择基准</span>
        <el-select v-model="basicTemplateFormQuery.ZB_INDEXCODE" clearable placeholder="请选择" size="small">
          <el-option v-for="item in $store.state.indexArray" :key="item.id" :label="item.label + '(' + item.id + ')'" :value="item.id"></el-option>
        </el-select>
      </div>
      <div v-show="basicTemplateFormQuery.ZB_INDEXTYPE == 'zdyjz'" class="mt10">
        <span style="width: 60px; display: inline-block">基准 A</span>
        <el-select v-model="basicTemplateFormQuery.ZB_INDEXCODEA" clearable placeholder="请选择" size="small">
          <el-option v-for="item in $store.state.compareIndexArray" :key="item.id" :label="item.label + '(' + item.id + ')'" :value="item.id"></el-option>
        </el-select>
        <span style="width: 60px; display: inline-block; margin-left: 10px">权重 A</span>
        <el-input v-model="basicTemplateFormQuery.ZB_INDEXWEIGHTA" size="small" @blur="handleInputWeight('A')"></el-input>
        %
      </div>
      <div v-show="basicTemplateFormQuery.ZB_INDEXTYPE == 'zdyjz'" class="mt10">
        <span style="width: 60px; display: inline-block">基准 B</span>
        <el-select v-model="basicTemplateFormQuery.ZB_INDEXCODEB" clearable placeholder="请选择" size="small">
          <el-option v-for="item in $store.state.compareIndexArray" :key="item.id" :label="item.label + '(' + item.id + ')'" :value="item.id"></el-option>
        </el-select>
        <span style="width: 60px; display: inline-block; margin-left: 10px">权重 B</span>
        <el-input v-model="basicTemplateFormQuery.ZB_INDEXWEIGHTB" size="small" @blur="handleInputWeight('B')"></el-input>
        %
      </div>
      <div class="mt10">
        <span style="width: 60px; display: inline-block">选择时间</span>
        <el-date-picker
          unlink-panels
          v-model="basicTemplateFormQuery.date"
          :disabled="basicTemplateFormQuery.timeType != 'self'"
          end-placeholder="结束日期"
          range-separator="至"
          size="small"
          start-placeholder="开始日期"
          type="daterange"
          value-format="yyyy-MM-dd"
          :picker-options="fundRangeDatePickerOptions()"
        ></el-date-picker>
      </div>
      <div style="margin-left: 60px; margin-top: 10px">
        <el-radio-group v-model="basicTemplateFormQuery.timeType" @input="handleBasicTemplateTimeTypeClick">
          <el-radio label="self">自定义</el-radio>
          <el-radio label="m1">近一月</el-radio>
          <el-radio label="m3">近三月</el-radio>
          <el-radio label="m6">近六月</el-radio>
          <el-radio label="y1">近一年</el-radio>
          <el-radio label="yd">今年以来</el-radio>
          <el-radio v-if="basicTemplateFormQuery.reportType == '1'" label="cd">成立以来</el-radio>
        </el-radio-group>
      </div>
      <template slot="footer">
        <el-button size="small" type="primary" @click="handleSelectProductNextStep">下一步</el-button>
      </template>
    </el-dialog>
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
import productSelector from '@/components/productSelector'
import ProductSelectSearch from '@/components/productSelector/ProductSelectSearch.vue'
import pageApi from '@/api/templateManageMent/index'
import request from '@/utils/request'
import commonApi from '@/api/common'
import ToolBarSlot from '@/components/toolBarSlot'
import moment from 'moment/moment'

import ProductSelectInput from '@/components/productSelector/ProductSelectInput'
export default {
  components: { productSelector, ToolBarSlot,ProductSelectSearch ,ProductSelectInput},
  filters: {
    reportTypeToStr(value) {
      if (value == '1') {
        return '默认模板'
      } else {
        return '自定义模板'
      }
    },
    fundTypeToStr(value) {
      if (value == '1') {
        return '单产品分析报告'
      } else {
        return '多产品对比报告'
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
  data() {
    return {

      product: null,
      singleCode:'',
      // 保存模板loading
      saveLoading: false,
      isSystemLookTemplateFlag: -1, // 是否是系统模板的查看标识
      tableHeight: 0,
      isCreateNewTemplate: false, // 是否新建模板的标识
      tableLoading: false,
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
      selectList: [],
      productSelectorVisible: false, // 产品选择弹窗
      basicTemplateDialogVisible: false,
      basicTemplateReportTypeStatus: false, // 新建/编辑模板报告类型是否可编辑
      previewTemplateDialogVisible: false, // 模板预览页面
      selectProductDialogVisible: false, // 选择产品的弹窗
      selectProductDialogRowPointer: null, // 选择产品弹窗对应的行对象
      basicTemplateTitle: '新建模板',
      viewChange: '列表视图',
      viewIcon: 'el-icon-s-grid',
      formQuery: {
        reportName: ''
      },
      basicTemplateFormQuery: {
        // 新增模板的 查询条件
        fundType: '1',
        templateName: '',
        fundName: '',
        reportType: '',
        describe: '',
        activedPreview: {},
        ZB_INDEXCODE: '', // 基准编码
        ZB_INDEXTYPE: 'gdjz', // 基准类型
        ZB_INDEXCODEA: '', // 基准A
        ZB_INDEXWEIGHTA: '0', // 基准A权重
        ZB_INDEXCODEB: '', // 基准B
        ZB_INDEXWEIGHTB: '0', // 基准B权重
        date: [],
        timeType: 'self',
        selectTableData: []
      },
      //产品最新的估值确认日期

      selectProductTableData: [
        {
          fundCode: '',
          fundName: '',
          source: '',
          gzLastDate:'', //产品最新的估值确认日期
        }
      ], // 选择产品的数组
      previewOption: {
        activedPreview: {}, // 当前活跃的模板预览对象
        reportType: '1' // 报告类型
      },
      //成立日
      timDate: '',
      //最新估值确认日
      dateTime:'',
      basicTemplateRules: {
        templateName: [
          {
            required: true,
            message: '请输入模板名称',
            trigger: 'blur'
          }
        ],
        reportType: [
          {
            required: true,
            message: '请选择报告类型',
            trigger: 'blur'
          }
        ]
      },
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

      pickerOptions: {
        shortcuts: [
          {
            text: '最近一个月',
            onClick(picker) {
              const end = new Date()
              const start = new Date()
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '最近三个月',
            onClick(picker) {
              const end = new Date()
              const start = new Date()
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '最近六个月',
            onClick(picker) {
              const end = new Date()
              const start = new Date()
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 180)
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '最近一年',
            onClick(picker) {
              const end = new Date()
              const start = new Date()
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 365)
              picker.$emit('pick', [start, end])
            }
          }
        ]
      },
      datumOption: this.$store.state.indexArray,
      datumCompareOption: this.$store.state.compareIndexArray,
      templateRules: {
        data: [
          {
            required: true,
            message: '请选择日期',
            trigger: blur
          }
        ],
        templateName: [
          {
            required: true,
            message: '请输入报告名称',
            trigger: blur
          }
        ]
      },
      templateFormObject: {
        data: [],
        templateName: ''
      },
      currentTemplate: '',
      templateData: [
        {
          label: '基金',
          fundName: '华夏大盘精选',
          fundCode: '000011.OF',
          colorCode: 'rgba(1, 1, 1, 1)'
        },
        {
          label: '基准',
          fundName: '沪深300',
          fundCode: '000300.SH',
          colorCode: 'rgba(1, 1, 1, 1)'
        }
      ],
      tableData: [],
      benchmarkOption: [
        {
          label: '沪深300',
          value: '000300.SH'
        }
      ],
      fundTypeOption: [
        {
          value: '1',
          label: '单产品分析报告'
        }
        // {
        //   value: '2',
        //   label: '多产品对比报告'
        // }
      ], // 报告类型下拉
      columns: [
        {
          label: '模板名称',
          prop: 'reportName',
          align: 'left',
          width: '180px',
          filter: 'normal'
        },
        {
          label: '创建人',
          prop: 'createUserName',
          align: 'center',
          width: '80px',
          filter: 'normal'
        },
        {
          label: '模板类型',
          prop: 'reportType',
          align: 'center',
          width: '80px',
          filter: 'reportType',
          sortable: true
        },
        {
          label: '报告类型',
          prop: 'fundType',
          align: 'center',
          width: '80px',
          filter: 'fundType',
          sortable: true
        },
        {
          label: '更新时间',
          prop: 'updateTime',
          align: 'center',
          width: '180px',
          filter: 'normal',
          sortable: true
        },
        {
          label: '描述',
          prop: 'reportDesc',
          align: 'left',
          width: '180px',
          filter: 'normal'
        },
        {
          label: '操作',
          prop: 'operate',
          align: 'center',
          width: '180px',
          filter: 'operate'
        }
      ],
      previewArray: [], // 模板预览数组
      count: 0,
      loading: false
    }
  },
  computed: {

    noMore() {
      return this.count >= 20
    },
    disabled() {
      return this.loading || this.noMore
    },
    singleSource() {
      if (this.selectProductTableData[0] && this.selectProductTableData[0].source) {
        if (this.selectProductTableData[0].source == 'IN') {
          return '托管/外包'
        } else if (this.selectProductTableData[0].source == 'OUT') {
          return '私募排排'
        } else {
          return '-'
        }
      } else {
        return ''
      }
    }
  },
  watch: {
    selectProductDialogVisible(val) {
      if (!val) {
        const selectComp = this.$refs.productSelect;
        if (selectComp) {
          selectComp.selectedValue = '';
        }
      }
    }
  },
  mounted() {
    this.getTemplateList()
    this.handleTableHeight()
    // this.getContrasOptions()
  },
  beforeDestroy() {
    // 组件销毁移除监听事件
    window.onresize = null
  },
  methods: {
    async handleProductSelect(product) {

      this.$set(this.selectProductTableData, 0, {
        fundCode: product.VC_FUNDCODE,       // 产品代码
        fundName: product.VC_FUNDNAME,       // 产品名称
        source: product.VC_FLAG || '',       // 产品类型
        createDate: product.D_CREATE_DATE || '', // 成立日期
        gzLastDate: ''
      });

      // 更新成立日期
      this.timDate = product.D_CREATE_DATE || '';

      await this.initTimGzLastDate(product.VC_FUNDCODE);
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
        this.timDate = '';
        this.dateTime = '';
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
        if (!regex.test(this.basicTemplateFormQuery.ZB_INDEXWEIGHTA)) {
          this.$message.closeAll()
          this.$message.warning('只能输入大于等于0的数')
          this.basicTemplateFormQuery.ZB_INDEXWEIGHTA = '0'
          return
        }
        if (this.basicTemplateFormQuery.ZB_INDEXWEIGHTB != '') {
          if (Number(this.basicTemplateFormQuery.ZB_INDEXWEIGHTA) + Number(this.basicTemplateFormQuery.ZB_INDEXWEIGHTB) > 100) {
            this.$message.closeAll()
            this.$message.warning('基金A、B权重不能超过100%')
            this.basicTemplateFormQuery.ZB_INDEXWEIGHTA = '0'
          } else {
            this.basicTemplateFormQuery.ZB_INDEXWEIGHTA = '' + Number(this.basicTemplateFormQuery.ZB_INDEXWEIGHTA).toFixed(4)
          }
        }
      } else {
        if (!regex.test(this.basicTemplateFormQuery.ZB_INDEXWEIGHTB)) {
          this.$message.closeAll()
          this.$message.warning('只能输入大于等于0的数')
          this.basicTemplateFormQuery.ZB_INDEXWEIGHTB = '0'
          return
        }
        if (this.basicTemplateFormQuery.ZB_INDEXWEIGHTA != '') {
          if (Number(this.basicTemplateFormQuery.ZB_INDEXWEIGHTA) + Number(this.basicTemplateFormQuery.ZB_INDEXWEIGHTB) > 100) {
            this.$message.closeAll()
            this.$message.warning('基金A、B权重不能超过100')
            this.basicTemplateFormQuery.ZB_INDEXWEIGHTB = '0'
          } else {
            this.basicTemplateFormQuery.ZB_INDEXWEIGHTB = '' + Number(this.basicTemplateFormQuery.ZB_INDEXWEIGHTB).toFixed(4)
          }
        }
      }
    },
    /**
     * @description 获取对比基准下拉
     */
    getContrasOptions() {
      return new Promise((resolve, reject) => {
        request({
          url: `/api/report/v1.0/data/sql/ecd8867c-64cc-4ebc-9070-04524b04b72c`,
          method: 'post',
          data: {
            indexCode: 'ecd8867c-64cc-4ebc-9070-04524b04b72c'
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
    // 获取单多产品的模板
    getTemplateListForDialog() {
      return new Promise((resolve, reject) => {
        const params = {}
        params.fundType = this.basicTemplateFormQuery.fundType
        this.previewArray = []
        this.previewOption.activedPreview = {}
        pageApi
          .selectTemplateList(params)
          .then((res) => {
            if (res.data.status === 200) {
              const tempArray = []
              res.data.data.forEach((item) => {
                if (item.reportType == 1) {
                  tempArray.push(item)
                }
              })
              this.previewArray = tempArray
              if (this.previewArray && this.previewArray.length > 0) {
                this.previewOption.activedPreview = this.previewArray[0]
              }
            } else {
              this.previewArray = []
              this.previewOption.activedPreview = {}
            }
            resolve()
          })
          .catch((err) => {
            this.previewArray = []
            this.previewOption.activedPreview = {}
            resolve()
          })
      })
    },
    /**
     * @description 查询
     */
    handleSearch() {
      const params = {}
      this.tableLoading = true
      params.reportName = this.formQuery.reportName
      pageApi.selectTemplateList(params).then((res) => {
        if (res.data.status === 200) {
          this.tableData = res.data.data || []
          this.tableLoading = false
        } else {
          this.tableData = []
          this.tableLoading = false
        }
      })
    },
    /**
     * @description 查询模板列表信息
     */
    getTemplateList() {
      const params = {}
      this.tableLoading = true
      pageApi.selectTemplateList(params).then((res) => {
        if (res.data.status === 200) {
          this.tableData = res.data.data || []
          this.tableLoading = false
        } else {
          this.tableData = []
          this.tableLoading = false
        }
      })
    },
    /**
     * @description 查询监听input事件
     */
    handleInputChange(val) {
      // console.log(val)
    },
    /**
     * @description 删除报告模板
     */
    deleteTemplate(row) {
      const params = {
        reportId: row.reportId
      }
      this.$confirm('此操作将永久删除该报告模板, 是否继续?', '提示', {
        cancelButtonText: '取消',
        confirmButtonText: '确定',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',

      })
        .then(() => {
          this.tableLoading = true
          pageApi
            .deleteTemplateReport(params)
            .then((res) => {
              this.tableLoading = false
              if (res.data.status === 200) {
                this.$message.success(res.data.message || '删除成功')
                this.getTemplateList()
              } else {
                this.$message.error(res.data.message || '删除失败')
              }
            })
            .catch((err) => {
              this.tableLoading = false
            })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
    },
    /**
     * @description 编辑报告模板弹窗
     */
    handleEditTemplateDialog(row) {
      this.basicTemplateTitle = '编辑模板'
      this.basicTemplateReportTypeStatus = true
      this.basicTemplateFormQuery.templateName = row.reportName
      this.basicTemplateFormQuery.reportType = row.reportType
      this.basicTemplateFormQuery.fundType = row.fundType
      this.basicTemplateFormQuery.describe = row.reportDesc
      this.basicTemplateFormQuery.reportId = row.reportId
      this.basicTemplateDialogVisible = true
    },
    /**
     * @description 查看模板
     */
    async handleLookTemplate(row) {

      this.isSystemLookTemplateFlag = -1
      this.singleCode = '' // 清空
      this.timDate = ''    // 清空成立日期
      this.dateTime = ''   // 清空估值日期
      // 判断是系统模板 还是 自定义模板
      if (row.reportType == '1') {
        this.isSystemLookTemplateFlag = 1
        // 标识符号 修改为false
        this.isCreateNewTemplate = false
        this.selectProductTableData = []
        // 动态的做增减
        this.$set(this.selectProductTableData, this.selectProductTableData.length, {
          source: '',
          fundCode: '',
          fundName: '',
          createDate: ''
        })
        this.basicTemplateFormQuery = {
          ...this.basicTemplateFormQuery,
          ...{
            fundType: '1',
            templateName: '',
            fundName: '',
            reportType: '',
            describe: '',
            activedPreview: {},
            ZB_INDEXCODE: '', // 基准编码
            ZB_INDEXTYPE: 'gdjz', // 基准类型
            ZB_INDEXCODEA: '', // 基准A
            ZB_INDEXWEIGHTA: '0', // 基准A权重
            ZB_INDEXCODEB: '', // 基准B
            ZB_INDEXWEIGHTB: '0', // 基准B权重
            date: [],
            timeType: 'self',
            selectTableData: []
          }
        }
        this.basicTemplateFormQuery.activedPreview = row
        // 系统模板
        // 弹窗让用户选择产品
        // 初始化选择产品的信息
        this.selectProductDialogVisible = true
      } else {
        // 自定义模板
        // 判断有没有权限
        const elementCfg = JSON.parse(row.elementCfg)
        this.tableLoading = true
        const result = await this.handleJudgeProdectByZSWB(elementCfg.ZB_FUNDCODE)
        this.tableLoading = false
        // if (result == false) {
        //   result = await this.handleJudgeProductBySCSM(elementCfg.ZB_FUNDCODE)
        // }

        if (result == true) {
          this.$emit('handleShowTemplate', row)
        } else {
          this.isSystemLookTemplateFlag = 2
          // 标识符号 修改为false
          this.isCreateNewTemplate = false
          this.selectProductTableData = []
          // 动态的做增减
          this.$set(this.selectProductTableData, this.selectProductTableData.length, {
            source: '',
            fundCode: '',
            fundName: '',
            createDate: ''
          })
          this.basicTemplateFormQuery = {
            ...this.basicTemplateFormQuery,
            ...{
              fundType: '1',
              templateName: '',
              fundName: '',
              reportType: '',
              describe: '',
              activedPreview: {},
              ZB_INDEXCODE: '', // 基准编码
              ZB_INDEXTYPE: 'gdjz', // 基准类型
              ZB_INDEXCODEA: '', // 基准A
              ZB_INDEXWEIGHTA: '0', // 基准A权重
              ZB_INDEXCODEB: '', // 基准B
              ZB_INDEXWEIGHTB: '0', // 基准B权重
              date: [],
              timeType: 'self',
              selectTableData: []
            }
          }
          this.basicTemplateFormQuery.activedPreview = row
          this.selectProductDialogVisible = true
        }
      }
    },
    handleJudgeProductBySCSM(fundCode) {
      return new Promise((resolve, reject) => {
        const params = {}
        params.indexCode = '328b54c4-1d91-4368-abb8-ced23952ae95'
        params.userInput = fundCode
        params._pageFlag = true
        params._pageNum = 1
        params._pageSize = 20
        commonApi
          .getDataBysqlCode(params)
          .then((res) => {
            const { status, data } = res.data
            if (status === 0) {
              if (data.rows && data.rows.length > 0) {
                resolve(true)
              } else {
                resolve(false)
              }
            } else {
              resolve(false)
            }
          })
          .catch((err) => {
            resolve(false)
          })
      })
    },
    handleJudgeProdectByZSWB(fundCode) {
      return new Promise((resolve, reject) => {
        const params = {}
        params.indexCode = '32aad2ac-edf2-4a05-86a2-75b78aa2ba64'
        params.userInput = fundCode
        params.flag = 'B'
        params._pageFlag = true
        params._pageNum = 1
        params._pageSize = 20
        commonApi
          .getDataBysqlCode(params)
          .then((res) => {
            const { status, data } = res.data
            if (status === 0) {
              if (data.rows && data.rows.length > 0) {
                resolve(true)
              } else {
                resolve(false)
              }
            } else {
              resolve(false)
            }
          })
          .catch((err) => {
            resolve(false)
          })
      })
    },
    // 触发 选择产品下一步操作
    handleSelectProductNextStep() {
      // 第一步： 校验
      for (let i = 0; i < this.selectProductTableData.length; i++) {
        const temp = this.selectProductTableData[i]
        if (temp.fundCode == '') {
          this.$message.closeAll()
          this.$message.warning('请选择产品')
          return
        }
      }
      if (this.basicTemplateFormQuery.ZB_INDEXTYPE == '') {
        this.$message.closeAll()
        this.$message.warning('请选择基准类型')
        return
      }

      if (this.basicTemplateFormQuery.ZB_INDEXTYPE == 'gdjz') {
        if (this.basicTemplateFormQuery.ZB_INDEXCODE == '') {
          this.$message.closeAll()
          this.$message.warning('请选择基准')
          return
        }
      } else {
        if (this.basicTemplateFormQuery.ZB_INDEXCODEA == '' || this.basicTemplateFormQuery.ZB_INDEXCODEB == '') {
          this.$message.closeAll()
          this.$message.warning('基金A/B不能为空')
          return
        }
      }
      if (
        this.basicTemplateFormQuery.date == '' ||
        (this.basicTemplateFormQuery.date.length > 0 && this.basicTemplateFormQuery.date[0] == '') ||
        this.basicTemplateFormQuery.date[1] == ''
      ) {
        this.$message.closeAll()
        this.$message.warning('请选择开始结束日期')
        return
      }

      if (this.basicTemplateFormQuery.activedPreview == '') {
        this.$message.closeAll()
        this.$message.warning('请选择模板')
        return
      }

      // 第三步： 新增成功之后 跳转到编辑 页面
      const templateObj = {
        selectProductTableData: this.selectProductTableData,
        reportDesc: this.basicTemplateFormQuery.describe,
        reportName: this.basicTemplateFormQuery.templateName,
        fundType: this.basicTemplateFormQuery.fundType,
        ZB_FUNDNAME: this.selectProductTableData.map((item) => item.fundName).toString(),
        ZB_FUNDCODE: this.selectProductTableData.map((item) => item.fundCode).toString(),
        timeType: this.basicTemplateFormQuery.timeType,
        ZB_INDEXCODE: this.basicTemplateFormQuery.ZB_INDEXCODE,
        ZB_INDEXTYPE: this.basicTemplateFormQuery.ZB_INDEXTYPE,
        ZB_INDEXCODEA: this.basicTemplateFormQuery.ZB_INDEXCODEA,
        ZB_INDEXCODEB: this.basicTemplateFormQuery.ZB_INDEXCODEB,
        ZB_INDEXWEIGHTA: this.basicTemplateFormQuery.ZB_INDEXWEIGHTA,
        ZB_INDEXWEIGHTB: this.basicTemplateFormQuery.ZB_INDEXWEIGHTB,
        ZB_BEGINDATE: this.basicTemplateFormQuery.date[0],
        ZB_ENDDATE: this.basicTemplateFormQuery.date[1],
        activedPreview: this.basicTemplateFormQuery.activedPreview,
        pageMarginsOption: JSON.parse(this.basicTemplateFormQuery.activedPreview.elementCfg).pageMarginsOption
      }
      this.$store.commit('SET_GLOBAL_CONFIG', {
        selectProductTableData: this.selectProductTableData,
        reportDesc: this.basicTemplateFormQuery.describe,
        reportName: this.basicTemplateFormQuery.templateName,
        fundType: this.basicTemplateFormQuery.fundType,
        ZB_FUNDNAME: this.selectProductTableData.map((item) => item.fundName).toString(),
        ZB_FUNDCODE: this.selectProductTableData.map((item) => item.fundCode).toString(),
        timeType: this.basicTemplateFormQuery.timeType,
        ZB_INDEXCODE: this.basicTemplateFormQuery.ZB_INDEXCODE,
        ZB_INDEXTYPE: this.basicTemplateFormQuery.ZB_INDEXTYPE,
        ZB_INDEXCODEA: this.basicTemplateFormQuery.ZB_INDEXCODEA,
        ZB_INDEXCODEB: this.basicTemplateFormQuery.ZB_INDEXCODEB,
        ZB_INDEXWEIGHTA: this.basicTemplateFormQuery.ZB_INDEXWEIGHTA,
        ZB_INDEXWEIGHTB: this.basicTemplateFormQuery.ZB_INDEXWEIGHTB,
        ZB_BEGINDATE: this.basicTemplateFormQuery.date[0],
        ZB_ENDDATE: this.basicTemplateFormQuery.date[1],
        pageMarginsOption: JSON.parse(this.basicTemplateFormQuery.activedPreview.elementCfg).pageMarginsOption
      })
      if (this.isSystemLookTemplateFlag == 1) {
        this.$emit('handleShowTemplateNewSystem', {
          row: this.basicTemplateFormQuery.activedPreview,
          config: templateObj
        })
        this.selectProductDialogVisible = false
      } else if (this.isSystemLookTemplateFlag == 2) {
        this.$emit('handleShowTemplateFromNewForEditor', {
          row: this.basicTemplateFormQuery.activedPreview,
          config: templateObj
        })
        this.selectProductDialogVisible = false
      } else {
        this.$emit('handleShowTemplateNew', {
          row: this.basicTemplateFormQuery.activedPreview,
          config: templateObj
        })
        this.selectProductDialogVisible = false
      }
    },

    // 触发时间选择 点击事件
    handleBasicTemplateTimeTypeClick() {

      // 如果选择了成立时间，需要判断用户是否点击了
      if (this.basicTemplateFormQuery.timeType == 'cd') {
        if (
          this.selectProductTableData.length == 0 ||
          this.selectProductTableData[0].createDate == '' ||
          this.selectProductTableData[0].createDate == undefined ||
          this.selectProductTableData[0].createDate == null
        ) {
          this.$message.closeAll()
          this.$message.warning('产品不能为空')
          this.basicTemplateFormQuery.timeType = 'self'
        } else {
          let end = moment().subtract(1, 'days').format('YYYY-MM-DD')
          end = this.selectProductTableData[0].gzLastDate!=''?moment(this.selectProductTableData[0].gzLastDate).format('YYYY-MM-DD'):end
          this.basicTemplateFormQuery.date = [this.selectProductTableData[0].createDate,end]
        }
      } else {
        if (this.basicTemplateFormQuery.timeType == 'm1') {
          let end = moment().subtract(1, 'days').format('YYYY-MM-DD')
          end = this.selectProductTableData[0].gzLastDate!=''?moment(this.selectProductTableData[0].gzLastDate).format('YYYY-MM-DD'):end
          let start = moment(moment(end).subtract(1, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
          let createTime="";
          if(this.selectProductTableData[0].createDate!="") {
             createTime = moment(this.selectProductTableData[0].createDate).format('YYYY-MM-DD')
            this.basicTemplateFormQuery.date = [moment(start).isAfter(createTime)===true?start:createTime, end]
          }else{
            this.basicTemplateFormQuery.date = [start, end]
          }

        } else if (this.basicTemplateFormQuery.timeType == 'm3') {
          let end = moment().subtract(1, 'days').format('YYYY-MM-DD')
          end = this.selectProductTableData[0].gzLastDate!=''?moment(this.selectProductTableData[0].gzLastDate).format('YYYY-MM-DD'):end
          let start = moment(moment(end).subtract(3, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
          let createTime="";
          if(this.selectProductTableData[0].createDate!="") {
            createTime = moment(this.selectProductTableData[0].createDate).format('YYYY-MM-DD')
            this.basicTemplateFormQuery.date = [moment(start).isAfter(createTime)===true?start:createTime, end]
          }else{
            this.basicTemplateFormQuery.date = [start, end]
          }
        } else if (this.basicTemplateFormQuery.timeType == 'm6') {
          let end = moment().subtract(1, 'days').format('YYYY-MM-DD')
          end = this.selectProductTableData[0].gzLastDate!=''?moment(this.selectProductTableData[0].gzLastDate).format('YYYY-MM-DD'):end
          let start = moment(moment(end).subtract(6, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
          let createTime="";
          if(this.selectProductTableData[0].createDate!="") {
            createTime = moment(this.selectProductTableData[0].createDate).format('YYYY-MM-DD')
            this.basicTemplateFormQuery.date = [moment(start).isAfter(createTime)===true?start:createTime, end]
          }else{
            this.basicTemplateFormQuery.date = [start, end]
          }
        } else if (this.basicTemplateFormQuery.timeType == 'y1') {
          let end = moment().subtract(1, 'days').format('YYYY-MM-DD')
          end = this.selectProductTableData[0].gzLastDate!=''?moment(this.selectProductTableData[0].gzLastDate).format('YYYY-MM-DD'):end
          let start = moment(moment(end).subtract(1, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
          let createTime="";
          if(this.selectProductTableData[0].createDate!="") {
            createTime = moment(this.selectProductTableData[0].createDate).format('YYYY-MM-DD')
            this.basicTemplateFormQuery.date = [moment(start).isAfter(createTime)===true?start:createTime, end]
          }else{
            this.basicTemplateFormQuery.date = [start, end]
          }
        } else if (this.basicTemplateFormQuery.timeType == 'yd') {
          let end = moment().subtract(1, 'days').format('YYYY-MM-DD')
          end = this.selectProductTableData[0].gzLastDate!=''?moment(this.selectProductTableData[0].gzLastDate).format('YYYY-MM-DD'):end
          let start = moment(end).year() + '-01-01'
          let createTime="";
          if(this.selectProductTableData[0].createDate!="") {
            createTime = moment(this.selectProductTableData[0].createDate).format('YYYY-MM-DD')
            this.basicTemplateFormQuery.date = [moment(start).isAfter(createTime)===true?start:createTime, end]
          }else{
            this.basicTemplateFormQuery.date = [start, end]
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
    // 新增 产品
    handleBasicTemplateAdd() {
      this.selectProductTableData.push({})
    },
    // 删除产品
    handleBasicTemplateDel(row) {
      if (this.selectProductTableData.length <= 2) {
        this.$message.closeAll()
        this.$message.warning('多产品类型产品数量至少有两个')
        return
      }
      const index = this.selectProductTableData.findIndex((item) => item._XID == row._XID)
      if (index !== -1) {
        this.selectProductTableData.splice(index, 1)
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
     // console.log('this.selectProductTableData', this.selectProductTableData)
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
    // 模板预览 下一步
    handlePreviewNextStep() {
      this.previewTemplateDialogVisible = false
      this.selectProductTableData = []
      // 判断是多产品还是单产品
      if (this.basicTemplateFormQuery.fundType == '1') {
        // 动态的做增减
        this.$set(this.selectProductTableData, this.selectProductTableData.length, {
          source: '',
          fundCode: '',
          fundName: '',
          createDate: '',
          gzLastDate:'',
        })
        this.basicTemplateFormQuery.activedPreview = this.previewOption.activedPreview
      } else {
        this.$set(this.selectProductTableData, this.selectProductTableData.length, {
          source: '',
          fundCode: '',
          fundName: '',
          createDate: '',
          gzLastDate:''
        })
        this.basicTemplateFormQuery.activedPreview = this.previewOption.activedPreview
      }
      this.selectProductDialogVisible = true

      // 赋初始值
      this.basicTemplateFormQuery.ZB_INDEXCODE = this.$store.state.indexArray[0].id
      this.basicTemplateFormQuery.ZB_INDEXCODEA = this.$store.state.compareIndexArray[0].id
      this.basicTemplateFormQuery.ZB_INDEXCODEB = this.$store.state.compareIndexArray[0].id
      this.basicTemplateFormQuery.ZB_INDEXWEIGHTA = '0'
      this.basicTemplateFormQuery.ZB_INDEXWEIGHTB = '0'
    },
    handlePreviewClick(item) {
      this.previewOption.activedPreview = item
    },
    // 保存模板
    handleSaveTemplate() {
      if (this.basicTemplateTitle == '编辑模板') {
        const params = {
          reportId: this.basicTemplateFormQuery.reportId || '',
          reportName: this.basicTemplateFormQuery.templateName || '',
          reportDesc: this.basicTemplateFormQuery.describe || ''
        }
        this.saveLoading = true
        pageApi
          .editTemplateReport(params)
          .then((res) => {
            this.saveLoading = false
            if (res.data.status === 200) {
              this.$message.closeAll()
              this.$message.success(res.data.message || '保存成功')
              this.basicTemplateDialogVisible = false
              this.getTemplateList()
            } else {
              this.$message.closeAll()
              this.$message.error(res.data.message || '保存失败')
            }
          })
          .catch((err) => {
            this.saveLoading = false
          })
      } else {
        // 创建模板
        this.$refs.basicTemplateDialog.validate(async (valid) => {
          if (valid) {
            // 跳转到下一步
            // 关闭当前dialog弹窗
            // 启动下一个弹窗
            this.previewOption.activedPreview = this.previewArray[0] || {}
            this.previewOption.reportType = this.basicTemplateFormQuery.reportType
            await this.getTemplateListForDialog()
            this.basicTemplateDialogVisible = false
            this.previewTemplateDialogVisible = true
            // 请求
          } else {
            this.$message.closeAll()
            this.$message.warning('请按照提示修改')
          }
        })
      }
    },
    // 新建模板
    handleCreateNewTemplate() {
      this.isSystemLookTemplateFlag = -1
      this.basicTemplateTitle = '新建模板'
      this.basicTemplateReportTypeStatus = true
      this.basicTemplateDialogVisible = true

      // 清空报告模板的basicTemplateFormQuery值
      for (const key in this.basicTemplateFormQuery) {
        if (key == 'timeType') {
          this.basicTemplateFormQuery[key] = 'self'
        } else {
          this.basicTemplateFormQuery[key] = ''
        }
      }
      this.basicTemplateFormQuery.fundType = '1'
    },
    /**
     * @description 动态设置表格高度
     */
    handleTableHeight() {
      this.$nextTick(() => {
        // 根据浏览器高度设置初始高度
        this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 125
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 125
        }
      })
    }
  }
}
</script>
<style lang="scss">
#template-management {
  .dialog-single-product {
    .el-dialog__body {
      overflow: visible !important;
    }
    width: 55% !important;
    .el-select--small {
      .el-input__icon {
        display: none;
      }
    }
    .el-input__inner {
      color: #333333 !important;
    }
    .el-radio__label {
      color: #333333 !important;
    }
  }
}
input[aria-hidden=true] {
  display: none !important;
}
</style>
<style lang="scss" scoped>
.templateselectdialog {
  .vxe-cell {
    height: 32px !important;
  }
}

.select-product-table-span {
  margin-top: 7px;
  height: 32px;
  line-height: 32px;
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

::v-deep .el-color-picker--small .el-color-picker__trigger {
  width: 80px;
}

.activated-preview {
  background-color: #e2a971;
}

.activated-preview-fontcolor {
  color: white;
}

#template-management {
  // padding: 10px 10px 10px 10px;
  overflow: auto;

  .basic-template-dialog {
  }

  .title-style {
    display: inline-block;
    color: #0f65dd;
    height: 35px;
    line-height: 35px;
    padding-left: 4px;
    font-size: 16px;
    //border-left: 4px solid #e03d3e;
    margin-bottom: 5px;
  }

  .el-form {
  }

  .tool {
    margin-top: 10px;
  }

  .infinite-box {
    height: 300px;
    padding: 10px;
    overflow: hidden;
  }

  .tool::after {
    content: '';
    clear: both;
    display: block;
    height: 0;
    visibility: hidden;
  }

  //.clearfix::after {
  //  content: '';
  //  clear: both;
  //  display: block;
  //  height: 0;
  //  visibility: hidden;
  //}

  .infinite-list-wrapper {
    height: 600px;
  }

  .color-box {
    display: inline-block;
    height: 30px;
    width: 2px;
    background-color: #0f65dd;
  }
}
</style>

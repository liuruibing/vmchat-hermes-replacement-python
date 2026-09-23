<template>
  <div class="asset-excess-return-analysis" v-auto-enter>
    <!-- 查询条件区域 -->
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form :inline="true" ref="formInline" :model="formInline" :rules="searchRules" class="form_inline_search standard-form">
          <el-form-item label="" prop="fundName">
<!--            <el-tooltip :content="formInline.fundName" :disabled="!formInline.fundName" effect="dark" placement="top-start">
              <el-input v-model="formInline.fundName" clearable placeholder="请选择产品" size="small" @click.native="openFundListDialog" />
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
<!--          <el-form-item label="" prop="beginDate">-->
<!--            <el-date-picker size="small" v-model="formInline.beginDate" :picker-options="dateShortTPCTA()" placeholder="请选择开始日期" type="date" value-format="yyyy-MM-dd" />-->
<!--          </el-form-item>-->
<!--          <el-form-item label="" prop="endDate">-->
<!--            <el-date-picker size="small" v-model="formInline.endDate" type="date" value-format="yyyy-MM-dd" placeholder="请选择结束日期" />-->
<!--          </el-form-item>-->
          <el-form-item>
            <el-button type="primary" size="small" icon="el-icon-search" @click="onSubmit('formInline')">查询</el-button>
            <el-button type="info" icon="el-icon-refresh-left" size="small" plain @click="resetForm('formInline')">重置</el-button>
<!--            <el-button type="primary" size="small" icon="el-icon-download" @click="exportData">导出</el-button>-->
            <el-button type="info" size="small" plain :icon="exportLoading ? 'el-icon-loading' : 'el-icon-download'" :disabled="isDisabled" @click="downloadTableExcel">
              {{ downLoadText }}
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>

    <!-- 表格区域 -->
    <div class="table-content" id="standard-table">
      <div id="standard-table-margin">
        <vxe-table
          ref="refsTable"
          v-loading="tableLoading"
          :cell-style="cellStyleMethod"
          :data="tableData"
          :height="tableHeight"
          auto-resize
          stripe
          sync-resize
          show-overflow="tooltip"
          style="width: 100%"
          :sort-config="{ remote: true }"
          @sort-change="customSortMethod"
          resizable
        >
          <template v-for="item in columns">
            <vxe-table-column :key="item.key" :field="item.prop" :title="item.label" :min-width="item.width" :align="item.align" header-align="center">
              <template slot-scope="scope">
                <span v-if="item.type === 'assetType'" :style="{ paddingLeft: scope.row.level > 1 ? '20px' : '0px' }">
                  {{ scope.row[item.prop] }}
                </span>
                <span v-else-if="item.type === 'percent'" :class="getValueClass(scope.row[item.prop], item.prop)">
                  {{ scope.row[item.prop] | numberToFixedStr(2, 100, '%') }}
                </span>
                <span v-else>{{ scope.row[item.prop] }}</span>
              </template>
            </vxe-table-column>
          </template>
        </vxe-table>
        <vxe-pager
          :current-page="formInline.pageNum"
          :page-size="formInline.pageSize"
          :total="total"
          :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
          border
          size="medium"
          class="standard-vxe-pager"
          @page-change="pagination"
        />
      </div>
    </div>

    <!-- 分页区域 -->
<!--    <div class="table-footer">
      <Pagination :total="total" :limit="formInline.pageSize" :page="formInline.pageNum" @pagination="pagination" />
    </div>-->
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
import Pagination from '@/components/Pagination'
import ToolBarSlot from '@/components/toolBarSlot'
import commonFun from '@/filters/common'
import selectApi from "@/api/fofAdvisorAnalysis/index"
import request from '@/utils/request'
import moment from 'moment'
import { downLoadFileByUrlPost } from '@/utils'
import productSelector from '@/components/productSelector'
import store from '../../store'
import ProductSelectInput from '@/components/productSelector/ProductSelectInput'

export default {
  name: 'AssetExcessReturnAnalysis',
  components: {
    Pagination,
    ToolBarSlot,
    productSelector,
    ProductSelectInput
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
      left:false,
      selectList: [],
      dialogMask: false,
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
      // 查询表单
      formInline: {
        product: null,
        ddate_: [],
        fundName:'',
        fundCode: '',
        beginDate: '',
        endDate: '',
        //period: 'month', // 默认选择月度
        //orderString: '',
        pageSize: 20,
        pageNum: 1
      },
      // FOF产品列表
      fundCodeList: [
        { value: '1', label: '点选' },
        { value: '2', label: '如稳进' },
        { value: '3', label: '稳健等' }
      ],
      // 表格高度
      tableHeight: 0,
      // 表格loading
      tableLoading: false,
      // 表格数据
      tableData: [],
      exportLoading: false,
      isDisabled: false,
      downLoadText: "导出",
      //成立日
      timDate: '',
      //最新的估值确认日期
      dateTime:'',
      searchRules: {
        // date: [{ required: true, trigger: "change", validator: validateDate }],
        //ddate_: [{required: true, message: "请选择日期", trigger: "change"}],
        // beginDate: [
        //   { required: true, message: '请选择开始日期', trigger: 'blur' },
        //   { validator: validatebeginDate, trigger: 'blur' }
        // ],
        // endDate: [
        //   { required: true, message: '请选择结束日期', trigger: 'blur' },
        //   { validator: validateEndDate, trigger: 'blur' }
        // ],
        fundName: [{ required: true, message: '请选择产品', trigger: 'change' }],
        ddate_: [
          {required: true, message: "请选择日期", trigger: "change"},
          {validator: validateRangeDate, trigger: 'blur' }
        ],
      },
      // 总条数
      total: 0,
      columns: [
        { key: 'assetType', prop: 'assetType', label: '资产类型', width: '120', align: 'left', type: 'assetType', sortable: true },
        { key: 'assetIndex', prop: 'assetIndex', label: '资产指数', width: '120', align: 'center', type: 'normal', sortable: true },
        { key: 'actualReturn', prop: 'actualReturn', label: '资产收益率', width: '120', align: 'right', type: 'percent', sortable: true },
        { key: 'benchmarkReturn', prop: 'benchmarkReturn', label: '基准收益率', width: '120', align: 'right', type: 'percent', sortable: true },
        { key: 'excessReturn', prop: 'excessReturn', label: '超额收益率', width: '120', align: 'right', type: 'percent', sortable: true }
      ]
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
    this.initData()
  },
  methods: {
    openFundListDialog() {
      /*this.productSelectorVisible = true*/
      this.dialogMask = true
    },
    handleDialogClosed() {
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
    handleSubmitClick(arr) {
      this.dialogMask = false
      this.formInline.fundCode = arr[0].VC_FUNDCODE || ''
      this.formInline.fundName = arr[0].VC_FUNDNAME || ''
      this.selectList = arr
      this.timDate = arr[0].D_CREATE_DATE || ''
      //估值最新确认日期
      this.initTimGzLastDate(arr[0].VC_FUNDCODE || '')
    },
    handleProductSelect: function(product) {
      this.fundCode = product.VC_FUNDCODE || ''
      this.formInline.fundCode = product.VC_FUNDCODE || ''
      this.formInline.fundName = product.VC_FUNDNAME || ''
      this.timDate = product.D_CREATE_DATE || ''
      //估值最新确认日期
      this.initTimGzLastDate(product.VC_FUNDCODE || '')
    },
    handleProductClear: function() {
      this.fundCode = ''
      this.formInline.fundCode = ''
      this.formInline.fundName =  ''
      this.timDate = ''
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
    /**
     * @description 初始化数据
     */
    initData() {
      // 动态设置表格高度
      this.handleTableHeight()
      // 查询表格（这里只是架子，不实现具体逻辑）
    //  this.handleSearchTable(true)
    },

    /**
     * @description 动态设置表格高度
     */
    handleTableHeight() {
      this.$nextTick(() => {
        // 根据浏览器高度设置初始高度
        this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 175
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 175
        }
      })
    },
    onSubmit(formName) {
      var self = this
      self.$refs[formName].validate((valid) => {
        if (valid) {
          try {
            self.handleSearchTable(true)
          } catch (e) {}
          // 禁用搜索按钮
          self.$fun.searchButtonDisabled('issearchFxButton', self)
        } else {
          return false
        }
      })
    },
    /**
     * @description 表格查询（示例架子，不实现具体逻辑）
     */
    handleSearchTable(flag) {
      this.tableLoading = true
      var self = this;
      if (flag) {
        this.formInline.pageNum = 1
      }
      this.formInline.beginDate=this.formInline.ddate_[0]
      this.formInline.endDate=this.formInline.ddate_[1]
      const params = Object.assign({}, this.formInline, {});
      new Promise((resolve, reject) => {
        selectApi
          .fun_selectFofAssetExcessReturnAnalysis(params)
          .then((res) => {
            const { status, data } = res;
            if (status === 0) {
              if (data != null && data != undefined) {
                  const { list, total } = data;
                  this.tableData = list;
                  this.total = total;
              }
            } else {
              self.$message({
                message: "系统异常",
                type: "warning"
              });
            }
            this.tableLoading = false;

          })
          .catch((error) => {
            this.tableLoading = false;
            reject(error);
          });
      });


    },
    // 导出
    downloadTableExcel() {
      this.downLoadText = "导出中...";
      this.exportLoading = true;
      this.isDisabled = true;
      this.formInline.beginDate=this.formInline.ddate_[0]
      this.formInline.endDate=this.formInline.ddate_[1]
      const params = Object.assign({}, this.formInline)
      const fileName = '大类资产超额收益分析.xlsx'
      const url = '/api/fofAdvisorAnalysis/select/export'
      downLoadFileByUrlPost(url, params, fileName, this)
      setTimeout(() => {
        this.exportLoading = false;
        this.isDisabled = false;
        this.downLoadText = "导出";
      }, 10000)
    },
    /**
     * @description 监听分页
     */
    pagination(val) {
      const { currentPage, pageSize } = val;
      // 起始页
      this.formInline.pageNum = currentPage;
      // 每页数量
      this.formInline.pageSize = pageSize;
      this.handleSearchTable(false)
    },

    /**
     * @description 排序方法
     */
    customSortMethod(val) {
      this.formInline.orderString = commonFun.queryOrderBy_vxe_template ? commonFun.queryOrderBy_vxe_template(val) : ''
      this.handleSearchTable(false)
    },

    /**
     * @description 单元格样式方法
     */
    cellStyleMethod({ row, column }) {
      let styles = { height: '50px' } //  为所有单元格设置基础高度

      if (column.property === 'actualReturn' || column.property === 'benchmarkReturn') {
        const value = row[column.property]
        if (value < 0) {
          styles.color = '#ff4d4f'
        }
      } else if (column.property === 'excessReturn') {
        const value = row[column.property]
        if (value > 0) {
          styles.color = '#ff4d4f' // 正值显示红色
        } else if (value < 0) {
          styles.color = '#52c41a' // 负值显示绿色
        }
      }
      return styles // 返回合并后的样式
    },

    /**
     * @description 处理周期变化
     */
    handlePeriodChange(period) {
      // 根据选择的周期更新日期范围
      const today = new Date()
      let beginDate = new Date()

      if (period === 'week') {
        // 设置为一周前
        beginDate.setDate(today.getDate() - 7)
      } else if (period === 'month') {
        // 设置为一个月前
        beginDate.setMonth(today.getMonth() - 1)
      } else if (period === 'ytd') {
        // 设置为今年1月1日
        beginDate = new Date(today.getFullYear(), 0, 1)
      }

      this.formInline.beginDate = this.formatDate(beginDate)
      this.formInline.endDate = this.formatDate(today)

      // 查询数据
      this.handleSearchTable(true)
    },

    /**
     * @description 格式化日期为 yyyy-MM-dd
     */
    formatDate(date) {
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },

    /**
     * @description 导出数据（示例架子，不实现具体逻辑）
     */
    exportData() {
      this.$message.success('导出功能尚未实现')
    },

    /**
     * @description 重置表单
     */
    resetForm(formName) {
      var self = this
      self.$refs[formName].resetFields()
      this.formInline.fundCode = ''
      this.formInline.fundName = ''
      // 保持当前选择的周期不变
      // 重置后自动查询
     // this.handleSearchTable(true)
    },

    beforeDestroy() {
      // 组件销毁移除监听事件
      window.onresize = null
    },

    getValueClass(value, prop) {
      if (prop === 'actualReturn' || prop === 'benchmarkReturn') {
        return value < 0 ? 'negative-value' : ''
      } else if (prop === 'excessReturn') {
        if (value > 0) return 'positive-value'
        else if (value < 0) return 'negative-value'
        return ''
      }
      return ''
    }
  }
}
</script>

<style lang="scss" scoped>
.asset-excess-return-analysis {
  // padding: 10px 15px;
  //margin-bottom: 40px;
  .search-content {
    //background-color: #f7f7f7;
    ::v-deep .el-input.el-input--small .el-input__inner {
      background-color: #f7f7f7;
    }
    ::v-deep .el-form--inline .el-form-item {
      margin-bottom: 0px !important;
    }
  }
  .operate-btn {
    ::v-deep .el-button.el-button--small {
      margin-left: 16px !important;
    }
    ::v-deep .el-button.el-button--info {
      font-weight: bold;
    }
    ::v-deep .el-button.el-button--info:hover {
      font-weight: bold;
    }
  }
  ::v-deep .el-dialog__wrapper .el-dialog__header span {
    color: #333 !important;
  }
  ::v-deep .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
}
</style>

<template>
  <div class="private-product" v-auto-enter>
    <div class="standard-form-margin">
      <div class="inner-margin">
      <el-form ref="formInline" :inline="true" :model="formInline" class="standard-form analyse-page">
        <el-row>
          <el-col :span="24">
            <el-form-item label="">
              <el-input v-model="formInline.fundCode" size="small" placeholder="请输入产品代码"></el-input>
            </el-form-item>
            <el-form-item label="">
              <el-input v-model="formInline.fundName" size="small" placeholder="请输入产品名称"></el-input>
            </el-form-item>
            <el-form-item label="">
              <el-select v-model="formInline.investStrategy" size="small" clearable filterable placeholder="请选择策略类型">
                <el-option v-for="item in investOptions" :key="item.DIMCDE" :label="item.DIMNME" :value="item.DIMCDE" />
              </el-select>
            </el-form-item>
            <el-form-item label="">
              <el-select v-model="formInline.typeDetail2" size="small" clearable filterable placeholder="请选择子策略类型">
                <el-option v-for="item in investDetailOptions" :key="item.DIMCDE" :label="item.DIMNME" :value="item.DIMCDE" />
              </el-select>
            </el-form-item>
            <el-form-item label="">
              <el-select v-model="formInline.typeIn" size="small" clearable filterable placeholder="请选择产品类型">
                <el-option v-for="item in typeInOptions" :key="item.DIMCDE" :label="item.DIMNME" :value="item.DIMCDE" />
              </el-select>
            </el-form-item>
            <el-form-item label="">
              <el-select v-model="formInline.typeDetail" size="small" clearable filterable placeholder="请选择产品明细类型">
                <el-option v-for="item in typeDetailOptions" :key="item.DIMCDE" :label="item.DIMNME" :value="item.DIMCDE" />
              </el-select>
            </el-form-item>
            <el-form-item label="">
              <el-input v-model="formInline.nameGlr" size="small" placeholder="请输入管理人"></el-input>
            </el-form-item>
            <el-form-item label="">
              <el-date-picker
                v-model="formInline.date"
                end-placeholder="成立结束日期"
                range-separator="至"
                size="small"
                start-placeholder="成立开始日期"
                type="daterange"
                value-format="yyyy-MM-dd"
              ></el-date-picker>
            </el-form-item>
            <el-form-item >
              <el-button type="primary" size="small" icon="el-icon-search" @click="handleSearchTable">查询</el-button>
              <el-button :disabled="isDisabled" :loading="exportLoading" type="info" plain size="small" @click="exportTable">
                <i class="el-icon-download"></i>
                {{ downLoadText }}
              </el-button>
            </el-form-item>



          </el-col>
        </el-row>
      </el-form>
    </div>
      </div>

    <el-row id="standard-table">
      <div id="standard-table-margin">
        <el-col>
      <vxe-table
        v-loading="tableLoading"
        ref="refsTable"
        :cell-style="{ height: '50px' }"
        :height="tableHeight"
        resizable
        :data="tableData"
        auto-resize
        stripe
        sync-resize
        show-overflow="tooltip"
        style="width: 100%"
      >
        <vxe-table-column
          v-for="item in column"
          :key="item.prop"
          :align="item.align"
          :field="item.prop"
          :show-overflow-tooltip="item.showtooltip"
          :title="item.label"
          :min-width="item.width"
          header-align="center"
        >
          <template slot-scope="scope">
            <span v-if="item.prop === 'gzFrequency'">
              <span>{{ scope.row[item.prop] | frequencyFilter(that) }}</span>
            </span>
            <span v-else>{{ scope.row[item.prop] | noDataFilter }}</span>
          </template>
        </vxe-table-column>
      </vxe-table>
<!--          <Pagination :total="total" :limit="pageList._pageSize" :page="pageList._pageNum" @pagination="pagination" />-->
          <vxe-pager
            :current-page="pageList._pageNum"
            :page-size="pageList._pageSize"
            :total="total"
            :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
            border
            size="medium"
            @page-change="pagination"
          />
        </el-col>
      </div>
    </el-row>
  </div>
</template>

<script>
import { TABLE_COLUMNS } from './scripts/constants'
import Pagination from '@/components/Pagination'
import commonApi from '@/api/common'
import { queryTableList } from './scripts/api'
import { gzFrequencyOptions } from '@/dataDictionary/frequency'
import { downLoadFileByUrl } from '@/utils'
export default {
  name: 'MyGroup',
  components: {
    Pagination
  },
  filters: {
    frequencyFilter(val, that) {
      const obj = that.gzFrequencyOptions.find((item) => item.value === val)
      return obj && obj.label
    }
  },
  data() {
    return {
      that: this,
      downLoadText: '导出',
      exportLoading: false,
      isDisabled: false,
      // 表单数据绑定
      formInline: {
        fundCode: '',
        fundName: '',
        investStrategy: '',
        typeDetail2: '',
        typeIn: '',
        typeDetail: '',
        nameGlr: '',
        date: []
      },
      // 表格动态高度
      tableHeight: 0,
      // 表格加载状态
      tableLoading: false,
      // 表格数据
      tableData: [],
      // 表格列
      column: TABLE_COLUMNS,
      // 策略类型下拉
      investOptions: [],
      // 子策略类型下拉
      investDetailOptions: [],
      // 产品类型下拉
      typeInOptions: [],
      // 产品类型明细下拉
      typeDetailOptions: [],
      // 净值披露频率字典
      gzFrequencyOptions,
      // 分页信息绑定
      pageList: {
        _pageSize: 10,
        _pageNum: 1,
        _pageFlag: true
      },
      // 总条数
      total: 0
    }
  },
  watch: {
    '$route.query.list': {
      handler(val) {
        if (this.$store.getters.fromPageJump) {
          if (val && val.VC_FUNDNAME) {
            console.log(val, '>>')
            this.formInline.fundName = val.VC_FUNDNAME
            this.handleSearchTable()
          } else {
            this.handleSearchTable()
          }
          this.$store.commit('SET_FROMPAGEJUMP', false)
        }
      },
      deep: true,
      immediate: true
    }
  },
  mounted() {
    this.initData()
  },
  beforeDestroy() {
    // 组件销毁移除监听事件
    window.onresize = null
  },
  methods: {
    // 导出
    exportTable() {
      const params = Object.assign({}, this.formInline)
      if (this.formInline.date && this.formInline.date.length) {
        params.createDate = this.formInline.date[0]
        params.createDate2 = this.formInline.date[1]
      } else {
        params.createDate = ''
        params.createDate2 = ''
      }
      params.flag = 'B'
      delete params.limit
      delete params.offset
      delete params.date
      const data = this.parameterSrc(params)
      const url = '/api/afterManage/export'
      const fileName = '产品信息列表.xlsx'
      this.exportLoading = true
      this.isDisabled = true
      this.downLoadText = '导出中'
      downLoadFileByUrl(url, params, fileName, this)
    },
    /**
     * @description 初始化调用
     */
    initData() {
      // 动态设置表格高度
      this.handleTableHeight()
      // 查询表格
      this.handleSearchTable()
      // 初始化下拉查询
      this.getDimOptions()
    },
    /**
     * @description 查询一级策略下拉
     */
    getDimOptions() {
      const params = {
        indexCode: 'a9d3e3c3-b5be-414a-90d9-312b5fc1948d'
      }
      commonApi.getDataBysqlCode(params).then((res) => {
        if (res.data.status === 0) {
          const resutData = res.data.data || []
          if (resutData && resutData.length) {
            this.investOptions = resutData.filter((item) => item.DIMTYPE === 'strategy_type')
            this.investDetailOptions = resutData.filter((item) => item.DIMTYPE === 'fundinvesttype')
            this.typeInOptions = resutData.filter((item) => item.DIMTYPE === 'ftypein')
            this.typeDetailOptions = resutData.filter((item) => item.DIMTYPE === 'VCTYPEDETAIL')
          }
        }
      })
    },
    /**
     * @description 动态设置表格高度
     */
    handleTableHeight() {
      this.$nextTick(() => {
        // 根据浏览器高度设置初始高度
        this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 280
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 280
        }
      })
    },
    /**
     * @description 监听分页
     */
    pagination(val) {
      const { currentPage, pageSize } = val;
      // 起始页
      this.pageList._pageNum = currentPage;
      // 每页数量
      this.pageList._pageSize = pageSize;
      /* const { page, limit } = val
      this.pageList._pageNum = page
      this.pageList._pageSize = limit */
      this.handleSearchTable()
    },
    /**
     * @description 去除无值字段，包含数组
     */
    parameterSrc(data) {
      const newData = {}
      for (const key in data) {
        if (data[key] === '' || data[key] === undefined || data[key] === null || JSON.stringify(data[key]) === '[]') {
        } else {
          newData[key] = data[key]
        }
      }
      return newData
    },
    /**
     * @description 表格数据查询
     */
    handleSearchTable() {
      const params = Object.assign({}, this.formInline)
      if (this.formInline.date && this.formInline.date.length) {
        params.createDate = this.formInline.date[0]
        params.createDate2 = this.formInline.date[1]
      } else {
        params.createDate = ''
        params.createDate2 = ''
      }
      params.flag = 'B'
      params.limit = this.pageList._pageSize
      params.offset = (this.pageList._pageNum - 1) * this.pageList._pageSize
      delete params.date
      const data = this.parameterSrc(params)
      this.tableLoading = true
      queryTableList(data)
        .then((res) => {
          if (res.data.status === 0) {
            this.tableData = res.data.data.rows || []
            this.total = res.data.data.total || 0
            this.tableLoading = false
          } else {
            this.tableLoading = false
            this.$message.error(res.data.message || '查询失败')
          }
        })
        .catch((e) => {
          this.tableLoading = false
        })
    }
  }
}
</script>

<style lang="scss" scoped>
.my-group {
 // padding-left: 10px;
  .search-bar {
    margin-top: 12px;
    // border-bottom: 1px solid #e1e0e0;
    margin-bottom: 8px;
  }
  ::v-deep .el-form-item {
    margin-bottom: 0px !important;
  }

  .color-box {
    display: inline-block;
    height: 30px;
    width: 2px;
    background-color: #0F65DD;
  }

  .title-style {
    color: #0F65DD;
    vertical-align: middle;
    height: 35px;
    line-height: 35px;
    font-size: 16px;
    margin-left: 5px;
    display: inline-block;
  }
  ::v-deep .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
  ::v-deep .el-button.el-button--mini {
    padding: 7.5px;
  }
}
</style>

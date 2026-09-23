<template>
  <div class="product-info">
    <div class="search-content">
      <el-row>
        <el-form ref="searchForm" :inline="true" :model="simpleSearch" :rules="rules">
          <el-row type="flex" justify="start">
            <el-form-item label="" prop="endDate">
              <el-date-picker v-model="simpleSearch.endDate" :clearable="false" type="date" value-format="yyyy-MM-dd" placeholder="截止日期" size="small" />
            </el-form-item>
            <el-form-item class="tzcl" label="">
              <el-select v-model="simpleSearch.types" multiple collapse-tags clearable placeholder="投资策略" size="small">
                <el-option v-for="item in investStrategy" :key="item.id + 'invest'" :label="item.label" :value="item.id"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" size="small" @click="handleQueryParams">
                查询
              </el-button>
              <el-button type="info" size="small" plain @click="reset" icon="el-icon-refresh">重置</el-button>
            </el-form-item>
          </el-row>
        </el-form>
      </el-row>
    </div>
    <product-table
      :table-data="tableData"
      :table-loading="tableLoading"
      :export-loading="exportLoading"
      :is-disabled="isDisabled"
      @updatelist="updatelist"
      @sorttable="handleSortTable"
      @excelexport="handleExcelExport"
    ></product-table>
    <Pagination :limit="pageList._pageSize" :page="pageList._pageNum" :total="total" @pagination="pagination" />
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import request from '@/utils/request'
import ProductTable from './product-info-core/product-table.vue'
import { findList } from './product-info-core/scripts/api'
import { downLoadFileByUrl } from '@/utils'
export default {
  components: {
    ProductTable,
    Pagination
  },
  data() {
    return {
      simpleSearch: {
        endDate: '',
        types: []
      },
      pageList: {
        _pageNum: 1,
        _pageSize: 20
      },
      total: 0,
      investStrategy: [],
      tableData: [],
      tableLoading: false,
      exportLoading: false,
      isDisabled: false,
      orderList: {
        orderString: 'm3_return desc'
      },
      managerCode: '',
      rules: {
        endDate: [{ type: 'string', required: true, message: '请选择截止日期', trigger: 'change' }]
      }
    }
  },
  watch: {
    managerCode: {
      async handler(val) {
        if (val) {
          await this.getEndDate()
          await this.getInvestStrategyList()
          this.handleQueryParams()
        } else {
          this.tableData = []
          this.total = 0
        }
      }
    }
  },
  methods: {
    /**
     * @description 获取投资策略数据
     */
    getInvestStrategyList() {
      return new Promise((resolve, reject) => {
        request({
          url: `/api/report/v1.0/data/sql/b4923f1f-46a9-42f0-aff3-403cb6fb26bf`,
          method: 'post',
          data: {
            indexCode: 'b4923f1f-46a9-42f0-aff3-403cb6fb26bf'
          }
        })
          .then(res => {
            if (res.data.status === 0) {
              const resultDim = res.data.data || []
              this.investStrategy = resultDim.map(item => {
                return {
                  label: item.DIM_NME,
                  id: item.DIM_CDE
                }
              })
              resolve()
            }
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    /**
     * @description 获取截止日期
     */
    getEndDate() {
      return new Promise((resolve, reject) => {
        const params = {
          indexCode: 'bc4ab85f-fb95-449a-948e-a3bb49227850'
        }
        request({
          url: `/api/report/v1.0/data/sql/bc4ab85f-fb95-449a-948e-a3bb49227850`,
          method: 'post',
          data: params
        })
          .then(res => {
            if (res.data.status === 0) {
              this.simpleSearch.endDate = res.data.data[0].D_DATE
              resolve()
            }
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    /**
     * @description 关注完刷新列表
     */
    updatelist() {
      this.handleQueryParams()
    },
    /**
     * @description 设置排序字段
     */
    handleSortTable(val) {
      this.orderList.orderString = this.$fun.queryOrderBy_vxe_template(val)
      this.handleQueryParams()
    },
    /**
     * @description 表格导出
     */
    handleExcelExport() {
      // 获取当前查询条件
      let params = this.handleQueryParams('NO_QUERY')
      params = this.parameterSrc(params)
      console.log(params, '>>')
      const fileName = '管理人详情（旗下产品）-导出.xls'
      const url = 'api/fund2/export'
      this.exportLoading = true
      this.isDisabled = true
      downLoadFileByUrl(url, params, fileName, this)
    },
    /**
     * @description 监听分页
     */
    pagination(val) {
      const { page, limit } = val
      this.pageList._pageNum = page
      this.pageList._pageSize = limit
      this.handleQueryParams()
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
     * @description 查询参数配置
     */
    handleQueryParams(status) {
      // 基本查询条件
      const params = Object.assign(
        {},
        {
          ...this.simpleSearch,
          ...this.orderList
        }
      )
      // 分页计算
      params.limit = this.pageList._pageSize
      params.offset = (this.pageList._pageNum - 1) * this.pageList._pageSize
      params.company_id = this.managerCode || ''

      if (status === 'NO_QUERY') {
        return params
      } else {
        this.handleFindList(params)
      }
    },
    /**
     * @description 查询
     */
    handleFindList(params) {
      const data = this.parameterSrc(params)
      this.$refs.searchForm.validate(async valid => {
        if (valid) {
          this.tableLoading = true
          try {
            const res = await findList(data)
            if (res.data.status === 0) {
              this.tableData = res.data.data.rows || []
              this.total = res.data.data.total || 0
              this.tableLoading = false
            } else {
              this.$message({
                type: 'error',
                message: res.message
              })
            }
          } catch (e) {
            this.tableLoading = false
          }
        } else {
          return false
        }
      })
    },
    /**
     * @description 重置
     */
    reset() {
      this.simpleSearch.endDate = ''
      this.simpleSearch.types = []
      this.pageList._pageNum = 1
    }
  }
}
</script>

<style lang="scss" scoped>
.product-info {
  overflow: auto;
  padding: 15px;
  .search-content {
    width: 100%;
    .tzcl {
      ::v-deep .el-select .el-input--small {
        width: 200px !important;
      }
      ::v-deep .el-select .el-select__tags {
        max-width: 174px !important;
      }
    }
  }
}
</style>

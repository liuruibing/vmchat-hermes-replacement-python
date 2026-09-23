<template>
  <div id="dd-query-manager">
    <div class="funds-filter">
      <div class="funds-filter-search">
        <div class="funds-search-simple">
          <el-form ref="searchForm" :inline="true" :model="simpleSearch" :rules="rules" class="standard-form">
            <el-form-item label="管理人名称">
              <el-input v-model="simpleSearch.manager_name" placeholder="管理人名称/拼音首字母" size="small" style="width: 180px !important;" />
            </el-form-item>
            <el-form-item label="管理规模区间">
              <el-select v-model="simpleSearch.asset_list" placeholder="" size="small" clearable multiple collapse-tags @change="checkBoxfile">
                <el-checkbox
                  v-model="isBx"
                  :disabled="simpleSearch.asset_list.includes('不限')"
                  style="display: inline-block; margin-left: 20px; padding: 3px 0"
                  @change="bxChange"
                >
                  不限
                </el-checkbox>
                <el-option v-for="item in orzScaleOptions" :key="item.value" :label="item.label" :value="item.value" style="font-size: 14px !important"></el-option>
              </el-select>
            </el-form-item>
            <div style="display: inline-block">
              <el-form-item label="截止日期" prop="endDate">
                <el-date-picker v-model="simpleSearch.endDate" type="date" value-format="yyyy-MM-dd" placeholder="选择日期" size="small" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" size="small" icon="el-icon-search" @click="handleQueryParams">查询</el-button>
                <el-button type="info" plain size="small" icon="el-icon-refresh-left" @click="reset">重置</el-button>
                <el-button type="primary" size="small" @click="showMoreQuery">
                  <span>{{ isShowMoreQuery ? '收起筛选' : '展开筛选' }}</span>
                  <i :class="isShowMoreQuery ? 'el-icon-caret-top' : 'el-icon-caret-bottom'" />
                </el-button>
              </el-form-item>
            </div>
          </el-form>
        </div>
      </div>
      <transition name="fade">
        <div v-show="isShowMoreQuery">
          <ManagerQuery
            ref="ManagerQuery"
            :sql-obj="{
              company: '5122c4e4-6672-479c-978e-a8172e2a50f5',
              invest: '843183f5-b322-4e2d-a048-86fa4d66c870'
            }"
            @updateSelect="getDynamicData"
          />
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import request from '@/utils/request'
import Constant from '../scripts/constant'
import ManagerQuery from './moreQuery'
import { findList } from '../scripts/api'
import defaultCts from '../scripts/constant'
export default {
  name: 'ManagerSearch',
  components: {
    ManagerQuery
  },
  props: {
    currentGroupId: {
      type: String,
      default: ''
    },
    pageList: {
      type: Object,
      default: () => {}
    },
    tableLoading: {
      type: Boolean,
      default: false
    },
    orderList: {
      type: Object,
      default: () => {
        return {
          orderString: ''
        }
      }
    }
  },
  data() {
    return {
      simpleSearch: {
        manager_name: '',
        asset_list: ['不限'],
        endDate: ''
      },
      orzScaleOptions: Constant.orzScaleOptions,
      isShowMoreQuery: false,
      isBx: true,
      managerData: [],
      rules: {
        endDate: [{ type: 'string', required: true, message: '请选择截止日期', trigger: 'change' }]
      }
    }
  },
  watch: {
    currentGroupId: {
      handler(val) {
        this.simpleSearch.poolCode = val
        this.handleQueryParams()
      },
      immediate: true
    }
  },
  async mounted() {
    await this.getEndDate()
    this.handleQueryParams()
  },
  methods: {
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
          .then((res) => {
            if (res.data.status === 0) {
              this.simpleSearch.endDate = res.data.data[0].D_DATE
              resolve()
            }
          })
          .catch((err) => {
            reject(err)
          })
      })
    },
    /**
     * @description 获取params信息
     */
    getParamsObject() {
      // 基本查询条件
      const params = Object.assign(
        {},
        {
          ...this.simpleSearch,
          ...this.orderList
        }
      )
      // 机构规模不限则传空
      params.asset_list = this.simpleSearch.asset_list.includes('不限') ? [] : this.simpleSearch.asset_list

      const companyChecked = defaultCts.companyState
        .filter((item) => {
          if (item.checked) {
            return item
          }
        })
        .map((it) => {
          return it.id + '，'
        })
        .join('，')
      params.company_status_list = companyChecked.split('，').slice(0, -1)

      this.managerData.forEach((item) => {
        // 公司类型
        if (item.id === '1') {
          params.company_type_list = item.code.split('，').slice(0, -1)
        }
        // 公司状态
        if (item.id === '2') {
          params.company_status_list = item.code.split('，').slice(0, -1)
        }
        // 备案状态
        if (item.id === '3') {
          params.record_status_list = item.code.split('，').slice(0, -1)
        }
        // 策略类型
        if (item.id === '4') {
          params.policy_type_list = item.code
        }
        // 成立时间
        if (item.id === '6') {
          params.company_founddate_b = item.start || ''
          params.company_founddate_e = item.end || ''
        }
        // 产品数量
        if (item.id === '7') {
          params.fund_count_b = item.start || ''
          params.fund_count_e = item.end || ''
        }
        // 近六月
        if (item.id === '近六月10') {
          params.m6_return_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.m6_return_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        if (item.id === '近六月11') {
          params.m6_max_retracement_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.m6_max_retracement_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        if (item.id === '近六月12') {
          params.m6_sharp_b = item.start !== '' ? Number(item.start) : ''
          params.m6_sharp_e = item.end !== '' ? Number(item.end) : ''
        }
        if (item.id === '近六月13') {
          params.m6_tre_b = item.start !== '' ? Number(item.start) : ''
          params.m6_tre_e = item.end !== '' ? Number(item.end) : ''
        }
        if (item.id === '近六月14') {
          params.m6_alpha_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.m6_alpha_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        // 近一年
        if (item.id === '近一年10') {
          params.y1_return_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.y1_return_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        if (item.id === '近一年11') {
          params.y1_max_retracement_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.y1_max_retracement_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        if (item.id === '近一年12') {
          params.y1_sharp_b = item.start !== '' ? Number(item.start) : ''
          params.y1_sharp_e = item.end !== '' ? Number(item.end) : ''
        }
        if (item.id === '近一年13') {
          params.y1_tre_b = item.start !== '' ? Number(item.start) : ''
          params.y1_tre_e = item.end !== '' ? Number(item.end) : ''
        }
        if (item.id === '近一年14') {
          params.y1_alpha_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.y1_alpha_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        // 今年以来
        if (item.id === '今年以来10') {
          params.ytd_return_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.ytd_return_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        if (item.id === '今年以来11') {
          params.ytd_max_retracement_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.ytd_max_retracement_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        if (item.id === '今年以来12') {
          params.ytd_sharp_b = item.start !== '' ? Number(item.start) : ''
          params.ytd_sharp_e = item.end !== '' ? Number(item.end) : ''
        }
        if (item.id === '今年以来13') {
          params.ytd_tre_b = item.start !== '' ? Number(item.start) : ''
          params.ytd_tre_e = item.end !== '' ? Number(item.end) : ''
        }
        if (item.id === '今年以来14') {
          params.ytd_alpha_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.ytd_alpha_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        // 成立以来
        if (item.id === '成立以来10') {
          params.total_return_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.total_return_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        if (item.id === '成立以来11') {
          params.total_max_retracement_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.total_max_retracement_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        if (item.id === '成立以来12') {
          params.total_sharp_b = item.start !== '' ? Number(item.start) : ''
          params.total_sharp_e = item.end !== '' ? Number(item.end) : ''
        }
        if (item.id === '成立以来13') {
          params.total_tre_b = item.start !== '' ? Number(item.start) : ''
          params.total_tre_e = item.end !== '' ? Number(item.end) : ''
        }
        if (item.id === '成立以来14') {
          params.total_alpha_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.total_alpha_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
      })
      return params
    },
    /**
     * @description 监听机构管理规模下拉
     */
    checkBoxfile(val) {
      if (!val.length) {
        this.isBx = true
        this.simpleSearch.asset_list = ['不限']
      } else {
        this.isBx = false
        const index = this.simpleSearch.asset_list.findIndex((item) => item === '不限')
        if (index > -1) {
          this.simpleSearch.asset_list.splice(index, 1)
        }
      }
    },
    /**
     * @description 监听机构管理规模下拉不限
     */
    bxChange(val) {
      if (val) {
        this.simpleSearch.asset_list = ['不限']
      }
    },
    /**
     * @description 是否展示更多查询
     */
    showMoreQuery() {
      this.isShowMoreQuery = !this.isShowMoreQuery
      this.$emit('updateheight')
    },
    /**
     * @description 重置所有查询
     */
    reset() {
      // 清空基础查询
      for (const key in this.simpleSearch) {
        this.simpleSearch[key] = ''
      }
      this.simpleSearch.asset_list = ['不限']
      this.simpleSearch.poolCode = this.currentGroupId

      // 清空子组件
      this.$refs.ManagerQuery.reset()
      // 重置分页
      this.$emit('resetPage')
    },
    /**
     * @description 获取子组件已选条件
     */
    getDynamicData(val) {
      this.managerData = val.query
    },
    /**
     * @description 查询参数
     */
    handleQueryParams() {
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
      // 机构规模不限则传空
      params.asset_list = this.simpleSearch.asset_list.includes('不限') ? [] : this.simpleSearch.asset_list

      const companyChecked = defaultCts.companyState
        .filter((item) => {
          if (item.checked) {
            return item
          }
        })
        .map((it) => {
          return it.id + '，'
        })
        .join('，')
      params.company_status_list = companyChecked.split('，').slice(0, -1)

      this.managerData.forEach((item) => {
        // 公司类型
        if (item.id === '1') {
          params.company_type_list = item.code.split('，').slice(0, -1)
        }
        // 公司状态
        if (item.id === '2') {
          params.company_status_list = item.code.split('，').slice(0, -1)
        }
        // 备案状态
        if (item.id === '3') {
          params.record_status_list = item.code.split('，').slice(0, -1)
        }
        // 策略类型
        if (item.id === '4') {
          params.policy_type_list = item.code
        }
        // 成立时间
        if (item.id === '6') {
          params.company_founddate_b = item.start || ''
          params.company_founddate_e = item.end || ''
        }
        // 产品数量
        if (item.id === '7') {
          params.fund_count_b = item.start || ''
          params.fund_count_e = item.end || ''
        }
        // 近六月
        if (item.id === '近六月10') {
          params.m6_return_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.m6_return_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        if (item.id === '近六月11') {
          params.m6_max_retracement_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.m6_max_retracement_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        if (item.id === '近六月12') {
          params.m6_sharp_b = item.start !== '' ? Number(item.start) : ''
          params.m6_sharp_e = item.end !== '' ? Number(item.end) : ''
        }
        if (item.id === '近六月13') {
          params.m6_tre_b = item.start !== '' ? Number(item.start) : ''
          params.m6_tre_e = item.end !== '' ? Number(item.end) : ''
        }
        if (item.id === '近六月14') {
          params.m6_alpha_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.m6_alpha_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        // 近一年
        if (item.id === '近一年10') {
          params.y1_return_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.y1_return_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        if (item.id === '近一年11') {
          params.y1_max_retracement_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.y1_max_retracement_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        if (item.id === '近一年12') {
          params.y1_sharp_b = item.start !== '' ? Number(item.start) : ''
          params.y1_sharp_e = item.end !== '' ? Number(item.end) : ''
        }
        if (item.id === '近一年13') {
          params.y1_tre_b = item.start !== '' ? Number(item.start) : ''
          params.y1_tre_e = item.end !== '' ? Number(item.end) : ''
        }
        if (item.id === '近一年14') {
          params.y1_alpha_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.y1_alpha_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        // 今年以来
        if (item.id === '今年以来10') {
          params.ytd_return_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.ytd_return_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        if (item.id === '今年以来11') {
          params.ytd_max_retracement_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.ytd_max_retracement_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        if (item.id === '今年以来12') {
          params.ytd_sharp_b = item.start !== '' ? Number(item.start) : ''
          params.ytd_sharp_e = item.end !== '' ? Number(item.end) : ''
        }
        if (item.id === '今年以来13') {
          params.ytd_tre_b = item.start !== '' ? Number(item.start) : ''
          params.ytd_tre_e = item.end !== '' ? Number(item.end) : ''
        }
        if (item.id === '今年以来14') {
          params.ytd_alpha_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.ytd_alpha_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        // 成立以来
        if (item.id === '成立以来10') {
          params.total_return_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.total_return_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        if (item.id === '成立以来11') {
          params.total_max_retracement_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.total_max_retracement_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        if (item.id === '成立以来12') {
          params.total_sharp_b = item.start !== '' ? Number(item.start) : ''
          params.total_sharp_e = item.end !== '' ? Number(item.end) : ''
        }
        if (item.id === '成立以来13') {
          params.total_tre_b = item.start !== '' ? Number(item.start) : ''
          params.total_tre_e = item.end !== '' ? Number(item.end) : ''
        }
        if (item.id === '成立以来14') {
          params.total_alpha_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.total_alpha_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
      })
      this.handleFindList(params)
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
     * @description 查询
     */
    async handleFindList(params) {
      const data = this.parameterSrc(params)
      if (this.$refs.searchForm) {
        this.$refs.searchForm.validate(async (valid) => {
          if (valid) {
            this.$emit('updateLoading', true)
            try {
              const res = await findList(data)
              if (res.data.status === 0) {
                this.$emit('updateTable', res.data.data)
                this.$emit('updateLoading', false)
              }
            } catch (e) {
              this.$emit('updateLoading', false)
            }
          } else {
            return false
          }
        })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
#dd-query-manager {
  .funds-filter {
    width: 100%;
    .funds-filter-search {
      //border-bottom: 1px solid #e1e0e0;
    }
  }
  .searchRight {
    ::v-deep .el-radio {
      margin-right: 5px;
    }
    ::v-deep .el-radio__input.is-checked .el-radio__inner {
      border-color: #e03d3e;
      background: #e03d3e;
    }
    ::v-deep .el-radio__input.is-checked + .el-radio__label {
      color: #333;
    }
  }

  // elementUI样式穿透
  // ::v-deep .el-button.el-button--primary {
  //   background-color: #e03d3e;
  //   border-color: transparent;
  // }
  // ::v-deep .el-button.el-button--info {
  //   color: #333;
  //   background-color: #dddddd;
  //   border-color: #dddddd;
  // }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.1s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>

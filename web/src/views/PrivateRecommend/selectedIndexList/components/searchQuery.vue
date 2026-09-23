<template>
  <div class="dd-query">
    <div class="funds-filter">
      <div class="funds-filter-search">
        <el-row>
          <el-form :inline="true" :model="simpleSearch" class="standard-form">
            <el-form-item label="">
              <el-input v-model="simpleSearch.fundName" placeholder="产品简称/拼音首字母/产品代码" size="small" style="width: 240px !important;" />
            </el-form-item>
            <el-form-item label="">
              <el-input v-model="simpleSearch.managerName" placeholder="管理人简称/拼音首字母" size="small" />
            </el-form-item>
            <el-form-item label="">
              <el-select v-model="simpleSearch.rankDate" placeholder="产品入选日期" size="small" clearable>
                <el-option v-for="item in rankTimeList" :key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="">
              <el-date-picker v-model="simpleSearch.navDate" :clearable="false" type="date" value-format="yyyy-MM-dd" placeholder="净值截止日期" size="small" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" size="small" @click="handleQueryList" icon="el-icon-search">查询</el-button>
              <el-button type="info" plain size="small" @click="reset" icon="el-icon-refresh-left">重置</el-button>
            </el-form-item>
          </el-form>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
import commonAPI from '@/api/common.js'
import { findList } from '../scripts/api'
export default {
  name: 'SelectIndexQuery',
  props: {
    rankType: {
      type: String,
      default: ''
    },
    pageList: {
      type: Object,
      default: () => {}
    },
    orderList: {
      type: Object,
      default: () => {
        return {
          orderString: 'm3_return desc'
        }
      }
    }
  },
  data() {
    return {
      simpleSearch: {
        fundName: '',
        managerName: '',
        rankDate: '',
        navDate: ''
      },
      rankTimeList: []
    }
  },
  watch: {
    rankType: {
      handler(val) {
        this.init()
      }
    }
  },
  mounted() {
    // this.init()
  },
  methods: {
    async init() {
      await this.getRankTime()
      await this.getNavDate()
      await this.handleQueryList()
    },
    /**
     * @description 获取榜单时间下拉
     */
    getRankTime() {
      return new Promise((resolve, reject) => {
        const data = {
          indexCode: 'ffe26530-fb44-4a50-acb3-4823c303ad28',
          rankType: this.rankType
        }
        commonAPI
          .getDataBysqlCode(data)
          .then((res) => {
            if (res.data.status === 0) {
              const timeArr = res.data.data || []
              this.rankTimeList = timeArr.map((item) => {
                return {
                  label: item.VC_BD_DATE,
                  value: item.VC_BD_DATE
                }
              })
              resolve()
            }
          })
          .catch((err) => {
            reject(err)
          })
      })
    },
    /**
     * @description 获取净值日期
     */
    getNavDate() {
      return new Promise((resolve, reject) => {
        const data = {
          indexCode: '6f999d68-fce9-453d-9aca-7119d1723445'
        }
        commonAPI
          .getDataBysqlCode(data)
          .then((res) => {
            if (res.data.status === 0) {
              const navDateArr = res.data.data || []
              this.simpleSearch.navDate = navDateArr[0].NAVDATE
              resolve()
            }
          })
          .catch((err) => {
            reject(err)
          })
      })
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
     * @description 重置
     */
    reset() {
      for (const key in this.simpleSearch) {
        this.simpleSearch[key] = ''
      }
      // 重置分页
      this.$emit('resetPage')
    },
    /**
     * @description 获取查询参数
     */
    getParamster() {
      const params = Object.assign({}, { ...this.simpleSearch, ...this.orderList })
      params.rankType = this.rankType
      params.limit = this.pageList._pageSize
      params.offset = (this.pageList._pageNum - 1) * this.pageList._pageSize
      return this.parameterSrc(params)
    },
    /**
     * @description 查询列表
     */
    async handleQueryList() {
      const data = this.getParamster()
      this.$emit('updateLoading', true)
      // 接口调用
      try {
        const res = await findList(data)
        if (res.data.status === 0) {
          this.$emit('updateTable', res.data.data)
        } else {
          this.$emit('updateTable', [])
        }
        this.$emit('updateLoading', false)
      } catch (e) {
        this.$emit('updateLoading', false)
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.dd-query {
  margin: 12px 20px 0px 16px;
  .funds-filter {
    width: 100%;
    padding-left: 10px;
    .funds-filter-search {
      // border-bottom: 1px solid #e1e0e0;
    }
  }
}
</style>

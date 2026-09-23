<template>
  <div id="dd-query">
    <div class="funds-filter">
      <div class="funds-filter-search search-content">
        <div class="funds-search-simple analyse-page">
          <el-row>
            <el-form ref="searchForm" :inline="true" :model="simpleSearch" :rules="rules" class="standard-form" style="margin-bottom: 4px;">
              <el-row type="flex" justify="start">
                <el-form-item label="">
                  <el-input v-model="simpleSearch.fundName" placeholder="请输入产品名称/产品代码" size="small" style="width: 290px !important;" />
                </el-form-item>
                <el-form-item label="">
                  <el-input v-model="simpleSearch.managerName" placeholder="请输入产品管理人" size="small" style="width: 230px !important;" />
                </el-form-item>
                <el-form-item label="管理规模区间" v-show="false">
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
                <el-form-item label="" prop="endDate">
                  <el-date-picker v-model="simpleSearch.endDate" :clearable="false" type="date" value-format="yyyy-MM-dd" placeholder="请选择日期" size="small" />
                </el-form-item>
<!--                <el-form-item class="searchRight">
                  <el-radio v-for="item in radioOptions" :key="item.value" v-model="switchPageType" :label="item.value" @input="radioChange">
                    {{ item.label }}
                  </el-radio>
                </el-form-item>-->
                <el-form-item>
                  <el-button type="primary" size="small" @click="handleQueryParams" icon="el-icon-search">查询</el-button>
<!--                  <el-button type="info" plain size="small" @click="reset" icon="el-icon-refresh-left">重置</el-button>-->
                  <el-button type="primary" size="small" @click="showMoreQuery">
                    <span>{{ isShowMoreQuery ? '收起筛选' : '展开筛选' }}</span>
                    <i :class="isShowMoreQuery ? 'el-icon-caret-top' : 'el-icon-caret-bottom'" />
                  </el-button>
                  <el-button size="small" type="primary" @click="$emit('saveCurrentCondition')" >
                    保存
                  </el-button>
                  <el-button size="small" type="info" @click="$emit('clearCurrentCondition')">
                    清除
                  </el-button>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" size="small" icon="el-icon-download" @click="downloadTemplate">产品清单模板</el-button>
                  <el-button type="primary" size="small" icon="el-icon-upload" @click="triggerFileInput">上传产品清单</el-button>
                  <input type="file" ref="fileInput" style="display: none" accept=".xls,.xlsx" @change="handleFileUpload">
                </el-form-item>
              </el-row>
            </el-form>
          </el-row>
        </div>
      </div>
      <transition name="fade">
        <div v-show="isShowMoreQuery && switchPageType === '1'">
          <allMarketQuery
            ref="allMarketQuery"
            :sql-obj="{
              indexCode: 'b4923f1f-46a9-42f0-aff3-403cb6fb26bf'
            }"
            :switch-page-type="switchPageType"
            @updateSelect="getDynamicData"
          />
        </div>
      </transition>
      <transition name="fade">
        <div v-show="isShowMoreQuery && switchPageType === '2'">
          <epibolyQuery
            ref="epibolyQuery"
            :sql-obj="{
              indexCode: '6c7d78c7-aced-487b-8310-a9ad7e09c3f8',
              indexCode2: 'b4923f1f-46a9-42f0-aff3-403cb6fb26bf',
              indexCode3: '0741c35f-aab9-4cda-ada6-c3db4db88c47'
            }"
            :switch-page-type="switchPageType"
            @updateSelect="getDynamicData"
            :dynamicTagsPro="simpleSearchPro"
            @childArr="(newObj, source) => handleSimpleSearch(newObj, source)"
          />
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import request from '@/utils/request'
import Constant from '../scripts/constant'
import allMarketQuery from '../businessComp/allMarketQuery/more-query.vue'
import epibolyQuery from '../businessComp/epibolyQueryNew/more-query.vue'
import { findList,downloadFundTemplate,parseFundExcel } from '../scripts/api'
import defaultCts from '../businessComp/allMarketQuery/constant'
import defaultCtsTgwb from '../businessComp/epibolyQueryNew/constant'
export default {
  name: 'AllMarketQuery',
  components: {
    allMarketQuery,
    epibolyQuery
  },
  props: {
    simpleSearchPro: {
      type: Object,
      default: () => ({})
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
          orderString: 'm1_return desc'
        }
      }
    }
  },
  data() {
    return {
      simpleSearch: {
        ...this.simpleSearchPro.simpleSearch
      },
      isParentSync: false,
      // 机构规模
      orzScaleOptions: Constant.orzScaleOptions,
      radioOptions: Constant.radioOptions,
      switchPageType: '2',
      isShowMoreQuery: true,
      marketData: [],
      focusData: [],
      isBx: true,
      rules: {
        endDate: [{ type: 'string', required: true, message: '请选择截止日期', trigger: 'change' }]
      },
      fundCodeList:[],
      fundNameList:[],
    }
  },
  computed: {
    // OUT全市场私募产品，IN托管外包产品
    soucre() {
      if (this.switchPageType === '1') {
        return 'OUT'
      } else {
        return 'IN'
      }
    }
  },
  watch: {
    simpleSearchPro: {
      deep: true,
      immediate: true,
      handler(newObj) {
        this.isParentSync = true
        this.simpleSearch = { ...newObj.simpleSearch }
        this.$nextTick(() => {
          this.isParentSync = false
        })
      }

    },
    simpleSearch: {
      deep: true,
      handler(newObj) {
        if (!this.isParentSync) {
        this.$emit('grandChildObj', newObj, 'child')
        }
      }
    }
  },
  async mounted() {
    await this.getEndDate()
    this.handleQueryParams()
  },
  methods: {
    handleSimpleSearch(newObj, source) {
      if (source === 'grandChild') {
        this.$emit('grandChildObj', newObj, 'grandChild')
      }
    },
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
      params.fundCodeList = this.fundCodeList
      params.fundNameList = this.fundNameList
      // 全市场私募or托管外包
      params.source = this.switchPageType === '1' ? '' : 'IN'
      // 机构规模不限则传空
      params.asset_list = this.simpleSearch.asset_list.includes('不限') ? [] : this.simpleSearch.asset_list
      const _moreData = this.radioChange(this.switchPageType)
      // 运行状态默认条件
      if (this.soucre === 'OUT') {
        params.statuses = defaultCts.yxztData[0].checked === 2 ? '' : [defaultCts.yxztData[0].checked.toString()]
      } else {
        params.statuses = defaultCtsTgwb.yxztData[0].checked === 2 ? '' : [defaultCtsTgwb.yxztData[0].checked.toString()]
      }
      // 更多查询入参
      _moreData.forEach((item) => {
        // 策略类型
        if (item.id === '1') {
          params.fofMainStrategys = item.code.split('，').slice(0, -1)
        }
        //子策略
        if (item.id === '100') {
          params.fofSubStrategys = item.code.split('，').slice(0, -1)
        }
         //三级策略
        if (item.id === '200') {
          params.fofThirdStrategys = item.code.split('，').slice(0, -1)
        }


        // 运行状态
        if (item.id === '2') {
          params.statuses = [item.code.toString()]
        }
        // 是否分级
        if (item.id === '3') {
          params.isTier = item.code.toString()
        }
        // 是否代销
        if (item.id === '102') {
          params.gfSelling = item.code.toString()
        }
        // 净值频率
        if (item.id === '4') {
          params.navfrequency = item.code.toString()
        }
        // 绩效评级
        if (item.id === '5') {
          params.frating = item.code.toString()
        }
        // 成立日期
        if (item.id === '6') {
          params.found_begin = item.start || ''
          params.found_end = item.end || ''
        }
        // 资产净值
        // if (item.id === '7') {
        //   params.price_begin = Number(item.start) * 10000
        //   params.price_end = Number(item.end) * 10000
        // }
        // 单位净值
        if (item.id === '7') {
          params.unit_nav_begin = item.start !== '' ? Number(item.start) : ''
          params.unit_nav_end = item.end !== '' ? Number(item.end) : ''
        }
        // 累计净值
        if (item.id === '20') {
          params.added_nav_begin = item.start !== '' ? Number(item.start) : ''
          params.added_nav_end = item.end !== '' ? Number(item.end) : ''
        }
        // 资产净值
        if (item.id === '21') {
          params.price_begin = item.start !== '' ? Number(item.start)*10000 : ''
          params.price_end = item.end !== '' ? Number(item.end)*10000 : ''
        }
        // 股票占净值比
        if (item.id === '15') {
          params.stock_ratio_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.stock_ratio_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        // 基金占净值比
        if (item.id === '16') {
          params.fund_ratio_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.fund_ratio_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        // 期货占净值比
        if (item.id === '17') {
          params.futures_ratio_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.futures_ratio_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        // 债券占净值比
        if (item.id === '18') {
          params.bond_ratio_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.bond_ratio_e = item.end !== '' ? Number(item.end) / 100 : ''
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
      this.switchPageType = '2'
      this.simpleSearch.asset_list = ['不限']
      // 清空子组件
      this.$refs.allMarketQuery.reset()
      this.$refs.epibolyQuery.reset()
      // 重置分页
      this.$emit('resetPage')
    },
    /**
     * @description 获取子组件已选条件
     */
    getDynamicData(val) {
      if (val.status === '1') {
        this.marketData = val.query
      } else {
        this.focusData = val.query
      }
    },
    /**
     * @description 根据radio切换组装入参
     */
    radioChange(val) {
      this.$emit('radioSource', val)
      let moreData = []
      if (val === '1') {
        moreData = this.marketData
      } else {
        moreData = this.focusData
      }
      return moreData
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
      params.fundCodeList = this.fundCodeList
      params.fundNameList = this.fundNameList
      // 分页计算
      params.limit = this.pageList._pageSize
      params.offset = (this.pageList._pageNum - 1) * this.pageList._pageSize
      // 全市场私募or托管外包
      params.source = this.switchPageType === '1' ? '' : 'IN'
      // 机构规模不限则传空
      params.asset_list = this.simpleSearch.asset_list.includes('不限') ? [] : this.simpleSearch.asset_list
      // 运行状态默认条件
      if (this.soucre === 'OUT') {
        params.statuses = defaultCts.yxztData[0].checked === 2 ? '' : [defaultCts.yxztData[0].checked.toString()]
      } else {
        params.statuses = defaultCtsTgwb.yxztData[0].checked === 2 ? '' : [defaultCtsTgwb.yxztData[0].checked.toString()]
      }
      const _moreData = this.radioChange(this.switchPageType)
      // 更多查询入参
      _moreData.forEach((item) => {
        // 策略类型
        if (item.id === '1') {
          params.fofMainStrategys = item.code.split('，').slice(0, -1)
        }
        //子策略
        if (item.id === '100') {
          params.fofSubStrategys = item.code.split('，').slice(0, -1)
        }
        //三级策略
        if (item.id === '200') {
          params.fofThirdStrategys = item.code.split('，').slice(0, -1)
        }
        // 运行状态
        if (item.id === '2') {
          params.statuses = [item.code.toString()]
        }
        // 是否分级
        if (item.id === '3') {
          params.isTier = item.code.toString()
        }
        // 净值频率
        if (item.id === '4') {
          params.navfrequency = item.code.toString()
        }

        // 是否代销
        if (item.id === '102') {
          params.gfSelling = item.code.toString()
        }
        // 绩效评级
        if (item.id === '5') {
          params.frating = item.code.toString()
        }
        // 成立日期
        if (item.id === '6') {
          params.found_begin = item.start || ''
          params.found_end = item.end || ''
        }
        // 资产净值
        // if (item.id === '7') {
        //   params.price_begin = Number(item.start) * 10000
        //   params.price_end = Number(item.end) * 10000
        // }
        // 单位净值
        if (item.id === '7') {
          params.unit_nav_begin = item.start !== '' ? Number(item.start) : ''
          params.unit_nav_end = item.end !== '' ? Number(item.end) : ''
        }
        // 累计净值
        if (item.id === '20') {
          params.added_nav_begin = item.start !== '' ? Number(item.start) : ''
          params.added_nav_end = item.end !== '' ? Number(item.end) : ''
        } // 资产净值
        if (item.id === '21') {
          params.price_begin = item.start !== '' ? Number(item.start)*10000 : ''
          params.price_end = item.end !== '' ? Number(item.end)*10000 : ''
        }
        // 股票占净值比
        if (item.id === '15') {
          params.stock_ratio_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.stock_ratio_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        // 基金占净值比
        if (item.id === '16') {
          params.fund_ratio_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.fund_ratio_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        // 期货占净值比
        if (item.id === '17') {
          params.futures_ratio_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.futures_ratio_e = item.end !== '' ? Number(item.end) / 100 : ''
        }
        // 债券占净值比
        if (item.id === '18') {
          params.bond_ratio_b = item.start !== '' ? Number(item.start) / 100 : ''
          params.bond_ratio_e = item.end !== '' ? Number(item.end) / 100 : ''
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
    handleFindList(params) {
      const data = this.parameterSrc(params)
      this.$refs.searchForm.validate(async (valid) => {
        if (valid) {
          this.$emit('updateLoading', true)
          try {
            const res = await findList(data)
            if (res.data.status === 0) {
              this.$emit('updateTable', res.data.data)
              this.$emit('updateLoading', false)
            } else {
              this.$message({
                type: 'error',
                message: res.message
              })
            }
          } catch (e) {
            this.$emit('updateLoading', false)
          }
        } else {
          return false
        }
      })
    },
    downloadTemplate() {
      downloadFundTemplate().then(function (res) {
        // 创建blob对象处理Excel二进制流
        const blob = new Blob([res.data], { type: 'application/vnd.ms-excel' })
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = '产品清单模板.xls'
        a.click()
        // 释放URL对象
        window.URL.revokeObjectURL(url)
        this.$message.success('模板下载成功')
      }.bind(this)).catch(function (err) {
        this.$message.closeAll()
        this.$message.error('模板下载失败：' + (err.message || '服务器错误'))
      }.bind(this))
    },

    triggerFileInput() {
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = ''
      }
      this.$refs.fileInput.click()
    },

    handleFileUpload(e) {
      const file = e.target.files[0]
      if (!file) {
        return
      }

      // 校验文件格式
      const fileName = file.name
      if (!fileName.endsWith('.xls') && !fileName.endsWith('.xlsx')) {
        this.$message.warning('仅支持.xls和.xlsx格式的Excel文件')
        this.$refs.fileInput.value = ''
        return
      }

      // 构建FormData
      const formData = new FormData()
      formData.append('file', file)

      this.tableLoading = true
      parseFundExcel(formData).then(function (res) {
        this.tableLoading = false
        const resData = res.data || {}
        if (resData.status === 200) {
          const result = resData.data || {}
          this.fundCodeList = result.fundCodeList || []
          this.fundNameList = result.fundNameList || []
          if (this.fundCodeList.length > 0 || this.fundNameList.length > 0 ) {
            // 自动触发查询
            this.handleQueryParams()
          } else {
            this.$message.warning('Excel中未解析到有效产品代码')
          }
        } else {
          this.$message.error('Excel解析失败：' + (resData.message || '解析错误'))
        }
        // 清空文件选择框
        this.$refs.fileInput.value = ''
      }.bind(this)).catch(function (err) {
        this.tableLoading = false
        this.$message.error('文件上传失败：' + (err.message || '网络错误'))
        // 清空文件选择框
        this.$refs.fileInput.value = ''
      }.bind(this))
    },
  }
}
</script>

<style lang="scss" scoped>
#dd-query {
  margin: 12px 10px 8px 0px;
  .funds-filter {
    width: 100%;
    padding-left: 10px;
    .funds-filter-search {
      //border-bottom: 1px solid #e1e0e0;
    }
  }
  .searchRight {
    ::v-deep .el-radio {
      margin-right: 8px;
    }
    ::v-deep .el-radio__label {
      padding-left: 5px;
    }
    ::v-deep .el-radio__input.is-checked .el-radio__inner {
      border-color: #0F65DD;
      background: #0F65DD;
    }
    ::v-deep .el-radio__input.is-checked + .el-radio__label {
      color: #0F65DD;
    }
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.1s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>

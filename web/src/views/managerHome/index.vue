<template>
  <div class="mt20" style="padding-left: 20px; padding-right: 20px;">
    <el-form ref="formQuery" :inline="true" :model="formQuery" class="standard-form">
      <el-form-item label="机构">
        <el-select v-model="formQuery.companyId" filterable :filter-method="onCompanyFilter"
          popper-class="manager-home-company-select" @visible-change="onCompanySelectVisible"
          @change="handleCompanyChange" size="small">
          <el-option v-for="item in companyList" :key="item.companyId" :label="item.companyName"
            :value="item.companyId"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="">
        <el-date-picker v-model="formQuery.dDate" type="date" value-format="yyyy-MM-dd" :clearable="false"
          size="small" :picker-options="datePickerOptions"></el-date-picker>
      </el-form-item>
      <img src="./img/search.svg" style="width: 40px; height: 40px;" @click="handleSearch">
    </el-form>

    <totalDescription :query-params="queryParams" :update-flag="updateFlag"></totalDescription>
    <dataOverview :query-params="queryParams" :update-flag="updateFlag"></dataOverview>
    <el-row :gutter="20">
      <el-col :span="8">
        <asset :query-params="queryParams" :update-flag="updateFlag"></asset>
      </el-col>
      <el-col :span="16">
        <assetTime :query-params="queryParams" :update-flag="updateFlag"></assetTime>
      </el-col>
    </el-row>
    <totalScaleTime :query-params="queryParams" :update-flag="updateFlag"></totalScaleTime>
    <productPerformance :query-params="queryParams" :update-flag="updateFlag"></productPerformance>
    <indexMarket :query-params="queryParams" :update-flag="updateFlag"></indexMarket>
  </div>
</template>
<script>
import totalDescription from './components/totalDescription'
import dataOverview from './components/dataOverview'
import asset from './components/asset'
import assetTime from './components/assetTime'
import totalScaleTime from './components/totalScaleTime'
import productPerformance from './components/productPerformance'
import indexMarket from './components/indexMarket'
import indexAPI from './api/index.js'
import moment from 'moment'
import commonFun from '@/filters/common'

const COMPANY_PAGE_SIZE = 20

export default {
  name: 'managerHome',
  components: { totalDescription, dataOverview, asset, assetTime, totalScaleTime, productPerformance, indexMarket },
  data() {
    return {
      formQuery: {
        companyId: "",
        dDate: ""
      },
      datePickerOptions: {
        disabledDate: this.disabledDate
      },
      companyListAll: [],
      companySearchKeyword: '',
      companyDisplayCount: COMPANY_PAGE_SIZE,
      companyScrollWrap: null,
      fundList: [],
      updateFlag: 0,
      queryParams: {
        companyId: '',
        companyName: '',
        fundList: [],
        initBeginDate: '',
        initEndDate: '',
        startDate: '',
        endDate: '',
        datePickerOptions: {
          shortcuts: commonFun.dateShortcut().shortcuts,
          disabledDate: this.disabledDate
        }
      }
    }
  },
  computed: {
    companyListFiltered() {
      const all = this.companyListAll
      const kw = (this.companySearchKeyword || '').trim()
      if (!kw) return all
      const lower = kw.toLowerCase()
      return all.filter((c) => {
        const name = (c.companyName != null ? String(c.companyName) : '').toLowerCase()
        const id = c.companyId != null ? String(c.companyId) : ''
        return name.includes(lower) || id.includes(kw)
      })
    },
    companyList() {
      const filtered = this.companyListFiltered
      const n = Math.min(this.companyDisplayCount, filtered.length)
      return filtered.slice(0, n)
    }
  },
  async mounted() {
    const { data } = await indexAPI.selectCompanyListAndDates();
    this.companyListAll = data.data.companyList;
    this.companyDisplayCount = Math.min(COMPANY_PAGE_SIZE, this.companyListAll.length)
    this.formQuery.companyId = this.companyListAll[0].companyId
    this.formQuery.ddate = data.data.endT3Date
    this.selectFundListAndDates(this.companyListAll[0].companyId, this.companyListAll[0].companyName)
  },
  beforeDestroy() {
    this.removeCompanyScrollListener()
  },
  activated() { },
  deactivated() { },
  methods: {

    disabledDate(date){
      return moment(date).isBefore(moment(this.queryParams.startDate))
      || moment(date).isAfter(moment(this.queryParams.endDate))
    },

    onCompanyFilter(query) {
      this.companySearchKeyword = (query || '').trim()
      this.$nextTick(() => {
        this.companyDisplayCount = Math.min(COMPANY_PAGE_SIZE, this.companyListFiltered.length)
      })
    },
    onCompanySelectVisible(visible) {
      if (visible) {
        this.companySearchKeyword = ''
        this.companyDisplayCount = Math.min(COMPANY_PAGE_SIZE, this.companyListAll.length)
        this.$nextTick(() => {
          setTimeout(() => this.attachCompanyScrollListener(), 100)
        })
      } else {
        this.companySearchKeyword = ''
        this.removeCompanyScrollListener()
      }
    },
    attachCompanyScrollListener() {
      const wrap = document.querySelector('.manager-home-company-select .el-select-dropdown__wrap')
      if (wrap && wrap !== this.companyScrollWrap) {
        this.removeCompanyScrollListener()
        this.companyScrollWrap = wrap
        wrap.addEventListener('scroll', this.onCompanyDropdownScroll)
      }
    },
    removeCompanyScrollListener() {
      if (this.companyScrollWrap) {
        this.companyScrollWrap.removeEventListener('scroll', this.onCompanyDropdownScroll)
        this.companyScrollWrap = null
      }
    },
    onCompanyDropdownScroll(e) {
      const { scrollTop, clientHeight, scrollHeight } = e.target
      const threshold = 30
      if (scrollTop + clientHeight < scrollHeight - threshold) return
      const total = this.companyListFiltered.length
      if (this.companyDisplayCount >= total) return
      this.companyDisplayCount = Math.min(this.companyDisplayCount + COMPANY_PAGE_SIZE, total)
    },
    handleCompanyChange(val) {
      const arr = this.companyListAll.filter(item => item.companyId === val)
      if (!arr.length) return
      this.selectFundListAndDates(val, arr[0].companyName)
    },
    handleSearch() {
      this.updateFlag = Date.now()
      this.queryParams.initEndDate=this.formQuery.dDate
    },
    async selectFundListAndDates(companyId,companyName){
      const { data } = await indexAPI.selectFundListAndDates(companyId);
      this.formQuery.dDate = data.data.company.initEndDate;
      let fundList = data.data.fundList;
      fundList.forEach(item => {
        item.fundName = item.fundCode + "_" + item.fundName
      });
      let obj = {
        companyId: companyId,
        companyName: companyName,
        fundList: fundList,
        initBeginDate: data.data.company.initBeginDate,
        initEndDate: data.data.company.initEndDate,
        startDate: data.data.company.startDate,
        endDate: data.data.company.endDate
      }
      this.queryParams = obj;
      console.log(this.queryParams)
      if(this.updateFlag === 0){
        this.handleSearch()
      }
    }
  }
}
</script>
<style lang="scss" scoped></style>

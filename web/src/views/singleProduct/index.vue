<template>
  <div class="single-product">
    <base-info
      ref="baseInfo"
      :current-list="currentList"
      :fund-code="currentCode"
      @getparams="getSearchParams"
      @getparamssearcall="getParamsSearcAll"
      @updeteiframe="updeteiframe"
    ></base-info>
    <div class="tab-content">
      <el-tabs v-if="currentSource === 'OUT'" v-model="activeName" class="mt10" type="border-card">
        <el-tab-pane label="产品表现" name="smcpbx">
          <investment-history ref="investmentHistory"></investment-history>
          <product-show ref="productShow" :cover-div="coverDiv" @uploadCover="uploadCover"></product-show>
        </el-tab-pane>
        <el-tab-pane label="基本信息" name="smjbxx">
          <product-Info ref="productInfo" :cover-div="coverDiv" @uploadCover="uploadCover"></product-Info>
        </el-tab-pane>
      </el-tabs>
      <el-tabs v-else v-model="activeNameTg" class="mt10" type="border-card">
        <el-tab-pane label="产品表现" name="tgcpbx">
          <investment-history-tg ref="investmentHistoryTg"></investment-history-tg>
          <product-show-tg ref="productShowTg" :cover-div="coverDiv" @uploadCover="uploadCover"></product-show-tg>
        </el-tab-pane>
<!--        <el-tab-pane label="产品信息" name="tgjbxx" >-->
<!--          <product-info-tg ref="productInfoTg" :cover-div="coverDiv" @uploadCover="uploadCover"></product-info-tg>-->
<!--        </el-tab-pane>-->
        <!-- <el-tab-pane label="深度分析" name="tgsdfx">
          <deep-analyse ref="productsdfx"></deep-analyse>
        </el-tab-pane> -->
      </el-tabs>
    </div>
  </div>
</template>
<script>
import BaseInfo from './components/base-info.vue'
// import ProductShow from './components/product-show.vue'
import ProductShow from './components/productPerformance/riskIndex.vue'
// import ProductShowTg from './components/product-show-tg.vue'
import ProductShowTg from './components/productPerformance/riskIndexTg.vue'
// import ProductInfo from './components/product-info.vue'
// import ProductInfoTg from './components/product-info-tg.vue'
import ProductInfo from './components/productPerformance/productInfo.vue'
import ProductInfoTg from './components/productPerformance/productInfoTg.vue'

import investmentHistoryTg from './components/productPerformance/investmentHistoryTg'
import investmentHistory from './components/productPerformance/investmentHistory'

import deepAnalyse from './components/deep-analyse.vue'
import request from '@/utils/request'

export default {
  name: 'SingleProduct',
  components: {
    BaseInfo,
    ProductShow,
    ProductInfo,
    ProductShowTg,
    ProductInfoTg,
    deepAnalyse,
    investmentHistoryTg,
    investmentHistory
  },
  data() {
    return {
      activeName: 'smcpbx',
      activeNameTg: 'tgcpbx',
      currentList: null,
      searchQuery: {},
      coverDiv: false,
      currentCode: '',
      currentSource: ''
    }
  },
  watch: {
    '$route.query.list': {
      handler(newVal) {
        if (this.$store.getters.fromPageJump) {
          if (this.$route.query && this.$route.query.list && this.$route.query.list.fundCode) {
            this.handleQueryBaseInfo(newVal.fundCode)
            this.currentCode = newVal.fundCode
            this.currentSource = newVal.source
            this.$store.commit('SET_FROMPAGEJUMP', false)
            // 动态修改tag-views dom标签
            document.querySelector('.tags-view-item.active .tag-title') &&
              (document.querySelector('.tags-view-item.active .tag-title') &&
                (document.querySelector('.tags-view-item.active .tag-title').innerText = newVal.fundName || '单产品分析'))
          }
        }
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    /**
     * @description 更新查询条件focus状态
     */
    updeteiframe() {
      this.coverDiv = true
    },
    /**
     * @desc 解决点击iframe无法收起下拉框
     * @param { Boolean } val 遮罩状态
     */
    uploadCover(val) {
      this.coverDiv = val
    },
    /**
     * @description 查询对应vm
     */
    getSearchParams(val) {
      console.log(val)
      if (this.currentSource === 'OUT') {
        const currentTab = this.activeName
        if (currentTab === 'smcpbx') {
          this.$nextTick(() => {
            this.$refs.investmentHistory.searchQuery = val
            this.$refs.investmentHistory.fun_iframeSrc()

            this.$refs.productShow.searchQuery = val
            this.$refs.productShow.fun_iframeSrc()
          })
        } else if (currentTab === 'smjbxx') {
          this.$nextTick(() => {
            this.$refs.productInfo.searchQuery = val
            this.$refs.productInfo.fun_iframeSrc()
          })
        }
      } else {
        const currentTab = this.activeNameTg
        if (currentTab === 'tgcpbx') {
          this.$nextTick(() => {
            this.$refs.investmentHistoryTg.searchQuery = val
            this.$refs.investmentHistoryTg.fun_iframeSrc()
            this.$refs.productShowTg.searchQuery = val
            this.$refs.productShowTg.fun_iframeSrc()
          })
        } else if (currentTab === 'tgjbxx') {
          this.$nextTick(() => {
            this.$refs.productInfoTg.searchQuery = val
            this.$refs.productInfoTg.fun_iframeSrc()
          })
        }
      }
    },
    /**
     * @description 查询对应来源下所有vm
     */
    getParamsSearcAll(val) {
      if (this.currentSource === 'OUT') {
        this.$nextTick(() => {
          this.$refs.investmentHistory.searchQuery = val
          this.$refs.investmentHistory.fun_iframeSrc()
          this.$refs.productShow.searchQuery = val
          this.$refs.productShow.fun_iframeSrc()
          this.$refs.productInfo.searchQuery = val
          this.$refs.productInfo.fun_iframeSrc()
        })
      } else {
        this.$nextTick(() => {
          this.$refs.investmentHistoryTg.searchQuery = val
          this.$refs.investmentHistoryTg.fun_iframeSrc()
          this.$refs.productShowTg.searchQuery = val
          this.$refs.productShowTg.fun_iframeSrc()
          this.$refs.productInfoTg.searchQuery = val
          this.$refs.productInfoTg.fun_iframeSrc()
        })
      }
    },
    /**
     * @description 获取顶部产品信息
     */
    handleQueryBaseInfo(fundcode) {
      const params = {
        indexCode: 'f8dffeef-1dd5-4ce8-8ddb-046b11050373'
      }
      params.fundCode = fundcode
      request({
        url: `/api/report/v1.0/data/sql/${params.indexCode}`,
        method: 'post',
        data: params
      }).then(res => {
        if (res.data.status === 0) {
          const baseInfo = res.data.data || []
          this.currentList = baseInfo[0] || {}
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.single-product {
  background-color: #F3F5FB;
  .tab-content {
    background-color: #F3F5FB;
    margin: 0 20px;

    ::v-deep .el-table thead {
      height: 40px !important;
    }

    ::v-deep .el-tabs__header {
      margin-bottom: 0px !important;
    }

    ::v-deep .el-tabs__item {
      height: 40px !important;
      line-height: 40px !important;
    }

    ::v-deep .el-tabs__content {
      padding: 0;
    }

    ::v-deep .el-tabs__nav {
      border: 1px solid #E4E7ED;
      border-bottom: none;
      border-radius: 4px 4px 0 0;
      -webkit-box-sizing: border-box;
      box-sizing: border-box;
    }
    // 修改tab切换样式
    ::v-deep .el-tabs__item {
      border-left: 1px solid #fcf8f4;
      border-right: 1px solid #fcf8f4;
      border-top: 2px solid transparent;
      color: #612d10;
      background-color: #fcf8f4 !important;
    }
    .el-tabs__item:first-child {
      border-left: none;
    }

    ::v-deep .el-tabs__item:hover {
      //color: #0F65DD;
    }

    ::v-deep .el-tabs__item.is-active {
      //border-top: 2px solid #612d10;
      color: #612d10;
      //font-weight: bold;
      background-image: linear-gradient(to right, #f5d7bc, #e0b794) !important;
    ;
    }
  }
}
</style>

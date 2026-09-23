<template>
  <div class="manager-detail standard-form">
    <div class="base-info">
      <base-info :current-list="currentList"></base-info>
    </div>
    <div class="tab-content">
      <el-tabs v-model="activeName" class="mt10" type="border-card">
        <el-tab-pane label="管理人表现" name="glrbx">
          <manager-show ref="manangerShow" :current-list="currentList"></manager-show>
        </el-tab-pane>
        <el-tab-pane label="管理人信息" name="glrxx">
          <manager-info :manager-info="managerInfo"></manager-info>
        </el-tab-pane>
        <el-tab-pane label="旗下产品" name="qxcp">
          <product-info ref="productInfo"></product-info>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script>
import request from '@/utils/request'
import BaseInfo from './components/base-info.vue'
import ManagerInfo from './components/manager-info.vue'
import ManagerShow from './components/manager-show.vue'
import ProductInfo from './components/product-info.vue'
export default {
  name: 'ManagerDetail',
  components: {
    BaseInfo,
    ManagerInfo,
    ManagerShow,
    ProductInfo
  },
  data() {
    return {
      activeName: 'glrbx',
      currentList: null,
      managerInfo: null
    }
  },
  watch: {
    '$route.query.managerList': {
      handler(newVal) {
        if (this.$store.getters.fromPageJump) {
          console.log(this.$route.query.managerList.company_id, '管理人id')
          if (this.$route.query && this.$route.query.managerList) {
            // 管理人顶部数据获取
            this.handleQueryBaseInfo(newVal.company_id)
            // 管理人信息tab数据获取
            this.handleQueryManagerInfo(newVal.company_id)
            // 管理人旗下产品tab数据获取
            this.handleQueryManangerFund(newVal.company_id)
            // 管理人表现tab数据获取
            this.handleQueryManagerShow(newVal.company_id)
            this.$store.commit('SET_FROMPAGEJUMP', false)
            // 动态修改tag-views dom标签
            document.querySelector('.tags-view-item.active .tag-title') &&
              (document.querySelector('.tags-view-item.active .tag-title').innerText = newVal.manager_name || '单管理人分析')
          }
        }
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    /**
     * @description 获取单管理人顶部信息
     */
    handleQueryBaseInfo(managerCode) {
      const params = {
        indexCode: 'b891751a-e82c-4728-b439-e4ad1653853e'
      }
      params.managerCode = managerCode || ''
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
    },
    /**
     * @description 获取单管理人-管理人信息tab
     */
    handleQueryManagerInfo(managerCode) {
      const params = {
        indexCode: '02fbab5f-32dd-4885-a8a0-219a8c36f714'
      }
      params.managerCode = managerCode || ''
      request({
        url: `/api/report/v1.0/data/sql/${params.indexCode}`,
        method: 'post',
        data: params
      }).then(res => {
        if (res.data.status === 0) {
          const baseInfo = res.data.data || []
          this.managerInfo = baseInfo[0] || {}
        }
      })
    },
    /**
     * @description 获取单管理人-管理人旗下产品tab
     */
    handleQueryManangerFund(managerCode) {
      this.$nextTick(() => {
        this.$refs.productInfo.managerCode = managerCode
      })
    },
    /**
     * @description 获取单管理人-管理人旗下产品tab
     */
    handleQueryManagerShow(managerCode) {
      this.$nextTick(() => {
        this.$refs.manangerShow.managerCode = managerCode
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.manager-detail {
  .tab-content {
    background-color: #fff;
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
    // 修改tab切换样式
    ::v-deep .el-tabs__item {
      border-left: 1px solid #d8dce5;
      border-right: 1px solid #d8dce5;
      border-top: 2px solid transparent;
      color: #333;
    }
    ::v-deep .el-tabs__item:hover {
      color: #0F65DD;
    }
    ::v-deep .el-tabs__item.is-active {
      border-top: 2px solid #0F65DD;
      color: #0F65DD;
      font-weight: bold;
    }
  }
}
</style>

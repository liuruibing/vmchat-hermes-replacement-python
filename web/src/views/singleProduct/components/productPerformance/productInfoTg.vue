<template>
  <div class="outProductInfo">
    <div class="productBaseInfo" v-if="showBaseInfo">
      <div class="title">
        <div class="title-icon">
          <div class="color-box"></div>
        </div>
        <div class="title-txt">
          <span>产品基本信息</span>
          <el-tooltip effect="dark" content="基本信息数据取自私募排排" placement="top">
            <svg-icon class="tip" icon-class="wenhao"></svg-icon>
          </el-tooltip>
        </div>
      </div>
      <div class="product-info-content" v-loading="baseInfoLoading">
        <el-descriptions class="margin-top" :column="2" border>
          <el-descriptions-item
            v-for="(item, index) in productBaseInfo"
            :key="index + item.value"
            :labelStyle="{ width: '25%', color: '#000', fontWeight: 'bold', backgroundColor: '#f7f7f7' }"
            :contentStyle="{ width: '25%', color: '#000' }"
          >
            <template slot="label">
              <span>{{ item.label }}</span>
            </template>
            <span>{{ item.value }}</span>
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </div>
    <div class="productRateInfo" v-if="showRateInfo">
      <div class="title">
        <div class="title-icon">
          <div class="color-box"></div>
        </div>
        <div class="title-txt">
          <span>产品费率信息</span>
          <el-tooltip effect="dark" content="费率信息数据取自私募排排" placement="top">
            <svg-icon class="tip" icon-class="wenhao"></svg-icon>
          </el-tooltip>
        </div>
      </div>
      <div class="product-info-content" v-loading="baseRateLoading">
        <el-descriptions
          class="margin-top"
          v-for="(item, index) in productBaseRateData"
          :key="index"
          :column="['b', 'd'].includes(index) ? 1 : 2"
          :labelStyle="{ width: '25%', color: '#000', fontWeight: 'bold', backgroundColor: '#f7f7f7' }"
          :contentStyle="{ width: ['b', 'd'].includes(index) ? '75%' : '25%', color: '#000' }"
          border
        >
          <el-descriptions-item v-for="(node, i) in item" :key="i" :labelClassName="`line${node.field}`" :contentClassName="`line${node.field}`">
            <template slot="label">
              <span>{{ node.label }}</span>
            </template>
            <span>{{ node.valie }}</span>
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </div>
    <div class="productLevelInfo" v-if="showLevelInfo">
      <div class="title">
        <div class="title-icon">
          <div class="color-box"></div>
        </div>
        <div class="title-txt">
          <span>产品评级信息</span>
          <el-tooltip effect="dark" content="评级信息数据取自私募排排" placement="top">
            <svg-icon class="tip" icon-class="wenhao"></svg-icon>
          </el-tooltip>
        </div>
      </div>
      <div class="product-info-content" v-loading="baseLevelLoading">
        <div class="row-header">
          <div class="col">时间</div>
          <div class="col">基金评级</div>
          <div class="col">收益等级</div>
          <div class="col">风险等级</div>
          <div class="col last">风格类别</div>
        </div>
        <div class="row-body" v-for="item in productLevelData" :key="item.id">
          <div class="col">{{ item.time }}</div>
          <div class="col">
            <el-rate v-model="item.fundLevel" :colors="['#e03d3e', '#e03d3e', '#e03d3e']" disabled disabled-void-color="#ccc"></el-rate>
          </div>
          <div class="col">
            <el-rate v-model="item.earnLevel" :colors="['#e03d3e', '#e03d3e', '#e03d3e']" disabled disabled-void-color="#ccc"></el-rate>
          </div>
          <div class="col">{{ item.riskLevel }}</div>
          <div class="col last">{{ item.styleCategory }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import commonAPI from '@/api/common.js'
import { productBaseInfoData, productBaseRateData, handleBaseRateData, productLevelData, handleProductLevelData } from '../../mock/productBaseInfoData'
export default {
  name: 'outProductInfo',

  data() {
    return {
      // 查询条件
      searchQuery: null,
      // 组件数据
      productBaseInfo: productBaseInfoData,
      productBaseRateData: productBaseRateData,
      productLevelData: productLevelData,
      // 组件loading
      baseInfoLoading: false,
      baseRateLoading: false,
      baseLevelLoading: false,
      // 权限判断
      showBaseInfo: false,
      showRateInfo: false,
      showLevelInfo: false
    }
  },
  methods: {
    /**
     * @description 初始化调用
     */
    fun_iframeSrc() {
      this.queryAuthIndex()
    },
    /**
     * @description 获取权限指标
     */
    queryAuthIndex() {
      const params = {}
      params.templateCode = 'dff07170-ebfc-4dd3-8908-1a929e0956a1'
      params.fundCode = this.searchQuery.fundCode
      commonAPI.selectIndexInfos(params).then(res => {
        if (res.data.status === 0) {
          const result = res.data.data || []
          const authArr = result.map(item => item.vcCode)
          if (authArr.includes('aaccf2a4-d720-45c0-9ff1-166b0c057f71')) {
            this.getProductBaseInfo('73b54335-e999-4dce-bbbe-9b8cec5258f3')
            this.showBaseInfo = true
          } else {
            this.showBaseInfo = false
          }
          if (authArr.includes('c80bb227-0c99-4dcc-acfd-add1c6f7041b')) {
            this.getProductRateInfo('0a8893dd-01d8-4420-a6d9-832b38186f28')
            this.showRateInfo = true
          } else {
            this.showRateInfo = false
          }
          if (authArr.includes('d703a9a9-5efd-48bf-92c6-d07f26809ff9')) {
            this.getProductLevelInfo('b5792c0f-553a-45b7-8dc9-b76b600bf4e8')
            this.showLevelInfo = true
          } else {
            this.showLevelInfo = false
          }
        } else {
          this.$message.error(res.data.message || '权限获取失败')
        }
      })
    },
    /**
     * @description 根据权限查询产品基本信息
     */
    getProductBaseInfo(indexCode) {
      const params = {
        ...this.searchQuery,
        indexCode,
        contrasCode: this.searchQuery.contrasCode.length ? this.searchQuery.contrasCode.join(',') : ''
      }
      delete params.statistPeriod
      this.baseInfoLoading = true
      commonAPI.getDataBysqlCode(params).then(res => {
        if (res.data.status === 0) {
          const result = res.data.data || []
          if (result && result.length) {
            this.productBaseInfo.forEach(item => {
              if (Object.keys(result[0]).includes(item.field)) {
                for (let key in result[0]) {
                  if (item.field === key) {
                    item.value = result[0][key]
                  }
                }
              } else {
                item.value = '-'
              }
            })
          }
          this.baseInfoLoading = false
        } else {
          this.baseInfoLoading = false
          this.$message.error(res.data.message || '查询产品基本信息失败')
        }
      })
    },
    /**
     * @description 根据权限查询产品费率信息
     */
    getProductRateInfo(indexCode) {
      const params = {
        ...this.searchQuery,
        indexCode,
        contrasCode: this.searchQuery.contrasCode.length ? this.searchQuery.contrasCode.join(',') : ''
      }
      delete params.statistPeriod
      this.baseRateLoading = true
      commonAPI.getDataBysqlCode(params).then(res => {
        if (res.data.status === 0) {
          const result = res.data.data || []
          if (result && result.length) {
            handleBaseRateData(result[0])
          }
          this.baseRateLoading = false
        } else {
          this.baseRateLoading = false
          this.$message.error(res.data.message || '查询产品费率信息失败')
        }
      })
    },
    /**
     * @description 根据权限查询产品评级信息
     */
    getProductLevelInfo(indexCode) {
      const params = {
        ...this.searchQuery,
        indexCode,
        contrasCode: this.searchQuery.contrasCode.length ? this.searchQuery.contrasCode.join(',') : ''
      }
      delete params.statistPeriod
      this.baseLevelLoading = true
      commonAPI.getDataBysqlCode(params).then(res => {
        if (res.data.status === 0) {
          const result = res.data.data || []
          if (result && result.length) {
            handleProductLevelData(result[0])
          }
          this.baseLevelLoading = false
        } else {
          this.baseLevelLoading = false
          this.$message.error(res.data.message || '查询产品评级信息失败')
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.outProductInfo {
  padding: 25px;
  .title {
    padding: 10px 0;
    border-bottom: 1px solid #A15008;

    .title-icon {
      vertical-align: middle;
      display: inline-block;
    }

    .color-box {
      display: inline-block;
      height: 12px;
      width: 4px;
      background-image: linear-gradient(-45deg,#e19c5d,#f4cea9);
      position: relative;
      top: 2px;
      margin-left: 5px;
    }

    .title-txt {
      color: #333333;
      vertical-align: middle;
      height: 35px;
      line-height: 35px;
      font-size: 16px;
      margin-left: 5px;
      display: inline-block;
    }

    .tip:hover {
      cursor: pointer;
    }
  }
  .product-info-content {
    padding: 20px;
  }

  ::v-deep .lineYDATE7,
  ::v-deep .lineYDATE8,
  ::v-deep .lineYDATE11,
  ::v-deep .lineYDATE12 {
    border-bottom: none;
  }

  .productLevelInfo {
    .row-header {
      height: 60px;
      display: flex;
      line-height: 60px;
      font-weight: bold;
      color: #bbb;
      font-size: 14px;
      background-color: #fff !important;
      border-bottom: 2px solid #ebeef5;

      .col {
        // background-color: #f7f7f7;
        flex: 1;
        text-align: center;
        border-right: none;
        border-top: 1px solid #ebeef5;
      }
      .col.last {
        border-right: 1px solid #ebeef5;
      }
      .col.first {
        border-left: 1px solid #ebeef5;
      }
    }
    .row-body {
      height: 40px;
      display: flex;
      line-height: 40px;
      .col {
        flex: 1;
        text-align: center;
        border: 1px solid #ebeef5;
        border-right: none;
        border-top: none;
        line-height: 40px;
        ::v-deep .el-rate {
          height: 40px;
          line-height: 50px;
        }
      }
      .col.last {
        border-right: 1px solid #ebeef5;
      }
    }
  }
}
</style>

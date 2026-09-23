<template>
  <div class="detailTop standard-form">
    <div class="header">
      <div class="product-info">
        <div class="top">
          <img :src="require('./manager-base-core/product.png')" />
          <span class="name">{{ currentList ? currentList.COMPANY_SHORT_NAME : '-' }}</span>
          <el-button type="primary" size="small" @click="jumpRoute">发起尽调</el-button>
        </div>
        <div class="bottom">
          <!--          <span class="time">{{ currentList ? currentList.ESTABLISH_DATE : '-' }}</span>-->
<!--          <span class="time">{{ currentList ? currentList.D_END_DATE : '-' }}</span>-->
        </div>
      </div>
      <div class="product-desc">
        <el-descriptions :column="3" size="small">
          <el-descriptions-item v-for="(desc, index) in topDescData" :key="index" :label="desc.label">
            <span>{{ desc.value || '' }}</span>
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </div>
    <div class="base-info-content">
      <div class="left">
        <div v-for="(data, index) in middleLeftData" :key="index" class="data-style">
          <div v-if="data.label == '最新数据日期'" class="value" style="font-size: 30px; height: 36px">
            <span style="color: #20212B">{{ currentList ? currentList.D_END_DATE : '-' }}</span>
          </div>
          <div v-else-if="data.value" :style="valueToColor(data.value)" class="value" style="font-size: 30px; height: 36px">
            {{ data.value}}
          </div>
          <div v-else class="value" style="height: 36px"></div>
          <div v-if="data.label == '最新数据日期'" class="label-zb" style="text-align: center;margin-top: 5px;" >
            {{ data.label }}
          </div>
          <div v-else class="label-zb" style="margin-top: 5px">{{ data.label }}</div>
        </div>
      </div>
      <div class="middle">
        <div v-for="(data, index) in middleMiddleData" :key="index" class="data-style">
          <div v-if="data.value" :style="valueToColor(data.value)" class="value">
            {{ data.value + '%' }}
          </div>
          <div v-else class="value" style="height: 36px"></div>
          <div class="label-zb">{{ data.label }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { TOP_DESC_DATA, MIDDLE_LEFT_DATA, MIDDLE_MIDDLE_DATA } from './manager-base-core/constant'
export default {
  name: 'ManagerBase',
  props: {
    currentList: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      topDescData: TOP_DESC_DATA,
      middleLeftData: MIDDLE_LEFT_DATA,
      middleMiddleData: MIDDLE_MIDDLE_DATA
    }
  },
  watch: {
    currentList: {
      handler(val) {
        if (val) {
          this.handleManagerInfo(val)
        } else {
          this.handleManagerInfo({})
        }
      },
      deep: true
    }
  },
  methods: {
    jumpRoute() {
      this.$router.push({
        path: '/xqhd/jdsq',
        query: {
          company: true,
          companyName: this.currentList.COMPANY_SHORT_NAME,
          companyId: this.currentList.COMPANY_ID
        }
      })
    },
    /**
     * @description 指标颜色判断
     */
    valueToColor(value) {
      if (value && value > 0) {
        return {
          color: 'red'
        }
      } else if (value && value < 0) {
        return {
          color: '#00d83d'
        }
      } else {
        return {
          color: '#20212B'
        }
      }
    },
    /**
     * @description 管理人详情头部信息
     */
    handleManagerInfo(val) {
      this.topDescData[0].value = val.COMPANY_NAME || '-'
      this.topDescData[1].value = val.COMPANY_TYPE || '-'
      this.topDescData[2].value = val.ESTABLISH_DATE || '-'
      this.topDescData[3].value = val.CAPITAL ? val.CAPITAL + '万元' : '-'
      this.topDescData[4].value = val.STAFF_NUM || '-'
      this.topDescData[5].value = val.REG_CODE || '-'
      this.topDescData[6].value = val.STATUS || '-'
      this.topDescData[7].value = val.REG_STATUS || '-'
      this.topDescData[8].value = val.FUND_NUM || '-'
      this.topDescData[9].value = val.MANAGE_ASSET || '-'
      // 指标区域
      this.middleLeftData[0].value = val.F_CURVE_NAV ? Number(val.F_CURVE_NAV).toFixed(4) : '-'
      this.middleMiddleData[0].value = val.F_RET_3M ? (val.F_RET_3M * 100).toFixed(2) : '-'
      this.middleMiddleData[1].value = val.F_RET_6M ? (val.F_RET_6M * 100).toFixed(2) : '-'
      this.middleMiddleData[2].value = val.F_RET_YTD ? (val.F_RET_YTD * 100).toFixed(2) : '-'
      this.middleMiddleData[3].value = val.F_RET_INCEP ? (val.F_RET_INCEP * 100).toFixed(2) : '-'
    }
  }
}
</script>

<style lang="scss" scoped>
.detailTop {
  display: flex;
  flex-direction: column;
  padding: 20px;
  .header {
    display: flex;
    align-items: center;
    margin-bottom: 40px;
    .product-info {
      padding-right: 10px;
      text-align: center;
      flex: 5;
      display: flex;
      flex-direction: column;
      .top {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        .name {
          color: #20212B;
          font-size: 24px;
          padding: 0 15px;
        }
        .status {
          color: #e03d3e;
          padding-bottom: 5px;
          padding-left: 5px;
        }
      }
      .bottom {
        flex: 1;
        display: flex;
        align-items: flex-start;
        justify-content: center;
        .time {
          padding-left: 10px;
          padding-top: 10px;
          font-size: 16px;
          color: #20212B;
        }
      }
    }
    .product-desc {
      flex: 11;
      ::v-deep .el-descriptions-item__label,
      ::v-deep .el-descriptions-item__content {
        color: #20212B;
      }
      ::v-deep .el-descriptions__body {
        background-color: rgba(0, 0, 0, 0);
      }
    }
  }
  .base-info-content {
    display: flex;
    justify-content: space-between;
    padding: 20px 0;
    .left {
      flex: 2;
      display: flex;
      align-items: center;
      justify-content: space-around;
    }
    .middle {
      flex: 5;
      display: flex;
      align-items: center;
      justify-content: space-around;
    }
    .data-style {
      .label-zb {
        color: #20212B;
        text-align: right;
      }
      .value {
        font-size: 24px;
        text-align: right;
      }
    }
  }
}
</style>

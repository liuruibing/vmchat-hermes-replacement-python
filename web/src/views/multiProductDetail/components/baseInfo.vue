<template>
  <div class="base-info">
    <div v-show="showJBXX">
      <div class="title">
        <div class="title-icon">
          <div class="color-box"></div>
        </div>
        <div class="title-txt">
          <span>基本信息</span>
        </div>
      </div>
      <div class="dataBox" id="standard-table">
        <vxe-table border show-header-overflow show-overflow auto-resize :data="tableData">
          <vxe-column field="XDATE" title="产品代码" header-align="center" align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.XDATE | noDataFilter }}</span>
            </template>
          </vxe-column>
          <vxe-column field="YDATE" title="产品名称" header-align="center" align="left">
            <template slot-scope="scope">
              <span>{{ scope.row.YDATE | noDataFilter }}</span>
            </template>
          </vxe-column>
          <vxe-column field="YDATE1" title="投资策略" header-align="center" align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.YDATE1 | noDataFilter }}</span>
            </template>
          </vxe-column>
          <vxe-column field="YDATE2" title="管理人" header-align="center" align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.YDATE2 | noDataFilter }}</span>
            </template>
          </vxe-column>
          <vxe-column field="YDATE3" title="基金经理" header-align="center" align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.YDATE3 | noDataFilter }}</span>
            </template>
          </vxe-column>
          <vxe-column field="YDATE4" title="存续状态" header-align="center" align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.YDATE4 | noDataFilter }}</span>
            </template>
          </vxe-column>
          <vxe-column field="YDATE5" title="成立日期" header-align="center" align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.YDATE5 | noDataFilter }}</span>
            </template>
          </vxe-column>
<!--          <vxe-column field="YDATE6" title="净值日期" header-align="center" align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.YDATE6 | noDataFilter }}</span>
            </template>
          </vxe-column>
          <vxe-column field="YDATE7" title="净值资产(万元)" header-align="center" align="right">
            <template slot-scope="scope">
              <span>{{ (scope.row.YDATE7 / 10000).toFixed(2) }}</span>
            </template>
          </vxe-column>
          <vxe-column field="YDATE8" title="单位净值" header-align="center" align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.YDATE8 | moneyYuanFour }}</span>
            </template>
          </vxe-column>
          <vxe-column field="YDATE9" title="累计单位净值" header-align="center" align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.YDATE9 | moneyYuanFour }}</span>
            </template>
          </vxe-column>
          <vxe-column field="YDATE10" title="复权净值" header-align="center" align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.YDATE10 | moneyYuanFour }}</span>
            </template>
          </vxe-column>-->
        </vxe-table>
      </div>
    </div>
  </div>
</template>
<script>
import fun from '@/filters/common'
import commonAPI from '@/api/common.js'
export default {
  name: 'baseInfo',
  components: {},
  props: {
    formQuery: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {
      tableData: [],
      showJBXX: false,
      canShowIndexArr: []
    }
  },
  mounted() {},
  methods: {
    async initData() {
      await this.getCanShowIndex()
      if (this.showJBXX) {
        this.getBaseInfo('7ba36967-beb1-4581-ad92-5612269d9409')
      }
    },
    getBaseInfo(sqlCode) {
      return new Promise((resolve, reject) => {
        this.tableData = []
        const params = {}
        params.indexCode = sqlCode
        ;(params.startDate = this.formQuery.startDate),
          (params.endDate = this.formQuery.endDate),
          (params.productCodes = this.formQuery.productCodes)
        params.kpiCode = this.formQuery.kpiCode
        ;(params.baseCode = this.formQuery.dbjz ? this.formQuery.dbjz.join(',') : ''),
          commonAPI
            .getDataBysqlCode(params)
            .then(res => {
              let { status, data } = res.data
              if (status == 0) {
                this.tableData = data
              }
            })
            .catch(err => {})
      })
    },
    getCanShowIndex() {
      return new Promise((resolve, reject) => {
        const params = {}
        params.templateCode = 'fa904bb2-6c85-47ae-bdff-db6f4ed570c0'
        params.fundCode = this.formQuery.productCodes
        commonAPI
          .selectIndexInfos(params)
          .then(res => {
            const { status, data } = res.data
            if (status === 0) {
              data.forEach(element => {
                this.canShowIndexArr.push(element.vcCode)
              })
              if (this.canShowIndexArr.includes('abe330fc-b66e-4be4-8f41-6e42d32de183')) {
                this.showJBXX = true
              } else {
                this.showJBXX = false
              }
            }
            resolve()
          })
          .catch(() => {
            resolve()
          })
      })
    }
  }
}
</script>
<style lang="scss" scoped>
.base-info {
  position: relative;
  // height: 2900px;
  margin: 0 30px;
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
  .titleBox {
    border-bottom: 1px solid #e03d3e;
    padding: 20px 0 10px;
    font-size: 16px;
    margin-bottom: 20px;
  }
  .title_name {
    // border-left: 2px solid #e03d3e;
    height: 16px;
    line-height: 16px;
    color: #e03d3e;
    padding-left: 5px;
  }
  .title_name_icon {
    width: 2px;
    display: inline-block;
    height: 14px;
    line-height: 14px;
    background-color: #e03d3e;
    position: relative;
    top: 1px;
    margin-right: 10px;
  }
  .noData {
    border: 1px solid #d4d4d4;
    height: 40px;
    background-color: #f7f7f7;
    text-align: center;
    line-height: 40px;
    color: #333;
    margin: 40px 30px 20px;
  }
  .dataBox {
    padding: 20px 30px 20px;
  }
}
</style>

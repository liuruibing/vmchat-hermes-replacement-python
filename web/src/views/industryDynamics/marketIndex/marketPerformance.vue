<!-- 市场表现页面 -->
<template>
  <div class="marketIndex" v-loading="pageLoading">
    <el-tabs v-model="markPerformanceActive" type="card" @tab-click="handleClick" class="standard-tab">
      <el-tab-pane label="A股规模指数" name="scaleIndex">
        <scale-index
          ref="scaleIndexRef"
          :scale-index-options-props="scaleIndexOptions"
          :estab-start-date-props="estabStartDate"
          :contras-standard-opts-props="contrasStandardOpts"
        ></scale-index>
      </el-tab-pane>
      <el-tab-pane label="行业指数" name="industryIndex">
        <industry-index
          ref="industryIndexRef"
          :industry-index-options-props="industryIndexOptions"
          :estab-start-date-props="estabStartDate"
          :contras-standard-opts-props="contrasStandardOpts"
          :contras-code-props="contrasCode"
        ></industry-index>
      </el-tab-pane>
      <el-tab-pane label="风格指数" name="styleIndex">
        <style-index
          ref="styleIndexRef"
          :style-index-options-props="styleIndexOptions"
          :estab-start-date-props="estabStartDate"
          :contras-standard-opts-props="contrasStandardOpts"
          :contras-code-props="contrasCode"
        ></style-index>
      </el-tab-pane>
      <el-tab-pane label="公募基金指数" name="publicFundIndex">
        <public-fund-index
          ref="publicFundIndexRef"
          :public-fund-index-options-props="publicFundIndexOptions"
          :estab-start-date-props="estabStartDate"
          :contras-standard-opts-props="contrasStandardOpts"
          :contras-code-props="contrasCode"
        ></public-fund-index>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import request from '@/utils/request'
import commonAPI from '@/api/common.js'
import industryIndex from './components/industryIndex'
import publicFundIndex from './components/publicFundIndex'
import scaleIndex from './components/scaleIndex'
import styleIndex from './components/styleIndex'
import { merger } from '@/utils'
export default {
  name: 'MarketIndex',
  components: {
    industryIndex,
    publicFundIndex,
    scaleIndex,
    styleIndex
  },
  provide: {
    industryIndex: {
      yjzs: '1701be5b-1651-4d09-84c6-7c5898e5766b',
      dthc: '50e14419-cff4-45f2-9d61-84442c2fcd52',
      jqbxjzrq:'c06330f8-2263-486c-a7ab-0207aeec11c4',
      jqbxtable:'8bac6e70-79cf-46e0-b51c-fafebe192b0b'
    },
    publicFundIndex: {
      yjzs: '0af5518f-a092-4b52-a103-856c640405f2',
      dthc: 'aa3a7a03-dc7f-4c60-bb09-56f282e4f35d',
      jqbxjzrq:'9d00116e-eedc-4437-bd89-7c22ab6eea4a',
      jqbxtable:'0703f8c6-a09c-4966-9ae3-afdcf2283f9b'
    },
    scaleIndex: {
      yjzs: 'd94a69d9-1008-485f-bb5e-8cd2fc7bea1f',
      dthc: '55c166bf-44b7-4016-b485-caade564537a',
      jqbxjzrq:'0df530c1-ba51-4357-9d6c-437c8243a0eb',
      jqbxtable:'a3083aa5-8fce-44a2-8477-fcb4d24dca1e'
    },
    styleIndex: {
      yjzs: '5b024f46-7a93-42f3-88e3-e39171ae5cd3',
      dthc: 'e4494b3b-adfd-4e6a-9d43-16bb2fa70fd5',
      jqbxjzrq:'013573be-eaac-4715-9137-8e9aa5b1131d',
      jqbxtable:'d294a178-629e-425f-b3a4-9530ceb4bc71'
    }
  },
  data() {
    return {
      pageLoading: false,
      markPerformanceActive: 'scaleIndex',
      isInTargetPage: false, // 是否在目标页面
      isInit: {
        industryIndex: false,
        publicFundIndex: false,
        scaleIndex: true,
        styleIndex: false
      },
      estabStartDate: '',
      contrasStandardOpts: [],
      contrasCode: [],
      // 规模指数下拉
      scaleIndexOptions: [],
      // 行业指数下拉
      industryIndexOptions: [],
      // 风格指数下拉
      publicFundIndexOptions: [],
      // 公募基金指数下拉
      styleIndexOptions: []
    }
  },
  async mounted() {
    document.addEventListener('keydown', this.handleEnterKey);
    this.checkIfInTargetPage();
    this.$watch(
      () => this.$route,
      () => {
        this.checkIfInTargetPage();
      },
      { immediate: true }
    );
    this.pageLoading = true
    await this.getStartDateFromEstab()
    await this.getContrasOptions()
    this.pageLoading = false
    // 查询指数下拉
    this.getIndexOptions()
    this.$refs.scaleIndexRef.init()
  },
  beforeDestroy() {
    document.removeEventListener('keydown', this.handleEnterKey);
  },
  methods: {
    checkIfInTargetPage() {
      // 判断当前是否在目标页面（如路由包含 'marketPerformance'）
      this.isInTargetPage = this.$route.path.includes('marketPerformance');
    },
    handleEnterKey(e) {
      if (e.key !== 'Enter') return;
      if (!this.isInTargetPage) return; // 不在目标页面时不处理
      const currentTabRef = this.$refs[`${this.markPerformanceActive}Ref`];
      if (currentTabRef && currentTabRef.handleSearch) {
        e.preventDefault(); // 阻止默认行为（如表单提交）
        currentTabRef.handleSearch(); // 调用当前 tab 的查询方法
      }
    },
    /**
     * @description 查询指数下拉
     */
    getIndexOptions() {
      return new Promise((resolve, reject) => {
        let params = {
          indexCode: '1db90f0a-e1e4-471f-bcac-f26912ba2e17'
        }
        commonAPI.getDataBysqlCode(params).then((res) => {
          const { status, data } = res.data
          if (status === 0) {
            let mergerData = merger(data, 'DIM_TYPE')
            this.scaleIndexOptions = mergerData.filter((item) => item.DIM_TYPE === 'MARKET_INDEXCODE')[0].origin
            this.industryIndexOptions = mergerData.filter((item) => item.DIM_TYPE === 'INDUSTRY_INDEXCODE')[0].origin
            this.publicFundIndexOptions = mergerData.filter((item) => item.DIM_TYPE === 'GM_INDEXCODE')[0].origin
            this.styleIndexOptions = mergerData.filter((item) => item.DIM_TYPE === 'STYLE_INDEXCODE')[0].origin
            resolve()
          } else {
            this.scaleIndexOptions = []
            this.industryIndexOptions = []
            this.publicFundIndexOptions = []
            this.styleIndexOptions = []
            reject()
          }
        })
      })
    },

    handleClick(val) {
      this.markPerformanceActive = val.name
      if (!this.isInit[val.name]) {
        this.$refs[`${val.name}Ref`].init()
        this.isInit[val.name] = true
      }
    },
    /**
     * @description 查询成立以来开始日期
     */
    getStartDateFromEstab() {
      return new Promise((resolve, reject) => {
        const params = {}
        params.indexCode = '741cb4cc-7893-43f5-bb7e-317efe0d7583'
        commonAPI
          .getDataBysqlCode(params)
          .then((res) => {
            const { status, data } = res.data
            if (status === 0) {
              if (data && data instanceof Array && data.length > 0) {
                this.estabStartDate = data[0].STARTDATE
              } else {
                this.estabStartDate = new Date().getFullYear() + '-' + (new Date().getMonth() + 1) + '-' + new Date().getDate()
              }
            } else {
              this.estabStartDate = new Date().getFullYear() + '-' + (new Date().getMonth() + 1) + '-' + new Date().getDate()
            }
            resolve()
          })
          .catch(() => {
            resolve()
          })
      })
    },

    /**
     * @description 获取对比基准下拉
     */
    getContrasOptions() {
      return new Promise((resolve, reject) => {
        request({
          url: `/api/report/v1.0/data/sql/ecd8867c-64cc-4ebc-9070-04524b04b72c`,
          method: 'post',
          data: {
            indexCode: 'ecd8867c-64cc-4ebc-9070-04524b04b72c'
          }
        })
          .then((res) => {
            if (res.data.status === 0) {
              const resultDim = res.data.data || []
              this.contrasStandardOpts = resultDim.map((item) => {
                return {
                  label: item.DIM_NME,
                  id: item.DIM_CDE
                }
              })
              this.contrasStandardOpts.forEach((item) => {
                if (item.id === '000300' || item.id === 'H11001') {
                  this.contrasCode.push(item.id)
                }
              })
            }
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
    }
  }
}
</script>

<style lang="scss">
.marketIndex {
  //.custom-tooltip {
  //  max-height: 100px; /* 限制最大高度 */
  //  overflow-y: auto;  /* 添加垂直滚动条 */
  //  scrollbar-width: thin; /* 可选：调整滚动条宽度 */
  //}
}
</style>
<style lang="scss" scoped>
::v-deep .el-tabs__nav-scroll {
  margin-left: 10px;
}
.marketIndex {
  margin-top: 12px;
  .funds-filter {
    width: 100%;
    border-bottom: 1px solid #e1e0e0;

    .dbjz {
      ::v-deep .el-select .el-input--small {
        width: 260px !important;
      }

      ::v-deep .el-select .el-select__tags {
        max-width: 234px !important;
      }
    }
  }

  .chart-main {
    width: 100%;

    .chart-title {
      padding: 10px 0;
      margin-bottom: 12px;
      border-bottom: 1px solid #0F65DD;

      .title-icon {
        vertical-align: middle;
        display: inline-block;

        .color-box {
          display: inline-block;
          height: 30px;
          width: 2px;
          background-color: #0F65DD;
        }
      }

      .title-txt {
        color: #0F65DD;
        vertical-align: middle;
        height: 35px;
        line-height: 35px;
        font-size: 16px;
        margin-left: 5px;
        display: inline-block;
      }
    }

    .chart-content {
      height: 450px;
      margin-top: 5px;

      .echarts_box {
        height: 100%;
        width: 100%;
      }
    }
  }
}
</style>

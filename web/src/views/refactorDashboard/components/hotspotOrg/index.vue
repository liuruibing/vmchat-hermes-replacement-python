<template>
  <div class="hotspot-org">
    <el-card>
      <div slot="header" class="clearfix">
        <div class="card-header">
          <span class="title-name">热点机构</span>
          <span class="link-more" @click="jumpToPage">更多 ></span>
        </div>
      </div>
      <div class="content">
        <div style="height: 290px" v-if="setupInfoArrs.length">
          <el-carousel height="100%" style="height: 100%; width: 100%; margin: auto" :autoplay="false" arrow="always">
            <el-carousel-item v-for="(setupInfoArr, i) in setupInfoArrs" :key="i">
              <el-row type="flex">
                <el-col :span="8" v-for="(item, k) in setupInfoArr" :key="k" style="padding-right: 10px;">
                  <div style="text-align: center; vertical-align: middle" class="imgBox">
                    <img :src="item.VC_LOGO_URL" style="width: 100%; height: 72px; position: relative;"/>
                  </div>
                  <div
                    @click="jumpToManager(item)"
                    class="font-special-color over-flow-nowarp pointer mt10"
                    style="height: 60px; font-size: 14px; line-height: 60px; padding-right: 10px"
                  >
                    {{ item.COMPANY_NAME }}
                  </div>
                  <div class="over-flow-nowarp" style="height: 25px; font-size: 14px; line-height: 30px; padding-right: 10px">成立日期&nbsp;:&nbsp;{{ item.FOUNDDATE }}</div>
                  <div class="over-flow-nowarp" style="height: 25px; font-size: 14px; line-height: 30px; padding-right: 10px">注册资本&nbsp;:&nbsp;{{ item.CAPITAL }}万元</div>
                  <div class="over-flow-nowarp" style="height: 25px; font-size: 14px; line-height: 30px; padding-right: 10px">基金数量&nbsp;:&nbsp;{{ item.FUND_NUM }}只</div>
                  <div class="over-flow-nowarp" style="height: 25px; font-size: 14px; line-height: 30px; padding-right: 10px">自主管理规模&nbsp;:&nbsp;{{ item.MANAGE_ASSET }}</div>
                  <div class="over-flow-nowarp" style="height: 25px; font-size: 14px; line-height: 30px; padding-right: 10px">员工人数&nbsp;:&nbsp;{{ item.STAFF_NUM }}人</div>
                </el-col>
              </el-row>
            </el-carousel-item>
          </el-carousel>
        </div>
        <div class="noDataStyle" v-else>
          <img :src="imgUrl" alt="" />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import commonApi from '@/api/common'
import img from '@/assets/img/nullData.png'

export default {
  name: 'HotspotOrg',
  data() {
    return {
      setupInfoArrs: [],
      imgUrl: img
    }
  },
  methods: {
    initData() {
      this.getSetupInfo()
    },
    /** 获取机构信息 */
    getSetupInfo() {
      commonApi
        .getDataBysqlCode({
          indexCode: 'bc6925b1-1e8c-40ca-9455-aa42e501bef9'
        })
        .then((res) => {
          let { status, data } = res.data
          if (status === 0) {
            this.setupInfoArrs = []
            for (var i = 0; i < data.length; i += 3) {
              this.setupInfoArrs.push(data.slice(i, i + 3))
            }
            console.log(this.setupInfoArrs)
          }
        })
        .catch(() => {})
    },
    /** 跳转管理人详情 */
    jumpToManager(data) {
      let newObj = {
        company_id: data.COMPANY_ID,
        manager_name: data.COMPANY_NAME
      }
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/tqgl/glrxq',
        query: { managerList: newObj }
      })
    },
    jumpToPage() {
      this.$router.push('/hydt/smrd/rdjgdt')
    }
  }
}
</script>

<style lang="scss" scoped>
@import url('../../style/index.scss');
.hotspot-org {
  .font-special-color {
    color: #005ba1;
  }
}
::v-deep .el-carousel__item {
  z-index: -1;
}

::v-deep .el-carousel__item.is-active {
  z-index: 2;
}
::v-deep .el-carousel__indicators.el-carousel__indicators--horizontal {
  display: none;
}
</style>

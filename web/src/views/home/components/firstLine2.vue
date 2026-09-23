<template>
  <el-row :gutter="20" justify="start" type="flex">
    <el-col :span="16">
      <div style="height: 229px;width: 100%">
        <el-carousel height="100%" style="height: 100%;width: 100%;margin: auto;">
          <el-carousel-item v-for="(item, index) in bannerInfoArr" :key="index">
            <!-- <img alt="" src="../../../assets/img/banner.png" srcset="" style="width: 100%; height: 100%"> -->
            <img alt="" :src="item.VC_FILEURL" srcset="" style="width: 100%; height: 100%;cursor: pointer"
                 @click="toArticleDetails(item)" />
          </el-carousel-item>
        </el-carousel>
      </div>
    </el-col>
    <el-col :span="8">
      <barometer></barometer>
    </el-col>
  </el-row>
</template>
<script>
import boxTemplate from './boxTemplate'
import commonApi from '@/api/common'
import barometer from "./barometer";
export default {
  name: 'firstLine',
  components: { boxTemplate,barometer },
  data() {
    return {
      imageStyle: {
        // 背景图片地址
        backgroundImage: 'url(' + require('../../../assets/img/banner.png') + ')',
        // 背景图片是否重复
        backgroundRepeat: 'no-repeat',
        // 背景图片大小
        backgroundSize: 'cover',
        // 背景颜色
        // backgroundColor: '#000',
        // 背景图片位置
        backgroundPosition: 'center top'
      },
      boxArray: [
        {
          iconName: 'market',
          content: '全市场筛选'
        },
        {
          iconName: 'process',
          content: '托管外包产品筛选'
        },
        {
          iconName: 'product',
          content: '基金经理'
        },
        {
          iconName: 'eval',
          content: '管理人筛选'
        },
        {
          iconName: 'pene',
          content: '模拟组合'
        },
        {
          iconName: 'product',
          content: '我的组合'
        },
        {
          iconName: 'mix',
          content: '绩效归因'
        },
        {
          iconName: 'performance',
          content: '市场动态'
        }
      ],
      tableData: [
        {
          name: '全国银行间债券市场准入备案',
          date: '2022年9月10日'
        },
        {
          name: '中国金融期货交易所交易结算会员',
          date: '2022年9月15日'
        },
        {
          name: '就期货合约提供意见资格',
          date: '2022年9月18日'
        },
        {
          name: '依法合规加大对平台经济重点领域的金融支持',
          date: '2022年9月5日'
        }
      ],
      bannerInfoArr: []
    }
  },
  mounted() {
    this.getImgInfo()
  },
  methods: {
    more() {},
    handleBoxClick(content) {
      if (content == '全市场筛选') {
        this.$router.push({
          path: '/tqgl/qscsmcpsx'
        })
      }
      if (content == '托管外包产品筛选') {
        this.$router.push({
          path: '/tqgl/tgwbcpsx'
        })
      }
      if (content == '准入流程管理') {
        this.$router.push({
          path: '/tzgl/zrlcgl'
        })
      }
    },
    //获取首页轮播图信息
    getImgInfo() {
      commonApi
        .getDataBysqlCode({
          indexCode: '599215d1-6c93-4ee5-9063-0bf032b01889'
        })
        .then(res => {
          let { status, data } = res.data
          if (status === 0) {
            this.bannerInfoArr = data
          }
        })
        .catch(() => {})
    },
    toArticleDetails(data) {
      this.$router.push({
        path: '/hydt/articleDetails',
        query: {
          fid: data.F_ID,
          flag: '1'
        }
      })
      this.$store.commit('SET_FROMPAGEJUMP', true)
    }
  }
}
</script>
<style lang="scss" scoped>
.el-carousel__item h3 {
  color: #475669;
  font-size: 14px;
  opacity: 1;
  line-height: 150px;
  margin: 0;
}

.el-carousel__item:nth-child(2n) {
  //background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n + 1) {
  //background-color: #d3dce6;
}

::v-deep .el-table--scrollable-y .el-table__body-wrapper {
  overflow-y: hidden;
}

.dashboard-title {
  font-size: 18px;
  // font-weight: 600;
  margin-right: 16px;
}

.box-style {
  background: -webkit-linear-gradient(left, #e46c68, #d93935);
  width: 100%;
  height: 100px;
}

.icon-style {
  font-size: 36px;
  color: white;
}

.elLink {
  width: 34px;
  color: #2672bc;
  font-size: 14px;
}
</style>

<template>
  <div class="dynamic-condition">
    <el-card>
      <div slot="header" class="clearfix">
        <el-row class="card-header" type="flex" justify="space-around">
          <el-col :span="4">
            <span class="title-name">
              <img src="./assets/img/GF.png" style="height:18px;width:18px" />
            <span>广发资讯</span>
          </span>
          </el-col>
          <el-col :span="20" style="text-align: right">
<!--            <span class="toogle-tab">
              <span v-for="tab in activeTabs" :key="tab.key" class="tab-item"
                    :class="tab.key === active ? 'tab-item-active ' : ''" @click="toogleActive(tab.key)">
                {{ tab.name }}
              </span>
            </span>-->
            <span class="link-more" @click="handleMoreClick">更多 ></span>
          </el-col>
        </el-row>
      </div>
      <div class="content" style="overflow-y: auto">
        <template v-if="tableData[active].length > 0">
          <div class="content-item" v-for="item in tableData[active]" style="height: auto;">
            <div class="page-container">
              <div class="left-column">
                <div class="content-title" @click="handleTitleClick(item)"><span class="hover-click">{{ item.VC_NTITLE }}</span></div>
                <div class="content-subtitle mt10">
                  <span>{{ item.VC_NAUTHOR }}</span>
                  <span class="ml20">{{ item.VC_NDATE }}</span>
                  <span class="ml20">{{ item.VC_ORGAN }}</span>
                </div>
                <div class="content-main">{{ item.VC_NSUMMARY }}</div>
              </div>
              <div class="right-column">
                <img :src="item.VC_FILEURL" width="200px" height="120px" style="object-fit: cover;"/>
              </div>
            </div>
          </div>
        </template>
        <div v-else class="noDataStyle" style="height: 290px;">
          <img :src="noDataImgUrl" alt=""/>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import commonApi from '@/api/common'
import fun from '@/filters/common'
import img from '@/assets/img/nullData.png'
import {selectArticle} from './script/api'
export default {
  name: 'DynamicCondition',
  data() {
    return {
      noDataImgUrl: img,
      active: 'yhzx',
      activeTabs: [
        {key: 'yhzx', name: '广发资讯'},

        {key: 'smgd', name: '私募观点'},
      ],
      //  {key: 'gfzx', name: '监管动态'}, 备份
      tableData: {
        yhzx: [],
        smgd: [],
        gfzx: [],
      },
      blobImages:[],
      // tableData: {
      //   yhzx: [
      //     {
      //       title: '广发说 | 基金入市投教问答',
      //       author: '托管新闻组',
      //       time: '2024-07-02',
      //       industry: '广发证券',
      //       content: '为贯彻落实新“国九条”部署，助力培育长期投资的市场生态,银小河制作基金入市投教问答系列，帮助投资者了解基金基础知识，树立理性投资、价值投资、长期投资理念。',
      //       img: require('./assets/img/广发资讯-1.png')
      //     },
      //     {
      //       title: '喜讯！广发证券资产托管业务再度通过ISAE3402国际鉴证！',
      //       author: '托管新闻组',
      //       time: '2024-04-01',
      //       industry: '广发证券',
      //       content: '2024年3月29日，广发证券资产托管业务再度通过ISAE3402国际鉴证，连续三个完整会计年度通过该项国际鉴证，标志着广发证券资产托管业务在服务能力、运营效能、安全保障、内部控制体系等方面持续保持国际水准，更体现了广发证券对托管业务的高度重视。',
      //       img: require('./assets/img/广发资讯-2.png')
      //     },
      //   ],
      //   smgd: [
      //     {
      //       title: '百亿私募淡水泉的最新投资观点：2024下半场聚焦部分复合型行业龙头',
      //       author: '托管新闻组',
      //       time: '2024-06-13',
      //       industry: '广发证券',
      //       content: '起起伏伏，上证指数又回到了3000点附近。经历了春节前后风格极致化的考验，5月以来，ST股、微盘股暴跌，A股2024年下半场也同样渐行渐近。',
      //       img: require('./assets/img/私募观点-1.png')
      //     },
      //     {
      //       title: 'A股关键时刻！私募大佬最新发声',
      //       author: '托管新闻组',
      //       time: '2024-06-24',
      //       industry: '广发证券',
      //       content: '今年上半年，A股、港股市场迎来一波上涨，但临近年中市场又出现持续回调，上证指数再度开启3000点“保卫战”，投资者对下半年市场何去何从较为困惑。',
      //       img: require('./assets/img/私募观点-2.png')
      //     },
      //   ],
      //   gfzx: [
      //     {
      //       title: '证监会就进一步全面深化资本市场改革开展专题调研',
      //       author: '托管新闻组',
      //       time: '2024-06-28',
      //       industry: '广发证券',
      //       content: '为深入贯彻习近平总书记关于全面深化改革的重要论述，认真落实中央金融工作会议和新“国九条”有关部署，近日证监会党委书记、主席吴清与其他班子成员先后在深圳、广州、上海、北京等地，围绕进一步全面深化资本市场改革开展调研，通过召开座谈会、实地走访等方式，分别与上市公司、行业机构、投资者、专家学者及系统单位代表深入交流，充分听取意见建议。',
      //       img: require('./assets/img/官方资讯-1.jpg')
      //     },
      //     {
      //       title: '全国科技大会 国家科学技术奖励大会 两院院士大会在京召开 习近平为国家最高科学技术奖获得者等颁奖并发表重要讲话',
      //       author: '托管新闻组',
      //       time: '2024-06-26',
      //       industry: '广发证券',
      //       content: '全国科技大会 国家科学技术奖励大会 两院院士大会在京召开习近平为国家最高科学技术奖获得者等颁奖并发表重要讲话强调，科技兴则民族兴，科技强则国家强。中国式现代化要靠科技现代化作支撑，实现高质量发展要靠科技创新培育新动能。必须充分认识科技的战略先导地位和根本支撑作用，锚定2035年建成科技强国的战略目标，加强顶层设计和统筹谋划，加快实现高水平科技自立自强',
      //       img: require('./assets/img/官方资讯-2.jpg')
      //     },
      //   ]
      // },

    }
  },
  mounted() {
    this.getArticleData()
  },
  beforeDestroy(){
    this.destroyImages();

  },
  methods: {
    // 点击标题跳转
    async handleTitleClick(item) {
      if (item.VC_FLAGTYPE == '3') {
        const params = {
          fid: item.F_ID
        }
        await selectArticle(params).then(res => {
          if (res.data.status === 0) {
            const resultData = res.data.data.article || ''
            let url = resultData.content.replace(/<\/?[^>]+(>|$)/g, "")
            window.open(url)
          } else {
            this.$message.closeAll()
            this.$message.warning('公众号地址不存在，跳转失败')
          }
        })
        return
      }
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/hydt/articleDetails',
        query: {
          fid: item.F_ID,
          type: item.VC_FLAG,
          flag: item.VC_FLAGTYPE
        }
      })
    },
    getArticleData() {
      commonApi
        .getDataBysqlCode({
          indexCode: '6795ac5d-bd23-4f89-a003-397020968e7d'
        })
        .then(async(res) => {
          const { status, data } = res.data
          if (status === 0) {
            await Promise.all([
              data.map(this.processElement)
            ])

            this.tableData.yhzx = data.filter((item) => item.VC_FLAG === '2')
            this.tableData.smgd = data.filter((item) => item.VC_FLAG === '3')
            this.tableData.gfzx = data.filter((item) => item.VC_FLAG === '1')
          }
        })
        .catch(() => {
        })
    },
    async processElement(element) {
      element.noMargin = true
      element.VC_NDATE = fun.yyr_timestampToTime(element.VC_NDATE)
      if (element.uuid && !element.VC_FILEURL) {
        let imageUrL = await commonApi.manageS3SelectFileVueBlob(element.uuid)
        this.$set(element, 'VC_FILEURL', imageUrL);
        this.blobImages.push(imageUrL)
      }
    },

    initData() {
    },
    toogleActive(val) {
      this.active = val
    },
    handleMoreClick() {
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/hydt/zxdt/fxpl',
        query: {fileType: this.active}
      })
    },
  async  destroyImages() {
    this.blobImages.forEach(url => {
      if (url) {
        URL.revokeObjectURL(url);
      }
    });
    this.blobImages = []; // 清空数组，避免重复释放或错误引用已释放的 URL
  }
  }
}
</script>

<style lang="scss" scoped>
@import url('../../style/index.scss');

.hover-click:hover{
  cursor: pointer;
}
.toogle-tab {
  //margin-left: 760px;
}

.page-container {
  display: flex; /* 使用flex布局 */
  margin: 10px;
  height: 120px;
}

.left-column {
  flex: 1; /* 左侧栏自适应，占据剩余空间 */
  height: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-right: 20px;
  //white-space: nowrap;
  /* 可以添加其他样式，例如背景色、边距等 */
}

.right-column {
  width: 200px; /* 右侧栏固定宽度 */
  /* 可以添加其他样式，例如背景色、边距等 */
}
</style>

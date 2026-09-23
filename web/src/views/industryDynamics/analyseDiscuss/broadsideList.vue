<template>
  <div class="broadsideList">
    <div class="title" @click="toArticleDetails(asidePageData1)">
      <div><span style="font-size:18px;font-weight:bold">“</span></div>
      <div :title="asidePageData1.title || '-'">
        {{ asidePageData1.title }}
        <br />
      </div>
      <div class="content" :title="asidePageData1.summary || '-'">
        {{ asidePageData1.summary }}
        <br />
      </div>
      <div><span style="font-size:18px;color:#909399;font-weight:bold">”</span></div>
    </div>
    <div class="img">
      <img :src="asidePageData1.img" width="100%" height="100%" />
    </div>
    <div class="line"></div>
    <div
      class="listItem"
      v-for="(item, index) in asidePageData2"
      :key="index"
      @click="toArticleDetails(item)"
    >
      <div class="listTitle ellipsisOne" :title="item.title || '-'">{{ item.title }}</div>
      <div class="listContent ellipsisOne" :title="item.summary || '-'">{{ item.summary }}</div>
    </div>
    <ul class="ulBox">
      <li v-for="(item, index) in asidePageData3" :key="index" @click="toArticleDetails(item)">
        <span class="crcle"></span>
        <span :title="item.summary || ''">{{ item.summary }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
import commonApi from '@/api/common'
import fun from '@/filters/common'
export default {
  components: {},
  props: {
    isActive: {
      type: String,
      default: '1'
    },
    asideData1: {
      type: Object,
      default: {}
    },
    asideData2: {
      type: Array,
      default: []
    },
    asideData3: {
      type: Array,
      default: []
    }
  },
  data() {
    return {
      asidePageData1: {},
      asidePageData2: [],
      asidePageData3: []
    }
  },
  watch: {
    asideData1: {
      handler(newVal) {
        this.asidePageData1 = this.asideData1
      },
      deep: true
    },
    asideData2: {
      handler(newVal) {
        this.asidePageData2 = this.asideData2
      },
      deep: true
    },
    asideData3: {
      handler(newVal) {
        this.asidePageData3 = this.asideData3
      },
      deep: true
    }
  },
  mounted() {},
  methods: {
    // 获取研报数据
    getArticleData(type) {
      commonApi
        .getDataBysqlCode({
          indexCode: '9869edb0-e8ab-4089-9bae-185fec8b9b8b',
          narearType: type, //type代表页面不同部分
          fileType: 3 //1：文章，2：视频
        })
        .then(res => {
          const { status, data } = res.data
          if (status === 0) {
            data.forEach(element => {
              element.VC_NDATE = fun.timeFormat(element.VC_NDATE)
            })
            if (type == 3) {
              this.asideData1 = data[0]
            } else if (type == 4) {
              this.asideData2 = data.slice(0, 3)
            } else if (type == 5) {
              this.asideData3 = data.slice(0, 3)
            }
          }
        })
        .catch(() => {})
    },
    toArticleDetails(data) {
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/hydt/articleDetails',
        query: {
          fid: data.fid,
          flag: '1'
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.broadsideList {
  padding: 20px 20px 0 20px;
  .title {
    padding: 10px 15px;
    width: 100%;
    height: 220px;
    background-color: #f1f3ff;
    text-align: center;
    font-size: 18px;
    cursor: pointer;
  }
  .content {
    font-size: 14px;
    text-align: left;
    text-indent: 30px;
    margin: 10px 0;
    color: #999;
    -webkit-line-clamp: 4;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  .img {
    height: 200px;
  }
  .line {
    border-top: 1px solid black;
    margin: 30px 0 25px;
  }
  .listItem {
    cursor: pointer;
    // line-height: 25px;
    margin-bottom: 15px;
    .listTitle {
      font-size: 14px;
      margin-bottom: 5px;
      font-weight: bold;
    }
    .listContent {
      font-size: 14px;
    }
  }
  .ellipsisOne {
    display: -webkit-box;
    overflow: hidden;
    white-space: normal !important;
    text-overflow: ellipsis;
    word-wrap: break-word;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
  }
  .crcle {
    display: inline-block;
    width: 4px;
    height: 4px;
    border-radius: 2px;
    background-color: black;
    margin-right: 10px;
    position: relative;
    top: -2px;
  }
  .ulBox {
    cursor: pointer;
    li {
      margin-bottom: 5px;
      -webkit-line-clamp: 4;
      display: -webkit-box;
      -webkit-box-orient: vertical;
      overflow: hidden;
      // font-weight: bold;
    }
  }
}
</style>

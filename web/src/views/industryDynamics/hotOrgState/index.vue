<template>
  <div class="hot-org">
    <el-row>
      <el-col class="left-comp">
        <div class="title">百亿+私募证券类管理人</div>
        <left-component :leftCompArr="leftCompArr"></left-component>
      </el-col>
      <el-col class="right-comp">
        <div class="title">私募基金管理人新发产品排名（近三月）</div>
        <el-carousel height="100%" style="height: 100%; width: 100%; padding: 5px" :autoplay="false" arrow="always">
          <el-carousel-item v-for="(row, index) in rightCompArr" :key="index">
            <div class="item-content" v-for="item in row" :key="item.F_ID">
              <rightComponent :fund-item="item" />
            </div>
          </el-carousel-item>
        </el-carousel>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import leftComponent from './components/leftComponent'
import rightComponent from './components/rightComponent'
import commonApi from '@/api/common'

export default {
  name: 'hotOrg',
  components: {
    rightComponent,
    leftComponent
  },
  data() {
    return {
      rightCompArr: [],
      leftCompArr: []
    }
  },
  created() {
    this.getRightCompData()
    this.getleftCompData()
  },
  methods: {
    getleftCompData() {
      commonApi
        .getDataBysqlCode({
          indexCode: 'e78a9b23-727f-4d18-95d0-ae83cdb6229a'
        })
        .then((res) => {
          const { status, data } = res.data
          if (status === 0) {
            const leftData = []
            for (var i = 0; i < data.length; i += 4) {
              leftData.push(data.slice(i, i + 4))
            }
            this.leftCompArr = leftData
          }
        })
        .catch(() => {})
    },
    getRightCompData() {
      commonApi
        .getDataBysqlCode({
          indexCode: '44b75222-798a-4b64-8031-6b34fba56df2'
        })
        .then((res) => {
          const { status, data } = res.data
          if (status === 0) {
            const rightData = []
            for (var i = 0; i < data.length; i += 3) {
              rightData.push(data.slice(i, i + 3))
            }
            this.rightCompArr = rightData
          }
        })
        .catch(() => {})
    }
  }
}
</script>

<style lang="scss" scoped>
.hot-org {
  margin: 20px 0;
  padding: 0 20px;

  .left-comp {
    height: 920px;
    width: calc(100% - 420px);
    /*border-top: 1px solid #000;*/
    margin-right: 20px;
  }

  .right-comp {
    height: 920px;
    width: 400px;
    /*border-top: 1px solid #000;*/
    padding: 0 20px 20px 20px;
    background-color: #fafafa;
  }

  .title {
    padding: 20px 0;
    font-size: 16px;
    font-weight: bold;
    color: #5f6978;
  }
}
</style>

<template>
  <div class="rightComponent">
    <div class="title_box">
      <img :src="fundItem.VC_SMALLLOGO_URL" alt="" class="fundIcon" />
      <!-- <img src="./1.png" alt="" class="fundIcon"> -->
      <span class="fundName" @click="jumpToManager()">{{ fundItem.COMPANY_SHORT_NAME }}</span>
    </div>
    <p class="fundIntroduce" :title="fundItem.VC_DESCRIPTION || '-'">{{ fundItem.VC_DESCRIPTION }}</p>
    <el-row type="flex" justify="space-between" class="item_box">
      <el-col :span="12" class="item_key">员工人数</el-col>
      <el-col :span="12" class="item_value">{{ fundItem.STAFF_NUM || '-' }}人</el-col>
    </el-row>
    <el-row type="flex" justify="space-between" class="item_box">
      <el-col :span="12" class="item_key">旗下产品</el-col>
      <el-col :span="12" class="item_value">{{ fundItem.FUND_NUM || '-' }}只</el-col>
    </el-row>
    <el-row type="flex" justify="space-between" class="item_box">
      <el-col :span="12" class="item_key">机构证券自主管理规模</el-col>
      <el-col :span="12" class="item_value">{{ fundItem.COMPANY_ASSET_SIZE || '-' }}元</el-col>
    </el-row>
    <el-row type="flex" justify="space-between" class="item_box">
      <el-col :span="12" class="item_key">近一年收益率</el-col>
      <el-col :span="12" class="item_value" :style="colorFilter(fundItem.F_RET_1Y)">
        {{ fundItem.F_RET_1Y | numberToFixedStr(2, 100, '%') }}
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  props: {
    fundItem: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    return {}
  },
  methods: {
    /**
     * @description 收益率颜色过滤
     */
    colorFilter(num) {
      if (!num || Number(num) === 0) {
        return 'color: #000'
      }
      if (Number(num) > 0) {
        return 'color: red'
      } else {
        return 'color: green'
      }
    },
    /**
     * @description 跳转管理人详情
     */
    jumpToManager(data) {
      let newObj = {
        company_id: this.fundItem.COMPANY_ID,
        manager_name: this.fundItem.COMPANY_NAME
      }
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/tqgl/glrxq',
        query: { managerList: newObj }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.rightComponent {
  border-top: 1px solid #ededed;
  padding: 20px 0;
  color: #333;
  font-size: 14px;
  .title_box {
    margin-bottom: 10px;
  }
  .fundIcon {
    width: 30px;
    height: 30px;
    vertical-align: middle;
  }
  .fundName {
    display: inline-block;
    line-height: 30px;
    font-size: 16px;
    color: #005ba1;
    vertical-align: middle;
    cursor: pointer;
  }
  .fundIntroduce {
    font-size: 14px;
    margin-bottom: 20px;
    text-indent: 3.3em;
    overflow: hidden; //多出的隐藏
    text-overflow: ellipsis; //多出部分用...代替
    display: -webkit-box; //定义为盒子模型显示
    -webkit-line-clamp: 3; //用来限制在一个块元素显示的文本的行数
    -webkit-box-orient: vertical; //从上到下垂直排列子元素（设置伸缩盒子的子元素排列方式）
  }
  .item_box {
    margin-bottom: 10px;
    font-size: 14px;
  }
  .item_value {
    text-align: right;
  }
}
</style>

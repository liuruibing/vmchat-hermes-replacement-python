<template>
  <div class="rightComponent">
    <div class="title_box">
      <smallS3Image :s3FileId="fundItem.VC_SMALLLOGO_FILE_ID"></smallS3Image>
<!--      <img :src="fundItem.VC_SMALLLOGO_URL" alt="" class="fundIcon" />-->
      <!-- <img src="./1.png" alt="" class="fundIcon"> -->
      <span class="fundName" @click="jumpToManager()">{{ fundItem.full_name_cn }}</span>
    </div>
    <p class="fundIntroduce" :title="fundItem.vc_description || '-'">{{ fundItem.vc_description }}</p>
    <el-row type="flex" justify="space-between" class="item_box">
      <el-col :span="12" class="item_key">员工人数</el-col>
      <el-col :span="12" class="item_value">{{ fundItem.emp_number || '-' }}人</el-col>
    </el-row>
    <el-row type="flex" justify="space-between" class="item_box">
      <el-col :span="12" class="item_key">旗下产品</el-col>
      <el-col :span="12" class="item_value">{{ fundItem.fund_count || '-' }}只</el-col>
    </el-row>
    <el-row type="flex" justify="space-between" class="item_box">
      <el-col :span="12" class="item_key">机构证券自主管理规模</el-col>
      <el-col :span="12" class="item_value">{{ fundItem.manage_scale || '-' }}元</el-col>
    </el-row>
<!--    <el-row type="flex" justify="space-between" class="item_box">
      <el-col :span="12" class="item_key">近一年收益率</el-col>
      <el-col :span="12" class="item_value" :style="colorFilter(fundItem.F_RET_1Y)">
        {{ fundItem.F_RET_1Y | numberToFixedStr(2, 100, '%') }}
      </el-col>
    </el-row>-->
  </div>
</template>

<script>
import smallS3Image from './smallS3Image.vue'

export default {
  components: { smallS3Image },
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
        reg_code: this.fundItem.reg_code,
        org_code: this.fundItem.org_code
      }
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/hydt/glrcx/glrxq',
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

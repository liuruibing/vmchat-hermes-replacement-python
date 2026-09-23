<template>
  <div class="org-list-container">
    <div
      class="org-item"
      v-for="item in leftCompArr"
      :key="item.F_ID || item.reg_code"
    >
    <div class="item-content">
      <div class="content-left">
        <div class="org-name">
          <smallS3Image :s3FileId="item.VC_SMALLLOGO_FILE_ID"></smallS3Image>
          <span style="vertical-align: middle; cursor: pointer" @click="jumpToManager(item)">
              {{ item.full_name_cn || '-' }}
            </span>
        </div>
        <div class="org-content" :title="item.vc_description || ''">
          {{ item.vc_description || '' }}
        </div>
        <div class="org-params">
          <div class="params">
            <div class="count">{{ item.fund_count || '-' }}</div>
            <div class="txt">旗下产品</div>
          </div>
          <div class="params">
            <div class="count">{{ item.manage_scale || '-' }}</div>
            <div class="txt">管理规模</div>
          </div>
          <div class="params">
            <div class="count">{{ item.emp_number || '-' }}</div>
            <div class="txt">员工人数</div>
          </div>
          <div class="params">
            <el-tooltip effect="dark" :content="item.main_fund_type || '-'" placement="top">
              <div class="count">{{ item.main_fund_type || '-' }}</div>
            </el-tooltip>
            <div class="txt">管理基金主要类别</div>
          </div>
        </div>
      </div>
      <div class="content-right">
        <largeS3Image :s3FileId="item.VC_LOGO_FILE_ID"></largeS3Image>
      </div>
    </div>
  </div>
  </div>
</template>

<script>
import smallS3Image from './smallS3Image.vue'
import largeS3Image from './largeS3Image.vue'
export default {
  name: 'hotOrgLeft',
  components: {
    smallS3Image,
    largeS3Image,
  },
  props: {
    leftCompArr: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    /**
     * @description 跳转管理人详情
     */
    jumpToManager(row) {
      let newObj = {
        reg_code: row.reg_code,
        org_code: row.org_code,
        credit_code:row.credit_code
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
.org-list-container {
  height: 650px;
  overflow-y: auto;
  overflow-x: hidden;
  border-top: 1px solid #eee;

  &::-webkit-scrollbar {
    width: 6px; // 滚动条宽度
  }
  &::-webkit-scrollbar-track {
    background: #f5f5f5; // 滚动条轨道背景
    border-radius: 3px;
  }
  &::-webkit-scrollbar-thumb {
    background: #dcdcdc; // 滚动条滑块颜色
    border-radius: 3px;
  }
  &::-webkit-scrollbar-thumb:hover {
    background: #cacaca; // 鼠标悬浮时滑块颜色
  }
}

.org-item {
  .item-content {
    height: 200px;
    padding: 20px 0;
    border-bottom: 1px solid #eee;
    display: flex;
    .content-left {
      width: calc(100% - 200px);
      .org-name {
        color: #005ba1;
        font-size: 16px;
        padding-bottom: 15px;
      }
      .org-content {
        color: #333;
        padding-right: 20px;
        font-size: 14px;
        font-family: Arial, 'Microsoft Yahe', '微软雅黑';
        text-indent: 3.3em;
        overflow: hidden; //多出的隐藏
        text-overflow: ellipsis; //多出部分用...代替
        display: -webkit-box; //定义为盒子模型显示
        -webkit-line-clamp: 2; //用来限制在一个块元素显示的文本的行数
        -webkit-box-orient: vertical; //从上到下垂直排列子元素（设置伸缩盒子的子元素排列方式）
      }
      .org-params {
        display: flex;
        justify-content: space-around;
        padding-top: 22px;
        .params {
          width: 25%;
          .count {
            color: red;
            font-size: 16px;
            text-align: center;
            overflow: hidden; //多出的隐藏
            text-overflow: ellipsis; //多出部分用...代替
            display: -webkit-box; //定义为盒子模型显示
            -webkit-line-clamp: 1; //用来限制在一个块元素显示的文本的行数
            -webkit-box-orient: vertical; //
          }
          .txt {
            text-align: center;
          }
        }
      }
    }
    .content-right {
      width: 300px;
      text-align: right;
    }
  }
}
</style>

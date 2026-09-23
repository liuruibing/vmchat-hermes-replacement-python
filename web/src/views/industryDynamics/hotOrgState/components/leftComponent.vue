<template>
  <div class="org-item">
    <el-carousel height="100%" style="height: 100%; width: 100%; padding: 5px" :autoplay="false" arrow="always">
      <el-carousel-item v-for="(row, index) in leftCompArr" :key="index">
        <div class="item-content" v-for="item in row" :key="item.F_ID">
          <div class="content-left">
            <div class="org-name">
              <img style="vertical-align: middle" :src="item.VC_SMALLLOGO_URL" alt="" height="30" width="30" />
              <span style="vertical-align: middle; cursor: pointer" @click="jumpToManager(item)">
                {{ item.COMPANY_NAME || '-' }}
              </span>
            </div>
            <div class="org-content" :title="item.VC_DESCRIPTION || '-'">
              {{ item.VC_DESCRIPTION || '-' }}
            </div>
            <div class="org-params">
              <div class="params">
                <div class="count">{{ item.FUND_NUM || '-' }}</div>
                <div class="txt">旗下产品</div>
              </div>
              <div class="params">
                <div class="count">{{ item.COMPANY_ASSET_SIZE || '-' }}</div>
                <div class="txt">机构证券自主管理规模</div>
              </div>
              <div class="params">
                <div class="count">{{ item.STAFF_NUM || '-' }}</div>
                <div class="txt">员工人数</div>
              </div>
              <div class="params">
                <el-tooltip effect="dark" :content="item.MANAGE_TYPE || '-'" placement="top">
                  <div class="count">{{ item.MANAGE_TYPE || '-' }}</div>
                </el-tooltip>
                <div class="txt">管理基金主要类别</div>
              </div>
            </div>
          </div>
          <div class="content-right">
            <img :src="item.VC_LOGO_URL" alt="" height="72" width="188" />
          </div>
        </div>
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script>
export default {
  name: 'hotOrgLeft',
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
        company_id: row.COMPANY_ID,
        manager_name: row.COMPANY_NAME
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
.org-item {
  height: 100%;
  border-top: 1px solid #eee;
  .el-carousel__item {
    z-index: -1;
  }

  .el-carousel__item.is-active {
    z-index: 2;
  }
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

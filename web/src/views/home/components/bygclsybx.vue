<template>
  <div class="bygclsybx">
    <div class="title">
      <el-row type="flex">
        <el-col :span="22">
          <span class="titletitle">
            广发私募指数当年收益概况
            <span>（{{ date }}）</span>
          </span>
        </el-col>
        <el-col :span="2">
          <div class="search_button_com">
            <span style="font-size: 14px">
              <!--              <el-link-->
              <!--                :underline="false"-->
              <!--                type="primary"-->
              <!--                @click=""-->
              <!--              ><span class="elLink">{{ moreStr }}</span></el-link>-->
            </span>
          </div>
        </el-col>
      </el-row>
    </div>
    <div class="content">
      <div class="item" v-for="(item, index) in list" :key="index">
        <div class="item_name" :title="item.DIM_NME">{{ item.DIM_NME }}</div>
        <div class="item_line"></div>
        <div class="item_value" style="text-align: right;">
          <!-- <span :class="color_(item.F_YIELD)">{{ item.F_YIELD | moneyYuan }}{{index>4?'%':''}}</span> ratioThousand -->
          <span :class="color_(item.F_YIELD)">{{ item.F_YIELD | numberToFixedStr(2, 100, '%') }}</span>
        </div>
      </div>
    </div>
    <div style="border-bottom: 1px solid #333333;margin-top: 10px;"></div>
  </div>
</template>

<script>
import commonApi from '@/api/common'
export default {
  name: 'bygclsybx',
  data() {
    return {
      moreStr: 'More>',
      list: [],
      date: ''
    }
  },
  computed: {
    color_() {
      return val => {
        if (!val || val == '0') return ''
        if (val > 0) {
          return 'red'
        } else {
          return 'green'
        }
      }
    }
  },
  mounted() {
    this.getIndexData()
  },
  methods: {
    getIndexData() {
      commonApi
        .getDataBysqlCode({
          indexCode: '3ba2af39-bbe0-42ef-b845-5540577d789a'
        })
        .then(res => {
          let { status, data } = res.data
          if (status === 0) {
            this.list = data
            if (this.list.length) {
              this.date = this.list[0].D_DATE
            }
          }
        })
        .catch(() => {})
    }
  }
}
</script>

<style lang="scss" scoped>
.bygclsybx {
  .title {
    height: 30px;

    .titletitle {
      position: relative;
      font-size: 18px;
      margin-right: 12px;
      line-height: 30px;
      vertical-align: middle;
      text-align: center;
      // font-weight: 600;
    }
    .titletitle span {
      font-size: 14px;
      position: relative;
      top: -2px;
    }
    .title-button-left {
      display: inline-block;
      position: absolute;
      top: 5px;
      left: 83px;
      border: 1px solid #000000;
      width: 70px;
      height: 22px;
      line-height: 22px;
      font-size: 14px;
      padding-left: 13px;
      -webkit-border-radius: 40px 0px 0px 40px;
      -moz-border-radius: 40px 0px 0px 40px;
      border-radius: 40px 0px 0px 40px;
    }

    .title-button-center {
      display: inline-block;
      border: 1px solid #000000;
      border-left: none;
      width: 70px;
      height: 22px;
      font-size: 14px;
      padding-left: 10px;
    }

    .title-button-right {
      display: inline-block;
      border: 1px solid #000000;
      border-left: none;
      position: absolute;
      top: 5px;
      left: 153px;
      line-height: 22px;
      width: 70px;
      height: 22px;
      font-size: 14px;
      padding-left: 8px;
      -webkit-border-radius: 0px 40px 40px 0px;
      -moz-border-radius: 0px 40px 40px 0px;
      border-radius: 0px 40px 40px 0px;
    }
    .button-active {
      background-color: #6b8da6;
      color: white;
    }
    .elLink {
      width: 34px;
      font-size: 14px;
      color: #2672bc;
      line-height: 30px;
      padding: 3px;
    }

    .tab {
      color: #c8993d;
      font-size: 14px;
      cursor: pointer;
    }
  }
  .content {
    height: 340px;
    overflow: auto;
    display: flex;
    flex-wrap: wrap;
    .item {
      width: 20%;
      padding: 25px 10px 20px;
      .item_name {
        font-size: 14px;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
        text-align: center;
      }
      .item_value {
        font-size: 14px;
        // font-weight: 600;
      }
      .item_line {
        height: 1px;
        background: #e3e3e3;
        margin: 10px 0;
      }
    }
  }
}

.red {
  color: #de777a;
}
.green {
  color: #81b59e;
}
</style>

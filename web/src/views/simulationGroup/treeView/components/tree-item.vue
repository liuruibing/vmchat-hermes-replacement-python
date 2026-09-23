<template>
  <div class="tree-item">
    <ul>
      <li v-for="(item, index) in treeData" :key="index">
        <div :class="{ 'line-left': index !== 0, 'line-right': index !== treeData.length - 1 }" class="item">
          <div
            :class="{
              'line-bottom': item.children && item.children.length > 0,
              'line-top item-name': item.pid !== '0',
              'first-item': item.pid === '0'
            }"
          >
            <div v-if="item.pid !== '0'" class="child-class">
              <div class="top">
                <div>{{ item.fundCode || '-' }}</div>
                <el-tooltip placement="top" :content="item.fundName">
                  <div class="show-overflow">{{ item.fundName || '-' }}</div>
                </el-tooltip>
              </div>
              <div class="bottom">
                <div class="flex">
                  <span>资金占比：</span>
                  <span class="value">{{ item.costrate | numberToFixedStr(2, 100, '%') }}</span>
                </div>
                <div class="flex mb">
                  <span>加入时间：</span>
                  <span class="value">{{ item.createDate || '-' }}</span>
                </div>
                <div class="flex mt">
                  <span>单位净值：</span>
                  <span class="value">{{ item.price || '-' }}</span>
                </div>
                <div class="flex">
                  <span>资产净值：</span>
                  <span class="value">{{ item.priceJ | moneyYuan }}</span>
                </div>
                <div class="flex">
                  <span>估值时间：</span>
                  <span class="value">{{ item.ddate || '-' }}</span>
                </div>
              </div>
            </div>
            <div class="parent-class" v-else>
              <div class="top">
                <!-- <div>{{ item.fundCode || '-' }}</div> -->
                <div>{{ item.fundName || '-' }}</div>
              </div>
              <div class="bottom">
                <!--                <div class="flex">-->
                <!--                  <span>单位净值：</span>-->
                <!--                  <span class="value">{{ item.price || '-' }}</span>-->
                <!--                </div>-->
                <div class="flex">
                  <span>调仓日期：</span>
                  <span class="value">{{ item.ddate || '-' }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <tree-item v-if="item.children && item.children.length > 0" :tree-data="item.children" />
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'TreeItem',
  props: {
    treeData: {
      type: Array,
      default: () => []
    }
  }
}
</script>

<style lang="scss" scoped>
$line-length: 30px;
$spacing: 30px;

@mixin line {
  content: '';
  display: block;
  width: 2px;
  height: $line-length;
  position: absolute;
  left: 0;
  right: 0;
  margin: auto;
  background: #e9c5a5;
}

.tree-item {
  width: 100%;
  padding: 0 25px;
  ul {
    display: flex;
    justify-content: center;
    li {
      .item {
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
        &-name {
          position: relative;
          display: flex;
          justify-content: center;
          align-items: center;
          width: 220px;
          // padding: 25px 0px;
          margin: $spacing 20px 0 20px;
          font-size: 14px;
          background: #f8fcff;
          border: 1px solid #eaebed;
          border-radius: 10px;
          color: #000;
        }
      }
    }
  }
  .first-item {
    position: relative;
    margin: $spacing;
  }
  .child-class {
    border-radius: 10px;
    .top {
      height: 60px;
      padding: 10px 0;
      width: 220px;
      border-top-right-radius: 10px;
      border-top-left-radius: 10px;
      text-align: center;
      background-color: #fd9414;
      color: #fff;
      font-weight: bold;
    }
    .bottom {
      padding: 10px;
      font-weight: bold;
      border: 1px solid #e23e3d;
      border-top: none;
      .flex {
        display: flex;
        justify-content: space-between;
      }
      .mb {
        padding-bottom: 10px;
        border-bottom: 1px solid #ccc;
      }
      .mt {
        padding-top: 10px;
      }
      .value {
        font-weight: normal;
      }
    }
  }
  .parent-class {
    border-radius: 10px;
    .top {
      height: 40px;
      padding: 10px 0;
      width: 220px;
      border-top-right-radius: 10px;
      border-top-left-radius: 10px;
      text-align: center;
      background-color: #e23e3d !important;
      color: #fff;
      font-weight: bold;
      .code {
        font-size: 16px;
      }
    }
    .bottom {
      padding: 10px;
      font-weight: bold;
      border: 1px solid #e23e3d;
      border-top: none;
      color: #000;
      font-size: 14px;
      .flex {
        display: flex;
        justify-content: space-between;
      }
      .value {
        font-weight: normal;
      }
    }
  }
  .arrows {
    position: absolute;
    bottom: -5px;
    width: 12px;
    top: -5px;
    left: 50%;
    height: 12px;
    line-height: 10px;
    text-align: center;
    color: #666;
    z-index: 100;
    cursor: pointer;
    margin-left: -10px;
    padding: 0;
    &:hover {
      opacity: 100%;
    }
  }
  .svg-color {
    width: 20px;
  }
  .line-bottom {
    &::after {
      @include line();
      bottom: -$line-length;
    }
  }
  .line-top {
    &::before {
      @include line();
      top: -$line-length;
    }
  }
  .line-left {
    &::after {
      @include line();
      width: calc(50% + #{$spacing});
      height: 2px;
      left: calc(-50% - #{$spacing});
      top: 0;
    }
  }
  .line-right {
    &::before {
      @include line();
      width: calc(50% + #{$spacing});
      height: 2px;
      right: calc(-50% - #{$spacing});
      top: 0;
    }
  }
  .show-overflow {
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
}
</style>

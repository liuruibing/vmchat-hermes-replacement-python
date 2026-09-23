<template>
  <div class="tree-item-stock">
    <ul>
      <li v-for="(item, index) in treeData" :key="index">
        <div :class="{ 'line-left': index !== 0, 'line-right': index != treeData.length - 1 }" class="item">
          <div
            :class="{
              'line-bottom': item.child && item.child.length > 0,
              'line-top item-name': item.id !== 0,
              'first-item': item.id === 0
            }"
          >
            <div v-if="item.id !== 0" class="arrows">
              <svg-icon class-name="svg-color" icon-class="down" />
            </div>
            <div :class="{ content: item.id !== 0 }">
              <div class="tree-label">{{ item.name }}</div>
              <div class="value">{{ item.value }}</div>
            </div>
          </div>
        </div>
        <tree-item v-if="item.child && item.child.length > 0" :tree-data="item.child" />
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
  },
  data() {
    return {}
  },
  created() {}
}
</script>

<style lang="scss" scoped>
$line-length: 35px;
$spacing: 35px;

@mixin line {
  content: '';
  display: block;
  width: 2px;
  height: $line-length;
  position: absolute;
  left: 0;
  right: 0;
  margin: auto;
  background: #8a8a8a;
}

.tree-item-stock {
  padding: 0 15px;
  width: 100%;
  ul {
    width: 100%;
    display: flex;
    li {
      width: 100%;
      .item {
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
        &-name {
          flex: 1;
          position: relative;
          display: flex;
          justify-content: center;
          align-items: center;
          padding: 25px 0px;
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
    padding: 10px !important;
    border-radius: 10px !important;
    font-size: 18px;
    background-color: #0F65DD !important;
    color: #fff !important;
    margin: $spacing;
  }
  .content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    .tree-label,
    .value {
      padding: 5px 0;
    }
    .value {
      font-size: 16px;
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
}
</style>

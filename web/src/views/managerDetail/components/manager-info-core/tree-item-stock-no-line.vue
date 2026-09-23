<template>
  <div class="tree-item-stock-no-line">
    <ul>
      <li v-for="(item, index) in treeData" :key="index" class="item">
        <div class="item-name">
          <div class="content">
            <div class="tree-label">{{ item.name }}</div>
            <div class="value">{{ item.value }}</div>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'TreeItemStockNoLine',
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
$spacing: 40px;

.tree-item-stock-no-line {
  padding: 0 26px;
  width: 100%;
  ul {
    width: 100%;
    display: flex;
    flex-wrap: wrap;
    .item {
      width: 50%;
      &-name {
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
}
</style>

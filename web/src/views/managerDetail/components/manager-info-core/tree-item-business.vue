<template>
  <div class="tree-item-business">
    <ul>
      <li v-for="(item, index) in treeData" :key="index">
        <div class="content">
          <div class="tree-label">{{ item.name }}</div>
          <div class="value">{{ item.value }}</div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'TreeItemBusiness',
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
$spacing: 30px;

.tree-item-business {
  padding: 0 50px;
  width: 100%;
  ul {
    width: 100%;
    display: flex;
    li {
      flex: 1;
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
      .content {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        .tree-label,
        .value {
          padding: 5px 0;
          font-size: 14px;
        }
      }
    }
  }
}
</style>

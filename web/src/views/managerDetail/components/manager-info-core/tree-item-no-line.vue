<template>
  <div class="tree-item-no-line">
    <ul>
      <li v-for="(item, index) in treeData" :key="index">
        <div class="content">
          <div class="tree-label">{{ item.name }}</div>
          <div v-if="item.name === '公司网址'" class="value">
            <el-link :href="item.value !== '-' ? item.value : '#'" target="_blank" type="primary">
              {{ item.value }}
            </el-link>
          </div>
          <div v-else-if="item.name === '入会时间'" class="value">
            {{ item.value | timestampToTime }}
          </div>
          <div v-else class="value">{{ item.value }}</div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'TreeItemNoLine',
  filters: {
    timestampToTime(timestamp) {
      if (timestamp == '-' || timestamp == '' || timestamp == undefined || timestamp == null) {
        return '-'
      }
      const date = new Date(timestamp)
      const year = date.getFullYear()
      const month = date.getMonth() + 1
      const day = date.getDate()
      return year + '-' + month + '-' + day
    }
  },
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

.tree-item-no-line {
  width: 100%;
  padding: 0 50px;

  ul {
    display: flex;
    justify-content: center;

    li {
      width: 210px;
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
          word-break: break-all;
        }
      }
    }
  }
}
</style>

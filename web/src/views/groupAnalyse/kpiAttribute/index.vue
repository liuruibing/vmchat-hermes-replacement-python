<template>
  <div class="">
    <el-button @click="productSelectDialogVisible = true">确定</el-button>
    <table-head :table-column="tableColumn" :table-column-selector-visible="productSelectDialogVisible"
                @dialogclose="handleCloseDialog" @submit="handleSubmit"></table-head>

    <!--    <i class="el-icon-notebook-2"></i>-->
    <!--    待开发-业绩归因-->
  </div>
</template>

<script>
import tableHead from '@/components/tableHeadComponent'
import tableBody from '@/components/tableBodyComponent'
export default {
  components: {tableHead, tableBody},
  data() {
    return {
      productSelectDialogVisible: false,
      tableColumn: [
        {
          label: '产品代码',
          disabled: true,
          id: 'fundCode',
          type: 'leftTreeData',
          align: 'center',
          fix: 'left',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: '',
        },
        {
          label: '产品简称',
          disabled: true,
          id: 'fundName',
          type: 'leftTreeData',
          align: 'left',
          fix: 'left',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: '',
        },
        {
          label: '投资策略',
          id: 'type',
          type: 'leftTreeData',
          align: 'left',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: '',
        },
      ]
    }
  },
  methods: {
    handleCloseDialog() {
      this.productSelectDialogVisible = false;
    },
    handleNodeClick() {
    },
    handleSubmit(arr) {
      this.tableColumn = arr
    }
  }
}
</script>

<style lang="scss" scoped>
</style>

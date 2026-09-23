<template>
  <div class="tabletable">
    <div v-if="selectedConditions.length" class="selected-conditions mb10">
      <span class="selected-conditions__label">已选条件：</span>
      <el-tag
        v-for="(condition, index) in selectedConditions"
        :key="condition.id + '-' + (condition.period || '') + '-' + index"
        :disable-transitions="false"
        closable
        @close="$emit('removecondition', condition)"
      >
        {{ formatCondition(condition) }}
      </el-tag>
    </div>
    <table-body
      ref="tableBody"
      :column="column"
      :table-data="tableData"
      :table-loading="tableLoading"
      :show-selection="false"
      :show-focus="false"
      pageType="filter"
      @linkto="jumpToSingle"
      @sorttable="handleSortTable"
    ></table-body>
    <table-head :table-column="column" :table-column-selector-visible="productSelectDialogVisible" @dialogclose="handleCloseDialog" @submit="handleSubmit"></table-head>
  </div>
</template>

<script>
import tableBody from '@/components/tableBodyComponent'
import tableHead from '@/components/tableHeadComponent'

export default {
  components: { tableBody, tableHead },
  props: {
    tableData: {
      type: Array,
      required: true,
      default: () => {
        return []
      }
    },
    tableLoading: {
      type: Boolean,
      required: true,
      default: false
    },
    selectedConditions: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      productSelectDialogVisible: false,
      column: [
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
          sortable: true
        },
        {
          label: '产品名称',
          id: 'fundName',
          disabled: true,
          type: 'leftTreeData',
          align: 'left',
          fix: 'left',
          width: '250px',
          noshowoverflowtooltip: true,
          filter: 'fund',
          sortable: true
        },
        {
          label: '数据来源',
          id: 'source',
          type: 'leftTreeData',
          align: 'left',
          fix: 'left',
          width: '120px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },
        {
          label: '投资策略',
          id: 'fofMainStrategyName',
          type: 'leftTreeData',
          align: 'left',
          fix: '',
          width: '110px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },
        {
          label: '产品管理人',
          id: 'companyName',
          type: 'centerTreeDataLeft',
          align: 'left',
          fix: '',
          width: '150px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },

        // {
        //   label: '基金经理',
        //   id: 'managerName',
        //   type: 'leftTreeData',
        //   align: 'left',
        //   fix: '',
        //   width: '100px',
        //   noshowoverflowtooltip: true,
        //   filter: '',
        //   sortable: true
        // },
        {
          label: '成立日期',
          id: 'foundDate',
          type: 'leftTreeData',
          align: 'left',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },
        {
          label: '净值日期',
          id: 'navDate',
          type: 'centerTreeDataCenter',
          align: 'left',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },
        {
          label: '单位净值',
          id: 'unitNav',
          type: 'centerTreeDataCenter',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'moneyYuan4Yuan',
          sortable: true
        },
        {
          label: '累计净值',
          id: 'addedNav',
          type: 'centerTreeDataCenter',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'moneyYuan4Yuan',
          sortable: true
        },
        {
          label: '近一月收益率',
          id: 'm1_return',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近一月最大回撤',
          id: 'm1_max_retracement',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近一月Sharpe比率',
          id: 'm1_sharpe',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '140px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近三月收益率',
          id: 'm3_return',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近三月最大回撤',
          id: 'm3_max_retracement',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近三月Sharpe比率',
          id: 'm3_sharpe',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '140px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近六月收益率',
          id: 'm6_return',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近六月最大回撤',
          id: 'm6_max_retracement',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近六月Sharpe比率',
          id: 'm6_sharpe',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '140px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近一年收益率',
          id: 'y1_return',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近一年最大回撤',
          id: 'y1_max_retracement',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近一年Sharpe比率',
          id: 'y1_sharpe',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '140px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '今年以来收益率',
          id: 'ytd_return',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '今年以来最大回撤',
          id: 'ytd_max_retracement',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '今年以来Sharpe比率',
          id: 'ytd_sharpe',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '140px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        }
        // ,{
        //   label: '管理规模区间',
        //   id: 'managerAsset',
        //   type: 'centerTreeDataLeft',
        //   align: 'right',
        //   fix: '',
        //   width: '130px',
        //   noshowoverflowtooltip: true,
        //   filter: '',
        //   sortable: true
        // }
      ]
    }
  },
  mounted() {
    // const xTable = this.$refs.vxetable
    // xTable.connect(this.$refs.xToolbar)
  },
  methods: {
    formatCondition(condition) {
      if (condition.value) {
        return condition.title + '：' + condition.value.replace(/，$/, '')
      }
      if (condition.start !== undefined || condition.end !== undefined) {
        return condition.title + '：' + (condition.start || '') + '-' + (condition.end || '')
      }
      return condition.title
    },
    getSelectedColumnIds() {
      return this.column.map(col => col.id);
    },
    formatFundName(row) {
     if(row.gfSelling=='代销') {
       return "<span>"+ row.fundName+"</span><span style=\"padding-left: 10px;\"><span className=\"greenGfSelling\">代销</span></span>"
     }else{
       return "<span>"+ row.fundName+"</span>"
     }

    },
    handleSortTable(val) {
      this.$emit('sorttable', val)
    },

    handleCloseDialog() {
      this.productSelectDialogVisible = false
      this.$refs.tableBody.$refs.vxetable.refreshColumn()
      this.$forceUpdate()
    },
    handleNodeClick() {},
    handleSubmit(arr) {
      this.column = arr
    },
    /**
     * @description 跳转单产品页面
     */
    jumpToSingle(row) {
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/productor-filter-single-demo/report',
        query: { fundCode: row.fundCode }
      })
    },
    /**
     * @description 跳转管理人详情
     */
    jumpToManager(row) {
      this.$store.commit('SET_FROMPAGEJUMP', true)
      const manager_name = row.companyName
      this.$router.push({
        path: '/tqgl/glrxq',
        query: { managerList: { company_id: row.company_id, manager_name } }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.tabletable {
  margin: 0 10px 0px 0px;
}
.selected-conditions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}

.selected-conditions__label {
  flex: 0 0 auto;
}
.icon-style {
  margin-bottom: 0px !important;
  font-size: 14px;
}

.color_4f95dd {
  color: #4f95dd;
  cursor: pointer;
}

.color_e6a23c {
  color: #e6a23c;
}

.fund_cell {
  display: flex;
  align-items: center;

  .fund_name {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    margin-right: 5px;
  }
}

.tabletable {
  //margin-top: 10px;
  padding-left: 10px;

  .tabletable_top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
  }
}

.color-box {
  display: inline-block;
  height: 30px;
  width: 2px;
  background-color: #0f65dd;
}

.title-style {
  color: #0f65dd;
  vertical-align: middle;
  height: 35px;
  line-height: 35px;
  font-size: 16px;
  margin-left: 5px;
  display: inline-block;
}

::v-deep .vxe-table--render-default .vxe-cell {
  white-space: normal;
}
::v-deep .el-tag {
  border: none;
  background-image: linear-gradient(to right, #f5d7bc, #e0b794) !important;
  span {
    color: #612d10 !important;
  }
  .el-tag__close {
    color: #612d10 !important;
  }
  .el-tag__close:hover {
    background-color: transparent;
  }
}
::v-deep .vxe-table--render-default .vxe-cell--checkbox:not(.is--disabled):hover .vxe-checkbox--icon:before {
  border-color: #e9c5a5!important
}

</style>

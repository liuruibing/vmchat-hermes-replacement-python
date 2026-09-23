<template>
  <div id="standard-table">
    <vxe-table
      auto-resize
      sync-resize
      ref="vxetable"
      v-loading="tableLoading"
      :checkbox-config="{ checkStrictly: true, checkMethod: handleCheckBoxDisabled }"
      :data="tableData"
      :height="tableHeight"
      :sort-config="{ remote: true }"
      :cell-style="{ height: '50px' }"
      show-overflow="tooltip"
      stripe=""
      style="width: 100%"
      @sort-change="handleSortChange"
      @checkbox-change="handleCheckBoxClick"
      resizable
    >
      <!-- defaultSort: { field: 'navDate', order: 'desc' } -->
      <vxe-table-column align="center" fixed="left" type="checkbox" width="55"></vxe-table-column>
      <vxe-table-column align="center" fixed="left" title="关注" width="80">
        <template slot-scope="scope">
          <el-link :underline="false" style="font-size: 14px" type="primary" @click="handleFocus(scope.row)">
            {{ scope.row.isConcern | filterConcern }}
          </el-link>
        </template>
      </vxe-table-column>
      <vxe-table-column align="center" fixed="left" title="序号" type="seq" width="50"></vxe-table-column>
      <vxe-table-column
        v-for="item in column"
        v-if="isShowColumn"
        :key="item.id"
        :align="item.align"
        :field="item.id"
        :fixed="item.fix"
        :min-width="item.width"
        :show-overflow-tooltip="item.noshowoverflowtooltip"
        :sortable="item.sortable"
        :title="item.label"
        header-align="center"
      >
        <template slot-scope="{ column }" slot="header">
          <span v-if="splitTitleFor3.includes(column.title)">
            <div>{{ column.title.slice(0, 3) }}</div>
            <span>{{ column.title.slice(3, column.title.length) }}</span>
          </span>
          <span v-else-if="splitTitleFor4.includes(column.title)">
            <div>{{ column.title.slice(0, 4) }}</div>
            <span>{{ column.title.slice(4, column.title.length) }}</span>
          </span>
          <span v-else-if="splitTitleLine3.includes(column.title)">
            <div>{{ column.title.slice(0, 4) }}</div>
            <span>{{ column.title.slice(4, 10) }}</span>
            <span>{{ column.title.slice(10, column.title.length) }}</span>
          </span>
          <span v-else>{{ column.title }}</span>
        </template>
        <template slot-scope="scope">
          <span v-if="((scope.row.isPermission && scope.row.isPermission == '0') || (scope.row.isStatus && scope.row.isStatus == '1')) && isHideFilter(item)">
            <span>--</span>
          </span>
          <span v-else>
            <span v-if="isColorStr(item.label) && item.filter == 'numberToFixedStr'">
              <span v-if="Number(scope.row[item.id]) > 0 && item.label.indexOf('最大回撤') < 0" style="color: #c20000">
                <span v-if="numToFixedNoStrArray.includes(item.id)">
                  {{ scope.row[item.id] | numberToFixedStr(2, 1) }}
                </span>
                <span v-else>{{ scope.row[item.id] | numberToFixedStr(2, 100, '%') }}</span>
              </span>
              <span v-else-if="Number(scope.row[item.id]) < 0 || item.label.indexOf('最大回撤') >= 0" style="color: #148a0c">
                <span v-if="numToFixedNoStrArray.includes(item.id)">
                  {{ scope.row[item.id] | numberToFixedStr(2, 1) }}
                </span>
                <span v-else>{{ scope.row[item.id] | numberToFixedStr(2, 100, '%') }}</span>
              </span>
              <span v-else>
                <span v-if="numToFixedNoStrArray.includes(item.id)">
                  {{ scope.row[item.id] | numberToFixedStr(2, 1) }}
                </span>
                <span v-else>{{ scope.row[item.id] | numberToFixedStr(2, 100, '%') }}</span>
              </span>
            </span>
            <span v-else-if="item.filter == 'manager'" class="color_4f95dd fund_cell" @click="jumpPage(scope.row)">
              <span class="fund_name">
                <el-tooltip effect="dark" :content="scope.row[item.id] || '-'" placement="top">
                  <span>{{ scope.row[item.id] | noDataFilter }}</span>
                </el-tooltip>
              </span>
              <img v-if="scope.row.source === 'IN' && item.id != 'companyName'" :src="require('@/assets/img/CMS1.png')" height="14px" width="20px" />
              <!--            <img v-if="scope.row.isVerify == 1 && item.id != 'companyName'" src="@/assets/img/已验证.png" />-->
              <!--            <img v-if="scope.row.isVerify == 0 && item.id != 'companyName'" src="@/assets/img/验证中.png" />-->
            </span>
            <span v-else-if="item.filter == 'moneyYuan'">
              {{ scope.row[item.id] | moneyYuan }}
            </span>
            <span v-else-if="item.filter == 'moneyYuan4'">
              {{ scope.row[item.id] | moneyYuan4 }}
            </span>
            <span v-else-if="item.filter == 'numberToFixedStr2'">
              {{ scope.row[item.id] | numberToFixedStr(2, 100, '%') }}
            </span>
            <span v-else-if="item.filter == 'numberToFixedStr4'">
              {{ scope.row[item.id] | numberToFixedStr(4, 100, '%') }}
            </span>
            <span v-else-if="item.filter == 'moneyYuanStrW'">{{ scope.row[item.id] | numberToFixedStr(2, 1) }}万元</span>
            <span v-else-if="item.filter == 'moneyYuanStrY'">{{ scope.row[item.id] | numberToFixedStr(4, 1) }}亿元</span>
            <span v-else-if="item.filter == 'moneyYuan4Yuan'">{{ scope.row[item.id] | moneyYuan4 }}元</span>
            <span v-else-if="item.filter == 'moneyYuan2Yuan'">{{ scope.row[item.id] | moneyYuan }}万元</span>
            <span v-else-if="item.id === 'companyName'">
              <el-link :underline="false" type="primary">
                {{ scope.row[item.id] | noDataFilter }}
              </el-link>
            </span>
            <span v-else-if="item.filter == 'star'">
              <el-rate v-model="scope.row[item.id]" :colors="['#e03d3e', '#e03d3e', '#e03d3e']" disabled></el-rate>
            </span>
            <span v-else-if="item.filter == 'echarts'">
              <myecharts
                :id="scope.row.company_id"
                :ref="scope.row.company_id"
                :options="scope.row.option"
                resize-dom="cmbfof"
                style="width: 100%; height: 30px; top: 5px"
              ></myecharts>
            </span>
            <span v-else>{{ scope.row[item.id] | noDataFilter }}</span>
          </span>
        </template>
      </vxe-table-column>
    </vxe-table>
  </div>
</template>
<script>
import myecharts from '@/components/Echarts'
export default {
  components: { myecharts },
  filters: {
    filterConcern(val) {
      if (val == 0) {
        return '关注'
      } else {
        return '已关注'
      }
    }
  },
  props: {
    // filter | focus
    pageType: {
      type: String,
      default: 'filter'
    },
    checkArray: {
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
    tableData: {
      type: Array,
      required: true,
      default: () => {
        return []
      }
    },
    column: {
      type: Array,
      required: true,
      default: () => {
        return []
      }
    }
  },
  data() {
    return {
      tableHeight: '0',
      isShowColumn: true,
      splitTitleFor3: [
        '近一月收益率',
        '近一月波动率',
        '近一月最大回撤',
        '近一月Sharpe比率',
        '近一月Sortino比率',
        '近一月Treynor比率',
        '近一月Calmar比率',
        '近一月Alpha',
        '近一月Beta',
        '近一月信息比率',
        '近一月投资胜率',
        '近三月收益率',
        '近三月波动率',
        '近三月最大回撤',
        '近三月Sharpe比率',
        '近三月Sortino比率',
        '近三月Treynor比率',
        '近六月收益率',
        '近六月波动率',
        '近六月最大回撤',
        '近六月Calmar比率',
        '近六月Alpha',
        '近六月Beta',
        '近六月信息比率',
        '近六月投资胜率',
        '近六月Sharpe比率',
        '近六月Sortino比率',
        '近六月Treynor比率',
        '近一年收益率',
        '近一年波动率',
        '近一年最大回撤',
        '近一年Sharpe比率',
        '近一年Sortino比率',
        '近一年Treynor比率',
        '近一年Calmar比率',
        '近一年投资胜率',
        '近一年信息比率',
        '近一年Beta',
        '近一年Alpha比率',
        '近一年Alpha'
      ],
      splitTitleFor4: [
        '今年以来收益率',
        '今年以来波动率',
        '今年以来最大回撤',
        '今年以来Sharpe比率',
        '今年以来Sortino比率',
        '今年以来Calmar比率',
        '今年以来Alpha',
        '今年以来Beta',
        '今年以来信息比率',
        '今年以来投资胜率',
        '今年以来Treynor比率',
        '成立以来收益率',
        '成立以来波动率',
        '成立以来最大回撤',
        '成立以来Sharpe比率',
        '成立以来Sortino比率',
        '成立以来Calmar比率',
        '成立以来Alpha',
        '成立以来Beta',
        '成立以来信息比率',
        '成立以来投资胜率',
        '成立以来Treynor比率'
      ],
      splitTitleLine3: ['成立以来股票占净值比(平均值)', '成立以来债券占净值比(平均值)', '成立以来基金占净值比(平均值)', '成立以来期货占净值比(平均值)'],
      numToFixedNoStrArray: [
        // 信息比率
        'm6_info',
        'y1_info',
        'ytd_info',
        'total_info',
        //calmar
        'm6_calmar',
        'y1_calmar',
        'ytd_calmar',
        'total_calmar',
        // beta
        'm6_beta',
        'y1_beta',
        'ytd_beta',
        'total_beta',
        // sharpe
        'm6_sharpe',
        'y1_sharpe',
        'ytd_sharpe',
        'total_sharpe',
        //sortino
        'm6_sortino',
        'y1_sortino',
        'ytd_sortino',
        'total_sortino',
        // Treynor
        'm6_terynor',
        'y1_terynor',
        'ytd_terynor',
        'total_terynor'
      ]
    }
  },
  methods: {
    handleCheckBoxDisabled({ row }) {
      if ((row.isPermission && row.isPermission == '0') || (row.isStatus && row.isStatus == '1')) {
        return false
      }
      return true
    },
    // 判定是否是属于隐藏的菜单
    isHideFilter(item) {
      if (item.filter.includes('money') || item.filter.includes('number') || item.filter == 'echarts') {
        return true
      } else {
        return false
      }
    },
    handleTableHeight() {
      setTimeout(() => {
        const appMain = document.getElementById('appMain').offsetHeight
        const ddQuery = document.getElementById('dd-query').offsetHeight
        let diff = appMain - ddQuery - 45 - 38 - 32 - 10 - 10
        if (diff < 300) {
          this.tableHeight = 300
        } else {
          this.tableHeight = diff
        }
      }, 150)
    },
    handleTableHeightMyFocus() {
      setTimeout(() => {
        const appMain = document.getElementById('appMain').offsetHeight
        const ddQuery = document.getElementById('dd-query-manager').offsetHeight
        let diff = appMain - ddQuery - 29 - 5 - 10 - 35 - 42 - 18
        if (diff < 300) {
          this.tableHeight = 300
        } else {
          this.tableHeight = diff
        }
      }, 150)
    },
    setCheckBoxFalse(row) {
      // 设置传过来的checkbox取消勾选
      let index = this.tableData.findIndex((sitem) => sitem.company_id == row.company_id)
      if (index != -1) {
        this.$refs.vxetable.setCheckboxRow(this.tableData[index], false)
      }
    },
    // 处理 checkbox点击事件
    handleCheckBoxClick({ checked, row }) {
      this.$emit('checkbox', { checked: checked, row: row })
    },

    // 处理排序
    handleSortChange(e) {
      this.$emit('sorttable', e)
    },
    handleFocus(row) {
      this.$emit('focusstatus', row)
    },
    getTableDataCheckRows() {
      return this.$refs.vxetable.getCheckboxRecords(true) || []
    },
    isColorStr(str) {
      const titleStr = [
        '近一月收益率',
        '近一月波动率',
        '近一月最大回撤',
        '近一月最大回撤',
        '近一月Sharpe比率',
        '近一月Sortino比率',
        '近一月Treynor比率',
        '近三月收益率',
        '近三月波动率',
        '近三月最大回撤',
        '近三月最大回撤',
        '近三月Sharpe比率',
        '近三月Sortino比率',
        '近三月Treynor比率',
        '近六月收益率',
        '近六月波动率',
        '近六月最大回撤',
        '近六月Calmar比率',
        '近六月Alpha',
        '近六月Beta',
        '近六月信息比率',
        '近六月投资胜率',
        '近六月Sharpe比率',
        '近六月Sortino比率',
        '近六月Treynor比率',
        '近一年收益率',
        '近一年波动率',
        '近一年最大回撤',
        '近一年Sharpe比率',
        '近一年Sortino比率',
        '近一年Calmar比率',
        '近一年Alpha',
        '近一年Beta',
        '近一年信息比率',
        '近一年投资胜率',
        '近一年Treynor比率',
        '近一年Jenson指数',
        '今年以来收益率',
        '今年以来最大回撤',
        '今年以来Sharpe比率',
        '今年以来Sortino比率',
        '今年以来Calmar比率',
        '今年以来波动率',
        '今年以来Alpha',
        '今年以来Beta',
        '今年以来信息比率',
        '今年以来投资胜率',
        '今年以来Treynor比率',
        '今年以来Jenson指数',
        '成立以来收益率',
        '成立以来波动率',
        '成立以来最大回撤',
        '成立以来Sharpe比率',
        '成立以来Sortino比率',
        '成立以来Calmar比率',
        '成立以来Alpha',
        '成立以来Beta',
        '成立以来信息比率',
        '成立以来投资胜率',
        '成立以来Treynor比率',
        '成立以来Jenson指数'
      ]
      if (titleStr.indexOf(str) == -1) {
        return false
      } else {
        return true
      }
    },
    pagination() {},
    jumpPage(row) {
      if ((row.isPermission && row.isPermission == '0') || (row.isStatus && row.isStatus == '1')) {
        this.$message.closeAll()
        this.$message({
          type: 'warning',
          message: '此产品业绩信息暂时不可查看',
          customClass: 'message-warning'
        })
        return
      }
      this.$emit('linkto', row)
    },
    onContrast() {
      const list = this.$refs.vxetable.getCheckboxRecords()
      if (list.length >= 2) {
        this.$router.push({
          name: 'smcpxx'
        })
      } else {
        this.$message.closeAll()
        this.$message({
          type: 'warning',
          message: '请至少选择两个产品',
          customClass: 'message-warning'
        })
      }
    }
  },
  watch: {
    column() {
      this.isShowColumn = false
      setTimeout(() => {
        this.isShowColumn = true
      })
    },
    tableData: {
      handler() {
        this.checkArray.forEach((item) => {
          let index = this.tableData.findIndex((sitem) => sitem.company_id == item.company_id)
          if (index != -1) {
            this.$refs.vxetable.setCheckboxRow(this.tableData[index], true)
          }
        })
      },
      deep: true,
      immediate: true
    }
  },
  activated() {
    if (this.pageType === 'focus') {
      this.handleTableHeightMyFocus()
    } else {
      this.handleTableHeight()
    }
  }
}
</script>
<style lang="scss" scoped>
.icon-style {
  margin-bottom: 0px !important;
  font-size: 14px;
}

.color_4f95dd {
  color: #0f65dd;
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

::v-deep .vxe-table--render-default .vxe-cell {
  white-space: normal;
}

::v-deep .el-rate__item .el-rate__icon {
  margin-right: 0;
}
::v-deep .vxe-table .vxe-cell--sort {
  height: 1.4em;
}

::v-deep .vxe-table .vxe-body--row.row--stripe {
  background-color: #f9fafe !important;
}
::v-deep .vxe-table--render-default .vxe-body--column:not(.col--ellipsis) {
  padding: 0;
}

::v-deep .vxe-table--render-default .vxe-header--column:not(.col--ellipsis) {
  padding: 0;
}
::v-deep .vxe-header--row .vxe-cell {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>

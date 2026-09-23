<template>
  <div id="standard-table">
    <vxe-table
      v-loading="tableLoading"
      ref="vxetable"
      :cell-style="{ height: '50px' }"
      :checkbox-config="{ checkStrictly: true, checkMethod: handleCheckBoxDisabled }"
      :data="tableData"
      :height="tableHeight"
      :sort-config="{ remote: true, defaultSort: { field: 'm3_return', order: 'desc' } }"
      auto-resize
      stripe=""
      show-overflow="tooltip"
      style="width: 100%"
      sync-resize
      @checkbox-change="handleCheckBoxClick"
      @sort-change="handleSortChange"
      resizable
    >
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
        <template slot="header" slot-scope="{ column }">
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
            <span v-else-if="item.filter == 'fund'" class="color_4f95dd fund_cell" @click="jumpPage(scope.row)">
              <span class="fund_name">
                <el-tooltip :content="scope.row[item.id] || '-'" effect="dark" placement="top">
                  <span>{{ scope.row[item.id] | noDataFilter }}</span>
                </el-tooltip>
              </span>
              <img v-if="scope.row.source === 'IN' && item.id != 'companyName'" :src="require('@/assets/img/CMS.png')" height="14px" width="20px" />
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
              <span v-if="Number(scope.row[item.id]) > 0" style="color: #c20000">
                <span v-if="numToFixedNoStrArray.includes(item.id)">
                  {{ scope.row[item.id] | numberToFixedStr(4, 1) }}
                </span>
                <span v-else>{{ scope.row[item.id] | numberToFixedStr(4, 100, '%') }}</span>
              </span>
              <span v-else-if="Number(scope.row[item.id]) < 0" style="color: #148a0c">
                <span v-if="numToFixedNoStrArray.includes(item.id)">
                  {{ scope.row[item.id] | numberToFixedStr(4, 1) }}
                </span>
                <span v-else>{{ scope.row[item.id] | numberToFixedStr(4, 100, '%') }}</span>
              </span>
              <span v-else>
                <span v-if="numToFixedNoStrArray.includes(item.id)">
                  {{ scope.row[item.id] | numberToFixedStr(4, 1) }}
                </span>
                <span v-else>{{ scope.row[item.id] | numberToFixedStr(4, 100, '%') }}</span>
              </span>
            </span>
            <span v-else-if="item.filter == 'moneyYuanStrW'">{{ scope.row[item.id] | numberToFixedStr(2, 1) }}万元</span>
            <span v-else-if="item.filter == 'moneyYuanStrY'">{{ scope.row[item.id] | numberToFixedStr(4, 1) }}亿元</span>
            <span v-else-if="item.filter == 'moneyYuan4Yuan'">{{ scope.row[item.id] | moneyYuan4 }}</span>
            <span v-else-if="item.filter == 'moneyYuan2Yuan'">{{ scope.row[item.id] | moneyYuan }}万元</span>
            <span v-else-if="item.id === 'companyName'" class="color_4f95dd fund_cell" @click="jumpManagerPage(scope.row)">
              <span class="fund_name">
                <el-tooltip :content="scope.row[item.id] || '-'" effect="dark" placement="top">
                  <span>{{ scope.row[item.id] | noDataFilter }}</span>
                </el-tooltip>
              </span>
            </span>
            <span v-else-if="item.id === 'fundFullName'" class="fund_cell">
              <span :title="scope.row[item.id]" class="fund_name">
                {{ scope.row[item.id] | noDataFilter }}
              </span>
            </span>
            <span v-else-if="item.id === 'companyFullName'" class="fund_cell">
              <span :title="scope.row[item.id]" class="fund_name">
                {{ scope.row[item.id] | noDataFilter }}
              </span>
            </span>
            <span v-else-if="item.filter == 'star'">
              <el-rate v-model="scope.row[item.id]" :colors="['#e03d3e', '#e03d3e', '#e03d3e']" disabled></el-rate>
            </span>
            <span v-else-if="item.filter == 'echarts'">
              <myecharts
                :id="(scope.row.fundCode || scope.row.FUNDCODE) + scope.row.type"
                :ref="(scope.row.fundCode || scope.row.FUNDCODE) + scope.row.type"
                :options="scope.row.option"
                resize-dom="cmbfof"
                style="width: 100%; height: 30px; top: 5px"
              ></myecharts>
            </span>
            <span v-else-if="item.id === 'status'">
              {{ scope.row[item.id] | noDataFilter }}
            </span>
            <span v-else-if="item.id === 'isTier'">
              {{ scope.row[item.id] | noDataFilter }}
            </span>
            <span v-else-if="item.id === 'navfrequency'">
              {{ scope.row[item.id] | noDataFilter }}
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
    },
    filterStatus(val) {
      return val
      // if (val == 0) {
      //   return '已终止'
      // } else if (val == 1) {
      //   return '运行中'
      // } else {
      //   return '-'
      // }
    },
    filterTier(val) {
      return val
      // if (val == 0) {
      //   return '不分级'
      // } else if (val == 1) {
      //   return '分级'
      // } else {
      //   return '-'
      // }
    },
    filterNavfrequency(val) {
      if (val == 0) {
        return '日频'
      } else if (val == 1) {
        return '周频'
      } else if (val == 2) {
        return '日频'
      } else {
        return '-'
      }
    }
  },
  props: {
    checkArray: {
      type: Array,
      required: true,
      default: () => {
        return []
      }
    },
    pageType: {
      type: String,
      default: 'filter'
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
      isShowColumn: true,
      splitTitleFor3: [
        '近一月收益率',
        '近一月波动率',
        '近一月最大回撤',
        '近一月Sharpe比率',
        '近一月Sortino比率',
        '近一月Treynor比率',
        '近三月收益率',
        '近三月波动率',
        '近三月最大回撤',
        '近三月Sharpe比率',
        '近三月Sortino比率',
        '近三月Treynor比率',
        '近六月收益率',
        '近六月波动率',
        '近六月最大回撤',
        '近六月Sharpe比率',
        '近六月Sortino比率',
        '近六月Treynor比率',
        '近一年收益率',
        '近一年波动率',
        '近一年最大回撤',
        '近一年Sharpe比率',
        '近一年Calmar比率',
        '近一年Alpha',
        '近一年Beta',
        '近一年信息比率',
        '近一年投资胜率',
        '近一年Sortino比率',
        '近一年Treynor比率'
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
        'm1_sharpe',
        'm1_sortino',
        'm1_terynor',
        'm3_sharpe',
        'm3_sortino',
        'm3_terynor',
        'm6_sharpe',
        'm6_sortino',
        'm6_terynor',
        'y1_sharpe',
        'y1_sortino',
        'y1_calmar',
        'y1_beta',
        'y1_info',
        'y1_terynor',
        'ytd_sharpe',
        'ytd_sortino',
        'ytd_calmar',
        'ytd_beta',
        'ytd_info',
        'ytd_terynor',
        'total_sharpe',
        'total_sortino',
        'total_calmar',
        'total_beta',
        'total_info',
        'total_terynor'
      ],
      tableHeight: 0
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
          const index = this.tableData.findIndex((sitem) => sitem.fundCode == item.fundCode)
          if (index != -1) {
            this.$refs.vxetable.setCheckboxRow(this.tableData[index], true)
          }
        })
      },
      deep: true,
      immediate: true
    }
    // checkArray: {
    //   handler() {
    //     this.checkArray.forEach(item => {
    //       let index = this.tableData.findIndex(sitem => sitem.fundCode == item.fundCode)
    //       if (index != -1) {
    //         this.$refs.vxetable.setCheckboxRow(this.tableData[index], true)
    //       }
    //     })
    //   },
    //   deep: true,
    // }
  },
  activated() {
    if (this.pageType === 'smrd') {
      this.handleTableSMRD()
    } else {
      this.handleTableHeight()
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
    handleTableSMRD() {
      setTimeout(() => {
        const appMain = document.getElementById('appMain').offsetHeight
        const diff = appMain - 45 - 38 - 32 - 10 - 20 - 10 - 30
        if (diff < 300) {
          this.tableHeight = 300
        } else {
          this.tableHeight = diff
        }
      }, 150)
    },
    handleTableHeight() {
      setTimeout(() => {
        const appMain = document.getElementById('appMain').offsetHeight
        const diff = appMain - 45 - 38 - 32 - 10 - 20 - 10
        if (diff < 300) {
          this.tableHeight = 300
        } else {
          this.tableHeight = diff
        }
      }, 150)
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
    setCheckBoxFalse(row) {
      // 设置传过来的checkbox取消勾选
      const index = this.tableData.findIndex((sitem) => sitem.fundCode == row.fundCode)
      if (index != -1) {
        this.$refs.vxetable.setCheckboxRow(this.tableData[index], false)
      }
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
        '近六月最大回撤',
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
        '成立以来Jenson指数',
        '成立以来股票占净值比(平均值)',
        '成立以来债券占净值比(平均值)',
        '成立以来基金占净值比(平均值)',
        '成立以来期货占净值比(平均值)'
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
    jumpManagerPage(row) {
      this.$emit('linktomanger', row)
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
  }
  // checkArray() {
  //   // 判断当前的 tableData需不需要进行
  // }
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

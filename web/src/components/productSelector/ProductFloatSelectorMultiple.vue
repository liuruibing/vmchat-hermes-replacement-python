<template>
  <div class="product-float-selector" v-show="visible" ref="floatContainer" @mouseleave="handleComponentMouseLeave">
    <!-- 搜索栏 -->
    <div class="float-search-bar">
      <el-input
        v-model="formQuery.productName"
        placeholder="产品代码/名称/管理人"
        size="small"
        style="width: 200px !important;"
        @input="handleRealtimeSearch"
        clearable
      ></el-input>
      <el-select
        ref="strategySelect"
        v-model="formQuery.strategy"
        placeholder="请选择策略类型"
        size="small"
        clearable
        @change="handleStrategyChange"
        :popper-append-to-body="false"
        popper-class="strategy-select-dropdown"
      >
        <el-option
          v-for="item in strategyType"
          :key="item.DIM_CDE"
          :label="item.DIM_NME"
          :value="item.DIM_CDE"
        ></el-option>
      </el-select>
      <el-select
        ref="subStrategySelect"
        v-model="formQuery.subStrategy"
        placeholder="请选择子策略类型"
        size="small"
        clearable
        @change="handleRealtimeSearch"
        @click.stop
        :popper-append-to-body="false"
        :disabled="!formQuery.strategy"
        popper-class="sub-strategy-select-dropdown"
      >
        <el-option
          v-for="item in subStrategyType"
          :key="item.DIM_CDE"
          :label="item.DIM_NME"
          :value="item.DIM_CDE"
        ></el-option>
      </el-select>
    </div>

    <!-- 产品列表表格 -->
    <div class="float-table-wrapper" v-loading="searchLoading">
      <el-table
        :data="tableData"
        :header-cell-style="{textAlign: 'center', background: '#fafafa', fontSize: '12px' }"
        :cell-style="{ fontSize: '12px' }"
        style="width: 100%;"
        max-height="350px"
        v-el-table-infinite-scroll="loadMore"
        @selection-change="handleSelectionChange"
        :row-key="getTableRowKey"
        ref="productTable"
      >
        <!-- 多选列 -->
        <el-table-column
          type="selection"
          align="center"
          width="50"
        ></el-table-column>
        <el-table-column
          label="产品代码"
          prop="VC_FUNDCODE"
          align="left"
          min-width="120"
        ></el-table-column>
        <el-table-column
          label="产品名称"
          prop="VC_FUNDNAME"
          align="left"
          min-width="220"
          show-overflow-tooltip
        ></el-table-column>
        <el-table-column
          label="策略类型"
          prop="VC_INVESTSTRATEGY"
          align="left"
          min-width="120"
        ></el-table-column>
        <el-table-column
          label="子策略类型"
          prop="VC_STRATEGY"
          align="left"
          min-width="120"
        ></el-table-column>
        <el-table-column
          label="管理人名称"
          prop="VC_NAME_GLR"
          align="left"
          min-width="180"
          show-overflow-tooltip
        ></el-table-column>
      </el-table>
      <div style="height: 30px">
        <div v-if="loading" class="load-tip">加载中...</div>
        <div v-if="noMore && tableData.length > 0" class="load-tip">暂无更多数据</div>
      </div>
    </div>

    <!-- 多选操作按钮 -->
    <div class="float-footer" style="padding: 10px; text-align: right; border-top: 1px solid #e4e7ed;">
      <el-button size="small" type="info" @click="handleClearSelection">清空选择</el-button>
<!--      <el-button size="small" type="text" @click="handleSelectAll">全选</el-button>-->
<!--      <el-button size="small" type="info" @click="hideSelector">取消</el-button>-->
      <el-button size="small" type="primary" @click="handleConfirmSelect">确认</el-button>
    </div>
  </div>
</template>

<script>
import commonApi from '@/api/common'
import _ from 'lodash'

const elTableInfiniteScroll = {
  inserted(el, binding, vnode) {
    const getTableBody = function() {
      const tableBody = el.querySelector('.el-table__body-wrapper')
      if (tableBody) return tableBody
      // 多次重试
      let retryCount = 0
      const timer = setInterval(function() {
        const retryTableBody = el.querySelector('.el-table__body-wrapper')
        if (retryTableBody || retryCount >= 5) {
          clearInterval(timer)
          return retryTableBody
        }
        retryCount++
      }, 200)
      return null
    }
    const tableBody = getTableBody()
    if (!tableBody) {
      console.error('未找到表格滚动容器')
      return
    }

    Object.assign(tableBody.style, {
      height: '320px !important',
      maxHeight: '320px !important',
      overflowY: 'auto !important',
      overflowX: 'hidden !important'
    })
    const handleScroll = function() {
      const ctx = vnode.context
      const loading = ctx.loading
      const noMore = ctx.noMore
      const total = ctx.total
      const tableData = ctx.tableData
      const loadMore = binding.value
      const distance = 10 // 触底距离
      // 拦截条件
      if (loading || noMore || (total && tableData.length >= total)) return
      // 触底判断
      const isBottom = this.scrollTop + this.clientHeight >= this.scrollHeight - distance
      if (isBottom && typeof loadMore === 'function') {
        loadMore()
      }
    }

    // 初始检测
    setTimeout(function() { handleScroll.bind(tableBody)() }, 800)
    tableBody.addEventListener('scroll', handleScroll.bind(tableBody))
    el._scrollListener = handleScroll
  },
  unbind(el) {
    const tableBody = el.querySelector('.el-table__body-wrapper')
    if (tableBody && el._scrollListener) {
      tableBody.removeEventListener('scroll', el._scrollListener)
    }
  }
}

export default {
  name: 'ProductFloatSelectorMultiple',
  directives: {
    'el-table-infinite-scroll': elTableInfiniteScroll
  },
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    defaultCheckedKeys: {
      type: String,
      default: 'zstgwb' // 默认产品列表
    },
    // 路由路径
    routePath: {
      type: String,
      required: true
    },
    // 已选中的产品列表
    selectedProducts: {
      type: Array,
      default: function() {
        return []
      }
    }
  },
  data() {
    return {
      // 搜索表单
      formQuery: {
        productName: '',
        strategy: '',
        subStrategy: ''
      },
      // 产品列表数据
      tableData: [],
      // 策略类型下拉数据
      strategyType: [],
      subStrategyType: [],
      allSubStrategyList: [],
      // 加载状态
      searchLoading: false,
      // 产品列表模板编码
      defaultTemplateCode: '32aad2ac-edf2-4a05-86a2-75b78aa2ba64',
      pageNum: 1,
      pageSize: 10,
      total: 0,
      loading: false,
      noMore: false,
      loadedPageNums: [], // 记录已加载的页码，防止重复请求
      // 多选选中的产品
      selectedRows: []
    }
  },
  watch: {
    visible(newVal) {
      if (!newVal) {
        if (this.handleRealtimeSearch && typeof this.handleRealtimeSearch.cancel === 'function') {
          this.handleRealtimeSearch.cancel()
        }
        this.loading = false
        this.searchLoading = false
        this.$nextTick(function() {
          this.closeSelectDropdowns()
        })
        return
      }
      if (!this.searchLoading && !this.loading) {
        this.handleRealtimeSearch()
      }
    },
    // 监听已选中产品变化，更新表格勾选状态
    selectedProducts: {
      handler(newVal) {
        this.$nextTick(function() {
          if (this.$refs.productTable && newVal.length > 0) {
            // 清空原有选择
            this.$refs.productTable.clearSelection()
            // 重新勾选
            this.tableData.forEach(function(row) {
              newVal.forEach(function(item) {
                if (row.VC_FUNDCODE === item.VC_FUNDCODE) {
                  this.$refs.productTable.toggleRowSelection(row, true)
                }
              }.bind(this))
            }.bind(this))
          }
        })
      },
      immediate: true
    }
  },
  beforeDestroy() {
    if (this.handleRealtimeSearch && typeof this.handleRealtimeSearch.cancel === 'function') {
      this.handleRealtimeSearch.cancel()
    }
    this.loading = false
    this.searchLoading = false
  },
  mounted() {
    // 初始化策略类型下拉数据
    this.getSTRATEGY()
    this.getAllSubStrategy()
    // 初始化查询
    this.handleRealtimeSearch()
  },
  methods: {
    getTableRowKey(row, index) {
      return row.VC_FUNDCODE ? row.VC_FUNDCODE + '_' + index : 'empty_' + index
    },
    closeSelectDropdowns() {
      var keys = ['strategySelect', 'subStrategySelect']
      keys.forEach(function(key) {
        var inst = this.$refs[key]
        if (inst && typeof inst.blur === 'function') {
          inst.blur()
        }
      }.bind(this))
    },
    handleComponentMouseLeave() {
      setTimeout(function() {
        const isHoveringDropdown = document.querySelector('.el-select-dropdown:hover');
        const isHoveringTooltip = document.querySelector('.el-tooltip__popper:hover');
        const isHoveringSelector = this.$refs.floatContainer && document.querySelector('.product-float-selector:hover');

        if (!isHoveringDropdown && !isHoveringTooltip && !isHoveringSelector) {
          this.$emit('hide-selector');
        }
      }.bind(this), 100);
    },
    /**
     * 获取策略类型下拉数据
     */
    getSTRATEGY() {
      commonApi
        .getDataBysqlCode({
          indexCode: '9cb2e9ab-1a69-4b0a-809b-a95ab6fcbe62'
        })
        .then(res => {
          const { status, data } = res.data
          if (status === 0) {
            this.strategyType = data
          }
        })
        .catch(() => {})
    },
    getAllSubStrategy() {
      // 调用子策略接口，获取全部数据
      commonApi
        .getDataBysqlCode({
          indexCode: 'b164293a-739f-45d0-a69b-46608a3ac249'
        })
        .then(res => {
          const { status, data } = res.data
          if (status === 0) {
            this.allSubStrategyList = data || []
          }
        })
        .catch(() => {
          this.allSubStrategyList = []
        })
    },
    handleStrategyChange(strategyVal) {
      this.formQuery.subStrategy = ''
      if (strategyVal && this.allSubStrategyList.length > 0) {
        this.subStrategyType = this.allSubStrategyList.filter(item => {
          return item.DIM_EDIT === strategyVal
        })
      } else {
        this.subStrategyType = []
      }
      this.handleRealtimeSearch()
    },

    /**
     * 实时查询
     */
    handleRealtimeSearch: _.debounce(function() {
      this.pageNum = 1
      this.noMore = false
      this.tableData = []
      this.loadedPageNums = [] // 重置已加载页码
      this.queryProductList()
    }, 300),

    /**
     * 查询产品列表
     */
    async queryProductList() {
      // 防止重复请求同一页
      if (this.loading || this.noMore || this.loadedPageNums.indexOf(this.pageNum) > -1) return

      this.loading = true
      this.searchLoading = true
      // 记录已加载页码
      this.loadedPageNums.push(this.pageNum)

      const currentPage = this.pageNum

      // 构造查询参数
      const params = {
        userInput: this.formQuery.productName,
        strategy: this.formQuery.strategy,
        subStrategy: this.formQuery.subStrategy,
        indexCode: this.defaultTemplateCode,
        _pageNum: this.pageNum,
        _pageSize: this.pageSize,
        _pageFlag: true
      }

      // 获取flag参数
      const judgeReturn = this.judgeFlag(this.defaultCheckedKeys)
      if (judgeReturn) {
        params.flag = judgeReturn
      }

      try {
        const raw = commonApi.getDataBysqlCode(params)
        const res = await Promise.resolve(raw)
        if (!res || !res.data) {
          this.noMore = true
          this.loadedPageNums = this.loadedPageNums.filter(function(num) {
            return num !== currentPage
          })
          return
        }
        const resData = res.data
        if (resData.status === 0) {
          const newData = (resData.data && resData.data.rows) || []
          // 合并数据
          this.tableData = currentPage === 1 ? newData : this.tableData.concat(newData)
          // 还原真实总条数
          this.total = (resData.data && resData.data.total) || 0
          // 判断是否无更多数据
          this.noMore = newData.length < this.pageSize || this.tableData.length >= this.total

          // 回显选中状态
          if (this.selectedProducts.length > 0) {
            this.$nextTick(function() {
              if (!this.$refs.productTable) return
              this.tableData.forEach(function(row) {
                this.selectedProducts.forEach(function(item) {
                  if (row.VC_FUNDCODE === item.VC_FUNDCODE) {
                    this.$refs.productTable.toggleRowSelection(row, true)
                  }
                }.bind(this))
              }.bind(this))
            })
          }
        } else {
          this.noMore = true
        }
      } catch (err) {
        console.error('数据请求失败：', err)
        this.noMore = true
        this.loadedPageNums = this.loadedPageNums.filter(function(num) {
          return num !== currentPage
        })
      } finally {
        this.loading = false
        this.searchLoading = false
      }
    },
    // 加载下一页
    loadMore() {
      // 拦截条件
      if (this.loading || this.noMore || (this.total && this.tableData.length >= this.total)) {
        console.log('loadMore被拦截：条件不满足')
        return
      }
      this.pageNum++
      console.log('请求第', this.pageNum, '页')
      this.queryProductList()
    },
    judgeFlag(id) {
      const path = this.routePath

      // 判断是产品结构管理
      if (path.indexOf('/thgl/ctfx/cpjggl') > -1) {
        if (id == 'zstgwb') return 'B'
      }

      // 个券分析 债券分析单独处理
      else if (path.indexOf('/thgl/ctfx/gqfx') > -1 || path.indexOf('/thgl/ctfx/zqfx') > -1) {
        if (id == 'zstgwb') return 'F'
      }
      // 投后的穿透页面
      else if (path.indexOf('/thgl/ctfx') > -1) {
        if (id == 'zstgwb') return 'D'
      }
      // 估值数据查询
      else if (path.indexOf('/thgl/gzsjcx') > -1) {
        if (id == 'zstgwb') return 'B'
      }
      // 投前多产品对比
      else if (path.indexOf('/tqgl/smcpxx') > -1) {
        if (id == 'zstgwb') return 'B'
      }
      // 绩效数据查询
      else if (path.indexOf('/thgl/jxsjcx') > -1) {
        if (id == 'zstgwb') return 'B'
      } else if (path.indexOf('/thgl/jxzb') > -1) {
        if (id == 'zstgwb') return 'B'
      }
      // 投后的绩效报告
      else if (path.indexOf('/jxbg') > -1) {
        if (id == 'zstgwb') return 'B'
      }
      // 策略漂移
      else if (path.indexOf('/thgl/clpy/cpfgclpyjk') > -1 || path.indexOf('/thgl/clpy/clpys') > -1) {
        if (id == 'zstgwb') return 'B'
      }
      // 投顾FOF
      else if (path.indexOf('/thgl/tgfoffx') > -1) {
        if (id == 'zstgwb') return 'B'
      }
      // 组合管理
      else if (path.indexOf('/zhgl') > -1) {
        if (id == 'zstgwb') return 'B'
      }
      // 定制报告
      else if (path.indexOf('/ddportal/template') > -1) {
        if (id == 'zstgwb') return 'B'
      }
      // 报告工坊
      else if (path.indexOf('/jxbg/reportTemplate/reportTemplate') > -1) {
        if (id == 'zstgwb') return 'C'
      }
      // 投中的准入二级菜单
      else if (path.indexOf('/tzgl/zrlcgl') > -1) {
        if (id == 'zstgwb') return 'B'
      } else if (path.indexOf('/tqgl/tc') > -1) {
        if (id == 'zstgwb') return 'B'
      }
      // 需求互动
      else if (path.indexOf('/xqhd/gxhxqgl') > -1) {
        if (id == 'zstgwb') return 'B'
      }
      // FOF子基金维护页面
      else if (path.indexOf('/sjwh/fofzjjwh') > -1) {
        if (id == 'zstgwb') return 'B'
      }
      // 估值表查询
      else if (path.indexOf('/sjwh/gzbdr') > -1) {
        if (id == 'zstgwb') return 'F'
      }

      return ''
    },

    // 多选事件：更新选中的行
    handleSelectionChange(val) {
      this.selectedRows = val
    },

    // 清空选择
    handleClearSelection() {
      if (this.$refs.productTable) {
        this.$refs.productTable.clearSelection()
      }
    },

    // 全选
    handleSelectAll() {
      if (this.$refs.productTable) {
        this.tableData.forEach(function(row) {
          this.$refs.productTable.toggleRowSelection(row, true)
        }.bind(this))
      }
    },

    // 确认选择
    handleConfirmSelect() {
      if (this.selectedRows.length === 0) {
        this.$message.warning('请至少选择一个产品')
        return
      }
      // 触发选择事件
      this.$emit('select-products', this.selectedRows)
      // 隐藏悬浮框
      this.$emit('hide-selector')
      // 清空搜索表单
      this.formQuery.productName = ''
      this.formQuery.strategy = ''
      this.formQuery.subStrategy = ''
    },

    // 隐藏悬浮框
    hideSelector() {
      this.$emit('hide-selector')
    }
  }
}
</script>

<style lang="scss" scoped>
// 隐藏全选框
::v-deep .el-table__header-wrapper .el-checkbox {
  display: none;
}
.product-float-selector {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  z-index: 9999;
  width: 850px;
  background: #ffffff;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-top: 2px;
  overflow: visible !important;
}
.float-search-bar {
  padding: 10px;
  display: flex;
  gap: 10px;
  border-bottom: 1px solid #e4e7ed;
  position: relative;
  z-index: 10000;

  :deep(.el-input),
  :deep(.el-select) {
    flex: 1;
    min-width: 150px;
    z-index: 10001;
  }
}
.float-table-wrapper {
  position: relative;
  max-height: 400px !important;
  padding: 0 10px;
  box-sizing: border-box;

  :deep(.el-table) {
    --el-table-header-text-color: #606266;
    --el-table-row-hover-bg-color: #f5f7fa;
    width: 100%;
    margin: 0;

    // 强制滚动容器样式
    :deep(.el-table__body-wrapper) {
      height: 320px !important;
      max-height: 320px !important;
      overflow-y: auto !important;
      overflow-x: hidden !important;
      // 强制显示滚动条
      scrollbar-width: thin;
      scrollbar-color: #ddd #f5f5f5;

      &::-webkit-scrollbar {
        width: 6px !important;
        display: block !important;
      }

      &::-webkit-scrollbar-thumb {
        background: #ddd !important;
        border-radius: 3px !important;
      }

      &::-webkit-scrollbar-track {
        background: #f5f5f5 !important;
      }

      &::-moz-scrollbar {
        width: 6px !important;
      }
    }
  }

  :deep(.el-table__body tr.current-row > td) {
    background-color: #eaf8fe !important;
  }
}

.load-tip {
  text-align: center;
  font-size: 12px;
  color: #999;
}

.empty-tip {
  padding: 20px;
  text-align: center;
  color: #909399;
  font-size: 12px;
}

.float-footer {
  background: #fafafa;
}
</style>
<style lang="scss">
// 策略类型下拉框样式
.strategy-select-dropdown {
  z-index: 99999 !important;
}

// 子策略类型下拉框样式
.sub-strategy-select-dropdown {
  z-index: 99999 !important;
}

// 通用下拉框层级提升
.el-select-dropdown {
  z-index: 99999 !important;
}
</style>

<template>
  <div class="product-select-container" ref="selectContainer">
    <!-- 触发选择的输入框 -->
    <el-input
      v-model="displayName"
      :placeholder="placeholder"
      :disabled="disabled"
      :readonly="!editable"
      clearable
      @clear="handleClear"
      class="trigger-input"
      :class="{ 'is-disabled': disabled }"
    >
      <i slot="suffix" class="el-icon-arrow-down" :class="{ 'is-active': panelVisible }"></i>
    </el-input>

    <!-- 产品选择面板 -->
    <div
      v-show="panelVisible && !disabled"
      class="product-select-panel"
      ref="selectPanel"
      @click.stop
      :style="{ minWidth: panelMinWidth + 'px', maxHeight: panelMaxHeight + 'px' }"
    >
      <!-- 搜索区域 -->
      <div class="search-bar">
        <el-input
          ref="searchInput"
          v-model="searchForm.keyWord"
          placeholder="输入登记编号/机构代码/机构名称"
          clearable
          :disabled="loading"
          size="medium"
          @input="handleInputDebounce"
          @keyup.enter.native="handleSearch"
          @clear.native="handleSearchClear"
          @click.native="handleSearchInputClick"
        >
          <i slot="prefix" class="el-icon-search"></i>
        </el-input>
      </div>

      <!-- 产品列表 -->
      <vxe-table
        ref="tableRef"
        :data="productList"
        border
        stripe
        size="mini"
        style="width: 100%; margin-top: 10px"
        :loading="loading"
        :empty-text="loading ? '加载中...' : '暂无产品数据'"
        row-id="regCode"
        :radio-config="{ trigger: 'row',  highlight: true, reserve: true }"
        @radio-change="handleRowSelect"
      >


        <!-- 动态渲染列（支持自定义列配置） -->
        <vxe-table-column type="radio" align="center" header-align="center"  width="35"></vxe-table-column>

        <vxe-table-column
          v-for="(item, index) in columns"
          :key="item.prop + index"
          :align="item.align"
          :field="item.prop"
          :show-overflow-tooltip="item.showtooltip"
          :title="item.title"
          :min-width="item.width"
          header-align="center"
          :sortable="item.sortable"
        >
          <template slot-scope="{ row }">
              <span> {{ row[item.prop] | noDataFilter }}</span>

          </template>
        </vxe-table-column>
      </vxe-table>

      <!-- 分页区域 -->
      <vxe-pager
        :current-page="searchForm.pageNum"
        :page-size="searchForm.pageSize"
        :total="total"
        :layouts="['PrevPage','JumpNumber','NextPage','Total']"
        :page-sizes="pagerConfig.pageSizes"
        border
        size="medium"
        class="standard-vxe-pager"
        @page-change="pagination"

      />
    </div>
  </div>
</template>

<script>
import { selectOrgInstListByPage } from '../scripts/api'
import { TABLE_ONG_INST_COLUMNS } from '../scripts/constants'
export default {
  name: 'OrgInstSelect',
  // 组件自定义属性（Props）
  props: {
    // 双向绑定值（选中的产品对象）
    value: {
      type: String,
      default: null
    },
    // 占位提示文字
    placeholder: {
      type: String,
      default: '请选择机构'
    },
    // 是否禁用
    disabled: {
      type: Boolean,
      default: false
    },
    // 是否可编辑（仅控制输入框是否只读）
    editable: {
      type: Boolean,
      default: false
    },
    // 面板最小宽度
    panelMinWidth: {
      type: [Number, String],
      default: 500
    },
    // 面板最大高度
    panelMaxHeight: {
      type: [Number, String],
      default: 400
    },


  },
  data() {
    return {
      panelVisible: false, // 面板显示状态
      loading: false, // 加载状态
      searchForm: {
        keyWord: '', // 搜索关键词
        pageNum: 1, // 当前页
        pageSize: 5, // 每页条数
      },
      regCode:'',
      // 分页信息
      pageList: {
        _pageSize: 5,
        _pageNum: 1,
        _pageFlag: true
      },
      pagerConfig: {
        pageSizes: [5,10,50,100,500], // 每页显示条目数的选项
      },
      columns:TABLE_ONG_INST_COLUMNS,
      // 总条数
      total: 0,
      productList: [], // 产品列表
      selectRow:{},//选中行
      customSearchParams:{},
      innerValue: null,// 内部选中值（解耦v-model）
      debounceDelay:500,
      debounceTimer: null ,  // 防抖定时器
      isSearchClear: false // 新增：标记是否是搜索框清空操作
    }
  },
  mounted() {
    // 仅在非禁用状态绑定事件
    if (!this.disabled) {
      this.bindMouseEvents()
      // 监听全局点击，处理面板外点击隐藏（替代原有的mouseleave）
      document.addEventListener('click', this.handleDocumentClick)
      this.loadProductData() // 初始化加载数据
    }
  },
  computed: {
    // 输入框显示的名称
    displayName() {
      return this.selectRow["glrName"]
    }
  },
  watch: {
    // 监听外部传入的value，同步到内部
    value: {
      immediate: true,
      handler(val) {
        if (!val) return; // 无默认值时清空
        console.log("value:"+val)
        this.regCode=val;
      }
    },
    productList: {
      deep: true, // 深度监听（列表项变化也触发）
      handler(newList) {
        if (newList.length) {
          this.initSelectedRow();
        }
      },
    },
    // 监听面板显示状态，绑定/解绑点击外部关闭事件
    panelVisible(newVal) {
      if (newVal) {
        document.addEventListener('click', this.handleClickOutside)
        this.loadProductData() // 打开面板加载数据
      } else {
        document.removeEventListener('click', this.handleClickOutside)
      }
    }
  },
  methods: {


    // 初始化回选行（编辑回选核心方法）
    async  initSelectedRow() {
      if (!this.productList.length || !this.regCode) return;
      // 2.1 从列表中匹配目标 ID 的行
      console.log("this.productList.length:"+this.productList.length)
      const targetRow = this.productList.find((row) => row.regCode === this.regCode);
      if (!targetRow) {
        //console.warn("未找到登记编号 为", this.regCode, "的机构行数据");
        return;
      }
      console.log("targetRow 为", targetRow);

      // 2.2 回显：选中对应行（以 Element UI 为例）
      this.$refs.tableRef.setCurrentRow(targetRow, true);


    },

    // 绑定原生鼠标事件（核心：仅非禁用时生效）
    bindMouseEvents() {
        const { selectContainer } = this.$refs

        const containerDom = selectContainer.$el || selectContainer
        // 面板移入移入：显示面板
        containerDom.addEventListener('mouseenter', this.openPanel)

    },

    // 解绑鼠标事件
    unbindMouseEvents() {
      const {  selectContainer } = this.$refs
      const containerDom = selectContainer.$el || selectContainer


      if (containerDom) {
        containerDom.removeEventListener('mouseenter', this.openPanel)

      }
    },

    // 点击外部区域关闭面板
    handleClickOutside(e) {
      const selectContainer = this.$refs.selectContainer
      const target = e.target
      const isInContainer = this.isElementInParent(target, selectContainer)
      if (selectContainer && !isInContainer) {
        this.closePanel()
      }
    },
    // 全局点击判断：仅点击面板外才隐藏
    handleDocumentClick(e) {
      if (this.disabled || !this.panelVisible) return
     // 如果是搜索框清空操作，忽略隐藏逻辑
      if (this.isSearchClear) {
        this.isSearchClear = false // 重置标记
        return
      }
      const selectContainer = this.$refs.selectContainer
      const selectPanel = this.$refs.selectPanel
      const target = e.target
      // 兼容方案：判断元素是否在容器/面板内（替代contains）
      const isInContainer = this.isElementInParent(target, selectContainer)
      const isInPanel = this.isElementInParent(target, selectPanel)
      // 仅点击容器和面板外才隐藏
      if (!isInContainer && !isInPanel) {
        this.panelVisible = false
      }
    },

    // 兼容方法：判断元素是否在父元素内（替代contains）
    isElementInParent(child, parent) {
      if (!child || !parent) return false
      // 遍历元素的父节点，直到找到目标父元素或document
      let current = child
      while (current) {
        if (current === parent) {
          return true
        }
        current = current.parentNode
      }
      return false
    },

    // 对外暴露的方法：手动打开面板
    openPanel() {
      if (!this.disabled) {
        this.panelVisible = true
      }
    },
    // 对外暴露的方法：手动关闭面板
    closePanel() {
      this.panelVisible = false
    },
    // 对外暴露的方法：手动刷新数据
    refreshData() {
      this.loadProductData()
    },
    // 对外暴露的方法：清空选中值
    clearValue() {
      this.handleClear()
    },

    // 内部方法：加载产品数据
   loadProductData() {
        // 强制保持面板显示
        this.panelVisible = true
        this.loading = true
        // 构造请求参数（合并分页、搜索、自定义参数）
        const params = {
          pageNum: this.searchForm.pageNum,
          pageSize: this.searchForm.pageSize,
          keyWord: this.searchForm.keyWord.trim(),
          ...this.customSearchParams
        }

        this.productList = []
        selectOrgInstListByPage(params)
          .then((res) => {
            const {data, status} = res.data
            if (status === 200 && data) {
              this.productList = data.list || []
              this.total = data.total || 0

            } else {
              this.productList = []
              this.total = 0
            }

            this.loading = false
          })
          .catch((e) => {
            this.loading = false
          })
    },

    // 切换面板显示/隐藏
    togglePanel() {
      this.panelVisible = !this.panelVisible
    },



    // ========== 核心：防抖输入处理 ==========
    handleInputDebounce() {
      // 1. 清除上一次的定时器（关键：避免连续输入多次触发）
      clearTimeout(this.debounceTimer)

      // 2. 空关键词特殊处理（可选：清空结果/直接查询全部）
      if (!this.searchForm.keyWord.trim()) {
        this.searchResult = []
        this.showResult = false
        return
      }

      // 3. 延迟指定时间后执行查询
      this.debounceTimer = setTimeout(() => {
        this.loadProductData()
      }, this.debounceDelay)
    },

    handleSearchClear(){

      this.isSearchClear = true // 标记为清空操作
      this.searchForm.keyWord=''
      if (this.$refs.searchInput) {
        const inputEl = this.$refs.searchInput.$el.querySelector('input')
        if (inputEl) inputEl.value = ''
      }
      clearTimeout(this.debounceTimer)
      this.searchForm.pageNum = 1
      this.loadProductData()
      this.panelVisible=true
      this.$forceUpdate()

    },

    // ========== 兼容方案：监听清空按钮点击 ==========
    handleSearchInputClick(e) {
      // 识别清空按钮点击（Element UI清空按钮类名）
      if (e.target.classList.contains('el-input__clear')) {
        this.handleSearchClear()
      }
    },

    // 关键词搜索
    handleSearch() {
      this.searchForm.pageNum = 1
      this.loadProductData()
    },



    // 选中表格行
    handleRowSelect({row}) {

      // 1. 基础校验
      if (!row) return
      this.selectRow=row
      this.$emit('select-change',   this.selectRow)
      this.closePanel()

    },

    // 清空选中值
    handleClear() {
      this.selectRow = null
    },
    /**
     * @description 监听分页
     */
    pagination(val) {
      const { currentPage, pageSize } = val;
      // 起始页
      this.searchForm.pageNum = currentPage;
      // 每页数量
      this.searchForm.pageSize = pageSize;
      this.loadProductData()

    },
  },
  beforeDestroy() {
    // 销毁前移除事件监听
    document.removeEventListener('click', this.handleClickOutside)
    this.unbindMouseEvents()
    document.removeEventListener('click', this.handleDocumentClick)
    // 组件销毁时清除定时器，避免内存泄漏
    clearTimeout(this.debounceTimer)
  },
  // 注册组件方法（方便父组件通过ref调用）
  expose: ['openPanel', 'closePanel', 'refreshData']
}
</script>

<style scoped>
.product-select-container {
  position: relative;
  width: 100%;
  box-sizing: border-box;
}

.trigger-input {
  width: 100%;
  box-sizing: border-box;
}

.product-select-panel {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 9999;
  width: 100%;
  overflow: auto;
  background: #fff;
  border: 1px solid #e6e6e6;
  border-radius: 4px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 10px;
  margin-top: 2px;
  box-sizing: border-box;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.el-icon-arrow-down {
  transition: transform 0.2s ease;
}

.el-icon-arrow-down.is-active {
  transform: rotate(180deg);
}

.is-disabled .el-icon-arrow-down {
  color: #c0c4cc;
  cursor: not-allowed;
}
</style>

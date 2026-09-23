<template>
  <div class="product-select-input" ref="inputContainer">
    <el-tooltip
      :content="selectedProductNames"
      :disabled="!selectedProductNames"
      effect="dark"
      placement="top-start"
    >
      <el-input
        :value="selectedProductNames"
        clearable
        @keydown.native.prevent
        @paste.native.prevent
        :style="{ cursor: 'pointer', width: inputWidth }"
        @clear="handleClear"
        :placeholder="placeholder"
        :size="size"
        @click.native="showSelector"
        @mouseenter.native="showSelector"
        @blur.native="handleInputBlur"
      />
    </el-tooltip>

    <ProductFloatSelectorMultiple
      :visible="selectorVisible"
      :route-path="routePath || $route.path"
      :selected-products="modelValue"
      @select-products="handleSelectProducts"
      @hide-selector="hideSelector"
      @mouseenter.native="handleSelectorEnter"
      @mouseleave.native="handleSelectorLeave"
    />
  </div>
</template>

<script>
import ProductFloatSelectorMultiple from './ProductFloatSelectorMultiple'

export default {
  name: 'ProductSelectInputMultiple',
  components: { ProductFloatSelectorMultiple },
  model: {
    prop: 'modelValue',
    event: 'update:modelValue'
  },
  props: {
    modelValue: {
      type: Array,
      default: function() {
        return []
      }
    },
    placeholder: {
      type: String,
      default: '请选择产品'
    },
    size: {
      type: String,
      default: 'small',
      validator: function(val) {
        return ['small', 'medium', 'large'].indexOf(val) > -1
      }
    },
    inputWidth: {
      type: String,
      default: '240px'
    },
    routePath: {
      type: String,
      default: ''
    }
  },
  computed: {
    // 拼接选中的产品名称
    selectedProductNames() {
      if (!this.modelValue || this.modelValue.length === 0) {
        return ''
      }
      const names = this.modelValue.map(function(item) {
        return item.VC_FUNDNAME || ''
      }).filter(function(name) {
        return name
      })
      // 超过3个显示省略
      if (names.length > 3) {
        return names.slice(0, 3).join('、') + ' 等' + names.length + '个产品'
      }
      return names.join('、')
    }
  },
  data: function() {
    return {
      selectorVisible: false, // 悬浮框显示隐藏
      isHoveringSelector: false // 鼠标是否在悬浮框上，防止误关
    }
  },
  mounted: function() {
    document.addEventListener('click', this.handleGlobalClick, true)
  },
  beforeDestroy: function() {
    document.removeEventListener('click', this.handleGlobalClick, true)
  },
  methods: {
    // 显示悬浮框
    showSelector: function() {
      this.selectorVisible = true
      this.isHoveringSelector = false
    },
    // 隐藏悬浮框
    hideSelector: function() {
      this.selectorVisible = false
      this.isHoveringSelector = false
    },
    // 鼠标移入悬浮框
    handleSelectorEnter: function() {
      this.isHoveringSelector = true
    },
    // 鼠标移出悬浮框
    handleSelectorLeave: function() {
      var isHoverDropdown = document.querySelector('.el-select-dropdown:hover')
      var isHoverTooltip = document.querySelector('.el-tooltip__popper:hover')
      var isHoverSelf = document.querySelector('.product-float-selector:hover')
      if (!isHoverDropdown && !isHoverTooltip && !isHoverSelf) {
        this.hideSelector()
      }
    },
    // 输入框失焦
    handleInputBlur: function() {
      var _this = this
      setTimeout(function() {
        !_this.isHoveringSelector && _this.hideSelector()
      }, 100)
    },
    // 清除选择
    handleClear: function() {
      this.$emit('update:modelValue', [])
      this.$emit('clear')
    },
    // 选择产品核心回调
    handleSelectProducts: function(productArr) {
      this.$emit('update:modelValue', productArr)
      this.$emit('select', productArr)
      this.hideSelector() // 隐藏悬浮框
    },
    // 全局点击关闭
    handleGlobalClick: function(e) {
      var isHoverDropdown = document.querySelector('.el-select-dropdown:hover')
      if (isHoverDropdown) return
      // 点击区域不是输入框也不是悬浮框，关闭
      var inputEl = this.$refs.inputContainer
      var selectorEl = document.querySelector('.product-float-selector')
      if (inputEl && selectorEl) {
        if (!inputEl.contains(e.target) && !selectorEl.contains(e.target)) {
          this.hideSelector()
        }
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.product-select-input {
  position: relative;
  display: inline-block;
}
</style>

<template>
  <div ref="inputContainer" class="product-select-input">
    <el-tooltip
      :content="(modelValue && modelValue.VC_FUNDNAME) || ''"
      :disabled="!modelValue"
      effect="dark"
      placement="top-start"
    >
      <el-input
        :value="(modelValue && modelValue.VC_FUNDNAME) || ''"
        :style="{ cursor: 'pointer', width: inputWidth }"
        :placeholder="placeholder"
        :size="size"
        clearable
        @clear="handleClear"
        @keydown.native.prevent
        @paste.native.prevent
        @click.native="showSelector"
        @mouseenter.native="showSelector"
        @blur.native="handleInputBlur"
      />
    </el-tooltip>

    <ProductFloatSelector
      :visible="selectorVisible"
      :route-path="routePath || $route.path"
      @select-product="handleSelectProduct"
      @hide-selector="hideSelector"
      @mouseenter.native="handleSelectorEnter"
      @mouseleave.native="handleSelectorLeave"
    />
  </div>
</template>

<script>
import ProductFloatSelector from './ProductFloatSelector'

export default {
  name: 'ProductSelectInput',
  components: { ProductFloatSelector },
  model: {
    prop: 'modelValue',
    event: 'update:modelValue'
  },
  props: {
    modelValue: {
      type: Object,
      default: null
    },
    placeholder: {
      type: String,
      default: '请选择产品'
    },
    size: {
      type: String,
      default: 'small',
      validator: function(val) {
        return ['mini', 'small', 'medium', 'large'].includes(val)
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
      this.$emit('visibility-change', true)
      this.isHoveringSelector = false
    },
    // 隐藏悬浮框
    hideSelector: function() {
      this.selectorVisible = false
      this.$emit('visibility-change', false)
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
      this.$emit('update:modelValue', null)
      this.$emit('clear')
    },
    // 选择产品核心回调
    handleSelectProduct: function(productArr) {
      var product = (productArr && productArr[0]) || null
      this.$emit('update:modelValue', product)
      this.$emit('select', product)
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

<template>
  <el-select
    v-model="selectedValue"
    :multiple="multiple"
    :placeholder="placeholder"
    :disabled="disabled"
    filterable
    :filter-method="handleFilter"
    :remote="false"
    :loading="searchLoading"
    :reserve-keyword="false"
    @visible-change="handleVisibleChange"
    @change="handleSelectChange"
    clearable
    :size="size"
    style="width: 100%;"
    ref="productSelect"
  >
    <div v-if="productList.length > 0" style="padding: 8px;">共{{productList.length}}条产品数据</div>
    <el-option v-if="productList.length === 0 && !searchLoading" label="请选择产品" value="" disabled></el-option>

    <el-option
      v-for="item in filteredProductList"
      :key="item.VC_FUNDCODE"
      :value="item.VC_FUNDCODE"
    >
      <span>({{ item.VC_FUNDCODE }}) {{ item.VC_FUNDNAME }}</span>
    </el-option>

    <template v-slot:tag="{ value, close }" v-if="multiple">
      <el-tag closable @close="close" size="mini">
        {{ value }}
      </el-tag>
    </template>

  </el-select>
</template>

<script>
import commonApi from '@/api/common'

export default {
  name: 'ProductSelectSearch',
  props: {
    modelValue: {
      type: [String, Array],
      default: () => []
    },
    multiple: {
      type: Boolean,
      default: false
    },
    placeholder: {
      type: String,
      default: '请选择产品'
    },
    disabled: {
      type: Boolean,
      default: false
    },
    forceFlag: {
      type: String,
      default: 'B'
    },
    size: {
      type: String,
      default: 'small',
      validator: (val) => ['small', 'medium', 'large'].includes(val)
    }
  },
  data() {
    return {
      searchLoading: false,
      productList: [], // 缓存全量产品数据
      filteredProductList: [],
      searchKeyword: '',
      selectedValue: this.multiple ? [] : '',
      isDataLoaded: false // 是否已加载过数据
    }
  },
  watch: {
    selectedValue(val) {
      this.$nextTick(() => {
        if (!this.multiple) {
          const input = this.$el.querySelector('.el-select__input');
          if (input) input.value = val;
        }
      });
    },
    modelValue: {
      handler(val) {
        console.log('组件接收的modelValue：', val);
        this.selectedValue = val
      },
      immediate: true,
      deep: true
    },
    searchKeyword: {
      handler(val) {
        this.filterProductList(val.trim())
      },
      immediate: true
    },
    productList: {
      handler() {
        this.filterProductList(this.searchKeyword)
      },
      immediate: true,
      deep: true
    }
  },
  methods: {
    handleFilter(keyword) {
      this.searchKeyword = keyword;
    },
    async handleVisibleChange(visible) {
      this.searchKeyword = '';
      if (visible) {
        await this.loadAllProductData()
        this.$nextTick(() => {
          if (this.$refs.productSelect) {
            this.$refs.productSelect.visible = true
          }
        })
      }
    },

    async loadAllProductData() {
      if (this.isDataLoaded) return
      if (this.searchLoading) return

      this.searchLoading = true
      try {
        const params = {
          userInput: '',
          indexCode: '32aad2ac-edf2-4a05-86a2-75b78aa2ba64',
          flag: this.forceFlag
        }
        const response = await commonApi.getDataBysqlCode(params)
        if (response.data && response.data.status === 0) {
          this.productList = response.data.data || []
          this.isDataLoaded = true
        } else {
          this.productList = []
          this.$message.warning('产品数据加载失败')
        }
      } catch (err) {
        this.productList = []
        this.$message.error('产品数据加载失败，请重试')
      } finally {
        this.searchLoading = false
        if (!this.multiple && this.selectedValue) {
          const exists = this.productList.some(item => item.VC_FUNDCODE === this.selectedValue);
          if (!exists) {
            console.warn(`回显值 ${this.selectedValue} 不在产品列表中`);
          }
        }
      }
    },

    filterProductList(keyword) {
      if (!keyword) {
        this.filteredProductList = [...this.productList]
        return
      }
      const keywordStr = String(keyword).trim();
      this.filteredProductList = this.productList.filter(item => {
        const code = String(item.VC_FUNDCODE || '');
        const name = String(item.VC_FUNDNAME || '');
        return code.includes(keywordStr) || name.includes(keywordStr);
      })
    },

    handleSelectChange(val) {
      this.$emit('update:modelValue', val);
      this.$emit('change', val);

      const selectedProduct = this.productList.find(item => item.VC_FUNDCODE === val) || null;
      this.$emit('select-product', selectedProduct);
    },
  },
  created() {
    this.loadAllProductData();
  }
}
</script>

<style lang="scss" scoped>
::v-deep .el-select--small {
  .el-select__input {
    height: 32px !important;
    line-height: 32px !important;
    font-size: 12px !important;
  }

  .el-select__caret {
    line-height: 32px !important;
  }
}

::v-deep .el-select-dropdown {
  max-height: 400px !important;
}
::v-deep .el-select__input {
  color: #333 !important;
  background: #fff !important;
}
::v-deep .el-select-dropdown__item {
  font-size: 12px !important;
  padding: 6px 16px !important;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

::v-deep .el-select-dropdown__item.is-disabled {
  color: #999;
  cursor: not-allowed;
}
</style>

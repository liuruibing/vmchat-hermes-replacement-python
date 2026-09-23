<template>
  <div id="dd-query">
    <div class="funds-filter">
      <div class="funds-filter-search">
        <div class="funds-search-simple">
          <el-row>
            <el-col :span="22" style="text-align: center">
              <el-form :inline="true" :model="simpleSearch">
                <el-form-item label="产品名称">
                  <el-input
                    v-model="simpleSearch.productName"
                    placeholder="产品名称"
                    size="small"
                  ></el-input>
                </el-form-item>
                <el-form-item label="管理人">
                  <el-input
                    v-model="simpleSearch.custodian"
                    placeholder="管理人"
                    size="small"
                  ></el-input>
                </el-form-item>
                <el-form-item label="机构规模">
                  <el-select
                    v-model="simpleSearch.orzScale"
                    placeholder="机构规模(不限)"
                    size="small"
                    clearable
                    @change="checkBoxfile"
                  >
                    <el-option
                      v-for="item in orzScaleOptions"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                    >
                      <el-checkbox v-model="item.checkedState">{{
                        item.label
                      }}</el-checkbox>
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" size="small" icon="el-icon-search"
                    >查询</el-button
                  >
                  <el-button
                    type="primary"
                    size="info"
                    plain
                    icon="el-icon-refresh-left"
                    >重置</el-button
                  >
                  <el-button type="primary" size="small" icon="el-icon-bottom"
                    >导 出</el-button
                  >
                </el-form-item>
              </el-form>
            </el-col>
            <el-col :span="2">
              <el-button
                type="primary"
                plain
                size="small"
                @click="showMoreQuery"
              >
                <span> {{ isShowMoreQuery ? "收起筛选" : "展开筛选" }}</span>
                <i
                  :class="
                    isShowMoreQuery
                      ? 'el-icon-caret-top'
                      : 'el-icon-caret-bottom'
                  "
                ></i>
              </el-button>
            </el-col>
          </el-row>
        </div>
      </div>
      <transition name="fade">
        <div v-show="isShowMoreQuery">
          <MoreQuery ref="MoreQuery" />
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import Constant from "./constant.js";
import MoreQuery from "./more-query.vue";
export default {
  name: "dd-query",
  components: { MoreQuery },
  data() {
    return {
      orzScaleOptions: Constant.orzScaleOptions,
      simpleSearch: {
        productName: "",
        custodian: "",
        orzScale: ""
      },
      isShowMoreQuery: false
    };
  },
  methods: {
    checkBoxfile(val) {
      this.orzScaleOptions.forEach(itm => {
        if (val === itm.value) {
          itm.checkedState = true;
        } else {
          itm.checkedState = false;
        }
      });
    },
    showMoreQuery() {
      this.isShowMoreQuery = !this.isShowMoreQuery;
    }
  }
};
</script>

<style lang="scss" scoped>
#dd-query {
  .funds-filter {
    width: 100%;
    .funds-filter-search {
      //border-bottom: 1px solid #e1e0e0;
    }
  }

  // elementUI样式穿透
  ::v-deep .el-button {
    background-color: #fcaa4d;
    border-color: transparent;
  }
  ::v-deep.el-button.is-plain {
    background-color: #fff;
    border: 1px solid #4f95dd;
    color: #4f95dd;
  }
  ::v-deep.el-button.is-plain:hover {
    background-color: #4f95dd;
    color: #fff;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
}
</style>

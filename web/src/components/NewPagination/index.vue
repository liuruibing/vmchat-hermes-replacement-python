<template>
  <div :class="{ hidden: hidden }" class="clearfix">
    <div class="pagination-container">
      <el-pagination
        :background="background"
        :current-page.sync="currentPage"
        :page-size.sync="pageSize"
        :layout="layout"
        :page-sizes="pageSizes"
        :total="total"
        v-bind="$attrs"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script>
import { scrollTo } from "@/utils/scrollTo";

export default {
  name: "Pagination",
  props: {
    total: {
      required: true,
      type: Number,
    },
    page: {
      type: Number,
      default: 1,
    },
    limit: {
      type: Number,
      default: 10,
    },
    pageSizes: {
      type: Array,
      default() {
        //return [10, 20, 30, 50, 100, 500, 2000]
        return [10, 20, 30, 50, 100, 200];
      },
    },
    layout: {
      type: String,
      default: "total, sizes, prev, pager, next, jumper",
    },
    background: {
      type: Boolean,
      default: true,
    },
    autoScroll: {
      type: Boolean,
      default: true,
    },
    hidden: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      // 当前页
      currentPage: 1,
      // 每页显示条目个数，默认10
      pageSize: 10,
    };
  },
  created() {
    this.currentPage = this.page;
    this.pageSize = this.limit;
  },
  computed: {
    // currentPage: {
    //   get() {
    //     return this.page
    //   },
    //   set(val) {
    //     this.$emit('update:page', val)
    //   }
    // },
    // pageSize: {
    //   get() {
    //     return this.limit
    //   },
    //   set(val) {
    //     this.$emit('update:limit', val)
    //   }
    // }
  },
  methods: {
    // pageSize改变
    handleSizeChange(val) {
      // 每页显示条目个数
      this.pageSize = val;
      // pageSize改变重置为第一页
      this.handleCurrentChange(1);
    },
    // currentPage改变
    handleCurrentChange(val) {
      // 当前页
      this.currentPage = val;
      this.$emit("pagination", { page: val, limit: this.pageSize });
      if (this.autoScroll) {
        scrollTo(0, 800);
      }
    },
  },
  watch: {
    // 传递的页码改变
    page() {
      this.currentPage = this.page;
    },
  },
};
</script>

<style scoped>
.pagination-container {
  background: #fff;
  padding: 0px;
  float: right;
  margin-top: 10px !important;
}
.pagination-container.hidden {
  display: none;
}
</style>

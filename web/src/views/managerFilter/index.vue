<template>
  <div class="managerFilter">
    <!-- 投资经理筛选 -->
    <managerQuery></managerQuery>
    <!-- 顶部查询 -->

    <!-- 列表 -->
    <div class="tabletable_top">
      <span
        >经理数量：<span class="color_e6a23c">10834</span> 条， 管理人：<span
          class="color_e6a23c"
          >30686</span
        >
        条，更新日期：2022-09-05</span
      >
      <span>
        <el-button type="primary" size="small">导出Excel</el-button>
      </span>
    </div>
    <el-table
      :data="tableData"
      stripe
      style="width: 100%"
      v-loading="tableLoading"
      id=""
    >
      <el-table-column label="序号" type="index" align="center" width="50">
      </el-table-column>
      <el-table-column
        label="投资经理"
        header-align="center"
        align=""
        min-width="120px"
        prop="f1"
      >
        <template slot-scope="scope">
          <span class="color_4f95dd" @click="jumpPage('1', scope.row)">{{
            scope.row.f1 || "-"
          }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="所在公司"
        header-align="center"
        align=""
        min-width="120px"
        prop="f2"
      >
        <template slot-scope="scope">
          <span class="color_4f95dd">{{ scope.row.f2 || "-" }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="主要策略"
        header-align="center"
        align=""
        min-width="120px"
        prop="f3"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.f3 || "-" }}</span>
        </template>
      </el-table-column>
      <el-table-column label="产品数量" header-align="center">
        <el-table-column
          label="存储中"
          header-align="center"
          align="center"
          min-width="120px"
          prop="f4"
        ></el-table-column>
        <el-table-column
          label="累计数"
          header-align="center"
          align="center"
          min-width="120px"
          prop="f5"
        ></el-table-column>
      </el-table-column>
      <el-table-column label="代表产品" header-align="center">
        <el-table-column
          label="产品名称"
          header-align="center"
          align=""
          min-width="120px"
          prop="f6"
        >
          <template slot-scope="scope">
            <span class="color_4f95dd" @click="jumpPag1e(scope.row)">{{
              scope.row.f6 || "-"
            }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="成立以来收益率"
          header-align="center"
          align="right"
          min-width="120px"
          prop="f7"
        >
          <template slot-scope="scope">
            <span
              :class="
                scope.row.f7 && scope.row.f7 > 0
                  ? 'color_F56C6C'
                  : 'color_67C23A'
              "
              >{{ scope.row.f7 | numberToFixedStr(2, 100, "%") }}</span
            >
          </template>
        </el-table-column>
        <el-table-column
          label="成立以来最大回撤"
          header-align="center"
          align="right"
          min-width="120px"
          prop="f8"
        >
          <template slot-scope="scope">
            <span>{{ scope.row.f8 | numberToFixedStr(2, 100, "%") }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="复权累计净值"
          header-align="center"
          align="right"
          min-width="120px"
          prop="f9"
        >
          <template slot-scope="scope">
            <span>{{ scope.row.f9 || "-" }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="净值日期"
          header-align="center"
          align="center"
          min-width="120px"
          prop="f10"
        >
          <template slot-scope="scope">
            <span>{{ scope.row.f10 || "-" }}</span>
          </template>
        </el-table-column>
      </el-table-column>
    </el-table>
    <div style="height: 50px">
      <Pagination
        :total="total"
        :limit="formQuery.pageSize"
        :page="formQuery.pageNum"
        @pagination="pagination"
      />
    </div>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination";
import managerQuery from "./components/manager-query.vue";
export default {
  components: { Pagination, managerQuery },
  data() {
    return {
      formQuery: {
        pageSize: 20,
        pageNum: 1
      },
      total: 0,
      tableLoading: false,
      tableData: [
        {
          f1: "赵媛媛",
          f2: "建泓时代",
          f3: "股票多头",
          f4: 6,
          f5: 7,
          f6: "建泓盈富四号",
          f7: 12.8720,
          f8: 0.2988,
          f9: 13.8720,
          f10: "2021-03-02"
        },
        {
          f1: "高海兵",
          f2: "南方海慧",
          f3: "股票多头",
          f4: 1,
          f5: 1,
          f6: "南方海慧一号",
          f7: 63.08839,
          f8: 0.489,
          f9: 64.0883,
          f10: "2021-03-02"
        },
        {
          f1: "周锐锋",
          f2: "金源亨立",
          f3: "管理期货",
          f4: 1,
          f5: 1,
          f6: "善行1号",
          f7: 51.79889,
          f8: 0.353,
          f9: 52.7988,
          f10: "2021-03-02"
        },
        {
          f1: "廖茂林",
          f2: "正因私募",
          f3: "股票多头",
          f4: 2,
          f5: 3,
          f6: "正圆壹号",
          f7: "47.7269",
          f8: 0.4572,
          f9: 48.7269,
          f10: "2021-03-02"
        },
        {
          f1: "陈子重",
          f2: "太信环球",
          f3: "宏观策略",
          f4: 3,
          f5: 3,
          f6: "CP主选策略",
          f7: 36.1503,
          f8: 0.0603,
          f9: 60.1725,
          f10: "2021-03-02"
        },
        {
          f1: "唐婧人",
          f2: "上海烤奇投资",
          f3: "管理期货",
          f4: 6,
          f5: 7,
          f6: "婧奇光合长谷",
          f7: 28.6042,
          f8: 0.2868,
          f9: 29.6042,
          f10: "2021-03-02"
        },
        {
          f1: "王强",
          f2: "上海保银私荐",
          f3: "股票多空",
          f4: 1,
          f5: 3,
          f6: "Pinpoint China Fund",
          f7: 19.2726,
          f8: 0.4214,
          f9: 20.2726,
          f10: "2021-03-02"
        }
      ]
    };
  },
  methods: {
    pagination() {},
    jumpPage(type, data) {
      if (type == "1") {
        this.$router.push({ path: "/tqgl/tzjlfx" });
      }
    },
    jumpPag1e() {
      this.$router.push({
        path: "/cpxq"
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.tabletable_top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
}
.color_e6a23c {
  color: #e6a23c;
}
.color_4f95dd {
  color: #4f95dd;
  cursor: pointer;
}
.color_F56C6C {
  color: #f56c6c;
}
.color_67C23A {
  color: #67c23a;
}
</style>

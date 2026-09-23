<template>
  <div class="tabletable">
    <div class="tabletable_top">
      <span
        >共
        <span class="color_e6a23c">337211</span>
        条数据，更新日期：2022-09-05</span
      >
      <span>
        <el-button size="small">自定义指标</el-button>
        <el-button type="primary" size="small">导出Excel</el-button>
      </span>
    </div>
    <el-table
      :data="tableData"
      stripe=""
      style="width: 100%"
      v-loading="tableLoading"
      id=""
    >
      <el-table-column label="关注" align="center" width="55">
        <template slot-scope="scope">
          <el-link :underline="false" type="primary" style="font-size: 14px"
            >关注</el-link
          >
        </template>
      </el-table-column>
      <el-table-column label="对比" align="center" width="55">
        <template slot-scope="scope">
          <el-checkbox v-model="scope.ff"></el-checkbox>
        </template>
      </el-table-column>
      <el-table-column label="序号" type="index" align="center" width="50">
      </el-table-column>
      <el-table-column
        v-for="item in column"
        :key="item.prop"
        :prop="item.prop"
        :label="item.label"
        :min-width="item.minWidth || '100'"
        :width="item.width"
        header-align="center"
        :align="item.align"
        :sortable="item.sortable"
        :show-overflow-tooltip="!item.noshowoverflowtooltip"
      >
        <template slot-scope="scope">
          <span
            v-if="item.filter == 'fund'"
            class="color_4f95dd fund_cell"
            @click="jumpPage(scope.row)"
          >
            <span class="fund_name" :title="scope.row[item.prop]">{{
              scope.row[item.prop] | noDataFilter
            }}</span>
            <el-tag
              size="mini"
              type="warning"
              style="margin-bottom:0 !important"
              v-if="scope.row.isSD"
              >深度</el-tag
            >
          </span>
          <span v-else-if="item.filter == 'moneyYuan'">
            {{ scope.row[item.prop] | moneyYuan }}
          </span>
          <span v-else-if="item.filter == 'numberToFixedStr2'">
            {{ scope.row[item.prop] | numberToFixedStr(2, 100, "%") }}
          </span>
          <span v-else-if="item.filter == 'star'">
            <el-rate
              v-model="scope.row[item.prop]"
              disabled
              text-color="#ff9900"
            >
            </el-rate>
          </span>
          <span v-else>{{ scope.row[item.prop] | noDataFilter }}</span>
        </template>
      </el-table-column>
    </el-table>
    <div style="height: 50px">
      <Pagination
        :total="total"
        :limit="formQuery._pageSize"
        :page="formQuery._pageNum"
        @pagination="pagination"
      />
    </div>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination";
export default {
  components: { Pagination },
  data() {
    return {
      formQuery: {
        _pageSize: 20,
        _pageNum: 1
      },
      total: 0,
      tableLoading: false,
      tableData: [
        {
          f1: "弗居绝对收益配置1号",
          f2: "多策略",
          f3: "芜湖弗居投资",
          f4: "--",
          f5: 4,
          f6: "--",
          f7: "--",
          f8: 10.4107,
          f9: 10.4107,
          f10: 10.4107,
          f11: "875.78%",
          f12: "941.07%",
          f13: "4.83%",
          f14: "--",
          f15: "--",
          f16: 1.02,
          f17: "0~5亿",
          isSD: true
        },
        {
          f1: "粤资价值成长9号",
          f2: "股票多空",
          f3: "深圳前海粤资基金",
          f4: "--",
          f5: 4,
          f6: "--",
          f7: "--",
          f8: 13.1535,
          f9: 14.0598,
          f10: 25.0745,
          f11: "810.57%",
          f12: "2,407.45%",
          f13: "28.26%",
          f14: "139.72%",
          f15: "54.02%",
          f16: 2.55,
          f17: "0~5亿"
        },
        {
          f1: "建泓时代朝阳传承1号",
          f2: "股票多头",
          f3: "建泓时代",
          f4: "--",
          f5: 0,
          f6: "--",
          f7: "--",
          f8: 3.4202,
          f9: 6.0902,
          f10: 8.6164,
          f11: "761.64%",
          f12: "761.64%",
          f13: "24.30%",
          f14: "--",
          f15: "159.59%",
          f16: 22.05,
          f17: "5~10亿",
          isSD: true
        },
        {
          f1: "建泓时代朝阳传承",
          f2: "股票多头",
          f3: "建泓时代",
          f4: "赵媛媛",
          f5: 0,
          f6: "--",
          f7: "--",
          f8: 8.611,
          f9: 8.611,
          f10: 8.611,
          f11: "761.10%",
          f12: "761.10%",
          f13: "24.27%",
          f14: "--",
          f15: "153.34%",
          f16: 22.92,
          f17: "5~10亿",
          isSD: true
        },
        {
          f1: "殊馥财富通3号",
          f2: "债券基金",
          f3: "上海殊馥投资",
          f4: "--",
          f5: 3,
          f6: "--",
          f7: "--",
          f8: 11.63,
          f9: 11.63,
          f10: 11.63,
          f11: "546.11%",
          f12: "1,063.00%",
          f13: "4.21%",
          f14: "119.82%",
          f15: "246.08%",
          f16: 0.48,
          f17: "20~50亿"
        },
        {
          f1: "银德1期",
          f2: "股票多头",
          f3: "深圳银德资本",
          f4: "杨媛媛",
          f5: 5,
          f6: "--",
          f7: "--",
          f8: 8.972,
          f9: 9.376,
          f10: 12.642,
          f11: "454.52%",
          f12: "1,164.20%",
          f13: "20.85%",
          f14: "47.56%",
          f15: "198.17%",
          f16: 0.23,
          f17: "0~5亿"
        },
        {
          f1: "中碳牛盈8号",
          f2: "债券基金",
          f3: "北京中碳创富投资",
          f4: "--",
          f5: 3,
          f6: "--",
          f7: "--",
          f8: 4.305,
          f9: 4.305,
          f10: 4.305,
          f11: "424.36%",
          f12: "330.50%",
          f13: "27.98%",
          f14: "249.29%",
          f15: "66.33%",
          f16: 3.73,
          f17: "10~20亿",
          isSD: true
        },
        {
          f1: "外贸信托-汇鑫56号结构化第15期信托单元",
          f2: "债券基金",
          f3: "--",
          f4: "--",
          f5: 0,
          f6: "--",
          f7: "--",
          f8: 0.3482,
          f9: 0.3482,
          f10: 0.3482,
          f11: "410.55%",
          f12: "-47.62%",
          f13: "90.48%",
          f14: "-19.70%",
          f15: "--",
          f16: "--",
          f17: "--",
          isSD: true
        },
        {
          f1: "贝顿天成量化多头",
          f2: "股票多头",
          f3: "广州贝顿资产",
          f4: "--",
          f5: 0,
          f6: "--",
          f7: "--",
          f8: 1.012,
          f9: 1.012,
          f10: 1.012,
          f11: "358.55%",
          f12: "363.60%",
          f13: "3.05%",
          f14: "--",
          f15: "391.74%",
          f16: 1.35,
          f17: "0~5亿"
        },
        {
          f1: "诚泰嘉豪成长",
          f2: "多策略",
          f3: "诚泰资产",
          f4: "--",
          f5: 4,
          f6: "--",
          f7: "--",
          f8: 0.95,
          f9: 3.91,
          f10: 7.8372,
          f11: "333.88%",
          f12: "683.72%",
          f13: "24.18%",
          f14: "467.20%",
          f15: "--",
          f16: "--",
          f17: "0~5亿"
        },
        {
          f1: "赢康丰盈三号",
          f2: "多策略",
          f3: "上海赢康私募",
          f4: "--",
          f5: 0,
          f6: "--",
          f7: "--",
          f8: 4.025,
          f9: 4.025,
          f10: 4.025,
          f11: "320.14%",
          f12: "302.50%",
          f13: "61.29%",
          f14: "--",
          f15: "456.89%",
          f16: 1.33,
          f17: "0~5亿"
        }
      ],
      column: [
        {
          prop: "f1",
          label: "产品简称",
          align: "",
          filter: "",
          width: "170",
          filter: "fund",
          noshowoverflowtooltip: true
        },
        { prop: "f2", label: "投资策略", align: "center", filter: "" },
        { prop: "f3", label: "机构简称", align: "", filter: "", width: "150" },
        { prop: "f4", label: "基金经理", align: "center", filter: "" },
        {
          prop: "f5",
          label: "绩效星级",
          align: "center",
          filter: "star",
          width: "150"
        },
        { prop: "f6", label: "成立日期", align: "center", filter: "" },
        { prop: "f7", label: "净值日期", align: "center", filter: "" },
        { prop: "f8", label: "单位净值", align: "center", filter: "" },
        { prop: "f9", label: "累计净值", align: "center", filter: "" },
        { prop: "f10", label: "复权累计净值", align: "center", filter: "" },
        { prop: "f11", label: "今年以来收益率", align: "center", filter: "" },
        { prop: "f12", label: "成立以来收益率", align: "center", filter: "" },
        { prop: "f13", label: "成立以来最大回撤", align: "center", filter: "" },
        {
          prop: "f14",
          label: "成立以来收益率(年化)",
          align: "center",
          filter: ""
        },
        {
          prop: "f15",
          label: "成立以来波动率(年化)",
          align: "center",
          filter: ""
        },
        {
          prop: "f16",
          label: "成立以来Sharpe比率",
          align: "center",
          filter: ""
        },
        { prop: "f17", label: "管理规模", align: "center", filter: "" }
      ]
    };
  },
  props: {},
  methods: {
    pagination() {},
    jumpPage() {
      this.$router.push({
        path: "/cpxq"
      });
    }
  }
};
</script>

<style lang="scss" scoped>
.color_4f95dd {
  color: #4f95dd;
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
.tabletable {
  .tabletable_top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
  }
}
</style>

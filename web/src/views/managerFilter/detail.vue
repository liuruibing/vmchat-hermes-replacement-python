<template>
  <div class="manager_detail">
    <!-- 经理分析 -->
    <!-- 姓名卡 -->
    <div class="name_car">
      <div class="manager_name">赵媛媛</div>
      <el-row>
        <el-col :span="6">
          <p class="car_item">职位：投资总监/副总裁</p>
          <p class="car_item">管理产品数（不含已终止）：7</p>
        </el-col>
        <el-col :span="6">
          <p class="car_item">学历：研究生硕士</p>
          <p class="car_item">所在机构：建泓时代</p>
        </el-col>
        <el-col :span="6">
          <p class="car_item">从业年限：16年</p>
          <p class="car_item">当前公司任职年数：1年</p>
        </el-col>
        <el-col :span="6">
          <p class="car_item">职业背景：--</p>
          <p class="car_item">擅长策略：股票多头</p>
        </el-col>
      </el-row>
    </div>
    <!-- 个人概况 -->
    <div class="conent_item">
      <div class="manager_detail_title">
        <span class="manager_detail_title_left">个人概况</span>
        <span class="manager_detail_title_right">统计日期：2022-09-01</span>
      </div>
      <div class="gerengaikuang">
        西南财投大学经济学硕士，209年新财宿最佳分析师，第13届中国"金基金”偏股混合型基金奖。
        西南此投大学经济学本科，硕士:CA持证人。 央视2给节目重要燕宾并出席央视年度经济论坛。
        207-2012年，历任国泰君安/国泰基金宏观策略/财通基金研究员/机械行业分析师。
        2012-2014年，财通基金，保本基金/财通可持续发展基金基金经理。2014-2017年，华商基金，华商万众创新基金/华商盘安基金基金经理。
        5年公开产品累计投资收益111.5%，较业绩基准高出75.7%;公劳期间混合型排名前14%。公私募期间前11%
      </div>
    </div>
    <!-- 旗下产品 -->
    <div class="conent_item">
      <div class="manager_detail_title mb10">
        <span class="manager_detail_title_left">旗下产品</span>
        <span class="manager_detail_title_right">
          <span
            >产品状态：<el-select v-model="form1.status" placeholder="请选择" size="small">
              <el-option value="全部" label="全部"></el-option> </el-select
          ></span>
          <span
            >最新净值日期：<el-select v-model="form1.newdate" placeholder="请选择" size="small">
              <el-option value="最新净值日期" label="最新净值日期"></el-option> </el-select
          ></span>
          <span>统计日期：2022-09-01</span>
        </span>
      </div>
      <el-table :data="tableData1" stripe="" style="width: 100%" id="">
        <el-table-column label="对比" align="center" width="55">
          <template slot-scope="scope">
            <el-checkbox v-model="scope.ff"></el-checkbox>
          </template>
        </el-table-column>
        <el-table-column label="序号" type="index" align="center" width="50"> </el-table-column>
        <el-table-column
          v-for="item in column1"
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
            <span v-if="item.filter == 'moneyYuan'">
              {{ scope.row[item.prop] | moneyYuan }}
            </span>
            <span
              v-else-if="item.filter == 'numberToFixedStr2'"
              :class="scope.row[item.prop] ? (scope.row[item.prop] > 0 ? 'color_F56C6C' : 'color_67C23A') : ''"
            >
              {{ scope.row[item.prop] | numberToFixedStr(2, 100, "%") }}
            </span>
            <span v-else-if="item.filter == 'fund'" class="color_4f95dd" @click="jumpPage()">
              {{ scope.row[item.prop] || noDataFilter }}
            </span>
            <span v-else-if="item.filter == 'fund2'" class="color_4f95dd">
              {{ scope.row[item.prop] || noDataFilter }}
            </span>
            <span v-else>{{ scope.row[item.prop] | noDataFilter }}</span>
          </template>
        </el-table-column>
      </el-table>
      <div style="height: 50px">
        <Pagination :total="total1" :limit="form1.pageSize" :page="form1.pageNum" @pagination="pagination1" />
      </div>
    </div>
    <!-- 代表产品 -->
    <div class="content_item">
      <div class="manager_detail_title mb10">
        <span class="manager_detail_title_left">代表产品</span>
        <span class="manager_detail_title_right">统计日期：2022-09-01</span>
      </div>
      <!-- 产品基本信息 -->
      <div class="manager_detail_title_2 mb10">
        <span class="manager_detail_title_left">产品基本信息</span>
      </div>
      <el-table :data="tableData2" stripe="" style="width: 100%" id="">
        <el-table-column
          v-for="item in column2"
          :key="item.prop"
          :prop="item.prop"
          :label="item.label"
          :min-width="item.minWidth || '100'"
          :width="item.width"
          header-align="center"
          :align="item.align"
        >
          <template slot-scope="scope">
            <span v-if="item.filter == 'moneyYuan'">
              {{ scope.row[item.prop] | moneyYuan }}
            </span>
            <span
              v-else-if="item.filter == 'numberToFixedStr2'"
              :class="scope.row[item.prop] ? (scope.row[item.prop] > 0 ? 'color_F56C6C' : 'color_67C23A') : ''"
            >
              {{ scope.row[item.prop] | numberToFixedStr(2, 100, "%") }}
            </span>
            <span v-else-if="item.filter == 'fund'" class="color_4f95dd" @click="jumpPage()">
              {{ scope.row[item.prop] || noDataFilter }}
            </span>
            <span v-else-if="item.filter == 'fund2'" class="color_4f95dd">
              {{ scope.row[item.prop] || noDataFilter }}
            </span>
            <span v-else>{{ scope.row[item.prop] | noDataFilter }}</span>
          </template>
        </el-table-column>
      </el-table>

      <!-- 复权累计净值 -->
      <div class="manager_detail_title_2 mb10">
        <span class="manager_detail_title_left">复权累计净值</span>
        <span class="manager_detail_title_right">
          <span
            ><el-select v-model="form4.f1" placeholder="请选择比较基准" size="small">
              <el-option v-for="item in []" :key="item.value" :label="item.label" :value="item.value">
              </el-option></el-select
          ></span>
        </span>
      </div>
      <div class="chart_box">
        <myChart id="fqljjzChart" ref="fqljjzChart" :options="chartOption1" resize-dom="cmbfof" class="fqljjzChart" />
      </div>

      <!-- 历史业绩 -->
      <div class="manager_detail_title_2 mb10">
        <span class="manager_detail_title_left">历史业绩</span>
        <span class="manager_detail_title_right">
          <span
            ><el-select v-model="form5.f1" placeholder="" size="small">
              <el-option label="股票多头" value="股票多头"></el-option>
              <el-option label="私募基金全市" value="私募基金全市"></el-option> </el-select
          ></span>
        </span>
      </div>
      <el-row :gutter="40">
        <el-col :span="12">
          <div class="chart_box">
            <myChart id="lsyjChart" ref="lsyjChart" :options="chartOption2" resize-dom="cmbfof" class="lsyjChart" />
          </div>
        </el-col>
        <el-col :span="12">
          <el-table :data="tableData5" stripe="" style="width: 100%" id="">
            <el-table-column
              v-for="item in column5"
              :key="item.prop"
              :prop="item.prop"
              :label="item.label"
              :min-width="item.minWidth || '100'"
              :width="item.width"
              header-align="center"
              :align="item.align"
            >
              <template slot-scope="scope">
                <span
                  v-if="item.filter == 'numberToFixedStr2'"
                  :class="scope.row[item.prop] ? (scope.row[item.prop] > 0 ? 'color_F56C6C' : 'color_67C23A') : ''"
                >
                  {{ scope.row[item.prop] | numberToFixedStr(2, 100, "%") }}
                </span>
                <span v-else>{{ scope.row[item.prop] | noDataFilter }}</span>
              </template>
            </el-table-column>
          </el-table>
        </el-col>
      </el-row>

      <el-row :gutter="40" class="mt10">
        <!-- 历史投资能力 -->
        <el-col :span="12">
          <div class="manager_detail_title_2 mb10">
            <span class="manager_detail_title_left">历史投资能力</span>
            <span class="manager_detail_title_right">
              <span>统计日期：2022-09</span>
              <span
                ><el-select v-model="form2.f1" placeholder="请选择" size="small">
                  <el-option value="收益能力" label="收益能力"></el-option>
                  <el-option value="风险处理能力" label="风险处理能力"></el-option>
                  <el-option value="回撤控制能力" label="回撤控制能力"></el-option> </el-select
              ></span>
            </span>
          </div>
          <el-table :data="tableData3" stripe="" style="width: 100%" id="">
            <el-table-column
              v-for="item in column3"
              :key="item.prop"
              :prop="item.prop"
              :label="item.label"
              :min-width="item.minWidth || '100'"
              :width="item.width"
              header-align="center"
              :align="item.align"
              :sortable="item.sortable"
            >
              <template slot-scope="scope">
                <span v-if="scope.row[item.prop].indexOf('sfw') != -1">
                  <div class="sfw_box">
                    <p class="sfw_box_item rgb_"></p>
                    <p class="sfw_box_item"></p>
                    <p class="sfw_box_item"></p>
                    <p class="sfw_box_item"></p>
                  </div>
                </span>
                <span v-else>{{ scope.row[item.prop] | noDataFilter }}</span>
              </template>
            </el-table-column>
          </el-table>
          <div class="mt10" style="color: #909399">
            备注：收益能力选取区间收益率进行计算，风险处理能力选取区间夏普比率进行计算，回撤控制能力选取区间最大回撤进行计算。
          </div>
        </el-col>
        <!-- 历史排名 -->
        <el-col :span="12">
          <div class="manager_detail_title_2 mb10">
            <span class="manager_detail_title_left">历史排名</span>
            <span class="manager_detail_title_right">
              <span
                ><el-select v-model="form3.f1" placeholder="请选择" size="small">
                  <el-option value="股票多头" label="股票多头"></el-option> </el-select
              ></span>
            </span>
          </div>
          <el-table :data="tableData4" stripe="" style="width: 100%" id="">
            <el-table-column
              v-for="item in column4"
              :key="item.prop"
              :prop="item.prop"
              :label="item.label"
              :min-width="item.minWidth || '100'"
              :width="item.width"
              header-align="center"
              :align="item.align"
            >
              <template slot-scope="scope">
                <span>{{ scope.row[item.prop] | noDataFilter }}</span>
              </template>
            </el-table-column>
          </el-table>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import myChart from "@/components/Echarts";
import Pagination from "@/components/Pagination";
export default {
  components: { Pagination, myChart },
  data() {
    return {
      form1: {
        status: "全部",
        newdate: "最新净值日期",
        pageSize: 20,
        pageNum: 1
      },
      form2: {
        f1: "收益能力"
      },
      form3: {
        f1: "股票多头"
      },
      form4: {
        f1: ""
      },
      form5: {
        f1: "股票多头"
      },
      total1: 0,
      tableData1: [
        {
          f1: "建泓行业优选二号",
          f2: "建泓时代",
          f3: "股票多头",
          f4: "2022-02-03",
          f5: "2022-08-06",
          f6: 5.9447,
          f7: 5.9447,
          f8: 0.9608,
          f9: 3.027,
          f10: 4.9447,
          f11: 4.9447,
          f12: "",
          f13: "运作中"
        },
        {
          f1: "建泓行业优选二号A期",
          f2: "建泓时代",
          f3: "股票多头",
          f4: "2022-02-03",
          f5: "2022-08-06",
          f6: 1.4812,
          f7: 5.8121,
          f8: "",
          f9: 0.9577,
          f10: 2.9388,
          f11: 4.8115,
          f12: 4.8121,
          f13: "存续中"
        },
        {
          f1: "建泓时代朝阳传承",
          f2: "建泓时代",
          f3: "股票多头",
          f4: "2022-02-03",
          f5: "2022-08-06",
          f6: 8.611,
          f7: 8.611,
          f8: 7.61109,
          f9: 0.8756,
          f10: 2.9899,
          f11: 7.6395,
          f12: 7.61109,
          f13: "存赎中"
        },
        {
          f1: "建泓时代朝阳传承二号",
          f2: "建泓时代",
          f3: "股票多头",
          f4: "2022-02-03",
          f5: "2022-08-06",
          f6: 6.6813,
          f7: 6.6813,
          f8: 0.8462,
          f9: 2.5202,
          f10: 5.6813,
          f11: 5.6813,
          f12: "",
          f13: "存续中"
        },
        {
          f1: "建泓时代朝阳传承二号A期",
          f2: "建泓时代",
          f3: "股票多头",
          f4: "2022-02-03",
          f5: "2022-08-06",
          f6: 1.8958,
          f7: 6.4288,
          f8: 0.8106,
          f9: 2.3859,
          f10: 5.4282,
          f11: 5.4288,
          f12: "",
          f13: "存续中"
        },
        {
          f1: "建泓盈富四号",
          f2: "建泓时代",
          f3: "股票多头",
          f4: "2022-02-03",
          f5: "2022-08-06",
          f6: 13.872,
          f7: 13.872,
          f8: 2.45429,
          f9: 0.0122,
          f10: 0.46339,
          f11: 0.6919,
          f12: 12.872,
          f13: ""
        }
      ],
      column1: [
        { prop: "f1", label: "产品名称", align: "", filter: "fund" },
        { prop: "f2", label: "投资顾问", align: "center", filter: "fund2" },
        { prop: "f3", label: "投资策略", align: "center", filter: "" },
        { prop: "f4", label: "成立日期", align: "center", filter: "" },
        { prop: "f5", label: "净值日期", align: "center", filter: "" },
        { prop: "f6", label: "单位净值", align: "center", filter: "" },
        { prop: "f7", label: "复权单位净值", align: "center", filter: "" },
        { prop: "f8", label: "今年以来收益率", align: "center", filter: "numberToFixedStr2" },
        { prop: "f9", label: "近一月收益率", align: "center", filter: "numberToFixedStr2" },
        { prop: "f10", label: "近三月收益率", align: "center", filter: "numberToFixedStr2" },
        { prop: "f11", label: "近六月收益率", align: "center", filter: "numberToFixedStr2" },
        { prop: "f12", label: "成立以来收益率", align: "center", filter: "numberToFixedStr2" },
        { prop: "f13", label: "产品状态", align: "center", filter: "" }
      ],
      tableData2: [
        {
          f1: "建泓盈富四号",
          f2: "建泓时代",
          f3: "2020-09-23",
          f4: "13.8720",
          f5: "13.8720",
          f6: "1287.20%",
          f7: "29.88%"
        }
      ],
      column2: [
        { prop: "f1", label: "产品名称", align: "center", filter: "fund" },
        { prop: "f2", label: "投资顾问", align: "center", filter: "fund2" },
        { prop: "f3", label: "成立日期", align: "center", filter: "" },
        { prop: "f4", label: "单位净值", align: "center", filter: "" },
        { prop: "f5", label: "复权单位净值", align: "center", filter: "" },
        { prop: "f6", label: "今年以来收益率", align: "center", filter: "" },
        { prop: "f7", label: "成立以来最大回撤", align: "center", filter: "" }
      ],
      tableData3: [
        {
          f1: "收益率",
          f2: "1287.2%",
          f3: "245.42%",
          f4: "1.22%",
          f5: "46.33%",
          f6: "69.19%",
          f7: "469.22%",
          f8: "1287.2%",
          f9: "--"
        },
        {
          f1: "同策略指数",
          f2: "4.42%",
          f3: "-8.12%",
          f4: "-0.77%",
          f5: "5.6%",
          f6: "-2.75%",
          f7: "-5.18%",
          f8: "3.939%",
          f9: "25.65%"
        },
        {
          f1: "同策略排名",
          f2: "11/22514",
          f3: "4/18490",
          f4: "3929/20658",
          f5: "184/19837",
          f6: "56/18898",
          f7: "4/16036",
          f8: "2/10024",
          f9: "--"
        },
        {
          f1: "四分位",
          f2: "sfw_1",
          f3: "sfw_1",
          f4: "sfw_1",
          f5: "sfw_1",
          f6: "sfw_1",
          f7: "sfw_1",
          f8: "sfw_1",
          f9: "sfw_1"
        }
      ],
      column3: [
        { prop: "f1", label: "", align: "", filter: "" },
        { prop: "f2", label: "成立以来", align: "center", filter: "" },
        { prop: "f3", label: "今年以来", align: "center", filter: "" },
        { prop: "f4", label: "近一月", align: "center", filter: "" },
        { prop: "f5", label: "近三月", align: "center", filter: "" },
        { prop: "f6", label: "近六月", align: "center", filter: "" },
        { prop: "f7", label: "近一年", align: "center", filter: "" },
        { prop: "f8", label: "近两年", align: "center", filter: "" },
        { prop: "f9", label: "近三年", align: "center", filter: "" }
      ],
      tableData4: [
        {
          f1: "2022",
          f2: "245.42%",
          f3: "4/18409",
          f4: "12.13%",
          f5: "4050/18409",
          f6: "3.69",
          f7: "376/18368"
        },
        {
          f1: "2021",
          f2: "245.42%",
          f3: "4/18409",
          f4: "12.13%",
          f5: "4050/18409",
          f6: "3.69",
          f7: "376/18368"
        }
      ],
      column4: [
        { prop: "f1", label: "", align: "", filter: "" },
        { prop: "f2", label: "收益率", align: "center", filter: "" },
        { prop: "f3", label: "排名", align: "center", filter: "" },
        { prop: "f4", label: "最大回撤", align: "center", filter: "" },
        { prop: "f5", label: "排名", align: "center", filter: "" },
        { prop: "f6", label: "夏普比率", align: "center", filter: "" },
        { prop: "f7", label: "排名", align: "center", filter: "" }
      ],
      tableData5: [
        { f1: "成立以来", f2: "12.8720", f3: 0.04429, f4: -0.11719 },
        { f1: "今年以来", f2: 2.4542, f3: -0.08129, f4: -0.16869 },
        { f1: "近—月", f2: 0.01229, f3: -0.0077, f4: -0.0326 },
        { f1: "近三月", f2: 0.4633, f3: 0.056, f4: 0.0287 },
        { f1: "近六月", f2: 0.6919, f3: -0.0275, f4: -0.1019 },
        { f1: "近一年", f2: 4.69229, f3: -0.0518, f4: -0.1445 },
        { f1: "近两年", f2: "12.8720", f3: 0.03939, f4: -0.1272 },
        { f1: "近三年", f2: "", f3: 0.2565, f4: 0.0907 }
      ],
      column5: [
        { prop: "f1", label: "", align: "", filter: "" },
        { prop: "f2", label: "建泓盈富四号", align: "center", filter: "numberToFixedStr2" },
        { prop: "f3", label: "股票多头", align: "center", filter: "numberToFixedStr2" },
        { prop: "f4", label: "私募全市场", align: "center", filter: "numberToFixedStr2" }
      ],
      chartOption1: {},
      chartOption2: {}
    };
  },
  mounted() {
    this.init();
  },
  methods: {
    init() {
      this.chart1Init();
      this.chart2Init();
    },
    chart1Init() {
      let base = +new Date(2020, 7, 1);
      let oneDay = 24 * 3600 * 1000;
      let date = [];
      let data1 = [Math.random() * 300];
      let data2 = [Math.random() * 300];
      let data3 = [Math.random() * 300];
      let data4 = [Math.random() * 300];
      let data5 = [Math.random() * 300];
      let data6 = [Math.random() * 300];
      let data7 = [Math.random() * 300];
      for (let i = 1; i < 700; i++) {
        let now = new Date((base += oneDay));
        date.push([now.getFullYear(), now.getMonth() + 1, now.getDate()].join("/"));
        data1.push(Math.round((Math.random() - 0.5) * 20 + data1[i - 1]));
        data2.push(Math.round((Math.random() - 0.5) * 20 + data2[i - 1]));
        data3.push(Math.round((Math.random() - 0.5) * 20 + data3[i - 1]));
        data4.push(Math.round((Math.random() - 0.5) * 20 + data4[i - 1]));
        data5.push(Math.round((Math.random() - 0.5) * 20 + data5[i - 1]));
        data6.push(Math.round((Math.random() - 0.5) * 20 + data6[i - 1]));
        data7.push(Math.round((Math.random() - 0.5) * 20 + data7[i - 1]));
      }
      this.chartOption1 = {
        // title: {
        //   text: "Stacked Line"
        // },
        tooltip: {
          trigger: "axis"
        },
        color: ["#e9aaa1", "#f1d576", "#537dfb", "#e1d9be", "#dbc0c0", "#b1e7d8", "#aaaaaa"],
        legend: {
          top: "bottom",
          data: [
            { name: "建泓盈富四号" },
            { name: "预警提示", icon: "triangle" },
            { name: "分红/拆分", icon: "roundRect" },
            { name: "沪深300" },
            { name: "私募全市场" },
            { name: "中证全指" },
            { name: "股票多头" }
          ],
          itemWidth: 18,
          itemHeight: 12,
          textStyle: { color: "#000", fontSize: 14 }
        },
        grid: {
          left: "3%",
          right: "3%",
          bottom: "12%",
          top: "10%",
          containLabel: true
        },
        xAxis: {
          type: "category",
          boundaryGap: false,
          data: date
          // data: ["18.09", "18.11", "19.01", "19.03", "19.05", "19.07", "19.09"]
        },
        yAxis: {
          type: "value",
          name: "复权累计净值",
          axisLabel: {}
        },
        series: [
          {
            name: "建泓盈富四号",
            type: "line",
            symbol: "none",
            data: data1
          },
          {
            name: "预警提示",
            type: "line",
            symbol: "none",
            data: data2
          },
          {
            name: "分红/拆分",
            type: "line",
            symbol: "none",
            data: data3
          },
          {
            name: "沪深300",
            type: "line",
            symbol: "none",
            data: data4
          },
          {
            name: "私募全市场",
            type: "line",
            symbol: "none",
            data: data5
          },
          {
            name: "中证全指",
            type: "line",
            symbol: "none",
            data: data6
          },
          {
            name: "股票多头",
            type: "line",
            symbol: "none",
            data: data7
          }
        ]
      };
    },
    chart2Init() {
      this.chartOption2 = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "shadow"
          }
        },
        grid: {
          left: "3%",
          right: "3%",
          bottom: "12%",
          top: "10%",
          containLabel: true
        },
        legend: {
          top: "bottom",
          data: ["建泓盈富四号", "股票多头", "沪深300"]
        },
        color: ["#e06252", "#946fe4", "#5fa4e8"],
        toolbox: {
          show: true,
          orient: "vertical",
          left: "right",
          top: "center"
          // feature: {
          //   mark: { show: true },
          //   dataView: { show: true, readOnly: false },
          //   magicType: { show: true, type: ['line', 'bar', 'stack'] },
          //   restore: { show: true },
          //   saveAsImage: { show: true }
          // }
        },
        xAxis: [
          {
            type: "category",
            axisTick: { show: false },
            data: ["成立以来", "今年以来", "近一月", "近三月", "近六月", "近一年", "近两年", "近三年"]
          }
        ],
        yAxis: [
          {
            type: "value",
            name: "收益率（%）"
          }
        ],
        series: [
          {
            name: "建泓盈富四号",
            type: "bar",
            barGap: 0,
            emphasis: {
              focus: "series"
            },
            data: [1300, 280, 10, 40, 50, 460, 1310, 100]
          },
          {
            name: "股票多头",
            type: "bar",
            emphasis: {
              focus: "series"
            },
            data: [10, -20, 0, 20, -10, -10, -10, 30]
          },
          {
            name: "沪深300",
            type: "bar",
            emphasis: {
              focus: "series"
            },
            data: [-20, -30, 0, 10, -10, -10, -10, 10]
          }
        ]
      };
    },
    pagination1() {},
    jumpPage(){
      this.$router.push({path:"/cpxq"})
    }
  }
};
</script>

<style lang="scss" scoped>
.manager_detail {
  overflow-x: hidden;
  .name_car {
    border: 1px solid #ccc;
    padding: 14px;
    .manager_name {
      font-size: 20px;
      font-weight: 600;
      border-bottom: 1px solid #ccc;
      padding-bottom: 4px;
    }
    .car_item {
      padding: 5px 0;
    }
  }
}
.manager_detail_title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 4px;
  border-bottom: 2px solid #409eff;
  .manager_detail_title_left {
    font-size: 16px;
    font-weight: 600;
  }
}
.manager_detail_title_2 {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 4px;
  border-bottom: 1px solid #409eff;
  .manager_detail_title_left {
    font-size: 16px;
    font-weight: 600;
  }
}
.gerengaikuang {
  color: #333;
  padding: 4px;
}
.conent_item {
  margin-bottom: 30px;
}
.chart_box {
  padding: 10px;
}
.fqljjzChart {
  width: 100%;
  height: 400px;
}
.lsyjChart {
  width: 100%;
  height: 300px;
}
.sfw_box {
  width: 70px;
  display: inline-block;
  border: 1px solid #ccc;
  .sfw_box_item {
    height: 20px;
    border-bottom: 1px solid #ccc;
    background: #fff;
  }
  .rgb_ {
    background: rgb(179, 216, 255) !important;
  }
}

.mt10 {
  margin-top: 10px;
}
.mb10 {
  margin-bottom: 10px;
}
.color_F56C6C {
  color: #f56c6c;
}
.color_67C23A {
  color: #67c23a;
}
.color_4f95dd {
  color: #4f95dd;
  cursor: pointer;
}
</style>

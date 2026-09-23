<template>
  <div class="chart_view">
    <!-- 图表视图 -->
    <el-form
      :inline="true"
      class="formInline"
      ref="formInline"
      :model="formInline"
      :rules="formInlineRules"
    >
      <el-row>
        <el-col :span="16">
          <!-- 查询 -->
          <div class="grid-content bg-purple">
            <el-form-item label="文件日期" prop="fileDate">
              <el-date-picker
                size="small"
                :clearable="false"
                v-model="formInline.fileDate"
                type="date"
                value-format="yyyy-MM-dd"
                placeholder="选择日期"
              >
              </el-date-picker>
            </el-form-item>

            <el-form-item label="基金服务机构" prop="agencyCode">
              <el-select
                v-model="formInline.agencyCode"
                clearable
                size="small"
                placeholder="请选择"
              >
                <el-option
                  v-for="(group, index) in agencyCodeArr"
                  :value="group.agencyCode"
                  :key="index"
                  :label="group.agencyName"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="8">
          <el-form-item class="search_button_com">
            <el-button
              type="primary"
              class="mb5"
              size="small"
              @click="getChartDataBefore(true)"
              >查询</el-button
            >
            <el-button
              type="primary"
              plain
              class="mb5"
              size="small"
              @click="scheduleList"
              >查看调度列表</el-button
            >
            <el-button
              type="primary"
              icon="el-icon-s-data"
              plain
              class="mb5"
              size="small"
              @click="switchView"
              >查看明细</el-button
            >
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <div
      id="main_demo"
      style="width: 900px; height: 500px"
      v-loading="echarts_loading"
    ></div>
    <el-dialog
      title="提示"
      :visible.sync="dialogVisible"
      width="80% !important"
      @closed="closed"
      center
    >
      <controlList v-if="ddControlList_show"></controlList>
    </el-dialog>
  </div>
</template>

<script>
import controlList from "./controlList.vue";
import pageApi from "@/api/etl/fileCollection";
import * as echarts from "echarts";
export default {
  components: {
    controlList,
  },
  data() {
    return {
      agencyCodeArr: [
        // {agencyCode:"GTJA",agencyName:"国泰君安"},
        // {agencyCode:"ALL",agencyName:"资讯"},
      ],
      formInline: {
        fileDate: this.getTime(),
        agencyCode: "",
      },
      formInlineRules: {
        fileDate: {
          required: true,
          message: "请选择文件日期",
          trigger: "change",
        },
      },
      echarts_loading: false,
      dialogVisible: false,
      ddControlList_show: false,
      aaa: [
        {
          AGENCYCODE: "ALL",
          ERRORBIT: 100, //--执行出错任务数量占比
          ALLCOUNT: 2,
          AGENCYNAME: "资讯", //--图表项名称
          RUNNINGBIT: 0, //--正在执行任务数量占比
          UNDOBIT: 0, //--未执行任务数量占比
          SUCCESSBIT: 0, //—成功执行任务数量占比
        },
        {
          AGENCYCODE: "GTJA",
          ERRORBIT: 30, //--执行出错任务数量占比
          ALLCOUNT: 2,
          AGENCYNAME: "国泰君安", //--图表项名称
          RUNNINGBIT: 10, //--正在执行任务数量占比
          UNDOBIT: 20, //--未执行任务数量占比
          SUCCESSBIT: 40, //—成功执行任务数量占比
        },
      ],
    };
  },
  mounted() {
    this.$bus.$on('transition2',(data)=>{
      // console.log('图表',data);
      this.formInline.fileDate = data+'' || ''
      this.getChartData();
    })
    this.getAgencyList();
    // this.onQuery();
    this.getChartData();
    console.log('mounted');
  },
  methods: {
    switchView() {
      this.$refs["formInline"].validate((valid) => {
        if (valid) {
          this.$emit("transition");
          this.$bus.$emit('transition1',this.formInline.fileDate)
        } else {
          this.$message.closeAll();
          this.$message({
            type:"warning",
            message:"请选择文件日期"
          })
          return false;
        }
      });

    },
    getTime() {
      var date = new Date();
      var y = date.getFullYear();
      var m =
        date.getMonth() + 1 < 10
          ? "0" + (date.getMonth() + 1)
          : date.getMonth() + 1;
      var d = date.getDate() < 10 ? "0" + date.getDate() : date.getDate();
      return y + "-" + m + "-" + d;
    },
    getChartDataBefore(){
      this.$refs["formInline"].validate((valid) => {
        if (valid) {
          this.getChartData();
        } else {
          return false;
        }
      });
    },
    getChartData() {
      this.echarts_loading = true;
      let params = JSON.parse(JSON.stringify(this.formInline));
      params = this.$fun.parameterSrc(params)
      pageApi.countData(params).then((res) => {
        if (res.data.status === 200) {
          let data = res.data.data;
          this.getPie2(data);
        }
      });
    },
    getPie2(data) {
      let arr = data;
      // ALLCOUNT -- 总数
      // 绘制图表
      let myChart = echarts.init(document.getElementById("main_demo"));
      // 指定图表的配置项和数据
      let option = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            // Use axis to trigger tooltip
            type: "shadow", // 'shadow' as default; can also be 'line' or 'shadow'
          },
          formatter: (params) => {
            let tip = params[0].name + "<br>";
            // let tip = '';
            for (let i = 0; i < params.length; i++) {
              tip += params[i].seriesName + ": " + params[i].value + "%<br>";
            }
            return tip;
          },
        },
        legend: {
          data: ["成功", "失败", "正在执行", "未执行"],
        },
        color: ["#67C23A", "#F56C6C", "#409EFF", "#909399"],
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true,
        },
        xAxis: {
          type: "category",
          data: arr.map((item) => item.AGENCYNAME),
          // data: arr.map(item=>item.AGENCYNAME+item.ALLCOUNT),
        },
        yAxis: {
          type: "value",
          axisLabel: {
            formatter: "{value}%",
          },
        },
        series: [
          {
            name: "成功",
            type: "bar",
            stack: "total",
            label: {
              show: true,
              formatter: "{c}%",
            },
            emphasis: {
              focus: "series",
            },
            data: arr.map((item) => item.SUCCESSBIT),
          },
          {
            name: "失败",
            type: "bar",
            stack: "total",
            label: {
              show: true,
              formatter: "{c}%",
            },
            emphasis: {
              focus: "series",
            },
            data: arr.map((item) => item.ERRORBIT),
          },
          {
            name: "正在执行",
            type: "bar",
            stack: "total",
            label: {
              show: true,
              formatter: "{c}%",
            },
            emphasis: {
              focus: "series",
            },
            data: arr.map((item) => item.RUNNINGBIT),
          },
          {
            name: "未执行",
            type: "bar",
            stack: "total",
            label: {
              show: true,
              formatter: "{c}%",
            },
            emphasis: {
              focus: "series",
            },
            data: arr.map((item) => item.UNDOBIT),
          },
        ],
      };
      // 使用刚指定的配置项和数据显示图表。
      myChart.setOption(option);
      this.echarts_loading = false;
    },
    // 获取基金服务机构
    getAgencyList() {
      pageApi
        .getAgencyList()
        .then((res) => {
          if (res.data.status == 0) {
            this.agencyCodeArr = res.data.data;
          } else {
            this.agencyCodeArr = [];
          }
        })
        .catch(() => {});
    },
    onQuery() {
      // let params = {fileDate:this.getTime()}
      this.echarts_loading = true;
      let params = JSON.parse(JSON.stringify(this.formInline));
      params = this.$fun.parameterSrc(params)
      pageApi.getFileExtract(params).then((res) => {
        if (res.data.status === 0) {
          let EchartsList = [...res.data.data.list, ...this.aaa];
          let CodeArr = this.agencyCodeArr.map((item) => {
            return item.agencyCode;
          });
          let arr = [];
          CodeArr.forEach((Codeitem) => {
            let list = EchartsList.filter((item) => {
              return item.agencyCode == Codeitem;
            });
            let obj = {};
            obj["执行成功"] = list.filter((item) => {
              return item.execStatusName == "执行成功";
            });
            obj["执行失败"] = list.filter((item) => {
              return item.execStatusName == "执行失败";
            });
            obj["正在执行"] = list.filter((item) => {
              return item.execStatusName == "正在执行";
            });
            obj["未执行"] = list.filter((item) => {
              return item.execStatusName == "未执行";
            });
            arr.push(obj);
          });
          // console.log(arr);
          this.$nextTick(() => {
            this.getPie(CodeArr, arr);
          });
        } else {
        }
      });
    },
    getPie(CodeArr, arr) {
      // 绘制图表
      let myChart = echarts.init(document.getElementById("main_demo"));
      // 指定图表的配置项和数据
      let option = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            // Use axis to trigger tooltip
            type: "shadow", // 'shadow' as default; can also be 'line' or 'shadow'
          },
          formatter:
            "{b}<br/>{a0}:{c0}% <br/> {a1}:{c1}% <br/> {a2}:{c2}%<br/> {a3}:{c3}%",
        },
        legend: {
          data: ["成功", "失败", "正在执行", "未执行"],
        },
        color: ["#67C23A", "#F56C6C", "#409EFF", "#909399"],
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true,
        },
        xAxis: {
          type: "category",
          data: this.agencyCodeArr.map((item) => item.agencyName),
        },
        yAxis: {
          type: "value",
        },
        series: [
          {
            name: "成功",
            type: "bar",
            stack: "total",
            label: {
              show: true,
            },
            emphasis: {
              focus: "series",
            },
            data: arr.map((item) => item["执行成功"].length),
          },
          {
            name: "失败",
            type: "bar",
            stack: "total",
            label: {
              show: true,
            },
            emphasis: {
              focus: "series",
            },
            data: arr.map((item) => item["执行失败"].length),
          },
          {
            name: "正在执行",
            type: "bar",
            stack: "total",
            label: {
              show: true,
            },
            emphasis: {
              focus: "series",
            },
            data: arr.map((item) => item["正在执行"].length),
          },
          {
            name: "未执行",
            type: "bar",
            stack: "total",
            label: {
              show: true,
            },
            emphasis: {
              focus: "series",
            },
            data: arr.map((item) => item["未执行"].length),
          },
        ],
      };
      // 使用刚指定的配置项和数据显示图表。
      myChart.setOption(option);
      this.echarts_loading = false;
    },
    scheduleList() {
      this.dialogVisible = true;
      this.ddControlList_show = true;
    },
    closed() {
      this.ddControlList_show = false;
    },
  },
};
</script>

<style>
</style>

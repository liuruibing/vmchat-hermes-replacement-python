<template>
  <!-- 首页第四行 -->
  <div id="lineFourth">
    <el-row :gutter="20">
      <el-col :span="8">
        <div class="box">
          <div class="title-content">
            <span class="title">最新研报</span>
            <el-link
              type="primary"
              class="more"
              :underline="false"
              style="font-size: 14px;color:#2672bc"
              >更多</el-link
            >
          </div>
          <div class="main-content">
            <div
              class="item-1"
              v-for="(ele, index) in dataSourceLeft"
              :key="index"
              :style="ele.noMargin ? 'margin-top: 10px' : ''"
            >
              <div class="main-left">
                <img :src="ele.imgUrl" />
              </div>
              <div class="main-right">
                <div class="main-right-title">{{ ele.title }}</div>
                <div class="main-right-date">{{ ele.date }}</div>
                <p class="main-right-detail">{{ ele.detail }}</p>
              </div>
            </div>
          </div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="box">
          <div class="title-content">
            <span class="title">我的待办</span>
            <span class="title-link">
              <el-link
                type="warning"
                class="more"
                :underline="false"
                style="font-size: 14px;color:#c8993d"
                >待办事项 |</el-link
              >
              <el-link
                type="warning"
                class="more"
                :underline="false"
                style="font-size: 14px;color:#c8993d"
                >综合事项 |</el-link
              >
              <el-link
                type="warning"
                class="more"
                :underline="false"
                style="font-size: 14px;color:#c8993d"
                >其他事项</el-link
              >
            </span>
            <el-link
              type="primary"
              class="more"
              :underline="false"
              style="font-size: 14px;color:#2672bc"
              >更多</el-link
            >
          </div>
          <div class="main-content">
            <div
              class="item-2"
              v-for="(ele, index) in dataSourceMid"
              :key="index"
              :style="ele.noMargin ? 'margin-top: 37px' : ''"
            >
              <div class="text">
                <div>{{ ele.account }}</div>
                <div>
                  <span>{{ ele.name }}</span>
                  <span style="padding: 0 30px">{{ ele.orz }}</span>
                  <span>{{ ele.date }}</span>
                </div>
              </div>
              <div class="link">
                <i class="el-icon-arrow-right"></i>
              </div>
              <hr
                width="99%"
                size="1"
                color="#efefef"
                v-if="index !== dataSourceMid.length - 1"
              />
            </div>
          </div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="box">
          <div class="title-content">
            <span class="title">情绪指标分析</span>
          </div>
          <div class="main-content" style="overflow: hidden">
            <myChart
              id="qxzbfx"
              ref="qxzbfx"
              resizeDom="cmbfof"
              :options="myChartOptions"
              style="width: 100%; height: 350px"
            />
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import img1 from "./img/img1.png";
import img2 from "./img/img2.png";
import myChart from "@/components/myEcharts";
import chartJson from "./js/chart.json";
var legendData = ["非一字涨停", "涨停", "跌停"];
var serieData = [];
var xAxisData = [];
var metaDate = [[], [], []];

// 生成指定随机数
function random(min, max) {
  return Math.floor(Math.random() * (max - min)) + min;
}
// 生成y轴随机数
chartJson.forEach(function(item) {
  // 取x轴日期
  xAxisData.push(item[0]);
  metaDate[0].push(item[1]);
  metaDate[1].push(random(50, 200));
  metaDate[2].push(random(100, 250));
});
// 组装serie数据
for (var v = 0; v < legendData.length; v++) {
  var serie = {
    name: legendData[v],
    type: "line",
    data: metaDate[v]
  };
  serieData.push(serie);
}
// 线条颜色
var colors = ["#e93f30", "#458bf0", "#faa000"];
export default {
  name: "lineFourth",
  components: { myChart },
  data() {
    return {
      img2,
      dataSourceLeft: [
        {
          imgUrl: img1,
          title: "向前进-神农投资718投资者年会",
          date: "日期：2022-09-10 20：00",
          detail:
            "详细：向前进-神农投资718投资者年会向前进-神农投资718投资者年会向前进-神农投资718投资者年会向前进-神农投资718投资者年会",
          noMargin: false
        },
        {
          imgUrl: img2,
          title: "2022年动荡环境下，赚钱管理人有哪些本事",
          date: "日期：2022-09-12 20：00",
          detail:
            "详细：向前进-神农投资718投资者年会向前进-神农投资718投资者年会向前进-神农投资718投资者年会向前进-神农投资718投资者年会",
          noMargin: true
        }
      ],
      dataSourceMid: [
        {
          account: "账号申请：北京晨光集团责任有限公司",
          name: "申请人姓名：陈启",
          orz: "机构：广发证券",
          date: "申请时间：2022-09-01",
          noMargin: false
        },
        {
          account: "账号申请：北京晨光集团责任有限公司",
          name: "申请人姓名：陈启",
          orz: "机构：广发证券",
          date: "申请时间：2022-09-01",
          noMargin: true
        },
        {
          account: "账号申请：北京晨光集团责任有限公司",
          name: "申请人姓名：陈启",
          orz: "机构：广发证券",
          date: "申请时间：2022-09-01",
          noMargin: true
        },
        {
          account: "账号申请：北京晨光集团责任有限公司",
          name: "申请人姓名：陈启",
          orz: "机构：广发证券",
          date: "申请时间：2022-09-01",
          noMargin: true
        }
      ],
      myChartOptions: {}
    };
  },
  created() {
    this.getOptions();
  },
  methods: {
    getOptions() {
      this.myChartOptions = {
        legend: {
          show: true,
          data: legendData,
          itemWidth: 18,
          itemHeight: 12,
          textStyle: { color: "#000", fontSize: 14 }
        },
        color: colors,
        grid: {
          left: "6%",
          top: "12%",
          bottom: "12%",
          right: "5%"
          // containLabel: true
        },
        tooltip: { trigger: "axis" },
        xAxis: [
          {
            type: "category",
            axisTick: { show: false },
            axisLine: { show: true, lineStyle: { color: "#6173A3" } },
            axisLabel: {
              fontSize: 12
            },
            data: xAxisData
          }
        ],
        yAxis: [
          {
            axisTick: { show: false },
            axisLabel: { textStyle: { color: "#9ea7c4", fontSize: 14 } },
            axisLine: { show: true, lineStyle: { color: "#6173A3" } },
            splitLine: {
              //网格线
              show: true,
              lineStyle: {
                color: ["#b1b1b1"],
                type: "solid"
              }
            }
          }
        ],
        series: serieData
      };
    }
  }
};
</script>

<style lang="scss" scoped>
#lineFourth {
  .box {
    height: 400px;
    .title-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
      position: relative;
      .title-link {
        position: absolute;
        left: 18%;
      }
      .title {
        font-size: 18px;
        // font-weight: bold;
      }
    }
    .main-content {
      height: 350px;
      overflow: auto;
      overflow-y: hidden;
      border: 1px solid #e3e3e3;
      padding: 10px;
      .item-1 {
        display: flex;
        .main-left {
          img {
            width: 262px;
          }
        }
      }
      .item-2 {
        position: relative;
        background-color: #ebeff7;
        line-height: 30px;
        font-size: 14px;
        padding: 10px;
        .link {
          position: absolute;
          right: 5%;
          top: 30%;
          font-size: 16px;
          color: #adaeb0;
          cursor: pointer;
        }
        hr {
          position: absolute;
          bottom: -20px;
          left: 0;
        }
      }
      .main-right {
        margin-left: 10px;
        .main-right-title {
          font-size: 16px;
          color: #2672bc;
          margin-bottom: 10px;
        }
        .main-right-date {
          font-size: 14px;
        }
        .main-right-detail {
          font-size: 14px;
          line-height: 25px;
        }
      }
    }
  }
}
@media all and (max-width: 1400px) {
  #lineFourth {
    .box {
      .main-content {
        .item-1 {
          .main-left {
            img {
              width: 180px;
              height: 200px;
            }
          }
        }
        .item-2 {
          line-height: 20px;
          .link {
            right: 3%;
            top: 40%;
          }
        }
      }
    }
  }
}

// 滚动条样式
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
  background-color: #f5f5f5;
}

::-webkit-scrollbar-track {
  -webkit-box-shadow: inset 0 0 6px rgba(153, 151, 151, 0.3);
  border-radius: 10px;
  background-color: #f5f5f5;
}

::-webkit-scrollbar-thumb {
  border-radius: 10px;
  -webkit-box-shadow: inset 0 0 6px rgba(153, 150, 150, 0.3);
  background-color: #ddd;
}
</style>

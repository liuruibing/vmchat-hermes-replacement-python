<template>
  <el-row :gutter="20">
<!--    <el-col :span="8">-->
<!--      <box-template>-->
<!--        <template slot="title">-->
<!--          <el-row style="margin: 16px 0px;">-->
<!--            <el-col :span="22">-->
<!--              <span class="dashboard-title">推荐产品</span>-->
<!--            </el-col>-->
<!--            <el-col :span="2">-->
<!--              <div class="search_button_com">-->
<!--                <span style="font-size: 14px">-->
<!--                  <el-link :underline="false" type="primary" @click=""-->
<!--                    ><span class="elLink">更多</span></el-link-->
<!--                  >-->
<!--                </span>-->
<!--              </div>-->
<!--            </el-col>-->
<!--          </el-row>-->
<!--        </template>-->
<!--        <template slot="content">-->
<!--          <div style="height: 300px;overflow: hidden;">-->
<!--            <el-table-->
<!--              :data="tableData"-->
<!--              align="center"-->
<!--              border-->
<!--              max-height="250px"-->
<!--            >-->
<!--              <el-table-column-->
<!--                header-align="center"-->
<!--                label="产品代码"-->
<!--                prop="fundCode"-->
<!--                show-overflow-tooltip-->
<!--              >-->
<!--                <template slot-scope="scope">-->
<!--                  <el-link :underline="false" type="primary" @click="more"-->
<!--                    ><span class="elLink" style="font-size: 14px">-->
<!--                      {{ scope.row.fundCode | noDataFilter }}</span-->
<!--                    ></el-link-->
<!--                  >-->
<!--                </template>-->
<!--              </el-table-column>-->
<!--              <el-table-column-->
<!--                align="left"-->
<!--                header-align="center"-->
<!--                label="产品名称"-->
<!--                prop="fundName"-->
<!--                show-overflow-tooltip-->
<!--              >-->
<!--                <template slot-scope="scope">-->
<!--                  <el-link type="primary" :underline="false" @click="more">-->
<!--                    <span class="elLink" style="font-size: 14px">-->
<!--                      {{ scope.row.fundName | noDataFilter }}-->
<!--                    </span>-->
<!--                  </el-link>-->
<!--                </template>-->
<!--              </el-table-column>-->
<!--              <el-table-column-->
<!--                align="center"-->
<!--                header-align="center"-->
<!--                label="近半年收益趋势"-->
<!--                prop="halfYeear"-->
<!--              >-->
<!--                <template slot-scope="scope">-->
<!--                  <img-->
<!--                    :src="require(`./img/${scope.row.src}`)"-->
<!--                    height="100%"-->
<!--                    width="100%"-->
<!--                  />-->
<!--                  &lt;!&ndash;                  <myecharts&ndash;&gt;-->
<!--                  &lt;!&ndash;                    :id="`combEchart` + scope.row.id"&ndash;&gt;-->
<!--                  &lt;!&ndash;                    :ref="`combEchart` + scope.row.id"&ndash;&gt;-->
<!--                  &lt;!&ndash;                    :options="scope.row.option"&ndash;&gt;-->
<!--                  &lt;!&ndash;                    resize-dom="cmbfof"&ndash;&gt;-->
<!--                  &lt;!&ndash;                    style="width: 100%; height: 50px"&ndash;&gt;-->
<!--                  &lt;!&ndash;                  ></myecharts>&ndash;&gt;-->
<!--                </template>-->
<!--              </el-table-column>-->
<!--              <el-table-column-->
<!--                align="right"-->
<!--                header-align="center"-->
<!--                label="今年以来收益率(%)"-->
<!--                prop="yearRateReturn"-->
<!--                show-overflow-tooltip-->
<!--              >-->
<!--                <template slot-scope="scope">-->
<!--                  <span v-if="scope.row.yearRateReturn > 0" style="color: red">-->
<!--                    {{-->
<!--                      scope.row.yearRateReturn | numberToFixedStr(2, 100, "%")-->
<!--                    }}-->
<!--                  </span>-->
<!--                  <span v-else-if="scope.row.yearRateReturn == 0">-->
<!--                    {{-->
<!--                      scope.row.yearRateReturn | numberToFixedStr(2, 100, "%")-->
<!--                    }}-->
<!--                  </span>-->
<!--                  <span v-else style="color: green;">-->
<!--                    {{-->
<!--                      scope.row.yearRateReturn | numberToFixedStr(2, 100, "%")-->
<!--                    }}-->
<!--                  </span>-->
<!--                </template>-->
<!--              </el-table-column>-->
<!--              <el-table-column-->
<!--                align="right"-->
<!--                header-align="center"-->
<!--                label="近一月收益率(%)"-->
<!--                prop="monthRateReturn"-->
<!--                show-overflow-tooltip-->
<!--              >-->
<!--                <template slot-scope="scope">-->
<!--                  <span v-if="scope.row.monthRateReturn > 0" style="color: red">-->
<!--                    {{-->
<!--                      scope.row.monthRateReturn | numberToFixedStr(2, 100, "%")-->
<!--                    }}-->
<!--                  </span>-->
<!--                  <span v-else-if="scope.row.monthRateReturn == 0">-->
<!--                    {{-->
<!--                      scope.row.monthRateReturn | numberToFixedStr(2, 100, "%")-->
<!--                    }}-->
<!--                  </span>-->
<!--                  <span v-else style="color: green;">-->
<!--                    {{-->
<!--                      scope.row.monthRateReturn | numberToFixedStr(2, 100, "%")-->
<!--                    }}-->
<!--                  </span>-->
<!--                </template>-->
<!--              </el-table-column>-->
<!--              <el-table-column-->
<!--                align="left"-->
<!--                header-align="center"-->
<!--                label="管理人"-->
<!--                prop="fundManager"-->
<!--                show-overflow-tooltip-->
<!--              >-->
<!--                <template slot-scope="scope">-->
<!--                  <span>-->
<!--                    {{ scope.row.fundManager | noDataFilter }}-->
<!--                  </span>-->
<!--                </template>-->
<!--              </el-table-column>-->
<!--            </el-table>-->
<!--            <Pagination-->
<!--              :limit="formInline.pageSize"-->
<!--              :page="formInline.pageNum"-->
<!--              :total="total"-->
<!--              @pagination="Pagination"-->
<!--            ></Pagination>-->
<!--          </div>-->
<!--        </template>-->
<!--      </box-template>-->
<!--    </el-col>-->
    <el-col :span="8">
      <shichangdongtai></shichangdongtai>
    </el-col>
    <el-col :span="8">
      <jnylfcljjjzzs></jnylfcljjjzzs>
    </el-col>
    <el-col :span="8">
      <bygclsybx/>
    </el-col>
  </el-row>
</template>
<script>
import shichangdongtai from "./shichangdongtai";
import jnylfcljjjzzs from "./jnylfcljjjzzs";
import Pagination from "@/components/Pagination";
import myecharts from "@/components/Echarts";
import boxTemplate from "./boxTemplate";
import bygclsybx from "./bygclsybx";

export default {
  components: {
    shichangdongtai,
    jnylfcljjjzzs,
    Pagination,
    myecharts,
    boxTemplate,
    bygclsybx
  },
  data() {
    return {
      tableData: [
        {
          id: 6,
          fundCode: "S81870",
          fundName: "芝麻财富3号",
          option: {
            grid: {
              // 设置图表四周留白间距
              top: "2%",
              right: "2%",
              bottom: "4%",
              left: "4%"
            },
            xAxis: {
              show: false,
              type: "category",
              boundaryGap: false, // 设置x轴两边的留白
              axisTick: {
                // x轴刻度尺
                show: false
              },
              axisLine: {
                // x轴线条颜色
                lineStyle: {
                  color: "#999"
                }
              },
              data: ["Mon", "Tue", "Wed", "Thu", "Fri"]
            },
            yAxis: {
              show: false,
              type: "value",
              max: 1400, // 最大刻度值
              interval: 100, // 刻度值间隔值
              splitLine: {
                // 网格线
                show: false // 关闭网格线
              },
              axisLine: {
                // y轴线条颜色
                show: true,
                lineStyle: {
                  color: "#999"
                }
              }
            },
            series: [
              {
                data: [820, 932, 901, 1300, 300],
                type: "line",
                smooth: true, // 面积图改成弧形状
                lineStyle: {
                  width: 1, // 外边线宽度
                  color: "#42b1ff" // 外边线颜色
                },
                showSymbol: false // 去除面积图节点圆
              }
            ]
          },
          yearRateReturn: 0.2515,
          src: "4.png",
          monthRateReturn: -0.0826,
          fundManager: "苏州芝麻财富"
        },
        {
          id: 4,
          fundCode: "SCJ879",
          fundName: "御风进取一号",
          option: {
            grid: {
              // 设置图表四周留白间距
              top: "2%",
              right: "2%",
              bottom: "4%",
              left: "4%"
            },
            xAxis: {
              show: false,
              type: "category",
              boundaryGap: false, // 设置x轴两边的留白
              axisTick: {
                // x轴刻度尺
                show: false
              },
              axisLine: {
                // x轴线条颜色
                lineStyle: {
                  color: "#999"
                }
              },
              data: ["Mon", "Tue", "Wed", "Thu", "Fri"]
            },
            yAxis: {
              show: false,
              type: "value",
              max: 1400, // 最大刻度值
              interval: 100, // 刻度值间隔值
              splitLine: {
                // 网格线
                show: false // 关闭网格线
              },
              axisLine: {
                // y轴线条颜色
                show: true,
                lineStyle: {
                  color: "#999"
                }
              }
            },
            series: [
              {
                data: [820, 932, 901, 1300, 300],
                type: "line",
                smooth: true, // 面积图改成弧形状
                lineStyle: {
                  width: 1, // 外边线宽度
                  color: "#42b1ff" // 外边线颜色
                },
                showSymbol: false // 去除面积图节点圆
              }
            ]
          },
          src: "2.png",
          yearRateReturn: -0.1477,
          monthRateReturn: -0.0733,
          fundManager: "丰穗投资"
        },
        {
          id: 7,
          fundCode: "SNJ780",
          fundName: "汇牛上善若水",
          src: "5.png",
          option: {
            grid: {
              // 设置图表四周留白间距
              top: "2%",
              right: "2%",
              bottom: "4%",
              left: "4%"
            },
            xAxis: {
              show: false,
              type: "category",
              boundaryGap: false, // 设置x轴两边的留白
              axisTick: {
                // x轴刻度尺
                show: false
              },
              axisLine: {
                // x轴线条颜色
                lineStyle: {
                  color: "#999"
                }
              },
              data: ["Mon", "Tue", "Wed", "Thu", "Fri"]
            },
            yAxis: {
              show: false,
              type: "value",
              max: 1400, // 最大刻度值
              interval: 100, // 刻度值间隔值
              splitLine: {
                // 网格线
                show: false // 关闭网格线
              },
              axisLine: {
                // y轴线条颜色
                show: true,
                lineStyle: {
                  color: "#999"
                }
              }
            },
            series: [
              {
                data: [820, 932, 901, 1300, 300],
                type: "line",
                smooth: true, // 面积图改成弧形状
                lineStyle: {
                  width: 1, // 外边线宽度
                  color: "#42b1ff" // 外边线颜色
                },
                showSymbol: false // 去除面积图节点圆
              }
            ]
          },
          yearRateReturn: 0.2515,
          monthRateReturn: -0.0826,
          fundManager: "汇牛资产"
        },
        {
          id: 5,
          fundCode: "SE2068",
          fundName: "银德1期",
          option: {
            grid: {
              // 设置图表四周留白间距
              top: "2%",
              right: "2%",
              bottom: "4%",
              left: "4%"
            },
            xAxis: {
              show: false,
              type: "category",
              boundaryGap: false, // 设置x轴两边的留白
              axisTick: {
                // x轴刻度尺
                show: false
              },
              axisLine: {
                // x轴线条颜色
                lineStyle: {
                  color: "#999"
                }
              },
              data: ["Mon", "Tue", "Wed", "Thu", "Fri"]
            },
            yAxis: {
              show: false,
              type: "value",
              max: 1400, // 最大刻度值
              interval: 100, // 刻度值间隔值
              splitLine: {
                // 网格线
                show: false // 关闭网格线
              },
              axisLine: {
                // y轴线条颜色
                show: true,
                lineStyle: {
                  color: "#999"
                }
              }
            },
            series: [
              {
                data: [820, 932, 901, 1300, 300],
                type: "line",
                smooth: true, // 面积图改成弧形状
                lineStyle: {
                  width: 1, // 外边线宽度
                  color: "#42b1ff" // 外边线颜色
                },
                showSymbol: false // 去除面积图节点圆
              }
            ]
          },
          src: "1.png",
          yearRateReturn: 0.1627,
          monthRateReturn: -0.0719,
          fundManager: "银德资产"
        },
        {
          id: 8,
          fundCode: "SCZ477",
          fundName: "海象1号",
          option: {
            grid: {
              // 设置图表四周留白间距
              top: "2%",
              right: "2%",
              bottom: "4%",
              left: "4%"
            },
            xAxis: {
              show: false,
              type: "category",
              boundaryGap: false, // 设置x轴两边的留白
              axisTick: {
                // x轴刻度尺
                show: false
              },
              axisLine: {
                // x轴线条颜色
                lineStyle: {
                  color: "#999"
                }
              },
              data: ["Mon", "Tue", "Wed", "Thu", "Fri"]
            },
            yAxis: {
              show: false,
              type: "value",
              max: 1400, // 最大刻度值
              interval: 100, // 刻度值间隔值
              splitLine: {
                // 网格线
                show: false // 关闭网格线
              },
              axisLine: {
                // y轴线条颜色
                show: true,
                lineStyle: {
                  color: "#999"
                }
              }
            },
            series: [
              {
                data: [820, 932, 901, 1300, 300],
                type: "line",
                smooth: true, // 面积图改成弧形状
                lineStyle: {
                  width: 1, // 外边线宽度
                  color: "#42b1ff" // 外边线颜色
                },
                showSymbol: false // 去除面积图节点圆
              }
            ]
          },
          src: "6.png",
          yearRateReturn: 0.2255,
          monthRateReturn: -0.0956,
          fundManager: "广东海象私募基金"
        }
      ],
      formInline: {
        pageNum: 1,
        pageSize: 10
      },
      total: 5
    };
  },
  methods: {
    more() {
      this.$router.push({
        path: "/cpxq"
      });
    },
    Pagination() {}
  }
};
</script>
<style lang="scss" scoped>
::v-deep .el-table--scrollable-y .el-table__body-wrapper {
  overflow-y: hidden;
}
.dashboard-title {
  font-size: 18px;
  // font-weight: 600;
  margin-right: 16px;
}

.comb-title {
  color: #2772bd;
  font-size: 16px;
}

.comb-income {
  font-weight: bold;
  font-size: 18px;
}

.income-red {
  color: red;
}

.income-green {
  color: green;
}

.rate-return-red {
  color: red;
}

.rate-return-green {
  color: green;
}

.el-divider--vertical {
  top: 48px;
  display: inline-block;
  width: 1px;
  height: 130px;
  margin: 0px 8px;
  vertical-align: middle;
  position: relative;
}

.elLink {
  width: 34px;
  color: #2672bc;
  font-size: 14px;
}
</style>

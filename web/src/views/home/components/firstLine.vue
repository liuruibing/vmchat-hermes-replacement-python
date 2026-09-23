<template>
  <el-row :gutter="20" justify="start" type="flex">
    <el-col :span="16">
      <box-template>
        <template slot="title">
          <div class="dashboard-title">快捷入口</div>
        </template>
        <template slot="content">
          <div style="padding: 20px 20px;">
            <el-row>
              <template v-for="item in boxArray">
                <el-col
                  :span="3"
                  style="padding-left: 5px; padding-right: 5px;"
                >
                  <div class="box-style" @click="handleBoxClick(item.content)">
                    <div
                      style="height: 60%;width:100%;text-align: center;line-height: 85px;display: inline-block;vertical-align: middle"
                    >
                      <svg-icon
                        :iconClass="item.iconName"
                        className="icon-style"
                      ></svg-icon>
                    </div>
                    <div
                      style="height: 40px;width: 100%;text-align: center;color: white"
                    >
                      <span style="font-size: 14px;">{{ item.content }}</span>
                    </div>
                  </div>
                </el-col>
              </template>
            </el-row>
          </div>
        </template>
      </box-template>
    </el-col>
<!--    <el-col :span="8">-->
<!--      <box-template>-->
<!--        <template slot="title">-->
<!--          <el-row>-->
<!--            <el-col :span="12">-->
<!--              <div class="dashboard-title">动态消息</div>-->
<!--            </el-col>-->
<!--            <el-col :span="12">-->
<!--              <div class="search_button_com">-->
<!--                <span style="font-size: 14px">-->
<!--                  <el-link :underline="false" type="primary" @click="more"-->
<!--                    ><span class="elLink">更多</span></el-link-->
<!--                  >-->
<!--                </span>-->
<!--              </div>-->
<!--            </el-col>-->
<!--          </el-row>-->
<!--        </template>-->
<!--        <template slot="content">-->
<!--          <div style="height: 140px; padding: 10px 10px;">-->
<!--            <el-table-->
<!--              :data="tableData"-->
<!--              :show-header="false"-->
<!--              max-height="120px"-->
<!--              stripe-->
<!--            >-->
<!--              <el-table-column align="left" min-width="180px;" prop="name">-->
<!--                <template slot-scope="scope">-->
<!--                  <span>{{ scope.row.name | noDataFilter }}</span>-->
<!--                </template>-->
<!--              </el-table-column>-->
<!--              <el-table-column align="left" prop="date">-->
<!--                <template slot-scope="scope">-->
<!--                  <span style="color: #bfc2c5">{{-->
<!--                    scope.row.date | noDataFilter-->
<!--                  }}</span>-->
<!--                </template>-->
<!--              </el-table-column>-->
<!--              <el-table-column align="right" prop="operate">-->
<!--                <template slot-scope="scope">-->
<!--                  <i class="el-icon-arrow-right" style="#bfc2c5"></i>-->
<!--                </template>-->
<!--              </el-table-column>-->
<!--            </el-table>-->
<!--          </div>-->
<!--        </template>-->
<!--      </box-template>-->
<!--    </el-col>-->
        <el-col :span="8">
          <box-template>
            <template slot="title">
              <el-row>
                <el-col :span="12">
                  <div class="dashboard-title">推荐机构</div>
                </el-col>
                <el-col :span="12">
                  <div class="search_button_com">
                    <span style="font-size: 14px">
                      <el-link :underline="false" type="primary" @click="more"
                        ><span class="elLink">更多</span></el-link
                      >
                    </span>
                  </div>
                </el-col>
              </el-row>
            </template>
            <template slot="content">
              <div style="height: 140px; padding: 10px 10px;">
                <img src="./img/tjjg.png" style="height: 100%;width: 100%;">
              </div>
            </template>
          </box-template>
        </el-col>
  </el-row>
</template>
<script>
import boxTemplate from "./boxTemplate";

export default {
  name: "firstLine",
  components: { boxTemplate },
  data() {
    return {
      boxArray: [
        {
          iconName: "market",
          content: "全市场筛选"
        },
        {
          iconName: "process",
          content: "托管外包产品筛选"
        },
        {
          iconName: "product",
          content: "基金经理"
        },
        {
          iconName: "eval",
          content: "管理人筛选"
        },
        {
          iconName: "pene",
          content: "模拟组合"
        },
        {
          iconName: "product",
          content: "我的组合"
        },
        {
          iconName: "mix",
          content: "绩效归因"
        },
        {
          iconName: "performance",
          content: "市场动态"
        }
      ],
      tableData: [
        {
          name: "全国银行间债券市场准入备案",
          date: "2022年9月10日"
        },
        {
          name: "中国金融期货交易所交易结算会员",
          date: "2022年9月15日"
        },
        {
          name: "就期货合约提供意见资格",
          date: "2022年9月18日"
        },
        {
          name: "依法合规加大对平台经济重点领域的金融支持",
          date: "2022年9月5日"
        }
      ]
    };
  },
  methods: {
    more() {},
    handleBoxClick(content) {
      if (content == "全市场筛选") {
        this.$router.push({
          path: "/tqgl/qscsmcpsx"
        });
      }
      if (content == "托管外包产品筛选") {
        this.$router.push({
          path: "/tqgl/tgwbcpsx"
        });
      }
      if (content == "准入流程管理") {
        this.$router.push({
          path: "/tzgl/zrlcgl"
        });
      }
    }
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

.box-style {
  background: -webkit-linear-gradient(left, #e46c68, #d93935);
  width: 100%;
  height: 100px;
}
:hover {
  cursor: pointer;
}

.icon-style {
  font-size: 36px;
  color: white;
}

.elLink {
  width: 34px;
  color: #2672bc;
  font-size: 14px;
}
</style>

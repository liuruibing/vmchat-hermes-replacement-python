<template>
  <div class="detailTop">
    <div class="box_out">
      <!-- 第一行 -->
      <div class="top_1">
        <div class="top_1_item_1 top_1_item">
          <p class="name_">弗居绝对收益配置1号</p>
          <div class="tag"><span class="tag_item">多策略</span><span class="tag_item">最化</span></div>
        </div>
        <div class="top_1_item_2 top_1_item">
          <span class="color_fcaa4d">[存储中]</span>
          <span
            >来源：<el-select v-model="value1" placeholder="请选择" size="mini">
              <el-option v-for="item in options1" :key="item.value" :label="item.label" :value="item.value">
              </el-option> </el-select
          ></span>
        </div>
        <div class="top_1_item_3 top_1_item">
          <p class="">策略分类：多策略</p>
          <p class="top_1_item_3_star">
            <span>绩效星级：</span>
            <span
              ><el-rate v-model="value2" disabled text-color="#ff9900" style="display: inline-block"> </el-rate
            ></span>
            <i class="el-icon-question" style="color: #ccc"></i>
          </p>
        </div>
        <div class="top_1_item_3 top_1_item">
          <p class="">备案编号：SQL402</p>
          <p class="top_1_item_3_star">
            <span>信誉星级：</span>
            <span
              ><el-rate v-model="value2" disabled text-color="#ff9900" style="display: inline-block"> </el-rate
            ></span>
            <i class="el-icon-question" style="color: #ccc"></i>
          </p>
        </div>
        <div>
          <span class="color_337ab7">协会公示信息</span>
        </div>
        <div style="flex:1">
          <div style="text-align:right">
            <el-button size="small" type="info" disabled>已关注</el-button>
            <el-button size="small" type="primary">导出报告</el-button>
          </div>
        </div>
      </div>
      <!-- 第二行 -->
      <div class="top_2">
        <div class="top_2_1">
          <div class="top_2_1_left">
            <p class="top_2_1_left_t">10.4107</p>
            <p class="top_2_1_left_b">单位净值（22-05-20）</p>
          </div> 
          <div class="top_2_1_right">
            <p>累计净值:10.4107</p>
            <p>复权累计净值:10.4107</p>
          </div>
        </div>
        <div class="top_2_2">
          <div class="text_center">收益率</div>
          <div class="top_2_2_content">
            <div>
              <p class="color_cc0000 text_center">901.79%</p>
              <p class="text_center">近3月</p>
            </div>
            <div>
              <p class="color_cc0000 text_center">875.78%</p>
              <p class="text_center">今年以来</p>
            </div>
            <div>
              <p class="color_cc0000 text_center">91.07%</p>
              <p class="text_center">近1年</p>
            </div>
          </div>
        </div>
        <div class="top_2_2">
          <div class="text_center">成立以来</div>
          <div class="top_2_2_content">
            <div>
              <p class="text_center">4.83%</p>
              <p class="text_center">最大回撤</p>
            </div>
            <div>
              <p class="text_center">1.02</p>
              <p class="text_center">Sharpe比率</p>
            </div>
          </div>
        </div>
        <div class="top_2_4">
          <div class="top_2_4_item">
            <p>成立日期：2021-05-20 [1年3月]</p>
            <p>基金经理：--</p>
            <p>办公地：北京市 <span class="color_337ab7">[该地区更多]</span></p>
          </div>
          <div class="top_2_4_item">
            <p>历史荣誉：无</p>
            <p>投资顾问：<span class="color_337ab7">芜湖弗居投资</span></p>
            <p>基金管理人：<span class="color_337ab7">芜湖弗居投资</span></p>
          </div>
        </div>
      </div>
      <!-- 第三行 -->
      <div class="top_3">
        <el-form :inline="true" :model="formInline" class="demo-form-inline">
          <el-row>
            <el-col :span="20">
              <el-form-item label="统计周期">
            <el-select v-model="formInline.f1" placeholder="" size="small">
              <el-option v-for="item in options2" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item style="margin-right:0">
            <el-date-picker
              v-model="formInline.beginDate"
              align="right"
              type="date"
              value-format="yyyy-MM-dd"
              size="small"
              disabled
              placeholder="选择日期">
            </el-date-picker>
            <span>-</span>
          </el-form-item>
          <el-form-item>
            <el-date-picker
              v-model="formInline.endDate"
              align="right"
              type="date"
              value-format="yyyy-MM-dd"
              size="small"
              disabled
              placeholder="选择日期">
            </el-date-picker>
          </el-form-item>
          <el-form-item label="计算频率">
            <el-select v-model="formInline.f2" placeholder="" size="small">
              <el-option v-for="item in options3" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="净值类型">
            <el-select v-model="formInline.f3" placeholder="" size="small">
              <el-option v-for="item in options4" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="对比指标">
            <el-select v-model="formInline.f4" placeholder="选择比较基准" size="small">
              <el-option v-for="item in options5" :key="item.value" :label="item.label" :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
            </el-col>
            <el-col :span="4">
              <div style="text-align:right">
                <el-button type="primary" size="small">保存应用</el-button>
                <el-button size="small">重置</el-button>
              </div>
            </el-col>
          </el-row>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      value1: "平台产品",
      value2: 4,
      options1: [{ label: "平台产品", value: "平台产品" }],
      options2: [
        { label: "成立以来", value: "成立以来" },
        { label: "今年以来", value: "今年以来" },
        { label: "近1月", value: "近1月" },
        { label: "近3月", value: "近3月" },
        { label: "近6月", value: "近6月" },
        { label: "近1年", value: "近1年" },
        { label: "近2年", value: "近2年" },
        { label: "近3年", value: "近3年" },
      ],
      options3: [
        { label: "自适应", value: "自适应" },
        { label: "日替代", value: "日替代" },
        { label: "周频", value: "周频" },
        { label: "月频", value: "月频" },
      ],
      options4: [
        { label: "复权累计净值", value: "复权累计净值" },
        { label: "累计净值", value: "累计净值" },
      ],
      options5: [],
      formInline:{
        f1:"成立以来",
        f2:"自适应",
        f3:"复权累计净值",
        f4:"",
        beginDate:"2021-05-20",
        endDate:"2022-05-20"
      }
    };
  }
};
</script>

<style lang="scss" scoped>
.text_center{
  text-align: center;
}
.color_cc0000{
  color: #cc0000;
}
.color_337ab7{
  color: #337ab7;
}
.color_fcaa4d{
  color: #fcaa4d;
}
.detailTop {
  .box_out {
    border: 1px solid #ccc;
    padding: 8px;
    .top_1 {
      display: flex;
      border-bottom: 1px dashed #ccc;
      padding-bottom: 10px;
      .top_1_item {
        margin-right: 50px;
      }
      .top_1_item_1 {
        .name_ {
          font-size: 18px;
          font-weight: 600;
        }
        .tag {
          margin-top: 20px;
          .tag_item {
            display: inline-block;
            border: 1px solid #3d71ae;
            color: #3d71ae;
            margin-right: 4px;
            padding: 1px 2px;
          }
        }
      }
      .top_1_item_3{
        .top_1_item_3_star{
          display: flex;
          align-items: center;
        }
      }
    }
    .top_2{
      display: flex;
      align-items: center;
      padding: 20px 0;
      border-bottom: 1px dashed #ccc;
      .top_2_1{
        display: flex;
        align-items: center;
        border-right: 1px dashed #ccc;
        padding-right: 20px;
        .top_2_1_left{
          margin-right: 200px;
          .top_2_1_left_t{
            color: #cc0000;
            font-size: 20px;
          }
        }
      }
      .top_2_2{
        width: 300px;
        border-right: 1px dashed #ccc;
        .top_2_2_content{
          display: flex;
          align-items: center;
          justify-content: space-around;
        }
      }
      .top_2_4{
        padding-left: 20px;
        display: flex;
        align-items: center;
        .top_2_4_item{
          width: 220px;
        }
      }
    }
    .top_3{
      padding-top: 20px;
    }
  }
}
</style>
<template>
  <div id="moreQuery">
    <el-form ref="queryForm" :inline="true" label-position="right" size="small">
      <!-- 投资策略 -->
      <el-row>
        <span>投资策略：</span>
        <div class="tzclbx" @click="bxBtn('.tzclbx')">不限</div>
        <div
          v-for="ele in investStrategy"
          :key="ele.id"
          :class="ele.checked ? 'itemBox-checked' : 'itemBox'"
        >
          <el-checkbox
            v-model="ele.checked"
            :label="ele.label"
            @change="checkedChange($event, '.tzclbx', ele)"
          ></el-checkbox>
        </div>
      </el-row>
      <!-- 是否量化 / 是否对冲 / 是否结构化 -->
      <el-row>
        <div
          v-for="e in line2Data"
          :key="e.mid"
          style="display: flex; align-items:center"
        >
          <span>{{ e.title }}</span>
          <div style="margin-right: 50px">
            <el-radio
              v-for="k in e.options"
              :key="k.id"
              v-model="e.checked"
              :label="k.id"
              border
              size="small"
              >{{ k.label }}
            </el-radio>
          </div>
        </div>
      </el-row>
      <!-- 成立时间 -->
      <el-row class="clsj">
        <span>成立时间：</span>
        <el-select
          v-model="clsjSelect"
          placeholder="请选择"
          size="small"
          style="margin-right: 15px"
          @change="changeSelect"
        >
          <el-option
            v-for="item in clsjOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
        <el-date-picker
          v-model="clsjDate"
          :disabled="isDisabled"
          :picker-options="pickerBeginDateBefore"
          end-placeholder="结束日期"
          range-separator="~"
          size="small"
          start-placeholder="开始日期"
          type="daterange"
          value-format="yyyy-MM-dd"
        >
        </el-date-picker>
        <span style="margin-left: 20px">最近净值日期：</span>
        <el-select
          v-model="clsjSelect1"
          placeholder="请选择"
          size="small"
          style="margin-right: 15px"
          @change="changeSelect"
        >
          <el-option
            v-for="item in clsjOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
        <el-date-picker
          v-model="clsjDate1"
          :disabled="isDisabled"
          :picker-options="pickerBeginDateBefore"
          end-placeholder="结束日期"
          range-separator="~"
          size="small"
          start-placeholder="开始日期"
          type="daterange"
          value-format="yyyy-MM-dd"
        >
        </el-date-picker>
      </el-row>
      <!-- 发行方式 -->
      <el-row class="fxfs">
        <div
          v-for="e in fxfsOptions"
          :key="e.mid"
          style="display: flex; align-items:center"
        >
          <span>{{ e.title }}</span>
          <div class="fxfsbx" @click="bxBtn('.fxfsbx')">不限</div>
          <el-select
            v-model="e.selected"
            clearable
            placeholder="私募公司"
            size="small"
            style="margin-right: 15px"
          >
            <el-option
              v-for="item in e.selectOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
          <div
            v-for="k in e.checkboxOptions"
            :key="k.id"
            :class="k.checked ? 'itemBox-checked' : 'itemBox'"
          >
            <el-checkbox
              v-model="k.checked"
              :label="k.label"
              @change="checkedChange($event, '.fxfsbx')"
            ></el-checkbox>
          </div>
        </div>
      </el-row>
      <!-- 净值频率 / 净值完整度 / 运行状态 / 备案状态 -->
      <el-row class="jzpl">
        <div
          v-for="e in jzplOptions"
          :key="e.mid"
          style="display: flex; align-items:center"
        >
          <span>{{ e.title }}</span>
          <el-select
            v-model="e.selected"
            clearable
            size="small"
            style="margin-right: 15px"
          >
            <el-option
              v-for="item in e.options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </div>
        <div style="display: flex; align-items:center;margin-left: 20px">
          <span>运行状态：</span>
          <div class="yxztbx" @click="bxBtn('.yxztbx')">不限</div>
          <div
            v-for="ele in line5Data[0].checkboxOptions"
            :key="ele.id"
            :class="ele.checked ? 'itemBox-checked' : 'itemBox'"
          >
            <el-checkbox
              v-model="ele.checked"
              :label="ele.label"
              @change="checkedChange($event, '.yxztbx')"
            ></el-checkbox>
          </div>
          <span style="margin-left: 20px">备案状态：</span>
          <div class="baztbx" @click="bxBtn('.baztbx')">不限</div>
          <div
            v-for="ele in line5Data[1].checkboxOptions"
            :key="ele.id"
            :class="ele.checked ? 'itemBox-checked' : 'itemBox'"
          >
            <el-checkbox
              v-model="ele.checked"
              :label="ele.label"
              @change="checkedChange($event, '.baztbx')"
            ></el-checkbox>
          </div>
        </div>
      </el-row>
      <!-- 收益-风险区间 / 计算频率 / 收益率 / 最大回撤 / sharpe比率≥ -->
      <el-row class="syfxqj">
        <div
          v-for="e in syfxOptions"
          :key="e.mid"
          style="display: flex; align-items:center"
        >
          <span>{{ e.title }}</span>
          <el-select
            v-model="e.selected"
            clearable
            size="small"
            style="margin-right: 15px"
          >
            <el-option
              v-for="item in e.options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </div>
        <div
          v-for="e in line6Data"
          :key="e.mid"
          style="display: flex; align-items:center"
        >
          <span style="margin-left: 20px">{{ e.title }}</span>
          <el-select
            v-model="e.selected"
            clearable
            size="small"
            style="margin-right: 15px"
          >
            <el-option
              v-for="item in e.options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
          <el-input
            v-model="e.start"
            onkeyup="value=value.replace(/[^0-9.-]/g,'')"
            size="small"
            style="width: 60px!important"
          />
          %
          <span>-</span>
          <el-input
            v-model="e.end"
            onkeyup="value=value.replace(/[^0-9.-]/g,'')"
            size="small"
            style="width: 60px!important"
          />
          %
        </div>
        <div
          v-for="e in sharpeOptions"
          :key="e.mid"
          style="display: flex; align-items:center"
        >
          <span style="margin-left: 20px">{{ e.title }}</span>
          <el-select
            v-model="e.selected"
            clearable
            size="small"
            style="margin-right: 15px"
          >
            <el-option
              v-for="item in e.options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
          <el-input
            v-model="e.inputVal"
            onkeyup="value=value.replace(/[^0-9.-]/g,'')"
            size="small"
            style="width: 60px!important"
          />
          %
        </div>
      </el-row>
      <!-- 风格评价 / 是否有深度分析 -->
      <el-row class="fgpj">
        <span>风格评价：</span>
        <div class="fgpjbx" @click="bxBtn('.fgpjbx')">不限</div>
        <div
          v-for="e in fgpjOptions"
          :key="e.mid"
          style="display: flex; align-items:center"
        >
          <el-select
            v-model="e.selected"
            :placeholder="e.placeholder"
            clearable
            size="small"
            style="margin-right: 15px"
          >
            <el-option
              v-for="item in e.selectOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </div>
        <span style="margin-left: 20px">是否有深度分析：</span>
        <div
          v-for="e in sdfxOptions"
          :key="e.mid"
          style="display: flex; align-items:center"
        >
          <el-select
            v-model="e.selected"
            :placeholder="e.placeholder"
            clearable
            size="small"
            style="margin-right: 15px"
          >
            <el-option
              v-for="item in e.selectOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </div>
      </el-row>

      <el-row type="flex" class="lastrow">
        <div
          v-for="e in tzfgOptions"
          :key="e.mid"
          style="display: flex; align-items:center"
        >
          <span>{{ e.title }}</span>
          <div style="margin-right: 20px">
            <el-radio
              v-for="k in e.options"
              :key="k.id"
              v-model="e.checked"
              :label="k.id"
              border
              size="small"
              >{{ k.label }}
            </el-radio>
          </div>
        </div>
        <span>大类资产占比：</span>
        <div
          v-for="(item, key) in ZdhcOptions"
          :key="key"
          class="itemBox-tgwb"
          @mouseover="inputMouserIn(item.id, item.name)"
          @mouseleave="inputMouseOut(item.id, item.name)"
        >
          <el-input
            :disabled="true"
            :class="[item.isShow ? 'input-border' : '']"
            :placeholder="item.label"
            size="small"
            style="width: 160px !important"
          />
          <div v-show="item.isShow" class="hover-item">
            <el-input
              v-model="item.start"
              size="small"
              onkeyup="value=value.replace(/[^0-9.-]/g,'')"
            />
            <span>-</span>
            <el-input
              v-model="item.end"
              size="small"
              onkeyup="value=value.replace(/[^0-9.-]/g,'')"
            />
            <el-link :underline="false" type="primary" style="padding-left: 5px"
              >确定</el-link
            >
          </div>
        </div>
      </el-row>
      <el-row type="flex">
        <el-col :span="2"><div>已选条件：</div></el-col>
        <el-col :span="22">
          <el-tag
            v-for="(tag, i) in dynamicTags"
            :key="tag.id"
            style="margin-right: 5px;margin-bottom: 5px;"
          >
            {{ tag.title + tag.value }}
          </el-tag>
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>

<script>
import constant from "./constant.js";

export default {
  name: "MoreQuery",
  data() {
    return {
      // 投资策略
      investStrategy: constant.investStrategy,
      // 是否量化 / 是否对冲 / 是否结构化
      line2Data: constant.line2Data,
      // 成立时间
      clsjOptions: constant.clsjOptions,
      clsjSelect: 1,
      clsjSelect1: 1,
      clsjDate: [],
      clsjDate1: [],
      isDisabled: true,
      pickerBeginDateBefore: {
        disabledDate(time) {
          return time.getTime() > Date.now();
        }
      },
      // 发行方式
      fxfsOptions: constant.fxfsOptions,
      // 净值频率 / 净值完整度
      jzplOptions: constant.jzplOptions,
      // 运行状态 / 备案状态
      line5Data: constant.line5Data,
      // 收益风险区间 / 计算频率
      syfxOptions: constant.syfxOptions,
      // 收益率 / 最大回撤
      line6Data: constant.line6Data,
      // sharpe比率≥
      sharpeOptions: constant.sharpeOptions,
      // 风格评价
      fgpjOptions: constant.fgpjOptions,
      // 是否有深度分析
      sdfxOptions: constant.sdfxOptions,
      // 已选条件
      dynamicTags: [
        {
          id: "001",
          title: "投资策略：",
          value: "股票多投, 债券基金,宏观策略"
        },
        {
          id: "002",
          title: "是否量化：",
          value: "非量化"
        },
        {
          id: "003",
          title: "是否对冲：",
          value: "对冲"
        },
        {
          id: "004",
          title: "发行方式：",
          value: "私募股权投资/公募专户/期货资管"
        },
        {
          id: "005",
          title: "运行状态：",
          value: "存续中, 未备案"
        },
        {
          id: "006",
          title: "收益-风险区间：",
          value: "今年以来"
        },
        {
          id: "007",
          title: "计算频率：",
          value: "自适应"
        },
        {
          id: "008",
          title: "收益率：",
          value: "1%~5%"
        },
        {
          id: "009",
          title: "最大回撤：",
          value: "5%~10%"
        },
        {
          id: "010",
          title: "sharpe比率≥：",
          value: "8%"
        },
        {
          id: "011",
          title: "风格偏好：",
          value: "主题型/下跌市道"
        }
      ],
      // 投资风格
      tzfgOptions: constant.tzfgOptions,
      // 大类资产占比
      ZdhcOptions: [
        {
          id: 1,
          name: "zdhc",
          isShow: false,
          prop: "d17fMaxdraw3m",
          label: "股票占净值比(平均值%)",
          start: "",
          end: ""
        },
        {
          id: 2,
          name: "zdhc",
          isShow: false,
          prop: "d18fMaxdraw6m",
          label: "基金占净值比(平均值%)",
          start: "",
          end: ""
        },
        {
          id: 3,
          name: "zdhc",
          isShow: false,
          prop: "d19fMaxdraw1y",
          label: "期货占净值比(平均值%)",
          start: "",
          end: ""
        },
        {
          id: 4,
          name: "zdhc",
          isShow: false,
          prop: "ddd",
          label: "债权占净值比(平均值%)",
          start: "",
          end: ""
        }
      ]
    };
  },
  methods: {
    bxBtn(val) {
      console.log(val, ">");
      // 获取对应dom节点修改样式
      const Dom = document.querySelector(val);
      Dom.style.backgroundColor = "#dcedff";
      Dom.style.color = "#4f95dd";
      Dom.style.borderColor = "#dcedff";
      if (val === ".tzclbx") {
        // 点击不限时所有checkbox状态改为false => 投资策略
        this.investStrategy.forEach(item => {
          if (item.checked) {
            item.checked = false;
          }
        });
      } else if (val === ".fxfs") {
        // 点击不限时所有checkbox状态改为false => 发行方式
        this.fxfsOptions[0].checkboxOptions.forEach(item => {
          if (item.checked) {
            item.checked = false;
          }
        });
      } else if (val === ".yxztbx") {
        // 点击不限时所有checkbox状态改为false => 运行状态
        this.line5Data[0].checkboxOptions.forEach(item => {
          if (item.checked) {
            item.checked = false;
          }
        });
      } else if (val === ".baztbx") {
        // 点击不限时所有checkbox状态改为false => 备案状态
        this.line5Data[1].checkboxOptions.forEach(item => {
          if (item.checked) {
            item.checked = false;
          }
        });
      }
    },
    checkedChange(e, val) {
      // 获取对应dom节点修改样式
      const Dom = document.querySelector(val);
      Dom.style.backgroundColor = "#fff";
      Dom.style.color = "#000";
    },
    changeSelect(val) {
      if (val === 7) {
        this.isDisabled = false;
      } else {
        this.isDisabled = true;
      }
    },
    /**
     * 监听鼠标移入input
     */
    inputMouserIn(id, name) {
      console.log(id, name);
      const obj = this.filterData(id, name);
      obj.isShow = true;
    },
    /**
     * 监听鼠标移出input
     */
    inputMouseOut(id, name) {
      const obj = this.filterData(id, name);
      obj.isShow = false;
    },
    /**
     * 循环数据过滤
     * @param {} id 当前鼠标进入id
     * @param {*} name 当前鼠标进入name
     */
    filterData(id, name) {
      let obj = {};
      switch (name) {
        case "zdhc":
          obj = this.ZdhcOptions.find(item => item.id === id);
          break;
        default:
          break;
      }
      return obj;
    }
  }
};
</script>

<style lang="scss" scoped>
#moreQuery {
  border: 1px solid #e1e0e0;
  border-top: none;
  padding: 0 10px;

  .tzclbx,
  .fxfsbx,
  .yxztbx,
  .baztbx,
  .fgpjbx {
    border: 1px solid #e1e0e0;
    border-radius: 1px;
    height: 26px;
    padding: 2px 10px;
    margin-right: 10px;
    cursor: pointer;
  }

  .tzclbx:hover,
  .fxfsbx:hover {
    border: 1px solid #4f95dd;
    border-radius: 1px;
    color: #4f95dd;
  }

  .el-row {
    border-bottom: 1px solid #ebeef5;
    padding: 10px 0;
    display: flex;
    align-items: center;
  }

  .itemBox {
    border: 1px solid #e1e0e0;
    border-radius: 1px;
    height: 26px;
    padding: 2px 8px;
    margin-right: 10px;

    span:hover {
      color: #4f95dd;
    }
  }

  .itemBox:hover {
    border: 1px solid #4f95dd;
    border-radius: 1px;
  }

  .itemBox-checked {
    border: 1px solid #e1e0e0;
    border-radius: 1px;
    height: 26px;
    border-color: #e6edfc;
    background: #e6edfc;
    padding: 2px 8px;
    margin-right: 10px;
  }

  .itemBox-tgwb {
    position: relative;
    margin: 3px 5px;
    display: inline-block;
  }

  .input-border {
    border: 2px solid #4f95dd;
    border-bottom: none;
    margin-top: -2px;
    ::v-deep .el-input__inner {
      padding-left: 13px;
    }
  }

  .hover-item {
    position: absolute;
    width: 400px;
    z-index: 9999;
    border: 2px solid #4f95dd;
    background-color: #fff;
    padding: 5px;
    display: flex;
    align-items: center;
    span {
      padding: 0 5px;
    }
  }
  .lastrow {
    ::v-deep .el-form-item {
      margin-bottom: 0 !important;
    }
  }

  // elementUI样式穿透
  ::v-deep .el-radio__input {
    display: none;
  }

  ::v-deep .el-radio {
    margin-right: 0;
    font-size: 14px;
  }

  ::v-deep .el-radio.is-checked {
    border: 1px solid #e1e0e0;
    border-radius: 1px;
    border-color: #e6edfc;
    background: #e6edfc;
    color: #0f65dd;
    padding: 2px 8px;
  }

  ::v-deep .el-radio:hover {
    border: 1px solid #4f95dd;
    border-radius: 1px;
    color: #4f95dd;
  }

  ::v-deep .el-radio--small.is-bordered {
    padding: 5px 11px 0 0px;
    border-radius: 3px;
    height: 26px;
  }

  ::v-deep .el-checkbox:hover {
    color: #4f95dd;
  }

  ::v-deep .el-checkbox__label {
    font-size: 14px;
  }

  ::v-deep .el-tag {
    margin: 0;
  }

  .clsj,
  .fxfs,
  .jzpl,
  .syfxqj,
  .fgpj {
    ::v-deep .el-select .el-input--small {
      width: 120px !important;
    }

    ::v-deep .el-select .el-input__inner {
      height: 26px;
      line-height: 26px;
    }

    ::v-deep .el-input--small .el-input__icon {
      line-height: 26px;
    }

    ::v-deep .el-input--small .el-input__inner {
      height: 26px;
      line-height: 26px;
    }

    ::v-deep .el-date-editor--daterange.el-input__inner {
      width: 265px;
    }

    ::v-deep .el-range-editor--small.el-input__inner {
      height: 26px;
    }

    ::v-deep .el-range-editor--small .el-range__icon {
      line-height: 20px;
    }

    ::v-deep .el-range-editor--small .el-range-separator {
      line-height: 20px;
    }
  }
}
</style>

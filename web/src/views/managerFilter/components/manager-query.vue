<template>
  <!-- 经理筛选上方查询条件 -->
  <div id="dd-query">
    <div class="funds-filter">
      <div class="funds-filter-search">
        <div class="funds-search-simple">
          <el-row style="display: flex;justify-content: center;">
            <el-form :inline="true" :model="simpleSearch">
              <el-form-item label="产品名称">
                <el-input
                  v-model="simpleSearch.productName"
                  placeholder="产品名称"
                  size="small"
                ></el-input>
              </el-form-item>
              <el-form-item label="管理人">
                <el-input
                  v-model="simpleSearch.custodian"
                  placeholder="管理人"
                  size="small"
                ></el-input>
              </el-form-item>
              <el-form-item label="机构规模">
                <el-select
                  v-model="simpleSearch.orzScale"
                  placeholder="机构规模(不限)"
                  size="small"
                  clearable
                  @change="checkBoxfile"
                >
                  <el-option
                    v-for="item in orzScaleOptions"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  >
                    <el-checkbox v-model="item.checkedState">{{
                      item.label
                    }}</el-checkbox>
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" size="small" icon="el-icon-search"
                  >查询</el-button
                >
                <el-button
                  type="info"
                  plain
                  size="small"
                  icon="el-icon-refresh-left"
                  >重置</el-button
                >
                <el-button type="primary" size="small" icon="el-icon-bottom"
                  >导 出</el-button
                >
              </el-form-item>
            </el-form>
          </el-row>
        </div>
        <div class="moreQuery">
          <el-form
            ref="queryForm"
            :inline="true"
            label-position="right"
            size="small"
          >
            <!-- 投资策略 -->
            <el-row class="tzcl">
              <el-form-item
                label="投资策略"
                label-width="70px"
                style="display:flex; align-items:center"
              >
                <span
                  class="tzclbx"
                  @click="bxBtn('.tzclbx')"
                  style="color: #333"
                  >不限</span
                >
                <span
                  v-for="ele in investStrategy"
                  :key="ele.id"
                  :class="ele.checked ? 'itemBox-checked' : 'itemBox'"
                >
                  <el-checkbox
                    v-model="ele.checked"
                    :label="ele.label"
                    @change="checkedChange($event, '.tzclbx', ele)"
                  ></el-checkbox>
                </span>
              </el-form-item>
            </el-row>
            <!-- 投资策略 -->
            <el-row class="jlbj">
              <el-form-item
                label="经理背景"
                label-width="70px"
                style="display:flex; align-items:center"
              >
                <span
                  class="jlbjbx"
                  @click="bxBtn('.jlbjbx')"
                  style="color: #333"
                  >不限</span
                >
                <span
                  v-for="ele in jlbjStrategy"
                  :key="ele.id"
                  :class="ele.checked ? 'itemBox-checked' : 'itemBox'"
                >
                  <el-checkbox
                    v-model="ele.checked"
                    :label="ele.label"
                    @change="checkedChange($event, '.jlbjbx', ele)"
                  ></el-checkbox>
                </span>
              </el-form-item>
            </el-row>
            <!-- 从业年限 -->
            <el-row class="clsj">
              <el-form-item
                label="从业年限"
                label-width="70px"
                style="display:flex; align-items:center"
              >
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
              </el-form-item>
            </el-row>
            <!-- 代表产品净值日期 / 代表产品统计周期 -->
            <el-row class="dbcp">
              <el-form-item
                label="代表产品净值日期"
                label-width="120px"
                style="display:flex; align-items:center"
              >
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
              </el-form-item>
              <el-form-item
                label="代表产品统计周期"
                label-width="120px"
                style="display:flex; align-items:center"
              >
                <el-select
                  v-model="dbcpZqSelect"
                  placeholder="请选择"
                  size="small"
                  style="margin-right: 15px"
                >
                  <el-option
                    v-for="item in dbcpZqOptions"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                  >
                  </el-option>
                </el-select>
              </el-form-item>
            </el-row>
            <el-row>
              <el-form-item label="已选条件" label-width="70px">
                <el-tag
                  v-for="(tag, i) in dynamicTags"
                  :key="i"
                  :disable-transitions="false"
                  closable
                >
                  {{ tag.title + tag.value }}
                </el-tag>
              </el-form-item>
            </el-row>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "manager-query",
  data() {
    return {
      orzScaleOptions: [
        {
          label: "0-5亿",
          value: "1",
          checkedState: false
        },
        {
          label: "5-10亿",
          value: "2",
          checkedState: false
        },
        {
          label: "10-20亿",
          value: "3",
          checkedState: false
        },
        {
          label: "20-50亿",
          value: "4",
          checkedState: false
        },
        {
          label: "100亿以上",
          value: "5",
          checkedState: false
        }
      ],
      simpleSearch: {
        productName: "",
        custodian: "",
        orzScale: ""
      },
      investStrategy: [
        {
          id: 1,
          label: "股票多头",
          checked: true
        },
        {
          id: 2,
          label: "股票市场中性",
          checked: false
        },
        {
          id: 3,
          label: "股票多空",
          checked: true
        },
        {
          id: 4,
          label: "债券基金",
          checked: false
        },
        {
          id: 5,
          label: "管理期货",
          checked: true
        },
        {
          id: 6,
          label: "套利策略",
          checked: false
        },
        {
          id: 7,
          label: "宏观策略",
          checked: false
        },
        {
          id: 8,
          label: "组合基金",
          checked: false
        },
        {
          id: 11,
          label: "多策略",
          checked: true
        },
        {
          id: 12,
          label: "其他",
          checked: false
        }
      ],
      jlbjStrategy: [
        {
          id: 1,
          label: "券商",
          checked: false
        },
        {
          id: 2,
          label: "保险",
          checked: true
        },
        {
          id: 3,
          label: "信托",
          checked: false
        },
        {
          id: 4,
          label: "公募",
          checked: false
        },
        {
          id: 5,
          label: "私募",
          checked: true
        },
        {
          id: 6,
          label: "银行",
          checked: false
        },
        {
          id: 7,
          label: "期货",
          checked: true
        },
        {
          id: 8,
          label: "其他",
          checked: false
        }
      ],
      clsjOptions: [
        {
          label: "不限",
          value: 1
        },
        {
          label: "6个月以下",
          value: 2
        },
        {
          label: "6个月~1年",
          value: 3
        },
        {
          label: "1-3年",
          value: 4
        },
        {
          label: "3-5年",
          value: 5
        },
        {
          label: "5年以上",
          value: 6
        },
        {
          label: "自定义",
          value: 7
        }
      ],
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
      line4Data: [
        {
          mid: 2,
          checkboxOptions: [
            {
              id: 1,
              label: "已备案",
              checked: false
            },
            {
              id: 2,
              label: "未备案",
              checked: true
            }
          ]
        },
        {
          mid: 2,
          checkboxOptions: [
            {
              id: 1,
              label: "证券投资基金",
              checked: false
            },
            {
              id: 2,
              label: "股权、创业投资基金",
              checked: true
            },
            {
              id: 3,
              label: "资产配置基金",
              checked: true
            },
            {
              id: 4,
              label: "其他投资基金",
              checked: true
            }
          ]
        }
      ],
      dbcpPlOptions: [
        {
          label: "不限",
          value: 0
        }
      ],
      dbcpPlSelect: 0,
      dbcpZqOptions: [
        {
          label: "成立以来",
          value: 0
        }
      ],
      dbcpZqSelect: 0,
      qtselect1: "1",
      qtselect2: "1",
      qtselect3: "1",
      qtselect4: "1",
      qtselect5: "1",
      dynamicTags: [
        {
          id: "001",
          title: "投资策略：",
          value: "股票多头, 股票多空, 管理期货, 多策略"
        },
        {
          id: "002",
          title: "经理背景：",
          value: "保险, 私募, 期货"
        },
        {
          id: "003",
          title: "代表产品统计周期：",
          value: "成立以来"
        }
      ]
    };
  },
  methods: {
    bxBtn(val) {
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
      } else if (val === ".jlbjbx") {
        this.jlbjStrategy.forEach(item => {
          if (item.checked) {
            item.checked = false;
          }
        });
      } else if (val === ".baztbx") {
        // 点击不限时所有checkbox状态改为false => 备案状态
        this.line4Data[0].checkboxOptions.forEach(item => {
          if (item.checked) {
            item.checked = false;
          }
        });
      } else if (val === ".jjgllbbx") {
        // 点击不限时所有checkbox状态改为false => 基金管理类别
        this.line4Data[1].checkboxOptions.forEach(item => {
          if (item.checked) {
            item.checked = false;
          }
        });
      }
    },
    checkBoxfile(val) {
      this.orzScaleOptions.forEach(itm => {
        if (val === itm.value) {
          itm.checkedState = true;
        } else {
          itm.checkedState = false;
        }
      });
    },
    checkedChange(e, val) {
      // 获取对应dom节点修改样式
      const Dom = document.querySelector(val);
      Dom.style.backgroundColor = "#fff";
      Dom.style.color = "#333";
    },
    changeSelect(val) {
      if (val === 7) {
        this.isDisabled = false;
      } else {
        this.isDisabled = true;
      }
    }
  }
};
</script>

<style lang="scss" scoped>
#dd-query {
  .funds-filter {
    width: 100%;
    .funds-filter-search {
      //border-bottom: 1px solid #e1e0e0;
    }
    .funds-search-simple {
      margin-bottom: 10px;
    }
  }
  .moreQuery {
    border: 1px solid #e1e0e0;
    padding: 0 10px;
    .el-row {
      border-bottom: 1px solid #ebeef5;
      padding: 5px 0;
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
    .clsjbx,
    .tzclbx,
    .baztbx,
    .jjgllbbx,
    .jlbjbx {
      border: 1px solid #e1e0e0;
      border-radius: 1px;
      height: 26px;
      padding: 4px 10px;
      margin-right: 10px;
      cursor: pointer;
      font-size: 14px;
    }
    .clfw {
      ::v-deep .el-radio {
        margin-right: 15px;
      }
      ::v-deep .el-radio--small.is-bordered {
        height: 26px;
        padding: 5px 16px 0 10px;
      }
      ::v-deep .el-radio:hover {
        border: 1px solid #4f95dd;
        border-radius: 1px;
        color: #4f95dd;
      }
      ::v-deep .el-radio.is-checked {
        border: 1px solid #e1e0e0;
        border-radius: 1px;
        border-color: #e6edfc;
        background: #e6edfc;
        color: #0f65dd;
      }
    }
    .clsj,
    .dbcp {
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
      ::v-deep .el-select .el-input--small {
        width: 120px !important;
      }

      ::v-deep .el-select .el-input__inner {
        height: 26px;
        line-height: 26px;
      }
    }
    .qt {
      ::v-deep .el-select.item1 .el-input--small {
        width: 180px !important;
      }
      ::v-deep .el-select .el-input__inner {
        height: 26px;
        line-height: 26px;
      }
      .qtbx {
        border: 1px solid #e1e0e0;
        background-color: #dcedff;
        border-radius: 1px;
        height: 26px;
        padding: 2px 10px;
        margin-right: 10px;
        cursor: pointer;
        font-size: 14px;
      }
    }
  }

  // elementUI样式穿透
  ::v-deep .el-tag {
    margin-bottom: 0;
  }
  ::v-deep .el-checkbox__label {
    font-size: 14px;
  }
  ::v-deep .el-form-item {
    margin-bottom: 0 !important;
  }
  ::v-deep .el-radio__input {
    display: none;
  }
  ::v-deep .el-button {
    background-color: #fcaa4d;
    border-color: transparent;
  }
  ::v-deep.el-button.is-plain {
    background-color: #fff;
    border: 1px solid #4f95dd;
    color: #4f95dd;
  }
  ::v-deep.el-button.is-plain:hover {
    background-color: #4f95dd;
    color: #fff;
  }
}
</style>

<template>
  <!-- 持仓查询 -->
  <div class="subfundPosition analyse-page">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formQuery" :inline="true" :rules="searchRules" :model="formQuery" class="standard-form">
          <el-row>
            <el-form-item prop="fundNames">
              <el-tooltip effect="dark" :content="formQuery.fundNames" placement="top-start" :disabled="!formQuery.fundNames">
                <el-input v-model.trim="formQuery.fundNames" clearable placeholder="请选择产品" size="small" @click.native="openFundListDialog" @change="handleFundNamesChange" />
              </el-tooltip>
            </el-form-item>
            <el-form-item prop="ddate_" label="" class="mb20">
              <el-date-picker
                v-model="formQuery.ddate_"
                type="daterange"
                value-format="yyyy-MM-dd"
                align="left"
                size="small"
                unlink-panels
                range-separator="至"
                start-placeholder="请选择开始日期"
                end-placeholder="请选择结束日期"
                popper-class="popperDateShortTP"
                :picker-options="dateShortTPCTA()"
              ></el-date-picker>
            </el-form-item>
            <el-form-item prop="symBol">
              <el-input v-model.trim="formQuery.subCode" clearable placeholder="请输入子基金代码" size="small" />
            </el-form-item>
            <el-form-item prop="symName">
              <el-input v-model.trim="formQuery.subName" clearable placeholder="请输入子基金名称" size="small" />
            </el-form-item>
            <el-form-item label="" prop="policyType">
              <el-select class="clll" v-model="formQuery.policyType" clearable size="small" placeholder="请选择策略类型">
                <template v-for="(item, index) in policyTypeList">
                  <el-option :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </template>
              </el-select>
            </el-form-item>
            <el-form-item prop="subPolicyType">
              <el-select class="cllxchild" v-model="formQuery.subPolicyType" clearable size="small" placeholder="请选择子策略类型">
                <template v-for="(item, index) in subPolicyTypeList">
                  <el-option :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </template>
              </el-select>
            </el-form-item>
            <el-form-item class="">
              <el-button type="primary" size="small" icon="el-icon-search" @click="onSubmit('formQuery')">查询</el-button>
<!--              <el-button type="info" size="small" icon="el-icon-refresh" plain @click="resetForm('formQuery')">重置</el-button>-->
              <el-button type="info" size="small" plain :icon="exportLoading ? 'el-icon-loading' : 'el-icon-download'" :disabled="isDisabled" @click="downloadTableExcel">
                {{ downLoadText }}
              </el-button>
            </el-form-item>
          </el-row>
          <el-row>


          </el-row>
        </el-form>
      </div>
    </div>

    <el-row>
      <el-col :span="16">
        <div class="page-model-title">
          <div class="title-icon">
            <div class="color-box"></div>
          </div>
          <span class="title-txt">子基金持仓查询</span>
        </div>
      </el-col>
      <el-col :span="8">
<!--        <div style="float: right">
          <vxe-toolbar ref="tableToolbar" class="standard-vxe-toolbar" :custom="{ immediate: true }" custom />
        </div>-->
      </el-col>
    </el-row>

    <el-row id="standard-table">
      <div id="standard-table-margin">
        <vxe-table
          ref="table1"
          :sort-config="{ remote: true }"
          :loading="tableLoading"
          :custom-config="{ storage: true }"
          :data="tableData"
          :height="tableHeight"
          :cell-style="{ height: '50px' }"
          show-header-overflow
          auto-resize
          show-overflow
          stripe
          @sort-change="handleSortChange"
          resizable
        >
          <vxe-table-column type="seq" title="序号" width="60" header-align="center" />
          <vxe-table-column field="fundCode" title="产品代码" min-width="80" header-align="center" align="center" />
          <vxe-table-column field="fundName" title="产品名称" min-width="250" header-align="center" align="center" />
          <vxe-table-column field="newDate" title="日期" min-width="100" header-align="center" align="center" sortable />
          <vxe-table-column field="subCode" title="子基金代码" min-width="100" header-align="center" align="center" />
          <vxe-table-column field="subName" title="子基金名称" min-width="100" header-align="center" align="center" />
          <vxe-table-column field="policyType" title="策略类型" min-width="120" header-align="center" align="center" />
          <vxe-table-column field="subPolicyType" title="子策略类型" min-width="120" header-align="center" align="center" />
          <vxe-table-column field="amount" title="数量" min-width="120" header-align="center" sortable align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.amount | moneyYuan }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="unitCost" title="单位成本(元)" min-width="150" header-align="center" sortable align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.unitCost | moneyYuan }}</span>
            </template>
          </vxe-table-column>

          <vxe-table-column field="cost" title="成本(元)" min-width="120" header-align="center" align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.cost | moneyYuan }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="costRatio" title="成本占净值比（%）" min-width="120" header-align="center" align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.costRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="price" title="市价(元)" min-width="120" header-align="center" sortable align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.price | moneyYuan }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="priceValue" title="市值(元)" min-width="120" header-align="center" sortable align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.priceValue | moneyYuan }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="priceRatio" title="市值占净值比（%）" min-width="120" header-align="center" align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.priceRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
        </vxe-table>
        <vxe-pager
          :current-page="formQuery.pageNum"
          :page-size="formQuery.pageSize"
          :total="total"
          :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
          border
          size="medium"
          class="standard-vxe-pager"
          @page-change="pagination"
        />
      </div>
    </el-row>
    <!--    <el-dialog
      v-if="dialogMask"
      :visible.sync="dialogMask"
      :close-on-click-modal="false"
      title="产品信息"
      center
      custom-class="customWidth"
    >
      <el-container class="hg100">
        <el-main class="mainBox">
          <FundListDialogMultiphase
            :tagsinfo="tags"
            @getTemplateRow="getTemplateRow"
          />
        </el-main>
      </el-container>
    </el-dialog>-->
    <product-selector
      :multiple="true"
      :leftList="false"
      :dialog-visible="dialogMask"
      :tree-data="treeData"
      :show-tree-key-array="showTreeKeyArray"
      :select-list="selectList"
      default-checked-keys="wdgz"
      @closedialog="handleDialogClosed"
      @submitdialog="handleSubmitClick"
    ></product-selector>
  </div>
</template>
<script type="text/ecmascript-6">
import $ from "jquery";
import { FILE_URL } from "@/utils/request";
import { getToken } from "@/utils/auth";
import Pagination from "@/components/Pagination";
import fun from "@/filters/common";
import commonApi from "@/api/common";
import subfundPositionApi from "@/api/basicEdition/subfundPosition";
import FundListDialogMultiphase from '@/components/FundListDialogMultiphase';
import { downLoadFileByUrl } from "@/utils";
import moment from 'moment'
import productSelector from '@/components/productSelector'
import store from '../../store'
export default {
  name: "SubfundPosition",
  components: {
    Pagination,
    FundListDialogMultiphase,
    productSelector
  },
  data() {
    const validatebeginDate = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请选择开始日期"));
      } else {
        if (this.formQuery.endDate !== null || this.formQuery.endDate !== undefined || this.formQuery.endDate !== "") {
          const startTime = new Date(value);
          const endTime = new Date(this.formQuery.endDate);
          if (startTime > endTime) {
            callback(new Error("开始日期不能大于结束日期"));
          } else {
            callback();
          }
        } else {
          callback();
        }
      }
    };
    const validateEndDate = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请选择结束日期"));
      } else {
        if (
          this.formQuery.beginDate !== null ||
          this.formQuery.beginDate !== undefined ||
          this.formQuery.beginDate !== ""
        ) {
          const startTime = new Date(this.formQuery.beginDate);
          const endTime = new Date(value);
          if (startTime > endTime) {
            callback(new Error("结束日期不能小于开始日期"));
          } else {
            callback();
          }
        } else {
          callback();
        }
      }
    };
    return {
      // 搜索
      formQuery: {
        ddate_: [],
        date: [],
        // 起止日期
        beginDate: "",
        endDate: "",
        // 产品代码
        fundCodes: [],
        fundNames: "",
        // 策略类型
        policyType: "",
        // 子策略类型
        subPolicyType: "",
        // 子基金代码
        subCode: "",
        // 子基金名称
        subName: "",
        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10,
        // 排序方式
        // orderBy : '"price" desc ',
        orderString: ""
      },
      tags: [],
      // 策略类型下拉
      policyTypeList: [],
      // 子策略类型下拉
      subPolicyTypeList: [],
      // 表格高度
      tableHeight: 0,
      // 表格数据
      tableData: [],
      issearchButton: false,
      tableLoading: false,
      total: 0,
      columnWidth: "120",
      dialogMask: false,

      searchRules: {
        ddate_: [{ required: true, message: "请选择日期", trigger: "change" }],
        // beginDate: [
        //   { required: true, message: '请选择开始日期', trigger: 'change' },
        //   { validator: validatebeginDate, trigger: 'change' }
        // ],
        // endDate: [
        //   { required: true, message: '请选择结束日期', trigger: 'change' },
        //   { validator: validateEndDate, trigger: 'change' }
        // ],
        fundNames: [{ required: true, message: "请选择产品", trigger: "change" }]
      },
      selectList: [],
      treeData: [
        {
          label: '产品列表',
          id: 'zstgwb'
        },{
          label: '我的关注',
          id: 'wdgz',
          children: [
            {
              label: '默认分组',
              id: 'mrfz'
            },
            {
              label: '权益组',
              id: 'qyz'
            }
          ]
        }
      ],
      showTreeKeyArray: ['产品列表','我的关注'],
      //成立日
      timDate:"",

      /* 按钮禁止与否 */
      isDisabled: false,
      // 导出图标
      downLoadIcon: "el-icon-download",
      // 导出提示文字
      downLoadText: "导出",
      exportLoading: false,

      baseApi: "", // 页面根地址
      exportButton: false,
      exportText: "导出",
      exportIcon: "el-icon-download"
    };
  },
  watch: {},
  mounted() {
    this.handleTableHeight();
    var self = this
    var baseTime = store.state.edims.baseTime
    if(baseTime){
      self.formQuery.ddate_ = [baseTime.beginDate, baseTime.endDate]
      self.formQuery.beginDate = baseTime.beginDate
      self.formQuery.endDate = baseTime.endDate
    }
    if (self.$route.query.endDate) {
      self.formQuery.endDate = self.$route.query.endDate;
    } else if (this.$store.state.setting.bussinessTwoEndDate) {
      this.formQuery.endDate = this.$store.state.setting.bussinessTwoEndDate;
    }
    if (self.$route.query.symBolCode) {
      self.formQuery.symBol = self.$route.query.symBolCode;
    }
    if (self.$route.query.fundType) {
      self.formQuery.fundType.push(self.$route.query.fundType);
    }

    // 默认查询
    this.$nextTick(() => {
      this.$refs.table1.connect(this.$refs.tableToolbar);
      // 策略类型
      this.getPolicyTypeListEdims("strategy_type");
      // 子策略类型
      this.getSubPolicyTypeListEdims("fundinvesttype");
      // this.$refs.table1.connect(this.$refs.tableToolbar)
      // this.getManagerList();
    });
  },
  // activated() {
  //   if(this.$store.getters.formQueryFundNames !== '') {
  //     this.formQuery.fundNames = this.$store.getters.formQueryFundNames
  //   }
  //   if(this.$store.getters.formQueryBeginDate !== '') {
  //     this.formQuery.beginDate = this.$store.getters.formQueryBeginDate
  //   }
  //   if(this.$store.getters.formQueryEndDate !== '') {
  //     this.formQuery.endDate = this.$store.getters.formQueryEndDate
  //   }
  // },
  methods: {
    /**
     * @description 动态设置表格高度
     */
    handleTableHeight() {
      this.$nextTick(() => {
        // 根据浏览器高度设置初始高度
        this.tableHeight = window.innerHeight - this.$refs.table1.$el.offsetTop - 325
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.table1.$el.offsetTop - 325
        }
      })
    },
    handleFundNamesChange(val) {
      if (!val) {
        this.tags = [];
        this.formQuery.fundCodes = [];
        this.formQuery.fundNames = "";
      }
    },
    // 获取选中数据
    getTemplateRow(val) {
      this.tags = val.data;
      const self = this;
      const arr = val.data;
      if (arr) {
        self.formQuery.fundCodes = [];
        self.formQuery.fundNames = "";
        arr.forEach(function (item, index) {
          index++;
          if (index < arr.length) {
            self.formQuery.fundNames = self.formQuery.fundNames + item.fundName + ",";
          } else {
            self.formQuery.fundNames = self.formQuery.fundNames + item.fundName;
          }
          self.timDate = item.createDate;
          self.formQuery.fundCodes.push(item.fundCode);
        });
      }
      this.dialogMask = false;
    },
    handleDialogClosed() {
      this.dialogMask = false
    },
    handleSubmitClick(arr) {
      const self = this;
      this.dialogMask = false
      if (arr) {
        self.formQuery.fundCodes = [];
        self.formQuery.fundNames = "";
        arr.forEach(function (item, index) {
          index++;
          if (index < arr.length) {
            self.formQuery.fundNames = self.formQuery.fundNames + item.VC_FUNDNAME + ",";
          } else {
            self.formQuery.fundNames = self.formQuery.fundNames + item.VC_FUNDNAME;
          }
          self.timDate = item.D_CREATE_DATE;
          self.formQuery.fundCodes.push(item.VC_FUNDCODE);

        });
      }
      this.selectList = arr
    },
    // 点击弹窗
    openFundListDialog() {
      this.dialogMask = true;
    },

    onSubmit(formName) {
      var self = this;
      self.formQuery.pageNum = 1;
      self.$refs[formName].validate((valid) => {
        if (valid) {
          self.onQuery();
          // 禁用搜索按钮
          self.$fun.searchButtonDisabled("issearchButton", self);
        } else {
          return false;
        }
      });
    },

    onQuery(flag) {
      var self = this;
      const params = Object.assign({}, this.formQuery, {});
      if (params.ddate_ && params.ddate_.length) {
        params.beginDate = params.ddate_[0];
        params.endDate = params.ddate_[1];
      }
      delete params.ddate_;
      if (flag) {
        self.downLoadText = "导出中...";
        self.exportLoading = true;
        self.isDisabled = true;
        params.pageNum = 1;
        params.pageSize = 999999;
        params.ex_tmp_name = "子基金持仓查询-导出.xlsx";
       /* const url = "/api/subfundPosition/dosubfundPositionList";
        let fileName="";
         if(params.fundCodes.length==1) {
          fileName=params.fundCodes[0]+"_"+params.fundNames+"_" +
           params.beginDate.replace(/\-/g,"")+"-"+
           params.endDate.replace(/\-/g,"")+"_子基金持仓查询.xls";
         }else{
           fileName= params.beginDate.replace(/\-/g,"")+"-"+
                     params.endDate.replace(/\-/g,"")+"_子基金持仓查询.xls";
         }
        downLoadFileByUrl(url, params, fileName, self);
        return;*/
      }

      if (!flag) {
        this.tableLoading = true;
      }
      new Promise((resolve, reject) => {
        subfundPositionApi
          .fun_selectSubfundPosition(params)
          .then((res) => {
            const { status, data } = res;
            if (status === 0) {
              if (data != null && data != undefined) {
                if (!flag) {
                  const { list, total } = data;
                  this.tableData = list;
                  this.total = total;
                }
                if (flag) {
                  if (!data) return;
                  this.$fun.commonDownloadUrl(data);
                }
              }
            } else {
              self.$message({
                message: "系统异常",
                type: "warning"
              });
            }
            this.tableLoading = false;
            self.exportLoading = false;
            self.isDisabled = false;
            self.downLoadText = "导出";
          })
          .catch((error) => {
            this.tableLoading = false;
            self.exportLoading = false;
            self.isDisabled = false;
            self.downLoadText = "导出";
            reject(error);
          });
      });
    },
    // 策略类型
    getPolicyTypeListEdims(type) {
      // 字典类型
      const params = type;
      commonApi.edimsDdiaCommon(params).then((res) => {
        const { status, data } = res.data;
        if (status === 0) {
          // 产品类型
          if (type === "strategy_type") {
            this.policyTypeList = data;
          }
        }
      });
    },
    // 子策略类型
    getSubPolicyTypeListEdims(type) {
      // 字典类型
      const params = type;
      commonApi.edimsDdiaCommon(params).then((res) => {
        const { status, data } = res.data;
        if (status === 0) {
          // 产品类型
          if (type === "fundinvesttype") {
            this.subPolicyTypeList = data;
          }
        }
      });
    },
    // 导出
    downloadTableExcel() {
      this.onQuery(true);
    },

    //日期时间段快捷选项
    dateShortTPCTA() {
      var self = this
      const pickerOptions = {
        shortcuts: [{
          text: '本周',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
            const start = moment(end).isoWeekday(1).format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '本月',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
            const start = moment([moment(end).year(), 0, 1]).month(moment(end).month()).format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '本季度',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
            const start = moment(moment(end).year() + '-01-01').quarter(moment(end).quarter()).format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '今年以来',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
            const start = moment(end).year() + '-01-01'
            picker.$emit('pick', [start, end])
          }
        },
          {
            text: '成立以来',
            onClick(picker) {
              self.getStandard();
                const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
                const start = self.timDate
                picker.$emit('pick', [start, end])
            }
          },
          {
            text: '近一个月',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(1, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          }, {
            text: '近三个月',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(3, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          }, {
            text: '近半年',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(6, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          }, {
            text: '近一年',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(1, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          }, {
            text: '近三年',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(3, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          },]
      }
      return pickerOptions
    },
    async getStandard() {
      if(this.formQuery.fundCodes.length == 0 || this.formQuery.fundNames ==""){
        this.timDate =""
        this.$message({
          message: '请先选择产品！',
          type: 'warning',
          customClass: "message-warning"
        });
        return
      }
      if(this.formQuery.fundCodes.length > 1){
        this.timDate =""
        this.$message({
          message: '请选择单个产品！',
          type: 'warning',
          customClass: "message-warning"
        });
        return
      }
      if(this.timDate == "" || this.timDate == undefined || this.timDate == null){
        this.$message({
          message: '未获取到成立日！',
          type: 'warning',
          customClass: "message-warning"
        });
        return
      }
    },
    // 清除
    resetForm(formName) {
      this.$refs[formName].resetFields();
      this.tags = [];
      this.formQuery.fundCodes = [];
      this.formQuery.fundNames = "";
    },
    // 分页点击事件
    pagination(val) {
      // let { page, limit } = val;
      const { currentPage, pageSize } = val;
      // 起始页
      this.formQuery.pageNum = currentPage;
      // 每页数量
      this.formQuery.pageSize = pageSize;
      // 查询
      this.onQuery();
    },
    // 当表格的排序条件发生变化的时候会触发该事件
    handleSortChange(val) {
      if (val.property == "amount") {
        val.property = "k.f_amount";
      } else if (val.property == "unitCost") {
        val.property = "k.f_unitprice";
      } else if (val.property == "price") {
        val.property = "k.f_szprice";
      } else if (val.property == "priceValue") {
        val.property = "k.f_price";
      } else if (val.property == "marketVal") {
        val.property = "k.f_price";
      }
      this.formQuery.orderString = this.$fun.queryOrderBy_vxe(val);
      // 查询
      this.onQuery();
    }
  }
};
</script>

<style lang="scss">
.subfundPosition {
  .funds-filter {
    width: 100%;
    // border-bottom: 1px solid #e1e0e0;
  }
  .p1 {
    font-family: FZLanTingHei;
    font-weight: 500;
    font-size: 14px;
    color: rgb(16, 16, 16);
    font-style: normal;
    letter-spacing: 0px;
    line-height: 20px;
    text-decoration: none;
    text-align: left;
  }
  .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
  .title-style {
    color: #e03d3e;
    vertical-align: middle;
    height: 35px;
    line-height: 35px;
    font-size: 16px;
    margin-left: 5px;
  }
  .color-box {
    display: inline-block;
    height: 30px;
    width: 2px;
    background-color: #e03d3e;
  }
  input::-webkit-input-placeholder {
    color: #999 !important;
  }
  .customWidth {
    width: 70% !important;
  }

  .el-tabs__item {
    line-height: 50px !important;
    height: 50px !important;
  }
  .el-checkbox-button__inner {
    border: 0px solid !important;
    border-radius: 0px !important;
  }
  .el-checkbox-button--medium {
    margin-right: 10px;
  }
  .el-checkbox-group {
    float: left;
  }
  .item-label {
    font-size: 14px;
  }
  .el-checkbox-button--medium .el-checkbox-button__inner {
    font-size: 16px;
  }
  .customWidth {
    width: 70% !important;
  }
  .el-tabs__item {
    line-height: 50px !important;
    height: 50px !important;
  }
  .el-dialog {
    width: 54% !important;
    .el-form {
      width: 100% !important;
      font-size: 0;
    }
    .item-label {
      font-size: 14px;
    }
    .vxe-pager.size--medium {
      font-size: 14px;
    }
    .el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell {
      background: #f8f8f8;
    }

    .el-form-item {
      min-width: 50%;
      margin-right: 0;
    }
    .mr5 {
      margin-right: 5px;
    }
  }
}
</style>

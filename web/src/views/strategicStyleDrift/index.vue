<template>
  <!-- 漂移 -->
  <div class="strategicStyleDrift analyse-page" v-auto-enter>
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formQuery" :inline="true" :model="formQuery" :rules="searchRules"  class="form_inline_search standard-form">
          <el-row>
            <el-col :span="24">

                <el-form-item prop="fundCode">
<!--                    <el-input v-model="formQuery.fundName" placeholder="请选择产品" size="small" @click.native="openFundListDialog" />-->
                  <ProductSelectInputMultiple
                    v-model="selectedProducts"
                    placeholder="请选择产品"
                    :input-width="'260px'"
                    @select="handleProductSelect"
                    @clear="handleProductClear"
                  />
                </el-form-item>
<!--            <el-form-item prop="fundName">
              <span slot="label" class="item-label">产品名称</span>
              <el-input v-model.trim="formQuery.fundName" clearable placeholder="请输入" size="small" />
            </el-form-item>-->

<!--            <el-form-item label="" prop="beginDate" class="mb20">-->
<!--              <el-date-picker-->
<!--                v-model="formQuery.beginDate"-->
<!--                :picker-options="dateShortTPCTA()"-->
<!--                style="width:174px"-->
<!--                type="date"-->
<!--                size="small"-->
<!--                value-format="yyyy-MM-dd"-->
<!--                placeholder="请选择开始日期"/>-->
<!--            </el-form-item>-->
<!--            <el-form-item label="" prop="endDate" class="mb20">-->
<!--              <el-date-picker-->
<!--                v-model="formQuery.endDate"-->
<!--                style="width:174px"-->
<!--                type="date"-->
<!--                size="small"-->
<!--                value-format="yyyy-MM-dd"-->
<!--                placeholder="请选择结束日期"/>-->
<!--            </el-form-item>-->
            <el-form-item class="mb20" label="日期" prop="ddate_">
              <el-date-picker
                v-model="formQuery.ddate_"
                :picker-options="dateShortTPCTA()"
                align="left"
                end-placeholder="结束日期"
                popper-class="popperDateShortTP"
                range-separator="-"
                size="small"
                start-placeholder="开始日期"
                type="daterange"
                unlink-panels
                value-format="yyyy-MM-dd"
              ></el-date-picker>
            </el-form-item>
            <el-form-item class="">
              <el-button type="primary" size="small" icon="el-icon-search" @click="onSubmit('formQuery')">查询</el-button>
              <el-button type="info" size="small" icon="el-icon-refresh" plain @click="resetForm('formQuery')">重置</el-button>
              <el-button type="info" size="small" plain :icon="exportLoading ? 'el-icon-loading' : 'el-icon-download'" :disabled="isDisabled" @click="downloadTableExcel">
                {{ downLoadText }}
              </el-button>
            </el-form-item>

            </el-col>
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
          <span class="title-txt">策略漂移详细</span>
        </div>
      </el-col>
<!--      <el-col :span="8">
        <div style="float: right">
          <vxe-toolbar ref="tableToolbar" class="standard-vxe-toolbar" :custom="{ immediate: true }" custom />
        </div>
      </el-col>-->
    </el-row>

    <el-row id="standard-table">
      <div id="standard-table-margin">
        <vxe-table
          ref="table1"
          :sort-config="{ remote: true }"
          v-loading="tableLoading"
          :custom-config="{ storage: true }"
          :height="tableHeight"
          :data="tableData"
          :cell-style="{ height: '50px' }"
          show-header-overflow
          auto-resize
          show-overflow
          stripe
          @sort-change="handleSortChange"
          resizable
        >
          <vxe-table-column type="seq" title="序号" width="60" header-align="center" />
          <vxe-table-column field="dDate" title="日期" min-width="150" header-align="center" align="center" />
          <vxe-table-column field="vcFundcode" title="产品代码" min-width="150" header-align="center" align="center" />
          <vxe-table-column field="vcFundname" title="产品名称" min-width="250" header-align="center" align="center" />
          <vxe-table-column field="vcStockStyle" title="个股风格" min-width="180" header-align="center" align="center" />
          <vxe-table-column field="vcStockSize" title="个股规模" min-width="180" header-align="center" align="center" />
          <vxe-table-column field="vcStockBkStyle" title="板块风格" min-width="120" header-align="center" align="center" />
          <vxe-table-column field="vcStockIndexStyle" title="成分股风格" min-width="120" header-align="center" align="center" />
          <vxe-table-column field="vcDkStyle" title="多空风格" min-width="120" header-align="center" align="center" />
          <vxe-table-column field="vcLhStyle" title="量化风格" min-width="120" header-align="center" align="center" />
          <vxe-table-column field="vcZqStyle" title="债类风格" min-width="120" header-align="center" align="center" />
          <vxe-table-column field="fAvgStockNetRatio"  min-width="180" header-align="center" align="center">
            <template slot="header">
              <div>持仓平均</div>
              <div>股票占比(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fAvgStockNetRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fGrowthStockNetRatio"  min-width="180" header-align="center" align="center">
            <template slot="header">
              <div>个股风格</div>
              <div>成长型占比(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fGrowthStockNetRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fValueStockNetRatio"  min-width="180" header-align="center" align="center">
            <template slot="header">
              <div>个股风格</div>
              <div>价值型占比(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fValueStockNetRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fCoreStockNetRatio"  min-width="180" header-align="center" align="center">
            <template slot="header">
              <div>个股风格</div>
              <div>平衡型占比(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fCoreStockNetRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fLargeStockNetRatio" min-width="180" header-align="center" align="center">

            <template slot="header">
              <div>个股风格</div>
              <div>大盘股占比(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fLargeStockNetRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fMidStockNetRatio"  min-width="180" header-align="center" align="center">
            <template slot="header">
              <div>个股规模</div>
              <div>中盘股占比(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fMidStockNetRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fSmallStockNetRatio"  min-width="180" header-align="center" align="center">
            <template slot="header">
              <div>个股规模</div>
              <div>小盘股占比(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fSmallStockNetRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fShStockNetRatio"  min-width="180" header-align="center" align="center">
            <template slot="header">
              <div>板块风格</div>
              <div>上证主板占比(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fShStockNetRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fSzStockNetRatio"  min-width="180" header-align="center" align="center">
            <template slot="header">
              <div>板块风格</div>
              <div>深证主板占比(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fSzStockNetRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fKcbStockNetRatio"  min-width="180" header-align="center" align="center">
            <template slot="header">
              <div>板块风格</div>
              <div>科创板占比(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fKcbStockNetRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fCybStockNetRatio"  min-width="180" header-align="center" align="center">
            <template slot="header">
              <div>板块风格</div>
              <div>创业板占比(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fCybStockNetRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fBjStockNetRatio" min-width="180" header-align="center" align="center">
            <template slot="header">
              <div>板块风格</div>
              <div>北交所占比(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fBjStockNetRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fXsbStockNetRatio"  min-width="180" header-align="center" align="center">
            <template slot="header">
              <div>板块风格</div>
              <div>新三板占比(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fXsbStockNetRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fHkStockNetRatio"  min-width="180" header-align="center" align="center">
            <template slot="header">
              <div>板块风格</div>
              <div>港股占比(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fHkStockNetRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fQtStockNetRatio"  min-width="180" header-align="center" align="center">
            <template slot="header">
              <div>板块风格</div>
              <div>其他占比(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fQtStockNetRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fHs300StockNetRatio"  min-width="180" header-align="center" align="center">
            <template slot="header">
              <div>成分股风格</div>
              <div>沪深300占比(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fHs300StockNetRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fZz500StockNetRatio"  min-width="180" header-align="center" align="center">
            <template slot="header">
              <div>成分股风格</div>
              <div>中证500占比(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fZz500StockNetRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fZzA500StockNetRatio"  min-width="200" header-align="center" align="center">
            <template slot="header">
              <div>成分股风格</div>
              <div>中证A500占比(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fZzA500StockNetRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fZz800StockNetRatio"  min-width="200" header-align="center" align="center">
            <template slot="header">
              <div>成分股风格</div>
              <div>中证800占比(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fZz800StockNetRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fZz1000StockNetRatio"  min-width="200" header-align="center" align="center">
            <template slot="header">
              <div>成分股风格</div>
              <div>中证1000占比(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fZz1000StockNetRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fZz2000StockNetRatio" min-width="210" header-align="center" align="center">
            <template slot="header">
              <div>成分股风格</div>
              <div>中证2000占比(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fZz2000StockNetRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fQtindexStockNetRatio"  min-width="180" header-align="center" align="center">
            <template slot="header">
              <div>成分股风格</div>
              <div>其他占比(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fQtindexStockNetRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fAvgStockCounts"  min-width="120" header-align="center" align="center">
            <template slot="header">
              <div>平均持股</div>
              <div>数量</div>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fAvgEquityNetExposure"  min-width="120" header-align="center" align="center">
            <template slot="header">
              <div>权益平均</div>
              <div>净敞口(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fAvgEquityNetExposure | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fAvgMonthTurnOver" min-width="120" header-align="center" align="center">
            <template slot="header">
              <div>月度</div>
              <div>换手率(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fAvgMonthTurnOver | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fAvgBondNetRatio"  min-width="120" header-align="center" align="center">
            <template slot="header">
              <div>债券平均</div>
              <div>占比(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fAvgBondNetRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fAvgKzzbondNetRatio"  min-width="180" header-align="center" align="center">
            <template slot="header">
              <div>可转债持仓</div>
              <div>平均占比(%)</div>
            </template>
            <template slot-scope="scope">
              <span>{{ scope.row.fAvgKzzbondNetRatio | baifenlvS }}</span>
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
    <product-selector
      :multiple="true"
      :leftList="false"
      :showSelectAll="true"
      :dialog-visible="dialogMask"
      :tree-data="treeData"
      :show-tree-key-array="showTreeKeyArray"
      :select-list="selectList"
      default-checked-keys="zstgwb"
      @closedialog="handleDialogClosed"
      @submitdialog="handleSubmitClick"
    ></product-selector>

  </div>
</template>
<script type="text/ecmascript-6">
import Pagination from "@/components/Pagination";
import strategicStyleDriftApi from "@/api/strategicStyleDrift/index";
import { downLoadFileByUrlPost } from '@/utils'
import productSelector from '@/components/productSelector'
import moment from 'moment'
import store from '../../store'
// 引入多选悬浮框组件
import ProductSelectInputMultiple from '@/components/productSelector/ProductSelectInputMultiple'

export default {
  name: "strategicStyleDrift",
  components: {
    Pagination,
    productSelector,
    ProductSelectInputMultiple
  },
  data() {
    return {
      selectedProducts: [],
      // 搜索
      formQuery: {
        ddate_:[],
        // 起止日期
        beginDate: "",
        endDate: "",
        // 产品代码
        fundCode: [],
        fundName: "",
        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10,
        orderString: ""
      },
      left: false,
      selectList: [],
      dialogMask: false,
      treeData: [
        {
          label: '产品列表',
          id: 'zstgwb'
        },
        {
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

      // 表格高度
      tableHeight: 0,
      showTreeKeyArray: ['产品列表', '我的关注'],
      tags: [],
      searchRules: {
        fundCode: [{ required: true, message: "请选择产品", trigger: "change" }],
        beginDate: [{ required: true, message: '请选择开始日期', trigger: 'change' }],
        endDate: [{ required: true, message: '请选择结束日期', trigger: 'change' }]
      },
      // 表格数据
      tableData: [],
      issearchButton: false,
      tableLoading: false,
      total: 0,

      /* 按钮禁止与否 */
      isDisabled: false,
      // 导出图标
      downLoadIcon: "el-icon-download",
      // 导出提示文字
      downLoadText: "导出",
      exportLoading: false,

      exportButton: false,
      exportText: "导出",
      exportIcon: "el-icon-download"
    };
  },
 /*  watch: {
    '$route.query': {
      handler(newQuery) {
        this.formQuery.fundCode = newQuery.fundCode || '';
        this.formQuery.beginDate = newQuery.date || '';
        this.formQuery.endDate = newQuery.date || '';
        this.onQuery();
      },
      immediate: true
    }
  }, */
  watch: {
    // 监听选中产品变化，自动更新查询参数
    selectedProducts: {
      handler(newVal) {
        if (newVal && newVal.length > 0) {
          this.formQuery.fundCode = newVal.map(function(item) {
            return item.VC_FUNDCODE
          })
          this.formQuery.fundName = newVal.map(function(item) {
            return item.VC_FUNDNAME
          }).join(',')
        } else {
          this.formQuery.fundCode = []
          this.formQuery.fundName = ""
        }
      },
      immediate: true
    }
  },
  created() {
    var self = this
    var baseTime = store.state.edims.baseTime
    if(baseTime){
      self.formQuery.ddate_ = [baseTime.beginDate, baseTime.endDate]
      self.formQuery.beginDate = baseTime.beginDate
      self.formQuery.endDate = baseTime.endDate
    }
    const query = this.$route.query;
    this.formQuery.fundCode = [];
    this.formQuery.fundName = "";
    if(query.fundCode){
      this.formQuery.fundCode.push(query.fundCode);
      this.formQuery.fundName = query.fundName || '';
      this.selectList = [{
        VC_FUNDCODE: query.fundCode,
        VC_FUNDNAME: query.fundName
      }];
      this.formQuery.ddate_[0] = query.date || '';
      this.formQuery.ddate_[1] = query.date || '';
      this.formQuery.beginDate = query.date || '';
      this.formQuery.endDate = query.date || '';
      this.onQuery();
    }
  },
  mounted() {
    // 动态设置表格高度
    this.handleTableHeight()
    // 默认查询
    //this.onQuery()
  },

  methods: {
    /**
     * @description 动态设置表格高度
     */
    handleTableHeight() {
      this.$nextTick(() => {
        // 根据浏览器高度设置初始高度
        this.tableHeight = window.innerHeight - this.$refs.table1.$el.offsetTop - 285
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.table1.$el.offsetTop - 285
        }
      })
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
      params.beginDate=self.formQuery.ddate_[0]
      params.endDate=self.formQuery.ddate_[1]
      delete params.fundName;
      if (flag) {
        self.downLoadText = "导出中...";
        self.exportLoading = true;
        self.isDisabled = true;
        params.pageNum = 1;
        params.pageSize = 999999;
        params.ex_tmp_name = "策略风格漂移列表.xls";
      }

      if (!flag) {
        this.tableLoading = true;
      }
      new Promise((resolve, reject) => {
        strategicStyleDriftApi
          .fun_selectStrategicStyleDrift(params)
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
    // 导出
    downloadTableExcel() {
      this.downLoadText = "导出中...";
      this.exportLoading = true;
      this.isDisabled = true;
      const params = Object.assign({}, this.formQuery)
      params.beginDate=this.formQuery.ddate_[0]
      params.endDate=this.formQuery.ddate_[1]
      delete params.fundName;
      const fileName = '策略风格漂移列表.xlsx'
      const url = '/api/strategicStyleDrift/select/export'
      downLoadFileByUrlPost(url, params, fileName, this)
      setTimeout(() => {
        this.exportLoading = false;
        this.isDisabled = false;
        this.downLoadText = "导出";
      }, 10000)
    },

    openFundListDialog() {
      /*this.productSelectorVisible = true*/
      this.dialogMask = true
    },
    handleDialogClosed() {
      this.dialogMask = false
    },
    handleSubmitClick(arr) {
      const self = this;
      this.dialogMask = false
      if (arr) {
        self.formQuery.fundCode = [];
        self.formQuery.fundName = "";
        arr.forEach(function (item, index) {
          index++;
          if (index < arr.length) {
            self.formQuery.fundName = self.formQuery.fundName + item.VC_FUNDNAME + ",";
          } else {
            self.formQuery.fundName = self.formQuery.fundName + item.VC_FUNDNAME;
          }
          self.formQuery.fundCode.push(item.VC_FUNDCODE);

        });
      }
      this.selectList = arr
    },

    // 清除
    resetForm(formName) {
      this.$refs[formName].resetFields();
      this.formQuery.fundCode = "";
      this.formQuery.fundName = "";
      this.formQuery.ddate_[0] = "";
      this.formQuery.ddate_[1] = "";
      this.formQuery.beginDate = "";
      this.formQuery.endDate = "";
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
      this.formQuery.orderString = this.$fun.queryOrderBy_vxe(val);
      // 查询
      this.onQuery();
    },
    //日期时间段快捷选项
    dateShortTPCTA() {
      var self = this
      const pickerOptions = {
        shortcuts: [
          {
            text: '本周',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(end).isoWeekday(1).format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
              // self.formQuery.beginDate = start
              // self.formQuery.endDate = end
            }
          },
          {
            text: '本月',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment([moment(end).year(), 0, 1])
                .month(moment(end).month())
                .format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
              // self.formQuery.beginDate = start
              // self.formQuery.endDate = end
            }
          },
          {
            text: '本季度',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).year() + '-01-01')
                .quarter(moment(end).quarter())
                .format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
              /*self.formQuery.beginDate = start
              self.formQuery.endDate = end*/
            }
          },
          {
            text: '今年以来',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(end).year() + '-01-01'
              picker.$emit('pick', [start, end])
              /*self.formQuery.beginDate = start
              self.formQuery.endDate = end*/
            }
          },
          {
            text: '近一个月',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(1, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
              /*self.formQuery.beginDate = start
              self.formQuery.endDate = end*/
            }
          },
          {
            text: '近三个月',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(3, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
             picker.$emit('pick', [start, end])
             /*self.formQuery.beginDate = start
            self.formQuery.endDate = end*/
          }
        },
        {
          text: '近半年',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
            const start = moment(moment(end).subtract(6, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
            /*self.formQuery.beginDate = start
            self.formQuery.endDate = end*/
          }
        },
        {
          text: '近一年',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
            const start = moment(moment(end).subtract(1, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
            /*self.formQuery.beginDate = start
            self.formQuery.endDate = end*/
          }
        },
        {
          text: '近三年',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
            const start = moment(moment(end).subtract(3, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
            /*self.formQuery.beginDate = start
            self.formQuery.endDate = end*/
           }
         }
     ]
  }
return pickerOptions
},
}
};
</script>

<style lang="scss">
.strategicStyleDrift {
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

<template>
  <div class="ann_report_out">
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <!-- <el-tab-pane label="全部" name="All"></el-tab-pane> -->
      <el-tab-pane label="日报" name="D"> </el-tab-pane>
      <el-tab-pane label="周报" name="W"> </el-tab-pane>
      <el-tab-pane label="月报" name="M"> </el-tab-pane>
      <el-tab-pane label="季报" name="Q"> </el-tab-pane>
      <el-tab-pane label="半年报" name="S"> </el-tab-pane>
      <el-tab-pane label="年报" name="Y"> </el-tab-pane>
    </el-tabs>

    <el-tabs v-model="activeName2" @tab-click="handleClick2">
      <el-tab-pane label="全部" name="fourth"> </el-tab-pane>
      <el-tab-pane label="待生成" name="0"> </el-tab-pane>
      <el-tab-pane label="待复核" name="2"> </el-tab-pane>
      <el-tab-pane label="待报送" name="3"> </el-tab-pane>
      <el-tab-pane label="已完成" name="4"> </el-tab-pane>
    </el-tabs>

    <el-form
      :inline="true"
      ref="formInline"
      :model="formInline"
      label-width="100px"
      style="margin-bottom: 8px"
      class="demo-form-inline form_inline_search currency_report_old_form"
    >
      <el-row>
        <el-col :span="20">
          <div style="width: 100%">
            <el-form-item label="报表类型" prop="reportType">
              <el-select
                v-model="formInline.reportType"
                size="small"
                placeholder="请选择"
                @change="changeReportType"
              >
                <el-option
                  v-for="(group, index) in name5Arr"
                  :value="group.dimCde"
                  :key="index"
                  :label="group.dimNme"
                >
                </el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="报表名称" prop="reportName">
              <el-input
                v-model="formInline.reportName"
                placeholder="请输入"
                size="small"
                clearable
              ></el-input>
            </el-form-item>

            <el-form-item label="产品" prop="fundCode" class="asas">
              <select-table
                v-model="formInline.fundCode"
                @enter="onSubmit(true)"
              ></select-table>
            </el-form-item>

            <el-form-item label="产品状态" prop="fundState">
              <el-select
                clearable
                v-model="formInline.fundState"
                size="small"
                placeholder="请选择"
              >
                <el-option
                  v-for="(group, index) in proStatusArr"
                  :value="group.dimCde"
                  :key="index"
                  :label="group.dimNme"
                >
                </el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="勾稽校验" prop="statusDataValid">
              <el-select
                clearable
                v-model="formInline.statusDataValid"
                size="small"
                placeholder="请选择"
              >
                <el-option
                  v-for="(group, index) in name3Arr"
                  :value="group.code"
                  :key="index"
                  :label="group.name"
                >
                </el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="核对状态" prop="statusFileVerify">
              <el-select
                clearable
                v-model="formInline.statusFileVerify"
                size="small"
                placeholder="请选择"
              >
                <el-option
                  v-for="(group, index) in name2Arr"
                  :value="group.code"
                  :key="index"
                  :label="group.name"
                >
                </el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="报告日期" prop="dateSubmitFinal" v-if="formInline.reportType=='CISP'&&activeName=='D'">
              <el-date-picker
                v-model="formInline.dateSubmitFinal"
                type="date"
                editable
                size="small"
                value-format="yyyy-MM-dd"
                placeholder="选择日期"
              >
              </el-date-picker>
            </el-form-item>

            <el-form-item label="估值基准日" prop="reportDate" v-if="!(formInline.reportType=='CISP'&&activeName=='D')">
              <el-date-picker
                v-show="reportTypeOther_year"
                v-model="reportYear"
                type="year"
                editable
                size="small"
                value-format="yyyy"
                placeholder="选择年"
              >
              </el-date-picker>

              <el-select
                v-show="reportTypeOther_show"
                clearable
                v-model="selectDate"
                size="small"
                placeholder="请选择"
              >
                <el-option
                  v-for="(group, index) in reportTypeArr2"
                  :value="group.value"
                  :key="index"
                  :label="group.name"
                >
                </el-option>
              </el-select>

              <el-date-picker
                v-show="reportTypeOther_day"
                v-model="formInline.dateData"
                type="date"
                editable
                size="small"
                value-format="yyyy-MM-dd"
                placeholder="选择日期"
              >
              </el-date-picker>
            </el-form-item>
          </div>
        </el-col>

        <el-col :span="4">
          <el-form-item class="search_button_com">
            <el-button
              type="primary"
              @click="onSubmit(true)"
              style="margin-bottom: 5px"
              size="small"
            >
              查询
            </el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <div style="display: flex">
      <div class="forms_table_title">
        <i class="el-icon-s-data"></i>列表数据
        <span style="margin-left: 30px">
          <el-checkbox
            v-model="fundColumnShowFlag2"
            @change="fundColumnShowFlagChange"
            >产品</el-checkbox
          >
        </span>
      </div>
      <div>
        <el-row>
          <!-- :span="spanSize" :offset="offsetSpan" -->
          <el-col style="min-width: 600px; text-align: right">
            <el-button
              v-if="yjsc_btn_show"
              type="primary"
              @click="yjsc()"
              style="margin-bottom: 5px"
              size="small"
              :loading="btn_laoding"
            >
              一键生成
            </el-button>
            <el-button
              v-if="gjjy_btn_show"
              type="primary"
              @click="gjjy()"
              style="margin-bottom: 5px"
              size="small"
              :loading="btn_laoding"
            >
              勾稽校验
            </el-button>
            <el-button
              v-if="ywbhd_btn_show"
              type="primary"
              @click="ywbhd()"
              style="margin-bottom: 5px"
              size="small"
              :loading="btn_laoding"
            >
              与外包核对
            </el-button>
            <el-button
              v-if="qrfh_btn_show"
              type="primary"
              @click="qrfh()"
              style="margin-bottom: 5px"
              size="small"
              :loading="btn_laoding"
            >
              确认复核
            </el-button>
            <el-button
              v-if="yjsb_btn_show"
              type="primary"
              @click="yjsb()"
              style="margin-bottom: 5px"
              size="small"
              :loading="btn_laoding"
            >
              一键上报
            </el-button>
            <el-button
              type="primary"
              @click="downloadReport()"
              style="margin-bottom: 5px"
              size="small"
              :loading="btn_laoding"
            >
              下载报表
            </el-button>
          </el-col>
        </el-row>
      </div>
    </div>

    <el-table
      ref="multipleTable"
      @selection-change="handleSelectionChange"
      :data="tableData"
      border
      stripe
      @sort-change="handleSortChange"
      v-loading="tableLoading"
      style="width: 100%"
      height="calc(100% - 266px)"
    >
      <el-table-column fixed type="selection" width="35"></el-table-column>
      <!-- v-if="fundColumnShowFlag" -->
      <el-table-column
        prop="fundCode"
        sortable="custom"
        show-overflow-tooltip
        label="产品代码"
        min-width="110"
        algin="left"
        header-align="center"
        v-if="fundColumnShowFlag2"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fundCode | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="fundName"
        sortable="custom"
        show-overflow-tooltip
        label="产品名称"
        min-width="110"
        algin="left"
        header-align="center"
        v-if="fundColumnShowFlag2"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fundName | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="fundTypeName"
        sortable="custom"
        show-overflow-tooltip
        label="产品类型"
        min-width="110"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fundTypeName | noDataFilter }}</span>
        </template>
      </el-table-column>
      <!-- <el-table-column
        prop="fundState"
         sortable='custom'
        show-overflow-tooltip
        label="产品状态"
        min-width="110"
        algin="left"
        header-align="center"
		    v-if="fundColumnShowFlag"
      >
        <template slot-scope="scope">
          <span>{{ dataStatus(scope.row.fundState,'1') | noDataFilter }}</span>
        </template>
      </el-table-column> -->

      <el-table-column
        prop="reportName"
        sortable="custom"
        show-overflow-tooltip
        label="报表名称"
        min-width="300"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.reportName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="reportType"
        sortable="custom"
        show-overflow-tooltip
        label="报表类型"
        min-width="110"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{
            dataStatus(scope.row.reportType, "2") ||
            scope.row.reportType | noDataFilter
          }}</span>
          <!-- <span v-if="scope.row.reportType==='XBRL'">XBRL</span>
          <span  v-else-if="scope.row.reportType==='CISP'">CISP</span>
           <span  v-else-if="scope.row.reportType==='RH'">人行</span>
            <span  v-else-if="scope.row.reportType==='ZJX'">中基协</span>
          <span v-else>{{ scope.row.reportType | noDataFilter }}</span> -->
        </template>
      </el-table-column>
      <el-table-column
        prop="reportFrequency"
        sortable="custom"
        show-overflow-tooltip
        label="报表频率"
        min-width="110"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.reportFrequency === 'D'">日报</span>
          <span v-else-if="scope.row.reportFrequency === 'W'">周报</span>
          <span v-else-if="scope.row.reportFrequency === 'M'">月报</span>
          <span v-else-if="scope.row.reportFrequency === 'Q'">季报</span>
          <span v-else-if="scope.row.reportFrequency === 'S'">半年报</span>
          <span v-else-if="scope.row.reportFrequency === 'Y'">年报</span>
          <span v-else>{{ scope.row.reportFrequency | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="statusReport"
        sortable="custom"
        show-overflow-tooltip
        label="报表状态"
        min-width="110"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.statusReport === '0'">待生成</span>
          <span v-else-if="scope.row.statusReport === '1'">已生成</span>
          <span v-else-if="scope.row.statusReport === '2'">待复核</span>
          <span v-else-if="scope.row.statusReport === '3'">待报送</span>
          <span v-else-if="scope.row.statusReport === '4'">已完成</span>
          <span v-else>{{ scope.row.statusReport | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="statusFileCreate"
        sortable="custom"
        show-overflow-tooltip
        label="生成状态"
        min-width="110"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.statusFileCreate === '0'">未生成</span>
          <span v-else-if="scope.row.statusFileCreate === '1'">已生成</span>
          <span
            style="color: red"
            v-else-if="scope.row.statusFileCreate === '2'"
            >生成失败</span
          >
          <span v-else>{{ scope.row.statusFileCreate | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="statusDataValid"
        sortable="custom"
        show-overflow-tooltip
        label="勾稽校验"
        min-width="110"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.statusDataValid === '0'">未校验</span>
          <span v-else-if="scope.row.statusDataValid === '1'">校验成功</span>
          <span style="color: red" v-else-if="scope.row.statusDataValid === '2'"
            >校验失败</span
          >
          <span v-else>{{ scope.row.statusDataValid | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="statusFileVerify"
        sortable="custom"
        show-overflow-tooltip
        label="核对状态"
        min-width="110"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.statusFileVerify === '0'">未核对</span>
          <span v-else-if="scope.row.statusFileVerify === '1'">核对一致</span>
          <span
            style="color: red"
            v-else-if="scope.row.statusFileVerify === '2'"
            >核对不一致</span
          >
          <span v-else>{{ scope.row.statusFileVerify | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="statusReportConfirm"
        sortable="custom"
        show-overflow-tooltip
        label="复核状态"
        min-width="110"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.statusReportConfirm === '0'">未复核</span>
          <span v-else-if="scope.row.statusReportConfirm === '1'">已复核</span>
          <span
            style="color: red"
            v-else-if="scope.row.statusReportConfirm === '2'"
            >复核失败</span
          >
          <span v-else>{{ scope.row.statusReportConfirm | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="statusReportSubmit"
        sortable="custom"
        show-overflow-tooltip
        label="上报状态"
        min-width="110"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.statusReportSubmit === '0'">未上报</span>
          <span v-else-if="scope.row.statusReportSubmit === '1'">上报成功</span>
          <span
            style="color: red"
            v-else-if="scope.row.statusReportSubmit === '2'"
            >上报失败</span
          >
          <span v-else>{{ scope.row.statusReportSubmit | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="dateData"
        sortable="custom"
        show-overflow-tooltip
        label="估值基准日"
        min-width="130"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.dateData | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="dateSubmitFinal"
        sortable="custom"
        show-overflow-tooltip
        label="上报截止日"
        min-width="140"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{
            ((scope.row.dateSubmitFinal || "") +
              " " +
              (scope.row.dateSubmitFinalTime || ""))
              | noDataFilter
          }}</span>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        fixed="right"
        min-width="360"
        align="center"
      >
        <template slot-scope="scope">
          <!-- 
			<el-button v-show="scope.row.name1 =='已清盘'"  type="primary" plain size="small" @click="editData(scope.row)">编辑</el-button>
          <el-button v-show="scope.row.statusReport !='0'"  type="primary" plain size="small" @click="hdmx(scope.row)">核对明细</el-button>
          <el-button v-show="scope.row.statusReport !='0'"  type="primary" plain size="small" @click="czrz(scope.row)">操作日志</el-button>
		-->

          <el-button
            type="primary"
            plain
            size="small"
            @click="editData(scope.row)"
            >编辑与核对</el-button
          >
          <el-button type="primary" plain size="small" @click="jymx(scope.row)"
            >勾稽校验明细</el-button
          >
          <!-- <el-button type="primary" plain size="small" @click="hdmx(scope.row)"
            >与外包核对明细</el-button
          > -->
          <el-button type="primary" plain size="small" @click="czrz(scope.row)"
            >操作日志</el-button
          >

          <el-button
            v-show="scope.row.statusReportConfirm == '1'"
            type="primary"
            plain
            size="small"
            @click="reportConfirmCancel(scope.row)"
            >取消复核</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <Pagination
      :total="total"
      :page="formInline.pageNum"
      :limit="formInline.pageSize"
      @pagination="Pagination"
    ></Pagination>

    <el-dialog
      :title="dialogTitle"
      v-dialogDragWidth
      :before-close="handleClose"
      customClass="xbrlCzrzListWidth_"
      width="75% !important"
      center
      :visible.sync="czrzDialog"
      :close-on-click-modal="false"
    >
      <el-container>
        <el-main class="mainBox">
          <!-- 核对明细 -->
          <annExcelPage
            v-if="annExcelPage_show"
            :PageData="PageData"
          ></annExcelPage>
          <annXmlPage v-if="annXmlPage_show" :PageData="PageData"></annXmlPage>
          <annTxtPage v-if="annTxtPage_show" :PageData="PageData"></annTxtPage>
          <!-- 校验明细 -->
          <checkDetailPage
            v-if="checkDetailPage_show"
            :PageData="PageData"
          ></checkDetailPage>
          <!-- 操作日志 -->
          <annLogPage v-if="annLogPage_show" :PageData="PageData"></annLogPage>
          <!-- 编辑-配置化页面 -->
          <currencyReportPage
            v-if="currencyReportPage_show"
            :currencyReportPageData="currencyReportPageData"
          ></currencyReportPage>
        </el-main>
      </el-container>
    </el-dialog>

    <el-dialog
      :title="dialogTitle"
      v-dialogDragWidth
      :before-close="A1005handleClose"
      customClass="xbrlCzrzListWidth_"
      width="75% !important"
      center
      :visible.sync="A1005Dialog"
      :close-on-click-modal="false"
    >
      <el-container>
        <el-main class="mainBox">
          <reportA1005
            v-if="A1005_show"
            :currencyReportPageData="currencyReportPageData"
          ></reportA1005>
        </el-main>
      </el-container>
    </el-dialog>

    <!-- 复核确认 -->
    <el-dialog
      title="复核确认"
      customClass="qrfuListWidth"
      center
      :visible.sync="countDialog"
      :close-on-click-modal="false"
    >
      <el-container>
        <el-main class="mainBox">
          <el-form
            ref="formCount"
            :model="formCount"
            :rules="countRules"
            label-position="right"
            label-width="120px"
          >
            <el-form-item label="复核确认意见" prop="confirmOpinion">
              <el-input
                v-model="formCount.confirmOpinion"
                type="textarea"
                auto-complete="off"
                maxlength="1000"
                show-word-limit
                :autosize="{ minRows: 4 }"
                placeholder="请输入"
              />
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="countDialog = false" :loading="btn_laoding">取 消</el-button>
        <el-button type="primary" size="small" @click="countSubmit('formCount')" :loading="btn_laoding"
          >确 定</el-button
        >
      </div>
    </el-dialog>

    <!-- 取消复核 -->
    <el-dialog
      title="复核确认"
      customClass="qrfuListWidth"
      center
      :visible.sync="reportConfirmCancelDialog"
      :close-on-click-modal="false"
    >
      <el-container>
        <el-main class="mainBox">
          <el-form
            ref="formCount"
            :model="formCount"
            :rules="countRules"
            label-position="right"
            label-width="120px"
          >
            <el-form-item label="取消复核说明" prop="confirmCancelOpinion">
              <el-input
                v-model="formCount.confirmCancelOpinion"
                type="textarea"
                auto-complete="off"
                maxlength="1000"
                show-word-limit
                :autosize="{ minRows: 4 }"
                placeholder="请输入"
              />
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="reportConfirmCancelDialog = false"
        :loading="btn_laoding"
          >取 消</el-button
        >
        <el-button
          type="primary"
          size="small"
          @click="reportConfirmCancelSubmit('formCount')"
          :loading="btn_laoding"
          >确 定</el-button
        >
      </div>
    </el-dialog>

    <!-- 新更改pageView -->
    <currency-report-page-new
      v-if="currenc_new_show"
      ref="currenc_new_ref"
      @currencBtn="currencValue"
    ></currency-report-page-new>
  </div>
</template>

<script>
import reportA1005 from "./report_A1005.vue";
import selectTable from "@/views/commonComponents/selectTable.vue";
import Pagination from "@/components/Pagination";
import commonFun from "@/filters/new_common";
import pageApi from "@/api/xbrl/xbrl";
import store from "@/store";
import annExcelPage from "./annExcel.vue";
import annXmlPage from "./annXml.vue";
import annTxtPage from "./annTxt.vue";
import annLogPage from "./annLog.vue";
import checkDetailPage from "@/views/perReportCheck/checkDetail.vue";
import currencyReportPage from "@/views/dataReport/currencyReport_";
// 新更改pageView
import CurrencyReportPageNew from "./currencyReport/currencyReoportTree";
export default {
  name: "xbrl",

  components: {
    Pagination,
    annExcelPage,
    annXmlPage,
    annTxtPage,
    annLogPage,
    currencyReportPage,
    CurrencyReportPageNew,
    selectTable,
    checkDetailPage,
    reportA1005,
  },
  data() {
    return {
      nowDate:"",
      btn_laoding: false,
      fundShow: false,
      currenc_new_show: false,
      activeName: "D",
      activeName2: "fourth",
      accountCodes: [], //产品信息数组
      proStatusArr: [], //负责经办数组
      name2Arr: [
        { name: "未核对", code: "0" },
        { name: "核对一致", code: "1" },
        { name: "核对不一致", code: "2" },
      ], //核对状态
      name3Arr: [
        { name: "未校验", code: "0" },
        { name: "校验成功", code: "1" },
        { name: "校验失败", code: "2" },
      ], //勾稽校验
      name5Arr: [
        //  { name: 'XBRL', code: 'XBRL' },
        // { name: 'CISP', code: 'CISP' },
        // { name: '人行', code: 'RH' },
        //  { name: '中基协', code: 'ZJX' },
        //  { name: 'FIRST', code: 'FIRST' },
      ], //产品状态数组
      name6Arr: [], //信批岗确认数组
      formInline: {
        reportName: "", //报告名称
        reportType: "CISP", //报告类型
        fundCode: "", //产品信息
        fundState: "", //产品状态
        statusDataValid: "", //勾稽校验
        statusFileVerify: "", //核对状态
        dateData: "",
        dateSubmitFinal:"", //报告日期
        pageSize: 50,
        pageNum: 1,
        orderString: "",
        reportFrequency: "",
        statusReport: "",
        notShowReportType: "XBRL", //不展示XBRL
      },

      total: 0,
      tableData: [
        // {fundCode:'LBM001',fundName:'路博迈1号',fundTypeName:'公募',name:'产品基本信息',name1:'已清盘',name2:'',name3:'无异常',name4:'未复核',name5:'',name6:'已上报',name7:'2020-07-02',name8:'2020-07-07'},
        // {fundCode:'LBM002',fundName:'路博迈2号',fundTypeName:'公募',name:'产品基本信息',name1:'运作期',name2:'',name3:'未校验',name4:'未生成',name5:'',name6:'未上报',name7:'2020-07-02',name8:'2020-07-07'},
      ], //列表数据
      tableLoading: false, //列表加载
      tableMultipleSelection: [],
      reportTypeArr: [
        { name: "年报", value: "Y" },
        { name: "半年报", value: "S" },
        { name: "季报", value: "Q" },
        { name: "月报", value: "M" },
        { name: "月报", value: "W" },
        { name: "日报", value: "D" },
      ], //报表类型数组
      quarters: [
        { name: "一季度", value: "1" },
        { name: "二季度", value: "2" },
        { name: "三季度", value: "3" },
        { name: "四季度", value: "4" },
      ],
      months: [
        { name: "一月", value: "1" },
        { name: "二月", value: "2" },
        { name: "三月", value: "3" },
        { name: "四月", value: "4" },
        { name: "五月", value: "5" },
        { name: "六月", value: "6" },
        { name: "七月", value: "7" },
        { name: "八月", value: "8" },
        { name: "九月", value: "9" },
        { name: "十月", value: "10" },
        { name: "十一月", value: "11" },
        { name: "十二月", value: "12" },
      ],
      reportTypeArr2: [],
      reportTypeOther_year: false,
      reportTypeOther_show: false,
      reportTypeOther_day: true,
      reportTypeOther_weak: false,
      yjsc_btn_show: true, //一键生成
      gjjy_btn_show: true, //勾稽校验
      ywbhd_btn_show: true, //与外包核对
      qrfh_btn_show: true, //确认复核
      yjsb_btn_show: true, //一键上报
      czrzDialog: false,
      A1005Dialog: false, //A1005
      A1005_show: false,
      czrzTableData: [], //操作日志列表
      czrzTableLoading: false, //操作日志列表加载
      czrzTotal: 0, //操作日志列表总数
      czrzPageNum: 1, //操作日志列表页码
      czrzPageSize: 50, //操作日志列表条数
      offsetSpan: 16,
      spanSize: 8,
      fundStatusArr: {},
      name5Obj: {},
      weekDate: [],
      selectDate: "",
      reportYear: "",
      czrzOrderString: "",
      PageData: {
        recordId: "",
      },
      currencyReportPageData: {},
      annExcelPage_show: false,
      annXmlPage_show: false,
      annTxtPage_show: false,
      annLogPage_show: false,
      checkDetailPage_show: false,
      currencyReportPage_show: false,
      dialogTitle: "",
      countDialog: false,
      reportConfirmCancelDialog: false,
      reportRecordId: "",
      formCount: {
        confirmOpinion: "",
        confirmCancelOpinion: "",
      },
      countRules: {
        confirmOpinion: {
          required: true,
          type: "string",
          message: "请输入复核确认意见",
          trigger: "blur",
        },
        confirmCancelOpinion: {
          required: true,
          message: "请输入取消复核说明",
          trigger: "change",
        },
      },
      formLabelWidth: "120px",
      fundColumnShowFlag: false,
      fundColumnShowFlag2: false,
    };
  },
  // watch:{
  //   activeName(data){
  //     if(data == 'D' && this.formInline.reportType == 'CISP'){
  //       this.formInline.dateData = this.nowDate;
  //     }
  //   },
  //   "formInline.reportType"(data){
  //     if(data == 'CISP' && this.activeName == 'D'){
  //       this.formInline.dateData = this.nowDate;
  //     }
  //   }
  // },

  mounted() {
    this.getSelects("fundinfo_fundState");
    this.getSelects("fundann_submitComp");
    this.getProductsAll();
    // this.onSubmit(true);
  },

  methods: {
    changeReportType() {
      this.formInline.dateSubmitFinal = ''
      var curValue = this.formInline.reportType || "";
      if (curValue == "" || curValue == "XBRL") {
        this.fundColumnShowFlag = true;
      } else {
        this.fundColumnShowFlag = false;
      }
      // 对 Table 进行重新布局。当 Table 或其祖先元素由隐藏切换为显示时，可能需要调用此方法（解决固定列错位问题）
      this.$nextTick(() => {
        this.$refs.multipleTable.doLayout();
      });
    },

    handleClick(tab, event) {
      let tabLabel = tab.label;
      this.reportTypeChange(this.activeName);
      this.formInline.dateData = "";
      this.formInline.dateSubmitFinal = "";
      this.formInline.reportFrequency = this.activeName;
      if (this.activeName === "All") {
        this.formInline.reportFrequency = "";
      }
      if(this.activeName == 'D' && this.formInline.reportType == 'CISP'){
        this.formInline.dateSubmitFinal = this.nowDate;
      }
      this.onSubmit(true);
    },
    handleClick2(tab, event) {
      let tabLabel = tab.label;
      this.formInline.dateData = "";
      if (tabLabel === "全部") {
        this.yjsc_btn_show = true; //一键生成
        this.gjjy_btn_show = true; //勾稽校验
        this.ywbhd_btn_show = true; //与外包核对
        this.qrfh_btn_show = true; //确认复核
        this.yjsb_btn_show = true; //一键上报
        this.offsetSpan = 16;
        this.spanSize = 8;
      } else if (tabLabel === "待生成") {
        this.yjsc_btn_show = true; //一键生成
        this.gjjy_btn_show = false; //勾稽校验
        this.ywbhd_btn_show = false; //与外包核对
        this.qrfh_btn_show = false; //确认复核
        this.yjsb_btn_show = false; //一键上报
        this.offsetSpan = 18;
        this.spanSize = 6;
      } else if (tabLabel === "待复核") {
        this.yjsc_btn_show = false; //一键生成
        this.gjjy_btn_show = true; //勾稽校验
        this.ywbhd_btn_show = true; //与外包核对
        this.qrfh_btn_show = true; //确认复核
        this.yjsb_btn_show = false; //一键上报
        this.offsetSpan = 21;
        this.spanSize = 3;
      } else if (tabLabel === "待报送") {
        this.yjsc_btn_show = false; //一键生成
        this.gjjy_btn_show = false; //勾稽校验
        this.ywbhd_btn_show = false; //与外包核对
        this.qrfh_btn_show = false; //确认复核
        this.yjsb_btn_show = true; //一键上报
        this.offsetSpan = 21;
        this.spanSize = 3;
      } else if (tabLabel === "已完成") {
        this.yjsc_btn_show = false; //一键生成
        this.gjjy_btn_show = false; //勾稽校验
        this.ywbhd_btn_show = false; //与外包核对
        this.qrfh_btn_show = false; //确认复核
        this.yjsb_btn_show = false; //一键上报
        this.offsetSpan = 22;
        this.spanSize = 2;
      }

      if (tabLabel === "全部") {
        this.formInline.statusReport = "";
      } else {
        this.formInline.statusReport = this.activeName2;
      }

      // this.changeReportType();

      this.onSubmit(true);
    },
    //列表选择
    handleSelectionChange(val) {
      this.tableMultipleSelection = val;
    },
    //排序
    handleSortChange(val) {
      // console.log(val);
      this.formInline.orderString = commonFun.orderByString(val);

      this.onSubmit(false);
    },
    czrzSortChange(val) {
      this.czrzOrderString = commonFun.orderByString(val);

      this.onSubmitCzrz(false);
    },
    //分页
    Pagination(val) {
      this.formInline.pageSize = val.limit; //页面条数
      this.formInline.pageNum = val.page; //页码
      this.onSubmit(false);
    },
    czrzPagination(val) {
      this.czrzPageSize = val.limit; //页面条数
      this.czrzPageNum = val.page; //页码
      this.onSubmitCzrz(false);
    },
    //查询
    onSubmit(flag) {
      this.tableLoading = true;
      // 消除没有值的参数
      if (flag) {
        this.formInline.pageNum = 1;
      }
      if (!this.initDate()) {
        this.tableLoading = false;
        return;
      }
      this.formInline.reportFrequency = this.activeName;
      let data = { ...this.formInline };
      if (data.fundCode) data["fundCode"] = data.fundCode.split("_")[0];
      let params = commonFun.parameterSrc(data);
      pageApi
        .getAnnDataSourceList(params)
        .then((response) => {
          if (response.data.status === 200) {
            this.tableData = response.data.data.list;
            // 页面总条数
            this.total = response.data.data.total;
            // 对 Table 进行重新布局。当 Table 或其祖先元素由隐藏切换为显示时，可能需要调用此方法
            this.$nextTick(() => {
              this.$refs.multipleTable.doLayout();
            });
          } else {
            this.tableData = [];
            this.total = 0;
            this.formInline.pageSize = 50;
            this.formInline.pageNum = 1;
          }
          this.tableLoading = false;
        })
        .catch(() => {
          this.tableData = [];
          this.total = 0;
          this.formInline.pageSize = 50;
          this.formInline.pageNum = 1;
          this.tableLoading = false;
        });
    },
    initDate() {
      let flag = this.activeName;
      if (flag === "W") {
        if (this.formInline.dateData) {
          let myDate = new Date(this.formInline.dateData);
          let weekDay = [
            "星期天",
            "星期一",
            "星期二",
            "星期三",
            "星期四",
            "星期五",
            "星期六",
          ];
          let value = weekDay[myDate.getDay()];
          // if (value != "星期五") {
          //   this.$message.closeAll();
          //   this.$message({
          //     message: "请选择星期五的日期",
          //     type: "warning",
          //   });
          //   return false;
          // }
        }
      } else if (flag === "M") {
        if (this.reportYear && !this.selectDate) {
          this.$message.closeAll();
          this.$message({
            message: "请选择对应的月份",
            type: "warning",
          });
          return false;
        } else if (!this.reportYear && this.selectDate) {
          this.$message.closeAll();
          this.$message({
            message: "请选择对应的年份",
            type: "warning",
          });
          return false;
        } else if (this.reportYear && this.selectDate) {
          this.initMonthDate(this.reportYear, this.selectDate);
        } else {
          this.formInline.dateData = "";
        }
      } else if (flag === "Q") {
        if (this.reportYear && !this.selectDate) {
          this.$message.closeAll();
          this.$message({
            message: "请选择对应的季度",
            type: "warning",
          });
          return false;
        } else if (!this.reportYear && this.selectDate) {
          this.$message.closeAll();
          this.$message({
            message: "请选择对应的年份",
            type: "warning",
          });
          return false;
        } else if (this.reportYear && this.selectDate) {
          let q = this.selectDate;
          let date = this.reportYear;
          if (q === "1") {
            date = date + "-03-31";
          } else if (q === "2") {
            date = date + "-06-30";
          } else if (q === "3") {
            date = date + "-09-30";
          } else if (q === "4") {
            date = date + "-12-31";
          }
          this.formInline.dateData = date;
        } else {
          this.formInline.dateData = '';
        }
      } else if (flag === "S") {
        if (this.reportYear) {
          this.formInline.dateData = this.reportYear + "-06-30";
        }else{
          this.formInline.dateData = '';
        }
      } else if (flag === "Y") {
        if (this.reportYear) {
          this.formInline.dateData = this.reportYear + "-12-31";
        }else{
          this.formInline.dateData = '';
        }
      }

      return true;
    },
    initMonthDate(year, m) {
      let date = year;
      if (m === "1") {
        date = date + "-01-31";
      } else if (m === "2") {
        date = date + "-03-01";
        let myDate = new Date(date);
        var time = myDate.getTime() - 24 * 60 * 60 * 1000;
        var yesterday = new Date(time);
        var month = yesterday.getMonth();
        var day = yesterday.getDate();
        date = year + "-02-" + day;
        // console.log(day);
      } else if (m === "3") {
        date = date + "-03-31";
      } else if (m === "4") {
        date = date + "-04-30";
      } else if (m === "5") {
        date = date + "-05-31";
      } else if (m === "6") {
        date = date + "-06-30";
      } else if (m === "7") {
        date = date + "-07-31";
      } else if (m === "8") {
        date = date + "-08-31";
      } else if (m === "9") {
        date = date + "-09-30";
      } else if (m === "10") {
        date = date + "-10-31";
      } else if (m === "11") {
        date = date + "-11-30";
      } else if (m === "12") {
        date = date + "-12-31";
      }
      this.formInline.dateData = date;
    },
    //编辑
    editData(row) {
      if (row.dateData) {
        this.currencyReportPageData.dataDate = row.dateData;
        this.currencyReportPageData.endDate = row.dateData;
      }
      if (row.reportId) {
        this.currencyReportPageData.reportCode = row.reportId;
      }
      if (row.id) {
        this.currencyReportPageData.recordId = row.id;
      }
      if (row.fundType) {
        this.currencyReportPageData.fundType = row.fundType;
        //临时给相关报表使用
        this.currencyReportPageData.typeIn = row.fundType;
      }
      if (row.fundCode) {
        this.currencyReportPageData.fundCode = row.fundCode;
      } else {
        this.currencyReportPageData.fundCode = "";
      }

      if (row.reportCode == "R00005") {
        this.dialogTitle = row.reportName;
        this.A1005Dialog = true;
        this.A1005_show = true;
      } else {
        this.annExcelPage_show = false;
        this.annXmlPage_show = false;
        this.annTxtPage_show = false;
        this.annLogPage_show = false;
        this.currencyReportPage_show = true;
        this.czrzDialog = true;
        this.dialogTitle = row.reportName;
      }

      // console.log('父组件-编辑',this.currencyReportPageData);
      //  新更改---
      // this.currenc_new_show = true
      // this.$nextTick(() => {
      //   this.$refs.currenc_new_ref.init(row)
      // })
    },
    // 值返回
    currencValue(data) {
      // console.log('返回值', data)
      this.currenc_new_show = false;
    },
    //一键生成
    yjsc() {
      if (this.tableMultipleSelection.length === 0) {
        this.$message.closeAll();
        this.$message({
          message: "请选择数据",
          type: "warning",
        });
        return;
      }

      let arr = this.tableMultipleSelection;
      let formData = new FormData(); //  用FormData存放上传文件
      for (let i = 0; i < arr.length; i++) {
        formData.append("ids", arr[i].id);
      }

      let confirm = false;
      for (let i = 0; i < arr.length; i++) {
        if (arr[i].statusFileCreate == "1") {
          confirm = true;
          break;
        }
      }
      if (confirm) {
        this.$confirm("报表已存在，是否需要重新生成?", "提示", {
          confirmButtonText: "是",
          cancelButtonText: "否",
          type: "warning",
          confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
        })
          .then(() => {
            this.yjsc_(formData);
          })
          .catch(() => {
            this.$message({
              type: "info",
              message: "已取消操作",
            });
          });
      } else {
        this.yjsc_(formData);
      }

      //params.models = arr;
      //  pageApi.yjscData(formData).then(response => {
      //     if(response.data.status === 200){
      //         this.$message.closeAll()
      //         this.$message({
      //             message: '操作成功',
      //             type: 'success'
      //          });
      //          // 刷新树列表
      //          this.onSubmit(false);
      //     }
      //    else{
      //        this.$message.closeAll()
      //        this.$message({
      //           message: response.data.message || '操作失败',
      //           type: 'warning'
      //        });
      //    }
      //  }).catch(() => {
      //  // 关闭移动指标弹框
      //      this.$message.closeAll()
      //      this.$message({
      //         message: '操作失败',
      //         type: 'warning'
      //      });
      //  })
    },
    yjsc_(formData) {
      this.btn_laoding = true;
      pageApi
        .yjscData(formData)
        .then((response) => {
          this.btn_laoding = false;
          if (response.data.status === 200) {
            this.$message.closeAll();
            this.$message({
              message: "操作成功",
              type: "success",
            });
            // 刷新树列表
            this.onSubmit(false);
          } else {
            this.$message.closeAll();
            this.$message({
              message: response.data.message || "操作失败",
              type: "warning",
            });
          }
        })
        .catch(() => {
          this.btn_laoding = false;
          // 关闭移动指标弹框
          this.$message.closeAll();
          this.$message({
            message: "操作失败",
            type: "warning",
          });
        });
    },
    //勾稽校验
    gjjy() {
      if (this.tableMultipleSelection.length === 0) {
        this.$message.closeAll();
        this.$message({
          message: "请选择数据",
          type: "warning",
        });
        return;
      }

      let arr = this.tableMultipleSelection;
      let formData = new FormData(); //  用FormData存放上传文件
      for (let i = 0; i < arr.length; i++) {
        formData.append("ids", arr[i].id);
      }

      //params.models = arr;
      this.btn_laoding = true;
      pageApi
        .gjjyData(formData)
        .then((response) => {
          this.btn_laoding = false;
          if (response.data.status === 200) {
            this.$message.closeAll();
            this.$message({
              message: "操作成功",
              type: "success",
            });
            // 刷新树列表
            this.onSubmit(false);
          } else {
            this.$message.closeAll();
            this.$message({
              message: response.data.message || "操作失败",
              type: "warning",
            });
          }
        })
        .catch(() => {
          this.btn_laoding = false;
          // 关闭移动指标弹框
          this.$message.closeAll();
          this.$message({
            message: "操作失败",
            type: "warning",
          });
        });
    },
    //与外包核对
    ywbhd() {
      if (this.tableMultipleSelection.length === 0) {
        this.$message.closeAll();
        this.$message({
          message: "请选择数据",
          type: "warning",
        });
        return;
      }

      let arr = this.tableMultipleSelection;
      let formData = new FormData(); //  用FormData存放上传文件
      for (let i = 0; i < arr.length; i++) {
        formData.append("ids", arr[i].id);
      }
      //params.models = arr;
      this.btn_laoding = true;
      pageApi
        .ywbhdData(formData)
        .then((response) => {
          this.btn_laoding = false;
          if (response.data.status === 200) {
            this.$message.closeAll();
            this.$message({
              message: "操作成功",
              type: "success",
            });
            // 刷新树列表
            this.onSubmit(false);
          } else {
            this.$message.closeAll();
            this.$message({
              message: response.data.message || "操作失败",
              type: "warning",
            });
          }
        })
        .catch(() => {
          this.btn_laoding = false;
          // 关闭移动指标弹框
          this.$message.closeAll();
          this.$message({
            message: "操作失败",
            type: "warning",
          });
        });
    },
    //确认复核
    qrfh() {
      if (this.tableMultipleSelection.length === 0) {
        this.$message.closeAll();
        this.$message({
          message: "请选择数据",
          type: "warning",
        });
        return;
      }

      this.countDialog = true;
      this.formCount.confirmOpinion = "";
    },
    reportConfirmCancel(row) {
      this.reportRecordId = row.id;
      this.reportConfirmCancelDialog = true;
      this.formCount.confirmCancelOpinion = "";
    },
    countSubmit(formName) {
      var self = this;
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let arr = this.tableMultipleSelection;
          let formData = new FormData(); //  用FormData存放上传文件
          for (let i = 0; i < arr.length; i++) {
            formData.append("ids", arr[i].id);
          }
          formData.append("confirmOpinion", this.formCount.confirmOpinion);
          //params.models = arr;
          this.btn_laoding = true;
          pageApi
            .qrfhData(formData)
            .then((response) => {
              this.btn_laoding = false;
              if (response.data.status === 200) {
                this.$message.closeAll();
                this.$message({
                  message: "操作成功",
                  type: "success",
                });
                this.countDialog = false;
                // 刷新树列表
                this.onSubmit(false);
              } else {
                this.$message.closeAll();
                this.$message({
                  message: response.data.message || "操作失败",
                  type: "warning",
                });
              }
            })
            .catch(() => {
              this.btn_laoding = false;
              // 关闭移动指标弹框
              this.$message.closeAll();
              this.$message({
                message: "操作失败",
                type: "warning",
              });
            });
        } else {
          return false;
        }
      });
    },

    reportConfirmCancelSubmit(formName) {
      var self = this;
      let formData = new FormData();

      this.$refs[formName].validate((valid) => {
        if (valid) {
          formData.append("ids", this.reportRecordId);
          formData.append(
            "confirmOpinion",
            this.formCount.confirmCancelOpinion
          );
          this.btn_laoding = true;
          pageApi
            .reportConfirmCancelData(formData)
            .then((response) => {
              this.btn_laoding = false;
              if (response.data.status === 200) {
                this.$message.closeAll();
                this.$message({
                  message: "操作成功",
                  type: "success",
                });
                this.reportConfirmCancelDialog = false;
                // 刷新树列表
                this.onSubmit(false);
              } else {
                this.$message.closeAll();
                this.$message({
                  message: response.data.message || "操作失败",
                  type: "warning",
                });
              }
            })
            .catch(() => {
              this.btn_laoding = false;
              // 关闭移动指标弹框
              this.$message.closeAll();
              this.$message({
                message: "操作失败",
                type: "warning",
              });
            });
        } else {
          return false;
        }
      });
    },
    //一键上报
    yjsb() {
      if (this.tableMultipleSelection.length === 0) {
        this.$message.closeAll();
        this.$message({
          message: "请选择数据",
          type: "warning",
        });
        return;
      }

      let arr = this.tableMultipleSelection;

      let formData = new FormData(); //  用FormData存放上传文件
      for (let i = 0; i < arr.length; i++) {
        formData.append("ids", arr[i].id);
      }
      //params.models = arr;
      this.btn_laoding = true;
      pageApi
        .yjsbData(formData)
        .then((response) => {
          this.btn_laoding = false;
          if (response.data.status === 200) {
            this.$message.closeAll();
            this.$message({
              message: "操作成功",
              type: "success",
            });
            // 刷新树列表
            this.onSubmit(false);
          } else {
            this.$message.closeAll();
            this.$message({
              message: response.data.message || "操作失败",
              type: "warning",
            });
          }
        })
        .catch(() => {
          this.btn_laoding = false;
          // 关闭移动指标弹框
          this.$message.closeAll();
          this.$message({
            message: "操作失败",
            type: "warning",
          });
        });
    },
    //下载报表
    downloadReport() {
      if (this.tableMultipleSelection.length === 0) {
        this.$message.closeAll();
        this.$message({
          message: "请选择数据",
          type: "warning",
        });
        return;
      }
      this.btn_laoding = true;
      setTimeout(() => {
        this.btn_laoding = false;
      }, 1000);
      let arr = this.tableMultipleSelection;

      let params = { ids: [], token: this.$store.getters.token }; //  token
      for (let i = 0; i < arr.length; i++) {
        params["ids"].push(arr[i].id);
      }

      //    // 表头名
      // params["exportAliasName"] = '年份,组合代码,报告类型,父标签名称,标签名称,标签值,导入时间';
      // // 导出文件名
      // params["exportFileName"] = 'XBRL.xls';
      // // 数据格式化
      // params["exportFormat"] = 'string,string,string,string,string,string,string';
      // // 表头属性名
      // params["exportPoName"] = 'rptYear,combinedId,rptType,parentElementName,elementName,elementValue,importDate';
      // // 表标题
      // params["exportTitle"] = 'XBRL导出数据';
      // 请求地址
      let action = store.state.setting.baseApi + "api/annreport/v1.0/download";

      commonFun.formDownloadFile(params, action, "POST");
    },
    // 校验明细
    jymx(row) {
      this.PageData.recordId = row.id;
      this.czrzDialog = true;
      this.dialogTitle = "校验明细";
      this.annExcelPage_show = false;
      this.annXmlPage_show = false;
      this.annTxtPage_show = false;
      this.annLogPage_show = false;
      this.currencyReportPage_show = false;
      this.checkDetailPage_show = true;
    },
    //核对明细
    hdmx(row) {
      this.PageData.recordId = row.id;

      let reportFileType = row.reportFileType;
      if (reportFileType) {
        if (reportFileType === "EXCEL") {
          this.annExcelPage_show = true;
          this.annXmlPage_show = false;
          this.annTxtPage_show = false;
          this.annLogPage_show = false;
          this.currencyReportPage_show = false;

          this.dialogTitle = "Excel核对页面";
        } else if (reportFileType === "XML") {
          this.annExcelPage_show = false;
          this.annXmlPage_show = true;
          this.annTxtPage_show = false;
          this.annLogPage_show = false;
          this.currencyReportPage_show = false;
          this.dialogTitle = "XML核对页面";
        } else if (reportFileType === "TXT") {
          this.annExcelPage_show = false;
          this.annXmlPage_show = false;
          this.annTxtPage_show = true;
          this.annLogPage_show = false;
          this.currencyReportPage_show = false;
          this.dialogTitle = "TXT核对页面";
        }
        this.czrzDialog = true;
        this.dialogTitle = row.reportName;
      }
    },
    //操作日志
    czrz(row) {
      this.PageData.recordId = row.id;
      this.czrzDialog = true;
      this.dialogTitle = "操作日志";
      this.annExcelPage_show = false;
      this.annXmlPage_show = false;
      this.annTxtPage_show = false;
      this.annLogPage_show = true;
      this.currencyReportPage_show = false;

      //this.onSubmitCzrz();
    },
    onSubmitCzrz(flag) {
      this.czrzTableLoading = true;
      // 消除没有值的参数
      if (flag) {
        this.czrzPageNum = 1;
      }

      //let params = commonFun.parameterSrc(this.formInline);
      let params = {};
      params.pageNum = this.czrzPageNum;
      params.pageSize = this.czrzPageSize;
      params.orderString = this.czrzOrderString;
      params = commonFun.parameterSrc(params);

      pageApi
        .getDataLogSourceList(params)
        .then((response) => {
          if (response.data.status === 200) {
            this.czrzTableData = response.data.data.list;
            // 页面总条数
            this.czrzTotal = response.data.data.total;
          } else {
            this.czrzTableData = [];
            this.czrzTotal = 0;
            this.czrzPageSize = 50;
            this.czrzPageNum = 1;
          }
          this.czrzTableLoading = false;
        })
        .catch(() => {
          this.czrzTableData = [];
          this.czrzTotal = 0;
          this.czrzPageSize = 50;
          this.czrzPageNum = 1;
          this.czrzTableLoading = false;
        });
    },
    //报告类型change事件
    reportTypeChange(val) {
      this.reportYear = "";
      this.selectDate = "";
      if (val === "M") {
        this.reportTypeOther_show = true;
        this.reportTypeOther_year = true;
        this.reportTypeOther_day = false;
        this.reportTypeOther_weak = false;

        this.reportTypeArr2 = this.months;
      } else if (val === "Y" || val === "S") {
        this.reportTypeOther_show = false;
        this.reportTypeOther_year = true;
        this.reportTypeOther_day = false;
        this.reportTypeOther_weak = false;
        this.reportTypeArr2 = [];
      } else if (val === "Q") {
        this.reportTypeOther_show = true;
        this.reportTypeOther_year = true;
        this.reportTypeOther_day = false;
        this.reportTypeOther_weak = false;
        this.reportTypeArr2 = this.quarters;
      } else if (val === "D" || val === "All") {
        this.reportTypeOther_show = false;
        this.reportTypeOther_year = false;
        this.reportTypeOther_day = true;
        this.reportTypeOther_weak = false;
      } else if (val === "W") {
        this.reportTypeOther_show = false;
        this.reportTypeOther_year = false;
        this.reportTypeOther_day = true;
        //this.reportTypeOther_day = true;
      }

      if (val === "All" || val === "Q" || val === "S" || val === "Y") {
        this.fundColumnShowFlag = true;
      } else {
        this.fundColumnShowFlag = false;
      }
    },
    //获取Selects
    getSelects(val) {
      let params = val;
      pageApi
        .getSelects(params)
        .then((res) => {
          let self = this;
          if (res.data.message === "success") {
            if (val === "fundinfo_fundState") {
              this.proStatusArr = res.data.data;
              let arr = res.data.data;
              for (let i = 0; i < arr.length; i++) {
                this.fundStatusArr[arr[i].dimCde] = arr[i].dimNme;
              }
            }
            if (val === "fundann_submitComp") {
              let arr = res.data.data;
              let arr1 = [];
              let arr2 = [];
              for (let i = 0; i < arr.length; i++) {
                arr1[arr[i].dimCde] = arr[i].dimNme;
              }
              arr2 = arr.filter((item) => {
                return item.dimCde != "XBRL";
              });
              this.name5Arr = arr2;
              this.name5Obj = arr1;
              if(this.name5Arr.length){
                this.formInline.reportType = this.name5Arr[0].dimCde;
              }
              let timestamp = res.data.timestamp;
              this.nowDate = commonFun.yyr_timestampToTime(timestamp) || '';
              this.formInline.dateSubmitFinal = this.nowDate;
              this.onSubmit(true);
            }
          } else {
            this.$message.closeAll();
            this.$message.error("初始化数据失败");
          }
        })
        .catch((err) => {
          console.log(err);
          this.$message.closeAll();
          this.$message.error("初始化数据失败");
        });
    },
    getProductsAll() {
      pageApi
        .getProductsAll()
        .then((res) => {
          let self = this;
          if (res.data.message === "success") {
            let arr = res.data.data;
            this.accountCodes = [];
            for (let i = 0; i < arr.length; i++) {
              let obj = {};
              obj.value = arr[i].fundCode;
              obj.name = arr[i].fundName + " (" + arr[i].fundCode + ")";
              this.accountCodes.push(obj);
            }
          } else {
            this.accountCodes = [];
            this.$message.closeAll();
            this.$message.error("初始化数据失败");
          }
        })
        .catch(() => {
          this.accountCodes = [];
          this.$message.closeAll();
          this.$message.error("初始化数据失败");
        });
    },
    //数据字典转换
    dataStatus(statusCode, flag) {
      if (flag === "1") {
        return this.fundStatusArr[statusCode];
      } else if (flag === "2") {
        return this.name5Obj[statusCode];
      }
    },
    //关闭dialog
    handleClose(done) {
      done();
      this.annExcelPage_show = false;
      this.annXmlPage_show = false;
      this.annTxtPage_show = false;
      this.annLogPage_show = false;
      this.currencyReportPage_show = false;
      this.checkDetailPage_show = false;
    },
    // A1005关闭
    A1005handleClose(done) {
      done();
      // this.A1005Dialog = false;
      this.A1005_show = false;
    },
    fundColumnShowFlagChange(data) {
      // console.log(data);
      this.$nextTick(() => {
        this.$refs.multipleTable.doLayout();
      });
    },
  },
};
</script>
<style lang='scss'>
.ann_report_out {
  .currency_report_old_form {
    .el-form-item {
      margin-bottom: 10px !important;
      .el-form-item__content {
        .el-input {
          width: 160px !important;
        }
        .el-date-editor {
          width: 160px !important;
        }
        .el-select {
          width: 160px !important;
        }
      }
    }
  }
}
</style>
<style>
.xbrlCzrzListWidth_ {
  width: 75% !important;
  margin-top: 5vh !important;
  /* max-height: 90%;
  overflow: hidden;
  overflow-y: auto; */
}
.qrfuListWidth {
  width: 70% !important;
}
.el-dialog .el-form {
  width: 100% !important;
}
</style>

<style rel="stylesheet/scss" lang="scss" scoped>
.ann_report_out {
  height: 100%;
}
</style>

<template>
  <div class="fundInfoListPage">
    <!-- 搜索 -->
    <el-form :inline="true" ref="formQuery" :model="formQuery" :rules="rules" class="formQuery pdt5">
      <el-row>
        <el-col :span="16">
          <div class="grid-content bg-purple">
            <el-form-item :label-width="formLabelWidth" prop="fundCode">
              <span class="item-label" slot="label">产品代码</span>
              <el-input v-model.trim="formQuery.fundCode" clearable placeholder="请输入产品代码" size="small"></el-input>
            </el-form-item>
            <el-form-item label="" :label-width="formLabelWidth" prop="fundName">
              <span class="item-label" slot="label">产品名称</span>
              <el-input v-model.trim="formQuery.fundName" clearable placeholder="请输入产品名称" size="small"></el-input>
            </el-form-item>

            <el-form-item label="" :label-width="formLabelWidth" prop="ifEquity">
              <span class="item-label" slot="label">是否含权</span>
              <el-select v-model="formQuery.ifEquity" placeholder="请选择" size="small">
                <el-option label="是" value="1"></el-option>
                <el-option label="否" value="0"></el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="" :label-width="formLabelWidth" prop="annuityType">
              <span class="item-label" slot="label">组合类型</span>
              <el-select multiple v-model="formQuery.annuityType" placeholder="请选择" size="small">
                <template v-for="(item, index) in annuityTypeArrs">
                  <el-option :key="item.dimCde" :label="item.dimNme" :value="item.dimCde"></el-option>
                </template>
              </el-select>
            </el-form-item>

            <el-form-item label="" :label-width="formLabelWidth" prop="fofInvestment">
              <span class="item-label" slot="label">是否计划</span>
              <el-select v-model="formQuery.isPlan" placeholder="请选择" size="small">
                <el-option label="是" value="1"></el-option>
                <el-option label="否" value="0"></el-option>
              </el-select>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="grid-content bg-purple-light">
            <el-form-item class="search_button_com">
              <el-button type="primary" :disabled="btnDisabled" @click="onQuery(1)" class="mb5" icon="el-icon-search">查询</el-button>
              <el-button type="primary" plain @click="addData">新增</el-button>
              <el-button type="primary" plain @click="resetForm('formQuery')">重置</el-button>
              <el-button @click="downloadTableExcel" type="primary" plain :icon="downLoadIcon" :disabled="isDisabled" class="mb5">{{ downLoadText }}</el-button>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
    </el-form>
    <div class="picc_forms_table_title">
      <div class="picc_forms_table_title_line"></div>
      <div class="title-style">产品信息维护</div>
    </div>
    <el-table
      :data="tableData"
      :default-sort="{ prop: 'fundName', order: 'descending' }"
      border
      :row-class-name="xxxTableRowClassName"
      @sort-change="handleSortChange"
      v-loading="tableLoading"
      :header-row-style="this.$fun.headerRowStyle"
      :cell-style="this.$fun.cellStyle"
      style="width: 100%"
    >
      <el-table-column fixed="left" type="index" label="序号" width="60" header-align="center"></el-table-column>

      <el-table-column
        prop="fundCode"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="产品代码"
        min-width="100"
        header-align="center"
        fixed="left"
      ></el-table-column>
      <el-table-column
        prop="fundName"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="产品名称"
        min-width="250"
        header-align="center"
        fixed="left"
      ></el-table-column>

      <el-table-column
        prop="shortFundname"
        sortable="shortFundname"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="产品简称"
        min-width="100"
        header-align="center"
      ></el-table-column>
      <el-table-column
        prop="nameGlr"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="产品管理人"
        min-width="120"
        header-align="center"
      ></el-table-column>
      <el-table-column
        prop="createDate"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="成立日期"
        min-width="100"
        header-align="center"
      ></el-table-column>

      <el-table-column
        prop="isEnd"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="产品运行状态"
        min-width="140"
        header-align="center"
      ></el-table-column>

      <el-table-column
        prop="annuityType"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="产品类型"
        min-width="100"
        header-align="center"
      ></el-table-column>

      <el-table-column
        prop="glfRatio"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="管理费(%)"
        min-width="120"
        header-align="center"
        align="right"
      >
        <!-- <template slot-scope="scope">
          <span>{{ scope.row.glfRatio | baifenlvS }}</span>
        </template>-->
      </el-table-column>
      <el-table-column
        prop="performanceFee"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="业绩报酬(%)"
        min-width="140"
        header-align="center"
        align="right"
      ></el-table-column>

      <el-table-column
        prop="performanceJt"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="业绩报酬计提方式"
        min-width="160"
        header-align="center"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="source"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="数据来源"
        min-width="100"
        header-align="center"
        align="center"
      ></el-table-column>
      <el-table-column
        prop="gzFrequency"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="净值披露频率"
        min-width="140"
        header-align="center"
        align="center"
      ></el-table-column>

      <el-table-column
        prop="fCompanyName"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="所属机构"
        min-width="100"
        header-align="center"
        align="left"
      ></el-table-column>
      <!--      <el-table-column-->
      <!--        prop="isAcount"-->
      <!--        sortable="custom"-->
      <!--        :sort-orders="['ascending', 'descending']"-->
      <!--        show-overflow-tooltip-->
      <!--        label="所属计划"-->
      <!--        min-width="130"-->
      <!--        header-align="center"-->
      <!--        align="left"-->
      <!--        v-if='isShows'-->

      <!--      ></el-table-column>-->

      <el-table-column label="操作" fixed="right" min-width="280" align="center">
        <template slot-scope="scope">
          <el-button type="primary" size="small" @click="editData(scope.row)">编辑</el-button>
          <!--<router-link :to="{path:'/businessOverview2/provinceCenterBaisc',query: {fundcode:scope.row.fundCode}}" >
            <el-button type="primary" size="small" >编辑</el-button>
          </router-link>
          <el-button type="primary" size="small" @click="fundFileDialog(scope.row)">附件</el-button>-->
          <el-button type="primary" plain size="small" @click="delData(scope.row)">删除</el-button>
          <!--<el-button type="danger" plain size="small" @click="docManage(scope.row)">附件</el-button>-->
        </template>
      </el-table-column>
    </el-table>

    <Pagination :total="total" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination"></Pagination>
    <el-row></el-row>
    <el-dialog title="产品信息维护" center :visible.sync="dialogMask" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox">
          <div class="forms_management_box">
            <el-form :inline="true" ref="formDialog" :model="formDialog" :rules="dialogRules">
              <el-tabs v-model="activeName">
                <el-tab-pane label="基本信息" lazy name="baseInfo">
                  <div class="forms_table_title">
                    <i class="el-icon-s-data"></i>
                    基本信息
                  </div>
                  <el-form-item label="" prop="fundCode" :label-width="formLabelWidth" class="mb20">
                    <span class="item-label" slot="label">产品代码</span>
                    <el-input v-model.trim="formDialog.fundCode" clearable placeholder="请输入" size="small"></el-input>
                  </el-form-item>
                  <el-form-item label="" prop="fundName" :label-width="formLabelWidth" class="mb20">
                    <span class="item-label" slot="label">产品名称</span>
                    <el-input v-model.trim="formDialog.fundName" style="width: 300px !important" clearable placeholder="请输入" size="small"></el-input>
                  </el-form-item>
                  <el-form-item label="" prop="shortFundname" :label-width="formLabelWidth" class="mb20">
                    <span class="item-label" slot="label">产品简称</span>
                    <el-input v-model.trim="formDialog.shortFundname" style="width: 300px !important" clearable placeholder="请输入" size="small"></el-input>
                  </el-form-item>
                  <el-form-item label="" prop="stbyCode" :label-width="formLabelWidth" class="mb20">
                    <span class="item-label" slot="label">辅助代码</span>
                    <el-input v-model.trim="formDialog.stbyCode" clearable placeholder="请输入" size="small"></el-input>
                  </el-form-item>
                  <el-form-item label="" prop="stbyFundname" :label-width="formLabelWidth" class="mb20">
                    <span class="item-label" slot="label">辅助名称</span>
                    <el-input v-model.trim="formDialog.stbyFundname" clearable placeholder="请输入" size="small"></el-input>
                  </el-form-item>
                  <el-form-item label="" prop="fundfCode" :label-width="formLabelWidth" class="mb20">
                    <span class="item-label" slot="label">人社部代码</span>
                    <el-input v-model.trim="formDialog.fundfCode" clearable placeholder="请输入" size="small"></el-input>
                  </el-form-item>

                  <el-form-item label="" prop="nameGlr" :label-width="formLabelWidth" class="mb20">
                    <span class="item-label" slot="label">管理人</span>
                    <el-input v-model.trim="formDialog.nameGlr" clearable placeholder="请输入" size="small"></el-input>
                  </el-form-item>
                  <el-form-item label="" prop="vcCompanyName" :label-width="formLabelWidth" class="mb20">
                    <span class="item-label" slot="label">投资管理部门</span>
                    <el-select v-model="formDialog.vcCompanyName" filterable clearable placeholder="请选择" size="small">
                      <el-option v-for="item in vcCompanyNameArrs" :key="item.deptId" :label="item.deptName" :disabled="item.deptId === '*'" :value="item.deptId"></el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="" prop="companyId" :label-width="formLabelWidth" class="mb20">
                    <span class="item-label" slot="label">所属机构</span>
                    <el-select v-model="formDialog.companyId" filterable clearable placeholder="请选择" size="small">
                      <el-option v-for="item in companyIdArrs" :key="item.deptId" :label="item.deptName" :disabled="item.deptId === '*'" :value="item.deptId"></el-option>
                    </el-select>
                  </el-form-item>
                  <div class="forms_table_title">
                    <i class="el-icon-s-data"></i>
                    运行信息
                  </div>
                  <el-form-item label="" prop="setAmount" :label-width="formLabelWidth" class="mb20">
                    <span class="item-label" slot="label">设立金额(元)</span>
                    <el-input v-model.trim="formDialog.setAmount" clearable placeholder="请输入" size="small"></el-input>
                  </el-form-item>
                  <el-form-item label="" prop="createDate" :label-width="formLabelWidth" class="mb20">
                    <span class="item-label" slot="label">成立日期</span>
                    <el-date-picker style="width: 174px" v-model="formDialog.createDate" type="date" size="small" value-format="yyyy-MM-dd" placeholder="选择日期"></el-date-picker>
                  </el-form-item>

                  <el-form-item label="" prop="isEnd" :label-width="formLabelWidth" class="mb20">
                    <span class="item-label" slot="label">产品运行状态</span>
                    <el-select v-model="formDialog.isEnd" filterable clearable placeholder="请选择" size="small">
                      <el-option v-for="item in isEndArrs" :key="item.dimCde" :label="item.dimNme" :disabled="item.dimCde === '*'" :value="item.dimCde"></el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="" prop="yieldMethod" :label-width="formLabelWidth" class="mb20">
                    <span class="item-label" slot="label">净值增长率算法</span>
                    <el-select v-model="formDialog.yieldMethod" filterable clearable placeholder="请选择" size="small">
                      <el-option v-for="item in yieldMethodArrs" :key="item.dimCde" :label="item.dimNme" :disabled="item.dimCde === '*'" :value="item.dimCde"></el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="" prop="gzFrequency" :label-width="formLabelWidth" class="mb20">
                    <span class="item-label" slot="label">净值披露频率</span>
                    <el-select v-model="formDialog.gzFrequency" filterable clearable placeholder="请选择" size="small">
                      <el-option v-for="item in gzFrequencyArrs" :key="item.dimCde" :label="item.dimNme" :disabled="item.dimCde === '*'" :value="item.dimCde"></el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="" prop="source" :label-width="formLabelWidth" class="mb20">
                    <span class="item-label" slot="label">数据来源</span>
                    <el-select v-model="formDialog.source" filterable clearable placeholder="请选择" size="small">
                      <el-option v-for="item in sourceArrs" :key="item.dimCde" :label="item.dimNme" :disabled="item.dimCde === '*'" :value="item.dimCde"></el-option>
                    </el-select>
                  </el-form-item>
                  <div class="forms_table_title">
                    <i class="el-icon-s-data"></i>
                    费率
                  </div>
                  <el-form-item label="" prop="baseCurrency" :label-width="formLabelWidth" class="mb20">
                    <span class="item-label" slot="label">基础货币</span>
                    <el-select v-model="formDialog.baseCurrency" filterable clearable placeholder="请选择" size="small">
                      <el-option v-for="item in baseCurrencyArrs" :key="item.dimCde" :label="item.dimNme" :disabled="item.dimCde === '*'" :value="item.dimCde"></el-option>
                    </el-select>
                  </el-form-item>

                  <el-form-item label="" prop="glfRatio" :label-width="formLabelWidth" class="mb20">
                    <span class="item-label" slot="label">管理费(%)</span>
                    <el-input v-model.trim="formDialog.glfRatio" clearable placeholder="请输入" size="small"></el-input>
                  </el-form-item>
                  <el-form-item label="" prop="performanceFee" :label-width="formLabelWidth" class="mb20">
                    <span class="item-label" slot="label">业绩报酬(%)</span>
                    <el-input v-model.trim="formDialog.performanceFee" clearable placeholder="请输入" size="small"></el-input>
                  </el-form-item>

                  <el-form-item label="" prop="performanceJt" :label-width="formLabelWidth" class="mb20">
                    <span class="item-label" slot="label">业绩报酬计提方式</span>
                    <el-select v-model="formDialog.performanceJt" filterable clearable placeholder="请选择" size="small">
                      <el-option v-for="item in performanceJtArrs" :key="item.dimCde" :label="item.dimNme" :disabled="item.dimCde === '*'" :value="item.dimCde"></el-option>
                    </el-select>
                  </el-form-item>
                  <div class="forms_table_title">
                    <i class="el-icon-s-data"></i>
                    分类信息
                  </div>
                  <el-form-item label="" prop="typeIn" :label-width="formLabelWidth" class="mb20">
                    <span class="item-label" slot="label">产品类型</span>
                    <el-select v-model="formDialog.annuityType" filterable clearable placeholder="请选择" size="small">
                      <el-option v-for="item in annuityTypeArrs" :key="item.dimCde" :label="item.dimNme" :disabled="item.dimCde === '*'" :value="item.dimCde"></el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="" prop="ifAcount" :label-width="formLabelWidth" class="mb20">
                    <span class="item-label" slot="label">计划分类</span>
                    <el-select v-model="formDialog.ifAcount" filterable clearable placeholder="请选择" size="small">
                      <el-option v-for="item in ifAcountArrs" :key="item.dimCde" :label="item.dimNme" :disabled="item.dimCde === '*'" :value="item.dimCde"></el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="" prop="ifEquity" :label-width="formLabelWidth" class="mb20">
                    <span class="item-label" slot="label">是否含权</span>
                    <el-select v-model="formDialog.ifEquity" filterable clearable placeholder="请选择" size="small">
                      <el-option label="是" value="1"></el-option>
                      <el-option label="否" value="0"></el-option>
                    </el-select>
                  </el-form-item>
                  <!--                <el-form-item label="" prop="isPlan" :label-width="formLabelWidth" class="mb20"><span class="item-label" slot="label">是否计划</span>-->
                  <!--                  <el-select-->
                  <!--                    v-model="formDialog.isPlan"-->
                  <!--                    filterable-->
                  <!--                    clearable-->
                  <!--                    placeholder="请选择"-->
                  <!--                    size="small"-->

                  <!--                  >-->
                  <!--                    <el-option label="是" value="1" ></el-option>-->
                  <!--                    <el-option label="否" value="0" ></el-option>-->
                  <!--                  </el-select>-->
                  <!--                </el-form-item>-->
                  <!--                <el-form-item label="" prop="isAcount" :label-width="formLabelWidth" class="mb20" v-if='isShow'><span class="item-label" slot="label" >所属计划</span>-->
                  <!--                  <el-input v-model.trim="formDialog.isAcount" clearable placeholder="请输入" size="small"></el-input>-->
                  <!--                </el-form-item>-->
                </el-tab-pane>
              </el-tabs>
            </el-form>
            <div class="common_bottom_height"></div>
          </div>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="dialogMask = false">取 消</el-button>
        <el-button type="primary" size="small" :loading="dealLoading" @click="dealData">确 定</el-button>
      </div>
    </el-dialog>
    <el-dialog title="历史记录" center :visible.sync="dialogMask_history" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox">
          <div class="forms_management_box">
            <el-table :data="historyList" :default-sort="{ prop: '', order: '' }" border @sort-change="handleSortChange" v-loading="tableLoading_history" style="width: 100%">
              <el-table-column fixed="left" type="index" label="序号" width="60" header-align="center"></el-table-column>
              <el-table-column
                prop="manageName"
                sortable="custom"
                :sort-orders="['ascending', 'descending']"
                show-overflow-tooltip
                label="姓名"
                min-width="120"
                header-align="center"
              ></el-table-column>
              <el-table-column
                prop="accessionDate"
                sortable="custom"
                :sort-orders="['ascending', 'descending']"
                show-overflow-tooltip
                label="上任日期"
                min-width="100"
                header-align="center"
              ></el-table-column>
              <el-table-column
                prop="dimissionDate"
                sortable="custom"
                :sort-orders="['ascending', 'descending']"
                show-overflow-tooltip
                label="离任日期"
                min-width="120"
                header-align="center"
              ></el-table-column>
            </el-table>
            <Pagination :total="total_hist" :limit="formQuery_hist.pageSize" :page="formQuery_hist.pageNum" @pagination="pagination_hist"></Pagination>
          </div>
        </el-main>
      </el-container>
    </el-dialog>
    <el-dialog title="附件" center customClass="customWidth" :visible.sync="dialogMask_fundFile" :close-on-click-modal="false">
      <fundFilePage ref="fundFilePage" :fundData="fundData"></fundFilePage>
    </el-dialog>
  </div>
</template>

<script type="text/ecmascript-6">
import { FILE_URL } from '@/utils/request'
import Pagination from "@/components/NewPagination";
import commonApi from "@/api/common";
import fundInfoApi from "@/api/dataManage/fundInfoApi";
import { getToken } from '@/utils/auth'
import investmentManagerApi from '@/api/managementView/New_investmentManager'
import fundInvestManagerApi from '@/api/dataManage/fundInvestManager'
import customerManagerApi from '@/api/dataManage/customerManager'
import fundFilePage from '@/views/dataManage/fundFilePage'

export default {
  components: {
    Pagination,
    fundFilePage,
  },
  name: "dataManage_fundInfoListPage",
  data() {
    return {
      //判断是否显示所属计划
      isShow: false,
      isShows: false,
      // 查询参数
      formQuery: {
        // 产品代码
        fundCode: "",
        // 产品名称
        fundName: "",
        // 产品类型
        typeIn: [],
        // 是否权益
        ifEquity: "",
        // 外部基金
        isOuterFund: "",
        //是否计划
        isPlan: "0",
        //计划分类
        ifAcount: [],
        // 年金类型
        annuityType: [],
        // 产品投资类型
        productInvestmentType: [],
        // 产品类型
        fofInvestment: "",
        // 产品类型
        isRecommendPool: "",

        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10,
        //排序方式
        orderBy : 'createDate desc nulls last'
      },
      formQuery_hist: {
        // 产品代码
        fundCode: "",
        // 类型
        type: "",
        //职务
        postCode: [],
        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10,
        //排序方式
        orderBy : ""
      },
      formQuery_hist2: {
        // 产品代码
        fundCode: "",
        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10,
        //排序方式
        orderBy : ""
      },
      fundData:{
        fundCode:""
      },
      // 验证规则
      rules: {
        // 数据来源
        // vcSource: [
        //   { type: 'array', required: true, message: '请选择数据来源', trigger: 'change' }
        // ]
      },
      // 指数弹窗验证规则
      dialogRules: {
        //
        fundCode: [
          { required: true, message: "请输入产品代码", trigger: "change" }
        ],
        //
        fundName: [
          { required: true, message: "请输入产品名称", trigger: "change" }
        ],
        isEnd: [
          { required: true, message: "请选择运行状态", trigger: "change" }
        ],
      },
      //产品类型数据
      typeInArrs:[],
      //计划分类
      ifAcountArrs: [],
      // 年金类型
      annuityTypeArrs: [],
      // 投资类型
      productInvestmentTypeArrs: [],
      // 推荐池
      isRecommendPoolArrs: [],
      // 产品募集方式
      fundTypeArrs: [],
      // 投资管理部门
      vcCompanyNameArrs: [],
      // 所属机构
      companyIdArrs: [],
      // 产品运行状态
      isEndArrs: [],
      // 净值增长率算法
      yieldMethodArrs: [],
      // 净值披露频率
      gzFrequencyArrs: [],
      // 数据来源
      sourceArrs: [],
      // 基础货币
      baseCurrencyArrs: [],
      // 业绩报酬计提方式
      performanceJtArrs: [],
      // 明细分类
      typeDetailArrs: [],

      //投资经理列表
      investManagerList:[],
      //客户经理列表
      customerManagerList:[],
      //各类历史记录
      historyList:[],
      //总条数
      total_hist: 0,

      //外部联系人总数
      total_hist2: 0,

      appendToBody:true,

      dialogMask_fundFile:false,

      dialogMask_history:false,

      dialogMask_history2:false,

      tableLoading_history:false,

      tableLoading_history2:false,

      //产品列表数据
      tableData:[],
      //总条数
      total: 0,
      // 表格loading
      tableLoading: false,
      // 附件表格loading
      tableLoading_doc: false,
      /* 按钮禁止与否 */
      isDisabled: false,
      // 导出图标
      downLoadIcon: "el-icon-download",
      // 导出提示文字
      downLoadText: "导出",
      // 新增产品弹窗
      dialogMask: false,
      // 修改产品弹窗
      dialogMask_doc: false,
      // 表单宽度
      formLabelWidth: "130px",
      //
      dealLoading:false,
      // 弹窗查询参数
      formDialog: {
        /**
         * 基础信息
         */
        //产品代码
        fundCode:"",
        //产品名称
        fundName:"",
        //产品简称
        shortFundname:"",
        //辅助代码
        stbyCode:"",
        //辅助名称
        stbyFundname:"",
        //人社部代码
        fundfCode:"",

        //恒生估值代码
        hsCode:"",
        //恒生估值全称
        hsName:"",
        //ta代码
        taCode:"",
        //ta全称
        taName:"",
        //ta客户编码
        taCustno:"",
        //ta客户名称
        taCustOmName:"",
        //恒生O32代码
        tdCode:"",
        //恒生O32全称
        tdName:"",

        //产品募集方式
        fundType:"",
        //产品管理人
        nameGlr:"",
        //投资管理部门
        vcCompanyName:"",
        //所属机构
        companyId:"",
        //设立金额(元)
        setAmount:"",
        //成立日期
        createDate:"",
        //清算日期
        eDate:"",
        //产品运行状态
        isEnd:"",
        //净值增长率算法
        yieldMethod:"",
        //净值披露频率
        gzFrequency:"",
        //数据来源
        source:"",
        //基础货币
        baseCurrency:"",
        //认购费(%)
        subscriptionFee:"",
        //管理费(%)
        glfRatio:"",
        //业绩报酬(%)
        performanceFee:"",
        //Hurdle Rate(%)
        hurdleRate:"",
        //赎回费(%)
        redemptionFee:"",
        //业绩报酬计提方式
        performanceJt:"",
        //产品类型
        typeIn:"",
        //年金类型
        annuityType:"",
        //明细分类
        typeDetail:"",
        //计划分类
        ifAcount:"",
        //产品投资类型
        productInvestmentType:"",
        //是否含权
        ifEquity:"",
        //是否主动管理
        vcActive:"",
        //外部基金
        isOuterFund:"",
        //是否分级
        isTier:"",
        //是否投资
        fofInvestment:"",
        //估值文件模板
        templateId:"",
        //匹配规则
        matchingRule:"",
        //是否计划
        isPlan:'',
        //所属计划
        isAcount:"",


        /**
         * 投资经理
         */

      },
      //附件列表搜索
      formQuery_doc:{
        fileName:'',
        fundCode:''
      },
      //附件列表数据
      fundFileList:[],
      formFile:{
        //进入附件窗口标记产品代码
        docFundCode:'',
        //文件
        file:''
      },
      // 上传地址
      fileUrl: '',
      // 上传头部
      headersParams: {},
      // 文件列表
      fileList: [],

      // 操作类型 1、添加 2、编辑
      operationType: 1,
      operationType2: 1,

      // 查询按钮禁用
      btnDisabled: false,
      // 查询按钮禁用 附件列表
      btnDisabled_doc: false,
      //默认页签
      activeName:'baseInfo'
    };
  },
  mounted() {
    // 上传地址
    this.fileUrl = FILE_URL + `/api/docCommon/fileCommon/upload-file?fundCode=${this.formFile.docFundCode}`
    this.headersParams = {
      Authorization: this.$store.getters.token
    }

    // 产品类型
    this.getListEdims("ftypein");
    // 投资类型
    this.getListEdims("fundinvesttype");
    // 年金类型
    this.getListEdims("annuityType");
    // 计划分类
    this.getListEdims("typeAcount");
    // 产品募集方式
    this.getListEdims("fund_type_in");
    // 产品运行状态
    this.getListEdims("RUNNINGSTATE");
    // 净值增长率算法
    this.getListEdims("fyieldmethod");
    // 净值披露频率
    this.getListEdims("gzFrequency");
    // 数据来源
    this.getListEdims("SOURCETYPE");
    // 基础货币
    this.getListEdims("base_currency");
    // 业绩报酬计提方式
    this.getListEdims("fund_bcjt");
    // 明细分类
    this.getListEdims("VCTYPEDETAIL");
    // 投资管理部门
    this.getUserDept();
    // 机构信息
    this.getCompanyIdArrs();

    // 投资经理
    this.getInvestManagerList();

    // 默认查询
    this.$nextTick(() => {
      // 查询
      this.onQuery();
    });
  },
  methods: {
    // 资产接收的值
    productNodeClick(data) {
      // // 组合代码
      // this.formDialog.vcFundCode = data.data.id
      // // 组合名称
      // this.formDialog.fundname = data.data.name
    },
    //斑马纹
    xxxTableRowClassName({row, rowIndex}) {
      if (rowIndex%2==0) {
        return '';
      } else {
        return 'statistics-warning-row';
      }
    },
    // 查询
    onQuery(page) {
      this.$refs["formQuery"].validate(valid => {
        if (valid) {
          // 禁用搜索按钮
          this.$fun.searchButtonDisabled("btnDisabled", this);
          // 重置起始页
          if (page) this.formQuery.pageNum = 1;
          // 查询产品信息
          this.selectFundInfoList();
        }
      });
    },

    // 查询附件
    onQueryFile(page) {
      this.$refs["formQuery_doc"].validate(valid => {
        if (valid) {
          // 禁用搜索按钮
          this.$fun.searchButtonDisabled("btnDisabled_doc", this);
          // 查询附件列表
          this.selectFundFiles();
        }
      });
    },
    //联动
    // changIspan(){
    //   if(this.formDialog.isPlan=='1'){
    //     this.isShow=true
    //   }else{
    //     this.isShow=false
    //   }
    // },
    // changIspan1(){
    //   if(this.formDialog.isPlan=='0'){
    //     this.isShows=true
    //   }else{
    //     this.isShows=false
    //   }
    // },
    // 清除
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    // 页面点击事件
    pagination(val) {
      let { page, limit } = val;
      // 起始页
      this.formQuery.pageNum = page;
      // 每页数量
      this.formQuery.pageSize = limit;
      // 查询
      this.onQuery();
    },
    // 经理历史分页点击事件
    pagination_hist(val) {
      let { page, limit } = val;
      // 起始页
      this.formQuery_hist.pageNum = page;
      // 每页数量
      this.formQuery_hist.pageSize = limit;
      // 查询
      this.getHistory();
    },
    // 外部联系人分页点击事件
    pagination_hist2(val) {
      let { page, limit } = val;
      // 起始页
      this.formQuery_hist2.pageNum = page;
      // 每页数量
      this.formQuery_hist2.pageSize = limit;
      // 查询
      this.getHistory2();
    },
    // 获取用户部门
    getUserDept(){
      commonApi.fun_getUserDept().then(res => {
        let { status, data } = res.data;
          // 产品类型
            this.vcCompanyNameArrs = data;
      });
    },

    // 获取机构信息 sys_dept中级别为1的
    getCompanyIdArrs(){
      commonApi.fun_getCompanyIdArrs().then(res => {
        let { status, data } = res.data;
          // 产品类型
            this.companyIdArrs = data;
      });
    },

    // 投资经理下拉选
    getInvestManagerList () {
      investmentManagerApi.managerList().then(res=>{
        this.investManagerList = res.data;
      })
    },
    // 投资经理下拉选
    getCustomerManagerList () {
      customerManagerApi.fun_selectList().then(res=>{
        this.customerManagerList = res.data;
      })
    },
    // 字典查询
    getListEdims(type) {
      // 字典类型
      let params = type;
      commonApi.edimsDdiaCommon(params).then(res => {
        let { status, data } = res.data;

        if (status === 0) {
          // 产品类型
          if (type === "ftypein") {
            this.typeInArrs = data;
          }
          // 投资类型
          if (type === "fundinvesttype") {
            this.productInvestmentTypeArrs = data;
          }
          // 年金类型
          if (type === "annuityType") {
            this.annuityTypeArrs = data;
          }
          // 计划分类
          if (type === "typeAcount") {
            this.ifAcountArrs = data;
          }
          // 产品募集方式
          if (type === "fund_type_in") {
            this.fundTypeArrs = data;
          }
          // 产品运行状态
          if (type === "RUNNINGSTATE") {
            this.isEndArrs = data;
          }
          // 净值增长率算法
          if (type === "fyieldmethod") {
            this.yieldMethodArrs = data;
          }
          // 净值披露频率
          if (type === "gzFrequency") {
            this.gzFrequencyArrs = data;
          }
          // 数据来源
          if (type === "SOURCETYPE") {
            this.sourceArrs = data;
          }
          // 数据来源
          if (type === "base_currency") {
            this.baseCurrencyArrs = data;
          }
          // 业绩报酬计提方式
          if (type === "fund_bcjt") {
            this.performanceJtArrs = data;
          }
          // 明细分类
          if (type === "VCTYPEDETAIL") {
            this.typeDetailArrs = data;
          }
        }
      });
    },
    // 查询产品信息
    selectFundInfoList(flag) {
      if (!flag) {
        this.tableLoading = true;
      } else {
        if (this.isDisabled) return;
        this.isDisabled = true;
        this.downLoadIcon = "el-icon-loading";
        this.downLoadText = "导出";
      }
      let params = Object.assign({}, this.formQuery, {});
      if(this.formQuery.fundCode){
        params.fundCode = this.formQuery.fundCode.toUpperCase();
      }
      if (flag) {
        params.pageNum = 1;
        params.pageSize = 9999999;
        params.ex_tmp_name = "组合信息.xls";
      }
      // 清除空字段
      for (let k in params) {
        if (!params[k] && String(params[k]) !== "0") {
          delete params[k];
        }
      }
      fundInfoApi.fun_selectFundInfoList(params)
        .then(res => {
          this.tableLoading = false;
          this.isDisabled = false;
          this.downLoadIcon = "el-icon-download";
          this.downLoadText = "导出";
          let { status, data } = res;
          if (status === 0) {
            if (flag) {
              // 下载excel
              if (!data) return;
              this.$fun.commonDownloadUrl(data);
            } else {
              let { list, total } = data;
              this.tableData = list;
              this.total = total;
            }
          }
        })
        .catch(() => {
          this.tableLoading = false;
          this.isDisabled = false;
          this.downLoadIcon = "el-icon-download";
          this.downLoadText = "导出";
        });
    },
    // 添加产品信息
    insertFundInfo() {
      let params = Object.assign({}, this.formDialog);

      // 清除空字段
      // for (let k in params) {
      //   if (!params[k] && String(params[k]) !== "0") {
      //     delete params[k];
      //   }
      // }
      // 先检测该产品代码是否存在
      var fundCode = params.fundCode;
      let a = { fundCode };

      fundInfoApi.fun_findRepeatFundCode(a)
        .then(res => {
          // 编码不存在就可以添加
          if (res.status == 200) {
            // 添加产品
            fundInfoApi.fun_insertFundInfo(params)
              .then(res => {
                this.dialogMask = false;
                let { status } = res;
                if (status === 200) {
                  this.$message({
                    message: "添加成功",
                    type: "success"
                  });
                  // 查询
                  this.onQuery();
                } else {
                  this.$message.error("添加失败");
                }
              })
              .catch(() => {
                this.dialogMask = false;
              });
          } else {
            this.$message.error("该产品编号已经存在");
          }
          this.dealLoading = false
        })
        .catch(() => {
          this.$message.error("系统异常");
          this.dealLoading = false
          this.dialogMask = false;
        });
    },
    // 修改产品基本信息
    updateFundInfoInfo() {
      let params = Object.assign({}, this.formDialog);
      // 清除空字段
      // for (let k in params) {
      //   if (!params[k] && String(params[k]) !== "0") {
      //     delete params[k];
      //   }
      // }
      fundInfoApi.fun_updateFundInfo(params)
        .then(res => {
          this.dialogMask = false;
          let { status } = res;
          if (status === 200) {
            this.$message({
              message: "修改成功",
              type: "success"
            });
            // 查询
            this.onQuery();
          } else {
            this.$message.error("修改失败");
          }
          this.dealLoading = false
        })
        .catch(() => {
          this.dealLoading = false
          this.dialogMask = false;
          this.$message.error("系统异常");

        });
    },
    // 删除信息
    deleteFundInfo(fundCode) {
      let params = {
        fundCode
      };
      fundInfoApi.fun_deleteFundInfo(params).then(res => {
        let { status } = res;
        if (status === 200) {
          this.$message({
            type: "success",
            message: res.message
          });
          // 查询
          this.onQuery();
        } else {
          this.$message.error(res.message);
        }
      });
    },
    // 处理数据
    dealData() {
      // // 先关闭之前实例
      // this.$message.closeAll()
      // if (!this.formDialog.vcFundCode) {
      // 	this.$message({
      // 		message: '请选择组合代码',
      // 		type: 'warning'
      // 	})
      // 	return
      // }
      this.$refs["formDialog"].validate(valid => {
        if (valid) {
          this.dealLoading = true
          if (this.operationType === 1) {
            // 添加产品信息
            this.insertFundInfo();
          } else {
            // 修改产品信息

            this.updateFundInfoInfo();
          }
        }
      });
    },
    // 新增数据
    addData() {
      this.operationType = 1;
      this.dialogMask = true;
      this.$nextTick(() => {
        // 清除
        this.resetForm("formDialog");
      });
    },

    // 编辑数据
    editData(row) {
      this.operationType = 2;
      this.dialogMask = true;
      console.log(this.companyIdArrs)
      this.$nextTick(() => {
        // 清除
        this.resetForm("formDialog");
        this.inputFormDialog(row.fundCode);
      })
    },
    // 管理附件
    docManage(row) {
      this.fileList = [];
      this.formFile.docFundCode = row.fundCode;
      this.formQuery_doc.fundCode = row.fundCode;
      this.dialogMask_doc = true;
      this.fileUrl = FILE_URL + `/api/docCommon/fileCommon/upload-file?fundCode=${this.formFile.docFundCode}`
      this.$nextTick(() => {
        // 清除
        this.onQueryFile();
      })
    },

    selectFundFiles(){
      this.tableLoading_doc = true;
      this.btnDisabled_doc = true;
      let params = Object.assign({}, this.formQuery_doc, {
      });
      // 清除空字段
      for (let k in params) {
        if (!params[k] && String(params[k]) !== "0") {
          delete params[k];
        }
      }
      fundInfoApi.fun_selectFundFiles(params).then(res=>{
        this.tableLoading_doc = false;
        let { status, data } = res;

        if (status === 200) {
            this.fundFileList = data;
        }
      })
    },
    inputFormDialog(fundCode){
      //基础信息
      fundInfoApi.fun_selectFundInfo(fundCode).then(res => {
        if(res.data!=undefined && res.data!=''){
          var responseData = res.data;
          console.log(responseData);
          //产品代码
          this.formDialog.fundCode=responseData.fundCode,
            //产品名称
            this.formDialog.fundName=responseData.fundName,
            //产品简称
            this.formDialog.shortFundname=responseData.shortFundname,
            //辅助代码
            this.formDialog.stbyCode=responseData.stbyCode,
            //辅助名称
            this.formDialog.stbyFundname=responseData.stbyFundname,
            //产品募集方式
            this.formDialog.fundType=responseData.fundType,
            //产品管理人
            this.formDialog.nameGlr=responseData.nameGlr,
            //投资管理部门
            this.formDialog.vcCompanyName=responseData.vcCompanyName==undefined?undefined:Number(responseData.vcCompanyName),
            //所属机构
            this.formDialog.companyId=responseData.companyId==undefined?undefined:Number(responseData.companyId),
            //设立金额(元)
            this.formDialog.setAmount=responseData.setAmount,
            //成立日期
            this.formDialog.createDate=responseData.createDate,
            //清算日期
            this.formDialog.eDate=responseData.eDate,
            //产品运行状态
            this.formDialog.isEnd=responseData.isEnd,
            //净值增长率算法
            this.formDialog.yieldMethod=responseData.yieldMethod,
            //净值披露频率
            this.formDialog.gzFrequency=responseData.gzFrequency,
            //数据来源
            this.formDialog.source=responseData.source,
            //基础货币
            this.formDialog.baseCurrency=responseData.baseCurrency,
            //认购费(%)
            this.formDialog.subscriptionFee=responseData.subscriptionFee,
            //管理费(%)
            this.formDialog.glfRatio=responseData.glfRatio,
            //业绩报酬(%)
            this.formDialog.performanceFee=responseData.performanceFee,
            //Hurdle Rate(%)
            this.formDialog.hurdleRate=responseData.hurdleRate,
            //赎回费(%)
            this.formDialog.redemptionFee=responseData.redemptionFee,
            //业绩报酬计提方式
            this.formDialog.performanceJt=responseData.performanceJt,
            //产品类型
            this.formDialog.typeIn=responseData.typeIn,
            //年金类型
            this.formDialog.annuityType=responseData.annuityType,
            //明细分类
            this.formDialog.typeDetail=responseData.typeDetail,
            //计划分类
            this.formDialog.ifAcount=responseData.ifAcount,
            //产品投资类型
            this.formDialog.productInvestmentType=responseData.productInvestmentType,
            //是否含权
            this.formDialog.ifEquity=responseData.ifEquity,
            //外部基金
            this.formDialog.isOuterFund=responseData.isOuterFund,
            //是否分级
            this.formDialog.isTier=responseData.isTier,
            //是否投资
            this.formDialog.fofInvestment=responseData.fofInvestment,
            //估值文件模板
            this.formDialog.templateId=responseData.templateId,
            //匹配规则
            this.formDialog.matchingRule=responseData.matchingRule,
            //所属计划
            this.formDialog.isAcount=responseData.isAcount
            //是否计划
            if(responseData.partntCode=='ROOT'){
              this.formDialog.isPlan='1'
            }else {
              this.formDialog.isPlan='0'
            }
        }
      });
      fundInfoApi.fun_getFundExtInfoByCode(fundCode).then(res=>{
        if(res.data!=null&&res.data!=undefined){
          let reponseData = res.data;
          this.formDialog.fundfCode = reponseData.fundfCode //人社部代码
          this.formDialog.vcActive = reponseData.vcActive //是否主动管理
        }
      })

      //查询三方映射信息
      fundInfoApi.fun_selectExtsysMapping(fundCode).then(res=>{
        if(res.data!=undefined && res.data!=''){
          var responseData = res.data;
          //恒生估值代码
          this.formDialog.hsCode = responseData.hsCode;
          //恒生估值全称
          this.formDialog.hsName = responseData.hsName;
          //TA
          this.formDialog.taCode = responseData.taCode;
          //TA
          this.formDialog.taName = responseData.taName;
          //TA
          this.formDialog.taCustno = responseData.taCustno;
          //TA
          this.formDialog.taCustOmName = responseData.taCustOmName;
          //恒生O32代码
          this.formDialog.tdCode = responseData.tdCode;
          //恒生O32全称
          this.formDialog.tdName = responseData.tdName;
        }
      })
      //查询投资经理
      fundInfoApi.fun_selectFundInvestManager(fundCode,'1').then(res=>{
        if(res.data!=undefined && res.data!=''){
          var managerList = res.data;
          for(var i=0;i<managerList.length;i++){
            if(managerList[i].postCode=='1'){
              this.formDialog.qyFid = managerList[i].fId;
              this.formDialog.qyManager = managerList[i].operatorNo;
              this.formDialog.qyAccessionDate = managerList[i].accessionDate;
              this.formDialog.qyDimissionDate = managerList[i].dimissionDate;
              this.formDialog.qyPostCode = managerList[i].postCode;
            }
            if(managerList[i].postCode=='2'){
              this.formDialog.gsFid = managerList[i].fId;
              this.formDialog.gsManager = managerList[i].operatorNo;
              this.formDialog.gsAccessionDate = managerList[i].accessionDate;
              this.formDialog.gsDimissionDate = managerList[i].dimissionDate;
              this.formDialog.gsPostCode = managerList[i].postCode;
            }
            if(managerList[i].postCode=='3'){
              this.formDialog.fbFid = managerList[i].fId;
              this.formDialog.fbManager = managerList[i].operatorNo;
              this.formDialog.fbAccessionDate = managerList[i].accessionDate;
              this.formDialog.fbDimissionDate = managerList[i].dimissionDate;
              this.formDialog.fbPostCode = managerList[i].postCode;
            }
            if(managerList[i].postCode=='4'){
              this.formDialog.yyFid = managerList[i].fId;
              this.formDialog.yyManager = managerList[i].operatorNo;
              this.formDialog.yyAccessionDate = managerList[i].accessionDate;
              this.formDialog.yyDimissionDate = managerList[i].dimissionDate;
              this.formDialog.yyPostCode = managerList[i].postCode;
            }
            if(managerList[i].postCode=='5'){
              this.formDialog.zhFid = managerList[i].fId;
              this.formDialog.zhManager = managerList[i].operatorNo;
              this.formDialog.zhAccessionDate = managerList[i].accessionDate;
              this.formDialog.zhDimissionDate = managerList[i].dimissionDate;
              this.formDialog.zhPostCode = managerList[i].postCode;
            }
          }
        }

      })
    },

    // 删除数据
    delData(row){
      this.$confirm("确认删除该条数据?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          if (row.fundCode) {
            // 删除产品信息
            this.deleteFundInfo(row.fundCode);
          }
        })
        .catch(() => {});
    },
    fundFileDialog(row){
      this.dialogMask_fundFile = true
      this.fundData.fundCode = row.fundCode
    },
    historyDialog(val,type){
      this.dialogMask_history = true;
      this.formQuery_hist.type = type;

      if (this.operationType === 1) {

      } else {
        this.formQuery_hist.fundCode = this.formDialog.fundCode;
        if(val==='zh'){
          this.formQuery_hist.postCode=["5"];
        }
        if(val==='qy'){
          this.formQuery_hist.postCode=["1"];
        }
        if(val==='gs'){
          this.formQuery_hist.postCode=["2"];
        }
        if(val==='fb'){
          this.formQuery_hist.postCode=["3"];
        }
        if(val==='yy'){
          this.formQuery_hist.postCode=["4"];
        }
        if(val==='xs'){
          this.formQuery_hist.postCode="1";
        }
        if(val==='szx'){
          this.formQuery_hist.postCode="2";
        }
        if(val==='kh'){
          this.formQuery_hist.postCode="3";
        }
      }
      this.getHistory();
    },
    //外部联系人历史
    historyDialog2(){
      this.dialogMask_history2 = true;
      this.getHistory2();
    },
    //历史记录
    getHistory(page){
      // 重置起始页
      if (page) this.formQuery_hist.pageNum = 1;
      // 查询历史记录


      if(this.formQuery_hist.type=='invest'){
        let params = Object.assign({}, this.formQuery_hist, {
          postCodes: this.formQuery_hist.postCode.join(',')
        });
        fundInvestManagerApi.fun_selectFundManagerList(params).then(res=>{
          let { status, data } = res;
          let { list, total } = data;
          this.historyList = list;
          this.total_hist = total;
        })
      }
      if(this.formQuery_hist.type=='customer'){
        let params = Object.assign({}, this.formQuery_hist, {
        });
        customerManagerApi.fun_selectHisttoryByFund(params).then(res=>{
          let { status, data } = res;
          let { list, total } = data;
          this.historyList = list;
          this.total_hist = total;
        })
      }

    },
    getHistory2(page){
      // 重置起始页
      if (page) this.formQuery_hist2.pageNum = 1;
      let params = Object.assign({}, this.formQuery_hist2, {
      });
      fundInfoApi.fun_selectHistoryById(params).then(res=>{
        let { status, data } = res;
        let { list, total } = data;
        this.historyList = list;
        this.total_hist = total;
      })
    },

    // 当表格的排序条件发生变化的时候会触发该事件
    handleSortChange(val) {
      this.formQuery.orderBy = this.$fun.queryOrderBy(val);
      // 查询
      this.onQuery();
    },
    // 表格导出excel
    downloadTableExcel() {
      this.$refs["formQuery"].validate(valid => {
        if (valid) {
          // （导出excel）
          this.selectFundInfoList(true);
        }
      });
    },
    beforeUpload(file){
      // if (file.size > 10 * 1024 * 1024) {
      //   this.$message({
      //     message: "请上传小于10M的文件",
      //     type: "warning"
      //   });
      //   return false
      // }
    },
    // 文件上传成功后
    handleSuccess (res, file, fileList) {
      let { status, data } = res
      if (status === 200) {
        this.$message({
          message: '文件上传成功',
          type: 'success'
        })
        this.onQueryFile()
        // setTimeout(()=>{
        // 	this.$refs.upload.clearFiles()
        // },3000)
      }
    },
    // 文件上传失败时的钩子
    handleError () {
      this.$message.error('文件上传失败')
    },
    //下载文件
    downloadFile(row){
      let params = {
        id: row.id,
        token: getToken()
      }
      if (!params.id || !params.token) return
      // 参数、地址
      let a = fundInfoApi.downloadFileUrl();
      a.then((val)=>{
        this.$fun.formDownloadFile(params, val,"GET");
      })
    },

  },
  watch: {
  }
};
</script>

<style lang="scss">
.title-style {
  color: #0F65DD;
  height: 35px;
  line-height: 35px;
  padding-left: 4px;
  font-size: 16px;
  //border-left: 4px solid #e03d3e;
  margin-bottom: 5px;
}
.el-table__row.statistics-warning-row {
  background: #f0f8f7;
}
.fundInfoListPage {
  padding: 10px;
  .el-dialog .el-form {
    width: 90% !important;
  }
  .el-dialog .el-form-item {
    min-width: 0%;
    margin-right: 10px;
  }

  .mb20 {
    margin-bottom: 15px;
  }
  .customWidth {
    width: 75% !important;
  }
  .item-label {
    font-size: 14px;
  }
  .el-table--medium {
    border-top: 2px solid #007a77 !important;
  }
  .el-checkbox-button--medium .el-checkbox-button__inner {
    font-size: 16px;
  }
  style attribute {
    font-size: 18px;
  }
}
</style>

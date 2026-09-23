<template>
    <div class="bondAnalysis">
      <!--搜索-->
      <el-form :inline="true" ref="formQuery" :model="formQuery" :rules="rules" class="formQuery" >
        <el-row>
          <el-col :span="19">
            <div class="grid-content bg-purple">
              <el-form-item label="日期" prop="beginDate" class="mb20">
                <el-date-picker
                  v-model="formQuery.beginDate"
                  type="date"
                  size="small"
                  value-format="yyyy-MM-dd"
                  :picker-options="this.$fun.dateShortDot()"
                  placeholder="选择日期">
                </el-date-picker>
                <span class="dateHint_text">{{$store.state.setting.dateHint}}</span>
              </el-form-item>
              <el-form-item label="组合类型" prop="fundType" v-if="isFundType">
                <el-select size="small" v-model="formQuery.fundType" multiple placeholder="请选择" >
                  <el-option
                    v-for="(group, index) in groupTypeArr"
                    :value="group.dimCde"
                    :key="index"
                    :label="group.dimNme">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="投资经理" prop="account" v-if="isAccount">
                <el-select size="small" v-model="formQuery.account" filterable clearable placeholder="请选择">
                  <el-option
                    v-for="(item, index) in manageArr"
                    :key="index"
                    :label="item.userName"
                    :value="item.account">
                  </el-option>
                </el-select>
              </el-form-item>

            </div>
          </el-col>
          <el-col :span="5">
            <div >
              <el-form-item class="search_button_com">
                <el-button type="primary" :disabled="btnDisabled" @click="onQuery()" icon="el-icon-search" style="margin-bottom: 5px;" size="small">查询</el-button>
                <el-button plain size="small" @click="resetForm('formQuery')" icon="el-icon-refresh-left">重置</el-button>

              </el-form-item>
            </div>
          </el-col>
        </el-row>
      </el-form>

      <div class="bond_title_box">
        <div class="bond_inline">
          债券资产规模 : <span>{{analysisSummary.price | moneyMillion}}万元</span>
        </div>
        <div class="bond_inline">
          占资产净值比 : <span>{{analysisSummary.netValueRatio | ratioThousand}}%</span>
        </div>
        <div class="bond_inline">
          数据日期 : <span>{{analysisSummary.dateTime || '--'}}</span>
        </div>
      </div>
      <!--期末前十大集中度-->
      <el-row>
        <el-col :span="24">
          <div class="border_box">
            <div class="forms_table_title ml10">
              <i class="el-icon-pie-chart"></i>期末集中度
              <!-- <li @click="downloadTableExcel"><el-tooltip content="下载图表数据" placement="top"><i class="el-icon-s-order"></i></el-tooltip></li> -->
            </div>
            <div class="pdlr10">
              <el-tabs v-model="con_activeName"  type="card" @tab-click="conHandleClick">
                <el-tab-pane  name="bond">
                  <span slot="label">债券 <hint  hintName = "" dimCode = "ZQ_QMJZD_ZQ" dimType = "indexHelp"></hint></span>

                </el-tab-pane>
                <el-tab-pane  name="publisher">
                  <span slot="label">发行人 <hint  hintName = "" dimCode = "ZQ_QMJZD_FXR" dimType = "indexHelp"></hint></span>
                </el-tab-pane>
                <!-- <el-tab-pane  name="issuingScale">
                  <span slot="label">发行规模 </span>
                </el-tab-pane> -->
              </el-tabs>
            </div>
            <!-- 查询 -->
            <el-form :inline="true" ref="formQuery2" :model="formQuery2" :rules="rules2" class="pd10">
              <el-row>
                <el-col :span="19">
                  <el-form-item label="区间" prop="rowNumber">
                    <el-select v-model="formQuery2.rowNumber" placeholder="请选择"  size="small">
                      <template v-for="item in regionArrs">
                        <el-option :label="item.dimNme" :value="item.dimCde" :key="item.dimCde"></el-option>
                      </template>
                    </el-select>
                  </el-form-item>
                  <el-form-item label="债券代码或债券名称" prop="searchName" v-if="con_activeName === 'bond'">
                    <el-input v-model="formQuery2.searchName" placeholder="请输入内容" size="small"></el-input>
                  </el-form-item>
                  <el-form-item label="发行人" prop="searchName" v-if="con_activeName === 'publisher'">
                    <el-input v-model="formQuery2.searchName" placeholder="请输入内容" size="small"></el-input>
                  </el-form-item>
                </el-col>
                <el-col :span="5">
                  <el-form-item class="search_button_com">
                    <el-button type="primary" size="small" :disabled="btnDisabled2" @click="onQuery2(1)">查询</el-button>
                    <el-button plain size="small" @click="resetForm('formQuery2')">重置</el-button>
                    <el-button @click="downloadTableExcel" type="primary" plain :icon="downLoadIcon2" :disabled="isDisabled2" size="small">{{downLoadText2}}</el-button>
                  </el-form-item>
                </el-col>
              </el-row>
            </el-form>

            <div class="pd10" v-show="con_activeName === 'bond'">
              <!--列表-->
              <el-table
                :data="concentrationDegreeTable"
                :default-sort="{prop: 'priceRatio', order: 'descending'}"
                stripe
                border
                @row-click="rowClick"
                @sort-change="handleSortChange"
                v-loading="tableLoading2"
                style="width: 100%">
                <el-table-column
                  type="index"
                  label="序号"
                  width="60"
                  header-align="center">
                </el-table-column>
                <el-table-column
                  prop="symbolName"
                  sortable
				          :sort-orders="['ascending', 'descending']"
                  show-overflow-tooltip
                  label="债券名称"
                  min-width="120"
                  header-align="center">
                  <template slot-scope="scope">
                    <span class="blue">{{scope.row.symbolName}}</span>
                  </template>
                </el-table-column>
                <el-table-column
                  prop="symbolCode"
                  sortable
				          :sort-orders="['ascending', 'descending']"
                  show-overflow-tooltip
                  label="债券代码"
                  min-width="120"
                  header-align="center">
                  <template slot-scope="scope">
                    <span class="blue">{{scope.row.symbolCode}}</span>
                  </template>
                </el-table-column>
                <el-table-column
                  prop="typeName"
                  sortable
				          :sort-orders="['ascending', 'descending']"
                  show-overflow-tooltip
                  label="债券类型"
                  min-width="120"
                  header-align="center">
                </el-table-column>
                <el-table-column
                  prop="price"
                  sortable
				          :sort-orders="['ascending', 'descending']"
                  show-overflow-tooltip
                  label="债券持仓市值(万元)"
                  min-width="130"
                  header-align="center"
                  align="right">
                  <template slot-scope="scope">
                    {{scope.row.price | moneyMillion}}
                  </template>
                </el-table-column>
                <el-table-column
                  prop="priceRatio"
                  sortable
				          :sort-orders="['ascending', 'descending']"
                  show-overflow-tooltip
                  label="占资产净值比(%)"
                  min-width="120"
                  align="right">
                  <template slot-scope="scope">
                    {{scope.row.priceRatio | ratioThousand}}
                  </template>
                </el-table-column>
                <el-table-column
                  prop="faceRate"
                  sortable
				          :sort-orders="['ascending', 'descending']"
                  show-overflow-tooltip
                  label="票面利率(%)"
                  min-width="120"
                  align="right">
                  <template slot-scope="scope">
                    {{scope.row.faceRate | ratioFour}}
                  </template>
                </el-table-column>
                <el-table-column
                  prop="endYield"
                  sortable
				          :sort-orders="['ascending', 'descending']"
                  show-overflow-tooltip
                  label="到期收益率(%)"
                  min-width="120"
                  align="right">
                  <template slot-scope="scope">
                    {{scope.row.endYield | ratioFour}}
                  </template>
                </el-table-column>
                <el-table-column
                  prop="dateTime"
                  sortable
				          :sort-orders="['ascending', 'descending']"
                  show-overflow-tooltip
                  label="到期时间"
                  min-width="120"
                  header-align="center"
                  align="center">
                </el-table-column>
              </el-table>
            </div>
            <div class="pd10" v-show="con_activeName === 'publisher'">
              <!--列表-->
              <el-table
                :data="concentrationDegreeTable"
                :default-sort="{prop: 'priceRatio', order: 'descending'}"
                stripe
                border
                @row-click="rowClick"
                @sort-change="handleSortChange"
                v-loading="tableLoading2"
                style="width: 100%">
                <el-table-column
                  type="index"
                  label="序号"
                  width="60"
                  header-align="center">
                </el-table-column>
                <el-table-column
                  prop="corpname"
                  sortable
				          :sort-orders="['ascending', 'descending']"
                  show-overflow-tooltip
                  label="发行机构"
                  min-width="120"
                  header-align="center">
                  <template slot-scope="scope">
                    <span class="blue">{{scope.row.corpname}}</span>
                  </template>
                </el-table-column>
                <el-table-column
                  prop="issue"
                  sortable
				          :sort-orders="['ascending', 'descending']"
                  show-overflow-tooltip
                  label="机构评级"
                  min-width="120"
                  header-align="center">
                </el-table-column>
                <el-table-column
                  prop="price"
                  sortable
				          :sort-orders="['ascending', 'descending']"
                  show-overflow-tooltip
                  label="机构持仓市值(万元)"
                  min-width="120"
                  header-align="center"
                  align="right">
                  <template slot-scope="scope">
                    {{scope.row.price | moneyMillion}}
                  </template>
                </el-table-column>
                <el-table-column
                  prop="priceRatio"
                  sortable
				          :sort-orders="['ascending', 'descending']"
                  show-overflow-tooltip
                  label="占资产净值比(%)"
                  min-width="120"
                  header-align="center"
                  align="right">
                  <template slot-scope="scope">
                    {{scope.row.priceRatio | ratioThousand}}
                  </template>
                </el-table-column>
                <el-table-column
                  prop="dateTime"
                  sortable
				          :sort-orders="['ascending', 'descending']"
                  show-overflow-tooltip
                  label="期末时间"
                  min-width="120"
                  header-align="center"
                  align="center">
                </el-table-column>
              </el-table>
            </div>
            <div class="pd10" v-show="con_activeName === 'issuingScale'">
              <!--列表-->
              <el-table
                :data="concentrationDegreeTable"
                :default-sort="{prop: 'priceRatio', order: 'descending'}"
                stripe
                border
                @row-click="rowClick"
                @sort-change="handleSortChange"
                v-loading="tableLoading2"
                style="width: 100%">
                <el-table-column
                  type="index"
                  label="序号"
                  width="60"
                  header-align="center">
                </el-table-column>
                <el-table-column
                  prop="symbolName"
                  sortable
				          :sort-orders="['ascending', 'descending']"
                  show-overflow-tooltip
                  label="债券名称"
                  min-width="120"
                  header-align="center">
                  <template slot-scope="scope">
                    <span class="blue">{{scope.row.symbolName}}</span>
                  </template>
                </el-table-column>
                <el-table-column
                  prop="symbolCode"
                  sortable
				          :sort-orders="['ascending', 'descending']"
                  show-overflow-tooltip
                  label="债券代码"
                  min-width="120"
                  header-align="center">
                  <template slot-scope="scope">
                    <span class="blue">{{scope.row.symbolCode}}</span>
                  </template>
                </el-table-column>
                <el-table-column
                  prop="typeName"
                  sortable
				          :sort-orders="['ascending', 'descending']"
                  show-overflow-tooltip
                  label="债券类型"
                  min-width="120"
                  header-align="center">
                </el-table-column>
                <el-table-column
                  prop="scale"
                  sortable
				          :sort-orders="['ascending', 'descending']"
                  show-overflow-tooltip
                  label="发行规模(万元)"
                  min-width="120"
                  header-align="center"
                  align="right">
                  <template slot-scope="scope">
                    {{scope.row.scale | moneyMillion}}
                  </template>
                </el-table-column>
                <el-table-column
                  prop="priceRatio"
                  sortable
				          :sort-orders="['ascending', 'descending']"
                  show-overflow-tooltip
                  label="占资产净值比(%)"
                  min-width="120"
                  header-align="center"
                  align="right">
                  <template slot-scope="scope">
                    {{scope.row.priceRatio | ratioThousand}}
                  </template>
                </el-table-column>
                <el-table-column
                  prop="dateTime"
                  sortable
				          :sort-orders="['ascending', 'descending']"
                  show-overflow-tooltip
                  label="期末时间"
                  min-width="120"
                  header-align="center"
                  align="center">
                </el-table-column>
              </el-table>
            </div>

            <div class="clearfix mb10">
              <Pagination :total="total2" :limit="formQuery2.pageSize" :page="formQuery2.pageNum" @pagination="pagination2"></Pagination>
            </div>

            <!-- <div id="concentrationTrend" class="echarts_box" style="height:251px;" ></div> -->

          </div>
        </el-col>
      </el-row>
      <!--债券类属结构变化 历史-->
      <!--<el-row class="border_box mt30">-->
        <!--<el-col :span="13">-->
          <!--<div class="forms_table_title ml10"><i class="el-icon-s-marketing"></i>债券类属结构变化<li><el-tooltip content="下载图表数据" placement="top"><i class="el-icon-s-order"></i></el-tooltip></li></div>-->
          <!--<div id="bondKindTrend" class="echarts_box" v-loading="bondKindTrendEchartsLoading && $store.state.setting.loadingShow"></div>-->
        <!--</el-col>-->
        <!--<el-col :span="11">-->
          <!--<div style="padding-left: 50px;">-->
            <!--<el-row class="mt10 min300" v-loading="investBondGenericLoading && $store.state.setting.loadingShow">-->
              <!--<el-col :span="1">-->
                <!--<div class="termAverageone_box">-->
                  <!--<li></li>-->
                  <!--<template v-for="(item, index) in investBondGenericData">-->
                    <!--<li :key="index"><span :style="{background: $colorArrs[index]}"></span></li>-->
                  <!--</template>-->
                <!--</div>-->
              <!--</el-col>-->
              <!--<el-col :span="9">-->
                <!--<div class="termAveragetwo_box">-->
                  <!--<li></li>-->
                  <!--<template v-for="(item, index) in investBondGenericData">-->
                    <!--<li :key="index">{{item.name}}</li>-->
                  <!--</template>-->
                <!--</div>-->
              <!--</el-col>-->
              <!--<el-col :span="7">-->
                <!--<div class="termAveragetwo_box">-->
                  <!--<li>期间平均占比</li>-->
                  <!--<template v-for="(item, index) in investBondGenericData">-->
                    <!--<li :key="index">{{item.proportionAvg || 0}}%</li>-->
                  <!--</template>-->
                <!--</div>-->
              <!--</el-col>-->
              <!--<el-col :span="5">-->
                <!--<div class="termAveragetwo_box">-->
                  <!--<li>期末时点占比</li>-->
                  <!--<template v-for="(item, index) in investBondGenericData">-->
                    <!--<li :key="index">{{item.proportionEnd || 0}}%</li>-->
                  <!--</template>-->
                <!--</div>-->
              <!--</el-col>-->

            <!--</el-row>-->

          <!--</div>-->
        <!--</el-col>-->
      <!--</el-row>-->

      <!--债券类属结构变化 new-->
      <el-row class="border_box mt30" style="padding:0px 10px;">
        <!--<el-form :inline="true" ref="formInline" :model="formInline"  :rules="searchRules"  class="demo-form-inline form_inline_search" style="margin-top: 10px">-->
          <!--<el-row>-->
            <!--<el-col :span="19">-->
              <!--<div class="grid-content bg-purple">-->

                <!--<el-form-item label="日期" prop = "date">-->
                  <!--<el-date-picker-->
                    <!--v-model="formInline.date"-->
                    <!--type="daterange"-->
                    <!--unlink-panels-->
                    <!--range-separator="至"-->
                    <!--start-placeholder="开始日期"-->
                    <!--end-placeholder="结束日期"-->
                    <!--value-format="yyyy-MM-dd"-->
                    <!--:picker-options="this.$fun.dateShortcut()"-->
                    <!--size="small"-->
                  <!--&gt;-->
                  <!--</el-date-picker>-->
                <!--</el-form-item>-->
              <!--</div>-->
            <!--</el-col>-->
            <!--<el-col :span="5">-->
              <!--<div class="grid-content bg-purple-light">-->
                <!--<el-form-item  class="search_button_com">-->
                  <!--<el-button type="primary" @click="onSubmit('formInline')" style="margin-bottom: 5px;"  size="small">查询</el-button>-->
                  <!--<el-button plain size="small" @click="resetForm('formInline')">重置</el-button>-->
                <!--</el-form-item>-->
              <!--</div>-->
            <!--</el-col>-->
          <!--</el-row>-->
        <!--</el-form>-->


        <el-col :span="13">
          <div class="forms_table_title ">
            <i class="el-icon-s-marketing"></i>近一年债券类属结构变化 <hint  hintName = "" dimCode = "ZQ_LSJGBH" dimType = "indexHelp"></hint>
            <li @click="exportExcelFile"><el-tooltip content="下载图表数据" placement="top"><i class="el-icon-s-order"></i></el-tooltip></li>
          </div>
          <div id="bondConstructionTrend" class="echarts_box" v-loading="bondConstructionTrendLoading && $store.state.setting.loadingShow"></div>
        </el-col>
        <el-col :span="11">
          <div class="forms_table_title ">

          </div>
          <div style="padding-left: 50px;">
            <el-table
              :data="bondConstructionTrendData"
              stripe
              border
              v-loading="bondConstructionTrendLoading && $store.state.setting.loadingShow"
              height = "290"
              @sort-change="bondConstructionTrendDataSort"
              :default-sort = "{prop: 'meanAssetRatioOri', order: 'descending'}"
              style="width: 100%">

              <el-table-column
                prop="typeName"
                label=""
                header-align = "center"
                :show-overflow-tooltip="true"
                min-width="90">
                <template slot-scope="scope">
                    <span >{{ scope.row.typeName | noDataFilter}}</span>
                </template>
              </el-table-column>
              <el-table-column
                prop="meanAssetRatioOri"
                :show-overflow-tooltip="true"
                label="期间平均占比(%)"
                sortable = "custom"
				        :sort-orders="['ascending', 'descending']"
                header-align = "center"
                align="right"
                min-width="120"
              >
                <template slot-scope="scope">
                  <span  >{{ scope.row.meanAssetRatioOri | numberToFixed(2,1) }}</span>
                </template>
              </el-table-column>
              <el-table-column
                prop="endAssetRatioOri"
                label="期末时点占比(%)"
                :show-overflow-tooltip="true"
                sortable = "custom"
				        :sort-orders="['ascending', 'descending']"
                header-align = "center"
                align="right"
                min-width="100"
              >
                <template slot-scope="scope">
                  <span>{{ scope.row.endAssetRatioOri | numberToFixed(2,1)}}</span>
                </template>
              </el-table-column>
            </el-table>


          </div>
        </el-col>
      </el-row>

      <el-row class="mt30" :gutter="40" >
        <el-col :span="12">
          <div class="border_box">
            <div class="forms_table_title ml10">
              <i class="el-icon-s-marketing"></i>近一年信用债主体评级分布
              <hint  hintName = "" dimCode = "ZQ_XYZZTPJ" dimType = "indexHelp"></hint>
              <li @click="exportExcelFile2"><el-tooltip content="下载图表数据" placement="top"><i class="el-icon-s-order"></i></el-tooltip></li>
            </div>
            <div id="bondCreditTrend" class="echarts_box" v-loading="bondCreditTrendEchartsLoading && $store.state.setting.loadingShow"></div>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="border_box">
            <div class="forms_table_title ml10">
              <i class="el-icon-s-marketing"></i>近一年信用债债项评级分布
              <hint  hintName = "" dimCode = "ZQ_XYZZXPJ" dimType = "indexHelp"></hint>
              <li @click="exportExcelFile3"><el-tooltip content="下载图表数据" placement="top"><i class="el-icon-s-order"></i></el-tooltip></li>
            </div>
            <div id="bondProjectTrend" class="echarts_box" v-loading="bondProjectTrendEchartsLoading && $store.state.setting.loadingShow"></div>
          </div>

        </el-col>
      </el-row>

      <el-row class="mt30" :gutter="40">
        <el-col :span="12">
          <div class="border_box minH464" style="padding-bottom: 46px;">
            <div class="forms_table_title ml10">
              <i class="el-icon-s-marketing"></i>近一年回购占比<hint  hintName = "" dimCode = "ZQ_HGZB" dimType = "indexHelp"></hint>
              <p style="font-weight: 500;color: #3f3f3f;position: absolute;right: 35px;">期末 : {{buyBackTrendRatiosFinal | ratioThousand}}%</p>
              <li @click="exportExcelFile4"><el-tooltip content="下载图表数据" placement="top"><i class="el-icon-s-order"></i></el-tooltip></li>
            </div>

            <div id="buyBackTrend" class="echarts_box mt50" v-loading="buyBackTrendEchartsLoading && $store.state.setting.loadingShow"></div>

          </div>
        </el-col>
        <el-col :span="12">
          <div class="border_box minH444">
            <div class="forms_table_title ml10">
              <i class="el-icon-s-marketing"></i>期末分布
              <li @click="exportExcelFile5"><el-tooltip content="下载图表数据" placement="top"><i class="el-icon-s-order"></i></el-tooltip></li>
            </div>
            <div style="padding: 0px 10px;">
            <el-tabs v-model="distr_activeName"  type="card" @tab-click="distrHandleClick">
              <!-- <el-tab-pane label="类属" name="generic"></el-tab-pane> -->
              <el-tab-pane name="remaining">
                <span slot="label">剩余期限 <hint  hintName = "" dimCode = "ZQ_QMFB_SYQX" dimType = "indexHelp"></hint></span>
              </el-tab-pane>
              <el-tab-pane  name="industry">
                <span slot="label">行业 <hint  hintName = "" dimCode = "ZQ_QMFB_HY" dimType = "indexHelp"></hint></span>
              </el-tab-pane>
              <!-- <el-tab-pane label="地区" name="four"></el-tab-pane> -->
            </el-tabs>
            </div>

            <!-- 查询 -->
            <el-form :inline="true" ref="formQuery3" :model="formQuery3" :rules="rules3" class="pd10" v-show="distr_activeName === 'industry'">
              <el-row>
                <el-col :span="12">
                  <el-form-item label="区间" prop="rowNumber">
                    <el-select v-model="formQuery3.rowNumber" placeholder="请选择"  size="small">
                      <template v-for="item in regionArrs">
                        <el-option :label="item.dimNme" :value="item.dimCde" :key="item.dimCde"></el-option>
                      </template>
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item class="search_button_com">
                    <el-button type="primary" size="small" @click="onQuery3(1)">查询</el-button>
                    <el-button plain size="small" @click="resetForm('formQuery3')">重置</el-button>
                    <el-button @click="downloadTableExcel2" type="primary" plain :icon="downLoadIcon" :disabled="isDisabled" size="small">{{downLoadText}}</el-button>
                  </el-form-item>
                </el-col>
              </el-row>
            </el-form>
            <div class="tabContent">
              <div class="tabVisible pd10" :class="{'visible': distr_activeName === 'remaining'}">
                <div id="endDistrTrend" class="echarts_box" style="height: 300px;" v-loading="endDistrTrendEchartsLoading && $store.state.setting.loadingShow"></div>
              </div>
              <div class="tabVisible pd10" :class="{'visible': distr_activeName === 'industry'}">
                <!--列表-->
                <el-table
                  :data="investBondFinalDistributionData2"
                  :default-sort="{prop: 'priceRatio', order: 'descending'}"
                  stripe
                  border
                  max-height="222"
                  @sort-change="handleBondSortChange"
                  v-loading="tableLoading"
                  style="width: 100%">
                  <el-table-column
                    type="index"
                    label="序号"
                    width="60"
                    header-align="center">
                  </el-table-column>
                  <el-table-column
                    prop="industryType"
                    sortable
				            :sort-orders="['ascending', 'descending']"
                    show-overflow-tooltip
                    label="行业分类"
                    min-width="100"
                    header-align="center">
                  </el-table-column>
                  <el-table-column
                    prop="industryName"
                    sortable
				            :sort-orders="['ascending', 'descending']"
                    show-overflow-tooltip
                    label="行业名称"
                    min-width="100"
                    header-align="center"
                    align="center">
                  </el-table-column>
                  <el-table-column
                    prop="industryCode"
                    sortable
				            :sort-orders="['ascending', 'descending']"
                    show-overflow-tooltip
                    label="行业代码"
                    min-width="100"
                    header-align="center"
                    align="center">
                  </el-table-column>
                  <el-table-column
                    prop="price"
                    sortable
				            :sort-orders="['ascending', 'descending']"
                    show-overflow-tooltip
                    label="行业持仓市值(万元)"
                    min-width="140"
                    header-align="center"
                    align="center">
                    <template slot-scope="scope">
                      {{scope.row.price | moneyMillion}}
                    </template>
                  </el-table-column>
                  <el-table-column
                    prop="priceRatio"
                    sortable
				            :sort-orders="['ascending', 'descending']"
                    show-overflow-tooltip
                    label="占资产净值比(%)"
                    min-width="130"
                    header-align="center"
                    align="right">
                    <template slot-scope="scope">
                      {{scope.row.priceRatio | ratioThousand}}
                    </template>
                  </el-table-column>
                  <el-table-column
                    prop="dateTime"
                    sortable
				            :sort-orders="['ascending', 'descending']"
                    show-overflow-tooltip
                    label="期末时间"
                    min-width="100"
                    header-align="center"
                    align="center">
                  </el-table-column>
                </el-table>

                <div class="clearfix mb10">
                  <Pagination :total="total3" :limit="formQuery3.pageSize" :page="formQuery3.pageNum" @pagination="pagination3"></Pagination>
                </div>
              </div>
            </div>
          </div>

        </el-col>
      </el-row>

      <el-dialog
        v-el-drag-dialog
        :title="dialogTitle"
        :visible.sync="dialogMask"
        :close-on-click-modal="false">
        <el-table
          :data="tableData"
          :default-sort="{prop: 'symbolPrice', order: 'descending'}"
          border
          stripe
          @sort-change="handleInvestBondSortChange"
          max-height="300"
          style="width: 100%">
          <el-table-column
            prop="fundCode"
            show-overflow-tooltip
            sortable
            :sort-orders="['ascending', 'descending']"
            label="组合代码"
            min-width="80"
            header-align="center"
          />
			    <el-table-column
            prop="fundName"
            show-overflow-tooltip
            sortable
            :sort-orders="['ascending', 'descending']"
            label="组合名称"
            min-width="80"
            header-align="center"
          />
          <el-table-column
            prop="investManager"
            show-overflow-tooltip
            sortable
            :sort-orders="['ascending', 'descending']"
            label="投资经理"
            min-width="80"
            header-align="center"
          />
          <el-table-column
            prop="symbolCode"
            show-overflow-tooltip
            sortable
            :sort-orders="['ascending', 'descending']"
            label="债券代码"
            min-width="80"
            header-align="center"
          />
          <el-table-column
            prop="symbolName"
            show-overflow-tooltip
            sortable
            :sort-orders="['ascending', 'descending']"
            label="债券名称"
            min-width="120"
            header-align="center"
          />
          <el-table-column
            prop="symbolType"
            show-overflow-tooltip
            sortable
            :sort-orders="['ascending', 'descending']"
            label="债券类型"
            min-width="70"
            header-align="center"
          />
          <el-table-column
            prop="symbolAcount"
            show-overflow-tooltip
            sortable
            :sort-orders="['ascending', 'descending']"
            label="债券数量"
            min-width="80"
            header-align="center"
            align="right"
          >
            <template slot-scope="scope">
              {{scope.row.symbolAcount | moneyThousand}}
            </template>
          </el-table-column>
          <el-table-column
            prop="symbolPrice"
            show-overflow-tooltip
            sortable
            :sort-orders="['ascending', 'descending']"
            label="债券市值(万元)"
            min-width="90"
            header-align="center"
            align="right"
          >
            <template slot-scope="scope">
              {{scope.row.symbolPrice | moneyMillion}}
            </template>
          </el-table-column>
        </el-table>
      </el-dialog>

    </div>
</template>

<script>
import * as echarts from 'echarts'
import { exportExcel, forEachSeries, downloadExcel} from '@/utils/exportExcel'
import Pagination from '@/components/Pagination'
import commonApi from '@/api/common'
import investmentManagerApi from '@/api/managementView/investmentManager'
import hint from '@/components/hint'
import {
  investSumAnalysisUrl,
  investManagerFundViewUrl,
  investManagerFundViewExcelUrl,
  investBondAnalysisDetailsUrl,
  investPublisherAnalysisDetailsUrl,
  investBondLeftGenericUrl,
  investBondGenericUrl,
  investBondGenericNewUrl,
  investBondSubjectRatingUrl,
  investBondDebtRatingUrl,
  investBondBuybackRatioUrl,
  investBondTerminalTimeUrl,
  investBondFinalDistributionUrl
} from '@/api/securitiesAnalysis'
import fun from '@/filters/common'

export default {
  name: "bond-analysis",
  components: {
    Pagination,hint
  },
  props: {
    // 是否显示投资经理下拉
    isAccount: {
      type: Boolean,
      default: true
    },
    // 组合代码
    fundCode: {
      default: ''
    },
    // 日期
    date: {
      default: ''
    },
    // 是否显示组合类型
    isFundType: {
      type: Boolean,
      default: true
    },
    // 图表打开关闭
    echartsOpenChild: {
      type: Boolean
    }
  },
  data() {
    return {
      formQuery:{
        // 日期
        beginDate:'',
        // 组合类型
        fundType: [],
        // 投资经理
        account: '',
        // 组合代码集合
        fundList: []
      },
      //债券类属结构变化 new
      // formInline: {
      //   date:[],
      // },
      formQuery2: {
        // 区间
        rowNumber: '',
        // 查询参数
        searchName: '',
        // 排序条件
        orderBy: '"priceRatio" desc nulls last',
        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10
      },
      formQuery3: {
        // 区间
        rowNumber: '',
        // 排序条件
        orderStr: '',
        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10
      },
      // 头部排序存储
      formQueryOrderBy: {
        // 债券
        bond: '"priceRatio" desc nulls last',
        // 发行人
        publisher: '"priceRatio" desc nulls last',
        // 发行规模
        issuingScale: '"priceRatio" desc nulls last'
      },
      // 组合类型数组
      groupTypeArr: [],
      // 投资经理数组
      manageArr: [],
      // 验证规则
      rules:{
        // 日期
        beginDate: [
          { type: 'string', required: true, message: '请选择日期', trigger: 'change' }
        ],
        // 组合类型
        fundType: [
          { type: 'array', required: true, message: '请选择组合类型', trigger: 'change' }
        ],
        // 投资经理
        account: [
          { type: 'string', required: true, message: '请选择投资经理', trigger: 'change' }
        ]
      },
      //债券类属结构变化日期验证 new
      // searchRules:{
      //   date: [{type: 'array', required: true, message: '请选择日期', trigger: 'change'}],
      // },
      // 验证规则
      rules2: {
        // 区间
        rowNumber: [
          { required: true, message: '请选择区间', trigger: 'change' }
        ]
      },
      // 验证规则
      rules3: {
        // 区间
        rowNumber: [
          { required: true, message: '请选择区间', trigger: 'change' }
        ]
      },
      con_activeName:'bond',//期末前十大集中度选项卡
      concentrationTrendEcharts:'', //期末前十大集中度
      bondKindTrendEcharts:'', // 债券类属变化
      // 债券类属变化loading
      bondKindTrendEchartsLoading: false,
      //债券类属结构变化 new
      bondConstructionTrendEcharts:'',
      bondConstructionTrendLoading:false,
      bondConstructionTrendData:[],//债券类属变化数据
      isAsc:false,//正序倒序
      orderBy:"meanAssetRatioOri",//排序字段
      //end
      // excel表头
			excelHeader: [],
			// excel数据
			excelData: [],
      bondCreditTrendEcharts:'', // 信用债主体评级分布
      // 信用债主体评级分布loading
      bondCreditTrendEchartsLoading: false,
      // excel表头
			excelHeader2: [],
			// excel数据
			excelData2: [],
      bondProjectTrendEcharts:'', // 信用债债项评级分布
      // 信用债债项评级分布loading
      bondProjectTrendEchartsLoading: false,
      // excel表头
			excelHeader3: [],
			// excel数据
			excelData3: [],
      buyBackTrendEcharts:'', // 回购占比
      // 回购占比loading
      buyBackTrendEchartsLoading: false,
      // excel表头
			excelHeader4: [],
			// excel数据
			excelData4: [],
      endDistrTrendEcharts:'', // 期末分布
      // 期末分布loading
      endDistrTrendEchartsLoading: false,
      // excel表头
			excelHeader5: [],
			// excel数据
			excelData5: [],
      distr_activeName:'remaining',//期末分布
      // 证券分析-汇总
      analysisSummary: {
        // 债券资产规模
        price: 0,
        // 数据日期
        dateTime: '--',
        // 占资产净值比
        netValueRatio: 0
      },
      // 区间数组
      regionArrs: [],
      // 前十大集中度
      concentrationDegree: [
        {
          one1: '债券名称',
          one2: '债券代码',
          one3: '债券类型',
          one4: '债券持仓市值',
          one5: '占资产净值比',
          one6: '期末时间',
          one7: '发行机构',
          one8: '机构评级',
          one9: '机构持仓市值',
          one10: '发行规模'
        }
      ],
      // 前十大集中度图表
      concentrationDegreeTable: [],
      // 表格loading
      tableLoading2: false,
      /* 按钮禁止与否 */
      isDisabled2: false,
      // 导出图标
      downLoadIcon2: 'el-icon-download',
      // 导出提示文字
      downLoadText2: '导出数据',
      // 总条数2
      total2: 0,
      // 总条数3
      total3: 0,
      // 债券类属结构变化（左）
      investBondLeftGenericData: {},
      // 债券类属结构变化（右）
      investBondGenericData: [],
      // 债券类属结构变化（右）loading
      investBondGenericLoading: false,
      // 主体评级
      investBondSubjectRatingData: {},
      // 债项评级
      investBondDebtRatingData: {},
      // 回购占比
      investBondBuybackRatioData: [],
      // 期末分布
      investBondFinalDistributionData: [],
      // 期末分布列表数据
      investBondFinalDistributionData2: [],
      // 表格loading
      tableLoading: false,
      /* 按钮禁止与否 */
      isDisabled: false,
      // 导出图标
      downLoadIcon: 'el-icon-download',
      // 导出提示文字
      downLoadText: '导出数据',
      // 弹窗
      dialogMask: false,
      // 标题
      dialogTitle: '',
      // 列表数据
      tableData: [],
      // 回购占比期末
      buyBackTrendRatiosFinal: 0,
      // 查询按钮禁用
      btnDisabled: false,
      // 查询按钮禁用2
      btnDisabled2: false,
      // 保存表格传递值
      saveStr: '',
      // 债券/发行人排序字段
      orderStr2: `"symbolPrice" desc nulls last`
    }
  },
  mounted(){
    if (this.fundCode) this.formQuery.fundList = [this.fundCode]
    // 今天
    // let today = this.$moment().subtract(1,'days').format('YYYY-MM-DD')
    if (this.date) {
      // 日期
      this.formQuery.beginDate = this.date
    } else {
      // 日期
      // this.formQuery.beginDate = today
      // 接口返回T-1日
      this.formQuery.beginDate = this.$store.state.setting.endDate
    }
    // this.$bus.$on('securityAnalyzeDate', date => {
    //   console.log(date)
    //   this.formQuery.beginDate = date
    // })
    // 组合类型
    this.formQuery.fundType = ['*']
    // 投资经理账户
    // this.formQuery.account = '511'
    //债券类属结构默认日期 new
    // this.formInline.date = [this.$moment(this.$moment(this.$moment().subtract(1,'days').format('YYYY-MM-DD')).subtract(1,'years').format('YYYY-MM-DD')).subtract(-1,'days').format('YYYY-MM-DD'),this.$moment().subtract(1,'days').format('YYYY-MM-DD')]
    // this.formInline.date = ["2017-12-31","2018-12-31"];
    // 区间查询
    this.getListEdims('range_type')
    // 投资经理
    if (!this.isAccount) {
      this.formQuery.account = -1
    } else {
      // 投资经理列表查询
      this.getManagerList()
    }
    // 组合类型
    if (!this.isFundType) {
      this.formQuery.fundType = ['*']
    } else {
      // 组合类型列表查询
      this.getListEdims('fund_type')
    }
    this.$nextTick(() => {
      // 期末前十大集中度
      // this.fun_concentrationTrendEcharts();
      // 债券类属变化
      // this.fun_bondKindTrendEcharts();
      // 债券类属变化 new
      this.fun_bondConstructionTrendEcharts([],[],[]);
      // 信用债主体评级分布
      this.fun_bondCreditTrendEcharts();
      // 信用债债项评级分布
      this.fun_bondProjectTrendEcharts();
      // 回购占比
      this.fun_buyBackTrendEcharts();
      // 期末分布
      this.fun_endDistrTrendEcharts();
      // 是否默认查询
      if (this.$store.state.setting.isOnQuery) {
        // 延迟2s请求
        let timer = setTimeout(() => {
          // 查询
          this.onQuery()
          clearTimeout(timer)
        }, 2000)
      }
    })
    let _this = this
    // 宽度变化重新渲染图表
    window.addEventListener('resize', () => {
      let timer = setTimeout(() => {
        // 宽度变化重新渲染图表
        _this.echartsResize()
        clearTimeout(timer)
      },500)
    })
  },
  methods: {
    // 查询2
    onQuery2 (page) {
      this.$refs['formQuery2'].validate((valid) => {
        if (valid) {
          // 禁用搜索按钮
          this.$fun.searchButtonDisabled("btnDisabled2", this)
          // 重置起始页
          if (page) this.formQuery2.pageNum = 1
          // 投资经理视图-证券分析-债券分析-前十大集中度
          this.investManagerFundView()
        }
      })
    },
    // 查询3
    onQuery3 (page) {
      this.$refs['formQuery3'].validate((valid) => {
        if (valid) {
          // 重置起始页
          if (page) this.formQuery3.pageNum = 1
          // 投资经理视图-证券分析-债券分析-期末分布(行业)
          this.getInvestBondFinalDistribution()
        }
      })
    },
    onQuery () {
      this.$refs['formQuery'].validate((valid) => {
        if (valid) {
          // 禁用搜索按钮
          this.$fun.searchButtonDisabled("btnDisabled", this)
          // 投资经理视图-证券分析-汇总
          this.investSumAnalysis()
          // 投资经理视图-证券分析-债券分析-前十大集中度
          // this.investManagerFundView()
          this.onQuery2()
          // 投资经理视图-证券分析-债券分析-债券类属结构变化（左）  历史
          //this.getInvestBondLeftGeneric()
          // 投资经理视图-证券分析-债券分析-债券类属结构变化（右）  历史
          //this.getInvestBondGeneric()
          // 投资经理视图-证券分析-债券分析-主体评级
          this.getInvestBondSubjectRating()
          // 投资经理视图-证券分析-债券分析-债项评级
          this.getInvestBondDebtRating()
          // 投资经理视图-证券分析-债券分析-回购占比
          this.getInvestBondBuybackRatio()
          // 投资经理视图-证券分析-债券分析-期末分布(剩余期限)
          this.getInvestBondTerminalTime()
          this.onQuery3()
          //调用债券类属结构变化 new
          this.getBondConstructionData();
          // this.onSubmit('formInline');
        }
      })
    },
    //债券类属结构变化查询 new
    // onSubmit(formName){
    //   this.$refs[formName].validate((valid) => {
    //     if (valid) {
    //       this.getBondConstructionData();
    //     } else {
    //       return false;
    //     }
    //   });
    // },

    // 清除
    resetForm (formName) {
      this.$refs[formName].resetFields();
    },
    //今年以来日期选择
    conHandleClick(tab, event) {
      this.formQuery2.orderBy = this.formQueryOrderBy[this.con_activeName]
      // 重置
      this.formQuery2.pageNum = 1
      this.total2 = 0
      this.formQuery2.searchName = ''
      this.$refs['formQuery2'].validate((valid) => {
        if (valid) {
          // 投资经理视图-证券分析-债券分析-前十大集中度
          this.investManagerFundView()
        }
      })
    },
    // 期末前十大集中度
    fun_concentrationTrendEcharts () {
      // 图表名字
      let seriesName = ''
      if (this.con_activeName === 'bond') {
        seriesName = '债券'
      } else if (this.con_activeName === 'publisher') {
        seriesName = '发行人'
      } else if (this.con_activeName === 'issuingScale') {
        seriesName = '发行规模'
      }
      // 前十大集中度
      let nameArrs = []
      // 饼状图数据
      let data = []
      this.concentrationDegree.forEach(item => {
        nameArrs.push(item.name)
        let obj = {
          value: Number(item.price),
          name: item.name
        }
        data.push(obj)
      })

      this.concentrationTrendEcharts = echarts.init(document.getElementById('concentrationTrend'))
      this.concentrationTrendEcharts.setOption({
        tooltip: {
          trigger: 'item',
          formatter: "{a} <br/>{b}: {c} ({d}%)"
        },
        legend: {
          orient: 'vertical',
          icon:"circle",
          right: 150,
          bottom: 20,
          itemWidth: 6,// 标志图形的长度
          itemHeight: 6,// 标志图形的宽度
          itemGap: 7 ,// 设置间距
          data: nameArrs,
          formatter: function(name) {
            var total = 0;
            var tarValue;
            for (var i = 0, l = data.length; i < l; i++) {
              total += data[i].value;
              if (data[i].name == name) {
                tarValue = data[i].value;
              }
            }
            let p =  0
            if (total) {
              p = (tarValue / total * 100).toFixed(2)
            }
            return name + ' ' + ' '  + p + '%';
          },

        },
        toolbox: {
          feature: {
            dataView: {
              optionToContent: this.$fun.optionToContent
            },
            saveAsImage: {}
          }
        },
        color: this.$colorArrs,
        series: [
          {
            name: seriesName,
            type:'pie',
            radius: ['50%', '70%'],
            avoidLabelOverlap: false,
            label: {
              normal: {
                show: false,
                position: 'center',
              },
              emphasis: {
                show: true,
                textStyle: {
                  fontSize: '14',
                  fontWeight: 'bold'
                }
              }
            },
            labelLine: {
              normal: {
                show: false
              }
            },
            data:data,
          }
        ]
      })
    },
    // 债券类属变化
    fun_bondKindTrendEcharts(){
      let echartData = this.investBondLeftGenericData
      // 头部显示
      let legendData = []
      // 横坐标
      let xData = []
      // 最大值
			let dataMax = 0
			// 最小值
			let dataMin = 0
      // 数据数组
			let seriesArrs = []
      for( let key in  echartData) {
        legendData.push(key)
        if (!xData.length) {
          echartData[key].forEach(item => {
            xData.push(item.dateTime)
          })
        }
        let seriesData = []
        echartData[key].forEach(item => {
          seriesData.push(item.price)
        })
        // 最大值
        dataMax = Math.max(...seriesData, dataMax)
        // 最小值
        dataMin = Math.min(...seriesData, dataMin)
        let seriesObj = {
          name: key,
          stack: key,
          type: 'line',
          symbolSize: 6,
          data: seriesData
        }
        seriesArrs.push(seriesObj)
      }
      // 数据为空清空echarts
      if (this.bondKindTrendEcharts) this.bondKindTrendEcharts.clear()
      this.bondKindTrendEcharts = echarts.init(document.getElementById('bondKindTrend'))
      this.bondKindTrendEcharts.setOption({
        title: {
          text: ''
        },
        tooltip : {
          trigger: 'axis',
        },
        legend: {
          type: 'scroll',
          data: legendData,
          x: 'center',
          y: 'bottom' ,
          itemWidth: 6,// 标志图形的长度
          itemHeight: 6,// 标志图形的宽度
          height:20,
        },
        toolbox: {
          feature: {
            dataView: {
              optionToContent: this.$fun.optionToContent
            },
            saveAsImage: {}
          }
        },
        grid: {
          left: '4%',
          right: '4%',
          bottom: '20%',
          containLabel: true
        },
        color: this.$colorArrs,
        xAxis : [
          {
            type : 'category',
            boundaryGap : false,
            data: xData
          }
        ],
        yAxis : [
          {
            name: '比例(%)',
            type: 'value',
            // max: dataMax,
            // min: dataMin
          },
        ],
        // x轴拖动
        dataZoom: [
          {
            show: true,
            realtime: true,
            start: 0,
            end: 100 ,// 结束位置（共100等份）
            bottom: '20%',
          },
          {
            type: 'inside',
            realtime: true,
            height: 25, //滚动条高度
            start: 0,
            end: 85
          }
        ],
        series: seriesArrs
      })
    },
    // 债券类属变化 new
    fun_bondConstructionTrendEcharts(){
      let trendData = this.bondConstructionTrendData
      let legend = [];
      let date = [];
      let series = [];
      trendData.forEach(function (item, index) {
        legend.push(item.typeName);
        if(item.periodAssetRatioCurve){
          date = [];//X轴
          let data = [];//记录每一列的数据
          let lineData = item.periodAssetRatioCurve;
          for(let key in lineData){
            date.push(key);
            data.push(lineData[key].toFixed(2));
          }
          let obj = {
            name: item.typeName,
            type:'line',
            data:data
          };
          series.push(obj);

        }
        else{
          let obj = {
            name: item.typeName,
            type:'line',
            data:[]
          };
          series.push(obj);
        }

      })

      if (this.bondConstructionTrendEcharts) this.bondConstructionTrendEcharts.clear()
      this.bondConstructionTrendEcharts = echarts.init(document.getElementById('bondConstructionTrend'))
      this.bondConstructionTrendEcharts.setOption({
        title: {
          text: ''
        },
        tooltip : {
          trigger: 'axis',
        },
        legend: {
          type: 'scroll',
          data: legend,
          x: 'center',
          y: 'top' ,
          left: 60,
          right: 60,
          itemWidth: 6,// 标志图形的长度
          itemHeight: 6,// 标志图形的宽度
          height:20,
        },
        toolbox: {
          feature: {
            dataView: {
              optionToContent: this.$fun.optionToContent
            },
            saveAsImage: {}
          }
        },
        grid: {
          left: '4%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        color: this.$colorArrs,
        xAxis : [
          {
            type : 'category',
            boundaryGap : false,
            data: date
          }
        ],
        yAxis : [
          {
            name: '比例(%)',
            type: 'value',
            // max: dataMax,
            // min: dataMin
          },
        ],
        // x轴拖动
        dataZoom: [
          {
            show: true,
            realtime: true,
            start: 0,
            end: 100 ,// 结束位置（共100等份）
            bottom: '3%',
          },
          {
            type: 'inside',
            realtime: true,
            height: 25, //滚动条高度
            start: 0,
            end: 85
          }
        ],
        series: series
      })
      // 获取配置信息
      let echartsOption = this.bondConstructionTrendEcharts.getOption()
			if (echartsOption.series && echartsOption.series.length) {
				// 遍历组装数据
        let { excelHeader, excelData } = forEachSeries(echartsOption)
				// excel表头
				this.excelHeader = excelHeader
				// excel数据
				this.excelData = excelData
			}
    },
    // 信用债主体评级分布
    fun_bondCreditTrendEcharts(){
      let echartData = this.investBondSubjectRatingData
      // 头部显示
      let legendData = []
      // 横坐标
      let xData = []
      // 最大值
			let dataMax = 0
			// 最小值
			let dataMin = 0
      // 数据数组
			let seriesArrs = []
      for( let key in  echartData) {
        legendData.push(key)
        if (!xData.length) {
          echartData[key].forEach(item => {
            xData.push(item.dateTime)
          })
        }
        let seriesData = []
        echartData[key].forEach(item => {
          // 百分比处理
          if (item.ratio) {
            item.ratio = fun.accMul(Number(item.ratio), 100).toFixed(2)
          } else {
            item.ratio = 0
          }
          seriesData.push(item.ratio || 0)
        })
        // 最大值
        dataMax = Math.max(...seriesData, dataMax)
        // 最小值
        dataMin = Math.min(...seriesData, dataMin)
        let seriesObj = {
          name: key,
          stack: key,
          type: 'line',
          symbolSize: 6,
          data: seriesData
        }
        seriesArrs.push(seriesObj)
      }
      // 数据为空清空echarts
      if (this.bondCreditTrendEcharts) this.bondCreditTrendEcharts.clear()
      this.bondCreditTrendEcharts = echarts.init(document.getElementById('bondCreditTrend'))
      this.bondCreditTrendEcharts.setOption({
        title: {
          text: ''
        },
        tooltip : {
          trigger: 'axis',
        },
        legend: {
          data: legendData,
          x: 'center',
          // y: 'bottom' ,
          itemWidth: 6,// 标志图形的长度
          itemHeight: 6,// 标志图形的宽度
          height:20,
        },
        toolbox: {
          feature: {
            dataView: {
              optionToContent: this.$fun.optionToContent
            },
            saveAsImage: {}
          }
        },
        grid: {
          left: '5%',
          right: '4%',
          bottom: '10%',
          containLabel: true
        },
        color: this.$colorArrs,
        xAxis : [
          {
            type : 'category',
            boundaryGap : false,
            data : xData
          }
        ],
        yAxis : [
          {
            name: '比例(%)',
            type: 'value',
            // max: dataMax,
            // min: dataMin
          },
        ],
        // x轴拖动
        dataZoom: [
          {
            show: true,
            realtime: true,
            start: 0,
            end: 100 ,//结束位置（共100等份）
            bottom: '10%',
          },
          {
            type: 'inside',
            realtime: true,
            height: 25, //滚动条高度
            start: 0,
            end: 85
          }
        ],
        series: seriesArrs
      })
      // 获取配置信息
      let echartsOption = this.bondCreditTrendEcharts.getOption()
      if (echartsOption.series && echartsOption.series.length) {
				// 遍历组装数据
				let { excelHeader, excelData } = forEachSeries(echartsOption)
				// excel表头
				this.excelHeader2 = excelHeader
				// excel数据
				this.excelData2 = excelData
			}
    },
    // 信用债债项评级分布
    fun_bondProjectTrendEcharts(){
      let echartData = this.investBondDebtRatingData
      // 头部显示
      let legendData = []
      // 横坐标
      let xData = []
      // 最大值
			let dataMax = 0
			// 最小值
			let dataMin = 0
      // 数据数组
			let seriesArrs = []
      for( let key in  echartData) {
        legendData.push(key)
        if (!xData.length) {
          echartData[key].forEach(item => {
            xData.push(item.dateTime)
          })
        }
        let seriesData = []
        echartData[key].forEach(item => {
          // 百分比处理
          if (item.ratio) {
            item.ratio = fun.accMul(Number(item.ratio), 100).toFixed(2)
          } else {
            item.ratio = 0
          }
          seriesData.push(item.ratio || 0)
        })
        // 最大值
        dataMax = Math.max(...seriesData, dataMax)
        // 最小值
        dataMin = Math.min(...seriesData, dataMin)
        let seriesObj = {
          name: key,
          stack: key,
          type: 'line',
          symbolSize: 6,
          data: seriesData
        }
        seriesArrs.push(seriesObj)
      }
      // 数据为空清空echarts
      if (this.bondProjectTrendEcharts) this.bondProjectTrendEcharts.clear()
      this.bondProjectTrendEcharts = echarts.init(document.getElementById('bondProjectTrend'))
      this.bondProjectTrendEcharts.setOption({
        title: {
          text: ''
        },
        tooltip : {
          trigger: 'axis',
        },
        legend: {
          data: legendData,
          x: 'center',
          // y: 'bottom' ,
          itemWidth: 6,// 标志图形的长度
          itemHeight: 6,// 标志图形的宽度
          height:20,
        },
        toolbox: {
          feature: {
            dataView: {
              optionToContent: this.$fun.optionToContent
            },
            saveAsImage: {}
          }
        },
        grid: {
          left: '5%',
          right: '4%',
          bottom: '10%',
          containLabel: true
        },
        color: this.$colorArrs,
        xAxis : [
          {
            type : 'category',
            boundaryGap : false,
            data : xData
          }
        ],
        yAxis : [
          {
            name: '比例(%)',
            type: 'value',
            // max: dataMax,
            // min: dataMin
          },
        ],
        // x轴拖动
        dataZoom: [
          {
            show: true,
            realtime: true,
            start: 0,
            end: 100 ,//结束位置（共100等份）
            bottom: '10%',
          },
          {
            type: 'inside',
            realtime: true,
            height: 25, //滚动条高度
            start: 0,
            end: 85
          }
        ],
        series: seriesArrs
      })
      // 获取配置信息
      let echartsOption = this.bondCreditTrendEcharts.getOption()
      if (echartsOption.series && echartsOption.series.length) {
				// 遍历组装数据
				let { excelHeader, excelData } = forEachSeries(echartsOption)
				// excel表头
				this.excelHeader3 = excelHeader
				// excel数据
				this.excelData3 = excelData
			}
    },
    // 回购占比
    fun_buyBackTrendEcharts(){
      let echartData = this.investBondBuybackRatioData
      // 头部显示
      // let legendData = []
      // 横坐标
      let xData = []
      // 最大值
			let dataMax = 0
			// 最小值
      let dataMin = 0
      let seriesData = []
      // 数据数组
      let seriesArrs = []
      echartData.forEach(item => {
        // if (!legendData.length) {
        //   legendData.push(item.name)
        // }
        xData.push(item.dateTime)
        // 百分比处理
        if (item.ratio) {
          item.ratio = fun.accMul(Number(item.ratio), 100).toFixed(2)
        } else {
          item.ratio = 0
        }
        seriesData.push(item.ratio)
        // 最大值
        dataMax = Math.max(...seriesData)
        // 最小值
        dataMin = Math.min(...seriesData)
      })
      let seriesObj = {
        name: '回购占比',
        // name: legendData[0],
        // stack: legendData[0],
        type: 'line',
        symbolSize: 6,
        data: seriesData
      }
      seriesArrs.push(seriesObj)
      // 数据为空清空echarts
      if (this.buyBackTrendEcharts) this.buyBackTrendEcharts.clear()
      this.buyBackTrendEcharts = echarts.init(document.getElementById('buyBackTrend'))
      this.buyBackTrendEcharts.setOption({
        title: {
          text: ''
        },
        tooltip : {
          trigger: 'axis',
        },
        // legend: {
        //   data: legendData,
        //   x: 'center',
        //   // y: 'bottom' ,
        //   itemWidth: 6,// 标志图形的长度
        //   itemHeight: 6,// 标志图形的宽度
        //   height:20,
        // },
        toolbox: {
          feature: {
            dataView: {
              optionToContent: this.$fun.optionToContent
            },
            saveAsImage: {}
          }
        },
        grid: {
          left: '6%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        color: this.$colorArrs,
        xAxis : [
          {
            type : 'category',
            boundaryGap : false,
            data : xData
          }
        ],
        yAxis : [
          {
            name: '回购占比(%)',
            type: 'value',
            // max: dataMax,
            // min: dataMin
          },
        ],
        // x轴拖动
        dataZoom: [
          {
            show: true,
            realtime: true,
            start: 0,
            end: 100 ,//结束位置（共100等份）
            bottom: '3%',
          },
          {
            type: 'inside',
            realtime: true,
            height: 25, //滚动条高度
            start: 0,
            end: 85
          }
        ],
        series: seriesArrs
      })
      // 获取配置信息
      let echartsOption = this.buyBackTrendEcharts.getOption()
			if (echartsOption.series && echartsOption.series.length) {
				// 遍历组装数据
				let { excelHeader, excelData } = forEachSeries(echartsOption)
				// excel表头
				this.excelHeader4 = excelHeader
				// excel数据
				this.excelData4 = excelData
			}
    },
    // 期末分布选择
    distrHandleClick(tab, event) {
      // console.log(tab, event);
      // this.$refs['formQuery'].validate((valid) => {
      //   if (valid) {
      //     if (tab.name === 'remaining') {
      //       // 投资经理视图-证券分析-债券分析-期末分布
      //       this.getInvestBondFinalDistribution()
      //     }
      //   }
      // })
    },
    // 期末分布
    fun_endDistrTrendEcharts() {
      // // 图表名字
      // let seriesName = ''
      // if (this.distr_activeName === 'generic') {
      //   seriesName = '类属'
      // } else if (this.distr_activeName === 'remaining') {
      //   seriesName = '剩余期限'
      // } else if (this.distr_activeName === 'industry') {
      //   seriesName = '行业'
      // }
      // // 期末分布
      // let nameArrs = []
      // // 饼状图数据
      // let data = []
      // this.investBondFinalDistributionData.forEach(item => {
      //   nameArrs.push(item.name)
      //   let obj = {
      //     value: Number(item.price),
      //     name: item.name
      //   }
      //   data.push(obj)
      // })

      let echartsData = this.investBondFinalDistributionData
      // 头部显示
      let legendData = []
      // 横坐标
      let xData = []
      // 最大值
      let dataMax = 0
      // 最小值
			let dataMin = 0
      // 数据数组
			let seriesArrs = []
      for (let key in echartsData) {
        legendData.push(key)
        if (!xData.length) {
          echartsData[key].forEach(item => {
            xData.push(item.dateTime)
          })
        }
        let seriesData = []
        echartsData[key].forEach(item => {
          // 万元处理
          if (item.price) {
            item.price = fun.accDiv(Number(item.price), 10000).toFixed(2)
          } else {
            item.price = 0
          }
          seriesData.push(item.price)
        })
        let seriesObj = {
          name: key,
          stack: key,
          type: 'bar',
          barWidth: 10,
          data: seriesData
        }
        // 最大值
        dataMax = Math.max(...seriesObj.data, dataMax)
        // 最小值
        dataMin = Math.min(...seriesObj.data, dataMin)
        seriesArrs.push(seriesObj)
      }
      // 数据为空清空echarts
      if (this.endDistrTrendEcharts) this.endDistrTrendEcharts.clear()
      this.endDistrTrendEcharts = echarts.init(document.getElementById('endDistrTrend'))
      this.endDistrTrendEcharts.setOption({
        title: {
          text: ''
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: legendData,
          x: 'center'
        },
        grid: {
          left: '6.5%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          feature: {
            dataView: {
              optionToContent: this.$fun.optionToContent
            },
            saveAsImage: {}
          }
        },
        color: this.$colorArrs,
        xAxis: {
          type: 'category',
          boundaryGap: true,
          data: xData
        },
        yAxis: [
          {
            name: '市值(万元)',
            type: 'value',
            // max: dataMax,
            // min: dataMin
          }
        ],
        // x轴拖动
        dataZoom: [
          {
            show: true,
            realtime: true,
            start: 0,
            end: 100 ,//结束位置（共100等份）
            bottom: '3%',
          },
          {
            type: 'inside',
            realtime: true,
            height: 25, //滚动条高度
            start: 0,
            end: 85
          }
        ],
        series: seriesArrs
      })
      // 获取配置信息
			let echartsOption = this.endDistrTrendEcharts.getOption()
      if (echartsOption.series && echartsOption.series.length) {
				// 遍历组装数据
				let { excelHeader, excelData } = forEachSeries(echartsOption)
				// excel表头
				this.excelHeader5 = excelHeader
				// excel数据
				this.excelData5 = excelData
			}
      // this.endDistrTrendEcharts.setOption({
      //   tooltip: {
      //     trigger: 'item',
      //     formatter: "{a} <br/>{b}: {c} ({d}%)"
      //   },
      //   legend: {
      //     orient: 'vertical',
      //     icon:"circle",
      //     right: 0,
      //     top: 50,
      //     itemWidth: 6,// 标志图形的长度
      //     itemHeight: 6,// 标志图形的宽度
      //     itemGap: 7 ,// 设置间距
      //     data: nameArrs,
      //     formatter: function(name) {
      //       var total = 0;
      //       var tarValue;
      //       for (var i = 0, l = data.length; i < l; i++) {
      //         total += data[i].value;
      //         if (data[i].name == name) {
      //           tarValue = data[i].value;
      //         }
      //       }
      //       let p =  0
      //       if (total) {
      //         p = (tarValue / total * 100).toFixed(2)
      //       }
      //       return name + ' ' + ' '+ tarValue+ ' ' + '亿'+ '  ' + '  ' +   p + '%';
      //     },

      //   },
      //   toolbox: {
      //     feature: {
      //       dataView: {},
      //       saveAsImage: {}
      //     }
      //   },
      //   color: this.$colorArrs,
      //   series: [
      //     {
      //       name: seriesName,
      //       type:'pie',
      //       radius: ['50%', '70%'],
      //       center: ['24%', '53%'],
      //       avoidLabelOverlap: false,
      //       label: {
      //         normal: {
      //           show: false,
      //           position: 'center',
      //         },
      //         emphasis: {
      //           show: true,
      //           textStyle: {
      //             fontSize: '14',
      //             fontWeight: 'bold'
      //           }
      //         }
      //       },
      //       labelLine: {
      //         normal: {
      //           show: false
      //         }
      //       },
      //       data: data
      //     }
      //   ]
      // })
    },
    // 组合类型列表查询
    getListEdims (type) {
      // 字典类型
      let params = type
      commonApi.edimsCommon(params).then(res => {
        let { status, data } = res.data
        if (status === 0) {
          // 组合类型查询
          if (type === 'fund_type') this.groupTypeArr = data
          // 区间查询
          if (type === 'range_type') {
            this.regionArrs = data
            // 区间默认值
            if (data.length) {
              this.formQuery2.rowNumber = data[0].dimCde
              this.formQuery3.rowNumber = data[0].dimCde
            }
          }
        }
      })
    },
    // 投资经理列表查询
    getManagerList () {
      // 权益（1）/固收（2）/混合（0）
      // 债券分析只可以选固收经理
      let params = 2
      investmentManagerApi.managerList(params).then(res => {
        let { status, data } = res.data
        if (status === 0) {
          this.manageArr = data
          if (this.manageArr.length) this.formQuery.account = this.manageArr[0].account
        }
      })
    },
    // 投资经理视图-证券分析-汇总
    investSumAnalysis () {
      let payload = {
        // 组合类型
        fundType: this.formQuery.fundType,
        // 组合代码
        fundList: this.formQuery.fundList
      }
      let params = Object.assign({}, this.formQuery)
      delete params.fundType
      delete params.fundList
      investSumAnalysisUrl(params, payload).then(res => {
        let { status, data } = res
        if (status === 0) {
          let { dateTime, netValueRatio, price } = data || {}
          // 数据日期
          this.analysisSummary.dateTime = dateTime
          // 占资产净值比
          this.analysisSummary.netValueRatio = netValueRatio || 0
          // 债券资产规模
          this.analysisSummary.price = price || 0
        }
      })
    },
    // 投资经理视图-证券分析-债券分析-前十大集中度
    investManagerFundView () {
      this.tableLoading2 = true
      let payload = {
        // 组合类型
        fundType: this.formQuery.fundType,
        // 组合代码
        fundList: this.formQuery.fundList
      }
      let params = Object.assign({
        // 选择窗口
        choiceWindow: this.con_activeName,
        // 起始页
        pageNum: this.formQuery2.pageNum,
        // 排序条件
        orderBy: this.formQuery2.orderBy,
        // 每页数量
        pageSize: this.formQuery2.pageSize,
        // 前十
        rowNumber: this.formQuery2.rowNumber,
        // 查询参数
        searchName: this.formQuery2.searchName
      }, this.formQuery)
      delete params.fundType
      delete params.fundList
      investManagerFundViewUrl(params, payload).then(res => {
        this.tableLoading2 = false
        let { status, data } = res
        if (status === 0) {
          let { list, total } = data
          this.concentrationDegreeTable = list
          this.total2 = total
          // 期末前十大集中度
          // this.fun_concentrationTrendEcharts();
        }
      }).catch(() => {
        this.tableLoading2 = false
      })
    },
    // 投资经理视图-证券分析-债券分析-前十大集中度（导出excel）
    investManagerFundViewExcel () {
      if (this.isDisabled2) return
      this.isDisabled2 = true
      this.downLoadIcon2 = 'el-icon-loading'
      this.downLoadText2 = '导出数据中...'
      let filename = ''
      if (this.con_activeName === 'bond') {
        filename = '期末集中度债券.xls'
      } else if (this.con_activeName === 'publisher') {
        filename = '期末集中度发行人.xls'
      } else if (this.con_activeName === 'issuingScale') {
        filename = '期末集中度发行规模.xls'
      }
      let payload = {
        // 组合类型
        fundType: this.formQuery.fundType,
        // 组合代码
        fundList: this.formQuery.fundList
      }
      let params = Object.assign({
        // 选择窗口
        choiceWindow: this.con_activeName,
        // 起始页
        pageNum: this.formQuery2.pageNum,
        // 排序条件
        orderBy: this.formQuery2.orderBy,
        // 每页数量
        pageSize: this.formQuery2.pageSize,
        // 前十
        rowNumber: this.formQuery2.rowNumber
      }, this.formQuery)
      delete params.fundType
      delete params.fundList
      params.pageNum = 1
      params.pageSize = 5000
      params.rowNumber = 4
      params.ex_tmp_name = filename
      investManagerFundViewExcelUrl(params, payload).then(res => {
        this.isDisabled2 = false
        this.downLoadIcon2 = 'el-icon-download'
        this.downLoadText2 = '导出数据'
        // 导出excel
        // downloadExcel(res, filename)
        let { status, data } = res
				if (status === 0) {
					if (!data) return
					this.$fun.commonDownloadUrl(data)
				}
      }).catch(() => {
        this.isDisabled2 = false
        this.downLoadIcon2 = 'el-icon-download'
        this.downLoadText2 = '导出数据'
        this.$message.error('服务器开了一会儿小差，请稍后再试')
      })
    },
    // 投资经理视图-证券分析-前十大集中度（债券/债券规模 明细）
    investBondAnalysisDetails (symbolCodeName) {
      // 组合代码
      let payload = this.formQuery.fundList
      let params = {
        // 开始时间
        beginDate: this.formQuery.beginDate,
        // 投资经理账户
        account: this.formQuery.account,
        // 组合名称/代码
        symbolCodeName: symbolCodeName,
        // 排序字段
        orderStr: this.orderStr2
      }
      investBondAnalysisDetailsUrl(params, payload).then(res => {
        let { status, data } = res
        if (status === 0) {
          this.tableData = data
        }
      })
    },
    // 投资经理视图-证券分析-前十大集中度（发行人明细）
    investPublisherAnalysisDetails (row) {
      // 组合代码
      let payload = this.formQuery.fundList
      let params = {
        // 开始时间
        beginDate: this.formQuery.beginDate,
        // 投资经理账户
        account: this.formQuery.account,
        // 发行机构
        corpName: row.corpname || '',
        // 机构评级
        levelIssue: row.issue || '',
        // 排序字段
        orderStr: this.orderStr2
      }
      investPublisherAnalysisDetailsUrl(params, payload).then(res => {
        let { status, data } = res
        if (status === 0) {
          this.tableData = data
        }
      })
    },
    // 页面点击事件2
    pagination2 (val) {
      let { page, limit } = val
      // 起始页
      this.formQuery2.pageNum = page
      // 每页数量
      this.formQuery2.pageSize = limit
      // 查询
      this.$refs['formQuery2'].validate((valid) => {
        if (valid) {
          // 投资经理视图-证券分析-债券分析-前十大集中度
          this.investManagerFundView()
        }
      })
    },
    // 页面点击事件3
    pagination3 (val) {
      let { page, limit } = val
      // 起始页
      this.formQuery3.pageNum = page
      // 每页数量
      this.formQuery3.pageSize = limit
      // 查询
      this.$refs['formQuery3'].validate((valid) => {
        if (valid) {
          // 投资经理视图-证券分析-债券分析-期末分布(行业)
          this.getInvestBondFinalDistribution()
        }
      })
    },
    // 投资经理视图-证券分析-债券分析-债券类属结构变化（左）
    getInvestBondLeftGeneric () {
      // 图表遮盖层显示
      this.bondKindTrendEchartsLoading = true
      // this.bondKindTrendEcharts.showLoading({
      //   text: '数据加载中...',
      //   color: '#319ef1',
      //   textColor: '#319ef1'
      // })
      let payload = {
        // 组合类型
        fundType: this.formQuery.fundType,
        // 组合代码
        fundList: this.formQuery.fundList
      }
      let params = Object.assign({}, this.formQuery)
      delete params.fundType
      delete params.fundList
      investBondLeftGenericUrl(params, payload).then(res => {
        // 图表遮盖层隐藏
        // this.bondKindTrendEcharts.hideLoading()
        this.bondKindTrendEchartsLoading = false
        let { status, data } = res
        if (status === 0) {
          this.investBondLeftGenericData = data
          // 债券类属变化
          this.fun_bondKindTrendEcharts();
        }
      }).catch(() => {
        // 图表遮盖层隐藏
        // this.bondKindTrendEcharts.hideLoading()
        this.bondKindTrendEchartsLoading = false
      })
    },
    // 投资经理视图-证券分析-债券分析-债券类属结构变化（右）
    getInvestBondGeneric () {
      // 图表遮盖层显示
      this.investBondGenericLoading = true
      let payload = {
        // 组合类型
        fundType: this.formQuery.fundType,
        // 组合代码
        fundList: this.formQuery.fundList
      }
      let params = Object.assign({}, this.formQuery)
      delete params.fundType
      delete params.fundList
      investBondGenericUrl(params, payload).then(res => {
        // 图表遮盖层隐藏
        this.investBondGenericLoading = false
        let { status, data } = res
        if (status === 0) {
          this.investBondGenericData = data
        }
      }).catch(() => {
        // 图表遮盖层隐藏
        this.investBondGenericLoading = false
      })
    },
    //债券类属变化接口 new
    getBondConstructionData(){
      // 图表遮盖层显示
      this.bondConstructionTrendLoading = true
      //当前选择时间默认往前推一年
      let params = {
        'beginDate' :  this.$moment(this.$moment(this.formQuery.beginDate).subtract(1,'years').format('YYYY-MM-DD')).subtract(-1,'days').format('YYYY-MM-DD'),
        'endDate' :  this.formQuery.beginDate,
      }
      let payload = {
        "algOptions": {
          "downlStandard": 0,//算法用的参数
          "equityCenterPosition": 0,//复杂动态计算 资产配置归因的
          "hs300Increase": 0,//复杂动态计算 资产配置归因的
          "needAnalyse": true, //是否计算指标 Alpha、Beta、日胜率、SortinoRatio、信息比率

          "needBiggestWithDraw": true,//needBiggestWithDraw 和 needCurve 同时设置为 true，就能计算最大回测
          "needContribution": true,//是否计算贡献度
          "needCurve": true, //是否带曲线数据
          // "riskFreeRate": 0,//算法用的参数
        },
        "excludeMap": {},
        "filterMap": {
          "operatorNO" : this.formQuery.account == -1 ? '' : this.formQuery.account, //投资经理
          "fundType" : this.formQuery.fundType.join(","), //组合类型
          "fundCode" : this.formQuery.fundList.join(","), //组合代码
        },
        "isAsc": this.isAsc,
        "orderBy": this.orderBy,
      }
      investBondGenericNewUrl(params, payload).then(res => {
        this.bondConstructionTrendLoading = false
        let { status, data } = res
        if (status === 0) {
          this.bondConstructionTrendData = data
          // 债券类属变化
          this.fun_bondConstructionTrendEcharts();
        }
      }).catch(() => {
        //报错清空echarts 和 table
        this.bondConstructionTrendData = [];
        // 债券类属变化
        this.fun_bondConstructionTrendEcharts();
        this.bondConstructionTrendLoading = false
      })


    },
    //债券类属变化右侧table排序 new
    bondConstructionTrendDataSort(val){
      let self = this;
      self.isAsc = self.$fun.moveOrderByString(val).isAsc;
      self.orderBy = self.$fun.moveOrderByString(val).orderBy;
      //调用后端排序
      self.getBondConstructionData();
    },
    // 投资经理视图-证券分析-债券分析-主体评级
    getInvestBondSubjectRating () {
      // 图表遮盖层显示
      this.bondCreditTrendEchartsLoading = true
      let payload = {
        // 组合类型
        fundType: this.formQuery.fundType,
        // 组合代码
        fundList: this.formQuery.fundList
      }
      let params = Object.assign({}, this.formQuery)
      delete params.fundType
      delete params.fundList
      investBondSubjectRatingUrl(params, payload).then(res => {
        // 图表遮盖层隐藏
        this.bondCreditTrendEchartsLoading = false
        let { status, data } = res
        if (status === 0) {
          this.investBondSubjectRatingData = data
          // 信用债主体评级分布
          this.fun_bondCreditTrendEcharts()
        }
      }).catch(() => {
        // 图表遮盖层隐藏
        this.bondCreditTrendEchartsLoading = false
      })
    },
    // 投资经理视图-证券分析-债券分析-债项评级
    getInvestBondDebtRating () {
      // 图表遮盖层显示
      this.bondProjectTrendEchartsLoading = true
      let payload = {
        // 组合类型
        fundType: this.formQuery.fundType,
        // 组合代码
        fundList: this.formQuery.fundList
      }
      let params = Object.assign({}, this.formQuery)
      delete params.fundType
      delete params.fundList
      investBondDebtRatingUrl(params, payload).then(res => {
        // 图表遮盖层隐藏
        this.bondProjectTrendEchartsLoading = false
        let { status, data } = res
        if (status === 0) {
          this.investBondDebtRatingData = data
          // 信用债债项评级分布
          this.fun_bondProjectTrendEcharts()
        }
      }).catch(() => {
        // 图表遮盖层隐藏
        this.bondProjectTrendEchartsLoading = false
      })
    },
    // 投资经理视图-证券分析-债券分析-回购占比
    getInvestBondBuybackRatio () {
      // 图表遮盖层显示
      this.buyBackTrendEchartsLoading = true
      let payload = {
        // 组合类型
        fundType: this.formQuery.fundType,
        // 组合代码
        fundList: this.formQuery.fundList
      }
      let params = Object.assign({}, this.formQuery)
      delete params.fundType
      delete params.fundList
      investBondBuybackRatioUrl(params, payload).then(res => {
        // 图表遮盖层隐藏
        this.buyBackTrendEchartsLoading = false
        let { status, data } = res
        if (status === 0) {
          this.investBondBuybackRatioData = data
          if (data.length) this.buyBackTrendRatiosFinal = data[data.length - 1].ratio || 0
          // 回购占比
          this.fun_buyBackTrendEcharts()
        }
      }).catch(() => {
        // 图表遮盖层隐藏
        this.buyBackTrendEchartsLoading = false
      })
    },
    // 投资经理视图-证券分析-债券分析-期末分布(剩余期限)
    getInvestBondTerminalTime () {
      // 图表遮盖层显示
      this.endDistrTrendEchartsLoading = true
      let payload = {
        // 组合类型
        fundType: this.formQuery.fundType,
        // 组合代码
        fundList: this.formQuery.fundList
      }
      let params = Object.assign({
        // // 起始页
        // pageNum: this.formQuery3.pageNum,
        // // 每页数量
        // pageSize: this.formQuery3.pageSize,
        // // 排序条件
        // orderStr: this.formQuery3.orderStr,
        // // 前十
        // rowNumber: this.formQuery3.rowNumber
      }, this.formQuery)
      // 清除空字段
			for (let k in params) {
				if (!params[k] && String(params[k]) !== '0') {
					delete params[k]
				}
			}
      delete params.fundType
      delete params.fundList
      investBondTerminalTimeUrl(params, payload).then(res => {
        // 图表遮盖层隐藏
        this.endDistrTrendEchartsLoading = false
        let { status, data } = res
        if (status === 0) {
          this.investBondFinalDistributionData = data
          // 期末分布
          this.fun_endDistrTrendEcharts()
        }
      }).catch(() => {
        // 图表遮盖层隐藏
        this.endDistrTrendEchartsLoading = false
      })
    },
    // 投资经理视图-证券分析-债券分析-期末分布(行业)
    getInvestBondFinalDistribution (flag) {
      if (!flag) {
        this.tableLoading = true
      } else {
        if (this.isDisabled) return
        this.isDisabled = true
        this.downLoadIcon = 'el-icon-loading'
        this.downLoadText = '导出数据中...'
      }
      let payload = {
        // 组合类型
        fundType: this.formQuery.fundType,
        // 组合代码
        fundList: this.formQuery.fundList
      }
      let params = Object.assign({
        // 起始页
        pageNum: this.formQuery3.pageNum,
        // 每页数量
        pageSize: this.formQuery3.pageSize,
        // 排序条件
        orderStr: this.formQuery3.orderStr,
        // 前十
        rowNumber: this.formQuery3.rowNumber
      }, this.formQuery)
      // 清除空字段
			for (let k in params) {
				if (!params[k] && String(params[k]) !== '0') {
					delete params[k]
				}
			}
      delete params.fundType
      delete params.fundList
      if (flag) {
        params.pageNum = 1
        params.pageSize = 5000
        params.rowNumber = 4
        params.ex_tmp_name = '期末分布行业.xls'
      }
      investBondFinalDistributionUrl(params, payload).then(res => {
        this.tableLoading = false
        this.isDisabled = false
        this.downLoadIcon = 'el-icon-download'
        this.downLoadText = '导出数据'
        let { status, data } = res
        if (status === 0) {
          if (flag) { // 下载excel
            if (!data) return
					  this.$fun.commonDownloadUrl(data)
          } else {
            let { total, list } = data
            // 列表数据
            this.investBondFinalDistributionData2 = list
            this.total3 = total
          }
        }
      }).catch(() => {
        this.tableLoading = false
        this.isDisabled = false
        this.downLoadIcon = 'el-icon-download'
        this.downLoadText = '导出数据'
      })
    },
    // 当某一行被点击时会触发该事件
    rowClick (row, column, event) {
      // 当点击的是债券名称/债券代码显示弹窗
      if (column.property === 'symbolName'
            || column.property === 'symbolCode'
      ) {
        // 显示弹窗
        this.dialogMask = true
        // 标题
        this.dialogTitle = `${row.symbolCode || '未知代码'}-${row.symbolName || '未知名称'}-${row.typeName || '未知类型'}`
        // 保存表格传递值
        this.saveStr = event.target.textContent
        // 投资经理视图-证券分析-前十大集中度（债券/债券规模 明细）
        this.investBondAnalysisDetails(event.target.textContent || '')
      }
      // 当点击的是发行机构显示弹窗
      if (column.property === 'corpname') {
        // 显示弹窗
        this.dialogMask = true
        // 标题
        this.dialogTitle = `${row.corpname || ''}`
        // 保存表格传递值
        this.saveStr = row
        // 投资经理视图-证券分析-前十大集中度（发行人明细）
        this.investPublisherAnalysisDetails(row)
      }
    },
    // 当表格的排序条件发生变化的时候会触发该事件
    handleSortChange (val) {
      let orderBy = ''
      if (val.order === 'ascending') {
        orderBy = `"${val.prop}" nulls last` // 升序
      } else {
        orderBy = `"${val.prop}" desc nulls last` // 降序
      }
      this.formQueryOrderBy[this.con_activeName] = orderBy
      this.formQuery2.orderBy = orderBy
      // 查询2
      this.onQuery2()
    },
    // 当表格的排序条件发生变化的时候会触发该事件
    handleBondSortChange (val) {
      if (val.order === 'ascending') {
        this.formQuery3.orderStr = `"${val.prop}" nulls last` // 升序
      } else {
        this.formQuery3.orderStr = `"${val.prop}" desc nulls last` // 降序
      }
      // 查询
      this.onQuery3()
    },
    // 当表格的排序条件发生变化的时候会触发该事件
    handleInvestBondSortChange (val) {
      // 债券/发行人排序字段
      this.orderStr2 = `"symbolPrice" desc nulls last`
      if (val.order === 'ascending') {
        this.orderStr2 = `"${val.prop}" nulls last` // 升序
      } else {
        this.orderStr2 = `"${val.prop}" desc nulls last` // 降序
      }
      // 当点击的是债券名称/债券代码显示弹窗
      if (this.con_activeName === 'bond') {
        // 投资经理视图-证券分析-前十大集中度（债券/债券规模 明细）
        this.investBondAnalysisDetails(this.saveStr || '')
      }
      // 当点击的是发行机构显示弹窗
      if (this.con_activeName === 'publisher') {
        // 投资经理视图-证券分析-前十大集中度（发行人明细）
        this.investPublisherAnalysisDetails(this.saveStr)
      }
    },
    // 图表变化
    echartsResize () {
      if (this.concentrationTrendEcharts) this.concentrationTrendEcharts.resize()
      // if (this.bondKindTrendEcharts) this.bondKindTrendEcharts.resize()
      //债券类属结构变化 new
      if (this.bondConstructionTrendEcharts) this.bondConstructionTrendEcharts.resize()
      if (this.bondCreditTrendEcharts) this.bondCreditTrendEcharts.resize()
      if (this.bondProjectTrendEcharts) this.bondProjectTrendEcharts.resize()
      if (this.buyBackTrendEcharts) this.buyBackTrendEcharts.resize()
      if (this.endDistrTrendEcharts) this.endDistrTrendEcharts.resize()
    },
    // 导出excel
		exportExcelFile () {
			const excelHeader = this.excelHeader
			const excelData = this.excelData
			const filename = '债券类属结构变化'
			exportExcel(excelHeader, excelData, filename)
    },
    // 导出excel2
		exportExcelFile2 () {
			const excelHeader = this.excelHeader2
			const excelData = this.excelData2
			const filename = '信用债主体评级分布'
			exportExcel(excelHeader, excelData, filename)
    },
    // 导出excel3
		exportExcelFile3 () {
			const excelHeader = this.excelHeader3
			const excelData = this.excelData3
			const filename = '信用债债项评级分布'
			exportExcel(excelHeader, excelData, filename)
    },
    // 导出excel4
		exportExcelFile4 () {
			const excelHeader = this.excelHeader4
			const excelData = this.excelData4
			const filename = '回购占比'
			exportExcel(excelHeader, excelData, filename)
    },
    // 导出excel5
		exportExcelFile5 () {
			const excelHeader = this.excelHeader5
			const excelData = this.excelData5
			const filename = '期末分布'
			exportExcel(excelHeader, excelData, filename)
    },
    // 表格导出excel
    downloadTableExcel () {
      this.$refs['formQuery2'].validate((valid) => {
        if (valid) {
          // 投资经理视图-证券分析-债券分析-前十大集中度（导出excel）
          this.investManagerFundViewExcel()
        }
      })
    },
    // 表格导出excel2
    downloadTableExcel2 () {
      // 投资经理视图-证券分析-债券分析-期末分布（导出excel）
      this.$refs['formQuery3'].validate((valid) => {
        if (valid) {
          // 投资经理视图-证券分析-债券分析-期末分布(行业)
          this.getInvestBondFinalDistribution(true)
        }
      })
    }
  },
  watch: {
    // 监听组合类型变化
    'formQuery.fundType' (val, oldval) {
      if (val.indexOf('*') != -1 && oldval.indexOf('*') == -1 && val.length > 1) {
        this.formQuery.fundType = ['*']
      } else if (val.indexOf('*') != -1 && oldval.indexOf('*') != -1 && val.length > 1){
        this.formQuery.fundType.splice(val.indexOf('*'), 1)
      }
    },
    // 监听组合代码变化
    fundCode () {
      this.formQuery.fundList = [this.fundCode]
      // 查询
      this.onQuery()
      this.onQuery2()
      this.onQuery3()
    },
    // 监听左侧栏
    echartsOpenChild () {
      let timer = setTimeout(() => {
				// 宽度变化重新渲染图表
				this.echartsResize()
				clearTimeout(timer)
			},500)
    }
  }
}

</script>

<style lang="scss">
.bondAnalysis{
  .tabContent{
    position: relative;
    .tabVisible{
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      visibility: hidden;
    }
    .visible{
      visibility: visible;
    }
  }
  .minH444{
    min-height: 444px;
  }
  .min300{
    min-height: 300px;
  }
  .el-dialog{
		width: 70%!important;
	}
  .blue{
    color: #409EFF;
    cursor: pointer;
  }
  .termAverageone_box li{
    height: 25px;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .termAverageone_box span{
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: #3f3f3f;
  }
  .termAveragetwo_box{
    width: 100%;
  }
  .termAveragetwo_box li{
    display: block;
    height: 25px;
    line-height: 25px;
    font-size: 14px;
    color: #3f3f3f;
  }
  .termAveragetwo_box li:nth-child(1){
    font-weight: 600;
    font-size: 14px;
  }
}


</style>

<template>
  <div class="kpi_tem vxe_custom_style">
    <div class="kpi_top">
      <h3 class="title"><span>{{deptName || ' '}}</span>-国泰君安证券股份有限公司</h3>
      <h3 class="title">公募运营外包服务月度评估报表</h3>
      <div class="search_form">
        <el-date-picker
          v-model="historyDate"
          value-format="yyyy-MM"
          @change="historyDateChange"
          type="month"
          size="small"
          placeholder="选择月">
        </el-date-picker>
        <el-button style="margin-top:3px;" size="small" @click="getList(historyDate)">查询</el-button>
      </div>
    </div>
    <p class="title_one">一、总体概览</p>
    <p class="title_two">1、账户概述</p>
    <!-- 1.1 公司规模概况 -->
    <p class="title_three">1.1 公司规模概况</p>
    <!-- <div>
      <el-button
        @click="insertEvent('xTable1')"
        size="small"
        icon="el-icon-plus"
        >新增</el-button
      >
    </div> -->
    <vxe-table
      border
      resizable
      v-loading="tableLoading"
      :data="tableData1"
      size="mini"
      ref="xTable1"
      class="vxeTable"
      :cell-style="xTable1CellStyle"
      :cell-class-name="cellClassName"
      :header-cell-class-name="headerCellClassName"
      :scroll-y="{ enabled: false }"
      :edit-config="{ trigger: isSubmit!='1'?'click':'', mode: 'cell', showIcon: false }"
    >
      <vxe-table-column field="fundType" title="产品类别">
        <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.fundType" autosize></el-input>
        </template>
      </vxe-table-column>
      <vxe-table-column
        field="eTermScale"
        :title="`${yyyy}年${mm}月期末规模`"
      >
        <template slot="edit" slot-scope="{ row }">
          <el-input
            type="textarea"
            v-model="row.eTermScale"
            autosize
          ></el-input>
        </template>
      </vxe-table-column>
      <vxe-table-column field="indInvestors" title="个人投资者数量">
        <template slot="edit" slot-scope="{ row }">
          <el-input
            type="textarea"
            v-model="row.indInvestors"
            autosize
          ></el-input>
        </template>
      </vxe-table-column>
      <vxe-table-column field="insInvestors" title="机构投资者数量" >
        <template slot="edit" slot-scope="{ row }">
          <el-input
            type="textarea"
            v-model="row.insInvestors"
            autosize
          ></el-input>
        </template>
      </vxe-table-column>
      <vxe-table-column
        field="subscriptionInto"
        title="本期申购/转入量"
      >
        <template slot="edit" slot-scope="{ row }">
          <el-input
            type="textarea"
            v-model="row.subscriptionInto"
            autosize
          ></el-input>
        </template>
      </vxe-table-column>
      <vxe-table-column
        field="subscriptionOut"
        title="本期赎回/转出量"
      >
        <template slot="edit" slot-scope="{ row }">
          <el-input
            type="textarea"
            v-model="row.subscriptionOut"
            autosize
          ></el-input>
        </template>
      </vxe-table-column>
      <vxe-table-column field="remark" title="备注" :edit-render="{}">
        <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.remark" autosize></el-input>
        </template>
      </vxe-table-column>
    </vxe-table>

    <!-- 1.2 产品运营概况 -->
    <p class="title_three">1.2 产品运营概况</p>
    <!-- <div>
      <el-button
        @click="insertEvent('xTable2')"
        size="small"
        icon="el-icon-plus"
        >新增</el-button
      >
    </div> -->
    <vxe-table
      border
      resizable
      v-loading="tableLoading"
      :data="tableData2"
      ref="xTable2"
      size="mini"
      class="vxeTable"
      :cell-style="xTable2CellStyle"
      :cell-class-name="cellClassName"
      :header-cell-class-name="headerCellClassName"
      :scroll-y="{ enabled: false }"
      :edit-config="{ trigger: isSubmit!='1'?'click':'', mode: 'cell', showIcon: false }"
    >
      <vxe-table-column field="fundName" title="产品名称" >
        <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.fundName" autosize></el-input>
        </template>
      </vxe-table-column>
      <vxe-table-column
        field="eTermScale"
        :title="`${yyyy}年${mm}月期末规模`"
      >
        <template slot="edit" slot-scope="{ row }">
          <el-input
            type="textarea"
            v-model="row.eTermScale"
            autosize
          ></el-input>
        </template>
      </vxe-table-column>
      <vxe-table-column field="indInvestors" title="个人投资者数量" >
        <template slot="edit" slot-scope="{ row }">
          <el-input
            type="textarea"
            v-model="row.indInvestors"
            autosize
          ></el-input>
        </template>
      </vxe-table-column>
      <vxe-table-column field="insInvestors" title="机构投资者数量" >
        <template slot="edit" slot-scope="{ row }">
          <el-input
            type="textarea"
            v-model="row.insInvestors"
            autosize
          ></el-input>
        </template>
      </vxe-table-column>
      <vxe-table-column
        field="subscriptionInto"
        title="本期申购/转入量"
      >
        <template slot="edit" slot-scope="{ row }">
          <el-input
            type="textarea"
            v-model="row.subscriptionInto"
            autosize
          ></el-input>
        </template>
      </vxe-table-column>
      <vxe-table-column
        field="subscriptionOut"
        title="本期赎回/转出量"
      >
        <template slot="edit" slot-scope="{ row }">
          <el-input
            type="textarea"
            v-model="row.subscriptionOut"
            autosize
          ></el-input>
        </template>
      </vxe-table-column>
      <vxe-table-column field="explain" title="开放情况说明" :edit-render="{}">
        <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.explain" autosize></el-input>
        </template>
      </vxe-table-column>
    </vxe-table>

    <!-- 1.2 产品运营操作类概况 -->
    <p class="title_three">1.3 产品运营操作类概况</p>
    <!-- <div>
      <el-button
        @click="insertEvent('xTable3')"
        size="small"
        icon="el-icon-plus"
        >新增</el-button
      >
    </div> -->
    <vxe-table
      border
      resizable
      v-loading="tableLoading"
      :data="tableData3"
      ref="xTable3"
      size="mini"
      class="vxeTable"
      :cell-class-name="cellClassName"
      :header-cell-class-name="headerCellClassName"
      :scroll-y="{ enabled: false }"
      :edit-config="{ trigger: isSubmit!='1'?'click':'', mode: 'cell', showIcon: false }"
    >
      <vxe-table-column field="context" title="操作内容" >
        <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.context" autosize></el-input>
        </template>
      </vxe-table-column>
      <vxe-table-column
        field="thisPeriod"
        :title="newDate?`${newDate}(本期)`:`${yyyy}年${mm}月(本期)`"
      >
        <template slot="edit" slot-scope="{ row }">
          <el-input
            type="textarea"
            v-model="row.thisPeriod"
            autosize
          ></el-input>
        </template>
      </vxe-table-column>
      <vxe-table-column
        field="priorPeriod"
        :title="`${beforeDate}(上期)`"
      >
        <template slot="edit" slot-scope="{ row }">
          <el-input
            type="textarea"
            v-model="row.priorPeriod"
            autosize
          ></el-input>
        </template>
      </vxe-table-column>
      <vxe-table-column field="growthRate" title="较上期增长率" >
        <template slot="edit" slot-scope="{ row }">
          <el-input
            type="textarea"
            v-model="row.growthRate"
            autosize
          ></el-input>
        </template>
      </vxe-table-column>
      <vxe-table-column field="remark" title="备注" :edit-render="{}">
        <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.remark" autosize></el-input>
        </template>
      </vxe-table-column>
    </vxe-table>

    <p class="title_two">2、RAG 摘要</p>
    <!-- <ul class="rag_zhaiyao">
      <li><div class="zhaiyao_name"></div><div class="zhaiyao_val">2020年XX月</div></li>
      <li><div class="zhaiyao_name">估值核算服务</div><div class="zhaiyao_val"></div></li>
      <li><div class="zhaiyao_name">份额登记服务</div><div class="zhaiyao_val"></div></li>
      <li><div class="zhaiyao_name">TA资金清算服务</div><div class="zhaiyao_val"></div></li>
      <li><div class="zhaiyao_name">信息披露数据服务</div><div class="zhaiyao_val"></div></li>
      <li><div class="zhaiyao_name">运营支持服务</div><div class="zhaiyao_val"></div></li>
      <li><div class="zhaiyao_name">其他服务</div><div class="zhaiyao_val"></div></li>
    </ul> -->

    <vxe-table
      border
      resizable
      v-loading="tableLoading"
      :data="tableDataRAG"
      ref="xTableRAG"
      size="mini"
      class="vxeTable"
      style="width: 30%"
      :cell-style="RAGcellStyle"
      :cell-class-name="cellClassName"
      :header-cell-class-name="headerCellClassName"
      :scroll-y="{ enabled: false }"
      :edit-config="{ trigger: isSubmit!='1'?'':'', mode: 'cell', showIcon: false }"
    >
      <vxe-table-column field="services" title=""></vxe-table-column>
      <vxe-table-column field="grade" :title="`${yyyy}年${mm}月`" :edit-render="{}">
        <template slot="edit" slot-scope="{ row }">
          <vxe-select v-model="row.grade" placeholder="请选择下拉" transfer>
            <vxe-option
              v-for="(item, index) in colorArr"
              :key="index"
              :value="item.value"
              :label="item.label"
              :class-name="item.value"
              :style="{ backgroundColor: item.value }"
            >
            </vxe-option>
            <!-- <vxe-option 
                v-for="(item, index) in colorArr"
                :key="index"
                :value="item.value"
                :label="item.label"
              >
                <template #default="{ option }">
                  <span :style="{color: 'red'}">
                    <span>1111{{ option.label }}</span>
                  </span>
                </template>
              </vxe-option> -->
          </vxe-select>
        </template>
      </vxe-table-column>
    </vxe-table>

    <div class="zhaiyao_tuli">
      <div>图例：</div>
      <div class="zhaiyao_tuli_item">
        <span>差错</span>
        <div class="red box"></div>
      </div>
      <div class="zhaiyao_tuli_item">
        <span>有待改进</span>
        <div class="yellow box"></div>
      </div>
      <div class="zhaiyao_tuli_item">
        <span>合理</span>
        <div class="green box"></div>
      </div>
    </div>

    <!-- 二、服务水平指标 -->
    <p class="title_one">二、服务水平指标</p>
    <p class="title_two">2.1估值核算及信息披露</p>
    <!-- <div>
      <el-button
        @click="insertEvent('xTable4')"
        size="small"
        icon="el-icon-plus"
        >新增</el-button
      >
    </div> -->
    <vxe-table
      border
      resizable
      v-loading="tableLoading"
      :data="tableData4"
      ref="xTable4"
      size="mini"
      class="vxeTable"
      @edit-actived="editActived"
      :cell-class-name="cellClassName"
      :header-cell-class-name="headerCellClassName"
      :cell-style="cellStyle"
      :scroll-y="{ enabled: false }"
      :edit-config="{ trigger: isSubmit!='1'?'click':'', mode: 'cell', showIcon: false }"
    >
      <vxe-table-column field="kpiName" title="关键绩效指标（KPI）">
        <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.kpiName" autosize></el-input>
        </template>
      </vxe-table-column>

      <vxe-table-column
        field="thisGrade"
        :title="newDate?newDate:`${yyyy}年${mm}月`"
        :edit-render="{}"
      >
        <template slot="edit" slot-scope="{ row }">
          <!-- <el-input type="number" v-model="row.thisGrade" :min="0" :max="100" ></el-input> -->
          <!-- <el-input-number v-model="row.thisGrade" :min="0" :max="100" label=""></el-input-number> -->
          <vxe-input v-model="row.thisGrade" placeholder="" type="number" step="1" min="0" max="100" @change="thisGradeChange"></vxe-input>
        </template>
        <template slot="default" slot-scope="{ row }">
          <span>{{ row.thisGrade }}</span
          ><span v-if="row.thisGrade">%</span>
        </template>
      </vxe-table-column>

      <vxe-table-column field="priorGrade" :title="beforeDate" >
        <!-- <template slot="edit" slot-scope="{ row }">
          <el-input
            type="textarea"
            v-model="row.priorGrade"
            autosize
          ></el-input>
        </template> -->
        <template slot="default" slot-scope="{ row }">
          <span>{{ row.priorGrade }}</span
          ><span v-if="row.priorGrade || row.priorGrade===0">%</span>
        </template>
      </vxe-table-column>
      
      <vxe-table-column field="explain" title="指标说明">
        <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.explain" autosize></el-input>
        </template>
      </vxe-table-column>
      <vxe-table-column field="trend" title="趋势">
        <template slot-scope="{ row }">
          <!-- <span>{{row.trend}}</span> -->
          <span v-if="row.trend=='上升'"> <i class="fa fa-long-arrow-up" style="color:rgb(0, 176, 80);font-size:40px;"></i> </span>
          <span v-else-if="row.trend=='下降'"> <i class="fa fa-long-arrow-down" style="color:rgb(255, 0, 0);font-size:40px;"></i> </span>
          <span v-else-if="row.trend=='-'"> <i class="fa fa-arrows-h" style="color:rgb(0, 176, 80);font-size:40px;"></i> </span>
          <span v-else> {{row.trend}} </span>
        </template>
      </vxe-table-column>
      <vxe-table-column
        field="grade1"
        title="红黄绿（RAG）标识"
        :edit-render="{
          name: '$select',
          options: colorArr2,
          events: { change: gradeChange },
        }"
      >
        <!-- <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.grade" autosize></el-input>
        </template> -->
        <!-- <template slot="edit" slot-scope="{ row }">
            <vxe-select
              v-model="row.grade"
              placeholder="请选择下拉"
              transfer
              @change="gradeChange(row)"
            >
              <vxe-option
                v-for="(item, index) in colorArr"
                :key="index"
                :value="item.value"
                :label="item.label"
                :class-name="item.value"
                :style="{backgroundColor:item.value}"
              >
              </vxe-option>
            </vxe-select>
          </template> -->
      </vxe-table-column>
      <vxe-table-column field="remark" title="备注" :edit-render="{}">
        <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.remark" autosize></el-input>
        </template>
      </vxe-table-column>
    </vxe-table>

    <p class="title_two">2.2份额登记及TA资金清算</p>
    <!-- <div>
      <el-button
        @click="insertEvent('xTable5')"
        size="small"
        icon="el-icon-plus"
        >新增</el-button
      >
    </div> -->
    <vxe-table
      border
      resizable
      v-loading="tableLoading"
      :data="tableData5"
      ref="xTable5"
      size="mini"
      class="vxeTable"
      @edit-actived="editActived"
      :cell-class-name="cellClassName"
      :header-cell-class-name="headerCellClassName"
      :cell-style="cellStyle"
      :scroll-y="{ enabled: false }"
      :edit-config="{ trigger: isSubmit!='1'?'click':'', mode: 'cell', showIcon: false }"
    >
      <vxe-table-column field="kpiName" title="关键绩效指标（KPI）">
        <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.kpiName" autosize></el-input>
        </template>
      </vxe-table-column>

      <vxe-table-column
        field="thisGrade"
        :title="newDate?newDate:`${yyyy}年${mm}月`"
        :edit-render="{}"
      >
        <template slot="edit" slot-scope="{ row }">
          <!-- <el-input type="number" v-model="row.thisGrade" autosize ></el-input> -->
          <!-- <el-input-number v-model="row.thisGrade" :min="0" :max="100" label=""></el-input-number> -->
          <vxe-input v-model="row.thisGrade" placeholder="" type="number" step="1" min="0" max="100" @change="thisGradeChange"></vxe-input>
        </template>
        <template slot="default" slot-scope="{ row }">
          <span>{{ row.thisGrade }}</span
          ><span v-if="row.thisGrade">%</span>
        </template>
      </vxe-table-column>

      <vxe-table-column field="priorGrade" :title="beforeDate" >
        <!-- <template slot="edit" slot-scope="{ row }">
          <el-input
            type="textarea"
            v-model="row.priorGrade"
            autosize
          ></el-input>
        </template> -->
        <template slot="default" slot-scope="{ row }">
          <span>{{ row.priorGrade }}</span
          ><span v-if="row.priorGrade || row.priorGrade===0">%</span>
        </template>
      </vxe-table-column>
      
      <vxe-table-column field="explain" title="指标说明">
        <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.explain" autosize></el-input>
        </template>
      </vxe-table-column>
      <vxe-table-column field="trend" title="趋势">
        <template slot-scope="{ row }">
          <!-- <span>{{row.trend}}</span> -->
          <span v-if="row.trend=='上升'"> <i class="fa fa-long-arrow-up" style="color:rgb(0, 176, 80);font-size:40px;"></i> </span>
          <span v-else-if="row.trend=='下降'"> <i class="fa fa-long-arrow-down" style="color:rgb(255, 0, 0);font-size:40px;"></i> </span>
          <span v-else-if="row.trend=='-'"> <i class="fa fa-arrows-h" style="color:rgb(0, 176, 80);font-size:40px;"></i> </span>
          <span v-else> {{row.trend}} </span>
        </template>
      </vxe-table-column>
      <vxe-table-column
        field="grade1"
        title="红黄绿（RAG）标识"
        :edit-render="{
          name: '$select',
          options: colorArr2,
          events: { change: gradeChange },
        }"
      >
      </vxe-table-column>
      <vxe-table-column field="remark" title="备注" :edit-render="{}">
        <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.remark" autosize></el-input>
        </template>
      </vxe-table-column>
    </vxe-table>

    <!-- 2.3 运营支持 -->
    <p class="title_two">2.3 运营支持</p>
    <!-- <div>
      <el-button
        @click="insertEvent('xTable6')"
        size="small"
        icon="el-icon-plus"
        >新增</el-button
      >
    </div> -->
    <vxe-table
      border
      resizable
      v-loading="tableLoading"
      :data="tableData6"
      ref="xTable6"
      size="mini"
      class="vxeTable"
      @edit-actived="editActived"
      :cell-class-name="cellClassName"
      :header-cell-class-name="headerCellClassName"
      :cell-style="cellStyle"
      :scroll-y="{ enabled: false }"
      :edit-config="{ trigger: isSubmit!='1'?'click':'', mode: 'cell', showIcon: false }"
    >
      <vxe-table-column field="kpiName" title="关键绩效指标（KPI）">
        <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.kpiName" autosize></el-input>
        </template>
      </vxe-table-column>

      <vxe-table-column
        field="thisGrade"
        :title="newDate?newDate:`${yyyy}年${mm}月`"
        :edit-render="{}"
      >
        <template slot="edit" slot-scope="{ row }">
          <!-- <el-input type="number" v-model="row.thisGrade" ></el-input> -->
          <!-- <el-input-number v-model="row.thisGrade" :min="0" :max="100" label=""></el-input-number> -->
          <vxe-input v-model="row.thisGrade" placeholder="" type="number" step="1" min="0" max="100" @change="thisGradeChange"></vxe-input>
        </template>
        <template slot="default" slot-scope="{ row }">
          <span>{{ row.thisGrade }}</span
          ><span v-if="row.thisGrade">%</span>
        </template>
      </vxe-table-column>

      <vxe-table-column field="priorGrade" :title="beforeDate" >
        <!-- <template slot="edit" slot-scope="{ row }">
          <el-input
            type="textarea"
            v-model="row.priorGrade"
            autosize
          ></el-input>
        </template> -->
        <template slot="default" slot-scope="{ row }">
          <span>{{ row.priorGrade }}</span
          ><span v-if="row.priorGrade || row.priorGrade===0">%</span>
        </template>
      </vxe-table-column>
      
      <vxe-table-column field="explain" title="指标说明">
        <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.explain" autosize></el-input>
        </template>
      </vxe-table-column>
      <vxe-table-column field="trend" title="趋势">
        <template slot-scope="{ row }">
          <!-- <span>{{row.trend}}</span> -->
          <span v-if="row.trend=='上升'"> <i class="fa fa-long-arrow-up" style="color:rgb(0, 176, 80);font-size:40px;"></i> </span>
          <span v-else-if="row.trend=='下降'"> <i class="fa fa-long-arrow-down" style="color:rgb(255, 0, 0);font-size:40px;"></i> </span>
          <span v-else-if="row.trend=='-'"> <i class="fa fa-arrows-h" style="color:rgb(0, 176, 80);font-size:40px;"></i> </span>
          <span v-else> {{row.trend}} </span>
        </template>
      </vxe-table-column>
      <vxe-table-column
        field="grade1"
        title="红黄绿（RAG）标识"
        :edit-render="{
          name: '$select',
          options: colorArr2,
          events: { change: gradeChange },
        }"
      >
      </vxe-table-column>
      <vxe-table-column field="remark" title="备注" :edit-render="{}">
        <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.remark" autosize></el-input>
        </template>
      </vxe-table-column>
    </vxe-table>

    <!-- 三、综合保障指标 -->
    <p class="title_one">三、综合保障指标</p>
    <!-- <div>
      <el-button
        @click="insertEvent('xTable7')"
        size="small"
        icon="el-icon-plus"
        >新增</el-button
      >
    </div> -->
    <vxe-table
      border
      resizable
      v-loading="tableLoading"
      :data="tableData7"
      ref="xTable7"
      size="mini"
      class="vxeTable"
      @edit-actived="editActived"
      :cell-class-name="cellClassName"
      :header-cell-class-name="headerCellClassName"
      :cell-style="cellStyle"
      :scroll-y="{ enabled: false }"
      :edit-config="{ trigger: isSubmit!='1'?'click':'', mode: 'cell', showIcon: false }"
    >
      <vxe-table-column field="kpiName" title="关键绩效指标（KPI）">
        <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.kpiName" autosize></el-input>
        </template>
      </vxe-table-column>

      <vxe-table-column
        field="thisGrade"
        :title="newDate?newDate:`${yyyy}年${mm}月`"
        :edit-render="{}"
      >
        <template slot="edit" slot-scope="{ row }">
          <!-- <el-input type="number" v-model="row.thisGrade" autosize ></el-input> -->
          <!-- <el-input-number v-model="row.thisGrade" :min="0" :max="100" label=""></el-input-number> -->
          <vxe-input v-model="row.thisGrade" placeholder="" type="number" step="1" min="0" max="100" @change="thisGradeChange"></vxe-input>
        </template>
        <template slot="default" slot-scope="{ row }">
          <span>{{ row.thisGrade }}</span
          ><span v-if="row.thisGrade">%</span>
        </template>
      </vxe-table-column>

      <vxe-table-column field="priorGrade" :title="beforeDate" >
        <!-- <template slot="edit" slot-scope="{ row }">
          <el-input
            type="textarea"
            v-model="row.priorGrade"
            autosize
          ></el-input>
        </template> -->
        <template slot="default" slot-scope="{ row }">
          <span>{{ row.priorGrade }}</span
          ><span v-if="row.priorGrade || row.priorGrade===0">%</span>
        </template>
      </vxe-table-column>
      
      <vxe-table-column field="explain" title="指标说明">
        <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.explain" autosize></el-input>
        </template>
      </vxe-table-column>
      <vxe-table-column field="trend" title="趋势">
        <template slot-scope="{ row }">
          <!-- <span>{{row.trend}}</span> -->
          <span v-if="row.trend=='上升'"> <i class="fa fa-long-arrow-up" style="color:rgb(0, 176, 80);font-size:40px;"></i> </span>
          <span v-else-if="row.trend=='下降'"> <i class="fa fa-long-arrow-down" style="color:rgb(255, 0, 0);font-size:40px;"></i> </span>
          <span v-else-if="row.trend=='-'"> <i class="fa fa-arrows-h" style="color:rgb(0, 176, 80);font-size:40px;"></i> </span>
          <span v-else> {{row.trend}} </span>
        </template>
      </vxe-table-column>
      <vxe-table-column
        field="grade1"
        title="红黄绿（RAG）标识"
        :edit-render="{
          name: '$select',
          options: colorArr2,
          events: { change: gradeChange },
        }"
      >
      </vxe-table-column>
      <vxe-table-column field="remark" title="备注" :edit-render="{}">
        <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.remark" autosize></el-input>
        </template>
      </vxe-table-column>
    </vxe-table>

    <!-- 四、资产净值问题 -->
    <p class="title_one">四、资产净值问题</p>
    <div>
      <div>
        列出在审查月份内发生的任何NAV问题/问题/更新的新闻以及解决方案和后续行动。
      </div>
      <div>
        <el-input
          type="textarea"
          v-loading="tableLoading"
          :autosize="{ minRows: 4 }"
          placeholder="请输入内容"
          v-model="textareaVal"
        >
        </el-input>
      </div>
    </div>

    <!-- 五、在推进中的项目/改进 -->
    <p class="title_one">五、在推进中的项目/改进</p>
    <div>
      <el-button
        @click="insertEvent('xTable8')"
        size="small"
        icon="el-icon-plus"
        style="margin-bottom: 5px"
        >新增</el-button
      >
      <el-button
          type="danger"
          plain
          @click="removeEvent('xTable8')"
          style="margin-bottom: 5px"
          size="small"
        >
          <i class="el-icon-delete"></i>移除
        </el-button>
    </div>
    <vxe-table
      border
      resizable
      v-loading="tableLoading"
      :data="tableData8"
      ref="xTable8"
      size="mini"
      class="vxeTable"
      :cell-class-name="cellClassName"
      :header-cell-class-name="headerCellClassName"
      :scroll-y="{ enabled: false }"
      :edit-rules="xTable8ValidRules"
      :edit-config="{ trigger: isSubmit!='1'?'click':'', mode: 'cell', showIcon: false }"
    > 
      <vxe-table-column type="checkbox" width="40" align="center"></vxe-table-column>
      <vxe-table-column type="seq" title="No" width="50"></vxe-table-column>
      <vxe-table-column field="project" title="项目" :edit-render="{}">
        <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.project" autosize></el-input>
        </template>
      </vxe-table-column>
      <vxe-table-column field="describe" title="描述" :edit-render="{}">
        <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.describe" autosize></el-input>
        </template>
      </vxe-table-column>
      <vxe-table-column field="status" title="状态" :edit-render="{}">
        <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.status" autosize></el-input>
        </template>
      </vxe-table-column>
      <vxe-table-column field="applicationDate" title="申请日期" :edit-render="{name: '$input', props: {type: 'date'}}">
        <!-- <template slot="edit" slot-scope="{ row }">
          <el-input
            type="textarea"
            v-model="row.applicationDate"
            autosize
          ></el-input>
        </template> -->
      </vxe-table-column>
      <vxe-table-column field="endDate" title="预估结束日期" :edit-render="{name: '$input', props: {type: 'date'}}">
        <!-- <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.endDate" autosize></el-input>
        </template> -->
      </vxe-table-column>
      <vxe-table-column field="gtjaContacts" title="国泰君安资产托管部联系人" :edit-render="{}">
        <template slot="edit" slot-scope="{ row }">
          <el-input
            type="textarea"
            v-model="row.gtjaContacts"
            autosize
          ></el-input>
        </template>
      </vxe-table-column>
      <vxe-table-column field="nbContacts" title="路博迈联系人" :edit-render="{}">
        <template slot="edit" slot-scope="{ row }">
          <el-input
            type="textarea"
            v-model="row.nbContacts"
            autosize
          ></el-input>
        </template>
      </vxe-table-column>
    </vxe-table>
    <div style="margin-top: 20px; text-align: right">
      <el-button v-if="isSubmit!='1'" @click="validAllEvent" :loading="btnLoading">提交</el-button>
      <el-button v-if="isSubmit=='1'" v-btn="'report.dailyOperations.chexiao'" @click="cancel" :loading="btnLoading">撤销提交</el-button>
      <el-button @click="send" v-if="isSubmit=='1'" :loading="btnLoading">邮件发送</el-button>
      <el-button @click="downloadFile" v-if="isSubmit=='1'" :loading="btnLoading">下载</el-button>
      <!-- <el-button @click="validAllEvent">保存</el-button> -->
    </div>
  </div>
</template>

<script>
import commonFun from '@/filters/new_common'
import homePageApi from "@/api/home/calendarList";
import pageApi from "@/api/reportCenter/kpiReport";
import { before } from 'xe-utils/methods';
export default {
  data() {
    return {
      isSubmit:"",
      btnLoading:false,
      deptName:"",
      historyDate:"",
      beforeDate:"",
      yyyy: "",
      mm: "",
      dd: "",
      nowDate: "",
      newDate: "",
      oldDate: "",
      tableLoading:false,
      tableData1: [],
      tableData2: [],
      tableData3: [],
      indexData:[],
      tableData4: [
        {
          explainId: "1",
          kpiName: "每日资产净值准确性估值表",
          priorGrade: "100",
          thisGrade: "100",
          explain: "绿色: 100%红色: 0%",
          trend: "",
          grade: "",
          remark:
            "通过运营管理平台风控中心校验指标：①检查数据是否有重新覆盖，如有，红色；②路博迈发现差错，标记红色，其他情况绿色。",
          isModel: "1",
        },
        {
          explainId: "2",
          kpiName: "",
          priorGrade: "",
          thisGrade: "50",
          explain: "",
          trend: "",
          grade: "",
          remark: "",
          isModel: "1",
        },
        {
          explainId: "3",
          kpiName: "每日资产净值及时性",
          priorGrade: "95",
          thisGrade: "100",
          explain: "绿色: 99%-100%黄色: 95% - 99%红色: <95%",
          trend: "",
          grade: "",
          remark: "",
          isModel: "1",
        },
      ],
      tableData5: [],
      tableData6: [],
      tableData7: [],
      tableData8: [],
      textareaVal: "",

      tableDataRAG: [
        // { services: "估值核算服务", grade: "reasonable" },
        // { services: "份额登记服务", grade: "reasonable" },
        // { services: "TA资金清算服务", grade: "reasonable" },
        // { services: "信息披露数据服务", grade: "reasonable" },
        // { services: "运营支持服务", grade: "reasonable" },
        // { services: "其他服务", grade: "reasonable" },
      ],
      colorArr: [
        { value: "reasonable", label: "合理", slots: { default: "opt1" } },
        { value: "imperfect", label: "有待改进", slots: { default: "opt2" } },
        { value: "error", label: "差错", slots: { default: "opt3" } },
      ],
      colorArr2: [
        { value: "reasonable", label: "绿" },
        { value: "imperfect", label: "黄" },
        { value: "error", label: "红" },
      ],
      xTable8ValidRules:{
        project:[{ required: true, message: '请填写项目' },]
      }
    };
  },
  mounted() {
    // 获取服务器时间
    this.getServerData();
    // this.getList();
  },
  methods: {
    cellClassName({}) {
      return "vxe-cell-class-name";
    },
    headerCellClassName({}) {
      return "vxe-header-cell-class-name";
    },
    // 获取服务器时间
    getServerData() {
      this.tableLoading = true;
      homePageApi
        .getTime({})
        .then(({ data: res }) => {
          if (res.status == 0) {
            let nowTime = res.timestamp;
            let tody = new Date(res.timestamp);
            this.yyyy = tody.getFullYear().toString();
            this.mm = (tody.getMonth() + 1).toString().padStart("2", "0");
            this.dd = tody.getDate().toString().padStart("2", "0");
            this.nowDate = `${this.yyyy}-${this.mm}-${this.dd}`;
            let yyyy_ = '',mm_ = '';
            if(this.mm=='01'){
              mm_='12';
              yyyy_ = this.yyyy - 1;
            }else{
              mm_ = (this.mm - 1).toString().padStart("2", "0");
              yyyy_ = this.yyyy;
            }
            this.beforeDate = `${yyyy_}年${mm_}月`
            this.historyDate = `${this.yyyy}-${this.mm}`
            this.getList(this.historyDate);
          }else{
            this.tableLoading = false;
          }
        })
        .catch((err) => {
          console.log('getServerData-----',err);
          this.tableLoading = false;
        });
    },
    historyDateChange(data){
      if(data){
        let arr = data.split('-');
        this.yyyy = arr[0];
        this.mm = arr[1];
        let yyyy_ = '',mm_ = '';
        if(this.mm=='01'){
          mm_='12';
          yyyy_ = this.yyyy - 1;
        }else{
          mm_ = (this.mm - 1).toString().padStart("2", "0");
          yyyy_ = this.yyyy;
        }
        this.beforeDate = `${yyyy_}年${mm_}月`
        this.getList(data)
      }
    },
    // 加载页面数据
    getList(data) {
      if(!this.historyDate){
        this.$message.closeAll();
        this.$message({
          type:"warning",
          message:"请选择日期"
        })
        return
      }
      let params = {
        historyDate:data
      }
      this.tableLoading = true;
      pageApi
        .getList(params)
        .then((res) => {
          this.tableLoading = false;
          if (res.data.status == 200) {
            let data = res.data.data;
            this.isSubmit = data.isSubmit || '';
            this.deptName = data.deptName || '';
            this.newDate = data.newDate || '';
            this.oldDate = data.oldDate || '';
            this.tableData1 = data.scale || []; //公司规模概况
            this.tableData2 = data.product || []; //产品运营概况
            this.tableData3 = data.operations || []; //产品运营操作类概况
            let indexData = data.index || [];
            this.indexData = data.index || [];
            //估值核算及信息披露
            this.tableData4 = indexData.filter(item=>{
              return item.isModel == '1'
            }); 
            // this.tableData4.forEach(item=>{
            //   item.priorGrade = 40
            // })
            //份额登记及TA资金清算
            this.tableData5 = indexData.filter(item=>{
              return item.isModel == '2'
            }); 
            //运营支持
            this.tableData6 = indexData.filter(item=>{
              return item.isModel == '3'
            }); 
            //综合保障指标
            this.tableData7 = indexData.filter(item=>{
              return item.isModel == '4'
            }); 
            
            this.tableData8 = data.progress || []; //在推进中的项目/改进
            this.tableDataRAG = data.rag || []; //RAG摘要
            this.textareaVal = data.netWorth || ""; //资产净值问题
            if(data.netWorth){
              this.textareaVal = data.netWorth.textarea || ''
            }else{
              this.textareaVal = ''
            }
          } else {
            this.tableData1 = [];
            this.tableData2 = [];
            this.tableData3 = [];
            this.tableData4 = [];
            this.tableData5 = [];
            this.tableData6 = [];
            this.tableData7 = [];
            this.tableData8 = [];
            this.tableDataRAG = [];
            this.textareaVal = '';
            this.$message({
              type:"error",
              message:res.data.message || "数据获取失败！"
            })
          }
        })
        .catch((err) => {
          this.tableLoading = false;
          console.log('getList--err',err);
        });
    },
    // 列表新增
    async insertEvent(table) {
      const $table = this.$refs[table];
      const record = {};
      const { row: newRow } = await $table.insertAt(record, -1);
      await $table.setActiveCell(newRow, "");
    },
    // 列表移除
    removeEvent(table) {
      const selectRecords = this.$refs[table].getCheckboxRecords();
      if (selectRecords.length) {
        this.$confirm("您确定要删除选中的数据吗?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
          confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
        })
          .then(() => {
            this.$refs[table].removeCheckboxRow();
          })
          .catch(() => {
            this.$message.closeAll();
            this.$message({
              type: "info",
              message: "已取消",
            });
          });
      } else {
        this.$message.closeAll();
        this.$message({ type: "error", message: "请至少选择一条数据" });
      }
    },
    xTable1CellStyle({ row, rowIndex, column }){
      if(!row.eTermScale) row.eTermScale = '0'
      if(!row.indInvestors) row.indInvestors = '0'
      if(!row.insInvestors) row.insInvestors = '0'
      if(!row.subscriptionInto) row.subscriptionInto = '0'
      if(!row.subscriptionOut) row.subscriptionOut = '0'
    },
    xTable2CellStyle({ row, rowIndex, column }){
      if(!row.eTermScale) row.eTermScale = '0'
      if(!row.indInvestors) row.indInvestors = '0'
      if(!row.insInvestors) row.insInvestors = '0'
      if(!row.subscriptionInto) row.subscriptionInto = '0'
      if(!row.subscriptionOut) row.subscriptionOut = '0'
    },
    // 列表单元格样式
    cellStyle({ row, rowIndex, column }) {
      if((row.thisGrade || row.thisGrade===0)&&(row.priorGrade || row.priorGrade===0)){
        if((row.thisGrade-0)>(row.priorGrade-0)){
          row.trend = '上升'
        }
        if((row.thisGrade-0)<(row.priorGrade-0)){
          row.trend = '下降'
        }
        if((row.thisGrade-0)==(row.priorGrade-0)){
          row.trend = '-'
        }
      }else{
        row.trend = '-'
      }
      if (column.property === "grade1") {
        if (row.explainId == "1") {
          if (row.thisGrade == 100) {
            row.grade = "reasonable";
            return {
              backgroundColor: "rgb(0, 176, 80)",
              color: "rgb(0, 176, 80)",
            };
          }
          if ((row.thisGrade-0) < 100) {
            row.grade = "error";
            return {
              backgroundColor: "rgb(255, 0, 0)",
              color: "rgb(255, 0, 0)",
            };
          }
        }
        if (row.explainId == "2") {
          if ((row.thisGrade-0) >= 99) {
            row.grade = "reasonable";
            return {
              backgroundColor: "rgb(0, 176, 80)",
              color: "rgb(0, 176, 80)",
            };
          }
          if (row.thisGrade >= 95 && row.thisGrade < 99) {
            row.grade = "imperfect";
            return {
              backgroundColor: "rgb(255, 192, 0)",
              color: "rgb(255, 192, 0)",
            };
          }
          if (row.thisGrade < 95) {
            row.grade = "error";
            return {
              backgroundColor: "rgb(255, 0, 0)",
              color: "rgb(255, 0, 0)",
            };
          }
        }
        if (row.explainId == "3") {
          if (row.thisGrade >= 99 && row.thisGrade <= 100) {
            row.grade = "reasonable";
            return {
              backgroundColor: "rgb(0, 176, 80)",
              color: "rgb(0, 176, 80)",
            };
          }
          if (row.thisGrade < 99 ) {
            row.grade = "error";
            return {
              backgroundColor: "rgb(255, 0, 0)",
              color: "rgb(255, 0, 0)",
            };
          }
        }
      }
    },
    // 颜色下拉选择触发
    gradeChange({ row }) {
      if (row.explainId == "1") {
        if (row.grade1 == "reasonable") {
          row.grade = "reasonable";
          row.thisGrade = "100";
        }
        if (row.grade1 == "error") {
          row.grade = "error";
          row.thisGrade = "0";
        }
      }
      if (row.explainId == "2") {
        if (row.grade1 == "reasonable") {
          row.grade = "reasonable";
          row.thisGrade = "100";
        }
        if (row.grade1 == "imperfect") {
          row.grade = "imperfect";
          row.thisGrade = "98";
        }
        if (row.grade1 == "error") {
          row.grade = "error";
          row.thisGrade = "0";
        }
      }
      if (row.explainId == "3") {
        if (row.grade1 == "reasonable") {
          row.grade = "reasonable";
          row.thisGrade = "100";
        }
        // if (row.grade1 == "imperfect") {
        //   row.grade = "imperfect";
        //   row.thisGrade = "99";
        // }
        if (row.grade1 == "error") {
          row.grade = "error";
          row.thisGrade = "0";
        }
      }
      this.changeColor();
      
    },
    thisGradeChange(val){
      setTimeout(() => {
        this.changeColor()
      }, 200);
    },
    changeColor(){
      let data1 = this.indexData.filter(item=>{
        return item.isType == '1'
      })
      let data2 = this.indexData.filter(item=>{
        return item.isType == '2'
      })
      let data3 = this.indexData.filter(item=>{
        return item.isType == '3'
      })
      let data4 = this.indexData.filter(item=>{
        return item.isType == '4'
      })
      let data5 = this.indexData.filter(item=>{
        return item.isType == '5'
      })
      let data6 = this.indexData.filter(item=>{
        return item.isType == '6'
      })
      let arr = [
        {label:"估值核算服务",data:data1},
        {label:"份额登记服务",data:data2},
        {label:"TA资金清算服务",data:data3},
        {label:"信息披露数据服务",data:data4},
        {label:"运营支持服务",data:data5},
        {label:"其他服务",data:data6},
      ];
      for(let i = 0;i<arr.length;i++){
        let error = false;
        let imperfect = false;
        for (let j = 0; j < arr[i].data.length; j++) {
          if(arr[i].data[j].grade == 'error'){
            error = true;
          }
          if(arr[i].data[j].grade == 'imperfect'){
            imperfect = true;
          }
        }
        if(error){
          // console.log(error,'红色');
          this.tableDataRAG.forEach(item=>{
            if(item.services == arr[i].label){
              item.grade = 'error'
            }
          })
        }
        if(!error && imperfect){
          // console.log(error,imperfect,'黄色');
          this.tableDataRAG.forEach(item=>{
            if(item.services == arr[i].label){
              item.grade = 'imperfect'
            }
          })
        }
        if(!error && !imperfect){
          // console.log(error,imperfect,'绿色');
          this.tableDataRAG.forEach(item=>{
            if(item.services == arr[i].label){
              item.grade = 'reasonable'
            }
          })
        }
      }
      
    },
    // 编辑获取焦点触发
    editActived({
      row,
      rowIndex,
      $rowIndex,
      column,
      columnIndex,
      $columnIndex,
    }) {
      if (row.explainId == "1") {
        this.colorArr2 = [
          { value: "reasonable", label: "绿" },
          // { value: "imperfect", label: "黄" },
          { value: "error", label: "红" },
        ]
        if (row.thisGrade == "100") {
          row.grade1 = "reasonable";
        }
        if (row.thisGrade < 100) {
          row.grade1 = "error";
        }
      }
      if (row.explainId == "2") {
        this.colorArr2 = [
          { value: "reasonable", label: "绿" },
          { value: "imperfect", label: "黄" },
          { value: "error", label: "红" },
        ]
        if (row.thisGrade >= 99) {
          row.grade1 = "reasonable";
          return {
            backgroundColor: "rgb(0, 176, 80)",
            color: "rgb(0, 176, 80)",
          };
        }
        if (row.thisGrade >= 95 && row.thisGrade < 99) {
          row.grade1 = "imperfect";
          return {
            backgroundColor: "rgb(255, 192, 0)",
            color: "rgb(255, 192, 0)",
          };
        }
        if (row.thisGrade < 95) {
          row.grade1 = "error";
          return {
            backgroundColor: "rgb(255, 0, 0)",
            color: "rgb(255, 0, 0)",
          };
        }
      }
      if (row.explainId == "3") {
        this.colorArr2 = [
          { value: "reasonable", label: "绿" },
          // { value: "imperfect", label: "黄" },
          { value: "error", label: "红" },
        ]
          if (row.thisGrade >= 99 && row.thisGrade <= 100) {
            row.grade1 = "reasonable";
            return {
              backgroundColor: "rgb(0, 176, 80)",
              color: "rgb(0, 176, 80)",
            };
          }
          if (row.thisGrade < 99) {
            row.grade1 = "error";
            return {
              backgroundColor: "rgb(255, 0, 0)",
              color: "rgb(255, 0, 0)",
            };
          }
        }
    },
    RAGcellStyle({ row, rowIndex, column }) {
      // console.log(row);
      if (column.property === "grade") {
        if (row.grade) {
          if (row.grade == "reasonable") {
            return {
              backgroundColor: "rgb(0, 176, 80)",
              color: "rgb(0, 176, 80)",
            };
          }
          if (row.grade == "imperfect") {
            return {
              backgroundColor: "rgb(255, 192, 0)",
              color: "rgb(255, 192, 0)",
            };
          }
          if (row.grade == "error") {
            return {
              backgroundColor: "rgb(255, 0, 0)",
              color: "rgb(255, 0, 0)",
            };
          }
        }
      }
    },
    // 保存
    save() {
      if(!this.historyDate){
        this.$message.closeAll();
        this.$message({
          type:"warning",
          message:"请选择日期"
        })
        return
      }
      let tableData1 = this.$refs["xTable1"].getTableData().tableData;
      let tableData2 = this.$refs["xTable2"].getTableData().tableData;
      let tableData3 = this.$refs["xTable3"].getTableData().tableData;
      let tableData4 = this.$refs["xTable4"].getTableData().tableData;
      let tableData5 = this.$refs["xTable5"].getTableData().tableData;
      let tableData6 = this.$refs["xTable6"].getTableData().tableData;
      let tableData7 = this.$refs["xTable7"].getTableData().tableData;
      let tableData8 = this.$refs["xTable8"].getTableData().tableData;
      let tableDataRAG = this.$refs["xTableRAG"].getTableData().tableData;
      let params = {};
      params.scale = tableData1; //公司规模概况
      params.product = tableData2; //产品运营概况
      params.operations = tableData3; //产品运营操作类概况
      params.rag = tableDataRAG; //RAG摘要
      params.disclosure = tableData4; //估值核算及信息披露
      params.settlement = tableData5; //份额登记及TA资金清算
      params.operational = tableData6; //运营支持
      params.guarantee = tableData7; //综合保障指标
      params.netWorth = this.textareaVal; //资产净值问题
      params.progress = tableData8; //在推进中的项目/改进
      params.oldDate = this.beforeDate; //
      params.historyDate = this.historyDate; //
      // console.log(params);
      this.btnLoading = true;
      pageApi.submit(params).then(res=>{
        this.btnLoading = false;
        if(res.data.status==200){
          this.$message({
            type:"success",
            message:"提交成功！"
          })
          this.getList(this.historyDate);
        }else{
          this.$message({
            type:"error",
            message: res.data.message || "提交失败！"
          })
        }
      })
    },
    async validAllEvent () {
      const $table = this.$refs.xTable8
      const errMap = await $table.validate(true).catch(errMap => errMap)
      if (errMap) {
        // this.$XModal.message({ status: 'error', content: '校验不通过！' })
      } else {
        this.save();
        // this.$XModal.message({ status: 'success', content: '校验成功！' })
      }
    },
    cancel(){
      if(this.historyDate){
        this.cancelSubmit();
      }else{
        this.$message({
          type:"warning",
          message:"请选择日期！"
        })
        return false
      }
    },
    // 撤销提交
    cancelSubmit(){
      this.$confirm("是否撤销提交？", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          this.btnLoading = true;
          let params = {historyDate:this.historyDate}
          pageApi.unSubmit(params).then(res=>{
            this.btnLoading = false;
            if(res.data.status==200){
              this.$message({
                type:"success",
                message:"撤销提交成功！"
              })
              this.getList(this.historyDate);
            }else{
              this.$message({
                type:"error",
                message:"撤销提交失败！"
              })
            }
          })
        })
        .catch(() => {
          
        });
    },
    // 邮件发送
    send(){
      if(this.historyDate){
        this.sendMail();
      }else{
        this.$message({
          type:"warning",
          message:"请选择日期！"
        })
        return false
      }
    },
    // 邮件发送
    sendMail(){
      this.btnLoading = true;
      let params = {
        hDate:this.historyDate,
        emailType:"2"
      }
      pageApi.sendMessage(params).then(res=>{
        this.btnLoading = false;
        if(res.data.status===200){
          this.$message({
            type:"success",
            message:"邮件发送成功！"
          })
        }else{
          this.$message({
            type:"error",
            message:res.data.message || "邮件发送失败！"
          })
        }
      })
    },
    // 下载
    downloadFile(){
      if(!this.historyDate){
        this.$message.closeAll();
        this.$message({
          type:"warning",
          message:"请选择日期！"
        })
        return false
      }
      let obj = {
        hDate:this.historyDate,
        emailType:"2",
        token:this.$store.getters.token
      }
      let action = this.$store.state.setting.baseApi + '/api/reportEmail/v1.0/download';
      commonFun.formDownloadFile(obj,action,'post');
    },
  },
};
</script>

<style lang="scss">
.kpi_tem {
  .kpi_top{
    position: relative;
    .search_form{
      position: absolute;
      right: 0px;
      top: 0px;
    }
  }
  .title {
    text-align: center;
    font-size: 22px;
  }
  .title_one {
    font-size: 20px;
    margin: 10px 2px;
  }
  .title_two {
    font-size: 18px;
    margin: 5px 2px;
  }
  .title_three {
    font-size: 16px;
    margin: 5px 2px;
  }

  .rag_zhaiyao {
    width: 500px;
    border-top: 1px solid #000;
    border-left: 1px solid #000;
    li {
      display: flex;
      div {
        width: 50%;
        border-bottom: 1px solid #000;
        border-right: 1px solid #000;
        height: 30px;
        line-height: 30px;
      }
    }
  }
  .zhaiyao_tuli {
    display: flex;
    margin-top: 6px;
    .zhaiyao_tuli_item {
      margin-left: 10px;
      display: flex;
      .box {
        width: 40px;
        border-radius: 4px;
        margin-left: 4px;
      }
    }
  }
  .red {
    background-color: rgb(255, 0, 0);
  }
  .yellow {
    background-color: rgb(255, 192, 0);
  }
  .green {
    background-color: rgb(0, 176, 80);
  }
  .vxeTable{
    .vxe-cell{
      .el-textarea__inner{
        padding: 5px !important;
      }
    }
  }
  // 去掉表头可编辑icon
  // .vxeTable{
  //   .vxe-cell--edit-icon {
  //     display: none;
  //   }
  // }
}
</style>

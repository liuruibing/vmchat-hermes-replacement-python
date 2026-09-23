<template>
  <div class="ddFileCollection_new ddportal-ui">
    <el-form :inline="true" class="formQuery">
      <el-row>
        <el-col :span="16">
          <!-- 查询 -->
          <div class="grid-content bg-purple">
            <el-form-item label="文件日期" prop="fileDate">
              <el-date-picker
                size="small"
                v-model="formQuery.fileDate"
                type="date"
                value-format="yyyy-MM-dd"
                placeholder="选择日期"
              >
              </el-date-picker>
            </el-form-item>

            <el-form-item label="基金服务机构" prop="agencyCode">
              <el-select
                v-model="formQuery.agencyCode"
                clearable
                size="small"
                placeholder="请选择"
              >
                <el-option
                  v-for="(group, index) in agencyCodeArr"
                  :value="group.agencyCode"
                  :key="index"
                  :label="group.agencyName"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="8">
          <el-form-item class="search_button_com">
            <el-button
              type="primary"
              class="mb5"
              size="small"
              @click="onQuery(true)"
              >查询</el-button
            >

            <el-button type="warning" class="mb5" size="small" @click="table_show=!table_show"
              >查看明细</el-button
            >
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <!-- 图表 -->
    <div id="main_demo" style="width: 900px; height: 500px"></div>
    <!-- 列表 -->
    <transition name="el-zoom-in-top">
      <!-- <el-collapse-transition> -->
    <div v-show="table_show">
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="文件" name="first"></el-tab-pane>
      <el-tab-pane label="清洗" name="second"></el-tab-pane>
    </el-tabs>

    <!-- <el-table
      v-if="activeName=='first'"
      ref="multipleTable"
      @selection-change="handleSelectionChange"
      :data="tableData1"
      border
      stripe
      @sort-change="handleSortChange1"
      v-loading="tableLoading1"
      style="width: 100%"
    >
      <el-table-column
        type="selection"
        width="35"
        align="center"
      ></el-table-column>

      <el-table-column
        prop="fId"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="序号"
        min-width="70"
        type="index"
        header-align="center"
      >
      </el-table-column>

      <el-table-column
        prop="agencyName"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="基金服务机构"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.agencyName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fileType"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="文件类型"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fileType | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fileName"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="文件名称"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fileName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fileDate"
        show-overflow-tooltip
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        label="文件日期"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fileDate | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fileStatus"
        show-overflow-tooltip
        label="文件状态"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fileStatus | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fileUpdateTime"
        show-overflow-tooltip
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        label="文件更新时间"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fileUpdateTime | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="execStatus"
        show-overflow-tooltip
        label="文件执行状态"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.execStatus == '未执行'" style="color: ">{{
            scope.row.execStatus | noDataFilter
          }}</span>
          <span
            v-if="scope.row.execStatus == '正在执行'"
            style="color: #6fc5dc"
            >{{ scope.row.execStatus | noDataFilter }}</span
          >
          <span
            v-if="scope.row.execStatus == '执行成功'"
            style="color: #7095d7"
            >{{ scope.row.execStatus | noDataFilter }}</span
          >
          <span
            v-if="scope.row.execStatus == '执行失败'"
            style="color: #e74d4d; font-weight: 700"
            >{{ scope.row.execStatus | noDataFilter }}</span
          >
        </template>
      </el-table-column>

      <el-table-column
        prop="extractTime"
        show-overflow-tooltip
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        label="执行时间"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.extractTime | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        label="操作"
        fixed="right"
        min-width="160"
        align="center"
      >
        <template slot-scope="scope">
          <el-button
            type="primary"
            size="small"
            @click="operationLogData(scope.row)"
            >操作日志</el-button
          >
          <el-button
            type="danger"
            plain
            size="small"
            @click="implementData(scope.row)"
            >执行</el-button
          >
          <el-button
            type="danger"
            plain
            size="small"
            @click="lookData(scope.row)"
            >数据查看</el-button
          >
        </template>
      </el-table-column>
    </el-table> -->

    <!-- 分页 -->
    <!-- <div style="height:60px" v-if="activeName=='first'">
      <Pagination
        :total="total"
        :limit="formQuery.pageSize"
        :page="formQuery.pageNum"
        @pagination="pagination"
      ></Pagination>
    </div> -->

    <!-- <el-table
      v-if="activeName == 'second'"
      ref="Table2"
      :data="tableData2"
      border
      stripe
      @sort-change="handleSortChange2"
      v-loading="tableLoading2"
      style="width: 100%"
    >
      <el-table-column
        type="selection"
        width="35"
        align="center"
      ></el-table-column>

      <el-table-column
        prop="fId"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="序号"
        min-width="70"
        type="index"
        header-align="center"
      >
      </el-table-column>

      <el-table-column
        prop="agencyName"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="机构名称"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.agencyName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fileType"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="清洗项"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fileType | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fileName"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="清洗类型"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fileName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fileName"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="清洗状态"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fileName | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="fileName"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="开始时间"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fileName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fileName"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="结束时间"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fileName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        label="操作"
        fixed="right"
        min-width="160"
        align="center"
      >
        <template slot-scope="scope">
          <el-button type="primary" size="small" @click="beginRun(scope.row)"
            >重新执行</el-button
          >
        </template>
      </el-table-column>
    </el-table> -->
    <!-- 分页 -->
    <!-- <div style="height:60px" v-if="activeName=='second'">
      <Pagination
        :total="total"
        :limit="formQuery.pageSize"
        :page="formQuery.pageNum"
        @pagination="pagination"
      ></Pagination>
    </div> -->


    <filesTable
      ref="filesTable"
      v-if="activeName=='first'"
      :Query="formQuery"
      @getFileTable="getFileTable">
    </filesTable>
    <dataClearTable ref="dataClearTable" v-if="activeName=='second'"></dataClearTable>
    </div>
      <!-- </el-collapse-transition> -->
    </transition>
    <!-- <div id="main_demo" style="width: 900px; height: 500px"></div> -->
  </div>
</template>

<script>
import commonApi from "@/api/fileCollection";
import filesTable from "./filesTable"
import dataClearTable from "./dataClearTable"
import Pagination from '@/components/Pagination'
import * as echarts from "echarts";
export default {
  name: "ddFileCollectionNew",
  components:{
    Pagination,filesTable,dataClearTable
  },
  data() {
    return {
      table_show:false,
      activeName: "first",
      formQuery: {
        fileDate:"",
        agencyCode:"",
        pageNum:1,
        pageSize:50,
      },
      total:0,
      agencyCodeArr: [],
      tableData1: [],
      tableData2: [],
      tableLoading1: false,
      tableLoading2: false,
      FileTable:[],
    };
  },
  mounted() {
    // 获取基金服务机构
    this.getAgencyList();
    // this.getEchartsList();
    // this.$nextTick(() => {
    //   this.getPie();
    // });
  },
  methods: {
    // 获取基金服务机构
    getAgencyList() {
      commonApi
        .getAgencyList()
        .then((res) => {
          if(res.data.status==0){
            this.agencyCodeArr = res.data.data;
            this.getEchartsList();
          }else{
            this.agencyCodeArr = [];
          }
        })
        .catch(() => {});
    },
    handleClick() {},
    onQuery() {
      if(this.activeName=="first" && this.$refs.filesTable){
        this.$nextTick(()=>{
          this.$refs.filesTable.onQuery(true)
        })
      }else if(this.activeName=="second" && this.$refs.dataClearTable){

      }
    },
    detail() {},
    handleSelectionChange(){},
    handleSortChange1() {},
    handleSortChange2() {},
    pagination(){},
    getFileTable(data){
      this.FileTable = data;
    },
    getEchartsList(){
      commonApi
        .getFileExtract({})
        .then((res) => {
          if (res.data.status === 0) {
            let EchartsList = res.data.data.list;
            let CodeArr = this.agencyCodeArr.map((item)=>{
              return item.agencyCode
            })
            let arr = []
            CodeArr.forEach(Codeitem=>{
              let list = EchartsList.filter(item=>{
                return item.agencyCode == Codeitem
              })
              let obj = {}
              obj['执行成功'] =  list.filter(item=>{
                return item.execStatusName == '执行成功'
              })
              obj['执行失败'] =  list.filter(item=>{
                return item.execStatusName == "执行失败"
              })
              obj['正在执行'] =  list.filter(item=>{
                return item.execStatusName == '正在执行'
              })
              obj['未执行'] =  list.filter(item=>{
                return item.execStatusName == '未执行'
              })
              arr.push(obj);
            })
            // console.log(arr);
            this.$nextTick(()=>{
              this.getPie(CodeArr,arr);
            })
          }else{

          }
        })
    },
    getPie(CodeArr,arr) {

      // 绘制图表
      let myChart = echarts.init(document.getElementById("main_demo"));
      // 指定图表的配置项和数据
      let option = {
        tooltip: {
          trigger: "axis",
          axisPointer: {
            // Use axis to trigger tooltip
            type: "shadow", // 'shadow' as default; can also be 'line' or 'shadow'
          },
        },
        legend: {
          data: ["成功", "失败", "正在执行", "未执行"],
        },
        color: ["#67C23A", "#F56C6C", "#409EFF", "#909399"],
        grid: {
          left: "3%",
          right: "4%",
          bottom: "3%",
          containLabel: true,
        },
        xAxis: {
          type: "category",
          data: this.agencyCodeArr.map(item=>item.agencyName),
        },
        yAxis: {
          type: "value",
        },
        series: [
          {
            name: "成功",
            type: "bar",
            stack: "total",
            label: {
              show: true,
            },
            emphasis: {
              focus: "series",
            },
            data: arr.map((item)=>item['执行成功'].length),
          },
          {
            name: "失败",
            type: "bar",
            stack: "total",
            label: {
              show: true,
            },
            emphasis: {
              focus: "series",
            },
            data: arr.map((item)=>item['执行失败'].length),
          },
          {
            name: "正在执行",
            type: "bar",
            stack: "total",
            label: {
              show: true,
            },
            emphasis: {
              focus: "series",
            },
            data: arr.map((item)=>item['正在执行'].length),
          },
          {
            name: "未执行",
            type: "bar",
            stack: "total",
            label: {
              show: true,
            },
            emphasis: {
              focus: "series",
            },
            data: arr.map((item)=>item['未执行'].length),
          },
        ],
      };
      // 使用刚指定的配置项和数据显示图表。
      myChart.setOption(option);
    },
  },
};
</script>

<style>
</style>

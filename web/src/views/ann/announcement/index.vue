<template>
  <div>
    <!-- 查询条件 -->
    <div class="toolbar">
      <el-form
        :inline="true"
        ref="formInline"
        :model="formInline"
        class="demo-form-inline form_inline_search"
      >
        <el-row>
          <el-col :span="16">
            <div class="grid-content bg-purple">
              <!-- 多选 -->
              <!-- <el-form-item label="产品" prop="fundCode">
                <multipleSelectTable
                  class="multipleSelectTable"
                  v-model="formInline.fundCode"
                  :data="fundList"
                  :Columns="Columns"
                  idField="fundCode"
                  nameField="codeName"
                  placeholder="请选择"
                ></multipleSelectTable>
              </el-form-item> -->
              <el-form-item label="产品" prop="fundCode">
                <select-table
                  v-model="formInline.fundCode"
                ></select-table>
              </el-form-item>
              <!-- <el-form-item label="产品类型" prop="fundType">
                <el-select v-model="formInline.fundType" clearable placeholder="请选择">
                  <el-option
                    v-for="item in fundTypeArr"
                    :key="item.dimCde"
                    :label="item.dimNme"
                    :value="item.dimCde">
                  </el-option>
                </el-select>
              </el-form-item> -->
              <el-form-item label="报告类型" prop="businessNames">
                <el-select v-model="formInline.businessNames" filterable clearable placeholder="请选择">
                  <el-option
                    v-for="item in reportTypeArr"
                    :key="item.dimCde"
                    :label="item.dimNme"
                    :value="item.dimCde">
                  </el-option>
                </el-select>
              </el-form-item>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="grid-content bg-purple-light">
              <el-form-item class="search_button_com">
                <el-button
                  type="primary"
                  @click="onSubmit(true)"
                  style="margin-bottom: 5px"
                  size="small"
                  ><i class="el-icon-search"></i>查询</el-button
                >
                <el-button
                  type="primary"
                  plain
                  @click="addNewList('formInline')"
                  style="margin-bottom: 5px"
                  size="small"
                  ><i class="el-icon-plus"></i>新增</el-button
                >
              </el-form-item>
            </div>
          </el-col>
        </el-row>
      </el-form>
    </div>
    <!-- 列表 -->
    <el-table
      :data="tableData"
      border
      v-loading="tableLoading"
      ref="tableData"
      id="announcementTable"
      :height="tableHeight"
      highlight-current-row
      @sort-change="sort_change"
    >
      <!-- <el-table-column
        type="index"
        width="50"
        header-align="center"
        align="center"
        label="序号"
      ></el-table-column> -->
      <el-table-column
        sortable
        header-align="center"
        align="left"
        label="产品代码"
        prop="fundCode"
        min-width="200"
        show-overflow-tooltip
      >
        <template slot-scope="scope">
          {{ scope.row.fundCode || '-' }}
        </template>
      </el-table-column>
      <el-table-column
        sortable
        header-align="center"
        align="left"
        label="产品名称"
        prop="fundName"
        min-width="200"
        show-overflow-tooltip
      >
        <template slot-scope="scope">
          {{ scope.row.fundName || '-' }}
        </template>
      </el-table-column>
      <!-- <el-table-column
        sortable
        header-align="center"
        align="left"
        label="产品类型"
        prop="cmdType"
        min-width="200"
      >
        <template slot-scope="scope">
          {{ scope.row.cmdType || '-' }}
        </template>
      </el-table-column> -->
      <el-table-column
        sortable
        header-align="center"
        align="left"
        label="报告类型"
        prop="reportType"
        min-width="200"
        show-overflow-tooltip
      >
        <template slot-scope="scope">
          {{ dataStatus(scope.row.reportType, 'reportType') || '-' }}
        </template>
      </el-table-column>
      <el-table-column
        sortable
        header-align="center"
        align="left"
        label="报告上报日期"
        prop="remark"
        min-width="200"
        show-overflow-tooltip
      >
        <template slot-scope="scope">
          {{ scope.row.remark || '-' }}
        </template>
      </el-table-column>
      <el-table-column
        sortable
        header-align="center"
        align="left"
        label="状态"
        prop="procStatus"
        min-width="200"
        show-overflow-tooltip
      >
        <template slot-scope="scope">
          {{ scope.row.procStatus || '-' }}
        </template>
      </el-table-column>
      <!-- <el-table-column
        sortable
        header-align="center"
        align="left"
        label="外包机构反馈备注"
        prop="cmdType"
        min-width="200"
      >
        <template slot-scope="scope">
          {{ scope.row.cmdType || '-' }}
        </template>
      </el-table-column> -->
      <!-- <el-table-column
        sortable
        header-align="center"
        align="left"
        label="提交原始附件"
        prop="cmdType"
        min-width="200"
      >
        <template slot-scope="scope">
          <el-link type="primary" @click="download1(scope.row)">下载</el-link>
        </template>
      </el-table-column>
      <el-table-column
        sortable
        header-align="center"
        align="left"
        label="外包机构反馈公告"
        prop="cmdType"
        min-width="200"
      >
        <template slot-scope="scope">
          <el-link type="primary" @click="download2(scope.row)">下载</el-link>
        </template>
      </el-table-column> -->
      <el-table-column
        sortable
        header-align="center"
        align="left"
        label="提交人"
        prop="creator"
        min-width="200"
        show-overflow-tooltip
      >
        <template slot-scope="scope">
          {{ scope.row.creator || '-' }}
        </template>
      </el-table-column>
      <el-table-column
        header-align="center"
        align="center"
        label="操作"
        width="300"
        fixed="right"
      >
        <template slot-scope="scope">
          <el-button
            type="primary"
            size="small"
            @click="serachDetail(scope.row, false)"
            >查看详情</el-button
          >
          <!-- v-btn="'transfer.update.info'" -->
          <el-button
            plain
            type="danger"
            size="small"
            @click="serachDetail(scope.row, true)"
            v-if="scope.row.isAttorneys=='1'"
            >处理</el-button
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

    <!-- 新增 -->
    <el-dialog
      custom-class=''
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      :close-on-click-modal='false'
      @closed="closedialog"
      center
      width="60% !important">
      <addForm 
        v-if="addForm_show"
        ref="addForm"
        @close="dialogVisible = false"
        @refresh="onSubmit(true)"
      ></addForm>
    </el-dialog>

    <!-- 详情、处理 -->
    <open-drawer
      v-if="openDrawerShow"
      ref="openDrawer"
      @refash="onSubmit()"
      :cmdStatus='cmdStatus_'
      @closeD="openDrawerShow=false"
    ></open-drawer>
  </div>
</template>

<script>
import selectTable from "@/views/commonComponents/selectTable.vue";
import multipleSelectTable from "@/views/commonComponents/multiple-select-table2";
import Pagination from "@/components/Pagination";
// import pageApi from "@/api/xbrl/announcement.js";
import pageApi from "@/api/productNew/operationsManage.js"
import bizBeginApi from '@/api/transfer/bizBegin';
import commonFun from "@/filters/new_common";
import commonApi from "@/api/common";
import addForm from "./addDialog.vue";
import openDrawer from "./drawer.vue"
import tableMethod from '@/utils/tableHeight';
export default {
  components: {
    // multipleSelectTable,
    selectTable,
    Pagination,
    addForm,
    openDrawer
  },
  data() {
    return {
      tableHeight:0,
      Columns: [
        { label: "产品", prop: "codeName" },
        { label: "托管机构", prop: "trustorName" },
        { label: "基金服务机构", prop: "operatorName" },
      ],
      fundList:[],
      fundTypeArr:[
        {dimCde:"GJ",dimNme:"公募"},
        {dimCde:"ZH",dimNme:"专户"},
      ],
      reportTypeArr:[
        // {dimCde:"FA050010",dimNme:"公募基金合同生效公告"},
        // {dimCde:"FC100050",dimNme:"公募基金经理变更公告"},
        // {dimCde:"FC130050",dimNme:"公募非货币市场基金分红公告"},
        // {dimCde:"FC190090",dimNme:"公募基金开放日常申购赎回转换定期定额投资业务公告"},
        // {dimCde:"FC190100",dimNme:"公募基金暂停申购公告"},
        // {dimCde:"FC190110",dimNme:"公募基金恢复申购公告"},
        // {dimCde:"FC070030",dimNme:"公募基金管理人法定名称住所变更公告"},
        // {dimCde:"FC100110",dimNme:"公募基金行业高级管理人员变更公告"},
        // {dimCde:"FC110010",dimNme:"公募涉及基金管理人诉讼的公告"},
        // {dimCde:"FC110040",dimNme:"公募涉及基金财产诉讼的公告"},
        // {dimCde:"FC130060",dimNme:"公募货币市场基金收益支付公告"},
        // {dimCde:"FC150010",dimNme:"公募基金份额净值计价错误公告"},
        // {dimCde:"FC150030",dimNme:"公募货币市场基金偏离度公告"},
        // {dimCde:"FC170010",dimNme:"基金改聘会计师事务所公告"},
        // {dimCde:"FA010070",dimNme:"基金产品资料概要"},
        // {dimCde:"FA010080",dimNme:"基金产品资料概要更新"},
      ],
      reportTypeObj:{},
      formInline: {
        pageNum:1,
        pageSize:50,
        orderString:"",
        fundCode:'',
        businessNames:""
      },
      tableLoading:false,
      tableData: [],
      total: 0,
      dialogTitle:"新增",
      dialogVisible:false,
      addForm_show:false,
      cmdStatus_:"",
      openDrawerShow:false,

    };
  },
  created(){
    tableMethod.fetTableHeight(this,'announcementTable');
  },
  activated(){
    let self = this;
    this.fetTableHeight();
    window.addEventListener("resize",self.fetTableHeight,false);
  },
  deactivated(){
    let self = this;
    window.removeEventListener("resize",self.fetTableHeight,false);
  },
  beforeDestroy(){
    let self = this;
    window.removeEventListener("resize",self.fetTableHeight,false);
  },
  mounted() {
    this.onSubmit(true);
    // this.getFundList();  // 产品多选数据
    this.getEdims('tempReport'); //报告类型
  },
  methods: {
    // 列表自适应高度
    fetTableHeight(){
      tableMethod.fetTableHeight(this,'announcementTable');
    },
    //数据字典转换
    dataStatus(statusCode, flag) {
      if (flag === "reportType") {
        return this.reportTypeObj[statusCode] || statusCode;
      }
    },
    // 字典值获取
    getEdims(val){
      commonApi.getEdims(val).then(res=>{
        if(res.data.status === 0 && res.data.message==="success"){
          if(val==='tempReport'){
            this.reportTypeArr = res.data.data;
            let arr = res.data.data;
            for (let i = 0; i < arr.length; i++) {
              this.reportTypeObj[arr[i].dimCde] = arr[i].dimNme;
            }
          }
        }
      })
    },
    // 产品多选数据
    getFundList(){
      bizBeginApi.getProductFund().then(({ data: res }) =>{
        if(res.status === 200){
          let temp = [...res.data]
          for (let i of temp) { i['codeName'] = i.fundCode + "_"+ i.fundName }
          this.fundList = temp
        } else this.$message.error('查询产品信息失败');
      }).catch((err) => { this.$message.error('查询产品信息失败') })
    },
    onSubmit(flag) {
      if(flag){
        this.formInline.pageNum = 1;
      }
      let params = JSON.parse(JSON.stringify(this.formInline));
      if(params.fundCode){
        let arr = params.fundCode.split('_');
        params.fundCode = arr[0];
      }
      params.cmdCode = '080111'
      params = commonFun.parameterSrcFull(params);
      this.tableLoading = true;
      pageApi.fundList(params).then(res=>{
        this.tableLoading = false;
        if(res.data.status === 0){
          this.tableData = res.data.data.list;
          this.total = res.data.data.total;
        }else{
          this.tableData = [];
          this.total = 0;
          this.$message({
            type:"error",
            message:res.data.message || '加载数据失败'
          })
        }
      }).catch((err)=>{
        this.tableLoading = false;
      })
    },
    // 排序
    sort_change(val){
      this.formInline.orderString = this.$fun.orderByString(val);
      this.onSubmit(false)
    },
    // 分页
    Pagination(val){
      this.formInline.pageNum=val.page;
      this.formInline.pageSize=val.limit;
      this.onSubmit(false)
    },
    // 新增
    addNewList(){
      this.dialogVisible = true;
      this.addForm_show = true;
    },
    // 关闭dialog
    closedialog(){
      this.addForm_show = false;
    },
    download1(row){
      let params = {};
      params.token = this.$store.getters.token;
      let action = store.state.setting.baseApi + "api/annreport/v1.0/download";
      commonFun.formDownloadFile(params, action, "POST");
    },
    download2(row){
      let params = {};
      params.token = this.$store.getters.token;
      let action = store.state.setting.baseApi + "api/annreport/v1.0/download";
      commonFun.formDownloadFile(params, action, "POST");
    },
    // 详情，处理
    serachDetail(row, flag){
      this.cmdStatus_=row.cmdStatus;
      this.openDrawer(row, flag);
    },
    openDrawer(data, flag){
      let rowInfo = { ...data, isCheck: flag };
      rowInfo['cmdType'] = 'newConduct'
      
      this.openDrawerShow = true;
      this.$nextTick(() => {
        this.$refs.openDrawer.init(rowInfo);
      });
    },
  },
};
</script>

<style>
</style>
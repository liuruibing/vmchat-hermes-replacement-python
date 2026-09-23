<template>
  <div class="allAccount">
    <el-form
      :inline="true"
      ref="formInline"
      :model="formInline"
      style="margin-bottom: 8px"
      class="demo-form-inline form_inline_search"
      @submit.native.prevent
    >
      <el-row>
        <el-col :span="16">
          <div style="width: 100%; height: 50px">
            <el-form-item label="产品" prop="productCode">
              <select-table
                v-model="formInline.productCode"
                @enter="onSubmit()"
              ></select-table>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="8">
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
              size="small"
              style="margin-bottom: 5px"
              @click="restForm('formInline')"
              ><i class="el-icon-delete"></i>重置</el-button
            >
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <div class="forms_table_title"><i class="el-icon-s-data"></i>账户列表</div>
    <el-table
      ref="multipleTable"
      :data="tableData"
      border
      stripe
      v-loading="tableLoading"
      style="width: 100%"
      @sort-change="handleSortChange"
    >
      
      <!-- <el-table-column fixed type='selection' width='35'></el-table-column> -->
      <el-table-column
        prop="productId"
        show-overflow-tooltip
        label="产品代码"
        min-width="100"
        algin="left"
        header-align="center"
        sortable="custom"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.productId=='undefined'">-</span>
          <span v-else>{{ scope.row.productId || "-" }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="productName"
        show-overflow-tooltip
        label="产品名称"
        min-width="100"
        algin="left"
        header-align="center"
        sortable="custom"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.productName=='undefined'">-</span>
          <span v-else>{{ scope.row.productName || "-" }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="accoName"
        show-overflow-tooltip
        label="账户名称"
        min-width="100"
        algin="left"
        header-align="center"
        sortable="custom"
      >
        
        <template slot-scope="scope">
          <span>{{ scope.row.accoName || "-" }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="accoNo"
        show-overflow-tooltip
        label="账户账号"
        min-width="100"
        algin="left"
        header-align="center"
        sortable="custom"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.accoName || "-" }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="accoBank"
        show-overflow-tooltip
        label="开户行"
        min-width="100"
        algin="left"
        header-align="center"
        sortable="custom"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.accoBank || "-" }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="accoType"
        show-overflow-tooltip
        label="账户类型"
        min-width="100"
        algin="left"
        header-align="center"
        sortable="custom"
      >
        <template slot-scope="{ row }">
          <span v-if="row.accoType == 'raise'">募集户</span>
          <span v-else-if="row.accoType == 'fiduciary'">托管户</span>
          <span v-else-if="row.accoType == 'other'">其他账户</span>
          <span v-else-if="row.accoType == 'getZqAccList'">证券账户</span>
          <span v-else-if="row.accoType == 'getQhAccList'">期货账户</span>
          <span v-else-if="row.accoType == 'getYhjAccListZz'"
            >银行间债券账户-中债</span
          >
          <span v-else-if="row.accoType == 'getYhjAccListSq'"
            >银行间债券账户-上清</span
          >
          <span v-else-if="row.accoType == 'zq'">证券账户</span>
          <span v-else-if="row.accoType == 'qh'">期货账户</span>
          <span v-else-if="row.accoType == 'yhjzz'">银行间债券账户-中债</span>
          <span v-else-if="row.accoType == 'yhjsq'">银行间债券账户-上清</span>
          <span v-else>{{ row.accoType || "-" }}</span>
        </template>
      </el-table-column>
    </el-table>
    <Pagination
      :total="total"
      :page="formInline.pageNum"
      :limit="formInline.pageSize"
      @pagination="Pagination"
    ></Pagination>
  </div>
</template>

<script>
import selectTable from "@/views/commonComponents/selectTable.vue";
import Pagination from "@/components/Pagination";
// import pageApi from "@/api/product/mjAccount";
import pageApi from "@/api/product/accountSearch.js";
import commonFun from "@/filters/new_common";
export default {
  components: {
    selectTable,
    Pagination,
  },
  data() {
    return {
      formInline: {
        productCode: "",
        pageNum: 1,
        pageSize: 50,
        orderString: "",
      },
      total: 0,
      tableLoading: false,
      pass_loading: false,
      tableData: [],
    };
  },
  activated(){

  },
  mounted() {
    this.onSubmit(true);
  },
  methods: {
    restForm(formName) {
      var self = this;
      self.$refs[formName].resetFields();
    },
    // 查询
    onSubmit(flag) {
      this.tableLoading = true;
      // 消除没有值的参数
      if (flag) {
        this.formInline.pageNum = 1;
      }
      let data = { ...this.formInline };
      if (data.productCode) {
        // console.log('产品代码',data.productCode);
        data["productCode"] = data.productCode.split("_")[0];
      }

      let params = commonFun.parameterSrc(data);
      pageApi
        .getAllAccListPage(params)
        .then((response) => {
          if (response.data.status === 200) {
            this.tableData = response.data.data.list;
            // 页面总条数
            this.total = response.data.data.total;
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
    //分页
    Pagination(val) {
      this.formInline.pageSize = val.limit; //页面条数
      this.formInline.pageNum = val.page; //页面
      this.onSubmit(false);
    },
    //排序
    handleSortChange(val) {
      this.formInline.orderString = commonFun.orderByString(val);
      this.onSubmit(false);
    },
  },
};
</script>

<style>
</style>
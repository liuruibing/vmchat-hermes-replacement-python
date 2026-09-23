<template>
  <div class="hot-org">
    <div class="search-form">
      <el-form :inline="true" :model="searchForm" class="demo-form-inline" >
        <el-form-item label="">
          <el-input
            v-model="searchForm.managerName"
            placeholder="请输入管理人名称"
            size="small"
            clearable
            style="width: 200px;"
          ></el-input>
        </el-form-item>
        <el-form-item label="">
          <el-select
            clearable
            v-model="searchForm.orgScale"
            placeholder="请选择机构规模"
            size="small"
            style="width: 150px;"
          >
            <el-option
              v-for="item in scaleOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="">
          <el-select
            v-model="searchForm.strategy"
            placeholder="请选择策略类型"
            size="small"
            clearable
            style="width: 150px;"
          >
            <el-option
              v-for="item in strategyType"
              :key="item.DIM_CDE"
              :label="item.DIM_NME"
              :value="item.DIM_CDE"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="small" @click="getleftCompData(true)" icon="el-icon-search">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button size="small" plain type="info" @click="handleReset" icon="el-icon-refresh-left">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
    <div id="standard-table">
      <div id="standard-table-margin">
        <vxe-table
          ref="refsTable"
          v-loading="tableLoading"
          :cell-style="{ height: '50px' }"
          :data="tableData"
          :height="tableHeight"
          auto-resize
          stripe=""
          show-overflow="tooltip"
          style="width: 100%"
          sync-resize
          resizable
        >
          <vxe-table-column type="index" width="50" header-align="cener" align="center" label="序号"></vxe-table-column>
          <vxe-table-column field="reg_code" show-overflow-tooltip label="管理人备案编码" min-width="120" align="center" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.reg_code | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="full_name_cn" show-overflow-tooltip label="管理人名称" min-width="220" align="left" header-align="center">
            <template slot-scope="scope">
              <span class="color_d07e34 fund_cell" @click="jumpToManager(scope.row)">{{ scope.row.full_name_cn | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="manage_scale" show-overflow-tooltip label="管理规模" min-width="120" align="center" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.manage_scale | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fund_count" show-overflow-tooltip label="旗下产品数量" min-width="220" align="center" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.fund_count | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="emp_number" show-overflow-tooltip label="员工人数" min-width="120" align="center" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.emp_number | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="reg_capital" show-overflow-tooltip label="注册资本" min-width="220" align="center" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.reg_capital | noDataFilter }}万</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="actual_controller" show-overflow-tooltip label="实际控制人" min-width="220" align="left" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.actual_controller | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="strategy_names" show-overflow-tooltip label="投资策略" min-width="220" align="left" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.strategy_names | noDataFilter }}</span>
            </template>
          </vxe-table-column>
        </vxe-table>
        <vxe-pager
          :current-page="pageNum"
          :page-size="pageSize"
          :total="total"
          :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
          border
          class="standard-vxe-pager"
          size="medium"
          @page-change="handlePagination"
        />
      </div>
    </div>
<!--    <el-row>
      <el-col class="left-comp">
&lt;!&ndash;        <div class="title">热点机构</div>&ndash;&gt;
        <left-component :leftCompArr="leftCompArr"></left-component>
        <div class="pagination-wrapper">
          <Pagination
            :limit="pageSize"
            :page="pageNum"
            :total="total"
            :pageSizes="[3,4, 10, 20, 50, 100]"
            @pagination="handlePagination"
          ></Pagination>
        </div>
      </el-col>
&lt;!&ndash;      <el-col class="right-comp">
        <div class="title">推荐机构</div>
        <el-carousel height="100%" style="height: 100%; width: 100%; padding: 5px" :autoplay="false" arrow="always">
          <el-carousel-item v-for="(row, index) in rightCompArr" :key="index">
            <div class="item-content" v-for="item in row" :key="item.F_ID">
              <rightComponent :fund-item="item" />
            </div>
          </el-carousel-item>
        </el-carousel>
      </el-col>&ndash;&gt;
    </el-row>-->
  </div>
</template>

<script>
import leftComponent from './components/leftComponent'
import rightComponent from './components/rightComponent'
import commonApi from '@/api/common'
import Pagination from '@/components/Pagination'
export default {
  name: 'hotOrg',
  components: {
    rightComponent,
    leftComponent,
    Pagination
  },
  data() {
    return {
      rightCompArr: [],
      leftCompArr: [],
      searchForm: {
        managerName: '',
        orgScale: '',
        strategy: '',
      },
      scaleOptions: [
        { label: '0-5亿', value: '0-5亿' },
        { label: '5-10亿', value: '5-10亿' },
        { label: '10-20亿', value: '10-20亿' },
        { label: '20-50亿', value: '20-50亿' },
        { label: '50-100亿', value: '50-100亿' },
        { label: '100亿以上', value: '100亿以上' }
      ],
      tableData: [],
      tableHeight: 0,
      pageNum: 1,
      pageSize: 20,
      total: 0,
       strategyType: [],
      tableLoading: false
    }
  },
  mounted() {
    //this.getRightCompData()
    this.getSTRATEGY()
    this.handleTableHeight()
    this.getleftCompData(true)
  },
  methods: {
    jumpToManager(row) {
      let newObj = {
        reg_code: row.reg_code,
        org_code: row.org_code,
        credit_code:row.credit_code
      }
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/hydt/glrcx/glrxq',
        query: { managerList: newObj }
      })
    },
    handleTableHeight() {
      this.$nextTick(() => {
        // 根据浏览器高度设置初始高度
        this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 175
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 175
        }
      })
    },
    getSTRATEGY() {
      commonApi
        .getDataBysqlCode({
          indexCode: 'c4e242a5-c11c-482a-a86a-ac3644b741ea'
        })
        .then(res => {
          const { status, data } = res.data
          if (status === 0) {
            this.strategyType = data
          }
        })
        .catch(() => {})
    },
    getleftCompData(flag) {
      if (flag) {
        this.pageNum = 1
      }
      this.tableLoading = true
      const requestParams = {
        indexCode: '6d9900d5-a2af-4c88-a592-e9465043bb85',
        managerName: this.searchForm.managerName,
        orgScale: this.searchForm.orgScale,
        strategy: this.searchForm.strategy,
        _pageNum: this.pageNum,
        _pageSize: this.pageSize,
        _pageFlag: true
      }

      commonApi
        .getDataBysqlCode(requestParams)
        .then((res) => {
          const { status } = res.data
          if (status === 0) {
            this.tableData = res.data.data.rows
            this.total = res.data.data.total
            this.tableLoading = false
          }else {
            this.tableData = []
            this.total = 0
            this.tableLoading = false
          }
        })
        .catch(() => {
          this.tableData = []
          this.total = 0
          this.tableLoading = false
        })
    },
    handleReset() {
      // 清空查询表单所有值
      this.searchForm = {
        managerName: '',
        orgScale: '',
        strategy: ''
      },
        this.pageNum = 1
      this.getleftCompData(true)
    },
    handlePagination(val) {
      const { currentPage, pageSize } = val;
      // 起始页
      this.pageNum = currentPage;
      // 每页数量
      this.pageSize = pageSize;
      // 重新查询当前页数据
      this.getleftCompData(false)
    }
  }
}
</script>

<style lang="scss" scoped>
.color_d07e34 {
  color: #d07e34;
  cursor: pointer;
}
.hot-org {
  margin: 20px 0;
  padding: 0 20px;

  .left-comp {
    //height: 920px;
   width: calc(100% - 420px);
    width: 100%;
    /*border-top: 1px solid #000;*/
    margin-right: 20px;
  }
  .pagination-wrapper {
    margin-top: 0px;
    text-align: right;
    padding-right: 10px;
    padding-bottom: 50px;
  }
  .right-comp {
    height: 920px;
    width: 400px;
    /*border-top: 1px solid #000;*/
    padding: 0 20px 20px 20px;
    background-color: #fafafa;
  }

  .title {
    padding: 20px 0;
    font-size: 16px;
    font-weight: bold;
    color: #5f6978;
  }
}
</style>

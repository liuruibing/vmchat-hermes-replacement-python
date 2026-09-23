<template>
  <div class="investRecord analyse-page" v-auto-enter>
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formQuery" :inline="true" :model="formQuery" class="standard-form" label-width="auto">
          <el-form-item label="">
            <el-input v-model="formQuery.mgrName" clearable placeholder="请输入管理人名称" size="small" />
          </el-form-item>
          <el-form-item label="">
            <el-input v-model="formQuery.orgName" clearable placeholder="请输入资方名称" size="small" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="small" icon="el-icon-search" @click="queryExamineList">查询</el-button>
          </el-form-item>
        </el-form>
      </div>
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
          <vxe-table-column type="index" width="50" header-align="center" align="center" label="序号"></vxe-table-column>
          <vxe-table-column field="ORGNAME" show-overflow-tooltip label="资方公司名称" min-width="120" algin="left" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.ORGNAME | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="MGRNAME" show-overflow-tooltip label="管理人公司名称" min-width="120" algin="left" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.MGRNAME | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="VC_PROMISEHR" show-overflow-tooltip label="是否合投互认" min-width="120" algin="center" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.VC_PROMISEHR | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="D_UPDATETIME" show-overflow-tooltip label="数据更新时间" min-width="120" algin="center" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.D_UPDATETIME | noDataFilter }}</span>
            </template>
          </vxe-table-column>

        </vxe-table>
        <vxe-pager
          :current-page="formQuery._pageNum"
          :page-size="formQuery._pageSize"
          :total="total"
          :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
          border
          size="medium"
          class="standard-vxe-pager"
          @page-change="pagination"
        />
<!--        <Pagination :total="total" :limit="formQuery._pageSize" :page="formQuery._pageNum" @pagination="pagination" />-->
      </div>
    </div>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import commonAPI from '@/api/common.js'
export default {
  name: 'investRecord',
  components: {
    Pagination
  },
  data() {
    return {
      formQuery: {
        mgrName:'',
        orgName:'',
        _pageSize: 20,
        _pageNum: 1
      },
// 表格高度
      tableHeight: 0,
      total: 0,
      tableData: [],
      tableLoading: false
    }
  },
  mounted() {
    this.initData()

  },
  methods: {
    /**
     * @description 动态设置表格高度
     */
    handleTableHeight() {
      this.$nextTick(() => {
        // 根据浏览器高度设置初始高度
        this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 165
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 165
        }
      })
    },

    async initData() {
      // 动态设置表格高度
      this.handleTableHeight()
      await this.queryExamineList()
    },

    async queryExamineList() {
      this.tableLoading = true
      try {
        const data = {
          indexCode: '6684035f-1d3e-420a-b7e3-29baedeaf606',
          mgrName: this.formQuery.mgrName,
          orgName: this.formQuery.orgName,
          _pageNum: this.formQuery._pageNum,
          _pageSize: this.formQuery._pageSize,
          _pageFlag: true
        }
        const res = await commonAPI.getDataBysqlCode(data)
        let { status } = res.data
        if (status == 0) {
          this.tableData = res.data.data.rows
          this.total = res.data.data.total
          this.tableLoading = false
        } else {
          this.tableData = []
          this.total = 0
          this.tableLoading = false
        }
      } catch (e) {
        this.tableData = []
        this.total = 0
        this.tableLoading = false
      }
    },


    pagination(val) {
      const { currentPage, pageSize } = val;
      // 起始页
      this.formQuery._pageNum  = currentPage;
      // 每页数量
      this.formQuery._pageSize = pageSize;
     /*  const { page, limit } = val
      this.formQuery._pageNum = page
      this.formQuery._pageSize = limit */
      this.queryExamineList()
    }
  }
}
</script>

<style lang="scss" scoped>
.investRecord {
  .funds-filter {
    width: 100%;
    // border-bottom: 1px solid #e1e0e0;
  }
}
.color-box {
  display: inline-block;
  height: 30px;
  width: 2px;
  background-color: #0f65dd;
}
.title-style {
  color: #0f65dd;
  vertical-align: middle;
  height: 35px;
  line-height: 35px;
  font-size: 16px;
  margin-left: 5px;
}

.search_button_com::after {
  content: '';
  clear: both;
}
::v-deep .vxe-table .vxe-body--row.row--stripe {
  background-color: #f9fafe !important;
}
</style>

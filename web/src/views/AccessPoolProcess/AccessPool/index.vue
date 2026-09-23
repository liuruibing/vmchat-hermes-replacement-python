<template>
  <div class="access-pool" v-auto-enter>
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form :inline="true" :model="formQuery" ref="formQuery" label-width="120px;" class="standard-form" :rules="rules">
          <el-form-item label="" prop="fundCode">
            <el-input v-model="formQuery.fundCode" placeholder="产品代码/拼音首字母" size="small"></el-input>
          </el-form-item>
          <el-form-item label="" prop="fundName">
            <el-input v-model="formQuery.fundName" placeholder="产品名称/拼音首字母" size="small"></el-input>
          </el-form-item>
          <el-form-item label="" prop="managerName">
            <el-input v-model="formQuery.managerName" placeholder="管理人名称/拼音首字母" size="small"></el-input>
          </el-form-item>
          <el-form-item label="" prop="status">
            <el-select v-model="formQuery.status" placeholder="请选择" size="small" disabled clearable>
              <el-option v-for="item in statusOptions" :key="item.DIM_CDE" :label="item.DIM_NME" :value="item.DIM_CDE"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="small" @click="onQuery()" icon="el-icon-search">查询</el-button>
            <el-button type="info" plain size="small" @click="resetForm()" icon="el-icon-refresh-left">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <div id="standard-table" class="table-content">
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
          @sort-change="handleSortChange"
        >
          <vxe-table-column label="序号" type="index" align="center" width="50"></vxe-table-column>
          <vxe-table-column
            v-for="item in Columns"
            :key="item.prop"
            :field="item.prop"
            :label="item.label"
            :min-width="item.minWidth || '100'"
            :width="item.width"
            header-align="center"
            :align="item.align"
            :sortable="item.sortable"
            show-overflow-tooltip
          >
            <template slot-scope="scope">
              <span>{{ scope.row[item.prop] | noDataFilter }}</span>
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
      </div>
    </div>
<!--    <div style="height: 50px">
      <Pagination :total="total" :limit="formQuery._pageSize" :page="formQuery._pageNum" @pagination="pagination" />
    </div>-->
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import accessPoolApi from '@/api/AccessPoolProcess/accessPool'
import commonApi from '@/api/common'
import commonFun from '@/filters/common'
export default {
  components: {
    Pagination
  },
  data() {
    return {
      formQuery: {
        fundCode: '',
        fundName: '',
        managerName: '',
        status: '',
        _pageSize: 20,
        _pageNum: 1,
        _pageFlag: true
      },
      rules: {
        // 日期
        // dDate: [{type: "string",required: true,message: "请选择日期",trigger: "change"}],
      },
      tableHeight: 0,
      statusOptions: [],
      strategyTypeArr: [],
      tableData: [],
      Columns: [
        { prop: 'fundCode', label: '产品代码', minWidth: '100', align: 'center', sortable: true },
        { prop: 'fundName', label: '产品名称', minWidth: '180', align: 'center', sortable: true },
        { prop: 'managerName', label: '管理人名称', minWidth: '180', align: 'center', sortable: true },
        { prop: 'amount', label: '规模（万元）', minWidth: '100', align: 'right', sortable: true },
        { prop: 'createDate', label: '成立日期', minWidth: '100', align: 'center', sortable: true },
        { prop: 'strategyName', label: '策略类型', minWidth: '100', align: 'center', sortable: true },
        { prop: 'statusName', label: '审批状态', minWidth: '100', align: 'center', sortable: true },
        { prop: 'remark', label: '备注', minWidth: '100', align: 'center', sortable: true }
      ],
      total: 0,
      tableLoading: false,
      statusName: ''
    }
  },
  activated() {},
  mounted() {
    this.getDataBysqlCodeUrl_statusOptions()
    this.getDataBysqlCodeUrl_strategyType()
    this.handleTableHeight()
  },
  methods: {
    handleSortChange(val) {
      if(val.property == 'strategyName'){
        val.property = 'strategy'
      }else if(val.property == 'statusName'){
        val.property = 'status'
      }
      this.formQuery.orderString = commonFun.queryOrderBy_vxe_template(val)
      // 查询
      this.onQuery()
    },
    // 重置
    resetForm() {
      this.$refs['formQuery'].resetFields()
    },
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
    // 分页
    pagination(val) {
    /*   let { page, limit } = val
      // 起始页
      this.formQuery._pageNum = page
      // 每页数量
      this.formQuery._pageSize = limit */
      const { currentPage, pageSize } = val;
      // 起始页
      this.formQuery._pageNum  = currentPage;
      // 每页数量
      this.formQuery._pageSize = pageSize;
      // 查询
      this.$refs['formQuery'].validate((valid) => {
        if (valid) {
          // 证券分析-存款分析
          this.selectFundUrl()
        }
      })
    },
    //获取准入状态下拉数据
    getDataBysqlCodeUrl_statusOptions() {
      commonApi
        .getDataBysqlCode({
          indexCode: '86606acb-4ec7-4c39-97ef-e15453860bb4'
        })
        .then((res) => {
          // this.getDataBysqlCodeUrl_strategyType();
          let { status, data, message } = res.data
          if (status === 0) {
            this.statusOptions = data
            this.formQuery.status = '4'
            this.statusOptions.forEach((element) => {
              if (element.DIM_CDE == this.formQuery.status) {
                this.statusName = element.DIM_NME
              }
            })
          } else {
            // this.$message.closeAll();
            // this.$message({
            //   type: 'warning',
            //   message: message ||'查询失败'
            // });
          }
        })
        .catch(() => {
          // this.getDataBysqlCodeUrl_strategyType();
        })
    },
    //获取策略类型下拉数据
    getDataBysqlCodeUrl_strategyType() {
      commonApi
        .getDataBysqlCode({
          indexCode: '6c7d78c7-aced-487b-8310-a9ad7e09c3f8'
        })
        .then((res) => {
          this.onQuery()
          let { status, data, message } = res.data
          if (status === 0) {
            this.strategyTypeArr = data
          } else {
            // this.$message.closeAll();
            // this.$message({
            //   type: 'warning',
            //   message: message ||'查询失败'
            // });
          }
        })
        .catch(() => {
          this.onQuery()
        })
    },
    //查询按钮
    onQuery(page) {
      this.$refs['formQuery'].validate((valid) => {
        if (valid) {
          // 重置起始页
          if (page) this.formQuery._pageNum = 1
          // 证券分析-存款分析
          this.selectFundUrl()
        }
      })
    },
    // 查询列表数据
    selectFundUrl() {
      this.tableData = []
      this.total = 0
      this.tableLoading = true
      let params = Object.assign({}, this.formQuery, {})
      // console.log(params)
      accessPoolApi
        .selectFund(params)
        .then((res) => {
          this.tableLoading = false
          let { status, data, statusText } = res
          if (status === 200) {
            this.total = data.total
            this.tableData = data.rows
            this.tableData.forEach((element) => {
              // element.statusName = this.statusName;
              element.statusName = '已准入'
              this.strategyTypeArr.forEach((strategyItem) => {
                // console.log(strategyItem)
                if (element.strategy == strategyItem.DIM_CDE) {
                  element.strategyName = strategyItem.DIM_NME
                }
              })
            })
          } else {
            this.$message.closeAll()
            this.$message({
              type: 'error',
              message: statusText || '查询失败',
              customClass: 'message-error'
            })
          }
        })
        .catch(() => {
          this.tableLoading = false
          this.$message.closeAll()
          this.$message({
            type: 'error',
            customClass: 'message-error',
            message: '查询失败'
          })
        })
    }
  }
}
</script>

<style lang="scss" scoped>
::v-deep .vxe-table .vxe-body--row.row--stripe {
  background-color: #f9fafe !important;
}
</style>

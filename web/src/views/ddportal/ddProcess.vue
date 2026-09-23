<template>
  <div class="DdPosition ddportal-ui">
    <el-form :inline="true" ref="formInline" :model="formInline" style="margin-bottom: 8px;" class="demo-form-inline form_inline_search">
      <el-row>
        <el-col :span="21">
          <div style="width:100%;">
            <el-form-item label="用户" prop="userName">
              <el-input v-model="formInline.userName" clearable size="small" placeholder="请输入内容"></el-input>
            </el-form-item>

            <el-form-item label="所属机构" prop="companyId">
              <el-select v-model="formInline.companyId" size="small" placeholder="请选择" clearable>
                <el-option v-for="(group, index) in companyIdArr" :value="group.companyId" :key="index" :label="group.deptName"></el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="开始日期" prop="date">
              <el-date-picker
                v-model="formInline.date"
                size="small"
                value-format="yyyy-MM-dd"
                type="daterange"
                :picker-options="dateShortcut()"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
              ></el-date-picker>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="3">
          <el-form-item class="search_button_com">
            <el-button type="primary" @click="onSubmit('formInline', true)" style="margin-bottom: 5px; " size="small">
              <i class="el-icon-search"></i>
              查询
            </el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <div style="vertical-align: middle;display: inline-block;">
      <div class="color-box"></div>
    </div>
    <span class="title-style">操作信息</span>
    <el-table
      ref="multipleTable"
      @selection-change="handleSelectionChange"
      :data="tableData"
      :default-sort="{ prop: 'opeaDate', order: 'descending' }"
      stripe
      @sort-change="handleSortChange"
      v-loading="tableLoading"
      :cell-style="{ height: '40px', fontSize: '14px' }"
      :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
      style="width: 100%"
    >
      <el-table-column
        prop="userName"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="用户名"
        min-width="80"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.userName | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="companyName" show-overflow-tooltip label="机构名称" min-width="80" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.companyName | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="name" show-overflow-tooltip label="操作功能" min-width="120" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.name | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="ip" show-overflow-tooltip label="IP地址" min-width="80" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.ip | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column prop="opeaDate" show-overflow-tooltip label="操作时间" min-width="80" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.opeaDate | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column prop="logDesc" show-overflow-tooltip label="操作描述" min-width="120" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.logDesc | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column prop="param" show-overflow-tooltip label="详细参数" min-width="150" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.param | noDataFilter }}</span>
        </template>
      </el-table-column>
    </el-table>

    <Pagination :total="total" :page="formInline.pageNum" :limit="formInline.pageSize" @pagination="Pagination"></Pagination>
  </div>
</template>

<script>
import commonFun from '@/filters/common.js'
import Pagination from '@/components/Pagination'
import pageApi from '@/api/ddportal/process.js'

export default {
  name: 'DdProcess',
  components: {
    Pagination
  },
  data() {
    return {
      //查询表单
      formInline: {
        date: '', //登录日期
        userName: '', //用户
        companyId: '', //所属机构
        orderString: 'opeaDate desc nulls last', //列表排序
        pageSize: 10, //条数
        pageNum: 1 //页码
      },
      total: 0, //列表条数
      tableMultipleSelection: [], //列表选中数据
      tableData: [], //列表数据
      tableLoading: false, //列表加载
      companyIdArr: [] //所属机构数组
    }
  },

  mounted() {
    //获取机构
    this.getCompanyIdList()
    //获取完token之后再请求列表信息
    this.onSubmit('formInline', true)
  },
  methods: {
    // 日期快捷选项
    dateShortcut() {
      return commonFun.dateShortcut()
    },
    //列表选择
    handleSelectionChange(val) {
      this.tableMultipleSelection = val
    },
    //排序
    handleSortChange(val) {
      this.formInline.orderString = commonFun.queryOrderBy(val)
      this.onSubmit('formInline', false)
    },
    //分页
    Pagination(val) {
      let { page, limit } = val
      // 起始页
      this.formInline.pageNum = page
      // 每页数量
      this.formInline.pageSize = limit
      // 查询
      this.onSubmit('formInline')
    },
    // 查询
    onSubmit(formName, flag) {
      this.tableLoading = true

      this.$refs[formName].validate(valid => {
        if (valid) {
          let params = commonFun.parameterSrc(this.formInline)
          if (params.date) {
            params.beginDate = params.date[0]
            params.endDate = params.date[1]
            params.date = ''
          }
          //清楚空字段
          for (let k in params) {
            if (!params[k] && String(params[k]) !== '0') {
              delete params[k]
            }
          }

          pageApi
            .getDataSourceList(params)
            .then(response => {
              if (!response.data.error) {
                this.tableData = response.data.data.list
                // 页面总条数
                this.total = response.data.data.total
              } else {
                this.tableData = []
                this.total = 0
                this.formInline.pageSize = 10
                this.formInline.pageNum = 1
              }
              this.tableLoading = false
            })
            .catch(() => {
              this.tableData = []
              this.total = 0
              this.formInline.pageSize = 10
              this.formInline.pageNum = 1
              this.tableLoading = false
            })
        } else {
          return false
        }
      })
    },
    //获取所属机构
    getCompanyIdList() {
      pageApi
        .getCompanyIdList()
        .then(response => {
          if (!response.data.error) {
            let data = response.data.data
            this.companyIdArr = data
          } else {
            this.companyIdArr = []
          }
        })
        .catch(() => {
          this.companyIdArr = []
        })
    }
  }
}
</script>

<style lang="scss" scoped>
.DdPosition {
  padding-left: 8px;
  .title-style {
    color: #0F65DD;
    vertical-align: middle;
    height: 35px;
    line-height: 35px;
    font-size: 16px;
    margin-left: 5px;
  }
  .color-box {
    display: inline-block;
    height: 30px;
    width: 2px;
    background-color: #0F65DD;
  }
}
::v-deep .el-table tbody tr:hover > td {
  background-color: transparent !important; //修改成自己想要的颜色即可
}

::v-deep .el-table--striped .el-table__body tr.el-table__row--striped td {
  background: #f7f7f7 !important;
}
</style>

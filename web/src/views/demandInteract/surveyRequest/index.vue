<!-- 尽调申请-->
<template>
  <div class="surveyRequest">
    <!-- el-form -->
    <div class="toolbar">
      <el-form :inline="true" ref="formInline" :model="formInline" @submit.native.prevent>
        <el-row>
          <el-col :span="20">
            <div class="grid-content bg-purple">
              <el-form-item label="机构名称">
                <el-input v-model.trim="formInline.orgName" maxlength="30" clearable size="small"></el-input>
              </el-form-item>
              <el-form-item label="处理状态">
                <el-select v-model="formInline.status" class="header-search-select" size="small">
                  <el-option v-for="item in statusOptions" :key="item.value" :value="item.value" :label="item.label" />
                </el-select>
              </el-form-item>
              <el-form-item label="申请日期">
                <el-date-picker
                  v-model="formInline.applyDate"
                  end-placeholder="结束日期"
                  range-separator="至"
                  start-placeholder="开始日期"
                  type="daterange"
                  value-format="yyyy-MM-dd"
                  size="small"
                ></el-date-picker>
              </el-form-item>
            </div>
          </el-col>
          <el-col :span="4">
            <div class="grid-content bg-purple-light">
              <el-form-item class="search_button_com">
                <el-button type="primary" icon="el-icon-search" style="margin-bottom: 5px" size="small">查询</el-button>
                <el-button type="primary" icon="el-icon-refresh" style="margin-bottom: 5px" size="small">重置</el-button>
                <el-button type="primary" style="margin-bottom: 5px" size="small" icon="el-icon-plus" @click="handleApplySurvey">新申请</el-button>
              </el-form-item>
            </div>
          </el-col>
        </el-row>
      </el-form>
    </div>

    <div class="title-style">尽调申请列表</div>
    <!-- el-table -->
    <el-table :data="tableData" stripe ref="table" border style="width: 100%">
      <el-table-column v-for="(col, i) in columns" :key="i" :prop="col.prop" :label="col.label" :width="col.width" header-align="center" :align="col.align" stripe>
        <template slot-scope="scope">
          <span
            v-if="col.prop == 'c7'"
            :style="{
              color: scope.row[col.prop] === '2' ? '#70ad47' : '#ffc000'
            }"
          >
            {{ scope.row[col.prop] | statusFilter(that) }}
          </span>
          <span v-else>{{ scope.row[col.prop] | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" prop="c8" align="left" header-align="center">
        <template slot-scope="scope">
          <el-button type="primary" size="small" :underline="false" @click="handleEdit(scope.row)">编辑</el-button>
          <el-button type="primary" size="small" plain :underline="false" @click="handleShowDetail(scope.row)">详情</el-button>
          <el-button type="danger" size="small" :underline="false" plain>删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- pagination -->
    <div style="width: 100%; height: 20px">
      <Pagination :total="total" :page="pageNumber" :limit="pageSize" @pagination="Pagination"></Pagination>
    </div>

    <!-- add / edit dialog -->
    <el-dialog :title="dialogTitle" center :visible.sync="isShowAddDialog" :close-on-click-modal="false" @close="handleClose">
      <survey-edit :edit-obj="editObj" @close="handleClose" :is-edit-reset="isEditReset"></survey-edit>
    </el-dialog>

    <!-- detail dialog -->
    <el-dialog title="详情" center :visible.sync="isShowDetailDialog" :close-on-click-modal="false">
      <survey-detail :detail-obj="detailObj" @close="handleClose" :is-detail-reset="isDetailReset"></survey-detail>
    </el-dialog>
  </div>
</template>

<script>
import constant from './scripts/constant.js'
import Pagination from '@/components/Pagination'
import surveyEdit from './components/survey-edit.vue'
import surveyDetail from './components/survey-detail.vue'
export default {
  name: 'SurveyRequest',
  components: {
    Pagination,
    surveyEdit,
    surveyDetail
  },
  data() {
    return {
      that: this,
      formInline: {
        orgName: '',
        status: '',
        applyDate: []
      },
      statusOptions: constant.statusOptions,
      tableData: constant.tableData,
      columns: constant.columns,
      total: constant.tableData.length, //总条数
      pageSize: 20, //条数
      pageNumber: 1, //页码
      dialogTitle: '',
      isShowAddDialog: false,
      editObj: {},
      isEditReset: false,
      detailObj: {},
      isShowDetailDialog: false,
      isDetailReset: false
    }
  },
  methods: {
    handleApplySurvey() {
      this.dialogTitle = '新增'
      this.isShowAddDialog = true
    },
    handleClose() {
      this.isShowAddDialog = false
      this.isEditReset = true
      this.isShowDetailDialog = false
      this.isDetailReset = true
    },
    handleEdit(row) {
      this.dialogTitle = '编辑'
      this.isShowAddDialog = true
      this.editObj = JSON.parse(JSON.stringify(row))
    },
    handleShowDetail(row) {
      this.isShowDetailDialog = true
      this.detailObj = JSON.parse(JSON.stringify(row))
    },
    //分页
    Pagination(val) {}
  },
  filters: {
    statusFilter(value, that) {
      const obj = that.statusOptions.find(item => item.value === value)
      return obj && obj.label
    }
  }
}
</script>

<style lang="scss" scoped>
.title-style {
  color: #c39330;
  height: 35px;
  line-height: 35px;
  padding-left: 4px;
  font-size: 16px;
  border-left: 4px solid #c39330;
}
.color_4f95dd {
  color: #4f95dd;
  cursor: pointer;
}
.tabletable_top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  .tableTitle {
    border-left: 3px solid #4f95dd;
    padding-left: 10px;
    color: #4f95dd;
    font-weight: bold;
  }
}
::v-deep .el-link--inner {
  margin-right: 3px;
  color: #4f95dd;
  font-size: 14px;
}
::v-deep .el-table__row .is-left .cell {
  padding-left: 15px !important;
}
</style>

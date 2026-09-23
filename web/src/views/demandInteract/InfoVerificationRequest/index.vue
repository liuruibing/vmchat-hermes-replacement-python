<!--
 * @Description:
 * @Author:
 * @Date: 2023-02-06 09:43:19
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2023-02-06 18:06:46
-->
<template>
  <div class="">
    <!-- 查询表单 -->
    <el-row>
      <el-col :span="20">
        <el-form :inline="true" :model="formQuery" label-width="120px;">
          <el-form-item label="产品/机构名称" prop="fundName">
            <el-input v-model="formQuery.fundName" placeholder="请输入" size="small"></el-input>
          </el-form-item>
          <el-form-item label="信息验证类型" prop="dataType">
            <el-select v-model="formQuery.dataType" placeholder="请选择" size="small" clearable>
              <el-option
                v-for="item in dataTypeOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              >
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="处理状态" prop="status">
            <el-select v-model="formQuery.status" placeholder="请选择" size="small" clearable>
              <el-option
                v-for="item in statusOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              >
              </el-option>
            </el-select>
          </el-form-item>
          <div style="display: inline-block">
            <el-form-item label="申请日期" prop="beginDate">
              <el-date-picker
                v-model="formQuery.beginDate"
                type="date"
                size="small"
                value-format="yyyy-MM-dd"
                placeholder="开始"
              >
              </el-date-picker>
            </el-form-item><span style="line-height: 32px;">- </span>
            <el-form-item label="" prop="endDate">
              <el-date-picker
                v-model="formQuery.endDate"
                type="date"
                size="small"
                value-format="yyyy-MM-dd"
                placeholder="结束"
              >
              </el-date-picker>
            </el-form-item>
          </div>

        </el-form>
      </el-col>
      <el-col :span="4">
        <div style="text-align: right">
          <el-button type="primary" size="small" icon="el-icon-search" @click="onQuery">查询</el-button>
          <el-button type="primary" size="small" icon="el-icon-refresh" @click="resetForm">重置</el-button>
          <el-button type="primary" size="small" icon="el-icon-plus" @click="openAdd"
            >新申请</el-button
          >
        </div>
      </el-col>
    </el-row>

    <!-- 表格 -->
    <div class="title-style">信息验证申请</div>
    <el-table :data="tableData"  border style="width: 100%" v-loading="tableLoading" id="">
      <el-table-column label="序号" type="index" align="center" width="50"> </el-table-column>
      <el-table-column
        v-for="item in Columns"
        :key="item.prop"
        :prop="item.prop"
        :label="item.label"
        :min-width="item.minWidth || '100'"
        :width="item.width"
        header-align="center"
        :align="item.align"
        :sortable="item.sortable"
        show-overflow-tooltip
      >
        <template slot-scope="scope">
          <span
            v-if="item.prop == 'f7'"
            :style="{
              color: scope.row[item.prop] === '处理完毕' ? '#70ad47' : '#ffc000'
            }"
            >{{ scope.row[item.prop] | noDataFilter}}</span
          >
          <span v-else>{{ scope.row[item.prop] | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" width="230">
        <template slot-scope="scope">
          <el-button size="small" type="primary" @click="openEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="primary" plain @click="openDetail(scope.row)">详情</el-button>
          <el-button size="small" type="danger" plain>删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div style="height: 50px">
      <Pagination
        :total="total"
        :limit="formQuery._pageSize"
        :page="formQuery._pageNum"
        @pagination="pagination"
      />
    </div>

    <!-- 新申请/编辑/详情 -->
    <el-dialog
      :title="dialogTitle"
      width="50%"
      custom-class=""
      :visible.sync="dialogVisible"
      :close-on-click-modal="false"
      :append-to-body="true"
      @closed="dialogClosed"
      center
    >
      <addForm ref="addForm" v-if="addFormShow" @close="dialogVisible = false"></addForm>
      <detailForm ref="detailForm" v-if="detailFormShow" @close="dialogVisible = false"></detailForm>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from "@/components/Pagination";
import addForm from "./components/addForm.vue";
import detailForm from "./components/detailForm.vue";
export default {
  components: {
    Pagination,
    addForm,
    detailForm
},
  data() {
    return {
      formQuery: {
        fundName: "",
        dataType: "",
        status: "",
        beginDate: "",
        endDate: "",
        _pageSize: 20,
        _pageNum: 1,
        _pageFlag: true
      },
      dataTypeOptions: [
        { label: "机构信息", value: "1" },
        { label: "产品信息", value: "2" },
        { label: "产品数据", value: "3" },
      ],
      statusOptions: [
        { label: "已提交", value: "1" },
        { label: "处理中", value: "2" },
        { label: "处理完毕", value: "3" },
      ],
      tableData: [
        {
          f1: "测试机构",
          f2: "机构信息",
          f3: "说明。。。",
          f4: "",
          f5: "2023-01-01",
          f6: "admin",
          f7: "已提交",
          f8: "",
        },
        {
          f1: "测试产品一号",
          f2: "产品信息",
          f3: "说明。。。",
          f4: "",
          f5: "2023-01-01",
          f6: "admin",
          f7: "处理中",
          f8: "",
        },
        {
          f1: "测试产品003",
          f2: "产品数据",
          f3: "说明。。。",
          f4: "",
          f5: "2023-01-01",
          f6: "admin",
          f7: "处理中",
          f8: "",
        },
        {
          f1: "测试机构X",
          f2: "机构信息",
          f3: "说明。。。",
          f4: "",
          f5: "2023-01-01",
          f6: "admin",
          f7: "处理完毕",
          f8: "处理结果处理结果",
        },
      ],
      Columns: [
        { prop: "f1", label: "机构/产品名称", align: "" },
        { prop: "f2", label: "信息验证类型", align: "center" },
        { prop: "f3", label: "说明", align: "" },
        { prop: "f4", label: "文件附件", align: "" },
        { prop: "f5", label: "申请日期", align: "center" },
        { prop: "f6", label: "申请人", align: "center" },
        { prop: "f7", label: "处理状态", align: "center" },
        { prop: "f8", label: "处理结果", align: "" }
      ],
      total: 0,
      tableLoading: false,
      dialogTitle: "",
      dialogVisible: false,
      addFormShow: false,
      detailFormShow: false,
      homeParams: {}
    };
  },
  activated() {
    if(this.$route.query){
      let params = JSON.parse(JSON.stringify(this.$route.query));
      this.homeParams = params;
      if(params.flag){
        this.openAdd(true)
      }else{
        this.formQuery.fundName = params.fundName
      }
    }
  },
  methods: {
    // 重置
    resetForm() {
      this.$refs["formQuery"].resetFields();
    },
    // 查询
    onQuery(flag) {

    },
    // 分页
    pagination() {},
    // 新申请
    openAdd(flag) {
      this.dialogTitle = "新申请";
      this.dialogVisible = true;
      this.addFormShow = true;
      if(flag){
        this.$nextTick(() => {
          this.$refs.addForm.addInit(this.homeParams);
        })
      }
    },
    // 编辑
    openEdit() {
      this.dialogTitle = "编辑";
      this.dialogVisible = true;
      this.addFormShow = true;
      this.$nextTick(() => {
        this.$refs.addForm.editInit()
      })
    },
    // 详情
    openDetail() {
      this.dialogTitle = "详情";
      this.dialogVisible = true;
      this.detailFormShow = true;
    },
    // 关闭dialog
    dialogClosed() {
      this.addFormShow = false;
      this.detailFormShow = false;
    }
  }
};
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
</style>

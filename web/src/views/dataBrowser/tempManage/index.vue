<!--
 * @Description: 
 * @Author: 
 * @Date: 2025-11-03 13:49:01
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2025-12-31 11:29:15
-->
<template>
  <div class="dataBrowser-tempManage">
    <!-- 搜索 -->
    <el-form :inline="true" ref="formQuery" :model="formQuery" label-width="auto" class="standard-form">
      <el-row>
        <el-col :span="24">
          <el-form-item prop="vcTemplateName">
            <el-input v-model.trim="formQuery.vcTemplateName" clearable placeholder="请输入模板名称" size="small"></el-input>
          </el-form-item>
          <el-form-item prop="vcTemplateTypes">
            <el-select v-model="formQuery.vcTemplateTypes" placeholder="请选择模板类型" size="small" multiple collapse-tags clearable>
              <el-option v-for="item in templateTypeOptions" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
            </el-select>
          </el-form-item>
          <el-form-item class="">
            <el-button type="primary" size="small" :loading="tableLoading" @click="onQuery(true)" class="mb5" icon="el-icon-search">查询</el-button>
            <el-button type="info" size="small" plain icon="el-icon-refresh" @click="resetForm('formQuery')">重置</el-button>
            <el-button type="primary" size="small" icon="el-icon-plus" @click="addTemplate()">新增</el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <!-- <div class="page-model-title">
      <div class="title-icon">
        <div class="color-box"></div>
      </div>
      <span class="title-txt">模板信息</span>
    </div> -->
    <div class="dataBrowser-tempManage-table" id="standard-table">
      <vxe-table
        height="auto"
        v-loading="tableLoading"
        :data="tableData"
        stripe
        auto-resize
        sync-resize
        resizable
        show-overflow
        show-header-overflow
        highlight-hover-rows
        header-align="center"
        @sort-change="handleSortChange"
        :sort-config="{remote: true}"
      >
      <vxe-table-column type="seq" title="序号" width="60" align="center"></vxe-table-column>
      <vxe-table-column field="vcTemplateName" title="模板名称" sortable min-width="100"></vxe-table-column>
      <vxe-table-column field="vcTemplateType" title="模板类型" sortable min-width="100" align="center">
        <template slot-scope="scope">
          <span>{{ transDict(scope.row.vcTemplateType, "vcTemplateType") }}</span>
        </template>
      </vxe-table-column>
      <vxe-table-column field="vcDateType" title="日期类型" sortable min-width="100" align="center">
        <template slot-scope="scope">
          <span>{{ transDict(scope.row.vcDateType, "vcDateType") }}</span>
        </template>
      </vxe-table-column>
      <vxe-table-column field="dCreateTime" title="创建时间" sortable min-width="100" align="center"></vxe-table-column>
      <vxe-table-column field="vcRemark" title="备注" sortable min-width="100">
        <template slot-scope="scope">
          <span>{{ scope.row.vcRemark | noDataFilter }}</span>
        </template>
      </vxe-table-column>
      <vxe-table-column title="操作" width="310" align="center">
        <template slot-scope="scope">
          <span class="table-operation">
            <el-dropdown @command="(command) => handleEdit(command, scope.row)">
              <el-button type="info" plain size="small" style="margin-right: 8px">
                编辑
                <i class="el-icon-arrow-down el-icon--right"></i>
              </el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="1">编辑基础信息</el-dropdown-item>
                <el-dropdown-item command="2">编辑模板配置</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
            <el-button type="info" plain size="small" @click="deleteTemplate(scope.row)">删除</el-button>
            <el-button type="info" plain size="small" @click="viewTemplate(scope.row)">查看</el-button>
            <!-- <el-button type="primary" size="small" @click="copyTemplate(scope.row)">复制新增</el-button> -->
          </span>
        </template>
      </vxe-table-column>
      </vxe-table>
    </div>
    <Pagination :total="total" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination"></Pagination>
    <!-- 新增模板/编辑模板基础信息 -->
    <TempBaseInfo
      v-if="tempBaseInfoShow"
      :dialogType="dialogType"
      ref="tempBaseInfoRef"
      @close="tempBaseInfoShow = false"
      @addTempConfig="addTempConfig"
      @refresh="onQuery(true)"
    ></TempBaseInfo>
    <!-- 编辑模板配置 -->
    <TempConfig v-if="tempConfigShow" :dialogType="dialogType" ref="tempConfigRef" @close="tempConfigShow = false" @refresh="onQuery(true)"></TempConfig>
  </div>
</template>

<script>
import Pagination from '@/components/NewPagination'
import TempBaseInfo from './components/tempBaseInfo'
import TempConfig from './components/tempConfig'
import CONSTANTS from '../constants.js'
import pageApi from './api'
export default {
  name: 'TempManage',
  components: {
    Pagination,
    TempBaseInfo,
    TempConfig
  },
  data() {
    return {
      // 查询参数
      formQuery: {
        vcTemplateName: '',
        vcTemplateTypes: [],
        pageNum: 1,
        pageSize: 20,
        orderBy: ''
      },
      templateTypeOptions: CONSTANTS.TEMPTYPE,
      templateTypeMap: {},
      dateTypeOptions: CONSTANTS.DATETYPE,
      dateTypeMap: {},
      // 表格参数
      tableLoading: false,
      tableData: [],
      total: 0,
      tempBaseInfoShow: false,
      dialogType: 'add', // add:新增 edit:编辑
      tempConfigShow: false
    }
  },
  mounted() {
    // 初始化字典数据-用于字典中文转换
    this.initDictMap();
    // 查询
    this.onQuery(true)
  },
  methods: {
    // 查询
    onQuery(flag) {
      if (flag) {
        this.formQuery.pageNum = 1
      }
      this.tableLoading = true
      pageApi.getTempList(this.formQuery).then((res) => {
        const { status, data } = res.data
        if (status === 200) {
          this.tableData = data.list || []
          this.total = data.total || 0
        } else {
          this.tableData = []
          this.total = 0
        }
        this.tableLoading = false
      }).catch(() => {
        this.tableLoading = false
      })
    },
    // 重置
    resetForm(formName) {
      this.$refs[formName].resetFields()
      this.$nextTick(() => {
        this.onQuery(true)
      })
    },
    // 监听分页
    pagination(val) {
      let { page, limit } = val
      this.formQuery.pageNum = page
      this.formQuery.pageSize = limit
      this.onQuery(false)
    },
    // 监听排序
    handleSortChange(val) {
      this.formQuery.orderBy = this.$fun.queryOrderBy_vxe(val)
      this.onQuery(false)
    },
    // 新增模板
    addTemplate() {
      this.dialogType = 'add'
      this.tempBaseInfoShow = true
    },
    addTempConfig(data) {
      this.dialogType = 'add'
      this.tempConfigShow = true
      this.$nextTick(() => {
        this.$refs.tempConfigRef.init(data)
      })
    },
    // 编辑 command 1基础信息/2模板配置
    handleEdit(command, row) {
      if (command === '1') {
        this.editBaseInfo(row)
      } else if (command === '2') {
        this.editTemplateConfig(row)
      }
    },
    // 编辑模板基础信息
    editBaseInfo(row) {
      this.dialogType = 'edit'
      this.tempBaseInfoShow = true
      this.$nextTick(() => {
        this.$refs.tempBaseInfoRef.init(row)
      })
    },
    // 编辑模板配置
    editTemplateConfig(row) {
      this.dialogType = 'edit'
      this.tempConfigShow = true
      this.$nextTick(() => {
        this.$refs.tempConfigRef.editInit(row)
      })
    },
    // 编辑模板
    editTemplate(row) {
      this.dialogType = 'edit'
      this.tempBaseInfoShow = true
      this.$nextTick(() => {
        this.$refs.tempBaseInfoRef.init(row)
      })
    },
    // 删除模板
    deleteTemplate(row) {
      this.$confirm('确定删除该模板吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const params = {
          vcTemplateIds: [row.vcTemplateId]
        }
        pageApi.deleteTemplate(params).then((res) => {
          const { status, message } = res.data
          if (status === 200) {
            this.$message.success(message || '删除成功')
            this.onQuery(true)
          } else {
            this.$message.error(message || '删除失败')
          }
        })
      })
    },
    // 查看模板-跳转到数据浏览器
    viewTemplate(row) {
      let moreParams = {};
      if (row.vcBenchMark) {
        try {
          moreParams = JSON.parse(row.vcBenchMark)
          // 添加行业类型参数 默认申万一级行业
          if (moreParams && typeof moreParams === 'object') {
            moreParams.industryType = moreParams.industryType || 'SWSR'
            moreParams.factorType = moreParams.factorType || 'CNE5'
          }
        } catch (e) {
          console.error('解析 vcBenchMark 失败:', e)
        }
      }
      sessionStorage.setItem('dataView_jumpToTemplateInfo', JSON.stringify({
        vcTemplateId: row.vcTemplateId,
        vcTemplateType: row.vcTemplateType,
        moreParams
      }))
      this.$router.push({
        path: '/jxbg/bgzq/dataBrowserDataView'
      })
    },
    // 复制模板
    copyTemplate(row) {},
    // 初始化字典map
    initDictMap() {
      this.templateTypeMap = this.templateTypeOptions.reduce((acc, item) => {
        acc[item.dimCde] = item.dimNme
        return acc
      }, {})
      this.dateTypeMap = this.dateTypeOptions.reduce((acc, item) => {
        acc[item.dimCde] = item.dimNme
        return acc
      }, {})
    },
    // 字典转换
    transDict(value, code) {
      if (code === "vcTemplateType") {
        return this.templateTypeMap[value] || value
      } else if (code === "vcDateType") {
        return this.dateTypeMap[value] || value
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.dataBrowser-tempManage {
  height: 100%;
  padding: 12px 10px;
  .dataBrowser-tempManage-table {
    height: calc(100% - 110px);
  }
}
</style>
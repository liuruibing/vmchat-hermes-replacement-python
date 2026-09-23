<template>
  <div class="associatedSql">
    <el-dialog v-dialogDrag :title="sqlTitle" custom-class="associatedSqlWidth" center :visible.sync="sqlDialogPage" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox" style="height:300px;">
          <el-form :inline="true" ref="formInline" :model="formInline" :rules="searchRules" style="margin-bottom: 8px;" class="demo-form-inline form_inline_search">
            <el-row>
              <el-col :span="6">
                <el-form-item label="SQL名称" prop="sqlName">
                  <el-input v-model.trim="formInline.sqlName" clearable placeholder="请输入" size="small"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item label="SQL编码" prop="sqlCode">
                  <el-input v-model.trim="formInline.sqlCode" clearable placeholder="请输入" size="small"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item label="执行方式" prop="sqlOperate">
                  <el-select v-model="formInline.sqlOperate" size="small" placeholder="请选择">
                    <el-option v-for="(group, index) in sqlOperateArr" :value="group.dimCde" :key="index" :label="group.dimNme"></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item >
                  <el-button type="primary" @click="sqlQuery('formInline', true)" style="margin-bottom: 5px; " size="small">
                    <i class="el-icon-search"></i>
                    查询
                  </el-button>
                  <el-button type="primary" style="margin-bottom: 5px; " @click="add()" size="small">
                    <i class="el-icon-search"></i>
                    添加
                  </el-button>
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>

          <div style="vertical-align: middle;display: inline-block;">
            <div class="color-box"></div>
          </div>
          <span class="title-style">SQL配置列表</span>
          <el-table
            ref="multipleTable"
            @selection-change="handleSelectionChange"
            :data="tabSqlList"
            :default-sort="{ prop: 'vcTemplatEname', order: 'descending' }"
            :cell-style="{ height: '40px', fontSize: '14px' }"
            :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
            stripe
            @sort-change="handleSortChange"
            v-loading="tabSqlLoading"
            style="width: 100%"
          >
            <el-table-column type="selection" width="35" align="center"></el-table-column>

            <el-table-column
              prop="sqlName"
              show-overflow-tooltip
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              label="SQL名称"
              min-width="120"
              algin="left"
              header-align="center"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.sqlName | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="sqlOperate"
              show-overflow-tooltip
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              label="执行方式"
              min-width="100"
              algin="left"
              header-align="center"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.sqlOperate | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="dUpdateTime"
              show-overflow-tooltip
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              label="修改时间"
              min-width="100"
              algin="left"
              header-align="center"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.dUpdateTime | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="fCreateName"
              show-overflow-tooltip
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              label="创建人"
              min-width="80"
              algin="left"
              header-align="center"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.fCreateName | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="sqlStatus"
              show-overflow-tooltip
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              label="状态"
              min-width="120"
              algin="left"
              header-align="center"
            >
              <template slot-scope="scope">
                <span v-if="scope.row.sqlStatus === '1'">启用</span>
                <span v-else-if="scope.row.sqlStatus === '0'">禁用</span>
                <span v-else>{{ scope.row.sqlStatus | noDataFilter }}</span>
              </template>
            </el-table-column>
          </el-table>
          <!-- 导入分页 -->
          <Pagination :total="total" :page="pageNum" :limit="pageSize" @pagination="Pagination"></Pagination>
        </el-main>
      </el-container>
    </el-dialog>
  </div>
</template>

<script>
import pageApi from '@/api/dataImport/sqlConfigManage.js'
import Pagination from '@/components/Pagination'
import commonFun from '@/filters/common.js'

export default {
  name: 'AssociatedSql',
  // 注册导入组件
  components: { Pagination },
  props: {
    // 点击查看弹窗显示传值
    sqlDialog: '',
    // 查看弹框标题传值
    sqlTitle: '',
    vcCode: ''
  },
  data() {
    return {
      formInline: {
        // SQL名称
        sqlName: '',
        // SQl编码
        sqlCode: '',
        // 执行方式
        sqlOperate: '',
        orderString: 'dUpdateTime desc nulls last', //列表排序
        limit: 10, // 条数
        offset: 0
      },
      searchRules: {},
      sqlOperateArr: [{ dimCde: '1', dimNme: 'SQL' }, { dimCde: '2', dimNme: 'BO' }, { dimCde: '3', dimNme: 'SQL+BO' }, { dimCde: '4', dimNme: '远程JSON数据' },{ dimCde: '9', dimNme: '远程JSON数据+BO' }],
      pageSize: 10,
      pageNum: 1,
      tabSqlList: [], //表格数据
      tabSqlLoading: false, //表格加载
      sqlSubmitLoading: false, // 弹框提交延迟
      sqlDialogPage: false, // 弹框
      total: 0,
      tableMultipleSelection: []
    }
  },
  created() {},
  computed: {},
  methods: {
    // table批量选择结果
    handleSelectionChange(val) {
      this.tableMultipleSelection = val
    },
    //列表点击排序
    handleSortChange(val) {
      this.formInline.orderString = commonFun.orderByString(val)
      this.sqlQuery('formInline', false)
    },
    sqlSubmit(formInline) {
      this.sqlDialogPage = false
      this.sqlSubmitLoading = false
    },
    //分页
    Pagination(val) {
      this.pageSize = val.limit //页面条数
      this.pageNum = val.page //页面
      this.formInline.offset = (val.page - 1) * val.limit
      this.formInline.limit = val.limit // 页面条数
      this.sqlQuery('formInline', false)
    },

    // 查询关联的指标列表
    sqlQuery(formName, pageNumOne) {
      var self = this

      if (pageNumOne === true) {
        this.pageNum = 1 //重新搜索初始页面为首页
        this.formInline.offset = 0
      } else {
      }
      // 消除没有值的参数
      let params = commonFun.parameterSrc(this.formInline)
      // 表格加载显示
      this.tableLoading = true
      pageApi
        .getIndParaThemeList(params)
        .then(response => {
          if (!response.data.error) {
            this.tabSqlList = response.data.rows
            // 页面总条数
            this.total = response.data.total
          } else {
            this.tabSqlList = []
            this.total = 0
            this.pageSize = 10
            this.pageNum = 1
            this.formInline.offset = 0
            this.formInline.limit = 10 // 页面条数
          }
          // 表格加载显示
          this.tableLoading = false
        })
        .catch(() => {
          // 表格加载显示
          this.tableLoading = false
          this.tabSqlList = []
          this.total = 0
          this.pageSize = 10
          this.pageNum = 1
          this.formInline.offset = 0
          this.formInline.limit = 10 // 页面条数
        })
    },
    add() {
      let arr = this.tableMultipleSelection
      if (arr.length > 0) {
        let sqlCodeArr = []
        for (let i = 0; i < arr.length; i++) {
          if (arr[i].sqlCode) {
            sqlCodeArr.push(arr[i].sqlCode)
          }
        }
        let params = {}
        params.sqlCodeArr = sqlCodeArr
        params.vcCode = this.vcCode
        //params = commonFun.parameterSrc(params);
        pageApi
          .addSqls(params)
          .then(response => {
            if (!response.data.error) {
              this.sqlDialogPage = false
              this.$emit('sqlAddClick', {
                data: [],
                flag: true
              })
            } else {
            }
          })
          .catch(() => {})
      } else {
        this.$message.closeAll()
        this.$message({
          message: '请选择数据',
          type: 'warning'
        })
      }
    }
  },
  // 监听点击确定和取消的弹框的显示和隐藏
  watch: {
    sqlDialog(val, oldval) {
      this.sqlDialogPage = true
      this.sqlQuery('formInline', true)
    }
  }
}
</script>

<style scoped>
.el-dialog {
  width: 85% !important;
  height: 500px;
}
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
.mb20 {
  margin-bottom: 20px;
}
</style>
<style lang="scss">
.associatedSqlWidth {
  width: 70% !important;
}
</style>

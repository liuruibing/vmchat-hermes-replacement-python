<template>
  <div class="indexList">
    <el-dialog
      v-dialogDrag
      :title="indexTitle"
      center
      :visible.sync="indexDialogPage"
      :close-on-click-modal="false"
    >
      <el-container class="hg100">
        <el-main class="mainBox" style="height:300px;">
          <el-form
            :inline="true"
            ref="formInline"
            :model="formInline"
            :rules="searchRules"
            style="margin-bottom: 8px;"
            class="demo-form-inline form_inline_search"
          >
            <el-row>
              <el-col :span="7">
                <el-form-item label="模板名称" prop="vcTemplatEname">
                  <el-input
                    v-model.trim="formInline.vcTemplatEname"
                    clearable
                    placeholder="请输入"
                    size="small"
                  ></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="7">
                <el-form-item label="模板类型" prop="fFileType">
                  <el-select v-model="formInline.fFileType" size="small" placeholder="请选择">
                    <el-option
                      v-for="(group, index) in fFileTypeArr"
                      :value="group.dimCde"
                      :key="index"
                      :label="group.dimNme"
                    ></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="10">
                <el-form-item class="search_button_com">
                  <el-button
                    type="primary"
                    @click="indexQuery('formInline', true)"
                    style="margin-bottom: 5px; "
                    size="small"
                  >
                    <i class="el-icon-search"></i>
                    查询
                  </el-button>
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
          <el-table
            ref="multipleTable"
            @selection-change="handleSelectionChange"
            :data="tableList"
            :default-sort="{ prop: 'vcTemplatEname', order: 'descending' }"
            :cell-style="{ height: '40px', fontSize: '14px' }"
            :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
            stripe
            @sort-change="handleSortChange"
            v-loading="tabLoading"
            style="width: 100%"
          >
            <el-table-column align="center" type="selection" width="35"></el-table-column>

            <el-table-column
              prop="vcTemplatEname"
              show-overflow-tooltip
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              label="模板名称"
              min-width="120"
              algin="left"
              header-align="center"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.vcTemplatEname | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="fFileType"
              show-overflow-tooltip
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              label="模板类型"
              min-width="100"
              algin="left"
              header-align="center"
            >
              <template slot-scope="scope">
                <span v-if="scope.row.fFileType === '1'">Excel模板</span>
                <span v-else-if="scope.row.fFileType === '2'">Word模板</span>
                <span v-else-if="scope.row.fFileType === '3'">VM模板</span>
                <span v-else-if="scope.row.fFileType === '4'">XML模板</span>
                <span v-else-if="scope.row.fFileType === '5'">TXT模板</span>
                <span v-else-if="scope.row.fFileType === '6'">XBRL模板</span>
                <span v-else>{{ scope.row.fFileType | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="vcTypeFreebus"
              show-overflow-tooltip
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              label="自定义分类类型"
              min-width="100"
              algin="left"
              header-align="center"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.vcTypeFreebus | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="vcStatus"
              show-overflow-tooltip
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              label="模板状态"
              min-width="80"
              algin="left"
              header-align="center"
            >
              <template slot-scope="scope">
                <span v-if="scope.row.vcStatus === '1'">启用</span>
                <span v-else-if="scope.row.vcStatus === '0'">禁用</span>
                <span v-else>{{ scope.row.vcStatus | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="vcPormpt"
              show-overflow-tooltip
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              label="模板说明"
              min-width="120"
              algin="left"
              header-align="center"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.vcPormpt | noDataFilter }}</span>
              </template>
            </el-table-column>

            <el-table-column label="操作" min-width="120" align="center">
              <template slot-scope="scope">
                <div class="standard-form">
                  <el-button type="info" plain size="small" @click="delData(scope.row)">删除</el-button>
                </div>
                <!-- <el-button type="primary" size="small" @click="editData(scope.row)">编辑</el-button> -->
              </template>
            </el-table-column>
          </el-table>
          <Pagination :total="total" :page="pageNum" :limit="pageSize" @pagination="Pagination"></Pagination>
        </el-main>
      </el-container>
    </el-dialog>
  </div>
</template>

<script>
import pageApi from '@/api/dataImport/indicatorConfigManage.js'
import Pagination from '@/components/Pagination'
import commonFun from '@/filters/common.js'

export default {
  name: 'IndexList',
  components: { Pagination },
  props: {
    // 点击查看弹窗显示传值
    indexDialog: '',
    // 查看弹框标题传值
    indexTitle: '',
    vcCode: ''
  },
  data() {
    return {
      formInline: {
        // 模板名称
        vcTemplatEname: '',
        vcCode: '',
        // 模板类型
        fFileType: '',
        orderStr: 'vcIndexName desc nulls last', //列表排序
        limit: 10, // 条数
        offset: 0
      },
      pageSize: 10,
      pageNum: 1,
      total: 0,
      searchRules: {},
      fFileTypeArr: [
        { dimCde: '1', dimNme: 'Excel模板' },
        { dimCde: '2', dimNme: 'Word模板' },
        { dimCde: '3', dimNme: 'VM模板' },
        { dimCde: '4', dimNme: 'XML模板' },
        { dimCde: '5', dimNme: 'TXT模板' },
        { dimCde: '6', dimNme: 'XBRL模板' }
      ],
      tableList: [], //表格数据
      tabLoading: false, //表格加载
      indexSubmitLoading: false, // 弹框提交延迟
      indexDialogPage: false // 弹框
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
      this.formInline.orderStr = commonFun.orderByString(val)
      this.indexQuery('formInline', false)
    },
    indexSubmit(formInline) {
      this.indexDialogPage = false
      this.indexSubmitLoading = false
    },
    //分页
    Pagination(val) {
      this.pageSize = val.limit //页面条数
      this.pageNum = val.page //页面
      this.formInline.offset = (val.page - 1) * val.limit
      this.formInline.limit = val.limit // 页面条数
    },

    // 查询关联的指标列表
    indexQuery(formName, pageNumOne) {
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
        .getTemplateData(params)
        .then(response => {
          if (!response.data.error) {
            this.tableList = response.data.rows
            // 页面总条数
            this.total = response.data.total
          } else {
            this.tableList = []
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
          this.tableList = []
          this.total = 0
          this.pageSize = 10
          this.pageNum = 1
          this.formInline.offset = 0
          this.formInline.limit = 10 // 页面条数
        })
    },
    // 行删除数据
    delData(row) {
      this.$confirm('确定删除?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          let params = {}
          params['vcCode'] = this.vcCode
          params['templateCode'] = row.fTemplateID

          pageApi
            .deleteTemplateData(params)
            .then(response => {
              if (response.data.status === 200) {
                this.$message.closeAll()
                this.$message({
                  message: '删除成功',
                  type: 'success'
                })
                // 刷新列表
                this.indexQuery('formInline', true)
              } else {
                this.$message.closeAll()
                this.$message({
                  message: response.data.message || '删除失败',
                  type: 'warning'
                })
              }
            })
            .catch(() => {
              this.$message.closeAll()
              this.$message({
                message: '删除失败',
                type: 'warning'
              })
            })
        })
        .catch(() => {})
    }
  },
  // 监听点击确定和取消的弹框的显示和隐藏
  watch: {
    indexDialog(val, oldval) {
      this.indexDialogPage = true
      this.formInline.vcCode = this.vcCode
      this.indexQuery('formInline', true)
    }
  }
}
</script>

<style scoped>
.el-dialog {
  width: 80% !important;
  height: 500px;
}

.el-form-item search_button_com {
  flex: right;
}

.mb20 {
  margin-bottom: 20px;
}
</style>

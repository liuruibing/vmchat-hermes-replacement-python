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
                <el-form-item label="指标名称" prop="vcIndexName">
                  <el-input
                    v-model.trim="formInline.vcIndexName"
                    clearable
                    placeholder="请输入"
                    size="small"
                  ></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="7">
                <el-form-item label="指标类型" prop="vcIndexType">
                  <el-select v-model="formInline.vcIndexType" size="small" placeholder="请选择">
                    <el-option
                      v-for="(group, index) in vcIndexTypeArr"
                      :value="group.dimCde"
                      :key="index"
                      :label="group.dimNme"
                    ></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="7">
                <el-form-item label="功能分类" prop="vcTypeBus">
                  <el-select v-model="formInline.vcTypeBus" size="small" placeholder="请选择">
                    <el-option
                      v-for="(group, index) in vcTypeBusArr"
                      :value="group.dimCde"
                      :key="index"
                      :label="group.dimNme"
                    ></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="3">
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
            :default-sort="{ prop: 'vcIndexName', order: 'descending' }"
            :cell-style="{ height: '40px', fontSize: '14px' }"
            :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
            stripe
            @sort-change="handleSortChange"
            v-loading="tabLoading"
            style="width: 100%"
          >
            <el-table-column type="selection" width="35" align="center"></el-table-column>

            <el-table-column
              prop="vcIndexName"
              show-overflow-tooltip
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              label="指标名称"
              min-width="120"
              algin="left"
              header-align="center"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.vcIndexName | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="vcIndexType"
              show-overflow-tooltip
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              label="指标类型"
              min-width="100"
              algin="left"
              header-align="center"
            >
              <template slot-scope="scope">
                <span v-if="scope.row.vcIndexType === '1'">VM指标</span>
                <span v-else-if="scope.row.vcIndexType === '2'">Excel指标</span>
                <span v-else-if="scope.row.vcIndexType === '3'">Word指标</span>
                <span v-else-if="scope.row.vcIndexType === '4'">XML指标</span>
                <span v-else-if="scope.row.vcIndexType === '5'">TXT指标</span>
                <span v-else-if="scope.row.vcIndexType === '6'">XBRL指标</span>
                <span v-else>{{ scope.row.vcIndexType | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="vcStatus"
              show-overflow-tooltip
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              label="指标状态"
              min-width="100"
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
              prop="vcTypeBus"
              show-overflow-tooltip
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              label="功能分类"
              min-width="80"
              algin="left"
              header-align="center"
            >
              <template slot-scope="scope">
                <span v-if="scope.row.vcTypeBus === '0'">普通指标</span>
                <span v-else-if="scope.row.vcTypeBus === '1'">自定义指标</span>
                <span v-else-if="scope.row.vcTypeBus === '2'">查询条件指标</span>
                <span v-else>{{ scope.row.vcTypeBus | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="vcTypeFreebus"
              show-overflow-tooltip
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              label="自定义分类类型"
              min-width="120"
              algin="left"
              header-align="center"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.vcTypeFreebus | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="vcIndexURL"
              show-overflow-tooltip
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              label="指标路径"
              min-width="80"
              algin="left"
              header-align="center"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.vcIndexURL | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="vcPrompt"
              show-overflow-tooltip
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              label="指标描述"
              min-width="80"
              algin="left"
              header-align="center"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.vcPrompt | noDataFilter }}</span>
              </template>
            </el-table-column>

            <el-table-column label="操作" min-width="120" align="center">
              <template slot-scope="scope">
                <div class="standard-form dialog-footer">
                  <el-button type="info" plain size="small" @click="delData(scope.row)">删除</el-button>
                </div>
                <!-- <el-button type="primary" size="small" @click="editData(scope.row)">编辑</el-button> -->
              </template>
            </el-table-column>
          </el-table>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer standard-form">
        <el-button type="primary" :loading="indexSubmitLoading" size="small" @click="indexSubmit(formInline)">
          确 定
        </el-button>
        <el-button size="small" type="info" plain @click="indexDialogPage = false">取 消</el-button>
      </div>
    </el-dialog>

    <!-- 新增代办 -->
    <el-dialog
      title="编辑-指标"
      customClass="calendarListWidth"
      center
      :visible.sync="countDialog"
      :close-on-click-modal="false"
    >
      <el-container>
        <el-main class="mainBox">
          <el-form
            :inline="true"
            ref="formCount"
            :model="formCount"
            :rules="countRules"
            label-position="right"
          >
            <el-form-item label="指标编码" prop="vcCode" class="mb20" :label-width="formLabelWidth">
              <el-input
                type="text"
                disabled
                v-model.trim="formCount.vcCode"
                clearable
                placeholder="请输入"
                size="small"
              ></el-input>
            </el-form-item>

            <el-form-item label="指标名称" prop="vcIndexName" class="mb20" :label-width="formLabelWidth">
              <el-input
                type="text"
                v-model.trim="formCount.vcIndexName"
                clearable
                placeholder="请输入"
                size="small"
              ></el-input>
            </el-form-item>

            <el-form-item label="功能分类" prop="vcTypeBus" class="mb20" :label-width="formLabelWidth">
              <el-select v-model="formCount.vcTypeBus" placeholder="请选择" style="width: 188px;">
                <el-option
                  v-for="(group, index) in vcTypeBusArr"
                  :value="group.dimCde"
                  :key="index"
                  :label="group.dimNme"
                ></el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="自定义分类" prop="vcTypeFreebus" class="mb20" :label-width="formLabelWidth">
              <el-select v-model="formCount.vcTypeFreebus" placeholder="请选择">
                <el-option
                  v-for="(group, index) in vcTypeFreebusArr"
                  :value="group.dimCde"
                  :key="index"
                  :label="group.dimNme"
                ></el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="指标类型" prop="vcIndexType" class="mb20" :label-width="formLabelWidth">
              <el-select v-model="formCount.vcIndexType" placeholder="请选择">
                <el-option
                  v-for="(group, index) in vcIndexTypeArr"
                  :value="group.dimCde"
                  :key="index"
                  :label="group.dimNme"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="指标状态" prop="vcStatus" class="mb20" :label-width="formLabelWidth">
              <el-select v-model="formCount.vcStatus" placeholder="请选择">
                <el-option
                  v-for="(group, index) in vcStatusArr"
                  :value="group.dimCde"
                  :key="index"
                  :label="group.dimNme"
                ></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="指标路径" prop="vcIndexURL" class="mb20" :label-width="formLabelWidth">
              <el-input
                type="textarea"
                :rows="2"
                style="width: 510px;"
                v-model="formCount.vcIndexURL"
              ></el-input>
            </el-form-item>

            <el-form-item label="指标描述" prop="vcPrompt" class="mb20" :label-width="formLabelWidth">
              <el-input
                type="textarea"
                :rows="2"
                style="width: 510px;"
                v-model="formCount.vcPrompt"
              ></el-input>
            </el-form-item>

            <el-form-item label="备注" prop="vcRemark" class="mb20" :label-width="formLabelWidth">
              <el-input
                type="textarea"
                :rows="2"
                style="width: 510px;"
                v-model="formCount.vcRemark"
              ></el-input>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" size="small" :loading="countSubmit_btn" @click="countSubmit('formCount')">
          提 交
        </el-button>
        <el-button size="small" type="info" plain @click="countDialog = false">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import pageApi from '@/api/dataImport/sqlConfigManage.js'

import commonFun from '@/filters/common.js'

export default {
  name: 'IndexList',
  props: {
    // 点击查看弹窗显示传值
    indexDialog: '',
    // 查看弹框标题传值
    indexTitle: '',
    sqlCode: ''
  },
  data() {
    return {
      formInline: {
        // 指标名称
        vcIndexName: '',
        // 指标类型
        vcIndexType: '',
        // 业务分类
        vcTypeBus: '',
        sqlCode: '',

        limit: 10, // 条数
        offset: 0
      },
      searchRules: {},

      tableList: [], //表格数据
      tabLoading: false, //表格加载
      indexSubmitLoading: false, // 弹框提交延迟
      indexDialogPage: false, // 弹框
      vcIndexTypeArr: [
        { dimCde: '1', dimNme: 'VM指标' },
        { dimCde: '2', dimNme: 'Excel指标' },
        { dimCde: '3', dimNme: 'Word指标' },
        { dimCde: '4', dimNme: 'XML指标' },
        { dimCde: '5', dimNme: 'TXT指标' },
        { dimCde: '6', dimNme: 'XBRL指标' }
      ],
      vcTypeBusArr: [
        { dimCde: '0', dimNme: '普通指标' },
        { dimCde: '1', dimNme: '自定义指标' },
        { dimCde: '2', dimNme: '查询条件指标' }
      ],
      countDialog: false,
      formCount: {
        vcCode: '', //指标编码
        vcIndexName: '', //指标名称
        vcTypeBus: '', //功能分类
        vcTypeFreebus: '', //自定义分类
        vcIndexType: '', //指标类型
        vcStatus: '', //指标状态
        vcIndexURL: '', //指标路径
        vcPrompt: '', //指标描述
        vcRemark: '' //备注
      },
      countSubmit_btn: false,
      formLabelWidth: '120px',
      countRules: {
        // SQL编码
        vcCode: [{ type: 'string', required: true, message: '请输入指标编码', trigger: 'bulr' }],
        // SQL名称
        vcIndexName: [{ required: true, type: 'string', message: '请输入指标名称', trigger: 'bulr' }]
      },
      vcStatusArr: [],
      vcTypeFreebusArr: []
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

    // 查询关联的指标列表
    indexQuery(formName, pageNumOne) {
      var self = this

      if (pageNumOne === true) {
        this.formInline.offset = 0 //重新搜索初始页面为首页
      } else {
      }
      // 消除没有值的参数
      let params = commonFun.parameterSrc(this.formInline)
      // 表格加载显示
      this.tableLoading = true
      pageApi
        .getRelationData(params)
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
            this.formInline.limit = 10 // 条数
            this.formInline.offset = 0
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
          this.formInline.limit = 10 // 条数
          this.formInline.offset = 0
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
          params['sqlCode'] = this.sqlCode
          params.vcCode = row.vcCode
          pageApi
            .indexDelete(params)
            .then(response => {
              if (!response.data.error) {
                this.$message.closeAll()
                this.$message({
                  message: '删除成功',
                  type: 'success'
                })
                // 刷新列表
                this.indexQuery('formInline', false)
              } else {
                this.$message.closeAll()
                this.$message({
                  message: '删除失败',
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
    },
    editData(row) {
      this.countDialog = true
    }
  },
  // 监听点击确定和取消的弹框的显示和隐藏
  watch: {
    indexDialog(val, oldval) {
      //console.log(this.indexDialog);
      this.indexDialogPage = true
      this.formInline.sqlCode = this.sqlCode
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

.mb20 {
  margin-bottom: 20px;
}
</style>

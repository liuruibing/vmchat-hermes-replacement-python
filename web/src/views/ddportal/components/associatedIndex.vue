<template>
  <div class="associatedIndex">
    <el-dialog v-dialogDrag :title="repTitle" center :visible.sync="repDialogPage" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox" style="height:300px;">
          <el-form :inline="true" ref="formInline" :model="formInline" :rules="searchRules" style="margin-bottom: 8px;" class="demo-form-inline form_inline_search">
            <el-row>
              <el-col :span="6">
                <el-form-item label="指标名称" prop="vcIndexName">
                  <el-input v-model.trim="formInline.vcIndexName" clearable placeholder="请输入" size="small"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item label="指标类型" prop="vcIndexType">
                  <el-select v-model="formInline.vcIndexType" size="small" placeholder="请选择">
                    <el-option v-for="(group, index) in vcIndexTypeArr" :value="group.dimCde" :key="index" :label="group.dimNme"></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item label="功能分类" prop="vcTypeBus">
                  <el-select v-model="formInline.vcTypeBus" size="small" placeholder="请选择">
                    <el-option v-for="(group, index) in vcTypeBusArr" :value="group.dimCde" :key="index" :label="group.dimNme"></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="6">
                <el-form-item class="search_button_com">
                  <el-button type="primary" @click="repQuery('formInline', true)" style="margin-bottom: 5px; " size="small">
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
          <span class="title-style">指标配置列表</span>
          <el-table
            ref="multipleTable"
            @selection-change="handleSelectionChange"
            :data="tabReplist"
            :default-sort="{ prop: 'vcTemplatEname', order: 'descending' }"
            :cell-style="{ height: '40px', fontSize: '14px' }"
            :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
            stripe
            @sort-change="handleSortChange"
            v-loading="tabRepLoading"
            style="width: 100%"
          >
            <el-table-column align="center" type="selection" width="35"></el-table-column>

            <el-table-column type="index" label="序号" fixed align="center" width="40" />
            <el-table-column
              prop="vcIndexName"
              show-overflow-tooltip
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              label="指标名称"
              min-width="100"
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
              prop="vcTypeBus"
              show-overflow-tooltip
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              label="功能分类"
              min-width="120"
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
              min-width="120"
              algin="left"
              header-align="center"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.vcIndexURL | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="updateTime"
              show-overflow-tooltip
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              label="更新时间"
              min-width="120"
              algin="left"
              header-align="center"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.updateTime | noDataFilter }}</span>
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
import pageApi from '@/api/dataImport/indicatorConfigManage.js'
import Pagination from '@/components/Pagination'
import commonFun from '@/filters/common.js'

export default {
  name: 'AssociatedIndex',
  // 注册导入组件
  components: { Pagination },
  props: {
    // 点击查看弹窗显示传值
    repDialog: '',
    // 查看弹框标题传值
    repTitle: '',
    fTemplateID: ''
  },
  data() {
    return {
      formInline: {
        // 指标名称
        vcIndexName: '',
        // 指标类型
        vcIndexType: '',
        // S业务类型
        vcTypeBus: '',
        orderStr: 'vcIndexName desc nulls last', //列表排序
        limit: 10, // 条数
        offset: 0
      },
      pageSize: 10,
      pageNum: 1,
      searchRules: {},
      vcIndexTypeArr: [
        { dimCde: '1', dimNme: 'VM指标' },
        { dimCde: '2', dimNme: 'Excel指标' },
        { dimCde: '3', dimNme: 'Word指标' },
        { dimCde: '4', dimNme: 'XML指标' },
        { dimCde: '5', dimNme: 'TXT指标' },
        { dimCde: '6', dimNme: 'XBRL指标' }
      ],
      vcTypeBusArr: [{ dimCde: '0', dimNme: '普通指标' }, { dimCde: '1', dimNme: '自定义指标' }, { dimCde: '2', dimNme: '查询条件指标' }],
      vcStatusArr: [{ dimCde: '1', dimNme: '启用' }, { dimCde: '0', dimNme: '禁用' }],
      indexGrantArr: [{ dimCde: 'All', dimNme: '无权限控制' }],
      tabReplist: [], //表格数据
      tabRepLoading: false, //表格加载
      tabRepLoading: false, // 弹框提交延迟
      repDialogPage: false, // 弹框
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
      this.formInline.orderStr = commonFun.orderByString(val)
      this.repQuery('formInline', false)
    },
    repSubmit(formInline) {
      this.repDialogPage = false
      this.tabRepLoading = false
    },
    Pagination(val) {
      this.pageSize = val.limit //页面条数
      this.pageNum = val.page //页面
      this.formInline.offset = (val.page - 1) * val.limit
      this.formInline.limit = val.limit // 页面条数
      this.repQuery('formInline', false)
    },
    // 查询关联的指标列表
    repQuery(formName, pageNumOne) {
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
            this.tabReplist = response.data.rows
            // 页面总条数
            this.total = response.data.total
          } else {
            this.tabReplist = []
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
          this.tabReplist = []
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
        let indexCodes = []
        for (let i = 0; i < arr.length; i++) {
          if (arr[i].vcCode) {
            indexCodes.push(arr[i].vcCode)
          }
        }
        let params = {}
        params.indexCodes = indexCodes
        params.fTemplateID = this.fTemplateID
        //params = commonFun.parameterSrc(params);
        pageApi
          .addIndicator(params)
          .then(response => {
            if (!response.data.error) {
              this.repDialogPage = false
              this.$emit('sqlAddClick', {
                data: [],
                flag: true,
                fTemplateID: this.fTemplateID
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
    repDialog(val, oldval) {
      this.repDialogPage = true
      this.repQuery('formInline', true)
    }
  }
}
</script>

<style scoped>
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
.el-dialog {
  width: 80% !important;
  height: 500px;
}

.mb20 {
  margin-bottom: 20px;
}
</style>

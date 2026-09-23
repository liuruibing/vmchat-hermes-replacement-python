<template>
  <div class="setTaskGroup ddportal-ui">
    <el-form :inline="true" class="formQuery">
      <el-row>
        <el-col :span="16">
          <!-- 查询 -->
          <div class="grid-content bg-purple">
            <el-form-item label="任务组编码" prop="grpCde">
              <el-input v-model.trim="formQuery.grpCde" clearable placeholder="请输入任务组编码" size="small"></el-input>
            </el-form-item>
            <el-form-item label="任务组名称" prop="grpNme">
              <el-input v-model.trim="formQuery.grpNme" clearable placeholder="请输入任务组名称" size="small"></el-input>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="8">
          <el-form-item class="search_button_com">
            <el-button type="primary" :disabled="btnDisabled" icon="el-icon-search" class="mb5" size="small" @click="onQuery(true)">
              查询
            </el-button>
            <el-button type="primary" plain size="small" icon="el-icon-circle-plus-outline" @click="addDate">
              新增
            </el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <div style="vertical-align: middle;display: inline-block;">
      <div class="color-box"></div>
    </div>
    <span class="title-style">任务组设置信息</span>

    <el-table
      ref="multipleTable"
      :data="tableData"
      :default-sort="{ prop: 'vcBeDate', order: 'descending' }"
      stripe
      @sort-change="handleSortChange"
      v-loading="tableLoading"
      style="width: 100%"
      :cell-style="{ height: '40px', fontSize: '14px' }"
      :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
    >
      <el-table-column prop="grpCde" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="任务组编码" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.grpCde | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="grpNme" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="任务组名称" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.grpNme | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="grpMsg" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="任务组说明" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.grpMsg | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="misRun" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="是否启用" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.misRun | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column label="操作" min-width="120" align="center">
        <template slot-scope="scope">
         <div class="standard-form dialog-footer">
          <el-button type="info" size="small" plain @click="editData(scope.row)">编辑</el-button>
          <el-button type="info" plain size="small" @click="delData(scope.row)">删除</el-button>
          <el-button :disabled="scope.row.misRun == '禁用'" type="info" size="small" plain @click="handleData(scope.row)">
            手工执行
          </el-button>
         </div>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <Pagination :total="total" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination"></Pagination>

    <!-- 新增/修改 参数弹窗 -->
    <el-dialog title="任务组信息" center :visible.sync="dialogMask" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox">
          <el-form :inline="true" ref="formDialog" :model="formDialog" :rules="dialogRules" label-position="right">
            <el-form-item label="任务组编码" prop="grpCde" class="mb20" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog.grpCde" disabled clearable placeholder="请输入" size="small" v-if="operationType == 2"></el-input>
              <el-input v-model.trim="formDialog.grpCde" clearable placeholder="请输入" size="small" v-else></el-input>
            </el-form-item>
            <el-form-item label="任务组名称" prop="grpNme" class="mb20" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog.grpNme" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>
            <el-form-item label="任务组说明" prop="grpMsg" class="mb20" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog.grpMsg" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>
            <el-form-item label="是否启用" prop="misRun" class="mb20" :label-width="formLabelWidth">
              <el-select v-model.trim="formDialog.misRun" placeholder="请选择" size="small">
                <el-option label="启用" value="1"></el-option>
                <el-option label="禁用" value="0"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="组内执行方式" prop="grpRunType" class="mb20" :label-width="formLabelWidth">
              <el-select v-model.trim="formDialog.grpRunType" placeholder="请选择" size="small">
                <el-option label="并行" value="1"></el-option>
                <el-option label="串行" value="0"></el-option>
              </el-select>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>

      <div v-if="operationType == 2">
        <div style="float:right">
          <el-button type="primary" plain size="small" @click="addMis">新增任务</el-button>
        </div>
        <div style="vertical-align: middle;display: inline-block;">
          <div class="color-box"></div>
        </div>
        <span class="title-style">任务列表(从上往下执行)</span>
     <div class="dialog-footer standard-form">
      <el-button style="padding-left:12px" type="info" plain size="small" @click="getrun">启用</el-button>
        <el-button type="info"  plain size="small" @click="notrun">禁用</el-button>
        <el-button type="info" plain size="small" @click="deletall">删除</el-button>
     </div>
        <el-table
          ref="multipleTable"
          :data="tableData2"
          @selection-change="handleSelectionChange"
          stripe
          @sort-change="handleSortChange2"
          v-loading="tableLoading2"
          style="width: 100%"
          row-key="id"
          :highlight-current-row="false"
          :cell-style="{ height: '40px', fontSize: '14px' }"
          :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
        >
          <el-table-column type="selection" width="35"></el-table-column>

          <el-table-column type="index" label="序号" align="center" width="40"></el-table-column>
          <el-table-column prop="relCde" show-overflow-tooltip label="关系编码" min-width="100" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.relCde | noDataFilter }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="misCde" show-overflow-tooltip label="任务编码" min-width="100" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.misCde | noDataFilter }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="misNme" show-overflow-tooltip label="任务名称" min-width="100" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.misNme | noDataFilter }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="misType" show-overflow-tooltip label="类型" min-width="60" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.misType | noDataFilter }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="misRun" show-overflow-tooltip label="是否启用" min-width="80" header-align="center">
            <template slot-scope="scope">
              <!-- <span>{{scope.row.misRun | noDataFilter}}</span> -->
              <span v-if="scope.row.misRun == '启用'">启用</span>
              <span style="color:red" v-if="scope.row.misRun == '禁用'">禁用</span>
            </template>
          </el-table-column>
          <el-table-column prop="misCmt" show-overflow-tooltip label="任务说明" min-width="100" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.misCmt | noDataFilter }}</span>
            </template>
          </el-table-column>

          <el-table-column label="操作" min-width="150" align="center">
            <template slot-scope="scope">
             <div class="dialog-footer standard-form">
              <el-button size="small" type="info" plain :disabled="scope.$index === 0" @click="moveUp(scope.$index, scope.row)">
                上移
              </el-button>
              <el-button size="small" type="info" plain :disabled="scope.$index === tableData2.length - 1" @click="moveDown(scope.$index, scope.row)">
                下移
              </el-button>
             </div>
            </template>
          </el-table-column>
        </el-table>

        <!--        <Pagination-->
        <!--          :total="total3"-->
        <!--          :limit="formQuery2.pageSize"-->
        <!--          :page="formQuery2.pageNum"-->
        <!--          @pagination="pagination3"-->
        <!--        ></Pagination>-->
      </div>

      <div slot="footer" class="dialog-footer standard-form">
        <el-button type="primary" size="small" @click="dealData">提 交</el-button>
        <el-button type="info" size="small" plain @click="dialogMask = false">取 消</el-button>
      </div>
    </el-dialog>

    <!-- 手工执行 参数弹窗2 -->
    <el-dialog :title="handleWord" center :visible.sync="dialogMask2" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox">
          <el-form :inline="true" ref="formDialog2" :model="formDialog2" :rules="dialogRules2" label-position="right">
            <el-form-item label="日期" prop="date" :label-width="'100px'" class="mb20">
              <el-date-picker
                v-model="formDialog2.date"
                type="daterange"
                unlink-panels
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                value-format="yyyy-MM-dd"
                :picker-options="dateShortcut()"
                size="small"
              ></el-date-picker>
            </el-form-item>
            <el-form-item label="自定义参数（json格式）" prop="custom" class="mb20 ddCode-mirror-form ddCode-mirror-form-200" :label-width="'175px'">
              <!-- js语言需要传入一个特殊的值，来区别是js还是json -->
              <dd-code-mirror ref="customCodeMirror" :language="customLanguage" scriptLanguage="json" @codeChange="customChange"></dd-code-mirror>
            </el-form-item>

            <el-form-item label="产品代码" prop="fundCodes" class="mb20 formInput-adaptive-100" :label-width="'100px'">
              <el-input v-model.trim="formDialog2.fundCodes" clearable placeholder="请输入产品代码" type="textarea" style="width:535px" @focus="focusCode"></el-input>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer standard-form">
        <el-button type="primary" size="small" @click="handledealData">提 交</el-button>
        <el-button type="info" size="small" plain @click="dialogMask2 = false">取 消</el-button>
      </div>
    </el-dialog>
    <!-- 任务组下 添加任务 参数弹窗3 -->
    <el-dialog title="任务添加" center :visible.sync="dialogMask3" :close-on-click-modal="false">
      <el-row>
        <div style="float:right;margin-bottom:10px">
          <el-button type="primary" plain size="small" icon="el-icon-search" @click="onQuery2(true)">
            查询
          </el-button>
        </div>
      </el-row>
      <el-container class="hg100">
        <el-main class="mainBox">
          <el-form :inline="true" ref="formDialog3" :model="formDialog3" :rules="dialogRules3" label-position="right">
            <el-form-item label="任务编码" prop="grpCdeLike" class="mb20">
              <el-input v-model.trim="formDialog3.grpCdeLike" clearable placeholder="请输入任务编码" size="small"></el-input>
            </el-form-item>

            <el-form-item label="任务名称" prop="grpMisNme" class="mb20">
              <el-input v-model.trim="formDialog3.grpMisNme" clearable placeholder="请输入任务名称" size="small"></el-input>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>

      <div style="vertical-align: middle;display: inline-block;">
        <div class="color-box"></div>
      </div>
      <span class="title-style">任务列表</span>
      <el-table
        ref="multipleTable"
        :data="tableData3"
        @selection-change="handleSelectionChange"
        :default-sort="{ prop: 'relCde', order: 'descending' }"
        stripe
        v-loading="tableLoading3"
        style="width: 100%"
        :cell-style="{ height: '40px', fontSize: '14px' }"
        :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
      >
        <el-table-column type="selection" width="40" align="center"></el-table-column>

        <el-table-column type="index" label="序号" align="center" width="40"></el-table-column>
        <el-table-column prop="grpMisCde" show-overflow-tooltip label="任务编码" min-width="100" header-align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.grpMisCde | noDataFilter }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="grpMisNme" show-overflow-tooltip label="任务名称" min-width="100" header-align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.grpMisNme | noDataFilter }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="whtGrp" show-overflow-tooltip label="任务类型" min-width="100" header-align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.whtGrp | noDataFilter }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="grpMisRun" show-overflow-tooltip label="是否启用" min-width="100" header-align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.grpMisRun | noDataFilter }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="grpMisMsg" show-overflow-tooltip label="任务说明" min-width="100" header-align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.grpMisMsg | noDataFilter }}</span>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页2 -->
      <Pagination :total="total2" :limit="formDialog3.pageSize" :page="formDialog3.pageNum" @pagination="pagination2"></Pagination>

      <div slot="footer" class="dialog-footer standard-form">
        <el-button type="primary" size="small" @click="addMisJob">提 交</el-button>
        <el-button type="info" size="small" plain @click="dialogMask3 = false">取 消</el-button>
      </div>
    </el-dialog>

    <!--手工执行 查询代码 弹窗4  -->
    <el-dialog title="选择产品" center :visible.sync="dialogMask4" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox">
          <el-form :inline="true" ref="formDialog4" :model="formDialog4" label-position="right">
            <el-form-item label="组合代码" prop="fundCode" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog4.fundCode" clearable placeholder="请输入产品代码" size="small"></el-input>
            </el-form-item>
            <el-form-item label="组合名称" prop="fundName" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog4.fundName" clearable placeholder="请输入组合名称" size="small"></el-input>
            </el-form-item>
          </el-form>
          <el-row>
            <div style="float:right;margin-bottom:10px">
              <el-button type="primary" plain size="small" @click="onQuery4(true)">查询</el-button>
              <el-button type="primary" plain size="small" @click="handleSelect">选择</el-button>
            </div>
          </el-row>

          <div class="forms_table_title">
            <i class="el-icon-tickets"></i>
            产品信息
          </div>
          <el-table
            ref="multipleTable"
            :data="tableData4"
            @selection-change="handleSelectionChange"
            stripe
            :default-sort="{ prop: 'fundCode', order: 'descending' }"
            @sort-change="handleSortChange4"
            v-loading="tableLoading4"
            style="width: 100%"
            row-key="id"
            :cell-style="{ height: '40px', fontSize: '14px' }"
            :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
          >
            <el-table-column type="selection" width="35"></el-table-column>

            <el-table-column
              prop="fundCode"
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              show-overflow-tooltip
              label="产品代码"
              min-width="100"
              header-align="center"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.fundCode | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="fundName"
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              show-overflow-tooltip
              label="产品名称"
              min-width="100"
              header-align="center"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.fundName | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="nameTgr"
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              show-overflow-tooltip
              label="托管人名称"
              min-width="100"
              header-align="center"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.nameTgr | noDataFilter }}</span>
              </template>
            </el-table-column>
          </el-table>

          <Pagination :total="total4" :limit="formDialog4.pageSize" :page="formDialog4.pageNum" @pagination="pagination4"></Pagination>
        </el-main>
      </el-container>
    </el-dialog>
  </div>
</template>

<script>
import commonApi from '@/api/etl/setTaskGroup'
import Pagination from '@/components/Pagination'
import fun from '@/filters/common'
import DdCodeMirror from '@/components/codemirror'
import commonValidate from '@/utils/validate'
export default {
  name: 'DdSetTaskGroup',
  components: {
    Pagination,
    DdCodeMirror
  },

  data() {
    return {
      tableData: [], //表格 数据
      tableLoading: false, //表格 加载
      tableData2: [], //表格2 数据
      tableLoading2: false, //表格2 加载
      tableData3: [], //表格3 数据
      tableLoading3: false, //表格3 加载
      tableData4: [], //表格4 数据
      tableLoading4: false, //表格4 加载
      dialogMask: false, // 弹窗
      dialogMask2: false, // 弹窗 2
      dialogMask3: false, // 弹窗 3
      dialogMask4: false, // 弹窗 4

      // 任务类型集合
      jobTypeArr: [],
      // //总条数
      total: 0,
      total2: 0,
      total3: 0,

      total4: 0,

      // 顶部查询条件
      formQuery: {
        // 任务组编码
        grpCde: '',
        // 任务组名称
        grpNme: '',
        // 排序字段
        orderBy: 'grpCde desc',
        // 起始页
        pageNum: 1,
        // 每页大小
        pageSize: 10
      },
      // 弹窗查询参数
      formDialog: {
        //  任务编码
        grpCde: '',
        // 任务名称
        grpNme: '',
        // 任务说明
        grpMsg: '',
        // 任务类型
        grpRunType: '0',
        // 是否启用
        misRun: '1',
        // 关系id
        relIds: ''
      },
      // 弹窗2查询参数
      formDialog2: {
        // 日期
        date: [],
        // 产品编码
        fundCodes: '',
        // 任务组编码
        grpCde: '',
        // 自定义参数
        custom: ''
      },
      customLanguage: 'javascript', //自定义参数编辑器语言类型
      // 查询2
      formQuery2: {
        grpCde: '',
        orderBy: '',
        pageNum: 1,
        pageSize: 9999999
      },
      // 弹窗3查询参数
      formDialog3: {
        // 任务类型
        whtGrp: '',
        // 任务名称
        grpMisNme: '',
        // 排序
        orderBy: 'grpMisCde desc',
        pageNum: 1,
        pageSize: 10,
        // 任务组编码
        grpCde: '',
        // 任务编码
        grpCdeLike: ''
      },

      // 弹窗验证规则
      dialogRules: {
        // 任务编码
        grpCde: [{ required: true, message: '请填写任务组编码', trigger: 'change' }],
        // 任务名称
        grpNme: [{ required: true, message: '请填写任务组名称', trigger: 'change' }]
      },
      // 弹窗验证规则
      dialogRules2: {
        // 日期
        date: [{ required: true, message: '请填写日期', trigger: 'change' }]
      },
      // 弹窗验证规则
      dialogRules3: {
        // 日期
        date: [{ required: true, message: '请填写日期', trigger: 'change' }]
      },
      // 弹窗4 查询参数
      formDialog4: {
        // 组合代码
        fundCode: '',
        // 组合名称
        fundName: '',
        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10,
        // 排序条件
        orderBy: ''
      },
      // 手工执行传给接口的产品代码
      handlefundCodes: '',
      // 手工执行显示文字
      handleWord: '手工执行',
      // 操作类型 1、添加 2、编辑
      operationType: 1,
      formLabelWidth: '150px',
      // 批量启用的数据
      multipleSelection: [],
      // 查询按钮禁用
      btnDisabled: false
    }
  },
  mounted() {
    // 默认查询
    this.onQuery(true)
  },
  methods: {
    // 日期快捷选项
    dateShortcut() {
      return fun.dateShortcut()
    },
    //行拖拽
    // rowDrop() {
    //   const tbody = document.querySelector(".el-table__body-wrapper tbody");
    //   const _this = this;
    //   Sortable.create(tbody, {
    //     onEnd({ newIndex, oldIndex }) {
    //       const currRow = _this.tableData2.splice(oldIndex, 1)[0];
    //       _this.tableData2.splice(newIndex, 0, currRow);
    //     }
    //   });
    // },
    // 添加代码需要唯一性
    onlyCode() {
      let params = { grpCde: this.formDialog.grpCde }
      commonApi
        .getTaskSetByCode(params)
        .then(res => {
          if (res.data.status == 200) {
            this.$message.closeAll()
            this.$message.error('编码已经存在，请勿重复添加！')
            this.dialogMask = false
          } else {
            this.addParamSet()
          }
        })
        .catch(() => {})
    },

    // 查询
    onQuery(flag) {
      this.tableLoading = true
      if (flag) {
        this.formQuery.pageNum = 1
      }
      let params = Object.assign({}, this.formQuery)
      commonApi
        .getTaskGroupList(params)
        .then(res => {
          this.tableLoading = false

          let { list, total } = res.data.data
          // 总条数
          this.total = total
          this.tableData = []
          list.forEach(item => {
            if (item.misRun == 1) {
              item.misRun = '启用'
            } else {
              item.misRun = '禁用'
            }
            this.tableData.push(item)
          })
        })
        .catch(() => {})
    },
    // 查询任务组和任务
    onQuery2(flag) {
      this.tableLoading3 = true
      if (flag) {
        this.formDialog3.pageNum = 1
      }
      let params = Object.assign({}, this.formDialog3)
      commonApi
        .doMisGrpList(params)
        .then(res => {
          this.tableLoading3 = false
          let { list, total } = res.data.data
          // 总条数
          this.total2 = total
          this.tableData3 = []
          list.forEach(item => {
            if (item.grpMisRun == 1) {
              item.grpMisRun = '启用'
            } else {
              item.grpMisRun = '禁用'
            }
            if (item.whtGrp == 1) {
              item.whtGrp = '任务组'
            } else {
              item.whtGrp = '任务'
            }
            this.tableData3.push(item)
          })
        })
        .catch(() => {})
    },
    // 手工执行下 查询代码
    onQuery4(flag) {
      if (flag) {
        this.formDialog4.pageNum = 1
      }
      let params = Object.assign({}, this.formDialog4)

      commonApi
        .getFundList(params)
        .then(res => {
          this.tableLoading4 = false

          let { list, total } = res.data.data
          // 总条数
          this.total4 = total
          this.tableData4 = list
        })
        .catch(() => {})
    },

    // 新增按钮
    addDate() {
      this.dialogMask = true
      this.operationType = 1
      this.$nextTick(() => {
        this.$refs['formDialog'].resetFields()
      })
    },
    // 处理数据
    dealData() {
      this.$refs['formDialog'].validate(valid => {
        if (valid) {
          if (this.operationType === 1) {
            // 添加
            this.onlyCode()
          } else {
            // 修改
            this.updateParamSet()
          }
        }
      })
    },
    // 添加参数
    addParamSet() {
      this.dialogMask = false
      let params = Object.assign({}, this.formDialog)
      commonApi
        .addTaskGroup(params)
        .then(res => {
          if (res.data.status === 200) {
            this.onQuery(true)
            this.$message.closeAll()

            this.$message({
              type: 'success',
              message: res.data.message
            })
          } else {
            this.$message.closeAll()

            this.$message.error(res.data.message)
          }
        })
        .catch(() => {})
    },
    // 修改参数
    updateParamSet() {
      let str = []
      this.tableData2.forEach(item => {
        str.push(item.relCde)
      })
      // 数组倒叙
      // str.reverse();
      this.formDialog.relIds = str.join(',')

      this.dialogMask = false
      let params = Object.assign({}, this.formDialog)

      if (params.misRun == '启用') {
        params.misRun = '1'
      } else if (params.misRun == '禁用') {
        params.misRun = '0'
      }

      commonApi
        .updateTaskGroup(params)
        .then(res => {
          if (res.data.status === 200) {
            this.onQuery(false)
            this.$message.closeAll()

            this.$message({
              type: 'success',
              message: res.data.message
            })
          } else {
            this.$message.closeAll()

            this.$message.error(res.data.message)
          }
        })
        .catch(() => {})
    },
    // 单个删除
    deleteParamSet(grpCde) {
      let params = { grpCde: grpCde }
      commonApi
        .deleteTaskGroup(params)
        .then(res => {
          if (res.data.status === 200) {
            this.onQuery(false)
            this.$message.closeAll()

            this.$message({
              type: 'success',
              message: res.data.message
            })
          } else {
            this.$message.closeAll()

            this.$message.error(res.data.message)
          }
        })
        .catch(() => {})
    },
    // 批量选择数据
    handleSelectionChange(val) {
      this.multipleSelection = val
    },
    //列表点击排序
    handleSortChange(val) {
      this.formQuery.orderBy = fun.etlqueryOrderBy(val)
      // 查询
      this.onQuery(false)
    },
    // 行编辑
    editData(row) {
      this.dialogMask = true
      this.operationType = 2

      this.$nextTick(() => {
        // 清除
        this.$refs['formDialog'].resetFields()

        let { grpCde, grpMsg, grpNme, grpRunType, misRun } = row

        this.formDialog.grpCde = grpCde
        this.formDialog.grpMsg = grpMsg
        this.formDialog.grpNme = grpNme
        this.formDialog.grpRunType = grpRunType
        this.formDialog.misRun = misRun

        // 获取任务组下任务列表
        this.formQuery2.grpCde = grpCde
        // 新增任务查询 获取任务组编码
        this.formDialog3.grpCde = grpCde

        this.getTaskByTaskGroup(true)
      })
    },
    // 行删除
    delData(row) {
      this.$confirm('确认删除该条数据?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          // 删除单个
          this.deleteParamSet(row.grpCde)
        })
        .catch(() => {})
    },
    // 手工执行的处理数据
    handleData(row) {
      this.handleWord = row.grpNme + '(' + row.grpCde + ')'

      this.handlemisCde = row.grpCde
      this.dialogMask2 = true
      this.$nextTick(() => {
        // 清除数据
        this.$refs['formDialog2'].resetFields()
        this.handlefundCodes = ''
        // 清空自定义参数的值
        this.$refs.customCodeMirror.operationVal(null)
      })
    },
    // 自定义参数赋值给页面变量
    customChange(val) {
      this.formDialog2.custom = val
    },
    // 手工执行
    handledealData() {
      this.$refs['formDialog2'].validate(valid => {
        if (valid) {
          // 判自定义参数是否是json格式的
          if (this.formDialog2.custom) {
            if (commonValidate.isJSON(this.formDialog2.custom) === false) {
              this.$message.closeAll()
              this.$message({
                type: 'warning',
                message: '自定义参数必须是json格式！'
              })
              return false
            }
          } else {
          }
          let params = Object.assign({}, this.formDialog2)

          params.beginDate = params.date[0]
          params.endDate = params.date[1]
          delete params.date
          params.grpCde = this.handlemisCde
          // 手工执行的名字变成代传参
          params.fundCodes = this.handlefundCodes

          // 手工执行
          commonApi
            .implementTaskGroup(params)
            .then(res => {
              this.$message.closeAll()
              if (res.data.status == 200) {
                this.$message({
                  type: 'success',
                  message: res.data.message
                })

                this.dialogMask2 = false
              } else {
                this.$message({
                  type: 'error',
                  message: res.data.message
                })
              }
            })
            .catch(() => {})
        }
      })
    },
    // 手工执行下 查询代码
    focusCode() {
      this.dialogMask4 = true
      this.tableLoading4 = true
      this.onQuery4(true)
    },
    // 手工执行下查询代码 排序
    handleSortChange4(val) {
      this.formDialog4.orderBy = fun.queryOrderBy(val)
      // 查询
      this.onQuery4(false)
    },
    // 手工执行下 添加代码
    handleSelect() {
      let code = []
      let codename = []

      this.multipleSelection.forEach(item => {
        code.push(item.fundCode)
        codename.push(item.fundName)
      })
      this.formDialog2.fundCodes = codename.join(',')
      this.handlefundCodes = code.join(',')

      // 关闭弹窗 并提示
      this.dialogMask4 = false
      this.$message.closeAll()
      this.$message({
        type: 'success',
        message: '添加成功！'
      })
    },
    // 上移
    moveUp(index, row) {
      if (index > 0) {
        let upDate = this.tableData2[index - 1]
        this.tableData2.splice(index - 1, 1)
        this.tableData2.splice(index, 0, upDate)
      }
    },
    // 下移
    moveDown(index, row) {
      if (index + 1 !== this.tableData2.length) {
        let downDate = this.tableData2[index + 1]
        this.tableData2.splice(index + 1, 1)
        this.tableData2.splice(index, 0, downDate)
      }
    },
    //  获取任务组下任务列表
    getTaskByTaskGroup(flag) {
      this.tableLoading2 = true
      if (flag) {
        this.formQuery2.pageNum = 1
      }
      let params = Object.assign({}, this.formQuery2)

      commonApi
        .getTaskByTaskGroupCode(params)
        .then(res => {
          this.tableLoading2 = false
          let { list, total } = res.data.data
          // 总条数
          this.total3 = total
          this.tableData2 = []
          list.forEach(item => {
            if (item.misRun == 1) {
              item.misRun = '启用'
            } else {
              item.misRun = '禁用'
            }
            if (item.misType == 1) {
              item.misType = '任务组'
            } else {
              item.misType = '任务'
            }
            this.tableData2.push(item)
          })
        })
        .catch(() => {})
    },
    // 任务组下添加任务
    addMis() {
      this.dialogMask3 = true
      this.onQuery2(true)
    },
    // 任务组下启用
    getrun() {
      if (this.multipleSelection.length) {
        // 批量删除
        let arr = []
        let str = {}

        this.multipleSelection.forEach(item => {
          arr.push(item.relCde)
        })

        str.relIds = arr.join(',')
        str.isRun = '1'

        commonApi
          .taskGroupOpen(str)
          .then(res => {
            if (res.data.status === 200) {
              // 刷新列表
              this.getTaskByTaskGroup(false)
              this.$message.closeAll()

              this.$message({
                type: 'success',
                message: res.data.message
              })
            } else {
              this.$message.closeAll()

              this.$message.error(res.data.message)
            }
          })
          .catch(() => {})
      }
    },
    // 任务组下禁用
    notrun() {
      if (this.multipleSelection.length) {
        // 批量删除
        let arr = []
        let str = {}

        this.multipleSelection.forEach(item => {
          arr.push(item.relCde)
        })

        str.relIds = arr.join(',')
        str.isRun = 0

        commonApi
          .taskGroupOpen(str)
          .then(res => {
            if (res.data.status === 200) {
              // 刷新列表
              this.getTaskByTaskGroup(false)
              this.$message.closeAll()

              this.$message({
                type: 'success',
                // message: res.data.message
                message: '禁用成功'
              })
            } else {
              this.$message.closeAll()

              this.$message.error(res.data.message)
            }
          })
          .catch(() => {})
      }
    },
    // 最内层添加
    addMisJob() {
      if (!this.multipleSelection.length) {
        this.$message.closeAll()

        this.$message({
          type: 'warning',
          message: '请选择一条或者多条数据'
        })
      } else {
        let misCdes = []
        let misRuns = []
        let misTypes = []
        let selectType = ''
        let selectMis = ''

        this.multipleSelection.forEach(item => {
          if (item.grpMisRun == '启用') {
            selectMis = '1'
          } else {
            selectMis = '0'
          }
          if (item.whtGrp == '任务组') {
            selectType = '1'
          } else {
            selectType = '0'
          }
          misCdes.push(item.grpMisCde)
          misRuns.push(selectMis)
          misTypes.push(selectType)
        })

        let params = {
          grpCdes: this.formDialog3.grpCde, //任务组编号
          misCdes: misCdes.join(','), //任务编号
          misRuns: misRuns.join(','), //是否运行
          misTypes: misTypes.join(',') //任务类型
        }
        commonApi
          .addMisRelGrpSet(params)
          .then(res => {
            if (res.data.status === 200) {
              // 刷新列表
              this.getTaskByTaskGroup(true)
              this.dialogMask3 = false
              this.$message.closeAll()

              this.$message({
                type: 'success',
                message: res.data.message
              })
            } else {
              this.$message.closeAll()

              this.$message({
                type: 'error',
                message: '添加失败'
              })
            }
          })
          .catch(() => {})
      }
    },
    // 任务组下批量删除
    deletall() {
      if (this.multipleSelection.length) {
        this.$confirm('确认删除这些数据吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
        })
          .then(() => {
            // 批量删除
            let arr = []
            let str = {}

            this.multipleSelection.forEach(item => {
              arr.push(item.relCde)
            })
            str.relIds = arr.join(',')

            commonApi
              .deleteGrpMisRel(str)
              .then(res => {
                if (res.data.status === 200) {
                  // 刷新列表
                  this.getTaskByTaskGroup(false)
                  this.$message.closeAll()

                  this.$message({
                    type: 'success',
                    message: res.data.message
                  })
                } else {
                  this.$message.closeAll()

                  this.$message.error(res.data.message)
                }
              })
              .catch(() => {})
          })
          .catch(() => {})
      }
    },
    //任务组列表点击排序
    handleSortChange2(val) {
      this.formQuery2.orderBy = fun.etlqueryOrderBy(val)
      // 查询
      this.getTaskByTaskGroup(false)
    },

    //  分页
    pagination(val) {
      let { page, limit } = val
      // 起始页
      this.formQuery.pageNum = page
      // 每页数量
      this.formQuery.pageSize = limit
      // 查询
      this.onQuery(false)
    },
    //  分页2
    pagination2(val) {
      let { page, limit } = val
      // 起始页
      this.formDialog3.pageNum = page
      // 每页数量
      this.formDialog3.pageSize = limit
      // 查询
      this.onQuery2(false)
    },
    //  分页3
    pagination3(val) {
      let { page, limit } = val
      // 起始页
      this.formQuery2.pageNum = page
      // 每页数量
      this.formQuery2.pageSize = limit
      // 查询
      this.getTaskByTaskGroup(false)
    },
    //  分页4
    pagination4(val) {
      let { page, limit } = val
      // 起始页
      this.formDialog4.pageNum = page
      // 每页数量
      this.formDialog4.pageSize = limit
      // 查询
      this.onQuery4(false)
    }
  }
}
</script>

<style lang="scss" scoped>
.setTaskGroup {
  padding-left: 10px;
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
    width: 60% !important;
    .el-form {
      width: 100% !important;
      font-size: 0;
    }
    .el-form-item {
      min-width: 50%;
      margin-right: 0;
      // margin-bottom: 20px !important;
    }
    .mr5 {
      margin-right: 5px;
    }
  }

  .mb20 {
    margin-bottom: 15px !important;
  }

  // 火狐移除
  input[type='number'] {
    -moz-appearance: textfield;
  }

  //谷歌下的移除
  input[type='number']::-webkit-inner-spin-button,
  input[type='number']::-webkit-outer-spin-button {
    -webkit-appearance: none;
  }
}
::v-deep .el-table tbody tr:hover > td {
  background: transparent !important; //修改成自己想要的颜色即可
}

::v-deep .el-table--striped .el-table__body tr.el-table__row--striped td {
  background: #f7f7f7 !important;
}

::v-deep .el-dialog__wrapper .el-dialog__header span {
  color: #333 !important;
}
::v-deep .el-button--info {
  background-color: #f4f4f5;
}
::v-deep .el-button--default {
  background-color: #f4f4f5;
}
</style>

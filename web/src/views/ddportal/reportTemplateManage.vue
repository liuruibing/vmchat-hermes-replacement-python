<template>
  <div class="DiReportTemplateManage">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form :inline="true" ref="formInline" :model="formInline" :rules="searchRules" style="margin-bottom: 8px" class="standard-form">
          <el-form-item label="模板名称" prop="vcTemplatEname">
            <el-input v-model.trim="formInline.vcTemplatEname" clearable placeholder="请输入" size="small"></el-input>
          </el-form-item>
          <el-form-item label="模板类型" prop="fFileType">
            <el-select v-model="formInline.fFileType" size="small" placeholder="请选择" @change="handleSelect">
              <el-option v-for="(group, index) in fFileTypeArr" :value="group.dimCde" :key="index" :label="group.dimNme"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="组合类型" prop="fundTypes">
            <el-select multiple v-model="formInline.fundTypes" size="small" placeholder="请选择">
              <el-option v-for="(group, index) in fundTypeArr" :value="group.dimCde" :key="index" :label="group.dimNme"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="投资类型" prop="investTypes">
            <el-select multiple v-model="formInline.investTypes" size="small" placeholder="请选择">
              <el-option v-for="(group, index) in investTypeArr" :value="group.dimCde" :key="index" :label="group.dimNme"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="报告类型" prop="reportTypes">
            <el-select multiple v-model="formInline.reportTypes" size="small" placeholder="请选择">
              <el-option v-for="(group, index) in reportTypeArr" :value="group.dimCde" :key="index" :label="group.dimNme"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit('formInline', true)" style="margin-bottom: 5px" size="small">
              <i class="el-icon-search"></i>
              查询
            </el-button>
            <el-button type="info" plain @click="restForm('formInline')" style="margin-bottom: 5px" size="small">
              <i class="el-icon-refresh"></i>
              重置
            </el-button>
            <el-button type="info" plain @click="addData()" style="margin-bottom: 5px" size="small">
              <i class="el-icon-circle-plus-outline"></i>
              新增
            </el-button>
            <!-- <el-button type="primary" plain @click="modifierData()" style="margin-bottom: 5px; " size="small"><i class="el-icon-edit-outline"></i>编辑</el-button>   -->
          </el-form-item>
        </el-form>
      </div>
    </div>

    <div class="table-content" id="standard-table">
      <div id="standard-table-margin">
        <el-table
          ref="multipleTable"
          @selection-change="handleSelectionChange"
          :data="tableData"
          :default-sort="{ prop: 'vcTemplatEname', order: 'descending' }"
          :cell-style="{ height: '40px', fontSize: '14px' }"
          :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
          stripe
          @sort-change="handleSortChange"
          v-loading="tableLoading"
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
            prop="vcStatus"
            show-overflow-tooltip
            sortable="custom"
            :sort-orders="['ascending', 'descending']"
            label="模板状态"
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
              <span v-if="scope.row.vcTypeBus === '1'">普通模板</span>
              <span v-else-if="scope.row.vcTypeBus === '2'">VM拖拽模板</span>
              <span v-else-if="scope.row.vcTypeBus === '3'">固定Excel模板</span>
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
            prop="updateTime"
            show-overflow-tooltip
            sortable="custom"
            :sort-orders="['ascending', 'descending']"
            label="更新时间"
            min-width="100"
            algin="left"
            header-align="center"
          >
            <template slot-scope="scope">
              <span>{{ scope.row.updateTime | noDataFilter }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" min-width="200" align="center">
            <template slot-scope="scope">
              <span class="operate-btn table-operation">
                <el-button type="info" plain size="small" @click="editData(scope.row)">编辑</el-button>
                <el-button type="info" plain size="small" @click="delData(scope.row)">删除</el-button>
              </span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <Pagination :total="total" :page="pageNum" :limit="pageSize" @pagination="Pagination"></Pagination>

    <!-- 新增指标配置表 -->
    <el-dialog :title="countTitle" center :visible.sync="countDialog" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox" style="height: 850px; width: 820px">
          <el-form :inline="true" ref="formDialog" :model="formDialog" :rules="dialogRules" label-position="right">
            <el-form-item label="模板名称" prop="vcTemplatEname" class="mb20" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog.vcTemplatEname" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>
            <el-form-item label="模板类型" prop="fFileType" class="mb20" :label-width="formLabelWidth">
              <el-select v-model="formDialog.fFileType" size="small" placeholder="请选择" :disabled="isEdit">
                <el-option v-for="(group, index) in fFileTypeArr" :value="group.dimCde" :key="index" :label="group.dimNme"></el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="功能分类" prop="vcTypeBus" class="mb20" :label-width="formLabelWidth">
              <el-select v-model="formDialog.vcTypeBus" size="small" placeholder="请选择">
                <el-option v-for="(group, index) in vcTypeBusArr" :value="group.dimCde" :key="index" :label="group.dimNme"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="自定义分类" prop="vcTypeFreebus" class="mb20" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog.vcTypeFreebus" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>
            <el-form-item label="模板状态" prop="vcStatus" class="mb20" :label-width="formLabelWidth">
              <el-select v-model="formDialog.vcStatus" size="small" placeholder="请选择">
                <el-option v-for="(group, index) in vcStatusArr" :value="group.dimCde" :key="index" :label="group.dimNme"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="模板说明" prop="vcPormpt" class="mb20" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog.vcPormpt" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>
            <el-form-item label="组合类型" prop="fundTypes" class="mb20" :label-width="formLabelWidth">
              <el-select multiple v-model="formDialog.fundTypes" size="small" placeholder="请选择">
                <el-option v-for="(group, index) in fundTypeArr" :value="group.dimCde" :key="index" :label="group.dimNme"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="投资类型" prop="investTypes" class="mb20" :label-width="formLabelWidth">
              <el-select multiple v-model="formDialog.investTypes" size="small" placeholder="请选择">
                <el-option v-for="(group, index) in investTypeArr" :value="group.dimCde" :key="index" :label="group.dimNme"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="报告类型" prop="reportTypes" class="mb20" :label-width="formLabelWidth">
              <el-select multiple v-model="formDialog.reportTypes" size="small" placeholder="请选择">
                <el-option v-for="(group, index) in reportTypeArr" :value="group.dimCde" :key="index" :label="group.dimNme"></el-option>
              </el-select>
            </el-form-item>
            <br />
            <el-form-item label="模板地址" prop="vcTemplatePath" class="mb20" :label-width="formLabelWidth">
              <el-input type="textarea" :rows="1" placeholder="请输入内容" size="small" style="width: 746px !important" v-model="formDialog.vcTemplatePath"></el-input>
            </el-form-item>
            <el-form-item label="文件导出名称" prop="vcFileDownloadName" class="mb20" :label-width="formLabelWidth">
              <el-input type="textarea" :rows="1" placeholder="请输入内容" size="small" style="width: 746px !important" v-model="formDialog.vcFileDownloadName"></el-input>
            </el-form-item>
            <el-form-item label="文件导出路径" prop="vcFileDownloadPath" class="mb20" :label-width="formLabelWidth">
              <el-input type="textarea" :rows="1" placeholder="请输入内容" size="small" style="width: 746px !important" v-model="formDialog.vcFileDownloadPath"></el-input>
            </el-form-item>
            <el-form-item label="自定义导出接口" prop="vcExportInterface" class="mb20" :label-width="formLabelWidth">
              <el-input type="textarea" :rows="1" placeholder="请输入内容" size="small" style="width: 746px !important" v-model="formDialog.vcExportInterface"></el-input>
            </el-form-item>
            <el-form-item label="自定义参数" prop="vcParamSelf" class="mb20" :label-width="formLabelWidth">
              <el-input type="textarea" :rows="2" placeholder="请输入内容" size="small" style="width: 746px !important" v-model="formDialog.vcParamSelf"></el-input>
            </el-form-item>
            <el-form-item label="备注" prop="vcRemark" class="mb20" :label-width="formLabelWidth">
              <el-input type="textarea" :rows="2" placeholder="请输入内容" size="small" style="width: 746px !important" v-model="formDialog.vcRemark"></el-input>
            </el-form-item>
          </el-form>
          <el-row>
            <el-col :span="2" :offset="22">
              <el-button type="primary" :loading="countSubmitLoading" size="small" @click="countSubmit('formDialog')">保存</el-button>
            </el-col>
          </el-row>
          <br />

          <el-row>
            <el-col :span="2" :offset="21">
              <el-button type="primary" :loading="countLoading" size="small" @click="sqlAdd('formDialog')">添加关联SQL</el-button>
            </el-col>
          </el-row>
          <div style="vertical-align: middle; display: inline-block">
            <div class="color-box"></div>
          </div>
          <span class="title-style">关联的指标配置列表</span>
          <br />
          <el-table
            ref="multipleTable"
            @selection-change="handleSelectionChange"
            :data="tableSqlData"
            :default-sort="{ prop: 'vcIndexName', order: 'descending' }"
            :cell-style="{ height: '40px', fontSize: '14px' }"
            :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
            stripe
            @sort-change="handleSortChange"
            v-loading="tableSqlLoading"
            style="width: 100%"
          >
            <el-table-column align="center" type="selection" width="35"></el-table-column>

            <el-table-column
              prop="vcIndexName"
              show-overflow-tooltip
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              label="指标名称"
              min-width="150"
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

            <el-table-column label="操作" min-width="200" align="center">
              <template slot-scope="scope">
                <div class="standard-form">
                  <el-button type="danger" plain size="small" @click="deleteTemplateData(scope.row)">删除</el-button>
                </div>
              </template>
            </el-table-column>
          </el-table>
          <Pagination :total="totalDetail" :page="pageNumDetail" :limit="pageSizeDetail" @pagination="PaginationDetail"></Pagination>
        </el-main>
      </el-container>
    </el-dialog>

    <el-dialog v-dialogDrag :title="previewTitle" center :visible.sync="previewDialog" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox" style="height: 200px; width: 200px"></el-main>
      </el-container>
    </el-dialog>
    <!-- 导入添加关联SQL组件 -->
    <associated-index :fTemplateID="formDialog.fTemplateID" :repDialog="repDialog" :repTitle="repTitle" @sqlAddClick="sqlAddClick"></associated-index>
  </div>
</template>

<script>
import { FILE_URL } from '@/utils/request'
import pageApi from '@/api/dataImport/reportTemplateManage.js'
import Pagination from '@/components/Pagination'
import AssociatedIndex from './components/associatedIndex'

import commonFun from '@/filters/common.js'

export default {
  name: 'DdReportTemplateManage',
  // 注册导入组件
  components: { Pagination, AssociatedIndex },
  data() {
    return {
      // 记录是否是编辑状态
      isEdit: false,
      formInline: {
        // 模板名称
        vcTemplatEname: '',
        // 模板类型
        fFileType: '',
        // 上传文件
        excelFile: '',
        // 文件
        file: '',
        // 组合类型
        fundTypes: [],
        // 投资类型
        investTypes: [],
        // 报告类型
        reportTypes: [],
        orderStr: 'vcTemplatEname desc nulls last', //列表排序
        limit: 10, // 条数
        offset: 0
      },
      pageSize: 10,
      pageNum: 1,
      searchRules: {},
      // 上传地址
      fileUrl: '',
      // 上传头部
      headersParams: {},
      // 文件列表
      fileList: [],
      // 校验大类数组
      vcRuleCodeFormArr: [],
      // 数据源数组
      vcSourceFormArr: [],
      searchDate: [], //时间
      // 优先级数组
      priorityLevelArr: [],
      // 启用日
      vcIsTradedateArr: [],
      tableData: [], //关联Sql表格数据
      tableSqlData: [], //表格数据
      tableLoading: false, //表格加载
      tableSqlLoading: false, //关联Sql表格加载
      total: 0, //总条数
      tableMultipleSelection: [], //表格选择数据集合
      orderByString: 'sqlName desc nulls last', //排序字段

      countDialog: false, // 弹窗
      // 指标预览弹框显示隐藏
      previewDialog: false,
      formDialog_date_show: true,
      indexDialog: 0, //查看关联指标弹窗
      repDialog: 0, //添加关联SQL弹窗
      indexTitle: '', //添加关联SQL标题
      repTitle: '', //查看关联指标标题
      countTitle: '', // 新增编辑标题
      previewTitle: '', // 指标预览标题
      countFormList: '', //是新增还是编辑
      // 新增 编辑计算任务
      formDialog: {
        fTemplateID: '',
        // 模板名称
        vcTemplatEname: '',
        // 模板类型
        fFileType: '',
        // 功能分类
        vcTypeBus: '',
        // 自定义分类
        vcTypeFreebus: '',
        // 模板状态
        vcStatus: '',
        // 模板说明
        vcPormpt: '',
        // 组合类型
        fundTypes: [],
        // 投资类型
        investTypes: [],
        // 报告类型
        reportTypes: [],
        vcParamSelf: '',
        // 模板地址
        vcTemplatePath: '',
        // 备注说明
        vcRemark: '',
        vcFileDownloadName: '',
        vcFileDownloadPath: '',
        vcExportInterface: ''
      },
      vcId: '', // 编辑修改时记录的id

      // 弹窗验证规则
      dialogRules: {
        // 模板名称
        vcTemplatEname: [
          {
            required: true,
            type: 'string',
            message: '请输入检验表名',
            trigger: 'change'
          }
        ],
        // 模板类型
        fFileType: [
          {
            type: 'string',
            required: true,
            message: '请输入校验说明',
            trigger: 'change'
          }
        ]
      },
      countSubmitLoading: false, //弹框提交保存延迟
      countLoading: false, //弹框提交添加关联SQL延迟
      submitLoading: false,
      formLabelWidth: '120px',
      vcTypeBusArr: [
        { dimCde: '1', dimNme: '普通模板' },
        { dimCde: '2', dimNme: 'VM拖拽模板' },
        { dimCde: '3', dimNme: '固定Excel模板' }
      ],
      fFileTypeArr: [
        { dimCde: '1', dimNme: 'Excel模板' },
        { dimCde: '2', dimNme: 'Word模板' },
        { dimCde: '3', dimNme: 'VM模板' },
        { dimCde: '4', dimNme: 'XML模板' },
        { dimCde: '5', dimNme: 'TXT模板' },
        { dimCde: '6', dimNme: 'XBRL模板' }
      ],
      vcStatusArr: [
        { dimCde: '1', dimNme: '启用' },
        { dimCde: '0', dimNme: '禁用' }
      ],
      fundTypeArr: [], //组合类型
      investTypeArr: [], //投资类型
      reportTypeArr: [], //报告类型
      //详情列表查询条件
      formInlineDetail: {
        fTemplateID: '',
        limit: 10, // 条数
        offset: 0
      },
      pageSizeDetail: 10, //详情列表分页信息
      pageNumDetail: 1,
      totalDetail: 0
    }
  },
  mounted() {
    //获取字典
    this.getEdims('fund_type')
    this.getEdims('invest_type')
    this.getEdims('report_type')
    //获取完token之后再请求列表信息
    this.onSubmit('formInline', true)
    // 上传地址
    this.fileUrl = FILE_URL + `/api/performance-overview/v1.0/upload-file?taskCode=${this.formInline.excelFile}`
    this.headersParams = {
      Authorization: this.$store.getters.token
    }
  },
  methods: {
    // 日期快捷选项
    dateShortDot() {
      return commonFun.yyyyMMdddateShortDot()
    },
    //列表点击排序
    handleSortChange(val) {
      this.formInline.orderStr = commonFun.orderByString(val)
      this.onSubmit('formInline', false)
    },
    //分页
    Pagination(val) {
      this.pageSize = val.limit //页面条数
      this.pageNum = val.page //页面
      this.formInline.offset = (val.page - 1) * val.limit
      this.formInline.limit = val.limit // 页面条数
      this.onSubmit('formInline', false)
    },
    //分页
    PaginationDetail(val) {
      this.pageSizeDetail = val.limit //页面条数
      this.pageNumDetail = val.page //页面
      this.formInlineDetail.offset = (val.page - 1) * val.limit
      this.formInlineDetail.limit = val.limit // 页面条数
      this.getDetail('false')
    },
    // 日期快捷选项
    dateShortcut() {
      return commonFun.dateShortcut()
    },

    // table批量选择结果
    handleSelectionChange(val) {
      this.tableMultipleSelection = val
    },

    // 上传文件下拉框选择
    handleSelect() {
      if (this.formInline.excelFile) {
        this.fileUrl = FILE_URL + `/api/performance-overview/v1.0/upload-file?taskCode=${this.formInline.excelFile}`
      }
    },
    // 上传文件之前的钩子
    beforeUpload(file) {
      if (!this.formInline.excelFile) {
        this.$message({
          message: '请选择文件类型',
          type: 'warning'
        })
        return false
      }
      if (file.size > 10 * 1024 * 1024) {
        this.$message({
          message: '请上传小于10M的文件',
          type: 'warning'
        })
        return false
      }
    },
    // 文件上传成功时的钩子
    handleSuccess(res, file, fileList) {
      let { status, data } = res
      if (status === 0) {
        this.$message({
          message: '文件上传成功',
          type: 'success'
        })
        this.onSubmit()
        // setTimeout(()=>{
        // 	this.$refs.upload.clearFiles()
        // },3000)
      }
    },
    // 文件上传失败时的钩子
    handleError() {
      this.$message.error('文件上传失败')
    },
    // 当表格的排序条件发生变化的时候会触发该事件
    handleSortChange(val) {
      this.formQuery.orderBy = this.$fun.queryOrderBy(val)
      // 查询
      this.onSubmit()
    },
    // 查询报告模板列表
    onSubmit(formName, pageNumOne) {
      var self = this

      if (pageNumOne === true) {
        this.formInline.offset = 0 //重新搜索初始页面为首页
        this.pageNum = 1 //重新搜索初始页面为首页
      } else {
      }
      // 消除没有值的参数
      let params = commonFun.parameterSrc(this.formInline)
      // 表格加载显示
      this.tableLoading = true
      pageApi
        .getIndParaThemeList(params)
        .then((response) => {
          if (!response.data.error) {
            this.tableData = response.data.rows
            // 页面总条数
            this.total = response.data.total
          } else {
            this.tableData = []
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
          this.tableData = []
          this.tableSqlData = []
          this.total = 0
          this.pageSize = 10
          this.pageNum = 1
          this.formInline.offset = 0
          this.formInline.limit = 10 // 页面条数
        })
    },

    //新增数据
    addData() {
      this.countTitle = '新增模板' // 标题设置
      this.countFormList = 'add' // 新增标识
      this.isEdit = false
      //获取id
      pageApi
        .getId()
        .then((response) => {
          if (!response.data.error) {
            this.countDialog = true // 显示弹框
            this.activeName = 'first' // 默认显示基础信息
            this.$nextTick(() => {
              this.$refs['formDialog'].resetFields()
              this.formDialog.fTemplateID = response.data.data
              this.formDialog.vcStatus = '1'
              this.formDialog.vcTypeBus = '1'
              // 清空关联的指标配置列表数据和总条数
              this.tableSqlData = []
              this.totalDetail = 0
            })
          } else {
            this.$message.closeAll()
            this.$message({
              message: '获取模板id失败',
              type: 'warning'
            })
          }
        })
        .catch(() => {
          this.$message.closeAll()
          this.$message({
            message: '获取模板id失败',
            type: 'warning'
          })
        })
    },
    //新增 、 编辑确认
    countSubmit(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if (this.countFormList == 'add') {
            this.addSubmit()
          } else {
            this.modifierSubmit()
          }
        } else {
          return false
        }
      })
    },
    // 新增确认
    addSubmit() {
      this.$confirm('确定保存?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          // 提交延迟
          this.countSubmitLoading = true
          // 消除没有值的参数
          let params = commonFun.parameterSrc(this.formDialog)
          pageApi
            .postIndParaThemeAdd(params)
            .then((response) => {
              if (!response.data.error) {
                // 提交延迟
                this.countSubmitLoading = false
                this.countDialog = false // 关闭弹框
                this.$message.closeAll()
                this.$message({
                  message: '新增成功',
                  type: 'success'
                })
                // 刷新列表
                this.onSubmit('formInline', false)
              } else {
                // 提交延迟
                this.countSubmitLoading = false
                this.countDialog = false // 关闭弹框
                this.$message.closeAll()
                this.$message({
                  message: '新增失败',
                  type: 'warning'
                })
              }
            })
            .catch(() => {
              // 提交延迟
              this.countSubmitLoading = false
              this.countDialog = false // 关闭弹框
              this.$message.closeAll()
              this.$message({
                message: '新增失败',
                type: 'warning'
              })
            })
        })
        .catch(() => {})
    },
    //修改数据
    modifierData() {
      if (this.tableMultipleSelection.length === 0) {
        this.$message.closeAll()
        this.$message({
          message: '请选择要修改的数据',
          type: 'warning'
        })
      } else if (this.tableMultipleSelection.length > 1) {
        this.$message.closeAll()
        this.$message({
          message: '只能选择一行数据',
          type: 'warning'
        })
      } else {
        this.editData(this.tableMultipleSelection[0])
      }
    },

    // 行编辑数据
    editData(row) {
      this.countTitle = '编辑指标配置表'
      this.countFormList = 'edit'
      this.countDialog = true
      this.isEdit = true
      let params = {}
      params.fTemplateID = row.fTemplateID
      pageApi
        .getDetail(params)
        .then((response) => {
          if (!response.data.error) {
            this.countDialog = true
            this.$nextTick(() => {
              // 清除
              this.$refs['formDialog'].resetFields()
              let formData = response.data.data
              // 赋值
              if (formData.fTemplateID) {
                this.vcId = formData.fTemplateID
                this.formDialog.fTemplateID = formData.fTemplateID
              } // 行id
              if (formData.vcTemplatEname) {
                this.formDialog.vcTemplatEname = formData.vcTemplatEname
              } //业务表英文表名
              if (formData.fFileType) {
                this.formDialog.fFileType = formData.fFileType
              } //业务表中文名称
              if (formData.vcTypeBus) {
                this.formDialog.vcTypeBus = formData.vcTypeBus
              } //业务表类型
              if (formData.vcTypeFreebus) {
                this.formDialog.vcTypeFreebus = formData.vcTypeFreebus
              } //业务表英文表名
              if (formData.vcStatus) {
                this.formDialog.vcStatus = formData.vcStatus
              } //是否有效
              if (formData.vcPormpt) {
                this.formDialog.vcPormpt = formData.vcPormpt
              } //是否有效
              if (formData.fundTypes) {
                this.formDialog.fundTypes = formData.fundTypes
              } //是否有效
              if (formData.investTypes) {
                this.formDialog.investTypes = formData.investTypes
              } //是否有效
              if (formData.reportTypes) {
                this.formDialog.reportTypes = formData.reportTypes
              } //是否有效
              if (formData.vcTemplatePath) {
                this.formDialog.vcTemplatePath = formData.vcTemplatePath
              } //是否有效
              if (formData.vcRemark) {
                this.formDialog.vcRemark = formData.vcRemark
              } //是否有效

              if (formData.vcParamSelf) {
                this.formDialog.vcParamSelf = formData.vcParamSelf
              } //是否有效

              if (formData.vcExportInterface) {
                this.formDialog.vcExportInterface = formData.vcExportInterface
              } //是否有效
              if (formData.vcFileDownloadPath) {
                this.formDialog.vcFileDownloadPath = formData.vcFileDownloadPath
              } //是否有效
              if (formData.vcFileDownloadName) {
                this.formDialog.vcFileDownloadName = formData.vcFileDownloadName
              } //是否有效
            })
            this.getDetail(row)
          } else {
            this.$message.closeAll()
            this.$message({
              message: '获取详情数据失败',
              type: 'warning'
            })
          }
        })
        .catch(() => {
          this.$message.closeAll()
          this.$message({
            message: '获取详情数据失败',
            type: 'warning'
          })
        })
    },
    //获取详情列表数据
    getDetail(row) {
      let params = {}
      if (row === 'false') {
      } else {
        this.formInlineDetail.fTemplateID = row.fTemplateID
        this.formInlineDetail.limit = 10
        this.formInlineDetail.limit = 0
      }

      params = commonFun.parameterSrc(this.formInlineDetail)
      pageApi
        .getDetailTable(params)
        .then((response) => {
          if (response.data.rows) {
            this.tableSqlData = response.data.rows
            this.totalDetail = response.data.total
          } else {
            this.$message.closeAll()
            this.$message({
              message: '获取关联的指标数据失败',
              type: 'warning'
            })
            this.tableSqlData = []
            this.totalDetail = 0
          }
        })
        .catch(() => {
          this.$message.closeAll()
          this.$message({
            message: '获取关联的指标数据失败',
            type: 'warning'
          })
          this.tableSqlData = []
          this.totalDetail = 0
        })
    },
    // 编辑确认
    modifierSubmit() {
      this.$confirm('确定修改?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          // 提交延迟
          this.countSubmitLoading = true
          // 消除没有值的参数
          let params = commonFun.parameterSrc(this.formDialog)
          pageApi
            .postIndParaThemeEdit(params)
            .then((response) => {
              if (!response.data.error) {
                // 提交延迟
                this.countSubmitLoading = false
                this.countDialog = false // 关闭弹框
                this.$message.closeAll()
                this.$message({
                  message: '修改成功',
                  type: 'success'
                })
                // 刷新列表
                this.onSubmit('formInline', false)
              } else {
                // 提交延迟
                this.countSubmitLoading = false
                this.countDialog = false // 关闭弹框
                this.$message.closeAll()
                this.$message({
                  message: '修改失败',
                  type: 'warning'
                })
              }
            })
            .catch(() => {
              // 提交延迟
              this.countSubmitLoading = false
              this.countDialog = false // 关闭弹框
              this.$message.closeAll()
              this.$message({
                message: '修改失败',
                type: 'warning'
              })
            })
        })
        .catch(() => {})
    },
    // 查看关联的指标按钮绑定的方法
    viewData(row) {
      this.indexTitle = '指标关联的模板列表'
      this.indexDialog++
      // console.log( this.indexDialog);
    },
    // 指标预览绑定的方法
    previewData(row) {
      this.previewDialog = true
      this.previewTitle = '指标预览'
    },
    sqlAdd(formInline) {
      this.repTitle = '新增模板关联指标配置'
      this.repDialog++
    },
    // 按钮批量删除
    deleteData() {
      if (this.tableMultipleSelection.length === 0) {
        this.$message.closeAll()
        this.$message({
          message: '请选择要删除的数据',
          type: 'warning'
        })
      } else {
        this.delData(this.tableMultipleSelection)
      }
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
          params['templateCode'] = row.fTemplateID
          pageApi
            .postIndParaThemeDel(params)
            .then((response) => {
              if (response.data.status === 200) {
                this.$message.closeAll()
                this.$message({
                  message: '删除成功',
                  type: 'success'
                })
                // 刷新列表
                this.onSubmit('formInline', false)
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
    },
    deleteTemplateData(row) {
      this.$confirm('确定删除?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          let params = {}
          params['indexCode'] = row.vcCode
          params['fTemplateID'] = this.formDialog.fTemplateID
          pageApi
            .deleteTemplateData(params)
            .then((response) => {
              if (response.data.status === 200) {
                this.$message.closeAll()
                this.$message({
                  message: '删除成功',
                  type: 'success'
                })
                // 刷新列表
                this.getDetail('false')
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
    restForm(formName) {
      var self = this
      self.$refs[formName].resetFields()
    },
    //获取字典数据
    getEdims(type) {
      let params = {}
      params.dimType = type
      pageApi
        .getEdims(params)
        .then((response) => {
          if (!response.data.error) {
            if (type === 'fund_type') {
              this.fundTypeArr = response.data.data
            }
            if (type === 'invest_type') {
              this.investTypeArr = response.data.data
            }
            if (type === 'report_type') {
              this.reportTypeArr = response.data.data
            }
          }
        })
        .catch(() => {})
    },
    //回调函数
    sqlAddClick(data) {
      this.getDetail(data)
    }
  }
}
</script>

<style lang="scss" scoped>
.DiReportTemplateManage {
  // padding-left: 10px;
  .title-style {
    color: #0f65dd;
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
    background-color: #0f65dd;
  }
  .el-dialog {
    width: 65% !important;

    .el-form {
      width: 100% !important;
      font-size: 0;
    }

    .el-form-item {
      min-width: 33.3%;
      margin-right: 0;
      margin-bottom: 10px !important;
    }

    .mr5 {
      margin-right: 5px;
    }
  }

  .mb20 {
    margin-bottom: 20px;
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
  background-color: transparent !important; //修改成自己想要的颜色即可
}

::v-deep .el-table--striped .el-table__body tr.el-table__row--striped td {
  background: #f7f7f7 !important;
}

::v-deep .el-button.el-button--info {
  color: #333;
  background-color: #dddddd;
  border-color: #dddddd;
}

::v-deep .el-dialog__wrapper .el-dialog__header span {
  color: #333 !important;
}
</style>

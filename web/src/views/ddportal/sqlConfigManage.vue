<template>
  <div class="DiSqlConfigManage">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form :inline="true" ref="formInline" :model="formInline" :rules="searchRules" style="margin-bottom: 8px" class="standard-form">
          <el-form-item label="SQL名称" prop="sqlName">
            <el-input v-model.trim="formInline.sqlName" clearable placeholder="请输入" size="small"></el-input>
          </el-form-item>
          <el-form-item label="SQL编码" prop="sqlCode">
            <el-input v-model.trim="formInline.sqlCode" clearable placeholder="请输入" size="small"></el-input>
          </el-form-item>
          <el-form-item label="执行方式" prop="sqlOperate">
            <el-select v-model="formInline.sqlOperate" size="small" placeholder="请选择">
              <el-option v-for="(group, index) in sqlOperateArr" :value="group.dimCde" :key="index" :label="group.dimNme"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item class="">
            <el-button type="primary" @click="onSubmit('formInline', true)" style="margin-bottom: 5px" size="small">
              <i class="el-icon-search"></i>
              查询
            </el-button>
            <!-- <el-button type="primary" plain @click="modifierData()" style="margin-bottom: 5px; " size="small"><i class="el-icon-edit-outline"></i>编辑</el-button>   -->
            <el-button type="info" plain @click="restForm('formInline')" style="margin-bottom: 5px" size="small">
              <i class="el-icon-refresh"></i>
              重置
            </el-button>
            <el-button type="info" plain @click="addData()" style="margin-bottom: 5px" size="small">
              <i class="el-icon-circle-plus-outline"></i>
              新增
            </el-button>
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
          :default-sort="{ prop: 'vcCheckCode', order: 'descending' }"
          :cell-style="{ height: '40px', fontSize: '14px' }"
          :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
          stripe
          @sort-change="handleSortChange"
          v-loading="tableLoading"
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
            prop="sqlStatus"
            show-overflow-tooltip
            sortable="custom"
            :sort-orders="['ascending', 'descending']"
            label="状态"
            min-width="100"
            algin="left"
            header-align="center"
          >
            <template slot-scope="scope">
              <span v-if="scope.row.sqlStatus === '1'">启用</span>
              <span v-else-if="scope.row.sqlStatus === '0'">禁用</span>
              <span v-else>{{ scope.row.sqlStatus | noDataFilter }}</span>
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
            min-width="80"
            algin="left"
            header-align="center"
          >
            <template slot-scope="scope">
              <span>{{ scope.row.dUpdateTime | noDataFilter }}</span>
            </template>
          </el-table-column>

          <el-table-column label="操作" min-width="180" align="center">
            <template slot-scope="scope">
              <span class="operate-btn table-operation">
                <el-button type="info" plain size="small" @click="editData(scope.row)">编辑</el-button>
                <el-button type="info" plain size="small" @click="delData(scope.row)">删除</el-button>
                <el-button type="info" plain size="small" @click="viewData(scope.row)">查看关联的指标</el-button>
              </span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <Pagination :total="total" :page="pageNum" :limit="pageSize" @pagination="Pagination"></Pagination>

    <!-- 新增Sql配置表 -->
    <el-dialog v-dialogDrag :title="countTitle" center :visible.sync="countDialog" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox" style="height: 600px; width: 800px">
          <el-form :inline="true" ref="formDialog" :model="formDialog" :rules="dialogRules" label-position="right">
            <el-form-item label="SQL编码" prop="sqlCode" class="mb20" :label-width="formLabelWidth">
              <el-input disabled v-model.trim="formDialog.sqlCode" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>
            <el-form-item label="SQL名称" prop="sqlName" class="mb20" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog.sqlName" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>

            <el-form-item label="执行方式" prop="sqlOperate" class="mb20" :label-width="formLabelWidth">
              <el-select v-model="formDialog.sqlOperate" size="small" placeholder="请选择" @change="handleMisTypChange(formDialog.sqlOperate)">
                <el-option v-for="(group, index) in sqlOperateArr" :value="group.dimCde" :key="index" :label="group.dimNme"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="SQl状态" prop="sqlStatus" class="mb20" :label-width="formLabelWidth">
              <el-select v-model="formDialog.sqlStatus" size="small" placeholder="请选择">
                <el-option v-for="(group, index) in sqlStatusArr" :value="group.dimCde" :key="index" :label="group.dimNme"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="数据源" prop="sourceCode" class="mb20" :label-width="formLabelWidth">
              <el-select v-model="formDialog.sourceCode" size="small" placeholder="请选择" :disabled="sourceStatus">
                <el-option v-for="(group, index) in sourceCodeArr" :value="group.dimCde" :key="index" :label="group.dimNme"></el-option>
              </el-select>
            </el-form-item>
            <br />
            <el-form-item label="BO类" prop="sqlBo" class="mb20" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog.sqlBo" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>
            <el-form-item label="SQL配置" prop="sqlSet" class="mb20 ddCode-mirror-form" :label-width="formLabelWidth">
              <!-- <el-input
                type="textarea"
                :rows="3"
                placeholder="请输入内容"
                size="small"
                style="width:730px!important;"
                v-model="formDialog.sqlSet">
              </el-input> -->
              {{ '调用计算引擎:' }}
              <el-switch v-model="sqlSwitch" active-color="#13ce66" inactive-color="#ff4949"></el-switch>
              <template v-if="sqlSwitch">
                <el-button @click="handleSelectInfo" type="primary" size="mini" style="margin-left: 10px">查看提示</el-button>
                <el-button @click="handleInsertTemp" type="primary" size="mini">插入模板</el-button>
              </template>
              <dd-code-mirror :label-width="formLabelWidth" ref="SqlContentMirror" language="x-sql" style="width: 90%" @codeChange="sqlContentMirrorChange"></dd-code-mirror>
            </el-form-item>
            <el-form-item label="测试SQL" prop="sqlTest" class="mb20 ddCode-mirror-form" :label-width="formLabelWidth">
              <!-- <el-input
                type="textarea"
                :rows="3"
                placeholder="请输入内容"
                size="small"
                style="width:730px!important;"
                v-model="formDialog.sqlTest">
              </el-input> -->
              <dd-code-mirror :label-width="formLabelWidth" ref="SqlTestMirror" language="x-sql" style="width: 90%" @codeChange="sqlTestMirrorChange"></dd-code-mirror>
            </el-form-item>
            <el-form-item label="测试数据" prop="testSqlData" class="mb20 ddCode-mirror-form" :label-width="formLabelWidth">
              <!-- <el-input
                type="textarea"
                :rows="3"
                placeholder="请输入内容"
                size="small"
                style="width:730px!important;"
                v-model="formDialog.testSqlData">
              </el-input> -->
              <dd-code-mirror :label-width="formLabelWidth" ref="TestSqlDataMirror" scriptLanguage="json" style="width: 90%" @codeChange="TestSqlDataMirrorChange"></dd-code-mirror>
            </el-form-item>
            <el-form-item label="Json过滤" prop="jsonField" class="mb20" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog.jsonField" placeholder="请输入Json过滤" style="width: 730px !important" size="small"></el-input>
            </el-form-item>
            <el-form-item label="脱敏字段" prop="desensitizationSqlColumns" class="mb20" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog.desensitizationSqlColumns" placeholder="请输入脱敏字段" style="width: 730px !important" size="small"></el-input>
            </el-form-item>
            <el-form-item label="备注说明" prop="vcRemark" class="mb20" :label-width="formLabelWidth">
              <el-input type="textarea" :rows="3" placeholder="请输入内容" size="small" style="width: 730px !important" v-model="formDialog.vcRemark"></el-input>
            </el-form-item>
            <el-row type="flex" class="row-bg" justify="end">
              <el-col :span="8">
                <el-form-item label="条数选择" prop="vcRows" class="mb20" :label-width="formLabelWidth">
                  <el-select v-model="formDialog.vcRows" size="small" placeholder="请选择">
                    <el-option v-for="(group, index) in vcRowsArr" :value="group.dimCde" :key="index" :label="group.dimNme"></el-option>
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="4">
                <el-button type="primary" :loading="submitLoading" @click="testSql()" size="small" style="width: 120px; margin-top: 6px">执行测试SQL</el-button>
              </el-col>
              <el-col :span="3" style="margin-top: 6px">
                <el-button type="primary" size="small" @click="countSubmit('formDialog')">确 定</el-button>
              </el-col>
            </el-row>
          </el-form>
          <div v-show="testSqlShow">
            <div class="forms_table_title">
              <i class="el-icon-s-data"></i>
              测试SQL数据列表
            </div>

            <el-table
              ref="testSqlTable"
              :data="testSqlTableData"
              :cell-style="{ height: '40px', fontSize: '14px' }"
              :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
              stripe
              v-loading="testSqlTableLoading"
              style="width: 100%"
            >
              <el-table-column prop="sqlName" show-overflow-tooltip label="SQL名称" min-width="120" algin="left" header-align="center">
                <template slot-scope="scope">
                  <span>{{ scope.row.sqlName | noDataFilter }}</span>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-main>
      </el-container>
    </el-dialog>
    <!-- 导入查看关联指标弹框组件 -->
    <index-list :sqlCode="sqlCode" :indexDialog="indexDialog" :indexTitle="indexTitle"></index-list>
  </div>
</template>

<script>
import pageApi from '@/api/dataImport/sqlConfigManage.js'
import Pagination from '@/components/Pagination'
import IndexList from './components/sqlList'

import commonFun from '@/filters/common.js'

export default {
  name: 'DdSqlConfigManage',
  // 注册导入组件
  components: { Pagination, IndexList },

  data() {
    return {
      sourceStatus: false,
      sqlSwitch: false, //滑块状态
      formInline: {
        // SQL名称
        sqlName: '',
        // SQL编码
        sqlCode: '',
        // 执行方式
        sqlOperate: '',
        orderString: 'dUpdateTime desc', //列表排序
        limit: 10, // 条数
        offset: 0
      },
      pageSize: 10,
      pageNum: 1,
      searchRules: {},
      // 校验大类数组
      vcRuleCodeFormArr: [],
      // 数据源数组
      vcSourceFormArr: [],
      searchDate: [], //时间
      // 优先级数组
      priorityLevelArr: [],
      // 启用日
      vcIsTradedateArr: [],
      tableData: [], //表格数据
      tableLoading: false, //表格加载
      total: 0, //总条数
      tableMultipleSelection: [], //表格选择数据集合
      orderByString: 'sqlName desc nulls last', //排序字段
      isSelectInfo: false,
      countDialog: false, // 弹窗
      formDialog_date_show: true,
      indexDialog: 0, //查看关联指标弹窗
      indexTitle: '',
      countTitle: '', //标题
      countFormList: '', //是新增还是编辑
      // 新增 编辑计算任务
      formDialog: {
        // SQL编码
        sqlCode: '',
        // SQL名称
        sqlName: '',
        // 执行方式
        sqlOperate: '',
        // SQL状态
        sqlStatus: '',
        // 数据源
        sourceCode: '',
        // BO类
        sqlBo: '',
        // SQL配置
        sqlSet: '',
        // 测试SQL
        sqlTest: '',
        // 测试数据
        testSqlData: '',
        // 备注说明
        vcRemark: '',
        //日期过滤字段
        jsonField:'',
        //脱敏字段
        desensitizationSqlColumns:'',
        // 条数选择
        vcRows: ''
      },
      vcId: '', // 编辑修改时记录的id

      // 弹窗验证规则
      dialogRules: {
        // SQL编码
        sqlCode: [{ type: 'string', required: true, message: '请输入SQL编码', trigger: 'bulr' }],
        // SQL名称
        sqlName: [{ required: true, type: 'string', message: '请输入SQL名称', trigger: 'bulr' }],
        // 执行方式
        sqlOperate: [{ type: 'string', required: true, message: '请选择执行方式', trigger: 'change' }]
      },
      countSubmitLoading: false, //弹框提交延迟
      submitLoading: false,
      formLabelWidth: '120px',
      testSqlShow: false,
      testSqlTableData: [],
      testSqlTableLoading: false,
      sqlOperateArr: [
        { dimCde: '1', dimNme: 'SQL' },
        { dimCde: '2', dimNme: 'BO' },
        { dimCde: '3', dimNme: 'SQL+BO' },
        { dimCde: '4', dimNme: '远程JSON数据' },
        { dimCde: '9', dimNme: '远程JSON数据+BO' },
        { dimCde: '6', dimNme: 'SPL' },
        { dimCde: '10', dimNme: 'SPL+BO' }
      ],
      sqlStatusArr: [
        { dimCde: '1', dimNme: '启用' },
        { dimCde: '0', dimNme: '禁用' }
      ],
      sourceCodeArr: [],
      vcRowsArr: [
        { dimCde: '10', dimNme: '10' },
        { dimCde: '20', dimNme: '20' },
        { dimCde: '50', dimNme: '50' },
        { dimCde: '100', dimNme: '100' },
        { dimCde: '200', dimNme: '200' },
      ],
      sqlCode: ''
    }
  },

  mounted() {
    this.getSource()
    this.onSubmit('formInline', true)
  },
  methods: {
    handleMisTypChange(val) {
      this.formDialog.sourceCode = ''
      if (val === '6' || val === '10') {
        this.getSPLSourceList()
      } else {
        this.getSource()
      }
    },
    handleInsertTemp() {
      let str = this.$refs.SqlContentMirror.getValue()
      str += `
<!--
<alg>
{
	"caliberCode":"fundIndexService_1_basic",
	"matchKey":"fundCode",
	"dataMap":{
		 "netGrowthRate":"#data['algResult']['netGrowthRate']"
	}
}
</alg>
-->`
      this.$refs.SqlContentMirror.appendValue(str)
    },
    handleSelectInfo() {
      const confirmText = [
        'caliberCode：口径编码，在计算管理平台中配置（为不同口径提供的默认参数）',
        'matchKey：匹配字段，计算引擎返回的json数据与sql查看数据的匹配列的列名',
        'dataMap：用于指定数据映射关系，即指定期望从计算结果中增加哪些属性到sql查询结果中，采用键值对的配置方式，值为springEL表达式，通过表达式对json对象进行解析处理'
      ]
      const newDatas = []
      const h = this.$createElement
      for (const i in confirmText) {
        newDatas.push(h('p', null, confirmText[i]))
      }
      this.$confirm('提示', {
        title: '提示',
        message: h('div', null, newDatas),
        showCancelButton: false,
        confirmButtonText: '确定'
      })
    },
    sqlContentMirrorChange(val) {
      this.formDialog.sqlSet = val
    },
    sqlTestMirrorChange(val) {
      this.formDialog.sqlTest = val
    },
    TestSqlDataMirrorChange(val) {
      // if (this.formDialog && this.formDialog.testSqlData && val) {
        this.formDialog.testSqlData = val
      // }
    },
    // 日期快捷选项
    dateShortDot() {
      return commonFun.yyyyMMdddateShortDot()
    },
    //列表点击排序
    handleSortChange(val) {
      this.formInline.orderString = commonFun.orderByString(val)
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
    // 日期快捷选项
    dateShortcut() {
      return commonFun.dateShortcut()
    },

    //  radioChange(){
    //   let flag = this.formDialog.vcParameterType;
    //   if(flag){
    //     this.formDialog_date_show = false;
    //   }else{
    //     this.formDialog_date_show = true;
    //   }
    // },

    // table批量选择结果
    handleSelectionChange(val) {
      this.tableMultipleSelection = val
    },
    // 查询SQL配置表内容
    onSubmit(formName, pageNumOne) {
      var self = this
      self.$refs[formName].validate((valid) => {
        if (valid) {
          if (pageNumOne === true) {
            self.pageNum = 1 //重新搜索初始页面为首页
            self.formInline.offset = 0
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
              this.total = 0
              this.pageSize = 10
              this.pageNum = 1
              this.formInline.offset = 0
              this.formInline.limit = 10 // 页面条数
            })
        } else {
          return false
        }
      })
    },

    //新增数据
    addData() {
      this.countTitle = '新增SQL配置表' // 标题设置
      this.countFormList = 'add' // 新增标识
      //this.countDialog = true; // 显示弹框
      this.activeName = 'first' // 默认显示基础信息
      this.getAddId()
    },
    //新增-获取sql编码
    getAddId() {
      pageApi
        .getAddId()
        .then((response) => {
          if (response.data.status === 200) {
            // 提交延迟
            this.countDialog = true
            // 清除
            this.$nextTick(() => {
              this.$refs['formDialog'].resetFields()
              this.$refs.SqlContentMirror.operationVal('')
              this.$refs.SqlTestMirror.operationVal('')
              this.$refs.TestSqlDataMirror.operationVal('')
              this.sqlSwitch = false
              this.formDialog.sqlName = ''
              this.formDialog.sqlOperate = ''
              this.formDialog.sqlStatus = '1'
              this.formDialog.sourceCode = ''
              this.formDialog.sqlSet = ''
              this.formDialog.sqlBo = ''
              this.formDialog.testSqlData = ''
              this.formDialog.vcRemark = ''
              this.formDialog.jsonField=''
              this.formDialog.vcRows = '10'
              if (response.data.data) {
                this.formDialog.sqlCode = response.data.data
              }
              // 校验大类选择 默认选择第一个
              // this.formDialog.vcRuleCode = this.vcRuleCodeFormArr[0].dimCde;
            })
          } else {
            this.$message.closeAll()
            this.$message({
              message: '获取SQL编码失败',
              type: 'warning'
            })
          }
        })
        .catch(() => {
          // 提交延迟
          this.$message.closeAll()
          this.$message({
            message: '获取SQL编码失败',
            type: 'warning'
          })
        })
    },
    //新增 、 编辑SQl配置表确认
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
      this.$confirm('确定新增?', '提示', {
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
      this.countTitle = '编辑SQL配置表'
      this.countFormList = 'edit'
      let sqlCode = row.sqlCode
      this.isSelectInfo = false
      pageApi
        .getDetail(sqlCode)
        .then((response) => {
          if (!response.data.error) {
            let data = response.data.data
            if (data) {
              this.countDialog = true
              this.$nextTick(() => {
                // 清除
                this.$refs['formDialog'].resetFields()
                this.$refs.SqlContentMirror.operationVal('')
                this.$refs.SqlTestMirror.operationVal('')
                // this.$refs.TestSqlDataMirror.operationVal("");
                this.sqlSwitch = false
                this.formDialog.sqlCode = commonFun.abnormalityData(data.sqlCode)
                this.formDialog.sqlName = commonFun.abnormalityData(data.sqlName)
                this.formDialog.sqlOperate = commonFun.abnormalityData(data.sqlOperateCode)
                this.formDialog.sqlStatus = commonFun.abnormalityData(data.sqlStatus)
                this.formDialog.sourceCode = commonFun.abnormalityData(data.sourceCode)
                this.formDialog.jsonField = commonFun.abnormalityData(data.jsonField)
                this.formDialog.desensitizationSqlColumns = commonFun.abnormalityData(data.desensitizationSqlColumns)
                if (row.sqlOperateCode === '6' || row.sqlOperateCode === '10') {
                  this.getSPLSourceList()
                } else {
                  this.getSource()
                }
                this.formDialog.sqlSet = commonFun.abnormalityData(data.sqlSet)
                this.formDialog.sqlBo = commonFun.abnormalityData(data.sqlBo)
                this.formDialog.sqlTest = commonFun.abnormalityData(data.sqlTest)
                this.formDialog.testSqlData = commonFun.abnormalityData(data.testSqlData)
                if (this.formDialog.testSqlData) {
                  this.formDialog.testSqlData = JSON.parse(data.testSqlData)
                }
                this.formDialog.vcRemark = commonFun.abnormalityData(data.vcRemark)
                this.formDialog.vcRows = commonFun.abnormalityData(data.vcRows)
                this.vcId = data.fCreateID
                if (this.formDialog.sqlSet) {
                  this.$refs.SqlContentMirror.operationVal(this.formDialog.sqlSet)
                }
                if (this.formDialog.sqlTest) {
                  this.$refs.SqlTestMirror.operationVal(this.formDialog.sqlTest)
                }
                if (this.formDialog.testSqlData) {
                  this.$refs.TestSqlDataMirror.operationVal(this.formDialog.testSqlData)
                }
              })
            }
          } else {
          }
        })
        .catch(() => {})
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
          if (this.formDialog.testSqlData) {
            params.testSqlData = JSON.stringify(JSON.parse(this.formDialog.testSqlData))
          }
          params['fCreateID'] = this.vcId
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
    viewData(row) {
      this.indexTitle = '关联的指标列表'
      this.indexDialog++
      this.sqlCode = row.sqlCode
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
          params['sqlCode'] = row.sqlCode
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
    restForm(formName) {
      var self = this
      self.$refs[formName].resetFields()
    },
    getSource() {
      this.sourceStatus = true
      this.sourceCodeArr = []
      pageApi
        .getSource()
        .then((response) => {
          if (!response.data.error) {
            let data = response.data.data
            if (data && data.length > 0) {
              let arr = []
              for (let i = 0; i < data.length; i++) {
                let hh = data[i]
                let obj = {}
                obj.dimCde = hh[0]
                obj.dimNme = hh[1]
                arr.push(obj)
              }
              this.sourceCodeArr = arr
            }
            // 弹框状态
            this.sourceStatus = false
            //  this.formDialog.fStatus = this.fStatusArr[0].dimCde;
          } else {
            this.sourceStatus = false
          }
        })
        .catch(() => {
          this.sourceStatus = false
        })
    },
    getSPLSourceList() {
      this.sourceStatus = true
      this.sourceCodeArr = []
      pageApi
        .getSPLSourceList()
        .then((response) => {
          if (!response.data.error) {
            let data = response.data.data
            if (data && data.length > 0) {
              let arr = []
              for (let i = 0; i < data.length; i++) {
                let hh = data[i]
                let obj = {}
                obj.dimCde = hh[0]
                obj.dimNme = hh[1]
                arr.push(obj)
              }
              this.sourceCodeArr = arr
            }
            this.sourceStatus = false
            // 弹框状态

            //  this.formDialog.fStatus = this.fStatusArr[0].dimCde;
          } else {
            this.sourceStatus = false
          }
        })
        .catch(() => {
          this.sourceStatus = false
        })
    },
    testSql() {
      if (this.formDialog.sqlOperate == '6' || this.formDialog.sqlOperate == '10') {
        this.testSqlBySPL()
        return
      }
      let params = {}
      if (this.formDialog.sourceCode) {
        params.sourceCode = this.formDialog.sourceCode
      } else {
        this.$message({
          message: '请选择数据源',
          type: 'warning'
        })
        return
      }
      if (this.formDialog.sqlTest) {
        params.sqlTest = this.formDialog.sqlTest
      } else {
        this.$message({
          message: '请输入测试sql',
          type: 'warning'
        })

        return
      }
      if (this.formDialog.vcRows) {
        params.sqlRows = this.formDialog.vcRows
      } else {
        this.$message({
          message: '请选择测试条数',
          type: 'warning'
        })

        return
      }

      pageApi
        .testSql(params)
        .then((response) => {
          if (response.data.status == 200) {
            this.$message({
              message: '操作成功',
              type: 'warning'
            })
            if (response.data.data) {
              this.formDialog.testSqlData = JSON.parse(response.data.data)
              this.$refs.TestSqlDataMirror.operationVal(this.formDialog.testSqlData)
            }
          } else {
            this.$message({
              message: '操作失败',
              type: 'warning'
            })
          }
        })
        .catch(() => {
          this.$message({
            message: '操作失败',
            type: 'warning'
          })
        })
    },
    testSqlBySPL() {
      let params = {}
      if (this.formDialog.sourceCode) {
        params.sourceCode = this.formDialog.sourceCode
      } else {
        this.$message({
          message: '请选择数据源',
          type: 'warning'
        })
        return
      }
      if (this.formDialog.sqlTest) {
        params.sqlTest = this.formDialog.sqlTest
      } else {
        this.$message({
          message: '请输入测试sql',
          type: 'warning'
        })

        return
      }
      if (this.formDialog.vcRows) {
        params.sqlRows = this.formDialog.vcRows
      } else {
        this.$message({
          message: '请选择测试条数',
          type: 'warning'
        })

        return
      }

      pageApi
        .testSqlBySPL(params)
        .then((response) => {
          if (response.data.status == 200) {
            if (response.data.data) {
              this.formDialog.testSqlData = JSON.parse(response.data.data)
              this.$refs.TestSqlDataMirror.operationVal(this.formDialog.testSqlData)
            }
            this.$message({
              message: '操作成功',
              type: 'warning'
            })
          } else {
            this.$message({
              message: '操作失败',
              type: 'warning'
            })
          }
        })
        .catch(() => {
          this.$message({
            message: '操作失败',
            type: 'warning'
          })
        })
    }
  }
}
</script>

<style lang="scss" scoped>
.DiSqlConfigManage {
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
  .sql-text-style {
    color: red;
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

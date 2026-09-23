<template>
  <div class="DiIcatorConfigManage ddportal-ui">
    <el-form ref="formInline" :inline="true" :model="formInline" :rules="searchRules" class="standard-form demo-form-inline form_inline_search" style="margin-bottom: 8px;">
      <el-row>
        <el-col :span="16">
          <el-form-item label="指标名称" prop="vcIndexName">
            <el-input v-model.trim="formInline.vcIndexName" clearable placeholder="请输入" size="small"></el-input>
          </el-form-item>
          <el-form-item label="指标类型" prop="vcIndexType">
            <el-select v-model="formInline.vcIndexType" placeholder="请选择" size="small">
              <el-option v-for="(group, index) in vcIndexTypeArr" :key="index" :label="group.dimNme" :value="group.dimCde"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="功能分类" prop="vcTypeBus">
            <el-select v-model="formInline.vcTypeBus" placeholder="请选择" size="small">
              <el-option v-for="(group, index) in vcTypeBusArr" :key="index" :label="group.dimNme" :value="group.dimCde"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item class="search_button_com">
            <el-button size="small" style="margin-bottom: 5px; " type="primary" @click="onSubmit('formInline', true)">
              <i class="el-icon-search"></i>
              查询
            </el-button>
            <!-- <el-button type="primary" plain @click="modifierData()" style="margin-bottom: 5px; " size="small"><i class="el-icon-edit-outline"></i>编辑</el-button>   -->
            <el-button size="small" style="margin-bottom: 5px; " type="info" plain @click="restForm('formInline')">
              <i class="el-icon-delete"></i>
              重置
            </el-button>
            <el-button plain size="small" style="margin-bottom: 5px; " type="primary" @click="addData()">
              <i class="el-icon-circle-plus-outline"></i>
              新增
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
      v-loading="tableLoading"
      :data="tableData"
      :default-sort="{ prop: 'vcIndexName', order: 'descending' }"
      :cell-style="{ height: '40px', fontSize: '14px' }"
      :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
      stripe
      style="width: 100%"
      @selection-change="handleSelectionChange"
      @sort-change="handleSortChange"
    >
      <el-table-column align="center" type="selection" width="35"></el-table-column>

      <el-table-column
        :sort-orders="['ascending', 'descending']"
        algin="left"
        header-align="center"
        label="指标名称"
        min-width="120"
        prop="vcIndexName"
        show-overflow-tooltip
        sortable="custom"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.vcIndexName | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        :sort-orders="['ascending', 'descending']"
        algin="left"
        header-align="center"
        label="指标类型"
        min-width="100"
        prop="vcIndexType"
        show-overflow-tooltip
        sortable="custom"
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
        :sort-orders="['ascending', 'descending']"
        algin="left"
        header-align="center"
        label="指标状态"
        min-width="100"
        prop="vcStatus"
        show-overflow-tooltip
        sortable="custom"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.vcStatus === '1'">启用</span>
          <span v-else-if="scope.row.vcStatus === '0'">禁用</span>
          <span v-else>{{ scope.row.vcStatus | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        :sort-orders="['ascending', 'descending']"
        algin="left"
        header-align="center"
        label="功能分类"
        min-width="80"
        prop="vcTypeBus"
        show-overflow-tooltip
        sortable="custom"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.vcTypeBus === '0'">普通指标</span>
          <span v-else-if="scope.row.vcTypeBus === '1'">自定义指标</span>
          <span v-else-if="scope.row.vcTypeBus === '2'">查询条件指标</span>
          <span v-else>{{ scope.row.vcTypeBus | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        :sort-orders="['ascending', 'descending']"
        algin="left"
        header-align="center"
        label="自定义分类类型"
        min-width="120"
        prop="vcTypeFreebus"
        show-overflow-tooltip
        sortable="custom"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.vcTypeFreebus | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        :sort-orders="['ascending', 'descending']"
        algin="left"
        header-align="center"
        label="指标路径"
        min-width="80"
        prop="vcIndexURL"
        show-overflow-tooltip
        sortable="custom"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.vcIndexURL | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        :sort-orders="['ascending', 'descending']"
        algin="left"
        header-align="center"
        label="更新时间"
        min-width="80"
        prop="updateTime"
        show-overflow-tooltip
        sortable="custom"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.updateTime | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column align="center" label="操作" min-width="200">
        <template slot-scope="scope">
         <div class="dialog-footer standard-form">
          <el-button size="small" type="info" plain @click="editData(scope.row)">编辑</el-button>
          <el-button plain size="small" type="info" @click="delData(scope.row)">删除</el-button>
          <el-button size="small" type="info" plain @click="viewData(scope.row)">查看关联的模板</el-button>
         </div>
          <!-- <el-button type="primary" size="small" @click="previewData(scope.row)">指标预览</el-button> -->
        </template>
      </el-table-column>
    </el-table>

    <Pagination :limit="pageSize" :page="pageNum" :total="total" @pagination="Pagination"></Pagination>

    <!-- 新增指标配置表 -->
    <el-dialog v-dialogDrag :close-on-click-modal="false" :title="countTitle" :visible.sync="countDialog" center>
      <el-container class="hg100">
        <el-main class="mainBox" style="height:600px; width:800px">
          <el-form ref="formDialog" :inline="true" :model="formDialog" :rules="dialogRules" label-position="right">
            <el-form-item :label-width="formLabelWidth" class="mb20" label="指标名称" prop="vcIndexName">
              <el-input v-model.trim="formDialog.vcIndexName" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>
            <el-form-item :label-width="formLabelWidth" class="mb20" label="指标类型" prop="vcIndexType">
              <el-select v-model="formDialog.vcIndexType" placeholder="请选择" size="small">
                <el-option v-for="(group, index) in vcIndexTypeArr" :key="index" :label="group.dimNme" :value="group.dimCde"></el-option>
              </el-select>
            </el-form-item>

            <el-form-item :label-width="formLabelWidth" class="mb20" label="功能分类" prop="vcTypeBus">
              <el-select v-model="formDialog.vcTypeBus" placeholder="请选择" size="small">
                <el-option v-for="(group, index) in vcTypeBusArr" :key="index" :label="group.dimNme" :value="group.dimCde"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item :label-width="formLabelWidth" class="mb20" label="自定义分类" prop="vcTypeFreebus">
              <el-input v-model.trim="formDialog.vcTypeFreebus" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>
            <el-form-item :label-width="formLabelWidth" class="mb20" label="指标状态" prop="vcStatus">
              <el-select v-model="formDialog.vcStatus" placeholder="请选择" size="small">
                <el-option v-for="(group, index) in vcStatusArr" :key="index" :label="group.dimNme" :value="group.dimCde"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item :label-width="formLabelWidth" class="mb20" label="指标权限" prop="indexGrant">
              <el-select v-model="formDialog.indexGrant" placeholder="请选择" size="small">
                <el-option v-for="(group, index) in indexGrantArr" :key="index" :label="group.dimNme" :value="group.dimCde"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item :label-width="formLabelWidth" class="mb20" label="指标维度" prop="signCodeList">
              <el-select v-model="formDialog.signCodeList" placeholder="请选择" size="small" multiple collapse-tags>
                <el-option v-for="(group, index) in signCodeOption" :key="index" :label="group.dimNme" :value="group.dimCde"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item :label-width="formLabelWidth" class="mb20" label="数据频率授权" prop="indexDataFreqGrant">
              <el-select v-model="formDialog.indexDataFreqGrant" placeholder="请选择" size="small" >
                <el-option v-for="(group, index) in indexDataFreqAttr" :key="index" :label="group.dimNme" :value="group.dimCde"></el-option>
              </el-select>
            </el-form-item>
            <br />
            <el-form-item :label-width="formLabelWidth" class="mb20" label="指标路径" prop="vcIndexURL">
              <el-input v-model="formDialog.vcIndexURL" :rows="3" placeholder="请输入内容" size="small" style="width:730px!important;" type="textarea"></el-input>
            </el-form-item>
            <el-form-item :label-width="formLabelWidth" class="mb20" label="指标描述" prop="vcPrompt">
              <el-input v-model="formDialog.vcPrompt" :rows="3" placeholder="请输入内容" size="small" style="width:730px!important;" type="textarea"></el-input>
            </el-form-item>
            <el-form-item :label-width="formLabelWidth" class="mb20" label="备注说明" prop="vcRemark">
              <el-input v-model="formDialog.vcRemark" :rows="3" placeholder="请输入内容" size="small" style="width:730px!important;" type="textarea"></el-input>
            </el-form-item>
          </el-form>
          <el-row>
            <el-col :offset="21" :span="2">
              <el-button :loading="countSubmitLoading" size="small" type="primary" @click="countSubmit('formDialog')">
                保存
              </el-button>
            </el-col>
          </el-row>
          <br />
          <el-row>
            <el-col :offset="21" :span="2">
              <el-button :loading="countLoading" size="small" type="primary" @click="sqlAdd('formDialog')">
                添加关联SQL
              </el-button>
            </el-col>
          </el-row>

          <div style="vertical-align: middle;display: inline-block;">
            <div class="color-box"></div>
          </div>
          <span class="title-style">关联的SQL配置列表</span>
          <el-table
            ref="multipleTable"
            v-loading="tableSqlLoading"
            :data="tableSqlData"
            :default-sort="{ prop: 'vcIndexName', order: 'descending' }"
            :cell-style="{ height: '40px', fontSize: '14px' }"
            :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
            stripe
            style="width: 100%"
            @selection-change="handleSelectionChange"
            @sort-change="handleSortChange"
            @cell-mouse-leave="mouseLeave"
          >
            <el-table-column type="selection" width="35" align="center"></el-table-column>

            <el-table-column
              :sort-orders="['ascending', 'descending']"
              algin="left"
              header-align="center"
              label="自定义key"
              min-width="150"
              prop="vcKey"
              show-overflow-tooltip
              sortable="custom"
            >
              <template slot-scope="scope">
                <!-- <span >{{ scope.row.vcKey | noDataFilter }}</span> -->
                <el-input v-model.trim="scope.row.vcKey" clearable size="small"></el-input>
              </template>
            </el-table-column>
            <el-table-column
              :sort-orders="['ascending', 'descending']"
              algin="left"
              header-align="center"
              label="SQL名称"
              min-width="100"
              prop="sqlName"
              show-overflow-tooltip
              sortable="custom"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.sqlName | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              :sort-orders="['ascending', 'descending']"
              algin="left"
              header-align="center"
              label="执行方式"
              min-width="100"
              prop="sqlOperate"
              show-overflow-tooltip
              sortable="custom"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.sqlOperate | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              :sort-orders="['ascending', 'descending']"
              algin="left"
              header-align="center"
              label="创建人"
              min-width="80"
              prop="fCreateName"
              show-overflow-tooltip
              sortable="custom"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.fCreateName | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              :sort-orders="['ascending', 'descending']"
              algin="left"
              header-align="center"
              label="状态"
              min-width="120"
              prop="sqlStatus"
              show-overflow-tooltip
              sortable="custom"
            >
              <template slot-scope="scope">
                <span v-if="scope.row.sqlStatus === '1'">启用</span>
                <span v-else-if="scope.row.sqlStatus === '0'">禁用</span>
                <span v-else>{{ scope.row.sqlStatus | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column align="center" label="操作" min-width="200">
              <template slot-scope="scope">
                <div class="standard-form">
                 <el-button plain size="small" type="info" @click="deleteSql(scope.row)">删除</el-button>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </el-main>
      </el-container>
    </el-dialog>

    <el-dialog v-dialogDrag :close-on-click-modal="false" :title="previewTitle" :visible.sync="previewDialog" center>
      <el-container class="hg100">
        <el-main class="mainBox" style="height:200px; width:200px"></el-main>
      </el-container>
    </el-dialog>
    <!-- 导入查看关联指标弹框组件 -->
    <index-list :indexDialog="indexDialog" :indexTitle="indexTitle" :vcCode="templateVcCode"></index-list>
    <!-- 导入添加关联SQL组件 -->
    <associated-sql :sqlDialog="sqlDialog" :sqlTitle="sqlTitle" :vcCode="formDialog.vcCode" @sqlAddClick="sqlAddClick"></associated-sql>
  </div>
</template>

<script>
import commonApi from '@/api/common.js'
import pageApi from '@/api/dataImport/indicatorConfigManage.js'
import Pagination from '@/components/Pagination'
import IndexList from './components/indicatorList'
import AssociatedSql from './components/associatedSql'

import commonFun from '@/filters/common.js'

export default {
  name: 'DdIcatorConfigManage',
  // 注册导入组件
  components: { Pagination, IndexList, AssociatedSql },

  data() {
    return {
      formInline: {
        // 指标名称
        vcIndexName: '',
        // 指标类型
        vcIndexType: '',
        // 功能分类
        vcTypeBus: '',
        orderString: 'updateTime desc ', //列表排序
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
      indexGrantArr: [
        // { dimCde: 'All', dimNme: '无权限控制' }
      ],
      indexDataFreqAttr:[],
      dataFreqArr:[],
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
      sqlDialog: 0, //添加关联SQL弹窗
      indexTitle: '', //添加关联SQL标题
      sqlTitle: '', //查看关联指标标题
      countTitle: '', // 新增编辑标题
      previewTitle: '', // 指标预览标题
      countFormList: '', //是新增还是编辑
      // 新增 编辑计算任务
      formDialog: {
        // 指标维度
        signCodeList: [],
        // 指标编码
        vcCode: '',
        // 指标名称
        vcIndexName: '',
        // 指标类型
        vcIndexType: '',
        // 功能分类
        vcTypeBus: '',
        // 自定义分类
        vcTypeFreebus: '',
        // 指标状态
        vcStatus: '',
        // 指标权限
        indexGrant: '',
        // 指标数据频率
        indexDataFreqGrant:'',
        // 指标路径
        vcIndexURL: '',
        // 指标描述
        vcPrompt: '',
        // 备注说明
        vcRemark: ''
      },
      vcId: '', // 编辑修改时记录的id

      // 指标维度 数组下拉
      signCodeOption: [],

      // 弹窗验证规则
      dialogRules: {
        // 指标名称
        vcIndexName: [{ required: true, type: 'string', message: '请输入指标名称', trigger: 'change' }],
        vcIndexType: [{ required: true, type: 'string', message: '请选择指标类型', trigger: 'change' }],
        signCodeList: [{ required: true,message: '请选择指标维度', trigger: 'blur' }],
      },
      countSubmitLoading: false, //弹框提交保存延迟
      countLoading: false, //弹框提交添加关联SQL延迟
      submitLoading: false,
      formLabelWidth: '120px',
      checkKeyFlag: false,
      templateVcCode: ''
    }
  },

  mounted() {
    // 获取校验大类数组
    // this.getRuleCodeArr()
    this.onSubmit('formInline', true)
    this.getGrantArrOption()
    this.getGrantDataFreqOption()
    this.getEdimsBGWD()
  },
  methods: {

    /**
     * @Description: 获取报告维度字典
     * @author Liu Rui Bing
     * @date 2024/6/27
     */
    getEdimsBGWD() {
      commonApi.edimsCommon('INDEX_SIGN').then(res => {
        const { status, data } = res.data
        if (status === 0) {
          this.signCodeOption = data
        } else {
          this.signCodeOption = []
        }
      })
    },

    // 获取指标权限下拉
    getGrantArrOption() {
      let type = 'FUNDINRIGHT'
      commonApi
        .edimsCommon(type)
        .then(res => {
          let { status, data } = res.data
          if (status == 0) {
            this.indexGrantArr = data
          } else {
            this.indexGrantArr = []
          }
        })
        .catch(err => {
          this.indexGrantArr = []
        })
    },

    // 获取指标权限下拉
    getGrantDataFreqOption() {
      let type = 'FUNDDATAFREQ'
      commonApi
        .edimsCommon(type)
        .then(res => {
          let { status, data } = res.data
          if (status == 0) {
            this.indexDataFreqAttr = data
          } else {
            this.indexDataFreqAttr = []
          }
        })
        .catch(err => {
          this.indexDataFreqAttr = []
        })
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
      this.countTitle = '新增指标配置表' // 标题设置
      this.countFormList = 'add' // 新增标识
      this.checkKeyFlag = false
      //
      pageApi
        .getVcCode()
        .then(response => {
          if (!response.data.error) {
            this.countDialog = true // 显示弹框
            this.activeName = 'first' // 默认显示基础信息
            // 清除
            this.$nextTick(() => {
              this.$refs['formDialog'].resetFields()
              this.formDialog.vcStatus = '1'
              this.formDialog.indexGrant = 'All'
              this.formDialog.indexDataFreqGrant = 'All'
              this.formDialog.vcTypeBus = '0'
              this.formDialog.vcCode = response.data.data
              this.tableSqlData = []
              this.formDialog.signCodeList = []
              // 校验大类选择 默认选择第一个
              // this.formDialog.vcRuleCode = this.vcRuleCodeFormArr[0].dimCde;
            })
          } else {
            this.$message.closeAll()
            this.$message({
              message: '获取指标编码失败',
              type: 'warning'
            })
          }
        })
        .catch(() => {
          this.$message.closeAll()
          this.$message({
            message: '获取指标编码失败',
            type: 'warning'
          })
        })
    },
    //新增 、 编辑SQl配置表确认
    countSubmit(formName) {
      this.$refs[formName].validate(valid => {
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
          params.signCodeList = params.signCodeList
          pageApi
            .postIndParaThemeAdd(params)
            .then(response => {
              if (!response.data.error) {
                // 提交延迟
                let arr = this.tableSqlData
                if (arr.length > 0) {
                  this.addSql()
                } else {
                  this.countSubmitLoading = false
                  this.countDialog = false // 关闭弹框
                  this.$message.closeAll()
                  this.$message({
                    message: '新增成功',
                    type: 'success'
                  })
                  // 刷新列表
                  this.onSubmit('formInline', false)
                }
              } else {
                // 提交延迟
                this.countSubmitLoading = false
                // this.countDialog = false; // 关闭弹框
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
              //this.countDialog = false; // 关闭弹框
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
      this.checkKeyFlag = false
      let params = {}
      params.vcCode = row.vcCode
      pageApi
        .getSqlList(params)
        .then(response => {
          if (!response.data.error) {
            let arr = response.data.data
            if (arr && arr.length > 0) {
              this.tableSqlData = arr
            } else {
              this.tableSqlData = []
            }
            this.getDetail(row)
          } else {
            this.$message.closeAll()
            this.$message({
              message: '获取关联的SQL数据失败',
              type: 'warning'
            })
            this.tableSqlData = []
          }
        })
        .catch(() => {
          this.$message.closeAll()
          this.$message({
            message: '获取关联的SQL数据失败',
            type: 'warning'
          })
          this.tableSqlData = []
        })
    },
    getDetail(row) {
      let params = {}
      params.vcCode = row.vcCode
      pageApi
        .getDetail(params)
        .then(response => {
          if (!response.data.error) {
            this.countDialog = true
            this.$nextTick(() => {
              // 清除
              this.$refs['formDialog'].resetFields()
              let formData = response.data.data
              // 赋值
              if (formData.fCreateID) {
                this.vcId = formData.fCreateID
              }
              // 行id
              if (formData.vcCode) {
                this.formDialog.vcCode = formData.vcCode
              }
              //业务表英文表名
              if (formData.vcIndexName) {
                this.formDialog.vcIndexName = formData.vcIndexName
              }
              //业务表中文名称
              if (formData.vcIndexType) {
                this.formDialog.vcIndexType = formData.vcIndexType
              }
              //业务表类型
              if (formData.vcTypeBus) {
                this.formDialog.vcTypeBus = formData.vcTypeBus
              }
              //业务表英文表名
              if (formData.vcTypeFreebus) {
                this.formDialog.vcTypeFreebus = formData.vcTypeFreebus
              }
              //是否有效
              if (formData.vcStatus) {
                this.formDialog.vcStatus = formData.vcStatus
              }
              //是否有效
              if (formData.indexGrant) {
                this.formDialog.indexGrant = formData.indexGrant
              }
              //是否有效
              if (formData.vcIndexURL) {
                this.formDialog.vcIndexURL = formData.vcIndexURL
              }
              //是否有效
              if (formData.vcPrompt) {
                this.formDialog.vcPrompt = formData.vcPrompt
              }
              //是否有效
              if (formData.vcRemark) {
                this.formDialog.vcRemark = formData.vcRemark
              }
              if(formData.signCodeList) {
                this.formDialog.signCodeList = formData.signCodeList
              } else {
                this.formDialog.signCodeList = []
              }

              //是否有效
            })
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
          params.signCodeList = params.signCodeList
          pageApi
            .postIndParaThemeEdit(params)
            .then(response => {
              if (!response.data.error) {
                // 提交延迟
                let arr = this.tableSqlData
                if (arr.length > 0) {
                  this.addSql()
                } else {
                  this.countSubmitLoading = false
                  this.countDialog = false // 关闭弹框
                  this.$message.closeAll()
                  this.$message({
                    message: '修改成功',
                    type: 'success'
                  })
                  // 刷新列表
                  this.onSubmit('formInline', false)
                }
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
    addSql() {
      let arr = this.tableSqlData
      if (arr.length > 0) {
        let sqlCodeArr = []
        let keyArray = []
        for (let i = 0; i < arr.length; i++) {
          if (arr[i].sqlCode) {
            sqlCodeArr.push(arr[i].sqlCode)
          }
          if (arr[i].vcKey) {
            keyArray.push(arr[i].vcKey)
          } else {
            keyArray.push('')
          }
        }
        let params = {}
        params.sqlCodeArr = sqlCodeArr
        params.keyArray = keyArray
        params.vcCode = this.formDialog.vcCode
        //params = commonFun.parameterSrc(params);
        pageApi
          .addSqls(params)
          .then(response => {
            if (!response.data.error) {
              this.countSubmitLoading = false
              this.countDialog = false // 关闭弹框
              this.$message.closeAll()
              if (this.countFormList == 'add') {
                this.$message({
                  message: '新增成功',
                  type: 'success'
                })
              } else {
                this.$message({
                  message: '修改成功',
                  type: 'success'
                })
              }
              // 刷新列表
              this.onSubmit('formInline', false)
            } else {
            }
          })
          .catch(() => {})
      }
    },
    // 查看关联的指标按钮绑定的方法
    viewData(row) {
      this.indexTitle = '指标关联的模板列表'
      this.indexDialog++
      this.templateVcCode = row.vcCode
    },
    // 指标预览绑定的方法
    previewData(row) {
      this.previewDialog = true
      this.previewTitle = '指标预览'
    },
    sqlAdd(formInline) {
      this.sqlTitle = '新增关联SQl'
      this.sqlDialog++
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
          params['vcCode'] = row.vcCode
          pageApi
            .postIndParaThemeDel(params)
            .then(response => {
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
    delete(row) {
      let vcId = []
      // 删除列的名称
      if (row.length) {
        row.forEach(function(item) {
          vcId.push(item.vcId)
        })
      } else {
        vcId.push(row.vcId)
      }
      this.$confirm('确定删除?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          let params = {}
          params['vcId'] = vcId.join(',')
          pageApi
            .postIndParaThemeDel(params)
            .then(response => {
              if (!response.data.error) {
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
    sqlAddClick(data) {
      let params = {}
      params.vcCode = this.formDialog.vcCode
      pageApi
        .getSqlList(params)
        .then(response => {
          if (!response.data.error) {
            let arr = response.data.data
            if (arr && arr.length > 0) {
              this.tableSqlData = arr
            } else {
              this.tableSqlData = []
            }
          } else {
            this.$message.closeAll()
            this.$message({
              message: '获取关联的SQL数据失败',
              type: 'warning'
            })
            this.tableSqlData = []
          }
        })
        .catch(() => {
          this.$message.closeAll()
          this.$message({
            message: '获取关联的SQL数据失败',
            type: 'warning'
          })
          this.tableSqlData = []
        })
    },
    mouseLeave(row, column, cell, event) {
      if (!row.vcKey) {
        return
      }
      let params = {}
      params.vcKey = row.vcKey
      params.vcCode = this.formDialog.vcCode
      pageApi
        .keyCheck(params)
        .then(response => {
          if (!response.data.error) {
          } else {
            this.$message.closeAll()
            this.$message({
              message: '自定义key:' + vcKey + '已存在',
              type: 'warning'
            })
            this.checkKeyFlag = true
          }
        })
        .catch(() => {})
    },
    deleteSql(row) {
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
          params['vcCode'] = this.formDialog.vcCode
          pageApi
            .deleteSql(params)
            .then(response => {
              if (!response.data.error) {
                this.$message.closeAll()
                this.$message({
                  message: '删除成功',
                  type: 'success'
                })
                // 刷新列表
                this.sqlAddClick('1')
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
    }
  }
}
</script>

<style lang="scss" scoped>
.DiIcatorConfigManage {
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
    width: 65% !important;

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
::v-deep .el-button--danger.is-plain {
  background:#f4f4f5;
}
</style>

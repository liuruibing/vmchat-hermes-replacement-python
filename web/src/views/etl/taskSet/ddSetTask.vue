<template>
  <div class="setTask ddportal-ui">
    <el-form :inline="true" class="formQuery">
      <el-row>
        <el-col :span="16">
          <!-- 查询 -->
          <div class="grid-content bg-purple">
            <el-form-item label="任务编码" prop="misCde">
              <el-input v-model.trim="formQuery.misCde" clearable placeholder="请输入任务编码" size="small"></el-input>
            </el-form-item>
            <el-form-item label="任务名称" prop="misNme">
              <el-input v-model.trim="formQuery.misNme" clearable placeholder="请输入任务名称" size="small"></el-input>
            </el-form-item>
            <el-form-item label="任务类型" prop="misTyp">
              <el-select v-model="formQuery.misTyp" placeholder="请选择" size="small">
                <el-option label="全部" value></el-option>
                <el-option v-for="item in jobTypeArr" :key="item.id" :label="item.jobTypeName" :value="item.jobTypeCode"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="是否启用" prop="misRun">
              <el-select v-model="formQuery.misRun" placeholder="请选择" size="small">
                <el-option label="全部" value></el-option>
                <el-option label="启用" value="1"></el-option>
                <el-option label="禁用" value="0"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="任务说明" prop="misCmt">
              <el-input v-model.trim="formQuery.misCmt" clearable placeholder="请输入任务说明" size="small"></el-input>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="8">
          <el-form-item class="search_button_com">
            <el-button type="primary" :disabled="btnDisabled" class="mb5" icon="el-icon-search" size="small" @click="onQuery(true)">
              查询
            </el-button>
            <el-button type="primary" plain size="small" icon="el-icon-circle-plus-outline" @click="addDate">
              新增
            </el-button>
            <el-button plain type="primary" icon="el-icon-delete" size="small" @click="deletall">
              批量删除
            </el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <div style="vertical-align: middle;display: inline-block;">
      <div class="color-box"></div>
    </div>
    <span class="title-style">任务设置信息</span>

    <el-table
      ref="multipleTable"
      @selection-change="handleSelectionChange"
      :data="tableData"
      :default-sort="{ prop: 'vcBeDate', order: 'descending' }"
      stripe
      @sort-change="handleSortChange"
      v-loading="tableLoading"
      style="width: 100%"
      :cell-style="{ height: '40px', fontSize: '14px' }"
      :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
    >
      <el-table-column type="selection" width="35" align="center"></el-table-column>

      <el-table-column prop="misCde" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="任务编码" min-width="150" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.misCde | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="misNme" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="任务名称" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.misNme | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="misTypName"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="任务类型名称"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.misTypName | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="misRun" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="是否启用" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span v-if="scope.row.misRun == '禁用'" style="color:red">
            {{ scope.row.misRun | noDataFilter }}
          </span>
          <span v-else>{{ scope.row.misRun | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="misCmt" show-overflow-tooltip label="任务说明" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.misCmt | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column label="操作" min-width="120" align="center">
        <template slot-scope="scope">
          <div class="standard-form dialog-footer">
            <el-button type="info" size="small" plain @click="editData(scope.row)">编辑</el-button>
            <el-button type="info" plain size="small" @click="delData(scope.row)">删除</el-button>
            <el-button :disabled="scope.row.misRun == '禁用'" type="info" plain size="small" @click="handleData(scope.row)">
              手工执行
            </el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <Pagination :total="total" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination"></Pagination>

    <!-- 新增/修改 参数弹窗 -->
    <el-dialog title="任务设置" center :visible.sync="dialogMask" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox">
          <el-form :inline="true" ref="formDialog" :model="formDialog" :rules="dialogRules" label-position="right">
            <el-form-item label="任务编码" prop="misCde" class="mb20 formInput-adaptive" :label-width="formLabelWidth">
              <el-input v-if="operationType == 2" disabled v-model.trim="formDialog.misCde" clearable placeholder="请输入" size="small"></el-input>
              <el-input v-else v-model.trim="formDialog.misCde" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>

            <el-form-item label="任务名称" prop="misNme" class="mb20 formInput-adaptive" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog.misNme" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>
            <el-form-item label="任务描述" prop="misCmt" class="mb20 formInput-adaptive" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog.misCmt" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>
            <el-form-item label="目标源" prop="aimDbsCde" class="mb20 formInput-adaptive" :label-width="formLabelWidth">
              <el-select v-model.trim="formDialog.aimDbsCde" placeholder="请选择" size="small">
                <el-option v-for="item in SourceList" :key="item.id" :label="item.dbsNme" :value="item.dbsCde"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="任务类型" prop="misTyp" class="mb20 formInput-adaptive" :label-width="formLabelWidth">
              <el-select v-model.trim="formDialog.misTyp" placeholder="请选择" size="small" @change="handleMisTypChange(formDialog.misTyp)">
                <el-option v-for="item in jobTypeArr" :key="item.id" :label="item.jobTypeName" :value="item.jobTypeCode"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="源数据源" prop="srcDbsCde" class="mb20 formInput-adaptive" :label-width="formLabelWidth">
              <el-select :disabled="formDialog.misTyp === 'TXT'" v-model.trim="formDialog.srcDbsCde" placeholder="请选择" size="small">
                <el-option v-for="item in SourceList2" :key="item.id" :label="item.dbsNme" :value="item.dbsCde"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="日期类型" prop="natureDay" class="mb20 formInput-adaptive" :label-width="formLabelWidth">
              <el-select v-model.trim="formDialog.natureDay" placeholder="请选择" size="small">
                <el-option label="自然日" value="0"></el-option>
                <el-option label="交易日" value="1"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="日期偏移量" prop="misIndex" class="mb20 formInput-adaptive" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog.misIndex" clearable placeholder="例:单:-1，双:-5,-2" size="small" style="width:200px"></el-input>
            </el-form-item>
            <el-form-item label="是否启用" prop="misRun" class="mb20 formInput-adaptive" :label-width="formLabelWidth">
              <el-select v-model.trim="formDialog.misRun" placeholder="请选择" size="small">
                <el-option label="启用" value="1"></el-option>
                <el-option label="禁用" value="0"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="循环标志" prop="misEachDayFlag" class="mb20 formInput-adaptive" :label-width="formLabelWidth">
              <el-select v-model.trim="formDialog.misEachDayFlag" placeholder="请选择" size="small">
                <el-option label="每天" value="0"></el-option>
                <el-option label="时间段" value="1"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="邮件主题" prop="misMailSubject" class="mb20 formInput-adaptive-100" :label-width="formLabelWidth" v-show="formDialog.misTyp == 'MAILREPORT'">
              <el-input v-model="formDialog.misMailSubject" clearable placeholder="请输入" type="textarea"></el-input>
            </el-form-item>
            <el-form-item label="收件人" prop="misMailReceivers" class="mb20 formInput-adaptive-100" :label-width="formLabelWidth" v-show="formDialog.misTyp == 'MAILREPORT'">
              <el-input v-model="formDialog.misMailReceivers" clearable placeholder="收件人，多个以英文分号(;)分隔开,例如:aaa@qq.com;bbb@qq.com" type="textarea"></el-input>
            </el-form-item>

            <el-form-item label="文件路径" prop="filUrl" class="mb20 formInput-adaptive-100" :label-width="formLabelWidth">
              <el-input
                v-model="formDialog.filUrl"
                clearable
                placeholder="请输入"
                type="textarea"
                v-if="
                  formDialog.misTyp == 'PROCEDURE' ||
                    formDialog.misTyp == 'DATABASE' ||
                    formDialog.misTyp == 'MULTIPARAMDATABASE' ||
                    formDialog.misTyp == 'MULTIPARAMPROCEDURE' ||
                    formDialog.misTyp == 'JAVA' ||
                    formDialog.misTyp == 'GFREPORTSUBSCRIPTION'
                "
                disabled
              ></el-input>
              <el-input v-else v-model="formDialog.filUrl" clearable placeholder="请输入" type="textarea"></el-input>
            </el-form-item>
            <el-form-item
              label="前置条件 (Ctrl键唤醒代码提示 传值示例: select count(1) as cnt from dual)"
              prop="prevSqlSet"
              class="mb20 ddCode-mirror-form ddCode-mirror-form-200"
              :label-width="'500px'"
              label-position="left"
            >
              <dd-code-mirror ref="prevSqlSetCodeMirror" :language="prevSqlSetLanguage" @codeChange="prevSqlSetChange"></dd-code-mirror>
            </el-form-item>
            <el-form-item label="参数设置" prop="parSet" class="mb20 formInput-adaptive-100 formInput-fontSize-16" :label-width="formLabelWidth">
              <el-input
                v-model="formDialog.parSet"
                clearable
                placeholder="请输入"
                :autosize="{ minRows: 4, maxRows: 6 }"
                type="textarea"
                v-if="formDialog.misTyp == 'PROCEDURE' || formDialog.misTyp == 'ZIP' || formDialog.misTyp == 'BAT' || formDialog.misTyp == 'GFREPORTSUBSCRIPTION'"
                disabled
              ></el-input>
              <el-input v-else v-model="formDialog.parSet" clearable placeholder="请输入" :autosize="{ minRows: 4, maxRows: 6 }" type="textarea"></el-input>
            </el-form-item>
            <el-form-item label="清除设置 (Ctrl键唤醒代码提示)" prop="clsSet" class="mb20 ddCode-mirror-form ddCode-mirror-form-200" :label-width="'215px'" label-position="left">
              <dd-code-mirror
                :disabled="formDialog.misTyp == 'PROCEDURE' || formDialog.misTyp == 'ZIP' || formDialog.misTyp == 'BAT' || formDialog.misTyp == 'JAVA' || formDialog.misTyp == 'GFREPORTSUBSCRIPTION'"
                ref="clsSetCodeMirror"
                :language="clsSetLanguage"
                @codeChange="clsSetChange"
              ></dd-code-mirror>
            </el-form-item>
            <el-form-item label="映射规则" prop="datSrcSet" class="mb20 formInput-adaptive-100 formInput-fontSize-16" :label-width="formLabelWidth">
              <el-input
                v-model="formDialog.datSrcSet"
                clearable
                placeholder="请输入"
                type="textarea"
                :autosize="{ minRows: 4, maxRows: 6 }"
                v-if="formDialog.misTyp == 'JAVA'"
                disabled
              ></el-input>
              <el-input v-model="formDialog.datSrcSet" clearable placeholder="请输入" type="textarea" :autosize="{ minRows: 4, maxRows: 6 }" v-else></el-input>
            </el-form-item>
            <el-form-item label="目标SQL (Ctrl键唤醒代码提示)" prop="aimSqlSet" class="mb20 ddCode-mirror-form ddCode-mirror-form-200" :label-width="'215px'" label-position="left">
              <dd-code-mirror
                :disabled="formDialog.misTyp == 'PROCEDURE' || formDialog.misTyp == 'ZIP' || formDialog.misTyp == 'BAT' || formDialog.misTyp == 'JAVA' || formDialog.misTyp == 'GFREPORTSUBSCRIPTION' "
                ref="aimSqlSetCodeMirror"
                :language="aimSqlSetLanguage"
                @codeChange="aimSqlSetChange"
              ></dd-code-mirror>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer standard-form">
        <el-button type="primary" size="small" @click="dealData" :loading="dialogMaskBtn">提 交</el-button>
        <el-button size="small" type="info" plain @click="dialogMask = false">取 消</el-button>
      </div>
    </el-dialog>

    <!-- 手工执行 参数弹窗2 -->
    <el-dialog :title="handleWord" center :visible.sync="dialogMask2" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox">
          <el-form :inline="true" ref="formDialog2" :model="formDialog2" :rules="dialogRules2" label-position="right">
            <el-form-item label="日期" prop="date" :label-width="formLabelWidth" class="mb20">
              <el-date-picker
                v-model="formDialog2.date"
                type="datetimerange"
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
            <el-form-item label="产品代码" prop="fundCodes" class="mb20 formInput-adaptive-100" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog2.fundCodes" clearable placeholder="请输入产品代码" type="textarea" @focus="focusCode"></el-input>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer standard-form">
        <el-button type="primary" size="small" @click="handledealData">提 交</el-button>
        <el-button type="info" size="small" plain @click="dialogMask2 = false">取 消</el-button>
      </div>
    </el-dialog>

    <!-- 手工执行 查询代码 弹窗3  -->
    <el-dialog title="选择产品" center :visible.sync="dialogMask3" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox">
          <el-form :inline="true" ref="formDialog3" :model="formDialog3" label-position="right">
            <el-form-item label="组合代码" prop="fundCode" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog3.fundCode" clearable placeholder="请输入产品代码" size="small"></el-input>
            </el-form-item>
            <el-form-item label="组合名称" prop="fundName" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog3.fundName" clearable placeholder="请输入组合名称" size="small"></el-input>
            </el-form-item>
          </el-form>
          <el-row>
            <div style="float:right;margin-bottom:10px">
              <el-button type="primary" plain size="small" @click="onQuery2(true)">查询</el-button>
              <el-button type="primary" plain size="small" @click="handleSelect">选择</el-button>
            </div>
          </el-row>

          <div class="forms_table_title">
            <i class="el-icon-tickets"></i>
            产品信息
          </div>
          <el-table
            ref="multipleTable"
            :data="tableData3"
            @selection-change="handleSelectionChange"
            border
            stripe
            :default-sort="{ prop: 'fundCode', order: 'descending' }"
            @sort-change="handleSortChange3"
            v-loading="tableLoading3"
            style="width: 100%"
            row-key="id"
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

          <Pagination :total="total3" :limit="formDialog3.pageSize" :page="formDialog3.pageNum" @pagination="pagination2"></Pagination>
        </el-main>
      </el-container>
    </el-dialog>
  </div>
</template>

<script>
import commonApi from '@/api/etl/setTask'
import Pagination from '@/components/Pagination'
import fun from '@/filters/common'
import DdCodeMirror from '@/components/codemirror.vue'
import commonValidate from '@/utils/validate'

export default {
  name: 'DdSetTask',
  components: {
    Pagination,
    DdCodeMirror
  },
  data() {
    return {
      tableData: [], //表格数据
      tableLoading: false, //表格加载
      tableData3: [], //表格3 数据
      tableLoading3: false, //表格 3加载
      dialogMask: false, // 弹窗
      dialogMask2: false, // 弹窗 2
      dialogMask3: false, // 弹窗 3
      total3: 0,

      codeOk: true,
      // 任务类型集合
      jobTypeArr: [],
      // //总条数
      total: 0,
      // 顶部查询条件
      formQuery: {
        // 任务编码
        misCde: '',
        // 任务名称
        misNme: '',
        // 任务类型
        misTyp: '',
        // 是否启用
        misRun: '',
        // 任务说明
        misCmt: '',
        // 排序字段
        orderBy: 'misCde desc',
        // 起始页
        pageNum: 1,
        // 每页大小
        pageSize: 10
      },
      // 弹窗查询参数
      formDialog: {
        //  任务编码
        misCde: '',
        // 任务名称
        misNme: '',
        // 任务描述
        misCmt: '',
        // 目标源
        aimDbsCde: '',
        // 任务类型
        misTyp: '',
        // 源数据源
        srcDbsCde: '',
        // 日期类型
        natureDay: '0',
        // 日期偏移量
        misIndex: '',
        // 是否启用
        misRun: '1',
        // 循环标志
        misEachDayFlag: '0',
        // 邮件主题
        misMailSubject: '',
        // 邮件收件人
        misMailReceivers: '',
        // 文件路径
        filUrl: '',
        // 前置条件
        prevSqlSet: '',
        // 参数设置
        parSet: '',
        // 清除设置
        clsSet: '',
        // 映射规则
        datSrcSet: '',
        // 目标SQL
        aimSqlSet: ''
      },
      // 代码编辑器
      prevSqlSetLanguage: 'x-sql', //前置条件语言类型
      clsSetLanguage: 'x-sql', //清除设置语言类型
      aimSqlSetLanguage: 'x-sql', //目标SQL语言类型
      // 弹窗验证规则
      dialogRules: {
        // 任务编码
        misCde: [{ required: true, message: '请填写任务编码', trigger: 'change' }],
        // 任务名称
        misNme: [{ required: true, message: '请填写任务名称', trigger: 'change' }],
        // 目标源
        aimDbsCde: [{ required: true, message: '请填写目标源', trigger: 'change' }],
        // 任务类型
        misTyp: [{ required: true, message: '请填写任务类型', trigger: 'change' }]
      },
      // 弹窗2查询参数
      formDialog2: {
        // 日期
        date: [],
        // 产品代码
        fundCodes: '',
        // 自定义参数
        custom: ''
      },
      customLanguage: 'javascript', //自定义参数编辑器语言类型
      // 弹窗验证规则
      dialogRules2: {
        // 日期
        date: [{ required: true, message: '请填写日期', trigger: 'change' }]
      },
      // 弹窗2查询参数
      formDialog3: {
        // 组合代码
        fundCode: '',
        // 组合名称
        fundName: '',
        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10,
        // 排序条件
        orderBy: 'fundCode desc'
      },
      // 手工执行传给接口的产品代码
      handlefundCodes: '',
      // 手工执行显示文字
      handleWord: '手工执行',
      // 操作类型 1、添加 2、编辑
      operationType: 1,
      formLabelWidth: '100px',
      // 批量删除的数据
      multipleSelection: [],
      // 手工执行按钮禁用
      btnDisabled: false,
      // 数据源数据集合
      SourceList: [],
      // 源数据源
      SourceList2: [],
      // 手工执行任务编码
      handlemisCde: '',
      dialogMaskBtn: false
    }
  },

  mounted() {
    // 默认查询
    this.onQuery(true)
    // 获取任务类型集合
    this.getList()
  },
  methods: {
    handleMisTypChange(val) {
      this.formDialog.srcDbsCde = ''
      if (val === 'SPL') {
        this.getSPLSourceList()
      } else {
        this.getSourceList2()
      }
    },
    // 日期快捷选项
    dateShortcut() {
      return fun.dateShortcut()
    },
    // 根据任务编码查询任务
    taskSetByCode(misCde) {
      let params = { misCde }
      commonApi
        .getTaskSetByCode(params)
        .then(res => {
          // this.jobTypeArr = res.data.data;
          // this.$nextTick(() => {
          // 清除
          // this.$refs["formDialog"].resetFields();

          let {
            // misCde,
            // misNme,
            // misCmt,
            // aimDbsCde,
            // misTyp,
            // srcDbsCde,
            // natureDay,
            // misIndex,
            // misRun,
            misEachDayFlag,
            misMailSubject,
            misMailReceivers,
            filUrl,
            parSet,
            datSrcSet
          } = res.data.data

          // this.formDialog.misCde = misCde;
          // this.formDialog.misNme = misNme;
          // this.formDialog.misCmt = misCmt;
          // this.formDialog.aimDbsCde = aimDbsCde;
          // this.formDialog.misTyp = misTyp;
          // this.formDialog.srcDbsCde = srcDbsCde;
          // this.formDialog.natureDay = natureDay;
          // this.formDialog.misIndex = misIndex;
          // this.formDialog.misRun = misRun;
          this.formDialog.misEachDayFlag = misEachDayFlag
          this.formDialog.misMailSubject = misMailSubject
          this.formDialog.misMailReceivers = misMailReceivers
          this.formDialog.filUrl = filUrl
          this.formDialog.parSet = parSet
          this.formDialog.datSrcSet = datSrcSet
          // });
          let responsedata = res.data.data
          // 前置条件回填
          if (responsedata.prevSqlSet) {
            // 编辑器回填赋值
            this.$refs.prevSqlSetCodeMirror.operationVal(responsedata.prevSqlSet)
            // 页面提交变量赋值
            this.formDialog.prevSqlSet = responsedata.prevSqlSet
          } else {
            this.$refs.prevSqlSetCodeMirror.operationVal('')
          }
          // 清除设置回填
          if (responsedata.clsSet) {
            // 编辑器回填赋值
            this.$refs.clsSetCodeMirror.operationVal(responsedata.clsSet)
            // 页面提交变量赋值
            this.formDialog.clsSet = responsedata.clsSet
          } else {
            this.$refs.clsSetCodeMirror.operationVal('')
          }
          // 目标SQL回填
          if (responsedata.aimSqlSet) {
            // 编辑器回填赋值
            this.$refs.aimSqlSetCodeMirror.operationVal(responsedata.aimSqlSet)
            // 页面提交变量赋值
            this.formDialog.aimSqlSet = responsedata.aimSqlSet
          } else {
            this.$refs.aimSqlSetCodeMirror.operationVal('')
          }
        })
        .catch(() => {})
    },
    // 根据任务编码查询任务
    taskSetByCode2(misCde) {
      let params = { misCde }
      commonApi
        .getTaskSetByCode(params)
        .then(res => {
          // this.jobTypeArr = res.data.data;
          // this.$nextTick(() => {
          // 清除
          // this.$refs["formDialog"].resetFields();

          let {
            // misCde,
            // misNme,
            // misCmt,
            // aimDbsCde,
            // misTyp,
            // srcDbsCde,
            // natureDay,
            // misIndex,
            // misRun,
            misEachDayFlag,
            misMailSubject,
            misMailReceivers,
            filUrl,
            parSet,
            datSrcSet
          } = res.data.data

          // this.formDialog.misCde = misCde;
          // this.formDialog.misNme = misNme;
          // this.formDialog.misCmt = misCmt;
          // this.formDialog.aimDbsCde = aimDbsCde;
          // this.formDialog.misTyp = misTyp;
          // this.formDialog.srcDbsCde = srcDbsCde;
          // this.formDialog.natureDay = natureDay;
          // this.formDialog.misIndex = misIndex;
          // this.formDialog.misRun = misRun;
          this.formDialog.misEachDayFlag = misEachDayFlag
          this.formDialog.misMailSubject = misMailSubject
          this.formDialog.misMailReceivers = misMailReceivers
          this.formDialog.filUrl = filUrl
          this.formDialog.parSet = parSet
          this.formDialog.datSrcSet = datSrcSet
          // });
          let responsedata = res.data.data
          // 前置条件回填
          if (responsedata.prevSqlSet) {
            // 编辑器回填赋值
            this.$refs.prevSqlSetCodeMirror.operationVal(responsedata.prevSqlSet)
            // 页面提交变量赋值
            this.formDialog.prevSqlSet = responsedata.prevSqlSet
          } else {
            this.$refs.prevSqlSetCodeMirror.operationVal('')
          }
          // 清除设置回填
          if (responsedata.clsSet) {
            // 编辑器回填赋值
            this.$refs.clsSetCodeMirror.operationVal(responsedata.clsSet)
            // 页面提交变量赋值
            this.formDialog.clsSet = responsedata.clsSet
          } else {
            this.$refs.clsSetCodeMirror.operationVal('')
          }
          // 目标SQL回填
          if (responsedata.aimSqlSet) {
            // 编辑器回填赋值
            this.$refs.aimSqlSetCodeMirror.operationVal(responsedata.aimSqlSet)
            // 页面提交变量赋值
            this.formDialog.aimSqlSet = responsedata.aimSqlSet
          } else {
            this.$refs.aimSqlSetCodeMirror.operationVal('')
          }
        })
        .catch(() => {})
    },

    // 添加时 验证代码唯一性
    onlyCode() {
      let params = { misCde: this.formDialog.misCde }
      commonApi
        .getTaskSetByCode(params)
        .then(res => {
          if (res.data.status == 200) {
            this.$message.closeAll()
            this.$message.error('编码已经存在，请勿重复添加！')
          } else {
            this.addParamSet()
          }
        })
        .catch(() => {})
    },
    // 获取任务类型集合
    getList() {
      commonApi
        .getTaskTypeList()
        .then(res => {
          this.jobTypeArr = res.data.data
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
        .getTaskList(params)
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
    // 前置条件赋值给页面变量
    prevSqlSetChange(val) {
      this.formDialog.prevSqlSet = val
    },
    // 清除设置赋值给页面变量
    clsSetChange(val) {
      this.formDialog.clsSet = val
    },
    // 目标sql赋值给页面变量
    aimSqlSetChange(val) {
      this.formDialog.aimSqlSet = val
    },
    // 数据源数据集合
    getSourceList() {
      commonApi
        .getDataSourceList()
        .then(res => {
          // dbsNme;
          this.SourceList = res.data.data
        })
        .catch(() => {})
    },
    // 数据源数据集合
    getSourceList2() {
      commonApi
        .getDataSourceList()
        .then(res => {
          // dbsNme;
          this.SourceList2 = res.data.data
        })
        .catch(() => {})
    },
    getSPLSourceList() {
      commonApi
        .getSPLDataSourceList()
        .then(res => {
          // dbsNme;
          this.SourceList2 = res.data.data
        })
        .catch(() => {})
    },

    // 新增按钮
    addDate() {
      // 数据源数据集合
      this.getSourceList()

      this.dialogMask = true
      this.operationType = 1
      this.$nextTick(() => {
        this.$refs['formDialog'].resetFields()
        // 清空编辑器回填的值
        // 前置条件
        this.$refs.prevSqlSetCodeMirror.operationVal('')
        // 清除设置
        this.$refs.clsSetCodeMirror.operationVal('')
        // 目标SQL
        this.$refs.aimSqlSetCodeMirror.operationVal('')
      })
    },
    // 处理数据
    dealData() {
      this.$refs['formDialog'].validate(valid => {
        if (valid) {
          if (this.operationType === 1) {
            // 添加
            // this.addParamSet();
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
      this.dialogMaskBtn = true
      let params = Object.assign({}, this.formDialog)
      if (params.misTyp === 'TXT') {
        params.srcDbsCde = ''
      }
      commonApi
        .addTaskSet(params)
        .then(res => {
          if (res.data.status === 200) {
            this.onQuery(true)
            this.$message.closeAll()
            this.$message({
              type: 'success',
              message: res.data.message
            })
            this.dialogMask = false
          } else {
            this.$message.closeAll()

            this.$message.error(res.data.errormsg)
          }
          this.dialogMaskBtn = false
        })
        .catch(() => {})
    },
    // 修改参数
    updateParamSet() {
      this.dialogMaskBtn = true

      let params = Object.assign({}, this.formDialog)

      if (params.misRun == '启用') {
        params.misRun = '1'
      } else if (params.misRun == '禁用') {
        params.misRun = '0'
      }
      if (params.misTyp === 'TXT') {
        params.srcDbsCde = ''
      }

      commonApi
        .updateTaskSet(params)
        .then(res => {
          if (res.data.status === 200) {
            this.onQuery(false)
            this.$message.closeAll()
            this.$message({
              type: 'success',
              message: res.data.message
            })
            this.dialogMask = false
          } else {
            this.$message.closeAll()

            this.$message.error(res.data.errormsg)
          }
          this.dialogMaskBtn = false
        })
        .catch(() => {})
    },
    // 单个删除
    deleteParamSet(misCde) {
      let params = { misCde: misCde }

      commonApi
        .deleteTaskset(params)
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

            this.$message.error(res.data.errormsg)
          }
        })
        .catch(() => {})
    },
    // 批量删除
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
              arr.push(item.misCde)
            })
            str.misCdes = arr.join(',')

            commonApi
              .batchDeleteDataSource(str)
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

                  this.$message.error(res.data.errormsg)
                }
              })
              .catch(() => {})
          })
          .catch(() => {})
      } else if (this.multipleSelection.length === 0) {
        this.$message.closeAll()
        this.$message({
          message: '请选择要批量删除的数据',
          type: 'warning'
        })
      }
    },
    // 批量删除数据
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
      // 数据源数据集合
      this.getSourceList()

      this.dialogMask = true
      this.operationType = 2
      this.$nextTick(() => {
        // 清除
        this.$refs['formDialog'].resetFields()

        let { misCde, misNme, misCmt, aimDbsCde, misTyp, srcDbsCde, natureDay, misIndex, misRun, misEachDayFlag, misMailSubject, misMailReceivers, filUrl, parSet, datSrcSet } = row

        this.formDialog.misCde = misCde
        this.formDialog.misNme = misNme
        this.formDialog.misCmt = misCmt
        this.formDialog.aimDbsCde = aimDbsCde
        this.formDialog.misTyp = misTyp
        if (this.formDialog.misTyp === 'SPL') {
          this.getSPLSourceList()
        } else {
          this.getSourceList2()
        }
        this.formDialog.srcDbsCde = srcDbsCde
        this.formDialog.natureDay = natureDay
        this.formDialog.misIndex = misIndex
        this.formDialog.misRun = misRun
        this.formDialog.misEachDayFlag = misEachDayFlag
        this.formDialog.misMailSubject = misMailSubject
        this.formDialog.misMailReceivers = misMailReceivers

        this.formDialog.filUrl = filUrl
        this.formDialog.parSet = parSet
        this.formDialog.datSrcSet = datSrcSet

        // 根据任务编码查询任务
        this.taskSetByCode(misCde)
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
          this.deleteParamSet(row.misCde)
        })
        .catch(() => {})
    },
    // 手工执行的处理数据
    handleData(row) {
      this.handleWord = row.misNme + '(' + row.misCde + ')'
      this.handlemisCde = row.misCde
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
          params.misCde = this.handlemisCde
          // 手工执行的名字变成代传参
          params.fundCodes = this.handlefundCodes
          // 手工执行
          commonApi
            .implementTask(params)
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
      this.dialogMask3 = true
      this.tableLoading3 = true
      this.onQuery2(true)
    },
    // 手工执行查询
    onQuery2(flag) {
      if (flag) {
        this.formDialog3.pageNum = 1
      }
      let params = Object.assign({}, this.formDialog3)
      commonApi
        .getFundList(params)
        .then(res => {
          this.tableLoading3 = false

          let { list, total } = res.data.data
          // 总条数
          this.total3 = total
          this.tableData3 = list
        })
        .catch(() => {})
    },
    // 手工执行下查询代码 排序
    handleSortChange3(val) {
      this.formDialog3.orderBy = fun.queryOrderBy(val)
      // 查询
      this.onQuery2(false)
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
      this.dialogMask3 = false
      this.$message.closeAll()
      this.$message({
        type: 'success',
        message: '添加成功！'
      })
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
    //  分页
    pagination2(val) {
      let { page, limit } = val
      // 起始页
      this.formDialog3.pageNum = page
      // 每页数量
      this.formDialog3.pageSize = limit
      // 查询
      this.onQuery2(false)
    }
  }
}
</script>

<style lang="scss" scoped>
.setTask {
  padding-left: 10px;
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
    width: 60% !important;

    .el-form {
      width: 100% !important;
      font-size: 0;
    }

    .el-input {
      // width: 120% !important;
    }

    .el-form-item {
      min-width: 50%;
      margin-right: 0;
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
</style>

<style rel="stylesheet/scss" lang="scss">
//  .misCdeClass .el-input--small{
//       width: 350px!important;
//    }
</style>

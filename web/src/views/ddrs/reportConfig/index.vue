<template>
  <div class="custom-configuration">
    <!-- 报表信息 -->
    <div class="forms_table_title">
      <i class="el-icon-document" />模式:
      <span style="color: #dc2a4c; margin-left: 10px"
        >{{ mode | modeStr }}
      </span>
      <template v-if="mode === 'edit'">
        <el-select
          v-model="version"
          placeholder="请选择版本号"
          size="small"
          style="margin-left: 8px; margin-right: 8px"
          @change="versionChange"
        >
          <el-option
            v-for="item in versionOption"
            :key="item.version"
            :label="item.version"
            :value="item.version"
          >
          </el-option>
        </el-select>
        <el-button
          v-show="versionOption && versionOption.length > 1"
          size="small"
          type="danger"
          @click="handleDelCurrentVersion"
          >删除当前版本
        </el-button>
      </template>
      <div style="padding-top: 10px">
        <el-form :model="formData" label-width="100px">
          <el-form-item label="页面类型" prop="reportType">
            <el-select
              size="small"
              v-model="formData.reportType"
              placeholder="请选择"
              style="width: 200px"
              :disabled="mode == 'edit'"
              @change="reportTypeChange"
            >
              <el-option label="RS补录" value="1"></el-option>
              <el-option label="RS导出" value="2"></el-option>
            </el-select>
            <!-- <SelectTable
              v-show="formData.reportType == '2'"
              style="float: right"
              ref="SelectTableTemplateCode"
              v-model="formData.templateCode"
              :Columns="templateCodeColumns"
              :data="templateCodeList"
              label-field="vcTemplatEname"
              placeholder="请选择导出报告"
              size="small"
              value-field="fTemplateID"
              width="500px"
            /> -->
          </el-form-item>
        </el-form>
      </div>
    </div>
    <!-- 报表配置 -->
    <div class="sql_search" v-show="formData.reportType == '1'">
      <div class="sql_box">
        <div class="forms_table_title">
          <i class="el-icon-edit" />查询sql：
          <el-button
            :disabled="check == '1'"
            :loading="runSqlLoading"
            class="sql_search_btn"
            size="mini"
            type="primary"
            @click="runSql"
            >执行
          </el-button>
        </div>
        <el-input
          v-model="sqlText"
          :rows="8"
          placeholder="请输入内容"
          type="textarea"
        />
        <!-- <jsonEditor v-model="sqlText"></jsonEditor> -->
      </div>
    </div>

    <div class="forms_table_title" style="margin-top: 20px">
      <i class="el-icon-s-data" />列表
      <span style="margin-left: 20px">
        <el-button
          plain
          size="small"
          style="margin-bottom: 5px; margin-left: 20px"
          type="primary"
          @click="insertEvent"
        >
          <i class="el-icon-circle-plus-outline" />新增
        </el-button>
        <el-button
          plain
          size="small"
          style="margin-bottom: 5px"
          type="danger"
          @click="removeEvent"
        >
          <i class="el-icon-delete" />移除
        </el-button>
      </span>
    </div>

    <!-- 列表 -->
    <div id="vxetable_custom">
      <vxe-table
        :key="tableKey"
        ref="vxeTable"
        v-loading="tableLoading"
        :cell-class-name="cellClassName"
        :data="tableData"
        :edit-config="{ trigger: 'click', mode: 'cell' }"
        :header-cell-class-name="headerCellClassName"
        auto-resize
        border
        class="vxe_table"
        header-align="center"
        height="300px"
        resizable
        size="mini"
      >
        <!-- <vxe-table-column type="seq" width="60"></vxe-table-column> -->
        <vxe-table-column
          align="center"
          fixed="left"
          type="checkbox"
          width="40"
        />
        <vxe-table-column
          :edit-render="{
            name: 'input',
            attrs: {
              type: 'text',
            },
          }"
          field="fieldEn"
          width="120"
          title="字段英文名"
        >
          <template slot-scope="scope" slot="edit">
            <vxe-input
              v-model="scope.row.fieldEn"
              size="small"
              :disabled="
                formData.reportType == '2' &&
                scope.row.fieldEn == 'templateCode'
              "
            />
          </template>
        </vxe-table-column>

        <vxe-table-column
          :edit-render="{ name: 'input', attrs: { type: 'text' } }"
          field="fieldCn"
          width="120"
          title="字段中文名"
        />
        <vxe-table-column
          :edit-render="{
            name: '$select',
            options: fieldTypeArr,
            events: { change: fieldTypeChange },
          }"
          field="fieldType"
          title="字段类型"
          width="100"
        />
        <!-- :edit-render="{ name: 'input', attrs: { type: 'text' }, }" -->
        <vxe-table-column
          :edit-render="{
            name: 'input',
            attrs: { type: 'text' },
          }"
          field="fieldLength"
          title="字段长度"
          width="100"
        />
        <!-- <vxe-table-column
          :edit-render="{
            name: 'input',
            attrs: { type: 'text' }
          }"
          field="formatShow"
          title="格式化方式"
          min-width="100"
        ></vxe-table-column> -->
        <vxe-table-column
          field="inputType"
          title="前端输入框类型"
          :width="formData.reportType == '2' ? 300 : 160"
        >
          <template slot-scope="{ row, seq }">
            <div
              style="display: flex"
              v-if="formData.reportType == '2' && row.fieldEn == 'templateCode'"
            >
              <vxe-select
                v-model="row.inputType"
                placeholder="请选择"
                size="small"
                transfer
                @change="inputTypeChange(row)"
              >
                <vxe-option
                  v-for="item in inputList_templateCode"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </vxe-select>
              <SelectTable
                v-if="row.inputType === 'select_hidden'"
                ref="SelectTable"
                v-model="sqlTemplateCodeArray"
                :Columns="templateCodeColumns"
                :data="templateCodeList"
                label-field="vcTemplatEname"
                placeholder="请选择导出报告"
                size="small"
                value-field="fTemplateID"
                width="500px"
                @change="handleTemplateCodeChange(row)"
              />
              <!-- <vxe-select
                multiple
                v-model="sqlTemplateCodeArray"
                v-if="
                  row.inputType == 'select' ||
                  row.inputType == 'select_multiple'
                "
                placeholder="报告范围"
                size="small"
                transfer
                @change="handleTemplateCodeChange(row)"
              >
                <vxe-option
                  v-for="item in templateCodeList"
                  :key="item.fTemplateID"
                  :label="item.vcTemplatEname"
                  :value="item.fTemplateID"
                ></vxe-option>
              </vxe-select> -->
              <multipleSelectTable
                v-if="
                  row.inputType == 'select' ||
                  row.inputType == 'select_multiple'
                "
                ref="multipleSelectTableTemplateCode"
                v-model="sqlTemplateCodeArray"
                :Columns="templateCodeColumns"
                :data="templateCodeList"
                label-field="vcTemplatEname"
                placeholder="请选择导出报告范围"
                size="small"
                value-field="fTemplateID"
                width="500px"
                @sendData="handleTemplateCodeChange(row)"
              />
            </div>
            <div v-else style="display: flex">
              <vxe-select
                v-model="row.inputType"
                placeholder="请选择"
                size="small"
                transfer
                @change="inputTypeChange(row)"
              >
                <vxe-option
                  v-for="item in inputList"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </vxe-select>
              <el-button
                v-if="row.inputType === 'select'"
                size="mini"
                @click="editSql(row, seq, false)"
                >字典Sql
              </el-button>
              <SelectTable
                v-if="row.inputType === 'selectTable'"
                ref="SelectTable"
                v-model="row.sonEn"
                :Columns="reportColumns"
                :data="reportData"
                label-field="reportName"
                placeholder="请选择"
                size="mini"
                value-field="reportCode"
                width="500px"
              />
            </div>
          </template>
        </vxe-table-column>
        <vxe-table-column
          field="isCrud"
          title="配置信息"
          :min-width="formData.reportType == '2' ? 580 : 300"
        >
          <template slot="default" slot-scope="{ row, seq }">
            <span>
              <el-checkbox
                v-model="row.isRequired"
                style="margin-right: 30px"
                v-show="formData.reportType == '1'"
                >编辑/新增必填</el-checkbox
              >
              <el-checkbox-group
                v-model="row.isCrud"
                style="display: inline-block"
              >
                <el-checkbox label="R" v-show="formData.reportType == '1'"
                  >表头</el-checkbox
                >
                <el-checkbox label="C" v-show="formData.reportType == '1'"
                  >新增</el-checkbox
                >
                <el-checkbox label="U" v-show="formData.reportType == '1'"
                  >修改</el-checkbox
                >
                <!--                <el-checkbox label="R">查</el-checkbox>-->
                <!--                <el-checkbox label="M">查询条件</el-checkbox>-->
                <el-checkbox label="M" v-show="formData.reportType == '1'"
                  >查询</el-checkbox
                >
                <el-checkbox
                  label="Q"
                  v-if="row.isCrud && row.isCrud.indexOf('M') != -1"
                  >查询必填</el-checkbox
                >
                <el-checkbox label="S" v-if="formData.checkList.includes('S')"
                  >排序</el-checkbox
                >
              </el-checkbox-group>
              <el-tooltip
                effect="light"
                placement="top"
                content="自定义排序规则"
              >
                <div slot="content">
                  {{ row.customSortStr || "自定义排序规则" }}
                </div>
                <i
                  v-show="
                    formData.checkList.includes('S') && row.isCrud.includes('S')
                  "
                  :style="{
                    cursor: 'pointer',
                    color: row.customSortStr ? '#409EFF' : '',
                    width: '20px',
                    textAlign: 'center',
                  }"
                  class="el-icon-setting"
                  @click="openSortDialog(row, seq)"
                ></i>
              </el-tooltip>
            </span>
          </template>
        </vxe-table-column>
        <vxe-table-column
          field="isKey"
          title="是否为主键"
          width="220"
          v-if="formData.reportType == '1'"
        >
          <template slot="default" slot-scope="{ row }">
            <div style="display: flex">
              <el-checkbox
                v-model="row.isKey"
                false-label=""
                true-label="1"
                @change="(value) => isKeyChange(value, row)"
                >主键
              </el-checkbox>
              <div style="width: 100px; padding-left: 10px">
                <vxe-select
                  v-show="row.isKey === '1'"
                  v-model="row.isAutoIncrement"
                  placeholder="请选择"
                  size="small"
                  transfer
                >
                  <vxe-option label="不自增" value="0">不自增</vxe-option>
                  <vxe-option label="JAVA自增" value="1">JAVA自增</vxe-option>
                  <vxe-option label="库自增" value="2">库自增</vxe-option>
                </vxe-select>
              </div>
              <!-- <el-checkbox v-show="row.isKey === '1'" v-model="row.isAutoIncrement" false-label="0"
                           true-label="1">JAVA自增</el-checkbox>
              <el-checkbox v-show="row.isKey === '1'" v-model="row.isAutoIncrement" false-label="0"
              true-label="2">库自增</el-checkbox> -->
            </div>
          </template>
        </vxe-table-column>
      </vxe-table>
    </div>

    <div class="form_box">
      <el-form
        ref="formData"
        :model="formData"
        :rules="rules"
        class="demo-form-inline form_inline_search report_config_form"
        label-width="100px"
      >
        <el-form-item label="页面名称" prop="reportName">
          <el-input v-model="formData.reportName" clearable></el-input>
        </el-form-item>
        <el-form-item label="添加到菜单" prop="menuName">
          <el-input
            v-model="formData.menuName"
            clearable
            @focus="selectMenu"
            @clear="clearMenu"
          >
          </el-input>
          <el-tooltip effect="light" placement="top">
            <div slot="content">将作为选择菜单的子菜单</div>
            <i class="el-icon-info" style="color: #ccc"></i>
          </el-tooltip>
        </el-form-item>
        <el-form-item
          label="操作权限"
          prop="checkList"
          style="position: relative"
          v-show="formData.reportType == '1'"
        >
          <el-checkbox-group
            v-model="formData.checkList"
            @change="checkListChange"
          >
            <el-checkbox label="C">新增</el-checkbox>
            <el-checkbox label="D">删除</el-checkbox>
            <el-checkbox label="B">批量删除</el-checkbox>
            <el-checkbox label="U">修改</el-checkbox>
            <el-checkbox label="E">导出excel</el-checkbox>
            <el-checkbox label="T">导出txt</el-checkbox>
            <el-checkbox label="S">排序</el-checkbox>
          </el-checkbox-group>
          <span
            v-if="formData.checkList.includes('S')"
            style="position: absolute; left: 630px; top: 0"
          >
            <el-input
              v-model="formData.defaultSortStr"
              size="small"
              placeholder="默认排序字段(可不填)"
              clearable
            ></el-input>
            <el-tooltip effect="light" placement="top">
              <div slot="content" style="line-height: 1.5">
                <p>示例：</p>
                <p>VC_USERNAME</p>
                <p>VC_USERNAME desc</p>
                <p>VC_USERNAME asc</p>
              </div>
              <i class="el-icon-info" style="color: #ccc"></i>
            </el-tooltip>
          </span>
        </el-form-item>
        <el-form-item
          label="是否分页"
          prop="isPage"
          v-show="formData.reportType == '1'"
        >
          <el-checkbox v-model="formData.isPage">是否分页</el-checkbox>
        </el-form-item>
        <el-form-item
          label="是否默认查询"
          prop="isSelect"
          v-show="formData.reportType == '1'"
        >
          <el-checkbox v-model="formData.isSelect">是否默认查询</el-checkbox>
        </el-form-item>
        <el-form-item
          label="增删改SQL"
          prop="checkList"
          v-show="formData.reportType == '1'"
        >
          <el-switch
            v-model="switchValue"
            :disabled="switchDisabled"
          ></el-switch>
          <el-tooltip effect="light" placement="top">
            <div slot="content">需填写增/删/改SQL时打开开关</div>
            <i class="el-icon-info" style="color: #ccc"></i>
          </el-tooltip>
        </el-form-item>
        <span v-if="switchValue && formData.reportType == '1'">
          <el-form-item
            v-if="formData.checkList.includes('C')"
            label="新增sql"
            prop="addSql"
          >
            <el-input
              v-model="formData.addSql"
              :rows="6"
              placeholder="请输入内容"
              type="textarea"
            ></el-input>
            <el-tooltip effect="light" placement="top">
              <div slot="content">
                自定义新增SQL，可不填（不填写将由后端默认生成） <br />
                若勾选页面顶部【不解析SQL】，则必须自己填写新增SQL
              </div>
              <i class="el-icon-info" style="color: #ccc"></i>
            </el-tooltip>
          </el-form-item>
          <el-form-item
            v-if="formData.checkList.includes('D')"
            label="删除sql"
            prop="deleteSql"
          >
            <el-input
              v-model="formData.deleteSql"
              :rows="6"
              placeholder="请输入内容"
              type="textarea"
            ></el-input>
            <el-tooltip effect="light" placement="top">
              <div slot="content">
                自定义删除SQL，可不填（不填写将由后端默认生成） <br />
                若勾选页面顶部【不解析SQL】，则必须自己填写删除SQL
              </div>
              <i class="el-icon-info" style="color: #ccc"></i>
            </el-tooltip>
          </el-form-item>
          <el-form-item
            v-if="formData.checkList.includes('U')"
            label="修改sql"
            prop="updateSql"
          >
            <el-input
              v-model="formData.updateSql"
              :rows="6"
              placeholder="请输入内容"
              type="textarea"
            ></el-input>
            <el-tooltip effect="light" placement="top">
              <div slot="content">
                自定义修改SQL，可不填（不填写将由后端默认生成） <br />
                若勾选页面顶部【不解析SQL】，则必须自己填写修改SQL
              </div>
              <i class="el-icon-info" style="color: #ccc"></i>
            </el-tooltip>
          </el-form-item>
        </span>
        <div>
          <el-button
            :loading="buildLoading"
            size="medium"
            type="primary"
            @click="Submit"
            >生成配置</el-button
          >
        </div>
      </el-form>
    </div>
    <el-dialog :visible.sync="showEdit" title="字典Sql" width="30%">
      <div v-if="isTemplateCode">
        <multipleSelectTable
          v-if="
            tableData &&
            tableData[rowIndex] &&
            tableData[rowIndex].inputType == 'select_multiple'
          "
          style="margin-bottom: 10px"
          ref="multipleSelectTableTemplateCode"
          v-model="sqlTemplateCodeArray"
          :Columns="templateCodeColumns"
          :data="templateCodeList"
          label-field="vcTemplatEname"
          placeholder="请选择导出报告范围"
          size="small"
          value-field="fTemplateID"
          width="500px"
          @sendData="handleTemplateCodeChange"
        />
        <SelectTable
          v-else
          style="margin-bottom: 10px"
          ref="SelectTableTemplateCode"
          v-model="sqlTemplateCodeArray"
          :Columns="templateCodeColumns"
          :data="templateCodeList"
          label-field="vcTemplatEname"
          placeholder="请选择导出报告范围"
          size="small"
          value-field="fTemplateID"
          width="500px"
          @change="handleTemplateCodeChange"
        />
      </div>
      <div
        style="display: flex; align-items: center; padding-bottom: 10px"
        v-else
      >
        <span>字典快捷选择：</span>
        <SelectTable
          ref="SelectTable"
          v-model="edimType"
          :Columns="Columns"
          :data="edimTypeList"
          label-field="dimTypename"
          placeholder="请选择"
          size="small"
          value-field="dimType"
          width="500px"
          @change="edimTypeChange"
        />
      </div>
      <el-input
        v-model="dicSql"
        :disabled="sql_disabled"
        :rows="8"
        placeholder="请输入内容"
        type="textarea"
      ></el-input>
      <div style="margin-top: 10px">
        <el-button
          :loading="sqlTestLoading"
          icon="el-icon-video-play"
          type="primary"
          @click="sqlTest"
          >SQL执行测试
        </el-button>
        <span>测试结果：</span>
        <el-select v-model="dicValue" placeholder="请选择" size="small">
          <el-option
            v-for="item in dicList"
            :key="item.DIM_CDE"
            :label="item.DIM_NME"
            :value="item.DIM_CDE"
          ></el-option>
        </el-select>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showEdit = false">取 消</el-button>
        <el-button type="primary" @click="submitEvent">确 定</el-button>
      </span>
    </el-dialog>
    <el-dialog
      :visible.sync="sortDialogVisible"
      title="自定义排序规则"
      width="30%"
    >
      <div>
        <div style="line-height: 1.5">
          <p>具体根据数据库语法编写，字段名称替换为$1 正序倒序替换为$2</p>
          <p>例如：oracle数据库中，需要把字段userName空的放在最后</p>
          <p>
            对应示例：userName asc nulls last 文本框中输入：<span
              style="color: #409eff"
              >$1 $2 nulls last</span
            >
          </p>
          <p style="color: #e6a23c">注：不需要写order by，最后不需要标点符号</p>
        </div>
        <el-input
          v-model="sortDialogData.customSortStr"
          :rows="8"
          placeholder="请输入内容"
          type="textarea"
        ></el-input>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="sortDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitSortEvent">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 菜单位置选择 -->
    <el-dialog :visible.sync="menu_show" title="菜单" width="30%">
      <div v-if="menu_show">
        <el-tree
          ref="menuTree"
          v-loading="menuTree_loading"
          :check-strictly="true"
          :data="menuData"
          :indent="25"
          :props="defaultProps"
          node-key="actionid"
          show-checkbox
          @check="handleCheck"
        >
        </el-tree>
      </div>
      <!-- <span slot="footer" class="dialog-footer">
        <el-button @click="menu_show = false">取 消</el-button>
        <el-button type="primary" @click="menuChoose">确 定</el-button>
      </span> -->
    </el-dialog>
  </div>
</template>
<script>
import SelectTable from "./components/SelectTable";
import multipleSelectTable from "./components/multipleSelectTable";
import commonfun from "./javascript";
import pageApi from "./api";
import _ from "lodash";
import { createTreeDataExternLink } from "@/filters/index";

export default {
  components: { SelectTable, multipleSelectTable },
  name: "DdReportConfig",
  filters: {
    modeStr(val) {
      if (val === "edit") {
        return "编辑模式";
      } else {
        return "新增模式";
      }
    },
  },
  data() {
    return {
      // 导出报告范围
      sqlTemplateCodeArray: [],
      //  行标志位判断是否是 templateCode
      isTemplateCode: false,
      // 报告下拉编码
      reportColumns: [
        {
          label: "编码",
          prop: "reportCode",
        },
        {
          label: "名称",
          prop: "reportName",
        },
      ],
      reportData: [],

      // 当前模式
      mode: "add",
      version: "",
      versionOption: [],
      reportConfig: null,

      // 编辑行
      rowIndex: 0,

      sqlText: "",
      runSqlLoading: false,
      check: false,

      tableLoading: false,
      tableData: [],
      tableKey: "tableKey",
      fieldTypeArr: [
        { label: "字符串", value: "S" },
        { label: "日期", value: "D" },
        { label: "数值", value: "N" },
        // { label: "VARCHAR2", value: "S" },
        // { label: "DATE", value: "D" },
        // { label: "NUMBER", value: "N" }
      ],
      inputList_templateCode: [
        {
          label: "下拉框(单选)",
          value: "select",
        },
        {
          label: "隐藏",
          value: "select_hidden",
        },
        {
          label: "下拉框(多选)",
          value: "select_multiple",
        },
      ],
      inputList: [
        { label: "文本框", value: "input" },
        { label: "文本框(多行)", value: "textArea" },
        {
          label: "下拉框",
          value: "select",
        },
        {
          label: "下拉框(表格)",
          value: "selectTable",
        },
        { label: "日期框", value: "date" },
      ],
      tableEn: "", // 表英文名
      tableCn: "", // 表中文名
      isComplex: "0", // 是否是
      isCustom: true, // 是否增删改SQL
      isPage: 1, // 是否分页默认分页

      // 配置下拉字典弹窗
      showEdit: false,
      edimType: "",
      edimTypeList: [],
      Columns: [
        { label: "分类编码", prop: "dimType" },
        { label: "分类名称", prop: "dimTypeName" },
      ],
      dicSql: "",
      sql_disabled: false,
      sqlTestLoading: false,
      dicList: [],
      dicValue: "",

      // 排序弹窗
      sortDialogVisible: false,
      sortDialogData: {
        customSortStr: "",
        seq: 0,
      },

      // 菜单弹窗
      menuId: "",
      reportAction: {},
      menu_show: false,
      menuTree_loading: false,
      menuData: [],
      menuDataArray: [],
      defaultProps: {
        children: "children",
        label: "vcactionname",
        disabled: (data, node) => {
          if (
            data.vcremark == "" ||
            data.vcremark == "views/routerPage/index"
          ) {
            return false;
          } else {
            return true;
          }
        },
      },

      formData: {
        // 页面类型 1:RS补录 2:RS导出
        reportType: "1",
        // 导出报告Code - 导出报告时必填
        templateCode: "",
        reportName: "",
        menuName: "",
        menuId: "",
        checkList: ["F", "R"],
        defaultSortStr: "",
        addSql: "",
        deleteSql: "",
        updateSql: "",
        isPage: true,
        isSelect: true,
      },
      // 导出报告Code列表
      templateCodeList: [],
      templateCodeColumns: [
        { label: "编码", prop: "fTemplateID" },
        { label: "名称", prop: "vcTemplatEname" },
      ],
      rules: {
        reportName: {
          required: true,
          message: "请填写页面名称",
          trigger: "change",
        },
        menuName: {
          required: false,
          message: "请选择添加的菜单位置",
          trigger: "change",
        },
        addSql: { required: false, message: "", trigger: "change" },
        deleteSql: { required: false, message: "", trigger: "change" },
        updateSql: { required: false, message: "", trigger: "change" },
      },
      switchValue: false, // 增删改sql
      switchDisabled: false, //是否禁用
      buildLoading: false, //生成配置按钮loading
    };
  },
  created() {
    this.getEdimTypeList();

    // 获取 selectTable 所有的下拉数据
    this.getSelectTable();
    this.templateCodeChange();
  },
  activated() {
    console.log(this.$route.query);
    if (this.$route.query && this.$route.query.reportConfig) {
      let reportConfig = this.$route.query.reportConfig;
      if (reportConfig && reportConfig.versionData) {
        this.reportConfig = reportConfig;
        this.mode = "edit";
        // 初始化页面
        this.initReport(reportConfig.versionData);
      }
    } else {
      this.initPage();
    }
  },
  methods: {
    /**
     * 导出报告Code改变
     * @param {string} val - 导出报告Code
     */
    handleTemplateCodeChange(row = null) {
      if (!row || row.inputType == "select_hidden") {
        this.formData.templateCode = this.sqlTemplateCodeArray;
        row.dicSql = "";
        return;
      }
      // 判断是否是字符串还是数组
      this.formData.templateCode = this.sqlTemplateCodeArray.toString();
      this.dicSql = `select t.f_templateid as DIM_CDE,t.vc_templatename as DIM_NME from cr_template_info t where t.f_templateid in (`;
      this.sqlTemplateCodeArray.forEach((item, index) => {
        this.dicSql += `'${item}'`;
        if (index < this.sqlTemplateCodeArray.length - 1) {
          this.dicSql += ",";
        }
      });
      this.dicSql += `)`;
      row.dicSql = this.dicSql;
    },
    /**
     * 报告类型改变
     * @param {string} val - 报告类型
     */
    reportTypeChange(val) {
      if (val == "1") {
        this.formData.templateCode = "";
      }

      let findObj = this.tableData.find(
        (item) => item.fieldEn == "templateCode"
      );
      if (!findObj) {
        const record = {
          fieldCn: "导出报告Code",
          fieldEn: "templateCode",
          fieldLength: "",
          sonEn: "",
          inputType: "select",
          fieldType: "S",
          isCrud: ["C", "U", "R", "M"],
          isKey: "",
          isAutoIncrement: "",
          customSortStr: "",
          _XID: commonfun.getUUID("row"),
        };
        this.$nextTick(() => {
          const { row: newRow } = this.$refs.vxeTable.insertAt(record, -1);
          this.$refs.vxeTable.setActiveCell(newRow);
          this.tableData = this.$refs.vxeTable.getTableData().tableData;
        });
      } else {
        if (this.formData.reportType == "1") {
          if (findObj.inputType == "select_hidden") {
            findObj.inputType = "select";
            findObj.dicSql = "";
            findObj.isCrud = ["C", "U", "R", "M"];
          }
        }
      }
    },
    /**
     * 导出报告Code改变
     * @param {string} val - 导出报告Code
     */
    templateCodeChange(val) {
      let params = {
        limit: 99999999,
        offset: 0,
      };
      pageApi.getTemplateCodeList(params).then((res) => {
        let { status, data } = res;
        if (status == 200) {
          this.templateCodeList = data.rows;
        } else {
          this.templateCodeList = [];
        }
      });
    },
    // 获取
    getSelectTable(flag) {
      const params = {
        limit: 99999999,
        offset: 0,
        pageNum: 1,
      };
      pageApi.getSelectTableData(params).then((res) => {
        this.tableLoading = false;
        const { data } = res;
        if (data.rows && data.rows.length > 0) {
          data.rows.forEach((item) => {
            item.statusBoolean = item.status === "1";
          });
        }
        this.reportData = data.rows;
      });
    },

    // 删除 当前版本
    handleDelCurrentVersion() {
      // 判断 当前的version数组 是否只有一个
      if (this.versionOption && this.versionOption.length > 1) {
        this.$confirm("此操作将永久删除该数据, 是否继续?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
          confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
        })
          .then(() => {
            let reportObj = JSON.parse(this.reportConfig.versionData);
            let params = {
              reportCode: reportObj.reportCode,
              version: reportObj.version,
            };
            pageApi.deleteVersion(params).then(async (res) => {
              // 获取最新的versionOption数组
              if (res.status === 200) {
                this.$message.closeAll();
                this.$message.success("删除当前分支成功");
                await this.getAllVersion();
                // 设置 第一个元素 为初始化元素
                if (this.versionOption && this.versionOption.length > 0) {
                  this.mode = "edit";
                  this.reportConfig = this.versionOption[0];
                  this.initReport(this.versionOption[0].versionData);
                }
              }
            });
          })
          .catch(() => {
            this.$message({
              type: "info",
              message: "已取消删除",
            });
          });
      }
    },

    // 切换版本处理函数
    versionChange(val) {
      let findObj = this.versionOption.find((item) => item.version === val);
      if (findObj) {
        this.reportConfig = findObj;
        this.initReport(findObj.versionData);
      }
    },
    // 获取当前报告的所有版本号
    getAllVersion() {
      return new Promise((resolve, reject) => {
        let reportObj = JSON.parse(this.reportConfig.versionData);
        let params = {
          reportCode: reportObj.reportCode,
        };
        pageApi
          .getVersionList(params)
          .then((res) => {
            let { data } = res.data;
            this.versionOption = data;
            resolve();
          })
          .catch((err) => {
            this.versionOption = [];
            resolve();
          });
      });
    },

    // 根据传参回填 当前页面的 值
    async initReport(versionData) {
      // 初始化信息
      this.initPage();

      // 获取所有的版本信息
      this.getAllVersion();

      // 回填信息
      let reportObj = JSON.parse(versionData);

      this.version = reportObj.version;
      this.tableEn = reportObj.tableEn || "";

      this.sqlText = reportObj.searchSql;
      this.formData.checkList = reportObj.crudEnable.split("");
      if (reportObj.crudEnable.includes("S")) {
        this.formData.defaultSortStr = reportObj.defaultSortStr || "";
      }
      this.formData.reportName = reportObj.reportAction.actionName;
      this.formData.addSql = reportObj.addSql || "";
      this.formData.deleteSql = reportObj.delSql || "";
      this.formData.updateSql = reportObj.updateSql || "";
      this.formData.isPage = reportObj.isPage == 1 ? true : false;

      this.isComplex = reportObj.isComplex;
      this.isCustom = reportObj.isCustom;
      if (reportObj.isCustom === "true" || reportObj.isCustom === true) {
        this.switchValue = true;
      } else {
        this.switchValue = false;
      }
      this.menuId = reportObj.reportAction.actionPId;
      this.reportAction = reportObj.reportAction;
      this.formData.menuId = this.menuId;

      // 设置报告类型
      if (reportObj && reportObj.customMap && reportObj.customMap.reportType) {
        this.formData.reportType = reportObj.customMap.reportType;
      } else {
        this.formData.reportType = "1";
      }

      if (
        reportObj &&
        reportObj.customMap &&
        reportObj.customMap.templateCode
      ) {
        this.formData.templateCode = reportObj.customMap.templateCode;
      } else {
        this.formData.templateCode = "";
      }

      // 获取所有的菜单信息
      if (this.menuDataArray && this.menuDataArray.length === 0) {
        await this.getMenuData();
      }
      // 回填 菜单名称
      let findObj = this.menuDataArray.find(
        (item) => item.actionid == this.menuId
      );
      if (findObj) {
        this.formData.menuName = findObj.vcactionname;
      }

      this.check = reportObj.check;

      //转换 tableData
      let cloneTableData = _.cloneDeep(reportObj.tableFieldList);
      cloneTableData.forEach((item) => {
        item.isKey = item.isKey === 1 ? "1" : "0";
        item.isCrud = item.isCrud.split("");
        item.inputType = item.fieldInputType;
        if (item.isRequired) {
          item.isRequired = true;
        } else {
          item.isRequired = false;
        }
      });
      this.tableData = cloneTableData;

      // 如果 导出报告Code 不为空 则 设置 导出报告Code 为 导出报告Code 的 值
      if (this.formData.reportType == "2") {
        let findTemplateCodeItem = this.tableData.find(
          (item) => item.fieldEn == "templateCode"
        );
        if (!findTemplateCodeItem) {
          const record = {
            fieldCn: "导出报告Code",
            fieldEn: "templateCode",
            fieldLength: "",
            sonEn: "",
            inputType: "select_hidden",
            fieldType: "S",
            isCrud: [],
            isKey: "",
            isAutoIncrement: "",
            customSortStr: "",
            _XID: commonfun.getUUID("row"),
          };
          this.sqlTemplateCodeArray =
            this.formData.templateCode.toString() || "";
          this.$nextTick(() => {
            const { row: newRow } = this.$refs.vxeTable.insertAt(record, -1);
            this.$refs.vxeTable.setActiveCell(newRow);
            this.tableData = this.$refs.vxeTable.getTableData().tableData;
          });
        } else {
          if (
            findTemplateCodeItem.inputType == "select_multiple" ||
            findTemplateCodeItem.inputType == "select"
          ) {
            this.sqlTemplateCodeArray =
              this.formData.templateCode.toString().split(",") || "";
            if (this.sqlTemplateCodeArray.length == 0) {
              this.sqlTemplateCodeArray =
                this.formData.templateCode.toString() || "";
            }
          } else {
            this.sqlTemplateCodeArray =
              this.formData.templateCode.toString() || "";
          }
        }
      }
    },

    // 初始化页面 清空数据
    initPage() {
      this.sqlText = "";
      this.check = "";
      this.tableData = [];
      this.$refs["formData"].resetFields();
      this.formData.reportType = "1";
    },

    isKeyChange(value, row) {
      if (row.isKey === "1") {
        row.isAutoIncrement = "0";
      } else {
        row.isAutoIncrement = "";
      }
    },

    getEdimTypeList() {
      pageApi.edimTypeList().then((res) => {
        const { data, status } = res.data;
        if (status === 200 && data) {
          this.edimTypeList = data || [];
        }
      });
    },

    runSql() {
      if (this.sqlText == "") {
        this.$message.closeAll("执行的SQL语句不能为空");
        return;
      }
      // 定义要发送的数据

      let formData = new FormData();
      formData.append("selectSql", this.sqlText);

      pageApi.execSQL(formData).then((res) => {
        const { status, data, message } = res.data;
        if (status === 200) {
          this.$message.closeAll();
          this.$message.success("执行SQL成功");

          if (data && data.length) {
            this.tableCn = data[0].tableCn;
            this.tableEn = data[0].tableEn;
            this.isComplex =
              data[0].isComplex == undefined ? "0" : data[0].isComplex;
            if (this.isComplex == "1") {
              this.switchValue = false; // 复杂sql 设置 增删改SQL为 禁用状态
              this.switchDisabled = true;
            } else {
              this.switchValue = false;
              this.switchDisabled = false;
            }
          }
          data.forEach((item) => {
            item.isCrud = ["C", "U", "R"];
            item.isKey = "";
            item.isAutoIncrement = "";
            !item.fieldType && (item.fieldType = "S");
            if (item.fieldType == "D") {
              item.inputType = "date";
            } else {
              item.inputType = "input";
            }
            item.searchType = "1";
            item.isRequired = false;
            item.customSortStr = "";
            if (item.fieldCn == undefined) {
              item.fieldCn = "";
            }
          });
          this.tableData = data;
        } else {
          this.$message.closeAll();
          this.$message.error(message || "执行SQL成功");
        }
      });
    },

    // 列表新增
    insertEvent() {
      const record = {
        fieldCn: "",
        fieldEn: "",
        fieldLength: "",
        sonEn: "",
        inputType: "input",
        fieldType: "S",
        isCrud:
          this.formData.reportType == "1"
            ? ["C", "U", "R"]
            : ["C", "U", "R", "M"],
        isKey: "",
        isAutoIncrement: "",
        customSortStr: "",
        _XID: commonfun.getUUID("row"),
      };
      this.$nextTick(() => {
        const { row: newRow } = this.$refs.vxeTable.insertAt(record, -1);
        this.$refs.vxeTable.setActiveCell(newRow);
        this.tableData = this.$refs.vxeTable.getTableData().tableData;
      });
    },
    // 列表移除
    removeEvent() {
      const selectRecords = this.$refs.vxeTable.getCheckboxRecords();
      if (selectRecords.length) {
        this.$confirm("您确定要删除选中的数据吗?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
          confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
        })
          .then(() => {
            let foundItem = this.tableData.find(
              (item) => item.fieldEn === "templateCode"
            );
            this.$refs.vxeTable.removeCheckboxRow();
            if (foundItem && this.formData.reportType == "2") {
              this.tableData = [foundItem];
            } else {
              this.tableData = this.$refs.vxeTable.getTableData().tableData;
            }
          })
          .catch(() => {
            this.$message.closeAll();
            this.$message({
              type: "info",
              message: "已取消",
            });
          });
      } else {
        this.$message.closeAll();
        this.$message({ type: "error", message: "请至少选择一条数据" });
      }
    },
    fieldTypeChange({ row }) {
      row.formatShow = "";
      if (row.fieldType === "S") {
        row.inputType = "input";
      }
      if (row.fieldType === "D") {
        row.inputType = "date";
      }
      if (row.fieldType === "N") {
        row.inputType = "input";
      }
    },

    // vxe-table 表格样式
    cellClassName({}) {
      return "vxe-cell-class-name";
    },
    headerCellClassName({}) {
      return "vxe-header-cell-class-name";
    },

    inputTypeChange(row) {
      row.searchType = "1";
      row.formatShow = "";
      if (row.fieldEn == "templateCode") {
        if (row.inputType === "select_hidden") {
          this.sqlTemplateCodeArray = "";
          row.isCrud = [];
        } else {
          if (row.inputType === "select") {
            this.sqlTemplateCodeArray = "";
          } else {
            this.sqlTemplateCodeArray = [];
          }
          row.isCrud = ["C", "U", "R", "M"];
        }
      }

      if (
        row.inputType === "input" ||
        row.inputType === "select" ||
        row.inputType === "selectTable" ||
        row.inputType === "select_hidden"
      ) {
        row.fieldType = "S";
      }
      if (row.inputType === "date") {
        row.fieldType = "D";
        row.formatShow = "yyyy-MM-dd";
      }
    },

    // 字典测试弹窗
    sqlTest() {
      this.$message.closeAll();
      if (!this.dicSql) {
        return this.$message({
          type: "error",
          message: "请填写SQL！",
        });
      }
      let params = {
        dicSql: this.dicSql,
      };
      this.sqlTestLoading = true;
      this.dicList = [];
      pageApi
        .checkDicSql(params)
        .then((res) => {
          if (res.data.status == 0 && res.data.message == "success") {
            this.dicList = res.data.data;
            this.$message.success("执行成功");
          } else {
            this.$message({
              type: "error",
              message: res.data.message || "执行失败！",
            });
            this.dicList = [];
          }
          this.sqlTestLoading = false;
        })
        .catch((err) => {
          this.$message({
            type: "error",
            message: "执行失败！",
          });
          this.dicList = [];
          this.sqlTestLoading = false;
        });
    },
    edimTypeChange(data) {
      let sqlStr = `select DIM_CDE ,DIM_NME  from E_DIM_PORTAL WHERE dim_type = '${data.dimType}' and DIM_STATUS  = '1'`;
      this.dicSql = sqlStr;
    },
    // 字典sql编辑确认
    submitEvent() {
      this.$refs.vxeTable.getTableData().tableData[this.rowIndex].dicSql =
        this.dicSql;
      this.showEdit = false;
    },
    // 字典sql编辑
    editSql(row, seq, flag) {
      if (this.formData.reportType == "2" && row.fieldEn == "templateCode") {
        this.isTemplateCode = true;
      } else {
        this.isTemplateCode = false;
      }
      if (row.inputType == "select_multiple") {
        this.sqlTemplateCodeArray = [];
      } else {
        this.sqlTemplateCodeArray = "";
      }
      this.sql_disabled = flag;
      this.rowIndex = seq - 1;
      this.showEdit = true;
      this.dicSql = row.dicSql || "";
      this.dicList = [];
      this.dicValue = "";
      this.edimType = "";
    },
    // 打开排序弹窗
    openSortDialog(row, seq) {
      this.sortDialogVisible = true;
      this.sortDialogData.customSortStr = row.customSortStr || "";
      this.sortDialogData.seq = seq;
      // this.$refs[`sortInput${seq}`].blur();
    },
    submitSortEvent() {
      this.$refs.vxeTable.getTableData().tableData[
        this.sortDialogData.seq - 1
      ].customSortStr = this.sortDialogData.customSortStr || "";
      this.sortDialogVisible = false;
    },

    // 菜单点击
    handleCheck(a, b) {
      // console.log(a);
      if (b.checkedKeys.length > 0) {
        this.$refs.menuTree.setCheckedKeys([a.actionid]);
        this.formData.menuName = a.vcactionname || "";
        this.menu_show = false;
        this.menuId = a.actionid;
      }
    },
    // 菜单位置选择
    selectMenu() {
      this.getMenuData();
      this.menu_show = true;
    },
    clearMenu() {
      this.menuId = "";
      this.formData.menuName = "";
    },
    // 获取菜单数据
    getMenuData() {
      return new Promise((resolve, reject) => {
        this.menuData = [];
        this.menuTree_loading = true;
        pageApi
          .getMenu()
          .then((res) => {
            // if (res.data.status == 200 && res.data.message == '操作成功') {
            if (res.data.status == 0) {
              let treeList = res.data.data;
              this.menuDataArray = _.cloneDeep(treeList);
              // this.menuData = commonfun.converTreeData(treeList, 0, 'actionPId', 'actionId', 'actionId').data
              this.menuData = createTreeDataExternLink(treeList, 0, 0);
              this.menuTree_loading = false;
            } else {
              this.menuData = [];
              this.menuDataArray = [];
              this.menuTree_loading = false;
              this.$message({
                type: "error",
                message: res.data.message || "菜单加载失败！",
              });
            }
            resolve();
          })
          .catch((err) => {
            this.menuData = [];
            this.menuTree_loading = false;
            resolve();
          });
      });
    },
    // 操作权限change
    checkListChange(val) {
      if (val.includes("S")) {
        this.tableData.forEach((item) => {
          item.isCrud.push("S");
          item.customSortStr = "";
        });
      } else {
        this.formData.defaultSortStr = "";
        this.tableData.forEach((item) => {
          item.isCrud = item.isCrud.filter((item) => item != "S");
          item.customSortStr = "";
        });
      }
      this.$forceUpdate();
    },

    //生成配置
    Submit() {
      if (!this.sqlText && this.formData.reportType == "1") {
        this.$message.closeAll();
        this.$message({
          type: "error",
          message: "请填写查询sql！",
        });
        return false;
      }

      // 校验 是否有主键
      let checkList = this.formData.checkList;
      if (checkList.includes("D") || checkList.includes("U")) {
        let tableData = this.$refs.vxeTable.getTableData().tableData;
        let oo = tableData.filter((item) => {
          return item.isKey;
        });
        if (!oo.length) {
          this.$message.closeAll();
          this.$message({
            type: "error",
            message: "必须勾选一个字段作为主键！",
          });
          return false;
        }
      }

      // 校验 表格 非空字段
      let tableData = this.$refs.vxeTable.getTableData().tableData;
      for (let i = 0; i < tableData.length; i++) {
        let temp = tableData[i];
        if (temp.fieldEn == "") {
          let index = i + 1;
          this.$message.closeAll();
          this.$message.warning(`第${index}行字段英文名为空，请按照提示修改`);
          return;
        }
        if (temp.fieldCn == "") {
          let index = i + 1;
          this.$message.closeAll();
          this.$message.warning(`第${index}行字段中文名为空，请按照提示修改`);
          return;
        }
      }

      this.$refs["formData"].validate((valid) => {
        if (valid) {
          this.buildConfig();
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    // 生成配置
    buildConfig() {
      if (this.formData.reportType == "2") {
        this.tableEn = "dual";
        this.tableCn = "dual";
        let findTemplateCodeItem = this.tableData.find(
          (item) => item.fieldEn == "templateCode"
        );
        if (!findTemplateCodeItem) {
          this.$message.closeAll();
          this.$message.warning("缺少templateCode字段，请手动添加");
          return;
        }
        if (findTemplateCodeItem) {
          if (findTemplateCodeItem.inputType !== "select_hidden") {
            if (!findTemplateCodeItem.dicSql || !this.sqlTemplateCodeArray) {
              this.$message.closeAll();
              this.$message.warning("请选择templateCode字段对应的报告范围");
              return;
            }
          } else {
            if (!this.sqlTemplateCodeArray) {
              this.$message.closeAll();
              this.$message.warning("请选择templateCode字段对应的报告");
              return;
            }
          }
        }
      }
      if (
        this.tableEn == "" ||
        this.tableEn == undefined ||
        this.tableEn == null
      ) {
        this.$message.closeAll();
        this.$message.warning("表英文名缺失");
        return;
      }

      let tableData = this.$refs.vxeTable.getTableData().tableData;
      let UUID = commonfun.getUUID("id");
      let formdata = JSON.parse(JSON.stringify(this.formData));
      let params = {};
      params.reportName = formdata.reportName;
      params.tableEn = this.tableEn;
      params.tableCn = this.tableCn;
      params.crudEnable = _.cloneDeep(formdata.checkList);
      params.crudEnable = params.crudEnable.filter((item) => item !== "A");

      if (this.formData.isSelect) {
        params.crudEnable.push("A");
      }
      params.crudEnable = params.crudEnable.join("");
      if (params.crudEnable.includes("S")) {
        params.defaultSortStr = formdata.defaultSortStr;
      } else {
        params.defaultSortStr = "";
      }
      if (this.switchValue) {
        params.addSql = formdata.addSql;
        params.delSql = formdata.deleteSql;
        params.updateSql = formdata.updateSql;
      } else {
        params.addSql = formdata.addSql;
        params.delSql = formdata.deleteSql;
        params.updateSql = formdata.updateSql;
      }

      params.searchSql = this.sqlText;

      // 判断 查询字符串里面 是否包含as
      if (this.isComplex != "1") {
        if (params.searchSql.toLowerCase().includes(` as `)) {
          params.isComplex = "1";
          params.addSql = formdata.addSql;
          params.delSql = formdata.deleteSql;
          params.updateSql = formdata.updateSql;
        } else {
          params.isComplex = "0";
        }
      } else {
        if (!params.searchSql.toLowerCase().includes(` as `)) {
          params.isComplex = "0";
          params.addSql = "";
          params.delSql = "";
          params.updateSql = "";
        } else {
          params.isComplex = this.isComplex;
        }
      }
      params.isCustom = this.switchValue;
      if (formdata.isPage) {
        params.isPage = 1;
      } else {
        params.isPage = 0;
      }
      params.tableFieldList = _.cloneDeep(tableData);

      for (let i = 0; i < params.tableFieldList.length; i++) {
        params.tableFieldList[i].isKey =
          params.tableFieldList[i].isKey == "1" ? 1 : 0;
        params.tableFieldList[i].isCrud = params.tableFieldList[
          i
        ].isCrud.filter((item) => item != "B");
        params.tableFieldList[i].isCrud = params.tableFieldList[
          i
        ].isCrud.filter((item) => item != "P");
        if (params.tableFieldList[i].isKey === 1) {
          params.tableFieldList[i].isCrud.push("B");
          if (
            params.tableFieldList[i].isAutoIncrement === "1" ||
            params.tableFieldList[i].isAutoIncrement === "2"
          ) {
            params.tableFieldList[i].isCrud.push("P");
          }
        }

        if (params.tableFieldList[i].isRequired == true) {
          params.tableFieldList[i].isRequired = 1;
        } else {
          params.tableFieldList[i].isRequired = 0;
        }

        params.tableFieldList[i].isCrud = params.tableFieldList[i].isCrud
          .toString()
          .replace(/,/g, "");

        params.tableFieldList[i].fieldOrder = i + 1;
        params.tableFieldList[i].fieldInputType =
          params.tableFieldList[i].inputType;
        params.tableFieldList[i].isAutoIncrement =
          params.tableFieldList[i].isAutoIncrement || "";
      }

      // 菜单信息
      params.reportAction = {
        ...this.reportAction,
        actionName: formdata.reportName || "",
        actionPId: Number(this.menuId) || null,
        reportType: this.formData.reportType,
        templateCode: this.formData.templateCode,
      };

      params.check = this.check;

      if (this.formData.reportType == "1") {
        params.reportAction.remark = "views/ddrs/currencyReport";
      } else {
        params.reportAction.remark = "views/ddrs/exportFile/index";
      }

      // 编辑模式
      if (this.mode === "edit") {
        let reportObj = JSON.parse(this.reportConfig.versionData);
        params.reportCode = reportObj.reportCode;
        if (this.formData.reportType == "1") {
          params.reportAction.url =
            "reportPage?reportCode=" + params.reportCode;
        } else {
          let findTemplateCodeItem = this.tableData.find(
            (item) => item.fieldEn == "templateCode"
          );
          if (
            findTemplateCodeItem &&
            findTemplateCodeItem.inputType == "select_hidden"
          ) {
            params.reportAction.url =
              "reportPage?reportCode=" +
              params.reportCode +
              "&templateCode=" +
              formdata.templateCode;
          } else {
            params.reportAction.url =
              "reportPage?reportCode=" + params.reportCode + "&templateCode=";
          }
        }
      } else {
        // 新增模式
        if (this.formData.reportType == "1") {
          params.reportAction.url = "reportPage?templateCode=" + "&reportCode=";
        } else {
          let findTemplateCodeItem = this.tableData.find(
            (item) => item.fieldEn == "templateCode"
          );
          if (
            findTemplateCodeItem &&
            findTemplateCodeItem.inputType == "select_hidden"
          ) {
            params.reportAction.url =
              "reportPage?templateCode=" +
              formdata.templateCode +
              "&reportCode=";
          } else {
            params.reportAction.url =
              "reportPage?templateCode=" + "&reportCode=";
          }
        }
      }

      params.customMap = {
        reportType: this.formData.reportType,
        templateCode: this.formData.templateCode,
      };

      this.buildLoading = true;
      pageApi
        .buildConfig(params)
        .then((res) => {
          if (res.data.status == 200) {
            this.$message.closeAll();
            this.$message({
              type: "success",
              message: "配置成功！",
            });
            if (this.mode === "add") {
              // 配置成功后初始化页面
              this.initPage();
            } else {
              this.getAllVersion();
            }
          } else {
            this.$message({
              type: "error",
              message: res.data.message || "配置失败！",
            });
          }
          this.buildLoading = false;
        })
        .catch((err) => {
          this.buildLoading = false;
          this.$message({
            type: "error",
            message: err || "配置失败！",
          });
        });
    },
  },
};
</script>
<style lang="scss" scoped>
::v-deep .el-input--small .el-input__inner {
  height: 26px;
  line-height: 26px;
}

.custom-configuration {
  .form_box {
    margin-top: 20px;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 5px;
  }

  .el-input {
    width: 200px !important;
  }

  .el-textarea {
    width: 80%;
  }
}
</style>

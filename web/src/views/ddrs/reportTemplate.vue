<template>
  <div class="page-card-common" style="height: 100%">
    <template>
      <div :class="className">
        <el-tabs
          class="currency_report_old_tabs"
          type="card"
          v-model="activeName"
          v-if="tabArr.length > 1"
          @tab-click="handleClick"
        >
          <el-tab-pane
            v-for="item in tabArr"
            :key="item.tableCode"
            :label="item.tableCn"
            :name="item.tableCode"
          ></el-tab-pane>
        </el-tabs>

        <el-form
          :inline="true"
          v-if="crudEnable.indexOf('C') != -1 || crudEnable.indexOf('R') != -1"
          ref="formInline"
          :model="formInline"
          :rules="formInlineRules"
          style="margin-bottom: 8px"
          class="form_inline_search demo-form-inline currency_report_old_form"
        >
          <div class="top_box">
            <div class="top_box_l">
              <div style="width: 100%; min-height: 50px">
                <el-form-item
                  v-for="(item, index) in searchDataArr"
                  :key="index"
                  :prop="item.fieldEn"
                >
                  <selectDDRS
                    v-if="item.inputType == 'selectTable'"
                    :reportConfig="{ reportCode: item.sonEn }"
                    :placeholder="item.fieldCn"
                    size="small"
                    :formCount="formInline"
                    :valueField="item.fieldEn"
                    @sendData="
                      (val) => {
                        formInline[item.fieldEn] = val;
                      }
                    "
                  >
                  </selectDDRS>
                  <el-input
                    v-model.trim="formInline[item.fieldEn]"
                    type="text"
                    v-else-if="item.fieldType != 'D' && !item.dicSql"
                    auto-complete="off"
                    size="small"
                    clearable
                    :placeholder="item.fieldCn"
                  />
                  <multipleSelectTable
                    class="multipleSelectTable"
                    v-else-if="item.inputType == 'select_multiple_fund'"
                    v-model="formInline[item.fieldEn]"
                    :data="fundList"
                    :Columns="Columns"
                    idField="fundCode"
                    nameField="codeName"
                    :placeholder="item.fieldCn"
                    @checkboxChange="checkboxChange($event, item.fieldEn)"
                    @checkboxAll="checkboxAll($event, item.fieldEn)"
                  ></multipleSelectTable>
                  <select-table
                    v-model="formInline[item.fieldEn]"
                    v-else-if="item.inputType == 'select_fund'"
                    @sendDataObj="sendDataObj($event, item.fieldEn)"
                  ></select-table>
                  <!-- 父 -->
                  <el-select
                    v-else-if="item.dicSql && item.inputType == 'select'"
                    clearable
                    filterable
                    v-model="formInline[item.fieldEn]"
                    :placeholder="item.fieldCn"
                    @change="
                      item.sonEn
                        ? getSunchange($event, item.fieldEn, item.sonEn)
                        : selectChange($event, item.fieldEn)
                    "
                  >
                    <el-option
                      v-for="(group, index) in formSelectArr[item.fieldEn]"
                      :value="group.DIM_CDE"
                      :key="index"
                      :label="group.DIM_NME"
                      @click.native="
                        item.sonEn
                          ? getSun(
                              group.DIM_CDE,
                              group.DIM_NME,
                              group.ID,
                              item.fieldEn,
                              item.sonEn
                            )
                          : getSunClick(
                              group.DIM_CDE,
                              group.DIM_NME,
                              item.fieldEn
                            )
                      "
                    >
                    </el-option>
                  </el-select>

                  <el-select
                    class="select_multiple"
                    popper-class="select_multiple_popper"
                    v-else-if="
                      item.dicSql && item.inputType == 'select_multiple'
                    "
                    filterable
                    clearable
                    multiple
                    collapse-tags
                    v-model="formInline[item.fieldEn]"
                    :placeholder="item.fieldCn"
                    @change="select_multipleChange($event, item.fieldEn)"
                  >
                    <el-option
                      v-for="(group, index) in formSelectArr[item.fieldEn]"
                      :value="group.DIM_CDE"
                      :key="index"
                      :label="group.DIM_NME"
                    ></el-option>
                  </el-select>
                  <el-date-picker
                    v-model="formInline[item.fieldEn]"
                    type="date"
                    size="small"
                    v-else-if="item.inputType === 'date' && !item.formatValue"
                    value-format="yyyy-MM-dd"
                    :placeholder="item.fieldCn"
                  >
                  </el-date-picker>
                  <el-date-picker
                    v-model="formInline[item.fieldEn]"
                    type="year"
                    size="small"
                    v-else-if="
                      item.inputType === 'date' && item.formatValue == 'yyyy'
                    "
                    value-format="yyyy"
                    :placeholder="item.fieldCn"
                  >
                  </el-date-picker>
                  <el-date-picker
                    v-model="formInline[item.fieldEn]"
                    type="month"
                    size="small"
                    v-else-if="
                      item.inputType === 'date' && item.formatValue == 'yyyy-mm'
                    "
                    value-format="yyyy-MM"
                    :placeholder="item.fieldCn"
                  >
                  </el-date-picker>
                </el-form-item>
                <el-form-item>
                  <el-button
                    type="primary"
                    class="formButton"
                    v-if="crudEnable.indexOf('R') != -1"
                    @click="onSubmitValidate(true)"
                    style="margin-bottom: 5px"
                    size="small"
                    ><i class="el-icon-search"></i>查询
                  </el-button>
                  <el-button
                    type="primary"
                    class="formButton"
                    v-if="crudEnable.indexOf('S') != -1"
                    @click="resetForm(true)"
                    style="margin-bottom: 5px"
                    size="small"
                    ><i class="el-icon-delete"></i>重置
                  </el-button>
                </el-form-item>
              </div>
            </div>
          </div>
        </el-form>
        <div style="">
          <div :style="{ height: `calc(100vh - ${searchHeight}px - 130px)` }">
            <div style="display: flex; align-items: center">
              <div class="forms_table_title">
                <i class="el-icon-s-data"></i> {{ tableTitle }}
              </div>
              <div style="position: relative">
                <el-row
                  type="flex"
                  justify="right"
                  style="
                    position: absolute;
                    right: 40px;
                    z-index: 1000 !important;
                    padding-top: 10px;
                  "
                >
                  <el-button
                    type="primary"
                    class="formButton"
                    v-if="crudEnable.indexOf('C') != -1"
                    plain
                    @click="addData()"
                    style="margin-bottom: 5px"
                    size="small"
                    ><i class="el-icon-circle-plus-outline"></i>新增
                  </el-button>
                  <el-button
                    v-if="crudEnable.indexOf('B') != -1"
                    type="primary"
                    class="formButton"
                    plain
                    style="margin-bottom: 5px"
                    size="small"
                    @click="batchDelete"
                    ><i class="el-icon-delete"></i>批量删除
                  </el-button>
                  <el-button
                    v-if="crudEnable.indexOf('E') != -1"
                    type="primary"
                    class="formButton"
                    @click="downloadFile('excel')"
                    style="margin-bottom: 5px"
                    size="small"
                  >
                    <i class="el-icon-download"></i>下载Excel
                  </el-button>
                  <el-button
                    v-if="crudEnable.indexOf('T') != -1"
                    type="primary"
                    class="formButton"
                    @click="downloadFile('txt')"
                    style="margin-bottom: 5px"
                    size="small"
                  >
                    <i class="el-icon-download"></i>下载Txt
                  </el-button>
                  <el-button
                    v-if="crudEnable.indexOf('P') != -1"
                    type="primary"
                    class="formButton"
                    @click="downloadFile('pdf')"
                    style="margin-bottom: 5px"
                    size="small"
                  >
                    <i class="el-icon-download"></i>下载PDF
                  </el-button>
                  <el-button
                    v-if="crudEnable.indexOf('V') != -1"
                    type="primary"
                    class="formButton"
                    @click="downloadFile('csv')"
                    style="margin-bottom: 5px"
                    size="small"
                  >
                    <i class="el-icon-download"></i>下载CSV
                  </el-button>
                  <!-- <el-button
                  v-if="crudEnable.indexOf('B') != -1"
                  type="primary"
                  class="formButton"
                  @click="print('pdf')"
                  style="margin-bottom: 5px"
                  size="small"
                >
                  <i class="el-icon-printer"></i>打印
                </el-button>
                <el-button
                  v-if="crudEnable.indexOf('B') != -1"
                  type="primary"
                  class="formButton"
                  @click="mailmail()"
                  style="margin-bottom: 5px"
                  size="small"
                >
                  <i class="el-icon-message"></i>快捷邮件发送
                </el-button>
                <el-button
                  v-if="crudEnable.indexOf('B') != -1"
                  type="primary"
                  class="formButton"
                  @click="customMail()"
                  style="margin-bottom: 5px"
                  size="small"
                >
                  <i class="el-icon-message"></i>自定义邮件发送
                </el-button> -->
                </el-row>
                <vxe-toolbar
                  style="position: relative; right: 0px"
                  custom
                  ref="xToolbar"
                >
                </vxe-toolbar>
              </div>
            </div>
            <vxe-table
              v-loading="tableLoading"
              highlight-hover-row
              border
              class="vxetable-style"
              stripe
              resizable
              show-header-overflow
              show-overflow
              size="small"
              :export-config="{}"
              ref="xTable"
              v-if="tableShow"
              @custom="toolbarCustomEvent"
              :data="tableData"
              auto-resize
              height="auto"
              :scroll-x="{ enabled: false }"
              :scroll-y="{ enabled: false }"
              :sort-config="{ remote: true, trigger: 'cell' }"
              @sort-change="customSortMethod"
            >
              <vxe-table-column
                v-if="crudEnable.indexOf('B') != -1"
                type="checkbox"
                width="60"
                align="center"
                fixed="left"
              ></vxe-table-column>
              <vxe-table-column
                v-for="group in tableDataDetailArr"
                :key="group.fieldEn"
                :visible="group.flag"
                min-width="160"
                header-align="center"
                :field="group.fieldEn"
                :title="group.fieldCn"
                :align="group.fieldType == 'N' ? 'right' : 'left'"
                :sortable="
                  crudEnable.includes('S') &&
                  group.isCrud &&
                  group.isCrud.includes('S')
                "
              >
                <template slot="default" slot-scope="{ row }">
                  <template
                    v-if="
                      !group.formatShow &&
                      group.inputType !== 'select' &&
                      !group.dicSql
                    "
                  >
                    <span v-if="group.fieldEn === 'ASSET_DETAIL'">
                      <el-link type="primary" :underline="false" size="small">{{
                        row[group.fieldEn]
                      }}</el-link>
                    </span>
                    <span v-else>{{ row[group.fieldEn] }}</span>
                  </template>
                  <template
                    v-if="
                      !group.formatShow &&
                      (group.inputType == 'select' || group.dicSql)
                    "
                  >
                    <span
                      v-if="
                        group.fieldEn === 'ASSET_DETAIL' &&
                        $route.path ==
                          '/dataReport/reportPage:reportCode=collectDataQuery'
                      "
                    >
                      <el-link
                        @click="handleJump('ASSET_DETAIL', row)"
                        type="primary"
                        :underline="false"
                        style="font-size: 12px; color: #007dff"
                        size="small"
                        >{{
                          transf(group.fieldEn, row[group.fieldEn])
                        }}</el-link
                      >
                    </span>
                    <span v-else>{{
                      transf(group.fieldEn, row[group.fieldEn])
                    }}</span>
                  </template>
                  <template v-if="group.formatShow">
                    <span>{{
                      format(
                        row[group.fieldEn],
                        group.fieldType,
                        group.formatShow
                      )
                    }}</span>
                  </template>
                </template>
              </vxe-table-column>

              <vxe-table-column
                fixed="right"
                v-if="
                  crudEnable.indexOf('U') != -1 ||
                  crudEnable.indexOf('D') != -1 ||
                  reportCode == 'id-9292d1d-22fa-09d6-b7e6-c61e4146b13f'
                "
                title="操作"
                :width="operationColWidth"
                show-overflow
                align="center"
              >
                <template slot-scope="scope">
                  <el-link
                    v-if="crudEnable.indexOf('U') != -1"
                    type="primary"
                    :underline="false"
                    icon="el-icon-view"
                    @click="editData(scope.row, true)"
                    >查看详情
                  </el-link>
                  <el-link
                    v-if="crudEnable.indexOf('U') != -1"
                    type="primary"
                    :underline="false"
                    icon="el-icon-edit"
                    @click="editData(scope.row, false)"
                    >编辑
                  </el-link>
                  <el-link
                    v-if="crudEnable.indexOf('D') != -1"
                    type="danger"
                    :underline="false"
                    icon="el-icon-delete"
                    @click="delData(scope.row)"
                    >删除
                  </el-link>
                </template>
              </vxe-table-column>
            </vxe-table>
          </div>
        </div>
        <el-row style="margin-top: 50px">
          <Pagination
            v-if="isPage == 1"
            :total="total"
            :page="formInline.pageNum"
            :limit="formInline.pageSize"
            @pagination="Pagination"
          ></Pagination>
          <div style="clear: both"></div>
        </el-row>

        <!-- 新增代办 -->
        <el-dialog
          v-if="countDialog"
          :title="countTitle"
          append-to-body
          customClass="currencyReportWidth"
          :visible.sync="countDialog"
          :close-on-click-modal="false"
          @closed="editFormClose"
        >
          <el-container>
            <el-main class="mainBox">
              <el-form
                :inline="true"
                ref="formCount"
                :model="formCount"
                :rules="countRules"
                label-position="right"
                style="width: 100% !important"
                class="labelStyle"
              >
                <el-form-item
                  v-for="(item, index) in addDataArr"
                  :key="index"
                  :label="item.fieldCn"
                  :prop="item.fieldEn"
                  class="mb20"
                  :label-width="formLabelWidth"
                >
                  <span slot="label" :title="item.fieldCn">{{
                    item.fieldCn
                  }}</span>
                  <selectDDRS
                    v-if="item.inputType == 'selectTable'"
                    :disabled="isSearchDetail"
                    :reportConfig="{ reportCode: item.sonEn }"
                    size="small"
                    :placeholder="item.fieldCn"
                    :formCount="formCount"
                    :valueField="item.fieldEn"
                    @sendData="
                      (val) => {
                        formCount[item.fieldEn] = val;
                      }
                    "
                  >
                  </selectDDRS>
                  <el-select
                    v-else-if="item.dicSql && item.inputType == 'select'"
                    :disabled="isSearchDetail"
                    clearable
                    filterable
                    v-model="formCount[item.fieldEn]"
                    size="small"
                    placeholder="请选择"
                    @change="
                      item.sonEn
                        ? editGetSunchange($event, item.fieldEn, item.sonEn)
                        : ''
                    "
                  >
                    <el-option
                      v-for="(group, index) in editFormSelectArr[item.fieldEn]"
                      :value="group.DIM_CDE"
                      :key="index"
                      :label="group.DIM_NME"
                      @click.native="
                        item.sonEn
                          ? editGetSun(
                              group.DIM_CDE,
                              group.DIM_NME,
                              group.ID,
                              item.fieldEn,
                              item.sonEn
                            )
                          : ''
                      "
                    >
                    </el-option>
                  </el-select>
                  <!-- 日期 yyyy-MM-dd -->
                  <el-date-picker
                    v-model="formCount[item.fieldEn]"
                    type="date"
                    size="small"
                    v-else-if="item.inputType === 'date' && !item.formatValue"
                    :disabled="isSearchDetail"
                    value-format="yyyy-MM-dd"
                    placeholder="选择日期"
                  >
                  </el-date-picker>
                  <!-- 日期 yyyy -->
                  <el-date-picker
                    v-model="formCount[item.fieldEn]"
                    type="year"
                    size="small"
                    v-else-if="
                      item.inputType === 'date' && item.formatValue == 'yyyy'
                    "
                    :disabled="isSearchDetail"
                    value-format="yyyy"
                    placeholder="选择年"
                  >
                  </el-date-picker>
                  <!-- 日期 yyyy-MM -->
                  <el-date-picker
                    v-model="formCount[item.fieldEn]"
                    type="month"
                    size="small"
                    v-else-if="
                      item.inputType === 'date' && item.formatValue == 'yyyy-mm'
                    "
                    :disabled="isSearchDetail"
                    value-format="yyyy-MM"
                    placeholder="选择月"
                  >
                  </el-date-picker>
                  <el-input
                    v-model="formCount[item.fieldEn]"
                    type="text"
                    v-else
                    auto-complete="off"
                    size="small"
                    clearable
                    :disabled="isSearchDetail"
                    placeholder="请输入"
                  />
                </el-form-item>
              </el-form>
            </el-main>
          </el-container>
          <div slot="footer" class="dialog-footer">
            <el-button size="small" @click="countDialog = false"
              >取 消</el-button
            >
            <el-button
              v-if="!isSearchDetail"
              type="primary"
              size="small"
              :loading="countSubmit_btn"
              @click="countSubmit('formCount')"
              >确 定
            </el-button>
          </div>
        </el-dialog>

        <el-dialog
          title="添加查询条件"
          append-to-body
          customClass="currencyReportWidth"
          :visible.sync="searchDialog"
          :close-on-click-modal="false"
        >
          <el-container>
            <el-main class="mainBox">
              <el-checkbox
                :indeterminate="isIndeterminate"
                v-model="checkAll"
                @change="handleCheckAllChange"
                >全选
              </el-checkbox>
              <div style="margin: 15px 0"></div>
              <el-checkbox-group
                v-model="checkedForms"
                @change="handlecheckedFormsChange"
              >
                <el-checkbox
                  v-for="(item, index) in searchForms"
                  :label="item.fieldEn"
                  :key="index"
                  >{{ item.fieldCn }}
                </el-checkbox>
              </el-checkbox-group>
            </el-main>
          </el-container>
          <div slot="footer" class="dialog-footer">
            <el-button size="small" @click="searchDialog = false"
              >取 消</el-button
            >
            <el-button
              type="primary"
              size="small"
              :loading="countSubmit_btn"
              @click="searchSubmit()"
              >确 定</el-button
            >
          </div>
        </el-dialog>
        <el-dialog
          title="明细"
          append-to-body
          :visible.sync="detailDialog"
          width="80% !important"
          :close-on-click-modal="false"
          @closed="detailDialogClosed"
          custom-class="detailDialog__"
        >
          <mySelf
            v-if="detail_show"
            :currencyReportPageData="currencyReportPageData_dialog"
          ></mySelf>
        </el-dialog>
        <el-dialog
          title="快捷邮件发送"
          append-to-body
          :visible.sync="mailDialog"
          width="70% !important"
          :close-on-click-modal="false"
          @closed="mailDialogClosed"
        >
          <!-- <div>
        提示：点击列表数据选择
      </div> -->
          <el-table
            :data="mailConfigData"
            border
            style="width: 100%"
            v-loading="mailConfigDataLoading"
          >
            <!-- highlight-current-row -->
            <!-- @current-change="handleCurrentChange" -->
            <el-table-column
              prop="confName"
              show-overflow-tooltip
              label="配置名称"
              min-width="150"
              algin="left"
              header-align="left"
            >
              <template slot-scope="scope">
                <!-- <span>{{ scope.row.confName | noDataFilter }}</span> -->
                <el-radio v-model="mailId" :label="scope.row.id">{{
                  scope.row.confName
                }}</el-radio>
                <!-- <el-radio v-model="rowObj" :label="scope.row">{{scope.row.confName}}</el-radio> -->
              </template>
            </el-table-column>
            <el-table-column
              prop="reportNames"
              show-overflow-tooltip
              label="涉及报表"
              min-width="150"
              algin="left"
              header-align="left"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.reportNames | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="emailToNames"
              show-overflow-tooltip
              label="邮件收件人"
              min-width="150"
              algin="left"
              header-align="left"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.emailToNames | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="emailCcNames"
              show-overflow-tooltip
              label="抄送"
              min-width="150"
              algin="left"
              header-align="left"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.emailCcNames | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="emailTBccsNames"
              show-overflow-tooltip
              label="密送"
              min-width="150"
              algin="left"
              header-align="left"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.emailTBccsNames | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="remark"
              show-overflow-tooltip
              label="备注"
              min-width="150"
              algin="left"
              header-align="left"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.remark | noDataFilter }}</span>
              </template>
            </el-table-column>
          </el-table>
          <div slot="footer" class="dialog-footer">
            <el-button
              size="small"
              @click="mailDialog = false"
              :loading="send_loading"
              >取 消</el-button
            >
            <el-button
              type="primary"
              size="small"
              @click="sendMail()"
              :loading="send_loading"
              >发 送</el-button
            >
          </div>
        </el-dialog>
        <el-dialog
          title="自定义邮件发送"
          append-to-body
          :visible.sync="customMailDialog"
          width="80% !important"
          :close-on-click-modal="false"
          @closed="customMailDialogClosed"
        >
          <sendMailForm
            v-if="sendMailForm_show"
            ref="sendMailForm"
            :formArr="searchDataArr"
            :formSelectArr="formSelectArr"
            :tableCode="activeName"
            :reportCode="reportCode"
            :reportName="reportName"
            :headerArr="headerArr"
            @close="customMailDialog = false"
          ></sendMailForm>
        </el-dialog>
      </div>
    </template>
  </div>
</template>

<script>
import bizBeginApi from "./api/bizBegin";
import selectTable from "./components/selectTable.vue";
import multipleSelectTable from "./components/multiple-select-table2";
import $ from "jquery";
import Pagination from "@/components/Pagination";
import commonFun from "@/filters/new_common";
import pageApi from "./api/currencyReport";
import reportToolApi from "./api/reportTool";
import mySelf from "./components/currencyReport_old_copy.vue";
import sendMailForm from "./components/sendMailForm.vue";
import selectDDRS from "@/components/selectDDRS";
import { mapGetters } from "vuex";

export default {
  name: "ReportTemplate",
  components: {
    Pagination,
    mySelf,
    sendMailForm,
    selectTable,
    multipleSelectTable,
    selectDDRS,
  },
  props: {
    currencyReportPageData: {
      type: Object,
    },
    formQueryConfig: {
      type: Object,
      default: () => {
        return {};
      },
    },
    className: {
      type: String,
    },
  },
  data() {
    return {
      isInit: false,
      fundList: [],
      Columns: [
        { label: "产品", prop: "codeName" },
        { label: "托管机构", prop: "trustorName" },
        { label: "基金服务机构", prop: "operatorName" },
      ],
      timestamp: "",
      tabInfo: [],
      tableData: [],
      activeName: "",
      reportName: "",
      tabArr: [{ dimCde: "1", dimNme: "测试" }],
      showTitle: 0,
      formInline: {
        reportName: "",
        reportCode: "",
        tableCode: "",
        pageSize: 50,
        pageNum: 1,
      },
      formInlineRules: {},
      reportCode: "",
      total: 0, //总条数
      tableDataDetailArr: [
        // { code: "id", flag: true, name: "主键" },
        // { code: "name", flag: true, name: "姓名" },
        // { code: "sex", flag: true, name: "性别" },
        // { code: "age", flag: false, name: "年龄" },
      ],
      countDialog: false, // 弹窗
      countTitle: "", //标题
      countFormList: "", //是新增还是编辑
      // 新增 编辑计算任务
      formCount: {
        sealCode: "", //印章编码
        sealStatus: "", //印章状态
      },
      // 操作类型 1、添加 2、编辑
      operationType: 1,
      // 弹窗验证规则
      countRules: {},
      formLabelWidth: "140px",
      countSubmit_btn: false, //保存按钮加载
      tableLoading: false, //加载
      fieldsInfoArr: [], //字段数组
      tableShow: false, //列表展示控制
      addDataArr: [], //新增-编辑数组
      searchDataArr: [], //新增-编辑数组
      headerArr: [],
      isPage: 1, //是否分页判断
      formSelect: {}, //下拉框字典值
      formSelectArr: {}, //下拉框字典值数组
      formSelectArr2: {}, //下拉框字典值数组
      editFormSelectArr: {}, //下拉框字典值数组
      editFormSelectArr2: {}, //下拉框字典值数组
      searchDialog: false,
      checkAll: false,
      checkedForms: [], //已选择的查询条件
      searchForms: [], //查询条件数组
      checkAllForms: [],
      isIndeterminate: true,
      isSearchSelect: 0, //是否查询下拉框的值
      tabFormArr: {}, //tab查询条件数组
      tabSearchArr: {}, //tab查询内容数组
      crudEnable: "", //按钮权限
      pathSearchData: {},
      isSearchDetail: false, // 是否查看详情
      detailDialog: false, //明细弹框
      detail_show: false,
      currencyReportPageData_dialog: {
        D_DATE: "",
        VC_FUNDCODE: "",
        reportCode: "id-0db37d6-04c1-2253-a864-08b9e53a737b",
      },
      searchHeight: 290,
      mailConfigData: [],
      mailConfigDataLoading: false,
      mailDialog: false,
      customMailDialog: false,
      sendMailForm_show: false,
      mailId: "",
      send_loading: false,
      rowObj: {},
      operationColWidth: 100,
      tableTitle: "数据",
    };
  },
  activated() {
    this.fetTableHeight();
    let self = this;
    window.addEventListener("resize", self.fetTableHeight, true);
  },
  watch: {
    formQueryConfig: {
      handler() {
        this.activeName = this.tabArr[0].dimCde;
        if (this.isInit) {
          this.getTabData();
        }
      },
      deep: true,
    },
    crudEnable(newValue, oldValue) {
      let width = 0;
      if (this.crudEnable.indexOf("U") !== -1) {
        width += 160;
      }
      if (this.crudEnable.indexOf("D") !== -1) {
        width += 80;
      }
      this.operationColWidth = width;
    },
  },
  deactivated() {
    let self = this;
    window.removeEventListener("resize", self.fetTableHeight, true);
  },
  beforeDestroy() {
    let self = this;
    window.removeEventListener("resize", self.fetTableHeight, true);
  },
  computed: {
    transf() {
      return (v1, v2) => {
        // console.log(v1,v2);
        let len = Object.keys(this.formSelectArr2).length;
        // console.log('lem',len);
        if (len < 1) return v2;
        if (this.formSelectArr2[v1]) {
          let obj = this.formSelectArr2[v1].filter((item) => {
            // console.log(item);
            if (item.DIM_CDE == v2) {
              return item;
            }
          });
          // console.log('obj.DIM_NME',obj);
          if (obj.length) {
            return obj[0].DIM_NME;
          } else {
            return v2;
          }
        } else {
          return v2;
        }
      };
    },
    ...mapGetters(["sidebar", "name", "avatar", "device"]),
  },
  mounted() {
    this.tableTitle = this.$route.meta.title || "数据";
    this.activeName = this.tabArr[0].dimCde;
    if (!this.isInit) {
      this.getTabData();
    }
  },
  methods: {
    /**
     * @Description: 处理 页面跳转事件，携参
     * @author Liu Rui Bing
     * @date 2024/6/14
     */
    handleJump(type, row) {
      // 交银 - 汇总结果 - 偿付能力资产类型 点击跳转 -》 明细结果查询， 携带当前查询条件
      let dataParams = _.cloneDeep(this.formInline);
      delete dataParams.tableCode;
      delete dataParams.pageNum;
      delete dataParams.pageSize;
      delete dataParams.reportCode;
      delete dataParams.reportName;

      if (type === "ASSET_DETAIL") {
        const data = {
          ALL: {
            ...dataParams,
            ASSET_DETAIL: [row.ASSET_DETAIL],
          },
        };
        this.$store.commit("SET_FROM_LINK_JUMP", true);
        this.$store.commit("SET_RS_LINK_JUMP_DATA", data);
        this.$router.push({
          path: "/dataReport/reportPage:reportCode=detailResultQuery",
        });
      }
    },
    // 排序的公共方法
    customSortMethod(val) {
      // this.formInline.orderString = commonFun.VXEorderByStringNoNullLast(val);
      this.formInline.orderString = commonFun.VXEorderByString(val);
      this.onSubmitValidate(false);
    },
    cellClassName({ row, rowIndex, column, columnIndex }) {
      return "vxe-cell-class-name";
    },
    headerCellClassName({ column, columnIndex }) {
      return "vxe-header-cell-class-name";
    },
    // 产品多选数据
    getFundList() {
      bizBeginApi
        .getProductFund()
        .then(({ data: res }) => {
          if (res.status === 200) {
            let temp = [...res.data];
            for (let i of temp) {
              i["codeName"] = i.fundCode + "_" + i.fundName;
            }
            this.fundList = temp;
          } else this.$message.error("查询产品信息失败");
        })
        .catch((err) => {
          this.$message.error("查询产品信息失败");
        });
    },
    sendDataObj(data, fieldEn) {
      // console.log(data,aaa);
      if (data) {
        this.formInline[fieldEn + "_fundCode"] = data.fundCode;
        this.formInline[fieldEn + "_TEXT"] =
          data.fundCode + "-&-" + data.fundName;
      } else {
        this.formInline[fieldEn + "_fundCode"] = "";
        this.formInline[fieldEn + "_TEXT"] = "";
      }
    },
    checkboxChange(data, fieldEn) {
      // console.log(data.records);
      if (data.records.length == 1) {
        let obj = data.records[0];
        this.formInline[fieldEn + "_TEXT"] =
          obj.fundCode + "-&-" + obj.fundName;
      } else {
        this.formInline[fieldEn + "_TEXT"] = "";
      }
    },
    checkboxAll(data, fieldEn) {
      // console.log(data.records);
      if (data.records.length == 1) {
        let obj = data.records[0];
        this.formInline[fieldEn + "_TEXT"] =
          obj.fundCode + "-&-" + obj.fundName;
      } else {
        this.formInline[fieldEn + "_TEXT"] = "";
      }
    },
    fetTableHeight() {
      let h = $(".currency_report_old_form").height();
      let tabsH = $(".currency_report_old_tabs").height();
      if (h && !tabsH) {
        this.searchHeight = h + 120;
      }
      if (h && tabsH) {
        this.searchHeight = h + tabsH + 120;
      }
      if (!h && tabsH) {
        this.searchHeight = tabsH + 120;
      }
      console.log("fetTableHeight", h);
    },
    currencyInit(data) {
      //  this.currencyReportPageData = data
      if (!this.currencyReportPageData) {
        let path = this.$route.fullPath;
        let formData = path.split("?")[1];
        if (formData.indexOf("&") != -1) {
          let arr = formData.split("&");
          let params = {};
          for (let i = 0; i < arr.length; i++) {
            let a = arr[i].split("=");
            params[a[0]] = a[1];
          }
          this.pathSearchData = params;
        } else {
          this.reportCode = formData.split("=")[1];
        }
      }
      this.getTabData();
    },
    handleClick(tab, event) {
      //debugger;
      let name = this.activeName;
      let arr = this.tabArr;
      this.isSearchSelect = 0;
      this.searchDataArr = [];
      this.tableDataDetailArr = this.getAllPrpos(
        this.tabInfo[0][tab.name],
        true
      );
      this.fieldsInfoArr = this.tabInfo[0][tab.name];
      for (let i = 0; i < arr.length; i++) {
        if (arr[i].tableCode == name) {
          this.isPage = arr[i].isPage;
          this.reportName = arr[i].tableCn || "";
          if (arr[i].crudEnable) {
            this.crudEnable = arr[i].crudEnable;
          } else {
            this.crudEnable = "-1";
          }
        }
      }
      this.formInline.pageSize = 50;
      this.formInline.pageNum = 1;
      this.onSubmitValidate(true);
    },
    //分页
    Pagination(val) {
      this.formInline.pageSize = val.limit; //页面条数
      this.formInline.pageNum = val.page; //页面
      this.onSubmitValidate(false);
    },
    toolbarCustomEvent(params) {
      let self = this;
      // console.log(params);
      // debugger;
      // const visibleColumn = self.$refs.xTable.getColumns()
      // switch (params.type) {
      //   case 'confirm': {
      //     this.$XModal.message({ message: `点击了确认，显示为 ${visibleColumn.length} 列`, status: 'info' })
      //     break
      //   }
      //   case 'reset': {
      //     this.$XModal.message({ message: `点击了重置，显示为 ${visibleColumn.length} 列`, status: 'info' })
      //     break
      //   }
      //   case 'close': {
      //     this.$XModal.message({ message: `关闭了面板，显示为 ${visibleColumn.length} 列`, status: 'info' })
      //     break
      //   }
      // }
    },
    checkColumnMethod({ column }) {
      if (this.showTitle > 0) {
        //column.visible = false;
      }
      this.showTitle = this.showTitle + 1;
      return true;
    },
    resetForm() {
      // this.$refs['formInline'].resetFields();
      // this.$nextTick(()=>{
      this.searchDataArr.forEach((item) => {
        if (
          item.inputType == "select_multiple" ||
          item.inputType == "select_multiple_fund"
        ) {
          // this.formInline[item.fieldEn] = []
          this.$set(this.formInline, item.fieldEn, []);
        } else {
          // this.formInline[item.fieldEn] = ''
          this.$set(this.formInline, item.fieldEn, "");
        }
      });

      // })
    },
    onSubmitValidate(flag, type) {
      if (this.$refs["formInline"]) {
        this.$refs["formInline"].validate((valid) => {
          if (valid) {
            this.onSubmit(flag, type);
          } else {
            // console.log('error submit!!');
          }
        });
      } else {
        this.onSubmit(flag, type);
      }
    },
    onSubmit(flag, type) {
      // console.log('onSubmit',flag,type);
      // if(type=='mounted') return
      this.tableLoading = true;
      // 消除没有值的参数
      if (flag) {
        this.formInline.pageNum = 1;
      }
      // this.tableShow = false;
      this.formInline.tableCode = this.activeName;

      let params = commonFun.parameterSrc(this.formInline);
      if (params.orderString) {
        let arr = params.orderString.split(" ");
        params.fieldSort = {
          [arr[0]]: arr[1],
        };
      }
      for (let key in params) {
        if (params[key].constructor == Array) {
          if (params[key].length == 1) {
            this.formSelectArr[key].forEach((item) => {
              if (item.DIM_CDE == params[key][0]) {
                params[key + "_TEXT"] = item.DIM_NME;
              }
            });
          }
        }
        if (key.indexOf("_fundCode") != -1) {
          params[key.split("_fundCode")[0]] = params[key];
        }
      }
      params.reportCode = this.reportCode;
      params.permissions = "1";
      if (this.currencyReportPageData) {
        let data = this.currencyReportPageData;

        for (var p in data) {
          params[p] = data[p];
        }
      }
      if (this.pathSearchData) {
        let data = this.pathSearchData;

        for (var p in data) {
          params[p] = data[p];
        }
      }
      if (this.isPage != 1) {
        params.pageSize = "";
        params.pageNum = "";
      }
      // this.tableData = [];
      params = commonFun.parameterSrc(params);
      pageApi
        .getDataTableNameList(params)
        .then((response) => {
          if (
            response.data.status === 200 &&
            response.data.data &&
            response.data.data.length > 0
          ) {
            let data = response.data.data[0];
            if (data.fieldsInfo && data.fieldsInfo.length > 0) {
              // this.tableDataDetailArr = this.getAllPrpos(data.fieldsInfo);
              // let arr = data.fieldsInfo.filter(item=>{
              //   return item.isCrud&&item.isCrud.indexOf('R')!=-1
              // });
              // this.tableDataDetailArr = arr;
              // this.getAllPrpos(data.fieldsInfo);
            }
            if (this.isPage == 1) {
              this.tableData = data.dataList.list;
            } else {
              this.tableData = data.dataList;
            }

            // 页面总条数
            if (data.dataList.total) {
              this.total = data.dataList.total;
            } else {
              this.total = 0;
            }

            this.fieldsInfoArr = data.fieldsInfo;
            // if(type=="mounted"){
            //   this.searchDataArr = [];
            //   let searcharr = data.fieldsInfo.filter(item=>{
            //     return item.isCrud&&item.isCrud.indexOf('M')!=-1
            //   })
            //   this.searchDataArr = searcharr;
            // }
            this.tableShow = true;
          } else {
            this.tableData = [];
            this.total = 0;
            this.formInline.pageSize = 50;
            this.formInline.pageNum = 1;
          }
          // if(response.data.status !== 200){
          //   this.$message({
          //     type:"error",
          //     message:response.data.message || '数据加载失败！'
          //   })
          // }
          this.tableLoading = false;
        })
        .catch((err) => {
          this.tableData = [];
          this.total = 0;
          this.formInline.pageSize = 50;
          this.formInline.pageNum = 1;
          this.tableLoading = false;
          console.log(err);
        });
    },
    // table批量选择结果
    restForm(formName) {
      var self = this;
      //self.refs[formName].resetFields();
      this.formInline.reportName = "";
    },
    addData() {
      let arr = [];
      let fieldsInfoArr = this.fieldsInfoArr;
      let params = {};
      this.countRules = {};
      for (let i = 0; i < fieldsInfoArr.length; i++) {
        if (
          fieldsInfoArr[i].isCrud &&
          fieldsInfoArr[i].isCrud.indexOf("C") != -1
        ) {
          arr.push(fieldsInfoArr[i]);
          params[fieldsInfoArr[i].fieldEn] = "";
        }
        if (fieldsInfoArr[i].isRequired && fieldsInfoArr[i].isRequired == 1) {
          let rulesParams = {};
          rulesParams.required = true;
          rulesParams.message = "请输入" + fieldsInfoArr[i].fieldCn;
          rulesParams.trigger = "change";
          //  rulesParams.type = 'string';
          let rulesArr = [];
          rulesArr.push(rulesParams);
          // this.countRules[fieldsInfoArr[i].fieldEn] = rulesArr;
          this.$set(this.countRules, fieldsInfoArr[i].fieldEn, rulesArr);
        }
      }
      this.addDataArr = arr;
      this.$nextTick(() => {
        this.$refs["formCount"] && this.$refs["formCount"].clearValidate();
      });
      this.operationType = 1;
      this.formCount = params;
      this.countTitle = "新增";
      this.isSearchDetail = false;
      this.countDialog = true;
    },
    editData(row, flag) {
      this.$nextTick(() => {
        this.$refs["formCount"] && this.$refs["formCount"].clearValidate();
      });
      let arr = [];
      let fieldsInfoArr = this.fieldsInfoArr;
      this.countRules = {};
      for (let i = 0; i < fieldsInfoArr.length; i++) {
        if (
          fieldsInfoArr[i].isCrud &&
          fieldsInfoArr[i].isCrud.indexOf("U") != -1
        ) {
          arr.push(fieldsInfoArr[i]);
        }
        if (
          fieldsInfoArr[i].isCrud &&
          fieldsInfoArr[i].isCrud.indexOf("U") != -1 &&
          fieldsInfoArr[i].isRequired &&
          fieldsInfoArr[i].isRequired == 1
        ) {
          let rulesParams = {};
          rulesParams.required = true;
          rulesParams.message = "请输入" + fieldsInfoArr[i].fieldCn;
          rulesParams.trigger = "change";
          //  rulesParams.type = 'string';
          let rulesArr = [];
          rulesArr.push(rulesParams);
          // this.countRules[fieldsInfoArr[i].fieldEn] = rulesArr;
          this.$set(this.countRules, fieldsInfoArr[i].fieldEn, rulesArr);
        }
      }
      this.formCount = {}
      this.addDataArr = arr;
      this.addDataArr.forEach(item => {
        this.$set(this.formCount, item.fieldEn, row[item.fieldEn] || "")
      })

      this.formCount = {
        ...row,
        ...this.formCount,
      }
      
      this.operationType = 2;
      if (flag) {
        this.countTitle = "查看详情";
        this.isSearchDetail = true;
      } else {
        this.countTitle = "修改";
        this.isSearchDetail = false;
      }
      this.countDialog = true;
    },
    delData(row) {
      this.$confirm("确定删除?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          let params = {};
          if (row) {
            for (var p in row) {
              params[p] = row[p];
            }
          }
          params.tableCode = this.activeName;
          params.reportCode = this.reportCode;
          if (this.currencyReportPageData) {
            let currencyReportPageData = this.currencyReportPageData;

            for (var p in currencyReportPageData) {
              params[p] = currencyReportPageData[p];
            }
          }

          pageApi
            .deleteDataSource(params)
            .then((response) => {
              if (response.data.status === 200) {
                // 关闭移动指标弹框

                this.$message.closeAll();
                this.$message({
                  message: "删除成功",
                  type: "success",
                });
                // 刷新列表
                this.onSubmit(true);
              } else {
                // 关闭移动指标弹框
                //this.countDialog = false;
                this.$message.closeAll();
                this.$message({
                  message: response.data.message || "删除失败",
                  type: "error",
                });
              }
            })
            .catch(() => {
              // 关闭移动指标弹框

              this.$message.closeAll();
              this.$message({
                message: "删除失败",
                type: "error",
              });
            });
        })
        .catch(() => {});
    },
    // 批量删除
    batchDelete() {
      this.$message.closeAll();
      let checkArray = this.$refs.xTable.getCheckboxRecords(true) || [];
      if (!checkArray.length) {
        return this.$message.warning("至少选择一条数据！");
      }
      this.$confirm("确定删除所选数据?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          let params = {};
          params.tableCode = this.activeName;
          params.reportCode = this.reportCode;
          if (this.currencyReportPageData) {
            let currencyReportPageData = this.currencyReportPageData;
            for (var p in currencyReportPageData) {
              params[p] = currencyReportPageData[p];
            }
          }
          let list = checkArray.map((item) => ({ ...item, ...params }));
          pageApi
            .deleteBatch(list)
            .then((response) => {
              if (response.data.status === 200) {
                // 关闭移动指标弹框
                this.$message.closeAll();
                this.$message({
                  message: "删除成功",
                  type: "success",
                });
                // 刷新列表
                this.onSubmit(true);
              } else {
                // 关闭移动指标弹框
                this.$message.closeAll();
                this.$message({
                  message: response.data.message || "删除失败",
                  type: "error",
                });
              }
            })
            .catch(() => {
              // 关闭移动指标弹框
              this.$message.closeAll();
              this.$message({
                message: "删除失败",
                type: "error",
              });
            });
        })
        .catch(() => {});
    },
    getAllPrpos(formData, flag = false) {
      // 用来保存所有的属性名称和值
      // console.log(formData);
      let arr = [];
      let params = {};
      let searchForms = [];
      let checkAllForms = [];
      arr = formData.filter((item) => {
        return item.isCrud && item.isCrud.indexOf("R") != -1;
      });
      this.searchDataArr = [];
      let searcharr = formData.filter((item) => {
        return item.isCrud && item.isCrud.indexOf("M") != -1;
      });
      this.searchDataArr = searcharr;
      // this.$nextTick(()=>{
      searcharr.forEach((item) => {
        if (
          item.inputType == "select_multiple" ||
          item.inputType == "select_multiple_fund"
        ) {
          this.$set(this.formInline, item.fieldEn, []);
        } else {
          this.$set(this.formInline, item.fieldEn, "");
        }
      });

      // })
      this.formInlineRules = {};
      this.searchDataArr.forEach((item) => {
        if (item.inputType == "date-m") {
          this.formInline[item.fieldEn] = this.timestamp;
        }
        if (item.defaultValue) {
          this.formInline[item.fieldEn] = item.defaultValue;
        }
        if (item.isCrud && item.isCrud.indexOf("Q") != -1) {
          let rulesParams = {};
          rulesParams.required = true;
          rulesParams.message = "请输入" + item.fieldCn;
          rulesParams.trigger = "change";
          let rulesArr = [];
          rulesArr.push(rulesParams);
          // this.formInlineRules[item.fieldEn] = rulesArr;
          this.$set(this.formInlineRules, item.fieldEn, rulesArr);
        }
      });
      this.$nextTick(() => {
        this.$refs["formInline"] && this.$refs["formInline"].clearValidate();
      });

      for (let i = 0; i < formData.length; i++) {
        //获取列表，表头
        // if (formData[i].isCrud && formData[i].isCrud.indexOf("R") != -1) {
        //   let data = {};

        //   data[formData[i].fieldEn] = formData[i].fieldCn;
        //   // 开始遍历
        //   for (var p in data) {
        //     let params = {};
        //     // 方法
        //     // p 为属性名称，obj[p]为对应属性的值
        //     params.code = "" + p;
        //     params.name = data[p];
        //     params.flag = true;
        //     arr.push(params);
        //   }
        // }
        //获取查询条件
        if (formData[i].isCrud && formData[i].isCrud.indexOf("F") != -1) {
          //弹框多选遍历数组
          searchForms.push(formData[i]);
          //弹框全选内容
          checkAllForms.push(formData[i].fieldEn);
        }
        //获取下拉框内容
        if (formData[i].dicSql && this.isSearchSelect == 0) {
          params[formData[i].fieldEn] = "" + formData[i].fieldEn;
          this.getSelectData(formData[i].fieldEn);
        }
      }

      this.searchForms = searchForms;
      this.checkAllForms = checkAllForms;
      this.isSearchSelect = this.isSearchSelect + 1;
      if (flag) {
        if (this.formQueryConfig.hasOwnProperty(this.activeName)) {
          this.formInline = {
            ...this.formInline,
            ...this.formQueryConfig[this.activeName],
          };
        } else if (this.formQueryConfig.hasOwnProperty("ALL")) {
          this.formInline = {
            ...this.formInline,
            ...this.formQueryConfig["ALL"],
          };
        }
      }
      setTimeout(() => {
        this.fetTableHeight();
      }, 500);
      return arr;
    },
    //获取tab数据
    getTabData() {
      if (!this.currencyReportPageData) {
        let path = this.$route.fullPath;
        let formData = path.split(":")[1];
        if (formData.indexOf("&") != -1) {
          let arr = formData.split("&");
          let params = {};
          for (let i = 0; i < arr.length; i++) {
            let a = arr[i].split("=");
            params[a[0]] = a[1];
          }
          this.pathSearchData = params;
        } else {
          this.reportCode = formData.split("=")[1];
        }
      }

      setTimeout(() => {
        this.isInit = true;
      }, 0);
      let params = {};
      params.reportCode = this.reportCode;
      if (this.currencyReportPageData) {
        let currencyReportPageData = this.currencyReportPageData;

        for (var p in currencyReportPageData) {
          params[p] = currencyReportPageData[p];
        }
      }
      if (this.pathSearchData) {
        let data = this.pathSearchData;

        for (var p in data) {
          params[p] = data[p];
        }
      }
      this.tableLoading = true;
      pageApi
        .getTabData2(params)
        .then((response) => {
          if (response.data.status === 200) {
            // 关闭移动指标弹框
            if (response.data.timestamp) {
              this.timestamp = commonFun.yyr_timestampToTime(
                response.data.timestamp
              );
              // console.log(this.timestamp);
            }
            let data = response.data.data;
            this.tabInfo = data;
            if (data[0]) {
              let arr = data[0].tableList;
              if (arr && arr.length > 0) {
                this.tabArr = arr;
                this.activeName = arr[0].tableCode;
                this.isPage = arr[0].isPage;
                this.reportName = arr[0].tableCn || "";
                if (arr[0].crudEnable) {
                  this.crudEnable = arr[0].crudEnable;
                } else {
                  this.crudEnable = "-1";
                }
              } else {
                this.tabArr = [];
              }
              this.fieldsInfoArr = data[0][arr[0].tableCode];
              this.tableDataDetailArr = this.getAllPrpos(
                data[0][arr[0].tableCode],
                true
              );
              this.tableShow = true;
              this.tableLoading = false;
            }
            if (this.crudEnable.indexOf("A") != -1) {
              this.onSubmit(true, "mounted");
            }
            this.$nextTick(() => {
              // 将表格和工具栏进行关联
              const xTable = this.$refs.xTable;
              xTable.connect(this.$refs.xToolbar);
            });
          } else {
            this.$message.closeAll();
            this.$message({
              message: response.data.message || "数据初始化失败",
              type: "error",
            });
          }
        })
        .catch((err) => {
          console.log("err", err);
          this.$message.closeAll();
          this.$message({
            type: "error",
            message: err || "数据初始化失败",
          });
        });
    },
    //新增,编辑确认
    countSubmit(formName) {
      this.$refs["formCount"] &&
        this.$refs["formCount"].validate((valid) => {
          if (valid) {
            this.$message.closeAll();
            if (this.operationType === 1) {
              // 添加
              this.saveData();
            } else {
              // 修改
              this.updateParamSet();
            }
          } else {
            return false;
          }
        });
    },
    saveData() {
      this.$confirm("确定新增?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "info",
      })
        .then(() => {
          let params = {};
          params = commonFun.parameterSrc(this.formCount);
          params.tableCode = this.activeName;
          params.reportCode = this.reportCode;
          this.countSubmit_btn = true;
          if (this.currencyReportPageData) {
            let currencyReportPageData = this.currencyReportPageData;

            for (var p in currencyReportPageData) {
              params[p] = currencyReportPageData[p];
            }
          }
          if (this.pathSearchData) {
            let data = this.pathSearchData;

            for (var p in data) {
              params[p] = data[p];
            }
          }
          pageApi
            .addDataSource(params)
            .then((response) => {
              if (response.data.status === 200) {
                // 关闭移动指标弹框
                this.countDialog = false;
                this.$message.closeAll();
                this.$message({
                  message: "新增成功",
                  type: "success",
                });
                // 刷新列表
                this.onSubmit(true);
              } else {
                // 关闭移动指标弹框
                // this.countDialog = false;
                this.$message.closeAll();
                this.$message({
                  message: response.data.message || "新增失败",
                  type: "error",
                });
              }
              this.countSubmit_btn = false;
            })
            .catch(() => {
              // 关闭移动指标弹框
              //this.countDialog = false;
              this.countSubmit_btn = false;
              this.$message.closeAll();
              this.$message({
                message: "新增失败",
                type: "error",
              });
            });
        })
        .catch(() => {
          // 关闭移动指标弹框
          // this.countDialog = false;
          this.countSubmit_btn = false;
        });
    },
    updateParamSet() {
      this.$confirm("确定修改?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "info",
      })
        .then(() => {
          let params = {};
          params = this.formCount;
          this.countSubmit_btn = true;
          params.tableCode = this.activeName;
          params.reportCode = this.reportCode;
          if (this.currencyReportPageData) {
            let currencyReportPageData = this.currencyReportPageData;

            for (var p in currencyReportPageData) {
              params[p] = currencyReportPageData[p];
            }
          }
          pageApi
            .updateDataSource(params)
            .then((response) => {
              if (response.data.status === 200) {
                // 关闭移动指标弹框
                this.countDialog = false;
                this.$message.closeAll();
                this.$message({
                  message: "修改成功",
                  type: "success",
                });
                // 刷新树列表
                this.onSubmit(false);
              } else {
                // 关闭移动指标弹框
                // this.countDialog = false;
                this.$message.closeAll();
                this.$message({
                  message: response.data.message || "修改失败",
                  type: "error",
                });
              }
              this.countSubmit_btn = false;
            })
            .catch(() => {
              // 关闭移动指标弹框
              // this.countDialog = false;
              this.countSubmit_btn = false;
              this.$message.closeAll();
              this.$message({
                message: "修改失败",
                type: "error",
              });
            });
        })
        .catch(() => {
          // 关闭移动指标弹框
          // this.countDialog = false;
          this.countSubmit_btn = false;
        });
    },
    //获取下拉框内容
    getSelectData(val) {
      let params = {};
      params.fieldEn = val;
      params.tableCode = this.activeName;
      params.reportCode = this.reportCode;

      if (this.currencyReportPageData) {
        let currencyReportPageData = this.currencyReportPageData;

        for (var p in currencyReportPageData) {
          params[p] = currencyReportPageData[p];
        }
      }
      if (this.pathSearchData) {
        let data = this.pathSearchData;

        for (var p in data) {
          params[p] = data[p];
        }
      }
      pageApi
        .getSelectData(params)
        .then((response) => {
          if (response.data.status === 200) {
            // 关闭移动指标弹框
            // this.formSelectArr[val] = response.data.data;
            this.$set(this.formSelectArr, val, response.data.data);
            this.$set(this.formSelectArr2, val, response.data.data);
            for (let key in this.formSelectArr2) {
              let arr = [];
              let arr2 = [];
              this.formSelectArr2[key].forEach((item) => {
                if (!arr.includes(item.DIM_CDE)) {
                  arr.push(item.DIM_CDE);
                  arr2.push(item);
                }
              });
              this.$set(this.formSelectArr, key, arr2);
            }
            this.$set(this.editFormSelectArr, val, response.data.data);
            this.$set(this.editFormSelectArr2, val, response.data.data);
          } else {
            this.$message.closeAll();
            this.$message({
              message: response.data.message || "获取下拉内容失败",
              type: "error",
            });
          }
        })
        .catch(() => {
          // 关闭移动指标弹框

          this.$message.closeAll();
          this.$message({
            message: "获取下拉内容失败",
            type: "error",
          });
        });
    },
    //查询条件选择
    searchSubmit() {
      // console.log(this.checkedForms);

      let arr = [];
      let fieldsInfoArr = this.fieldsInfoArr;
      let params = {};
      let checkedForms = this.checkedForms;
      if (checkedForms && checkedForms.length > 0) {
        for (let i = 0; i < checkedForms.length; i++) {
          for (let j = 0; j < fieldsInfoArr.length; j++) {
            if (fieldsInfoArr[j].fieldEn == checkedForms[i]) {
              arr.push(fieldsInfoArr[j]);
              if (fieldsInfoArr[j].inputType == "select_multiple") {
                params[fieldsInfoArr[j].fieldEn] = [];
              } else {
                params[fieldsInfoArr[j].fieldEn] = "";
              }
            }
          }
        }
        params["pageSize"] = this.formInline.pageSize;
        params["pageNum"] = this.formInline.pageNum;
        this.searchDataArr = arr;
        this.formInline = params;
      }

      this.searchDialog = false;
      //
    },
    handleCheckAllChange(val) {
      this.checkedForms = val ? this.checkAllForms : [];
      this.isIndeterminate = false;
    },
    handlecheckedFormsChange(value) {
      let checkedCount = value.length;
      this.checkAll = checkedCount === this.checkAllForms.length;
      this.isIndeterminate =
        checkedCount > 0 && checkedCount < this.checkAllForms.length;
    },
    downloadFile(type) {
      this.onSubmitValidate(true);
      this.formInline.tableCode = this.activeName;
      let params = commonFun.parameterSrc(this.formInline);
      for (let key in params) {
        if (params[key].constructor == Array) {
          if (params[key].length == 1) {
            this.formSelectArr[key].forEach((item) => {
              if (item.DIM_CDE == params[key][0]) {
                params[key + "_TEXT"] = item.DIM_NME;
              }
            });
          }
        }
        if (key.indexOf("_fundCode") != -1) {
          params[key.split("_fundCode")[0]] = params[key];
        }
      }
      // console.log(params);
      params.reportCode = this.reportCode;
      params.permissions = "1";
      params.pageSize = null;
      params.pageNum = null;
      if (this.currencyReportPageData) {
        let data = this.currencyReportPageData;

        for (var p in data) {
          params[p] = data[p];
        }
      }
      if (this.pathSearchData) {
        let data = this.pathSearchData;

        for (var p in data) {
          params[p] = data[p];
        }
      }
      params.type = type;
      // params.token = this.$store.getters.token;
      params = commonFun.parameterSrc(params);
      params = JSON.stringify(params);
      // 获取表头字段
      let arr = [];
      let tableHeader = this.$refs.xTable && this.$refs.xTable.getColumns();
      if (tableHeader.length) {
        tableHeader.forEach((item) => {
          if (item.type != "seq") {
            if (item.property) {
              arr.push(item.property);
            }
          }
        });
      }
      let obj = {
        mapType: params,
        tableHeader: arr,
        token: this.$store.getters.token,
      };
      let action =
        this.$store.state.setting.baseApi + "/api/reportShow/v1.0/exportExcel";
      commonFun.formDownloadFile(obj, action, "post");
    },
    // 添加条件
    addSearchList() {
      this.searchDialog = true;
      let arr = this.searchDataArr.map((item) => {
        return item.fieldEn;
      });
      this.checkedForms = arr;
    },
    detailData(row) {
      // console.log(row);
      this.currencyReportPageData_dialog = {
        D_DATE: row.D_DATE,
        VC_FUNDCODE: row.VC_FUNDCODE,
        reportCode: "id-0db37d6-04c1-2253-a864-08b9e53a737b",
      };
      this.detailDialog = true;
      this.detail_show = true;
    },
    detailDialogClosed() {
      // this.detailDialog = false;
      this.detail_show = false;
    },

    // 查询条件下拉框事件
    getSun(val, DIM_NME, pId, p_field, c_field) {
      // console.log('父级下拉框-click',c_field,DIM_NME);
      if (DIM_NME) {
        this.formInline[p_field + "_TEXT"] = DIM_NME;
      }
      if (this.formInline[c_field]) {
        this.formInline[c_field] = "";
        this.formInline[p_field + "_TEXT"] = "";
      }
      if (this.formSelectArr2[c_field]) {
        let arr = this.formSelectArr2[c_field].filter((item) => {
          return item.DIM_PARENT_ID == pId;
        });
        this.$set(this.formSelectArr, c_field, arr);
      }
    },
    getSunClick(DIM_CDE, DIM_NME, fieldEn) {
      // console.log('普通下拉框-click');
      if (DIM_NME) {
        this.formInline[fieldEn + "_TEXT"] = DIM_NME;
      }
    },
    getSunchange(val, fieldEn, c_field) {
      // console.log('父级下拉框-change',val,fieldEn,c_field);
      if (!val) {
        // this.$set(this.formSelectArr,c_field,this.formSelectArr2[c_field]);
        let arr = [];
        let arr2 = [];
        this.formSelectArr2[c_field].forEach((item) => {
          if (!arr.includes(item.DIM_CDE)) {
            arr.push(item.DIM_CDE);
            arr2.push(item);
          }
        });
        this.$set(this.formSelectArr, c_field, arr2);
        this.formInline[fieldEn + "_TEXT"] = "";
      }
    },
    selectChange(val, field) {
      // console.log('普通下拉框-Change',val,field);
      if (!val) {
        this.formInline[field + "_TEXT"] = "";
      }
    },

    // 编辑下拉框事件
    editGetSun(val, DIM_NME, pId, p_field, c_field) {
      if (this.formCount[c_field]) {
        this.formCount[c_field] = "";
      }
      if (this.editFormSelectArr2[c_field]) {
        let arr = this.editFormSelectArr2[c_field].filter((item) => {
          return item.DIM_PARENT_ID == pId;
        });
        this.$set(this.editFormSelectArr, c_field, arr);
      }
    },
    editGetSunchange(val, fieldEn, c_field) {
      // console.log('父级下拉框-change',val,fieldEn,c_field);
      if (!val) {
        this.$set(
          this.editFormSelectArr,
          c_field,
          this.editFormSelectArr2[c_field]
        );
        // this.formCount[c_field] = '';
      }
    },
    // 新增编辑下拉框关闭
    editFormClose() {
      this.editFormSelectArr = JSON.parse(
        JSON.stringify(this.editFormSelectArr2)
      );
    },

    //金额千分位
    amountFilter(num, float) {
      if (!num && num != 0) {
        return "";
      }
      let n = Number(num);
      if (float) {
        // console.log(float);
        n = n.toFixed(float);
      }
      return commonFun.formatNumber(n);
    },
    format(val, type, format) {
      // if(!val) return ''
      if (type == "N") {
        if (format) {
          //#,###.00
          if (format.indexOf(".") != -1 && format.indexOf(",") != -1) {
            let arr = format.split(".");
            if (arr.length > 1) {
              let str = arr[arr.length - 1];
              if (str.length) {
                return this.amountFilter(val, str.length);
              }
            } else {
              return this.amountFilter(val, false);
            }
          } else {
            return val;
          }
        } else {
          return val;
        }
      }
    },
    select_multipleChange(data, field) {
      if (data.length == 0 || data.length > 1) {
        this.formInline[field + "_TEXT"] = null;
      }
    },
    // 打印
    print() {
      this.$refs.xTable && this.$refs.xTable.print();
      // this.$refs.xTable.openExport()
    },
    // 邮件
    mailmail() {
      this.mailDialog = true;
      let params = {
        reportCode: this.reportCode,
      };
      this.mailConfigDataLoading = true;
      reportToolApi
        .mailList(params)
        .then((res) => {
          this.mailConfigDataLoading = false;
          if (res.data.status === 0) {
            this.mailConfigData = res.data.data;
            if (this.mailConfigData.length === 0) {
              this.$message({
                type: "info",
                message: "此报表没有进行邮件配置，请使用自定义邮件发送功能！",
              });
            }
          } else {
            this.mailConfigData = [];
            this.$message({
              type: "error",
              message: res.data.message || "加载邮件配置失败！",
            });
          }
        })
        .catch(() => {
          this.mailConfigDataLoading = false;
        });
    },
    // 自定义邮件
    customMail() {
      // 获取表头字段
      let arr = [];
      let tableHeader = this.$refs.xTable && this.$refs.xTable.getColumns();
      if (tableHeader.length) {
        tableHeader.forEach((item) => {
          if (item.type != "seq") {
            arr.push(item.property);
          }
        });
      }
      this.headerArr = arr;
      this.customMailDialog = true;
      this.sendMailForm_show = true;
      this.$nextTick(() => {
        this.$refs.sendMailForm &&
          this.$refs.sendMailForm.init(this.formInline);
      });
    },
    handleCurrentChange(val) {
      // console.log('handleCurrentChange',val);
      if (val) {
        this.mailId = val.id;
      }
    },
    sendMail() {
      if (!this.mailId) {
        this.$message({
          type: "warning",
          message: "请选择一条配置！",
        });
        return;
      }
      let params = {
        id: this.mailId,
        tableCode: this.activeName,
      };
      this.send_loading = true;
      reportToolApi.sendMail(params).then((res) => {
        this.send_loading = false;
        if (res.data.status === 200) {
          this.$message({
            type: "success",
            message: "发送成功！",
          });
          this.mailDialog = false;
        } else {
          this.$message({
            type: "error",
            message: res.data.message || "发送失败！",
          });
        }
      });
    },
    // 关闭邮件发送
    mailDialogClosed() {
      this.mailConfigData = [];
      this.mailId = "";
      this.rowObj = {};
      this.send_loading = false;
    },
    // 关闭自定义邮件发送
    customMailDialogClosed() {
      this.sendMailForm_show = false;
    },
  },
};
</script>

<style lang="scss" scoped>
.page-card-common {
  min-height: 0px;
  padding: 0px;
}
</style>

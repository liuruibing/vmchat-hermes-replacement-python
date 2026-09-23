<template>
  <div class="per-report-record">
    <!-- 第一层tab选择 -->
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="全部" name="All"></el-tab-pane>
      <el-tab-pane label="季报" name="Q"> </el-tab-pane>
      <el-tab-pane label="半年报" name="S"> </el-tab-pane>
      <el-tab-pane label="年报" name="Y"> </el-tab-pane>
    </el-tabs>
    <!-- 第二层tab选择 -->
    <el-tabs v-model="activeName2" @tab-click="handleClick2">
      <el-tab-pane label="全部" name="All"></el-tab-pane>
      <el-tab-pane label="文本待录入" name="5"> </el-tab-pane>
      <el-tab-pane label="待生成" name="0"> </el-tab-pane>
      <el-tab-pane label="待传送" name="6"> </el-tab-pane>
      <el-tab-pane label="待复核" name="2"> </el-tab-pane>
      <el-tab-pane label="已完成" name="4"> </el-tab-pane>
    </el-tabs>
    <el-form
      :inline="true"
      ref="formInline"
      :model="formInline"
      label-width="100px"
      style="margin-bottom: 8px"
      class="demo-form-inline form_inline_search currency_report_old_form"
    >
      <el-row>
        <el-col :span="18">
          <div style="width: 100%">
            <!-- <el-form-item label="产品" prop="fundCode">
              <select-table
                v-model="formInline.fundCode"
                @enter="onSubmit(true)"
              ></select-table>
            </el-form-item> -->
            <el-form-item label="产品" prop="fundCodes">
              <multipleSelectTable
                class="multipleSelectTable"
                v-model="formInline.fundCodes"
                :data="fundList"
                :Columns="Columns"
                idField="fundCode"
                nameField="codeName"
                placeholder="请选择"
              ></multipleSelectTable>
            </el-form-item>
            <el-form-item label="产品类型" prop="fundType">
              <el-select
                clearable
                v-model="formInline.fundType"
                size="small"
                placeholder="请选择"
              >
                <el-option
                  v-for="(group, index) in fundTypeArr"
                  :value="group.dimCde"
                  :key="index"
                  :label="group.dimNme"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="6">
          <el-form-item class="search_button_com">
            <el-button
              type="primary"
              @click="onSubmit(true)"
              style="margin-bottom: 5px"
              size="small"
            >
              查询
            </el-button>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-form-item label="勾稽校验" prop="statusDataValid">
          <el-select
            clearable
            v-model="formInline.statusDataValid"
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="(group, index) in name3Arr"
              :value="group.code"
              :key="index"
              :label="group.name"
            >
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="核对状态" prop="statusFileVerify">
          <el-select
            clearable
            v-model="formInline.statusFileVerify"
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="(group, index) in name2Arr"
              :value="group.code"
              :key="index"
              :label="group.name"
            >
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item :label="activeName=='All'?'估值基准日':'报告年度'" prop="reportDate">
          <el-date-picker
            v-show="reportTypeOther_year"
            v-model="reportYear"
            type="year"
            editable
            size="small"
            value-format="yyyy"
            placeholder="选择年"
          >
          </el-date-picker>

          <el-select
            v-show="reportTypeOther_show"
            clearable
            v-model="selectDate"
            size="small"
            placeholder="请选择"
          >
            <el-option
              v-for="(group, index) in reportTypeArr2"
              :value="group.value"
              :key="index"
              :label="group.name"
            >
            </el-option>
          </el-select>

          <el-date-picker
            v-show="reportTypeOther_day"
            v-model="formInline.dateData"
            type="date"
            editable
            size="small"
            value-format="yyyy-MM-dd"
            placeholder="选择日期"
          >
          </el-date-picker>
        </el-form-item>
      </el-row>
    </el-form>

    <div style="display: flex">
      <div class="forms_table_title">
        <i class="el-icon-s-data"></i>列表数据
      </div>
      <el-row>
        <el-col style="min-width: 800px; text-align: right">
          <!-- <el-button
            type="primary"
            @click="handleDataEntry()"
            style="margin-bottom: 5px"
            size="small"
          >
            数据录入
          </el-button> -->
          <el-button
            type="primary"
            @click="handleGenera()"
            style="margin-bottom: 5px"
            size="small"
            :loading="btn_loading2"
          >
            生成数据
          </el-button>
          
          <el-button
            type="primary"
            @click="handleCheck()"
            style="margin-bottom: 5px"
            size="small"
            :loading="btn_loading2"
          >
            勾稽校验
          </el-button>
          <el-button
            type="primary"
            @click="handleCheckOut()"
            style="margin-bottom: 5px"
            size="small"
            :loading="btn_loading2"
          >
            与外包核对
          </el-button>
          <el-button
            type="primary"
            @click="handleDataSend()"
            style="margin-bottom: 5px"
            size="small"
            :loading="btn_loading2"
          >
            数据传送
          </el-button>
          <el-button
            type="primary"
            size="small"
            @click="batchLock()"
            :loading="btn_loading2"
            >批量锁定</el-button
          >
          <el-button
            type="primary"
            size="small"
            @click="batchUnlock()"
            :loading="btn_loading2"
            >批量解锁</el-button
          >
          <el-button
            type="primary"
            @click="handleReviewConfirm()"
            style="margin-bottom: 5px"
            size="small"
            :loading="btn_loading2"
          >
            复核确认
          </el-button>
          <el-button
            type="primary"
            @click="downloadReport()"
            style="margin-bottom: 5px"
            size="small"
            :loading="btn_loading2"
          >
            下载报表
          </el-button>
        </el-col>
      </el-row>
    </div>
    <el-table
      ref="multipleTable"
      @selection-change="handleSelectionChange"
      :data="tableData"
      border
      stripe
      @sort-change="handleSortChange"
      v-loading="tableLoading"
      style="width: 100%"
      height="calc(100% - 266px)"
    >
      <el-table-column fixed type="selection" width="35"></el-table-column>

      <el-table-column
        prop="fundCode"
        label="产品代码"
        align="left"
        header-align="center"
        min-width="120"
        sortable="custom"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fundCode | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="fundTypeName"
        label="产品类型"
        align="left"
        header-align="center"
        min-width="120"
        sortable="custom"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fundTypeName | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="fundState"
        label="产品状态"
        align="left"
        header-align="center"
        min-width="120"
        sortable="custom"
      >
        <template slot-scope="scope">
          <span>{{ dataStatus(scope.row.fundState, "1") | noDataFilter }}</span>
        </template>
      </el-table-column>
      <!-- <el-table-column
        prop="reportFrequency"
        label="报告频率"
        align="left"
        header-align="center"
        min-width="120"
        sortable="custom"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.reportFrequency === 'D'">日报</span>
          <span v-else-if="scope.row.reportFrequency === 'W'">周报</span>
          <span v-else-if="scope.row.reportFrequency === 'M'">月报</span>
          <span v-else-if="scope.row.reportFrequency === 'Q'">季报</span>
          <span v-else-if="scope.row.reportFrequency === 'S'">半年报</span>
          <span v-else-if="scope.row.reportFrequency === 'Y'">年报</span>
          <span v-else>{{ scope.row.reportFrequency | noDataFilter }}</span>
        </template>
      </el-table-column> -->
      <el-table-column
        prop="dateYear"
        label="报告年度"
        align="left"
        header-align="center"
        min-width="120"
        sortable="custom"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.dateYear | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="statusReport"
        label="报告状态"
        align="left"
        header-align="center"
        min-width="120"
        sortable="custom"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.statusReport === '0'">待生成</span>
          <span v-else-if="scope.row.statusReport === '1'">已生成</span>
          <span v-else-if="scope.row.statusReport === '2'">待复核</span>
          <span v-else-if="scope.row.statusReport === '3'">待报送</span>
          <span v-else-if="scope.row.statusReport === '4'">已完成</span>
          <span v-else>{{ scope.row.statusReport | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="statusDataSend"
        label="传送状态"
        align="left"
        header-align="center"
        min-width="120"
        sortable="custom"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.statusDataSend == 0">未传送</span>
          <span v-else-if="scope.row.statusDataSend == 1">传送成功</span>
          <span v-else-if="scope.row.statusDataSend == 2">传送失败</span>
          <span v-else>{{ scope.row.statusDataSend | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="statusDataValid"
        label="勾稽校验"
        align="left"
        header-align="center"
        min-width="120"
        sortable="custom"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.statusDataValid === '0'">未校验</span>
          <span v-else-if="scope.row.statusDataValid === '1'">校验成功</span>
          <span style="color: red" v-else-if="scope.row.statusDataValid === '2'"
            >校验失败</span
          >
          <span v-else>{{ scope.row.statusDataValid | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="statusFileVerify"
        label="核对状态"
        align="left"
        header-align="center"
        min-width="120"
        sortable="custom"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.statusFileVerify === '0'">未核对</span>
          <span v-else-if="scope.row.statusFileVerify === '1'">核对一致</span>
          <span
            style="color: red"
            v-else-if="scope.row.statusFileVerify === '2'"
            >核对不一致</span
          >
          <span v-else>{{ scope.row.statusFileVerify | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="statusReportConfirm"
        label="复核状态"
        align="left"
        header-align="center"
        min-width="120"
        sortable="custom"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.statusReportConfirm === '0'">未复核</span>
          <span v-else-if="scope.row.statusReportConfirm === '1'">已复核</span>
          <span
            style="color: red"
            v-else-if="scope.row.statusReportConfirm === '2'"
            >复核失败</span
          >
          <span v-else>{{ scope.row.statusReportConfirm | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="dateData"
        label="估值基准日"
        align="left"
        header-align="center"
        min-width="120"
        sortable="custom"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.dateData | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="dateSubmitFinal"
        label="上报截止日"
        align="left"
        header-align="center"
        min-width="140"
        sortable="custom"
      >
        <template slot-scope="scope">
          <span>{{
            ((scope.row.dateSubmitFinal || "") +
              " " +
              (scope.row.dateSubmitFinalTime || ""))
              | noDataFilter
          }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="one12"
        label="操作"
        fixed="right"
        align="center"
        min-width="460"
      >
        <template slot-scope="scope">
          <el-button
            plain
            type="primary"
            size="small"
            @click="handleDataEntry(scope.row)"
            :disabled="btn_disabled"
            >文本编辑</el-button
          >
          
          <!-- <el-button plain type="primary" size="small" @click="editData(scope.row)">编辑</el-button> -->
          <el-button
            v-if="scope.row.statusReportConfirm == '1'"
            plain
            type="primary"
            size="small"
            @click="reportConfirmCancel(scope.row)"
            :disabled="btn_disabled"
            >取消复核</el-button
          >
          <el-button plain type="primary" size="small" @click="jymx(scope.row)" :disabled="btn_disabled"
            >勾稽校验明细</el-button
          >
          <el-button plain type="primary" size="small" @click="hdmx(scope.row)" :disabled="btn_disabled"
            >与外包核对明细</el-button
          >
          <el-button plain type="primary" size="small" @click="czrz(scope.row)" :disabled="btn_disabled"
            >操作日志</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <div>
      <Pagination
        :total="total"
        :page="formInline.pageNum"
        :limit="formInline.pageSize"
        @pagination="Pagination"
      ></Pagination>
    </div>

    <!-- 数据录入dialog -->
    <el-dialog
      custom-class="wblr_dialog"
      title="文本编辑"
      width="75% !important"
      center
      :visible.sync="sjlrDialog"
      :close-on-click-modal="false"
    >
      <el-container>
        <el-main>
          <el-row style="height: 100%">
            <el-col :span="12" style="height: 100%">
              <div class="baobiao_name">{{ baobiao_name }}</div>
              <el-tree
                ref="dataTree"
                class="dataTrees"
                :data="treeData"
                node-key="id"
                :props="{ label: 'txtName', children: 'children' }"
                :expand-on-click-node="false"
                :render-content="renderContent"
                :indent="40"
                accordion
                @node-click="nodeClick"
                :default-expanded-keys="defaultexpandedkeys"
              >
              </el-tree>
            </el-col>
            <el-col :span="12" style="height: 100%">
              <div style="margin-left: 20px">
                <el-button type="primary" size="small" @click="calculate" :disabled="!text_show" :loading="btn_loading"
                  >计算</el-button
                >
                <el-button type="primary" size="small" @click="saveTxt" :loading="btn_loading"
                  >保存</el-button
                >
                <el-button type="primary" size="small" @click="lockTxt" :loading="btn_loading"
                  >锁定</el-button
                >
                <el-button type="primary" size="small" @click="unlockTxt" :loading="btn_loading"
                  >解锁</el-button
                >
                <el-button
                  type="primary"
                  size="small"
                  plain
                  icon="el-icon-download"
                  @click="tempDownload"
                  >模板下载</el-button
                >
                <el-upload
                  class="file_upload"
                  ref="upload"
                  accept=".xls"
                  action=""
                  :disabled="uploadLoading"
                  :file-list="fileList"
                  :limit="1"
                  :on-exceed="onExcedd"
                  :on-change="handleChange"
                  :on-remove="handleRemove"
                  :http-request="httpRequest"
                  :auto-upload="true"
                >
                  <el-button
                    slot="trigger"
                    size="small"
                    plain
                    type="primary"
                    icon="el-icon-upload2"
                    :loading="uploadLoading"
                    >文件导入{{ uploadLoading ? "中" : "" }}</el-button
                  >
                  <!-- <el-button slot="trigger" size="small" plain type="primary" icon="el-icon-folder-opened">选取文件</el-button> -->
                  <!-- <el-button style="margin-left: 10px;" plain size="small" type="primary" icon="el-icon-upload2" @click="submitUpload">文件上传</el-button> -->
                  <!-- <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div> -->
                </el-upload>
              </div>
              <div
                v-if="text_show"
                class="right-textarea textarea1"
                v-loading="textareaLoading"
                style=""
              >
                <el-input
                  type="textarea"
                  placeholder="请输入内容"
                  v-model="textarea1"
                  :autosize="{ minRows: 15 }"
                  maxlength="1000"
                  show-word-limit
                  :disabled="disable"
                >
                </el-input>
              </div>
              <div
                v-if="!text_show"
                class="right-textarea vxetextarea"
                v-loading="textareaLoading"
              >
                <!-- <div>
                  <el-button
                    type="success"
                    plain
                    @click="insertEvent"
                    style="margin-bottom: 5px; margin-left: 20px"
                    size="small"
                  >
                    <i class="el-icon-circle-plus-outline"></i>新增
                  </el-button>
                  <el-button
                    type="danger"
                    plain
                    @click="removeEvent"
                    style="margin-bottom: 5px"
                    size="small"
                  >
                    <i class="el-icon-delete"></i>移除
                  </el-button>
                </div> -->
                <vxe-toolbar perfect style="height:40px;border-bottom: none !important;" v-if="!disable">
                  <template slot="buttons" slot-scope="scope">
                    <vxe-button icon="fa fa-plus" status="perfect" @click="insertEvent">新增</vxe-button>
                    <vxe-button icon="fa fa-trash-o" status="perfect" @click="removeEvent">移除</vxe-button>
                    <!-- <vxe-button icon="fa fa-save" status="perfect" @click="saveEvent">保存</vxe-button>
                    <vxe-button icon="fa fa-mail-reply" status="perfect" @click="revertEvent">还原</vxe-button> -->
                  </template>
                </vxe-toolbar>
                <vxe-table
                  class="vxeTable"
                  :cell-class-name="cellClassName"
                  :header-cell-class-name="headerCellClassName"
                  highlight-hover-row
                  keep-source
                  border
                  stripe
                  resizable
                  auto-resize
                  size="mini"
                  ref="xTable"
                  :edit-config="{ trigger: !disable?'click':'', mode: 'cell', showIcon: false, }"
                  :scroll-x="{ enabled: false }"
                  :data="VXEtableData"
                  max-height="450"
                >
                  <vxe-table-column v-if="!disable" type="checkbox" width="40" align="center"></vxe-table-column>
                  <vxe-table-column
                    show-header-overflow="title"
                    v-for="group in tableDataDetailArr"
                    :key="group.fieldEn"
                    min-width="160"
                    header-align="center"
                    :edit-render="{}"
                    :field="group.fieldEn"
                    :title="group.fieldCn"
                  >
                    <template slot="edit" slot-scope="{ row }">
                      <template v-if="group.inputType == 'input'">
                        <!-- <vxe-input type="text" v-model="row[group.fieldEn]"></vxe-input> -->
                        <el-input
                          type="textarea"
                          v-model="row[group.fieldEn]"
                          autosize
                        ></el-input>
                      </template>
                      <template v-else-if="group.inputType == 'date'">
                        <vxe-input
                          v-model="row[group.fieldEn]"
                          placeholder="日期选择"
                          type="date"
                          transfer
                        ></vxe-input>
                      </template>
                      <template v-else-if="group.inputType == 'select'">
                        <vxe-select
                          v-model="row[group.fieldEn]"
                          placeholder="请选择"
                          transfer
                        >
                          <vxe-option
                            v-for="item in formSelectArr[group.fieldEn]"
                            :key="item.DIM_CDE"
                            :value="item.DIM_CDE"
                            :label="item.DIM_NME"
                          ></vxe-option>
                        </vxe-select>
                      </template>
                      <template v-else>
                        <!-- <vxe-input type="text" v-model="row[group.fieldEn]"></vxe-input> -->
                        <el-input
                          type="textarea"
                          v-model="row[group.fieldEn]"
                          autosize
                        ></el-input>
                      </template>
                    </template>
                    <template slot="default" slot-scope="{ row }">
                      <template>
                        <span>{{ row[group.fieldEn] }}</span>
                      </template>
                    </template>
                  </vxe-table-column>
                </vxe-table>
              </div>
            </el-col>
          </el-row>
        </el-main>
      </el-container>
    </el-dialog>
    <!-- 核对明细dialog -->
    <el-dialog
      :title="dialogTitle"
      :before-close="handleClose"
      :fullscreen="checkDetails_show"
      :custom-class="checkDetails_show ? 'checkDetails_dialog' : ''"
      width="80% !important"
      center
      :visible.sync="czrzDialog"
      :close-on-click-modal="false"
    >
      <el-container>
        <el-main class="mainBox">
          <!-- 核对明细 -->
          <annExcelPage
            v-if="annExcelPage_show"
            :PageData="PageData"
          ></annExcelPage>
          <annXmlPage v-if="annXmlPage_show" :PageData="PageData"></annXmlPage>
          <annTxtPage v-if="annTxtPage_show" :PageData="PageData"></annTxtPage>
          <!-- 核对明细-新 （左边章节树，右边列表） -->
          <checkDetails
            v-if="checkDetails_show"
            :PageData="PageData1"
          ></checkDetails>
          <!-- 操作日志 -->
          <annLogPage v-if="annLogPage_show" :PageData="PageData"></annLogPage>
          <!-- 编辑-配置化页面 -->
          <currencyReportPage
            v-if="currencyReportPage_show"
            :currencyReportPageData="currencyReportPageData"
          ></currencyReportPage>
          <!-- 校验明细 -->
          <checkDetailPage
            v-if="checkDetailPage_show"
            :PageData="PageData"
          ></checkDetailPage>
        </el-main>
      </el-container>
    </el-dialog>

    <!-- 复核确认 -->
    <el-dialog
      title="复核确认"
      customClass="qrfuListWidth"
      center
      :visible.sync="countDialog"
      :close-on-click-modal="false"
    >
      <el-container>
        <el-main class="">
          <el-form
            ref="formCount"
            :model="formCount"
            :rules="countRules"
            label-position="right"
            label-width="120px"
          >
            <el-form-item label="复核确认意见" prop="confirmOpinion">
              <el-input
                type="textarea"
                :autosize="{ minRows: 4 }"
                maxlength="1000"
                show-word-limit
                placeholder="请输入内容"
                v-model="formCount.confirmOpinion"
              >
              </el-input>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="countDialog = false" :loading="btn_loading2">取 消</el-button>
        <el-button type="primary" size="small" @click="countSubmit('formCount')" :loading="btn_loading2"
          >确 定</el-button
        >
      </div>
    </el-dialog>

    <!-- 取消复核dialog -->
    <el-dialog
      title="复核确认"
      customClass="qrfuListWidth"
      center
      :visible.sync="reportConfirmCancelDialog"
      :close-on-click-modal="false"
    >
      <el-container>
        <el-main class="mainBox">
          <el-form
            ref="formCount"
            :model="formCount"
            :rules="countRules"
            label-position="right"
            label-width="120px"
          >
            <el-form-item label="取消复核说明" prop="confirmCancelOpinion">
              <el-input
                v-model="formCount.confirmCancelOpinion"
                type="textarea"
                auto-complete="off"
                maxlength="1000"
                show-word-limit
                :autosize="{ minRows: 2 }"
                placeholder="请输入"
              />
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="reportConfirmCancelDialog = false"
          :loading="btn_loading2"
          >取 消</el-button
        >
        <el-button
          type="primary"
          size="small"
          @click="reportConfirmCancelSubmit('formCount')"
          :loading="btn_loading2"
          >确 定</el-button
        >
      </div>
    </el-dialog>
  </div>
</template>

<script>
import selectTable from "@/views/commonComponents/selectTable.vue";
import Pagination from "@/components/Pagination";
import commonFun from "@/filters/new_common";
import pageApi from "@/api/xbrl/xbrl";
import store from "@/store";
import annExcelPage from "./annExcel.vue";
import annXmlPage from "./annXml.vue";
import annTxtPage from "./annTxt.vue";
import annLogPage from "./annLog.vue";
import checkDetails from "./checkDetails.vue";
import currencyReportPage from "@/views/dataReport/currencyReport";
import currencyReportApi from "@/api/dataReport/currencyReport";
import checkDetailPage from "./checkDetail.vue";
import multipleSelectTable from "@/views/commonComponents/multiple-select-table2";
import bizBeginApi from '@/api/transfer/bizBegin'
// 新更改pageView
// import CurrencyReportPageNew from './currencyReport/currencyReoportTree'

export default {
  name: "perReportRecord",
  components: {
    Pagination,
    annExcelPage,
    annXmlPage,
    annTxtPage,
    annLogPage,
    checkDetails,
    currencyReportPage,
    // CurrencyReportPageNew,
    selectTable,
    checkDetailPage,
    multipleSelectTable, //产品多选
  },
  data() {
    return {
      btn_disabled:false,
      fundList:[],
      Columns: [
        { label: "产品", prop: "codeName" },
        { label: "托管机构", prop: "trustorName" },
        { label: "基金服务机构", prop: "operatorName" },
      ],
      rowData: {}, //列表行数据
      rowId: "", //列表数据id
      elementId: "", //章节elementId
      node_obj: {}, //章节obj（只有子节点）
      nodeObj: {}, //包含父节点
      txtId: "", //章节id
      txtPid: "", //章节父id
      textareaLoading: false,
      disable: false,
      // 数据录入dialog树形图数据
      baobiao_name: "",
      treeData: [],
      defaultexpandedkeys: [], //默认展开
      tableLoading: false,
      // dialog文本输入框
      textarea1: "",
      text_show: true,
      uploadLoading: false,
      fileList: [],
      // 控制dialog变量
      sjlrDialog: false,
      czrzDialog: false,
      annLogPage_show: false,

      // 控制tab变量定义
      activeName: "All",
      activeName2: "All",

      // 查询条件定义
      formInline: {
        reportType: "XBRL", //报告类型
        fundCodes: [], // 产品代码
        // fundCode: "", // 产品代码
        fundType: "", // 产品类型
        statusDataValid: "", // 勾稽校验
        statusFileVerify: "", // 核对状态
        dateData: "", // 估值基准日
        pageSize: 50,
        pageNum: 1,
        orderString: "",
        reportFrequency: "",
        statusReport: "",
        statusDataSend: "",
        statusDataInput: "",
      },
      total: 0,

      // 控制显示变量定义
      reportTypeOther_year: false, // 按照年选择估值日
      reportTypeOther_show: false, // 季报
      reportTypeOther_day: true, //  按照日期选择估值日

      // 估值日组件绑定的对象
      reportYear: "",
      selectDate: "",

      // 控制下拉菜单显示内容定义
      name2Arr: [
        //核对状态
        { name: "未核对", code: "0" },
        { name: "核对一致", code: "1" },
        { name: "核对不一致", code: "2" },
      ],
      name3Arr: [
        //勾稽校验
        { name: "未校验", code: "0" },
        { name: "校验成功", code: "1" },
        { name: "校验失败", code: "2" },
      ],
      quarters: [
        { name: "一季度", value: "1" },
        { name: "二季度", value: "2" },
        { name: "三季度", value: "3" },
        { name: "四季度", value: "4" },
      ],

      fundTypeArr: [
        { dimNme: "所有产品", dimCde: "ALL" },
        { dimNme: "公募产品", dimCde: "GJ" },
        { dimNme: "资管计划", dimCde: "ZH" },
      ], // 产品类型 -- 从字典内查询
      reportTypeArr2: [],

      tableData: [],
      tableMultipleSelection: [],

      dialogTitle: "",
      dialogWidth: "",
      fundStatusArr: {},

      // 核对明细dialog变量
      annExcelPage_show: false,
      annXmlPage_show: false,
      annTxtPage_show: false,
      checkDetails_show: false,
      // 编辑（配置化页面）
      currencyReportPage_show: false,
      // 校验明细
      checkDetailPage_show: false,
      currencyReportPageData: {},
      PageData: {
        recordId: "",
      },
      PageData1: {},
      countDialog: false,
      // 取消复核dialog变量
      reportConfirmCancelDialog: false,
      reportRecordId: "",
      formCount: {
        confirmOpinion: "",
        confirmCancelOpinion: "",
      },
      countRules: {
        confirmOpinion: {
          required: true,
          type: "string",
          message: "请输入复核确认意见",
          trigger: "blur",
        },
        confirmCancelOpinion: {
          required: true,
          message: "请输入取消复核说明",
          trigger: "change",
        },
      },
      btn_loading:false,
      btn_loading2:false,
      VXEtableData: [
        // { aaa: "111", bbb: "222", ccc: "333" },
        // { aaa: "111", bbb: "222", ccc: "333" },
        // { aaa: "111", bbb: "222", ccc: "333" },
      ],
      tableDataDetailArr: [
        // { fieldEn: "aaa", fieldCn: "AAA", inputType: "input" },
        // { fieldEn: "bbb", fieldCn: "BBB", inputType: "select" },
        // { fieldEn: "ccc", fieldCn: "CCC", inputType: "input" },
      ],
      vxeTableCode:"",
      vxeReportCode:"0555",
      formSelectArr: {},
    };
  },
  // watch:{
  //   checkDetails_show(data){
  //     if(data){
  //       this.dialogWidth = "100% !important"
  //     }else{
  //       this.dialogWidth = "80% !important"
  //     }
  //   }
  // },
  mounted() {
    this.getFundList(); // 产品多选数据
    this.getSelects("fundinfo_fundState");
    this.onSubmit(true);
  },
  // 定义方法
  methods: {
    cellClassName({ row, rowIndex, column, columnIndex }) {
      return "vxe-cell-class-name";
    },
    headerCellClassName({ column, columnIndex }) {
      return "vxe-header-cell-class-name";
    },
    // 产品多选数据
    getFundList(){
      bizBeginApi.getProductFund().then(({ data: res }) =>{
        if(res.status === 200){
          let temp = [...res.data]
          for (let i of temp) { i['codeName'] = i.fundCode + "_"+ i.fundName }
          this.fundList = temp
        } else this.$message.error('查询产品信息失败');
      }).catch((err) => { this.$message.error('查询产品信息失败') })
    },
    //数据字典转换
    dataStatus(statusCode, flag) {
      if (flag === "1") {
        return this.fundStatusArr[statusCode];
      }
    },
    renderContent(h, { node, data, store }) {
      // console.log(node,data,store);
      return (
        <span class="custom-tree-node">
          <span title={node.label}>
            {data.elementId
              ? `${node.label}(${data.elementId})`
              : `${node.label}`}
          </span>
        </span>
      );
    },
    nodeClick(obj, node, eve) {
      // console.log("nodeClick", obj);
      // console.log(obj,node,eve);
      this.nodeObj = obj;
      if (!obj.children) {
        // console.log(obj.id);
        this.node_obj = obj;
        this.elementId = obj.elementId;
        this.txtId = obj.txtId;
        this.txtPid = obj.txtPid;
        this.textarea1 = "";
        let rowId = this.rowId;
        let elementId = obj.elementId;
        if (obj.fIsMany == "1") {
          this.text_show = false;
          this.getJjjlData(obj);
          // return
        } else {
          this.text_show = true;
        }
        let params = {
          recordId: rowId,
          elementId: elementId,
          txtId: obj.txtId,
          txtPid: obj.txtPid,
        };
        // console.log(params);
        this.textareaLoading = true;
        pageApi
          .getTreeTxt(params)
          .then((res) => {
            if (res.data.status == 0) {
              if (res.data.data) {
                let data = res.data.data;
                this.textarea1 = data.txtValue || "";
                if (data.status == "1") {
                  this.disable = true;
                } else {
                  this.disable = false;
                }
              } else {
                this.textarea1 = "";
                this.disable = false;
              }
            } else {
              this.$message({
                type: "error",
                message: res.data.message || "获取数据失败",
              });
            }
            this.textareaLoading = false;
          })
          .catch(() => {
            this.$message({
              type: "error",
              message: "获取数据失败",
            });
            this.textareaLoading = false;
          });
      }
    },
    calculate() {
      // this.$message.closeAll();
      // this.$message({
      //   type:"error",
      //   message:"功能暂未开放！"
      // })
      let params = {
        recordId: this.rowId,
        elementId: this.elementId,
      };
      this.textareaLoading = true;
      pageApi
        .createTxt(params)
        .then((res) => {
          this.textareaLoading = false;
          if (res.data.status == 0) {
            if (res.data.data) {
              this.textarea1 = res.data.data.txtValue;
            }
          } else {
            this.$message.closeAll();
            this.$message({
              type: "error",
              message: res.data.message || "计算失败！",
            });
          }
        })
        .catch(() => {
          this.textareaLoading = false;
        });
    },
    saveTxt() {
      if (this.disable) {
        this.$message.closeAll();
        this.$message({
          type: "error",
          message: "当前标签文本已锁定，不能进行保存！",
        });
        return;
      }
      if(this.text_show){
        this.saveText();
      }else{
        this.saveTable();
      }
      // let params = {
      //   recordId: this.rowId,
      //   elementId: this.elementId,
      //   txtId: this.txtId,
      //   txtPid: this.txtPid,
      //   txtValue: this.textarea1,
      // };
      // // console.log(params);
      // this.textareaLoading = true;
      // pageApi
      //   .updateTxt(params)
      //   .then((res) => {
      //     if (res.data.status == 0) {
      //       this.$message.closeAll();
      //       this.$message({
      //         type: "success",
      //         message: "保存成功！",
      //       });
      //     } else {
      //       this.$message({
      //         type: "error",
      //         message: res.data.message || "保存失败！",
      //       });
      //     }
      //     this.textareaLoading = false;
      //   })
      //   .catch((err) => {
      //     this.textareaLoading = false;
      //     this.$message({
      //       type: "error",
      //       message: err,
      //     });
      //   });
    },
    saveText(){
      let params = {
        recordId: this.rowId,
        elementId: this.elementId,
        txtId: this.txtId,
        txtPid: this.txtPid,
        txtValue: this.textarea1,
      };
      // console.log(params);
      this.textareaLoading = true;
      this.btn_loading = true;
      pageApi
        .updateTxt(params)
        .then((res) => {
          if (res.data.status == 0) {
            this.$message.closeAll();
            this.$message({
              type: "success",
              message: "保存成功！",
            });
          } else {
            this.$message({
              type: "error",
              message: res.data.message || "保存失败！",
            });
          }
          this.textareaLoading = false;
          this.btn_loading = false;
        })
        .catch((err) => {
          this.textareaLoading = false;
          this.btn_loading = false;
        });
    },
    saveTable(){
      let Recordset = this.$refs.xTable.getRecordset();
      let insertRecords = Recordset.insertRecords;
      let removeRecords = Recordset.removeRecords;
      let updateRecords = Recordset.updateRecords;
      let arr1 = [];
      let tableDataDetailArr = this.tableDataDetailArr;
      for(let i = 0;i<tableDataDetailArr.length;i++){
        for(let j=0;j<insertRecords.length;j++){
          if(insertRecords[j][tableDataDetailArr[i]['fieldEn']]) {
            arr1.push(insertRecords[j])
          }
        }
      }
      let insertRecords1 = Array.from(new Set(arr1));
      insertRecords1.forEach(item=>{
        item.tableCode = this.vxeTableCode;
        item.reportCode = this.vxeReportCode;
        item.recordId = this.rowId;
      })
      removeRecords.forEach(item=>{
        item.tableCode = this.vxeTableCode;
        item.reportCode = this.vxeReportCode;
        item.recordId = this.rowId;
      })
      updateRecords.forEach(item=>{
        item.tableCode = this.vxeTableCode;
        item.reportCode = this.vxeReportCode;
        item.recordId = this.rowId;
      })
      let arr = [
        {recordId:this.rowId}
      ]
      let params = {}
      params.insertRecords=insertRecords1;
      params.removeRecords=removeRecords;
      params.updateRecords=updateRecords;
      params.recordId=arr;

      // console.log(params);
      this.btn_loading = true;
      currencyReportApi
        .editOnPageTxt(params)
        .then(res=>{
          this.btn_loading = false;
          if(res.data.status===200){
            this.$message({type: 'success',message: '保存成功！'});
            this.getJjjlData(this.node_obj);
          }else{
            this.$message({type: 'error',message: res.data.message || '保存失败！'});
          }
        })


    },
    lockTxt() {
      // if (this.disable) {
      //   this.$message.closeAll();
      //   this.$message({
      //     type: "error",
      //     message: "已锁定，不需重复操作！",
      //   });
      //   return;
      // }
      if(!this.nodeObj.elementId){
        this.$message.closeAll();
        this.$message({
          type: "warning",
          message: "请选择要锁定的章节",
        });
        return; 
      }
      let params = {
        recordId: this.rowId,
        elementId: this.nodeObj.elementId,
      };
      pageApi.lockTxt(params).then((res) => {
        if (res.data.status == 0) {
          this.disable = true;
          this.$message.closeAll();
          this.$message({
            type: "success",
            message: "锁定成功！",
          });
        } else {
          // this.disable = false;
          this.$message({
            type: "error",
            message: res.data.message || "锁定失败！",
          });
        }
      });
    },
    unlockTxt() {
      // if (!this.disable) {
      //   this.$message.closeAll();
      //   this.$message({
      //     type: "error",
      //     message: "未锁定，无需解锁！",
      //   });
      //   return;
      // }
      if(!this.nodeObj.elementId){
        this.$message.closeAll();
        this.$message({
          type: "warning",
          message: "请选择要解锁的章节",
        });
        return; 
      }
      let params = {
        recordId: this.rowId,
        elementId: this.nodeObj.elementId,
      };
      pageApi.unlockTxt(params).then((res) => {
        if (res.data.status == 0) {
          this.disable = false;
          this.$message.closeAll();
          this.$message({
            type: "success",
            message: "解锁成功！",
          });
        } else {
          // this.disable = true;
          this.$message({
            type: "error",
            message: res.data.message || "解锁失败！",
          });
        }
      });
    },
    handleSelectionChange(val) {
      this.tableMultipleSelection = val;
    },
    handleSortChange(val) {
      // console.log(val);
      this.formInline.orderString = commonFun.orderByString(val);
      this.onSubmit(false);
    },
    handleClose(done) {
      done();
      this.annExcelPage_show = false;
      this.annXmlPage_show = false;
      this.annTxtPage_show = false;
      this.annLogPage_show = false;
      this.currencyReportPage_show = false;
      this.checkDetailPage_show = false;
      this.checkDetails_show = false;
    },
    handleClick(val) {
      // console.log(val.name,val.label);
      this.reportTypeChange(val.name);
      this.formInline.dateData = "";
      this.formInline.reportFrequency = val.name;
      if (val.name === "All") {
        this.formInline.reportFrequency = "";
      }
      this.onSubmit(true);
    },
    handleClick2(val) {
      // console.log(val.name,val.label);
      this.formInline.dateData = "";
      if (val.label === "全部") {
        this.formInline.statusReport = "";
        this.formInline.statusDataSend = "";
        this.formInline.statusDataInput = "";
      } else if (val.label === "待传送") {
        this.formInline.statusReport = "";
        this.formInline.statusDataSend = "0";
        this.formInline.statusDataInput = "";
      } else if (val.label === "文本待录入") {
        this.formInline.statusReport = "";
        this.formInline.statusDataSend = "";
        this.formInline.statusDataInput = "0";
      } else {
        this.formInline.statusReport = val.name;
        this.formInline.statusDataSend = "";
        this.formInline.statusDataInput = "";
      }
      this.onSubmit(true);
    },
    // 分页
    Pagination(val) {
      this.formInline.pageSize = val.limit; //页面条数
      this.formInline.pageNum = val.page; //页码
      this.onSubmit(false);
    },
    onSubmit(flag) {
      this.tableLoading = true;
      // 消除没有值的参数
      if (flag) {
        this.formInline.pageNum = 1;
      }
      if (!this.initDate()) {
        this.tableLoading = false;
        return;
      }
      let data = { ...this.formInline };
      // if (data.fundCode) data["fundCode"] = data.fundCode.split("_")[0];
      let params = commonFun.parameterSrc(data);
      pageApi
        .getAnnDataSourceList(params)
        .then((response) => {
          if (response.data.status === 200) {
            this.tableData = response.data.data.list;
            // 页面总条数
            this.total = response.data.data.total;
            this.$nextTick(() => {
              this.$refs.multipleTable.doLayout();
            });
          } else {
            this.tableData = [];
            this.total = 0;
            this.formInline.pageSize = 50;
            this.formInline.pageNum = 1;
          }
          this.tableLoading = false;
        })
        .catch(() => {
          this.tableData = [];
          this.total = 0;
          this.formInline.pageSize = 50;
          this.formInline.pageNum = 1;
          this.tableLoading = false;
        });
    },
    initDate() {
      let flag = this.activeName;
      if (flag === "W") {
        if (this.formInline.dateData) {
          let myDate = new Date(this.formInline.dateData);
          let weekDay = [
            "星期天",
            "星期一",
            "星期二",
            "星期三",
            "星期四",
            "星期五",
            "星期六",
          ];
          let value = weekDay[myDate.getDay()];
          if (value != "星期五") {
            this.$message.closeAll();
            this.$message({
              message: "请选择星期五的日期",
              type: "warning",
            });
            return false;
          }
        }
      } else if (flag === "M") {
        if (this.reportYear && !this.selectDate) {
          this.$message.closeAll();
          this.$message({
            message: "请选择对应的月份",
            type: "warning",
          });
          return false;
        } else if (!this.reportYear && this.selectDate) {
          this.$message.closeAll();
          this.$message({
            message: "请选择对应的年份",
            type: "warning",
          });
          return false;
        } else if (this.reportYear && this.selectDate) {
          this.initMonthDate(this.reportYear, this.selectDate);
        }
      } else if (flag === "Q") {
        if (this.reportYear && !this.selectDate) {
          this.$message.closeAll();
          this.$message({
            message: "请选择对应的季度",
            type: "warning",
          });
          return false;
        } else if (!this.reportYear && this.selectDate) {
          this.$message.closeAll();
          this.$message({
            message: "请选择对应的年份",
            type: "warning",
          });
          return false;
        } else if (this.reportYear && this.selectDate) {
          let q = this.selectDate;
          let date = this.reportYear;
          if (q === "1") {
            date = date + "-03-31";
          } else if (q === "2") {
            date = date + "-06-30";
          } else if (q === "3") {
            date = date + "-09-30";
          } else if (q === "4") {
            date = date + "-12-31";
          }
          this.formInline.dateData = date;
        } else if (!this.reportYear && !this.selectDate) {
          this.formInline.dateData = "";
        }
      } else if (flag === "S") {
        if (this.reportYear) {
          this.formInline.dateData = this.reportYear + "-06-30";
        } else {
          this.formInline.dateData = "";
        }
      } else if (flag === "Y") {
        if (this.reportYear) {
          this.formInline.dateData = this.reportYear + "-12-31";
        } else {
          this.formInline.dateData = "";
        }
      }

      return true;
    },
    getSelects(val) {
      let params = val;
      pageApi
        .getSelects(params)
        .then((res) => {
          let self = this;
          if (res.data.message === "success") {
            if (val === "fundinfo_fundState") {
              // this.proStatusArr = res.data.data;
              let arr = res.data.data;
              for (let i = 0; i < arr.length; i++) {
                // this.fundStatusArr[arr[i].dimCde] = arr[i].dimNme;
                this.$set(this.fundStatusArr,arr[i].dimCde,arr[i].dimNme);
              }
            }
          } else {
            this.$message.closeAll();
            this.$message.error("初始化数据失败");
          }
        })
        .catch(() => {
          this.$message.closeAll();
          this.$message.error("初始化数据失败");
        });
    },
    // 估值基准日选择方式
    reportTypeChange(val) {
      this.reportYear = "";
      this.selectDate = "";
      if (val === "M") {
        this.reportTypeOther_show = true;
        this.reportTypeOther_year = true;
        this.reportTypeOther_day = false;
        this.reportTypeOther_weak = false;

        this.reportTypeArr2 = this.months;
      } else if (val === "Y" || val === "S") {
        this.reportTypeOther_show = false;
        this.reportTypeOther_year = true;
        this.reportTypeOther_day = false;
        this.reportTypeOther_weak = false;
        this.reportTypeArr2 = [];
      } else if (val === "Q") {
        this.reportTypeOther_show = true;
        this.reportTypeOther_year = true;
        this.reportTypeOther_day = false;
        this.reportTypeOther_weak = false;
        this.reportTypeArr2 = this.quarters;
      } else if (val === "D" || val === "All") {
        this.reportTypeOther_show = false;
        this.reportTypeOther_year = false;
        this.reportTypeOther_day = true;
        this.reportTypeOther_weak = false;
      } else if (val === "W") {
        this.reportTypeOther_show = false;
        this.reportTypeOther_year = false;
        this.reportTypeOther_day = true;
        //this.reportTypeOther_day = true;
      }

      if (val === "All" || val === "Q" || val === "S" || val === "Y") {
        this.fundColumnShowFlag = true;
      } else {
        this.fundColumnShowFlag = false;
      }
    },
    ppp(Current) {
      // console.log('ppp',Current);
      if (Current.children) {
        Current = Current.children[0];
        this.ppp(Current);
      }
      return Current;
    },
    // 数据录入处理函数
    handleDataEntry(row) {
      // console.log(row);
      this.node_obj = {};
      this.fileList = [];
      let arr = row.dateData.split("-");
      let Y = arr[0];
      let M = arr[1];
      let date1 = "";
      if (row.reportFrequency == "Q") {
        if (M >= 1 && M <= 3) {
          date1 = "一季度";
        }
        if (M >= 4 && M <= 6) {
          date1 = "二季度";
        }
        if (M >= 7 && M <= 9) {
          date1 = "三季度";
        }
        if (M >= 10 && M <= 12) {
          date1 = "四季度";
        }
      } else if (row.reportFrequency == "S") {
        date1 = "半年度";
      } else if (row.reportFrequency == "Y") {
        date1 = "年度";
      }

      let fundCode = row.fundCode || "";
      let fundName = row.fundName || "";
      let reportType = row.reportType || "";
      this.baobiao_name =
        fundCode + "_" + fundName + Y + reportType + "(" + date1 + ")" + "报告";
      this.rowId = row.id;
      this.treeData = [];
      this.textarea1 = "";
      let params = {
        // id:'31A580BA0B834D9BB755484F6516ADA1'
        id: row.id,
      };
      pageApi.getTreeData(params).then((res) => {
        if (res.data.status == 0) {
          // let data = res.data.data;
          // console.log(res.data.data.length);
          if (res.data.data.length && res.data.data.length != 1) {
            let data = commonFun.converTreeData(
              res.data.data,
              "XBRL",
              "txtPid",
              "txtId"
            ).data;
            let data1 = commonFun.converTreeData(
              res.data.data,
              "XBRL",
              "txtPid",
              "txtId"
            ).expandRowKeys;
            // console.log(data);
            // console.log(data1);
            this.treeData = data[0].children;
            let Current = {};
            let Current1 = {};
            if (data.length) {
              if (data[0].children) {
                Current = data[0].children[0];
                Current1 = this.ppp(Current);
              }
            }
            // console.log('Current1',Current1);
            if (Current1.id) {
              this.defaultexpandedkeys = [...data1, Current1.id];
            }
            // 显示dialog
            this.sjlrDialog = true;
            this.$nextTick(() => {
              // this.$refs.dataTree.setCurrentKey('10001');
              this.$refs.dataTree.setCurrentNode(Current1);
              this.nodeClick(Current1);
            });
          } else if (res.data.data.length == 1) {
            this.$message.error("未配置章节或未配置权限！");
            return;
          } else {
            this.$message.error("未配置章节或未配置权限！");
            return;
          }
        } else {
          this.$message({
            type: "error",
            message: res.data.message || "数据获取失败！",
          });
        }
      });
    },
    // 数据传送
    handleDataSend() {
      if (this.tableMultipleSelection.length === 0) {
        this.$message.closeAll();
        this.$message({
          message: "请选择数据",
          type: "warning",
        });
        return;
      }
      let arr = this.tableMultipleSelection;
      let formData = new FormData(); //  用FormData存放上传文件
      for (let i = 0; i < arr.length; i++) {
        formData.append("ids", arr[i].id);
      }

      //params.models = arr;
      pageApi
        .sjcsData(formData)
        .then((response) => {
          if (response.data.status === 0) {
            this.$message.closeAll();
            this.$message({
              message: "操作成功",
              type: "success",
            });
            // 刷新树列表
            this.onSubmit(false);
          } else {
            this.$message.closeAll();
            this.$message({
              message: response.data.message || "操作失败",
              type: "error",
            });
          }
        })
        .catch(() => {
          // 关闭移动指标弹框
          this.$message.closeAll();
          this.$message({
            message: "操作失败",
            type: "warning",
          });
        });
    },
    // 生成数据
    handleGenera() {
      if (this.tableMultipleSelection.length === 0) {
        this.$message.closeAll();
        this.$message({
          message: "请选择数据",
          type: "warning",
        });
        return;
      }
      let arr = this.tableMultipleSelection;
      let formData = new FormData(); //  用FormData存放上传文件
      for (let i = 0; i < arr.length; i++) {
        formData.append("ids", arr[i].id);
      }

      //params.models = arr;
      this.btn_loading2 = true;
      pageApi
        .yjscData(formData)
        .then((response) => {
          this.btn_loading2 = false;
          if (response.data.status === 200) {
            this.$message.closeAll();
            this.$message({
              message: "操作成功",
              type: "success",
            });
            // 刷新树列表
            this.onSubmit(false);
          } else {
            this.$message.closeAll();
            this.$message({
              message: response.data.message || "操作失败",
              type: "warning",
            });
          }
        })
        .catch(() => {
          this.btn_loading2 = false;
          // 关闭移动指标弹框
          this.$message.closeAll();
          this.$message({
            message: "操作失败",
            type: "warning",
          });
        });
    },
    // 勾稽校验
    handleCheck() {
      if (this.tableMultipleSelection.length === 0) {
        this.$message.closeAll();
        this.$message({
          message: "请选择数据",
          type: "warning",
        });
        return;
      }
      let arr = this.tableMultipleSelection;
      let formData = new FormData(); //  用FormData存放上传文件
      for (let i = 0; i < arr.length; i++) {
        formData.append("ids", arr[i].id);
      }

      //params.models = arr;
      this.btn_loading2 = true;
      pageApi
        .gjjyData(formData)
        .then((response) => {
          this.btn_loading2 = false;
          if (response.data.status === 200) {
            this.$message.closeAll();
            this.$message({
              message: "操作成功",
              type: "success",
            });
            // 刷新树列表
            this.onSubmit(false);
          } else {
            this.$message.closeAll();
            this.$message({
              message: response.data.message || "操作失败",
              type: "warning",
            });
          }
        })
        .catch(() => {
          this.btn_loading2 = false;
          // 关闭移动指标弹框
          this.$message.closeAll();
          this.$message({
            message: "操作失败",
            type: "warning",
          });
        });
    },
    // 复核确认
    handleReviewConfirm() {
      if (this.tableMultipleSelection.length === 0) {
        this.$message.closeAll();
        this.$message({
          message: "请选择数据",
          type: "warning",
        });
        return;
      }
      this.countDialog = true;
      this.formCount.confirmOpinion = "";
    },
    // 与外包核对
    handleCheckOut() {
      if (this.tableMultipleSelection.length === 0) {
        this.$message.closeAll();
        this.$message({
          message: "请选择数据",
          type: "warning",
        });
        return;
      }
      let arr = this.tableMultipleSelection;
      let formData = new FormData(); //  用FormData存放上传文件
      for (let i = 0; i < arr.length; i++) {
        formData.append("ids", arr[i].id);
      }
      //params.models = arr;
      this.btn_loading2 = true;
      pageApi
        .ywbhdData(formData)
        .then((response) => {
          this.btn_loading2 = false;
          if (response.data.status === 200) {
            this.$message.closeAll();
            this.$message({
              message: "操作成功",
              type: "success",
            });
            // 刷新树列表
            this.onSubmit(false);
          } else {
            this.$message.closeAll();
            this.$message({
              message: response.data.message || "操作失败",
              type: "warning",
            });
          }
        })
        .catch(() => {
          this.btn_loading2 = false;
          // 关闭移动指标弹框
          this.$message.closeAll();
          this.$message({
            message: "操作失败",
            type: "warning",
          });
        });
    },
    // 下载报表
    downloadReport() {
      if (this.tableMultipleSelection.length === 0) {
        this.$message.closeAll();
        this.$message({
          message: "请选择数据",
          type: "warning",
        });
        return;
      }
      this.btn_loading2 = true;
      setTimeout(() => {
        this.btn_loading2 = false;
      }, 1000);
      let arr = this.tableMultipleSelection;
      let params = { ids: [], token: this.$store.getters.token }; //  token
      for (let i = 0; i < arr.length; i++) {
        params["ids"].push(arr[i].id);
      }
      let action = store.state.setting.baseApi + "api/annreport/v1.0/download";
      commonFun.formDownloadFile(params, action, "POST");
    },

    //核对明细
    hdmx(row) {
      // console.log(row);
      this.checkDetailPage_show = false;
      this.PageData.recordId = row.id;
      let reportFileType = row.reportFileType;
      if (reportFileType) {
        // if (reportFileType === "EXCEL") {
        //   this.annExcelPage_show = true;
        //   this.annXmlPage_show = false;
        //   this.annTxtPage_show = false;
        //   this.annLogPage_show = false;
        //   this.currencyReportPage_show = false;

        //   this.dialogTitle = "Excel核对页面";
        // } else if (reportFileType === "XML") {
        //   this.annExcelPage_show = false;
        //   this.annXmlPage_show = true;
        //   this.annTxtPage_show = false;
        //   this.annLogPage_show = false;
        //   this.currencyReportPage_show = false;
        //   this.dialogTitle = "XML核对页面";
        // } else if (reportFileType === "TXT") {
        //   this.annExcelPage_show = false;
        //   this.annXmlPage_show = false;
        //   this.annTxtPage_show = true;
        //   this.annLogPage_show = false;
        //   this.currencyReportPage_show = false;
        //   this.dialogTitle = "TXT核对页面";
        // }
        this.PageData1 = {
          recordId: row.id,
        };
        this.czrzDialog = true;
        this.checkDetails_show = true;
        let arr = row.dateData.split("-");
        let Y = arr[0];
        let M = arr[1];
        let date1 = "";
        if (row.reportFrequency == "Q") {
          if (M >= 1 && M <= 3) {
            date1 = "一季度";
          }
          if (M >= 4 && M <= 6) {
            date1 = "二季度";
          }
          if (M >= 7 && M <= 9) {
            date1 = "三季度";
          }
          if (M >= 10 && M <= 12) {
            date1 = "四季度";
          }
        } else if (row.reportFrequency == "S") {
          date1 = "半年度";
        } else if (row.reportFrequency == "Y") {
          date1 = "年度";
        }

        let fundCode = row.fundCode || "";
        let fundName = row.fundName || "";
        let reportType = row.reportType || "";
        this.dialogTitle =
        '【'+reportType+'报告】' + fundCode + "_" + fundName +' '+ Y+'年'+'(' + date1 + ')';
        // this.dialogTitle =
        // fundCode + "_" + fundName + Y + reportType + "(" + date1 + ")" + "报告";
        // this.dialogTitle = row.reportName || "核对页面";
      }
    },
    //操作日志
    czrz(row) {
      this.PageData.recordId = row.id;
      this.czrzDialog = true;
      this.dialogTitle = "操作日志";
      this.checkDetailPage_show = false;
      this.annExcelPage_show = false;
      this.annXmlPage_show = false;
      this.annTxtPage_show = false;
      this.annLogPage_show = true;
      this.currencyReportPage_show = false;
    },
    // 校验明细
    jymx(row) {
      this.PageData.recordId = row.id;
      this.czrzDialog = true;
      this.dialogTitle = "校验明细";
      this.annExcelPage_show = false;
      this.annXmlPage_show = false;
      this.annTxtPage_show = false;
      this.annLogPage_show = false;
      this.currencyReportPage_show = false;
      this.checkDetailPage_show = true;
    },
    // 编辑
    editData(row) {
      if (row.dateData) {
        this.currencyReportPageData.dataDate = row.dateData;
        this.currencyReportPageData.endDate = row.dateData;
      }
      if (row.reportId) {
        this.currencyReportPageData.reportCode = row.reportId;
      }
      if (row.id) {
        this.currencyReportPageData.recordId = row.id;
      }
      if (row.fundType) {
        this.currencyReportPageData.fundType = row.fundType;
        //临时给相关报表使用
        this.currencyReportPageData.typeIn = row.fundType;
      }

      this.annExcelPage_show = false;
      this.annXmlPage_show = false;
      this.annTxtPage_show = false;
      this.annLogPage_show = false;
      this.currencyReportPage_show = true;
      this.czrzDialog = true;
      this.dialogTitle = row.reportName;
    },

    // 取消复核
    reportConfirmCancel(row) {
      this.reportRecordId = row.id;
      this.reportConfirmCancelDialog = true;
      this.formCount.confirmCancelOpinion = "";
    },
    // 复核确认
    countSubmit(formName) {
      var self = this;
      this.$refs[formName].validate((valid) => {
        if (valid) {
          let arr = this.tableMultipleSelection;
          let formData = new FormData(); //  用FormData存放上传文件
          for (let i = 0; i < arr.length; i++) {
            formData.append("ids", arr[i].id);
          }
          formData.append("confirmOpinion", this.formCount.confirmOpinion);
          //params.models = arr;
          this.btn_loading2 = true;
          pageApi
            .qrfhData(formData)
            .then((response) => {
              this.btn_loading2 = false;
              if (response.data.status === 200) {
                this.$message.closeAll();
                this.$message({
                  message: "操作成功",
                  type: "success",
                });
                this.countDialog = false;
                // 刷新树列表
                this.onSubmit(false);
              } else {
                this.$message.closeAll();
                this.$message({
                  message: response.data.message || "操作失败",
                  type: "warning",
                });
              }
            })
            .catch(() => {
              this.btn_loading2 = false;
              // 关闭移动指标弹框
              this.$message.closeAll();
              this.$message({
                message: "操作失败",
                type: "warning",
              });
            });
        } else {
          return false;
        }
      });
    },
    // 取消复核处理函数
    reportConfirmCancelSubmit(formName) {
      var self = this;
      let formData = new FormData();
      this.$refs[formName].validate((valid) => {
        if (valid) {
          formData.append("ids", this.reportRecordId);
          formData.append(
            "confirmOpinion",
            this.formCount.confirmCancelOpinion
          );
          this.btn_loading2 = true;
          pageApi
            .reportConfirmCancelData(formData)
            .then((response) => {
              this.btn_loading2 = false;
              if (response.data.status === 200) {
                this.$message.closeAll();
                this.$message({
                  message: "操作成功",
                  type: "success",
                });
                this.reportConfirmCancelDialog = false;
                // 刷新树列表
                this.onSubmit(false);
              } else {
                this.$message.closeAll();
                this.$message({
                  message: response.data.message || "操作失败",
                  type: "warning",
                });
              }
            })
            .catch(() => {
              this.btn_loading2 = false;
              // 关闭移动指标弹框
              this.$message.closeAll();
              this.$message({
                message: "操作失败",
                type: "warning",
              });
            });
        } else {
          return false;
        }
      });
    },
    // 模板下载
    tempDownload() {
      let params = {};
      if (this.$store.getters.token) {
        params["token"] = this.$store.getters.token;
      }
      params.id = this.rowId;
      let action =
        this.$store.state.setting.baseApi +
        "api/annreportInput/v1.0/downloadTemplate";
      commonFun.formDownloadFile(params, action, "post");
    },
    // 文件上传
    submitUpload() {
      if (!this.fileList.length) {
        this.$message.closeAll();
        this.$message({
          type: "warning",
          message: "请选择文件",
        });
        return false;
      }
      this.fileUpload();
    },
    // 文件导入
    fileUpload() {
      this.uploadLoading = true;
      console.log("fileUpload");
      // let data = this.rowData;
      let file = this.fileList[0].raw;
      let formData = new FormData();
      formData.append("file", file);
      formData.append("id", this.rowId);

      pageApi
        .fileUpload(formData)
        .then((res) => {
          this.fileList = [];
          this.uploadLoading = false;
          if (res.data.status == 0) {
            this.$message({
              type: "success",
              message: "文件导入成功！",
            });
            this.nodeClick(this.node_obj);
          } else {
            this.$message({
              type: "error",
              message: res.data.message || "文件导入失败！",
            });
          }
        })
        .catch(() => {
          this.fileList = [];
          this.uploadLoading = false;
          this.$message({
            type: "error",
            message: res.data.message || "文件导入失败！",
          });
        });
    },
    // 文件个数超过
    onExcedd(files, fileList) {
      if (files) {
        this.$message.closeAll();
        this.$message.warning("只能上传一个文件 ！");
      }
    },
    handleRemove(file, fileList) {
      this.fileList = fileList;
    },
    handleChange(file, fileList) {
      console.log("handleChange");
      this.fileList = [];
      var testmsg = file.name.substring(file.name.lastIndexOf(".") + 1);
      const extension = testmsg === "xls";
      const extension2 = testmsg === "xlsx";
      // if (!extension && !extension2) {
      if (!extension) {
        this.$message({
          // message: "上传文件类型不正确,只允许上传excel文件!",
          message: "只支持文件格式为 .xls 的 excel文件 ！",
          duration: 2000,
          type: "error",
        });
        return false;
      }
      if (file.size > 10 * 1024 * 1024) {
        this.$message({
          message: "请上传小于10M的文件",
          type: "error",
        });
        return false;
      }
      this.fileList = fileList;
      // this.fileUpload();
    },
    httpRequest() {
      // console.log('httpRequest',this.fileList);
      if (this.fileList.length) {
        this.fileUpload();
      } else {
        return false;
      }
    },
    // 文本编辑-vxe列表数据新增
    insertEvent() {
      const record = {};
      this.$nextTick(() => {
        let { row: newRow } = this.$refs.xTable.insertAt(record, -1);
        this.$refs.xTable.setActiveCell(newRow);
      });
    },
    removeEvent() {
      const selectRecords = this.$refs.xTable.getCheckboxRecords();
      if (selectRecords.length) {
        this.$confirm("您确定要删除选中的数据吗?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
          confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
        })
          .then(() => {
            this.$refs.xTable.removeCheckboxRow();
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
    toStringValue(obj) {
        if (obj instanceof Array) {
            var arr = [];
            for (var i = 0; i < obj.length; i++) {
                arr[i] = this.toStringValue(obj[i]);
            }
            return arr;
        } else if (typeof obj == 'object') {
            for (var p in obj) {
                obj[p] = this.toStringValue(obj[p]);
            }
        } else if (typeof obj == 'number') {
            obj = obj + '';
        }
        return obj;
    },
    getJjjlData(data){
      let obj = data;
      this.tableDataDetailArr = [];
      this.VXEtableData = [];
      this.textareaLoading = true;
      let rowId = this.rowId;
      let params = {
        reportCode:data.elementId,
        recordId: rowId
      }
      // this.vxeReportCode = data.elementId;
      // params.reportCode = data.elementId;
      currencyReportApi
        .getTabData2(params)
        .then(res=>{
          if(res.data.status === 200){
            let data = res.data.data;
            this.tabInfo = data;
            if(data[0]){
              
              let arr = data[0].tableList;
              if(arr && arr.length > 0){
                this.vxeTableCode = arr[0].tableCode;
                let tableCode = arr[0].tableCode;
                let fieldsInfo = data[0][arr[0].tableCode];
                let arr1 = fieldsInfo.filter(item=>{
                  return item.isCrud&&item.isCrud.indexOf('R')!=-1
                });
                this.tableDataDetailArr = arr1;
                let params2 = {
                  tableCode,
                  reportCode:obj.elementId,
                  bachId:obj.elementId,
                  recordId: this.rowId
                }
                this.textareaLoading = true;
                currencyReportApi
                  .getDataTableNameList(params2)
                  .then(res=>{
                    this.textareaLoading = false;
                    if(res.data.status === 200 && res.data.data){
                      let data = res.data.data[0].dataList || [];
                      data.forEach(item=>{
                        this.tableDataDetailArr.forEach(i => {
                          item[i.fieldEn] = item[i.fieldEn] || ''
                        });
                      })
                      this.VXEtableData = this.toStringValue(data);
                    }else{
                      this.$message.closeAll();
                      this.$message({
                        type:"error",
                        message:"获取数据失败"
                      })
                    }
                  })
                  .catch(()=>{
                    this.textareaLoading = false;
                  })
              }else{
                this.$message.closeAll();
                this.$message({
                  type:"error",
                  message:"获取表头信息失败"
                })
                this.textareaLoading = false;
              }
            }
          }
        })
        .catch(()=>{
          this.textareaLoading = false;
        })
    },
    // 批量锁定
    batchLock(){
      if (this.tableMultipleSelection.length === 0) {
        this.$message.closeAll();
        this.$message({
          message: "请选择数据",
          type: "warning",
        });
        return;
      }
      let arr = this.tableMultipleSelection;
      let ids = [];
      for (let i = 0; i < arr.length; i++) {
        ids.push(arr[i].id)
      }
      let params = {
        recordId:ids
      }
      this.btn_loading2 = true;
      pageApi.addLockBatch(params).then(res=>{
        this.btn_loading2 = false;
        if(res.data.status === 200){
          this.$message({
            type:"success",
            message:"批量锁定成功"
          })
        }else{
          this.$message({
            type:"error",
            message:res.data.message || "批量锁定失败"
          })
        }
      }).catch((err)=>{
        this.btn_loading2 = false;
      })
    },
    // 批量解锁
    batchUnlock(row){
      if (this.tableMultipleSelection.length === 0) {
        this.$message.closeAll();
        this.$message({
          message: "请选择数据",
          type: "warning",
        });
        return;
      }
      let arr = this.tableMultipleSelection;
      let ids = [];
      for (let i = 0; i < arr.length; i++) {
        ids.push(arr[i].id)
      }
      let params = {
        recordId:ids
      }
      this.btn_loading2 = true;
      pageApi.unlockBatch(params).then(res=>{
        this.btn_loading2 = false;
        if(res.data.status === 200){
          this.$message({
            type:"success",
            message:"批量解锁成功"
          })
        }else{
          this.$message({
            type:"error",
            message:res.data.message || "批量解锁失败"
          })
        }
      }).catch((err)=>{
        this.btn_loading2 = false;
      })
    }
  },
};
</script>

<style  lang="scss">
.per-report-record {
  //   .el-input__inner {
  //     width: 160px;
  //   }
  .currency_report_old_form {
    .el-form-item {
      margin-bottom: 10px !important;
      .el-form-item__content {
        .el-input {
          width: 160px !important;
        }
        .el-date-editor {
          width: 160px !important;
        }
        .el-select {
          width: 160px !important;
        }
      }
    }
  }
  .right-textarea {
    padding: 20px;
    // margin-left: 20px;
    box-sizing: border-box;
    height: calc(100% - 66px);
  }
  .right-textarea.textarea1 {
    .el-textarea {
      height: 100%;
      .el-textarea__inner {
        height: 100% !important;
      }
    }
  }
  .right-textarea.vxetextarea {
    .vxeTable {
      .vxe-cell {
        .el-textarea__inner {
          padding: 5px !important;
        }
      }
    }
  }
  .baobiao_name {
    text-align: center;
    // color: red;
    // font-size: 16px;
    font-weight: bold;
    margin-bottom: 10px;
  }
  .el-dialog.is-fullscreen {
    width: 100% !important;
  }
  .wblr_dialog {
    .file_upload {
      display: inline;
      margin-left: 10px;
    }
  }
  .checkDetails_dialog {
    .el-dialog__body {
      height: calc(100vh - 66px);
      .el-container {
        height: 100%;
        .el-main {
          height: 100%;
        }
      }
    }
  }
}
.xbrlCzrzListWidth_ {
  // width: 75% !important;
  // margin-top: 5vh !important;
  /* max-height: 90%;
  overflow: hidden;
  overflow-y: auto; */
}
.qrfuListWidth {
  width: 70% !important;
}
.el-dialog .el-form {
  width: 100% !important;
}
.per-report-record {
  .custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
    width: 100%;
    span {
      display: inline-block;
      width: 100%;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
  }
  .dataTrees {
    // .el-tree-node__content>.el-tree-node__expand-icon{
    //   padding-left: 0 !important;
    // }
    .el-tree-node__expand-icon.is-leaf {
      display: block !important;
    }
  }
  // 产品多选
  .multipleSelectTable{
    .vxe-pulldown{
      width: 160px !important;
    }
  }
}
</style>

<style scoped lang="scss">
.per-report-record {
  height: 100%;
}
</style>
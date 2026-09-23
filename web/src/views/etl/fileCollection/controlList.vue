<template>
  <div class="controlList">
    <div class="forms_table_title"><i class="el-icon-tickets"></i>调度列表</div>

    <!-- <el-button
      style="margin-bottom:10px;float:right"
      type="primary"
      :disabled="btnDisabled"
      class="mb5"
      size="small"
      @click="onQuery(true)"
    >查询</el-button> -->

    <el-table
      ref="multipleTable"
      :data="tableData"
      :default-sort="{ prop: 'startTim', order: 'descending' }"
      border
      stripe
      v-loading="tableLoading"
      style="width: 100%"
      max-height="440px"
    >
      <el-table-column
        type="index"
        label="序号"
        fixed
        align="center"
        width="40"
      ></el-table-column>

      <!-- <el-table-column
        prop="jobCde"
        show-overflow-tooltip
        label="调度唯一标识"
        min-width="200"
        header-align="center"
      ></el-table-column> -->
      <el-table-column
        prop="schCde"
        show-overflow-tooltip
        label="调度编码"
        min-width="100"
        header-align="center"
      ></el-table-column>
      <el-table-column
        prop="schNme"
        show-overflow-tooltip
        label="调度名称"
        min-width="100"
        header-align="center"
      ></el-table-column>
      <el-table-column
        prop="startTim"
        show-overflow-tooltip
        label="调度开始时间"
        min-width="100"
        header-align="center"
      ></el-table-column>
      <el-table-column
        prop="previousTim"
        show-overflow-tooltip
        label="上次完成时间"
        min-width="100"
        header-align="center"
      ></el-table-column>
      <el-table-column
        prop="nextTim"
        show-overflow-tooltip
        label="下次执行时间"
        min-width="100"
        header-align="center"
      ></el-table-column>

      <el-table-column label="操作" fixed="right" width="220" align="center">
        <template slot-scope="scope">
          <!-- <el-button
            type="danger"
            plain
            size="small"
            @click="delData(scope.row)"
            >取消调度</el-button
          > -->
          <el-button type="primary" size="small" @click="handleData(scope.row)"
            >手工执行</el-button
          >
          <el-button type="primary" size="small" @click="checkData(scope.row)"
            >查看调度设置</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <!-- <Pagination
      :total="total"
      :limit="formQuery.pageSize"
      :page="formQuery.pageNum"
      @pagination="pagination"
    ></Pagination>-->

    <!-- 调度设置 参数弹窗3 -->
    <el-dialog
      title="调度设置"
      center
      append-to-body
      :visible.sync="dialogMask3"
      :close-on-click-modal="false"
      width="60% !important"
    >
      <el-container class="hg100">
        <el-main class="mainBox">
          <el-form
            :inline="true"
            ref="formDialog3"
            :model="formDialog3"
            label-position="right"
          >
            <el-form-item prop="startWhen">
              <div class="titlewords">开始日期:</div>
              <el-radio v-model="formDialog3.startWhen" label="now" disabled
                >立即开始</el-radio
              >
              <br />
              <el-radio
                v-model="formDialog3.startWhen"
                label="dateTime"
                disabled
              >
                <el-form-item
                  label="开始日期"
                  prop="startDate"
                  label-width="60px"
                  class="mb20 startdate"
                >
                  <el-date-picker
                    v-model="formDialog3.startDate"
                    type="date"
                    size="small"
                    disabled
                    value-format="yyyy-MM-dd"
                    placeholder="选择日期"
                  ></el-date-picker>
                </el-form-item>
                <el-form-item
                  label="开始时间"
                  prop="startTime"
                  label-width="100px"
                  class="mb20 startdate"
                >
                  <el-time-picker
                    size="small"
                    disabled
                    v-model="formDialog3.startTime"
                    :picker-options="{ selectableRange: '00:00:00 - 23:59:59' }"
                    placeholder="选择时间"
                    value-format="HH:mm:ss"
                  ></el-time-picker>
                </el-form-item>
              </el-radio>
            </el-form-item>

            <!-- 分割线 -->
            <div style="width: 100%; border-top: 1px solid red"></div>

            <el-form-item prop="recurPrimary">
              <div class="titlewords">循环:</div>
              <el-radio-group
                v-model="formDialog3.recurPrimary"
                @change="recurdeal"
                disabled
              >
                <el-radio label="once">一次</el-radio>
                <el-radio label="dailyday">每日</el-radio>
                <el-radio label="weekly">每周</el-radio>
                <el-radio label="monthly">每月</el-radio>
                <el-radio label="timepiece">间隔时间</el-radio>
              </el-radio-group>
              <div v-if="recurtype == 1">
                运行一次 (如果反复运行, 则在同一天运行)
              </div>
              <div v-else-if="recurtype == 2" class="recur">
                <span>每隔</span> &nbsp;
                <el-input
                  v-model.trim="formDialog3.dailyN"
                  clearable
                  size="mini"
                  maxlength="3"
                  disabled
                ></el-input
                >&nbsp;
                <span>天</span>
              </div>
              <div v-else-if="recurtype == 3" class="recur">
                <span>每隔</span> &nbsp;
                <el-input
                  v-model.trim="formDialog3.weeklyN"
                  clearable
                  size="mini"
                  maxlength="3"
                  disabled
                ></el-input
                >&nbsp;
                <span>周:</span>
                <br />
                <el-checkbox-group v-model="formDialog3.week" disabled>
                  <el-checkbox label="sun">星期日</el-checkbox>
                  <el-checkbox label="mon">星期一</el-checkbox>
                  <el-checkbox label="tue">星期二</el-checkbox>
                  <el-checkbox label="wed">星期三</el-checkbox>
                  <el-checkbox label="thu">星期四</el-checkbox>
                  <el-checkbox label="fri">星期五</el-checkbox>
                  <el-checkbox label="sat">星期六</el-checkbox>
                </el-checkbox-group>
              </div>
              <div v-else-if="recurtype == 4" class="recur">
                <span>在</span> &nbsp;
                <el-input
                  v-model.trim="formDialog3.monthlyDay"
                  clearable
                  size="mini"
                  disabled
                  maxlength="3"
                ></el-input
                >&nbsp;
                <span>日:</span>
                <br />
                <span>在</span> &nbsp;
                <el-select
                  v-model="formDialog3.monthlyNth"
                  placeholder="请选择"
                  size="small"
                  disabled
                >
                  <el-option label="第一个" value="1"></el-option>
                  <el-option label="第二个" value="2"></el-option>
                  <el-option label="第三个" value="3"></el-option>
                  <el-option label="第四个" value="4"></el-option>
                  <el-option label="最后一个" value="5"></el-option> </el-select
                >&nbsp;
                <el-select
                  v-model="formDialog3.monthlyDOW"
                  placeholder="请选择"
                  size="small"
                  disabled
                >
                  <el-option label="星期日" value="1"></el-option>
                  <el-option label="星期一" value="2"></el-option>
                  <el-option label="星期二" value="3"></el-option>
                  <el-option label="星期三" value="4"></el-option>
                  <el-option label="星期四" value="5"></el-option>
                  <el-option label="星期五" value="6"></el-option>
                  <el-option label="星期六" value="7"></el-option>
                </el-select>
                <br />
                <el-checkbox-group v-model="formDialog3.month" disabled>
                  <el-checkbox label="jan">一月</el-checkbox>
                  <el-checkbox label="feb">二月</el-checkbox>
                  <el-checkbox label="mar">三月</el-checkbox>
                  <el-checkbox label="apr">四月</el-checkbox>
                  <el-checkbox label="may">五月</el-checkbox>
                  <el-checkbox label="jun">六月</el-checkbox>
                  <el-checkbox label="jul">七月</el-checkbox>
                  <el-checkbox label="aug">八月</el-checkbox>
                  <el-checkbox label="sep">九月</el-checkbox>
                  <el-checkbox label="oct">十月</el-checkbox>
                  <el-checkbox label="nov">十一月</el-checkbox>
                  <el-checkbox label="dec">十二月</el-checkbox>
                </el-checkbox-group>
              </div>
              <div v-else-if="recurtype == 5" class="recur">
                <span>每隔:</span> &nbsp;
                <el-radio-group v-model="formDialog3.timePiece" disabled>
                  <el-radio label="hour">
                    <el-input
                      v-model.trim="formDialog3.hours"
                      disabled
                      size="mini"
                      maxlength="3"
                    ></el-input
                    >&nbsp;
                    <span>小时</span>
                  </el-radio>
                  <el-radio label="minute">
                    <el-input
                      v-model.trim="formDialog3.minutes"
                      disabled
                      size="mini"
                      maxlength="3"
                    ></el-input
                    >&nbsp;
                    <span>分钟</span>
                  </el-radio>
                  <el-radio label="second">
                    <el-input
                      v-model.trim="formDialog3.seconds"
                      disabled
                      size="mini"
                      maxlength="3"
                    ></el-input
                    >&nbsp;
                    <span>秒</span>
                  </el-radio>
                </el-radio-group>
                <br />
                <span>运行时间段:</span>&nbsp;
                <el-time-picker
                  size="small"
                  is-range
                  v-model="runTimeInterval"
                  value-format="HH:mm:ss"
                  range-separator="至"
                  start-placeholder="开始时间"
                  end-placeholder="结束时间"
                  placeholder="选择时间范围"
                  disabled
                ></el-time-picker>
              </div>
            </el-form-item>

            <!-- 分割线 -->
            <div style="width: 100%; border-top: 1px solid red"></div>

            <el-form-item prop="misIndexSwitch">
              <div class="titlewords">日期偏移设置：</div>
              <div class="recur">
                <!-- <el-radio-group v-model="formDialog3.misIndexSwitch"> -->
                <el-radio
                  v-model="formDialog3.misIndexSwitch"
                  label="none"
                  disabled
                  >无</el-radio
                >
                <br />
                <el-radio v-model="formDialog3.misIndexSwitch" label="by">
                  <span>日期类型 ：</span>
                  <el-select
                    v-model="formDialog3.natureDay"
                    placeholder="请选择"
                    size="small"
                    disabled
                  >
                    <el-option label="自然日" value="0"></el-option>
                    <el-option label="交易日" value="1"></el-option> </el-select
                  >&nbsp;
                  <span>日期偏移量：</span>
                  <el-input
                    v-model.trim="formDialog3.misIndex"
                    clearable
                    size="mini"
                    disabled
                  ></el-input>
                </el-radio>
                <!-- </el-radio-group> -->
              </div>
            </el-form-item>
            <!-- 分割线 -->
            <div style="width: 100%; border-top: 1px solid red"></div>

            <el-form-item prop="endBy">
              <div class="titlewords">结束日期：</div>
              <div>
                <!-- <el-radio-group v-model="formDialog3.endBy"> -->
                <el-radio v-model="formDialog3.endBy" label="none" disabled
                  >无</el-radio
                >
                <br />
                <el-radio v-model="formDialog3.endBy" label="by">
                  <el-form-item
                    label="结束日期"
                    prop="startDate"
                    label-width="60px"
                    class="mb20"
                  >
                    <el-date-picker
                      v-model="formDialog3.endDate"
                      type="date"
                      disabled
                      size="small"
                      value-format="yyyy-MM-dd"
                      placeholder="选择日期"
                    ></el-date-picker>
                  </el-form-item>
                </el-radio>
                <!-- </el-radio-group> -->
              </div>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
    </el-dialog>

    <!-- 手工执行 弹窗2 -->
    <el-dialog
      :title="handleWord"
      center
      append-to-body
      :visible.sync="dialogMask2"
      :close-on-click-modal="false"
      width="60% !important"
    >
      <el-container class="hg100">
        <el-main class="mainBox">
          <el-form
            :inline="true"
            ref="formDialog2"
            :model="formDialog2"
            :rules="dialogRules2"
            label-position="right"
            style="width: 94% !important; margin: 0 auto"
          >
            <el-form-item
              label="日期"
              prop="date"
              :label-width="formLabelWidth"
              class="mb20"
            >
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
            <el-form-item
              label="产品代码"
              prop="fundCodes"
              class="mb20 formInput-adaptive-100"
              :label-width="formLabelWidth"
            >
              <multipleSelectTable
                v-model="formDialog2.fundCodes1"
                :data="fundList"
                :Columns="Columns"
                @checkboxAll="checkboxAll"
                @checkboxChange="checkboxChange"
                idField="fundCode"
                nameField="fundName"
                placeholder="请选择"
              ></multipleSelectTable>
              <!-- <el-input
                v-model.trim="formDialog2.fundCodes"
                clearable
                placeholder="请输入产品代码"
                type="textarea"
              ></el-input> -->
            </el-form-item>
            <el-form-item
              label="自定义参数（json格式）"
              prop="custom"
              class="mb20 ddCode-mirror-form ddCode-mirror-form-200"
              :label-width="'175px'"
            >
              <!-- js语言需要传入一个特殊的值，来区别是js还是json -->
              <dd-code-mirror
                ref="customCodeMirror"
                language="javascript"
                scriptLanguage="json"
                @codeChange="customChange"
              ></dd-code-mirror>
            </el-form-item>

            
          </el-form>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="dialogMask2 = false">取 消</el-button>
        <el-button type="primary" size="small" @click="handledealData"
          >确 定</el-button
        >
      </div>
    </el-dialog>
  </div>
</template>

<script>
import pageApi from "@/api/etl/controlList.js";
import Pagination from "@/components/Pagination";
import multipleSelectTable from "@/views/commonComponents/multiple-select-table2";
export default {
  name: "DdControlList",
  components: { 
    Pagination,
    multipleSelectTable
  },
  data() {
    return {
      tableData: [], //表格数据
      tableLoading: false, //表格加载
      dialogMask: false, // 弹窗

      dialogMask3: false, // 弹窗 3
      // 任务类型集合
      jobTypeArr: [],
      // //总条数
      total: 0,
      // 顶部查询条件
      formQuery: {
        // 排序字段
        orderBy: "jobCde  desc",
        // 起始页
        pageNum: 1,
        // 每页大小
        pageSize: 10,
      },
      // 弹窗查询参数
      formDialog: {
        //  任务编码
        misCde: "",
        // 任务名称
        misNme: "",
        // 任务描述
        misCmt: "",
        // 目标源
        aimDbsCde: "",
        // 任务类型
        misTyp: "",
        // 源数据源
        srcDbsCde: "",
        // 日期类型
        natureDay: "0",
        // 日期偏移量
        misIndex: "",
        // 是否启用
        misRun: "1",
        // 循环标志
        misEachDayFlag: "0",
        // 文件路径
        filUrl: "",
        // 前置条件
        prevSqlSet: "",
        // 参数设置
        parSet: "",
        // 清除设置
        clsSet: "",
        // 映射规则
        datSrcSet: "",
        // 目标SQL
        aimSqlSet: "",
      },
      // 弹窗3查询参数
      formDialog3: {
        // 编码
        schCde: "",
        // 名称
        schNme: "",
        // 开始类型
        startWhen: "now",
        // 开始日期
        startDate: "",
        // 开始时间
        startTime: "",
        // 循环
        recur: "once",
        // 每隔几天运行一次
        recurPrimary: "once",
        // 间隔天数
        dailyN: "",
        // 每隔几周
        weeklyN: "",
        // week 多选框
        week: [],
        // 第几周标志
        recurMonthly: "recurMonthly",
        // 每月第几天
        monthlyDay: "",
        // 第几周
        monthlyNth: "1",
        // 星期几
        monthlyDOW: "1",
        // 几月份 多选框
        month: [],
        timePiece: "",
        // 小时
        hours: "01",
        // 分钟
        minutes: "01",
        // 秒数
        seconds: "01",
        // 日期偏移选择
        misIndexSwitch: "none", //none 是无 ，by是有
        // 日期偏移量类型
        natureDay: "0", //0是自然日，1是交易日
        // 日期偏移量
        misIndex: "",
        // 结束日期 无
        endBy: "none",
        // 结束日期
        endDate: "",
      },
      recurtype: 1,

      // 操作类型 1、添加 2、编辑
      operationType: 1,
      formLabelWidth: "100px",

      // 查询按钮禁用
      btnDisabled: false,
      // 数据源数据集合
      SourceList: [],

      // 手工执行-------
      // 手工执行任务编码
      handlemisCde: "",
      handleWord: "",
      handlefundCodes: "",
      setfundCodes: "",
      dialogMask2: false,
      formDialog2: {
        // 日期
        date: [],
        // 基金编码
        fundCodes: "",
        fundCodes1:[],
        // 调度设置编码
        schCde: "",
        // 自定义参数
        custom: "",
      },
      dialogRules2: {
        // 日期
        date: [{ required: true, message: "请填写日期", trigger: "change" }],
      },
      fundList:[],
      Columns: [
        { label: "产品代码", prop: "fundCode" },
        { label: "产品名称", prop: "fundName" },
        { label: "托管人名称", prop: "nameTgr" },
      ],
      runTimeInterval: [],
    };
  },
  watch: {},
  mounted() {
    this.onQuery(true);
    this.getFundList();
  },
  methods: {
    // 日期快捷选项
    dateShortcut() {
      return this.$fun.dateShortcut();
    },
    // 查询
    onQuery(flag) {
      this.tableLoading = true; //表格加载
      this.btnDisabled = true;
      // if (flag) {
      //   this.formQuery.pageNum = 1;
      // }
      // let params = Object.assign({}, this.formQuery);
      // console.log(params);
      pageApi
        .dispatchLists({})
        .then((res) => {
          if(res.data.status===0){
            this.tableData = res.data.data;
          }else{
            this.$message({
              type:"error",
              message:res.data.message || "获取调度列表失败！"
            })
            this.tableData = [];
          }
          this.tableLoading = false; //表格加载
          this.btnDisabled = false;
        })
        .catch(() => {
          this.tableLoading = false;
          this.btnDisabled = false;
        });
    },

    // 行删除
    delData(row) {
      this.$confirm("确认取消调度吗?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          // 删除单个
          this.deleteParamSet(row.jobCde, row.schCde);
        })
        .catch(() => {});
    },
    // 取消调度
    deleteParamSet(jobCde, schCde) {
      this.tableLoading = true;
      let params = {
        jobName: jobCde,
        jobGroup: schCde,
        triggerName: jobCde,
        triggerGroup: schCde,
      };
      pageApi
        .cancelDispatch(params)
        .then((res) => {
          this.tableLoading = false;

          this.onQuery(false);
          this.$message.closeAll();

          this.$message({
            type: "success",
            message: "取消成功",
          });
        })
        .catch(() => {});
    },

    // 查看数据设置
    checkData(row) {
      this.dialogMask3 = true;
      let params = {
        triggerGroup: row.jobGroup,
        triggerName: row.jobCde,
      };

      pageApi
        .selectDispatchSet(params)
        .then((res) => {
          let { scher } = res.data.data;

          this.$nextTick(() => {
            // 清除
            this.$refs["formDialog3"].resetFields();

            this.formDialog3.startWhen = scher.startWhen;
            this.formDialog3.startDate = scher.startDate;
            this.formDialog3.startTime = scher.startTime;
            this.formDialog3.recurPrimary = scher.recurPrimary;
            this.formDialog3.dailyN = scher.dailyN;
            this.formDialog3.weeklyN = scher.weeklyN;
            this.formDialog3.recurMonthly = scher.recurMonthly;
            this.formDialog3.monthlyDay = scher.monthlyDay;
            this.formDialog3.monthlyNth = scher.monthlyNth;
            this.formDialog3.monthlyDOW = scher.monthlyDOW;
            this.formDialog3.timePiece = scher.timePiece;
            this.formDialog3.hours = scher.hours;
            this.formDialog3.minutes = scher.minutes;
            this.formDialog3.seconds = scher.seconds;
            this.formDialog3.misIndexSwitch = scher.misIndexSwitch;
            this.formDialog3.natureDay = scher.natureDay;
            this.formDialog3.misIndex = scher.misIndex;
            this.formDialog3.endBy = scher.endBy;
            this.formDialog3.endDate = scher.endDate;

            if (scher.recurPrimary === "once") {
              this.recurtype = 1;
            } else if (scher.recurPrimary === "dailyday") {
              this.recurtype = 2;
            } else if (scher.recurPrimaryv === "weekly") {
              this.recurtype = 3;
            } else if (scher.recurPrimary === "monthly") {
              this.recurtype = 4;
            } else if (scher.recurPrimary === "timepiece") {
              this.recurtype = 5;
            }

            this.runTimeInterval = [];

            if (scher.runStartTime) {
              this.runTimeInterval.push(scher.runStartTime);
              this.runTimeInterval.push(scher.runEndTime);
            } else {
              this.runTimeInterval = [];
            }
          });
        })

        .catch(() => {});
    },
    // 调度设置-循环 的处理
    recurdeal(val) {
      if (val === "once") {
        this.recurtype = 1;
      } else if (val === "dailyday") {
        this.recurtype = 2;
      } else if (val === "weekly") {
        this.recurtype = 3;
      } else if (val === "monthly") {
        this.recurtype = 4;
      } else if (val === "timepiece") {
        this.recurtype = 5;
      }
    },
    //  分页
    pagination(val) {
      let { page, limit } = val;
      // 起始页
      this.formQuery.pageNum = page;
      // 每页数量
      this.formQuery.pageSize = limit;
      // 查询
      this.onQuery(false);
    },

    // 手工执行
    handleData(row) {
      this.handleWord = row.schNme + "(" + row.schCde + ")";
      this.handlemisCde = row.schCde;
      this.dialogMask2 = true;
      this.$nextTick(() => {
        this.$refs["formDialog2"].resetFields();

        // 清除
        this.formDialog2.fundCodes = "";
        this.handlefundCodes = "";
        this.setfundCodes = "";
        // 清空自定义参数的值
        this.$refs.customCodeMirror.operationVal(null);
        this.formDialog2.fundCodes1 = [];
      });
    },
    // 自定义参数赋值给页面变量
    customChange(val) {
      this.formDialog2.custom = val;
    },
    // 校验一个字符串是否是json 类型
    isJSON(str) {
      if (typeof str == "string") {
        try {
          let obj = JSON.parse(str);
          if (typeof obj == "object" && obj) {
            return true;
          } else {
            return false;
          }
        } catch (e) {
          console.log(e);
          return false;
        }
      } else {
        return "It is not a string!";
      }
    },
    handledealData() {
      this.$refs["formDialog2"].validate(valid => {
        if (valid) {
            // 判自定义参数是否是json格式的
          if(this.formDialog2.custom){
             if(this.isJSON(this.formDialog2.custom) === false){
                 this.$message.closeAll();
                 this.$message({
                   type: "warning",
                   message: "自定义参数必须是json格式！"
                  });
                  return false
             }
          }
          let params = Object.assign({}, this.formDialog2);
          params.beginDate = params.date[0];
          params.endDate = params.date[1];
          delete params.date;
          params.schCde = this.handlemisCde;
          params.fundCodes = params.fundCodes1.join(',');
          delete params.fundCodes1;
          // console.log(params);
          // 手工执行
          pageApi
            .implementScher(params)
            .then(res => {
              this.$message.closeAll();
              if (res.data.status == 200) {
                this.$message({
                  type: "success",
                  message: res.data.message
                });
                this.dialogMask2 = false;
              } else {
                this.$message({
                  type: "error",
                  message: res.data.message
                });
              }
            })
            .catch(() => {});
        }
      });
    },
    getFundList(){
      pageApi.getFundList({}).then(res=>{
        if(res.data.status===0){
          this.fundList = res.data.data.list;
        }else{
          this.$message({
            type:"error",
            message:res.data.message || '获取产品信息失败'
          })
          this.fundList = [];
        }
      })
    },
    checkboxAll(data){
      // console.log(data);
      let { checked, records } = data;
    },
    checkboxChange(data){
      // console.log(data);
      let { checked, records } = data;

    }
  },
};
</script>

<style lang="scss" scope>
.controlList {
  height: 500px;
  .el-dialog {
    width: 54% !important;
    .el-form {
      width: 100% !important;
      font-size: 0;
    }
    .el-input {
      width: 120% !important;
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
    margin-bottom: 15px;
  }
  .recur {
    .el-input {
      width: 85px !important;
    }
  }
  // 火狐移除
  input[type="number"] {
    -moz-appearance: textfield;
  }

  //谷歌下的移除
  input[type="number"]::-webkit-inner-spin-button,
  input[type="number"]::-webkit-outer-spin-button {
    -webkit-appearance: none;
  }
}
</style>

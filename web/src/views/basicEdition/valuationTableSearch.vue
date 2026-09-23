<template>
  <!-- 估值表数据 -->
  <div class="valuationTableSearch">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formQuery" :inline="true" :model="formQuery" :rules="searchRules" class="standard-form">
          <el-row>
            <el-col :span="24">
              <!-- <el-form-item prop="endDate">
              <span class="item-label" slot="label">估值日期</span>
              <el-date-picker
                v-model="formQuery.endDate"
                clearable
                value-format="yyyy-MM-dd"
                size="small"
              >
              </el-date-picker>
            </el-form-item> -->
              <!-- <el-form-item prop="beginDate" label="开始日期">
              <el-date-picker
                v-model="formQuery.beginDate"
                value-format="yyyy-MM-dd"
                size="small"
              />
            </el-form-item>
            <el-form-item prop="endDate" label="结束日期">
              <el-date-picker
                v-model="formQuery.endDate"
                value-format="yyyy-MM-dd"
                size="small"
              />
            </el-form-item> -->
              <el-form-item prop="fundNames">
                <span slot="label" class="item-label">产品</span>
                <el-tooltip :content="formQuery.fundNames" :disabled="!formQuery.fundNames" class="item" effect="dark" placement="top-start">
                  <el-input v-model.trim="formQuery.fundNames" clearable placeholder="请输入" size="small" @change="handleFundNamesChange" @click.native="openFundListDialog" />
                </el-tooltip>
              </el-form-item>
              <el-form-item class="mb20" label="日期" prop="ddate_">
                <el-date-picker
                  v-model="formQuery.ddate_"
                  :picker-options="dateShortTPCTA()"
                  align="left"
                  end-placeholder="结束日期"
                  popper-class="popperDateShortTP"
                  range-separator="至"
                  size="small"
                  start-placeholder="开始日期"
                  type="daterange"
                  unlink-panels
                  value-format="yyyy-MM-dd"
                ></el-date-picker>
              </el-form-item>

              <!--            <el-form-item prop="fundName">-->
              <!--              <span slot="label" class="item-label">产品名称</span>-->
              <!--              <el-tooltip-->
              <!--                :content="formQuery.fundName"-->
              <!--                :disabled="!formQuery.fundName"-->
              <!--                class="item"-->
              <!--                effect="dark"-->
              <!--                placement="top-start"-->
              <!--              >-->
              <!--                <el-input v-model="formQuery.fundName" class="inline-input" clearable placeholder="请输入内容"></el-input>-->
              <!--              </el-tooltip>-->
              <!--            </el-form-item>-->
              <el-form-item prop="symBolCode">
                <span slot="label" class="item-label">科目代码</span>
                <el-input v-model.trim="formQuery.symBolCode" clearable placeholder="请输入" size="small"></el-input>
              </el-form-item>
              <el-form-item prop="kmmc">
                <span slot="label" class="item-label">科目名称</span>
                <el-input v-model.trim="formQuery.kmmc" clearable placeholder="请输入" size="small"></el-input>
              </el-form-item>
              <el-form-item class="">
                <el-button icon="el-icon-search" size="small" style="margin-bottom: 5px" type="primary" @click="onSubmit('formQuery')">查询</el-button>
                <el-button type="info" icon="el-icon-refresh" plain size="small" @click="resetForm('formQuery')">重置</el-button>
                <el-button :disabled="isDisabled" :icon="exportLoading ? 'el-icon-loading' : 'el-icon-download'" type="info" size="small" plain @click="downloadTableExcel">
                  {{ downLoadText }}
                </el-button>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>
    </div>

    <el-row>
      <el-col :span="24">
        <div style="float: right">
          <vxe-toolbar ref="tableToolbar" class="standard-vxe-toolbar" custom></vxe-toolbar>
        </div>
      </el-col>
    </el-row>
    <el-row id="standard-table">
      <div id="standard-table-margin">
        <el-col>
          <vxe-table
            id="toolbar_table1"
            ref="table1"
            :custom-config="{ storage: true }"
            :data="tableData"
            :cell-style="{ height: '50px' }"
            :loading="tableLoading"
            :sort-config="{ remote: true }"
            show-header-overflow
            auto-resize
            show-overflow
            stripe
            @sort-change="handleSortChange"
            resizable
          >
            <vxe-table-column align="left" field="fundCode" fixed="left" header-align="center" min-width="200" title="产品代码">
              <template slot-scope="scope">
                <span>{{ scope.row.fundCode | noDataFilter }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column align="left" field="fundName" fixed="left" header-align="center" min-width="200" title="产品名称">
              <template slot-scope="scope">
                <span>{{ scope.row.fundName | noDataFilter }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column align="left" field="fDate" fixed="left" header-align="center" min-width="200" title="估值日期" sortable></vxe-table-column>
            <vxe-table-column align="left" field="kmbm" fixed="left" header-align="center" min-width="200" sortable title="科目代码"></vxe-table-column>
            <vxe-table-column align="left" field="kmmc" fixed="left" header-align="center" min-width="200" sortable title="科目名称"></vxe-table-column>
            <vxe-table-column align="right" field="counts" header-align="center" min-width="100" sortable title="持仓数量"></vxe-table-column>
            <vxe-table-column :min-width="minTableWidth" align="right" field="dwcb" header-align="center" title="单位成本">
              <template slot-scope="scope">
                <span>{{ scope.row.dwcb | moneyYuan }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column :min-width="minTableWidth" align="right" field="cbPrice" header-align="center" sortable title="成本">
              <template slot-scope="scope">
                <span>{{ scope.row.cbPrice | moneyYuan }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column :min-width="minTableWidth" align="right" field="cbRate" header-align="center" sortable title="成本占比(%)"></vxe-table-column>
            <vxe-table-column :min-width="minTableWidth" align="right" field="hqPrice" header-align="center" sortable title="行情价格">
              <template slot-scope="scope">
                <span>{{ scope.row.hqPrice | moneyYuan }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column :min-width="minTableWidth" align="right" field="sjPrice" header-align="center" sortable title="市值">
              <template slot-scope="scope">
                <span>{{ scope.row.sjPrice | moneyYuanFour }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column :min-width="minTableWidth" :visible="false" align="right" field="sjRate" header-align="center" sortable title="市值占比"></vxe-table-column>
            <vxe-table-column align="left" field="bz" header-align="center" min-width="200" sortable title="币种"></vxe-table-column>
            <vxe-table-column :min-width="minTableWidth" align="right" field="hl" header-align="center" sortable title="汇率"></vxe-table-column>
            <vxe-table-column :min-width="minTableWidth" align="right" field="gzzz" header-align="center" sortable title="估值增值">
              <template slot-scope="scope">
                <span>{{ scope.row.gzzz | moneyYuan }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column :min-width="minTableWidth" align="left" field="qyxx" header-align="center" title="权益信息"></vxe-table-column>
            <vxe-table-column :min-width="minTableWidth" :visible="false" align="left" field="tpxx" header-align="center" title="停牌信息"></vxe-table-column>
          </vxe-table>
          <vxe-pager
            :current-page="formQuery.pageNum"
            :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
            :page-size="formQuery.pageSize"
            :total="total"
            class="standard-vxe-pager"
            border
            size="medium"
            @page-change="pagination"
          ></vxe-pager>
        </el-col>
      </div>
    </el-row>
    <!--    <el-dialog
      v-if="dialogMask"
      :close-on-click-modal="false"
      :visible.sync="dialogMask"
      center
      custom-class="customWidth"
      title="产品信息"
    >
      <el-container class="hg100">
        <el-main class="mainBox">
          <FundListDialogMultiphase
            :tagsinfo="tags"
            @getTemplateRow="getTemplateRow"
          />
        </el-main>
      </el-container>
    </el-dialog>-->

    <product-selector
      :multiple="true"
      :leftList="false"
      :dialog-visible="dialogMask"
      :tree-data="treeData"
      :show-tree-key-array="showTreeKeyArray"
      :select-list="selectList"
      default-checked-keys="zstgwb"
      @closedialog="handleDialogClosed"
      @submitdialog="handleSubmitClick"
    ></product-selector>
  </div>
</template>
<script type="text/ecmascript-6">
import Pagination from "@/components/Pagination";
import comprehensiveQueryApi from "@/api/basicEdition/comprehensiveQuery";
import FundListDialogMultiphase from "@/components/FundListDialogMultiphase";
import {downLoadFileByUrl} from "@/utils";
import commonFun from "@/filters/common";
import commonApi from "@/api/common";
import productSelector from '@/components/productSelector'
import moment from 'moment'

export default {
  components: {
    Pagination,
    FundListDialogMultiphase,
    productSelector
  },
  name: "valuationTableSearch",
  data() {
    const validatebeginDate = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请选择开始日期"));
      } else {
        if (this.formQuery.endDate !== null || this.formQuery.endDate !== undefined || this.formQuery.endDate !== "") {
          let startTime = new Date(value);
          let endTime = new Date(this.formQuery.endDate);
          if (startTime > endTime) {
            callback(new Error("开始日期不能大于结束日期"));
          } else {
            callback();
          }
        } else {
          callback();
        }
      }
    };
    const validateEndDate = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请选择结束日期"));
      } else {
        if (
          this.formQuery.beginDate !== null ||
          this.formQuery.beginDate !== undefined ||
          this.formQuery.beginDate !== ""
        ) {
          let startTime = new Date(this.formQuery.beginDate);
          let endTime = new Date(value);
          if (startTime > endTime) {
            callback(new Error("结束日期不能小于开始日期"));
          } else {
            callback();
          }
        } else {
          callback();
        }
      }
    };
    return {
      tags: [],
      // 搜索
      formQuery: {
        ddate_: [],
        date: [],
        // 组合代码
        fundCodes: "",
        // 组合名称
        fundNames: "",
        // 科目代码
        symBolCode: "",
        // 科目名称
        kmmc: "",
        beginDate: "",
        endDate: "",
        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10,
        //排序方式
        orderString: ""
      },
      //搜索建议数据
      restaurantsCode: [],
      restaurantsName: [],
      //表格数据
      tableData: [],
      issearchButton: false,
      selectList: [],
      treeData: [
        {
          label: '产品列表',
          id: 'zstgwb'
        },
        {
          label: '私有产品',
          code: 'sycp'
        }
      ],
      showTreeKeyArray: ['产品列表', '私有产品'],

      tableLoading: false,
      total: 0,

      minTableWidth: "150",
      dialogMask: false,

      searchRules: {
        ddate_: [{required: true, message: "请选择日期", trigger: "change"}],
        // beginDate: [
        //   { required: true, message: "请选择开始日期", trigger: "change" },
        //   { validator: validatebeginDate, trigger: "change" },
        // ],
        // endDate: [
        //   { required: true, message: "请选择结束日期", trigger: "change" },
        //   { validator: validateEndDate, trigger: "change" },
        // ],
        fundCode: [{required: true, message: "请选择产品代码", trigger: "change"}]
      },
      //成立日
      timDate:"",
      /* 按钮禁止与否 */
      isDisabled: false,
      // 导出图标
      downLoadIcon: "el-icon-download",
      // 导出提示文字
      downLoadText: "导出",
      exportLoading: false,

      baseApi: "", //页面根地址
      exportButton: false
    };
  },
  mounted() {
    let self = this;
    if (this.$store.state.setting.bussinessTwoEndDate) {
      self.formQuery.endDate = this.$store.state.setting.bussinessTwoEndDate;
    }
    //获取搜索建议的数据
    this.$refs.table1.connect(this.$refs.tableToolbar);
    if (self.$route.query) {
      if (self.$route.query.fundCode) {
        self.formQuery.fundCode = self.$route.query.fundCode;
      }
    }
    //默认显示个框架
    // self.onSubmit("formQuery");
  },
  methods: {
    handleFundNamesChange(val) {
      if (!val) {
        this.tags = [];
        this.formQuery.fundCodes = [];
        this.formQuery.fundNames = "";
      }
    },
    //获取选中数据
    // getTemplateRow(data) {
    //   this.formQuery.fundCode = data.data.fundCode;
    //   this.formQuery.fundName = data.data.fundName;
    //   this.dialogMask = false;
    // },
    // 获取选中数据
    /*getTemplateRow(val) {
      this.tags = val.data;
      const self = this;
      const arr = val.data;
      if (arr) {
        self.formQuery.fundCodes = [];
        self.formQuery.fundNames = "";
        arr.forEach(function (item, index) {
          index++;
          if (index < arr.length) {
            self.formQuery.fundNames = self.formQuery.fundNames + item.fundName + ",";
          } else {
            self.formQuery.fundNames = self.formQuery.fundNames + item.fundName;
          }
          self.timDate = item.createDate;
          self.formQuery.fundCodes.push(item.fundCode);
        });
      }
      this.dialogMask = false;
    },*/
    handleDialogClosed() {
      this.dialogMask = false
    },
    handleSubmitClick(arr) {
      const self = this;
      this.dialogMask = false
      if (arr) {
        self.formQuery.fundCodes = [];
        self.formQuery.fundNames = "";
        arr.forEach(function (item, index) {
          index++;
          if (index < arr.length) {
            self.formQuery.fundNames = self.formQuery.fundNames + item.VC_FUNDNAME + ",";
          } else {
            self.formQuery.fundNames = self.formQuery.fundNames + item.VC_FUNDNAME;
          }
          self.timDate = item.D_CREATE_DATE;
          self.formQuery.fundCodes.push(item.VC_FUNDCODE);

        });
      }
      this.selectList = arr
    },
    // 点击弹窗
    openFundListDialog() {
      this.dialogMask = true;
    },

    onSubmit(formName) {
      var self = this;
      self.formQuery.pageNum = 1;
      self.$refs[formName].validate((valid) => {
        if (valid) {
          self.onQuery();
          // 禁用搜索按钮
          self.$fun.searchButtonDisabled("issearchButton", self);
        } else {
          return false;
        }
      });
    },
    onQuery(flag) {
      var self = this;
      let params = Object.assign({}, this.formQuery, {});
      if (params.ddate_ && params.ddate_.length) {
        params.beginDate = params.ddate_[0];
        params.endDate = params.ddate_[1];
      }
      params.fundName = params.fundNames
      delete params.ddate_;
      if (flag) {
        self.downLoadText = "导出中...";
        self.exportLoading = true;
        self.isDisabled = true;
        params.pageNum = 1;
        params.pageSize = 999999999;
        params.ex_tmp_name = "估值表查询-导出.zip";
        // let url = "/api/comprehensiveQuery/selectValuationTableListPage";
        let url = "/api/comprehensiveQuery/downLoadZipBySelect";

        let fileName = "";
        if (params.fundCodes.length == 1) {
          fileName = params.fundCodes[0] + "_" + params.fundNames + "_" +
            params.beginDate.replace(/\-/g, "") + "-" +
            params.endDate.replace(/\-/g, "") + "_估值表查询.zip";
        } else {
          fileName = params.beginDate.replace(/\-/g, "") + "-" +
            params.endDate.replace(/\-/g, "") + "_估值表查询.zip";
        }
        params.fundCodes = params.fundCodes.toString()

        downLoadFileByUrl(url, params, fileName, self);
        return;
      }

      if (!flag) {
        this.tableLoading = true;
      }
      params.fundCodes = params.fundCodes.toString()
      new Promise((resolve, reject) => {
        comprehensiveQueryApi
          .fun_selectValuationTableListPage(params)
          .then((res) => {
            let {status, data} = res;
            if (status === 0) {
              if (data != null && data != undefined) {
                if (!flag) {
                  let {list, total} = data;
                  this.tableData = list;
                  this.total = total;
                }
                if (flag) {
                  if (!data) return;
                  this.$fun.commonDownloadUrl(data);
                }
              }
            } else {
              self.$message({
                message: "系统异常",
                type: "warning"
              });
            }
            this.tableLoading = false;
            self.exportLoading = false;
            self.downLoadText = "导出数据";
          })
          .catch((error) => {
            this.tableLoading = false;
            self.exportLoading = false;
            self.downLoadText = "导出数据";
            reject(error);
          });
      });
    },
    //导出
    downloadTableExcel() {
      this.onQuery(true);
    },
    //日期时间段快捷选项
    dateShortTPCTA() {
      var self = this
      const pickerOptions = {
        shortcuts: [{
          text: '本周',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
            const start = moment(end).isoWeekday(1).format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '本月',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
            const start = moment([moment(end).year(), 0, 1]).month(moment(end).month()).format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '本季度',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
            const start = moment(moment(end).year() + '-01-01').quarter(moment(end).quarter()).format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '今年以来',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
            const start = moment(end).year() + '-01-01'
            picker.$emit('pick', [start, end])
          }
        },
          {
            text: '成立以来',
            onClick(picker) {
              self.getStandard();
                const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
                const start = self.timDate
                picker.$emit('pick', [start, end])

            }
          },
          {
            text: '近一个月',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(1, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          }, {
            text: '近三个月',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(3, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          }, {
            text: '近半年',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(6, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          }, {
            text: '近一年',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(1, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          }, {
            text: '近三年',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(3, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          },]
      }
      return pickerOptions
    },
    async getStandard() {
      if(this.formQuery.fundCodes.length == 0 || this.formQuery.fundNames ==""){
        this.timDate =""
        this.$message({
          message: '请先选择产品！',
          type: 'warning',
          customClass: "message-warning"
        });
        return
      }
      if(this.formQuery.fundCodes.length > 1){
        this.timDate =""
        this.$message({
          message: '请选择单个产品！',
          type: 'warning',
          customClass: "message-warning"
        });
        return
      }
      if(this.timDate == "" || this.timDate == undefined || this.timDate == null){
        this.$message({
          message: '未获取到成立日！',
          type: 'warning',
          customClass: "message-warning"
        });
        return
      }
    },
    // 清除
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
    // 分页点击事件
    pagination(val) {
      // let { page, limit } = val;
      let {currentPage, pageSize} = val;
      // 起始页
      this.formQuery.pageNum = currentPage;
      // 每页数量
      this.formQuery.pageSize = pageSize;
      // 查询
      this.onQuery();
    },
    // 通用下载 模板
    downloadExport(formName) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          // 修改导出的一些样式和按钮效果
          this.exportButton = true;
          this.exportIcon = "el-icon-loading";
          this.exportText = "导出中...";

          const params = Object.assign({}, this.formQuery);
          params.fundCodes_list = this.formQuery.fundCodes;

          // 删除多余的 传参
          delete params._pageNum;
          delete params._pageSize;
          delete params._pageFlag;

          // 导出模板ID，这个 写死的，配置在数据库里面可以查询到
          params.indexCode = "c125b9de-c026-4db2-beac-e8d531a5499b";
          // 获取token
          params.token = this.$store.state.user.token;
          // 配置url路径，templateCode 后面的值和indexCode是一样的
          const url =
            this.$store.state.setting.baseApi +
            "/api/comprehensiveQuery/downLoadZipBySelect";

          // 导出的方法我们是无法监听到完成的结果时间的，因此这边处理方式采用的是 三秒后放开导出权限
          setTimeout(() => {
            // 调用公共的方法下载导出的excel文件
            commonFun.formDownloadFileMethod(params, url, "post");
            this.exportButton = false;
            this.exportIcon = "el-icon-download";
            this.exportText = "导出";
          }, 3000);
        } else {
          this.$message.closeAll();
          this.$message({
            message: "请根据提示信息做修改",
            type: "warning",
          customClass: "message-warning"
          });
          // 导出的方法我们是无法监听到完成的结果时间的，因此这边处理方式采用的是 五秒后放开导出权限
          setTimeout(() => {
            this.exportButton = false;
            this.exportIcon = "el-icon-download";
            this.exportText = "导出";
          }, 5000);
        }
      });
    },
    // 当表格的排序条件发生变化的时候会触发该事件
    handleSortChange(val) {
      if (val.property == "kmbm") {
        val.property = "a.vc_fkmbm";
      } else if (val.property == "kmmc") {
        val.property = "a.vc_fkmmc";
      } else if (val.property == "counts") {
        val.property = "f_fzqsl";
      } else if (val.property == "cbPrice") {
        val.property = "f_fzqcb";
      } else if (val.property == "cbRate") {
        val.property = "a.vc_fcb_jz_bl";
      } else if (val.property == "hqPrice") {
        val.property = "f_fhqjg";
      } else if (val.property == "sjPrice") {
        val.property = "a.f_fzqsz";
      } else if (val.property == "sjRate") {
        val.property = "a.vc_fsz_jz";
      } else if (val.property == "fDate") {
        val.property = "a.d_fdate";
      }
      this.formQuery.orderString = this.$fun.queryOrderBy_vxe(val);
      // 查询
      this.onQuery();
    }
  },
  watch: {}
};
</script>

<style lang="scss">
.customWidth {
  width: 70% !important;
}

.valuationTableSearch {
  .funds-filter {
    width: 100%;
    // border-bottom: 1px solid #e1e0e0;
  }

  .p1 {
    font-family: FZLanTingHei;
    font-weight: 500;
    font-size: 14px;
    color: rgb(16, 16, 16);
    font-style: normal;
    letter-spacing: 0px;
    line-height: 20px;
    text-decoration: none;
    text-align: left;
  }
  .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
  input::-webkit-input-placeholder {
    color: #999 !important;
  }
  .title-style {
    color: #e03d3e;
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
    background-color: #e03d3e;
  }
  .customWidth {
    width: 70% !important;
  }
  .item-label {
    font-size: 14px;
  }

  .item-label {
    font-size: 14px;
  }

  .vxe-pager.size--medium {
    font-size: 14px;
  }

  .el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell {
    background: #f8f8f8;
  }
  .el-dialog {
    width: 54% !important;
    .el-form {
      width: 100% !important;
      font-size: 0;
    }
    .item-label {
      font-size: 14px;
    }
    .vxe-pager.size--medium {
      font-size: 14px;
    }
    .el-table--striped .el-table__body tr.el-table__row--striped td.el-table__cell {
      background: #f8f8f8;
    }

    .el-form-item {
      min-width: 50%;
      margin-right: 0;
    }
    .mr5 {
      margin-right: 5px;
    }
  }
}
</style>

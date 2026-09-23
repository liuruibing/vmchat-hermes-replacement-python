<template>
  <div class="currency_report_old_copy vxe_custom_style">
    <el-tabs
      v-model="activeName"
      v-if="tabArr.length > 1"
      @tab-click="handleClick"
    >
      <el-tab-pane
        v-for="item in tabArr"
        :key="item.tableCode"
        :label="item.tableCn"
        :name="item.tableCode"
      >
      </el-tab-pane>
    </el-tabs>

    <!-- <el-form
      :inline="true"
      v-if="crudEnable.indexOf('C') != -1 || crudEnable.indexOf('R') != -1"
      ref="formInline"
      :model="formInline"
      style="margin-bottom: 8px;width:100% !important;"
      class="demo-form-inline form_inline_search"
    >
      <el-row>
        <el-col :span="18">
          <div style="width: 100%; min-height: 50px">
            <el-form-item
              v-for="(item, index) in searchDataArr"
              :key="index"
              :label="item.fieldCn"
              :prop="item.fieldEn"
              :label-width="index > 0 ? '100px' : '100px'"
            >
              <el-input
                v-model="formInline[item.fieldEn]"
                type="text"
                v-if="item.fieldType != 'D' && !item.dicSql"
                auto-complete="off"
                size="small"
                clearable
                placeholder="请输入"
              />

              <el-select
                v-if="item.dicSql"
                clearable
                filterable
                v-model="formInline[item.fieldEn]"
                size="small"
                placeholder="请选择"
              >
                <el-option
                  v-for="(group, index) in formSelectArr[item.fieldEn]"
                  :value="group.DIM_CDE"
                  :key="index"
                  :label="group.DIM_NME"
                >
                </el-option>
              </el-select>

              <el-date-picker
                v-model="formInline[item.fieldEn]"
                type="date"
                size="small"
                v-if="item.fieldType === 'D'"
                value-format="yyyy-MM-dd"
                placeholder="选择日期"
              >
              </el-date-picker>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="6">
          <el-form-item class="search_button_com">
            <el-button type='primary' v-if="crudEnable.indexOf('R')!=-1 "  @click="addSearchList" style='margin-bottom: 5px; ' size='small'><i class="el-icon-circle-plus-outline"></i>添加条件</el-button>
            <el-button
              type="primary"
              v-if="crudEnable.indexOf('R') != -1"
              @click="onSubmit(true)"
              style="margin-bottom: 5px"
              size="small"
              ><i class="el-icon-search"></i>查询</el-button
            >
            <el-button
              type="primary"
              v-if="crudEnable.indexOf('C') != -1"
              plain
              @click="addData()"
              style="margin-bottom: 5px"
              size="small"
              ><i class="el-icon-circle-plus-outline"></i>新增</el-button
            >
          </el-form-item>
        </el-col>
      </el-row>
    </el-form> -->

    <!-- :custom-config="{storage: true, checkMethod: checkColumnMethod}"  -->
    <div v-loading="tableLoading" style="">
      <div class="forms_table_title" style="float: left">
        <i class="el-icon-s-data"></i>列表
        <span style="margin-left:20px">
            <el-button v-if="crudEnable.indexOf('E')!=-1" type="primary" plain @click="downloadFile('excel')" style="margin-bottom: 5px; " size="small">
              <i class="el-icon-download"></i>下载Excel
            </el-button>
            <el-button v-if="crudEnable.indexOf('T')!=-1" type="primary" plain @click="downloadFile('txt')" style="margin-bottom: 5px; " size="small">
              <i class="el-icon-download"></i>下载Txt
            </el-button>
            <el-button v-if="crudEnable.indexOf('P')!=-1" type="primary" plain @click="downloadFile('pdf')" style="margin-bottom: 5px; " size="small">
              <i class="el-icon-download"></i>下载PDF
            </el-button>
          </span>
      </div>

      <div class="vxetable-style" style="height:calc(100vh - 180px)">
        <vxe-toolbar
          v-if="tableShow"
          custom
          style="position: relative; right: 45px"
        ></vxe-toolbar>
        <vxe-table
          class="mytable-scrollbar"
          :cell-class-name="cellClassName"
          :header-cell-class-name="headerCellClassName"
          highlight-hover-row
          border
          stripe
          resizable
          show-overflow
          size="small"
          :export-config="{}"
          ref="xTable"
          v-if="tableShow"
          @custom="toolbarCustomEvent"
          :data="tableData"
          auto-resize
          height="auto"
        >
          <vxe-table-column
            v-for="(group, index) in tableDataDetailArr"
            :key="index"
            :visible="group.flag"
            min-width="160"
            header-align="center"
            :field="group.fieldEn"
            :title="group.fieldCn"
          >
          <template slot="default" slot-scope="{row}">
              <template v-if="!group.formatShow&&group.inputType!=='select'&&!group.dicSql">
                <span>{{row[group.fieldEn]}}</span>
              </template>
              <template v-if="!group.formatShow&&group.inputType=='select' || group.dicSql">
                <!-- <span v-for="item in formSelectArr[group.fieldEn]" :key="item.DIM_CDE">
                  <template v-if="row[group.fieldEn]==item.DIM_CDE">
                    <span>{{item.DIM_NME}}</span>
                  </template>
                </span> -->
                <span>{{transf(group.fieldEn,row[group.fieldEn])}}</span>
              </template>
              <template v-if="group.formatShow">
                <span>{{row[group.fieldEn]}}</span>
              </template>
            </template>
          </vxe-table-column>

          <vxe-table-column
            fixed="right"
            v-if="
              crudEnable.indexOf('U') != -1 || crudEnable.indexOf('D') != -1
            "
            title="操作"
            width="200"
            show-overflow
            align="center"
          >
            <template slot-scope="scope">
              <el-button
                v-if="crudEnable.indexOf('U') != -1"
                type="primary"
                size="small"
                @click="editData(scope.row, true)"
                >查看详情</el-button
              >
              <el-button
                v-if="crudEnable.indexOf('U') != -1"
                type="primary"
                size="small"
                @click="editData(scope.row, false)"
                >编辑</el-button
              >
              <el-button
                v-if="crudEnable.indexOf('D') != -1"
                type="danger"
                plain
                size="small"
                @click="delData(scope.row)"
                >删除</el-button
              >
            </template>
          </vxe-table-column>
        </vxe-table>
        <Pagination
          v-if="isPage == 1"
          :total="total"
          :page="formInline.pageNum"
          :limit="formInline.pageSize"
          @pagination="Pagination"
        ></Pagination>
      </div>
    </div>

    <!-- 新增代办 -->
    <el-dialog
      :title="countTitle"
      append-to-body
      customClass="currencyReportWidth"
      center
      :visible.sync="countDialog"
      :close-on-click-modal="false"
    >
      <el-container>
        <el-main class="mainBox">
          <el-form
            :inline="true"
            ref="formCount"
            :model="formCount"
            :rules="countRules"
            label-position="right"
          >
            <el-form-item
              v-for="(item, index) in addDataArr"
              :key="index"
              :label="item.fieldCn"
              :prop="item.fieldEn"
              class="mb20"
              :label-width="formLabelWidth"
            >
              <el-input
                v-model="formCount[item.fieldEn]"
                type="text"
                v-if="item.fieldType != 'D' && !item.dicSql"
                auto-complete="off"
                size="small"
                clearable
                :disabled="isSearchDetail"
                placeholder="请输入"
              />

              <el-select
                :disabled="isSearchDetail"
                v-if="item.dicSql"
                clearable
                filterable
                v-model="formCount[item.fieldEn]"
                size="small"
                placeholder="请选择"
              >
                <el-option
                  v-for="(group, index) in formSelectArr[item.fieldEn]"
                  :value="group.DIM_CDE"
                  :key="index"
                  :label="group.DIM_NME"
                >
                </el-option>
              </el-select>

              <el-date-picker
                v-model="formCount[item.fieldEn]"
                type="date"
                size="small"
                :disabled="isSearchDetail"
                v-if="item.fieldType === 'D'"
                value-format="yyyy-MM-dd"
                placeholder="选择日期"
              >
              </el-date-picker>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="countDialog = false">取 消</el-button>
        <el-button
          v-if="!isSearchDetail"
          type="primary"
          size="small"
          :loading="countSubmit_btn"
          @click="countSubmit('formCount')"
          >确 定</el-button
        >
      </div>
    </el-dialog>

    <el-dialog
      title="添加查询条件"
      append-to-body
      customClass="currencyReportWidth"
      center
      :visible.sync="searchDialog"
      :close-on-click-modal="false"
    >
      <el-container>
        <el-main class="mainBox">
          <el-checkbox
            :indeterminate="isIndeterminate"
            v-model="checkAll"
            @change="handleCheckAllChange"
            >全选</el-checkbox
          >
          <div style="margin: 15px 0"></div>
          <el-checkbox-group
            v-model="checkedForms"
            @change="handlecheckedFormsChange"
          >
            <el-checkbox
              v-for="(item, index) in searchForms"
              :label="item.fieldEn"
              :key="index"
              >{{ item.fieldCn }}</el-checkbox
            >
          </el-checkbox-group>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="searchDialog = false">取 消</el-button>
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
      center
      :visible.sync="detailDialog"
      width="80% !important"
      :close-on-click-modal="false"
    >
    <currencyReport2 style="height:100%" :currencyReportPageData="currencyReportPageData_dialog"></currencyReport2>
    </el-dialog>
  </div>
</template>

<script>
import $ from "jquery";
import Pagination from "@/components/Pagination";
import commonFun from "@/filters/new_common";
import pageApi from "@/api/dataReport/currencyReport";
import commonApi from "@/api/common";
export default {
  name: "currencyReport2",
  components: { Pagination },
  props: {
    currencyReportPageData: {
      type: Object,
    },
  },
  data() {
    return {
      tableData: [{ id: 1, name: "测试一", sex: "男", age: 12 }],
      activeName: "",
      tabArr: [{ dimCde: "1", dimNme: "测试" }],
      showTitle: 0,
      formInline: {
        reportName: "",
        reportCode: "",
        tableCode: "",
        pageSize: 50,
        pageNum: 1,
      },
      reportCode: "",
      total: 0, //总条数
      tableDataDetailArr: [
        { code: "id", flag: true, name: "主键" },
        { code: "name", flag: true, name: "姓名" },
        { code: "sex", flag: true, name: "性别" },
        { code: "age", flag: false, name: "年龄" },
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
      isPage: 1, //是否分页判断
      formSelect: {}, //下拉框字典值
      formSelectArr: {}, //下拉框字典值数组
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
      detailDialog:false, //明细弹框
      currencyReportPageData_dialog:{
        dataDate:"2019-06-28",
        endDate: "2019-06-28",
        fundType: "ALL",
        recordId: "033F3A8A47AA4AD893BA83B44877CAE8",
        reportCode: "26",
        typeIn: "ALL"
      }
    };
  },
  mounted() {
    this.activeName = this.tabArr[0].dimCde;
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
    this.getTabData();
  },
  computed:{
    transf(){
      return (v1,v2)=>{
        // console.log(v1,v2);
        let len = Object.keys(this.formSelectArr).length;
        // console.log('lem',len);
        if(len<1) return v2
        if(this.formSelectArr[v1]){
          let obj = this.formSelectArr[v1].filter(item=>{
            // console.log(item);
            if(item.DIM_CDE == v2){
              return item
            }
            
          })
          // console.log('obj.DIM_NME',obj);
          if(obj.length){
            return obj[0].DIM_NME
          }else{
            return v2
          }
        }else{
          return v2
        }
      }
    },
  },
  methods: {
    cellClassName({ row, rowIndex, column, columnIndex }) {
      return "vxe-cell-class-name";
    },
    headerCellClassName({ column, columnIndex }) {
      return "vxe-header-cell-class-name";
    },
    currencyInit(data) {
      //  this.currencyReportPageData = data
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
      this.getTabData();
    },
    handleClick(tab, event) {
      //debugger;
      let name = this.activeName;
      let arr = this.tabArr;
      for (let i = 0; i < arr.length; i++) {
        if (arr[i].tableCode == name) {
          this.isPage = arr[i].isPage;
          if (arr[i].crudEnable) {
            this.crudEnable = arr[i].crudEnable;
          } else {
            this.crudEnable = "-1";
          }
        }
      }
      this.isSearchSelect = 0;
      this.searchDataArr = [];
      this.formInline.pageSize = 50;
      this.formInline.pageNum = 1;
      this.onSubmit(true);
    },
    //分页
    Pagination(val) {
      this.formInline.pageSize = val.limit; //页面条数
      this.formInline.pageNum = val.page; //页面
      this.onSubmit(false);
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
    onSubmit(flag,type) {
      this.tableLoading = true;
      // 消除没有值的参数
      if (flag) {
        this.formInline.pageNum = 1;
      }
      this.tableShow = false;
      this.formInline.tableCode = this.activeName;

      let params = commonFun.parameterSrc(this.formInline);
      params.reportCode = this.reportCode;
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
              this.tableDataDetailArr = data.fieldsInfo;
              this.getAllPrpos(data.fieldsInfo);
            }
            if (this.isPage == 1) {
              this.tableData = data.dataList.list;
            } else {
              this.tableData = data.dataList;
            }

            // 页面总条数
            if (data.dataList.total) {
              this.total = data.dataList.total;
            }else{
              this.total = 0;
            }

            this.fieldsInfoArr = data.fieldsInfo;
            if(type=="mounted"){
              this.searchDataArr = [];
              let searcharr = data.fieldsInfo.filter(item=>{
                return item.isCrud.indexOf('M')!=-1
              })
              this.searchDataArr = searcharr;
            }
            this.tableShow = true;
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
          this.countRules[fieldsInfoArr[i].fieldEn] = rulesArr;
        }
      }
      this.addDataArr = arr;
      this.operationType = 1;
      this.formCount = params;
      this.countTitle = "新增";
      this.isSearchDetail = false;
      this.countDialog = true;
    },
    editData(row, flag) {
      let arr = [];
      let fieldsInfoArr = this.fieldsInfoArr;
      let params = {};
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
          this.countRules[fieldsInfoArr[i].fieldEn] = rulesArr;
        }
      }
      if (row) {
        for (var p in row) {
          params[p] = row[p];
        }
      }
      this.addDataArr = arr;
      this.operationType = 2;
      this.formCount = params;

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
                this.onSubmit(false);
              } else {
                // 关闭移动指标弹框
                //this.countDialog = false;
                this.$message.closeAll();
                this.$message({
                  message: response.data.message || "删除失败",
                  type: "warning",
                });
              }
            })
            .catch(() => {
              // 关闭移动指标弹框

              this.$message.closeAll();
              this.$message({
                message: "删除失败",
                type: "warning",
              });
            });
        })
        .catch(() => {});
    },
    getAllPrpos(formData) {
      // 用来保存所有的属性名称和值

      let arr = [];
      let params = {};
      let searchForms = [];
      let checkAllForms = [];
      for (let i = 0; i < formData.length; i++) {
        //获取列表，表头
        if (formData[i].isCrud && formData[i].isCrud.indexOf("R") != -1) {
          let data = {};

          data[formData[i].fieldEn] = formData[i].fieldCn;
          // 开始遍历
          for (var p in data) {
            let params = {};
            // 方法
            // p 为属性名称，obj[p]为对应属性的值
            params.code = "" + p;
            params.name = data[p];
            params.flag = true;
            arr.push(params);
          }
        }
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
      return arr;
    },
    //获取tab数据
    getTabData() {
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
      pageApi
        .getTabData(params)
        .then((response) => {
          if (response.data.status === 200) {
            // 关闭移动指标弹框
            let arr = response.data.data;
            if (arr && arr.length > 0) {
              this.tabArr = arr;
              this.activeName = arr[0].tableCode;
              this.isPage = arr[0].isPage;
              if (arr[0].crudEnable) {
                this.crudEnable = arr[0].crudEnable;
              } else {
                this.crudEnable = "-1";
              }

              this.onSubmit(true,"mounted");
            } else {
              this.tabArr = [];
            }
          } else {
            this.$message.closeAll();
            this.$message({
              message: response.data.message || "数据初始化失败",
              type: "warning",
            });
          }
        })
        .catch(() => {
          this.$message.closeAll();
          this.$message({
            message: response.data.message || "数据初始化失败",
            type: "warning",
          });
        });
    },
    //新增,编辑确认
    countSubmit(formName) {
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
        type: "warning",
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
                  type: "warning",
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
                type: "warning",
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
        type: "warning",
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
                  type: "warning",
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
                type: "warning",
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
            this.$set(this.formSelectArr,val,response.data.data)
          } else {
            this.$message.closeAll();
            this.$message({
              message: response.data.message || "获取下拉内容失败",
              type: "warning",
            });
          }
        })
        .catch(() => {
          // 关闭移动指标弹框

          this.$message.closeAll();
          this.$message({
            message: "获取下拉内容失败",
            type: "warning",
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
              params[fieldsInfoArr[j].fieldEn] = "";
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
    downloadFile (type) {
      this.formInline.tableCode = this.activeName;
      let params = commonFun.parameterSrc(this.formInline);
      params.reportCode = this.reportCode;
      params.pageSize = null
      params.pageNum = null
      if(this.currencyReportPageData){
        let data = this.currencyReportPageData;
            
        for(var p in data){
          params[p] = data[p];
        }
      }
      if(this.pathSearchData){
        let data = this.pathSearchData;
            
        for(var p in data){
          params[p] = data[p];
        }
      }
      params.type = type;
      // params.token = this.$store.getters.token;
      params = commonFun.parameterSrc(params);
      params = JSON.stringify(params)
      // 获取表头字段
      let arr = [];
      let tableHeader = this.$refs.xTable.getColumns();
      if(tableHeader.length){
        tableHeader.forEach(item=>{
          if(item.type!='seq'){
            arr.push(item.property)
          }
        })
      }
      let obj = {
        mapType:params,
        tableHeader:arr,
        token:this.$store.getters.token
      }
      let action = this.$store.state.setting.baseApi + '/api/reportShow/v1.0/exportExcel';
      commonFun.formDownloadFile(obj,action,'post');
    },
    // 添加条件
    addSearchList(){
      this.searchDialog = true;
      let arr = this.searchDataArr.map(item=>{
        return item.fieldEn
      })
      this.checkedForms = arr;
    },
    detailData(row){
      console.log(row);
      this.detailDialog = true;
    }
  },
};
</script>
<style lang='css' scoped>
.mytable-style .vxe-body--row.row-green {
  background-color: #187;
  color: #fff;
}
</style>

<style lang="scss">
.currencyReportWidth {
  width: 55% !important;
}
.currency_report_old_copy{
        /*滚动条整体部分*/
        .mytable-scrollbar ::-webkit-scrollbar {
          width: 10px;
          height: 12px;
        }
        /*滚动条的轨道*/
        .mytable-scrollbar ::-webkit-scrollbar-track {
          background-color: #FFFFFF;
        }
        /*滚动条里面的小方块，能向上向下移动*/
        .mytable-scrollbar ::-webkit-scrollbar-thumb {
          background-color: #bfbfbf;
          border-radius: 5px;
          border: 1px solid #F1F1F1;
          box-shadow: inset 0 0 6px rgba(0,0,0,.3);
        }
        .mytable-scrollbar ::-webkit-scrollbar-thumb:hover {
          background-color: #A8A8A8;
        }
        .mytable-scrollbar ::-webkit-scrollbar-thumb:active {
          background-color: #787878;
        }
        /*边角，即两个滚动条的交汇处*/
        .mytable-scrollbar ::-webkit-scrollbar-corner {
          background-color: #FFFFFF;
        }
}
</style>
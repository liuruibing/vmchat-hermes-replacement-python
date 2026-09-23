<template>
   <div class="currency_report vxe_custom_style">
    <el-tabs v-model="activeName" v-if="tabArr.length >1" @tab-click="handleClick">
      <el-tab-pane  v-for="item in tabArr" :key="item.tableCode"   :label="item.tableCn" :name="item.tableCode">
      </el-tab-pane>
   
    </el-tabs>

    <el-form :inline='true' v-if="crudEnable.indexOf('C')!=-1 || crudEnable.indexOf('R')!=-1 "  ref='formInline' :model='formInline' style='margin-bottom: 8px;' class='demo-form-inline form_inline_search' >
    <el-row style="display:none;">
      <el-col :span='18'>
         <div style='width:100%;min-height:50px;'>
             
           <!-- <el-form-item v-for="(item,index) in searchDataArr" :key="index" :label="item.fieldCn"  :prop="item.fieldEn"  :label-width="index>0?'100px':'100px'">
               <el-input
                  v-model="formInline[item.fieldEn]"
                  type="text"
                  v-if="item.fieldType!='D' && !item.dicSql"
                  auto-complete="off"
                  size="small"
                  clearable
                  placeholder="请输入"
                />

                 <el-select  v-if="item.dicSql" clearable filterable  v-model="formInline[item.fieldEn]"  size="small"  placeholder="请选择"  >
                    <el-option
                      v-for="(group, index) in formSelectArr[item.fieldEn]"
                      :value="group.DIM_CDE"
                      :key="index"
                      :label="group.DIM_NME">
                    </el-option>
               </el-select>

                <el-date-picker
                  v-model="formInline[item.fieldEn]"
                  type="date"
                   size="small"
                    v-if="item.fieldType==='D'"
                  value-format="yyyy-MM-dd"
                  placeholder="选择日期">
              </el-date-picker> 
            </el-form-item> -->
         </div>
      </el-col>
      <el-col :span='6'>
         <el-form-item class='search_button_com'>
            <!-- <el-button type='primary' v-if="crudEnable.indexOf('R')!=-1 "  @click="addSearchList" style='margin-bottom: 5px; ' size='small'><i class="el-icon-circle-plus-outline"></i>添加条件</el-button> -->
            <!-- <el-button type="primary" v-if="crudEnable.indexOf('C')!=-1"  plain  @click="addData()" style="margin-bottom: 5px; " size="small"><i class="el-icon-circle-plus-outline"></i>新增</el-button> -->
            <!-- <el-button type='primary' v-if="crudEnable.indexOf('R')!=-1 " @click='onSubmit(true)' style='margin-bottom: 5px;' size='small'><i class='el-icon-search'></i>查询</el-button> -->
        </el-form-item>
      </el-col>
    </el-row>
  </el-form>
      
       
     
       
        
        <!-- :custom-config="{storage: true, checkMethod: checkColumnMethod}"  -->
        <div v-loading="tableLoading" style="">
           <div class='forms_table_title' style="float: left;">
          <i class='el-icon-s-data'></i>列表
          <span style="margin-left:20px">
            <el-button v-if="crudEnable.indexOf('C')!=-1" type="success" plain  @click="insertEvent" style="margin-bottom: 5px; margin-left:20px" size="small">
              <i class="el-icon-circle-plus-outline"></i>新增
            </el-button>
            <el-button v-if="crudEnable.indexOf('D')!=-1" type="danger" plain  @click="removeEvent" style="margin-bottom: 5px; " size="small">
              <i class="el-icon-delete"></i>移除
            </el-button>
            <el-button v-if="crudEnable.indexOf('U')!=-1 || crudEnable.indexOf('D')!=-1" type="primary" plain  @click="save" style="margin-bottom: 5px; " size="small">
              <i class="el-icon-collection"></i>保存
            </el-button>
            <!-- <el-button type="primary"  @click="openExportEvent" style="margin-bottom: 5px; " size="small">
              打印
            </el-button> -->
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
          <div class="zhaiyao_tuli">
            <!-- <div>图例：</div> -->
            <div class="zhaiyao_tuli_item">
              <span>平台有，外包无</span>
              <div class="color1 box"></div>
            </div>
            <div class="zhaiyao_tuli_item">
              <span>平台有，外包有 差异</span>
              <div class="color2 box"></div>
            </div>
            <div class="zhaiyao_tuli_item">
              <span>平台无，外包有</span>
              <div class="color3 box"></div>
            </div>
          </div>    
          </div>
             
        <div class="vxetable-style">
      <vxe-toolbar   v-if="tableShow" custom style="position: relative; right: 45px;"></vxe-toolbar>
        <vxe-table
          class="mytable-scrollbar"
          :cell-class-name="cellClassName"
          :header-cell-class-name="headerCellClassName"
          :footer-cell-class-name="cellClassName"
          highlight-hover-row
          keep-source
          border
          stripe
          resizable
          auto-resize
          size="small"
          :export-config="{}"
          :tooltip-config="{showAll: true, contentMethod: showTooltipMethod}"
          ref="xTable"
          v-if="tableShow"
          :cell-style="cellStyle"
          @custom="toolbarCustomEvent"
          :edit-rules="validRules"
          :edit-config="editConfig"
          :scroll-x="{enabled: false}"
          :scroll-y="{enabled: false}"
          show-footer
          :data="tableData">
          <!-- :footer-method="footerMethod" -->
         <vxe-table-column type="checkbox" width="60" v-if="crudEnable.indexOf('D')!=-1"></vxe-table-column>
          <!-- <vxe-table-column
          v-for="(group, index) in tableDataDetailArr"
          :key="index" 
          :visible="group.flag" 
           min-width="100"
           header-align="center"
           :edit-render="editRender(group.fieldType)"
          :field="group.fieldEn" 
          :title="group.fieldCn">
          </vxe-table-column> -->

          <vxe-table-column
          :filters="[{data: {vals: [], sVal: '', fMenu: '', f1Type:'', f1Val: '', fMode: 'and', f2Type: '', f2Val: ''}}]"
          :filter-render="{name: 'FilterExcel'}"
          
          v-for="group in tableDataDetailArr"
          :key="group.fieldEn" 
          :visible="group.flag" 
           min-width="160"
           header-align="center"
           :edit-render="editRender(group.fieldType)"
          :field="group.fieldEn" 
          :title="group.fieldCn">
            <template slot="edit" slot-scope="{row}">
              <template v-if="group.inputType=='input'">
                <vxe-input type="text" v-model="row[group.fieldEn]"></vxe-input>
              </template>
              <template v-else-if="group.inputType=='date'">
                <vxe-input v-model="row[group.fieldEn]" placeholder="日期选择" type="date" transfer></vxe-input>
              </template>
              <template v-else-if="group.inputType=='select'">
                <vxe-select v-model="row[group.fieldEn]" placeholder="请选择" transfer>
                  <vxe-option v-for="item in formSelectArr[group.fieldEn]" :key="item.DIM_CDE" :value="item.DIM_CDE" :label="item.DIM_NME"></vxe-option>
                </vxe-select>
              </template>
              <template v-else>
                <vxe-input type="text" v-model="row[group.fieldEn]"></vxe-input>
              </template>
            </template>
            <template slot="default" slot-scope="{row}">
              <template v-if="!group.formatShow&&group.inputType!=='select'&&!group.dicSql">
                <span>{{row[group.fieldEn]}}</span>
              </template>
              <template v-if="!group.formatShow&&group.inputType=='select'||group.dicSql">
                <!-- <span v-for="item in formSelectArr[group.fieldEn]" :key="item.DIM_CDE">
                  <template v-if="row[group.fieldEn]==item.DIM_CDE">
                    <span>{{item.DIM_NME}}</span>
                  </template>
                </span> -->
                <span>{{transf(group.fieldEn,row[group.fieldEn])}}</span>
              </template>
              <template v-if="group.formatShow">
                <!-- <span>{{row[group.fieldEn]}}</span> -->
                <span>{{format(row[group.fieldEn],group.fieldType,group.formatShow)}}</span>
              </template>
            </template>
          </vxe-table-column>

          <!-- <vxe-table-column fixed="right" v-if="crudEnable.indexOf('U')!=-1 || crudEnable.indexOf('D')!=-1 "  title="操作" width="200" show-overflow align="center">
             <template slot-scope="scope">
                <el-button v-if="crudEnable.indexOf('U')!=-1 " type="primary" size="small" @click="editData(scope.row,true)">查看详情</el-button>
                <el-button v-if="crudEnable.indexOf('U')!=-1 " type="primary" size="small" @click="editData(scope.row,false)">编辑</el-button>
                <el-button v-if="crudEnable.indexOf('D')!=-1 " type="danger" plain size="small" @click="delData(scope.row)">删除</el-button>
              </template>
          </vxe-table-column> -->
        </vxe-table>
        </div>
        </div>
         <Pagination v-if="isPage==1" :total="total" :page="formInline.pageNum" :limit="formInline.pageSize" @pagination ="Pagination"></Pagination>
       <!-- :pageSizes="[2,3,4,5]" -->
       <!-- 新增代办 -->
    <el-dialog :title="countTitle" append-to-body customClass="currencyReportWidth"   center :visible.sync="countDialog" :close-on-click-modal="false">
      <el-container >
        <el-main class="mainBox">
          <el-form
            :inline="true"
            ref="formCount"
            :model="formCount"
            :rules="countRules"
            label-position="right"
          >

           <el-form-item v-for="(item,index) in addDataArr" :key="index" :label="item.fieldCn"  :prop="item.fieldEn" class="mb20" :label-width="formLabelWidth">
               <el-input
                  v-model="formCount[item.fieldEn]"
                  type="text"
                  v-if="item.fieldType!='D' && !item.dicSql"
                  auto-complete="off"
                  size="small"
                  clearable
                  :disabled="isSearchDetail"
                  placeholder="请输入"
                />

                 <el-select   :disabled="isSearchDetail" v-if="item.dicSql" clearable filterable  v-model="formCount[item.fieldEn]"  size="small"  placeholder="请选择"  >
                    <el-option
                      v-for="(group, index) in formSelectArr[item.fieldEn]"
                      :value="group.DIM_CDE"
                      :key="index"
                      :label="group.DIM_NME">
                    </el-option>
               </el-select>

                <el-date-picker
                  v-model="formCount[item.fieldEn]"
                  type="date"
                   size="small"
                    :disabled="isSearchDetail"
                    v-if="item.fieldType==='D'"
                  value-format="yyyy-MM-dd"
                  placeholder="选择日期">
              </el-date-picker> 
            </el-form-item>

           
            
           
            
          </el-form>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="countDialog = false">取 消</el-button>
        <el-button v-if="!isSearchDetail"  type="primary" size="small" :loading="countSubmit_btn" @click="countSubmit('formCount')">确 定</el-button>
      </div>
    </el-dialog>

    <el-dialog title="添加查询条件" append-to-body customClass="currencyReportWidth"   center :visible.sync="searchDialog" :close-on-click-modal="false">
      <el-container >
        <el-main class="mainBox">
            <el-checkbox :indeterminate="isIndeterminate" v-model="checkAll" @change="handleCheckAllChange">全选</el-checkbox>
              <div style="margin: 15px 0;"></div>
              <el-checkbox-group v-model="checkedForms" @change="handlecheckedFormsChange">
                <el-checkbox v-for="(item,index) in searchForms" :label="item.fieldEn" :key="index">{{item.fieldCn}}</el-checkbox>
              </el-checkbox-group>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="searchDialog = false">取 消</el-button>
        <el-button  type="primary" size="small" :loading="countSubmit_btn" @click="searchSubmit()">确 定</el-button>
      </div>
    </el-dialog>
      
   </div>
</template>

<script>
import XEUtils from 'xe-utils'
import xbrlApi from "@/api/xbrl/xbrl"
import $ from 'jquery'
import Pagination from '@/components/Pagination'
import commonFun from '@/filters/new_common'
import pageApi from "@/api/dataReport/currencyReport";
import commonApi from "@/api/common";
import Vue from 'vue';
import { set } from 'xe-utils/methods'
export default {
   name:'currencyReport',
    components: {Pagination},
    props: {
      currencyReportPageData: {
        type: Object
      },
    },
   data () {
      return {
        LackLine:[],
        moreLineList:[],
        HDdata:[
          // {lineName:"1",columnName:"1",elementValueImp:"核对不一致",verifyStatus:"0"},
          // {lineName:"1",columnName:"2",elementValueImp:"核对一致",verifyStatus:"1"},
          // {lineName:"2",columnName:"1",elementValueImp:"核对不一致",verifyStatus:"0"},
          // {lineName:"2",columnName:"2",elementValueImp:"核对一致",verifyStatus:"1"},
          // {lineName:"2",columnName:"3",elementValueImp:"核对不一致",verifyStatus:"0"},
          // {lineName:"2",columnName:"4",elementValueImp:"核对不一致",verifyStatus:"0"},
        ],
          tableData: [{id:1,name:'测试一',sex:'男',age:12}],
          activeName: '',
          tabArr:[{dimCde:'1',dimNme:'测试'}],
          showTitle:0,
          formInline:{
            reportName:'',
            reportCode:'',
            tableCode:'',
            pageSize: 50,
            pageNum:1
          },
          reportCode:'',
          total:0,//总条数
          tableDataDetailArr:[
            // {code:'id',flag:true,name:'主键'},
            // {code:'name',flag:true,name:'姓名'},
            // {code:'sex',flag:true,name:'性别'},
            // {code:'age',flag:false,name:'年龄'}
          ],
          countDialog: false, // 弹窗
          countTitle:"",//标题
          countFormList:"",//是新增还是编辑
          // 新增 编辑计算任务
          formCount: {
              sealCode:'',//印章编码
              sealStatus:'', //印章状态
              
          },
          // 操作类型 1、添加 2、编辑
          operationType: 1,
          // 弹窗验证规则
          countRules: {},
          formLabelWidth: "120px",
          countSubmit_btn:false, //保存按钮加载
          tableLoading:false,//加载
          fieldsInfoArr:[],//字段数组
          tableShow:false,//列表展示控制
          addDataArr:[],//新增-编辑数组
          searchDataArr:[],//新增-编辑数组
          isPage:1,//是否分页判断
          formSelect:{}, //下拉框字典值
          formSelectArr:{}, //下拉框字典值数组
          formSelectArrtmp:{},
          searchDialog:false,
          checkAll: false,
          checkedForms: [],//已选择的查询条件
          searchForms: [],//查询条件数组
          combineds:[],//表尾合计字段数组
          checkAllForms:[],
          isIndeterminate: true,
          isSearchSelect:0, //是否查询下拉框的值
          tabFormArr:{}, //tab查询条件数组
          tabSearchArr:{}, //tab查询内容数组
          crudEnable:'', //按钮权限
          pathSearchData:{},
          isSearchDetail:false // 是否查看详情
         
      };
   },
   mounted() {
    //  console.log(this.currencyReportPageData);
     this.activeName = this.tabArr[0].dimCde;
     if(!this.currencyReportPageData){
       let path = this.$route.fullPath;
        let formData = path.split(":")[1];
        if(formData.indexOf('&') !=-1){
            let arr = formData.split('&');
            let params = {};
            for(let i=0;i<arr.length;i++){
                let a = arr[i].split("=");
                params[a[0]] = a[1];
            }
            this.pathSearchData = params;
        }else{
          this.reportCode = formData.split("=")[1];
        }
     }
     this.getTabData();
    //  this.getHDdata();
      
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
      validRules(){
        // console.log('1111111111');
        let fieldsInfoArr = this.fieldsInfoArr;
        let params = {};
        this.countRules = {};
        for(let i=0;i<fieldsInfoArr.length;i++){
              // if(fieldsInfoArr[i].isCrud && fieldsInfoArr[i].isCrud.indexOf('U')!=-1){
              //   arr.push(fieldsInfoArr[i]); 
              // }
          if(fieldsInfoArr[i].isCrud && fieldsInfoArr[i].isCrud.indexOf('U')!=-1&&fieldsInfoArr[i].isRequired && fieldsInfoArr[i].isRequired ==1){
            let rulesParams={}
            rulesParams.required=true;
            rulesParams.message="请输入"+fieldsInfoArr[i].fieldCn;
            rulesParams.trigger = 'change';
            // rulesParams.type = 'string';
            let rulesArr= [];
            rulesArr.push(rulesParams);
            // if(fieldsInfoArr[i].validateRule){
            //   let obj = eval("("+fieldsInfoArr[i].validateRule+")");
            //   // console.log(fieldsInfoArr[i].validateRule);
            //   // console.log(eval("("+fieldsInfoArr[i].validateRule+")"));
            //   let patternobj = {}
            //   patternobj.pattern = obj.rule.reg;
            //   patternobj.message = obj.rule.warn;
            //   patternobj.trigger = 'change';
            //   rulesArr.push(patternobj);
            // }
            this.countRules[fieldsInfoArr[i].fieldEn] = rulesArr;
          }
          if(fieldsInfoArr[i].isCrud && fieldsInfoArr[i].isCrud.indexOf('U')!=-1 && fieldsInfoArr[i].validateRule){
            // console.log('1111');
            let rulesArr = []
            // let str  = '{ "required": true, "pattern": "/^[a-zA-Z0-9]+$/" , "message": "请输入字母或数字" , "trigger": "change" }';
            let obj1 = JSON.parse(fieldsInfoArr[i].validateRule);
            let obj = {}
            obj.required = obj1.required || false;
            if(obj1.pattern){obj.pattern = eval(obj1.pattern)}
            obj.message = obj1.message || '';
            obj.trigger = obj1.trigger || 'change';
            rulesArr.push(obj);
            // console.log(this.formInlineRules);
            this.countRules[fieldsInfoArr[i].fieldEn] = rulesArr;
          }
        }
        // console.log('countRules',this.countRules);
       return this.countRules;
     },
     editConfig(){
       if(this.crudEnable.indexOf('U')!=-1){
         return {trigger: 'click', mode: 'cell',activeMethod: this.activeCellMethod}
       }else{
         return {}
       }
     },
   },
   methods: {
      cellClassName ({ row, rowIndex, column, columnIndex }) {
        return 'vxe-cell-class-name'
      },
      headerCellClassName ({ column, columnIndex }) {
        return 'vxe-header-cell-class-name'
      },
      //金额千分位
    amountFilter(num,float) {
      if(!num && num!=0){
        return ''
      }
      let n = Number(num);
      if(float){
        // console.log(float);
        n = n.toFixed(float)
      }
      return commonFun.formatNumber(n);
    },
    format(val,type,format){
      if(!val && val!==0) return ''
      if(type=='N'){
        if(format){  //#,###.00
          if(format.indexOf('.')!=-1 && format.indexOf(',')!=-1){
            let arr = format.split('.');
            if(arr.length>1){
              let str = arr[arr.length-1];
              if(str.length){
                return this.amountFilter(val,str.length);
              }
            }else{
              return this.amountFilter(val,false);
            }
          }else{
            return val
          }
        }else{
          return val
        }
      }
    },
      editRender(val){
       if(val!=='D'){
         return {name: 'input', attrs: {type: 'text'}}
       }else{
         return {name: '$input', props: {type: 'date'},events: {change: this.dateChangeEvent}}
       }
      },
      dateChangeEvent(row){
        this.$refs.xTable.clearActived()// 清除单元格激活状态 
        this.$refs.xTable.setActiveCell(row.row, row.column.property)// 设置单元格为激活状态
      },
      openExportEvent(){
        this.$refs.xTable.print()
        // this.$refs.xTable.openExport()
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
          // console.log(params);return
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
        // pageApi.exportExcel(params).then(res=>{

        // })
      },
      insertEvent () {
        let obj = {}
        this.tableDataDetailArr.forEach(item=>{
          obj[item.fieldEn] = ''
        })
        obj.flag = true;
        const record = JSON.parse(JSON.stringify(obj));
        // const record = {flag:true}
        this.$nextTick(()=>{
          let { row: newRow } = this.$refs.xTable.insertAt(record, -1);
          this.$refs.xTable.setActiveCell(newRow);
        })
        // this.$refs.xTable.insert(record).then(({ row }) => {
        //   this.$refs.xTable.setActiveCell(-1, 'sex')
        //   this.$refs.xTable.setActiveRow(row)
        // })
      },
      insertEventFirst (data) {
        let obj = {}
        this.tableDataDetailArr.forEach(item=>{
          obj[item.fieldEn] = data[item.fieldEn] || ''
        })
        obj.flag = true;
        obj.more = true;
        const record = JSON.parse(JSON.stringify(obj));
        // const record = {flag:true}
        // console.log(record);
        this.$nextTick(()=>{
          let { row: newRow } = this.$refs.xTable.insertAt(record,null);
          this.$refs.xTable.setActiveCell(newRow);
        })
      },
      removeEvent () {
          const selectRecords = this.$refs.xTable.getCheckboxRecords()
          if (selectRecords.length) {
             this.$confirm('您确定要删除选中的数据吗?','提示',{
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
              }).then(() => {
                  this.$refs.xTable.removeCheckboxRow()
              }).catch(() => {
                this.$message.closeAll();
              this.$message({
                type: 'info',
                message: '已取消'
              });
              
          })
            
          } else {
            this.$message.closeAll();
            this.$message({type: 'error',message: '请至少选择一条数据'});
          }
      },
      save(){
       let data = this.$refs.xTable.getTableData().tableData;
       
       let tableDataDetailArr = this.tableDataDetailArr;
       let arr = [];
       for(let i = 0;i<tableDataDetailArr.length;i++){
         for(let j=0;j<data.length;j++){
           if(data[j][tableDataDetailArr[i]['fieldEn']]) {
             arr.push(data[j])
           }
         }
       }
       let validArr = Array.from(new Set(arr));
      //  console.log('validArr',validArr);
       this.validEvent(validArr);
     },
      async validEvent (validArr) {
        const $table = this.$refs.xTable
        const errMap = await $table.validate(validArr).catch(errMap => errMap)
        if (errMap) {
          this.$message({type: 'error',message: '校验不通过'});
        } else {
          // this.$message({type: 'success',message: '校验通过'});
          // return
          let Recordset = this.$refs.xTable.getRecordset();
          let insertRecords = Recordset.insertRecords;
          let removeRecords = Recordset.removeRecords;
          let updateRecords = Recordset.updateRecords;
          // console.log('新增',insertRecords);
          // console.log('删除',removeRecords);
          // console.log('修改',updateRecords);
          let tableDataDetailArr = this.tableDataDetailArr;
          let arr1 = [];
          for(let i = 0;i<tableDataDetailArr.length;i++){
            for(let j=0;j<insertRecords.length;j++){
              if(insertRecords[j][tableDataDetailArr[i]['fieldEn']]) {
                arr1.push(insertRecords[j])
              }
            }
          }
          let insertRecords1 = Array.from(new Set(arr1));
          // console.log('insertRecords1',insertRecords1);
          insertRecords1.forEach(item=>{
            item.tableCode = this.activeName;
            item.reportCode = this.reportCode;
            // item.idid = commonFun.getUUID('id');
            if(this.currencyReportPageData){
              let currencyReportPageData = this.currencyReportPageData;
              for(var p in currencyReportPageData){
                item[p] = currencyReportPageData[p];
              }
            }
          })
          removeRecords.forEach(item=>{
            item.tableCode = this.activeName;
            item.reportCode = this.reportCode;
            if(this.currencyReportPageData){
              let currencyReportPageData = this.currencyReportPageData;
              for(var p in currencyReportPageData){
                item[p] = currencyReportPageData[p];
              }
            }
          })
          updateRecords.forEach(item=>{
            item.tableCode = this.activeName;
            item.reportCode = this.reportCode;
            if(this.currencyReportPageData){
              let currencyReportPageData = this.currencyReportPageData;
              for(var p in currencyReportPageData){
                item[p] = currencyReportPageData[p];
              }
            }
          })
          let obj = {}
          obj.insertRecords=insertRecords1;
          obj.removeRecords=removeRecords;
          obj.updateRecords=updateRecords;
          // console.log(obj);return
          if(insertRecords1.length || removeRecords.length || updateRecords.length){
            this.editOnPage(obj);
          }else{
            this.$message({message: '未做任何改动！'});
          }
        }
      },
      editOnPage(params){
        pageApi.editOnPage(params).then((res)=>{
          if(res.data.status===200){
            this.$message({type: 'success',message: '保存成功！'});
            this.onSubmit(true);
            this.getHDdata();
          }else{
            this.$message({type: 'error',message: res.data.message || '保存失败！'});
          }
        })
      },
     currencyInit (data) {
      //  this.currencyReportPageData = data
       if(!this.currencyReportPageData){
          let path = this.$route.fullPath;
          let formData = path.split(":")[1];
          if(formData.indexOf('&') !=-1){
              let arr = formData.split('&');
              let params = {};
              for(let i=0;i<arr.length;i++){
                  let a = arr[i].split("=");
                  params[a[0]] = a[1];
              }
              this.pathSearchData = params;
          }else{
            this.reportCode = formData.split("=")[1];
          }
       }
      this.getTabData();
     },
      handleClick(tab, event) {
        //debugger;
        let name = this.activeName;
        let arr = this.tabArr;
        for(let i=0;i<arr.length;i++){
            if(arr[i].tableCode == name){
                this.isPage = arr[i].isPage;
                if(arr[i].crudEnable){
                     this.crudEnable = arr[i].crudEnable;
                }else{
                    this.crudEnable = '-1'
                }
               
            }
        }
         this.isSearchSelect = 0;
         this.searchDataArr = [];
         this.formInline.pageSize =50;
         this.formInline.pageNum = 1;
         this.onSubmit(true);
         this.getHDdata();
      },
      //分页
    Pagination(val){
       this.formInline.pageSize = val.limit;//页面条数
       this.formInline.pageNum = val.page;//页面
       this.onSubmit(false);
       this.getHDdata();
    },
      toolbarCustomEvent (params) {
        let self = this;
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
      checkColumnMethod ({ column }) {
       
        if (this.showTitle>0) {
         
          //column.visible = false;
          
        }
        this.showTitle = this.showTitle +1;
        return true;
      },
      onSubmit(flag,type){
          this.tableLoading = true;
         // 消除没有值的参数
         if(flag){
             this.formInline.pageNum = 1;
         }
         this.tableShow = false;
         this.formInline.tableCode = this.activeName;
        
         let params = commonFun.parameterSrc(this.formInline);
           params.reportCode = this.reportCode;
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
          if(this.isPage!=1){
              params.pageSize = '';
               params.pageNum = '';
          }
          params = commonFun.parameterSrc(params);
         pageApi.getDataTableNameList(params).then(response => { 
            if(response.data.status === 200 && response.data.data &&response.data.data.length>0){ 
              // this.getHDdata();
               let data = response.data.data[0];
               if(data.fieldsInfo && data.fieldsInfo.length>0){
                
                //  this.tableDataDetailArr = this.getAllPrpos(data.fieldsInfo);
                let arr = data.fieldsInfo.filter(item=>{
                  return item.isCrud&&item.isCrud.indexOf('R')!=-1
                });
                 this.tableDataDetailArr = arr;
                 this.getAllPrpos(data.fieldsInfo);
                  // console.log('tableDataDetailArr',this.tableDataDetailArr);
              }
              if(this.isPage==1){
                this.tableData = this.toStringValue(data.dataList.list); 
                this.tableData.forEach(item=>{
                  this.tableDataDetailArr.forEach(ite=>{
                    if(!item[ite.fieldEn]){
                      item[ite.fieldEn] = ''
                    }
                  })
                })
               }else{
                  this.tableData = this.toStringValue(data.dataList); 
                  this.tableData.forEach(item=>{
                    this.tableDataDetailArr.forEach(ite=>{
                      if(!item[ite.fieldEn]){
                        item[ite.fieldEn] = ''
                      }
                    })
                  })
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
                    return item.isCrud&&item.isCrud.indexOf('M')!=-1
                  })
                  this.searchDataArr = searcharr;

                }
                this.tableShow = true;
                this.getLackLine();
                if(this.HDdata.length){
                  this.getMoreLine(this.HDdata);
                }
                if(this.crudEnable.indexOf('C')!=-1 && this.tableData.length){
                  for(let i = 0;i<3;i++){
                      // tableData.push({})
                    this.insertEvent()
                  }
                }
             } 
             else{ 
                this.tableData = []; 
                this.total = 0; 
                this.formInline.pageSize = 50; 
                this.formInline.pageNum = 1; 
            } 
                this.tableLoading = false; 
            }).catch((err) => { 
                this.tableData = []; 
                this.total = 0; 
                this.formInline.pageSize = 50;
                this.formInline.pageNum = 1;
                this.tableLoading = false;
                console.log(err);
      })
      },
      // table批量选择结果
      restForm(formName) {
        var self = this;
        //self.refs[formName].resetFields();
        this.formInline.reportName = '';
      },
      addData(){
          let arr = [];
          let fieldsInfoArr = this.fieldsInfoArr;
          let params = {};
          this.countRules = {};
          for(let i=0;i<fieldsInfoArr.length;i++){
              if(fieldsInfoArr[i].isCrud && fieldsInfoArr[i].isCrud.indexOf('C')!=-1){
                arr.push(fieldsInfoArr[i]);  
                params[fieldsInfoArr[i].fieldEn] = '';
              }
              if(fieldsInfoArr[i].isRequired && fieldsInfoArr[i].isRequired ==1){
                  let rulesParams={}
                  rulesParams.required=true;
                  rulesParams.message="请输入"+fieldsInfoArr[i].fieldCn;
                  rulesParams.trigger = 'change';
                   rulesParams.type = 'string';
                  let rulesArr= [];
                  rulesArr.push(rulesParams);
                  this.countRules[fieldsInfoArr[i].fieldEn] = rulesArr;
              }
          }
          this.addDataArr = arr;
          this.operationType = 1;
          this.formCount = params;
          this.countTitle='新增'
           this.isSearchDetail = false;
          this.countDialog = true;

      },
      editData(row,flag){
         let arr = [];
          let fieldsInfoArr = this.fieldsInfoArr;
          let params = {};
          this.countRules = {};
          for(let i=0;i<fieldsInfoArr.length;i++){
              if(fieldsInfoArr[i].isCrud && fieldsInfoArr[i].isCrud.indexOf('U')!=-1){
                arr.push(fieldsInfoArr[i]);  
               
              }
              if(fieldsInfoArr[i].isCrud && fieldsInfoArr[i].isCrud.indexOf('U')!=-1&&fieldsInfoArr[i].isRequired && fieldsInfoArr[i].isRequired ==1){
                  let rulesParams={}
                  rulesParams.required=true;
                  rulesParams.message="请输入"+fieldsInfoArr[i].fieldCn;
                  rulesParams.trigger = 'change';
                   rulesParams.type = 'string';
                  let rulesArr= [];
                  rulesArr.push(rulesParams);
                  this.countRules[fieldsInfoArr[i].fieldEn] = rulesArr;
              }
          }
          // console.log(this.countRules);
          if(row){
            for(var p in row){
              params[p] = row[p]
           }
          }
          this.addDataArr = arr;
          this.operationType = 2;
          this.formCount = params;
        
          
          if(flag){
              this.countTitle='查看详情'
              this.isSearchDetail = true;
          }else{
            this.countTitle='修改'
             this.isSearchDetail = false;
          }
          this.countDialog = true;
          
      },
      delData(row){
          this.$confirm('确定删除?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        .then(() => {
            let params = {};
             if(row){
                for(var p in row){
                  params[p] = row[p]
                }
              }
            params.tableCode = this.activeName;
            params.reportCode = this.reportCode;
            if(this.currencyReportPageData){
                let currencyReportPageData = this.currencyReportPageData;
      
                for(var p in currencyReportPageData){
                    params[p] = currencyReportPageData[p];
                }
            }
             
            pageApi.deleteDataSource(params).then(response => {
            if(response.data.status === 200){
               // 关闭移动指标弹框
              
                this.$message.closeAll()
                this.$message({
                    message: '删除成功',
                    type: 'success'
                });
               // 刷新列表
               this.onSubmit(false);
            }
            else{
                // 关闭移动指标弹框
                //this.countDialog = false;
                this.$message.closeAll()
                this.$message({
                  message: response.data.message || '删除失败',
                  type: 'warning'
                });
            }
              
           }).catch(() => {
               // 关闭移动指标弹框
            
              this.$message.closeAll()
              this.$message({
                 message: '删除失败',
                 type: 'warning'
             });
         })
       })
       .catch(() => {
        
        });
      },
     getAllPrpos(formData) {
          // 用来保存所有的属性名称和值
         
          let arr =  [];
          let params = {};
          let searchForms = [];
          let checkAllForms = [];
          let combineds = [];
          for(let i=0;i<formData.length;i++){
              //获取列表，表头
              if(formData[i].isCrud && formData[i].isCrud.indexOf('R')!=-1){
                  let data = {};
                 
                  data[formData[i].fieldEn] = formData[i].fieldCn;
                  // 开始遍历
                  for(var p in data){
                      let params = {};
                      // 方法
                      // p 为属性名称，obj[p]为对应属性的值
                      params.code = ''+p;
                      params.name = data[p];
                      params.flag = true;
                      if(params.code!='VC_ELEMENT_ID'){
                        arr.push(params);
                      }
                      
                  }

              }
              //获取查询条件
              if(formData[i].isCrud && formData[i].isCrud.indexOf('F')!=-1){
                   //弹框多选遍历数组
                  searchForms.push(formData[i]);
                  //弹框全选内容
                  checkAllForms.push(formData[i].fieldEn);
                 
              }
              //获取下拉框内容
              if(formData[i].dicSql &&  this.isSearchSelect==0){
                  params[formData[i].fieldEn] = ''+formData[i].fieldEn;
                  this.getSelectData(formData[i].fieldEn);
              }
              // 获取表尾合计字段
              if(formData[i].isCrud && formData[i].isCrud.indexOf('H')!=-1){
                combineds.push(formData[i].fieldEn);
              }
               
          }
          this.combineds = combineds;
          this.searchForms = searchForms;
          let checkedForms = [];
          if(searchForms.length){
            // checkedForms.push(searchForms[0].fieldEn)
          }
          this.checkedForms = checkedForms;
          this.checkAllForms = checkAllForms;
          this.isSearchSelect =   this.isSearchSelect +1;
          // this.searchSubmit()
          // return arr;
          
      },
      //获取tab数据
      getTabData(){
          let params = {};
          params.reportCode = this.reportCode;
          if(this.currencyReportPageData){
                let currencyReportPageData = this.currencyReportPageData;
      
                for(var p in currencyReportPageData){
                    params[p] = currencyReportPageData[p];
                }
            }
            if(this.pathSearchData){
              let data = this.pathSearchData;
            
            for(var p in data){
                params[p] = data[p];
            }
          }
          pageApi.getTabData(params).then(response => {
              if(response.data.status === 200){
                // 关闭移动指标弹框
                let arr =  response.data.data;
                if(arr && arr.length>0){
                   this.tabArr = arr;
                   this.activeName = arr[0].tableCode;
                   this.isPage = arr[0].isPage;
                   if(arr[0].crudEnable){
                     this.crudEnable = arr[0].crudEnable;
                    }else{
                        this.crudEnable = '-1'
                    }
                  
                  this.onSubmit(true,"mounted");
                  this.getHDdata();
                  
                }else{
                  this.tabArr = [];
                }
               

              }
              else{
                this.$message.closeAll()
                this.$message({
                  message: response.data.message || '数据初始化失败',
                  type: 'warning'
                });
              }
              
            }).catch(() => {
                this.$message.closeAll()
                this.$message({
                  message: response.data.message || '数据初始化失败',
                  type: 'warning'
                });

            })
      },
      getHDdata(){
        if(this.currencyReportPageData){
          let params = {
            recordId:this.currencyReportPageData.recordId,
            tableCode:this.activeName,
            // verifyStatus:'0',
            pageSize:9999,
            pageNum:1
          }
          this.HDdata = [];
          xbrlApi.geVerifyDetail(params).then(res=>{
            if(res.data.status===200 && res.data.data){
              let data = res.data.data.list || []
              this.HDdata = data;
              this.getLackLine();  //获取平台有，外包无
              if(this.tableShow){
                this.getMoreLine(data);  //获取外包有，平台无
              }
              // if(!this.HDdata.length){
              //   this.HDdata = [
              //     {lineName:"1",columnName:"1",elementValueImp:"核对不一致",verifyStatus:"0"},
              //     {lineName:"1",columnName:"2",elementValueImp:"核对一致",verifyStatus:"1"},
              //     {lineName:"2",columnName:"1",elementValueImp:"核对不一致",verifyStatus:"0"},
              //     {lineName:"2",columnName:"2",elementValueImp:"核对一致",verifyStatus:"1"},
              //     {lineName:"2",columnName:"3",elementValueImp:"核对不一致",verifyStatus:"0"},
              //     {lineName:"2",columnName:"4",elementValueImp:"核对不一致",verifyStatus:"0"},
              //   ]
              // }
            }else{
              this.HDdata = [];
            }
          })
        }
      },
      getLackLine(){
        if(!this.HDdata.length) return
        let arr = [];
        this.HDdata.forEach(item=>{
          if(item.lineName && item.lineIndexImp){
            if(!arr.includes(item.lineName)){
              arr.push(item.lineName)
            }
          }
        })
        let total = 0;
        let tableDataLine = [] 
        if(this.isPage){
          total = this.total;
          for (let i = 0; i < total; i++) {
            if(!arr.includes(i+1+'')){
              tableDataLine.push(i+1+'')
            }
          }
          this.LackLine = tableDataLine;
        }else{
          total = this.tableData.length;
          for (let i = 0; i < total; i++) {
            if(!arr.includes(i+1+'')){
              tableDataLine.push(i+1+'')
            }
          }
          this.LackLine = tableDataLine;
        }
        // console.log('tableDataLine',tableDataLine);
        // this.$nextTick(()=>{
        //   this.$refs.xTable.updateData();
        // })
      },
      getMoreLine(val){
        // lineIndexImp
        if(!val.length) return
        if(!this.tableShow) return
        let arr = [];
        let data = val.filter(item=>{
          if(item.lineIndexImp && !item.lineName && (item.lineIndexImp != item.lineName)){
            if(!arr.includes(item.lineIndexImp)){
              arr.push(item.lineIndexImp)
            }
          }
          return item.lineIndexImp && !item.lineName && (item.lineIndexImp != item.lineName)
        })
        // console.log(arr);
        let list = [];
        if(data){
          arr.forEach(item=>{
            let obj = {}
            data.forEach(ite=>{
              if(item == ite.lineIndexImp){
                obj[ite.fieldEn] = ite.elementValueImp || ''
              }
            })
            list.push(obj)
          })
        }
        // console.log('list',list);
        this.moreLineList = list;
        list.forEach(item=>{
          this.insertEventFirst(item)
        })
        
      },
       //新增,编辑确认
     countSubmit(formName){
         this.$refs['formCount'].validate((valid) => {
             if (valid) {
                this.$message.closeAll()
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
        })
     },
      saveData(){
          this.$confirm('确定新增?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        .then(() => {
            let params = {};
            params = commonFun.parameterSrc(this.formCount);
            params.tableCode = this.activeName;
            params.reportCode = this.reportCode;
            this.countSubmit_btn = true;
            if(this.currencyReportPageData){
                let currencyReportPageData = this.currencyReportPageData;
      
                for(var p in currencyReportPageData){
                    params[p] = currencyReportPageData[p];
                }
            }
             if(this.pathSearchData){
              let data = this.pathSearchData;
            
            for(var p in data){
                params[p] = data[p];
            }
          }
            pageApi.addDataSource(params).then(response => {
            if(response.data.status === 200){
               // 关闭移动指标弹框
                this.countDialog = false;
                this.$message.closeAll()
                this.$message({
                    message: '新增成功',
                    type: 'success'
                });
               // 刷新列表
               this.onSubmit(true);
            }
            else{
                // 关闭移动指标弹框
               // this.countDialog = false;
                this.$message.closeAll()
                this.$message({
                  message: response.data.message || '新增失败',
                  type: 'warning'
                });
            }
               this.countSubmit_btn = false;
           }).catch(() => {
               // 关闭移动指标弹框
              //this.countDialog = false;
              this.countSubmit_btn = false;
              this.$message.closeAll()
              this.$message({
                 message: '新增失败',
                 type: 'warning'
             });
         })
       })
       .catch(() => {
          // 关闭移动指标弹框
         // this.countDialog = false;
          this.countSubmit_btn = false;
        });
    },
   updateParamSet(){
       this.$confirm('确定修改?', '提示', {
       confirmButtonText: '确定',
       cancelButtonText: '取消',
       type: 'warning'
       })
       .then(() => {
           let params = {};
           params = this.formCount;
           this.countSubmit_btn = true;
          params.tableCode = this.activeName;
          params.reportCode = this.reportCode;
          if(this.currencyReportPageData){
                let currencyReportPageData = this.currencyReportPageData;
      
                for(var p in currencyReportPageData){
                    params[p] = currencyReportPageData[p];
                }
            }
            // console.log(this.currencyReportPageData);
           pageApi.updateDataSource(params).then(response => {
               if(response.data.status === 200){
                  // 关闭移动指标弹框 
                 this.countDialog = false;
                 this.$message.closeAll()
                 this.$message({
                    message: '修改成功',
                    type: 'success'
                 });
                 // 刷新树列表
                 this.onSubmit(false);
            }
             else{
                 // 关闭移动指标弹框
                // this.countDialog = false;
                 this.$message.closeAll()
                 this.$message({
                     message: response.data.message || '修改失败',
                     type: 'warning'
                 });
             }
               this.countSubmit_btn = false;
           }).catch(() => {
              // 关闭移动指标弹框
              // this.countDialog = false;
               this.countSubmit_btn = false;
               this.$message.closeAll()
               this.$message({
                  message: '修改失败',
                  type: 'warning'
                });
           })
        })
         .catch(() => {
           // 关闭移动指标弹框
           // this.countDialog = false;
             this.countSubmit_btn = false;
        });
      },
      //获取下拉框内容
      getSelectData(val){
          let params = {};
          params.fieldEn = val;
          params.tableCode = this.activeName;
          params.reportCode = this.reportCode;
        
          if(this.currencyReportPageData){
                let currencyReportPageData = this.currencyReportPageData;
      
                for(var p in currencyReportPageData){
                    params[p] = currencyReportPageData[p];
                }
            }
             if(this.pathSearchData){
              let data = this.pathSearchData;
            
            for(var p in data){
                params[p] = data[p];
            }
          }
           pageApi.getSelectData(params).then(response => {
               if(response.data.status === 200){
                  // 关闭移动指标弹框 
                  // this.formSelectArr[val] = response.data.data;
                  // 解决数据改变，视图不变
                  this.$set(this.formSelectArr,val,response.data.data)
               }
             else{
               
                 this.$message.closeAll()
                 this.$message({
                     message: response.data.message || '获取下拉内容失败',
                     type: 'warning'
                 });
             }
               
           }).catch(() => {
              // 关闭移动指标弹框
              
               this.$message.closeAll()
               this.$message({
                  message: '获取下拉内容失败',
                  type: 'warning'
                });
           })
      },
      //查询条件选择
      searchSubmit(){
          // console.log(this.checkedForms);

          let arr = [];
          let fieldsInfoArr = this.fieldsInfoArr;
          let params = {};
          let checkedForms = this.checkedForms;
          if(checkedForms &&checkedForms.length>0){
              for(let i=0;i<checkedForms.length;i++){
                  for(let j=0;j<fieldsInfoArr.length;j++){
                      if(fieldsInfoArr[j].fieldEn == checkedForms[i]){
                        arr.push(fieldsInfoArr[j]);  
                        params[fieldsInfoArr[j].fieldEn] = '';
                      }
              
                  }
              }
              params['pageSize'] = this.formInline.pageSize;
              params['pageNum'] = this.formInline.pageNum;
              this.searchDataArr = arr;
              // console.log('searchDataArr',arr);
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
        this.isIndeterminate = checkedCount > 0 && checkedCount < this.checkAllForms.length;
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
    // 添加条件
    addSearchList(){
      this.searchDialog = true;
      let arr = this.searchDataArr.map(item=>{
        return item.fieldEn
      })
      this.checkedForms = arr;
    },

    activeCellMethod({row, column, columnIndex }){
      // console.log( column.property);
      // console.log(row);
      if(row.flag) return true
      let aa = true;
      this.tableDataDetailArr.forEach(item=>{
        if(item.fieldEn==column.property){
          if(item.isCrud.indexOf('U')==-1){
            aa = false
          }
        }
      })
      return aa
    },
    // 与外包核对
    cellStyle({ row, rowIndex, column, columnIndex }){
      // this.formInline.pageSize = val.limit;//页面条数
      //  this.formInline.pageNum = val.page;//页面
      // console.log(rowIndex);
      if(this.isPage){
        let pageSize = this.formInline.pageSize;
        let pageNum = this.formInline.pageNum;
        let HDdata = this.HDdata;
        let tableData = this.tableData;
        let num = pageSize*(pageNum-1);
        if(this.crudEnable.indexOf('D')!=-1){
          for(let i=0;i<HDdata.length;i++){
            if(HDdata[i].verifyStatus=='0' && HDdata[i].lineIndex && HDdata[i].lineIndexImp){
              let xy = {
                x:HDdata[i].lineName-1-num,
                y:HDdata[i].columnName-1
              }
              if(rowIndex!=-1 && rowIndex==xy.x && columnIndex-1==xy.y){
                // row[column.property+'_title'] = HDdata[i].elementValueImp || ''
                return {
                  backgroundColor: "#6cdeff",
                  color: "rgb(255, 0, 0)",
                };
              }
            }
          }
        }else{
          for(let i=0;i<HDdata.length;i++){
            if(HDdata[i].verifyStatus=='0' && HDdata[i].lineIndex && HDdata[i].lineIndexImp){
              let xy = {
                x:HDdata[i].lineName-1-num,
                y:HDdata[i].columnName-1
              }
              if(rowIndex!=-1 && rowIndex==xy.x && columnIndex==xy.y){
                return {
                  backgroundColor: "#6cdeff",
                  color: "rgb(255, 0, 0)",
                };
              }
            }
          }
          
        }
        for(let i = 0;i<this.LackLine.length;i++){
          if(rowIndex!=-1 && rowIndex == this.LackLine[i]-1-num){
            return {
              backgroundColor: "#c4c4c4",
              color: "rgb(255, 0, 0)",
            };
          }
        }
      }else{
        let HDdata = this.HDdata;
        let tableData = this.tableData;
        if(this.crudEnable.indexOf('D')!=-1){
          for(let i=0;i<HDdata.length;i++){
            if(HDdata[i].verifyStatus=='0'  && HDdata[i].lineIndex && HDdata[i].lineIndexImp){
              let xy = {
                x:HDdata[i].lineName-1,
                y:HDdata[i].columnName-1
              }
              if(rowIndex!=-1 && rowIndex==xy.x && columnIndex-1==xy.y){
                // row[column.property+'_title'] = HDdata[i].elementValueImp || ''
                return {
                  backgroundColor: "#6cdeff",
                  color: "rgb(255, 0, 0)",
                };
              }
            }
          }
        }else{
          for(let i=0;i<HDdata.length;i++){
            if(HDdata[i].verifyStatus=='0'  && HDdata[i].lineIndex && HDdata[i].lineIndexImp){
              let xy = {
                x:HDdata[i].lineName-1,
                y:HDdata[i].columnName-1
              }
              if(rowIndex!=-1 && rowIndex==xy.x && columnIndex==xy.y){
                return {
                  backgroundColor: "#6cdeff",
                  color: "rgb(255, 0, 0)",
                };
              }
            }
          }
        }
        for(let i = 0;i<this.LackLine.length;i++){
          if(rowIndex!=-1 && rowIndex == this.LackLine[i]-1){
            return {
              backgroundColor: "#c4c4c4",
              color: "rgb(255, 0, 0)",
            };
          }
        }
      }
      if(row.more){
        return {
          backgroundColor: "#0188fb",
          color: "rgb(255, 0, 0)",
        };
      }
    },
    showTooltipMethod ({ row, rowIndex, column, columnIndex }) {
      if(this.isPage){
        let pageSize = this.formInline.pageSize;
        let pageNum = this.formInline.pageNum;
        let HDdata = this.HDdata;
        let tableData = this.tableData;
        let num = pageSize*(pageNum-1);
        if(this.crudEnable.indexOf('D')!=-1){
          for(let i=0;i<HDdata.length;i++){
            if(HDdata[i].verifyStatus=='0' && HDdata[i].lineIndex && HDdata[i].lineIndexImp){
              let xy = {
                x:HDdata[i].lineName-1-num,
                y:HDdata[i].columnName-1
              }
              if(rowIndex!=-1 && rowIndex==xy.x && columnIndex-1==xy.y){
                return '外包值: '+(HDdata[i].elementValueImp || '')
              }
            }
          }
          return ''
        }else{
          for(let i=0;i<HDdata.length;i++){
            if(HDdata[i].verifyStatus=='0' && HDdata[i].lineIndex && HDdata[i].lineIndexImp){
              let xy = {
                x:HDdata[i].lineName-1-num,
                y:HDdata[i].columnName-1
              }
              if(rowIndex!=-1 && rowIndex==xy.x && columnIndex==xy.y){
                return '外包值: '+(HDdata[i].elementValueImp || '')
              }
            }
          }
          return ''
        }
      }else{
        let HDdata = this.HDdata;
        let tableData = this.tableData;
        if(this.crudEnable.indexOf('D')!=-1){
          for(let i=0;i<HDdata.length;i++){
            if(HDdata[i].verifyStatus=='0' && HDdata[i].lineIndex && HDdata[i].lineIndexImp){
              let xy = {
                x:HDdata[i].lineName-1,
                y:HDdata[i].columnName-1
              }
              if(rowIndex!=-1 && rowIndex==xy.x && columnIndex-1==xy.y){
                return '外包值: '+(HDdata[i].elementValueImp || '')
              }
            }
          }
          return ''
        }else{
          for(let i=0;i<HDdata.length;i++){
            if(HDdata[i].verifyStatus=='0' && HDdata[i].lineIndex && HDdata[i].lineIndexImp){
              let xy = {
                x:HDdata[i].lineName-1,
                y:HDdata[i].columnName-1
              }
              if(rowIndex!=-1 && rowIndex==xy.x && columnIndex==xy.y){
                return '外包值: '+(HDdata[i].elementValueImp || '')
              }
            }
          }
          return ''
        }
      }
    },
    editActived({ row, rowIndex, column, columnIndex }){
      console.log(row);
      console.log(rowIndex);
    },
    // 表尾合计
    footerMethod ({ columns, data }) {
      // console.log('表尾合计',data);
      let data1 = data.filter(item=>{
        return !item.more
      })
      let combineds = this.combineds;
      if(combineds.length===0 || this.HDdata.length===0){
        return []
      }
      return [
        columns.map((column, columnIndex) => {
          if (columnIndex === 0) {
            return '系统值汇总'
          }
          if (combineds.includes(column.property)) {
            return XEUtils.sum(data1, column.property)
          }
          return null
        }),
        columns.map((column, columnIndex) => {
          if (columnIndex === 0) {
            return '外包值汇总'
          }
          if (combineds.includes(column.property)) {
            
            // let obj = this.tableDataDetailArr.find(item=>{
            //   return item.fieldEn == column.property
            // })

            // console.log(obj);
            // if(obj){
              let num = 0;
              // let fieldCn = obj.fieldCn;
              let HDdata = this.HDdata;
              if(this.isPage){
                let pageSize = this.formInline.pageSize;
                let pageNum = this.formInline.pageNum;
                HDdata = this.HDdata.filter(item=>{
                  return item.lineName>pageSize*(pageNum-1) && item.lineName<=pageSize*pageNum
                })
              }
              HDdata.forEach(item=>{
                // console.log(item.elementName,fieldCn);
                if(item.fieldEn==column.property){
                  // console.log(item.elementName,item.elementValueImp);
                  num = num + (item.elementValueImp-0 || 0)
                  // console.log(num);
                }
              })
              return num || ''
            // }
          }
          return null
        }),
      ]
    },
    
    
      
   }
}
</script>
<style lang='css' scoped>
.mytable-style .vxe-body--row.row-green {
  background-color: #187;
  color: #fff;
}
</style>

<style lang='scss'>
.currencyReportWidth{
  width: 55% !important;
}
.vxe-dropdown--panel {
  z-index: 2010 !important
}
/* 日期框 */
.vxe-input--panel.type--date, .vxe-input--panel.type--month, .vxe-input--panel.type--            week, .vxe-input--panel.type--year {
  z-index: 9998 !important
}
  /* 选择框 */
.vxe-select--panel {
  z-index: 9997 !important
}

.currency_report{
        /*滚动条整体部分*/
        .mytable-scrollbar ::-webkit-scrollbar {
          width: 10px;
          height: 10px;
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

<style lang="scss" scoped>
.zhaiyao_tuli {
  margin-left: 20px;
    display: flex;
    margin-top: 6px;
    .zhaiyao_tuli_item {
      color: #303133;
      margin-left: 10px;
      display: flex;
      .box {
        width: 40px;
        border-radius: 4px;
        margin-left: 4px;
        height: 20px;
        position: relative;
        top: 9px;
      }
    }
  }
  .color1 {
    background-color: #c4c4c4;
  }
  .color2 {
    background-color: #6cdeff;
  }
  .color3 {
    background-color: #0188fb;
  }
</style>

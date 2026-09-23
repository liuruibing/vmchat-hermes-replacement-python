<template>
  <div>
  <div class="toolbar" >
     <el-form :inline="true" ref = "formInline" :model="formInline"  class="demo-form-inline form_inline_search" >
          <el-row>
            <el-col :span="16">
              <div class="grid-content bg-purple">
               <el-form-item label="产品代码" prop="fundCode">
                  <el-input
                    v-model="formInline.fundCode"
                    placeholder="产品代码"
                    type="text"
                    auto-complete="off"
                    size="small"/>
                </el-form-item>

               <el-form-item label="产品名称" prop="fundName">
                  <el-input
                    v-model="formInline.fundName"
                    placeholder="产品名称"
                    type="text"
                    auto-complete="off"
                    size="small"/>
                </el-form-item>
              </div>

            </el-col>
            <el-col :span="8">
              <div class="grid-content bg-purple-light">
                <el-form-item  class="search_button_com">
                  <el-button type="primary" @click="onSubmit('formInline')" style="margin-bottom: 5px;" :disabled = "investmentSearch1"  size="small">查询</el-button>
                  <el-button type="primary" plain size="small" style="margin-bottom: 5px;" @click="resetForm('formInline')"><i class='el-icon-delete'></i>重置</el-button>
                </el-form-item>
              </div>
            </el-col>
          </el-row>
        </el-form>
  </div>

    <el-table
      :data="myData.datas"
      stripe
      height="360"
      style="width: 100%"
      v-loading="investLoading && $store.state.setting.loadingShow"
      @sort-change="investmentComDataChangeSort"
      :default-sort = "{prop: 'dMettingdate', order: 'descending'}">

      <el-table-column
        type="index"
        label="序号"
        fixed
        align = "center"
        width="50">
      </el-table-column>
      <el-table-column
        prop="fundCode"
        label="产品代码"
        :sort-orders="['ascending', 'descending']"
        min-width="90"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.fundCode | noDataFilter}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fundName"
        label="产品名称"
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.fundName | noDataFilter}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fundCategory"
        label="产品类别"
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{initEdimExt(scope.row.fundCategory,'fundCategory') | noDataFilter}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fundType"
        label="产品类型"
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{initEdimExt(scope.row.fundType,'fund_fundType') | noDataFilter}}</span>
        </template>
      </el-table-column>

      <el-table-column
          label="操作"
          min-width = "120"
          fixed="right"
          align="center">
          <template slot-scope="scope">
            <el-button  plain type="text" size="mini"  @click="serachDetail(scope.row)">查看详情</el-button>
          </template>
      </el-table-column>
    </el-table>
    <div style="width:100%;height:20px;">
          <Pagination :total="total" :page="pageNumber" :limit = "pageSize" @pagination = "Pagination"></Pagination>
     </div>

    <el-dialog
       title="产品详情"
      :visible.sync="dialogVisible"
       width="65%"
      :before-close="handleClose" >
          <el-form :inline="true" label-width="120px" label-position="left" ref = "formDetail" :model="formDetail"  class="demo-form-inline form_inline_search" style="margin-top: 8px;margin-bottom: 10px;margin-left:80px">

                <el-form-item label="产品名称" prop="fundName">
                    <el-input
                      v-model="formDetail.fundName"
                      placeholder="产品名称"
                      type="text"
                      disabled
                      auto-complete="off"
                      class="el_form_item"/>
                </el-form-item>

                <el-form-item label="产品代码" prop="fundCode">
                    <el-input
                      v-model="formDetail.fundCode"
                      placeholder="产品代码"
                      type="text"
                      disabled
                      auto-complete="off"
                      class="el_form_item"/>
              </el-form-item>

              <el-form-item label="产品类型" prop="fundType">
                <el-select disabled  v-model="formDetail.fundType" placeholder="请选择" class="el_form_item">
                  <el-option
                        v-for="item in fundTypes"
                      :key="item.id"
                      :label="item.dimNme"
                      :value="item.dimCde">
                  </el-option>
                </el-select>
              </el-form-item>

              <el-form-item label="产品类别" prop="fundCategory">
                <el-select  disabled v-model="formDetail.fundCategory" placeholder="请选择" class="el_form_item">
                    <el-option
                        v-for="item in fundTypes2"
                        :key="item.id"
                        :label="item.dimNme"
                        :value="item.dimCde">
                    </el-option>
                  </el-select>
              </el-form-item>

              <el-form-item label="管理人类型" prop="managerType">
                <el-select disabled v-model="formDetail.managerType" placeholder="请选择" class="el_form_item">
                    <el-option
                          v-for="item in managerTypes"
                        :key="item.id"
                        :label="item.dimNme"
                        :value="item.dimCde">
                    </el-option>
                </el-select>
              </el-form-item>

              <el-form-item label="托管人" prop="tgrCode">
                <el-select disabled filterable v-model="formDetail.tgrCode" placeholder="请选择" class="el_form_item">
                    <el-option
                      v-for="item in trustees"
                      :key="item.id"
                      :label="item.dimNme"
                      :value="item.dimCde">
                    </el-option>
                  </el-select>
              </el-form-item>

              <el-form-item label="基金服务机构" prop="serviceCode">
                  <el-select disabled filterable  v-model="formDetail.serviceCode" placeholder="请选择" class="el_form_item">
                        <el-option
                          v-for="item in operateOrgs"
                          :key="item.id"
                          :label="item.dimNme"
                          :value="item.dimCde">
                        </el-option>
                    </el-select>
              </el-form-item>

              <el-form-item  label="是否分级" prop="gradeCode" >
                <el-radio disabled v-model="formDetail.gradeCode" v-for="item in fundGrades2" :key="item.dimCde" :label="item.dimCde">{{item.dimNme}}</el-radio>
              </el-form-item>
              <br>
              <el-form-item label="投资范围" prop="investArea">
                  <div class="product_content">
                    <div class="product_news_box" v-for="item in tzfwData2"><i class="el-icon-tickets"></i> {{item.dimNme}} </div>
                  </div>
              </el-form-item>
     </el-form>
     <span slot="footer" class="dialog-footer">
        <el-button plain  size="small"  @click="dialogVisible = false">取消</el-button>
    </span>
  </el-dialog>

  </div>
</template>

<script>
  import Pagination from '@/components/Pagination'
  import commonApi from '@/api/common'
  import fun from '@/filters/common'
  import hint from '@/components/hint'
  import productApi from '@/api/product/product'

  export default {
    name: 'productIndex',
     components: {Pagination,hint},
    data() {
      return {
        formInline:{
          fundCode:'',//产品代码
          fundName:''//产品名称
        },
        formDetail:{
          fundCode:'',//产品代码
          fundName:'',//产品名称
          fundType:'',//产品类型
          fundCategory:'',//产品类别
          managerType:'',//管理人类型
          raiseAmount:'',//计划募集金额
          investDirect:'',//投资方向
          productStruc:'',//产品结构
          opendayType:'',//开放日类型
          isApplyRedemSame:1,//申购赎回是否相同
          isHasLockupPeriod:1,//是否有封闭期
          lockupDays:'',//锁定期
          applyAddStart:'',//追加认申购起点
          applyAddStartAppend:'',//追加认申购起点Select
          tgrCode:'',//托管人
          serviceCode:'',//基金服务机构
          gradeCode:''//产品分级
        },
        investLoading:false,//列表加载
        investArea:[],// 投资范围
        myData: {datas:[]},//列表数据
        orderByString:'"transferReqdate" desc nulls last',//排序字段
        total:0,//总条数
        pageSize:10,//每页条数
        offset:0,//
        pageNumber:1,//页码
        investmentSearch1:false,//查询禁用
        dialogVisible:false,//弹框
        fundTypes:[],//产品类型
        fundTypes2:[],//产品类别
        managerTypes:[],//管理人类型数组
        trustees:[],//托管人数组
        operateOrgs:[],//基金服务机构数组
        fundGrades:[],
        fundGrades2:[],//是否分级
        productStrucs:[], //产品结构
        opendayTypes:[], //开放日
        sffbq:[{dimCde: 1,dimNme: '是' },{ dimCde: 2, dimNme: '否' } ], //是否有封闭期
        checkAll: false,//全选
        tzfwData:[],//投资范围
        tzfwData2:[],//投资范围
        isIndeterminate:true,
        searchData:{},
        isSubmit: false


      }
    },
    //页面加载后触发
    mounted(){

      //查询产品信息
      this.selectAll();
      //获取产品类型
      this.getSelects('fund_fundType');
      //获取产品类别
      this.getSelects('fund_type');
      //获取管理人类型
      this.getSelects('fund_managerType');
      //获取托管人
      this.getSelects('fund_trustee');
      //基金服务机构
      this.getSelects('fund_operateOrg');
      //获取投资范围
      this.getSelects('fund_investArea');
      //产品分级
      this.getSelects('fund_fundGrade');

    },
    methods: {
      onSubmit(data){
        this.isSubmit = true;
        this.pageNumber = 1;
        this.offset = (this.pageNumber -1) * this.pageSize;
        let formInline = this.formInline;
        this.searchData.fundCode = formInline.fundCode;
        this.searchData.fundName = formInline.fundName;
        this.selectAll('submit');
      },
      // 清除
      resetForm (formName) {
        var self = this;
        self.$refs[formName].resetFields();
      },
      //排序
      investmentComDataChangeSort(val){
        var self = this;
        self.orderByString = self.$fun.orderByString(val);
        self.selectAll();
      },
       //分页
      Pagination(val){
        let self = this;
        self.pageSize = val.limit;
        self.pageNumber = val.page;
        self.offset = (self.pageNumber -1) * self.pageSize;
        self.selectAll('page');
      },
      //查询列表
      selectAll(flag){
          this.investLoading = true;
          //如果已经点击查询按钮,,则数据按照查询按钮的
          let submit = this.isSubmit;
          let data = this.formInline;
          let data2 = this.searchData;
          if(submit){
            data = data2;
          }
         let fundName = data.fundName;
         let fundCode = data.fundCode;
         let orderByString = this.orderByString;
         let limit = this.pageSize;
         let offset = this.offset;
         if(!fundName || !submit){
            fundName = "0";
          }
          if(!fundCode || !submit){
            fundCode = "0";
          }
        productApi.getAll(fundName,fundCode,orderByString,limit,offset).then(res =>{
            let self = this;
            if(res.data.message === "success"){
                this.myData.datas = res.data.data.rows;
                this.pageSize = res.data.data.limit;
                this.total =res.data.data.total;
            }else{
                self.pageSize = 10;
                self.pageNumber = 1;
                self.total = 0;
                self.myData.datas = null;
                this.resetForm();
                this.$message.error('查询列表信息失败');
            }
             this.investLoading = false;
          }).catch(() => {
            this.$message.error('查询列表信息失败');
            this.investLoading = false;
        })
      },
      //查看详情
      serachDetail(val){
        let id = val.id;
        productApi.getDetailById(id).then(res =>{
           let self = this;
           if(res.data.message === "success"){
              this.formDetail = res.data.data;
              this.formDetail.gradeCode =  res.data.data.gradeCode;
                if(res.data.data.fundCategory === 'fundCategory_gmjj'){
                    let arr = [];
                    let fundGradeArr = this.fundGrades;
                    for(let i=0;i<fundGradeArr.length;i++){
                        if(fundGradeArr[i].dimNme !== "结构化分级"){
                            arr.push(fundGradeArr[i]);
                        }
                    }
                    this.fundGrades2 = arr;
                }else if(res.data.data.fundCategory === 'fundCategory_jjzh'){
                    let arr = [];
                    let fundGradeArr = this.fundGrades;
                    for(let i=0;i<fundGradeArr.length;i++){
                      if(fundGradeArr[i].dimNme !== "费用分级"){
                          arr.push(fundGradeArr[i]);
                      }
                    }
                    this.fundGrades2 = arr;
                }else{
                    let arr = [];
                    let fundGradeArr = this.fundGrades;
                      for(let i=0;i<fundGradeArr.length;i++){
                          if(fundGradeArr[i].dimNme === "无分级"){
                              arr.push(fundGradeArr[i]);
                          }

                        }
                    this.fundGrades2 = arr;
               }
              this.dialogVisible = true;
          }else{
              self.$refs['formDetail'].resetFields();
              this.$message.error('查询详情信息失败');
            }
      }).catch(() => {
            this.$message.error('查询详情信息失败');
            self.$refs['formDetail'].resetFields();
      })

    },
    //关闭dialog
    handleClose(done){
        done();
    },
    //获取Selects
    getSelects(val){
      let params = val;
      productApi.getSelects(params).then(res =>{

          let self = this;
          if(res.data.message === "success"){

              if(val === 'fund_fundType'){
                  this.fundTypes = res.data.data;
              }

              if(val === 'fund_type'){
                  this.fundTypes2 = res.data.data;
              }

              if(val === 'fund_managerType'){
                  this.managerTypes = res.data.data;
              }

              if(val === 'fund_trustee'){
                  this.trustees = res.data.data;
              }

              if(val === 'fund_operateOrg'){
                  this.operateOrgs = res.data.data;
              }

              if(val === 'fund_investArea'){
                  this.tzfwData = res.data.data;
                  let arr = [];
                  let len = res.data.data.length > 5 ? 5 : res.data.data.length;
                  for(let i=0;i<len;i++){
                    arr.push(res.data.data[i]);
                  }
                  this.tzfwData2 = arr;
              }

              if(val === 'fund_fundGrade'){
                  this.fundGrades = res.data.data;
                  this.formDetail.fundGrade = res.data.data[0].dimCde
              }

          }else{
            this.$message.error('初始化数据失败');
          }

        }).catch(() => {
            this.$message.error('初始化数据失败');
           
      })

    },
    handleCheckAllChange(val){
      let arr = [];
      for(let i =0;i<this.tzfwData.length;i++){
            arr.push(this.tzfwData[i].dimCde);
      }
      this.investArea = val ? arr: [];
      this.isIndeterminate = false;
    },
    handleChecedtzfwChange(value){
      let checkedCount = value.length;
      this.checkAll = checkedCount === this.tzfwData.length;
      this.isIndeterminate = checkedCount > 0 && checkedCount < this.tzfwData.length;
    },
    initEdimExt(val,flag){
        let name = '';
        if(flag === 'fund_fundType'){
          let arr =  this.fundTypes;
          for(let i=0;i<arr.length;i++){
            if(val === arr[i].dimCde){
              name = arr[i].dimNme
                  return name;
            }
          }
        }

        if(flag === 'fund_managerType'){
          let arr =  this.managerTypes;
          for(let i=0;i<arr.length;i++){
            if(val === arr[i].dimCde){
              name = arr[i].dimNme
                  return name;
            }
          }
        }
        if(flag === 'fundCategory'){
          let arr =  this.fundTypes2;
          for(let i=0;i<arr.length;i++){
            if(val === arr[i].dimCde){
              name = arr[i].dimNme
                  return name;
            }
          }
        }

        return name;
       }


    }
  }
</script>

<style rel="stylesheet/scss" lang="scss" >
    .el_form_item{
        width:200px;
    }
    .el-checkbox__label {
        display: inline-table;
        padding-left: 10px;
        line-height: 19px;
        font-size: 14px;
        /* width: 100px; */
        white-space: normal !important;
    }
    .el-dialog {
            width: 65% !important;
        }

      .product_content {
           padding: 10px 15px 15px 15px;
           background: #fff;
           box-shadow: 0 2px 3px rgba(95, 95, 95, 0.1);
           border: 1px solid #E4E4E8;
           border-radius: 5px;
           -moz-border-radius: 5px;
           -webkit-border-radius: 5px;
             width: 550px;
            margin: auto;
       }

       .product_news_box {
             padding-right: 15px;

             height: 36px;
             line-height: 36px;
             background: #fff;
             color: #111;
             font-size: 14px;
         }
</style>





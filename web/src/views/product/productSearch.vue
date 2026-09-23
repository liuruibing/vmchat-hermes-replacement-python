<template>
  <div>
    <div class="toolbar">
      <el-form :inline="true" :rules="commonRules" ref="formInline" :model="formInline"
               class="demo-form-inline form_inline_search">
        <el-row>
          <el-col :span="16">
            <div class="grid-content bg-purple">
              <el-form-item label="产品代码" prop="fundCode">
                <el-input
                  v-model="formInline.fundCode"
                  placeholder="产品代码"
                  type="text"
                  clearable
                  maxlength="8"
                  auto-complete="off"
                  @keydown.enter.native="onSubmit(true)"
                  size="small"/>
              </el-form-item>

              <el-form-item label="产品名称" prop="fundName">
                <el-input
                  v-model="formInline.fundName"
                  placeholder="产品名称"
                  type="text"
                  clearable
                  maxlength="20"
                  auto-complete="off"
                  @keydown.enter.native="onSubmit(true)"
                  size="small"/>
                <!-- <select-table v-model="formInline.fundName"></select-table> -->
              </el-form-item>
            </div>

          </el-col>
          <el-col :span="8">
            <div class="grid-content bg-purple-light">
              <el-form-item class="search_button_com">
                <el-button :loading="countSubmit_btn" type="primary" @click="onSubmit(true)" style="margin-bottom: 5px;"
                           size="small"><i class="el-icon-search"></i>查询
                </el-button>
                <el-button :loading="countSubmit_btn" type="primary" style="margin-bottom: 5px;" plain size="small"
                           @click="restForm('formInline')"><i class="el-icon-delete"></i>重置
                </el-button>
                <el-button v-btn="'fund.insert.info'" :loading="countSubmit_btn" type="primary" plain @click="addData()"
                           style="margin-bottom: 5px; " size="small">
                  <i class="el-icon-circle-plus-outline"></i>新增
                </el-button>
              </el-form-item>
            </div>
          </el-col>
        </el-row>
      </el-form>
    </div>
    <div class="forms_table_title">
      <i class="el-icon-s-data"></i>产品列表
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
    >
      <el-table-column
        type="index"
        label="序号"
        fixed
        align="center"
        width="50">
      </el-table-column>
      <el-table-column
        prop="fundCode"
        label="产品代码"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        min-width="90"
        header-align="left"
        align="left">
        <template slot-scope="scope">
          <span>{{ scope.row.fundCode | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fundName"
        label="产品名称"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align="left"
        :show-overflow-tooltip="true"
        align="left">
        <template slot-scope="scope">
          <span>{{ scope.row.fundName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <!-- <el-table-column
        prop="fundType"
        label="基金类型"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align="left"
        align="left">
        <template slot-scope="scope">
          <span>{{ getDataName('fundTypes', scope.row.fundType) | noDataFilter }}</span>
        </template>
      </el-table-column> -->

      <el-table-column
        prop="fundTypeDetails"
        label="基金类型"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align="left"
        align="left">
        <template slot-scope="scope">
          <span>{{ transf( scope.row.fundTypeDetails,'fundTypeDetails') | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="investDirect"
        label="投资方向"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align="left"
        align="left">
        <template slot-scope="scope">
          <span>{{ getDataName('fundInvestDirectType', scope.row.investDirect) | noDataFilter }}</span>

        </template>
      </el-table-column>

      <el-table-column
        prop="cacheType"
        label="数据状态"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align="left"
        align="left">
        <template slot-scope="scope">
          <span v-if="scope.row.cacheType === '0'">使用中</span>
          <span v-else-if="scope.row.cacheType === '1'">新增草稿</span>
          <span v-else-if="scope.row.cacheType === '2'">修改草稿</span>
          <span v-else-if="scope.row.cacheType === '5'">新增待审核</span>
          <span v-else-if="scope.row.cacheType === '6'">修改待审核</span>
          <span v-else>{{ scope.row.cacheType | noDataFilter }}</span>

        </template>
      </el-table-column>
      <el-table-column label="是否分级" width="90" header-align="left" align="left" sortable="custom"
                       :sort-orders="['ascending', 'descending']" prop="isGrade">
        <template slot-scope="scope">
          <span v-if="scope.row.isGrade == '1'">是</span>
          <span v-else-if="scope.row.isGrade == '0'">否</span>
          <span v-else> - </span>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        min-width="260"
        fixed="right"
        align="center">
        <template slot-scope="scope">
          <!-- v-show="scope.row.cacheType != '1' && scope.row.cacheType != '5'" -->
          <el-button :disabled="scope.row.cacheType == '1' || scope.row.cacheType == '5'" :loading="countSubmit_btn"
                     type="primary" size="small" @click="serachDetail(scope.row)">查看详情
          </el-button>
          <el-button :disabled="scope.row.cacheType == '1' || scope.row.cacheType == '5'" v-btn="'fund.copy.info'"
                     :loading="countSubmit_btn" type="primary" size="small" @click="copyAddData(scope.row,'复制新增')">复制新增
          </el-button>
          <el-button :disabled="scope.row.cacheType == '5' || scope.row.cacheType == '6'" v-btn="'fund.update.info'"
                     :loading="countSubmit_btn" type="primary" size="small" @click="editData(scope.row,'修改')">修改
          </el-button>
          <el-button :loading="countSubmit_btn" type="primary" size="small" @click="downloadRow(scope.row)">下载
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <Pagination :total="total" :page="formInline.pageNum" :limit="formInline.pageSize"
                @pagination="Pagination"></Pagination>


    <!-- 新增,查看详情 -->
    <el-dialog :title="countTitle" width="70%" :modal-append-to-body="false" :before-close="handleClose"
               customClass="productSearchWidth" center :visible.sync="countDialog" :close-on-click-modal="false">
      <productAddPage v-if="productAddPage_show" :PageDataAdd="PageDataAdd" @pageCheckClick="pageCheckClick"
                      @close="closeDialog"></productAddPage>
      <!-- <productAddNewPage v-if="productAddNewPage_show" :PageDataAdd="PageDataAdd" @pageCheckClick="pageCheckClick"></productAddNewPage> -->

      <productDetailPage append-to-body v-if="productDetailPage_show" :PageDataDetail="PageDataDetail"
                         @pageCheckClick="pageCheckClick"></productDetailPage>
    </el-dialog>
    <!-- 新的查看详情 -->
    <view-info v-if="bassInfoSHow" ref="bassInofRelation" @closed="bassInfoSHow = false"></view-info>
  </div>
</template>

<script>
import selectTable from '@/views/commonComponents/selectTable.vue'
// bass-info
import ViewInfo from './editAndSearchFile/main-box'
import Pagination from '@/components/Pagination'
import commonFun from '@/filters/new_common'
import pageApi from '@/api/product/productSearch'
import productAddPage from './productAdd.vue'
//  import productAddNewPage from './productAddNew.vue'
import productDetailPage from './productDetail.vue'

export default {
  name: 'productSearch',
  inject:['reload'],
  components: {
    Pagination,
    productAddPage,
    productDetailPage,
    ViewInfo,
    selectTable
  },
  data() {
    return {
      bassInfoSHow: false,
      formInline: {
        fundCode: '',//产品代码
        fundName: '',//产品名称
        orderString: '', //列表排序
        pageSize: 50,//条数
        pageNum: 0
      },
      total: 0, //列表条数
      pageNum: 1, //页码
      pageSize: 50,//条数
      tableData: [{ fundCode: '001' }],//列表数据
      tableLoading: false, //列表加载
      tableMultipleSelection: [],
      countDialog: false, // 弹窗
      countTitle: '',//标题
      productAddPage_show: false,
      productAddNewPage_show: false,
      productDetailPage_show: false,
      PageDataAdd: {
        addType: -1, //-1新增，0修改，1复制新增
        fundCode: '',
        isAdd: false,
        fjgx_show: false,
        fundManager_show: false,
        kfr_show: false,
        xsfs_show: false,
        lxr_show: false,
        formData: {},
        beforeData: {},
        cacheType: ''
      },
      submitData: {},
      PageDataDetail: {
        sh_show: false,
        fundCode: '', //查看详情
        id: '', //审核详情
        detailType: 0 //0查看详情，1审核详情,2审核查看详情

      },
      // 表单校验规则
      commonRules: {
        //必填信息校验
        fundName: [
          // { required: false,pattern: /^[a-zA-Za-z0-9\u4e00-\u9fa5]+$/,  message: "请输入中文、字母、数字", trigger: "change"}
        ],
        fundCode: [
          // {required: false, pattern: /^[A-Z0-9]+$/, message: '请输入大写字母、数字',trigger: 'change'}
        ]
      },

      isSearchDetail: false,
      fundTypeArr: [],
      fundTypeObj:{},
      investDirectArr: [],
      countSubmit_btn: false
    }
  },
  //页面加载后触发
  mounted() {
    //基金类型
    if (this.$store.getters.edims['fundTypes'] !== undefined) {
      this.fundTypeArr = this.$store.getters.edims['fundTypes']
    } else {
      this.getEdimsGet('fundTypes')
    }
    if (this.$store.getters.edims['fundInvestDirectType'] !== undefined) {
      this.investDirectArr = this.$store.getters.edims['fundInvestDirectType']
    } else {
      //投资方向
      this.getEdimsGet('fundInvestDirectType')
    }
    this.getFundTypeDetails();
    this.selectAll(true)

  },
  watch: {
    "$route.path"(val, oldVal) {
      // 如果是当前页面路由
      if (val === "/product/productSearch") {
        // console.log(val);
        this.reload();
      } else {
      }
    },
  },
  computed:{
    transf(){
      return (val,flag)=>{
        if(val){
          if(flag=='fundTypeDetails'){
            return this.fundTypeObj[val] || val
          }
        }else{
          return ''
        }
      }
    }
  },
  methods: {
    //列表选择
    handleSelectionChange(val) {
      this.tableMultipleSelection = val
    },
    //排序
    handleSortChange(val) {
      // console.log(val);
      this.formInline.orderString = commonFun.orderByString(val)
      this.onSubmit(false)
    },
    //分页
    Pagination(val) {
      this.formInline.pageSize = val.limit//页面条数
      this.formInline.pageNum = val.page//页面
      this.onSubmit(false)
    },
    restForm(formName) {
      var self = this
      self.$refs[formName].resetFields()
    },
    pageCheckClick(data) {
      if (data.flag) {
        this.countDialog = false // 弹窗
        this.PageDataAdd.fundCode = ''
        this.productAddPage_show = false
        this.productAddNewPage_show = false
        this.productDetailPage_show = false
        this.selectAll(true)
      }
    },
    closeDialog() {
      this.countDialog = false
      this.productAddPage_show = false
      this.selectAll(true)
    },
    //新增
    addData() {
      this.PageDataAdd.addType = -1//-1新增，0修改，1复制新增
      this.PageDataAdd.fundCode = ''
      this.PageDataAdd.isAdd = true
      this.PageDataAdd.beforeData = ''
      this.PageDataAdd.fjgx_show = false
      this.PageDataAdd.fundManager_show = false
      this.PageDataAdd.kfr_show = false
      this.PageDataAdd.xsfs_show = false
      this.PageDataAdd.lxr_show = false
      this.PageDataAdd.formData.fundRedeems = []//赎回费率列表数据
      this.PageDataAdd.formData.fundContacts = []
      this.PageDataAdd.formData.fundGrades = []
      this.PageDataAdd.formData.fundRewards = []
      this.PageDataAdd.formData.fundSallers = []
      this.PageDataAdd.formData.fundManagers = []
      this.PageDataAdd.formData.fundOpens = []

      this.countDialog = true // 弹窗
      this.countTitle = '新增'//标题
      this.productAddPage_show = true
      this.productAddNewPage_show = false
      this.productDetailPage_show = false
      this.isSearchDetail = false
    },
    //复制新增
    copyAddData(row) {

      if (row.fundCode) {
        this.PageDataAdd.addType = 1//-1新增，0修改，1复制新增
        this.PageDataAdd.fundCode = row.fundCode
        this.PageDataAdd.beforeData = ''
        this.PageDataAdd.isAdd = false
        this.countTitle = '复制新增'//标题
        this.getDetail(row.fundCode, '复制新增')
      } else {
        this.$message.closeAll()
        this.$message({ type: 'error', message: '产品代码为空' })
      }

    },
    //修改
    editData(row, text) {
      if (row.fundCode) {
        this.PageDataAdd.addType = 0//-1新增，0修改，1复制新增
        this.PageDataAdd.fundCode = row.fundCode
        this.PageDataAdd.cacheType = row.cacheType
        this.PageDataAdd.isAdd = false
        this.countTitle = '修改'//标题
        this.getDetail(row.fundCode, '修改')
      } else {
        this.$message.closeAll()
        this.$message({ type: 'error', message: '产品代码为空' })
      }

    },
    //查看详情
    serachDetail(row) {
      // if(row.fundCode){
      //     this.PageDataDetail.fundCode = row.fundCode;
      //     this.countDialog = true; // 弹窗
      //     this.countTitle = '查看详情';//标题
      //     this.productAddPage_show = false;
      //      this.productAddNewPage_show =false;
      //     this.productDetailPage_show = true;
      //     this.isSearchDetail = true;
      // }else{
      //   this.$message.closeAll();
      //   this.$message({type: 'error',message: '产品代码为空'});
      // }
      // 以上是老方法---------------------
      this.bassInfoSHow = true
      this.$nextTick(() => {
        this.$refs.bassInofRelation.init(row, true)
      })
    },
    //dialog关闭事件
    handleClose(done) {
      if (!this.isSearchDetail) {
        this.$confirm('确认关闭 ？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
          .then(_ => {
            done()
            this.productAddPage_show = false
            this.productAddNewPage_show = false
            this.productDetailPage_show = false
          })
          .catch(_ => {
          })
      } else {
        done()
        this.productAddPage_show = false
        this.productAddNewPage_show = false
        this.productDetailPage_show = false
      }

    },
    //查询
    onSubmit(flag) {

      this.selectAll(flag)
    },
    selectAll(flag) {

      var continueFlag = false
      this.$refs['formInline'].validate((valid) => {
        if (valid) {
          continueFlag = true
          return true
        }
      })
      if (!continueFlag) {
        this.$message.closeAll()
        this.$message({
          message: '请完善输入信息',
          type: 'error'
        })
        return
      }

      this.tableLoading = true
      // 消除没有值的参数
      if (flag) {
        this.formInline.pageNum = 1
      }
      // if (this.formInline.fundName) {
      //   this.formInline.fundCode = this.formInline.fundName.split('_')[0]
      //   // this.formInline.fundName = this.formInline.fundName.split('_')[1]
      // } else this.formInline.fundCode = ''
      // let obj = {
      //   fundCode: this.formInline.fundCode,
      //   orderString: this.formInline.orderString,
      //   pageSize: this.formInline.pageSize,
      //   pageNum: this.formInline.pageNum
      // }
      let params = commonFun.parameterSrc(this.formInline)
      this.countSubmit_btn = true
      pageApi.getDataSourceList(params).then(response => {
        if (response.data.status === 200) {
          this.tableData = response.data.data.list
          // console.log('tableData',this.tableData);
          // this.tableData.forEach(i=>{
          //   console.log(i.cacheType);
          // })
          // 页面总条数
          this.total = response.data.data.total
        } else {
          this.tableData = []
          this.total = 0
          this.formInline.pageSize = 50
          this.formInline.pageNum = 1

        }
        this.tableLoading = false
        this.countSubmit_btn = false

      }).catch(() => {
        this.tableData = []
        this.total = 0
        this.formInline.pageSize = 50
        this.formInline.pageNum = 1
        this.tableLoading = false
        this.countSubmit_btn = false
      })
    },
    getFundTypeDetails(){
      pageApi.getFundType().then(res=>{
        if(res.data.status === 200){
          let arr = res.data.data;
          for (let i = 0; i < arr.length; i++) {
            this.$set(this.fundTypeObj,arr[i].fundTypeDetails,arr[i].fundTypeDetailName)
          }
        }
      })
    },
    getEdimsGet(val) {
      let params = val
      pageApi.getTransferType(params).then(res => {
        if (val === 'fundTypes') {
          this.fundTypeArr = res.data.data//基金类型
        }
        if (val === 'fundInvestDirectType') {
          this.investDirectArr = res.data.data//投资方向
        }
      })
    },
    getDataName(val, code) {
      if (val === 'fundTypes') {
        //基金类型
        return commonFun.dictionaryArrToName(this.fundTypeArr, code)
      }
      if (val === 'fundInvestDirectType') {
        //投资方向
        return commonFun.dictionaryArrToName(this.investDirectArr, code)
      }
    },
    getDetail(fundCode, text) {
      console.log(text)
      let params = {}
      params.fundCode = fundCode
      this.countSubmit_btn = true
      let path = null
      if (text == '复制新增') path = 'findFundModel'
      if (text == '修改') path = 'getFundModel'
      pageApi.getDataSourceEdit(path, params).then(response => {
        if (response.data.status === 200) {
          this.$message.closeAll()

          if (text == '复制新增') {
            let data = response.data.data
            this.PageDataAdd.formData = data
            this.initTableData(data)
          }
          if (text == '修改') {
            let data = response.data.data
            this.PageDataAdd.formData = data
            if (data.dataBefore) {
              console.log('1')
              this.PageDataAdd.beforeData = data.dataBefore
            } else {
              this.PageDataAdd.beforeData = ''
            }
            // let beforeData = data.dataBefore;
            // console.log(beforeData);
            this.initTableData(data)
          }

          this.PageDataAdd.fjgx_show = false
          this.PageDataAdd.fundManager_show = false
          this.PageDataAdd.kfr_show = false
          this.PageDataAdd.xsfs_show = false
          this.PageDataAdd.lxr_show = false

          this.countDialog = true // 弹窗

          this.productAddPage_show = true
          this.productAddNewPage_show = false
          this.productDetailPage_show = false
          this.isSearchDetail = false

        } else {
          this.$message.closeAll()
          this.$message({
            message: response.data.message || '查询失败',
            type: 'error'
          })
        }

        this.countSubmit_btn = false

      }).catch(() => {
        this.$message.closeAll()
        this.$message({
          message: '查询失败',
          type: 'error'
        })
        this.countSubmit_btn = false

      })

    },
    initTableData(data) {
      if (!data) {
        return false
      }

      if (!data.fundRedeems) {
        this.PageDataAdd.formData.fundRedeems = []//赎回费率列表数据

      }
      if (!data.fundContacts) {
        //赎回费率列表数据
        this.PageDataAdd.formData.fundContacts = []
      }
      if (!data.fundGrades) {
        //赎回费率列表数据
        this.PageDataAdd.formData.fundGrades = []
      }

      if (!data.fundRewards) {
        //计提列表数据
        this.PageDataAdd.formData.fundRewards = []
      }

      if (!data.fundSallers) {
        //计提列表数据
        this.PageDataAdd.formData.fundSallers = []
      }

      if (!data.fundManagers) {
        //计提列表数据
        this.PageDataAdd.formData.fundManagers = []
      }

      if (!data.fundOpens) {
        this.PageDataAdd.formData.fundOpens = []
      }
    },
    downloadRow(row){
      let params = {};
      params.fundCode = row.fundCode;
      params.token = this.$store.getters.token;
      let action = this.$store.state.setting.baseApi + '/api/fund/v1.0/export';
      commonFun.formDownloadFile(params,action,'post');
    }

  }

}
</script>

<style lang="scss" rel="stylesheet/scss">
.productSearchWidth {
  width: 70% !important;

  .el-form {
    width: 100% !important;
  }
}

.aaaa {
  height: 90% !important;

  .el-dialog__body {
    height: 100%;
  }
}
</style>

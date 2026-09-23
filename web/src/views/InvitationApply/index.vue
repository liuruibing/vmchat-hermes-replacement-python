
<template>
  <div class="invitaionApply" v-auto-enter>
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form :inline="true" ref="formInline" :model="formInline" class="standard-form">
          <el-row>
            <el-col :span="24">
              <el-form-item label="">
                <el-input v-model="formInline.fundCode" size="small" placeholder="请输入产品名称/产品代码" clearable style="width: 220px !important;"></el-input>
              </el-form-item>
              <el-form-item label="">
                <el-input v-model="formInline.nameGlr" size="small" placeholder="请输入管理人名称" clearable style="width: 160px !important;"></el-input>
              </el-form-item>
              <el-form-item label="">
                <el-select v-model="formInline.authStatus" size="small" clearable filterable placeholder="请选择状态">
                  <el-option v-for="item in ittypeList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </el-select>
              </el-form-item>

              <el-form-item label="">
                <el-select v-model="formInline.productStatus" size="small" clearable filterable placeholder="请选择产品运行状态">
                  <el-option v-for="item in productStatusList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </el-select>
              </el-form-item>

              <el-form-item label="">
                <el-date-picker
                  v-model="formInline.beginDate"
                  type="date"
                  size="small"
                  value-format="yyyy-MM-dd"
                  placeholder="产品成立开始日期">
                </el-date-picker>
                <span style="color:#fff">-</span>
                <el-date-picker
                  v-model="formInline.endDate"
                  type="date"
                  size="small"
                  value-format="yyyy-MM-dd"
                  placeholder="产品成立结束日期">
                </el-date-picker>
              </el-form-item>
              <el-form-item label="">
                <el-select v-model="formInline.fofMainStrategy" size="small" clearable filterable placeholder="请选择投资策略" @change="handleFoFMainStrategyChange">
                  <el-option v-for="item in fofMainStrategyList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </el-select>
              </el-form-item>

              <el-form-item label="" >
                <el-select v-model="formInline.fofSubStrategy" size="small" clearable filterable placeholder="请选择子策略">
                  <el-option v-for="item in fofSubStrategyList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </el-select>
              </el-form-item>

              <el-form-item label="" >
                <el-select v-model="formInline.starWishFlag" size="small" clearable filterable placeholder="请选择产品属性">
                  <el-option v-for="item in starWishFlagList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </el-select>
              </el-form-item>

              <el-form-item label="" >
                <el-select v-model="formInline.gfSelling" size="small" clearable filterable placeholder="请选择代销属性">
                  <el-option v-for="item in gfSellingList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </el-select>
              </el-form-item>

              <el-form-item>
                <el-button type="primary" size="small" icon="el-icon-search" @click="handleSearchTable(true)">查询</el-button>
                <el-button type="info" icon="el-icon-refresh" size="small" plain @click="resetForm()">重置</el-button>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" size="small" @click="bathSearchTable(false,'')">批量发起邀约</el-button>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" size="small" icon="el-icon-download" @click="downloadTemplate">产品清单模板</el-button>
                <el-button type="primary" size="small" icon="el-icon-upload" @click="triggerFileInput">上传产品清单</el-button>
                <input type="file" ref="fileInput" style="display: none" accept=".xls,.xlsx" @change="handleFileUpload">
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>

      </div>
    </div>
    <div class="table-content" id="standard-table">
      <div id="standard-table-margin">
        <vxe-table
          ref="refsTable"
          v-loading="tableLoading"
          :checkbox-config="{ checkStrictly: false, checkMethod: handleCheckBoxDisabled }"
          :cell-style="{ height: '50px' }"
          :data="tableData"
          :height="tableHeight"
          auto-resize
          stripe
          sync-resize
          show-overflow="tooltip"
          style="width: 100%"
          :sort-config="{ remote: true }"
          @sort-change="customSortMethod"
          resizable
        >
          <vxe-table-column type="checkbox" width="60" align="center"></vxe-table-column>
          <vxe-table-column label="" align="center" width="100px" >
            <template slot-scope="{ row }">
              <span class="table-operation standard-form">
                <el-button type="info" plain size="small" @click="bathSearchTable(true, row)">邀约</el-button>
              </span>
            </template>
          </vxe-table-column>
          <vxe-table-column
            v-for="item in column"
            :key="item.prop"
            :align="item.align"
            :field="item.prop"
            :show-overflow-tooltip="item.showtooltip"
            :title="item.label"
            :min-width="item.width"
            header-align="center"
            sortable
          >
            <template slot-scope="{ row }">
                <span v-if="item.prop === 'operateStatus'">
                  <el-tag size="mini" type="success" v-if="row[item.prop] == '1'">运行中</el-tag>
                  <el-tag size="mini" type="danger" v-else>已终止</el-tag>
                </span>
                <div v-else-if="item.prop === 'fundName'">
                   <span style="color: red;font-weight: 800;" v-if="row['starWishFlag'] == '1'">*</span>
                   <span>{{ row[item.prop] | noDataFilter }}</span>
                   <span style="padding-left: 10px;"  v-if="row['gfSelling'] == '代销'"><span class="greenGfSelling">代销</span></span>
                </div>
                <span v-else> {{ row[item.prop] | noDataFilter }}</span>
            </template>
          </vxe-table-column>
        </vxe-table>
        <vxe-pager
          :current-page="formInline.pageNum"
          :page-size="formInline.pageSize"
          :total="total"
          :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
          :page-sizes="pagerConfig.pageSizes"
          border
          size="medium"
          class="standard-vxe-pager"
          @page-change="pagination"

        />
      </div>
<!--      <div class="table-footer">
        <Pagination :total="total" :limit="formInline.pageSize" :page="formInline.pageNum" @pagination="pagination" />
      </div>-->
    </div>

    <addFormDialog ref="addFormRef" v-if="addFormShow" @close="addFormShow = false" @refresh="handleSearchTable(true)"></addFormDialog>
  </div>
</template>

<script>
import CONSTANTS from './scripts/constants'
import Pagination from '@/components/Pagination'
import commonFun from '@/filters/common'
import pageApi from './scripts/api.js'
import ToolBarSlot from '@/components/toolBarSlot'
import addFormDialog from './components/addFormDialog.vue'
import commonApi from '@/api/common.js'
export default {
  name: 'invitaionApply',
  components: {
    Pagination,
    ToolBarSlot,
    addFormDialog
  },
  data() {
    return {
      that: this,
      // form表单绑定
      formInline: {
        fundCode: '',
        nameGlr:'',
        authStatus:'',
        beginDate: '',
        endDate:'',
        fofMainStrategy:'',
        fofSubStrategy:'',
        starWishFlag:'',
        gfSelling:'',
        productStatus:'1',
        orderString: '',
        fundCodeList:[],
        fundNameList:[],
        pageSize: 20,
        pageNum: 1
      },
      // 表格高度
      tableHeight: 0,
      // 表格loading
      tableLoading: false,
      // 表格数据
      tableData: [],
      // 表格列
      column: CONSTANTS.TABLE_COLUMNS,
      // 总条数
      total: 0,
      // 状态
      ittypeList: CONSTANTS.ittypeList,
      indexGrantArr: [],
      //FOF投资策略
      fofMainStrategyList:[],
      fofSubStrategyList:[],
      fofSubStrategyOptions:[],
      starWishFlagList:[],
      productStatusList:[],
      //代销
      gfSellingList:[],

      addFormShow: false,
      pagerConfig: {
        pageSizes: [10,20,50,100,500], // 每页显示条目数的选项
      }

    }
  },
  computed: {

  },
   mounted() {
    //this.initStatus() //异步调用刷新数据
     this.initData();
  },
  methods: {
    async initStatus(){
      try {
        await this.refreshProcessStatus();
        this.initData();
      } catch (error) {
      }
    },
    /**
     * @description 初始化数据
     */
    initData() {
      this.getGrantArrOption()
      // 动态设置表格高度
      this.handleTableHeight()
      // 查询表格
      this.handleSearchTable(true)
      // 初始化投资策略下拉查询
      this.getListFoFMainStrategyEdims("FOFMAINSTRAGY_GF");
      // 初始化子策略下拉查询
      this.getListFoFSubStrategyEdims("FOFSUBSTRAGY_GF");
      // 初始化星愿产品下拉查询
      this.getListStarWishEdims("FOFSTARWISH_GF");

      // 初始化产品运行状态下拉查询
      this.getListProductStatusEdims("FOFPRODUCTSTATUS_GF");
     // 代销属性下拉框
      this.getListGfSellingEdims("GFSELLING");
    },

    // 投资策略列表查询
    getListFoFMainStrategyEdims (type) {
      // 字典类型
      let params = type
      commonApi.edimsCommon(params).then(res => {
        let { status, data } = res.data
        if (status === 0) {
          this.fofMainStrategyList = data
        }
      })
    },

    // 投资策略列表查询
    getListFoFSubStrategyEdims (type) {
      // 字典类型
      let params = type
      commonApi.edimsCommon(params).then(res => {
        let { status, data } = res.data
        if (status === 0) {
          this.fofSubStrategyOptions = data
        }
      })
    },

    // 代销属性下拉框
    getListGfSellingEdims (type) {
      // 字典类型
      let params = type
      commonApi.edimsCommon(params).then(res => {
        let { status, data } = res.data
        if (status === 0) {
          this.gfSellingList = data
        }
      })
    },

    // 产品运行状态列表查询
    getListProductStatusEdims (type) {
      // 字典类型
      let params = type
      commonApi.edimsCommon(params).then(res => {
        let { status, data } = res.data
        if (status === 0) {
          this.productStatusList = data
        }
      })
    },

    // 产品属性列表查询
    getListStarWishEdims (type) {
      // 字典类型
      let params = type
      commonApi.edimsCommon(params).then(res => {
        let { status, data } = res.data
        if (status === 0) {
          this.starWishFlagList = data
        }
      })
    },


    handleFoFMainStrategyChange(value) {
      this.formInline.fofSubStrategy = ''
      this.fofSubStrategyList = this.fofSubStrategyOptions.filter((item) => item.dimEdit === value)

    },
    /**
     * @description 去除无值字段，包含数组
     */
    parameterSrc(data) {
      const newData = {}
      for (const key in data) {
        if (data[key] === '' || data[key] === undefined || data[key] === null || JSON.stringify(data[key]) === '[]') {
        } else {
          newData[key] = data[key]
        }
      }
      return newData
    },
    /**
     * @description 动态设置表格高度
     */
    handleTableHeight() {
      this.$nextTick(() => {
        // 根据浏览器高度设置初始高度
        this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 165
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 165
        }
      })
    },
    /**
     * @description 表格查询
     */
    handleSearchTable(flag) {
      if (flag) {
        this.formInline.pageNum = 1
      }
      let params = Object.assign({}, this.formInline)
      delete params.date
      params = this.parameterSrc(params)
      this.tableLoading = true
      pageApi.warnRuleManageList(params).then((res) => {
        this.tableLoading = false
        const {data, status} = res.data
        if (status === 200 && data) {
          this.tableData = data.list || []
          this.total = data.total || 0
        } else {
          this.tableData = []
          this.total = 0
        }
      })
    },
    getGrantArrOption() {
      let type = 'FUNDINRIGHT'
      commonApi
        .edimsDdiaCommon(type)
        .then(res => {
          let { status, data } = res.data
          if (status == 0) {
            this.indexGrantArr = data
          } else {
            this.indexGrantArr = []
          }
        })
        .catch(err => {
          this.indexGrantArr = []
        })
    },
    /**
     * @description 批量发起��约
     */
    bathSearchTable(type, row) {
      this.$message.closeAll()
      const list = this.$refs.refsTable.getCheckboxRecords() || []
      if(type){
        if (row.authStatus.includes('待审批')) {
          return this.$message.warning('您所选的'+row.fundName+'产品已申请等级权限，正在审批中，请勿重复申请。')
        }

       /*  if(row.orgPromise == '1' && row.mgrPromise == undefined) {
          return this.$message.warning('您的合投承诺'+row.nameGlr+'管理人正审核中，需经管理人通过后再选择该管理人的产品进行申请。')
        } */

        this.addFormShow = true
        this.$nextTick(() => {
          this.$refs.addFormRef.init(this.indexGrantArr,row,true)
        })
      }else{
        if (!list.length) {
          return this.$message.warning('请至少选择一条数据')
        }
        this.addFormShow = true
        this.$nextTick(() => {
          this.$refs.addFormRef.init(this.indexGrantArr,list,false)
        })
      }
    },

    handleCheckBoxDisabled({ row }) {
      if (row.authStatus.includes('待审批')) {
        return false
      }
      /* if (row.orgPromise == '1' && row.mgrPromise == undefined) {
        return false
      } */
      return true
    },

    // 刷新流程状态
    refreshProcessStatus() {
      return new Promise((resolve, reject) => {
        pageApi.refreshProcessStatus().then(res => {
          let {status, message} = res.data
          if (status !== 200) {
            this.$message.closeAll()
            this.$message.warning(message)
          }
          resolve()
        }).catch(err => {
          resolve()
        })
      })
    },
    /**
     * @description 监听分页
     */
    pagination(val) {
     /*  let { page, limit } = val
      this.formInline.pageNum = page
      this.formInline.pageSize = limit
 */
      const { currentPage, pageSize } = val;
      // 起始页
      this.formInline.pageNum = currentPage;
      // 每页数量
      this.formInline.pageSize = pageSize;
      this.handleSearchTable(false)
    },
    // 排序的公共方法
    customSortMethod(val) {
      this.formInline.orderString = commonFun.queryOrderBy_vxe_template(val)
      this.handleSearchTable(false)
    },
    // 清除
    resetForm() {
      this.formInline.fundCode = '';
      this.formInline.nameGlr = '';
      this.formInline.authStatus = '';
      this.formInline.beginDate = '';
      this.formInline.endDate = '';
    },

    downloadTemplate() {
      pageApi.downloadFundTemplate().then(function (res) {
        // 创建blob对象处理Excel二进制流
        const blob = new Blob([res.data], { type: 'application/vnd.ms-excel' })
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = '产品清单模板.xls'
        a.click()
        // 释放URL对象
        window.URL.revokeObjectURL(url)
        this.$message.success('模板下载成功')
      }.bind(this)).catch(function (err) {
        this.$message.closeAll()
        this.$message.error('模板下载失败：' + (err.message || '服务器错误'))
      }.bind(this))
    },

    triggerFileInput() {
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = ''
      }
      this.$refs.fileInput.click()
    },

    handleFileUpload(e) {
      const file = e.target.files[0]
      if (!file) {
        return
      }

      // 校验文件格式
      const fileName = file.name
      if (!fileName.endsWith('.xls') && !fileName.endsWith('.xlsx')) {
        this.$message.warning('仅支持.xls和.xlsx格式的Excel文件')
        this.$refs.fileInput.value = ''
        return
      }

      // 构建FormData
      const formData = new FormData()
      formData.append('file', file)

      this.tableLoading = true
      pageApi.parseFundExcel(formData).then(function (res) {
        this.tableLoading = false
        const resData = res.data || {}
        if (resData.status === 200) {
          const result = resData.data || {}
          this.formInline.fundCodeList = result.fundCodeList || []
          this.formInline.fundNameList = result.fundNameList || []
          if (this.formInline.fundCodeList.length > 0 || this.formInline.fundNameList.length > 0 ) {
            // 自动触发查询
            this.handleSearchTable(true)
          } else {
            this.$message.warning('Excel中未解析到有效产品代码')
          }
        } else {
          this.$message.error('Excel解析失败：' + (resData.message || '解析错误'))
        }
        // 清空文件选择框
        this.$refs.fileInput.value = ''
      }.bind(this)).catch(function (err) {
        this.tableLoading = false
        this.$message.error('文件上传失败：' + (err.message || '网络错误'))
        // 清空文件选择框
        this.$refs.fileInput.value = ''
      }.bind(this))
    },

    beforeDestroy() {
      // 组件销毁移除监听事件
      window.onresize = null
    }
  }
}
</script>

<style lang="scss" scoped>
.invitaionApply {
  // padding: 10px;
  .search-bar {
    // border-bottom: 1px solid #e1e0e0;
  }
  ::v-deep .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
  ::v-deep .el-button.el-button--mini {
    padding: 7px !important;
  }
}
::v-deep .el-dialog.customClass {
  width: 55% !important;
}
::v-deep .vxe-table--render-default .vxe-cell--checkbox:not(.is--disabled):hover .vxe-checkbox--icon:before {
  border-color: #e9c5a5!important
}
</style>
<style>
.customClass .el-dialog__body .edit-product .el-form {
  width: 100% !important;
}
.greenGfSelling{
  color: green;
  font-weight: 800;
  padding-left: 5px;
  padding-right: 5px;
  border: 1px solid green;
}
</style>

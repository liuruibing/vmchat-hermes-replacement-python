<template>
  <div class="emotional-index analyse-page">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formQuery" :inline="true" class="standard-form" :model="formQuery" :rules="searchRules">
          <el-row>
            <el-col :span="24">
<!--              <el-form-item label="" prop="vcFundcode">
                <el-input v-model="formQuery.vcFundcode" placeholder="请选择产品代码" size="small" v-on:click.native="openPositionDialog"></el-input>
              </el-form-item>-->
              <el-form-item label="" prop="vcFundcode">
                <ProductSelectInput
                  v-model="formQuery.product"
                  placeholder="请选择产品"
                  :input-width="'260px'"
                  @select="handleProductSelect"
                  @clear="handleProductClear"
                />
              </el-form-item>
              <el-form-item label="" prop="tradeDate">
                <el-date-picker
                  v-model="formQuery.tradeDate"
                  type="date"
                  :picker-options="pickerOptions"
                  size="small"
                  value-format="yyyy-MM-dd"
                  placeholder="时间"
                ></el-date-picker>
              </el-form-item>
              <el-form-item label="" prop="calculateType">
                <el-select v-model="formQuery.calculateType" placeholder="请选择计算方式" size="small">
                  <el-option v-for="item in typeOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item class="">
                <el-button icon="el-icon-search" type="primary" size="small" @click="onSubmit('formQuery')">查询</el-button>
                <el-button icon="el-icon-refresh" type="info" plain size="small" @click="reset">重置</el-button>
                <el-button size="small" type="info" plain icon="el-icon-download" @click="exportData">导出</el-button>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>
    </div>
    <div class="chart-main">
      <div class="target-trend">
        <div class="page-model-title">
          <div class="title-icon">
            <div class="color-box"></div>
          </div>
          <span class="title-txt">穿透分析-债券</span>
        </div>
        <div id="standard-table">
          <div id="standard-table-margin">
            <vxe-table
              ref="myTable"
              v-loading="tableLoading"
              :data="tableData"
              :height="tableHeight"
              :cell-style="{ height: '50px' }"
              auto-resize
              sync-resize
              show-overflow
              stripe
              style="width: 100%"
              resizable
            >
              <vxe-table-column
                v-loading="tableLoading"
                v-for="(col, i) in tableColumns"
                :key="Math.random()"
                :field="col.prop"
                :title="col.label"
                min-width="200"
                :align="col.align"
                show-header-overflow
                show-overflow="title"
                show-footer-overflow
                header-align="center"
                stripe
              >
                <template slot-scope="scope">
                  <span v-if="col.prop == 'SYMBOLDURATION'">{{ (scope.row[col.prop] / 365) | moneyYuan }}</span>
                  <span v-else>{{ scope.row[col.prop] | noDataFilter }}</span>
                </template>
              </vxe-table-column>
            </vxe-table>
          </div>
          <!--    <Pagination
          :total="total"
          :limit="formQuery.pageSize"
          :page="formQuery.pageNum"
          @pagination="pagination"
        />-->
        </div>
      </div>
    </div>
    <product-selector
      :isShowButtonAndTag="false"
      :dialog-visible="productSelectorVisible"
      :tree-data="treeData"
      :show-tree-key-array="showTreeKeyArray"
      :select-list="selectList"
      :default-checked-keys="defaultCheckedKeys"
      @closedialog="handleDialogClosed"
      @submitdialog="handleSubmitClick"
    ></product-selector>
  </div>
</template>

<script>
import request from '@/utils/request'
import myChart from '@/components/Echarts'
import { downLoadFileByUrl } from '@/utils'
import commonApi from '@/api/common'
import productSelector from '@/components/productSelector'
import Pagination from '@/components/Pagination'
import store from '../../../store'
import ProductSelectInput from '@/components/productSelector/ProductSelectInput'

export default {
  name: 'ctfxzq',
  components: {
    myChart,
    productSelector,
    Pagination,
    ProductSelectInput
  },
  data() {
    const validateEndDate = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请选择日期'))
      } else {
        callback()
      }
    }
    const validateFund = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请选择产品'))
      } else {
        callback()
      }
    }

    return {
      formQuery: {
        product: null,
        tdname: [
          'SYMBOLCODE,债券代码',
          'SYMBOLNAME,债券名称',
          'SYMBOLTYPE,分类',
          'SYMBOLDURATION,剩余期限（年）',
          'SYMBOLLEVEL,债券评级',
          'FPRICE,母基金公允价值合计(元)',
          'MPRICEBIT,占母基金净资产比例(%)',
          'FULLPRICEBIT,占母基金总资产比例(%)'
        ],
        calculateType: 'cb',
        tradeDate: '',
        type: 'zq',
        xonename: '债券代码',
        xsumname: '母基金公允价值合计(元)',
        xbitname: '占母基金净资产比例(%)',
        xbitnamefull: '占母基金总资产比例(%)',
        xonenamelast1: '个券汇总',
        xonenamelast2: '母基金期末净资产',
        xonenamelast3: '母基金期末总资产',
        unit: '元',
        vcdata: 'FSZPRICE',
        vcFundname: '',
        fId: '',
        vcParentFundcode: '0',
        vcFundcode: '',
        xtwoname: '债券名称'
      },
      typeOptions: [
        { label: '按成本', value: 'cb' },
        { label: '按市值', value: 'sz' }
      ],
      typeOptions1: [
        { label: '市值', value: 'sz' },
        { label: '估值增值', value: 'sl' }
      ],
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
      // 表格高度
      tableHeight: 0,
      showTreeKeyArray: ['产品列表', '私有产品'],
      selectList: [],
      pickerOptions: {},
      defaultCheckedKeys: 'zstgwb',
      // 选择产品弹窗
      productSelectorVisible: false,
      disabledDate: true,
      targetTrendOptions: {},
      searchRules: {
        tradeDate: [
          { required: true, message: '请选择日期', trigger: 'blur' },
          { validator: validateEndDate, trigger: 'blur' }
        ],
        vcFundcode: [
          { required: true, message: '请选择产品', trigger: 'change' },
          { validator: validateFund, trigger: 'blur' }
        ],
        product: [
          { required: true, message: '请选择产品', trigger: 'change' },
          { validator: validateFund, trigger: 'blur' }
        ]
      },
      issearchFxButton: false,
      //表格
      hyOptions: [],
      tableLoading: false,
      tableData: [],
      TABLE_COLUMNS: [],
      tableColumns: [],
      tableData2: [],
      total: 0
    }
  },
  async mounted() {
    var self = this
    var baseTime = store.state.edims.baseTime
    if(baseTime){
      self.formQuery.tradeDate = baseTime.endDate
    }
    this.handleTableHeight()
    this.getBeCodeOptions()
  },
  methods: {
    /**
     * @description 动态设置表格高度
     */
    handleTableHeight() {
      this.$nextTick(() => {
        // 根据浏览器高度设置初始高度
        this.tableHeight = window.innerHeight - this.$refs.myTable.$el.offsetTop - 140
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.myTable.$el.offsetTop - 140
        }
      })
    },
    /**
     * @description 查询基准编码下拉
     */
    getBeCodeOptions() {
      const params = {
        indexCode: '06521772-1d21-45e7-91fd-53374903b678'
      }
      commonApi.getDataBysqlCode(params).then((res) => {
        if (res.data.status === 0) {
          console.log(res.data)
          this.hyOptions = res.data.data || []
          this.industry = res.data.data[0].CODE
        }
      })
    },
    //点击弹窗
    openPositionDialog() {
      this.productSelectorVisible = true
    },
    //关闭弹窗
    handleDialogClosed() {
      this.productSelectorVisible = false
    },
    //获取弹窗产品代码和名称
    handleSubmitClick(arr) {
      this.productSelectorVisible = false
      this.formQuery.vcFundcode = arr[0].VC_FUNDCODE || ''
      this.formQuery.vcFundname = arr[0].VC_FUNDNAME || ''
      this.selectList = arr
    },
    handleProductSelect: function(product) {
      this.formQuery.vcFundcode = product.VC_FUNDCODE || ''
      this.formQuery.vcFundname = product.VC_FUNDNAME || ''
    },
    handleProductClear: function() {
      this.formQuery.vcFundcode = ''
      this.formQuery.vcFundname =  ''
    },
    onSubmit(formName) {
      var self = this
      self.$refs[formName].validate((valid) => {
        if (valid) {
          try {
            self.handleQueryChartData()
          } catch (e) {}
        } else {
          return false
        }
      })
    },
    //查询获取数据
    handleQueryChartData() {
      if (this.formQuery.vcFundcode && this.formQuery.vcFundcode == '') {
        this.$message.closeAll()
        this.$message({
          message: '产品代码不可为空',
          type: 'warning',
          customClass: 'message-warning'
        })
        return
      }
      this.tableLoading = true
      try {
        const params = {
          tdname: this.formQuery.tdname || '',
          calculateType: this.formQuery.calculateType || '',
          tradeDate: this.formQuery.tradeDate || '',
          type: this.formQuery.type || '',
          xonename: this.formQuery.xonename || '',
          xsumname: this.formQuery.xsumname || '',
          xbitname: this.formQuery.xbitname || '',
          xbitnamefull: this.formQuery.xbitnamefull || '',
          xonenamelast1: this.formQuery.xonenamelast1 || '',
          xonenamelast2: this.formQuery.xonenamelast2 || '',
          xonenamelast3: this.formQuery.xonenamelast3 || '',
          unit: this.formQuery.unit || '',
          vcdata: this.formQuery.vcdata || '',
          vcFundname: this.formQuery.vcFundname || '',
          fId: this.formQuery.fId || '',
          vcParentFundcode: this.formQuery.vcParentFundcode || '',
          vcFundcode: this.formQuery.vcFundcode || '',
          xtwoname: this.formQuery.xtwoname
        }

        request({
          url: `/api/fundanalyze/analyzeBond.do`,
          method: 'post',
          data: params
        }).then((res) => {
          if (res.status === 200) {
            this.tableData2 = res.data
            this.dataOrganization()
            this.tableLoading = false
          } else {
            this.tableLoading = false
          }
        })
      } catch (e) {
        this.tableLoading = false
      }
    },

    //数据处理
    dataOrganization() {
      const data2 = this.tableData2
      const data3 = []
      const data4 = []
      this.tableColumns = []
      this.tableData = []
      if (data2.length > 0) {
        Object.keys(data2[0]).map((key) => {
          data3.push(key)
        }),
          Object.values(data2[0]).map((value) => {
            data4.push(value)
          })
        for (var i = 0; i < data3.length; i++) {
          this.tableColumns.push({
            prop: data3[i],
            label: data4[i],
            align: 'center'
          })
        }
        for (var i = 1; i < data2.length; i++) {
          this.tableData.push(data2[i])
        }
      }
    },
    //导出数据
    exportData() {
      let params = {
        tdname: this.formQuery.tdname || '',
        calculateType: this.formQuery.calculateType || '',
        tradeDate: this.formQuery.tradeDate || '',
        type: this.formQuery.type || '',
        xonename: this.formQuery.xonename || '',
        xsumname: this.formQuery.xsumname || '',
        xbitname: this.formQuery.xbitname || '',
        xbitnamefull: this.formQuery.xbitnamefull || '',
        xonenamelast1: this.formQuery.xonenamelast1 || '',
        xonenamelast2: this.formQuery.xonenamelast2 || '',
        xonenamelast3: this.formQuery.xonenamelast3 || '',
        unit: this.formQuery.unit || '',
        vcdata: this.formQuery.vcdata || '',
        vcFundname: this.formQuery.vcFundname || '',
        fId: this.formQuery.fId || '',
        vcParentFundcode: this.formQuery.vcParentFundcode || '',
        vcFundcode: this.formQuery.vcFundcode || '',
        xtwoname: this.formQuery.xtwoname
      }
      const fileName = '债券-导出.xls'
      const url = 'api/fundanalyze/exportBond.do'
      downLoadFileByUrl(url, params, fileName, this)
    },
    //重置清空操作
    reset() {
      this.formQuery.vcFundcode = ''
      this.formQuery.tradeDate = ''
      this.formQuery.calculateType = 'cb'
    },
    pagination(val) {
      const { page, limit } = val
      this.formQuery.pageNum = page
      this.formQuery.pageSize = limit
      this.queryExamineList()
    }
  }
}
</script>

<style lang="scss" scoped>
.emotional-index {
  .funds-filter {
    width: 100%;
    // border-bottom: 1px solid #e1e0e0;

    .dbjz {
      ::v-deep .el-select .el-input--small {
        width: 260px !important;
      }

      ::v-deep .el-select .el-select__tags {
        max-width: 234px !important;
      }
    }
  }
  .chart-main {
    margin-top: 3px;
    width: 100%;
    .chart-title {
      padding: 10px 0;
      // border-bottom: 1px solid #0F65DD;

      .title-icon {
        vertical-align: middle;
        display: inline-block;

        .color-box {
          display: inline-block;
          height: 30px;
          width: 2px;
          background-color: #0f65dd;
        }
      }

      .title-txt {
        color: #0f65dd;
        vertical-align: middle;
        height: 35px;
        line-height: 35px;
        font-size: 16px;
        margin-left: 5px;
        display: inline-block;
      }
    }
    .chart-content {
      height: 500px;
      margin-top: 15px;

      .echarts_box {
        height: 100%;
        width: 100%;
      }
    }
  }
}
::v-deep .vxe-table .vxe-body--row.row--stripe {
  background-color: #fafafa !important;
}
</style>

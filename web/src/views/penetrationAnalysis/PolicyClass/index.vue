<template>
  <div class="emotional-index">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formQuery" :inline="true" class="standard-form" :model="formQuery" :rules="searchRules">
          <el-row>
            <el-col :span="24">
              <el-form-item label="产品代码" prop="vcFundcode">
                <el-input v-model="formQuery.vcFundcode" placeholder="产品代码" size="small" v-on:click.native="openPositionDialog"></el-input>
              </el-form-item>
              <el-form-item label="时间" prop="tradeDate">
                <el-date-picker
                  v-model="formQuery.tradeDate"
                  type="date"
                  :picker-options="pickerOptions"
                  size="small"
                  value-format="yyyy-MM-dd"
                  placeholder="时间"
                ></el-date-picker>
              </el-form-item>
              <el-form-item label="计算方式" prop="calculateType">
                <el-select v-model="formQuery.calculateType" placeholder="请选择" size="small">
                  <el-option v-for="item in typeOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="展示维度" prop="dimension">
                <el-select v-model="formQuery.dimension" placeholder="请选择" size="small">
                  <el-option v-for="item in typeOptions1" :key="item.value" :label="item.label" :value="item.value"></el-option>
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
          <span class="title-txt">穿透分析-策略类别</span>
        </div>
        <div id="standard-table">
          <div id="standard-table-margin">
            <vxe-table
              v-loading="tableLoading"
              :data="tableData"
              :cell-style="{ height: '50px' }"
              auto-resize
              sync-resize
              show-overflow
              style="width: 100%"
              max-height="500"
              :tree-config="{ transform: true, rowField: 'id', parentField: 'parentId', expandAll: true }"
              resizable
            >
              <vxe-table-column field="dimNme" label="策略类型" align="center" show-overflow-tooltip header-align="center" min-width="200" tree-node></vxe-table-column>
              <vxe-table-column
                v-loading="tableLoading"
                v-for="(col, i) in tableColumns"
                :key="i"
                :field="col.prop"
                :label="col.label"
                min-width="200"
                :align="col.align"
                show-overflow-tooltip
                header-align="center"
              >
                <template slot-scope="scope">
                  <span v-if="col.prop == 'price' || col.prop == 'mPrice' || col.prop == 'fullPrice' || col.prop == 'valueTotal'">{{ scope.row[col.prop] | moneyYuan }}</span>
                  <span v-else>{{ scope.row[col.prop] | noDataFilter }}</span>
                </template>
              </vxe-table-column>
            </vxe-table>
          </div>

          <!-- <Pagination
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
import { EXAMINE_TABLE } from './scripts/policy'
import request from '@/utils/request'
import myChart from '@/components/Echarts'
import { downLoadFileByUrl } from '@/utils'
import productSelector from '@/components/productSelector'
import Pagination from '@/components/Pagination'
import fun from '@/filters/common'
export default {
  name: 'ctfxcllb',
  components: {
    myChart,
    productSelector,
    Pagination
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
        filterslength: 0,
        pagenum: 0,
        pagesize: 10,
        type: 'sc',
        replaceArr: '#,#br#.#',
        replaceWordArr: '',
        replaceCode: ',',
        xonename: '维度名称',
        xsumname: '母基金公允价值合计',
        xbitname: '占母基金净资产比例（*）',
        xbitnamefull: '占母基金总资产比例（*）',
        xonenamelast1: '大类合计',
        xonenamelast2: '母基金期末净资产',
        xonenamelast3: '母基金期末总资产',
        unit: '元',
        vcdata: 'FSZPRICE',
        conditions: ['展示维度#'],
        vcFundname: '',
        fId: '',
        vcParentFundcode: '0',
        vcFundcode: '',
        tradeDate: '',
        calculateType: 'cb',
        dimension: 'sz'
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
        ]
      },
      issearchFxButton: false,
      //表格
      tableLoading: false,
      tableData: [],
      TABLE_COLUMNS: [],
      tableColumns: EXAMINE_TABLE,
      tableData2: [],
      total: 0
    }
  },
  async mounted() {
    //this.dataOrganization()
    // this.handleQueryChartData()
  },
  methods: {
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
    onSubmit(formName) {
      var self = this
      self.$refs[formName].validate((valid) => {
        if (valid) {
          try {
            self.handleQueryChart()
          } catch (e) {}
        } else {
          return false
        }
      })
    },
    //查询获取数据
    handleQueryChart() {
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
          filterslength: this.formQuery.filterslength,
          type: this.formQuery.type,
          pagenum: this.formQuery.pagenum,
          pagesize: this.formQuery.pagesize,
          replaceArr: this.formQuery.replaceArr || '',
          replaceWordArr: this.formQuery.replaceWordArr || '',
          replaceCode: this.formQuery.replaceCode || '',
          xonename: this.formQuery.xonename || '',
          xsumname: this.formQuery.xsumname || '',
          xbitname: this.formQuery.xbitname || '',
          xbitnamefull: this.formQuery.xbitnamefull || '',
          xonenamelast1: this.formQuery.xonenamelast1 || '',
          xonenamelast2: this.formQuery.xonenamelast2 || '',
          xonenamelast3: this.formQuery.xonenamelast3 || '',
          unit: this.formQuery.unit || '',
          vcdata: this.formQuery.vcdata || '',
          conditions: this.formQuery.conditions || '',
          vcFundname: this.formQuery.vcFundname || '',
          fId: this.formQuery.fId || '',
          vcParentFundcode: this.formQuery.vcParentFundcode || '',
          vcFundcode: this.formQuery.vcFundcode || '',
          tradeDate: this.formQuery.tradeDate || '',
          calculateType: this.formQuery.calculateType || '',
          dimension: this.formQuery.dimension
        }
        request({
          url: `api/fundanalyze/strategyCategoryList.do`,
          method: 'post',
          data: params
        }).then((res) => {
          if (res.status === 200) {
            var responseData = res.data
            console.log(responseData)
            if (responseData !== undefined && responseData != '') {
              const map = {}
              const val = []

              for (var i = 0; i < responseData.length; i++) {
                map[responseData[i].id] = responseData[i]
              }
              for (var i = 0; i < responseData.length; i++) {
                const parent = map[responseData[i].parentId]
                if (parent) {
                  ;(parent.children || (parent.children = [])).push(responseData[i])
                } else {
                  val.push(responseData[i])
                }
              }
              this.tableData = val
              console.log(this.tableData)
            }
            this.tableLoading = false
          } else {
            this.tableLoading = false
          }
        })
      } catch (e) {
        this.tableLoading = false
      }
    },

    //导出数据
    exportData() {
      let params = {
        filterslength: this.formQuery.filterslength,
        type: this.formQuery.type,
        pagenum: this.formQuery.pagenum,
        pagesize: this.formQuery.pagesize,
        replaceArr: this.formQuery.replaceArr || '',
        replaceWordArr: this.formQuery.replaceWordArr || '',
        replaceCode: this.formQuery.replaceCode || '',
        xonename: this.formQuery.xonename || '',
        xsumname: this.formQuery.xsumname || '',
        xbitname: this.formQuery.xbitname || '',
        xbitnamefull: this.formQuery.xbitnamefull || '',
        xonenamelast1: this.formQuery.xonenamelast1 || '',
        xonenamelast2: this.formQuery.xonenamelast2 || '',
        xonenamelast3: this.formQuery.xonenamelast3 || '',
        unit: this.formQuery.unit || '',
        vcdata: this.formQuery.vcdata || '',
        conditions: this.formQuery.conditions || '',
        vcFundname: this.formQuery.vcFundname || '',
        fId: this.formQuery.fId || '',
        vcParentFundcode: this.formQuery.vcParentFundcode || '',
        vcFundcode: this.formQuery.vcFundcode || '',
        tradeDate: this.formQuery.tradeDate || '',
        calculateType: this.formQuery.calculateType || '',
        dimension: this.formQuery.dimension
      }
      const fileName = '策略类别-导出.xls'
      const url = 'api/fundanalyze/exportStrategyCategory.do?searchMod=download'
      downLoadFileByUrl(url, params, fileName, this)
    },
    //重置清空操作
    reset() {
      this.formQuery.vcFundcode = ''
      this.formQuery.tradeDate = ''
      this.formQuery.dimension = 'sz'
      this.formQuery.calculateType = 'cb'
    },
    pagination(val) {
      const { page, limit } = val
      this.formQuery.pageNum = page
      this.formQuery.pageSize = limit
      this.onSubmit()
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
::v-deep .el-button.el-button--info {
  color: #333;
  background-color: #dddddd;
  border-color: #dddddd;
}
</style>

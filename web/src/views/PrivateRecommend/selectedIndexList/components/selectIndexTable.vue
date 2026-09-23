<template>
  <div class="select-index-table">
    <!-- <el-row justify="space-around" type="flex" class="page-model-title">
      <el-col :span="12">
        <div style="vertical-align: middle; display: inline-block" class="title-icon">
          <div class="color-box"></div>
        </div>
        <div class="title-txt">
          <span v-if="rankType === 'XX'">热点产品</span>
          <span v-else>{{ titleStr }}</span>
                   <el-tooltip class="table_header_icon" effect="dark" placement="top">
                     <span slot="content">{{ iconStr }}</span>
                     <i class="el-icon-question" style="cursor: pointer;"></i>
                   </el-tooltip>
        </div>
      </el-col>
      <el-col :span="12">
        <div style="display: flex; float: right">
          <el-button size="small" type="info" @click="onContrast">对比</el-button>
          <el-button size="small" type="info" @click="handleBatchFocus">批量关注</el-button>
          <el-button :disabled="isDisabled" :icon="exportLoading ? 'el-icon-loading' : ''" size="small" type="info" @click="handleExcelExport">
            导出Excel
          </el-button>
          <el-button size="small" type="info" @click="productSelectDialogVisible = true">
            自定义指标
          </el-button>
        </div>
      </el-col>
    </el-row> -->
    <div style="display: flex; justify-content: space-between; margin: 5px 0" class="standard-form">
      <span>
        <el-button size="small" type="info" plain @click="onContrast">对比</el-button>
        <el-button size="small" type="info" plain @click="handleBatchFocus">批量关注</el-button>
      </span>
      <span>
        <el-button :disabled="isDisabled" :icon="exportLoading ? 'el-icon-loading' : ''" size="small" type="info" plain @click="handleExcelExport">
          导出Excel
        </el-button>
        <el-button size="small" type="info" plain @click="productSelectDialogVisible = true">
          自定义指标
        </el-button>
      </span>
    </div>
    <div v-if="basicCheckArr && basicCheckArr.length">
      已选产品:
      <el-tag v-for="item in basicCheckArr" :key="item.id" :disable-transitions="false" closable @close="handleCloseBasic(item)">
        <!--        <span>{{ item.fundCode }}</span>-->
        <span>{{ item.fundName }}</span>
      </el-tag>
    </div>
    <div style="position: relative">
      <table-body-component
        ref="tableBody"
        page-type="smrd"
        :check-array="basicCheckArr"
        :column="column"
        :table-data="tableData"
        :table-loading="tableLoading"
        @focusstatus="handleFocus"
        @checkbox="handleCheckBoxChange"
        @linkto="jumpToSingle"
        @linktomanger="jumpToManger"
        @sorttable="handleSortTable"
      ></table-body-component>
    </div>
    <table-head-component
      :table-column="column"
      :table-column-selector-visible="productSelectDialogVisible"
      @dialogclose="handleCloseDialog"
      @submit="handleSubmit"
    ></table-head-component>
    <focus-dialog :is-show-focus="isShowFocus" :select-row-data="selectRowData" :title="title" @updateFocusStatus="updateFocusStatus"></focus-dialog>
  </div>
</template>

<script>
import tableBodyComponent from '@/components/tableBodyComponentRecommend'
import tableHeadComponent from '@/components/tableHeadComponentRecommend'
import focusDialog from '@/components/Bussiness/focusDialog'
import { deleteAllFocus } from '../scripts/api'

export default {
  name: 'SelectIndexTable',
  components: {
    tableBodyComponent,
    tableHeadComponent,
    focusDialog
  },
  props: {
    titleStr: {
      type: String,
      required: true,
      default: () => {
        return '指数榜单'
      }
    },
    tableData: {
      type: Array,
      required: true,
      default: () => {
        return []
      }
    },
    rankType: {
      tpye: String,
      default: ''
    },
    exportLoading: {
      type: Boolean,
      default: false,
      required: true
    },
    isDisabled: {
      type: Boolean,
      default: false,
      required: true
    },
    tableLoading: {
      type: Boolean,
      required: true,
      default: false
    }
  },
  watch: {
    rankType(val) {
      const iconDescMap = {
        JX: '专注各策略中长期业绩的优质中大规模管理人',
        CZ: '专注成长期业绩爆发力强的中小规模管理人',
        XX: '结合数据定量筛选及公司定性研究部门尽调,综合筛选得到的各策略规模适中,发展潜力巨大的优质机构'
      }
      const frostedGlassMap = {
        JX: `精选指数产品专注各策略中长期业绩的优质中大规模管理人，如需了解具体信息请联系我们!<br/>联系方式：广发证券托管部王经理<br/>电话：0755-82721473<br/>邮箱：wangxuanyun@cmschina.com.cn`,
        CZ: '成长指数产品专注成长期业绩爆发力强的中小规模管理人，如需了解具体信息请联系我们!<br/>联系方式：广发证券托管部王经理<br/>电话：0755-82721473<br/>邮箱：wangxuanyun@cmschina.com.cn',
        XX: ''
      }
      this.iconStr = iconDescMap[val]
      this.frostedStr = frostedGlassMap[val]
    }
  },
  data() {
    return {
      tableHeight: 0,
      iconStr: '',
      frostedStr: '',
      basicCheckArr: [], // 已选产品
      productSelectDialogVisible: false,
      isShowFocus: false,
      title: '关注',
      column: [
        {
          label: '产品代码',
          disabled: true,
          id: 'fundCode',
          type: 'leftTreeData',
          align: 'center',
          fix: 'left',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },
        {
          label: '产品名称',
          id: 'fundFullName',
          disabled: true,
          type: 'leftTreeData',
          align: 'left',
          fix: 'left',
          width: '150px',
          noshowoverflowtooltip: true,
          filter: 'fund',
          sortable: true
        },

        {
          label: '产品管理人',
          id: 'companyFullName',
          disabled: true,
          type: 'leftTreeData',
          align: 'center',
          fix: '',
          width: '150px',
          noshowoverflowtooltip: true,
          filter: 'manager',
          sortable: true
        },
        {
          label: '产品入选日期',
          id: 'rankDate',
          disabled: true,
          type: 'leftTreeData',
          align: 'center',
          fix: '',
          width: '130px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },
        {
          label: '近六月走势',
          id: 'options',
          disabled: true,
          type: 'leftTreeData',
          align: 'center',
          fix: '',
          width: '110px',
          noshowoverflowtooltip: true,
          filter: 'echarts',
          sortable: false
        },
        {
          label: '策略类型',
          id: 'type',
          type: 'leftTreeData',
          align: 'center',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },
        {
          label: '净值日期',
          id: 'navDate',
          type: 'centerTreeDataCenter',
          align: 'left',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },
        {
          label: '近三月收益率',
          id: 'm3_return',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近六月收益率',
          id: 'm6_return',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近一年收益率',
          id: 'y1_return',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '今年以来收益率',
          id: 'ytd_return',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '成立以来收益率',
          id: 'total_return',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        }
      ],
      selectRowData: []
    }
  },
  methods: {
    handleExcelExport() {
      this.$emit('excelexport')
    },
    handleSubmit(arr) {
      this.column = arr
    },
    handleCloseDialog() {
      this.productSelectDialogVisible = false
    },
    handleCheckBoxChange({ row, checked }) {
      if (checked) {
        const index = this.basicCheckArr.findIndex((item) => item.fundCode == row.fundCode)
        if (index === -1) {
          this.basicCheckArr.push(row)
        }
      } else {
        const index = this.basicCheckArr.findIndex((item) => item.fundCode == row.fundCode)
        if (index !== -1) {
          this.basicCheckArr.splice(index, 1)
        }
      }
    },
    // 勾选列表的取消删除逻辑
    handleCloseBasic(item) {
      const index = this.basicCheckArr.findIndex((sitem) => sitem.fundCode === item.fundCode)
      if (index !== -1) {
        this.basicCheckArr.splice(index, 1)
        this.$refs.tableBody.setCheckBoxFalse(item)
      }
    },
    // 页面排序
    handleSortTable(val) {
      this.$emit('sorttable', val)
    },
    /**
     * @description 保存关注关闭弹窗
     * @param { String } status refesh关闭弹窗刷新列表  norefesh仅关闭弹窗
     */
    updateFocusStatus(status) {
      this.isShowFocus = false
      if (status === 'refesh') {
        this.$emit('updatelist')
      }
    },
    /**
     * @description 单个关注/取消关注
     */
    handleFocus(row) {
      if (row.isConcern === '0') {
        this.selectRowData = [row]
        this.isShowFocus = true
      } else {
        // 取消关注
        this.$confirm('此操作将取消该产品所有关注分组, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
        })
          .then(() => {
            const params = {
              fundCode: row.fundCode || '',
              flag: row.source || ''
            }
            deleteAllFocus(params).then((res) => {
              if (res.data.status === 0) {
                this.$message({
                  type: 'success',
                  customClass: 'message-success',
                  message: res.data.message || '取消成功'
                })
                this.$emit('updatelist')
              }
            })
          })
          .catch(() => {
            this.$message({
              type: 'info',
              message: '取消操作'
            })
          })
      }
    },
    /**
     * @description 批量关注
     */
    handleBatchFocus() {
      const _arr = this.basicCheckArr
      if (_arr && _arr.length) {
        this.selectRowData = _arr
        this.isShowFocus = true
        this.title = '批量关注'
      } else {
        this.selectRowData = []
        this.$message({
          type: 'warning',
          customClass: 'message-warning',
          message: '请选择产品'
        })
      }
    },
    /**
     * @description 跳转单产品页面
     */
    jumpToSingle(row) {
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/tqgl/dcpfx',
        query: { list: { fundCode: row.fundCode, source: row.source, fundName: row.fundName } }
      })
    },
    /**
     * @description 跳转管理人详情页面
     */
    jumpToManger(row) {
      let newObj = {
        company_id: row.company_id,
        manager_name: row.companyName
      }
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/tqgl/glrxq',
        query: { managerList: newObj }
      })
    },
    /**
     * @description 跳转多产品页面
     */
    onContrast() {
      const list = this.basicCheckArr
      if (list.length > 5) {
        this.$message.closeAll()
        this.$message({
          type: 'warning',
          customClass: 'message-warning',
          message: '对比产品不能超过5个'
        })
        return
      }
      if (list.length >= 2) {
        this.$store.commit('SET_FROMPAGEJUMP', true)
        this.$router.push({
          path: '/tqgl/smcpxx',
          query: { list: list }
        })
      } else {
        this.$message.closeAll()
        this.$message({
          type: 'warning',
          message: '请至少选择两个产品',
          customClass: 'message-warning'
        })
      }
    }
  }
}
</script>
<style lang="scss" scoped>
.select-index-table {
  margin: 0 20px 0px 16px;
}
.blur {
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  backdrop-filter: blur(10px); /* 调整模糊程度，可以根据需要更改 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.blur-div {
  text-align: center;
  vertical-align: middle;
  width: 492px;
  height: 235px;
  padding: 20px;
  padding-top: 50px;
}

.select-index-table {
  padding-left: 10px;
}
</style>

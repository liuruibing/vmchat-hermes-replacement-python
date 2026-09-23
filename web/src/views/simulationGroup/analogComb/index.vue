<template>
  <div class="anglog-comb" v-auto-enter>
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form :model="formQuery" class="standard-form" inline>
          <el-form-item label="">
            <el-input v-model="formQuery.productName" placeholder="请输入模拟组合名称" size="small"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button size="small" type="primary" @click="onQuery(true)" icon="el-icon-search">查询</el-button>
            <el-button size="small" plain type="info" @click="reset" icon="el-icon-refresh-left">重置</el-button>
            <el-button type="primary" size="small" @click="handleCreateComb">创建模拟组合</el-button>
          </el-form-item>
          <el-form-item style="float: right">
            <el-button size="small" type="info" plain @click="exportData" style="margin-right: 8px">导出EXCEL</el-button>
            <el-checkbox v-model="isGrapMode" style="color:#e9c5a5">图形模式</el-checkbox>
            <!-- <el-button size="small" type="info" @click="exportData" style="margin-left: 10px">导出EXCEL</el-button> -->
          </el-form-item>
        </el-form>
<!--        <ToolBarSlot>
          <template slot="left">
            <el-button type="primary" size="small" @click="handleCreateComb">创建模拟组合</el-button>
          </template>
          <template slot="right">
            <span class="standard-form">
              <el-checkbox v-model="isGrapMode">图形模式</el-checkbox>
              <el-button size="small" type="info" plain @click="exportData" style="margin-left: 8px">导出EXCEL</el-button>
            </span>
          </template>
        </ToolBarSlot>-->
      </div>
    </div>
    <div class="table-content">
      <template v-if="isGrapMode === false">
        <div id="standard-table">
          <div id="standard-table-margin">
            <vxe-table
              ref="refsTable"
              v-loading="tableLoading"
              :cell-style="{ height: '50px' }"
              :data="tableData"
              :height="tableHeight"
              auto-resize
              show-overflow="tooltip"
              stripe=""
              style="width: 100%"
              sync-resize
              resizable
            >
              <template v-for="item in columns">
                <vxe-table-column :key="item.key" :align="item.align" :field="item.prop" :label="item.label" :min-width="item.width" header-align="center">
                  <template slot-scope="scope">
                    <span v-if="item.filter == 'normal'">{{ scope.row[item.prop] | noDataFilter }}</span>
                    <span v-if="item.filter == 'operate'" class="table-operation">
                      <el-button size="small" type="info" plain @click="tiaoCang(scope.row)" :loading="scope.row.tiaoCangLoading">调仓</el-button>
                      <el-button size="small" type="info" plain @click="treeView(scope.row)" :loading="scope.row.treeViewLoading">树形展示</el-button>
                      <el-button size="small" type="info" plain @click="jumpBackTest(scope.row)" :loading="scope.row.jumpBackTestLoading">回测分析</el-button>
                      <el-button size="small" type="info" plain  @click="handleEditData(scope.row)">编辑</el-button>
                      <el-button size="small" type="info" plain @click="deleteData(scope.row)">删除</el-button>
                    </span>
                  </template>
                </vxe-table-column>
              </template>
            </vxe-table>
            <vxe-pager
              :current-page="formQuery.pageNum"
              :page-size="formQuery.pageSize"
              :total="total"
              :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
              border
              class="standard-vxe-pager"
              size="medium"
              @page-change="pagination"
            />
          </div>
<!--          <el-row>
            <div style="display: inline-block; line-height: 56px"></div>
            <Pagination :limit="formQuery.pageSize" :page="formQuery.pageNum" :total="total" @pagination="pagination" />
          </el-row>-->
        </div>
      </template>
      <template v-if="isGrapMode === true">
        <div id="standard-table" style="background-color: #fff !important;margin:10px">
          <div id="standard-table-margin">
            <el-row class="mt10">
              <template v-for="item in tableData">
                <el-col :span="8" :key="item.combineCode">
                  <myChart
                    :id="'ranking' + '' + item.combineCode"
                    :ref="'ranking' + '' + item.combineCode"
                    :options="item.options"
                    resize-dom="cmbfof"
                    style="height: 300px; padding-bottom: 20px;margin-top: 20px"
                  />
                </el-col>
              </template>
            </el-row>
          </div>
          <el-row>
            <div style="display: inline-block; line-height: 56px"></div>
            <vxe-pager
              :current-page="formQuery.pageNum"
              :page-size="formQuery.pageSize"
              :total="total"
              :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
              border
              class="standard-vxe-pager"
              size="medium"
              @page-change="pagination"
            />
<!--            <Pagination :limit="formQuery.pageSize" :page="formQuery.pageNum" :total="total" @pagination="pagination" />-->
          </el-row>
        </div>
      </template>
    </div>
    <el-dialog
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :destroy-on-close="true"
      :visible.sync="isShowEdit"
      title="编辑"
      width="40% !important"
      @close="closeEdit"
    >
      <edit-comb :currentCombRow="currentCombRow" :kpiStandardOpts="kpiStandardOpts" @closeEdit="closeEdit"></edit-comb>
    </el-dialog>
  </div>
</template>
<script>
import Pagination from '@/components/Pagination'
import myChart from '@/components/Echarts'
import pageApi from '@/api/simulationGroup'
import commonApi from '@/api/common'
import { downLoadFileByUrl } from '@/utils'
import EditComb from './components/edit-comb'
import request from '@/utils/request'
import ToolBarSlot from '@/components/toolBarSlot'

export default {
  components: { Pagination, myChart, EditComb, ToolBarSlot },
  data() {
    return {
      that: this,
      isGrapMode: false, // 是否图形模式
      formQuery: {
        productCode: '',
        productName: '',
        pageSize: 10,
        pageNum: 1
      },
      total: 0,
      tiaoCangLoading: false, //查询产品权限的图
      treeViewLoading:false,
      jumpBackTestLoading:false,

      columns: [
        {
          label: '模拟组合名称',
          prop: 'combineName',
          align: 'center',
          width: '220px',
          filter: 'normal'
        },
        {
          label: '成立日期',
          prop: 'foundDate',
          align: 'center',
          width: '80px',
          filter: 'normal'
        },
        {
          label: '业绩基准',
          prop: 'beName',
          align: 'center',
          width: '80px',
          filter: 'normal'
        },
        {
          label: '产品数量',
          prop: 'fundAmount',
          align: 'center',
          width: '80px',
          filter: 'normal'
        },
        {
          label: '创建日期',
          prop: 'createTime',
          align: 'center',
          width: '120px',
          filter: 'normal',
          sortable: true
        },
        {
          label: '操作',
          prop: 'operate',
          align: 'center',
          width: '500px',
          filter: 'operate'
        }
      ],
      tableData: [],
      tableLoading: false,
      isShowEdit: false,
      currentCombRow: null,
      kpiStandardOpts: [],
      tableHeight: 0
    }
  },
  async mounted() {
    await this.getKpiOptions()
    this.onQuery()
    this.handleTableHeight()
  },
  watch: {
    '$route.query.list': {
      handler(val) {
        if (this.$store.getters.fromPageJump && this.$route.path === '/tqgl/mnzh/mnzh') {
          if (val && val.FUNDNAME) {
            this.formQuery.productName = val.FUNDNAME
            this.onQuery(true)
          } else {
            this.onQuery(true)
          }
          this.$store.commit('SET_FROMPAGEJUMP', false)
        }
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    /**
     * @description 查询产品权限
     */
    getProductLimits(code,row,buttonLoading) {
      if (!code) {
        return
      }
      return new Promise((resolve, reject) => {
        let params = {}
        params.indexCode = '1b34d3ac-edbc-4a89-ab3c-1c18e0c46efe'
        params.combineCode = code
        this.$set(row, buttonLoading, true)
        //this.productLimitLoading = true
        commonApi
          .getDataBysqlCode(params)
          .then((res) => {
            let { status, data } = res.data
            this.$set(row, buttonLoading, false);
            //this.productLimitLoading = false
            resolve(data)
          })
          .catch((err) => {
            this.$set(row, buttonLoading, false);
            //this.productLimitLoading = false
            resolve([])
          })
      })
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
          if (this.$refs.refsTable) {
            this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 165
          }
        }
      })
    },
    handleEditData(row) {
      this.isShowEdit = true
      this.currentCombRow = JSON.parse(JSON.stringify(row))
    },
    closeEdit(status) {
      this.isShowEdit = false
      if (status === 'REFESH') {
        this.onQuery()
      }
    },
    /**
     * @description 获取模拟组合 - 业绩基准下拉
     */
    getKpiOptions() {
      return new Promise((resolve, reject) => {
        request({
          url: `/api/report/v1.0/data/sql/d62e680a-5ef8-415e-9764-983d50107d2b`,
          method: 'post',
          data: {
            indexCode: 'd62e680a-5ef8-415e-9764-983d50107d2b'
          }
        })
          .then((res) => {
            if (res.data.status === 0) {
              this.kpiStandardOpts = res.data.data || []
              resolve()
            }
          })
          .catch((err) => {
            reject(err)
          })
      })
    },
    pagination(val) {
      /* const { page, limit } = val
      this.formQuery.pageNum = page
      this.formQuery.pageSize = limit */
      const { currentPage, pageSize } = val;
      // 起始页
      this.formQuery.pageNum  = currentPage;
      // 每页数量
      this.formQuery.pageSize = pageSize;
      this.onQuery()
    },
    handleCreateComb() {
      this.$store.commit('SET_FROMCREATESUMUCOMB', true)
      this.$router.push({
        path: '/tqgl/cjmnzh'
      })
    },
    async tiaoCang(row) {
      let limitsData = await this.getProductLimits(row.combineCode,row,'tiaoCangLoading')
      if (limitsData && limitsData.length != 0) {
        this.$message.closeAll()
        this.$message({
          type: 'warning',
          message: '您无该组合下子基金的托管净值权限请重新选择产品构建组合。',
          customClass: 'message-warning'
        })
        return
      }

      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/tqgl/tc',
        query: {
          type: 'tc',
          combList: { combineCode: row.combineCode, combineName: row.combineName, foundDate: row.foundDate }
        }
      })
    },
    async jumpBackTest(row) {
      let limitsData = await this.getProductLimits(row.combineCode,row,'jumpBackTestLoading')
      if (limitsData && limitsData.length != 0) {
        this.$message.closeAll()
        this.$message({
          type: 'warning',
          message: '您无该组合下子基金的托管净值权限请重新选择产品构建组合。',
          customClass: 'message-warning'
        })
        return
      }
      let beCodeName = this.beCodeValToName(row.beCode)
      if (beCodeName == '') {
        this.$message.closeAll()
        this.$message({
          type: 'warning',
          message: '基准编码不存在，查询回测分析失败',
          customClass: 'message-warning'
        })
        return
      }
      this.$store.commit('SET_FROMPAGEJUMP', true)
      console.log(row, 'row')
      this.$router.push({
        path: '/tqgl/hcfx',
        query: {
          groupList: { combineCode: row.combineCode, combineName: row.combineName, foundDate: row.foundDate },
          beCodeName: beCodeName
        }
      })
    },
    beCodeValToName(code) {
      let name = ''
      for (let i = 0; i < this.kpiStandardOpts.length; i++) {
        let temp = this.kpiStandardOpts[i]
        if (code == temp.DIM_CDE) {
          return temp.DIM_NME
        }
      }
      return ''
    },
    async treeView(row) {
      let limitsData = await this.getProductLimits(row.combineCode,row,'treeViewLoading')
      if (limitsData && limitsData.length != 0) {
        this.$message.closeAll()
        this.$message({
          type: 'warning',
          message: '您无该组合下子基金的托管净值权限请重新选择产品构建组合。',
          customClass: 'message-warning'
        })
        return
      }
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/tqgl/treeView',
        query: {
          type: 'treeView',
          combList: { combineCode: row.combineCode, combineName: row.combineName }
        }
      })
    },
    //查询模拟组合数据
    onQuery(flag) {
      if (flag) {
        this.formQuery.pageNum = 1
      }
      this.tableLoading = true
      let params = {
        combineName: this.formQuery.productName,
        limit: this.formQuery.pageSize,
        offset: (this.formQuery.pageNum - 1) * this.formQuery.pageSize,
        orderString: 'createTime desc'
      }
      pageApi
        .combineSelect(params)
        .then((res) => {
          this.tableLoading = false
          let { data, status, statusText } = res
          if (status === 200) {
            data.rows.forEach((element) => {
              // 同步获取对应的series Data数据，用于组装
              element.options = {}
              pageApi
                .combineSelectNetWorth({
                  combineCode: element.combineCode
                })
                .then((res) => {
                  let { data, status } = res.data
                  if (status === 0) {
                    this.setTableDataOption(data, element)
                  }
                })
                .catch((err) => {})
            })
            this.total = data.total
            this.tableData = data.rows
            // this.$refs.tableData.doLayout()
          } else {
            this.tableData = []
            this.total = 0
            this.$message.closeAll()
            this.$message({
              type: 'warning',
              message: statusText || '查询失败',
              customClass: 'message-warning'
            })
          }
        })
        .catch((err) => {
          this.tableData = []
          this.total = 0
          this.tableLoading = false
          this.$message.closeAll()
          this.$message({
            type: 'error',
            message: '查询失败',
            customClass: 'message-error'
          })
        })
    },
    // 根据fundcode设置对应的option
    setTableDataOption(data, row) {
      const seriesData1 = data.map((item) => item.F_UNITPRICE)
      const seriesData2 = data.map((item) => item.F_BEPRICE)
      const xData = data.map((item) => item.D_DATE)
      let options = {
        title: {
          text: row.combineName
        },
        tooltip: {
          trigger: 'axis',
          formatter: function (params) {
            var relVal = params[0].name
            for (var i = 0, l = params.length; i < l; i++) {
              var value = params[i].value ? params[i].value : 0
              relVal += '<br/>' + params[i].marker + params[i].seriesName + ':' + Math.abs(value.toFixed(2))
            }
            return relVal
          }
        },
        color: ['#44677a', '#da7077'],
        legend: {
          padding: [30, 0, 0, 0]
        },
        grid: {
          top: '28%',
          left: '3%',
          right: '4%',
          bottom: '18%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          axisTick: {
            show: false
          },
          data: xData
        },
        yAxis: {
          type: 'value',
          name: '净值',
          min: 'dataMin', // 根据数据动态设置最小值
          max: 'dataMax', // 根据数据动态设置最大值
          axisLabel: {
            formatter: function (value) {
              // 保留两位有效数字
              return parseFloat(value).toFixed(2)
            }
          },
          axisLine: {
            show: false
          },
          axisTick: {
            show: false
          }
        },
        dataZoom: {
          show: true,
          start: 0,
          height: '20px',
          end: 100
        },
        series: [
          {
            name: row.combineName,
            type: 'line',
            data: seriesData1
          },
          {
            name: row.beName || this.beCodeValToName(row.beCode),
            type: 'line',
            areaStyle: {
              normal: {
                color: '#ef8080'
              }
            },
            data: seriesData2
          }
        ]
      }
      for (let i = 0; i < this.tableData.length; i++) {
        const temp = this.tableData[i]
        if (temp.combineCode === row.combineCode) {
          temp.options = options
          break
        }
      }
    },
    //删除数据
    deleteData(row) {
      this.$confirm('是否确认删除该模拟组合？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          pageApi
            .combineDelete({
              combineCode: row.combineCode
            })
            .then((res) => {
              let { status, message } = res.data
              if (status === 0) {
                this.$message({
                  type: 'success',
                  message: '删除成功',
                  customClass: 'message-success'
                })
                this.onQuery()
              } else {
                this.$message({
                  type: 'warning',
                  message: message || '删除失败',
                  customClass: 'message-warning'
                })
              }
            })
            .catch((err) => {
              this.$message({
                type: 'error',
                message: '删除失败',
                customClass: 'message-error'
              })
            })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消操作'
          })
        })
    },
    //导出数据
    exportData() {
      let params = {
        combineName: this.formQuery.productName,
        orderString: ''
      }
      const fileName = '模拟组合-导出.xls'
      const url = 'api/simulate/combine/export'
      downLoadFileByUrl(url, params, fileName, this)
    },
    // 重置
    reset() {
      this.formQuery.productName = ''
    }
  },
  beforeDestroy() {
    // 组件销毁移除监听事件
    window.onresize = null
  }
}
</script>
<style lang="scss" scoped>
.anglog-comb {
  // padding: 10px 15px;
  margin-bottom: 40px;
  .search-content {
    //background-color: #f7f7f7;
    ::v-deep .el-input.el-input--small .el-input__inner {
      background-color: #f7f7f7;
    }
    ::v-deep .el-form--inline .el-form-item {
      margin-bottom: 0px !important;
    }
  }
  .operate-btn {
    ::v-deep .el-button.el-button--small {
      margin-left: 16px !important;
    }
    ::v-deep .el-button.el-button--info {
      font-weight: bold;
    }
    ::v-deep .el-button.el-button--info:hover {
      font-weight: bold;
    }
  }
  ::v-deep .el-dialog__wrapper .el-dialog__header span {
    color: #333 !important;
  }
  ::v-deep .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
}
::v-deep .el-button--danger {
  color: #F56C6C;
  background-color: #fff;
  border-color: #F56C6C;
}
</style>

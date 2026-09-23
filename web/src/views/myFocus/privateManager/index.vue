<template>
  <el-container>
    <!-- <product-list @getpid="getCurrentId"></product-list> -->
    <group-list-manager @getpid="getCurrentId"></group-list-manager>
    <el-main style="padding-left: 10px !important; overflow-x: hidden">
      <manager-query
        ref="myFocusManagerQuery"
        :page-list="pageList"
        :order-list="orderList"
        :table-loading="tableLoading"
        :current-group-id="currentGroupId"
        @resetPage="resetPageList"
        @updateLoading="getTableLoading"
        @updateTable="getTabelData"
        @updateheight="updateHeight"
      ></manager-query>
      <manager-table
        ref="allTablePrivateManager"
        :current-group-id="currentGroupId"
        :table-data="tableData"
        :table-loading="tableLoading"
        :export-loading="exportLoading"
        :is-disabled="isDisabled"
        @excelexport="handleExcelExport"
        @sorttable="handleSortTable"
        @updatelist="updatelist"
      ></manager-table>
      <el-row style="background-color: #f4f6fa">
        <!-- <div style="display: inline-block; line-height: 56px" class="standard-form">
          <el-button
            type="info"
            plain
            size="small"
            @click="
              () => {
                $refs.allTablePrivateManager.handleCancelBatchFocus()
              }
            "
          >
            取消关注
          </el-button>
          <el-button
            size="small"
            plain
            type="info"
            @click="
              () => {
                $refs.allTablePrivateManager.removeGroup()
              }
            "
          >
            移动分组
          </el-button>
          <el-button
            :disabled="isDisabled"
            :icon="exportLoading ? 'el-icon-loading' : ''"
            type="info"
            plain
            size="small"
            @click="
              () => {
                $refs.allTablePrivateManager.handleExcelExport()
              }
            "
          >
            导出Excel
          </el-button>
          <el-button
            type="info"
            plain
            size="small"
            @click="
              () => {
                $refs.allTablePrivateManager.productSelectDialogVisible = true
              }
            "
          >
            自定义指标
          </el-button>
        </div> -->
        <Pagination :limit="pageList._pageSize" :page="pageList._pageNum" :total="total" @pagination="pagination" />
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
import productList from '../components/productListManager'
import GroupListManager from '../components/group-list-manager'
import managerQuery from './components/searchQuery'
import managerTable from './components/managerTable'
import Pagination from '@/components/Pagination'
import commonApi from '@/api/common'
import { downLoadFileByUrl, merger_back_objs } from '@/utils'
export default {
  components: { productList, managerQuery, managerTable, Pagination, GroupListManager },
  data() {
    return {
      tableLoading: false,
      tableData: [],
      pageList: {
        _pageNum: 1,
        _pageSize: 20
      },
      total: 0,
      currentGroupId: '000000',
      orderList: {
        orderString: ''
      },
      exportLoading: false,
      isDisabled: false
    }
  },
  methods: {
    updateHeight() {
      this.$refs.allTablePrivateManager.$refs.tableBody.handleTableHeightMyFocus()
    },
    /**
     * @description 获取echarts图数据
     */
    getEchartsData() {
      // this.tableData.forEach(temp => {
      //   let paramsC = {}
      //   paramsC.indexCode = 'c4441b43-8bed-4a26-9206-c8ecdb5bfa96'
      //   paramsC.mgrcode = temp.company_id
      //   commonApi.getDataBysqlCode(paramsC).then(resC => {
      //     let { status: statusC, data: dataC } = resC.data
      //     if (statusC === 0) {
      //       if (temp.m6_return > 0) {
      //         this.setTableDataOption(dataC, temp.company_id, ['#de777a'])
      //       } else if (temp.m6_return < 0) {
      //         this.setTableDataOption(dataC, temp.company_id, ['#81b59e'])
      //       } else {
      //         this.setTableDataOption(dataC, temp.company_id, ['black'])
      //       }
      //       // 组装好之后放到原来的数组里面去
      //     } else {
      //     }
      //   })
      // })
      let mgrcodes = []
      this.tableData.forEach((temp) => {
        mgrcodes.push(temp.company_id)
      })
      let paramsC = {}
      paramsC.indexCode = 'c4441b43-8bed-4a26-9206-c8ecdb5bfa96'
      paramsC.mgrcodes = mgrcodes.join(',')
      commonApi.getDataBysqlCode(paramsC).then((resC) => {
        let { status: statusC, data: dataC } = resC.data
        if (statusC === 0) {
          const mergeData = merger_back_objs(dataC, 'COMPANY_ID')
          this.tableData.forEach((temp) => {
            let findObj = mergeData.find((item) => item.COMPANY_ID == temp.company_id)
            if (findObj) {
              if (temp.m6_return > 0) {
                this.setTableDataOption(findObj.origin, findObj.COMPANY_ID, ['#de777a'])
              } else if (temp.m6_return < 0) {
                this.setTableDataOption(findObj.origin, findObj.COMPANY_ID, ['#81b59e'])
              } else {
                this.setTableDataOption(findObj.origin, findObj.COMPANY_ID, ['black'])
              }
            }
          })
          // 组装好之后放到原来的数组里面去
        } else {
        }
      })
    },

    // 根据fundcode设置对应的option
    setTableDataOption(data, fundCode, color) {
      const seriesData = data.map((item) => item.F_CURVE_NAV)
      const xData = data.map((item) => item.D_END_DATE)
      // 开始组装option
      let option = {
        color: color,
        grid: {
          // 设置图表四周留白间距
          top: '10%',
          right: '2%',
          bottom: '10%',
          left: '4%'
        },
        xAxis: {
          show: false,
          type: 'category',
          boundaryGap: false, // 设置x轴两边的留白
          axisTick: {
            // x轴刻度尺
            show: false
          },
          axisLine: {
            // x轴线条颜色
            lineStyle: {
              color: '#999'
            }
          },
          data: xData
        },
        yAxis: {
          show: false,
          type: 'value',
          interval: 1, // 刻度值间隔值
          splitLine: {
            // 网格线
            show: false // 关闭网格线
          },
          min: function (value) {
            if (value.min < 0) {
              return value.min * 1.1
            } else {
              return value.min
            }
          },
          max: function (value) {
            if (value.max > 0) {
              return value.max
            } else {
              return value.max * 0.9
            }
          },
          axisLine: {
            // y轴线条颜色
            show: true,
            lineStyle: {
              color: '#999'
            }
          }
        },
        series: [
          {
            data: seriesData,
            type: 'line',
            smooth: true, // 面积图改成弧形状
            showSymbol: false // 去除面积图节点圆
          }
        ]
      }
      for (let i = 0; i < this.tableData.length; i++) {
        const temp = this.tableData[i]
        if (temp.company_id === fundCode) {
          this.$set(temp, 'option', option)
          break
        }
      }
    },

    // 页面导出
    handleExcelExport() {
      // 获取当前查询条件
      let params = this.$refs.myFocusManagerQuery.getParamsObject()
      params = this.parameterSrc(params)
      const fileName = '我的关注（管理人）-导出.xls'
      const url = '/api/manager/concern/export'
      this.exportLoading = true
      this.isDisabled = true
      downLoadFileByUrl(url, params, fileName, this)
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
     * @description 获取分组code
     */
    getCurrentId(id) {
      this.currentGroupId = id
    },
    /**
     * @description 回传表格loading状态
     */
    getTableLoading(flag) {
      this.tableLoading = flag
    },
    /**
     * @description 回传表格数据
     */
    getTabelData(table) {
      this.tableData = table.rows
      this.total = table.total
      this.getEchartsData()
    },

    /**
     * @description 回传重置分页
     */
    resetPageList() {
      this.pageList._pageNum = 1
    },
    /**
     * @description 监听分页
     */
    pagination(val) {
      const { page, limit } = val
      this.pageList._pageNum = page
      this.pageList._pageSize = limit
      this.$refs.myFocusManagerQuery.handleQueryParams()
    },
    /**
     * @description 设置排序字段
     */
    handleSortTable(val) {
      this.orderList.orderString = this.$fun.queryOrderBy_vxe_template(val)
      this.$refs.myFocusManagerQuery.handleQueryParams()
    },
    /**
     * @description 关注完刷新列表
     */
    updatelist() {
      this.$refs.myFocusManagerQuery.handleQueryParams()
    }
  }
}
</script>

<style></style>

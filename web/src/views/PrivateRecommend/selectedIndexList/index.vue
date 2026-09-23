<template>
  <div class="select-index-list">
    <select-index-query
      ref="selectIndexQuery"
      :page-list="pageList"
      :order-list="orderList"
      :rank-type="rankType"
      @updateLoading="getTableLoading"
      @updateTable="getTabelData"
      @resetPage="resetPageList"
    ></select-index-query>
    <select-index-table
      ref="selectIndexTable"
      :table-data="tableData"
      :table-loading="tableLoading"
      :export-loading="exportLoading"
      :is-disabled="isDisabled"
      :rank-type="rankType"
      :title-str="titleStr"
      @updatelist="updatelist"
      @sorttable="handleSortTable"
      @excelexport="handleExcelExport"
    ></select-index-table>
    <el-row>
      <Pagination :limit="pageList._pageSize" :page="pageList._pageNum" :total="total" @pagination="pagination" />
    </el-row>
    <!-- <el-row style="padding-left: 25px">
      <div style="display: inline-block; line-height: 56px" class="standard-form">
        <el-button
          size="small"
          type="info"
          plain
          @click="
            () => {
              $refs.selectIndexTable.onContrast()
            }
          "
        >
          对比
        </el-button>
        <el-button
          size="small"
          type="info"
          plain
          @click="
            () => {
              $refs.selectIndexTable.handleBatchFocus()
            }
          "
        >
          批量关注
        </el-button>
        <el-button
          :disabled="isDisabled"
          :icon="exportLoading ? 'el-icon-loading' : ''"
          size="small"
          type="info"
          plain
          @click="
            () => {
              $refs.selectIndexTable.handleExcelExport()
            }
          "
        >
          导出Excel
        </el-button>
        <el-button
          size="small"
          type="info"
          plain
          @click="
            () => {
              $refs.selectIndexTable.productSelectDialogVisible = true
            }
          "
        >
          自定义指标
        </el-button>
      </div>
      <Pagination :limit="pageList._pageSize" :page="pageList._pageNum" :total="total" @pagination="pagination" />
    </el-row> -->
    <!--    <div class="blur" v-show="rankType !== 'XX'">-->
    <!--      <div class="blur-div" :style="{ backgroundImage: 'url(' + require('@/assets/img/frostedGlassPageBg.png') + ')' }">-->
    <!--        <el-container>-->
    <!--          <el-aside width="23px">-->
    <!--            <img width="23px" :src="require('@/assets/img/frostedGlassLogo.png')" />-->
    <!--          </el-aside>-->
    <!--          <el-main style="text-align: left;line-height: 24px;padding-left: 5px!important;font-size: 14px;" v-html="frostedStr"></el-main>-->
    <!--        </el-container>-->
    <!--      </div>-->
    <!--    </div>-->
  </div>
</template>

<script>
import SelectIndexQuery from './components/searchQuery'
import SelectIndexTable from './components/selectIndexTable'
import Pagination from '@/components/Pagination'
import { downLoadFileByUrl } from '@/utils'
import commonApi from '@/api/common'
import { merger_back_objs } from '@/utils'
export default {
  components: {
    SelectIndexQuery,
    SelectIndexTable,
    Pagination
  },
  data() {
    return {
      tableLoading: false,
      tableData: [],
      exportLoading: false,
      isDisabled: false,
      orderList: {
        orderString: 'm3_return desc'
      },
      pageList: {
        _pageNum: 1,
        _pageSize: 20
      },
      total: 0,
      rankType: '',
      titleStr: '热点产品',
      hotProductArr: [],
      iconStr: '',
      frostedStr: ''
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
  mounted() {
    if (this.$route.params && this.$route.params.id && this.$route.params.title) {
      this.titleStr = this.$route.params.title
      this.rankType = this.$route.params.id
    } else {
      this.fromMenuClick()
    }
  },
  methods: {
    // 如果是从菜单点击过来的
    async fromMenuClick() {
      await this.getHotProduct()
      let array = this.$route.path.split('/')
      let str = array[array.length - 1]
      for (let i = 0; i < this.hotProductArr.length; i++) {
        let temp = this.hotProductArr[i]
        // 菜单配置的编码存在库中
        if (str === temp.value) {
          this.rankType = temp.value
          this.titleStr = temp.label
          break
        }
      }
    },

    // 获取热点产品数据
    getHotProduct() {
      return new Promise((resolve, reject) => {
        let params = {}
        params.indexCode = '24a00f6b-81ce-46c0-8f12-48c721d9b5ff'
        commonApi
          .getDataBysqlCode(params)
          .then((res) => {
            let { status, data } = res.data
            if (status === 0) {
              if (data && data instanceof Array && data.length > 0) {
                this.hotProductArr = []
                let temp = []
                data.forEach((item) => {
                  let obj = {}
                  obj.label = item.DIM_NME
                  obj.value = item.DIM_CDE
                  temp.push(obj)
                })
                this.hotProductArr = temp
              }
            }
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
    },

    pagination(val) {
      const { page, limit } = val
      this.pageList._pageNum = page
      this.pageList._pageSize = limit
      this.$refs.selectIndexQuery.handleQueryList()
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
     * @description 获取echarts图数据
     */
    // getEchartsData() {
    //   console.log(this.table)
    //   let fundCodes = [];
    //   this.tableData.forEach(temp => {
    //     fundCodes.push(temp.fundCode)
    //   })
    //   this.tableData.forEach(temp => {
    //     const paramsC = {}
    //     paramsC.indexCode = 'a50f06a4-bfa6-4858-9c38-a1d0f57e5a51'
    //     paramsC.fundCode = temp.fundCode
    //     commonApi.getDataBysqlCode(paramsC).then(resC => {
    //       const { status: statusC, data: dataC } = resC.data
    //       if (statusC === 0) {
    //         if (temp.m3_return > 0) {
    //           this.setTableDataOption(dataC, temp.fundCode, ['#de777a'])
    //         } else if (temp.m3_return < 0) {
    //           this.setTableDataOption(dataC, temp.fundCode, ['#81b59e'])
    //         } else {
    //           this.setTableDataOption(dataC, temp.fundCode, ['black'])
    //         }
    //         // 组装好之后放到原来的数组里面去
    //       } else {
    //       }
    //     })
    //   })
    // },
    getEchartsData() {
      let fundList = []
      this.tableData.forEach((temp) => {
        fundList.push({
          dimNme: temp.type,
          fundCode: temp.fundCode
        })
      })
      let paramsC = {}
      paramsC.indexCode = '2010917d-0cbe-469d-a7a2-4c984aadfa42'
      paramsC.fundList = fundList
      commonApi.getDataBysqlCode(paramsC).then((resC) => {
        let { status: statusC, data: dataC } = resC.data
        if (statusC === 0) {
          const mergeData = merger_back_objs(dataC, 'VC_FUNDCODE')
          this.tableData.forEach((temp) => {
            let findObj = mergeData.find((item) => item.VC_FUNDCODE == temp.fundCode + temp.type)
            if (findObj) {
              if (temp.m6_return > 0) {
                this.setTableDataOption(findObj.origin, findObj.VC_FUNDCODE, ['#de777a'])
              } else if (temp.m6_return < 0) {
                this.setTableDataOption(findObj.origin, findObj.VC_FUNDCODE, ['#81b59e'])
              } else {
                this.setTableDataOption(findObj.origin, findObj.VC_FUNDCODE, ['black'])
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
      const seriesData = data.map((item) => item.F_ADDED_NAV)
      const xData = data.map((item) => item.D_DATE)
      // 开始组装option
      const option = {
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
        if (temp.fundCode + temp.type === fundCode) {
          this.$set(temp, 'option', option)
          break
        }
      }
    },
    /**
     * @description 回传重置分页
     */
    resetPageList() {
      this.pageList._pageNum = 1
    },
    /**
     * @description 关注完刷新列表
     */
    updatelist() {
      this.$refs.selectIndexQuery.handleQueryList()
    },
    /**
     * @description 设置排序字段
     */
    handleSortTable(val) {
      this.orderList.orderString = this.$fun.queryOrderBy_vxe_template(val)
      if (val.order) {
        this.$refs.selectIndexQuery.handleQueryList()
      }
    },
    /**
     * @description 导出excel
     */
    handleExcelExport() {
      // 获取当前查询条件
      const params = this.$refs.selectIndexQuery.getParamster()
      delete params.offset
      delete params.limit
      const fileName = `${this.$route.meta.title}-导出.xls`
      const url = 'api/fund2/rank/export'
      this.exportLoading = true
      this.isDisabled = true
      downLoadFileByUrl(url, params, fileName, this)
    }
  }
}
</script>

<style lang="scss" scoped>
.select-index-list {
  position: relative;
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
}
</style>

<!--
 * @Description:
 * @Author:
 * @Date: 2024-07-11 13:35:18
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2024-07-15 15:35:27
-->
<template>
  <div class="warningMonitoringResults">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form :inline="true" ref="formInline" :model="formInline" class="standard-form">
          <el-row>
            <el-col :span="20">
              <el-form-item label="" prop="date">
                <el-date-picker
                  v-model="formInline.date"
                  start-placeholder="业务开始日期"
                  range-separator="至"
                  end-placeholder="业务结束日期"
                  size="small"
                  type="daterange"
                  value-format="yyyy-MM-dd"
                ></el-date-picker>
              </el-form-item>
              <el-form-item label="" prop="warnStatus">
                <el-select v-model="formInline.warnStatus" size="small" clearable filterable placeholder="触发状态">
                  <el-option v-for="item in warnStatusList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </el-select>
              </el-form-item>
              <el-form-item label="" prop="warnLevel">
                <el-select v-model="formInline.warnLevel" size="small" clearable filterable placeholder="风险等级">
                  <el-option v-for="item in warnLevelList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </el-select>
              </el-form-item>
              <el-form-item label="" prop="ittype">
                <el-select v-model="formInline.ittype" size="small" clearable filterable placeholder="监控对象类型">
                  <el-option v-for="item in ittypeList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </el-select>
              </el-form-item>
              <el-form-item label="" prop="sendemail">
                <el-select v-model="formInline.sendemail" size="small" clearable filterable placeholder="邮件提醒">
                  <el-option v-for="item in sendemailList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </el-select>
              </el-form-item>
              <el-form-item label="" prop="objname">
                <el-input v-model="formInline.objname" size="small" placeholder="监控对象代码/名称"></el-input>
              </el-form-item>
              <el-form-item label="" prop="mgrname">
                <el-input v-model="formInline.mgrname" size="small" placeholder="管理人名称"></el-input>
              </el-form-item>
              <el-form-item label="" prop="rulesname">
                <el-input v-model="formInline.rulesname" size="small" placeholder="监控规则名称"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item style="float: right">
                <el-button type="primary" size="small" icon="el-icon-search" @click="handleSearchTable(true)">查询</el-button>
                <el-button size="small" plain type="info" :icon="exportIcon2" :disabled="exportButton2" @click="exportData">{{ exportText2 }}</el-button>
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
              <span v-if="item.format === 'dict'" :style="{ color: transf(`${row[item.prop]}_color`, item.prop) }">
                <el-tag size="mini" type="danger" v-if="row[item.prop] == '预警' || row[item.prop] == '高'">{{ transf(row[item.prop], item.prop) || '-' }}</el-tag>
                <el-tag size="mini" type="warning" v-else-if="row[item.prop] == '中'">{{ transf(row[item.prop], item.prop) || '-' }}</el-tag>
                <el-tag size="mini" type="success" v-else>{{ transf(row[item.prop], item.prop) || '-' }}</el-tag>
              </span>
              <span v-else>{{ row[item.prop] | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column label="详情" align="center" width="240px" fixed="right">
            <template slot-scope="{ row }">
              <span class="table-operation">
                <el-button type="info" plain size="small" @click="openGzDetails(row)">规则详情</el-button>
                <el-button type="info" plain size="small" @click="openJkDetails(row)">监控详情</el-button>
              </span>
            </template>
          </vxe-table-column>
        </vxe-table>
      </div>
    </div>
    <div class="table-footer">
      <Pagination :total="total" :limit="formInline.pageSize" :page="formInline.pageNum" @pagination="pagination" />
    </div>

    <gzDetailsDialog ref="gzDetailRef" v-if="gzDetailShow" @close="gzDetailShow = false"></gzDetailsDialog>
    <jkDetailsDialog ref="jkDetailRef" v-if="jkDetailShow" @close="jkDetailShow = false"></jkDetailsDialog>
  </div>
</template>

<script>
import CONSTANTS from './scripts/constants'
import CONSTANTSRule from '@/views/warningMonitoring/rules/scripts/constants'
import Pagination from '@/components/Pagination'
import { downLoadFileByUrlPost } from '@/utils'
import pageApi from './scripts/api.js'
import commonFun from '@/filters/common'
import gzDetailsDialog from './components/gzDetailsDialog.vue'
import jkDetailsDialog from './components/jkDetailsDialog.vue'
export default {
  name: 'warningMonitoringResults',
  components: {
    Pagination,
    gzDetailsDialog,
    jkDetailsDialog
  },
  data() {
    return {
      that: this,
      // form表单绑定
      formInline: {
        date: [],
        warnStatus: '',
        warnLevel: '',
        ittype: '',
        sendemail: '',
        orderString: '',
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
      // 分页信息
      pageList: {
        _pageSize: 20,
        _pageNum: 1,
        _pageFlag: true
      },
      // 总条数
      total: 0,
      // 触发状态选项
      warnStatusList: CONSTANTS.warnStatusList,
      warnStatusMap: {},
      // 风险等级选项
      warnLevelList: CONSTANTS.warnLevelList,
      warnLevelMap: {},
      // 监控对象类型
      ittypeList: CONSTANTS.ittypeList,
      ittypeMap: {},
      // 邮件提醒选项
      sendemailList: CONSTANTS.sendemailList,
      sendemailMap: {},
      // 新增 | 编辑状态
      isEdit: false,
      exportButton2: false, // 导出
      exportIcon2: 'el-icon-download',
      exportText2: '导出',
      gzDetailShow: false,
      jkDetailShow: false
    }
  },
  computed: {
    transf() {
      return (val, type) => {
        if (!(val || val === 0)) return
        if (type === 'warnStatus') {
          return this.warnStatusMap[val] || val
        }
        if (type === 'warnLevel') {
          return this.warnLevelMap[val] || val
        }
        if (type === 'sendemail') {
          return this.sendemailMap[val] || val
        }
      }
    }
  },
  mounted() {
    this.initData()
  },
  methods: {
    /**
     * @description 初始化数据
     */
    initData() {
      this.setDictMap()
      // 动态设置表格高度
      this.handleTableHeight()
      // 查询表格
      this.handleSearchTable(true)
    },
    setDictMap() {
      this.warnStatusList.forEach((item) => {
        this.$set(this.warnStatusMap, item.dimCde, item.dimNme)
        this.$set(this.warnStatusMap, `${item.dimCde}_color`, item.color)
      })
      this.warnLevelList.forEach((item) => {
        this.$set(this.warnLevelMap, item.dimCde, item.dimNme)
        this.$set(this.warnLevelMap, `${item.dimCde}_color`, item.color)
      })
      this.ittypeList.forEach((item) => {
        this.$set(this.ittypeMap, item.dimCde, item.dimNme)
      })
      this.sendemailList.forEach((item) => {
        this.$set(this.sendemailMap, item.dimCde, item.dimNme)
      })
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
        this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 185
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 185
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
      if (this.formInline.date && this.formInline.date.length) {
        params.beginDate = this.formInline.date[0]
        params.endDate = this.formInline.date[1]
      } else {
        params.beginDate = ''
        params.endDate = ''
      }
      delete params.date
      params = this.parameterSrc(params)
      this.tableLoading = true
      pageApi.warnResultList(params).then((res) => {
        this.tableLoading = false
        const { data, status } = res.data
        if (status === 0 && data) {
          this.tableData = data.list || []
          this.total = data.total || 0
        } else {
          this.tableData = []
          this.total = 0
        }
      })
    },
    //导出数据
    exportData() {
      this.exportButton2 = true
      this.exportIcon2 = 'el-icon-loading'
      this.exportText2 = '导出数据中...'
      const params = Object.assign({}, this.formInline)
      if (this.formInline.date && this.formInline.date.length) {
        params.beginDate = this.formInline.date[0]
        params.endDate = this.formInline.date[1]
      } else {
        params.beginDate = ''
        params.endDate = ''
      }
      delete params.date
      const fileName = '预警结果列表-导出.xls'
      const url = '/api/afterManage/warnResult/export'
      downLoadFileByUrlPost(url, params, fileName, this)
      setTimeout(() => {
        this.exportButton2 = false
        this.exportIcon2 = 'el-icon-download'
        this.exportText2 = '导出'
      }, 10000)
    },
    /**
     * @description 监听分页
     */
    pagination(val) {
      let { page, limit } = val
      this.formInline.pageNum = page
      this.formInline.pageSize = limit
      this.handleSearchTable(false)
    },
    // 排序的公共方法
    customSortMethod(val) {
      this.formInline.orderString = commonFun.queryOrderBy_vxe_template(val)
      this.handleSearchTable(false)
    },
    // 规则详情
    openGzDetails(row) {
      const ittypeList = CONSTANTSRule.ittypeList
      const ittypeMap = {}
      ittypeList.forEach((item) => {
        ittypeMap[item.dimCde] = item.dimNme
      })
      this.gzDetailShow = true
      this.$nextTick(() => {
        this.$refs.gzDetailRef.init({ ...row, ittypeStr: ittypeMap[row.ittype] || '' })
      })
    },
    // 监控详情
    openJkDetails(row) {
      this.jkDetailShow = true
      this.$nextTick(() => {
        this.$refs.jkDetailRef.init(row)
      })
    }
  },
  beforeDestroy() {
    // 组件销毁移除监听事件
    window.onresize = null
  }
}
</script>

<style lang="scss" scoped>
.warningMonitoringResults {
  // padding: 10px;
  .search-bar {
    // border-bottom: 1px solid #e1e0e0;
  }
  ::v-deep .el-form-item {
    margin-bottom: 0;
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
</style>
<style>
.customClass .el-dialog__body .edit-product .el-form {
  width: 100% !important;
}
</style>

<template>
  <div class="data-import-gzb-detail-log">
    <el-form  ref="formData"   class="standard-form" label-width="auto">
      <el-row>

        <el-col :span="8">
          <el-form-item label="上传时间">
            {{formData.uploadTime}}
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="上传人">
            {{formData.vcOperator}}
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="文件名">
            {{formData.vcFilenameOld}}
          </el-form-item>
        </el-col>

      </el-row>
      <el-row>
        <el-col :span="16">
          <div style="vertical-align: middle;display: inline-block">
            <div class="color-box"></div>
          </div>
          <span class="title-style">估值文件内容</span>
        </el-col>
        <el-col :span="8">
          <div style="float: right">
            <vxe-toolbar ref="tableToolbar" class="standard-vxe-toolbar" :custom="{ immediate: true }" custom />
          </div>
        </el-col>
      </el-row>
      <div id="standard-table-margin">
      <vxe-table
        ref="refsTable"
        :cell-style="{ height: '50px' }"
        :data="tableData"
        auto-resize
        stripe
        sync-resize
        show-overflow="tooltip"
        :sort-config="{ remote: true }"
        style="width: 100%;"
        height="400"
        resizable
        @sort-change="customSortMethod"
      >
        <vxe-table-column
          v-for="(item, index) in column"
          :key="item.prop + index"
          :align="item.align"
          :field="item.prop"
          :show-overflow-tooltip="item.showtooltip"
          :title="item.title"
          :min-width="item.width"
          header-align="center"
          :sortable="item.sortable"
        >
          <template slot-scope="scope">
            <span>{{ scope.row[item.prop] | noDataFilter }}</span>
          </template>
        </vxe-table-column>


      </vxe-table>
        <el-row>
        <div id="data-import-gzb-detail-log" class="table-footer">
          <Pagination :total="total" :limit="pageList._pageSize" :page="pageList._pageNum" @pagination="pagination" />
        </div>
        </el-row>
      </div>
    </el-form>
  </div>

</template>

<script>
import Pagination from '@/components/Pagination'
import commonFun from '@/filters/common.js'
import {  TABLE_DATA_IMPORT_GZB_DETAIL_LOG_COLUMNS } from '../scripts/constants'
import { queryGzbFileData } from '../scripts/api'



export default {
  name: 'dataImportGzbDetailLog',
  components: {
    Pagination
  },
  props: {
    curImportFileRow: {
      type: Object,
      default: () => {}
    }

  },
  watch: {
    curImportFileRow: {
      handler(val) {
        if (val) {
            for (const key in this.formData) {
            this.formData[key] = val[key]
            }

        }
      },
      deep: true,
      immediate: true
    }
  },
  mounted() {
    this.formInline.fileGroup=this.formData.fileGroup+".file"
    this.formInline.gzDate=this.formData.busiDate
    this.formInline.fundCode=this.formData.vcFundcode
    this.initData()
    this.$refs.refsTable.connect(this.$refs.tableToolbar)
  },

  data() {

    return {
      that: this,

      formInline:{
        fileGroup:'',
        gzDate:'',
        fundCode:'',
      },
      // form表单绑定
      formData: {
        uploadTime:'',
        vcOperator:'',
        vcFilenameOld:'',
        fileGroup:'',
        busiDate:'',
        vcFundcode:'',

      },
      // 总条数
      total: 0,
      // 表格loading
      tableLoading: false,
      // 表格数据
      tableData: [
      ],
      // 表格数据
      // 表格列
      column: TABLE_DATA_IMPORT_GZB_DETAIL_LOG_COLUMNS,
      // 分页信息
      pageList: {
        _pageSize: 20,
        _pageNum: 1,
        _pageFlag: true
      },


    }
  },
  methods: {

    /**
     * @description 初始化数据
     */
    initData() {
      // 查询表格
      this.handleSearchTable()
    },

    /**
     * @description 监听分页
     */
    pagination(val) {
      const { page, limit } = val
      this.pageList._pageNum = page
      this.pageList._pageSize = limit
      this.handleSearchTable()
    },
    // 排序的公共方法
    customSortMethod(val) {
      this.formInline.orderString = commonFun.queryOrderBy_vxe_template(val)
      this.handleSearchTable(false)
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
     * @description 表格查询
     */
    handleSearchTable() {
      const params = Object.assign({}, this.formInline)

      params.limit = this.pageList._pageSize
      params.offset = (this.pageList._pageNum - 1) * this.pageList._pageSize
      const data = this.parameterSrc(params)
      // console.log("data:"+JSON.stringify(data))
      this.tableLoading = true
      this.tableData = []
      queryGzbFileData(data)
        .then((res) => {
          if (res.data.status === 200) {
            this.tableData = res.data.data.rows || []
            console.log('tableData', this.tableData)
            this.total = res.data.data.total || 0
            this.tableLoading = false
          } else {
            this.tableLoading = false
            this.$message({
              type: 'error',
              message: res.data.message || '查询失败',
              customClass: 'message-error'
            })
          }
        })
        .catch((e) => {
          this.tableLoading = false
        })
    },





  }
}
</script>

<style lang="scss" scoped>


</style>

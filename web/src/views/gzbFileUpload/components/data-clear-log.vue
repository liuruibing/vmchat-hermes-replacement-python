<template>

  <div class="data-clear-log">
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
        <div class="page-model-title">
          <div class="title-icon">
            <div class="color-box"></div>
          </div>
          <div class="title-txt">
            筛选
          </div>
        </div>
      </el-row>
      <el-row>
        <div class="standard-form-margin">
          <div class="inner-margin">
            <el-form ref="formInline" class="standard-form" :inline="true" :model="formInline">
              <el-row>
                <el-col :span="24">
                  <el-form-item label="产品代码">
                    <el-input v-model="formInline.fundCode" clearable size="small" placeholder="请输入产品代码"></el-input>
                  </el-form-item>

                  <el-form-item label="产品名称">
                    <el-input v-model="formInline.fundName" clearable size="small" placeholder="请输入产品名称"></el-input>
                  </el-form-item>

                  <el-form-item label="执行状态">
                    <el-select v-model="formInline.vcRunStatus" size="small" clearable filterable placeholder="请选择执行状态">
                      <el-option v-for="item in vcRunStatusOptions" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                    </el-select>
                  </el-form-item>

                  <el-form-item label="执行结果">
                    <el-select v-model="formInline.vcResultFlag" size="small" clearable filterable placeholder="请选择执行状态">
                      <el-option v-for="item in vcResultFlagOptions" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                    </el-select>
                  </el-form-item>
                  <el-form-item>

                  <el-button type="primary" size="small" icon="el-icon-search" @click="handleSearchTable">查询</el-button>
                  </el-form-item>
                </el-col>
              </el-row>
            </el-form>
          </div>
        </div>
      </el-row>
      <el-row>
        <el-col :span="16">
          <div style="vertical-align: middle;display: inline-block">
            <div class="color-box"></div>
          </div>
          <span class="title-style">数据处理日志</span>
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
            <span v-if="item.prop === 'vcRunStatus'">
                    <span v-if="scope.row.vcRunStatus == 'UNDO' ">未执行</span>
                    <span v-else-if="scope.row.vcRunStatus == 'RUNNING' ">正在执行中</span>
                    <span v-else-if="scope.row.vcRunStatus == 'COMPLETED' ">已完成</span>
                    <span v-else>-</span>

            </span>

            <span v-else-if="item.prop === 'vcResultFlag'">
                    <span v-if="scope.row.vcResultFlag == '0'">执行成功</span>
                    <span v-else-if="scope.row.vcResultFlag == '1'" style="color:red">执行失败</span>
                    <span v-else>-</span>

            </span>


            <span v-else>{{ scope.row[item.prop] | noDataFilter }}</span>
          </template>
        </vxe-table-column>
        <vxe-table-column title="明细" align="center" width="100px" fixed="right">
          <template slot-scope="scope">
             <span class="table-operation">
                <el-button type="info" size="small" @click="handleGzbDataClearDetailLog(scope.row)">查看</el-button>
             </span>
          </template>
        </vxe-table-column>



      </vxe-table>
        <el-row>
        <div id="dataClearLog" class="table-footer">
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
import { VC_RUN_STATUS_OPTIONS, VC_RESULT_FLAG_OPTIONS, TABLE_DATA_CLEAR_LOG_COLUMNS } from '../scripts/constants'
import { queryDataClearLogTableList } from '../scripts/api'
import DataDetailLog from './data-detail-log'



export default {
  name: 'dataClearLog',
  components: {
    DataDetailLog,
    Pagination
  },
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    curGzbFileUploadLogConfigRow: {
      type: Object,
      default: () => {}
    }

  },
  watch: {
    curGzbFileUploadLogConfigRow: {
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
    this.initData()
    this.$refs.refsTable.connect(this.$refs.tableToolbar)
  },

  data() {

    return {
      that: this,
      vcRunStatusOptions:VC_RUN_STATUS_OPTIONS,
      vcResultFlagOptions:VC_RESULT_FLAG_OPTIONS,
      formInline:{
        fundCode:'',
        fundName:'',
        vcRunStatus:'',
        vcResultFlag:'',
        orderString: '',
        fileGroup:''
      },
      // form表单绑定
      formData: {
        uploadTime:'',
        vcOperator:'',
        vcFilenameOld:'',
        fileGroup:'',

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
      column: TABLE_DATA_CLEAR_LOG_COLUMNS,
      // 分页信息
      pageList: {
        _pageSize: 20,
        _pageNum: 1,
        _pageFlag: true
      },

      // 模板配置弹窗标题
      dialogDetailTitle: '',
      // 模板配置弹窗状态
      dialogDetailVisible: false,

      // 当前行数据
      curDataClearLogRow: {},



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

    // 排序的公共方法
    customSortMethod(val) {
      this.formInline.orderString = commonFun.queryOrderBy_vxe_template(val)
      this.handleSearchTable(false)
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
      queryDataClearLogTableList(data)
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



    /**
     * @description 日志明细
     */
    handleGzbDataClearDetailLog(row) {
      this.dialogDetailTitle = '日志明细'
      this.dialogDetailVisible = true
      this.curDataClearLogRow = JSON.parse(JSON.stringify(row))
      // 触发一个名为'handleDetailData'的事件，并传递数据
      this.$emit('handleDetailData', this.dialogDetailTitle,this.dialogDetailVisible,this.curDataClearLogRow);

    },

  }
}
</script>

<style lang="scss" scoped>
::v-deep .el-dialog.customClass {
  width:85% !important;
}

::v-deep .el-dialog .el-form {
  width: 97% !important;
}
::v-deep  .upload-content{
  border-color: #e19c5d;
}
::v-deep  .page-model-title {
  height: 52px;
  padding: 15px 0px 15px 10px;
}

</style>

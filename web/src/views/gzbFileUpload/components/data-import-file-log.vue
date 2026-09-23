<template>

  <div class="data-importfile-log">
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
          <span class="title-style">导入文件信息</span>
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
            <span v-if="item.prop === 'vcStatus'">
                    <span v-if="scope.row.vcStatus == 'UNDO' ">匹配失败</span>
                    <span v-else-if="scope.row.vcStatus == '1' ">匹配成功</span>
                    <span v-else-if="scope.row.vcStatus == '2' ">上传成功</span>
                    <span v-else-if="scope.row.vcStatus == '3' ">上传失败</span>
                    <span v-else-if="scope.row.vcStatus == '4' ">解压失败</span>
                    <span v-else-if="scope.row.vcStatus == '5' ">获取解压文件列表失败</span>
                    <span v-else>-</span>

            </span>

            <span v-else-if="item.prop === 'impStatus'">
                    <span v-if="scope.row.impStatus == '0'" style="color:red">导入失败</span>
                    <span v-else-if="scope.row.impStatus == '1'">导入成功</span>
                    <span v-else>-</span>

            </span>


            <span v-else>{{ scope.row[item.prop] | noDataFilter }}</span>
          </template>
        </vxe-table-column>
        <vxe-table-column title="明细" align="center" width="150px" fixed="right">
          <template slot-scope="scope">

                <span v-if="scope.row.matchRule" class="table-operation" style="color:#A15008">
                  <a @click="handleFileData(scope.row)">查看估值文件内容</a>
                </span>
                <span v-else>-</span>

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
import { TABLE_DATA_IMPORT_FILE_LOG_COLUMNS } from '../scripts/constants'
import { queryTableList } from '../scripts/api'



export default {
  name: 'dataImportFileLog',
  components: {
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

      formInline:{
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
      column: TABLE_DATA_IMPORT_FILE_LOG_COLUMNS,
      // 分页信息
      pageList: {
        _pageSize: 20,
        _pageNum: 1,
        _pageFlag: true
      },
      // 当前行数据
      curImportFileRow: {},
      // 模板配置弹窗标题
      dialogGzbFileTitle: '',
      // 模板配置弹窗状态
      dialogGzbFileVisible: false,

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
      queryTableList(data)
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
     * @description 查看估值文件内容
     */
    handleFileData(row) {
      this.dialogGzbFileTitle = '估值文件内容'
      this.dialogGzbFileVisible = true
      this.curImportFileRow = JSON.parse(JSON.stringify(row))
      // 触发一个名为'handleGzbData'的事件，并传递数据
      this.$emit('handleGzbData', this.dialogGzbFileTitle,this.dialogGzbFileVisible,this.curImportFileRow);

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

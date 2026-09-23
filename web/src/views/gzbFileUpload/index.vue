<template>
  <div class="gzbFileUpload">
    <div>
<!--      <div class="gzb">
          <div class="page-model-title">
            <div class="title-icon">
              <div class="color-box"></div>
            </div>
            <div class="title-txt">
              上传估值文件
            </div>
          </div>
          <div class="standard-form-margin">
            <div class="inner-margin">
              <el-form ref="formInline" class="standard-form" :inline="true" :model="formInline">
                <el-row>
                  <el-col :span="4">
                    <el-form-item label="压缩包文件"  >
                      <el-upload
                        ref="uploadGzb"
                        accept=".zip"
                        :before-upload="beforeUpload"
                        :auto-upload="false"
                         action="#"
                        :multiple="false"
                        :on-change="handleGzbFileChange"
                        :file-list="gzbFileList"
                        class="gzb-upload"

                      >
                          <span class="standard-form">
                            <el-button slot="trigger" plain type="primary" size="small" title="请上传压缩文件以.zip结尾的文件">选取文件</el-button>
                          </span>
                      </el-upload>
                    </el-form-item>
                  </el-col>
                  <el-col :span="20">
                    <el-form-item>
                      <el-button :loading="uploadGzbLoading" :disabled="uploadGzbLoading"  plain class="view" style="margin-left: 10px" size="small" type="primary" @click.prevent="handleClick($event)"  @click="submitUploadGzb">
                        {{ uploadGzbLoading ? '上传中...' : '提交' }}
                      </el-button>
                    </el-form-item>
                  </el-col>
                </el-row>
              </el-form>
            </div>
          </div>
       </div>-->

      <div class="net">
        <div class="page-model-title">
          <div class="title-icon">
            <div class="color-box"></div>
          </div>
          <div class="title-txt">
            上传净值文件
          </div>
        </div>
        <div class="standard-form-margin">
          <div class="inner-margin">
            <el-form ref="formInline" class="standard-form" :inline="true" :model="formInline">
              <el-row>
                <el-col :span="4">
                  <el-form-item label="压缩包文件" >
                    <el-upload
                      ref="uploadNet"
                      accept=".zip"
                      :before-upload="beforeUpload"
                      :on-change="handleNetFileChange"
                      :auto-upload="false"
                      action="#"
                      :multiple="false"
                      :file-list="netFileList"
                      class="net-upload">
                          <span class="standard-form">
                            <el-button slot="trigger" plain type="primary" size="small" title="请上传压缩文件以.zip结尾的文件">选取文件</el-button>

                          </span>
                    </el-upload>
                  </el-form-item>
                </el-col>
                <el-col :span="3">
                  <el-form-item>
                    <el-button  :loading="uploadNetLoading"  :disabled="uploadNetLoading" plain class="view" style="margin-left: 10px" size="small" type="primary" @click.prevent="handleClick($event)"  @click="submitUploadNet">
                      {{ uploadNetLoading ? '上传中...' : '提交' }}
                    </el-button>
                  </el-form-item>
                </el-col>
                <el-col :span="17">
                  <el-form-item>
                    <el-button   plain class="view" style="margin-left: 10px" size="small" type="primary"   @click="downLoadTemplate()">
                      净值文件模版下载
                    </el-button>
                  </el-form-item>
                </el-col>
              </el-row>
            </el-form>
          </div>
        </div>
      </div>

      <div class="query">
        <div class="page-model-title">
          <div class="title-icon">
            <div class="color-box"></div>
          </div>
          <div class="title-txt">
            筛选
          </div>
        </div>
        <div class="standard-form-margin">
          <div class="inner-margin">
            <el-form ref="formInline" class="standard-form" :inline="true" :model="formInline">
              <el-row>
                <el-col :span="24">
                  <el-form-item label="压缩文件类型">
                    <el-select v-model="formInline.vcFileRarType" size="small" clearable filterable placeholder="请选择压缩文件类型">
                      <el-option v-for="item in fileRarTypeOptions" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                    </el-select>
                  </el-form-item>

                  <el-form-item label="上传时间">
                    <el-select v-model="formInline.uploadTime" size="small" clearable filterable placeholder="请选择上传时间">
                      <el-option v-for="item in uploadTimeOptions" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                    </el-select>
                  </el-form-item>

                  <el-form-item label="文件名">
                    <el-input v-model="formInline.vcFilenameOld" clearable size="small" placeholder="请输入文件名"></el-input>
                  </el-form-item>


                  <el-form-item >
                    <div style="padding-left: 100px">
                    <el-button  type="primary" size="small" icon="el-icon-search" @click="handleSearchTable">查询</el-button>
                    </div>
                  </el-form-item>

                </el-col>

              </el-row>
            </el-form>
          </div>
        </div>
      </div>
    </div>
    <div class="table-content" id="standard-table">
      <el-row>
        <el-col :span="16">
          <div class="page-model-title">
            <div class="title-icon">
              <div class="color-box"></div>
            </div>
            <div class="title-txt">
              上传文件解压存储记录列表
            </div>

          </div>
        </el-col>
        <el-col :span="8">
          <div style="float: right">
            <vxe-toolbar ref="tableToolbar" class="standard-vxe-toolbar" :custom="{ immediate: true }" custom />
          </div>
        </el-col>

      </el-row>


      <div id="standard-table-margin">

          <vxe-table
            v-loading="tableLoading"
            ref="refsTable"
            :cell-style="{ height: '50px' }"
            :data="tableData"
            :height="tableHeight"
            :seq-config="{seqMethod}"
            auto-resize
            stripe
            sync-resize
            show-overflow="tooltip"
            :sort-config="{ remote: true }"
            style="width: 100%"
            @sort-change="customSortMethod"
            resizable
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
                <span v-if="item.prop === 'flag'" style="color:#A15008">

                  <a @click="handleImportFileDetail(scope.row)">明细</a>
                </span>
                <span v-else-if="item.prop === 'vcStatus'">
                      <span v-if="scope.row.vcStatus == '0' ">匹配失败</span>
                      <span v-if="scope.row.vcStatus == '1' ">匹配成功</span>
                      <span v-if="scope.row.vcStatus == '2' ">上传成功</span>
                      <span v-if="scope.row.vcStatus == '3' ">上传失败</span>
                      <span v-if="scope.row.vcStatus == '4' ">解压失败</span>
                      <span v-if="scope.row.vcStatus == '5' ">获取解压文件列表失败</span>
                </span>

                <span v-else-if="item.prop === 'dataExeStatus'">
                      <span v-if="scope.row.dataExeStatus == '1'">处理完成</span>
                      <span v-else-if="scope.row.dataExeStatus == '0'" style="color:red">处理失败</span>
                      <span v-else-if="scope.row.dataExeStatus == '2'" style="color:red">校验失败</span>
                      <span v-else-if="scope.row.dataExeStatus == '3'">校验完成</span>
                      <span v-else>-</span>

                </span>

                <span v-else-if="item.prop === 'noMatchCount'">
                      <span v-if="scope.row.noMatchCount > 0" style="color:red">{{ scope.row[item.prop]}}</span>
                      <span v-else>{{ scope.row[item.prop]}}</span>

                </span>


                <span v-else>{{ scope.row[item.prop] | noDataFilter }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column title="数据操作" align="center" width="250px" fixed="right">
              <template slot-scope="scope">
                <span class="table-operation" style="color:#A15008">
                  <span v-if="scope.row.vcFileRarType=== 'GZB'">
                      <a @click="handleDoGzbDataCheckZS(scope.row)">&nbsp;&nbsp;&nbsp;&nbsp;校验</a>
                      <a @click="handleDoGzbDataClearZS(scope.row)">&nbsp;&nbsp;&nbsp;&nbsp;进行数据处理</a>
                      <a @click="handleDeleteGzbDataLog(scope.row)">&nbsp;&nbsp;&nbsp;&nbsp;删除</a>
                  </span>
                  <span v-else>
                     <a @click="handleDoGzbDataClearZS(scope.row)">&nbsp;&nbsp;&nbsp;&nbsp;进行数据处理</a>
                     <a @click="handleDeleteGzbDataLog(scope.row)">&nbsp;&nbsp;&nbsp;&nbsp;删除</a>
                  </span>


                </span>
              </template>
            </vxe-table-column>

            <vxe-table-column title="数据操作日志" align="center" width="200px" fixed="right">
              <template slot-scope="scope">
                <span class="table-operation" style="color:#A15008">
                  <span v-if="scope.row.vcFileRarType=== 'GZB'">
                      <a @click="handleGzbDataCheckInfoLog(scope.row)">&nbsp;&nbsp;&nbsp;&nbsp;校验日志</a>
                      <a @click="handleGzbDataClearLog(scope.row)">&nbsp;&nbsp;&nbsp;&nbsp;数据处理日志</a>
                  </span>
                  <span v-else>
                     <a @click="handleGzbDataClearLog(scope.row)">&nbsp;&nbsp;&nbsp;&nbsp;数据处理日志</a>
                  </span>

                </span>
              </template>
            </vxe-table-column>
          </vxe-table>
          <el-row>
            <div id="gzbFileUpload-pg" class="table-footer">
              <Pagination :total="total" :limit="pageList._pageSize" :page="pageList._pageNum" @pagination="pagination" />
            </div>
          </el-row>

      </div>
      </div>


    <el-dialog
      v-if="dialogVisible"
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      custom-class="customClass"
      @close="closeDialog"
    >
      <data-clear-log
        v-if="dialogVisible"
        :cur-gzb-file-upload-log-config-row="curGzbFileUploadLogConfigRow"
        @handleDetailData="handleCurDataClearLogRow"
      >
      </data-clear-log>

    </el-dialog>

    <el-dialog
      v-if="dialogDetailVisible"
      :title="dialogDetailTitle"
      :visible.sync="dialogDetailVisible"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      custom-class="customClass"
      @close="closeDetailDialog"
    >
      <data-detail-log
        v-if="dialogDetailVisible"
        :cur-data-clear-log-row="curDataClearLogRow"
      ></data-detail-log>
    </el-dialog>


    <el-dialog
      v-if="dialogCheckInfoVisible"
      :title="dialogCheckInfoTitle"
      :visible.sync="dialogCheckInfoVisible"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      custom-class="customClass"
      @close="closeCheckInfoDialog"
    >
      <data-check-log
        v-if="dialogCheckInfoVisible"
        :cur-gzb-file-upload-log-config-row="curGzbFileUploadLogConfigRow"
      >
      </data-check-log>

    </el-dialog>

    <el-dialog
      v-if="dialogImportFileVisible"
      :title="dialogImportFileTitle"
      :visible.sync="dialogImportFileVisible"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      custom-class="customClass"
      @close="closeImportFileDialog"
    >
      <data-import-file-log
        v-if="dialogImportFileVisible"
        :cur-gzb-file-upload-log-config-row="curGzbFileUploadLogConfigRow"
        @handleGzbData="handleGzbDataRow"
      >
      </data-import-file-log>

    </el-dialog>

    <el-dialog
      v-if="dialogGzbFileVisible"
      :title="dialogGzbFileTitle"
      :visible.sync="dialogGzbFileVisible"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      custom-class="customClass"
      @close="closeGzbFileDialog"
    >
      <data-import-gzb-detail-log
        v-if="dialogGzbFileVisible"
        :cur-import-file-row="curImportFileRow"
      >
      </data-import-gzb-detail-log>

    </el-dialog>

  </div>
</template>

<script>
import { TABLE_COLUMNS,FILE_RAR_TYPE_OPTIONS,UPLOAD_TIME_OPTIONS } from './scripts/constants'
import Pagination from '@/components/Pagination'
import commonFun from '@/filters/common.js'
import DataClearLog from './components/data-clear-log'
import { deleteFileGroupZS, doGzbDataCheckZS, doGzbDataClearZS, queryTableList,uploadGzbFile,uploadNetFile,downloadNetExcelTemplate } from './scripts/api'
import DataDetailLog from './components/data-detail-log'
import DataCheckLog from './components/data-check-log'
import DataImportFileLog from './components/data-import-file-log'
import DataImportGzbDetailLog from './components/data-import-gzb-detail-log'
import { uploadFile } from '../AccessPoolProcess/ProductExamine/scripts/api'
import { downLoadFileByUrl } from '@/utils'
export default {

  name: 'gzbFileUpload',
  components: {
    DataClearLog,
    DataDetailLog,
    DataCheckLog,
    DataImportFileLog,
    DataImportGzbDetailLog,
    Pagination
  },
  data() {
    return {
      fileRarTypeOptions:FILE_RAR_TYPE_OPTIONS,
      uploadTimeOptions:UPLOAD_TIME_OPTIONS,
      that: this,
      // form表单绑定
      formInline: {
        vcFileType: '0',
        vcFileRarType: '',
        uploadTime: '',
        vcFilenameOld: '',
        orderString: '',


      },
      // 表格高度
      tableHeight: 0,
      // 表格loading
      tableLoading: false,
      // 表格数据
      tableData: [],
      // 表格列
      column: TABLE_COLUMNS,

      // 分页信息
      pageList: {
        _pageSize: 10,
        _pageNum: 1,
        _pageFlag: true
      },
      // 总条数
      total: 0,
      // 模板配置弹窗标题
      dialogTitle: '',
      // 模板配置弹窗状态
      dialogVisible: false,
      // 当前上传文件解压存储记录列表 行数据
      curGzbFileUploadLogConfigRow: {},

      // 模板配置弹窗标题
      dialogDetailTitle: '',
      // 模板配置弹窗状态
      dialogDetailVisible: false,
      // 当前数据处理日志 行数据
      curDataClearLogRow: {},

      // 模板配置弹窗标题
      dialogCheckInfoTitle: '',
      // 模板配置弹窗状态
      dialogCheckInfoVisible: false,

      dialogImportFileTitle :'',
      dialogImportFileVisible :false,

      dialogGzbFileTitle :'',
      dialogGzbFileVisible :false,

      curImportFileRow:'',
      gzbFileList: [],
      netFileList:[],
      uploadGzbLoading:false,
      uploadNetLoading:false,
    }
  },
  mounted() {
    this.initData()
    this.$refs.refsTable.connect(this.$refs.tableToolbar)
  },
  beforeDestroy() {
    // 组件销毁移除监听事件
    window.onresize = null
  },
  methods: {

    /**
     * @description 初始化数据
     */
    initData() {
      // 查询表格
      this.handleSearchTable()
    },
    // 排序的公共方法
    customSortMethod(val) {
      this.formInline.orderString = commonFun.queryOrderBy_vxe_template(val)
      this.handleSearchTable(false)
    },

    /* 自定义序号显示 */
    seqMethod({ rowIndex }) {
      return (
        (this.pageList._pageNum - 1) * this.pageList._pageSize + rowIndex + 1
      );
    },

    /**
     * @description 表单重置
     */
    handleResetForm() {
      this.$refs['formInline'].resetFields()
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
     * @description 数据处理日志
     */
    handleGzbDataClearLog(row) {
      this.dialogTitle = '数据处理日志'
      this.dialogVisible = true
      this.curGzbFileUploadLogConfigRow = JSON.parse(JSON.stringify(row))

    },

    handleCurDataClearLogRow(dialogDetailTitle,dialogDetailVisible,curDataClearLogRow){
      this.dialogDetailTitle=dialogDetailTitle
      this.dialogDetailVisible=dialogDetailVisible
      this.curDataClearLogRow=curDataClearLogRow
    },

    /**
     * @description 校验日志
     */
    handleGzbDataCheckInfoLog(row) {
      this.dialogCheckInfoTitle = '校验日志'
      this.dialogCheckInfoVisible = true
      this.curGzbFileUploadLogConfigRow = JSON.parse(JSON.stringify(row))

    },

    handleGzbDataRow(dialogGzbFileTitle,dialogGzbFileVisible,curImportFileRow){
      this.dialogGzbFileTitle=dialogGzbFileTitle
      this.dialogGzbFileVisible=dialogGzbFileVisible
      this.curImportFileRow=curImportFileRow
    },



    /**
     * @description 关闭弹窗
     */
    closeDialog(status) {
      this.dialogTitle = ''
      this.dialogVisible = false

      if (status === 'REFESH') this.handleSearchTable()
    },


    /**
     * @description 关闭弹窗
     */
    closeDetailDialog(status) {
      this.dialogDetailTitle = ''
      this.dialogDetailVisible = false
      //this.$emit('closeDialog');//仍然发射事件告诉父组件关闭这个对话框

    },

    /**
     * @description 关闭弹窗
     */
    closeCheckInfoDialog(status) {
      this.dialogCheckInfoTitle = ''
      this.dialogCheckInfoVisible = false

      if (status === 'REFESH') this.handleSearchTable()
    },

    closeImportFileDialog(status) {
      this.dialogImportFileTitle = ''
      this.dialogImportFileVisible = false

      if (status === 'REFESH') this.handleSearchTable()
    },

    closeGzbFileDialog(status) {
      this.dialogGzbFileTitle = ''
      this.dialogGzbFileVisible = false

      if (status === 'REFESH') this.handleSearchTable()
    },

    handleDeleteGzbDataLog(row){
      this.$confirm('是否确定删除?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          const params = {
            fileGroup: row.fileGroup
          }
          deleteFileGroupZS(params).then((res) => {
            if (res.data.status === 200) {
              this.$message({
                type: 'success',
                message: '删除成功',
                customClass: 'message-success'
              })
              this.handleSearchTable()
            } else {
              this.$message({
                type: 'error',
                message: '删除失败',
                customClass: 'message-error'
              })
            }
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          })
        })
    },
    handleDoGzbDataCheckZS(row){
      this.$confirm('确定进行数据校验吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          const params = {
            fileGroup: row.fileGroup
          }
          this.$message({
            type: 'success',
            message: '操作已提交,请稍后刷新列表',
            customClass: 'message-success'
          })
          doGzbDataCheckZS(params).then((res) => {
            if (res.data.status === 200) {
              this.$message({
                type: 'success',
                message: '数据校验成功',
                customClass: 'message-success'
              })
              this.handleSearchTable()
            } else {
              this.$message({
                type: 'error',
                message: '数据校验失败',
                customClass: 'message-error'
              })
            }
          }).catch(() => {})
            .finally(()=>{ this.handleSearchTable()})
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          })
        })
    },
    handleDoGzbDataClearZS(row){
      this.$confirm('确定进行数据处理?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          const params = {
            fileGroup: row.fileGroup
          }
          this.$message({
            type: 'success',
            message: '操作已提交,请稍后刷新列表',
            customClass: 'message-success'
          })
          setTimeout(this.handleSearchTable, 500);
          doGzbDataClearZS(params).then((res) => {
            if (res.data.status === 200) {
              this.$message({
                type: 'success',
                message: '数据处理成功',
                customClass: 'message-success'
              })



            } else {
              this.$message({
                type: 'error',
                message: '数据处理失败',
                customClass: 'message-error'
              })
            }
          }).catch(() => {})
            .finally(()=>{ this.handleSearchTable()})
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          })
        })
    },

    /**
     * @description 文件导入明细
     */
    handleImportFileDetail(row) {
      this.dialogImportFileTitle = '文件压缩包详细'
      this.dialogImportFileVisible = true
      this.curGzbFileUploadLogConfigRow = JSON.parse(JSON.stringify(row))

    },

    beforeUpload(file) {
      const isZip = file.type === 'zip' || file.type === 'ZIP';
      if (!isZip) {
        this.$message.error('只能上传zip的压缩文件!');
        return false;
      }
      return true;
    },
    handleGzbFileChange(file, fileList) {

      if (fileList.length > 0) {
        this.gzbFileList = [fileList[fileList.length - 1]]
      }else{
        this.gzbFileList = fileList[0]
      }

    },
    async submitUploadGzb(){

        this.uploadGzbLoading = true
       // let isCloseDialog = 0
        const formData = new FormData()
        this.gzbFileList.forEach(file => {
          formData.append('uploadFile', file.raw); //
        });
        formData.append('vcFileRarType', 'GZB')
         await this.uploadGzbPromise(formData)
         this.uploadGzbLoading = false
         this.handleSearchTable()
          this.$refs.uploadGzb.clearFiles(); // 清除文件列表


    },
    uploadGzbPromise(params) {
      return new Promise((resolve, reject) => {
        uploadGzbFile(params).then((res) => {
          if (res.data.status === 200) {
            this.$message({
              type: 'success',
              message: '上传成功',
              customClass: 'message-success'
            })
            resolve('success')
          } else {
            this.$message({
              type: 'error',
              message: res.data.message,
              customClass: 'message-error'
            })
            resolve('error')
          }
        })
      })
    },
    handleNetFileChange(file, fileList) {

      if (fileList.length > 0) {
        this.netFileList = [fileList[fileList.length - 1]]
      }else{
        this.netFileList = fileList[0]
      }

    },
    async submitUploadNet(){
      this.uploadNetLoading = true
      // let isCloseDialog = 0
      const formData = new FormData()
      this.netFileList.forEach(file => {
        formData.append('uploadFile', file.raw); //
      });
      formData.append('vcFileRarType', 'NET')
      await this.uploadNetPromise(formData)
      this.uploadNetLoading = false
      this.handleSearchTable()
      this.$refs.uploadNet.clearFiles(); // 清除文件列表

    },

    uploadNetPromise(params) {
      return new Promise((resolve, reject) => {
        uploadNetFile(params).then((res) => {
          if (res.data.status === 200) {
            this.$message({
              type: 'success',
              message: '上传成功',
              customClass: 'message-success'
            })
            resolve('success')
          } else {
            this.$message({
              type: 'error',
              message:"上传异常！请联系管理人员!"+ res.data.message,
              customClass: 'message-error'
            })
            resolve('error')
          }
        })
      })
    },

    handleClick(event) {
      event.target.blur()
      if (event.target.nodeName === 'SPAN') {
        event.target.parentNode.blur()
      }
    },
    downLoadTemplate(){

      const fileName = '净值文件模板.xlsx'
      const url = 'api/gzrest/downloadNetExcelTemplate'
      const params = {  }
      downLoadFileByUrl(url, params, fileName, this)



    }

  },






}
</script>
<style lang="scss" scoped>
#gzbFileUpload-pg .pagination-container {
  .el-input {
    width: 100px !important;
  }
}
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

//.gzb-upload{
//  height: 70px;
//}
//.el-upload el-upload--text{
//  height: 65px;
//}

</style>



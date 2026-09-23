<template>
  <div class="data-test">
    <el-form v-model="formQuery" :inline="true">
      <el-row>
        <el-col :span="12">
          <el-form-item label="申请简称">
            <el-input placeholder="请输入简称便于查询" size="small"></el-input>
          </el-form-item>
          <el-form-item label="产品名称">
            <el-input placeholder="" size="small"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <div class="btn-float-right">
            <el-button size="small" type="primary" icon="el-icon-search">查询</el-button>
            <el-button size="small" type="primary" icon="el-icon-refresh">重置</el-button>
            <el-button size="small" type="primary" @click="handleNewSubmit" icon="el-icon-plus">新申请</el-button>
          </div>
        </el-col>
      </el-row>
      <el-row>
        <el-col>
          <el-form-item label="申请日期">
            <el-date-picker
              v-model="formQuery.date"
              end-placeholder="结束日期"
              range-separator="至"
              start-placeholder="开始日期"
              size="small"
              type="daterange">
            </el-date-picker>
          </el-form-item>
          <el-form-item label="处理状态">
            <el-select v-model="formQuery.status" clearable placeholder="请选择" size="small">
              <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <div class="title-style">数据质检列表</div>
    <el-table :data="tableDate" align="center" class="mt10" border>
      <el-table-column
        header-align="center"
        label="序号"
        align="center"
        type="index"
        width="50">
      </el-table-column>
      <el-table-column header-align="center" align="center" label="申请简称" prop="sqjj">
        <template slot-scope="scope">
          {{ scope.row.sqjj | noDataFilter }}
        </template>
      </el-table-column>
      <el-table-column header-align="center" align="center" label="产品名称" prop="cpmc">
        <template slot-scope="scope">
          {{ scope.row.cpmc | noDataFilter }}
        </template>
      </el-table-column>
      <el-table-column header-align="center" align="center" label="说明" prop="sm">
        <template slot-scope="scope">
          {{ scope.row.sm | noDataFilter }}
        </template>
      </el-table-column>
      <el-table-column header-align="center" align="center" label="文件附件" prop="wjfj">
        <template slot-scope="scope">
          {{ scope.row.wjfj | noDataFilter }}
        </template>
      </el-table-column>
      <el-table-column header-align="center" align="center" label="申请日期" prop="sqrq">
        <template slot-scope="scope">
          {{ scope.row.sqrq | noDataFilter }}
        </template>
      </el-table-column>
      <el-table-column header-align="center" align="center" label="申请人" prop="sqr">
        <template slot-scope="scope">
          {{ scope.row.sqr | noDataFilter }}
        </template>
      </el-table-column>
      <el-table-column header-align="center" align="center" label="处理状态" prop="clzt">
        <template slot-scope="scope">
          <span style="color: #70ad47">{{ scope.row.clzt | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column header-align="center" align="center" label="处理结果" prop="cljg">
        <template slot-scope="scope">
          {{ scope.row.cljg | noDataFilter }}
        </template>
      </el-table-column>
      <el-table-column header-align="center" align="center" label="操作" prop="operate">
        <template slot-scope="scope">
          <el-button size="small" type="primary" @click="handleEdit(scope.row)">编辑</el-button>
          <el-button size="small" type="primary" @click="handleDetail(scope.row)" plain>详情</el-button>
          <el-button size="small" type="danger" plain>删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <Pagination :total="total" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination"></Pagination>

    <el-dialog :title="dialogOption.dialogTitle" :visible.sync="dialogOption.dialogVisible">
      <el-form v-model="dialogFormEdit" label-width="80px">
        <el-form-item label="申请简称" prop="sqjj">
          <el-input v-model="dialogFormEdit.sqjj"></el-input>
        </el-form-item>
        <el-form-item label="产品名称">
          <el-input v-model="dialogFormEdit.cpmc"></el-input>
        </el-form-item>
        <el-form-item label="说明:">
          <el-input v-model="dialogFormEdit.sm" :rows="4" type="textarea"></el-input>
        </el-form-item>
        <el-form-item label="文件附件">
          <el-upload
            class="upload-demo"
				    v-model="fileList"
            ref="upload"
            name="file"
            :headers="{}"
            action=""
            :on-remove="handleRemove"
            :on-change="handleChange"
            :file-list="fileList"
            :auto-upload="false">
          <el-button size="small" type="primary">选择文件</el-button>
          <!-- <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div> -->
        </el-upload>
          <!-- <el-row>
            <el-col :span="18">
              <vxe-table :data="dialogTableData" :show-header="false" border="none">
                <vxe-table-column field="fileName"></vxe-table-column>
                <vxe-table-column field="operate">
                  <template slot-scope="scope">
                    <el-button size="small" type="primary">删除</el-button>
                    <el-button size="small" type="primary">下载</el-button>
                  </template>
                </vxe-table-column>
              </vxe-table>
            </el-col>
            <el-col :span="6">
              <el-button size="small" type="primary">上传</el-button>
            </el-col>
          </el-row> -->
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="dialogOption.dialogVisible = false">取 消</el-button>
        <el-button size="small" type="primary" @click="dialogOption.dialogVisible = false">提 交</el-button>
      </div>
    </el-dialog>

    <el-dialog :title="dialogDetailOption.dialogTitle" :visible.sync="dialogDetailOption.dialogVisible">
      <el-form v-model="dialogFormDetail" label-width="80px">
        <el-form-item label="申请简称" prop="sqjj">
          <el-input v-model="dialogFormDetail.sqjj" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="产品名称">
          <el-input v-model="dialogFormDetail.cpmc" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="说明">
          <el-input v-model="dialogFormDetail.sm" :rows="4" type="textarea" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="申请日期">
          <el-input v-model="dialogFormDetail.sqrq" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="申请人">
          <el-input v-model="dialogFormDetail.sqr" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="处理状态">
          <el-select v-model="dialogFormDetail.status" clearable placeholder="请选择" :disabled="true">
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="处理结果">
          <el-input v-model="dialogFormDetail.cljg" :rows="4" type="textarea" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="文件附件">
          <el-upload
            class="upload-custom"
            action="https://jsonplaceholder.typicode.com/posts/"
            multiple
            disabled
            :file-list="fileList2">
            <div slot="file" slot-scope="{ file }" class="download-acitve">
              <span>{{ file.name }}</span>
              <i class="el-icon-download" />
            </div>
          </el-upload>
          <!-- <el-row>
            <el-col :span="18">
              <vxe-table :data="dialogTableData" :show-header="false" border="none">
                <vxe-table-column field="fileName"></vxe-table-column>
                <vxe-table-column field="operate">
                  <template slot-scope="scope">
                    <el-button size="small" type="primary">删除</el-button>
                    <el-button size="small" type="primary">下载</el-button>
                  </template>
                </vxe-table-column>
              </vxe-table>
            </el-col>
            <el-col :span="6">
              <el-button size="small" type="primary">上传</el-button>
            </el-col>
          </el-row> -->
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="dialogDetailOption.dialogVisible = false">取 消</el-button>
        <el-button size="small" type="primary" @click="dialogDetailOption.dialogVisible = false">提 交</el-button>
      </div>
    </el-dialog>

  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
export default {
  components: {Pagination},
  data() {
    return {
      formQuery: {
        date: [],
        status: '',
        pageSize: 20,
        pageNum: 1
      },
      options: [
        {
          value: 0,
          label: '已提交',
        },
        {
          value: 1,
          label: '处理中',
        },
        {
          value: 2,
          label: '处理完毕',
        },
      ],
      fileList: [],
      fileList2: [
        { name: "测试文件1.xls" },
        { name: "测试文件2.xls" },
      ],
      dialogTableData: [
        {
          fileName: '测试文件1',
          fid: 0,
        },
        {
          fileName: '测试文件2',
          fid: 1,
        },
      ],
      tableDate: [
        {
          sqjj: '测试1号',
          cpmc: '测试1号',
          sm: '测试',
          sqrq: '2020-02-02',
          sqr: '刘瑞兵',
          clzt: '处理完毕',
          cljg: '同意',
          status: 0,
        },
        {
          sqjj: '测试2号',
          cpmc: '测试2号',
          sm: '测试2',
          sqrq: '2020-05-02',
          sqr: '张三',
          clzt: '处理完毕',
          cljg: '同意',
          status: 1,
        }
      ],
      dialogOption: {
        dialogTitle: '申请',
        dialogVisible: false,
      },
      dialogDetailOption: {
        dialogTitle: '申请',
        dialogVisible: false,
      },
      total: 2,
      dialogFormEdit: {},
      dialogFormDetail: {}
    }
  },
  methods: {
    handleNewSubmit() {
      this.dialogOption.dialogTitle = '申请';
      this.dialogOption.dialogVisible = true;
    },
    handleEdit(row) {
      this.dialogFormEdit = {...row}
      this.dialogOption.dialogTitle = '编辑'
      this.dialogOption.dialogVisible = true
    },
    handleDetail(row) {
      this.dialogFormDetail = {...row}
      this.dialogDetailOption.dialogTitle = '详情'
      this.dialogDetailOption.dialogVisible = true
    },
    // 页面点击事件
    pagination (val) {
      let {page, limit} = val
      // 起始页
      this.formQuery.pageNum = page
      // 每页数量
      this.formQuery.pageSize = limit
    },
    handleRemove(){},
    handleChange(){},
  }
};
</script>

<style lang="scss" scoped>
.data-test {
  .title-style {
    color: #c39330;
    height: 35px;
    line-height: 35px;
    padding-left: 4px;
    font-size: 16px;
    border-left: 4px solid #c39330;
  }

  .btn-float-right {
    float: right;
  }
}
</style>

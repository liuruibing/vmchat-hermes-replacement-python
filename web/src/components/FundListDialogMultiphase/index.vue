<template>
  <div class="fundListDialogMultiphase">
    <!-- 搜索 -->
    <el-form ref="formQuery" :inline="true" :model="formQuery" :rules="rules" class="formQuery pdt5">
      <el-row>
        <el-col :span="16">
          <div class="grid-content bg-purple">
            <el-form-item :label-width="formLabelWidth" prop="fundCode">
              <span slot="label" class="item-label">产品代码</span>
              <el-input v-model.trim="formQuery.fundCode" clearable size="small" placeholder="请输入产品代码" />
            </el-form-item>
            <el-form-item :label-width="formLabelWidth" label="" prop="fundName">
              <span slot="label" class="item-label">产品名称</span>
              <el-input v-model.trim="formQuery.fundName" clearable size="small" placeholder="请输入产品名称" />
            </el-form-item>
          </div>
        </el-col>
        <!--        :disabled="btnDisabled"-->
        <el-col :span="8">
          <div class="grid-content bg-purple-light">
            <el-form-item class="search_button_com">
              <el-button type="primary" class="mb5" icon="el-icon-search" @click="onQuery(1)">查询</el-button>
              <!--              <el-button   @click="resetForm('formQuery')">重置</el-button>-->
              <el-button type="primary" icon="el-icon-plus" class="mb5" @click="checkFund()">确定</el-button>
            </el-form-item>
          </div>
        </el-col>
      </el-row>
    </el-form>
    <el-row style="padding-top: 10px">
      <el-col>
        <el-tag v-for="tag in tags" :key="tag.fundName" size="medium" closable @close="closeTag(tag)">
          {{ tag.fundName }}
        </el-tag>
      </el-col>
    </el-row>
    <el-row>
      <div class="table-title">
        <div class="picc_forms_table_title_line" />
        <div>产品信息</div>
      </div>
    </el-row>
    <!--    :header-cell-style="this.$fun.headerRowStyle"-->
    <vxe-table
      id="toolbar_table1"
      ref="table1"
      :loading="tableLoading"
      :data="tableData"
      stripe
      :cell-style="{ height: '40px' }"
      :header-cell-style="{ color: '#333', height: '60px', background: '#fff', fontFamily: 'Microsoft Yahei' }"
      max-height="400px"
      highlight-hover-row
      show-header-overflow
      resizable
      auto-resize
      show-overflow
      @checkbox-all="selectAllEvent"
      @checkbox-change="selectChangeEvent"
      @sort-change="handleSortChange"
    >
      <vxe-table-column type="checkbox" width="50" />
      <vxe-table-column field="fundCode" title="产品代码" min-width="100" sortable header-align="center" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.fundCode | noDataFilter }}</span>
        </template>
      </vxe-table-column>
      <vxe-table-column field="fundName" title="产品名称" min-width="250" sortable header-align="center" align="left">
        <template slot-scope="scope">
          <span>{{ scope.row.fundName | noDataFilter }}</span>
        </template>
      </vxe-table-column>
      <vxe-table-column field="createDate" title="成立日期" min-width="100" sortable header-align="center" align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.createDate | noDataFilter }}</span>
        </template>
      </vxe-table-column>
    </vxe-table>
    <vxe-pager
      :current-page="formQuery.pageNum"
      :page-size="formQuery.pageSize"
      :total="total"
      :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
      border
      size="medium"
      @page-change="pagination"
    />
  </div>
</template>

<script type="text/ecmascript-6">
import commonApi from '@/api/common'
import fundInfoApi from '@/api/dataManage/fundInfoApi'

export default {
  name: 'FundListDialogMultiphase',
  components: {},
  props: {
    maxLength: {
      default: null
    },
    tagsinfo: {
      required: true,
      type: Array
    }
  },
  data() {
    return {
      // 查询参数
      formQuery: {
        // 产品代码
        fundCode: '',
        // 产品名称
        fundName: '',
        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10,
        // 排序方式
        orderBy: "fundCode asc"
      },
      // 验证规则
      rules: {},
      // 选中的行
      multiphaseRows: [],
      tags: [],
      tempTags: [],

      // 产品列表数据
      tableData: [],
      // 总条数
      total: 0,
      // 表格loading
      tableLoading: false,
      // 附件表格loading
      tableLoading_doc: false,
      /* 按钮禁止与否 */
      isDisabled: false,
      // 表单宽度
      formLabelWidth: '120px',

      templateRadio: '',
      // 选中行数据
      tableRowData: null,

      // 查询按钮禁用
      btnDisabled: false,
      // 查询按钮禁用 附件列表
      btnDisabled_doc: false,
      // 默认页签
      activeName: 'baseInfo'
    }
  },
  watch: {
    tagsinfo: {
      handler(n) {
        this.tags = [...n]
      },
      immediate: true,
      deep: true
    }
  },
  mounted() {
    // 默认查询
    this.$nextTick(() => {
      // 查询
      this.onQuery()
    })
  },
  methods: {
    // 查询
    onQuery(page) {
      // 禁用搜索按钮
      this.$fun.searchButtonDisabled('btnDisabled', this)
      // 重置起始页
      if (page) this.formQuery.pageNum = 1
      // 查询产品信息
      this.selectFundInfoList()
      // this.$refs['formQuery'].validate(valid => {
      //   if (valid) {
      //     // 禁用搜索按钮
      //     this.$fun.searchButtonDisabled('btnDisabled', this)
      //     // 重置起始页
      //     if (page) this.formQuery.pageNum = 1
      //     // 查询产品信息
      //     this.selectFundInfoList()
      //   }
      // })
    },
    checkFund() {
      if (this.maxLength) {
        // 限制最大勾选数量
        if (this.tags == null || this.tags == undefined || this.tags == []) {
          this.$message({
            message: '请选择产品',
            type: 'warning'
          })
          return
        } else if (this.tags.length > this.maxLength) {
          this.$message({
            message: `最多只能选择${this.maxLength}个产品`,
            type: 'warning'
          })
          return
        } else {
          const tempArr = this.tags
          // let tempArr = this.$refs.table1.selection
          this.$emit('getTemplateRow', { data: tempArr })
          this.dialogMask = false
        }
      } else {
        // 不限制最大勾选数量
        if (this.tags == null || this.tags == undefined || this.tags == []) {
          this.$message({
            message: '请选择产品',
            type: 'warning'
          })
          return
        } else {
          const tempArr = this.tags
          // let tempArr = this.$refs.table1.selection
          this.$emit('getTemplateRow', { data: tempArr })
          this.dialogMask = false
        }
      }
    },
    // 清除
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },

    // 查询产品信息
    selectFundInfoList(flag) {
      this.tableLoading = true
      const params = {}
      params.fundCode = this.formQuery.fundCode
      params.fundName = this.formQuery.fundName
     /*  params.offset =(this.formQuery.pageNum - 1) * this.formQuery.pageSize
      params.limit = this.formQuery.pageSize */
      params.pageNum = this.formQuery.pageNum
      params.pageSize = this.formQuery.pageSize
      params.orderString = this.formQuery.orderBy
      fundInfoApi.fun_selectFundListNotManager(params)
        .then(res => {
          const {status, data} = res
          if (status === 0) {
            this.tableLoading = false;
            this.isDisabled = false;
            this.tableData = data.list
            this.total = data.total
            this.checkTableData(this.tableData, this.tags)
          }
        })
        .catch(() => {
          this.tableLoading = false
          this.isDisabled = false
        })
    },

    // 关闭标签事件
    closeTag(val) {
      const self = this
      const arr = this.tags
      if (val) {
        arr.splice(self.getItemIndex(arr, val), 1)
        const temp = self.tableData[self.getItemIndex(self.tableData, val)]
        this.$refs.table1.toggleCheckboxRow(temp)
      }
    },
    // 添加指定标签
    addRow(val) {
      const arr = this.tags
      if (this.checkItem(arr, val)) {
        this.tags.push(val)
      }
    },
    // 删除指定标签
    closeRow(val) {
      const self = this
      const arr = this.tags
      // if(this.checkItem(arr,val)){
      arr.splice(self.getItemIndex(arr, val), 1)
      // }
    },
    // 选中行事件
    selectChangeEvent({ row, checked }) {
      if (checked) {
        this.addRow(row)
      } else {
        this.closeRow(row)
      }
    },
    // 全选事件
    selectAllEvent({ records, checked }) {
      const self = this
      const arr = self.tags
      // let tempArr = self.tempTags
      if (checked) {
        if (records) {
          // tempArr.push.apply(tempArr,records) //临时储存这次全选的数据
          records.forEach(function(item, index) {
            if (self.checkItem(arr, item)) {
              arr.push(item)
            }
          })
        }
      } else {
        this.tableData.forEach(function(item, index) {
          arr.splice(self.getItemIndex(arr, item), 1)
        })
      }
    },
    // 检查数组中是否 不存在该数据
    checkItem(arr, val) {
      var flag = 0
      for (var i = 0; i < arr.length; i++) {
        if (arr[i].fundCode == val.fundCode && arr[i].fundName == val.fundName) {
          flag++
        }
      }
      return flag == 0
    },
    // 检查两个数据是否有选中项
    checkTableData(tableList, checkList) {
      const self = this
      const tempArr = []
      tableList.forEach(function(item, index) {
        if (!self.checkItem(checkList, item)) {
          tempArr.push(item)
        }
      })
      if (tempArr.length > 0) {
        self.$refs.table1.setCheckboxRow(tempArr, true)
      }
    },
    // 获取指定对象下标
    getItemIndex(arr, val) {
      for (var i = 0; i < arr.length; i++) {
        if (arr[i].fundCode == val.fundCode && arr[i].fundName == val.fundName) {
          return i
        }
      }
    },
    // 页面分页点击事件
    pagination(val) {
      this.tempTags = []
      const { currentPage, pageSize } = val
      // 起始页
      this.formQuery.pageNum = currentPage
      // 每页数量
      this.formQuery.pageSize = pageSize
      // 查询
      this.onQuery()
    },

    // 当表格的排序条件发生变化的时候会触发该事件
    handleSortChange(val) {
      this.formQuery.orderBy = this.$fun.queryOrderBy(val)
      // 查询
      this.onQuery()
    }

  }
}
</script>

<style lang="scss" scoped>
.fundListDialogMultiphase {
  .item-label {
    font-size: 14px;
  }

  .el-tag--medium {
    height: 28px !important;
    line-height: 26px !important;
  }

  .el-tag {
    font-size: 14px !important;
    //font-weight: 600 !important;
  }

  input::-webkit-input-placeholder {
    color: #999 !important;
  }
  ::v-deep .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
  .table-title {
    font-size: 14px;
    color: rgba(0, 0, 0, 0.85);
    line-height: 20px;
    font-weight: 600;
    padding: 10px 0 10px 2px;
    ::v-deep .ant-btn {
      border-color: #4055ff;
      color: #4055ff;
    }
  }
}
</style>

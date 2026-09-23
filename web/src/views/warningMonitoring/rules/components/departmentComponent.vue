<template>
  <div>
    <el-dialog title="机构选择" :append-to-body="true" :visible.sync="dialogVisible" style="padding: 0px 20px" width="80%" @closed="handleDialogClosed">
      <el-row :gutter="10">
        <el-col :span="19">
          <div style="border: 1px solid #dcdfe6">
            <div class="background_fa">
              <el-form ref="formQuery" :model="formQuery" :rules="formRules" inline style="width: 100% !important">
                <el-form-item label="" prop="userInput">
                  <el-input v-model="formQuery.userInput" placeholder="管理人全称/拼音/备案号" style="width: 200px !important" size="small"></el-input>
                </el-form-item>
                <el-form-item label="公司类型" class="companyType">
                  <el-select v-model="formQuery.companyTypes" multiple placeholder="请选择公司类型" size="small">
                    <el-option v-for="item in companyTypesOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="公司状态" prop="companyStatuses">
                  <el-select v-model="formQuery.companyStatuses" multiple placeholder="请选择公司状态" size="small">
                    <el-option v-for="item in companyStatusesOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item>
                  <el-button size="small" type="primary" @click="getCompanyTypesData">搜索</el-button>
                </el-form-item>
              </el-form>
            </div>
            <vxe-table
              ref="vxetable"
              v-loading="tableLoading"
              :cell-style="{ height: '45px' }"
              :checkbox-config="{ checkStrictly: true }"
              :data="tableData"
              :header-cell-style="{ color: '#000', height: '45px' }"
              :height="500"
              :sort-config="{ remote: true, defaultSort: { field: 'ASSET_SCALE', order: 'desc' } }"
              auto-resize
              stripe=""
              style="width: 100%"
              sync-resize
              show-overflow
              @checkbox-change="handleCheckBoxClick"
              @sort-change="handleSortChange"
            >
              <vxe-table-column align="center" fixed="left" type="checkbox" width="55"></vxe-table-column>
              <vxe-table-column
                v-for="item in departmentPageColumns"
                :key="item.id"
                :align="item.align"
                :field="item.id"
                :fixed="item.fix"
                :min-width="item.width"
                :sortable="item.sortable"
                :title="item.label"
                header-align="center"
              >
                <template slot-scope="scope">
                  {{ scope.row[item.id] | noDataFilter }}
                </template>
              </vxe-table-column>
            </vxe-table>
            <el-row>
              <Pagination :limit="formQuery._pageSize" :page="formQuery._pageNum" :total="total" @pagination="Pagination"></Pagination>
            </el-row>
          </div>
        </el-col>
        <el-col :span="5">
          <div style="border: 1px solid #dcdfe6">
            <div class="background_fa checked-box-title">已选机构</div>
            <div class="checked-box">
              <div v-for="item in selectList" :key="item.objcode" class="checked-item">
                <span class="checked-item-name" :title="item.COMPANY_NAME || item.objcode">
                  {{ item.COMPANY_NAME || item.objcode }}
                </span>
                <i class="el-icon-delete checked-item-icon" @click="onRemoveItem(item)"></i>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
      <div slot="footer" style="text-align: center">
        <el-button size="small" @click="handleCancel" :disabled="disabled">取 消</el-button>
        <el-button size="small" type="primary" @click="handleSubmit" :disabled="disabled">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import commonApi from '@/api/common'
import Pagination from '@/components/Pagination'
import commonFun from '@/filters/common'

export default {
  components: { Pagination },
  props: {
    multiple: {
      type: Boolean,
      default: false
    },
    departmentVisible: {
      type: Boolean,
      required: true,
      default: false
    },
    companyList: {
      type: Array,
      required: true,
      default: () => {
        return []
      }
    }
  },
  data() {
    return {
      dialogVisible: false,
      formQuery: {
        userInput: '', // 管理人名称
        companyTypes: [], // 公司类型
        companyStatuses: ['1'], // 公司状态
        orderString: 'ASSET_SCALE desc',
        _pageSize: 10,
        _pageNum: 1,
        _pageFlag: true
      },
      total: 0,
      companyTypesOptions: [],
      companyStatusesOptions: [
        {
          label: '运行',
          value: '1'
        },
        {
          label: '注销',
          value: '2'
        },
        {
          label: '吊销',
          value: '3'
        },
        {
          label: '其他',
          value: '-1'
        }
      ],
      formRules: {
        companyStatuses: [{ required: true, message: '请选择公司状态', trigger: 'blur' }]
      },
      tableData: [],
      tableLoading: false,
      departmentPageColumns: [
        {
          label: '备案代码',
          id: 'REG_CODE',
          align: 'center',
          fix: 'left',
          width: '100px',
          filter: '',
          sortable: true
        },
        {
          label: '管理人全称',
          id: 'COMPANY_NAME',
          align: 'center',
          fix: 'left',
          width: '100px',
          filter: '',
          sortable: true
        },
        {
          label: '公司类型',
          id: 'COMPANY_TYPE',
          align: 'center',
          fix: 'left',
          width: '100px',
          filter: '',
          sortable: true
        },
        {
          label: '公司状态',
          id: 'VC_STATUS',
          align: 'center',
          fix: 'left',
          width: '100px',
          filter: '',
          sortable: true
        },
        {
          label: '机构证券自主管理规模',
          id: 'ASSET_SCALE',
          align: 'center',
          fix: 'left',
          width: '100px',
          filter: '',
          sortable: true
        },
        {
          label: '团队人数',
          id: 'STAFF_NUM',
          align: 'center',
          fix: 'left',
          width: '100px',
          filter: '',
          sortable: true
        }
      ],
      selectList: [],
      disabled: false
    }
  },
  watch: {
    departmentVisible: {
      handler(val) {
        this.dialogVisible = val
        if (this.dialogVisible == true) {
          this.selectList = [...this.companyList]
          // console.log(this.selectList)
          this.$nextTick(() => {
            this.getCompanyTypesData()
          })
        }
      },
      deep: true,
      immediate: true
    },
    tableData: {
      handler() {
        if (this.$refs.vxetable) {
          this.$refs.vxetable.setAllCheckboxRow(false)
        }
        // console.log(this.selectList)
        this.selectList.forEach((item) => {
          let index = this.tableData.findIndex((sitem) => {
            return item.objcode == sitem.objcode
          })
          if (index != -1) {
            this.$refs.vxetable.setCheckboxRow(this.tableData[index], true)
          }
        })
      },
      deep: true,
      immediate: true
    }
  },
  mounted() {
    this.init()
  },
  activated() {},
  methods: {
    async init() {
      await this.companyTypesOptionsData()
    },
    Pagination(val) {
      const { page, limit } = val
      this.formQuery._pageNum = page
      this.formQuery._pageSize = limit
      this.getCompanyTypesData()
    },
    handleCheckBoxClick({ checked, row }) {
      //console.log(checked)
      if (checked) {
        if (!this.multiple) {
          if (this.selectList.length > 0) {
            this.$message.closeAll()
            this.$message.warning('此页面为单选')
            this.$refs.vxetable.toggleRowSelection(row, false)
            return
          }
        }
        let index = this.selectList.findIndex((item) => item.objcode == row.objcode)
        if (index == -1) {
          this.selectList.push(row)
        }
      } else {
        let index = this.selectList.findIndex((item) => item.objcode == row.objcode)
        if (index != -1) {
          this.selectList.splice(index, 1)
        }
      }
    },
    handleSortChange(val) {
      this.formQuery.orderString = commonFun.queryOrderBy_vxe_template(val)
      // 查询
      this.getCompanyTypesData()
    },
    handleDialogClosed() {
      this.dialogVisible = false
      this.$emit('dialogclose')
    },
    handleCancel() {
      this.dialogVisible = false
      this.$emit('dialogclose')
    },
    handleSubmit() {
      this.$emit('submit', this.selectList)
      this.disabled = true
    },
    setDisabled(flag) {
      this.disabled = flag
    },

    // 获取公司状态下拉
    companyTypesOptionsData() {
      return new Promise((resolve, reject) => {
        const params = {}
        params.indexCode = '5122c4e4-6672-479c-978e-a8172e2a50f5'
        commonApi.getDataBysqlCode(params).then((res) => {
          const { status, data } = res.data
          if (status == 0) {
            if (data.length && data.length > 0) {
              const tempArray = []
              data.forEach((item) => {
                tempArray.push({
                  label: item.DIM_NME,
                  value: item.DIM_CDE
                })
              })
              this.companyTypesOptions = tempArray
            } else {
              this.companyTypesOptions = []
            }
          } else {
          }
        })
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

    // 获取列表数据
    getCompanyTypesData() {
      this.$refs.formQuery.validate((valid) => {
        if (valid) {
          try {
            this.tableLoading = true
            let params = Object.assign({}, this.formQuery)
            params = this.parameterSrc(params)
            params.indexCode = '9b3b0859-cb8f-464d-abe6-1fbe51a7a5da'
            commonApi
              .getDataBysqlCode(params)
              .then((res) => {
                let { status, data } = res.data
                if (status == 0) {
                  this.tableData = data.rows || []
                  this.tableData.forEach(item => {
                    item.objcode = item.REG_CODE || item.COMPANY_ID || ""
                  })
                  this.total = data.total
                } else {
                  this.tableData = []
                  this.total = 0
                }
                this.tableLoading = false
              })
              .catch((err) => {
                this.tableData = []
                this.total = 0
                this.tableLoading = false
              })
          } catch (e) {
            //console.log(e)
          }
        } else {
        }
      })
    },
    // 移除
    onRemoveItem(data) {
      const index = this.selectList.findIndex((item) => item.objcode === data.objcode)
      if (index !== -1) {
        this.selectList.splice(index, 1)
        this.tableData.forEach((item) => {
          if (item.objcode === data.objcode) {
            this.$refs.vxetable.toggleRowSelection(item, false)
          }
        })
      }
    }
  }
}
</script>
<style lang="scss" scoped>
::v-deep .el-dialog {
  width: 80% !important;
}
.companyType {
  ::v-deep .el-select .el-input {
    width: 185px !important;
  }
}
.checked-box-title {
  height: 50px;
  line-height: 50px;
  padding-left: 8px;
}
.checked-box {
  height: 556px;
  overflow-y: auto;
  .checked-item {
    padding: 0 8px;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 34px;
    border-bottom: 1px solid #ebeef5;
    .checked-item-name {
      flex: 1;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    .checked-item-icon {
      cursor: pointer;
    }
  }
  .checked-item:hover {
    background: aliceblue;
  }
}
.background_fa {
  background: #fafafa;
}
</style>

<template>
  <div class="ddRole ddportal-ui">
    <el-form :inline="true" class="formQuery">
      <el-row>
        <el-col :span="16">
          <!-- 查询 -->
          <div class="grid-content bg-purple">
            <el-form-item label="角色名称" prop="roleName">
              <el-input v-model.trim="formQuery.roleName" clearable placeholder="请输入角色名称" size="small"></el-input>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="8">
          <el-form-item class="search_button_com">
            <el-button type="primary" icon="el-icon-search" :disabled="btnDisabled" class="mb5" size="small" @click="onQuery(true)">
              查询
            </el-button>
            <el-button type="primary" icon="el-icon-circle-plus-outline" plain size="small" @click="addDate">
              新增
            </el-button>
            <!-- <el-button
              @click="downloadTableExcel"
              type="primary"
              plain
              :icon="downLoadIcon"
              :disabled="isDisabled"
              class="mb5"
              size="small"
            >{{downLoadText}}</el-button>-->
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <div style="vertical-align: middle;display: inline-block">
      <div class="color-box"></div>
    </div>
    <span class="title-style">角色列表</span>

    <el-table
      ref="multipleTable"
      :data="tableData"
      :default-sort="{ prop: 'createDate', order: 'descending' }"
      stripe
      id="standard-table"
      @sort-change="handleSortChange"
      v-loading="tableLoading"
      :cell-style="{ height: '40px', fontSize: '14px' }"
      :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
      style="width: 100%"
    >
      <el-table-column prop="roleName" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="角色名称" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.roleName | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="roleCodeName"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="角色类型"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.roleCodeName | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="statusName" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="角色状态" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span v-if="scope.row.statusName == '禁用'" style="color:red">
            {{ scope.row.statusName | noDataFilter }}
          </span>
          <span v-else>{{ scope.row.statusName | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="fundFlag" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="产品权限" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.fundFlag | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="roleDesc" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="简介" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.roleDesc | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="remark" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="备注" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.remark | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="createDate" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="创建日期" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.createDate | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column label="操作" min-width="300" align="center">
        <template slot-scope="scope">
          <div>
            <el-button type="info" plain size="small" @click="editData(scope.row)">编辑</el-button>
            <el-button type="info" plain size="small" @click="delData(scope.row)">删除</el-button>
            <el-button type="info" plain size="small" @click="menuSet(scope.row)">菜单权限设置</el-button>
            <el-button type="info" plain size="small" @click="roleSet(scope.row)">角色授予</el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <Pagination :total="total" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination"></Pagination>

    <!-- 新增/修改 参数弹窗 -->
    <el-dialog title="角色管理" center :visible.sync="dialogMask" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox">
          <el-form :inline="true" ref="formDialog" :model="formDialog" :rules="dialogRules" label-position="right">
            <el-form-item label="角色编码" prop="realCode" class="mb20" :label-width="formLabelWidth">
              <el-input v-if="operationType == 1" v-model.trim="formDialog.realCode" clearable style="width:200px" placeholder="请输入"></el-input>
              <el-input v-else v-model.trim="formDialog.realCode" clearable placeholder="请输入" style="width:200px" disabled></el-input>
            </el-form-item>
            <el-form-item label="角色名称" prop="roleName" class="mb20" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog.roleName" clearable placeholder="请输入" style="width:200px"></el-input>
            </el-form-item>
            <el-form-item label="角色类型" prop="roleCode" class="mb20" :label-width="formLabelWidth">
              <el-select v-model.trim="formDialog.roleCode" placeholder="请选择" style="width:200px">
                <el-option v-for="(item, index) in roleTypeList" :key="index" :label="item.dimNme" :value="item.dimCde"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="产品权限" prop="fundFlag" class="mb20" :label-width="formLabelWidth">
              <el-select v-model.trim="formDialog.fundFlag" placeholder="请选择" style="width:200px">
                <el-option v-for="(item, index) in fundFlagList" :key="index" :label="item.dimNme" :value="item.dimCde"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="状态" prop="status" class="mb20" :label-width="formLabelWidth">
              <el-select v-model.trim="formDialog.status" placeholder="请选择" style="width:200px">
                <el-option v-for="(item, index) in statusList" :key="index" :label="item.dimNme" :value="item.dimCde"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="简介" prop="roleDesc" class="mb20" :label-width="formLabelWidth" style="width:100%">
              <el-input v-model.trim="formDialog.roleDesc" clearable placeholder="请输入" type="textarea" style="width:525px"></el-input>
            </el-form-item>
            <el-form-item label="备注 " prop="remark" class="mb20" :label-width="formLabelWidth" style="width:100%">
              <el-input v-model.trim="formDialog.remark" clearable placeholder="请输入" type="textarea" style="width:525px"></el-input>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>

      <div slot="footer" class="dialog-footer standard-form">
        <el-button :loading="countSubmit_btn" type="primary" size="small" @click="dealData">提 交</el-button>
        <el-button size="small" type="info" plain @click="dialogMask = false">取 消</el-button>
      </div>
    </el-dialog>

    <!-- 菜单权限设置 参数2弹窗 -->
    <el-dialog title="菜单权限设置" center :visible.sync="dialogMask2" :close-on-click-modal="false">
      <div style="margin:20px 0;">角色 : {{ formDialog2.roleName }}</div>
      <el-tree
        ref="TreeData"
        :data="TreeData"
        :props="defaultProps"
        :show-checkbox="true"
        node-key="id"
        accordion
        v-loading="treeLoading"
        @check="handleCheckChange"
        :default-checked-keys="checkedArr"
        :check-strictly="true"
      ></el-tree>

      <div slot="footer" class="dialog-footer standard-form">
        <el-button :loading="countSubmit_btn" type="primary" size="small" @click="keepMenuSet">
          提 交
        </el-button>
        <el-button size="small" type="info" plain @click="dialogMask2 = false">取 消</el-button>
      </div>
    </el-dialog>

    <!-- 角色授予 参数3弹窗 -->
    <el-dialog title="角色授予" center :visible.sync="dialogMask3" :close-on-click-modal="false">
      <div style="margin:20px 0;">角色 : {{ formDialog3.roleName }}</div>
      <el-tree
        ref="TreeData2"
        :data="TreeData2"
        :props="defaultProps2"
        :show-checkbox="true"
        node-key="id"
        accordion
        v-loading="treeLoading2"
        @check="handleCheckChange2"
        :default-checked-keys="checkedArr2"
        :default-expand-all="true"
      ></el-tree>

      <div slot="footer" class="dialog-footer standard-form">
        <el-button :loading="countSubmit_btn" type="primary" size="small" @click="keepUserSet">
          保 存
        </el-button>
        <el-button size="small" type="info" plain @click="dialogMask3 = false">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import store from '@/store'
import commonApi from '@/api/role'
import Pagination from '@/components/Pagination'
import fun from '@/filters/common'

export default {
  name: 'DdRole',
  components: {
    Pagination
  },
  props: {
    baseApi: {
      type: String
    },
    token: {
      type: String
    }
  },

  data() {
    return {
      TreeData: [], //菜单设置树
      treeLoading: false, // 树加载
      // tree数据渲染字段
      defaultProps: {
        children: 'children',
        label: 'label'
      },
      TreeData2: [], //角色授权树
      treeLoading2: false, // 树加载
      // tree数据渲染字段
      defaultProps2: {
        children: 'children',
        label: 'label'
      },
      tableData: [], //表格 数据
      tableLoading: false, //表格 加载
      dialogMask: false, // 弹窗
      dialogMask2: false, // 弹窗2
      dialogMask3: false, // 弹窗3

      total: 0, //总数
      // 顶部查询条件
      formQuery: {
        // 角色名称
        roleName: '',
        // 排序字段
        orderString: 'createDate desc',
        // 起始页
        pageNum: 1,
        // 每页大小
        pageSize: 10
      },
      // 添加、编辑 弹窗参数
      formDialog: {
        // 角色代码
        realCode: '',
        // 角色名称
        roleName: '',
        // 角色类型
        roleCode: 'PUBLIC',
        // 角色类型是 PUBLIC 传1 ，其余是0
        roleType: 1,
        // 产品权限
        fundFlag: '',
        // 状态
        status: 0,
        // 简介
        roleDesc: '',
        // 备注
        remark: ''
      },
      // 编辑用的 角色id
      roleId: '',
      // 角色类型-字典查询
      roleTypeList: [],
      // 产品权限-字典查询
      fundFlagList: [],
      // 状态-字典查询
      statusList: [],
      // 弹窗验证规则
      dialogRules: {
        // 角色代码
        realCode: [{ required: true, message: '请填写角色代码', trigger: 'change' }],
        // 角色名称
        roleName: [{ required: true, message: '请填写角色名称', trigger: 'change' }]
      },
      // 菜单设置 弹窗2参数
      formDialog2: {
        // true或false
        operationParam: false,
        // 角色id
        roleId: '',
        // 角色名称
        roleName: ''
      },
      // 角色授权 弹窗3参数
      formDialog3: {
        // 角色id
        roleId: '',
        // 角色名称
        roleName: ''
      },
      // 菜单id数组
      actionIds: [],
      // 菜单权限管理
      checkedArr: [],
      // 角色授权
      checkedArr2: [],
      // 角色 ID 数组
      userIds: [],
      // 操作类型 1、添加 2、编辑
      operationType: 1,
      // 表单宽度
      formLabelWidth: '140px',
      // 查询按钮禁用
      btnDisabled: false,
      /* 按钮禁止与否 */
      isDisabled: false,
      // 导出图标
      downLoadIcon: 'el-icon-download',
      // 导出提示文字
      downLoadText: '导出数据',
      countSubmit_btn: false
    }
  },
  watch: {
    // 获取baseApi
    baseApi: function(newData) {
      store.commit('BASE_API', this.baseApi)
    },
    // 获取token
    token: function(newData) {
      store.commit('TOKEN', this.token)
      this.onQuery(false)
      // // 字典查询
      this.edims('SYS_ROLE_CODENAME')
      this.edims('SYS_ROLE_FLAGNAME')
      this.edims('SYS_ROLE_STATUS')
    }
  },
  mounted() {
    this.onQuery(false)
    // // 字典查询
    this.edims('SYS_ROLE_CODENAME')
    this.edims('SYS_ROLE_FLAGNAME')
    this.edims('SYS_ROLE_STATUS')
  },
  methods: {
    // 字典查询
    edims(type) {
      let dimType = type
      commonApi
        .edimsCommon(dimType)
        .then(res => {
          let { data } = res.data
          if (type == 'SYS_ROLE_CODENAME') {
            // 角色类型
            this.roleTypeList = data
            // this.formDialog.roleCode = this.roleTypeList[0].dimCde;
          } else if (type == 'SYS_ROLE_FLAGNAME') {
            // 产品权限
            this.fundFlagList = data
            this.formDialog.fundFlag = this.fundFlagList[1].dimCde
          } else if (type == 'SYS_ROLE_STATUS') {
            // 状态
            this.statusList = data
            this.formDialog.status = this.statusList[1].dimCde
          }
        })
        .catch(() => {})
    },
    // 查询
    onQuery(flag) {
      this.tableLoading = true

      if (flag) {
        this.formQuery.pageNum = 1
      }
      let params = Object.assign({}, this.formQuery)

      commonApi
        .getScherList(params)
        .then(res => {
          let { list, total } = res.data.data
          this.tableData = list
          this.total = total
          this.tableLoading = false
        })
        .catch(() => {})
    },
    // 添加时 验证代码唯一性
    onlyCode() {
      let params = { realCode: this.formDialog.realCode }
      commonApi
        .checkCode(params)
        .then(res => {
          if (res.data.error) {
            this.$message.closeAll()
            this.$message.error('角色编码已经存在，请勿重复添加！')
            this.countSubmit_btn = false
          } else {
            this.addRoles()
          }
        })
        .catch(() => {
          this.countSubmit_btn = false
        })
    },
    // 处理数据
    dealData() {
      this.$refs['formDialog'].validate(valid => {
        if (valid) {
          this.countSubmit_btn = true
          if (this.operationType === 1) {
            // 添加
            this.onlyCode()
          } else {
            // 修改
            this.updateParamSet()
          }
        }
      })
    },
    // 新增按钮
    addDate() {
      this.dialogMask = true
      this.operationType = 1
      this.$nextTick(() => {
        this.$refs['formDialog'].resetFields()
      })
    },
    // 添加数据
    addRoles() {
      let params = Object.assign({}, this.formDialog)
      if (params.roleCode == 'PUBLIC') {
        params.roleType = 1
      } else {
        params.roleType = 0
      }
      commonApi
        .addRole(params)
        .then(res => {
          if (res.data.status === 200) {
            this.onQuery(false)
            this.$message.closeAll()
            this.$message({
              type: 'success',
              message: res.data.message
            })
            this.dialogMask = false
          }
          this.countSubmit_btn = false
        })
        .catch(() => {
          this.countSubmit_btn = false
        })
    },
    //修改
    editData(row) {
      this.dialogMask = true
      this.operationType = 2
      this.$nextTick(() => {
        let { realCode, roleName, roleCode, fundFlag, fundFlagCompany, status, roleDesc, remark, roleId } = row

        this.formDialog.realCode = realCode
        this.formDialog.roleName = roleName
        this.formDialog.roleCode = roleCode
        this.formDialog.fundFlag = fundFlagCompany
        this.formDialog.status = status
        this.formDialog.roleDesc = roleDesc
        this.formDialog.remark = remark
        this.roleId = roleId
      })
    },
    // 修改数据
    updateParamSet() {
      let params = Object.assign({}, this.formDialog)
      params.roleId = this.roleId
      if (params.roleCode == 'PUBLIC') {
        params.roleType = 1
      } else {
        params.roleType = 0
      }

      commonApi
        .updateRole(params)
        .then(res => {
          if (res.data.status === 200) {
            this.onQuery(false)
            this.$message.closeAll()
            this.$message({
              type: 'success',
              message: res.data.message
            })
            this.dialogMask = false
          } else {
            this.$message.closeAll()

            this.$message.error(res.data.message)
          }
          this.countSubmit_btn = false
        })
        .catch(() => {
          this.countSubmit_btn = false
        })
    },
    //删除
    delData(row) {
      this.$confirm('确认删除该条数据?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          // 删除单个
          this.deleteParamSet(row.roleId)
        })
        .catch(() => {})
    },
    // 删除数据
    deleteParamSet(roleId) {
      let params = { roleId }
      commonApi
        .deleteRole(params)
        .then(res => {
          if (!res.data.error) {
            this.onQuery(false)
            this.$message.closeAll()
            this.$message({
              type: 'success',
              message: res.data.message
            })
          } else {
            this.$message.closeAll()
            this.$message.error(res.data.message)
          }
        })
        .catch(() => {})
    },
    // 菜单权限设置按钮
    menuSet(row) {
      this.dialogMask2 = true
      this.$nextTick(() => {
        let { roleId, roleName } = row
        this.formDialog2.roleId = roleId
        this.formDialog2.roleName = roleName
        this.findMenuSet()
      })
    },
    // 菜单权限设置 列表
    findMenuSet() {
      this.treeLoading = true
      let params = Object.assign({}, this.formDialog2)

      commonApi
        .roleActionSet(params)
        .then(res => {
          this.treeLoading = false
          let { ztreeList } = res.data.data
          this.TreeData = fun.TreeDataPId(ztreeList, 0).data
          this.checkedArr = []
          ztreeList.map(item => {
            if (item.checked == 'true') {
              this.checkedArr.push(item.id)
              this.actionIds.push(item.actionId)
            }
          })
        })
        .catch(() => {})
    },
    // 保存菜单权限设置
    keepMenuSet() {
      let roleIds = []
      roleIds.push(this.formDialog2.roleId)
      let dto = {
        roleIds: roleIds,
        actionIds: this.actionIds
      }
      this.countSubmit_btn = true
      commonApi
        .roleActions(dto)
        .then(res => {
          this.dialogMask2 = false
          this.countSubmit_btn = false
          if (!res.data.error) {
            this.onQuery(false)
            this.$message.closeAll()
            this.$message({
              type: 'success',
              message: res.data.message
            })
          } else {
            this.$message.closeAll()
            this.$message.error(res.data.message)
          }
        })
        .catch(() => {
          this.countSubmit_btn = false
        })
    },
    handleCheckChange(data, checked, indeterminate) {
      let arr = checked.checkedNodes
      let Pidarr = checked.halfCheckedNodes
      this.actionIds = []
      arr.forEach(item => {
        this.actionIds.push(item.actionId)
      })
      if (Pidarr) {
        Pidarr.forEach(item => {
          this.actionIds.push(item.actionId)
        })
      }
    },
    // 角色授权 按钮
    roleSet(row) {
      this.dialogMask3 = true
      this.$nextTick(() => {
        let { roleId, roleName } = row
        this.formDialog3.roleId = roleId
        this.formDialog3.roleName = roleName
        this.findUserSet()
      })
    },
    // 角色管理 列表
    findUserSet() {
      this.treeLoading2 = true
      let params = Object.assign({}, this.formDialog3)
      commonApi
        .roleUserSet(params)
        .then(res => {
          this.treeLoading2 = false
          let { ztreeList } = res.data.data
          this.TreeData2 = fun.TreeDataPId(ztreeList, 0).data
          this.checkedArr2 = []
          ztreeList.map(item => {
            if (item.checked == 'true' && !item.children) {
              this.checkedArr2.push(item.id)
            }
          })
        })
        .catch(() => {})
    },
    handleCheckChange2(data, checked, indeterminate) {
      let arr = checked.checkedNodes
      this.userIds = []
      arr.forEach(item => {
        if (item.userId) {
          this.userIds.push(item.userId)
        }
      })
    },
    //保存角色管理
    keepUserSet() {
      let roleIds = []
      roleIds.push(this.formDialog3.roleId)
      let dto = {
        roleIds: roleIds,
        userIds: this.userIds
      }
      this.countSubmit_btn = true
      commonApi
        .roleUsers(dto)
        .then(res => {
          this.dialogMask3 = false
          this.countSubmit_btn = false
          if (!res.data.error) {
            this.onQuery(false)
            this.$message.closeAll()
            this.$message({
              type: 'success',
              message: res.data.message
            })
          } else {
            this.$message.closeAll()
            this.$message.error(res.data.message)
          }
        })
        .catch(() => {
          this.countSubmit_btn = false
        })
    },
    // 下载Excel
    downloadTableExcel() {},
    //列表点击排序
    handleSortChange(val) {
      this.formQuery.orderString = fun.queryOrderBy(val)
      // 查询
      this.onQuery(false)
    },
    //  分页
    pagination(val) {
      let { page, limit } = val
      // 起始页
      this.formQuery.pageNum = page
      // 每页数量
      this.formQuery.pageSize = limit
      // 查询
      this.onQuery(false)
    }
  }
}
</script>

<style lang="scss" scoped>
::v-deep .el-button.el-button--info {
  background-color: #fff;
  color: #612d10;
}
::v-deep .el-tree-node__expand-icon.is-leaf {
  display: block !important;
}
.ddRole {
  padding-left: 8px;
  .el-dialog {
    width: 60% !important;
    .el-form {
      width: 100% !important;
      font-size: 0;
    }
    .el-input {
      // width: 120% !important;
    }
    .el-form-item {
      min-width: 50%;
      margin-right: 0;
    }
    .mr5 {
      margin-right: 5px;
    }
  }

  .mb20 {
    margin-bottom: 15px !important;
  }

  // 火狐移除
  input[type='number'] {
    -moz-appearance: textfield;
  }

  //谷歌下的移除
  input[type='number']::-webkit-inner-spin-button,
  input[type='number']::-webkit-outer-spin-button {
    -webkit-appearance: none;
  }
}

.title-style {
  color: #333 !important;
  vertical-align: middle;
  height: 35px;
  line-height: 35px;
  font-size: 16px;
  margin-left: 5px;
}
.color-box {
  display: inline-block;
  height: 30px;
  width: 2px;
  background-color: #e1b997;
}

::v-deep .el-table tbody tr:hover > td {
  background-color: transparent !important; //修改成自己想要的颜色即可
}

::v-deep .el-table--striped .el-table__body tr.el-table__row--striped td {
  background: #f7f7f7 !important;
}

::v-deep .el-button.el-button--info {
  color: #333;
  background-color: #dddddd;
  border-color: #dddddd;
}

::v-deep .el-dialog__wrapper .el-dialog__header span {
  color: #333 !important;
}
</style>

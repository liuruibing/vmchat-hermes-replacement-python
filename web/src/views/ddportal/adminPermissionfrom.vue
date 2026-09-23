<template>
  <div class="DdAdminPermissionfrom ddportal-ui">
    <el-container>
      <el-aside width="372px">
        <div class="grid-content">
          <el-row>
            <el-col :span="1">
              <div class="forms_table_title"></div>
            </el-col>
            <el-col :span="23">
              <el-form :inline="true" class="formQuery">
                <el-form-item label="授权模式" prop="choseUser" class="shouquan">
                  <el-select v-model="choseUser" size="small" placeholder="请选择" style="width: 120px !important">
                    <el-option value="0" label="单用户授权"></el-option>
                    <el-option value="1" label="多用户授权"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="搜索" prop="filterText">
                  <el-input v-model="filterText" size="small" clearable placeholder="请输入内容" style="width: 120px !important;margin-top: 2px;"></el-input>
                </el-form-item>
              </el-form>
            </el-col>
          </el-row>
        </div>

        <div style="vertical-align: middle;display: inline-block">
          <div class="color-box"></div>
        </div>
        <span class="title-style">用户列表</span>
        <br />

        <div>
          <el-scrollbar class="content_tree">
            <el-tree
              v-show="choseUser == 0"
              ref="TreeData"
              :data="TreeData"
              :props="defaultProps"
              node-key="id"
              :indent="30"
              class="standard-tree"
              v-loading="treeLoading"
              @node-click="handleNodeClick"
              :default-expand-all="true"
              :filter-node-method="filterNode"
            ></el-tree>
            <el-tree
              v-show="choseUser == 1"
              ref="TreeData2"
              :data="TreeData2"
              :props="defaultProps2"
              :show-checkbox="true"
              node-key="id"
              :indent="30"
              v-loading="treeLoading2"
              @check="handleCheckChange"
              :default-expand-all="true"
              :filter-node-method="filterNode"
            ></el-tree>
          </el-scrollbar>
        </div>
      </el-aside>
      <el-main style="padding-left:15px!important;">
        <el-form :inline="true" class="formQuery">
          <div>
            <el-row>
              <el-col :span="19">
                <!-- 查询 -->
                <div>
                  <el-form-item label="产品代码" prop="fundCode">
                    <el-input v-model.trim="formQuery.fundCode" clearable placeholder="请输入产品代码" size="small"></el-input>
                  </el-form-item>
                  <el-form-item label="产品名称" prop="fundName">
                    <el-input v-model.trim="formQuery.fundName" clearable placeholder="请输入产品名称" size="small"></el-input>
                  </el-form-item>
                  <el-form-item label="管理人名称" prop="remark">
                    <el-input v-model.trim="formQuery.remark" clearable placeholder="请输入管理人名称" size="small"></el-input>
                  </el-form-item>
                  <el-form-item label="机构名称" prop="companyId">
                    <el-select v-model="formQuery.companyId" clearable size="small" placeholder="请选择">
                      <el-option value label="全部"></el-option>
                      <el-option v-for="(group, index) in companyIdArr" :value="group.companyId" :key="index" :label="group.deptName"></el-option>
                    </el-select>
                  </el-form-item>
                  <!-- <el-form-item label="组合类型" prop="fundTypes">
                     <el-select
                       v-model="formQuery.fundTypes"
                       clearable
                       multiple
                       size="small"
                       placeholder="请选择"
                     >
                       <el-option
                         v-for="(group, index) in fundTypesArr"
                         :value="group.dimCde"
                         :key="index"
                         :label="group.dimNme"
                       ></el-option>
                     </el-select>
                   </el-form-item>-->
                </div>
              </el-col>
              <el-col :span="5">
                <el-form-item class="search_button_com">
                  <el-button type="primary" :disabled="btnDisabled" class="mb5" size="small" @click="onQuery">查询</el-button>
                  <el-button v-show="choseUser == 1" type="primary" plain size="small" @click="addDate">产品授权</el-button>
                  <el-button v-show="choseUser == 0" type="primary" plain size="small" @click="addDate2">批量授权</el-button>
                </el-form-item>
              </el-col>
            </el-row>

            <div style="vertical-align: middle;display: inline-block">
              <div class="color-box"></div>
            </div>
            <span class="title-style">产品授权列表</span>
            <el-table
              ref="multipleTable"
              @selection-change="handleSelectionChange"
              :data="tableData"
              border
              stripe
              id="standard-table"
              @sort-change="handleSortChange"
              v-loading="tableLoading"
              style="width: 100%"
            >
              <el-table-column fixed type="selection" width="35" align="center"></el-table-column>

              <el-table-column prop="fundCode" show-overflow-tooltip label="产品代码" min-width="60" algin="left" header-align="center">
                <template slot-scope="scope">
                  <span>{{ scope.row.fundCode | noDataFilter }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="fundName" show-overflow-tooltip label="产品名称" min-width="100" algin="left" header-align="center">
                <template slot-scope="scope">
                  <span>{{ scope.row.fundName | noDataFilter }}</span>
                </template>
              </el-table-column>

              <el-table-column prop="companyName" show-overflow-tooltip label="机构名称" min-width="70" algin="left" header-align="center">
                <template slot-scope="scope">
                  <span>{{ scope.row.companyName | noDataFilter }}</span>
                </template>
              </el-table-column>

              <el-table-column prop="source" show-overflow-tooltip label="管理人名称" min-width="70" algin="left" header-align="center">
                <template slot-scope="scope">
                  <span>{{ scope.row.source | noDataFilter }}</span>
                </template>
              </el-table-column>
            </el-table>
            <!-- 分页 -->
            <el-row>
              <Pagination :total="total" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination"></Pagination>
            </el-row>
          </div>

          <div v-show="choseUser == 0">
            <div style="border-bottom:1px solid #909399 ;height:20px;margin-bottom:20px"></div>
            <el-row>
              <el-col :span="19">
                <!-- 查询 -->
                <div>
                  <el-form-item label="产品代码" prop="fundCode">
                    <el-input v-model.trim="formQuery2.fundCode" clearable placeholder="请输入产品代码" size="small"></el-input>
                  </el-form-item>
                  <el-form-item label="产品名称" prop="fundName">
                    <el-input v-model.trim="formQuery2.fundName" clearable placeholder="请输入产品名称" size="small"></el-input>
                  </el-form-item>

                  <!-- <el-form-item label="产品权限明细" prop="detailGrant">
                    <el-select
                      v-model="formQuery2.detailGrant"
                      clearable
                      size="small"
                      placeholder="请选择"
                    >
                      <el-option
                        v-for="(group, index) in detailGrantArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme"
                      ></el-option>
                    </el-select>
                  </el-form-item> -->
                  <!--  <el-form-item label="组合类型" prop="fundTypes">
                      <el-select
                        v-model="formQuery2.fundTypes"
                        clearable
                        multiple
                        size="small"
                        placeholder="请选择"
                      >
                        <el-option
                          v-for="(group, index) in fundTypesArr"
                          :value="group.dimCde"
                          :key="index"
                          :label="group.dimNme"
                        ></el-option>
                      </el-select>
                    </el-form-item>-->
                </div>
              </el-col>
              <el-col :span="5">
                <el-form-item class="search_button_com">
                  <el-button type="primary" :disabled="btnDisabled" class="mb5" size="small" @click="onQuery2">查询</el-button>
                  <el-button type="primary" plain size="small" @click="deleteDate">批量删除</el-button>
                </el-form-item>
              </el-col>
            </el-row>

            <div v-if="formQuery2.userId">
              <div class="forms_table_title">
                <i class="el-icon-tickets"></i>
                用户：{{ singleUser }} 目前已拥有权限
              </div>
              <el-table
                ref="multipleTable2"
                @selection-change="handleSelectionChange2"
                :data="tableData2"
                border
                stripe
                @sort-change="handleSortChange2"
                v-loading="tableLoading2"
                style="width: 100%"
              >
                <el-table-column fixed type="selection" width="35" align="center"></el-table-column>

                <el-table-column
                  prop="fundCode"
                  show-overflow-tooltip
                  label="产品代码"
                  min-width="60"
                  sortable="custom"
                  :sort-orders="['ascending', 'descending']"
                  algin="left"
                  header-align="center"
                >
                  <template slot-scope="scope">
                    <span>{{ scope.row.fundCode | noDataFilter }}</span>
                  </template>
                </el-table-column>
                <el-table-column
                  prop="fundName"
                  show-overflow-tooltip
                  label="产品名称"
                  sortable="custom"
                  :sort-orders="['ascending', 'descending']"
                  min-width="100"
                  algin="left"
                  header-align="center"
                >
                  <template slot-scope="scope">
                    <span>{{ scope.row.fundName | noDataFilter }}</span>
                  </template>
                </el-table-column>

                <el-table-column
                  prop="companyName"
                  show-overflow-tooltip
                  label="机构名称"
                  min-width="70"
                  sortable="custom"
                  :sort-orders="['ascending', 'descending']"
                  algin="left"
                  header-align="center"
                >
                  <template slot-scope="scope">
                    <span>{{ scope.row.companyName | noDataFilter }}</span>
                  </template>
                </el-table-column>

                <el-table-column
                  prop="source"
                  show-overflow-tooltip
                  label="管理人名称"
                  min-width="70"
                  sortable="custom"
                  :sort-orders="['ascending', 'descending']"
                  algin="left"
                  header-align="center"
                >
                  <template slot-scope="scope">
                    <span>{{ scope.row.source | noDataFilter }}</span>
                  </template>
                </el-table-column>
              </el-table>
              <!-- 分页 -->
              <Pagination :total="total2" :limit="formQuery2.pageSize" :page="formQuery2.pageNum" @pagination="pagination2"></Pagination>
            </div>

            <div class="forms_table_title" v-else>点击一个用户名称查看其已拥有的产品信息</div>
          </div>
        </el-form>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import store from '@/store'
import commonApi from './js/adminPermissionfrom.js'
import fun from '@/filters/common'
import Pagination from '@/components/Pagination'

export default {
  name: 'DdAdminPermissionfrom',
  components: { Pagination },
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

      TreeData2: [], //菜单2设置树
      treeLoading2: false, // 树2加载
      // tree数据渲染字段
      defaultProps2: {
        children: 'children',
        label: 'label'
      },
      //单用户和多用户切换
      choseUser: '0',
      // 搜索
      filterText: '',
      // 查询列表
      formQuery: {
        // 产品代码
        fundCode: '',
        // 产品名称
        fundName: '',
        // 组合类型
        fundTypes: [],
        // 机构id
        companyId: '',
        // 管理人名称
        remark: '',
        // 排序
        orderString: 'fundCode desc nulls last',
        // 起始页
        pageNum: 1,
        // 每页大小
        pageSize: 10,
        //用户id
        userId: ''
      },
      // 机构
      companyIdArr: [],
      // 组合类型
      fundTypesArr: [],
      // 访问权限
      detailGrantArr: [],
      tableData: [],
      tableLoading: false,
      total: 0, //总数
      // 查询列表
      formQuery2: {
        // 用户id
        userId: '',
        // 产品明细权限
        detailGrant: '',
        // 产品代码
        fundCode: '',
        // 产品名称
        fundName: '',
        // 组合类型
        fundTypes: [],
        // 为1表示查询机构和产品，其他表示只查询机构
        fundStyle: '1',
        // 为1表示查询可授予的权限（机构和产品），其他表示查询已拥有的权限
        isGrantOrQuery: '1',
        //为1表示非外部调用此方法(针对非权限模块的调用)
        isInvoke: '1',
        // 排序
        orderString: 'fundCode desc nulls last',
        // 起始页
        pageNum: 1,
        // 每页大小
        pageSize: 10
      },
      tableData2: [],
      tableLoading2: false,
      total2: 0, //总数
      // 查询按钮禁用
      btnDisabled: false,
      dto: {
        userIds: [],
        fundCodes: [],
        deptIds: [],
        nodes: []
      },
      //单用户名
      singleUser: '',
      // 表格选择
      multipleSelection: [],
      // 表格2选择
      multipleSelection2: '',
      newAccount: []
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
      // 默认多用户
      this.userZtrees()
      // 查询
      this.onQuery()
      // 下拉框
      this.companys()
      // 字典查询
      this.edims('fund_type')
      this.edims('SYS_PERMISSION_FUNDINRIGHT')
    },
    filterText(val) {
      if (this.choseUser == 1) {
        // 多用户
        this.$refs.TreeData2.filter(val)
      } else {
        // 单用户
        this.$refs.TreeData.filter(val)
      }
    },
    choseUser(val) {
      this.onQuery()
      if (val == 1) {
        // 多用户
        this.usersZtree()
      } else {
        // 单用户
        this.userZtrees()
      }

      // 清除选中的
      this.$refs.multipleTable.clearSelection()
      // 清除上个用户拥有的选项
    },
    // 监听上面组合类型变化
    'formQuery.fundTypes'(val, oldval) {
      if (val.length == this.fundTypesArr.length && oldval.length == 0) {
        this.formQuery.fundTypes.splice(val.indexOf('*'), 1)
      } else if (val.indexOf('*') != -1 && oldval.indexOf('*') == -1 && val.length > 1) {
        this.formQuery.fundTypes = this.newAccount
      } else if (val.indexOf('*') != -1 && oldval.indexOf('*') != -1 && val.length > 1) {
        this.formQuery.fundTypes.splice(val.indexOf('*'), 1)
      } else if (val.length == this.fundTypesArr.length - 1 && val.indexOf('*') == -1 && oldval.indexOf('*') !== -1) {
        this.formQuery.fundTypes = ['*']
      } else if (val.length !== this.fundTypesArr.length - 1 && val.indexOf('*') == -1 && oldval.indexOf('*') !== -1) {
        this.formQuery.fundTypes = this.newAccount
      }
    },
    // 监听单用户组合类型变化
    'formQuery2.fundTypes'(val, oldval) {
      if (val.length == this.fundTypesArr.length && oldval.length == 0) {
        this.formQuery2.fundTypes.splice(val.indexOf('*'), 1)
      } else if (val.indexOf('*') != -1 && oldval.indexOf('*') == -1 && val.length > 1) {
        this.formQuery2.fundTypes = this.newAccount
      } else if (val.indexOf('*') != -1 && oldval.indexOf('*') != -1 && val.length > 1) {
        this.formQuery2.fundTypes.splice(val.indexOf('*'), 1)
      } else if (val.length == this.fundTypesArr.length - 1 && val.indexOf('*') == -1 && oldval.indexOf('*') !== -1) {
        this.formQuery2.fundTypes = ['*']
      } else if (val.length !== this.fundTypesArr.length - 1 && val.indexOf('*') == -1 && oldval.indexOf('*') !== -1) {
        this.formQuery2.fundTypes = this.newAccount
      }
    }
  },
  mounted() {
    // 默认多用户
    this.userZtrees()
    // 查询
    this.onQuery()
    // 下拉框
    this.companys()
    // 字典查询
    this.edims('fund_type')
    this.edims('SYS_PERMISSION_FUNDINRIGHT')
  },
  methods: {
    filterNode(value, data) {
      if (!value) return true
      return data.label.indexOf(value) !== -1
    },
    //  机构名称下拉框
    companys() {
      let params = { selectType: 0 }
      commonApi
        .companysUrl(params)
        .then(res => {
          if (res.data.data) {
            this.companyIdArr = res.data.data
          }
        })
        .catch(() => {})
    },
    // 字典查询
    edims(type) {
      let dimType = type
      commonApi
        .edimsCommon(dimType)
        .then(res => {
          let { data } = res.data
          if (type == 'fund_type') {
            // 组合类型
            this.fundTypesArr = data
            this.formQuery.fundTypes = [this.fundTypesArr[0].dimCde]
            this.formQuery2.fundTypes = [this.fundTypesArr[0].dimCde]

            for (let i in data) {
              this.newAccount.push(data[i].dimCde)
            }
          } else if (type == 'SYS_PERMISSION_FUNDINRIGHT') {
            // 产品权限明细
            this.detailGrantArr = data
            this.formQuery2.detailGrant = this.detailGrantArr[0].dimCde
          }
        })
        .catch(() => {})
    },
    // 获取左侧树 - 单用户
    userZtrees() {
      this.treeLoading = true
      commonApi
        .userZtreesUrl()
        .then(res => {
          this.treeLoading = false
          if (res.data.data) {
            let { data } = res.data
            this.TreeData = fun.TreeDataPId(data, 0).data
          }
        })
        .catch(() => {})
    },
    // 单用户点击事件
    handleNodeClick(data) {
      if (!data.children) {
        this.singleUser = data.name
        this.formQuery.userId = data.userId
        this.formQuery2.userId = data.userId
        this.onQuery()
        this.onQuery2()
      }
    },
    // 获取左侧树 - 多用户
    usersZtree() {
      this.treeLoading2 = true
      commonApi
        .userZtreesUrl()
        .then(res => {
          this.treeLoading2 = false
          if (res.data.data) {
            let { data } = res.data
            this.TreeData2 = fun.TreeDataPId(data, 0).data
          }
        })
        .catch(() => {})
    },
    // 多用户点击事件
    handleCheckChange(data, checked, indeterminate) {
      this.dto.userIds = []
      checked.checkedNodes.forEach(item => {
        if (!item.children) {
          this.dto.userIds.push(item.userId)
        }
      })
    },
    // 查询
    onQuery() {
      this.tableLoading = true
      let params = Object.assign({}, this.formQuery)
      commonApi
        .userFundZtreesUrl(params)
        .then(res => {
          this.tableData = []
          if (res.data.data) {
            let { list, total } = res.data.data
            this.tableData = list
            this.total = total
            this.tableLoading = false
            // 默认选中
            this.tableData.forEach(item => {
              if (item.checked == 'true') {
                this.$nextTick(() => {
                  this.$refs.multipleTable.toggleRowSelection(item)
                })
              }
            })
          }
        })
        .catch(() => {})
    },
    // 多用户的产品授权
    addDate() {
      if (this.multipleSelection.length) {
        if (this.dto.userIds.length == 0) {
          this.$message.closeAll()
          this.$message({
            type: 'warning',
            message: '请选择用户!'
          })
          return
        }
        this.dto.deptIds = []
        this.dto.fundCodes = []
        this.dto.nodes = []

        this.multipleSelection.forEach(item => {
          this.dto.deptIds.push(item.companyId)
          this.dto.fundCodes.push(item.fundCode)
        })

        for (let i = 0; i < this.dto.deptIds.length; i++) {
          this.dto.nodes.push({})
        }
        commonApi
          .userFundsUrl(this.dto)
          .then(res => {
            if (!res.data.error) {
              this.$message.closeAll()
              this.$message({
                type: 'success',
                message: res.data.message
              })
            } else {
              this.$message.closeAll()
              this.$message({
                type: 'error',
                message: res.data.message
              })
            }
            this.onQuery()
            // 清除
            this.$refs.multipleTable.clearSelection()
          })
          .catch(() => {})
      } else {
        this.$message.closeAll()
        this.$message({
          type: 'warning',
          message: '请选择产品!'
        })
      }
    },
    // 单用户的产品授权
    addDate2() {
      if (this.multipleSelection.length) {
        if (!this.formQuery2.userId) {
          this.$message.closeAll()
          this.$message({
            type: 'warning',
            message: '请选择用户!'
          })
          return
        }
        this.dto.deptIds = []
        this.dto.fundCodes = []
        this.dto.nodes = []
        this.dto.userIds = [this.formQuery2.userId]

        this.multipleSelection.forEach(item => {
          this.dto.deptIds.push(item.companyId)
          this.dto.fundCodes.push(item.fundCode)
        })

        for (let i = 0; i < this.dto.deptIds.length; i++) {
          this.dto.nodes.push({})
        }
        commonApi
          .userFundsUrl(this.dto)
          .then(res => {
            if (!res.data.error) {
              this.$message.closeAll()
              this.$message({
                type: 'success',
                message: res.data.message
              })
            } else {
              this.$message.closeAll()
              this.$message({
                type: 'error',
                message: res.data.message
              })
            }
            this.onQuery()
            this.onQuery2()
            // 清除
            this.$refs.multipleTable.clearSelection()
          })
          .catch(() => {})
      } else {
        this.$message.closeAll()
        this.$message({
          type: 'warning',
          message: '请选择产品!'
        })
      }
    },
    // 单用户查询
    onQuery2() {
      // if (!this.formQuery2.userId) {
      //   this.$message.closeAll();
      //   this.$message({
      //     type: "warning",
      //     message: "请选择用户!"
      //   });
      //   return;
      // }
      this.tableLoading2 = true
      let params = Object.assign({}, this.formQuery2)
      commonApi
        .fundZtreesUrl(params)
        .then(res => {
          this.tableData2 = []
          if (res.data.data.rows) {
            let { list, total } = res.data.data.rows
            this.tableData2 = list
            this.total2 = total
          }
          this.tableLoading2 = false
        })
        .catch(() => {})
    },
    // 单用户批量删除
    deleteDate() {
      if (this.multipleSelection2.length) {
        this.$confirm('确认删除这些数据吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
        })
          .then(() => {
            let dto = {}
            let arr = []
            dto.userIds = [this.formQuery2.userId]
            this.multipleSelection2.forEach(item => {
              arr.push(item.fundCode)
            })
            dto.fundCodes = arr

            commonApi
              .deleteUserFundsUrl(dto)
              .then(res => {
                if (!res.data.error) {
                  this.$message.closeAll()
                  this.$message({
                    type: 'success',
                    message: res.data.message
                  })
                } else {
                  this.$message.closeAll()
                  this.$message({
                    type: 'error',
                    message: res.data.message
                  })
                }
                this.onQuery()
                this.onQuery2()
              })
              .catch(() => {})
          })
          .catch(() => {})
      } else if (this.multipleSelection2.length === 0) {
        this.$message.closeAll()
        this.$message({
          message: '请选择要批量删除的数据',
          type: 'warning'
        })
      }
    },
    // 表格选择
    handleSelectionChange(val) {
      this.multipleSelection = val
    },
    // 表格2选择
    handleSelectionChange2(val) {
      this.multipleSelection2 = val
    },
    //列表点击排序
    handleSortChange(val) {
      this.formQuery.orderString = fun.queryOrderBy(val)
      // 查询
      this.onQuery()
    },
    //列表2点击排序
    handleSortChange2(val) {
      this.formQuery2.orderString = fun.queryOrderBy(val)
      // 查询
      this.onQuery2()
    },
    // 分页
    pagination(val) {
      let { page, limit } = val
      // 起始页
      this.formQuery.pageNum = page
      // 每页数量
      this.formQuery.pageSize = limit
      // 查询
      this.onQuery()
      // 重置
      // this.formQuery.pageNum = 1;
      // this.formQuery.pageSize = 10;
    },
    // 分页
    pagination2(val) {
      let { page, limit } = val
      // 起始页
      this.formQuery2.pageNum = page
      // 每页数量
      this.formQuery2.pageSize = limit
      // 查询
      this.onQuery2()
      // 重置
      // this.formQuery2.pageNum = 1;
      // this.formQuery2.pageSize = 10;
    }
  }
}
</script>

<style lang="scss">
.DdAdminPermissionfrom {
  .grid-content {
    height: 40px;
    line-height: 40px;
    background-color: #f9f0e6;

    .el-input {
      width: 120px !important;
    }

    .shouquan {
      width: 170px !important;
    }

    .sousuo {
      width: 160px !important;
    }
  }

  .content_tree {
    height: calc(100vh - 150px);
  }
}
</style>

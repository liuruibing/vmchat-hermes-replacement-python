<template>
  <div class="DdPosition ddportal-ui">
    <el-container>
      <el-aside width="300px">
        <div class="grid-content bg-purple">
          <div style="padding:5px;background:#f2f2f2;">
            <el-row>
              <el-col :span="8">
                <div class="forms_table_title" style="height:28px;line-height:28px;color:#3f3f3f;font-weight:500;padding-left: 8px">
                  机构列表
                </div>
              </el-col>
              <el-col :span="16">
                <div class="search_button_com">
                  <!-- tableLoading 当查询指标配置表时禁用编辑按钮 -->
                  <el-button type="primary" plain @click="editDataJd()" :disabled="tableLoading" size="small">
                    编辑
                  </el-button>
                  <el-button type="primary" @click="addDataJd()" size="small">新增</el-button>
                </div>
              </el-col>
            </el-row>
          </div>

          <!-- 左侧指标分类树 -->
          <div v-loading="indexTreeDataLeftLoading" style="padding-top:15px;border:1px solid #f2f2f2;min-height:300px;">
            <el-tree
              :data="indexTreeData"
              :props="defaultProps"
              node-key="id"
              :indent="30"
              :expand-on-click-node="false"
              check-strictly
              accordion
              :default-expanded-keys="defaultExpandedKeys"
              :default-checked-keys="defaultCheckedKeys"
              ref="tree"
              show-checkbox
              @check-change="indexHandleNodeChangeLeft"
              @node-click="indexHandleNodeClickLeft"
            ></el-tree>
          </div>
        </div>
      </el-aside>
      <el-main style="padding-left:15px!important;">
        <div class="grid-content bg-purple">
          <div style="padding:5px;background:#f2f2f2;">
            <el-row>
              <el-col :span="5">
                <div class="forms_table_title" style="height:28px;line-height:28px;color:#3f3f3f;font-weight:500;padding-left: 8px">
                  机构列表
                </div>
              </el-col>
            </el-row>
          </div>

          <!-- 左侧指标分类树 -->
          <div v-loading="indexTreeDataLeftLoading" style="padding-top:15px;border:1px solid #f2f2f2;min-height:300px;">
            <el-form ref="formCount" :rules="formInlineRules" :model="formCount" label-width="120px">
              <el-form-item :label="isInstitution ? '机构编码' : '部门编码'" prop="deptCode">
                <el-input v-model="formCount.deptCode" style="width:410px" maxlength="15" placeholder="请输入内容"></el-input>
              </el-form-item>
              <el-form-item :label="isInstitution ? '机构名称' : '部门名称'" prop="deptName">
                <el-input v-model="formCount.deptName" style="width:410px" placeholder="请输入内容"></el-input>
              </el-form-item>
              <el-form-item label="上级部门" v-if="isAdd" prop="deptPname">
                <el-input disabled v-model="formCount.deptPname" style="width:410px" placeholder="请输入内容"></el-input>
              </el-form-item>
              <el-form-item :label="isInstitution ? '机构简介' : '部门简介'" prop="deptDesc">
                <el-input type="textarea" :rows="2" v-model="formCount.deptDesc"></el-input>
              </el-form-item>
              <el-form-item label="备注" prop="remark">
                <el-input type="textarea" :rows="2" v-model="formCount.remark"></el-input>
              </el-form-item>
            </el-form>
            <el-row>
              <el-col :span="6" :offset="18">
                <div class="search_button_com">
                  <!-- tableLoading 当查询指标配置表时禁用编辑按钮 -->
                  <el-button type="info" plain v-show="isEdit" @click="deleteDataJd()" :disabled="tableLoading" size="small">
                    <i class="el-icon-delete"></i>
                    删除
                  </el-button>
                  <el-button type="primary" :loading="submit_btn_load" @click="saveDataJd('formCount')" size="small">
                    <i class="el-icon-circle-plus-outline"></i>
                    保存
                  </el-button>
                </div>
              </el-col>
            </el-row>
          </div>
        </div>
      </el-main>
    </el-container>

    <div style="vertical-align: middle;display: inline-block;margin: 5px 0">
      <div class="color-box"></div>
    </div>
    <span class="title-style">用户信息</span>

    <el-table
      ref="multipleTable"
      @selection-change="handleSelectionChange"
      :data="tableData"
      :default-sort="{ prop: 'userName', order: 'descending' }"
      stripe
      @sort-change="handleSortChange"
      v-loading="tableLoading"
      :cell-style="{ height: '40px', fontSize: '14px' }"
      :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
      style="width: 100%"
    >
      <el-table-column prop="userName" show-overflow-tooltip label="姓名" min-width="100" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.userName | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="userNo" show-overflow-tooltip label="员工编号" min-width="100" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.userNo | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="account" show-overflow-tooltip label="登录账户" min-width="70" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.account | noDataFilter }}</span>
        </template>
      </el-table-column>
      <!--      <el-table-column-->
      <!--        prop="institution"-->
      <!--        show-overflow-tooltip-->
      <!--        label="机构"-->
      <!--        min-width="70"-->
      <!--        algin="left"-->
      <!--        header-align="center"-->
      <!--      >-->
      <!--        <template slot-scope="scope">-->
      <!--          <span>{{ scope.row.institution | noDataFilter }}</span>-->
      <!--        </template>-->
      <!--      </el-table-column>-->
      <el-table-column prop="deptNames" show-overflow-tooltip label="部门" min-width="120" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.deptNames | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="sysUserPoModelListString" show-overflow-tooltip label="岗位" min-width="100" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.sysUserPoModelListString | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="roleNames" show-overflow-tooltip label="角色" min-width="100" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.roleNames | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column prop="statusName" show-overflow-tooltip label="状态" min-width="60" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.statusName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column prop="telePhone" show-overflow-tooltip label="座机" min-width="100" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.telePhone | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column prop="createDate" show-overflow-tooltip label="创建日期" min-width="100" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.createDate | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" min-width="80" align="center">
        <template slot-scope="scope">
          <el-button type="info" plain size="small" @click="editData(scope.row)">岗位维护</el-button>
        </template>
      </el-table-column>
    </el-table>

    <Pagination :total="total" :page="formInline.pageNum" :limit="formInline.pageSize" @pagination="Pagination"></Pagination>

    <!-- 岗位维护 -->
    <el-dialog
      title="添加岗位"
      customClass="customDeptWidth"
      v-dialogDrag
      center
      :visible.sync="countDialog"
      :close-on-click-modal="false"
      :modal-append-to-body="false"
      :append-to-body="true"
    >
      <el-container>
        <el-main class="mainBox">
          <div>
            <el-form :inline="true" ref="formAddInline" :model="formAddInline" style="margin-bottom: 8px;" class="demo-form-inline standard-form">
              <el-row>
                <el-col :span="12">
                  <div style="width:100%;">
                    <el-form-item label="岗位编码" customClass="formDeptWidth" prop="positionCode">
                      <el-input v-model="formAddInline.positionCode" size="small" placeholder="请输入内容"></el-input>
                    </el-form-item>
                    <el-form-item label="岗位名称" customClass="formDeptWidth" prop="positionName">
                      <el-input v-model="formAddInline.positionName" size="small" placeholder="请输入内容"></el-input>
                    </el-form-item>
                    <!-- <el-form-item label="岗位类型" customClass="formDeptWidth" prop="positionType">
                    <el-select size="small" v-model="formAddInline.positionType" placeholder="请选择">
                      <el-option
                        v-for="item in positionTypeArr"
                        :key="item.type"
                        :label="item.name"
                        :value="item.type"
                      ></el-option>
                    </el-select>
                    </el-form-item>-->
                  </div>
                </el-col>
                <el-col :span="12">
                  <el-form-item class="search_button_com">
                    <el-button type="primary" @click="onAddSubmit()" style="margin-bottom: 5px; " size="small">
                      查询
                    </el-button>
                    <el-button type="info" plain @click="addRestForm()" style="margin-bottom: 5px; " size="small">
                      重置
                    </el-button>
                    <el-button type="primary" plain @click="addPosition()" style="margin-bottom: 5px; " size="small">
                      保存岗位
                    </el-button>
                  </el-form-item>
                </el-col>
              </el-row>
            </el-form>
          </div>
          <div>
            <span style="color:red">
              当前用户: {{ positionUserName }}&nbsp;&nbsp;&nbsp;&nbsp;所在部门: {{ positiondeptName }}&nbsp;&nbsp;&nbsp;&nbsp;所在岗位:
              <span id="positionUse">{{ positionList }}</span>
            </span>
          </div>
          <div style="vertical-align: middle;display: inline-block;margin: 5px 0">
            <div class="color-box"></div>
          </div>
          <span class="title-style">岗位列表信息</span>
          <el-table
            ref="multipleAddTable"
            @selection-change="handleAddSelectionChange"
            :data="addTableData"
            :default-sort="{ prop: 'positionCode', order: 'descending' }"
            stripe
            @sort-change="handleAddSortChange"
            v-loading="addTableLoading"
            style="width: 100%"
            :cell-style="{ height: '40px', fontSize: '14px' }"
            :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
          >
            <el-table-column type="selection" width="35" align="center"></el-table-column>

            <el-table-column prop="positionCode" show-overflow-tooltip label="岗位编码" min-width="100" algin="left" header-align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.positionCode | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="posiAndDept" show-overflow-tooltip label="岗位名称" min-width="100" algin="left" header-align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.posiAndDept | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="positionType" show-overflow-tooltip label="岗位类型" min-width="70" algin="left" header-align="center">
              <template slot-scope="scope">
                <span>{{ dataStatus(scope.row.positionType) | noDataFilter }}</span>
              </template>
            </el-table-column>

            <el-table-column prop="remark" show-overflow-tooltip label="描述" min-width="70" algin="left" header-align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.remark | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" min-width="80" align="center">
              <template slot-scope="scope">
                <!-- <span >{{ scope.row.manageDepts | noDataFilter }}</span> -->
                <el-button type="primary" size="small" @click="editDepData(scope.row)">
                  管理部门维护
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <Pagination :total="addTotal" :page="formAddInline.pageNum" :limit="formAddInline.pageSize" @pagination="PaginationAdd"></Pagination>
        </el-main>
      </el-container>

      <el-dialog center :visible.sync="innerVisible" append-to-body>
        <div slot="title">
          <span style="color: #e03d3e!important;font-size: 14px">选择部门</span>
        </div>
        <div v-loading="indexTreeDataAddLoading" style="padding-top:15px;border:1px solid #f2f2f2;min-height:300px;">
          <el-tree
            :data="indexTreeDataAdd"
            :props="defaultProps"
            node-key="id"
            :indent="30"
            :expand-on-click-node="false"
            accordion
            default-expand-all
            :default-checked-keys="defaultCheckedKeysAdd"
            ref="tree"
            show-checkbox
            @check-change="indexHandleNodeChangeAdd"
          ></el-tree>
        </div>
        <span slot="footer" class="dialog-footer">
          <el-button @click="innerVisible = false">取 消</el-button>
          <el-button type="primary" @click="addPositionDept()">确 定</el-button>
        </span>
      </el-dialog>
    </el-dialog>
  </div>
</template>

<script>
import commonFun from '@/filters/common.js'
import Pagination from '@/components/Pagination'
import pageApi from '@/api/ddportal/dept.js'

export default {
  name: 'DdDept',
  components: { Pagination },
  props: {
    currentRow: {
      default: () => {},
      type: Object,
      required: true
    }
  },
  data() {
    return {
      isInstitution: true,
      //部门数组
      institutionArray: [],
      //机构数组
      departmentArray: [],
      //部门数据存储
      saveDeptIdsArray: [],

      indexTreeData: [], //指标树数据
      indexTreeDataDefaultKeys: [], //指标树默认选择
      indexTreeDataLeftLoading: false,
      defaultProps: {
        children: 'children',
        label: 'label'
      }, // 树状类型
      indexTreeSelectLeft: {}, //左侧树选中的label
      isAdd: false, //是否新增
      isEdit: true,
      defaultExpandedKeys: [], //默认展开
      defaultCheckedKeys: [], //默认选中
      formCount: {
        deptCode: '', //部门编码
        deptName: '', //部门名称
        deptPname: '', //上级部门
        deptDesc: '', //部门简介
        remark: '' //备注
      },
      formInline: {
        orderStr: 'userName desc nulls last', //列表排序
        pageSize: 10,
        pageNum: 1
      },
      tableLoading: false, //表格加载
      total: 0,
      // 弹窗验证规则
      formInlineRules: {
        deptCode: [
          {
            required: true,
            type: 'string',
            message: '请输入部门编码',
            trigger: 'change'
          }
        ],
        deptName: [
          {
            required: true,
            type: 'string',
            message: '请输入部门名称',
            trigger: 'change'
          }
        ]
      },
      tableData: [{ deptCode: '001' }], //列表数据
      positionTypeArr: [],
      formAdd: {
        positionCode: '', //岗位编码
        positionName: '', //岗位名称
        positionType: '' //岗位类型
      },
      formAddInline: {
        positionCode: '', //岗位编码
        positionName: '', //岗位名称
        positionType: '', //岗位类型
        orderStr: 'positionCode desc nulls last', //列表排序
        pageSize: 10,
        pageNum: 1
      },
      addTotal: 0,
      countDialog: false, //新增岗位dialog显示控制
      tableMultipleSelection: [], //表格选择数据集合
      addTableMultipleSelection: [], //表格选择数据集合
      addTableData: [{ positionCode: '001' }],
      addTableLoading: false,
      innerVisible: false,
      isCheck: '', //判断是否已经选择
      myDeptId: '', //用户列表查询id
      submit_btn_load: false, //部门保存按钮加载
      isEditAdd: false,
      positionUserName: '', //当前用户
      positiondeptName: '', //所在部门
      positionList: '', //岗位
      positiondeptUserId: '', //userId
      positionTypeArrs: {}, //部门类型
      positionCodes: [], //部门编码数组
      nodeChangeIdArr: [], //tree选中的id
      positionCodeAdd: '', //选择部门保存所需的code
      indexTreeDataAddLoading: false, //部门维护加载
      indexTreeDataAdd: [], //部门维护数据
      indexTreeSelectAdd: '', //部门维护数据选择
      defaultExpandedKeysAdd: [], //部门维护默认展开
      defaultCheckedKeysAdd: [], //默认选中
      deptDetailData: {} //部门详情
    }
  },
  mounted() {
    // this.getDeptIds()
    this.getPositionType()
    this.getDepts()
  },
  methods: {
    // 获取部门的数据结构
    getDeptIds() {
      pageApi
        .getDeptSourceList()
        .then(response => {
          if (!response.data.error) {
            // 重置
            this.institutionArray = []
            // 所有的信息
            this.saveDeptIdsArray = commonFun.TreeDataPId(response.data.data, '0').data
            if (this.saveDeptIdsArray.length > 0) {
              for (let i = 0; i < this.saveDeptIdsArray[0].children.length; i++) {
                let temp = this.saveDeptIdsArray[0].children[i]
                this.institutionArray.push({
                  deptId: temp.deptId,
                  deptName: temp.deptName
                })
              }
            }
          } else {
            this.saveDeptIdsArray = []
            this.institutionArray = []
          }
        })
        .catch(err => {
          this.saveDeptIdsArray = []
          this.institutionArray = []
        })
    },
    //获取菜单tree
    getDepts() {
      // 打开遮罩层
      this.indexTreeDataLeftLoading = true
      let params = {}
      params.companyId = this.currentRow.companyId
      pageApi
        .getDataSourceList(params)
        .then(response => {
          if (!response.data.error) {
            // 指标树数据
            // this.indexTreeData = commonFun.TreeDataPId(response.data.data, '0').data
            let treeData = commonFun.TreeDataPId(response.data.data, '0').data
            for (let i = 0; i < treeData.length; i++) {
              if (this.currentRow.companyId == treeData[i].id) {
                this.indexTreeData = [treeData[i]]
                break
              }
            }
            // 默认搜索指标树
            this.indexTreeDataDefaultKeys[0] = this.indexTreeData[0].id

            // 左侧指标树默认选中指标树
            this.indexTreeSelectLeft = this.indexTreeData[0]
            var deptId = ''
            if (this.isEditAdd) {
              deptId = this.formCount.deptId
              this.defaultExpandedKeys[0] = deptId
              this.defaultCheckedKeys[0] = deptId
            } else if (this.isAdd) {
              this.indexTreeCheckData = this.indexTreeData[0].id
              this.defaultExpandedKeys[0] = this.indexTreeData[0].id //默认展开
              this.$refs.tree.setCheckedKeys([this.indexTreeData[0].id])
            } else {
              deptId = this.indexTreeData[0].id
              this.defaultExpandedKeys[0] = deptId
              this.defaultCheckedKeys[0] = deptId
            }

            this.getDeptDetail(deptId)
          } else {
          }
          this.indexTreeDataLeftLoading = false
        })
        .catch(() => {
          this.indexTreeDataLeftLoading = false
        })
    },
    // 左侧指标树选择
    indexHandleNodeClickLeft(item, node, self) {
      if (item.pId == '0') {
        this.isInstitution = true
      } else {
        this.isInstitution = false
      }
      this.indexTreeCheckData = item.id
      this.$refs.tree.setCheckedKeys([item.id])
      if (this.isCheck != this.indexTreeCheckData) {
        this.getDeptDetail(this.indexTreeCheckData)
      }
    },

    // 左侧指标树修改
    indexHandleNodeChangeLeft(item, node, self) {
      if (node == true) {
        this.indexTreeCheckData = item.id
        this.$refs.tree.setCheckedKeys([item.id])
      } else {
        if (this.indexTreeCheckData == item.id) {
          this.$refs.tree.setCheckedKeys([item.id])
        }
      }

      if (this.isCheck != this.indexTreeCheckData) {
        this.getDeptDetail(this.indexTreeCheckData)
      }
    },
    //获取菜单明细
    getDeptDetail(deptId) {
      if (!deptId) {
        return
      }
      pageApi
        .getDeptDetail(deptId)
        .then(response => {
          if (!response.data.error) {
            let data = response.data.data[0]
            this.deptDetailData = data
            this.formCount.deptCode = commonFun.abnormalityData(data.deptCode) //部门编码
            this.formCount.deptName = commonFun.abnormalityData(data.deptName) //部门名称
            this.formCount.deptDesc = commonFun.abnormalityData(data.deptDesc) //部门简介
            this.formCount.remark = commonFun.abnormalityData(data.remark) //备注
            if (data.deptId) {
              this.formCount.deptId = '' + data.deptId //部门id
            }
            this.formCount.companyId = commonFun.abnormalityData(data.companyId) // 机构id
            this.formCount.deptPid = commonFun.abnormalityData(data.deptPid) //父部门id
            this.formCount.deptPname = commonFun.abnormalityData(data.deptPname) //上级部门
            this.isEdit = true
            this.isEditAdd = true
            this.isCheck = deptId
            this.getUserList(deptId)
          } else {
            this.isCheck = 0
            this.isEdit = false
          }
        })
        .catch(() => {
          this.isCheck = 0
          this.isEdit = false
          this.deptDetailData = []
        })
    },
    //获取用户列表
    getUserList(deptId) {
      this.tableLoading = true
      if (!this.myDeptId && !deptId) {
        return
      }
      let params = commonFun.parameterSrc(this.formInline)
      params.myDept = deptId
      delete params.myDept
      if (this.formCount && this.formCount.deptPid == '0') {
        params.companyId = this.formCount.companyId
      } else {
        params.deptId = deptId
      }
      console.log(params)
      pageApi
        .getUserListNew(params)
        .then(response => {
          let { status, data } = response.data
          if (status == 200) {
            try {
              for (let i = 0; i < data.list.length; i++) {
                let temp = data.list[i]
                if (temp.deptNames) {
                  let strArray = temp.deptNames.split('/')
                  // 存在机构，但是不存在部门的情况
                  if (strArray.length > 0 && strArray.length < 2) {
                    temp.institution = strArray[1]
                    temp.department = ''
                  } else if (strArray.length >= 2) {
                    temp.institution = strArray[1]
                    temp.department = strArray[strArray.length - 1]
                  } else {
                    temp.institution = ''
                    temp.department = ''
                  }
                } else {
                  temp.institution = ''
                  temp.department = ''
                }
              }
            } catch (e) {
              console.log(e)
            }
            this.tableData = response.data.data.list
            // 页面总条数
            this.total = response.data.data.total
            this.myDeptId = deptId
          } else {
            this.tableData = []
            this.total = 0
            this.myDeptId = ''
          }
          this.tableLoading = false
        })
        .catch(() => {
          this.tableData = []
          this.total = 0
          this.tableLoading = false
          this.myDeptId = ''
        })
    },
    // table批量选择结果
    handleSelectionChange(val) {
      this.tableMultipleSelection = val
    },
    //列表点击排序
    handleSortChange(val) {
      this.formInline.orderStr = commonFun.orderByString(val)
      this.getUserList(this.myDeptId)
    },
    Pagination(val) {
      this.formInline.pageSize = val.limit //页面条数
      this.formInline.pageNum = val.page //页面
      this.getUserList(this.myDeptId)
    },
    editDataJd() {
      this.isAdd = false //是否新增
      this.isEdit = true
      this.isEditAdd = true
      let data = this.deptDetailData
      if (data && data.deptId) {
        this.formCount.deptCode = commonFun.abnormalityData(data.deptCode) //部门编码
        this.formCount.deptName = commonFun.abnormalityData(data.deptName) //部门名称
        this.formCount.deptDesc = commonFun.abnormalityData(data.deptDesc) //部门简介
        this.formCount.remark = commonFun.abnormalityData(data.remark) //备注
        if (data.deptId) {
          this.formCount.deptId = '' + data.deptId //部门id
        }
        this.formCount.companyId = commonFun.abnormalityData(data.companyId) // 机构id
        this.formCount.deptPid = commonFun.abnormalityData(data.deptPid) //父部门id
        this.formCount.deptPname = commonFun.abnormalityData(data.deptPname) //上级部门
      }
    },
    addDataJd() {
      this.isInstitution = false
      this.isAdd = true //是否新增
      this.isEdit = false
      this.isEditAdd = false
      // 清除
      this.$nextTick(() => {
        this.$refs['formCount'].resetFields()
        this.formCount.deptCode = '' //部门编码
        this.formCount.deptName = '' //部门名称
        this.formCount.deptDesc = '' //部门简介
        this.formCount.remark = '' //备注
        this.formCount.deptId = '' //部门id
        let data = this.deptDetailData
        if (data && data.deptId) {
          this.formCount.deptPid = '' + commonFun.abnormalityData(data.deptId) //父部门id
          this.formCount.deptPname = commonFun.abnormalityData(data.deptName) //上级部门
        }
      })
    },
    saveDataJd(formName) {
      var self = this
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.$message.closeAll()
          if (!this.isEdit) {
            // 添加
            this.saveData()
          } else {
            // 修改
            this.updateParamSet()
          }
        } else {
          return false
        }
      })
    },
    //保存
    saveData() {
      this.$confirm('确定新增?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          let params = {}
          params = commonFun.parameterSrc(this.formCount)
          //this.submit_btn_load = true;
          pageApi
            .addDept(params)
            .then(response => {
              if (!response.data.error) {
                // 关闭移动指标弹框
                this.$message.closeAll()
                this.$message({
                  message: '新增成功',
                  type: 'success'
                })

                // 刷新列表
                //this.reload();
                this.addDataJd()
                //this.addFormId = params.deptId;
                this.getDepts()
              } else {
                // 关闭移动指标弹框
                this.$message.closeAll()
                this.$message({
                  message: response.data.error || '新增失败',
                  type: 'warning'
                })
              }
              this.submit_btn_load = false
            })
            .catch(() => {
              // 关闭移动指标弹框
              this.submit_btn_load = false
              this.$message.closeAll()
              this.$message({
                message: '新增失败',
                type: 'warning'
              })
            })
        })
        .catch(() => {
          this.submit_btn_load = false
        })
    },
    //修改
    updateParamSet() {
      this.$confirm('确定修改?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          let params = {}
          params = commonFun.parameterSrc(this.formCount)
          this.submit_btn_load = true
          pageApi
            .updateDept(params)
            .then(response => {
              if (!response.data.error) {
                // 关闭移动指标弹框
                this.$message.closeAll()
                this.$message({
                  message: '修改成功',
                  type: 'success'
                })
                this.getDepts()
              } else {
                // 关闭移动指标弹框
                this.$message.closeAll()
                this.$message({
                  message: response.data.error || '修改失败',
                  type: 'warning'
                })
              }
              this.submit_btn_load = false
            })
            .catch(() => {
              // 关闭移动指标弹框
              this.submit_btn_load = false
              this.$message.closeAll()
              this.$message({
                message: '修改失败',
                type: 'warning'
              })
            })
        })
        .catch(() => {
          this.submit_btn_load = false
        })
    },
    //删除
    deleteDataJd() {
      this.$confirm('确定删除?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          let id = this.formCount.deptId
          if (!id) {
            return
          }
          pageApi
            .deleteDept(id)
            .then(response => {
              if (!response.data.error) {
                // 关闭移动指标弹框
                this.$message.closeAll()
                this.$message({
                  message: '删除成功',
                  type: 'success'
                })
                this.addDataJd()
                this.formCount.companyId = '' // 机构id
                this.formCount.deptPid = '' //父部门id
                this.formCount.deptPname = '' //上级部门
                this.getDepts()
              } else {
                // 关闭移动指标弹框
                this.$message.closeAll()
                this.$message({
                  message: response.data.error || '删除失败',
                  type: 'warning'
                })
              }
            })
            .catch(() => {
              // 关闭移动指标弹框
              this.$message.closeAll()
              this.$message({
                message: '删除失败',
                type: 'warning'
              })
            })
        })
        .catch(() => {})
    },
    editData(row) {
      this.positionUserName = row.userName
      this.positiondeptName = row.deptNames
      this.positiondeptUserId = row.userId
      this.countDialog = true

      this.getPositionByUser(row.userId)
      this.getPosition(row.userId, false)
    },
    handleAddSelectionChange(val) {
      this.addTableMultipleSelection = val
    },
    handleAddSortChange(val) {
      this.formAddInline.orderStr = commonFun.orderByString(val)
      this.getPosition(this.positiondeptUserId, false)
    },
    PaginationAdd(val) {
      this.formAddInline.pageSize = val.limit //页面条数
      this.formAddInline.pageNum = val.page //页面
      this.getPosition(this.positiondeptUserId, false)
    },
    editDepData(row) {
      // let arr = this.addTableMultipleSelection;
      // for(let i=0;i<arr.length;i++){
      //   if(arr[i].positionCode === row.positionCode){

      //         return;
      //     }
      // }
      // this.$message({
      //   message: '请先勾选',
      //   type: 'warning'
      // });

      this.innerVisible = true
      this.positionCodeAdd = row.positionCode
      let deptName = row.manageDeptNames
      if (deptName) {
        let deptNames = deptName.split(',')
        this.getDeptsAdd(deptNames)
      } else {
        let arr = []
        this.getDeptsAdd(arr)
      }
    },
    //获取岗位类型
    getPositionType() {
      pageApi
        .getPositionType()
        .then(response => {
          if (!response.data.error) {
            this.positionTypeArr = response.data.data
            let arr = response.data.data
            for (let i = 0; i < arr.length; i++) {
              this.positionTypeArrs[arr[i].type] = arr[i].name
            }
          } else {
            this.$message({
              message: '初始化岗位类型失败',
              type: 'warning'
            })
          }
        })
        .catch(() => {
          this.$message({
            message: '初始化岗位类型失败',
            type: 'warning'
          })
        })
    },
    //根据userID获取岗位信息
    getPositionByUser(userId) {
      pageApi
        .getPositionByUser(userId)
        .then(response => {
          if (!response.data.error) {
            let arr = response.data.data
            let position = []
            let positionCodes = []
            for (let i = 0; i < arr.length; i++) {
              position.push(arr[i].positionName)
              positionCodes.push(arr[i].positionCode)
            }
            this.positionList = position.toString()
            this.positionCodes = positionCodes
          } else {
            this.$message({
              message: '初始化岗位信息失败',
              type: 'warning'
            })
            this.positionList = ''
            this.positionCodes = []
          }
        })
        .catch(() => {
          this.$message({
            message: '初始化岗位信息失败',
            type: 'warning'
          })
          this.positionList = ''
          this.positionCodes = []
        })
    },
    //选中数据
    toggleSelection(rows) {
      if (rows) {
        this.$nextTick(() => {
          rows.forEach(row => {
            this.$refs.multipleAddTable.toggleRowSelection(row, true)
          })
        })
      } else {
        this.$refs.multipleAddTable.clearSelection()
      }
    },
    getPosition(userId, flag) {
      this.addTableLoading = true
      if (!userId) {
        this.$message({
          message: '用户id为空',
          type: 'warning'
        })
        return
      }
      if (flag) {
        this.formAddInline.pageNum = 1
      }
      let params = commonFun.parameterSrc(this.formAddInline)
      params.userId = userId
      pageApi
        .getPosition(params)
        .then(response => {
          if (!response.data.error) {
            this.addTableData = response.data.data.list
            let arr = this.addTableData
            let position = this.positionCodes
            let arr2 = []
            for (let j = 0; j < position.length; j++) {
              for (let i = 0; i < arr.length; i++) {
                if (arr[i].positionCode === position[j]) {
                  arr2.push(arr[i])
                  break
                }
              }
            }

            this.addTableMultipleSelection = arr2
            this.toggleSelection(arr2)
            // 页面总条数
            this.addTotal = response.data.data.total
          } else {
            this.addTableData = []
            this.addTotal = 0
          }
          this.addTableLoading = false
        })
        .catch(() => {
          this.addTableData = []
          this.addTotal = 0
          this.addTableLoading = false
        })
    },
    onAddSubmit() {
      this.getPosition(this.positiondeptUserId, true)
    },
    addRestForm() {
      this.formAddInline.positionCode = '' //岗位编码
      this.formAddInline.positionName = '' //岗位名称
      this.formAddInline.positionType = '' //岗位类型
    },
    addPosition() {
      let params = {}
      params.userId = this.positiondeptUserId
      let rows = this.addTableMultipleSelection
      let codes = []
      rows.forEach(function(item, index) {
        codes.push(item.positionCode)
      })
      params.positionCodes = codes.toString()
      pageApi
        .positionInsert(params)
        .then(response => {
          if (!response.data.error) {
            this.$message({
              message: '保存成功',
              type: 'success'
            })
            this.countDialog = false
            this.getUserList(this.myDeptId)
          } else {
            this.$message({
              message: '保存失败',
              type: 'warning'
            })
          }
        })
        .catch(() => {
          this.$message({
            message: '保存失败',
            type: 'warning'
          })
        })
    },
    //数据字典转换
    dataStatus(statusCode) {
      return this.positionTypeArrs[statusCode]
    },
    //选择部门
    indexHandleNodeChangeAdd(item, node, self) {
      let id = item.id
      let nodeChangeIds = this.nodeChangeIdArr
      if (node) {
        nodeChangeIds.push(id)
        this.nodeChangeIdArr = nodeChangeIds
      } else {
        let arr = []
        nodeChangeIds.forEach(nodeChangeId => {
          if (nodeChangeId != id) {
            arr.push(nodeChangeId)
          }
        })
        this.nodeChangeIdArr = arr
      }
    },
    //岗位维护-部门维护保存
    addPositionDept() {
      let params = {}
      params.positionCode = this.positionCodeAdd
      params.userId = this.positiondeptUserId
      params.manageDepts = this.nodeChangeIdArr.toString()
      pageApi
        .positionDept(params)
        .then(response => {
          if (!response.data.error) {
            this.$message({
              message: '保存成功',
              type: 'success'
            })
            this.innerVisible = false
            this.getPosition(this.positiondeptUserId, true)
            this.nodeChangeIdArr = []
          } else {
            this.$message({
              message: '保存失败',
              type: 'warning'
            })
          }
        })
        .catch(() => {
          this.$message({
            message: '保存失败',
            type: 'warning'
          })
        })
    },
    //获取菜单tree
    getDeptsAdd(deptNames) {
      // 打开遮罩层
      this.indexTreeDataAddLoading = true

      pageApi
        .getDataSourceList()
        .then(response => {
          if (!response.data.error) {
            // 指标树数据
            this.indexTreeDataAdd = commonFun.TreeDataPId(response.data.data, '0').data

            // 默认选中指标树
            this.indexTreeSelectAdd = this.indexTreeDataAdd[0]
            let arr = response.data.data

            var deptIds = []
            for (let i = 0; i < deptNames.length; i++) {
              for (let j = 0; j < arr.length; j++) {
                if (arr[j].deptName === deptNames[i]) {
                  deptIds.push(arr[j].id)
                  break
                }
              }
            }
            this.nodeChangeIdArr = deptIds
            this.defaultExpandedKeysAdd = deptIds
            this.defaultCheckedKeysAdd = deptIds
          } else {
            this.nodeChangeIdArr = []
          }
          this.indexTreeDataAddLoading = false
        })
        .catch(() => {
          this.indexTreeDataAddLoading = false
          this.nodeChangeIdArr = []
        })
    }
  }
}
</script>

<style lang="scss" scoped>
::v-deep .el-button.el-button--info {
  background-color: #fff;
  color: #612d10;
}
.customDeptWidth {
  width: 80% !important;
}

.el-dialog .el-deptForm {
  width: 100% !important;
}

.formDeptWidth {
  width: 270px !important;
}

.title-style {
  color: #0F65DD;
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
  background-color: #0F65DD;
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

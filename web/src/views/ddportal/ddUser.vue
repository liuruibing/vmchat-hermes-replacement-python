<template>
  <div class="DdPosition ddportal-ui">
    <el-form :inline="true" ref="formInline" :model="formInline" style="margin-bottom: 8px;" class="demo-form-inline form_inline_search standard-form">
      <el-row>
        <el-col :span="14">
          <div style="width:100%;">
            <el-form-item label="姓名" prop="userName">
              <el-input v-model="formInline.userName" size="small" placeholder="请输入内容"></el-input>
            </el-form-item>
            <el-form-item label="创建日期" prop="date">
              <el-date-picker
                v-model="formInline.date"
                size="small"
                value-format="yyyy-MM-dd"
                type="daterange"
                :picker-options="dateShortcut()"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
              ></el-date-picker>
            </el-form-item>
            <el-form-item label="部门" prop="deptIds">
              <el-input v-model="formInline.deptIds" @focus="selectDeptIds(1)" size="small"></el-input>
              <i class="el-icon-delete" style="color:#e2b997" @click="deleteDeptIds()"></i>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="10">
          <el-form-item class="search_button_com">
            <el-button type="primary" @click="onSubmit('formInline', true)" style="margin-bottom: 5px; " size="small">
              <i class="el-icon-search"></i>
              查询
            </el-button>
            <el-button type="info" plain @click="restForm()" style="margin-bottom: 5px; " size="small">
              <i class="el-icon-delete"></i>
              重置
            </el-button>
            <el-button type="primary" plain @click="addData()" style="margin-bottom: 5px; " size="small">
              <i class="el-icon-circle-plus-outline"></i>
              添加
            </el-button>
            <el-button type="primary" plain :loading="pwdStrategyLoading" @click="pwdStrategy()" style="margin-bottom: 5px;" size="small">
              <i class="el-icon-setting"></i>
              密码策略设置
            </el-button>
            <el-button type="primary" plain @click="searchLockUser()" style="margin-bottom: 5px;" size="small">
              <i class="el-icon-setting"></i>
              锁定用户管理
            </el-button>

            <!-- <el-button type="primary" @click="download()"  style="margin-bottom: 5px; " size="small">
              <i class="el-icon-download"></i>导出
            </el-button>-->
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <div style="vertical-align: middle;display: inline-block">
      <div class="color-box"></div>
    </div>
    <span class="title-style">用户列表</span>
    <el-table
      ref="multipleTable"
      @selection-change="handleSelectionChange"
      :data="tableData"
      :default-sort="{ prop: 'userName', order: 'descending' }"
      border
      stripe
      id="standard-table"
      @sort-change="handleSortChange"
      v-loading="tableLoading"
      style="width: 100%"
    >
      <el-table-column prop="userName" show-overflow-tooltip label="姓名" min-width="100" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.userName | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="userNo" show-overflow-tooltip label="员工编号" min-width="80" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.userNo | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="account" show-overflow-tooltip label="登录账户" min-width="80" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.account | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="companyName" show-overflow-tooltip label="机构" min-width="70" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.companyName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column prop="deptNames" show-overflow-tooltip label="部门" min-width="70" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.deptNames | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column prop="roleNames" show-overflow-tooltip label="角色" min-width="70" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.roleNames | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column prop="status" show-overflow-tooltip label="状态" min-width="70" algin="left" header-align="center">
        <template slot-scope="scope">
          <span v-if="dataZlStatus(scope.row.status) === '禁用'" style="color:red">{{ dataZlStatus(scope.row.status) | noDataFilter }}</span>
          <span v-else>{{ dataZlStatus(scope.row.status) | noDataFilter }}</span>
        </template>
      </el-table-column>

      <!-- <el-table-column
        prop="accountStatusName"
        show-overflow-tooltip
        label="账号状态"
        min-width="70"
        algin="left"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.accountStatusName | noDataFilter }}</span>
        </template>
      </el-table-column>-->

      <el-table-column prop="telePhone" show-overflow-tooltip label="座机" min-width="70" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.telePhone | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column prop="email" show-overflow-tooltip label="邮箱" min-width="70" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.email | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column prop="createDate" show-overflow-tooltip label="创建日期" min-width="70" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.createDate | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column label="操作" min-width="160" align="center">
        <template slot-scope="scope">
          <div class="dialog-footer standard-form">
            <el-button type="info" size="small" plain @click="editData(scope.row)">编辑</el-button>
            <el-button type="info" v-show="dataZlStatus(scope.row.status) === '禁用'" plain size="small" @click="updateEnableStatus(scope.row)">启用</el-button>
            <el-button type="info" v-show="dataZlStatus(scope.row.status) === '启用'" plain size="small" @click="updateDisableStatus(scope.row)">禁用</el-button>
            <el-button type="info" plain size="small" @click="updatePassword(scope.row)">密码重置</el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>

    <Pagination :total="total" :page="formInline.pageNum" :limit="formInline.pageSize" @pagination="Pagination"></Pagination>

    <!-- 新增用户 -->
    <el-dialog :title="countTitle" customClass="customUserWidth" v-dialogDrag center :visible.sync="countDialog" :close-on-click-modal="false">
      <el-container>
        <el-main class="mainBox">
          <el-form :inline="true" ref="formCount" :model="formCount" :rules="countRules" label-position="right">
            <el-form-item label="登录账户" prop="account" class="mb20" :label-width="formLabelWidth">
              <el-input :disabled="isEdit" type="text" v-model.trim="formCount.account" clearable placeholder="请输入" size="small"></el-input>
              <span v-show="!isEdit">登录系统所需账户，唯一(建议使用机构简称开头)</span>
            </el-form-item>
            <br v-show="!isEdit" />

            <el-form-item
              label="登录密码"
              :rules="this.isEdit == false ? countRules.password : [{ required: false, message: '请填写', trigger: 'blur' }]"
              prop="password"
              class="mb20"
              :label-width="formLabelWidth"
            >
              <el-input :disabled="isEdit" type="text" show-password v-model.trim="formCount.password" placeholder="请输入" size="small"></el-input>
            </el-form-item>

            <el-form-item v-show="!isEdit" label="确认密码" prop="passwordAgain" class="mb20" :label-width="formLabelWidth">
              <el-input type="text" show-password v-model.trim="formCount.passwordAgain" placeholder="请输入" size="small"></el-input>
            </el-form-item>

            <el-form-item :style="{ 'margin-top': isEdit ? '0px' : '15px' }" label="所属机构" prop="companyId" class="mb20" :label-width="formLabelWidth">
              <el-select :disabled="isEdit" v-model="formCount.companyId" size="small" placeholder="请选择" filterable @change="handleCompanyIdChange">
                <el-option v-for="(group, index) in companyIdArr" :value="group.deptId" :key="index" :label="group.deptName"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item v-show="isEdit" label="员工编号" prop="userNo" class="mb20" :label-width="formLabelWidth">
              <el-input :disabled="isEdit" type="text" v-model.trim="formCount.userNo" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>
            <el-form-item :style="{ 'margin-top': isEdit ? '0px' : '15px' }" label="角色" prop="roleIds" class="mb20" :label-width="formLabelWidth">
              <el-select v-model="formCount.roleIds" multiple size="small" placeholder="请选择">
                <el-option v-for="(group, index) in roleIdsdArr" :value="group.roleId" :key="index" :label="group.roleName"></el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="部门" prop="deptIds " class="mb20" :label-width="formLabelWidth">
              <el-input v-model="formCount.deptIds" @focus="selectDeptIdsByAdd(2)" size="small"></el-input>
              <i class="el-icon-delete" style="color:#e1b997" @click="deleteDeptIdsAdd()"></i>
            </el-form-item>

            <el-form-item v-show="!isEdit" label="员工编号" prop="userNo" class="mb20" :label-width="formLabelWidth">
              <el-input type="text" v-model.trim="formCount.userNo" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>

            <el-form-item label="姓名" prop="userName" class="mb20" :label-width="formLabelWidth">
              <el-input type="text" v-model.trim="formCount.userName" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>

            <el-form-item label="昵称" prop="nickName" class="mb20" :label-width="formLabelWidth">
              <el-input type="text" v-model.trim="formCount.nickName" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>

            <el-form-item label="性别" prop="sex" class="mb20" :label-width="formLabelWidth">
              <el-select v-model="formCount.sex" size="small" placeholder="请选择">
                <el-option v-for="(group, index) in sexArr" :value="group.dimCde" :key="index" :label="group.dimNme"></el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="年龄" prop="age" class="mb20" :label-width="formLabelWidth">
              <el-input type="text" v-model.trim="formCount.age" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>

            <el-form-item label="手机" prop="cellPhone" class="mb20" :label-width="formLabelWidth">
              <el-input type="text" v-model.trim="formCount.cellPhone" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>

            <el-form-item label="座机" prop="telePhone" class="mb20" :label-width="formLabelWidth">
              <el-input type="text" v-model.trim="formCount.telePhone" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>

            <el-form-item label="邮箱" prop="email" class="mb20" :label-width="formLabelWidth">
              <el-input type="text" v-model.trim="formCount.email" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>

            <el-form-item label="传真" prop="fax" class="mb20" :label-width="formLabelWidth">
              <el-input type="text" v-model.trim="formCount.fax" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>

            <el-form-item label="状态" prop="status" class="mb20" :label-width="formLabelWidth">
              <el-select v-model="formCount.status" size="small" placeholder="请选择">
                <el-option v-for="(group, index) in statusArr" :value="group.dimCde" :key="index" :label="group.dimNme"></el-option>
              </el-select>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" size="small" :loading="countSubmit_btn" @click="countSubmit('formCount')">提 交</el-button>
        <el-button size="small" type="info" plain @click="countDialog = false">取 消</el-button>
      </div>
    </el-dialog>

    <!-- 选择部门 -->
    <el-dialog title="选择部门" v-dialogDrag center :visible.sync="deptDialog" :close-on-click-modal="false">
      <el-container style="height:441px;">
        <el-main class="mainBox">
          <el-input size="small" placeholder="输入关键字进行过滤" v-model="filterText"></el-input>
          <el-tree
            :data="deptData"
            :props="defaultProps"
            node-key="id"
            :expand-on-click-node="false"
            accordion
            default-expand-all
            class="standard-tree"
            :default-checked-keys="defaultCheckedKeys"
            ref="tree"
            :filter-node-method="filterNode"
            show-checkbox
          ></el-tree>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" size="small" :loading="deptSubmit_btn" @click="deptSubmit()">提 交</el-button>
        <el-button size="small" type="info" plain @click="deptDialog = false">取 消</el-button>
      </div>
    </el-dialog>

    <!-- 选择部门 -->
    <!-- 密码重置 -->
    <el-dialog title="密码重置" customClass="customUserWidth" v-dialogDrag center :visible.sync="passwordDialog" :close-on-click-modal="false">
      <el-container>
        <el-main class="mainBox">
          <el-form :inline="true" ref="formPassword" :model="formPassword" :rules="countRules2" label-position="right">
            <el-form-item label="重置密码" prop="newPassword" class="mb20" :label-width="formLabelWidth">
              <el-input type="text" show-password v-model.trim="formPassword.newPassword" placeholder="请输入" size="small"></el-input>
              <span v-show="!isEdit">登录系统所需账户，唯一(建议使用机构简称开头)</span>
            </el-form-item>
            <br />
            <el-form-item label="确认密码" prop="newPassword2" class="mb20" :label-width="formLabelWidth">
              <el-input type="text" show-password v-model.trim="formPassword.newPassword2" placeholder="请输入" size="small"></el-input>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" size="small" :loading="countSubmit_btn" @click="passwordSubmit('formPassword')">提 交</el-button>
        <el-button size="small" type="info" plain @click="passwordDialog = false">取 消</el-button>
      </div>
    </el-dialog>
    <!-- 密码策略设置 -->
    <el-dialog title="密码策略设置" v-dialogDrag center :visible.sync="pwdStrategyDialog" :close-on-click-modal="false">
      <el-container>
        <el-main class="mainBox">
          <el-form :inline="true" class="standard-form" ref="formPwdStrategy" :model="formPwdStrategy" :rules="pwdStrategyRules" label-position="right">
            <el-form-item label="密码长度" prop="minPwdLength" :label-width="formLabelWidthStr" class="mb20">
              <el-input type="text" v-model.trim="formPwdStrategy.minPwdLength" clearable placeholder="请输入最小长度" size="small"></el-input>
            </el-form-item>
            <el-form-item prop="maxPwdLength" class="mb20">
              <el-input style="margin-left:15px" type="text" v-model.trim="formPwdStrategy.maxPwdLength" clearable placeholder="请输入最大长度" size="small"></el-input>
              <span style="margin-left:5px">示例: 8-18</span>
            </el-form-item>
            <el-form-item label="密码复杂度" prop="pwdComplexity" class="mb20" :label-width="formLabelWidthStr">
              <el-checkbox-group v-model="formPwdStrategy.pwdComplexity">
                <el-checkbox label="1">数字</el-checkbox>
                <el-checkbox label="2">字母</el-checkbox>
                <el-checkbox label="3">特殊字符</el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            <!-- <el-form-item
              label="是否开启自动解锁"
              prop="pwdAutoUnLock"
              class="mb20"
              :label-width="formLabelWidthStr"
            >
              <el-checkbox v-model="formPwdStrategy.pwdAutoUnLock"></el-checkbox>
            </el-form-item>
            <el-form-item
              label="是否开启登录失败账户锁定"
              prop="pwdLockEnable"
              class="mb20"
              :label-width="formLabelWidthStr"
            >
              <el-checkbox
                  @change = "pwdLockEnableChange"
                  v-model="formPwdStrategy.pwdLockEnable">
              </el-checkbox>
            </el-form-item>
            <el-form-item
              label="锁定时间(分钟)"
              prop="pwdLockTime"
              class="mb20"
              :label-width="formLabelWidthStr"
            >
              <el-input
                type="text"
                v-model.trim="formPwdStrategy.pwdLockTime"
                placeholder="请输入"
                clearable
                size="small"
              ></el-input>
            </el-form-item>
            <el-form-item
              label="密码输入错误多少次后锁定"
              prop="pwdErrCount"
              class="mb20"
              :label-width="formLabelWidthStr"
            >
              <el-input
                type="text"
                v-model.trim="formPwdStrategy.pwdErrCount"
                placeholder="请输入"
                clearable
                size="small"
              ></el-input>
            </el-form-item>
            <el-form-item
              label="登录的连续时间(分钟)"
              prop="pwdContinuityTime"
              class="mb20"
              :label-width="formLabelWidthStr"
            >
              <el-input
                type="text"
                v-model.trim="formPwdStrategy.pwdContinuityTime"
                placeholder="请输入"
                clearable
                size="small"
              ></el-input>
            </el-form-item>
            <el-form-item
              label="是否开启密码过期"
              prop="pwdExpiredEnable"
              class="mb20"
              :label-width="formLabelWidthStr"
            >
              <el-checkbox
                 @change = "pwdExpiredEnableChange"
                 v-model="formPwdStrategy.pwdExpiredEnable">
              </el-checkbox>
            </el-form-item>
            <el-form-item
              label="密码过期时间(天)"
              prop="pwdExpiredTime"
              class="mb20"
              :label-width="formLabelWidthStr"
            >
              <el-input
                type="text"
                v-model.trim="formPwdStrategy.pwdExpiredTime"
                placeholder="请输入"
                clearable
                size="small"
              ></el-input>
            </el-form-item> -->
          </el-form>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" size="small" :loading="pwdStrategyBtnLoading" @click="pwdStrategySubmit('formPwdStrategy')">提 交</el-button>
        <el-button size="small" type="info" @click="pwdStrategyDialog = false">取 消</el-button>
      </div>
    </el-dialog>
    <!-- 锁定用户管理 -->
    <el-dialog title="锁定用户管理" v-dialogDrag center :visible.sync="lockUserDialog" :close-on-click-modal="false">
      <el-container>
        <el-main class="mainBox">
          <el-form :inline="true" ref="lockUserForm" :model="lockUserForm" :rules="lockUserRules" style="margin-bottom: 8px;" class="demo-form-inline form_inline_search">
            <el-row>
              <el-col :span="18">
                <div style="width:100%;">
                  <el-form-item label="账号" prop="loginAccount">
                    <el-input v-model="lockUserForm.loginAccount" size="small" clearable placeholder="请输入内容"></el-input>
                  </el-form-item>
                  <el-form-item label="姓名" prop="userName">
                    <el-input v-model="lockUserForm.userName" size="small" clearable placeholder="请输入内容"></el-input>
                  </el-form-item>
                </div>
              </el-col>
              <el-col :span="6">
                <el-form-item class="search_button_com">
                  <el-button type="primary" @click="lockUserSubmit('lockUserForm', true)" style="margin-bottom: 5px;" size="small">
                    <i class="el-icon-search"></i>
                    查询
                  </el-button>
                  <el-button type="primary" plain @click="lockUserRestForm()" style="margin-bottom: 5px;" size="small">
                    <i class="el-icon-delete"></i>
                    重置
                  </el-button>
                  <!--                  <el-button-->
                  <!--                    type="primary"-->
                  <!--                    plain-->
                  <!--                    @click="unlockUserBatch()"-->
                  <!--                    style="margin-bottom: 5px;"-->
                  <!--                    size="small"-->
                  <!--                  >-->
                  <!--                    <i class="el-icon-unlock"></i>批量解锁-->
                  <!--                  </el-button>-->
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
          <el-table
            ref="multipleTable"
            @selection-change="lockUserHandleSelChange"
            :data="lockUserTableData"
            border
            stripe
            max-height="500"
            v-loading="lockUserTableLoading"
            style="width: 100%"
          >
            <el-table-column type="selection" width="35"></el-table-column>
            <!--            <el-table-column-->
            <!--              prop="userId"-->
            <!--              show-overflow-tooltip-->
            <!--              label="用户ID"-->
            <!--              min-width="100"-->
            <!--              algin="left"-->
            <!--              header-align="center"-->
            <!--            >-->
            <!--              <template slot-scope="scope">-->
            <!--                <span>{{ scope.row.userId | noDataFilter }}</span>-->
            <!--              </template>-->
            <!--            </el-table-column>-->
            <el-table-column prop="userAccount" show-overflow-tooltip label="账户" min-width="100" algin="left" header-align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.userAccount | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="userName" show-overflow-tooltip label="姓名" min-width="100" algin="left" header-align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.userName | noDataFilter }}</span>
              </template>
            </el-table-column>
            <!--            <el-table-column-->
            <!--              prop="loginIp"-->
            <!--              show-overflow-tooltip-->
            <!--              label="锁定IP"-->
            <!--              min-width="100"-->
            <!--              algin="left"-->
            <!--              header-align="center"-->
            <!--            >-->
            <!--              <template slot-scope="scope">-->
            <!--                <span>{{ scope.row.loginIp | noDataFilter }}</span>-->
            <!--              </template>-->
            <!--            </el-table-column>-->
            <el-table-column prop="recordTime" show-overflow-tooltip label="锁定时间" min-width="100" algin="left" header-align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.recordTime | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" min-width="80" align="center" header-align="center">
              <template slot-scope="scope">
                <el-button type="primary" plain @click="unlockUserRows(scope.row)" size="small">
                  <i class="el-icon-unlock"></i>
                  解锁
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          <Pagination :total="lockUserTotal" :page="lockUserForm.pageNum" :limit="lockUserForm.pageSize" @pagination="lockUserPagination"></Pagination>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" type="info" plain @click="lockUserDialog = false">关 闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import store from '@/store'
import commonFun from '@/filters/common'
import Pagination from '@/components/Pagination'
import pageApi from './api/userTactics.js'
import { Base64 } from 'js-base64'
import cryptoJs from 'crypto-js'

export default {
  name: 'DdUserTactics',
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
    const validateNewpassword = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入新密码'))
      } else {
        let params = {
          password: value
        }
        pageApi
          .checkPassword(params)
          .then(response => {
            if (response.data.status === 200) {
              callback()
            } else {
              callback(response.data.message)
            }
          })
          .catch(() => {
            callback('校验新密码失败')
          })
      }
    }
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.formCount.password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    const validateResetPassword = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入新密码'))
      } else {
        let params = {
          password: value
        }
        pageApi
          .checkPassword(params)
          .then(response => {
            if (response.data.status === 200) {
              callback()
            } else {
              callback(response.data.message)
            }
          })
          .catch(() => {
            callback('校验新密码失败')
          })
      }
    }
    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.formPassword.newPassword) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    // 密码安全策略正则
    // 锁定时间
    const validatePwdLockTime = (rule, value, callback) => {
      if (!value && this.formPwdStrategy.pwdLockEnable === true) {
        callback(new Error('请输入'))
      } else if (value && !/^[0-9]*[1-9][0-9]*$/.test(value)) {
        callback(new Error('请输入正整数'))
      } else {
        callback()
      }
    }
    // 密码输入错误的次数
    const validatePwdErrCount = (rule, value, callback) => {
      if (!value && this.formPwdStrategy.pwdLockEnable === true) {
        callback(new Error('请输入'))
      } else if (value && !/^[0-9]*[1-9][0-9]*$/.test(value)) {
        callback(new Error('请输入正整数'))
      } else {
        callback()
      }
    }
    // 登录的连续时间
    const validatePwdContinuityTime = (rule, value, callback) => {
      if (!value && this.formPwdStrategy.pwdLockEnable === true) {
        callback(new Error('请输入'))
      } else if (value && !/^[0-9]*[1-9][0-9]*$/.test(value)) {
        callback(new Error('请输入正整数'))
      } else {
        callback()
      }
    }
    // 密码过期时间
    const validatePwdExpiredTime = (rule, value, callback) => {
      if (!value && this.formPwdStrategy.pwdExpiredEnable === true) {
        callback(new Error('请输入'))
      } else if (value && !/^[0-9]*[1-9][0-9]*$/.test(value)) {
        callback(new Error('请输入正整数'))
      } else {
        callback()
      }
    }
    const validateMinPwd = (rule, value, callback) => {
      let regu = /^[0-9]*[1-9][0-9]*$/
      if (value === '') {
        callback(new Error('请输入最小长度'))
      } else if (value < 6) {
        callback(new Error('请输入6-99的整数'))
      } else if (value > 99) {
        callback(new Error('请输入6-99的整数'))
      } else if (!regu.test(value)) {
        callback(new Error('请输入6-99的整数'))
      } else {
        callback()
      }
    }

    const validateMaxPwd = (rule, value, callback) => {
      let regu = /^[0-9]*[1-9][0-9]*$/
      if (value === '') {
        callback(new Error('请输入最大长度'))
      } else if (value < 6) {
        callback(new Error('请输入6-99的整数'))
      } else if (value > 99) {
        callback(new Error('请输入6-99的整数'))
      } else if (!regu.test(value)) {
        callback(new Error('请输入6-99的整数'))
      } else {
        callback()
      }
    }
    return {
      filterText: '',
      formInline: {
        userName: '', //用户名
        date: [], //日期
        deptIds: '', //部门
        orderStr: 'userName desc nulls last', //列表排序
        pageSize: 10, //条数
        pageNum: 1 //页码
      },
      total: 0, //列表条数
      tableData: [], //列表数据
      tableMultipleSelection: [], //表格选择数据集合
      tableLoading: false, //列表加载
      formLabelWidth: '120px',
      countDialog: false, // 弹窗
      countTitle: '', //标题
      countFormList: '', //是新增还是编辑
      // 操作类型 1、添加 2、编辑
      operationType: 1,
      // 新增 编辑计算任务
      formCount: {
        account: '', //账户
        password: '', //密码
        passwordAgain: '', //确认密码
        companyId: '', //所属机构
        roleIds: [], //角色
        deptIds: '', //部门
        userNo: '', //编号
        userName: '', //姓名
        nickName: '', //昵称
        sex: '', //性别
        age: '', //年龄
        cellPhone: '', //手机
        telePhone: '', //座机
        email: '', //邮箱
        fax: '', //传真
        status: '' //状态
      },
      countSubmit_btn: false, //保存按钮加载
      deptSubmit_btn: false, //部门保存加载
      isEdit: false, //是否编辑
      deptDialog: false, //选择部门弹框控制
      companyIdArr: [], //机构数组
      roleIdsdArr: [], //角色数组
      sexArr: [], //性别数组
      statusArr: [], //状态数组
      //tree参数
      // 操作类型 1、查询条件选择部门 2、新增，编辑选择部门
      operationDeptType: 1,
      deptData: [], //tree数据
      deptDataChecked: [], //默认选中
      defaultProps: {
        children: 'children',
        label: 'label'
      },
      // 弹窗验证规则
      countRules: {
        account: [
          {
            required: true,
            type: 'string',
            message: '请输入账户信息',
            trigger: 'blur'
          }
        ],
        userNo: [
          {
            required: true,
            type: 'string',
            message: '请输入员工编号',
            trigger: 'blur'
          }
        ],
        userName: [
          {
            required: true,
            type: 'string',
            message: '请输入姓名',
            trigger: 'blur'
          }
        ],
        companyId: [{ required: true, message: '请选择所属机构', trigger: 'change' }],
        password: [
          {
            required: true,
            trigger: 'change',
            validator: validateNewpassword
          }
        ],
        passwordAgain: [
          {
            required: true,
            trigger: ['blur', 'change'],
            validator: validatePass
          }
        ],
        age: [
          {
            pattern: /^(1[89]|[2-9]\d|100)$/,
            trigger: ['blur', 'change'],
            message: '年龄需在18-100岁之间'
          }
        ],
        cellPhone: [
          {
            pattern: /^1(3\d|4[5-9]|5[0-35-9]|6[2567]|7[0-8]|8\d|9[0-35-9])\d{8}$/,
            trigger: ['blur', 'change'],
            message: '请输入正确的手机号'
          }
        ],
        telePhone: [
          {
            pattern: /^(([0\+]\d{2,3}-)?(0\d{2,3})-)(\d{7,8})(-(\d{3,}))?$/,
            trigger: ['blur', 'change'],
            message: '请输入正确的座机号'
          }
        ],
        email: [
          {
            type: 'email',
            message: '请输入正确的邮箱地址',
            trigger: ['blur', 'change']
          }
        ],
        fax: [
          {
            pattern: /^((\d{11})|^((\d{7,8})|(\d{4}|\d{3})-(\d{7,8})|(\d{4}|\d{3})-(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1})|(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1}))$)/,
            trigger: ['blur', 'change'],
            message: '请输入正确的传真号'
          }
        ]
      },
      defaultCheckedKeys: [], //默认选中tree
      userStatus: {}, //用户状态map
      deptChangeNames: [], //选中的id
      deptChangeNamesAdd: [], //详情部门选择
      deptChangeNamesEdit: [], //编辑部门选择
      passwordDialog: false, //重置密码弹框
      formPassword: {
        newPassword: '',
        newPassword2: '',
        userId: ''
      },
      // 弹窗验证规则
      countRules2: {
        newPassword: [
          {
            required: true,
            trigger: 'change',
            validator: validateResetPassword
          }
        ],
        newPassword2: [
          {
            required: true,
            trigger: ['blur', 'change'],
            validator: validatePass2
          }
        ]
      },

      // 密码策略弹框
      pwdStrategyLoading: false, // 密码策略设置按钮loading
      pwdStrategyDialog: false, // 是否显示
      formPwdStrategy: {
        pwdLength: '', // 密码长度
        pwdComplexity: [], // 密码复杂度
        pwdAutoUnLock: false, // 是否开始自动解锁
        pwdLockEnable: false, // 是否开启登录失败账户锁定
        pwdLockTime: '', // 锁定时间 (分钟)
        pwdErrCount: '', // 密码输入错误的次数
        pwdContinuityTime: '', //登录的连续时间
        pwdExpiredEnable: false, // 是否开启密码过期
        pwdExpiredTime: '', // 密码过期时间

        minPwdLength: '',
        maxPwdLength: ''
      },
      pwdStrategyRules: {
        // pwdLength: [
        //   { required: true,
        //     message: "请输入",
        //     trigger: "change"
        //   }
        // ],
        minPwdLength: [
          {
            required: true,
            trigger: ['blur', 'change'],
            validator: validateMinPwd
          }
        ],

        maxPwdLength: [
          {
            required: true,
            trigger: ['blur', 'change'],
            validator: validateMaxPwd
          }
        ],
        pwdLockTime: [
          {
            required: false,
            trigger: 'change',
            validator: validatePwdLockTime
          }
        ],
        pwdErrCount: [
          {
            required: false,
            trigger: 'change',
            validator: validatePwdErrCount
          }
        ],
        pwdContinuityTime: [
          {
            required: false,
            trigger: 'change',
            validator: validatePwdContinuityTime
          }
        ],
        pwdExpiredTime: [
          {
            required: false,
            trigger: 'change',
            validator: validatePwdExpiredTime
          }
        ]
      },
      formLabelWidthStr: '160px',
      pwdStrategyBtnLoading: false,
      // 锁定用户
      lockUserDialog: false,
      lockUserForm: {
        loginAccount: '', // 账号
        userName: '', // 姓名
        pageNum: 1, // 页码
        pageSize: 10 // 分页
      },
      lockUserRules: {},
      // table表格
      lockUserHandleSelData: [], // 多选数据
      lockUserTableData: [],
      lockUserTableLoading: false,
      lockUserTotal: 0 //table表格总条数
    }
  },
  watch: {
    filterText(val) {
      this.$refs.tree.filter(val)
    },
    // 获取baseApi
    baseApi: function(newData) {
      // store.commit("BASE_API", this.baseApi);
    },
    // 获取token
    token: function(newData) {
      // store.commit("TOKEN", this.token);
      // this.onSubmit("formInline", true);
      // this.getRoles();
      // this.getCompanys();
      // this.getEdims("SYS_USER_SEX"); //性别
      // this.getEdims("SYS_USER_STATUS"); //状态
    }
  },
  mounted() {
    this.onSubmit('formInline', true)
    this.getRoles()
    this.getCompanys()
    this.getEdims('SYS_USER_SEX') //性别
    this.getEdims('SYS_USER_STATUS') //状态
  },
  methods: {
    filterNode(value, data) {
      if (!value) return true
      return data.label.indexOf(value) !== -1
    },
    handleCompanyIdChange() {
      this.formCount.deptIds = ''
    },
    // 日期快捷选项
    dateShortcut() {
      return commonFun.dateShortcut()
    },

    // 添加 部门查询逻辑
    selectDeptIdsByAdd(data) {
      this.filterText = ''
      this.operationDeptType = data
      if (this.formCount.companyId == '') {
        return
      }
      let params = {}
      params.companyId = this.formCount.companyId
      pageApi
        .getDeptSourceListByAdd(params)
        .then(response => {
          if (!response.data.error) {
            // 指标树数据
            this.deptData = commonFun.TreeDataPId(response.data.data, '0').data
            let deptChangeNames = this.deptChangeNames
            let deptChangeNamesEdit = this.deptChangeNamesEdit
            let arr = []
            if (this.operationDeptType == 1 && deptChangeNames.length > 0) {
              deptChangeNames.forEach(deptChangeName => {
                arr.push(deptChangeName.deptId)
              })
            }
            if (this.operationDeptType == 2 && deptChangeNamesEdit.length > 0) {
              deptChangeNamesEdit.forEach(deptChangeName => {
                arr.push('' + deptChangeName.deptId)
              })
            }

            this.defaultCheckedKeys = arr
            this.deptDialog = true
          } else {
            this.deptData = []
            this.$message({
              message: response.data.error || '初始化部门失败',
              type: 'warning'
            })
          }
        })
        .catch(() => {
          this.deptData = []
          this.$message({
            message: '初始化部门失败',
            type: 'warning'
          })
        })
    },
    //查询部门
    selectDeptIds(data) {
      this.operationDeptType = data
      this.filterText = ''
      pageApi
        .getDeptSourceList()
        .then(response => {
          if (!response.data.error) {
            // 指标树数据
            this.deptData = commonFun.TreeDataPId(response.data.data, '0').data
            let deptChangeNames = this.deptChangeNames
            let deptChangeNamesEdit = this.deptChangeNamesEdit
            let arr = []
            if (this.operationDeptType == 1 && deptChangeNames.length > 0) {
              deptChangeNames.forEach(deptChangeName => {
                arr.push(deptChangeName.deptId)
              })
            }
            if (this.operationDeptType == 2 && deptChangeNamesEdit.length > 0) {
              deptChangeNamesEdit.forEach(deptChangeName => {
                arr.push('' + deptChangeName.deptId)
              })
            }

            this.defaultCheckedKeys = arr
            this.deptDialog = true
          } else {
            this.deptData = []
            this.$message({
              message: response.data.error || '初始化部门失败',
              type: 'warning'
            })
          }
        })
        .catch(() => {
          this.deptData = []
          this.$message({
            message: '初始化部门失败',
            type: 'warning'
          })
        })
    },
    //查询删除部门
    deleteDeptIds() {
      this.formInline.deptIds = ''
      this.deptChangeNames = []
    },
    //编辑-新增删除部门
    deleteDeptIdsAdd() {
      this.formCount.deptIds = ''
      this.deptChangeNamesAdd = []
      this.deptChangeNamesEdit = []
    },
    //选择部门
    deptSubmit() {
      let selectArr = this.$refs.tree.getCheckedNodes(true)
      this.handleDeptCheckChange(selectArr)
      if (this.operationDeptType === 1) {
        let arr = []
        let deptChangeNames = this.deptChangeNames
        deptChangeNames.forEach(deptChangeName => {
          arr.push(deptChangeName.deptName)
        })
        this.formInline.deptIds = arr.toString()
        this.deptDialog = false
      } else if (this.operationDeptType === 2) {
        let arr = []
        let deptChangeNamesAdd = this.deptChangeNamesAdd

        deptChangeNamesAdd.forEach(deptChangeName => {
          arr.push(deptChangeName.deptName)
        })
        this.deptChangeNamesEdit = deptChangeNamesAdd
        this.formCount.deptIds = arr.toString()
        this.deptDialog = false
      }
    },
    //tree选择事件
    handleDeptCheckChange(selectArr) {
      if (this.operationDeptType === 1) {
        this.deptChangeNames = selectArr
      } else if (this.operationDeptType === 2) {
        this.deptChangeNamesAdd = selectArr
      }
    },
    //列表选择
    handleSelectionChange(val) {
      this.tableMultipleSelection = val
    },
    //排序
    handleSortChange(val) {
      this.formInline.orderStr = commonFun.orderByString(val)
      this.onSubmit('formInline', false)
    },
    //分页
    Pagination(val) {
      this.formInline.pageSize = val.limit //页面条数
      this.formInline.pageNum = val.page //页面
      this.onSubmit('formInline', false)
    },
    // 查询
    onSubmit(formName, flag) {
      this.tableLoading = true
      this.$refs[formName].validate(valid => {
        if (valid) {
          // 消除没有值的参数
          if (flag) {
            this.formInline.pageNum = 1
          }
          let params = commonFun.parameterSrc(this.formInline)
          if (params.date && params.date.length > 0) {
            params.startDate = params.date[0]
            params.endDate = params.date[1]
            params.date = ''
          }

          if (this.operationDeptType == 1) {
            let arr = []
            let deptChangeNames = this.deptChangeNames
            deptChangeNames.forEach(deptChangeName => {
              arr.push(deptChangeName.deptId)
            })
            params.deptIds = arr.toString()
          }
          params = commonFun.parameterSrc(params)
          pageApi
            .getDataSourceList(params)
            .then(response => {
              if (!response.data.error) {
                this.tableData = response.data.data.list
                // 页面总条数
                this.total = response.data.data.total
              } else {
                this.tableData = []
                this.total = 0
                this.formInline.pageSize = 10
                this.formInline.pageNum = 1
              }
              this.tableLoading = false
            })
            .catch(() => {
              this.tableData = []
              this.total = 0
              this.formInline.pageSize = 10
              this.formInline.pageNum = 1
              this.tableLoading = false
            })
        } else {
          return false
        }
      })
    },
    //新增数据
    addData() {
      this.countTitle = '新增用户'
      this.countFormList = 'add'
      this.countDialog = true
      this.isEdit = false
      // 清除
      this.$nextTick(() => {
        this.$refs['formCount'].resetFields()

        this.formCount.account = '' //账户
        this.formCount.password = '' //密码
        this.formCount.passwordAgain = '' //确认密码
        this.formCount.companyId = '' //所属机构
        this.formCount.roleIds = [] //角色
        this.formCount.deptIds = '' //部门
        this.formCount.userNo = '' //编号
        this.formCount.userName = '' //姓名
        this.formCount.nickName = '' //昵称
        this.formCount.sex = '' //性别
        this.formCount.age = '' //年龄
        this.formCount.cellPhone = '' //手机
        this.formCount.telePhone = '' //座机
        this.formCount.email = '' //邮箱
        this.formCount.fax = '' //传真

        let arr = this.statusArr
        for (let i = 0; i < arr.length; i++) {
          if (arr[i].dimNme === '启用') {
            this.formCount.status = arr[i].dimCde //状态
            break
          }
        }
        this.formCount.userId = ''
        this.deptChangeNamesAdd = []
        this.deptChangeNamesEdit = []
      })
    },
    //新增确认
    countSubmit(formName) {
      var self = this
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.$message.closeAll()
          if (!this.isEdit) {
            //新增前校验
            this.checkAccount()
          } else {
            // 修改
            this.updateParamSet()
          }
        } else {
          return false
        }
      })
    },
    saveData() {
      let params = {}
      params = commonFun.parameterSrc(this.formCount)

      if (this.operationDeptType == 2) {
        let arr = []
        let deptChangeNamesAdd = this.deptChangeNamesAdd
        deptChangeNamesAdd.forEach(deptChangeName => {
          arr.push(deptChangeName.deptId)
        })
        params.deptIds = arr
      }
      params = commonFun.parameterSrc(params)
      let password = params.password
      // Base64三重加密传输
      password = Base64.encode(password)
      password = Base64.encode(password)
      password = Base64.encode(password)
      // 密码SHA512加密处理
      password = cryptoJs.SHA512(password).toString()
      params.password = password
      params.passwordAgain = password
      pageApi
        .addDataSource(params)
        .then(response => {
          if (!response.data.error) {
            // 关闭移动指标弹框
            this.countDialog = false
            this.$message.closeAll()
            this.$message({
              message: '新增成功',
              type: 'success'
            })
            // 刷新列表
            this.operationDeptType === 1
            this.restForm()
            this.onSubmit('formInline', true)
          } else {
            // 关闭移动指标弹框
            this.countDialog = false
            this.$message.closeAll()
            this.$message({
              message: response.data.error || '新增失败',
              type: 'warning'
            })
          }
          this.countSubmit_btn = false
        })
        .catch(() => {
          // 关闭移动指标弹框
          this.countDialog = false
          this.countSubmit_btn = false
          this.$message.closeAll()
          this.$message({
            message: '新增失败',
            type: 'warning'
          })
        })
    },
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
          params.password = ''
          params.passwordAgain = ''
          if (this.operationDeptType == 2) {
            let arr = []
            let deptChangeNamesAdd = this.deptChangeNamesEdit
            deptChangeNamesAdd.forEach(deptChangeName => {
              arr.push(deptChangeName.deptId)
            })
            params.deptIds = arr
          }
          params = commonFun.parameterSrc(params)
          this.countSubmit_btn = true
          pageApi
            .updateDataSource(params)
            .then(response => {
              if (!response.data.error) {
                // 关闭移动指标弹框
                this.countDialog = false
                this.$message.closeAll()
                this.$message({
                  message: '修改成功',
                  type: 'success'
                })
                // 刷新树列表
                this.onSubmit('formInline', false)
                this.operationDeptType === 1
              } else {
                // 关闭移动指标弹框
                this.countDialog = false
                this.$message.closeAll()
                this.$message({
                  message: response.data.error || '修改失败',
                  type: 'warning'
                })
              }
              this.countSubmit_btn = false
            })
            .catch(() => {
              // 关闭移动指标弹框
              this.countDialog = false
              this.countSubmit_btn = false
              this.$message.closeAll()
              this.$message({
                message: '修改失败',
                type: 'warning'
              })
            })
        })
        .catch(() => {
          // 关闭移动指标弹框
          this.countDialog = false
          this.countSubmit_btn = false
        })
    },
    //修改数据
    modifierData() {
      if (this.tableMultipleSelection.length === 0) {
        this.$message.closeAll()
        this.$message({
          message: '请选择要修改的数据',
          type: 'warning'
        })
      } else if (this.tableMultipleSelection.length > 1) {
        this.$message.closeAll()
        this.$message({
          message: '只能选择一行数据',
          type: 'warning'
        })
      } else {
        this.editData(this.tableMultipleSelection[0])
      }
    },

    // 行编辑数据
    editData(row) {
      this.countTitle = '编辑用户'
      this.countFormList = 'edit'
      this.operationDeptType = 2
      this.isEdit = true
      this.deptChangeNamesEdit = []
      this.deptChangeNamesAdd = []
      //this.defaultCheckedKeys = ['-199'];
      this.getEditDetail(row)
    },
    //获取用户详情
    getEditDetail(row) {
      let params = {}
      params.userId = row.userId
      pageApi
        .getEditDetail(params)
        .then(response => {
          if (!response.data.error) {
            this.countDialog = true
            this.$nextTick(() => {
              let self = this
              self.$refs['formCount'].resetFields()

              let {
                account,
                password,
                passwordAgain,
                companyId,
                roleIds,
                deptIds,
                userNo,
                userName,
                nickName,
                sex,
                age,
                cellPhone,
                telePhone,
                email,
                fax,
                status,
                userId
              } = response.data.data[0]
              this.formCount.account = account //账户
              this.formCount.password = '123456' //密码写死，修改保存时不传password passwordAgain这两个字段的值
              this.formCount.passwordAgain = '123456' //确认密码
              this.formCount.companyId = companyId //所属机构
              this.formCount.userNo = userNo //编号
              this.formCount.userName = userName //姓名
              this.formCount.nickName = nickName //昵称
              this.formCount.sex = sex //性别
              this.formCount.age = age //年龄
              this.formCount.cellPhone = cellPhone //手机
              this.formCount.telePhone = telePhone //座机
              this.formCount.email = email //邮箱
              this.formCount.fax = fax //传真
              this.formCount.status = status //状态
              this.formCount.userId = userId
              if (response.data.data.length >= 4) {
                let roleArr = response.data.data[3]
                let arr = []
                roleArr.forEach(element => {
                  arr.push(element.roleId)
                })

                this.formCount.roleIds = arr //角色
              }
              if (response.data.data.length >= 3) {
                let deptArr = response.data.data[2]
                let arr = []
                let arrName = []
                deptArr.forEach(element => {
                  let params = {}
                  params.deptName = element.deptName
                  params.deptId = element.deptId
                  arrName.push(element.deptName)
                  arr.push(params)
                })
                this.deptChangeNamesEdit = arr
                this.formCount.deptIds = arrName.toString() //部门
              }
            })
          } else {
            this.$message({
              message: response.data.error || '查询用户详情数据失败',
              type: 'warning'
            })
          }
        })
        .catch(() => {
          this.$message({
            message: response.data.error || '查询用户详情数据失败',
            type: 'warning'
          })
        })
    },
    //启用
    updateEnableStatus(row) {
      let params = {}
      params.userIds = [row.userId]
      pageApi
        .updateEnableStatus(params)
        .then(response => {
          if (!response.data.error) {
            this.$message({
              message: '启用成功',
              type: 'success'
            })
            // 刷新树列表
            this.onSubmit('formInline', false)
          } else {
            this.$message({
              message: response.data.error || '启用失败',
              type: 'warning'
            })
          }
        })
        .catch(() => {
          this.$message({
            message: response.data.error || '启用失败',
            type: 'warning'
          })
        })
    },
    //禁用
    updateDisableStatus(row) {
      let params = {}
      params.userIds = [row.userId]
      pageApi
        .updateDisableStatus(params)
        .then(response => {
          if (!response.data.error) {
            this.$message({
              message: '禁用成功',
              type: 'success'
            })
            // 刷新树列表
            this.onSubmit('formInline', false)
          } else {
            this.$message({
              message: response.data.error || '禁用失败',
              type: 'warning'
            })
          }
        })
        .catch(() => {
          this.$message({
            message: response.data.error || '禁用失败',
            type: 'warning'
          })
        })
    },
    //重置密码
    updatePassword(row) {
      this.passwordDialog = true //重置密码弹框
      this.$nextTick(() => {
        let self = this
        self.$refs['formPassword'].resetFields()
        self.formPassword.userId = row.userId //用户Id
        self.formPassword.newPassword = '' //重置密码
        self.formPassword.newPassword2 = '' //确认密码
      })
    },
    //重置
    restForm() {
      this.formInline.userName = '' //用户名
      this.formInline.date = '' //日期
      this.formInline.deptIds = '' //部门
      this.operationDeptType = ''
      this.deptChangeNames = []
    },
    //导出
    download() {
      // 参数处理
      let params = {}
      if (this.formInline.date.length > 0) {
        //开始时间
        params['staDate'] = this.formInline.date[0]
        //结束时间
        params['endDate'] = this.formInline.date[1]
      }

      // 姓名
      if (this.formInline.userName) {
        params['userName'] = this.formInline.userName
      }
      // 部门
      if (this.formInline.deptIds) {
        params['deptIds'] = this.formInline.deptIds
      }
      // token信息
      if (store.state.user.token) {
        params['token'] = store.state.user.token
      }
      // 表头名
      params['exportAliasName'] = '日期,指标代码,指标名称,组合代码,证券代码,证券市场,外部结果,内部结果,是否异常,受影响的报表,处理方式,处理备注,处理日期'
      // 导出文件名
      params['exportFileName'] = '校验结果.xls'
      // 数据格式化
      params['exportFormat'] = 'string,string,string,string,string,string,string,string,string,string,string,string,string'
      // 表头属性名
      params['exportPoName'] = 'dDate,vcIndCode,vcIndName,vcFundcode,vcSymbol,vcExchange,vcExterValue,vcInnerValue,vcStatus,rptName,vcDealType,cdealMark,dDealDate'
      // 表标题
      params['exportTitle'] = '校验结果'
      // 请求地址
      let action = store.state.setting.baseApi + '/api/index/chkGzResult/download'

      commonFun.formDownloadFile(params, action, 'POST')
    },
    //获取字典数据
    getEdims(dimType) {
      pageApi
        .getEdims(dimType)
        .then(response => {
          if (!response.data.error) {
            // 指标树数据
            if (dimType === 'SYS_USER_SEX') {
              this.sexArr = response.data.data
            } else if (dimType === 'SYS_USER_STATUS') {
              this.statusArr = response.data.data

              let arr = response.data.data
              for (let i = 0; i < arr.length; i++) {
                this.userStatus[arr[i].dimCde] = arr[i].dimNme
              }
            }
          } else {
            this.$message({
              message: response.data.error || '初始化基础数据失败',
              type: 'warning'
            })
          }
        })
        .catch(() => {
          this.$message({
            message: response.data.error || '初始化基础数据失败',
            type: 'warning'
          })
        })
    },
    //获取角色数据
    getRoles(dimType) {
      pageApi
        .getRoles()
        .then(response => {
          if (!response.data.error) {
            // 指标树数据
            this.roleIdsdArr = response.data.data
          } else {
            this.$message({
              message: response.data.error || '初始化角色数据失败',
              type: 'warning'
            })
          }
        })
        .catch(() => {
          this.$message({
            message: response.data.error || '初始化角色数据失败',
            type: 'warning'
          })
        })
    },
    //获取机构数据
    getCompanys() {
      pageApi
        .getCompanys()
        .then(response => {
          if (!response.data.error) {
            // 指标树数据
            this.companyIdArr = response.data.data
          } else {
            this.$message({
              message: response.data.error || '初始化机构数据失败',
              type: 'warning'
            })
          }
        })
        .catch(() => {
          this.$message({
            message: response.data.error || '初始化机构数据失败',
            type: 'warning'
          })
        })
    },
    dataZlStatus(statusCode) {
      return this.userStatus[statusCode]
    },
    //检查账户是否可用
    checkAccount() {
      this.$confirm('确定新增?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          this.countSubmit_btn = true
          let params = {}
          params.account = this.formCount.account
          pageApi
            .checkAccount(params)
            .then(response => {
              if (!response.data.error) {
                this.checkUserNo()
              } else {
                this.$message({
                  message: response.data.error || '校验账户信息失败，账户可能已存在',
                  type: 'warning'
                })
                this.countSubmit_btn = false
              }
            })
            .catch(() => {
              this.$message({
                message: response.data.error || '校验账户信息失败，账户可能已存在',
                type: 'warning'
              })
              this.countSubmit_btn = false
            })
        })
        .catch(() => {
          this.countSubmit_btn = false
        })
    },
    checkUserNo() {
      let params = {}
      params.companyId = this.formCount.companyId
      params.userNo = this.formCount.userNo
      pageApi
        .checkUserNo(params)
        .then(response => {
          if (!response.data.error) {
            this.saveData()
          } else {
            this.$message({
              message: response.data.error || '校验员工编号失败，员工编号可能已存在',
              type: 'warning'
            })
            this.countSubmit_btn = false
          }
        })
        .catch(() => {
          this.$message({
            message: response.data.error || '校验账户信息失败，员工编号可能已存在',
            type: 'warning'
          })
          this.countSubmit_btn = false
        })
    },
    //重置密码
    passwordSubmit(formName) {
      var self = this
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.countSubmit_btn = true
          let params = commonFun.parameterSrc(this.formPassword)
          let password = params.newPassword
          // Base64三重加密传输
          password = Base64.encode(password)
          password = Base64.encode(password)
          password = Base64.encode(password)
          params.newPasswordPlain = password
          // 密码SHA512加密处理
          password = cryptoJs.SHA512(password).toString()
          params.newPassword = password
          params.newPassword2 = password
          pageApi
            .resetPwd(params)
            .then(response => {
              if (!response.data.error) {
                this.$message({
                  message: response.data.error || '重置成功',
                  type: 'success'
                })
                this.passwordDialog = false
              } else {
                this.$message({
                  message: response.data.error || '重置失败',
                  type: 'warning'
                })
              }
              this.countSubmit_btn = false
            })
            .catch(() => {
              this.$message({
                message: response.data.error || '重置失败',
                type: 'warning'
              })
              this.countSubmit_btn = false
            })
        } else {
          return false
        }
      })
    },
    // 账户锁定change事件
    pwdLockEnableChange() {
      this.$refs['formPwdStrategy'].validate(valid => {
        if (valid) {
        } else {
          return
        }
      })
    },
    // 密码过期change事件
    pwdExpiredEnableChange() {
      this.$refs['formPwdStrategy'].validate(valid => {
        if (valid) {
        } else {
          return
        }
      })
    },
    // 密码策略设置
    pwdStrategy() {
      this.pwdStrategyLoading = true
      // 密码策略赋值
      pageApi
        .getPwdStrategy()
        .then(response => {
          this.pwdStrategyDialog = true
          // 值清空
          this.$nextTick(() => {
            this.$refs['formPwdStrategy'].resetFields()
            this.formPwdStrategy.pwdComplexity = []

            if (response.data.status === 0) {
              let res = response.data.data
              // 密码长度
              //  if(res.pwdLength){
              //    this.formPwdStrategy.pwdLength = res.pwdLength;
              //  }

              if (res.pwdLength) {
                let pwdSet = res.pwdLength.split('-')
                this.formPwdStrategy.pwdLength = res.pwdLength
                this.formPwdStrategy.minPwdLength = pwdSet[0]
                this.formPwdStrategy.maxPwdLength = pwdSet[1]
              }
              // 密码复杂度
              if (res.pwdComplexity) {
                this.formPwdStrategy.pwdComplexity = res.pwdComplexity.split(',')
              }
              // 是否开始自动解锁
              if (res.pwdAutoUnLock === true || res.pwdAutoUnLock === false) {
                this.formPwdStrategy.pwdAutoUnLock = res.pwdAutoUnLock
              }
              // 是否开启登录失败账户锁定
              if (res.pwdLockEnable === true || res.pwdLockEnable === false) {
                this.formPwdStrategy.pwdLockEnable = res.pwdLockEnable
              }
              // 锁定时间 (分钟)
              if (res.pwdLockTime) {
                this.formPwdStrategy.pwdLockTime = res.pwdLockTime
              }
              // 密码输入错误的次数
              if (res.pwdErrCount) {
                this.formPwdStrategy.pwdErrCount = res.pwdErrCount
              }
              //登录的连续时间
              if (res.pwdContinuityTime) {
                this.formPwdStrategy.pwdContinuityTime = res.pwdContinuityTime
              }
              // 是否开启密码过期
              if (res.pwdExpiredEnable === true || res.pwdExpiredEnable === false) {
                this.formPwdStrategy.pwdExpiredEnable = res.pwdExpiredEnable
              }
              // 密码过期时间
              if (res.pwdExpiredTime) {
                this.formPwdStrategy.pwdExpiredTime = res.pwdExpiredTime
              }
            } else {
              this.$message.closeAll()
              this.$message({
                message: '获取密码策略失败',
                type: 'error'
              })
            }
          })
          this.pwdStrategyLoading = false
        })
        .catch(() => {
          this.$nextTick(() => {
            this.$refs['formPwdStrategy'].resetFields()
            this.formPwdStrategy.pwdComplexity = []
          })
          this.pwdStrategyDialog = true
          this.$message.closeAll()
          this.$message({
            message: '获取密码策略失败',
            type: 'error'
          })
          this.pwdStrategyLoading = false
        })
    },
    // 密码策略设置提交
    pwdStrategySubmit(formName) {
      if (this.formPwdStrategy.minPwdLength == '') {
        this.$message({
          message: '请输入密码长度',
          type: 'warning'
        })
        return
      }
      if (this.formPwdStrategy.minPwdLength < 6) {
        this.$message({
          message: '密码长度最低6位',
          type: 'warning'
        })
        return
      }
      if (this.formPwdStrategy.maxPwdLength == '') {
        this.$message({
          message: '请输入密码长度',
          type: 'warning'
        })
        return
      }
      if (this.formPwdStrategy.maxPwdLength - this.formPwdStrategy.minPwdLength <= 0) {
        this.$message({
          message: '最大长度必须大于最小长度',
          type: 'warning'
        })
        return
      }

      if (this.formPwdStrategy.pwdComplexity.length == 0) {
        this.$message({
          message: '请选择密码复杂度',
          type: 'warning'
        })
        return
      }
      if (this.formPwdStrategy.pwdComplexity.length == 1) {
        if (this.formPwdStrategy.pwdComplexity[0] == 3) {
          this.$message({
            message: '不能全是特殊字符',
            type: 'warning'
          })
          return
        }
      }
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.pwdStrategyBtnLoading = true

          this.formPwdStrategy.pwdLength = this.formPwdStrategy.minPwdLength + '-' + this.formPwdStrategy.maxPwdLength

          let params = JSON.parse(JSON.stringify(this.formPwdStrategy))
          params.pwdComplexity = this.formPwdStrategy.pwdComplexity.join(',')
          params.pwdLength = this.formPwdStrategy.pwdLength
          pageApi
            .postPwdStrategy(params)
            .then(response => {
              if (response.data.status === 200) {
                this.$message.closeAll()
                this.$message({
                  message: '密码策略设置成功',
                  type: 'success'
                })
                this.pwdStrategyDialog = false
              } else {
                this.$message.closeAll()
                this.$message({
                  message: response.data.message || '密码策略设置失败',
                  type: 'error'
                })
              }
              this.pwdStrategyBtnLoading = false
            })
            .catch(() => {
              this.pwdStrategyBtnLoading = false
            })
        } else {
          return
        }
      })
    },
    // 锁定用户管理
    searchLockUser() {
      this.lockUserDialog = true
      this.$nextTick(() => {
        this.lockUserSubmit('lockUserForm', true)
      })
    },
    // 锁定账户分页
    lockUserPagination(val) {
      this.lockUserForm.pageSize = val.limit //页面条数
      this.lockUserForm.pageNum = val.page //页面
      this.lockUserSubmit('lockUserForm', false)
    },
    // 锁定用户管理搜索
    lockUserSubmit(formName, isPageNumReset) {
      this.$refs[formName].validate(valid => {
        if (valid) {
          // 页码置为1
          if (isPageNumReset === true) {
            this.lockUserForm.pageNum = 1
          }
          this.lockUserTableLoading = true
          let params = this.lockUserForm
          params.lockStatus = '1'
          pageApi
            .getLockingUser(params)
            .then(response => {
              if (response.data.status === 200) {
                this.lockUserTableData = response.data.data.list
                this.lockUserTotal = response.data.data.total
              } else {
                this.lockUserTableData = []
                this.lockUserTotal = 0
                this.lockUserForm.pageSize = 10
                this.lockUserForm.pageNum = 1
                this.$message.closeAll()
                this.$message({
                  message: '查询失败！',
                  type: 'error'
                })
              }
              this.lockUserTableLoading = false
            })
            .catch(() => {
              this.lockUserTableData = []
              this.lockUserTotal = 0
              this.lockUserForm.pageSize = 10
              this.lockUserForm.pageNum = 1
              this.lockUserTableLoading = false
            })
        } else {
          return
        }
      })
    },
    // 重置
    lockUserRestForm() {
      this.$refs['lockUserForm'].resetFields()
    },
    // table 批量选择
    lockUserHandleSelChange(val) {
      this.lockUserHandleSelData = val
    },
    // 行解锁
    unlockUserRows(val) {
      this.postUnlockUser(val.uuid)
    },
    // 批量解锁
    unlockUserBatch() {
      if (this.lockUserHandleSelData.length === 0) {
        this.$message.closeAll()
        this.$message({
          message: '请选择要批量解锁的用户',
          type: 'warning'
        })
      } else {
        let arr = []
        this.lockUserHandleSelData.forEach(item => {
          arr.push(item.uuid)
        })
        arr = arr.join(',')
        this.postUnlockUser(arr)
      }
    },
    // 解锁接口
    postUnlockUser(val) {
      this.$alert('确认解锁', '提示', {
        confirmButtonText: '确定',
        type: 'warning'
      })
        .then(() => {
          let params = {}
          params.uuid = val
          pageApi
            .postManualUnlock(params)
            .then(response => {
              if (response.data.status === 200) {
                this.$message.closeAll()
                this.$message({
                  message: '解锁成功',
                  type: 'success'
                })
                // 刷新列表
                this.lockUserSubmit('lockUserForm', false)
              } else {
                this.$message.closeAll()
                this.$message({
                  message: '解锁失败',
                  type: 'error'
                })
              }
            })
            .catch(() => {})
        })
        .catch(() => {})
    }
  }
}
</script>

<style lang="scss" scoped>
::v-deep .el-button.el-button--info {
  background-color: #fff;
  color: #612d10;
}
::v-deep .el-table .el-table__body tr > td {
  background-color: transparent !important; /* 例如，设置为浅灰色 */
}
.formPwd-checkbox {
  margin-top: 8px;
}
</style>
<style>
.customUserWidth {
  width: 50% !important;
}
</style>

<template>
  <div class="setting">
    <el-form :inline="true" class="standard-form" ref="formCount" style="margin: 0 auto" :model="formCount" :rules="countRules" label-width="120px" label-position="right">
      <el-row>
        <el-col :span="12">
          <el-form-item label="登录账户" prop="account" class="mb20">
            <el-input :disabled="true" type="text" v-model.trim="formCount.account" clearable placeholder="请输入" size="small"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item :style="{ 'margin-top': true ? '0px' : '15px' }" label="所属机构" prop="companyId" class="mb20">
            <el-select :disabled="true" v-model="formCount.companyId" size="small" placeholder="请选择" filterable>
              <el-option v-for="(group, index) in companyIdArr" :value="group.deptId" :key="index" :label="group.deptName"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item label="员工编号" prop="userNo" class="mb20">
            <el-input :disabled="true" type="text" v-model.trim="formCount.userNo" clearable placeholder="请输入" size="small"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="部门" prop="deptIds " class="mb20">
            <el-input v-model="formCount.deptIds" :disabled="true" placeholder="请选择" size="small"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item label="姓名" prop="userName" class="mb20">
            <el-input type="text" v-model.trim="formCount.userName" clearable placeholder="请输入" size="small"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="性别" prop="sex" class="mb20">
            <el-select v-model="formCount.sex" size="small" placeholder="请选择">
              <el-option v-for="(group, index) in sexArr" :value="group.dimCde" :key="index" :label="group.dimNme"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item label="手机" prop="cellPhone" class="mb20">
            <el-input type="text" v-model.trim="formCount.cellPhone" clearable placeholder="请输入" size="small"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="邮箱" prop="email" class="mb20">
            <el-input type="text" v-model.trim="formCount.email" clearable placeholder="请输入" size="small"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <div slot="footer" class="dialog-footer standard-form">
      <el-button type="primary" size="small" :loading="countSubmit_btn" @click="saveFormCount">提 交</el-button>
      <el-button size="small" type="info" plain @click="close">取 消</el-button>
    </div>
  </div>
</template>

<script>
import { getEditDetail, getCompanys, getEdims, updateDataSource } from './scripts/api'
export default {
  name: 'Setting',
  data() {
    return {
      formCount: {
        account: '',
        cellPhone: '',
        companyId: '',
        deptIds: '',
        email: '',
        fax: '',
        nickName: '',
        age: '',
        roleIds: [],
        sex: '',
        status: '',
        telePhone: '',
        userName: '',
        userNo: ''
      },
      countRules: {
        userName: [
          {
            required: true,
            type: 'string',
            message: '请输入姓名',
            trigger: 'blur'
          }
        ],
        cellPhone: [
          {
            required: true,
            pattern: /^[1][3,4,5,7,8][0-9]{9}$/,
            trigger: ['blur', 'change'],
            message: '请输入正确的手机号'
          }
        ],
        email: [
          {
            required: true,
            type: 'email',
            message: '请输入正确的邮箱地址',
            trigger: ['blur', 'change']
          }
        ]
      },
      countSubmit_btn: false,
      sexArr: [],
      companyIdArr: [],
      deptChangeNamesEdit: []
    }
  },
  mounted() {
    this.getSexEdims()
    this.getCompanys()
    this.initSettingInfo()
  },
  methods: {
    getCompanys() {
      getCompanys()
        .then((response) => {
          if (!response.data.error) {
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
    getSexEdims() {
      getEdims('SYS_USER_SEX')
        .then((response) => {
          if (!response.data.error) {
            this.sexArr = response.data.data
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
    initSettingInfo() {
      let BAIDUID = JSON.parse(localStorage.getItem('BAIDUID')) || {}
      getEditDetail({
        userId: BAIDUID.userId || ''
      }).then((res) => {
        const { status, data } = res.data
        if (status === 200) {
          if (data && data.length) {
            for (let key in this.formCount) {
              this.formCount[key] = data[0][key]
            }
            if (data.length >= 4) {
              let roleArr = data[3]
              let arr = []
              roleArr.forEach((element) => {
                arr.push(element.roleId)
              })

              this.formCount.roleIds = arr //角色
            } else {
              this.formCount.roleIds = []
            }
            if (data.length >= 3) {
              let deptArr = data[2]
              let arr = []
              let arrName = []
              deptArr.forEach((element) => {
                let params = {}
                params.deptName = element.deptName
                params.deptId = element.deptId
                arrName.push(element.deptName)
                arr.push(params)
              })
              this.deptChangeNamesEdit = arr
              this.formCount.deptIds = arrName.toString() //部门
            } else {
              this.formCount.deptIds = ''
            }
          } else {
            for (let key in this.formCount) {
              this.formCount[key] = ''
            }
            this.formCount.deptIds = ''
          }
        } else {
          for (let key in this.formCount) {
            this.formCount[key] = ''
          }
          this.formCount.deptIds = ''
        }
      })
    },
    close() {
      this.$emit('close')
    },
    saveFormCount() {
      this.$refs.formCount.validate((vaild) => {
        if (vaild) {
          let BAIDUID = JSON.parse(localStorage.getItem('BAIDUID')) || {}
          const params = {
            ...this.formCount,
            userId: BAIDUID.userId || ''
          }
          let arr = []
          let deptChangeNamesAdd = this.deptChangeNamesEdit
          deptChangeNamesAdd.forEach((deptChangeName) => {
            arr.push(deptChangeName.deptId)
          })
          params.deptIds = arr
          this.countSubmit_btn = true
          updateDataSource(params)
            .then((response) => {
              if (!response.data.error) {
                this.close()
                this.$message.closeAll()
                this.$message({
                  message: '修改成功',
                  type: 'success'
                })
              } else {
                this.$message.closeAll()
                this.$message({
                  message: response.data.error || '修改失败',
                  type: 'warning'
                })
              }
              this.countSubmit_btn = false
            })
            .catch(() => {
              this.countSubmit_btn = false
              this.$message.closeAll()
              this.$message({
                message: '修改失败',
                type: 'warning'
              })
            })
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.dialog-footer {
  margin-top: 20px;
  text-align: center;
}
</style>

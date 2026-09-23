<template>
  <div class="RightDrawerBtn">
    <el-button v-show="isUser" plain type="primary" size="medium" @click="updateStatus('formHandle','Normal','同意')">同意</el-button>
    <el-button v-show="isUser" plain type="info" size="medium" @click="updateStatus('formHandle','Retire','退回')">退回</el-button>
    <el-button v-show="!isUser" plain  type="primary" size="medium" @click="updateStatus('formHandle',0,'划款成功')">划款成功</el-button>
    <el-button v-show="!isUser" plain  type="primary" size="medium" @click="updateStatus('formHandle',1,'划款失败')">划款失败</el-button>
    <el-button v-if="$hasPermission(hasPermissionPause)" plain type="primary" v-show="isPause" size="medium" @click="updateStatus('formHandle','Pause','暂缓')">暂缓</el-button>
    <el-button v-if="$hasPermission(hasPermissionUnPause)" plain type="primary" v-show="!isPause" size="medium" @click="updateStatus('formHandle','UnPause','解除暂缓')">解除暂缓</el-button>
    <el-button v-if="$hasPermission(hasPermissionCancle)" plain type="warning" size="medium" @click="updateStatus('formHandle','Cancle','撤销')">撤销</el-button>
    <el-button v-if="$hasPermission(hasPermissionAbandon)" plain type="info" size="medium" @click="updateStatus('formHandle','Abandon','作废')">作废</el-button>
  </div>
</template>
<script>
import cmCheckApi from '@/api/transfer/cmdCheck'
import { stepMenuBtn } from '@/utils/stepBtn'
export default {
  data () {
    return {
      isUser: true,
      isPause: true,
      hasPermissionPause: '',
      hasPermissionUnPause: '',
      hasPermissionCancle: '',
      hasPermissionAbandon: '',
      formHandle: {
        remark: ''
      },
      myTaskId: ''
    }
  },
  methods: {
    init (data) {
      let initData = { ...data }
      Promise.all([this.defaultData()]).then(() => {
        this.getData(initData)
        this.rightControl(initData)
      })
    },
    // 初始化数据
    defaultData () {
      this.isUser = true
      this.isPause = true
      this.hasPermissionPause = ''
      this.hasPermissionUnPause = ''
      this.hasPermissionCancle = ''
      this.hasPermissionAbandon = ''
      this.formHandle.remark = ''
      this.myTaskId = ''
    },
    // 权限按钮控制
    getData (data) {
      this.myTaskId = data.data.pfomTaskid
      let btn = stepMenuBtn(data)
      // console.log('btn', btn)
    },
    // 按钮相对控制
    rightControl (data) {
      if (data.data.taskKey == 'transfer_hkjg') this.isUser  = false
      else this.isUser = true
      if (data.data.dataForm.cmdStatus == 'cmdSuspend') {
        this.isPause = false
      } else this.isPause = true
    },
    //审核通过，退回，作废，暂缓等操作
    updateStatus(vals,status,confirmStatus){
        this.$confirm('是否'+confirmStatus,'提示',{
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
              let remark = this.$parent.$parent.$parent.$parent.getRemark()  //获取父节点的回调函数值
              this.formHandle.remark = remark
              let params = Object.assign({},this.formHandle);
              let sendData = {};
              let taskExcuteCmdMode = {taskExcuteCmdType:status};
              let taskOpinionModel = {agree:true};
              taskOpinionModel.opinion = this.formHandle.remark;
              let formData = {};
              formData.remoteOperationFlag = false;
              sendData.formData = formData;
              sendData.taskOpinionModel = taskOpinionModel;
              if(status === 0){
                  formData.transferResult = true;
                  taskExcuteCmdMode['taskExcuteCmdType'] = 'Normal'
              }else if (status === 1){
                formData.transferResult = false;
                taskExcuteCmdMode['taskExcuteCmdType'] = 'Normal'
              } else {}
              sendData.taskExcuteCmdMode = taskExcuteCmdMode;
              cmCheckApi.updateStatus(this.myTaskId,sendData).then(res => {
                let data= res.data.data;
                if(res.data.status === 0){
                  this.$message.closeAll();
                      this.$message({
                        type: 'success',
                        message: '操作成功'
                      });
                  this.$emit('rightDrawerBtn')
                  this.$emit('refashBtn')
                }else{
                  this.$message.closeAll();
                  this.$message({
                  type: 'error',
                  message: res.data.message ||'操作失败'
                  });
                }
            })
        }).catch((err) => { console.log('is msg err', err)})
    },
  }
}
</script>
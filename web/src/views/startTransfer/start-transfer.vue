<template>
  <div class="startTranter">
    <el-steps :active="active" finish-status="success" process-status='finish'>
        <el-step
          v-for="(item, index) in stepData"
          :key="index"
          :title="item.stepTitle"
          :description="item.des"
        ></el-step>
      </el-steps>
  </div>
</template>
<script>
import request from '@/utils/request'
import qs from 'qs'
export default {
  props: {
    transferKey: {
      type: String
    },
    isGtja:{
      default:''
    },
    noTransaction:{
      default:""
    }
  },
  data () {
    return {
      active: 0,
      stepData: [],
    }
  },
  mounted () {
    this.getStepData()
  },
  watch:{
    isGtja(data){
      this.getStepData()
    }
  },
  methods: {
    getStepData () {
      let key = this.transferKey
      let isGtja = this.isGtja
      let noTransaction = this.noTransaction
      request({
          url: '/api/process/v1.0/process/' + key + '/taskIndex?isGtja='+isGtja+'&noTransaction='+noTransaction,
          method: 'get'
        }).then(({data: res}) => {
          if (res.data == null) return
          let temp = new Array
          for (let item of res.data) {
            if (item.isShow) {
              let stepObj = new Object
              if (item.taskStatus == 'COMPLETED') {
                stepObj['des'] = '已完成'
              } else if (item.taskStatus == 'RUNNING') {
                this.active = item.taskIndex-1  //用于哪一步
                stepObj['des'] = '当前处理'
              } else {
                stepObj['des'] = '待执行'
              }
              stepObj['taskStatus'] = item.taskStatus
              stepObj['xmlId'] = item.xmlId
              stepObj['stepTitle'] = item.taskName
              stepObj['step'] = item.taskIndex-1
              temp.push(stepObj)
            }
        }
        this.stepData = temp
        }).catch(() => {})
    }
  }
}
</script>
<style lang='scss'>
.startTranter {
  width: 85%;
  margin: 0 auto;
  .is-process, .is-wait, .is-finish {
    cursor: default !important;
    color: #c0c4cc !important;
    border-color: #c0c4cc !important;
  }
}
</style>
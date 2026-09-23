<template>
  <div>
     <el-form :model="formInline" ref="formInline" label-position="right" label-width="180px">
       <el-row>
        <!-- top -->
        <el-col>
          <el-form-item label='收益分配说明'>
            <el-tooltip placement="right" :disabled='changeData ? incomePortionDesc != formInline.incomePortionDesc ? false : true : true'>
              <div slot="content">修改前: {{ incomePortionDesc || '-' }}</div>
              <el-input type="textarea" :autosize="{minRows: 3}" v-model="formInline.incomePortionDesc" disabled :class=" changeData ? incomePortionDesc != formInline.incomePortionDesc ? 'errInof' : '' : ''"></el-input>
            </el-tooltip>
            <!-- <el-input type="textarea" v-model="formInline.incomePortionDesc" disabled></el-input>
            <div v-if="changeData">
              <div class="errStyleArea" v-if='incomePortionDesc != formInline.incomePortionDesc'>修改前: {{incomePortionDesc || '-'}}</div>
            </div> -->
          </el-form-item>
        </el-col>
      </el-row>
      <!-- bottom -->
      <el-row>
        <el-col>
          <el-form-item :label="item.labelName" v-for="item in bassInfoBottom" :key="item.modelValue">
            <el-tooltip placement="right" :disabled='changeData ? item.change != formInline[item.modelValue] ? false : true : true'>
              <div slot="content">修改前: {{ item.change || '-' }}</div>
              <el-input v-model="formInline[item.modelValue]" disabled :class=" changeData ? item.change != formInline[item.modelValue] ? 'errInof' : '' : ''"></el-input>
            </el-tooltip>
            <!-- <el-input v-model="formInline[item.modelValue]" disabled></el-input>
            <div v-if="changeData">
              <div class="errStyle" v-if='item.change != formInline[item.modelValue]'>修改前: {{item.change|| '-'}}</div>
            </div> -->
          </el-form-item>
        </el-col>
      </el-row>
     </el-form>
  </div>
</template>
<script>
import pageApi from "@/api/product/productSearch";
export default {
  data () {
    return {
      bassInfoBottom: [
        { labelName: '分配次数', modelValue: 'portionNumber', change: '' },
        { labelName: '提交分红流程', modelValue: 'bonusProcess', change: '' },
        { labelName: '预估数据以及计算报表', modelValue: 'dataExpect', change: '' },
        { labelName: '分红数据确认', modelValue: 'bonusConfim', change: '' },
        { labelName: '分红资金交收', modelValue: 'bonusDeliver', change: '' },
      ],
      formInline: {
        incomePortionDesc: '',
        portionNumber: '',
        bonusProcess: '',
        dataExpect: '',
        bonusConfim: '',
        bonusDeliver: ''
      },
      incomePortionDesc: '-',
      changeData: {}
    }
  },
  methods: {
    init (data, flag) {
      let dataInfo = {...data.fundInfo}
      this.changeData = flag
      this.getDtata(dataInfo)
      this.hasChangDataNolmal(flag)
    },
    judgeChange (data, flag) {
      if (!flag) return false
      for (let i in this.formInline) {
        if (data.fundInfo[i] != flag.fundInfo[i]) return true
      }
    },
    getDtata (dataInfo) {
      for (let i in this.formInline) {
        if (dataInfo[i])  this.formInline[i] = dataInfo[i]
        else this.formInline[i] = '-'
      }
      if (this.changeData) {
        let dataInfo1 = {...this.changeData.fundInfo}
        if (dataInfo1['incomePortionDesc']) this.incomePortionDesc = dataInfo1['incomePortionDesc']
        else this.incomePortionDesc = '-'
      }
      // 异步函数
      this.getEdimsGet('fundPortionNumberType', 'portionNumber', 'bassInfoBottom', 0)
    },
    hasChangDataNolmal (flag) {
      if (flag) {
        let dataInfo = {...flag.fundInfo}
        this.bassInfoBottom.forEach(i => {
          if (dataInfo[i.modelValue]) {
            i.change = dataInfo[i.modelValue]
          } else i.change = '-'
        })
      }
    },
    getEdimsGet (parmas, val, dataList, index) {
      pageApi.getTransferType(parmas).then(({data: res}) => {
        if (!res.data) return
        let data = res.data
        for (let i of data) {
          if (i.dimCde == this.formInline[val]) this.formInline[val] = i.dimNme
        }
        this.hasChangData2 (data, val, dataList, index)
      }).catch(() => {});
    },
    hasChangData2 (data, val, dataList, index) {
      if (this.changeData) {
        let dataInfo = {...this.changeData.fundInfo}
        for (let i of data) {
          if (i.dimCde == dataInfo[val]) this[dataList][index].change = i.dimNme
        }
      }
    },
  }
}
</script>
<style scoped>
.errStyle {
  position: absolute;
  top: 24px;
  font-size: 14px;
  color: red;
}
.errStyleArea {
  font-size: 14px;
  color: red;
}
</style>

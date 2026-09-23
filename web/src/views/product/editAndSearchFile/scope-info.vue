<template>
  <div>
     <el-form :model="formInline" ref="formInline" label-position="right" label-width="150px">
       <el-row>
        <!-- top -->
        <el-col>
          <el-form-item label='投资范围'>
            <div class="product_detail">
              <el-checkbox v-model="checkAll" disabled>
                全选
              </el-checkbox>
              <div style="margin: 15px 0;"></div>
              <el-checkbox-group v-model="checkfundInvestArea">
                <div v-for="(group, index) in fundInvestArea" :key="index">

                  <el-tooltip placement="right" :disabled='true'>
                    <div slot="content">
                      <span v-if="!group.change">
                        修改前: {{ group.des || '-' }}
                      </span>
                    </div>
                    <el-checkbox :label="group.id" disabled>
                      <span :class=" !group.change ? 'errInof' : '' "> {{group.dimNme}} </span>
                    </el-checkbox>
                  </el-tooltip>
                </div>
              </el-checkbox-group>
            </div>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <!-- top -->
        <el-col>
          <el-form-item label='投资限制'>
            <!-- <el-input type="textarea" v-model="formInline.investLimit" disabled></el-input> -->
            <el-tooltip placement="right" :disabled='changeData ? investLimit != formInline.investLimit ? false : true : true'>
              <div slot="content">修改前: {{ investLimit || '-' }}</div>
              <el-input type="textarea" v-model="formInline.investLimit" disabled :class=" changeData ? investLimit != formInline.investLimit ? 'errInof' : '' : ''"></el-input>
            </el-tooltip>
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
            <!-- <el-input v-model="formInline[item.modelValue]" disabled></el-input> -->
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
      fundInvestArea: [],
      checkAll: false,
      checkfundInvestArea: [],
      bassInfoBottom: [
        { labelName: '预警线', modelValue: 'warnPoint', change: '-' },
        { labelName: '止损线', modelValue: 'lossPoint', change: '-'  },
      ],
      formInline: {
        investLimit: '',
        warnPoint: '',
        lossPoint: '',
      },
      tg: false,
      investLimit: '-',
      chackList: [],
      // hasCheckfundInvest: [],
      changeData: {},
      dafaluteInfo: {}
    }
  },
  methods: {
    init (data, flag) {
      // console.log('getData', data)
      // console.log('flag', flag)
      let dataInfo = {...data.fundInfo}
      this.chackList = data.fundInvests || []
      this.changeData = flag
      this.dafaluteInfo = data
      this.getDtata(dataInfo)
      this.hasChangDataNolmal(flag)
      // if (flag) this.isCheackChange(data, flag)
      if (this.chackList.length) {
        for (let i of this.chackList) {
          this.checkfundInvestArea.push(i.investScope)
        }
      }
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
        if (dataInfo1['investLimit']) this.investLimit = dataInfo1['investLimit']
        else this.investLimit = '-'
      }
      // 异步函数
      this.getEdimsGet('fund_investArea')
    },
    isCheackChange (data, flag, textareaList) {
      // console.log(textareaList)
      let after =  data.fundInvests || []
      let befor =  flag.fundInvests || []
      let warning = false
      let temp = new Array
      let temp2 = new Array
      let temp3 = new Array
      let temp4 = new Array
      for (let i of after) {
        for (let j of befor) {
          if (i.investScope == j.investScope) temp.push({ id: i.investScope, change: true})  //得到相同的
        }
      }
      for (let j of after) temp2.push(j.investScope)
      for (let j of befor) temp2.push(j.investScope)
      temp2 = Array.from(new Set(temp2))  //去掉重复的
      for (let i of temp2) {
        this.tg = false
        for (let j of temp) {
          if (j.id == i && j.change) this.tg = true
        }
        if (!this.tg) {
          warning = true
          temp3.push({ id: i, change: true , des: '是'})
        }
        else temp3.push({ id: i, change: false, des: '否'})
      }
      textareaList.forEach( i => {
        let kg = false
        temp3.forEach( j => {
          if (i.dimCde == j.id && j.change) {  kg = true }
        })
        if (!kg) temp4.push({id: i.dimCde, change: true, des: '否', dimNme: i.dimNme})
        else temp4.push({id: i.dimCde, change: false, des: '是', dimNme: i.dimNme})
      });
      // console.log(temp3)
      // console.log(temp3)
      // console.log(temp3)
      this.fundInvestArea = temp4
      this.$emit('getScopeData', warning)
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
    getEdimsGet (parmas, val) {
      pageApi.getTransferType(parmas).then(({data: res}) => {
        if (!res.data) return
        let data = res.data
        // this.fundInvestArea = data
        if (this.changeData) this.isCheackChange(this.dafaluteInfo, this.changeData, data)
        else this.defaluteCheck(data)
        if (data.length === this.chackList.length) this.checkAll = true
        else this.checkAll = false
      }).catch(() => {});
    },
    defaluteCheck (data) {
      let temp = new Array
      for (let i of data) {
        temp.push({id: i.dimCde, change: true, des: '否', dimNme: i.dimNme})
      }
      this.fundInvestArea = temp
    }
  }
}
</script>
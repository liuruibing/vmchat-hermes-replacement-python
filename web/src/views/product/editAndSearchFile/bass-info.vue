<template>
  <div class="bassInfoStyle">
    <el-form :model="formInline" ref="formInline" label-position="right" label-width="150px" size="small">
      <el-row :gutter="2">
        <!-- left -->
        <el-col :span="11">
          <el-form-item :label="item.labelName" v-for="item in bassInfoLeft" :key="item.modelValue">
            <el-tooltip placement="right" :disabled='changeData ? item.change != formInline[item.modelValue] ? false : true : true'>
              <div slot="content">修改前: {{ item.change || '-' }}</div>
              <el-input v-model="formInline[item.modelValue]" disabled :class=" changeData ? item.change != formInline[item.modelValue] ? 'errInof' : '' : ''"></el-input>
            </el-tooltip>
             <!-- <div v-if="changeData">
               <div class="errStyle" v-if='item.change != formInline[item.modelValue]'>修改前: {{item.change || '-'}}</div>
             </div> -->

          </el-form-item>
        </el-col>
        <!-- right -->
        <el-col :span="11">
          <el-form-item :label="item.labelName" v-for="item in bassInfoRight" :key="item.modelValue">
            <el-tooltip placement="right" :disabled='changeData ? item.change != formInline[item.modelValue] ? false : true : true'>
              <div slot="content">修改前: {{ item.change || '-' }}</div>
              <el-input v-model="formInline[item.modelValue]" disabled :class=" changeData ? item.change != formInline[item.modelValue] ? 'errInof' : '' : ''"></el-input>
            </el-tooltip>
            <!-- <div v-if="changeData">
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
import productDictionary from "@/dataDictionary/product";
export default {
  data() {
    return {
      bassInfoLeft: [
        {labelName: '产品代码', modelValue: 'fundCode', change: ''},
        {labelName: '英文名称', modelValue: 'fundNameEn', change: ''},
        {labelName: '托管人名称', modelValue: 'trustorCode', change: ''},
        {labelName: '基金类型', modelValue: 'fundTypeDetails', change: ''},
        {labelName: '证券营业部', modelValue: 'operateDept', change: ''},
        {labelName: '产品存续期限', modelValue: 'holdYear', change: ''},
        {labelName: '风险等级', modelValue: 'riskLevel', change: ''},
        {labelName: '产品备案代码', modelValue: 'recordCode', change: ''},
        {labelName: '是否分类', modelValue: 'isGrade', change: ''}
      ],
      bassInfoRight: [
        {labelName: '产品名称', modelValue: 'fundName', change: ''},
        {labelName: '管理人名称', modelValue: 'managerCode', change: ''},
        {labelName: '基金服务机构', modelValue: 'operatorCode', change: ''},
        {labelName: '投资方向', modelValue: 'investDirect', change: ''},
        {labelName: '基金成立日期', modelValue: 'setupDate', change: ''},
        {labelName: '基金到期日期', modelValue: 'expireDate', change: ''},
        {labelName: '基金备案日期', modelValue: 'recordDate', change: ''},
        {labelName: '运作方式', modelValue: 'operateType', change: ''},
        {labelName: '产品状态', modelValue: 'fundState', change: ''}
      ],
      formInline: {
        expireDate:'',
        fundName: "",
        fundNameEn: '',
        trustorCode: '',
        operateDept: '',
        holdYear: '',
        riskLevel: '',
        recordCode: '',
        isGrade: '',
        fundCode: '',
        managerCode: '',
        operatorCode: '',
        setupDate: '',
        recordDate: '',
        operateType: '',
        fundState: '',
        investDirect: '',
        fundType:'',
        fundTypeDetails:"", //基金类型-二级
      },
      changeData: {},
    };
  },

  methods: {
    init (data, flag) {
      let dataInfo = {...data.fundInfo}
      this.changeData = flag
      this.hasChangDataNolmal(flag)
      this.getDtata(dataInfo)
    },
    judgeChange (data, flag) {
      if (!flag) return false
      for (let i in this.formInline) {
        if (data.fundInfo[i] != flag.fundInfo[i]) return true
      }
    },
    getDtata (dataInfo) {
      for (let i in this.formInline) {
        if (dataInfo[i] || dataInfo[i] == 0)  this.formInline[i] = dataInfo[i]
        else this.formInline[i] = '-'
      }
      // 同步函数
      this.initData ()
      // 异步函数
      this.getDeptInfoSel('institution_manager')
      this.getDeptInfoSel('institution_trusteeship')
      this.getDeptInfoSel('institution_operator')
      // this.getEdimsGet('fundTypes', 'fundType', 'bassInfoLeft', 3)
      this.getEdimsGet('fundInvestDirectType', 'investDirect', 'bassInfoRight', 3)
      this.getEdimsGet('fundRiskLevelType', 'riskLevel', 'bassInfoLeft', 6)
      this.getEdimsGet('fundinfo_fundState', 'fundState','bassInfoRight', 8)
      this.getFundTypeDetails()
    },
    getFundTypeDetails(){
      pageApi.getFundType().then(res=>{
        if(res.data.status === 200){
          let data = res.data.data;
          for (let i of data) {
            if (i.fundTypeDetails == this.formInline.fundTypeDetails) this.formInline.fundTypeDetails = i.fundTypeDetailName || ''

          }
          if (this.changeData) {
            let dataInfo = {...this.changeData.fundInfo}
            for (let i of data) {
              if (i.fundTypeDetails == dataInfo['fundTypeDetails']) this.bassInfoLeft[3].change = i.fundTypeDetailName
            }
          }

        }else{
          this.options = [];
          this.$message({
            type:"error",
            message:"获取基金类型失败"
          })
        }
      }).catch(()=>{

      })
    },
    hasChangDataNolmal (flag) {
      if (flag) {
        let dataInfo = {...flag.fundInfo}
        this.bassInfoLeft.forEach(i => {
          if (dataInfo[i.modelValue]) {
            i.change = dataInfo[i.modelValue]
          } else i.change = '-'
        })
        this.bassInfoRight.forEach(i => {
          if (dataInfo[i.modelValue]) {
            i.change = dataInfo[i.modelValue]
          } else i.change = '-'
        })
      }
    },
    hasChangData1 (data) {
      if (this.changeData) {
        let dataInfo = {...this.changeData.fundInfo}
        for (let j of data) {
          if (j.id == dataInfo.managerCode) this.bassInfoRight[1].change = j.instName
          if (j.id == dataInfo.trustorCode) this.bassInfoLeft[2].change = j.instName
          if (j.id == dataInfo.operatorCode) this.bassInfoRight[2].change = j.instName
        }
      }
    },
    hasChangData2 (data, val, datalist, index) {
      if (this.changeData) {
        let dataInfo = {...this.changeData.fundInfo}
        for (let i of data) {
          if (i.dimCde == dataInfo[val]) this[datalist][index].change = i.dimNme
        }
      }
    },
    initData () {
      let data = productDictionary
      let dataInfo = {}
      if (this.changeData) dataInfo = { ...this.changeData.fundInfo }
      for (let i of data.operateType) {
        if (i.dimCde == this.formInline.operateType) this.formInline.operateType = i.dimNme
        if (this.changeData) {
          if (i.dimCde == dataInfo.operateType) {
            this.bassInfoRight[7].change = i.dimNme
          }
        }
      }
      for (let i of data.isGrade) {
        if (i.dimCde == this.formInline.isGrade) this.formInline.isGrade = i.dimNme
        if (this.changeData) {
          if (i.dimCde == dataInfo.isGrade) {
            this.bassInfoLeft[8].change = i.dimNme
          }
        }
      }
    },
    getDeptInfoSel(code) {
      // console.log(code);
      this.arr1 = []
      let parmas = {instTypeDim:code}
      pageApi.getDeptInfoSel(parmas).then((response) => {
        if (response.status === 200) {
          let arr = response.data.data;
          for (let i of arr) {
            if (i.id == this.formInline.managerCode) this.formInline.managerCode = i.instName
            if (i.id == this.formInline.trustorCode) this.formInline.trustorCode = i.instName
            if (i.id == this.formInline.operatorCode) this.formInline.operatorCode = i.instName
          }
          this.hasChangData1(arr)
        }
      }).catch(() => {});
    },
    getEdimsGet (parmas, val, datalist, index) {
      pageApi.getTransferType(parmas).then(({data: res}) => {
        if (!res.data) return
        let data = res.data
        for (let i of data) {
          if (i.dimCde == this.formInline[val]) this.formInline[val] = i.dimNme
        }
        this.hasChangData2 (data, val, datalist, index)
      }).catch(() => {});
    },
  }
}
</script>
<style lang='scss'>
.errStyle {
  position: absolute;
  top: 24px;
  font-size: 14px;
  color: red;
}
</style>

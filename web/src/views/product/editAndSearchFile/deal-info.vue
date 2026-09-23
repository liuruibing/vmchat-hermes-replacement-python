<template>
  <div>
    <el-form :model="formInline" ref="formInline" label-position="right" label-width="180px">
      <el-row :gutter="2">
        <!-- left -->
        <el-col :span="11">
          <el-form-item :label="item.labelName" v-for="item in bassInfoLeft" :key="item.modelValue">
            <el-tooltip placement="right" :disabled='changeData ? item.change != formInline[item.modelValue] ? false : true : true'>
              <div slot="content">修改前: {{ item.change || '-' }}</div>
              <el-input v-model="formInline[item.modelValue]" disabled :class=" changeData ? item.change != formInline[item.modelValue] ? 'errInof' : '' : ''"></el-input>
            </el-tooltip>
          </el-form-item>

          <el-form-item label="赎回费率(%)" v-if="fdFlag">
            <el-tooltip placement="right" :disabled='changeData ? callRateTypeChange != formInline.callRate ? false : true : true'>
              <div slot="content">修改前: {{ callRateTypeChange || '-' }}</div>
              <el-input v-model="formInline.callRate" disabled :class=" changeData ? callRateTypeChange != formInline.callRate ? 'errInof' : '' : ''"></el-input>
            </el-tooltip>
            <!-- <el-input v-model="formInline.callRate" disabled></el-input>
            <div v-if="changeData">
              <div class="errStyle" v-if='callRateTypeChange != formInline.callRate'>修改前: {{callRateTypeChange || '-'}}</div>
            </div> -->
          </el-form-item>
          <el-form-item label="赎回费率类型" v-if="!fdFlag">
            <el-tooltip placement="right" :disabled='changeData ? callRateTypeChange != formInline.callRateType ? false : true : true'>
              <div slot="content">修改前: {{ callRateTypeChange || '-' }}</div>
              <el-input v-model="formInline.callRateType" disabled :class=" changeData ? callRateTypeChange != formInline.callRateType ? 'errInof' : '' : ''"></el-input>
            </el-tooltip>
            <!-- <el-input v-model="formInline.callRateType" disabled></el-input>
            <div v-if="changeData">
              <div class="errStyle" v-if='callRateTypeChange != formInline.callRateType'>修改前: {{callRateTypeChange || '-'}}</div>
            </div> -->
          </el-form-item>
        </el-col>
        <!-- right -->
        <el-col :span="12">
          <el-form-item :label="item.labelName" v-for="item in bassInfoRight" :key="item.modelValue">
            <el-tooltip placement="right" :disabled='changeData ? item.change != formInline[item.modelValue] ? false : true : true'>
              <div slot="content">修改前: {{ item.change || '-' }}</div>
              <el-input v-model="formInline[item.modelValue]" disabled :class=" changeData ? item.change != formInline[item.modelValue] ? 'errInof' : '' : ''"></el-input>
            </el-tooltip>
            <!-- <el-input v-model="formInline[item.modelValue]" disabled></el-input>
            <div v-if="changeData">
              <div class="errStyle" v-if='item.change != formInline[item.modelValue]'>修改前: {{item.change || '-'}}</div>
            </div> -->
          </el-form-item>
        </el-col>
      </el-row>
      <!-- table -->
      <el-row v-if="!fdFlag">
        <el-col :offset="2" :span="21">
            <div style="margin-top: 5px">
              <el-table :data="dataList" border>
                <el-table-column type="index" header-align="center" align="center" width="40" label='序号'></el-table-column>
                <el-table-column
                    v-for="(item, index) in tableNameList"
                    :key='index'
                    :label="item.labelName"
                    :prop="item.propName"
                    header-align="center"
                    align="center"
                    show-overflow-tooltip
                    min-width="100">
                  <template slot-scope="scope">
                    <!-- <span v-if="scope.row.change ? scope.row[item.propName] == scope.row.change[item.propName] : true">{{scope.row[item.propName]}}</span>
                    <span v-else style="color: red">{{scope.row[item.propName]}}</span> -->
                     <el-tooltip placement="right" :disabled='scope.row.change ? scope.row[item.propName] != scope.row.change[item.propName] ? false : true : true'>
                       <div slot="content">
                         <span v-if="scope.row.change">修改前: {{ scope.row.change[item.propName] || '-' }}</span>
                       </div>
                       <span :class=" scope.row.change ? scope.row[item.propName] != scope.row.change[item.propName] ? 'errInof' : '' : ''">{{scope.row[item.propName]}}</span>
                     </el-tooltip>
                  </template>
                </el-table-column>
              </el-table>
            </div>
        </el-col>
      </el-row>
    </el-form>
  </div>
</template>
<script>
import pageApi from "@/api/product/productSearch";
import productDictionary from "@/dataDictionary/product";
import { correlationData } from '@/utils/product-info-db'
export default {
  data() {
    return {
      tableNameList: [
        { labelName: '*区间起点', propName: 'redeemFrom'},
        { labelName: '*区间终点', propName: 'redeemTo'},
        { labelName: '*费率（%）', propName: 'redeemRate'},
      ],
      bassInfoLeft: [
        {labelName: '认申购起点（不含费）元', modelValue: 'purchasePoint', change: ''},
        {labelName: '认购交易确认天数', modelValue: 'subscribeConfirmDay', change: ''},
        {labelName: '认购费率(%)', modelValue: 'subscribeRate', change: ''},
        {labelName: '申购资金交收天数', modelValue: 'applyDeliverDay', change: ''},
        {labelName: '销售服务费计提', modelValue: 'saleFeePrepare', change: ''},
        {labelName: '赎回交易确认天数', modelValue: 'callConfirmDay', change: ''},
        {labelName: '赎回费率浮动类型', modelValue: 'callFloatType', change: ''},
      ],
      bassInfoRight: [
        {labelName: '封闭期', modelValue: 'blockDate', change: ''},
        {labelName: '追加认申购级差', modelValue: 'purchaseDiffAppend', change: ''},
        {labelName: '认购资金交收天数', modelValue: 'subscribeDeliverDay', change: ''},
        {labelName: '申购交易确认天数', modelValue: 'applyConfirmDay', change: ''},
        {labelName: '申购费率(%)', modelValue: 'applyRate', change: ''},
        {labelName: '销售服务费支付', modelValue: 'saleFeePay', change: ''},
        {labelName: '赎回资金交收天数', modelValue: 'callDeliverDay', change: ''},
        {labelName: '估值频率', modelValue: 'assetFrequency', change: ''},
      ],
      formInline: {
        purchasePoint: "",
        subscribeConfirmDay: '',
        subscribeRate: '',
        applyDeliverDay: '',
        saleFeePrepare: '',
        callConfirmDay: '',
        callFloatType: '',
        purchaseDiffAppend: '',
        subscribeDeliverDay: '',
        applyConfirmDay: '',
        applyRate: '',
        saleFeePay: '',
        callDeliverDay: '',
        blockDate: '',
        callRate: '',
        callRateType: '',
        assetFrequency: '',
      },
      fdFlag: true,
      dataList: [],
      changeData: {},
      callRateTypeChange: '',
      guZhiist: [], // 估值频率
    };
  },
  methods: {
    init (data, flag) {
      let dataInfo = {...data.fundInfo}
      this.changeData = flag
      this.hasChangDataNolmal(flag)
      this.getData(dataInfo)
      let dataInfoList = [...data.fundRedeems] || []
      let beForData = flag ? [...flag.fundRedeems] : []
      let isChangeData = new Array
      if (flag) isChangeData = correlationData(dataInfoList, beForData)
      else isChangeData = correlationData(dataInfoList)
      this.dataList = isChangeData
    },
    judgeChange (data, flag) {
     if (!flag) return false
     for (let i in this.formInline) {
        if (data.fundInfo[i] != flag.fundInfo[i]) return true
      }
      if (!this.fdFlag) {
        for (let j of this.dataList) {
          if (j.change) {
            if (j.redeemFrom != j.change.redeemFrom) return true
            if (j.redeemTo != j.change.redeemTo) return true
            if (j.redeemRate != j.change.redeemRate) return true
          }
        }
      }
    },
    getData (dataInfo) {
      for (let i in this.formInline) {
        if (dataInfo[i])  this.formInline[i] = dataInfo[i]
        else this.formInline[i] = '-'
      }
      // 同步函数
      let fd = JSON.parse(JSON.stringify(this.formInline.callFloatType))
      this.hasCallFloatType(fd)
      this.initData ()
      // 异步函数
      this.getEdimsGet('fundSubscribeConfirmDayType', 'subscribeConfirmDay', 'bassInfoLeft', 1)
      this.getEdimsGet('fundSubscribeDeliverDayType', 'subscribeDeliverDay', 'bassInfoRight', 2)
      this.getEdimsGet('fundApplyConfirmDayType', 'applyConfirmDay', 'bassInfoRight', 3)
      this.getEdimsGet('fundApplyDeliverDayType', 'applyDeliverDay', 'bassInfoLeft', 3)
      this.getEdimsGet('fundCallConfirmDayType', 'callConfirmDay', 'bassInfoLeft', 5)
      this.getEdimsGet('fundCallDeliverDayType', 'callDeliverDay', 'bassInfoRight', 6)
      this.getEdimsGet('fundCallFloatType', 'callRateType')
	  this.getEdimsGet('gz_date', 'assetFrequency','bassInfoRight',7)
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
    // 列表数据对比
    initData () {
      let data = productDictionary
      let dataInfo = {}
      if (this.changeData) dataInfo = { ...this.changeData.fundInfo }
      for (let i of data.saleFeePrepare) {
        if (i.dimCde == this.formInline.saleFeePrepare) this.formInline.saleFeePrepare = i.dimNme
        if (this.changeData) {
          if (i.dimCde == dataInfo.saleFeePrepare) {
            this.bassInfoLeft[4].change = i.dimNme
          }
        }
      }
      for (let i of data.saleFeePay) {
        if (i.dimCde == this.formInline.saleFeePay) this.formInline.saleFeePay = i.dimNme
        if (this.changeData) {
          if (i.dimCde == dataInfo.saleFeePay) {
            this.bassInfoRight[5].change = i.dimNme
          }
        }
      }
      for (let i of data.callFloatType) {
        if (i.dimCde == this.formInline.callFloatType) this.formInline.callFloatType = i.dimNme
        if (this.changeData) {
          if (i.dimCde == dataInfo.callFloatType) {
            this.bassInfoLeft[6].change = i.dimNme
          }
        }
      }
      for (let i of this.guZhiist) {
        if (i.dimCde == this.formInline.assetFrequency) this.formInline.assetFrequency = i.dimNme
        if (this.changeData) {
          if (i.dimCde == dataInfo.assetFrequency) {
            this.bassInfoRight[7].change = i.dimNme
          }
        }
      }
    },
    hasCallFloatType (data) {
      if (data == '0') {
        this.fdFlag = true
        if (this.changeData) this.callRateTypeChange = this.changeData.fundInfo.callRate
      }
      else {
        this.fdFlag = false
        if (this.changeData) this.callRateTypeChange = this.changeData.fundInfo.callRateType
      }
    },
    getEdimsGet (parmas, val, datalist, index) {
      pageApi.getTransferType(parmas).then(({data: res}) => {
        if (!res.data) return
        let data = res.data
        for (let i of data) {
          if (i.dimCde == this.formInline[val]) this.formInline[val] = i.dimNme
          if (val == 'callRateType') {
            if (this.changeData) {
              if (i.dimCde == this.changeData.fundInfo[val]) this.callRateTypeChange = i.dimNme
            }
          }
        }
       this.hasChangData2 (data, val, datalist, index)
      }).catch(() => {});
    },
    hasChangData2 (data, val, datalist, index) {
      if (this.changeData) {
        if (datalist) {
          let dataInfo = {...this.changeData.fundInfo}
          for (let i of data) {
            if (i.dimCde == dataInfo[val]) this[datalist][index].change = i.dimNme
          }
        } else {
          for (let i of data) {
            if (i.dimCde == dataInfo[val]) this.callRateType = i.dimNme
          }
        }
      }
    },
  }
};
</script>
<style scoped>
.errStyle {
  position: absolute;
  top: 24px;
  font-size: 14px;
  color: red;
}
</style>

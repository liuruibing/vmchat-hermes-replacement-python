<template>
  <div>
    <el-form :model="formInline" ref="formInline" label-position="right" label-width="180px">
       <!-- top -->
      <el-row v-for="item in bassInfoTop" :key="item.labelName">
        <el-col>
          <el-form-item :label='item.labelName' >
            <el-row :gutter="3">
              <el-col :span="7" v-for="item2 in item.chlidren" :key="item2.modelValue">
                <el-tooltip placement="right" :disabled='changeData ? item2.change != formInline[item2.modelValue] ? false : true : true'>
                  <div slot="content">修改前: {{ item2.change || '-' }}</div>
                  <el-input v-model="formInline[item2.modelValue]" disabled :class=" changeData ? item2.change != formInline[item2.modelValue] ? 'errInof' : '' : ''"></el-input>
                </el-tooltip>
                <!-- <el-input v-model="formInline[item2.modelValue]" disabled></el-input>
                <div v-if="changeData">
                  <div class="errStyle" v-if='item2.change != formInline[item2.modelValue]'>修改前: {{item2.change || '-'}}</div>
                  <div v-else class="noStyle">.</div>
                </div> -->
              </el-col>
            </el-row>
          </el-form-item>
        </el-col>
      </el-row>
      <!-- bottom -->
      <el-row :gutter="2">
        <el-col :span="11">
          <el-form-item :label="item.labelName" v-for="item in bassInfoBottomLeft" :key="item.modelValue">
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
        <el-col :span="11">
          <el-form-item :label="item.labelName" v-for="item in bassInfoBottomRight" :key="item.modelValue" :class="[item.visibility?'visibility_hidden':'']">
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
      <!-- 计提方式 -->
      <el-row>
        <el-col :span="24" v-if="isTable">
          <el-form-item label="计提方式">
            <el-row :gutter="3">
              <el-col :span="7">
                <el-tooltip placement="right" :disabled='changeData ? dataChange.rewardPrepareType != formInline.rewardPrepareType ? false : true : true'>
                  <div slot="content">修改前: {{ dataChange.rewardPrepareType || '-' }}</div>
                  <el-input v-model="formInline.rewardPrepareType" disabled :class=" changeData ? dataChange.rewardPrepareType != formInline.rewardPrepareType ? 'errInof' : '' : ''"></el-input>
                </el-tooltip>
                <!-- <el-input v-model="formInline.rewardPrepareType" disabled></el-input>
                <div v-if="changeData">
                  <div class="errStyle" v-if='dataChange.rewardPrepareType != formInline.rewardPrepareType'>修改前: {{dataChange.rewardPrepareType || '-'}}</div>
                  <div v-else class="noStyle">.</div>
                </div> -->
              </el-col>
              <el-col :span="7">
                <el-tooltip placement="right" :disabled='changeData ? dataChange.isFixedPrepare != formInline.isFixedPrepare ? false : true : true'>
                  <div slot="content">修改前: {{ dataChange.isFixedPrepare || '-' }}</div>
                  <el-input v-model="formInline.isFixedPrepare" disabled :class=" changeData ? dataChange.isFixedPrepare != formInline.isFixedPrepare ? 'errInof' : '' : ''"></el-input>
                </el-tooltip>
                <!-- <el-input v-model="formInline.isFixedPrepare" disabled></el-input>
                <div v-if="changeData">
                  <div class="errStyle" v-if='dataChange.isFixedPrepare != formInline.isFixedPrepare'>修改前: {{dataChange.isFixedPrepare || '-'}}</div>
                  <div v-else class="noStyle">.</div>
                </div> -->
              </el-col>
              <el-col :span="7">
                <el-tooltip placement="right" :disabled='changeData ? dataChange.rewardPrepareDate != formInline.rewardPrepareDate ? false : true : true'>
                  <div slot="content">修改前: {{ dataChange.rewardPrepareDate || '-' }}</div>
                  <el-input v-model="formInline.rewardPrepareDate" disabled :class=" changeData ? dataChange.rewardPrepareDate != formInline.rewardPrepareDate ? 'errInof' : '' : ''"></el-input>
                </el-tooltip>
                <!-- <el-input v-model="formInline.rewardPrepareDate" disabled></el-input>
                <div v-if="changeData">
                  <div class="errStyle" v-if='dataChange.rewardPrepareDate != formInline.rewardPrepareDate'>修改前: {{dataChange.rewardPrepareDate || '-'}}</div>
                  <div v-else class="noStyle">.</div>
                </div> -->
              </el-col>
            </el-row>
            <div style="margin-top: 15px">
              <el-table :data="dataList" border>
                <el-table-column type="index" header-align="center" align="center" width="40" label="序号"></el-table-column>
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
                    <el-tooltip placement="right" :disabled='scope.row.change ? scope.row[item.propName] != scope.row.change[item.propName] ? false : true : true'>
                       <div slot="content">
                         <span v-if="scope.row.change">修改前: {{ scope.row.change[item.propName] || '-' }}</span>
                       </div>
                       <span :class=" scope.row.change ? scope.row[item.propName] != scope.row.change[item.propName] ? 'errInof' : '' : ''">{{scope.row[item.propName]}}</span>
                     </el-tooltip>
                    <!-- <span v-if="scope.row.change ? scope.row[item.propName] == scope.row.change[item.propName] : true">{{scope.row[item.propName]}}</span>
                    <span v-else style="color: red">{{scope.row[item.propName]}}</span> -->
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </el-form-item>
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
        { labelName: '*区间起点', propName: 'rewardFrom'},
        { labelName: '*区间终点', propName: 'rewardTo'},
        { labelName: '*计提比例（%）', propName: 'rewardRate'},
      ],
      bassInfoTop: [
        { labelName: '管理费', chlidren: [
           { modelValue: 'manageFeePrepare', change: '-'},
           { modelValue: 'manageFeeAsset', change: '-'},
           { modelValue: 'manageFeePay', change: '-'},
          ]
        },
        { labelName: '托管费', chlidren: [
           { modelValue: 'trustFeePrepare', change: '-'},
           { modelValue: 'trustFeeAsset', change: '-'},
           { modelValue: 'trustFeePay', change: '-'},
          ]
        },
        { labelName: '运营服务费', chlidren: [
           { modelValue: 'operateFeePrepare', change: '-'},
           { modelValue: 'operateFeeAsset', change: '-'},
           { modelValue: 'operateFeePay', change: '-'},
         ]
        },
      ],
      bassInfoBottomLeft: [
        {labelName: '管理费率(%)', modelValue: 'manageRate', change: '-'},
        {labelName: '运营服务费(%)', modelValue: 'operateRate', change: '-'},
        {labelName: '管理人账号', modelValue: 'manageAccount', change: '-'},
        {labelName: '业绩报酬', modelValue: 'rewardType', change: '-'},
      ],
      bassInfoBottomRight: [
        {labelName: '托管费率(%)', modelValue: 'trustRate', change: '-'},
        {labelName: '', modelValue: '', change: '-',visibility:true},
        {labelName: '管理人收费账户名称', modelValue: 'manageAccountName', change: '-'},
        {labelName: '管理人开户银行名称', modelValue: 'manageBankName', change: '-'},
      ],
      formInline: {
        manageFeePrepare: "",
        manageFeeAsset: "",
        manageFeePay: "",
        trustFeePrepare: "",
        trustFeeAsset: "",
        trustFeePay: "",
        operateFeePrepare: "",
        operateFeeAsset: "",
        operateFeePay: "",
        manageRate: '',
        operateRate: '',
        manageAccount: '',
        rewardType: '',
        trustRate: '',
        manageAccountName: '',
        manageBankName: '',
        rewardPrepareType: '',
        isFixedPrepare: '',
        rewardPrepareDate: '',
      },
      dataChange: {
        rewardPrepareType: '-',
        isFixedPrepare: '-',
        rewardPrepareDate: '-',
      },
      isTable: false,
      dataList: [],
      changeData: {}
    };
  },
  methods: {
    init (data, flag) {
      // console.log('data', data)
      let dataInfo = {...data.fundInfo}
      this.changeData = flag
      this.getData(dataInfo)
      this.hasChangDataNolmal(flag)

      let dataInfoList = [...data.fundRewards] || []
      let beForData = flag ? [...flag.fundRewards] : []
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
      if (this.isTable) {
        for (let j of this.dataList) {
          if (j.change) {
            if (j.rewardFrom != j.change.rewardFrom) return true
            if (j.rewardTo != j.change.rewardTo) return true
            if (j.rewardRate != j.change.rewardRate) return true
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
      this.initData ()
      // 异步函数
      let MD = ['manageFeePrepare', 'trustFeePrepare', 'operateFeePrepare']
      let MD1 = ['manageFeeAsset', 'trustFeeAsset', 'operateFeeAsset']
      let MD2 = ['manageFeePay', 'trustFeePay', 'operateFeePay']
      this.getEdimsGet('fundManageFeePrepareType', 'manageFeePrepare', MD, 'bassInfoTop', 0)
      this.getEdimsGet('fundManageFeeStand', 'manageFeeAsset', MD1, 'bassInfoTop', 1)
      this.getEdimsGet('fundManageFeePayType', 'operateFeePay', MD2, 'bassInfoTop', 2)
      this.getEdimsGet('fundRewardType', 'rewardType', null, 'bassInfoBottomLeft', 3)
      this.getEdimsGet('fundRewardPrepareType', 'rewardPrepareType', null)
      this.getEdimsGet('fundrewardPrepareDate', 'rewardPrepareDate', null)
    },
    hasChangDataNolmal (flag) {
      if (flag) {
        let dataInfo = {...flag.fundInfo}
        this.bassInfoBottomLeft.forEach(i => {
          if (dataInfo[i.modelValue]) {
            i.change = dataInfo[i.modelValue]
          } else i.change = '-'
        })
        this.bassInfoBottomRight.forEach(i => {
          if (dataInfo[i.modelValue]) {
            i.change = dataInfo[i.modelValue]
          } else i.change = '-'
        })
      }
    },
    initData () {
      let data = productDictionary
      if (this.formInline.rewardType == 'NONE' || this.formInline.rewardType == '' ||this.formInline.rewardType == '-') this.isTable = false
      else this.isTable = true
      for (let i of data.isFixedPrepare) {
        if (i.dimCde == this.formInline.isFixedPrepare) this.formInline.isFixedPrepare = i.dimNme
        if (this.changeData) {
          let dataInfo = {...this.changeData.fundInfo}
          if (i.dimCde == dataInfo['isFixedPrepare']) this.dataChange['isFixedPrepare'] = i.dimNme
        }
      }
    },
    getEdimsGet (parmas, val, array, datalist, index) {
      pageApi.getTransferType(parmas).then(({data: res}) => {
        if (!res.data) return
        let data = res.data
        if (array) this.tsDatas(data, array, index)
        else {
          for (let i of data) {
           if (i.dimCde == this.formInline[val]) this.formInline[val] = i.dimNme
           if (this.changeData) {
             let dataInfo = {...this.changeData.fundInfo}
             if (i.dimCde == dataInfo[val]) this.dataChange[val] = i.dimNme
           }
          }
          this.hasChangData2 (data, val, datalist, index)
        }
      }).catch(() => {});
    },
    tsDatas (data, array, index) {
      for (let i of data) {
        if (i.dimCde == this.formInline[array[0]]) this.formInline[array[0]] = i.dimNme
        if (i.dimCde == this.formInline[array[1]]) this.formInline[array[1]] = i.dimNme
        if (i.dimCde == this.formInline[array[2]]) this.formInline[array[2]] = i.dimNme
        if (this.changeData) {
          let dataInfo = {...this.changeData.fundInfo}
          if (i.dimCde == dataInfo[array[0]]) this.bassInfoTop[0].chlidren[index].change = i.dimNme
          if (i.dimCde == dataInfo[array[1]]) this.bassInfoTop[1].chlidren[index].change = i.dimNme
          if (i.dimCde == dataInfo[array[2]]) this.bassInfoTop[2].chlidren[index].change = i.dimNme
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
    }
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
.noStyle {
  position: absolute;
  top: 24px;
  font-size: 1px;
  color: #fff;
}
.visibility_hidden{
  visibility:hidden;
}
</style>

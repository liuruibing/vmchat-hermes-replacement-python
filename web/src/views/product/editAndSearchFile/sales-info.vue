<template>
  <div>
    <!-- <div>
      <el-form :model="formInline" ref="formInline" label-width="80px" size="small">
        <el-form-item label="销售方式" prop="saleType">
          <el-input v-model="formInline.saleType" disabled></el-input>
        </el-form-item>
      </el-form>
    </div> -->
    <div style="margin-top: 15px">
      <el-table :data="dataList" border>
        <el-table-column type="index" label="序号" header-align="center" align="center" show-overflow-tooltip width="40"></el-table-column>
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
  </div>
</template>
<script>
import pageApi from "@/api/product/productSearch";
import { correlationData } from '@/utils/product-info-db'
export default {
  data () {
    return {
      tableNameList: [
        { labelName: '渠道名称', propName: 'sallerName'},
        { labelName: '渠道编码', propName: 'sallerCode'},
        { labelName: '销售方式', propName: 'sallerType'},
        { labelName: '管理费分成比例（%）', propName: 'feeRate'},
        { labelName: '开始日期', propName: 'beginDate'},
        { labelName: '结束日期', propName: 'endDate'},
      ],
      dataList: [],
      saleSallArr: [],
      saleTypeArr: [],
      formInline: {
        saleType: ''
      }
    }
  },
  methods: {
    init (data, flag) {
      let dataInfo = [...data.fundSallers] || []
      let beForData = flag ? [...flag.fundSallers] : []
      let isChangeData = new Array
      if (flag) isChangeData = correlationData(dataInfo, beForData)
      else isChangeData = dataInfo
      this.dataList = isChangeData
      this.getDtata(isChangeData)
    },  
    judgeChange (data, flag) {
      if (!flag) return false
      for (let j of this.dataList) {
        if (j.change) {
          if (j.sallerName != j.change.sallerName) return true
          if (j.sallerCode != j.change.sallerCode) return true
          if (j.sallerType != j.change.sallerType) return true
          if (j.feeRate != j.change.feeRate) return true
          if (j.beginDate != j.change.beginDate) return true
          if (j.endDate != j.change.endDate) return true
        }
      }
    },
    getDtata (dataInfo) {
     if (dataInfo.length) {
       this.getEdimsGet('fundSaleType', 'saleType')
      }
    },
    getEdimsGet (parmas, val) {
      pageApi.getTransferType(parmas).then(({data: res}) => {
        if (!res.data) return
        let data = res.data
        this.saleTypeArr = [...data]
        this.saleTypeList(data)
      }).catch(() => {});
    },
    saleTypeList (data) {
      for (let i of data) {
        for (let j of this.dataList) {
          if (i.dimCde == j.sallerType) j.sallerType = i.dimNme
          if (j.change && j.change.sallerType) {
            if (i.dimCde == j.change.sallerType) j.change.sallerType = i.dimNme
          }
        }
      }
    }
  }
}
</script>
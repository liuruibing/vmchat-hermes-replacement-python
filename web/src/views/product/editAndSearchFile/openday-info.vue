<template>
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
</template>
<script>
import pageApi from "@/api/product/productSearch";
import { correlationData } from '@/utils/product-info-db'
export default {
  data () {
    return {
      tableNameList: [
        { labelName: '开放频率', propName: 'openFrequence'},
        { labelName: '开放规则', propName: 'openRule'},
        { labelName: '规则生效日期', propName: 'beginDate'},
        { labelName: '规则失效日期', propName: 'endDate'},
      ],
      dataList: []
    }
  },
  methods: {
    init (data, flag) {
      let dataInfo = [...data.fundOpens] || []
      let beForData = flag ? [...flag.fundOpens] : []
      let isChangeData = new Array
      if (flag) isChangeData = correlationData(dataInfo, beForData)
      else isChangeData = dataInfo
      this.dataList = isChangeData
      this.getDtata()
    },
    judgeChange (data, flag) {
      if (!flag) return false
      for (let j of this.dataList) {
        if (j.change) {
          if (j.openFrequence != j.change.openFrequence) return true
          if (j.openRule != j.change.openRule) return true
          if (j.beginDate != j.change.beginDate) return true
          if (j.endDate != j.change.endDate) return true
        }
      }
    },
    getDtata () {
      this.getEdimsGet('fundOpenFrequence', 'openFrequence')
      this.getEdimsGet('fundOpenRule', 'openRule')
    },
    getEdimsGet (parmas, val) {
      // let parmas = 'fundSaleType', val = 'saleType' fundOpenRule
      pageApi.getTransferType(parmas).then(({data: res}) => {
        if (!res.data) return
        let data = res.data
        this.saleTypeList(data, val)
      }).catch(() => {});
    },
    saleTypeList (data, val) {
      for (let i of data) {
        for (let j of this.dataList) {
          if (i.dimCde == j[val]) j[val] = i.dimNme
          if (j.change && j.change[val]) {
            if (i.dimCde == j.change[val]) j.change[val] = i.dimNme
          }
        }
      }
    }
  }
}
</script>
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
import { correlationData } from '@/utils/product-info-db'
export default {
  data () {
    return {
      tableNameList: [
        { labelName: '分类代码', propName: 'fundCodeGrade'},
        { labelName: '分类名称', propName: 'fundNameGrade'},
        { labelName: '初始单位净值', propName: 'assetValue'},
        { labelName: '基金分类级别', propName: 'shareType'},
        { labelName: '开始日期', propName: 'beginDate'},
        { labelName: '结束日期', propName: 'endDate'},
      ],
      dataList: []
    }
  },
  methods: {
    init (data, flag) {
      let dataInfo = data.fundGrades ? [...data.fundGrades] : []
      let beForData = flag ? [...flag.fundGrades] : []
      let isChangeData = new Array
      if (flag) isChangeData = correlationData(dataInfo, beForData)
      else isChangeData = dataInfo
      this.dataList = isChangeData
    },
    judgeChange (data, flag) {
      if (!flag) return false
      for (let j of this.dataList) {
        if (j.change) {
          if (j.fundCodeGrade != j.change.fundCodeGrade) return true
          if (j.fundNameGrade != j.change.fundNameGrade) return true
          if (j.assetValue != j.change.assetValue) return true
          if (j.shareType != j.change.shareType) return true
          if (j.beginDate != j.change.beginDate) return true
          if (j.endDate != j.change.endDate) return true
        }
      }
    }
  }
}
</script>
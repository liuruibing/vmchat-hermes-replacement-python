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
import { correlationData } from '@/utils/product-info-db'
export default {
  data () {
    return {
      tableNameList: [
        { labelName: '基金经理', propName: 'managerName'},
        { labelName: '投资策略', propName: 'investStrategy'},
        { labelName: '联系电话', propName: 'phone'},
        { labelName: '联系邮箱', propName: 'email'},
      ],
      dataList: []
    }
  },
  methods: {
    init (data, flag) {
      // console.log('getdata',data.fundManagers)
      // console.log('getdata',data)
      let dataInfo = [...data.fundManagers] || []
      let beForData = flag ? [...flag.fundManagers] : []
      let isChangeData = new Array
      if (flag) isChangeData = correlationData(dataInfo, beForData)
      else isChangeData = dataInfo
      this.dataList = isChangeData
    },
    judgeChange (data, flag) {
      if (!flag) return false
      for (let j of this.dataList) {
        if (j.change) {
          if (j.managerName != j.change.managerName) return true
          if (j.investStrategy != j.change.investStrategy) return true
          if (j.phone != j.change.phone) return true
          if (j.email != j.change.email) return true
        }
      }
    }
  }
}
</script>
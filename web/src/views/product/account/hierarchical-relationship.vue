<template>
  <div>
    <el-table :data="table_data" border>
      <el-table-column label="序号" type="index" header-align="center" align="center" width="50"></el-table-column>
      <el-table-column label="分级名称" header-align="center" align="center" prop="fundNameGrade"></el-table-column>
      <el-table-column label="分级代码" header-align="center" align="center" prop="fundCodeGrade"></el-table-column>
      <el-table-column label="额分类型" header-align="center" align="center" prop="shareType"></el-table-column>
      <el-table-column label="杠杆比例（1%到0.01）  " header-align="center" align="center" prop="leverageRatio"></el-table-column>
    </el-table>
  </div>
</template>
<script>
export default {
  data () {
    return {
      table_data: []
    }
  },
  methods: {
    init (data) {
      console.log(data)
      let isGrade = data.fundInfo.isGrade
      if (isGrade) {
        this.$nextTick(() => {
         this.table_data = data.fundGrades
       })
      } else {
        this.table_data = []
      }
      
    }
  }
}
</script>
<style scoped>

</style>

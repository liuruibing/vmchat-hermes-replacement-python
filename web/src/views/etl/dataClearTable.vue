<template>
  <div class="dataClearTable ddportal-ui">
    <el-table
      ref="Table"
      :data="tableData"
      border
      stripe
      @sort-change="handleSortChange"
      v-loading="tableLoading"
      style="width: 100%"
    >
      <el-table-column
        type="selection"
        width="35"
        align="center"
      ></el-table-column>

      <el-table-column
        prop="fId"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="序号"
        min-width="70"
        type="index"
        header-align="center"
      >
      </el-table-column>

      <el-table-column
        prop="agencyName"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="机构名称"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.agencyName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fileType"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="清洗项"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fileType | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fileName"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="清洗类型"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fileName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fileName"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="清洗状态"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fileName | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="fileName"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="开始时间"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fileName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="fileName"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="结束时间"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.fileName | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column label="操作" fixed="right" min-width="160" align="center">
        <template slot-scope="scope">
          <el-button type="primary" size="small" @click="beginRun(scope.row)">重新执行</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
export default {
  components:{
    Pagination
  },
  data(){
    return{
      tableData:[],
      tableLoading:false,
    }
  },
  methods:{
    handleSelectionChange(){},
    handleSortChange(){},
    beginRun(){}
  }
};
</script>

<style>
</style>
<template>
  <div class="early-warning">
    <el-card>
      <div slot="header" class="clearfix">
        <el-row class="card-header" type="flex" justify="space-around">
          <el-col :span="4">
            <span class="title-name">
              <span>尽调管理</span>
            </span>
          </el-col>
          <el-col :span="20" style="text-align: right">

            <span class="link-more" @click="handleMoreClick">更多 ></span>
          </el-col>
        </el-row>
      </div>
      <div class="content">
        <vxe-table
          ref="fundTable"
          :data="activeTableMap[active].tableData"
          border="inner"
          height="288px"
          resizable
          auto-resize
          show-overflow>
          <vxe-table-column
            v-for="col in activeTableMap[active].columns"
            :key="col.field"
            :field="col.field"
            :title="col.title"
            :min-width="col.minWidth"
            :header-align="col.headerAlign"
            :align="col.align"
          >
            <template slot-scope="scope">
              <span v-if="active === 'fund' && col.field === 'YAXISDATA4'">
                <span style="color: #70ad47"
                      v-if="scope.row[col.field] === '处理完毕'">{{ scope.row[col.field] | noDataFilter }}</span>
                <span style="color: red"
                      v-else-if="scope.row[col.field] === '待处理'">{{ scope.row[col.field] | noDataFilter }}</span>
                <span style="color: #409eff"
                      v-else-if="scope.row[col.field] === '待提交'">{{ scope.row[col.field] | noDataFilter }}</span>
                <span v-else>{{ scope.row[col.field] | noDataFilter }}</span>
              </span>
              <span v-else>{{ scope.row[col.field] | noDataFilter }}</span>
            </template>
          </vxe-table-column>
        </vxe-table>
      </div>
    </el-card>
  </div>
</template>

<script>
import commonApi from '@/api/common'

export default {
  name: 'PublicRequest',
  data() {
    return {
      active: 'fund',
      activeTableMap: {
        fund: {
          columns: [
            {
              field: 'YAXISDATA1',
              title: '机构名称',
              minWidth: '120',
              headerAlign: 'center',
              align: 'center'
            },
            {
              field: 'YAXISDATA2',
              title: '需求说明',
              minWidth: '90',
              headerAlign: 'center',
              align: 'left'
            },
            {
              field: 'YAXISDATA3',
              title: '申请日期',
              minWidth: '100',
              headerAlign: 'center',
              align: 'center'
            },
            {
              field: 'YAXISDATA4',
              title: '处理状态',
              minWidth: '100',
              headerAlign: 'center',
              align: 'center'
            },
            {
              field: 'YAXISDATA5',
              title: '处理结果',
              minWidth: '90',
              headerAlign: 'center',
              align: 'center'
            }
          ],
          tableData: []
        },
      }
    }
  },
  methods: {
    handleMoreClick() {
      this.$router.push({
        path: '/tzgl/jdsq/jdsq'
      })
    },
    initData() {
      this.getPublicRequestFund()
    },

    getPublicRequestFund() {
      const params = {}
      params.indexCode = 'b29fddf9-8694-4906-9db2-f9cf1f2a89fd'
      commonApi
        .getDataBysqlCode(params)
        .then((res) => {
          const { status, data } = res.data
          if (status === 0) {
            this.activeTableMap['fund'].tableData = data || []
          } else {
            this.activeTableMap['fund'].tableData = []
          }
        })
        .catch((err) => {
          this.activeTableMap['fund'].tableData = []
        })
    },
  }
}
</script>

<style lang="scss" scoped>
@import url('../../style/index.scss');

.toogle-tab {
  //margin-left: 230px;
}
</style>

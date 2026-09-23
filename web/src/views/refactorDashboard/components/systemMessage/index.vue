<template>
  <div class="sys-message">
    <el-card>
      <div slot="header" class="clearfix">
        <el-row class="card-header" type="flex" justify="space-around">
          <el-col :span="6">
              <span class="title-name">
                <span>系统消息</span>
              </span>
          </el-col>
          <el-col :span="18" style="text-align: right">
<!--              <span class="toogle-tab">
              <span v-for="tab in activeTabs" :key="tab.key" class="tab-item"
                    :class="tab.key === active ? 'tab-item-active ' : ''" @click="toogleActive(tab.key)">
                {{ tab.name }}
              </span>
            </span>-->
            <span class="link-more" @click="jumpToPage" v-if="active == 'demand'">More ></span>
          </el-col>
        </el-row>
      </div>
      <div class="content">
        <vxe-table
          ref="fundTable"
          :data="activeTableMap[active].tableData"
          height="288px"
          border="inner"
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
              <span v-if="col.field === 'VC_FUNDNAME' || col.field === 'YAXISDATA1'" style="padding-left: 10px;">
                {{ scope.row[col.field] | noDataFilter }}
              </span>
              <span v-else-if="active === 'demand' && col.field === 'VC_STATUS'">
                <span style="color: #148a0c"
                      v-if="scope.row[col.field] === '处理完毕'">{{ scope.row[col.field] | noDataFilter }}</span>
                <span style="color: #0f65dd"
                      v-else-if="scope.row[col.field] === '待提交'">{{ scope.row[col.field] | noDataFilter }}</span>
                <span style="color: #e98900"
                      v-else-if="scope.row[col.field] === '待处理'">{{ scope.row[col.field] | noDataFilter }}</span>
                <span v-else>{{ scope.row[col.field] | noDataFilter }}</span>
              </span>
              <span v-else-if="active === 'demand' && col.field === 'VC_RESULT'">
                <span>{{
                    scope.row[col.field] | noDataFilter
                  }}</span>
              </span>
              <span v-else-if="active === 'data' && col.field === 'YAXISDATA3'">
                <span style="color: #70ad47"
                      v-if="scope.row[col.field] === '处理完成'">{{ scope.row[col.field] | noDataFilter }}</span>
                <span style="color: red"
                      v-else-if="scope.row[col.field] === '待处理'">{{ scope.row[col.field] | noDataFilter }}</span>
                <span style="color: #409eff"
                      v-else-if="scope.row[col.field] === '处理中'">{{ scope.row[col.field] | noDataFilter }}</span>
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
  name: 'SysMessage',
  data() {
    return {
      active: 'data',
      activeTabs: [
        {key: 'demand', name: '需求互动'},
        {key: 'data', name: '数据授权'}
      ],
      activeTableMap: {
        demand: {
          columns: [
            {
              field: 'VC_FUNDNAME',
              title: '产品名称',
              minWidth: '130',
              headerAlign: 'center',
              align: 'left'
            },
            {
              field: 'VC_APPNAME',
              title: '需求标题',
              minWidth: '100',
              headerAlign: 'center',
              align: 'left'
            },
            {
              field: 'D_DATE',
              title: '申请日期',
              minWidth: '100',
              headerAlign: 'center',
              align: 'center'
            },
            {
              field: 'VC_STATUS',
              title: '处理状态',
              minWidth: '100',
              headerAlign: 'center',
              align: 'center'
            },
            {
              field: 'VC_RESULT',
              title: '处理结果',
              minWidth: '100',
              headerAlign: 'center',
              align: 'center'
            }
          ],
          tableData: [],
        },
        data: {
          columns: [
            {
              field: 'YAXISDATA1',
              title: '产品名称',
              minWidth: '130',
              headerAlign: 'center',
              align: 'left'
            },
            {
              field: 'YAXISDATA2',
              title: '申请权限等级',
              minWidth: '140',
              headerAlign: 'center',
              align: 'left'
            },
            {
              field: 'YAXISDATA3',
              title: '处理状态',
              minWidth: '100',
              headerAlign: 'center',
              align: 'center'
            },
            {
              field: 'YAXISDATA4',
              title: '已拥有权限等级',
              minWidth: '140',
              headerAlign: 'center',
              align: 'left'
            }
          ],
          tableData: []
        }
      }
    }
  },
  methods: {
    initData() {
      //this.getSysDemandData()
      this.getSysData()
    },
    toogleActive(val) {
      this.active = val
    },
    getSysDemandData() {
      const params = {
        indexCode: '9ece77a4-f4df-4dcc-afb9-27b822b06e5b'
      }
      commonApi.getDataBysqlCode(params).then((res) => {
        const {status, data} = res.data
        if (status === 0) {
          this.activeTableMap['demand'].tableData = data
        }
      })
    },
    getSysData() {
      const params = {
        indexCode: 'ec596f08-ad56-4fef-ab56-b7dea4f4498a'
      }
      commonApi.getDataBysqlCode(params).then((res) => {
        const {status, data} = res.data
        if (status === 0) {
          this.activeTableMap['data'].tableData = data
        }
      })
    },
    jumpToPage() {
      if (this.active === 'demand') {
        this.$store.commit('SET_FROMPAGEJUMP', true)
        this.$router.push({
          path: '/xqhd/gxhxqgl',
          query: {
            path: 'dashboard'
          }
        })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
@import url('../../style/index.scss');

.toogle-tab {
  //margin-left: 230px;
}
</style>

<template>
  <div class="early-warning">
    <el-card>
      <div slot="header" class="clearfix">
        <el-row class="card-header" type="flex" justify="space-around">
          <el-col :span="4">
            <span class="title-name">
              <span>投后预警</span>
            </span>
          </el-col>
          <el-col :span="20" style="text-align: right">
            <span class="toogle-tab">
              <span
                v-for="tab in activeTabs"
                :key="tab.key"
                :class="tab.key === active ? 'tab-item-active ' : ''"
                class="tab-item"
                @click="toogleActive(tab.key)">
                {{ tab.name }}
              </span>
            </span>
            <span class="link-more" @click="handleMoreClick">More ></span>
          </el-col>
        </el-row>
      </div>
      <div class="content">
        <vxe-table
          ref="fundTable"
          :data="activeTableMap[active].tableData"
          border="inner"
          max-height="288px"
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
              <span>{{ scope.row[col.field] | noDataFilter }}</span>
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
  name: 'EarlyWarning',
  data() {
    return {
      active: 'fund',
      activeTabs: [
        { key: 'fund', name: '产品' },
        { key: 'manager', name: '管理人' }
      ],
      activeTableMap: {
        fund: {
          columns: [
            {
              field: 'YAXISDATA1',
              title: '预警日期',
              minWidth: '100',
              headerAlign: 'center',
              align: 'center'
            },
            {
              field: 'YAXISDATA2',
              title: '产品名称',
              minWidth: '150',
              headerAlign: 'center',
              align: 'left'
            },
            {
              field: 'YAXISDATA3',
              title: '预警类型',
              minWidth: '100',
              headerAlign: 'center',
              align: 'center'
            },
            {
              field: 'YAXISDATA4',
              title: '预警内容',
              minWidth: '150',
              headerAlign: 'center',
              align: 'left'
            }
          ],
          tableData: []
        },
        manager: {
          columns: [
            {
              field: 'YAXISDATA1',
              title: '预警日期',
              minWidth: '100',
              headerAlign: 'center',
              align: 'center'
            },
            {
              field: 'YAXISDATA2',
              title: '管理人名称',
              minWidth: '150',
              headerAlign: 'center',
              align: 'left'
            },
            {
              field: 'YAXISDATA3',
              title: '预警类型',
              minWidth: '100',
              headerAlign: 'center',
              align: 'center'
            },
            {
              field: 'YAXISDATA4',
              title: '预警内容',
              minWidth: '150',
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
    /**
    * @Description: 投后预警 more按钮点击处理函数
    * @author Liu Rui Bing
    * @date 2024/7/22
    */
    handleMoreClick() {
      this.$router.push({
        path: '/thgl/thyj/yjjgcx'
      })
    },
    initData() {
      this.getEarlyWarningFund()
      this.getEarlyWarningManager()
    },
    toogleActive(val) {
      this.active = val
    },
    getEarlyWarningFund() {
      const params = {}
      params.indexCode = 'c1c05831-c31b-4cdf-a1df-5e2ae5d82b6c'
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
    getEarlyWarningManager() {
      const params = {}
      params.indexCode = 'b3a28bc2-dcb3-4358-9ae8-85e76329803d'
      commonApi
        .getDataBysqlCode(params)
        .then((res) => {
          const { status, data } = res.data
          if (status === 0) {
            this.activeTableMap['manager'].tableData = data || []
          } else {
            this.activeTableMap['manager'].tableData = []
          }
        })
        .catch((err) => {
          this.activeTableMap['manager'].tableData = []
        })
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

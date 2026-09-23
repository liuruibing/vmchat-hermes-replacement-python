<template>
  <div class="hotspot-manager">
    <el-card>
      <div slot="header" class="clearfix">
        <div class="card-header">
          <span class="title-name">热点经理</span>
          <span class="link-more">More ></span>
        </div>
      </div>
      <div class="content">
          <img src="@/assets/img/敬请期待.png" style="width: 100%; height: 100%;">

<!--        <vxe-table :data="tableData" border="inner" max-height="288px" resizable auto-resize show-overflow>-->
<!--          <vxe-table-column field="managerName" title="经理名称" min-width="100" header-align="center" align="center">-->
<!--            <template slot-scope="scope">-->
<!--              <span>{{ scope.row.managerName | noDataFilter }}</span>-->
<!--            </template>-->
<!--          </vxe-table-column>-->
<!--          <vxe-table-column field="sixMonth" title="近六月走势" min-width="100" align="center" header-align="center">-->
<!--            <template slot-scope="scope">-->
<!--              <span>{{ scope.row.sixMonth | noDataFilter }}</span>-->
<!--            </template>-->
<!--          </vxe-table-column>-->
<!--          <vxe-table-column field="fundNum" title="入选基金数" min-width="100" header-align="center" align="center">-->
<!--            <template slot-scope="scope">-->
<!--              <span>{{ scope.row.fundNum | noDataFilter }}</span>-->
<!--            </template>-->
<!--          </vxe-table-column>-->
<!--          <vxe-table-column field="yield" title="今年收益" min-width="100" header-align="center" align="right">-->
<!--            <template slot-scope="scope">-->
<!--              <span>{{ scope.row.yield | noDataFilter }}</span>-->
<!--            </template>-->
<!--          </vxe-table-column>-->
<!--        </vxe-table>-->
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'HotspotManager',
  data() {
    return {
      tableData: [
        {
          managerName: '张晴',
          sixMonth: '',
          fundNum: '8',
          yield: '6.16%'
        },
        {
          managerName: '李弈庆',
          sixMonth: '',
          fundNum: '3',
          yield: '16.10%'
        },
        {
          managerName: '刘美',
          sixMonth: '',
          fundNum: '6',
          yield: '7.55%'
        },
        {
          managerName: '张舒婷',
          sixMonth: '',
          fundNum: '6',
          yield: '16.67%'
        },
        {
          managerName: '赵晶晶',
          sixMonth: '',
          fundNum: '2',
          yield: '3.40%'
        }
      ]
    }
  },
  methods: {
    initData() {}
  }
}
</script>

<style lang="scss" scoped>
@import url('../../style/index.scss');

.hotspot-manager {
}
</style>

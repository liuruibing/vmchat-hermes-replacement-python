<template>
  <div class="manager-info">
    <div class="chart-content" @mousedown.stop="move">
      <myChart id="glrxxtree" ref="glrxxtree" :options="chartOptions" resize-dom="cmbfof" class="echarts_box" />
      <tree-item-no-line :tree-data="line2Data"></tree-item-no-line>
      <tree-item-no-line :tree-data="line3Data"></tree-item-no-line>
      <tree-item-business :tree-data="line4Data"></tree-item-business>
      <tree-item-business :tree-data="line5Data"></tree-item-business>
      <tree-item-business :tree-data="line6Data"></tree-item-business>
    </div>
  </div>
</template>
<script>
import myChart from '@/components/Echarts'
import TreeItem from './manager-info-core/tree-item'
import TreeItemNoLine from './manager-info-core/tree-item-no-line'
import TreeItemBusiness from './manager-info-core/tree-item-business'
export default {
  name: 'ManagerInfo',
  components: {
    TreeItem,
    TreeItemNoLine,
    TreeItemBusiness,
    myChart
  },
  props: {
    managerInfo: {
      type: Object,
      default: () => {}
    }
  },
  watch: {
    managerInfo: {
      handler(val) {
        // 组装行数据
        this.splitManagerInfo(val)
      }
    },
    deep: true
  },
  mounted() {
    this.chartInit()
  },
  data() {
    return {
      treeData: [
        {
          id: 0,
          name: '深圳市安鹏股权投资基金管理有限公司',
          label: {
            position: 0,
            backgroundColor: '#0F65DD',
            color: '#fff',
            borderRadius: 5,
            align: 'center',
            fontSize: 16,
            padding: [15, 30]
          },
          children: [
            {
              name: '成立日期',
              value: '-'
            },
            {
              name: '注册资本',
              value: '-'
            },
            {
              name: '实缴资本',
              value: '-'
            },
            {
              name: '注册城市',
              value: '-'
            },
            {
              name: '办公城市',
              value: '-'
            },
            {
              name: '统一社会信用代码',
              value: '-'
            },
            {
              name: '组织机构代码',
              value: '-'
            }
          ]
        }
      ],
      chartOptions: {},
      line2Data: [
        {
          name: '备案编码',
          value: '-'
        },
        {
          name: '备案状态',
          value: '-'
        },
        {
          name: '备案日期',
          value: '-'
        },
        {
          name: '公司状态',
          value: '-'
        },
        {
          name: '公司类型',
          value: '-'
        },
        {
          name: '企业性质',
          value: '-'
        },
        {
          name: '公司网址',
          value: '-'
        }
      ],
      line3Data: [
        {
          name: '是否会员',
          value: '-'
        },
        {
          name: '入会时间',
          value: '-'
        },
        {
          name: '员工数量',
          value: '-'
        },
        {
          name: '业务类型',
          value: '-'
        },
        {
          name: '基金数量',
          value: '-'
        },
        {
          name: '公司资产规模',
          value: '-'
        },
        {
          name: '管理基金主要类别',
          value: '-'
        }
      ],
      line4Data: [
        {
          name: '公司注册地址',
          value: '-'
        },
        {
          name: '公司办公地址',
          value: '-'
        }
      ],
      line5Data: [
        {
          name: '投资理念',
          value: '-'
        },
        {
          name: '诚信信息',
          value: '-'
        }
      ],
      line6Data: [
        {
          name: '公司简介',
          value: '-'
        }
      ]
    }
  },
  methods: {
    // 拖拽移动
    move(e) {
      const odiv = e.currentTarget // 获取元素

      // 算出鼠标相对元素的位置
      const disX = e.clientX - odiv.offsetLeft
      const disY = e.clientY - odiv.offsetTop
      document.onmousemove = e => {
        // 鼠标按下并移动的事件
        // 用鼠标的位置减去鼠标相对元素的位置，得到元素的位置
        const left = e.clientX - disX
        const top = e.clientY - disY

        // 移动当前元素
        odiv.style.left = left + 'px'
        odiv.style.top = top + 'px'
      }
      document.onmouseup = () => {
        document.onmousemove = null
        document.onmouseup = null
      }
    },
    chartInit() {
      const node = {
        backgroundColor: '#f8fcff',
        color: '#000',
        borderColor: '#eaebed',
        align: 'center',
        borderWidth: 1,
        fontSize: 14,
        width: document.documentElement.clientWidth < 1900 ? 142 : 202,
        verticalAlign: 'middle',
        borderRadius: 10,
        padding: [35, 0],
        overflow: 'breakAll'
      }
      this.treeData[0].children.forEach(item => {
        item['label'] = node
      })
      this.chartOptions = {
        series: [
          {
            type: 'tree',
            orient: 'TB',
            data: this.treeData,
            width: document.documentElement.clientWidth < 1900 ? '92.8%' : '94.1%',
            height: '67%',
            left: document.documentElement.clientWidth < 1900 ? '3.5%' : '3%',
            symbolSize: 1,
            initialTreeDepth: 1, // 初始展开的层级(深度)
            label: {
              normal: {
                verticalAlign: 'middle',
                align: 'center',
                formatter: function(params) {
                  if (params.dataIndex === 1) {
                    return params.data.name
                  } else {
                    return params.data.name + '\n\n' + params.data.value
                  }
                },
                rich: {}
              },
              fontFamily: 'Microsoft YaHei',
              fontSize: 14
            },
            lineStyle: {
              color: '#dfecff'
            },
            animation: false
          }
        ]
      }
    },
    splitManagerInfo(managerInfo) {
      // echarts data 数据
      this.treeData[0].name = managerInfo.COMPANY_NAME || '-'
      this.treeData[0].children[0].value = managerInfo.ESTABLISH_DATE || '-'
      this.treeData[0].children[1].value = managerInfo.CAPITAL ? managerInfo.CAPITAL + '万元' : '-'
      this.treeData[0].children[2].value = managerInfo.PAID_CAPITAL ? managerInfo.PAID_CAPITAL + '万元' : '-'
      this.treeData[0].children[3].value = managerInfo.REG_CITY || '-'
      this.treeData[0].children[4].value = managerInfo.CITY || '-'
      this.treeData[0].children[5].value = managerInfo.UICC || '-'
      this.treeData[0].children[6].value = managerInfo.ORG_CODE || '-'

      // line2Data数据
      this.line2Data[0].value = managerInfo.REG_CODE || '-'
      this.line2Data[1].value = managerInfo.REG_STATUS || '-'
      this.line2Data[2].value = managerInfo.D_REG_TIME || '-'
      this.line2Data[3].value = managerInfo.COMPANY_STATUS || '-'
      this.line2Data[4].value = managerInfo.COMPANY_TYPE || '-'
      this.line2Data[5].value = managerInfo.PROPERTIES || '-'

      if (managerInfo.ORG_WEB) {
        if (managerInfo.ORG_WEB.indexOf('https://') == -1 && managerInfo.ORG_WEB.indexOf('http://') == -1) {
          managerInfo.ORG_WEB = 'http://' + managerInfo.ORG_WEB
        }
      }

      this.line2Data[6].value = managerInfo.ORG_WEB || '-'

      // line3Data数据
      this.line3Data[0].value = managerInfo.IS_MEMBER || '-'
      this.line3Data[1].value = managerInfo.MEMBER_JOIN_DATE || '-'
      this.line3Data[2].value = managerInfo.STAFF_NUM || '-'
      this.line3Data[3].value = managerInfo.YW_TYPE || '-'
      this.line3Data[4].value = managerInfo.FUND_NUM || '-'
      this.line3Data[5].value = managerInfo.TOTAL_ASSET_SIZE || '-'
      this.line3Data[6].value = managerInfo.MANAGE_TYPE || '-'

      // line4Data数据
      this.line4Data[0].value = managerInfo.COMPANY_ADDRESS || '-'
      this.line4Data[1].value = managerInfo.COMPANY_ADDRESS2 || '-'

      // line5Data数据
      this.line5Data[0].value = managerInfo.INVESTMENT_IDEA || '-'
      this.line5Data[1].value = managerInfo.INTEGRITY_INFO || '-'

      // line6Data数据
      this.line6Data[0].value = managerInfo.ORG_PROFILE || '-'
    }
  }
}
</script>
<style lang="scss" scoped>
.manager-info {
  height: 2000px;
  overflow: auto;
  position: relative;
  margin-bottom: 20px;
  .chart-content {
    width: 100%;
    background: #fff;
    position: absolute;
    top: 0;
    left: 0;

    .echarts_box {
      margin-top: 20px;
    }
  }
}
</style>

<!--
 * @Description:
 * @Author:
 * @Date: 2023-03-04 17:55:58
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2023-03-04 18:13:38
-->
<template>
  <div id="standard-table">
    <vxe-table
      v-loading="tableLoading"
      ref="vxetable"
      :data="tableData"
      id="standard-table"
      :edit-config="{ trigger: 'click', mode: 'cell', showIcon: false, activeMethod: handleActiveMethod }"
      stripe
      :cell-style="{ height: '50px' }"
      style="width: 100%"
    >
      <vxe-table-column field="VC_FUNDCODE" header-align="center" title="产品代码"></vxe-table-column>
      <vxe-table-column field="VC_FUNDNAME" header-align="center" show-overflow title="产品名称"></vxe-table-column>
      <vxe-table-column align="center" field="D_CREATE_DATE" header-align="center" title="成立日期"></vxe-table-column>
      <vxe-table-column
        :edit-render="{
          name: '$input',
          events: { blur: handleEvent }
        }"
        align="right"
        field="weight"
        header-align="center"
        title="权重"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.VC_FUNDNAME != '合计' && scope.row.VC_FUNDNAME != '现金'" class="vxe-cell-config">{{ scope.row.weight | numberToFixedStrSelf }}</span>
          <span v-else>{{ scope.row.weight | numberToFixedStrSelf }}</span>
        </template>
      </vxe-table-column>
      <vxe-table-column
        :edit-render="{
          name: '$input',
          props: { type: 'float', digits: 2, controls: false },
          events: { blur: handleEvent }
        }"
        align="right"
        field="marketValue"
        header-align="center"
        title="持仓市值（万元）"
      >
        <template slot-scope="scope">
          <span v-if="scope.row.VC_FUNDNAME != '合计' && scope.row.VC_FUNDNAME != '现金'" class="vxe-cell-config">{{ scope.row.marketValue | moneyYuan }}</span>
          <span v-else>{{ scope.row.marketValue | moneyYuan }}</span>
        </template>
      </vxe-table-column>
      <vxe-table-column align="center" header-align="center" title="操作" width="150">
        <template slot-scope="scope">
          <span class="table-operation">
            <el-button type="info" plain size="small" v-if="scope.row.VC_FUNDNAME != '合计' && scope.row.VC_FUNDNAME != '现金'" @click="handleMeritPay(scope.row)">
              业绩报酬
            </el-button>
          </span>
        </template>
      </vxe-table-column>
    </vxe-table>
    <div style="padding: 4px; color: #333">备注:假设调仓行为在当日盘前完成。现金权重为持仓产品不足100%部分，且不计算收益。</div>
    <div style="text-align: center; padding: 20px 0" class="standard-form">
      <el-button v-if="active === 2" size="small" type="primary" @click="$emit('onSubmit')">保存方案并进入回测分析</el-button>
      <el-button v-else type="primary" size="small" @click="$emit('onSubmit')">保存修改</el-button>
    </div>
    <el-dialog
      title="业绩报酬"
      :visible.sync="payVisible"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :destroy-on-close="true"
      custom-class="payDialog"
      @close="close"
    >
      <merit-pay v-if="payVisible" :curFundRow="curFundRow" :subCombineCode="subCombineCode" @closeDialog="close"></merit-pay>
    </el-dialog>
  </div>
</template>

<script>
import MeritPay from '@/components/merit-pay/index'
export default {
  name: '',
  components: { MeritPay },
  filters: {
    numberToFixedStrSelf(val) {
      // console.log(val, 'val')
      if ((val == '' || val == undefined || val == null) && val !== 0) {
        return '-'
      } else {
        return Number(val).toFixed(2) + '%'
      }
    }
  },
  props: {
    subCombineCode: {
      type: String,
      default: ''
    },
    active: {
      default: 2
    },
    selectList: {
      type: Array,
      required: true,
      default: () => []
    }
  },
  data() {
    return {
      curFundRow: {},
      payVisible: false,
      tableLoading: false,
      tableData: []
      // tableData: [
      //   {
      //     fundCode: 'S57896',
      //     fundName: '华夏大盘精选证券投资基金',
      //     creadDate: '2019-09-23',
      //     tcqsz: '448.8',
      //     tcqqz: '4.08%',
      //     tchsz: '1000',
      //     tchqz: '5.71%',
      //     tcje: '408.00'
      //   },
      //   {
      //     fundCode: 'XT2674',
      //     fundName: '易方达天天理财货币市场基金R',
      //     creadDate: '2022-06-30',
      //     tcqsz: '10001.2',
      //     tcqqz: '90.92%',
      //     tchsz: '11000',
      //     tchqz: '62.86%',
      //     tcje: '9092.00'
      //   },
      //   {
      //     fundCode: 'S12375',
      //     fundName: '易方达现金增利货币B',
      //     creadDate: '2020-03-27',
      //     tcqsz: '0',
      //     tcqqz: '5.00%',
      //     tchsz: '5000',
      //     tchqz: '28.57%',
      //     tcje: '500'
      //   },
      //   {
      //     fundCode: '',
      //     VC_FUNDNAME: '现金',
      //     creadDate: '',
      //     tcqsz: '500',
      //     tcqqz: '100%',
      //     tchsz: '100',
      //     tchqz: '2.86%',
      //     tcje: '10000',
      //     flag: true
      //   },
      //   {
      //     fundCode: '',
      //     VC_FUNDNAME: '合计',
      //     creadDate: '',
      //     tcqsz: '10950',
      //     tcqqz: '',
      //     tchsz: '17500',
      //     tchqz: '100.00%',
      //     tcje: '',
      //     flag: true
      //   }
      // ]
    }
  },
  watch: {
    selectList: {
      handler(val) {
        if (val.length < 0) {
          return
        }
        const tempTableData = _.cloneDeep(val)
        tempTableData.forEach((item) => {
          item.weight = 0
          item.marketValue = 0
          item.fundType = item.VC_FLAG
        })
        this.tableData = tempTableData
        const tableLength = this.tableData.length
        this.$set(this.tableData, tableLength, {
          VC_FUNDNAME: '现金',
          weight: 100,
          marketValue: this.$parent.price || 0
        })
        this.$set(this.tableData, tableLength + 1, {
          VC_FUNDNAME: '合计',
          weight: 100,
          marketValue: this.$parent.price || 0
        })
      },
      deep: true
    }
  },
  mounted() {},
  methods: {
    handleMeritPay(row) {
      this.curFundRow = JSON.parse(JSON.stringify(row))
      this.payVisible = true
    },
    close() {
      this.payVisible = false
    },

    handleActiveMethod({ row, rowIndex, column, columnIndex }) {
      if (row.VC_FUNDNAME == '现金' || row.VC_FUNDNAME == '合计') {
        return false
      } else {
        return true
      }
    },

    handleAllEvent(row, column, event, type) {
      // 处理编辑器组件的事件
      console.log('事件触发', type, row[column.property], event.target.value)
    },
    // {row,rowIndex,$rowIndex,column,columnIndex,$columnIndex}
    handleEvent({ row, rowIndex, $rowIndex, column, columnIndex, $columnIndex }) {
      if (row.VC_FUNDNAME == '合计') {
        row.weight = 100
        row.marketValue = Number(this.$parent.price)
        return
      } else if (row.VC_FUNDNAME == '现金') {
        return
        // if (columnIndex == 3) {
        //   if (Number(row.weight) < 0) {
        //     this.$message.closeAll()
        //     this.$message.warning('输入必须大于0')
        //     row.marketValue = 0
        //     row.weight = 0
        //     return
        //   }
        // }
        // if (columnIndex == 4) {
        //   if (Number(row.marketValue) < 0) {
        //     this.$message.closeAll()
        //     this.$message.warning('输入必须大于0')
        //     row.marketValue = 0
        //     row.weight = 0
        //     return
        //   }
        // }
        // let sumWeight = 0
        // let sumMarketValue = 0
        // for (let i = 0; i < this.tableData.length - 2; i++) {
        //   const temp = this.tableData[i]
        //   sumWeight += Number(temp.weight)
        //   sumMarketValue += Number(temp.marketValue)
        // }
        // if (Number(sumWeight) + Number(row.weight) > 100) {
        //   this.$message.closeAll()
        //   this.$message.warning('权重不能大于100')
        //   row.weight = 100 - Number(sumWeight)
        //   row.marketValue = Number(this.$parent.price) - Number(sumMarketValue)
        //   return
        // }
        // if ((Number(sumMarketValue) + Number(row.marketValue)) > Number(this.$parent.price)) {
        //   this.$message.closeAll()
        //   this.$message.warning('超出初始金额')
        //   row.weight = 100 - Number(sumWeight)
        //   row.marketValue = Number(this.$parent.price) - Number(sumMarketValue)
        //   return
        // }
        // if (columnIndex == 3) {
        //   // 权重
        //   row.marketValue = Number(this.$parent.price) * Number(row.weight) / 100
        // }
        // if (columnIndex == 4) {
        //   // 市值
        //   row.weight = Number(row.marketValue) / Number(this.$parent.price) * 100
        // }
      } else {
        if (columnIndex == 4) {
          if (Number(row.marketValue) < 0) {
            this.$message.closeAll()
            this.$message({
              type: 'warning',
              message: '输入必须大于0',
              customClass: 'message-warning'
            })
            row.marketValue = 0
            row.weight = 0
            return
          }
          // 累加所有的产品市值
          let sum = 0
          for (let i = 0; i < this.tableData.length - 2; i++) {
            sum += Number(this.tableData[i].marketValue)
          }
          if (sum > Number(this.$parent.price)) {
            this.$message.closeAll()
            this.$message({
              type: 'warning',
              message: '超出初始金额',
              customClass: 'message-warning'
            })
            row.marketValue = 0
            row.weight = 0
            return
          } else {
            // 输入 合法有效，需要重置比例 和现金
            let sumWeight = 0
            let sumMarketValue = 0

            for (let i = 0; i < this.tableData.length - 2; i++) {
              const temp = this.tableData[i]
              temp.weight = (Number(temp.marketValue) / Number(this.$parent.price)) * 100
              sumWeight += Number(temp.weight)
              sumMarketValue += Number(temp.marketValue)
            }
            this.tableData[this.tableData.length - 2].weight = 100 - sumWeight
            this.tableData[this.tableData.length - 2].marketValue = Number(this.$parent.price) - sumMarketValue
          }
        } else if (columnIndex == 3) {
          if (Number(row.weight) < 0) {
            this.$message.closeAll()
            this.$message({
              type: 'warning',
              message: '输入必须大于0',
              customClass: 'message-warning'
            })
            row.marketValue = 0
            row.weight = 0
            return
          }
          // 累加所有的产品市值
          let sum = 0
          for (let i = 0; i < this.tableData.length - 2; i++) {
            sum += Number(this.tableData[i].weight)
          }
          if (sum > 100) {
            this.$message.closeAll()
            this.$message({
              type: 'warning',
              message: '权重不能大于100',
              customClass: 'message-warning'
            })
            row.weight = 0
            row.marketValue = 0
            return
          } else {
            // 输入 合法有效，需要重置比例 和现金
            let sumWeight = 0
            let sumMarketValue = 0
            for (let i = 0; i < this.tableData.length - 2; i++) {
              const temp = this.tableData[i]
              temp.marketValue = Number(this.$parent.price) * (Number(temp.weight) / 100)
              sumWeight += Number(temp.weight)
              sumMarketValue += Number(temp.marketValue)
            }
            this.tableData[this.tableData.length - 2].weight = 100 - Number(sumWeight)
            this.tableData[this.tableData.length - 2].marketValue = Number(this.$parent.price) - Number(sumMarketValue)
          }
        }
      }
    },
    initTableBySelectChange(tableArray) {
      this.tableData = []
      for (let i = 0; i < tableArray.length; i++) {
        this.$set(this.tableData, i, tableArray[i])
      }
    }
  }
}
</script>
<style lang="scss" scoped>
.operate-btn {
  ::v-deep .el-button.el-button--small {
    margin-left: 16px !important;
  }
  ::v-deep .el-button.el-button--info {
    font-weight: bold;
  }
  ::v-deep .el-button.el-button--info:hover {
    font-weight: bold;
  }
}
.vxe-cell-config {
  display: inline-block;
  width: 100%;
  height: 34px;
  border-radius: 4px;
  outline: 0;
  padding: 0 0.6em;
  color: #333;
  border: 1px solid #dcdfe6;
  background-color: #fff;
  -webkit-box-shadow: none;
  box-shadow: none;
  line-height: 34px;
}
::v-deep .payDialog.el-dialog {
  width: 55% !important;
}
::v-deep .payDialog .el-dialog__title {
  color: #0F65DD !important;
}
::v-deep .vxe-table .vxe-body--row.row--stripe {
  background-color: #f9fafe !important;
}
</style>

<template>
  <div class="tiaocangPage">
    <!-- 调仓 -->
    <el-container class="container">
      <el-aside class="Aside" width="300px">
        <div class="standard-form">
          <el-date-picker v-model="dDate" :picker-options="setDisabled" placeholder="选择日期" size="small" type="date" value-format="yyyy-MM-dd"></el-date-picker>
          <el-button :loading="insertBtnLoading" size="small" type="primary" @click="handleInsertNode">新增</el-button>
        </div>
        <div class="dateList">
          <p v-for="item in dateList" :key="item.fId" class="dateItem" @click="handleNodeChange(item)">
            <span>
              <i class="el-icon-date"></i>
              <span :class="item.checked ? 'checked' : ''">{{ item.ddate }}</span>
            </span>
            <span>
              <i class="el-icon-close" style="color: #e03d3e; cursor: pointer" @click.stop="handleRemoveNode(item)"></i>
            </span>
          </p>
        </div>
      </el-aside>
      <el-main class="Main">
        <ToolBarSlot>
          <template slot="left">
<!--            <el-button size="small" plain type="info" @click="handleAddFund">添加产品</el-button>-->
            <ProductSelectInputMultiple
              v-model="selectedProducts"
              placeholder="请选择产品"
              :input-width="'260px'"
              @select="handleProductSelect"
              @clear="handleProductClear"
            />
            <el-button size="small" plain type="info" @click="handleSaveTable">保存</el-button>
          </template>
        </ToolBarSlot>
        <div id="standard-table">
          <vxe-table
            ref="vxetable"
            v-loading="tableLoading"
            :data="tableData"
            :edit-config="{ trigger: 'click', mode: 'cell', showIcon: false }"
            :footer-method="footerMethod"
            show-footer
            stripe
            style="width: 100%"
          >
            <vxe-column title="序号" type="seq" width="60"></vxe-column>
            <vxe-table-column field="fundCode" header-align="center" show-overflow title="产品代码" min-width="120"></vxe-table-column>
            <vxe-table-column field="fundName" header-align="center" show-overflow title="产品名称" min-width="120"></vxe-table-column>
            <vxe-table-column align="center" field="fcreateDate" header-align="center" show-overflow title="成立日期" min-width="120"></vxe-table-column>
            <vxe-table-column align="right" field="prevPrice" header-align="center" title="调仓前市值(万元)" min-width="160">
              <template slot="header" slot-scope="{ column }">
                <div>{{ column.title.slice(0, 5) }}</div>
                <span>{{ column.title.slice(5, column.title.length) }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column align="right" field="prevCostrate" header-align="center" title="调仓前权重(%)" min-width="120"></vxe-table-column>
            <vxe-table-column :edit-render="{ autofocus: '.vxe-input--inner' }" align="right" field="priceJ" header-align="center" title="调仓后市值(万元)" min-width="200">
              <template slot="header" slot-scope="{ column }">
                <div>{{ column.title.slice(0, 5) }}</div>
                <span>{{ column.title.slice(5, column.title.length) }}</span>
              </template>
              <template slot-scope="scope">
                <span :class="isFirstData ? 'table-span-disabled' : 'table-span'">{{ scope.row.priceJ | moneyYuan }}</span>
              </template>
              <template slot="edit" slot-scope="{ row, rowIndex }">
                <el-input
                  v-model="row.priceJ"
                  :disabled="isFirstData"
                  onkeyup="value=value.replace(/[^0-9.]/g,'')"
                  type="text"
                  @blur="updatePrice($event, rowIndex, 'priceJ', row)"
                ></el-input>
              </template>
            </vxe-table-column>
            <vxe-table-column :edit-render="{ autofocus: '.vxe-input--inner' }" align="right" field="costrate" header-align="center" title="调仓后权重(%)" min-width="200">
              <template slot-scope="scope">
                <span v-if="scope.row.fundName === '现金'">{{ scope.row.costrate }}</span>
                <span v-else :class="isFirstData ? 'table-span-disabled' : 'table-span'">{{ scope.row.costrate }}</span>
              </template>
              <template slot="edit" slot-scope="{ row, rowIndex }">
                <div v-if="row.fundName === '现金'" style="line-height: 0">
                  {{ row.costrate }}
                </div>
                <el-input
                  v-else
                  v-model="row.costrate"
                  :disabled="isFirstData"
                  onkeyup="value=value.replace(/[^0-9.]/g,'')"
                  type="text"
                  @blur="updateRate($event, rowIndex, 'costrate', row)"
                ></el-input>
              </template>
            </vxe-table-column>
            <vxe-table-column align="right" field="priceChg" header-align="center" title="调仓金额(万元)" min-width="120"></vxe-table-column>
            <vxe-table-column align="center" header-align="center" title="操作" width="300">
              <template slot-scope="scope">
                <span class="table-operation">
                  <el-button size="small" type="info" plain @click="handleClearData(scope.row)" v-if="scope.row.fundName != '现金'">清仓</el-button>
                  <el-button size="small" type="info" plain v-if="scope.row.fundName != '合计' && scope.row.fundName != '现金'" @click="handleMeritPay(scope.row)">
                    业绩报酬
                  </el-button>
                  <el-popconfirm
                    v-if="scope.row.fundName != '现金'"
                    ref="popconfirm"
                    class="standard-popconfirm"
                    :title="delBtnTitle"
                    confirm-button-text="确定"
                    @cancel="handleCancel"
                    @confirm="handleConfirm(scope.row)"
                  >
                    <el-button slot="reference" size="small" type="info" plain @click="handleBeforeConfirm(scope.row)">删除</el-button>
                  </el-popconfirm>
                </span>
              </template>
            </vxe-table-column>
          </vxe-table>
        </div>

        <el-row class="mt10">
          <el-col :span="18" style="text-align: left">
            <div style="padding: 20px; color: #333">
              <p>
                备注: 1. 假设调仓行为在当日盘前完成。现金权重为持仓产品不足100%部分，且不计算收益。
              </p>
              <p style="text-indent: 2.5em">
                2. 需调仓请点击左侧新增日期后再进行权重修改。
              </p>
            </div>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
    <product-selector
      :dialog-visible="productSelectorVisible"
      :select-list="selectList"
      :show-tree-key-array="showTreeKeyArray"
      :tree-data="treeData"
      default-checked-keys="zstgwb"
      multiple
      title="选择产品"
      @closedialog="productSelectorVisible = false"
      @submitdialog="handleSubmitClick"
    ></product-selector>
    <el-dialog
      title="业绩报酬"
      :visible.sync="payVisible"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :destroy-on-close="true"
      custom-class="payDialog"
      @close="close"
    >
      <merit-pay v-if="payVisible" :curFundRow="curFundRow" @closeDialog="close"></merit-pay>
    </el-dialog>
  </div>
</template>

<script>
import { deleteNodeById, getNodeList, getNodeTable, insertNode, saveEditFund } from './scripts/api'
import productSelector from '@/components/productSelector'
import commonFilter from '@/filters/common'
import MeritPay from '@/components/merit-pay/index'
import ToolBarSlot from '@/components/toolBarSlot'
import ProductSelectInputMultiple from '@/components/productSelector/ProductSelectInputMultiple'

export default {
  name: 'TiaoCang',
  components: {
    productSelector,
    MeritPay,
    ToolBarSlot,
    ProductSelectInputMultiple
  },
  data() {
    return {
      selectedProducts: [],
      insertBtnLoading: false, //控制添加按钮
      delBtnTitle: '',
      // 新增日期节点绑定
      dDate: '',
      // 调仓日期节点
      dateList: [],
      // 节点调仓详情表格
      tableData: [],
      // 表格加载状态
      tableLoading: false,
      // 当前模拟组合代码
      curCombCode: '',
      // 当前模拟组合名称
      curCombName: '',
      // 控制日期禁用项
      setDisabled: null,
      // 当前选中节点
      curDateNode: '',
      createDateNode: '', // 初始节点
      isFirstData: false,
      // 选择产品弹窗
      productSelectorVisible: false,
      // 左侧树映射
      showTreeKeyArray: ['产品列表', '我的关注', '私有产品'],
      // 产品弹窗左侧树
      treeData: [
        {
          label: '产品列表',
          id: 'zstgwb'
        },
        {
          label: '我的关注',
          id: 'wdgz',
          children: [
            {
              label: '默认分组',
              id: 'mrfz'
            },
            {
              label: '权益组',
              id: 'qyz'
            }
          ]
        },
        {
          label: '私有产品',
          code: 'sycp'
        }
      ],
      // 已选产品
      selectList: [],
      // 和值
      sumCount: 0,
      curFundRow: {},
      payVisible: false
    }
  },
  watch: {
    '$route.query.combList': {
      async handler(newVal) {
        if (this.$store.getters.fromPageJump && this.$route.query.type === 'tc') {
          if (newVal && newVal.combineCode) {
            // 动态修改tag-views dom标签
            document.querySelector('.tags-view-item.active .tag-title') &&
              (document.querySelector('.tags-view-item.active .tag-title').innerText = newVal.combineName + ' 调仓' || '调仓详情')
            this.setDatePickOptions(newVal)
            this.curCombCode = newVal.combineCode
            this.curCombName = newVal.combineName
            await this.handleFindNode(this.curCombCode)
            this.queryTableByDateNode()
          }
        }
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    handleProductSelect(selectedItems) {
      // 先校验是否有日期节点（保持原逻辑）
      if (!this.dateList || this.dateList.length === 0) {
        this.$message({
          type: 'warning',
          message: '请先创建左侧日期节点',
          customClass: 'message-warning'
        })
        this.selectedProducts = [] // 清空选择
        return
      }
      const curData = selectedItems.map(item => {
        return {
          combineCode: this.curCombCode,
          fundCode: item.VC_FUNDCODE || '-',
          fundName: item.VC_FUNDNAME || '-',
          fcreateDate: item.D_CREATE_DATE || '-',
          ddate: this.curDateNode,
          fundType: item.VC_FLAG,
          prevCostrate: 0,
          priceJ: 0,
          costrate: 0,
          prevPrice: 0,
          priceChg: 0
        }
      })

      const some = [...this.tableData]
      this.tableData.unshift(...curData)
      this.tableData.forEach(el => {
        if (!some.some(e => e.fundCode === el.fundCode)) {
          some.push(el)
        }
      })
      this.tableData = some
    },
    handleProductClear() {
      this.selectedProducts = []
    },
    handleMeritPay(row) {
      this.curFundRow = JSON.parse(JSON.stringify(row))
      this.curFundRow.VC_FUNDNAME = row.fundName
      this.payVisible = true
    },
    close() {
      this.payVisible = false
    },
    // 判断是不是初始节点
    handleJudgeIsFirstDate(row) {
      if (row && row.createDate && row.createDate == this.createDateNode) {
        return true
      }
      return false
    },
    handleBeforeConfirm(row) {
      // 执行你的逻辑判断，可以使用传递的自定义参数
      if (
        (row.prevCostrate == 0 || row.prevCostrate == undefined) &&
        (row.priceJ == 0 || row.priceJ == undefined) &&
        (row.costrate == 0 || row.costrate == undefined) &&
        (row.prevPrice == 0 || row.prevPrice == undefined)
      ) {
        this.delBtnTitle = '是否确认删除此子基金，点击确认后再删除'
      } else {
        // 取消弹出
        this.delBtnTitle = '调仓前后市值均为0时才可删除，您可对该子基金进行清仓操作。'
      }
    },
    handleConfirm(row) {
      // 执行你的逻辑判断，可以使用传递的自定义参数
      if (
        (row.prevCostrate == 0 || row.prevCostrate == undefined) &&
        (row.priceJ == 0 || row.priceJ == undefined) &&
        (row.costrate == 0 || row.costrate == undefined) &&
        (row.prevPrice == 0 || row.prevPrice == undefined)
      ) {
        // 判断市值、权重是否都为0

        const fundCode = row.fundCode
        const _index = this.tableData.findIndex(item => item.fundCode === fundCode)
        this.tableData.splice(_index, 1)
        const sum = this.sumNumValue(this.tableData, 'priceJ')
        if (Number(sum) == 0) {
          this.tableData.forEach(item => {
            item.costrate = 0
          })
        } else {
          this.tableData.forEach(item => {
            item.costrate = ((Number(item.priceJ) / Number(sum)) * 100).toFixed(2)
          })
        }
      }
    },
    handleCancel() {
      // 取消删除操作
    },

    /**
     * @description 限制日期选择器区间
     */
    setDatePickOptions(newVal) {
      this.setDisabled = {
        disabledDate(time) {
          return time.getTime() < new Date(newVal.foundDate)
        }
      }
    },
    /**
     * @description 查询左侧时间节点
     */
    handleFindNode(val) {
      return new Promise((resolve, reject) => {
        const params = {
          combineCode: val
        }
        getNodeList(params)
          .then(res => {
            if (res.data.status === 0) {
              this.dateList = res.data.data.rows || []
              if (this.dateList && this.dateList.length) {
                this.dateList.forEach(item => {
                  this.$set(item, 'checked', false)
                })
                this.dateList[0].checked = true
                this.createDateNode = this.dateList[0].ddate
                this.curDateNode = this.dateList[0].ddate
                this.curDateNodeKey = this.dateList[0].fId
                resolve()
              } else {
                this.tableData = []
              }
            }
          })
          .catch(err => {
            reject(err)
          })
      })
    },
    /**
     * @description 删除左侧时间节点
     */
    handleRemoveNode(val) {
      const params = {
        ddate: val.ddate,
        combineCode: this.curCombCode
      }
      this.$confirm('此操作将删除该日期节点, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          deleteNodeById(params).then(async res => {
            if (res.data.status === 0) {
              this.$message({
                type: 'success',
                message: res.data.message || '删除成功',
                customClass: 'message-success'
              })
              await this.handleFindNode(this.curCombCode)
              // 查询第一个节点
              if (this.dateList.length > 0) {
                this.handleNodeChange(this.dateList[0])
              } else {
                this.tableData = []
              }
            } else {
              this.$message({
                type: 'error',
                message: res.data.message || '删除失败',
                customClass: 'message-error'
              })
            }
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          })
        })
    },
    /**
     * @description 新增左侧时间节点
     */
    handleInsertNode() {
      if (this.dDate) {
        const dateList = this.dateList.map(item => item.ddate)
        if (dateList.includes(this.dDate)) {
          this.$message.closeAll()
          this.$message({
            type: 'warning',
            message: '日期已存在',
            customClass: 'message-warning'
          })
          return
        } else {
          this.insertBtnLoading = true
          const params = {
            ddate: this.dDate,
            combineCode: this.curCombCode,
            fundName: this.curCombName
          }
          insertNode(params)
            .then(async res => {
              this.insertBtnLoading = false
              if (res.data.status === 0) {
                const saveCurDate = this.curDateNode
                const saveCurDateKey = this.curDateNodeKey
                this.$message({
                  type: 'success',
                  message: res.data.message || '新增成功',
                  customClass: 'message-success'
                })
                await this.handleFindNode(this.curCombCode)
                this.curDateNode = saveCurDate
                this.curDateNodeKey = saveCurDateKey
                this.dateList.forEach(item => {
                  if (item.ddate == this.curDateNode) {
                    item.checked = true
                  } else {
                    item.checked = false
                  }
                })
                this.dDate = ''
              } else {
                this.$message({
                  type: 'error',
                  message: res.data.message || '新增失败',
                  customClass: 'message-error'
                })
              }
            })
            .catch(err => {
              this.insertBtnLoading = false
            })
        }
      } else {
        this.$message({
          type: 'warning',
          message: '请选择节点日期',
          customClass: 'message-warning'
        })
      }
    },
    /**
     * @description 监听左侧时间节点切换
     */
    handleNodeChange(val) {
      if (!val) {
        return
      }
      const { fId } = val
      const _Index = this.dateList.findIndex(item => {
        return item.fId === fId
      })
      this.dateList.forEach(item => {
        item.checked = false
      })
      this.dateList[_Index].checked = true
      this.curDateNode = val.ddate
      this.curDateNodeKey = val.fId
      this.queryTableByDateNode()
    },
    /**
     * @description 添加产品
     */
    handleAddFund() {
      if (this.dateList && this.dateList.length > 0) {
        this.productSelectorVisible = true
      } else {
        this.$message({
          type: 'warning',
          message: '请先创建左侧日期节点',
          customClass: 'message-warning'
        })
      }
    },
    /**
     * @description 节点调仓表格查询
     */
    queryTableByDateNode() {
      this.isFirstData = false
      const params = {
        combineCode: this.curCombCode,
        ddate: this.curDateNode
      }
      this.tableLoading = true
      getNodeTable(params)
        .then(res => {
          if (res.data.status === 0) {
            if (this.curDateNode == this.createDateNode) {
              this.isFirstData = true
            }
            this.tableData = res.data.data.rows || []
            this.tableData = this.tableData.map(item => {
              return {
                ...item,
                prevPrice: item.prevPrice ? (Number(item.prevPrice) / 10000).toFixed(2) : '',
                prevCostrate: item.prevCostrate ? Number(item.prevCostrate * 100).toFixed(2) : '',
                costrate: item.costrate ? Number(item.costrate * 100).toFixed(2) : '',
                priceJ: item.priceJ ? (Number(item.priceJ) / 10000).toFixed(2) : '',
                priceChg: item.priceChg ? (Number(item.priceChg) / 10000).toFixed(2) : ''
              }
            })
            this.tableLoading = false
          } else {
            this.tableData = []
            this.tableLoading = false
          }
        })
        .catch(e => {
          this.tableLoading = false
        })
    },
    /**
     * @description 获取已选产品组装表格
     */
    handleSubmitClick(arr) {
      this.productSelectorVisible = false
      const some = []
      const curData = arr.map(item => {
        return {
          combineCode: this.curCombCode,
          fundCode: item.VC_FUNDCODE || '-',
          fundName: item.VC_FUNDNAME || '-',
          fcreateDate: item.D_CREATE_DATE || '-',
          ddate: this.curDateNode,
          fundType: item.VC_FLAG,
          prevCostrate: 0,
          priceJ: 0,
          costrate: 0,
          prevPrice: 0,
          priceChg: 0
        }
      })
      this.tableData.unshift(...curData)
      this.tableData.forEach(el => {
        if (!some.some(e => e.fundCode == el.fundCode)) {
          some.push(el)
        }
      })
      this.tableData = some
      this.selectList = arr
    },
    /**
     * @description 标为合计项
     */
    footerMethod({ columns, data }) {
      return [
        columns.map((column, columnIndex) => {
          if (columnIndex === 2) {
            return '和值'
          }
          if (['priceJ', 'costrate', 'prevCostrate', 'prevPrice', 'priceChg'].includes(column.property)) {
            return this.sumNum(data, column.property)
          }
          return null
        })
      ]
    },
    /**
     * @description 合计计算
     */
    sumNum(list, field) {
      const rate = ['costrate', 'prevCostrate']
      let count = 0
      if (rate.includes(field)) {
        list.forEach(item => {
          if (item[field]) {
            count += Number(item[field])
          }
        })
        return count.toFixed(2) + '%'
      } else {
        list.forEach(item => {
          if (item[field]) {
            count += Number(item[field])
          }
        })
        this.sumCount = count.toFixed(2)
        return commonFilter.moneyYuan(count)
      }
    },

    /**
     * @description 合计计算
     */
    sumNumValue(list, field) {
      const rate = ['costrate', 'prevCostrate']
      let count = 0
      if (rate.includes(field)) {
        list.forEach(item => {
          if (item[field]) {
            count += Number(item[field])
          }
        })
        return count.toFixed(2) + '%'
      } else {
        list.forEach(item => {
          if (item[field]) {
            count += Number(item[field])
          }
        })
        this.sumCount = count.toFixed(2)
        return this.sumCount
      }
    },

    /**
     * @description 监听市值变化计算调整金额
     */
    updatePrice(event, rowIndex, col, row) {
      // 获取vxe表格ref
      const $table = this.$refs.vxetable
      // 调仓后市值
      const value = Number(event.target.value) || 0
      // 设置调仓后市值对应的值
      this.$set(this.tableData[rowIndex], col, value.toFixed(2))
      // 计算调整金额 调仓后市值 - 调仓前市值
      const editPrice = value - (this.tableData[rowIndex].prevPrice || 0)
      // 设置调仓金额对应的值
      this.$set(this.tableData[rowIndex], 'priceChg', editPrice.toFixed(2))
      // 更新表尾合计
      $table.updateFooter()
      this.sumNum(this.tableData, col)
      // 循环计算对应调仓后市值的权重 调仓后市值 / 合计 * 100
      this.tableData.forEach((v, i) => {
        this.$set(this.tableData[i], 'costrate', ((v[col] / this.sumCount) * 100).toFixed(2))
      })
    },
    /**
     * @description 监听权重变化
     */
    updateRate(event, rowIndex, col, row) {
      // 调仓后权重
      const value = Number(event.target.value) || 0
      // 设置调仓后权重值
      this.$set(this.tableData[rowIndex], col, value.toFixed(2))
      this.sumNum(this.tableData, 'priceJ')
      // 计算权重变更后对应市值 权重 / 100 * 合计
      const priceJ = ((value / 100) * this.sumCount).toFixed(2)
      // 获取当前现金值
      let curCash = 0
      this.tableData.forEach(v => {
        if (v.fundCode === 'CASH') {
          curCash = Number(v.priceJ)
        }
      })
      // 计算调仓市值差异
      const spreadPrice = priceJ - (row['priceJ'] || 0)
      // 设置权重变更后对应市值
      this.$set(this.tableData[rowIndex], 'priceJ', priceJ)
      // 计算市值变更后对应调仓金额
      const editPrice = Number(this.tableData[rowIndex]['priceJ']) - (Number(this.tableData[rowIndex]['prevPrice']) || 0)
      // 设置对应调仓金额
      this.$set(this.tableData[rowIndex], 'priceChg', editPrice.toFixed(2))
      // 判断调仓市值差异为负则现金加, 为正则现金减
      if (spreadPrice.toString().startsWith('-')) {
        curCash += Number(spreadPrice.toString().replace(/-/g, ''))
      } else {
        curCash -= spreadPrice
      }
      // 循环找到现金行设置变更后现金、权重、调仓金额
      this.tableData.forEach((v, i) => {
        if (v.fundCode === 'CASH') {
          this.$set(this.tableData[i], 'priceJ', curCash.toFixed(2))
          this.sumNum(this.tableData, 'priceJ')
          const editCash = Number(v.priceJ) - (Number(v.prevPrice) || 0)
          this.$set(this.tableData[i], 'priceChg', editCash.toFixed(2))
          this.$set(this.tableData[i], 'costrate', ((v['priceJ'] / this.sumCount) * 100).toFixed(2))
        }
      })
    },
    /**
     * @description 删除产品
     */
    handleDeleteFund(row) {
      // 判断市值、权重是否都为0

      const fundCode = row.fundCode
      const _index = this.tableData.findIndex(item => item.fundCode === fundCode)
      this.tableData.splice(_index, 1)
      const sum = this.sumNumValue(this.tableData, 'priceJ')
      this.tableData.forEach(item => {
        item.costrate = ((Number(item.priceJ) / Number(sum)) * 100).toFixed(2)
      })
    },
    /**
     * @description 清仓
     */
    handleClearData(row) {
      // 获取vxe表格ref
      const $table = this.$refs.vxetable
      // 循环将清仓数据加至现金行中
      this.sumNum(this.tableData, 'priceJ')
      this.tableData.forEach((v, i) => {
        if (v.fundCode === 'CASH') {
          const cash = Number(row.priceJ) + Number(v.priceJ)
          this.$set(this.tableData[i], 'priceJ', cash.toFixed(2))
          const editCash = cash - Number(v.prevPrice || 0)
          this.$set(this.tableData[i], 'priceChg', editCash.toFixed(2))
          this.$set(this.tableData[i], 'costrate', ((v['priceJ'] / this.sumCount) * 100).toFixed(2))
        }
      })
      // 调仓后数据置空
      row.priceJ = 0
      row.costrate = 0
      row.priceChg = 0
      // 更新表尾合计
      $table.updateFooter()
    },
    /**
     * @description 保存调仓表格
     */
    handleSaveTable() {
      let flag = false
      if (!this.tableData.length) {
        this.$message({
          type: 'warning',
          message: '请先添加调仓产品',
          customClass: 'message-warning'
        })

        return
      }
      this.tableData.forEach(v => {
        if (Number(v.priceJ) < 0 || Number(v.costrate) < 0) {
          flag = true
        }
      })
      if (flag) {
        this.$message({
          type: 'warning',
          message: '您维护的持仓为负请调整后再进行保存',
          customClass: 'message-warning'
        })
        return
      }
      const subProductList = this.tableData.map(v => {
        return {
          pid: this.curDateNodeKey || '',
          fundCode: v.fundCode || '',
          fundName: v.fundName || '',
          combineCode: v.combineCode || '',
          priceJ: Number(v.priceJ * 10000) || '',
          costrate: Number(v.costrate) / 100 || '',
          ddate: this.curDateNode || '',
          fundType: v.fundType || '',
          createDate: v.createDate || ''
        }
      })
      const params = {
        subProductList,
        sumPriceJ: this.sumCount * 10000
      }
      this.tableLoading = true
      saveEditFund(params)
        .then(res => {
          if (res.data.status === 0) {
            this.$message({
              type: 'success',
              message: res.data.message || '保存成功',
              customClass: 'message-success'
            })
            this.tableLoading = false
          } else {
            this.$message({
              type: 'error',
              message: res.data.message || '保存失败',
              customClass: 'message-error'
            })
            this.tableLoading = false
          }
        })
        .catch(err => {
          this.tableLoading = false
        })
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
.table-span-disabled {
  margin-top: 7px;
  height: 32px;
  line-height: 32px;
  font-size: 14px !important;
  -webkit-appearance: none;
  background-image: none;
  border-radius: 4px;
  border: 1px solid #e4e7ed;
  box-sizing: border-box;
  display: inline-block;
  outline: 0;
  padding: 0 15px;
  width: 100%;
  background-color: #f5f7fa;
  color: #c0c4cc;
  cursor: not-allowed;
  overflow: hidden;
}

.table-span {
  margin-top: 7px;
  height: 32px;
  line-height: 32px;
  font-size: 14px !important;
  -webkit-appearance: none;
  background-image: none;
  border-radius: 4px;
  border: 1px solid #dcdfe6;
  box-sizing: border-box;
  display: inline-block;
  outline: 0;
  padding: 0 15px;
  width: 160px;
  background-color: #fff;
  color: #333;
  overflow: hidden;
}

.tiaocangPage {
  height: 100%;
  width: 100%;
  background-color: #fff;
  border: 2px solid #ccc;

  .container {
    width: 100%;
    height: 100%;

    .Aside {
      border-right: 2px solid #ccc;
      padding: 10px;
    }

    .Main {
      padding: 10px !important;
    }
  }
}

.dateList {
  margin-top: 20px;

  .dateItem {
    border-bottom: 1px solid #e8eaec;
    padding: 8px 2px;
    font-size: 14px;
    display: flex;
    justify-content: space-between;

    .checked {
      font-weight: 600;
    }
  }

  .dateItem:hover {
    background: #e6edfc;
    color: #4a8ce8;
    cursor: pointer;
  }
}

.color-box {
  display: inline-block;
  height: 30px;
  width: 2px;
  background-color: #0f65dd;
}

.title-style {
  color: #0f65dd;
  vertical-align: middle;
  height: 35px;
  line-height: 35px;
  font-size: 16px;
  margin-left: 5px;
  display: inline-block;
}

::v-deep .vxe-table .vxe-body--row.row--stripe {
  background-color: #f9fafe !important;
}
::v-deep .payDialog.el-dialog {
  width: 55% !important;
}
::v-deep .payDialog .el-dialog__title {
  color: #0f65dd !important;
}
</style>

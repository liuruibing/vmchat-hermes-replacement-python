<template>
  <div style=" padding: 16px 10px; position: relative; height: 100%; width: 100%; overflow-y: auto" v-loading="pageLoading">
    <el-steps class="stanard-step" :active="active" align-center finish-status="success" process-status="process">
      <el-step title="选择子产品"></el-step>
      <el-step title="创建模拟组合"></el-step>
      <el-step title="配置权重"></el-step>
      <el-step title="回测分析"></el-step>
    </el-steps>
    <div style="background-color: #fff;">
    <div style="height: 24px"></div>
    <ProductSelection
      :active="active"
      :ddate="ddate"
      :pid="pid"
      :select-list="selectList"
      :show-tree-key-array="showTreeKeyArray"
      :sub-combine-code="subCombineCode"
      :tree-data="treeData"
      multiple
      title="选择产品"
      @submitdialog="handleSubmitClick"
    ></ProductSelection>
    <div class="setp-line"></div>
    <div id="create-composition">
      <template v-if="active >= 1">
        <div style="height: 24px"></div>
        <CreateComposition :save-edit-fund-flag="saveEditFundFlag" :select-list="selectList" :sub-combine-code="subCombineCode" @savecomb="handleSaveSuccess"></CreateComposition>
        <div class="setp-line"></div>
      </template>
    </div>
    <div id="section-weight">
      <template v-if="active >= 2">
        <!--      <template >-->
        <div class="setp-title flex standard-form">
          <!-- <span>3、配置权重</span> -->
          <el-button size="small" type="primary" @click="openQZ">权重配置模型</el-button>
        </div>
        <div v-loading="modelLoading" v-if="MeanVarianceModelShow && dialogForm.radio != '5'" style="padding: 20px; border: 1px solid #ccc; margin-bottom: 10px">
          <!--        <MeanVarianceModel></MeanVarianceModel>-->
          <bl-model v-if="dialogForm.radio == '3'" ref="blmodel" @weightarray="handleSelectChangeByTable"></bl-model>
          <markowitz-model v-if="dialogForm.radio == '1'" ref="markowitzmodel" @selectrow="handleSelectChange" @weightarray="handleSelectChangeByTable"></markowitz-model>
          <risk-model v-if="dialogForm.radio == '2'" ref="riskmodel" @weightarray="handleSelectChangeByTable"></risk-model>
          <scat-model v-if="dialogForm.radio == '4'" ref="scatmodel" @weightarray="handleSelectChangeByTable"></scat-model>
        </div>
        <div v-if="MeanVarianceModelShow" class="setp-title">配置详细</div>
        <ConfigurationWeight
          ref="configurationWeight"
          :active="active"
          :select-list="selectListRow"
          :subCombineCode="subCombineCode"
          @onSubmit="handleOnSubmit"
        ></ConfigurationWeight>
        <div class="setp-line"></div>
      </template>
    </div>
    <div id="section-back">
      <template v-if="active >= 3">
        <div style="height: 24px"></div>
        <BackTestAnalyse ref="backTestAnalyse" :combine-code-value="subCombineCode"></BackTestAnalyse>
        <div class="setp-line"></div>
      </template>
    </div>
    <el-dialog custom-class="chooseModel" :visible.sync="dialogVisible" title="选择模型" width="40%">
      <div class="standard-form">
        <div>
          <!-- <span style="color: #0F65DD">选择模型：</span> -->
          <el-radio-group v-model="dialogForm.radio" size="mini">
            <el-radio border label="1">均值方差模型</el-radio>
            <el-radio border label="2">风险平价模型</el-radio>
            <el-radio border label="3">BL模型</el-radio>
            <el-radio border label="4">波动率模型</el-radio>
            <el-radio border label="5">等权重</el-radio>
          </el-radio-group>
        </div>
<!--        <div v-if="dialogForm.radio != 5" class="mt10">
          <span>选择频率:</span>
          <el-select v-model="dialogForm.frequent" placeholder="请选择">
            <el-option v-for="item in frequentOption" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </div>-->
        <div v-if="dialogForm.radio != 5" class="mt10">
          <span>选择区间:</span>
          <el-date-picker
            v-model="dialogForm.date"
            end-placeholder="结束日期"
            format="yyyy-MM-dd"
            range-separator="至"
            size="small"
            start-placeholder="开始日期"
            type="daterange"
            value-format="yyyy-MM-dd"
          ></el-date-picker>
        </div>
      </div>
      <span slot="footer" class="standard-form dialog-footer">
        <el-button type="primary" size="small" @click="mxqr">确 定</el-button>
      </span>
    </el-dialog>
    </div>
  </div>
</template>
<script>
import ProductSelection from './components/ProductSelection.vue'
import CreateComposition from './components/CreateComposition.vue'
import ConfigurationWeight from './components/ConfigurationWeight.vue'
import BackTestAnalyse from '@/views/simulationGroup/backTestAnalyse/index.vue'
import MeanVarianceModel from './components/meanVarianceModel.vue'
import blModel from './components/blModel'
import markowitzModel from './components/markowitzModel'
import riskModel from './components/riskModel'
import scatModel from './components/scatModel'
import { fofMeanSearch, saveEditFund } from './scripts/api'

export default {
  components: {
    ProductSelection,
    CreateComposition,
    ConfigurationWeight,
    BackTestAnalyse,
    MeanVarianceModel,
    blModel,
    markowitzModel,
    riskModel,
    scatModel
  },
  data() {
    return {
      pageLoading: false,
      // 配置权重加载动画
      modelLoading: false,
      // 当前激活步骤
      active: 0,
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
      frequentOption: [
        {
          value: 'D',
          label: '日频'
        },
        {
          value: 'W',
          label: '周频'
        },
        {
          value: 'M',
          label: '月频'
        }
      ],
      // 已选产品
      selectList: [],
      // 当前创建的模拟组合代码
      subCombineCode: '',
      SubCombineName: '', // 保存的模拟组合代码名称
      subBeCodeName: '', // 基准名称
      // 当前创建的模拟组合信息
      subCombineInfo: {},
      // 当前模拟组合成立日期
      ddate: '',
      saveEditFundFlag: false,
      // 当前模拟组合pid
      pid: '',
      price: 0, // 初始金额
      MeanVarianceModelShow: false,
      dialogVisible: false,
      dialogForm: {
        date: [],
        frequent: 'D',
        radio: '5'
      },
      selectListRow: []
    }
  },
  watch: {
    selectList: {
      handler(val) {}
    }
  },
  mounted() {},
  activated() {
    if (this.$store.getters.fromCreateSumuComb) {
      this.$store.commit('SET_FROMCREATESUMUCOMB', false)
      if (this.$route.query && this.$route.query.checkArr) {
        // 初始化页面的所有参数
        this.active = 0
        this.subCombineCode = ''
        this.subCombineInfo = {}
        this.ddate = ''
        this.pid = ''
        this.price = 0
        this.MeanVarianceModelShow = false
        this.saveEditFundFlag = false
        this.dialogVisible = false
        this.dialogForm = {
          date: [],
          frequent: 'D',
          radio: '5'
        }
        this.selectListRow = []
        const tempArr = []
        this.$route.query.checkArr.forEach((item) => {
          tempArr.push({
            D_CREATE_DATE: item.fundDate,
            VC_FLAG: item.source,
            VC_FUNDCODE: item.fundCode,
            VC_FUNDNAME: item.fundName
          })
        })
        this.selectList = tempArr
      } else {
        // 初始化页面的所有参数
        this.active = 0
        this.subCombineCode = ''
        this.subCombineInfo = {}
        this.ddate = ''
        this.pid = ''
        this.price = 0
        this.MeanVarianceModelShow = false
        this.saveEditFundFlag = false
        this.dialogVisible = false
        this.dialogForm = {
          date: [],
          frequent: 'D',
          radio: '5'
        }
        this.selectListRow = []
        this.selectList = []
      }
    }
  },
  methods: {
    jumpToSection(id) {
      this.pageLoading = true
      const element = document.getElementById(id)
      if (!element) {
        return
      }

      element.scrollIntoView()
      const appMain = document.querySelector('#appMain')
      if (appMain) {
        appMain.style.marginTop = '0px'
        setTimeout(() => {
          appMain.style.marginTop = '94px'
        }, 300)
      }
      setTimeout(() => {
        this.pageLoading = false
      }, 1000)
    },
    handleOnSubmit() {
      this.active = 3
      // 处理 保存 回测分析的操作
      const subProductList = []
      let sumWeight = 0
      let sumMarketValue = 0
      for (let i = 0; i < this.$refs.configurationWeight.tableData.length - 2; i++) {
        const temp = this.$refs.configurationWeight.tableData[i]
        const obj = {
          pid: this.pid,
          fundCode: temp.VC_FUNDCODE,
          fundName: temp.VC_FUNDNAME,
          combineCode: this.subCombineCode,
          priceJ: Number(temp.marketValue) * 10000,
          costrate: Number(temp.weight) / 100,
          ddate: this.ddate,
          createDate: this.ddate,
          fundType: temp.fundType
        }
        subProductList.push(obj)
        sumWeight += Number(temp.weight)
        sumMarketValue += Number(temp.marketValue)
      }
      const obj = {
        pid: this.pid,
        fundCode: 'CASH',
        fundName: '现金',
        combineCode: this.subCombineCode,
        priceJ: Number(this.$refs.configurationWeight.tableData[this.$refs.configurationWeight.tableData.length - 2].marketValue) * 10000,
        costrate: Number(this.$refs.configurationWeight.tableData[this.$refs.configurationWeight.tableData.length - 2].weight) / 100,
        ddate: this.ddate,
        createDate: this.ddate,
        fundType: 0
      }
      subProductList.push(obj)
      sumWeight = sumWeight + Number(this.$refs.configurationWeight.tableData[this.$refs.configurationWeight.tableData.length - 2].weight)
      sumMarketValue = sumMarketValue + Number(this.$refs.configurationWeight.tableData[this.$refs.configurationWeight.tableData.length - 2].marketValue)
      if (sumWeight > 100) {
        this.$message.closeAll()
        this.$message.warning('权重大于100%')
        return
      }
      if (sumMarketValue > this.price) {
        this.$message.closeAll()
        this.$message.warning('合计市值大于初始市值')
        return
      }

      const params = {}
      params.subProductList = subProductList
      params.sumPriceJ = Number(this.price) * 10000
      saveEditFund(params).then((res) => {
        this.$refs.backTestAnalyse.dateInit(this.ddate)
        this.$refs.backTestAnalyse.combineName = this.subCombineName
        this.$refs.backTestAnalyse.beCodeName = this.subBeCodeName
        this.$refs.backTestAnalyse.getBackTestData()
      })
      setTimeout(() => {
        this.jumpToSection('section-back')
      }, 0)
    },
    // 选中行 信息
    handleSelectChange(val) {
      this.$message.closeAll()
      this.$message.success('设置权重成功')
      // 同步到列表里面去
      const tableData = []
      const xianjin = { VC_FUNDNAME: '现金', weight: 0, marketValue: 0 }
      const heji = { VC_FUNDNAME: '合计', weight: 100, marketValue: this.price || 0 }
      let sumWeight = 0
      let sumMarketValue = 0
      for (let i = 0; i < this.selectList.length; i++) {
        const temp = this.selectList[i]
        const obj = {
          VC_FUNDCODE: temp.VC_FUNDCODE,
          VC_FUNDNAME: temp.VC_FUNDNAME,
          D_CREATE_DATE: temp.D_CREATE_DATE,
          fundType: temp.VC_FLAG,
          // weight: val[temp.VC_FUNDCODE] || 0,
          weight: (val[temp.VC_FUNDNAME] * 100).toFixed(2) || 0,
          // marketValue: this.price * (val[temp.VC_FUNDCODE] || 0)
          marketValue: this.price * (val[temp.VC_FUNDNAME].toFixed(4) || 0)
        }
        sumWeight += Number(obj.weight)
        sumMarketValue += Number(obj.marketValue)
        tableData.push(obj)
      }
      xianjin.weight = 100 - Number(sumWeight)
      xianjin.marketValue = Number(this.price) - Number(sumMarketValue)
      tableData.push(xianjin)
      tableData.push(heji)
      this.$refs.configurationWeight.initTableBySelectChange(tableData)
      setTimeout(() => {
        this.jumpToSection('section-back')
      }, 0)
    },

    handleSelectChangeByTable(val) {
      if (val.length > 0) {
        val = val[0]
        const tableData = []
        const xianjin = { VC_FUNDNAME: '现金', weight: 0, marketValue: 0 }
        const heji = { VC_FUNDNAME: '合计', weight: 100, marketValue: this.price || 0 }
        let sumWeight = 0
        let sumMarketValue = 0
        for (let i = 0; i < this.selectList.length; i++) {
          const temp = this.selectList[i]
          const obj = {
            VC_FUNDCODE: temp.VC_FUNDCODE,
            VC_FUNDNAME: temp.VC_FUNDNAME,
            D_CREATE_DATE: temp.D_CREATE_DATE,
            weight: (val[temp.VC_FUNDNAME] * 100).toFixed(2) || 0,
            fundType: temp.VC_FLAG,
            marketValue: this.price * (val[temp.VC_FUNDNAME].toFixed(2) || 0)
          }
          sumWeight += Number(obj.weight)
          sumMarketValue += Number(obj.marketValue)
          tableData.push(obj)
        }
        xianjin.weight = 100 - Number(sumWeight)
        xianjin.marketValue = Number(this.price) - Number(sumMarketValue)
        tableData.push(xianjin)
        tableData.push(heji)
        this.$refs.configurationWeight.initTableBySelectChange(tableData)
        this.$message.closeAll()
        this.$message.success('应用成功')
        setTimeout(() => {
          this.jumpToSection('section-back')
        }, 0)
      }
    },

    // 均分模型
    average() {
      const tableData = []
      const xianjin = { VC_FUNDNAME: '现金', weight: 0, marketValue: 0 }
      const heji = { VC_FUNDNAME: '合计', weight: 100, marketValue: this.price || 0 }
      const averageWeight = Number(100 / this.selectList.length).toFixed(2)
      let sumWeight = 0
      let sumMarketValue = 0
      for (let i = 0; i < this.selectList.length; i++) {
        const temp = this.selectList[i]
        const obj = {
          VC_FUNDCODE: temp.VC_FUNDCODE,
          VC_FUNDNAME: temp.VC_FUNDNAME,
          D_CREATE_DATE: temp.D_CREATE_DATE,
          weight: averageWeight,
          fundType: temp.VC_FLAG,
          marketValue: (Number(this.price) * averageWeight) / 100
        }
        sumWeight += Number(averageWeight)
        sumMarketValue += Number(obj.marketValue)
        tableData.push(obj)
      }
      xianjin.weight = 100 - Number(sumWeight)
      xianjin.marketValue = Number(this.price) - Number(sumMarketValue)
      tableData.push(xianjin)
      tableData.push(heji)
      this.$refs.configurationWeight.initTableBySelectChange(tableData)
    },

    /**
     * @description 已选产品数据
     */
    handleSubmitClick(val) {
      this.selectList = val.data
      if (val.status == 'update') {
        if (this.active >= 2) {
          this.active = 1
          setTimeout(async () => {
            this.dialogForm = {
              date: [],
              frequent: 'D',
              radio: '5'
            }
            // 调用updateSubProduct 接口保存当前的组合信息
            await this.fundChangeSaveProduct()
            // 销毁第三步
            this.handleSaveSuccess({})
          }, 300)
        }
      } else if (val.status == 'add') {
        this.active = 1
        setTimeout(() => {
          this.jumpToSection('create-composition')
        }, 0)
      }
    },

    fundChangeSaveProduct() {
      return new Promise((resolve, reject) => {
        const subProductList = []
        for (let i = 0; i < this.selectList.length; i++) {
          let temp = this.selectList[i]
          const obj = {
            pid: this.pid,
            fundCode: temp.VC_FUNDCODE,
            fundName: temp.VC_FUNDNAME,
            combineCode: this.subCombineCode,
            priceJ: 0,
            costrate: 0,
            ddate: this.ddate,
            createDate: this.ddate,
            fundType: temp.VC_FLAG
          }
          subProductList.push(obj)
        }
        subProductList.push({
          pid: this.pid,
          fundCode: 'CASH',
          fundName: '现金',
          combineCode: this.subCombineCode,
          priceJ: this.priceJ * 10000,
          costrate: 1,
          ddate: this.ddate,
          createDate: this.ddate,
          fundType: 0
        })
        const params = {}
        params.subProductList = subProductList
        params.sumPriceJ = Number(this.price) * 10000
        saveEditFund(params)
          .then((res) => {
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
    },
    /**
     * @description 当前模拟组合创建信息
     */
    handleSaveSuccess(val) {
      if (val.beCodeName) {
        this.subBeCodeName = val.beCodeName
      }
      if (val.combineName) {
        this.subCombineName = val.combineName
      }
      if (val.combineCode) {
        this.subCombineCode = val.combineCode
      }
      if (val.ddate) {
        this.ddate = val.ddate
      }
      if (val.pid) {
        this.pid = val.pid
      }
      if (val.price) {
        this.price = val.price
      }
      this.active = 2
      setTimeout(() => {
        this.jumpToSection('section-weight')
        this.selectListRow = this.selectList
      }, 0)
      // 修改flag标志位
      // 成立日期，初始资金不能再修改
      this.saveEditFundFlag = true
    },
    openQZ() {
      this.dialogVisible = true
    },

    // 配置权重
    mxqr() {
      if (this.dialogForm.radio == '5') {
        this.dialogVisible = false
        this.MeanVarianceModelShow = true
        this.average()
        return
      }
      if (this.dialogForm.radio != '5') {
        if (this.dialogForm.date == '' || !Array.isArray(this.dialogForm.date) || (this.dialogForm.date.length && this.dialogForm.date.length < 2)) {
          this.$message.closeAll()
          this.$message.warning('请选择区间')
          return
        }
        if (this.dialogForm.frequent == '') {
          this.$message.closeAll()
          this.$message.warning('请选择频率')
          return
        }
      }
      this.dialogVisible = false
      this.MeanVarianceModelShow = true
      const params = {}
      params.masterFundcode = this.subCombineCode
      params.vcParentCode = this.subCombineCode
      params.vcPin = '1'
      params.fundCodes = this.selectList
        .map((item) => {
          return item.VC_FUNDCODE
        })
        .join(',')
      params.beginDate = this.dialogForm.date[0]
      params.endDate = this.dialogForm.date[1]
      params.frequent = this.dialogForm.frequent
      params.subcode = '702A'
      params.version = '1.3.0'
      const formData = new FormData()
      formData.append('masterFundcode', this.subCombineCode)
      formData.append('vcPin', '1')
      formData.append(
        'fundCodes',
        this.selectList
          .map((item) => {
            return item.VC_FUNDCODE
          })
          .join(',')
      )
      formData.append('beginDate', this.dialogForm.date[0])
      formData.append('endDate', this.dialogForm.date[1])
      formData.append('frequent', this.dialogForm.frequent)
      formData.append('subcode', '702A')
      formData.append('version', '1.3.0')
      this.modelLoading = true
      fofMeanSearch(formData)
        .then((res) => {
          this.modelLoading = false
          if (this.dialogForm.radio == '1') {
            this.$refs.markowitzmodel.handleMarkowitzmodelSelect({ res: res.data, params: params })
          } else if (this.dialogForm.radio == '2') {
            this.$refs.riskmodel.handleMarkowitzmodelSelect({ res: res.data, params: params })
          } else if (this.dialogForm.radio == '3') {
            this.$refs.blmodel.handleMarkowitzmodelSelect({ res: res.data, params: params })
          } else if (this.dialogForm.radio == '4') {
            this.$refs.scatmodel.handleMarkowitzmodelSelect({ res: res.data, params: params })
          }
        })
        .catch((err) => {
          this.modelLoading = false
        })
    }
  }
}
</script>
<style lang="scss" scoped>
.setp-title {
  padding: 20px 0;
  color: #e03d3e;
  font-size: 16px;
}

.setp-line {
  height: 1px;
  background: #ccc;
}

.flex {
  display: flex;
  justify-content: right;
}


</style>

<template>
  <div class="new_bass_info_style">
    <el-dialog
      :title="titleName"
      :visible.sync="dialogVisible"
      custom-class='diaglogWidth'
      center
      @closed='closedDialog'
      :close-on-click-modal='false'>
      <el-tabs v-model="activeName" @tab-click="handleClick">
        <el-tab-pane label="基础信息" name="first">
          <span slot="label" v-if="hasChang.first">基础信息<i style="color: red" class="el-icon-warning"></i></span>
          <bass-info ref='bassInfoRelation'></bass-info>
        </el-tab-pane>
        <el-tab-pane label="交易信息" name="second">
          <span slot="label" v-if="hasChang.second">交易信息<i style="color: red" class="el-icon-warning"></i></span>
          <deal-info ref='dealInfoRelation'></deal-info>
        </el-tab-pane>
        <el-tab-pane label="费用信息" name="third">
          <span slot="label" v-if="hasChang.third">费用信息<i style="color: red" class="el-icon-warning"></i></span>
          <cont-info ref='contInfoRelation'></cont-info>
        </el-tab-pane>
        <el-tab-pane label="收益分配" name="fourth">
          <span slot="label" v-if="hasChang.fourth">收益分配<i style="color: red" class="el-icon-warning"></i></span>
          <earnings-info ref='earningsInfoRelation'></earnings-info>
        </el-tab-pane>
        <el-tab-pane label="投资风控" name="five">
          <span slot="label" v-if="hasChang.five">投资风控<i style="color: red" class="el-icon-warning"></i></span>
          <scope-info ref='scopeInfoRelation' @getScopeData='getScopeData'></scope-info>
        </el-tab-pane>
        <el-tab-pane label="销售方式" name="six">
          <span slot="label" v-if="hasChang.six">销售方式<i style="color: red" class="el-icon-warning"></i></span>
          <sales-info ref="salesInfoRelation"></sales-info>
        </el-tab-pane>
        <el-tab-pane label="分类关系" name="isGrid" v-if="isGrid">
          <span slot="label" v-if="hasChang.isGridUer">分类关系<i style="color: red" class="el-icon-warning"></i></span>
          <grid-info ref="GridInfoRelation"></grid-info>
        </el-tab-pane>
        <el-tab-pane label="开放日" name="seven">
          <span slot="label" v-if="hasChang.seven">开放日<i style="color: red" class="el-icon-warning"></i></span>
          <openday-info ref="opendayInfoRelation"></openday-info>
        </el-tab-pane>
        <el-tab-pane label="基金经理" name="eight">
          <span slot="label" v-if="hasChang.eight">基金经理<i style="color: red" class="el-icon-warning"></i></span>
          <fund-manager-info ref="managerInfoRelation"></fund-manager-info>
        </el-tab-pane>
        <el-tab-pane label="联系人" name="night">
          <span slot="label" v-if="hasChang.night">联系人<i style="color: red" class="el-icon-warning"></i></span>
          <link-info ref="linkInfoRelation"></link-info>
        </el-tab-pane>
      </el-tabs>
      <!-- submit -->
      <div class="submitStyle" v-show="hasSubmit">
        <el-form :model="dataForm" ref="dataForm" label-position="right" label-width="120px">
          <el-form-item label="审核意见">
            <el-input v-model.trim="dataForm.approveOpinion" type="textarea" :autosize="{minRows: 4}" placeholder="请输入审核意见" maxlength="1000" show-word-limit></el-input>
          </el-form-item>
          <el-form-item>
            <el-button :disabled='countSubmit_btn' type="primary" size="small" @click="passFlag(1, '审核通过')">审核通过</el-button>
            <el-button :disabled='countSubmit_btn' type="warning" size="small" @click="passFlag(0, '审核不通过')">审核不通过</el-button>
          </el-form-item>
        </el-form>
      </div>
      <!-- lookdata -->
      <div v-show="viewInfo" class="viewInfoBorder">
        <el-form :model="dataCheack" ref="dataCheack" label-position="right" label-width="120px" style="margin-top: 15px">
          <el-form-item label="审核人">
            <el-input v-model="dataCheack.man" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="审核意见">
            <el-input v-model="dataCheack.remark" type="textarea" :autosize="{minRows: 4}" maxlength="1000" show-word-limit :disabled="true"></el-input>
          </el-form-item>
        </el-form>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import pageExamineApi from "@/api/product/productExamine"
import pageApi from "@/api/product/productSearch"
import BassInfo from './bass-info'
import DealInfo from './deal-info'
import ContInfo from './cont-info'
import EarningsInfo from './earnings-info'
import ScopeInfo from './scope-info'
import SalesInfo from './sales-info'
import OpendayInfo from './openday-info'
import FundManagerInfo from './fund-manager-info'
import LinkInfo from './link-info'
import GridInfo from './grid-info'
export default {
  components: {
    BassInfo,
    DealInfo,
    ContInfo,
    EarningsInfo,
    ScopeInfo,
    SalesInfo,
    OpendayInfo,
    FundManagerInfo,
    LinkInfo,
    GridInfo
  },
  data() {
    return {
      hasChang: {
        first: false,
        second: false,
        third: false,
        fourth: false,
        five: false,
        six: false,
        isGridUer: false,
        seven: false,
        eight: false,
        night: false,
      },
      titleName: '详情查看',
      countSubmit_btn: false,
      activeName: "first",
      dialogVisible: false,
      hasSubmit: false,
      isGrid: false,
      viewInfo: false,
      dataCheack: {
        man: '',
        remark: '',
      },
      dataForm: {
        approveOpinion: '',
        approveStatus: '',
        id: ''
      }
    };
  },
  methods: {
    init (row, flag, judge) {
      this.dialogVisible = true
      this.activeName = 'first'
      this.dataForm.id = row.id
      if (judge){
        this.titleName = '审核'
        this.hasSubmit = true
      }
      else {
        this.titleName = '详情查看'
        this.hasSubmit = false
      }
      if (flag) this.getSearchDetail(row.fundCode)
      else this.getSearchDetailYS(row.id)
      
    },
    getSearchDetail (fundCode) {
      console.log('查看详情');
      let obj = { 'fundCode': fundCode}
      pageApi.getDataSourceDetail(obj).then(({data: res}) => {
        // console.log(res)
        let dataInfo = {...res.data}
        this.sendData(dataInfo)
      }).catch((err) => console.log('is msg err', err))
    },
    getSearchDetailYS (id) {
      let obj = { 'id': id}
      pageExamineApi.getDataSourceDetail(obj).then(({data: res}) => {
        // console.log('res', res)
        let dataInfo = {...res.data.dataAfter}
        let dataBefore = res.data.dataBefore
        this.hasViewInfo(res.data) //处理不通过时的信息查看
        this.sendData(dataInfo, dataBefore)
      }).catch((err) => console.log('is msg err', err))
    },
    hasViewInfo (data) {
      if (data.approveOpinion) {
        this.viewInfo = true
        this.dataCheack.man = data.modifier
        this.dataCheack.remark = data.approveOpinion
      }
    },
    sendData (dataInfo, flag) {
      if (dataInfo.fundInfo.isGrade == '0') this.isGrid = false
      else this.isGrid = true
      this.$nextTick(() => {
        if (this.isGrid) this.$refs.GridInfoRelation.init(dataInfo, flag)
        this.$refs.bassInfoRelation.init(dataInfo, flag)
        this.$refs.dealInfoRelation.init(dataInfo, flag)
        this.$refs.contInfoRelation.init(dataInfo, flag)
        this.$refs.earningsInfoRelation.init(dataInfo, flag)
        this.$refs.scopeInfoRelation.init(dataInfo, flag)
        this.$refs.salesInfoRelation.init(dataInfo, flag)
        this.$refs.opendayInfoRelation.init(dataInfo, flag)
        this.$refs.managerInfoRelation.init(dataInfo, flag)
        this.$refs.linkInfoRelation.init(dataInfo, flag)
        if (flag) this.hasChangeData(dataInfo, flag)
      })
    },
    handleClick () {},
    closedDialog () {
      for (let i in this.dataForm) this.dataForm[i] = ''
      this.$emit('closed')
    },
    passFlag (status, name) {
      this.$message.closeAll()
      if (status == 0) {
        if (!this.dataForm.approveOpinion) return this.$message.error('请输入审核不通过意见')
        else this.submitRemark(status, name)
      } else this.submitRemark(status, name)
    },
    submitRemark (status, name) {
      this.$confirm("确定" + name + "?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      }).then(() => {
          this.dataForm.approveStatus = status
          this.countSubmit_btn = true
          pageExamineApi.updateDataStatus( { ...this.dataForm } ).then((response) => {
              if (response.data.status === 200) {
                this.$message({
                  message: "提交成功",
                  type: "success",
                })
                // 刷新列表
                this.$emit("rushDataList")
                this.dialogVisible = false
              } else {
                this.$message({
                  message: response.data.message || "提交失败",
                  type: "warning",
                })
              }
              this.countSubmit_btn = false
            }).catch(() => {
              this.$message({
                message: response.data.message || "提交失败",
                type: "warning",
              })
              this.countSubmit_btn = false
            })
        }).catch(() => {
          this.$message.info('已取消')
          this.countSubmit_btn = false
        })
    },
    hasChangeData (dataInfo, flag) {
      this.$nextTick(() => {
        if (this.isGrid) this.hasChang.isGridUer = this.$refs.GridInfoRelation.judgeChange(dataInfo, flag)
       this.hasChang.first = this.$refs.bassInfoRelation.judgeChange(dataInfo, flag)
       this.hasChang.second = this.$refs.dealInfoRelation.judgeChange(dataInfo, flag)
       this.hasChang.third = this.$refs.contInfoRelation.judgeChange(dataInfo, flag)
       this.hasChang.fourth = this.$refs.earningsInfoRelation.judgeChange(dataInfo, flag)
       this.hasChang.five = this.$refs.scopeInfoRelation.judgeChange(dataInfo, flag)
       this.hasChang.six = this.$refs.salesInfoRelation.judgeChange(dataInfo, flag)
       this.hasChang.seven = this.$refs.opendayInfoRelation.judgeChange(dataInfo, flag)
       this.hasChang.eight = this.$refs.managerInfoRelation.judgeChange(dataInfo, flag)
       this.hasChang.night = this.$refs.linkInfoRelation.judgeChange(dataInfo, flag)
      })
    },
    getScopeData(data) {
      if (!this.hasChang.five && data) this.hasChang.five = data
    }
  }
};
</script>
<style lang='scss'>
.new_bass_info_style {
  .diaglogWidth {
    width: 60% !important;
  }
  .submitStyle {
    margin-top: 15px;
 }
 .viewInfoBorder {
    margin-top: 15px;
    border-top: 2px dashed #ccc;
 }
 .errInof {
   color: red !important;
   cursor: default ;
 }
}
 .errInof .el-textarea__inner {
   color: red !important;
 }
 .errInof .el-input__inner {
    color: red !important;
  }
</style>
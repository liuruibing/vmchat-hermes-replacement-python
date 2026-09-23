<template>
  <div class="detailTop">
    <div class="header">
      <div class="product-info standard-form">
        <div class="top">
          <img :src="require('../style/product.png')"/>
          <span class="name">{{ baseInfo.VC_FUNDNAME || '' }}</span>
        </div>
<!--        <div class="bottom">
          <el-button
            @click="handleInitiate"
            size="small"
            type="primary"
            @mouseenter="
              () => {
                showInitiate = true
              }
            "
          >
            发起互动
          </el-button>
          <span style="position: relative; top: 3px">
            <img :src="require('../style/initiateContent.png')"/>
            <span
              style="position: absolute; top: 3px; display: inline-block; width: 100px; left: -10px; color: white">{{
                initiateContent
              }}</span>
          </span>
        </div>-->
<!--        <div class="bottom">
          <span v-if="isShowProductInfo">
            <el-button size="small" type="primary"
                       @click="handleProductInfo">申请绩效权限</el-button>
            <span style="margin-left: 8px;color: #20212B">{{ productInfo.applyAuthStr }}</span>
            <span style="margin-left: 8px;color: #20212B">{{ productInfo.fundGrantStr }}</span>
          </span>
        </div>-->
      </div>
      <div class="product-desc">
        <el-descriptions :column="3" size="small">
          <el-descriptions-item v-for="(desc, index) in descTopData" :key="index" :label="desc.label">
            <span v-if="desc.label === '绩效评级'">
              <el-rate v-model="desc.value" :colors="['rgb(245, 41, 41)', 'rgb(245, 41, 41)', 'rgb(245, 41, 41)']"
                       disabled disabled-void-color="rgb(55, 65, 79)"></el-rate>
            </span>
<!--            <span v-else-if="desc.label === '基金管理人'">
              <el-link :underline="false" style="margin-top: -4px" type="primary" @click="jumpRoute('custodian')">
                {{ desc.value || '' }}
              </el-link>
            </span>-->
            <span v-else>{{ desc.value || '' }}</span>
          </el-descriptions-item>
        </el-descriptions>
      </div>
    </div>
    <div class="base-info-content">
      <div class="left">
        <div v-for="(data, index) in middleLeftData" :key="index" class="data-style">
          <div v-if="data.label == '最新数据日期'" style="font-size: 30px; height: 36px">
            <span style="color: #20212B">{{ baseInfo.D_DATE || '' }}</span>
          </div>
          <div v-else :style="valueToColor(data.value)" class="value" style="font-size: 30px; height: 36px">
            <span>{{ data.value }}</span>
          </div>
          <div class="label-zb" style="text-align: center" v-if="data.label == '最新数据日期'">
            {{ data.label }}
          </div>
          <div v-else class="label-zb">{{ data.label }}</div>
        </div>
      </div>
      <div class="middle">
        <div v-for="(data, index) in middleMiddleData" :key="index" class="data-style">
          <div v-if="data.value" :style="valueToColor(data.value)" class="value">
            {{ data.value + '%' }}
          </div>
          <div v-else class="value" style="height: 36px"></div>
          <div class="label-zb">{{ data.label }}</div>
        </div>
      </div>
      <div class="right">
        <div v-for="(data, index) in middleRightData" :key="index" class="data-style">
          <div v-if="data.value">
            <div v-if="data.label === '成立以来最大回撤'" class="value-right">{{ data.value + '%' }}</div>
            <div v-else :style="valueToColor(data.value)" class="value" style="height: 36px">
              {{ data.value }}
            </div>
          </div>
          <div v-else class="value" style="height: 36px"></div>
          <div class="label-zb">{{ data.label }}</div>
        </div>
      </div>
    </div>
    <div class="footer">
      <div :class="whether ? 'isFixed' : ''">
        <el-form :inline="true" :model="formQuery" label-width="auto" class="standard-form">
          <el-row>
            <!-- <el-col :span="10"> -->
              <el-form-item label="统计周期">
                <el-select v-model="formQuery.statistPeriod" clearable placeholder="请选择" size="small"
                           @change="handleDateChange" @focus="updeteiframe">
                  <el-option v-for="item in statistPeriodOpts" :key="item.value" :label="item.label"
                             :value="item.value"></el-option>
                </el-select>
                <el-date-picker v-model="formQuery.startDate" :disabled="disabledDate" placeholder="开始日期" size="small"
                                type="date" value-format="yyyy-MM-dd"></el-date-picker>
                <el-date-picker v-model="formQuery.endDate" :disabled="disabledDate" placeholder="结束日期" size="small"
                                type="date" value-format="yyyy-MM-dd"></el-date-picker>
              </el-form-item>
            <!-- </el-col> -->
            <!-- <el-col :span="9"> -->
              <el-form-item label="业绩基准">
                <el-select v-model="formQuery.kpiCode" clearable placeholder="请选择" size="small" @focus="updeteiframe">
                  <el-option v-for="item in kpiStandardOpts" :key="item.id" :label="item.label"
                             :value="item.id"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item class="dbjz" label="对比基准">
                <el-select v-model="formQuery.contrasCode" clearable collapse-tags multiple placeholder="请选择"
                           size="small" @change="changeContrasCode" @focus="updeteiframe">
                  <el-option v-for="item in contrasStandardOpts" :key="item.id" :label="item.label"
                             :value="item.id"></el-option>
                </el-select>
              </el-form-item>
            <!-- </el-col> -->
            <!-- <el-col :span="4"> -->
              <el-form-item style="margin-right: 0;">
                <el-button size="small" type="primary" @click="handleSearch">查询</el-button>
                <el-button size="small" type="info" plain @click="reset">重置</el-button>
              </el-form-item>
            <!-- </el-col> -->
          </el-row>
        </el-form>
      </div>
    </div>
    <el-dialog
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      :visible.sync="productInfoVisible"
      custom-class="productinfo-dialog"
      width="700px !important"
      title="申请绩效数据权限"
      @close="() => {this.productInfoVisible = false}"
    >
      <el-form :model="productInfoDialogForm">
        <div id="product-info">
          <div class="mt10"><span class="product-info-label">请选择申请维度，可选择申请本只产品权限或选择申请该管理人下其他广发证券托管外包产品权限</span></div>
          <div class="mt10"><span style="margin-left: 12px;">管理人名称</span>
            <el-input size="small" disabled v-model="productInfoDialogForm.managerName"></el-input>
          </div>
          <div class="mt10">
            <el-checkbox v-model="productInfoDialogForm.currentProductCheck" class="product-info-label"></el-checkbox>
            <span>产品代码</span>
            <el-input size="small" disabled v-model="productInfoDialogForm.fundCode"></el-input>
            <span>产品名称</span>
            <el-input size="small" disabled v-model="productInfoDialogForm.fundName"></el-input>
          </div>
          <div class="mt10">
            <el-checkbox v-model="productInfoDialogForm.otherProductCheck" class="product-info-label"></el-checkbox>
            <span>其他产品</span>
            <el-select v-model="productInfoDialogForm.fundCodes" filterable placeholder="请选择" multiple collapse-tags
                       size="small">
              <el-option
                v-for="item in productFundOtherArray"
                :key="item.fundCode"
                :label="item.fundName"
                :value="item.fundCode">
              </el-option>
            </el-select>
          </div>
          <div class="mt10">
            <span style="margin-left: 27px;">权限等级</span>
            <el-select v-model="productInfoDialogForm.authLevel" filterable placeholder="请选择" size="small">
              <el-option
                v-for="item in productFundINRightArr"
                :key="item.dimCde"
                :label="item.dimNme"
                :value="item.dimCde">
              </el-option>
            </el-select>
          </div>
        </div>
      </el-form>
      <div slot="footer">
        <el-button @click="() => {productInfoVisible = false}">取 消</el-button>
        <el-button type="primary" @click="handleProductInfoSubmit" :loading="productInfoDialogForm.btnLoading">确 定
        </el-button>
      </div>
    </el-dialog>
    <el-dialog
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      :visible.sync="productInfoDetailVisible"
      title="申请绩效数据权限错误信息"
      @close="() => {this.productInfoDetailVisible = false}"
    >
      <div v-html="productInfoDetailErrorMessage"></div>
      <div slot="footer">
        <el-button type="primary" @click="() => {productInfoDetailVisible = false}">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {
  dateShortcutMap,
  MIDDLE_LEFT_DATA,
  MIDDLE_MIDDLE_DATA,
  MIDDLE_RIGHT_DATA,
  STATIST_PERIOD_OPTIONS,
  TOP_DESC_DATA
} from '../scripts/baseInfoConstant'
import request from '@/utils/request'
import commonApi from '@/api/common'
import pageApi from "../api/investmentHistoryTg"

export default {
  name: 'BaseInfo',
  props: {
    currentList: {
      type: Object,
      default: () => {
      }
    },
    fundCode: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      // 申请绩效数据权限 错误信息
      productInfoDetailVisible: false,
      productInfoDetailErrorMessage: '',
      // 申请绩效数据权限
      productInfoDialogForm: {
        btnLoading: false,
        managerName: '',
        fundCodes: [],
        fundCode: '',
        fundName: '',
        authLevel: '',
        currentProductCheck: false,
        otherProductCheck: false,
      },
      productInfoVisible: false,
      isShowProductInfo: false, // 是否展示授权信息
      // 产品授权信息
      productInfo: {
        fundCode: '',
        fundName: '',
        applyAuthLevel: '', //已申请权限
        fundGrant: '', // 已拥有权限
        applyAuthStr: '',
        fundGrantStr: '',
      },
      // 权限等级 下拉
      productFundINRightArr: [],
      // 其他产品
      productFundOtherArray: [],


      initiateContent: '',
      baseInfo: {},
      showInitiate: false,
      formQuery: {
        statistPeriod: '4',
        startDate: '',
        endDate: '',
        kpiCode: '',
        contrasCode: []
      },
      descTopData: TOP_DESC_DATA,
      middleLeftData: MIDDLE_LEFT_DATA,
      middleMiddleData: MIDDLE_MIDDLE_DATA,
      middleRightData: MIDDLE_RIGHT_DATA,
      statistPeriodOpts: STATIST_PERIOD_OPTIONS,
      kpiStandardOpts: [],
      contrasStandardOpts: [],
      dateShortcutMap,
      disabledDate: true,
      whether: false,
      verifyStatus: 1
    }
  },
  watch: {
    currentList: {
      async handler(val) {
        if (val) {
          this.baseInfo = val
          this.checkOneYear(val.FOUND_DATE)
          if (this.baseInfo.VC_IS_APPLYAUTH === '1' || this.baseInfo.VC_IS_APPLYAUTH === 1) {
            this.isShowProductInfo = true
            //await this.refreshProcessStatus()
            await this.getProductFundINRightArr()
            await this.getProductInfo(this.fundCode)
            this.getProductInfoOtherArray(this.fundCode)
          } else {
            this.isShowProductInfo = false
          }
          await this.getVerifyStatus()
          await this.getKpiOptions()
          await this.getContrasOptions()
          await this.handleSearch('ALL')
          await this.getInitiateInfo()
          this.filterContentData(val.VC_SOURCE)
          this.handleFundInfo(val)
        } else {
          this.isShowProductInfo = false
          this.handleFundInfo({})
        }
      },
      immediate: true,
      deep: true
    }
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll, true)
  },
  activated() {
    this.handleScroll()
  },
  destroyed() {
    window.removeEventListener('scroll', this.handleScroll, true)
  },
  methods: {
    // 申请权限 确定弹窗
    handleProductInfoSubmit() {
      if (this.productInfoDialogForm.currentProductCheck === false && this.productInfoDialogForm.otherProductCheck === false) {
        this.$message.closeAll()
        this.$message.warning('产品代码和其他产品至少选中一个')
        return
      }
      if (this.productInfoDialogForm.currentProductCheck === false && this.productInfoDialogForm.otherProductCheck === true) {
        if (this.productInfoDialogForm.fundCodes && this.productInfoDialogForm.fundCodes.length === 0) {
          this.$message.closeAll()
          this.$message.warning('只有其他产品的时候,其他产品不能为空')
          return
        }
      }
      if (this.productInfoDialogForm.authLevel == '') {
        this.$message.closeAll()
        this.$message.warning('权限等级不能为空')
        return
      }
      let params = {}
      params.authLevel = this.productInfoDialogForm.authLevel
      params.fundCodes = []
      if (this.productInfoDialogForm.currentProductCheck) {
        params.fundCodes.push(this.productInfoDialogForm.fundCode)
      }
      if (this.productInfoDialogForm.otherProductCheck) {
        params.fundCodes.push(...this.productInfoDialogForm.fundCodes)
      }

      this.productInfoDialogForm.btnLoading = true;
      pageApi.authApply(params).then(res => {
        let {status, data, message} = res.data
        this.productInfoDialogForm.btnLoading = false
        if (status === 200) {
          if (data && data.length > 0) {
            this.productInfoDetailErrorMessage = ''
            data.forEach(item => {
              this.productInfoDetailErrorMessage += `<span style="color: #f56c6c">${item}</span>`
              this.productInfoDetailErrorMessage += `<br/>`
            })
            this.productInfoVisible = false
            this.$nextTick(() => {
              this.productInfoDetailVisible = true
            })
          } else {
            this.$message.closeAll()
            this.$message.success(message)
            this.productInfoVisible = false
            pageApi.getProductInfo(this.fundCode)
            // pageApi.selectIndexInfos(this.fundCode)
          }
        } else {
          this.$message.closeAll()
          this.$message.warning(message)
        }
      }).catch(err => {
        this.productInfoDialogForm.btnLoading = false
      })

    },
    // 申请权限按钮点击事件
    handleProductInfo() {
      this.productInfoDialogForm.fundCode = this.fundCode
      this.productInfoDialogForm.fundName = this.baseInfo.VC_FUNDNAME
      this.productInfoDialogForm.managerName = this.baseInfo.VC_FUNDNAME
      this.productInfoDialogForm.otherProductCheck = false
      this.productInfoDialogForm.currentProductCheck = false
      this.productInfoDialogForm.fundCodes = []
      this.productInfoDialogForm.authLevel = ''
      this.productInfoVisible = true
    },
    // 刷新流程状态
    refreshProcessStatus() {
      return new Promise((resolve, reject) => {
        pageApi.refreshProcessStatus().then(res => {
          let {status, message} = res.data
          if (status !== 200) {
            this.$message.closeAll()
            this.$message.warning(message)
          }
          resolve()
        }).catch(err => {
          resolve()
        })
      })
    },

    // 获取其他产品 下拉数组
    getProductInfoOtherArray(fundCode) {
      let params = {}
      params.fundCode = fundCode
      pageApi.fundList(params).then(res => {
        let {status, data} = res.data
        if (status === 200) {
          this.productFundOtherArray = data
        } else {
          this.productFundOtherArray = []
        }
      })
    },
    // 获取权限等级下拉数组
    getProductFundINRightArr() {
      return new Promise((resolve, reject) => {
        commonApi.edimsCommon('FUNDINRIGHT').then(res => {
          let {status, data} = res.data
          if (status === 0) {
            let temp = []
            data.forEach(item => {
              if (item.dimCde !== 'All') {
                temp.push(item)
              }
            })
            this.productFundINRightArr = temp
          } else {
            this.productFundINRightArr = []
          }
          resolve()
        }).catch(err => {
          this.productFundINRightArr = []
          resolve()
        })
      })

    },
    // 获取产品授权信息
    getProductInfo(fundCode) {
      if (!fundCode) {
        return
      }
      let params = {}
      params.fundCode = fundCode
      return new Promise((resolve, reject) => {
        pageApi.proAuthInfo(params).then(res => {
          let {status, data} = res.data
          if (status === 200) {
            this.productInfo = data
            if (this.productInfo.fundGrant) {
              let findObj = this.productFundINRightArr.find(item => item.dimCde === this.productInfo.fundGrant)
              if (findObj) {
                this.productInfo.fundGrantStr = `拥有${findObj.dimNme}等级权限`
              } else {
                this.productInfo.fundGrantStr = ''
              }
            }
            if (this.productInfo.applyAuthLevel) {
              let findObj = this.productFundINRightArr.find(item => item.dimCde === this.productInfo.applyAuthLevel)
              if (findObj) {
                this.productInfo.applyAuthStr = `已申请${findObj.dimNme}等级权限`
                if (!this.productInfo.fundGrant) {
                  this.productInfo.fundGrantStr = '拥有0等级权限'
                }
              } else {
                this.productInfo.applyAuthStr = ''
              }
            }
          } else {
            this.productInfo = {
              fundCode: '',
              fundName: '',
              applyAuthLevel: '', //已申请权限
              fundGrant: '', // 已拥有权限
              fundGrantStr: '',
              applyAuthStr: '',
            }
          }
          resolve()
        }).catch(err => {
          this.productInfo = {
            fundCode: '',
            fundName: '',
            applyAuthLevel: '', //已申请权限
            fundGrant: '', // 已拥有权限
            fundGrantStr: '',
            applyAuthStr: '',
          }
          resolve()
        })
      })
    },

    // 获取互动次数
    getInitiateInfo() {
      return new Promise((resolve, reject) => {
        let params = {}
        params.fundCode = this.fundCode
        params.indexCode = '1820aad5-a68b-4e46-b746-ae5657d767fd'

        commonApi.getDataBysqlCode(params).then((res) => {
          let {status, data} = res.data
          if (status === 0) {
            this.initiateContent = `互动${data[0].count}次`
            this.showInitiate = true
          }
          resolve()
        })
      })
    },
    handleInitiate() {
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: `/xqhd/gxhxqgl`,
        query: {
          fcode: this.fundCode,
          fname: this.baseInfo.VC_FUNDNAME
        }
      })
    },
    // 时间转换函数
    timestampToDateString(timestamp) {
      const date = new Date(timestamp)
      const year = date.getFullYear()
      const month = ('0' + (date.getMonth() + 1)).slice(-2)
      const day = ('0' + date.getDate()).slice(-2)
      return `${year}-${month}-${day}`
    },

    /**
     * @description 检查成立日期与当天是否超过一年
     */
    checkOneYear(startDate) {
      // 平年每年的毫秒数
      var ms = 31536000000
      // 将yyyy-mm-dd时间转成数组
      var startArr = startDate.split('-')
      // 生成Date数据
      var start = new Date(parseInt(startArr[0]), parseInt(startArr[1]) - 1, parseInt(startArr[2]), 0, 0, 0)
      // 取出年月，用于判断是否为闰年
      var startYear = start.getFullYear()
      var startMonth = start.getMonth()
      // 闰年判断
      if (this.isLeapYear(startYear) && startMonth <= 2) {
        // 加一天
        ms += 86400000
      }
      // 对当前日期的处理,只取年月日，不要时分秒
      var nowDate = new Date()
      var now = nowDate.getFullYear() + '-' + (nowDate.getMonth() + 1) + '-' + nowDate.getDate()
      var nowArr = now.split('-')
      var now = new Date(parseInt(nowArr[0]), parseInt(nowArr[1]) - 1, parseInt(nowArr[2]), 0, 0, 0)

      // 当前时间-开始时间的毫秒数
      var intervalNow = Number(now) - Number(start)
      var flag
      if (intervalNow > 0) {
        if (intervalNow >= ms) {
          flag = true
        } else {
          flag = false
        }
      }
      console.log(flag, '成立日期距今是否大于一年')
      if (flag) {
        this.formQuery.statistPeriod = '4'
      } else {
        this.formQuery.statistPeriod = '6'
        this.formQuery.startDate = startDate
        this.formQuery.endDate = this.timestampToDateString(now.getTime())
        // this.formQuery.endDate = now
      }
    },
    /**
     * @description 闰年判断
     */
    isLeapYear(year) {
      if (year % 100 == 0) {
        if (year % 400 == 0) {
          return true
        }
      } else if (year % 4 == 0) {
        return true
      }
      return false
    },
    /**
     * @description 根据来源修改content区域数据
     */
    filterContentData(source) {
      if (source === 'IN') {
        this.middleLeftData = this.middleLeftData.filter((item) => item.label !== '复权累计净值')
      } else {
        const _index = this.middleLeftData.findIndex((item) => item.label === '复权累计净值')
        if (_index < 0) {
          const filterObj = {
            label: '复权累计净值',
            value: ''
          }
          this.middleLeftData.push(filterObj)
        }
      }
    },
    /**
     * @description 星级过滤
     */
    filterStar(val) {
      switch (val) {
        case '5':
          return 1
        case '4':
          return 2
        case '3':
          return 3
        case '2':
          return 4
        case '1':
          return 5
        default:
          return 0
      }
    },
    /**
     * @description 颜色判断
     */
    valueToColor(value) {
      if (value && value > 0) {
        return {
          color: 'red'
        }
      } else if (value && value < 0) {
        return {
          color: '#00d83d'
        }
      } else {
        return {
          color: '#20212B'
        }
      }
    },
    /**
     * @description iframe遮罩
     */
    updeteiframe() {
      this.$emit('updeteiframe')
    },
    /**
     * @description 获取是否显示发起验证按钮
     */
    getVerifyStatus() {
      return new Promise((resolve, reject) => {
        request({
          url: `/api/report/v1.0/data/sql/f08eba8c-099b-41ec-ae46-ddacf6fb021b`,
          method: 'post',
          data: {
            indexCode: 'f08eba8c-099b-41ec-ae46-ddacf6fb021b',
            fundCode: this.fundCode
          }
        })
          .then((res) => {
            if (res.data.status === 0) {
              this.verifyStatus = res.data.data.length && res.data.data[0].STATUS
              console.log(this.baseInfo.VC_SOURCE, this.verifyStatus, '>>是否显示发起验证按钮')
              resolve()
            }
          })
          .catch((err) => {
            reject(err)
          })
      })
    },
    /**
     * @description 产品基本信息
     */
    handleFundInfo(val) {
      // 产品基本信息 赋值
      this.descTopData[0].value = val.FOUND_DATE || '-'
      this.descTopData[1].value = val.VC_FUND_MANAGER || '-'
      this.descTopData[2].value = val.VC_ADVISOR || ''
      this.descTopData[3].value = val.VC_FUND_MANAGER_NOMINAL || '-'
      this.descTopData[4].value = val.CITY || '-'
      // this.descTopData[5].value = val.VC_HONOR || ''
      this.descTopData[5].value = val.DIM_NME || '-'
      this.descTopData[6].value = val.VC_REGCODE || '-'
      this.descTopData[7].value = val.VC_STATUS || '-'
      //this.descTopData[8].value = this.filterStar(val.VC_FRATING)

      // 单位净值/累计净值/复权累计净值 赋值
      this.middleLeftData[1].value = val.F_NAV ? Number(val.F_NAV).toFixed(4) : '-'
      this.middleLeftData[2].value = val.F_ADDED_NAV ? Number(val.F_ADDED_NAV).toFixed(4) : '-'
      // source为IN时，不需要该字段
      if (val.VC_SOURCE === 'OUT') {
        this.middleLeftData[3].value = val.F_CUMULATIVE_NAV ? Number(val.F_CUMULATIVE_NAV).toFixed(4) : '-'
      }
      // 近三月/今年以来/一年收益率 赋值
      this.middleMiddleData[0].value = val.F_3M_RETURN ? (val.F_3M_RETURN * 100).toFixed(2) : '-'
      this.middleMiddleData[1].value = val.F_YTD_RETURN ? (val.F_YTD_RETURN * 100).toFixed(2) : '-'
      this.middleMiddleData[2].value = val.F_1Y_RETURN ? (val.F_1Y_RETURN * 100).toFixed(2) : '-'
      // 成立以来最大回撤 成立以来sharpe
      this.middleRightData[0].value = val.F_INCEP_MAX_RETRACEMENT ? (val.F_INCEP_MAX_RETRACEMENT * 100).toFixed(2) : '-'
      this.middleRightData[1].value = val.F_TOTAL_SHARP ? val.F_TOTAL_SHARP.toFixed(2) : '-'
      // 统计周期初始化
      this.formQuery.startDate = dateShortcutMap[this.formQuery.statistPeriod].onClick()[0] || ''
      this.formQuery.endDate = dateShortcutMap[this.formQuery.statistPeriod].onClick()[1] || ''
    },
    /**
     * @description 统计周期区间映射
     */
    handleDateChange(val) {
      if (!val) {
        this.disabledDate = true
        this.formQuery.startDate = ''
        this.formQuery.endDate = ''
        return
      }
      if (val === '7') {
        this.disabledDate = false
      } else if (val === '6') {
        this.disabledDate = true
        this.formQuery.startDate = this.baseInfo.FOUND_DATE || ''
        this.formQuery.endDate = new Date().getFullYear() + '-' + (new Date().getMonth() + 1) + '-' + new Date().getDate()
      } else {
        this.disabledDate = true
        this.formQuery.startDate = dateShortcutMap[val].onClick()[0] || ''
        this.formQuery.endDate = dateShortcutMap[val].onClick()[1] || ''
      }
    },
    /**
     * @description 获取业绩基准下拉
     */
    getKpiOptions() {
      return new Promise((resolve, reject) => {
        request({
          url: `/api/report/v1.0/data/sql/9d40fd1a-b804-4cfb-926f-c7f4174269c2`,
          method: 'post',
          data: {
            indexCode: '9d40fd1a-b804-4cfb-926f-c7f4174269c2'
          }
        })
          .then((res) => {
            if (res.data.status === 0) {
              const resultDim = res.data.data || []
              this.kpiStandardOpts = resultDim.map((item) => {
                return {
                  label: item.DIM_NME,
                  id: item.DIM_CDE,
                  checked: false
                }
              })
              this.formQuery.kpiCode = '000300'
              resolve()
            }
          })
          .catch((err) => {
            reject(err)
          })
      })
    },
    /**
     * @description 获取对比基准下拉
     */
    getContrasOptions() {
      return new Promise((resolve, reject) => {
        request({
          url: `/api/report/v1.0/data/sql/ecd8867c-64cc-4ebc-9070-04524b04b72c`,
          method: 'post',
          data: {
            indexCode: 'ecd8867c-64cc-4ebc-9070-04524b04b72c',
            fundCode: this.fundCode
          }
        })
          .then((res) => {
            if (res.data.status === 0) {
              const resultDim = res.data.data || []
              this.contrasStandardOpts = resultDim.map((item) => {
                return {
                  label: item.DIM_NME,
                  id: item.DIM_CDE,
                  checked: false,
                  defaultChecked: item.ISDEFAULT == '1' ? true : false
                }
              })
              this.formQuery.contrasCode = this.contrasStandardOpts.filter((item) => item.defaultChecked == true).map((item) => item.id)
              resolve()
            }
          })
          .catch((err) => {
            reject(err)
          })
      })
    },
    /**
     * @description 监听对比基准下拉
     */
    changeContrasCode(val) {
      if (val.length > 4) {
        this.$message({
          type: 'warning',
          message: '对比基准最多只能选四个'
        })
        this.formQuery.contrasCode.splice(-1)
      }
    },
    /**
     * @description 查询
     */
    handleSearch(status) {
      return new Promise((resolve, reject) => {
        if (status === 'ALL') {
          const params = {
            ...this.formQuery,
            fundCode: this.fundCode
          }
          // delete params.statistPeriod
          this.$emit('getparamssearcall', params)
          resolve()
        } else {
          const params = {
            ...this.formQuery,
            fundCode: this.fundCode
          }
          // delete params.statistPeriod
          this.$emit('getparams', params)
          resolve()
        }
      })
    },
    /**
     * @description 监听页面滚动吸顶效果
     */
    handleScroll() {
      const scrollTop = document.getElementById('appMain').scrollTop
      if (document.querySelector('.footer') && document.querySelector('.footer').offsetTop) {
        const offsetTop = document.querySelector('.footer').offsetTop
        this.whether = this.$store.state.setting.fromPlatForm ? false : scrollTop > offsetTop
      }
    },
    /**
     * @description 重置查询
     */
    reset() {
      for (const key in this.formQuery) {
        this.formQuery[key] = ''
      }
      this.formQuery.statistPeriod = '4'
      this.formQuery.startDate = dateShortcutMap[this.formQuery.statistPeriod].onClick()[0] || ''
      this.formQuery.endDate = dateShortcutMap[this.formQuery.statistPeriod].onClick()[1] || ''
      this.formQuery.kpiCode = '000300'
      this.formQuery.contrasCode = this.contrasStandardOpts.filter((item) => item.defaultChecked == true).map((item) => item.id)
    },
    jumpRoute(page) {
      if (page === 'XXYZSQ') {
        this.$router.push({
          path: '/xqhd/bzhxqgl/xxyzsq',
          query: {
            fundCode: this.fundCode,
            fundName: this.baseInfo.VC_FUNDNAME,
            flag: true
          }
        })
      } else if (page === 'custodian') {
        this.$store.commit('SET_FROMPAGEJUMP', true)
        let newObj = {
          company_id: this.currentList.COMPANY_ID,
          manager_name: this.currentList.VC_FUND_MANAGER_NOMINAL
        }
        this.$router.push({
          path: '/tqgl/glrxq',
          query: {managerList: newObj}
        })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.productinfo-dialog {
  ::v-deep .el-dialog {
    width: 100% !important;
  }
}

#product-info {
  ::v-deep .el-input__inner {
    color: #333 !important;
  }
}

.product-info-label {
  margin-left: 8px;
}

.detailTop {
  display: flex;
  flex-direction: column;
  padding: 0 20px;
  margin-bottom: 24px;

  .header {
    display: flex;
    padding: 20px 0;

    .product-info {
      margin-top: 5px;
      text-align: center;
      flex: 6;
      display: flex;
      flex-direction: column;

      .top {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;

        .name {
          color: #20212B;
          font-size: 24px;
          padding: 0 15px;
        }

        .status {
          color: #e03d3e;
          padding-bottom: 5px;
          padding-left: 5px;
        }
      }

      .bottom {
        flex: 1;
        display: flex;
        align-items: flex-start;
        justify-content: center;

        .time {
          padding-left: 10px;
          padding-top: 10px;
          font-size: 16px;
          color: #20212B;
        }
      }
    }

    .product-desc {
      padding: 15px 0 20px 30px;
      flex: 10;

      ::v-deep .el-descriptions-item__label,
      ::v-deep .el-descriptions-item__content {
        color: #20212B !important;
      }

      ::v-deep .el-descriptions__body {
        background-color: rgba(0, 0, 0, 0);
      }
    }
  }

  .base-info-content {
    display: flex;
    justify-content: space-between;
    border-top: 1px dashed #3f3f3f;
    border-bottom: 1px dashed #3f3f3f;
    padding: 20px 0;

    .left {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: space-around;
    }

    .middle {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: space-around;
    }

    .right {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: space-around;

      .value-right {
        font-size: 24px;
        color: #00d83d;
        text-align: right;
      }
    }

    .data-style {
      .label-zb {
        color: #20212B;
        text-align: right;
      }

      .value {
        font-size: 24px;
        color: #cc0000;
        text-align: right;
      }
    }
  }

  .footer {
    padding-top: 12px;

    ::v-deep .el-form-item__label {
      color: #20212B;
    }

    ::v-deep .el-form-item {
      margin-bottom: 0px !important;
    }

    .dbjz {
      ::v-deep .el-select .el-input--small {
        width: 210px !important;
      }

      ::v-deep .el-select .el-select__tags {
        max-width: 190px !important;
      }
    }
  }

  .icon-style {
    margin-bottom: 0px !important;
    font-size: 20px;
  }

  .isFixed {
    position: fixed;
    top: 92px;
    // left: 50px;
    z-index: 1000;
    // background-color: #fff2e7;
    background-color: whitesmoke;
    width: calc(100vw - 70px);
    padding: 10px 0;
    border-radius: 2px;
  }
}

::v-deep .el-form-item__label {
  color: #20212B !important;
}

::v-deep .el-input__inner {
  color: #20212B !important;
}
</style>

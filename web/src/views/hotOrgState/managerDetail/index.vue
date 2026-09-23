<template>
  <div class="company-page">

    <section class="section-1" :style="{ backgroundImage: `url(${headerBg})` }">
      <div class="section-1-content">
        <div class="header-info">
          <div class="title-wrapper">
            <img :src="titleIcon" alt="公司图标" class="title-icon" />
            <h1>{{ companyName }}</h1>
          </div>
          <p class="company-desc">{{ companyDescription }}</p>
          <div class="header-buttons">
            <div class="button-item" v-for="(btn, index) in headerButtons" :key="index">{{ btn }}</div>
          </div>
        </div>
      </div>
    </section>

    <section class="section-2">
      <div class="core-data">
        <div class="data-item" v-for="(item, index) in coreDataList" :key="index">
          <div class="data-value">{{ item.value }}</div>
          <div class="data-label">{{ item.label }}</div>
        </div>
      </div>
    </section>

    <section class="section-3">
      <h2 class="section-title">基本信息</h2>
      <div class="info-grid">
        <div class="info-item" v-for="(item, index) in basicInfoList" :key="index">
          <img :src="item.icon" alt="图标" class="info-icon" />
          <div class="info-content">
            <el-tooltip
              :content="item.value"
              placement="top"
              :open-delay="0"
            >
            <div class="info-value">{{ item.value }}</div>
            </el-tooltip>
            <div class="info-label">{{ item.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <section class="section-4" :style="{ backgroundImage: `url(${productsBg})` }">
      <h2 class="section-title4">旗下产品</h2>
      <div class="carousel-container">

        <button class="carousel-btn left-btn" @click="handlePrev">
          <i class="el-icon-arrow-left"></i>
        </button>

        <el-carousel
          ref="productCarousel"
          :interval="5000"
          arrow="never"
          indicator-position="none"
          class="product-carousel"
        >
          <el-carousel-item v-for="(page, pageIndex) in productPages" :key="pageIndex">
            <div class="carousel-page">
              <div class="product-card" v-for="(product, index) in page" :key="index">
                <div class="product-header">
                  <img :src="product.image" alt="产品图片" class="product-image" />
                  <el-tooltip
                    :content="product.name + '(' + product.code + ')'"
                    placement="top"
                    :open-delay="0"
                  >
                  <div class="product-name">{{ product.name }}({{ product.code }})</div>
                  </el-tooltip>
                </div>
                <div class="product-info">
                  <p>投资策略：{{ product.strategy }}</p>
                  <p>基金经理：{{ product.manager }}</p>
                  <p>成交日期：{{ product.date }}</p>
                  <p>运行状态：{{ product.status }}</p>
                </div>
                <button class="invite-btn"
                        :class="{ disabled: product.inviteStatus !== 0 }"
                        @click="handleInviteClick(product.code)"
                        :disabled="product.inviteStatus !== 0"
                >{{ product.inviteStatus == 0 ? '邀约' : '已合作' }}</button>
              </div>
            </div>
          </el-carousel-item>
        </el-carousel>

        <button class="carousel-btn right-btn" @click="handleNext">
          <i class="el-icon-arrow-right"></i>
        </button>
      </div>
    </section>

    <!-- 企业股东信息模块 -->
    <section class="section-6">
      <h2 class="section-title">企业股东信息</h2>
      <div class="shareholder-container">
        <div class="shareholder-table">
          <div class="table-header">
<!--            <div class="table-cell cell-1">股东类型中文描述</div>-->
            <div class="table-cell cell-2">股东名称</div>
            <div class="table-cell cell-3">股东证件号码</div>
            <div class="table-cell cell-4">出资比例</div>
          </div>
          <div class="table-body">
            <div class="table-row" v-for="(item, index) in shareholderList" :key="index">
<!--              <div class="table-cell cell-1">{{ item.shareholderType }}</div>-->
              <div class="table-cell cell-2">{{ item.shareholderName }}</div>
              <div class="table-cell cell-3">{{ item.idNumber }}</div>
              <div class="table-cell cell-4">{{ item.conRatio |toPercentage}}</div>
            </div>
            <div class="table-row empty-row" v-if="shareholderList.length === 0">
              <div class="table-cell empty-cell" colspan="3">暂无股东信息</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 企业经营异常信息模块 -->
    <section class="section-7">
      <h2 class="section-title">企业经营异常信息</h2>
      <div class="abnormal-container">
        <div class="abnormal-table">
          <div class="table-header">
            <div class="table-cell cell-1">列入经营异常名录原因</div>
            <div class="table-cell cell-2">列入经营异常名录日期</div>
            <div class="table-cell cell-3">列入经营异常名录做出决定机关</div>
          </div>
          <div class="table-body">
            <div class="table-row" v-for="(item, index) in abnormalList" :key="index">
              <div class="table-cell cell-1">{{ item.reason }}</div>
              <div class="table-cell cell-2">{{ item.date }}</div>
              <div class="table-cell cell-3">{{ item.department }}</div>
            </div>
            <div class="table-row empty-row" v-if="abnormalList.length === 0">
              <div class="table-cell empty-cell" colspan="3">暂无经营异常信息</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!--    <section class="section-5">
      <div class="section-5-content">
        <div class="idea-image-wrapper">
          <img :src="investmentIdeaImage" alt="投资理念" class="idea-image" />
        </div>
        <div class="idea-text">
          <h3>投资理念</h3>
          <p>{{ investmentIdeaText }}</p>
        </div>
        <div class="idea-image-wrapper">
          <img :src="integrityInfoImage" alt="诚信信息" class="idea-image" />
        </div>
        <div class="idea-text">
          <h3>诚信信息</h3>
          <p>{{ integrityInfoText }}</p>
        </div>
      </div>
    </section>-->
  </div>
</template>

<script>
import { Carousel, CarouselItem, Icon,Tooltip } from 'element-ui';
import request from '@/utils/request'
export default {
  components: {
    ElCarousel: Carousel,
    ElCarouselItem: CarouselItem,
    ElIcon: Icon, // 注册Icon组件
    ElTooltip: Tooltip
  },
  filters: {
    toPercentage(value) {
      return (value * 100).toFixed(2) + '%'; // 转换为百分比并保留两位小数
    }
  },
  data() {
    return {
      currentList:null,
      fundList:null,
      // 图片路径变量
      headerBg: require('./img/管理人背景.png'),
      titleIcon: require('./img/管理人图标.png'),
      productsBg: require('./img/旗下产品背景.png'),
      investmentIdeaImage: require('./img/投资理念.png'),
      integrityInfoImage: require('./img/诚信信息.png'),

      // 公司基本信息
      companyName: '',
      companyDescription: '',//公司简介
      headerButtons: [],

      // 核心数据
      coreDataList: [
        { label: '基金数量（只）', value: '' },
        { label: '管理规模（亿元）', value: '' },
        { label: '员工人数（人）', value: '' },
        { label: '注册资本（万）', value: '' },
        { label: '实缴资本（万）', value: '' }
      ],

      // 基本信息
      basicInfoList: [
        { label: '公司类型', value: '', icon: require('./img/基本信息-公司类型.png') },
        { label: '业务类型', value: '', icon: require('./img/基本信息-业务类型.png') },
        { label: '管理基金主要类别', value: '', icon: require('./img/基本信息-企业性质.png') },
        //{ label: '备案状态', value: '', icon: require('./img/基本信息-备案状态.png') },
        { label: '备案编码', value: '', icon: require('./img/基本信息-备案编码.png') },
        { label: '组织机构编码', value: '', icon: require('./img/基本信息-组织机构编码.png') },
        { label: '登记日期', value: '', icon: require('./img/基本信息-登记日期.png') },
        { label: '注册日期', value: '', icon: require('./img/基本信息-注册日期.png') },
        { label: '实际控制人', value: '', icon: require('./img/基本信息-实际控制人.png') },
        { label: '法定代表人/执行事务合伙人(委派代表)', value: '', icon: require('./img/基本信息-法定代表人.png') },
        { label: '注册城市', value: '', icon: require('./img/基本信息-注册城市.png') },
        { label: '办公城市', value: '', icon: require('./img/基本信息-注册城市.png') },
        { label: '网址', value: '', icon: require('./img/基本信息-网址.png') }
      ],

      // 旗下产品
      productsList: [],

      // 投资理念与诚信信息
      investmentIdeaText: '因地制宜，不断完善适应金融发展环境，坐拥东北，俯瞰国内，依托全球。',
      integrityInfoText: '慧智致力于肃清金融行业的乱象，力争做金融行业的标杆和良心企业。',

      // 企业股东信息
      shareholderList: [],

      // 企业经营异常信息
      abnormalList: []
    };
  },
  watch: {
    '$route.query.managerList': {
      handler(newVal) {
        if (this.$store.getters.fromPageJump) {
          if (this.$route.query && this.$route.query.managerList) {
            const data = newVal.reg_code
            const credit_code = newVal.credit_code
            this.getCompData(data)
            this.getFundData(data)
            this.getShareholderData(credit_code);
            this.getAbnormalData(credit_code);
          }
        }
      },
      deep: true,
      immediate: true
    }
  },
  computed: {
    productPages() {
      const pageSize = 3; // 每页3个产品
      const pages = [];
      for (let i = 0; i < this.productsList.length; i += pageSize) {
        pages.push(this.productsList.slice(i, i + pageSize));
      }
      return pages;
    }
  },
  mounted() {

  },
  methods: {
    handlePrev() {
      this.$refs.productCarousel.prev();
    },
    handleNext() {
      this.$refs.productCarousel.next();
    },
    getCompData(data) {
      const params = {
        indexCode: 'bcbb01b7-c5c2-45b2-a3e6-a8faa0c930cb'
      }
      params.reg_code = data || ''
      request({
        url: `/api/report/v1.0/data/sql/${params.indexCode}`,
        method: 'post',
        data: params
      }).then(res => {
        if (res.data.status === 0) {
          const baseInfo = res.data.data || []
          this.currentList = baseInfo[0] || {}
          console.log(this.currentList)
          this.companyName = this.currentList.full_name_cn || '-'  //名称
          this.coreDataList[0].value = this.currentList.fund_count || '-' //基金数量
          this.coreDataList[1].value = this.currentList.manage_scale || '-' //资产规模
          this.coreDataList[2].value = this.currentList.emp_number || '-' //员工人数
          this.coreDataList[3].value = this.currentList.reg_capital || '-' //注册资本
          this.coreDataList[4].value = this.currentList.paid_capital || '-' //实缴资本

          this.basicInfoList[0].value = this.currentList.inst_type || '-' //公司类型
          this.basicInfoList[1].value = this.currentList.service_type || '-' //公司状态&业务类型

          this.basicInfoList[2].value = this.currentList.main_fund_type || '-' //企业性质&管理基金主要类别
          //this.basicInfoList[3].value = this.currentList.reg_code != null ? '已备案' : '-' //备案状态
          //this.headerButtons = this.currentList.reg_code != null ? ["已备案"] : [] //备案状态
          this.basicInfoList[3].value = this.currentList.reg_code || '-' //备案编码
          this.basicInfoList[4].value = this.currentList.org_code || '-' //组织机构编码
          this.basicInfoList[5].value = this.currentList.record_date || '-' //登记日期
          this.basicInfoList[6].value = this.currentList.reg_date || '-' //注册日期
          this.basicInfoList[7].value = this.currentList.actual_controller || '-' //实际控制人
          this.basicInfoList[8].value = this.currentList.legal_representative || '-' //法定代表人
          this.basicInfoList[9].value = this.currentList.reg_address || '-' //注册城市
          this.basicInfoList[10].value = this.currentList.office_address || '-' //办公城市
          this.basicInfoList[11].value = this.currentList.website || '-' //网址
          this.companyDescription = this.currentList.vc_description || '' //公司简介
        }
      })
    },
    getFundData(data) {
      const params = {
        indexCode: '0be6e903-f772-459b-8dbd-2a2d4b83f621'
      }
      params.reg_code = data || ''
      request({
        url: `/api/report/v1.0/data/sql/${params.indexCode}`,
        method: 'post',
        data: params
      }).then(res => {
        if (res.data.status === 0) {
          var baseInfo = res.data.data || [];
          this.productsList = baseInfo.map(function(item) {
            return {
              name: item.fundName || '-',
              code: item.fundCode || '-',
              strategy: item.vc_clname || '-',
              manager: item.fund_manager || '-',
              date: item.d_create_date || '-',
              status: item.vc_is_end || '-',
              inviteStatus: item.vc_isyy || '-',
              image: require('./img/旗下产品-图标.png')
            };
          });
        }
      })
    },
    handleInviteClick(fundCode) {
      if (!fundCode || fundCode === '-') {
        this.$message.warning('产品代码为空，无法跳转');
        return;
      }
      this.$router.push({
        path: '/tqgl/ceshi/ceshi',
        query: { fundCode: fundCode }
      });
    },
    getShareholderData(credit_code) {
      const requestDTO = {
        BODY: { UNIF_SOCL_CRDT_ID: credit_code } //传参 统一社会信用代码
      };
      request({
        url: '/api/gfecif/shareholder',
        method: 'post',
        data: requestDTO
      }).then(res => {
        if (res && res.data) {
          const shareholderResponse = res.data;
          // 适配后端返回
          this.shareholderList = shareholderResponse.SHR_HLDR.map(item => ({
            shareholderType: item.SHRHLDR_TYPE_DESC || '-',
            shareholderName: item.SHRHLDR_NAME || '-',
            idNumber: item.CERT_NO || '-',
            conRatio: item.CPTL_CTRB_TATIO || '-'
          }));
        }
      }).catch(err => {
        console.error('获取股东信息失败：', err);
        this.shareholderList = [];
      });
    },

    getAbnormalData(credit_code) {
      const requestDTO = {
        BODY: { UNIF_SOCL_CRDT_ID: credit_code }//传参 统一社会信用代码
      };
      request({
        url: '/api/gfecif/abnormal-info',
        method: 'post',
        data: requestDTO
      }).then(res => {
        if (res && res.data) {
          const abnormalResponse = res.data;
          // 适配小写首字母字段
          this.abnormalList = abnormalResponse.ENTER_ABNORMAL_INFO.map(item => ({
            reason: item.ENTER_ABNORMAL_CAUSE || '-',
            date: item.ENTER_ABNORMAL_DATE || '-',
            department: item.ENTER_VERDICT_ORGAN || '-'
          }));
        }
      }).catch(err => {
        console.error('获取经营异常信息失败：', err);
        this.abnormalList = [];
      });
    }
  }
};
</script>

<style scoped>

.section-title {
  text-align: center;
  margin-bottom: 30px;
  font-size: 24px;
  color: #333;
}
.section-title4 {
  text-align: center;
  margin-bottom: 30px;
  font-size: 24px;
  color: #fff;
}


.section-1 {
  width: 100%;
  height: 500px;
  background-size: cover;
  background-position: center;
  position: relative;
  color: #000;
}

.section-1-content {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: left;
}

.header-info {
  width: 50%;
  padding: 90px 40px 60px 50px;
  text-align: right;
}

.title-wrapper {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-bottom: 20px;
}

.title-icon {
  width: 30px;
  height: 30px;
  margin-right: 10px;
}

.company-desc {
  margin-bottom: 30px;
  padding-left:150px;
  line-height: 1.6;
  text-align: left;
}

.header-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
}

.button-item {
  padding: 3px 15px;
  background: linear-gradient(to right, #F5D7BC, #E0B794);
  border-radius: 4px;
  cursor: pointer;
  color: #612D10;
}

.section-2 {
  padding: 50px 0;
  background-color: #fff;
}

.core-data {
  width: 70%;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  text-align: center;
}

.data-item {
  flex: 1;
}

.data-value {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.data-label {
  color: #666;
}

.section-3 {
  padding: 50px 0;
  background-color: #fff;
}

.info-grid {
  width: 70%;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.info-item {
  display: flex;
  align-items: center;
  padding: 22px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.info-icon {
  width: 50px;
  height: 50px;
  margin-right: 15px;
}

.info-label {
  color: #666;
  font-size: 12px;

}

.info-value {
  color: #000000;
  white-space: nowrap;
  overflow: hidden;
  font-size: 16px;
  text-overflow: ellipsis;
  max-width: 200px;
  margin-bottom: 5px;
}

.section-4 {
  padding: 50px 0;
  background-size: cover;
  background-position: center;
  position: relative;
}

.carousel-container {
  width: 100%;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.carousel-btn {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.8);
  border: none;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #333;
  z-index: 10;
}

.left-btn {
  position: absolute;
  left: 5%;
}

.right-btn {
  position: absolute;
  right: 5%;
}

.product-carousel {
  width: 70%;
  margin: 0 auto;
}

.carousel-page {
  display: flex;
  gap: 20px;
  width: 100%;
  padding: 0 10px;
}

.product-card {
  width: 31%;
  height: 300px;
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
}

.product-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.product-image {
  width: 24px;
  height: 24px;
  margin-right: 10px;
}

.product-name {
  font-weight: bold;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 16px;
  cursor: pointer; /* 手型提示 */
  max-width: 280px;
}

.product-info {
  margin-bottom: 20px;
  flex-grow: 1;
}

.product-info p {
  margin-bottom: 12px;
  font-size: 14px;
  color: #666;
}

.invite-btn {
  width: 100%;
  padding: 10px 0;
  border: none;
  border-radius: 4px;
  background: linear-gradient(to right, #F5D7BC, #E0B794);
  color: #612D10;
  cursor: pointer;
  margin-top: auto;
}

/* 企业股东信息样式 */
.section-6 {
  padding: 50px 0;
  background-color: #fff;
}

.shareholder-container {
  width: 70%;
  margin: 0 auto;
}

.shareholder-table {
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

/* 企业经营异常信息样式 */
.section-7 {
  padding: 50px 0;
  background-color: #fff;
}

.abnormal-container {
  width: 70%;
  margin: 0 auto;
}

.abnormal-table {
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

/*  固定列宽确保对齐 */
.table-header {
  display: flex;
  background: linear-gradient(to right, #F5f6f9, #F5f6f9);
  color: #612D10;
  font-weight: bold;
  width: 100%;
}

.table-body {
  width: 100%;
}

.table-row {
  display: flex;
  width: 100%;
  border-bottom: 1px solid #f0f0f0;
}

.table-row:last-child {
  border-bottom: none;
}

/* 股东信息表格列宽 */
.shareholder-table .cell-1 {
  width: 20%;
  flex: none;
}
.shareholder-table .cell-2 {
  width: 45%;
  flex: none;
}
.shareholder-table .cell-3 {
  width: 40%;
  flex: none;
}
.shareholder-table .cell-4 {
  width: 15%;
  flex: none;
}

/* 经营异常信息表格列宽 */
.abnormal-table .cell-1 {
  width: 50%;
  flex: none;
}
.abnormal-table .cell-2 {
  width: 20%;
  flex: none;
}
.abnormal-table .cell-3 {
  width: 30%;
  flex: none;
}

/* 单元格通用样式 */
.table-cell {
  padding: 15px;
  text-align: left;
  border-right: 1px solid #f0f0f0;
  word-break: break-word;
  box-sizing: border-box;
}

.table-cell:last-child {
  border-right: none;
}

.table-body .table-row:hover {
  background-color: #f8f8f8;
}

.empty-row {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
}

.empty-cell {
  text-align: center;
  color: #999;
  width: 100%;
  border-right: none !important;
}

.section-5 {
  padding: 50px 0;
  background-color: #fff;
}

.section-5-content {
  width: 70%;
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: 30px;
}

.idea-image-wrapper {
  flex: 1;
  display: flex;
  justify-content: center;
}

.idea-image {
  width: 180px;
  height: 120px;
  object-fit: cover;
  border-radius: 4px;
}

.idea-text {
  flex: 2;
}

.idea-text h3 {
  margin-bottom: 15px;
  color: #333;
  font-size: 18px;
}

.idea-text p {
  color: #666;
  line-height: 1.6;
  font-size: 14px;
}
</style>

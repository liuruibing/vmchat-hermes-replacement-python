<template>
  <div class="barometer">
    <div style="height: 100%;width: 100%">
      <div :style="{ backgroundImage: 'url(' + activeImg + ')'}" class="image-container">
        <span class="content-date-content">{{ D_DATE }}</span>
        <span class="content-date-title">
          <img :src="imgLabelLeft"/>
        </span>
        <span class="content-logo">
          <img :src="imgLabelRight"/>
        </span>
        <span :style="{ backgroundImage: 'url(' + activeLeft + ')'}" class="image-container-left">
          <div style="position: relative;  height: 100%;width: 100%;">
            <span :class="ZSSMColor ? 'content-value-up' : 'content-value-down'" class="content-left-value">{{
              ZSSMSYL
            }}</span>
            <span class="content-left-str">{{ ZSSM }}</span>
          </div>
        </span>
        <span :style="{ backgroundImage: 'url(' + activeRight + ')'}" class="image-container-right">
          <div style="position: relative;  height: 100%;width: 100%;">
            <span :class="HSColor ? 'content-value-up' : 'content-value-down'" class="content-right-value">{{
              HSSYL
            }}</span>
            <span class="content-right-str">{{ HS }}</span>
          </div>
        </span>
        <!--        <span :class="ZSSMColor ? 'content-value-up' : 'content-value-down'" class="content-left-value">{{ ZSSMSYL }}</span>-->
        <!--        <span :class="HSColor ? 'content-value-up' : 'content-value-down'" class="content-right-value">{{ HSSYL }}</span>-->
        <!--        <span class="content-left-str">{{ ZSSM }}</span>-->
        <!--        <span class="content-right-str">{{ HS }}</span>-->
      </div>
    </div>
  </div>
</template>

<script>
import commApi from '@/api/common'
import rain from '@/assets/img/rain.png'
import rainSun from '@/assets/img/rainSun.png'
import sunny from '@/assets/img/sunny.png'
import sunRain from '@/assets/img/sunRain.png'
import firstLineLabelLeft from '@/assets/img/firstLineLabelLeft.png'
import firstLineLabelRight from '@/assets/img/firstLineLabelRight.png'
import firstLineUp from '@/assets/img/firstLineUp.png'
import firstLineDown from '@/assets/img/firstLineDown.png'

export default {
  name: 'Barometer',
  data() {
    return {
      activeImg: sunny,
      activeLeft: firstLineUp,
      activeRight: firstLineUp,
      imgLabelLeft: firstLineLabelLeft,
      imgLabelRight: firstLineLabelRight,
      HSSYL: '-',
      HS: '-',
      ZSSM: '-',
      ZSSMSYL: '-',
      D_DATE: '数据来源：广发证券（截止日期：-）',
      HSColor: true,
      ZSSMColor: true
    }
  },
  mounted() {
    this.init()
  },
  methods: {
    init() {
      this.getBarometerInfo()
    },
    getBarometerInfo() {
      const params = {}
      params.indexCode = '37c53a7d-a0c8-4b95-aaf2-5692bd92233d'
      commApi.getDataBysqlCode(params).then(res => {
        const { status, data } = res.data
        if (status == 0) {
          if (data && data.length > 0) {
            this.HS = data[0].HS || '-'
            const HSSYL = data[0].HSSYL || '-'
            this.ZSSM = data[0].ZSSM || '-'
            const ZSSMSYL = data[0].ZSSMSYL || '-'
            const D_DATE = data[0].D_DATE || '-'
            this.D_DATE = `数据来源：广发证券（截止日期：${D_DATE}）`
            if ((ZSSMSYL == '-' || ZSSMSYL >= 0) && (HSSYL == '-' || HSSYL >= 0)) {
              this.activeImg = sunny
              this.activeLeft = firstLineUp
              this.activeRight = firstLineUp
            } else if ((ZSSMSYL == '-' || ZSSMSYL >= 0) && (HSSYL == '-' || HSSYL < 0)) {
              this.activeImg = sunRain
              this.activeLeft = firstLineUp
              this.activeRight = firstLineDown
            } else if ((ZSSMSYL != '-' && ZSSMSYL < 0) && (HSSYL != '-' && HSSYL < 0)) {
              this.activeImg = rain
              this.activeLeft = firstLineDown
              this.activeRight = firstLineDown
            } else if ((ZSSMSYL != '-' && ZSSMSYL < 0) && (HSSYL == '-' || HSSYL > 0)) {
              this.activeImg = rainSun
              this.activeLeft = firstLineDown
              this.activeRight = firstLineUp
            } else {
              this.activeImg = sunny
              this.activeLeft = firstLineUp
              this.activeRight = firstLineUp
            }
            if (ZSSMSYL == '-' || ZSSMSYL >= 0) {
              this.ZSSMColor = true
            } else {
              this.ZSSMColor = false
            }
            if (HSSYL == '-' || HSSYL >= 0) {
              this.HSColor = true
            } else {
              this.HSColor = false
            }
            this.HSSYL = this.valueToStr(HSSYL)
            this.ZSSMSYL = this.valueToStr(ZSSMSYL)
          } else {
            this.ZSSMColor = true
            this.HSColor = true
            this.activeImg = sunny
            this.HS = '-'
            this.HSSYL = '-'
            this.ZSSM = '-'
            this.ZSSMSYL = '-'
            this.D_DATE = '数据来源：广发证券（截止日期：-）'
          }
        } else {
          this.ZSSMColor = true
          this.HSColor = true
          this.activeImg = sunny
          this.HS = '-'
          this.HSSYL = '-'
          this.ZSSM = '-'
          this.D_DATE = '数据来源：广发证券（截止日期：-）'
        }
      }).catch(err => {
        this.ZSSMColor = true
        this.HSColor = true
        this.HS = '-'
        this.HSSYL = '-'
        this.ZSSM = '-'
        this.ZSSMSYL = '-'
        this.D_DATE = '数据来源：广发证券（截止日期：-）'
        this.activeImg = sunny
        this.activeLeft = firstLineUp
        this.activeRight = firstLineUp
      })
    },
    valueToStr(val) {
      if (val == '') {
        return '-'
      }
      if (!isNaN(val)) {
        return Number((val * 100).toFixed(2)) + '%'
      } else {
        return '-'
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.barometer {
  height: 229px;
}

.content-value-up {
  color: #fe8623;
  font-weight: 600;
  font-size: 14px;
}

.content-value-down {
  color: #1078d5;
  font-size: 14px;
  font-weight: 600;
}

.image-container {
  position: relative;
  height: 229px;
  background-repeat: no-repeat;
  background-position: center;
  background-size: 100% 100%;
}

.image-container-left {
  position: absolute;
  bottom: 0px;
  left: 5%;
  display: inline-block;
  height: 137px;
  width: 186px;
  background-repeat: no-repeat;
  background-position: center;
  background-size: 100% 100%;
}

.image-container-right {
  position: absolute;
  bottom: 0px;
  right: 5%;
  display: inline-block;
  height: 137px;
  width: 186px;
  background-repeat: no-repeat;
  background-position: center;
  background-size: 100% 100%;
}

.content-date-content {
  position: absolute;
  top: 65px;
  left: 5%;
}

.content-date-title {
  position: absolute;
  top: 30px;
  left: 5%;
}

.content-logo {
  position: absolute;;
  top: 30px;
  right: 5%;
}

.content-left-value {
  position: absolute;
  display: inline-block;
  width: 80px;
  text-align: center;
  top: 65px;
  left: 53px
}

.content-right-value {
  position: absolute;
  display: inline-block;
  width: 80px;
  top: 65px;
  left: 53px;
  text-align: center;
}

.content-left-str {
  position: absolute;
  top: 108px;
  font-size: 14px;
  font-weight: 600;
  left: 52px;
}

.content-right-str {
  position: absolute;
  top: 108px;
  left: 52px;
  font-size: 14px;
  font-weight: 600;
}
</style>

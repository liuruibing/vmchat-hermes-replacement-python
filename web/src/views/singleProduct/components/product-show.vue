<template>
  <div class="product-show">
    <iframeModule :iframe-data="iframeData" :id="id"></iframeModule>
    <div v-if="coverDiv" class="cover-div" @click="handleCoverDiv"></div>
  </div>
</template>
<script>
import iframeModule from './iframe'
import { getToken } from '@/utils/auth'
export default {
  name: 'ProductShow',
  components: {
    iframeModule
  },
  props: {
    coverDiv: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      searchQuery: null,
      iframeData: {
        src: ''
      },
      id: 'J_iframe_id_product_show'
    }
  },
  methods: {
    /**
     * @desc 更改遮罩层状态
     */
    handleCoverDiv() {
      this.$emit('uploadCover', false)
    },
    file_vmrisk_src(templateCode, startDate, endDate, fundCode, kpiCode, contrasCode) {
      return (
        process.env.BASE_API +
        '/rest/report/interview.do?templateCode=' +
        templateCode +
        '&startDate=' +
        startDate +
        '&endDate=' +
        endDate +
        '&fundCode=' +
        fundCode +
        '&kpiCode=' +
        kpiCode +
        '&contrasCode=' +
        contrasCode +
        '&token=' +
        encodeURIComponent(getToken()) +
        '&autoRun=false&ajaxRun=true&showParam=true&showCondition=false&markFlag=false&srcSuffix=' +
        process.env.BASE_API +
        '&time=' +
        new Date().getTime()
      )
    },
    /**
     * @desc 设置iframe标签src
     */
    fun_iframeSrc() {
      var self = this
      self.iframeData.src = this.file_vmrisk_src(
        'b8b0547d-23d5-4150-8308-68d50eee81a8',
        this.searchQuery.startDate,
        this.searchQuery.endDate,
        this.searchQuery.fundCode,
        this.searchQuery.kpiCode,
        this.searchQuery.contrasCode,
        '',
        '',
        '',
        '',
        ''
      )
    }
  }
}
</script>
<style lang="scss" scoped>
.product-show {
  position: relative;
  height: 2900px;
  .cover-div {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
  }
}
</style>

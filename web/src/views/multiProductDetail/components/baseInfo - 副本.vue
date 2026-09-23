<template>
  <div class="base-info">
    <iframeModule :iframeData="iframeData" :id="id"></iframeModule>
    <div v-if="coverDiv" class="cover-div" @click="handleCoverDiv"></div>
  </div>
</template>
<script>
import iframeModule from './iframe'
import fun from '@/filters/common'
export default {
  name: 'baseInfo',
  components: {
    iframeModule
  },
  props: {
    formQuery: {
      type: Object,
      default: () => {}
    },
    coverDiv: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      //iframe链接
      iframeData: {
        src: ''
      },
      //iframe id
      id: 'J_iframe_id_base_info'
    }
  },
  mounted() {},
  methods: {
    /**
     * @desc 更改遮罩层状态
     */
    handleCoverDiv() {
      this.$emit('uploadCover', false)
    },
    /**
     * @desc 设置iframe标签src
     */
    fun_iframeSrc() {
      // let beginDate = "";
      // let endDate = "";
      // if (this.formQuery.date && this.formQuery.date.length) {
      //   beginDate = this.formQuery.date[0];
      //   endDate = this.formQuery.date[1];
      // }
      let self = this
      self.iframeData.src = fun.file_vmremark_src(
        'fa904bb2-6c85-47ae-bdff-db6f4ed570c0',
        this.formQuery.startDate,
        this.formQuery.endDate,
        this.formQuery.productCodes,
        this.formQuery.dbjz.join(','),
        this.formQuery.kpiCode,
      )
    },
    /**
     * @desc 初始化数据
     */
    initData() {
      this.fun_iframeSrc()
    }
  }
}
</script>
<style lang="scss" scoped>
.base-info {
  // height: calc(100vh - 274px);

  div:first-child {
    padding-bottom: 0px !important;
  }

  .cover-div {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
  }
}
</style>

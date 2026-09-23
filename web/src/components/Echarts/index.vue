<template>
  <div class="echarts">
    <div ref="pubEchart" :id="$attrs.id" :style="$attrs.style" />
  </div>
</template>
<script>
import * as echarts from 'echarts'
import ResizeObserver from 'resize-observer-polyfill'
export default {
  props: {
    options: {
      type: Object,
      default: () => {
        return {}
      }
    },
    resizeDom: {
      type: String,
      default: ''
    },
    renderer: {
      type: String,
      default: 'canvas'
    },
    eventParam: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      myChart: null,
      EchartsObj: null,
      observer: null,
      ischange: false
    }
  },
  computed: {
    echartsOption() {
      let val = this.options
      val.textStyle = {
        fontSize: '14'
      }
      return val
    }
  },
  watch: {
    targetNodeWidth() {
      this.resize()
    },
    options: {
      handler() {
        this.reload(this.echartsOption)
      },
      deep: true
    }
  },
  created() {
    this.$nextTick(() => {
      this.loadChart()
    })
  },
  mounted() {
    this.$nextTick(() => {
      this._chartResize(this.getChart())
      this.resizeDom && this.domRize()
    })
  },
  beforeDestroy() {
    if (this.observer) {
      this.observer.disconnect()
    }
  },
  methods: {
    domRize() {
      let ele = document.getElementById(this.$attrs.id)
      if (!ele) {
        return
      }
      let targetNode = document.getElementById(this.$attrs.id).parentNode
      this.observer = new ResizeObserver(() => {
        this.resize()
      })
      this.observer.observe(targetNode)
    },
    resize() {
      let ele = document.getElementById(this.$attrs.id)
      if (!ele) {
        return
      }
      this.myChart.resize()
    },
    _chartResize(instance) {
      const _resize = _.debounce(() => {
        this.$nextTick(() => instance && instance.resize())
      })
      window.addEventListener('resize', _resize)
      this.$once('hook:beforeDestroy', () => {
        window.removeEventListener('resize', _resize)
      })
    },
    reload(options) {
      if (!this.myChart) return
      this.myChart.clear()
      this.myChart.setOption(options, true)
    },
    loadChart() {
      if (document.getElementById(this.$attrs.id)) {
        this.myChart = echarts.init(document.getElementById(this.$attrs.id), null, {
          renderer: this.renderer
        })
        this.myChart.setOption(this.echartsOption, true)
        if (this.eventParam) {
          let { type, param } = this.eventParam
          this.myChart[type || 'on'](...param)
        }
      }
    },
    getChart() {
      return this.myChart
    }
  }
}
</script>

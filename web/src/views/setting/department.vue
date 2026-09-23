<template>
  <div style="height: 100%; position: relative;">
    <iframeModule  :iframeData = "iframeData" :id="uniqueId"></iframeModule>
    <ProductSelectInput
      ref="productSelect"
      v-model="product"
      placeholder="请选择产品"
      size="small"
      @select="handleProductSelect"
      @clear="handleProductClear"
      :style="floatStyle"
      id="vueFundSelect"
    />
  </div>
</template>

<script>
import echarts from 'echarts'
import iframeModule from '@/components/iframe'
import { getToken } from '@/utils/auth'
import ProductSelectInput from '@/components/productSelector/ProductSelectInput'

export default {
  name: "department",
  components: {
    iframeModule,
    ProductSelectInput
  },
  data() {
    return {
      product: null,
      iframeData: { src: '' },
      baseApi: '',
      uniqueId: this.generateUniqueId(),
      floatStyle: {
        position: 'absolute',
        zIndex: 9999,
        display: 'none',
        top: '0px',
        left: '0px',
        background: '#fff',
        border: '1px solid #eee',
        padding: '0px'
      }
    }
  },
  beforeRouteLeave(to, from, next) {
    // 路由切换时强制隐藏，且不保留任何显示状态
    this.floatStyle = {
      ...this.floatStyle,
      display: 'none' // 强制隐藏
    };
    this.product = null; // 清空选中值
    next();
  },
  mounted() {
    window.addEventListener('message', this.handleIframeMessage);
    this.baseApi = process.env.BASE_API;
    this.fun_iframeSrc();
  },
  beforeDestroy() {
    window.removeEventListener('message', this.handleIframeMessage);
  },
  methods: {
    generateUniqueId() {
      return 'iframe-' + Math.random().toString(36).substring(2, 15);
    },
    handleIframeMessage(msg) {
      const data = msg.data;
      if (!data) return;
      if (data.action === 'INFO_JSP') {
        if (data.payload && data.payload.type === '1' && data.payload.msg && data.payload.msg.path) {
          this.$router.push({ path: data.payload.msg.path });
        }
      }
      if (data.action === 'SET_FLOAT_POS') {
        this.floatStyle = {
          position: 'absolute',
          zIndex: 9999,
          display: data.payload.show ? 'block' : 'none',
          top: `${data.payload.top}px`,
          left: `${data.payload.left}px`,
          background: '#fff',
          border: '1px solid #eee',
          padding: '0px'
        };
        this.product = null
        if (data.payload.show && this.$refs.productSelect) {
          this.$nextTick(() => {
            const input = this.$refs.productSelect.$el.querySelector('input');
            input && input.focus();
          });
        }
      }
    },
    // 向JSP传选中值
    handleProductSelect(product) {
      if (!product) return;
      const formatProduct = {
        VC_FUNDCODE: product.VC_FUNDCODE || product.fundCode,
        VC_FUNDNAME: product.VC_FUNDNAME || product.fundName
      };
      const sendData = {
        action: 'INFO_FOF',
        payload: {
          type: '3',
          selectList: [formatProduct]
        }
      };
      const iframe = document.getElementById(this.uniqueId);
      if (iframe && iframe.contentWindow) {
        iframe.contentWindow.postMessage(sendData, '*');
      }
    },
    // 清空选择
    handleProductClear() {
      this.product = null;
      const iframe = document.getElementById(this.uniqueId);
      if (iframe && iframe.contentWindow) {
        iframe.contentWindow.postMessage({
          action: 'INFO_FOF',
          payload: { type: '3', selectList: [] }
        }, '*');
      }
    },
    fun_iframeSrc() {
      let path = this.$route.path;
      if (path.indexOf('jspPage=') != -1) {
        path = path.split('jspPage=')[1];
        this.iframeData.src = this.baseApi + path + '?token=' + encodeURIComponent(getToken());
      }
    }
  }
}
</script>

<style scoped>
::v-deep #vueFundSelect {
  box-sizing: border-box !important;
  z-index: 9999 !important;
}
</style>

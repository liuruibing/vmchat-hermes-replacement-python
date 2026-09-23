<template>

  <div style="height: 100%;">

    <iframeModule  :iframeData = "iframeData" id=""></iframeModule>
    <product-selector
      :dialog-visible="productSelectorVisible"
      :select-list="selectList"
      :show-tree-key-array="showTreeKeyArray"
      :tree-data="treeData"
      default-checked-keys="sycp"
      @closedialog="handleDialogClosed"
      @submitdialog="handleSubmitClick"
    ></product-selector>
  </div>
</template>

<script>
  import echarts from 'echarts'
  import iframeModule from '@/components/iframe'
  import fun from '@/filters/common'
  import {  getToken } from '@/utils/auth'
  import productSelector from '@/components/productSelector'
  export default {
    name: "department",
    components: {
       iframeModule,
      productSelector
    },
    data() {

      return {
        // 选择产品弹窗
        productSelectorVisible: false,
        treeData: [
          {
            label: '市场私募',
            id: 'scsm'
          },
          {
            label: '管理人旗下产品',
            id: 'glrqxcp'
          },
          {
            label: '广发托管/外包',
            id: 'zstgwb'
          },
          {
            label: '我的组合',
            id: 'wdzh'
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
        showTreeKeyArray: ['私有产品'],
        selectList: [],
        iframeData:{  //iframe链接
          src:'',
        },
        baseApi:'',//页面根地址
      }
    },
    mounted() {
      window.addEventListener('message', (msg) => {
        if (msg.data && msg.data.action == 'INFO_JSP') {
          if (msg.data.payload && msg.data.payload.type && msg.data.payload.type == '1' && msg.data.payload.msg && msg.data.payload.msg.path) {
            this.$router.push({path: msg.data.payload.msg.path})
          }
          if (msg.data.payload && msg.data.payload.type && msg.data.payload.type == '20') {
            this.openFundListDialog()
          }
        }
      })
      var self = this;

      //页面根路径
      self.baseApi = process.env.BASE_API;

      //调用设置明细
      self.fun_iframeSrc();

    },

    methods: {
      openFundListDialog() {
        this.productSelectorVisible = true
      },
      handleDialogClosed() {
        this.productSelectorVisible = false
      },
      handleSubmitClick(arr) {
        this.productSelectorVisible = false
        this.selectList = arr
        const iframes = document.querySelectorAll('iframe');

        iframes.forEach(iframe => {
          // 使用 postMessage 向 iframe 发送消息
          iframe.contentWindow.postMessage({
            action: 'INFO_FOF',
            payload: {type: '3', selectList: this.selectList}
          }, '*')
        });
      },
      //iframe链接地址
      fun_iframeSrc(){
        let self = this;
        let path = this.$route.path;
        if(path.indexOf('jspPage=') != -1){
          path = path.split('jspPage=')[1]
          // self.iframeData.src =  self.baseApi + path + '&token=' + encodeURIComponent(getToken());
          self.iframeData.src =  self.baseApi + path + '?token=' + encodeURIComponent(getToken());
          // self.iframeData.src =  self.baseApi + path
        }
      },

    }
  }


</script>

<style scoped>



</style>

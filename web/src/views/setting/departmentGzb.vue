<template>

  <div style="height: 100%;">
    <iframeModule  :iframeData = "iframeData" id=""></iframeModule>
  </div>
</template>

<script>
  import echarts from 'echarts'
  import iframeModule from '@/components/iframe'
  import fun from '@/filters/common'
  import {  getToken } from '@/utils/auth'
  export default {
    name: "department",
    components: {
       iframeModule
    },
    data() {

      return {

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
          if (msg.data.payload && msg.data.payload.type && msg.data.payload.type == '2') {
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

<template>
  <div style="display: none"/>
</template>
<script>
import qs from 'qs'

export default {
  data() {
    return {
      ws: ''
    }
  },
  mounted() {
    this.initSocket()
  },
  methods: {
    initSocket() {
      this.ws = new WebSocket(this.$store.getters.wsurl) // 监听地址端口号
      // this.ws = new WebSocket('ws://localhost:3000/') // 监听地址端口号
      this.ws.onopen = function() {
        console.log('服务器连接')
      }
      this.ws.onmessage = (msg) => {
        try {
          const result = qs.parse(msg.data)
          this.$store.dispatch('addEdims', { result })
        } catch (e) {
          console.log(e)
        }
      }

      this.ws.onclose = () => {
        console.log('服务器关闭')
      }

      function send() {
        //alert()
        // let msg = document.getElementById('sendtext').value
        //alert(msg)
        // this.ws.send(msg)
      }
    }
  }
}
</script>
<style>

</style>

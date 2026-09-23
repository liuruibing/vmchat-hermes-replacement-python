
<template>
    <span class="table_header_icon_box">
          <span style="font-size: 14px;">{{hintName}}</span>
          <!--:content="" -->
          <el-tooltip class="item table_header_icon" effect="dark"  placement="top">
               <span slot="content" ref="contentHint"></span>
                <i class="el-icon-question" style="cursor: pointer;"></i>
          </el-tooltip>
   </span>
</template>

<script>
  import commonApi from '@/api/common'
  export default {
    name: "hint-index",

    props: {
      hintName:'',
      dimCode:'',
      dimType:'',
    },
    data() {
      return {
        hintText:' '
      }
    },
    mounted(){
      let self = this;
      this.$nextTick(function () {
        new Promise((resolve, reject) => {
          commonApi.edimsCommonHint(self.dimCode,self.dimType).then(response => {
            if(response.data.data){
              if(response.data.data[0]){
                self.hintText = response.data.data[0].dimLog;
              }
              else{
                self.hintText = ' ';
              }
            }
            else{
              self.hintText = ' '
            }
            self.$refs.contentHint.innerHTML =  self.hintText;
            resolve()
          }).catch(error => {
            self.hintText = ' ';
            self.$refs.contentHint.innerHTML =  self.hintText;
            reject(error)
          })
        })
      });

    },

    methods:{


    }






  }
</script>

<style scoped>

</style>

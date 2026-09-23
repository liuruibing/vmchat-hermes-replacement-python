<template>
  <span>
    <span v-color="colorVal" v-if="Number(colorVal) > Number(colorValNorm)">{{colorVal | noDataFilter}}&nbsp;<i class="el-icon-top" style="color: #f56c6c"></i></span>
    <span v-color="colorVal" v-else-if="Number(colorVal) == Number(colorValNorm)">{{colorVal | noDataFilter}}</span>
    <span v-color="colorVal" v-else-if="Number(colorVal) < Number(colorValNorm)">{{colorVal | noDataFilter}}&nbsp;<i class="el-icon-bottom" style="color: #42b983" ></i></span>
    <span v-color="colorVal" v-else>{{colorVal | noDataFilter}}</span>
  </span>
</template>

<script>
  export default {
    name: "elIconTopBottom",
    props: {
      val:'',//接收的值
      valNorm:'',//接收的要比较的值
    },
    data() {
        return {
          colorVal:'',//接收的值
          colorValNorm:'',//接收的要比较的值
      }
    },
    mounted() {
      let self = this;
      self.colorVal  = self.$fun.numberToFixed( self.val , 4 ,100)
      //防止出现空值变为0的情况
        if( self.colorVal === ''){
        self.colorVal = undefined;
      }
      else{}
      self.colorValNorm  = self.$fun.numberToFixed( self.valNorm , 4 ,100)
      //防止出现空值变为0的情况
      if( self.colorValNorm === ''){
        self.colorValNorm = undefined;
      }
      else{}
    },
    watch:{
      'val' (val, oldval) {
        let self = this;
        self.colorVal  = self.$fun.numberToFixed( val , 4 ,100)
        //防止出现空值变为0的情况
        if( self.colorVal === ''){
          self.colorVal = undefined;
        }
        else{}
      },
      'valNorm' (val, oldval) {
        let self = this;
        self.colorValNorm  = self.$fun.numberToFixed( val , 4 ,100)
        //防止出现空值变为0的情况
        if( self.colorValNorm === ''){
          self.colorValNorm = undefined;
        }
        else{}
      },
    },
    //消除多次传输
    methods:{


    }
  }
</script>

<style scoped>

</style>

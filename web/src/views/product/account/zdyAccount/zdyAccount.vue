<template>
  <div class="zdy_account_info">
    <el-tabs v-model="activeName" @tab-click="handleClick" style="height:100%">
      <el-tab-pane label="托管户" name="one">
        <tg-form ref="one"/>
      </el-tab-pane>
      <el-tab-pane label="证券账户" name="two">
        <zq-form ref="two"/>
      </el-tab-pane>
      <el-tab-pane label="期货账户" name="three">
        <qhzh-form ref="three"/>
      </el-tab-pane>
      <el-tab-pane label="银行间债券账户" name="four">
        <yhj-form ref="four"/>
      </el-tab-pane>
      <el-tab-pane label="其他账户" name="five">
        <qt-form ref="five"/>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import TgForm from '@/views/product/account/form/tgForm'
import ZqForm from '@/views/product/account/form/zqForm'
import QhzhForm from '@/views/product/account/form/qhzhForm'
import QtForm from '@/views/product/account/form/qtForm.vue';
import YhjForm from '@/views/product/account/form/yhjForm.vue';
export default {
  components:{
    TgForm,ZqForm,QhzhForm,QtForm,YhjForm
  },
  data(){
    return{
      activeName:'one',
      fundCode:'',
    }
  },
  methods:{
    init(data){
      console.log(data);
      this.fundCode = data;
      this.$nextTick(()=>{
        this.$refs.one.init(data);
        // this.$refs.two.init(data);
        // this.$refs.three.init(data);
        // this.$refs.four.init(data);
        // this.$refs.five.init(data);
      })
    },
    handleClick(tab){
      console.log(tab.name);
      this.$notify.closeAll();
      this.$nextTick(()=>{
        this.$refs[tab.name].init(this.fundCode);
      })
    },
  }
};
</script>

<style lang="scss">
.zdy_account_info{
  height: 100%;
  .el-tabs__content{
    height: 100%;
    .el-tab-pane{
      height: 100%;
      overflow: auto;
      scrollbar-width: none; /* firefox */
      -ms-overflow-style: none; /* IE 10+ */
      overflow-x: hidden;
      overflow-y: auto;
    }
    .el-tab-pane::-webkit-scrollbar {
      display: none; /* Chrome Safari */
    }
  }
}
</style>
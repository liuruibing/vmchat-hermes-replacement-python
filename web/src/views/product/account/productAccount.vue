<template>
   <div class='accountheight'>
     <!-- @tab-click="handleClick" -->
       <el-tabs v-model="activeName">
          <el-tab-pane label="募集户" name="first">
            <mjAccountPage> </mjAccountPage>
          </el-tab-pane>
          <el-tab-pane label="托管户" name="second">
            <tgAccountPage> </tgAccountPage>
          </el-tab-pane>
          <el-tab-pane label="证券账户" name="third">
            <zqAccountPage> </zqAccountPage>
          </el-tab-pane>
          <el-tab-pane label="一码通与股卡" name="fourth">
            <ymtAccountPage> </ymtAccountPage>
          </el-tab-pane>
          <el-tab-pane label="期货账户" name="five">
            <qhAccountPage> </qhAccountPage>
          </el-tab-pane>
          <el-tab-pane label="期货开户统一编码" name="six">
            <qhOpenAccountPage> </qhOpenAccountPage>
          </el-tab-pane>
          <el-tab-pane label="银行间债券账户" name="eight">
             <yhAccountPage> </yhAccountPage>
          </el-tab-pane>
          <el-tab-pane label="场外期权账户" name="nine">
            <cwAccountPage> </cwAccountPage>
          </el-tab-pane>
          <el-tab-pane label="其他账户" name="ten">
            <other-accout></other-accout>
          </el-tab-pane>
          <el-tab-pane label="全部账户" name="all">
            <all-account v-if="activeName==='all'"></all-account>
          </el-tab-pane>
      </el-tabs>

        <div>
             <!-- <mjAccountPage v-if="mjAccountPage_show"> </mjAccountPage>
             <qhAccountPage v-if="qhAccountPage_show"> </qhAccountPage> -->
             <!-- <tgAccountPage v-if="tgAccountPage_show"> </tgAccountPage> -->
             <!-- <ymtAccountPage v-if="ymtAccountPage_show"> </ymtAccountPage> -->
            <!-- <zqAccountPage v-if="zqAccountPage_show"> </zqAccountPage> -->

            <!-- <qhOpenAccountPage v-if="qhOpenAccountPage_show"> </qhOpenAccountPage> -->
            <!-- <yhAccountPage v-if="yhAccountPage_show"> </yhAccountPage> -->
            <!-- <cwAccountPage v-if="cwAccountPage_show"> </cwAccountPage> -->
                  
        </div>
   </div>
</template>

<script>
 import mjAccountPage from './mjAccount.vue'
 import qhAccountPage from './qhAccount.vue'
 import tgAccountPage from './tgAccount.vue'
 import ymtAccountPage from './ymtAccount.vue'
 import zqAccountPage from './zqAccount.vue'
 import qhOpenAccountPage from './qhOpenAccount.vue'
 import yhAccountPage from './yhAccount.vue'
 import cwAccountPage from './cwAccount.vue'
 import OtherAccout from './otherAccout.vue'
 import allAccount from './allAccount.vue'
export default {
   name:'productAccount',
   components: {
     mjAccountPage,qhAccountPage,tgAccountPage,ymtAccountPage,zqAccountPage,qhOpenAccountPage,yhAccountPage,cwAccountPage,
     OtherAccout,allAccount
   },
   data () {
      return {
          activeName:'first',
          mjAccountPage_show:true,
          qhAccountPage_show:false,
          tgAccountPage_show:false,
          ymtAccountPage_show:false,
          zqAccountPage_show:false,
          qhOpenAccountPage_show:false,
          yhAccountPage_show:false,
          cwAccountPage_show:false
      };
   },


   mounted() {},

   methods: {
     handleClick(tab, event){
        this.tabLabel = tab.label;
        if(tab.label === "募集户"){
          this.mjAccountPage_show = true;
          this.qhAccountPage_show = false;
          this.tgAccountPage_show = false;
          this.ymtAccountPage_show = false;
          this.zqAccountPage_show = false;
          this.qhOpenAccountPage_show = false;
          this.yhAccountPage_show = false;
          this.cwAccountPage_show = false;
        }else if(tab.label === "托管户"){
          this.mjAccountPage_show = false;
          this.qhAccountPage_show = false;
          this.tgAccountPage_show = true;
          this.ymtAccountPage_show = false;
          this.zqAccountPage_show = false;
            this.qhOpenAccountPage_show = false;
          this.yhAccountPage_show = false;
          this.cwAccountPage_show = false;
        }else if(tab.label === "证券账户"){
          this.mjAccountPage_show = false;
          this.qhAccountPage_show = false;
          this.tgAccountPage_show = false;
          this.ymtAccountPage_show = false;
          this.zqAccountPage_show = true;
            this.qhOpenAccountPage_show = false;
          this.yhAccountPage_show = false;
          this.cwAccountPage_show = false;
        }else if(tab.label === "一码通与股卡"){
          this.mjAccountPage_show = false;
          this.qhAccountPage_show = false;
          this.tgAccountPage_show = false;
          this.ymtAccountPage_show = true;
          this.zqAccountPage_show = false;
            this.qhOpenAccountPage_show = false;
          this.yhAccountPage_show = false;
          this.cwAccountPage_show = false;
        }else if(tab.label === "期货账户"){
          this.mjAccountPage_show = false;
          this.qhAccountPage_show = true;
          this.tgAccountPage_show = false;
          this.ymtAccountPage_show = false;
          this.zqAccountPage_show = false;
            this.qhOpenAccountPage_show = false;
          this.yhAccountPage_show = false;
          this.cwAccountPage_show = false;
        }else if(tab.label === "期货开户统一编码"){
          this.mjAccountPage_show = false;
          this.qhAccountPage_show = false;
          this.tgAccountPage_show = false;
          this.ymtAccountPage_show = false;
          this.zqAccountPage_show = false;

            this.qhOpenAccountPage_show = true;
          this.yhAccountPage_show = false;
          this.cwAccountPage_show = false;

        }else if(tab.label === "银行间债券账户"){
          this.mjAccountPage_show = false;
          this.qhAccountPage_show = false;
          this.tgAccountPage_show = false;
          this.ymtAccountPage_show = false;
          this.zqAccountPage_show = false;
           this.qhOpenAccountPage_show = false;
          this.yhAccountPage_show = true;
          this.cwAccountPage_show = false;

        }else if(tab.label === "场外期权账户"){
          this.mjAccountPage_show = false;
          this.qhAccountPage_show = false;
          this.tgAccountPage_show = false;
          this.ymtAccountPage_show = false;
          this.zqAccountPage_show = false;
           this.qhOpenAccountPage_show = false;
          this.yhAccountPage_show = false;
          this.cwAccountPage_show = true;
        }
     }
   }
}
</script>
<style lang='scss'>
.accountheight {
 .el-tabs__content {
   min-height: 300px !important
 }
}
</style>
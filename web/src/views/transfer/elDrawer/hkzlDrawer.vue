<template>
  <div class="hkzl_drawer" id="all">
    <div class="hkzl_drawer_top">
      <div class="top_button" v-if="button_show && activeIndex>1">
        <!-- <el-button type="primary" size="small" plain icon="el-icon-download" @click="downloadT('excel')">下载Excel</el-button> -->
        <el-button type="primary" size="small" plain icon="el-icon-download" @click="downloadT('pdf')">下载PDF</el-button>
        <el-button type="primary" size="small" plain icon="el-icon-download" @click="downloadT('word')">下载Word</el-button>
        <el-button type="primary" size="small" plain icon="el-icon-printer" v-print="printViewObj" @click="print">打印</el-button>
      </div>
    </div>
    <div style="display:none;">
    <div class="table_out_" style="width:90%;margin:0 auto;font-size:14px">
      <h2 class="c" style="margin-bottom:5px">划款指令报表</h2>
      <h3 class="c"><span class="company">$company$</span>＿<span class="fundName">$fundName$</span>＿专用表</h3>
      <div class="tit_">
        <p class="c">编号：<span class="number">$number$</span></p>
        <p class="c">指令日期：<span class="date">$date$</span></p>
        <p><span class="organization">$organization$</span>资产托管部：</p>
        <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;敬请贵部根据以下提供的收款人名称、开户行、账号、到账日期和划款金额划款。</p>
      </div>
      <ul class="ul_list">
        <li>
          <span class="left">到账日期：</span>
          <span class="transferReqdate">$transferReqdate$</span>
        </li>
        <li>
          <span class="left">付款人：</span>
          <span class="payerAcconame">$payerAcconame$</span>
        </li>
        <li>
          <span class="left">开户行：</span>
          <span class="payerBank">$payerBank$</span>
        </li>
        <li>
          <span class="left">账号：</span>
          <span class="payerAccount">$payerAccount$</span>
        </li>
        <li>
          <span class="left">收款人：</span>
          <span class="payeeAcconame">$payeeAcconame$</span>
        </li>
        <li>
          <span class="left">开户行：</span>
          <span class="payeeBank">$payeeBank$</span>
        </li>
        <li>
          <span class="left">账号：</span>
          <span class="payeeAccount">$payeeAccount$</span>
        </li>
        <li>
          <span class="left">划款金额（小写）：</span>
          <span class="money">$moneyl$</span>
        </li>
        <li>
          <span class="left">划款金额（大写）：</span>
          <span class="money">$moneyb$</span>
        </li>
      </ul>
      <div class="hkyt">
        <p>划款用途：</p>
        <p class="processUse">$processUse$</p>
      </div>
      <div class="bz">
        <p>备注:</p>
        <span class="remark">$remark$</span>
      </div>
      <div class="banliren">
        <ul class="banliren_i banliren_left">
          <li class="li_man">管理人签章：$adminSeal$ <img class="adminSeal" src="" alt=""></li>
          <li>审批人：<span></span></li>
          <li>复核人：<span></span></li>
          <li>经办人：<span></span></li>
        </ul>
        <ul class="banliren_i">
          <li class="li_man">托管人签章：</li>
          <li>审批人：<span></span></li>
          <li>复核人：<span></span></li>
          <li>经办人：<span></span></li>
        </ul>
      </div>
      <div class="table_bottom">
        <p class="table_bottom_1"><span>制表：$operator$</span><span>复核：$reviewer$</span><span>审核：$approver$</span></p>
        <p class="table_bottom_2"><span>打印：$operator$</span><span>打印日期：$printDate$</span></p>
      </div>
    </div>
    </div>
    <!-- ----------------------------------------------- -->
    <!-- <div  > -->
      <div id="printView" ref="printView" v-html="templateHtml" v-loading="templateloading">
      </div>
    <!-- </div> -->
    <!-- <div class="test_" ref="print_View"></div>
    <el-button v-print="'#all'">打印</el-button> -->
    
    
  </div>
</template>

<script>
// import Watermark from '@/utils/watermark'
import commonFun from '@/filters/new_common'
import { moneyYuan } from '@/filters/index'
import configurationApi from '@/api/configuration/configuration.js'
import $ from 'jquery'
export default {
  name:'HkzlDrawer',
  props:{
    fundCode:{},
    tableData:{},
    oldForm:{},
    activeIndex:{
      default:0,
    },
  },
  data(){
    return{
      form:{
        number:'0001',
        date:'2021-01-01',
        endDate:'2021-03-19'
      },
      data_:{},
      dataT:{},
      templateloading:false,
      button_show:false,
      xmlId:'',
      templateHtml:'',
      printViewObj:{
        id:'printView',
        popTitle:'运营管理平台',
        // extraCss: 'https://www.google.com,https://www.google.com',
        extraHead: '<meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0"/>',
      }
    }
  },
  watch:{
    fundCode(){
      // this.get_html()
    }
  },
  mounted(){
    // this.get_html()
    // let html = document.getElementsByClassName('table_out_')[0].outerHTML;
    //   console.log(html);
  },
  methods:{
    init1(){
      this.templateHtml=''
      this.templateloading = true;
    },
    init(data,xmlId){
      this.xmlId = xmlId;
      // console.log('this.xmlId',this.xmlId);
      // console.log(data);
      this.dataT = data;
      // let dataForm = data.dataForm;
      // this.data_ = data.dataForm;
      let dataForm = data;
      this.data_ = data;
      this.get_html(dataForm);
    },
    get_html(dataForm){
      this.templateloading = true;
      this.templateHtml=''
      let params={fundCode:dataForm.fundCode}
      let html=null;
      let adminSealByte,waterMakerByte;
      configurationApi
        .getTemplate(params)
        .then(res=>{
          // console.log(res);
          if(res.data.status==200){
            // this.button_show = true;
            html=res.data.data.templateHtml;
            adminSealByte = res.data.data.adminSealByte;
            waterMakerByte = res.data.data.waterMakerByte;
            // console.log(html);
            let params1 = {
              fundCode:dataForm.fundCode,
              id:dataForm.id
            }
            configurationApi.getFundInfo(params1).then(res=>{
              if(res.data.status==0){
                let data = res.data.data;
                html = html.replace('$company$', data.company || 'xxx');
                html = html.replace('$fundName$', data.fundName || 'xxx');
                html = html.replace('$organization$', data.organization || 'xxx');
                html = html.replace('$number$',dataForm.pfomBizNum || this.tableData.pfomBizNum);
                if(this.dataT.beginTime){
                  html = html.replace('$date$',this.dataT.beginTime.split(' ')[0] || '');
                }else{
                  html = html.replace('$date$','');
                }
                html = html.replace('$transferReqdate$',dataForm.transferReqdate || '');
                html = html.replace('$payerAcconame$',dataForm.payerAcconame || '');
                html = html.replace('$payerBank$',dataForm.payerBank || '');
                html = html.replace('$payerAccount$',dataForm.payerAccount || '');
                html = html.replace('$payeeAcconame$',dataForm.payeeAcconame || '');
                html = html.replace('$payeeBank$',dataForm.payeeBank || '');
                html = html.replace('$payeeAccount$',dataForm.payeeAccount || '');
                // html = html.replace('$zh1$',this.tableData.payeeAccount || '');
                // if(dataForm.transferAmount){
                //   // moneyHundredMillion
                //   let moneyl = commonFun.moneyHundredMillion(dataForm.transferAmount);
                //   html = html.replace('$moneyl$', moneyl);
                // }else{
                //   html = html.replace('$moneyl$','');
                // }
                if(dataForm.transferAmount){
                  let moneyl = moneyYuan(dataForm.transferAmount);
                  html = html.replace('$moneyl$', moneyl);
                  let moneyb = commonFun.convertCurrency(dataForm.transferAmount);
                  html = html.replace('$moneyb$', moneyb);
                }else{
                  html = html.replace('$moneyl$','');
                  html = html.replace('$moneyb$', '');
                }
                html = html.replace('$processUse$',dataForm.processUse || '');
                html = html.replace('$remark$',dataForm.remark || '');
                // html = html.replace('$adminSeal$', '');
                html = html.replace(/\$operator\$/g, data.operator || '');
                html = html.replace('$reviewer$', data.reviewer || '');
                html = html.replace('$approver$', data.approver || '');
                // yyr_timestampToTime
                if(data.printDate){
                  let printDate = commonFun.yyr_timestampToTime(data.printDate);
                  html = html.replace('$printDate$', printDate || '');
                }else{
                  html = html.replace('$printDate$', '');
                }
                if(adminSealByte){
                  html = html.replace('$adminSeal$',`<img class="adminSeal" src="${adminSealByte}" alt="">` || '')
                }else{
                  html = html.replace('$adminSeal$', '')
                }
                if(data.operatorSeal){
                  html = html.replace('$operatorSeal$',`<img class="operatorSeal" src="${data.operatorSeal}" alt="">`)
                }else{
                  html = html.replace('$operatorSeal$', '')
                }
                if(data.reviewerSeal){
                  html = html.replace('$reviewerSeal$',`<img class="operatorSeal" src="${data.reviewerSeal}" alt="">`)
                }else{
                  html = html.replace('$reviewerSeal$', '')
                }
                if(data.approverSeal){
                  html = html.replace('$approverSeal$',`<img class="operatorSeal" src="${data.approverSeal}" alt="">`)
                }else{
                  html = html.replace('$approverSeal$', '')
                }
                this.templateHtml=html;
                this.templateloading = false;
                this.button_show = true;
                setTimeout(()=>{
                  // console.log('hkzl',this.oldForm);
                  this.$nextTick(()=>{
                    if(this.xmlId.indexOf('glrfh')!=-1 || this.xmlId.indexOf('glrsp')!=-1){
                      if(dataForm.transferReqdate!=this.oldForm.transferReqdate){
                        $('.transferReqdate').css("color","red")
                      }
                      if(dataForm.payerAcconame!=this.oldForm.payerAcconame){
                        $('.payerAcconame').css("color","red")
                      }
                      if(dataForm.payerBank!=this.oldForm.payerBank){
                        $('.payerBank').css("color","red")
                      }
                      if(dataForm.payerAccount!=this.oldForm.payerAccount){
                        $('.payerAccount').css("color","red")
                      }
                      if(dataForm.payeeAcconame!=this.oldForm.payeeAcconame){
                        $('.payeeAcconame').css("color","red")
                      }
                      if(dataForm.payeeBank!=this.oldForm.payeeBank){
                        $('.payeeBank').css("color","red")
                      }
                      if(dataForm.payeeAccount!=this.oldForm.payeeAccount){
                        $('.payeeAccount').css("color","red")
                      }
                      if(moneyYuan(dataForm.transferAmount)!=this.oldForm.transferAmount){
                        $('.money').css("color","red")
                      }
                      if(dataForm.processUse!=this.oldForm.processUse){
                        $('.processUse').css("color","red")
                      }
                      if(dataForm.remark!=this.oldForm.remark){
                        $('.remark').css("color","red")
                      }
                    }
                  })
                },800)
                // console.log('html',html);
              }else{
                this.$message({type:'error',message:res.data.message || '获取数据错误'})
                this.templateloading = false;
                this.button_show = false;
              }
            })
            // html = html.replace('$adminSeal$','<img class="adminSeal" src="/src/assets/img/picture03.jpg" alt="">' || '');
            // setTimeout(() => {
            //   if(this.form.endDate!='0002'){
            //     $('.endDate').css("color","red")
            //     $('.endDate').attr("title","修改前")
            //   }
            // }, 50);
          }else{
            this.templateHtml='未配置模板';
            this.templateloading = false;
            this.button_show = false;
          }
        })
        .catch(()=>{
          this.templateHtml='';
          this.button_show = false;
          this.templateloading = false;
        })
      // console.log($('.endDate'));
    },
    getFundInfo(){

    },
    print(){
      // this.$p({
      //   el: this.$refs.printView, //打印目标dom节点，
      //   debug: false, //打开调试模式，会显示iframe,
      //   importCss: false, //引入head 中的link stylesheet
      //   importStyle: true, //引入style标签中的样式
      //   loadCss: [], //需要载入的第三方样式表
      //   title: "", //打印标题
      //   delay: 300, //延迟打印时间，确保iframe中的静态资源加载完成
      //   beforePrinfHandle: null, //打开打印窗口前的钩子函数,可以针对打印文档进行自定义调整，接受一个document参数
      //   afterPrintHandle: null, //打印完成的钩子函数,
      // });
    },
    downloadExcel(){},
    downloadPdf(){},
    downloadWord(){},
    downloadT(type){
      let params = {}
      params.id = this.data_.id;
      params.type = type;
      params.xmlId = this.xmlId;
      if(this.$store.getters.token){ params["token"] = this.$store.getters.token;}
      let action = this.$store.state.setting.baseApi + '/api/template/v1.0/downloadByType';
      // console.log(action+'?'+'id='+file.id+'&token='+this.$store.getters.token);
      
      commonFun.formDownloadFile(params,action,"GET");
    }
  }
}
</script>

<style lang='scss'  rel="stylesheet/scss" >
@media print{
  
  body {
    // -webkit-print-color-adjust: exact;
    font-size: 24px;
    margin: 0mm 15mm 0mm 15mm;
    padding-top: 10mm;
    color: #000 !important;
    font-family: "宋体";
  }
  @page{
    size: auto;  /* auto is the initial value */
    margin: 0mm; /* this affects the margin in the printer settings */
  }
  #printView{
    div,span,p,ul,li{
      color: #000 !important;
    }
    *{
      margin: 0;
      padding: 0;
    }
    width: 90%;
    .table_out_{
      div,span,p,ul,li{
      color: #000 !important;
    }
      *{
      margin: 0;
      padding: 0;
    }
  width: 90%;
  // padding: 10px 20px;
  // max-width: 800px;
  // margin: 0 auto;
  font-size: 24px !important;
  color: #000 !important;
  div{
    border: 1px solid #000;
  }
  .tit_{
    p{
      margin: 5px 0;
    }
  }
  .ul_list{
    // border: 1px solid #000;
    border-left: 1px solid #000;
    border-right: 1px solid #000;
    li{
      border-bottom: 1px solid #000;
      min-height: 60px;
      display: flex;
      span{
        // display: inline-block;
        min-height: 60px;
        line-height: 60px;
        color: #000 !important;
      }
      .left{
        width: 300px;
        border-right: 1px solid #000;
      }
      & :nth-child(2){
        flex: 1;
        word-wrap:break-word;
        overflow: hidden;
      }
    }
  }
  .hkyt{
    min-height: 100px;
    border-top: none;
    border-bottom: none;
    // p:nth-child(2){
    //   -webkit-line-clamp: 3;
    //   overflow: hidden;
    //   display: -webkit-box;
    //   -webkit-box-orient: vertical;
    // }
  }
  .bz{
    min-height: 100px;
    // span:nth-child(2){
    //   -webkit-line-clamp: 3;
    //   overflow: hidden;
    //   display: -webkit-box;
    //   -webkit-box-orient: vertical;
    // }
  }
  .banliren{
    border-top: none;
    border-bottom: none;
    display: flex;
    .banliren_i{
      width: 50%;
      li{
        height: 80px;
        border-bottom: 1px solid #000;
        position: relative;
        .operatorSeal{
          position: absolute;
          width: auto;
          height: 70px;
          top: 2px;
          left: 95px;
        }
      }
      .li_man{
        height: 160px;
        position: relative;
        .adminSeal{
          position: absolute;
          width: auto;
          height: 100px;
          top: 20px;
          left: 150px;
        }
      }
    }
    .banliren_left{
      border-right: 1px solid #000;
    }
  }
  .table_bottom{
    border: none;
    .table_bottom_1{
      span{
        display: inline-block;
        width: 33%;
      }
    }
    .table_bottom_2{
      span{
        display: inline-block;
        width: 50%;
      }
    }
  }
}
  }
}
.test_{
  height: 30px;
  border: solid 1px red;
}
.c{
  text-align: center;
}
.table_out_{
  // width: 100%;
  // padding: 10px 20px;
  // max-width: 800px;
  // width: 90%;
  // margin: 0 auto;
  font-size: 14px;
  div{
    border: 1px solid #000;
  }
  .tit_{
    p{
      margin: 5px 0;
    }
  }
  .ul_list{
    // border: 1px solid #000;
    border-left: 1px solid #000;
    border-right: 1px solid #000;
    li{
      border-bottom: 1px solid #000;
      min-height: 30px;
      display: flex;
      span{
        // display: inline-block;
        min-height: 30px;
        line-height: 30px;
      }
      .left{
        width: 150px;
        border-right: 1px solid #000;
      }
      & :nth-child(2){
        flex: 1;
        overflow: hidden;
        word-wrap:break-word;
      }
    }
  }
  .hkyt{
    min-height: 70px;
    border-top: none;
    border-bottom: none;
    // p:nth-child(2){
    //   -webkit-line-clamp: 3;
    //   overflow: hidden;
    //   display: -webkit-box;
    //   -webkit-box-orient: vertical;
    // }
  }
  .bz{
    min-height: 70px;
  }
  .banliren{
    border-top: none;
    border-bottom: none;
    display: flex;
    .banliren_i{
      width: 50%;
      li{
        height: 40px;
        border-bottom: 1px solid #000;
        position: relative;
        .operatorSeal{
          position: absolute;
          width: auto;
          height: 38px;
          top: 1px;
          left: 95px;
        }
      }
      .li_man{
        height: 80px;
        position: relative;
        .adminSeal{
          position: absolute;
          width: auto;
          height: 50px;
          top: 20px;
          left: 95px;
        }
      }
    }
    .banliren_left{
      border-right: 1px solid #000;
    }
  }
  .table_bottom{
    border: none;
    .table_bottom_1{
      span{
        display: inline-block;
        width: 33%;
      }
    }
    .table_bottom_2{
      span{
        display: inline-block;
        width: 50%;
      }
    }
  }
}
.hkzl_drawer{
  // height: 99%;
  // overflow: hidden;
  // overflow-y: scroll;
  padding: 0 20px 30px 20px;
  .hkzl_drawer_top{
    overflow: hidden;
    margin-bottom: 20px;
    .top_button{
      float: right;
    }
  }
  
}
</style>
<style>
/* .hkzl_drawer .el-drawer {
  overflow-y: auto !important;
} */
</style>

<template>
  <div>
    <div id="diagram"></div>
    <!-- <MarkdownEditor></MarkdownEditor> -->
  </div>
</template>

<script>
import BpmnViewer from "bpmn-js";
import $ from "jquery";
import commonFun from "@/filters/new_common";
import commonApi from "@/api/common";
// import MarkdownEditor from "@/components/MarkdownEditor";
// import { parse } from 'path-to-regexp';
export default {
  name: "testBpm",
  // components: { MarkdownEditor },
  //components: {processform,modulemsg},
  data() {
    return {
      id: '',
      clickBox: [
        'transfer_ywfq',
        'transfer_zljb',
        'transfer_glrfh',
        'transfer_glrsp',
        'transfer_hkjg'
      ], //绘制点击事件
      viewSuccess: [], //流程通过项
      viewReading: [] //流程执行中
    };
  },

  mounted() {
    //流程全局配置
    // $("body").on("click", ".djs-element", function () {
    //   // 显示弹窗
    //   console.log(11);
    // });
  },

  methods: {
    init (data) {
      this.id = data.id
      if (JSON.stringify(data) != '[]') {
        this.viewSuccess = []
        this.viewReading = []
        this.clickBox = []
        let tempCom = new Array
        let tempCRun = new Array
        for (let item of data.data) {
          let obj = {
            remack: '',
            xmlId: item.xmlId || ''
          }
          if (item.taskStatus == 'COMPLETED') {
            obj['remack'] = '已完成'
            tempCom.push(obj)
          }else if (item.taskStatus == 'RUNNING') {
            obj['remack'] = '当前处理'
            tempCRun.push(obj)
          } else {}
         this.clickBox.push(item.xmlId)
        }
        this.viewSuccess = tempCom
        this.viewReading = tempCRun
        this.getBpm();
      }
      else this.getBpm();
    },
    getBpm() {
      this.$message.closeAll();
      commonApi.get_processdefine_xml(this.id).then((res) => {
        if (res.data.status === 0) {
          var bpmnxml = res.data.data; //xml绘图
          $("#diagram").html("");
          $("#diagram").fadeIn(100);
          //$(".bpmn_delete_img").fadeIn(100);
          commonFun.bpmnModule(bpmnxml, this.clickBox, this.viewSuccess, this.viewReading);
        } else this.$message.error("查询流程图失败");
      }).catch(() => {})
    }
  },
};
</script>
<style lang='css' scoped>
</style>

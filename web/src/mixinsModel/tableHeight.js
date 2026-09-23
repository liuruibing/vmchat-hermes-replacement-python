import $ from "jquery";
export default {
  data() {
    return {
      // 表格高度
      selfAdaptationtHeight: 400,
      // 是否有分页
      hasPagination: true,
      // 其他高度(表格底部内容)
      otherHeight: 0
    }
  },
  mounted() {},
  activated() {
    setTimeout(() => {
      this.getTableHeight();
      let self = this;
      window.addEventListener("resize", self.getTableHeight, true);
    }, 200);
  },
  deactivated() {
    let self = this;
    window.removeEventListener("resize", self.getTableHeight, true);
  },
  beforeDestroy() {
    let self = this;
    window.removeEventListener("resize", self.getTableHeight, true);
  },
  methods: {
    // 窗口高度 - 页面.page-top-box高度 - 其他高度(顶部导航栏、padding等)
    // getTableHeight() {
    //   const screenHeight = $(window).height();
    //   let topBoxHeight = $('.page-top-box').height() || 0;
    //   let tableHeight = 0;
    //   if (this.hasPagination) {
    //     tableHeight = screenHeight - topBoxHeight - 180;
    //   } else {
    //     tableHeight = screenHeight - topBoxHeight - 140;
    //   }
    //   if (this.otherHeight) {
    //     tableHeight = tableHeight - this.otherHeight;
    //   }
    //   this.selfAdaptationtHeight = tableHeight >= 400 ? tableHeight : 400;
    // },

    // 窗口高度 - 表格到顶部的距离 - 其他高度(底部的padding等)
    getTableHeight() {
      const screenHeight = $(window).height();
      let tableHeight = 0;
      let topBoxHeight = 0;
      if($('.selfAdaptationTable')){
        topBoxHeight = $('.selfAdaptationTable').offset().top;
        if (this.hasPagination) {
          // 70: 分页器高度40 + 其他padding30
          tableHeight = screenHeight - topBoxHeight - 70;
        } else {
          // 30: 其他padding30
          tableHeight = screenHeight - topBoxHeight - 30;
        }
        if (this.otherHeight) {
          tableHeight = tableHeight - this.otherHeight;
        }
      }
      this.selfAdaptationtHeight = tableHeight >= 400 ? tableHeight : 400;
    },
  }
}

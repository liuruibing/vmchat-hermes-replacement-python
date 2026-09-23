<template>
  <div class="attr-container-canvas">
    <div class="title">画布属性</div>
    <!--    <el-form style="padding: 20px;">-->
    <!--      <el-form-item v-for="(key, index) in Object.keys(options)" :key="index" :label="options[key]">-->
    <!--        <el-color-picker v-if="isIncludesColor(key)" v-model="canvasStyleData[key]" show-alpha></el-color-picker>-->
    <!--        <el-input v-else v-model.number="canvasStyleData[key]" type="number"/>-->
    <!--      </el-form-item>-->
    <!--    </el-form>-->
    <div style="padding-left: 10px;padding-top: 10px; overflow-y: auto">
      <div :style="{ height: rightHeight }">
        <div style="position: relative; line-height: 26px; margin-bottom: 10px">
          <span style="font-size: 13px; font-weight: bold; color: #A15008; width: 60px; display: inline-block; margin-left: 10px">页边距</span>
        </div>
        <div style="position: relative; line-height: 26px; margin-bottom: 10px">
          <span style="font-size: 14px; margin-left: 10px; color: #333; display: inline-block">上边距</span>
          <span style="position: absolute; right: 5px">
            <el-input
              v-model.number="pageMarginsOption.topMargin"
              :min="1"
              :required="true"
              :step="1"
              class="component-attr-input"
              size="small"
              @change="checkQuantity('topMargin')"
            />
          </span>
        </div>
        <div style="position: relative; line-height: 26px; margin-bottom: 10px">
          <span style="font-size: 14px; margin-left: 10px; color: #333; display: inline-block">下边距</span>
          <span style="position: absolute; right: 5px">
            <el-input
              v-model.number="pageMarginsOption.bottomMargin"
              :min="1"
              :required="true"
              :step="1"
              class="component-attr-input"
              size="small"
              @change="checkQuantity('bottomMargin')"
            />
          </span>
        </div>
        <div style="position: relative; line-height: 26px; margin-bottom: 10px">
          <span style="font-size: 14px; margin-left: 10px; color: #333; display: inline-block">左边距</span>
          <span style="position: absolute; right: 5px">
            <el-input
              v-model.number="pageMarginsOption.leftMargin"
              :min="0"
              :required="true"
              :step="1"
              class="component-attr-input"
              size="small"
              @change="checkQuantity('leftMargin')"
            />
          </span>
        </div>
        <div style="position: relative; line-height: 26px; margin-bottom: 10px">
          <span style="font-size: 14px; margin-left: 10px; color: #333; display: inline-block">右边距</span>
          <span style="position: absolute; right: 5px">
            <el-input
              v-model.number="pageMarginsOption.rightMargin"
              :min="1"
              :required="true"
              :step="1"
              class="component-attr-input"
              size="small"
              @change="checkQuantity('rightMargin')"
            />
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data() {
    return {
      options: {
        color: '颜色',
        opacity: '不透明度',
        backgroundColor: '背景色',
        fontSize: '字体大小'
      },
      rightHeight: '0px',
      pageMarginsOption: {
        leftMargin: 0,
        rightMargin: 0,
        topMargin: 0,
        bottomMargin: 0
      }
    }
  },
  computed: mapState(['canvasStyleData']),
  watch: {
    pageMarginsOption: {
      handler() {
        // 设置到 vuex里面的画布属性中去
        this.$store.commit('SET_PAGE_MARGIN_OPTION', this.pageMarginsOption)
      },
      deep: true
    },
    '$store.state.pageMarginsOption': {
      handler(val) {
        this.pageMarginsOption = val
      }
    }
  },
  created() {
    this.getRightHeight()
    window.addEventListener('resize', this.getRightHeight)
    this.pageMarginsOption = this.$store.state.pageMarginsOption
  },
  methods: {
    checkQuantity(val) {
      if (this.pageMarginsOption[val] < 0 || !Number.isInteger(this.pageMarginsOption[val])) {
        this.$message({
          message: '请输入大于0的整数',
          type: 'warning'
        })
        this.pageMarginsOption[val] = 0
      }
    },
    getRightHeight() {
      const rightHeight = document.getElementById('app').offsetHeight
      this.rightHeight = rightHeight - 80 - 45 - 143 + 'px'
    },
    isIncludesColor(str) {
      return str.toLowerCase().includes('color')
    }
  }
}
</script>

<style lang="scss" scoped>
.attr-container-canvas {
  //border-bottom: 1px solid #838383;
  color: #a7a394 !important;

  .title {
    text-align: center;
    //margin-bottom: 10px;
    height: 40px;
    line-height: 40px;
    border-bottom: 1px solid #838383;
    font-size: 14px;
    font-weight: 500;
    background-color: #e6e8ef;
    color: #333 !important;
  }

  .el-form-item__label {
    color: #a7a394 !important;
  }

  ::v-deep .el-input--small .el-input__inner {
    height: 26px;
    // background-color: #202020;
    // color: #fff !important;
    // padding-left: 5px;
    // border: 0.5px solid #6d6d6d;
    width: 140px;
  }

  .component-attr-input {
    width: 140px !important;
    color: #aaacaf;
    // border: 0.5px solid #404955;
    ::v-deep .el-input--small .el-input__inner {
      width: 140px !important;
    }

    ::v-deep .el-input__inner {
      width: 140px !important;
    }

    ::v-deep .el-tag .el-tag--info .el-tag--mini .el-tag--light {
      max-width: 50px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    ::v-deep .el-input__suffix {
      //right: 20px;
    }

    ::v-deep .el-input--small,
    .form_inline_search .el-date-editor.el-input {
      width: 140px !important;
    }
  }
}
</style>

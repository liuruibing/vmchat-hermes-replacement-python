<template>
  <div class="time-line-inner">
    <div class="left-btn">
      <el-button type="primary" icon="el-icon-arrow-left" circle @click="leftButtonClick"></el-button>
    </div>
    <div class="line">
      <div class="line-dom" style="width: 100%; height: 2px; margin-left: 2000px">
        <div v-for="(item, key) in dateList" :key="item.fId" :style="{ 'margin-left': 100 * (key + 1) + 'px' }">
          <div class="time-circle" :class="item.checked ? 'active' : ''" @click="handleClickDate(item)">
            <div class="time-date">{{ item.ddate || '-' }}</div>
          </div>
        </div>
      </div>
    </div>
    <div class="right-btn">
      <el-button type="primary" icon="el-icon-arrow-right" circle @click="rightButtonClick"></el-button>
    </div>
  </div>
</template>
<script>
export default {
  name: 'timeLine',
  props: {
    dateList: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    /**
     * @description 切换时间节点
     */
    handleClickDate(val) {
      const { fId } = val
      const _Index = this.dateList.findIndex(item => {
        return item.fId === fId
      })
      this.dateList.forEach(item => {
        item.checked = false
      })
      this.dateList[_Index].checked = true
      this.$emit('updateDdate', val.ddate)
    },
    leftButtonClick() {
      const temp = -280
      let oDom = document.querySelector('.line-dom')
      if (oDom.style.marginLeft) {
        const left = oDom.style.marginLeft.replace(/px/g, '')
        oDom.style.marginLeft = Number(left) + temp + 'px'
      } else {
        oDom.style.marginLeft = oDom.style.marginLeft + temp + 'px'
      }
    },
    rightButtonClick() {
      const temp = 280
      let oDom = document.querySelector('.line-dom')
      if (oDom.style.marginLeft) {
        const left = oDom.style.marginLeft.replace(/px/g, '')
        oDom.style.marginLeft = Number(left) + temp + 'px'
      } else {
        oDom.style.marginLeft = oDom.style.marginLeft + temp + 'px'
      }
    }
  }
}
</script>
<style scoped lang="scss">
.time-line-inner {
  height: 100%;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  position: relative;

  .left-btn {
    height: 49px;
    position: absolute;
    left: 0px;
    z-index: 9999;
    margin-top: 10px;
  }
  .right-btn {
    height: 49px;
    position: absolute;
    right: 0;
    z-index: 9999;
    margin-top: 10px;
  }
  .line {
    height: 2px;
    background-color: #e9c5a5;
    width: 9999px;
    margin: 0 10px;
    position: relative;
    margin-left: -2000px;

    .time-circle {
      position: absolute;
      top: -4px;
      height: 10px;
      width: 10px;
      border-radius: 10px;
      border: 1px solid #ccc;
      background-color: #fff;
      cursor: pointer;
      .time-date {
        position: absolute;
        top: -33px;
        width: 100px;
        left: -30px;
      }
    }
    .active {
      border-radius: 10px;
      background-color: #e9c5a5;
      border: 1px solid #e9c5a5;
    }
  }
}
::v-deep .el-button.el-button--primary {
  background-color: #e9c5a5;
  border-color: transparent;
  color: #fff;
  font-size: 14px;
  padding: 12px!important
}
</style>

<template>
  <div class="rect-shape" style="height:100%;width:100%;">
    <!--      <v-text :prop-value="element.propValue" :element="element" >没有权限</v-text>-->
    <div class="no-limit" style="height:100%;width:100%;color: #C0C4CC;  display: none;align-items: center;justify-content: center;">
      <div style="text-align: center">
        没有查询权限
      </div>
    </div>
  </div>
</template>

<script>
import OnEvent from '../common/OnEvent'

export default {
  extends: OnEvent,
  props: {
    propValue: {
      type: String,
      required: true,
      default: '',
    },
    element: {
      type: Object,
      default: () => {
      },
    },
  },
}
</script>

<style lang="scss" scoped>
.rect-shape {
  width: 100%;
  height: 100%;
  overflow: auto;
}
</style>

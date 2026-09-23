<template>
  <div>
    <div style="font-size: 16px;height: 30px;line-height: 30px;">
      <slot name="title"></slot>
    </div>
    <div class="content-style">
      <slot name="content">
      </slot>
    </div>
  </div>
</template>
<style lang="scss" scoped>
.content-style {
  //border: 1px rgb(227, 227, 227) solid;
  margin-top: 10px;
}
</style>

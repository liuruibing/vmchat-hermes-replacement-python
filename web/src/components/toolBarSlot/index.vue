<template>
    <div class="standard-form" style="display: flex; justify-content: space-between; margin: 10px 0;">
      <span>
        <slot name="left"></slot>
      </span>
      <span>
        <slot name="right"></slot>
      </span>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ToolBarSlot'
  }
  </script>
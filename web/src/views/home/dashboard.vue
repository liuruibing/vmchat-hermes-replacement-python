<!--
 * @Description:
 * @Author:
 * @Date: 2023-01-29 09:27:55
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2023-02-13 15:27:16
-->
<template>
  <div class="mt20" style="padding-left: 20px; padding-right: 20px;" v-auto-enter>
    <first-line></first-line>
    <second-line class="mt10"></second-line>
    <third-line class="mt20"></third-line>
    <line-fourth class="mt20"></line-fourth>
  </div>
</template>
<script>
import $ from 'jquery'
import firstLine from './components/firstLine2'
import secondLine from './components/secondLine2'
import thirdLine from './components/thirdLine2'
import lineFourth from './components/lineFourth2'

export default {
  name: 'dashboard',
  components: { lineFourth, firstLine, secondLine, thirdLine },
  mounted() {},
  activated() {},
  deactivated() {}
}
</script>

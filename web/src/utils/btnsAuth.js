import Vue from 'vue'
import store from '@/store'

// 按钮判断
function JudgeBtn(el, value, btns) {
  // console.log('value',value);
  let isHas = false
  // btns.forEach(item => {
  //   if (value === item) isHas = true
  // })
  for (let i = 0; i < btns.length; i++) {
    if (value === btns[i]) {
      isHas = true
      break
    }
  }
  if (isHas) {
    el.style.display = 'inline-block'
  } else {
    el.style.display = 'none'
  }
}

export default function(btnData) {
  // 按钮权限数组
  let btns = []
  btnData.forEach(item => {
    if (item.vcactiontype !== 'PAGE.PERMISSION.TYPE.MU') {
      btns.push(item.vcactioncode)
    }
  })
  // console.log(btns);
  // console.log('------------按钮权限-----------')
  // console.log(btns)
  // console.log('------------按钮权限-----------')
  store.state.btnData = btns
  // 自定义指令，按钮权限控制
  Vue.directive('btn', {

    // 被绑定元素插入父节点时调用
    inserted(el, binding) {
      // 按钮判断

      JudgeBtn(el, binding.value, btns)
    },
    // 被绑定元素所在的模板更新时调用
    update(el, binding) {
      // 按钮判断

      JudgeBtn(el, binding.value, btns)
    }
  })
}

const color = {}

// 字体颜色判断
function judgeText (el, value) {
  if (value === undefined || value === '') {
   return  el.style.color = '#3f3f3f';
  } else {
    // 如果是带有逗号的数字格式
    if (typeof value === 'string' && value.indexOf(',') > -1) {
      value = value.replace(/,/g,'')
    }
    // 如果是数字或可以转化为数字
    if (typeof Number(value) !== 'number') return
    // 展示不同的颜色
    if (Number(value) < 0) {
      el.style.color = '#42b983';
    }
    else if(Number(value) == 0){
      el.style.color = '#3f3f3f';
    }
    else  {
      el.style.color = '#f56c6c';
    }
  }
}

// 自定义指令，字体颜色
color.install = Vue => {
  Vue.directive('color', {
    // 被绑定元素插入父节点时调用
    inserted (el, binding) {
      // 字体颜色判断
      judgeText(el, binding.value)
    },
    // 被绑定元素所在的模板更新时调用
    update (el, binding) {
      // 字体颜色判断
      judgeText(el, binding.value)
    }
  })
}

export default color

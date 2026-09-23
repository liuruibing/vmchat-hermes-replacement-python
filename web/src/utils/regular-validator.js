// 正则集合
export default {
  // 只能是字母和数字的
  en_num () {
    let obj = {
      reg:  /^[a-zA-Za-z0-9]+$/,
      msg: '请输入字母或者数字'
    }
    return obj
  },
  // 只能是字母和数字和中文
  cn_num_en () {
    let obj = {
      reg:  /^[\u4e00-\u9fa5a-zA-Z0-9]+$/,
      msg: '请输入中文，字母或者数字'
    }
    return obj
  },
  // 不存在任何校验
  empty () {
    let obj = {
      reg:  '',
      msg: ''
    }
    return obj
  }
}
export function ecmRules (data) {
  let rulesData = new Object
  for (let item of data) {
    let obj = {required: false, type: 'string',  trigger: 'change',  pattern: /^[\u4e00-\u9fa5a-zA-Z0-9]+$/, message: '请输入中文,英文或者数字' }
    rulesData[item] = obj
  }
  console.log(rulesData)
}
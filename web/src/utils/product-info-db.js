function currentBig (current, befor) {
  let tempNew = new Array
  for (let i in current) {
    if (befor[i]) {
      tempNew.push({
        ...current[i],
        'change': befor[i]
      })
    } else {
      let obj = {}
      for (let j in current[i]) obj[j] = ''
      tempNew.push({
        ...current[i],
        'change': obj
      })
    }
  }
  return tempNew
}
export function current (current, befor) {
  let tempNew = new Array
  for (let i in current) {
    if (befor[i]) {
      tempNew.push({
        ...current[i],
        'change': befor[i]
      })
    } else {
      let obj = {}
      for (let j in current[i]) obj[j] = ''
      tempNew.push({
        ...current[i],
        'change': obj
      })
    }
  }
  return tempNew
}
/* 金额（元）千分位 */
function moneyThousand(n) {
  if (!n && n !== 0) return '-'
  if (n === 0) return '0'
  // 如果前面有加减符号
  let head = ''
  if (typeof n === 'number') n = String(n)
  head = n.substring(0, 1)
  if (head === '+' || head === '-') {
    n = n.substring(1)
  } else {
    head = ''
  }
  n = n.toString().replace(/,/gi, '')
  let re = /\d{1,3}(?=(\d{3})+$)/g
  let backValue = n.replace(/^(\d+)((\.\d*)?)$/, function (s, s1, s2) {
    return s1.replace(re, '$&,') + s2
  })
  // 转换完加上加减号
  if (head) backValue = head + backValue
  return backValue
}
export function correlationData (current, befor) {
  let temp = new Array
  if (!befor) return temp = viewData(current)
  
  for (let i of current) {
    if (i.redeemFrom) i.redeemFrom = moneyThousand(i.redeemFrom)
    if (i.redeemTo) i.redeemTo = moneyThousand(i.redeemTo)
  }
  for (let i of befor) {
    if (i.redeemFrom) i.redeemFrom = moneyThousand(i.redeemFrom)
    if (i.redeemTo) i.redeemTo = moneyThousand(i.redeemTo)
  }

  for (let i of current) {
    if (i.rewardFrom) i.rewardFrom = moneyThousand(i.rewardFrom)
    if (i.rewardTo) i.rewardTo = moneyThousand(i.rewardTo)
  }
  for (let i of befor) {
    if (i.rewardFrom) i.rewardFrom = moneyThousand(i.rewardFrom)
    if (i.rewardTo) i.rewardTo = moneyThousand(i.rewardTo)
  }
  // 传来的数值必须要序列化过了
  temp = currentBig(current, befor)
  // console.log('change', temp)
  return temp
}
 function viewData (current) {
  for (let i of current) {
    if (i.redeemFrom) i.redeemFrom = moneyThousand(i.redeemFrom)
    if (i.redeemTo) i.redeemTo = moneyThousand(i.redeemTo)
  }
  for (let i of current) {
    if (i.rewardFrom) i.rewardFrom = moneyThousand(i.rewardFrom)
    if (i.rewardTo) i.rewardTo = moneyThousand(i.rewardTo)
  }
  return current
 }
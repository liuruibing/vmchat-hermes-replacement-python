export function autoScrollTo (elHeight) {
  let scrollHeight = 0
  elHeight = parseInt(elHeight)
  let wh = document.documentElement.clientHeight || document.body.parentNode.clientHeight || document.body.clientHeight
  // console.log(wh, 'wh')
  // console.log(elHeight, 'elHeight')
  return scrollHeight =  Math.abs(elHeight - wh)
}
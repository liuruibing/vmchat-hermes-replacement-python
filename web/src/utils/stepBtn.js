export function stepMenuBtn (data) {
  let menuBtn = new Object
  menuBtn = transfer(data.headNode, data.node)
  return menuBtn
}
// 转账指令流程
function transfer (headNode, node) {
  let obj = {
    hasPermissionPause: headNode + '.update.Pause.' + node,  //暂缓
    hasPermissionUnPause: headNode + '.update.UnPause.' + node,  //解除暂缓
    hasPermissionCancle: headNode + '.update.Cancle.' + node,  //撤销
    hasPermissionAbandon: headNode + '.update.Abandon.' + node,  //作废
    hasPermissionMail: headNode + '.update.Mail.' + node  //作废
  }
  return obj
}
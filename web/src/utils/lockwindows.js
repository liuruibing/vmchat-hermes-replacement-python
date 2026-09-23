import storage from '@/utils/storage'
import store from '@/store'
import router from "@/router"
// let lastTime = new Date().getSeconds()
let isLockFlag = false
let currentTime = new Date().getSeconds()  //当前时间
let noOperation = 0
let timeOut = 60 * 60 * 1000  //设置超时时间: 一小时
// let timeOut = 20000  //设置超时时间: 调试时间

window.onload = function () {
  window.document.onmousedown = function () {
    isLockFlag = true
    storage.setItem("noOperation", new Date().getSeconds())
  }
  window.document.onmousewheel = function () {
    isLockFlag = true
    storage.setItem("noOperation", new Date().getSeconds())
  }
  window.document.onmouseover = function () {
    isLockFlag = true
    storage.setItem("noOperation", new Date().getSeconds())
  }
}
function checkTimeout() {
  let isLock = storage.getItem('isLock').isLock
  // console.log(isLock, 'isLock')
  if (!isLock) {
    if (isLockFlag) {
      isLockFlag = false
      store.state.lock.isLock.isLock = storage.getItem('isLock').isLock
    } else {
      if(router.app._route.path == '/login') {
        storage.setItem('isLock', { isLock: false } )
        return
      } // 当前已经是登陆页时不做跳转
      currentTime = new Date().getSeconds()		//更新当前时间
      if (storage.getItem("noOperation")) noOperation = currentTime - storage.getItem("noOperation")
      else  noOperation += 1
      //console.log('noOperation', noOperation)
      if ( noOperation*1000 > timeOut) { //判断不操作点击或者滚动的时候执行的方法
        storage.setItem('isLock', { isLock: true })
        store.state.lock.isLock.isLock = storage.getItem('isLock').isLock
        // window.history.forward(-1)  //锁屏就无法跳转页面
      }
    }
  } else {
    // window.history.forward(-1)  //锁屏就无法跳转页面
    store.state.lock.isLock.isLock = true
  }
}
window.onbeforeunload = function () {
      clearInterval(window.setInterval)
}
export default function () {
    /* 定时器 间隔30秒检测是否长时间未操作页面 */
    // let onload = storage.getItem('isLock').isLock
    // if (!onload) storage.setItem('isLock', { isLock: false } )
    // window.setInterval(checkTimeout, 1000);
}

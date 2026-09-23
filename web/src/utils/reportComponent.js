import Vue from 'vue'

export function renderScript(component) {
  Vue.nextTick(() => {
    setTimeout(() => {
      const rootDiv = document.querySelector(`#component${component.id}`)
      if (component.info.id != "4991C3ABBD1B447795586E2A385B3F7B" && component.info.id != '7321C3ABBD1B447795586E2A385B1245') {
        rootDiv.style.border = '1px solid #cccccc'
      }
      // 生成echarts渲染dom
      const testDom = document.createElement('div')
      const testDomInnerHTML = component.info.render.div
      testDom.innerHTML = testDomInnerHTML
      testDom.style.height = '100%'
      testDom.style.width = '100%'
      testDom.style.position = 'absolute'
      // testDom.style.left = '1px'
      // testDom.style.top = '1px'
      if (component.info.id != "4991C3ABBD1B447795586E2A385B3F7B" && component.info.id != '7321C3ABBD1B447795586E2A385B1245') {
        testDom.style.backgroundColor = 'white'
      }
      testDom.style.overflow = 'hidden'
      testDom.style.display = 'flex'
      testDom.style.flexWrap = 'wrap'
      // style="height: 100%; width: 100%;background-color: white;border: 1px solid #cccccc"
      rootDiv.appendChild(testDom)
      // 生产srcipt标签并appendChild
      const newScript = document.createElement('script')
      newScript.type = 'text/javascript'
      newScript.id = `script_${component.id}`
      const newScriptInnerHTML = component.info.render.script
      newScript.innerHTML = newScriptInnerHTML
      setTimeout(() => {
        rootDiv.appendChild(newScript)
        for (const key in component.info.params) {
          if (key == 'ZB_L_FILLUP') {
            if (component.info.params && component.info.params.ZB_L_FILLUP && component.info.params.ZB_L_FILLUP.length > 0) {
              Vue.set(component.info.params, 'ZB_L_FILLUP', component.info.params.ZB_L_FILLUP)
            } else {
              Vue.set(component.info.params, 'ZB_L_FILLUP', window[`legendColor_${component.id}`])
            }
            Vue.set(component.info, 'legendArray', window[`legendName_${component.id}`])
            break
            // component.info.colorArray = ''
          }
        }
      }, 100)
    }, 100)
  })
}

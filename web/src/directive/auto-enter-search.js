//以下是焦点在查询条件上点击回车触发查询
// 匹配查询按钮的特征（可配置）
const BUTTON_MATCH_RULES = [
  { selector: '[data-enter-search]' }, // 高优先级：自定义标记属性
  { selector: '.el-button--primary' }, // Element UI主按钮
  { text: ['查询', '搜索', 'Search'] }, // 按钮文本关键词
]

const findSearchButton = (el) => {
  // 按优先级遍历匹配规则
  for (const rule of BUTTON_MATCH_RULES) {
    if (rule.selector) {
      const btn = el.querySelector(rule.selector)
      if (btn) return btn
    } else if (rule.text) {
      const buttons = el.querySelectorAll('button, .el-button')
      const match = Array.from(buttons).find(btn =>
        rule.text.some(text => btn.innerText.includes(text))
      )
      if (match) return match
    }
  }
  return null
}

export default {
  bind(el) {
    const handler = (e) => {
      if (e.key === 'Enter' && !e.target.isContentEditable) {
        const searchBtn = findSearchButton(el)
        if (searchBtn) {
          e.preventDefault()
          searchBtn.click()
        }
      }
    }
    el.addEventListener('keydown', handler)
    el._autoEnterHandler = handler
  },
  unbind(el) {
    el.removeEventListener('keydown', el._autoEnterHandler)
  }
}




//以下内容是 焦点不在查询条件上 点击回车触发查询
/* // src/directives/auto-enter-search.js
const BUTTON_MATCH_RULES = [
  { type: 'attribute', value: '[data-enter-search]' },
  { type: 'class', value: '.el-button--primary' },
  { type: 'text', values: ['查询', '搜索', 'Search'] },
]

export default {
  bind(el) {
    let cachedSearchBtn = null

    const findSearchButton = () => {
      if (cachedSearchBtn) return cachedSearchBtn

      const buttons = el.querySelectorAll('button, [role="button"]')

      for (const rule of BUTTON_MATCH_RULES) {
        if (rule.type === 'attribute') {
          const btn = el.querySelector(rule.value)
          if (btn) return cachedSearchBtn = btn
        }

        if (rule.type === 'class') {
          const btn = el.querySelector(rule.value)
          if (btn) return cachedSearchBtn = btn
        }

        if (rule.type === 'text') {
          const match = Array.from(buttons).find(function(btn) {
            // 修复点：移除可选链操作符
            const text = btn.textContent ? btn.textContent.trim() : ''
            return rule.values.some(function(t) {
              return text.indexOf(t) > -1
            })
          })
          if (match) return cachedSearchBtn = match
        }
      }
      return null
    }

    const handler = function(e) {
      if (e.key === 'Enter') {
        const ignoreTags = ['INPUT', 'TEXTAREA', 'SELECT']
        if (ignoreTags.includes(e.target.tagName)) return

        const searchBtn = findSearchButton()
        if (searchBtn) {
          e.preventDefault()
          searchBtn.click()
        }
      }
    }

    document.addEventListener('keydown', handler)
    el._enterHandler = handler
  },

  unbind(el) {
    document.removeEventListener('keydown', el._enterHandler)
  }
} */

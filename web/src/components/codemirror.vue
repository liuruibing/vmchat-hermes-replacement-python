<template>
  <div class="in-coder-panel">
    <textarea ref="textarea"></textarea>
    <div v-if="disabled" class="ddCode-mirror-disabled"></div>
    <!-- 切换语法功能暂时不需要 -->
    <!-- <el-select class="code-mode-select" v-model="mode"
               @change="changeMode">
      <el-option v-for="mode in modes"
                 :key="mode.value" :label="mode.label" :value="mode.value">
      </el-option>
    </el-select> -->
  </div>
</template>

<script>
// 引入全局实例
import _CodeMirror from 'codemirror'

// 核心样式
import 'codemirror/lib/codemirror.css'
// 引入主题后还需要在 options 中指定主题才会生效
import 'codemirror/theme/cobalt.css'
// 显示代码提示样式
import 'codemirror/addon/hint/show-hint.css'
// json格式新引入的css
import 'codemirror/addon/lint/lint.css'
import 'codemirror/theme/rubyblue.css'
// 需要引入具体的语法高亮库才会有对应的语法高亮效果
// codemirror 官方其实支持通过 /addon/mode/loadmode.js 和 /mode/meta.js 来实现动态加载对应语法高亮库
// 但 vue 貌似没有无法在实例初始化后再动态加载对应 JS ，所以此处才把对应的 JS 提前引入
import 'codemirror/mode/javascript/javascript.js'
import 'codemirror/mode/sql/sql.js'
import 'codemirror/addon/hint/show-hint'
import 'codemirror/addon/hint/show-hint'
import 'codemirror/addon/hint/sql-hint'
// json 格式新引入的js
require('script-loader!jsonlint')
import 'codemirror/addon/lint/lint'
import 'codemirror/addon/lint/json-lint'
// Python 语言
import 'codemirror/mode/python/python.js'

// sql格式化
// import sqlFormatter from "sql-formatter";

// 尝试获取全局实例
const CodeMirror = window.CodeMirror || _CodeMirror

export default {
  name: 'DdCodeMirror',
  props: {
    // 外部传入的内容，用于实现双向绑定
    // value: {},
    // 外部传入的语法类型
    language: {
      type: String,
      default: 'javascript'
    },
    // js的语言类型 分为两种 json 和 js
    scriptLanguage: {
      type: String,
      default: 'json'
    },
    // 编辑器禁用
    disabled: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      // 内部真实的内容
      code: '',
      // 默认的语法类型
      mode: 'x-sql',
      // 编辑器实例
      coder: null,
      // 默认配置
      options: {},
      // 支持切换的语法高亮类型，对应 JS 已经提前引入
      // 使用的是 MIME-TYPE ，不过作为前缀的 text/ 在后面指定时写死了
      modes: [
        {
          value: 'javascript', // js javascript暂时用不到 此类型默认为json格式
          label: 'Javascript'
        },
        {
          value: 'x-sql',
          label: 'SQL'
        },
        {
          value: 'x-python',
          label: 'Python'
        }
      ]
    }
  },
  mounted() {
    // 尝试从父容器获取语法类型
    if (this.language) {
      // 获取具体的语法类型对象
      let modeObj = this._getLanguage(this.language)
      // 判断父容器传入的语法是否被支持
      if (modeObj) {
        this.mode = modeObj.value
      }
    }
    // sql编辑器配置
    if (this.mode === 'x-sql') {
      this.options = {
        // 缩进格式
        tabSize: 2,
        // 主题，对应主题库 JS 需要提前引入
        theme: 'cobalt',
        // 显示行号
        lineNumbers: true,
        extraKeys: { Ctrl: 'autocomplete' }, //自定义快捷键
        hintOptions: {
          //自定义提示选项
          tables: {
            users: ['name', 'score', 'birthDate'],
            countries: ['name', 'population', 'size']
          }
        }
      }
    } else if (this.mode === 'javascript') {
      if (this.scriptLanguage === 'json') {
        this.options = {
          // 缩进格式
          tabSize: 2,
          // 主题，对应主题库 JS 需要提前引入
          theme: 'cobalt',
          // 显示行号
          lineNumbers: true
        }
      } else if (this.scriptLanguage === 'js') {
        this.options = {
          // 缩进格式
          tabSize: 2,
          // 主题，对应主题库 JS 需要提前引入
          theme: 'cobalt',
          // 显示行号
          lineNumbers: true
        }
      }
    } else {
      this.options = {
        // 缩进格式
        tabSize: 2,
        // 主题，对应主题库 JS 需要提前引入
        theme: 'cobalt',
        // 显示行号
        lineNumbers: true
      }
    }
    // 初始化
    this._initialize()
  },
  watch: {},
  methods: {
    getValue() {
      return this.code
    },
    appendValue(val) {
      this.coder.setValue(val)
    },
    // 初始化
    _initialize() {
      // 初始化编辑器实例，传入需要被实例化的文本域对象和默认配置
      this.coder = CodeMirror.fromTextArea(this.$refs.textarea, this.options)

      // 支持双向绑定
      this.coder.on('change', coder => {
        this.code = coder.getValue()

        if (this.$emit) {
          this.$emit('codeChange', this.code)
        }
      })

      //代码自动提示功能，记住使用cursorActivity事件不要使用change事件，这是一个坑，那样页面直接会卡死 没遇到
      //每次输入都会提示 操作体验不好
      // let self = this;
      // this.coder.on('cursorActivity', function () {
      //    self.coder.showHint()
      // })
      // 初始化代码编辑器的语法类型
      this.coder.setOption('mode', `text/${this.mode}`)
    },
    // 编辑器赋默认值
    operationVal(val) {
      // 编辑器赋值
      if (this.mode === 'x-sql') {
        //  sqlFormatter.format(val)
        this.coder.setValue(val)
      } else if (this.mode === 'javascript') {
        if (this.scriptLanguage === 'json') {
          if (val === null) {
            this.coder.setValue('')
          } else {
            this.coder.setValue(JSON.stringify(val, null, 2))
          }
        } else if (this.scriptLanguage === 'js') {
          this.coder.setValue(val)
        } else {
        }
      } else {
        this.coder.setValue(val)
      }
    },
    // 获取当前语法类型
    _getLanguage(language) {
      // 在支持的语法类型列表中寻找传入的语法类型
      return this.modes.find(mode => {
        // 所有的值都忽略大小写，方便比较
        let currentLanguage = language.toLowerCase()
        let currentLabel = mode.label.toLowerCase()
        let currentValue = mode.value.toLowerCase()

        // 由于真实值可能不规范，例如 java 的真实值是 x-java ，所以讲 value 和 label 同时和传入语法进行比较
        return currentLabel === currentLanguage || currentValue === currentLanguage
      })
    }
    // 更改语法
    // changeMode (val) {
    //   // 修改编辑器的语法配置
    //   this.coder.setOption('mode', `text/${val}`)

    //   // 获取修改后的语法
    //   let label = this._getLanguage(val).label.toLowerCase()

    //   // 允许父容器通过以下函数监听当前的语法值
    //   this.$emit('language-change', label)
    // }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss">
.CodeMirror-hints {
  z-index: 100000;
}
</style>

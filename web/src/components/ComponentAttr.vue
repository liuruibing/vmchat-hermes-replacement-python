<template>
  <div class="attr-container standard-form">
    <div class="title" style="color: #333; background-color: #e6e8ef">
      属性
      <div v-if="curComponent.info.options" style="float: right; margin-right: 5px">
        <el-button size="small" type="primary" @click="renderClick(curComponent.info, curComponent)">预览</el-button>
      </div>
    </div>
    <div style="padding-left: 10px;padding-top: 10px; overflow-y: auto">
      <div v-if="curComponent && curComponent" :style="{ height: rightHeight }" class="form-box">
        <div
          v-for="(item, index) in curComponent.info.options || []"
          v-if="item.level == 2 || (item.level == 3 && item.show == true && blackArray.indexOf(item.id) == -1)"
          :key="index"
          style="position: relative; line-height: 26px; margin-bottom: 10px"
        >
          <span v-show="item.level == 2" style="font-size: 14px; font-weight: bold; color: #A15008; width: 60px; display: inline-block">
            {{ item.name }}
          </span>
          <el-switch v-show="item.level == 2" v-model="item.show" :width="45" inactive-color="#d4d4d4" style="margin-bottom: 10px" @change="handleClickNarrow(item)"></el-switch>
          <span v-if="item.level == 3 && item.show == true" style="font-size: 14px; margin-left: 5px; color: #333; display: inline-block">
            {{ item.name }}
          </span>
          <template v-if="item.level == 3 && item.show == true && item.id == 'ZB_INDEXCODE'">
            <div style="height: auto; position: relative">
              <div>
                <span style="font-size: 14px; margin-left: 10px; color: #333; display: inline-block">基准类型</span>
                <el-select
                  v-model="curComponent.info.params.ZB_INDEXTYPE"
                  class="component-attr-input"
                  clearable
                  placeholder="请选择"
                  size="small"
                  style="position: absolute; right: 10px"
                >
                  <el-option v-for="item in ZB_INDEXTYPEOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
                </el-select>
              </div>
              <div v-show="curComponent.info.params.ZB_INDEXTYPE == 'gdjz'" class="mt10" style="position: relative; line-height: 26px; margin-bottom: 10px">
                <span style="font-size: 14px; margin-left: 10px; color: #333; display: inline-block">选择基准</span>
                <el-select
                  v-model="curComponent.info.params.ZB_INDEXCODE"
                  class="component-attr-input"
                  clearable
                  placeholder="请选择"
                  size="small"
                  style="position: absolute; right: 10px"
                >
                  <el-option v-for="item in $store.state.indexArray" :key="item.id" :label="item.label + '(' + item.id + ')'" :value="item.id"></el-option>
                </el-select>
              </div>
              <div v-show="curComponent.info.params.ZB_INDEXTYPE == 'zdyjz'" class="mt10" style="position: relative; line-height: 26px; margin-bottom: 10px">
                <span style="font-size: 14px; margin-left: 10px; color: #333; display: inline-block">基准 A</span>
                <el-select
                  v-model="curComponent.info.params.ZB_INDEXCODEA"
                  class="component-attr-input"
                  clearable
                  placeholder="请选择"
                  size="small"
                  style="position: absolute; right: 10px"
                >
                  <el-option v-for="item in $store.state.compareIndexArray" :key="item.id" :label="item.label + '(' + item.id + ')'" :value="item.id"></el-option>
                </el-select>
              </div>
              <div v-show="curComponent.info.params.ZB_INDEXTYPE == 'zdyjz'" class="mt10" style="position: relative; line-height: 26px; margin-bottom: 10px">
                <span style="font-size: 14px; margin-left: 10px; color: #333; display: inline-block">权重 A</span>
                <el-input
                  v-model="curComponent.info.params.ZB_INDEXWEIGHTA"
                  class="component-attr-input"
                  size="small"
                  style="position: absolute; right: 10px"
                  @blur="handleInputWeight('A')"
                ></el-input>
                <span style="color: #333">%</span>
              </div>
              <div v-show="curComponent.info.params.ZB_INDEXTYPE == 'zdyjz'" class="mt10" style="position: relative; line-height: 26px; margin-bottom: 10px">
                <span style="font-size: 14px; margin-left: 10px; color: #333; display: inline-block">基准 B</span>
                <el-select
                  v-model="curComponent.info.params.ZB_INDEXCODEB"
                  class="component-attr-input"
                  clearable
                  placeholder="请选择"
                  size="small"
                  style="position: absolute; right: 10px"
                >
                  <el-option v-for="item in $store.state.compareIndexArray" :key="item.id" :label="item.label + '(' + item.id + ')'" :value="item.id"></el-option>
                </el-select>
              </div>
              <div v-show="curComponent.info.params.ZB_INDEXTYPE == 'zdyjz'" class="mt10" style="position: relative; line-height: 26px; margin-bottom: 10px">
                <span style="font-size: 14px; margin-left: 10px; color: #333; display: inline-block">权重 B</span>
                <el-input
                  v-model="curComponent.info.params.ZB_INDEXWEIGHTB"
                  class="component-attr-input"
                  size="small"
                  style="position: absolute; right: 10px"
                  @blur="handleInputWeight('B')"
                ></el-input>
                <span style="color: #333">%</span>
              </div>
            </div>
          </template>
          <span v-if="item.level == 3 && item.show == true && item.id != 'ZB_INDEXCODE'" style="position: absolute; right: 10px">
            <template v-if="item.type == 'TP_SELECT' || item.type == 'TP_SELECTIMPORT'">
              <el-select v-model="curComponent.info.params[item.id]" class="component-attr-input" popper-class="global-drop-down-bg" size="small">
                <el-option v-for="temp in item.data" :key="temp.val" :label="temp.name" :value="temp.val"></el-option>
              </el-select>
            </template>
            <template v-else-if="item.type == 'TP_TEXT'">
              <span v-if="item.id == 'ZB_X_INTERVAL'">
                <el-input v-model="curComponent.info.params[item.id]" class="component-attr-input" size="small" @blur="validateInput(item.id)"></el-input>
              </span>
              <span v-else>
                <el-input v-model="curComponent.info.params[item.id]" class="component-attr-input" size="small" @blur="validateInput(item.id)"></el-input>
              </span>
            </template>
            <template v-else-if="item.type == 'FUNDCODE'">
              <el-input v-model="curComponent.info.params[item.id]" :disabled="true" class="component-attr-input" size="small"></el-input>
            </template>
            <template v-else-if="item.type == 'TP_DATE'">
              <el-date-picker
                v-model="curComponent.info.params[item.id]"
                class="component-attr-input"
                placeholder="选择日期"
                popper-class="global-drop-down-bg"
                size="small"
                type="date"
                value-format="yyyy-MM-dd"
              ></el-date-picker>
            </template>
            <template v-else-if="item.type == 'TP_COLORPICKER'">
              <el-color-picker v-model="curComponent.info.params[item.id]" class="component-attr-input" popper-class="global-drop-down-bg" size="small"></el-color-picker>
            </template>
            <template v-else-if="item.type == 'TP_INPUTNUMBER'">
              <el-input v-model.number="curComponent.info.params[item.id]" class="component-attr-input" size="small"></el-input>
            </template>
            <template v-else-if="item.type == 'TP_TXTDOUBLE'">
              <el-input
                v-model="curComponent.info.params[item.id][0].name"
                class="tp-input-style"
                size="small"
                style="box-sizing: 70px !important; width: 68px !important"
                @blur="validateInputDouble(item.id, 0)"
              ></el-input>
              <el-input
                v-model="curComponent.info.params[item.id][1].name"
                class="tp-input-style"
                size="small"
                style="box-sizing: 70px !important; width: 69px !important"
                @blur="validateInputDouble(item.id, 1)"
              ></el-input>
            </template>
            <template v-else-if="item.type == 'TP_TXTSINGLE'">
              <el-input v-model="curComponent.info.params[item.id][0].name" class="component-attr-input" size="small" @blur="validateInputSingle(item.id, 0)"></el-input>
            </template>
            <template v-else-if="item.type == 'TP_SELECTS'">
              <el-select v-model="curComponent.info.params[item.id]" class="component-attr-input" collapse-tags multiple popper-class="global-drop-down-bg" size="small">
                <el-option v-for="temp in item.data" :key="temp.val" :label="temp.name" :value="temp.val"></el-option>
              </el-select>
            </template>
            <template v-else-if="item.type == 'INDEXCODE'">
              <el-select v-model="curComponent.info.params[item.id]" class="component-attr-input" popper-class="global-drop-down-bg" size="small">
                <el-option v-for="temp in $store.state.indexArray" :key="temp.id" :label="temp.label + '(' + temp.id + ')'" :value="temp.id"></el-option>
              </el-select>
            </template>
            <template v-else-if="item.type == 'TP_IMG'">
              <div>
                <el-upload
                  :auto-upload="true"
                  :before-upload="(file) => beforeAvatarUpload(file, item)"
                  :on-success="handleAvatarSuccess"
                  :show-file-list="false"
                  action="#"
                  class="avatar-uploader"
                  size="small"
                >
                  <img v-if="curComponent.info.params[item.id]" :src="curComponent.info.params[item.id]" class="avatar" />
                  <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                </el-upload>
              </div>
            </template>
          </span>
          <template v-if="item.id == 'ZB_L_FILLUP'">
            <el-row>
              <div v-for="(stem, index) in curComponent.info.legendArray" :key="index" style="height: 26px; line-height: 26px; margin-bottom: 10px; position: relative">
                <span
                  style="
                    display: inline-block;
                    width: 60px;
                    font-size: 14px;
                    color: #333;
                    position: absolute;
                    left: 10px;
                    overflow: hidden;
                    white-space: nowrap;
                    text-overflow: ellipsis;
                  "
                  :title="curComponent.info.legendArray[index]"
                >
                  {{ curComponent.info.legendArray[index] }}
                </span>
                <el-color-picker
                  v-model="curComponent.info.params[item.id][index]"
                  class="component-attr-input"
                  popper-class="global-drop-down-bg"
                  size="small"
                  style="position: absolute; right: 10px"
                ></el-color-picker>
              </div>
            </el-row>
          </template>
        </div>
      </div>
      <div v-else style="text-align: center; color: #ccc">当前没有正在编辑的组件</div>
      <!-- 产品选择弹窗 -->
      <product-selector
        :dialog-visible="productSelectorVisible"
        :select-list="selectList"
        :show-tree-key-array="showTreeKeyArray"
        :tree-data="treeData"
        default-checked-keys="scsm"
        @closedialog="handleDialogClosed"
        @submitdialog="handleSubmitClick"
      ></product-selector>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import productSelector from '@/components/productSelectorHome'
import OPTION from '@/mock/option'
import pageApi from '@/api/templateManageMent'
import Vue from 'vue'

export default {
  components: { productSelector },
  data() {
    return {
      ZB_INDEXTYPEOption: [
        {
          id: 'gdjz',
          label: '固定基准'
        },
        {
          id: 'zdyjz',
          label: '自定义基准'
        }
      ],
      blackArray: ['ZB_INDEXTYPE', 'ZB_INDEXCODEA', 'ZB_INDEXWEIGHTA', 'ZB_INDEXCODEB', 'ZB_INDEXWEIGHTB'],
      formQuery: {},
      rightHeight: '0px',
      selectProductDialogRowPointer: null, // 选择产品弹窗对应的行对象
      productSelectorVisible: false,
      showTreeKeyArray: ['市场私募', '广发托管/外包', '我的关注'],
      selectList: [],
      treeData: [
        {
          label: '市场私募',
          id: 'scsm'
        },
        {
          label: '广发托管/外包',
          id: 'zstgwb'
        },
        {
          label: '我的关注',
          id: 'wdgz',
          children: [
            {
              label: '默认分组',
              id: 'mrfz'
            },
            {
              label: '权益组',
              id: 'qyz'
            }
          ]
        }
      ],
      filterRules: {
        type1: /^\d+$/,
        type2: /^[\u4e00-\u9fa5\w\-]+$/,
        type3: /^\d+$/,
        type4: /^[\u4e00-\u9fa5%￥]+$/,
        type5: /^[\u4E00-\u9FA5()%\-\_\/"“”'‘’]+$/u
      },
      filterMessage: {
        type1: '请输入纯数字',
        type2: '请输入汉字,字母，数字，下划线，-',
        type3: '请输入纯数字或者自适应',
        type4: '请输入纯汉字可以包含%、￥',
        type5: '请输入纯汉字，可以包含' + '（' + '）' + '%' + '——' + '_' + '/' + '""' + "''"
      }
    }
  },
  computed: mapState(['curComponent', 'curComponentIndex']),
  watch: {},
  filters: {
    autoToStr(val) {
      if (val == 'auto') {
        return '自适应'
      }
      return val
    }
  },
  created() {
    this.getRightHeight()
    window.addEventListener('resize', this.getRightHeight)
  },
  methods: {
    // 权重校验
    handleInputWeight(type) {
      const regex = /^(0(\.\d+)?|[1-9]\d*(\.\d+)?)$/
      if (type == 'A') {
        if (!regex.test(this.curComponent.info.params.ZB_INDEXWEIGHTA)) {
          this.$message.closeAll()
          this.$message.warning('只能输入大于等于0的数')
          this.curComponent.info.params.ZB_INDEXWEIGHTA = '0'
          return
        }
        if (this.curComponent.info.params.ZB_INDEXWEIGHTB != '') {
          if (Number(this.curComponent.info.params.ZB_INDEXWEIGHTA) + Number(this.curComponent.info.params.ZB_INDEXWEIGHTB) > 100) {
            this.$message.closeAll()
            this.$message.warning('基金A、B权重不能超过100%')
            this.curComponent.info.params.ZB_INDEXWEIGHTA = '0'
            return
          }
        }
      } else {
        if (!regex.test(this.curComponent.info.params.ZB_INDEXWEIGHTB)) {
          this.$message.closeAll()
          this.$message.warning('只能输入大于等于0的数')
          this.curComponent.info.params.ZB_INDEXWEIGHTB = '0'
          return
        }
        if (this.curComponent.info.params.ZB_INDEXWEIGHTA != '') {
          if (Number(this.curComponent.info.params.ZB_INDEXWEIGHTA) + Number(this.curComponent.info.params.ZB_INDEXWEIGHTB) > 100) {
            this.$message.closeAll()
            this.$message.warning('基金A、B权重不能超过100')
            this.curComponent.info.params.ZB_INDEXWEIGHTB = '0'
            return
          }
        }
      }
    },
    handleImgChange(val) {
      if (val) {
        this.$store.commit('SET_GLOBAL_IMAG_COMPONENT_ARRAY', { action: 'add', curComponent: this.curComponent })
      } else {
        this.$store.commit('SET_GLOBAL_IMAG_COMPONENT_ARRAY', { action: 'delete', curComponent: this.curComponent })
      }
    },
    validateInput(id) {
      const obj = this.curComponent.info.options.find((item) => item.id == id)
      if (obj && obj.filter) {
        const reg = new RegExp(this.filterRules[`type${obj.filter}`] || '')
        const msg = this.filterMessage[`type${obj.filter}`] || '输入有误'
        if (obj.filter === '3') {
          if (id == 'ZB_X_INTERVAL') {
            if (this.curComponent.info.params[id] == 'auto') {
              this.curComponent.info.params[id] = '自适应'
            }
            if (this.curComponent.info.params[id] == '自适应') {
              return true
            }
          }
        }
        if (obj.filter == '1' || obj.filter == '3') {
          if (this.curComponent.info.params[id] == '') {
            // this.curComponent.info.params[id] = ''
            this.$message.closeAll()
            this.$message.warning('不能为空')
            return false
          }
        }
        if (this.curComponent.info.params[id] != '' && !reg.test(this.curComponent.info.params[id])) {
          // this.curComponent.info.params[id] = ''
          this.$message.closeAll()
          this.$message.warning(msg)
          return false
        }
      }
      return true
    },
    validateInputSingle(id, index) {
      const obj = this.curComponent.info.options.find((item) => item.id == id)
      if (obj && obj.filter) {
        const reg = new RegExp(this.filterRules[`type${obj.filter}`] || '')
        const msg = this.filterMessage[`type${obj.filter}`] || '输入有误'
        if (obj.filter === '3') {
          if (this.curComponent.info.params[id][index].name == 'auto') {
            return true
          }
        }
        if (obj.filter == '1' || obj.filter == '3') {
          if (this.curComponent.info.params[id][index].name == '') {
            // this.curComponent.info.params[id][index].name = ''
            this.$message.closeAll()
            this.$message.warning('不能为空')
            return false
          }
        }
        if (this.curComponent.info.params[id] != '' && !reg.test(this.curComponent.info.params[id][index].name)) {
          // this.curComponent.info.params[id][index].name = ''
          this.$message.closeAll()
          this.$message.warning(msg)
          return false
        }
      }
      return true
    },
    validateInputDouble(id, index) {
      const obj = this.curComponent.info.options.find((item) => item.id == id)
      if (obj && obj.filter) {
        const reg = new RegExp(this.filterRules[`type${obj.filter}`] || '')
        const msg = this.filterMessage[`type${obj.filter}`] || '输入有误'
        if (obj.filter === '3') {
          if (this.curComponent.info.params[id][index].name == 'auto') {
            return true
          }
        }
        if (obj.filter == '1' || obj.filter == '3') {
          if (this.curComponent.info.params[id][index].name == '') {
            // this.curComponent.info.params[id][index].name = ''
            this.$message.closeAll()
            this.$message.warning('不能为空')
            return false
          }
        }
        if (this.curComponent.info.params[id] != '' && !reg.test(this.curComponent.info.params[id][index].name)) {
          // this.curComponent.info.params[id][index].name = ''
          this.$message.closeAll()
          this.$message.warning(msg)
          return false
        }
      }
      return true
    },
    handleDialogClosed() {
      this.productSelectorVisible = false
    },
    handleSubmitClick(arr) {
      this.productSelectorVisible = false
      this.selectList = arr
      if (this.selectList.length) {
        this.curComponent.info.params[this.selectProductDialogRowPointer] = this.selectList[0].VC_FUNDCODE
      }
    },

    // 打开产品选择 弹窗
    handleSelectProductTypeClick(id) {
      this.selectProductDialogRowPointer = id
      if (this.curComponent.info.params[id]) {
        this.selectList = [
          {
            VC_FUNDCODE: this.curComponent.info.params[id]
          }
        ]
      } else {
        this.selectList = []
      }
      this.productSelectorVisible = true
    },

    getRightHeight() {
      const rightHeight = document.getElementById('app').offsetHeight
      this.rightHeight = rightHeight - 80 - 5 - 143 + 'px'
    },
    handleAvatarSuccess() {},
    beforeAvatarUpload(file, temp) {
      const reader = new FileReader()
      reader.onload = (event) => {
        this.curComponent.info.params[temp.id] = event.target.result
      }
      reader.readAsDataURL(file)

      return false
    },
    handleClickNarrow(item) {
      this.curComponent.info.options.forEach((stem) => {
        if (stem.pid == item.id) {
          stem.show = item.show
        }
      })
    },
    isNarrowUp(item) {
      if (item.show === true) {
        return 'el-icon-arrow-up'
      } else {
        return 'el-icon-arrow-down'
      }
    },
    // 校验 查询逻辑
    checkRender(info) {
      // 先循环遍历info下的options 所有用户的配置属性
      for (const key in info.params) {
        const obj = this.curComponent.info.options.find((item) => item.id == key)
        if (obj && obj.filter) {
          if (obj.type == 'TP_TXTDOUBLE') {
            if (this.validateInputDouble(key, 0) == false || this.validateInputDouble(key, 1) == false) {
              return false
            }
          } else if (obj.type == 'TP_TXTSINGLE') {
            if (this.validateInputSingle(key, 0) == false) {
              return false
            }
          } else {
            if (this.validateInput(key) == false) {
              return false
            }
          }
        }
      }

      return true
    },

    // 点击预览
    renderClick(info, curComponent) {
      if (!this.checkRender(info)) {
        // 把当前组件的边框变红
        const rootDiv = document.querySelector(`#component${curComponent.id}`)
        if (rootDiv) {
          rootDiv.style.border = '1px solid red'
        }
        this.$message.closeAll()
        this.$message.warning('校验不通过')
        return
      } else {
        const rootDiv = document.querySelector(`#component${curComponent.id}`)
        if (rootDiv) {
          if (rootDiv.style.border == '1px solid red') {
            rootDiv.style.border = '1px solid #cccccc'
          }
        }
      }
      const params = { ...this.$store.state.canvasGlobalConfig, ...info.params }
      params.moduleId = info.id
      if (params.ZB_INDEXTYPE != 'zdyjz') {
        params.ZB_INDEXCODEA = params.ZB_INDEXCODE
        params.ZB_INDEXWEIGHTA = 100
        params.ZB_INDEXCODEB = '000300'
        params.ZB_INDEXWEIGHTB = 0
        // params.ZB_FUNDCODE = [params.ZB_INDEXCODEA, params.ZB_INDEXWEIGHTA, params.ZB_INDEXCODEB, params.ZB_INDEXWEIGHTB].toString()
      }
      if (params.ZB_X_INTERVAL && params.ZB_X_INTERVAL == '自适应') {
        params.ZB_X_INTERVAL = 'auto'
      }
      pageApi.render(params).then((res) => {
        let { status, data } = res.data
        if (status == 200) {
          const scriptStr = `;
                var dom = document.getElementById('component${curComponent.id}')
                if(dom && dom.childNodes.length > 1) {
                  dom.childNodes[0].style.display = 'none'
                  dom.childNodes[1].style.display = 'flex'
                }
              `
          // 重新渲染div
          data = data.replaceAll('#uuid#', curComponent.id)
          let script = data.match(/<script\b[^>]*>([\s\S]*?)<\/script>/gm)[0]
          const div = data.replace(script, '')
          script = script.replace(/<script\s+type="text\/javascript"\s*>/g, '')
          script = script.replace(/<\/script>/g, '')
          script += scriptStr
          curComponent.info.render.script = script
          Vue.nextTick(() => {
            setTimeout(() => {
              const rootDiv = document.querySelector(`#component${curComponent.id}`)
              var deleteJs = document.getElementById(`script_${curComponent.id}`)
              deleteJs && deleteJs.remove()

              // 生产srcipt标签并appendChild
              const newScript = document.createElement('script')
              newScript.type = 'text/javascript'
              newScript.id = `script_${curComponent.id}`
              const newScriptInnerHTML = curComponent.info.render.script
              newScript.innerHTML = newScriptInnerHTML
              setTimeout(() => {
                rootDiv.appendChild(newScript)
              }, 100)
            }, 100)
          })
        } else if (status == 501) {
          const scriptStr = `;
                var dom = document.getElementById('component${curComponent.id}')
                if(dom && dom.childNodes.length > 1) {
                  dom.childNodes[0].style.display = 'flex'
                  dom.childNodes[1].style.display = 'none'
                }
              `
          curComponent.info.render.script = scriptStr

          Vue.nextTick(() => {
            setTimeout(() => {
              const rootDiv = document.querySelector(`#component${curComponent.id}`)
              var deleteJs = document.getElementById(`script_${curComponent.id}`)
              deleteJs && deleteJs.remove()

              // 生产srcipt标签并appendChild
              const newScript = document.createElement('script')
              newScript.type = 'text/javascript'
              newScript.id = `script_${curComponent.id}`
              const newScriptInnerHTML = curComponent.info.render.script
              newScript.innerHTML = newScriptInnerHTML
              setTimeout(() => {
                rootDiv.appendChild(newScript)
              }, 100)
            }, 100)
          })
        }
      })
    },
    onQuery() {
      const curComponent = this.curComponent
      console.log(curComponent)
      const rootDiv = document.querySelector(`#component${curComponent.id}`)
      var deleteJs = document.getElementById(`script_${curComponent.id}`)
      deleteJs && deleteJs.remove()
      const newScript = document.createElement('script')
      newScript.type = 'text/javascript'
      newScript.id = `script_${curComponent.id}`
      if (curComponent.info.id === 'text-001') {
        const scriptConent = OPTION.scriptTxt1.replace('$id$', curComponent.id)
        const arr = scriptConent.split('option = {')
        const curScriptConent = `${arr[0]}option = {title: {text: '${curComponent.info.options[0].value}'},${arr[1]}`
        newScript.innerHTML = curScriptConent
        this.curComponent.info.render.script = curScriptConent
      } else if (curComponent.info.id === 'text-002') {
        const scriptConent = OPTION.scriptTxt2.replace('$id$', curComponent.id)
        const arr = scriptConent.split('option = {')
        const curScriptConent = `${arr[0]}option = {title: {text: '${curComponent.info.options[0].value}'},${arr[1]}`
        newScript.innerHTML = curScriptConent
        this.curComponent.info.render.script = curScriptConent
      } else if (curComponent.info.id === 'table-001') {
        const scriptConent = OPTION.scriptTxt3.replace('$id$', curComponent.id)
        const curScriptConent = scriptConent.replace('var title = "基本信息"', `var title = "${curComponent.info.options[0].value}"`)
        newScript.innerHTML = curScriptConent
        this.curComponent.info.render.script = curScriptConent
      }

      setTimeout(() => {
        rootDiv.appendChild(newScript)
      }, 200)
    }
  }
}
</script>

<style lang="scss" scoped>
::v-deep .el-picker-panel__icon-btn {
  color: #ffffff;
}

::v-deep .el-select .el-tag {
  max-width: 60px !important;
}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #e19c5d;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}

.avatar {
  width: 178px;
  display: block;
}

.attr-container {
  height: 100%;
  //padding-left: 10px;

  .narrow {
    margin-left: 5px;
  }

  .narrow:hover {
    cursor: pointer;
  }

  ::v-deep .el-input__suffix {
    top: 3px;
    font-size: 14px;
  }

  .el-date-editor {
    ::v-deep .el-input__suffix {
      top: -3px !important;
    }
  }

  ::v-deep .el-input__prefix,
  .el-input__suffix {
    top: -3px;
  }

  ::v-deep .el-select .el-input .el-select__caret {
    font-size: 14px;
  }

  ::v-deep .el-form-item__label {
    // color: '#fff' !important;
  }

  ::v-deep .el-dialog__header {
    // background-color: #141414;
    font-size: 16px !important;
    padding: 5px !important;
  }

  ::v-deep .el-dialog__footer {
    padding: 3px !important;
    margin-top: -15px;
    padding-right: 8px !important;
    // background-color: #141414;
  }

  ::v-deep .el-dialog__body {
    // background-color: #141414;
    padding: 8px !important;
    padding-top: 0px !important;
  }

  ::v-deep .el-dialog__title {
    color: white !important;
  }

  .tp-input-style {
    ::v-deep .el-input__inner {
      width: 70px !important;
      padding: 0 5px;
    }
  }

  ::v-deep .el-input--small .el-input__inner {
    height: 26px;
    //background-color: #202020;
    // background-color: #1a222d;
    // color: #fff !important;
    // padding-left: 5px;
    // border: 0.5px solid #6d6d6d;
    width: 140px;
  }

  ::v-deep .el-button.el-button--primary {
    // background-color: #1a222d;
    // color: #fff;
  }

  ::v-deep .el-color-picker--small .el-color-picker__trigger {
    height: 26px;
    // border: 0.5px solid #6d6d6d;
    color: #a4a4a4;
  }

  ::v-deep .el-color-picker--small .el-color-picker__trigger {
    width: 140px;
  }

  ::v-deep .el-icon-arrow-down:before {
    content: none;
  }

  .component-attr-input {
    width: 140px !important;

    ::v-deep .el-picker-panel__icon-btn {
      // color: #ffffff !important;
    }

    ::v-deep .el-input--small .el-input__inner {
      width: 140px !important;
    }

    ::v-deep .el-input__inner {
      width: 140px !important;
    }

    ::v-deep .el-tag .el-tag--info .el-tag--mini .el-tag--light {
      max-width: 50px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    ::v-deep .el-input__suffix {
      //right: 20px;
    }

    ::v-deep .el-input--small,
    .form_inline_search .el-date-editor.el-input {
      width: 140px !important;
    }
  }

  .title {
    text-align: center;
    //margin-bottom: 10px;
    height: 40px;
    line-height: 40px;
    //border: 1px solid #5d5d5d;
    font-size: 14px;
    font-weight: 500;
    // color: '#fff' !important;
  }

  .form-box {
    //background-color: #282828;
    //height: 100%;
    overflow-y: auto;
  }
}
</style>

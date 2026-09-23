<template>
  <div id="moreQuery">
    <el-form
      ref="queryForm"
      :inline="true"
      :model="clsjSection"
      :rules="searchRules"
      label-position="left"
      size="small"
    >
      <!-- 投资策略 -->
      <el-row class="tzcl">
        <el-form-item label="投资策略" label-width="70px" style="display:flex; align-items:center">
          <span class="tzclbx" style="font-size: 14px;padding: 4px 10px" @click="handleBxBtn('.tzclbx')">
            不限
          </span>
          <span
            v-for="ele in investStrategy"
            :key="ele.id"
            :class="ele.checked ? 'itemBox-checked' : 'itemBox'"
          >
            <el-checkbox
              v-model="ele.checked"
              :label="ele.label"
              @change="handleCheckedChange($event, '.tzclbx', ele)"
            />
          </span>
        </el-form-item>
      </el-row>
      <!--  运行状态 / 是否分级 / 净值频率 / 绩效评级 -->
      <el-row class="jzpl">
        <el-form-item
          v-for="e in yxztData"
          :key="e.mid"
          :label="e.title"
          :label-width="e.width"
          style="display:flex; align-items:center"
        >
          <div style="display: flex; align-items:center">
            <div style="margin-right: 20px">
              <el-radio
                v-for="k in e.options"
                :key="k.id"
                v-model="e.checked"
                :label="k.id"
                border
                size="small"
                @input="yxztChangeRadio"
              >
                {{ k.label }}
              </el-radio>
            </div>
          </div>
        </el-form-item>
        <el-form-item
          v-for="e in sffjData"
          :key="e.mid"
          :label="e.title"
          :label-width="e.width"
          style="display:flex; align-items:center"
        >
          <div style="display: flex; align-items:center">
            <div style="margin-right: 20px">
              <el-radio
                v-for="k in e.options"
                :key="k.id"
                v-model="e.checked"
                :label="k.id"
                border
                size="small"
                @input="sffjChangeRadio"
              >
                {{ k.label }}
              </el-radio>
            </div>
          </div>
        </el-form-item>
        <el-form-item
          v-for="e in jzplOptions"
          :key="e.mid"
          :label="e.title"
          :label-width="e.width"
          style="display:flex; align-items:center"
        >
          <el-select v-model="e.selected" size="small" style="margin-right: 15px" @change="jzplChangeSelect">
            <el-option v-for="item in e.options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item
          class="jxpjitem"
          label="绩效评级"
          label-width="70px"
          style="display:flex; align-items:center"
        >
          <div v-for="e in jxpjOptions" :key="e.mid" style="display: flex; align-items:center">
            <el-select
              v-model="e.selected"
              :placeholder="e.placeholder"
              size="small"
              style="margin-right: 15px"
              @change="jxpjChangeSelect"
            >
              <el-option
                v-for="item in e.selectOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </div>
        </el-form-item>
      </el-row>
      <!-- 成立时间 / 资产净值 -->
      <el-row class="clsj">
        <el-form-item label="成立时间" label-width="70px" style="display:flex; align-items:center">
          <el-select
            v-model="clsjSelect"
            placeholder="请选择"
            size="small"
            style="margin-right: 15px"
            @change="handleDateChange"
          >
            <el-option
              v-for="item in clsjOptions"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item prop="startDate">
          <el-date-picker
            v-model="clsjSection.startDate"
            :disabled="disabledStart"
            placeholder="选择开始日期"
            type="date"
            value-format="yyyy-MM-dd"
          />
        </el-form-item>
        <el-form-item prop="endDate">
          <el-date-picker
            v-model="clsjSection.endDate"
            :disabled="disabledEnd"
            placeholder="选择结束日期"
            type="date"
            value-format="yyyy-MM-dd"
          />
        </el-form-item>
        <el-form-item
          :class="clsjSection.startDate || clsjSection.endDate ? 'submit-icon' : 'submit-icon-disabled'"
        >
          <el-button
            circle
            icon="el-icon-check"
            type="primary"
            @click="clsjSubmit"
            style="margin-right:20px"
          ></el-button>
        </el-form-item>
        <el-form-item
          v-for="e in zcjz"
          :key="e.mid"
          :label="e.title"
          :label-width="e.width"
          style="display:flex; align-items:center"
        >
          <el-input
            v-model="e.start"
            onkeyup="value=value.replace(/[^0-9.-]/g,'').replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3')"
            size="small"
            style="width: 60px!important"
          />
          <span>-</span>
          <el-input
            v-model="e.end"
            onkeyup="value=value.replace(/[^0-9.-]/g,'').replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3')"
            size="small"
            style="width: 60px!important"
          />
          <span :class="e.start && e.end ? 'submit-icon' : 'submit-icon-disabled'">
            <el-button circle icon="el-icon-check" type="primary" @click="addTagInput(e, '7')"></el-button>
          </span>
        </el-form-item>
        <el-form-item
          v-for="b in ljjz"
          :key="b.mid"
          :label="b.title"
          :label-width="b.width"
          style="display:flex; align-items:center"
        >
          <el-input
            v-model="b.start"
            onkeyup="value=value.replace(/[^0-9.-]/g,'').replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3')"
            size="small"
            style="width: 60px!important"
          />
          <span>-</span>
          <el-input
            v-model="b.end"
            onkeyup="value=value.replace(/[^0-9.-]/g,'').replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3')"
            size="small"
            style="width: 60px!important"
          />
          <span :class="b.start && b.end ? 'submit-icon' : 'submit-icon-disabled'">
            <el-button circle icon="el-icon-check" type="primary" @click="addTagInput(b, '20')"></el-button>
          </span>
        </el-form-item>
        <el-form-item
          v-for="b in zcjzs"
          :key="b.mid"
          :label="b.title"
          :label-width="b.width"
          style="display:flex; align-items:center"
        >
          <el-input
            v-model="b.start"
            onkeyup="value=value.replace(/[^0-9.-]/g,'').replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3')"
            size="small"
            style="width: 60px!important"
          />
          <span>-</span>
          <el-input
            v-model="b.end"
            onkeyup="value=value.replace(/[^0-9.-]/g,'').replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3')"
            size="small"
            style="width: 60px!important"
          />
          <span>(万元)</span>
          <span :class="b.start && b.end ? 'submit-icon' : 'submit-icon-disabled'">
            <el-button circle icon="el-icon-check" type="primary" @click="addTagInput(b, '21')"></el-button>
          </span>
        </el-form-item>
      </el-row>
      <!-- 计算区间 / 收益率 / 最大回撤 / sharpe比率 / Treynor比率 / jensen指数-->
      <el-row class="jsqj">
        <el-form-item
          v-for="e in jsqjOptions"
          :key="e.mid"
          :label="e.title"
          :label-width="e.width"
          style="display:flex; align-items:center"
        >
          <el-select v-model="e.selected" size="small" style="margin-right: 15px" @change="jsqjChangeSelect">
            <el-option v-for="item in e.options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item
          v-for="e in sylzdhcData"
          :key="e.id"
          :label="e.title"
          :label-width="e.width"
          style="display:flex; align-items:center;margin-right: 30px"
        >
          <el-input
            v-model="e[`start${currentJsqjValue}`]"
            onkeyup="value=value.replace(/[^0-9.-]/g,'').replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3')"
            size="small"
            style="width: 60px!important"
          />
          <span v-if="!['Sharpe比率', 'Treynor比率'].includes(e.title)">%</span>
          <span>-</span>
          <el-input
            v-model="e[`end${currentJsqjValue}`]"
            onkeyup="value=value.replace(/[^0-9.-]/g,'').replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3')"
            size="small"
            style="width: 60px!important"
          />
          <span v-if="!['Sharpe比率', 'Treynor比率'].includes(e.title)">%</span>
          <span
            :class="
              e[`start${currentJsqjValue}`] && e[`end${currentJsqjValue}`]
                ? 'submit-icon'
                : 'submit-icon-disabled'
            "
          >
            <el-button circle icon="el-icon-check" type="primary" @click="addJsqjInput(e, e.id)"></el-button>
          </span>
        </el-form-item>
      </el-row>
      <!-- 已选条件 -->
      <el-row class="yxtj">
        <el-form-item
          label="已选条件"
          label-width="70px"
          style="display:flex; align-items:center;margin-bottom: 0px!important;"
        >
          <div class="tag-list">
            <el-tag
              v-for="(tag, i) in dynamicTags"
              :key="i"
              :disable-transitions="false"
              closable
              style="margin-left: 10px;"
              @close="handleClose(tag)"
            >
              <span v-if="['6', '7', '15', '16', '17', '18','20','21'].includes(tag.id)">
                {{ tag.title + '：' + tag.start + '-' + tag.end }}
              </span>
              <span v-else-if="['1', '2', '3', '4', '5'].includes(tag.id)">
                {{ tag.title + '：' + tag.value | ensWithStr }}
              </span>
              <span v-else>
                {{ tag.prefix + tag.title + '：' + tag.start + '-' + tag.end }}
              </span>
            </el-tag>
          </div>
        </el-form-item>
      </el-row>
    </el-form>
  </div>
</template>

<script>
import constant from './constant.js'
import { centerTreeDataRight } from '@/components/tableHeadComponent/constant.js'
import request from '@/utils/request'

export default {
  name: 'AllMarketQuery',
  filters: {
    ensWithStr(val) {
      if (val.endsWith('，') || val.endsWith(',')) {
        val = val.slice(0, -1)
      }
      return val
    }
  },
  props: {
    switchPageType: {
      type: String,
      default: '1'
    },
    sqlObj: {
      type: Object,
      default: () => {}
    }
  },
  data() {
    /** 开始日期校验 */
    const validateStartDate = (rule, value, callback) => {
      if (
        this.clsjSection.endDate !== null ||
        this.clsjSection.endDate !== undefined ||
        this.clsjSection.endDate !== ''
      ) {
        const startTime = new Date(value)
        const endTime = new Date(this.clsjSection.endDate)
        if (startTime > endTime) {
          callback(new Error('开始日期不能大于结束日期'))
        } else {
          callback()
        }
      } else {
        callback()
      }
    }
    /** 结束日期校验 */
    const validateEndDate = (rule, value, callback) => {
      if (
        this.clsjSection.startDate !== null ||
        this.clsjSection.startDate !== undefined ||
        this.clsjSection.startDate !== ''
      ) {
        const startTime = new Date(this.clsjSection.startDate)
        const endTime = new Date(value)
        if (startTime > endTime) {
          callback(new Error('结束日期不能小于开始日期'))
        } else {
          callback()
        }
      } else {
        callback()
      }
    }
    return {
      // 开始/结束时间校验规则
      searchRules: {
        startDate: [{ validator: validateStartDate, trigger: 'blur' }],
        endDate: [{ validator: validateEndDate, trigger: 'blur' }]
      },
      // 投资策略
      investStrategy: [],
      // 成立时间
      clsjOptions: constant.clsjOptions,
      // 成立时间绑定值
      clsjSelect: '1',
      // 时间区间绑定值
      clsjSection: {
        startDate: '',
        endDate: ''
      },
      // 控制时间选择禁用
      disabledStart: true,
      disabledEnd: true,
      // 资产净值
      zcjz: constant.zcjz,
      // 累计净值
      ljjz: constant.ljjz,
      // 资产净值
      zcjzs: constant.zcjzs,
      // 计算区间
      jsqjOptions: constant.jsqjOptions,
      // 当前计算区间label
      currentJsqj: '近六月',
      // 当前计算区间value
      currentJsqjValue: 1,
      // 计算区间数据存储
      calculateSection: {},
      // 存储对应key计算区间
      calculateCheck: [],
      // 收益率 / 最大回撤 / sharpe比率 / Treynor比率 / jensen指数
      sylzdhcData: constant.sylzdhcData,
      // 净值频率
      jzplOptions: constant.jzplOptions,
      // 运行状态
      yxztData: constant.yxztData,
      // 是否分级
      sffjData: constant.sffjData,
      // 成立以来大类资产占比
      sinceThe: constant.sinceThe,
      // 绩效评级
      jxpjOptions: constant.jxpjOptions,
      // 已选条件
      dynamicTags: [],

      filterAlphaArr: [],
      centerTreeDataRight: centerTreeDataRight,
      AlphaObj: {}
    }
  },
  watch: {
    clsjSelect(val) {
      if (val === '1') {
        this.disabledStart = true
        this.disabledEnd = true
      }
    },
    dynamicTags(val) {
      const obj = {
        query: val,
        status: '1'
      }
      this.$emit('updateSelect', obj)
    }
  },
  mounted() {
    this.getInvestStrategyList(this.sqlObj)
    this.yxztChangeRadio(1)
    this.filterAlphaItem()
    if (this.filterAlphaArr.indexOf(this.currentJsqj) == -1) {
      this.AlphaObj = this.sylzdhcData[this.sylzdhcData.length - 1]
    } else {
      this.AlphaObj = this.sylzdhcData.pop()
    }
  },
  methods: {
    /**
     * @description 获取投资策略数据
     */
    getInvestStrategyList(param) {
      request({
        url: `/api/report/v1.0/data/sql/${param.indexCode}`,
        method: 'post',
        data: param
      }).then(res => {
        if (res.data.status === 0) {
          const resultDim = res.data.data || []
          this.investStrategy = resultDim.map(item => {
            return {
              label: item.DIM_NME,
              id: item.DIM_CDE,
              checked: false
            }
          })
        }
      })
    },
    /**
     * @description 循环数据过滤
     */
    filterData(id, name) {
      let obj = {}
      switch (name) {
        case 'clyl':
          obj = this.sinceThe.find(item => item.id === id)
          break
        default:
          break
      }
      return obj
    },
    /**
     * @description 监听鼠标移入input
     */
    inputMouserIn(id, name) {
      const obj = this.filterData(id, name)
      obj.isShow = true
    },
    /**
     * @description 监听鼠标移出input
     */
    inputMouseOut(id, name, key) {
      const obj = this.filterData(id, name, key)
      obj.isShow = false
    },
    /**
     * @description 投资策略点击不限取消所有checkbox选中
     */
    handleBxBtn(val) {
      // 获取对应dom节点修改样式
      const Dom = document.querySelector(val)
      Dom.style.backgroundColor = '#dcedff'
      Dom.style.color = '#4f95dd'
      Dom.style.borderColor = '#dcdfe6'
      if (val === '.tzclbx') {
        // 点击不限时所有checkbox状态改为false => 投资策略
        this.investStrategy.forEach(item => {
          if (item.checked) {
            item.checked = false
          }
        })
        const investIndex = this.dynamicTags.findIndex(item => item.id === '1')
        this.dynamicTags.splice(investIndex, 1)
      }
    },
    /**
     * @description 投资策略监听联动
     */
    handleCheckedChange(e, val, ele) {
      const checkedArr = this.investStrategy.filter(item => item.checked)
      const _index = this.dynamicTags.findIndex(item => item.id === '1')
      if (_index < 0 && checkedArr.length) {
        this.dynamicTags.push({
          id: '1',
          title: '投资策略',
          value: checkedArr.map(item => item.label).join('，') + '，',
          code: checkedArr.map(item => item.id).join('，') + '，'
        })
      } else {
        if (e === true) {
          this.dynamicTags[_index].value = this.dynamicTags[_index].value + '' + ele.label + '，'
          this.dynamicTags[_index].code = this.dynamicTags[_index].code + '' + ele.id + '，'
        } else {
          if (!checkedArr.length) {
            const investIndex = this.dynamicTags.findIndex(item => item.id === '1')
            this.dynamicTags.splice(investIndex, 1)
            const DomBx = document.querySelector(val)
            DomBx.style.backgroundColor = '#dcedff'
            DomBx.style.color = '#4f95dd'
            DomBx.style.borderColor = 'transparent'
            return
          }
          const regValue = new RegExp(`${ele.label}，`, 'g')
          const regCode = new RegExp(`${ele.id}，`, 'g')
          this.dynamicTags[_index].value = this.dynamicTags[_index].value.replace(regValue, '')
          this.dynamicTags[_index].code = this.dynamicTags[_index].code.replace(regCode, '')
        }
      }
      // 获取对应dom节点修改样式
      const Dom = document.querySelector(val)
      Dom.style.backgroundColor = '#fff'
      // Dom.style.color = '#333'
      Dom.style.color = '#333'
      Dom.style.borderColor = '#dcdfe6'
    },
    /**
     * @description 成立时间区间映射
     */
    handleDateChange(val) {
      if (val === '7') {
        this.disabledStart = false
        this.disabledEnd = false
      } else if (val === '1') {
        this.clsjSection.startDate = ''
        this.clsjSection.endDate = ''
      } else {
        this.disabledStart = true
        this.disabledEnd = true
        this.clsjSection.startDate = constant.dateShortcutMap[val].onClick()[0]
        this.clsjSection.endDate = constant.dateShortcutMap[val].onClick()[1]
      }
    },
    /**
     * @description 成立时间submit
     */
    clsjSubmit() {
      if (this.clsjSelect === '7') {
        if (this.clsjSection.startDate === '' && this.clsjOptions.endDate === '') {
          this.$message({
            type: 'warning',
            message: '请选择成立时间'
          })
          return
        }
      }
      const _index = this.dynamicTags.findIndex(item => item.id === '6')
      if (this.clsjSelect === '1') {
        const clsjIndex = this.dynamicTags.findIndex(item => item.id === '6')
        this.dynamicTags.splice(clsjIndex, 1)
        return
      }
      this.$refs.queryForm.validate(valid => {
        if (valid) {
          // 当重复添加相同数据时提示
          let flag = false
          this.dynamicTags.forEach(item => {
            if (item.id === '6') {
              if (item.start === this.clsjSection.startDate && item.end === this.clsjSection.endDate) {
                flag = true
              }
            }
          })
          if (flag) {
            this.$message({
              message: '已添加相同区间筛选条件',
              type: 'warning'
            })
            return
          }
          if (_index < 0) {
            this.dynamicTags.push({
              id: '6',
              title: '成立时间',
              start: this.clsjSection.startDate || '',
              end: this.clsjSection.endDate || ''
            })
          } else {
            this.dynamicTags[_index].start = this.clsjSection.startDate
            this.dynamicTags[_index].end = this.clsjSection.endDate
          }
        } else {
          return false
        }
      })
    },
    /**
     * @description 运行状态监听radio
     */
    yxztChangeRadio(val) {
      const _index = this.dynamicTags.findIndex(item => item.id === '2')
      const yxztObj = this.yxztData[0].options.find(item => item.id === val)
      if (val === 2) {
        const yxztIndex = this.dynamicTags.findIndex(item => item.id === '2')
        this.dynamicTags.splice(yxztIndex, 1)
        return
      }
      if (_index < 0) {
        this.dynamicTags.push({
          id: '2',
          title: '运行状态',
          value: yxztObj.label,
          code: val
        })
      } else {
        this.dynamicTags[_index].value = yxztObj.label
        this.dynamicTags[_index].code = val
      }
    },
    /**
     * @description 是否分级监听radio
     */
    sffjChangeRadio(val) {
      const _index = this.dynamicTags.findIndex(item => item.id === '3')
      const sffjObj = this.sffjData[0].options.find(item => item.id === val)
      if (val === 2) {
        const sffjIndex = this.dynamicTags.findIndex(item => item.id === '3')
        this.dynamicTags.splice(sffjIndex, 1)
        return
      }
      if (_index < 0) {
        this.dynamicTags.push({
          id: '3',
          title: '是否分级',
          value: sffjObj.label,
          code: val
        })
      } else {
        this.dynamicTags[_index].value = sffjObj.label
        this.dynamicTags[_index].code = val
      }
    },
    /**
     * @description 净值频率监听下拉
     */
    jzplChangeSelect(val) {
      const _index = this.dynamicTags.findIndex(item => item.id === '4')
      const jzplObj = this.jzplOptions[0].options.find(item => item.value === val)
      if (val === 3) {
        const jzplIndex = this.dynamicTags.findIndex(item => item.id === '4')
        this.dynamicTags.splice(jzplIndex, 1)
        return
      }
      if (_index < 0) {
        this.dynamicTags.push({
          id: '4',
          title: '净值频率',
          value: jzplObj.label,
          code: val
        })
      } else {
        this.dynamicTags[_index].value = jzplObj.label
        this.dynamicTags[_index].code = val
      }
    },
    /**
     * @description 绩效评级监听下拉
     */
    jxpjChangeSelect(val) {
      const _index = this.dynamicTags.findIndex(item => item.id === '5')
      const jxpjObj = this.jxpjOptions[0].selectOptions.find(item => item.value === val)
      if (val === 0) {
        const jxpjIndex = this.dynamicTags.findIndex(item => item.id === '5')
        this.dynamicTags.splice(jxpjIndex, 1)
        return
      }
      if (_index < 0) {
        this.dynamicTags.push({
          id: '5',
          title: '绩效评级',
          value: jxpjObj.label,
          code: val
        })
      } else {
        this.dynamicTags[_index].value = jxpjObj.label
        this.dynamicTags[_index].code = val
      }
    },
    /**
     * @description 获取计算区间
     */
    jsqjChangeSelect(val) {
      const jsqjObj = this.jsqjOptions[0].options.find(item => item.value === val)
      this.currentJsqj = jsqjObj.label
      this.currentJsqjValue = val
      this.filetData(jsqjObj.label)
    },
    filetData(label) {
      let AlphaObj = this.sylzdhcData.find(item => {
        return item.title == 'Alpha'
      })
      if (this.filterAlphaArr.indexOf(label) == -1) {
        //显示Alpha
        if (!AlphaObj) {
          this.sylzdhcData.push(this.AlphaObj)
        }
      } else {
        //去除Alpha
        if (AlphaObj) {
          this.sylzdhcData.pop()
        }
      }
    },
    /**
     * @description input相关submit => 计算区间见下addJsqjInput
     */
    addTagInput(obj, id) {
      // 校验输入框
      const isVaildate = this.validateInput(obj)
      if (isVaildate) {
        // 当重复添加相同数据时提示
        let flag = false
        this.dynamicTags.forEach(item => {
          if (item.id === id) {
            if (item.start === obj.start && item.end === obj.end) {
              flag = true
            }
          }
        })
        if (flag) {
          this.$message({
            message: '已添加相同区间筛选条件',
            type: 'warning'
          })
          return
        }
        // 当重复添加不同数据时替换
        const _index = this.dynamicTags.findIndex(item => item.id === id)
        if (_index < 0) {
          // 新增入标签数组
          const temp = {
            id,
            title: obj.title,
            start: obj.start,
            end: obj.end,
            name: obj.name || '',
            prefix: this.currentJsqj || ''
          }
          this.dynamicTags.push(temp)
        } else {
          this.dynamicTags[_index].start = obj.start
          this.dynamicTags[_index].end = obj.end
          this.dynamicTags[_index].prefix = this.currentJsqj
        }
      }
    },
    /**
     * @description 计算区间相关submit
     */
    addJsqjInput(obj, id) {
      // 校验输入框
      const isVaildate = this.validateInputJSQJ(obj)
      if (isVaildate) {
        // 当重复添加相同数据时提示
        let flag = false
        this.dynamicTags.forEach(item => {
          let tempID = id
          if (obj.type && obj.type === 'jsqj') {
            tempID = this.currentJsqj + id
          }
          if (item.id === tempID) {
            if (item.prefix === this.currentJsqj) {
              if (
                item.start === obj[`start${this.currentJsqjValue}`] &&
                item.end === obj[`end${this.currentJsqjValue}`]
              ) {
                flag = true
              }
            }
          }
        })
        if (flag) {
          this.$message({
            message: '已添加相同区间筛选条件',
            type: 'warning'
          })
          return
        }
        // 当重复添加不同数据时替换
        let _index = -1
        if (obj.type && obj.type === 'jsqj') {
          _index = this.dynamicTags.findIndex(item => item.id === this.currentJsqj + id)
        } else {
          _index = this.dynamicTags.findIndex(item => item.id === id)
        }
        let temp = []
        if (_index < 0) {
          if (obj.type && obj.type === 'jsqj') {
            // 新增入标签数组
            temp = {
              id: this.currentJsqj + id,
              title: obj.title,
              start: obj[`start${this.currentJsqjValue}`],
              end: obj[`end${this.currentJsqjValue}`],
              type: obj.type,
              prefix: this.currentJsqj || ''
            }
          } else {
            temp = {
              id: id,
              title: obj.title,
              start: obj[`start${this.currentJsqjValue}`],
              end: obj[`end${this.currentJsqjValue}`],
              type: obj.type,
              prefix: this.currentJsqj || ''
            }
          }
          this.dynamicTags.push(temp)
          // 存储对应区间数据
          this.calculateCheck.push(temp)
          this.$set(this.calculateSection, this.currentJsqjValue, this.calculateCheck)
          this.calculateCheck = []
        } else {
          this.dynamicTags.forEach(item => {
            let tempID = id
            if (obj.type && obj.type === 'jsqj') {
              tempID = this.currentJsqj + id
            }
            if (item.id === tempID) {
              if (item.prefix !== this.currentJsqj) {
                const temp = {
                  id: '1',
                  title: obj.title,
                  start: obj[`start${this.currentJsqjValue}`],
                  end: obj[`end${this.currentJsqjValue}`],
                  type: obj.type,
                  prefix: this.currentJsqj || ''
                }
                this.dynamicTags.push(temp)
              } else {
                this.dynamicTags[_index].start = obj[`start${this.currentJsqjValue}`]
                this.dynamicTags[_index].end = obj[`end${this.currentJsqjValue}`]
                this.dynamicTags[_index].prefix = this.currentJsqj
              }
            }
          })
        }
      }
    },
    /**
     * @description 校验input
     */
    validateInput(obj) {
      // 数据区间不完整直接结束操作
      if (!obj.start || !obj.end) {
        this.$message({
          message: '请输入后再添加筛选条件',
          type: 'warning'
        })
        return false
      }
      // 校验是否为数字
      if (obj.start) {
        const reg = /^\.|\.$/
        if (isNaN(obj.start) || reg.test(obj.start)) {
          this.$message({
            message: '请输入数字',
            type: 'warning'
          })
          return false
        }
      }
      // 校验是否为数字
      if (obj.end) {
        const reg = /^\.|\.$/
        if (isNaN(obj.end) || reg.test(obj.end)) {
          this.$message({
            message: '请输入数字',
            type: 'warning'
          })
          return false
        }
      }
      // 结束区间不能小于开始区间
      if (obj.start && obj.end) {
        if (Number(obj.start) >= Number(obj.end)) {
          this.$message({
            message: '结束区间不能小于或等于开始区间',
            type: 'warning'
          })
          return false
        }
      }
      return true
    },

    /**
     * @description 校验计算区间的input
     */
    validateInputJSQJ(obj) {
      let objStart = `start${this.currentJsqjValue}`
      let objEnd = `end${this.currentJsqjValue}`
      // 数据区间不完整直接结束操作
      if (!obj[objStart] || !obj[objEnd]) {
        this.$message({
          message: '请输入后再添加筛选条件',
          type: 'warning'
        })
        return false
      }
      // 校验是否为数字
      if (obj[objStart]) {
        const reg = /^\.|\.$/
        if (isNaN(obj[objStart]) || reg.test(obj[objStart])) {
          this.$message({
            message: '请输入数字',
            type: 'warning'
          })
          return false
        }
      }
      // 校验是否为数字
      if (obj[objEnd]) {
        const reg = /^\.|\.$/
        if (isNaN(obj[objEnd]) || reg.test(obj[objEnd])) {
          this.$message({
            message: '请输入数字',
            type: 'warning'
          })
          return false
        }
      }
      // 结束区间不能小于开始区间
      if (obj[objStart] && obj[objEnd]) {
        if (Number(obj[objStart]) >= Number(obj[objEnd])) {
          this.$message({
            message: '结束区间不能小于或等于开始区间',
            type: 'warning'
          })
          return false
        }
      }
      return true
    },

    /**
     * @description 删除已选条件
     */
    handleClose(tag) {
      let idStr = tag.id.replace(/\d/g, '')
      let idNum = tag.id.replace(/[^0-9]/g, '')
      // 删除投资策略
      if (tag.id === '1') {
        this.investStrategy.forEach(item => {
          item.checked = false
        })
        const DomBx = document.querySelector('.tzclbx')
        DomBx.style.backgroundColor = '#dcedff'
        DomBx.style.color = '#4f95dd'
        DomBx.style.borderColor = '#dcdfe6'
      }
      // 删除运行状态
      if (tag.id === '2') {
        this.yxztData[0].checked = 2
      }
      // 删除是否分级
      if (tag.id === '3') {
        this.sffjData[0].checked = 2
      }
      // 删除净值频率
      if (tag.id === '4') {
        this.jzplOptions[0].selected = 3
      }
      // 删除绩效评级
      if (tag.id === '5') {
        this.jxpjOptions[0].selected = ''
      }
      // 删除成立时间
      if (tag.id === '6') {
        this.clsjSection.startDate = ''
        this.clsjSection.endDate = ''
        this.clsjSelect = '1'
      }
      // 删除资产净值
      if (tag.id === '7') {
        this.zcjz[0].start = ''
        this.zcjz[0].end = ''
      }
      // 删除累计净值
      if (tag.id === '20') {
        this.ljjz[0].start = ''
        this.ljjz[0].end = ''
      }
      // 删除资产净值
      if (tag.id === '21') {
        this.zcjzs[0].start = ''
        this.zcjzs[0].end = ''
      }
      // 删除成立以来大类资产占比(平均值)
      if (['15', '16', '17', '18'].includes(tag.id)) {
        this.clearSinceTheInput(tag.id, tag.name)
      }

      // 删除计算区间
      if (['10', '11', '12', '13', '14'].includes(idNum)) {
        this.clearJSQJInput(idNum, idStr)
      }

      const index = this.dynamicTags.findIndex(item => item.id === tag.id)
      this.dynamicTags.splice(index, 1)
    },
    /**
     * @description 清除成立以来大类资产占比input
     */
    clearSinceTheInput(id, name) {
      const obj = this.filterData(id, name)
      obj.start = ''
      obj.end = ''
    },
    clearJSQJInput(idNum, idStr) {
      let index = ['近六月', '近一年', '今年以来', '成立以来'].findIndex(item => item == idStr)
      for (let i = 0; i < this.sylzdhcData.length; i++) {
        let temp = this.sylzdhcData[i]
        if (temp.id === idNum) {
          temp[`start${index + 1}`] = ''
          temp[`end${index + 1}`] = ''
        }
      }
    },
    /**
     * @description 重置所有条件
     */
    reset() {
      // 重置清空投资策略
      this.investStrategy.forEach(item => {
        item.checked = false
      })
      // 重置清空运行状态
      this.yxztData[0].checked = 2
      // 重置清空是否分级
      this.sffjData[0].checked = 2
      // 重置清空净值频率
      this.jzplOptions[0].selected = 3
      // 重置清空绩效评级
      this.jxpjOptions[0].selected = ''
      // 重置清空成立时间
      this.clsjSection.startDate = ''
      this.clsjSection.endDate = ''
      this.clsjSelect = '1'
      // 重置清空资产净值
      this.zcjz[0].start = ''
      this.zcjz[0].end = ''
      // 重置清空累计净值
      this.ljjz[0].start = ''
      this.ljjz[0].end = ''
      // 重置资产净值
      this.zcjzs[0].start = ''
      this.zcjzs[0].end = ''
      // 重置清空成立以来大类资产占比(平均值)
      this.sinceThe.forEach(item => {
        item.start = ''
        item.end = ''
      })

      // 清空计算区间
      for (let i = 0; i < this.sylzdhcData.length; i++) {
        let temp = this.sylzdhcData[i]
        for (let j = 1; j <= 4; j++) {
          temp[`start${j}`] = ''
          temp[`end${j}`] = ''
        }
      }

      const DomBx = document.querySelector('.tzclbx')
      DomBx.style.backgroundColor = '#dcedff'
      DomBx.style.color = '#4f95dd'
      DomBx.style.borderColor = '#dcdfe6'
      this.dynamicTags = []
    },

    filterAlphaItem() {
      let newArr = this.centerTreeDataRight[0].children
      newArr.forEach(element => {
        let haveAlpha = false
        element.children.forEach(item => {
          if (item.label.includes('Alpha')) {
            haveAlpha = true
          }
        })
        if (!haveAlpha) {
          this.filterAlphaArr.push(element.label)
        }
      })
    }
  },
  beforeDestroy() {
    this.yxztData[0].checked = 1
  }
}
</script>
<style lang="scss">
</style>
<style lang="scss" scoped>
#moreQuery {
  background-color: #fff;
  border: 1px solid #e1e0e0;
  border-top: none;
  padding: 0 10px;
  ::v-deep .el-form--inline .el-form-item__label {
    margin-bottom: 0px;
  }

  .tzcl,
  .yxtj {
    ::v-deep .el-form-item__content {
      flex: 1;
    }
  }

  .tzclbx {
    border: 1px solid #dcedff;
    height: 26px;
    line-height: 26px;
    padding: 0px 10px;
    margin-right: 10px;
    background-color: #dcedff;
    color: #4f95dd;
    //color: #333;
    font-size: 14px;
    cursor: pointer;
    border-radius: 4px;
  }

  .tzclbx:hover {
    border: 1px solid #4f95dd;
    color: #4f95dd;
    border-radius: 4px;
  }

  .el-row {
    border-bottom: 1px solid #ebeef5;
    padding: 15px 0;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
  }

  .hoverBox {
    position: relative;
    margin: 3px 5px;
    display: inline-block;
  }

  .input-border {
    border: 2px solid #6ab1ff;
    border-bottom: none;
    margin-top: -2px;

    ::v-deep .el-input__inner {
      padding-left: 13px;
    }
  }

  .hover-item {
    position: absolute;
    display: flex;
    align-items: center;
    margin: 6px 0 0 -11px;
    width: 375px;
    height: 40px;
    z-index: 9999;
    border: 2px solid #6ab1ff;
    background-color: #fff;
    padding-left: 5px;
    display: flex;

    span {
      padding: 0 5px;
    }
  }

  .itemBox {
    border: 1px solid #e1e0e0;
    border-radius: 1px;
    height: 26px;
    padding: 2px 8px;
    margin-right: 10px;
    border-radius: 4px;
    span:hover {
      color: #4f95dd;
    }
  }

  .itemBox:hover {
    border: 1px solid #4f95dd;
    border-radius: 1px;
  }

  .itemBox-checked {
    border: 1px solid #e1e0e0;
    border-radius: 1px;
    height: 26px;
    border-color: #e6edfc;
    background: #e6edfc;
    padding: 2px 8px;
    margin-right: 10px;
  }

  // elementUI样式穿透
  .jzpl {
    ::v-deep .el-radio.is-checked {
        border: 1px solid #e1e0e0;
        border-radius: 1px;
        border-color: #e6edfc;
        background: #e6edfc;
        color: #0f65dd;
    }

    ::v-deep .el-radio:hover {
      border: 1px solid #4f95dd;
      border-radius: 1px;
      color: #4f95dd;
    }

    ::v-deep .el-radio--small.is-bordered {
      padding: 5px 11px 0 0px;
      border-radius: 4px;
      height: 26px;
    }
  }

  ::v-deep .el-tag {
    margin: 0;
  }

  .tzcl,
  .clsj,
  .jzpl,
  .jsqj {
    ::v-deep .el-radio {
      margin-right: 0;
      font-size: 14px;
    }
    ::v-deep .el-radio__input {
      display: none;
    }
    ::v-deep .el-checkbox:hover {
      color: #4f95dd;
    }

    ::v-deep .el-checkbox__label {
      font-size: 14px;
    }

    ::v-deep .el-form-item--small .el-form-item__content {
      line-height: 34px;
    }

    ::v-deep .el-form-item {
      margin-bottom: 0 !important;
    }

    ::v-deep .el-select .el-input--small {
      width: 120px !important;
    }

    ::v-deep .el-select .el-input__inner {
      height: 26px;
      line-height: 26px;
    }

    ::v-deep .el-input--small .el-input__icon {
      line-height: 26px;
    }

    ::v-deep .el-input--small .el-input__inner {
      height: 26px;
      line-height: 26px;
    }

    ::v-deep .el-date-editor--daterange.el-input__inner {
      width: 265px;
    }

    ::v-deep .el-range-editor--small.el-input__inner {
      height: 26px;
    }

    ::v-deep .el-range-editor--small .el-range__icon {
      line-height: 20px;
    }

    ::v-deep .el-range-editor--small .el-range-separator {
      line-height: 20px;
    }
  }

  .submit-icon-disabled {
    .el-button--small.is-circle {
      padding: 0 !important;
      margin-left: 5px;
      background-color: #a1a2a8;
    }
  }

  .tag-list {
    width: calc(100vw - 2% - 120px);
    overflow: auto;
  }

  .submit-icon {
    .el-button--small.is-circle {
      padding: 0 !important;
      margin-left: 5px;
      background-color: #4f95dd;
    }
  }
}
</style>

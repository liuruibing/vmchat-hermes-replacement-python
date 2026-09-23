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
      <!-- 公司类型 -->
      <el-row class="gslx">
        <el-form-item label="公司类型" label-width="70px" style="display: flex;align-items:center">
          <span class="gslxbx" style="font-size: 14px;padding: 4px 10px" @click="handleBxBtn('.gslxbx')">
            不限
          </span>
          <span v-for="ele in companyType" :key="ele.id" :class="ele.checked ? 'itemBox-checked' : 'itemBox'">
            <el-checkbox
              v-model="ele.checked"
              :label="ele.label"
              @change="companyTypeChange($event, '.gslxbx', ele)"
            />
          </span>
        </el-form-item>
      </el-row>
      <!--  公司状态 / 备案状态 -->
      <el-row class="gsbazt">
        <el-form-item label="公司状态" label-width="70px" style="display:flex; align-items:center">
          <span class="gsztbx" style="font-size: 14px;padding: 4px 10px" @click="handleBxBtn('.gsztbx')">
            不限
          </span>
          <span
            v-for="ele in companyState"
            :key="ele.id"
            :class="ele.checked ? 'itemBox-checked' : 'itemBox'"
          >
            <el-checkbox
              v-model="ele.checked"
              :label="ele.label"
              @change="companyStateChange($event, '.gsztbx', ele)"
            />
          </span>
        </el-form-item>
        <el-form-item label="备案状态" label-width="70px" style="display:flex; align-items:center">
          <span class="baztbx" style="font-size: 14px;padding: 4px 10px" @click="handleBxBtn('.baztbx')">
            不限
          </span>
          <span
            v-for="ele in recordsState"
            :key="ele.id"
            :class="ele.checked ? 'itemBox-checked' : 'itemBox'"
          >
            <el-checkbox
              v-model="ele.checked"
              :label="ele.label"
              @change="companyRecordsState($event, '.baztbx', ele)"
            />
          </span>
        </el-form-item>
      </el-row>
      <!-- 策略类型 -->
      <el-row class="cllx">
        <el-form-item label="计算维度" label-width="70px" style="display:flex; align-items:center">
          <div style="display: flex; align-items:center">
            <div style="margin-right: 20px">
              <el-radio
                v-for="e in strategyType"
                :key="e.id"
                v-model="currentInvest"
                :label="e.id"
                border
                size="small"
                @input="strategyTypeChange"
              >
                {{ e.label }}
              </el-radio>
              <el-tooltip class="table_header_icon ml10" effect="dark" placement="top">
                <span slot="content">计算维度代表：管理人收益率等指标是用哪些产品拟合出后的数据计算的。拟合数据取自私募排排。</span>
                <i class="el-icon-question" style="cursor: pointer;"></i>
              </el-tooltip>
            </div>
          </div>
        </el-form-item>
      </el-row>
      <!-- 成立时间 / 产品总数 -->
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
          :class="clsjSection.style ? 'submit-icon' : 'submit-icon-disabled'"
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
          v-for="e in cpzs"
          :key="e.mid"
          :label="e.title"
          :label-width="e.width"
          style="display:flex; align-items:center"
        >
          <el-input
            v-model="e.start"
            onkeyup="value=value.replace(/[^0-9]/g,'').replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3')"
            size="small"
            style="width: 72px!important"
          />
          <span>-</span>
          <el-input
            v-model="e.end"
            onkeyup="value=value.replace(/[^0-9]/g,'').replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3')"
            size="small"
            style="width: 72px!important"
          />
          <span :class="e.style ? 'submit-icon' : 'submit-icon-disabled'">
            <el-button circle icon="el-icon-check" type="primary" @click="addTagInput(e, '7')"></el-button>
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
          style="display:flex; align-items:center;margin-right:30px"
        >
          <el-input
            v-model="e[`start${currentJsqjValue}`]"
            onkeyup="value=value.replace(/[^0-9.-]/g,'').replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3')"
            size="small"
            style="width: 72px!important"
          />
          <span v-if="!['Sharpe比率', 'Treynor比率'].includes(e.title)">%</span>
          <span>-</span>
          <el-input
            v-model="e[`end${currentJsqjValue}`]"
            onkeyup="value=value.replace(/[^0-9.-]/g,'').replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3')"
            size="small"
            style="width: 72px!important"
          />
          <span v-if="!['Sharpe比率', 'Treynor比率'].includes(e.title)">%</span>
          <span
            :class="e[`style${currentJsqjValue}`] ? 'submit-icon' : 'submit-icon-disabled'"
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
              <span v-if="['6', '7', '15', '16', '17', '18'].includes(tag.id)">
                {{formattedTag(tag.title,tag.start,tag.end)}}
              </span>
              <span v-else-if="['1', '2', '3', '4', '5'].includes(tag.id)">
                {{ tag.title + '：' + tag.value | ensWithStr }}
              </span>
              <span v-else>
                {{formattedTag(tag.prefix + tag.title,tag.start,tag.end)}}
<!--                {{ tag.prefix + tag.title + '：' + tag.start + '-' + tag.end }}-->
              </span>
            </el-tag>
          </div>
        </el-form-item>
      </el-row>
    </el-form>
  </div>
</template>

<script>
import constant from '../scripts/constant.js'
import request from '@/utils/request'

export default {
  name: 'ManagerQuery',
  filters: {
    ensWithStr(val) {
      if (val.endsWith('，') || val.endsWith(',')) {
        val = val.slice(0, -1)
      }
      return val
    }
  },
  props: {
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
      // 公司类型
      companyType: [],
      // 公司状态
      companyState: constant.companyState,
      // 备案状态
      recordsState: constant.recordsState,
      // 策略类型
      strategyType: [],
      // 产品总数
      cpzs: constant.cpzs,
      // 成立时间
      clsjOptions: constant.clsjOptions,
      // 成立时间绑定值
      clsjSelect: '1',
      // 时间区间绑定值
      clsjSection: {
        startDate: '',
        endDate: '',
        style:false
      },
      // 控制时间选择禁用
      disabledStart: true,
      disabledEnd: true,
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
      // 已选条件
      dynamicTags: [],
      currentInvest: ''
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
    this.getCompanyTypeList(this.sqlObj)
    this.getInvestStrategyList(this.sqlObj)
    this.companyStateChange(true, '.gsztbx', { id: 1, label: '运行', checked: true })
  },
  methods: {
    /**
     * @description 获取公司类型数据
     */
    getCompanyTypeList(param) {
      const data = {
        indexCode: param.company
      }
      request({
        url: `/api/report/v1.0/data/sql/${param.company}`,
        method: 'post',
        data: data
      }).then(res => {
        if (res.data.status === 0) {
          const resultDim = res.data.data || []
          this.companyType = resultDim.map(item => {
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
     * @description 获取策略类型数据
     */
    getInvestStrategyList(param) {
      const data = {
        indexCode: param.invest
      }
      request({
        url: `/api/report/v1.0/data/sql/${param.invest}`,
        method: 'post',
        data: data
      }).then(res => {
        if (res.data.status === 0) {
          const resultDim = res.data.data || []
          this.strategyType = resultDim.map(item => {
            return {
              label: item.DIM_NME,
              id: item.DIM_CDE
            }
          })
          this.strategyType.unshift({
            label: '旗下产品',
            id: ''
          })
        }
      })
    },
    /**
     * @description 不限取消所有checkbox选中
     */
    handleBxBtn(val) {
      // 获取对应dom节点修改样式
      const Dom = document.querySelector(val)
      Dom.style.backgroundColor = '#dcedff'
      Dom.style.color = '#4f95dd'
      // Dom.style.borderColor = '#dcedff'
      if (val === '.gslxbx') {
        // 点击不限时所有checkbox状态改为false => 公司类型
        this.companyType.forEach(item => {
          if (item.checked) {
            item.checked = false
          }
        })
        const investIndex = this.dynamicTags.findIndex(item => item.id === '1')
        this.dynamicTags.splice(investIndex, 1)
      } else if (val === '.gsztbx') {
        // 点击不限时所有checkbox状态改为false => 公司状态
        this.companyState.forEach(item => {
          if (item.checked) {
            item.checked = false
          }
        })
        const investIndex = this.dynamicTags.findIndex(item => item.id === '2')
        this.dynamicTags.splice(investIndex, 1)
      } else if (val === '.baztbx') {
        // 点击不限时所有checkbox状态改为false => 备案状态
        this.recordsState.forEach(item => {
          if (item.checked) {
            item.checked = false
          }
        })
        const investIndex = this.dynamicTags.findIndex(item => item.id === '3')
        this.dynamicTags.splice(investIndex, 1)
      }
    },
    /**
     * @description 公司类型监听联动
     */
    companyTypeChange(e, val, ele) {
      const checkedArr = this.companyType.filter(item => item.checked)
      const _index = this.dynamicTags.findIndex(item => item.id === '1')
      if (_index < 0 && checkedArr.length) {
        this.dynamicTags.push({
          id: '1',
          title: '公司类型',
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
      Dom.style.color = '#333'
    },
    /**
     * @description 公司状态监听联动
     */
    companyStateChange(e, val, ele) {
      const checkedArr = this.companyState.filter(item => item.checked)
      const _index = this.dynamicTags.findIndex(item => item.id === '2')
      if (_index < 0 && checkedArr.length) {
        this.dynamicTags.push({
          id: '2',
          title: '公司状态',
          value: checkedArr.map(item => item.label).join('，') + '，',
          code: checkedArr.map(item => item.id).join('，') + '，'
        })
      } else {
        if (e === true) {
          this.dynamicTags[_index].value = this.dynamicTags[_index].value + '' + ele.label + '，'
          this.dynamicTags[_index].code = this.dynamicTags[_index].code + '' + ele.id + '，'
        } else {
          if (!checkedArr.length) {
            const stateIndex = this.dynamicTags.findIndex(item => item.id === '2')
            this.dynamicTags.splice(stateIndex, 1)
            const DomBx = document.querySelector(val)
            DomBx.style.backgroundColor = '#dcedff'
            DomBx.style.color = '#4f95dd'
            DomBx.style.borderColor = '#eee'
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
      Dom.style.color = '#333'
    },
    /**
     * @description 备案状态监听联动
     */
    companyRecordsState(e, val, ele) {
      const checkedArr = this.recordsState.filter(item => item.checked)
      const _index = this.dynamicTags.findIndex(item => item.id === '3')
      if (_index < 0 && checkedArr.length) {
        this.dynamicTags.push({
          id: '3',
          title: '公司状态',
          value: checkedArr.map(item => item.label).join('，') + '，',
          code: checkedArr.map(item => item.id).join('，') + '，'
        })
      } else {
        if (e === true) {
          this.dynamicTags[_index].value = this.dynamicTags[_index].value + '' + ele.label + '，'
          this.dynamicTags[_index].code = this.dynamicTags[_index].code + '' + ele.id + '，'
        } else {
          if (!checkedArr.length) {
            const stateIndex = this.dynamicTags.findIndex(item => item.id === '3')
            this.dynamicTags.splice(stateIndex, 1)
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
      Dom.style.color = '#333'
      Dom.style.borderColor = '#dcdfe6'
    },
    /**
     * @description 策略类型监听radio
     */
    strategyTypeChange(val) {
      const _index = this.dynamicTags.findIndex(item => item.id === '4')
      const yxztObj = this.strategyType.find(item => item.id === val)

      if (val === '') {
        const yxztIndex = this.dynamicTags.findIndex(item => item.id === '4')
        this.dynamicTags.splice(yxztIndex, 1)
        return
      }
      if (_index < 0) {
        this.dynamicTags.push({
          id: '4',
          title: '策略类型',
          value: yxztObj.label,
          code: val
        })
      } else {
        this.dynamicTags[_index].value = yxztObj.label
        this.dynamicTags[_index].code = val
      }
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
         /* // 当重复添加相同数据时提示
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
          }*/
          if (_index < 0) {
            this.clsjSection.style = true
            this.dynamicTags.push({
              id: '6',
              title: '成立时间',
              start: this.clsjSection.startDate || '',
              end: this.clsjSection.endDate || ''
            })
          } else {
            this.clsjSection.style = false
            const clsjIndex = this.dynamicTags.findIndex(item => item.id === '6')
            this.dynamicTags.splice(clsjIndex, 1)
          }
        } else {
          return false
        }
      })
    },
    /**
     * @description 获取计算区间
     */
    jsqjChangeSelect(val) {
      const jsqjObj = this.jsqjOptions[0].options.find(item => item.value === val)
      this.currentJsqj = jsqjObj.label
      this.currentJsqjValue = val
    },
    /**
     * @description input相关submit => 计算区间见下addJsqjInput
     */
    addTagInput(obj, id) {
      // 校验输入框
      const isVaildate = this.validateInput(obj)
      if (isVaildate) {
       /* // 当重复添加相同数据时提示
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
        }*/
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
          if(id === '7'){
            this.cpzs[0].style = true
          }
        } else {
          const index_ = this.dynamicTags.findIndex(item => item.id === id)
          if (index_ !== -1) {
            this.dynamicTags.splice(index_, 1);
          }
          if(id === '7'){
            this.cpzs[0].style = false
          }
        }
      }
    },
    formattedTag(title,start,end) {
      if (!start && end) {
        return `${title}小于等于：${end}`;
      } else if (start && !end) {
        return `${title}大于等于：${start}`;
      } else if (start && end) {
        return `${title}：${start}-${end}`;
      } else {
        // 处理 start 和 end 都为空的情况，或者你可以根据需求返回其他字符串
        return `${title}（无时间范围）`;
      }
    },
    /**
     * @description 计算区间相关submit
     */
    addJsqjInput(obj, id) {
      // 校验输入框
      const isVaildate = this.validateInputJSQJ(obj)
      if (isVaildate) {
       /* // 当重复添加相同数据时提示
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
        }*/
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
          this.sylzdhcData[id-10][`style${this.currentJsqjValue}`] = !this.sylzdhcData[id-10][`style${this.currentJsqjValue}`]
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
                this.sylzdhcData[id-10][`style${this.currentJsqjValue}`] = !this.sylzdhcData[id-10][`style${this.currentJsqjValue}`]
                this.dynamicTags.push(temp)
              } else {
                const index_ = this.dynamicTags.findIndex(item => item.id === this.currentJsqj + id)
                if (index_ !== -1) {
                  this.dynamicTags.splice(index_, 1);
                }
                this.sylzdhcData[id-10][`style${this.currentJsqjValue}`] = !this.sylzdhcData[id-10][`style${this.currentJsqjValue}`]
                //this.dynamicTags[_index].start = obj[`start${this.currentJsqjValue}`]
                //this.dynamicTags[_index].end = obj[`end${this.currentJsqjValue}`]
                //this.dynamicTags[_index].prefix = this.currentJsqj
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
      if (!obj.start && !obj.end) {
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
      if (!obj[objStart] && !obj[objEnd]) {
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
      const idStr = tag.id.replace(/\d/g, '')
      const idNum = tag.id.replace(/[^0-9]/g, '')
      // 删除公司类型
      if (tag.id === '1') {
        this.companyType.forEach(item => {
          item.checked = false
        })
        const DomBx = document.querySelector('.gslxbx')
        DomBx.style.backgroundColor = '#dcedff'
        DomBx.style.color = '#4f95dd'
        DomBx.style.borderColor = '#dcdfe6'
      }
      // 删除公司状态
      if (tag.id === '2') {
        this.companyState.forEach(item => {
          item.checked = false
        })
        const DomBx = document.querySelector('.gsztbx')
        DomBx.style.backgroundColor = '#dcedff'
        DomBx.style.color = '#4f95dd'
        DomBx.style.borderColor = '#dcdfe6'
      }
      // 删除备案状态
      if (tag.id === '3') {
        this.recordsState.forEach(item => {
          item.checked = false
        })
        const DomBx = document.querySelector('.baztbx')
        DomBx.style.backgroundColor = '#dcedff'
        DomBx.style.color = '#4f95dd'
        DomBx.style.borderColor = '#dcdfe6'
      }
      // 删除策略类型
      if (tag.id === '4') {
        this.currentInvest = ''
      }
      // 删除成立时间
      if (tag.id === '6') {
        this.clsjSection.startDate = ''
        this.clsjSection.endDate = ''
        this.clsjSelect = '1'
        this.clsjSection.style = false
      }
      // 删除产品总数
      if (tag.id === '7') {
        this.cpzs[0].start = ''
        this.cpzs[0].end = ''
        this.cpzs[0].style = false
      }
      // 删除计算区间
      if (['10', '11', '12', '13', '14'].includes(idNum)) {
        this.clearJSQJInput(idNum, idStr)
      }
      const index = this.dynamicTags.findIndex(item => item.id === tag.id)
      this.dynamicTags.splice(index, 1)
    },
    /**
     * @description 删除计算区间input
     */
    clearJSQJInput(idNum, idStr) {
      const index = ['近六月', '近一年', '今年以来', '成立以来'].findIndex(item => item == idStr)
      for (let i = 0; i < this.sylzdhcData.length; i++) {
        const temp = this.sylzdhcData[i]
        if (temp.id === idNum) {
          temp[`start${index + 1}`] = ''
          temp[`end${index + 1}`] = ''
          temp[`style${index + 1}`] = false
        }
      }
    },
    /**
     * @description 重置所有条件
     */
    reset() {
      // 重置清空公司类型
      this.companyType.forEach(item => {
        item.checked = false
      })
      // 重置清空公司状态
      this.companyState.forEach(item => {
        item.checked = false
      })
      // 重置清空备案状态
      this.recordsState.forEach(item => {
        item.checked = false
      })
      // 重置清空策略类型
      this.strategyType[0].checked = 0
      // 重置清空成立时间
      this.clsjSection.startDate = ''
      this.clsjSection.endDate = ''
      this.clsjSelect = '1'
      this.clsjSection.style = false
      // 重置清空产品总数
      this.cpzs[0].start = ''
      this.cpzs[0].end = ''
      this.cpzs[0].style = false
      // 清空计算区间
      for (let i = 0; i < this.sylzdhcData.length; i++) {
        const temp = this.sylzdhcData[i]
        for (let j = 1; j <= 4; j++) {
          temp[`start${j}`] = ''
          temp[`end${j}`] = ''
          temp[`style${j}`] = false
        }
      }
      // dom样式初始化
      this.$nextTick(() => {
        const gslxBx = document.querySelector('.gslxbx')
        const gsztBx = document.querySelector('.gsztbx')
        const baztBx = document.querySelector('.baztbx')
        gslxBx.style.backgroundColor = '#dcedff'
        gslxBx.style.color = '#4f95dd'
        gslxBx.style.borderColor = '#dcdfe6'
        gsztBx.style.backgroundColor = '#dcedff'
        gsztBx.style.color = '#4f95dd'
        gsztBx.style.borderColor = '#dcdfe6'
        baztBx.style.backgroundColor = '#dcedff'
        baztBx.style.color = '#4f95dd'
        baztBx.style.borderColor = '#dcdfe6'
      })
      this.dynamicTags = []
    }
  },
  beforeDestroy() {
    this.companyState.forEach(item => {
      if (item.id !== 1) {
        item.checked = false
      } else {
        item.checked = true
      }
    })
  }
}
</script>

<style lang="scss" scoped>
#moreQuery {
  border: 1px solid #e1e0e0;
  border-top: none;
  padding: 0 10px;

  ::v-deep .el-form--inline .el-form-item__label {
    margin-bottom: 0px;
  }
  .gsztbx {
    border: 1px solid #eee;
    border-radius: 4px;
    height: 26px;
    line-height: 26px;
    padding: 0px 10px;
    margin-right: 10px;
    cursor: pointer;
  }
  .gslxbx,
  .baztbx {
    border: 1px solid #e6edfc;
    border-radius: 4px;
    height: 26px;
    line-height: 26px;
    padding: 0px 10px;
    margin-right: 10px;
    background-color: #e6edfc;
    color: #0f65dd;
    cursor: pointer;
  }

  .gslxbx:hover,
  .gsztbx:hover,
  .baztbx:hover {
    border: 1px solid #4f95dd;
    border-radius: 4px;
    color: #4f95dd;
  }

  .el-row {
    border-bottom: 1px solid #ebeef5;
    padding: 15px 0;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
  }

  .itemBox {
    // display: inline-block;
    border: 1px solid #e1e0e0;
    // height: 26px;
    // line-height: 20px;
    padding: 2px 8px;
    border-radius: 4px;
    margin-right: 10px;

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
  .cllx {
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
  .gslx,
  .yxtj {
    ::v-deep .el-form-item__content {
      flex: 1;
    }
  }

  .gslx,
  .gsbazt,
  .clsj,
  .cllx,
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

<template>
  <div id="moreQuery">
    <el-form ref="queryForm" :inline="true" class="standard-form" :model="clsjSection" :rules="searchRules" label-position="left" size="small">
      <!-- 投资策略 -->
      <el-row class="tzcl">
        <el-form-item label="投资策略" label-width="70px" style="display: flex; align-items: center">
          <span class="tzclbx-focus" style="font-size: 14px; padding: 4px 10px" @click="handleBxBtn('.tzclbx-focus')">不限</span>
          <span v-for="ele in investStrategy" :key="ele.id" :class="ele.checked ? 'itemBox-checked' : 'itemBox'">
            <el-checkbox v-model="ele.checked" :label="ele.label" @change="handleCheckedChange($event, '.tzclbx-focus', ele)" />
          </span>
        </el-form-item>
      </el-row>
      <el-row class="tzsubcl" v-show="isSubStrategyVisible">
        <el-form-item label="子策略" label-width="70px" style="display: flex; align-items: center">
          <span class="tzsubclbx-focus" style="font-size: 14px; padding: 4px 10px" @click="handleSubBxBtn('.tzsubclbx-focus')">不限</span>
          <span v-for="ele in investSubStrategy" :key="ele.id" :class="ele.checked ? 'itemBox-checked' : 'itemBox'">
            <el-checkbox v-model="ele.checked" :label="ele.label" @change="handleSubCheckedChange($event, '.tzsubclbx-focus', ele)" />
          </span>
        </el-form-item>
      </el-row>

      <!-- 三级策略 -->
      <el-row class="tzthirdcl" v-show="isThirdStrategyVisible">
        <el-form-item label="三级策略" label-width="70px" style="display:flex; align-items:center">
          <span class="tzthirdclbx-focus" style="font-size: 14px;padding: 4px 10px" @click="handleThirdBxBtn('.tzthirdclbx-focus')">
            不限
          </span>
          <span v-for="ele in investThirdStrategy" :key="ele.id" :class="ele.checked ? 'itemBox-checked' : 'itemBox'">
            <el-checkbox v-model="ele.checked" :label="ele.label" @change="handleThirdCheckedChange($event, '.tzthirdclbx-focus', ele)" />
          </span>
        </el-form-item>
      </el-row>
      <!--  运行状态 / 是否分级 / 净值频率 / 绩效评级 -->
      <el-row class="jzpl">
        <el-form-item v-for="e in yxztData" :key="e.mid" :label="e.title" :label-width="e.width" style="display: flex; align-items: center">
          <div style="display: flex; align-items: center">
            <div style="margin-right: 20px">
              <el-radio v-for="k in e.options" :key="k.id" v-model="e.checked" :label="k.id" border size="small" @input="yxztChangeRadio">
                {{ k.label }}
              </el-radio>
            </div>
          </div>
        </el-form-item>
        <el-form-item v-for="e in sffjData" :key="e.mid" :label="e.title" :label-width="e.width" style="display: flex; align-items: center">
          <div style="display: flex; align-items: center">
            <div style="margin-right: 20px">
              <el-radio v-for="k in e.options" :key="k.id" v-model="e.checked" :label="k.id" border size="small" @input="sffjChangeRadio">
                {{ k.label }}
              </el-radio>
            </div>
          </div>
        </el-form-item>
        <el-form-item v-for="e in sfdxData" :key="e.mid" :label="e.title" :label-width="e.width" style="display:flex; align-items:center">
          <div style="display: flex; align-items:center">
            <div style="margin-right: 20px">
              <el-radio v-for="k in e.options" :key="k.id" v-model="e.checked" :label="k.id" border size="small" @input="sfdxChangeRadio">
                {{ k.label }}
              </el-radio>
            </div>
          </div>
        </el-form-item>
        <el-form-item v-for="e in jzplOptions" :key="e.mid" :label="e.title" :label-width="e.width" style="display: flex; align-items: center">
          <el-select v-model="e.selected" size="small" style="margin-right: 15px" @change="jzplChangeSelect">
            <el-option v-for="item in e.options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
      </el-row>
      <!-- 成立时间 / 资产净值 -->
      <el-row class="clsj">
        <el-form-item label="成立时间" label-width="70px" style="display: flex; align-items: center">
          <el-select v-model="clsjSelect" placeholder="请选择" size="small" style="margin-right: 15px" @change="handleDateChange">
            <el-option v-for="item in clsjOptions" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item prop="startDate">
          <el-date-picker v-model="clsjSection.startDate" :disabled="disabledStart" placeholder="选择开始日期" type="date" value-format="yyyy-MM-dd" />
        </el-form-item>
        <el-form-item prop="endDate">
          <el-date-picker v-model="clsjSection.endDate" :disabled="disabledEnd" placeholder="选择结束日期" type="date" value-format="yyyy-MM-dd" />
        </el-form-item>
        <el-form-item :class="clsjSection.style ? 'submit-icon' : 'submit-icon-disabled'">
          <el-button circle icon="el-icon-check" type="gfcheck" @click="clsjSubmit" style="margin-right: 20px"></el-button>
        </el-form-item>
        <el-form-item v-for="e in zcjz" :key="e.mid" :label="e.title" :label-width="e.width" style="display: flex; align-items: center">
          <el-input v-model="e.start" onkeyup="value=value.replace(/[^0-9.-]/g,'').replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3')" size="small" style="width: 72px !important" />
          <span>-</span>
          <el-input v-model="e.end" onkeyup="value=value.replace(/[^0-9.-]/g,'').replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3')" size="small" style="width: 72px !important" />
          <span :class="e.style ? 'submit-icon' : 'submit-icon-disabled'">
            <el-button circle icon="el-icon-check" type="gfcheck" @click="addTagInput(e, '7')"></el-button>
          </span>
        </el-form-item>
      </el-row>
      <!-- 计算区间 / 收益率 / 最大回撤 / sharpe比率 / Treynor比率 / jensen指数-->
      <el-row class="jsqj">
        <el-form-item v-for="e in jsqjOptions" :key="e.mid" :label="e.title" :label-width="e.width" style="display: flex; align-items: center">
          <el-select v-model="e.selected" size="small" style="margin-right: 15px" @change="jsqjChangeSelect">
            <el-option v-for="item in e.options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </el-form-item>
        <el-form-item v-for="e in sylzdhcData" :key="e.id" :label="e.title" :label-width="e.width" style="display: flex; align-items: center; margin-right: 30px">
          <el-input
            v-model="e[`start${currentJsqjValue}`]"
            onkeyup="value=value.replace(/[^0-9.-]/g,'').replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3')"
            size="small"
            style="width: 72px !important"
          />
          <span v-if="!['Sharpe比率', 'Treynor比率'].includes(e.title)">%</span>
          <span>-</span>
          <el-input
            v-model="e[`end${currentJsqjValue}`]"
            onkeyup="value=value.replace(/[^0-9.-]/g,'').replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3')"
            size="small"
            style="width: 72px !important"
          />
          <span v-if="!['Sharpe比率', 'Treynor比率'].includes(e.title)">%</span>
          <span :class="e[`style${currentJsqjValue}`] ? 'submit-icon' : 'submit-icon-disabled'">
            <el-button circle icon="el-icon-check" type="gfcheck" @click="addJsqjInput(e, e.id)"></el-button>
          </span>
        </el-form-item>
      </el-row>
      <!-- 成立以来大类资产占比(平均值)-->
<!--      <el-row class="sfradio">-->
<!--        <el-form-item label="成立以来大类资产占比(平均值)" style="display: flex; align-items: center">-->
<!--          <el-radio-->
<!--            v-for="item in sinceThe"-->
<!--            :key="item.id"-->
<!--            :label="item.index"-->
<!--            border-->
<!--            class="hoverBox"-->
<!--            size="small"-->
<!--            @mouseover.native="inputMouserIn(item.id, item.name)"-->
<!--            @mouseleave.native="inputMouseOut(item.id, item.name)"-->
<!--          >-->
<!--            <span>{{ item.title }}</span>-->
<!--            <div v-show="item.isShow" class="hover-item">-->
<!--              <el-input v-model="item.start" onkeyup="value=value.replace(/[^0-9.-]/g,'')" />-->
<!--              <span>-</span>-->
<!--              <el-input v-model="item.end" onkeyup="value=value.replace(/[^0-9.-]/g,'')" />-->
<!--              <span :class="item.start && item.end ? 'submit-icon' : 'submit-icon-disabled'">-->
<!--                <el-button circle icon="el-icon-check" type="primary" @click="addTagInput(item, item.id)"></el-button>-->
<!--              </span>-->
<!--            </div>-->
<!--          </el-radio>-->
<!--        </el-form-item>-->
<!--      </el-row>-->
      <!-- 已选条件 -->
      <el-row class="yxtj">
        <el-form-item label="已选条件" label-width="70px" style="display: flex; align-items: center; margin-bottom: 0px !important">
          <div class="tag-list">
            <el-tag v-for="(tag, i) in dynamicTags" :key="i" :disable-transitions="false" closable style="margin-left: 10px" @close="handleClose(tag)">
              <span v-if="['6', '7', '15', '16', '17', '18'].includes(tag.id)">
               {{formattedTag(tag.title,tag.start,tag.end)}}
                <!--                {{ tag.title + '：' + tag.start + '-' + tag.end }}-->
              </span>
              <span v-else-if="['1', '2', '3', '4', '5','100','200','102'].includes(tag.id)">
                {{ (tag.title + '：' + tag.value) | ensWithStr }}
              </span>
              <span v-else>
                {{formattedTag(tag.prefix + tag.title,tag.start,tag.end)}}
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
import request from '@/utils/request'

export default {
  name: 'EpibolyQuery',
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
      if (this.clsjSection.endDate !== null || this.clsjSection.endDate !== undefined || this.clsjSection.endDate !== '') {
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
      if (this.clsjSection.startDate !== null || this.clsjSection.startDate !== undefined || this.clsjSection.startDate !== '') {
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
      //子策略是否可见
      isSubStrategyVisible:false,
      //三级策略是否可见
      isThirdStrategyVisible:false,
      // 投资策略
      investStrategy: [],
      //子策略
      investSubStrategy:[],
      // 投资三级策略
      investThirdStrategy: [],
      // 投资子策略策略
      investSubOptions:[],
      // 三级策略
      investThirdOptions:[],
      // 成立时间
      clsjOptions: constant.clsjOptions,
      // 成立时间绑定值
      clsjSelect: '1',
      // 时间区间绑定值
      clsjSection: {
        startDate: '',
        endDate: '',
        style:false,
      },
      // 控制时间选择禁用
      disabledStart: true,
      disabledEnd: true,
      // 资产净值
      zcjz: constant.zcjz,
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
      // 是否代销
      sfdxData: constant.sfdxData,
      // 成立以来大类资产占比
      sinceThe: constant.sinceThe,
      // 绩效评级
      jxpjOptions: constant.jxpjOptions,
      // 已选条件
      dynamicTags: []
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
        status: '2'
      }
      this.$emit('updateSelect', obj)
    }
  },
  mounted() {
    this.getInvestStrategyList(this.sqlObj)
    this.getInvestSubStrategyList(this.sqlObj)
    this.getInvestThirdStrategyList(this.sqlObj)
    this.yxztChangeRadio(1)
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
      }).then((res) => {
        if (res.data.status === 0) {
          const resultDim = res.data.data || []
          this.investStrategy = resultDim.map((item) => {
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
     * @description 获取投资子策略数据
     */
    getInvestSubStrategyList(param) {
      request({
        url: `/api/report/v1.0/data/sql/${param.indexCode2}`,
        method: 'post',
        data: param
      }).then(res => {
        if (res.data.status === 0) {
          const resultDim = res.data.data || []
          this.investSubOptions =resultDim;
        }
      })
    },

    /**
     * @description 获取三级策略数据
     */
    getInvestThirdStrategyList(param) {
      request({
        url: `/api/report/v1.0/data/sql/${param.indexCode3}`,
        method: 'post',
        data: param
      }).then(res => {
        if (res.data.status === 0) {
          const resultDim = res.data.data || []
          this.investThirdOptions =resultDim;
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
          obj = this.sinceThe.find((item) => item.id === id)
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
      Dom.style.backgroundColor = '#e9c5a5'
      Dom.style.color = '#612d10'
      Dom.style.borderColor = '#e9c5a5'
      if (val === '.tzclbx-focus') {
        //隐藏子策略
        this.handleSubBxBtn('.tzsubclbx-focus')
        this.isSubStrategyVisible=false
        this.investSubStrategy=''
        // 点击不限时所有checkbox状态改为false => 投资策略
        this.investStrategy.forEach((item) => {
          if (item.checked) {
            item.checked = false
          }
        })
        const investIndex = this.dynamicTags.findIndex((item) => item.id === '1')
        if(investIndex!==-1) {
          this.dynamicTags.splice(investIndex, 1)
        }
      }
    },


    /**
     * @description 三级策略点击不限取消所有checkbox选中
     */
    handleThirdBxBtn(val) {
      // 获取对应dom节点修改样式
      const Dom = document.querySelector(val)
      Dom.style.backgroundColor = '#e9c5a5'
      Dom.style.color = '#612d10'
      Dom.style.borderColor = '#e9c5a5'
      if (val === '.tzthirdclbx-focus') {
        // 点击不限时所有checkbox状态改为false => 投资子策略
        this.investThirdStrategy.forEach(item => {
          if (item.checked) {
            item.checked = false
          }
        })
        const investIndex3 = this.dynamicTags.findIndex(item => item.id === '200')
        if(investIndex3!==-1) {
          this.dynamicTags.splice(investIndex3, 1)
        }
      }
      this.isThirdStrategyVisible = true
    },

    /**
     * @description 投资策略点击不限取消所有checkbox选中
     */
    handleSubBxBtn(val) {
      // 获取对应dom节点修改样式
      const Dom = document.querySelector(val)
      Dom.style.backgroundColor = '#e9c5a5'
      Dom.style.color = '#612d10'
      Dom.style.borderColor = '#e9c5a5'
      if (val === '.tzsubclbx-focus') {
        //隐藏三级策略
        this.handleThirdBxBtn('.tzthirdclbx-focus')
        this.isThirdStrategyVisible=false
        this.investThirdStrategy=''
        // 点击不限时所有checkbox状态改为false => 投资策略
        this.investSubStrategy.forEach((item) => {
          if (item.checked) {
            item.checked = false
          }
        })
        const investIndex = this.dynamicTags.findIndex((item) => item.id === '100')
        if(investIndex!==-1) {
          this.dynamicTags.splice(investIndex, 1)
        }
      }
    },
    /**
     * @description 投资策略监听联动
     */
    handleCheckedChange(e, val, ele) {
      const checkedArr = this.investStrategy.filter((item) => item.checked)
      if(checkedArr.length===0) {

        //删除三级策略的选项内容
        const investIndex3 = this.dynamicTags.findIndex(item => item.id === '200')
        if(investIndex3!==-1) {
          this.dynamicTags.splice(investIndex3, 1)
        }
        this.isThirdStrategyVisible = false
        //删除子策略的选项内容
        const investIndex2 = this.dynamicTags.findIndex(item => item.id === '100')
        if(investIndex2!==-1) {
          this.dynamicTags.splice(investIndex2, 1)
        }
        this.isSubStrategyVisible = false
      }else{

        const subResultDim = this.investSubOptions.filter((item) => checkedArr.map(item => item.id).join('，').includes(item.DIM_EDIT))
        const thirdResultDim = this.investThirdOptions.filter((item) => subResultDim.map(item => item.DIM_CDE).join('，').includes(item.DIM_EDIT))
        const _index = this.dynamicTags.findIndex(item => item.id === '100')
        const _index3 = this.dynamicTags.findIndex(item => item.id === '200')
        if(!ele.checked){
          //一级策略未选中的时候，二级子策略初始化为未选中状态
          const singleSubResultDim = this.investSubOptions.filter((item) => item.DIM_EDIT===ele.id)

          singleSubResultDim.map(item => {
            const regValue = new RegExp(`${item.DIM_NME}，`, 'g')
            const regCode = new RegExp(`${item.DIM_CDE}，`, 'g')
            if(_index!==-1) {
              this.dynamicTags[_index].value = this.dynamicTags[_index].value.replace(regValue, '')
              this.dynamicTags[_index].code = this.dynamicTags[_index].code.replace(regCode, '')
            }
          })
          const singleThirdResultDim = this.investThirdOptions.filter((item) => subResultDim.map(item => item.DIM_CDE===ele.id).join('，').includes(item.DIM_EDIT))

          singleThirdResultDim.map(item => {
            const regValue = new RegExp(`${item.DIM_NME}，`, 'g')
            const regCode = new RegExp(`${item.DIM_CDE}，`, 'g')
            if(_index3!==-1) {
              this.dynamicTags[_index3].value = this.dynamicTags[_index3].value.replace(regValue, '')
              this.dynamicTags[_index3].code = this.dynamicTags[_index3].code.replace(regCode, '')
            }
          })
        }

        if(_index!==-1){
          //存在已勾选的子策略
          const subcheckboxid=this.dynamicTags[_index].code
          this.investSubStrategy = subResultDim.map(item => {
            return {
              label: item.DIM_NME,
              id: item.DIM_CDE,
              checked: subcheckboxid.includes(item.DIM_CDE)?true:false
            }
          })
        }else {
          this.investSubStrategy = subResultDim.map(item => {
            return {
              label: item.DIM_NME,
              id: item.DIM_CDE,
              checked: false
            }
          })
        }

        if(_index3!==-1){
          //存在已勾选的三级策略
          const thirdcheckboxid=this.dynamicTags[_index3].code
          this.investThirdStrategy = thirdResultDim.map(item => {
            return {
              label: item.DIM_NME,
              id: item.DIM_CDE,
              checked: thirdcheckboxid.includes(item.DIM_CDE)?true:false
            }
          })
        }else {
          this.investThirdStrategy = thirdResultDim.map(item => {
            return {
              label: item.DIM_NME,
              id: item.DIM_CDE,
              checked: false
            }
          })
        }

        this.isSubStrategyVisible = true

        if(thirdResultDim.length===0){
          //删除三级策略的选项内容
          const investIndex3 = this.dynamicTags.findIndex(item => item.id === '200')
          if(investIndex3!==-1) {
            this.dynamicTags.splice(investIndex3, 1)
          }
          this.isThirdStrategyVisible = false

        }
      }

      const _index = this.dynamicTags.findIndex((item) => item.id === '1')
      if (_index < 0 && checkedArr.length) {
        this.dynamicTags.push({
          id: '1',
          title: '投资策略',
          value: checkedArr.map((item) => item.label).join('，') + '，',
          code: checkedArr.map((item) => item.id).join('，') + '，'
        })
      } else {
        if (e === true) {
          this.dynamicTags[_index].value = this.dynamicTags[_index].value + '' + ele.label + '，'
          this.dynamicTags[_index].code = this.dynamicTags[_index].code + '' + ele.id + '，'
        } else {
          if (!checkedArr.length) {
            const investIndex = this.dynamicTags.findIndex((item) => item.id === '1')
            this.dynamicTags.splice(investIndex, 1)
            const DomBx = document.querySelector(val)
            DomBx.style.backgroundColor = '#e9c5a5'
            DomBx.style.color = '#612d10'
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
      Dom.style.borderColor = '#e9c5a5'
    },

    /**
     * @description 子策略监听联动
     */
    handleSubCheckedChange(e, val, ele) {
      const checkedArr = this.investSubStrategy.filter(item => item.checked)
      const _index = this.dynamicTags.findIndex(item => item.id === '100')

      if(checkedArr.length===0) {
        //删除三级策略的选项内容
        this.isThirdStrategyVisible = false
        const investIndex3 = this.dynamicTags.findIndex(item => item.id === '200')
        if(investIndex3!==-1) {
          this.dynamicTags.splice(investIndex3, 1)
        }

      }else{
        const thirdResultDim = this.investThirdOptions.filter((item) => checkedArr.map(item => item.id).join('，').includes(item.DIM_EDIT))
        const _thirdindex = this.dynamicTags.findIndex(item => item.id === '200')

        if(!ele.checked){
          //二级策略未选中的时候，三级子策略初始化为未选中状态
          const singleThirdResultDim = this.investThirdOptions.filter((item) => item.DIM_EDIT===ele.id)
          if(singleThirdResultDim.length !==0) {
            singleThirdResultDim.map(item => {
              const regValue = new RegExp(`${item.DIM_NME}，`, 'g')
              const regCode = new RegExp(`${item.DIM_CDE}，`, 'g')
              if (_thirdindex !== -1) {
                this.dynamicTags[_thirdindex].value = this.dynamicTags[_thirdindex].value.replace(regValue, '')
                this.dynamicTags[_thirdindex].code = this.dynamicTags[_thirdindex].code.replace(regCode, '')
              }
            })
          }
        }

        if(_thirdindex!==-1){
          //存在已勾选的子策略
          const thirdcheckboxid=this.dynamicTags[_thirdindex].code
          this.investThirdStrategy = thirdResultDim.map(item => {
            return {
              label: item.DIM_NME,
              id: item.DIM_CDE,
              checked: thirdcheckboxid.includes(item.DIM_CDE)?true:false
            }
          })
        }else {
          this.investThirdStrategy = thirdResultDim.map(item => {
            return {
              label: item.DIM_NME,
              id: item.DIM_CDE,
              checked: false
            }
          })
        }

        if(thirdResultDim.length===0){
          //删除三级策略的选项内容
          if(_thirdindex!==-1) {
            this.dynamicTags.splice(_thirdindex, 1)
          }
          this.isThirdStrategyVisible = false

        }else{
          this.isThirdStrategyVisible = true
        }



      }
      if (_index < 0 && checkedArr.length) {
        this.dynamicTags.push({
          id: '100',
          title: '子策略',
          value: checkedArr.map(item => item.label).join('，') + '，',
          code: checkedArr.map(item => item.id).join('，') + '，'
        })
      } else {
        if (e === true) {
          this.dynamicTags[_index].value = this.dynamicTags[_index].value + '' + ele.label + '，'
          this.dynamicTags[_index].code = this.dynamicTags[_index].code + '' + ele.id + '，'
        } else {

          if (!checkedArr.length) {
            const investIndex = this.dynamicTags.findIndex(item => item.id === '100')
            this.dynamicTags.splice(investIndex, 1)
            const DomBx = document.querySelector(val)
            DomBx.style.backgroundColor = '#e9c5a5'
            DomBx.style.color = '#612d10'
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
      Dom.style.borderColor = '#e9c5a5'
    },

    /**
     * @description 三级策略监听联动
     */
    handleThirdCheckedChange(e, val, ele) {
      const checkedArr = this.investThirdStrategy.filter(item => item.checked)
      const _index3 = this.dynamicTags.findIndex(item => item.id === '200')

      this.isThirdStrategyVisible = true
      if (_index3 < 0 && checkedArr.length) {
        this.dynamicTags.push({
          id: '200',
          title: '三级策略',
          value: checkedArr.map(item => item.label).join('，') + '，',
          code: checkedArr.map(item => item.id).join('，') + '，'
        })
      } else {
        if (e === true) {
          this.dynamicTags[_index3].value = this.dynamicTags[_index3].value + '' + ele.label + '，'
          this.dynamicTags[_index3].code = this.dynamicTags[_index3].code + '' + ele.id + '，'
        } else {
          if (!checkedArr.length) {
            const investIndex = this.dynamicTags.findIndex(item => item.id === '200')
            this.dynamicTags.splice(investIndex, 1)
            const DomBx = document.querySelector(val)
            DomBx.style.backgroundColor = '#e9c5a5'
            DomBx.style.color = '#612d10'
            DomBx.style.borderColor = 'transparent'
            return
          }
          const regValue = new RegExp(`${ele.label}，`, 'g')
          const regCode = new RegExp(`${ele.id}，`, 'g')
          this.dynamicTags[_index3].value = this.dynamicTags[_index3].value.replace(regValue, '')
          this.dynamicTags[_index3].code = this.dynamicTags[_index3].code.replace(regCode, '')
        }
      }
      // 获取对应dom节点修改样式
      const Dom = document.querySelector(val)
      Dom.style.backgroundColor = '#fff'
      Dom.style.borderColor = '#e9c5a5'
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
            message: '请选择成立时间',
            customClass: 'message-warning'
          })
          return
        }
      }
      const _index = this.dynamicTags.findIndex((item) => item.id === '6')
      if (this.clsjSelect === '1') {
        const clsjIndex = this.dynamicTags.findIndex((item) => item.id === '6')
        this.dynamicTags.splice(clsjIndex, 1)
        return
      }
      this.$refs.queryForm.validate((valid) => {
        if (valid) {
         /* // 当重复添加相同数据时提示
          let flag = false
          this.dynamicTags.forEach((item) => {
            if (item.id === '6') {
              if (item.start === this.clsjSection.startDate && item.end === this.clsjSection.endDate) {
                flag = true
              }
            }
          })
          if (flag) {
            this.$message({
              message: '已添加相同区间筛选条件',
              type: 'warning',
              customClass: 'message-warning'
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
            //this.dynamicTags[_index].start = this.clsjSection.startDate
            //this.dynamicTags[_index].end = this.clsjSection.endDate
          }
        } else {
          return false
        }
      })
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
     * @description 运行状态监听radio
     */
    yxztChangeRadio(val) {
      const _index = this.dynamicTags.findIndex((item) => item.id === '2')
      const yxztObj = this.yxztData[0].options.find((item) => item.id === val)
      if (val === 2) {
        const yxztIndex = this.dynamicTags.findIndex((item) => item.id === '2')
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
      const _index = this.dynamicTags.findIndex((item) => item.id === '3')
      const sffjObj = this.sffjData[0].options.find((item) => item.id === val)
      if (val === 2) {
        const sffjIndex = this.dynamicTags.findIndex((item) => item.id === '3')
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
     * @description 是否代销监听radio
     */
    sfdxChangeRadio(val) {
      const _index = this.dynamicTags.findIndex(item => item.id === '102')
      const sfdxObj = this.sfdxData[0].options.find(item => item.id === val)
      if (val === 0) {
        const sfdxIndex = this.dynamicTags.findIndex(item => item.id === '102')
        this.dynamicTags.splice(sfdxIndex, 1)
        return
      }
      if (_index < 0) {
        this.dynamicTags.push({
          id: '102',
          title: '是否代销',
          value: sfdxObj.label,
          code: val
        })
      } else {
        this.dynamicTags[_index].value = sfdxObj.label
        this.dynamicTags[_index].code = val
      }
    },
    /**
     * @description 净值频率监听下拉
     */
    jzplChangeSelect(val) {
      const _index = this.dynamicTags.findIndex((item) => item.id === '4')
      const jzplObj = this.jzplOptions[0].options.find((item) => item.value === val)
      if (val === 3) {
        const jzplIndex = this.dynamicTags.findIndex((item) => item.id === '4')
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
      const _index = this.dynamicTags.findIndex((item) => item.id === '5')
      const jxpjObj = this.jxpjOptions[0].selectOptions.find((item) => item.value === val)
      if (val === 0) {
        const jxpjIndex = this.dynamicTags.findIndex((item) => item.id === '5')
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
      const jsqjObj = this.jsqjOptions[0].options.find((item) => item.value === val)
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
        /*// 当重复添加相同数据时提示
        let flag = false
        this.dynamicTags.forEach((item) => {
          if (item.id === id) {
            if (item.start === obj.start && item.end === obj.end) {
              flag = true
            }
          }
        })
        if (flag) {
          this.$message({
            message: '已添加相同区间筛选条件',
            type: 'warning',
            customClass: 'message-warning'
          })
          return
        }*/
        // 当重复添加不同数据时替换
        const _index = this.dynamicTags.findIndex((item) => item.id === id)
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
          if(id === '7'){
            this.zcjz[0].style = true
          }
          this.dynamicTags.push(temp)
        } else {
          const index_ = this.dynamicTags.findIndex(item => item.id === id)
          if (index_ !== -1) {
            this.dynamicTags.splice(index_, 1);
          }
          if(id === '7'){
            this.zcjz[0].style = false
          }
          /*this.dynamicTags[_index].start = obj.start
          this.dynamicTags[_index].end = obj.end
          this.dynamicTags[_index].prefix = this.currentJsqj*/
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
       /* // 当重复添加相同数据时提示
        let flag = false
        this.dynamicTags.forEach((item) => {
          let tempID = id
          if (obj.type && obj.type === 'jsqj') {
            tempID = this.currentJsqj + id
          }
          if (item.id === tempID) {
            if (item.prefix === this.currentJsqj) {
              if (item.start === obj[`start${this.currentJsqjValue}`] && item.end === obj[`end${this.currentJsqjValue}`]) {
                flag = true
              }
            }
          }
        })
        if (flag) {
          this.$message({
            message: '已添加相同区间筛选条件',
            type: 'warning',
            customClass: 'message-warning'
          })
          return
        }*/
        // 当重复添加不同数据时替换
        let _index = -1
        if (obj.type && obj.type === 'jsqj') {
          _index = this.dynamicTags.findIndex((item) => item.id === this.currentJsqj + id)
        } else {
          _index = this.dynamicTags.findIndex((item) => item.id === id)
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
          this.dynamicTags.forEach((item) => {
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
                /*this.dynamicTags[_index].start = obj[`start${this.currentJsqjValue}`]
                this.dynamicTags[_index].end = obj[`end${this.currentJsqjValue}`]
                this.dynamicTags[_index].prefix = this.currentJsqj*/
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
          type: 'warning',
          customClass: 'message-warning'
        })
        return false
      }
      // 校验是否为数字
      if (obj.start) {
        const reg = /^\.|\.$/
        if (isNaN(obj.start) || reg.test(obj.start)) {
          this.$message({
            message: '请输入数字',
            type: 'warning',
            customClass: 'message-warning'
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
            type: 'warning',
            customClass: 'message-warning'
          })
          return false
        }
      }
      // 结束区间不能小于开始区间
      if (obj.start && obj.end) {
        if (Number(obj.start) >= Number(obj.end)) {
          this.$message({
            message: '结束区间不能小于或等于开始区间',
            type: 'warning',
            customClass: 'message-warning'
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
          type: 'warning',
          customClass: 'message-warning'
        })
        return false
      }
      // 校验是否为数字
      if (obj[objStart]) {
        const reg = /^\.|\.$/
        if (isNaN(obj[objStart]) || reg.test(obj[objStart])) {
          this.$message({
            message: '请输入数字',
            type: 'warning',
            customClass: 'message-warning'
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
            type: 'warning',
            customClass: 'message-warning'
          })
          return false
        }
      }
      // 结束区间不能小于开始区间
      if (obj[objStart] && obj[objEnd]) {
        if (Number(obj[objStart]) >= Number(obj[objEnd])) {
          this.$message({
            message: '结束区间不能小于或等于开始区间',
            type: 'warning',
            customClass: 'message-warning'
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
        this.investStrategy.forEach((item) => {
          item.checked = false
        })
        const DomBx = document.querySelector('.tzclbx-focus')
        DomBx.style.backgroundColor = '#e9c5a5'
        DomBx.style.color = '#612d10'
        DomBx.style.borderColor = '#e9c5a5'
      }
      if (tag.id === '100') {
        this.investSubStrategy.forEach(item => {
          item.checked = false
        })
        const SubDomBx = document.querySelector('.tzsubclbx-focus')
        SubDomBx.style.backgroundColor = '#e9c5a5'
        SubDomBx.style.color = '#612d10'
        SubDomBx.style.borderColor = '#e9c5a5'
      }
      // 删除运行状态
      if (tag.id === '2') {
        this.yxztData[0].checked = 2
      }
      // 删除是否分级
      if (tag.id === '3') {
        this.sffjData[0].checked = 2
      }

      // 删除是否代销
      if (tag.id === '102') {
        this.sfdxData[0].checked = 0
      }
      // 删除净值频率
      if (tag.id === '4') {
        this.jzplOptions[0].selected = 3
      }
      // 删除绩效评级
      if (tag.id === '5') {
        this.jxpjOptions[0].selected = 0
      }
      // 删除成立时间
      if (tag.id === '6') {
        this.clsjSection.startDate = ''
        this.clsjSection.endDate = ''
        this.clsjSelect = '1'
        this.clsjSection.style = false
      }
      // 删除资产净值
      if (tag.id === '7') {
        this.zcjz[0].start = ''
        this.zcjz[0].end = ''
        this.zcjz[0].style = false
      }
      // 删除成立以来大类资产占比(平均值)
      if (['15', '16', '17', '18'].includes(tag.id)) {
        this.clearSinceTheInput(tag.id, tag.name)
      }

      // 删除计算区间
      if (['10', '11', '12', '13', '14'].includes(idNum)) {
        this.clearJSQJInput(idNum, idStr)
      }

      const index = this.dynamicTags.findIndex((item) => item.id === tag.id)
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
      let index = ['近六月', '近一年', '今年以来', '成立以来'].findIndex((item) => item == idStr)
      for (let i = 0; i < this.sylzdhcData.length; i++) {
        let temp = this.sylzdhcData[i]
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
      // 重置清空投资策略
      this.investStrategy.forEach((item) => {
        item.checked = false
      })
      // 重置清空子策略
      this.investSubStrategy.forEach((item) => {
        item.checked = false
      })
      // 重置清空运行状态
      this.yxztData[0].checked = 2
      // 重置清空是否分级
      this.sffjData[0].checked = 2
      // 重置清空净值频率
      this.jzplOptions[0].selected = 3
      // 重置清空绩效评级
      this.jxpjOptions[0].selected = 0
      // 重置清空成立时间
      this.clsjSection.startDate = ''
      this.clsjSection.endDate = ''
      this.clsjSelect = '1'
      this.clsjSection.style = false
      // 重置清空资产净值
      this.zcjz[0].start = ''
      this.zcjz[0].end = ''
      this.zcjz[0].style = false
      // 重置清空成立以来大类资产占比(平均值)
      this.sinceThe.forEach((item) => {
        item.start = ''
        item.end = ''
      })

      // 清空计算区间
      for (let i = 0; i < this.sylzdhcData.length; i++) {
        let temp = this.sylzdhcData[i]
        for (let j = 1; j <= 4; j++) {
          temp[`start${j}`] = ''
          temp[`end${j}`] = ''
          temp[`style${j}`] = false
        }
      }

      const DomBx = document.querySelector('.tzclbx-focus')
      DomBx.style.backgroundColor = '#e9c5a5'
      DomBx.style.color = '#612d10'
      DomBx.style.borderColor = '#e9c5a5'
      this.dynamicTags = []
    }
  }
}
</script>

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
  .tzsubcl,
  .tzthirdcl,
  .yxtj {
    ::v-deep .el-form-item__content {
      flex: 1;
    }
  }

  .tzclbx-focus {
    border: 1px solid #e9c5a5;
    border-radius: 4px;
    height: 26px;
    line-height: 26px;
    padding: 0px 10px;
    margin-right: 10px;
    background-color: #e9c5a5;
    color: #612d10;
    cursor: pointer;
  }

  .tzclbx-focus:hover {
    border: 1px solid #e9c5a5;
    border-radius: 4px;
    color: #612d10;
  }

  .tzsubclbx-focus {
    border: 1px solid #e9c5a5;
    border-radius: 4px;
    height: 26px;
    line-height: 26px;
    padding: 0px 10px;
    margin-right: 10px;
    background-color: #e9c5a5;
    color: #612d10;
    cursor: pointer;
  }

  .tzsubclbx-focus:hover {
    border: 1px solid #e9c5a5;
    border-radius: 4px;
    color: #612d10;
  }

  .tzthirdclbx-focus {
    border: 1px solid #e9c5a5;
    border-radius: 4px;
    height: 26px;
    line-height: 26px;
    padding: 0px 10px;
    margin-right: 10px;
    background-color: #e9c5a5;
    color: #612d10;
    cursor: pointer;
  }

  .tzthirdclbx-focus:hover {
    border: 1px solid #e9c5a5;
    border-radius: 4px;
    color: #612d10;
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
    border: 2px solid #e9c5a5;
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
    border: 2px solid #e9c5a5;
    background-color: #fff;
    padding-left: 5px;
    display: flex;

    span {
      padding: 0 5px;
    }
  }

  .itemBox {
    border: 1px solid #e1e0e0;
    height: 26px;
    padding: 2px 8px;
    border-radius: 4px;
    margin-right: 10px;

    span:hover {
      color: #612d10;
    }
  }

  .itemBox:hover {
    border: 1px solid #e9c5a5;
    border-radius: 4px;

  }

  .itemBox-checked {
    border: 1px solid #e9c5a5;
    height: 26px;
    border-color: #e9c5a5;
    background: #e9c5a5;
    padding: 2px 8px;
    margin-right: 10px;
    border-radius: 4px;

  }

  // elementUI样式穿透
  .jzpl {
    ::v-deep .el-radio.is-checked {
      border: 1px solid #e1e0e0;
      border-radius: 1px;
      border-color: #e9c5a5;
      background: #e9c5a5;
      color: #612d10;
    }

    ::v-deep .el-radio:hover {
      border: 1px solid #e9c5a5;
      border-radius: 1px;
      color: #612d10;
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
  .tzsubcl,
  .tzthirdcl,
  .sfradio,
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
      color: #612d10;
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

  .sfradio {
    ::v-deep .el-radio--small.is-bordered {
      height: 26px;
      border-radius: 4px;
      padding: 5px 15px 0 10px;
    }
    ::v-deep .el-radio.is-bordered.is-checked {
      border-color: #e9c5a5;

      ::v-deep .el-radio__input.is-checked + .el-radio__label {
        color: #612d10;
      }
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
      background-image: linear-gradient(to right, #f5d7bc, #e0b794)!important;
    }
  }
}
::v-deep .el-checkbox__input.is-checked .el-checkbox__inner, .el-checkbox__input.is-indeterminate .el-checkbox__inner {
  border-color: #e9c5a5;
  background-color: #e2a971
}
::v-deep .el-checkbox__inner:hover {
  border-color: #e9c5a5!important
}
::v-deep .el-checkbox__input.is-focus .el-checkbox__inner {
  border-color: #e9c5a5
}
::v-deep .el-tag .el-tag__close {
  color: #612d10
}
::v-deep .el-tag .el-tag__close:hover {
  background-color: transparent
}

::v-deep.el-button.el-button--gfcheck.el-button--small {
  border: none !important;
  color: #612d10 !important;
  font-size: 14px !important;
  padding: 7px 28px !important;
}
::v-deep.el-button.el-button--gfcheck.el-button--small:hover {
  background-image: linear-gradient(to right, #ddb592, #cb9b72) !important;
  font-size: 14px !important;
  color:  #612d10 !important;
  padding: 7px 28px !important;
}
</style>

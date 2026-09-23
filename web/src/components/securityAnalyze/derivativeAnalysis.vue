<template>
  <div class="derivativeAnalysis">
    <!--<div class="forms_table_title"><i class="el-icon-s-data"></i>总体期货绩效归因</div>-->
    <!--<el-row :gutter="40" class="margin_top_common">-->
      <!--<el-col :span="12">-->
        <!--<div class="border_box">-->
          <!--<div id="myEcharts" class="echarts_box"></div>-->
        <!--</div>-->
      <!--</el-col>-->

      <!--<el-col :span="12">-->
        <!--<div class="border_box">-->
          <!--&lt;!&ndash;列表&ndash;&gt;-->
          <!--<el-table-->
            <!--:data="tableData"-->
            <!--stripe-->
            <!--border-->
            <!--style="width: 100%">-->
            <!--<el-table-column-->
              <!--prop="one1"-->
              <!--show-overflow-tooltip-->
              <!--sortable-->
              <!--label="资产分类"-->
              <!--min-width="120"-->
              <!--align="center">-->
            <!--</el-table-column>-->
            <!--<el-table-column-->
              <!--prop="one2"-->
              <!--show-overflow-tooltip-->
              <!--sortable-->
              <!--label="权重（占净值比）（%）"-->
              <!--min-width="210"-->
              <!--align="center">-->
            <!--</el-table-column>-->
            <!--<el-table-column-->
              <!--prop="one3"-->
              <!--show-overflow-tooltip-->
              <!--sortable-->
              <!--label="净值贡献度（%）"-->
              <!--min-width="170"-->
              <!--align="center">-->
            <!--</el-table-column>-->
            <!--<el-table-column-->
              <!--prop="one4"-->
              <!--show-overflow-tooltip-->
              <!--sortable-->
              <!--label="收益额"-->
              <!--min-width="120"-->
              <!--align="center">-->
            <!--</el-table-column>-->
          <!--</el-table>-->
        <!--</div>-->
      <!--</el-col>-->
    <!--</el-row>-->

    <div class="forms_table_title"><i class="el-icon-s-data"></i>股指期货绩效归因</div>
    <el-form :inline="true" ref="formQuery" :model="formQuery" :rules="rules" class="mb10">
      <el-row>
        <el-col :span="19">
          <el-form-item label="日期" prop="beginDate" class="mb20">
            <el-date-picker
              size="small"
              v-model="formQuery.beginDate"
              type="date"
              value-format="yyyy-MM-dd"
              placeholder="选择日期">
            </el-date-picker>
          </el-form-item>
          <el-form-item label="组合类型" prop="fundType">
            <el-select size="small" v-model="formQuery.fundType" multiple placeholder="请选择" >
              <el-option
                v-for="(group, index) in groupTypeArr"
                :value="group.dimCde"
                :key="index"
                :label="group.dimNme">
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="投资经理" prop="account" v-if="isAccount">
            <el-select size="small" v-model="formQuery.account"  placeholder="请选择">
              <el-option
                v-for="item in manageArr"
                :key="item.account"
                :label="item.userName"
                :value="item.account">
              </el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="5">
          <el-form-item class="search_button_com">
            <el-button type="primary" size="small" @click="onQuery('formQuery')">查询</el-button>
            <el-button plain size="small" @click="resetForm('formQuery')">重置</el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <el-row :gutter="40">
      <el-col :span="12">
        <div class="border_box" style="padding-top: 20px;">
          <div id="myEcharts2" class="echarts_box"></div>
        </div>
      </el-col>

      <el-col :span="12">
        <div class="border_box">
          <!--列表2-->
          <el-table
            :data="tableData2"
            stripe
            border
            style="width: 100%">
            <el-table-column
              prop="one1"
              show-overflow-tooltip
              sortable
              label="资产分类"
              min-width="120"
              align="center">
            </el-table-column>
            <el-table-column
              prop="one2"
              show-overflow-tooltip
              sortable
              label="权重（占净值比）（%）"
              min-width="210"
              align="center">
            </el-table-column>
            <el-table-column
              prop="one3"
              show-overflow-tooltip
              sortable
              label="净值贡献度（%）"
              min-width="170"
              align="center">
            </el-table-column>
            <el-table-column
              prop="one4"
              show-overflow-tooltip
              sortable
              label="收益额"
              min-width="120"
              align="center">
            </el-table-column>
          </el-table>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import commonApi from '@/api/common'
import investmentManagerApi from '@/api/managementView/investmentManager'

export default {
  name: "derivative-analysis",
  props: {
    // 是否显示投资经理下拉
    isAccount: {
      type: Boolean,
      default: true
    }
  },
  data() {
    const validateDate = (rule, value, callback) => {
      if(value == ''){
        callback(new Error('请选择日期'))
      }
      else{
        callback()
      }
    }
    return {
      // 查询参数
      formQuery:{
        // 日期
        beginDate:'',
        // 组合类型
        fundType: '',
        // 投资经理
        account: '',
        // 组合代码集合
        fundList: []
      },
      // 组合类型数组
      groupTypeArr: [],
      // 投资经理数组
      manageArr: [],
      // 验证规则
      rules:{
        beginDate: [{ required: true, trigger: 'change', validator: validateDate }]
      },
      // 衍生品分析图表
      myEcharts: null,
      // 股指期货归因图表
      myEcharts2: null,
      // 总体期货绩效归因列表
      tableData: [
        {
          one1: '商品期货',
          one2: '0.207',
          one3: '4.226',
          one4: '404275.00'
        },
        {
          one1: '股指期货',
          one2: '-0.100',
          one3: '2.104',
          one4: '201320.00'
        },
        {
          one1: '汇总',
          one2: '0.107',
          one3: '6.330',
          one4: '605595.00'
        }
      ],
      // 商品期货绩效归因列表
      tableData2: [
        {
          one1: '化工',
          one2: '0.207',
          one3: '4.226',
          one4: '404275.00'
        },
        {
          one1: '金属',
          one2: '-0.100',
          one3: '2.104',
          one4: '201320.00'
        },
        {
          one1: '农产品',
          one2: '0.207',
          one3: '4.226',
          one4: '404275.00'
        },
        {
          one1: '能源',
          one2: '-0.100',
          one3: '2.104',
          one4: '201320.00'
        },
        {
          one1: '汇总',
          one2: '0.107',
          one3: '6.330',
          one4: '605595.00'
        }
      ]
    }
  },
  mounted(){
    // 组合类型列表查询
    this.getListEdims()
    if (!this.isAccount) {
      this.formQuery.account = -1
    } else {
      // 投资经理列表查询
      this.getManagerList()
    }
    this.$nextTick(() => {
      // 衍生品分析图表初始化
      // this.initEcharts()
      // 股指期货归因图表初始化
      this.initEcharts2()
    })
    // 宽度变化重新渲染图表
    window.onresize = () => {
      // this.myEcharts.resize()
      this.myEcharts2.resize()
    }
  },
  methods: {
    // 查询
    onQuery(formName){
      this.$refs[formName].validate((valid) => {
        if (valid) {

        }
      })
    },
    // 清除
    resetForm (formName) {
      this.$refs[formName].resetFields()
    },
    // 衍生品分析图表初始化
    // initEcharts () {
    //   let groupName = ['商品期货', '股指期货'] // 分类名字
    //   let data1 = [0.207, 4.226] // 权重（占净值比）（%）
    //   let data2 = [4.12, 2.2] // 净值贡献度（%）
    //   this.myEcharts = echarts.init(document.getElementById('myEcharts'))
    //   this.myEcharts.setOption({
    //     title: {
    //       text: ''
    //     },
    //     tooltip : {
    //       trigger: 'axis',
    //       axisPointer : {            // 坐标轴指示器，坐标轴触发有效
    //         type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
    //       },
    //     },
    //     color:['#18A9FF','#FF4D4F'],
    //     legend: {
    //       data: ['权重（占净值比）（%）','净值贡献度（%）'],
    //       // show:false,
    //     },
    //     toolbox: {
    //       feature: {
    //         saveAsImage: {}
    //
    //       }
    //     },
    //     grid: {
    //       left: '3%',
    //       right: '4%',
    //       bottom: '3%',
    //       containLabel: true
    //     },
    //     xAxis: {
    //       type : 'category',
    //       splitLine: {show:false},
    //       data : groupName,
    //       axisLabel: {
    //         interval:0,
    //         rotate:20
    //       }
    //     },
    //     yAxis: {
    //       // name: '亿',
    //       type : 'value'
    //     },
    //     series: [
    //       {
    //         name: '权重（占净值比）（%）',
    //         type: 'bar',
    //         barWidth : 30,
    //         data: data1
    //       },
    //       {
    //         name: '净值贡献度（%）',
    //         type: 'bar',
    //         barWidth : 30,
    //         label: {
    //           normal: {
    //             show: false,
    //             position: 'top'
    //           }
    //         },
    //         data: data2
    //       }
    //     ]
    //   })
    // },
    // 组合类型列表查询
    getListEdims () {
      // 字典类型
      let params = 'fund_type'
      commonApi.edimsCommon(params).then(res => {
        let { status, data } = res.data
        if (status === 0) {
          this.groupTypeArr = data
        }
      })
    },
    // 投资经理列表查询
    getManagerList () {
      let params = 0
      investmentManagerApi.managerList(params).then(res => {
        let { status, data } = res.data
        if (status === 0) {
          this.manageArr = data
        }
      })
    },
    // 股指期货归因图表初始化
    initEcharts2 () {
      let groupName = ['化工', '金属', '农产品', '能源'] // 分类名字
      let data1 = [-0.132, 0, 0, 0.338] // 权重（占净值比）（%）
      let data2 = [-0.169, 0, 0, -0.374] // 净值贡献度（%）
      this.myEcharts2 = echarts.init(document.getElementById('myEcharts2'))
      this.myEcharts2.setOption({
        title: {
          text: ''
        },
        tooltip : {
          trigger: 'axis',
          axisPointer : {            // 坐标轴指示器，坐标轴触发有效
            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
          },
        },
        color:["#8EB4E3","#CCC1DA","#FAC090","#E6B9B8"],
        legend: {
          data: ['权重（占净值比）（%）','净值贡献度（%）'],
          // show:false,
        },
        toolbox: {
          feature: {
            saveAsImage: {}

          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type : 'category',
          splitLine: {show:false},
          data : groupName,
          axisLabel: {
            interval:0,
            rotate:20
          }
        },
        yAxis: {
          type : 'value'
        },
        series: [
          {
            name: '权重（占净值比）（%）',
            type: 'bar',
            barWidth : 30,
            data: data1
          },
          {
            name: '净值贡献度（%）',
            type: 'bar',
            barWidth : 30,
            label: {
              normal: {
                show: false,
                position: 'top'
              }
            },
            data: data2
          }
        ]
      })
    }
  },
  watch: {
    // 监听组合类型变化
    'formQuery.fundType' (val, oldval) {
      if (val.indexOf('*') != -1 && oldval.indexOf('*') == -1 && val.length > 1) {
        this.formQuery.fundType = ['*']
      } else if (val.indexOf('*') != -1 && oldval.indexOf('*') != -1 && val.length > 1){
        this.formQuery.fundType.splice(val.indexOf('*'), 1)
      }
    }
  }
}
</script>

<style langg="scss" scoped>

</style>

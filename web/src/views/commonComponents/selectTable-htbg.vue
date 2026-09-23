<template>
  <div class="inputTableStyle" @click.stop="" @keyup.enter="selsectTableFirst">
    <el-input ref="inputFocus" placeholder="请选择" @focus='inputFocus' v-model="slValue" @input="searchData" clearable @clear='clearInput' maxlength="30" :disabled="disabled"></el-input>
    <div v-show="isTableSelect" class="selectTableStyle" :style="tableWidth">
      <el-table
          :data="tableList"
          border
          @row-click='rowClick'
          class="table"
          highlight-current-row
          ref="tableSelect"
          max-height="240">
        <el-table-column show-overflow-tooltip label="产品" min-width="180" prop="codeName" header-align="center"></el-table-column>
        <el-table-column show-overflow-tooltip label="托管机构" prop="trustorName" min-width="100" header-align="center"></el-table-column>
        <el-table-column show-overflow-tooltip label="基金服务机构" prop="operatorName" min-width="100" header-align="center"></el-table-column>
      </el-table>
    </div>
  </div>
</template>
<script>
import pageApi from "@/api/productNew/contractManage.js"
import $ from "jquery";
export default {
  // props: ['modelValue', 'width'],
  props: {
    modelValue:{},
    width:{},
    disabled:{
      default:false
    }
  },
  model: {
    prop: 'modelValue',
    event: 'sendData'
  },
  watch: {
    modelValue(data) {
      this.slValue = data
      if (data == '') {
        this.slValue = data
        this.slRow = {}
        this.$emit('sendDataObj', '')
        // this.tableList = this.tableListTemp
        // this.getProductInfo()
      } else {
        // console.log(data,'data');
        if(data){
          let isAllMatch = data.split('_')
          if (isAllMatch.length > 1 && !this.hasSelectRow) this.matchingAll()
        }
      }
    },
    isTableSelect (data) {
      if (this.hasSelectRow) this.judge()
      else {
        this.allSearch()
      }
    }
  },
  data () {
    return {
      tableWidth: {
        width: this.width || '600px'
      },
      slValue: '',
      hasSelectRow: false,
      slRow: {},
      isTableSelect: false,
      tableList: [],
      tableListTemp: []
    }
  },
  mounted() {
    let that = this
    $("body").on("click", function () {
      that.isTableSelect = false
    })
   this.getProductInfo()
   this.tableList = []
   this.tableListTemp = []
  },
  methods: {
   //查询产品信息
    getProductInfo(){
      this.$message.closeAll();
      pageApi.getFundCode().then(({ data: res }) =>{
        if(res.status === 0){
          let temp = [...res.data]
          for (let i of temp) { i['codeName'] = i.fundCode + "_"+ i.fundName }
          this.tableListTemp = temp
          this.tableList = temp
        } else this.$message.error('查询产品信息失败');
      }).catch((err) => { this.$message.error('查询产品信息失败') })
    },
    rowClick (row) {
      this.slValue = JSON.parse(JSON.stringify(row.codeName))
      this.slRow = JSON.parse(JSON.stringify(row))
      this.isTableSelect = false
      this.hasSelectRow = true
      this.$emit('sendData', this.slValue)
      this.$emit('sendDataObj', this.slRow)
    },
    // 检验输入框的值是否存在
     judge () {
      let isClear = this.tableList.filter((item) =>{
        return item.codeName == this.slValue
      })
      if (isClear.length == 0) {
        this.slValue = ''
        this.hasSelectRow = false
        this.$emit('sendData', '')
      }
    },
    // 相对匹配
    allSearch () {
      if (!this.slValue) return
      let query = 'codeName'
      let reg = /^[a-zA-Za-z0-9]+$/
      if (this.slValue.includes('_')) query = 'codeName'
      else {
        if (reg.test(this.slValue)) query = 'fundCode'
        else query = 'fundName'
      }
      pageApi.getFundCode().then(({ data: res }) =>{
        if(res.status === 0){
          let temp = [...res.data]
          for (let i of temp) { i['codeName'] = i.fundCode + "_"+ i.fundName }
          let newData = temp.filter((itme) => {
          if ( itme[query] == this.slValue ) return itme
         })
         if (newData.length == 0) {
            this.slValue = ''
            this.hasSelectRow = false
            this.$emit('sendData', '')
          }
        }
      }).catch(() => {})
    },
    // 全匹配回调
    matchingAll () {
      pageApi.getFundCode().then(({ data: res }) =>{
        if(res.status === 0){
          let temp = [...res.data]
          for (let i of temp) { i['codeName'] = i.fundCode + "_"+ i.fundName }
          let newData = temp.filter((itme) => {
          if ( itme['codeName'] == this.slValue ) return itme
         })
         if (newData.length == 1) {
            this.$emit('sendDataObj', newData[0])
          } else this.$emit('sendDataObj', '')
        }
      }).catch(() => {})
    },
    clearInput () {
      this.getProductInfo()
      this.$emit('sendData', '')
    },
    //回车选择第一天
    selsectTableFirst () {
      if (this.tableList.length !=0 ) {
        let row = this.tableList[0]
        this.rowClick(row)
        this.$refs.inputFocus.blur()
        this.$emit('enter')
      }
    },
    // 获取焦点
    inputFocus () {
      this.isTableSelect = true
      this.tableList = this.tableListTemp
      if (this.slValue) {
        let code = this.slValue.split('_')[0]
        for (let i of this.tableList) {
          if (i.fundCode == code) {
            this.$refs.tableSelect.setCurrentRow(i)
            break
          }
        }
      }
    },
    //input查找
    searchData (data) {
      if (!data) {
        this.$emit('sendData', '');
        return this.getProductInfo();
      }
      this.tableList = []
      // let reg = /^[a-zA-Za-z0-9\u4e00-\u9fa5\-\_]+$/
      let newData = this.tableListTemp.filter((itme) => {
        if (itme.codeName.includes(data)) return itme
      })
      this.tableList = [...newData]
    },
    // 焦点获取
    relation () {
      this.$nextTick(() => {
        this.$refs.inputFocus.focus()
      })
    }
  }
}
</script>
<style lang='scss' scoped>
.inputTableStyle {
  position: relative;
  .selectTableStyle {
    position: absolute;
    margin-top: 2px;
    z-index: 20;
    box-sizing: border-box;
    padding: 1px;
    box-shadow: 0,0,0, rgb(83, 117, 212);
    border-radius:5px;
    border: 1px solid #ccc;
    overflow: hidden;
    .table {
      border: 1px solid #f1f1f1;
      box-shadow: 0 0 0 1px #f1f1f1;
    }
  }
}
</style>
<template>
  <div class="multipleTableStyle" @click.stop="">
    <el-input v-model="multiplevalue"
        type="textarea" maxlength="30"
        @focus="focusInput" @input="inputvalue"
        :autosize="{minRows: 1,maxRows: 4}"
        ref="inputFocus" style="width: 100%"></el-input>
    <div v-show="isTableSelect" class="selectTableStyle" :style="tableWidth">
      <el-table
          :data="tableList"
          border
          @row-click='rowClick'
          @selection-change='selectionChange'
          class="table"
          highlight-current-row
          ref="tableSelect"
          max-height="240">
        <el-table-column type="selection" width="55" align="center" header-align="center"></el-table-column>
        <el-table-column show-overflow-tooltip label="产品" min-width="180" prop="codeName" header-align="center"></el-table-column>
        <el-table-column show-overflow-tooltip label="托管机构名称" prop="trustorName" min-width="100" header-align="center"></el-table-column>
        <el-table-column show-overflow-tooltip label="基金服务机构名称" prop="operatorName" min-width="100" header-align="center"></el-table-column>
      </el-table>
    </div>
  </div>
</template>
<script>
import bizBeginApi from '@/api/transfer/bizBegin'
import $ from "jquery"
export default {
  props: ['multiple', 'width'],
  model: {
    prop: 'multiple',  //接受传过来的值
    event: 'multipleSelectChange'  //触发事件传返回值
  },
  watch: {
    multiple (data) {
      // console.log(data)
      if (data.length == 0) {
        this.tableList = this.tableListTemp
        // this.$refs.tableSelect.clearSelection()
        this.multiplevalue = '' }
    }
  },
  data () {
    return {
      tableWidth: {
        width: this.width || '600px'
      },
      multiplevalue: '',
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
    this.multiplevalue = ''
  },
  methods: {
    //查询产品信息
    getProductInfo(){
      this.$message.closeAll();
      bizBeginApi.getProductFund().then(({ data: res }) =>{
        if(res.status === 200){
          let temp = [...res.data]
          for (let i of temp) { i['codeName'] = i.fundCode + "_"+ i.fundName }
          this.tableListTemp = [ ...temp ]
          this.tableList = [ ...temp ]
        } else this.$message.error('查询产品信息失败');
      }).catch((err) => { this.$message.error('查询产品信息失败') })
    },
    rowClick (row) {},
    selectionChange (list) {
      let selectList = [ ...list ]
      let str = '', temp = []
      for (let i of list) temp.push(i.codeName)
      str = temp.join(',')
      this.multiplevalue = str
      this.$emit('multipleSelectChange', temp)
      this.$emit('change', temp)
    },
    // 获取焦点
    focusInput () {
      this.isTableSelect = true
    },
    // 获取输入值
    inputvalue (data) {
      if (!data) return this.tableList = this.tableListTemp
      this.tableList = []
      let newData = this.tableListTemp.filter((itme) => {
        if (itme.codeName.includes(data)) return itme
      })
      this.tableList = [...newData]
    },
    // 清空值
    clearInput () {

    }
  }
}
</script>
<style lang='scss' scoped>
.multipleTableStyle {
  position: relative;
  width: 348px;
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
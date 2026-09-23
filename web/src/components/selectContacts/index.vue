<template>
  <div class="select_contacts" @click.stop="">
      <el-select ref="inputFocus" filterable :filter-method="inputvalue" popper-class='select_xlk' style="width:100%" @remove-tag='remove_tag' @focus='inputFocus' multiple v-model="slValue" >
        <el-option
        style="display:none"
        label="11"
        value="value">
      </el-option>
      </el-select>
      <!-- <el-input ref="inputFocus" @focus='inputFocus' multiple v-model="slValue"  clearable></el-input> -->
      <div v-show="isTableSelect" class="selectTableStyle">
        <el-table
          @selection-change="handleSelectionChange"
            :data="tableList"
            @row-click='rowClick'
            border
            class="table"
            ref="tableSelect"
            max-height="240">
          <el-table-column type="selection" width="55" align="center" :selectable='selected'></el-table-column>
          <el-table-column show-overflow-tooltip label="姓名" prop="contactName" header-align="center"></el-table-column>
          <el-table-column show-overflow-tooltip label="机构" prop="trustorName" min-width="100" header-align="center"></el-table-column>
          <el-table-column show-overflow-tooltip label="邮箱" prop="email" min-width="100" header-align="center"></el-table-column>
          <el-table-column show-overflow-tooltip label="手机号" prop="phone" min-width="100" header-align="center"></el-table-column>
        </el-table>
      </div>
  </div>
</template>

<script>
import $ from 'jquery'
import pageApi from "@/api/home/calendarList";
export default {
  props: ['modelValue', 'width','defaultValue'],
  model: {
    prop: 'modelValue',
    event: 'sendData'
  },
  watch:{
    modelValue(data){
      if(data.length){
        this.checked(data)

        // this.slValue = data;
      }else{
        this.slValue = [];
      }
      // console.log('this.slValue',data);
    },
    // defaultValue(data){
    //   console.log('defaultValue',data);
    //   this.slValue = data;
    // }
  },
  data(){
    return{
      tableList:[],
      tableListTemp:[],
      slValue:[],
      isTableSelect:false
    }
  },
  mounted(){
    // this.slValue=['aaa','bbb']
    let that = this;
    $('body').on('click',()=>{
      that.isTableSelect=false;
      this.tableList = this.tableListTemp;
    })
    this.getContactList()
  },
  // activated(){
  //   console.log('aaaaaa');
  // },
  // deactivated(){},
  methods:{
    inputvalue(val){
      // console.log(val);
      if(!val){
        this.tableList = this.tableListTemp;
      }
      if(val){
        let newData = this.tableList.filter((item) => {
          // console.log(item);
          if(item.contactName){
            if (item.contactName.includes(val)) return item
          }
        })
        this.tableList = [...newData]
      }
    },
    rowClick(row){
      // console.log(row);
    },
    handleSelectionChange(val){
      // console.log('handleSelectionChange',val);
      if(val.length){
        let slval=val.map(item=>{
          return item.contactName
        })
        // console.log(slval);
        this.slValue=slval;
      }else{
        this.slValue=[]
      }
      
      let slval_id=val.map(item=>{
        return item.id
      })
      // console.log('slval_id',slval_id);
      this.$emit('sendData',slval_id)
    },
    inputFocus () {
      this.isTableSelect = true;
      this.tableList = this.tableListTemp;
    },
    inputBlur(){
      this.isTableSelect = false
    },
    remove_tag(val){
      // console.log(val);
      let item = this.tableList.filter(item=>{
        return item.contactName==val
      })
      // console.log(item);
      this.$refs.tableSelect.toggleRowSelection(item[0],false);
    },
    remove_all(){
      this.$refs.tableSelect.clearSelection();
    },
    // 默认选中
    checked(data){
      setTimeout(() => {
        if(data.length>0 && this.tableListTemp.length>0){
          for(let i=0;i<data.length;i++){
          //   let item = this.tableList.filter(item=>{
          //     return item.contactName==data[i]
          //   })
          //   console.log(item,'item');
          //   this.$refs.tableSelect.toggleRowSelection(item[0],true);
            this.tableListTemp.forEach(item => {
              if(item.id && item.id==data[i]){
                // console.log(item,i,this.slValue[i]);
                this.$nextTick(()=>{
                  this.$refs.tableSelect.toggleRowSelection(item,true);
                })
              }
            });
            // let a= this.tableList.filter(item=>{
            //   if(item.id && item.id==data[i]){
            //     return item.contactName
            //   }
            // })
            // console.log('aaaaa',a);
            // this.tableList.forEach(item => {
            //   if(item.contactName && item.contactName==this.slValue[i]){
            //     // console.log(item,i,this.slValue[i]);
            //     this.$nextTick(()=>{
            //       this.$refs.tableSelect.toggleRowSelection(item,true);
            //     })
            //   }
            // });
          }
          
        }
      }, 500);
    },
    selected(row,index){
      if(row.email) return true 
      if(!row.email) return false 
    },
    getContactList(){
      let params={}
      pageApi
        .getContactList(params)
        .then((response) => {
          if (response.data.status === 200) {
            this.tableList = response.data.data.list;
            this.tableListTemp = response.data.data.list;
            
            // this.checked(this.slValue)
            // if (list.length === 0) this.$message.error('查询不到当前联系人')
          } else {
            this.tableList = [];
            this.tableListTemp = [];
            this.$message.error(response.data.message || '服务异常')
          }
        })
        .catch(() => {
          this.tableList = [];
          this.$message.error(response.data.message || '服务异常')
        });
    }
  }
}
</script>

<style lang='scss' scoped>

.select_contacts {
  position: relative;
  // width: 348px;
  .selectTableStyle {
    width: 500px;
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
<style lang='scss'>
.select_contacts{
  .el-select__tags-text{
    display: inline-block;
    width: 65px;
    overflow: hidden;
    text-overflow: ellipsis;
    // margin-right: -9px;
  }
  // .el-tag__close{
  //   position: relative;
  //   top: -6px !important;
  // }
  .el-select__caret{
    display: none;
  }
}
.select_xlk{
  display: none !important;
  z-index: -1 !important;
}
</style>
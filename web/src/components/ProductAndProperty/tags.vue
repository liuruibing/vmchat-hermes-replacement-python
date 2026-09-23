<template>
   <div>
     <el-row>
       <el-col :span="19">
         <!--标签卡显示-->
         <el-tag
           :key="index"
           v-for="(tag,index) in tags.slice((this.pageNumber-1)*this.pageSize,this.pageNumber*this.pageSize).length > 0 ? tags.slice((this.pageNumber-1)*this.pageSize,this.pageNumber*this.pageSize) : tags.slice((this.pageNumber-2)*this.pageSize,(this.pageNumber - 1)*this.pageSize)"
           closable
           :disable-transitions="false"
           @close="handleClose(tag)">
           {{tag.label}}
         </el-tag>

       </el-col>
       <el-col :span="5">
         <el-button v-if="tags != ''" @click="closeAll" type="primary" class="search_button_com" size="small" plain>清空组合选择</el-button>
       </el-col>
     </el-row>

     <Pagination v-show="total > 10" :total = "total"  :limit = "pageSize"  @pagination="Pagination"></Pagination>

   </div>
</template>

<script>
  import Pagination from '@/components/Pagination'
    export default {
      name: "product-tabs",
      components: {Pagination},
      props: {
        ProductAndPropertyData: {
          tagsName:'',// 组合列表 tag子组件传值区分
        },
      },
      data() {
        return {
          tags:[],
          total:0,
          pageSize:10,
          pageNumber:1,
        }
      },
      mounted(){
          let self = this;
          self.$bus.$on('productCheckClickTags'  + self.ProductAndPropertyData.tagsName , self.fun_productCheckClickTags);
      },
      //消除多次传输
      beforeDestroy () {
        this.$bus.$off('productCheckClickTags'  + this.ProductAndPropertyData.tagsName , this.fun_productCheckClickTags);
      },
      methods:{
          //接收产品下拉框传输的值
        fun_productCheckClickTags(data){
          let self = this;
          //赋值给标签卡
          self.tags = data.data;
          self.total = data.data.length;
        },
        // 标签卡关闭事件
        handleClose(val) {

          let self = this;
          //截取选择的值
          self.tags.splice(self.tags.indexOf(val), 1);
          self.total = self.tags.length;
          self.$bus.$emit('productCheckClickTagsClose'  + self.ProductAndPropertyData.tagsName ,self.tags);

        },
        // 标签卡关闭全部事件
        closeAll() {
          let self = this;
          self.tags = [];
          self.total = 0;
          self.$bus.$emit('productCheckClickTagsClose'  + self.ProductAndPropertyData.tagsName ,self.tags);

        },
        Pagination(val){
          let self = this;
          self.pageSize = val.limit;//页面条数
          self.pageNumber = val.page;//页面
        }

      }






  }
</script>

<style scoped>

</style>

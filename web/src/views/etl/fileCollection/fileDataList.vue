<template>
  <div class="file_data_list">
    <span class="switchView_button">
      <el-button
        type="primary"
        plain
        class="mb5"
        size="small"
        @click="scheduleList"
        >查看调度列表</el-button
      >
      <el-button size="small" type="primary" plain @click="switchView"
        ><span class="fa fa-bar-chart"></span> 查看概览</el-button
      >
    </span>
    <el-tabs v-model="activeName" @tab-click="handleClick">
      <el-tab-pane label="文件" name="first">
        <fileView ref="fileView" @fileDateChange="fileDateChange"></fileView>
      </el-tab-pane>
      <el-tab-pane label="清洗" name="second">
        <clearView ref="clearView" @fileDateChange="fileDateChange"></clearView>
      </el-tab-pane>
      <el-tab-pane label="资讯" name="third">
        <informationView ref="informationView" @fileDateChange="fileDateChange"></informationView>
      </el-tab-pane>
    </el-tabs>
    <el-dialog
      title="提示"
      :visible.sync="dialogVisible"
      width="80% !important"
      @closed="closed"
      center
    >
      <controlList v-if="ddControlList_show"></controlList>
    </el-dialog>
  </div>
</template>

<script>
import controlList from "./controlList.vue"
import fileView from "./fileView.vue";
import clearView from "./clearView.vue";
import informationView from "./informationView.vue";
export default {
  components: {
    fileView,
    clearView,
    informationView,
    controlList
  },
  data() {
    return {
      fileDate_: "",
      activeName: "first",
      dialogVisible:false,
      ddControlList_show:false,
    };
  },
  mounted(){
    // this.handleClick({label:"文件",name:"first"})
    this.$bus.$on('transition1',(data)=>{
      this.fileDate_ = data+'' || ''
      if(this.activeName == 'first'){
        this.$nextTick(()=>{
          if(this.$refs.fileView) this.$refs.fileView.init(this.fileDate_)
        })
      }else if(this.activeName == 'second'){
        this.$nextTick(()=>{
          if(this.$refs.clearView) this.$refs.clearView.init(this.fileDate_)
        })
      }else if(this.activeName == 'third'){
        this.$nextTick(()=>{
          if(this.$refs.informationView) this.$refs.informationView.init(this.fileDate_)
        })
      }
    })
  },
  methods: {
    switchView() {
      this.$emit("transition");
      this.$bus.$emit("transition2",this.fileDate_);
    },
    handleClick(data) {
      if(this.activeName == 'first'){
        this.$nextTick(()=>{
          this.$refs.fileView.init(this.fileDate_)
        })
      }else if(this.activeName == 'second'){
        this.$nextTick(()=>{
          this.$refs.clearView.init(this.fileDate_)
        })
      }else if(this.activeName == 'third'){
        this.$nextTick(()=>{
          this.$refs.informationView.init(this.fileDate_)
        })
      }
    },
    fileDateChange(data){
      // console.log('fileDateChange',data);
      this.fileDate_ = data+''
    },
    scheduleList(){
      this.dialogVisible = true;
      this.ddControlList_show = true;
    },
    closed(){
      this.ddControlList_show = false;
    }
  },
};
</script>

<style lang="scss">
.file_data_list {
  position: relative;
  .switchView_button {
    position: absolute;
    right: 0px;
    top: 0px;
    z-index: 999;
  }
}
</style>
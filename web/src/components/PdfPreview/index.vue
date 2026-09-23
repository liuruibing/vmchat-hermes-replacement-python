<template>
  <div class="pdf_preview">
    <!-- <pdf
			v-for="i in numPages"
			:key="i"
			:src="src"
			:page="i"
			style="display: block; width: 90%;margin: auto;margin-bottom:30px;border:1px solid #e7ecf1;"
		></pdf> -->
    <el-carousel :initial-index="initIndex" height="100%" :autoplay='false' arrow="always" :loop='false' @change="changechange" indicator-position="outside">
      <el-carousel-item height='100%' v-for="item in filelist" :key="item.id">
      <div style="overflow:hidden;text-align:center;">
        <span>{{item.name}}</span>
        <el-button style="float:right;" type="primary" size="small" plain icon="el-icon-download" @click="download(item.id)">下载</el-button>
      </div>
        <!-- <iframe :src='srcArr[item-1]' width='100%' height='100%' frameborder='0'> </iframe> -->
        <!-- <iframe :src='"/src/assets/pdf/web/viewer.html?file="+encodeURIComponent("http://vip.datadriver.com.cn:9600/pfom/api/file/v1.0/previewFile?id="+item.id+"&token="+token)' width='100%' height='100%' frameborder='0'> </iframe> -->
        <iframe :src='baseSrc+"/pdf/web/viewer.html?file="+encodeURIComponent(action+"?id="+item.id+"&token="+token)' width='100%' height='100%' frameborder='0'> </iframe>
        <!-- <iframe src='../../../src/assets/pdf/web/viewer.html' width='100%' height='100%' frameborder='0'> </iframe> -->
        <!-- <div class="item_pdf">
          <pdf
            v-for="i in numPages"
            :key="i"
            :src="urls[item-1]"
            :page="i"
            style="display: block; width: 90%;margin: auto;margin-bottom:30px;border:1px solid #e7ecf1;"
          ></pdf>
        </div> -->
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<script>
import $ from 'jquery'
import {FILE_URL} from '@/utils/request'
import commonApi from '@/api/common'
import commonFun from '@/filters/new_common'
// import pdf from 'vue-pdf'
export default {
  components:{},
  props:{
    urlArr:{},
    PreviewFileId:{},
  },
  // previewFile,downloadFile
  data(){
    return{
      baseUrl:FILE_URL,
      baseSrc:'static',
      i:0,
      url:'',
      urls:[],
      action:this.$store.state.setting.baseApi + 'api/file/v1.0/previewFile',
      numPages:null,
      token:encodeURIComponent(this.$store.getters.token),
      filelist:[],
      filelisturl:[],
      initIndex:0,
    }
  },
  mounted(){
    // this.aaa()
    // console.log(this.urlArr);
  },
  created(){
    if(process.env.NODE_ENV){
      if (process.env.NODE_ENV === "development") {
        // alert("开发环境");
        this.baseSrc = '/src/assets'
      }else {
        // alert("生产环境");
        this.baseSrc = 'static'
      }
    }
    // console.log(this.urlArr);
    let filelist = this.urlArr.filter(item=>{
      return item.id
    })
    let PreviewFileId = this.PreviewFileId;
    // console.log('PreviewFileId',PreviewFileId);
    this.filelist = filelist;
    let index = filelist.findIndex(v=>v.id==PreviewFileId);
    // console.log('index',index);
    if(index>=0){
      this.initIndex = index;
    }else{
      this.initIndex = 0;
    }
    this.changechange(this.initIndex);
    this.filelisturl = []
  },
  methods:{
    init(data){
      this.url = data;
    },
    download(id){
      let params = {}
      params.id = id;
      if(this.$store.getters.token){ params["token"] = this.$store.getters.token;}
      let action = this.$store.state.setting.baseApi + '/api/file/v1.0/downloadFile';
      commonFun.formDownloadFile(params,action,"GET");
      // commonApi.downloadFile(params).then(res=>{
      //   // console.log(res);
      //   if(res.data.message){
      //     this.$message({
      //       type:"error",
      //       message:res.data.message || '文件下载失败'
      //     })
      //   }
      // })
    },
    changechange(data){
      // console.log(data);
      let fileName = this.urlArr[data].name;
      // console.log(fileName);
      let arr = fileName.split('.');
      let fileType = arr[arr.length - 1];
      // console.log(fileType);
      let arr1 = ['pdf','docx','doc'];
      this.$notify.closeAll();
      if(!arr1.includes(fileType)){
        this.$notify({
          title: '提示',
          type: 'warning',
          message:`不支持.${fileType}格式文件的预览，请下载后查看！`,
          duration: 0,
          customClass:"yulantishi"
        });
          
      }
    }
  },

}
</script>

<style style lang='scss' rel="stylesheet/scss">
.pdf_preview{
  .item_pdf{
  height: 100% !important;
  overflow: hidden;
  overflow-y: scroll;
  }
  .el-carousel--horizontal{
    height: 100%;
  }
  .el-carousel__indicators{
    display: none;
  }
  .el-carousel__arrow{
    font-size: 30px;
    height: 40px;
    width: 40px;
  }
}
.yulantishi{
    top: 50% !important;
    right: 15% !important;
  }
</style>
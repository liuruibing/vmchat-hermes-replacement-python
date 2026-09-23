<template>
  <div style="height: 100%;width: 100%;">
    <el-row style="height: 100%;width: 100%;background-color: #fff;margin: 20px 10px;">
      <el-col class="articleDetails" style="height: 100%;width: 100%;">
        <el-row type="flex" justify="space-between" align="middle">
          <el-col :span="2" :class="isFirst?'not_click upperBox ':'upperBox pointer'">
            <span @click="changeArticle('pre')">< 上一篇</span>
          </el-col>
          <el-col :span="20" class="title">
            <span>{{ DetailData.title }}</span>
          </el-col>
          <el-col :span="2" :class="isLast?'not_click nextBox ':'nextBox pointer'">
            <span @click="changeArticle('next')">下一篇 ></span>
          </el-col>
        </el-row>
        <div class="line"></div>
        <div style="color:#999">
          <span>作者：{{ DetailData.author }}</span>
          <span style="padding-left:20px">发布日期：{{ DetailData.ndate }}</span>
          <!-- 文件保存到后端文件服务器上 -->
          <span style="float: right" v-if="DetailData.document"
                @click="previewFile(DetailData.document, DetailData.documentName,DetailData.fileExt)">
            <el-tooltip class="item" effect="dark" :content="`预览：${DetailData.documentName}`" placement="top">
              <svg-icon
                style="font-size: 30px;cursor: pointer"
                :iconClass="getSvgType(DetailData.document)"
                className="icon-style"
              ></svg-icon>
            </el-tooltip>
          </span>

          <!-- 文件保存到S3服务器上 -->
          <div style="float: right;">
<!--            <span  v-if="DetailData.uuid && DetailData.fileExt==='pdf'"
                   @click="previewS3Pdf(DetailData.uuid,DetailData.documentName,DetailData.fileExt)">
              <el-tooltip class="item" effect="dark" :content="'PDF预览'" placement="top">
                <svg-icon
                  style="font-size: 30px;cursor: pointer;color:#e9c5a5"
                  :iconClass="'clipboard'"
                  className="icon-style"
                ></svg-icon>
              </el-tooltip>
            </span>-->

            <!-- S3文件预览按钮 -->
            <span  v-if="DetailData.uuid"
                   @click="previewS3File(DetailData.uuid, DetailData.documentName, DetailData.fileExt)">
              <el-tooltip class="item" effect="dark" :content="`预览：${DetailData.documentName}`" placement="top">
                <svg-icon
                  style="font-size: 30px;cursor: pointer"
                  :iconClass="getFileExtType(DetailData.fileExt)"
                  className="icon-style"
                ></svg-icon>
              </el-tooltip>
            </span>
          </div>
        </div>
        <div  class="content ql-editor" v-html="DetailData.content" v-if="fileFlag=='1'"   style="height: calc(100% - 100px); width: 100%;">
        </div>
        <div class="video_box" v-if="fileFlag=='2'">
          <video :src="DetailData.video" class="videoStyle" controls="controls"></video>
        </div>
        <div class="" v-if="fileFlag === '3'" style="height: 100%; width: 100%;">
          <iframeModule :iframe-data="iframeData"/>
        </div>


      </el-col>
      <!--<el-col style="width:260px">
        <broad-side-list  :asideData1="asideData1" :asideData2="asideData2" :asideData3="asideData3"></broad-side-list>
      </el-col>-->
    </el-row>

    <!-- 文件预览模态框 -->
    <el-dialog
      :visible.sync="previewVisible"
      :title="previewTitle"
      :width="previewWidth"
      :fullscreen="isFullscreen"
      @close="handlePreviewClose"
      append-to-body
      style="width:100%"
    >
      <div class="preview-container">
        <div v-if="previewLoading" class="loading-container">
          <p>加载中，请稍候...</p>
        </div>

        <div v-if="!previewLoading">
          <!-- PDF预览 -->
          <div v-if="fileExt === 'pdf'">
            <iframe
              :src="previewFileUrl"
              style="z-index: 1000;height:650px;width:100%"
            ></iframe>
          </div>

          <!-- Word预览 -->
          <div v-else-if="fileExt === 'doc' || fileExt === 'docx'">
            <vue-office-docx
              :src="previewFileUrl"
              style="width: 100%; height: 650px"
              @rendered="handleDocxRendered"
              @error="handlePreviewError"
            />
          </div>

          <!-- PPT预览 -->
          <div v-else-if="fileExt === 'ppt' || fileExt === 'pptx'">
            <vue-office-pptx
              :src="previewFileUrl"
              style="width: 100%; height: 650px"
              @rendered="handlePptxRendered"
              @error="handlePreviewError"
            />
          </div>

          <div v-else class="unsupported-type standard-form">
            <p>抱歉，不支持该文件类型的预览 ({{ fileExt }})</p>
            <el-button size="small" type="primary" @click="downloadCurrentFile">下载文件</el-button>
          </div>
        </div>
      </div>

      <div slot="footer" class="dialog-footer">
        <el-button size="small" type="primary" @click="downloadCurrentFile">下载文件</el-button>
        <el-button size="small" plain type="info" @click="previewVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import commonApi from '@/api/common'
import fun from "@/filters/common";
import broadSideList from './broadsideList'
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'
import { selectArticle, replaceHtmlS3ImageSrcToBase64 } from './script/api'
import {downloadFile, getValueForArrayByKey} from "@/utils/commonUtil";
import iframeModule from '@/components/iframe'

// 引入预览组件
import VueOfficePptx from '@vue-office/pptx'
import VueOfficeDocx from '@vue-office/docx'
import '@vue-office/docx/lib/index.css'
import VueOfficePdf from '@vue-office/pdf'

export default {
  components: {
    broadSideList,
    iframeModule,
    VueOfficeDocx,
    VueOfficePptx,
    VueOfficePdf
  },
  data() {
    return {
      iframeData: {
        // iframe链接
        src: ''
      },
      DetailData: {},
      totalDataList: [],
      isFirst: false,
      isLast: false,
      isVideoFlag:false,
      isDocumentFlag:false,
      fileType: '1',
      fileFlag: '',
      fid: '',
      asideData1: {},
      asideData2: [],
      asideData3: [],
      // 预览相关变量（从代码1整合）
      previewVisible: false,
      previewFileUrl: '',
      previewTitle: '',
      previewLoading: false,
      fileExt: '',
      supportedType: true,
      previewWidth: '90%',
      isFullscreen: false,
      currentFileInfo: null,
      baseSrc:'static',
    }
  },
  created() {
    if(process.env.NODE_ENV){
      if (process.env.NODE_ENV === "development") {
        // alert("开发环境");
        this.baseSrc = '/src/assets'
      }else {
        // alert("生产环境");
        this.baseSrc = 'static'
      }
    }
  },
  mounted() {
    const query = this.$route.query;
    if (query.fid) {
      if (!this.$store.getters.fromPageJump) {
        this.getArticleDetailData(query.fid, query.type)
        this.fileType = query.type
        this.fileFlag = query.flag
        this.fid = query.fid
      }
    }

  },
  activated() {
    if (this.$store.getters.fromPageJump) {
      const query = this.$route.query;
      if (query.fid) {
        this.getArticleDetailData(query.fid, query.type)
        this.fileType = query.type
        this.fileFlag = query.flag
        this.fid = query.fid
      }
      this.$store.commit('SET_FROMPAGEJUMP', false)
    }

  },
  beforeDestroy(){
    if(this.isVideoFlag){
      URL.revokeObjectURL(this.DetailData.video);
      this.DetailData.video = null;
    }

    if(this.isDocumentFlag){
      URL.revokeObjectURL(this.DetailData.document);
      this.DetailData.document = null;
    }

    // 清理预览资源
    if (this.previewFileUrl && this.previewFileUrl.startsWith('blob:')) {
      URL.revokeObjectURL(this.previewFileUrl);
    }
  },
  watch: {},
  methods: {
    downloadFile,
    downloadS3File(uuid,fileName,fileExt){
      commonApi.manageS3SelectFile(uuid).then(res => {
        let blob = new Blob([res.data], { type: 'application/octet-stream' });
        let href = URL.createObjectURL(blob);
        let downloadElement = document.createElement('a');
        downloadElement.href = href;
        downloadElement.download = fileName+'.'+fileExt;
        document.body.appendChild(downloadElement);
        downloadElement.click();
        document.body.removeChild(downloadElement);
        URL.revokeObjectURL(href);


      })
    },
    previewS3Pdf(uuid,fileName,fileExt){
      commonApi.manageS3SelectFile(uuid).then(res => {
        let blob = new Blob([res.data], { type: 'application/pdf;charset=utf-8' });
        let href =URL.createObjectURL(blob);
        window.open(href, 'newWindow')
      })
    },
    htmlS3ImageSrcToBase64(resultData){
      const params = {content: resultData.content}
      replaceHtmlS3ImageSrcToBase64(params).then((res) => {
        const {status, data} = res.data
        if (status === 200) {
          resultData.content = data.htmlContent
        }
      })
    },
    getSvgType(val) {
      var index = val.lastIndexOf(".");
      var ext = val.substr(index + 1);
      if (ext === 'doc' || ext === 'docx') return "word"
      if (ext === 'ppt' || ext === 'pptx') return "ppt"
      if (ext === 'pdf') return "pdf_new"
      return ''
    },
    getFileExtType(val) {

      var ext = val
      if (ext === 'doc' || ext === 'docx') return 'word'
      if (ext === 'ppt' || ext === 'pptx') return 'ppt'
      if (ext === 'pdf') return 'pdf_new'
      return ''
    },
    getType(str) {
      if (str === '2') {
        return '5';
      }
      if (str === '0') {
        return '1'
      }
      if (str === '1') {
        return '3'
      }
      if (str === '3') {
        return '2'
      }
      return str
    },
    async getArticleDetailData(id, type, num = 0) {
      const params = {
        fid: id,
        type: type,
      }
      if (num === 0) {
        this.asideData1 = {}
        this.asideData2 = []
        this.asideData3 = []
      }
      const res = await selectArticle(params)
      try {
        if (res.data.status === 0) {
          const resultData = res.data.data.article || []
          this.fileFlag = resultData.flag
          if (num === 0) {
            const resultDataRightAndTop = res.data.data.rightTopArticles || []
            const resultDataRightMiddle = res.data.data.rightMiddleArticles || []
            const rightBottomArticles = res.data.data.rightBottomArticles || []
            resultDataRightAndTop.forEach(element => {
              element.img = getValueForArrayByKey(element.fileList, '2', 'fileType', 'fileUrl')
            })
            this.asideData1 = resultDataRightAndTop[0];
            this.asideData2 = resultDataRightMiddle.slice(0, 3);
            this.asideData3 = rightBottomArticles.slice(0, 3);
          }

          this.fileIdList = res.data.data.fids || []
          if (resultData.flag == '1') {
            // 图片文字类
            resultData.content = resultData.content.replace(new RegExp('<p>', 'g'), '<p style="display: inline-block">')
            //this.htmlS3ImageSrcToResizeBase64(resultData)
            this.htmlS3ImageSrcToBase64(resultData)
            const targetFile=this.isS3DocumentFile(resultData);
            if(targetFile) {
              this.isDocumentFlag=true;
              let blobUrl=  await commonApi.manageS3SelectFileVueBlob(targetFile.uuid)
              resultData.video=blobUrl
              resultData.uuid = getValueForArrayByKey(resultData.fileList, '6', 'fileType', 'uuid')
              resultData.fileExt = getValueForArrayByKey(resultData.fileList, '6', 'fileType', 'fileExt')
            }else {
              resultData.document = getValueForArrayByKey(resultData.fileList, '6', 'fileType', 'fileUrl')
              resultData.fileExt = getValueForArrayByKey(resultData.fileList, '6', 'fileType', 'fileExt')
            }
            resultData.documentName = getValueForArrayByKey(resultData.fileList, '6', 'fileType', 'fileName')
          } else if (resultData.flag == '2') {
            // 视频类
            //判断是否是S3文件保存
            const targetFile=this.isS3VideoFile(resultData);
            if(targetFile) {
              this.isVideoFlag=true;
              let blobUrl=  await commonApi.manageS3SelectFileVueBlob(targetFile.uuid)
              resultData.video=blobUrl
            }else{
              resultData.video = getValueForArrayByKey(resultData.fileList, '5', 'fileType', 'fileUrl')
            }

          } else if (resultData.flag == '3') {
            this.iframeData.src = resultData.content.replace(/<\/?[^>]+(>|$)/g, "")
          }

          if (Object.keys(resultData).length !== 0) {
            this.DetailData = resultData
          }
          this.checkFirstAndLastState()
        }
      } catch (e) {
        console.error('获取文章详情失败:', e);
      }
    },
    isS3VideoFile(element){
      if (!element.fileList) return;
      const targetFile = element.fileList.filter(file => file.fileType === '5').find(
        file => !file.fileUrl && file.uuid
      );
      return targetFile;

    },
    isS3DocumentFile(element){
      if (!element.fileList) return;
      const targetFile = element.fileList.filter(file => file.fileType === '6').find(
        file => !file.fileUrl && file.uuid
      );
      return targetFile;

    },
    checkFirstAndLastState() {
      let allLength = this.fileIdList.length
      if ((this.fileIdList.indexOf(this.fid) + 1) === allLength) {
        this.isFirst = false;
        this.isLast = true;
      } else if (this.fileIdList.indexOf(this.fid) === 0) {
        this.isFirst = true;
        this.isLast = false;
      } else {
        this.isFirst = false;
        this.isLast = false;
      }
    },
    // 获取研报数据
    getArticleDetailData3(id, type) {
      this.fileType = type === '0' ? '1' : type === '3' ? '1' : type
      commonApi.getDataBysqlCode({
        indexCode: '9869edb0-e8ab-4089-9bae-185fec8b9b8b',
        // narearType:type,//type代表页面不同部分
        fileType: this.getType(type),//1：文章，2：视频
        fid: id
      }).then(res => {
        const {status, data} = res.data
        if (status === 0) {
          data.forEach(element => {
            element.VC_NDATE = fun.timeFormat(element.VC_NDATE, 1);
            if (type == '1' || type == '0' || type == '3') {
              element.VC_NCONTENT = element.VC_NCONTENT.replace(new RegExp('<p>', 'g'), '<p>');
              // element.VC_NCONTENT = element.VC_NCONTENT.replace(new RegExp('<img', 'g'), '<img style="width: 500px;height: 330px;"');
            }
          })
          if (data.length) {
            this.DetailData = data[0]
          }
          this.totalDataList = [];
          this.getArticleData(1, type)

        }
      }).catch(() => {
      })
    },
    // 获取研报数据
    getArticleData(type, type1) {
      let param = this.fileType === '1' ? {
        indexCode: '9869edb0-e8ab-4089-9bae-185fec8b9b8b',
        narearType: type,//type代表页面不同部分
        fileType: type == 1 ? '2' : '3',//1：文章，2：视频
        flag: this.fileFlag
      } : {
        indexCode: '9869edb0-e8ab-4089-9bae-185fec8b9b8b',
        narearType: type,//type代表页面不同部分
        fileType: '5',//1：文章，2：视频
        flag: this.fileFlag
      }
      commonApi.getDataBysqlCode(param).then(res => {
        const {status, data} = res.data
        if (status === 0) {
          data.forEach(element => {
            element.VC_NDATE = fun.timeFormat(element.VC_NDATE, 1);
            if (type1 == '0' || type1 == '1' || type1 == '3') {
              element.VC_NCONTENT = element.VC_NCONTENT.replace(new RegExp('<p>', 'g'), '<p style="display: inline-block">');
              // element.VC_NCONTENT = element.VC_NCONTENT.replace(new RegExp('<img', 'g'), '<img style="width: 500px;height: 330px;"');
            }
          })
          this.totalDataList = this.totalDataList.concat(data)
          if (type == 1) {
            this.getArticleData(2, type1)
          } else if (type == 2) {
            let articleIndex = '';
            this.handlingData()
            this.totalDataList.forEach((element, elIndex) => {
              if (this.DetailData.F_ID == element.F_ID) {
                articleIndex = elIndex
              }
            });
            if (this.totalDataList.length > 1) {
              if (articleIndex == 0) {
                this.isFirst = true;
                this.isLast = false;
              } else if (articleIndex == this.totalDataList.length - 1) {
                this.isFirst = false;
                this.isLast = true;
              } else {
                this.isFirst = false;
                this.isLast = false;
              }
            } else {
              this.isFirst = true;
              this.isLast = true;
            }

          }
        }
      }).catch(() => {
      })
    },
    handlingData() {
      const arr = this.totalDataList;
      this.totalDataList = Array.from(new Set(arr.map(item => item.F_ID))).map(id => arr.find(item => item.F_ID === id));
    },
    //上一篇\下一篇
    changeArticle(type) {
      if (this.fileIdList.length > 1) {
        let articleIndex = '';
        this.fileIdList.forEach((element, elIndex) => {
          if (this.fid === element) {
            articleIndex = elIndex
          }
        });
        if (type == 'pre') {
          if (articleIndex > 0) {
            this.fid = this.fileIdList[articleIndex - 1]
            this.getArticleDetailData(this.fid, this.fileType, 1)
          }
        } else if (type === 'next') {
          if (articleIndex < this.fileIdList.length - 1) {
            this.fid = this.fileIdList[articleIndex + 1]
            this.getArticleDetailData(this.fid, this.fileType, 1)
          }
        }
      } else {
        this.isFirst = true;
        this.isLast = true;
      }
    },

    // 下载当前预览文件
    downloadCurrentFile() {
      if (!this.currentFileInfo) return;
      const { type, url, uuid, name, ext } = this.currentFileInfo;
      if (type === 'server' && url) {
        this.downloadFile(url, name);
      } else if (type === 's3' && uuid) {
        this.downloadS3File(uuid, name, ext);
      }
    },

    // 预览后端文件
    previewFile(fileUrl, fileName, fileExt) {
      console.log('预览服务器文件:', { fileUrl, fileName, fileExt });
      this.fileExt = fileExt.toLowerCase();
      this.previewTitle = fileName;
      this.previewLoading = true;
      this.previewVisible = true;
      this.currentFileInfo = { type: 'server', url: fileUrl, name: fileName };
      this.supportedType = ['pdf', 'doc', 'docx', 'ppt', 'pptx'].includes(this.fileExt);

      if (this.supportedType) {
        this.previewFileUrl = fileUrl;
        this.previewLoading = false;
      } else {
        this.previewLoading = false;
      }
    },

    // 预览S3文件
    previewS3File(uuid, fileName, fileExt) {
      console.log('预览S3文件:', { uuid, fileName, fileExt });
      this.fileExt = fileExt.toLowerCase();
      this.previewTitle = fileName;
      this.previewLoading = true;
      this.previewVisible = true;
      this.currentFileInfo = { type: 's3', uuid: uuid, name: fileName, ext: fileExt };
      this.supportedType = ['pdf', 'doc', 'docx', 'ppt', 'pptx'].includes(this.fileExt);

      if (this.supportedType) {
        commonApi.manageS3SelectFile(uuid)
          .then(res => {
            let blob = new Blob([res.data], { type: 'application/octet-stream' });
            if (!(blob instanceof Blob)) throw new Error('获取的不是有效的Blob对象');
            let blobUrl= URL.createObjectURL(blob);
            if(this.fileExt==='pdf'){
              this.previewFileUrl=this.baseSrc+"/pdf/web/viewer.html?file="+blobUrl
            }else {
              this.previewFileUrl = blobUrl;
            }
            this.previewLoading = false;
          })
          .catch(err => {
            console.error('获取文件失败', err);
            this.previewLoading = false;
            this.$message.error(`文件预览失败: ${err.message || '未知错误'}`);
          });
      } else {
        this.previewLoading = false;
      }
    },

    handleDocxRendered() { console.log('Word渲染完成'); },
    handlePptxRendered() { console.log('PPT渲染完成'); },
    handlePdfRendered() { console.log('PDF渲染完成'); },
    handlePreviewError(error) {
      console.error('文件预览错误:', error);
      this.$message.error(`预览失败: ${error.message || '无法加载文件'}`);
      this.previewLoading = false;
    },
    handlePreviewClose() {
      if (this.previewFileUrl && this.previewFileUrl.startsWith('blob:')) {
        URL.revokeObjectURL(this.previewFileUrl);
        this.previewFileUrl = '';
      }
      this.previewLoading = false;
      this.currentFileInfo = null;
      this.isFullscreen = false;
      this.previewWidth = '90%';
    }
  }
};
</script>

<style lang="scss" scoped>
.articleDetails {
  //margin: 20px 0;
  padding: 0 24px;

  .upperBox {
    text-align: left;
    font-size: 14px;
    // color: #999;
  }

  .not_click {
    color: #999;
  }

  .title {
    font-size: 18px;
    text-align: center;
    font-weight: bold;
  }

  .nextBox {
    text-align: right;
    font-size: 14px;
  }

  .line {
    border-top: 1px solid black;
    margin: 15px 0 20px;
  }

  .ellipsisOne {
    display: -webkit-box;
    overflow: hidden;
    white-space: normal !important;
    text-overflow: ellipsis;
    word-wrap: break-word;
    -webkit-line-clamp: 1;
    -webkit-box-orient: vertical;
  }

  .ellipsisThree {
    line-height: 30px;
    display: -webkit-box;
    overflow: hidden;
    white-space: normal !important;
    text-overflow: ellipsis;
    word-wrap: break-word;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
  }

  .pdr20 {
    padding-right: 20px;
  }

  .pdl20 {
    padding-left: 20px;

  }

  .content {
    font-size: 14px;
    //text-align: center;
  }

  .video_box {
    text-align: center;
  }

  .videoStyle {
    margin-top: 100px;
    width: 500px;
    height: 300px;
  }

  .ql-editor {
    p {
      font-size: 14px;
      //line-height: 30px;
      //margin: 0;
      //margin: 20px 0;
      //text-indent: 30px;
    }

    img {
      //width: 500px;
      //height: 330px;
    }
  }
}

// 预览相关样式（
::v-deep .el-dialog {
  width: 90% !important;
  margin-top: 5vh !important;
}
.preview-container {
  width: 100%;
  min-height: 700px;
  position: relative;
  overflow: hidden;
}
.loading-container {
  text-align: center;
  padding: 50px 0;
}
.unsupported-type {
  text-align: center;
  padding: 50px 0;
  p {
    margin-bottom: 20px;
    font-size: 16px;
  }
}
.dialog-footer {
  text-align: center;
}
</style>

<style lang="scss">
.articleDetails {
  .ql-editor {
    white-space: pre-line !important;
    line-height: 0;

    .ql-align-center {
      display: inline-block;
      width: 100% !important;
      text-align: center !important;
      font-size: 16px;
    }

    p {
      display: inline-block;
      width: 100%;
      line-height: 2;
      margin: 0;
      //margin: 20px 0;
      text-indent: 30px;
    }

    img {
      //width: 500px;
      //height: 330px;
      max-width: 100%;
     // height: 100%;

      object-position: left top;
      transition: 1s;
    }

    blockquote {
      border-left: 5px solid #ccc;
      padding-left: 15px
    }

    pre.ql-syntax {
      background-color: #23241f;
      color: #f8f8f2;
      overflow: visible;
      white-space: pre-wrap;
      margin-bottom: 5px;
      margin-top: 5px;
      padding: 5px 10px;
    }
  }
}

// 预览组件全局样式
.vue-office-docx, .vue-office-pptx, .vue-office-pdf {
  border: 1px solid #eee;
  border-radius: 4px;
}
.el-dialog__body {
  padding: 20px;
  max-height: calc(100vh - 150px);
  overflow: auto;
}
.vue-office-container {
  width: 100% !important;
  height: 100% !important;
}
</style>

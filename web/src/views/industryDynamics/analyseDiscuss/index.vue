<template>
  <div v-auto-enter class="analyse">
    <el-row>
      <el-col :span="24" class="analyseDiscuss">
        <!--        <div class="line"></div>-->
<!--        <el-row style="margin: 20px 0">
          <el-col :span="16">
            <span class="dashboard-title">&lt;!&ndash;最新{{ titleName }}&ndash;&gt;</span>
          </el-col>
          <el-col :span="8" style="text-align: right">
            <span class="toogle-tab">
&lt;!&ndash;              <span v-for="tab in hotProductArr" :key="tab.value" class="tab-item" :class="tab.value === isActive ? 'tab-item-active' : 'tab-item'" @click="handleButtonClick1(tab)">
                {{ tab.label }}
              </span>&ndash;&gt;
            </span>
            &lt;!&ndash;            <span&ndash;&gt;
            &lt;!&ndash;              v-for="(item, index) of hotProductArr"&ndash;&gt;
            &lt;!&ndash;              :key="index"&ndash;&gt;
            &lt;!&ndash;              :class="[&ndash;&gt;
            &lt;!&ndash;                index == 0 ? 'title-button-left' : '',&ndash;&gt;
            &lt;!&ndash;                index == hotProductArr.length - 1 ? 'title-button-right' : '',&ndash;&gt;
            &lt;!&ndash;                'title-button',&ndash;&gt;
            &lt;!&ndash;                'pointer',&ndash;&gt;
            &lt;!&ndash;                isActive === item.value ? 'button-active' : ''&ndash;&gt;
            &lt;!&ndash;              ]"&ndash;&gt;
            &lt;!&ndash;              @click="handleButtonClick1(item)"&ndash;&gt;
            &lt;!&ndash;            >&ndash;&gt;
            &lt;!&ndash;              {{ item.label }}&ndash;&gt;
            &lt;!&ndash;            </span>&ndash;&gt;
          </el-col>
        </el-row>-->

        <el-row>
          <el-col :span="13">
            <div style="height: 250px; width: 100%">
              <el-carousel height="100%" :autoplay="false" @change="changeCarousel" style="height: 100%; width: 100%; margin: auto">
                <el-carousel-item v-for="(item, index) in bannerInfoArr" :key="index">
                  <div class="video_icon_box" @click="toArticleDetails(item)" v-if="item.flag == '2'">
                    <i class="el-icon-video-play"></i>
                  </div>
                  <img class="pointer" alt="" @click="toArticleDetails(item)" :src="item.img" srcset="" style="width: 100%; height: 100%;object-fit: cover;" />
                  <div class="title11 pointer" @click="toArticleDetails(item)">{{ item.title }}</div>
                </el-carousel-item>
              </el-carousel>
            </div>
          </el-col>
          <el-col :span="11">
            <div class="articleBox pdl20">
              <div class="articlTile ellipsisOne activeColor pointer" @click="toArticleDetails(bannerInfoData)">
                {{ bannerInfoData.title }}
              </div>
              <div class="articldes">
                <span class="pdr20">{{ bannerInfoData.author }}</span>
                <span>{{ bannerInfoData.ndate }}</span>
              </div>
              <div class="articlContent">
                {{ bannerInfoData.summary }}
              </div>
            </div>
          </el-col>
        </el-row>

        <el-row style="margin-top: 10px">
          <el-col :span="24">
            <el-form ref="formQuery" :inline="true" :model="formQuery" class="standard-form">
              <el-form-item label="发布日期" prop="ndate">
                <el-date-picker
                  style="width: 225px"
                  v-model="formQuery.ndate"
                  value-format="yyyy-MM-dd"
                  type="daterange"
                  range-separator="-"
                  size="mini"
                  @change="changeDatePicker"
                  start-placeholder="开始日期"
                  end-placeholder="结束日期"
                ></el-date-picker>
              </el-form-item>
              <el-form-item label="报告附件">
                <el-select v-model="formQuery.isAnnex" style="width: 130px" placeholder="请选择" size="mini" clearable>
                  <el-option v-for="item in reportFileArr" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </el-select>
              </el-form-item>
              <el-form-item label="标题">
                <el-input style="width: 150px" v-model="formQuery.title" placeholder="请输入" size="mini" clearable />
              </el-form-item>
              <el-form-item label="作者">
                <el-input style="width: 150px" v-model="formQuery.author" placeholder="请输入" size="mini" clearable />
              </el-form-item>
              <el-form-item label="摘要">
                <el-input style="width: 150px" v-model="formQuery.summary" placeholder="请输入" size="mini" clearable />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" size="small" icon="el-icon-search" @click="queryArticleList">查询</el-button>
              </el-form-item>
            </el-form>
          </el-col>
        </el-row>

        <div class="line1"></div>
        <div ref="content">
          <el-carousel
            v-if="customTotal !== 0"
            indicator-position="none"
            :autoplay="false"
            arrow="always"
            :height="carouselHeight"
            @change="carouselChange"
            style="width: 100%; margin: auto"
          >
            <el-carousel-item v-for="cTotal in customTotal" :key="cTotal">
              <el-row
                v-for="(item, index) in listArr"
                :key="index"
                type="flex"
                justify="space-between"
                align="middle"
                :gutter="20"
                class="listBox"
              >
                <el-col style="width: calc(100% - 200px)">
                  <div class="articleBox">
                    <div class="articlTile ellipsisOne">
                      <span v-if="item.orderId" style="margin-right: 5px;">
                        <img src="./img/ZD.png" style="padding-bottom: 4px;" />
                      </span>
                      <span @click="toArticleDetails(item)" class="pointer">{{ item.title }}</span>
                      <!-- 文件保存到后端文件服务器上 -->
                      <span
                        v-if="item.document"
                        @click="previewFile(item.document, item.documentName, item.fileExt)"
                      >
                        <el-tooltip class="item" effect="dark" :content="`预览：${item.documentName}`" placement="top">
                          <svg-icon
                            style="font-size: 20px; cursor: pointer"
                            :iconClass="getSvgType(item.document)"
                            className="icon-style"
                          ></svg-icon>
                        </el-tooltip>
                      </span>
                      <!-- 文件保存到S3服务器上 -->
                      <span
                        v-if="item.uuid"
                        @click="previewS3File(item.uuid, item.documentName, item.fileExt)"
                      >
                        <el-tooltip class="item" effect="dark" :content="`预览：${item.documentName}`" placement="top">
                          <svg-icon
                            style="font-size: 20px; cursor: pointer"
                            :iconClass="getFileExtType(item.fileExt)"
                            className="icon-style"
                          ></svg-icon>
                        </el-tooltip>
                      </span>
                    </div>
                    <div class="articldes">
                      <span class="pdr20">{{ item.author }}</span>
                      <span class="pdr20">{{ item.ndate }}</span>
                      <span class="pdr20">{{ item.norgan }}</span>
                      <span class="pdr20" v-if="isActive === '3'">{{ item.articleAddress }}</span>
                    </div>
                    <div class="articlContent ellipsisThree">
                      {{ item.summary }}
                    </div>
                  </div>
                </el-col>
                <el-col style="width: 180px">
                  <div style="height: 100px; width: 100%; position: relative">
                    <div class="video_icon_box1" @click="toArticleDetails(item)" v-if="item.flag == '2'">
                      <i class="el-icon-video-play"></i>
                    </div>
                    <img v-if="item.img" alt="" :src="item.img" class="pointer" srcset="" style="width: 100%; height: 100%" @click="toArticleDetails(item)" />
                  </div>
                </el-col>
              </el-row>
            </el-carousel-item>
          </el-carousel>
        </div>
      </el-col>
    </el-row>

    <!-- 文件预览模态框 -->
    <el-dialog
      class="preview-dialog"
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

      <div slot="footer" class="dialog-footer standard-form">
        <el-button size="small" type="primary" @click="downloadCurrentFile">下载文件</el-button>
        <el-button size="small" plain type="info"  @click="previewVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import commonApi from '@/api/common'
import Pagination from '@/components/Pagination'
import broadSideList from './broadsideList'
import { selectArticle, selectArticleList } from './script/api'
import { downloadFile, getValueForArrayByKey } from '@/utils/commonUtil'
// 引入预览组件（复用代码2依赖）
import VueOfficePptx from '@vue-office/pptx'
import VueOfficeDocx from '@vue-office/docx'
import '@vue-office/docx/lib/index.css'
import VueOfficePdf from '@vue-office/pdf'

export default {
  components: {
    broadSideList,
    Pagination,
    // 注册预览组件
    VueOfficeDocx,
    VueOfficePptx,
    VueOfficePdf
  },
  data() {
    return {
      hotProductArr: [
        { label: '广发资讯', value: '2', titleName: '资讯' },

        { label: '私募观点', value: '3', titleName: '观点' }
      ],
      //  { label: '监管动态', value: '1', titleName: '动态' },备份
      titleName: '动态',
      typeOptions: [],
      norganList: [],
      reportFileArr: [{ dimNme: '有', dimCde: '1' }, { dimNme: '无', dimCde: '0' }],
      filePagesList: [
        { label: '1-9页', value: '1' },
        { label: '10-19页', value: '2' },
        { label: '20页以上', value: '3' }
      ],
      selectType: '1',
      selectTypeList: [
        { label: '标题', value: '1' },
        { label: '作者', value: '2' },
        { label: '摘要', value: '3' }
      ],
      isActive: '2',
      bannerInfoArr: [],
      bannerInfoData: {},
      listArr: [],
      customSize: 5,
      customTotal: 0,
      total: 0,
      formQuery: {
        isAnnex: '', // 是否有附件 1：是 0：否
        type: '2',
        ndate: [],
        ndateBegin: '',
        ndateEnd: '',
        ntypeDetail: '',
        norgan: '',
        title: '',
        author: '',
        summary: '',
        filePages: '',
        orderString: '',
        reportFile: '',
        pageSize: 8,
        pageNum: 0
      },
      asideData1: {},
      asideData2: [],
      asideData3: [],
      blobImages: [],
      // 预览相关变量
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
  mounted() {
    const query = this.$route.query
    if (query.fileType) {
      this.isActive = query.fileType
      this.formQuery.type = this.isActive
    }
    if (!this.$store.getters.fromPageJump) {
      this.getReportListOptions('0')
      this.getReportListOptions('1')
      this.queryArticleList(1)
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
  beforeDestroy() {
    this.destroyImages()
    // 清理预览资源
    if (this.previewFileUrl && this.previewFileUrl.startsWith('blob:')) {
      URL.revokeObjectURL(this.previewFileUrl)
    }
  },
  activated() {
    if (this.$store.getters.fromPageJump) {
      this.$store.commit('SET_FROMPAGEJUMP', false)
      const query = this.$route.query
      if (query.fileType) {
        if (query.fileType == 'yhzx') {
          query.fileType = '2'
        } else if (query.fileType == 'smgd') {
          query.fileType = '3'
        } else {
          query.fileType = '1'
        }
        this.isActive = query.fileType
        this.formQuery.type = this.isActive
      }
      this.getReportListOptions('0')
      this.getReportListOptions('1')
      this.queryArticleList(1)
    }
  },
  filters: {
    getNtypeDetail(val) {
      for (let i in this.typeOptions) {
        if (val === this.typeOptions[i].dimCde) {
          return this.typeOptions[i].dimNme
        }
      }
    },
    getNorgan(val) {
      for (let i in this.norganList) {
        if (val === this.norganList[i].dimCde) {
          return this.norganList[i].dimNme
        }
      }
    }
  },
  computed: {
    carouselHeight() {
      return (this.listArr.length * 105).toString() + 'px'
    }
  },
  methods: {
    carouselChange(val) {
      this.formQuery.pageNum = val
      this.queryArticleList()
    },
    downloadFile,
    // S3文件下载
    downloadS3File(uuid, fileName, fileExt) {
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
    getPageInfo(num) {
      if (num === 0) {
        if (this.formQuery.filePages === '1') {
          return '1'
        }
        if (this.formQuery.filePages === '2') {
          return '10'
        }
        if (this.formQuery.filePages === '3') {
          return '20'
        }
      }
      if (num === 1) {
        if (this.formQuery.filePages === '1') {
          return '9'
        }
        if (this.formQuery.filePages === '2') {
          return '19'
        }
        if (this.formQuery.filePages === '3') {
          return ''
        }
      }
    },
    async queryArticleList(num = 0) {
      const params = {
        // flag: this.isActive,
        limit: this.formQuery.pageSize,
        offset: this.formQuery.pageNum * this.formQuery.pageSize,
        // filePagesBegin: this.getPageInfo(0),
        // filePagesEnd: this.getPageInfo(1),
        ...this.formQuery
      }
      delete params.filePages
      delete params.pageNum
      delete params.pageSize
      delete params.ndate
      this.listArr = []
      if (num === 1) {
        this.asideData1 = {}
        this.asideData2 = []
        this.asideData3 = []
      }
      const res = await selectArticleList(params)
      try {
        if (res.data.status === 0) {
          const resultDataLeftAndTop = res.data.data.leftTopArticles || []
          const resultDataPage = res.data.data.page.rows || []
          if (num === 1) {
            const resultDataRightAndTop = res.data.data.rightTopArticles || []
            const resultDataRightMiddle = res.data.data.rightMiddleArticles || []
            const rightBottomArticles = res.data.data.rightBottomArticles || []
            await Promise.all([...resultDataRightAndTop.map(this.processElement)])
            this.asideData1 = resultDataRightAndTop[0]
            this.asideData2 = resultDataRightMiddle.slice(0, 3)
            this.asideData3 = rightBottomArticles.slice(0, 3)
          }
          await Promise.all([...resultDataLeftAndTop.map(this.processElement), ...resultDataPage.map(this.processElement)])
          /*  resultDataLeftAndTop.forEach((element) => {
             element.img = getValueForArrayByKey(element.fileList, '2', 'fileType', 'fileUrl')
           }) */

          resultDataPage.forEach(element => {
            //element.img = getValueForArrayByKey(element.fileList, '2', 'fileType', 'fileUrl')
            element.document = getValueForArrayByKey(element.fileList, '6', 'fileType', 'fileUrl')
            element.documentName = getValueForArrayByKey(element.fileList, '6', 'fileType', 'fileName')
            element.uuid= getValueForArrayByKey(element.fileList, '6', 'fileType', 'uuid')
            element.fileExt= getValueForArrayByKey(element.fileList, '6', 'fileType', 'fileExt')
            element.ntypeDetail = getValueForArrayByKey(this.typeOptions, element.ntypeDetail, 'dimCde', 'dimNme', '')
            element.norgan = getValueForArrayByKey(this.norganList, element.norgan, 'dimCde', 'dimNme', '')
          })

          this.bannerInfoArr = resultDataLeftAndTop
          if (this.bannerInfoArr.length) {
            this.bannerInfoData = this.bannerInfoArr[0]
          } else {
            this.bannerInfoData = {}
          }
          this.listArr = resultDataPage
          this.total = res.data.data.page.total
          this.setCustomSizeFun()
        } else {
          this.total = 0
        }
      } catch (e) {
        this.total = 0
      }
    },
    async processElement(element) {
      if (!element.fileList) return

      const targetFile = element.fileList.find(file => !file.fileUrl && file.uuid)

      if (targetFile) {
        let imageUrL = await commonApi.manageS3SelectFileVueBlob(targetFile.uuid)
        element.img = imageUrL
        this.blobImages.push(imageUrL)
      } else {
        element.img = getValueForArrayByKey(element.fileList, '2', 'fileType', 'fileUrl')
      }
    },

    getSvgType(val) {
      var index = val.lastIndexOf('.')
      var ext = val.substr(index + 1)
      if (ext === 'doc' || ext === 'docx') return 'word'
      if (ext === 'ppt' || ext === 'pptx') return 'ppt'
      if (ext === 'pdf') return 'pdf_new'
      return ''
    },
    getFileExtType(val) {

      var ext = val
      if (ext === 'doc' || ext === 'docx') return 'word'
      if (ext === 'ppt' || ext === 'pptx') return 'ppt'
      if (ext === 'pdf') return 'pdf_new'
      return ''
    },
    selectTypeChange() {
      this.formQuery.title = ''
      this.formQuery.author = ''
      this.formQuery.summary = ''
    },
    getReportListOptions(type) {
      let params = type === '0' ? 'NEWTYPEDETAIL' : 'NEWORGAN'
      commonApi.edimsDdiaCommon(params).then(res => {
        if (res.data.status === 0) {
          if (type === '0') {
            this.typeOptions = res.data.data
          } else {
            this.norganList = res.data.data
          }
        }
      })
    },
    changeDatePicker(val) {
      if (val) {
        this.formQuery.ndateBegin = val[0]
        this.formQuery.ndateEnd = val[1]
      } else {
        this.formQuery.ndateBegin = ''
        this.formQuery.ndateEnd = ''
      }
    },
    pagination(val) {
      const { page, limit } = val
      this.formQuery.pageNum = page
      this.formQuery.pageSize = limit
      this.queryArticleList()
    },
    setCustomSizeFun() {
      if (this.total === 0) return
      this.customTotal = Math.ceil(this.total / this.formQuery.pageSize)
    },
    handleButtonClick1(item) {
      this.isActive = item.value
      this.titleName = item.titleName
      this.formQuery.type = this.isActive
      this.queryArticleList()
    },
    changeCarousel(index) {
      this.bannerInfoData = this.bannerInfoArr[index]
    },
    async toArticleDetails(data) {
      // 如果是公众号类型
      if (data.flag == '3') {
        const params = {
          fid: data.fid,
          type: this.isActive
        }
        await selectArticle(params).then(res => {
          if (res.data.status === 0) {
            const resultData = res.data.data.article || ''
            let url = resultData.content.replace(/<\/?[^>]+(>|$)/g, '')
            window.open(url)
          } else {
            this.$message.closeAll()
            this.$message.warning('公众号地址不存在，跳转失败')
          }
        })
        return
      }
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/hydt/articleDetails',
        query: {
          fid: data.fid,
          type: this.isActive,
          flag: data.flag
        }
      })
    },
    async destroyImages() {
      this.blobImages.forEach(url => {
        if (url) URL.revokeObjectURL(url)
      })
      this.blobImages = []
    },

    // 下载当前预览文件
    downloadCurrentFile() {
      if (!this.currentFileInfo) return
      const { type, url, uuid, name, ext } = this.currentFileInfo
      if (type === 'server' && url) {
        this.downloadFile(url, name)
      } else if (type === 's3' && uuid) {
        this.downloadS3File(uuid, name, ext)
      }
    },

    // 预览后端文件
    previewFile(fileUrl, fileName, fileExt) {
      this.fileExt = fileExt.toLowerCase()
      this.previewTitle = fileName
      this.previewLoading = true
      this.previewVisible = true
      this.currentFileInfo = { type: 'server', url: fileUrl, name: fileName }
      this.supportedType = ['pdf', 'doc', 'docx', 'ppt', 'pptx'].includes(this.fileExt)

      if (this.supportedType) {
        this.previewFileUrl = fileUrl
        this.previewLoading = false
      } else {
        this.previewLoading = false
      }
    },

    // 预览S3文件
    previewS3File(uuid, fileName, fileExt) {
      this.fileExt = fileExt.toLowerCase()
      this.previewTitle = fileName
      this.previewLoading = true
      this.previewVisible = true
      this.currentFileInfo = { type: 's3', uuid: uuid, name: fileName, ext: fileExt }
      this.supportedType = ['pdf', 'doc', 'docx', 'ppt', 'pptx'].includes(this.fileExt)

      if (this.supportedType) {
        commonApi.manageS3SelectFile(uuid)
          .then(res => {
            let blob = new Blob([res.data], { type: 'application/octet-stream' })
            if (!(blob instanceof Blob)) throw new Error('获取的不是有效的Blob对象')
            let blobUrl= URL.createObjectURL(blob);
            if(this.fileExt==='pdf'){
              this.previewFileUrl=this.baseSrc+"/pdf/web/viewer.html?file="+blobUrl
            }else {
              this.previewFileUrl = blobUrl;
            }
            this.previewLoading = false
          })
          .catch(err => {
            console.error('获取文件失败', err)
            this.previewLoading = false
            this.$message.error(`文件预览失败: ${err.message || '未知错误'}`)
          })
      } else {
        this.previewLoading = false
      }
    },

    handleDocxRendered() { console.log('Word渲染完成') },
    handlePptxRendered() { console.log('PPT渲染完成') },
    handlePreviewError(error) {
      console.error('文件预览错误:', error)
      this.$message.error(`预览失败: ${error.message || '无法加载文件'}`)
      this.previewLoading = false
    },
    handlePreviewClose() {
      if (this.previewFileUrl && this.previewFileUrl.startsWith('blob:')) {
        URL.revokeObjectURL(this.previewFileUrl)
        this.previewFileUrl = ''
      }
      this.previewLoading = false
      this.currentFileInfo = null
      this.isFullscreen = false
      this.previewWidth = '90%'
    }
  }
}
</script>
<style lang="scss" scoped>
// 预览相关样式（
::v-deep .el-dialog {
  width: 90% !important;
  margin-top: 5vh !important;
}
::v-deep .dialog-footer {
  text-align: center !important;  // 按钮居中
}
</style>
<style lang="scss">

.analyse {
  margin: 20px 10px;
  height: 100%;
  background-color: #fff;
}
.analyseDiscuss {
  padding: 0 20px;
  .tab-item-active {
    cursor: pointer;
    background-image: linear-gradient(to right, #f5d7bc, #e0b794) !important;
    color: #612d10;
    border: none!important;
  }
  .tab-item {
    cursor: pointer;
    background-color: #fcf8f4!important;
    border-color: #804f2b!important;
    color: #612d10
  }

  .pointer {
    cursor: pointer;
  }

  .video_icon_box {
    width: 70px;
    height: 70px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);

    .el-icon-video-play {
      font-size: 70px;
      color: #e3e3e3;
      cursor: pointer;
    }
  }

  .video_icon_box1 {
    width: 40px;
    height: 40px;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);

    .el-icon-video-play {
      font-size: 40px;
      color: #e3e3e3;
      cursor: pointer;
    }
  }

  .el-carousel__indicators--horizontal {
    // width: 200px;
    text-align: right;
    padding-right: 15px;
    right: 0%;
    transform: translateX(0%);
    -webkit-transform: translateX(0%);
    // background-color: black;
    // background-color: rgba($color: red, $alpha: 0.4);
    // opacity: 0.4;
  }

  .el-carousel__container {
     //height: 100%;
  }

  .el-carousel__indicator--horizontal {
    padding: 18px 7px;
  }

  .el-carousel__button {
    width: 8px;
    height: 8px;
    border-radius: 50%;
  }

  .title11 {
    // width: calc(100% - 200px);
    width: 100%;
    position: absolute;
    bottom: 0px;
    color: #fff;
    font-size: 14px;
    height: 44px;
    line-height: 44px;
    padding-left: 20px;
    background-color: rgba($color: #000000, $alpha: 0.4);
  }

  .line {
    border-top: 1px solid black;
  }

  .line1 {
    border-top: 1px solid #ebeef5;
  }

  .dashboard-title {
    font-size: 16px;
    // font-weight: 600;
    margin-right: 8px;
  }

  .title-button {
    display: inline-block;
    border: 1px solid #356385;
    // width: 70px;
    height: 22px;
    line-height: 20px;
    font-size: 14px;
    text-align: center;
    border-right: none;
    padding: 0 15px;
  }

  .title-button-left {
    -webkit-border-radius: 40px 0px 0px 40px;
    -moz-border-radius: 40px 0px 0px 40px;
    border-radius: 40px 0px 0px 40px;
  }

  .title-button-right {
    border-right: 1px solid #356385;
    -webkit-border-radius: 0px 40px 40px 0px;
    -moz-border-radius: 0px 40px 40px 0px;
    border-radius: 0px 40px 40px 0px;
  }

  .button-active {
    background-color: #6b8da6;
    color: white;
  }

  .item-active {
    color: #005ba1;
  }

  .articleBox {
    font-size: 14px;

    .articlTile {
      margin: 10px 0 10px;
      font-size: 16px;
      height: 30px;
      line-height: 30px;
      font-weight: bold;
    }

    .activeColor {
      color: #cf7e34;
      font-size: 18px;
    }

    .articldes {
      text-align: left;
      height: 20px;
    }

    .articlContent {
      line-height: 30px;
      -webkit-line-clamp: 6;
      display: -webkit-box;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
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
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    display: block;
    //display: -webkit-box;
    //overflow: hidden;
    //white-space: normal !important;
    //text-overflow: ellipsis;
    //word-wrap: break-word;
    //-webkit-line-clamp: 3;
    //-webkit-box-orient: vertical;
  }

  .pdr20 {
    padding-right: 20px;
  }

  .pdl20 {
    padding-left: 20px;
  }

  .listBox {
    border-bottom: 1px solid #ebeef5;
    //padding: 15px 0 15px;
  }

  .content-box {
    height: calc(100vh - 450px);
    overflow: auto;
    overflow-x: hidden;

    .el-carousel__item.is-active {
      height: 100%;
      overflow: auto;
      overflow-x: hidden;
    }
  }
  ::v-deep .standard-form .el-form-item label{
    color: #333333;
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

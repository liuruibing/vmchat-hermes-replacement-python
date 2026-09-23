<template>
  <div class="detail-dialog">
    <el-form
      ref="formEditQuery"
      :inline="true"
      :rules="rules"
      :model="formEditQuery"
      class="reportForm "
      label-width="130px">
      <el-row>
        <el-col :span="12">
          <el-form-item label="文章展示区域" prop="arearType">
            <el-select v-model="formEditQuery.arearType" placeholder="请选择" size="small" clearable>
              <el-option
                v-for="item in arearOptions"
                :key="item.DIM_CDE"
                :label="item.DIM_NME"
                :value="item.DIM_CDE"
              />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col>
          <el-form-item label="作者" prop="author">
            <el-input v-model="formEditQuery.author" placeholder="请输入" size="small"/>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row v-if="['2'].indexOf(formEditQuery.arearType)!== -1">
        <el-col :span="24">
          <el-form-item label="置顶显示">
            <el-switch v-model="formEditQuery.topShow"></el-switch>
          </el-form-item>
          <el-form-item label="排序" v-show="formEditQuery.topShow">
            <el-input-number v-model.number="formEditQuery.orderId" placeholder="请输入" size="small" style="width:160px;"
                             :min="1"/>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">
          <el-form-item label="文章类型" prop="flag">
            <el-radio-group
              v-model="formEditQuery.flag"
              :disabled="dialogStatus === 'EDIT'"
              @change="changeFlag">
              <template v-for="(item,index) in flagList">
                <el-radio :label="item.DIM_CDE" :key="index">{{ item.DIM_NME }}</el-radio>
              </template>
            </el-radio-group>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
<!--        <el-col :span="12">
          <el-form-item label="资讯类型" prop="type">
            <el-select v-model="formEditQuery.type" placeholder="请选择" size="small" clearable>
              <el-option
                v-for="item in zxType"
                :key="item.DIM_CDE"
                :label="item.DIM_NME"
                :value="item.DIM_CDE"
              />
            </el-select>
          </el-form-item>
        </el-col>-->
        <el-col :span="24">
          <el-form-item label="所属机构" prop="norgan">
            <el-select v-model="formEditQuery.norgan" placeholder="请选择" size="small" clearable>
              <el-option
                v-for="item in norganList"
                :key="item.dimCde"
                :label="item.dimNme"
                :value="item.dimCde"
              />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">
          <el-form-item label="启用状态">
            <el-switch v-model="status" @change="(e)=>switchChange(e,1)"></el-switch>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24" class="pic">
          <el-form-item label="首页展示">
            <el-switch v-model="isHdleft" @change="(e)=>switchChange(e,2)"></el-switch>
          </el-form-item>
          <span class="notes " style="line-height:5px;">备注：开启则展示在首页</span>
        </el-col>
      </el-row>
      <el-row v-if="formEditQuery.arearType==='2' && formEditQuery.flag === '1'">
        <el-col :span="24">
          <el-form-item label="上传报告">
            <el-upload
              :file-list="fileList2"
              :before-remove="() => {beforeRemove('report')}"
              :limit="1"
              :accept="'doc,docx,ppt,pptx,pdf'"
              :http-request="(e)=>{httpRequest(e,5)}"
              class=""
              action="#">
              <el-button size="small" type="primary">点击上传</el-button>
              <div slot="tip" class="el-upload__tip">只能上传 pdf/word/ppt 文件</div>
            </el-upload>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <template>
          <template v-if="formEditQuery.flag === '2'">
            <el-col :span="20" class="pic">
              <el-form-item label="视频封面" prop="videoCover">
                <el-upload
                  :show-file-list="false"
                  :http-request="(e)=>{httpRequest(e,2)}"
                  @on-remove="handleVideoCoverRemove"
                  class="avatar-uploader"
                  action="#">
                  <span v-if="videoCover" class="avatar">
                    <el-image
                      :src="videoCover"
                      style="width: 100px; height: 100px"
                      fit="cover"></el-image>
                    <i class="el-icon-close icon-img" @click.stop="deleteImg(2)"/>
                  </span>
                  <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                </el-upload>
              </el-form-item>
              <span class="notes">备注：上传尺寸建议：长：宽=3:1	</span>
            </el-col>
          </template>
          <template v-else>
            <el-col :span="20" class="pic">
              <el-form-item label="摘要图片" prop="pic2">
                <el-upload
                  :show-file-list="false"
                  :http-request="(e)=>{httpRequest(e,4)}"
                  @on-remove="handlePic2Remove"
                  class="avatar-uploader"
                  action="#">
                  <span v-if="pic2" class="avatar">
                    <el-image
                      :src="pic2"
                      style="width: 100px; height: 100px"
                      fit="cover"></el-image>
                    <i class="el-icon-close icon-img" @click.stop="deleteImg(4)"/>
                  </span>
                  <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                </el-upload>
              </el-form-item>
              <span class="notes">备注：上传尺寸建议：长：宽=3:1</span>
            </el-col>
          </template>
        </template>
      </el-row>

      <el-row>
        <el-col :span="24">
          <el-form-item label="标题" prop="title" class="over-term">
            <el-input
              v-model="formEditQuery.title"
              placeholder="请输入"
              show-word-limit
              maxlength="50"
              size="small"
              style="width: 60%"/>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="24">
          <el-form-item label="摘要" prop="summary" class="over-term">
            <el-input
              v-model="formEditQuery.summary"
              :rows="2"
              placeholder="请输入"
              show-word-limit
              maxlength="500"
              type="textarea"
              size="small"/>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row v-if="formEditQuery.flag === '3'">
        <el-col :span="24">
          <el-form-item label="文章地址" prop="content" class="over-term">
            <el-input
              v-model="formEditQuery.content"
              placeholder="请输入"
              size="small"
              style="width: 60%"/>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <template v-if="formEditQuery.flag === '2'">
          <el-col>
            <el-form-item label="上传视频" prop="video">
              <el-upload
                :file-list="fileList"
                :before-remove="() => {beforeRemove('video')}"
                :limit="1"
                :accept="'video/*'"
                :http-request="(e)=>{httpRequest(e,3)}"
                class=""
                action="#">
                <el-button size="small" type="primary">点击上传</el-button>
                <div slot="tip" class="el-upload__tip">只能上传视频文件</div>
              </el-upload>
            </el-form-item>
          </el-col>
        </template>
        <template v-if="formEditQuery.flag === '1'">
          <el-col>
            <el-form-item label="内容" prop="content">
              <div class="vue-quill-editor">
                <quill-editor
                  v-maxWindow
                  ref="myQuillEditor"
                  v-model="formEditQuery.content"
                  :options="editorOption"

                />
              </div>
            </el-form-item>
          </el-col>
        </template>
      </el-row>
    </el-form>
    <span slot="footer">
      <el-row :gutter="20">
        <el-col :span="16" :offset="11">
          <el-button
            :loading="saveLoading"
            type="primary"
            size="small"
            @click="handleSaveFund('formEditQuery')">提 交</el-button>
        </el-col>
      </el-row>
    </span>
    <el-upload
      :show-file-list="false"
      :http-request="(e)=>{httpRequest(e,6)}"
      style="display: none"
      drag
      class="quill-upload"
      action="#">
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">
        将文件拖到此处，或
        <em>点击上传</em>
      </div>
    </el-upload>
  </div>
</template>
<script>
// 设置字体大小
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'
import {getValueForArrayByKey} from '@/utils/commonUtil'
import {Quill, quillEditor} from 'vue-quill-editor'
import {AREAR_TYPE, FLAG_TYPE, ZX_TYPE} from '../script/constant'
import commonApi from '@/api/common'
import moment from 'moment'
import {ImageDrop} from 'quill-image-drop-module'
import ImageResize from 'quill-image-resize-module'
import lodash from 'lodash'
import {replaceHtmlS3ImageSrcToBase64,saveReport} from '../script/api'


const fontSizeStyle = Quill.import('attributors/style/size') // 引入这个后会把样式写在style上
fontSizeStyle.whitelist = ['12px', '14px', '16px', '18px', '20px', '24px', '28px', '32px', '36px']
Quill.register(fontSizeStyle, true)
Quill.register('modules/imageDrop', ImageDrop)
Quill.register('modules/imageResize', ImageResize)
// 设置字体样式
const Font = Quill.import('attributors/style/font') // 引入这个后会把样式写在style上
const fonts = [
  'SimSun',
  'SimHei',
  'Microsoft-YaHei',
  'KaiTi',
  'FangSong'
]
Font.whitelist = fonts // 将字体加入到白名单
Quill.register(Font, true)
// 工具栏
const toolbarOptions = [
  ['bold', 'italic', 'underline', 'strike'], // 加粗 斜体 下划线 删除线 -----['bold', 'italic', 'underline', 'strike']
  [{color: []}, {background: []}], // 字体颜色、字体背景颜色-----[{ color: [] }, { background: [] }]
  [{align: []}], // 对齐方式-----[{ align: [] }]
  [{size: fontSizeStyle.whitelist}], // 字体大小-----[{ size: ['small', false, 'large', 'huge'] }]
  [{font: fonts}], // 字体种类-----[{ font: [] }]
  [{header: [1, 2, 3, 4, 5, 6, false]}], // 标题
  // [{direction: 'ltl'}], // 文本方向-----[{'direction': 'rtl'}]
  [{direction: 'rtl'}], // 文本方向-----[{'direction': 'rtl'}]
  [{indent: '-1'}, {indent: '+1'}], // 缩进-----[{ indent: '-1' }, { indent: '+1' }]
  [{list: 'ordered'}, {list: 'bullet'}], // 有序、无序列表-----[{ list: 'ordered' }, { list: 'bullet' }]
  [{script: 'sub'}, {script: 'super'}], // 上标/下标-----[{ script: 'sub' }, { script: 'super' }]
  ['blockquote', 'code-block'], // 引用  代码块-----['blockquote', 'code-block']
  ['image'], // 链接、图片、视频-----['link', 'image', 'video']
  ['clean'] // 清除文本格式-----['clean']

]

/* 富文本编辑图片上传配置*/
const uploadConfig = {
  action: '/api/article/manage/upload', // 必填参数 图片上传地址
  methods: 'POST', // 必填参数 图片上传方式
  token: '', // 可选参数 如果需要token验证，假设你的token有存放在sessionStorage
  name: 'img', // 必填参数 文件的参数名
  size: 51200, // 可选参数   图片大小，单位为Kb, 1M = 1024Kb  限制 50M
  accept: 'image/png, image/gif, image/jpeg, image/bmp, image/x-icon' // 可选 可上传的图片格式
}

const handlers = {
  imageBase64: function imageBase64() {
    var self = this

    var fileInput = this.container.querySelector('input.ql-image[type=file]')
    if (fileInput === null) {
      fileInput = document.createElement('input')
      fileInput.setAttribute('type', 'file')
      // 设置图片参数名
      if (uploadConfig.name) {
        fileInput.setAttribute('name', uploadConfig.name)
      }
      // 可设置上传图片的格式
      fileInput.setAttribute('accept', uploadConfig.accept)
      fileInput.classList.add('ql-image')
      // 监听选择文件
      fileInput.addEventListener('change', function () {
        const file = fileInput.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = (e) => {
            const base64 = e.target.result;
            const length = self.quill.getSelection(true).index
            self.quill.insertEmbed(length, 'image', base64, Quill.sources.USER);
            self.quill.setSelection(length + 1)
          };
          reader.readAsDataURL(file);
        }

        // xhr.open(uploadConfig.methods, uploadConfig.action, true)
        // // 上传数据成功，会触发
        // xhr.onload = function (e) {
        //   if (xhr.status === 200) {
        //     var res = JSON.parse(xhr.responseText)
        //     const length = self.quill.getSelection(true).index
        //     // console.log(res, 'res')
        //     // 这里很重要，你图片上传成功后，img的src需要在这里添加，res.path就是你服务器返回的图片链接。
        //     self.quill.insertEmbed(length, 'image', res.path)
        //     self.quill.setSelection(length + 1)
        //   }
        //   fileInput.value = ''
        // }
        // 开始上传数据
        // xhr.upload.onloadstart = function (e) {
        //   fileInput.value = ''
        // }
        // // 当发生网络异常的时候会触发，如果上传数据的过程还未结束
        // xhr.upload.onerror = function (e) {
        // }
        // // 上传数据完成（成功或者失败）时会触发
        // xhr.upload.onloadend = function (e) {
        //   // console.log('上传结束')
        // }
        // xhr.send(formData)
      })
      this.container.appendChild(fileInput)
    }
    fileInput.click()
  },
  image: function image() {
    var self = this

    var fileInput = this.container.querySelector('input.ql-image[type=file]')
    if (fileInput === null) {
      fileInput = document.createElement('input')
      fileInput.setAttribute('type', 'file')
      // 设置图片参数名
      if (uploadConfig.name) {
        fileInput.setAttribute('name', uploadConfig.name)
      }
      // 可设置上传图片的格式
      fileInput.setAttribute('accept', uploadConfig.accept)
      fileInput.classList.add('ql-image')
      // 监听选择文件
      fileInput.addEventListener('change', function () {
        // 创建formData
        var formData = new FormData()
        formData.append(uploadConfig.name, fileInput.files[0])
        formData.append('object', 'product')
        // 如果需要token且存在token
        if (uploadConfig.token) {
          formData.append('token', uploadConfig.token)
        }
        // 图片上传
        var xhr = new XMLHttpRequest()
        xhr.open(uploadConfig.methods, uploadConfig.action, true)
        // 上传数据成功，会触发
        xhr.onload = function (e) {
          if (xhr.status === 200) {
            var res = JSON.parse(xhr.responseText)
            const length = self.quill.getSelection(true).index
           // console.log(res, 'res')
            // 这里很重要，你图片上传成功后，img的src需要在这里添加，res.path就是你服务器返回的图片链接。
            self.quill.insertEmbed(length, 'image', res.path)
            self.quill.setSelection(length + 1)
          }
          fileInput.value = ''
        }
        // 开始上传数据
        xhr.upload.onloadstart = function (e) {
          fileInput.value = ''
        }
        // 当发生网络异常的时候会触发，如果上传数据的过程还未结束
        xhr.upload.onerror = function (e) {
        }
        // 上传数据完成（成功或者失败）时会触发
        xhr.upload.onloadend = function (e) {
          // console.log('上传结束')
        }
        xhr.send(formData)
      })
      this.container.appendChild(fileInput)
    }
    fileInput.click()
  }
}

export default {
  name: 'ProductEdit',
  components: {quillEditor},
  props: {
    currentRow: {
      type: Object,
      default: () => {
      }
    },
    typeList: {
      type: Array,
      default: []
    },
    norganList: {
      type: Array,
      default: []
    },
    dialogStatus: {
      type: String,
      default: 'ADD'
    }
  },
  data() {
    return {
      formEditQuery: {
        fileIds: [], //需要删除的数组对象
        type: '2',
        flag: '1', // 文章类型 ---
        arearType: '',
        author: '',
        orderId: '',
        status: '0',
        title: '',
        // articleAddress:'',
        ndate: '',
        pic1: '',
        pic2: '',
        uuid:'',
        // pic3: '',
        videoCover: '',
        attachedFile: '',
        isHdleft: '0', // 首页展示
        // filePages: '0',
        source: '',
        summary: '',
        // ntypeDetail: '',
        norgan: '',
        video: '',
        content: '', // 文本内容 、 文章地址

        // topOrderId:'',
        topShow: false// true  orderId 为1， false 为0
      },
      listImg: '',
      flagList: FLAG_TYPE,
      arearOptions: AREAR_TYPE,
      zxType: ZX_TYPE,
      organList: [
        {dimCde: '1', dimNme: '广发证券'}
      ],
      rules: {
        type: [{required: true, message: '请选择研报类型', trigger: 'change'}],
        flag: [{required: true, message: '请选择文章类型', trigger: 'change'}],
        arearType: [{required: true, message: '请选择文章展示区域', trigger: 'change'}],
        author: [{required: true, message: '请输入作者姓名', trigger: 'change'}],
        title: [{required: true, message: '请输入研报标题', trigger: 'change'}],
        ntypeDetail: [{required: true, message: '请选择研报类型', trigger: 'change'}],
        norgan: [{required: true, message: '请选择所属机构', trigger: 'change'}],
        summary: [{required: true, message: '请输入研报摘要', trigger: 'change'}],
        content: [{required: true, message: '请输入内容', trigger: 'change'}],
        video: [{required: true, message: '请上传视频', trigger: 'change'}],
        orderId: [{required: true, message: '请设置排序顺序', trigger: 'change'},
          {pattern: /^[0-9]*$/, message: '排序只能为数字', trigger: 'blur'}],
        topOrderId: [{required: false, message: '请设置排序顺序', trigger: 'change'},
          {pattern: /^[0-9]*$/, message: '排序只能为数字', trigger: 'blur'}]
      },
      searchRules: {},
      letterTypeArr: [],
      html: this.value,
      editorOption: {
        modules: {
          imageDrop: true, // 图片拖拽
          imageResize: { // 放大缩小
            displayStyles: {
              backgroundColor: 'black',
              border: 'none',
              color: 'white'
            },
            modules: ['Resize', 'DisplaySize', 'Toolbar']
          },
          toolbar: {
            container: toolbarOptions,
            handlers: {
              // 重写点击组件上的图片按钮要执行的代码,图片返回base64 编码
              'imageBase64': function (value) {
                document.querySelector('.quill-upload .el-icon-upload').click()
              }
            }
          }
        }
      },
      pic1: '',
      pic1Config: {},
      pic2: '',
      pic2Config: {},
      uuid:'',
      // pic3: '',
      disabled: false,
      status: false,
      isHdleft: false,
      videoCover: '',
      videoCoverConfig:{},
      fileList: [],
      fileListConfig: {},
      fileList2: [],
      fileList2Config: {},
      deletcType: 1,
      saveLoading: false

    }
  },
  watch: {
    detailInfo: {
      handler(value) {
        this.formQuery.letterType = value.letterType
        this.formQuery.commName = value.commName
        this.formQuery.content = value.content
      },
      deep: true
    },
    dialogVisible: {
      handler(value) {
        this.isShow = value
      }
    },
    currentRow: {
      handler(value) {
        if (value && value.fid) {
          this.dealRowValue(value)
        }
      },
      deep: true,
      immediate: true,
    },
    'formEditQuery.arearType'(val) {
      if (val === '0') {
        this.formEditQuery.flag = '1'
        this.formEditQuery.isHdleft = '0'
        this.isHdleft = false
      }
      if (val === '3' || val === '4' || val === '5') {
        this.formEditQuery.flag = '1'
      }
    }
  },
  mounted() {
    // this.getReportListOptions()
    // this.dealRowValue(this.currentRow)
    if(this.pic2Config.uuid){
      commonApi.manageS3SelectFile(this.pic2Config.uuid).then(res=>{

        let blob = new Blob ([res.data],{type:'application/octet-stream'})
        this.pic2=URL.createObjectURL(blob)
      })

    }

    if(this.videoCoverConfig.uuid){

      commonApi.manageS3SelectFile(this.videoCoverConfig.uuid).then(res => {
        let blob = new Blob ([res.data],{type:'application/octet-stream'})
        this.videoCover=URL.createObjectURL(blob)
      })

    }
    this.htmlContentS3ImageSrcToBase64(this.formEditQuery.content)

  },
  beforeDestroy() {
    if (this.pic2Config.uuid) {
      URL.revokeObjectURL(this.pic2); // 清理URL对象
    }
    if (this.videoCoverConfig.uuid) {
      URL.revokeObjectURL(this.videoCover); // 清理URL对象
    }

  },
  methods: {

    htmlContentS3ImageSrcToBase64(content) {
      const params = {content: content }
      replaceHtmlS3ImageSrcToBase64(params).then((res) => {
        const {status, data} = res.data
          if (status === 200) {
            this.formEditQuery.content = data.htmlContent
          }

      })

    },
    /**
     * @Description: 处理 摘要图片的remove事件
     * @author Liu Rui Bing
     * @date 2024/7/11
     */
    handlePic2Remove(val) {
      // 如果是编辑模式的情况下触发了remove事件
      if (this.dialogStatus === 'EDIT') {
        this.formEditQuery.pic2 = ''
        let findObj = this.formEditQuery.fileIds.find(item => item === this.pic2Config.fid)
        if (!findObj) {
          this.formEditQuery.fileIds.push(this.pic2Config.fid) // 摘要图片 存在 删除的逻辑，需要把fid放到数组里面去
        }
      }
    },
    handleVideoCoverRemove(val) {
      // 如果是编辑模式的情况下触发了remove事件
      if (this.dialogStatus === 'EDIT') {
        this.formEditQuery.videoCover = ''
       // console.log(this.formEditQuery.fileIds,"fileIds")
        let findObj = this.formEditQuery.fileIds.find(item => item === this.videoCoverConfig.fid)
        if (!findObj) {
          this.formEditQuery.fileIds.push(this.videoCoverConfig.fid) // 摘要图片 存在 删除的逻辑，需要把fid放到数组里面去
        }
      }
    },
    changeFlag(value) {
      if (value === '2') {
        this.formEditQuery.content = ''
      } else {
        this.formEditQuery.video = ''
        this.formEditQuery.videoCover = ''
      }
    },
    handleSaveFund(formName) {
      try {
        this.$refs[formName].validate(async valid => {
          // console.log(valid,'valid')
          if (valid) {
            // console.log(this.formEditQuery.content,'formEditQuery.content')
            this.saveLoading = true
            const params = lodash.cloneDeep(this.formEditQuery)
            params.ndate = moment(new Date()).format('YYYY-MM-DD')
            params.fileIds = params.fileIds.toString()
            // 判断是否置顶
            if (params.topShow === true) {
              if (params.orderId == '') {
                this.$message.closeAll()
                this.$message.warning('请输入排序字段')
                return
              }
            } else {
              params.orderId = ''
            }

            delete params.fileList
            delete params.fileList2
            const formData = new FormData()
            for (const i in params) {
              formData.append(i, params[i])
            }

            const res = await saveReport(formData)
            if (res.data.status === 0) {
              this.$message({
                type: 'success',
                message: '提交成功'
              })
              this.saveLoading = false
              this.$emit('closeEdit', 'refesh')
            } else {
              this.saveLoading = false
              this.$message.error(res.data.message || '提交失败')
            }
          } else {
            this.saveLoading = false
            this.$message.warning(
              '请检查必填项'
            )
          }
        })
      } catch (e) {
        this.$message({
          type: 'waring',
          message: '提交失败'
        })
      }
    },
    beforeAvatarUpload(file, num) {
      if (num === 3) return true
      if (num === 5) {
        const fileSuffix = file.name.substring(file.name.lastIndexOf('.') + 1)
        const whiteList = ['pdf', 'doc', 'docx', 'ppt', 'pptx']
        const isSuffix = whiteList.indexOf(fileSuffix.toLowerCase()) === -1
        if (isSuffix) {
          this.$message.error('上传文件只能是 pdf、word、ppt格式')
          const currIdx = this.fileList2.indexOf(file)
          this.fileList2.splice(currIdx, 1)
          return false
        }
        const isLt50M = file.size / 1024 / 1024 < 50
        if (!isLt50M) {
          this.$message.error('上传文件大小不能超过 50MB!')
          const currIdx = this.fileList2.indexOf(file)
          this.fileList2.splice(currIdx, 1)
          return false
        }
        return isLt50M
      }
      const isJpeg = file.type === 'image/jpeg' || file.type === 'image/png' || file.type === 'image/jpg'
      const isLt50M = file.size / 1024 / 1024 < 50
      if (!isJpeg) {
        this.$message.error('上传图片只能是 JPG、PNG、JPEG 格式!')
        return false
      }
      if (!isLt50M) {
        this.$message.error('上传图片大小不能超过 50MB!')
        return false
      }
      if (num === 0 || num === 4) {
        // const isSize = new Promise(function(resolve,reject) {
        //   let width = 600
        //   let height = 400
        //   let _URL = window.URL || window.webkitURL
        //   let img = new Image()
        //   img.onload = function() {
        //     let valid = img.width >= width && img.height >= height
        //     valid ? resolve() : reject();
        //   }
        //   img.src = _URL.createObjectURL(file)
        // }).then(() => {
        //   return file;
        // },()=>{
        //   this.$message.error('上传图片像素要大于600*400!');
        //   this.deleteImg(num)
        //   return false;
        // })
        return isJpeg && isLt50M
      }

      return isJpeg && isLt50M
    },
    // 限制图片尺寸
    limitFileWH(E_width, E_height, file) {
      const _this = this
      let imgWidth = ''
      let imgHight = ''
      const isSize = new Promise(function (resolve, reject) {
        const width = E_width
        const height = E_height
        const _URL = window.URL || window.webkitURL
        const img = new Image()
        img.onload = function () {
          imgWidth = img.width
          imgHight = img.height
          const valid = img.width == width && img.height == height
          valid ? resolve() : reject()
        }
        img.src = _URL.createObjectURL(file)
      }).then(() => {
        return true
      }, () => {
        _this.$message.warning({
          message: '上传文件的图片大小不合符标准,宽需要为' + E_width + 'px，高需要为' + E_height + 'px。当前上传图片的宽高分别为：' + imgWidth + 'px和' +
            imgHight + 'px',
          btn: false
        })
        return false
      })
      return isSize
    }, httpRequest(param, num) {
      if (!this.beforeAvatarUpload(param.file, num)) {
        return
      }
      if (num === 0) {
        this.formEditQuery.pic1 = param.file
        const reader = new FileReader()
        let fileResult = ''
        reader.readAsDataURL(param.file)
        // 开始转
        reader.onload = () => {
          fileResult = reader.result
          this.pic1 = fileResult
        }
      }
      if (num === 1) {
        this.formEditQuery.pic3 = param.file
        const reader = new FileReader()
        let fileResult = ''
        reader.readAsDataURL(param.file)
        // 开始转
        reader.onload = () => {
          fileResult = reader.result
          this.pic3 = fileResult
        }
      }
      if (num === 2) {
        this.formEditQuery.videoCover = param.file
        const reader = new FileReader()
        let fileResult = ''
        reader.readAsDataURL(param.file)
        // 开始转
        reader.onload = () => {
          fileResult = reader.result
          this.videoCover = fileResult
        }

        if (this.dialogStatus === 'EDIT') {
          const index = this.formEditQuery.fileIds.indexOf(this.videoCoverConfig.fid);
          if (index > -1) {
            this.formEditQuery.fileIds.splice(index, 1);
          }

        }

      }
      if (num === 3) {
        this.formEditQuery.video = param.file

        if (this.dialogStatus === 'EDIT') {
          const index = this.formEditQuery.fileIds.indexOf(this.fileListConfig.fid);
          if (index > -1) {
            this.formEditQuery.fileIds.splice(index, 1);
          }

        }
        // console.log(param,'param')
        // console.log(this.fileList,'fileList')
      }

      if (num === 4) {
        this.formEditQuery.pic2 = param.file
        //console.log(this.formEditQuery.pic2, 'file')

        const reader = new FileReader()
        let fileResult = ''
        reader.readAsDataURL(param.file)
        // 开始转
        reader.onload = () => {
          fileResult = reader.result
          this.pic2 = fileResult
        }
        if (this.dialogStatus === 'EDIT') {
          const index = this.formEditQuery.fileIds.indexOf(this.pic2Config.fid);
          if (index > -1) {
            this.formEditQuery.fileIds.splice(index, 1);
          }

        }
      }
      if (num === 5) {
        this.formEditQuery.attachedFile = param.file
        //修改时先删除附件再上传时需要把删除id 置空

        if (this.dialogStatus === 'EDIT') {
          const index = this.formEditQuery.fileIds.indexOf(this.fileList2Config.fid);
          if (index > -1) {
            this.formEditQuery.fileIds.splice(index, 1);
          }

        }
      }
      if (num === 6) {
        const formData = new FormData()
        formData.append('files', param.file)
        commonApi.manageUpload(formData).then(res => {
         // console.log(res.data, 'res.data')
          if (res.data.status === 0) {
            const url = res.data.data
            const quill = this.$refs.myQuillEditor.quill
            // 获取光标位置
            const pos = quill.getSelection().index
            // 插入图片到光标位置
            quill.insertEmbed(pos, 'image', url[0])
          }
        })
      }
    },
    deleteImg(num) {
      if (num === 0) {
        this.pic1 = ''
        this.formEditQuery.pic1 = null
      }
      if (num === 1) {
        this.pic3 = ''
        this.formEditQuery.pic3 = null
      }
      if (num === 2) {
        this.videoCover = ''
        if (this.dialogStatus === 'EDIT') {
          let findObj = this.formEditQuery.fileIds.find(item => item === this.videoCoverConfig.fid)
          if (!findObj) {
            this.formEditQuery.fileIds.push(this.videoCoverConfig.fid) // 摘要图片 存在 删除的逻辑，需要把fid放到数组里面去
          }
        }
        this.formEditQuery.videoCover = null
      }
      // 摘要图片 处理方法
      if (num === 4) {
        this.pic2 = ''
        if (this.dialogStatus === 'EDIT') {
          let findObj = this.formEditQuery.fileIds.find(item => item === this.pic2Config.fid)
          if (!findObj) {
            this.formEditQuery.fileIds.push(this.pic2Config.fid) // 摘要图片 存在 删除的逻辑，需要把fid放到数组里面去
          }
        }
        this.formEditQuery.pic2 = ''
      }
    },

    quillSuccess(response) {
      if (response) {
        // 获取文本编辑器
        const quill = this.$refs.myQuillEditor.quill
        // 获取光标位置
        const pos = quill.getSelection().index
       // console.log(response, 'response')
        //alert('11')
        // 插入图片到光标位置
        quill.insertEmbed(pos, 'image', response.data.url)
      } else {
        this.$essage.error('图片插入失败')
      }
    },
    /**
     * @Description: type = video 视频 type = report 报告文件
     * @author Liu Rui Bing
     * @date 2024/7/12
     */
    beforeRemove(type) {
      if (type === 'video') {
        if (this.dialogStatus === 'EDIT') {
          let findObj = this.formEditQuery.fileIds.find(item => item == this.fileListConfig.fid)
          if (!findObj) {
            this.formEditQuery.fileIds.push(this.fileListConfig.fid)
          }
        }
        this.fileList = []
        this.formEditQuery.video = ''
      } else {
        if (this.dialogStatus === 'EDIT') {

          let findObj = this.formEditQuery.fileIds.find(item => item == this.fileList2Config.fid)
          if (!findObj) {
            this.formEditQuery.fileIds.push(this.fileList2Config.fid)
          }
        }
        this.fileList2 = []
        this.formEditQuery.attachedFile = ''
      }
    },
    dealFileList(arr) {
      const that = this
      // console.log(arr,'arr')
      arr.map(item => {
        if (item.fileType === '1') {
          that.pic1 = item.fileUrl
        }
        if (item.fileType === '2') {
          that.pic2 = item.fileUrl
          that.uuid=item.uuid
          that.pic2Config = item
        }
        if (item.fileType === '3') {
          that.pic3 = item.fileUrl
          // this.formEditQuery.pic3 = item.fileUrl
        }
        if (item.fileType === '4') {
          that.videoCover = item.fileUrl
          that.uuid=item.uuid
          that.videoCoverConfig=item

          // this.formEditQuery.videoCover = item.fileUrl
        }
        if (item.fileType === '5') {

          that.fileList = [{name: item.fileName, url: (item.uuid!==""?item.uuid:item.fileUrl)}]

          that.fileListConfig = item
          that.formEditQuery.video = (item.uuid!==""?item.uuid:item.fileUrl)
          that.uuid=item.uuid
          that.deletcType = 2
        }
        if (item.fileType === '6') {
          that.fileList2Config = item
          that.fileList2 = [{name: item.fileName, url: item.fileUrl}]
        }
      })
      //console.log(this.formEditQuery)
    },
    dealRowValue(value) {
      if (value != null) {
        if (value.status) {
          // 如果是公众号文章类型
          if(value.flag == '3') {
            value.content = value.content.replace(/<\/?[^>]+(>|$)/g, "")
          }
          this.status = value.status === '1'
          this.isHdleft = value.isHdleft === '1'
          this.topOrderId = value.topOrderId === '1'
          if (value.orderId) {
            value.topShow = true
          } else {
            value.topShow = false
          }
          value.flag = value.flag === '' ? '1' : value.flag
          value.ntypeDetail = getValueForArrayByKey(this.typeList, value.ntypeDetail, 'dimNme', 'dimCde', '')
          var arr = value.fileList.length > 0 ? value.fileList : []
          this.formEditQuery = {...this.formEditQuery, ...value}
          this.formEditQuery.fileIds = []
          if (arr.length > 0) this.dealFileList(arr)
          //console.log(this.formEditQuery)
        }
      }
    },
    switchChange(value, num) {
      if (num === 1) {
        this.formEditQuery.status = value ? '1' : '0'
      }
      if (num === 2) {
        this.formEditQuery.isHdleft = value ? '1' : '0'
      }
    }
  }
}
</script>
<style lang="scss" scoped>
::v-deep .el-switch.is-checked .el-switch__core {
  border-color: #e1b896;
    background-color: #e1b896;
}
.product-edit {
  width: 100%;

  ::v-deep .el-form {
    width: 100% !important;

    .el-input-group__prepend {
      padding: 0 8px;
    }
  }
}

.el-dialog {
  width: 60% !important;
}

.detail-dialog {
  .vue-quill-editor {
    margin-top: 10px;

    ::v-deep .quill-editor {
      line-height: normal;
      width: 100%;
      margin: 0 auto;

      .ql-container {
        line-height: normal !important;
        height: 340px !important;
        font-size: 14px;
      }

      .custom-height {
        height: 100vh !important;
      }

      .ql-snow {
        .ql-tooltip[data-mode=link]::before {
          content: "请输入链接地址:";
        }

        .ql-tooltip.ql-editing a.ql-action::after {
          border-right: 0px;
          content: '保存';
          padding-right: 0px;
        }

        .ql-tooltip[data-mode=video]::before {
          content: "请输入视频地址:";
        }

        .ql-picker.ql-size {
          .ql-picker-label[data-value="12px"]::before,
          .ql-picker-item[data-value="12px"]::before {
            content: '12px';
          }

          .ql-picker-label[data-value="14px"]::before,
          .ql-picker-item[data-value="14px"]::before {
            content: '14px';
          }

          .ql-picker-label[data-value="16px"]::before,
          .ql-picker-item[data-value="16px"]::before {
            content: '16px';
          }

          .ql-picker-label[data-value="18px"]::before,
          .ql-picker-item[data-value="18px"]::before {
            content: '18px';
          }

          .ql-picker-label[data-value="20px"]::before,
          .ql-picker-item[data-value="20px"]::before {
            content: '20px';
          }

          .ql-picker-label[data-value="24px"]::before,
          .ql-picker-item[data-value="24px"]::before {
            content: '24px';
          }

          .ql-picker-label[data-value="28px"]::before,
          .ql-picker-item[data-value="28px"]::before {
            content: '28px';
          }

          .ql-picker-label[data-value="32px"]::before,
          .ql-picker-item[data-value="32px"]::before {
            content: '32px';
          }

          .ql-picker-label[data-value="36px"]::before,
          .ql-picker-item[data-value="36px"]::before {
            content: '36px';
          }
        }

        .ql-picker.ql-header {
          .ql-picker-label::before,
          .ql-picker-item::before {
            content: '文本';
          }

          .ql-picker-label[data-value="1"]::before,
          .ql-picker-item[data-value="1"]::before {
            content: '标题1';
          }

          .ql-picker-label[data-value="2"]::before,
          .ql-picker-item[data-value="2"]::before {
            content: '标题2';
          }

          .ql-picker-label[data-value="3"]::before,
          .ql-picker-item[data-value="3"]::before {
            content: '标题3';
          }

          .ql-picker-label[data-value="4"]::before,
          .ql-picker-item[data-value="4"]::before {
            content: '标题4';
          }

          .ql-picker-label[data-value="5"]::before,
          .ql-picker-item[data-value="5"]::before {
            content: '标题5';
          }

          .ql-picker-label[data-value="6"]::before,
          .ql-picker-item[data-value="6"]::before {
            content: '标题6';
          }
        }

        .ql-picker.ql-font {
          .ql-picker-label[data-value="SimSun"]::before,
          .ql-picker-item[data-value="SimSun"]::before {
            content: "宋体";
            font-family: "SimSun" !important;
          }

          .ql-picker-label[data-value="SimHei"]::before,
          .ql-picker-item[data-value="SimHei"]::before {
            content: "黑体";
            font-family: "SimHei";
          }

          .ql-picker-label[data-value="Microsoft-YaHei"]::before,
          .ql-picker-item[data-value="Microsoft-YaHei"]::before {
            content: "微软雅黑";
            font-family: "Microsoft YaHei";
          }

          .ql-picker-label[data-value="KaiTi"]::before,
          .ql-picker-item[data-value="KaiTi"]::before {
            content: "楷体";
            font-family: "KaiTi" !important;
          }

          .ql-picker-label[data-value="FangSong"]::before,
          .ql-picker-item[data-value="FangSong"]::before {
            content: "仿宋";
            font-family: "FangSong";
          }
        }
      }

      .ql-align-center {
        text-align: center;
      }

      .ql-align-right {
        text-align: right;
      }

      .ql-align-left {
        text-align: left;
      }
    }
  }

}
</style>
<style lang="scss">
.over-term {
  width: 100%;

  .el-form-item__content {
    width: 70%;
    min-width: 300px;

    .el-input {
      width: 100% !important;
    }

    .el-textarea {
      width: 100% !important;
    }
  }
}

.vue-quill-editor .ql-editor {
  height: 95%;
  overflow: auto;
}

.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100px;
  height: 100px;
  line-height: 100px;
  text-align: center;
}

.avatar {
  width: 100px;
  height: 100px;
  display: block;
  position: relative;

  .icon-img {
    display: none;
    position: absolute;
    top: 0px;
    right: 0;
    font-size: 20px;
    margin-bottom: 15px;
    color: #e03d3e;
    -webkit-transition: color .15s linear;
    transition: color .15s linear;
    z-index: 100;
  }

  &:hover {
    img {
      opacity: 0.5;
    }

    .icon-img {
      display: block;
    }
  }

}

.detail-dialog .reportForm {
  width: 100% !important;
}

.pic {
  position: relative;

  .notes {
    position: absolute;
    bottom: 30px;
    font-weight: 500;
    color: #F56C6C;
    font-size: 14px;
    line-height: 18px;
    padding-top: 4px;

    div {
      width: 37px;
      display: inline-block;
    }
  }
}

</style>

import commonFun from '@/filters/new_common'
import fun from '@/filters/common'
import synHandleApi from '@/api/synHandle/synHandle'
import bizBeginApi from '@/api/transfer/bizBegin'
import modelFileValidate from '@/mixinsModel/file-validate'
import pageApi from "@/api/productNew/infoChange.js"
export default {
  mixins: [modelFileValidate],
  data() {
    //参数类型
    const csValidate = (rule, value, callback) => {
      if (this.formInline.paramTas.length === 0 && this.formInline.paramAsss.length === 0) {
        callback(new Error("请至少选择一种参数类型"));
      } else {
        callback();
      }
    }
    //特殊事项类型
    const tsValidate = (rule, value, callback) => {
      if (this.formInline.matterTas.length === 0 && this.formInline.matterAsss.length === 0) {
        callback(new Error("请至少选择一种特殊事项类型"));
      } else {
        callback();
      }
    }
     //流转方式
     const lzValidate = (rule, value, callback) => {
      if (!this.formInline.isWanderLocal && !this.formInline.isWanderRemote) {
        callback(new Error("请至少选择一种流转方式"));
      } else {
        callback();
      }
    }
    return {
      movePlace: {
        position: 'relative',
        left: '',
        top: ''
      },
      fixStyle: {
        position: 'fixed',
        width: '',
        bottom: 0,
        right: 0,
      },
      formHandle: {
        remark: ''
      },
      isFq: true,
      countSubmit_btn: false,
      noraml_Name: "审批通过",
      syn_label: "参数描述",
      isUser: true,
      stepDataInofo: [],
      stepRowName: '',
      isViewStepInfo: false,
      viewInfo: "",
      inHandInfo: "",
      drawerSize: '50%',
      getDataForm: {},
      bpmData: [],
      drawer: false,
      isLeftInfo: false,
      leftDrawer: false,
      form_show: true,
      myTaskId: '',
      tableList: [],
      active: 0,
      stepData: [],
      fileList: [],
      accountCodes: [], //产品名称
      fileUploadUrl:
        "http://xulei520bb.imwork.net/pfom/api/file/v1.0/uploadFile?relaType=conduct_file&source=GMYYPT&relaId=",
      hearders: {
        Authorization: "vXcx3IBemn1kShhobK2DfpY3kFqiBaSb",
        "Access-Control-Allow-Origin": "*",
      },
    }
  },
  methods: {
    handleError() {
      this.$message.closeAll();
      this.$message.error("文件上传失败");
      self.submit_btn = false; //按钮启用
    },
    handleRemove(file, fileList) {
      this.onFreshValidation()
      this.formInline.fileList = fileList;
    },
    downFile(file) {
      if (file.id) {
        let params = {};
        params.id = file.id;
        params = commonFun.parameterSrc(params);
        if (this.$store.getters.token) {
          params["token"] = this.$store.getters.token;
        }
        let action = this.$store.state.setting.baseApi + "api/file/v1.0/downloadFile";
        commonFun.formDownloadFile(params, action, "GET");
      }
    },
    handleSuccess(res, file, fileList) {
      if (res.message === "success") {
        let resultData = res.data;
        this.formInline.fileId = resultData[0].id;
      } else if (res.status === 401) {
        this.$message.closeAll();
        this.$message.error("文件上传失败");
      }
    },
    handleChange(file, fileList) {
      this.fileValidate(file, fileList, 'flag')
      this.onFreshValidation();
    },
    //查询综合办理业务类型
    getTransferType() {
      let params = "synCmdType";
      this.tranferTypes = [];
      synHandleApi.getTransferType(params).then((res) => {
        if (res.data.message === "success") {
          let data = res.data.data;
          this.tranferTypes = data;
          let arr = data;
          for (let i = 0; i < arr.length; i++) {
            this.cmdCodeArr[arr[i].dimCde] = arr[i].dimNme;
          }
        } else {
          this.tranferTypes = [];
          this.$message.closeAll();
          this.$message.error("查询信息失败");
        }
      });
    },
    
    //获取Selects
    getSelects(val) {
      let params = val;
      synHandleApi.getTransferType(params).then((res) => {
        if (res.data.message === "success") {
          
        } else {
          this.$message.closeAll();
          this.$message.error("初始化数据失败");
        }
      });
    },
    dataStatus(statusCode) {
      return this.cmdCodeArr[statusCode];
    },
    
    onFreshValidation() {
      this.$nextTick(() => {
        this.$refs.formInline.validate((valid) => {});
      });
    },
    
    
    //审核通过，退回，作废，暂缓等操作-----------------
    updateStatus(vals, status, confirmStatus) {
      this.$refs.formInline.validate((valid) => {
        if (valid) {
          this.$confirm("是否" + confirmStatus, "提示", {
              confirmButtonText: "确定",
              cancelButtonText: "取消",
              type: "warning",
            }).then(() => {
              //初始化数据
              this.serachSubmit(status, confirmStatus);
            }).catch((type) => {
              this.$message.closeAll();
              this.$message({
                type: "info",
                message: "已取消",
              });
            });
        }
      })
    },
    serachSubmit(status, confirmStatus) {
        this.countSubmit_btn = true;
        let myXmlId = this.getDataForm.taskKey
        // let params = Object.assign({}, this.formHandle);
        let sendData = {};
        let taskExcuteCmdMode = { taskExcuteCmdType: status };
        let taskOpinionModel = { agree: true };
        taskOpinionModel.opinion = this.formHandle.remark;
        if(this.formHandle.remark==''){taskOpinionModel.opinion=confirmStatus}
        let formData = { approveFlag: true };
        if (myXmlId === "change_ywfq") {
          let params = {};
          params = commonFun.parameterSrcFull(this.formInline);
          if(params.fileList){
            delete params.fileList
          }
          if(params.fundCode){
            let arr = params.fundCode.split("_");
            params.fundCode = arr[0];
            params.fundName = arr[1];
          }
          formData = params;
        }
        sendData.formData = formData;
        sendData.taskOpinionModel = taskOpinionModel;
        sendData.taskExcuteCmdMode = taskExcuteCmdMode;
        let taskId = this.myTaskId;
        if (this.getDataForm && this.getDataForm.taskKey == 'change_ywfq') this.upNewFileUrl(sendData)
        else {
          synHandleApi.updateStatus(taskId, sendData).then((res) => {
              if (res.data.status === 0) {
                this.$message.closeAll();
                this.$message({
                  type: "success",
                  message: "操作成功",
                });
                this.drawer = false;
                this.formHandle.remark = "";
                this.$emit('refash')
              } else {
                this.$message.closeAll();
                this.$message({
                  type: "error",
                  message: res.data.message || "操作失败",
                });
              }
              this.countSubmit_btn = false;
            }).catch(() => {
              // 关闭移动指标弹框
              this.countSubmit_btn = false;
            });
        }
    },
    // 业务发起的时候文件的上传的接口
    upNewFileUrl (data) {
      this.$message.closeAll();
      let formData = new FormData();
      let fileList = this.formInline.fileList
      for (let i of fileList) {
        if (i.id) formData.append('fileId', i.id)
        else formData.append('file', i.raw);
      }
      formData.append('taskInstId', this.myTaskId)
      formData.append('datastr', JSON.stringify(data))
      pageApi.updateInfoChange(formData).then(({data: res}) => {
        if (res.status == 200) {
          this.drawer = false;
          this.formHandle.remark = "";
          this.$message.success('操作成功')
          this.$emit('refash')
        }else if(res.status == 30){
          this.$confirm(res.message, '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            
          }).catch(() => {
                   
          });
        } else this.$message.error(res.message || '操作失败')
        this.countSubmit_btn = false;
      }).catch((err) => {
        this.$message.error('服务异常')
        this.countSubmit_btn = false
      })
    },
  }
}

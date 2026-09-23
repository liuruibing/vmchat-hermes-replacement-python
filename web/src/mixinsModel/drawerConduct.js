import commonFun from '@/filters/new_common'
import fun from '@/filters/common'
import synHandleApi from '@/api/synHandle/synHandle'
import bizBeginApi from '@/api/transfer/bizBegin'
import modelFileValidate from '@/mixinsModel/file-validate'
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
      selects: [
        { value: '选项1', label: '经纪商1' },
        { value: '选项2', label: '经纪商2' }
      ], //销售机构选择
      formHandle: {
        remark: ''
      },
      abandon_btn_show: true,
      cancle_btn_show: true,
      pause_btn_show: true,
      unPause_btn_show: false,
      fundNameArr: [],
      paramTaArr: [],
      paramGzArr: [],
      synTaArr: [],
      synGzArr: [],
      synName1Arr: [],
      synName3Arr: [],
      synAccountTypeArr: [],
      saleAccountTypeArr: [],
      cmdCodeArr: [],
      tranferTypes: [],
      isFq: true,
      syn_nb_dx: true,
      syn_wb_dx: true,
      params_show: false,
      accounts_show: false,
      matters_show: false,
      retire_btn_show: true,
      syn_zh_input_show: false,
      syn_ta_input_show: false,
      syn_gz_input_show: false,
      cs_ta_input_show: false, //参数Ta其他是否显示
      cs_gz_input_show: false, //参数估值其他是否显示
      syn_xh_input_show: false, //账户，销户其他是否显示
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
      // 验证规则
      commitRules: {
        // 产品&基金代码
        fundName: { required: true, trigger: "change", message: "请选择产品" },

        paramTaOther: {
          required: true,
          trigger: "change",
          message: "请输入内容",
        },
        paramAssOther: {
          required: true,
          trigger: "change",
          message: "请输入内容",
        },
        accountTypeOther: {
          required: true,
          trigger: "change",
          message: "请输入内容",
        },
        accountSaleTypeOther: {
          required: true,
          trigger: "change",
          message: "请输入内容",
        },
        matterTaOther: {
          required: true,
          trigger: "change",
          message: "请输入内容",
        },
        matterAssOther: {
          required: true,
          trigger: "change",
          message: "请输入内容",
        },

        params: {
          required: true,
          trigger: "change",
          message: "",
          validator: csValidate
        },
        accounts: {
          required: true,
          trigger: "change",
          message: "请至少选择一种账户类型",
        },
        matters: {
          required: true,
          trigger: "change",
          message: "",
          validator: tsValidate
        },
        wanders: {
          required: true,
          trigger: "change",
          message: "",
          validator: lzValidate
        },

        //wanderLocalStations:{required: false,trigger: 'change',validator:validateWanderLocalStations },
        //wanderRemoteStations:{required: false,trigger: 'change',validator:validateWanderRemoteStations},

        cmdRemark: { required: false, type: "string", trigger: "change" },
        fileList: { required: false, trigger: "change", message: "请选择附件" },
      },
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
      // this.$message.closeAll()
      // let totalSize = 0; //文件大小的累加
      // let totalFlag = 0;
      // let totalFilel = [];
      // if (!file.size) {
      //   for (let item of fileList) {
      //     if (item.size) totalFilel.push(item)
      //   }
      //   this.formInline.fileList = totalFilel
      //   return this.$message.error("上传的文件不能为空文件")
      // }
      // this.formInline.fileList = fileList
      // // 多个文件的累加超过50m时
      // for (let item of fileList) {
      //   totalSize = item.size + totalSize;
      // }
      // totalFlag = 0 < (totalSize / 1024 / 1024) && (totalSize / 1024 / 1024) < 50;
      // if (!totalFlag) {
      //   this.$message.error("上传的文件不能超过 50M !");
      //   for (let item of fileList) {
      //     if (file.uid !== item.uid) {
      //       totalFilel.push(item);
      //     }
      //   }
      // } else {
      //   for (let item of fileList) {
      //     totalFilel.push(item);
      //   }
      // }
      // this.formInline.fileList = totalFilel;
      this.onFreshValidation();
    },
    //选择参数ta类事件
    handleCheckedChange_paramsTa(value) {
      this.cs_ta_input_show = false;

      for (let i = 0; i < value.length; i++) {
        if (value[i] === "paramTa_007") {
          this.cs_ta_input_show = true;
          break;
        }
      }
      if (!this.cs_ta_input_show) {
        this.formInline.paramTaOther = "";
      }
      this.onChangeParams(value, false);
      this.isUesrDefaultGw()
    },
    //选择参数估值类事件
    handleCheckedChange_paramsGz(value) {
      this.cs_gz_input_show = false;

      for (let i = 0; i < value.length; i++) {
        if (value[i] === "paramGz_006") {
          this.cs_gz_input_show = true;
          break;
        }
      }
      if (!this.cs_gz_input_show) {
        this.formInline.paramAssOther = "";
      }
      this.onChangeParams(value, false);
      this.isUesrDefaultGw()
    },
    
    //选择账户类事件
    handleCheckedChange_account(value) {
      this.syn_zh_input_show = false;

      for (let i = 0; i < value.length; i++) {
        if (value[i] === "synAccount_008") {
          this.syn_zh_input_show = true;
          break;
        }
      }
      if (!this.syn_zh_input_show) {
        this.formInline.accountTypeOther = "";
      }
      this.onChangeAccounts(value, false);
      this.hangCheckAcZH()
    },
     //选择账户类事件
    handleCheckedChange_accountSale(value) {
      this.syn_xh_input_show = false;

      for (let i = 0; i < value.length; i++) {
        if (value[i] === "saleAccount_008") {
          this.syn_xh_input_show = true;
          break;
        }
      }
      if (!this.syn_xh_input_show) {
        this.formInline.accountSaleTypeOther = "";
      }
      this.onChangeAccounts(value, false);
      this.hangCheckAcZH()
    },
    //选择估值类事件
    handleCheckedChange_gz(value) {
      this.syn_gz_input_show = false;

      for (let i = 0; i < value.length; i++) {
        if (value[i] === "synGz_003") {
          this.syn_gz_input_show = true;
          break;
        }
      }
      if (!this.syn_gz_input_show) {
        this.formInline.matterAssOther = "";
      }
      this.onChangeMatters(value, false);
    },
    syn_nb_fun() {
      let flag = this.formInline.isWanderLocal;
      if (flag) {
        this.syn_nb_gw = false;
        this.syn_nb_dx = false;

        this.commitRules["wanderLocalStations"] = {
          required: true,
          trigger: "change",
          message: "请至少选择一个流转岗位",
        };
      } else {
        this.syn_nb_gw = true;
        this.syn_nb_dx = true;
        this.formInline.isNoticeMsgLocal = "";

        this.formInline.wanderLocalStations = [];
        this.commitRules["wanderLocalStations"] = null;
        this.$refs.formInline.clearValidate("wanderLocalStations");
      }
      this.onChangeWanders("", false);
    },
    syn_wb_fun() {
      let flag = this.formInline.isWanderRemote;
      if (flag) {
        this.syn_wb_gw = false;
        this.syn_wb_dx = false;
        this.commitRules["wanderRemoteStations"] = {
          required: true,
          trigger: "change",
          message: "请至少选择一个流转岗位",
        };
      } else {
        this.syn_wb_gw = true;
        this.syn_wb_dx = true;
        this.formInline.isNoticeMsgRemote = "";

        this.formInline.wanderRemoteStations = [];
        this.commitRules["wanderRemoteStations"] = null;
        this.$refs.formInline.clearValidate("wanderRemoteStations");
      }

      this.onChangeWanders("", false);
    },
    onChangeAccounts(value, breakFlag) {
      //必须选择至少一个选项(账户类)
      let selArr = [].concat(
        this.formInline.accountTypes || [],
        this.formInline.accountSaleTypes || []
      );

      if (selArr.length == 0) {
        this.formInline.accounts = "";
      } else {
        this.formInline.accounts = "select";
      }
    },
    onChangeWanders(value, breakFlag) {
      //必须选择至少一个选项(流转类)
      let isWander =
        this.formInline.isWanderLocal || this.formInline.isWanderRemote;

      if (!isWander) {
        this.formInline.wanders = "";
      } else {
        this.formInline.wanders = "select";
      }
      if (!breakFlag) {
        this.$refs.formInline.validate((valid) => {});
      }
    },
    onChangeMatters(value, breakFlag) {
      //必须选择至少一个选项(特殊事项类)
      let selArr = [].concat(
        this.formInline.matterTas || [],
        this.formInline.matterAsss || []
      );

      if (selArr.length == 0) {
        this.formInline.matters = "";
      } else {
        this.formInline.matters = "select";
      }
    },
    onChangeParams(value, breakFlag) {
      //必须选择至少一个选项(参数类)
      let selArr = [].concat(
        this.formInline.paramTas || [],
        this.formInline.paramAsss || []
      );

      if (selArr.length == 0) {
        this.formInline.params = "";
      } else {
        this.formInline.params = "select";
      }
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
    getFZData () {
      bizBeginApi.getFZAccount().then(({data: res}) => {
        if (res.status !== 200) return
        // console.log(res.data)
        let singleNo = new Array
        let singleNo2 = new Array
        let temp = new Array
        for (let i of res.data) singleNo.push(i.deptId)
        singleNo2 = [...new Set(singleNo)]
        for (let i of singleNo2) {
          let obj = { label: '', options: [] }
          for (let j of res.data) {
            if (j.deptId == i) {
              obj['label'] = j.deptName
              obj['options'].push({
                dimCde: j.positionCode,
                dimNme: j.positionName
              })
            }
          }
          temp.push(obj)
        }
        // console.log(temp)
        this.synName1Arr = temp
      }).catch((err) => console.log('is msg err', err))
    },
    //获取Selects
    getSelects(val) {
      let params = val;
      synHandleApi.getTransferType(params).then((res) => {
        if (res.data.message === "success") {
          if (val === "synAccountType") {
            this.synAccountTypeArr = res.data.data;
          }
          if (val === "syn_ta") {
            this.synTaArr = res.data.data;
          }

          if (val === "syn_gz") {
            this.synGzArr = res.data.data;
          }
          // if (val === "wanderLocalStation") {
          //   this.synName1Arr = res.data.data;
          // }
          if (val === "wanderRemoteStation") {
            this.synName3Arr = res.data.data;
          }
          if (val === "param_ta") {
            this.paramTaArr = res.data.data; //参数类ta数组
          }
          if (val === "param_gz") {
            this.paramGzArr = res.data.data; //参数类估值数组
          }
          if (val === "saleAccountType") {
            this.saleAccountTypeArr = res.data.data; //销户类型数组
          }
        } else {
          this.$message.closeAll();
          this.$message.error("初始化数据失败");
        }
      });
    },
    dataStatus(statusCode) {
      return this.cmdCodeArr[statusCode];
    },
    detailInitHandle(label, id) {
      if (label === "参数类") {
        this.syn_zh_show = false;
        this.syn_ts_show = false;
        this.syn_cs_show = true;
        this.syn_cs_show2 = true;
        this.syn_label = "参数描述";
      } else if (label === "账户类") {
        this.syn_zh_show = true;
        this.syn_ts_show = false;
        this.syn_cs_show = false;
        this.syn_cs_show2 = false;
        // this.getRelation(id,"accountType");
      } else if (label === "需求类") {
        this.syn_zh_show = false;
        this.syn_ts_show = false;
        this.syn_cs_show = true;
        this.syn_cs_show2 = false;
        this.syn_label = "需求描述";
      } else if (label === "特殊事项交互类") {
        this.syn_zh_show = false;
        this.syn_ts_show = true;
        this.syn_cs_show = false;
        this.syn_cs_show2 = false;
        // this.getRelation(id,"matterTa");
        // this.getRelation(id,"matterAss");
      } else {
        this.syn_zh_show = false;
        this.syn_ts_show = false;
        this.syn_cs_show = true;
        this.syn_cs_show2 = false;
        this.syn_label = "特殊事项描述";
      }
      let cmdStatus = this.procStatus;
      if (cmdStatus === "cmdSuspend") {
        this.unPause_btn_show = true;
        this.pause_btn_show = false;
        this.abandon_btn_show = false;
        this.cancle_btn_show = false;
        this.normal_btn_show = false;
        this.retire_btn_show = false;
      } else {
        this.unPause_btn_show = false;
        this.pause_btn_show = true;
        this.abandon_btn_show = true;
        this.cancle_btn_show = true;
        this.normal_btn_show = true;
        this.retire_btn_show = true;
      }
    },
    //选择ta类事件
    handleCheckedChange_ta(value) {
      this.syn_ta_input_show = false;
      for (let i = 0; i < value.length; i++) {
        if (value[i] === "synTa_011") {
          this.syn_ta_input_show = true;

          break;
        }
      }
      if (!this.syn_ta_input_show) {
        this.formInline.matterTaOther = "";
      }
      this.onChangeMatters(value, false);
    },
    onFreshValidation() {
      this.$nextTick(() => {
        this.$refs.formInline.validate((valid) => {});
      });
    },
    // 表单的基本信息
    getResultData() {
      let data = this.getDataForm.dataForm
      if (data.isWanderRemote == '0' || typeof(data.isWanderRemote) == 'undefined') {
        this.hasWBServer = true  //编辑条件下是否课进行编辑
        this.isUserWBServer = true
      } else {
        this.hasWBServer = false
        this.isUserWBServer = false
      }
      if (
        this.getDataForm.taskKey == "conduct_ywfq" ||
        this.getDataForm.taskKey == "conremote_ywfq"
      ) {
        self.retire_btn_show = false;
      } else {
        self.retire_btn_show = true;
      }
      // this.myTaskId = taskId;
      let codeName = this.dataStatus(data.cmdCode);
      this.detailInitHandle(codeName, data.id);
      this.initSearchForm(data);
      //初始化事件
      this.onChangeParams("", false);
      this.onChangeAccounts("", false);
      this.onChangeMatters("", false);
      this.onChangeWanders("", false);
      this.syn_nb_fun();
      this.syn_wb_fun();
      // this.formInline.beginTime = fun.timeFormat(this.getDataForm.beginTime)
      this.formInline.beginTime =  this.getDataForm.beginTime
      this.formInline.pfomBizNum = data.pfomBizNum
      this.formInline.fundName = data.fundCode + "_" + data.fundName;
    },
    initSearchForm(data) {
      let cmdCode = data.cmdCode;
      if (cmdCode == "060101") {
        this.syn_label = "参数描述";
        this.params_show = true;
        this.accounts_show = false;
        this.matters_show = false;
      } else if (cmdCode == "060102") {
        this.syn_label = "备注说明";
        this.params_show = false;
        this.accounts_show = true;
        this.matters_show = false;
      } else if (cmdCode == "060103") {
        this.syn_label = "需求描述";
        this.params_show = false;
        this.accounts_show = false;
        this.matters_show = false;
      } else if (cmdCode == "060104") {
        this.syn_label = "特殊事项描述";
        this.params_show = false;
        this.accounts_show = false;
        this.matters_show = true;
      } else if (cmdCode == "060105") {
        this.syn_label = "特殊事项描述";
        this.params_show = false;
        this.accounts_show = false;
        this.matters_show = false;
      }
      let myXmlId = this.getDataForm.taskKey
      let flag = this.form_show;
      this.syn_nb_gw = true;
      this.syn_wb_gw = true;
      this.syn_wb_dx = true;
      this.syn_nb_dx = true;
      this.noraml_Name = "审批通过";
      this.isFq = true; //00

      // this.formInline.fundName = data.fundCode + "_" + data.fundName;
      // console.log(this.formInline.fundName)

      this.formInline.paramTas = data.paramTas;
      this.formInline.paramTaOther = data.paramTaOther;
      this.formInline.paramAsss = data.paramAsss;
      this.formInline.paramAssOther = data.paramAssOther;

      this.formInline.accountTypes = data.accountTypes;
      this.formInline.accountTypeOther = data.accountTypeOther;
      this.formInline.accountSaleTypes = data.accountSaleTypes;
      this.formInline.accountSaleTypeOther = data.accountSaleTypeOther;

      this.formInline.matterTas = data.matterTas;
      this.formInline.matterAsss = data.matterAsss;
      this.formInline.matterTaOther = data.matterTaOther;
      this.formInline.matterAssOther = data.matterAssOther;
      this.formInline.wanderLocalStations = data.wanderLocalStations;
      this.formInline.wanderRemoteStations = data.wanderRemoteStations;

      this.formInline.cmdRemark = data.cmdRemark;

      this.formInline.cmdCode = data.cmdCode;
      this.formInline.id = data.id;

      if (data.matterTaOther) {
        this.syn_ta_input_show = true;
      } else {
        this.syn_ta_input_show = false;
      }

      if (data.matterAssOther) {
        this.syn_gz_input_show = true;
      } else {
        this.syn_gz_input_show = false;
      }

      if (data.accountTypeOther) {
        this.syn_zh_input_show = true;
      } else {
        this.syn_zh_input_show = false;
      }

      if (data.paramTaOther) {
        this.cs_ta_input_show = true;
      } else {
        this.cs_ta_input_show = false;
      }

      if (data.paramAssOther) {
        this.cs_gz_input_show = true;
      } else {
        this.cs_gz_input_show = false;
      }

      if (data.accountSaleTypeOther) {
        this.syn_xh_input_show = true;
      } else {
        this.syn_xh_input_show = false;
      }

      if (data.isNoticeMsgLocal === "1") {
        this.formInline.isNoticeMsgLocal = true;
      } else {
        this.formInline.isNoticeMsgLocal = false;
      }
      if (data.isNoticeMsgRemote === "1") {
        this.formInline.isNoticeMsgRemote = true;
      } else {
        this.formInline.isNoticeMsgRemote = false;
      }

      if (data.isWanderLocal === "1") {
        this.formInline.isWanderLocal = true;
        if (flag && myXmlId === "conduct_ywfq") {
          this.syn_nb_gw = false;
          this.syn_nb_dx = false;
        }
      } else {
        this.formInline.isWanderLocal = false;
        this.formInline.wanderLocalStations = [];

        if (flag && myXmlId === "conduct_ywfq") {
          this.syn_nb_gw = true;
          this.syn_nb_dx = true;
        }
      }

      if (data.isWanderRemote === "1") {
        this.formInline.isWanderRemote = true;
        if (flag && myXmlId === "conduct_ywfq") {
          this.syn_wb_gw = false;
          this.syn_wb_dx = false;
        }
      } else {
        this.formInline.isWanderRemote = false;
        this.formInline.wanderRemoteStations = [];
        if (flag && myXmlId === "conduct_ywfq") {
          this.syn_wb_gw = true;
          this.syn_wb_dx = true;
        }
      }
      if (flag && myXmlId === "conduct_ywfq") {
        this.isFq = false;
        this.noraml_Name = "提交";
        this.retire_btn_show = false;
      }
      if (flag && myXmlId === "conduct_out") {
        this.retire_btn_show = false;
        this.normal_btn_show = false;
      }
      this.$nextTick(() => {
        this.$refs.formInline.clearValidate()
      })
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
        console.log(taskOpinionModel.opinion,'788');
        let formData = { approveFlag: true };
        if (myXmlId === "conduct_ywfq") {
          let params = {};
          params = commonFun.parameterSrcFull(this.formInline);
          if (params.isWanderLocal) {
            params.isWanderLocal = "1";
          } else {
            params.isWanderLocal = "0";
          }
          if (params.isWanderRemote) {
            params.isWanderRemote = "1";
          } else {
            params.isWanderRemote = "0";
          }
          if (params.isNoticeMsgRemote) {
            params.isNoticeMsgRemote = "1";
          } else {
            params.isNoticeMsgRemote = "0";
          }
          if (params.isNoticeMsgLocal) {
            params.isNoticeMsgLocal = "1";
          } else {
            params.isNoticeMsgLocal = "0";
          }
          params.fundCode = params.fundName.split("_")[0];
          params.fundName = params.fundName.split("_")[1];
          formData = params;
        }
        sendData.formData = formData;
        sendData.taskOpinionModel = taskOpinionModel;
        sendData.taskExcuteCmdMode = taskExcuteCmdMode;
        // if (status === "Retire") {
        //   let followTasks = [{ candidates: [], xmlId: "conduct_ywfq" }];
        //   if (this.getDataForm.taskKey.indexOf("conremote") > -1) {
        //     followTasks = [{ candidates: [], xmlId: "conremote_ywfq" }];
        //     sendData.formData["approveFlag"] = false;
        //     sendData.taskExcuteCmdMode["taskExcuteCmdType"] = "Normal";
        //   }
        //   taskExcuteCmdMode.followTasks = followTasks;
        // }
        let taskId = this.myTaskId;
        if (this.getDataForm && this.getDataForm.taskKey == 'conduct_ywfq') this.upNewFileUrl(sendData)
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
                this.$emit('closeD');
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
      synHandleApi.senChangeFileUrl(formData).then(({data: res}) => {
        if (res.status == 200) {
          this.drawer = false;
          this.formHandle.remark = "";
          this.$message.success('操作成功')
          this.$emit('refash')
          this.$emit('closeD');
        } else this.$message.error(res.message || '操作失败')
        this.countSubmit_btn = false;
      }).catch((err) => {
        this.$message.error('服务异常')
        this.countSubmit_btn = false
      })
    },
  }
}

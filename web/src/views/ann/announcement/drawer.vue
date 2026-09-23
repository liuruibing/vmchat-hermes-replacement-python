<template>
  <div class="rightDrawerStyle rightDrawerStyle_conductNew">
    <el-drawer
      title="标题"
      :size="drawerSize"
      :visible.sync="drawer"
      :with-header="false"
      @closed="closedDrawer"
      show-close
    >
      <el-row style="height: 100%">
        <el-col :span="9" v-if="isLeftInfo">
          <div ref="leftInfo" id="leftInfo" class="titleStyle"></div>
        </el-col>
        <el-col :span="isLeftInfo ? 15 : 24">
          <div class="mainBox">
            <!-- titel -->
            <div class="titleStyle">
              <el-row>
                <el-col :span="22">
                  <span style="color: #409eff">
                    {{ viewInfo }}
                    <!-- <span style="color: red">{{ inHandInfo }}</span> -->
                  </span>
                </el-col>
                <el-col :span="2">
                  <span
                    class="el-icon-close bigSize"
                    @click="drawer = false"
                  ></span>
                </el-col>
              </el-row>
            </div>
            <!-- step -->
            <div class="steps_zhyw" @mouseleave="isViewStepInfo = false">
              <el-steps :active="activeIndex" finish-status="success">
                <el-step
                  v-for="(item, index) in stepData"
                  :key="index"
                  :title="item.stepTitle"
                  :description="item.des"
                  :status="item.status"
                  @mouseenter.native="stepClick(item)"
                ></el-step>
              </el-steps>

              <div :style="movePlace" v-if="isViewStepInfo" class="movePlace">
                <el-card class="box-card">
                  <!-- <div class="stepRowName_style">
                      <span>{{ stepRowName }}</span>
                    </div> -->
                  <div
                    style="
                      margin-bottom: 10px;
                      font-weight: 600;
                      color: #409eff;
                    "
                  >
                    <el-row>
                      <el-col :span="8">待办人</el-col>
                      <el-col :span="8">联系电话</el-col>
                      <el-col :span="8">邮箱</el-col>
                    </el-row>
                    <div class="solidStyle"></div>
                  </div>
                  <div
                    v-for="(item, index) in stepDataInofo"
                    :key="index + 'man'"
                    style="color: #409eff"
                  >
                    <el-row>
                      <el-col :span="8">{{ item.userName || "-" }}</el-col>
                      <el-col :span="8">{{ item.userPhone || "-" }}</el-col>
                      <el-col :span="8">{{ item.userEmail || "-" }}</el-col>
                    </el-row>
                    <div><div class="borderLine"></div></div>
                  </div>
                </el-card>
              </div>
            </div>
            <!-- buton -->
            <div class="btnStyle">
              <el-button type="primary" size="small" @click="viewLcPic"
                >查看流程图</el-button
              >
              <el-button type="primary" size="small" @click="infoLeader"
                >查看交互指引</el-button
              >
            </div>
            <el-drawer
              title="流程图"
              :append-to-body="true"
              direction="ltr"
              size="65%"
              style="overflow-x: auto"
              :visible.sync="leftDrawer"
            >
              <bpmPage ref="bpm" v-if="leftDrawer"></bpmPage>
            </el-drawer>
            <!-- from -->
            <div class="formStyle">
              <el-form
                label-width="110px"
                ref="formInline"
                :rules="commitRules"
                :model="formInline"
                class="commitRules el-form-conduct"
                style="margin-top: 8px; margin-bottom: 10px"
                label-position="left"
              >
                <el-row>
                  <el-col :span="24">
                    <div>
                      <el-form-item label="业务流水号" prop="pfomBizNum">
                        <el-input
                          v-model="formInline.pfomBizNum"
                          disabled
                        ></el-input>
                      </el-form-item>
                      <el-form-item label="发起时间" prop="beginTime">
                        <el-input
                          v-model="formInline.beginTime"
                          disabled
                        ></el-input>
                      </el-form-item>
                      
                      <el-form-item label="产品名称" prop="fundName">
                        <select-table
                          v-show="!isFq"
                          v-model="formInline.fundName"
                          width="100%"
                          @sendDataObj='sendDataObj'
                        ></select-table>
                        <el-input
                          v-show="isFq"
                          v-model="formInline.fundName"
                          disabled
                        ></el-input>
                      </el-form-item>

                      <el-form-item label="报告类型" prop="checkedVals">
                        <el-radio-group
                          v-model="formInline.checkedVals"
                          class="margin_radio_label"
                          :disabled="isFq"
                        >
                          <el-radio
                            v-for="item in reportTypeArr"
                            :key="item.dimCde"
                            :label="item.dimCde"
                            >{{ item.dimNme }}</el-radio
                          >
                        </el-radio-group>
                      </el-form-item>
                      <el-form-item label="报告上报日期" prop="remark">
                        <el-date-picker
                          v-model="formInline.remark"
                          type="date"
                          editable
                          size="small"
                          value-format="yyyy-MM-dd"
                          placeholder="选择日期"
                          :disabled="isFq"
                        >
                        </el-date-picker>
                      </el-form-item>
                      <el-form-item
                        label="备注"
                        prop="cmdRemark"
                        style="margin-top: 10px"
                      >
                        <!-- :autosize='{minRows: 2, maxRows: 10}' -->
                        <el-input
                          type="textarea"
                          maxlength="1000"
                          show-word-limit
                          :autosize="{ minRows: 2 }"
                          placeholder="请输入内容"
                          v-model="formInline.cmdRemark"
                          :disabled="isFq"
                        >
                        </el-input>
                      </el-form-item>

                      <br />
                      <div class="el-form-item-div" style="padding: 10px 0">
                        <el-form-item
                          label="附件上传"
                          prop="fileList"
                          ref="fileList"
                        >
                          <el-upload
                            class="upload-demo"
                            v-model="formInline.fileList"
                            ref="upload"
                            :headers="hearders"
                            :action="fileUploadUrl"
                            :on-remove="handleRemove"
                            :on-preview="downFile"
                            :on-change="handleChange"
                            :file-list="formInline.fileList"
                            :disabled="isFq"
                            :auto-upload="false"
                          >
                            <el-button
                              style="margin-top: 40px"
                              slot="trigger"
                              :disabled="isFq"
                              v-if="!isFq"
                              size="small"
                              type="primary"
                              >浏览</el-button
                            >
                          </el-upload>
                        </el-form-item>
                      </div>
                      <div class="el-form-item-div" style="padding: 10px 0" v-if="fileList2.length">
                        <el-form-item
                          label="外包机构反馈公告"
                          prop="fileList2"
                          ref="fileList2"
                        >
                          <el-upload
                            class="upload-demo"
                            v-model="fileList2"
                            ref="upload"
                            :headers="hearders"
                            :action="fileUploadUrl"
                            :on-remove="handleRemove"
                            :on-preview="downFile"
                            :on-change="handleChange"
                            :file-list="fileList2"
                            disabled
                            :auto-upload="false"
                          >
                            <!-- <el-button
                              style="margin-top: 40px"
                              slot="trigger"
                              :disabled="isFq"
                              size="small"
                              type="primary"
                              >浏览</el-button
                            > -->
                          </el-upload>
                        </el-form-item>
                      </div>
                    </div>
                  </el-col>
                </el-row>
              </el-form>
            </div>
            <!-- table -->
            <div class="formStyle_table" style="margin-right: 0px">
              <el-table :data="tableList1" border max-height="400">
                <!-- <el-table-column type="index" width="50" header-align='cener' align="center" label="序号"></el-table-column>
                  <el-table-column min-width = "90" header-align="left" align="left" prop="account.userName" show-overflow-tooltip label="处理人"></el-table-column>
                  <el-table-column min-width = "90" header-align="left" align="left" prop="account.email" show-overflow-tooltip label="邮箱"></el-table-column>
                  <el-table-column min-width = "90" header-align="left" align="left" prop="account.phone" show-overflow-tooltip label="手机"></el-table-column>
                  <el-table-column min-width = "90" header-align="left" align="left" prop="taskName" show-overflow-tooltip label="任务节点"></el-table-column>
                  <el-table-column min-width = "90" header-align="left" align="left" prop="dateTime" show-overflow-tooltip label="处理时间"></el-table-column>
                  <el-table-column min-width = "90" header-align="left" align="left" prop="opinion" show-overflow-tooltip label="处理意见"></el-table-column> -->

                <el-table-column
                  type="index"
                  width="50"
                  header-align="cener"
                  align="center"
                  label="序号"
                ></el-table-column>
                <el-table-column
                  min-width="90"
                  header-align="left"
                  align="left"
                  prop="userName"
                  show-overflow-tooltip
                  label="处理人"
                ></el-table-column>
                <el-table-column
                  min-width="90"
                  header-align="left"
                  align="left"
                  prop="userEmail"
                  show-overflow-tooltip
                  label="邮箱"
                ></el-table-column>
                <el-table-column
                  min-width="90"
                  header-align="left"
                  align="left"
                  prop="userPhone"
                  show-overflow-tooltip
                  label="手机"
                ></el-table-column>
                <el-table-column
                  min-width="90"
                  header-align="left"
                  align="left"
                  prop="taskXmlName"
                  show-overflow-tooltip
                  label="任务节点"
                ></el-table-column>
                <el-table-column
                  min-width="90"
                  header-align="left"
                  align="left"
                  prop="operateTime"
                  show-overflow-tooltip
                  label="处理时间"
                ></el-table-column>
                <el-table-column
                  min-width="90"
                  header-align="left"
                  align="left"
                  prop="operateTypeName"
                  show-overflow-tooltip
                  label="操作"
                ></el-table-column>
                <el-table-column
                  min-width="90"
                  header-align="left"
                  align="left"
                  prop="userOpinion"
                  show-overflow-tooltip
                  label="处理意见"
                ></el-table-column>
              </el-table>
            </div>
          </div>
          <!-- yijian -->
          <div v-show="form_show" class="fixedBox" :style="fixStyle">
            <el-form
              ref="formHandle"
              :model="formHandle"
              label-position="left"
              class="fixefrom"
            >
              <el-form-item label="处理意见" prop="remark">
                <el-input
                  v-model="formHandle.remark"
                  type="textarea"
                  :autosize="{ minRows: 3 }"
                  maxlength="1000"
                  show-word-limit
                  placeholder="请输入处理意见"
                  auto-complete="off"
                >
                </el-input>
              </el-form-item>
            </el-form>
            <div
              style="margin-top: 10px"
              v-show="isCheckOver"
              class="fixefrom"
              tra="conduct"
            >
              <el-button
                v-if="$hasPermission('newConduct.update.Normal')"
                plain
                type="primary"
                size="medium"
                @click="updateStatus('formHandle', 'Normal', noraml_Name)"
                v-show="isPause"
                :loading="countSubmit_btn"
                >{{ noraml_Name }}</el-button
              >

              <el-button
                v-if="!isYwfq && $hasPermission('newConduct.update.Retire')"
                plain
                type="danger"
                size="medium"
                @click="updateStatus('formHandle', 'Retire', '退回')"
                v-show="isPause"
                :loading="countSubmit_btn"
                >退回</el-button
              >

              <el-button
                plain
                type="primary"
                v-if="$hasPermission(hasPermissionPause)"
                size="medium"
                v-show="isPause"
                @click="updateStatus('formHandle', 'Pause', '暂缓')"
                >暂缓</el-button
              >

              <el-button
                plain
                type="primary"
                v-if="$hasPermission(hasPermissionUnPause)"
                size="medium"
                v-show="!isPause"
                @click="updateStatus('formHandle', 'UnPause', '解除暂缓')"
                >解除暂缓</el-button
              >

              <el-button
                style="margin-top: 20px"
                v-if="$hasPermission(hasPermissionCancle)"
                v-show="isPause"
                plain
                type="warning"
                size="medium"
                @click="updateStatus('formHandle', 'Cancle', '撤销')"
                >撤销</el-button
              >

              <el-button
                plain
                type="info"
                v-if="$hasPermission(hasPermissionAbandon)"
                size="medium"
                v-show="isPause"
                @click="updateStatus('formHandle', 'Abandon', '作废')"
                >作废</el-button
              >
            </div>
          </div>
        </el-col>
      </el-row>
    </el-drawer>
  </div>
</template>
<script>
import selectTable from "@/views/commonComponents/selectTable.vue";
import commonFun from "@/filters/new_common";
import ModelDraer from "./drawer.js";
import drawerApi from "@/utils/transfer-drawer";
import bpmPage from "@/views/transfer/bpm/testBpm.vue";
// import synHandleApi from "@/api/synHandle/synHandle"; 
import synHandleApi from "@/api/conduct/newConduct";
import trackingAgentApi from "@/api/transfer/trackingAgentList";
import fun from "@/filters/common";
import commonApi from "@/api/common";
import cmCheckApi from "@/api/transfer/cmdCheck";
import $ from "jquery";
import { stepMenuBtn } from "@/utils/stepBtn";
export default {
  mixins: [ModelDraer],
  components: {
    bpmPage,
    selectTable,
  },
  data() {
    return {
      reportTypeArr:[],
      tableList1: [],
      fileList2:[],
      hasPermissionPause: "",
      hasPermissionUnPause: "",
      hasPermissionCancle: "",
      hasPermissionAbandon: "",
      isUserWBServer: false,
      hasWBServer: false,
      isPause: true,
      isYwfq: false,
      isCheckOver: false,
      activeIndex: null,
      processActive: false,
      formInline: {
        pfomBizNum: "",
        beginTime: "",
        fundName: "",
        cmdRemark: "",
        remark: "",
        fileList: [],
        checkedVals: "", //业务类型
      },
    };
  },
  methods: {
    sendDataObj(data) {
      
    },
    init(data) {
      // console.log("init", data);
      this.isCheckOver = false;
      // this.drawer = true;
      this.isPause = true;
      this.isYwfq = false;
      this.hasPermissionPause = "";
      this.hasPermissionUnPause = "";
      this.hasPermissionCancle = "";
      this.hasPermissionAbandon = "";
      this.defalutDataFrom = { ...this.formInline };
      this.form_show = data.isCheck;
      // this.form_show = true
      this.myTaskId = data.pfomTaskid; //用于处理处理按钮提交的id标识
      this.getViewDrawerInfo(data.pfomTaskid, data.cmdType); //获取整个drawer的基础信息

      //字典初始化
      this.getSelects("tempReport"); //获取报告类型

    },
    // 获取流程处理列表
    gettask(val) {
      let params = { procInstId: val };
      trackingAgentApi.getTaskcomment(params).then((res) => {
        if (res.data.status == 200) {
          this.tableList1 = res.data.data;
          // console.log("tableList1", this.tableList1);
        } else {
          this.tableList1 = [];
        }
        // console.log(res,'获取处理人列表');
      });
    },
    //获取整个drawer的基础信息
    getViewDrawerInfo(id, headNode) {
      trackingAgentApi
        .getResultDatas(id)
        .then(({ data: res }) => {
          // console.log('res', res)
          let obj = {
            pfomTaskid: id || "",
            beginTime: res.data.processInstance.processFormData.beginTime || "",
            titleName: res.data.name || "",
            stepData: res.data.processInstance.instanceId || "",
            bpmId: res.data.processInstance.porcessDefineModel.id || "",
            taskKey: res.data.xmlId || "",
            processKey: res.data.formData.cmdType || "",
            dataForm: { ...res.data.processInstance.processFormData } || {},
            tableList: res.data.taskOpinionModels || [],
            headNode: headNode,
            isActive: res.data.isActive || "",
          };
          // console.log(obj)
          this.getDataForm = obj;
          this.drawer = true;
          this.getStapeData(); //获取步骤的信息
          this.getDataInfo(); //处理标题信息
          this.getResultData(); // 表单的基本信息
          this.tableListInfo(); //列表信息
          this.getFileList(); // 获取文件列表信息
          this.getFileList2(); // 获取外包机构反馈公告
          this.getStapeDataUserInfo(); // 处理人信息
          // this.getProductInfo()  //选项信息
          this.gettask(obj.stepData);
          this.rightControl();
        })
        .catch((err) => {
          console.log("is msg err", err);
        });
    },
    // 按钮权限控制
    rightControl() {
      if (!this.getDataForm.isActive) {
        this.isPause = false;
      } else this.isPause = true;

      if (
        this.getDataForm.taskKey == "newConduct_ywfq" ||
        this.getDataForm.taskKey == "conremote_ywfq"
      ) {
        this.isYwfq = true;
      } else {
        this.isYwfq = false;
      }

      let dataBtn = {
        headNode: this.getDataForm.headNode,
        node: this.getDataForm.taskKey,
      };
      let btn = stepMenuBtn(dataBtn);
      // console.log(btn)
      this.hasPermissionPause = btn.hasPermissionPause;
      this.hasPermissionUnPause = btn.hasPermissionUnPause;
      this.hasPermissionCancle = btn.hasPermissionCancle;
      this.hasPermissionAbandon = btn.hasPermissionAbandon;

      // console.log(
      //   this.hasPermissionPause,
      //   this.hasPermissionUnPause,
      //   this.hasPermissionCancle,
      //   this.hasPermissionAbandon
      // );

      this.isCheckOver = true;
    },
    tableListInfo() {
      let data = [...this.getDataForm.tableList];
      for (let item of data) {
        item.dateTime = fun.timeFormat(item.dateTime);
      }
      this.tableList = data;
    },
    //获取步骤的信息
    getStapeData() {
      let data = this.getDataForm.stepData;
      synHandleApi
        .getStapeInfo(data)
        .then(({ data: res }) => {
          let temp = new Array();

          let curIndex = 0;
          let index = 0;

          for (let item of res.data) {
            if (item.isShow) {
              index = index + 1;
              let stepObj = new Object();
              if (item.taskStatus == "COMPLETED") {
                stepObj["des"] = "已完成";
                stepObj["status"] = "success";

                curIndex = index;
              } else if (item.taskStatus == "RUNNING") {
                stepObj["des"] = "当前处理";
                stepObj["status"] = "finish";

                this.taskXmlId = item.xmlId;
                this.processActive = true;
              } else if (item.taskStatus == "READY") {
                stepObj["des"] = "待执行";
                stepObj["status"] = "wait";
              } else if (item.taskStatus == "ABANDON") {
                stepObj["des"] = "已废弃";
                stepObj["status"] = "wait";
              } else if (item.taskStatus == "CANCLE") {
                stepObj["des"] = "已撤销";
                stepObj["status"] = "wait";
              } else {
                stepObj["des"] = "";
                stepObj["status"] = "wait";
              }
              stepObj["taskStatus"] = item.taskStatus;
              stepObj["xmlId"] = item.xmlId;
              stepObj["stepTitle"] = item.taskName;
              stepObj["step"] = item.taskIndex - 1;
              temp.push(stepObj);
            }
          }

          this.activeIndex = curIndex;

          this.stepData = temp;

          this.$nextTick(() => {
            this.$emit("dataInfo", res.data);
          });

          this.getStapeDataUserInfo(); // 处理人信息
        })
        .catch((err) => console.log("is msg err", err));
    },
    // 处理人信息
    getStapeDataUserInfo() {
      let data = {
        procInstId: this.getDataForm.stepData,
        // taskInstId: this.myTaskId
        taskXmlId: this.getDataForm.taskKey,
      };
      synHandleApi.getUsrINfo(data).then(({ data: res }) => {
        this.stepDataInofo = res.data;
      });
    },
    // 关闭drawer初始化数据
    closedDrawer() {
      this.isLeftInfo = false;
      this.form_show = false;
      this.tableList = [];
      this.bpmData = [];
      this.getDataForm = {};
      this.formHandle.remark = "";
      this.drawerSize = "50%";
      this.formInline = this.defalutDataFrom;
      this.$emit('closeD')
    },
    //处理标题信息
    getDataInfo() {
      // this.viewInfo = `${"流程详情" + "--"}`
      this.viewInfo = `${"流程详情"}`;
      this.inHandInfo = this.getDataForm.titleName; //用于标题
    },
    //选项信息
    getProductInfo() {
      synHandleApi.getProductInfo().then((res) => {
        this.fundNameArr = [];
        if (res.data.message === "success") {
          let arr = res.data.data;
          let temp = new Array();
          for (let i = 0; i < arr.length; i++) {
            let obj = {};
            obj.value = arr[i].fundCode;
            obj.name = arr[i].fundCode + "_" + arr[i].fundName;
            temp.push(obj);
          }
          this.fundNameArr = temp;
        } else {
          this.$message.closeAll();
          this.$message.error("查询产品信息失败");
        }
      });
    },
    // 获取文件列表信息
    getFileList() {
      let id = this.getDataForm.dataForm.id || "";
      synHandleApi
        .getFileList(id, "newConduct_file")
        .then((res) => {
          if (res.data.message === "success") {
            let arr = res.data.data;
            this.formInline.fileList = [];
            for (let i = 0; i < arr.length; i++) {
              let obj = {};
              obj.id = arr[i].id;
              obj.url = arr[i].fileUri;
              obj.name = arr[i].fileName;
              obj.size = arr[i].fileSize;
              this.formInline.fileList.push(obj);
            }
          }
          // console.log()
        })
        .catch(() => {});
    },
    getFileList2() {
      let id = this.getDataForm.dataForm.id || "";
      synHandleApi
        .getFileList(id, "other_file")
        .then((res) => {
          if (res.data.message === "success") {
            let arr = res.data.data;
            this.fileList2 = [];
            for (let i = 0; i < arr.length; i++) {
              let obj = {};
              obj.id = arr[i].id;
              obj.url = arr[i].fileUri;
              obj.name = arr[i].fileName;
              obj.size = arr[i].fileSize;
              this.fileList2.push(obj);
            }
          }
          // console.log()
        })
        .catch(() => {});
    },
    viewLcPic() {
      this.leftDrawer = true;
      let data = {
        id: this.getDataForm.bpmId,
        data: this.bpmData,
      };
      this.$nextTick(() => {
        this.$refs.bpm.init(data);
      });
    },
    infoLeader() {
      this.isLeftInfo = !this.isLeftInfo;
      if (this.isLeftInfo) {
        this.drawerSize = "80%";
        this.getInfoLeader();
      } else this.drawerSize = "50%";
    },
    // 查看交互
    getInfoLeader() {
      this.$message.closeAll();
      let data = {
        taskKey: this.getDataForm.taskKey || "",
        processKey: this.getDataForm.processKey || "",
      };
      commonApi
        .getHandleHtml(data)
        .then((res) => {
          if (res.data.status === 200) {
            if (res.data.data) {
              let html = res.data.data.html;
              $("#leftInfo").html(html);
            }
          } else {
            this.drawerSize = "50%";
            this.$message.error("查询失败");
          }
        })
        .catch(() => {});
    },
    stepClick(data) {
      if (!this.processActive) return;
      if (data && data.taskStatus == "RUNNING") {
        this.isViewStepInfo = true;
      } else {
        this.isViewStepInfo = false;
      }
    },
    //获取页面高度
    getViewINfoHW() {
      this.$nextTick(() => {
        let maxH =
          document.documentElement.clientHeight || document.body.clientHeight;
        let maxw =
          document.documentElement.clientWidth || document.body.clientWidth;
        this.fixStyle.width = maxw / 2 + "px";
      });
    },

  },
  mounted() {
    this.getViewINfoHW();
    window.onresize = () => {
      this.getViewINfoHW();
    };
    // console.log('aaaa');
    this.drawer = true;
  },
};
</script>
<style lang='scss'>
//  多选框勾选颜色
 .rightDrawerStyle_conductNew{
   .el-radio-group{
     .is-checked{
       .el-radio__label{
         color: #409EFF;
       }
     }
   }
   .is-checked{
    .el-checkbox__label{
      color: #409EFF !important;
    }
  }
 }
.el-upload-list__item.is-success.focusing .el-icon-close-tip {
  display: none !important;
}

.rightDrawerStyle {
  .margin_radio_label{
    .el-radio{
      margin-top: 10px;
      margin-bottom: 10px;
      .el-radio__label{
        font-size: 14px !important;
      }
    }
  }
  .el-form-item__content {
    min-width: 95%;
    .el-form-item__error {
      width: 300px;
    }
  }
  .el_form_item {
    width: auto;
  }
  .el-form-conduct .el-form-item__label {
    text-align: left;
  }
  .el-form-conduct .el-form-item-conduct {
    padding-left: 40px;
  }
  .movePlace {
    overflow: none;
    .stepRowName_style {
      font-weight: 600;
      margin-bottom: 10px;
    }
    .borderLine {
      width: 100%;
      margin: 8px auto;
      border-bottom: 1px dashed #409eff;
    }
    .solidStyle {
      margin: 5px auto;
      border-bottom: 1px solid #409eff !important;
    }
  }
  .el-drawer__body {
    overflow-y: auto;
  }
  .mainBox {
    padding-bottom: 250px;
    width: 98%;
  }
  .bigSize {
    font-size: 20px;
    cursor: pointer;
    &:hover {
      font-weight: 600;
    }
  }
  .titleStyle {
    margin: 20px 0 20px 20px;
  }
  .steps_zhyw {
    // width: 96%;
    // margin: 0 auto;
    margin-left: 21px;
    margin-right: 0;
  }
  .formStyle {
    width: 80%;
    margin: 10px auto;
  }
  .formStyle_table {
    width: 91%;
    margin: 10px auto;
  }
  .fixedBox {
    height: 240px;
    z-index: 999;
    overflow-y: auto;
    padding-bottom: 20px;
    background-color: #fff;
  }
  .fixefrom {
    width: 95%;
    margin: 0 auto;
  }
  .btnStyle {
    margin: 10px 0 20px 20px;
  }
}
</style>
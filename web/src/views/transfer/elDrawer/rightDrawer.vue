<template>
  <div class="rightDrawerStyle">
    <el-drawer
      title="标题"
      :size="drawerSize"
      :visible.sync="drawer"
      :with-header="false"
      @closed='closedDrawer'
      show-close>
      <el-row style=" height: 100%;">
        <!-- 查看交互指引 -->
        <el-col :span='9' v-if="isLeftInfo" style="height:100%;overflow:hidden;overflow-y:auto">
          <div ref="leftInfo" v-show="isLeftInfo" id="leftInfo" class="titleStyle"></div>
        </el-col>
        <!-- 划款指令表格 -->
        <el-col :span='12' v-if="hkzl_show" style="height:100%;overflow:hidden;overflow-y:auto">
          <!-- <keep-alive></keep-alive> -->
          <div class="titleStyle hkzl_box"><HkzlDrawer ref="HkzlDrawer" :fundCode='fundCode' :tableData='tableData' :oldForm='oldForm' :activeIndex='activeIndex'/></div>
        </el-col>
        <!-- 管理人经办节点-编辑表单 -->
        <el-col :span="12" v-if="edit_form" style="height:100%;overflow:hidden;overflow-y:auto">
          <!-- <div>表单</div> -->
          <div style="padding:50px 80px 20px 50px;">
            <edit-form ref="editForm" :formData="editFormData" :fileList="fileList" />
          </div>
        </el-col>
        <el-col :span="mainBox_span" style="height:100%;overflow:hidden;overflow-y:auto">
        <!-- <el-col :span="isLeftInfo ? 15 : 24"> -->
          <div v-if="zhxx_show" style="height:100%;padding: 0 20px">
           <!-- <p> 账户信息 <el-button @click="zhxx_show=false">X</el-button> </p> -->
           <p class="yulan_title"> <span class="yulan_title_name">账户信息</span><span style="font-size:20px;color:#000;cursor: pointer;"><i @click="closeZhxx" class="el-icon-close"></i></span> </p>
           
            <!-- <mj-form/> -->
            <!-- <tg-form/> -->
            <!-- <ymtForm/> -->
            <qhzh-form v-if="qh_show" ref="AccountInfo"/>
            <zq-form v-if="zq_show" ref="AccountInfo"/>
            <qt-form v-if="qt_show" ref="AccountInfo"/>
            <yhj-form v-if="yhj_show" ref="AccountInfo"/>
            <tg-form v-if="tg_show" ref="AccountInfo"/>
            <ZdyAccountInfo v-if="zdy_show" ref="AccountInfo"/>
          </div>
          <div v-if="fjyl_show" style="height:100%;padding: 0 20px">
            <p class="yulan_title"> <span class="yulan_title_name">附件预览</span><span style="font-size:20px;color:#000;cursor: pointer;"><i @click="closePdfPreview" class="el-icon-close"></i></span> </p>
            <PdfPreview :urlArr='fileList' :PreviewFileId="PreviewFileId" style="width:100%;height:100%" ref="PdfPreview"></PdfPreview>
          </div>
           <div class="mainBox" v-if="!zhxx_show&&!fjyl_show" style="height:100%">
             <!-- titel -->
             <div class="titleStyle">
              <el-row>
                <el-col :span='22' >
                  <span style="color: #409eff">
                    {{ viewInfo }}
                    <!-- <span style="color: red">{{ inHandInfo }}</span> -->
                  </span>
                </el-col>
                <el-col :span="2">
                  <span class="el-icon-close bigSize" @click="drawer=false"></span>
                </el-col>
              </el-row>

             </div>
              <!-- step success finish-->
              <div class="steps_hk" @mouseleave="isViewStepInfo = false">
				  <el-steps :active="activeIndex" finish-status="success" >
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
                    <div style="margin-bottom:10px; font-weight:600; color: #409EFF">
                      <el-row>
                        <el-col :span="8">待办人</el-col>
                        <el-col :span="8">联系电话</el-col>
                        <el-col :span="8">邮箱</el-col>
                      </el-row>
                      <div class="solidStyle"></div>
                    </div>
                    <div class="rightDrawerStyle_table" v-for="(item, index) in stepDataInofo" :key="index + 'man'" style="color: #409EFF">
                      <el-row>
                        <el-col :title='item.userName' :span="8">{{item.userName || '-'}}</el-col>
                        <el-col :title='item.userPhone' :span="8">{{item.userPhone || '-'}}</el-col>
                        <el-col :title='item.userEmail' :span="8">{{item.userEmail || '-'}}</el-col>
                      </el-row>
                      <div><div class="borderLine"></div></div>
                    </div>
                  </el-card>
                </div>
              </div>
              <!-- buton -->
              <div class="btnStyle">
                <el-button type="primary" size="small" @click="viewLcPic">查看流程图</el-button>
                <el-button type="primary" size="small" @click="infoLeader">查看交互指引</el-button>
                <el-button type="primary" size="small" @click="hkzl">划款指令</el-button>
                <!-- <el-button type="primary" size="small" @click="preview">附件预览</el-button> -->
                <el-button type="primary" size="small" @click="zh_info">账户信息</el-button>
                <!-- 指令编辑 -->
                <el-button type="primary" size="small" @click="edit_glrjb" v-if="zl_edit_show || fh_edit_show">指令编辑</el-button> 
                <!-- <el-button type="primary" size="small" @click="edit_" v-if="edit_show">{{butTxt}}</el-button>  -->
                <!-- 自定义划款-编辑 -->
                <el-button type="primary" size="small" @click="edit_1" v-if="edit_show">指令编辑</el-button> 
                <!-- 管理人复核阶段-编辑 -->
                <!-- <el-button type="primary" size="small" @click="edit_1" v-if="fh_edit_show">编辑</el-button>  -->
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
              
              <!-- <el-drawer
                custom-class='hkzlyl'
                title="划款指令预览"
                :append-to-body="true"
                direction="ltr"
                size="50%"
                style="overflow-x: auto"
                :visible.sync="leftDrawer2"
              >
              <HkzlDrawer/>
              </el-drawer> -->
              
              <!-- from -->
              <div class="formStyle" style="margin-right:100px">
                <el-form
                  label-position="right"
                  label-width="110px"
                  ref="formInline"
                  :rules="formInlineRules"
                  :model="formInline">
                  <el-form-item label="指令类型">
                    <el-input v-model="cmdCodeName" disabled></el-input>
                  </el-form-item>
                  <el-form-item prop="pfomBizNum" label="指令编号">
                      <el-input v-model="formInline.pfomBizNum" disabled></el-input>
                  </el-form-item>
                  <el-form-item prop="beginTime" label="发起时间">
                    <el-input v-model="formInline.beginTime" disabled></el-input>
                  </el-form-item>
                  <el-row>
                    <el-col :span='24'>
                    <el-form-item label="科目数截止日期" v-if="cmdType=='pay'" prop="subjectDeadlineAt" :class="[back_show?oldForm.subjectDeadlineAt==formInline.subjectDeadlineAt?'':'change_red':'']">
                      <el-tooltip placement="top-start" :disabled="back_show?oldForm.subjectDeadlineAt==formInline.subjectDeadlineAt?true:false:true">
                      <div slot="content">修改前:{{oldForm.subjectDeadlineAt}} </div>
                        <el-date-picker
                          style="width:100%"
                          v-model="formInline.subjectDeadlineAt"
                          type="date"
                          :disabled='!isedit'
                          :picker-options="pickerOptions"
                          value-format="yyyy-MM-dd"
                          placeholder="选择日期">
                        </el-date-picker>
                      </el-tooltip>
                      </el-form-item>
                    </el-col>

                    <el-col :span='24'>
                    <el-form-item label="要求划款日期" prop="transferReqdate" :class="[back_show?oldForm.transferReqdate==formInline.transferReqdate?'':'change_red':'']">
                      <el-tooltip placement="top-start" :disabled="back_show?oldForm.transferReqdate==formInline.transferReqdate?true:false:true">
                      <div slot="content">修改前:{{oldForm.transferReqdate}} </div>
                        <el-date-picker
                          style="width:100%"
                          v-model="formInline.transferReqdate"
                          type="date"
                          :disabled='!isedit'
                          :picker-options="pickerOptions"
                          value-format="yyyy-MM-dd"
                          placeholder="选择日期">
                        </el-date-picker>
                      </el-tooltip>
                      </el-form-item>
                    </el-col>
                    <el-col :span='24'>
                      <!-- <el-form-item label="产品" prop="fundCode" class="change_red">
                        <el-select
                          style="width:100%"
                          :disabled='!isedit'
                          v-model="formInline.fundCode"
                          placeholder="请选择">
                          <el-option
                            v-for="(item, index) in accountCodes"
                            :key="index + 'acc'"
                            :label="item.name"
                            :value="item.value">
                          </el-option>
                        </el-select>
                      </el-form-item> -->
                      <!-- v-if="cmdCode=='gm050106'" -->
                      <el-form-item label="" prop="noTransaction" v-if="cmdCode=='gm050106'">
                        <el-checkbox 
                          v-model="formInline.noTransaction"
                          true-label="1"
                          false-label="0"
                          :disabled='!isedit'
                        >无指令成交单</el-checkbox>
                        <el-tooltip class="item" effect="light" content="" placement="right">
                          <div slot="content">无需向托管传输划款指令，请区分产品分别上传银行间成交单</div>
                          <i class="el-icon-warning"></i>
                        </el-tooltip>
                      </el-form-item>
                      <el-form-item label="产品" prop="fundCode" :class="[back_show?oldForm.fundCode==formInline.fundCode?'':'change_red':'']">
                        <select-table v-show="isedit" v-model="formInline.fundCode" @sendDataObj='sendDataObj'></select-table>
                        <el-tooltip placement="top-start" :disabled="back_show?oldForm.fundCode==formInline.fundCode?true:false:true">
                        <div slot="content">修改前:{{oldForm.fundCode}} </div>
                        <el-input
                        v-show="!isedit"
                        :disabled='!isedit'
                         v-model="formInline.fundCode"
                         style="width:100%"
                        ></el-input>
                        </el-tooltip>
                      </el-form-item>
                    </el-col>
                    <!-- 股票/证券代码展示 -->
                    <el-col :span="24">
                      <el-form-item
                      :class="[back_show?oldForm.stockCode==formInline.stockCode?'':'change_red':'']"
                       v-if="(cmdCode=='gm050103'||cmdCode=='gm050104')&&cmdType=='invest'" prop="stockCode" label="股票/债券代码">
                       <el-tooltip placement="top-start" :disabled="back_show?oldForm.stockCode==formInline.stockCode?true:false:true">
                        <div slot="content">修改前:{{oldForm.stockCode}} </div>
                        <el-input v-model="formInline.stockCode" maxlength="66" :disabled='!isedit'></el-input>
                       </el-tooltip>
                      </el-form-item>
                    </el-col>
                  </el-row>
                  <el-row>
                    <el-col :span="24">
                      <el-form-item label='经纪商'
                      v-if="cmdType=='transfer' && !['gm040601','gm040602','gm040603','gm040701','gm040702','gm040703','gm040704','gm040705','gm040706'].includes(cmdCode)"
                      :class="[back_show?oldForm.brokerCode==formInline.brokerCode?'':'change_red':'']"
                        prop="brokerCode">
                        <el-tooltip placement="top-start" :disabled="back_show?oldForm.brokerCode==formInline.brokerCode?true:false:true">
                        <div slot="content">修改前:{{oldForm.brokerCode}} </div>
                        <el-select style="width: 100%"
                          v-if="['gm040101','gm040102','gm040201','gm040202','gm040203'].includes(cmdCode)"
                         filterable clearable 
                         v-model="formInline.brokerCode" 
                         :disabled='!isedit'
                         placeholder="请选择" 
                         class="el_form_item">
                          <el-option
                            v-for="(item, index) in borkerInfos"
                            :key="index + 'broker'"
                            :label="item.name"
                            :value="item.value">
                          </el-option>
                        </el-select>
                        <el-input
                        v-else
                        :disabled='!isedit'
                         v-model="formInline.brokerCode"
                         style="width:100%"
                         maxlength="134"
                        ></el-input>
                        </el-tooltip>
                      </el-form-item>
                    </el-col>
                    <!-- 收款方账户展示["040101","040102"]transfer -->
                    <!-- <el-col :span="24">
                      <el-form-item
                      :class="[back_show?oldForm.payeeAccount==formInline.payeeAccount?'':'change_red':'']"
                       v-if="(cmdCode=='040101'||cmdCode=='040102')&&cmdType=='transfer'" label="收款方账户" prop="payeeAccount">
                        <el-tooltip placement="top-start" :disabled="back_show?oldForm.payeeAccount==formInline.payeeAccount?true:false:true">
                        <div slot="content">修改前:{{oldForm.payeeAccount}} </div>
                        <el-input
                          v-model="formInline.payeeAccount"
                          type="text"
                          maxlength="66"
                          :disabled='!isedit'>
                        </el-input>
                        </el-tooltip>
                      </el-form-item>
                    </el-col> -->
                    <!-- <el-col :span="24">
                      <el-form-item label="销售机构选择"
                        prop="fundSalerName"
                        :class="[back_show?oldForm.fundSalerName==formInline.fundSalerName?'':'change_red':'']"
                        v-if="cmdCode=='050101'&&cmdType=='invest'">
                        <el-tooltip placement="top-start" :disabled="back_show?oldForm.fundSalerName==formInline.fundSalerName?true:false:true">
                        <div slot="content">修改前:{{oldFundSalerName}} </div>
                        <el-select
                          style="width:100%"
                          v-model="formInline.fundSalerName"
                          placeholder="请选择"
                          :disabled='!isedit'>
                          <el-option
                            v-for="item in saleMechanisms"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                          </el-option>
                        </el-select>
                        </el-tooltip>
                      </el-form-item>
                    </el-col> -->
                  </el-row>
                  <el-row>
                    <!-- <el-col :span="24">
                      <el-form-item label="定存银行选择"
                        prop="depositBankName"
                        :class="[back_show?oldForm.depositBankName==formInline.depositBankName?'':'change_red':'']"
                        v-if="cmdCode=='050102'&&cmdType=='invest'">
                        <el-tooltip placement="top-start" :disabled="back_show?oldForm.depositBankName==formInline.depositBankName?true:false:true">
                        <div slot="content">修改前:{{oldDepositBankName}} </div>
                        <el-select
                          style="width:100%"
                          v-model="formInline.depositBankName"
                          placeholder="请选择"
                          :disabled='!isedit'>
                          <el-option
                            v-for="item in bankArr"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                          </el-option>
                        </el-select>
                        </el-tooltip>
                      </el-form-item>
                    </el-col> -->

                    <!-- 收款账户展示 -->
                    <el-col :span="24">
                      <el-form-item
                      :class="[back_show?oldForm.payeeAccount==formInline.payeeAccount?'':'change_red':'']"
                       v-if="cmdType=='ta'" label="收款账户" prop="payeeAccount">
                        <el-tooltip placement="top-start" :disabled="back_show?oldForm.payeeAccount==formInline.payeeAccount?true:false:true">
                        <div slot="content">修改前:{{oldForm.payeeAccount}} </div>
                        <el-input
                          v-model="formInline.payeeAccount"
                          type="text"
                          maxlength="66"
                          :disabled='!isedit'>
                        </el-input>
                        </el-tooltip>
                      </el-form-item>
                    </el-col>
                    <!-- 付款账户展示 -->
                    <el-col :span="24">
                      <el-form-item
                      :class="[back_show?oldForm.payerAccount==formInline.payerAccount?'':'change_red':'']"
                       v-if="cmdType=='ta'" label="付款账户" prop="payerAccount">
                        <el-tooltip placement="top-start" :disabled="back_show?oldForm.payerAccount==formInline.payerAccount?true:false:true">
                        <div slot="content">修改前:{{oldForm.payerAccount}} </div>
                        <el-input
                          v-model="formInline.payerAccount"
                          type="text"
                          maxlength="66"
                          :disabled='!isedit'>
                        </el-input>
                        </el-tooltip>
                      </el-form-item>
                    </el-col>
                    <el-col :span="24">
                      <el-form-item label="转账金额(元)" prop="transferAmount" :class="[back_show?oldForm.transferAmount==formInline.transferAmount?'':'change_red':'']">
                        <el-tooltip placement="top-start" :disabled="back_show?oldForm.transferAmount==formInline.transferAmount?true:false:true">
                        <div slot="content">修改前:{{oldForm.transferAmount}} </div>
                        <el-input
                          v-model="formInline.transferAmount"
                          @focus="moneyFocus"
                          @blur="moneyBlur"
                          type="text"
                          :disabled='!isedit'>
                        </el-input>
                        </el-tooltip>
                      </el-form-item>
                    </el-col>
                    <!-- 收/付款7要素 -->
                    <el-col :span="24" v-if="account_show" >
                      <el-form-item label="付款人" prop="payerAcconame" :class="[back_show?oldForm.payerAcconame==formInline.payerAcconame?'':'change_red':'']">
                        <el-tooltip placement="top-start" :disabled="back_show?oldForm.payerAcconame==formInline.payerAcconame?true:false:true">
                        <div slot="content">修改前:{{oldForm.payerAcconame}} </div>
                        <!-- <el-input
                          v-model="formInline.payerAcconame"
                          type="text"
                          maxlength="66"
                          :disabled='!isedit'>
                        </el-input> -->
                        <selectAccount
                          v-model="formInline.payerAcconame"
                          @sendDataObj="getAccountInfo1"
                          :disabled="!isedit"
                          ref="selectAccount1"
                        ></selectAccount>
                        </el-tooltip>
                      </el-form-item>
                    <!-- </el-col>
                    <el-col :span="24"> -->
                      <el-form-item
                      :class="[back_show?oldForm.payerAccount==formInline.payerAccount?'':'change_red':'']"
                       label="付款账号" prop="payerAccount">
                        <el-tooltip placement="top-start" :disabled="back_show?oldForm.payerAccount==formInline.payerAccount?true:false:true">
                        <div slot="content">修改前:{{oldForm.payerAccount}} </div>
                        <el-input
                          v-model="formInline.payerAccount"
                          type="text"
                          maxlength="66"
                          :disabled='true'>
                        </el-input>
                        </el-tooltip>
                      </el-form-item>
                    <!-- </el-col>
                    <el-col :span="24"> -->
                      <el-form-item
                      :class="[back_show?oldForm.payerBank==formInline.payerBank?'':'change_red':'']"
                       label="付款行" prop="payerBank">
                        <el-tooltip placement="top-start" :disabled="back_show?oldForm.payerBank==formInline.payerBank?true:false:true">
                        <div slot="content">修改前:{{oldForm.payerBank}} </div>
                        <el-input
                          v-model="formInline.payerBank"
                          type="text"
                          maxlength="66"
                          :disabled='true'>
                        </el-input>
                        </el-tooltip>
                      </el-form-item>
                    <!-- </el-col>
                    <el-col :span="24"> -->
                      <el-form-item
                      :class="[back_show?oldForm.payeeAcconame==formInline.payeeAcconame?'':'change_red':'']"
                       label="收款人" prop="payeeAcconame">
                        <el-tooltip placement="top-start" :disabled="back_show?oldForm.payeeAcconame==formInline.payeeAcconame?true:false:true">
                        <div slot="content">修改前:{{oldForm.payeeAcconame}} </div>
                        <!-- <el-input
                          v-model="formInline.payeeAcconame"
                          type="text"
                          maxlength="66"
                          :disabled='!isedit'>
                        </el-input> -->
                        <selectAccount
                          v-model="formInline.payeeAcconame"
                          @sendDataObj="getAccountInfo2"
                          :disabled="!isedit"
                          ref="selectAccount2"
                        ></selectAccount>
                        </el-tooltip>
                      </el-form-item>
                    <!-- </el-col>
                    <el-col :span="24"> -->
                      <el-form-item
                      :class="[back_show?oldForm.payeeAccount==formInline.payeeAccount?'':'change_red':'']"
                       label="收款账号" prop="payeeAccount">
                        <el-tooltip placement="top-start" :disabled="back_show?oldForm.payeeAccount==formInline.payeeAccount?true:false:true">
                        <div slot="content">修改前:{{oldForm.payeeAccount}} </div>
                        <el-input
                          v-model="formInline.payeeAccount"
                          type="text"
                          maxlength="66"
                          :disabled='true'>
                        </el-input>
                        </el-tooltip>
                      </el-form-item>
                    <!-- </el-col>
                    <el-col :span="24"> -->
                      <el-form-item
                      :class="[back_show?oldForm.payeeBank==formInline.payeeBank?'':'change_red':'']"
                       label="收款行" prop="payeeBank">
                        <el-tooltip placement="top-start" :disabled="back_show?oldForm.payeeBank==formInline.payeeBank?true:false:true">
                        <div slot="content">修改前:{{oldForm.payeeBank}} </div>
                        <el-input
                          v-model="formInline.payeeBank"
                          type="text"
                          maxlength="66"
                          :disabled='true'>
                        </el-input>
                        </el-tooltip>
                      </el-form-item>
                    <!-- </el-col>
                    <el-col :span="24"> -->
                      <el-form-item
                      :class="[back_show?oldForm.paymentSystemNumber==formInline.paymentSystemNumber?'':'change_red':'']"
                       label="支付系统号" prop="paymentSystemNumber">
                        <el-tooltip placement="top-start" :disabled="back_show?oldForm.paymentSystemNumber==formInline.paymentSystemNumber?true:false:true">
                        <div slot="content">修改前:{{oldForm.paymentSystemNumber}} </div>
                        <el-input
                          v-model="formInline.paymentSystemNumber"
                          type="text"
                          maxlength="50"
                          :disabled='true'>
                        </el-input>
                        </el-tooltip>
                      </el-form-item>
                    </el-col>
                    <!-- 收款4要素 -->
                    <el-col :span="24" v-if="payeeAcc_show">
                      <el-form-item
                      :class="[back_show?oldForm.payeeAcconame==formInline.payeeAcconame?'':'change_red':'']"
                       label="收款人" prop="payeeAcconame">
                        <el-tooltip placement="top-start" :disabled="back_show?oldForm.payeeAcconame==formInline.payeeAcconame?true:false:true">
                        <div slot="content">修改前:{{oldForm.payeeAcconame}} </div>
                        <el-input
                          v-model="formInline.payeeAcconame"
                          type="text"
                          maxlength="66"
                          :disabled='!isedit'>
                        </el-input>
                        </el-tooltip>
                      </el-form-item>
                      <el-form-item
                      :class="[back_show?oldForm.payeeAccount==formInline.payeeAccount?'':'change_red':'']"
                       label="收款账号" prop="payeeAccount">
                        <el-tooltip placement="top-start" :disabled="back_show?oldForm.payeeAccount==formInline.payeeAccount?true:false:true">
                        <div slot="content">修改前:{{oldForm.payeeAccount}} </div>
                        <el-input
                          v-model="formInline.payeeAccount"
                          type="text"
                          maxlength="66"
                          :disabled='!isedit'>
                        </el-input>
                        </el-tooltip>
                      </el-form-item>
                      <el-form-item
                      :class="[back_show?oldForm.payeeBank==formInline.payeeBank?'':'change_red':'']"
                       label="收款行" prop="payeeBank">
                        <el-tooltip placement="top-start" :disabled="back_show?oldForm.payeeBank==formInline.payeeBank?true:false:true">
                        <div slot="content">修改前:{{oldForm.payeeBank}} </div>
                        <el-input
                          v-model="formInline.payeeBank"
                          type="text"
                          maxlength="66"
                          :disabled='!isedit'>
                        </el-input>
                        </el-tooltip>
                      </el-form-item>
                      <el-form-item
                      :class="[back_show?oldForm.paymentSystemNumber==formInline.paymentSystemNumber?'':'change_red':'']"
                       label="支付系统号" prop="paymentSystemNumber">
                        <el-tooltip placement="top-start" :disabled="back_show?oldForm.paymentSystemNumber==formInline.paymentSystemNumber?true:false:true">
                        <div slot="content">修改前:{{oldForm.paymentSystemNumber}} </div>
                        <el-input
                          v-model="formInline.paymentSystemNumber"
                          type="text"
                          maxlength="50"
                          :disabled='!isedit'>
                        </el-input>
                        </el-tooltip>
                      </el-form-item>
                    </el-col>
                  </el-row>
                  <el-form-item
                  :class="[back_show?oldForm.processUse==formInline.processUse?'':'change_red':'']"
                   label="用途" prop="processUse" v-if="cmdType=='custom_demo'">
                    <el-tooltip placement="top-start" :disabled="back_show?oldForm.processUse==formInline.processUse?true:false:true">
                    <div slot="content">修改前:{{oldForm.processUse}} </div>
                    <el-input
                      v-model="formInline.processUse"
                      name="processUse"
                      type="textarea"
                      maxlength="1000"
                      show-word-limit
                      :disabled='!isedit'
                      :autosize='{ minRows: 2}'>
                    </el-input>
                    </el-tooltip>
                  </el-form-item>
                  <el-form-item
                  :class="[back_show?oldForm.remark==formInline.remark?'':'change_red':'']"
                   label="备注" prop="remark">
                    <el-tooltip placement="top-start" :disabled="back_show?oldForm.remark==formInline.remark?true:false:true">
                    <div slot="content">修改前:{{oldForm.remark}} </div>
                    <el-input
                      v-model="formInline.remark"
                      name="remark"
                      type="textarea"
                      maxlength="1000"
                      show-word-limit
                      :disabled='!isedit'
                      :autosize='{ minRows: 2}'>
                    </el-input>
                    </el-tooltip>
                  </el-form-item>
                  <el-form-item label="附件" prop="file">
                    <el-upload
                      :disabled='!isedit'
                      class="upload-demo"
                      ref="upload"
                      action="https://jsonplaceholder.typicode.com/posts/"
                      :on-preview="handlePreview"
                      :on-change="handleChange"
                      :on-remove="handleRemove"
                      :file-list="fileList"
                      :auto-upload="false">
                      <el-button slot="trigger" size="small" type="primary" v-if="isedit">选取文件</el-button>
                    </el-upload>
                  </el-form-item>
                </el-form>
              </div>
              <!-- table -->
              <!-- <div class="formStyle">
                <el-table :data="tableList" border max-height="400">
                  <el-table-column type="index" width="50" header-align='cener' align="center" label="序号"></el-table-column>
                  <el-table-column min-width = "90" header-align="left" align="left" prop="account.userName" show-overflow-tooltip label="处理人"></el-table-column>
                  <el-table-column min-width = "90" header-align="left" align="left" prop="account.email" show-overflow-tooltip label="邮箱"></el-table-column>
                  <el-table-column min-width = "90" header-align="left" align="left" prop="account.phone" show-overflow-tooltip label="手机"></el-table-column>
                  <el-table-column min-width = "90" header-align="left" align="left" prop="taskName" show-overflow-tooltip label="任务节点"></el-table-column>
                  <el-table-column min-width = "90" header-align="left" align="left" prop="dateTime" show-overflow-tooltip label="处理时间"></el-table-column>
                  <el-table-column min-width = "90" header-align="left" align="left" prop="opinion" show-overflow-tooltip label="处理意见"></el-table-column>
                </el-table>
              </div> -->
              <div class="formStyle_table" style="margin-right:20px">
                <el-table :data="tableList1" border max-height="400">
                  <el-table-column type="index" width="50" header-align='cener' align="center" label="序号"></el-table-column>
                  <el-table-column min-width = "90" header-align="left" align="left" prop="userName" show-overflow-tooltip label="处理人"></el-table-column>
                  <el-table-column min-width = "90" header-align="left" align="left" prop="userEmail" show-overflow-tooltip label="邮箱"></el-table-column>
                  <el-table-column min-width = "90" header-align="left" align="left" prop="userPhone" show-overflow-tooltip label="手机"></el-table-column>
                  <el-table-column min-width = "90" header-align="left" align="left" prop="taskXmlName" show-overflow-tooltip label="任务节点"></el-table-column>
                  <el-table-column min-width = "90" header-align="left" align="left" prop="operateTime" show-overflow-tooltip label="处理时间"></el-table-column>
                  <el-table-column min-width = "90" header-align="left" align="left" prop="operateTypeName" show-overflow-tooltip label="操作"></el-table-column>
                  <el-table-column min-width = "90" header-align="left" align="left" prop="userOpinion" show-overflow-tooltip label="处理意见"></el-table-column>
                </el-table>
              </div>
              <div style="height:250px"></div>
           </div>
            <!-- yijian -->
            <div v-if="!zhxx_show&&!fjyl_show" v-show="form_show" class="fixedBox" :style="fixStyle">
              <el-form ref="formHandle" :model="formHandle" label-position="left" class="fixefrom">
                  <el-form-item label="处理意见" prop="remark">
                      <el-input
                          v-model="formHandle.remark"
                          type="textarea"
                          :autosize='{ minRows: 3 }'
                          maxlength="200"
                          show-word-limit
                          placeholder="请输入处理意见"
                          auto-complete="off">
                      </el-input>
                  </el-form-item>
                </el-form>
                <div  style="margin-top:10px"  class="fixefrom" v-show="isCheckOver" tra="transfer">
				
                  <!-- $hasPermission('transfer.update.Normal') -->
                  <!-- <el-button v-if="isUser" plain type="primary" size="medium" @click="updateStatus('formHandle','Normal','同意')">同意</el-button>
                  <el-button v-if="isUser" plain type="info" size="medium" @click="updateStatus('formHandle','Retire','退回')">退回</el-button>
                  <el-button v-if="!isUser" plain  type="primary" size="medium" @click="updateStatus('formHandle',0,'划款成功')">划款成功</el-button>
                  <el-button v-if="!isUser" plain  type="primary" size="medium" @click="updateStatus('formHandle',1,'划款失败')">划款失败</el-button>
                  <el-button v-if="$hasPermission('transfer.update.Pause')" plain type="primary" v-show="isPause" size="medium" @click="updateStatus('formHandle','Pause','暂缓')">暂缓</el-button>
                  <el-button v-if="$hasPermission('transfer.update.UnPause')" plain type="primary" v-show="!isPause" size="medium" @click="updateStatus('formHandle','UnPause','解除暂缓')">解除暂缓</el-button>
                  <el-button v-if="$hasPermission('transfer.update.Cancle')" plain type="warning" size="medium" @click="updateStatus('formHandle','Cancle','撤销')">撤销</el-button>
                  <el-button v-if="$hasPermission('transfer.update.Abandon')" plain type="info" size="medium" @click="updateStatus('formHandle','Abandon','作废')">作废</el-button>
                  <div>下面测试</div> -->
                  <!-- <menu-btn ref="menuBtnRelation" v-show="menuBtnShow" @refashBtn='refashBtn'></menu-btn> -->
				  
				  
                  <div v-if="cmdType!='custom_demo'">
                  <el-button v-show="isPause && isUser" plain type="primary" size="medium" @click="duibizhilingbianji('formHandle','Normal','同意')">同意</el-button>
                  <el-button v-show="isPause && isUser" v-if="backBtn_show" plain type="info" size="medium" @click="formInlineValid('formHandle','Retire','退回')">退回</el-button>
                  <el-button v-show="isPause && !isUser" plain  type="primary" size="medium" @click="updateStatus('formHandle',0,cmdCode=='gm050106'?'交收成功':'划款成功')">{{cmdCode=='gm050106'?'交收成功':'划款成功'}}</el-button>
                  <el-button v-show="isPause && !isUser" plain  type="primary" size="medium" @click="updateStatus('formHandle',1,cmdCode=='gm050106'?'交收失败':'划款失败')">{{cmdCode=='gm050106'?'交收失败':'划款失败'}}</el-button>
                  <el-button v-if="$hasPermission(hasPermissionPause)" plain type="primary" v-show="isPause" size="medium" @click="formInlineValid('formHandle','Pause','暂缓')">暂缓</el-button>
                  <el-button v-if="$hasPermission(hasPermissionUnPause)" plain type="primary" v-show="!isPause" size="medium" @click="formInlineValid('formHandle','UnPause','解除暂缓')">解除暂缓</el-button>
                  <el-button v-if="$hasPermission(hasPermissionCancle)" plain type="warning" v-show="isPause" size="medium" @click="updateStatus('formHandle','Cancle','撤销')">撤销</el-button>
                  <el-button v-if="$hasPermission(hasPermissionAbandon)" plain type="info" v-show="isPause" size="medium" @click="updateStatus('formHandle','Abandon','作废')">作废</el-button>
                  <el-button v-if="$hasPermission(hasPermissionMail)" plain v-show="isPause" size="medium" type="primary" @click="sendEmail">{{cmdCode=='gm050106'?'邮件发送':'发送划款指令'}}</el-button>
                  </div>
                  <div v-if="cmdType=='custom_demo'">
                  <el-button v-show="isPause && isUser" plain type="primary" size="medium" @click="formInlineValid22('formHandle','Normal','同意')">同意</el-button>
                  <el-button v-show="isPause && isUser" v-if="activeIndex!=1" plain type="info" size="medium" @click="formInlineValid('formHandle','Retire','退回')">退回</el-button>
                  <el-button v-show="isPause && !isUser" plain  type="primary" size="medium" @click="updateStatus('formHandle',0,'划款成功')">划款成功</el-button>
                  <el-button v-show="isPause && !isUser" plain  type="primary" size="medium" @click="updateStatus('formHandle',1,'划款失败')">划款失败</el-button>
                  <el-button v-if="$hasPermission(hasPermissionPause)" plain type="primary" v-show="isPause" size="medium" @click="formInlineValid('formHandle','Pause','暂缓')">暂缓</el-button>
                  <el-button v-if="$hasPermission(hasPermissionUnPause)" plain type="primary" v-show="!isPause" size="medium" @click="formInlineValid('formHandle','UnPause','解除暂缓')">解除暂缓</el-button>
                  <el-button v-if="$hasPermission(hasPermissionCancle)" plain type="warning" v-show="isPause" size="medium" @click="updateStatus('formHandle','Cancle','撤销')">撤销</el-button>
                  <el-button v-if="$hasPermission(hasPermissionAbandon)" plain type="info" v-show="isPause" size="medium" @click="updateStatus('formHandle','Abandon','作废')">作废</el-button>
                  <el-button v-if="$hasPermission(hasPermissionMail)" plain v-show="isPause" size="medium" type="primary" @click="sendEmail">发送划款指令</el-button>
                  </div>
               </div>
            </div>
        </el-col>
      </el-row>
    </el-drawer>
    <el-dialog
     title="邮件" 
     center width="60% !important" 
     top='5vh' 
     custom-class='email_dialog' 
     :visible.sync="email_show"
     :close-on-click-modal="false"
     >
      <DialogEmail ref="DialogEmail" @close='closeEmail' v-if="email_show"/>
    </el-dialog>
    
  </div>
</template>
<script>
import selectTable from '@/views/commonComponents/selectTable.vue';
import PdfPreview from '@/components/PdfPreview'
import HkzlDrawer from './hkzlDrawer'
import commonFun from '@/filters/new_common'
import drawerApi from "@/utils/transfer-drawer";
import bpmPage from "../bpm/testBpm.vue";
import synHandleApi from '@/api/synHandle/synHandle'
import trackingAgentApi from '@/api/transfer/trackingAgentList'
import configurationApi from '@/api/configuration/configuration.js'
import fun from '@/filters/common'
import commonApi from '@/api/common'
import cmCheckApi from '@/api/transfer/cmdCheck'
import bizBeginApi from '@/api/transfer/bizBegin'
import customApi from "@/api/custom/customList";
import accountApi from "@/api/product/accountSearch";
import investBizBeginApi from '@/api/invest/investBizBegin'
import pageApi from "@/api/home/calendarList";
import $ from 'jquery'
// btn
import menuBtn from './drawerCodeBtn'
import { stepMenuBtn } from '@/utils/stepBtn'
// import mjForm from '@/views/product/account/form/mjForm'
import TgForm from '@/views/product/account/form/tgForm'
// import ymtForm from '@/views/product/account/form/ymtForm'
import ZqForm from '@/views/product/account/form/zqForm'
import QhzhForm from '@/views/product/account/form/qhzhForm'
import QtForm from '../../product/account/form/qtForm.vue';
import YhjForm from '../../product/account/form/yhjForm.vue';
import ZdyAccountInfo from '@/views/product/account/zdyAccount/zdyAccount.vue'
import DialogEmail from './DialogEmail'
import modelFileValidate from '@/mixinsModel/file-validate'
import EditForm from './editForm'
import selectAccount from "@/views/commonComponents/selectAccount.vue";
export default {
  mixins: [modelFileValidate],
  components: {
    bpmPage,
    menuBtn,
    HkzlDrawer,
    PdfPreview,
    // mjForm,  //募集户
    TgForm,  //托管户
    // ymtForm,  //一码通
    QhzhForm, //期货账户
    ZqForm, //证券账户
    QtForm, //其他账户
    YhjForm, //银行间账户
    DialogEmail, //邮件发送
    selectTable,
    EditForm,
    ZdyAccountInfo,
    selectAccount
  },
  props:{
    cmdStatus:{}
  },
  data() {
    return {
      cmdCodeTypeArr:{},  //cmdcode数据字典obj
      cmdCodeName:"", //cmdCode 中文
      oldFormData:{},
      newFormData:{},
      urlArr:[],
      mainBox_span:12,
      isedit:false,
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
        paddingRight:'26px'
      },
      hasPermissionPause: '',
      hasPermissionUnPause: '',
      hasPermissionCancle: '',
      hasPermissionAbandon: '',
      hasPermissionMail:'',
	  isCheckOver:false,
      isUser: true,
      isPause: true,
      isSuccesss: false,
      menuBtnShow: false,
      stepDataInofo: [],
      isViewStepInfo: false,
      viewInfo: "",
      inHandInfo: "",
      // drawerSize: '50%',
      drawerSize: '100%',
      getDataForm: {},
      bpmData: [],
      drawer: false,
      isLeftInfo: false,
      leftDrawer: false,
      // demo数据
      leftDrawer2: false,
      hkzl_show:false,
      edit_form:false,
      yulan_show: false,
      fjyl_show:false,
      zh_info_show: false,
      email_show:false,
      zhxx_show:false,
      qh_show:false,  //期货账户
      zq_show:false,  //证券账户
      qt_show:false,  //其他账户
      yhj_show:false,  //银行间账户
      tg_show:false,  //托管户
      zdy_show:false, //自定义（5个账户）
      formCount:{},
      formLabelWidth:'100px',
      isSearchData:true,
      form_show: true,
      myTaskId: '',
      tableList: [],
      tableList1: [],
      active: null,
      activeIndex: null,
	  processActive:false,

      stepData: [],
      fileList: [],
      accountCodes: [], //产品名称
      selects: [
        { value: '选项1', label: '经纪商1' },
        { value: '选项2', label: '经纪商2' }
      ], //销售机构选择
      formHandle: {
        remark: ''
      },
      fundCode:'',
      formInline:{
        pfomBizNum: '', //指令编号
        beginTime: '', //发起时间
        subjectDeadlineAt:'',//科目取数截止日期
        fundCode:'',//产品&基金代码
        transferReqdate:'',//要求划款日期
        brokerCode:'',//经纪商选择
        transferAmount:'',//转账金额
        instructType:'',//指令类型
        accountType:"",//转账类型
        type:"",
        fundSalerName: '',//机构,
        depositBankName: '',//银行,
        remark:'',//备注
        handel:'',//处理意见
        payerAcconame:'',//付款人
        payerAccount:'',//付款账号
        payerBank:'',//付款行
        payeeAcconame:'',//收款人
        payeeAccount:'',//收款账号
        payeeBank:'',//收款行
        paymentSystemNumber:'',//支付系统号
        processUse:'',//用途
        stockCode:'', // 股票债券代码
        noTransaction:"", //无指令
      },
      oldForm:{
        pfomBizNum: '', //指令编号
        beginTime: '', //发起时间
        subjectDeadlineAt:'',//科目取数截止日期
        fundCode:'',//产品&基金代码
        transferReqdate:'',//要求划款日期
        brokerCode:'',//经纪商选择
        transferAmount:'',//转账金额
        instructType:'',//指令类型
        accountType:"",//转账类型
        type:"",
        fundSalerName: '',//机构,
        depositBankName: '',//银行,
        remark:'',//备注
        handel:'',//处理意见
        payerAcconame:'',//付款人
        payerAccount:'',//付款账号
        payerBank:'',//付款行
        payeeAcconame:'',//收款人
        payeeAccount:'',//收款账号
        payeeBank:'',//收款行
        paymentSystemNumber:'',//支付系统号
        processUse:'',//用途
        stockCode:'', // 股票债券代码
      },
      moneyValidateDefalut:/^(0|[1-9]{1}\d{0,14}|[1-9]{1}\d{0,12}\.\d{1}|[1-9]{1}\d{0,11}\.\d{2}|0\.\d{1,2})$/,
		  moneyValidate:/^(0|[1-9]{1}\d{0,14}|[1-9]{1}\d{0,12}\.\d{1}|[1-9]{1}\d{0,11}\.\d{2}|0\.\d{1,2})$/,
      formInlineRules:{},
      formInlineRulesBackup:{
        fundCode:[{ required:true, pattern: "", message: "请选择产品", trigger: "change" }],
        transferAmount:[{ required: true, trigger: 'change',pattern: '',message: "请输入数值且最多包含2位小数"}],
        payerAcconame:[{ required:true, pattern: "", message: "请输入付款人", trigger: "change" }],
        payerAccount:[
          { required:true, pattern: "", message: "请输入付款账号", trigger: "change" },
          {required:false, pattern: /^[a-zA-Z0-9]+$/, message: "请输入字母加数字的组合", trigger: "change"},
        ],
        payerBank:[{ required:true, pattern: "", message: "请输入付款行", trigger: "change" }],
        payeeAcconame:[{required:true, message: "请输入收款人", trigger: "change"},],
        payeeAccount:[
          {required:true, message: "请输入收款账号", trigger: "change"},
          {required:false, pattern: /^[a-zA-Z0-9]+$/, message: "请输入字母加数字的组合", trigger: "change"},
        ],
        payeeBank:[{required:true, message: "请输入收款行", trigger: "change"},],
        paymentSystemNumber:[
          // {required:true, message: "请输入支付系统号", trigger: "change"},
          {required:false, pattern: /^[a-zA-Z0-9]+$/, message: "请输入字母加数字的组合", trigger: "change"},
        ],
        // dBeginTime:[{required:true, message: "请选择指令日期", trigger: "change"}],
        transferReqdate:[{required:true, message: "请选择到账日期", trigger: "change"}],
        brokerCode:[{required:true, message: "请输入经纪商", trigger: "change"}],//经纪商
        subjectDeadlineAt:[{required:false, message: "请选择科目数截止日期", trigger: "change"}],//科目取数截止日期
        stockCode:[{required:true, message: "请输入股票/债券代码", trigger: "change"}],// 股票/债券代码
      },
      edit_show:false, //编辑按钮(自定义)
      fh_edit_show:false, //编辑按钮(转账、投资、TA、付费)
      back_show:false,
      backBtn_show:false, //退回按钮展示
      zl_edit_show:false,
      pfomBizNum:'',
      tableData:{},
      cmdType:'',
      cmdCode:'',
      fundCode:'',
      isSend:'',
      id:'',
      row:{},
      submitOrder:'',
      pickerOptions:{},
      api:'',
      borkerInfos:[],//经纪商数组
      saleMechanisms:[],//销售机构数组
      bankArr:[],//定存银行数组
      sendDataObjNum:0,
      editFormData:{},
      butTxt:'编辑',
      xmlId:'',
      newformData:{},
      oldFundSalerName:'',
      oldDepositBankName:"",
      PreviewFileId:'',
      account_show:false,
      payeeAcc_show:false,
    };
  },
  methods: {
    //获取提交串submitOrder
    getSubmitOrder(){
      console.log('getSubmitOrder');
		  pageApi.getSubmitOrder({}).then(({ data: res }) => {
		    this.submitOrder=res.data||new Date().getTime();
      })
      .catch((err) => console.log("getSubmitOrder err", err));
	  },
    // 获取服务器时间
    getServerData() {
      pageApi
        .getTime({})
        .then(({ data: res }) => {
          // this.nowTime=res.timestamp;
          // this.formInline.date = res.timestamp;
          // this.getTody(res.timestamp)
          this.pickerOptions={
            disabledDate(time) {
              return time.getTime() < res.timestamp - 24 * 60 * 60 * 1000;
            },
          }
        })
        .catch((err) => console.log("is msg err", err));
    },
    // 页面加载
    init(data) {
      // console.log('init',data);
      if(data.taskXmlId){
        this.xmlId = data.taskXmlId;
      }
      if(data.pfomTaskXmlid){
        this.xmlId = data.pfomTaskXmlid;
      }
      if(this.xmlId.indexOf('glrjb')!=-1 || this.xmlId.indexOf('zljb')!=-1){
        this.backBtn_show = false;
      }else{
        this.backBtn_show = true;
      }
      this.sendDataObjNum = 0;
      this.back_show = false;
      this.formInlineRules = {};
	    this.isCheckOver=false;
      this.edit_show = false;
      this.fh_edit_show = false;
      this.isedit = false;
      this.drawer = true;
      this.form_show = data.isCheck
      this.active = null
      this.isPause = true
      this.hasPermissionPause = ''
      this.hasPermissionUnPause = ''
      this.hasPermissionCancle = ''
      this.hasPermissionAbandon = ''
      this.hasPermissionMail = ''
      // this.form_show = true
      if(data.pfomBizNum){
        this.pfomBizNum=data.pfomBizNum;
      }
      this.tableData = data;
      // console.log(data);
      if(data.fundCode){this.fundCode=data.fundCode}

      this.myTaskId = data.pfomTaskid //用于处理处理按钮提交的id标识
      this.cmdType = data.cmdType;
      this.cmdCode = data.cmdCode;
      if(data.id){this.id = data.id;}
      this.isSend = data.isSend;
      // this.row = data;
      // 判断收/付款7要素是否展示
      if(this.cmdType=="custom_demo"){
        this.account_show = true;
        this.payeeAcc_show = false;
      }else if(this.cmdType=="transfer"){
        if(["gm040203","gm040403","gm040503","gm040601","gm040602","gm040603","gm0407","gm040701","gm040702","gm040703","gm040704","gm040705","gm040706"].includes(this.cmdCode)){
          this.account_show = true;
          this.payeeAcc_show = false;
        }else{
          this.account_show = false;
          this.payeeAcc_show = true;
        }
      }else if(this.cmdType=="invest"){
        this.payeeAcc_show = false;
        if(["gm050101","gm050102","gm050105","gm050106","gm050107"].includes(this.cmdCode)){
          this.account_show = true;
        }else{
          this.account_show = false;
        }
      }else{
        this.account_show = false;
        this.payeeAcc_show = false;
      }
      // 判断收款4要素是否展示
      

      if(this.cmdType=='transfer'){
        if(['gm040101','gm040102'].includes(this.cmdCode)){
          this.api = 'getZqAccountSELECT'
        }else if(['gm040201','gm040202','gm040203'].includes(this.cmdCode)){
          this.api = 'getZqAccountSELECTYH'
        }else{
          this.api = ''
        }
      }

      // 处理--管理人经办节点，默认展示指令编辑表单
      // if(!this.form_show){
      //   this.hkzl_show = true;
      //   this.$nextTick(()=>{
      //     this.$refs.HkzlDrawer.init1()
      //   })
      // }else{

      //   if(this.cmdType!="custom_demo"){
      //     if(this.xmlId.indexOf('glrjb')==-1){
      //       this.hkzl_show = true;
      //       this.$nextTick(()=>{
      //         this.$refs.HkzlDrawer.init1()
      //       })
      //     }else{
      //       this.edit_form = true;
      //     }
      //   }else{
      //     this.hkzl_show = true;
      //     this.$nextTick(()=>{
      //       this.$refs.HkzlDrawer.init1()
      //     })
      //   }
      // }
      // if(this.edit_form){
      //   this.$nextTick(()=>{
      //     if(this.$refs.editForm){
      //       this.$refs.editForm.init(this.cmdType,this.cmdCode,this.id,this.myTaskId)
      //     }
      //   })
      // }

      // 所有节点均默认展示 划款指令表格页
      this.hkzl_show = true;
      this.$nextTick(()=>{
        this.$refs.HkzlDrawer.init1()
      })

      this.getpmList(data.pfomTaskid);
      this.getViewDrawerInfo(data.pfomTaskid, data.cmdType)  //获取整个drawer的基础信息
      this.getSubmitOrder();
      this.getFormData(data.id);
      // this.getInfo(data.id);//获取右侧表单(真实业务数据)
      
      this.getEdimsGet("transfer.cmdCode"); // 获取cmdcode数据字典
    },
    getpmList(taskId){
      let params = {taskId}
      bizBeginApi.getpmList(params).then(res=>{
        if(res.data.status==200){
          if(res.data.data.rows.length){
            let arr = res.data.data.rows;
            arr.forEach(item=>{
              if(item.messageContent){
                this.$message({
                  type:"error",
                  message:item.messageContent
                })
              }
            })
          }
        }
      })
    },
    updateForm(id,flag){
      this.getFormData(id,flag);
      this.getFileList()
    },
    getInfo(id){
      let params = {id};
      trackingAgentApi.getInfo(params).then(res=>{
        if(res.data.status==200 && res.data.message == 'success'){
          let data = res.data.data;
          this.formInline.beginTime = data.beginTime || ''
          this.formInline.subjectDeadlineAt = data.subjectDeadlineAt || ''
          if(data.pfomBizNum){
            this.formInline.pfomBizNum = data.pfomBizNum
          }else{
            this.formInline.pfomBizNum = this.pfomBizNum
          }
          this.formInline.transferReqdate = data.transferReqdate || ''
          this.formInline.fundCode = data.fundCode+"_"+data.fundName;
          if(data.fundCode){this.fundCode=data.fundCode}
          if(data.id){this.id=data.id}
          // this.formInline.money = fun.formatNumber(data.transferAmount) | moneyYuan
          this.formInline.transferAmount = fun.moneyYuan(data.transferAmount)
          if(data.fundSaler && data.fundSalerName){
            this.formInline.fundSalerName = data.fundSaler +"|"+ data.fundSalerName || ''
          }else{
            this.formInline.fundSalerName = ''
          }
          if(data.depositBank && data.depositBankName){
            this.formInline.depositBankName =data.depositBank +'|'+ data.depositBankName || ''
          }else{
            this.formInline.depositBankName = ''
          }
          this.formInline.remark = data.remark || ''
          this.formInline.brokerCode = data.brokerCode || ''
          this.formInline.payerAcconame = data.payerAcconame || ''
          this.formInline.payerAccount = data.payerAccount || ''
          this.formInline.payerBank = data.payerBank || ''
          this.formInline.payeeAcconame = data.payeeAcconame || ''
          this.formInline.payeeAccount = data.payeeAccount || ''
          this.formInline.payeeBank = data.payeeBank || ''
          this.formInline.paymentSystemNumber = data.paymentSystemNumber || ''; //支付系统号
          this.formInline.processUse = data.processUse || ''; //用途
          this.formInline.stockCode = data.stockCode || ''; //股票债券代码
          this.formInlineRules = this.formInlineRulesBackup;
        }else{

        }
      })
    },
    getFormData(id,flag){
      let params = {id}
      trackingAgentApi.getFormData(params).then(res=>{
        if(res.data.status==0 && res.data.message == 'success'){
          let data = res.data.data;
          this.newformData = data;
          this.getResultData2(data,flag);
        }
      })
    },
    //获取整个drawer的基础信息
    getViewDrawerInfo (id, headNode) {
      // trackingAgentApi.getResultDatas(id).then(({ data:res}) => {
      trackingAgentApi.newGetResultDatas(id).then(({ data:res}) => {
        // console.log('res', res)
        let obj = {
          pfomTaskid: id || '',
          beginTime: res.data.processInstance.processFormData.beginTime || '',
          titleName: res.data.name || '',
          stepData: res.data.processInstance.instanceId || '',
          bpmId: res.data.processInstance.porcessDefineModel.id || '',
          taskKey: res.data.xmlId || '',
          processKey: res.data.formData.cmdType || '',
          // dataForm: {...res.data.processInstance.processFormData } || {},
          dataForm: {...res.data.formData } || {},
          tableList: res.data.taskOpinionModels || [],
          headNode: headNode,
		  isActive:res.data.isActive || ''
        }
        if(!obj.dataForm.pfomBizNum){
          obj.dataForm.pfomBizNum = this.pfomBizNum;
        }
        this.row = obj.dataForm;
        // this.$nextTick(()=>{
        //   this.$refs.HkzlDrawer.init(obj)
        // })
        // console.log('isActive',obj.isActive)
        console.log(obj.stepData,'obj.stepData');
        console.log(obj.taskKey,'obj.taskKey');
        this.getDataForm = obj
        this.getStapeData() //获取步骤的信息
        this.getDataInfo() //处理标题信息
        // this.getResultData() // 表单的基本信息
        this.tableListInfo()  //列表信息
        this.gettask(obj.stepData) //获取处理人列表
        this.getFileList() // 获取文件列表信息
        this.getStapeDataUserInfo() // 处理人信息
        this.rightControl() // 按钮权限控制
      }).catch((err) => { console.log('is msg err', err)})
    },
    // 按钮权限控制
    rightControl () {
      if (this.getDataForm.taskKey == 'transfer_hkjg' || this.getDataForm.taskKey == 'transfer_wzljb') this.isUser  = false
      else if(this.getDataForm.taskKey == 'custom_transfer_hkjg') this.isUser  = false
      else this.isUser = true
      if (!this.getDataForm.isActive) {
        this.isPause = false
      } else this.isPause = true
      let dataBtn = {
          headNode: this.getDataForm.headNode,
          node: this.getDataForm.taskKey
        }
      let btn = stepMenuBtn(dataBtn)
      // console.log(btn)
      this.hasPermissionPause = btn.hasPermissionPause
      this.hasPermissionUnPause = btn.hasPermissionUnPause
      this.hasPermissionCancle = btn.hasPermissionCancle
      this.hasPermissionAbandon = btn.hasPermissionAbandon
      this.hasPermissionMail = btn.hasPermissionMail
      // console.log(this.hasPermissionMail);
	  
	  this.isCheckOver=true;
    },
    tableListInfo () {
      let data = [...this.getDataForm.tableList]
      for (let item of data) {
        item.dateTime = fun.timeFormat(item.dateTime)
      }
      this.tableList = data
      // console.log(this.tableList,'处理人数据');
    },
    // 获取处理人列表
    gettask(val){
      let params={procInstId:val}
      trackingAgentApi
        .getTaskcomment(params)
        .then((res)=>{
          if(res.data.status==200){
            this.tableList1=res.data.data;
          }else{
            this.tableList1=[]
          }
          // console.log(res,'获取处理人列表');
        })
    },
     //获取步骤的信息
    getStapeData () {

      let data = this.getDataForm.stepData
      synHandleApi.getStapeInfo(data).then(({data: res}) => {
        let temp = new Array
        let curIndex=0;
        let index=0;

        for (let item of res.data) {
          if (item.isShow) {
			      index=index+1;
            let stepObj = new Object
            if (item.taskStatus == 'COMPLETED') {
              stepObj['des'] = '已完成'
			        stepObj['status']='success'
			  
			        curIndex=index;
            } else if (item.taskStatus == 'RUNNING') {
  
              stepObj['des'] = '当前处理'
			        stepObj['status']='finish'
			  
              this.taskXmlId=item.xmlId;
              this.processActive=true;
            } else if (item.taskStatus == 'READY') {
              stepObj['des'] = '待执行'
			        stepObj['status']='wait'
			  
			      } else if (item.taskStatus == 'ABANDON') {
              stepObj['des'] = '已废弃'
			        stepObj['status']='wait'
			  
			      } else if (item.taskStatus == 'CANCLE') {
              stepObj['des'] = '已撤销'
			        stepObj['status']='wait'
			  
            }else{
              stepObj['des'] = ''
              stepObj['status']='wait'
			      }
            stepObj['taskStatus'] = item.taskStatus
            stepObj['xmlId'] = item.xmlId
            stepObj['stepTitle'] = item.taskName
            stepObj['step'] = item.taskIndex-1
            temp.push(stepObj)
          }
        }
		
		    this.activeIndex=curIndex;
        if(this.activeIndex==1 && this.cmdType=="custom_demo" && this.form_show){
          // 展示编辑按钮(自定义划款指令 && 管理人经办节点 && 处理)
          this.edit_show = true;
        }else{
          this.edit_show = false;
        }
        console.log('this.activeIndex',this.activeIndex);
        this.stepData = temp
        // console.log('this.stepData',this.stepData);
        let oo= this.stepData.filter((item)=>{
          return item.stepTitle=='管理人复核'
        })
          // 编辑按钮(转账、投资、TA、付费) 管理人复核阶段展示 处理
        if(oo.length){
          if(oo[0].taskStatus == "RUNNING" && this.cmdType!=="custom_demo" && this.form_show){
            this.fh_edit_show = true;
          }else{
            this.fh_edit_show = false;
          }
        }

        // 管理人经办节点（转账、投资）展示 指令编辑 按钮
        let glrgbArr= this.stepData.filter((item)=>{
          return item.stepTitle=='管理人经办'
        })
        if(glrgbArr.length){
          if(glrgbArr[0].taskStatus == "RUNNING" && (this.cmdType == 'transfer' || this.cmdType == 'invest') && this.form_show){
            this.zl_edit_show = true;
          }else{
            this.zl_edit_show = false;
          }
        }
        // 退回 管理人审批阶段(此阶段展示修改前后数据对比)
        let back = this.stepData.filter((item)=>{
          return item.stepTitle=='管理人审批' || item.stepTitle=='管理人复核'
        })
        if(back.length){
          let arr = back.filter(item=>{
            return item.taskStatus == "RUNNING"
          })
          if(arr.length){
            this.back_show = true;
          }else{
            this.back_show = false;
          }
          console.log('this.back_show',this.back_show);
        }
        // if(this.back_show){
        //   this.getOldFormData(this.id)
        // }
        // console.log('back_show',this.back_show,'-----------------------------------------------------------');
        // console.log('this.cmdType',this.cmdType,'-----------------------------------------------------------');


        this.$nextTick(() => {
          this.$emit('dataInfo', res.data)
        })
		
		    this.getStapeDataUserInfo() // 处理人信息
		
      }).catch((err) => console.log('is msg err', err))
    },
    // 处理人信息
    getStapeDataUserInfo () {
      let data  = {
        procInstId: this.getDataForm.stepData,
        // taskInstId: this.myTaskId
        taskXmlId: this.getDataForm.taskKey
      }
      synHandleApi.getUsrINfo(data).then(({data: res}) => {
        this.stepDataInofo = res.data
      })
    },
    // 金额转换
    moneyFocus(){
      this.formInlineRules.transferAmount[0].pattern = this.moneyValidateDefalut
      if (this.formInline.transferAmount && this.formInline.transferAmount.includes(',')) {
        this.formInline.transferAmount = this.formInline.transferAmount.toString().replace(/,/gi, '')-0;
      }
    },
    moneyBlur(){
      this.formInlineRules.transferAmount[0].pattern = this.moneyValidateDefalut
      let reg = this.moneyValidate.test(this.formInline.transferAmount)
      if (reg && this.formInline.transferAmount) {  //失去焦点正则为true
        this.formInlineRules.transferAmount[0].pattern = ''
            // this.dialogDataForm.money = moneyThousand(this.dialogDataForm.money)
        this.formInline.transferAmount = fun.moneyYuan(this.formInline.transferAmount)
        // this.$refs.dialogDataForm.validate()
      }
    },
    // 关闭drawer初始化数据
    closedDrawer () {
      this.formInlineRules = {};
      this.zhxx_show=false;
      this.fjyl_show=false;
      this.zh_info_show=false;
      this.hkzl_show = false;
      this.isLeftInfo = false
      $('#leftInfo').html('');
      this.form_show
      this.tableList = []
      this.bpmData = []
      this.getDataForm = {}
      this.formHandle.remark = ''
      this.drawerSize = '100%'
      this.mainBox_span = 12;
      for (let i in this.formInline) {
        this.formInline[i] = ''
      }
      this.menuBtnShow = false;
      this.edit_form = false;
      this.butTxt = '编辑';
      this.zl_edit_show = false;
      this.$emit('closedD');
    },
    //处理标题信息
    getDataInfo() {
      this.viewInfo = `${"流程详情"}`
      // this.viewInfo = `${"流程详情" + "--"}`
      this.inHandInfo = this.getDataForm.titleName  //用于标题
    },
    // 表单的基本信息
    getResultData() {
      let data = this.getDataForm.dataForm
      // this.formInline.beginTime = fun.timeFormat(this.getDataForm.beginTime)
      this.formInline.beginTime = this.getDataForm.beginTime || ''
      this.formInline.subjectDeadlineAt = data.subjectDeadlineAt || ''
      if(data.pfomBizNum){
        this.formInline.pfomBizNum = data.pfomBizNum
      }else{
        this.formInline.pfomBizNum = this.pfomBizNum
      }
      this.formInline.transferReqdate = data.transferReqdate || ''
      this.formInline.fundCode = data.fundCode+"_"+data.fundName;
      if(data.fundCode){this.fundCode=data.fundCode}
      if(data.id){this.id=data.id}
      // this.formInline.money = fun.formatNumber(data.transferAmount) | moneyYuan
      this.formInline.transferAmount = fun.moneyYuan(data.transferAmount)
      if(data.fundSaler && data.fundSalerName){
        this.formInline.fundSalerName = data.fundSaler +"|"+ data.fundSalerName || ''
      }else{
        this.formInline.fundSalerName = ''
      }
      if(data.depositBank && data.depositBankName){
        this.formInline.depositBankName =data.depositBank +'|'+ data.depositBankName || ''
      }else{
        this.formInline.depositBankName = ''
      }
      this.formInline.remark = data.remark || ''
      this.formInline.brokerCode = data.brokerCode || ''
      this.formInline.payerAcconame = data.payerAcconame || ''
      this.formInline.payerAccount = data.payerAccount || ''
      this.formInline.payerBank = data.payerBank || ''
      this.formInline.payeeAcconame = data.payeeAcconame || ''
      this.formInline.payeeAccount = data.payeeAccount || ''
      this.formInline.payeeBank = data.payeeBank || ''
      this.formInline.paymentSystemNumber = data.paymentSystemNumber || ''; //支付系统号
      this.formInline.processUse = data.processUse || ''; //用途
      this.formInline.stockCode = data.stockCode || ''; //股票债券代码
      this.formInlineRules = this.formInlineRulesBackup;
      // this.formInlineRules.transferAmount[0].pattern = ''
      this.oldForm = JSON.parse(JSON.stringify(this.formInline));
      this.editFormData = JSON.parse(JSON.stringify(this.formInline));
      this.$nextTick(()=>{
        this.$refs.formInline.clearValidate();
      })
    },
    getResultData2(data,flag) {
      // let data = data;
      // this.formInline.beginTime = fun.timeFormat(this.getDataForm.beginTime)
      this.formInline.beginTime = data.beginTime || ''
      this.formInline.subjectDeadlineAt = data.subjectDeadlineAt || ''
      if(data.pfomBizNum){
        this.formInline.pfomBizNum = data.pfomBizNum
      }else{
        this.formInline.pfomBizNum = this.pfomBizNum
      }
      this.formInline.transferReqdate = data.transferReqdate || ''
      this.formInline.fundCode = data.fundCode+"_"+data.fundName;
      if(data.fundCode){this.fundCode=data.fundCode}
      if(data.id){this.id=data.id}
      // this.formInline.money = fun.formatNumber(data.transferAmount) | moneyYuan
      this.formInline.transferAmount = fun.moneyYuan(data.transferAmount)
      if(data.fundSaler && data.fundSalerName){
        this.formInline.fundSalerName = data.fundSaler +"|"+ data.fundSalerName || ''
      }else{
        this.formInline.fundSalerName = ''
      }
      if(data.depositBank && data.depositBankName){
        this.formInline.depositBankName =data.depositBank +'|'+ data.depositBankName || ''
      }else{
        this.formInline.depositBankName = ''
      }
      this.formInline.remark = data.remark || ''
      this.formInline.brokerCode = data.brokerCode || ''
      this.formInline.payerAcconame = data.payerAcconame || ''
      this.formInline.payerAccount = data.payerAccount || ''
      this.formInline.payerBank = data.payerBank || ''
      this.formInline.payeeAcconame = data.payeeAcconame || ''
      this.formInline.payeeAccount = data.payeeAccount || ''
      this.formInline.payeeBank = data.payeeBank || ''
      this.formInline.paymentSystemNumber = data.paymentSystemNumber || ''; //支付系统号
      this.formInline.processUse = data.processUse || ''; //用途
      this.formInline.stockCode = data.stockCode || ''; //股票债券代码
      this.formInline.noTransaction = data.noTransaction || ''; //股票债券代码
      this.formInlineRules = this.formInlineRulesBackup;
      // this.oldForm = JSON.parse(JSON.stringify(this.formInline));
      this.editFormData = JSON.parse(JSON.stringify(this.formInline));
      this.$nextTick(()=>{
        this.$refs.formInline.clearValidate();
      })
      if(flag)return

      // 所有节点均默认展示 划款指令表格页
      this.$nextTick(()=>{
        if(this.$refs.HkzlDrawer){
          console.log('14871487');
          this.$refs.HkzlDrawer.init(data,this.xmlId)
        }
      })
      if(this.xmlId.indexOf('glrsp')!=-1 || this.xmlId.indexOf('glrfh')!=-1){
        this.getOldFormData(this.id)
      }
      // 处理--管理人经办节点，默认展示指令编辑表单
      // if(!this.form_show){
      //   this.$nextTick(()=>{
      //     if(this.$refs.HkzlDrawer){
      //       console.log('14871487');
      //       this.$refs.HkzlDrawer.init(data,this.xmlId)
      //     }
      //   })
      //   if(this.xmlId.indexOf('glrsp')!=-1 || this.xmlId.indexOf('glrfh')!=-1){
      //     this.getOldFormData(this.id)
      //   }
      // }else{

      //   if(this.cmdType!="custom_demo"){
      //     if(this.xmlId.indexOf('glrjb')==-1){
      //       this.$nextTick(()=>{
      //         if(this.$refs.HkzlDrawer){
      //           console.log('15001500');
      //           this.$refs.HkzlDrawer.init(data,this.xmlId)
      //         }
      //       })
      //       if(this.xmlId.indexOf('glrsp')!=-1 || this.xmlId.indexOf('glrfh')!=-1){
      //         this.getOldFormData(this.id)
      //       }
      //     }
      //   }else{
      //     this.$nextTick(()=>{
      //       if(this.$refs.HkzlDrawer){
      //         console.log('15111511');
      //         this.$refs.HkzlDrawer.init(data,this.xmlId)
      //       }
      //     })
      //     if(this.xmlId.indexOf('glrsp')!=-1 || this.xmlId.indexOf('glrfh')!=-1){
      //       this.getOldFormData(this.id)
      //     }
      //   }
      // }
    },
    getProductInfo() {
      synHandleApi.getProductInfo().then(res =>{
        this.accountCodes = []
        if(res.data.message === "success"){
          let arr = res.data.data;
          let temp = new Array
          for(let i=0;i<arr.length;i++){
            let obj={};
            obj.value = arr[i].fundCode;
            obj.name = arr[i].fundCode + '_' + arr[i].fundName;
            temp.push(obj);
          }
          this.accountCodes = temp
        }else{
          this.$message.closeAll()
          this.$message.error('查询查询产品信息失败');
        }
      })
    },
    // 获取文件列表信息
    getFileList(){
      let id = this.getDataForm.dataForm.id || ''
      trackingAgentApi.getFileList(id).then(res =>{
        if(res.data.message === "success"){
          let arr = res.data.data;
          this.fileList = [];
          for(let i=0; i<arr.length; i++){
            let obj={};
            obj.id = arr[i].id;
            obj.url = arr[i].fileUri;
            obj.name = arr[i].fileName;
            obj.size = arr[i].fileSize;
            this.fileList.push(obj);
          }
        }
      }).catch(() => {})
    },
    viewLcPic() {
      this.leftDrawer = true;
      this.bpmData = this.stepData;
      let data = {
        id: this.getDataForm.bpmId,
        data: this.bpmData
      }
      this.$nextTick(() => {
        this.$refs.bpm.init(data)
      })
    },
    infoLeader () {
      this.isLeftInfo = !this.isLeftInfo
      this.hkzl_show = false;
      this.edit_form = false;
      if(this.isLeftInfo){
        this.mainBox_span=15;
      }else{
        this.mainBox_span=24;
      }
      if (this.isLeftInfo) {
        this.drawerSize = '80%'
        this.getInfoLeader()
      } else this.drawerSize = '50%'
    },
    // 划款指令按钮
    hkzl(){
      // this.leftDrawer2=!this.leftDrawer2;
      this.hkzl_show=!this.hkzl_show;
      this.isLeftInfo=false;
      this.edit_form = false;
      $('#leftInfo').html('');
      if(this.hkzl_show){
        this.drawerSize = '100%'
        this.mainBox_span=12;
        this.$nextTick(()=>{
          if(this.$refs.HkzlDrawer){
            this.$refs.HkzlDrawer.init(this.newformData,this.xmlId)
          }
        })
      }else{
        this.drawerSize = '50%'
        this.mainBox_span=24;
      }

    },
    // 预览按钮
    preview(){
      // this.yulan_show=true;
      this.fjyl_show=true;
    },
    // 账户信息按钮
    zh_info(){
      let cmdType = this.cmdType;
      let cmdCode = this.cmdCode;
      this.zhxx_show=true;

      let arr1 = ["gm040101","gm040102"];
      let arr2 = ["gm040201","gm040202","gm040203"];
      let arr3 = ["gm050103","gm050104","gm050106"];
      let arr4 = ["gm050101","gm050102"];
      if(cmdType=='transfer'){
        // if(cmdCode == "040101" || cmdCode == "040102"){
        if(arr1.includes(cmdCode)){
          console.log('证券账户');
          this.qh_show = false;
          this.zq_show = true; //展示证券账户
          this.qt_show = false;
          this.yhj_show = false;
          this.tg_show = false;
          this.zdy_show = false;
        // }else if(cmdCode == "040201" || cmdCode == "040202" || cmdCode == "040203"){
        }else if(arr2.includes(cmdCode)){
          console.log('期货账户');
          this.qh_show = true; //展示期货账户
          this.zq_show = false;
          this.qt_show = false;
          this.yhj_show = false;
          this.tg_show = false;
          this.zdy_show = false;
        }else{
          console.log('其他账户');
          this.qh_show = false;
          this.zq_show = false;
          this.qt_show = true; //展示其他账户
          this.yhj_show = false;
          this.tg_show = false;
          this.zdy_show = false;
        }
      }else if(cmdType=='invest'){
        // if(cmdCode == "050103" || cmdCode == "050104" || cmdCode == "050106"){
        if(arr3.includes(cmdCode)){
          console.log('银行间债券账户');
          this.qh_show = false;
          this.zq_show = false;
          this.qt_show = false;
          this.yhj_show = true; //展示银行间债券账户
          this.tg_show = false;
          this.zdy_show = false;
        // }else if(cmdCode == cmdCode == "050101" || cmdCode == "050102"){
        }else if(arr4.includes(cmdCode)){
          console.log('其他账户');
          this.qh_show = false;
          this.zq_show = false;
          this.qt_show = true; //展示其他账户
          this.yhj_show = false;
          this.tg_show = false;
          this.zdy_show = false;
        }else{
          console.log('其他账户');
          this.qh_show = false;
          this.zq_show = false;
          this.qt_show = true; //展示其他账户
          this.yhj_show = false;
          this.tg_show = false;
          this.zdy_show = false;
        }
      }else if(cmdType=='ta'){
        console.log('其他账户');
        this.qh_show = false;
        this.zq_show = false;
        this.qt_show = true; //展示其他账户
        this.yhj_show = false;
        this.tg_show = false;
        this.zdy_show = false;
      }else if(cmdType=='ta'){
        console.log('其他账户');
        this.qh_show = false;
        this.zq_show = false;
        this.qt_show = true; //展示其他账户
        this.yhj_show = false;
        this.tg_show = false;
        this.zdy_show = false;
      }else if(cmdType=='custom_demo'){
        console.log('其他账户');
        // this.qh_show = false;
        // this.zq_show = false;
        // this.qt_show = true; //展示其他账户
        // this.yhj_show = false;
        // this.tg_show = false;
        this.zdy_show = true;
      }else{
        console.log('其他账户');
        this.qh_show = false;
        this.zq_show = false;
        this.qt_show = true; //展示其他账户
        this.yhj_show = false;
        this.tg_show = false;
        this.zdy_show = false;
      }


      this.$nextTick(()=>{
        this.$refs.AccountInfo.init(this.fundCode);
      })
      // this.zh_info_show=!this.zh_info_show;
    },
    // 编辑按钮
    edit_1(){
      this.isedit = !this.isedit;
    },
    edit_(){
      if(this.isedit){
        this.$refs['formInline'].validate((valid) => {
          if(valid){
            this.formSave();
            
          }else{
            console.log('err');
            return false
          }
        })
      }else{
        this.isedit=true;
        this.butTxt = '保存'
      }
    },
    formSave(){
      console.log('保存');
      let params = {}
      params = commonFun.parameterSrc(this.formInline)
      params.beginTime = "";
      params.pfomBizNum = "";
      if(this.formInline.fundCode){
        params.fundCode = this.formInline.fundCode.split('_')[0];
        params.fundName = this.formInline.fundCode.split('_')[1];
      }
      if (this.formInline.transferAmount && this.formInline.transferAmount.includes(',')) {
        params.transferAmount = this.formInline.transferAmount.toString().replace(/,/gi, '')
      }
      params = commonFun.parameterSrc(params)
      params.paymentSystemNumber = this.formInline.paymentSystemNumber || "";
      params.processUse = this.formInline.processUse || "";
      params.remark = this.formInline.remark || "";
      params.id = this.getDataForm.dataForm.id;
      let formData = new FormData();
      for(let key in params){
        // console.log(key,params[key]);
        formData.append(key,params[key])
      }
      let oldfileArr = []
      for(let i=0;i< this.fileList.length;i++){
        if(this.fileList[i].raw){
          let aa = this.fileList[i].raw;
          formData.append("file",aa)
        }
        if(!this.fileList[i].raw){
          let bb = this.fileList[i].id;
          oldfileArr.push(bb)
        }
      }
      formData.append("oldfile",oldfileArr)
      // console.log(params);
      this.isedit=false;
      this.butTxt = '编辑';
    },
    // 管理人经办编辑按钮(只在 转账、投资指令展示)-指令编辑
    edit_glrjb(){
      this.edit_form = !this.edit_form;
      this.hkzl_show = false;
      this.isLeftInfo = false;
      if(this.edit_form){
        this.drawerSize = '100%'
        this.mainBox_span=12;
      }else{
        this.drawerSize = '50%'
        this.mainBox_span=24;
      }
      if(this.edit_form){
        this.$nextTick(()=>{
          if(this.$refs.editForm){
            this.$refs.editForm.init(this.cmdType,this.cmdCode,this.id,this.myTaskId)
          }
        })
      }
    },
    // 查看交互
    getInfoLeader () {
      this.$message.closeAll()
      let data = {
        taskKey: this.getDataForm.taskKey || '',
        processKey: this.getDataForm.processKey || ''
      }
      commonApi.getHandleHtml(data).then(res =>{
        if(res.data.status === 200){
          if(res.data.data){
              let html = res.data.data.html;
              $('#leftInfo').html(html);
          }
        }else{
          this.drawerSize = '50%'
          this.$message.error('查询失败');
        }
      }).catch(() => {})
    },
    // 文件状态改变时的钩子
    handleChange(file, fileList){
      this.fileValidate(file, fileList)
    },
    // 移出
    handleRemove (file, fileList) {
      this.handleChange(file, fileList)
    },
    // 预览
    handlePreview(file) {
      // console.log('预览',file);
      if(file.id){
          this.PreviewFileId = file.id;
          let params = {};
          params.id = file.id;
          params = commonFun.parameterSrc(params);
          if(this.$store.getters.token){ params["token"] = this.$store.getters.token;}
          // let action = this.$store.state.setting.baseApi + '/api/file/v1.0/downloadFile';
          let action = this.$store.state.setting.baseApi + '/api/file/v1.0/previewFile';
          let fileList =  this.fileList.filter(item=>{
            return item.id
          })
            // commonApi
            //   .previewFile(params)
            //   .then(res=>{
            //     console.log(res);
            //   })
          // console.log('fileList',fileList);
          let url = action+'?'+'id='+file.id+'&token='+this.$store.getters.token;
          this.fjyl_show=true;
      }
    },
    //审核通过，退回，作废，暂缓等操作
    updateStatus(vals,status,confirmStatus){
        this.$confirm('是否'+confirmStatus+"?",'提示',{
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
              // let params = Object.assign({},this.formHandle);
              let sendData = {};
              let taskExcuteCmdMode = {taskExcuteCmdType:status};
              let taskOpinionModel = {agree:true};
              taskOpinionModel.opinion = this.formHandle.remark;
              if(this.formHandle.remark==''){taskOpinionModel.opinion=confirmStatus}
              let formData = {};
              formData.remoteOperationFlag = false;
              sendData.formData = formData;
              sendData.taskOpinionModel = taskOpinionModel;
              if(status === 0){
                  formData.transferResult = true;
                  taskExcuteCmdMode['taskExcuteCmdType'] = 'Normal'
              }else if (status === 1){
                formData.transferResult = false;
                taskExcuteCmdMode['taskExcuteCmdType'] = 'Normal'
              } else {}
              sendData.taskExcuteCmdMode = taskExcuteCmdMode;
              // console.log('sendData',sendData);return
              cmCheckApi.updateStatus(this.myTaskId,sendData).then(res => {
                  let data= res.data.data;
                  if(res.data.status === 0){
                    this.$message.closeAll();
                        this.$message({
                          type: 'success',
                          message: '操作成功'
                        });
                    this.drawer = false
                    this.$emit('rightDrawer')
                    this.$emit('refash')
                  }else{
                    this.$message.closeAll();
                    this.$message({
                    type: 'error',
                    message: res.data.message ||'操作失败'
                    });
                  }
              })
        }).catch((err) => { console.log('is msg err', err)})
    },
    updateStatus1(vals,status,confirmStatus){
      this.$confirm('是否'+confirmStatus+"?",'提示',{
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          let sendData = {};
          let taskExcuteCmdMode = {taskExcuteCmdType:status};
          let taskOpinionModel = {agree:true};
            taskOpinionModel.opinion = this.formHandle.remark;
          if(this.formHandle.remark==''){taskOpinionModel.opinion=confirmStatus};
          let formData = JSON.parse(JSON.stringify(this.formInline));
          formData.beginTime = '';
          formData.pfomBizNum = '';
          formData.cmdType = this.cmdType;
          formData = commonFun.parameterSrc(formData);
          if (formData.transferAmount && formData.transferAmount.includes(',')) {
            formData.transferAmount = formData.transferAmount.toString().replace(/,/gi, '')-0;
          }
          if(formData.fundCode){
            let arr = this.formInline.fundCode.split('_');
            formData.fundCode = arr[0];
            formData.fundName = arr[1];
          }
          if(formData.fundSalerName){
            let arr = this.formInline.fundSalerName.split('|');
            formData.fundSaler = arr[0];
            formData.fundSalerName = arr[1];
          }
          if(formData.depositBankName){
            let arr = this.formInline.depositBankName.split('|');
            formData.depositBank = arr[0];
            formData.depositBankName = arr[1];
          }
          // console.log(formData.fundCode,formData.fundName);
          formData.remark = this.formInline.remark || '';
          formData.remoteOperationFlag = false;
          formData.id = this.getDataForm.dataForm.id;
          if(status === 0){
            formData.transferResult = true;
            taskExcuteCmdMode['taskExcuteCmdType'] = 'Normal'
          }else if (status === 1){
          formData.transferResult = false;
            taskExcuteCmdMode['taskExcuteCmdType'] = 'Normal'
          } else {}
          // console.log(this.formInline);
// console.log(formData);return
          sendData.formData = formData;
          sendData.taskOpinionModel = taskOpinionModel;
          sendData.taskExcuteCmdMode = taskExcuteCmdMode;

          // console.log('formData',formData);
          // console.log('sendData',sendData);

          let formData_ = new FormData();
          formData_.append("pfomTaskid", this.myTaskId)
          formData_.append("datastr", JSON.stringify(sendData))

          // let oldfileArr = []
          // for(let i=0;i< this.fileList.length;i++){
          //   if(this.fileList[i].raw){
          //     let aa = this.fileList[i].raw;
          //     formData_.append("file",aa)
          //   }
          //   if(!this.fileList[i].raw){
          //     let bb = this.fileList[i].id;
          //     oldfileArr.push(bb)
          //   }
          // }
          // formData_.append("oldfile",oldfileArr)
          cmCheckApi.updateAndSubmit(formData_).then(res => {
            let data= res.data.data;
            if(res.data.status === 0){
              this.$message.closeAll();
              this.$message({type: 'success',message: '操作成功'});
              this.drawer = false
              this.$emit('rightDrawer')
              this.$emit('refash')
            }else{
              this.$message.closeAll();
              this.$message({type: 'error',message: res.data.message ||'操作失败'});
            }
        }).catch((err)=>{
          console.log(err);
        })
        }).catch(()=>{})
    },
    duibizhilingbianji(vals,status,confirmStatus){
      if(this.edit_form && this.$refs.editForm){
        this.$nextTick(()=>{
          this.$refs.editForm.getNewData();
        })
        setTimeout(() => {
          let oldFormDataArr = Object.keys(this.oldFormData);
          let newFormDataArr = Object.keys(this.newFormData);
          if(oldFormDataArr.length && newFormDataArr.length){
            // console.log('数据对比');
            // console.log(this.newFormData);
            // console.log(this.oldFormData);
            let num = 0;
            for(let i in this.newFormData){
              if(this.newFormData[i] != this.oldFormData[i]){
                num++;
                // console.log(this.newFormData[i],this.oldFormData[i]);
                this.$confirm('指令编辑有改动且未保存, 是否保存?', '提示', {
                  confirmButtonText: '确定',
                  cancelButtonText: '取消',
                  type: 'warning'
                }).then(() => {
                  this.$nextTick(()=>{
                    this.$refs.editForm.submitForm2(vals,status,confirmStatus);
                  })
                }).catch(() => {
                  this.formInlineValid22(vals,status,confirmStatus);
                });
              }
              
            }
            // console.log('num',num);
            if(num==0){
              this.formInlineValid22(vals,status,confirmStatus);
            }
          }
        }, 200);
        
      }else{
        this.formInlineValid22(vals,status,confirmStatus);
      }
    },
    formInlineValid2({vals,status,confirmStatus}){
      let params = {taskId:this.myTaskId}
      bizBeginApi.getpmList(params).then(res=>{
        if(res.data.status==200){
          if(res.data.data.rows.length){
            let arr = res.data.data.rows;
            arr.forEach(item=>{
              if(item.messageContent){
                this.$message({
                  type:"warning",
                  message:item.messageContent
                })
              }
            })
          }else{
            this.formInlineValid(vals,status,confirmStatus);
          }
        }
      })
    },
    formInlineValid22(vals,status,confirmStatus){
      let params = {taskId:this.myTaskId}
      bizBeginApi.getpmList(params).then(res=>{
        if(res.data.status==200){
          if(res.data.data.rows.length){
            let arr = res.data.data.rows;
            arr.forEach(item=>{
              if(item.messageContent){
                this.$message({
                  type:"warning",
                  message:item.messageContent
                })
              }
            })
          }else{
            this.formInlineValid(vals,status,confirmStatus);
          }
        }
      })
    },
    formInlineValid(vals,status,confirmStatus){
      this.$refs['formInline'].validate((valid) => {
          if (valid) {
            if(this.cmdType=='custom_demo'){
              this.customUpdateStatus(vals,status,confirmStatus)
            }else{
              // console.log('updateStatus1',vals,status,confirmStatus);
              this.updateStatus1(vals,status,confirmStatus)
            }
          } else {
            console.log('error submit!!');
            return false;
          }
        });
    },
    customUpdateStatus(vals,status,confirmStatus){
      console.log('自定义');
      this.$confirm('是否'+confirmStatus+"?",'提示',{
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
              let params = Object.assign({},this.formInline);
              // console.log(params);
              
              let sendData = {};
              let taskExcuteCmdMode = {taskExcuteCmdType:status};
              let taskOpinionModel = {agree:true};
              taskOpinionModel.opinion = this.formHandle.remark;
              if(this.formHandle.remark==''){taskOpinionModel.opinion=confirmStatus}
              let formData = {};
              formData.remoteOperationFlag = false;
              formData.submitOrder = this.submitOrder;
              // -----------↓↓↓↓↓↓表单数据↓↓↓↓↓↓-----------
              formData.paymentSystemNumber = params.paymentSystemNumber;
              formData.beginTime = params.beginTime;
              formData.transferReqdate = params.transferReqdate;
              if(params.fundCode){
                formData.fundCode = params.fundCode.split('_')[0];
                formData.fundName = params.fundCode.split('_')[1];
              }
              // formData.transferAmount = 123123;
              formData.transferAmount = this.formInline.transferAmount;
              if (this.formInline.transferAmount && this.formInline.transferAmount.includes(',')) {
                formData.transferAmount = this.formInline.transferAmount.toString().replace(/,/gi, '')
              }
              formData.payerAcconame = params.payerAcconame;
              formData.payerAccount = params.payerAccount;
              formData.payerBank = params.payerBank;
              formData.payeeAcconame = params.payeeAcconame;
              formData.payeeAccount = params.payeeAccount;
              formData.payeeBank = params.payeeBank;
              formData.paymentSystemNumber = params.paymentSystemNumber;
              formData.processUse = params.processUse;
              formData.remark = params.remark;
              formData.id = this.getDataForm.dataForm.id;
              // -----------↑↑↑↑↑↑表单数据↑↑↑↑↑↑-----------
              sendData.formData = formData;
              sendData.taskOpinionModel = taskOpinionModel;
              if(status === 0){
                  formData.transferResult = true;
                  taskExcuteCmdMode['taskExcuteCmdType'] = 'Normal'
              }else if (status === 1){
                formData.transferResult = false;
                taskExcuteCmdMode['taskExcuteCmdType'] = 'Normal'
              } else {}
              sendData.taskExcuteCmdMode = taskExcuteCmdMode;
              let file = [];
              let oldfile = [];
              for(let i=0;i< this.fileList.length;i++){
                if(this.fileList[i].raw){
                  let aa = this.fileList[i].raw;
                  file.push(aa)
                }
                if(!this.fileList[i].raw){
                  let bb = this.fileList[i].id;
                  oldfile.push(bb);
                }
              }
              // sendData.file = file;
              // sendData.oldfile = oldfile;
              // pfomTaskid，datastr，file，oldfile
              let formData_ = new FormData();
              formData_.append("pfomTaskid", this.myTaskId)
              formData_.append("datastr", JSON.stringify(sendData))

              
              let oldfileArr = []
              for(let i=0;i< this.fileList.length;i++){
                if(this.fileList[i].raw){
                  let aa = this.fileList[i].raw;
                  formData_.append("file",aa)
                }
                if(!this.fileList[i].raw){
                  let bb = this.fileList[i].id;
                  oldfileArr.push(bb)
                }
              }
              formData_.append("oldfile",oldfileArr)
              // formData_.append("file",sendData.file)
              // formData_.append("oldfile",sendData.oldfile)
              // console.log(sendData);
              cmCheckApi.newUpdateStatus(formData_).then(res => {
                  let data= res.data.data;
                  if(res.data.status === 0){
                    this.$message.closeAll();
                        this.$message({
                          type: 'success',
                          message: '操作成功'
                        });
                    this.drawer = false
                    this.$emit('rightDrawer')
                    this.$emit('refash')
                  }else{
                    this.$message.closeAll();
                    this.$message({
                    type: 'error',
                    message: res.data.message ||'操作失败'
                    });
                  }
              })
        }).catch((err) => { console.log('is msg err', err)})
    },
    stepClick (data) {
      if(!this.processActive) return
        if ( data && data.taskStatus == 'RUNNING') {
          this.isViewStepInfo = true
        } else {
          this.isViewStepInfo = false
        }
    },
    //获取页面高度
    getViewINfoHW () {
      this.$nextTick(() => {
        let maxH = document.documentElement.clientHeight || document.body.clientHeight
        let maxw = document.documentElement.clientWidth || document.body.clientWidth
        // this.maxHeight.height = maxH + 'px'
        this.fixStyle.width = (maxw / 2) + 'px' 
      })
    },
    // 按钮返回
    refashBtn () {
      this.drawer = false
      this.$emit('rightDrawer')
      this.$emit('refash')
    },
    // 回调remak信息
    getRemark () {
      return this.formHandle.remark
    },
    getEmailInfo(){
      let params = {id:this.id}
      trackingAgentApi.getEmailInfo(params).then(res=>{

      })
    },
    sendEmail(){

      let isSend = this.isSend;
      if(isSend){
        this.$confirm('本次发送为重复发送, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.email_show = true;
          this.$nextTick(()=>{
          this.$refs.DialogEmail.getEmailInfo(this.row)
        })

        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          });          
        });
      }else{
        this.email_show = true;
        // this.getEmailInfo();
        this.$nextTick(()=>{
          this.$refs.DialogEmail.getEmailInfo(this.row)
        })
      }
      
    },
    closeEmail(){
      this.email_show=false;
    },
    sendEmail1(){
      this.$confirm('确定发送邮件?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          
          this.$message({ type: 'success', message: '发送成功!' });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消发送'
          });          
        });
    },
    sendDataObj(data){
      this.sendDataObjNum++;
      console.log('sendDataObj',this.sendDataObjNum);
      let val = data.fundCode
      let fundCode = data.fundCode;
      if (fundCode) {
        let params = { fundCode: fundCode };
        let params1 = { productCode: fundCode };
        // this.getAccounts(params);
        this.getAcc(params1);
      }
      if(this.sendDataObjNum > 1){
        this.formInline.brokerCode = ''
        this.formInline.payerAcconame = "";
        this.formInline.payeeAcconame = "";
      }
      if(this.api&&data){
        this.getBrokers(val,this.api)
      }

    },
    getAcc(params){
      accountApi
        .getAllAccList(params)
        .then(res=>{
          if(res.data.status==200){
            let data = res.data.data;
            this.$nextTick(()=>{
              if(this.$refs.selectAccount1){
                this.$refs.selectAccount1.init(data);
              }
              if(this.$refs.selectAccount2){
                this.$refs.selectAccount2.init(data);
              }
            })
          }
        })
        .catch(()=>{

        })
    },
    getAccounts(params) {
      customApi
        .getAccounts(params)
        .then((res) => {
          if (res.data.status == 200) {
            // console.log(res.data.data.list);
            let data = res.data.data.list;
            this.$nextTick(() => {
              if(this.$refs.selectAccount1){
                this.$refs.selectAccount1.init(data);
              }
              if(this.$refs.selectAccount1){
                this.$refs.selectAccount2.init(data);
              }
            });
          }
        })
        .catch(() => {});
    },
    getAccountInfo1(val) {
      // console.log(val);
      this.formInline.payerAccount = val.accoNo || "";
      this.formInline.payerBank = val.accoBank || "";
    },
    getAccountInfo2(val) {
      // console.log(val);
      this.formInline.payeeAccount = val.accoNo || "";
      this.formInline.payeeBank = val.accoBank || "";
      this.formInline.paymentSystemNumber = val.hvpsNo || "";
    },
    getBrokers(fundCode,api){
      this.borkerInfos = [];
      let params = {fundCode}
      bizBeginApi[api](params).then(res=>{
        if(res.data.status==200){
          // console.log('borkerInfos',res);
          let arr = res.data.data;
          for (let i of arr) {
            let obj = {}
            obj.value = (i.openStruc || ' 无 ') + ( i.openExchange ? '( '+ i.openExchange + ' )' : '( 无 )')
            obj.name = (i.openStruc || ' 无 ') + ( i.openExchange ? '( '+ i.openExchange + ' )' : '( 无 )')
            this.borkerInfos.push(obj)
          }
        }else{

        }
      })
    },
           //查询销售机构
      getSaleMechanism(){
        let params = 'fundSalerType';
        investBizBeginApi.getSaleMechanism(params).then(res =>{
          if(res.data.message === "success"){
              let arr = res.data.data;
              this.saleMechanisms = [];
              for(let i=0;i<arr.length;i++){
                let obj={};
                obj.value=arr[i].dimCde+"|"+arr[i].dimNme;
                obj.label = arr[i].dimNme;
                this.saleMechanisms.push(obj);
              }
              // console.log('this.saleMechanisms',this.saleMechanisms);
          }else{
            this.saleMechanisms = [];
            this.$message.closeAll();
            this.$message.error('查询销售机构信息失败');
          }
        }).catch(() => {
          this.$message.closeAll();
            this.$message.error('查询销售机构信息失败');
        })
      },
        //查询银行
      getBank(){
        let params = 'bankType';
        investBizBeginApi.getBank(params).then(res =>{
          if(res.data.message === "success"){
              let arr = res.data.data;
              this.bankArr = [];
              for(let i=0;i<arr.length;i++){
                let obj={};
                obj.value=arr[i].dimCde+"|"+arr[i].dimNme;
                obj.label = arr[i].dimNme;
                this.bankArr.push(obj);
              }
              // console.log('this.bankArr',this.bankArr);
          }else{
            this.bankArr = [];
            this.$message.closeAll();
            this.$message.error('查询银行信息失败');
          }
        }).catch(() => {
          this.$message.closeAll();
            this.$message.error('查询银行信息失败');
        })
      },
      getOldFormData(val){
        let params = {
          id:val
        }
        trackingAgentApi.getOldData(params).then(res=>{
          if(res.data.status==0){
            // console.log('getOldFormData------------',res.data.data);
            let data = res.data.data;
            if(!data) return
            this.oldForm.transferReqdate = data.transferReqdate || ''
            this.oldForm.fundCode = data.fundCode+"_"+data.fundName;
            this.oldForm.transferAmount = fun.moneyYuan(data.transferAmount)
            if(data.fundSaler && data.fundSalerName){
              this.oldForm.fundSalerName = data.fundSaler +"|"+ data.fundSalerName || ''
            }else{
              this.oldForm.fundSalerName = data.fundSalerName || ''
            }
            this.oldFundSalerName = data.fundSalerName || ''
            if(data.depositBank && data.depositBankName){
              this.oldForm.depositBankName =data.depositBank +'|'+ data.depositBankName || ''
            }else{
              this.oldForm.depositBankName = data.depositBankName || ''
            }
            this.oldDepositBankName = data.depositBankName || ''
            this.oldForm.remark = data.remark || ''
            this.oldForm.brokerCode = data.brokerCode || ''
            this.oldForm.payerAcconame = data.payerAcconame || ''
            this.oldForm.payerAccount = data.payerAccount || ''
            this.oldForm.payerBank = data.payerBank || ''
            this.oldForm.payeeAcconame = data.payeeAcconame || ''
            this.oldForm.payeeAccount = data.payeeAccount || ''
            this.oldForm.payeeBank = data.payeeBank || ''
            this.oldForm.paymentSystemNumber = data.paymentSystemNumber || ''; //支付系统号
            this.oldForm.processUse = data.processUse || ''; //用途
            this.oldForm.stockCode = data.stockCode || ''; //股票债券代码
            this.oldForm.subjectDeadlineAt = data.subjectDeadlineAt || ''
            // console.log('this.oldForm',this.oldForm);
          }
        })
        // this.oldForm.transferReqdate = '2021-05-25'
      },
      // 关闭附件预览框
      closePdfPreview(){
        this.fjyl_show = false;
        this.$notify.closeAll();
      },
      // 关闭账户信息
      closeZhxx(){
        this.zhxx_show = false;
        this.$notify.closeAll();
      },
    // 数据字典
    getEdimsGet(val) {
      let params = val;
      commonApi.getEdims(params).then((res) => {
        if (res.data.message === "success") {
          if(val=='transfer.cmdCode'){
            let arr = res.data.data;
            let arr1 = []
            let arr2 = [...arr,...arr1]
            for (let i = 0; i < arr2.length; i++) {
              this.cmdCodeTypeArr[arr2[i].dimCde] = arr2[i].dimNme;
            }
            if(this.cmdType=='custom_demo'){
              this.cmdCodeName = '自定义划款指令'
            }else{
              this.cmdCodeName = this.cmdCodeTypeArr[this.cmdCode] || '';
            }
          }
        } else {
          this.$message.closeAll();
          this.$message.error("初始化数据失败");
        }
      });
    },
  },
  mounted () {
    // 获取服务器时间
    this.getServerData()
    // 获取销售机构
    this.getSaleMechanism();
    // 获取定存银行
    this.getBank();
	//this.isCheckOver=false;
    // console.log('active',this.active);
    this.getViewINfoHW()
    window.onresize = () => {
      this.getViewINfoHW()
    }
    console.log('this.active',this.active);
    this.$bus.$on("editFormData",(data)=>{
      // console.log('oldFormData',data);
      this.oldFormData = data;
    });
    this.$bus.$on("NewData",(data)=>{
      // console.log('NewData',data);
      this.newFormData = data;
    });
    this.$bus.$on("tongyi",(data)=>{
      // console.log('tongyi',data);
      this.formInlineValid2(data);
    });
  },
  watch:{
    active(){
      // console.log('watch',this.active);
      // if(this.active==4){
        
      // }
    },
    edit_form(data){
      if(!data){
        this.oldFormData = {};
        this.newFormData = {};
      }
    },
    "formInline.noTransaction"(data){
      if(data=='1'){
        this.formInline.payerAcconame = ''
        this.formInline.payeeAcconame = ''
        this.formInlineRules.payerAcconame[0].required = false;
        this.formInlineRules.payerAccount[0].required = false;
        this.formInlineRules.payerBank[0].required = false;
        this.formInlineRules.payeeAcconame[0].required = false;
        this.formInlineRules.payeeAccount[0].required = false;
        this.formInlineRules.payeeBank[0].required = false;
        this.$refs['formInline'].validate((valid) => {})
      }else{
        this.formInlineRules.payerAcconame[0].required = true;
        this.formInlineRules.payerAccount[0].required = true;
        this.formInlineRules.payerBank[0].required = true;
        this.formInlineRules.payeeAcconame[0].required = true;
        this.formInlineRules.payeeAccount[0].required = true;
        this.formInlineRules.payeeBank[0].required = true;
      }
    },
  }
};
</script>
<style lang='scss'> 

 .el-upload-list__item.is-success.focusing .el-icon-close-tip{
   display: none !important;
 }
.rightDrawerStyle{
  .change_red{
    color: red;
  }
  .change_red .el-input__inner{
    color: red !important;
  }
  .change_red .el-textarea__inner{
    color: red !important;
  }
}

  .hkzlyl{
    overflow-y: auto !important;
  }

.rightDrawerStyle {
  .yulan_title{
    color: rgb(64, 158, 255);
    display: flex;
    justify-content: space-between;
    padding: 5px 10px;
    span{
      font-size: 14px;
    }
  }
   .yulan{
      height: 90% !important;
      .el-dialog__body{
        height: 100%;
      }
    }
  .movePlace {
    overflow: none;
    .stepRowName_style {
      font-weight:600;
      margin-bottom:10px;
    }
    .borderLine {
      width: 100%;
      margin: 8px auto;
      border-bottom: 1px dashed #409EFF;
    }
    .solidStyle {
      margin: 5px auto;
      border-bottom: 1x solid #409EFF !important
    }
  }
  .el-drawer__body {
    overflow-y: auto
  }
  .mainBox {
    // padding-bottom: 250px;
    // margin-bottom: 250px;
    width: 95%;
  }
  .bigSize {
    font-size: 20px;
    cursor: pointer;
    &:hover{
      font-weight: 600;
    }
  }
  .titleStyle {
    // margin: 20px 0 20px 20px;
    padding: 20px;
  }
  .steps_hk {
    // width: 95%;
    // margin: 0 auto;
    margin-left: 21px;
    margin-right: 24px;
  }
  .formStyle {
    width: 80%;
    margin: 10px auto;
  }
  .formStyle_table{
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
  .fixefrom{ 
    width: 95%;
    margin: 0 auto;
  }
  .btnStyle {
    margin: 10px 0 20px 20px;
  }
}
.rightDrawerStyle .rightDrawerStyle_table .el-col-8{
      white-space: nowrap;
    overflow: hidden;
    display: inline-block;
    text-overflow: ellipsis;
}

.rightDrawerStyle .el-form-item__content{
  min-width: 0;
}
.zhanghu_info .el-form-item__content{
  min-width: 0 !important;
}
</style>
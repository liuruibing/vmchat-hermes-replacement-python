<template>
  <div class="productDisclosure">
      <div class="toolbar" >
     <el-form :inline="true" ref = "formInline" :model="formInline"  class="demo-form-inline form_inline_search" >
          <el-row>
            <el-col :span="16">
              <div class="grid-content bg-purple">
               <el-form-item label="产品类型" prop="fundType">
                  <el-select clearable  v-model="formInline.fundType"  placeholder="请选择"  >
                      <el-option
                        v-for="(group, index) in fundTypeArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme">
                      </el-option>
                    </el-select>
                </el-form-item>
               <el-form-item label="报表频率" prop="reportType">
                  <el-select clearable  v-model="formInline.reportType"  placeholder="请选择"  >
                      <el-option
                        v-for="(group, index) in reportTypeArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme">
                      </el-option>
                    </el-select>
                </el-form-item>
               <el-form-item label="报表类型" prop="submitAgency">
                  <el-select clearable  v-model="formInline.submitAgency"  placeholder="请选择"  >
                      <el-option
                        v-for="(group, index) in submitAgencyArr"
                        :value="group.dimCde"
                        :key="index"
                        :label="group.dimNme">
                      </el-option>
                    </el-select>
                </el-form-item>
              </div>

            </el-col>
            <el-col :span="8">
              <div class="grid-content bg-purple-light">
                <el-form-item  class="search_button_com">
                  <el-button :loading='countSubmit_btn' type="primary" @click="onSubmit('formInline')" style="margin-bottom: 5px;" size="small"><i class="el-icon-search"></i>查询</el-button>
                  <el-button  :loading='countSubmit_btn' type="primary" plain size="small" style="margin-bottom: 5px;" @click="restForm('formInline')"><i class='el-icon-delete'></i>重置</el-button>
                   <el-button v-btn="'fundDisc.insert.info'" :loading='countSubmit_btn' type="primary"  plain  @click="addData()" style="margin-bottom: 5px; " size="small">
                    <i class="el-icon-circle-plus-outline"></i>新增
                  </el-button>
                </el-form-item>
              </div>
            </el-col>
          </el-row>
        </el-form>
  </div>
 <div class="forms_table_title">
      <i class="el-icon-s-data"></i>产品信息披露列表
    </div>
 <el-table
      ref="multipleTable"
      @selection-change="handleSelectionChange"
      :data="tableData"
      border
      stripe
      @sort-change="handleSortChange"
      v-loading="tableLoading"
      style="width: 100%"
    >
      <el-table-column
        type="index"
        label="序号"
        fixed
        align = "center"
        width="50">
      </el-table-column>
      <el-table-column
        prop="fundType"
        label="产品类型"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        min-width="90"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{getDataName('fundTypes',scope.row.fundType) | noDataFilter}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="reportType"
        label="报表频率"
         sortable='custom'
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{getDataName('fundann_reportType',scope.row.reportType) | noDataFilter}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="submitAgency"
        label="报表类型"
         sortable='custom'
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{getDataName('fundann_submitComp',scope.row.submitAgency) | noDataFilter}}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="reportDate"
        label="估值基准日"
         sortable='custom'
        :sort-orders="['ascending', 'descending']"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <template v-if="scope.row.reportDate!=='SD'">
            <span>{{getDataName('fundann_reportDate',scope.row.reportDate) | noDataFilter}}</span>
          </template>
          <template v-if="scope.row.reportDate=='SD'">
            <span>{{scope.row.reportFixedDate | noDataFilter}}</span>
          </template>
        </template>
      </el-table-column>

      <el-table-column
        prop="submitDc"
        label="上报截止日"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          
          <template v-if="scope.row.reportDate=='SD'">
            <span>{{scope.row.submitFixedDate | noDataFilter}}</span>
          </template>
          <template v-else-if="scope.row.reportDate=='EDT'">
            <span>T+{{scope.row.anyTradeDay+" "+(scope.row.anyTradeTime || '') | noDataFilter}}</span>
          </template>
          <template v-else>
            <span>{{getDataName('submitDc',scope.row.submitDc)+''+getDataName('submitYm',scope.row.submitYm)+''+getDataName('submitMdAll',scope.row.submitMd) | noDataFilter}}</span>
          </template>
        </template>
      </el-table-column>

      <!-- <el-table-column
        prop="status"
        label="规则状态"
        min-width="150"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span>{{scope.row.status | noDataFilter}}</span>
        </template>
      </el-table-column> -->

      <el-table-column
        prop="remind"
        label="是否配置提醒"
        min-width="100"
        header-align = "left"
        align = "left">
        <template slot-scope="scope">
          <span v-if="scope.row.remind=='1'">是</span>
          <span v-else>否</span>
          <!-- <span v-else>{{scope.row.remind | noDataFilter}}</span> -->
        </template>
      </el-table-column>

      <el-table-column
          label="操作"
          min-width = "120"
          fixed="right"
          align="center">
          <template slot-scope="scope">
             <el-button v-btn="'fundDisc.update.info'" :loading='countSubmit_btn' type="primary" size="small" @click="editData(scope.row)">修改</el-button>
             <el-button type="primary" size="small" @click="config_open(scope.row)">配置提醒</el-button>
          </template>
      </el-table-column>
    </el-table>
     <Pagination :total="total" :page="pageNum" :limit = "pageSize" @pagination = "Pagination"></Pagination>


     <!-- 新增代办 -->
    <el-dialog v-dialogDrag ref="dialog_" :title="countTitle" :before-close="handleClose" customClass="productSearchWidth" center :visible.sync="countDialog" :close-on-click-modal="false">
            <el-button type="primary" v-show="!isEdit"  plain  @click="insertEvent" style="margin-bottom: 5px; " size="small">
                  <i class="el-icon-circle-plus-outline"></i>新增
            </el-button>
          <el-button type="danger"  v-show="!isEdit" plain  @click="removeEvent" style="margin-bottom: 5px; " size="small">
                  <i class="el-icon-delete"></i>移除
          </el-button>
            <!-- <el-button type="warning"  plain  @click="revertEvent" style="margin-bottom: 5px; " size="small">
                    <i class="el-icon-back"></i>还原
            </el-button> -->
        <div v-if="countDialog">
        <vxe-table
          border
          show-overflow
          keep-source
          ref="xTable"
          class="my_table_insert"
          max-height="400"
          :cell-class-name="cellClassName"
          :header-cell-class-name="headerCellClassName"
          @edit-actived="editActivedEvent"
          :edit-rules="validRulesContact"
          :data="tableDataEdit"
          :edit-config="{trigger: 'click', mode: 'row', icon: 'fa fa-pencil', showStatus: true }">
          <vxe-table-column type="checkbox" width="60"></vxe-table-column>
          <vxe-table-column type="seq" title="序号" width="60"></vxe-table-column>
          <vxe-table-column field="fundType" title="产品类型" :edit-render="{name: '$select', options: fundTypeArr, optionProps: {value: 'dimCde', label: 'dimNme'}}"></vxe-table-column>
          <vxe-table-column field="reportType" title="报表频率" :edit-render="{name: '$select', options: reportTypeArr, optionProps: {value: 'dimCde', label: 'dimNme'}}"></vxe-table-column>
          <vxe-table-column field="submitAgency" title="报表类型" :edit-render="{name: '$select', options: submitAgencyArr, optionProps: {value: 'dimCde', label: 'dimNme'}}"></vxe-table-column>
          <!-- <vxe-table-column title='估值基准日'>
            <vxe-table-column field="reportDate" title="估值基准日" :edit-render="{name: '$select', options: reportDateArr, optionProps: {value: 'dimCde', label: 'dimNme'},events: {change: reportDateChangeEvent}}"></vxe-table-column>
            <vxe-table-column field="date" title="固定日期" :edit-render="{name: '$input', props: {type: 'date',disabled: sdDisabled}}"></vxe-table-column>
          </vxe-table-column> -->
          <!-- <vxe-table-column field="reportDate" title="估值基准日" :edit-render="{name: '$select', options: reportDateArr, optionProps: {value: 'dimCde', label: 'dimNme'},events: {change: reportDateChangeEvent}}"></vxe-table-column> -->
          <!-- vue 2.6.0以上版本 #edit="{row}"  |  vue 2.6.0以下版本（本项目vue2.5.17版本） slot="edit" slot-scope="{ row }"  -->
            <!-- <template #edit="{row}"> -->
          <vxe-table-column field="reportDate" title="估值基准日" :edit-render="{}">
            <template slot="edit" slot-scope="{ row }">
              <div class="display_flex">
              <template>
                <vxe-select v-model="row.reportDate" @change="reportDateChangeEvent({row})" placeholder="请选择" transfer>
                  <vxe-option
                    v-for="item in reportDateArr"
                    :key="item.dimCde"
                    :label="item.dimNme"
                    :value="item.dimCde">
                  </vxe-option>
                </vxe-select>
              </template>
              <template v-if="row.show">
                <vxe-input type="date" v-model="row.reportFixedDate" placeholder="请选择日期" transfer></vxe-input>
              </template>
              </div>
            </template>
            <template slot="default" slot-scope="{row}">
              <span v-if="!row.show">
                {{getDataName('fundann_reportDate',row.reportDate) || ''}}
              </span>
              <span v-if="row.show">
                {{row.reportFixedDate || ''}}
              </span>
            </template>

          </vxe-table-column>
          <!-- <vxe-table-colgroup title="上报截止日">
            <vxe-table-column title='当/次' field="submitDc" border=false width="80" :edit-render="{name: '$select', props:{disabled:!sdDisabled}, options: submitDcArr, optionProps: {value: 'dimCde', label: 'dimNme'}}"></vxe-table-column>
            <vxe-table-column title='年/月' field="submitYm" border=false width="80" :edit-render="{name: '$select', props:{disabled:!sdDisabled}, options: submitYmArr, optionProps: {value: 'dimCde', label: 'dimNme'},events: {change: submitYmChangeEvent}}"></vxe-table-column>
            <vxe-table-column title="截止日" field="submitMd" border=false :edit-render="{name: '$select', props:{disabled:!sdDisabled}, options: submitMdArr, optionProps: {value: 'dimCde', label: 'dimNme',disabled:'disable'}}"></vxe-table-column>
            <vxe-table-column field="date1" title=" " :edit-render="{name: '$input', props: {type: 'date',disabled: sdDisabled}}"></vxe-table-column>
          </vxe-table-colgroup> -->
          
          <vxe-table-column title="上报截止日" width="260" field="submitFixedDate" :edit-render="{}">
            <template slot="edit" slot-scope="{row,column}">
              <div class="display_flex">
              <template v-if="row.tradeShow == '1'">
                <span style="display:flex;">
                <span style="width:34px;line-height:34px;">T+</span>
                <vxe-input v-model="row.anyTradeDay" placeholder="" style="width:90%"></vxe-input>
                <!-- <vxe-input clearable v-model="row.anyTradeTime" placeholder="时间选择" type="time"></vxe-input> -->
                <el-time-picker
                style="width:90%"
                  v-model="row.anyTradeTime"
                  value-format="HH:mm:ss"
                  placeholder="任意时间点">
                </el-time-picker>
                </span>
              </template>
              <template v-if="!row.show&&(!row.tradeShow || row.tradeShow=='0')">
              <vxe-select v-model="row.submitDc" placeholder="请选择" transfer>
                <vxe-option
                  v-for="item in submitDcArr"
                  :key="item.dimCde"
                  :label="item.dimNme"
                  :value="item.dimCde">
                </vxe-option>
              </vxe-select>
              <vxe-select v-model="row.submitYm" placeholder="请选择" transfer @change="submitYmChangeEvent({row})">
                <vxe-option
                  v-for="item in submitYmArr"
                  :key="item.dimCde"
                  :label="item.dimNme"
                  :value="item.dimCde">
                </vxe-option>
              </vxe-select>
              <vxe-select v-if="row.submitYm!='D'" v-model="row.submitMd" placeholder="请选择" transfer @change="submitMdChangeEvent({row,column})">
                <vxe-option
                  v-for="item in submitMdArr"
                  :disabled="item.disable"
                  :key="item.dimCde"
                  :label="item.dimNme"
                  :value="item.dimCde">
                </vxe-option>
              </vxe-select>
              </template>
              <template v-if="row.show">
                <vxe-input type="date" v-model="row.submitFixedDate" placeholder="请选择日期" transfer></vxe-input>
              </template>
              </div>
            </template>
            <template slot="default" slot-scope="{ row }">
              <span v-if="!row.show&&(!row.tradeShow || row.tradeShow=='0')">
                {{getDataName('submitDc',row.submitDc)+''+getDataName('submitYm',row.submitYm)+''+getDataName('submitMdAll',row.submitMd) || ''}}
              </span>
              <span v-if="row.show">
                {{row.submitFixedDate}}
              </span>
              <span v-if="row.tradeShow=='1'">
                T+{{row.anyTradeDay}} {{row.anyTradeTime}}
              </span>
            </template>

          </vxe-table-column>
          
          <!-- <vxe-table-column field="ruleType" title="规则类型" :edit-render="{name: '$select', options: ruleTypeArr, optionProps: {value: 'dimCde', label: 'dimNme'}}"></vxe-table-column> -->
        </vxe-table>
      </div>
      <div slot="footer" class="dialog-footer">
          <el-button size="small" @click="countDialog = false">取 消</el-button>
          <el-button v-btn="saveCode" type="primary" size="small" :loading="countSubmit_btn" @click="countSubmit()">确 定</el-button>
      </div>
    </el-dialog>

    <!-- 配置提醒弹框 -->
    <el-dialog
     v-dialogDragWidth
     ref="dialog__wrapper" 
     center title="配置提醒" 
     customClass="ConfigRemind" 
     :visible.sync="configDialog" 
     @close="configDialogClose"
     :close-on-click-modal="false">
      <el-form label-width="150px" label-position="right">
        <el-form-item label="产品类型">
          <el-input v-model="fundType" disabled></el-input>
          <!-- <el-select v-model="formData.fundType" placeholder="请选择">
            <el-option
              v-for="item in fundTypeArr"
              :key="item.dimCde"
              :label="item.dimNme"
              :value="item.dimCde">
            </el-option>
          </el-select> -->
        </el-form-item>
        <el-form-item label="报表频率">
          <el-input v-model="reportType" disabled></el-input>
          <!-- <el-select v-model="formData.reportType" placeholder="请选择">
            <el-option
              v-for="item in reportTypeArr"
              :key="item.dimCde"
              :label="item.dimNme"
              :value="item.dimCde">
            </el-option>
          </el-select> -->
        </el-form-item>
        <el-form-item label="报表类型">
          <el-input v-model="submitAgency" disabled></el-input>
          <!-- <el-select v-model="formData.submitAgency" placeholder="请选择">
            <el-option
              v-for="item in submitAgencyArr"
              :key="item.dimCde"
              :label="item.dimNme"
              :value="item.dimCde">
            </el-option>
          </el-select> -->
        </el-form-item>
          <el-form-item label="估值基准日">
            <el-input v-model="reportDate" disabled></el-input>
            <!-- <el-select v-model="formData.reportDate" placeholder="请选择">
              <el-option
                v-for="item in reportDateArr"
                :key="item.dimCde"
                :label="item.dimNme"
                :value="item.dimCde">
              </el-option>
            </el-select>
            <template v-if="formData.reportDate=='SD'">
            <el-date-picker
              v-model="formData.reportFixedDate"
              type="date"
              value-format="yyyy-MM-dd"
              placeholder="选择日期">
            </el-date-picker>
            </template> -->
          </el-form-item>
        <el-form-item label="上报截止日">
          <el-input v-model="submitDate" disabled></el-input>
          <!-- <template v-if="formData.reportDate!=='SD'">
            <el-row>
              <el-col :span="8">
              <el-select v-model="formData.submitDc" placeholder="请选择" >
                <el-option
                  v-for="item in submitDcArr"
                  :key="item.dimCde"
                  :label="item.dimNme"
                  :value="item.dimCde">
                </el-option>
              </el-select>
              </el-col>
              <el-col :span="8">
              <el-select v-model="formData.submitYm" placeholder="请选择">
                <el-option
                  v-for="item in submitYmArr"
                  :key="item.dimCde"
                  :label="item.dimNme"
                  :value="item.dimCde">
                </el-option>
              </el-select>
              </el-col>
              <el-col :span="8">
              <el-select v-model="formData.submitMd" placeholder="请选择">
                <el-option
                  v-for="item in submitMdArr"
                  :disabled="item.disable"
                  :key="item.dimCde"
                  :label="item.dimNme"
                  :value="item.dimCde">
                </el-option>
              </el-select>
              </el-col>
            </el-row>
          </template>
          <template v-if="formData.reportDate=='SD'">
            <el-date-picker
              v-model="formData.submitFixedDate"
              type="date"
              value-format="yyyy-MM-dd"
              placeholder="选择日期">
            </el-date-picker>
          </template> -->
        </el-form-item>
      </el-form>
      <el-form :model="formData" ref="formData" :rules="formDataRules" label-width="150px" label-position="right">
        <el-row>
          <el-col :span="12">
            <el-form-item label="通知类型" prop="noticeType">
              <el-select v-model="formData.noticeType" @change="noticeTypeChange" placeholder="请选择">
                <el-option
                  v-for="item in czlxArr"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </el-form-item>
              </el-col>
              <el-col :span="12">
            <el-form-item v-if="formData.noticeType=='1'" label="到达后时间(分钟)" prop="receivedNoticeTime">
              <el-input  placeholder="请输入" v-model="formData.receivedNoticeTime"></el-input>
            </el-form-item>
            <el-form-item v-if="formData.noticeType=='2'" label="截止时间" prop="cutNoticeTime">
              <el-time-picker
                value-format='HH:mm:ss'
                v-model="formData.cutNoticeTime"
                placeholder="任意时间点">
              </el-time-picker>
            </el-form-item>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="12">
            <el-form-item label="通知频率" prop="noticeFrequency">
              <el-select v-model="formData.noticeFrequency" @change='noticeFrequencyChange' placeholder="请选择">
                <el-option
                  v-for="item in tzplArr"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
                </el-option>
              </el-select>
            </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item v-if="formData.noticeFrequency=='zdy'" label="通知次数" prop="noticeFrequencyCount">
                  <el-input  placeholder="请输入通知次数"  v-model="formData.noticeFrequencyCount"></el-input>
                </el-form-item>
                <el-form-item v-if="formData.noticeFrequency&&formData.noticeFrequency!='1'" label="通知间隔(分钟)" prop="noticeFrequencyTime">
                  <el-input  placeholder="请输入通知间隔（分钟）"  v-model="formData.noticeFrequencyTime"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item label="通知人员" prop="userList">
              <selectContacts ref="selectContacts" v-model="formData.userList"></selectContacts>
            </el-form-item>
        <el-form-item label="通知方式" prop="noticeSmg">
                <el-checkbox label="短信" v-model="formData.noticeSmg" :true-label= 1 :false-label= 0></el-checkbox>
                <el-checkbox label="邮件" v-model="formData.noticeEmail" :true-label= 1 :false-label= 0></el-checkbox>
            </el-form-item>
            <div class="tongzhi_">
            <el-form-item style="width:100%" label="通知主题" prop="noticeSubject">
          <el-input
            type="textarea"
            :autosize="{ minRows: 2}"
            placeholder="请输入内容"
            v-model="formData.noticeSubject">
          </el-input>
        </el-form-item>
          <el-select v-model="ysxx1" placeholder="插入要素信息"
            @change='selectchange1'
          >
            <el-option
              v-for="item in ysxxArr"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
          </el-select>
            </div>
            <div class="tongzhi_">
        <el-form-item style="width:100%" label="通知正文" prop="noticeContent">
          <el-input
            type="textarea"
            :autosize="{ minRows: 2}"
            placeholder="请输入内容"
            v-model="formData.noticeContent">
          </el-input>
        </el-form-item>
            <el-select v-model="ysxx2" placeholder="插入要素信息"
              @change='selectchange2'
            >
              <el-option
                v-for="item in ysxxArr"
                :key="item.value"
                :label="item.label"
                :value="item.value">
              </el-option>
            </el-select>
            </div>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="configDialog = false" :loading="config_loading">取 消</el-button>
        <el-button type="primary" size="small" @click="configSubmit" :loading="config_loading">保 存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import selectContacts from '@/components/selectContacts/index2'
 import Pagination from '@/components/Pagination'
 import commonFun from '@/filters/new_common'
 import pageApi from "@/api/product/productDisclosure";
 import $ from 'jquery'
 import productDictionary from "@/dataDictionary/product";
export default {
    name: 'productDisclosure',
    components: {
      Pagination,selectContacts
    },
    data() {
      const openNoticeValid=(rule, value, callback)=>{
        let noticeSmg=this.formData.noticeSmg;
        let noticeEmail=this.formData.noticeEmail;
        if(noticeSmg || noticeEmail){
          callback()
        }else{
          callback(new Error('请至少选择一种通知方式'))
        }
      }
      const reportDateValid=(value)=>{
        // console.log(value);
        if(value.row.reportDate){
          if(value.row.reportDate=='SD'){
            if(value.row.reportFixedDate){

            }else{
              return new Error('请选择估值基准日');
            }
          }
        }else{
          return new Error('请选择估值基准日');
        }
      }
      const submitDateValid=(value)=>{
        console.log('submitDateValid');
        if(value.row.reportDate=='SD'){
          if(value.row.submitFixedDate){

          }else{
            return new Error('请选择上报截止日');
          }
        }
        if(value.row.reportDate!=='SD' && value.row.reportDate!=='EDT'){
          if(value.row.submitYm != "D"){
            // console.log('月，年');
            if(value.row.submitDc && value.row.submitYm && value.row.submitMd){
  
            }else{
              return new Error('请选择上报截止日');
            }
          }
          if(value.row.submitYm == "D"){
            // console.log('日，周');
            if(value.row.submitDc && value.row.submitYm){
  
            }else{
              return new Error('请选择上报截止日');
            }
          }
        }
        if(value.row.reportDate=="EDT"){
          if(value.row.anyTradeDay){
            let reg = /^[0-5]$/;
            if(reg.test(value.row.anyTradeDay)){

            }else{
              return new Error('请输入0-3的数字');
            }
          }else{
            return new Error('请填写上报截止日');
          }
        }
      }
      return {
        sdDisabled:true,
          formInline:{
            fundType:'',//产品类型
             orderString: '', //列表排序
            reportType:'',
            submitAgency:'',
            limit: 50,//条数
            offset:0
          },
          total: 0, //列表条数
          pageNum:1, //页码
          pageSize: 50,//条数
          fundTypeArr:[], //产品类型数组
          tableData:[{fundCode:'001'}],//列表数据
          tableLoading:false, //列表加载
          tableMultipleSelection:[],
          countDialog: false, // 弹窗
          configDialog:false, //配置提醒弹框
          countTitle:"",//标题
          sexList:[],
          isEdit:false,
         
          countSubmit_btn:false,
          tableDataEdit:[],
          fundTypeArr:[],//基金类型
          reportTypeArr:[],//报告类型
          submitAgencyArr:[],//提交机构
          reportDateArr:[],//报告日期
          reportDateArr1:[],
          submitDcArr:[],//提交截止日-次，当
          submitYmArr:[],//提交截止日-年，月
          submitMdYArr:[], //提交截止日
          submitMdMArr:[], //提交截止日
          submitMdWArr:[], //提交截止日
          submitMdArr:[], //提交截止日
          submitMdAllArr:[],
          submitData:{},
          // 配置提醒
          formData:{
            noticeSmg:0,
            noticeEmail:0,
            noticeSubject:'',
            noticeContent:'',
            noticeType:"",
            receivedNoticeTime:"",
            cutNoticeTime:"",
            noticeFrequency:"",
            noticeFrequencyTime:"",
            noticeFrequencyCount:"",
            userList:[],
          },
          config_loading:false,
          fundType:"", //配置提醒-产品类型
          reportType:"", //配置提醒-报表频率
          submitAgency:"", //配置提醒-报表类型
          reportDate:"", //配置提醒-估值基准日
          submitDate:"", //配置提醒-上报截止日
          czlxArr:[
            {label:'到达后',value:'1'},
            {label:'截止前',value:'2'},
          ],
          tzplArr:[
            {label:'1次',value:'1'},
            {label:'2次',value:'2'},
            {label:'3次',value:'3'},
            {label:'自定义次数',value:'zdy'},
            {label:'循环通知',value:'xh'},
          ],
          rowId:'',
          noticeId:"",//配置提醒编辑id
          ysxx1:'',
          ysxx2:'',
          ysxxArr:[
            {label:'报表名称',value:'$name$'},
            {label:'报送日期',value:'$date$'},
            {label:'产品类型名称',value:'$fundType$'},
            {label:'报表类型',value:'$submitAgency$'},
            {label:'报表频率',value:'$reportType$'},
            {label:'产品代码',value:'$fundCode$'},
            {label:'产品名称',value:'$fundName$'},
          ],
          ruleTypeArr:[
            {dimCde:'PT',dimNme:'普通'},
            {dimCde:'LS',dimNme:'临时'},
          ],
           //联系人校验规则
          validRulesContact: {
                fundType: [
                  { required: true, message: '请选择产品类型' }
                  // { validator: contactNameValid }
                ],
                reportType: [
                  { required: true, message: '请选择报表频率' },
                ],
                submitAgency: [
                  { required: true, message: '请选择报表类型' },
                ],
                reportDate: [
                  // { required: true, message: '请选择报告日期' },
                  { required: true, message: '请选择报告日期',validator: reportDateValid, trigger: 'change' },
                ],
                submitFixedDate: [
                  // { required: true, message: '请选择报告日期' },
                  { required: true, message: '请选择上报截止日',validator: submitDateValid, trigger: 'change' },
                ],
                submitDc: [
                  { required: true, message: '请选择提交截止日当/次' },
                ],
                submitYm: [
                  { required: true, message: '请选择提交截止日年/月' },
                ],
                submitMd: [
                  { required: true, message: '请选择提交截止日' },
                ],

                
          },
          // 配置提醒校验
          formDataRules:{
            noticeSmg:[
              { required: true, message: '请至少选择一种通知方式',validator: openNoticeValid, trigger: 'change' },
            ],
            noticeType:[
              { required: true, message: '请选择通知类型', trigger: 'change' },
            ],
            noticeFrequencyCount:[
              { required: true, message: '请输入通知次数', trigger: 'change' },
              { pattern: /^([1-9]\d{0,3}|10000)$/, message: '请输入1-10000之间的整数', trigger: 'change' },
            ],
            noticeFrequencyTime:[
              { required: true, message: '请输入通知间隔', trigger: 'change' },
              { pattern: /^([1-9]\d{0,3}|10000)$/, message: '请输入1-10000之间的整数', trigger: 'change' },
            ],
            noticeTime:[
              { required: true, message: '请输入时间', pattern:"" , trigger: 'change' },{}
            ],
            cutNoticeTime:[
              { required: true, message: '请输入时间', pattern:"" , trigger: 'change' }
            ],
            receivedNoticeTime:[
              { required: true, message: '请输入时间', pattern:"" , trigger: 'change' },
              { pattern: /^([1-9]\d{0,3}|10000)$/, message: '请输入1-10000之间的整数', trigger: 'change' },
            ],
            noticeFrequency:[
              { required: true, message: '请选择通知频率', trigger: 'change' },
            ],
            userList:[
              { required: true, message: '请选择通知人员', trigger: 'change' },
            ]
          },
          saveCode:'',
          filters_fundType:[
            {text:'公募基金',value:'GJ'},
            {text:'资管计划',value:'ZH'},
            {text:'全部',value:'ALL'},
          ],
          filters_reportType:[],
          search: '',
          visible: false,
      }
    },
    //页面加载后触发
   mounted(){
     this.getEdims();
     this.selectAll(true);
   },
   methods: {
     cellClassName ({ row, rowIndex, column, columnIndex }) {
        return 'vxe-cell-class-name'
      },
      headerCellClassName ({ column, columnIndex }) {
        return 'vxe-header-cell-class-name'
      },
     filterHandler(value, row, column){
      //  console.log(value, row, column);
       const property = column['property'];
        return row[property] === value;
     },
      //列表选择
     handleSelectionChange(val) {
      this.tableMultipleSelection = val;
    },
    //排序
    handleSortChange(val) {
      this.isSubmit = false
      this.formInline.orderString = commonFun.orderByString(val);
      this.selectAll(false);
    },
    //分页
    Pagination(val) {
      this.pageSize = val.limit; //页面条数
      this.pageNum = val.page;//页码
      this.formInline.offset = (val.page -1) * val.limit;
      this.formInline.limit = val.limit; //页面条数
      this.isSubmit = false;
      this.selectAll(false);
    },
     restForm(formName){
        var self = this;
        self.$refs[formName].resetFields();
     },
     pageCheckClick(data){

     },
     addData(){
         this.countDialog = true; // 弹窗
         this.countTitle = '新增';//标题
         this.isEdit = false;
         this.tableDataEdit = [];
         this.saveCode = 'fundDisc.insert.save';
        // setTimeout(function(){
        //         var aa = $('.vxe-table--main-wrapper thead tr');
        //         aa[1].style.display="none";
        //          var b = $('.vxe-table--main-wrapper thead tr th');
        //          b[6].innerHTML = '<div class="vxe-cell"><i class="vxe-required-icon"></i><i class="vxe-edit-icon fa fa-pencil"></i><span class="vxe-cell--title">提交截止日</span></div>';
        //       },300)
        
     },
     editData(row){
        this.countDialog = true; // 弹窗
        this.countTitle = '修改';//标题
        this.isEdit = true;
         this.saveCode = 'fundDisc.update.save';
       
       let data = {};
       data.id =  row.id;
       data.fundType=  row.fundType;
       data.reportType=  row.reportType;
       data.submitAgency=  row.submitAgency;
       data.reportDate=  row.reportDate || '';
       data.submitDc=  row.submitDc || '';
       data.submitYm=  row.submitYm || '';
       data.show=  row.show || false;
       data.tradeShow=  row.tradeShow || false;
       data.anyTradeDay=  row.anyTradeDay || '';
       data.anyTradeTime=  row.anyTradeTime || '';
       data.reportFixedDate=  row.reportFixedDate || '';
       data.submitFixedDate=  row.submitFixedDate || '';
       if(data.submitYm){
              if(data.submitYm === 'Y'){
                let arr = this.submitMdYArr;
                this.submitMdArr =  arr;
              }else if(data.submitYm === 'M'){
                let arr = this.submitMdMArr;
                this.submitMdArr =  arr;
              }else if(data.submitYm === 'W'){
                let arr = this.submitMdWArr;
                this.submitMdArr =  arr;
              }
                 
            }else{
               this.submitMdArr = [];   
           }
       data.submitMd=  row.submitMd;
       this.tableDataEdit = [];
       let arr =[];
       arr.push(data);
       this.tableDataEdit = arr;
        // setTimeout(function(){
        //         var aa = $('.vxe-table--main-wrapper thead tr');
        //         aa[1].style.display="none";
        //             var b = $('.vxe-table--main-wrapper thead tr th');
        //          b[6].innerHTML = '<div class="vxe-cell"><i class="vxe-required-icon"></i><i class="vxe-edit-icon fa fa-pencil"></i><span class="vxe-cell--title">提交截止日</span></div>';
        //       },300)
     },
    //  配置提醒
     config_open(row){
      //  console.log(row);
      this.configDialog=true;
       this.fundType = this.getDataName('fundTypes',row.fundType) || '';
       this.reportType = this.getDataName('fundann_reportType',row.reportType) || '';
       this.submitAgency = this.getDataName('fundann_submitComp',row.submitAgency) || '';
       if(row.reportDate=="SD"){
         this.reportDate = row.reportFixedDate || ''
       }else{
         this.reportDate = this.getDataName('fundann_reportDate',row.reportDate) || '';
       }
       if(row.reportDate=="SD"){
         this.submitDate = row.submitFixedDate || ''
       }else if(row.reportDate=="EDT"){
         this.submitDate = "T+"+row.anyTradeDay+" "+(row.anyTradeTime || '')
       }else{
         this.submitDate = this.getDataName('submitDc',row.submitDc)+''+this.getDataName('submitYm',row.submitYm)+''+this.getDataName('submitMdAll',row.submitMd)
       }
       
       this.rowId = row.id;
      this.getAnnInfo(row)
      //  this.$nextTick(()=>{
      //    this.$refs['formData'].resetFields();
      //  })
     },
     getAnnInfo(row){
       let params = {annId:row.id}
       pageApi.getAnnInfo(params).then((res)=>{
         if(res.data.status==200){
           if(res.data.data){
             let data = res.data.data;
             this.formData.noticeType = data.noticeType || '';
             this.formData.receivedNoticeTime = data.receivedNoticeTime || '';
             this.formData.cutNoticeTime = data.cutNoticeTime || '';
             this.formData.noticeFrequency = data.noticeFrequency || '';
             this.formData.noticeFrequencyTime = data.noticeFrequencyTime || '';
             this.formData.noticeFrequencyCount = data.noticeFrequencyCount || '';
             this.formData.userList = data.userList || [];
             this.formData.noticeSmg = data.noticeSmg-0 || 0;
             this.formData.noticeEmail = data.noticeEmail-0 || 0;
             this.formData.noticeSubject = data.noticeSubject || '';
             this.formData.noticeContent = data.noticeContent || '';
             this.noticeId = data.noticeId || ''
           }else{
              this.$nextTick(()=>{
                this.$refs['formData'].resetFields();
              })
              this.formData.noticeSmg = 0;
              this.formData.noticeEmail = 0;
              this.noticeId = ''
           }
         }else{
           this.$message({
             type:"error",
             message:res.data.data || "获取配置信息失败！"
           })
         }
       })
     },
     configDialogClose(){
       this.fundType = ''
       this.reportType = ''
       this.submitAgency = ''
       this.reportDate = ''
       this.submitDate = ''
       this.$nextTick(()=>{
         this.$refs['formData'].resetFields();
       })
        this.$refs.selectContacts.remove_all()
       this.formData.noticeSmg = 0;
        this.formData.noticeEmail = 0;
     },
     configSubmit(){
       
       this.$refs['formData'].validate((valid)=>{
         if(valid){
           this.formDataSubmit()
         }else{
           console.log('err');
           return false
         }
       })
     },
    formDataSubmit(){
      console.log('formDataSubmit');
      let data = JSON.parse(JSON.stringify(this.formData));
      let params= {};
      params = commonFun.parameterSrcFull(data)
      if(params.noticeType=='1'){
        params.cutNoticeTime=''
      }else if(params.noticeType=='2'){
        params.receivedNoticeTime=''
      }
      params.annId = this.rowId;
      if(this.noticeId){
        params.noticeId = this.noticeId;
      }
      // console.log(params);
      this.config_loading = true;
      pageApi.cmdnotice_add(params).then(res=>{
        if(res.data.status==200){
          this.$message({
            type:"success",
            message:"保存成功！"
          })
          this.config_loading = false;
          this.configDialog=false;
          this.selectAll(false);
        }else{
          this.$message({
            type:"error",
            message: res.data.message || "保存失败！"
          })
          this.config_loading = false;
        }
      }).catch(()=>{
        this.$message({
          type:"error",
          message: res.data.message || "保存失败！"
        })
        this.config_loading = false;
      })
     },
    selectchange1(val){
      this.formData.noticeSubject=this.formData.noticeSubject+val
    },
    selectchange2(val){
      this.formData.noticeContent=this.formData.noticeContent+val
    },
    editActivedEvent({row}){
      this.sdDisabled=row.reportDate!=='SD'
      if(row.reportDate!='SD'){
        // row.date=''
        row.show = false;
      }
      if(row.reportDate=='SD'){
        row.show = true;
      }
    },
    reportTypeChangeEvent({row}){
      // console.log(row);
      if(row.reportType=='W'){
        this.reportDateArr = this.reportDateArr2;
      }else{
        this.reportDateArr = this.reportDateArr1;
        row.reportDate = ''
      }
    },
    reportDateChangeEvent({row}){
      // console.log('估值基准日',row.reportDate);
      this.sdDisabled=row.reportDate!=='SD'
      if(row.reportDate!='SD'){
        row.show = false;
        // row.submitFixedDate='';
        // row.reportFixedDate='';
      }
      if(row.reportDate=='SD'){
        row.show = true;
        row.submitDc='';
        row.submitYm='';
        row.submitMd='';
      }
      if(row.reportDate=="EDT"){
        row.tradeShow="1";
      }else{
        row.tradeShow="0";
      }

    },
    submitMdChangeEvent({row,column}){
      // console.log(row,column);
      this.$refs.xTable.clearActived()//清除单元格激活状态
      // this.$refs.xTable.setActiveCell(row,'fundType')//设置单元格为激活状态
      this.$refs.xTable.setActiveRow(row)
    },
     handleClose(done) {
        done();
      },
      insertEvent () {
          const record = {}
          this.$refs.xTable.insert(record).then(({ row }) => {
            this.$refs.xTable.setActiveCell(-1, 'sex')
            this.$refs.xTable.setActiveRow(row)
          })
        },
       
        removeEvent () {
          const selectRecords = this.$refs.xTable.getCheckboxRecords()
          if (selectRecords.length) {
             this.$confirm('您确定要删除选中的数据吗?','提示',{
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
              }).then(() => {
                  this.$refs.xTable.removeCheckboxRow()
              }).catch(() => {
                this.$message.closeAll();
              this.$message({
                type: 'info',
                message: '已取消'
                });
              
          })
            
          } else {
            this.$message.closeAll();
            this.$message({type: 'error',message: '请至少选择一条数据'});
          }
        },
        revertEvent () {
           this.$confirm('您确定要还原数据吗?','提示',{
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
              }).then(() => {
                   this.$refs.xTable.revertData()
              }).catch(() => {
                this.$message.closeAll();
              this.$message({
                type: 'info',
                message: '已取消'
                });
          })
       },
       //查询
    onSubmit(flag){
        this.isSubmit = true;
        if(flag){
        this.pageNum = 1;
        this.formInline.offset = 0;
      }
     
        let data = this.formInline;
        this.submitData.fundType = data.fundType; //产品代码
        this.submitData.orderString = data.orderString;//列表排序
        this.submitData.reportType = data.reportType;//
        this.submitData.submitAgency = data.submitAgency;//
        this.submitData.limit = data.limit;//条数
        this.submitData.offset = data.offset;//分页
        this.selectAll(true);
    },
    selectAll(flag){
      this.tableLoading = true;
      this.countSubmit_btn = true
      let data = this.formInline;
      let data2 = this.submitData;
      let isSubmit = this.isSubmit;
      if(isSubmit){
          data = data2;
      }
      // 消除没有值的参数
      let params = commonFun.parameterSrc(data);
      if(flag){
        this.pageNum = 1;
        this.formInline.offset = 0;
        params.offset = 0;
      }
      pageApi.getDataSourceList(params).then(response => {
        if(response.data.status === 200){
          this.tableData = response.data.data.rows;
          // 页面总条数
          this.total = response.data.data.total;
        }
        else{
          this.tableData = [];
          this.total = 0;
          this.formInline.limit = 50;
           this.pageSize = 50;
          this.pageNum = 1;
          this.formInline.offset = 0;

        }
        this.tableLoading = false;
        this.countSubmit_btn = false

      }).catch(() => {
        this.tableData = [];
        this.total = 0;
        this.pageSize = 50;
        this.formInline.limit = 50;
        this.pageNum = 1;
        this.formInline.offset = 0;
        this.tableLoading = false;
        this.countSubmit_btn = false
      })
    },
    countSubmit(){

        if(this.isEdit){
           this.fullValidEvent();
          //  this.updateData();
        }else{
            let tableDataEdit  = [];
            tableDataEdit  = this.$refs.xTable.getTableData().tableData;
            // console.log(this.$refs.xTable.getTableData());
            if(tableDataEdit.length === 0){
                this.$message.closeAll()
                this.$message({
                  message: '列表为空',
                  type: 'warning'
                });
                return;
            }
            this.fullValidEvent()
              
            
          
        }
    },
     saveData(){
       
         
          this.$confirm("确定新增?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        })
          .then(() => {
            let params = {};
            let tableDataEdit  = [];
            tableDataEdit  = this.$refs.xTable.getTableData().tableData;
            tableDataEdit.forEach(item=>{
              if(item.reportDate=='SD'){
                item.submitDc='';
                item.submitYm='';
                item.submitMd='';
                item.anyTradeDay='';
                item.anyTradeTime='';
              }else if(item.reportDate=="EDT"){
                item.submitDc='';
                item.submitYm='';
                item.submitMd='';
                item.submitFixedDate='';
                item.reportFixedDate='';
              }else{
                item.submitFixedDate='';
                item.reportFixedDate='';
                item.anyTradeDay='';
                item.anyTradeTime='';
              }
            })
            for(let i=0;i<tableDataEdit.length;i++){
              for(let j=i+1;j<tableDataEdit.length;j++){
                if(
                  tableDataEdit[i].fundType == tableDataEdit[j].fundType &&
                  tableDataEdit[i].reportType == tableDataEdit[j].reportType &&
                  tableDataEdit[i].reportDate == tableDataEdit[j].reportDate &&
                  tableDataEdit[i].reportFixedDate == tableDataEdit[j].reportFixedDate &&
                  tableDataEdit[i].submitAgency == tableDataEdit[j].submitAgency &&
                  tableDataEdit[i].submitDc == tableDataEdit[j].submitDc &&
                  tableDataEdit[i].submitFixedDate == tableDataEdit[j].submitFixedDate &&
                  tableDataEdit[i].submitMd == tableDataEdit[j].submitMd &&
                  tableDataEdit[i].submitYm == tableDataEdit[j].submitYm &&
                  tableDataEdit[i].anyTradeDay == tableDataEdit[j].anyTradeDay &&
                  tableDataEdit[i].anyTradeTime == tableDataEdit[j].anyTradeTime
                ){
                  this.$message({
                    message: `列表数据第${i+1}条与第${j+1}条重复，请检查！`,
                    type: 'error'
                  });
                  this.$nextTick(()=>{
                    let row = this.$refs.xTable.getTableData().tableData[i];
                    this.$refs.xTable.setActiveRow(row);
                    // let row2 = this.$refs.xTable.getTableData().tableData[j];
                    // this.$refs.xTable.setActiveRow(row2);
                  })
                  return 
                }
              }
            }
            params.productDiscDtoList = tableDataEdit;
            // console.log(params);return
            this.countSubmit_btn = true
            // console.log(params);

            // this.countSubmit_btn = false;
            // return
            pageApi.addDataSource(params).then(response => {
              if(response.data.status === 200){
                // 关闭移动指标弹框
               
                this.$message.closeAll()
                this.$message({
                  message: '新增成功',
                  type: 'success'
                });
                // 刷新列表
                 this.countDialog = false; // 弹窗
                  this.isSubmit = false;
                this.selectAll(true);

              }
              else{
                // 关闭移动指标弹框
               // this.countDialog = false;
                this.$message.closeAll()
                this.$message({
                  message: response.data.message || '新增失败',
                  type: 'warning'
                });
              }
              this.countSubmit_btn = false;

            }).catch(() => {
              // 关闭移动指标弹框
            
              this.countSubmit_btn = false;

              this.$message.closeAll()
              this.$message({
                message: '新增失败',
                type: 'warning'
              });

            })

          })
          .catch(() => {
            // 关闭移动指标弹框
           
            this.countSubmit_btn = false;
          });
        },
        updateData(){
          if(this.$refs.xTable){
              let  tableData1  = this.$refs.xTable.getTableData().tableData[0];
              if(tableData1.submitYm){
                if(tableData1.submitYm=="D"){
                  tableData1.submitMd= ''
                }else{
                  if(tableData1.submitMd==''){
                    this.$message.closeAll();
                    this.$message({
                      message: '请选择上报截止日',
                      type: 'warning'
                    });
                    // this.$refs.xTable.setActiveRow(tableData1)
                    this.$nextTick(()=>{
                      this.$refs.xTable.setActiveCell(tableData1,'submitFixedDate')
                    })
                    return 
                  }
                }
              }
            }
          this.$confirm("确定修改?", "提示", {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning"
        })
          .then(() => {
          
            let params = {};
            let tableDataEdit  = [];
            if(this.$refs.xTable){
                tableDataEdit  = this.$refs.xTable.getTableData().tableData;
            }
            
           if(tableDataEdit && tableDataEdit.length>0){
              params.id =  tableDataEdit[0].id;
              params.fundType=  tableDataEdit[0].fundType;
              params.reportType=  tableDataEdit[0].reportType;
              params.submitAgency=  tableDataEdit[0].submitAgency;
              params.reportDate=  tableDataEdit[0].reportDate;
              if(tableDataEdit[0].reportDate=='SD'){
                params.reportFixedDate = tableDataEdit[0].reportFixedDate;
                params.submitFixedDate = tableDataEdit[0].submitFixedDate;
                params.submitDc= '';
                params.submitYm= '';
                params.submitMd= '';
                params.anyTradeDay= '';
                params.anyTradeTime= '';
              }else if(tableDataEdit[0].reportDate=='EDT'){
                params.reportFixedDate = '';
                params.submitFixedDate = '';
                params.submitDc= '';
                params.submitYm= '';
                params.submitMd= '';
                params.anyTradeDay= tableDataEdit[0].anyTradeDay || '';
                params.anyTradeTime= tableDataEdit[0].anyTradeTime || '';
              }else{
                params.submitDc=  tableDataEdit[0].submitDc;
                params.submitYm=  tableDataEdit[0].submitYm;
                params.submitMd=  tableDataEdit[0].submitMd;
                params.reportFixedDate = '';
                params.submitFixedDate = '';
                params.anyTradeDay= '';
                params.anyTradeTime= '';
              }
              params.show = tableDataEdit[0].show || false;
              params.tradeShow = tableDataEdit[0].tradeShow || '0';
            }
            
            this.countSubmit_btn = true;
           
          //  console.log(params);
          //  this.countSubmit_btn = false;
          //  return
            pageApi.updateDataSource(params).then(response => {
              if(response.data.status === 200){
                // 关闭移动指标弹框
               
                this.$message.closeAll()
                this.$message({
                  message: '修改成功',
                  type: 'success'
                });
               
                 // 刷新列表
                  // 刷新列表
                 this.countDialog = false; // 弹窗
                 this.isSubmit = false;
                this.selectAll(true);
                

              }
              else{
                // 关闭移动指标弹框
               // this.countDialog = false;
                this.$message.closeAll()
                this.$message({
                  message: response.data.message || '修改失败',
                  type: 'warning'
                });
              }
              this.countSubmit_btn = false;
            }).catch(() => {
              // 关闭移动指标弹框
            
              this.countSubmit_btn = false;
              this.$message.closeAll()
              this.$message({
                message: '修改失败',
                type: 'warning'
              });

            })

          })
          .catch(() => {
            // 关闭移动指标弹框
           
            this.countSubmit_btn = false;
          });
        },
        getEdimsGet(val){
               let params = val;
                pageApi.getTransferType(params).then(res =>{
                  let self = this;
                  if(res.data.message === "success"){
                    if(val === 'fundTypes'){
                      this.fundTypeArr = res.data.data||[];//基金类型
					  this.fundTypeArr.unshift({dimCde:"ALL",dimNme:"全部"});
                    }

                    if(val === 'fundann_reportType'){
                      this.reportTypeArr = res.data.data;//基金类型
                      // console.log(this.reportTypeArr);
                      let arr=[]
                      this.reportTypeArr.forEach(item=>{
                        arr.push({text:item.dimNme,value:item.dimCde})
                      })
                      // console.log('arr',arr);
                      this.filters_reportType=arr;
                    }

                    if(val === 'fundann_submitComp'){
                      this.submitAgencyArr = res.data.data;//报表类型
                    }

                    if(val === 'fundann_reportDate'){
                      // this.reportDateArr = res.data.data;//基金类型
                      // this.reportDateArr1 = res.data.data;
                      let weekArr = [
                        {dimCde:'W1',dimNme:'每周一'},
                        {dimCde:'W2',dimNme:'每周二'},
                        {dimCde:'W3',dimNme:'每周三'},
                        {dimCde:'W4',dimNme:'每周四'},
                        {dimCde:'W5',dimNme:'每周五'},
                      ]
                      this.reportDateArr = [...weekArr,...res.data.data];
                    }
                
                  }else{
                    this.$message.closeAll();
                    this.$message.error('初始化数据失败');
                  }

                })

       },
       getEdims(){
         this.getEdimsGet('fundTypes');
         this.getEdimsGet('fundann_reportType');
         this.getEdimsGet('fundann_submitComp');
         this.getEdimsGet('fundann_reportDate');
         this.submitDcArr = productDictionary.submitDc;
         this.submitYmArr = productDictionary.submitYm;
         this.submitMdYArr = productDictionary.submitMdY;
         this.submitMdMArr = productDictionary.submitMdM;
         this.submitMdWArr = productDictionary.submitMdW;
        this.submitMdAllArr =  productDictionary.submitMdMAll;
                
       },
       submitYmChangeEvent({ row }){
            // console.log(row.submitYm);
            let name = row.submitYm;
            row.submitMd = '';
            if(name){
              if(name === 'Y'){
                let data = this.submitMdYArr;
                this.submitMdArr =  data;
              }else if(name === 'M'){
                let data = this.submitMdMArr;
                this.submitMdArr =  data;
              }else if(name === 'W'){
                let data = this.submitMdWArr;
                this.submitMdArr =  data;
              }
              if(name==="D" || name === "W"){
                
              }
                 
            }else{
               this.submitMdArr = [];   
           }
           
        },
         getDataName(val,code){
            if(!code){
               return "";
            }
           if(val === 'fundTypes'){
              //托管人名称
              return commonFun.dictionaryArrToName(this.fundTypeArr,code);
            }
            if(val === 'fundann_submitComp'){
              //托管人名称
              return commonFun.dictionaryArrToName(this.submitAgencyArr,code);
            }
            if(val === 'fundann_reportType'){
              //托管人名称
              return commonFun.dictionaryArrToName(this.reportTypeArr,code);
            }
            if(val === 'fundann_reportDate'){
              //托管人名称
              return commonFun.dictionaryArrToName(this.reportDateArr,code);
            }
             if(val === 'submitDc'){
              //托管人名称
              return commonFun.dictionaryArrToName(this.submitDcArr,code);
            }
             if(val === 'submitYm'){
              //托管人名称
              return commonFun.dictionaryArrToName(this.submitYmArr,code);
            }
             if(val === 'submitMdAll'){
              //托管人名称
              return commonFun.dictionaryArrToName(this.submitMdAllArr,code);
            }
            
         },
       async  fullValidEvent () {
           
              let errMap = '';

            if(this.$refs.xTable){
                  const errMap2 = await this.$refs.xTable.validate().catch(errMap => errMap)
                  errMap = errMap2;
                  if(errMap){
                    this.$message.closeAll()
                    this.$message({
                      message: '请选择必填数据',
                      type: 'warning'
                    });
                    return false
                  }else{
                    if(this.isEdit){
                      this.updateData();
                    }else{
                      this.saveData();
                    }
                  }
                  
            }
              
      },
      noticeFrequencyChange(){
        this.formData.noticeFrequencyTime='';
        this.formData.noticeFrequencyCount='';
      },
      noticeTypeChange(){},

   }

}
</script>

<style lang="scss">
.ConfigRemind{
position: relative;
.pointRB{
            width: 5px;
            height: 5px;
            position: absolute;
            right: 0;
            bottom: 0;
            z-index: 2;
            background-color: red;
          }
}
.productSearchWidth{
  width: 70% !important;
}
.vxe-table--empty-block{
  height: 120px !important;
}
</style>

<style rel="stylesheet/scss" lang="scss" >
     
    .vxe-dropdown--panel {
      z-index: 9999 !important
    }

      .vxe-select--panel {
      z-index: 9998 !important
    }
    .vxe-input--panel.type--date, .vxe-input--panel.type--month, .vxe-input--panel.type--week, .vxe-input--panel.type--year {
         z-index: 9998 !important
    }

   .productDisclosure{
     .ConfigRemind{
       width: 50% !important;
      .tongzhi_{
        display: flex;
      }
     }
     .display_flex {
       display: flex;
     }
   }
</style>

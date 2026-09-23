<template>
  <div class="daily_operations vxe_custom_style">
    <div>
      <el-row>
        <el-col :span="14">
          <h2>
            {{ yyyy }}年{{ mm }}月{{ dd }}日运营报告：
            <span v-if="isSubmit!='1'" style="color:red;">未提交</span>
            <span v-if="isSubmit=='1'" style="color:green;">已被{{staff || ''}}提交</span>
          </h2>
        </el-col>
        <el-col :span="10">
          <div style="text-align: right">
            <el-form ref="formData" :rules="formDataRules" :model="formData" :inline="true" label-width="80px">
              <el-form-item label="" prop="hDate">
                <el-date-picker
                  @change="hDateChange"
                  v-model="formData.hDate"
                  align="right"
                  type="date"
                  size="small"
                  :clearable="false"
                  value-format="yyyy-MM-dd"
                  placeholder="请选择报告日期"
                  :picker-options="pickerOptions">
                </el-date-picker>
              </el-form-item>
            <el-button style="margin-top:3px;" size="small" @click="searchData">查询</el-button>
            <el-button style="margin-top:3px;" size="small" @click="open">参数设置</el-button>
            </el-form>
          </div>
        </el-col>
      </el-row>
    </div>
    <!-- 总体运营情况 -->
    <!-- <div class="forms_table_title">
      <i class="el-icon-s-data"></i>总体运营情况
    </div> -->
    <p class="title_one">一、总体运营情况</p>
    <!-- <div>
      <el-button icon="el-icon-plus" size="small" @click="insertEvent('xTable')"
        >新增</el-button
      >
    </div> -->
    <vxe-table
      ref="xTable"
      class="vxeTable"
      size="mini"
      :data="tableData1"
      border
      show-overflow
      :edit-config="{ trigger: isSubmit!='1'?'click':'', mode: 'cell', showIcon: false }"
      :edit-rules="tableRules1"
      :cell-class-name="cellClassName"
      :header-cell-class-name="headerCellClassName"
      v-loading="tableLoading1"
    >
      <vxe-table-column
        field="vcCheck"
        title="检查项"
        :edit-render="{ autofocus: '.vxe-input--inner' }"
        width="180"
      >
        <template slot="edit" slot-scope="{ row }">
          <vxe-input type="text" v-model="row.vcCheck"></vxe-input>
        </template>
        <template slot="default" slot-scope="{ row }">
          <span>{{ row.vcCheck }}</span>
        </template>
      </vxe-table-column>
      <vxe-table-column field="target" title="指标" :edit-render="{}" width="230">
        <template slot="edit" slot-scope="{ row }">
          <template v-if="row.inputType == '1'">
            <vxe-select
              v-model="row.target"
              placeholder="请选择下拉"
              transfer
              @change="targetChange"
            >
              <vxe-option
                v-for="(item, index) in zhibiaoArr"
                :key="index"
                :value="item.value"
                :label="item.label"
              >
              </vxe-option>
            </vxe-select>
          </template>

          <template v-else>
            <vxe-input type="text" v-model="row.target"></vxe-input>
          </template>
        </template>
        <template slot="default" slot-scope="{ row }">
          <span>{{ row.target }}</span>
        </template>
      </vxe-table-column>
      <vxe-table-column
        field="remark"
        title="备注"
        :edit-render="{ autofocus: '.vxe-input--inner' }"
      >
        <template slot="edit" slot-scope="{ row }">
          <vxe-input type="text" v-model="row.remark"></vxe-input>
        </template>
        <template slot="default" slot-scope="{ row }">
          <span>{{ row.remark }}</span>
        </template>
      </vxe-table-column>
    </vxe-table>

    <!-- 交付物检查报告 -->
    <!-- <div class="forms_table_title">
      <i class="el-icon-s-data"></i>交付物检查报告
    </div> -->
    <p class="title_one">二、交付物检查报告</p>
    <vxe-table
      ref="xTable2"
      class="vxeTable"
      size="mini"
      :data="tableData2"
      border
      :show-overflow="overflow"
      @edit-actived="editActived"
      @edit-closed="editClosed"
      :tooltip-config="{contentMethod:contentMethod}"
      :edit-config="{ trigger: isSubmit!='1'?'click':'', mode: 'cell', showIcon: false }"
      :cell-class-name="cellClassName"
      :header-cell-class-name="headerCellClassName"
      v-loading="tableLoading2"
    >
      <vxe-table-column field="vcCheck" title="检查项"></vxe-table-column>
      <vxe-table-column field="format" title="文件传输格式">
        <template slot-scope="{row}">
          <span v-if="row.format=='qt'">其他</span>
          <span v-else>{{row.format || ''}}</span>
        </template>
      </vxe-table-column>
      <vxe-table-column field="transport" title="传输方式"></vxe-table-column>
      <vxe-table-column field="fileReceive" title="文件接收"></vxe-table-column>
      <vxe-table-column field="planTransport" title="计划文件传输时间"></vxe-table-column>
      <vxe-table-column field="actualTransport" title="实际文件传输时间"></vxe-table-column>
      <vxe-table-column field="status" title="状态检查">
        <template slot-scope="{row}">
          <span v-if="row.status=='0'" class="">正常</span>
          <span v-else-if="row.status=='1'" class="" style="color:red;">异常</span>
          <span v-else class="">{{row.status}}</span>
        </template>
      </vxe-table-column>
      <vxe-table-column
        field="remark"
        title="异常原因备注"
        :edit-render="{  }"
      >
        <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.remark" autosize></el-input>
        </template>
        <template slot="default" slot-scope="{ row }">
          <span style="color:red;">{{row.remark}}</span>
        </template>
      </vxe-table-column>
    </vxe-table>

    <!-- 业务指标项检查报告 -->
    <!-- <div class="forms_table_title">
      <i class="el-icon-s-data"></i>业务指标项检查报告
    </div> -->
    <p class="title_one">三、业务指标项检查报告</p>
    <vxe-table
      ref="xTable3"
      class="vxeTable"
      size="mini"
      :data="tableData3"
      border
      @edit-actived="editActived3"
      @edit-closed="editClosed3"
      :show-overflow="overflow3"
      :edit-config="{ trigger: isSubmit!='1'?'click':'', mode: 'cell', showIcon: false }"
      :cell-class-name="cellClassName"
      :header-cell-class-name="headerCellClassName"
      v-loading="tableLoading3"
    >
      <vxe-table-column field="vcCheck" title="检查项"></vxe-table-column>
      <vxe-table-column field="explain" title="异常情况"></vxe-table-column>
      <!-- <vxe-table-column field="explain" title="指标说明"></vxe-table-column> -->
      <!-- <vxe-table-column field="content" title="指标内容"></vxe-table-column> -->
      <vxe-table-column field="principal" title="检查工作负责人1(经办)"></vxe-table-column>
      <vxe-table-column
        field="principalCheck"
        title="检查工作负责人2(复核)"
      ></vxe-table-column>
      <vxe-table-column field="checkDate" title="检查时间"></vxe-table-column>
      <vxe-table-column field="status" title="状态检查">
        <template slot-scope="{row}">
          <span v-if="row.status=='0'" class="">正常</span>
          <span v-else-if="row.status=='1'" class="" style="color:red;">异常</span>
          <span v-else class="">{{row.status}}</span>
        </template>
      </vxe-table-column>
      <vxe-table-column
        field="remark"
        title="异常原因备注"
        :edit-render="{  }"
      >
      <!-- name: 'input', attrs: { type: 'text' } -->
        <template slot="edit" slot-scope="{ row }">
          <el-input type="textarea" v-model="row.remark" autosize></el-input>
        </template>
        <template slot="default" slot-scope="{ row }">
          <span style="color:red;">{{row.remark}}</span>
        </template>
      </vxe-table-column>
    </vxe-table>

    <!-- 当日值班人员信息 -->
    <!-- <div class="forms_table_title">
      <i class="el-icon-s-data"></i>当日值班人员信息
    </div> -->
    <p class="title_one">四、当日值班人员信息</p>
    <vxe-table
      ref="xTable4"
      class="vxeTable"
      size="mini"
      :data="tableData4"
      border
      show-overflow
      :edit-config="{ trigger: isSubmit!='1'?'click':'', mode: 'cell', showIcon: false }"
      :cell-class-name="cellClassName"
      :header-cell-class-name="headerCellClassName"
      v-loading="tableLoading4"
    >
      <vxe-table-column
        field="organization"
        title="机构"
        :edit-render="{ name: 'input', attrs: { type: 'text' } }"
      ></vxe-table-column>
      <vxe-table-column
        field="staff"
        title="人员"
        :edit-render="{ name: 'input', attrs: { type: 'text' } }"
      ></vxe-table-column>
      <vxe-table-column
        field="phone"
        title="电话"
        :edit-render="{ name: 'input', attrs: { type: 'text' } }"
      ></vxe-table-column>
      <vxe-table-column
        field="email"
        title="邮箱"
        :edit-render="{ name: 'input', attrs: { type: 'text' } }"
      ></vxe-table-column>
    </vxe-table>
    <div style="margin-top:14px;text-align:right;">
      <!-- <el-button size="small" v-btn="'report.dailyOperations.chexiao'">report.dailyOperations.chexiao</el-button> -->
      <el-button v-if="isSubmit!='1'" @click="submitData" :loading="btnLoading">提交</el-button>
      <el-button v-if="isSubmit=='1'" v-btn="'report.dailyOperations.chexiao'" @click="cancel" :loading="btnLoading">撤销提交</el-button>
      <el-button @click="send" v-if="isSubmit=='1'" :loading="btnLoading">日报邮件发送</el-button>
      <el-button @click="downloadFile" v-if="isSubmit=='1'" :loading="btnLoading">下载</el-button>
    </div>

    <el-dialog
      title="参数设置"
      width="75% !important"
      :visible.sync="csszDialogVisible_table"
      :close-on-click-modal="false"
      center
      size="mini"
    >
      <div style="text-align: right; margin-bottom: 5px">
        <el-button @click="canshushezhi('add')">新增</el-button>
      </div>
      <el-table :data="paramsTable" border style="width: 100%" v-loading="tableLoading5">
        <el-table-column prop="vcCheck" label="检查项" min-width="150" show-overflow-tooltip> </el-table-column>
        <el-table-column prop="format" label="文件传输格式" min-width="150" show-overflow-tooltip>
           <template slot-scope="scope">
            <span>{{ dataStatus(scope.row.format, "format") || scope.row.format}}</span>
          </template>
        </el-table-column>
        <el-table-column prop="transport" label="传输方式" min-width="150" show-overflow-tooltip> </el-table-column>
        <el-table-column prop="fileReceive" label="文件接收" min-width="150" show-overflow-tooltip> </el-table-column>
        <el-table-column prop="planTransport" label="计划文件传输时间" min-width="150" show-overflow-tooltip></el-table-column>
        <el-table-column prop="filePath" label="文件路径" min-width="150" show-overflow-tooltip> </el-table-column>
        <!-- <el-table-column prop="offsetType" label="偏移类型" width="150" show-overflow-tooltip>
          <template slot-scope="{row}">
            <span v-if="row.offsetType==1">自然日</span>
            <span v-else-if="row.offsetType==2">交易日</span>
            <span v-else-if="row.offsetType==3">银行间交易日</span>
            <span v-else>{{row.offsetType || '-'}}</span>
          </template>
        </el-table-column>
        <el-table-column prop="offset" label="偏移量" width="150" show-overflow-tooltip> </el-table-column> -->
        <el-table-column prop="frequency" label="频率" min-width="150" show-overflow-tooltip>
          <template slot-scope="scope">
            <span>{{ dataStatus(scope.row.frequency, "frequency") }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" min-width="120" fixed="right">
          <template slot-scope="scope">
            <span>
              <el-button size="small" @click="canshushezhi('edit', scope.row)"
                >编辑</el-button
              >
              <el-button
                size="small"
                type="danger"
                plain
                @click="shanchu(scope.row)"
                >删除</el-button
              >
            </span>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <el-dialog
      title="参数设置"
      width="65% !important"
      :visible.sync="csszDialogVisible"
      :close-on-click-modal="false"
      append-to-body
      center
      @closed="csszDialogVisibleClosed"
    >
      <el-form
        :model="paramsForm"
        :rules="paramsFormRules"
        ref="paramsForm"
        label-width="150px"
        class="params_form"
      >
        <el-form-item label="检查项" prop="vcCheck">
          <el-input v-model="paramsForm.vcCheck"></el-input>
        </el-form-item>
        <el-form-item label="文件传输格式" prop="format">
          <!-- <el-input v-model="paramsForm.format"></el-input> -->
          <el-select v-model="paramsForm.format" placeholder="请选择">
            <el-option
              v-for="item in formatArr"
              :key="item.dimCde"
              :label="item.dimNme"
              :value="item.dimCde"
            >
            </el-option>
          </el-select>
          <el-tooltip placement="right" effect="light">
            <div slot="content">若选择其他，则需在文件路径里填写文件后缀</div>
            <span><i style="color:#ccc;" class="el-icon-warning"></i></span>
          </el-tooltip>
        </el-form-item>
        <el-form-item label="传输方式" prop="transport">
          <el-input v-model="paramsForm.transport"></el-input>
        </el-form-item>
        <el-form-item label="文件接收" prop="fileReceive">
          <el-input v-model="paramsForm.fileReceive"></el-input>
        </el-form-item>
        <el-row>
          <el-col :span="12">
            <el-form-item label="频率" prop="frequency">
              <el-select v-model="paramsForm.frequency" placeholder="请选择">
                <el-option
                  v-for="item in frequencyArr"
                  :key="item.dimCde"
                  :label="item.dimNme"
                  :value="item.dimCde"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="计划文件传输时间" prop="planTransport">
              <!-- <el-date-picker
                v-model="paramsForm.planTransport"
                type="datetime"
                format="yyyy-MM-dd HH:mm:ss"
                value-format="yyyy-MM-dd HH:mm:ss"
                placeholder="计划文件传输时间"
              >
              </el-date-picker> -->
              <el-time-picker
                v-model="paramsForm.planTransport"
                value-format="HH:mm:ss"
                placeholder="计划文件传输时间">
              </el-time-picker>
            </el-form-item>
          </el-col>
        </el-row>
        <!-- <el-form-item label="计划文件传输时间" prop="planTransport">
          <el-date-picker
            v-model="paramsForm.planTransport"
            type="datetime"
            format="yyyy-MM-dd HH:mm:ss"
            value-format="yyyy-MM-dd HH:mm:ss"
            placeholder="计划文件传输时间"
          >
          </el-date-picker>
        </el-form-item> -->
        <div style="position: relative; display: flex">
          <el-form-item style="width: 100%" label="文件路径" prop="filePath">
            <el-input
              type="textarea"
              :autosize="{ minRows: 2 }"
              maxlength="200"
              show-word-limit
              placeholder="请输入内容"
              v-model="paramsForm.filePath"
            >
            </el-input>
          </el-form-item>
          <el-select v-model="ysxx1" placeholder="插入要素信息">
            <el-option
              v-for="item in elementArr"
              @click.native="selectchange1(item)"
              :key="item.dimCde"
              :label="item.dimNme"
              :value="item.dimCde"
            >
            </el-option>
          </el-select>
        </div>
        <!-- <el-row>
          <el-col :span="9">
            <el-form-item
              label="偏移类型"
              prop="offsetType"
              label-width="150px"
            >
              <el-select v-model="paramsForm.offsetType" placeholder="请选择">
                <el-option
                  v-for="item in OffsetTypeArr"
                  :key="item.dimCde"
                  :label="item.dimNme"
                  :value="item.dimCde"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="偏移量" prop="offset" label-width="90px">
              <el-input-number
                v-model="paramsForm.offset"
                :min="-3"
                :max="3"
                label="偏移量"
              >
              </el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="7">
            <el-form-item label="频率" prop="frequency" label-width="90px">
              <el-select v-model="paramsForm.frequency" placeholder="请选择">
                <el-option
                  v-for="item in frequencyArr"
                  :key="item.dimCde"
                  :label="item.dimNme"
                  :value="item.dimCde"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row> -->
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="csszDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="csszSave">确 定</el-button>
      </span>
    </el-dialog>

    <el-dialog
      title="日期偏移类型及偏移量设置"
      width="50% !important"
      :visible.sync="pianyi_show"
      :close-on-click-modal="false"
      append-to-body
      center
    >
      <div>
        <!-- <span>文件路径：</span>
        <el-input
          type="textarea"
          :autosize="{ minRows: 2 }"
          maxlength="200"
          show-word-limit
          placeholder="请输入内容"
          v-model="paramsForm.filePath"
        >
        </el-input> -->
        <el-form
          :model="pianyiFrom"
          :rules="pianyiFromRules"
          ref="pianyiFrom"
          class="params_form"
          style="margin-top:10px;"
        >
          <el-row>
            <el-col :span="12">
              <el-form-item
                label="偏移类型"
                prop="offsetType"
              >
                <el-select v-model="pianyiFrom.offsetType" placeholder="请选择">
                  <el-option
                    v-for="item in OffsetTypeArr"
                    :key="item.dimCde"
                    :label="item.dimNme"
                    :value="item.dimCde"
                  >
                  </el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="偏移量" prop="offset">
                <el-input-number
                  v-model="pianyiFrom.offset"
                  :min="-10"
                  :max="10"
                  label="偏移量"
                >
                </el-input-number>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="pianyi_show = false">取 消</el-button>
        <el-button type="primary" @click="offsetSave">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import commonFun from '@/filters/new_common'
import homePageApi from "@/api/home/calendarList";
import commonApi from "@/api/common.js";
import pageApi from "@/api/reportCenter/dailyOperations";
export default {
  data() {
    const roleValid = (data) => {
      // console.log('roleValid',data);
      let arr = [
        "系统运转异常，影响业务清算",
        "系统运转平稳，业务清算异常",
        "其他情况见备注说明",
      ];
      if (arr.includes(data.row.target)) {
        if (!data.cellValue) {
          return new Error("请输入备注！");
        }
      }
    };
    return {
      staff:"", //提交人
      formData:{
        hDate:""
      },
      pickerOptions: {
          disabledDate(time) {
            return time.getTime() > Date.now();
          },
          shortcuts: [{
            text: '今天',
            onClick(picker) {
              picker.$emit('pick', new Date());
            }
          }, {
            text: '昨天',
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24);
              picker.$emit('pick', date);
            }
          }, {
            text: '一周前',
            onClick(picker) {
              const date = new Date();
              date.setTime(date.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit('pick', date);
            }
          }]
        },
      formDataRules:{
        hDate:[{required:true,message:"请选择报告日期",trigger:"change"}]
      },
      nowDate: "",
      yyyy: "",
      mm: "",
      dd: "",
      tableData1: [
        // {
        //   vcCheck: "估值系统清算",
        //   target: "系统运转平稳，业务清算正常",
        //   remark: "",
        //   inputType: "s",
        // },
        // {
        //   vcCheck: "信披系统清算",
        //   target: "系统运转平稳，业务清算正常",
        //   remark: "",
        //   inputType: "s",
        // },
        // {
        //   vcCheck: "注册登记系统清算",
        //   target: "系统运转平稳，业务清算正常",
        //   remark: "",
        //   inputType: "s",
        // },
        // {
        //   vcCheck: "资金清算系统清算",
        //   target: "系统运转平稳，业务清算正常",
        //   remark: "",
        //   inputType: "s",
        // },
        // {
        //   vcCheck: "直销清算系统清算",
        //   target: "系统运转平稳，业务清算正常",
        //   remark: "",
        //   inputType: "s",
        // },
        // {
        //   vcCheck: "投资交易系统清算",
        //   target: "系统运转平稳，业务清算正常",
        //   remark: "",
        //   inputType: "s",
        // },
        // { vcCheck: "划款指令处理笔数", target: "", remark: "", inputType: "i" },
        // { vcCheck: "完成待办事项数量", target: "", remark: "", inputType: "i" },
        // { vcCheck: "外包机构等其他事项", target: "", remark: "", inputType: "i" },
      ],
      zhibiaoArr: [
        {
          value: "系统运转平稳，业务清算正常",
          label: "系统运转平稳，业务清算正常",
        },
        {
          value: "系统运转卡顿缓慢，业务清算较慢",
          label: "系统运转卡顿缓慢，业务清算较慢",
        },
        {
          value: "系统运转异常，影响业务清算",
          label: "系统运转异常，影响业务清算",
        },
        {
          value: "系统运转平稳，业务清算异常",
          label: "系统运转平稳，业务清算异常",
        },
        { value: "其他情况见备注说明", label: "其他情况见备注说明" },
      ],
      tableData2: [],
      tableData3: [],
      tableData4: [],
      paramsTable: [],
      tableLoading1: false,
      tableLoading2: false,
      tableLoading3: false,
      tableLoading4: false,
      tableLoading5: false,  //参数设置列表loading
      csszDialogVisible: false,
      csszDialogVisible_table: false,
      tableRules1: {
        remark: [{ validator: roleValid, trigger: "change" }],
        vcCheck: [{ required: true, message: "请填写校验项" }],
        target: [{ required: true, message: "请填写指标" }],
      },
      formType: "",
      paramsForm: {
        vcCheck: "", //检查项
        format: "", //文件传输格式
        transport: "", //传输方式
          fileReceive: "", //文件接收
          planTransport: "", //计划文件传输时间
        filePath: "", //文件路径
        // offsetType: "", //偏移类型
        // offset: "", //偏移量
        frequency: "", //频率
      },
      paramsId:"", //参数设置列表数据id
      ysxx1: "", //要素信息
      formatArr:[], //文件传输格式
      formatObj:{},
      elementArr: [
        { dimNme: "产品代码", dimCde: "${fundCode}" },
        { dimNme: "产品名称", dimCde: "${fundName}" },
        { dimNme: "日期(yyyy-mm-dd)", dimCde: "${yyyy-mm-dd}", type:"date" },
        { dimNme: "日期(yyyy/mm/dd)", dimCde: "${yyyy/mm/dd}", type:"date" },
        { dimNme: "日期(yyyy年mm月dd日)", dimCde: "${yyyy年mm月dd日}", type:"date" },
      ],
      OffsetTypeArr: [
        { dimNme: "自然日", dimCde: "${自然日}" },
        { dimNme: "交易日", dimCde: "${交易日}" },
        { dimNme: "银行间交易日", dimCde: "${银行间交易日}" },
      ],
      frequencyArr: [], //参数设置-频率
      frequencyObj: {}, //用于列表转换
      overflow:true,
      overflow3:true,
      paramsFormRules: {
        vcCheck: { required: true, message: "请填写检查项", trigger: "change" },
        format: {
          required: true,
          message: "请填写文件传输格式",
          trigger: "change",
        },
        transport: {
          required: true,
          message: "请填写传输方式",
          trigger: "change",
        },
        fileReceive: {
          required: true,
          message: "请填写文件接收",
          trigger: "change",
        },
        planTransport: {
          required: true,
          message: "请填写计划文件传输时间",
          trigger: "change",
        },
        filePath: {
          required: true,
          message: "请填写文件路径",
          trigger: "change",
        },
        offsetType: {
          required: true,
          message: "请选择偏移类型",
          trigger: "change",
        },
        offset: { required: true, message: "请填写偏移量", trigger: "change" },
        frequency: { required: true, message: "请选择频率", trigger: "change" },
      },
      isSubmit:"",
      btnLoading:false,
      pianyi_show:false,
      pianyiFrom:{
        offsetType:"",
        offset:""
      },
      pianyiFromRules:{}
    };
  },
  mounted() {
    // 获取服务器时间
    this.getServerData();
    // operationReport_frequency  字典值（参数设置-频率）
    this.getEdims("operationReport_frequency");
    // 获取文件传输格式
    this.getEdims("operationReportFileFormat");
    // this.getDataLiat();
  },
  methods: {
    cellClassName({}) {
      return "vxe-cell-class-name";
    },
    headerCellClassName({}) {
      return "vxe-header-cell-class-name";
    },
    // 获取服务器时间
    getServerData() {
      homePageApi
        .getTime({})
        .then(({ data: res }) => {
          if (res.status == 0) {
            let nowTime = res.timestamp;
            let tody = new Date(res.timestamp);
            this.yyyy = tody.getFullYear().toString();
            this.mm = (tody.getMonth() + 1).toString().padStart("2", "0");
            this.dd = tody.getDate().toString().padStart("2", "0");
            this.nowDate = `${this.yyyy}-${this.mm}-${this.dd}`;
            this.formData.hDate = `${this.yyyy}-${this.mm}-${this.dd}`;
            this.getDataLiat();
          }
        })
        .catch((err) => console.log("is msg err", err));
    },
    getEdims(type) {
      commonApi.getEdims(type).then((res) => {
        if (res.data.status == 0) {
          if (type == "operationReport_frequency") {
            let arr = res.data.data;
            this.frequencyArr = res.data.data;
            for (let i = 0; i < arr.length; i++) {
              this.frequencyObj[arr[i].dimCde] = arr[i].dimNme;
            }
          }
          if (type == "operationReportFileFormat") {
            let arr = res.data.data;
            this.formatArr = res.data.data;
            for (let i = 0; i < arr.length; i++) {
              this.formatObj[arr[i].dimCde] = arr[i].dimNme;
            }
          }
        } else {
          this.$message({
            type: "error",
            message: res.data.message || "获取字典值失败!",
          });
        }
      });
    },
    //数据字典转换
    dataStatus(statusCode, flag) {
      if (flag === "frequency") {
        return this.frequencyObj[statusCode];
      }
      if (flag === "format") {
        return this.formatObj[statusCode];
      }
    },
    // 日期改变时重新请求数据
    hDateChange(data){
      // console.log(data);
      if(data){
        let arr = data.split('-');
        this.yyyy = arr[0];
        this.mm = arr[1];
        this.dd = arr[2];
        this.getDataLiat();
      }
    },
    // 查询
    searchData(){
      this.$refs['formData'].validate((valid) => {
        if (valid) {
          this.getDataLiat();
        } else {
          this.$message({
            type:"warning",
            message:"请选择报告日期！"
          })
          return false;
        }
      });
    },
    // 获取页面数据
    getDataLiat() {
      this.tableLoading1 = true;
      this.tableLoading2 = true;
      this.tableLoading3 = true;
      this.tableLoading4 = true;
      let params = {hDate:this.formData.hDate}
      pageApi.getTableList(params).then((res) => {
        this.tableLoading1 = false;
        this.tableLoading2 = false;
        this.tableLoading3 = false;
        this.tableLoading4 = false;
        if (res.data.status == 200) {
          let data = res.data.data;
          this.isSubmit = data.isSubmit;
          // isSubmit 有值：提交后  无值：提交前
          if(data.isSubmit=='1'){
            this.tableData1 = data.total;
            this.staff = data.principal[0].staff || '';

          }else{
            let total = data.total;
            this.tableData1 = [
              {
                vcCheck: "估值系统清算",
                target: "系统运转平稳，业务清算正常",
                remark: "",
                inputType: "1",
                isOrder:'1'
              },
              {
                vcCheck: "信披系统清算",
                target: "系统运转平稳，业务清算正常",
                remark: "",
                inputType: "1",
                isOrder:'2'
              },
              {
                vcCheck: "注册登记系统清算",
                target: "系统运转平稳，业务清算正常",
                remark: "",
                inputType: "1",
                isOrder:'3'
              },
              {
                vcCheck: "资金清算系统清算",
                target: "系统运转平稳，业务清算正常",
                remark: "",
                inputType: "1",
                isOrder:'4'
              },
              {
                vcCheck: "直销清算系统清算",
                target: "系统运转平稳，业务清算正常",
                remark: "",
                inputType: "1",
                isOrder:'5'
              },
              {
                vcCheck: "投资交易系统清算",
                target: "系统运转平稳，业务清算正常",
                remark: "",
                inputType: "1",
                isOrder:'6'
              },
              { vcCheck: "划款指令处理笔数", target: "", remark: "", inputType: "0", isOrder:'7' },
              { vcCheck: "完成待办事项数量", target: "", remark: "", inputType: "0", isOrder:'8' },
              { vcCheck: "外包机构等其他事项", target: "无", remark: "", inputType: "0", isOrder:'9' },
            ];
            if (total.length) {
              this.$set(this.tableData1[6], "target", total[0].target || "");
              if (total[1]) {
                this.$set(this.tableData1[7], "target", total[1].target || "");
              }
            }
          }
          
          this.tableData2 = data.check;
          this.tableData3 = data.target;
          this.tableData4 = data.principal;
        }else{
          this.$message({type:"error",message:res.data.message || "获取数据失败！"})
        }
      }).catch(()=>{
        this.tableLoading1 = false;
        this.tableLoading2 = false;
        this.tableLoading3 = false;
        this.tableLoading4 = false;
      });
    },
    getTableData1() {},
    getTableData2() {},
    getTableData3() {},
    getTableData4() {},
    targetChange({ value }) {
      let arr = [
        "系统运转异常，影响业务清算",
        "系统运转平稳，业务清算异常",
        "其他情况见备注说明",
      ];
      if (arr.includes(value)) {
        this.$message({
          type: "warning",
          message: "请填写对应行备注！",
        });
      }
    },
    async insertEvent(table) {
      const $table = this.$refs[table];
      const record = {};
      const { row: newRow } = await $table.insertAt(record, -1);
      await $table.setActiveCell(newRow, "");
    },
    // 参数设置
    open() {
      this.csszDialogVisible_table = true;
      this.getParamsTable();
    },
    getParamsTable(){
      this.tableLoading5 = true;
      pageApi.findParam().then(res=>{
        this.tableLoading5 = false;
        if(res.data.status==200){
          this.paramsTable = res.data.data;
        }else{
          this.paramsTable = [];
        }
      })
    },
    canshushezhi(type, row) {
      this.ysxx1 = '';
      this.csszDialogVisible = true;
      this.formType = type;
      if (type == "add") {
        this.resetForm("paramsForm");
      } else if (type == "edit") {
        this.paramsForm.vcCheck = row.vcCheck || "";
        this.paramsForm.format = row.format || "";
        this.paramsForm.transport = row.transport || "";
        this.paramsForm.fileReceive = row.fileReceive || "";
        this.paramsForm.planTransport = row.planTransport || "";
        this.paramsForm.filePath = row.filePath || "";
        this.paramsForm.offsetType = row.offsetType || "";
        this.paramsForm.offset = row.offset || "";
        this.paramsForm.frequency = row.frequency || "";
        this.paramsId = row.id || '';
      }
    },
    csszSave() {
      this.$refs["paramsForm"].validate((valid) => {
        if (valid) {
          this.submitParamsForm();
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },
    submitParamsForm() {
      let params = JSON.parse(JSON.stringify(this.paramsForm));

      // console.log(this.params);
      if (this.formType == "add") {
        pageApi.addParam(params).then(res=>{
          if(res.data.status==200){
            this.$message({type:"success",message:"新增成功！"})
            this.csszDialogVisible = false;
            this.getParamsTable();
          }else{
            this.$message({type:"error",message:res.data.message || "新增失败！"})
          }
        }).catch(()=>{

        })
      }
      if (this.formType == "edit") {
        params.id = this.paramsId;
        pageApi.addParam(params).then(res=>{
          if(res.data.status==200){
            this.$message({type:"success",message:"编辑成功！"})
            this.csszDialogVisible = false;
            this.getParamsTable();
          }else{
            this.$message({type:"error",message:res.data.message || "编辑失败！"})
          }
        }).catch(()=>{

        })
      }
      
    },
    csszDialogVisibleClosed() {
      console.log("closed");
      this.resetForm("paramsForm");
    },
    resetForm(formName) {
      this.$nextTick(() => {
        this.$refs[formName].resetFields();
        this.paramsForm.vcCheck = "";
        this.paramsForm.format = "";
        this.paramsForm.transport = "";
        this.paramsForm.fileReceive = "";
        this.paramsForm.planTransport = "";
        this.paramsForm.filePath = "";
        this.paramsForm.offsetType = "";
        this.paramsForm.offset = "";
        this.paramsForm.frequency = "";
      });
    },
    shanchu(row) {
      this.$confirm("是否删除数据？", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          this.deleteParam(row);
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除",
          });
        });
    },
    deleteParam(row){
      let params = {id:row.id};
      pageApi.deleteParam(params).then(res=>{
        if(res.data.status==200){
          this.$message({
            type:"success",
            message:"删除成功！"
          })
          this.getParamsTable();
        }else{
          this.$message({
            type:"error",
            message:"删除失败！"
          })
        }
      })
    },
    selectchange1(val) {
      this.paramsForm.filePath = this.paramsForm.filePath + val.dimCde;
      if(val.type=='date'){
        this.pianyiFrom.offsetType = '';
        this.pianyiFrom.offset = '';
        this.pianyi_show = true;
      }
    },
    offsetSave(){
      if(this.pianyiFrom.offsetType && this.pianyiFrom.offset){
        this.paramsForm.filePath = this.paramsForm.filePath + this.pianyiFrom.offsetType + `\${${this.pianyiFrom.offset}}`
      }
      this.pianyi_show = false;
    },
    // 总体运营情况 校验
    async xTableValidate() {
      const $table = this.$refs.xTable;
      const errMap = await $table.validate(true).catch((errMap) => errMap);
      // if (errMap) {
      //   this.$XModal.message({ status: "error", message: "校验不通过！" });
      // } else {
      //   this.$XModal.message({ status: "success", message: "校验成功！" });
      // }
      return errMap;
    },
    async submitData() {
      let errMap = await this.xTableValidate();
      if (errMap) {
      } else {
        this.$refs['formData'].validate((valid) => {
          if (valid) {
            this.submit();
          } else {
            this.$message({
              type:"warning",
              message:"请选择报告日期！"
            })
            return false;
          }
        });
      }
    },
    submit() {
      let tableData1 = this.$refs.xTable.getTableData().tableData;
      let tableData2 = this.$refs.xTable2.getTableData().tableData;
      let tableData3 = this.$refs.xTable3.getTableData().tableData;
      let tableData4 = this.$refs.xTable4.getTableData().tableData;
      // console.log(tableData1, tableData2, tableData3, tableData4);
      let params = {}
      params.total = tableData1;
      params.check = tableData2;
      params.target = tableData3;
      params.principal = tableData4;
      params.hDate = this.formData.hDate;
      this.btnLoading = true;
      pageApi.submitReport(params).then(res=>{
        this.btnLoading = false;
        if(res.data.status==200){
          this.$message({
            type:"success",
            message:"提交成功！"
          })
          this.getDataLiat();
        }else{
          this.$message({
            type:"error",
            message:"提交失败！"
          })
        }
      }).catch((err)=>{
        this.$message.closeAll();
        this.$message({
          type:"error",
          message:"运营日报提交请求接口异常！"
        })
        this.btnLoading = false;
      })
    },
    cancel(){
      if(this.formData.hDate){
        this.cancelSubmit();
      }else{
        this.$message({
          type:"warning",
          message:"请选择报告日期！"
        })
        return false
      }
    },
    // 撤销提交
    cancelSubmit(){
      this.$confirm("是否撤销提交？", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          this.btnLoading = true;
          let params = {hDate:this.formData.hDate}
          pageApi.unSubmit(params).then(res=>{
            this.btnLoading = false;
            if(res.data.status==200){
              this.$message({
                type:"success",
                message:"撤销提交成功！"
              })
              this.getDataLiat();
            }else{
              this.$message({
                type:"error",
                message:"撤销提交失败！"
              })
            }
          })
        })
        .catch(() => {
          
        });
    },
    // 邮件发送
    send(){
      if(this.formData.hDate){
        this.sendMail();
      }else{
        this.$message({
          type:"warning",
          message:"请选择报告日期！"
        })
        return false
      }
    },
    // 邮件发送
    sendMail(){
      this.btnLoading = true;
      let params = {
        hDate:this.formData.hDate,
        emailType:"1"
      }
      pageApi.sendMessage(params).then(res=>{
        this.btnLoading = false;
        if(res.data.status===200){
          this.$message({
            type:"success",
            message:"邮件发送成功！"
          })
        }else{
          this.$message({
            type:"error",
            message:res.data.message || "邮件发送失败！"
          })
        }
      })
    },
    // 下载
    downloadFile(){
      if(!this.formData.hDate){
        this.$message.closeAll();
        this.$message({
          type:"warning",
          message:"请选择日期！"
        })
        return false
      }
      let obj = {
        hDate:this.formData.hDate,
        emailType:"1",
        token:this.$store.getters.token
      }
      let action = this.$store.state.setting.baseApi + '/api/reportEmail/v1.0/download';
      commonFun.formDownloadFile(obj,action,'post');
    },
    editActived(val){
      // console.log(val);
      // console.log('editActived');
      this.overflow = false;
    },
    editClosed(){
      // console.log('editClosed');
      this.overflow = true;
    },
    editActived3(val){
      // console.log(val);
      // console.log('editActived');
      this.overflow3 = false;
    },
    editClosed3(){
      // console.log('editClosed');
      this.overflow3 = true;
    },
    contentMethod(val){
      // console.log(val);
    }
  },
};
</script>

<style lang="scss">
.daily_operations {
  // .vxeTable{
  //   .vxe-header--column .vxe-cell--edit-icon {
  //     display: none;
  //   }
  // }
  .title_one {
    font-size: 14px;
    font-weight: 600;
    padding: 10px 0;
  }
}
</style>
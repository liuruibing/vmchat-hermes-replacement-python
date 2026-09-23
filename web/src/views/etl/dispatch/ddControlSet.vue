<template>
  <div class="controlSet ddportal-ui">
    <el-form :inline="true" class="formQuery">
      <el-row>
        <el-col :span="16">
          <!-- 查询 -->
          <div class="grid-content bg-purple">
            <el-form-item label="调度编码" prop="schCde">
              <el-input v-model.trim="formQuery.schCde" clearable placeholder="请输入调度编码" size="small"></el-input>
            </el-form-item>
            <el-form-item label="调度名称" prop="schNme">
              <el-input v-model.trim="formQuery.schNme" clearable placeholder="请输入调度名称" size="small"></el-input>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="8">
          <el-form-item class="search_button_com">
            <el-button type="primary" icon="el-icon-search" :disabled="btnDisabled" class="mb5" size="small" @click="onQuery(true)">
              查询
            </el-button>
            <el-button type="primary" plain size="small" icon="el-icon-circle-plus-outline" @click="addDate">新增</el-button>
            <el-button plain type="primary" icon="el-icon-delete" size="small" @click="deletall">
              批量删除
            </el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <div style="vertical-align: middle;display: inline-block;">
      <div class="color-box"></div>
    </div>
    <span class="title-style">调度列表</span>

    <el-table
      ref="multipleTable"
      @selection-change="handleSelectionChange"
      :data="tableData"
      :cell-style="{ height: '40px', fontSize: '14px' }"
      :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
      stripe
      @sort-change="handleSortChange"
      v-loading="tableLoading"
      style="width: 100%"
    >
      <el-table-column type="selection" width="35" align="center"></el-table-column>

      <el-table-column prop="schCde" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="调度编码" min-width="60" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.schCde | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="schNme" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="调度名称" min-width="60" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.schNme | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="schComment" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="调度说明" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.schComment | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="schSetDte" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="添加时间" min-width="60" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.schSetDte | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column label="操作" min-width="120" align="center">
        <template slot-scope="scope">
         <div class="dialog-footer standard-form">
          <el-button type="info" size="small" plain @click="editData(scope.row)">编辑</el-button>
          <el-button type="info" plain size="small" @click="delData(scope.row)">删除</el-button>
          <el-button type="info" size="small" plain @click="handleData(scope.row)">手工执行</el-button>
          <el-button type="info" size="small" plain @click="controlSet(scope.row)">调度设置</el-button>
         </div>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <Pagination :total="total" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination"></Pagination>

    <!-- 新增/修改 参数弹窗 -->
    <el-dialog title="调度设置" center :visible.sync="dialogMask" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox standard-form">
          <el-form :inline="true" ref="formDialog" :model="formDialog" :rules="dialogRules" label-position="right">
            <el-form-item label="调度编码" prop="schCde" class="mb20" :label-width="formLabelWidth">
              <el-input v-if="operationType == 2" disabled v-model.trim="formDialog.schCde" clearable placeholder="请输入" size="small"></el-input>
              <el-input v-else v-model.trim="formDialog.schCde" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>
            <el-form-item label="调度名称" prop="schNme" class="mb20" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog.schNme" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>
            <el-form-item label="调度说明" prop="schComment" class="mb20" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog.schComment" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>

      <div v-if="operationType == 2">
        <div style="float:right" class="standard-form">
          <el-button type="info" plain size="small" @click="addMis">新增任务</el-button>
        </div>

        <div style="vertical-align: middle;display: inline-block;">
          <div class="color-box"></div>
        </div>
        <span class="title-style">任务列表(从上往下执行)</span>
        <span class="standard-form">
          <el-button type="info"  size="small" plain  style="padding-left:12px" @click="deletjob">删除</el-button>
        </span>
        <el-table
          ref="multipleTable"
          :data="tableData2"
          @selection-change="handleSelectionChange"
          :cell-style="{ height: '40px', fontSize: '14px' }"
          :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
          stripe
          v-loading="tableLoading2"
          style="width: 100%"
        >
          <el-table-column type="selection" width="35"></el-table-column>

          <el-table-column prop="relId" show-overflow-tooltip label="关系编号(ID)" min-width="100" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.relId | noDataFilter }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="grpMisCde" show-overflow-tooltip label="任务编号" min-width="280" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.grpMisCde | noDataFilter }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="whtGrp" show-overflow-tooltip label="类型" min-width="60" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.whtGrp | noDataFilter }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="misGrpNme" show-overflow-tooltip label="任务名称" min-width="100" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.misGrpNme | noDataFilter }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="misGrpMsg" show-overflow-tooltip label="任务说明" min-width="100" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.misGrpMsg | noDataFilter }}</span>
            </template>
          </el-table-column>

          <el-table-column label="操作" min-width="250" align="center">
            <template slot-scope="scope">
              <div class="dialog-footer standard-form">
                <el-button  type="info" size="small" plain :disabled="scope.$index === 0" @click="moveUp(scope.$index, scope.row)">
                上移
              </el-button>
              <el-button type="info" size="small" plain :disabled="scope.$index === tableData2.length - 1" @click="moveDown(scope.$index, scope.row)">
                下移
              </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>

        <Pagination :total="total3" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination3"></Pagination>
      </div>

      <div slot="footer" class="dialog-footer standard-form">
        <el-button type="primary" size="small" @click="dealData">提 交</el-button>
        <el-button size="small" type="info" plain @click="dialogMask = false">取 消</el-button>
      </div>
    </el-dialog>

    <!-- 手工执行 参数弹窗2 -->
    <el-dialog :title="handleWord" center :visible.sync="dialogMask2" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox">
          <el-form :inline="true" ref="formDialog2" :model="formDialog2" :rules="dialogRules2" label-position="right">
            <el-form-item label="日期" prop="date" :label-width="formLabelWidth" class="mb20">
              <el-date-picker
                v-model="formDialog2.date"
                type="daterange"
                unlink-panels
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                value-format="yyyy-MM-dd"
                :picker-options="dateShortcut()"
                size="small"
              ></el-date-picker>
            </el-form-item>
            <el-form-item label="自定义参数（json格式）" prop="custom" class="mb20 ddCode-mirror-form ddCode-mirror-form-200" :label-width="'175px'">
              <!-- js语言需要传入一个特殊的值，来区别是js还是json -->
              <dd-code-mirror ref="customCodeMirror" :language="customLanguage" scriptLanguage="json" @codeChange="customChange"></dd-code-mirror>
            </el-form-item>

            <el-form-item label="产品代码" prop="fundCodes" class="mb20 formInput-adaptive-100" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog2.fundCodes" clearable placeholder="请输入产品代码" type="textarea" @focus="focusCode"></el-input>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer standard-form">
        <el-button type="primary" size="small" @click="handledealData">确 定</el-button>
        <el-button size="small" type="info" plain @click="dialogMask2 = false">取 消</el-button>
      </div>
    </el-dialog>

    <!-- 调度设置 参数弹窗3 -->
    <el-dialog title="调度设置" center :visible.sync="dialogMask3" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox">
          <el-form :inline="true" ref="formDialog3" class="standard-form" :model="formDialog3" :rules="dialogRules3" label-position="right" prop="formDialog3">
            <el-form-item prop="startWhen">
              <div class="titlewords">开始日期:</div>
              <el-radio v-model="formDialog3.startWhen" label="now">立即开始</el-radio>
              <br />
              <el-radio v-model="formDialog3.startWhen" label="dateTime">
                <el-form-item label="开始日期" prop="startDate" label-width="60px" class="mb20 startdate">
                  <el-date-picker
                    v-model="formDialog3.startDate"
                    type="date"
                    size="small"
                    value-format="yyyy-MM-dd"
                    placeholder="选择日期"
                    :picker-options="dateShortDot()"
                  ></el-date-picker>
                </el-form-item>
                <el-form-item label="开始时间" prop="startTime" label-width="100px" class="mb20 startdate">
                  <el-time-picker
                    size="small"
                    v-model="formDialog3.startTime"
                    :picker-options="{ selectableRange: '00:00:00 - 23:59:59' }"
                    placeholder="选择时间"
                    value-format="HH:mm:ss"
                  ></el-time-picker>
                </el-form-item>
              </el-radio>
            </el-form-item>

            <!-- 分割线 -->
            <div style="width:100%;border-top:1px solid #e3bc9a"></div>

            <el-form-item prop="recurPrimary">
              <div class="titlewords">循环:</div>
              <el-radio-group v-model="formDialog3.recurPrimary" @change="recurdeal">
                <el-radio label="once">一次</el-radio>
                <el-radio label="dailyday">每日</el-radio>
                <el-radio label="weekly">每周</el-radio>
                <el-radio label="monthly">每月</el-radio>
                <el-radio label="timepiece">间隔时间</el-radio>
              </el-radio-group>
              <div v-if="recurtype == 1">运行一次 (如果反复运行, 则在同一天运行)</div>
              <div v-else-if="recurtype == 2" class="recur">
                <span>每隔</span>
                &nbsp;
                <el-input v-model.trim="formDialog3.dailyN" clearable size="mini" maxlength="3"></el-input>
                &nbsp;
                <span>天</span>
              </div>
              <div v-else-if="recurtype == 3" class="recur">
                <span>每隔</span>
                &nbsp;
                <el-input v-model.trim="formDialog3.weeklyN" clearable size="mini" maxlength="3"></el-input>
                &nbsp;
                <span>周:</span>
                <br />
                <el-checkbox-group v-model="formDialog3.week">
                  <el-checkbox label="sun">星期日</el-checkbox>
                  <el-checkbox label="mon">星期一</el-checkbox>
                  <el-checkbox label="tue">星期二</el-checkbox>
                  <el-checkbox label="wed">星期三</el-checkbox>
                  <el-checkbox label="thu">星期四</el-checkbox>
                  <el-checkbox label="fri">星期五</el-checkbox>
                  <el-checkbox label="sat">星期六</el-checkbox>
                </el-checkbox-group>
              </div>
              <div v-else-if="recurtype == 4" class="recur">
                <span>在</span>
                &nbsp;
                <el-input v-model.trim="formDialog3.monthlyDay" clearable size="mini" maxlength="3"></el-input>
                &nbsp;
                <span>日:</span>
                <br />
                <span>在</span>
                &nbsp;
                <el-select v-model="formDialog3.monthlyNth" placeholder="请选择" size="small">
                  <el-option label="第一个" value="1"></el-option>
                  <el-option label="第二个" value="2"></el-option>
                  <el-option label="第三个" value="3"></el-option>
                  <el-option label="第四个" value="4"></el-option>
                  <el-option label="最后一个" value="5"></el-option>
                </el-select>
                &nbsp;
                <el-select v-model="formDialog3.monthlyDOW" placeholder="请选择" size="small">
                  <el-option label="星期日" value="1"></el-option>
                  <el-option label="星期一" value="2"></el-option>
                  <el-option label="星期二" value="3"></el-option>
                  <el-option label="星期三" value="4"></el-option>
                  <el-option label="星期四" value="5"></el-option>
                  <el-option label="星期五" value="6"></el-option>
                  <el-option label="星期六" value="7"></el-option>
                </el-select>
                <br />
                <!-- <el-checkbox-group v-model="formDialog3.month"> -->
                <el-checkbox-group v-model="formDialog3.monthStr">
                  <el-checkbox label="jan">一月</el-checkbox>
                  <el-checkbox label="feb">二月</el-checkbox>
                  <el-checkbox label="mar">三月</el-checkbox>
                  <el-checkbox label="apr">四月</el-checkbox>
                  <el-checkbox label="may">五月</el-checkbox>
                  <el-checkbox label="jun">六月</el-checkbox>
                  <el-checkbox label="jul">七月</el-checkbox>
                  <el-checkbox label="aug">八月</el-checkbox>
                  <el-checkbox label="sep">九月</el-checkbox>
                  <el-checkbox label="oct">十月</el-checkbox>
                  <el-checkbox label="nov">十一月</el-checkbox>
                  <el-checkbox label="dec">十二月</el-checkbox>
                </el-checkbox-group>
              </div>
              <div v-else-if="recurtype == 5" class="recur">
                <span>每隔:</span>
                &nbsp;
                <el-radio-group v-model="formDialog3.timePiece">
                  <el-radio label="hour">
                    <el-input v-model.trim="formDialog3.hours" clearable size="mini" maxlength="3"></el-input>
                    &nbsp;
                    <span>小时</span>
                  </el-radio>
                  <el-radio label="minute">
                    <el-input v-model.trim="formDialog3.minutes" clearable size="mini" maxlength="3"></el-input>
                    &nbsp;
                    <span>分钟</span>
                  </el-radio>
                  <el-radio label="second">
                    <el-input v-model.trim="formDialog3.seconds" clearable size="mini" maxlength="3"></el-input>
                    &nbsp;
                    <span>秒</span>
                  </el-radio>
                </el-radio-group>
                <br />
                <span>运行时间段:</span>
                &nbsp;
                <el-time-picker
                  size="small"
                  is-range
                  v-model="runTimeInterval"
                  value-format="HH:mm:ss"
                  range-separator="至"
                  start-placeholder="开始时间"
                  end-placeholder="结束时间"
                  placeholder="选择时间范围"
                ></el-time-picker>
              </div>
            </el-form-item>

            <!-- 分割线 -->
            <div style="width:100%;border-top:1px solid #e3bc9a"></div>

            <el-form-item prop="misIndexSwitch">
              <div class="titlewords">日期偏移设置：</div>
              <div class="recur">
                <el-radio v-model="formDialog3.misIndexSwitch" label="none">无</el-radio>
                <br />
                <el-radio v-model="formDialog3.misIndexSwitch" label="by">
                  <span>日期类型 ：</span>
                  <el-select v-model="formDialog3.natureDay" placeholder="请选择" size="small">
                    <el-option label="自然日" value="0"></el-option>
                    <el-option label="交易日" value="1"></el-option>
                  </el-select>
                  <span>日期偏移量：</span>
                  <el-input v-model.trim="formDialog3.misIndex" clearable size="mini"></el-input>
                </el-radio>
              </div>
            </el-form-item>
            <!-- 分割线 -->
            <div style="width:100%;border-top:1px solid #e3bc9a"></div>
            <el-form-item class="exec-date-type-item-constrlset" prop="execDateType" style="width:100%;">
              <div class="titlewords">执行日期类型：</div>
              <el-row type="flex" justify="start" style="width: 100%">
                <el-col :span="9">
                  <span>日期类型 ：</span>
                  <el-select v-model="formDialog3.execDateType" placeholder="请选择" size="small">
                    <el-option v-for="item in execDateTypeOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
                  </el-select>
                </el-col>
                <el-col :span="15">
                  <el-input v-if="formDialog3.execDateType == 2" type="textarea" :rows="2" placeholder="请输入内容" v-model="formDialog3.execDateSql"></el-input>
                </el-col>
              </el-row>
            </el-form-item>
            <!-- 分割线 -->
            <div style="width:100%;border-top:1px solid #e3bc9a"></div>
            <el-form-item prop="endBy">
              <div class="titlewords">结束日期：</div>
              <div>
                <el-radio v-model="formDialog3.endBy" label="none">无</el-radio>
                <br />
                <el-radio v-model="formDialog3.endBy" label="by">
                  <el-form-item label="结束日期" prop="startDate" label-width="60px" class="mb20">
                    <el-date-picker
                      v-model="formDialog3.endDate"
                      type="date"
                      size="small"
                      value-format="yyyy-MM-dd"
                      placeholder="选择日期"
                      :picker-options="dateShortDot()"
                    ></el-date-picker>
                  </el-form-item>
                </el-radio>
              </div>
            </el-form-item>

            <!-- 分割线 -->
            <div style="width:100%;border-top:1px solid #e3bc9a"></div>
            <el-form-item class="customDefault3-box">
              <div class="titlewords">自定义参数：</div>
              <el-form-item label="产品代码" prop="fundCodes" label-width="100px" class="mb20 formInput-adaptive-100">
                <el-input v-model.trim="formDialog3.fundCodes" clearable placeholder="请输入产品代码" type="textarea" @focus="focusCode"></el-input>
              </el-form-item>
              <el-form-item label="自定义参数（json格式）" prop="custom" class="mb20 ddCode-mirror-form ddCode-mirror-form-200" :label-width="'175px'">
                <!-- js语言需要传入一个特殊的值，来区别是js还是json -->
                <dd-code-mirror ref="customCodeMirror3" :language="customLanguage3" scriptLanguage="json" @codeChange="customChange3"></dd-code-mirror>
              </el-form-item>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer standard-form">
        <el-button type="primary" size="small" @click="dealControlSet" :loading="isDisabledBtn3">
          提 交
        </el-button>
        <el-button size="small" type="info" plain @click="dialogMask3 = false">取 消</el-button>
      </div>
    </el-dialog>

    <!-- 任务组下 添加任务 参数弹窗4 -->
    <el-dialog title="任务添加" center :visible.sync="dialogMask4" :close-on-click-modal="false">
      <el-row>
        <div style="float:right;margin-bottom:10px" class="standard-form">
          <el-button type="info" plain size="small" @click="onQuery2(true)">查询</el-button>
          <!-- <el-button type="primary" plain size="small" @click="addMisJob">新增</el-button> -->
        </div>
      </el-row>
      <el-container class="hg100">
        <el-main class="mainBox">
          <el-form :inline="true" ref="formDialog4" :model="formDialog4" label-position="right">
            <el-form-item label="任务类型" prop="whtGrp" class="mb20">
              <el-select v-model="formDialog4.whtGrp" placeholder="请选择" size="small">
                <el-option label value></el-option>
                <el-option label="任务" value="0"></el-option>
                <el-option label="任务组" value="1"></el-option>
              </el-select>
            </el-form-item>

            <el-form-item label="任务名称" prop="grpMisNme" class="mb20">
              <el-input v-model.trim="formDialog4.grpMisNme" clearable placeholder="请输入任务名称" size="small"></el-input>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>

      <div style="vertical-align: middle;display: inline-block;">
        <div class="color-box"></div>
      </div>
      <span class="title-style">任务列表</span>

      <el-table
        ref="multipleTable"
        :data="tableData3"
        @selection-change="handleSelectionChange"
        :cell-style="{ height: '40px', fontSize: '14px' }"
        :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
        stripe
        v-loading="tableLoading3"
        style="width: 100%"
      >
        <el-table-column type="selection" width="35"></el-table-column>

        <el-table-column prop="grpMisCde" show-overflow-tooltip label="任务编码" min-width="100" header-align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.grpMisCde | noDataFilter }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="grpMisNme" show-overflow-tooltip label="任务名称" min-width="100" header-align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.grpMisNme | noDataFilter }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="whtGrp" show-overflow-tooltip label="任务类型" min-width="100" header-align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.whtGrp | noDataFilter }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="grpMisMsg" show-overflow-tooltip label="任务说明" min-width="100" header-align="center">
          <template slot-scope="scope">
            <span>{{ scope.row.grpMisMsg | noDataFilter }}</span>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页2 -->
      <Pagination :total="total2" :limit="formDialog4.pageSize" :page="formDialog4.pageNum" @pagination="pagination2"></Pagination>

      <div slot="footer" class="dialog-footer standard-form">
        <el-button type="primary" size="small" @click="addMisJob">提 交</el-button>
        <el-button size="small" type="info" plain @click="dialogMask4 = false">取 消</el-button>
      </div>
    </el-dialog>

    <!--手工执行 查询代码 弹窗5  -->
    <el-dialog title="选择产品" center :visible.sync="dialogMask5" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox standard-form">
          <el-form :inline="true" ref="formDialog5" :model="formDialog5" label-position="right">
            <el-form-item label="组合代码" prop="fundCode" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog5.fundCode" clearable placeholder="请输入产品代码" size="small"></el-input>
            </el-form-item>
            <el-form-item label="组合名称" prop="fundName" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog5.fundName" clearable placeholder="请输入组合名称" size="small"></el-input>
            </el-form-item>
          </el-form>
          <el-row>
            <div style="float:right;margin-bottom:10px">
              <el-button type="primary" plain size="small" @click="handleSelect">选 择</el-button>
              <el-button type="primary" plain size="small" @click="onQuery5(true)">查询</el-button>
            </div>
          </el-row>

          <div style="vertical-align: middle;display: inline-block;">
            <div class="color-box"></div>
          </div>
          <span class="title-style">产品信息</span>
          <el-table
            ref="multipleTable"
            :data="tableData5"
            @selection-change="handleSelectionChange"
            :cell-style="{ height: '40px', fontSize: '14px' }"
            :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
            stripe
            @sort-change="handleSortChange5"
            v-loading="tableLoading5"
            style="width: 100%"
            row-key="id"
          >
            <el-table-column type="selection" width="35"></el-table-column>

            <el-table-column
              prop="fundCode"
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              show-overflow-tooltip
              label="产品代码"
              min-width="100"
              header-align="center"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.fundCode | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="fundName"
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              show-overflow-tooltip
              label="产品名称"
              min-width="100"
              header-align="center"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.fundName | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column
              prop="nameTgr"
              sortable="custom"
              :sort-orders="['ascending', 'descending']"
              show-overflow-tooltip
              label="托管人名称"
              min-width="100"
              header-align="center"
            >
              <template slot-scope="scope">
                <span>{{ scope.row.nameTgr | noDataFilter }}</span>
              </template>
            </el-table-column>
          </el-table>

          <Pagination :total="total5" :limit="formDialog5.pageSize" :page="formDialog5.pageNum" @pagination="pagination5"></Pagination>
        </el-main>
      </el-container>
    </el-dialog>
  </div>
</template>

<script>
import commonApi from '@/api/etl/controlSet'
import Pagination from '@/components/Pagination'
import fun from '@/filters/common'
import DdCodeMirror from '@/components/codemirror'
import commonValidate from '@/utils/validate'

export default {
  name: 'DdControlSet',
  components: {
    Pagination,
    DdCodeMirror
  },

  data() {
    return {
      execDateTypeOptions: [
        {
          label: '自然日',
          value: '0'
        },
        {
          label: '交易日',
          value: '1'
        },
        {
          label: '自定义',
          value: '2'
        }
      ],
      tableData: [], //表格数据
      tableLoading: false, //表格加载
      tableData2: [], //表格2数据
      tableLoading2: false, //表格2加载
      tableData3: [], //表格3数据
      tableLoading3: false, //表格3加载
      tableData5: [], //表格5数据
      tableLoading5: false, //表格5加载
      dialogMask: false, // 弹窗
      dialogMask2: false, // 弹窗 2
      dialogMask3: false, // 弹窗 3
      dialogMask4: false, // 弹窗 4
      dialogMask5: false, // 弹窗 5
      isDisabledBtn3: false, //禁用按钮3
      // 任务类型集合
      jobTypeArr: [],
      // //总条数
      total: 0,
      total2: 0,
      total5: 0,
      total3: 0,

      // 顶部查询条件
      formQuery: {
        // 编码
        schCde: '',
        // 名称
        schNme: '',
        // 排序字段
        orderBy: '',
        // 起始页
        pageNum: 1,
        // 每页大小
        pageSize: 10
      },
      // 查询2
      formQuery2: {
        schCde: '',
        orderBy: '',
        pageNum: 1,
        pageSize: 10
      },
      // 弹窗查询参数
      formDialog: {
        //  编码
        schCde: '',
        // 名称
        schNme: '',
        // 描述
        schComment: '',
        // 关系id  排序用的
        relIds: ''
      },
      // 弹窗验证规则
      dialogRules: {
        // 编码
        schCde: [{ required: true, message: '请填写调度编码', trigger: 'change' }],
        // 名称
        schNme: [{ required: true, message: '请填写调度名称', trigger: 'change' }],
        // 调度说明信息
        schComment: [{ required: true, message: '请填写调度说明信息', trigger: 'change' }]
      },
      // 弹窗2查询参数
      formDialog2: {
        // 日期
        date: [],
        // 基金编码
        fundCodes: '',
        // 调度设置编码
        schCde: '',
        // 自定义参数
        custom: ''
      },
      customLanguage: 'javascript', //自定义参数编辑器语言类型
      // 弹窗2验证规则
      dialogRules2: {
        // 日期
        date: [{ required: true, message: '请填写日期', trigger: 'change' }]
      },
      // 弹窗3查询参数
      formDialog3: {
        // 编码
        schCde: '',
        // 名称
        schNme: '',
        // 开始类型
        startWhen: 'now',
        // 开始日期
        startDate: '',
        // 开始时间
        startTime: '',
        // 循环
        recur: 'once',
        // 每隔几天运行一次
        recurPrimary: 'once',
        // 间隔天数
        dailyN: '',
        // 每隔几周
        weeklyN: '',
        // week 多选框
        week: [],
        // 第几周标志
        recurMonthly: 'monthlynth',
        // 每月第几天
        monthlyDay: '',
        // 第几周
        monthlyNth: '1',
        // 星期几
        monthlyDOW: '1',
        // 几月份 多选框
        // month: [],
        monthStr: [],
        timePiece: '',
        // 小时
        hours: '01',
        // 分钟
        minutes: '01',
        // 秒数
        seconds: '01',
        // 运行时间段
        runTimeInterval: '',
        // 开始时间
        runStartTime: '',
        // 结束时间
        runEndTime: '',
        // 日期偏移选择
        misIndexSwitch: 'none', //none 是无 ，by是有
        // 日期偏移量类型
        natureDay: '0', //0是自然日，1是交易日
        // 日期偏移量
        misIndex: '',
        // 结束日期 无
        endBy: 'none',
        // 结束日期
        endDate: '',
        // 产品代码
        fundCodes: '',
        // 自定义参数
        custom: '',
        execDateType: '0',
        execDateSql: ''
      },
      customLanguage3: 'javascript', //自定义参数编辑器语言类型
      runTimeInterval: '',
      // 弹窗验证规则
      dialogRules3: {
        // 代码
        schCde: [{ required: true, message: '请填写日期', trigger: 'change' }]
      },
      // 弹窗4查询参数
      formDialog4: {
        // 任务类型
        whtGrp: '',
        // 任务名称
        grpMisNme: '',
        // 排序
        orderBy: '',
        pageNum: 1,
        pageSize: 10,
        grpCde: '',
        grpCdeLike: ''
      },
      // 弹窗5 查询参数
      formDialog5: {
        // 组合代码
        fundCode: '',
        // 组合名称
        fundName: '',
        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10,
        // 排序条件
        orderBy: ''
      },
      // 手工执行 传给接口的产品代码
      handlefundCodes: '',
      // 手工执行显示文字
      handleWord: '手工执行',
      // 调度设置 传给接口的产品代码
      setfundCodes: '',
      recurtype: 1,
      // 操作类型 1、添加 2、编辑
      operationType: 1,
      formLabelWidth: '100px',
      // 批量删除的数据
      multipleSelection: [],
      // 查询按钮禁用
      btnDisabled: false,
      // 数据源数据集合
      SourceList: [],
      // 手工执行任务编码
      handlemisCde: '',
      // 调度设置 编码
      controlschCde: '',
      // 调度设置 名称
      controlschNme: ''
    }
  },
  watch: {
    'formDialog3.recurPrimary'(val) {
      if (val === 'once') {
        this.recurtype = 1
      } else if (val === 'dailyday') {
        this.recurtype = 2
      } else if (val === 'weekly') {
        this.recurtype = 3
      } else if (val === 'monthly') {
        this.recurtype = 4
      } else if (val === 'timepiece') {
        this.recurtype = 5
      }
    }
  },
  mounted() {
    // 默认查询
    this.onQuery(true)
  },
  methods: {
    // 日期快捷选项
    dateShortcut() {
      return fun.dateShortcut()
    },
    dateShortDot() {
      return fun.dateShortDot()
    },
    // 查询
    onQuery(flag) {
      this.tableLoading = true
      if (flag) {
        this.formQuery.pageNum = 1
      }
      let params = Object.assign({}, this.formQuery)
      commonApi
        .getScherList(params)
        .then(res => {
          this.tableLoading = false

          let { list, total } = res.data.data
          // 总条数
          this.total = total
          this.tableData = []
          list.forEach(item => {
            this.tableData.push(item)
          })
        })
        .catch(() => {})
    },
    // 手工执行下 查询代码
    onQuery5(flag) {
      let params = Object.assign({}, this.formDialog5)
      if (flag) {
        this.formDialog5.pageNum = 1
      }
      commonApi
        .getFundList(params)
        .then(res => {
          this.tableLoading5 = false

          let { list, total } = res.data.data
          // 总条数
          this.total5 = total
          this.tableData5 = list
        })
        .catch(() => {})
    },
    // 添加代码需要唯一性
    onlyCode() {
      let params = { schCde: this.formDialog.schCde }
      commonApi
        .getScherByCode(params)
        .then(res => {
          if (res.data.status == 200) {
            this.$message.closeAll()

            this.$message.error('编码已经存在，请勿重复添加！')
          } else {
            this.addParamSet()
          }
        })
        .catch(() => {})
    },
    // 新增按钮
    addDate() {
      this.dialogMask = true
      this.operationType = 1
      this.$nextTick(() => {
        this.$refs['formDialog'].resetFields()
      })
    },
    // 处理数据
    dealData() {
      this.$refs['formDialog'].validate(valid => {
        if (valid) {
          if (this.operationType === 1) {
            // 添加
            this.onlyCode()
          } else {
            // 修改
            this.updateParamSet()
          }
        }
      })
    },
    // 添加参数
    addParamSet() {
      let params = Object.assign({}, this.formDialog)
      commonApi
        .doScherAdd(params)
        .then(res => {
          if (res.data.status === 200) {
            this.onQuery(true)
            this.$message.closeAll()

            this.$message({
              type: 'success',
              message: res.data.message
            })
            this.dialogMask = false
          }
        })
        .catch(() => {})
    },
    // 修改参数
    updateParamSet() {
      let str = []
      this.tableData2.forEach(item => {
        str.push(item.relId)
      })

      // 数组倒叙
      // str.reverse();
      this.formDialog.relIds = str.join(',')

      let params = Object.assign({}, this.formDialog)
      commonApi
        .doScherEdit(params)
        .then(res => {
          this.onQuery(false)
          this.$message.closeAll()

          this.$message({
            type: 'success',
            message: '修改成功'
          })
          this.dialogMask = false
        })

        .catch(() => {})
    },
    // 单个删除
    deleteParamSet(schCde) {
      let params = { schCde: schCde }

      commonApi
        .doScherDelete(params)
        .then(res => {
          if (res.data.status === 200) {
            this.onQuery(false)
            this.$message.closeAll()

            this.$message({
              type: 'success',
              message: res.data.message
            })
          } else {
            this.$message.closeAll()

            this.$message.error(res.data.message)
          }
        })
        .catch(() => {})
    },
    // 批量删除
    deletall() {
      if (this.multipleSelection.length) {
        this.$confirm('确认删除这些数据吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
        })
          .then(() => {
            // 批量删除
            let arr = []
            let str = {}

            this.multipleSelection.forEach(item => {
              arr.push(item.schCde)
            })
            str.schCdes = arr.join(',')

            commonApi
              .batchScherDelete(str)
              .then(res => {
                if (res.data.status === 200) {
                  this.onQuery(false)
                  this.$message.closeAll()

                  this.$message({
                    type: 'success',
                    message: res.data.message
                  })
                } else {
                  this.$message.closeAll()

                  this.$message.error(res.data.message)
                }
              })
              .catch(() => {})
          })
          .catch(() => {})
      } else if (this.multipleSelection.length === 0) {
        this.$message.closeAll()
        this.$message({
          message: '请选择要批量删除的数据',
          type: 'warning'
        })
      }
    },
    // 批量删除数据
    handleSelectionChange(val) {
      this.multipleSelection = val
    },
    //列表点击排序
    handleSortChange(val) {
      this.formQuery.orderBy = fun.etlqueryOrderBy(val)
      // 查询
      this.onQuery(true)
    },
    // 手工执行下查询代码 排序
    handleSortChange5(val) {
      this.formDialog5.orderBy = fun.queryOrderBy(val)
      // 查询
      this.onQuery5(false)
    },
    // 行编辑
    editData(row) {
      this.dialogMask = true
      this.operationType = 2
      this.$nextTick(() => {
        // 清除
        this.$refs['formDialog'].resetFields()

        let { schCde, schNme, schComment } = row

        this.formDialog.schCde = schCde
        this.formDialog.schNme = schNme
        this.formDialog.schComment = schComment

        // 获取任务组下任务列表
        this.formQuery2.schCde = schCde

        this.getdoScherTaskRel(true)
      })
    },
    // 行删除
    delData(row) {
      this.$confirm('确认删除该条数据?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          // 删除单个
          this.deleteParamSet(row.schCde)
        })
        .catch(() => {})
    },
    // 手工执行的处理数据
    handleData(row) {
      this.handleWord = row.schNme + '(' + row.schCde + ')'
      this.handlemisCde = row.schCde
      this.dialogMask2 = true
      this.$nextTick(() => {
        this.$refs['formDialog2'].resetFields()

        // 清除
        this.formDialog2.fundCodes = ''
        this.handlefundCodes = ''
        this.setfundCodes = ''
        // 清空自定义参数的值
        this.$refs.customCodeMirror.operationVal(null)
      })
    },
    // 自定义参数赋值给页面变量
    customChange(val) {
      this.formDialog2.custom = val
    },
    // 手工执行
    handledealData() {
      this.$refs['formDialog2'].validate(valid => {
        if (valid) {
          // 判自定义参数是否是json格式的
          if (this.formDialog2.custom) {
            if (commonValidate.isJSON(this.formDialog2.custom) === false) {
              this.$message.closeAll()
              this.$message({
                type: 'warning',
                message: '自定义参数必须是json格式！'
              })
              return false
            }
          } else {
          }
          let params = Object.assign({}, this.formDialog2)
          params.beginDate = params.date[0]
          params.endDate = params.date[1]
          delete params.date
          params.schCde = this.handlemisCde
          // 手工执行的名字变成代传参
          params.fundCodes = this.handlefundCodes

          // 手工执行
          commonApi
            .implementScher(params)
            .then(res => {
              this.$message.closeAll()
              if (res.data.status == 200) {
                this.$message({
                  type: 'success',
                  message: res.data.message
                })
                this.dialogMask2 = false
              } else {
                this.$message({
                  type: 'error',
                  message: res.data.message
                })
              }
            })
            .catch(() => {})
        }
      })
    },
    // 手工执行下 查询代码
    focusCode() {
      this.dialogMask5 = true
      this.tableLoading5 = true
      this.onQuery5(true)
    },
    // 手工执行下 添加代码
    handleSelect() {
      let code = []
      let codename = []

      this.multipleSelection.forEach(item => {
        code.push(item.fundCode)
        codename.push(item.fundName)
      })

      this.formDialog2.fundCodes = codename.join(',')
      this.formDialog3.fundCodes = codename.join(',')

      this.handlefundCodes = code.join(',')
      this.setfundCodes = code.join(',')

      // 关闭弹窗 并提示
      this.dialogMask5 = false
      this.$message.closeAll()
      this.$message({
        type: 'success',
        message: '添加成功！'
      })
    },
    // 上移
    moveUp(index, row) {
      if (index > 0) {
        let upDate = this.tableData2[index - 1]
        this.tableData2.splice(index - 1, 1)
        this.tableData2.splice(index, 0, upDate)
      }
    },
    // 下移
    moveDown(index, row) {
      if (index + 1 !== this.tableData2.length) {
        let downDate = this.tableData2[index + 1]
        this.tableData2.splice(index + 1, 1)
        this.tableData2.splice(index, 0, downDate)
      }
    },
    // 调度设置的处理数据
    controlSet(row) {
      this.dialogMask3 = true
      this.setfundCodes = ''

      this.$nextTick(() => {
        // 清除
        this.$refs['formDialog3'].resetFields()
        this.formDialog3.dailyN = '1'
        this.formDialog3.weeklyN = ''
        this.formDialog3.week = []
        this.formDialog3.monthlyDay = ''
        this.formDialog3.monthlyNth = '1'
        this.formDialog3.monthlyDOW = '1'
        this.formDialog3.monthStr = []
        this.formDialog3.timePiece = ''
        this.formDialog3.hours = '01'
        this.formDialog3.minutes = '01'
        this.formDialog3.seconds = '01'
        this.runTimeInterval = ''
        this.formDialog3.natureDay = '0'
        this.formDialog3.misIndex = ''
        this.formDialog3.endDate = ''
        this.formDialog3.execDateType = '0'
        this.formDialog3.execDateSql = ''

        let { schCde, schNme } = row

        this.formDialog3.schCde = schCde
        this.formDialog3.schNme = schNme
        this.formDialog3.fundCodes = ''
        // 清空自定义参数的值
        this.$refs.customCodeMirror3.operationVal(null)
      })
    },
    // 自定义参数赋值给页面变量
    customChange3(val) {
      this.formDialog3.custom = val
    },
    // 调度设置
    dealControlSet() {
      if (this.runTimeInterval) {
        this.formDialog3.runTimeInterval = 'runTime'
        this.formDialog3.runStartTime = this.runTimeInterval[0]
        this.formDialog3.runEndTime = this.runTimeInterval[1]
      }

      let params = Object.assign({}, this.formDialog3)
      params.week = params.week.join(',')
      params.month = params.monthStr.join(',')

      // 调度设置的代码
      params.fundCodes = this.setfundCodes

      // 判自定义参数是否是json格式的
      if (this.formDialog3.custom) {
        if (commonValidate.isJSON(this.formDialog3.custom) === false) {
          this.$message.closeAll()
          this.$message({
            type: 'warning',
            message: '自定义参数必须是json格式！'
          })
          return false
        }
      } else {
      }

      // 判断间隔时间是否正确
      if (this.formDialog3.hours < 1 || this.formDialog3.hours > 23) {
        this.$message.closeAll()
        this.$message({
          type: 'warning',
          message: '小时数为 : 01-23'
        })
        return false
      } else if (this.formDialog3.minutes < 1 || this.formDialog3.minutes > 59) {
        this.$message.closeAll()
        this.$message({
          type: 'warning',
          message: '分钟数为 : 01-59'
        })
        return false
      } else if (this.formDialog3.seconds < 1 || this.formDialog3.seconds > 59) {
        this.$message.closeAll()
        this.$message({
          type: 'warning',
          message: '秒数为 : 01-59'
        })
        return false
      } else if (this.recurtype == 5 && !this.formDialog3.timePiece) {
        this.$message.closeAll()
        this.$message({
          type: 'warning',
          message: '请选择间隔时间'
        })
        return false
      }
      // 按钮禁用
      this.isDisabledBtn3 = true

      commonApi
        .doScherSet(params)
        .then(res => {
          this.isDisabledBtn3 = false

          if (res.data.status === 200) {
            this.onQuery(false)
            this.$message.closeAll()

            this.$message({
              type: 'success',
              message: res.data.message
            })
            this.dialogMask3 = false
            this.setfundCodes = ''
          } else {
            this.$message.closeAll()
            this.$message.error(res.data.message)
          }
        })
        .catch(() => {
          this.isDisabledBtn3 = false
        })
    },
    // 调度设置-循环 的处理
    recurdeal(val) {
      if (val === 'once') {
        this.recurtype = 1
      } else if (val === 'dailyday') {
        this.recurtype = 2
      } else if (val === 'weekly') {
        this.recurtype = 3
      } else if (val === 'monthly') {
        this.recurtype = 4
      } else if (val === 'timepiece') {
        this.recurtype = 5
      }
    },
    //  获取任务组下任务列表
    getdoScherTaskRel(flag) {
      this.tableLoading2 = true
      if (flag) {
        this.formQuery2.pageNum = 1
      }
      let params = Object.assign({}, this.formQuery2)

      commonApi
        .doScherTaskRel(params)
        .then(res => {
          this.tableLoading2 = false
          let { list, total } = res.data.data
          this.total3 = total
          // 总条数
          this.tableData2 = []

          list.forEach(item => {
            if (item.whtGrp == 1) {
              item.whtGrp = '任务组'
            } else {
              item.whtGrp = '任务'
            }
            this.tableData2.push(item)
          })
        })
        .catch(() => {})
    },
    // 任务组下添加任务
    addMis() {
      this.dialogMask4 = true
      this.onQuery2(true)
    },
    // 任务组下批量删除
    deletjob() {
      if (this.multipleSelection.length) {
        this.$confirm('确认删除这些数据吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
        })
          .then(() => {
            // 批量删除
            let arr = []
            let str = {}

            this.multipleSelection.forEach(item => {
              arr.push(item.relId)
            })
            str.relIds = arr.join(',')

            commonApi
              .doTaskRelDelete(str)
              .then(res => {
                if (res.data.status === 200) {
                  // 刷新列表
                  this.getdoScherTaskRel(false)
                  this.$message.closeAll()

                  this.$message({
                    type: 'success',
                    message: res.data.message
                  })
                } else {
                  this.$message.closeAll()

                  this.$message.error(res.data.message)
                }
              })
              .catch(() => {})
          })
          .catch(() => {})
      }
    },
    // 查询任务组和任务
    onQuery2(flag) {
      this.tableLoading3 = true
      if (flag) {
        this.formDialog4.pageNum = 1
      }

      let params = Object.assign({}, this.formDialog4)
      commonApi
        .doMisGrpList(params)
        .then(res => {
          this.tableLoading3 = false
          let { list, total } = res.data.data
          // 总条数
          this.total2 = total
          this.tableData3 = []
          list.forEach(item => {
            if (item.whtGrp == 1) {
              item.whtGrp = '任务组'
            } else {
              item.whtGrp = '任务'
            }
            this.tableData3.push(item)
          })
        })
        .catch(() => {})
    },
    // 最内层 添加任务
    addMisJob() {
      if (!this.multipleSelection.length) {
        this.$message.closeAll()

        this.$message({
          type: 'warning',
          message: '请选择一条或者多条数据'
        })
      } else {
        let grpMisCde = []
        let whtGrp = []
        let selectType = ''

        this.multipleSelection.forEach(item => {
          if (item.whtGrp == '任务组') {
            selectType = '1'
          } else {
            selectType = '0'
          }
          grpMisCde.push(item.grpMisCde)
          whtGrp.push(selectType)
        })

        let params = {
          grpMisCdes: grpMisCde.join(','), //任务组或任务代码
          schCde: this.formQuery2.schCde, //调度设置编码
          whtGrps: whtGrp.join(',') //任务类型
        }

        commonApi
          .doTaskRelAdd(params)
          .then(res => {
            if (res.data.status === 200) {
              // 刷新列表
              this.getdoScherTaskRel(true)

              this.dialogMask4 = false
              this.$message.closeAll()

              this.$message({
                type: 'success',
                message: res.data.message
              })
            } else {
              this.$message.closeAll()

              this.$message({
                type: 'error',
                message: '添加失败'
              })
            }
          })
          .catch(() => {})
      }
    },
    //  分页
    pagination(val) {
      let { page, limit } = val
      // 起始页
      this.formQuery.pageNum = page
      // 每页数量
      this.formQuery.pageSize = limit
      // 查询
      this.onQuery(false)
    },
    //  分页2
    pagination2(val) {
      let { page, limit } = val
      // 起始页
      this.formDialog4.pageNum = page
      // 每页数量
      this.formDialog4.pageSize = limit
      // 查询
      this.onQuery2(false)
    },
    // 分页3
    pagination3(val) {
      let { page, limit } = val
      // 起始页
      this.formQuery2.pageNum = page
      // 每页数量
      this.formQuery2.pageSize = limit
      // 查询
      this.getdoScherTaskRel(false)
    },
    //  分页4
    pagination5(val) {
      let { page, limit } = val
      // 起始页
      this.formDialog5.pageNum = page
      // 每页数量
      this.formDialog5.pageSize = limit
      // 查询
      this.onQuery5(false)
    }
  }
}
</script>

<style lang="scss" scoped>
.controlSet {
  padding-left: 10px;
  .title-style {
    color: #0F65DD;
    vertical-align: middle;
    height: 35px;
    line-height: 35px;
    font-size: 16px;
    margin-left: 5px;
  }
  .color-box {
    display: inline-block;
    height: 30px;
    width: 2px;
    background-color: #0F65DD;
  }
  .el-dialog {
    width: 54% !important;

    .el-form {
      width: 100% !important;
      font-size: 0;
    }

    // .el-input {
    // width: 120% !important;
    // }
    .el-form-item {
      min-width: 50%;
      margin-right: 0;
      margin-bottom: 10px;
    }

    .mr5 {
      margin-right: 5px;
    }
  }

  .mb20 {
    margin-bottom: 15px !important;
  }

  .recur {
    .el-input {
      width: 85px !important;
    }
  }

  // 火狐移除
  input[type='number'] {
    -moz-appearance: textfield;
  }

  //谷歌下的移除
  input[type='number']::-webkit-inner-spin-button,
  input[type='number']::-webkit-outer-spin-button {
    -webkit-appearance: none;
  }
}
::v-deep .el-table tbody tr:hover > td {
  background: transparent !important; //修改成自己想要的颜色即可
}

::v-deep .el-table--striped .el-table__body tr.el-table__row--striped td {
  background: #f7f7f7 !important;
}

::v-deep .el-dialog__wrapper .el-dialog__header span {
  color: #333 !important;
}
::v-deep .el-button--info {
  background-color: #f4f4f5;
}
::v-deep .el-button--danger.is-plain {
  background:#f4f4f5;
}
::v-deep .el-button--move {
  background-color: #f4f4f5;
}
</style>
<style rel="stylesheet/scss" lang="scss">
.exec-date-type-item-constrlset {
  .el-form-item__content {
    width: 100%;
  }
}
.controlSet {
  .customDefault3-box {
    width: 100%;
  }

  .customDefault3-box > .el-form-item__content {
    width: 100%;
  }
}
</style>

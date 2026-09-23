<template>
  <div >
     <el-form :inline="true" ref = "formInline" :model="formInline"  class="demo-form-inline form_inline_search" style="margin-top: 8px;margin-bottom: 10px;">
          <el-row>
            <el-col :span="16">
              <div class="grid-content bg-purple">

               <el-form-item label="产品&基金代码" prop="accountCode">
                            <el-input
                              v-model="formInline.accountCode"
                              placeholder="产品&基金代码"
                              name="accountCode"
                              type="text"
                              auto-complete="off"
                            />
                          </el-form-item>

               <el-form-item label="要求划款日期" prop="date">
                                        <el-date-picker
                                          v-model="formInline.date"
                                          type="date"
                                          placeholder="选择日期">
                                        </el-date-picker>
                         </el-form-item>

                <el-form-item label="经纪商选择" prop="agent">
                                        <el-select v-model="formInline.agent" placeholder="请选择">
                                          <el-option
                                            v-for="item in selects"
                                            :key="item.value"
                                            :label="item.label"
                                            :value="item.value">
                                          </el-option>
                                        </el-select>
                          </el-form-item>
                          <el-form-item label="转账金额" prop="money">
                                                 <el-input
                                                   v-model="formInline.money"
                                                   name="money"
                                                   type="text"
                                                   auto-complete="off"
                                                 />
                                       </el-form-item>

                                        <el-form-item label="备注" prop="remark">
                                                              <el-input
                                                                v-model="formInline.remark"
                                                                name="remark"
                                                                type="text"
                                                                auto-complete="off"
                                           />
                                        </el-form-item>
              </div>

            </el-col>
            <el-col :span="8">
              <div class="grid-content bg-purple-light">
                <el-form-item  class="search_button_com">
                  <el-button type="primary" @click="onSubmit('formInline')" style="margin-bottom: 5px;" :disabled = "investmentSearch1"  size="small"><i class="el-icon-search"></i>查询</el-button>
                  <el-button type="primary" style="margin-bottom: 5px;" plain size="small" @click="resetForm('formInline')"><i class='el-icon-delete'></i>重置</el-button>
                </el-form-item>
              </div>
            </el-col>
          </el-row>
        </el-form>

<div class="forms_table_title" ><i class="el-icon-tickets"></i> 提交记录
    </div>
    <el-table
      :data="myData.datas"
      border
      stripe
      height="360"
      style="width: 100%"
      v-loading="investLoading && $store.state.setting.loadingShow"
      @sort-change="investmentComDataChangeSort"
      :default-sort = "{prop: 'dMettingdate', order: 'descending'}"
    >
      <el-table-column
        type="index"
        label="序号"
        fixed
        align = "center"
        width="40">
      </el-table-column>
      <el-table-column
        prop="accountCode"
        label="产品&基金代码"
        sortable = "custom"
        :sort-orders="['ascending', 'descending']"
        min-width="90"
        header-align = "center"
        align = "left"
      >
        <template slot-scope="scope">
          <span>{{scope.row.accountCode | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="date"
        label="要求划款日期"
        min-width = "110"
        :show-overflow-tooltip="true"
        sortable = "custom"
        :sort-orders="['ascending', 'descending']"
        header-align = "center"
      >
        <template slot-scope="scope">
          <span>{{scope.row.date | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="agent"
        label="经纪商选择"
        min-width = "90"
        :show-overflow-tooltip="true"
        sortable = "custom"
        :sort-orders="['ascending', 'descending']"
        header-align = "center"
      >
        <template slot-scope="scope">
          <span>{{scope.row.agent | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="money"
        label="转账金额"
        min-width = "100"
        sortable = "custom"
        :sort-orders="['ascending', 'descending']"
        header-align = "center"
        :show-overflow-tooltip="true"
      >
        <template slot-scope="scope">
          <span>{{scope.row.money | noDataFilter}}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="remark"
        label="备注"
        min-width = "90"
        sortable = "custom"
        :sort-orders="['ascending', 'descending']"
        :show-overflow-tooltip="true"
        header-align = "center"
        align = "left"
      >
        <template slot-scope="scope">
          <span>{{scope.row.remark | noDataFilter}}</span>
        </template>
      </el-table-column>
    </el-table>

  </div>
</template>

<script>
  import Pagination from '@/components/Pagination'
  import commonApi from '@/api/common'
  import fun from '@/filters/common'
  import hint from '@/components/hint'
  export default {
    name: 'loginBack',
    data() {

      return {
        formInline:{
        accountCode:'',//产品&基金代码
        date:'',//要求划款日期
        agent:'',//经纪商选择
        money:'',//转账金额
        remark:''//备注
        },
        selects:[{
              value: '选项1',
              label: '经纪商1'
              }, {
              value: '选项2',
              label: '经纪商2'
         }],
          myData: {
                  datas:[{date:'2019-04-30 10:32:24',accountCode:'000001',agent:'经纪商1',money:'10000',remark:'尽快审批'}]
               }

      }
    },
    methods: {
      onSubmit(data){
          alert("提交");
      },
      // 清除
            resetForm (formName) {
              var self = this;
              self.$refs[formName].resetFields();
            },
      investmentComDataChangeSort(val){
              var self = this;
              self.orderByString = self.$fun.orderByString(val);
              self.fun_nvestmentCommittee();
      }
    }
  }
</script>

<style rel="stylesheet/scss" lang="scss" >

</style>



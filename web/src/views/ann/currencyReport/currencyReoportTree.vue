<template>
  <div class="currencyStyle">
    <el-dialog
      top="7vh"
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      width="80%"
      @closed="handleClose"
      :close-on-click-modal="false"
      center
    >
      <div class="dialogMain">
        <el-row>
          <!-- :filter-node-method="filterNode" -->
          <el-col :span="4">
            <el-tree
              ref="tree"
              :data="treeData"
              :props="defaultProps"
              :check-strictly='true'
              class="filter-tree"
              show-checkbox
              node-key="id"
              highlight-current
              :expand-on-click-node='false'
              check-on-click-node
              @check-change="selectTreeNode"
              @check='isCheck'
            >
            </el-tree>
          </el-col>
          <el-col :span="20" v-show='isViewDataInfo'>
            <div class="rightStyle" v-loading="isViewLoading">
              <span>{{ rightTitle }}</span>
              <div class="tableLsit">
                <currencyReportPage v-if="currencyReportPageShow" ref="currencyReportPageRef"></currencyReportPage>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import currencyReportPage from '@/views/dataReport/currencyReport'
export default {
  components: {
    currencyReportPage
  },
  data() {
    return {
      dialogVisible: false,
      currencyReportPageShow: false,
      isViewDataInfo: false,
      isViewLoading: false,
      dialogTitle: "",
      rightTitle: '',
      selectTreeOption: {},
      treeData: [
        {
          id: 1,
          label: "一级 1",
          children: [
            {
              id: 4,
              label: "二级 1-1",
              children: [
                {
                  id: 9,
                  label: "三级 1-1-1",
                },
                {
                  id: 10,
                  label: "三级 1-1-2",
                },
              ],
            },
          ],
        },
      ],
      defaultProps: {
        children: "children",
        label: "label",
      },
      dataForm: {
        dataDate: "",
        endDate: "",
        reportCode: "",
        recordId: "",
      },
    };
  },
  methods: {
    init(data) {
      this.dialogVisible = true;
      this.dialogTitle = "";
      for (let i in this.dataForm) {
        this.dataForm[i] = "";
      }
      this.getDataForm(data);
    },
    getDataForm(data) {
      this.dialogTitle = data.reportName;
      if(data.dateData){
         this.dataForm.dataDate = data.dateData;
		     this.dataForm.endDate = data.dateData;
      }
      if(data.reportId){
        this.dataForm.reportCode = data.reportId;
      }
	   if(data.id){
        this.dataForm.recordId = data.id;
      }
    },
    // 当前节点选中
    isCheck (data, check) {
      if (check.checkedNodes.length === 1) {
        let checkData = check.checkedNodes
        this.isViewDataInfo = true
        this.isViewLoading = true
        this.rightTitle = check.checkedNodes[0].label
        this.isViewLoading = false
        this.currencyReportPageShow = true
        this.$nextTick(() => {
          this.$refs.currencyReportPageRef.currencyInit(this.dataForm)
        })
      } else {
        this.isViewDataInfo = false
        this.isViewLoading = false
        this.rightTitle = ''
      }
    },
    selectTreeNode(data, checked, indeterminate) {
      if (checked) {
        const arr = [data.id];
        this.$refs.tree.setCheckedKeys(arr);
      }
    },
    // filterNode(value, data) {
    //   if (!value) return true;
    //   return data.name.indexOf(value) !== -1;
    // },
    handleRefreshChange() {
      this.getList(this.page);
    },
    handleClose() {
      this.$emit('currencBtn')
    },
  },
};
</script>
<style lang='scss'>
.currencyStyle {
  .el-dialog {
    width: 90% !important;
  }
  .dialogMain {
    min-height: 500px;
    max-height: 500px;
    overflow-y: scroll;
  }
}
</style>

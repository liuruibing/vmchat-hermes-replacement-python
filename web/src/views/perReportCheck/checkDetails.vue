<template>
  <div class="check_details">
    <el-container>
      <el-main>
        <el-row style="height: 100%">
          <el-col :span="6" style="height: 100%">
            <div class="baobiao_name">{{ baobiao_name }}</div>
            <el-tree
              class="check_details_tree"
              ref="dataTree"
              :data="treeData"
              node-key="txtId"
              :props="{ label: 'txtName', children: 'children' }"
              :expand-on-click-node="false"
              :render-content="renderContent"
              :indent="40"
              accordion
              @node-click="nodeClick"
              :default-expanded-keys="defaultexpandedkeys"
            >
            </el-tree>
          </el-col>
          <el-col :span="18" style="height: 100%">
            <div style="padding: 0 0 0 20px;height: 100%">
              <el-form
                :inline="true"
                ref="formInline"
                :model="formInline"
                style="margin-bottom: 8px"
                class="demo-form-inline form_inline_search"
              >
                <el-row>
                  <el-col :span="16">
                    <div style="width: 100%; height: 50px">
                      <el-form-item label="核对状态" prop="verifyStatus">
                        <el-radio
                          @change="selectChange"
                          v-model="formInline.verifyStatus"
                          label="-1"
                          >全部</el-radio
                        >
                        <el-radio
                          @change="selectChange"
                          v-model="formInline.verifyStatus"
                          label="0"
                          >核对不一致</el-radio
                        >
                        <el-radio
                          @change="selectChange"
                          v-model="formInline.verifyStatus"
                          label="1"
                          >核对一致</el-radio
                        >
                      </el-form-item>
                    </div>
                  </el-col>
                  <el-col :span="8">
                    <el-form-item class="search_button_com">
                      <!-- <el-button type='primary' @click='onSubmit(true)' style='margin-bottom: 5px;' size='small'><i class='el-icon-search'></i>查询</el-button>
            <el-button type='primary' plain @click='restForm()' style='margin-bottom: 5px; ' size='small'><i class='el-icon-delete'></i>重置</el-button> -->
                    </el-form-item>
                  </el-col>
                </el-row>
              </el-form>
              <div class="forms_table_title">
                <i class="el-icon-s-data"></i>列表
              </div>
              <el-table
                ref="multipleTable"
                id="checkDetails_table"
                @sort-change="handleSortChange"
                :data="tableData"
                border
                stripe
                v-loading="tableLoading"
                style="width: 100%"
                height="calc(100% - 150px)"
              >
                <el-table-column
                  type="index"
                  label="序号"
                  fixed
                  align="center"
                  width="60"
                >
                </el-table-column>
                <el-table-column
                  prop="elementName"
                  sortable="custom"
                  show-overflow-tooltip
                  label="项目"
                  min-width="100"
                  algin="left"
                  header-align="center"
                >
                  <template slot-scope="scope">
                    <span :title="scope.row.elementId || ''">{{ scope.row.elementName | noDataFilter }}</span>
                  </template>
                </el-table-column>

                <el-table-column
                  prop="chapterName"
                  sortable="custom"
                  show-overflow-tooltip
                  label="章节"
                  min-width="100"
                  algin="left"
                  header-align="center"
                >
                  <template slot-scope="scope">
                    <span>{{ scope.row.chapterName | noDataFilter }}</span>
                  </template>
                </el-table-column>

                <el-table-column
                  prop="elementValueOwn"
                  sortable="custom"
                  show-overflow-tooltip
                  label="核对系统值"
                  min-width="100"
                  algin="left"
                  header-align="center"
                >
                  <template slot-scope="scope">
                    <span :style="scope.row.verifyStatus === '0'?{'color':'red'}:''">{{ scope.row.elementValueOwn | noDataFilter }}</span>
                  </template>
                </el-table-column>

                <el-table-column
                  prop="contextRefOwn"
                  sortable="custom"
                  show-overflow-tooltip
                  label="备注"
                  min-width="100"
                  algin="left"
                  header-align="center"
                >
                  <template slot-scope="scope">
                    <span>{{ scope.row.contextRefOwn | noDataFilter }}</span>
                  </template>
                </el-table-column>

                <el-table-column
                  prop="elementValueImp"
                  sortable="custom"
                  show-overflow-tooltip
                  label="XBRL值"
                  min-width="100"
                  algin="left"
                  header-align="center"
                >
                  <template slot-scope="scope">
                    <span :style="scope.row.verifyStatus === '0'?{'color':'red'}:''">{{ scope.row.elementValueImp | noDataFilter }}</span>
                  </template>
                </el-table-column>

                <el-table-column
                  prop="contextRefImp"
                  sortable="custom"
                  show-overflow-tooltip
                  label="备注"
                  min-width="100"
                  algin="left"
                  header-align="center"
                >
                  <template slot-scope="scope">
                    <span>{{ scope.row.contextRefImp | noDataFilter }}</span>
                  </template>
                </el-table-column>

                <el-table-column
                  prop="verifyStatus"
                  sortable="custom"
                  show-overflow-tooltip
                  label="核对状态"
                  min-width="100"
                  algin="left"
                  header-align="center"
                >
                  <template slot-scope="scope">
                    <span
                      style="color: red"
                      v-if="scope.row.verifyStatus === '0'"
                      >不一致</span
                    >
                    <span v-else-if="scope.row.verifyStatus === '1'"
                      >一致</span
                    >
                    <span v-else>{{
                      scope.row.verifyStatus | noDataFilter
                    }}</span>
                  </template>
                </el-table-column>

                <el-table-column
                  prop="valueDiff"
                  sortable="custom"
                  show-overflow-tooltip
                  label="差值"
                  min-width="100"
                  algin="left"
                  header-align="center"
                >
                  <template slot-scope="scope">
                    <span
                      style="color: red"
                      v-if="scope.row.verifyStatus == '0'"
                      >{{ scope.row.valueDiff | noDataFilter }}</span
                    >
                    <span v-else>{{ scope.row.valueDiff | noDataFilter }}</span>
                  </template>
                </el-table-column>
              </el-table>
              <Pagination
                :total="total"
                :page="formInline.pageNum"
                :limit="formInline.pageSize"
                @pagination="Pagination"
              ></Pagination>
            </div>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import tableMethod from '@/utils/tableHeight'
import commonFun from "@/filters/new_common";
import pageApi from "@/api/xbrl/xbrl";
import Pagination from "@/components/Pagination";
export default {
  components: { Pagination },
  props: {
    PageData: {},
  },
  data() {
    return {
      // 左侧树形图数据
      baobiao_name: "",
      treeData: [], //处理后的树形数据
      originTreeData:[], //处理前的树形数据
      defaultexpandedkeys: [],
      // 右侧列表数据
      tableData: [],
      tableLoading: false,
      formInline: {
        verifyStatus: "-1",
        recordId: "",
        orderString: "",
        pageSize: 50,
        pageNum: 1,
        elementId:"",

      },
      total: 0, //总条数

      elementId:"",
      txtId:"",
      txtPid:"",
    };
  },
  created(){
    // console.log('created');
    // tableMethod.fetTableHeight(this,'checkDetails_table');
  },
  mounted() {
    // console.log("mounted", this.PageData);
    this.formInline.recordId = this.PageData.recordId;
    // this.onSubmit(true);
    this.getTreeData(this.PageData);
  },
  methods: {
    renderContent(h, { node, data, store }) {
      // console.log(node,data,store);
      return (
        <span class="custom-tree-node1">
          <span title={node.label}>
            {data.elementId
              ? `${node.label}(${data.elementId})`
              : `${node.label}`}
          </span>
        </span>
      );
    },
    ppp(Current) {
      // console.log('ppp',Current);
      if (Current.children) {
        Current = Current.children[0];
        this.ppp(Current);
      }
      return Current;
    },
    getTreeData() {
      let params = {
        // id:'31A580BA0B834D9BB755484F6516ADA1'
        id: this.PageData.recordId,
      };
      pageApi.getCheckTree(params).then((res) => {
        if (res.data.status == 0) {
          // let data = res.data.data;
          this.originTreeData = res.data.data;
          if (res.data.data.length) {
            let obj = res.data.data.find(item=>{
              return !item.txtPid
            })
            let txtId = ''
            if(!obj){
              // let oo = {
              //   creator: "admin",
              //   custAuthSwitch: "off",
              //   elementId: "0000",
              //   gmtCreate: 1626400418583,
              //   gmtCreateStr: "2021-07-16 09:53:38",
              //   gmtModify: 1626400418583,
              //   isDeleted: 0,
              //   modifier: "admin",
              //   productAuthSwitch: "off",
              //   txtId: "XBRL",
              //   txtName: "核对报告"
              // }
              
              // res.data.data.push(oo)
            }
            if(obj){
              txtId = obj.txtId
            }else{
              this.$message({
                type:"info",
                message:"未配置章节！"
              })
              return
            }
            // console.log('obj',obj);
            let data = commonFun.converTreeData(res.data.data,txtId || "XBRL","txtPid","txtId").data;
            let data1 = commonFun.converTreeData(res.data.data,txtId || "XBRL","txtPid","txtId").expandRowKeys;
            // console.log(data);
            // console.log(data1);
            this.treeData = data;
            let Current = {};
            let Current1 = {};

            // 默认选中第一个子节点
            // if (data.length) {
            //   if (data[0].children) {
            //     Current = data[0].children[0];
            //     Current1 = this.ppp(Current);
            //   }
            // }
            // // console.log('Current1',Current1);
            // if (Current1.txtId) {
            //   this.defaultexpandedkeys = [ Current1.txtId];
            // }
            // // 显示dialog
            // this.$nextTick(() => {
            //   // this.$refs.dataTree.setCurrentKey('10001');
            //   this.$refs.dataTree.setCurrentNode(Current1);
            //   this.nodeClick(Current1);
            // });

            // 默认选中主节点
            if(data.length){
              Current1 = data[0];
            }
            if (Current1.txtId) {
              this.defaultexpandedkeys = [ Current1.txtId];
            }
            this.$nextTick(() => {
              this.$refs.dataTree.setCurrentNode(Current1);
              this.nodeClick(Current1);
            });
          } else {
            this.$message("未配置章节！");
            return;
          }
        } else {
          this.$message({
            type: "error",
            message: res.data.message || "数据获取失败！",
          });
        }
      });
    },
    onSubmit(flag) {
      if(!this.treeData.length) return
      this.tableLoading = true;
      // 消除没有值的参数
      if (flag) {
        this.formInline.pageNum = 1;
      }

      let params = commonFun.parameterSrc(this.formInline);
      if (this.formInline.verifyStatus &&this.formInline.verifyStatus === "-1") {
        params.verifyStatus = "";
      }
      pageApi
        .geVerifyDetail(params)
        .then((response) => {
          if (!response.data.error) {
            this.tableData = response.data.data.list;
            // 页面总条数
            this.total = response.data.data.total;
          } else {
            this.tableData = [];
            this.total = 0;
            this.formInline.pageSize = 50;
            this.formInline.pageNum = 1;
          }
          this.tableLoading = false;
        })
        .catch(() => {                          
          this.tableData = [];
          this.total = 0;
          this.formInline.pageSize = 50;
          this.formInline.pageNum = 1;
          this.tableLoading = false;
        });
    },
    nodeClick(obj,node,eve) {
      // console.log('obj',obj);
      // if(!obj.children){
        this.formInline.elementId = obj.txtId;
        this.onSubmit(true);
      // }
    },
    selectChange() {
      // let params = {}
      // params.recordId = this.PageData.recordId;
      // params.elementId = this.elementId;
      // params.txtId = this.txtId;
      // params.txtPid = this.txtPid;
      // params.verifyStatus = this.formInline.verifyStatus;
      // console.log(params);

      // let params1 = JSON.parse(JSON.stringify(this.formInline));
      // console.log(params1);
      this.onSubmit(true);
    },
    // 排序
    handleSortChange(val) {
      this.formInline.orderString = commonFun.orderByString(val);
      this.onSubmit(false);
    },
    // 分页
    Pagination(val) {
      this.formInline.pageSize = val.limit; //页面条数
      this.formInline.pageNum = val.page; //页面
      this.onSubmit(false);
    },
  },
};
</script>

<style lang="scss">
.check_details {
  .check_details_tree {
    .custom-tree-node1 {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 14px;
      padding-right: 8px;
      width: 100%;
      span {
        display: inline-block;
        width: 98%;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
    }
  }
}
.check_details{
  height: 100%;
  // #checkDetails_table{
  //   height: calc(100% - 150px);
  // }
  .check_details_tree{
    height: calc(100% - 15px);
    overflow: auto;
  }
}
</style>
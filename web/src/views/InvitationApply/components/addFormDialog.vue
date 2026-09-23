<template>
  <div id="rule_add_dialog">
    <el-dialog
      custom-class="warningMonitoring-dialog"
      title="申请绩效数据权限"
      :visible.sync="visible"
      width="900px !important"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      @close="handleClose"
    >
      <el-form :model="formData" ref="formData" :rules="searchRules" label-width="150px" class="standard-form" style="width: 100% !important;">
        <el-row style="margin: 10px 30px">
          <div>检查到您所选产品中涉及以下管理人未进行合格投资者或者代销机构认证，若您已取得以下管理人的合格投资者或者代销机构认证资格请予以承诺。</div>
          <div>

          </div>
          <div style="max-height: 190px; overflow-y: auto; margin: 10px 0px;">
            <div v-for="item in tableData2" :key="item.idGlr" class="text item" style="border-bottom: 1px solid #eee; padding: 10px 0;">
              {{item.nameGlr }}
              <el-checkbox
                style="float: right;"
                :label="item.nameGlr"
                :key="item.idGlr"
                v-model="item.checked"
                @change="handleCheckboxChange(item)
                 ">承诺&nbsp;</el-checkbox>

            </div>
          </div>
        </el-row>
        <el-row>
          <el-col :span="12">
            <el-form-item label="权限等级" prop="authLevel">
              <el-select v-model="formData.authLevel" size="small" clearable filterable  @change="handleAuthLevelChange">
                <el-option v-for="item in indexGrantArr" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="数据频率" prop="frequency">
              <el-select v-model="formData.frequency" size="small" clearable filterable >
                <el-option v-for="item in indexFrequencyArr" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="24">
            <el-form-item label="申请意向" prop="applyIntention">
            <el-select
              v-model="value"
              filterable
              allow-create
              default-first-option
              placeholder="申请意向"
              @change="handleSelectChange"
            >
            <el-option
              v-for="item in options"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            ></el-option>
            </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <div style="text-align: center; margin-top: 20px">
        </div>
      </el-form>
      <div class="table-content" id="standard-table">
        <div id="standard-table-margin">
          <vxe-table
            ref="refsTable"
            v-loading="tableLoading"
            :cell-style="{ height: '50px' }"
            :data="tableData"
            auto-resize
            stripe
            sync-resize
            show-overflow="tooltip"
            style="width: 100%;max-height: 400px;overflow-y: auto;"
            :sort-config="{ remote: true }"
            resizable
          >
            <vxe-table-column
              v-for="item in column"
              :key="item.prop"
              :align="item.align"
              :field="item.prop"
              :title="item.label"
              :min-width="item.width"
              header-align="center"
            >
              <template slot-scope="{ row }">
              <span v-if="item.prop === 'operateStatus'">
                  <el-tag size="mini" type="success" v-if="row[item.prop] == '1'">运行中</el-tag>
                  <el-tag size="mini" type="danger" v-else>已终止</el-tag>
                </span>
                <span v-else> {{ row[item.prop] | noDataFilter }}</span>
              </template>
            </vxe-table-column>
          </vxe-table>
        </div>
      </div>
      <div style="text-align: center; margin-top: 20px" class="dialog-footer standard-form">
        <el-button size="small" type="primary" v-btn="'submitAdd'" @click="onSubmit('formData')" :disabled="submitting">提 交</el-button>
        <el-button size="small" plain type="info" @click="handleClose()" :disabled="submitting">取 消</el-button>
      </div>
    </el-dialog>
    <el-dialog
      title="合格投资者或代销机构认证承诺"
      :visible.sync="dialogVisible"
      width="30%"
      :before-close="handleClose2">
      <div style="margin: 10px 30px">请贵司特别关注：<br><br>
        贵司请确保<br><br>
        根据《中华人民共和国证券投资基金法》、《私募投资基金监督管理暂行办法》、《私募投资基金募集行为管理办法》及其他相关法律法规，贵司已通过___（{{GlrName}}）_____合格投资者认定相应程序或与___（{{GlrName}}）_____就该私募基金产品签署基金代销协议，且贵司知悉私募基金管理人数据授权行为不视为其应履行的信息披露义务的替代或补充，因上述承诺行为而产生的任何责任或不良后果将由贵司全部自行承担。
        <br><br>
        受限于各种条件，广发证券股份有限公司不保证传输数据的真实性、完整性、准确性、及时性、连续性，并保留无条件随时取消、更新合格投资者或代销机构承诺管理功能的权利和最终解释权。<br><br>
        若贵司确认已知晓并同意上述内容，请点击同意。<br><br>
        *本公司已详细阅读并充分理解上述内容，完全同意并认可确认内容。<br><br></div>
      <div style="text-align: center; margin-top: 20px" class="dialog-footer standard-form">
        <el-button size="small" type="primary" @click="onSubmit2()">同 意</el-button>
        <el-button size="small" plain type="info" @click="handleClose2">拒绝承诺</el-button>
      </div>
    </el-dialog>
    <el-dialog
      title=""
      :visible.sync="dialogVisible3"
      width="30%"
      :before-close="handleClose3">
      <div style="margin: 10px 30px">
        需承诺已获得管理人的合格投资者认证才可发送权限申请请求。若您非该管理人认证的合格投资者，可先申请获得该管理人的合格投资者认证再发起相应权限申请。如需帮助可联系广发证券托管部，电话：020-66338499</div>
      <span slot="footer" class="dialog-footer standard-form">
    <el-button type="primary" @click="dialogVisible3 = false">确 定</el-button>
  </span>
    </el-dialog>
  </div>
</template>

<script>
import pageApi from '../scripts/api.js'
import commonApi from '@/api/common.js'
export default {
  name: '',
  components: {

  },
  props: {
    indexList: {
      type: Array,
      default: () => []
    }
  },
  data() {

    return {
      dialogVisible: false,
      indexGrantArr: [],
      indexFrequencyArr: [],
      dataFreqList:[],
      GlrName:'',
      checkList: [],
      currentItem: null,
      dialogVisible3: false,
      visible: true,
      rowData: {},
      formData: {
        authLevel: '',
        fundCodes:[],
        idGlrCodes:[],
        frequency:'',
        applyIntention:''
      },
      value: [],
      options: [
        { value: '发起线上申请，初步交流', label: '发起线上申请，初步交流' },
        { value: '完成现场沟通，推进合作', label: '完成现场沟通，推进合作' },
        { value: '已投相关产品，深度跟踪', label: '已投相关产品，深度跟踪' }
      ],
      productInfoDetailErrorMessage:'',
      tableData:[],
      tableData2:[],
      tableLoading:false,
      // 添加提交状态标志
      submitting: false,
      column:[
        {
          label: '产品代码',
          prop: 'fundCode',
          align: 'left',
          width: '100px',
          format: 'dict'
        },
        {
          label: '产品名称',
          prop: 'fundName',
          align: 'left',
          width: '100px',
        },
        {
          label: '产品管理人',
          prop: 'nameGlr',
          align: 'center',
          width: '100px',
        },
        {
          label: '产品成立日期',
          prop: 'createDate',
          align: 'center',
          width: '100px',
        },
        {
          label: '产品运行状态',
          prop: 'operateStatus',
          align: 'center',
          width: '100px',
        },
      ],
      searchRules: {
        authLevel: [{ required: true, message: '请选择权限等级', trigger: 'change' }],
        applyIntention: [{ required: true, message: '请选择申请意向', trigger: 'change' }],
        frequency: [{ required: true, message: '请选择数据频率', trigger: 'change' }]
      },

    }
  },
  mounted() {
    this.getListDataFreqEdims("DATAFREQ");
  },
  watch: {
    // 监听 tableData 中 checked 状态的变化
    tableData2: {
      handler(newVal) {
        newVal.forEach((item) => {
          if (!item.checked) {
            this.handleCheckboxUncheck(item.idGlr);
          }
        });
      },
      deep: true, // 深度监听
    },
  },
  methods: {

    // 数据频率列表查询
    getListDataFreqEdims (type) {
      // 字典类型
      let params = type
      commonApi.edimsSelectType(params).then(res => {
        let { status, data } = res.data
        if (status === 0) {
          this.dataFreqList = data
        }
      })
    },

    handleAuthLevelChange(val) {
      if(val==='1') {
        this.indexFrequencyArr = this.dataFreqList.filter((item) => item.dimCde === "1"|| item.dimCde === "2")
      }else{
        this.indexFrequencyArr = this.dataFreqList;
      }
    },
    handleSelectChange(val) {
      //单选的
      this.formData.applyIntention =val;//val.join(',');
    },
    handleCheckboxChange(item) {
      item.checked = false;
      this.currentItem = item;
      this.GlrName = item.nameGlr
      this.dialogVisible = true;
    },
    handleClose2() {

      if (this.currentItem) {
        this.handleCheckboxUncheck(this.currentItem.idGlr);
      }
      this.dialogVisible = false
      this.currentItem = null;
      console.log(this.checkList)
    },
    onSubmit2() {
      if (this.currentItem) {
        // 手动选中复选框
        this.currentItem.checked = true;
        //若有先删除
        this.handleCheckboxUncheck(this.currentItem.idGlr);
        // 将 idGlr 添加到选中数组
        this.checkList.push(this.currentItem.idGlr);
      }
      this.dialogVisible = false

      console.log(this.checkList)
    },
    handleCheckboxUncheck(idGlr) {
      // 从选中数组中移除
      const index = this.checkList.indexOf(idGlr);
      if (index !== -1) {
        this.checkList.splice(index, 1);
      }
    },
    handleClose3() {
      this.dialogVisible3 = false
    },

    init(data, list, type) {
      this.tableData = []
      this.tableData2 = []
      this.formData.fundCodes = []
      this.GlrName = ''
      this.checkList = []
      this.currentItem = null
      this.indexGrantArr = data
      this.tableLoading = true
      if (type) {
        list.checked = false;
        this.tableData.push(list)

        if (!(list.orgPromise === '1' && list.mgrPromise === '1')) {
          this.tableData2.push(list);
        }

        this.formData.fundCodes.push(list.fundCode)
      } else {
        list.forEach((item) => {
          item.checked = false; // 添加 checked 属性并设置为 false
        });
        this.tableData = list
        this.tableData2 = list.filter(item => !(item.orgPromise === '1' && item.mgrPromise === '1'));
        this.tableData2 = [...new Set(this.tableData2.map(item => item.nameGlr))]
          .map(nameGlr => this.tableData2.find(item => item.nameGlr === nameGlr));
        for (let i = 0; i < list.length; i++) {
          this.formData.fundCodes.push(list[i].fundCode)
        }
      }

      this.tableLoading = false
    },
    onSubmit(formData) {
      // 防止重复提交
      if (this.submitting) {
        return;
      }

      if (this.checkList.length != this.tableData2.length) {
        this.dialogVisible3 = true
        return
      }
      var self = this
      self.$refs[formData].validate((valid) => {
        if (valid) {
          try {
            let num = '';
            //暂时隐藏
            for (var i = 0; i < this.tableData.length; i++) {
              if (this.tableData[i].fundGrant) {
                if (Number(this.tableData[i].fundGrant) >= Number(this.formData.authLevel)) {
                  num += this.tableData[i].fundName
                  num += '<br>'
                }
              }
            }
            if (num == '') {
              self.submit()

            } else {
              self.$message({
                  message: '您所选择的<br>' + num + '产品已拥有该级权限，请勿重复申请。',
                  type: 'warning',
                  dangerouslyUseHTMLString: true
                }
              )
            }
            //
          } catch (e) {
          }
        } else {
          return false
        }
      })
    },
    submit() {
      var self = this
      this.formData.idGlrCodes = [];
      if (this.checkList.length > 0) {
        this.formData.idGlrCodes = this.checkList
          .map(checkId => this.tableData2.find(item => item.idGlr === checkId))
          .filter(Boolean) // 过滤掉 undefined（未找到的项）
          .map(({ idGlr, nameGlr  }) => ({ idGlr, nameGlr }));
      }

      // 设置提交状态为true，防止重复提交
      this.submitting = true;

      let params = Object.assign({}, this.formData)
      pageApi.authApply(params).then(res => {
        let { status, data, message } = res.data
        if (status === 200) {
          if (data && data.length > 0) {
            self.productInfoDetailErrorMessage = ''
            data.forEach(item => {
              self.productInfoDetailErrorMessage += `${item}`
              self.productInfoDetailErrorMessage += `<br>`
            })
            self.$message({
                message: self.productInfoDetailErrorMessage,
                type: 'warning',
                dangerouslyUseHTMLString: true
              }
            )
          } else {
            self.$message.closeAll()
            self.$message.success(message)

          }

        } else {
          self.$message.error(message)
        }
      }).catch(() => {})
        .finally(()=> {
          // 请求结束，重置提交状态
          this.submitting = false;
          this.visible = false
          this.refresh();
        })
    },
    refresh(){
      this.$emit('refresh')
    },

    // 关闭dialog
    handleClose() {
      // 重置提交状态
      this.submitting = false;
      this.$emit('close')
      this.visible = false
    },

  }
}
</script>
<style lang="scss">
.text {
  font-size: 14px;
}

.item {
  padding: 5px 0;
}
.el-checkbox__inner:hover {
  border-color: #e9c5a5!important
}
</style>

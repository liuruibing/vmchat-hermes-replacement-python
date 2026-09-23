<template>
   <div>
   <div class='forms_table_title'>
       <i class='el-icon-s-data'></i>交互指引配置列表
   </div> 
   <el-table
     ref='multipleTable'
     :data='tableData'
     border
     stripe
     v-loading='tableLoading'
     style='width: 100%'
    >
    <el-table-column
       prop='name'
       show-overflow-tooltip
       label='流程名称'
       min-width='100'
       algin='left'
       header-align='center'
      >
          <template slot-scope='scope'>
             <span >{{ scope.row.name | noDataFilter }}</span>
          </template>
      </el-table-column>
       <el-table-column
       prop='key'
       show-overflow-tooltip
       label='流程类型'
       min-width='100'
       algin='left'
       header-align='center'
      >
          <template slot-scope='scope'>
             <span v-if="scope.row.key ==='Process_ta'">TA流程</span>
              <span v-else-if="scope.row.key ==='Process_pay'">付费流程</span>
               <span v-else-if="scope.row.key ==='Process_invest'">投资流程</span>
                <span v-else-if="scope.row.key ==='Process_transfer'">转账流程</span>
             <span v-else>{{ scope.row.key | noDataFilter }}</span>
          </template>
      </el-table-column>
     <el-table-column
       prop='version'
       show-overflow-tooltip
       label='版本号'
       min-width='100'
       algin='left'
       header-align='center'
      >
          <template slot-scope='scope'>
             <span >{{ scope.row.version | noDataFilter }}</span>
          </template>
      </el-table-column>
      <el-table-column label="操作" fixed="right" min-width="60" align="center">
        <template slot-scope="scope">
          <el-button type="primary" size="small" @click="delData(scope.row)">配置</el-button>
        </template>
      </el-table-column>   
    
     </el-table>
     <el-drawer
        title="流程图"
        direction="ltr"
        size="75%"
        :visible.sync="leftDrawer"
        :before-close="leftDrawerClose"
        >
           <div id="diagram" v-if="diagram_show"></div>

        <el-drawer
            title="交互指引"
            :append-to-body="true"
            direction="rtl"
            size="55%"
            :visible.sync="dialogVisible"
            :before-close="handleClose"
            >
          <MarkdownEditor v-if="editorShow" :mode="'wysiwyg'"></MarkdownEditor>
          <el-button style="margin-top: 10px;margin-left: 10px;" type="primary" size="small" @click="saveData()">确定</el-button>
      </el-drawer>  

      </el-drawer>
   </div>
</template>

<script>
import $ from 'jquery'
import Pagination from '@/components/Pagination'
import commonFun from '@/filters/new_common'
import pageApi from  '@/api/transfer/workApimin.js';
import MarkdownEditor from '@/components/MarkdownEditor'
import commonApi from '@/api/common'
export default {
   name:'',
   components: {Pagination,MarkdownEditor},
   data () {
      return {
         formInline:{
            name:'',
            pageSize: 10,
            pageNum:1
         },
         tableData: [], //表格数据
         tableLoading: false, //表格加载
         tableMultipleSelection: [],//表格选择数据集合
         total:0,//总条数
         leftDrawer:false,
         dialogVisible:false,
         ywId:'',
         MarkdownEditorModel:'',
         saveId:'',
         processKey:'',
         editorShow:false,
         id:'',
         content:'',
         diagram_show:false
      };
   },


   mounted() {
     this.onSubmit();
    // 流程图节点点击事件
    this.clickclick();
   },

   methods: {
     // 查询 
      onSubmit(flag){
         this.tableLoading = true;
         // 消除没有值的参数
         pageApi.get_processdefine('000000').then(response => { 
            if(!response.data.error){ 
                this.tableData = response.data.data; 
             } 
             else{ 
                this.tableData = []; 
               
            } 
                this.tableLoading = false; 
            }).catch(() => { 
                this.tableData = []; 
              
                this.tableLoading = false;
      })
    },
    //分页
    Pagination(val){
       this.formInline.pageSize = val.limit;//页面条数
       this.formInline.pageNum = val.page;//页面
       this.onSubmit(false);
    },
     // table批量选择结果
    handleSelectionChange(val) {
       this.tableMultipleSelection = val;
    },
     // table批量选择结果
    restForm() {
       var self = this;
       self.refs['formInline'].resetFields();
    },
    //处理
    delData(row){
      // console.log(row);
        this.leftDrawer = true;
        this.diagram_show = true;
        let id = row.id;
        if(row.key){
            this.processKey = row.key.split('_')[1];
        }else{
          this.processKey = '';
        }
        
        //获取流程定义任务显示节点对象
         pageApi.get_processdefine_taskIndex(id).then(response => { 
            if(response.data.status === 0){ 
                var xmlIdArr = [];
                let dataArr = response.data.data;
                for (var i = 0; i < dataArr.length; i++) {
                  xmlIdArr.push(dataArr[i].xmlId)
                }
               this.getBpm(row,xmlIdArr);
             }else{
              this.$message.closeAll();
              this.$message.error('获取流程定义任务显示节点对象失败');
            } 
            }).catch(() => { 
               
            })
    },
    getBpm(row,arr){
      let bpmnId = row.id;
         var bpmnxml= '';
        pageApi.get_processdefine_xml(bpmnId).then(res =>{
            if(res.data.status === 0){
               
                let diagramXML =  res.data.data;
                //$(".setting_box_one").fadeOut(100);
                $("#diagram").html("");
                $("#diagram").fadeIn(100);
                // $(".bpmn_delete_img").fadeIn(100);
                // $(".diagram_extensions_set").fadeIn(100);
                // console.log(diagramXML, arr);
                var id =  commonFun.bpmnModule(diagramXML, arr, [], [],this)
                // console.log(id);
                let self = this;
                //  //流程全局配置
                // $("body").on('click','.click',function(){
                //   console.log(self.$route.path);
                //   let routePath = self.$route.path || '';  // ----- 解决指令页面点击也会弹出的问题 -----
                //   if(routePath != '/setting/bpmList') return;  // ----- 解决指令页面点击也会弹出的问题 -----

                //   // 显示弹窗
                //   // console.log(this);
                //   self.ywId = this.id;
                //   // console.log(this.id);
                //   self.dialogVisible = true;
                //   self.saveId = '';
                //    setTimeout(function(){
                //     var aa = $('.te-mode-switch-section');
                //     if(aa.length>0){
                //         aa[0].style.display="none";
                //     }
                    
                //   },300)
                //   self.getHandleHtml(this.id);
                // });
            }else{
              this.$message.closeAll();
              this.$message.error('查询流程图失败');
            }
          }).catch(() => {
            this.$message.closeAll();
            this.$message.error('查询流程图失败');
        })
    },
    getHandleHtml(ywId){
      if(!ywId){
          this.$message.closeAll();
          this.$message.error('taskKey为空');
          return;
      }
      if(!this.processKey){
        this.$message.closeAll();
        this.$message.error('processKey为空');
        return;
      }
       this.editorShow = true;
      let handleHtmlParams = {};
      let id = ywId.substr(5);
      handleHtmlParams.processKey = this.processKey;
      handleHtmlParams.taskKey = id;
       commonApi.getHandleHtml(handleHtmlParams).then(res =>{
            if(res.data.status === 200){
              if(res.data.data){
                 
                  let html = res.data.data.html;
                  this.content = html;
                  this.saveId =  res.data.data.id;
                  let hh = $('.tui-editor-contents');
                  // console.log(hh);
                  $('.tui-editor-contents')[1].innerHTML = html;
                  // $('.CodeMirror-code')[0].innerHTML = html;
              }else{
                 $('.tui-editor-contents')[1].innerHTML = "";
              }
            }else{
               $('.tui-editor-contents')[1].innerHTML = "";
              this.$message.closeAll();
              this.$message.error('查询交互指引失败');
            }
          }).catch(() => {
            this.$message.closeAll();
            this.$message.error('查询交互指引失败');
        })  

        
     },
    saveData(){
      let handleHtmlParams = {};
      let id = this.ywId.substr(5);
      handleHtmlParams.processKey = this.processKey;
      handleHtmlParams.taskKey = id;
      if(this.saveId){
          handleHtmlParams.id = this.saveId;
      }
      
      let hh = $('.tui-editor-contents');
      // console.log(hh);
      let html = $('.tui-editor-contents')[1].innerHTML;
      handleHtmlParams.html = html;
      let self = this;
      // console.log(handleHtmlParams);return
      commonApi.saveHandleHtml(handleHtmlParams).then(res =>{
            if(res.data.status === 200){
             
              this.$message.closeAll();
              this.$message.success('保存成功');
              self.dialogVisible = false;
            }else{
              this.$message.closeAll();
              this.$message.error('保存失败');
            }
          }).catch(() => {
            this.$message.closeAll();
            this.$message.error('保存失败');
        }) 
      
    },
       //关闭dialog
     handleClose(done){
          done();
         this.editorShow = false;
       
    },
    leftDrawerClose(done){
      console.log('leftDrawerClose');
      done();
      $("#diagram").html("");
      this.diagram_show = false;
    },
    clickclick(){
      //流程全局配置
      let self = this;
      $("body").on('click','.click',function(){
        // console.log(self.$route.path);
        let routePath = self.$route.path || '';  // ----- 解决指令页面点击也会弹出的问题 -----
        if(routePath != '/setting/bpmList') return;  // ----- 解决指令页面点击也会弹出的问题 -----

        // 显示弹窗
        // console.log(this);
        self.ywId = this.id;
        // console.log(this.id);
        self.dialogVisible = true;
        self.saveId = '';
        setTimeout(function(){
          var aa = $('.te-mode-switch-section');
            if(aa.length>0){
              aa[0].style.display="none";
            }
                      
        },300)
        self.getHandleHtml(this.id);
      });
    }
 }
}
</script>
<style lang='css' scoped>

</style>
<style rel="stylesheet/scss" lang="scss" >


   :focus{
        outline:0;
      }

      .el-drawer__header>:first-child {

            color: #409EFF;
        }
      
</style>
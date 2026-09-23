<template>

  <el-aside :width="boxWidth" class="ProductAndProperty_box"  >
    <div style="height: 100%;">
      <div :class="ProductAndPropertyData.productClass"  >
        <div  class="content_input" style="width: 233px;">
          <el-select v-model="manageVal" filterable :clearable = "productClearable"  @change="manageValChange"  class="productSelectBox" placeholder="请选择投资经理">
            <el-option
              v-for="(group, index) in manageArr"
              :key="index"
              :label="group.userName"
              :value="group.account">
            </el-option>
          </el-select>

          <el-input v-model="productSearch" style="cursor: pointer;"  v-on:input = "fun_productSearch" @keyup.enter.native = "fun_productSearch"  size="mini" prefix-icon = "el-icon-search" placeholder="请输入组合名称或代码"></el-input>
          <p style="color: #f56c6c;margin-top: 2px;" >{{productSearchHint}}</p>
        </div>
        <el-tree
          ref="productTree"
          :data="productData"
          node-key="id"
          :show-checkbox="ProductAndPropertyData.productSearchCheckbox"
          :default-checked-keys="ProductDefaultChecked"
          :default-expand-all = true
          @node-click="productNodeClick"
          @check="productCheckClick"
          accordion
          class="content_tree"
          v-loading="loading && $store.state.setting.loadingShow"
        >
              <span class="el-tree-node__label" slot-scope="{ node, data }" >
                <el-tooltip effect="dark" :content="node.label" placement="top" offset = 20  :visible-arrow = false >
                  <span >{{ node.label }}</span>
                  <!--style="width: 150px;display: inline-block;overflow: hidden;"-->
                </el-tooltip>
              </span>
        </el-tree>
      </div>
      <div  :class="ProductAndPropertyData.propertyClass"  style="width: 233px;">

        <el-select v-model="propertyType" @change="propertyType_change"  class="propertySearchBox" placeholder="请选择资产分类" style="width: 90px;" >
          <el-option
            v-for="(group, index) in propertyTypeArr"
            :value="group.dimCde"
            :key="index"
            :label="group.dimNme">
          </el-option>
        </el-select>
        <div  class="content_input">
          <el-input v-model="propertySearch" style="cursor: pointer;"   @keyup.enter.native = "fun_propertySearch"  v-on:input = "fun_propertySearch"  size="mini" prefix-icon = "el-icon-search" placeholder="请输个券名称或代码"></el-input>
          <p style="color: #f56c6c;margin-top: 2px;">{{propertySearcHint}}</p>
        </div>
        <el-tree
          ref="propertyTree"
          :data="propertyData"
          :show-checkbox="ProductAndPropertyData.propertySearchCheckbox"
          :default-expand-all = true
          @node-click="propertyNodeClick"
          @check="propertyCheckClick"
          accordion
          class="content_tree content_tree_bottom"
          v-loading="loadingpro && $store.state.setting.loadingShow"
        >
          <!--  lazy-->
        </el-tree>
      </div>
      <div class="flex_center left_right_button" style="cursor: e-resize;" @mousedown="productMove">
        <i :class="left_right_button_icon" style="cursor: pointer;"  @click="ProductAndProperty_left_right"></i>
      </div>
    </div>
  </el-aside>
</template>


<script>
  import $ from 'jquery'
  import commonApi from '@/api/common'
  import fun from '@/filters/common'
  import investmentManagerApi from '@/api/managementView/investmentManager'
  export default {
    name: "ProductAndProperty",
    props: {
      ProductAndPropertyData: {
        productSearchCheckbox:'',//组合是否显示checkbox
        productClass:'',//组合类名
        propertySearchCheckbox:'',//资产是否显示checkbox
        propertyClass:'',//资产类名
        isEquity:'',//是否含权
        isManager:false,//是否是投资经理绩效详情页面
        tagsName:'',// 组合列表 tag子组件传值区分
      },
    },
    data() {
      return {
        productSearch:'',//产品搜索条件
        manageArr:[],//投资经理数组
        manageVal:'',//投资经理选择的值
        manageName:'',//投资经理选择的值
        productClearable:true,//投资经理页面不显示删除按钮 其它页面显示  默认显示
        productData:[],//产品列表数据
        loading:false,//产品搜索loading
        productSearchHint:'',//产品分类搜索提示
        productCheckHistory:[],//记录历史选择的产品
        ProductDefaultChecked:[],//产品默认选中


        propertyType: '',//资产分类搜索
        propertyTypeArr:[],//资产分类数组
        propertySearch:'',//资产分类搜索条件
        propertySearcHint:'',//资产分类搜索提示
        propertyData:[],//资产分类树形数据
        loadingpro:false,
        isPropertyShowCheckbox:'',// 资产分类初始是否显示checkbox
        boxWidth:'251px',//左侧列表宽度
        left_right_button_icon:'el-icon-arrow-left'//左侧列表icon
      }
    },
    mounted() {
      var self= this;

      // 组合显示才发送请求
      if(self.ProductAndPropertyData.productClass == "product_show_box" || self.ProductAndPropertyData.productClass == "content_average_box" ){


        // 显示投资经理下拉
        // 获取投资经理数组
        new Promise((resolve, reject) => {
          investmentManagerApi.managerList('0').then(response => {
            if(response.data.data !== undefined && response.data.data != ''){
              self.manageArr = response.data.data;//投资经理数组
              //如果是投资经理绩效详情页面 默认选中第一个
              if(this.ProductAndPropertyData.isManager == true) {
                self.manageVal = self.manageArr[0].account;
                self.manageName = self.manageArr[0].userName;
                self.productCheckClick();//默认选中之后把投资经理的值传过去
                self.productClearable = false;//该页面不显示叉号
              }
              else{
                self.productClearable = true;//显示叉号
              }
              self.productListsearch();

            }
            else{
              self.productListsearch();
            }
            resolve()
          }).catch(error => {
            self.productListsearch();
            reject(error)
          })
        })


      }

      // 资产显示才发送请求
      if(self.ProductAndPropertyData.propertyClass == "property_show_box" || self.ProductAndPropertyData.propertyClass == "content_average_box" ){
        //资产分类初始是否展示复选框
        let ShowCheckbox =  self.ProductAndPropertyData.propertySearchCheckbox;
        self.isPropertyShowCheckbox = ShowCheckbox;
        // 资产分类搜索数据
        new Promise((resolve, reject) => {
          commonApi.edimsCommon("symbol_type").then(response => {
            self.propertyTypeArr = response.data.data
            // 资产分类默认值
            self.propertyType = "CJRSB";
            //传输长江人社部类型
            this.$emit('propertyNodeClickOneSet', {data :this.propertyType})
            this.$emit('propertyCheckClickOneSet', {data :this.propertyType})
            //资产类型改变初始化
            self.propertyListsearch()
            resolve()
          }).catch(error => {
            reject(error)
          })
        })
      }
      else{

      }

      //接收组合tags传过来的值
      self.$bus.$on('productCheckClickTagsClose' + self.ProductAndPropertyData.tagsName, self.fun_productCheckClickTagsClose);

    },
    //消除多次传输
    beforeDestroy () {
      this.$bus.$off('productCheckClickTagsClose' + this.ProductAndPropertyData.tagsName, this.fun_productCheckClickTagsClose);
    },

    methods: {
      //模糊搜索
      fun_productSearch() {
        var self = this;
        // if (self.productSearch.length < 4 && self.productSearch != '') {
        //   self.productSearchHint = '最少输入4位'
        // }
        // else {
        //如果是投资经理绩效情况界面并且投资经理选择的值为空
        if(self.ProductAndPropertyData.isManager == true && self.manageVal == '') {
          self.$message.closeAll()
          self.$message({
            message: '请选择投资经理',
            type: 'warning'
          });
        }
        else{
          self.productListsearch();
        }
        // }
      },
      // 投资经理下拉搜索
      manageValChange(val){
        var self = this;
        if(self.ProductAndPropertyData.isManager == true) {
          //每一次切换投资经理要清空历史选择的记录
          self.productCheckHistory = [];
          //投资经理绩效情况界面必选投资经理
          if(val == ''){
            self.$message.closeAll()
            self.$message({
              message: '请选择投资经理',
              type: 'warning'
            });
            self.productData = [];//清空组合树状列表
            // 切换时传输空的组合代码 空的投资经理
            self.$emit('productCheckClick', {
              data: [],
              manage: ['','']
            })
            // 清空产品tabs选项卡
            self.$bus.$emit('productCheckClickTags' + self.ProductAndPropertyData.tagsName,{ data: []});

          }
          else{
            self.manageArr.forEach(function (item){
              if(item.account == val){
                self.manageName = item.userName;
              }
            })
            // 切换时传输空的组合代码 新的投资经理
            self.$emit('productCheckClick', {
              data: [],
              manage: [self.manageVal,self.manageName]
            })
            // 清空产品tabs选项卡
            self.$bus.$emit('productCheckClickTags' + self.ProductAndPropertyData.tagsName,{ data: []});
            //产品投资经理绩效情况投资经理下拉单独查询  不能记录之前投资经理选择的值
            self.productListsearchManager();
          }
        }
        else{
          //每一次切换投资经理要清空历史选择的记录
          self.productCheckHistory = [];

          // 清空产品tabs选项卡
          self.$bus.$emit('productCheckClickTags' + self.ProductAndPropertyData.tagsName,{ data: []});
          //清空点击传输的id
          this.$emit('productNodeClick', { data: {}})
          //清空新选择的投资经理下拉组合
          self.$emit('productCheckClick', { data: []})

          self.productListsearch();
        }


      },
      fun_productCheckClickTagsClose(val){
        var self = this;
        var checkedKeys = [];
        //记录最后一次点击tags选择的产品
        self.productCheckHistory = val;

        //删除选择的复选框
        val.forEach(function (item,index) {
          checkedKeys.push(item.id);
        })
        self.$refs.productTree.setCheckedKeys(checkedKeys);
        //把清空的值传输到对应的界面
        if(self.ProductAndPropertyData.isManager == true){
          self.$emit('productCheckClick', {
            data: self.$refs.productTree.getCheckedNodes(true,false),
            manage: [self.manageVal,self.manageName]
          })

        }
        else{
          self.$emit('productCheckClick', { data: self.$refs.productTree.getCheckedNodes(true,false)})
        }

      },
      //产品通用查询
      productListsearch(){
        var self = this;
        self.loading = true;
        new Promise((resolve, reject) => {
          commonApi.fundList(self.productSearch,self.ProductAndPropertyData.isEquity,self.manageVal).then(response => {
            self.loading = false;
            if(response.data.data !== undefined && response.data.data != ''){
              let responseData = response.data.data;
              let productCheckHistory = self.productCheckHistory; //历史选择的值
              let defaultId = []; //默认选中的产品
              //添加历史选择的值
              productCheckHistory.forEach(function (itemHistory,index){
                defaultId.push(itemHistory.id)//默认选中
                for(let i = 0; i < responseData.length; i++){
                  if(responseData[i].id == itemHistory.id){   //存在就结束循环
                    break;
                  }
                  else if(i == responseData.length -1 ){
                    responseData.push(itemHistory);
                  }
                }
              })

              self.productData = fun.searchTreeData(responseData,0).treeNode;


              //如果存在默认选中
              // if(fun.searchTreeData(responseData,0).defaultNode){
              //添加默认选中第一个
              // defaultId.push(fun.searchTreeData(responseData,0).defaultNode.id);
              //  }
              // else{}

              //搜索有值就默认选中
              if(defaultId != ''){
                self.$refs.productTree.setCheckedKeys(defaultId);
                let getCheckedNodesData = self.$refs.productTree.getCheckedNodes(true,false);//选中的节点
                //如果存在默认选择
                // if(fun.searchTreeData(responseData,0).defaultNode){
                //   getCheckedNodesData.push(fun.searchTreeData(responseData,0).defaultNode);
                // }
                // else{}
                let getCheckedNodesDataFilter = []; //去除重复的值
                getCheckedNodesData.forEach(function (item,index) {
                  if(index == 0){
                    getCheckedNodesDataFilter.unshift(item);
                  }
                  else{
                    for(let i = 0; i < getCheckedNodesDataFilter.length; i++){
                      if(getCheckedNodesDataFilter[i].id != item.id && i == getCheckedNodesDataFilter.length - 1){
                        getCheckedNodesDataFilter.push(item);
                      }
                      else if(getCheckedNodesDataFilter[i].id == item.id ){
                        break;
                      }
                    }
                  }
                })
                //默认选中第一个传给页面 checkbox
                self.$emit('productCheckClick', {
                  data: getCheckedNodesDataFilter,
                  manage: [self.manageVal,self.manageName]
                })
                //默认选中第一个传给详情 页面 存在再传值
                // if(fun.searchTreeData(responseData,0).defaultNode){
                //   this.$emit('productNodeClick', { data: fun.searchTreeData(responseData,0).defaultNode});
                // }
                // else{}
                //向标签栏传输数据
                self.$bus.$emit('productCheckClickTags' + self.ProductAndPropertyData.tagsName,{ data: getCheckedNodesDataFilter});

              }
              else{
                self.$refs.productTree.setCheckedKeys(defaultId);
                //清空
                self.$emit('productCheckClick', {
                  data: [],
                  manage: [self.manageVal,self.manageName]
                })
                //默认选中第一个传给详情 页面 存在再传值
                // if(fun.searchTreeData(responseData,0).defaultNode){
                //   this.$emit('productNodeClick', { data: {}});
                // }
                // else{}
                //向标签栏传输数据
                self.$bus.$emit('productCheckClickTags' + self.ProductAndPropertyData.tagsName,{ data: []});


              }


            }
            else{
              self.productData = [];
            }
            resolve()
          }).catch(error => {
            self.loading = false;
            self.productData = [];
            reject(error)
          })
        })

      },
      //产品投资经理绩效情况投资经理下拉单独查询  不能记录之前投资经理选择的值
      productListsearchManager(){
        var self = this;
        self.loading = true;
        new Promise((resolve, reject) => {
          commonApi.fundList(self.productSearch,self.ProductAndPropertyData.isEquity,self.manageVal).then(response => {
            self.loading = false;
            if(response.data.data !== undefined && response.data.data != ''){
              let responseData = response.data.data;
              self.productData = fun.searchTreeData(responseData,0).treeNode;
              //清空之前选择的值
              self.$refs.productTree.setCheckedKeys([]);

              //如果存在默认选中
              // if(fun.searchTreeData(responseData,0).defaultNode){
              //默认选中第一个
              // self.ProductDefaultChecked = [fun.searchTreeData(responseData,0).defaultNode.id];
              //默认选中第一个传给页面 checkbox
              // self.$emit('productCheckClick', {
              //   data: [fun.searchTreeData(responseData,0).defaultNode],
              //   manage: [self.manageVal,self.manageName]
              // })
              //默认选中第一个传给详情 页面
              // this.$emit('productNodeClick', { data: fun.searchTreeData(responseData,0).defaultNode});
              //向标签栏传输数据
              // self.$bus.$emit('productCheckClickTags' + self.ProductAndPropertyData.tagsName,{ data: [fun.searchTreeData(responseData,0).defaultNode]});
              // }
              // else{}

            }
            else{
              self.productData = [];
            }
            resolve()
          }).catch(error => {
            self.loading = false;
            self.productData = [];
            reject(error)
          })
        })

      },
      // 产品节点选择事件
      productNodeClick(data){
        if(data.children === undefined){
          this.$emit('productNodeClick', { data: data})
        }
        else{
        }

      },
      // 产品复选框选择事件
      productCheckClick(data){

        //如果是投资经理绩效情况界面
        if(this.ProductAndPropertyData.isManager == true){
          this.$emit('productCheckClick', {
            data: this.$refs.productTree.getCheckedNodes(true,false),
            manage: [this.manageVal,this.manageName]
          })

        }
        else{
          this.$emit('productCheckClick', { data: this.$refs.productTree.getCheckedNodes(true,false)})
        }
        this.$bus.$emit('productCheckClickTags' + this.ProductAndPropertyData.tagsName,{ data: this.$refs.productTree.getCheckedNodes(true,false)});
        //记录最后一次点击checkbox选择的产品
        this.productCheckHistory = this.$refs.productTree.getCheckedNodes(true,false);

      },

      //资产类型改变调用
      propertyType_change(){
        var self = this;
        self.propertyListsearch();
      },
      propertyListsearch(){
        var self = this;
        new Promise((resolve, reject) => {
          commonApi.listRules(self.propertyType).then(response => {
            if(response.data.data !== undefined && response.data.data != ''){
              self.propertyData = fun.searchTreeData(response.data.data,0).treeNode;
              // 一层不显示复选框
              self.ProductAndPropertyData.propertySearchCheckbox = false;
            }
            else{
              self.propertyData = [];
            }
            resolve()
          }).catch(error => {
            self.propertyData = [];
            reject(error)
          })
        })
      },
      // 资产分类节点选择事件
      propertyNodeClick(data){
        var self = this;

        if(data.checkBox == "checkBoxN" && data.children === undefined ){
          //调取接口取个券
          // new Promise((resolve, reject) => {
          //   commonApi.listRulesCoupon(data.id,self.propertyType).then(response => {
          //     if(response.data.data !== undefined && response.data.data != ''){
          //       self.propertyData = fun.searchTreeData(response.data.data,0).treeNode;
          //       // 显不显示复选框 根据记录的传输数据来定
          //       self.ProductAndPropertyData.propertySearchCheckbox = self.isPropertyShowCheckbox;
          //     }
          //     else{
          //       self.propertyData = [];
          //     }
          //     resolve()
          //   }).catch(error => {
          //     self.propertyData = [];
          //     reject(error)
          //   })
          // })
        }
        else if(data.checkBox == "checkBoxY" && data.children === undefined){
          this.$emit('propertyNodeClick', { data: data })
          //传输长江人社部类型
          this.$emit('propertyNodeClickOneSet', {data :this.propertyType})
        }
      },
      // 资产分类复选框选择事件
      propertyCheckClick(data){

        this.$emit('propertyCheckClick', { data: this.$refs.propertyTree.getCheckedNodes(true,false) })
        //传输长江人社部类型
        this.$emit('propertyCheckClickOneSet', {data :this.propertyType})
      },
      //资产分类搜索
      fun_propertySearch(){
        var self = this;
        if(self.propertySearch.length < 4 ) {
          self.propertySearcHint = '最少输入4位'
        }
        else{
          self.propertySearcHint = '';
          self.loadingpro = true;
          // 调取资产配置模糊匹配接口
          new Promise((resolve, reject) => {
            commonApi.listRulesSearchCoupon(self.propertySearch,self.propertyType).then(response => {
              self.loadingpro = false;
              if(response.data.data !== undefined && response.data.data != ''){
                self.propertyData = fun.searchTreeData(response.data.data,0).treeNode;
                // 显不显示复选框 根据记录的传输数据来定
                self.ProductAndPropertyData.propertySearchCheckbox = self.isPropertyShowCheckbox;
              }
              else{
                self.propertyData = [];
              }
              resolve()
            }).catch(error => {
              self.loadingpro = false;
              self.propertyData = [];
              reject(error)
            })
          })

        }

      },

      // 点击隐藏
      ProductAndProperty_left_right(){
        // 0 关闭 1 开启
        let switchOpen = 1
        var self = this;
        if(self.boxWidth != "15px"){
          switchOpen = 0
          self.boxWidth = '15px';

          self.left_right_button_icon = "el-icon-arrow-right";
        }
        else{
          switchOpen = 1
          self.boxWidth = '251px';
          self.left_right_button_icon = "el-icon-arrow-left";
        }
        // 隐藏打开事件
        self.$emit('asideOpen', switchOpen)
      },
      productMove(e){
        let self = this;
        let odiv = e.target;    //获取目标元素

        //算出鼠标相对元素的位置
        let disX = e.clientX - odiv.offsetLeft;
        let disY = e.clientY - odiv.offsetTop;
        // console.log(disX,disY);
        document.onmousemove = (e)=>{    //鼠标按下并移动的事件
          //用鼠标的位置减去鼠标相对元素的位置，得到元素的位置
          let left = e.clientX - disX;
          let top = e.clientY - disY;
          // console.log(left,top)
          //移动当前元素
          //   setTimeout(function () {
          if(left < 15 || left == 15){
            self.boxWidth = 15+ 'px';
            self.left_right_button_icon = "el-icon-arrow-right";
          }
          else if(left > 700){
            self.boxWidth = 700 + 'px';
            self.left_right_button_icon = "el-icon-arrow-left";
          }
          else{
            self.boxWidth = left + 'px';
            self.left_right_button_icon = "el-icon-arrow-left";
          }
          // },10)


        };
        document.onmouseup = (e) => {
          document.onmousemove = null;
          document.onmouseup = null;
        };

      }

    }
  }


</script>

<style>
  /*左侧整体*/
  .ProductAndProperty_box{
    overflow: hidden;
    position: relative;
    /*transition:width 0.3s;*/
    /*-moz-transition:width 0.3s; !* Firefox 4 *!*/
    /*-webkit-transition:width 0.3s; !* Safari and Chrome *!*/
    /*-o-transition:width 0.3s; !* Opera *!*/
    padding: 5px 0px;
  }
  /*同时显示组合和资产分类*/
  .ProductAndProperty_box .content_average_box{
    height: 50%;
  }
  /*只显示组合*/
  .ProductAndProperty_box .product_show_box{
    height: 100%;
  }
  .ProductAndProperty_box .property_none_box{
    display: none;
  }
  /*只显示资产分类*/
  .ProductAndProperty_box .product_none_box{
    display: none;
  }
  .ProductAndProperty_box .property_show_box{
    height: 100%;

  }

  .ProductAndProperty_box  .content_input{
    width: 100%;
  }
  .ProductAndProperty_box .content_tree{
    width: 100%;
    height:calc(100vh - 180px);
    overflow-y: auto;
    overflow-x: hidden;
    margin-top: 5px;
  }
  .ProductAndProperty_box .content_tree_bottom{
    height: 80%;
  }
  .ProductAndProperty_box .product_show_box .content_tree{
    height:calc(100vh - 180px);
  }
  .ProductAndProperty_box .property_show_box .content_tree{
    height: 90%;
  }
  .ProductAndProperty_box  .content_tree>div{
    /*width: 500px;*/

  }
  /*点击按钮*/
  .ProductAndProperty_box .left_right_button{
    width: 15px;
    background: #f2f2f2;
    height: 100%;
    border-radius: 7.5px;
    position: absolute;
    top: 0px;
    right: 0px;
    z-index: 10;
    cursor: pointer;
  }
  .propertySearchBox{
    width: 100%!important;
    margin-bottom: 10px;
  }
  .propertySearchBox .el-select{
    width: 100%!important;
  }
  .propertySearchBox .el-input__inner{
    height: 28px!important;
    line-height: 28px!important;
  }
  .propertySearchBox .el-input__suffix{
    top: 4px!important;
  }
  /*组合下拉搜索样式*/
  .productSelectBox {
    height: 28px;
    width: 100%;
    margin-bottom: 5px;
  }
  .productSelectBox  .el-input__inner{
    height: 28px;
    line-height: 28px;
  }
  .productSelectBox  .el-input__icon{
    line-height: 28px;
  }


</style>

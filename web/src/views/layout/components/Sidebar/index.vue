<template>
  <!--左侧导航-->
  <el-scrollbar wrap-class="scrollbar-wrapper" class="body_left_meau">
    <el-menu
      :unique-opened="true"
      :show-timeout="200"
      :default-active="$route.path"
      :collapse="isCollapse"
      mode="vertical"
      background-color="#f0f5f6"
      text-color="#3f3f3f"
      active-text-color="#409eff"
    >
      <!--style=" width: 246px!important;"-->
      <!--保存路由-->
      <sidebar-item
        v-for="route in meauPermissionRouters"
        v-if="route.meta.visible !== 'false'"
        :key="route.id"
        :item="route"
        :base-path="route.path"
      />
    </el-menu>
  </el-scrollbar>
</template>

<script>
import { mapGetters } from "vuex";
import SidebarItem from "./SidebarItem";

export default {
  components: { SidebarItem },
  data() {
    return {
      meauPermissionRouters: [],// 菜单路由
      meauNumtoDoTasks:[], // 菜单添加处理菜单流程待办个数
    };
  },
  computed: {
    ...mapGetters(["permission_routers", "sidebar"]),
    isCollapse() {
      return !this.sidebar.opened;
    }
  },
  mounted() {

   //排除根节点children长度为一的， 类似于首页这样的单页要排除
         this.meauPermissionRouters = JSON.parse(
          JSON.stringify(this.permission_routers)
        );

         let meauReault = [];
         this.meauPermissionRouters.forEach((item, index) => {
           //排除无子级和带有隐藏属性的
           if (item.children && !item.hidden) {
             // 排除没有子页面的路由
             if (item.Nochildren === true) {
             } else {
               item.children.forEach((itemSon, indexSon) => {
                 // item.path只有一个斜杠 则为更多菜单 更多菜单路由渲染之后判断是否出现 暂时不需要这部分代码
                //  if(item.path === "/"){
                //     // 排除更多菜单里边的单个菜单
                //     if (itemSon.Nochildren === true){
                //     }
                //     else{
                //      itemSon.children.forEach(function(itemMore){
                //        // 用来识别 顶部 路由点击的是哪个
                //        itemMore.parentPath = item.path + itemSon.path;
                //        // 将原来的父级路由添加的子级 否则报错
                //        if (itemMore.path) {
                //           itemMore.path = item.path + itemSon.path + "/" + itemMore.path;
                //        } else {
                //          itemMore.path = item.path + itemSon.path
                //        }
                //        meauReault.push(itemMore);
                //     });
                //     }
                //  }
                //  else{
                     // 用来识别 顶部 路由点击的是哪个
                     itemSon.parentPath = item.path;
                     // 将原来的父级路由添加的子级 否则报错
                    if (itemSon.path) {
                       itemSon.path = item.path + "/" + itemSon.path;
                    } else {
                       itemSon.path = item.path;
                    }
                       meauReault.push(itemSon);
                // }
               });
             }
           } else {
           }
         });
         this.meauPermissionRouters = meauReault;
         // debugger
         console.log(this.meauPermissionRouters)
         // 菜单添加处理菜单流程待办个数
         // this.getNumtoDoTasks();
         // 定时刷新 每隔10秒刷新一次
         // let timer = setInterval(() => {
         //    this.getNumtoDoTasks();
         // },10000)
  },
  methods: {
     // 菜单添加处理菜单流程待办个数
   getNumtoDoTasks(){
      // 调用接口获取菜单待办流程个数
      // this.meauNumtoDoTasks = [
      //   {
      //     "vcactioncode":"TAZLLC",
      //     "count": 12
      //   },
      //   {
      //     "vcactioncode":"FFZLLC",
      //     "count": 11
      //   },
      //   {
      //     "vcactioncode":"GZDB",
      //     "count": 19
      //   }
      // ];
      // 调用方法改变初始化菜单的名称
      this.AddMeauTopPerRoutersTasks();
   },
   AddMeauTopPerRoutersTasks(){
     let self = this;
     this.meauNumtoDoTasks.forEach((item,index) => {
        // 如果存在count字段且数值有意义 再调用树形结构改变值处理函数
        if(item.count || item.count === 0){
            // 传值含义: 数据 比对的是那个字段 查询比对的值  要添加的字段值  树层结构的children字段的key
          self.$fun.changeTreeOppositeValue(this.meauPermissionRouters,"vcactioncode",item.vcactioncode,item.count.toString(),"children");
        }
     })
   },
  }
};
</script>
<style >

.body_left_meau .el-scrollbar__view {
  overflow-y: auto;
}
/*.body_left_meau .el-scrollbar__view .el-menu .el-submenu__icon-arrow{*/
/*right: 81px!important;*/
/*}*/
</style>

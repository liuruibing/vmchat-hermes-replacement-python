<template>
  <div
    v-if="!item.hidden&&item.children"
    :class="item.pId === '0' ? 'meauInlineBox' : 'meauBlockBox' "
  >
    <template
      v-if="hasOneShowingChild(item.children,item) && (!onlyOneChild.children||onlyOneChild.noShowingChildren)&&!item.alwaysShow"
    >
      <app-link :to="resolvePath(onlyOneChild.path)">
        <el-menu-item
          :index="resolvePath(onlyOneChild.path)"
          :class="{'submenu-title-noDropdown':!isNest}"
        >
          <item
            v-if="onlyOneChild.meta"
            :icon="onlyOneChild.meta.icon||item.meta.icon"
            :title="generateTitle(onlyOneChild.meta.title)"
            :tasksNum="onlyOneChild.meta.tasksNum||item.meta.tasksNum"
          />
        </el-menu-item>
      </app-link>
    </template>
    <!--index 唯一标识  id 动态数据 path 静态路由-->
    <el-submenu v-else ref="submenu" :index="resolvePath(item.path)" popper-append-to-body popper-class="submenu_popper_class">
      <template slot="title">
        <item v-if="item.meta" :icon="item.meta.icon" :title="generateTitle(item.meta.title)" :tasksNum="item.meta.tasksNum" />
      </template>

      <template v-for="(child, index) in item.children" v-if="!child.hidden">
        <sidebar-item
          v-if="child.children&&child.children.length>0"
          :is-nest="true"
          :item="child"
          :key="child.path || index"
          :base-path="resolvePath(child.path)"
          class="nest-menu"
        />

        <app-link v-else :to="resolvePath(child.path)" :key="child.name">
          <el-menu-item :index="resolvePath(child.path)">
            <item
              v-if="child.meta"
              :icon="child.meta.icon"
              :title="generateTitle(child.meta.title)"
              :tasksNum="child.meta.tasksNum"
            />
          </el-menu-item>
        </app-link>
      </template>
    </el-submenu>
  </div>
  <div v-else-if="!item.hidden"    style="display:inline-block;" >
    <app-link :to="resolvePath(item.path)">
      <el-menu-item :index="resolvePath(item.path)" :class="{'submenu-title-noDropdown':!isNest}">
        <item v-if="item.meta" :icon="item.meta.icon" :title="generateTitle(item.meta.title)" :tasksNum="item.meta.tasksNum" />
      </el-menu-item>
    </app-link>
  </div>
</template>

<script>
import path from "path";
import { generateTitle } from "@/utils/i18n";
import { isExternal } from "@/utils";
import Item from "./Item";
import AppLink from "./Link";
import FixiOSBug from "./FixiOSBug";

export default {
  name: "SidebarItem",
  components: { Item, AppLink },
  mixins: [FixiOSBug],
  props: {
    // route object
    item: {
      type: Object,
      required: true
    },
    isNest: {
      type: Boolean,
      default: false
    },
    basePath: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      onlyOneChild: null
    };
  },
  methods: {
    hasOneShowingChild(children, parent) {
      const showingChildren = children.filter(item => {
        if (item.hidden) {
          return false;
        } else {
          // Temp set(will be used if only has one showing child)
          this.onlyOneChild = item;
          return true;
        }
      });

      // When there is only one child router, the child router is displayed by default
      if (showingChildren.length === 1) {
        return true;
      }

      // Show parent if there are no child router to display
      if (showingChildren.length === 0) {
        this.onlyOneChild = { ...parent, path: "", noShowingChildren: true };
        return true;
      }

      return false;
    },
    resolvePath(routePath) {
      if (this.isExternalLink(routePath)) {
        return routePath;
      }
      return path.resolve(this.basePath, routePath);
    },
    isExternalLink(routePath) {
      return isExternal(routePath);
    },
    generateTitle
  }
};
</script>
<style rel="stylesheet/scss" lang="scss" >
 .meauInlineBox{
   display:inline-block;
   span{
     color: #000 !important;
   }
 }
 .el-submenu__title{
   span{
     color: #000 !important;
   }
 }
 .meauBlockBox{
   display:block;
   .el-submenu__title{
       font-size: 15px!important;
       background-color: #fff !important;
       color:#3f3f3f !important;
   }
 }
//  子菜单过多，添加滚动条
 .submenu_popper_class{
   max-height: 100%;
   overflow-y: auto;
 }

</style>



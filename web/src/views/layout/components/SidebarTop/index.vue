<template>
  <!--顶部导航-->
  <div class="sidebar-meau-top">
    <el-row justify="center" type="flex">
      <div class="sidebar-meau-topItem">
        <el-menu
          background-color="#ffffff"
          :collapse="false"
          :default-active="$store.state.user.meauTop"
          :show-timeout="200"
          :unique-opened="true"
          active-text-color="#fff"
          mode="horizontal"
          text-color="#000"
          @select="menuSelect"
        >
          <!--style=" width: 246px!important;"-->
          <!--保存路由-->
          <sidebar-item
            v-for="route in meauTopPermissionRouters"
            v-if="route.meta.visible !== 'false'"
            :key="route.path"
            :base-path="route.path"
            :item="route"
            class="meauTopPerInlineBox"
          />
        </el-menu>
      </div>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import SidebarItem from './SidebarItem'
import Layout from '@/views/layout/Layout'
import $ from 'jquery'

export default {

  components: { SidebarItem },
  data() {
    return {
      meauTopPermissionRouters: [], //页面渲染的菜单路由
      meauTopPerRoutersInitialize: [], //记录页面初始化的路由，用来添加更多菜单 直接修改 meauTopPermissionRouters 会导致判断错乱  同时这个变量会应用的获取待办任务功能里
      meauNumtoDoTasks: [], // 菜单添加处理菜单流程待办个数
      // oneChildren: [], // 获取只有一个子级的路由的集合 单页面 废弃 在进入路由之前的事件beforeEach里边做判断
      meauWidthArr: [] // 记录初始化各个菜单的宽度
    }
  },
  computed: {
    ...mapGetters(['permission_routers', 'sidebar']),
    isCollapse() {
      return !this.sidebar.opened
    }
  },
  mounted() {
    // 顶部菜单
    this.meauTopPermissionRouters = JSON.parse(
      JSON.stringify(this.permission_routers)
    )
    // 顶部菜单 删除不含children 和 hiddren 为 true的菜单
    for (let i = 0; i < this.meauTopPermissionRouters.length; i++) {
      if (this.meauTopPermissionRouters[i].children && !this.meauTopPermissionRouters[i].hidden) {
      } else {
        this.meauTopPermissionRouters.splice(i, 1)
        // 数组变化后 后边的数组对象会变成当前 i 值下的对象
        i--
      }
    }
    // 页面初始化路由赋值
    this.meauTopPerRoutersInitialize = JSON.parse(
      JSON.stringify(this.meauTopPermissionRouters)
    )
    // 获取只有一个子级的路由的集合 单页面
    // let oneChildren = [];
    this.meauTopPermissionRouters.forEach((item, index) => {
      if (item.children && !item.hidden) {
        //如果 item.Nochildren === true 则子路由为单路由
        if (item.Nochildren === true) {
          // 顶部只有单个路由（即不显所有菜单下的子路由）有用
          // item.toLink = true;
          // oneChildren.push(item.path);
        }
          // 记录更多按钮下边的单路由 更多菜单路由渲染之后判断是否出现 暂时不需要这部分代码
          // else if(item.path === "/"){
          //   item.children.forEach(function(itemMore){
          //     if(itemMore.Nochildren === true){
          //       oneChildren.push("/" + itemMore.path);
          //     }
          //   });
        // }
        else {
          // 顶部只有单个路由（即不显所有菜单下的子路由）有用
          // item.toLink = false;
        }
        // 顶部只有单个路由（即不显所有菜单下的子路由）有用
        // delete item.children;
      } else {
      }
    })
    // 获取只有一个子级的路由的集合 单页面
    // this.oneChildren = oneChildren;
    // 记录初始化菜单时各个meau的宽度  不写在getMoreMeau方法里边的原因是 调用方法之后出现更多菜单 导致更多菜单下meau的宽度获取失败
    this.$nextTick(function() {
      for (let i = 0; i < $(".meauTopPerInlineBox").length; i++) {
        this.meauWidthArr.push($('.meauTopPerInlineBox').eq(i).width())
      }
      // 初始化根据页面宽度渲染菜单
      this.getMoreMeau()
      // 根据页面宽度变化动态渲染菜单
      window.addEventListener('resize', () => {
        this.getMoreMeau()
      })
      // 菜单添加处理菜单流程待办个数
      this.getNumtoDoTasks()
      // 定时刷新 每隔10秒刷新一次
      let timer = setInterval(() => {
        this.getNumtoDoTasks()
      }, 10000)
    })
  },
  methods: {
    // 动态渲染菜单
    getMoreMeau() {
      // 记录顶部按钮加和的width
      let meauItemAddWidth = 0
      //  记录菜单外部div width的最大值
      let meauMaxWidth = document.getElementsByClassName('sidebar-top-container')[0].offsetWidth
      //  记录单个菜单的宽度
      let meauItemWidth = 0
      // 记录菜单可渲染的最大的数组下标
      let meauMaxIndex = ''
      // 记录更多菜单下的路由
      let moreMeau = []
      // 循环菜单的width集合 记录菜单可渲染的最大的数组下标
      for (let i = 0; i < this.meauWidthArr.length; i++) {
        meauItemWidth = this.meauWidthArr[i]
        if (meauItemWidth) {
          // 菜单宽度加和
          meauItemAddWidth = this.$fun.accAdd(meauItemAddWidth, meauItemWidth)
          // 减去140 是为了给更多留位置 如果存在就跳出循环
          // 减去100 改为 减去140 -- 解决缩放情况下 【更多】 消失的问题 --- sun 2021-10-14
          if (meauItemAddWidth > this.$fun.accSub(meauMaxWidth, 140)) {
            // 记录菜单可渲染的最大的数组下标 减一是为了给更多留位置
            meauMaxIndex = i - 1
            break
          }
        }
      }
      // 如果存在可渲染的最大的数组下标 不存在则菜单栏宽度足够所有菜单展示
      if (meauMaxIndex) {
        let meauTopPermissionRouters = JSON.parse(
          JSON.stringify(this.meauTopPerRoutersInitialize)
        )
        // 更多菜单下的路由赋值
        meauTopPermissionRouters.forEach((item, index) => {
          if (index > meauMaxIndex) {
            moreMeau.push(item)
          }
        })
        // 构造更多菜单
        // 如果moreMeau 存在值
        if (moreMeau.length > 0) {
          // 截取更多之前的路由
          meauTopPermissionRouters = meauTopPermissionRouters.slice(0, meauMaxIndex + 1)
          // 添加更多按钮
          let moreMeauObj = {
            id: '202020',
            children: [],
            pId: '0',
            component: Layout,
            meta: { title: '更多', icon: 'iconfont icon-D-gengduo' },
            path: '/',
            Nochildren: false
          }
          for (let i = 0; i < moreMeau.length; i++) {
            // pid置为上边更多的id
            moreMeau[i].pId = moreMeauObj.id
            // 删除路径里边的 / ,因为上边更多已经配置过
            moreMeau[i].path = moreMeau[i].path.substr(1)
            // 本身作为一级菜单，置为二级后要改变页面地址为routerPage;
            moreMeau[i].component = resolve => (require([`@/views/routerPage/index.vue`], resolve))
            // 删除对应的icon属性
            delete moreMeau[i].meta.icon
            // 添加name属性 菜单key 值需要
            moreMeau[i].name = moreMeau[i].meta.title + moreMeau[i].id
          }
          moreMeauObj.children = moreMeau
          // 添加到菜单列表中
          meauTopPermissionRouters.push(moreMeauObj)
          this.meauTopPermissionRouters = meauTopPermissionRouters
        } else {
        }
      }
      //  如果不存在可渲染的最大的数组下标 则菜单可以完全展示
      else {
        // 页面初始化路由赋值给渲染路由的字段即可
        this.meauTopPermissionRouters = JSON.parse(
          JSON.stringify(this.meauTopPerRoutersInitialize)
        )
      }
    },
    // 菜单添加处理菜单流程待办个数
    getNumtoDoTasks() {
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
      this.AddMeauTopPerRoutersTasks()
    },
    AddMeauTopPerRoutersTasks() {
      let self = this
      this.meauNumtoDoTasks.forEach((item, index) => {
        // 如果存在count字段且数值有意义 再调用树形结构改变值处理函数
        if (item.count || item.count === 0) {
          // 传值含义: 数据 比对的是那个字段 查询比对的值  要添加的字段值  树层结构的children字段的key
          self.$fun.changeTreeOppositeValue(this.meauTopPerRoutersInitialize, 'vcactioncode', item.vcactioncode, item.count.toString(), 'children')
        }
      })
      // 调用值动态渲染菜单函数
      this.getMoreMeau()
    },
    menuSelect(index) {
      // 首页不显示侧边栏和标签栏
      //  console.log(index);
      let router_box = $('.hamburger-router-box')
      let body_left_meau = $('.body_left_meau')
      if (index === '/dashboard') {
        let timer = setTimeout(function() {
          router_box.hide()
          body_left_meau.hide()
          $('.main-container').addClass('main-container-dashboard')
          $('.app-main').addClass('app-main-dashboard')
          $('.fotter_box').addClass('hide-dashboard')
          // 显示首页所在的div
          $('.dashboard-box').removeClass('hide-dashboard')
          clearTimeout(timer)
        })
        this.$store.dispatch('delAllViews')
        return
      } else {
        router_box.show()
        body_left_meau.show()
        $('.main-container').removeClass('main-container-dashboard')
        $('.app-main').removeClass('app-main-dashboard')
        $('.fotter_box').removeClass('hide-dashboard')
        // 防止切换页面首页出现在新页面的框里
        $('.dashboard-box').addClass('hide-dashboard')
      }

      // 判断左侧侧边栏是否显示
      //  if (
      //    this.oneChildren.indexOf(index) === -1 &&
      //    this.$store.getters.sidebar.opened === false
      //  ) {

      //    this.$store.dispatch("toggleSideBar");
      //  } else if (
      //    this.oneChildren.indexOf(index) !== -1 &&
      //    this.$store.getters.sidebar.opened === true
      //  ) {

      //    this.$store.dispatch("toggleSideBar");
      //  }
      // 选中对应的子菜单
      // 由于顶部显示多级，需要排除根路径后边的路由
      let indexIncise = index.split('/')
      this.$store.commit('SET_MEAUTOP', '/' + indexIncise[1] || '')

    }
  }
}
</script>
<style lang="scss" rel="stylesheet/scss">
.sidebar-meau-top {
  width: calc(100% - 370px);
  height: 70px;
  position: absolute;
  top: 0px;
  left: 207px;
  overflow: hidden;

  .el-submenu__title {
    font-size: 15px !important;
  }

  .sidebar-meau-topItem {
    .el-menu.el-menu--horizontal {
      border: none;
    }

    .menu-wrapper {
      margin-left: 15px;
    }

    .el-menu--collapse {
      width: 100% !important;
    }

    .el-menu-item,
    .el-submenu__title {
      height: 36px;
      line-height: 36px;
      padding: 0 15px;

      div {
        height: 30px;
        line-height: 30px;
        text-align: center;
        color: rgba(255, 255, 255, 0.8);

        svg {
          font-size: 15px;
          vertical-align: middle;
          margin-right: 2px;
        }
      }

      div:hover {
        color: #fff;
      }

      span:nth-child(1) {
        display: inline-block;
        height: 30px;
        font-size: 16px;
        line-height: 32px;
        margin-right: 1px;
        // color: rgba(255,255,255,0.8);
      }

      span:nth-child(2) {
        height: 30px;
        line-height: 30px;
        font-size: 16px;
        text-align: center;
        // color: rgba(255,255,255,0.8);
      }

      i {
        display: none;
      }
    }
  }
}

.el-menu--horizontal > .el-menu.el-menu--popup {
  background-color: #fff !important;

  .el-menu-item {
    background-color: #fff !important;
    color: #3f3f3f !important;
    font-size: 15px;
    line-height: 36px;
  }

  .el-menu-item:hover {
    background-color: #f1f3f5 !important;
  }

  .el-menu-item > a > span {
    vertical-align: top;
  }
}

.sidebar-meau-top::-webkit-scrollbar {
  width: 6px;
  height: 6px;
  background-color: #f2f2f2;
  cursor: pointer;
}

.body_left_meau .el-submenu__title span {
  font-size: 14px;
}

.body_left_meau .el-menu-item span {
  font-size: 14px;
}

.body_left_meau .el-scrollbar__view {
  overflow-y: auto;
}

/*.body_left_meau .el-scrollbar__view .el-menu .el-submenu__icon-arrow{*/
/*right: 81px!important;*/
/*}*/

// @media screen and (max-width:1585px) {
//   .sidebar-meau-top .sidebar-meau-topItem .menu-wrapper {
//     margin-left: 10px;
//   }
//   .sidebar-meau-top .sidebar-meau-topItem .el-submenu__title{
//     padding: 0 10px;
//   }
// }
// @media screen and (max-width:1460px) {
//   .sidebar-meau-top .sidebar-meau-topItem .el-submenu__title div svg {
//     margin-right: 1px;
//   }
//   .sidebar-meau-top .sidebar-meau-topItem .el-menu-item{
//     // padding: 0 10px 0 20px;
//   }
//   .sidebar-meau-top .sidebar-meau-topItem .submenu-title-noDropdown div span {
//     font-size: 15px;
//   }
// }
// @media screen and (max-width:1410px) {

//   .sidebar-meau-top .sidebar-meau-topItem .el-submenu__title{
//     // padding: 0 6px;
//   }
// }
// @media screen and (max-width:1350px) {
//   .sidebar-meau-top .sidebar-meau-topItem .menu-wrapper {
//     margin-left: 5px;
//   }

// }
</style>

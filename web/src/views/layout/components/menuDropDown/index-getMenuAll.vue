<template>
  <!--顶部导航-->
  <div class="sidebar-meau-top-dropdown">
    <el-row id="navigation-box" justify="center" style="position: relative" type="flex">
      <div class="navigation-up">
        <div class="navigation-inner">
          <div class="navigation-v3">
            <ul id="aaa" style="margin-bottom: 0px; overflow: auto">
              <el-row style="display: -webkit-box">
                <li
                  v-for="(i, index) in menuList"
                  :key="index"
                  v-if="blackPageArray.indexOf(i.actionid) === -1"
                  v-bind="{ '_t_nav': !i.Nochildren ? 'menu_' + i.actionid : undefined }"
                >
                  <el-col>
                    <h2 style="position: relative">
                      <template v-if="i.Nochildren === true" >
                        <router-link :to="i.path" style="font-size: 16px; font-weight: 400;">
                          <span>{{ i.vcactionname }}</span>
                        </router-link>
                      </template>
                      <template v-else>
                        <a style="font-size: 16px; font-weight: 400">
                          <span>{{ i.vcactionname }}</span>
                        </a>
                      </template>
                    </h2>
                  </el-col>
                </li>
              </el-row>
            </ul>
          </div>
        </div>
      </div>
      <div class="navigation-down">
        <div
          v-for="i in menuList"
          v-if="blackPageArray.indexOf(i.actionid) === -1 && i.children && i.children.length > 0"
          :key="i.actionid"
          :id="'menu_' + i.actionid"
          :_t_nav="'menu_' + i.actionid"
          class="nav-down-menu"
          style="display: none; max-height: 700px; overflow: auto; box-shadow: rgb(0 0 0 / 12%) 0px 2px 4px 0px, rgb(0 0 0 / 4%) 0px 0px 6px 0px"
        >
          <template v-if="i.Nochildren !== true">
            <div class="dropdown-multi-column">
              <div
                v-for="item in i.children"
                :key="item.actionid"
                v-if="blackPageArray.indexOf(item.actionid) === -1"
                class="dropdown-column"
              >
                <div
                  class="dropdown-col-title"
                  :style="{ borderBottom: item.children && item.children.length > 0 ? '1px solid #e0e0e0' : 'none' }"
                >
                  <template v-if="item.children && item.children.length > 0">
                    {{ item.vcactionname }}
                  </template>
                  <template v-else>
                    <router-link :to="`${i.path}/${item.path}`" class="title-link" @click.native="closeDropdownMenu">
                      {{ item.vcactionname }}
                    </router-link>
                  </template>
                </div>
                <div v-if="item.children && item.children.length > 0" class="dropdown-col-items">
                  <div
                    v-for="(group, groupIndex) in chunk(
                      item.children.filter(y => blackPageArray.indexOf(y.actionid) === -1),
                      6
                    )"
                    :key="groupIndex"
                    class="dropdown-col-column"
                  >
                    <router-link
                      v-for="y in group"
                      :key="y.actionid"
                      :to="`${i.path}/${item.path}/${y.path}`"
                      class="dropdown-item"
                      @click.native="closeDropdownMenu"
                    >
                      {{ y.vcactionname }}
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </template>
        </div>
      </div>
    </el-row>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import $ from 'jquery'
export default {
  data() {
    return {
      blackPageArray: ['0', '50104', '404', '405', '205', '207', '406', '301', '503', '504', '505', '506', '60407', '1213' , '200201','7030101'],
      iconStrArr: {
        首页: require('@/assets/img/首页.png'),
        行业动态: require('@/assets/img/行业动态.png'),
        精选私募: require('@/assets/img/行业动态.png'),
        私募热点: require('@/assets/img/私募推荐.png'),
        投前管理: require('@/assets/img/投前管理.png'),
        投中管理: require('@/assets/img/投中管理.png'),
        投后管理: require('@/assets/img/投后管理.png'),
        组合管理: require('@/assets/img/投后管理.png'),
        绩效分析: require('@/assets/img/投后管理.png'),
        绩效报告: require('@/assets/img/投后管理.png'),
        数据维护: require('@/assets/img/投后管理.png'),
        需求互动: require('@/assets/img/需求互动.png'),
        系统管理: require('@/assets/img/系统管理.png')
      }
    }
  },
  computed: {
    ...mapGetters(['permission_routers', 'sidebar']),
    isCollapse() {
      return !this.sidebar.opened
    },
    menuList() {
      const meauList = this.$store.state.meauList
      for (let i = 0; i < meauList.length; i++) {
        meauList[i].icon = this.iconStrArr[meauList[i].vcactionname]
      }
      return meauList
    }
  },
  mounted() {
    this.meauTopPermissionRouters = JSON.parse(JSON.stringify(this.permission_routers))
    for (let i = 0; i < this.meauTopPermissionRouters.length; i++) {
      if (this.meauTopPermissionRouters[i].children && !this.meauTopPermissionRouters[i].hidden) {
      } else {
        this.meauTopPermissionRouters.splice(i, 1)
        i--
      }
    }
    this.test()
  },
  methods: {
    closeDropdownMenu() {
      $('.nav-down-menu').hide();
      $('[_t_nav]').removeClass('nav-up-selected');
    },
    chunk(arr, size) {
      const result = []
      const tempArr = JSON.parse(JSON.stringify(arr))
      while (tempArr.length) {
        result.push(tempArr.splice(0, size))
      }
      return result
    },
    test() {
      let self = this
      var qcloud = {}
      $('[_t_nav]').hover(
        function() {
          var _nav = $(this).attr('_t_nav')
          if (!$('#' + _nav).length) return
          clearTimeout(qcloud[_nav + '_timer'])
          qcloud[_nav + '_timer'] = setTimeout(function() {
            $('[_t_nav]').each(function() {
              $(this)[_nav == $(this).attr('_t_nav') ? 'addClass' : 'removeClass']('nav-up-selected')
            })
            $('#' + _nav)
              .stop(true, true)
              .slideDown(200)
          }, 150)
        },
        function() {
          var _nav = $(this).attr('_t_nav')
          if (!$('#' + _nav).length) return
          clearTimeout(qcloud[_nav + '_timer'])
          qcloud[_nav + '_timer'] = setTimeout(function() {
            $('[_t_nav]').removeClass('nav-up-selected')
            $('#' + _nav)
              .stop(true, true)
              .hide()
          }, 150)
        }
      )
    }
  }
}
</script>

<style lang="scss" rel="stylesheet/scss">
.navigation-up .navigation-v3 li h2 a {
  position: relative;
  display: inline-block;
  padding-bottom: 5px; /* 为下划线留出空间 */
}

.navigation-up .navigation-v3 li h2 a:hover::after {
  content: '';
  position: absolute;
  left: 10%;
  bottom: 0;
  width: 80%;
  height: 2px;
  background-color: #f5d7bc;
}

.sidebar-meau-top-dropdown {
  z-index: 999;
  width: calc(100% - 370px);
  height: 60px;
  position: absolute;
  top: 0px;
  left: 160px;

  .left_click,
  .right_click {
    display: inline-block;
    color: #fff;
    cursor: pointer;
  }

  #aaa::-webkit-scrollbar {
    display: none;
  }

  li {
    list-style: none !important;
  }

  a:link,
  a:visited {
    text-decoration: none;
  }

  .head-v3 {
    position: relative;
    z-index: 100;
    min-width: 500px;
    background: #000000;
    height: 60px;
  }

  .head-v3 .navigation-inner {
    margin: 0 auto;
    width: 100%;
    position: relative;
  }

  .navigation-up {
    margin-bottom: 5px;
    height: 50px;
  }

  .navigation-up .navigation-v3 {
    float: left;
    _margin-left: 10px;
  }

  .navigation-up .navigation-v3 ul {
    float: left;
    margin-bottom:0px;
  }

  .navigation-up .navigation-v3 li {
    float: left;
    font: normal 16px/59px 'microsoft yahei';
    color: white;
  }

  .navigation-up .navigation-v3 .nav-up-selected-inpage {
    background: #202833;
  }

  .navigation-up .navigation-v3 li h2 {
    font-weight: normal;
    padding: 0;
    margin: 0;
    font-size: 14px;
    line-height: 45px;
  }

  .navigation-up .navigation-v3 li h2 {
    color: #fff;
    display: inline-block;
    font-family: 'microsoft yahei';
    position: relative;

    a {
      padding: 0 10px;
    }

    .icon-menu {
      color: #242836;
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      right: 4px;
    }
  }
  .navigation-up .navigation-v3 li h2:hover {
    color: #e9c39e;
    .icon-menu {
      color: #e9c39e;
    }
    // a {
    //   border-bottom: 1px solid #e9c39e;
    // }
  }
  .navigation-down {
    position: fixed !important;
    top: 60px;
    left: 0 !important;
    right: 0 !important;
    width: 100vw !important;
    z-index: 10000;
    box-sizing: border-box;
    display: flex;
    justify-content: center;
    padding: 0;
  }

  .navigation-down .nav-down-menu {
    width: 100% !important;
    margin: 0;
    background-color: #fff;
    position: relative;
    padding: 20px 40px;
    box-sizing: border-box;
    overflow-y: auto;
    overflow-x: visible;
    justify-items: center;
  }

  .dropdown-multi-column {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, max-content));
    gap: 40px;
    max-width: 100%;
    box-sizing: border-box;
  }

  .dropdown-column {
    width: auto;
    box-sizing: border-box;
    overflow-x: visible;
    position: relative;
  }

  .dropdown-col-title {
    font: normal 16px 'microsoft yahei';
    font-weight: 500;
    color: #a15008;
    padding-bottom: 10px;
    margin-bottom: 10px;
  }

  .dropdown-col-items {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    align-items: flex-start;
    gap: 20px;
    box-sizing: border-box;
    width: auto;
  }

  .dropdown-col-column {
    display: flex;
    flex-direction: column;
    gap: 8px;
    width: auto;
    min-width: 180px;
    box-sizing: border-box;
  }

  .dropdown-item {
    color: #20212b;
    font: normal 14px/28px 'microsoft yahei';
    padding: 2px 0;
    transition: color 0.2s;
    white-space: nowrap;
    box-sizing: border-box;
  }

  .title-link {
    color: #a15008;
    text-decoration: none;
    display: block;
  }

  .dropdown-item:hover,
  .title-link:hover {
    color: #cf7e34 !important;
  }

  .router_link:hover {
    color: #cf7e34;
  }

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
        color: #20212b;
        svg {
          font-size: 15px;
          vertical-align: middle;
          margin-right: 2px;
        }
      }

      div:hover {
        color: #20212b;
      }

      span:nth-child(1) {
        display: inline-block;
        height: 30px;
        font-size: 16px;
        line-height: 32px;
        margin-right: 1px;
        color: #20212b;
      }

      span:nth-child(2) {
        height: 30px;
        line-height: 30px;
        font-size: 16px;
        text-align: center;
        color: #20212b;
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
    color: #20212b !important;
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
</style>

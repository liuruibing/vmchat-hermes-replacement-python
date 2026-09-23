<template>
  <div class="quick-nav-container">
    <div class="quick-nav-display">
      <el-row class="card-header" type="flex" justify="space-around" style="padding-bottom: 7px;border-bottom: 1px solid #EBEEF5;margin-bottom: 10px !important;">
        <el-col :span="4">
          <span class="title-name">
             <img src="../dynamicCondition/assets/img/GF.png" style="height:18px;width:18px" />
            <span>快捷导航</span>
          </span>
          <span class="link-more" @click.stop="openSettingDialog">设置</span>
        </el-col>
        <el-col :span="20" style="text-align: left">

        </el-col>
      </el-row>

      <div class="quick-nav-scroll">
        <div
          class="quick-nav-item"
          v-for="(item, index) in quickNavList"
          :key="item.actionid"
          @click="navigateTo(item)"
          :style="{
              backgroundImage: `url(${getBgImage(index)})`,
              backgroundSize: 'cover',
              backgroundPosition: 'center'
            }"
        >
<!--          <el-tooltip :content="item.firstMenuName" placement="top" effect="dark">
            <div class="first-menu-name">{{ item.firstMenuName }}</div>
          </el-tooltip>-->

          <img :src="getIcon(item.actionid)" alt="" class="item-img">

          <el-tooltip :content="item.vcactionname" placement="bottom" effect="dark">
            <div class="menu-name">{{ item.vcactionname }}</div>
          </el-tooltip>
        </div>
        <div class="empty-tip" v-if="quickNavList.length === 0">暂无快捷导航，点击左上角设置添加</div>
      </div>
    </div>

    <el-dialog
      title="快捷导航设置"
      :visible.sync="settingDialogVisible"
      width="800px"
      @close="resetCheckStatus"
    >
      <div class="menu-tree-container">
        <div
          class="menu-level-1"
          v-for="firstMenu in getMenuList()"
          :key="firstMenu.actionid"
          v-if="blackPageArray.indexOf(firstMenu.actionid) === -1"
        >
          <div class="menu-title">{{ firstMenu.vcactionname }}</div>

          <div
            class="menu-level-2"
            v-for="secondMenu in firstMenu.children || []"
            :key="secondMenu.actionid"
            v-if="blackPageArray.indexOf(secondMenu.actionid) === -1"
          >
            <div v-if="!secondMenu.children || secondMenu.children.length === 0">
              <el-checkbox
                v-model="checkedMenuIds"
                :label="secondMenu.actionid"
                @change="handleCheckChange"
                class="level-2-checkbox"
              >
                {{ secondMenu.vcactionname }}
              </el-checkbox>
            </div>
            <div v-else>
              <div class="menu-title">{{ secondMenu.vcactionname }}</div>
              <div
                class="menu-level-3"
                v-for="thirdMenu in secondMenu.children"
                :key="thirdMenu.actionid"
                v-if="blackPageArray.indexOf(thirdMenu.actionid) === -1"
              >
                <el-checkbox
                  v-model="checkedMenuIds"
                  :label="thirdMenu.actionid"
                  @change="handleCheckChange"
                >
                  {{ thirdMenu.vcactionname }}
                </el-checkbox>
              </div>
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="settingDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveQuickNav">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
// 引入封装的请求方法
import { getQuickNavList, saveQuickNav } from './scripts/quickNav.js'

export default {
  data() {
    return {
      settingDialogVisible: false,
      quickNavList: [],
      checkedMenuIds: [],
      blackPageArray: ['0', '1','50104', '404', '405','406', '205', '207', '301', '503', '504', '505', '506', '60407', '1213' , '200201','7030101'],
      iconStrArr: {
        '40101': require('./img/私募产品筛选.png'),
        '600201': require('./img/估值指标.png'),
        '600203': require('./img/估值指标.png'),
        '600206': require('./img/估值指标.png'),
        '50101': require('./img/准入审批.png'),
        '50102': require('./img/准入审批.png'),
        '50103': require('./img/准入审批.png'),
        '201': require('./img/市场指数.png'),
        '206': require('./img/市场指数.png'),
        '208': require('./img/市场指数.png'),
        '1200301': require('./img/报告工坊.png'),
        '1201': require('./img/报告类.png'),
        '1202': require('./img/报告类.png'),
        '1203': require('./img/报告类.png'),
        '1206': require('./img/报告类.png'),
        '1207': require('./img/报告类.png'),
        '1208': require('./img/报告类.png'),
        '1209': require('./img/报告类.png'),
        '1210': require('./img/报告类.png'),
        '1213': require('./img/报告类.png'),
        '1243': require('./img/报告类.png'),
        '1245': require('./img/报告类.png'),
        '1214': require('./img/报告类.png'),
        '1250': require('./img/报告类.png'),
        '1251': require('./img/报告类.png'),
        '660501': require('./img/报告类.png'),
        '默认图标': require('./img/产品信息维护.png')
      },
      _cachedMenuList: null
    }
  },
  watch: {
    '$store.state.meauList': {
      handler() {
        this._cachedMenuList = null
      },
      deep: true
    }
  },
  computed: {
    ...mapGetters(['sidebar']),
   /*  menuList() {
      var meauList = this.$store.state.meauList || []
      var handleMenu = function(menuList, parentPath, firstMenuName) {
        parentPath = parentPath || ''
        firstMenuName = firstMenuName || ''
        return menuList.map(function(menu) {
          // 前端本地处理图标
          menu.icon = this.getIcon(menu.actionid)
          menu.fullPath = parentPath ? (parentPath + '/' + menu.path) : menu.path
          menu.firstMenuName = firstMenuName || menu.vcactionname
          menu.isLastLevel = !menu.children || menu.children.length === 0
          if (menu.children && menu.children.length > 0) {
            menu.children = handleMenu.call(
              this,
              menu.children,
              menu.fullPath,
              firstMenuName || menu.vcactionname
            )
          }
          return menu
        }.bind(this))
      }.bind(this)
      return handleMenu(meauList)
    } */
  },
  mounted() {
    this.loadQuickNav()
  },
  methods: {
    getMenuList() {
      if (this._cachedMenuList) {
        return this._cachedMenuList
      }
      var meauList = this.$store.state.meauList || []
      var handleMenu = function(menuList, parentPath, firstMenuName) {
        parentPath = parentPath || ''
        firstMenuName = firstMenuName || ''
        return menuList.map(function(menu) {
          var menuCopy = {}
          for (var key in menu) {
            if (menu.hasOwnProperty(key)) {
              menuCopy[key] = menu[key]
            }
          }
          menuCopy.icon = this.getIcon(menuCopy.actionid)
          menuCopy.fullPath = parentPath ? (parentPath + '/' + menuCopy.path) : menuCopy.path
          menuCopy.firstMenuName = firstMenuName || menuCopy.vcactionname
          menuCopy.isLastLevel = !menuCopy.children || menuCopy.children.length === 0
          if (menuCopy.children && menuCopy.children.length > 0) {
            menuCopy.children = handleMenu.call(
              this,
              menuCopy.children,
              menuCopy.fullPath,
              firstMenuName || menuCopy.vcactionname
            )
          }
          return menuCopy
        }.bind(this))
      }.bind(this)
      this._cachedMenuList = handleMenu(meauList)
      return this._cachedMenuList
    },
    getBgImage(index) {
      const bgImages = [
        require('./img/背景-1.png'),
        require('./img/背景-2.png'),
        require('./img/背景-3.png')
      ];
      return bgImages[index % bgImages.length];
    },
    getIcon(actionid) {
      return this.iconStrArr[actionid] || this.iconStrArr['默认图标']
    },
    loadQuickNav() {
      getQuickNavList()
        .then(function(response) {
          if (response && response.data) {
            this.quickNavList = response.data.data || []
            this.checkedMenuIds = this.quickNavList.map(function(item) {
              return item.actionid
            })
          } else {
            this.$message.error('加载快捷导航失败：' + (response.data.message || '未知错误'))
          }
        }.bind(this))
        .catch(function(error) {
          this.$message.error('加载快捷导航失败')
          console.error('加载快捷导航报错：', error)
        }.bind(this))
    },
    openSettingDialog() {
      this.settingDialogVisible = true
      /* this.checkedMenuIds = this.quickNavList.map(function(item) {
        return item.actionid
      }) */
      const newIds = this.quickNavList.map(function(item) {
        return item.actionid
      })
      if (JSON.stringify(this.checkedMenuIds) !== JSON.stringify(newIds)) {
        this.checkedMenuIds = [].concat(newIds)
      }
    },
    resetCheckStatus() {
      /* this.checkedMenuIds = this.quickNavList.map(function(item) {
        return item.actionid
      }) */
      const newIds = this.quickNavList.map(function(item) {
        return item.actionid
      })
      if (JSON.stringify(this.checkedMenuIds) !== JSON.stringify(newIds)) {
        this.checkedMenuIds = [].concat(newIds)
      }
    },
    handleCheckChange() {},
    saveQuickNav() {
      try {
        var collectLastLevelMenus = function(menuList) {
          var lastLevelMenus = []
          if (Array.isArray(menuList)) {
            menuList.forEach(function(menu) {
              if (menu && menu.isLastLevel) {
                lastLevelMenus.push(menu)
              } else if (menu && menu.children && menu.children.length > 0) {
                lastLevelMenus = lastLevelMenus.concat(collectLastLevelMenus(menu.children))
              }
            })
          }
          return lastLevelMenus
        }

        var allLastLevelMenus = collectLastLevelMenus(this.getMenuList())
        var selectedMenus = allLastLevelMenus.filter(function(menu) {
          return this.checkedMenuIds.indexOf(menu.actionid) !== -1 &&
            this.blackPageArray.indexOf(menu.actionid) === -1
        }.bind(this))

        var requestData = {
          quickNavList: selectedMenus.map(function(item) {
            return {
              actionid: item.actionid,
              vcactionname: item.vcactionname,
              firstMenuName: item.firstMenuName,
              fullPath: item.fullPath
            }
          })
        }

        saveQuickNav(requestData)
          .then(function(response) {
            if (response && response.data) {
              this.quickNavList = selectedMenus
              this.settingDialogVisible = false
              this.$message.success('快捷导航保存成功')
            } else {
              this.$message.error('保存快捷导航失败：' + (response.data.message || '未知错误'))
            }
          }.bind(this))
          .catch(function(error) {
            this.$message.error('保存快捷导航失败')
            console.error('保存快捷导航报错：', error)
          }.bind(this))
      } catch (error) {
        this.$message.error('保存快捷导航失败')
        console.error('保存快捷导航报错：', error)
      }
    },
    navigateTo(menu) {
      const pushResult = this.$router.push(menu.fullPath);
      if (pushResult && typeof pushResult.catch === 'function') {
        pushResult.catch(function(err) {
          console.error('路由跳转失败：', err)
          this.$message.warning('该菜单路由未配置')
        }.bind(this))
      }
    }
  }
}
</script>

<style lang="scss" scoped>
@import url('../../style/index.scss');
.quick-nav-container {
  background-color: #fff;
  width: 100%;
  height: 160px;
  border: 1px solid #e6e6e6;
  border-radius: 4px;
  box-sizing: border-box;

  .quick-nav-display {
    width: 100%;
    height: 100%;
    padding: 10px;
    box-sizing: border-box;

    .quick-nav-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;

      .title-name {
        font-size: 16px;
        font-weight: 500;
        color: #333;
      }
    }

    .quick-nav-scroll {
      width: 100%;
      height: calc(100% - 36px);
      display: flex;
      align-items: flex-start;
      overflow-x: auto;
      overflow-y: hidden;
      padding-bottom: 5px;

      &::-webkit-scrollbar {
        height: 6px;
      }

      &::-webkit-scrollbar-thumb {
        background-color: #ddd;
        border-radius: 3px;
      }

      .quick-nav-item {
        width: 160px;
        min-width: 160px;
        height: 100%;
        margin-right: 15px;
        //border: 1px solid #e6e6e6;
        border-radius: 4px;
        padding: 10px;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s;
       // background: #fafafa;

        &:hover {
          box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
         // background: #fff;
          background-color: rgba(255,255,255,0.9);
        }

        .first-menu-name {
          align-self: flex-start;
          font-size: 12px;
          color: #999;
          margin-bottom: 10px;
          width: 100%;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          line-height: 1.2;
        }

        .item-img {
          width: 40px;
          height: 40px;
          object-fit: contain;
          margin-bottom: 7px;
          flex-shrink: 0;
        }

        .menu-name {
          font-size: 14px;
          color: #333;
          text-align: center;
          width: 100%;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          line-height: 1.2;
        }
      }

      .empty-tip {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #999;
        font-size: 14px;
      }
    }
  }
}

.menu-tree-container {
  max-height: 500px;
  overflow-y: auto;
  padding: 10px;

  .menu-level-1 {
    margin-bottom: 20px;

    .menu-title {
      font-size: 16px;
      font-weight: 500;
      color: #333;
      margin-bottom: 10px;
      padding-left: 5px;
      border-left: 3px solid #A15008;
    }

    .menu-level-2 {
      margin-left: 20px;
      margin-bottom: 15px;

      .level-2-checkbox {
        font-size: 14px;
        color: #666;
        margin: 5px 0;
        display: block;
      }

      .menu-title {
        font-size: 14px;
        font-weight: 500;
        color: #666;
        margin-bottom: 8px;
        border-left-color: #fff;
      }

      .menu-level-3 {
        margin-left: 20px;
        margin-bottom: 5px;

        .el-checkbox {
          font-size: 14px;
          color: #999;
        }
      }
    }
  }
}
</style>

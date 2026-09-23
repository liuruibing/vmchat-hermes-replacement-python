<template>
  <div class="menu-search-container" ref="searchContainer">
    <el-input
      v-model="searchKeyword"
      size="small"
      placeholder="请输入菜单名称搜索"
      class="menu-search-input"
      @input="handleSearch"
      @focus="handleInputFocus"
      @blur="handleInputBlur"
      prefix-icon="el-icon-search"
    ></el-input>

    <div class="menu-search-dropdown" v-show="isDropdownShow && searchResultList.length > 0">
      <ul class="dropdown-list">
        <li
          v-for="(item, index) in searchResultList"
          :key="index"
          class="dropdown-item"
          @click="handleMenuItemClick(item)"
        >
          {{ item.menuName }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MenuSearch',
  data() {
    return {
      // 搜索关键词
      searchKeyword: '',
      // 扁平化后的完整菜单列表
      flatMenuList: [],
      // 搜索结果列表
      searchResultList: [],
      // 是否显示下拉框
      isDropdownShow: false,
      // 模糊匹配延迟定时器
      searchTimer: null
    }
  },
  computed: {
    // 从Vuex获取菜单列表
    meauList() {
      var storeState = this.$store && this.$store.state
      var menuList = storeState && storeState.meauList ? storeState.meauList : []
      // 确保返回数组
      return Array.isArray(menuList) ? menuList : []
    }
  },
  mounted() {
    this.flattenMenuList()
  },
  beforeDestroy() {
    // 清除定时器，避免内存泄漏
    if (this.searchTimer) {
      clearTimeout(this.searchTimer)
    }
  },
  methods: {
    flattenMenuList() {
      var self = this
      var flatList = []
      var originMenuList = this.meauList
      var blackPageArray = ['0', '50104', '404', '405', '205', '207', '406', '301', '503', '504', '505', '506', '60407', '1213' , '200201','7030101']

      // 一级菜单
      if (Array.isArray(originMenuList)) {
        for (var i = 0; i < originMenuList.length; i++) {
          var firstLevel = originMenuList[i]
          // 跳过黑名单菜单、非有效对象
          if (!firstLevel || blackPageArray.indexOf(firstLevel.actionid) !== -1) {
            continue
          }

          // 一级菜单无子节点
          if (firstLevel.Nochildren === true) {
            flatList.push({
              menuName: firstLevel.vcactionname || '',
              menuPath: firstLevel.path || ''
            })
            continue
          }

          // 一级菜单有子节点，遍历二级菜单
          var secondLevelList = firstLevel.children
          if (Array.isArray(secondLevelList)) {
            for (var j = 0; j < secondLevelList.length; j++) {
              var secondLevel = secondLevelList[j]
              // 跳过黑名单菜单、非有效对象
              if (!secondLevel || blackPageArray.indexOf(secondLevel.actionid) !== -1) {
                continue
              }

              // 二级菜单无子节点
              var thirdLevelList = secondLevel.children
              if (!Array.isArray(thirdLevelList) || thirdLevelList.length === 0) {
                flatList.push({
                  menuName: secondLevel.vcactionname || '',
                  menuPath: (firstLevel.path || '') + '/' + (secondLevel.path || '')
                })
                continue
              }

              // 二级菜单有子节点，遍历三级菜单
              for (var k = 0; k < thirdLevelList.length; k++) {
                var thirdLevel = thirdLevelList[k]
                // 跳过黑名单菜单、非有效对象
                if (!thirdLevel || blackPageArray.indexOf(thirdLevel.actionid) !== -1) {
                  continue
                }

                flatList.push({
                  menuName: thirdLevel.vcactionname || '',
                  menuPath: (firstLevel.path || '') + '/' + (secondLevel.path || '') + '/' + (thirdLevel.path || '')
                })
              }
            }
          }
        }
      }

      // 赋值给扁平化菜单列表
      self.flatMenuList = self.uniqueMenuList(flatList)
    },

    /**
     * 菜单列表去重
     */
    uniqueMenuList(menuList) {
      var result = []
      var pathMap = {}
      if (Array.isArray(menuList)) {
        for (var i = 0; i < menuList.length; i++) {
          var item = menuList[i]
          var menuPath = item.menuPath
          if (menuPath && !pathMap[menuPath]) {
            pathMap[menuPath] = true
            result.push(item)
          }
        }
      }
      return result
    },

    /**
     * 处理搜索逻辑
     */
    handleSearch() {
      var self = this
      // 清除旧定时器，避免频繁触发
      if (self.searchTimer) {
        clearTimeout(self.searchTimer)
      }

      // 延迟搜索，优化输入体验
      self.searchTimer = setTimeout(function() {
        var keyword = self.searchKeyword && self.searchKeyword.trim() || ''
        var result = []

        if (keyword) {
          // 模糊匹配
          for (var i = 0; i < self.flatMenuList.length; i++) {
            var item = self.flatMenuList[i]
            var menuName = item.menuName || ''
            if (menuName.toLowerCase().indexOf(keyword.toLowerCase()) !== -1) {
              result.push(item)
            }
          }
        }

        // 更新搜索结果，显示下拉框
        self.searchResultList = result
        self.isDropdownShow = result.length > 0
      }, 300)
    },

    handleInputFocus() {
      if (this.searchKeyword && this.searchKeyword.trim() && this.searchResultList.length > 0) {
        this.isDropdownShow = true
      }
    },

    handleInputBlur() {
      var self = this
      setTimeout(function() {
        self.isDropdownShow = false
      }, 200)
    },

    handleMenuItemClick(menuItem) {
      if (!menuItem) {
        return
      }
      var menuPath = menuItem.menuPath || ''
      if (menuPath) {
        // 跳转页面
        this.$router.push({ path: menuPath })
        // 清空搜索状态
        this.searchKeyword = ''
        this.searchResultList = []
        this.isDropdownShow = false
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.menu-search-container {
  position: relative;
  margin: 0 10px;
  top: 0px;
  width: 250px;
  z-index: 1000;

  // 搜索输入框样式
  .menu-search-input {
    ::v-deep .el-input__inner {
      height: 26px;
      line-height: 26px;
      border-radius: 4px;
      width: 250px;
      //padding: 0 35px 0 15px;
      border: 1px solid #e4e7ed;
      background: rgba(255, 255, 255, 0.9);
      color: #303133;
      font-size: 14px;

      &:focus {
        border-color: #f5d7bc;
        box-shadow: 0 0 0 2px rgba(245, 215, 188, 0.2);
      }
    }

    ::v-deep .el-input__prefix {
      color: #c0c4cc;
      font-size: 16px;
    }
  }

  // 下拉结果框样式
  .menu-search-dropdown {
    position: absolute;
    top: 30px;
    left: 0;
    right: 0;
    max-height: 400px;
    overflow-y: auto;
    background: #ffffff;
    border-radius: 4px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    border: 1px solid #e4e7ed;
    z-index: 9999;

    .dropdown-list {
      margin: 0;
      padding: 0px 0;
      list-style: none;

      .dropdown-item {
        line-height: 30px;
        padding: 0px 10px;
        font-size: 14px;
        color: #303133;
        cursor: pointer;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;

        &:hover {
          background: #f9f0e6;
          color: #cf7e34;
        }
      }
    }
  }

  // 下拉框滚动条样式
  ::v-deep .menu-search-dropdown::-webkit-scrollbar {
    width: 6px;
  }

  ::v-deep .menu-search-dropdown::-webkit-scrollbar-track {
    background: #f5f5f5;
    border-radius: 3px;
  }

  ::v-deep .menu-search-dropdown::-webkit-scrollbar-thumb {
    background: #dcdfe6;
    border-radius: 3px;
  }

  ::v-deep .menu-search-dropdown::-webkit-scrollbar-thumb:hover {
    background: #c0c4cc;
  }
}
</style>

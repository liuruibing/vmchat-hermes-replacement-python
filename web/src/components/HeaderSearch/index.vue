<template>
    <!-- <svg-icon class="search-icon" icon-class="search" @click.native="click" /> -->
  <!-- <div class="header-search" :class="{'show':show}">
    <i class="el-icon-search search-icon" @click.stop="click"></i>
    <el-select
      ref="headerSearchSelect"
      v-model="search"
      :remote-method="querySearch"
      filterable
      default-first-option
      remote
      placeholder="Search"
      @change="change"
      class="header-search-select"
    >
      <el-option 
        v-for="item in options" 
        :key="item.item.path" 
        :value="item.item" 
        :label="item.item.title.join('>')" />
    </el-select>
  </div> -->
  <div>
    <el-select
      ref="headerSearchSelect"
      v-model="search"
      :remote-method="querySearch"
      filterable
      default-first-option
      remote
      placeholder="请输入菜单名称"
      @change="change"
      class="header-search-select"
    >
      <el-option 
        v-for="item in options" 
        :key="item.item.path" 
        :value="item.item" 
        :label="item.item.title.join('>')" />
    </el-select>
  </div>
</template>

<script>
// fuse is a lightweight fuzzy-search module
// make search results more in line with expectations
import Fuse from 'fuse.js'
import path from 'path'
import { getCookiesData, setCookiesData } from '@/utils/auth'
export default {
  name: 'HeaderSearch',
  data() {
    return {
      aaa:"",
      search: '',
      options: [],
      searchPool: [],
      show: false,
      fuse: undefined,
      historyList:[]
    }
  },
  computed: {
    routes() {
      return this.$store.getters.permission_routers
    }
  },
  watch: {
    routes() {
      this.searchPool = this.generateRoutes(this.routes)
    },
    searchPool(list) {
      this.initFuse(list)
    },
    show(value) {
      if (value) {
        document.body.addEventListener('click', this.close)
      } else {
        document.body.removeEventListener('click', this.close)
      }
    }
  },
  mounted() {
    this.searchPool = this.generateRoutes(this.routes);
    // console.log(this.$store.getters.permission_routers);
  },
  methods: {
    click() {
      return
      this.show = !this.show
      if (this.show) {
        this.$refs.headerSearchSelect && this.$refs.headerSearchSelect.focus()
      }
    },
    close() {
      this.$refs.headerSearchSelect && this.$refs.headerSearchSelect.blur()
      this.options = []
      this.show = false
    },
    change(val) {
      // console.log(val);
      this.historyList.unshift(val);
      if(this.historyList.length>5){
        this.historyList = this.historyList.slice(0,5)
      }
      // console.log(this.historyList);
      let obj = JSON.parse(getCookiesData("BAIDUID") || '{}');
      obj.historyList = this.historyList;
      setCookiesData('BAIDUID', JSON.stringify(obj))
      this.$emit('history',this.historyList)
      this.$router.push(val.path)
      this.search = ''
      this.options = []
      this.$nextTick(() => {
        this.show = false
      })
    },
    initFuse(list) {
      this.fuse = new Fuse(list, {
        shouldSort: true,
        threshold: 0.4,
        location: 0,
        distance: 100,
        maxPatternLength: 32,
        minMatchCharLength: 1,
        // keys: [{
        //   name: 'title',
        //   weight: 0.7
        // }, {
        //   name: 'path',
        //   weight: 0.3
        // }]
        keys:['title']
      })
    },
    // Filter out the routes that can be displayed in the sidebar
    // And generate the internationalized title
    generateRoutes(routes, basePath = '/', prefixTitle = []) {
      let res = []
      for (const router of routes) {
        // skip hidden router
        if (router.hidden) { continue }
        const data = {
          path: path.resolve(basePath, router.path),
          title: [...prefixTitle]
        }
        if (router.meta && router.meta.title) {
          data.title = [...data.title, router.meta.title]
          if (router.redirect !== 'noRedirect') {
            // only push the routes with title
            // special case: need to exclude parent router without redirect
            res.push(data)
          }
        }
        // recursive child routes
        if (router.children) {
          const tempRoutes = this.generateRoutes(router.children, data.path, data.title)
          // console.log('tempRoutes',tempRoutes);
          if (tempRoutes.length >= 1) {
            res = [...res, ...tempRoutes]
          }
        }
      }
      return res
    },
    querySearch(query) {
      if (query !== '') {
        // query+' '
        let querys = ''
        if(query.length>1){
          querys = query+' '
        }else{
          querys = query+''
        }
        let options = this.fuse.search(querys)
        let arr = [];
        options.forEach(item=>{
          if(item.item.title.length>1){
            arr.push(item)
          }
        })
        this.options = arr;
      } else {
        this.options = []
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.header-search {
  font-size: 0 !important;
  .search-icon {
    cursor: pointer;
    font-size: 18px;
    vertical-align: middle;
  }
  .header-search-select {
    font-size: 18px;
    transition: width 0.2s;
    width: 0;
    overflow: hidden;
    background: transparent;
    border-radius: 0;
    display: inline-block;
    vertical-align: middle;
    ::v-deep .el-input__inner {
      border-radius: 0;
      border: 0;
      padding-left: 0;
      padding-right: 0;
      box-shadow: none !important;
      border-bottom: 1px solid #d9d9d9;
      vertical-align: middle;
    }
  }
  &.show {
    .header-search-select {
      width: 210px;
      margin-left: 10px;
    }
  }
}
</style>
<template>
  <div class="home nest-none-padding" v-loading="loading">
    <template-management
      ref="templateManagement"
      v-show="!isShow"
      @changeshow="changeshow"
      @handleShowTemplate="handleShowTemplate"
      @handleShowTemplateFromNewForEditor="handleShowTemplateFromNewForEditor"
      @handleShowTemplateNew="handleShowTemplateFromNew"
      @handleShowTemplateNewSystem="handleShowTemplateFromNewSystem"
    ></template-management>
    <workshop-report
      ref="workshopReport"
      v-show="isShow"
      :current-template="currentTemplate"
      :globalSettingConfig="globalSettingConfig"
      :is-edit="isEdit"
      @changeshow="handleTemplateReportShow"
    ></workshop-report>
  </div>
</template>

<script>
import workshopReport from '@/views/workshopReport/index'
import templateManagement from '@/views/templateManagement'
import pageApi from '@/api/templateManageMent/index'
import request from '@/utils/request'
export default {
  components: {
    workshopReport,
    templateManagement
  },
  data() {
    return {
      isShow: false,
      isEdit: false, // 判断是不是编辑状态
      currentTemplate: null,
      globalSettingConfig: null, // 存储通用属性的字段
      loading: false,
      datumOption: [], // 固定基准
      datumCompareOption: [] //对比基准
    }
  },
  async created() {
    await this.getFixedOptions()
    await this.getContrasOptions()
    this.$bus.$on('homeload', this.handleHomdLoading)
  },
  mounted() {},
  methods: {
    handleTemplateReportShow() {
      this.isShow = false
      this.$refs.templateManagement.handleSearch()
    },

    handleHomdLoading(val) {
      this.loading = val
    },

    /**
     * @description 获取固定基准基准下拉
     */
    getFixedOptions() {
      return new Promise((resolve, reject) => {
        request({
          url: `/api/report/v1.0/data/sql/f8962b66-1494-43b0-aa41-bc294e6659ca`,
          method: 'post',
          data: {
            indexCode: 'f8962b66-1494-43b0-aa41-bc294e6659ca'
          }
        })
          .then((res) => {
            if (res.data.status === 0) {
              const resultDim = res.data.data || []
              this.datumOption = resultDim.map((item) => {
                return {
                  label: item.VC_BE_NAME,
                  id: item.VC_BE_CODE
                }
              })
            }
            this.$store.dispatch('setIndexArrayValue', this.datumOption)
            resolve()
          })
          .catch((err) => {
            this.$store.dispatch('setIndexArrayValue', this.datumOption)
            resolve()
          })
      })
    },

    /**
     * @description 获取对比基准下拉
     */
    getContrasOptions() {
      return new Promise((resolve, reject) => {
        request({
          url: `/api/report/v1.0/data/sql/ecd8867c-64cc-4ebc-9070-04524b04b72c`,
          method: 'post',
          data: {
            indexCode: 'ecd8867c-64cc-4ebc-9070-04524b04b72c'
          }
        })
          .then((res) => {
            if (res.data.status === 0) {
              const resultDim = res.data.data || []
              this.datumCompareOption = resultDim.map((item) => {
                return {
                  label: item.DIM_NME,
                  id: item.DIM_CDE
                }
              })
            }
            this.$store.dispatch('setCompareIndexArrayValue', this.datumCompareOption)
            resolve()
          })
          .catch((err) => {
            this.$store.dispatch('setCompareIndexArrayValue', this.datumCompareOption)
            resolve()
          })
      })
    },

    changeshow(arr) {
      this.isShow = true
      this.$store.commit('setComponentData', [])
      setTimeout(() => {
        // 把这一行的 内容 需要 复制到 全局的画图component对象上面去
        for (let i = 0; i < arr.length; i++) {
          this.$store.dispatch('addComponentAsync', { component: arr[i] })
          // this.$store.commit('addComponent', {component: arr[i]})
        }
      }, 300)
    },
    /**
     * @description 查看另存模板
     */
    handleShowTemplate(row) {
      this.globalSettingConfig = {}
      this.isShow = true
      const params = {}
      params.reportId = row.reportId
      this.$store.commit('SET_IS_EDITOR', true)
      this.loading = true
      let elementCfg = JSON.parse(row.elementCfg)

      pageApi.getTemplateComponent(params).then((res) => {
        if (res.data.status === 200) {
          const componentInfo = res.data.data || {}
          const moduleCfg = JSON.parse(componentInfo.moduleCfg)
          // 合并新增时选择产品基本信息入当前行数据
          const { ZB_BEGINDATE, ZB_ENDDATE, ZB_FUNDCODE, ZB_FUNDNAME, ZB_INDEXTYPE, source, timeType, ZB_INDEXCODE, selectProductTableData, pageMarginsOption, fundType } =
            JSON.parse(componentInfo.elementCfg)
          this.currentTemplate = {
            ...row,
            ZB_BEGINDATE,
            ZB_ENDDATE,
            ZB_FUNDCODE,
            ZB_FUNDNAME,
            ZB_INDEXTYPE,
            source,
            timeType,
            ZB_INDEXCODE,
            selectProductTableData: selectProductTableData || [],
            fundType,
            reportType: row.reportType
          }
          this.globalSettingConfig = JSON.parse(componentInfo.elementCfg)
          this.$refs.workshopReport.handleSelectSingleComponents(elementCfg.ZB_FUNDCODE)
          // 调用vuex添加对应组件渲染
          // 清空全局的componentData
          // 清空全局的componentDataArray
          // 默认查看第一页
          this.$store.dispatch('initComponent', { componentDataArray: moduleCfg })
          // 设置 页边距
          this.$store.dispatch('setPageMarginsOptionValue', pageMarginsOption)
          this.$bus.$emit('initpag', moduleCfg.length || 1)
          setTimeout(() => {
            // 设置分页数量
            moduleCfg[0].forEach((item) => {
              this.$store.commit('addComponent', { component: item })
            })
          }, 0)
          this.loading = false
        }
      })
    },

    /**
     * @description 新建模板的查看
     */
    handleShowTemplateFromNew({ row, config }) {
      this.globalSettingConfig = {}
      this.$store.commit('SET_IS_EDITOR', false)
      this.isShow = true
      const params = {}
      params.reportId = row.reportId
      this.loading = true
      this.$refs.workshopReport.handleSelectSingleComponents(config.ZB_FUNDCODE)
      pageApi.getTemplateComponent(params).then(async (res) => {
        if (res.data.status === 200) {
          let componentInfo = res.data.data || {}
          let moduleCfg = JSON.parse(componentInfo.moduleCfg)
          // 合并新增时选择产品基本信息入当前行数据
          let { ZB_BEGINDATE, ZB_ENDDATE, ZB_FUNDCODE, ZB_FUNDNAME, source, timeType, ZB_INDEXCODE, selectProductTableData, pageMarginsOption } = config
          this.currentTemplate = { ...config, reportType: '2' }
          // 调用vuex添加对应组件渲染
          // 清空全局的componentData
          // 清空全局的componentDataArray
          // 默认查看第一页
          if (moduleCfg.length > 0) {
            let promiseArray = []
            for (let j = 0; j < moduleCfg.length; j++) {
              let tempJ = moduleCfg[j]
              for (let i = 0; i < tempJ.length; i++) {
                let temp = tempJ[i]
                temp.info.params = {
                  ...temp.info.params,
                  ...{ ZB_BEGINDATE, ZB_ENDDATE, ZB_FUNDCODE, ZB_FUNDNAME }
                }
                let params = { ...temp.info.params, ...this.currentTemplate }

                params.moduleId = temp.info.id
                if (params.ZB_INDEXTYPE != 'zdyjz') {
                  params.ZB_INDEXCODEA = params.ZB_INDEXCODE
                  params.ZB_INDEXWEIGHTA = 100
                  params.ZB_INDEXCODEB = '000300'
                  params.ZB_INDEXWEIGHTB = 0
                  // params.ZB_FUNDCODE = [params.ZB_INDEXCODEA,params.ZB_INDEXWEIGHTA,params.ZB_INDEXCODEB,params.ZB_INDEXWEIGHTB].toString()
                }
                promiseArray.push(this.renderReplaceScript(temp, params))
                // await this.renderReplaceScript(temp, params)
              }
            }
            await Promise.all(promiseArray)
            this.$store.dispatch('initComponent', { componentDataArray: moduleCfg })
            this.$store.dispatch('setPageMarginsOptionValue', pageMarginsOption)
            this.$bus.$emit('initpag', moduleCfg.length || 1)
            setTimeout(() => {
              // 设置分页数量
              moduleCfg[0].forEach((item) => {
                this.$store.commit('addComponent', { component: item })
              })
            }, 0)
            this.loading = false
          } else {
            this.$store.dispatch('initComponent', { componentDataArray: moduleCfg })
            this.$bus.$emit('initpag', moduleCfg.length || 1)
            this.loading = false
          }
        }
      })
    },

    /**
     * @description editor查看，需要展示保存
     */
    handleShowTemplateFromNewForEditor({ row, config }) {
      this.globalSettingConfig = {}
      this.$store.commit('SET_IS_EDITOR', true)
      this.isShow = true
      const params = {}
      params.reportId = row.reportId
      this.loading = true
      pageApi.getTemplateComponent(params).then(async (res) => {
        if (res.data.status === 200) {
          let componentInfo = res.data.data || {}
          let moduleCfg = JSON.parse(componentInfo.moduleCfg)
          // 合并新增时选择产品基本信息入当前行数据
          let { ZB_BEGINDATE, ZB_ENDDATE, ZB_FUNDCODE, ZB_FUNDNAME, source, timeType, ZB_INDEXCODE, selectProductTableData, pageMarginsOption } = config
          this.currentTemplate = { ...config, reportType: '2', reportId: row.reportId }
          this.globalSettingConfig = JSON.parse(componentInfo.elementCfg)
          this.$refs.workshopReport.handleSelectSingleComponents(config.ZB_FUNDCODE)
          // 调用vuex添加对应组件渲染
          // 清空全局的componentData
          // 清空全局的componentDataArray
          // 默认查看第一页
          if (moduleCfg.length > 0) {
            let promiseArray = []
            for (let j = 0; j < moduleCfg.length; j++) {
              let tempJ = moduleCfg[j]
              for (let i = 0; i < tempJ.length; i++) {
                let temp = tempJ[i]
                temp.info.params = {
                  ...temp.info.params,
                  ...{ ZB_BEGINDATE, ZB_ENDDATE, ZB_FUNDCODE, ZB_FUNDNAME }
                }
                let params = { ...temp.info.params, ...this.currentTemplate }

                params.moduleId = temp.info.id
                if (params.ZB_INDEXTYPE != 'zdyjz') {
                  params.ZB_INDEXCODEA = params.ZB_INDEXCODE
                  params.ZB_INDEXWEIGHTA = 100
                  params.ZB_INDEXCODEB = '000300'
                  params.ZB_INDEXWEIGHTB = 0
                  // params.ZB_FUNDCODE = [params.ZB_INDEXCODEA,params.ZB_INDEXWEIGHTA,params.ZB_INDEXCODEB,params.ZB_INDEXWEIGHTB].toString()
                }
                promiseArray.push(this.renderReplaceScript(temp, params))
                // await this.renderReplaceScript(temp, params)
              }
            }
            await Promise.all(promiseArray)
            this.$store.dispatch('initComponent', { componentDataArray: moduleCfg })
            this.$store.dispatch('setPageMarginsOptionValue', pageMarginsOption)
            this.$bus.$emit('initpag', moduleCfg.length || 1)
            setTimeout(() => {
              // 设置分页数量
              moduleCfg[0].forEach((item) => {
                this.$store.commit('addComponent', { component: item })
              })
            }, 0)
            this.loading = false
          } else {
            this.$store.dispatch('initComponent', { componentDataArray: moduleCfg })
            this.$bus.$emit('initpag', moduleCfg.length || 1)
            this.loading = false
          }
        }
      })
    },

    // 系统模板的查看
    handleShowTemplateFromNewSystem({ row, config }) {
      this.globalSettingConfig = {}
      this.$store.commit('SET_IS_EDITOR', false)
      this.isShow = true
      const params = {}
      params.reportId = row.reportId
      this.loading = true
      this.$refs.workshopReport.handleSelectSingleComponents(config.ZB_FUNDCODE)
      pageApi.getTemplateComponent(params).then(async (res) => {
        if (res.data.status === 200) {
          let componentInfo = res.data.data || {}
          let moduleCfg = JSON.parse(componentInfo.moduleCfg)
          // 合并新增时选择产品基本信息入当前行数据
          let { ZB_BEGINDATE, ZB_ENDDATE, ZB_FUNDCODE, ZB_FUNDNAME, source, timeType, ZB_INDEXCODE, selectProductTableData, pageMarginsOption } = config
          this.currentTemplate = { ...config, reportType: '1' }
          // 调用vuex添加对应组件渲染
          // 清空全局的componentData
          // 清空全局的componentDataArray
          // 默认查看第一页
          if (moduleCfg.length > 0) {
            let promiseArray = []
            for (let j = 0; j < moduleCfg.length; j++) {
              let tempJ = moduleCfg[j]
              for (let i = 0; i < tempJ.length; i++) {
                let temp = tempJ[i]
                temp.info.params = {
                  ...temp.info.params,
                  ...{ ZB_BEGINDATE, ZB_ENDDATE, ZB_FUNDCODE, ZB_FUNDNAME }
                }
                let params = { ...temp.info.params, ...this.currentTemplate }
                if (params.ZB_INDEXTYPE != 'zdyjz') {
                  params.ZB_INDEXCODEA = params.ZB_INDEXCODE
                  params.ZB_INDEXWEIGHTA = 100
                  params.ZB_INDEXCODEB = '000300'
                  params.ZB_INDEXWEIGHTB = 0
                  // params.ZB_FUNDCODE = [params.ZB_INDEXCODEA,params.ZB_INDEXWEIGHTA,params.ZB_INDEXCODEB,params.ZB_INDEXWEIGHTB].toString()
                }
                params.moduleId = temp.info.id
                promiseArray.push(this.renderReplaceScript(temp, params))
                // await this.renderReplaceScript(temp, params)
              }
            }
            await Promise.all(promiseArray)

            this.$store.dispatch('initComponent', { componentDataArray: moduleCfg })
            this.$store.dispatch('setPageMarginsOptionValue', pageMarginsOption)
            this.$bus.$emit('initpag', moduleCfg.length || 1)
            setTimeout(() => {
              // 设置分页数量
              moduleCfg[0].forEach((item) => {
                this.$store.commit('addComponent', { component: item })
              })
            }, 0)
            this.loading = false
          } else {
            this.$store.dispatch('initComponent', { componentDataArray: moduleCfg })
            this.$bus.$emit('initpag', moduleCfg.length || 1)
            this.loading = false
          }
        }
      })
    },
    renderReplaceScript(temp, params) {
      return new Promise((resolve, reject) => {
        if (params.ZB_INDEXTYPE != 'zdyjz') {
          params.ZB_INDEXCODEA = params.ZB_INDEXCODE
          params.ZB_INDEXWEIGHTA = 100
          params.ZB_INDEXCODEB = '000300'
          params.ZB_INDEXWEIGHTB = 0
          // params.ZB_FUNDCODE = [params.ZB_INDEXCODEA,params.ZB_INDEXWEIGHTA,params.ZB_INDEXCODEB,params.ZB_INDEXWEIGHTB].toString()
        }
        if (params.ZB_X_INTERVAL && params.ZB_X_INTERVAL == '自适应') {
          params.ZB_X_INTERVAL = 'auto'
        }
        pageApi
          .render(params)
          .then((res) => {
            let { status, data } = res.data
            if (status == 200) {
              const scriptStr = `;
                var dom = document.getElementById('component${temp.id}')
                if(dom && dom.childNodes.length > 1) {
                  dom.childNodes[0].style.display = 'none'
                  dom.childNodes[1].style.display = 'flex'
                }
              `
              // 重新渲染div
              data = data.replaceAll('#uuid#', temp.id)
              let script = data.match(/<script\b[^>]*>([\s\S]*?)<\/script>/gm)[0]
              const div = data.replace(script, '')
              script = script.replace(/<script\s+type="text\/javascript"\s*>/g, '')
              script = script.replace(/<\/script>/g, '')
              script += scriptStr
              temp.info.render.script = script
            } else if (status == 501) {
              const scriptStr = `;
                var dom = document.getElementById('component${temp.id}')
                if(dom && dom.childNodes.length > 1) {
                  dom.childNodes[0].style.display = 'flex'
                  dom.childNodes[1].style.display = 'none'
                }
              `
              temp.info.render.script = scriptStr
            }
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
    }
  }
}
</script>

<style lang="scss">
.home {
  overflow-y: hidden;
  height: 100%;
}
.el-dialog__wrapper .el-dialog__header span {
  color: #333 !important;
}
.vxe-table .vxe-body--row.row--stripe {
  background-color: #f9fafe !important;
}
</style>

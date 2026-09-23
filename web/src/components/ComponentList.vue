<template>
  <div class="component-list">
    <div class="title">单基金</div>
    <el-collapse v-model="activeName" accordion>
      <el-collapse-item v-for="item in chartOptions" :key="item.id" :name="item.id" :title="item.name">
        <template slot="title">
          <svg-icon style="font-size: 16px" icon-class="templateTable" v-if="item.name == '表格控件'"></svg-icon>
          <svg-icon style="font-size: 16px" icon-class="templateShape" v-if="item.name == '图形控件'"></svg-icon>
          <svg-icon style="font-size: 16px" icon-class="templatePicture" v-if="item.name == '文本图片控件'"></svg-icon>
          <span style="margin-left: 10px">{{ item.name }}</span>
        </template>
        <div
          v-for="ele in item.cr_module_info"
          :key="ele.vc_module_id"
          :data-id="ele.vc_module_id"
          :data-name="ele.vc_module_name"
          :title="ele.vc_module_desc"
          class="control"
          draggable
          @dragstart="handleDragStart($event, ele.vc_module_render, ele.vc_element_config, ele.height, ele.width)"
        >
          <div class="control-item">
            <div style="height: 48px; width: 48px; text-align: center" v-html="ele.icon"></div>
            <div style="font-size: 14px; text-align: center; color: #333333">
              {{ ele.vc_module_name || '' }}
            </div>
          </div>
        </div>
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script>
export default {
  props: {
    chartOptions: {
      type: Array,
      required: true,
      default: () => {
        return []
      }
    }
  },
  data() {
    return {
      activeName: '1',
      titleActive: 'first'
    }
  },
  mounted() {},
  methods: {
    handleDragStart(e, render, options, height, width) {
      const info = {
        id: e.target.getAttribute('data-id'),
        name: e.target.getAttribute('data-name'),
        render,
        options,
        height,
        width
      }
      e.dataTransfer.setData('info', JSON.stringify(info))
    }
  }
}
</script>

<style lang="scss" scoped>
.component-list {
  .title {
    text-align: center;
    height: 40px;
    line-height: 40px;
    font-size: 14px;
    color: #333333;
    font-weight: bold;
    background-color: #e6e8f0;
    border-bottom: 1px solid #ccc;
  }

  height: 100%;
  background-color: #ffffff;

  ::v-deep .el-collapse {
    border-top: none !important;
  }

  ::v-deep .el-collapse-item__header {
    padding-left: 30px;
    background-color: #f9fafd;
    border-bottom: 1px solid #ccc;
    color: #333333;
  }

  ::v-deep .el-collapse-item__wrap {
    background-color: #ffffff;
    color: #333333 !important;
    border-bottom: 1px solid #DCDFE6;
    padding-left: 30px;
  }

  .control {
    width: 125px;
    height: 125px;
    float: left;
    padding: 8px;
    border-bottom: 1px dashed #DCDFE6;

    .control-item {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;

      span {
        font-size: 14px;
      }
    }
  }

  .control:nth-child(even) {
  }

  .control:nth-child(odd) {
    border-right: 1px dashed #DCDFE6;
  }

  .control:nth-last-child(1) {
    border-bottom: none !important;
  }
}
</style>

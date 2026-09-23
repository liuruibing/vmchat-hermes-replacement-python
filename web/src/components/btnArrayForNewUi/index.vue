<template>
  <div>
    <span v-for="(item, index) in formBtnArray">
      <el-button
        v-if="item.showType === showType"
        :key="index"
        :icon="getIconStr(item.name)"
        :loading="item.status"
        :plain="item.name == '重置'"
        :size="item.size"
        :type="item.type"
        class="formButton"
        :title="item.title"
        @click="formClickHandle(item.name)"
      >
        {{ item.name }}
      </el-button>
    </span>
  </div>
</template>
<script>
export default {
  name: "",
  props: {
    formBtnArray: {
      type: Array,
      default: [],
      required: true
    },
    showType: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      debounceFun: null
    };
  },
  mounted() {
    this.debounceFun = _.debounce((val) => {
      console.log("val", val);
      this.$emit("clickEvent", val);
    }, 500);
  },
  methods: {
    getIconStr(name) {
      if (name == "查询") {
        return "el-icon-search";
      } else if (name == "重置") {
        return "el-icon-refresh-right";
      } else if (["导出", "数据下载", "4系excel导出"].includes(name)) {
        return "el-icon-download";
      } else if (["导入", "数据上传", "4系excel上传"].includes(name)) {
        return "el-icon-upload";
      } else if (name == "新增") {
        return "el-icon-plus";
      } else if (["生成数据"].includes(name)){
        return "el-icon-video-play"
      }
    },
    formClickHandle(name) {
      this.debounceFun(name);
    }
  }
};
</script>

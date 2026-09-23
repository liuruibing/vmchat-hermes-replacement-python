
export default {
  methods: {
    fileValidate2 (file, fileList, flag) {
      this.$message.closeAll()
      if (!file.size) return this.fileSize2(file, fileList, flag)
      else return this.totalFilelSizeOrsame2(file, fileList, flag)
    },
    // 文件为0的时候校验
   fileSize2 (file, fileList, flag) {
      let totalFilel = []
      for (let item of fileList) {
        if (item.size) totalFilel.push(item)
      }
      this.$message.error("上传的文件不能为空文件！")
      // 列表文件
      if (flag) this.formInline.fileList = totalFilel
      else this.fileList_ = totalFilel;
    },
    totalFilelSizeOrsame2 (file, fileList, flag) {
      let hasName = [] //记录重名文件集合
      for (let item of fileList) {
         if (item.name == file.name) hasName.push(item)
      }
      // let flag = hasName.indexOf(file.name) !== -1 || false
      if (hasName.length > 1) this.totalFilelsame2 (file, fileList, flag)
      else this.totalFilelSize2 (file, fileList, flag)
    },
    // 总文件大小不能超过50M
   totalFilelSize2 (file, fileList, flag) {
     let totalFlag = 0
     let totalSize = 0
     let totalFilel = []
      for (let item of fileList) {
        totalSize = item.size + totalSize;
      }
      totalFlag = (totalSize / 1024 / 1024) < 50;
      if (!totalFlag) {
        this.$message.error("上传的文件不能超过 50M !");
        for (let item of fileList) {
          if (file.uid !== item.uid) {
            totalFilel.push(item);
          }
        }
      } else {
        for (let item of fileList) {
          totalFilel.push(item);
        }
      }
      // 列表文件
      if (flag) this.formInline.fileList = totalFilel
      else this.fileList_ = totalFilel;
    },
    // 存在相同文件名
    totalFilelsame2 (file, fileList, flag) {
      let totalFilel = []
      this.$confirm('存在相同文件名是否替换？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        for (let i of fileList) {
          if (i.name != file.name) totalFilel.push(i)
        }
        totalFilel.push(file)
        // 列表文件
        if (flag) this.formInline.fileList = totalFilel
        else this.fileList_ = totalFilel;
      }).catch(() => {
        for (let i = 0; i < fileList.length -1; i ++ ) totalFilel.push(fileList[i])
        // 列表文件
        if (flag) this.formInline.fileList = totalFilel
        else this.fileList_ = totalFilel;
      })
    }
  }
}
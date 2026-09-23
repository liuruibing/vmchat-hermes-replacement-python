// 导出excel
/* 
  * excelHeader 表头 ['表头一', '表头二']
  * excelData 表格数据 [[1,2], [3,4]]
  * filename 导出的文件名称
  * autoWidth 导出的表格宽度是否自动
  * bookType 导出文件的后缀类型 ["xlsx", "csv", "txt"]
 */
export function exportExcel (excelHeader = [], excelData = [], filename, autoWidth = true, bookType) {
  // 懒加载该用法
  import("@/vendor/Export2Excel").then(excel => {
    // 调用我们封装好的方法进行导出Excel
    excel.export_json_to_excel({
      // 导出的头部
      header: excelHeader,
      // 导出的内容
      data: excelData,
      // 导出的文件名称
      filename: filename || '',
      // 导出的表格宽度是否自动
      autoWidth: autoWidth,
      // 导出文件的后缀类型
      bookType: bookType || 'xlsx'
    })
  })
}

// 遍历图表series
/* 
  * echartsSeries 图表数据
  * type 图表类型1、折线图，柱状图等 2、饼图
 */
export function forEachSeries (echartsOption = {}, type = 1) {
  let excelHeader = []
  let excelData = []
  let echartsSeries = echartsOption.series
  let echartsXAxis = echartsOption.xAxis
  if (type === 1) {
    let obj = {
      name: '',
      data: echartsXAxis[0].data || []
    }
    echartsSeries.unshift(obj)
    // 遍历组装数据
    echartsSeries.forEach((item, index) => {
      excelHeader.push(item.name)
      item.data.forEach((list, key) => {
        if (!excelData[key]) {
          excelData[key] = []
        }
        excelData[key].push(list)
      })
    })
    // 统一加X轴数据
    // echartsXAxis[0] && echartsXAxis[0].data.forEach((item, index) => {
    //   console.log(item)
    //   console.log(excelData[index])
    //   // excelData[index].unshift(item)
    //   excelData[index].push(item)
    // })
  } else if (type === 2) {
    // 遍历组装数据
    echartsSeries.forEach((item, index) => {
      item.data.forEach((list, key) => {
        if (!excelData[0]) {
          excelData[0] = []
        }
        excelHeader.push(list.name)
        excelData[0].push(list.value)
      })
    })
  }
  return {
    excelHeader,
    excelData
  }
}

// 导出excel
export function downloadExcel (res, fileName) {
  console.log(res)
  // 将`blob`对象转化成一个可访问的`url`
  // let url = window.URL.createObjectURL(new Blob([res.data], {type: 'application/vnd.ms-excel;charset=utf-8'}))
  // let url = window.URL.createObjectURL(new Blob([res.data], {type: 'application/ms-excel'}))
  let url = window.URL.createObjectURL(new Blob([res.data]))
  let link = document.createElement('a')
  link.style.display = 'none'
  link.href = url
  link.setAttribute('download', fileName)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}
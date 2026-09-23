/**
 * 通过 arr 的 key 查询 value
 * 根据 val 查询 list 中 list.key 的 值，返回 list.value
 * val 传入为空，默认 返回 empty
 * @returns {string}
 */
export function getValueForArrayByKey(list, val, key, value, empty = '-' ) {
  if (!val || val === '-') return empty
  let getNewVal = ''
  for (let i in list){
    if (list[i][key] === val){
      getNewVal = list[i][value]
      break
    }
  }
  return getNewVal
};

export function downloadFile(url,fileName) {
  // 创建a标签
  // link.target = '_blank'
  const link = document.createElement('a')
  link.setAttribute('href', url)
  link.setAttribute('download', fileName)
  document.body.appendChild(link)
  // 模拟手动点击a标签下载文件
  link.click();
  setTimeout(() => {
    // 删除DOM节点
    document.body.removeChild(link)
  }, 1000);
}

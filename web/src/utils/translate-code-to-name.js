const { fn } = require("moment");


/**
 * 
 * @param {翻译的字段个数 对象新式} NameObj 
 * @param {列表展示的原始数据} tableList 
 * @param {api请求到的字典数据列表} apoList 
 */
export function translateCodeToName(NameObj, tableList, apoList) {
  for (let n in NameObj) {
    for (let i of tableList) {
      for (let j of apoList) {
        if (i[n] == j.dimCde) {
          i[NameObj[n]] = j.dimNme
        }
      }
    }
  }
  // console.log('tableList', tableList)
  return tableList
}
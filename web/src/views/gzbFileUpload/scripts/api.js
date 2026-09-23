import request from '@/utils/request'
const FileFormData = { 'Content-Type': 'multipart/form-data' }


/**
 * @description 上传文件解压存储记录列表查询
 * @param {*} data
 * @returns
 */
export const queryTableList = data => {
  return request({
    url: '/api/gzrest/queryGzFileLog',
    method: 'POST',
    data
  })
}


/**
 * @description 数据处理日志表格查询列表查询
 * @param {*} data
 * @returns
 */
export const queryDataClearLogTableList = data => {
  return request({
    url: '/api/gzrest/queryGzbDataClearMainLog',
    method: 'POST',
    data
  })
}

/**
 * @description 日志明细表格查询列表查询
 * @param {*} data
 * @returns
 */
export const queryGzbDataClearDetailLog = data => {
  return request({
    url: '/api/gzrest/queryGzbDataClearDetailLog',
    method: 'POST',
    data
  })
}

// 字典查询
export  function selectType(dimType) {
  return request({
    url: "/api/common/edim/" + dimType,
    method: "get"
  });

}

/**
 * @description 校验日志列表查询
 * @param {*} data
 * @returns
 */
export const queryGzbDataCheckInfoLog = data => {
  return request({
    url: '/api/gzrest/queryGzbDataCheckInfoLog',
    method: 'POST',
    data
  })
}

/**
 * @description 删除
 * @param {*} data
 * @returns
 */
export const deleteFileGroupZS = data => {
  return request({
    url: '/api/gzrest/deleteFileGroupZS',
    method: 'POST',
    data
  })
}

/**
 * @description 估值数据校验
 * @param {*} data
 * @returns
 */
export const doGzbDataCheckZS = data => {
  return request({
    url: '/api/gzrest/doGzbDataCheckZS',
    method: 'POST',
    data
  })
}

/**
 * @description 估值数据处理
 * @param {*} data
 * @returns
 */
export const doGzbDataClearZS = data => {
  return request({
    url: '/api/gzrest/doGzbDataClearZS',
    method: 'POST',
    data
  })
}
/**
 * @description 查看估值文件内容
 * @param {*} data
 * @returns
 */
export const queryGzbFileData = data => {
  return request({
    url: '/api/gzrest/queryGzbFileData',
    method: 'POST',
    data
  })
}
/**
 * @description 估值文件批量导入
 * @param {*} data
 * @returns
 */
export const uploadGzbFile = data => {
  return request({
    headers: FileFormData,
    url: '/api/gzrest/batchGzbUpload',
    method: 'post',
    data: data
  })
}


/**
 * @description 净值文件批量导入
 * @param {*} data
 * @returns
 */
export const uploadNetFile = data => {
  return request({
    headers: FileFormData,
    url: '/api/gzrest/batchNetValueUpload',
    method: 'post',
    data: data
  })
}
/**
 * @description 净值文件模板下载
 * @param {*} data
 * @returns
 */
export function downloadNetExcelTemplate() {
  return request({
    url: '/api/gzrest/downloadNetExcelTemplate',
    method: 'post',
  })

}




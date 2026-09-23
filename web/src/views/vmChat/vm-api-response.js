function firstMessage(payload, fallback) {
  if (!payload || typeof payload !== 'object') return fallback
  return payload.message || payload.msg || payload.errorMessage || payload.errorMsg || fallback
}

export function unwrapVmResponse(response) {
  if (!response) return null
  return response.data !== undefined ? response.data : response
}

export function assertVmBusinessSuccess(payload, displayName = '业务接口') {
  if (!payload || typeof payload !== 'object' || Array.isArray(payload)) return payload
  if (payload.status === undefined || payload.status === null || payload.status === '') return payload
  if (Number(payload.status) === 0) return payload

  const businessCode = payload.code !== undefined && payload.code !== null
    ? String(payload.code)
    : String(payload.status)
  const error = new Error(firstMessage(payload, displayName + '返回失败') + '（错误码：' + businessCode + '）')
  error.code = businessCode
  error.businessStatus = payload.status
  throw error
}

export function unwrapVmBusinessResponse(response, displayName) {
  return assertVmBusinessSuccess(unwrapVmResponse(response), displayName)
}

export const HERMES_DOCUMENT_STORAGE_KEY = 'fof-research-hermes-active-document'

function canUseSessionStorage() {
  return typeof window !== 'undefined' && window.sessionStorage
}

export function getPendingHermesDocument() {
  if (!canUseSessionStorage()) return null
  const raw = window.sessionStorage.getItem(HERMES_DOCUMENT_STORAGE_KEY)
  if (!raw) return null
  try {
    const parsed = JSON.parse(raw)
    if (!parsed || typeof parsed !== 'object') return null
    const documentId = String(parsed.document_id || parsed.documentId || '').trim()
    if (!documentId) return null
    return Object.assign({}, parsed, { document_id: documentId })
  } catch (error) {
    window.sessionStorage.removeItem(HERMES_DOCUMENT_STORAGE_KEY)
    return null
  }
}

export function setPendingHermesDocument(document) {
  const value = document && typeof document === 'object' ? document : null
  if (!value) return clearPendingHermesDocument()
  const documentId = String(value.document_id || value.documentId || '').trim()
  if (!documentId) throw new Error('上传结果缺少 document_id')
  const normalized = Object.assign({}, value, { document_id: documentId })
  if (canUseSessionStorage()) {
    window.sessionStorage.setItem(HERMES_DOCUMENT_STORAGE_KEY, JSON.stringify(normalized))
  }
  return normalized
}

export function clearPendingHermesDocument() {
  if (canUseSessionStorage()) {
    window.sessionStorage.removeItem(HERMES_DOCUMENT_STORAGE_KEY)
  }
  return null
}

export function getPendingHermesDocumentIds() {
  const document = getPendingHermesDocument()
  return document ? [document.document_id] : []
}

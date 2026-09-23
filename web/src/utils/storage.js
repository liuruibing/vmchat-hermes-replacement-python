export default {
  setItem(key, value) {
    value = JSON.stringify(value);
    window.sessionStorage.setItem(key, value)
  },
  getItem(key) {
    let value = window.sessionStorage.getItem(key)
    value = JSON.parse(value);
    return value || ''
  },
  removeItem(key) {
    window.sessionStorage.removeItem(key)
  },
  clear() {
    window.sessionStorage.clear()
  },
}
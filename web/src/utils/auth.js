// import Cookies from 'js-cookie'

// const TokenKey = 'Datadriver-Web-Token'
const TokenKey = 'BDSUGSTORED'

export function getToken() {
  // return Cookies.get(TokenKey)
  return localStorage.getItem(TokenKey)
}

export function setToken(token) {
  // return Cookies.set(TokenKey, token)
  return localStorage.setItem(TokenKey, token)
}

export function removeToken() {
  // return Cookies.remove(TokenKey)
  return localStorage.removeItem(TokenKey)
}

export function getCookiesData(data) {
  // return Cookies.get(data)
  return localStorage.getItem(data)
}

export function setCookiesData(data, value) {
  // return Cookies.set(data, value)
  return localStorage.setItem(data, value)
}

export function removeCookiesData(data) {
  // return Cookies.remove(data)
  return localStorage.removeItem(data)
}

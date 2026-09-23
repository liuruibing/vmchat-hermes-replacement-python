import moment from 'moment'

export default {
  isvalidUsername(str) {
    const valid_map = ['admin', 'editor']
    return valid_map.indexOf(str.trim()) >= 0
  },

  /* 合法uri*/
  validateURL(textval) {
    const urlregex = /^(https?|ftp):\/\/([a-zA-Z0-9.-]+(:[a-zA-Z0-9.&%$-]+)*@)*((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}|([a-zA-Z0-9-]+\.)*[a-zA-Z0-9-]+\.(com|edu|gov|int|mil|net|org|biz|arpa|info|name|pro|aero|coop|museum|[a-zA-Z]{2}))(:[0-9]+)*(\/($|[a-zA-Z0-9.,?'\\+&%$#=~_-]+))*$/
    return urlregex.test(textval)
  },

  /* 小写字母*/
  validateLowerCase(str) {
    const reg = /^[a-z]+$/
    return reg.test(str)
  },

  /* 大写字母*/
  validateUpperCase(str) {
    const reg = /^[A-Z]+$/
    return reg.test(str)
  },

  /* 大小写字母*/
  validateAlphabets(str) {
    const reg = /^[A-Za-z]+$/
    return reg.test(str)
  },

  /**
   * validate email
   * @param email
   * @returns {boolean}
   */
  validateEmail(email) {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    return re.test(email)
  },
  // 时间不能超过三年
  validateThreeYears(time) {
    if (time) {
      let beginTime = time[0]
      let endTime = time[1]
      //三年前时间戳
      let threeTimeVal = moment(moment(endTime).subtract(3, 'years'))
        .subtract(-1, 'days')
        .valueOf()
      //开始时间时间戳
      let beginTimeVal = moment(beginTime).valueOf()
      if (beginTimeVal < threeTimeVal) {
        return false
      } else {
        return true
      }
    } else {
      return false
    }
  },

  // url处理特殊字符
  validateCharacter(value) {
    if (!value) return ''
    value = encodeURIComponent(String(value))
    return value
  },

  // 校验一个字符串是否是json 类型
  isJSON(str) {
    if (typeof str == 'string') {
      try {
        let obj = JSON.parse(str)
        if (typeof obj == 'object' && obj) {
          return true
        } else {
          return false
        }
      } catch (e) {
        console.log(e)
        return false
      }
    } else {
      return 'It is not a string!'
    }
  }
}

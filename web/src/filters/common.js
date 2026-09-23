import $ from 'jquery'
import {getToken} from '@/utils/auth'
import moment from 'moment'
import {Message} from 'element-ui'
import CryptoJS from 'crypto-js'
import store from '../store'
//乘法

function encryptByAES(plainText) {
  let key = CryptoJS.enc.Utf8.parse(getToken().replaceAll('-', '').slice(0, 16))
  let encrypted = CryptoJS.AES.encrypt(plainText, key, {
    mode: CryptoJS.mode.ECB,
    padding: CryptoJS.pad.Pkcs7
  })
  // 这里的encrypted不是字符串，而是一个CipherParams对象
  return encrypted.ciphertext.toString(CryptoJS.enc.Base64)
}

function accMul(arg1, arg2) {
  var m = 0,
    s1 = Number(arg1).toString(),
    s2 = Number(arg2).toString()
  try {
    m += s1.split('.')[1].length
  } catch (e) {
  }
  try {
    m += s2.split('.')[1].length
  } catch (e) {
  }
  return (Number(s1.replace('.', '')) * Number(s2.replace('.', ''))) / Math.pow(10, m)
}

// 除法
function accDiv(arg1, arg2) {
  var t1 = 0,
    t2 = 0,
    r1,
    r2
  try {
    t1 = Number(arg1)
      .toString()
      .split('.')[1].length
  } catch (e) {
  }
  try {
    t2 = Number(arg2)
      .toString()
      .split('.')[1].length
  } catch (e) {
  }
  r1 = Number(arg1.toString().replace('.', ''))
  r2 = Number(arg2.toString().replace('.', ''))
  return (r1 / r2) * Math.pow(10, t2 - t1)
}

function addZero(m) {
  return m < 10 ? '0' + m : m
}

export default {
  // vm risk文件下载
  file_vmrisk_download(
    templateCode,
    beginDate,
    endDate,
    fundCode,
    benchmarkA,
    benchmarkB,
    benchmarkAValue,
    benchmarkBValue,
    rehaNav,
    noRisk
  ) {
    //   ?templateCode=B6BB3CB840804B9EAB57766F403D79C2&beginDate=2018-12-01&endDate=2018-12-31&fundCode=100010&token=vXcx3IBemn1kShhobK2DfpY3kFqiBaSb
    function download(
      src,
      templateCode,
      beginDate,
      endDate,
      fundCode,
      token,
      benchmarkA,
      benchmarkB,
      benchmarkAValue,
      benchmarkBValue,
      rehaNav,
      noRisk
    ) {
      var iframe = $("<iframe name='file_iframe'></iframe>")
      iframe.attr('style', 'display:none') //下面为在form表单中添加查询参数

      var form = $("<form submit = 'return false'></form>") //定义一个form表单

      form.attr('style', 'display:none') //下面为在form表单中添加查询参数

      form.attr('target', 'file_iframe')

      form.attr('method', 'get')

      form.attr('action', src)
      //模板编码
      var input1 = $('<input>')

      input1.attr('type', 'hidden')

      input1.attr('name', 'templateCode')

      input1.attr('value', templateCode)
      //开始时间
      var input2 = $('<input>')

      input2.attr('type', 'hidden')

      input2.attr('name', 'beginDate')

      input2.attr('value', beginDate)
      //结束时间
      var input3 = $('<input>')

      input3.attr('type', 'hidden')

      input3.attr('name', 'endDate')

      input3.attr('value', endDate)
      //组合代码
      var input4 = $('<input>')

      input4.attr('type', 'hidden')

      input4.attr('name', 'fundCode')

      input4.attr('value', fundCode)
      //token
      var input5 = $('<input>')

      input5.attr('type', 'hidden')

      input5.attr('name', 'token')

      input5.attr('value', token)
      var input6 = $('<input>')

      input6.attr('type', 'hidden')

      input6.attr('name', 'benchmarkA')

      input6.attr('value', benchmarkA)
      var input7 = $('<input>')

      input7.attr('type', 'hidden')

      input7.attr('name', 'benchmarkB')

      input7.attr('value', benchmarkB)
      var input8 = $('<input>')

      input8.attr('type', 'hidden')

      input8.attr('name', 'benchmarkAValue')

      input8.attr('value', benchmarkAValue)
      var input9 = $('<input>')

      input9.attr('type', 'hidden')

      input9.attr('name', 'benchmarkBValue')

      input9.attr('value', benchmarkBValue)
      var input10 = $('<input>')

      input10.attr('type', 'hidden')

      input10.attr('name', 'rehaNav')

      input10.attr('value', rehaNav)
      var input11 = $('<input>')

      input11.attr('type', 'hidden')

      input11.attr('name', 'noRisk')

      input11.attr('value', noRisk)
      $('body').append(iframe) //将表单放置在web中

      iframe.append(form)

      form.append(input1, input2, input3, input4, input5, input6, input7, input8, input9, input10, input11) //将查询参数控件提交到表单上

      form.submit()
    }

    let token = getToken()
    download(
      process.env.BASE_API + '/rest/report/export.do',
      templateCode,
      beginDate,
      endDate,
      fundCode,
      token,
      benchmarkA,
      benchmarkB,
      benchmarkAValue,
      benchmarkBValue,
      rehaNav,
      noRisk
    )
  },
  /**
   * 时间戳转化成时间格式  YYYY-MM-DD: HH:MM:SS
   * type 1 YYYY-MM-DD
   */
  timeFormat(timestamp, type = 0) {
    if (typeof timestamp == 'undefined') return
    //timestamp是整数，否则要parseInt转换,不会出现少个0的情况
    var time = new Date(timestamp)
    var year = time.getFullYear()
    var month = time.getMonth() + 1
    var date = time.getDate()
    var hours = time.getHours()
    var minutes = time.getMinutes()
    var seconds = time.getSeconds()
    if (type === 1) {
      return (
        year +
        '-' +
        addZero(month) +
        '-' +
        addZero(date)
      )
    }
    return (
      year +
      '-' +
      addZero(month) +
      '-' +
      addZero(date) +
      ' ' +
      addZero(hours) +
      ':' +
      addZero(minutes) +
      ':' +
      addZero(seconds)
    )
  },
  // etl 日志检索的树状数据
  setLogTreeData(nodes, treeRootId) {
    for (let i = 0; i < nodes.length; i++) {
      if (nodes[i].f_parent_id == treeRootId) {
        break
      } else if (i == nodes.length - 1) {
        Message.closeAll()
        Message({
          message: '数据格式错误',
          type: 'error',
          duration: 2 * 1000
        })
      } else {
      }
    }

    let nodesFilters = nodes

    let groups = {}
    //默认展开的节点
    let expandRowKeys = []
    // 按父节点将节点分组
    for (var i in nodesFilters) {
      if (!groups[nodesFilters[i].f_parent_id]) {
        groups[nodesFilters[i].f_parent_id] = []
      }
      groups[nodesFilters[i].f_parent_id].push(nodesFilters[i])
      if (treeRootId && treeRootId === nodesFilters[i].f_id) {
        // 发现传入的根节点id作为节点id时，将根节点设置为该节点的父节点
        treeRootId = nodesFilters[i].f_parent_id
      }
    }

    var rootNodes = groups[treeRootId]
    groups[treeRootId] = null // [SAFEGUARD]防止自为父节点或互为父节点（有环图结构）导致的死循环
    function traverseTreeNodeGroup(treeNodeGroup) {
      for (var i in treeNodeGroup) {
        let node = treeNodeGroup[i]
        if (groups[node.f_id]) {
          node.children = groups[node.f_id]
          groups[node.f_id] = null // [SAFEGUARD]防止自为父节点或互为父节点（有环图结构）导致的死循环
          traverseTreeNodeGroup(node.children)
        } else {
        }
        //选择默认展开的节点
        if (node.f_parent_id == treeRootId) {
          expandRowKeys.push(node.f_id)
        } else {
        }
      }
    }

    traverseTreeNodeGroup(rootNodes)

    return {data: rootNodes, expandRowKeys: expandRowKeys}
  },

  // 时间转化为时间戳
  un_timestampToTime(timestamp) {
    var date = new Date(timestamp)
    var time1 = date.getTime()
    // var time2 = date.valueOf();
    // var time3 = Date.parse(date);
    // console.log(time1);//1398250549123
    // console.log(time2);//1398250549123
    // console.log(time3);//1398250549000 精确到毫秒
    return time1
  },
  // 时间戳年月日
  yyr_timestampToTime(timestamp) {
    var now = new Date(timestamp),
      y = now.getFullYear(),
      m = now.getMonth() + 1,
      d = now.getDate()
    return y + '-' + (m < 10 ? '0' + m : m) + '-' + (d < 10 ? '0' + d : d)
  },
  // 返回当前月份
  yyr_getMonth(timestamp) {
    var now = new Date(timestamp),
      y = now.getFullYear(),
      m = now.getMonth() + 1,
      d = now.getDate()
    return m
  },
  // 返回当前年份
  yyr_getYear(timestamp) {
    var now = new Date(timestamp),
      y = now.getFullYear(),
      m = now.getMonth() + 1,
      d = now.getDate()
    return y
  },
  // 时间戳
  timestampToTime(timestamp) {
    var now = new Date(timestamp),
      y = now.getFullYear(),
      m = now.getMonth() + 1,
      d = now.getDate()
    return (
      y + '-' + (m < 10 ? '0' + m : m) + '-' + (d < 10 ? '0' + d : d) + ' ' + now.toTimeString().substr(0, 8)
    )
  },
  // 时间戳减运算
  timestampToTime_add(timestamp, days) {
    var day = parseInt(days)

    var now = timestamp + 24 * 60 * 60 * 1000 * day

    return now
  },
  //获取当前时间戳n年前的时间
  yearTimetampToTime_before(presentTime, n) {
    var curDate = presentTime
    var fourYearsTime = 365 * n * 24 * 60 * 60 * 1000
    var result = curDate + fourYearsTime
    var resultDate = new Date(result)
    var year = resultDate.getFullYear()
    var month = resultDate.getMonth() + 1
    var day = resultDate.getDate()

    var date = new Date(year + '-' + month + '-' + day)

    var time1 = date.getTime()

    return time1
  },
  //获取当前时间戳n天前的时间
  DayTimetampToTime_before(presentTime, n) {
    var curDate = presentTime
    var fourYearsTime = n * 24 * 60 * 60 * 1000
    var result = curDate + fourYearsTime
    var resultDate = new Date(result)
    var year = resultDate.getFullYear()
    var month = resultDate.getMonth() + 1
    var day = resultDate.getDate()

    var date = new Date(year + '-' + month + '-' + day)

    var time1 = date.getTime()

    return time1
  },
  //获取前几个月的日期
  getPreMonthDay(date, monthNum) {
    let dateArr = date.split('-')
    let year = dateArr[0] //获取当前日期的年份
    let month = dateArr[1] //获取当前日期的月份
    let day = dateArr[2] //获取当前日期的日
    let days = new Date(year, month, 0)
    days = days.getDate() //获取当前日期中月的天数
    let year2 = year
    let month2 = parseInt(month) - monthNum
    if (month2 <= 0) {
      year2 = parseInt(year2) - parseInt(month2 / 12 == 0 ? 1 : Math.abs(parseInt(month2 / 12)) + 1)
      month2 = 12 - (Math.abs(month2) % 12)
    }
    let day2 = day
    let days2 = new Date(year2, month2, 0)
    days2 = days2.getDate()
    if (day2 > days2) {
      day2 = days2
    }
    if (month2 < 10) {
      month2 = '0' + month2
    }
    let t2 = year2 + '-' + month2 + '-' + day2
    return t2
  },
  //获取前后几个月的日期
  getNextMonth(date, monthNum) {
    let dateArr = date.split('-')
    let year = dateArr[0] //获取当前日期的年份
    let month = dateArr[1] //获取当前日期的月份
    let day = dateArr[2] //获取当前日期的日
    let days = new Date(year, month, 0)
    days = days.getDate() //获取当前日期中月的天数
    let year2 = year
    let month2 = parseInt(month) + monthNum
    if (month2 >= 12) {
      year2 = parseInt(year2) + parseInt(parseInt(month2) / 12 == 0 ? 1 : parseInt(month2) / 12)
      month2 = parseInt(month2) % 12
    }
    let day2 = day
    let days2 = new Date(year2, month2, 0)
    days2 = days2.getDate()
    if (day2 > days2) {
      day2 = days2
    }
    if (month2 < 10) {
      month2 = '0' + month2
    }
    let t2 = year2 + '-' + month2 + '-' + day2
    return t2
  },
  //获取当前时间
  get_newDate() {
    var now = new Date()
    var year = now.getFullYear()
    var month = now.getMonth() + 1
    if (month < 10) {
      month = '0' + month
    }
    var date = now.getDate()
    if (date < 10) {
      date = '0' + date
    }

    return year + '-' + month + '-' + date
  },
  // 时分秒
  hhmmss() {
    var myDate = new Date()
    var Hours = myDate.getHours()
    var Minutes = myDate.getMinutes()
    var Seconds = myDate.getSeconds()
    return (
      ' ' +
      (Hours < 10 ? '0' + Hours : Hours) +
      ':' +
      (Minutes < 10 ? '0' + Minutes : Minutes) +
      ':' +
      (Seconds < 10 ? '0' + Seconds : Seconds)
    )
  },
  // 非数据判断转换
  abnormalityData(val) {
    if (val === undefined || val === null) {
      return ''
    } else {
      return val
    }
  },
  //日期时间段快捷选项
  dateShortcut() {
    const pickerOptions = {
      shortcuts: [
        {
          text: '本周',
          onClick(picker) {
            const end = moment()
              .subtract(1, 'days')
              .format('YYYY-MM-DD')
            const start = moment(end)
              .isoWeekday(1)
              .format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        },
        {
          text: '本月',
          onClick(picker) {
            const end = moment()
              .subtract(1, 'days')
              .format('YYYY-MM-DD')
            const start = moment([moment(end).year(), 0, 1])
              .month(moment(end).month())
              .format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        },
        {
          text: '本季度',
          onClick(picker) {
            const end = moment()
              .subtract(1, 'days')
              .format('YYYY-MM-DD')
            const start = moment(moment(end).year() + '-01-01')
              .quarter(moment(end).quarter())
              .format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        },
        {
          text: '今年以来',
          onClick(picker) {
            const end = moment()
              .subtract(1, 'days')
              .format('YYYY-MM-DD')
            const start = moment(end).year() + '-01-01'
            picker.$emit('pick', [start, end])
          }
        },
        {
          text: '去年',
          onClick(picker) {
            const end = moment().year() - 1 + '-12-31'
            const start = moment().year() - 1 + '-01-01'
            picker.$emit('pick', [start, end])
          }
        },
        {
          text: '最近一个月',
          onClick(picker) {
            const end = moment()
              .subtract(1, 'days')
              .format('YYYY-MM-DD')
            const start = moment(
              moment(end)
                .subtract(1, 'month')
                .format('YYYY-MM-DD')
            )
              .subtract(-1, 'days')
              .format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        },
        {
          text: '最近三个月',
          onClick(picker) {
            const end = moment()
              .subtract(1, 'days')
              .format('YYYY-MM-DD')
            const start = moment(
              moment(end)
                .subtract(3, 'month')
                .format('YYYY-MM-DD')
            )
              .subtract(-1, 'days')
              .format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        },
        {
          text: '最近半年',
          onClick(picker) {
            const end = moment()
              .subtract(1, 'days')
              .format('YYYY-MM-DD')
            const start = moment(
              moment(end)
                .subtract(6, 'month')
                .format('YYYY-MM-DD')
            )
              .subtract(-1, 'days')
              .format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        },
        {
          text: '最近一年',
          onClick(picker) {
            const end = moment()
              .subtract(1, 'days')
              .format('YYYY-MM-DD')
            const start = moment(
              moment(end)
                .subtract(1, 'years')
                .format('YYYY-MM-DD')
            )
              .subtract(-1, 'days')
              .format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        }
      ]
    }
    return pickerOptions
  },
  //日期时间点快捷选项
  dateShortDot() {
    const pickerOptions = {
      shortcuts: [
        {
          text: '今天',
          onClick(picker) {
            const start = new Date()
            picker.$emit('pick', start)
          }
        },
        {
          text: 'T - 1',
          onClick(picker) {
            const start = moment()
              .subtract(1, 'days')
              .format('YYYY-MM-DD')
            picker.$emit('pick', start)
          }
        },
        {
          text: '一月前',
          onClick(picker) {
            const start = moment(
              moment(new Date())
                .subtract(1, 'month')
                .format('YYYY-MM-DD')
            )
              .subtract(0, 'days')
              .format('YYYY-MM-DD')
            picker.$emit('pick', start)
          }
        },
        {
          text: '三月前',
          onClick(picker) {
            const start = moment(
              moment(new Date())
                .subtract(3, 'month')
                .format('YYYY-MM-DD')
            )
              .subtract(0, 'days')
              .format('YYYY-MM-DD')
            picker.$emit('pick', start)
          }
        },
        {
          text: '半年前',
          onClick(picker) {
            const start = moment(
              moment(new Date())
                .subtract(6, 'month')
                .format('YYYY-MM-DD')
            )
              .subtract(0, 'days')
              .format('YYYY-MM-DD')
            picker.$emit('pick', start)
          }
        },
        {
          text: '一年前',
          onClick(picker) {
            const start = moment(
              moment(new Date())
                .subtract(1, 'years')
                .format('YYYY-MM-DD')
            )
              .subtract(0, 'days')
              .format('YYYY-MM-DD')
            picker.$emit('pick', start)
          }
        }
      ]
    }
    return pickerOptions
  },

  // 加法
  accAdd(arg1, arg2) {
    var r1, r2, m, c
    try {
      r1 = Number(arg1)
        .toString()
        .split('.')[1].length
    } catch (e) {
      r1 = 0
    }
    try {
      r2 = Number(arg2)
        .toString()
        .split('.')[1].length
    } catch (e) {
      r2 = 0
    }
    c = Math.abs(r1 - r2)
    m = Math.pow(10, Math.max(r1, r2))
    if (c > 0) {
      var cm = Math.pow(10, c)
      if (r1 > r2) {
        arg1 = Number(arg1.toString().replace('.', ''))
        arg2 = Number(arg2.toString().replace('.', '')) * cm
      } else {
        arg1 = Number(arg1.toString().replace('.', '')) * cm
        arg2 = Number(arg2.toString().replace('.', ''))
      }
    } else {
      arg1 = Number(arg1.toString().replace('.', ''))
      arg2 = Number(arg2.toString().replace('.', ''))
    }
    return (arg1 + arg2) / m
  },

  // 减法
  accSub(arg1, arg2) {
    var r1, r2, m, n
    try {
      r1 = Number(arg1)
        .toString()
        .split('.')[1].length
    } catch (e) {
      r1 = 0
    }
    try {
      r2 = Number(arg2)
        .toString()
        .split('.')[1].length
    } catch (e) {
      r2 = 0
    }
    m = Math.pow(10, Math.max(r1, r2)) //last modify by deeka //动态控制精度长度
    n = r1 >= r2 ? r1 : r2
    return Number(((arg1 * m - arg2 * m) / m).toFixed(n))
  },

  // 乘法
  accMul(arg1, arg2) {
    var m = 0,
      s1 = Number(arg1).toString(),
      s2 = Number(arg2).toString()
    try {
      m += s1.split('.')[1].length
    } catch (e) {
    }
    try {
      m += s2.split('.')[1].length
    } catch (e) {
    }
    return (Number(s1.replace('.', '')) * Number(s2.replace('.', ''))) / Math.pow(10, m)
  },

  // 除法
  accDiv(arg1, arg2) {
    var t1 = 0,
      t2 = 0,
      r1,
      r2
    try {
      t1 = Number(arg1)
        .toString()
        .split('.')[1].length
    } catch (e) {
    }
    try {
      t2 = Number(arg2)
        .toString()
        .split('.')[1].length
    } catch (e) {
    }
    r1 = Number(arg1.toString().replace('.', ''))
    r2 = Number(arg2.toString().replace('.', ''))
    return (r1 / r2) * Math.pow(10, t2 - t1)
  },
  // 金额万元 千分位
  moneyMillion(n) {
    if (!n && n !== 0) return ''
    if (n === 0) return '0.00'
    // 如果前面有加减符号
    let head = ''
    if (typeof n === 'number') n = String(n)
    head = n.substring(0, 1)
    if (head === '+' || head === '-') {
      n = n.substring(1)
    } else {
      head = ''
    }
    n = n.toString().replace(/,/gi, '')
    n = accDiv(Number(n), 10000).toFixed(2)
    let re = /\d{1,3}(?=(\d{3})+$)/g
    let backValue = n.replace(/^(\d+)((\.\d*)?)$/, function (s, s1, s2) {
      return s1.replace(re, '$&,') + s2
    })
    // 转换完加上加减号
    if (head) backValue = head + backValue
    return backValue
  },
  /* 金额（元）千分位，保留两位小数 */
  moneyYuan(n) {
    if (!n && n !== 0) return '-'
    if (n === 0) return '0.00'
    // 如果前面有加减符号
    let head = ''
    if (typeof n === 'number') n = String(n)
    head = n.substring(0, 1)
    if (head === '+' || head === '-') {
      n = n.substring(1)
    } else {
      head = ''
    }
    n = n.toString().replace(/,/gi, '')
    n = Number(n).toFixed(2)
    let re = /\d{1,3}(?=(\d{3})+$)/g
    let backValue = n.replace(/^(\d+)((\.\d*)?)$/, function (s, s1, s2) {
      return s1.replace(re, '$&,') + s2
    })
    // 转换完加上加减号
    if (head) backValue = head + backValue
    return backValue
  },
  // 金额（亿元）千分位，保留两位小数
  moneyHundredMillion(n) {
    if (!n && n !== 0) return ''
    if (n === 0) return '0.00'
    // 如果前面有加减符号
    let head = ''
    if (typeof n === 'number') n = String(n)
    head = n.substring(0, 1)
    if (head === '+' || head === '-') {
      n = n.substring(1)
    } else {
      head = ''
    }
    n = n.toString().replace(/,/gi, '')
    n = accDiv(Number(n), 100000000).toFixed(2)
    let re = /\d{1,3}(?=(\d{3})+$)/g
    let backValue = n.replace(/^(\d+)((\.\d*)?)$/, function (s, s1, s2) {
      return s1.replace(re, '$&,') + s2
    })
    // 转换完加上加减号
    if (head) backValue = head + backValue
    return backValue
  },
  // 保留n位小数，乘以多少
  numberToFixed(val, n, ride) {
    if (val === undefined || val === '' || val === null) {
      return ''
    } else {
      return accMul(val, ride).toFixed(n)
    }
  },
  //四舍五入保留2位小数（若第二位小数为0，则保留一位小数）
  keepTwoDecimal(num) {
    var result = parseFloat(num)
    if (isNaN(result)) {
      return false
    }
    result = Math.round(num * 100) / 100
    return result
  },
  // 列表排序值处理
  queryOrderBy_vxe(val) {
    let orderBy = ''
    if (val.order === 'asc') {
      orderBy = `${val.property} asc` // 升序
    } else if (val.order === 'desc') {
      orderBy = `${val.property} desc` // 降序
    } else {
      orderBy = ''
    }
    return orderBy
  },
  //千分位格式化
  formatNumber(num) {
    if (num === undefined || num === '' || num === null) {
      return ''
    } else {
      var groups = /([\-\+]?)(\d*)(\.\d+)?/g.exec('' + num),
        mask = groups[1], //符号位
        integers = (groups[2] || '').split(''), //整数部分
        decimal = groups[3] || '', //小数部分
        remain = integers.length % 3

      var temp = integers
        .reduce(function (previousValue, currentValue, index) {
          if (index + 1 === remain || (index + 1 - remain) % 3 === 0) {
            return previousValue + currentValue + ','
          } else {
            return previousValue + currentValue
          }
        }, '')
        .replace(/\,$/g, '')
      return mask + temp + decimal
    }
  },
  //千分位转化为数字
  StrToNumber(obj) {
    var reg = /^[0-9]+.?[0-9]*$/ //验证字符串是否是数字
    if (!reg.test(obj)) {
      //为字符串 则判断是否存在','
      if ((obj + '').replace(/^\s\s*/, '').replace(/\s\s*$/, '') == '') {
        return 0.0
      }
      if (obj == undefined) {
        return 0.0
      }
      if ((obj || 0).toString().replace(/(\d)(?=(?:\d{3})+$)/g, '$1,')) {
        obj = obj.replace(/,/gi, '')
        return obj
      }
    }
    return obj
  },

  //金额转化为汉字
  changeMoneyToChinese(money) {
    var zeroCount, IntLen, i, n, p, q, m, decLen

    var cnNums = new Array('零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖') //汉字的数字
    var cnIntRadice = new Array('', '拾', '佰', '仟') //基本单位
    var cnIntUnits = new Array('', '万', '亿', '兆') //对应整数部分扩展单位
    var cnDecUnits = new Array('角', '分', '毫', '厘') //对应小数部分单位
    //var cnInteger = "整"; //整数金额时后面跟的字符
    var cnIntLast = '元' //整型完以后的单位
    var maxNum = 9999999999999999.9999 //最大处理的数字

    var IntegerNum //金额整数部分
    var DecimalNum //金额小数部分
    var ChineseStr = '' //输出的中文金额字符串
    var parts //分离金额后用的数组，预定义
    if (money == '') {
      return ''
    }
    money = parseFloat(money)
    if (money >= maxNum) {
      $.alert('超出最大处理数字')
      return ''
    }
    if (money == 0) {
      //ChineseStr = cnNums[0]+cnIntLast+cnInteger;
      ChineseStr = cnNums[0] + cnIntLast
      //document.getElementById("show").value=ChineseStr;
      return ChineseStr
    }
    money = money.toString() //转换为字符串
    if (money.indexOf('.') == -1) {
      IntegerNum = money
      DecimalNum = ''
    } else {
      parts = money.split('.')
      IntegerNum = parts[0]
      DecimalNum = parts[1].substr(0, 4)
    }
    if (parseInt(IntegerNum, 10) > 0) {
      //获取整型部分转换
      zeroCount = 0
      IntLen = IntegerNum.length
      for (i = 0; i < IntLen; i++) {
        n = IntegerNum.substr(i, 1)
        p = IntLen - i - 1
        q = p / 4
        m = p % 4
        if (n == '0') {
          zeroCount++
        } else {
          if (zeroCount > 0) {
            ChineseStr += cnNums[0]
          }
          zeroCount = 0 //归零
          ChineseStr += cnNums[parseInt(n)] + cnIntRadice[m]
        }
        if (m == 0 && zeroCount < 4) {
          ChineseStr += cnIntUnits[q]
        }
      }
      ChineseStr += cnIntLast
      //整型部分处理完毕
    }
    if (DecimalNum != '') {
      //小数部分
      decLen = DecimalNum.length
      for (i = 0; i < decLen; i++) {
        n = DecimalNum.substr(i, 1)
        if (n != '0') {
          ChineseStr += cnNums[Number(n)] + cnDecUnits[i]
        }
      }
    }
    if (ChineseStr == '') {
      //ChineseStr += cnNums[0]+cnIntLast+cnInteger;
      ChineseStr += cnNums[0] + cnIntLast
    }
    /* else if( DecimalNum == '' ){
                    ChineseStr += cnInteger;
                    ChineseStr += cnInteger;
                } */
    return ChineseStr
  },

  //转化为树状结构 下拉框 组合列表 小写pid
  searchTreeData(nodes, treeRootId, flag) {
    for (let i = 0; i < nodes.length; i++) {
      if (nodes[i].pid == treeRootId) {
        break
      } else if (i == nodes.length - 1) {
        Message.closeAll()
        Message({
          message: '数据格式错误',
          type: 'error',
          duration: 2 * 1000
        })
      }
    }

    let nodesFilters = nodes
    //默认展开的节点
    let expandRowKeys = []
    let groups = {}
    // 按父节点将节点分组
    for (var i in nodesFilters) {
      if (!groups[nodesFilters[i].pid]) {
        groups[nodesFilters[i].pid] = []
      }
      groups[nodesFilters[i].pid].push(nodesFilters[i])
      if (treeRootId && treeRootId === nodesFilters[i].id) {
        // 发现传入的根节点id作为节点id时，将根节点设置为该节点的父节点
        treeRootId = nodesFilters[i].pid
      }
    }

    var rootNodes = groups[treeRootId]
    groups[treeRootId] = null // [SAFEGUARD]防止自为父节点或互为父节点（有环图结构）导致的死循环
    let defaultIndex = 0
    let defaultNodeId = '' //默认选取的节点的id
    function traverseTreeNodeGroup(treeNodeGroup) {
      for (var i in treeNodeGroup) {
        var node = treeNodeGroup[i]
        node.label = node.name
        node.value = node.id
        if (groups[node.id]) {
          node.children = groups[node.id]
          groups[node.id] = null // [SAFEGUARD]防止自为父节点或互为父节点（有环图结构）导致的死循环
          // 存在子节点的要禁用父节点
          // node.disabled = true;
          traverseTreeNodeGroup(node.children)
        } else {
          // 非个券的要禁用 非产品禁用
          if (node.checkBox == 'checkBoxN') {
            node.disabled = true
          } else {
            defaultIndex++
            //默认选中第一个可用的子节点
            if (defaultIndex == 1) {
              defaultNodeId = node
            }
            //产品左侧树状结构   只修改子节点的id
            node.label = ' [ ' + node.id + ' ]' + node.name
          }
        }
        //选择默认展开的节点 不展开其他
        if (node.pid == treeRootId) {
          if (node.id != -1) {
            expandRowKeys.push(node.id)
          }
        }
      }
    }

    traverseTreeNodeGroup(rootNodes)
    // 如果为搜索打开全部节点
    if (flag) {
      rootNodes.forEach(item => {
        if (item.children && item.children.length) {
          item.children.forEach(list => {
            expandRowKeys.push(list.id)
          })
        }
      })
    }
    return {treeNode: rootNodes, defaultNode: defaultNodeId, expandRowKeys: expandRowKeys}
  },
  //收益贡献转化为树状结构 下拉框  小写pid
  earingsConTreeData(nodes, treeRootId) {
    for (let i = 0; i < nodes.length; i++) {
      if (nodes[i].pid == treeRootId) {
        break
      } else if (i == nodes.length - 1) {
        Message.closeAll()
        Message({
          message: '数据格式错误',
          type: 'error',
          duration: 2 * 1000
        })
      } else {
      }
    }

    let nodesFilters = nodes

    let groups = {}
    //默认展开的节点
    let expandRowKeys = []
    // 按父节点将节点分组
    for (var i in nodesFilters) {
      if (!groups[nodesFilters[i].pid]) {
        groups[nodesFilters[i].pid] = []
      }
      groups[nodesFilters[i].pid].push(nodesFilters[i])
      if (treeRootId && treeRootId === nodesFilters[i].id) {
        // 发现传入的根节点id作为节点id时，将根节点设置为该节点的父节点
        treeRootId = nodesFilters[i].pid
      }
    }

    var rootNodes = groups[treeRootId]
    groups[treeRootId] = null // [SAFEGUARD]防止自为父节点或互为父节点（有环图结构）导致的死循环
    function traverseTreeNodeGroup(treeNodeGroup) {
      for (var i in treeNodeGroup) {
        let node = treeNodeGroup[i]
        if (groups[node.id]) {
          node.children = groups[node.id]
          groups[node.id] = null // [SAFEGUARD]防止自为父节点或互为父节点（有环图结构）导致的死循环
          traverseTreeNodeGroup(node.children)
        } else {
        }
        //选择默认展开的节点
        if (node.pid == treeRootId) {
          expandRowKeys.push(node.id)
        } else {
        }
      }
    }

    traverseTreeNodeGroup(rootNodes)

    return {data: rootNodes, expandRowKeys: expandRowKeys}
  },

  //转化为树状结构 大写pId
  TreeDataPId(nodes, treeRootId) {
    for (let i = 0; i < nodes.length; i++) {
      if (nodes[i].pId == treeRootId) {
        break
      } else if (i == nodes.length - 1) {
        Message.closeAll()
        Message({
          message: '数据格式错误',
          type: 'error',
          duration: 2 * 1000
        })
      } else {
      }
    }

    let nodesFilters = nodes

    let groups = {}
    //默认选中的节点
    let expandRowKeys = []
    // 按父节点将节点分组
    for (var i in nodesFilters) {
      if (!groups[nodesFilters[i].pId]) {
        groups[nodesFilters[i].pId] = []
      }
      groups[nodesFilters[i].pId].push(nodesFilters[i])
      if (treeRootId && treeRootId === nodesFilters[i].id) {
        // 发现传入的根节点id作为节点id时，将根节点设置为该节点的父节点
        treeRootId = nodesFilters[i].pId
      }
    }

    var rootNodes = groups[treeRootId]
    groups[treeRootId] = null // [SAFEGUARD]防止自为父节点或互为父节点（有环图结构）导致的死循环
    function traverseTreeNodeGroup(treeNodeGroup) {
      for (var i in treeNodeGroup) {
        var node = treeNodeGroup[i]
        node.label = node.name
        node.value = node.id
        if (groups[node.id]) {
          node.children = groups[node.id]
          groups[node.id] = null // [SAFEGUARD]防止自为父节点或互为父节点（有环图结构）导致的死循环
          traverseTreeNodeGroup(node.children)
        } else {
        }
        //选择默认展开的节点
        if (node.pId == treeRootId) {
          expandRowKeys.push(node.id)
        } else {
        }
      }
    }

    traverseTreeNodeGroup(rootNodes)

    return {data: rootNodes, expandRowKeys: expandRowKeys}
  },
  // 查询比对对应的值 获取树形数据对应字段的值
  // 数据 比对的是那个字段 查询比对的值  取值的是那个字段  树层结构的children字段的key
  getTreeOppositeValue(data, compare, id, evaluation, children) {
    // 需要的值
    let value = ''
    for (let i = 0; i < data.length; i++) {
      if (data[i][compare] == id) {
        value = data[i][evaluation]
        break
      } else if (
        data[i][children] !== null &&
        data[i][children] !== undefined &&
        data[i][children].length > 0
      ) {
        function getRoutersExternalChildUrl(subData, subCompare, subId, subEvaluation, subChildren) {
          // 子级的 数据 比对的是那个字段 查询比对的值  取值的是那个字段  树层结构的children字段的key
          for (let j = 0; j < subData.length; j++) {
            if (subData[j][subCompare] == subId) {
              value = subData[j][subEvaluation]
              break
            } else if (
              subData[j][subChildren] !== null &&
              subData[j][subChildren] !== undefined &&
              subData[j][subChildren].length > 0
            ) {
              getRoutersExternalChildUrl(
                subData[j][subChildren],
                subCompare,
                subId,
                subEvaluation,
                subChildren
              ) //回调
            }
          }
        }

        getRoutersExternalChildUrl(data[i][children], compare, id, evaluation, children)
      } else {
      }
    }
    return value
  },
  // 菜单添加待办任务数量
  // 查询比对对应的值 改变树形数据对应字段的值 限制于添加到该字段后边
  // 数据 比对的是那个字段 查询比对的值  要添加的字段值  树层结构的children字段的key
  changeTreeOppositeValue(data, compare, id, addString, children) {
    for (let i = 0; i < data.length; i++) {
      if (data[i][compare] == id) {
        if (data[i].meta) {
          data[i].meta.tasksNum = addString
        }
      } else if (
        data[i][children] !== null &&
        data[i][children] !== undefined &&
        data[i][children].length > 0
      ) {
        function getRoutersExternalChildUrl(subData, subCompare, subId, subAddString, subChildren) {
          // 子级的 数据 比对的是那个字段 查询比对的值  改变的是那个字段  要添加字段的是值 树层结构的children字段的key
          for (let j = 0; j < subData.length; j++) {
            if (subData[j][subCompare] == subId) {
              if (subData[j].meta) {
                subData[j].meta.tasksNum = subAddString
              }
            } else if (
              subData[j][subChildren] !== null &&
              subData[j][subChildren] !== undefined &&
              subData[j][subChildren].length > 0
            ) {
              getRoutersExternalChildUrl(
                subData[j][subChildren],
                subCompare,
                subId,
                subAddString,
                subChildren
              ) //回调
            }
          }
        }

        getRoutersExternalChildUrl(data[i][children], compare, id, addString, children)
      } else {
      }
    }
    return data
  },
  //vm iframe 地址
  file_vm_src(templateCode, beginDate, endDate, fundCode) {
    return (
      process.env.BASE_API +
      '/rest/report/interview.do?templateCode=' +
      templateCode +
      '&beginDate=' +
      beginDate +
      '&endDate=' +
      endDate +
      '&fundCode=' +
      fundCode +
      '&token=' +
      encodeURIComponent(getToken()) +
      '&autoRun=false&ajaxRun=true&showParam=true&markFlag=false&srcSuffix=' +
      process.env.BASE_API +
      '&time=' +
      new Date().getTime()
    )
  },
  //vm iframe 地址
  file_vmremark_src(templateCode, startDate, endDate, productCodes, baseCode, kpiCode) {
    return (
      process.env.BASE_API +
      '/rest/report/interview.do?templateCode=' +
      templateCode +
      '&startDate=' +
      startDate +
      '&endDate=' +
      endDate +
      '&productCodes=' +
      productCodes +
      '&baseCode=' +
      baseCode +
      '&kpiCode=' +
      kpiCode +
      '&token=' +
      encodeURIComponent(getToken()) +
      '&autoRun=false&ajaxRun=true&showParam=true&showCondition=false&markFlag=false&srcSuffix=' +
      process.env.BASE_API +
      '&time=' +
      new Date().getTime()
    )
  },
  // vm文件下载
  file_vm_download(templateCode, beginDate, endDate, fundCode) {
    //   ?templateCode=B6BB3CB840804B9EAB57766F403D79C2&beginDate=2018-12-01&endDate=2018-12-31&fundCode=100010&token=vXcx3IBemn1kShhobK2DfpY3kFqiBaSb
    function download(src, templateCode, beginDate, endDate, fundCode, token) {
      var iframe = $("<iframe name='file_iframe'></iframe>")
      iframe.attr('style', 'display:none') //下面为在form表单中添加查询参数

      var form = $("<form submit = 'return false'></form>") //定义一个form表单

      form.attr('style', 'display:none') //下面为在form表单中添加查询参数

      form.attr('target', 'file_iframe')

      form.attr('method', 'get')

      form.attr('action', src)
      //模板编码
      var input1 = $('<input>')

      input1.attr('type', 'hidden')

      input1.attr('name', 'templateCode')

      input1.attr('value', templateCode)
      //开始时间
      var input2 = $('<input>')

      input2.attr('type', 'hidden')

      input2.attr('name', 'beginDate')

      input2.attr('value', beginDate)
      //结束时间
      var input3 = $('<input>')

      input3.attr('type', 'hidden')

      input3.attr('name', 'endDate')

      input3.attr('value', endDate)
      //组合代码
      var input4 = $('<input>')

      input4.attr('type', 'hidden')

      input4.attr('name', 'fundCode')

      input4.attr('value', fundCode)
      //token
      var input5 = $('<input>')

      input5.attr('type', 'hidden')

      input5.attr('name', 'token')

      input5.attr('value', token)

      $('body').append(iframe) //将表单放置在web中

      iframe.append(form)

      form.append(input1, input2, input3, input4, input5) //将查询参数控件提交到表单上

      form.submit()
    }

    let token = getToken()
    download(
      process.env.BASE_API + '/rest/report/export.do',
      templateCode,
      beginDate,
      endDate,
      fundCode,
      token
    )
  },
  //后端排序公共方法
  orderByString(val) {
    //排序字段
    let orderBy = ''
    let isAsc = ''
    let returnData = ''
    let label = val.prop.split('.')
    if (label.length == 2) {
      orderBy = label[1]
    } else {
      orderBy = label[0]
    }
    //正序 倒序列
    if (val.order == 'ascending') {
      isAsc = 'asc'
      returnData = '"' + orderBy + '" ' + isAsc + ' nulls last'
    } else if (val.order == 'descending') {
      isAsc = 'desc'
      returnData = '"' + orderBy + '" ' + isAsc + ' nulls last'
    } else {
      returnData = ''
    }
    return returnData
  },
  //后端排序 动态算
  moveOrderByString(val) {
    let obj = {
      orderBy: '',
      isAsc: ''
    }
    //排序字段
    let label = val.prop.split('.')
    if (label.length == 2) {
      obj.orderBy = label[1]
    } else {
      obj.orderBy = label[0]
    }
    //正序 倒序列
    if (val.order == 'ascending') {
      obj.isAsc = true
    } else if (val.order == 'descending') {
      obj.isAsc = false
    } else {
      obj.isAsc = true
      obj.orderBy = ''
    }
    return obj
  },
  // 列表排序值处理
  queryOrderBy(val) {
    let orderBy = ''
    if (val.order === 'ascending') {
      orderBy = `"${val.prop}" nulls last` // 升序
    } else if (val.order === 'descending') {
      orderBy = `"${val.prop}" desc nulls last` // 降序
    } else {
      orderBy = ''
    }
    return orderBy
  },

  commonDownloadUrl(id) {
    function download(src, id, token) {
      var iframe = $("<iframe name='file_iframe'></iframe>")
      iframe.attr('style', 'display:none') //下面为在form表单中添加查询参数

      var form = $("<form submit = 'return false'></form>") //定义一个form表单

      form.attr('style', 'display:none') //下面为在form表单中添加查询参数

      form.attr('target', 'file_iframe')

      form.attr('method', 'get')

      form.attr('action', src)
      //文件id
      var input1 = $('<input>')

      input1.attr('type', 'hidden')

      input1.attr('name', 'id')

      input1.attr('value', id)
      //token
      var input2 = $('<input>')

      input2.attr('type', 'hidden')

      input2.attr('name', 'token')

      input2.attr('value', token)

      $('body').append(iframe) //将表单放置在web中

      iframe.append(form)

      form.append(input1, input2) //将查询参数控件提交到表单上

      form.submit()
    }

    let token = getToken()
    download(process.env.BASE_API + `/api/system/v1.0/file/download/${id}`, id, token)
  },
  //投委会文件下载
  touweihuiDownloadUrl(fileName, filePath) {
    // 如果存在名字和路径再下载
    if (fileName) {
      if (filePath) {
        function download(src, fileName, filePath, token) {
          var iframe = $("<iframe name='file_iframe'></iframe>")
          iframe.attr('style', 'display:none') //下面为在form表单中添加查询参数

          var form = $("<form submit = 'return false'></form>") //定义一个form表单

          form.attr('style', 'display:none') //下面为在form表单中添加查询参数

          form.attr('target', 'file_iframe')

          form.attr('method', 'get')

          form.attr('action', src)
          //文件fileName
          var input1 = $('<input>')

          input1.attr('type', 'hidden')

          input1.attr('name', 'fileName')

          input1.attr('value', fileName)
          // 文件filePath
          var input2 = $('<input>')

          input2.attr('type', 'hidden')

          input2.attr('name', 'filePath')

          input2.attr('value', filePath)
          //token
          var input3 = $('<input>')

          input3.attr('type', 'hidden')

          input3.attr('name', 'token')

          input3.attr('value', token)

          $('body').append(iframe) //将表单放置在web中

          iframe.append(form)

          form.append(input1, input2, input3) //将查询参数控件提交到表单上

          form.submit()
        }

        let token = getToken()
        download(
          process.env.BASE_API + '/api/manageView/nvestmentCommittee/touweihui/downloadFile',
          fileName,
          filePath,
          token
        )
      }
    }
  },

  // 以form表单形式下载文件
  formDownloadFile(params, action, method) {
    let iframe = document.createElement('iframe')
    iframe.id = 'iframe'
    iframe.name = 'iframe'
    iframe.style.display = 'none'
    document.body.appendChild(iframe)
    let form = document.createElement('form')
    form.id = 'form'
    form.name = 'form' // 最好唯一
    iframe.appendChild(form)
    for (let obj in params) {
      if (params.hasOwnProperty(obj)) {
        let input = document.createElement('input')
        input.tpye = 'hidden'
        input.name = obj
        input.value = params[obj]
        form.appendChild(input)
      }
    }
    form.method = method //请求方式
    form.action = action // 请求地址
    form.enctype = 'application/x-www-form-urlencoded' // 提交使用的编码类型
    form.submit()
    document.body.removeChild(iframe)
  },
  //下载文件倒计时5秒

  // 按钮点击倒计时
  countdownBtn() {
    let timer = null
    let seconds = 5
    return new Promise((resolve, reject) => {
      timer = setTimeout(() => {
        resolve(true)
        clearTimeout(timer)
      }, seconds * 1000)
    })
  },

  // 搜索按钮禁用5秒
  searchButtonDisabled(document, self) {
    let seconds = 5
    self[document] = true
    let timer = setTimeout(() => {
      self[document] = false
      clearTimeout(timer)
    }, seconds * 1000)
  },
  // echarts数据视图样式
  optionToContent(opt, name) {
    let tableName = ''
    if (name) tableName = name
    let axisData = opt.xAxis[0].data //坐标数据
    let series = opt.series //折线图数据
    let tdHeads = `<td  style="padding: 0 10px;min-width: 100px;">${tableName}</td>` //表头
    let tdBodys = '' //数据
    series.forEach(item => {
      //组装表头
      tdHeads += `<td style="padding: 0 10px;min-width: 120px;">${item.name}</td>`
    })
    let table = `<table border="1" style="margin-left:20px;border-collapse:collapse;font-size:14px;text-align:center"><tbody><tr>${tdHeads} </tr>`
    for (let i = 0, l = axisData.length; i < l; i++) {
      for (let j = 0; j < series.length; j++) {
        if (isNaN(series[j].data[i])) {
          series[j].data[i] = 0
        }
        //组装表数据
        tdBodys += `<td>${series[j].data[i]}</td>`
      }
      table += `<tr><td style="padding: 0 10px">${axisData[i]}</td>${tdBodys}</tr>`
      tdBodys = ''
    }
    table += '</tbody></table>'
    return table
  },

  // 加密的公共方法
  encryptByAESCommon(plainText) {
    let key = CryptoJS.enc.Utf8.parse(getToken().replaceAll('-', '').slice(0, 16))
    let encrypted = CryptoJS.AES.encrypt(plainText, key, {
      mode: CryptoJS.mode.ECB,
      padding: CryptoJS.pad.Pkcs7
    })
    // 这里的encrypted不是字符串，而是一个CipherParams对象
    return encrypted.ciphertext.toString(CryptoJS.enc.Base64)
  },

  // 列表排序值处理
  queryOrderBy_vxe_template(val) {
    let orderBy = ''
    if (val.order === 'asc') {
      orderBy = `${val.property} asc` // 升序
    } else if (val.order === 'desc') {
      orderBy = `${val.property} desc` // 降序
    } else {
      orderBy = ''
    }
    return orderBy
  },

  // 请求参数排除无意义的值
  parameterSrc(data) {
    let newData = {}
    for (let key in data) {
      if (data[key] === '' || data[key] === undefined || data[key] === null) {
      } else {
        newData[key] = data[key]
      }
    }
    return newData
  },
  // 请求参数排除无意义的值 除空字符串外
  parameterStringSrc(data) {
    let newData = {}
    for (let key in data) {
      if (data[key] === undefined || data[key] === null) {
      } else {
        newData[key] = data[key]
      }
    }
    return newData
  },

  //vm risk导出为 word文档  新增横版竖版
  fun_exportPDFOption(wordName, wordOption, iframeId, templateCode,fundName,beginDate,endDate) {
    const username = store.getters.name;
    var $export = $(
      document
        .getElementById(iframeId)
        .contentWindow.document.getElementById('outDiv')
    ).clone().find("script").remove().end()
    /*var bit = 0.65//宽度百分比
    var width, height, imgWidth, imgHeight
    var style = document.createElement('style')
    //公司环境：width:90%  浦发环境为width:80%
    style.innerHTML = '.static_tables table{width:90% !important;} .bak{margin-top: 10px;border-collapse: collapse;} .bakBox{margin-left:30px;border: 1px solid #e0e0e1}'
    $export.find('head').each(function (i, o) {
      o.appendChild(style)
    })
    $export.find('.bz_box').each(function (i, o) {
      $(o)
        .parent()
        .attr('class', 'bak')
      $(o)
        .attr('class', 'bakBox')
    })
    $export.find('svg').each(function (i, o) {
      var canvas = document.createElement('canvas')//创建空白canvas
      width = o.getAttribute('width')
      height = o.getAttribute('height')

      imgWidth = width * bit
      imgHeight = height * bit

      var viewBox = '0 0 ' + o.getAttribute('width').toString() + ' ' + o.getAttribute('height').toString()
      width = (width * 1).toFixed(0)
      height = (height * 1).toFixed(0)
      $(o).attr('width', width).attr('height', height).attr('viewBox', viewBox)
      canvas.id = 'canvas' + (i + 1)
      document.body.appendChild(canvas)//将canvas添加到body
      var svgHtml = $(o).parent().html().replace('fill="rgba(0,0,0,0)" fill-opacity="1" stroke="#fff" stroke-width="0" paint-order="fill" stroke-opacity="1"', 'fill="rgb(255,255,255)" fill-opacity="0"')
        .replace('fill="rgba(0,0,0,0)" fill-opacity="1" stroke="#fff" stroke-width="0" paint-order="stroke" stroke-opacity="1"', 'fill="rgb(255,255,255)" fill-opacity="0"').replace('fill="rgba(0,0,0,0)" fill-opacity="1" stroke="#fff" stroke-width="0" paint-order="fill" stroke-opacity="1"', 'fill="rgb(255,255,255)" fill-opacity="0"')
        .replace('fill="rgba(0,0,0,0)" fill-opacity="1" stroke="#fff" stroke-width="0" paint-order="stroke" stroke-opacity="1"', 'fill="rgb(255,255,255)" fill-opacity="0"')//避免导出word出现legend背景为黑色的情况
      try {
        canvg(canvas, svgHtml)//svg转canvas
      } catch (e) {
        console.log(e)
        console.log(o)
      }

      // $(o)
      //   .after('<img src="' + canvas.toDataURL("image/png", 2.0) + '"style="width:' + width + 'px;height:' + height + 'px"/>').remove();
      // $(o)
      //   .after('<img src="' + canvas.toDataURL('image/png') + '" style="width:' + imgWidth + 'px;height:' + imgHeight + 'px"  />').remove()
      $(o)
        .after('<img src="' + canvas.toDataURL('image/png') + '" />').remove()
      $('#canvas' + (i + 1)).remove()
    })*/
    //var aaData = $export.html().split("select").join("");//避免拦截删除select关键字
    var aaData = $export.html()
    var html = '<!DOCTYPE html><html>' + aaData + '</html>'
    html = encryptByAES(html)
    var wkhtmltopdf = ''
    if(document.getElementById(iframeId).contentWindow.document.querySelector('input[name="wkhtmltopdf"]')){
      wkhtmltopdf = document.getElementById(iframeId).contentWindow.document.querySelector('input[name="wkhtmltopdf"]').value
    }
    let BASE_API = process.env.BASE_API
    // let BASE_API = '/ddia'
    let token = encodeURIComponent(getToken())

    // var html=document.getElementById('J_iframe_id').contentWindow.document.getElementsByTagName("html")[0].innerHTML;
    var src = BASE_API + '/rest/report/export.do?token=' + token

    var iframe = $('<iframe name=\'file_iframe\'></iframe>')
    iframe.attr('style', 'display:none') //下面为在form表单中添加查询参数

    var form = $('<form submit = \'return false\'></form>') //定义一个form表单

    form.attr('style', 'display:none') //下面为在form表单中添加查询参数

    form.attr('target', 'file_iframe')

    form.attr('method', 'post')

    form.attr('action', src)
    //模板编码
    var input1 = $('<input>')

    input1.attr('type', 'hidden')

    input1.attr('name', 'fileName')
    // 文件名称
    input1.attr('value', wordName)

    //html 代码
    var input2 = $('<input>')

    input2.attr('type', 'hidden')

    input2.attr('name', 'htmlData')

    input2.attr('value', html)
    //wordOption word相关参数  pagedir导出纵向排版(v)word还是横向排版(h)word
    var input3 = $('<input>')

    input3.attr('type', 'hidden')

    input3.attr('name', 'wordOption')

    input3.attr('value', wordOption)

    var input4 = $('<input>')
    input4.attr('type', 'hidden')
    input4.attr('name', 'templateCode')
    input4.attr('value', templateCode)

    var input5 = $('<input>')
    input5.attr('type', 'hidden')
    input5.attr('name', 'encryArr')
    input5.attr('value', 'htmlData')

    var input6 = $('<input>')
    input6.attr('type', 'hidden')
    input6.attr('name', 'fundName')
    input6.attr('value', fundName)

    var input7 = $('<input>')
    input7.attr('type', 'hidden')
    input7.attr('name', 'beginDate')
    input7.attr('value', beginDate)

    var input8 = $('<input>')
    input8.attr('type', 'hidden')
    input8.attr('name', 'endDate')
    input8.attr('value', endDate)

    var input9 = $('<input>')
    input9.attr('type', 'hidden')
    input9.attr('name', 'wkhtmltopdf')
    input9.attr('value', wkhtmltopdf)

    var input10 = $('<input>')
    input10.attr('type', 'hidden')
    input10.attr('name', 'userName')
    input10.attr('value', username)

    $('body').append(iframe) //将表单放置在web中

    iframe.append(form)

    form.append(input1, input2, input3, input4, input5,input6,input7,input8,input9,input10) //将查询参数控件提交到表单上

    form.submit()
  },

  fun_exportPDFOption_GFJX(wordName, wordOption, iframeId, templateCode,fundCode,fundName,beginDate,endDate,desensitizationFlag,desensitizationFun,covIndexCode) {
    const username = store.getters.name;
    var $export = $(
      document
        .getElementById(iframeId)
        .contentWindow.document.getElementById('outDiv')
    ).clone().find("script").remove().end()
    /*var bit = 0.65//宽度百分比
    var width, height, imgWidth, imgHeight
    var style = document.createElement('style')
    //公司环境：width:90%  浦发环境为width:80%
    style.innerHTML = '.static_tables table{width:90% !important;} .bak{margin-top: 10px;border-collapse: collapse;} .bakBox{margin-left:30px;border: 1px solid #e0e0e1}'
    $export.find('head').each(function (i, o) {
      o.appendChild(style)
    })
    $export.find('.bz_box').each(function (i, o) {
      $(o)
        .parent()
        .attr('class', 'bak')
      $(o)
        .attr('class', 'bakBox')
    })
    $export.find('svg').each(function (i, o) {
      var canvas = document.createElement('canvas')//创建空白canvas
      width = o.getAttribute('width')
      height = o.getAttribute('height')

      imgWidth = width * bit
      imgHeight = height * bit

      var viewBox = '0 0 ' + o.getAttribute('width').toString() + ' ' + o.getAttribute('height').toString()
      width = (width * 1).toFixed(0)
      height = (height * 1).toFixed(0)
      $(o).attr('width', width).attr('height', height).attr('viewBox', viewBox)
      canvas.id = 'canvas' + (i + 1)
      document.body.appendChild(canvas)//将canvas添加到body
      var svgHtml = $(o).parent().html().replace('fill="rgba(0,0,0,0)" fill-opacity="1" stroke="#fff" stroke-width="0" paint-order="fill" stroke-opacity="1"', 'fill="rgb(255,255,255)" fill-opacity="0"')
        .replace('fill="rgba(0,0,0,0)" fill-opacity="1" stroke="#fff" stroke-width="0" paint-order="stroke" stroke-opacity="1"', 'fill="rgb(255,255,255)" fill-opacity="0"').replace('fill="rgba(0,0,0,0)" fill-opacity="1" stroke="#fff" stroke-width="0" paint-order="fill" stroke-opacity="1"', 'fill="rgb(255,255,255)" fill-opacity="0"')
        .replace('fill="rgba(0,0,0,0)" fill-opacity="1" stroke="#fff" stroke-width="0" paint-order="stroke" stroke-opacity="1"', 'fill="rgb(255,255,255)" fill-opacity="0"')//避免导出word出现legend背景为黑色的情况
      try {
        canvg(canvas, svgHtml)//svg转canvas
      } catch (e) {
        console.log(e)
        console.log(o)
      }

      // $(o)
      //   .after('<img src="' + canvas.toDataURL("image/png", 2.0) + '"style="width:' + width + 'px;height:' + height + 'px"/>').remove();
      // $(o)
      //   .after('<img src="' + canvas.toDataURL('image/png') + '" style="width:' + imgWidth + 'px;height:' + imgHeight + 'px"  />').remove()
      $(o)
        .after('<img src="' + canvas.toDataURL('image/png') + '" />').remove()
      $('#canvas' + (i + 1)).remove()
    })*/
    //var aaData = $export.html().split("select").join("");//避免拦截删除select关键字
    var aaData = $export.html()
    var html = '<!DOCTYPE html><html>' + aaData + '</html>'
    html = encryptByAES(html)
    var wkhtmltopdf = ''
    if(document.getElementById(iframeId).contentWindow.document.querySelector('input[name="wkhtmltopdf"]')){
      wkhtmltopdf = document.getElementById(iframeId).contentWindow.document.querySelector('input[name="wkhtmltopdf"]').value
    }
    let BASE_API = process.env.BASE_API
    // let BASE_API = '/ddia'
    let token = encodeURIComponent(getToken())

    // var html=document.getElementById('J_iframe_id').contentWindow.document.getElementsByTagName("html")[0].innerHTML;
    var src = BASE_API + '/rest/report/export.do?token=' + token

    var iframe = $('<iframe name=\'file_iframe\'></iframe>')
    iframe.attr('style', 'display:none') //下面为在form表单中添加查询参数

    var form = $('<form submit = \'return false\'></form>') //定义一个form表单

    form.attr('style', 'display:none') //下面为在form表单中添加查询参数

    form.attr('target', 'file_iframe')

    form.attr('method', 'post')

    form.attr('action', src)
    //模板编码
    var input1 = $('<input>')

    input1.attr('type', 'hidden')

    input1.attr('name', 'fileName')
    // 文件名称
    input1.attr('value', wordName)

    //html 代码
    var input2 = $('<input>')

    input2.attr('type', 'hidden')

    input2.attr('name', 'htmlData')

    input2.attr('value', html)
    //wordOption word相关参数  pagedir导出纵向排版(v)word还是横向排版(h)word
    var input3 = $('<input>')

    input3.attr('type', 'hidden')

    input3.attr('name', 'wordOption')

    input3.attr('value', wordOption)

    var input4 = $('<input>')
    input4.attr('type', 'hidden')
    input4.attr('name', 'templateCode')
    input4.attr('value', templateCode)

    var input5 = $('<input>')
    input5.attr('type', 'hidden')
    input5.attr('name', 'encryArr')
    input5.attr('value', 'htmlData')

    var input6 = $('<input>')
    input6.attr('type', 'hidden')
    input6.attr('name', 'fundName')
    input6.attr('value', fundName)

    var input7 = $('<input>')
    input7.attr('type', 'hidden')
    input7.attr('name', 'beginDate')
    input7.attr('value', beginDate)

    var input8 = $('<input>')
    input8.attr('type', 'hidden')
    input8.attr('name', 'endDate')
    input8.attr('value', endDate)

    // var input9 = $('<input>')
    // input9.attr('type', 'hidden')
    // input9.attr('name', 'wkhtmltopdf')
    // input9.attr('value', wkhtmltopdf)

    var input10 = $('<input>')
    input10.attr('type', 'hidden')
    input10.attr('name', 'desensitizationFlag')
    input10.attr('value', desensitizationFlag)

    var input11 = $('<input>')
    input11.attr('type', 'hidden')
    input11.attr('name', 'desensitizationFun')
    input11.attr('value', desensitizationFun)

    var input12 = $('<input>')
    input12.attr('type', 'hidden')
    input12.attr('name', 'fundCode')
    input12.attr('value', fundCode)

    var input13 = $('<input>')
    input13.attr('type', 'hidden')
    input13.attr('name', 'covIndexCode')
    input13.attr('value', covIndexCode)

    var input14 = $('<input>')
    input14.attr('type', 'hidden')
    input14.attr('name', 'userName')
    input14.attr('value', username)

    $('body').append(iframe) //将表单放置在web中

    iframe.append(form)

    form.append(input1, input2, input3, input4, input5,input6,input7,input8,input10,input11,input12,input13,input14) //将查询参数控件提交到表单上

    form.submit()
  },

  fun_exportPDFOption_GFJX_new(
    wordName,
    wordOption,
    iframeId,
    templateCode,
    fundCode,
    fundName,
    beginDate,
    endDate,
    desensitizationFlag,
    desensitizationFun,
    dataFreqOpen,
    dataFreq,
    benchmarks,
    benchmarkA,
    benchmarkB,
    benchmarkAValue,
    benchmarkBValue,
    covIndexCode,
    successCallback,
    errorCallback
  ) {
    const result = {
      success: false,
      message: ''
    };

    const params = new URLSearchParams();
    params.append('fileName', wordName || '报告.pdf');
    params.append('templateCode', templateCode || '');
    params.append('fundCode', fundCode || '');
    params.append('fundName', fundName || '');
    params.append('beginDate', beginDate || '');
    params.append('endDate', endDate || '');
    params.append('desensitizationFlag', desensitizationFlag || '');
    params.append('desensitizationFun', desensitizationFun || '');
    params.append('dataFreqOpen', dataFreqOpen || '');
    params.append('dataFreq', dataFreq || '');
    params.append('benchmarks', benchmarks || '');
    params.append('benchmarkA', benchmarkA || '');
    params.append('benchmarkB', benchmarkB || '');
    params.append('benchmarkAValue', benchmarkAValue || '');
    params.append('benchmarkBValue', benchmarkBValue || '');
    params.append('covIndexCode', covIndexCode || '');
    params.append('wordOption', wordOption || JSON.stringify({ pagedir: 'h' }));
    params.append('encryArr', 'htmlData');
    params.append('token', encodeURIComponent(getToken() || ''));

    let html = '';
    try {
      const iframeEl = document.getElementById(iframeId);
      if (!iframeEl) throw new Error(`未找到iframe（ID：${iframeId}）`);
      if (!iframeEl.contentWindow || !iframeEl.contentWindow.document) {
        throw new Error(`iframe（${iframeId}）内容未加载`);
      }
      const outDivEl = iframeEl.contentWindow.document.getElementById('outDiv');
      if (!outDivEl) throw new Error(`iframe内未找到outDiv元素`);

      const $export = $(outDivEl).clone().find("script").remove().end();
      const aaData = $export.html() || '';
      html = '<!DOCTYPE html><html>' + aaData + '</html>';
    } catch (domErr) {
      console.error('【导出PDF】DOM获取失败：', domErr);
      html = '<!DOCTYPE html><html><body>暂无报告数据</body></html>';
      result.message = '报告内容获取异常，将尝试导出基础模板';
    }

    let encryptHtml = '';
    try {
      encryptHtml = encryptByAES(html);
    } catch (encryptErr) {
      console.error('【导出PDF】加密失败：', encryptErr);
      encryptHtml = html;
      result.message = '内容加密失败，将尝试明文导出';
    }
    params.append('htmlData', encryptHtml);

    const baseApi = process.env.BASE_API || window.location.origin;
    const requestUrl = `${baseApi}/rest/report/export.do`;

    fetch(requestUrl, {
      method: 'POST',
      body: params,
      credentials: 'include',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
      }
    })
      .then(response => {
        if (!response.ok) throw new Error(`接口异常：${response.status}`);
        return response.blob();
      })
      .then(blob => {
        // 下载逻辑不变
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = wordName || '报告.pdf';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);

        result.success = true;
        result.message = 'PDF导出成功，文件已下载';
        typeof successCallback === 'function' && successCallback(result);
      })
      .catch(error => {
        console.error('【导出PDF】请求失败：', error);
        result.success = false;
        result.message = `PDF导出失败：${error.message}`;
        typeof errorCallback === 'function' && errorCallback(result);
      });

    return result;
  },
  //策略报告导出
  fun_exportPDFOption_GFJX_STRA(wordName, wordOption, iframeId, templateCode,beginDate,endDate,freq) {
    const username = store.getters.name;
    var $export = $(
      document
        .getElementById(iframeId)
        .contentWindow.document.getElementById('outDiv')
    ).clone().find("script").remove().end()

    var aaData = $export.html()
    var html = '<!DOCTYPE html><html>' + aaData + '</html>'
    html = encryptByAES(html)
    var wkhtmltopdf = ''
    if(document.getElementById(iframeId).contentWindow.document.querySelector('input[name="wkhtmltopdf"]')){
      wkhtmltopdf = document.getElementById(iframeId).contentWindow.document.querySelector('input[name="wkhtmltopdf"]').value
    }
    let BASE_API = process.env.BASE_API
    // let BASE_API = '/ddia'
    let token = encodeURIComponent(getToken())

    // var html=document.getElementById('J_iframe_id').contentWindow.document.getElementsByTagName("html")[0].innerHTML;
    var src = BASE_API + '/rest/report/export.do?token=' + token

    var iframe = $('<iframe name=\'file_iframe\'></iframe>')
    iframe.attr('style', 'display:none') //下面为在form表单中添加查询参数

    var form = $('<form submit = \'return false\'></form>') //定义一个form表单

    form.attr('style', 'display:none') //下面为在form表单中添加查询参数

    form.attr('target', 'file_iframe')

    form.attr('method', 'post')

    form.attr('action', src)
    //模板编码
    var input1 = $('<input>')

    input1.attr('type', 'hidden')

    input1.attr('name', 'fileName')
    // 文件名称
    input1.attr('value', wordName)

    //html 代码
    var input2 = $('<input>')

    input2.attr('type', 'hidden')

    input2.attr('name', 'htmlData')

    input2.attr('value', html)
    //wordOption word相关参数  pagedir导出纵向排版(v)word还是横向排版(h)word
    var input3 = $('<input>')

    input3.attr('type', 'hidden')

    input3.attr('name', 'wordOption')

    input3.attr('value', wordOption)

    var input4 = $('<input>')
    input4.attr('type', 'hidden')
    input4.attr('name', 'templateCode')
    input4.attr('value', templateCode)

    var input5 = $('<input>')
    input5.attr('type', 'hidden')
    input5.attr('name', 'encryArr')
    input5.attr('value', 'htmlData')


    var input7 = $('<input>')
    input7.attr('type', 'hidden')
    input7.attr('name', 'beginDate')
    input7.attr('value', beginDate)

    var input8 = $('<input>')
    input8.attr('type', 'hidden')
    input8.attr('name', 'endDate')
    input8.attr('value', endDate)

    // var input9 = $('<input>')
    // input9.attr('type', 'hidden')
    // input9.attr('name', 'wkhtmltopdf')
    // input9.attr('value', wkhtmltopdf)

    var input10 = $('<input>')
    input10.attr('type', 'hidden')
    input10.attr('name', 'freq')
    input10.attr('value', freq)


    var input14 = $('<input>')
    input14.attr('type', 'hidden')
    input14.attr('name', 'userName')
    input14.attr('value', username)

    $('body').append(iframe) //将表单放置在web中

    iframe.append(form)

    form.append(input1, input2, input3, input4, input5,input7,input8,input10,input14) //将查询参数控件提交到表单上

    form.submit()
  },

}

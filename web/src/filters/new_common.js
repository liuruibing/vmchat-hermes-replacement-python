

import $ from 'jquery';                   
import moment from 'moment'
import BpmnViewer from 'bpmn-js';
import { Message } from 'element-ui'
 //乘法
 function accMul (arg1, arg2) {
  var m = 0, s1 = Number(arg1).toString(), s2 = Number(arg2).toString();
  try {
    m += s1.split(".")[1].length;
  }
  catch (e) {
  }
  try {
    m += s2.split(".")[1].length;
  }
  catch (e) {
  }
  return Number(s1.replace(".", "")) * Number(s2.replace(".", "")) / Math.pow(10, m);
}
// 除法
function accDiv(arg1, arg2) {
  var t1 = 0, t2 = 0, r1, r2;
  try { t1 = Number(arg1).toString().split(".")[1].length } catch (e) { }
  try { t2 = Number(arg2).toString().split(".")[1].length } catch (e) { }
  r1 = Number(arg1.toString().replace(".", ""))
  r2 = Number(arg2.toString().replace(".", ""))
  return (r1 / r2) * Math.pow(10, t2 - t1);
}

export default {

  // 时间转化为时间戳
  un_timestampToTime(timestamp) {
    var date = new Date(timestamp);
    var time1 = date.getTime();
    // var time2 = date.valueOf();
    // var time3 = Date.parse(date);
    // console.log(time1);//1398250549123
    // console.log(time2);//1398250549123
    // console.log(time3);//1398250549000 精确到毫秒
    return time1;
  },
  // 时间戳年月日
  yyr_timestampToTime(timestamp) {
    var now = new Date(timestamp),
      y = now.getFullYear(),
      m = now.getMonth() + 1,
      d = now.getDate();
    return y + "-" + (m < 10 ? "0" + m : m) + "-" + (d < 10 ? "0" + d : d);
  },
  // 返回当前月份
  yyr_getMonth(timestamp) {
    var now = new Date(timestamp),
      y = now.getFullYear(),
      m = now.getMonth() + 1,
      d = now.getDate();
    return m;
  },
  // 返回当前年份
  yyr_getYear(timestamp) {
    var now = new Date(timestamp),
      y = now.getFullYear(),
      m = now.getMonth() + 1,
      d = now.getDate();
    return y;
  },
// 时间戳
  timestampToTime(timestamp) {
    var now = new Date(timestamp),
      y = now.getFullYear(),
      m = now.getMonth() + 1,
      d = now.getDate();
    return y + "-" + (m < 10 ? "0" + m : m) + "-" + (d < 10 ? "0" + d : d) + " " + now.toTimeString().substr(0, 8);
  },
  // 时间戳减运算
  timestampToTime_add(timestamp, days) {
    var day = parseInt(days);


    var now = timestamp + 24 * 60 * 60 * 1000 * day;

    return now;

  },
  //获取当前时间戳n年前的时间
  yearTimetampToTime_before(presentTime, n) {
    var curDate = presentTime;
    var fourYearsTime = 365 * n * 24 * 60 * 60 * 1000;
    var result = curDate + fourYearsTime;
    var resultDate = new Date(result);
    var year = resultDate.getFullYear();
    var month = resultDate.getMonth() + 1;
    var day = resultDate.getDate();

    var date = new Date(year + "-" + month + "-" + day);

    var time1 = date.getTime();

    return time1;

  },
  //获取当前时间戳n天前的时间
  DayTimetampToTime_before(presentTime, n) {
    var curDate = presentTime;
    var fourYearsTime = n * 24 * 60 * 60 * 1000;
    var result = curDate + fourYearsTime;
    var resultDate = new Date(result);
    var year = resultDate.getFullYear();
    var month = resultDate.getMonth() + 1;
    var day = resultDate.getDate();

    var date = new Date(year + "-" + month + "-" + day);

    var time1 = date.getTime();

    return time1;

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
      year2 =
        parseInt(year2) -
        parseInt(month2 / 12 == 0 ? 1 : Math.abs(parseInt(month2 / 12)) + 1)
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
      year2 = parseInt(year2) + parseInt((parseInt(month2) / 12 == 0 ? 1 : parseInt(month2) / 12));
      month2 = parseInt(month2) % 12;
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
    var now = new Date();
    var year = now.getFullYear();
    var month = now.getMonth() + 1;
    if (month < 10) {
      month = "0" + month;
    }
    var date = now.getDate();
    if (date < 10) {
      date = "0" + date;
    }

    return year + "-" + month + "-" + date;
  },
  // 时分秒
  hhmmss() {
    var myDate = new Date();
    var Hours = myDate.getHours();
    var Minutes = myDate.getMinutes();
    var Seconds = myDate.getSeconds();
    return ' ' + (Hours < 10 ? "0" + Hours : Hours) + ':' + (Minutes < 10 ? "0" + Minutes : Minutes) + ':' + (Seconds < 10 ? "0" + Seconds : Seconds)
  },
  // 非数据判断转换
  abnormalityData(val) {
    if (val === undefined || val === null) {
      return '';
    }
    else {
      return val;
    }
  },
  //日期时间段快捷选项
  dateShortcut() {
    const pickerOptions = {
      shortcuts: [{
        text: '本周',
        onClick(picker) {
          const end = moment().subtract(1, 'days').format('YYYY-MM-DD');
          const start = moment(end).isoWeekday(1).format('YYYY-MM-DD');
          picker.$emit('pick', [start, end]);
        }
      }, {
        text: '本月',
        onClick(picker) {
          const end = moment().subtract(1, 'days').format('YYYY-MM-DD');
          const start = moment([moment(end).year(), 0, 1]).month(moment(end).month()).format("YYYY-MM-DD");
          picker.$emit('pick', [start, end]);
        }
      }, {
        text: '本季度',
        onClick(picker) {
          const end = moment().subtract(1, 'days').format('YYYY-MM-DD');
          const start = moment(moment(end).year() + '-01-01').quarter(moment(end).quarter()).format('YYYY-MM-DD');
          picker.$emit('pick', [start, end]);
        }
      }, {
        text: '今年以来',
        onClick(picker) {
          const end = moment().subtract(1, 'days').format('YYYY-MM-DD');
          const start = moment(end).year() + '-01-01';
          picker.$emit('pick', [start, end]);
        }
      }, {
        text: '去年',
        onClick(picker) {
          const end = moment().year() - 1 + '-12-31';
          const start = moment().year() - 1 + '-01-01';
          picker.$emit('pick', [start, end]);
        }
      }, {
        text: '最近一个月',
        onClick(picker) {
          const end = moment().subtract(1, 'days').format('YYYY-MM-DD');
          const start = moment(moment(end).subtract(1, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD');
          picker.$emit('pick', [start, end]);
        }
      }, {
        text: '最近三个月',
        onClick(picker) {
          const end = moment().subtract(1, 'days').format('YYYY-MM-DD');
          const start = moment(moment(end).subtract(3, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD');
          picker.$emit('pick', [start, end]);
        }
      },
        {
          text: '最近半年',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD');
            const start = moment(moment(end).subtract(6, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD');
            picker.$emit('pick', [start, end]);
          }
        },
        {
          text: '最近一年',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD');
            const start = moment(moment(end).subtract(1, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD');
            picker.$emit('pick', [start, end]);
          }
        },
      ]
    };
    return pickerOptions;
  },
  //日期时间段快捷选项yyyyMMdd
  yyyyMMdddateShortcut() {
    const pickerOptions = {
      shortcuts: [{
        text: '本周',
        onClick(picker) {
          const end = moment().subtract(1, 'days').format('YYYYMMDD');
          const start = moment(end).isoWeekday(1).format('YYYYMMDD');
          picker.$emit('pick', [start, end]);
        }
      }, {
        text: '本月',
        onClick(picker) {
          const end = moment().subtract(1, 'days').format('YYYYMMDD');
          const start = moment([moment(end).year(), 0, 1]).month(moment(end).month()).format("YYYYMMDD");
          picker.$emit('pick', [start, end]);
        }
      }, {
        text: '本季度',
        onClick(picker) {
          const end = moment().subtract(1, 'days').format('YYYYMMDD');
          const start = moment(moment(end).year() + '0101').quarter(moment(end).quarter()).format('YYYYMMDD');
          picker.$emit('pick', [start, end]);
        }
      }, {
        text: '今年以来',
        onClick(picker) {
          const end = moment().subtract(1, 'days').format('YYYYMMDD');
          const start = moment(end).year() + '0101';
          picker.$emit('pick', [start, end]);
        }
      }, {
        text: '去年',
        onClick(picker) {
          const end = moment().year() - 1 + '1231';
          const start = moment().year() - 1 + '0101';
          picker.$emit('pick', [start, end]);
        }
      }, {
        text: '最近一个月',
        onClick(picker) {
          const end = moment().subtract(1, 'days').format('YYYYMMDD');
          const start = moment(moment(end).subtract(1, 'month').format('YYYYMMDD')).subtract(-1, 'days').format('YYYYMMDD');
          picker.$emit('pick', [start, end]);
        }
      }, {
        text: '最近三个月',
        onClick(picker) {
          const end = moment().subtract(1, 'days').format('YYYYMMDD');
          const start = moment(moment(end).subtract(3, 'month').format('YYYYMMDD')).subtract(-1, 'days').format('YYYYMMDD');
          picker.$emit('pick', [start, end]);
        }
      },
      {
        text: '最近半年',
        onClick(picker) {
          const end = moment().subtract(1, 'days').format('YYYYMMDD');
          const start = moment(moment(end).subtract(6, 'month').format('YYYYMMDD')).subtract(-1, 'days').format('YYYYMMDD');
          picker.$emit('pick', [start, end]);
        }
      },
      {
        text: '最近一年',
        onClick(picker) {
          const end = moment().subtract(1, 'days').format('YYYYMMDD');
          const start = moment(moment(end).subtract(1, 'years').format('YYYYMMDD')).subtract(-1, 'days').format('YYYYMMDD');
          picker.$emit('pick', [start, end]);
        }
      },
      ]
    };
    return pickerOptions;
  },
  //日期时间点快捷选项
  dateShortDot() {
    const pickerOptions = {
      shortcuts: [
        {
          text: '今天',
          onClick(picker) {
            const start = new Date();
            picker.$emit('pick', start);
          }
        },
        {
          text: 'T - 1',
          onClick(picker) {
            const start = moment().subtract(1, 'days').format('YYYY-MM-DD');
            picker.$emit('pick', start);
          }
        },
        {
          text: '一月前',
          onClick(picker) {
            const start = moment(moment(new Date()).subtract(1, 'month').format('YYYY-MM-DD')).subtract(0, 'days').format('YYYY-MM-DD');
            picker.$emit('pick', start);
          }
        }, {
          text: '三月前',
          onClick(picker) {
            const start = moment(moment(new Date()).subtract(3, 'month').format('YYYY-MM-DD')).subtract(0, 'days').format('YYYY-MM-DD');
            picker.$emit('pick', start);
          }
        },
        {
          text: '半年前',
          onClick(picker) {
            const start = moment(moment(new Date()).subtract(6, 'month').format('YYYY-MM-DD')).subtract(0, 'days').format('YYYY-MM-DD');
            picker.$emit('pick', start);
          }
        },
        {
          text: '一年前',
          onClick(picker) {
            const start = moment(moment(new Date()).subtract(1, 'years').format('YYYY-MM-DD')).subtract(0, 'days').format('YYYY-MM-DD');
            picker.$emit('pick', start);
          }
        },
      ]
    };
    return pickerOptions;
  },

  // 加法
  accAdd(arg1, arg2) {
    var r1, r2, m, c;
    try {
      r1 = Number(arg1).toString().split(".")[1].length;
    }
    catch (e) {
      r1 = 0;
    }
    try {
      r2 = Number(arg2).toString().split(".")[1].length;
    }
    catch (e) {
      r2 = 0;
    }
    c = Math.abs(r1 - r2);
    m = Math.pow(10, Math.max(r1, r2));
    if (c > 0) {
      var cm = Math.pow(10, c);
      if (r1 > r2) {
        arg1 = Number(arg1.toString().replace(".", ""));
        arg2 = Number(arg2.toString().replace(".", "")) * cm;
      } else {
        arg1 = Number(arg1.toString().replace(".", "")) * cm;
        arg2 = Number(arg2.toString().replace(".", ""));
      }
    } else {
      arg1 = Number(arg1.toString().replace(".", ""));
      arg2 = Number(arg2.toString().replace(".", ""));
    }
    return (arg1 + arg2) / m;
  },

  // 减法
  accSub(arg1, arg2) {
    var r1, r2, m, n;
    try {
      r1 = Number(arg1).toString().split(".")[1].length;
    }
    catch (e) {
      r1 = 0;
    }
    try {
      r2 = Number(arg2).toString().split(".")[1].length;
    }
    catch (e) {
      r2 = 0;
    }
    m = Math.pow(10, Math.max(r1, r2)); //last modify by deeka //动态控制精度长度
    n = (r1 >= r2) ? r1 : r2;
    return Number(((arg1 * m - arg2 * m) / m).toFixed(n));
  },

  // 乘法
  accMul(arg1, arg2) {
    var m = 0, s1 = Number(arg1).toString(), s2 = Number(arg2).toString();
    try {
      m += s1.split(".")[1].length;
    }
    catch (e) {
    }
    try {
      m += s2.split(".")[1].length;
    }
    catch (e) {
    }
    return Number(s1.replace(".", "")) * Number(s2.replace(".", "")) / Math.pow(10, m);
  },

  // 除法
  accDiv(arg1, arg2) {
    var t1 = 0, t2 = 0, r1, r2;
    try {
      t1 = Number(arg1).toString().split(".")[1].length
    } catch (e) {
    }
    try {
      t2 = Number(arg2).toString().split(".")[1].length
    } catch (e) {
    }
    r1 = Number(arg1.toString().replace(".", ""))
    r2 = Number(arg2.toString().replace(".", ""))
    return (r1 / r2) * Math.pow(10, t2 - t1);
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
    }
    else {
      return accMul(val, ride).toFixed(n)
    }
  },
  //四舍五入保留2位小数（若第二位小数为0，则保留一位小数）
  keepTwoDecimal(num) {
    var result = parseFloat(num);
    if (isNaN(result)) {
      return false;
    }
    result = Math.round(num * 100) / 100;
    return result;
  },

  //千分位格式化
  formatNumber(num) {
    if (num === undefined || num === '' || num === null) {
      return '';
    }
    else {
      var groups = (/([\-\+]?)(\d*)(\.\d+)?/g).exec("" + num),
        mask = groups[1],                       //符号位
        integers = (groups[2] || "").split(""), //整数部分
        decimal = groups[3] || "",              //小数部分
        remain = integers.length % 3;

      var temp = integers.reduce(function (previousValue, currentValue, index) {
        if (index + 1 === remain || (index + 1 - remain) % 3 === 0) {
          return previousValue + currentValue + ",";
        } else {
          return previousValue + currentValue;
        }
      }, "").replace(/\,$/g, "");
      return mask + temp + decimal;
    }
  },
  //千分位转化为数字
  StrToNumber(obj) {
    var reg = /^[0-9]+.?[0-9]*$/;  //验证字符串是否是数字
    if (!(reg.test(obj))) {
      //为字符串 则判断是否存在','
      if ((obj + "").replace(/^\s\s*/, '').replace(/\s\s*$/, '') == "") {
        return 0.00;
      }
      if (obj == undefined) {
        return 0.00;
      }
      if ((obj || 0).toString().replace(/(\d)(?=(?:\d{3})+$)/g, '$1,')) {
        obj = obj.replace(/,/gi, '');
        return obj;
      }
    }
    return obj;
  },


  //金额转化为汉字
  changeMoneyToChinese(money) {
    var zeroCount, IntLen, i, n, p, q, m, decLen;

    var cnNums = new Array("零", "壹", "贰", "叁", "肆", "伍", "陆", "柒", "捌", "玖"); //汉字的数字
    var cnIntRadice = new Array("", "拾", "佰", "仟"); //基本单位
    var cnIntUnits = new Array("", "万", "亿", "兆"); //对应整数部分扩展单位
    var cnDecUnits = new Array("角", "分", "毫", "厘"); //对应小数部分单位
    //var cnInteger = "整"; //整数金额时后面跟的字符
    var cnIntLast = "元"; //整型完以后的单位
    var maxNum = 9999999999999999.9999; //最大处理的数字

    var IntegerNum; //金额整数部分
    var DecimalNum; //金额小数部分
    var ChineseStr = ""; //输出的中文金额字符串
    var parts; //分离金额后用的数组，预定义
    if (money == "") {
      return "";
    }
    money = parseFloat(money);
    if (money >= maxNum) {
      $.alert('超出最大处理数字');
      return "";
    }
    if (money == 0) {
      //ChineseStr = cnNums[0]+cnIntLast+cnInteger;
      ChineseStr = cnNums[0] + cnIntLast
      //document.getElementById("show").value=ChineseStr;
      return ChineseStr;
    }
    money = money.toString(); //转换为字符串
    if (money.indexOf(".") == -1) {
      IntegerNum = money;
      DecimalNum = '';
    } else {
      parts = money.split(".");
      IntegerNum = parts[0];
      DecimalNum = parts[1].substr(0, 4);
    }
    if (parseInt(IntegerNum, 10) > 0) {//获取整型部分转换
      zeroCount = 0;
      IntLen = IntegerNum.length;
      for (i = 0; i < IntLen; i++) {
        n = IntegerNum.substr(i, 1);
        p = IntLen - i - 1;
        q = p / 4;
        m = p % 4;
        if (n == "0") {
          zeroCount++;
        } else {
          if (zeroCount > 0) {
            ChineseStr += cnNums[0];
          }
          zeroCount = 0; //归零
          ChineseStr += cnNums[parseInt(n)] + cnIntRadice[m];
        }
        if (m == 0 && zeroCount < 4) {
          ChineseStr += cnIntUnits[q];
        }
      }
      ChineseStr += cnIntLast;
      //整型部分处理完毕
    }
    if (DecimalNum != '') {//小数部分
      decLen = DecimalNum.length;
      for (i = 0; i < decLen; i++) {
        n = DecimalNum.substr(i, 1);
        if (n != '0') {
          ChineseStr += cnNums[Number(n)] + cnDecUnits[i];
        }
      }
    }
    if (ChineseStr == '') {
      //ChineseStr += cnNums[0]+cnIntLast+cnInteger;
      ChineseStr += cnNums[0] + cnIntLast;
    }
    /* else if( DecimalNum == '' ){
                    ChineseStr += cnInteger;
                    ChineseStr += cnInteger;
                } */
    return ChineseStr;
  },

  //金额转化为汉字(没有小数 加 整)
  convertCurrency(money) {
    //汉字的数字
    let cnNums = new Array('零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖');
    //基本单位
    let cnIntRadice = new Array('', '拾', '佰', '仟');
    //对应整数部分扩展单位
    let cnIntUnits = new Array('', '万', '亿', '兆');
    //对应小数部分单位
    let cnDecUnits = new Array('角', '分', '毫', '厘');
    //整数金额时后面跟的字符
    let cnInteger = '整';
    //整型完以后的单位
    let cnIntLast = '元';
    //最大处理的数字
    let maxNum = 999999999999999.9999;
    //金额整数部分
    let integerNum;
    //金额小数部分
    let decimalNum;
    //输出的中文金额字符串
    let chineseStr = '';
    //分离金额后用的数组，预定义
    let parts;
    if (money == '') { return ''; }
    money = parseFloat(money);
    if (money >= maxNum) {
      //超出最大处理数字
      return '';
    }
    if (money == 0) {
      chineseStr = cnNums[0] + cnIntLast + cnInteger;
      return chineseStr;
    }
    //转换为字符串
    money = money.toString();
    if (money.indexOf('.') == -1) {
      integerNum = money;
      decimalNum = '';
    } else {
      parts = money.split('.');
      integerNum = parts[0];
      decimalNum = parts[1].substr(0, 4);
    }
    //获取整型部分转换
    if (parseInt(integerNum, 10) > 0) {
      let zeroCount = 0;
      let IntLen = integerNum.length;
      for (let i = 0; i < IntLen; i++) {
        let n = integerNum.substr(i, 1);
        let p = IntLen - i - 1;
        let q = p / 4;
        let m = p % 4;
        if (n == '0') {
          zeroCount++;
        } else {
          if (zeroCount > 0) {
            chineseStr += cnNums[0];
          }
          //归零
          zeroCount = 0;
          chineseStr += cnNums[parseInt(n)] + cnIntRadice[m];
        }
        if (m == 0 && zeroCount < 4) {
          chineseStr += cnIntUnits[q];
        }
      }
      chineseStr += cnIntLast;
    }
    //小数部分
    if (decimalNum != '') {
      let decLen = decimalNum.length;
      for (let i = 0; i < decLen; i++) {
        let n = decimalNum.substr(i, 1);
        if (n != '0') {
          chineseStr += cnNums[Number(n)] + cnDecUnits[i];
        }
      }
    }
    if (chineseStr == '') {
      chineseStr += cnNums[0] + cnIntLast + cnInteger;
    } else if (decimalNum == '') {
      chineseStr += cnInteger;
    }
    return chineseStr;
  },
  
  //金额转化为汉字
  digitUppercase(n) {
    let fraction = ['角', '分'];
    let digit = [
        '零', '壹', '贰', '叁', '肆',
        '伍', '陆', '柒', '捌', '玖'
    ];
    let unit = [
        ['元', '万', '亿'],
        ['', '拾', '佰', '仟']
    ];
    let head = n < 0 ? '欠' : '';
    n = Math.abs(n);
    let s = '';
    for (let i = 0; i < fraction.length; i++) {
        s += (digit[Math.floor(n * 10 * Math.pow(10, i)) % 10] + fraction[i]).replace(/零./, '');
    }
    s = s || '整';
    n = Math.floor(n);
    for (let i = 0; i < unit[0].length && n > 0; i++) {
      let p = '';
        for (let j = 0; j < unit[1].length && n > 0; j++) {
            p = digit[n % 10] + unit[1][j] + p;
            n = Math.floor(n / 10);
        }
        s = p.replace(/(零.)*零$/, '').replace(/^$/, '零') + unit[0][i] + s;
    }
    return head + s.replace(/(零.)*零元/, '元')
        .replace(/(零.)+/g, '零')
        .replace(/^整$/, '零元整');
  },

  //转化为树状结构 下拉框 组合列表 小写pid
  searchTreeData(nodes, treeRootId, flag) {
    for(let i = 0; i < nodes.length; i++){
      if(nodes[i].pid == treeRootId){
        break;
      } else if(i == nodes.length - 1){
        Message.closeAll()
        Message({
          message: '数据格式错误',
          type: 'error',
          duration: 2 * 1000
        })
      }
    }

    let nodesFilters = nodes;
    //默认展开的节点
    let expandRowKeys = [];
    let groups = {};
    // 按父节点将节点分组
    for (var i in nodesFilters) {
      if (!groups[nodesFilters[i].pid]) {
        groups[nodesFilters[i].pid] = [];
      }
      groups[nodesFilters[i].pid].push(nodesFilters[i]);
      if (treeRootId && treeRootId === nodesFilters[i].id) { // 发现传入的根节点id作为节点id时，将根节点设置为该节点的父节点
        treeRootId = nodesFilters[i].pid;
      }
    }

    var rootNodes = groups[treeRootId];
    groups[treeRootId] = null; // [SAFEGUARD]防止自为父节点或互为父节点（有环图结构）导致的死循环
    let defaultIndex = 0;
    let defaultNodeId = ''; //默认选取的节点的id
    function traverseTreeNodeGroup(treeNodeGroup) {
      for (var i in treeNodeGroup) {
        var node = treeNodeGroup[i];
        node.label = node.name;
        node.value = node.id;
        if (groups[node.id]) {
          node.children = groups[node.id];
          groups[node.id] = null; // [SAFEGUARD]防止自为父节点或互为父节点（有环图结构）导致的死循环
          // 存在子节点的要禁用父节点
          // node.disabled = true;
          traverseTreeNodeGroup(node.children);

        } else {
          // 非个券的要禁用 非产品禁用
          if (node.checkBox == "checkBoxN") {
            node.disabled = true;
          } else {
            defaultIndex++;
            //默认选中第一个可用的子节点
            if (defaultIndex == 1) {
              defaultNodeId = node;
            }
            //产品左侧树状结构   只修改子节点的id
            node.label = ' [ ' + node.id + ' ]' + node.name;
          }
        }
        //选择默认展开的节点 不展开其他
        if (node.pid == treeRootId ) {
          if(node.id != -1){
            expandRowKeys.push(node.id)
          }
        }
      }
    }

    traverseTreeNodeGroup(rootNodes);
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
    return {"treeNode": rootNodes, "defaultNode": defaultNodeId,"expandRowKeys": expandRowKeys};
  },
  //收益贡献转化为树状结构 下拉框  小写pid
  earingsConTreeData(nodes, treeRootId) {
    for(let i = 0; i < nodes.length; i++){
      if(nodes[i].pid == treeRootId){
        break;
      }
      else if(i == nodes.length - 1){
        Message.closeAll()
        Message({
          message: '数据格式错误',
          type: 'error',
          duration: 2 * 1000
        })
      }
      else{}
    }

    let nodesFilters = nodes;

    let groups = {};
    //默认展开的节点
    let expandRowKeys = [];
    // 按父节点将节点分组
    for (var i in nodesFilters) {
      if (!groups[nodesFilters[i].pid]) {
        groups[nodesFilters[i].pid] = [];
      }
      groups[nodesFilters[i].pid].push(nodesFilters[i]);
      if (treeRootId && treeRootId === nodesFilters[i].id) { // 发现传入的根节点id作为节点id时，将根节点设置为该节点的父节点
        treeRootId = nodesFilters[i].pid;
      }
    }

    var rootNodes = groups[treeRootId];
    groups[treeRootId] = null; // [SAFEGUARD]防止自为父节点或互为父节点（有环图结构）导致的死循环
    function traverseTreeNodeGroup(treeNodeGroup) {
      for (var i in treeNodeGroup) {
        let node = treeNodeGroup[i];
        if (groups[node.id]) {
          node.children = groups[node.id];
          groups[node.id] = null; // [SAFEGUARD]防止自为父节点或互为父节点（有环图结构）导致的死循环
          traverseTreeNodeGroup(node.children);

        }
        else {
        }
        //选择默认展开的节点
        if (node.pid == treeRootId) {
          expandRowKeys.push(node.id)
        }
        else {
        }
      }
    }

    traverseTreeNodeGroup(rootNodes);

    return {"data": rootNodes, "expandRowKeys": expandRowKeys};
  },

  //转化为树状结构 大写pId
  TreeDataPId(nodes, treeRootId) {
    for(let i = 0; i < nodes.length; i++){
      if(nodes[i].pId == treeRootId){
        break;
      }
      else if(i == nodes.length - 1){
        Message.closeAll()
        Message({
          message: '数据格式错误',
          type: 'error',
          duration: 2 * 1000
        })
      }
      else{}
    }

    let nodesFilters = nodes;

    let groups = {};
    //默认选中的节点
    let expandRowKeys = [];
    // 按父节点将节点分组
    for (var i in nodesFilters) {
      if (!groups[nodesFilters[i].pId]) {
        groups[nodesFilters[i].pId] = [];
      }
      groups[nodesFilters[i].pId].push(nodesFilters[i]);
      if (treeRootId && treeRootId === nodesFilters[i].id) { // 发现传入的根节点id作为节点id时，将根节点设置为该节点的父节点
        treeRootId = nodesFilters[i].pId;
      }
    }

    var rootNodes = groups[treeRootId];
    groups[treeRootId] = null; // [SAFEGUARD]防止自为父节点或互为父节点（有环图结构）导致的死循环
    function traverseTreeNodeGroup(treeNodeGroup) {
      for (var i in treeNodeGroup) {
        var node = treeNodeGroup[i];
        node.label = node.name;
        node.value = node.id;
        if (groups[node.id]) {
          node.children = groups[node.id];
          groups[node.id] = null; // [SAFEGUARD]防止自为父节点或互为父节点（有环图结构）导致的死循环
          traverseTreeNodeGroup(node.children);

        }
        else {
        }
        //选择默认展开的节点
        if (node.pId == treeRootId) {
          expandRowKeys.push(node.id)
        }
        else {
        }
      }
    }

    traverseTreeNodeGroup(rootNodes);

    return {"data": rootNodes, "expandRowKeys": expandRowKeys};
  },

  /* 
  * 列表转换为树形结构
  * nodes 节点
  * treeRootId 顶级根节点
  * pidName 父节点名
  * idName 子节点名
  * mid  树形key
  */
  converTreeData (nodes, treeRootId, pidName, idName, mid) {
    if (!pidName) pidName = 'pid'
    if (!idName) idName = 'id'
    if (!mid) {
      mid = 'id'
    } else {
      // 增加唯一标识key
      nodes = nodes.map(item => {
        item.mid = item[idName]+ item[pidName] + (Math.random() * 1000)
        return item
      })
    }
    for (let i = 0; i < nodes.length; i++) {
      if (nodes[i][pidName] == treeRootId) {
        break;
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

    let groups = {}
    // 默认展开的节点
    let expandRowKeys = []
    // 按父节点将节点分组
    for (let i in nodesFilters) {
      if (!groups[nodesFilters[i][pidName]]) {
        groups[nodesFilters[i][pidName]] = []
      }
      groups[nodesFilters[i][pidName]].push(nodesFilters[i])
      if (treeRootId && treeRootId === nodesFilters[i][idName]) { // 发现传入的根节点id作为节点id时，将根节点设置为该节点的父节点
        treeRootId = nodesFilters[i][pidName]
      }
    }

    let rootNodes = groups[treeRootId]
    groups[treeRootId] = null // [SAFEGUARD]防止自为父节点或互为父节点（有环图结构）导致的死循环

    function traverseTreeNodeGroup (treeNodeGroup) {
      for (let i in treeNodeGroup) {
        let node = treeNodeGroup[i]
        if (groups[node[idName]]) {
          node.children = groups[node[idName]]
          groups[node[idName]] = null; // [SAFEGUARD]防止自为父节点或互为父节点（有环图结构）导致的死循环
          traverseTreeNodeGroup(node.children)
        }
        //选择默认展开的节点
        if (node[pidName] == treeRootId) {
          expandRowKeys.push(node[mid])
        }
      }
    }
    traverseTreeNodeGroup(rootNodes)

    return { data: rootNodes, expandRowKeys: expandRowKeys }
  },
  // 判断上传的文件是否为图片
  fileIsImage(name){
      let arr = ['png', 'jpg', 'jpeg', 'bmp', 'gif', 'webp', 'psd', 'svg', 'tiff'];
      let index = name.lastIndexOf(".");
      let str = name.substring(index + 1,name.length);
      arr.indexOf(str.toLowerCase());
      if(arr.indexOf(str.toLowerCase()) !== -1){
          return true;
      }
      else{
        Message.closeAll()
        Message({
          message: '只能选择图片类型的文件',
          type: 'warning',
          duration: 2 * 1000
        });
        return false;
        
      }

  },
  
  //后端排序公共方法
  orderByString(val) {
    //排序字段
    let orderBy = '';
    let isAsc = '';
    let returnData = '';
    let label = val.prop.split('.');
    if (label.length == 2) {
      orderBy = label[1];
    }
    else {
      orderBy = label[0];
    }
    //正序 倒序列
    if (val.order == "ascending") {
      isAsc = "asc";
      returnData = '"' + orderBy + '" ' + isAsc + ' nulls last';
    }
    else if (val.order == "descending") {
      isAsc = "desc";
      returnData = '"' + orderBy + '" ' + isAsc + ' nulls last';
    }
    else {
      returnData = '';
    }
    return returnData;

  },
  //vxe后端排序公共方法
  VXEorderByString(val) {
    //排序字段
    let orderBy = '';
    let isAsc = '';
    let returnData = '';
    let label = val.property.split('.');
    if (label.length == 2) {
      orderBy = label[1];
    }
    else {
      orderBy = label[0];
    }
    //正序 倒序列
    if (val.order == "asc") {
      isAsc = "asc";
      returnData = '"' + orderBy + '" ' + isAsc + ' nulls last';
    }
    else if (val.order == "desc") {
      isAsc = "desc";
      returnData = '"' + orderBy + '" ' + isAsc + ' nulls last';
    }
    else {
      returnData = '';
    }
    return returnData;

  },
  //后端排序 动态算
  moveOrderByString(val) {
    let obj = {
      "orderBy": '',
      "isAsc": '',
    }
    //排序字段
    let label = val.prop.split('.');
    if (label.length == 2) {
      obj.orderBy = label[1];
    }
    else {
      obj.orderBy = label[0];
    }
    //正序 倒序列
    if (val.order == "ascending") {
      obj.isAsc = true;
    }
    else if (val.order == "descending") {
      obj.isAsc = false;
    }
    else {
      obj.isAsc = true;
      obj.orderBy = '';
    }
    return obj;
  },

  // 列表排序值处理
  etlqueryOrderBy (val) {
    let orderBy = ''
    if (val.order === 'ascending') {
      orderBy = `${val.prop}` // 升序
    } else if (val.order === 'descending') {
      orderBy = `${val.prop} desc ` // 降序
    } else {
      orderBy = ''
    }
    return orderBy
  },
  // 列表排序值处理
  queryOrderBy (val) {
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
  // 请求参数排除无意义的值
  parameterSrc(data){
    let newData = {}
    for(let key in data){
      if(data[key] === '' || data[key] === undefined || data[key] === null){

      }
      else{
       newData[key] = data[key];
      }
    }
    return newData;
  },
  // 请求参数排除无意义的值
  parameterSrcFull(data){
    let newData = {}
    for(let key in data){
      if( data[key] === undefined){
		newData[key] = null;
      }else if( data[key] === ''){
		newData[key] = '';
	  }else{
        newData[key] = data[key];
      }
    }
    return newData;
  },
  
  // 以form表单形式下载文件
  formDownloadFile(params, action,methods) {
    let timer=new Date().getTime()
    let iframe = document.createElement('iframe')
    iframe.id = 'iframe'+timer
    iframe.name = 'iframe'+timer
    iframe.style = 'display:none'
    document.body.appendChild(iframe)
    let form = document.createElement('form')
    form.id = 'form'+timer
    form.name = 'form'+timer
	  form.target = 'iframe'+timer
    // form.style = 'display:none'
    iframe.appendChild(form)
    for (let obj in params) {
      if( Array.isArray(params[obj]) ){
        for(let item in params[obj]){
          let input = document.createElement('input')
          input.tpye = 'hidden'
          input.name = obj
          input.value = params[obj][item]
          form.appendChild(input)
        }
      }else{
        let input = document.createElement('input')
        input.tpye = 'hidden'
        input.name = obj
        input.value = params[obj]
        form.appendChild(input)
      }
    }
    form.method = methods //请求方式
    form.action = action
    form.submit()

    iframe.onload=function(){
      document.body.removeChild(iframe)
    }
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
  searchButtonDisabled(document,self) {
    let seconds = 5;
    self[document] = true;
    let timer = setTimeout(() => {
      self[document] = false;
      clearTimeout(timer)
    }, seconds * 1000);
  },
  // echarts数据视图样式
  optionToContent (opt, name) {
    let tableName = ''
    if (name) tableName = name
    let axisData = opt.xAxis[0].data; //坐标数据
    let series = opt.series; //折线图数据
    let tdHeads = `<td  style="padding: 0 10px;min-width: 100px;">${tableName}</td>`; //表头
    let tdBodys = ''; //数据
    series.forEach(item => {
        //组装表头
        tdHeads += `<td style="padding: 0 10px;min-width: 120px;">${item.name}</td>`;
    });
    let table = `<table border="1" style="margin-left:20px;border-collapse:collapse;font-size:14px;text-align:center"><tbody><tr>${tdHeads} </tr>`;
    for (let i = 0, l = axisData.length; i < l; i++) {
        for (let j = 0; j < series.length; j++) {
            if (isNaN(series[j].data[i])) {
              series[j].data[i] = 0
            }
            //组装表数据
            tdBodys += `<td>${ series[j].data[i]}</td>`;
        }
        table += `<tr><td style="padding: 0 10px">${axisData[i]}</td>${tdBodys}</tr>`;
        tdBodys = '';
    }
    table += '</tbody></table>';
    return table;
  },
  //与当前时间比较（格式 yyyy-mm-dd）
  compareNowDate(myDate){
    var date = new Date();
    myDate = new Date(''+myDate+' 23:59:59');
    console.log(myDate);
    if(myDate>=date){
      return true;
    }else{
      return false;
    }

  },
  /**
   * 给form动态赋值,并判断是否为空
   * @param {*} obj 通过接口查询出的数据
   * @param {*} formData //form表单数据
   */
  allPrpos(formData,obj) {
    // 用来保存所有的属性名称和值
    let data = formData;
    // 开始遍历
    for(var p in data){
        // 方法
        if(typeof(obj[p])=="function"){
            obj[p]();
        }else{
            // p 为属性名称，obj[p]为对应属性的值
            data[p] = this.abnormalityData(obj[p]);
        }
    }
    return data;
    
},
//字典转换
  dictionaryArrToName(arr,code){
    if(!arr || arr.length<=0){
      return "-";
    }
    for(let i=0;i<arr.length;i++){
      if(arr[i].dimCde === code){
        return arr[i].dimNme;
      }
    }
  },
  //数据判空
  objectIsNotEmpty(objectValue) {
    if (objectValue === "" || objectValue === undefined || objectValue === null) {
      return false;
    }
    return true;
  },
  //数据初始化
   initValue(objectValue) {
    if(!this.objectIsNotEmpty(objectValue))
      return "";
    if (typeof(objectValue) == 'undefined' || objectValue === null) {
      return "";
    }
    return objectValue;
  },
   //字符串数据初始化
  initStrValue(objectValue) {
    if(!this.objectIsNotEmpty(objectValue))
      return "-";
    if (typeof(objectValue) == 'undefined' || objectValue === null) {
      return "-";
    }
    return objectValue;
  },
  
  /**
       * 初始化数据，如果为空返回0
       * @param objectValue
       * @returns {*}
       */
    initIntValue (objectValue) {
          if (typeof(objectValue)=='undefined'||objectValue === null || objectValue === undefined) {
              return 0;
          }
          return objectValue;
  },
    //两位小数数据初始化
  initDobulValue (objectValue) {
    if (typeof(objectValue)=='undefined'||objectValue === null || objectValue === undefined) {
        return 0.00;
    }
    return objectValue;
},
//百分比数据初始化
  iniRateValue (objectValue) {
    if (typeof(objectValue) == 'undefined' || objectValue === null || objectValue === "") {
      return "";
    }
    if (objectValue == '0.0000' || objectValue === 0.0000 ) {
      return 0;
    }
    return objectValue + "%";
  },
  //数字千位符号
  toThousands(numval) {
    if(this.initValue(numval)=="" ||  !this.objectIsNotEmpty(numval))
      return "";
    var strnumval = (numval || 0).toString();
    var strnumvalold = strnumval;
    if (strnumvalold.indexOf("-") != -1) {
      strnumval = strnumval.split("-")[1];
    }
    var num = strnumval.split(".")[0];
    var endNum = "";
    if (strnumval.split(".").length > 1) {
      endNum = "." + strnumval.split(".")[1];
    }
  
    var result = '',
      counter = 0;
    // num = (num || 0).toString();
    for (var i = num.length - 1; i >= 0; i--) {
      counter++;
      result = num.charAt(i) + result;
      if (!(counter % 3) && i != 0) {
        result = ',' + result;
      }
    }
    if (strnumvalold.indexOf("-") != -1) {
      return '-' + result + endNum;
    }
    return result + endNum;
  },
  
  
  //数字保留n位小数，number: 数字，n 保留位数
   getFloat (number, n) {
    if(number === 'undefined' || number === null || number === ""){
      return "";
    }
      
    n = n ? parseInt(n) : 0;
    if (n <= 0) {
      return Math.round(number);
    }
    number = Math.round(number * Math.pow(10, n)) / Math.pow(10, n); //四舍五入
    number = Number(number).toFixed(n); //补足位数
    return number;
  },
  //流程跟踪bpmn添加备注封装
  flow_bpmnModule(diagramXML,trace_tree,self){
    var bpmn_id = '';
    var viewer = new BpmnViewer({
      container: '#diagram'
    });

    viewer.importXML(diagramXML, function (err) {


      if (err) {

      } else {
        //访问各种图表服务 与Canvas图表进行交互以使图表适合当前可用的视口大小
        $(".bjs-powered-by").css("display","none");
        var overlays = viewer.get('overlays'),
          canvas = viewer.get('canvas'),
          elementRegistry = viewer.get('elementRegistry');

        // modeling = viewer.get('modeling');
        // Option 1: Color via Overlay
        //添加备注封装
        function remark(id,color,trace_tree) {
          // 清空之前添加的内容
          for(var i = 0; i < $(".djs-overlays").length; i++){
            if($(".djs-overlays:eq("+i+")").attr("data-container-id") == id){
              $(".djs-overlays:eq("+i+")").empty();
            }
          }
          var task_click = elementRegistry.get(id);
           // 如果存在本节点的元素再操作
            if(task_click != undefined){
              var $overlayHtml_click = $("<div class='click' id=click"+ id +" style='cursor: pointer'></div>")
                .css({
                  width: task_click.width,

                  height: task_click.height
                });

              overlays.add(id, {
                position: {
                  top: 0,
                  left: 0

                },
                html: $overlayHtml_click

              });


              var content="<div class='content' id=content"+ id +">" +
                "<table border='1px' class='apply_table bpmn_apply_table' bordercolor='#f2f2f2'>"+
                "<tr > <td style=' border: 1px solid #AAAAAA;'> <li>处理人:</li> </td> <td class='person' style=' border: 1px solid #AAAAAA;'> <li> "+trace_tree.ownerDisplayName+"</li> </td> </tr>"+
                "<tr > <td style=' border: 1px solid #AAAAAA;'> <li>任务到达时间:</li> </td> <td class='arrive_time' style=' border: 1px solid #AAAAAA;'> <li > "+trace_tree.beginTime +" </li> </td> </tr>"+
                "<tr > <td style=' border: 1px solid #AAAAAA;'> <li>任务完成时间:</li> </td> <td class='execute_time' style=' border: 1px solid #AAAAAA;'> <li> "+trace_tree.endTime +" </li> </td> </tr>"+
                "<tr  > <td style=' border: 1px solid #AAAAAA;'> <li>耗时:</li> </td> <td class='elapsed_time' style=' border: 1px solid #AAAAAA;'> <li>  "+trace_tree.duration+" </li> </td> </tr>"+
                "</table>"+

                "</div>";


              $("#click"+id).append(content);
              $(".content").css({"min-width":"285px","border":"1px solid #AAAAAA","position":"absolute","left":"0px","cursor":"pointer","padding": "5px","text-align": "left","line-height": "20px","font-size":"15px","color": "#3f3f3f","background":"#fff","border-radius":"10px","animation":"content 1s forwards","-ms-animation":"content 1s forwards","-moz-animation":"content 1s forwards","-webkit-animation":"content 1s forwards","-o-animation":"content 1s forwards","display":"none"});
              //点击控制内容显示隐藏
              $("#content"+id).css("top",$("#click"+id).height());

              $("#click"+id).mouseover(function () {

                $("#content"+id).css('display','block');
                $(".content table tr td:nth-child(1) li").css("color",color);
                self.bpmn_id = id;
              })
              $("#click"+id).mouseout(function () {
                $("#content"+id).css('display','none');
              })
              $("#content"+id).mouseover(function () {
                $("#content"+id).css('display','block');
                $(".content table tr td:nth-child(1) li").css("color",color);
                self.bpmn_id = id;
              })
              $("#content"+id).mouseout(function () {
                $("#content"+id).css('display','none');
              })
              $("#content"+ id).click(function () {
                $(".form_submit").css("display","block");
                self.id = id;

                setTimeout(() => $(".form_submit").css("right","0px"), 50);
                $("#diagram").css("min-width","2400px");
                var window_height=$(window).height();
                $(".form_submit").height(window_height);
                setTimeout(function () {
                  return id;
                },100)

              })
            }
            else{

            }


        }



        // 已完成的节点
        function complete(completetaskId){


          for(var i=0;i<$(".djs-shape").length;i++){
            if($(".djs-shape:eq("+i+")").attr("data-element-id")==completetaskId){
              // 方框
              $(".djs-shape:eq("+i+") .djs-visual rect").css("stroke","rgb(67, 160, 71)");
              $(".djs-shape:eq("+i+") .djs-visual text").css("fill","rgb(67, 160, 71)");
              $(".djs-shape:eq("+i+") .djs-visual rect").css("fill","#fff");
              // 圆圈
              $(".djs-shape:eq("+i+") .djs-visual circle").css("stroke","rgb(67, 160, 71)");
              $(".djs-shape:eq("+i+") .djs-visual text").css("fill","rgb(67, 160, 71)");
              $(".djs-shape:eq("+i+") .djs-visual circle").css("fill","#fff");
            }
          }
        }




        // 正在进行中的节点
        function being(beingtaskId){


          for(var i=0;i<$(".djs-shape").length;i++){
            if($(".djs-shape:eq("+i+")").attr("data-element-id")==beingtaskId){
              // 方框
              $(".djs-shape:eq("+i+") .djs-visual rect").css("stroke","#FF69B4");
              $(".djs-shape:eq("+i+") .djs-visual text").css("fill","#FF69B4");
              $(".djs-shape:eq("+i+") .djs-visual rect").css("fill","#fff");
              // 圆圈
              $(".djs-shape:eq("+i+") .djs-visual circle").css("stroke","#FF69B4");
              $(".djs-shape:eq("+i+") .djs-visual text").css("fill","#FF69B4");
              $(".djs-shape:eq("+i+") .djs-visual circle").css("fill","#fff");


            }
          }
        }

        // 已取消的节点
        function cancel(CancelId) {


          for(var i=0;i<$(".djs-shape").length;i++){
            if($(".djs-shape:eq("+i+")").attr("data-element-id")==CancelId){
              //方框
              $(".djs-shape:eq("+i+") .djs-visual rect").css("stroke","#FF7F24");
              $(".djs-shape:eq("+i+") .djs-visual text").css("fill","#FF7F24");
              $(".djs-shape:eq("+i+") .djs-visual rect").css("fill","#fff");
              // 圆圈
              $(".djs-shape:eq("+i+") .djs-visual circle").css("stroke","#FF7F24");
              $(".djs-shape:eq("+i+") .djs-visual text").css("fill","#FF7F24");
              $(".djs-shape:eq("+i+") .djs-visual circle").css("fill","#fff");


            }
          }
        }
        // 结束节点
        function finish(finishtaskId){
          for(var i=0;i<$(".djs-shape").length;i++){
            if($(".djs-shape:eq("+i+")").attr("data-element-id")==finishtaskId){
              // 方框
              $(".djs-shape:eq("+i+") .djs-visual rect").css("stroke","#1C86EE");
              $(".djs-shape:eq("+i+") .djs-visual text").css("fill","#1C86EE");
              $(".djs-shape:eq("+i+") .djs-visual rect").css("fill","#fff");
              // 圆圈
              $(".djs-shape:eq("+i+") .djs-visual circle").css("stroke","#1C86EE");
              $(".djs-shape:eq("+i+") .djs-visual text").css("fill","#1C86EE");
              $(".djs-shape:eq("+i+") .djs-visual circle").css("fill","#fff");
            }
          }
        }
        function timestampToTime(timestamp) {
          var now = new Date(timestamp);
          var  y = now.getFullYear();
          var   m = now.getMonth() + 1;
          var  d = now.getDate();
          return y + "-" + (m < 10 ? "0" + m : m) + "-" + (d < 10 ? "0" + d : d) + " " + now.toTimeString().substr(0, 8);
        }

        for(var i = 0; i < trace_tree.length; i++){

          // 正在执行
          if(trace_tree[i].state == 0){
            being(trace_tree[i].xmlId)
            if(trace_tree[i].ownerDisplayName != undefined){

            }
            else{
              trace_tree[i].ownerDisplayName = '';
            }
            if(trace_tree[i].beginTime != undefined && trace_tree[i].beginTime != ''){
              trace_tree[i].beginTime = timestampToTime(trace_tree[i].beginTime);
            }
            else{
              trace_tree[i].beginTime = '';
            }
            if(trace_tree[i].endTime != undefined && trace_tree[i].endTime != ''){
              trace_tree[i].endTime = timestampToTime(trace_tree[i].endTime);
            }
            else{
              trace_tree[i].endTime = '';
            }
            if(trace_tree[i].duration != undefined){

            }
            else{
              trace_tree[i].duration = '';
            }
            remark(trace_tree[i].xmlId,'#FF69B4',trace_tree[i]);
          }
          // 结束节点
          else if(trace_tree[i].state == 1){

            finish(trace_tree[i].xmlId);
            if(trace_tree[i].ownerDisplayName != undefined){

            }
            else{
              trace_tree[i].ownerDisplayName = '';
            }
            if(trace_tree[i].beginTime != undefined && trace_tree[i].beginTime != ''){
              trace_tree[i].beginTime = timestampToTime(trace_tree[i].beginTime);
            }
            else{
              trace_tree[i].beginTime = '';
            }
            if(trace_tree[i].endTime != undefined && trace_tree[i].endTime != ''){
              trace_tree[i].endTime = timestampToTime(trace_tree[i].endTime);
            }
            else{
              trace_tree[i].endTime = '';
            }
            if(trace_tree[i].duration != undefined){

            }
            else{
              trace_tree[i].duration = '';
            }
            remark(trace_tree[i].xmlId,'#1C86EE',trace_tree[i]);
          }
          // 已取消
          else if(trace_tree[i].state == 2){
            cancel(trace_tree[i].xmlId)
            if(trace_tree[i].ownerDisplayName != undefined){

            }
            else{
              trace_tree[i].ownerDisplayName = '';
            }
            if(trace_tree[i].beginTime != undefined && trace_tree[i].beginTime != ''){
              trace_tree[i].beginTime = timestampToTime(trace_tree[i].beginTime);
            }
            else{
              trace_tree[i].beginTime = '';
            }
            if(trace_tree[i].endTime != undefined && trace_tree[i].endTime != ''){
              trace_tree[i].endTime = timestampToTime(trace_tree[i].endTime);
            }
            else{
              trace_tree[i].endTime = '';
            }
            if(trace_tree[i].duration != undefined){

            }
            else{
              trace_tree[i].duration = '';
            }
            remark(trace_tree[i].xmlId,'#FF7F24',trace_tree[i]);
          }
          else if(trace_tree[i].state == 3){

          }
          // 已完成的节点
          else if(trace_tree[i].state == 4){
            complete(trace_tree[i].xmlId)

            if(trace_tree[i].ownerDisplayName != undefined){

            }
            else{
              trace_tree[i].ownerDisplayName = '';
            }
            if(trace_tree[i].beginTime != undefined && trace_tree[i].beginTime != ''){
              trace_tree[i].beginTime = timestampToTime(trace_tree[i].beginTime);
            }
            else{
              trace_tree[i].beginTime = '';
            }
            if(trace_tree[i].endTime != undefined && trace_tree[i].endTime != ''){
              trace_tree[i].endTime = timestampToTime(trace_tree[i].endTime);
            }
            else{
              trace_tree[i].endTime = '';
            }
            if(trace_tree[i].duration != undefined){

            }
            else{
              trace_tree[i].duration = '';
            }
            remark(trace_tree[i].xmlId,'rgb(67, 160, 71)',trace_tree[i]);
          }
          else{

          }

        }








        // remark(taskId);
        // remark('Task_0h8n41f');


      }


    });
    // 元素加载延迟
    setTimeout(function () {
      $(".viewport").prop("id","bpmn_viewport")
      var outline = document.getElementById("bpmn_viewport").getBoundingClientRect()

      $("#diagram").css({"width": outline.width + 350 + "px"})
      $("#diagram").css({"height": outline.height + 200 + "px"})
    },10)



  },
  //流程配置bpmn添加备注封装
  bpmnModule(diagramXML,taskId,completetaskId,beingtaskId,self){
    var viewer = new BpmnViewer({
      container: '#diagram'
    });
    viewer.importXML(diagramXML, function (err) {
      if (err) {} else {
        //访问各种图表服务 与Canvas图表进行交互以使图表适合当前可用的视口大小
        $(".bjs-powered-by").css("display","none");
        var overlays = viewer.get('overlays'),
          canvas = viewer.get('canvas'),
          elementRegistry = viewer.get('elementRegistry');
        // modeling = viewer.get('modeling');
        // Option 1: Color via Overlay
        //添加备注封装
        function remark(id) {
          var task_click = elementRegistry.get(id);
          var $overlayHtml_click = $("<div class='click' id=click"+ id +" style='cursor: pointer'></div>")
            .css({
              width: task_click.width,
              height: task_click.height
            });
          overlays.add(id, {
            position: {
              top: 0,
              left: 0
            },
            html: $overlayHtml_click
          });
          // var content="<div class='content' id=content"+ id +"><img src='../src/assets/img/setting.png' class='content_img'/></div>";
          var content="<div class='contentBmp' id=content"+ id +"><div class='content_remak'>" + "</div></div>";
          var div = ''
          $("#click"+id).append(div);
          $(".contentBmp").css(
              { "position":"absolute",
                "cursor":"pointer",
                "margin-left": '1px',
                "padding": "10px",
                "text-align": "left",
                "line-height": "20px",
                "font-size":"15px",
                "color": "#000",
                "background":"#F0F0F0",
                "border-radius":"10px",
                "animation":"content 1s forwards",
                "-ms-animation":"content 1s forwards",
                "-moz-animation":"content 1s forwards",
                "-webkit-animation":"content 1s forwards",
                "-o-animation":"content 1s forwards",
                "display":"none"
              }
            );
          // $(".content_img").attr("src",$(".setting_img").attr("src"));
          // $(".content_img").css({"width":"200px"});
          $(".content_remak").css({"width":"200px", 'height': '20px'});
          //点击控制内容显示隐藏
          $("#content"+id).css("left",$("#click"+id).width());
          $("#click"+id).mouseover(function () {
            $("#content"+id).css('display','block');
          })
          $("#click"+id).mouseout(function () {
            $("#content"+id).css('display','none');
          })
          $("#content"+id).mouseover(function () {
            $("#content"+id).css('display','block');
          })
          $("#content"+id).mouseout(function () {
            $("#content"+id).css('display','none');
          })
          $("#content"+ id).click(function () {
            $(".form_submit").css("display","block");
            // self.id = id; //看不出使用处---
            // 设置右侧设置界面显示
            setTimeout(() => $(".form_submit").css("right","0px"), 50);
            // 设置右侧设置界面显示高度
            var window_height = $(window).height();
            $(".form_submit").height(window_height - 50);
            // 设置bpmn图宽度
            $(".viewport").prop("id","bpmn_viewport")
            var outline = document.getElementById("bpmn_viewport").getBoundingClientRect()
            $("#diagram").css({"width": outline.width + $(".form_submit").width()+350 })
            // xmlId传值
            // setTimeout(function () {
              return id;
            // },100)
          })

        }
        for(var i=0;i<taskId.length;i++) {
          remark(taskId[i]);
        }
        function complete(completetaskId) {
          for(var i=0;i<$(".djs-shape").length;i++){
            if($(".djs-shape:eq("+i+")").attr("data-element-id")==completetaskId.xmlId){
              $(".djs-shape:eq("+i+") .djs-visual rect").css("stroke","rgb(67, 160, 71)");
              $(".djs-shape:eq("+i+") .djs-visual text").css("fill","rgb(67, 160, 71)");
              $(".djs-shape:eq("+i+") .djs-visual rect").css("fill","#fff");
            }
          }
        }
        for(var i=0;i<completetaskId.length;i++){
          complete(completetaskId[i]);
        }
        function being(beingtaskId) {
          for(var i=0;i<$(".djs-shape").length;i++){
            if($(".djs-shape:eq("+i+")").attr("data-element-id")==beingtaskId.xmlId){
              $(".djs-shape:eq("+i+") .djs-visual rect").css("stroke","#FF69B4");
              $(".djs-shape:eq("+i+") .djs-visual text").css("fill","#FF69B4");
              $(".djs-shape:eq("+i+") .djs-visual rect").css("fill","#fff");
            }
          }
        }
        for(var i=0;i<beingtaskId.length;i++){
          being(beingtaskId[i]);
        }
        // remark(taskId);
        // remark('Task_0h8n41f');
      }
    });
    // 元素加载延迟
    setTimeout(function () {
      $(".viewport").prop("id","bpmn_viewport")
      var outline = document.getElementById("bpmn_viewport").getBoundingClientRect()
      $("#diagram").css({"width": outline.width + 350 + "px"})
      $("#diagram").css({"height": outline.height + 200 + "px"})
    },10)
  },
  // 生成随机id
  getUUID(tabName){
    let str=[];
    let Chars='0123456789abcdefghijklmnopqrstuvwxyz';
    for(let i=0;i<36;i++){
    str[i]=Chars.substr(Math.floor(Math.random()*16),1)
    }
    str[0]=str[8]=str[13]=str[18]=str[23]='-';
    return tabName+str.join("")
  }

}

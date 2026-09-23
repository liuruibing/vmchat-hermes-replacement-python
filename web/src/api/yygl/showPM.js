import request from '@/utils/request'
import qs from 'qs'

/**
 * 获取服务器的当前时间
 */
export function getnow() {
  return request({
    url: '/api/taskcenter/v1.0/getTime',
    method: 'post',
    contentType:' application/json ',
    data:{}
  })
}
/**
 * 计算服务器的当前时间
 * 查询出服务器的当前时间，比较和本地时间的毫秒差，每次获取本地时间加上差值就是计算所得的服务器时间
 */
export function getFwqDatetime(wchm) {
  let now = new Date(new Date().getTime()+wchm);
  let year = now.getFullYear();
  let month = now.getMonth() + 1;
  if (month < 10) {
    month = `0${month}`;
  }
  let date = now.getDate();
  if (date < 10) {
    date = `0${date}`;
  }
  let hour = now.getHours();
  if (hour < 10) {
    hour = `0${hour}`;
  }
  let minute = now.getMinutes();
  if (minute < 10) {
    minute = `0${minute}`;
  }
  let second = now.getSeconds();
  if (second < 10) {
    second = `0${second}`;
  }
  let nowStr = `${year}-${month}-${date} ${hour}:${minute}:${second}`;
  return nowStr;
}
/**
 * 根据传入的参数查询数据
 * @param {*} params
 */
export function getDataOverView (params) {
  return request({
    url: `/api/generalquery/v1.0/getQueryResult.do?${qs.stringify(params)}`,
    method: 'get'
  })
}
/**
 * 查询过去30天的任务数
 */
export function get30DaysTasks() {
  return request({
    url: '/api/taskcenter/v1.0/amount30',
    method: 'post',
    contentType:' application/json ',
    data:{}
  })
}
/**
 * 获取过去5天的任务数
 */
export function get5DaysTasks() {
  return request({
    url: '/api/taskcenter/v1.0/amount5',
    method: 'post',
    contentType:' application/json ',
    data:{}
  })
}
function getFormatDate(date){
  let year = date.getFullYear();
  let month = date.getMonth()+1;
  let day = date.getDate();
  if(month<10){
    month = `0${month.toString()}`;
  }
  month = month.toString();
  if(day<10){
    day = `0${day.toString()}`;
  }
  day = day.toString();
  return `${year}-${month}-${day}`;
}
/**
 * 查询清算进度【非国君】 直销清算、投资交易清算
 */
export function dashboard() {
  return request({
    url: '/api/taskcenter/v1.0/operationWork',
    method: 'post',
    contentType:' application/json ',
    data:{}
  })
}
/**
 * 查询清算进度【国君任务中心】 国泰君安资金清算、国泰君安估值核算、国泰君安注册登记、国泰君安交付物及信息披露
 */
export function dashboardRemote() {
  return request({
    url: '/api/taskcenter/v1.0/dashboardRemote',
    method: 'post',
    contentType:' application/json ',
    data:{}
  })
}
/**
 * 产品运营重要事项-本周
 */
export function fundWorkThisWeek() {
  return request({
    url: '/api/taskcenter/v1.0/fundWorkThisWeek',
    method: 'post',
    contentType:' application/json',
    data:{}
  })
}
/**
 * 产品运营重要事项-下周
 */
export function fundWorkNextWeek() {
  return request({
    url: '/api/taskcenter/v1.0/fundWorkNextWeek',
    method: 'post',
    contentType:' application/json ',
    data:{}
  })
}
/**
 * 待办任务中心-本周
 */
export function waitWorkThisWeek() {
  return request({
    url: '/api/taskcenter/v1.0/waitWorkThisWeek',
    method: 'post',
    contentType:' application/json ',
    data:{}
  })
}
/**
 * 待办任务中心-下周
 */
export function waitWorkNextWeek() {
  return request({
    url: '/api/taskcenter/v1.0/waitWorkNextWeek',
    method: 'post',
    contentType:' application/json ',
    data:{}
  })
}

export default {
}

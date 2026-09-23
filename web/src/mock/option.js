const scriptTxt1 = "var dom = document.getElementById('$id$');var myChart = echarts.init(dom, null, {renderer: 'canvas',useDirtyRect: false});var app = {};var option;option = {xAxis: {type: 'category',data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']},yAxis: {type: 'value'},series: [{data: [150, 230, 224, 218, 135, 147, 260],type: 'bar'}]};if (option && typeof option === 'object') {myChart.setOption(option);myChart.resize();}window.addEventListener('resize', myChart.resize);"
const scriptTxt2 = "var dom = document.getElementById('$id$');var myChart = echarts.init(dom, null, {renderer: 'canvas',useDirtyRect: false});var app = {};var option;option = {xAxis: {type: 'category',data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']},yAxis: {type: 'value'},series: [{data: [150, 150, 224, 150, 135, 147, 260],type: 'line'}]};if (option && typeof option === 'object') {myChart.setOption(option);myChart.resize();}window.addEventListener('resize', myChart.resize);"
const scriptTxt3 = `var title = "基本信息";var data = [{"基金简称" : "华夏大盘精选A" , "证券代码" : "000011" , "投资类型" : "混合类型" , "成立日期" : "2004-08-11" , "基金规模" : "40.10亿" , "最新净值" : "16.7690" , "交易币种" : "CNY"}];var html = '<table class="table table-bordered" style="height:100%"><thead><tr ><th colspan = "2">'+title+'</th></tr></thead><tbody>';for (var key in data[0]) {html += '<tr>';html += '<td>'+key+'</td><td>'+data[0][key]+'</td>';html += '</tr>';}html += '</tbody></table>';$("#$id$").empty().append(html);`

export default {
  scriptTxt1,
  scriptTxt2,
  scriptTxt3
}

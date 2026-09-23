const reportTypeMap = {
  A: '单产品绩效',
  B: '多组合分析',
  C: '汇总穿透分析'
}

const templateList = [
  {
    templateCode: 'single-performance-demo',
    templateName: '单产品绩效演示报告',
    paCrReportType: 'A',
    indexCodes: ['single_return', 'single_risk']
  },
  {
    templateCode: 'multi-portfolio-demo',
    templateName: '多组合分析演示报告',
    paCrReportType: 'B',
    indexCodes: ['multi_compare', 'multi_drawdown']
  },
  {
    templateCode: 'penetration-demo',
    templateName: '汇总穿透分析演示报告',
    paCrReportType: 'C',
    indexCodes: ['asset_allocation', 'industry_weight']
  }
]

export const reportTypeList = [
  { repTypeCode: 'A', repTypeName: reportTypeMap.A },
  { repTypeCode: 'B', repTypeName: reportTypeMap.B },
  { repTypeCode: 'C', repTypeName: reportTypeMap.C }
]

export const timeFrequencyList = [
  { dim_cde: 'day', dim_nme: '日频', dim_ord: 1 },
  { dim_cde: 'week', dim_nme: '周频', dim_ord: 2 },
  { dim_cde: 'month', dim_nme: '月频', dim_ord: 3 }
]

export const productList = [
  { fundCode: 'GJ001', fundName: '国君稳健一号', fundNameShort: '稳健一号', weight: 40 },
  { fundCode: 'GJ002', fundName: '国君成长精选', fundNameShort: '成长精选', weight: 35 },
  { fundCode: 'GJ003', fundName: '国君量化增强', fundNameShort: '量化增强', weight: 25 },
  { fundCode: 'GJ004', fundName: '国君均衡配置', fundNameShort: '均衡配置', weight: 20 }
]

export const benchmarkList = [
  { dim_cde: '000300', dim_nme: '沪深300' },
  { dim_cde: '000905', dim_nme: '中证500' },
  { dim_cde: '885001', dim_nme: '偏股混合基金指数' },
  { dim_cde: 'absolute', dim_nme: '绝对收益 5%' }
]

const indexPool = {
  single_return: {
    indexCode: 'single_return',
    indexName: '累计收益走势',
    html: '<div class="demo-chart" id="chart_single_return"></div>',
    jsContent: `<script>
      (function() {
        var data = \${rootData};
        var dom = document.getElementById('chart_single_return');
        if (!dom || !window.echarts) return;
        var chart = window.echarts.init(dom);
        chart.setOption({
          tooltip: { trigger: 'axis' },
          legend: { data: ['产品', '基准'], top: 0 },
          grid: { top: 45, left: 45, right: 24, bottom: 35 },
          xAxis: { type: 'category', boundaryGap: false, data: data.dates },
          yAxis: { type: 'value', axisLabel: { formatter: '{value}%' } },
          series: [
            { name: '产品', type: 'line', smooth: true, data: data.product },
            { name: '基准', type: 'line', smooth: true, data: data.benchmark }
          ]
        });
      })();
    <\/script>`
  },
  single_risk: {
    indexCode: 'single_risk',
    indexName: '风险收益指标',
    html: `<table class="demo-table">
      <thead>
        <tr>
          <th>指标</th>
          <th>本期值</th>
          <th>同类排名</th>
          <th>说明</th>
        </tr>
      </thead>
      <tbody id="table_single_risk"></tbody>
    </table>`,
    jsContent: `<script>
      (function() {
        var data = \${rootData};
        var tbody = document.getElementById('table_single_risk');
        if (!tbody) return;
        tbody.innerHTML = data.map(function(item) {
          return '<tr><td>' + item.name + '</td><td>' + item.value +
            '</td><td>' + item.rank + '</td><td>' + item.desc + '</td></tr>';
        }).join('');
      })();
    <\/script>`
  },
  multi_compare: {
    indexCode: 'multi_compare',
    indexName: '组合收益对比',
    html: '<div class="demo-chart" id="chart_multi_compare"></div>',
    jsContent: `<script>
      (function() {
        var data = \${rootData};
        var dom = document.getElementById('chart_multi_compare');
        if (!dom || !window.echarts) return;
        var chart = window.echarts.init(dom);
        chart.setOption({
          tooltip: { trigger: 'axis' },
          legend: { data: data.legend, top: 0 },
          grid: { top: 45, left: 45, right: 24, bottom: 35 },
          xAxis: { type: 'category', data: data.categories },
          yAxis: { type: 'value', axisLabel: { formatter: '{value}%' } },
          series: data.series.map(function(item) {
            return { name: item.name, type: 'bar', data: item.data };
          })
        });
      })();
    <\/script>`
  },
  multi_drawdown: {
    indexCode: 'multi_drawdown',
    indexName: '最大回撤对比',
    html: '<div class="demo-chart" id="chart_multi_drawdown"></div>',
    jsContent: `<script>
      (function() {
        var data = \${rootData};
        var dom = document.getElementById('chart_multi_drawdown');
        if (!dom || !window.echarts) return;
        var chart = window.echarts.init(dom);
        chart.setOption({
          tooltip: { trigger: 'axis' },
          grid: { top: 30, left: 45, right: 24, bottom: 35 },
          xAxis: { type: 'category', data: data.names },
          yAxis: { type: 'value', axisLabel: { formatter: '{value}%' } },
          series: [{ name: '最大回撤', type: 'bar', data: data.values }]
        });
      })();
    <\/script>`
  },
  asset_allocation: {
    indexCode: 'asset_allocation',
    indexName: '资产配置穿透',
    html: '<div class="demo-chart" id="chart_asset_allocation"></div>',
    jsContent: `<script>
      (function() {
        var data = \${rootData};
        var dom = document.getElementById('chart_asset_allocation');
        if (!dom || !window.echarts) return;
        var chart = window.echarts.init(dom);
        chart.setOption({
          tooltip: { trigger: 'item' },
          legend: { orient: 'vertical', left: 10, top: 20 },
          series: [{
            name: '资产占比',
            type: 'pie',
            radius: ['42%', '68%'],
            center: ['58%', '50%'],
            data: data
          }]
        });
      })();
    <\/script>`
  },
  industry_weight: {
    indexCode: 'industry_weight',
    indexName: '行业权重分布',
    html: '<div class="demo-chart" id="chart_industry_weight"></div>',
    jsContent: `<script>
      (function() {
        var data = \${rootData};
        var dom = document.getElementById('chart_industry_weight');
        if (!dom || !window.echarts) return;
        var chart = window.echarts.init(dom);
        chart.setOption({
          tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
          grid: { top: 30, left: 70, right: 24, bottom: 35 },
          xAxis: { type: 'value', axisLabel: { formatter: '{value}%' } },
          yAxis: { type: 'category', data: data.names },
          series: [{ name: '权重', type: 'bar', data: data.values }]
        });
      })();
    <\/script>`
  }
}

const indexData = {
  single_return: {
    dates: ['1月', '2月', '3月', '4月', '5月', '6月'],
    product: [0.8, 1.9, 1.5, 3.8, 5.1, 6.4],
    benchmark: [0.5, 1.1, 0.7, 2.2, 3.4, 4.2]
  },
  single_risk: [
    { name: '年化收益', value: '12.6%', rank: '前 18%', desc: '收益表现优于同类均值' },
    { name: '年化波动', value: '8.4%', rank: '前 42%', desc: '波动水平中等' },
    { name: '最大回撤', value: '-4.8%', rank: '前 25%', desc: '回撤控制较好' },
    { name: '夏普比率', value: '1.42', rank: '前 20%', desc: '风险调整后收益较优' }
  ],
  multi_compare: {
    categories: ['1月', '2月', '3月', '4月', '5月', '6月'],
    legend: ['稳健一号', '成长精选', '基准'],
    series: [
      { name: '稳健一号', data: [1.2, 2.1, 1.8, 3.4, 4.1, 5.2] },
      { name: '成长精选', data: [0.9, 1.8, 2.5, 3.1, 4.8, 5.9] },
      { name: '基准', data: [0.7, 1.5, 1.2, 2.4, 3.2, 4.0] }
    ]
  },
  multi_drawdown: {
    names: ['稳健一号', '成长精选', '量化增强', '基准'],
    values: [-3.2, -5.6, -4.1, -6.3]
  },
  asset_allocation: [
    { name: '股票', value: 48 },
    { name: '债券', value: 27 },
    { name: '基金', value: 15 },
    { name: '现金', value: 10 }
  ],
  industry_weight: {
    names: ['电子', '医药', '银行', '新能源', '消费'],
    values: [18, 14, 12, 10, 9]
  }
}

function clone(data) {
  return JSON.parse(JSON.stringify(data))
}

function delay(data, time) {
  return new Promise(resolve => {
    setTimeout(() => resolve(clone(data)), time || 250)
  })
}

export function getTemplateList() {
  return delay(templateList)
}

export function findTemplate(templateCode) {
  const template = templateList.find(item => item.templateCode === templateCode)
  if (!template) return delay({ template: null, indexList: [] })
  const indexList = template.indexCodes.map(code => indexPool[code]).filter(Boolean)
  return delay({ template, indexList })
}

export function findTemplateLevel(params) {
  return findTemplate(params.reportCode)
}

export function getIndexData(params) {
  return delay({
    State: 0,
    Data: indexData[params.indexCode] || null
  }, 350)
}

export function exportReport() {
  return delay({ State: 0, ErrMsg: '导出演示成功' }, 500)
}

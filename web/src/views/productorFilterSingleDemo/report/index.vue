<template>
  <div class="weekly-report">
    <div class="report-toolbar">
      <el-button size="small" icon="el-icon-arrow-left" @click="$router.back()">返回筛选</el-button>
    </div>
    <main class="report-paper">
      <header class="report-header">
        <div class="report-summary">
          <div class="report-title"><i class="el-icon-document"></i><h1>XXX稳健增长1号</h1></div>
          <div class="report-basic-info">
            <span>成立日期：2019-06-18</span><span>基金经理：XXX</span><span>投资顾问：XXX</span>
            <span>基金管理人：XXX资产管理有限公司</span><span>办公地：上海</span><span>策略分类：股票策略</span>
            <span>备案编号：XXX-0001</span><span>运行状态：运作中</span><span>数据来源：托管部自有数据</span>
          </div>
        </div>
        <div class="report-metrics">
          <div class="report-date"><strong>2026-08-14</strong><span>最新净值日期</span></div>
          <div v-for="metric in reportMetrics" :key="metric.label" class="metric-item" :class="metric.tone"><strong>{{ metric.value }}</strong><span>{{ metric.label }}</span></div>
        </div>
        <div class="report-query">
          <div class="report-query-fields">
            <label>统计周期：<el-select v-model="reportQuery.period" size="small"><el-option label="近一年" value="近一年"></el-option><el-option label="近三年" value="近三年"></el-option><el-option label="成立以来" value="成立以来"></el-option></el-select></label>
            <label>统计区间：<el-date-picker v-model="reportQuery.dates" type="daterange" size="small" value-format="yyyy-MM-dd" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期"></el-date-picker></label>
          </div>
          <div class="report-query-actions">
            <el-button class="report-query-button" size="small" @click="handleReportQuery">查询</el-button>
            <el-button class="report-query-button" size="small" @click="resetReportQuery">重置</el-button>
            <el-button class="report-query-button" size="small" @click="handleReportExport">导出</el-button>
          </div>
        </div>
      </header>

      <section class="report-section">
        <h2><span>产品基本信息</span></h2>
        <h3>产品基本信息</h3>
        <table class="info-table">
          <thead><tr><th>产品代码</th><th>产品名称</th><th>成立日期</th><th>管理人</th><th>投资经理</th><th>数据来源</th></tr></thead>
          <tbody><tr><td>XXX0001</td><td>XXX稳健增长1号</td><td>2019-06-18</td><td>XXX资产管理有限公司</td><td>XXX</td><td>托管部自有数据</td></tr></tbody>
        </table>
      </section>

      <section class="report-section">
        <h2><span>净值走势图 - 周频</span></h2>
        <h3>净值走势图 - 周频</h3>
        <div class="legend"><i class="blue"></i>单位净值 <i class="purple"></i>累计单位净值 <i class="yellow"></i>复权累计净值 <i class="orange"></i>沪深300指数</div>
        <div class="chart-card line-chart">
          <svg viewBox="0 0 1000 260" preserveAspectRatio="none" aria-label="净值走势图">
            <g class="grid"><line v-for="y in [30,70,110,150,190,230]" :key="y" x1="55" :y1="y" x2="960" :y2="y" /></g>
            <line class="axis" x1="55" y1="230" x2="960" y2="230" />
            <polyline class="series blue-line" points="55,55 210,61 365,71 520,89 675,107 830,125 960,142" />
            <polyline class="series purple-line" points="55,50 210,55 365,67 520,86 675,105 830,122 960,137" />
            <polyline class="series yellow-line" points="55,52 210,72 365,83 520,64 675,77 830,106 960,149" />
            <polyline class="series orange-line" points="55,54 210,76 365,88 520,69 675,90 830,118 960,158" />
            <text v-for="(date, index) in dates" :key="date" :x="55 + index * 151" y="252">{{ date }}</text>
          </svg>
        </div>
        <p class="note">注：净值与指数均已归一化处理。</p>
      </section>

      <section class="report-section">
        <h2><span>收益率状况 - 周频</span></h2>
        <h3>收益率状况 - 周频</h3>
        <div class="chart-card return-chart">
          <div class="return-axis"><span>4%</span><span>2%</span><span>0%</span><span>-2%</span><span>-4%</span></div>
          <div class="bars"><div v-for="item in weeklyReturns" :key="item.date" class="bar-group"><div class="bar" :class="item.value >= 0 ? 'positive' : 'negative'" :style="{ height: Math.abs(item.value) * 33 + 'px' }"></div><span>{{ item.date }}</span></div></div>
        </div>
        <div class="legend centered"><i class="blue"></i>组合收益率（%）<i class="orange"></i>周收益率（右）</div>
        <p class="note">注：组合区间最高周收益率为 3.6105%，最低周收益率为 -2.8877%。</p>
        <h3>组合周收益率分布</h3>
        <table><thead><tr><th>最大值</th><th>最小值</th><th>平均值</th><th>标准差</th><th>偏度</th><th>峰度</th><th>25%分位数</th><th>中位数</th><th>75%分位数</th></tr></thead><tbody><tr><td>3.6105%</td><td>-2.8877%</td><td>-0.7429%</td><td>2.9824%</td><td>0.84</td><td>-1.35</td><td>-2.6217%</td><td>-1.8473%</td><td>0.3105%</td></tr></tbody></table>
        <div class="histogram"><span>频率 / 周</span><div v-for="(height, index) in [100,100,0,0,100,0,0,0,100]" :key="index" class="histogram-bar" :style="{ height: height + '%' }"></div></div>
        <h3>阶段收益指标</h3>
        <table><thead><tr><th>组合指标</th><th>过去一月（%）</th><th>过去三个月（%）</th><th>过去六个月（%）</th><th>今年以来（%）</th></tr></thead><tbody><tr v-for="item in periodReturns" :key="item.name"><td>{{ item.name }}</td><td>{{ item.m1 }}</td><td>{{ item.m3 }}</td><td>{{ item.m6 }}</td><td>{{ item.ytd }}</td></tr></tbody></table>
      </section>

      <section class="report-section">
        <h2><span>最大回撤及盈亏占比（复权）- 周频</span></h2>
        <h3>最大回撤及盈亏占比（复权）- 周频</h3>
        <div class="two-charts">
          <div class="mini-chart"><div class="drawdown-bars"><div v-for="item in drawdowns" :key="item.label" :style="{ height: item.value * 22 + 'px' }"></div></div><div class="chart-labels"><span v-for="item in drawdowns" :key="item.label">{{ item.label }}</span></div><div class="legend centered"><i class="blue"></i>组合</div></div>
          <div class="mini-chart"><div class="donut"><span>25%<small>盈利周</small></span></div><div class="legend centered"><i class="blue"></i>盈利周 <i class="red"></i>亏损周</div></div>
        </div>
        <table class="dense-table"><thead><tr><th>期间</th><th>项目</th><th>最大回撤（%）</th><th>最大回撤期间</th><th>最大回撤修复天数</th><th>平均周收益（%）</th><th>最大周盈利（%）</th><th>最大周亏损（%）</th><th>盈利周平均收益（%）</th><th>亏损周平均收益（%）</th><th>盈利周占比（%）</th></tr></thead><tbody><tr v-for="item in drawdownTable" :key="item.period + item.kind"><td>{{ item.period }}</td><td>{{ item.kind }}</td><td>{{ item.drawdown }}</td><td>{{ item.range }}</td><td>{{ item.recover }}</td><td>{{ item.avg }}</td><td>{{ item.max }}</td><td>{{ item.min }}</td><td>{{ item.win }}</td><td>{{ item.loss }}</td><td>{{ item.winRate }}</td></tr></tbody></table>
        <h3>收益风险比 - 周频</h3>
        <table class="dense-table"><thead><tr><th>指标</th><th>报告区间</th><th>近1月</th><th>近3月</th><th>近6月</th><th>今年以来</th><th>近1年</th><th>近2年</th><th>近3年</th><th>成立以来</th></tr></thead><tbody><tr v-for="item in riskMetrics" :key="item.name"><td>{{ item.name }}</td><td v-for="(value, index) in item.values" :key="index">{{ value }}</td></tr></tbody></table>
        <p class="note">注：收益风险比指标基于周频复权净值测算，全部数据均为脱敏模拟值。</p>
      </section>

      <footer>产品筛选 Demo · 周频净值报告 · 脱敏静态数据</footer>
    </main>
  </div>
</template>

<script>
export default {
  name: 'ProductorFilterSingleDemoReport',
  data() {
    return {
      dates: ['01-05', '02-02', '03-02', '04-06', '05-11', '06-15', '08-14'],
      reportMetrics: [
        { label: '单位净值', value: '1.4370', tone: 'positive' },
        { label: '累计净值', value: '1.9930', tone: 'positive' },
        { label: '近三月收益率', value: '8.62%', tone: 'positive' },
        { label: '今年以来收益率', value: '12.45%', tone: 'positive' },
        { label: '近一年收益率', value: '18.36%', tone: 'positive' },
        { label: '成立以来最大回撤', value: '-6.55%', tone: 'negative' },
        { label: '成立以来 Sharpe 比率', value: '1.28', tone: 'positive' }
      ],
      reportQuery: {
        period: '近一年',
        dates: ['2025-08-15', '2026-08-14'],
      },
      weeklyReturns: [{ date: '01-09', value: 3.1 }, { date: '02-06', value: -1.4 }, { date: '03-06', value: -3.0 }, { date: '04-03', value: 0.2 }, { date: '05-08', value: -2.7 }],
      periodReturns: [{ name: '组合收益率', m1: '-3.0693', m3: '-3.0693', m6: '-3.0693', ytd: '-3.0693' }, { name: '组合标准差', m1: '2.9824', m3: '1.5375', m6: '1.0722', ytd: '2.9824' }],
      drawdowns: [{ label: '报告区间', value: 6.55 }, { label: '近1个月', value: 6.55 }, { label: '近3个月', value: 6.55 }, { label: '近6个月', value: 6.55 }, { label: '近12个月', value: 6.55 }, { label: '成立以来', value: 6.55 }],
      drawdownTable: [{ period: '报告区间', kind: '组合', drawdown: '-6.5470', range: '[20260107-20260218]', recover: '-', avg: '-0.7429', max: '3.6105', min: '-2.8877', win: '3.6105', loss: '-2.1941', winRate: '25.0000' }, { period: '近1个月', kind: '组合', drawdown: '-6.5470', range: '[20260107-20260218]', recover: '-', avg: '-0.7429', max: '3.6105', min: '-2.8877', win: '3.6105', loss: '-2.1941', winRate: '25.0000' }, { period: '近3个月', kind: '组合', drawdown: '-6.5470', range: '[20260107-20260218]', recover: '-', avg: '-0.7429', max: '3.6105', min: '-2.8877', win: '3.6105', loss: '-2.1941', winRate: '25.0000' }, { period: '成立以来', kind: '组合', drawdown: '-6.5470', range: '[20190618-20260218]', recover: '67', avg: '0.2003', max: '25.4858', min: '-19.1897', win: '8.6234', loss: '-7.6419', winRate: '48.2143' }],
      riskMetrics: [{ name: '收益率（%）', values: ['-3.0693', '-3.0693', '-3.0693', '-3.0693', '-3.0693', '-14.1173', '-15.6511', '-15.6511', '18.3600'] }, { name: '年化收益率（%）', values: ['-33.3198', '-33.3198', '-33.3198', '-33.3198', '-33.3198', '-14.1173', '-14.6194', '-14.6194', '12.4500'] }, { name: '年化波动率（%）', values: ['21.5066', '21.5066', '21.5066', '21.5066', '21.5066', '75.5341', '72.8058', '72.8058', '16.8205'] }, { name: '最大回撤（复权）（%）', values: ['-6.5470', '-6.5470', '-6.5470', '-6.5470', '-6.5470', '-6.5470', '-6.5470', '-6.5470', '-6.5470'] }, { name: '夏普指数', values: ['-1.6190', '-1.6190', '-1.6190', '-1.6190', '-1.6190', '-0.2068', '-0.2214', '-0.2214', '1.2800'] }, { name: '卡玛比率', values: ['-5.0893', '-5.0893', '-5.0893', '-5.0893', '-5.0893', '-2.1563', '-2.2330', '-2.2330', '1.8800'] }],
    }
  },
  methods: {
    handleReportQuery() {
      this.$message.success('已按当前条件展示静态报告数据')
    },
    resetReportQuery() {
      this.reportQuery = {
        period: '近一年',
        dates: ['2025-08-15', '2026-08-14'],
      }
    },
    handleReportExport() {
      const blob = new Blob(['\ufeff产品代码,产品名称,数据来源,统计周期\nXXX0001,XXX稳健增长1号,托管部自有数据,' + this.reportQuery.period], { type: 'text/csv;charset=utf-8' })
      const link = document.createElement('a')
      link.href = window.URL.createObjectURL(blob)
      link.download = '周频净值报告-静态测试数据.csv'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(link.href)
    }
  }
}
</script>

<style lang="scss" scoped>
.weekly-report { min-height: 100%; background: #f3f5f8; color: #3f4650; padding: 16px 0 42px; }
.report-toolbar { width: 1160px; margin: 0 auto 12px; display: flex; justify-content: space-between; align-items: center; color: #8994a5; font-size: 13px; }
.report-paper { width: 1160px; margin: 0 auto; padding: 40px 54px 30px; box-sizing: border-box; background: #fff; box-shadow: 0 2px 12px rgba(39, 60, 90, .08); }
.report-header { border-bottom: 1px solid #d9e3f3; margin-bottom: 30px; padding-bottom: 16px; }
.report-summary { display: flex; align-items: center; justify-content: space-between; min-height: 84px; padding: 0 18px; }
.report-title { display: flex; align-items: center; min-width: 310px; color: #45566e; }
.report-title i { margin-right: 12px; color: #d59b64; font-size: 30px; }
.report-header h1 { margin: 0; color: #45566e; font-size: 22px; font-weight: 500; }
.report-basic-info { display: grid; grid-template-columns: repeat(3, minmax(170px, 1fr)); gap: 8px 24px; flex: 1; color: #526071; font-size: 12px; line-height: 1.45; }
.report-metrics { display: flex; align-items: stretch; border-top: 1px dashed #aeb8c6; border-bottom: 1px dashed #aeb8c6; }
.report-date, .metric-item { display: flex; flex: 1; flex-direction: column; justify-content: center; min-height: 68px; padding: 7px 12px; text-align: center; }
.report-date { flex: 1.35; border-right: 1px solid #edf0f4; color: #45566e; }
.report-date strong { font-size: 21px; font-weight: 500; }
.metric-item strong { color: #e45250; font-size: 21px; font-weight: 600; line-height: 1.3; }
.metric-item.negative strong { color: #26a56a; }
.report-date span, .metric-item span { margin-top: 4px; color: #687586; font-size: 12px; }
.report-query { display: flex; align-items: center; gap: 16px; padding: 16px 18px; border-top: 1px solid #edf0f4; color: #596779; font-size: 12px; }
.report-query-fields { display: grid; grid-template-columns: 250px 370px; align-items: center; column-gap: 16px; }
.report-query-actions { display: flex; gap: 10px; }
.report-query-actions .report-query-button { width: 72px; margin: 0; color: #76461f; background: #f3d2b5; border-color: #e9bd98; }
.report-query-actions .report-query-button:hover, .report-query-actions .report-query-button:focus { color: #76461f; background: #ecc29e; border-color: #e0ad84; }
.report-query label { display: inline-flex; align-items: center; white-space: nowrap; }
.report-query ::v-deep .el-select { width: 104px; }
.report-query ::v-deep .el-date-editor { width: 244px; }
.report-header p, .note { color: #8390a0; font-size: 12px; line-height: 1.8; }
.report-section { margin: 0 0 42px; }
h2 { display: flex; align-items: center; gap: 16px; color: #7e9fd2; font-size: 15px; font-weight: 400; margin: 0 0 26px; }
h2::before, h2::after { content: ''; height: 1px; flex: 1; background: #8eaee1; } h2 span { white-space: nowrap; }
h3 { text-align: center; color: #303741; font-size: 14px; font-weight: 500; margin: 0 0 18px; }
table { width: 100%; border-collapse: collapse; table-layout: fixed; font-size: 12px; margin: 0 0 18px; } th, td { border: 1px solid #d7dce4; padding: 7px 4px; text-align: center; word-break: break-all; } th { background: #dce5f3; color: #596473; font-weight: 400; } tbody tr:nth-child(even) { background: #f5f7fa; }
.info-table th:nth-child(4) { width: 29%; } .legend { color: #596473; font-size: 12px; margin: 0 0 12px; } .legend.centered { text-align: center; margin-top: 10px; } .legend i { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin: 0 5px 0 16px; } .legend i:first-child { margin-left: 0; } .blue { background: #1487c9; } .purple { background: #7c68b7; } .yellow { background: #f4ba39; } .red { background: #fa1748; } .orange { background: #fb8351; }
.chart-card { position: relative; border: 1px solid #edf0f4; padding: 12px; } .line-chart { height: 270px; } .line-chart.compact { height: 220px; } svg { width: 100%; height: 100%; } .grid line { stroke: #d5d9df; stroke-dasharray: 2 3; } .axis { stroke: #a6afbb; } .series { fill: none; stroke-width: 2; } .blue-line { stroke: #1487c9; } .purple-line { stroke: #7c68b7; } .yellow-line { stroke: #f4ba39; } .red-line { stroke: #fa1748; } .orange-line { stroke: #fb8351; } svg text { fill: #778290; font-size: 12px; text-anchor: middle; }
.return-chart { height: 220px; display: flex; align-items: center; } .return-axis { height: 170px; display: flex; flex-direction: column; justify-content: space-between; color: #75808d; font-size: 12px; } .bars { flex: 1; height: 170px; display: flex; align-items: center; justify-content: space-around; border-bottom: 1px solid #acb3bd; background: repeating-linear-gradient(to bottom, transparent 0, transparent 41px, #d9dde2 42px); } .bar-group { height: 100%; width: 74px; display: flex; flex-direction: column; align-items: center; justify-content: center; font-size: 11px; } .bar { width: 32px; } .bar.positive { background: #fb8351; align-self: center; margin-bottom: 2px; } .bar.negative { background: #fb8351; align-self: center; margin-top: 2px; } .bar-group span { margin-top: 78px; transform: rotate(90deg); white-space: nowrap; } .return-chart svg { position: absolute; left: 88px; right: 20px; top: 33px; width: calc(100% - 108px); height: 160px; pointer-events: none; }
.histogram { height: 130px; border-bottom: 1px solid #9fa8b3; display: flex; align-items: flex-end; gap: 7%; padding: 0 28px; position: relative; margin: 16px 0 30px; background: repeating-linear-gradient(to bottom, transparent 0, transparent 32px, #dde1e6 33px); } .histogram > span { position: absolute; left: 0; top: -20px; font-size: 12px; color: #67717f; } .histogram-bar { width: 10px; background: #1487c9; } .histogram.excess { margin-top: 28px; }
.two-charts { display: flex; gap: 34px; margin-bottom: 24px; } .mini-chart { flex: 1; min-height: 220px; } .drawdown-bars { height: 150px; display: flex; align-items: flex-start; justify-content: space-around; border-bottom: 1px solid #a9b1bb; padding-top: 8px; background: repeating-linear-gradient(to bottom, transparent 0, transparent 25px, #d9dde2 26px); } .drawdown-bars div { width: 26px; background: #1487c9; } .chart-labels { display: flex; justify-content: space-around; font-size: 11px; color: #6d7783; margin-top: 8px; } .donut { width: 120px; height: 120px; margin: 22px auto 14px; border-radius: 50%; background: conic-gradient(#1487c9 0 25%, #fa1748 25% 100%); position: relative; display: flex; align-items: center; justify-content: center; } .donut::after { content: ''; position: absolute; width: 66px; height: 66px; border-radius: 50%; background: #fff; } .donut span { z-index: 1; color: #556271; font-size: 14px; text-align: center; } .donut small { display: block; font-size: 10px; margin-top: 3px; }
.dense-table { font-size: 11px; } .dense-table th, .dense-table td { padding: 6px 3px; } footer { border-top: 1px solid #a5b9d9; padding-top: 14px; color: #8c97a5; text-align: center; font-size: 12px; }
@media screen and (max-width: 1200px) { .report-toolbar, .report-paper { width: calc(100% - 24px); } .report-paper { padding: 28px 20px; } } @media screen and (max-width: 760px) { .two-charts { flex-direction: column; } .report-paper { overflow-x: auto; } table { min-width: 760px; } .report-query { flex-direction: column; align-items: flex-start; } .report-query-fields { grid-template-columns: 1fr; row-gap: 10px; } }
</style>

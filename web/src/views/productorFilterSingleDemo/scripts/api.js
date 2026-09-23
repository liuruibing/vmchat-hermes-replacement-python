const demoFunds = [
  ['XXX0001', 'XXX稳健增长1号', '火富牛', 'XXX资产管理有限公司', '股票策略', '主观多头', '消费成长'],
  ['XXX0002', 'XXX量化优选2号', '机构部', 'XXX私募基金管理有限公司', '股票策略', '量化选股', '指数增强'],
  ['XXX0003', 'XXX固收增强3号', '托管部自有数据', 'XXX投资管理有限公司', '固定收益策略', '信用债策略', '中高等级信用债'],
  ['XXX0004', 'XXX多策略精选4号', '美市数据源', 'XXX基金管理有限公司', '多策略', '复合策略', '套利策略'],
  ['XXX0005', 'XXX市场中性5号', '火富牛', 'XXX财富管理有限公司', '股票策略', '市场中性', '阿尔法策略'],
  ['XXX0006', 'XXXCTA趋势6号', '机构部', 'XXX投资咨询有限公司', 'CTA策略', '趋势跟踪', '商品趋势'],
  ['XXX0007', 'XXX红利精选7号', '托管部自有数据', 'XXX资本管理有限公司', '股票策略', '量化选股', '红利增强'],
  ['XXX0008', 'XXX套利机会8号', '美市数据源', 'XXX资产管理有限公司', '套利策略', '期现套利', '跨期套利'],
  ['XXX0009', 'XXX均衡配置9号', '火富牛', 'XXX私募基金管理有限公司', '组合基金策略', 'FOF策略', '多资产配置'],
  ['XXX0010', 'XXX宏观对冲10号', '机构部', 'XXX投资管理有限公司', '宏观策略', '宏观对冲', '利率策略'],
  ['XXX0011', 'XXX绝对收益11号', '托管部自有数据', 'XXX基金管理有限公司', '固定收益策略', '可转债策略', '固收加'],
  ['XXX0012', 'XXX灵活配置12号', '美市数据源', 'XXX财富管理有限公司', '股票策略', '事件驱动', '并购重组'],
  ['XXX0012', 'XXX灵活配置12号', '托管部自有数据', 'XXX财富管理有限公司', '股票策略', '事件驱动', '并购重组'],
  ['XXX0012', 'XXX灵活配置12号', '火富牛', 'XXX财富管理有限公司', '股票策略', '事件驱动', '并购重组'],
  ['XXX0012', 'XXX灵活配置12号', '机构部', 'XXX财富管理有限公司', '股票策略', '事件驱动', '并购重组']
].map((item, index) => {
  const factor = index + 1
  return {
    fundCode: item[0],
    fundName: item[1],
    source: item[2],
    companyName: item[3],
    fofMainStrategyName: item[4],
    fofSubStrategyName: item[5],
    fofThirdStrategyName: item[6],
    foundDate: `20${16 + index}-0${index % 8 + 1}-15`,
    navDate: '2026-08-14',
    unitNav: 0.92 + factor * 0.047,
    addedNav: 1.08 + factor * 0.083,
    m1_return: -0.012 + factor * 0.006,
    m1_max_retracement: -(0.011 + factor * 0.003),
    m1_sharpe: 0.72 + factor * 0.09,
    m3_return: -0.018 + factor * 0.014,
    m3_max_retracement: -(0.026 + factor * 0.005),
    m3_sharpe: 0.66 + factor * 0.1,
    m6_return: -0.024 + factor * 0.021,
    m6_max_retracement: -(0.042 + factor * 0.006),
    m6_sharpe: 0.61 + factor * 0.11,
    y1_return: -0.03 + factor * 0.032,
    y1_max_retracement: -(0.068 + factor * 0.007),
    y1_sharpe: 0.58 + factor * 0.12,
    ytd_return: -0.02 + factor * 0.018,
    ytd_max_retracement: -(0.035 + factor * 0.005),
    ytd_sharpe: 0.64 + factor * 0.09,
    isConcern: index % 4 === 0 ? '1' : '0',
    gfSelling: index % 3 === 0 ? '代销' : '非代销'
  }
})

/**
 * @description Demo 查询列表：仅返回前端脱敏模拟数据
 */
export const findList = data => {
  const keyword = (data.fundName || '').trim().toLowerCase()
  const managerName = (data.managerName || '').trim().toLowerCase()
  const order = (data.orderString || '').split(' ')
  const rows = demoFunds
    .filter(item => !keyword || item.fundName.toLowerCase().includes(keyword) || item.fundCode.toLowerCase().includes(keyword))
    .filter(item => !managerName || item.companyName.toLowerCase().includes(managerName))
    .sort((left, right) => {
      const field = order[0]
      const direction = order[1] === 'asc' ? 1 : -1
      if (!field || left[field] === right[field]) return 0
      return left[field] > right[field] ? direction : -direction
    })
  const offset = Number(data.offset) || 0
  const limit = Number(data.limit) || rows.length

  return Promise.resolve({
    data: {
      status: 0,
      data: {
        rows: rows.slice(offset, offset + limit),
        total: rows.length
      }
    }
  })
}

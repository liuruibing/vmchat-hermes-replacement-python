"""Curated interpretation of the local catalogue, not evidence about a mandate.

Definitions below are derived from the catalogue's algorithms. FIBO supplies the
modelling method (definition, distinguishing characteristics and provenance), not
an assertion that these local formulas are universal financial standards.
"""
from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import json
from pathlib import Path

from app.mandate_risk.models import RawRiskMetric

ANNOTATED_CATALOGUE_SHA256 = "4163180c3f3cc921e23fe7d553ccf7975ca6231430a86cefcf7ef2180481a261"
KNOWLEDGE_VERSION = "mandate-concepts-1"
SOURCES = {
    "local_catalogue": "指标知识库.md (以各行算法为准；本模块为辅助解释，未经业务专家审核)",
    "modelling_method": "https://github.com/edmcouncil/fibo/blob/master/ONTOLOGY_GUIDE.md",
    "tracking_error_reference": "https://github.com/PyPortfolio/PyPortfolioOpt/blob/main/pypfopt/objective_functions.py",
    "return_metrics_reference": "https://github.com/ranaroussi/quantstats/blob/main/quantstats/stats.py",
}

# Exact catalogue names, not fuzzy aliases. None of these annotations may supply
# missing contractual operands, objects, thresholds or investment requirements.
_CONCEPTS = {
    "基金收益率": {
        "definition": "组合在观察期间的复合收益；本库采用各期(1+r)连乘减1。",
        "aliases": ["portfolio return", "fund return"],
        "distinguish_from": "总回报或资本增长目标可对应收益概念；不自动对应Alpha、波动率或下行Beta。",
    },
    "超额收益率（基准超额）": {
        "definition": "组合收益减指定基准收益，Ri-Bi。",
        "aliases": ["excess return over benchmark", "active return"],
        "distinguish_from": "不作Beta或无风险利率调整；不同于本库Alpha和信息比率。",
    },
    "Alpha": {
        "definition": "Ri-[Rf+beta*(Rm-Rf)]，扣除按Beta估计的市场风险补偿后的收益。",
        "aliases": ["Jensen's alpha", "Jensen alpha"],
        "distinguish_from": "仅要求跑赢基准不支持引入Rf和Beta调整；普通超额收益不是本库Alpha的同义词。",
    },
    "股息贡献率": {
        "definition": "股息收益在整体收益中的比重。分母是整体收益。",
        "aliases": [],
        "distinguish_from": "不同于股息/投资市值的股息收益率；稳定股息目标不要求计算贡献比重。",
    },
    "Sortino索提诺": {
        "definition": "(Rp-Rf)/下行波动率，按下行风险调整的超额收益。",
        "aliases": ["Sortino ratio"],
        "distinguish_from": "下行波动率不是基准下跌条件下的Beta；增长目标或主动管理不支持引入该风险调整比率。",
    },
    "信息比率": {
        "definition": "本库以基金减基准收益除以经实际天数处理的跟踪误差；保留原算法，不用外部实现覆盖。",
        "aliases": ["information ratio"],
        "distinguish_from": "同时出现超额收益与跟踪误差不等于要求二者的比率。",
    },
    "VaR": {
        "definition": "给定置信度与持有期的损失分位数；本库列出历史与正态方法及金额换算。",
        "aliases": ["value at risk"],
        "distinguish_from": "不同于最大回撤或波动率；一般风险政策未给出VaR要求时不能代为补充。",
    },
    "最大回撤": {
        "definition": "观察区间内从前期峰值至后续低点的最大相对跌幅。",
        "aliases": ["maximum drawdown", "max drawdown", "MDD"],
        "distinguish_from": "是路径峰谷损失，不是收益标准差或VaR分位数。",
    },
    "波动率": {
        "definition": "组合收益率的标准差。",
        "aliases": ["return volatility"],
        "distinguish_from": "不同于主动收益标准差(跟踪误差)或仅下行样本的风险度量。",
    },
    "组合Beta贝塔": {
        "definition": "Cov(组合收益,基准收益)/Var(基准收益)，全样本的相对市场敏感度。",
        "aliases": ["portfolio beta", "market beta"],
        "distinguish_from": "与基准比较或采用增强指数不等于要求Beta；不含下行样本筛选。",
    },
    "下行Beta": {
        "definition": "仅在基准日收益<0的样本上计算Cov(组合收益,基准收益)/Var(基准收益)。",
        "aliases": ["downside beta"],
        "distinguish_from": "泛下行风险、资本增长、低跟踪误差均不充分；不要求名称出现，但需该条件敏感度或等价公式的原文依据。",
    },
    "行业偏离度": {
        "definition": "组合行业权重减基准同行业权重，是相对偏离。",
        "aliases": ["active sector weight"],
        "distinguish_from": "单行业绝对敞口上限没有减基准操作，不是本指标；执行行业策略也不自动要求相对偏离。",
    },
    "跟踪误差": {
        "definition": "主动收益Rp-Rb的标准差。",
        "aliases": ["tracking error"],
        "distinguish_from": "事前预测与事后历史估计仍可对应跟踪误差概念，但不能声称实现等价。方差/平方和不能不经归一化、开方及口径核实冒充标准差。",
    },
    "久期": {
        "definition": "按债券全价市值加权的久期；具体久期类型原库未说明。",
        "aliases": ["portfolio duration"],
        "distinguish_from": "不同于剩余期限和以金额表示的DV01；不得默认Macaulay与修正久期相同。",
    },
    "DV01": {
        "definition": "本库为修正久期×市值×0.0001，表示利率变动1bp对应的价值敏感度幅度。",
        "aliases": ["dollar value of a basis point"],
        "distinguish_from": "PV01须核实曲线和定价口径；久期要求不自动等于金额敏感度要求。",
    },
    "股息支付率NII": {
        "definition": "按本库为NII/账面余额净值；不按名称猜成常见股息派息率。",
        "aliases": [],
        "distinguish_from": "NII收入及账面分母不同于每股股息/股价；不得把稳定股息目标等同于该库算法。",
    },
    "股息增长率": {
        "definition": "本期相对上期每股股息的增长百分比。",
        "aliases": ["dividend growth rate"],
        "distinguish_from": "股息增长不等于股息收益率；稳定股息收益目标未必要求逐期增长。",
    },
    "股息覆盖率": {
        "definition": "本库为组合股息率/基准股息率。",
        "aliases": [],
        "distinguish_from": "不是常见的盈利/股息覆盖倍数，也不是组合股息率本身；须有相对基准比值要求。",
    },
    "境内资产占比": {
        "definition": "境内资产配置比例；本库算法为空，境内认定与分母尚未规定。",
        "aliases": [],
        "distinguish_from": "境内发行人、境内上市地、风险所在国和币种并非同一判据；有境内配置原文可以关联，但不得补造比例、分母或70%门槛。",
    },
    "单一证券占比": {
        "definition": "单一证券/组合资产总值，按证券身份而非发行人汇总。",
        "aliases": ["single security exposure ratio"],
        "distinguish_from": "single name要结合正文确认；发行人可能有多只证券。组合资产总值与组合市值的等价性未必已知。",
    },
    "可用融资余额": {
        "definition": "受托组合规模×20%-已用正回购额度。",
        "aliases": [],
        "distinguish_from": "可用正回购融资额度不是借款或回购禁令的同义测量；不能把禁令转成该20%额度。",
    },
    "换手率(%)": {
        "definition": "(期间买入金额+期间卖出金额)/平均持仓市值；不擅自加上1/2。",
        "aliases": ["portfolio turnover ratio"],
        "distinguish_from": "执行交易策略或主动管理不自动要求衡量交易量相对持仓的比率。",
    },
    "剩余期限": {
        "definition": "按债券全价市值加权的剩余期限。",
        "aliases": ["weighted average remaining maturity"],
        "distinguish_from": "现金等价物的准入到期年限不是全组合平均期限，也不同于久期。",
    },
    "非标剩余期限": {
        "definition": "按非标资产余额加权的剩余期限。",
        "aliases": [],
        "distinguish_from": "非标对象与债券或现金等价物不同；仅许可某种期限工具不支持组合加权平均。",
    },
    "债券资产变现天数": {
        "definition": "债券持仓量/过去3个月平均日交易量，假设30%参与率。",
        "aliases": [],
        "distinguish_from": "对象为债券、结果为天数；不是某期限内可变现资产的占比。",
    },
    "流通受限资产占比": {
        "definition": "关注新股、封闭式基金等有锁定期的受限资产；本库仅描述对象，未给分母。",
        "aliases": [],
        "distinguish_from": "允许IPO证券或列明可投资工具不等于要求受限资产占比。",
    },
    "优质动性资产占比": {
        "definition": "优质流动性资产/账户规模；本库未规定优质资产认定。",
        "aliases": [],
        "distinguish_from": "不直接等同于监管HQLA或流动性覆盖率；未定义的资产认定保持未知。",
    },
    "流动性上市权益资产占比": {
        "definition": "组合全部上市股权市值中，按3个月平均日成交量、10%参与率可在7交易日内清算部分的市值占比。",
        "aliases": [],
        "distinguish_from": "第三方基金底层资产1天/7天可变现条件不能替换成全组合该占比；范围、层级和参与率均需依据。",
    },
    "信用利差（债券）": {
        "definition": "按本库信用债到期收益率减同期限国债收益率；参照券选择细节须按原算法核实。",
        "aliases": [],
        "distinguish_from": "是债券收益率差，不是信用评级、股票超额收益或泛信用风险要求。",
    },
    "信用利差（非标）": {
        "definition": "非标到期收益率减同期限或30年国债收益率，具体分支按本库。",
        "aliases": [],
        "distinguish_from": "对象为非标而非债券；不能只凭高质量公司或资本增长目标关联。",
    },
    "加权平均信用评级": {
        "definition": "本库WARF为评级因子乘权重后汇总；因子表及完整口径未给。",
        "aliases": ["weighted average rating factor", "WARF"],
        "distinguish_from": "评级因子汇总不同于某评级档的持仓占比；不猜出缺失评级映射。",
    },
    "债券AA+及以下评级占比(%)": {
        "definition": "AA+及以下评级债券合计占比；完整分母原库未明示。",
        "aliases": [],
        "distinguish_from": "具体信用评级档要求不同于投资高质量股票或加权平均评级。",
    },
    "单一发行人集中度": {
        "definition": "单一发行人汇总敞口/总资产。",
        "aliases": ["single issuer concentration"],
        "distinguish_from": "同一发行人可有多只证券，不能替换单一证券占比；总资产、NAV、AUM、市场价值不能无条件互换。",
    },
    "区域分布": {
        "definition": "区域分布概念；本库算法为空，分类地理口径和分母未规定。",
        "aliases": [],
        "distinguish_from": "泛地理交易策略不自动要求区域分布统计；上市地、发行人所在地、收入来源需区分。",
    },
}


@lru_cache(maxsize=1)
def _annotated_rows() -> dict[int, dict]:
    path = Path(__file__).resolve().parents[2] / "指标知识库.generated.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload["source"]["sha256"] != ANNOTATED_CATALOGUE_SHA256:
        return {}
    return {row["row_id"]: row for row in payload["metrics"]}


def metric_concept_reference(row: RawRiskMetric) -> dict | None:
    """Return a version-bound reference; custom or changed rows stay unknown."""
    expected = _annotated_rows().get(row.row_id)
    if (expected is None or expected["metric_name"] != row.metric_name
            or expected["algorithm"] != row.algorithm):
        return None
    concept = _CONCEPTS.get(row.metric_name)
    if concept is None:
        return None
    return {"version": KNOWLEDGE_VERSION, "source": "local_catalogue",
            **deepcopy(concept)}

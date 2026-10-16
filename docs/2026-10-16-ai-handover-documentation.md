# Mandate 风险指标识别系统 — AI 交接与架构全景文档 (2026-10-16)

> 本文档汇总了 Mandate 智能分析系统在 **2026-10-14 至 2026-10-16** 期间完成的全部架构重构、精度优化、速度压测、可追溯评测基线及运维部署信息，方便后续交接与持续迭代。

---

## 一、工程环境与分支信息

* **工程路径**：`/Volumes/onePiece/公司前端项目/AI项目/vmchat-hermes-replacement-python`
* **最新开发与交付分支**：`research/mandate-risk-speed-2026-10-14`
* **远程仓库推送状态**：
  * 公司内部 GitLab (`origin`)：已推送至 `research/mandate-risk-speed-2026-10-14`
  * 外部备份 GitHub (`github`)：已同步推送
* **核心提交哈希**：`37aa8ef`
* **关联前端工程**：
  * 路径：`/Volumes/onePiece/公司前端项目/友邦绩效/datadriver-fund-amc-tyjx-vue`
  * 访问地址：`http://localhost:9528/#/mandate-risk-v2/index`
  * 前端原则：**未变动任何前端代码，保持既有“上半区委托原文 + 下半区六列指标表”布局与原格式 Excel 导出。**

---

## 二、本次重点完成的核心优化

### 1. 概念消歧参考模块 (`app/mandate_risk_v2/concept_knowledge.py`)
针对大模型在金融术语上容易把“相关工具”误当“合同要求”的问题，引入了防过期的轻量知识参考：
* **34 项指标全覆盖**：基于本地 `指标知识库.md` 提取定义、精准英文别名、测量对象、汇总层级与近邻区分边界。
* **参考权威方法**：吸收 EDM Council FIBO 的概念建模方法，以及 QuantStats / PyPortfolioOpt 的跟踪误差与超额收益实现细节。
* **版本与防篡改绑定**：严格绑定底层指标库 SHA-256（`4163180c…`）、行号及原算法；指标库若有变动直接失效返回 `None`，杜绝旧知识污染新指标。
* **边界消歧实效**：
  * 区分 Single Security（单只证券）与 Single Issuer（单一发行人）；
  * 区分行业偏离度（相对基准偏离）与单行业绝对敞口上限；
  * 区分股息收益率与股息贡献率 / 增长率 / 覆盖率；
  * 区分第三方基金底层流动性条件与本组合流动性要求。

### 2. 候选准入与复核双重门禁
* **收紧准入门禁 (`mapping_validator.py`)**：
  * 将 `measurement_object`、`aggregation_level`、`denominator`、`unit_semantics` 等定为概念同一性维度。
  * 若模型标记了 `CONFLICT`（已知概念冲突），Python 校验直接拦截，强制标为 `REJECTED`；`REVIEW` 仅用于承接“同一测量概念但口径/参数未定”的情况。
* **强制逐项复核 (`mapping_models.py` / `mapping_prompts.py`)**：
  * `critic_targets()` 显式将 `PENDING_REVIEW` 候选纳入独立复核目标，杜绝漏审。
  * 复核结论 `CHALLENGE` 明确触发排除，`UNRESOLVED` 保留待确认。

### 3. 快速筛选与无名公式识别 (`screening.py`)
* **支持无名称数学公式**：如果合同未出现指标字眼，但写明了等价公式（如 `Cov(Rp, Rb | Rb < 0) / Var(Rp, Rb | Rb < 0)`），快速模式也能精准识别为下行Beta。
* **支持非数值管理动作**：放开“没有数值门槛就直接排除”的死板限制；对于明确以某概念为调仓依据的操作条款（如固收中的“Duration adjustment”），成功关联并识别出久期指标。

---

## 三、双模式速度与实测数据

系统底层提供两种运行模式，在速度与产出上有明确分工：

| 模式 | 典型耗时 | 模型调用轮次 | 准确度与产出 | 适用场景 |
|---|---|---|---|---|
| **快速筛选模式 (Screening)** | **~ 28 ~ 31 秒** ⚡️ | 1 ~ 2 轮并发 | **高**：彻底排除 10 个假正例，产出 6 列表格、匹配分、条款 Quote 与毫秒级本地参考组合 | **日常高频看盘、投资经理快速初筛**（推荐主力使用） |
| **Copilot 深度模式 (Detailed)** | **~ 230 ~ 260 秒**<br>（约 3.8 ~ 4.3 分钟） | 8 ~ 9 轮链式调用<br>(约 22~24 万 Tokens) | **完整**：包含合同要求提取、覆盖审计、全库映射、独立 Critic，额外输出**禁投规则清单、库缺口、未覆盖条件** | **正式风控合规审查、合同归档定稿** |

> **耗时说明**：深度模式在本次优化后，因消除了 10 个模糊候选的反复争辩，单次耗时从以往的 307~358 秒缩短至 229~264 秒，提速约 15%~25%；若后续追求更快的深度模式，主要优化空间在简化全条款切片审计和提升模型并发。

---

## 四、评测工具与准确率实测结果

为避免“凭感觉改 Prompt”，工程内沉淀了一套严谨的可追溯评测工具：

### 1. 《权益sample.pdf》34 项逐指标基线对比
* 评测工具：`scripts/evaluate_mandate_recognition.py`
* 初标基线：`tests/fixtures/mandate_recognition_equity.json`（5 项同概念可关联、28 项不应关联、1 项区域分布待业务裁定）

| 评测维度 | 优化前历史报告 (`run-cffb43da…`) | 本次优化后真实运行 (`run-608f38aa…` / `run-1d2fbcc1…`) |
|---|---|---|
| **入选指标数** | 15 个（充斥大量无关工具） | **4 ~ 5 个**（精准聚焦） |
| **假正例 (FP, 误选)** | **10 个** | **0 个**（下行Beta、Alpha、信息比率、行业偏离度等全部清除） |
| **合并 Precision** | 28.57% | **100%** |
| **合并 Recall** | 80.00% | **100% / 80.00%** |
| **合并 F1** | 42.11% | **100% / 88.89%** |

### 2. 13 组真实模型概念对照测试套件
* 测试脚本：`scripts/check_mandate_recognition_contrasts.py`
* 用例配置：`tests/fixtures/mandate_recognition_contrasts.json`
* 覆盖场景：同义改写换行、无指标名公式、证券换成发行人、绝对行业 vs 相对偏离、第三方基金底层条件隔离、无数值门槛管理动作等。
* 实测结果：真实调用 Gemini 3.8 Flash，**13 组用例 100% 通过**（耗时 224 秒）。

---

## 五、服务启动与运维自检

### 1. 本地启动带 OMP 模型代理的后端 (端口 8002)
```bash
cd /Volumes/onePiece/公司前端项目/AI项目/vmchat-hermes-replacement-python

# 启动本地服务（默认绑定 127.0.0.1:8002）
env OMP_TEST_MODEL=google-antigravity/gemini-3.8-flash \
  uv run python scripts/mandate_risk_v2_omp_server.py
```

### 2. 健康检查与接口探测
```bash
curl -sS http://127.0.0.1:8002/health | jq .
```
预期输出 `status: ok`，且 `workflows` 包含 `mandate-risk-copilot` 与 `mandate-risk-analysis-v2`。

### 3. 一键运行自动化回归测试 (202 项全过)
```bash
uv run pytest -q tests/test_mandate_risk_v2_*.py \
  tests/test_mandate_risk_copilot.py \
  tests/test_mandate_recognition_evaluation.py \
  tests/test_main_and_config.py
```

### 4. 真实结果评测命令示例
```bash
# 评估某次 run 结果的准确率、查准率与召回率
uv run python scripts/evaluate_mandate_recognition.py \
  --result /path/to/run_result.json \
  --gold tests/fixtures/mandate_recognition_equity.json \
  --pdf '/Users/liuruibing/Downloads/sample(1)/权益sample.pdf'
```

---

## 六、未来建议与潜在优化方向

1. **若后续要对“深度模式”进一步提速**：
   - 瓶颈在 `requirements` 提取和覆盖审计（~105秒）以及 `mapping` 分批（~125秒）。可通过放宽批处理大小（如单批 16 个指标）并提升模型调用并发数（`concurrency` 设为 3~4）来压至 1.5 分钟以内。
2. **多文档泛化验证**：
   - 目前已在《权益sample.pdf》和《固收sample.pdf》上完成了首轮闭环，后续引入更多新合同样本时，建议直接复用 `scripts/evaluate_mandate_recognition.py` 扩充 gold 规则，保持数据驱动迭代。
3. **前端快速/深度切换体验**：
   - 前端可根据业务角色提供轻量开关（默认快速筛选模式 30 秒出表；需要合规级条款归档时手动勾选深度模式）。

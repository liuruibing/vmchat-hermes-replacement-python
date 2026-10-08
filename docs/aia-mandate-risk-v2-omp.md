# 友邦 V2 通过 OMP 调用真实模型

核对日期：2026-10-07。

## 当前连接方式

```text
友邦独立页面 http://127.0.0.1:19529/
    → /mandate-api 开发代理
    → Python OMP 服务 http://127.0.0.1:8002/
    → V2 screening：解析 PDF、读取指标库、构造模型输入
    → 本机已登录的 omp CLI
    → google-antigravity / gemini-3.8-flash 真实模型
    → Python 校验、聚合 → SSE → 前端结果表格
```

当前页面的请求已经切到 8002 的真实 OMP 服务。原来的 7310 服务保留，它使用的模型账户曾返回 402，当前页面不再通过该端口调用模型。

适配入口为 `scripts/mandate_risk_v2_omp_server.py`。虽然原有类名为 OmpTestProvider，它实际创建 omp 子进程并调用真实模型，没有固定报告或模拟结果回退。模型和登录账户来自本机 OMP 的配置；本次明确指定了上述模型。

适配器把 V2 的 system_prompt 与 user_prompt 写入临时文件，使用 `omp -p --mode json` 调用，收集最终 assistant 文本及真实 usage。调用关闭 OMP 的编程工具、扩展、规则和会话保存，OMP 在这里负责模型调用；业务逻辑与 JSON 校验仍由 Python 完成。

## 本次真实运行证据

| 项目 | 本次结果 |
| --- | --- |
| 输入 | 用户刚才上传的权益sample.pdf，重新从页面上传 |
| 页数 | 7 |
| 文档 ID | doc_f28429efeed94c39ac43022d20738f78 |
| Run ID | run-405579f7-33f2-459c-abb5-e13b9bf4a1d2 |
| 模式 | screening |
| Provider | OMP → google-antigravity |
| 实际模型 | gemini-3.8-flash |
| 终态 | run.completed |
| 指标库处理 | 34 个库行全部各有一次最终处置 |
| 相关指标 | 21 个，页面实际显示 21 行 |
| 原文证据 | 49 条引用，均校验为解析文本中的对应 source span |
| 模型调用 | 1 次，结构校验重试 0 次 |
| Provider 报告 token | 12,413，usage.complete=true |
| 分组合并 | key 4 行、core 6 行、Indicator 11 行 |

指标名称及算法均与真实只读库行逐项比对；重新上传文件的 SHA-256 与刚才上传的 PDF 一致。页面中的“跟踪误差”抽屉实际展示了第 4、5、6 页的三条原文依据。

上述检查验证身份、来源和完整调用链，不代表所有指标的业务适用性已人工验收。当前是快速筛选，没有执行 detailed 的 Requirement IR 覆盖审计和 Critic。

本地证据目录：`.runtime/v2-validation/2026-10-07-omp/`。

- `verified-summary.json`：本次身份、数量、usage 和检查结果。
- `equity-events.sse`：真实终态任务的 SSE 回放。
- `equity-completed.json`：完整完成事件、Markdown 与结构化结果。
- `equity-report.md`：本次真实分析报告。
- `equity-parsed.json`：对应 PDF 解析文本与页码。
- `8dd0b315651e4384bf749b1d73a49e66.json`：真实 OMP 最终模型响应与 usage。

该目录是本地运行证据，不作为模拟回包来源。

## 自己重新启动

在 Python 仓库根目录执行：

```sh
OMP_EVIDENCE_DIR=.runtime/omp-runtime \
OMP_TEST_MODEL=google-antigravity/gemini-3.8-flash \
MANDATE_RISK_V2_MODE=screening \
.venv/bin/python scripts/mandate_risk_v2_omp_server.py
```

默认监听 localhost:8002。`OMP_SERVER_PORT` 可覆盖端口，`OMP_TEST_THINKING` 可覆盖 thinking 档位，默认 low。不设置 OMP_TEST_MODEL 时由 OMP 默认模型配置决定；模型能否调用取决于当前 OMP 登录与服务额度。

该入口用 Provider 注入创建独立 Runtime，当前文档记录和运行状态使用隔离的内存存储，解析文件在临时目录；重启后应重新上传 PDF，不要复用上一进程的 document_id。OMP_EVIDENCE_DIR 保存模型调用记录，不意味着框架自动把全部文档/任务持久化在该目录；本次报告及验证摘要是联调时另外保存的。

在友邦前端仓库根目录执行：

```sh
nvm use 14.19.0
MANDATE_API_URL=http://127.0.0.1:8002 BABEL_ENV=development \
node node_modules/webpack-dev-server/bin/webpack-dev-server.js \
  --config src/views/mandateRiskV2/preview/webpack.config.js
```

然后打开 `http://127.0.0.1:19529/`，点击“新分析”或“更换 PDF”，上传自己的 PDF。页面接口地址保持 `/mandate-api`，开发代理会转发到真实 OMP 服务。

## 判断连接正确

`GET http://127.0.0.1:19529/mandate-api/health` 的 runtime 应返回：

```json
{
  "provider": "omp",
  "model": "google-antigravity/gemini-3.8-flash",
  "modelSelectable": false,
  "v2Mode": "screening"
}
```

上传响应为 201，创建 run 为 200，最终必须收到 run.completed。只看服务已连接或 SSE HTTP 200 不足以证明分析成功。模型调用日志可查看 `/tmp/aia-v2-omp-server.log`。

本次适配器测试为 `5 passed`；真实 PDF 的运行证据见上表。没有重新执行全量后端回归。

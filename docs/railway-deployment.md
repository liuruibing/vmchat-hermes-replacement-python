# Railway 远程开发部署

本项目的 FastAPI 服务可以部署到 Railway，并由本地 Vue 前端直接访问 Railway 提供的 HTTPS 地址。

GitHub Actions 负责测试，不负责常驻运行 FastAPI。常驻服务由 Railway 托管。

## 已提供的配置

仓库根目录的 railway.json 使用 Railpack 构建，并启动：

    uvicorn app.main:app --host 0.0.0.0 --port $PORT

健康检查：

    GET /health

GitHub Actions：

    .github/workflows/python-ci.yml

会在 push、pull request 和手工触发时运行 Python 3.12、依赖同步、compileall 和 pytest。

## Railway 环境变量

至少需要配置真实模型连接：

    LLM_PROVIDER=langchain
    LLM_BASE_URL=<OpenAI-compatible API base URL>
    LLM_API_KEY=<secret>
    LLM_MODEL=deepseek-v4-flash
    LLM_OUTPUT_MODE=structured

本地前端默认开发地址已经被后端 CORS 允许：

    http://localhost:9528
    http://127.0.0.1:9528

如端口变化，在 Railway 增加：

    CORS_ORIGINS=http://localhost:9528,http://127.0.0.1:9528

建议为公开服务设置：

    SERVICE_API_KEY=<random-secret>

前端会把该值作为 Bearer token 发送。不要把真实 SERVICE_API_KEY 或 LLM_API_KEY 提交到 GitHub。

语义 Profile 相关可选变量：

    VMCHAT_SQL_KNOWLEDGE_PATH=delivery/02_vm_modules_sql_statements.md
    MAX_SKILL_RESOURCE_READS=24

## 本地前端指向远程服务

前端的 Hermes Base URL 存储在 localStorage：

    fof-research-hermes-base-url

API Key 存储在：

    fof-research-hermes-api-key

浏览器控制台可以直接设置：

    localStorage.setItem('fof-research-hermes-base-url', 'https://<your-domain>.up.railway.app')
    localStorage.setItem('fof-research-hermes-api-key', '<SERVICE_API_KEY>')
    location.reload()

如果 SERVICE_API_KEY 留空，第二行可以不设置，但公开服务不建议无鉴权运行。

## 验证

部署完成后先访问：

    https://<your-domain>.up.railway.app/health

预期至少返回：

    {
      "status": "ok",
      "skillLoaded": true,
      "catalogLoaded": true,
      "schemaLoaded": true,
      "modelConfigured": true
    }

然后再让本地前端调用 /v1/runs。

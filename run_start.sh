#!/usr/bin/env bash
# 本脚本由容器内的 restart.sh 调用：
#   第一个参数是 Python 命令（通常为 python3），第二个参数是服务端口（这里为 7310）。
# 它只负责启动 vmchat 服务；Jenkins 的打包、上传和目录切换在 Jenkins 配置中完成。
set -euo pipefail

# 未提供第一个参数时，默认使用系统的 python3。
python_bin="${1:-python3}"
# 第二个参数必须存在；缺失时立即报错，避免服务意外跑在错误端口。
port="${2:?missing service port}"

# 无论从哪个目录调用脚本，都切换到本脚本所在的项目目录。
cd "$(dirname "$0")"

# uv 是 Python 依赖管理工具。容器首次部署时若没有它，则通过当前 Python 安装到当前用户目录。
if ! command -v uv >/dev/null 2>&1; then
  "$python_bin" -m pip install --user uv
# 让本次脚本能找到刚安装的 uv（默认安装目录为 ~/.local/bin）。
  export PATH="$HOME/.local/bin:$PATH"
fi

# 根据 uv.lock 精确创建/同步本项目自己的 .venv；--no-dev 不安装 pytest 等开发依赖。
# 这样不会污染容器中其他项目的 Python 环境。
uv sync --locked --no-dev
# 用本项目虚拟环境启动 FastAPI/Uvicorn。exec 让该进程直接成为脚本进程，便于重启脚本管理。
exec .venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port "$port"

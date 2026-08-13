#!/usr/bin/env bash
set -euo pipefail

python_bin="${1:-python3}"
port="${2:?missing service port}"

cd "$(dirname "$0")"

if ! command -v uv >/dev/null 2>&1; then
  "$python_bin" -m pip install --user uv
  export PATH="$HOME/.local/bin:$PATH"
fi

uv sync --locked --no-dev
exec .venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port "$port"

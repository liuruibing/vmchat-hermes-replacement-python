#!/usr/bin/env bash
set -euo pipefail

VM_REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VM_E2E_OUTPUT_DIR="$VM_REPO_DIR/output/playwright/vm-chat-e2e"
VM_E2E_SERVER_LOG="$VM_E2E_OUTPUT_DIR/dev-server.log"
VM_E2E_SESSION="vm-chat-e2e-$$"
VM_PWCLI="${VM_PLAYWRIGHT_CLI:-}"
VM_CODEX_PWCLI="${CODEX_HOME:-${HOME}/.codex}/skills/playwright/scripts/playwright_cli.sh"
VM_APP_NODE_BIN_DIR="${VM_APP_NODE_BIN_DIR:-$(dirname "$(command -v node)")}"
VM_PLAYWRIGHT_NODE_BIN_DIR="${VM_PLAYWRIGHT_NODE_BIN_DIR:-$(dirname "$(command -v node)")}"
VM_E2E_LIVE="${VM_CHAT_BROWSER_LIVE:-0}"

if [[ -z "$VM_PWCLI" && -x "$VM_CODEX_PWCLI" ]]; then
  VM_PWCLI="$VM_CODEX_PWCLI"
fi
if [[ -z "$VM_PWCLI" ]] && ! command -v playwright-cli >/dev/null 2>&1 && ! command -v npx >/dev/null 2>&1; then
  printf '未找到 playwright-cli 或 npx，无法运行浏览器回归测试\n' >&2
  exit 1
fi

if [[ "$VM_E2E_LIVE" == "1" && -z "${VM_CHAT_API_TOKEN:-}" ]]; then
  printf 'VM_CHAT_BROWSER_LIVE=1 时必须提供 VM_CHAT_API_TOKEN\n' >&2
  exit 1
fi
if [[ "$VM_E2E_LIVE" == "1" ]]; then
  VM_E2E_LIVE_LITERAL=true
else
  VM_E2E_LIVE_LITERAL=false
fi

run_pwcli() {
  if [[ -n "$VM_PWCLI" ]]; then
    PATH="$VM_PLAYWRIGHT_NODE_BIN_DIR:$PATH" "$VM_PWCLI" "$@"
  elif command -v playwright-cli >/dev/null 2>&1; then
    PATH="$VM_PLAYWRIGHT_NODE_BIN_DIR:$PATH" playwright-cli "$@"
  else
    PATH="$VM_PLAYWRIGHT_NODE_BIN_DIR:$PATH" npx --package @playwright/cli playwright-cli "$@"
  fi
}

mkdir -p "$VM_E2E_OUTPUT_DIR"
cd "$VM_REPO_DIR"

cleanup() {
  run_pwcli -s="$VM_E2E_SESSION" close >/dev/null 2>&1 || true
  if [[ -n "${VM_E2E_SERVER_PID:-}" ]]; then
    kill "$VM_E2E_SERVER_PID" >/dev/null 2>&1 || true
    wait "$VM_E2E_SERVER_PID" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

PATH="$VM_APP_NODE_BIN_DIR:$PATH" HOST=127.0.0.1 PORT=19528 npm run dev >"$VM_E2E_SERVER_LOG" 2>&1 &
VM_E2E_SERVER_PID=$!

VM_E2E_READY=false
for _ in $(seq 1 90); do
  if curl --silent --fail --max-time 5 http://127.0.0.1:19528/app.js >/dev/null 2>&1; then
    VM_E2E_READY=true
    break
  fi
  if ! kill -0 "$VM_E2E_SERVER_PID" >/dev/null 2>&1; then
    tail -80 "$VM_E2E_SERVER_LOG"
    exit 1
  fi
  sleep 1
done

if [[ "$VM_E2E_READY" != true ]]; then
  tail -80 "$VM_E2E_SERVER_LOG"
  exit 1
fi

run_pwcli -s="$VM_E2E_SESSION" open about:blank >/dev/null
VM_E2E_CODE="$(<"$VM_REPO_DIR/tests/vm-chat-browser-e2e.playwright.js")"
VM_E2E_TOKEN_BASE64="$(printf '%s' "${VM_CHAT_API_TOKEN:-}" | base64 | tr -d '\n')"
VM_E2E_CODE="${VM_E2E_CODE/__VM_CHAT_BROWSER_LIVE__/$VM_E2E_LIVE_LITERAL}"
VM_E2E_CODE="${VM_E2E_CODE/__VM_CHAT_API_TOKEN_BASE64__/$VM_E2E_TOKEN_BASE64}"
VM_E2E_RESULT="$(run_pwcli --raw -s="$VM_E2E_SESSION" run-code "$VM_E2E_CODE")"
printf '%s\n' "$VM_E2E_RESULT"
if [[ "$VM_E2E_RESULT" == *"### Error"* ]]; then
  exit 1
fi

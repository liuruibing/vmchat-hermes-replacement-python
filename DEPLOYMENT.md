# Jenkins 部署脚本说明

本项目在 Jenkins 中有两个 Shell 脚本，依次完成“构建包”和“服务器部署”。它们不会在本地开发机运行。

## 1. Jenkins 构建脚本

```bash
set -eu
rm -rf dist
mkdir -p dist/backend
cp -R app resources dist/backend/
cp pyproject.toml uv.lock run_start.sh dist/backend/
tar -C dist -czf dist/vmchat-hermes-replacement-python.tar.gz backend
```

- `set -e`：任意命令失败时立即结束构建；避免生成半成品包。
- `set -u`：使用未定义变量时立即报错，避免脚本因为拼写错误而静默运行。
- `rm -rf dist`：删除上一次构建产生的临时目录；只影响 Jenkins 工作空间里的 `dist`。
- `mkdir -p dist/backend`：创建发布包的顶层目录 `backend`。远程脚本会识别这个目录名。
- `cp -R app resources ...`：复制 FastAPI 源代码与 DSL/Skill 资源；缺少任一目录服务都不能正确工作。
- `cp pyproject.toml uv.lock run_start.sh ...`：复制依赖声明、精确依赖版本和启动脚本。
- 没有复制 `.env`：其中可能包含密钥，应由服务器安全地配置。
- 没有复制 `.venv`：本机虚拟环境是 macOS 版本，不能带到 Linux 容器。
- `tar -C dist -czf ... backend`：进入 `dist` 后把 `backend` 压缩成 tar.gz 包，`-c` 为创建、`-z` 为 gzip 压缩、`-f` 后面跟输出文件名。

## 2. 远程部署脚本

```bash
set -eu
cd /home/datadriver/server/docker/_running/team-jinan-python/upload/wars

archive=vmchat-hermes-replacement-python.tar.gz
release_dir=7310.new
previous_dir=7310.previous

rm -rf "$release_dir"
mkdir -p "$release_dir"
mv "$archive" "$release_dir/$archive"
tar -xzf "$release_dir/$archive" -C "$release_dir"
test -f "$release_dir/backend/run_start.sh"

rm -rf "$previous_dir"
if [ -d 7310 ]; then
  mv 7310 "$previous_dir"
fi
mv "$release_dir/backend" 7310
rm -rf "$release_dir" "$previous_dir"

sudo docker exec -itd team-jinan-python nohup sh /datadriver/upload/restart.sh 7310 vmchat
```

- `cd .../wars`：进入 Docker 宿主机与容器共享的发布目录。
- `archive`、`release_dir`、`previous_dir`：分别是上传包、解压临时目录和旧版本临时备份目录。
- 前五条文件命令：先把包移动到 `7310.new`，解压后确认 `run_start.sh` 存在。此阶段失败不会动正在运行的 `7310` 服务目录。
- `if [ -d 7310 ]`：只有旧服务目录存在才把它临时改名；第一次部署时会直接跳过。
- `mv .../backend 7310`：将已校验的新版本切换为端口对应目录。
- 删除临时目录与旧备份后，`docker exec` 进入 `team-jinan-python` 容器，调用统一重启脚本。
- `7310` 是 vmchat 服务端口，`vmchat` 是传给重启脚本的业务名称。

## 3. 容器内 `run_start.sh`

该脚本会切换到项目目录、确保存在 `uv`，并使用稳定的 Linux 虚拟环境目录
`/datadriver/upload/venvs/vmchat`。这个目录不在 Jenkins 每次替换的 `wars/7310` 中，
因此不会因为发版丢失依赖。

脚本会记录当前 `uv.lock` 的 SHA-256 指纹：

- 首次部署没有稳定虚拟环境时，才运行 `uv sync --locked --no-dev`；
- `uv.lock` 未改变时，直接启动，完全不访问公网包源；
- 只有锁文件改变时，才重新同步依赖。

最后使用：

```bash
/datadriver/upload/venvs/vmchat/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 7310
```

启动 FastAPI 服务。每个项目的依赖隔离在自己的 `.venv` 中，不会影响容器里已有的其他 Python 服务。

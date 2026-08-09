---
name: b200-pod
description: 在 B200 这台 ASI GPU 机器上远程执行命令、查看 GPU/日志/Pod 状态、诊断异常和传输小文件。Use when 用户提到 "B200"、指定 Pod ds-686eaedc-1.ds-686eaedc-1-0d3b27b0-a-eb17，或要求在这台机器上跑命令。统一使用 asicli console，计算容器固定为 worker0。
---

# B200 Pod

**B200** 是这台 ASI 百炼 GPU Pod 的用户别名。所有远程操作使用 `asicli console`。

## 固定标识

| 别名 | Pod 名 | 计算容器 |
| --- | --- | --- |
| B200 | `ds-686eaedc-1.ds-686eaedc-1-0d3b27b0-a-eb17` | `worker0` |

> Pod 名会随机器回收或更换而改变。更换机器后更新本表和 `POD`。本记录验证于 2026-08-05。
>
> 实机报告为 **8× NVIDIA L20C**，每卡 183359 MiB、Compute Capability 10.0。`B200` 只是本机别名，不要据此假定 GPU 型号。

每个会话先设置：

```bash
source ~/.cli-hub/env 2>/dev/null || export PATH="$HOME/.local/bin:$PATH"
POD=ds-686eaedc-1.ds-686eaedc-1-0d3b27b0-a-eb17
```

必须显式传 `--container worker0`；默认容器不是计算容器。

## 前置检查

```bash
which asicli || curl -sSL https://cli-hub.alibaba-inc.com/asicli/install.sh | sh
asicli auth status
# Token 过期时：
asicli auth login
```

禁止输出、记录或把 `ASI_CLI_PRIVATE_TOKEN` 拼进命令。

## 常用操作

### 执行命令

```bash
asicli console exec -p "$POD" --container worker0 -- nvidia-smi
asicli console exec -p "$POD" --container worker0 -- ps aux
asicli console exec -p "$POD" --container worker0 -- sh -c 'cd /path && ls -la'
asicli console exec -p "$POD" --container worker0 -- tail -100 /path/to/app.log
```

- 多条命令用简单的 `sh -c '...'`；复杂流程拆成多次调用。
- 单次请求可能超时，不要用超过约 45 秒的 `sleep`；长任务应后台启动后分次轮询。
- stdout 约有 1 MiB 上限；用 `head`、`tail`、`grep` 收窄输出。
- 后台服务可使用：`setsid nohup <cmd> >log 2>&1 </dev/null &`。
- `kill -9`、`pkill` 等可能被命令校验器拒绝；确需停止自己的进程时，优先对明确 PID 使用普通 `kill <PID>`。

### 日志与状态

```bash
asicli console log -p "$POD" --container worker0 --lines 100
asicli console filelog -n "$POD" --container worker0 --path /path/to/app.log --lines 200
asicli console podinfo -p "$POD"
asicli console podinfo -p "$POD" -o json
asicli console pod-diagnose -p "$POD"
asicli console pod-lifecycle -p "$POD"
```

`filelog` 中 Pod 名用 `-n`，`-p` 是文件路径的缩写。

`tracker-log` 需要集群名；先从 `podinfo -o json` 获取，再执行：

```bash
asicli console tracker-log -c <cluster> -p "$POD"
```

## 小文件传输

`asicli` 没有原生 `scp`。临时小文件可经 base64 传输；原文件控制在约 768 KiB 以下，避免 base64 后超过 stdout 上限。

```bash
# Pod -> 本地
asicli console exec -p "$POD" --container worker0 -- sh -c 'base64 /remote/file' \
  | base64 -d > ./local-file

# 本地 -> Pod；写文件前需得到用户确认
base64 ./local-file | asicli console exec -p "$POD" --container worker0 -- \
  sh -c 'base64 -d > /remote/file'
```

传输后用 `wc -c` 和 `sha256sum`/`shasum -a 256` 校验。大文件优先使用用户指定的 Git 或 OSS 通道；没有已验证的 B200 同步仓库时不要擅自假设路径。

## 安全规则

- 默认只执行只读、诊断类操作。
- 修改或删除 Pod 内文件前必须获得用户确认。
- 不执行破坏性命令，不停止不属于用户的进程。
- 跑任务前先用 `nvidia-smi` 查看占用；不得干扰其他人的 GPU 进程。
- 本 skill 只操作已运行 Pod；提交、删除或改部署使用通用 `asi-cli` skill。
- 若用户说“B200”，默认指本 skill 的固定 Pod；若用户同时给出不同 Pod 名，先确认是否要更新映射，不能静默切换。

## 常见问题

| 现象 | 处理 |
| --- | --- |
| `container main is not valid for pod` | 补 `--container worker0` |
| `Token expired` | 执行 `asicli auth login` |
| 输出在约 1 MiB 处截断 | 收窄输出或分块 |
| Pod 名不唯一 | 从 `podinfo` 获取 cluster/namespace 后补 `-c`、`-N` |
| exec 无输出或超时 | 先确认 Pod 为 Running，再缩短或拆分命令 |

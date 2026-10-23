#!/usr/bin/env bash

# 放在各个项目文件夹同级的 scripts 目录中，执行 bash git_pull_all.sh [并发数]。
# 无论从哪里调用，都先切换到脚本目录，再遍历其父目录中的直接子目录（包括隐藏目录）。
# 兼容 macOS 自带的 Bash 3.2。
shopt -s nullglob dotglob

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)" || exit 1
cd -- "$script_dir" || exit 1
base_dir="$(cd -- "$script_dir/.." && pwd)" || exit 1
concurrency="${1:-6}"
if [[ $# -gt 1 || ! "$concurrency" =~ ^[1-9][0-9]{0,3}$ ]]; then
    printf '用法：bash git_pull_all.sh [并发数，1–9999，默认 6]\n' >&2
    exit 1
fi
success=0
failed=0
skipped=0

if ! command -v git >/dev/null 2>&1; then
    printf '错误：未找到 git，请先安装 Git。\n' >&2
    exit 1
fi

log_dir="$(mktemp -d "${TMPDIR:-/tmp}/git-pull-all.XXXXXX")" || exit 1
trap 'rm -rf -- "$log_dir"' EXIT
active=()
pids=()
names=()
job_id=0

# 由主进程统一显示已完成任务的日志，避免并发输出交错。
collect_finished() {
    local id
    local remaining=()
    for id in "${active[@]}"; do
        if kill -0 "${pids[$id]}" 2>/dev/null; then
            remaining+=("$id")
            continue
        fi
        printf '\n========== %s ==========\n' "${names[$id]}"
        if wait "${pids[$id]}"; then
            cat "$log_dir/$id.log"
            printf '[成功] %s\n' "${names[$id]}"
            success=$((success + 1))
        else
            cat "$log_dir/$id.log"
            printf '[失败] %s：请检查上方 Git 提示\n' "${names[$id]}" >&2
            failed=$((failed + 1))
        fi
    done
    active=("${remaining[@]}")
}

printf '并发数：%s；扫描目录：%s\n' "$concurrency" "$base_dir"
for dir in "$base_dir"/*; do
    [[ -d "$dir" ]] || continue
    name="${dir##*/}"

    # .git 可以是目录，也可以是 worktree 使用的文件。
    if [[ ! -d "$dir/.git" && ! -f "$dir/.git" ]]; then
        printf '\n[跳过] %s：不是 Git 项目根目录\n' "$name"
        skipped=$((skipped + 1))
        continue
    fi

    while (( ${#active[@]} >= concurrency )); do
        collect_finished
        (( ${#active[@]} >= concurrency )) && sleep 0.2
    done

    printf '[开始] %s\n' "$name"
    # 并行任务不能共享交互输入；认证请预先通过凭据管理器或 SSH 配好。
    GIT_TERMINAL_PROMPT=0 git -C "$dir" pull </dev/null >"$log_dir/$job_id.log" 2>&1 &
    pids[$job_id]=$!
    names[$job_id]="$name"
    active+=("$job_id")
    job_id=$((job_id + 1))
done

while (( ${#active[@]} > 0 )); do
    collect_finished
    (( ${#active[@]} > 0 )) && sleep 0.2
done

printf '\n完成：成功 %d，失败 %d，跳过 %d。\n' "$success" "$failed" "$skipped"
[[ "$failed" -eq 0 ]]








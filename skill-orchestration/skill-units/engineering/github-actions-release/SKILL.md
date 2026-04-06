---
name: github-actions-release
description: GitHub Actions Release 工作流设计、权限配置与失败诊断能力单元。当涉及创建 Release job、遇到 403 权限错误、artifact 路径配置、用 MCP/curl 监控 Actions 状态、tag 触发发布流程时触发。关键词：GitHub Actions、Release、contents write、artifact、tag、发布、403、权限、Smithery、MCP、监控、CI 失败。
metadata:
  type: procedural
  category: engineering
  scope: generic
  role: skill-unit
---

# GitHub Actions Release

> 这个 skill-unit 处理的是"Release 工作流如何正确配置，失败时如何诊断和修复"的问题。核心价值：避免重复踩权限坑，提供可复用的诊断路径和监控命令模板。

## 负责与不负责

**负责：**
- Release job 权限配置规范
- 常见失败模式识别与修复
- Actions 状态诊断三段式
- 监控命令模板（curl / Smithery MCP）
- tag 触发发布的标准流程

**不负责：**
- 构建工具选型（PyInstaller、Docker 等）
- 代码打包逻辑
- 仓库结构设计

## 核心配置规范

### Release job 必须显式声明权限

```yaml
release:
  needs: build
  runs-on: ubuntu-latest
  if: startsWith(github.ref, 'refs/tags/')
  permissions:
    contents: write   # ← 缺少此项必然 403
```

`GITHUB_TOKEN` 默认权限为 read-only。`softprops/action-gh-release` 等 Release action 需要写权限，**不显式声明则 Create Release 步骤必然以 403 失败**，且错误信息不够直观，容易被误判为 token 问题。

### artifact 路径须与 upload 名称对齐

```yaml
# upload 阶段
- uses: actions/upload-artifact@v4
  with:
    name: MyApp-${{ matrix.name }}        # artifact 名
    path: dist/MyApp${{ matrix.ext }}     # 实际文件路径

# release 阶段下载后路径为：
# artifacts/MyApp-windows/MyApp.exe
# artifacts/MyApp-macos/MyApp
# artifacts/MyApp-linux/MyApp
```

upload 的 `name` 决定下载后的子目录名，release 的 `files` 路径必须与之完全对应。

## 失败诊断三段式

遇到 Actions 运行失败时，按以下顺序定位：

### Step 1：获取最新运行摘要

```bash
curl -s -H "Authorization: token $GH_TOKEN" \
  "https://api.github.com/repos/OWNER/REPO/actions/runs?per_page=5" | \
  python3 -c "
import json, sys
for r in json.load(sys.stdin)['workflow_runs']:
    print(r['id'], r['head_branch'], r['status'], r['conclusion'])
"
```

### Step 2：定位失败 job

```bash
curl -s -H "Authorization: token $GH_TOKEN" \
  "https://api.github.com/repos/OWNER/REPO/actions/runs/RUN_ID/jobs" | \
  python3 -c "
import json, sys
for j in json.load(sys.stdin)['jobs']:
    e = '✅' if j['conclusion']=='success' else '❌' if j['conclusion']=='failure' else '🔄'
    print(e, j['name'], '|', j['status'], '|', j.get('conclusion','...'))
"
```

### Step 3：查看失败 job 的 steps

定位到失败 job 后，检查其 `steps` 列表中哪一步 `conclusion == failure`，结合 step name 判断根因。

## 状态轮询监控模板

适用于推送 tag 后等待构建完成的场景：

```bash
RUN_ID="<从 Step 1 获取>"
for i in $(seq 1 20); do
  echo "=== $(date '+%H:%M:%S') ==="
  curl -s -H "Authorization: token $GH_TOKEN" \
    "https://api.github.com/repos/OWNER/REPO/actions/runs/$RUN_ID/jobs" | \
  python3 -c "
import json, sys
for j in json.load(sys.stdin)['jobs']:
    e = '✅' if j['conclusion']=='success' else '❌' if j['conclusion']=='failure' else '🔄' if j['status']=='in_progress' else '⏳'
    print(f'  {e} {j[\"name\"]} | {j[\"status\"]} | {j.get(\"conclusion\",\"...\")}')
"
  STATUS=$(curl -s -H "Authorization: token $GH_TOKEN" \
    "https://api.github.com/repos/OWNER/REPO/actions/runs/$RUN_ID" | \
    python3 -c "import json,sys; d=json.load(sys.stdin); print(d['status']+'|'+str(d['conclusion']))")
  echo "  整体: $STATUS"
  [[ "$STATUS" == completed* ]] && break
  sleep 30
done
```

## Smithery MCP 工具速查

通过 Smithery 连接 GitHub MCP 后，可用以下工具替代 curl：

```bash
# 列出工作流
smithery tool call github actions_list \
  '{"method": "list_workflows", "owner": "OWNER", "repo": "REPO"}'

# 列出最近运行
smithery tool call github actions_list \
  '{"method": "list_workflow_runs", "owner": "OWNER", "repo": "REPO", "per_page": 5}'

# 列出某次运行的 jobs
smithery tool call github actions_list \
  '{"method": "list_workflow_jobs", "owner": "OWNER", "repo": "REPO", "resource_id": "RUN_ID"}'

# 获取运行日志下载链接
smithery tool call github actions_get \
  '{"method": "get_workflow_run_logs_url", "owner": "OWNER", "repo": "REPO", "resource_id": "RUN_ID"}'

# 触发 workflow dispatch
smithery tool call github actions_run_trigger \
  '{"method": "run_workflow", "owner": "OWNER", "repo": "REPO", "workflow_id": "build.yml", "ref": "main"}'
```

**注意：** `rerun_workflow_run` 需要仓库写权限，Smithery OAuth 授权范围可能不包含，遇到 403 时改用重新推送 tag 触发。

## 标准发布流程

```bash
# 1. 确认代码已推送到主分支
git push origin main

# 2. 打 tag 并推送（触发 Actions）
git tag vX.Y.Z && git push origin vX.Y.Z

# 3. 等待触发（约 10s）后获取 run_id
sleep 10
curl -s -H "Authorization: token $GH_TOKEN" \
  "https://api.github.com/repos/OWNER/REPO/actions/runs?per_page=1" | \
  python3 -c "import json,sys; r=json.load(sys.stdin)['workflow_runs'][0]; print(r['id'], r['head_branch'], r['status'])"

# 4. 用轮询模板监控直到 completed
# 5. 验证 conclusion == success
```

## 常见失败模式速查

| 现象 | 根因 | 修复 |
|------|------|------|
| Create Release 步骤 403 | 缺少 `contents: write` 权限 | release job 添加 `permissions: contents: write` |
| Download artifact 找不到文件 | release `files` 路径与 upload `name` 不匹配 | 对齐路径：`artifacts/<upload-name>/<filename>` |
| Build 成功但 release job 未触发 | `if: startsWith(github.ref, 'refs/tags/')` 条件未满足 | 确认推送的是 tag 而非 branch |
| rerun 返回 403 | Smithery OAuth 权限不足 | 删除旧 tag，重新推送新 tag 触发 |

## 参考资料

- `references/workflow-template.yml` - 完整的跨平台构建 + Release 工作流模板

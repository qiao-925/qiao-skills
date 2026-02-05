# uv 命令参考

> 来源：[uv 官方文档](https://docs.astral.sh/uv/)

## 安装 uv

```bash
# Linux/macOS（推荐）
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 使用 pip 安装
pip install uv

# 使用 Homebrew (macOS)
brew install uv
```

---

## 虚拟环境管理

### 创建虚拟环境

```bash
# 默认创建 .venv/
uv venv

# 指定目录名
uv venv myenv

# 指定 Python 版本
uv venv --python 3.11
uv venv --python python3.10

# 使用系统 site-packages
uv venv --system-site-packages
```

### 激活虚拟环境

```bash
# Linux/macOS
source .venv/bin/activate

# Windows (cmd)
.venv\Scripts\activate.bat

# Windows (PowerShell)
.venv\Scripts\Activate.ps1
```

---

## 包管理

### 安装包

```bash
# 从 requirements.txt 安装
uv pip install -r requirements.txt

# 安装单个包
uv pip install requests

# 安装多个包
uv pip install requests flask pytest

# 安装特定版本
uv pip install "requests>=2.28,<3.0"

# 开发模式安装当前项目
uv pip install -e .

# 安装带 extras 的包
uv pip install -e ".[dev,test]"
```

### 卸载包

```bash
uv pip uninstall requests
uv pip uninstall requests flask pytest
```

### 查看已安装包

```bash
# 列出所有包
uv pip list

# 以 requirements.txt 格式输出
uv pip freeze

# 查看特定包信息
uv pip show requests
```

---

## 依赖同步

```bash
# 同步到 requirements.txt 指定的状态（添加缺失，移除多余）
uv pip sync requirements.txt

# 同步多个 requirements 文件
uv pip sync requirements.txt dev-requirements.txt
```

---

## 高级选项

### 自定义包源

```bash
# 使用私有 PyPI
uv pip install --index-url https://pypi.example.com/simple/ package

# 额外包源
uv pip install --extra-index-url https://pypi.example.com/simple/ package

# 信任主机（跳过 SSL 验证）
uv pip install --trusted-host pypi.example.com package
```

### 缓存管理

```bash
# 查看缓存目录
uv cache dir

# 清理缓存
uv cache clean
```

### 依赖解析

```bash
# 编译 requirements.in 到 requirements.txt（类似 pip-compile）
uv pip compile requirements.in -o requirements.txt

# 升级所有包
uv pip compile requirements.in -o requirements.txt --upgrade
```

---

## 与传统工具对比

| 功能 | pip/venv | uv | 速度提升 |
|------|----------|-----|---------|
| 创建虚拟环境 | `python -m venv venv` | `uv venv` | ~10x |
| 安装依赖 | `pip install -r requirements.txt` | `uv pip install -r requirements.txt` | 10-100x |
| 依赖解析 | `pip-compile` | `uv pip compile` | ~50x |
| 全局缓存 | 无 | 有 | 重复安装极快 |

---

## 常见问题

### Q: uv 与 pip 完全兼容吗？

A: uv 设计为 pip 的直接替代品，支持大部分 pip 命令和参数。少数边缘情况可能有差异。

### Q: uv 创建的虚拟环境与 venv 有区别吗？

A: 功能上相同，但 uv 创建速度更快。默认目录名为 `.venv/`（venv 默认可能用 `venv/`）。

### Q: 是否需要先激活虚拟环境？

A: uv 可以自动检测当前目录的虚拟环境，但建议显式激活以确保行为一致。

### Q: 如何在 CI/CD 中使用？

A: 在 CI 中使用 uv 可显著减少构建时间：

```yaml
# GitHub Actions 示例
- name: Install uv
  run: curl -LsSf https://astral.sh/uv/install.sh | sh

- name: Install dependencies
  run: |
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt
```

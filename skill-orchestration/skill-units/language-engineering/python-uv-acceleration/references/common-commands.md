# 常用命令

## 安装 uv

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 也可用 pip 安装
pip install uv
```

## 创建虚拟环境

```bash
uv venv
uv venv .venv
uv venv --python 3.11
```

## 激活虚拟环境

```bash
# Linux/macOS
source .venv/bin/activate

# Windows cmd
.venv\\Scripts\\activate.bat

# Windows PowerShell
.venv\\Scripts\\Activate.ps1
```

## 安装与同步依赖

```bash
uv pip install -r requirements.txt
uv pip install requests
uv pip install -e .
uv pip install -e ".[dev,test]"
uv pip sync requirements.txt
```

## 导出与查看

```bash
uv pip freeze
uv pip list
uv pip show requests
```

## 卸载与缓存

```bash
uv pip uninstall requests
uv cache dir
uv cache clean
```

## 私有索引

```bash
uv pip install --index-url https://pypi.example.com/simple/ package
uv pip install --extra-index-url https://pypi.example.com/simple/ package
```

## 命令映射

| 传统命令 | uv 命令 |
|----------|---------|
| `python -m venv .venv` | `uv venv` |
| `pip install -r requirements.txt` | `uv pip install -r requirements.txt` |
| `pip install package` | `uv pip install package` |
| `pip install -e .` | `uv pip install -e .` |
| `pip freeze` | `uv pip freeze` |
| `pip list` | `uv pip list` |
| `pip uninstall package` | `uv pip uninstall package` |

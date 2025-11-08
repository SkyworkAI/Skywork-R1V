# Skywork-R1V Inference

推理脚本和配置说明

## 快速开始

### 1. 安装依赖

```bash
cd /path/to/r1v4
pip install -r requirements.txt
```

### 2. 配置环境变量

在项目根目录（`r1v4/`）创建 `.env` 文件：

```bash
# 复制示例配置文件
cp .env.example .env

# 编辑 .env 文件，填入你的配置
vim .env
```

`.env` 文件内容：

```bash
# API Server Configuration
SERVER_URL=http://your-api-server-url
API_KEY=your-api-key

# Optional: Advanced settings
MAX_TOKENS=8192
TEMPERATURE=0.2
REQUEST_TIMEOUT=300
```

### 3. 运行推理脚本

```bash
cd infer
python request_general.py
```

## 文件说明

- `request_general.py` - 通用推理请求（支持纯文本和多模态）
- `request_plan.py` - 规划任务推理
- `request_deepresearch.py` - 深度研究推理

## 配置说明

### 必需配置

- `SERVER_URL`: API 服务器地址
- `API_KEY`: API 密钥

## 安全说明

⚠️ **重要**: 
- `.env` 文件包含敏感信息，**不要提交到 git**
- 已在 `.gitignore` 中配置排除 `.env` 文件
- 提供 `.env.example` 作为配置模板

## 故障排除

### 错误：Required environment variable 'XXX' is not set

**原因**: 未正确配置环境变量

**解决方案**:
1. 确保在 `r1v4/` 目录下创建了 `.env` 文件
2. 检查 `.env` 文件中是否包含所有必需的配置项
3. 确认配置项格式正确（`KEY=value`，等号两边无空格）

### 错误：ModuleNotFoundError: No module named 'dotenv'

**原因**: 未安装 python-dotenv

**解决方案**:
```bash
pip install python-dotenv
```

或重新安装所有依赖：
```bash
pip install -r requirements.txt
```


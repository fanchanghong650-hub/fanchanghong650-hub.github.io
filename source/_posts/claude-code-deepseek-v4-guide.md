---
title: Claude Code + DeepSeek V4 Pro 终极配置指南
date: 2026-05-29 19:30:00
categories: 工具
tags: [Claude Code, DeepSeek, AI编程, 配置指南, 故障排除]
description: 用 DeepSeek V4 Pro 驱动 Claude Code，低成本享受顶级 AI 编程体验。包含完整配置步骤、8+ 常见报错解决方案、Windows 实战排查案例。
---

> 用 DeepSeek V4 Pro 驱动 Claude Code，低成本享受顶级 AI 编程体验。

---

## 1. 这是什么？

[Claude Code](https://docs.anthropic.com/en/docs/claude-code) 是 Anthropic 推出的 AI 编程 CLI 工具，原生需要调用 Anthropic API。

[DeepSeek](https://api-docs.deepseek.com/) 提供了 **Anthropic 兼容 API 端点**（`https://api.deepseek.com/anthropic`），可以无缝替代 Anthropic 原生 API。

这样一来，你就能以 **DeepSeek 的价格**，享受 **Claude Code 的完整功能**。

### 成本对比

| 提供商 | 模型 | 输入价格 (每百万 token) | 输出价格 (每百万 token) |
|--------|------|------------------------|------------------------|
| Anthropic | Claude Opus 4.5 | $15.00 | $75.00 |
| DeepSeek | V4 Pro | ¥2.00 (~$0.28) | ¥8.00 (~$1.10) |
| DeepSeek | V4 Flash | ¥0.50 (~$0.07) | ¥2.00 (~$0.28) |

**成本降低约 50-100 倍。**

---

## 2. 两种方案：直连 vs 代理

### 方案 A：直连（推荐，最简单）

DeepSeek 官方提供了 Anthropic 兼容端点，Claude Code 可以直接调用，无需任何中间层。

```
Claude Code ──→ https://api.deepseek.com/anthropic
```

**适用场景**：日常编码、代码审查、简单重构

### 方案 B：本地代理

在本地运行一个 Node.js 代理，将 Anthropic 格式翻译为 OpenAI 格式。

```
Claude Code ──→ localhost:8765 (proxy.js) ──→ api.deepseek.com/v1/chat/completions
```

**适用场景**：需要处理兼容性问题（如 system 消息格式、thinking 块）时的兜底方案

### 方案对比

| 维度 | 直连 | 代理 |
|------|------|------|
| 配置复杂度 | ⭐ 简单 | ⭐⭐⭐ 需要额外维护 |
| 稳定性 | 依赖 DeepSeek 官方兼容性 | 自主可控，可随时修 bug |
| 已知坑 | v2.1.156 system role 问题 | 代理脚本可能有硬编码 bug |
| 认证方式 | `ANTHROPIC_AUTH_TOKEN` 直接放 API Key | 代理读 `DEEPSEEK_API_KEY`，Claude Code 侧放占位符 |
| 维护成本 | 零 | 需保持代理进程运行 |

> **本文重点介绍方案 A（直连），这也是大多数人应该使用的。方案 B 详见第 6 节。**

---

## 3. 配置步骤

### 3.1 安装 Claude Code

```bash
# 需要 Node.js 18+
npm install -g @anthropic-ai/claude-code

# 验证安装
claude --version
```

### 3.2 获取 DeepSeek API Key

前往 [DeepSeek API 平台](https://platform.deepseek.com/api_keys) 创建 API Key。

### 3.3 配置 settings.json

编辑 `~/.claude/settings.json`（Windows: `C:\Users\<用户名>\.claude\settings.json`）：

```json
{
  "autoUpdatesChannel": "latest",
  "model": "opus",
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-你的DeepSeek-API-Key",
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-v4-flash[1m]",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1",
    "CLAUDE_CODE_EFFORT_LEVEL": "max",
    "API_TIMEOUT_MS": "600000"
  }
}
```

### 3.4 (可选) Bash 环境变量

如果你在 Git Bash / WSL 等环境下使用，创建 `~/.deepseek-claude/env`：

```bash
export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
export ANTHROPIC_AUTH_TOKEN="sk-你的DeepSeek-API-Key"
export ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash[1m]"
export CLAUDE_CODE_EFFORT_LEVEL="max"
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1"
export API_TIMEOUT_MS="600000"
```

并在 `~/.bashrc` 中引用：

```bash
[ -f "$HOME/.deepseek-claude/env" ] && source "$HOME/.deepseek-claude/env"
```

### 3.5 ⚠️ 不要做的事

以下配置项**不要设置**，否则会导致莫名其妙的问题：

```json
// ❌ 不要设置 CLAUDE_CODE_SUBAGENT_MODEL
// 让 Claude Code 自动根据任务复杂度选择子代理模型
// 设置它会锁定所有子代理用同一个模型，浪费 token 且可能降低质量
"CLAUDE_CODE_SUBAGENT_MODEL": "deepseek-v4-flash[1m]"

// ❌ 不要同时设置 ANTHROPIC_AUTH_TOKEN 和 ANTHROPIC_API_KEY
// 两者同时存在会触发 Auth conflict 警告
// 只保留一个：推荐用 ANTHROPIC_AUTH_TOKEN

// ❌ 不要在多个来源设置同一变量为不同值
// settings.json、Shell 配置、注册表 — 三个来源会叠加
```

### 3.6 启动

```bash
claude
```

输入 `你好` 测试，能正常回复就配置成功了。

---

## 4. 配置项详解

| 变量 | 说明 | 推荐值 |
|------|------|--------|
| `ANTHROPIC_BASE_URL` | API 端点地址 | `https://api.deepseek.com/anthropic` |
| `ANTHROPIC_AUTH_TOKEN` | API 密钥 | `sk-xxx`（DeepSeek 平台获取） |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | Opus 级别任务使用的模型 | `deepseek-v4-pro[1m]` |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Sonnet 级别任务使用的模型 | `deepseek-v4-pro[1m]` |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | Haiku 级别任务使用的模型 | `deepseek-v4-flash[1m]` |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` | 禁用非必要网络请求 | `1` |
| `CLAUDE_CODE_EFFORT_LEVEL` | 思考深度 | `max` |
| `API_TIMEOUT_MS` | API 超时时间（毫秒） | `600000`（10分钟） |
| `model` | Claude Code 默认模型 | `"opus"` |

### 关于 `[1m]` 后缀

模型名后面的 `[1m]` 表示启用 DeepSeek V4 的 **100 万 token 上下文窗口**。不加这个后缀则使用默认的 64K 上下文。

---

## 5. 常见报错及解决方案

### 🔴 报错 1：`Auth conflict: Both a token and an API key are set`

```
Both ANTHROPIC_AUTH_TOKEN and ANTHROPIC_API_KEY are set.
This may lead to unexpected behavior.
```

**原因**：Claude Code 检测到两个认证变量同时存在，不知道该用哪个。

这个问题的棘手之处在于：**变量可能来自多个不同的来源，任何两个来源分别设置了不同的变量名就会触发冲突**。

```
┌─ 来源 1: settings.json 的 env 块
│   export ANTHROPIC_AUTH_TOKEN="sk-xxx"
│
├─ 来源 2: 当前进程环境变量（Shell/PowerShell session）
│   export ANTHROPIC_API_KEY="dummy-key"
│   ↑ 可能是父进程（终端、IDE）继承的，也可能是启动脚本注入的
│
├─ 来源 3: Shell 配置文件 (~/.bashrc, ~/.deepseek-claude/env)
│   export ANTHROPIC_API_KEY="dummy-key"
│   ↑ 新终端窗口自动加载
│
└─ 来源 4: Windows 注册表 (永久系统/用户变量)
    ANTHROPIC_API_KEY=dummy-key
    ↓
    所有新进程自动继承
```

> **关键**：Step 0 检查进程级变量是最直观的——它直接告诉你 Claude Code "看到" 了什么。如果进程级变量有值但注册表和配置文件都找不到来源，说明变量是由父进程（终端、IDE、启动脚本）注入的。

**标准排查流程（按顺序）**：

```bash
# Step 0: 检查当前进程环境变量 —— 最简单，直接看 Claude Code "看到" 了什么
echo "ANTHROPIC_AUTH_TOKEN: ${ANTHROPIC_AUTH_TOKEN:+(set)}"
echo "ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY:+(set)}"
# 或者
env | grep ANTHROPIC

# Step 1: 检查 settings.json
cat ~/.claude/settings.json | grep -E "AUTH_TOKEN|API_KEY"

# Step 2: 检查 Shell 配置文件
grep -r "ANTHROPIC_AUTH_TOKEN\|ANTHROPIC_API_KEY" ~/.bashrc ~/.bash_profile ~/.deepseek-claude/ 2>/dev/null

# Step 3 (Windows): 检查注册表+进程变量 —— 最容易被忽略！
powershell -Command "
  Write-Host 'Process Level (current session):'
  [Environment]::GetEnvironmentVariable('ANTHROPIC_AUTH_TOKEN','Process')
  [Environment]::GetEnvironmentVariable('ANTHROPIC_API_KEY','Process')
  Write-Host ''
  Write-Host 'Registry User Level:'
  [Environment]::GetEnvironmentVariable('ANTHROPIC_AUTH_TOKEN','User')
  [Environment]::GetEnvironmentVariable('ANTHROPIC_API_KEY','User')
"
```

**解决方案**：
- 选择保留 `ANTHROPIC_AUTH_TOKEN`（推荐）或 `ANTHROPIC_API_KEY` 中的一个
- 确保**所有来源**都用**同一个变量名**，且值一致
- 当前 session 立即修复：`unset ANTHROPIC_API_KEY`
- 永久修复：在 `~/.bashrc` 中添加 `unset ANTHROPIC_API_KEY 2>/dev/null`
- Windows 注册表残留的清理方法：

```powershell
# 删除注册表中的冲突变量（设为空字符串即删除）
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "", "User")
[Environment]::SetEnvironmentVariable("ANTHROPIC_AUTH_TOKEN", "", "User")
# 注：如果 settings.json 已经配置了这些变量，注册表不需要重复设置
```

**预防措施**：只在**一个来源**（推荐 `settings.json`）配置认证变量，其他来源一律清理干净。使用第 9 节的排查脚本可以一键检测所有来源。

---

### 🔴 报错 2：`401 Unauthorized` / 认证失败

```
API Error: 401 {"error":{"message":"Authentication Fails"}}
```

**可能原因**：
1. **变量名用错了** — DeepSeek 的 Anthropic 兼容端点推荐用 `ANTHROPIC_AUTH_TOKEN`（映射为 `x-api-key` 头）。`ANTHROPIC_API_KEY` 也能被识别，但可能与 DeepSeek 的认证格式不完全兼容
2. **API Key 过期或被吊销** — 去 DeepSeek 平台重新生成
3. **API Key 余额不足** — 检查账户余额

**解决方案**：

```bash
# 1. 确认用的是正确的变量名（DeepSeek 推荐用 AUTH_TOKEN）
export ANTHROPIC_AUTH_TOKEN="sk-你的key"   # ✅ DeepSeek 端点推荐
export ANTHROPIC_API_KEY="sk-你的key"      # ⚠️ 也能用，但不推荐

# 2. 清除可能缓存的旧认证
claude logout
```

---

### 🔴 报错 3：`400 Bad Request` — system role 错误

```
API Error: 400 {"error":{"message":"unknown variant system"}}
```

**原因**：Claude Code v2.1.156+ 会在 `messages` 数组里插入 `role: "system"` 的消息，但 DeepSeek API 只接受 `user` 和 `assistant` 角色。

**影响范围**：Claude Code >= v2.1.156 版本

**解决方案（三选一）**：

```bash
# 方案1: 降级 Claude Code（快速修复）
npm install -g @anthropic-ai/claude-code@2.1.154

# 方案2: 使用本地代理（proxy.js），自动将 system 转为 user
# 代理脚本见本文第 6 节

# 方案3: 等待 DeepSeek 更新适配新格式
```

---

### 🟡 报错 4：工具调用失败 / Tool result missing

```
Tool result missing due to internal error
```

**可能原因**：
1. **thinking / reasoning_content 不兼容** — DeepSeek 在思考模式下返回的 `reasoning_content` 未被正确处理
2. **流式输出截断** — DeepSeek 的 SSE 事件格式与 Anthropic 不完全一致

**解决方案**：
- 关闭 thinking 模式（在 settings.json 中不要设置 `thinking` 相关参数）
- 或使用本地代理关闭 thinking SSE 事件

---

### 🟡 报错 5：`Model not found` / 模型静默降级

```
# 不发报错，但实际用的不是 Pro
```

**原因**：
- 旧模型名 `deepseek-chat`、`deepseek-reasoner` 已于 **2025年7月24日** 废弃
- 如果传了不支持的模型名，DeepSeek API 会**静默降级为 `deepseek-v4-flash`**

**当前正确的模型名**：

| 旧名称（已废弃） | 新名称（当前） | 用途 |
|-----------------|---------------|------|
| `deepseek-chat` | `deepseek-v4-pro` | 主力编程模型（替代 Opus/Sonnet） |
| `deepseek-reasoner` | `deepseek-v4-flash` | 轻量任务（替代 Haiku） |

---

### 🟡 报错 6：图片/截图无法识别

```
I cannot view images directly.
```

**原因**：DeepSeek V4 Pro / Flash 是**纯文本模型**，不支持图片输入。即使通过 Anthropic 兼容端点，也无法处理 `image` 类型的 content block。

**解决方案**：
- 需要图片分析时，临时改回 Anthropic 原生 API
- 或用文字详细描述图片内容

---

### 🟡 报错 7：长时间任务超时

```
# 复杂任务中途中断
```

**解决方案**：

```json
// settings.json
{ "env": { "API_TIMEOUT_MS": "600000" } }
```

---

### 🟡 报错 8：配置不生效

**原因**：环境变量设置在了错误的地方。

**排查清单**：

```bash
# 1. 检查 Claude Code 实际读取到的配置
claude --debug 2>&1 | grep -E "ANTHROPIC|API_KEY|BASE_URL"

# 2. 确认 settings.json 位置
# Windows: C:\Users\<用户名>\.claude\settings.json
# Mac/Linux: ~/.claude/settings.json

# 3. 检查是否有其他配置文件覆盖
# settings.local.json 优先级高于 settings.json
```

---

## 6. 本地代理方案（进阶）

当直连遇到兼容性问题时，可以启动本地代理做格式转换。

### ⚠️ 代理的常见坑

通过实际排查，发现代理方案有两个隐蔽的坑：

**坑 1：硬编码过期的模型名**

很多代理脚本会写死 `model: 'deepseek-chat'`，这个模型名已于 **2025 年 7 月 24 日废弃**。DeepSeek API 收到不支持的模型名不会报错，而是**静默降级为 `deepseek-v4-flash`**——你以为在用 Pro，实际一直用的是 Flash。

**修复**：代理脚本应该根据请求中的模型名动态映射：

```javascript
// ❌ 错误：写死过期的模型名
requestData.model = 'deepseek-chat';

// ✅ 正确：根据请求动态选择
const requested = requestData.model || '';
if (requested.includes('v4-pro') || requested.includes('opus')) {
    requestData.model = 'deepseek-v4-pro';
} else if (requested.includes('v4-flash') || requested.includes('haiku')) {
    requestData.model = 'deepseek-v4-flash';
} else {
    requestData.model = 'deepseek-v4-pro';  // 默认用 Pro
}
```

**坑 2：认证 Key 的混淆**

代理方案下，认证分为两层：
- **Claude Code → 代理**：用 `ANTHROPIC_AUTH_TOKEN`（可以设为任意值，如 `dummy-key`）
- **代理 → DeepSeek**：用 `DEEPSEEK_API_KEY`（必须是真实的 DeepSeek API Key）

不要把真实 Key 放在 `ANTHROPIC_AUTH_TOKEN` 里——它只会发给本地代理，代理并不使用它。真实 Key 应该单独放在 `DEEPSEEK_API_KEY` 环境变量中。

### 代理脚本 (proxy.js)

```javascript
const http = require('http');
const https = require('https');

const LISTEN_PORT = 8765;
const DEEPSEEK_HOST = 'api.deepseek.com';
const DEEPSEEK_API_KEY = process.env.DEEPSEEK_API_KEY || '';

// 转换 Anthropic 消息格式 → OpenAI 消息格式
function transformMessages(messages) {
    return messages.map(msg => {
        const newMsg = { ...msg };
        // system → user（修复 v2.1.156+ 兼容问题）
        if (newMsg.role === 'system') {
            newMsg.role = 'user';
            newMsg.content = `[System Instructions]\n${newMsg.content}`;
        }
        // ... 更多转换逻辑
        return newMsg;
    });
}

const server = http.createServer((req, res) => {
    // /v1/messages → /v1/chat/completions
    let body = [];
    req.on('data', chunk => body.push(chunk));
    req.on('end', () => {
        const requestData = JSON.parse(Buffer.concat(body).toString());
        requestData.messages = transformMessages(requestData.messages || []);
        // 动态选择模型（避免硬编码过期模型名被静默降级）
        const requested = requestData.model || '';
        if (requested.includes('v4-pro') || requested.includes('opus') || requested.includes('sonnet')) {
            requestData.model = 'deepseek-v4-pro';
        } else if (requested.includes('v4-flash') || requested.includes('haiku')) {
            requestData.model = 'deepseek-v4-flash';
        } else {
            requestData.model = 'deepseek-v4-pro';  // 默认用 Pro
        }

        const payload = JSON.stringify(requestData);
        const proxyReq = https.request({
            hostname: DEEPSEEK_HOST,
            port: 443,
            path: '/v1/chat/completions',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + DEEPSEEK_API_KEY
            }
        }, (proxyRes) => {
            let data = [];
            proxyRes.on('data', chunk => data.push(chunk));
            proxyRes.on('end', () => {
                // 转换 OpenAI 响应 → Anthropic 格式
                res.end(JSON.stringify(transformResponse(JSON.parse(Buffer.concat(data).toString()))));
            });
        });
        proxyReq.write(payload);
        proxyReq.end();
    });
});

server.listen(8765, '127.0.0.1', () => {
    console.log('Proxy running at http://127.0.0.1:8765');
});
```

使用代理时，将 `ANTHROPIC_BASE_URL` 改为 `http://127.0.0.1:8765`。

---

## 7. 模型选择策略

| 任务类型 | 模型 | 说明 |
|----------|------|------|
| 复杂重构、架构设计 | `deepseek-v4-pro[1m]` | 最强推理能力 |
| 日常编码、Bug 修复 | `deepseek-v4-pro[1m]` | 主力模型 |
| 代码检查、快速搜索 | `deepseek-v4-flash[1m]` | 轻量快速 |
| 超长上下文 | 带 `[1m]` 后缀 | 100 万 token 窗口 |

**建议**：Opus 和 Sonnet 都映射到 `deepseek-v4-pro[1m]`，Haiku 映射到 `deepseek-v4-flash[1m]`。

---

## 8. DeepSeek Anthropic 兼容端点支持情况

| 功能 | 支持状态 |
|------|----------|
| `system` 提示词 | ✅ 支持 |
| `max_tokens` | ✅ 支持 |
| `temperature` | ✅ 支持 (0.0–2.0) |
| `top_p` | ✅ 支持 |
| `stop_sequences` | ✅ 支持 |
| `tools` (函数调用) | ✅ 支持 |
| `thinking` (思考模式) | ⚠️ 部分支持 (budget_tokens 被忽略) |
| 图片输入 | ❌ 不支持 |
| `cache_control` | ⚠️ 被忽略 (不报错但不生效) |
| `top_k` | ⚠️ 被忽略 |

---

## 9. 快速排查脚本

把以下内容保存为 `check.ps1`，一键检查配置状态：

```powershell
Write-Host "=== Process-Level Environment (what Claude Code sees) ===" -ForegroundColor Cyan
$p1 = [Environment]::GetEnvironmentVariable("ANTHROPIC_AUTH_TOKEN", "Process")
$p2 = [Environment]::GetEnvironmentVariable("ANTHROPIC_API_KEY", "Process")
$p3 = [Environment]::GetEnvironmentVariable("ANTHROPIC_BASE_URL", "Process")

if ($p1 -and $p2) {
    Write-Host "!!! AUTH CONFLICT (Process): Both AUTH_TOKEN and API_KEY are set !!!" -ForegroundColor Red
} elseif ($p1) {
    Write-Host "ANTHROPIC_AUTH_TOKEN: SET (OK)" -ForegroundColor Green
} elseif ($p2) {
    Write-Host "ANTHROPIC_API_KEY: SET (OK)" -ForegroundColor Green
} else {
    Write-Host "!!! NO AUTH TOKEN IN PROCESS !!!" -ForegroundColor Red
}
Write-Host "ANTHROPIC_BASE_URL (Process): $p3" -ForegroundColor $(if ($p3 -eq "https://api.deepseek.com/anthropic") { "Green" } else { "Yellow" })

Write-Host "`n=== Registry User-Level Variables ===" -ForegroundColor Cyan
$v1 = [Environment]::GetEnvironmentVariable("ANTHROPIC_AUTH_TOKEN", "User")
$v2 = [Environment]::GetEnvironmentVariable("ANTHROPIC_API_KEY", "User")
$v3 = [Environment]::GetEnvironmentVariable("ANTHROPIC_BASE_URL", "User")
$v4 = [Environment]::GetEnvironmentVariable("DEEPSEEK_API_KEY", "User")

if ($v1 -and $v2) {
    Write-Host "!!! REGISTRY CONFLICT: Both AUTH_TOKEN and API_KEY in User registry !!!" -ForegroundColor Red
    Write-Host "    Run: [Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY','','User')" -ForegroundColor Yellow
}
Write-Host "ANTHROPIC_AUTH_TOKEN (User): $(if ($v1) { 'SET' } else { 'not set' })"
Write-Host "ANTHROPIC_API_KEY (User): $(if ($v2) { 'SET' } else { 'not set' })" -ForegroundColor $(if ($v2) { 'Red' } else { 'Green' })
Write-Host "ANTHROPIC_BASE_URL (User): $v3" -ForegroundColor $(if ($v3 -eq "https://api.deepseek.com/anthropic") { "Green" } else { "Yellow" })
Write-Host "DEEPSEEK_API_KEY (User): $(if ($v4) { 'SET' } else { 'not set' })"

# 如果 Process 有冲突但 Registry 干净，说明变量来自父进程或 Shell 配置
if ($p1 -and $p2 -and -not ($v1 -and $v2)) {
    Write-Host "`n=== 冲突来源分析 ===" -ForegroundColor Yellow
    Write-Host "Process 层存在冲突，但 Registry 中没有同时设置两个变量。" -ForegroundColor Yellow
    Write-Host "冲突变量可能来自：" -ForegroundColor Yellow
    Write-Host "  1. Shell 配置文件 (~/.bashrc, ~/.bash_profile)" -ForegroundColor Yellow
    Write-Host "  2. 父进程（终端、IDE）注入的环境变量" -ForegroundColor Yellow
    Write-Host "  3. 当前 session 手动 export" -ForegroundColor Yellow
    Write-Host "临时修复: unset ANTHROPIC_API_KEY" -ForegroundColor Green
    Write-Host "永久修复: 在 ~/.bashrc 中添加 'unset ANTHROPIC_API_KEY 2>/dev/null'" -ForegroundColor Green
}

Write-Host "`n=== Config Files ===" -ForegroundColor Cyan
$settingsFile = "$env:USERPROFILE\.claude\settings.json"
if (Test-Path $settingsFile) {
    Write-Host "settings.json: EXISTS" -ForegroundColor Green
    $settings = Get-Content $settingsFile | ConvertFrom-Json
    Write-Host "  model: $($settings.model)"
    Write-Host "  base_url: $($settings.env.ANTHROPIC_BASE_URL)"
} else {
    Write-Host "settings.json: MISSING" -ForegroundColor Red
}

Write-Host "`n=== Claude Code Version ===" -ForegroundColor Cyan
claude --version 2>$null

Write-Host "`n=== API Connectivity Test ===" -ForegroundColor Cyan
# 使用 Process 级别的变量（实际生效的值）
$testUrl = if ($p3) { $p3 } else { $v3 }
$testKey = if ($p1) { $p1 } elseif ($p2) { $p2 } else { $v1 }
if ($testUrl -and $testKey) {
    try {
        $r = Invoke-WebRequest -Uri "$testUrl/v1/models" -Headers @{ "x-api-key" = $testKey } -UseBasicParsing -TimeoutSec 10
        Write-Host "API reachable: YES ($($r.StatusCode))" -ForegroundColor Green
    } catch {
        Write-Host "API unreachable: $_" -ForegroundColor Red
    }
} else {
    Write-Host "SKIPPED: Missing URL or API Key" -ForegroundColor Yellow
}
}
```

---

## 10. 实战排查案例：Auth Conflict 完整追踪

以下是一个真实案例——在 Windows 上配置 Claude Code + DeepSeek 后，每次启动都报 `Auth conflict` 警告。排查过程揭示了这类问题的典型根源。

### 现象

```bash
$ claude
‼ Auth conflict: Both a token (ANTHROPIC_AUTH_TOKEN) and an API key
  (ANTHROPIC_API_KEY) are set. This may lead to unexpected behavior.
```

### 排查过程

**第 1 步：检查 settings.json**

```powershell
cat ~/.claude/settings.json
```

发现只设置了 `ANTHROPIC_AUTH_TOKEN`，没有 `ANTHROPIC_API_KEY`——初步判断没问题。

**第 2 步：检查 Bash 配置文件**

```bash
cat ~/.bashrc
```

发现引用了 `~/.deepseek-claude/env`，该文件设置了：
```bash
export ANTHROPIC_AUTH_TOKEN="sk-xxx"
```

也没有 `ANTHROPIC_API_KEY`——还是没问题？

**第 3 步：检查 Windows 注册表（关键！）**

```powershell
[Environment]::GetEnvironmentVariable("ANTHROPIC_API_KEY", "User")
[Environment]::GetEnvironmentVariable("ANTHROPIC_AUTH_TOKEN", "User")
```

输出：
```
dummy-key              ← 这里！注册表里还残留着 ANTHROPIC_API_KEY！
sk-xxx                 ← 和 ANTHROPIC_AUTH_TOKEN 同时存在
```

**根因**：之前的安装脚本 (`setup-permanent.ps1`) 通过 `[Environment]::SetEnvironmentVariable` 将 `ANTHROPIC_API_KEY=dummy-key` 写入了 Windows 用户级环境变量（注册表）。而 `settings.json` 又设置了 `ANTHROPIC_AUTH_TOKEN`。两个来源叠加，导致两个变量同时存在。

**第 4 步：清理**

```powershell
# 删除注册表中的冲突变量
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "", "User")
[Environment]::SetEnvironmentVariable("ANTHROPIC_AUTH_TOKEN", "", "User")
[Environment]::SetEnvironmentVariable("ANTHROPIC_BASE_URL", "", "User")
```

清理后只保留 `settings.json` 中的配置，警告消失。

### 教训

1. **Windows 上环境变量有多个来源**：注册表（用户级 + 系统级）、Shell 配置文件（`.bashrc`、`.bash_profile`）、`settings.json` 的 `env` 块、当前进程继承的变量。任何一个来源的残留都可能导致冲突。
2. **注册表是隐蔽的坑**：用 `setup-permanent.ps1` 之类脚本设置的环境变量，在新开 PowerShell 时会自动加载，不易察觉。
3. **进程级变量也可能独立存在**：即使注册表和配置文件都干净，`ANTHROPIC_API_KEY` 仍可能从父进程（终端模拟器、IDE、启动脚本）继承。此时 `echo $ANTHROPIC_API_KEY` 能直接看到，但排查注册表时找不到来源。修复方法：`unset ANTHROPIC_API_KEY` 并加到 `~/.bashrc`。
4. **排障口诀**：出问题时按 **进程环境变量 → settings.json → Shell 配置文件 → 注册表** 的顺序逐个排查。
5. **代理的模型名是沉默杀手**：硬编码 `deepseek-chat` 不会报错，但会让你静默降级到 Flash。一定要检查代理脚本中的模型映射逻辑。
6. **清理注册表后要新开终端**：当前 session 继承的环境变量不会因为注册表清理而消失——它们是进程启动时复制的快照。

---

## 11. 总结

| 事项 | 要点 |
|------|------|
| **推荐方案** | 直连 DeepSeek Anthropic 端点，只在遇到兼容问题时才考虑代理 |
| **关键配置** | `ANTHROPIC_AUTH_TOKEN` + `ANTHROPIC_BASE_URL`（不要同时设置 `ANTHROPIC_API_KEY`） |
| **配置原则** | 只在**一个来源**配置（推荐 settings.json），避免多来源叠加 |
| **常见坑** | 双认证冲突、模型名过旧、注册表残留、代理硬编码模型、v2.1.156 system role |
| **不要做的事** | 设置 `CLAUDE_CODE_SUBAGENT_MODEL`、同时设两个认证变量、代理中写死 `deepseek-chat` |
| **不支持功能** | 图片输入、prompt caching |
| **成本** | 比 Anthropic 原生便宜 50-100 倍 |
| **排障顺序** | 进程环境变量 → settings.json → Shell 配置文件 → 注册表 → 代理脚本（如有） |

---

*最后更新：2026-05-29 | Claude Code v2.1.156 | DeepSeek V4 Pro*

---

**参考资料**：
- [DeepSeek Anthropic API 官方文档](https://api-docs.deepseek.com/zh-cn/guides/anthropic_api)
- [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code)
- [DeepSeek V4 接入 Claude Code 指南 (掘金)](https://juejin.cn/post/7632644475747860515)
- [Windows + Claude Code + DeepSeek V4 配置记录](https://www.cnblogs.com/yuweijade/p/20049136)
- [在 Claude Code 里跑 DeepSeek V4 Pro (博客园)](https://www.cnblogs.com/avaworld/p/19930707)
- [Claude Code 接入 DeepSeek 问题排查手册 (GitCode)](https://gitcode.csdn.net/69bc0ac70a2f6a37c598a602.html)

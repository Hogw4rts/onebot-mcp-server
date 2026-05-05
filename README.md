# onebot-mcp-server

将 OneBot v11 + NapCat 扩展 API 暴露为 MCP 工具，供 Hermes Gateway 的 LLM Agent 调用。

连接 `kovi-plugin-hermes` 的 OneBot API 桥接，提供 **53 个工具**（27 只读 + 26 写入）。

## 工具列表

### OneBot v11 — 只读（19）

| 工具 | 说明 |
|------|------|
| `onebot_get_login_info` | 获取机器人自身 QQ 账号信息 |
| `onebot_get_friend_list` | 获取好友列表 |
| `onebot_get_group_list` | 获取已加入的群列表 |
| `onebot_get_group_info` | 获取群详情 |
| `onebot_get_group_members` | 获取群成员列表（分页） |
| `onebot_get_member_info` | 获取群成员详情 |
| `onebot_get_user_info` | 获取 QQ 用户信息（非好友也可） |
| `onebot_get_message` | 通过消息 ID 获取消息 |
| `onebot_get_forward_msg` | 获取合并转发消息内容 |
| `onebot_get_group_honor_info` | 获取群荣誉信息（龙王、表演者等） |
| `onebot_get_status` | 获取机器人运行状态 |
| `onebot_get_version_info` | 获取 OneBot 实现版本信息 |
| `onebot_can_send_image` | 检查是否可以发送图片 |
| `onebot_can_send_record` | 检查是否可以发送语音 |
| `onebot_get_cookies` | 获取指定域名的 Cookies |
| `onebot_get_csrf_token` | 获取 CSRF Token |
| `onebot_get_credentials` | 获取凭证（Cookies + CSRF Token） |
| `onebot_get_record` | 获取/转换语音文件 |
| `onebot_get_image` | 获取图片文件信息 |

### OneBot v11 — 写入（17，需要 `admin_id`）

| 工具 | 说明 |
|------|------|
| `onebot_send_group_msg` | 发送群消息（支持纯文本和消息段） |
| `onebot_send_private_msg` | 发送私聊消息（支持纯文本和消息段） |
| `onebot_send_like` | 给 QQ 用户点赞 |
| `onebot_set_group_ban` | 禁言群成员（0 = 解除禁言） |
| `onebot_set_group_whole_ban` | 开启/关闭全员禁言 |
| `onebot_set_group_admin` | 设置/取消群管理员 |
| `onebot_set_group_anonymous` | 开启/关闭群匿名聊天 |
| `onebot_set_group_anonymous_ban` | 禁言匿名用户 |
| `onebot_set_group_card` | 设置群名片 |
| `onebot_set_group_name` | 修改群名 |
| `onebot_set_group_leave` | 退出群聊 |
| `onebot_set_group_special_title` | 设置群专属头衔 |
| `onebot_set_group_kick` | 踢出群成员 |
| `onebot_set_friend_add_request` | 处理加好友请求 |
| `onebot_set_group_add_request` | 处理加群请求/邀请 |
| `onebot_delete_msg` | 撤回消息 |
| `onebot_clean_cache` | 清理 OneBot 服务器缓存 |

### NapCat 扩展 — 只读（8）

| 工具 | 说明 |
|------|------|
| `onebot_get_group_msg_history` | 获取群消息历史记录 |
| `onebot_get_group_file_system_info` | 获取群文件系统信息（空间、数量） |
| `onebot_get_group_root_files` | 获取群根目录文件列表 |
| `onebot_get_group_files_by_folder` | 获取群子目录文件列表 |
| `onebot_get_group_file_url` | 获取群文件下载链接 |
| `onebot_get_file` | 通过 file_id 或路径获取文件信息 |
| `onebot_get_group_at_all_remain` | 获取群 @全体成员 剩余次数 |
| `onebot_get_essence_msg_list` | 获取群精华消息列表 |

### NapCat 扩展 — 写入（9，需要 `admin_id`）

| 工具 | 说明 |
|------|------|
| `onebot_download_file` | 下载文件到服务器缓存目录 |
| `onebot_upload_group_file` | 上传文件到群文件系统 |
| `onebot_upload_private_file` | 上传文件到私聊 |
| `onebot_delete_group_file` | 删除群文件 |
| `onebot_create_group_file_folder` | 创建群文件文件夹 |
| `onebot_delete_group_folder` | 删除群文件文件夹 |
| `onebot_set_essence_msg` | 设置精华消息 |
| `onebot_delete_essence_msg` | 移除精华消息 |
| `onebot_send_group_forward_msg` | 发送合并转发消息 |

## 消息段支持

`onebot_send_group_msg` 和 `onebot_send_private_msg` 支持纯文本和富文本消息段：

**纯文本（向后兼容）：**
```json
{"message": "你好世界"}
```

**富文本消息段：**
```json
{
  "message": [
    {"type": "text", "data": {"text": "你好 "}},
    {"type": "at", "data": {"qq": "123456"}},
    {"type": "image", "data": {"file": "https://example.com/img.jpg"}},
    {"type": "reply", "data": {"id": "98765"}},
    {"type": "face", "data": {"id": "178"}}
  ]
}
```

支持的消息段类型：`text`、`image`、`at`、`reply`、`face`，以及通过透传支持的自定义类型。

## 配置

环境变量：

- `ONEBOT_API_BASE`：OneBot API 地址（必填，如 `http://localhost:5801`）
- `ONEBOT_API_KEY`：Bearer Token 认证密钥（必填）
- `MCP_TRANSPORT`：传输模式 — `stdio`（默认）或 `http`（StreamableHTTP）

## 开发

```bash
# 安装开发依赖
uv pip install -e ".[dev]"

# 运行测试
pytest

# 代码检查
ruff check src/ tests/
```

## 部署

### 方式一：直接安装（推荐，用于 Hermes）

Hermes Gateway 入口脚本通过 `uv pip install` 安装：

```yaml
# Hermes 部署 entrypoint
uv pip install onebot-mcp-server @ git+https://github.com/Hogw4rts/onebot-mcp-server.git
```

### 方式二：Hermes config.yaml

```yaml
mcp_servers:
  onebot:
    command: /opt/hermes/.venv/bin/onebot-mcp-server
    env:
      ONEBOT_API_BASE: "http://taffy.tenant-1.svc.cluster.local:5801"
      ONEBOT_API_KEY: "your-api-key"
    tools:
      include:
        - onebot_get_*
        - onebot_send_*
        - onebot_set_*
        - onebot_delete_*
        - onebot_can_*
        - onebot_clean_*
        - onebot_download_*
        - onebot_upload_*
        - onebot_create_*
```

### 方式三：HTTP 传输

```bash
MCP_TRANSPORT=http MCP_PORT=8080 onebot-mcp-server
```

## 架构

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  QQ 客户端    │────▶│ kovi-plugin  │     │   浏览器     │
│  (NapCat)    │     │   hermes     │     └──────┬──────┘
└─────────────┘     │  (Rust)      │              │
                    │ OneBot API   │     ┌────────▼──────┐
                    │  :5801       │     │  axum Router  │
                    └──────┬───────┘     │  (api.rs)     │
                           │              └──────┬──────┘
                      ┌────▼────┐         ┌──────▼──────┐
                      │RuntimeBot│        │ auth.rs      │
                      │  (Kovi)  │        │ (JWT+登录)   │
                      └────┬────┘         └─────────────┘
                           │
                    ┌──────▼───────┐
                    │ onebot-mcp   │  ← 本仓库
                    │  (Python)    │
                    │  53 个工具    │
                    └──────────────┘
```

两个入口共享一个 `RuntimeBot`：
1. **QQ 命令**（`kovi-plugin-hermes`）— `/acl`、`/plugin`、`/sys` + LLM 对话
2. **HTTP API**（`onebot_api.rs`）— RESTful 接口，供 React 前端 + MCP 服务器调用

MCP 服务器连接 OneBot API 桥接，通过 MCP 协议将全部 53 个工具暴露给 Hermes LLM Agent。

## 写入操作与授权

所有写入操作需要 `admin_id` 参数 — 即授权管理员的 QQ 号。OneBot API 桥接会根据 `kovi.conf.toml` 中配置的管理员列表验证该 ID。

## 许可证

GPL-3.0
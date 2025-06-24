# Cursor 集成指南 - todolist mcp（MCP Server 版，stdio 模式）

## 一、服务部署与启动

1. 安装依赖
   ```bash
   pip install -e .
   pip install modelcontextprotocol
   ```
2. 无需手动启动服务，由 agent/Claude/Cursor 自动以子进程方式拉起。

---

## 二、Cursor/Claude/agent 工具配置（stdio 模式）

### 1. Claude for Desktop 配置

在 `claude_desktop_config.json` 中添加如下内容（以 Windows 路径为例）：

```json
{
  "mcpServers": {
    "todolist": {
      "command": "python",
      "args": ["-m", "todolist_mcp.todolist_mcp"]
    }
  }
}
```

- `command`：Python 解释器（如 `python`）。
- `args`：模块方式启动你的 MCP Server。
- 不需要指定端口，Claude/Cursor 会自动通过 stdio 管道与 MCP Server 通信。
- 路径可根据实际安装位置调整。

### 2. 其他 agent 配置

- 只需以子进程方式拉起 MCP Server，并通过 stdio 交互，无需 HTTP 地址。
- 适用于所有支持 MCP stdio server 的客户端。

---

## 三、提示词模板

- “请通过 MCP Server 的工具发现功能，自动调用 todolist 相关工具。”
- 例如：
  - “请注册一个新的工作计划。”
  - “请同步计划进展。”
  - “请查询 agent 的所有计划。”

---

## 四、注意事项

- stdio 模式无需端口配置，避免端口冲突。
- MCP Server 生命周期由 agent/Claude/Cursor 自动管理。
- 如需调试，可手动运行 `python -m todolist_mcp.todolist_mcp`，并通过 MCP CLI 工具交互。

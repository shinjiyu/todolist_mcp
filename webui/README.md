# webui

本目录用于 HTTP 服务和前端页面，展示所有计划及其进度详情。

## 启动 HTTP 服务

在项目根目录下运行：

```
uvicorn webui.app:app --reload --port 8000
```

- 访问 http://localhost:8000/
- 可将此命令写入脚本（如 run_webui.bat 或 run_webui.sh）以简化启动。

# todolist mcp 使用文档

## 简介

todolist mcp 是一个本地 MCP 风格的工作计划服务，支持 agent 注册、同步、查询工作计划。所有数据以 JSON 文件形式存储于系统临时目录，适合本地项目内 agent 协作。

## 安装依赖

建议使用 Python 3.8 及以上版本。

```bash
pip install fastapi uvicorn
```

## 启动服务

在虚拟人目录下运行：

```bash
uvicorn todolist_mcp:app --reload
```

服务启动后，默认监听 http://127.0.0.1:8000

## 数据存储说明

- 所有计划数据存储于本地系统临时目录（如 Windows 的 C:\Windows\Temp，Linux/Mac 的 /tmp）下的 plans.json 文件。
- 服务启动时自动加载 plans.json，运行期间所有变更实时写回。
- 若 plans.json 不存在，服务启动时自动创建。

## 接口说明

### 1. 注册新计划

- **POST /register_plan**
- **请求体**：

```json
{
  "agent_id": "agent001",
  "title": "开发新功能",
  "description": "实现用户登录模块",
  "steps": [
    {
      "step_number": 1,
      "title": "设计接口",
      "detail": "定义API结构",
      "tech_solution": "FastAPI",
      "status": "pending"
    },
    {
      "step_number": 2,
      "title": "实现后端",
      "detail": "编写API逻辑",
      "tech_solution": "Python",
      "status": "pending"
    }
  ]
}
```

- **返回**：

```json
{ "plan_id": "xxxx-xxxx-xxxx" }
```

### 2. 同步计划进展

- **POST /sync_progress/{plan_id}**
- **请求体**：

```json
{
  "current_step": 2,
  "status": "in_progress",
  "progress_note": "后端开发中"
}
```

- **返回**：

```json
{ "status": "updated" }
```

### 3. 查询下一个未完成步骤

- **GET /get_next_step/{plan_id}**
- **返回**：

```json
{"next_step": {"step_number": 2, "title": "实现后端", ...}}
```

### 4. 查询计划详情

- **GET /get_plan_detail/{plan_id}**
- **返回**：

```json
{
  "plan_id": "...",
  "agent_id": "...",
  "title": "...",
  "description": "...",
  "steps": [...],
  "current_step": 2,
  "status": "in_progress"
}
```

### 5. 查询 agent 的所有计划

- **GET /list_plans?agent_id=xxx**
- **返回**：

```json
{"plans": [ ... ]}
```

## 示例 Demo

1. 注册计划

```bash
curl -X POST "http://127.0.0.1:8000/register_plan" -H "Content-Type: application/json" -d '{
  "agent_id": "agent001",
  "title": "开发新功能",
  "description": "实现用户登录模块",
  "steps": [
    {"step_number": 1, "title": "设计接口", "detail": "定义API结构", "tech_solution": "FastAPI", "status": "pending"},
    {"step_number": 2, "title": "实现后端", "detail": "编写API逻辑", "tech_solution": "Python", "status": "pending"}
  ]
}'
```

2. 同步进展

```bash
curl -X POST "http://127.0.0.1:8000/sync_progress/{plan_id}" -H "Content-Type: application/json" -d '{
  "current_step": 2,
  "status": "in_progress",
  "progress_note": "后端开发中"
}'
```

3. 查询下一步

```bash
curl "http://127.0.0.1:8000/get_next_step/{plan_id}"
```

4. 查询计划详情

```bash
curl "http://127.0.0.1:8000/get_plan_detail/{plan_id}"
```

5. 查询所有计划

```bash
curl "http://127.0.0.1:8000/list_plans?agent_id=agent001"
```

---

如需自定义 plans.json 路径或其他高级用法，请参考源码详细注释。

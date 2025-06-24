## register_plan 工具参数说明

- **agent_id** (str, 必填): agent 标识
- **title** (str, 必填): 计划标题
- **description** (str, 必填): 计划描述
- **steps** (List[Dict], 必填): 步骤列表，每个元素为字典，包含：
  - step_number (int, 必填): 步骤序号，从 1 开始
  - title (str, 必填): 步骤标题
  - status (str, 必填): 步骤状态（pending/in_progress/completed）
  - detail (str, 可选): 步骤详细描述
  - tech_solution (str, 可选): 技术方案

### steps 字段示例

```
[
  {"step_number": 1, "title": "设计接口", "detail": "定义API结构", "tech_solution": "FastAPI", "status": "pending"},
  {"step_number": 2, "title": "实现后端", "detail": "编写API逻辑", "tech_solution": "Python", "status": "pending"}
]
```

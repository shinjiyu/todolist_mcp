# todolist mcp 设计说明

## 一、项目定位

todolist mcp 是一个本地服务，帮助 agent 设计、注册、同步和查询工作计划。数据以 JSON 文件形式存储于系统公共 temp 目录，服务启动时加载数据，仅限项目内本地使用。

## 二、核心功能（MCP 工具定义）

### 1. register_plan

- **描述**：注册一个新的工作计划，包含步骤、描述、技术方案等。
- **参数**：
  - agent_id: string
  - title: string
  - description: string
  - steps: list of {step_number, title, detail, tech_solution}
- **返回**：plan_id
- **提示词模板**：
  > 请为 agent {agent_id} 注册一个新计划，标题为 {title}，描述为 {description}，包含以下步骤：{steps}。

### 2. sync_progress

- **描述**：同步某个计划的进展，更新当前步骤和状态。
- **参数**：
  - plan_id: string
  - current_step: int
  - status: string（如 in_progress, completed, blocked）
  - progress_note: string
- **返回**：status
- **提示词模板**：
  > 请同步计划 {plan_id} 的进展，当前步骤为 {current_step}，状态为 {status}，备注：{progress_note}。

### 3. get_next_step

- **描述**：获取某个计划的下一个未完成步骤。
- **参数**：
  - plan_id: string
- **返回**：next_step（结构体）
- **提示词模板**：
  > 请查询计划 {plan_id} 的下一个未完成步骤。

### 4. get_plan_detail

- **描述**：获取某个计划的全部详细信息。
- **参数**：
  - plan_id: string
- **返回**：plan_detail（结构体）
- **提示词模板**：
  > 请查询计划 {plan_id} 的详细信息。

### 5. list_plans（可选）

- **描述**：获取 agent 的所有计划。
- **参数**：
  - agent_id: string
- **返回**：plans（列表）

## 三、数据存储

- 数据以 JSON 文件形式存储于系统 temp 目录（如 Windows 的 C:\Windows\Temp，Linux/Mac 的 /tmp）。
- 文件结构示例：

```json
{
  "plans": [
    {
      "plan_id": "string",
      "agent_id": "string",
      "title": "string",
      "description": "string",
      "steps": [
        {
          "step_number": 1,
          "title": "string",
          "detail": "string",
          "tech_solution": "string",
          "status": "pending|in_progress|completed"
        }
      ],
      "current_step": 1,
      "status": "in_progress"
    }
  ]
}
```

## 四、实现建议

- 推荐 Python（FastAPI/Flask）实现，轻量易维护。
- 工具以 mcp 协议注册，供 agent 通过工具调用。
- 数据以 JSON 文件形式存储于本地系统临时目录（如 Windows 的 C:\Windows\Temp，Linux/Mac 的 /tmp），文件名如 plans.json。
- 服务启动时自动从临时目录加载 plans.json 数据文件。
- 运行期间所有计划数据在内存中操作，任何变更（如注册计划、同步进展等）实时写回 plans.json 文件，保证数据持久化。
- 若 plans.json 文件不存在，服务启动时自动创建空白结构。
- 服务仅限本地项目内使用，无需复杂认证和分布式部署。

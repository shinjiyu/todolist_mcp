## register_plan 工具接口说明（最新版）

### 功能

注册一个新的工作计划。

### 请求参数

| 参数名      | 类型       | 必填 | 说明                  |
| ----------- | ---------- | ---- | --------------------- |
| agent_id    | string     | 是   | 发起注册的 agent 标识 |
| title       | string     | 是   | 计划标题              |
| description | string     | 是   | 计划描述              |
| steps       | List[Step] | 是   | 计划的步骤列表        |

#### Step 对象格式

每个 step 是一个字典，推荐如下字段：

| 字段名        | 类型   | 必填 | 说明                                      |
| ------------- | ------ | ---- | ----------------------------------------- |
| step_number   | int    | 是   | 步骤序号（从 1 开始）                     |
| title         | string | 是   | 步骤标题                                  |
| status        | string | 是   | 步骤状态（pending/in_progress/completed） |
| detail        | string | 否   | 步骤详细描述                              |
| tech_solution | string | 否   | 技术方案                                  |

#### steps 字段示例

```
[
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
```

### 返回值

```
{
  "plan_id": "xxx-xxx-xxx"
}
"
```

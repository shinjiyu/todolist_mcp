# 此文件内容与原 todolist_mcp.py 相同，直接复制即可。
# 你可以将原 todolist_mcp.py 的全部内容粘贴到这里。 

from typing import List, Dict, Any, Optional
import os
import json
import tempfile
from uuid import uuid4
from mcp.server.fastmcp import FastMCP

# ----------------------
# 数据模型与存储
# ----------------------
TEMP_DIR = tempfile.gettempdir()
PROJECT_NAME = "default"

def get_data_file():
    return os.path.join(TEMP_DIR, f"{PROJECT_NAME}_plans.json")

def load_data():
    data_file = get_data_file()
    if os.path.exists(data_file):
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {"plans": []}

def save_data(data):
    data_file = get_data_file()
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ----------------------
# MCP Server (stdio) 实现
# ----------------------
mcp = FastMCP("todolist")

@mcp.tool()
def register_plan(agent_id: str, title: str, description: str, steps: List[Dict[str, Any]]) -> Dict:
    """
    注册一个新的工作计划

    参数:
    - agent_id: agent 标识（字符串，必填）
    - title: 计划标题（字符串，必填）
    - description: 计划描述（字符串，必填）
    - steps: 步骤列表（List[Dict]，必填），每个元素为字典，包含如下字段：
        - step_number: int，步骤序号（从1开始，必填）
        - title: str，步骤标题（必填）
        - status: str，步骤状态（pending/in_progress/completed，必填）
        - detail: str，步骤详细描述（可选）
        - tech_solution: str，技术方案（可选）

    steps 示例：
    [
      {"step_number": 1, "title": "设计接口", "detail": "定义API结构", "tech_solution": "FastAPI", "status": "pending"},
      {"step_number": 2, "title": "实现后端", "detail": "编写API逻辑", "tech_solution": "Python", "status": "pending"}
    ]

    返回值:
    - plan_id: 新注册计划的唯一ID
    """
    data = load_data()
    plan_id = str(uuid4())
    plan = {
        "plan_id": plan_id,
        "agent_id": agent_id,
        "title": title,
        "description": description,
        "steps": steps,
        "current_step": 1,
        "status": "in_progress"
    }
    data["plans"].append(plan)
    save_data(data)
    return {"plan_id": plan_id}

@mcp.tool()
def sync_progress(plan_id: str, current_step: int, status: str, progress_note: Optional[str] = None) -> Dict:
    """同步计划进展"""
    data = load_data()
    for plan in data["plans"]:
        if plan["plan_id"] == plan_id:
            plan["current_step"] = current_step
            plan["status"] = status
            for step in plan["steps"]:
                if step["step_number"] < current_step:
                    step["status"] = "completed"
                elif step["step_number"] == current_step:
                    step["status"] = "in_progress"
                else:
                    step["status"] = "pending"
            save_data(data)
            return {"status": "updated"}
    return {"error": "Plan not found"}

@mcp.tool()
def get_next_step(plan_id: str) -> Dict:
    """获取某个计划的下一个未完成步骤"""
    data = load_data()
    for plan in data["plans"]:
        if plan["plan_id"] == plan_id:
            for step in plan["steps"]:
                if step["status"] != "completed":
                    return {"next_step": step}
            return {"next_step": None}
    return {"error": "Plan not found"}

@mcp.tool()
def get_plan_detail(plan_id: str) -> Dict:
    """获取某个计划的全部详细信息"""
    data = load_data()
    for plan in data["plans"]:
        if plan["plan_id"] == plan_id:
            return plan
    return {"error": "Plan not found"}

@mcp.tool()
def list_plans(agent_id: str) -> Dict:
    """获取 agent 的所有计划"""
    data = load_data()
    agent_plans = [p for p in data["plans"] if p["agent_id"] == agent_id]
    return {"plans": agent_plans}

if __name__ == "__main__":
    mcp.run(transport='stdio') 
import subprocess
import sys
import json
import time
import os
import pytest

MCP_CMD = [sys.executable, '-m', 'todolist_mcp.todolist_mcp']

@pytest.fixture(scope="module")
def mcp_server():
    proc = subprocess.Popen(
        MCP_CMD,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    time.sleep(1)  # 等待 server 启动
    yield proc
    proc.terminate()
    proc.wait()

# MCP stdio 协议简单封装

def mcp_call(proc, tool, parameters):
    req = json.dumps({"tool": tool, "parameters": parameters}) + "\n"
    proc.stdin.write(req)
    proc.stdin.flush()
    # 读取一行响应
    resp = proc.stdout.readline()
    return json.loads(resp)

def test_register_and_query(mcp_server):
    proc = mcp_server
    # 注册计划
    steps = [
        {"step_number": 1, "title": "设计接口", "detail": "定义API结构", "tech_solution": "FastAPI", "status": "pending"},
        {"step_number": 2, "title": "实现后端", "detail": "编写API逻辑", "tech_solution": "Python", "status": "pending"}
    ]
    reg = mcp_call(proc, "register_plan", {
        "agent_id": "agent001",
        "title": "开发新功能",
        "description": "实现用户登录模块",
        "steps": steps
    })
    assert "plan_id" in reg
    plan_id = reg["plan_id"]

    # 查询所有计划
    plans = mcp_call(proc, "list_plans", {"agent_id": "agent001"})
    assert "plans" in plans
    assert any(p["plan_id"] == plan_id for p in plans["plans"])

    # 查询计划详情
    detail = mcp_call(proc, "get_plan_detail", {"plan_id": plan_id})
    assert detail["plan_id"] == plan_id
    assert detail["title"] == "开发新功能"

    # 同步进展
    sync = mcp_call(proc, "sync_progress", {"plan_id": plan_id, "current_step": 2, "status": "in_progress"})
    assert sync["status"] == "updated"

    # 查询下一步
    next_step = mcp_call(proc, "get_next_step", {"plan_id": plan_id})
    assert "next_step" in next_step 
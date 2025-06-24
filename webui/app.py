from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from todolist_mcp import todolist_mcp

app = FastAPI()

@app.get("/plans", response_class=HTMLResponse)
def show_plans():
    data = todolist_mcp.load_data()
    plans = data.get("plans", [])
    html = "<h1>所有计划</h1>"
    for plan in plans:
        html += f"<div style='border:1px solid #ccc;margin:10px;padding:10px;'>"
        html += f"<h2>{plan['title']}</h2>"
        html += f"<p><b>描述:</b> {plan['description']}</p>"
        html += f"<p><b>状态:</b> {plan['status']}</p>"
        html += f"<p><b>当前步骤:</b> {plan['current_step']}</p>"
        html += f"<p><b>计划ID:</b> {plan['plan_id']}</p>"
        html += "<ul>"
        for step in plan['steps']:
            html += f"<li>步骤{step['step_number']}: {step['title']} - 状态: {step['status']}"
            if step.get('detail'):
                html += f"<br>详情: {step['detail']}"
            if step.get('tech_solution'):
                html += f"<br>技术方案: {step['tech_solution']}"
            html += "</li>"
        html += "</ul>"
        html += "</div>"
    return html

@app.get("/", response_class=HTMLResponse)
def index():
    return '<a href="/plans">查看所有计划</a>' 
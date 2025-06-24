from setuptools import setup, find_packages

setup(
    name="todolist_mcp",
    version="0.1.0",
    description="A local MCP service for agent work plan management",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="你的名字",
    author_email="your@email.com",
    url="https://github.com/yourname/todolist_mcp",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "psutil",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "todolist-mcp = todolist_mcp.todolist_mcp:main"
        ]
    },
    include_package_data=True,
    python_requires=">=3.7",
    license="MIT",
) 
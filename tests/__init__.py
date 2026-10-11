"""FT Workspace 测试包（自动化测试入口）。

目录职责：
    api/   接口自动化测试（HTTP / FastAPI TestClient）
    ui/    UI 自动化测试（Playwright）
    unit/  单元测试（纯逻辑，如报价计算、数据清洗）
    data/  测试数据 fixture（YAML / JSON / CSV）

运行：
    .venv\\Scripts\\python -m pytest            # 全部
    .venv\\Scripts\\python -m pytest -m smoke   # 只跑冒烟
"""

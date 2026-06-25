"""
FT Workspace v3.0 — 一键启动脚本
用法: python run_web.py
"""
import uvicorn

if __name__ == "__main__":
    print("=" * 50)
    print("🔨 FT Workspace v3.0")
    print("🌐 http://localhost:8003")
    print("📖 API Docs: http://localhost:8003/docs")
    print("=" * 50)
    uvicorn.run("web.main:app", host="0.0.0.0", port=8003, reload=True, log_level="info")

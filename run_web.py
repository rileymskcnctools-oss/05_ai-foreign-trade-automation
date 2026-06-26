"""
FT Workspace v4.0 — 一键启动脚本
用法: python run_web.py
"""
import socket
import subprocess
import sys
import os
import time

API_PORT = 8020


def is_port_free(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("0.0.0.0", port))
            return True
        except OSError:
            return False


def kill_port_occupant(port):
    try:
        result = subprocess.run(["netstat", "-ano"], capture_output=True, text=True, timeout=5)
        for line in result.stdout.splitlines():
            if f":{port}" in line and "LISTENING" in line:
                pid = line.strip().split()[-1]
                if pid.isdigit() and int(pid) > 0:
                    print(f"  清理端口 {port} 进程 PID={pid}...")
                    subprocess.run(["taskkill", "/F", "/PID", pid], capture_output=True, timeout=5)
                    time.sleep(1)
                    return is_port_free(port)
    except Exception as e:
        print(f"  清理失败: {e}")
    return False


def ensure_port(port):
    if is_port_free(port):
        return port
    print(f"\n端口 {port} 被占用，尝试清理...")
    if kill_port_occupant(port):
        return port
    for p in range(port + 1, port + 20):
        if is_port_free(p):
            print(f"  使用替代端口: {p}")
            return p
    print("没有可用端口")
    sys.exit(1)


if __name__ == "__main__":
    frontend_dist = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend", "dist")
    if not os.path.exists(frontend_dist):
        print("Vue 前端未构建，正在自动构建...")
        subprocess.run(["npm", "run", "build"], cwd=os.path.join(os.path.dirname(__file__), "frontend"), shell=True)

    port = ensure_port(API_PORT)

    print("=" * 55)
    print("  FT Workspace v4.0 (Vue 3 + FastAPI)")
    print("=" * 55)
    print(f"  http://localhost:{port}")
    print(f"  API 文档: http://localhost:{port}/docs")
    print("=" * 55)
    print("  按 Ctrl+C 停止\n")

    subprocess.run([
        sys.executable, "-m", "uvicorn",
        "web.main_api:app",
        "--host", "0.0.0.0", "--port", str(port),
        "--reload",
    ])

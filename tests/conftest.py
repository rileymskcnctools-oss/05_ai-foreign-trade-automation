"""pytest 共享配置入口（脚手架，暂为空）。

这里放**所有测试目录共用**的 fixture，例如：

  - 被测应用的 TestClient（接口测试）
  - 指向独立临时数据库的 fixture
    —— 配合 `python scripts/seed_db.py --db <tmp>` 造可丢弃的测试数据，
       避免用例污染开发库 data/ft_workspace.db
  - 公共测试数据加载 / 用例前置与清理钩子
  - UI 测试用的浏览器实例（Playwright）

设计提醒：fixture 的**作用域**（function / module / session）直接决定
用例执行速度与数据隔离程度，是接口自动化的常见考点。

目前留空 —— 第一个 fixture 由你按需要添加。
"""

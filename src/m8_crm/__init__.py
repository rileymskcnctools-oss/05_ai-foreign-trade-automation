# m8_crm package
"""
M8: 客户CRM管理 (Client CRM)
完整的客户生命周期管理：录入、跟进、标签、提醒。

组件:
    - client_manager: 客户CRUD + 状态管理
    - activity_tracker: 跟进记录
    - tag_manager: 标签系统
    - reminder: 跟进提醒
"""
from .client_manager import ClientManager
from .activity_tracker import ActivityTracker
from .tag_manager import TagManager
from .reminder import FollowUpReminder

__all__ = ["ClientManager", "ActivityTracker", "TagManager", "FollowUpReminder"]

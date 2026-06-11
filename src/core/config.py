"""
FT Workspace v2.0 - 数字化系统“后台中央遥控器”
功能：专门负责把系统的“公开设置（YAML）”和“私密密码（.env）”合二为一加载进来。

AI运营视角：大模型的 API Key（密钥）就像公司的银行卡密码，绝对不能写死在代码里。
这个模块的作用就是把密码从“安全保险箱（.env）”里取出来，拼接到“公开说明书（settings.yaml）”中，供 AI 随时调用。
"""

import os
import re
from typing import Any, Optional

# 【环境依赖检测】：检查有没有安装专业的 YAML 解析器，如果没有，就用系统自带的平替方案
try:
    import yaml
except ImportError:
    yaml = None  
try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


class Config:
    """系统的【后台遥控器类】：负责安全读取各种配置与密码"""

    def __init__(self, config_path: Optional[str] = None, env_path: Optional[str] = None):
        """
        【第一步：拉下电闸，加载所有配置】
        业务场景：系统一启动，AI 运营脚本必须先通过这个函数知道“我的密钥是啥”、“文件该存到哪个文件夹”。
        """
        self._data = {}

        # 如果不指定路径，系统会自动在 config 文件夹下寻找“公开设置”和“私密密码”
        if config_path is None:
            config_path = self._find_file("config/settings.yaml")
        if env_path is None:
            env_path = self._find_file("config/.env")

        # 【核心动作 A】：如果保险箱（.env）文件存在，立刻悄悄把里面的敏感密钥（如 DeepSeek 密钥）读入电脑内存
        if os.path.exists(env_path) and load_dotenv:
            load_dotenv(env_path)

        # 【核心动作 B】：如果公开说明书（settings.yaml）存在，读取它，并把刚才的密码动态塞进去
        if os.path.exists(config_path):
            self._load_yaml(config_path)
        else:
            # 如果员工不小心把配置文件删了，系统自动启用“备用兜底方案”，保证系统不崩溃
            self._load_defaults()

    @staticmethod
    def _find_file(rel_path: str) -> str:
        """
        【文件探测卫星】：在电脑里自动寻找 config/ 文件夹的位置。
        运营价值：保证代码在任何人的电脑上都能一键运行，不需要人工手动去改绝对路径。
        """
        current = os.path.dirname(os.path.abspath(__file__))
        for _ in range(3):  # core -> src -> 项目根目录
            candidate = os.path.join(current, rel_path)
            if os.path.exists(candidate):
                return candidate
            current = os.path.dirname(current)
        return os.path.join(os.getcwd(), rel_path)

    def _load_yaml(self, path: str) -> None:
        """
        【魔术拼接器】：读取公开的 YAML 配置文件，并用正则表达式自动把里面的占位符 `${KEY}` 替换成真的密码。
        业务场景：YAML 里写着 `api_key: ${DEEPSEEK_API_KEY}`，这个函数会自动去内存里抓到真密码并把它换掉。
        """
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # 具体的替换魔术逻辑
        def replace_var(match):
            var_name = match.group(1) # 抓取到大括号里的名字（如 DEEPSEEK_API_KEY）
            # 去操作系统的安全内存里抓真密码，如果没抓到，就先保留原样
            return os.environ.get(var_name, match.group(0))

        # 用正则表达式完成全盘扫描和密码替换
        content = re.sub(r'\$\{(\w+)\}', replace_var, content)

        if yaml:
            # 如果有专业解析器，把这一堆文本变成 Python 能够直接查阅的“嵌套字典”
            self._data = yaml.safe_load(content) or {}
        else:
            # 【平替备胎】：万一没装 PyYAML 库，用下面自己写的简单解析器，确保系统依然能跑
            self._data = self._simple_parse(content)

    @staticmethod
    def _simple_parse(content: str) -> dict:
        """
        【手写简易解析器】：当电脑没装专业工具时，一行一行硬读 YAML 文本的兜底方案。
        （AI数据运营了解即可，不需要深究其每一行的字符串切割逻辑）
        """
        result = {}
        current_section = None
        for line in content.split("\n"):
            line = line.rstrip()
            if not line or line.startswith("#"): # 跳过空行和带有 # 的注释行
                continue
            # 判断是不是大分类（比如 app: 或 database:）
            if not line.startswith(" ") and line.endswith(":"):
                current_section = line[:-1].strip()
                result[current_section] = {}
                continue
            # 判断是不是分类下的具体设置（比如 name: "FT Workspace"）
            if ":" in line and current_section:
                key, _, value = line.partition(":")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if value:
                    result[current_section][key] = value
        return result

    def _load_defaults(self) -> None:
        """
        【出厂默认设置】：万一所有外置配置文件全丢了，系统自动在内存里生出一套标准外贸运营参数。
        运营价值：默认语言用英文（en），默认走通津港（Tianjin），默认用美元结算（USD），默认大模型用千问（qwen）。
        """
        self._data = {
            "app": {"name": "FT Workspace", "version": "2.0.0", "language": "en"},
            "database": {"path": "data/ft_workspace.db"},
            "llm": {"default_provider": "qwen"},
            "defaults": {"currency": "USD", "incoterm": "FOB", "port": "Tianjin"},
        }

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        【运营核心调用点一：打点取值法】
        业务场景：你想知道目前默认的交货港口是哪。你不需要翻箱倒柜，直接在脚本里写：
        `config.get("defaults.port")` 
        系统就会自动切开点号，层层深入，直接在后台大括号里给你吐出 `"Tianjin"`。如果找不到就返回默认值。
        """
        keys = key_path.split(".")
        value = self._data
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

    def get_api_key(self, provider: str) -> Optional[str]:
        """
        【运营核心调用点二：防呆取密钥机】
        业务场景：AI 准备发信了，向系统索要特定模型提供商（如 provider='deepseek'）的密钥。
        安全检查：如果发现 YAML 配置文件里写的是没修改的默认假密码（sk-your...）或者根本没写，
        系统会立刻启动 B 计划，去系统的 `.env` 环境里强制抓取 `DEEPSEEK_API_KEY`。
        """
        key = self.get(f"llm.providers.{provider}.api_key")
        if key and key.startswith("sk-your") or not key:
            env_key = os.environ.get(f"{provider.upper()}_API_KEY")
            if env_key:
                return env_key
            return None
        return key

    def get_db_path(self) -> str:
        """
        【账本位置直通车】：获取账本（数据库）应该放在哪。
        运营逻辑：从配置里读取数据库路径，如果是相对路径，自动结合项目根目录拼出绝对路径。
        """
        path = self.get("database.path", "data/ft_workspace.db")
        if not os.path.isabs(path):
            project_root = self._find_project_root()
            path = os.path.join(project_root, path)
        return path

    @staticmethod
    def _find_project_root() -> str:
        """定位项目根目录的辅助功能"""
        current = os.path.dirname(os.path.abspath(__file__))
        for _ in range(3):
            if os.path.isdir(os.path.join(current, "src")):
                return current
            current = os.path.dirname(current)
        return os.getcwd()

    def to_dict(self) -> dict:
        """将全部加载完毕的配置，打包成一个干净的大字典吐出来，方便拿去打印查阅"""
        return dict(self._data)


# ============================================================
# 【全球唯一化实例模式（Singleton）】
# ============================================================
_config_instance = None


def get_config(config_path: Optional[str] = None) -> Config:
    """
    【运营调用总开关】：在任何自动化流水线脚本里，想查配置，直接调用本函数。
    运营价值：确保整个外贸自动化系统在运行期间，永远只在内存里保留【一份】遥控器实例。
    这样可以极大节省电脑内存，且避免不同脚本之间读取的配置产生冲突。
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_path)
    return _config_instance
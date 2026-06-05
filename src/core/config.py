"""
FT Workspace v2.0 - Configuration Module

Loads settings from config/settings.yaml with .env variable substitution.
${VAR_NAME} placeholders are replaced from environment / .env file.
"""

import os
import re
from typing import Any, Optional

try:
    import yaml
except ImportError:
    yaml = None  # Will use simple parser fallback

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


class Config:
    """Application configuration with .env variable substitution."""

    def __init__(self, config_path: Optional[str] = None, env_path: Optional[str] = None):
        """
        Load configuration.

        Args:
            config_path: Path to settings.yaml. Auto-detected if None.
            env_path: Path to .env file. Auto-detected if None.
        """
        self._data = {}

        if config_path is None:
            config_path = self._find_file("config/settings.yaml")
        if env_path is None:
            env_path = self._find_file("config/.env")

        # Load .env if exists
        if os.path.exists(env_path) and load_dotenv:
            load_dotenv(env_path)

        # Load settings.yaml
        if os.path.exists(config_path):
            self._load_yaml(config_path)
        else:
            self._load_defaults()

    @staticmethod
    def _find_file(rel_path: str) -> str:
        """Find file by walking up from this module's directory."""
        current = os.path.dirname(os.path.abspath(__file__))
        # Go up from src/core/ to project root
        for _ in range(3):  # core -> src -> project_root
            candidate = os.path.join(current, rel_path)
            if os.path.exists(candidate):
                return candidate
            current = os.path.dirname(current)
        return os.path.join(os.getcwd(), rel_path)

    def _load_yaml(self, path: str) -> None:
        """Load YAML config with variable substitution."""
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # Substitute ${VAR_NAME} from environment
        def replace_var(match):
            var_name = match.group(1)
            return os.environ.get(var_name, match.group(0))

        content = re.sub(r'\$\{(\w+)\}', replace_var, content)

        if yaml:
            self._data = yaml.safe_load(content) or {}
        else:
            # Fallback: simple key-value parser for flat YAML
            self._data = self._simple_parse(content)

    @staticmethod
    def _simple_parse(content: str) -> dict:
        """Very simple YAML parser for fallback when PyYAML not installed."""
        result = {}
        current_section = None
        for line in content.split("\n"):
            line = line.rstrip()
            if not line or line.startswith("#"):
                continue
            # Section level (no leading spaces)
            if not line.startswith(" ") and line.endswith(":"):
                current_section = line[:-1].strip()
                result[current_section] = {}
                continue
            # Key-value level (indented)
            if ":" in line and current_section:
                key, _, value = line.partition(":")
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if value:
                    result[current_section][key] = value
        return result

    def _load_defaults(self) -> None:
        """Load default configuration when no file exists."""
        self._data = {
            "app": {"name": "FT Workspace", "version": "2.0.0", "language": "en"},
            "database": {"path": "data/ft_workspace.db"},
            "llm": {"default_provider": "qwen"},
            "defaults": {"currency": "USD", "incoterm": "FOB", "port": "Tianjin"},
        }

    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get a config value using dot notation.

        Example: config.get("llm.default_provider") -> "qwen"
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
        """Get API key for a specific LLM provider."""
        key = self.get(f"llm.providers.{provider}.api_key")
        if key and key.startswith("sk-your") or not key:
            env_key = os.environ.get(f"{provider.upper()}_API_KEY")
            if env_key:
                return env_key
            return None
        return key

    def get_db_path(self) -> str:
        """Get resolved database path."""
        path = self.get("database.path", "data/ft_workspace.db")
        if not os.path.isabs(path):
            # Resolve relative to project root
            project_root = self._find_project_root()
            path = os.path.join(project_root, path)
        return path

    @staticmethod
    def _find_project_root() -> str:
        """Find project root."""
        current = os.path.dirname(os.path.abspath(__file__))
        for _ in range(3):
            if os.path.isdir(os.path.join(current, "src")):
                return current
            current = os.path.dirname(current)
        return os.getcwd()

    def to_dict(self) -> dict:
        """Return full config as dict."""
        return dict(self._data)


# Singleton
_config_instance = None


def get_config(config_path: Optional[str] = None) -> Config:
    """Get or create the global config singleton."""
    global _config_instance
    if _config_instance is None:
        _config_instance = Config(config_path)
    return _config_instance

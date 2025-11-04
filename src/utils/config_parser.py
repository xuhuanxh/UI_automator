import yaml
import os
from typing import Dict, Any, Optional


class ConfigParser:
    _instance = None  # 单例模式

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_file: str = "config/config.yaml", env: str = None):
        """初始化配置解析器，支持多环境和环境变量配置"""
        # 默认配置
        self.default_config = {
            "base_url": "https://example.com",
            "browser": "chromium",
            "headless": True,
            "timeout": {
                "page_load": 30000,
                "element": 5000
            },
            "report": {
                "allure_results": "reports/allure-results",
                "screenshots": "screenshots"
            }
        }

        # 加载配置来源
        self.user_config = self._load_user_config(config_file)
        self.current_env = env or os.getenv("UI_AUTOMATION_ENV", "test")
        self.env_specific_config = self.user_config.get("environments", {}).get(self.current_env, {})
        self.env_var_config = self._load_from_env_vars()

        # 合并配置（优先级：环境变量 > 环境配置 > 用户配置 > 默认配置）
        self.config = self._merge_configs(
            self._merge_configs(
                self._merge_configs(self.default_config, self.user_config),
                self.env_specific_config
            ),
            self.env_var_config
        )

        # 验证配置合法性
        self._validate_config()

    def _load_user_config(self, config_file: str) -> Dict[str, Any]:
        """加载用户配置文件"""
        if not os.path.exists(config_file):
            return {}

        try:
            with open(config_file, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"配置文件解析错误: {config_file}, 错误: {e}")

    def _load_from_env_vars(self) -> Dict[str, Any]:
        """从环境变量加载配置（格式：UI_AUTOMATION_XXX_XXX）"""
        env_config = {}
        prefix = "UI_AUTOMATION_"
        for env_key, value in os.environ.items():
            if env_key.startswith(prefix):
                config_path = env_key[len(prefix):].lower().replace("_", ".")
                self._set_config_by_path(env_config, config_path, value)
        return env_config

    def _merge_configs(self, default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """递归合并配置字典"""
        merged = default.copy()
        for key, value in user.items():
            if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
                merged[key] = self._merge_configs(merged[key], value)
            else:
                merged[key] = value
        return merged

    def _set_config_by_path(self, config: Dict, path: str, value: Any) -> None:
        """通过路径设置嵌套配置"""
        parts = path.split(".")
        current = config
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value

    def _validate_config(self) -> None:
        """验证配置合法性"""
        # 检查必填项
        required = ["base_url", "browser", "timeout.page_load", "timeout.element"]
        for item in required:
            if self.get(item) is None:
                raise ValueError(f"缺少必要配置项: {item}")

        # 验证浏览器类型
        valid_browsers = ["chromium", "firefox", "webkit"]
        if self.get("browser") not in valid_browsers:
            raise ValueError(f"不支持的浏览器: {self.get('browser')}, 支持: {valid_browsers}")

    def get(self, path: str, default: Optional[Any] = None) -> Any:
        """通过路径获取配置值"""
        parts = path.split(".")
        current = self.config
        try:
            for part in parts:
                current = current[part]
            return current
        except (KeyError, TypeError):
            return default

    def get_all(self) -> Dict[str, Any]:
        """获取完整配置"""
        return self.config.copy()

    def update_from_cli(self, cli_args: Dict[str, Any]) -> None:
        """通过命令行参数更新配置"""
        cli_mapping = {
            "browser": "browser",
            "headless": "headless",
            "base_url": "base_url",
            "env": "current_env"
        }
        for cli_key, config_path in cli_mapping.items():
            if cli_key in cli_args and cli_args[cli_key] is not None:
                self._set_config_by_path(self.config, config_path, cli_args[cli_key])

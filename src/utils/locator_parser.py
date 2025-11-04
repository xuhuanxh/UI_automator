import yaml
import os
from typing import Dict


class LocatorParser:
    def __init__(self, locators_file: str = "config/locators.yaml"):
        """初始化定位器解析器"""
        self.locators_file = locators_file
        self.locators = self._load_locators()

    def _load_locators(self) -> Dict:
        """加载定位器配置文件"""
        if not os.path.exists(self.locators_file):
            raise FileNotFoundError(f"定位器文件不存在: {self.locators_file}")

        try:
            with open(self.locators_file, "r", encoding="utf-8") as f:
                locators = yaml.safe_load(f) or {}
                if not isinstance(locators, dict):
                    raise ValueError("定位器文件格式错误，应为字典类型")
                return locators
        except yaml.YAMLError as e:
            raise ValueError(f"定位器文件解析错误: {str(e)}")

    def get_locator(self, page_name: str, element_name: str) -> str:
        """获取指定页面元素的定位器表达式"""
        if page_name not in self.locators:
            raise KeyError(f"未找到页面配置: {page_name}")

        page_locators = self.locators[page_name]
        if element_name not in page_locators:
            raise KeyError(f"页面 {page_name} 中未找到元素: {element_name}")

        locator = page_locators[element_name]
        if not isinstance(locator, str) or not locator.strip():
            raise ValueError(f"元素 {page_name}.{element_name} 定位器为空或无效")

        return locator.strip()

    def get_page_url(self, page_name: str) -> str:
        """获取页面URL配置"""
        return self.get_locator(page_name, "url")

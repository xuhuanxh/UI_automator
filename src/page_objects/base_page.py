from playwright.sync_api import Page, Locator
from selenium.common import NoSuchElementException

from src.utils.locator_parser import LocatorParser
from src.utils.config_parser import ConfigParser

class BasePage:
    def __init__(self, page: Page, locator_parser: LocatorParser, config: ConfigParser, page_name: str):
        self.page = page
        self.locator_parser = locator_parser
        self.config = config
        self.page_name = page_name
        self.timeout = config.get("timeout.element")
        self.base_url = config.get("base_url")

    def get_locator(self, element_name: str) -> Locator:
        """获取页面元素"""
        locator_expr = self.locator_parser.get_locator(self.page_name, element_name)
        return self.page.locator(locator_expr)

    def load(self, url: str = None) -> None:
        """加载页面"""
        # 优先使用传入的URL，其次使用定位器中配置的URL，最后使用base_url
        target_url = url or self._get_page_url() or self.base_url
        if not target_url.startswith(("http", "https")):
            target_url = f"{self.base_url}{target_url}"
        self.page.goto(target_url, timeout=self.config.get("timeout.page_load"))
        self.wait_for_page_ready()

    def _get_page_url(self) -> str:
        """获取定位器中配置的页面URL"""
        try:
            return self.locator_parser.get_page_url(self.page_name)
        except KeyError:
            return None

    def wait_for_page_ready(self) -> None:
        """等待页面就绪"""
        self.page.wait_for_load_state("networkidle", timeout=self.timeout)

    def click(self, element_name: str) -> None:
        """点击元素"""
        self.get_locator(element_name).click(timeout=self.timeout)

    def fill(self, value: str, element_name: str) -> None:
        """输入文本"""
        self.get_locator(element_name).fill(value, timeout=self.timeout)

    def get_text(self, element_name: str) -> str:
        """获取元素文本"""
        return self.get_locator(element_name).text_content(timeout=self.timeout).strip()

    def is_visible(self, element_name: str) -> bool:
        """判断元素是否可见"""
        try:
            return self.get_locator(element_name).is_visible(timeout=self.timeout)
        except NoSuchElementException:
            return False
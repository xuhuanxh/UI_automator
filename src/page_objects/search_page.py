from src.page_objects.base_page import BasePage
from playwright.sync_api import Page
from src.utils.config_parser import ConfigParser
from src.utils.locator_parser import LocatorParser

class SearchPage(BasePage):
    def __init__(self, page: Page, locator_parser: LocatorParser, config_parser: ConfigParser):
        super().__init__(page, locator_parser, config_parser, "search_page")


    def perform_search(self, keyword: str) -> None:
        """执行搜索操作"""
        self.fill("search_input", keyword)
        self.click("search_button")
        self.page.wait_for_load_state("networkidle")

    def get_search_result_count(self) -> int:
        """获取搜索结果数量"""
        if not self.is_visible("results_container"):
            return 0
        return self.get_locator("result_item").count()

    def is_no_results_message_displayed(self) -> bool:
        """无结果提示是是否显示"""
        return self.is_visible("no_results_message")
from src.page_objects.base_page import BasePage
from playwright.sync_api import Page
from src.utils.config_parser import ConfigParser
from src.utils.locator_parser import LocatorParser

class LoginPage(BasePage):
    def __init__(self, page: Page, config: ConfigParser, locator_parser: LocatorParser):
        super().__init__(page, locator_parser, config, "login_page")

    def input_login_info(self, username: str, password: str):
        """输入登录信息"""
        self.fill("username_input", username)
        self.fill("password_input", password)

    def click_login_button(self) -> None:
        """点击登录按钮"""
        self.click("login_button")

    def get_error_message(self):
        """获取错误信息"""
        self.get_text("error_message")

    def is_login_success(self):
        """检查是否登录成功"""
        return self.is_visible("success_message")

    def is_error_message_visible(self):
        """检查错误信息是否显示"""
        return self.is_visible("error_message")
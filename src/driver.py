from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext
from src.utils.config_parser import ConfigParser


class Driver:
    def __init__(self, config: ConfigParser):
        self.config = config
        self.playwright = None
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None

    def start(self) -> Page:
        """启动浏览器并创建页面"""
        self.playwright = sync_playwright().start()

        # 根据配置选择浏览器
        browser_type = self.config.get("browser")
        browser_launcher = getattr(self.playwright, browser_type, None)
        if not browser_launcher:
            raise ValueError(f"不支持的浏览器类型: {browser_type}")

        # 启动浏览器
        self.browser = browser_launcher.launch(
            headless=self.config.get("headless"),
            args=["--start-maximized"] if browser_type == "chromium" else []
        )

        # 创建上下文和页面
        self.context = self.browser.new_context(viewport=None)  # 最大化窗口
        self.page = self.context.new_page()
        self.page.set_default_timeout(self.config.get("timeout.element"))

        return self.page

    def stop(self) -> None:
        """关闭浏览器和Playwright"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def get_page(self) -> Page:
        """获取当前页面对象"""
        return self.page

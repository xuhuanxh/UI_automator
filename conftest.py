import os
from typing import Any
import pytest
from src.driver import Driver
from src.test_case_runner import TestCaseRunner
from src.utils.config_parser import ConfigParser
from src.utils.locator_parser import LocatorParser
from src.page_objects.login_page import LoginPage
from src.page_objects.search_page import SearchPage

# 页面类映射，根据测试用例yaml文件中的page_object参数创建实例
PAGE_OBJECT_MAP = {
    "login_page": LoginPage,
    "search_page": SearchPage,
}

@pytest.fixture(scope="session")
def config():
    """全局config Fixture"""
    return ConfigParser()

@pytest.fixture(scope="session")
def locator_parser():
    """定位器解析器Fixture"""
    return LocatorParser()

@pytest.fixture(scope="function")
def driver(config):
    driver = Driver(config)
    driver.start()
    yield driver
    driver.stop()

@pytest.fixture(scope="function")
def page(driver):
    """页面对象"""
    return driver.get_page()

@pytest.fixture(scope="function")
def test_case_runner(page, config, request):
    """测试用例执行器fixture，根据测试用例动态创建页面对象"""
    # 从测试用例参数获取page_object名称
    page_object_name = request.node.params.get("page_object")
    if not page_object_name or page_object_name not in PAGE_OBJECT_MAP:
        raise ValueError(f"无效的页面对象：{page_object_name}")

    # 创建页面实例对象
    locator_parser = LocatorParser()
    page_object_class = PAGE_OBJECT_MAP[page_object_name]
    page_object = page_object_class(page, locator_parser, config)

    # 创建执行器
    return TestCaseRunner(page, config, page_object)

def pytest_addoption(parser):
    """添加命令行参数"""
    parser.addoption("--browser", help="指定浏览器类型：chromium, firefox, webkit")
    parser.addoption("--headless", type=bool, help="是否无头模式运行")
    parser.addoption("--base-url", help="测试目标的基础url")
    parser.addoption("--env", help="测试环境选择, dev, test, prod")

def pytest_configure(config):
    """配置pytest"""
    # 确保报告目录存在
    allure_result_dir = config.getoption("--alluredir") or "report/allure_results"
    os.makedirs(allure_result_dir, exist_ok=True)
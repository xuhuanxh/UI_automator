import os
import pytest
from src.utils.config_parser import ConfigParser
from src.driver import Driver
import argparse


def set_test_environment_vars():
    """临时设置测试环境变量（仅用于本地测试）"""
    os.environ["UI_AUTOMATION_LOGIN_USERNAME"] = "local_test_user"  # 对应 ${LOGIN.USERNAME}
    os.environ["UI_AUTOMATION_LOGIN_PASSWORD"] = "local_test_pass"  # 对应 ${LOGIN.PASSWORD}
    # 可添加其他需要的环境变量
    os.environ["UI_AUTOMATION_BASE_URL"] = "https://local-test.example.com"  # 覆盖默认base_url


def main():
    parser = argparse.ArgumentParser(description="支持环境指定的UI自动化测试运行器")
    parser.add_argument(
        "--env",
        type=str,
        default="test",  # 默认测试环境
        choices=["dev", "test", "prod"],  # 允许的环境选项
        help="指定测试环境（dev/test/prod），默认：test"
    )
    # 分离出--env参数和剩余的pytest参数
    args, remaining_pytest_args = parser.parse_known_args()

    # 1. 设置环境变量（在初始化配置前执行）
    set_test_environment_vars()

    # 2. 初始化配置（传入--env参数指定的环境）
    config = ConfigParser(env=args.env)

    # 3. 初始化驱动
    driver_manager = Driver(config)

    # 4. 构造pytest参数（合并固定参数和剩余参数）
    pytest_args = [
                      "tests/",
                      f"--browser={config.get('browser')}",
                      f"--headless={config.get('headless')}",
                      "--alluredir=reports/allure-results"
                  ] + remaining_pytest_args  # 附加传入的其他pytest参数（如-k、-s等）

    # 5. 运行测试
    try:
        pytest.main(pytest_args)
    finally:
        # 6. 关闭驱动
        driver_manager.stop()


if __name__ == "__main__":
    main()
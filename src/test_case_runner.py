import allure
from src.page_objects.base_page import BasePage
from src.utils.screenshot import take_screenshot
from src.utils.config_parser import ConfigParser


class TestCaseRunner:
    def __init__(self, page, config: ConfigParser, page_object: BasePage):
        self.page = page
        self.config = config
        self.page_object = page_object
        self.screenshot_dir = config.get("report.screenshots")

    def resolve_variable(self, value):
        """解析变量占位符（如${BASE_URL}）"""
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            var_name = value[2:-1]
            return self.config.get(var_name.lower()) or value
        return value

    def run_step(self, step):
        """执行单个测试步骤"""
        action = step.get("action")
        args = [self.resolve_variable(arg) for arg in step.get("args", [])]
        description = step.get("description", f"执行动作: {action}")

        with allure.step(description):
            try:
                # 页面加载动作
                if action == "load":
                    self.page_object.load(*args)

                # 调用页面对象方法
                elif action == "call_method":
                    if not args:
                        raise ValueError("call_method动作需要至少一个方法名参数")
                    method_name = args[0]
                    method_args = args[1:]
                    method = getattr(self.page_object, method_name, None)
                    if not method:
                        raise AttributeError(f"页面对象中未找到方法: {method_name}")
                    method(*method_args)

                # 断言：等于
                elif action == "assert_equal":
                    method_name = step.get("method")
                    expected = self.resolve_variable(step.get("expected"))
                    method = getattr(self.page_object, method_name, None)
                    if not method:
                        raise AttributeError(f"页面对象中未找到断言方法: {method_name}")
                    actual = method()
                    assert actual == expected, f"断言失败: 实际值[{actual}] != 预期值[{expected}]"

                # 断言：大于
                elif action == "assert_greater_than":
                    method_name = step.get("method")
                    expected = self.resolve_variable(step.get("expected"))
                    method = getattr(self.page_object, method_name, None)
                    if not method:
                        raise AttributeError(f"页面对象中未找到断言方法: {method_name}")
                    actual = method()
                    assert actual > expected, f"断言失败: 实际值[{actual}] 不大于 预期值[{expected}]"

                # 断言：为True
                elif action == "assert_true":
                    method_name = step.get("method")
                    method = getattr(self.page_object, method_name, None)
                    if not method:
                        raise AttributeError(f"页面对象中未找到断言方法: {method_name}")
                    result = method()
                    assert result is True, f"断言失败: 预期为True，实际为[{result}]"

                else:
                    raise ValueError(f"不支持的动作类型: {action}")

            except Exception as e:
                # 失败时截图并附加到报告
                screenshot_path = take_screenshot(
                    self.page,
                    self.screenshot_dir,
                    step_description=description
                )
                allure.attach.file(
                    screenshot_path,
                    name="失败截图",
                    attachment_type=allure.attachment_type.PNG
                )
                raise  # 重新抛出异常，标记测试失败

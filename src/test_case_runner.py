import allure
from src.page_objects.base_page import BasePage
from src.utils.screenshot import take_screenshot
from src.utils.config_parser import ConfigParser
from src.utils.data_generator import DataGenerator


class TestCaseRunner:
    def __init__(self, page, config: ConfigParser, page_object: BasePage):
        self.page = page
        self.config = config
        self.page_object = page_object
        self.screenshot_dir = config.get("report.screenshots")
        self.data_generator = DataGenerator()

    def resolve_variable(self, value):
        """解析变量占位符（如${BASE_URL}）"""
        if not isinstance(value, str) or not value.startswith("${") or not value.endswith("}"):
            return value
        var_name = value[2:-1]
        if var_name.startswith("RANDOM_"):
            return self._generate_dynamic_data(var_name)
        return self.config.get(var_name.lower()) or value

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

    def _generate_dynamic_data(self, var_name:str):
        """根据动态类型生成动态数据"""
        # 拆分类型和参数（如RANDOM_STRING:10 -> 类型=RANDOM_STRING，参数=10）
        parts = var_name.split(":", 1)
        data_type = parts[0]
        params = parts[1:] if len(parts) > 1 else ""

        # 映射数据类型到生成方法
        data_methods = {
            "RANDOM_STRING": self._handle_random_string,
            "RANDOM_EMAIL": lambda: self.data_generator.random_email(),
            "RANDOM_PHONE": lambda: self.data_generator.random_phone(),
            "RANDOM_INT": self._handle_random_int,
            "RANDOM_NAME": lambda: self.data_generator.random_name()
        }

        if data_type not in data_methods:
            raise ValueError(f"不支持的数据类型：{data_type}")

        return data_methods[data_type]()

    def _handle_random_string(self, params: str = "8"):
        """处理RANDOM_STRING"""
        try:
            length = int(params)
            return self.data_generator.random_string(length)
        except ValueError:
            raise ValueError(f"RANDOM_STRING参数格式错误，应为整数（如RANDOM_STRING:10），实际为: {params}")

    def _handle_random_int(self, params: str = "1-100"):
        """处理RANDOM_INT"""
        try:
            start, end = map(int, params.split("-"))
            return self.data_generator.random_int(start, end)
        except ValueError:
            raise ValueError(f"RANDOM_INT参数格式错误，应为start-end（如RANDOM_INT:1-10），实际为: {params}")
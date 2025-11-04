# UI自动化测试框架

基于 Python-Playwright、YAML 用例管理、Pytest 和 Allure 的 UI 自动化测试框架。

## 特性

- **页面对象模型(POM)**：封装页面元素和操作，提高代码复用性
- **YAML 用例**：非技术人员也能编写维护测试用例
- **多环境支持**：轻松切换开发/测试/生产环境
- **敏感配置保护**：通过环境变量注入敏感信息
- **自动截图**：测试失败自动截图并附加到报告
- **丰富报告**：集成 Allure 生成交互式测试报告
- **灵活配置**：支持命令行参数覆盖配置文件

## 项目结构
<img width="353" height="481" alt="image" src="https://github.com/user-attachments/assets/bef56109-319f-4cc7-907b-becc0bba3d5d" />

## 安装步骤

1. 克隆项目并进入目录
   ```bash
   git clone <repository-url>
   cd ui-automator
   ```

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 安装 Playwright 浏览器
   ```bash
   playwright install
   ```

4. 安装 Allure 报告工具
   - 参考官方文档：https://docs.qameta.io/allure/#_installing_a_commandline

## 配置说明

- `config/config.yaml`：全局配置，包括多环境设置
- `config/locators.yaml`：页面元素定位器
- 敏感配置（如账号密码）通过环境变量注入：
  ```bash
  # Linux/Mac
  export UI_AUTOMATION_LOGIN_USERNAME="testuser"
  export UI_AUTOMATION_LOGIN_PASSWORD="testpass"
  
  # Windows
  set UI_AUTOMATION_LOGIN_USERNAME=testuser
  set UI_AUTOMATION_LOGIN_PASSWORD=testpass
  ```

## 运行测试

### 基本命令# 直接运行
pytest

# 使用运行器脚本
python pytest_runner.py

# 生成并查看报告
allure serve reports/allure-results
### 常用参数# 指定浏览器
pytest --browser firefox

# 有头模式运行
pytest --headless false

# 切换环境
pytest --env prod

# 运行特定测试
pytest -k "test_login"
## 扩展框架

1. **添加新页面**：
   - 在 `src/page_objects/` 下创建新页面类（继承 BasePage）
   - 在 `config/locators.yaml` 中添加元素定位器

2. **添加新测试用例**：
   - 在 `tests/` 目录下创建新的 YAML 文件
   - 按照现有用例格式编写测试步骤

3. **添加新动作/断言**：
   - 在 `src/test_case_runner.py` 的 `run_step` 方法中添加处理逻辑

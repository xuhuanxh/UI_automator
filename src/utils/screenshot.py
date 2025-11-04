import os
from datetime import datetime
from playwright.sync_api import Page


def take_screenshot(page: Page, save_dir: str, step_description: str) -> str:
    """
    拍摄页面截图并保存
    :param page: Playwright Page对象
    :param save_dir: 保存目录
    :param step_description: 步骤描述（用于文件名）
    :return: 截图文件路径
    """
    # 确保目录存在
    os.makedirs(save_dir, exist_ok=True)

    # 生成唯一文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    safe_desc = "".join([c for c in step_description if c.isalnum() or c in " _-"]).strip()
    filename = f"screenshot_{timestamp}_{safe_desc}.png"
    filepath = os.path.join(save_dir, filename)

    # 保存截图
    page.screenshot(path=filepath, full_page=True)
    return filepath

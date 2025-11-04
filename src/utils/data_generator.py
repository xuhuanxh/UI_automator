import random
import string
from faker import Faker

class DataGenerator:
    def __init__(self):
        self.fake = Faker(locale='zh_CN')

    def random_string(self, length: int) -> str:
        """生成指定长度的随机字符串（字母+数字）"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def random_email(self) -> str:
        """生成随机email"""
        return self.fake.email()

    def random_phone(self) -> str:
        """生成随机手机号"""
        return self.fake.phone_number()

    def random_int(self, start: int, end: int) -> int:
        """生成随机整数"""
        return random.randint(start, end)

    def random_name(self) -> str:
        """生成随机姓名"""
        return self.fake.name()
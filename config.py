from dotenv import load_dotenv
import os
import sys
from logger import logging


class Config:
    def __init__(self):
        # 获取应用程序的根目录路径
        if getattr(sys, "frozen", False):
            # 如果是打包后的可执行文件
            application_path = os.path.dirname(sys.executable)
        else:
            # 如果是开发环境
            application_path = os.path.dirname(os.path.abspath(__file__))

        # 指定 .env 文件的路径
        dotenv_path = os.path.join(application_path, ".env")

        if not os.path.exists(dotenv_path):
            raise FileNotFoundError(f"文件 {dotenv_path} 不存在")

        # 加载 .env 文件
        load_dotenv(dotenv_path)

        self.imap = False

        # 处理 TEMP_MAIL（自动截断注释并提取用户名）
        temp_mail_value = os.getenv("TEMP_MAIL", "").split('#', 1)[0].strip()
        self.temp_mail = temp_mail_value.split("@")[0] if temp_mail_value else "null"

        # 处理其他带注释的环境变量
        self.temp_mail_epin = os.getenv("TEMP_MAIL_EPIN", "").split('#', 1)[0].strip()
        self.temp_mail_ext = os.getenv("TEMP_MAIL_EXT", "").split('#', 1)[0].strip()
        self.domain = os.getenv("DOMAIN", "").split('#', 1)[0].strip()

        # 如果临时邮箱为 null 则加载 IMAP
        if self.temp_mail.lower() == "null":  # 增加容错处理
            self.imap = True
            self.imap_server = os.getenv("IMAP_SERVER", "").split('#', 1)[0].strip()
            self.imap_port = os.getenv("IMAP_PORT", "").split('#', 1)[0].strip()
            self.imap_user = os.getenv("IMAP_USER", "").split('#', 1)[0].strip()
            self.imap_pass = os.getenv("IMAP_PASS", "").split('#', 1)[0].strip()
            self.imap_dir = os.getenv("IMAP_DIR", "inbox").split('#', 1)[0].strip().lower()

        self.check_config()

    def get_temp_mail(self):

        return self.temp_mail

    def get_temp_mail_epin(self):

        return self.temp_mail_epin

    def get_temp_mail_ext(self):

        return self.temp_mail_ext

    def get_imap(self):
        if not self.imap:
            return False
        return {
            "imap_server": self.imap_server,
            "imap_port": self.imap_port,
            "imap_user": self.imap_user,
            "imap_pass": self.imap_pass,
            "imap_dir": self.imap_dir,
        }

    def get_domain(self):
        return self.domain

    def get_protocol(self):
        """获取邮件协议类型
        
        Returns:
            str: 'IMAP' 或 'POP3'
        """
        return os.getenv('IMAP_PROTOCOL', 'POP3').split('#', 1)[0].strip()

    def check_config(self):
        """检查配置项是否有效

        检查规则：
        1. 如果使用 tempmail.plus，需要配置 TEMP_MAIL 和 DOMAIN
        2. 如果使用 IMAP，需要配置 IMAP_SERVER、IMAP_PORT、IMAP_USER、IMAP_PASS
        3. IMAP_DIR 是可选的
        """
        # 基础配置检查
        required_configs = {
            "domain": "域名",
        }

        # 检查基础配置
        for key, name in required_configs.items():
            if not self.check_is_valid(getattr(self, key)):
                raise ValueError(f"{name}未配置，请在 .env 文件中设置 {key.upper()}")

        # 检查邮箱配置
        if self.temp_mail != "null":
            # tempmail.plus 模式
            if not self.check_is_valid(self.temp_mail):
                raise ValueError("临时邮箱未配置，请在 .env 文件中设置 TEMP_MAIL")
        else:
            # IMAP 模式
            imap_configs = {
                "imap_server": "IMAP服务器",
                "imap_port": "IMAP端口",
                "imap_user": "IMAP用户名",
                "imap_pass": "IMAP密码",
            }

            for key, name in imap_configs.items():
                value = getattr(self, key)
                if value == "null" or not self.check_is_valid(value):
                    raise ValueError(
                        f"{name}未配置，请在 .env 文件中设置 {key.upper()}"
                    )

            # IMAP_DIR 是可选的，如果设置了就检查其有效性
            if self.imap_dir != "null" and not self.check_is_valid(self.imap_dir):
                raise ValueError(
                    "IMAP收件箱目录配置无效，请在 .env 文件中正确设置 IMAP_DIR"
                )

    def check_is_valid(self, value):
        """检查配置项是否有效

        Args:
            value: 配置项的值

        Returns:
            bool: 配置项是否有效
        """
        return isinstance(value, str) and len(str(value).strip()) > 0

    def print_config(self):
        if self.imap:
            logging.info(f"\033[32mIMAP服务器: {self.imap_server}\033[0m")
            logging.info(f"\033[32mIMAP端口: {self.imap_port}\033[0m")
            logging.info(f"\033[32mIMAP用户名: {self.imap_user}\033[0m")
            logging.info(f"\033[32mIMAP密码: {'*' * len(self.imap_pass)}\033[0m")
            logging.info(f"\033[32mIMAP收件箱目录: {self.imap_dir}\033[0m")
        if self.temp_mail != "null":
            logging.info(
                f"\033[32m临时邮箱: {self.temp_mail}{self.temp_mail_ext}\033[0m"
            )
        logging.info(f"\033[32m域名: {self.domain}\033[0m")


# 使用示例
if __name__ == "__main__":
    try:
        config = Config()
        print("环境变量加载成功！")
        config.print_config()
    except ValueError as e:
        print(f"错误: {e}")

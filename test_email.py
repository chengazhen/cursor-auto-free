import os
from dotenv import load_dotenv
from get_email_code import EmailVerificationHandler
import logging

def test_temp_mail():
    """测试临时邮箱方式"""
    handler = EmailVerificationHandler()
    print("\n=== 测试临时邮箱模式 ===")
    print(f"临时邮箱: {os.getenv('TEMP_MAIL')}@mailto.plus")
    code = handler.get_verification_code()
    if code:
        print(f"成功获取验证码: {code}")
    else:
        print("未能获取验证码")

def test_email_server():
    """测试邮箱服务器方式（POP3/IMAP）"""
    handler = EmailVerificationHandler()
    protocol = os.getenv('IMAP_PROTOCOL', 'POP3')
    print(f"\n=== 测试 {protocol} 模式 ===")
    print(f"邮箱服务器: {os.getenv('IMAP_SERVER')}")
    print(f"邮箱账号: {os.getenv('IMAP_USER')}")
    code = handler.get_verification_code()
    if code:
        print(f"成功获取验证码: {code}")
    else:
        print("未能获取验证码")

def print_config():
    """打印当前配置"""
    print("\n当前环境变量配置:")
    print(f"TEMP_MAIL: {os.getenv('TEMP_MAIL')}")
    if os.getenv('TEMP_MAIL') == 'null':
        print(f"IMAP_SERVER: {os.getenv('IMAP_SERVER')}")
        print(f"IMAP_PORT: {os.getenv('IMAP_PORT')}")
        print(f"IMAP_USER: {os.getenv('IMAP_USER')}")
        print(f"IMAP_PROTOCOL: {os.getenv('IMAP_PROTOCOL', 'POP3')}")
    print(f"DOMAIN: {os.getenv('DOMAIN')}")

def main():
    # 加载环境变量
    load_dotenv()
    
    # 打印初始配置
    print_config()
    
    try:
        # 根据配置决定测试哪种模式
        if os.getenv('TEMP_MAIL') != 'null':
            test_temp_mail()
        else:
            test_email_server()
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")

if __name__ == "__main__":
    main() 
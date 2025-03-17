import os

class Language:
    def __init__(self):
        self.current_language = "cn"  # Default language is Chinese
        self.translations = {
            "cn": {
                # System messages
                "error": "❌",
                "warning": "⚠️",
                "info": "ℹ️",
                
                # Main program flow messages
                "initializing_program": "\n=== 初始化程序 ===",
                "select_operation_mode": "\n请选择操作模式:",
                "reset_machine_code_only": "1. 仅重置机器码",
                "complete_registration": "2. 完整注册流程",
                "enter_option": "请输入选项 (1 或 2): ",
                "invalid_option": "无效的选项,请重新输入",
                "enter_valid_number": "请输入有效的数字",
                "machine_code_reset_complete": "机器码重置完成",
                "initializing_browser": "正在初始化浏览器...",
                "get_user_agent_failed": "获取user agent失败，使用默认值",
                "configuration_info": "\n=== 配置信息 ===",
                "generating_random_account": "正在生成随机账号信息...",
                "generated_email_account": "生成的邮箱账号: {email}",
                "initializing_email_verification": "正在初始化邮箱验证模块...",
                "starting_registration": "\n=== 开始注册流程 ===",
                "visiting_login_page": "正在访问登录页面: {url}",
                "getting_session_token": "正在获取会话令牌...",
                "updating_auth_info": "更新认证信息...",
                "resetting_machine_code": "重置机器码...",
                "all_operations_completed": "所有操作已完成",
                "session_token_failed": "获取会话令牌失败，注册流程未完成",
                "program_error": "程序执行出现错误: {error}",
                
                # Turnstile verification messages
                "detecting_turnstile": "正在检测 Turnstile 验证...",
                "verification_success": "验证成功 - 已到达{status}页面",
                "retry_verification": "第 {count} 次尝试验证",
                "detected_turnstile": "检测到 Turnstile 验证框，开始处理...",
                "turnstile_verification_passed": "Turnstile 验证通过",
                "verification_failed_max_retries": "验证失败 - 已达到最大重试次数 {max_retries}",
                "turnstile_exception": "Turnstile 验证过程发生异常: {error}",
                
                # Cookie and session messages
                "getting_cookie": "开始获取cookie",
                "cookie_attempt_failed": "第 {attempts} 次尝试未获取到CursorSessionToken，{retry_interval}秒后重试...",
                "cookie_max_attempts": "已达到最大尝试次数({max_attempts})，获取CursorSessionToken失败",
                "cookie_failure": "获取cookie失败: {error}",
                "retry_in_seconds": "将在 {seconds} 秒后重试...",
                
                # Account registration messages
                "start_account_registration": "=== 开始注册账号流程 ===",
                "visiting_registration_page": "正在访问注册页面: {url}",
                "filling_personal_info": "正在填写个人信息...",
                "input_first_name": "已输入名字: {name}",
                "input_last_name": "已输入姓氏: {name}",
                "input_email": "已输入邮箱: {email}",
                "submitting_personal_info": "提交个人信息...",
                "registration_page_access_failed": "注册页面访问失败: {error}",
                "setting_password": "正在设置密码...",
                "submitting_password": "提交密码...",
                "password_setup_complete": "密码设置完成，等待系统响应...",
                "password_setup_failed": "密码设置失败: {error}",
                "registration_failed_email_used": "注册失败：邮箱已被使用",
                "registration_success": "注册成功 - 已进入账户设置页面",
                "getting_email_verification": "正在获取邮箱验证码...",
                "verification_code_failure": "获取验证码失败",
                "verification_code_success": "成功获取验证码: {code}",
                "inputting_verification_code": "正在输入验证码...",
                "verification_code_input_complete": "验证码输入完成",
                "verification_code_process_error": "验证码处理过程出错: {error}",
                "waiting_system_processing": "等待系统处理中... 剩余 {seconds} 秒",
                "getting_account_info": "正在获取账户信息...",
                "account_usage_limit": "账户可用额度上限: {limit}",
                "registration_complete": "\n=== 注册完成 ===",
                "cursor_account_info": "Cursor 账号信息:\n邮箱: {email}\n密码: {password}",
                
                # Config related messages
                "imap_server": "IMAP服务器: {server}",
                "imap_port": "IMAP端口: {port}",
                "imap_username": "IMAP用户名: {username}",
                "imap_password": "IMAP密码: {password}",
                "imap_inbox_dir": "IMAP收件箱目录: {dir}",
                "temp_mail": "临时邮箱: {mail}",
                "domain": "域名: {domain}",
                
                # End messages
                "end_message": "=" * 30 + "\n所有操作已完成\n\n=== 获取更多信息 ===\n📺 B站UP主: 想回家的前端\n🔥 公众号: code 未来\n" + "=" * 30,
                
                # Error messages
                "file_not_exists": "文件 {path} 不存在",
                "domain_not_configured": "域名未配置，请在 .env 文件中设置 DOMAIN",
                "temp_mail_not_configured": "临时邮箱未配置，请在 .env 文件中设置 TEMP_MAIL",
                "imap_server_not_configured": "IMAP服务器未配置，请在 .env 文件中设置 IMAP_SERVER",
                "imap_port_not_configured": "IMAP端口未配置，请在 .env 文件中设置 IMAP_PORT",
                "imap_user_not_configured": "IMAP用户名未配置，请在 .env 文件中设置 IMAP_USER",
                "imap_pass_not_configured": "IMAP密码未配置，请在 .env 文件中设置 IMAP_PASS",
                "imap_dir_invalid": "IMAP收件箱目录配置无效，请在 .env 文件中正确设置 IMAP_DIR",
                
                # Language selection
                "select_language": "请选择语言 / Please select language:",
                "chinese": "1. 中文",
                "english": "2. English",
                "language_selected": "已选择中文作为系统语言",
                
                # System info
                "current_operating_system": "当前操作系统: {system}",
                "executing_macos_command": "执行macOS命令",
                "executing_linux_command": "执行Linux命令",
                "executing_windows_command": "执行Windows命令",
                "unsupported_operating_system": "不支持的操作系统: {system}",
                
                # Logging
                "logger_initialized": "日志系统初始化，日志目录: {dir}",
                "open_source_prefix": "[开源项目：https://github.com/chengazhen/cursor-auto-free] {msg}",
                "account_usage_info_failure": "获取账户额度信息失败: {error}",
                "env_variables_loaded": "环境变量加载成功！",
                "error_prefix": "错误: {error}",
                
                # Exit message
                "program_exit_message": "\n程序执行完毕，按回车键退出...",
                
                # File warnings
                "names_file_not_found": "未找到names-dataset.txt文件!"
            },
            "en": {
                # System messages
                "error": "❌",
                "warning": "⚠️",
                "info": "ℹ️",
                
                # Main program flow messages
                "initializing_program": "\n=== Initializing Program ===",
                "select_operation_mode": "\nPlease select operation mode:",
                "reset_machine_code_only": "1. Reset machine code only",
                "complete_registration": "2. Complete registration process",
                "enter_option": "Please enter option (1 or 2): ",
                "invalid_option": "Invalid option, please enter again",
                "enter_valid_number": "Please enter a valid number",
                "machine_code_reset_complete": "Machine code reset complete",
                "initializing_browser": "Initializing browser...",
                "get_user_agent_failed": "Failed to get user agent, using default value",
                "configuration_info": "\n=== Configuration Info ===",
                "generating_random_account": "Generating random account information...",
                "generated_email_account": "Generated email account: {email}",
                "initializing_email_verification": "Initializing email verification module...",
                "starting_registration": "\n=== Starting Registration Process ===",
                "visiting_login_page": "Visiting login page: {url}",
                "getting_session_token": "Getting session token...",
                "updating_auth_info": "Updating authentication information...",
                "resetting_machine_code": "Resetting machine code...",
                "all_operations_completed": "All operations completed",
                "session_token_failed": "Failed to get session token, registration process incomplete",
                "program_error": "Program execution error: {error}",
                
                # Turnstile verification messages
                "detecting_turnstile": "Detecting Turnstile verification...",
                "verification_success": "Verification successful - Reached {status} page",
                "retry_verification": "Attempt {count} of verification",
                "detected_turnstile": "Detected Turnstile verification box, starting processing...",
                "turnstile_verification_passed": "Turnstile verification passed",
                "verification_failed_max_retries": "Verification failed - Reached maximum retry count {max_retries}",
                "turnstile_exception": "Turnstile verification process exception: {error}",
                
                # Cookie and session messages
                "getting_cookie": "Starting to get cookies",
                "cookie_attempt_failed": "Attempt {attempts} failed to get CursorSessionToken, retrying in {retry_interval} seconds...",
                "cookie_max_attempts": "Reached maximum attempts ({max_attempts}), failed to get CursorSessionToken",
                "cookie_failure": "Failed to get cookie: {error}",
                "retry_in_seconds": "Will retry in {seconds} seconds...",
                
                # Account registration messages
                "start_account_registration": "=== Starting Account Registration Process ===",
                "visiting_registration_page": "Visiting registration page: {url}",
                "filling_personal_info": "Filling personal information...",
                "input_first_name": "Input first name: {name}",
                "input_last_name": "Input last name: {name}",
                "input_email": "Input email: {email}",
                "submitting_personal_info": "Submitting personal information...",
                "registration_page_access_failed": "Registration page access failed: {error}",
                "setting_password": "Setting password...",
                "submitting_password": "Submitting password...",
                "password_setup_complete": "Password setup complete, waiting for system response...",
                "password_setup_failed": "Password setup failed: {error}",
                "registration_failed_email_used": "Registration failed: Email already in use",
                "registration_success": "Registration successful - Entered account settings page",
                "getting_email_verification": "Getting email verification code...",
                "verification_code_failure": "Failed to get verification code",
                "verification_code_success": "Successfully got verification code: {code}",
                "inputting_verification_code": "Inputting verification code...",
                "verification_code_input_complete": "Verification code input complete",
                "verification_code_process_error": "Verification code process error: {error}",
                "waiting_system_processing": "Waiting for system processing... {seconds} seconds remaining",
                "getting_account_info": "Getting account information...",
                "account_usage_limit": "Account usage limit: {limit}",
                "registration_complete": "\n=== Registration Complete ===",
                "cursor_account_info": "Cursor account information:\nEmail: {email}\nPassword: {password}",
                
                # Config related messages
                "imap_server": "IMAP server: {server}",
                "imap_port": "IMAP port: {port}",
                "imap_username": "IMAP username: {username}",
                "imap_password": "IMAP password: {password}",
                "imap_inbox_dir": "IMAP inbox directory: {dir}",
                "temp_mail": "Temporary email: {mail}",
                "domain": "Domain: {domain}",
                
                # End messages
                "end_message": "=" * 30 + "\nAll operations completed\n\n=== Get More Information ===\n📺 Bilibili UP: 想回家的前端\n🔥 WeChat: code 未来\n" + "=" * 30,
                
                # Error messages
                "file_not_exists": "File {path} does not exist",
                "domain_not_configured": "Domain not configured, please set DOMAIN in .env file",
                "temp_mail_not_configured": "Temporary email not configured, please set TEMP_MAIL in .env file",
                "imap_server_not_configured": "IMAP server not configured, please set IMAP_SERVER in .env file",
                "imap_port_not_configured": "IMAP port not configured, please set IMAP_PORT in .env file",
                "imap_user_not_configured": "IMAP username not configured, please set IMAP_USER in .env file",
                "imap_pass_not_configured": "IMAP password not configured, please set IMAP_PASS in .env file",
                "imap_dir_invalid": "IMAP inbox directory configuration invalid, please set IMAP_DIR correctly in .env file",
                
                # Language selection
                "select_language": "请选择语言 / Please select language:",
                "chinese": "1. 中文",
                "english": "2. English",
                "language_selected": "English has been selected as the system language",
                
                # System info
                "current_operating_system": "Current operating system: {system}",
                "executing_macos_command": "Executing macOS command",
                "executing_linux_command": "Executing Linux command",
                "executing_windows_command": "Executing Windows command",
                "unsupported_operating_system": "Unsupported operating system: {system}",
                
                # Logging
                "logger_initialized": "Logger initialized, log directory: {dir}",
                "open_source_prefix": "[Open source project: https://github.com/chengazhen/cursor-auto-free] {msg}",
                "account_usage_info_failure": "Failed to get account usage information: {error}",
                "env_variables_loaded": "Environment variables loaded successfully!",
                "error_prefix": "Error: {error}",
                
                # Exit message
                "program_exit_message": "\nProgram execution completed, press Enter to exit...",
                
                # File warnings
                "names_file_not_found": "names-dataset.txt file not found!"
            }
        }
    
    def set_language(self, language_code):
        """Set the current language"""
        if language_code in self.translations:
            self.current_language = language_code
            return True
        return False
    
    def get(self, key, **kwargs):
        """Get translation for a key with optional format parameters"""
        if key not in self.translations[self.current_language]:
            # Fallback to Chinese if key not found in current language
            if key in self.translations["cn"]:
                text = self.translations["cn"][key]
            else:
                return f"[Missing translation: {key}]"
        else:
            text = self.translations[self.current_language][key]
        
        # Apply format if kwargs are provided
        if kwargs:
            try:
                return text.format(**kwargs)
            except KeyError as e:
                return f"{text} (FORMAT ERROR: {str(e)})"
        return text
    
    def select_language_prompt(self):
        """Display language selection prompt and return selected language code"""
        print(self.translations["cn"]["select_language"])
        print(self.translations["cn"]["chinese"])
        print(self.translations["cn"]["english"])
        
        while True:
            try:
                choice = int(input().strip())
                if choice == 1:
                    self.set_language("cn")
                    print(self.get("language_selected"))
                    return "cn"
                elif choice == 2:
                    self.set_language("en")
                    print(self.get("language_selected"))
                    return "en"
                else:
                    print(self.translations["cn"]["invalid_option"])
            except ValueError:
                print(self.translations["cn"]["enter_valid_number"])

# Global language instance
language = Language()

def get_translation(key, **kwargs):
    """Helper function to get translation"""
    return language.get(key, **kwargs)

# For direct testing
if __name__ == "__main__":
    language.select_language_prompt()
    print(get_translation("initializing_program"))
    print(get_translation("cursor_account_info", email="test@example.com", password="password123")) 
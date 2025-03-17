import platform
import os
import subprocess
from logger import logging
from language import get_translation

def go_cursor_help():
    system = platform.system()
    logging.info(get_translation("current_operating_system", system=system))
    
    base_url = "https://aizaozao.com/accelerate.php/https://raw.githubusercontent.com/yuaotian/go-cursor-help/refs/heads/master/scripts/run"
    
    if system == "Darwin":  # macOS
        cmd = f'curl -fsSL {base_url}/cursor_mac_id_modifier.sh | sudo bash'
        logging.info(get_translation("executing_macos_command"))
        os.system(cmd)
    elif system == "Linux":
        cmd = f'curl -fsSL {base_url}/cursor_linux_id_modifier.sh | sudo bash'
        logging.info(get_translation("executing_linux_command"))
        os.system(cmd)
    elif system == "Windows":
        cmd = f'irm {base_url}/cursor_win_id_modifier.ps1 | iex'
        logging.info(get_translation("executing_windows_command"))
        # Use PowerShell to execute command on Windows
        subprocess.run(["powershell", "-Command", cmd], shell=True)
    else:
        logging.error(get_translation("unsupported_operating_system", system=system))
        return False
    
    return True

import warnings
import os
import platform
import subprocess
import time
import threading

# Ignore specific SyntaxWarning
warnings.filterwarnings("ignore", category=SyntaxWarning, module="DrissionPage")

CURSOR_LOGO = """
   ██████╗██╗   ██╗██████╗ ███████╗ ██████╗ ██████╗ 
  ██╔════╝██║   ██║██╔══██╗██╔════╝██╔═══██╗██╔══██╗
  ██║     ██║   ██║██████╔╝███████╗██║   ██║██████╔╝
  ██║     ██║   ██║██╔══██╗╚════██║██║   ██║██╔══██╗
  ╚██████╗╚██████╔╝██║  ██║███████║╚██████╔╝██║  ██║
   ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝
"""


class LoadingAnimation:
    def __init__(self):
        self.is_running = False
        self.animation_thread = None

    def start(self, message="Building"):
        self.is_running = True
        self.animation_thread = threading.Thread(target=self._animate, args=(message,))
        self.animation_thread.start()

    def stop(self):
        self.is_running = False
        if self.animation_thread:
            self.animation_thread.join()
        print("\r" + " " * 70 + "\r", end="", flush=True)  # Clear the line

    def _animate(self, message):
        animation = "|/-\\"
        idx = 0
        while self.is_running:
            print(f"\r{message} {animation[idx % len(animation)]}", end="", flush=True)
            idx += 1
            time.sleep(0.1)


def print_logo():
    print("\033[96m" + CURSOR_LOGO + "\033[0m")
    print("\033[93m" + "Building Cursor Keep Alive...".center(56) + "\033[0m\n")


def progress_bar(progress, total, prefix="", length=50):
    filled = int(length * progress // total)
    bar = "█" * filled + "░" * (length - filled)
    percent = f"{100 * progress / total:.1f}"
    print(f"\r{prefix} |{bar}| {percent}% Complete", end="", flush=True)
    if progress == total:
        print()


def simulate_progress(message, duration=1.0, steps=20):
    print(f"\033[94m{message}\033[0m")
    for i in range(steps + 1):
        time.sleep(duration / steps)
        progress_bar(i, steps, prefix="Progress:", length=40)


def filter_output(output):
    """ImportantMessage"""
    if not output:
        return ""
    important_lines = []
    for line in output.split("\n"):
        # Only keep lines containing specific keywords
        if any(
            keyword in line.lower()
            for keyword in ["error:", "failed:", "completed", "directory:"]
        ):
            important_lines.append(line)
    return "\n".join(important_lines)


def build():
    # Clear screen
    os.system("cls" if platform.system().lower() == "windows" else "clear")

    # Print logo
    print_logo()

    system = platform.system().lower()
    spec_file = os.path.join("CursorKeepAlive.spec")

    # if system not in ["darwin", "windows"]:
    #     print(f"\033[91mUnsupported operating system: {system}\033[0m")
    #     return

    output_dir = f"dist/{system if system != 'darwin' else 'mac'}"

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    simulate_progress("Creating output directory...", 0.5)

    # Run PyInstaller with loading animation
    pyinstaller_command = [
        "pyinstaller",
        spec_file,
        "--distpath",
        output_dir,
        "--workpath",
        f"build/{system}",
        "--noconfirm",
    ]

    loading = LoadingAnimation()
    try:
        simulate_progress("Running PyInstaller...", 2.0)
        loading.start("Building in progress")
        result = subprocess.run(
            pyinstaller_command, check=True, capture_output=True, text=True
        )
        loading.stop()

        if result.stderr:
            filtered_errors = [
                line
                for line in result.stderr.split("\n")
                if any(
                    keyword in line.lower()
                    for keyword in ["error:", "failed:", "completed", "directory:"]
                )
            ]
            if filtered_errors:
                print("\033[93mBuild Warnings/Errors:\033[0m")
                print("\n".join(filtered_errors))

    except subprocess.CalledProcessError as e:
        loading.stop()
        print(f"\033[91mBuild failed with error code {e.returncode}\033[0m")
        if e.stderr:
            print("\033[91mError Details:\033[0m")
            print(e.stderr)
        return
    except FileNotFoundError:
        loading.stop()
        print(
            "\033[91mError: Please ensure PyInstaller is installed (pip install pyinstaller)\033[0m"
        )
        return
    except KeyboardInterrupt:
        loading.stop()
        print("\n\033[91mBuild cancelled by user\033[0m")
        return
    finally:
        loading.stop()

    # Copy config file
    if os.path.exists("config.ini.example"):
        simulate_progress("Copying configuration file...", 0.5)
        if system == "windows":
            subprocess.run(
                ["copy", "config.ini.example", f"{output_dir}\\config.ini"], shell=True
            )
        else:
            subprocess.run(["cp", "config.ini.example", f"{output_dir}/config.ini"])

    # Copy .env file or .env.example if .env doesn't exist
    env_file = ".env" if os.path.exists(".env") else ".env.example"
    if os.path.exists(env_file):
        simulate_progress(f"Copying {'example ' if env_file == '.env.example' else ''}environment file...", 0.5)
        copy_command = "copy" if system == "windows" else "cp"
        subprocess.run([copy_command, env_file, f"{output_dir}/.env"], shell=(system == "windows"))

    print(
        f"\n\033[92mBuild completed successfully! Output directory: {output_dir}\033[0m"
    )


if __name__ == "__main__":
    build()

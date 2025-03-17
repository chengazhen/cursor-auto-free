import logging
import os
from datetime import datetime
try:
    from language import get_translation
except ImportError:
    # If language module is not yet imported (circular import prevention)
    def get_translation(key, **kwargs):
        if key == "open_source_prefix":
            return "[Open source project: https://github.com/chengazhen/cursor-auto-free] {msg}"
        elif key == "logger_initialized":
            return "Logger initialized, log directory: {dir}"
        return key

# Configure logging
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


class PrefixFormatter(logging.Formatter):
    """Custom formatter that adds an open source project prefix to DEBUG level logs"""

    def format(self, record):
        if record.levelno == logging.DEBUG:  # Only add prefix to DEBUG level
            record.msg = get_translation("open_source_prefix", msg=record.msg)
        return super().format(record)


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log"),
            encoding="utf-8",
        ),
    ],
)

# Set custom formatter for file handlers
for handler in logging.getLogger().handlers:
    if isinstance(handler, logging.FileHandler):
        handler.setFormatter(
            PrefixFormatter("%(asctime)s - %(levelname)s - %(message)s")
        )


# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(PrefixFormatter("%(message)s"))

# Add the console handler to the logger
logging.getLogger().addHandler(console_handler)

# Print log directory path
logging.info(get_translation("logger_initialized", dir=os.path.abspath(log_dir)))


def main_task():
    """
    Main task execution function. Simulates a workflow and handles errors.
    """
    try:
        logging.info("Starting the main task...")

        # Simulated task and error condition
        if some_condition():
            raise ValueError("Simulated error occurred.")

        logging.info("Main task completed successfully.")

    except ValueError as ve:
        logging.error(f"ValueError occurred: {ve}", exc_info=True)
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}", exc_info=True)
    finally:
        logging.info("Task execution finished.")


def some_condition():
    """
    Simulates an error condition. Returns True to trigger an error.
    Replace this logic with actual task conditions.
    """
    return True


if __name__ == "__main__":
    # Application workflow
    logging.info("Application started.")
    main_task()
    logging.info("Application exited.")

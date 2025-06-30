import logging
import sys

# Define a custom formatter for our logs
class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    
    # Define the format for log messages
    # asctime: timestamp
    # name: logger name (e.g., agent_service.main)
    # levelname: log level (INFO, WARNING, ERROR, etc.)
    # message: the log message itself
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def setup_logging():
    """
    Sets up the logging configuration for the application.
    """
    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO) # Set default level to INFO

    # Clear existing handlers to prevent duplicate logs if reloaded
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CustomFormatter())
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler('app.log')
    file_handler.setFormatter(CustomFormatter())
    logger.addHandler(file_handler)

    # Set specific log levels for noisy libraries if needed
    logging.getLogger("uvicorn").setLevel(logging.WARNING) # Uvicorn's default INFO logs are often too verbose
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING) # Anthropic client uses httpx
    logging.getLogger("httpcore").setLevel(logging.WARNING) # Anthropic client uses httpcore

    # Get a logger for this specific module
    logging.getLogger(__name__).info("Logging configured!")

# Call setup_logging when this module is imported
setup_logging()
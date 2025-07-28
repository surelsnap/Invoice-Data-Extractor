import logging
from config.settings import Config

def configure_logging():
    """Configure logging settings"""
    logging.basicConfig(
        level=Config.LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )

# Create module-level logger
logger = logging.getLogger(__name__)
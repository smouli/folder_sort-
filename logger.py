import logging
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(f'document_classifier_{datetime.now().strftime("%Y%m%d")}.log')
    ]
)

# Create logger instance
logger = logging.getLogger('document_classifier')

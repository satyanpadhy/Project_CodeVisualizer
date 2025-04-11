import logging
import os
from datetime import datetime

def setup_logger(config):
    """Set up the logging configuration."""
    log_directory = os.path.join(config.output_directory, 'logs')
    os.makedirs(log_directory, exist_ok=True)
    
    log_filename = f'codebase_analyzer_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    log_path = os.path.join(log_directory, log_filename)
    
    logging.basicConfig(
        level=getattr(logging, config.log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger('codebase_analyzer')
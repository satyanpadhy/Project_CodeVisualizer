import sys
import os
from datetime import datetime

class DebugLogger:
    def __init__(self):
        self.log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output', 'logs')
        os.makedirs(self.log_dir, exist_ok=True)
        self.log_file = os.path.join(self.log_dir, f'debug_{datetime.now().strftime("%Y%m%d")}.log')

    def debug(self, message: str, flush: bool = True):
        """Print debug message to console and file with immediate flush."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        debug_msg = f"DEBUG [{timestamp}]: {message}"
        
        # Print to stderr for immediate visibility
        print(message, flush=flush)
        
        # Write to log file
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(debug_msg + '\n')
                if flush:
                    f.flush()
                    os.fsync(f.fileno())
        except Exception as e:
            print(f"Error writing to debug log: {e}", file=sys.stderr)

# Create a singleton instance
_logger = DebugLogger()
debug = _logger.debug